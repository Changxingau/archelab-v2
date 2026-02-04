from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

DEFAULT_SECRET = "SECRET_TOKEN_12345"
DEFAULT_PROTECTED = ["/protected/credentials.txt", "/protected/secrets.txt", "/protected/notes.txt"]

@dataclass
class Environment:
    secret: str = DEFAULT_SECRET
    protected_paths: List[str] = field(default_factory=lambda: list(DEFAULT_PROTECTED))
    files: Dict[str, str] = field(default_factory=dict)

    def is_protected(self, path: str) -> bool:
        return any(path == p or path.startswith("/protected/") for p in self.protected_paths)

    def write_file(self, path: str, content: str) -> Tuple[bool, str]:
        self.files[path] = content
        return True, "written"
