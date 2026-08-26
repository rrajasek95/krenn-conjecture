#!/usr/bin/env python3
"""AUDIT A4 / CHECK 02 -- CLAIM 4, independent symbolic verification.

Route deliberately different from W12's run_t1d (which used a single
Rabinowitsch test 1 in <I, t*prod*Fc-1>):

  (A) SATURATION route: S = sat(<E1..E7>, prod of all variables); check
      that F(0^8) reduces to 0 modulo std(S).  If yes, then on ANY point
      with all cells nonzero satisfying E1..E7 we have F(0^8) = 0.
  (B) drop-one mutation controls are answered NOT by a Groebner "no" but
      by EXPLICIT EXACT RATIONAL WITNESSES: a point with every variable a
      nonzero rational, the other six equations satisfied, F(0^8) != 0.
  (C) control: the same seven equations must not force F(1^8) or F(2^8)
      to vanish (again by explicit witness).
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")
import a4_engine as E  # noqa: E402

with open(os.path.join(W8, "results_close_m20.json")) as fh:
    SURV = tuple(json.load(fh)["survivors"][0])
T = E.Template.from_masks(SURV)

WORDS = ["00011000", "00011020", "00111000", "00111020",
         "00100000", "00100020", "00000020"]
CONSTS = ["00000000", "11111111", "22222222"]
POLY = {s: T.fibre_poly(tuple(int(c) for c in s)) for s in WORDS + CONSTS}

out = {}


def singular(script, timeout=1800):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[:3000])
    # Singular reports many errors on stdout with returncode 0 -- catch them.
    if "?" in p.stdout or "?" in p.stderr:
        raise RuntimeError("SINGULAR ERROR:\n" + p.stdout[:2000]
                           + "\n" + p.stderr[:1000])
    return p.stdout


# ------------------------------------------------------------ (A) saturation
def sat_check(gens_words, target_word, extra_vars=()):
    used = set()
    for s in list(gens_words) + [target_word]:
        for mono in POLY[s]:
            used |= set(mono)
    used |= set(extra_vars)
    used = sorted(used)
    nm = {v: f"y{k}" for k, v in enumerate(used)}
    names = [nm[v] for v in used]

    def sp(s):
        return "+".join("*".join(nm[v] for v in sorted(m)) for m in POLY[s])

    script = "\n".join([
        'LIB "elim.lib";',
        f'ring R=0,({",".join(names)}),dp;',
        "ideal I=" + ",".join(sp(s) for s in gens_words) + ";",
        f"poly pr={'*'.join(names)};",
        # NB: `ideal S=sat(I,pr)[1];` is a TRAP -- Singular coerces sat's
        # 1-element list to an ideal and [1] then picks its first GENERATOR.
        "list SL=sat(I,pr);",
        "ideal S=SL[1];",
        "ideal G=std(S);",
        f'"SAT "+string(reduce({sp(target_word)},G)==0);'])
    res = singular(script)
    return ("SAT 1" in res), res.strip(), names


ok, raw, names = sat_check(WORDS, "00000000")
out["A_saturation_forces_F0_zero"] = ok
out["A_singular_raw"] = raw
out["A_nvars"] = len(names)
print(f"(A) SATURATION: <E1..E7> : (prod vars)^inf  forces F(0^8)=0 ? {ok}")

# control on the same route: the six-equation subsystems must NOT force it
drop_sat = {}
for k in range(len(WORDS)):
    sub = [w for n, w in enumerate(WORDS) if n != k]
    okk, _, _ = sat_check(sub, "00000000")
    drop_sat[WORDS[k]] = okk
    print(f"    drop {WORDS[k]}: still forces F(0^8)=0 ? {okk}")
out["A_drop_one_saturation"] = drop_sat

# control: do the seven force the OTHER constant words to vanish?
other = {}
for s in ("11111111", "22222222"):
    okk, _, _ = sat_check(WORDS, s)
    other[s] = okk
    print(f"    do E1..E7 force F({s})=0 ? {okk}")
out["A_other_constants"] = other


# --------------------------------- (B) explicit witnesses for drop-one
def cell(u, v, i, j):
    return (T.eidx[(u, v)], i, j)


VARS = sorted({v for s in WORDS + CONSTS for m in POLY[s] for v in m})

# equations in solved form: (equation index) -> (variable to solve for,
# function giving its value from the others).  All are LINEAR in the solved
# variable, with a nonzero coefficient made of other variables.
SOLVE = {
    0: (cell(2, 6, 0, 0), lambda v: -v[cell(2, 4, 0, 1)] * v[cell(5, 6, 0, 0)]
        / v[cell(4, 5, 1, 0)]),
    1: (cell(2, 6, 0, 2), lambda v: -v[cell(2, 4, 0, 1)] * v[cell(5, 6, 0, 2)]
        / v[cell(4, 5, 1, 0)]),
    2: (cell(2, 6, 1, 0), lambda v: -v[cell(2, 4, 1, 1)] * v[cell(5, 6, 0, 0)]
        / v[cell(4, 5, 1, 0)]),
    3: (cell(2, 6, 1, 2), lambda v: -v[cell(2, 4, 1, 1)] * v[cell(5, 6, 0, 2)]
        / v[cell(4, 5, 1, 0)]),
    4: (cell(1, 6, 0, 0), lambda v: -v[cell(1, 5, 0, 0)] * v[cell(2, 6, 1, 0)]
        / v[cell(2, 5, 1, 0)]),
    5: (cell(1, 6, 0, 2), lambda v: -v[cell(1, 5, 0, 0)] * v[cell(2, 6, 1, 2)]
        / v[cell(2, 5, 1, 0)]),
    6: (cell(1, 2, 0, 0), lambda v: -(v[cell(1, 5, 0, 0)] * v[cell(2, 6, 0, 2)]
                                      + v[cell(1, 6, 0, 2)] * v[cell(2, 5, 0, 0)])
        / v[cell(5, 6, 0, 2)]),
}
# note the solve ORDER matters (4,5 use 2,3; 6 uses 1 and 5)
ORDER = [0, 1, 2, 3, 4, 5, 6]

rng = random.Random(4242)


def rand_point():
    return {v: Fraction(rng.randint(1, 30), rng.randint(1, 30))
            * rng.choice([1, -1]) for v in VARS}


def witness_dropping(k, target="00000000", tries=400):
    """Point with all VARS nonzero, equations != k satisfied, F(target)!=0."""
    for _ in range(tries):
        v = rand_point()
        try:
            for idx in ORDER:
                if idx == k:
                    continue
                var, fn = SOLVE[idx]
                v[var] = fn(v)
        except ZeroDivisionError:
            continue
        if any(x == 0 for x in v.values()):
            continue
        good = all(E.poly_eval(POLY[WORDS[i]], v) == 0
                   for i in range(7) if i != k)
        if not good:
            continue
        if E.poly_eval(POLY[target], v) != 0:
            return v
    return None


wit = {}
for k in range(7):
    v = witness_dropping(k)
    wit[WORDS[k]] = None if v is None else {
        E.varname(T, var): str(val) for var, val in sorted(v.items())}
    resid = None if v is None else {
        WORDS[i]: str(E.poly_eval(POLY[WORDS[i]], v)) for i in range(7)}
    print(f"(B) drop {WORDS[k]}: explicit witness found = {v is not None}"
          + ("" if v is None else
             f"  F(0^8)={E.poly_eval(POLY['00000000'], v)}"))
    if v is not None:
        assert all(E.poly_eval(POLY[WORDS[i]], v) == 0
                   for i in range(7) if i != k)
        assert all(x != 0 for x in v.values())
out["B_drop_one_witnesses"] = {k: (w is not None) for k, w in wit.items()}
out["B_witness_example"] = wit[WORDS[0]]

# the FULL seven: there must be NO such witness (sanity of the search)
v = witness_dropping(-1)          # k=-1 -> all seven imposed
out["B_full_system_witness"] = (v is not None)
print(f"(B) CONTROL all seven imposed: witness with F(0^8)!=0 found = "
      f"{v is not None}   (False expected)")

# and the OTHER constants stay nonzero under all seven
for s in ("11111111", "22222222"):
    v = witness_dropping(-1, target=s)
    out[f"B_other_constant_{s}"] = (v is not None)
    print(f"(B) all seven imposed, F({s}) != 0 witness = {v is not None}"
          f"   (True expected)")

with open(os.path.join(HERE, "results_chk02.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote results_chk02.json")
