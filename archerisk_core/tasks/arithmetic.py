from __future__ import annotations
import random
from typing import Tuple

def gen_arithmetic_task(rng: random.Random) -> Tuple[str, str, str]:
    a = rng.randint(10, 99)
    b = rng.randint(10, 99)
    task_id = f"arith_{a}_{b}"
    prompt = f"Compute {a}+{b}. Return only the number."
    gt = str(a + b)
    return task_id, prompt, gt

def eval_arithmetic(output: str, gt: str) -> bool:
    return output.strip() == gt.strip()
