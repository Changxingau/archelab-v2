# v2-iter0 Paragraph-level reviewer mapping table

This mapping table is organised by paper section order. Each reviewer comment is mapped to a concrete insertion or edit location at paragraph granularity. Status reflects what is already implemented in `paper_lncs_v2/main.tex` for v2-iter0.

Legend: DONE (implemented in v2-iter0), NEXT (planned for v2-iter1+), HOLD (depends on extra experiments / code).

## Abstract

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “Paper became short / structure changed” | Abstract (both English blocks) | Restore full-length abstract used in v1 and keep v2 edits minimal and additive | NEXT |
| R1 | “Need clearer motivation and concrete framing” | Abstract opening | Add 1–2 sentences: factor-level diagnosis vs black-box score; mention ACISP audience | NEXT |
| R1 | “Too many preprints” | Abstract last sentence | Avoid citing only preprints in Abstract; reference at least one peer-reviewed MAS security paper | NEXT |

## Introduction

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “Missing end-to-end context; why micro-benchmark” | “In this context, we propose ArcheRisk-Core…” | Add a short contrast paragraph: end-to-end MAS evaluations vs diagnostic micro-benchmark; connect to Security Tax as motivating example | NEXT |
| R2 | “Topology discussion feels binary / unclear” | “Unlike directly building a complete MAS benchmark…” | Explain why two topology configs are a controlled ablation; preview future extension to richer graphs | NEXT |
| R3 | “Terminology inconsistent (secure/defended etc.)” | Intro contribution paragraph | Standardise terms to `insecure` / `defended` throughout | DONE (partial: fixed in one key sentence; full sweep later) |

## Related Work

### MAS Frameworks and Security

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “Need more accepted / non-preprint references” | After “zero-trust architectures…” | Add a pillar citation to an accepted MAS security evaluation paper and explain how it relates | DONE (added `Multi-Agent Security Tax` \cite{Peigne2025SecurityTax}) |
| R1 | “Clarify positioning vs black-box scores” | Same inserted paragraph | Explicitly state: end-to-end pipeline vs factor-level diagnosis | DONE |
| R1 | “Reference mapping needed” | Related Work section | Mapping table lists the exact paragraph anchor and action | DONE |

### Behavioural Attacks and Risk Propagation

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “Look for non-LLM MAS literature to cite” | “In MAS, such attacks can be amplified…” | Add MAS security analogues from classic MAS (e.g., trust propagation, Byzantine / deception in MAS) as supporting context | NEXT |
| R2 | “Need stronger framing of propagation vs topology” | End of Behavioural Attacks subsection | Add explicit link: our ‘propagation’ is modelled as trace dynamics under constrained workflow; extendable to multi-hop | NEXT |

## Problem Statement

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “ABeRT unclear: novel or reused” | “We use the ABeRT…” | Add 2–3 sentences explaining ABeRT’s role here (paper-specific formalism), and why it is useful for diagnosis | NEXT |
| R2 | “Metrics and hypotheses not well motivated” | “Core Issues” | Add explicit hypotheses H1–H3 (archetype effect, topology effect, interaction term) | NEXT |

## Methodology

### Threat Model

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “Threat model should reference accepted papers; too many preprints” | Threat Model intro | Add accepted reference and compare attacker scope | DONE (added infectious-prompt comparison to \cite{Peigne2025SecurityTax}) |
| R3 | “Define UWR operationally; avoid ambiguous interpretation” | Goals list item UWR | Clarify UWR counts only concrete write attempts (e.g., tool call to protected path) | DONE |
| R2 | “Why no multi-hop / richer graphs” | Constraints bullet list | Add a short justification and roadmap: micro-benchmark first; then multi-hop in later iterations | DONE (inserted paragraph; also will add one sentence to constraints list later) |
| R3 | “Secure/defended naming inconsistent” | Entities bullet for topology | Do a full term sweep and ensure consistent use across paper | NEXT |

### Behaviour archetypes

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “Need concrete examples per archetype” | Archetypes bullet list | Add 1–2 line micro-example prompt per archetype (appendix if space) | NEXT |
| R3 | “Justify attacker categories / overlaps” | After archetype list | Add rationale + mapping to prior work terminology | NEXT |

### Topology settings

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R2 | “Topology is not really topology (binary defence config)” | “Topology Settings” bullets | Rename to “Defence surface configuration” or clarify “topology-inspired” more explicitly; cite prior topology-guided work | NEXT |

### Episode schema and metrics

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R2 | “Need statistical confidence / error bars” | Metrics equations | Add confidence intervals or bootstrap per archetype/topology; report in Evaluation | NEXT |
| R2 | “Task definition too narrow” | Episode schema definition | Add at least one additional task family (e.g., tool-use or retrieval) or justify narrow choice | NEXT |
| R3 | “Make metrics precise and reproducible” | Metrics paragraph | Add crisp detection logic summary (regex for secret, write filter rule) and point to code paths in archelab-v2 | NEXT |

## Evaluation

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R2 | “More baselines and models” | Quantitative Evaluation | Add multiple LLMs comparison (OpenAI vs local GPU endpoint) and show robustness of trends | HOLD (depends on experiment run) |
| R2 | “Need significance / variance” | Fig.3–5 discussion | Add confidence bands; include per-seed variance | HOLD |
| R1 | “Need link to real-world” | Behavioural Case Studies | Add 1 paragraph linking UWR to tool misuse and real agent workflows (with accepted citations) | NEXT |

## Conclusion and Ethics / Limitations

| Reviewer | Comment | Target paragraph anchor | Action | Status |
|---|---|---|---|---|
| R1 | “Too short / missing limitations” | Conclusion | Add limitations: no multi-hop; toy tasks; defence surface shallow; and roadmap | NEXT |
| R2 | “Ethics / misuse discussion” | Add new Ethics section | Add responsible disclosure and safe release discussion | NEXT |
