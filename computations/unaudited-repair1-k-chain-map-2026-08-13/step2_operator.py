#!/usr/bin/env python3
"""STEP 2: rebuild the 8,580-column bounded operator; solve; export D2(u).

Writes operator_solution.json (metadata + coefficients) and
operator_d2_shadow.json (the grade-forgotten pair shadow of the solution).
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
import json
import pickle
import time

import common as C

t0 = time.time()
m = C.modules()
cols, shifts = C.build_operator_columns(m)
print("build seconds", round(time.time() - t0, 1), flush=True)

aff, cm = m["aff"], m["commutator"]
target = {(2, pair): int(v) for pair, v in cm.expected_second_shadow().items()}

t1 = time.time()
solution, rank = aff.exact_row_solution(cols, target)
print("solve seconds", round(time.time() - t1, 1), flush=True)

recon = defaultdict(Q)
for idx, coeff in solution.items():
    for row, val in cols[idx][1].items():
        recon[row] += Q(coeff) * Q(val)
recon = {r: v for r, v in recon.items() if v}
src = {r: v for r, v in recon.items() if r[0] == 0}
d1 = {r: v for r, v in recon.items() if r[0] == 1}
d2 = {r: v for r, v in recon.items() if r[0] == 2}

report = {
    "columns": len(cols),
    "exact_row_rank": rank,
    "solution_terms": len(solution),
    "source_output_support": len(src),
    "d1_output_support": len(d1),
    "d2_output_support": len(d2),
    "d2_equals_expected_second_shadow": (
        {r: Q(v) for r, v in d2.items()} == {r: Q(v) for r, v in target.items()}),
    "distinct_source_rows_in_block": len({r for _m, c in cols for r in c
                                          if r[0] == 0}),
    "distinct_d1_rows_in_block": len({r for _m, c in cols for r in c
                                      if r[0] == 1}),
    "distinct_shadow_rows_in_block": len({r for _m, c in cols for r in c
                                          if r[0] == 2}),
    "source_incidences_over_solution_support": sum(
        1 for i in solution for r in cols[i][1] if r[0] == 0),
    "solution_denominators": sorted({v.denominator for v in solution.values()}),
}
print(json.dumps(report, indent=1, sort_keys=True))
json.dump(report, open("step2_operator.json", "w"), indent=1, sort_keys=True)

with open("operator_state.pkl", "wb") as fh:
    pickle.dump({
        "columns": cols,
        "shifts": shifts,
        "solution": {k: (v.numerator, v.denominator) for k, v in solution.items()},
        "d2": {repr(r): (v.numerator, v.denominator) for r, v in d2.items()},
    }, fh)
print("total seconds", round(time.time() - t0, 1))
