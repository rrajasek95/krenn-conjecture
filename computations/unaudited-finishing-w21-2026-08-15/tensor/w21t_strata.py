#!/usr/bin/env python3
"""W21-M1-TENSOR -- the 2x2 rank strata, decided exactly in Singular.
UNAUDITED.  Exact over Q.

By Lemma 3 every solution of (T) with all six blocks nonzero is, after
GL_3^4, supported in a common 2x2 corner.  In the 2x2 world rank in {1,2},
and the rank-product inequalities |r12 r34 - r13 r24| <= 1 etc. leave only:
  B0  all six rank 1
  B1  exactly one rank 2
  B2  exactly two rank 2 (necessarily sharing a vertex)
  B3s three rank 2 forming a STAR
  B3t three rank 2 forming a TRIANGLE
  A   all six rank 2
(any complementary PAIR both of rank 2 forces all six to rank 2).
This module decides each stratum by saturation, with the ledger-13 guard,
and reports whether a site factors.  The feasible strata double as the
mandatory EXPLICIT-POINT CONTROLS for the infeasible verdicts.
"""
import json
import os
import subprocess
import sys
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w21t_sing as S                                           # noqa: E402
from w21t_class2 import VARS, NAMES, equations, ent             # noqa: E402

PAIRS = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


def det2(p):
    return "%s*%s - %s*%s" % (ent(p, 0, 0), ent(p, 1, 1),
                              ent(p, 0, 1), ent(p, 1, 0))


def entries(p):
    return [ent(p, i, j) for i in range(2) for j in range(2)]


def stratum_script(rank2):
    """rank2 = the set of pairs required to have rank 2; the rest rank 1
    and NONZERO."""
    rank1 = [p for p in PAIRS if p not in rank2]
    eqs = list(equations()) + [det2(p) for p in rank1]
    sat_nonzero = []
    for p in rank1:
        sat_nonzero.append("ideal(%s)" % ",".join(entries(p)))
    lines = ['LIB "primdec.lib";', 'LIB "elim.lib";',
             "ring Rng = 0,(%s),dp;" % ",".join(VARS),
             "ideal zzgI = %s;" % ",\n  ".join(eqs)]
    # saturate away the loci where a rank-1 block vanishes
    for k, s in enumerate(sat_nonzero):
        lines += ["list zzgL%d = sat(zzgI, %s);" % (k, s),
                  "ideal zzgI = zzgL%d[1];" % k]
    # saturate away the loci where a "rank 2" block is singular
    for k, p in enumerate(rank2):
        lines += ["list zzgM%d = sat(zzgI, ideal(%s));" % (k, det2(p)),
                  "ideal zzgI = zzgM%d[1];" % k]
    lines += ["ideal zzgG = std(zzgI);",
              'printf("DIM %s", dim(zzgG));',
              'printf("ISUNIT %s", size(zzgG) == 1 && '
              'leadmonom(zzgG[1]) == 1);',
              'printf("GENS %s", string(zzgG));',
              "quit;"]
    return "\n".join(lines) + "\n"


def main():
    res = {"_header": "UNAUDITED W21-M1-TENSOR 2x2 rank strata. Exact."}
    ok, _ = S.selftest()
    res["guard_selftest"] = ok
    print("guard self-test (4 planted traps): %s" % ok)
    strata = {
        "B0_all_rank1": [],
        "B1_one_rank2_(12)": [(1, 2)],
        "B2_two_rank2_(12)(13)": [(1, 2), (1, 3)],
        "B3star_(12)(13)(14)": [(1, 2), (1, 3), (1, 4)],
        "B3tri_(12)(13)(23)": [(1, 2), (1, 3), (2, 3)],
        "A_all_rank2": PAIRS,
    }
    for name, r2 in strata.items():
        sc = stratum_script(r2)
        open(os.path.join(HERE, "stratum_%s.sing" % name), "w").write(sc)
        try:
            out, errs = S.run(sc, set(VARS), timeout=900)
        except subprocess.TimeoutExpired:
            print("%-24s TIMEOUT" % name)
            res[name] = "timeout"
            continue
        dim = None
        unit = None
        for ln in out.splitlines():
            if ln.startswith("DIM "):
                dim = ln.split()[1]
            if ln.startswith("ISUNIT "):
                unit = ln.split()[1]
        verdict = ("EMPTY (unit ideal)" if dim == "-1"
                   else "NONEMPTY dim %s" % dim)
        print("%-24s %s   singular-errors=%s" % (name, verdict, errs[:2]))
        res[name] = dict(dim=dim, isunit=unit, errors=errs[:4],
                         verdict=verdict)
    json.dump(res, open(os.path.join(HERE, "results_strata.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
