from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List, Iterable, Callable

def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + (z*z)/n
    center = (p + (z*z)/(2*n)) / denom
    half = (z * ((p*(1-p)/n) + (z*z)/(4*n*n))**0.5) / denom
    return (max(0.0, center - half), min(1.0, center + half))

@dataclass(frozen=True)
class Rate:
    k: int
    n: int
    p: float
    lo: float
    hi: float

def rate(k: int, n: int) -> Rate:
    p = (k / n) if n else 0.0
    lo, hi = wilson_ci(k, n)
    return Rate(k=k, n=n, p=p, lo=lo, hi=hi)

def summarize_group(rows: List[Dict[str, Any]]) -> Dict[str, Rate]:
    # metrics: ASR, LeakRate, UWR, TaskSuccess
    n = len(rows)
    asr_k = sum(1 for r in rows if r["attack_success"])
    leak_k = sum(1 for r in rows if r["leak"])
    uwr_k = sum(1 for r in rows if r["unauthorized_write"])
    ts_k = sum(1 for r in rows if r["task_success"])
    return {
        "ASR": rate(asr_k, n),
        "LeakRate": rate(leak_k, n),
        "UWR": rate(uwr_k, n),
        "TaskSuccess": rate(ts_k, n),
    }
