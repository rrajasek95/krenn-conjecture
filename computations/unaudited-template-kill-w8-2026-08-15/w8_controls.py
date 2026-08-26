#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- mutation controls for every W8 checker.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

Controls implemented
  C1  numpy fibre engine vs a pure-Python reference (random templates)
  C2  W8 engine vs W2's w2_monomial.analyse on R_cell templates (same
      verdict family), i.e. cross-implementation agreement
  C3  planted O2  (a template built to have a mixed singleton)      -> O2
  C4  planted K0  (a colour with no supported constant matching)    -> K0
  C5  planted O1  (found, then INDEPENDENTLY re-verified from raw fibres)
  C6  planted survivor (all mixed fibres of size >= 3)              -> survivor
  C7  negative control: mutate a survivor into a killed template and back
  C8  FIE checker: planted violation and planted repair
  C9  symmetry: canonical form invariance + support/sigma invariance
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import permutations

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-witness-splitting-w2-2026-08-15")

import w8_core as C

RESULTS = {}


def reference_fibres(geo, template, word):
    """Pure Python, no numpy: list of matchings compatible with a word."""
    out = []
    for n, matching in enumerate(geo.matchings):
        ok = True
        for u, v in matching:
            e = geo.index[(u, v)]
            if not (template[e] >> (3 * word[u] + word[v])) & 1:
                ok = False
                break
        if ok:
            out.append(n)
    return out


def random_template(rng, m, cellrange=(1, 9)):
    edges = rng.sample(range(28), m)
    template = [0] * 28
    for e in edges:
        k = rng.randint(*cellrange)
        mask = 0
        for c in rng.sample(range(9), k):
            mask |= 1 << c
        template[e] = mask
    return tuple(template)


def control_C1(geo, rng, trials=40):
    bad = 0
    checked = 0
    for _ in range(trials):
        template = random_template(rng, rng.randint(8, 20))
        compat = C.compat_matrix(geo, template)
        table = C.fibre_table(geo, template, compat)
        for w in rng.sample(range(6561), 60):
            ref = reference_fibres(geo, template, geo.words[w])
            got = table.get(w, [])
            checked += 1
            if ref != got:
                bad += 1
    RESULTS["C1_numpy_vs_python"] = {"checks": checked, "mismatches": bad}
    return bad == 0


def control_C2(geo, rng, trials=25):
    import w2_monomial as W2
    w2geo = W2.geometry(8)
    agree, disagree, rows = 0, 0, []
    for _ in range(trials):
        m = rng.randint(12, 28)
        edges = rng.sample(range(28), m)
        labels = [None] * 28
        template = [0] * 28
        for e in edges:
            a, b = rng.randrange(3), rng.randrange(3)
            labels[e] = (a, b)
            template[e] = 1 << (3 * a + b)
        mine = C.analyse(geo, tuple(template))["verdict"]
        theirs = W2.analyse(w2geo, labels)["verdict"]
        rename = {"K0-missing-constant": "missing-constant",
                  "O2-literal-singleton": "O2-literal-singleton",
                  "O1-odd-holonomy": "O1-odd-holonomy",
                  "O2-one-live-class": "O2-one-live-class",
                  "K3-pure-vanishing": "K3-pure-vanishing",
                  "survivor": "survivor"}
        same = rename[mine] == theirs
        agree += same
        disagree += not same
        rows.append({"mine": mine, "w2": theirs, "agree": bool(same)})
    RESULTS["C2_vs_w2_engine"] = {"agree": agree, "disagree": disagree,
                                  "sample": rows[:6]}
    return disagree == 0


def planted_O2(geo):
    """One matching's cells only: every word it supports has fibre 1."""
    template = [0] * 28
    matching = geo.matchings[0]                    # (0,1)(2,3)(4,5)(6,7)
    for u, v in matching:
        template[geo.index[(u, v)]] = FULLDIAG = 0b100000001 | (1 << 4)
    return tuple(template)


def planted_K0(geo):
    template = [0] * 28
    for u, v in geo.matchings[0]:
        template[geo.index[(u, v)]] = (1 << 0) | (1 << 4)   # cells (0,0),(1,1)
    return tuple(template)


def planted_survivor(geo):
    """Two disjoint 4-cycles with full blocks: every fibre has >= 4 terms."""
    template = [0] * 28
    for cycle in ((0, 1, 2, 3), (4, 5, 6, 7)):
        for k in range(4):
            u, v = cycle[k], cycle[(k + 1) % 4]
            template[geo.index[tuple(sorted((u, v)))]] = C.FULL
    return tuple(template)


def find_planted_O1(geo, rng, tries=4000):
    """Prefer a calibrated m=28 R_cell template (all 28 carry an O1 circuit);
    fall back to random R_cell search."""
    try:
        with open("results_calib28.json") as handle:
            data = json.load(handle)
        for record in data["records"]:
            template = tuple(record["template"])
            out = C.analyse(geo, template)
            if out["verdict"] == "O1-odd-holonomy":
                return template, out
    except FileNotFoundError:
        pass
    for _ in range(tries):
        m = rng.randint(24, 28)
        edges = rng.sample(range(28), m)
        template = [0] * 28
        for e in edges:
            template[e] = 1 << rng.randrange(9)
        template = tuple(template)
        out = C.analyse(geo, template)
        if out["verdict"] == "O1-odd-holonomy":
            return template, out
    return None, None


def verify_O1_from_scratch(geo, template, verdict):
    """Independent re-derivation of an odd-holonomy certificate.

    Rebuilds the binomial relations from raw fibres (pure Python), rebuilds
    the integer dependency, and checks  sum n_k e_k = 0  with
    prod gamma^{n_k} != 1.  Exact integers/Fractions.
    """
    coords = C.CellCoords(geo, template)
    rows, gammas = [], []
    for w in range(6561):
        if not bool(geo.mixed[w]):
            continue
        members = reference_fibres(geo, template, geo.words[w])
        if len(members) == 2:
            a = coords.exponent(members[0], geo.words[w])
            b = coords.exponent(members[1], geo.words[w])
            rows.append([x - y for x, y in zip(a, b)])
            gammas.append(Fraction(-1))
    if not rows:
        return False, "no binomials"
    H, U, pivots, rank = C.hermite_with_transform(rows)
    for r in range(rank, len(rows)):
        relation = U[r]
        total = [0] * coords.width
        product = Fraction(1)
        for coefficient, row, gamma in zip(relation, rows, gammas):
            if coefficient:
                for c in range(coords.width):
                    total[c] += coefficient * row[c]
                product *= gamma ** coefficient
        if any(total):
            return False, "dependency is not a dependency"
        if product != 1:
            return True, {"coefficients": [x for x in relation if x],
                          "gamma_product": str(product),
                          "used_relations": sum(1 for x in relation if x)}
    return False, "no odd dependency found in the independent pass"


def control_C8(geo):
    template = list(planted_survivor(geo))
    before = C.fie_ok(geo, tuple(template))
    # repair: add 12 single cells (3-regular graph) covering all 24 demands
    cube = [(0, 4), (1, 5), (2, 6), (3, 7), (0, 5), (1, 6), (2, 7), (3, 4),
            (0, 6), (1, 7), (2, 4), (3, 5)]
    # far-end colour assignment: vertex p gets colours 0,1,2 on its 3 edges
    assign = {}
    for p in range(8):
        incident = [e for e in cube if p in e]
        for r, e in enumerate(sorted(incident)):
            j = e[0] if e[1] == p else e[1]
            assign[(p, j)] = r            # colour r at the FAR end j
    for u, v in cube:
        i = assign[(v, u)]                # colour at u demanded by v
        j = assign[(u, v)]                # colour at v demanded by u
        template[geo.index[(u, v)]] = 1 << (3 * i + j)
    after = C.fie_ok(geo, tuple(template))
    RESULTS["C8_fie"] = {"planted_violation_detected": not before,
                         "planted_repair_detected": after}
    return (not before) and after, tuple(template)


def main():
    geo = C.geometry(8)
    rng = random.Random(20260815)
    ok = {}

    ok["C1"] = control_C1(geo, rng)
    ok["C2"] = control_C2(geo, rng)

    t = planted_O2(geo)
    v = C.analyse(geo, t)
    RESULTS["C3_planted_O2"] = v["verdict"]
    ok["C3"] = v["verdict"] == "O2-literal-singleton"

    t = planted_K0(geo)
    v = C.analyse(geo, t)
    RESULTS["C4_planted_K0"] = v["verdict"]
    ok["C4"] = v["verdict"] == "K0-missing-constant"

    t, v = find_planted_O1(geo, rng)
    if t is None:
        RESULTS["C5_planted_O1"] = "not found"
        ok["C5"] = False
    else:
        good, detail = verify_O1_from_scratch(geo, t, v)
        RESULTS["C5_planted_O1"] = {
            "template": list(t), "engine": v["verdict"],
            "independent_check": good, "detail": detail}
        ok["C5"] = good

    # C5b: direct mutation control of the O1 detector (Character class).
    d1 = [1, 0, -1, 0]
    d2 = [0, 1, 0, -1]
    d3 = [1, 1, -1, -1]
    bad = C.Character(4)
    for row, gamma in ((d1, -1), (d2, -1), (d3, -1)):
        bad.add(row, Fraction(gamma))
    good = C.Character(4)
    for row, gamma in ((d1, -1), (d2, -1), (d3, 1)):
        good.add(row, Fraction(gamma))
    RESULTS["C5b_detector_mutation"] = {
        "inconsistent_detected": bad.odd_relation() is not None,
        "consistent_passes": good.odd_relation() is None}
    ok["C5b"] = (bad.odd_relation() is not None
                 and good.odd_relation() is None)

    t = planted_survivor(geo)
    v = C.analyse(geo, t)
    RESULTS["C6_planted_survivor"] = {
        "verdict": v["verdict"],
        "histogram": v.get("mixed_histogram"),
        "audit": C.audit(geo, t)}
    ok["C6"] = v["verdict"] == "survivor"

    # C7 mutation: delete one cell of the survivor -> must change the verdict
    mutated = list(planted_survivor(geo))
    e = next(i for i, mask in enumerate(mutated) if mask)
    mutated[e] = 1 << 0
    v2 = C.analyse(geo, tuple(mutated))
    restored = C.analyse(geo, planted_survivor(geo))["verdict"]
    RESULTS["C7_mutation"] = {"mutated_verdict": v2["verdict"],
                              "restored_verdict": restored}
    ok["C7"] = v2["verdict"] != "survivor" and restored == "survivor"

    good, repaired = control_C8(geo)
    ok["C8"] = good

    perm = (3, 1, 4, 0, 7, 6, 5, 2)
    cperm = (2, 0, 1)
    image = C.apply_symmetry(geo, repaired, perm, cperm)
    ok["C9"] = (C.support(image) == C.support(repaired)
                and C.sigma(image) == C.sigma(repaired)
                and C.fie_ok(geo, image) == C.fie_ok(geo, repaired)
                and sorted(C.fibre_histogram(geo, image).items())
                == sorted(C.fibre_histogram(geo, repaired).items()))
    RESULTS["C9_symmetry"] = {"invariant": ok["C9"]}

    RESULTS["summary"] = {k: bool(v) for k, v in ok.items()}
    print(json.dumps(RESULTS, indent=1, default=str))
    with open("results_controls.json", "w") as handle:
        json.dump(RESULTS, handle, indent=1, default=str)
    print("ALL CONTROLS PASS" if all(ok.values()) else "SOME CONTROL FAILED")
    return 0 if all(ok.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
