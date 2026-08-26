#!/usr/bin/env python3
"""W28 T4 -- controls: the calibration table, W25-F8 through this probe's own
engines, and the ledger batteries (6/11/12/13/14/18/19/20/21/22).
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402
import w28_diag as D                                              # noqa: E402
import w28_fast as F                                              # noqa: E402
import w28_sym as S                                               # noqa: E402

RES = {}
RAN = []
OUT = f"{BASE}/results_t4_controls.json"


def control(n):
    if n not in RAN:
        RAN.append(n)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def probe_fires(src, n, k, z=None):
    """Are all three colour systems at site z feasible?"""
    z = n - 1 if z is None else z
    for c in range(3):
        rows, rhs, tags, cols = K.site_rows_exact(src, z, c, n, k)
        part, kern = K.rref_solve(rows, rhs, len(cols))
        if part is None:
            return False
    return True


def main():
    t0 = time.time()
    rng = random.Random(4)

    print("=" * 74)
    print("(1) W25-F8 through W28's own engines")
    print("=" * 74)
    f8 = K.load_F8()
    ok3, w3 = K.in_Xk(f8, 8, 3)
    ok4, w4 = K.in_Xk(f8, 8, 4)
    pu = K.pures(f8, 8)
    nd = 0
    from itertools import product as pr
    for w in pr(range(3), repeat=8):
        if len(set(w)) == 1:
            continue
        if K.H_word(f8, w, 8) != 0:
            nd += 1
    print(f"   in X_3 {ok3}; in X_4 {ok4} (first failure {w4}); pures "
          f"{[str(x) for x in pu.values()]}; mixed defects {nd}")
    assert ok3 and not ok4 and list(w4) == [0, 0, 0, 0, 1, 1, 1, 1]
    assert nd == 103, nd
    RES["F8"] = {"in_X3": ok3, "in_X4": ok4, "first_X4_failure": list(w4),
                 "pures": [str(x) for x in pu.values()], "mixed_defects": nd,
                 "W27_reported_defects": 103}
    control("T4_1_F8")
    ck("f8")

    print("=" * 74)
    print("(2) THE CALIBRATION TABLE: does the site probe fire where X_k is "
          "KNOWN nonempty and go silent where X_k is KNOWN empty?")
    print("=" * 74)
    tab = {}
    for n in (6, 8):
        pms = K.delta3_pms(n)
        fam = []
        # family A: Delta^3_n with unit weights
        fam.append(("unit", K.delta3_source(n)))
        # family B: Delta^3_n with random nonzero weights (weights must
        # multiply to 1 on each matching for the pures; the probe only needs
        # the BACKGROUND, so weights are free here)
        for t in range(24):
            src = K.zero_source(n)
            for c in range(3):
                for e in pms[c]:
                    src[e][c][c] = Fraction(rng.choice([1, -1, 2, 3, -2]))
            fam.append((f"rand{t}", src))
        for k in (3, 4):
            fires = 0
            for nm, src in fam:
                if probe_fires(src, n, k):
                    fires += 1
            tab[f"({n},{k})"] = f"{fires}/{len(fam)}"
            print(f"   (N={n}, k={k}): probe fires {fires}/{len(fam)}")
    print(f"   expected signature: (6,3) and (8,3) FIRE (X_3 nonempty at both "
          f"rungs); (6,4) SILENT (X_4 = EXACT = empty at N=6); (8,4) is the "
          f"open cell -- it wears the (6,4) signature")
    assert tab["(6,3)"].split("/")[0] != "0"
    assert tab["(8,3)"].split("/")[0] != "0"
    assert tab["(6,4)"].startswith("0/")
    RES["calibration_table"] = tab
    control("T4_2_calibration")
    ck("calib")

    print("=" * 74)
    print("(3) LEDGER BATTERIES")
    print("=" * 74)
    led = {}
    # ledger 13: the no-shadowing guard must FIRE on a shadowing script
    bad_script = "ring zzR = 0, (m0,m1), dp;\npoly m0 = m1;\n"
    try:
        K.no_shadow_guard(bad_script, {"m0", "m1"})
        led["13_no_shadow_guard"] = "FAILED TO FIRE"
    except AssertionError:
        led["13_no_shadow_guard"] = "fires correctly"
    good_script = "ring zzR = 0, (m0,m1), dp;\npoly zzg = m1;\n"
    K.no_shadow_guard(good_script, {"m0", "m1"})
    led["13_clean_script_passes"] = "yes"

    # ledger 6/11/14: Singular reports errors on stdout with RC 0 -- the
    # '?'-scan must catch them; and elim.lib must be loadable
    try:
        K.run_singular("ring zzR = 0, (a,b), dp;\nideal zzI = sat(a,b);")
        led["14_elim_lib_missing_caught"] = "NOT CAUGHT"
    except RuntimeError as exc:
        led["14_elim_lib_missing_caught"] = f"caught: {str(exc)[:80]}"
    out = K.run_singular('LIB "elim.lib";\nring zzR = 0, (a,b), dp;\n'
                         'ideal zzI = a*b, a^2;\nlist zzL = sat(zzI, a);\n'
                         'ideal zzS = zzL[1];\n"SAT "; zzS;')
    led["14_sat_with_list_form"] = "ok"
    # ledger 22: rationals must be cleared before emission
    p = K.Poly(2, {(1, 0): Fraction(1, 3)})
    try:
        p.sing(["a", "b"])
        led["22_rational_emission_blocked"] = "NOT BLOCKED"
    except AssertionError:
        led["22_rational_emission_blocked"] = "blocked"
    q, L = K.clear_denoms([p])
    led["22_clear_denoms"] = f"multiplier {L}, emits {q[0].sing(['a','b'])}"
    # and Singular itself must reject the uncleared form with RC 0
    try:
        K.run_singular("ring zzR = 0, (a,b), dp;\npoly zzf = a^2/9;")
        led["22_singular_rational_caught"] = "NOT CAUGHT"
    except RuntimeError as exc:
        led["22_singular_rational_caught"] = f"caught: {str(exc)[:70]}"
    print(f"   {json.dumps(led, indent=3)}")
    RES["ledger"] = led
    control("T4_3_ledger")
    ck("ledger")

    print("=" * 74)
    print("(4) LEDGER 18: explicit points OUTSIDE each asserted locus")
    print("=" * 74)
    pts = {}
    # (a) for the F_21 verdict: an F_21 background + star satisfying every
    #     MIXED equation but with the constant coefficient K = 0 -- so the
    #     kill genuinely comes from the K != 0 side condition, not from a
    #     degenerate ideal.
    f21 = S.slice_f21()
    zero = [[Fraction(0)] * 3 for _ in range(3)]
    src0 = f21.build([zero])
    ok, rk, rc = S.averaged_feasible(src0, 0, 4)
    pts["F21_zero_background"] = {"feasible": ok, "rank_mixed": rk,
                                  "constant_row": [str(x) for x in rc]}
    # (b) a sigma-symmetric DIAGONAL background that IS feasible at k = 3 --
    #     a point where the k=4 conclusion does NOT already hold trivially
    sl = S.slice_sigma()
    found = None
    from itertools import product as pr2
    for combo in pr2(range(4), repeat=sl.nblocks):
        blocks = []
        for cc in combo:
            M = [[Fraction(0)] * 3 for _ in range(3)]
            if cc:
                M[cc - 1][cc - 1] = Fraction(1)
            blocks.append(M)
        s7 = sl.build(blocks)
        ts = [{e: s7[e][c][c] for e in s7 if s7[e][c][c] != 0}
              for c in range(3)]
        p3 = D.rung_profile(ts, (3,))
        if p3[3] == 3:
            found = combo
            pts["sigma_diag_X3_witness"] = {
                "pattern": list(combo),
                "profile": D.rung_profile(ts),
                "free_sites": {str(c): D.free_sites(ts, c) for c in range(3)}}
            break
    assert found is not None, "no sigma-diagonal X_3 witness -- slice vacuous"
    print(f"   F_21 zero background: {pts['F21_zero_background']}")
    print(f"   sigma-diagonal X_3 witness: pattern {found}, "
          f"profile {pts['sigma_diag_X3_witness']['profile']}, free sites "
          f"{pts['sigma_diag_X3_witness']['free_sites']}")
    RES["explicit_points"] = pts
    control("T4_4_explicit_points")
    ck("points")

    print("=" * 74)
    print("(5) LEDGER 19: the same verdict in several characteristics")
    print("=" * 74)
    agree = 0
    tot = 0
    for t in range(120):
        ts = [{}, {}, {}]
        for c in range(3):
            for e in rng.sample(list(combinations(range(7), 2)),
                                rng.randint(3, 7)):
                ts[c][e] = Fraction(rng.randint(-2, 2))
            ts[c] = {k2: v for k2, v in ts[c].items() if v != 0}
        src7 = {}
        for e in combinations(range(7), 2):
            src7[e] = [[Fraction(0)] * 3 for _ in range(3)]
            for c in range(3):
                src7[e][c][c] = ts[c].get(e, Fraction(0))
        a = F.rung_profile(src7, F.P1)
        b = F.rung_profile(src7, F.P2)
        d = D.rung_profile(ts)
        tot += 1
        agree += (a == b == d)
    print(f"   {agree}/{tot} agreed across p={F.P1}, p={F.P2} (both = 1 mod 3) "
          f"and exact Q")
    assert agree == tot
    RES["multichar"] = {"agree": agree, "total": tot,
                        "primes": [F.P1, F.P2]}
    control("T4_5_multichar")

    decl = ["T4_1_F8", "T4_2_calibration", "T4_3_ledger",
            "T4_4_explicit_points", "T4_5_multichar"]
    RES["manifest"] = {"declared": decl, "ran": RAN,
                       "missing": [x for x in decl if x not in RAN]}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: {RES['manifest']}")
    assert not RES["manifest"]["missing"]
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
