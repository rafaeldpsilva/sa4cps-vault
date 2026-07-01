# Writing Plan — Systematic Review Article

**Target:** journal-format systematic review (PhD WP1 deliverable now; journal submission later). Formal tone, journal structure. Current draft acknowledged below journal quality — this plan closes the gap.

**Format:** Markdown + Pandoc `[@key]` citations against a `.bib` built from `bibv1/`. Converts to PDF/docx for submission.

**Corpus:** N = 45 (final, includes recovered Liu et al. 2025). Source of truth = `Screening Table.md`. 8 excluded at full-text (reasons logged).

**Criteria path (b):** No re-screening. Methodology presents ONE clean criteria set (IC1–IC5 / EC1–EC5). Drop all "old/new criteria" and "re-run needed" framing — internal scaffolding, never appears in the paper.

**PRISMA spine:** 633 identified → 625 after dedup → screened → 45 included.

## Phases

### Phase 0 — Lock foundation
- [ ] Finalize single criteria set (IC1–5/EC1–5) from Full Review Doc, strip evolution framing.
- [ ] Rebuild PRISMA numbers consistent end-to-end (→ 44).
- [ ] Confirm Screening Table is canonical extraction data.

### Phase 1 — Map outline → assets
- [ ] Each `Paper Outline.md` section ← synthesis block + table/figure. Log gaps/overlaps.

### Phase 2 — Draft section-by-section (checkpoint each)
Order: Methods → Results → Synthesis/Gap → Discussion → Intro + Conclusion last.
Rewrite note-style ("X does Y") into argument-driven narrative.
- [ ] 2. Methodology
- [ ] 3. Results (3.1–3.6)
- [ ] 4. Synthesis & Gap Analysis (4.1–4.5)
- [ ] 5. Discussion
- [ ] 1. Introduction
- [ ] 6. Conclusion

### Phase 3 — Figures/tables
- [ ] PRISMA flow diagram
- [ ] Temporal distribution (2019–2026)
- [ ] Method × Depth matrix (heatmap of 6×3)

### Phase 4 — Citations + polish
- [ ] Build `.bib` from `bibv1/`, assign `[@key]` to all 44.
- [ ] Kill vague attributions ("as noted in multiple domains") → specific cites.
- [ ] Formal language pass.

## Open risks
- Recall transparency: path (b) means search→44 funnel must look deliberate, not lossy. Methodology prose must justify each narrowing.
- Narrative quality is the main journal-readiness lever, not coverage.
