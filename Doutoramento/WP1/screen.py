"""
Systematic review screener — title + abstract pass.
Reads all .bib files from review-bib/, deduplicates, applies keyword-based
inclusion/exclusion criteria, and outputs screening_results.csv.

Decisions:
  INCLUDE    — hits IC3 + IC4 + IC5 with no hard exclusion
  EXCLUDE    — hits at least one exclusion criterion (EC1–EC5)
  UNCERTAIN  — does not clearly match either; needs manual review
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
    "nlp", "language model", "generative model",
]

RELATIONAL_AI = [
    "knowledge graph", "graph neural network", "gnn", "ontology", "ontologies",
    "semantic web", "heterogeneous graph", "heterogeneous network",
    "relational embedding", "graph-based", "knowledge base", "graph convolutional",
    "graph attention", "knowledge representation",
]

HUMAN_DIMENSION = [
    "personality", "interaction style", "interaction modality", "user expectation",
    "cognitive model", "behavioral archetype", "psychographic", "big five",
    "mbti", "trust level", "user preference", "user profile", "user model",
    "preference modeling", "preference learning", "occupant preference",
    "resident preference", "occupant model", "user behavior model",
]

BUILT_ENV = [
    "smart building", "smart home", "intelligent building", "intelligent environment",
    "smart environment", "built environment", "ambient intelligence", "smart communit",
    "smart space", "smart office", "smart city", "iot", "cyber-physical",
    "home automation", "building automation", "intelligent home",
]

ENV_ONLY = [
    "thermal comfort", "occupancy detection", "occupancy sensing", "energy consumption",
    "hvac", "temperature control", "heating system", "cooling system",
    "energy efficiency", "energy management", "demand response",
]

WEB_PLATFORM = [
    "social media", "ad targeting", "advertisement targeting", "e-commerce",
    "sentiment analysis", "web platform", "online platform", "social network analysis",
    "click-through rate", "news recommendation", "movie recommendation",
]

NON_PAPER = [
    "workshop summary", "keynote", "editorial", "book chapter", "tutorial",
    "demo paper", "extended abstract", "poster paper",
]

# ---------------------------------------------------------------------------
# BibTeX parser
# ---------------------------------------------------------------------------

def parse_bib(filepath: Path) -> list[dict]:
    text = filepath.read_text(encoding="utf-8", errors="replace")
    entries = []
    # Split on entry starts
    raw_entries = re.split(r"(?=@\w+\s*\{)", text)
    for raw in raw_entries:
        raw = raw.strip()
        if not raw or raw.startswith("@string") or raw.startswith("@String"):
            continue
        entry = {"_source": filepath.stem, "_raw_type": ""}

        # Entry type
        m = re.match(r"@(\w+)\s*\{", raw, re.IGNORECASE)
        if m:
            entry["_raw_type"] = m.group(1).lower()

        # Fields
        for field in ["title", "abstract", "year", "doi", "author",
                      "booktitle", "journal", "keywords"]:
            pattern = rf"(?i)\b{field}\s*=\s*[{{\"](.*?)[}}\"](?:\s*,|\s*\}})"
            fm = re.search(pattern, raw, re.DOTALL)
            if fm:
                entry[field] = re.sub(r"\s+", " ", fm.group(1).strip())
            else:
                # Try multi-line braces
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


def screen(entry: dict) -> tuple[str, str]:
    title = entry.get("title", "")
    abstract = entry.get("abstract", "")
    combined = (title + " " + abstract).lower()
    year_str = entry.get("year", "")
    entry_type = entry.get("_raw_type", "")

    # EC4 — no abstract
    if not abstract.strip():
        return "EXCLUDE", "EC4 – no abstract available"

    # EC4 — non-paper type
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
        pass  # unknown year, don't exclude on this alone

    # EC2 — web platform with no built environment
    web_hits = hits(combined, WEB_PLATFORM)
    built_hits = hits(combined, BUILT_ENV)
    if web_hits and not built_hits:
        return "EXCLUDE", f"EC2 – web/social platform context ({', '.join(web_hits[:2])})"

    # EC1 — environment-only (no human dimension signals)
    env_hits = hits(combined, ENV_ONLY)
    human_hits = hits(combined, HUMAN_DIMENSION)
    if env_hits and not human_hits:
        return "EXCLUDE", f"EC1 – environment-only modeling ({', '.join(env_hits[:2])})"

    # IC3 — relational or generative AI method
    gen_hits = hits(combined, GENERATIVE_AI)
    rel_hits = hits(combined, RELATIONAL_AI)
    has_method = bool(gen_hits or rel_hits)

    # IC4 — human dimension
    has_human = bool(human_hits)

    # IC5 — built environment
    has_context = bool(built_hits)

    if has_method and has_human and has_context:
        method_used = (gen_hits[:1] or []) + (rel_hits[:1] or [])
        return "INCLUDE", f"IC3({', '.join(method_used[:2])}) + IC4({human_hits[0]}) + IC5({built_hits[0]})"

    # Partial matches → UNCERTAIN with reason
    missing = []
    if not has_method:
        missing.append("no relational/generative AI method detected")
    if not has_human:
        missing.append("no psychological/interactional dimension detected")
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
