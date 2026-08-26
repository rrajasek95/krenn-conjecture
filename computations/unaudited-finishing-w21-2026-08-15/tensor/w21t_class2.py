#!/usr/bin/env python3
"""W21-M1-TENSOR -- the 2x2 classification (which, by Lemma 3, IS the full
classification of the identically-vanishing K_4 hafnian with all six blocks
nonzero).  UNAUDITED.  Exact over Q.

Variables (24):  p = M12, q = M13, r = M14, s = M23, t = M24, u = M34,
each a 2x2 matrix pij etc.  Equations (16):
  p[y1][y2] u[y3][y4] + q[y1][y3] t[y2][y4] + r[y1][y4] s[y2][y3] = 0.
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

NAMES = {(1, 2): "p", (1, 3): "q", (1, 4): "r",
         (2, 3): "s", (2, 4): "t", (3, 4): "u"}
VARS = [NAMES[k] + "%d%d" % (a + 1, b + 1)
        for k in [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        for a in range(2) for b in range(2)]


def ent(pair, i, j):
    return NAMES[pair] + "%d%d" % (i + 1, j + 1)


def equations():
    eqs = []
    for y in product(range(2), repeat=4):
        y1, y2, y3, y4 = y
        eqs.append("%s*%s + %s*%s + %s*%s"
                   % (ent((1, 2), y1, y2), ent((3, 4), y3, y4),
                      ent((1, 3), y1, y3), ent((2, 4), y2, y4),
                      ent((1, 4), y1, y4), ent((2, 3), y2, y3)))
    return eqs


def build(extra=(), do="minAssGTZ"):
    eqs = list(equations()) + list(extra)
    lines = ['LIB "primdec.lib";', 'LIB "elim.lib";',
             "ring Rng = 0,(%s),dp;" % ",".join(VARS),
             "ideal zzgI = %s;" % ",\n  ".join(eqs)]
    if do == "minAssGTZ":
        lines += ["list zzgL = minAssGTZ(zzgI);",
                  'printf("NCOMP %s", size(zzgL));',
                  "int zzgk;",
                  "for (zzgk = 1; zzgk <= size(zzgL); zzgk++) {",
                  '  printf("COMPONENT %s dim %s", zzgk, dim(std(zzgL[zzgk])));',
                  '  printf("GENS %s", string(zzgL[zzgk]));',
                  "}"]
    elif do == "std":
        lines += ["ideal zzgG = std(zzgI);",
                  'printf("DIM %s", dim(zzgG));',
                  'printf("GENS %s", string(zzgG));']
    lines.append("quit;")
    return "\n".join(lines) + "\n"


def main():
    res = {"_header": "UNAUDITED W21-M1-TENSOR 2x2 classification. Exact."}
    ok, det = S.selftest()
    res["guard_selftest"] = ok
    print("guard self-test: %s" % ok)
    script = build()
    open(os.path.join(HERE, "class2.sing"), "w").write(script)
    try:
        out, errs = S.run(script, set(VARS), timeout=2400)
    except subprocess.TimeoutExpired:
        print("minAssGTZ TIMED OUT (2400 s)")
        res["minAssGTZ"] = "timeout"
        json.dump(res, open(os.path.join(HERE, "results_class2.json"), "w"),
                  indent=1)
        return
    res["singular_errors"] = errs
    if errs:
        print("SINGULAR ERRORS:", errs[:5])
    open(os.path.join(HERE, "log_class2_raw.txt"), "w").write(out)
    print(out[:6000])
    res["output_head"] = out[:20000]
    json.dump(res, open(os.path.join(HERE, "results_class2.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
