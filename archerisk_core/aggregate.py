from __future__ import annotations
import argparse
import json
import os
from collections import defaultdict
from typing import Dict, Any, List, Tuple

from .utils import read_jsonl
from .metrics import summarize_group

def _key(r: Dict[str, Any], fields: Tuple[str, ...]) -> Tuple[Any, ...]:
    return tuple(r[f] for f in fields)

def _group(rows: List[Dict[str, Any]], fields: Tuple[str, ...]) -> Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
    g: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        g[_key(r, fields)].append(r)
    return g

def _latex_rate(rt: Dict[str, Any]) -> str:
    return f"{rt['p']:.2f} [{rt['lo']:.2f}, {rt['hi']:.2f}]"

def export_latex_tables(summary: Dict[str, Any], latex_dir: str) -> None:
    os.makedirs(latex_dir, exist_ok=True)

    tableA = summary["tables"]["defended_by_archetype_baseline"]
    baselines = ["B1", "B2", "B3"]
    archetypes = ["MANIPULATOR", "COVERT_ACTOR", "DECEIVER", "INFILTRATOR_ESCALATOR", "MIXED"]

    lines = []
    lines.append("\\begin{tabular}{lccc}")
    lines.append("\\toprule")
    lines.append("Archetype & B1 (ASR) & B2 (ASR) & B3 (ASR) \\")
    lines.append("\\midrule")
    for a in archetypes:
        row = [a.replace("_", "\\_")]
        for b in baselines:
            rt = tableA[a][b]["ASR"]
            row.append(_latex_rate(rt))
        lines.append(" & ".join(row) + " \\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    with open(os.path.join(latex_dir, "tab_asr_defended.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    tableB = summary["tables"]["defended_uwr_by_topology_baseline"]
    topo = ["chain", "star", "fully_connected", "reviewer_hub"]

    lines = []
    lines.append("\\begin{tabular}{lccc}")
    lines.append("\\toprule")
    lines.append("Topology & B1 (UWR) & B2 (UWR) & B3 (UWR) \\")
    lines.append("\\midrule")
    for t in topo:
        row = [t.replace("_", "\\_")]
        for b in baselines:
            rt = tableB[t][b]["UWR"]
            row.append(_latex_rate(rt))
        lines.append(" & ".join(row) + " \\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    with open(os.path.join(latex_dir, "tab_uwr_topology.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Input EpisodeResult JSONL")
    ap.add_argument("--out", required=True, help="Output summary JSON")
    ap.add_argument("--latex_dir", default="paper_lncs/tables", help="Output LaTeX tables dir")
    args = ap.parse_args()

    rows = read_jsonl(args.inp)

    fields = ("defense_baseline", "topology_mode", "topology_family", "task_family", "attack_archetype")
    groups = _group(rows, fields)

    grouped_metrics: Dict[str, Any] = {}
    for k, rs in groups.items():
        gm = summarize_group(rs)
        grouped_metrics[str(k)] = {m: gm[m].__dict__ for m in gm}

    defended = [r for r in rows if r["topology_mode"] == "DEFENDED"]

    archetypes = ["MANIPULATOR", "COVERT_ACTOR", "DECEIVER", "INFILTRATOR_ESCALATOR", "MIXED"]
    baselines = ["B1", "B2", "B3"]
    tableA: Dict[str, Any] = {a: {} for a in archetypes}
    for a in archetypes:
        for b in baselines:
            rs = [r for r in defended if r["attack_archetype"] == a and r["defense_baseline"] == b]
            gm = summarize_group(rs)
            tableA[a][b] = {m: gm[m].__dict__ for m in gm}

    topo = ["chain", "star", "fully_connected", "reviewer_hub"]
    tableB: Dict[str, Any] = {t: {} for t in topo}
    for t in topo:
        for b in baselines:
            rs = [r for r in defended if r["topology_family"] == t and r["defense_baseline"] == b]
            gm = summarize_group(rs)
            tableB[t][b] = {m: gm[m].__dict__ for m in gm}

    summary = {
        "n_total": len(rows),
        "n_defended": len(defended),
        "grouped_metrics": grouped_metrics,
        "tables": {
            "defended_by_archetype_baseline": tableA,
            "defended_uwr_by_topology_baseline": tableB,
        }
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    export_latex_tables(summary, args.latex_dir)

    print(f"[OK] wrote summary to {args.out}")
    print(f"[OK] wrote LaTeX tables to {args.latex_dir}")

if __name__ == "__main__":
    main()
