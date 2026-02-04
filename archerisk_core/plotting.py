from __future__ import annotations
import argparse
import json
import os
from typing import Dict, Any, List

import matplotlib.pyplot as plt

ARCHETYPES = ["MANIPULATOR", "COVERT_ACTOR", "DECEIVER", "INFILTRATOR_ESCALATOR", "MIXED"]
BASELINES = ["B1", "B2", "B3"]

def _extract(summary: Dict[str, Any], metric: str) -> List[List[float]]:
    table = summary["tables"]["defended_by_archetype_baseline"]
    vals: List[List[float]] = []
    for b in BASELINES:
        row = []
        for a in ARCHETYPES:
            row.append(table[a][b][metric]["p"])
        vals.append(row)
    return vals

def _plot_grouped(vals: List[List[float]], title: str, ylabel: str, out_pdf: str, out_png: str) -> None:
    import numpy as np
    x = np.arange(len(ARCHETYPES))
    width = 0.24
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    for i, b in enumerate(BASELINES):
        ax.bar(x + (i-1)*width, vals[i], width, label=b)
    ax.set_xticks(x)
    ax.set_xticklabels([a.replace("_", "\n") for a in ARCHETYPES], fontsize=8)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8, ncols=3, loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(out_pdf)
    fig.savefig(out_png, dpi=200)
    plt.close(fig)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True)
    ap.add_argument("--out", required=True, help="Output directory for figures")
    args = ap.parse_args()

    with open(args.summary, "r", encoding="utf-8") as f:
        summary = json.load(f)

    os.makedirs(args.out, exist_ok=True)

    asr_vals = _extract(summary, "ASR")
    leak_vals = _extract(summary, "LeakRate")
    uwr_vals = _extract(summary, "UWR")

    _plot_grouped(asr_vals, "Attack Success Rate by Behaviour Archetype (DEFENDED)", "ASR", 
                  os.path.join(args.out, "fig_attack_success_behavior_lncs.pdf"),
                  os.path.join(args.out, "fig_attack_success_behavior_lncs.png"))

    _plot_grouped(leak_vals, "Leak Rate by Behaviour Archetype (DEFENDED)", "Leak Rate", 
                  os.path.join(args.out, "fig_leak_behavior_lncs.pdf"),
                  os.path.join(args.out, "fig_leak_behavior_lncs.png"))

    _plot_grouped(uwr_vals, "Unauthorized Write Rate by Behaviour Archetype (DEFENDED)", "UWR", 
                  os.path.join(args.out, "fig_unauthorized_write_behavior_lncs.pdf"),
                  os.path.join(args.out, "fig_unauthorized_write_behavior_lncs.png"))

    print(f"[OK] wrote figures to {args.out}")

if __name__ == "__main__":
    main()
