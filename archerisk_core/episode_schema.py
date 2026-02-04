from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, List, Dict, Any

TaskFamily = Literal["arithmetic_check", "policy_triage", "file_triage"]
TopologyFamily = Literal["chain", "star", "fully_connected", "reviewer_hub"]
DefenseBaseline = Literal["B1", "B2", "B3"]
TopologyMode = Literal["INSECURE", "DEFENDED"]
Archetype = Literal["MANIPULATOR", "COVERT_ACTOR", "DECEIVER", "INFILTRATOR_ESCALATOR", "MIXED"]

@dataclass(frozen=True)
class Episode:
    # Identification / reproducibility
    episode_id: str
    seed: int

    # Controlled factors
    task_family: TaskFamily
    task_id: str
    topology_family: TopologyFamily
    topology_mode: TopologyMode
    defense_baseline: DefenseBaseline
    attack_archetype: Archetype

    # Task + threat content
    prompt: str
    ground_truth: str
    secret: str
    protected_paths: List[str]
    attacker_injection: str

@dataclass(frozen=True)
class EpisodeResult:
    """
    EpisodeResult is the single source of truth for outputs and paper definitions.

    Fields (paper-aligned):
      - episode_id, seed
      - task_family, task_id
      - topology_family (explicit graph family) + topology_mode (INSECURE/DEFENDED)
      - defense_baseline (B1/B2/B3)
      - attack_archetype
      - task_success, attack_success, leak, unauthorized_write
      - trace_path (reproducibility; pointer to JSON trace)
    """
    episode_id: str
    seed: int

    task_family: str
    task_id: str

    topology_family: str
    topology_mode: str
    defense_baseline: str

    attack_archetype: str

    task_success: bool
    attack_success: bool
    leak: bool
    unauthorized_write: bool

    trace_path: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "seed": self.seed,
            "task_family": self.task_family,
            "task_id": self.task_id,
            "topology_family": self.topology_family,
            "topology_mode": self.topology_mode,
            "defense_baseline": self.defense_baseline,
            "attack_archetype": self.attack_archetype,
            "task_success": self.task_success,
            "attack_success": self.attack_success,
            "leak": self.leak,
            "unauthorized_write": self.unauthorized_write,
            "trace_path": self.trace_path,
        }
