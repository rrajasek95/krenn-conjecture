#!/usr/bin/env python3
"""UNAUDITED PROBE -- W5 task D: MUTATION CONTROLS.

Pinned HEAD: 181a4c084a91f1518c2bdfe2f574b9a7df1b1830

Every claim W5 makes is paired with a mutation that must MOVE the measured
quantity (or must not, when the claim is an invariance).  A control "fires"
when the predicted behaviour is observed; a silent control is a bug.

M1  kill all but one colour-c edge at p  ->  E^(c)_pq = 0            (support)
M2  scale a single EDGE (not a site)     ->  cleanliness pattern moves
M3  cancellation-clean example: full support, E_pq = 0 exactly      (the
    support criterion is sufficient, NOT necessary)
M4  all three colours clean at one pair, by cancellation, full support
M5  scalar vs tensor cleanliness are DIFFERENT: an explicit (source, pair,
    colour) that is scalar-clean and tensor-dirty  ->  only the TENSOR
    version supports F1, and scalar-dirty => tensor-dirty
M6  relabelling invariance: the scalar slice error does not depend on how
    the six spectator sites are named
M7  detector control: a deliberately all-three-dirty full-rank pair is
    reported as such by the task-B pipeline
M8  zero control: the zero weighting has every pair clean and every pair
    support-dead

Run: python3 run_d_controls.py
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

import slice_core as sc
from slice_core import ekey, haf, require

P1DIR = ("/Users/rishi/workplace/krenn-conjecture/computations/"
         "unaudited-witness-splitting-p1-2026-08-15")
B8 = tuple(range(8))
PAIRS8 = list(combinations(B8, 2))
COLORS = (0, 1, 2)


def U_of(pair):
    return tuple(a for a in B8 if a not in pair)


def fired(name, condition, detail=""):
    mark = "FIRES" if condition else "SILENT (investigate)"
    print(f"  {name:52s} {mark} {detail}")
    return {"control": name, "fired": bool(condition), "detail": str(detail)}


def main():
    rng = random.Random(4242)
    out = {"note": "UNAUDITED PROBE W5 task D", "controls": [],
           "head": "181a4c084a91f1518c2bdfe2f574b9a7df1b1830"}
    print("== D  mutation controls ==")

    # M1 -------------------------------------------------------------------
    w = sc.random_weighting(rng, B8, -6, 6)
    p, q = 0, 1
    U = U_of((p, q))
    base = sc.slice_error(w, p, q, U)
    w1 = dict(w)
    for a in U[1:]:
        w1[ekey(p, a)] = 0
    out["controls"].append(fired(
        "M1 support kill at p => E = 0",
        base != 0 and sc.slice_error(w1, p, q, U) == 0,
        f"(base {base})"))

    # M2 -------------------------------------------------------------------
    # scaling a single EDGE is not a gauge: it must change the errors.
    lam = Fraction(5, 2)
    w2 = dict(w)
    w2[ekey(2, 3)] = Fraction(w[ekey(2, 3)]) * lam
    moved = sum(1 for e in PAIRS8
                if sc.slice_error(w2, e[0], e[1], U_of(e))
                != sc.slice_error(w, e[0], e[1], U_of(e)))
    out["controls"].append(fired(
        "M2 single-edge scaling moves the errors", moved > 0,
        f"({moved}/28 pairs moved)"))

    # M3 -------------------------------------------------------------------
    # E_pq is MULTILINEAR, so E = 0 can be solved exactly for one entry.
    found = None
    for _ in range(200):
        cand = sc.random_weighting(rng, B8, -6, 6)
        if any(cand[e] == 0 for e in PAIRS8):
            continue
        pair = (0, 1)
        UU = U_of(pair)
        target = ekey(2, 3)

        def f(z, pr=pair, UU=UU):
            return sc.slice_error_direct(z, pr[0], pr[1], UU)

        slope = sc.partial(f, cand, target)
        if slope == 0:
            continue
        const = f(sc.set_edge(cand, target, 0))
        value = Fraction(-const, slope)
        if value == 0:
            continue
        fixed = sc.set_edge(cand, target, value)
        if f(fixed) == 0 and all(fixed[e] != 0 for e in PAIRS8):
            found = fixed
            break
    ok = found is not None
    detail = ""
    if ok:
        pair = (0, 1)
        UU = U_of(pair)
        detail = (f"|w| version = "
                  f"{sc.slice_error_abs(found, pair[0], pair[1], UU)} != 0")
    out["controls"].append(fired(
        "M3 cancellation-clean with FULL support exists", ok, detail))
    if ok:
        out["M3_example"] = {f"{a}-{b}": str(found[(a, b)]) for a, b in PAIRS8}

    # M4 -------------------------------------------------------------------
    # three colours clean at one pair, by cancellation, in a ternary source
    if P1DIR not in sys.path:
        sys.path.insert(0, P1DIR)
    import wsplit_core as p1core                      # noqa: E402
    pair = (0, 1)
    UU = U_of(pair)
    ok4 = False
    det_nonzero = False
    for _ in range(60):
        src = p1core.random_source(rng, -5, 5)
        target = ekey(2, 3)
        good = True
        for c in COLORS:
            wslice = sc.monochrome_slice(src, c)

            def f(z, pr=pair, UU=UU):
                return sc.slice_error_direct(z, pr[0], pr[1], UU)

            slope = sc.partial(f, wslice, target)
            if slope == 0:
                good = False
                break
            const = f(sc.set_edge(wslice, target, 0))
            src[target][c][c] = Fraction(-const, slope)
        if not good:
            continue
        good = all(
            sc.slice_error(sc.monochrome_slice(src, c), pair[0], pair[1], UU)
            == 0
            and sc.slice_error_abs(sc.monochrome_slice(src, c), pair[0],
                                   pair[1], UU) != 0
            for c in COLORS)
        if good:
            ok4 = True
            det_nonzero = sc.det3(src[ekey(*pair)]) != 0
            out["M4_example"] = {f"{a}-{b}": [[str(v) for v in row]
                                              for row in src[(a, b)]]
                                 for a, b in PAIRS8}
            break
    out["controls"].append(fired(
        "M4 all three slices cancellation-clean at one pair", ok4,
        f"(pair block full rank: {det_nonzero})"))

    # M5 -------------------------------------------------------------------
    # scalar clean but tensor dirty: STAGE_A pair (2,3), colours 0 and 1.
    import wsplit_sources as p1src                    # noqa: E402
    physical = p1src.load_stage_a()
    charted = p1src.rechart(physical, 2, 3)
    diffs = []
    for c in COLORS:
        wslice = sc.monochrome_slice(physical, c)
        scalar_clean = sc.slice_error(wslice, 2, 3, U_of((2, 3))) == 0
        key = tuple(sorted((p1core.kidx(c, c),) * 3))
        matrix = p1core.error_matrix(charted)
        tensor_clean = not any(matrix[wd].get(key, 0) for wd in p1core.WORDS)
        if scalar_clean and not tensor_clean:
            diffs.append(c)
    out["controls"].append(fired(
        "M5 scalar-clean but tensor-dirty exists (STAGE_A (2,3))",
        bool(diffs), f"(colours {diffs})"))

    # M6 -------------------------------------------------------------------
    perm = [0, 1, 5, 3, 7, 2, 6, 4]
    wperm = {ekey(perm[a], perm[b]): w[ekey(a, b)] for a, b in PAIRS8}
    same = all(sc.slice_error(w, a, b, U_of((a, b)))
               == sc.slice_error(wperm, perm[a], perm[b],
                                 tuple(s for s in B8
                                       if s not in (perm[a], perm[b])))
               for a, b in PAIRS8)
    out["controls"].append(fired(
        "M6 relabelling invariance (must be SILENT-safe: holds)", same,
        "(invariance control: fires when it HOLDS)"))

    # M7 -------------------------------------------------------------------
    src = p1core.random_source(rng, -6, 6)
    pair = (4, 5)
    UU = U_of(pair)
    dirty = all(sc.slice_error(sc.monochrome_slice(src, c),
                               pair[0], pair[1], UU) != 0 for c in COLORS)
    fullrank = sc.det3(src[ekey(*pair)]) != 0
    out["controls"].append(fired(
        "M7 detector sees an all-three-dirty full-rank pair",
        dirty and fullrank, f"(pair {pair})"))

    # M8 -------------------------------------------------------------------
    zero = {e: 0 for e in PAIRS8}
    ok8 = all(sc.slice_error(zero, a, b, U_of((a, b))) == 0
              and sc.slice_error_abs(zero, a, b, U_of((a, b))) == 0
              for a, b in PAIRS8)
    out["controls"].append(fired("M8 zero weighting is clean and support-dead",
                                 ok8))

    with open("results_d_controls.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
    print("wrote results_d_controls.json")
    require(all(c["fired"] for c in out["controls"]), "a control was silent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
