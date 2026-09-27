"""Pinned exact arithmetic reused from the preceding research package."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[2]
PREVIOUS = ROOT / 'computations/rate-design-frontier-2026-09-26'
spec = importlib.util.spec_from_file_location('utility_frontier', PREVIOUS / 'core.py')
core = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = core
spec.loader.exec_module(core)
C, ZERO, ONE = core.C, core.ZERO, core.ONE
require = core.require


def gram(rows):
    n = len(rows[0])
    out = [[ZERO]*n for _ in range(n)]
    for row in rows:
        active = [(i, x) for i, x in enumerate(row) if x]
        for i, x in active:
            for j, y in active:
                out[i][j] += core.conj(x)*y
    return out
