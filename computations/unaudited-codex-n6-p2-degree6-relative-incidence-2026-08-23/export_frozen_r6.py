#!/usr/bin/env python3
"""Replay the existing coefficient-aware degree-2..5 lift and freeze r6.

No new column choice is made here: this is the main loop of
coefficient_power2_filtration.py with the terminal Counter serialized so the
degree-six theorem-shape audit can be repeated without another long replay.
"""

from __future__ import annotations

import gzip
import pickle
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "computations"))

import coefficient_power2_filtration as F  # noqa: E402
import lift_power2_offdiag2 as L  # noqa: E402


OUT = Path(__file__).with_name("frozen_r6_p1009.pkl.gz")


def main() -> None:
    rhs2, rhs3, _, _ = L.diagonal_remainder()
    residuals = defaultdict(Counter)
    residuals[2] = F.normalize(rhs2)
    residuals[3] = F.normalize(rhs3)
    stage = []
    for degree in range(2, 6):
        residual = F.normalize(residuals.pop(degree, Counter()))
        if not residual:
            continue
        assigned = F.triangular_assignment(tuple(residual), degree)
        if assigned is None:
            raise RuntimeError(f"existing triangular assignment failed at {degree}")
        correction = F.solve_triangular(residual, assigned, degree)
        if correction is None:
            raise RuntimeError(f"existing triangular solve failed at {degree}")
        F.add_future(residuals, correction, degree, maximum_degree=6)
        stage.append((degree, len(residual), len(assigned), len(correction)))
        L.incident_leading_columns.cache_clear()
        L.leading_outputs.cache_clear()
        L.monomial_killed.cache_clear()
        L.monomial_column.cache_clear()
    r6 = F.normalize(residuals[6])
    payload = {
        "format": "n6-p2-coefficient-aware-r6-p1009-v1",
        "prime": F.PRIME,
        "stage": stage,
        "support": len(r6),
        "rows": tuple(sorted(r6.items())),
    }
    with gzip.open(OUT, "wb", compresslevel=6) as stream:
        pickle.dump(payload, stream, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"wrote {OUT} with {len(r6)} nonzero row orbits")


if __name__ == "__main__":
    main()
