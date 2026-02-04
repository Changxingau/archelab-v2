from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Tuple

DefenseBaseline = Literal["B1", "B2", "B3"]
TopologyMode = Literal["INSECURE", "DEFENDED"]

@dataclass(frozen=True)
class DefenseConfig:
    baseline: DefenseBaseline
    topology_mode: TopologyMode
    # message boundary markers
    boundary_prefix: str
    boundary_suffix: str
    # protections
    redact_secret: bool
    block_explicit_induction: bool
    strict_tool_guard: bool

def get_defense(baseline: DefenseBaseline, topology_mode: TopologyMode) -> DefenseConfig:
    # B1: no meaningful defenses; INSECURE only by default
    if baseline == "B1":
        return DefenseConfig(
            baseline="B1",
            topology_mode=topology_mode,
            boundary_prefix="",
            boundary_suffix="",
            redact_secret=False,
            block_explicit_induction=False,
            strict_tool_guard=False,
        )

    # B2: basic topology gating + injection sanitizer + tool guard
    if baseline == "B2":
        return DefenseConfig(
            baseline="B2",
            topology_mode=topology_mode,
            boundary_prefix="[BEGIN_UNTRUSTED]\n",
            boundary_suffix="\n[END_UNTRUSTED]",
            redact_secret=False,
            block_explicit_induction=True,
            strict_tool_guard=True,
        )

    # B3: Baseline-3: B2 + verified defense loop (redaction + stronger reviewer veto)
    return DefenseConfig(
        baseline="B3",
        topology_mode=topology_mode,
        boundary_prefix="[BEGIN_UNTRUSTED]\n",
            boundary_suffix="\n[END_UNTRUSTED]",
        redact_secret=True,
        block_explicit_induction=True,
        strict_tool_guard=True,
    )
