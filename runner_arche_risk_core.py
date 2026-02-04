#!/usr/bin/env python3
"""One-command runner for ArcheRisk-Core (Baseline-3).

This script is designed to be **100% no-hand-edit**:
- Generates dataset (default: 2000 episodes)
- Runs simulation -> per-episode EpisodeResult JSONL (paper-aligned schema)
- Aggregates (Wilson 95% CI) + exports LaTeX tables
- Plots LNCS-ready figures
- Optionally compiles LNCS paper (if pdflatex is available)

EpisodeResult fields are **strictly aligned** with paper definitions in `paper_lncs/main.tex`.
"""

from __future__ import annotations
import argparse
import os
import shutil
import subprocess
from pathlib import Path

from archerisk_core.dataset_generate import generate as gen_dataset
from archerisk_core.utils import write_jsonl
from archerisk_core.episode_schema import Episode
from archerisk_core.runner import simulate_episode
from archerisk_core.aggregate import main as aggregate_main
from archerisk_core.plotting import main as plotting_main

def _cmd_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def _compile_paper(paper_dir: Path) -> None:
    if not _cmd_exists("pdflatex"):
        print("[WARN] pdflatex not found; skip compilation.")
        return
    # LNCS build sequence
    cwd = os.getcwd()
    os.chdir(paper_dir)
    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], check=False)
        if _cmd_exists("bibtex"):
            subprocess.run(["bibtex", "main"], check=False)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], check=False)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], check=False)
    finally:
        os.chdir(cwd)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target_n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=7)

    ap.add_argument("--data_out", default="data/arche_risk_core_v3.jsonl")
    ap.add_argument("--results_out", default="runs/results.jsonl")
    ap.add_argument("--trace_dir", default="runs/traces")
    ap.add_argument("--summary_out", default="runs/summary.json")

    ap.add_argument("--latex_dir", default="paper_lncs/tables")
    ap.add_argument("--fig_dir", default="paper_lncs/figures")

    ap.add_argument("--compile_paper", action="store_true")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent

    data_out = repo / args.data_out
    results_out = repo / args.results_out
    trace_dir = repo / args.trace_dir
    summary_out = repo / args.summary_out
    latex_dir = repo / args.latex_dir
    fig_dir = repo / args.fig_dir

    data_out.parent.mkdir(parents=True, exist_ok=True)
    results_out.parent.mkdir(parents=True, exist_ok=True)
    trace_dir.mkdir(parents=True, exist_ok=True)

    # 1) dataset
    eps = gen_dataset(target_n=args.target_n, seed=args.seed)
    write_jsonl(str(data_out), [e.__dict__ for e in eps])
    print(f"[OK] dataset: {len(eps)} episodes -> {data_out}")

    # 2) run
    results = []
    for r in eps:
        ep = Episode(**r.__dict__)
        res = simulate_episode(ep, str(trace_dir))
        results.append(res.to_dict())
    write_jsonl(str(results_out), results)
    print(f"[OK] results: {len(results)} EpisodeResult rows -> {results_out}")

    # 3) aggregate (reuse module CLI)
    import sys
    sys.argv = ["arche-risk-aggregate", "--in", str(results_out), "--out", str(summary_out), "--latex_dir", str(latex_dir)]
    aggregate_main()

    # 4) plot (reuse module CLI)
    sys.argv = ["arche-risk-plot", "--summary", str(summary_out), "--out", str(fig_dir)]
    plotting_main()

    # 5) paper compile
    if args.compile_paper:
        _compile_paper(repo / "paper_lncs")

    print("[DONE]")

if __name__ == "__main__":
    main()
