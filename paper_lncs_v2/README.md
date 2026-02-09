# paper_lncs_v2 (v2-iter0)

This folder is intended to live alongside `paper_lncs_v1/` in the repo. v2-iter0 is an additive iteration that keeps the v1 structure, but thickens two areas:

1) Related Work: adds a pillar citation to `Multi-Agent Security Tax` and explicitly positions ArcheRisk-Core as factor-level diagnosis relative to end-to-end MAS security evaluations.

2) Threat Model: clarifies the single-injection attacker scope relative to infectious-prompt / multi-hop settings, and makes the UWR (unauthorised write) metric operational (tool-call based).

Practical note: v2 reuses v1 assets (figures and main bib) via relative paths. That keeps the diff small and avoids duplicating binaries.

## Files

- `main.tex`: v2-iter0 paper source (based on v1 main.tex with minimal edits).
- `acisp_references_v2_additions.bib`: new BibTeX entries used only by v2.
- `reviewer_mapping_v2_iter0.md`: paragraph-level mapping table for the full reviewer feedback set.

## Build

From repo root:

1. Ensure both `paper_lncs_v1/` and this `paper_lncs_v2/` folder exist.
2. Compile in `paper_lncs_v2/` as usual (LNCS pipeline). BibTeX should resolve:
   - `../paper_lncs_v1/acisp_references.bib`
   - `acisp_references_v2_additions.bib`

## What changed (v2-iter0)

- Added citation key: `Peigne2025SecurityTax`
- Inserted 1 paragraph in Related Work / MAS Frameworks and Security
- Inserted 1 paragraph in Threat Model (scope comparison)
- Clarified UWR definition in Threat Model goals
- Pointed all figures and bibliography to reuse v1 resources via `../paper_lncs_v1/`
