# ArcheRisk-Core Final Repo (Baseline-3 + Topology Families + A2A Adapter)

This repository is a **self-contained** release that:
- Generates a factorial-balanced episode dataset (~2000 episodes),
- Runs a minimal Planner–Worker–Reviewer MAS simulation under **4 topology families** and **3 defense baselines (B1–B3)**,
- Reports **ASR / Leak Rate / Unauthorized Write Rate** with **Wilson 95% CIs**,
- Produces LNCS-ready figures + LaTeX tables,
- Includes an **AgentBeats/A2A-compatible** harness (green judge + purple agent).

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .

# 1) Generate dataset
arche-risk-gen --out data/arche_risk_core_v3.jsonl --target_n 2000 --seed 7

# 2) Run benchmark (produces per-episode EpisodeResult)
arche-risk-run --data data/arche_risk_core_v3.jsonl --out runs/results.jsonl

# 3) Aggregate + export LaTeX tables
arche-risk-aggregate --in runs/results.jsonl --out runs/summary.json --latex_dir paper_lncs/tables

# 4) Plot LNCS figures
arche-risk-plot --summary runs/summary.json --out paper_lncs/figures

# 5) Compile paper (requires LNCS class/bst files)
cd paper_lncs
pdflatex main.tex
bibtex main || true
pdflatex main.tex
pdflatex main.tex
```

## Outputs

- `runs/results.jsonl`: per-episode EpisodeResult (schema matches paper)
- `runs/summary.json`: grouped rates + CIs
- `paper_lncs/figures/*.pdf`: figures used by the paper
- `paper_lncs/tables/*.tex`: tables used by the paper
- `paper_lncs/main.pdf`: compiled paper (if pdflatex available)

## Reviewer convergence highlights

- Gentle intro + concrete role examples.
- Unified terminology: **INSECURE** vs **DEFENDED**; baselines B1/B2/B3.
- Topology is **not binary**: 4 explicit communication graphs.
- Adds non-arithmetic task families (policy triage, file triage) in addition to arithmetic.
- Metrics include Wilson 95% confidence intervals.
- UWR is operationally defined under text-only attacker as **policy-flagged tool write attempts**.
