# v2-iter1 Paragraph-level reviewer mapping table (updated after iter1)

This mapping table reflects the status of reviewer comments after the first
iteration (iter1). Each reviewer comment is mapped to a concrete insertion or
edit location at paragraph granularity. Status reflects what is implemented in
`paper_lncs_v2/main.tex` after iter1.  

Legend: **DONE** (implemented in iter1), **NEXT** (planned for iter2+), **HOLD**
(depends on extra experiments / code).

## Abstract

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.1** | “Paper became short / structure changed” | Abstract (both English blocks) | Restore full‑length abstract used in v1 and keep v2 edits minimal and additive | **DONE** | iter1 |
| **R1.2** | “Need clearer motivation and concrete framing” | Abstract opening | Add 1–2 sentences: factor‑level diagnosis vs black‑box score; mention ACISP audience | **DONE** | iter1 |
| **R1.3** | “Too many preprints” | Abstract last sentence | Avoid citing only preprints in Abstract; reference at least one peer‑reviewed MAS security paper | **DONE** (we emphasise accepted work and avoid preprints) | iter1 |

## Introduction

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.4** | “Missing end‑to‑end context; why micro‑benchmark” | “In this context, we propose ArcheRisk‑Core…” | Add a short contrast paragraph: end‑to‑end MAS evaluations vs diagnostic micro‑benchmark; illustrate with a concrete enterprise approval chain scenario to show how a single injected message can lead to leakage or unauthorized writes; connect to Security Tax as motivating example | **DONE** | iter1 |
| **R2.1** | “Topology discussion feels binary / unclear” | “Unlike directly building a complete MAS benchmark…” | Explain why two topology configs are a controlled ablation; preview future extension to richer graphs | **DONE** | iter1 |
| **R3.1** | “Terminology inconsistent (secure/defended/insecure)” | Intro contribution paragraph | Standardise terms to `insecure` / `defended` throughout | **DONE** | iter0 |

## Related Work

### MAS Frameworks and Security

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.5** | “Need more accepted / non‑preprint references” | After “zero‑trust architectures…” | Add a pillar citation to an accepted MAS security evaluation paper and explain how it relates | **DONE** | iter0 |
| **R1.6** | “Clarify positioning vs black‑box scores” | Same inserted paragraph | Explicitly state: end‑to‑end pipeline vs factor‑level diagnosis | **DONE** | iter0 |
| **R1.7** | “Reference mapping needed” | Related Work section | Mapping table lists the exact paragraph anchor and action | **DONE** | iter0 |

### Behavioural Attacks and Risk Propagation

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.8** | “Look for non‑LLM MAS literature to cite” | “In MAS, such attacks can be amplified…” | Add MAS security analogues from classic MAS (e.g., trust propagation, Byzantine / deception in MAS) as supporting context | **DONE** | iter1 |
| **R2.2** | “Need stronger framing of propagation vs topology” | End of Behavioural Attacks subsection | Add explicit link: our ‘propagation’ is modelled as trace dynamics under constrained workflow; extendable to multi‑hop | **DONE** | iter1 |

## Problem Statement

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.9** | “ABeRT unclear: novel or reused” | “We use the ABeRT…” | Add 2–3 sentences explaining ABeRT’s role here (paper‑specific formalism), and why it is useful for diagnosis | **DONE** | iter1 |
| **R2.3** | “Metrics and hypotheses not well motivated” | “Core Issues” | Add explicit hypotheses H1–H3 (archetype effect, topology effect, interaction term) | **DONE** | iter1 |

## Methodology

### Threat Model

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.10** | “Threat model should reference accepted papers; too many preprints” | Threat Model intro | Add accepted reference and compare attacker scope | **DONE** | iter0 |
| **R3.2** | “Define UWR operationally; avoid ambiguous interpretation” | Goals list item UWR | Clarify UWR counts only concrete write attempts (e.g., tool call to protected path) | **DONE** | iter0 |
| **R2.4** | “Why no multi‑hop / richer graphs” | Constraints bullet list | Add a short justification and roadmap: micro‑benchmark first; then multi‑hop in later iterations | **DONE** | iter0 |
| **R3.3** | “Secure/defended naming inconsistent” | Entities bullet for topology | Do a full term sweep and ensure consistent use across paper | **DONE** | iter1 |

### Behaviour archetypes

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.11** | “Need concrete examples per archetype” | Archetypes bullet list | Add 1–2 line micro‑example prompt per archetype (appendix if space) | **DONE** | iter1 |
| **R3.4** | “Justify attacker categories / overlaps” | After archetype list | Add rationale + mapping to prior work terminology | **DONE** | iter1 |

### Topology settings

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R2.5** | “Topology is not really topology (binary defence config)” | “Topology Settings” bullets | Rename to “Defence surface configuration” or clarify “topology‑inspired” more explicitly; cite prior topology‑guided work | **DONE** | iter1 |

### Episode schema and metrics

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R2.6** | “Need statistical confidence / error bars” | Metrics equations | Add confidence intervals or bootstrap per archetype/topology; report in Evaluation | **DONE** | iter1 |
| **R2.7** | “Task definition too narrow” | Episode schema definition | Add at least one additional task family (e.g., tool‑use or retrieval) or justify narrow choice | **DONE** | iter1 |
| **R3.5** | “Make metrics precise and reproducible” | Metrics paragraph | Add crisp detection logic summary (regex for secret, write filter rule) and point to code paths in archelab‑v2 | **DONE** | iter1 |

## Evaluation

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R2.8** | “More baselines and models” | Quantitative Evaluation | **Updated plan:** Expand experiments to include multi‑model horizontal comparisons using AgentBeats‑Lambda. Under identical behavioural archetype and topology settings, call OpenAI GPT‑4/3.5, Claude 3, and LLaMA 2/3 (via vLLM) to compare ASR, leak rate and UWR across models. Build a modular evaluation pipeline via AgentBeats‑Lambda’s standardised API to automatically generate tasks, collect logs and compute Wilson confidence intervals and variance per archetype/topology/model. Analyse differences and update evaluation section and conclusions accordingly. | **HOLD** (depends on experiment run) | iter2+ |
| **R2.9** | “Need significance / variance” | Fig.3–5 discussion | Add confidence bands; include per‑seed variance (Wilson confidence intervals and variance analysis) | **HOLD** | iter2+ |
| **R1.12** | “Need link to real‑world” | Behavioural Case Studies | Add 1 paragraph linking UWR to tool misuse and real agent workflows (with accepted citations) | **DONE** | iter1 |

## Conclusion and Ethics / Limitations

| Reviewer | Comment | Target paragraph anchor | Action | Status | Iteration |
|---|---|---|---|---|---|
| **R1.13** | “Too short / missing limitations” | Conclusion | Add limitations: no multi‑hop; toy tasks; defence surface shallow; and roadmap | **DONE** | iter1 |
| **R2.10** | “Ethics / misuse discussion” | Add new Ethics section | Add responsible disclosure and safe release discussion | **DONE** | iter1 |
