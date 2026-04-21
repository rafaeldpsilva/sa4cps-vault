"""
Systematic review screener — title + abstract pass (rule-based).
Reads all .bib files from review-bib/, deduplicates, applies keyword-based
inclusion/exclusion criteria, and outputs screening_results.csv.

Revised criteria (v2):
  IC3 — any AI method (ML, RL, KG, GNN, LLM, Bayesian, etc.)
         Method type (relational / generative / general) is recorded for synthesis.
  IC4 — any occupant preference, behavioral pattern, latent intent, or
         collective dynamic beyond physical setpoints (broader than personality/traits)
  IC5 — built environment context (unchanged)
  EC1 — environment-only with no occupant preference/intent layer
  EC2 — web-platform profiling with no built-environment application
  EC3 — removed as a keyword-detectable gate (unreliable from title/abstract alone)
  EC4 — non-full paper / no abstract
  EC5 — published before 2019

Decisions:
  INCLUDE   — IC3 + IC4 + IC5 met, no hard exclusion
  EXCLUDE   — at least one EC triggered
  UNCERTAIN — not clearly in or out; needs manual review
"""

import csv
import os
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Keyword sets
# ---------------------------------------------------------------------------

GENERATIVE_AI = [
    "large language model", "llm", "gpt", "chatgpt", "generative ai",
    "foundation model", "bert", "transformer-based", "natural language processing",
    "nlp", "language model", "generative model", "multimodal ai",
    "retrieval-augmented", "rag", "in-context learning",
]

RELATIONAL_AI = [
    "knowledge graph", "graph neural network", "gnn", "ontology", "ontologies",
    "semantic web", "heterogeneous graph", "heterogeneous network",
    "relational embedding", "graph-based", "knowledge base", "graph convolutional",
    "graph attention", "knowledge representation", "knowledge-enhanced",
    "semantic model", "linked data",
]

GENERAL_AI = [
    "machine learning", "deep learning", "neural network", "reinforcement learning",
    "bayesian", "probabilistic model", "federated learning", "transfer learning",
    "random forest", "decision tree", "clustering", "classification",
    "regression model", "support vector", "attention mechanism",
    "convolutional network", "recurrent network", "lstm", "autoencoder",
    "diffusion model", "embedding", "recommendation algorithm",
    "collaborative filtering", "matrix factorization",
]

# IC4 — broader occupant human dimension (preferences, intent, behavior, collective)
HUMAN_DIMENSION = [
    # Preferences
    "user preference", "occupant preference", "resident preference",
    "preference modeling", "preference learning", "preference profile",
    "preference elicitation", "preference inference",
    # Behavioral / profiling
    "user profile", "user profil", "user model", "occupant model",
    "behavioral pattern", "behavior model", "behavioral model",
    "user behavior", "occupant behavior",
    # Intent / proactive
    "latent intent", "intent inference", "intent recognition",
    "proactive", "anticipatory", "implicit feedback",
    # Interaction style / modality
    "interaction style", "interaction modality", "interaction preference",
    # Psychological / personality (retained from v1)
    "personality", "cognitive model", "psychographic", "big five", "mbti",
    "user expectation", "trust level", "behavioral archetype",
    # Temporal / dynamic
    "dynamic profile", "profile evolution", "preference evolution",
    "temporal preference", "contextual preference", "context-aware",
    # Collective / multi-user
    "group preference", "collective preference", "multi-user",
    "shared preference", "preference conflict", "preference negotiation",
]

BUILT_ENV = [
    "smart building", "smart home", "intelligent building", "intelligent environment",
    "smart environment", "built environment", "ambient intelligence", "smart communit",
    "smart space", "smart office", "smart city", "iot", "cyber-physical",
    "home automation", "building automation", "intelligent home", "smart room",
    "indoor environment", "occupant", "building occupant",
]

ENV_ONLY = [
    "thermal comfort", "occupancy detection", "occupancy sensing", "energy consumption",
    "hvac", "temperature control", "heating system", "cooling system",
    "energy efficiency", "energy management", "demand response", "energy optimization",
]

WEB_PLATFORM = [
    "social media", "ad targeting", "advertisement targeting", "e-commerce",
    "sentiment analysis", "web platform", "online platform", "social network analysis",
    "click-through rate", "news recommendation", "movie recommendation",
    "social recommendation", "product recommendation", "twitter", "facebook",
    "instagram", "weibo", "tiktok", "youtube recommendation",
]

NON_PAPER = [
    "workshop summary", "workshop program", "keynote", "editorial",
    "book chapter", "tutorial", "demo paper", "extended abstract", "poster paper",
    "welcome and committee", "workshop welcome",
]

# ---------------------------------------------------------------------------
# BibTeX parser
# ---------------------------------------------------------------------------

def parse_bib(filepath: Path) -> list[dict]:
    text = filepath.read_text(encoding="utf-8", errors="replace")
    entries = []
    raw_entries = re.split(r"(?=@\w+\s*\{)", text)
    for raw in raw_entries:
        raw = raw.strip()
        if not raw or raw.startswith("@string") or raw.startswith("@String"):
            continue
        entry = {"_source": filepath.stem, "_raw_type": ""}

        m = re.match(r"@(\w+)\s*\{", raw, re.IGNORECASE)
        if m:
            entry["_raw_type"] = m.group(1).lower()

        for field in ["title", "abstract", "year", "doi", "author",
                      "booktitle", "journal", "keywords"]:
            pattern = rf"(?i)\b{field}\s*=\s*[{{\"](.*?)[}}\"](?:\s*,|\s*\}})"
            fm = re.search(pattern, raw, re.DOTALL)
            if fm:
                entry[field] = re.sub(r"\s+", " ", fm.group(1).strip())
            else:
                pattern2 = rf"(?i)\b{field}\s*=\s*\{{(.*?)\}}(?:\s*,|\s*\}})"
                fm2 = re.search(pattern2, raw, re.DOTALL)
                entry[field] = re.sub(r"\s+", " ", fm2.group(1).strip()) if fm2 else ""

        entries.append(entry)
    return entries


def clean_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(entries: list[dict]) -> list[dict]:
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()
    unique = []
    for e in entries:
        doi = e.get("doi", "").strip().lower()
        title_key = clean_title(e.get("title", ""))
        if doi and doi in seen_dois:
            continue
        if title_key and title_key in seen_titles:
            continue
        if doi:
            seen_dois.add(doi)
        if title_key:
            seen_titles.add(title_key)
        unique.append(e)
    return unique


# ---------------------------------------------------------------------------
# Screener
# ---------------------------------------------------------------------------

def hits(text: str, terms: list[str]) -> list[str]:
    text_lower = text.lower()
    return [t for t in terms if t in text_lower]


def method_type(gen_hits, rel_hits, gen_ai_hits) -> str:
    """Return a label describing the method type found, for synthesis."""
    types = []
    if rel_hits:
        types.append("relational")
    if gen_hits:
        types.append("generative")
    if gen_ai_hits and not (rel_hits or gen_hits):
        types.append("general-ml")
    return "+".join(types) if types else "unknown"


def screen(entry: dict) -> tuple[str, str]:
    title = entry.get("title", "")
    abstract = entry.get("abstract", "")
    combined = (title + " " + abstract).lower()
    year_str = entry.get("year", "")
    entry_type = entry.get("_raw_type", "")

    # EC4 — no abstract
    if not abstract.strip():
        return "EXCLUDE", "EC4 – no abstract available"

    # EC4 — non-paper entry type
    if entry_type in ("misc", "phdthesis", "mastersthesis", "techreport", "unpublished"):
        return "EXCLUDE", "EC4 – non-paper type"
    if hits(combined, NON_PAPER):
        return "EXCLUDE", "EC4 – workshop summary / non-full paper"

    # EC5 — year
    try:
        year = int(re.sub(r"\D", "", year_str))
        if year < 2019:
            return "EXCLUDE", f"EC5 – published before 2019 ({year})"
    except (ValueError, TypeError):
        pass

    # EC2 — web platform with no built environment anchor
    web_hits = hits(combined, WEB_PLATFORM)
    built_hits = hits(combined, BUILT_ENV)
    if web_hits and not built_hits:
        return "EXCLUDE", f"EC2 – web/social platform context ({', '.join(web_hits[:2])})"

    # EC1 — environment-only (no occupant preference/intent layer)
    env_hits = hits(combined, ENV_ONLY)
    human_hits = hits(combined, HUMAN_DIMENSION)
    if env_hits and not human_hits:
        return "EXCLUDE", f"EC1 – environment-only modeling ({', '.join(env_hits[:2])})"

    # IC3 — any AI method (relational, generative, or general ML)
    gen_hits   = hits(combined, GENERATIVE_AI)
    rel_hits   = hits(combined, RELATIONAL_AI)
    genai_hits = hits(combined, GENERAL_AI)
    has_method = bool(gen_hits or rel_hits or genai_hits)

    # IC4 — occupant preference / behavioral / intent dimension
    has_human = bool(human_hits)

    # IC5 — built environment
    has_context = bool(built_hits)

    if has_method and has_human and has_context:
        mtype = method_type(gen_hits, rel_hits, genai_hits)
        method_label = (gen_hits[:1] or rel_hits[:1] or genai_hits[:1])[0]
        return "INCLUDE", (
            f"IC3({mtype}: {method_label}) + "
            f"IC4({human_hits[0]}) + "
            f"IC5({built_hits[0]})"
        )

    # Partial matches → UNCERTAIN
    missing = []
    if not has_method:
        missing.append("no AI method detected")
    if not has_human:
        missing.append("no occupant preference/intent dimension detected")
    if not has_context:
        missing.append("no built environment context detected")
    return "UNCERTAIN", "; ".join(missing)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    bib_dir = Path(__file__).parent / "review-bib"
    out_path = Path(__file__).parent / "screening_results.csv"

    all_entries: list[dict] = []
    for bib_file in sorted(bib_dir.glob("*.bib")):
        parsed = parse_bib(bib_file)
        all_entries.extend(parsed)
        print(f"  {bib_file.name}: {len(parsed)} entries")

    print(f"\nTotal before dedup: {len(all_entries)}")
    unique = deduplicate(all_entries)
    print(f"Total after dedup:  {len(unique)}")

    results = []
    counts = {"INCLUDE": 0, "EXCLUDE": 0, "UNCERTAIN": 0}
    for i, entry in enumerate(unique, 1):
        decision, reason = screen(entry)
        counts[decision] += 1
        results.append({
            "id": i,
            "source": entry.get("_source", ""),
            "year": entry.get("year", ""),
            "title": entry.get("title", ""),
            "decision": decision,
            "reason": reason,
            "doi": entry.get("doi", ""),
        })

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "source", "year", "title",
                                               "decision", "reason", "doi"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults written to {out_path}")
    print(f"  INCLUDE:   {counts['INCLUDE']}")
    print(f"  EXCLUDE:   {counts['EXCLUDE']}")
    print(f"  UNCERTAIN: {counts['UNCERTAIN']}")


if __name__ == "__main__":
    main()
