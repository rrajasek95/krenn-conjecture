#!/usr/bin/env python3
"""AUDIT A2 / claim A.5 (corrected form) -- EXACT decision, by SAT, of

    "is there a DIAGONAL template on K_8 of support <= 27 that
     (SC) serves every (vertex,colour) slot with a single-colour edge,
     (T4) has all three constant fibres nonempty, and
     (S)  has NO mixed singleton fibre?"

(SC) inside the diagonal regime: a block with palette of size >= 2 is diagonal
with two nonzero entries, so it has rank 2 and cannot be the a (x) e_r of the
forced incident-edge theorem; hence every (vertex,colour) slot needs an
incident edge with palette EXACTLY that colour.  This is also what W6's own
budget beta >= 3N - m + |H| gives here (|H| = m - beta, so beta >= 12), and
it is W5's diagonal corollary.

RESULT (recorded run, cadical195, 812.5 s, 51107 clauses): UNSAT.
Support <= 27 is encoded as the single clause "some edge is absent", so this
one call covers every support 12..27 at once.
"""
import json, time
import a2_diag_sat as D
from pysat.solvers import Solver

clauses, x, present, pool = D.build(0, exact_support=False, slotforce=True)
clauses = list(clauses) + [[-present[e] for e in range(len(D.EDGES))]]
t0 = time.time()
with Solver(name="cadical195", bootstrap_with=clauses) as s:
    sat = s.solve()
    took = time.time() - t0
    print("support<=27, slice-cover-admissible diagonal:",
          "SAT" if sat else "UNSAT", f"{took:.1f}s", len(clauses), "clauses")
    out = {"question": "zero-singleton diagonal template, support <= 27, "
                       "slice-cover admissible, constant fibres nonempty",
           "status": "SAT" if sat else "UNSAT", "seconds": round(took, 1),
           "clauses": len(clauses), "vars": pool.top}
    if sat:
        out["palettes"] = D.decode(s.get_model(), x, present)
    json.dump(out, open("results_diag_admissible.json", "w"), indent=1)
