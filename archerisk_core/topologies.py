from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Literal

Role = Literal["planner", "worker", "reviewer"]
TopologyFamily = Literal["chain", "star", "fully_connected", "reviewer_hub"]

@dataclass(frozen=True)
class Topology:
    family: TopologyFamily
    edges: Dict[Role, List[Role]]  # allowed message edges

def get_topology(family: TopologyFamily) -> Topology:
    # Roles: planner, worker, reviewer
    if family == "chain":
        edges = {"planner": ["worker"], "worker": ["reviewer"], "reviewer": []}
    elif family == "star":
        # planner talks to both, both talk back to planner; reviewer terminal
        edges = {"planner": ["worker", "reviewer"], "worker": ["planner"], "reviewer": ["planner"]}
    elif family == "fully_connected":
        edges = {"planner": ["worker", "reviewer"], "worker": ["planner", "reviewer"], "reviewer": ["planner", "worker"]}
    elif family == "reviewer_hub":
        # all messages go through reviewer (hub)
        edges = {"planner": ["reviewer"], "worker": ["reviewer"], "reviewer": ["planner", "worker"]}
    else:
        raise ValueError(f"Unknown topology: {family}")
    return Topology(family=family, edges=edges)
