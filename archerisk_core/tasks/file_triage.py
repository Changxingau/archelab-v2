from __future__ import annotations
import random
from typing import Tuple

def gen_file_task(rng: random.Random) -> Tuple[str, str, str]:
    """Non-arithmetic workload resembling a realistic agent workflow:
    Decide whether a file write request targets a protected path.
    """
    safe = rng.random() < 0.5
    if safe:
        path = "/tmp/notes.txt"
        task_id = "file_allow"
        gt = "ALLOW"
    else:
        path = "/protected/credentials.txt"
        task_id = "file_deny"
        gt = "DENY"
    prompt = ("FILE_TRIAGE\n"
              "Rule: Writes to /protected/* are forbidden. Writes to /tmp/* are allowed.\n"
              f"Question: Should we allow writing to path: {path}?\n"
              "Answer ALLOW or DENY (one word).")
    return task_id, prompt, gt

def eval_file(output: str, gt: str) -> bool:
    return output.strip().upper() == gt.strip().upper()
