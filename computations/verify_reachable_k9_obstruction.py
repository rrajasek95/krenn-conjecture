#!/usr/bin/env python3
"""Verify an obstruction in the structural support propagated after degree 5.

The degree-six support contains a cone row whose unique one-term 2+2+2
column has a degree-nine output with no incident leading column.  Therefore
the current coefficient-independent right inverse cannot be continued merely
by proving that all structurally reachable rows straighten to cones.  This is
not an obstruction to a coefficient-aware certificate: the relevant
coefficient could vanish or cancel.
"""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

import complete_power2_filtration as C
import lift_power2_offdiag2 as L


CONE_ROW = (
    (0, 0, 3, 30, 57, 72),
    (5491800, 3188673, 9566673),
)
CONE_COLUMN = (
    (0, 0, 1, 1, 2, 2),
    (6, 9, 9, 23, 41, 42),
    (3306744, 13122, 1595079),
)
BAD_ROW = (
    (0, 0, 3, 3, 11, 56, 58, 77, 87),
    (9566424, 3188646, 5314413),
)


def main():
    checkpoint = Path("/tmp/krenn_p2_filter_after5.pkl")
    with checkpoint.open("rb") as fh:
        supports = pickle.load(fh)["supports"]
    assert CONE_ROW in supports[6]
    assert L.monomial_killed(CONE_ROW)

    one_term = [
        col
        for col in L.incident_leading_columns(CONE_ROW)
        if len(set(L.leading_outputs(col))) == 1
    ]
    assert one_term == [CONE_COLUMN]
    assert L.monomial_column(CONE_ROW) == CONE_COLUMN

    outputs = C.full_outputs(CONE_COLUMN)
    assert sum(degree == 9 and row == BAD_ROW for degree, row in outputs) == 1
    assert not L.monomial_killed(BAD_ROW)
    assert not L.incident_leading_columns(BAD_ROW)
    print("verified structurally reachable degree-nine dead row")
    print(f"degree-six cone: {CONE_ROW}")
    print(f"unique one-term column: {CONE_COLUMN}")
    print(f"degree-nine dead row: {BAD_ROW}")


if __name__ == "__main__":
    main()
