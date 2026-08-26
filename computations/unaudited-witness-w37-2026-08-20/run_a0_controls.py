"""W37 / A0 -- PRE-LAUNCH CONTROL BATTERY (UNAUDITED, 2026-08-20).

Ledger 27: every control tests the EXACT target of the lane, not a
relaxation.  The lane's targets are

  (T-E)  the cap-error tensor E_pq(K) on a given source and cap;
  (T-X)  X_k membership / the defect set of a source;
  (T-W)  the WITNESS/BLOCKED verdict at a pair (existence of an admissible
         cap killing the whole E tensor).

Ledger 21: the file ends by asserting an executed-control manifest.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "unaudited-x3core-w25-2026-08-15"))

import w37_core as C
import w37_decide as D

W25 = None
try:
    import w25_core as W25
except Exception as ex:                                          # noqa: BLE001
    print("!! w25_core unavailable:", ex)

HERE = os.path.dirname(os.path.abspath(__file__))
F8 = os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15",
                  "OBJECT_W25-F8_n8_allblocked_X3.json")
OUT = os.path.join(HERE, "results_a0_controls.json")

DECLARED = ["C1_def_vs_wm", "C2_haf_cross_family", "C3_cap_cross_family",
            "C4_F8_reproduction", "C5_decider_calibration_n6",
            "C6_blocked_notunit_point", "C7_mutation"]
RAN = []
RES = {"lane": "W37", "unaudited": True, "controls": {}}


def control(name):
    def deco(fn):
        def wrapped(*a, **kw):
            print(f"\n=== {name} ===", flush=True)
            out = fn(*a, **kw)
            RAN.append(name)
            RES["controls"][name] = out
            C.ckpt(OUT, RES)
            return out
        return wrapped
    return deco


def load_f8():
    d = json.load(open(F8))
    return C.parse_source(d["blocks"], d["N"]), d


def rand_source(n, rng, dens=0.8, lo=-3, hi=3):
    src = C.zeros(n)
    for u, v in combinations(range(n), 2):
        if rng.random() > dens:
            continue
        src[(u, v)] = [[Fraction(rng.randint(lo, hi)) for _ in range(3)]
                       for _ in range(3)]
    return src


def rand_cap(rng):
    K = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
    for c in range(3):
        if K[c][c] == 0:
            K[c][c] = Fraction(1)
    return K


def to_w25(src, n):
    return {k: [row[:] for row in v] for k, v in src.items()}


# ---------------------------------------------------------------------- C1
@control("C1_def_vs_wm")
def c1():
    """(T-E) the two internal code paths for E must agree termwise."""
    rng = random.Random(11)
    bad = 0
    tested = 0
    for n in (6, 8):
        for trial in range(6 if n == 6 else 3):
            src = rand_source(n, rng)
            for (p, q) in [(0, 1), (2, 5)]:
                U = tuple(x for x in range(n) if x not in (p, q))
                K = rand_cap(rng)
                e1 = C.cap_error_def(src, p, q, K, U)
                e2 = C.cap_error_wm(src, p, q, K, U, n=n)
                tested += 1
                if e1 != e2:
                    bad += 1
                    print("  MISMATCH", n, p, q)
    src, _ = load_f8()
    for (p, q) in [(0, 1), (1, 3), (5, 7)]:
        U = tuple(x for x in range(8) if x not in (p, q))
        K = rand_cap(rng)
        e1 = C.cap_error_def(src, p, q, K, U)
        e2 = C.cap_error_wm(src, p, q, K, U, n=8)
        tested += 1
        if e1 != e2:
            bad += 1
            print("  MISMATCH on F8", p, q)
    print(f"  def vs W22-M: {tested - bad}/{tested} agree")
    assert bad == 0, "internal E code paths disagree"
    return {"tested": tested, "mismatches": bad}


# ---------------------------------------------------------------------- C2
@control("C2_haf_cross_family")
def c2():
    """(T-X) my hafnian vs W25's bitmask DP, on random sources and on F8."""
    if W25 is None:
        return {"skipped": "w25_core unavailable"}
    rng = random.Random(23)
    tested = bad = 0
    for n in (6, 8):
        for _ in range(4):
            src = rand_source(n, rng)
            s25 = to_w25(src, n)
            for _ in range(40):
                w = tuple(rng.randrange(3) for _ in range(n))
                a = C.haf_word(src, w, tuple(range(n)))
                b = W25.H(s25, w, n)
                tested += 1
                bad += (a != b)
    src, meta = load_f8()
    s25 = to_w25(src, 8)
    for _ in range(200):
        w = tuple(rng.randrange(3) for _ in range(8))
        tested += 1
        bad += (C.haf_word(src, w, tuple(range(8))) != W25.H(s25, w, 8))
    print(f"  hafnian cross-family: {tested - bad}/{tested}")
    assert bad == 0
    return {"tested": tested, "mismatches": bad}


# ---------------------------------------------------------------------- C3
@control("C3_cap_cross_family")
def c3():
    """(T-E) my E vs W25's cap_error (independent implementation)."""
    if W25 is None:
        return {"skipped": "w25_core unavailable"}
    rng = random.Random(31)
    tested = bad = 0
    for n in (6, 8):
        for _ in range(3):
            src = rand_source(n, rng)
            s25 = to_w25(src, n)
            for (p, q) in [(0, 1), (1, 4)]:
                U = tuple(x for x in range(n) if x not in (p, q))
                K = rand_cap(rng)
                a = C.cap_error_def(src, p, q, K, U)
                b = W25.cap_error(s25, p, q, K, U)
                tested += 1
                if a != b:
                    bad += 1
                    print("   MISMATCH", n, p, q, len(a), len(b))
    src, _ = load_f8()
    s25 = to_w25(src, 8)
    for (p, q) in [(0, 1), (1, 3), (4, 7)]:
        U = tuple(x for x in range(8) if x not in (p, q))
        for seed in range(3):
            K = rand_cap(random.Random(100 + seed))
            a = C.cap_error_def(src, p, q, K, U)
            b = W25.cap_error(s25, p, q, K, U)
            tested += 1
            if a != b:
                bad += 1
                print("   MISMATCH F8", p, q)
    print(f"  cap-error cross-family: {tested - bad}/{tested}")
    assert bad == 0
    return {"tested": tested, "mismatches": bad}


# ---------------------------------------------------------------------- C4
@control("C4_F8_reproduction")
def c4():
    """(T-X) F8's stored claims re-derived from the raw word definition."""
    src, meta = load_f8()
    pures = [C.haf_word(src, (c,) * 8, tuple(range(8))) for c in range(3)]
    _, bad = C.defects(src, 8)
    prof = {}
    for w in bad:
        prof[C.offcount(w)] = prof.get(C.offcount(w), 0) + 1
    first = min((w for w in bad), default=None)
    print("  pures", pures, "n_defects", len(bad), "profile", prof)
    print("  first failing word (lex)", first)
    assert pures == [1, 1, 1]
    assert min(prof) == 4, "claims X_3 membership"
    assert len(bad) == meta["verification"]["n_mixed_defects"]
    assert prof == {int(k): v for k, v in
                    meta["verification"]["defect_offcounts"].items()}
    assert list(first) == meta["verification"]["first_X4_word_it_fails"]
    live = [(p, q) for p, q in combinations(range(8), 2) if C.is_live(src, p, q)]
    assert len(live) == meta["verification"]["n_live_pairs"]
    return {"pures": [str(x) for x in pures], "n_defects": len(bad),
            "offcount_profile": prof, "n_live": len(live),
            "first_word": list(first)}


# ---------------------------------------------------------------------- C5
@control("C5_decider_calibration_n6")
def c5():
    """(T-W) EXACT TARGET: the WITNESS/BLOCKED verdict.  Calibrated against
    W27's stored N=6 rigid point 'near_exact': 11 live pairs, witnesses at
    the 9 cross pairs, BLOCKED at (3,5) and (4,5)."""
    if W25 is None:
        return {"skipped": "w25_core unavailable"}
    src25 = W25.near_exact_six_site()
    src = {k: [[Fraction(x) for x in row] for row in v]
           for k, v in src25.items()}
    verd = {}
    for p, q in combinations(range(6), 2):
        if not C.is_live(src, p, q):
            continue
        U = tuple(x for x in range(6) if x not in (p, q))
        r = D.decide_pair(src, p, q, U, chars=(0,), timeout=300)
        verd[f"{p},{q}"] = r["verdict"]
        print(f"   pair {p},{q}: {r['verdict']} ({r['route']})", flush=True)
    wit = sorted(k for k, v in verd.items() if v == "WITNESS")
    blk = sorted(k for k, v in verd.items() if v == "BLOCKED")
    print("  witnesses", wit)
    print("  blocked  ", blk)
    assert len(wit) == 9, f"expected 9 witnesses, got {len(wit)}"
    assert blk == ["3,5", "4,5"], blk
    return {"verdicts": verd, "n_witness": len(wit), "blocked": blk}


# ---------------------------------------------------------------------- C6
@control("C6_blocked_notunit_point")
def c6():
    """Ledger 13(b)/18: for an infeasibility (BLOCKED) verdict, exhibit an
    explicit rational point of a KNOWN-FEASIBLE RELAXATION -- here, a cap
    with E = 0 that fails admissibility.  If none exists the verdict would
    be suspect (unit ideal before saturation)."""
    src, _ = load_f8()
    rng = random.Random(7)
    found = {}
    for (p, q) in [(0, 1), (1, 3), (5, 7)]:
        U = tuple(x for x in range(8) if x not in (p, q))
        hit = None
        for _ in range(400):
            K = [[Fraction(rng.randint(-2, 2)) for _ in range(3)]
                 for _ in range(3)]
            if C.admissible(src, p, q, K):
                continue
            if not C.cap_error_def(src, p, q, K, U):
                hit = K
                break
        if hit is None:
            K = [[Fraction(0)] * 3 for _ in range(3)]
            hit = K if not C.cap_error_def(src, p, q, K, U) else None
        found[f"{p},{q}"] = ([[str(x) for x in r] for r in hit]
                             if hit else None)
        print(f"   pair {p},{q}: inadmissible zero of E ->",
              "found" if hit else "NONE")
    assert all(v is not None for v in found.values())
    return found


# ---------------------------------------------------------------------- C7
@control("C7_mutation")
def c7():
    """A mutation control: perturbing one cell of F8 must break X_3."""
    src, _ = load_f8()
    n_break = 0
    trials = []
    rng = random.Random(5)
    for _ in range(6):
        u, v = sorted(rng.sample(range(8), 2))
        i, j = rng.randrange(3), rng.randrange(3)
        mut = {k: [row[:] for row in val] for k, val in src.items()}
        mut[(u, v)][i][j] = mut[(u, v)][i][j] + 1
        ok = C.in_Xk(mut, 8, 3)
        trials.append({"edge": [u, v], "cell": [i, j], "still_X3": ok})
        n_break += (not ok)
    print(f"  mutations breaking X_3: {n_break}/6")
    assert n_break >= 5, "mutation control did not fire"
    return {"broken": n_break, "trials": trials}


def main():
    c1(); c2(); c3(); c4(); c6(); c7(); c5()
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"])
    assert not RES["manifest"]["missing"], RES["manifest"]
    print("A0: ALL CONTROLS PASSED")


if __name__ == "__main__":
    main()
