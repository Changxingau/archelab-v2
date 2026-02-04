from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class Trace:
    episode_id: str
    meta: Dict[str, Any] = field(default_factory=dict)
    messages: List[Dict[str, Any]] = field(default_factory=list)
    tool_events: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)

    def set_meta(self, **kwargs: Any) -> None:
        self.meta.update(kwargs)

    def log_msg(self, role: str, sender: str, content: str, turn: int) -> None:
        self.messages.append({
            "ts": time.time(),
            "turn": turn,
            "role": role,
            "sender": sender,
            "content": content,
        })

    def log_tool(self, role: str, action: str, **payload: Any) -> None:
        e = {"ts": time.time(), "role": role, "action": action}
        e.update(payload)
        self.tool_events.append(e)

    def log_decision(self, role: str, decision: str, **payload: Any) -> None:
        e = {"ts": time.time(), "role": role, "decision": decision}
        e.update(payload)
        self.decisions.append(e)

    def to_json(self) -> Dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "meta": self.meta,
            "messages": self.messages,
            "tool_events": self.tool_events,
            "decisions": self.decisions,
        }

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, ensure_ascii=False, indent=2)
