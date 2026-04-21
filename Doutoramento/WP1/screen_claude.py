"""
Systematic review screener — Claude reasoning pass (v2).
Reads screening_results.csv (rule-based output) and re-screens every paper
using Claude to apply the revised IC/EC criteria with abstract-level reasoning.

Revised criteria applied:
  IC3 — any AI method produces a learned occupant representation
  IC4 — models occupant preference, behavioral pattern, latent intent,
         or collective/group dynamics beyond physical setpoints
  IC5 — work is situated in a built environment
  EC1 — environment-only (no occupant preference/intent layer)
  EC2 — web-platform profiling, no built-environment application
  EC3 — no learned occupant representation (pure rule-based/threshold)
  EC4 — non-full paper / no abstract
  EC5 — published before 2019

Output: screening_claude.csv
  Columns: id, source, year, title, decision, reason, method_type, doi

method_type records which AI category was detected (relational / generative /
general-ml / none) for use in the synthesis — it is NOT used as a gate.
"""

import csv
import json
import re
import time
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
BIB_DIR    = Path(__file__).parent / "review-bib"
INPUT_CSV  = Path(__file__).parent / "screening_results.csv"
OUTPUT_CSV = Path(__file__).parent / "screening_claude.csv"
DELAY_SEC  = 0.3   # polite delay between calls

SYSTEM_PROMPT = """You are a systematic review screener for a PhD literature review.
You will receive a paper's title and abstract and apply the inclusion/exclusion
criteria below. Respond ONLY with a valid JSON object — no markdown fences,
no prose before or after.

=== REVIEW SCOPE ===
This review maps AI methods applied to dynamically model, evolve, and reason
over occupant preferences and latent intent — at individual and collective
levels — within intelligent built environments. The analytical focus is on
identifying which methods exist and where relational/generative AI is underexplored.

=== INCLUSION CRITERIA (all must be met) ===
IC1: Peer-reviewed journal article or full conference paper.
IC2: Written in English.
IC3: Applies at least one AI method (ML, deep learning, RL, knowledge graph,
     GNN, ontology, LLM, Bayesian model, etc.) that produces a learned
     occupant-level representation — not solely a physical environment model.
IC4: Models or infers at least one dimension of occupant preference, behavioral
     pattern, contextual need, or latent intent beyond physical setpoints.
     This includes: comfort preferences, interaction preferences, temporal
     behavioral patterns, intent signals, personality traits, interaction styles,
     user expectations, group/collective preferences, or preference evolution.
IC5: Work is situated in a built environment: smart building, smart home,
     intelligent office, smart community, hospital, museum, or any other
     instrumented physical space regularly inhabited by humans.
     NOT: web platforms, social media, e-commerce, wireless networks, metaverse.

=== EXCLUSION CRITERIA (any one is sufficient to reject) ===
EC1: Focuses exclusively on physical/environmental modeling (occupancy sensing,
     thermal comfort, energy, HVAC) with no occupant preference or intent layer.
EC2: User profiling for web-platform purposes (social media, e-commerce, news/
     movie recommendation, ad targeting, sentiment analysis) with no built-
     environment application.
EC3: Pure rule-based or sensor-threshold system — no learned occupant model,
     profile, or preference representation produced.
EC4: Workshop summary, keynote abstract, editorial, book chapter, or paper
     with no retrievable abstract.
EC5: Published before 2019.

=== METHOD TYPE (record for synthesis — NOT a gate) ===
After deciding, also classify the primary AI method type detected:
- "relational"  — knowledge graph, GNN, ontology, semantic model
- "generative"  — LLM, foundation model, generative architecture, NLP
- "general-ml"  — other ML/DL (deep learning, RL, Bayesian, federated, etc.)
- "none"        — no AI method found
- "mixed"       — more than one category present

=== OUTPUT FORMAT (strict JSON, no markdown) ===
{
  "decision": "INCLUDE" | "EXCLUDE" | "UNCERTAIN",
  "reason": "<concise explanation referencing IC/EC codes; for UNCERTAIN list which ICs are missing, unclear, or borderline>",
  "method_type": "relational" | "generative" | "general-ml" | "mixed" | "none"
}

Decision rules:
- INCLUDE: all of IC3, IC4, IC5 met AND no EC triggered
- EXCLUDE: any EC clearly triggered from the abstract
- UNCERTAIN: cannot determine from abstract alone (e.g., IC5 is borderline,
  IC4 is ambiguous, or a key piece of information is missing from the abstract)
"""

# ---------------------------------------------------------------------------
# BibTeX parser (same as screen.py)
# ---------------------------------------------------------------------------

def parse_bib(filepath: Path) -> dict[str, dict]:
    """Return dict keyed by cleaned title → entry dict."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    entries = {}
    for raw in re.split(r"(?=@\w+\s*\{)", text):
        raw = raw.strip()
        if not raw or raw.startswith("@string") or raw.startswith("@String"):
            continue
        entry: dict = {}
        for field in ["title", "abstract", "year", "doi"]:
            pattern = rf"(?i)\b{field}\s*=\s*[{{\"](.*?)[}}\"](?:\s*,|\s*\}})"
            fm = re.search(pattern, raw, re.DOTALL)
            if fm:
                entry[field] = re.sub(r"\s+", " ", fm.group(1).strip())
            else:
                pattern2 = rf"(?i)\b{field}\s*=\s*\{{(.*?)\}}(?:\s*,|\s*\}})"
                fm2 = re.search(pattern2, raw, re.DOTALL)
                entry[field] = re.sub(r"\s+", " ", fm2.group(1).strip()) if fm2 else ""
        key = re.sub(r"[^a-z0-9]", "", entry.get("title", "").lower())
        if key:
            entries[key] = entry
    return entries


def build_abstract_index() -> dict[str, str]:
    """Build title-key → abstract mapping from all bib files."""
    index: dict[str, str] = {}
    for bib_file in sorted(BIB_DIR.glob("*.bib")):
        for key, entry in parse_bib(bib_file).items():
            if key not in index and entry.get("abstract"):
                index[key] = entry["abstract"]
    return index


# ---------------------------------------------------------------------------
# Claude call
# ---------------------------------------------------------------------------

client = anthropic.Anthropic()


def screen_with_claude(title: str, abstract: str) -> dict:
    user_msg = f"TITLE: {title}\n\nABSTRACT: {abstract or '(no abstract provided)'}"
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        raw = response.content[0].text.strip()
        # Strip markdown fences if model wraps anyway
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {
            "decision": "UNCERTAIN",
            "reason": f"parse error: {e} — raw: {raw[:120]}",
            "method_type": "none",
        }
    except Exception as e:
        return {
            "decision": "UNCERTAIN",
            "reason": f"API error: {e}",
            "method_type": "none",
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Building abstract index from bib files...")
    abstract_index = build_abstract_index()
    print(f"  {len(abstract_index)} abstracts indexed")

    # Read rule-based results as the paper list (titles + metadata)
    with open(INPUT_CSV, encoding="utf-8") as f:
        papers = list(csv.DictReader(f))
    print(f"  {len(papers)} papers to screen\n")

    # Resume support: skip already processed rows
    done_ids: set[str] = set()
    existing_rows: list[dict] = []
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done_ids.add(row["id"])
                existing_rows.append(row)
        print(f"  Resuming — {len(done_ids)} already done\n")

    fieldnames = ["id", "source", "year", "title", "decision", "reason", "method_type", "doi"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)

        counts = {"INCLUDE": 0, "EXCLUDE": 0, "UNCERTAIN": 0}
        for row in existing_rows:
            counts[row["decision"]] = counts.get(row["decision"], 0) + 1

        todo = [p for p in papers if p["id"] not in done_ids]
        for i, paper in enumerate(todo, 1):
            title = paper["title"]
            title_key = re.sub(r"[^a-z0-9]", "", title.lower())
            abstract = abstract_index.get(title_key, "")

            result = screen_with_claude(title, abstract)
            decision    = result.get("decision", "UNCERTAIN")
            reason      = result.get("reason", "")
            method_type = result.get("method_type", "none")

            counts[decision] = counts.get(decision, 0) + 1
            out_row = {
                "id":          paper["id"],
                "source":      paper["source"],
                "year":        paper["year"],
                "title":       title,
                "decision":    decision,
                "reason":      reason,
                "method_type": method_type,
                "doi":         paper["doi"],
            }
            writer.writerow(out_row)
            f.flush()

            pct = i / len(todo) * 100
            print(f"  [{i:4d}/{len(todo)}  {pct:5.1f}%]  {decision:<9}  {title[:70]}")
            time.sleep(DELAY_SEC)

    print(f"\nDone. Results written to {OUTPUT_CSV}")
    print(f"  INCLUDE:   {counts.get('INCLUDE', 0)}")
    print(f"  UNCERTAIN: {counts.get('UNCERTAIN', 0)}")
    print(f"  EXCLUDE:   {counts.get('EXCLUDE', 0)}")


if __name__ == "__main__":
    main()
