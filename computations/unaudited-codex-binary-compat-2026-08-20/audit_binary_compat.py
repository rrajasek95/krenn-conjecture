#!/usr/bin/env python3
"""Adversarial audit of the three-binary-restriction route at N=8.

STATUS: UNAUDITED COUNTEREXAMPLE / PROBE.  This script deliberately works
from the original endpoint-ordered cells A_uv[a,b] and the raw perfect-
matching definition.  It does not use an ideal or a finite-field search.

It certifies a four-parameter Laurent family, extracted from W40/T3a, for
which all three overlapping binary restrictions are exact and compatible.
In fact every level-4 word is exact.  The family fails only some genuinely
trichromatic level-5 (3,3,2) equations, so it is NOT a ternary exact source.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 8
COLORS = (0, 1, 2)
PAIRS = ((0, 1), (0, 2), (1, 2))
ZERO_EXP = (0, 0, 0, 0)  # parameters (s,t,a,b)


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


# A Laurent polynomial is {exponent_tuple: integer_coefficient}.
def lp_const(c):
    return {} if c == 0 else {ZERO_EXP: int(c)}


def lp_monom(exp, coeff=1):
    return {} if coeff == 0 else {tuple(exp): int(coeff)}


def lp_add(x, y):
    z = dict(x)
    for m, c in y.items():
        z[m] = z.get(m, 0) + c
        if z[m] == 0:
            del z[m]
    return z


def lp_mul(x, y):
    z = {}
    for mx, cx in x.items():
        for my, cy in y.items():
            m = tuple(a + b for a, b in zip(mx, my))
            z[m] = z.get(m, 0) + cx * cy
            if z[m] == 0:
                del z[m]
    return z


def lp_eval(x, vals):
    out = Fraction(0)
    for exp, coeff in x.items():
        term = Fraction(coeff)
        for v, k in zip(vals, exp):
            require(v != 0 or k >= 0, "zero substituted into Laurent inverse")
            term *= v ** k
        out += term
    return out


def lp_str(x):
    if not x:
        return "0"
    names = ("s", "t", "a", "b")
    parts = []
    for exp, coeff in sorted(x.items()):
        factors = []
        for name, k in zip(names, exp):
            if k:
                factors.append(name if k == 1 else f"{name}^{k}")
        mon = "*".join(factors) or "1"
        parts.append(f"{coeff}*{mon}")
    return " + ".join(parts).replace("1*1", "1")


def edges():
    return [(u, v) for u in range(N) for v in range(u + 1, N)]


def matchings(vs):
    vs = tuple(vs)
    if not vs:
        return [()]
    u = vs[0]
    out = []
    for i, v in enumerate(vs[1:]):
        rest = vs[1:i + 1] + vs[i + 2:]
        for tail in matchings(rest):
            out.append(((u, v),) + tail)
    return out


PMS = matchings(range(N))
require(len(PMS) == 105, "K8 must have 105 perfect matchings")


def blank_source():
    return {e: [[{} for _ in COLORS] for _ in COLORS] for e in edges()}


def put(src, u, v, cu, cv, value):
    require(u < v, "cells are stored with increasing endpoints")
    src[(u, v)][cu][cv] = dict(value)


def family_source():
    """W40/T3a as a four-parameter original-cell Laurent family.

    Parameters s,t,a,b are invertible.  The colour-2 pure layer has
      q04=a, q13=b, q26=-s*t, q57=-1/(a*b*s*t),
    so its unique pure matching has weight one.
    """
    src = blank_source()
    one, neg = lp_const(1), lp_const(-1)
    s = lp_monom((1, 0, 0, 0))
    t = lp_monom((0, 1, 0, 0))
    a = lp_monom((0, 0, 1, 0))
    b = lp_monom((0, 0, 0, 1))

    # W33-D5 twisted 4+4 {0,1} background.
    for u, v in ((0, 1), (2, 3), (4, 5), (6, 7)):
        put(src, u, v, 0, 0, one)
    for u, v in ((0, 3), (1, 2), (4, 7), (5, 6)):
        put(src, u, v, 1, 1, one)
    put(src, 0, 4, 0, 1, one)
    put(src, 0, 5, 1, 0, one)
    put(src, 1, 7, 0, 1, neg)
    put(src, 3, 4, 1, 0, neg)

    # Completion cells, directly in A_uv endpoint order.
    put(src, 1, 2, 0, 2, s)
    put(src, 2, 4, 2, 1, s)
    put(src, 0, 6, 0, 2, t)
    put(src, 6, 7, 2, 1, t)
    put(src, 0, 4, 2, 2, a)
    put(src, 1, 3, 2, 2, b)
    put(src, 2, 6, 2, 2, lp_monom((1, 1, 0, 0), -1))
    put(src, 5, 7, 2, 2, lp_monom((-1, -1, -1, -1), -1))
    return src


def amplitude_pm(src, word):
    """Raw definition: sum over all 105 perfect matchings."""
    total = {}
    for matching in PMS:
        term = lp_const(1)
        for u, v in matching:
            term = lp_mul(term, src[(u, v)][word[u]][word[v]])
            if not term:
                break
        total = lp_add(total, term)
    return total


def amplitude_dp_numeric(src, word, vals):
    """Independent recursive numeric hafnian engine for the point control."""
    cache = {0: Fraction(1)}

    def rec(mask):
        if mask in cache:
            return cache[mask]
        u = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << u)
        ans = Fraction(0)
        bits = rest
        while bits:
            v = (bits & -bits).bit_length() - 1
            bits ^= 1 << v
            e = (u, v) if u < v else (v, u)
            x = src[e][word[u]][word[v]] if u < v \
                else src[e][word[v]][word[u]]
            ans += lp_eval(x, vals) * rec(rest ^ (1 << v))
        cache[mask] = ans
        return ans

    return rec((1 << N) - 1)


def target(word):
    return 1 if len(set(word)) == 1 else 0


def off(word):
    return N - max(word.count(c) for c in COLORS)


def extract_pair(src, pair):
    """Restriction retaining its original colour labels."""
    a, b = pair
    return {e: {(x, y): dict(src[e][x][y]) for x in pair for y in pair}
            for e in edges()}


def pair_amplitude(pair_src, word):
    total = {}
    for matching in PMS:
        term = lp_const(1)
        for u, v in matching:
            term = lp_mul(term, pair_src[(u, v)][(word[u], word[v])])
            if not term:
                break
        total = lp_add(total, term)
    return total


def compatibility_failures(restrictions):
    """The complete entrywise overlap conditions for the three pairs.

    Two distinct 2x2 principal blocks overlap only in the pure diagonal
    cell for their common colour.  Therefore these 3*28 equalities are
    necessary and sufficient for a unique 3x3-cell amalgam.
    """
    failures = []
    for e in edges():
        for c, p, q in ((0, (0, 1), (0, 2)),
                        (1, (0, 1), (1, 2)),
                        (2, (0, 2), (1, 2))):
            x = restrictions[p][e][(c, c)]
            y = restrictions[q][e][(c, c)]
            if x != y:
                failures.append({"edge": list(e), "colour": c,
                                 "left_pair": list(p), "right_pair": list(q),
                                 "left": lp_str(x), "right": lp_str(y)})
    return failures


def amalgamate(restrictions):
    require(not compatibility_failures(restrictions),
            "cannot amalgamate incompatible principal blocks")
    src = blank_source()
    for pair in PAIRS:
        for e in edges():
            for x in pair:
                for y in pair:
                    value = restrictions[pair][e][(x, y)]
                    old = src[e][x][y]
                    if old:
                        require(old == value, "overlap changed during amalgamation")
                    else:
                        src[e][x][y] = dict(value)
    return src


def source_equal(x, y):
    return all(x[e][a][b] == y[e][a][b]
               for e in edges() for a in COLORS for b in COLORS)


def audit_binary_pair(pair_src, pair):
    failures = []
    checked = 0
    for word in itertools.product(pair, repeat=N):
        checked += 1
        got = pair_amplitude(pair_src, word)
        want = lp_const(target(word))
        if got != want:
            failures.append({"word": list(word), "got": lp_str(got),
                             "want": lp_str(want)})
    return checked, failures


def audit_level(src, max_off):
    checked, failures = 0, []
    for word in itertools.product(COLORS, repeat=N):
        if off(word) > max_off:
            continue
        checked += 1
        got = amplitude_pm(src, word)
        want = lp_const(target(word))
        if got != want:
            failures.append({"word": list(word), "off": off(word),
                             "got": lp_str(got), "want": lp_str(want)})
    return checked, failures


def nonzero_cells(src):
    out = []
    for e in edges():
        for a in COLORS:
            for b in COLORS:
                if src[e][a][b]:
                    out.append({"edge": list(e), "cell": [a, b],
                                "value": lp_str(src[e][a][b])})
    return out


def main():
    declared = [
        "w40_translation",
        "symbolic_binary_exactness",
        "symbolic_level4_exactness",
        "positive_through_filter",
        "raw_point_two_engine",
        "must_fire_overlap_mutation",
        "must_fire_exactness_mutation",
        "main_counterexample_decision",
    ]
    executed = []

    def mark(name):
        require(name in declared, f"undeclared control {name}")
        require(name not in executed, f"control ran twice: {name}")
        executed.append(name)

    src = family_source()
    restrictions = {p: extract_pair(src, p) for p in PAIRS}
    result = {
        "status": "UNAUDITED COUNTEREXAMPLE / SYMBOLIC PROBE",
        "target": ("standalone incompatibility claim: no three exact d=2 "
                   "N=8 sources on palettes 01,02,12 share their pure layers"),
        "parameter_ring": "Z[s^+-1,t^+-1,a^+-1,b^+-1]",
        "controls_declared": declared,
        "_controls_run": executed,
        "family_nonzero_cells": nonzero_cells(src),
    }

    # Ensure the hand translation of the integral W40/T3a witness is exact.
    w40_path = HERE.parent / "unaudited-x4general-w40-2026-08-20" / "results_t3.json"
    w40_bytes = w40_path.read_bytes()
    w40 = json.loads(w40_bytes)["engine_audit"]["witness_B_integral"]
    vals_one = tuple(Fraction(1) for _ in range(4))
    translation_bad = []
    for e in edges():
        for x in COLORS:
            for y in COLORS:
                ours = str(lp_eval(src[e][x][y], vals_one))
                stored = w40["source"][str(e)][x][y]
                if ours != stored:
                    translation_bad.append({"edge": list(e), "cell": [x, y],
                                            "ours": ours, "stored": stored})
    require(not translation_bad, f"W40 translation mismatch: {translation_bad[:1]}")
    result["w40_translation"] = {
        "ok": True, "cells_checked": len(edges()) * 9,
        "source_sha256": hashlib.sha256(w40_bytes).hexdigest(),
        "mismatches": translation_bad,
    }
    mark("w40_translation")

    # All 768 pair-word equations, over the Laurent ring itself.
    pair_results = {}
    for p in PAIRS:
        checked, failures = audit_binary_pair(restrictions[p], p)
        pair_results[str(p)] = {"words_checked": checked,
                                "failures": failures}
        require(not failures, f"binary exactness failure on {p}: {failures[:1]}")
    result["symbolic_binary_exactness"] = {
        "ok": True, "pairs": pair_results,
        "total_pair_word_checks": sum(x["words_checked"]
                                      for x in pair_results.values()),
    }
    mark("symbolic_binary_exactness")

    # Stronger than compatibility: every level-4 ternary equation holds.
    n4, bad4 = audit_level(src, 4)
    require(not bad4, f"symbolic level-4 failure: {bad4[:1]}")
    result["symbolic_level4_exactness"] = {
        "ok": True, "words_checked": n4, "failures": bad4}
    mark("symbolic_level4_exactness")

    # The exact compatibility filter reaches the full binary checks.
    overlap_bad = compatibility_failures(restrictions)
    glued = amalgamate(restrictions)
    result["positive_through_filter"] = {
        "ok": not overlap_bad and source_equal(src, glued),
        "candidates": 1, "filter_passed": 1, "full_checks": 1,
        "overlap_equalities_checked": 3 * len(edges()),
        "compatibility_failures": overlap_bad,
        "amalgamation_recovers_source": source_equal(src, glued),
    }
    require(result["positive_through_filter"]["ok"],
            "known positive did not reach full check")
    mark("positive_through_filter")

    # Raw-definition point audit with an independent recursive engine.
    vals = vals_one
    pm_bad, engine_disagreements = [], []
    off5_bad = []
    for word in itertools.product(COLORS, repeat=N):
        raw = lp_eval(amplitude_pm(src, word), vals)
        dp = amplitude_dp_numeric(src, word, vals)
        if raw != dp:
            engine_disagreements.append({"word": list(word),
                                         "pm": str(raw), "dp": str(dp)})
        if raw != target(word):
            item = {"word": list(word), "off": off(word), "value": str(raw)}
            pm_bad.append(item)
            if off(word) == 5:
                off5_bad.append(item)
    require(not engine_disagreements, "raw engines disagree")
    require(pm_bad and all(x["off"] == 5 for x in pm_bad),
            "point should fail exactly a nonempty set of level-5 equations")
    result["raw_point_two_engine"] = {
        "ok": True, "point": {"s": "1", "t": "1", "a": "1", "b": "1"},
        "all_ternary_words_checked": 3 ** N,
        "perfect_matchings_per_word": len(PMS),
        "engine_disagreements": engine_disagreements,
        "all_exactness_failures": pm_bad,
        "level5_332_failures": off5_bad,
    }
    mark("raw_point_two_engine")

    # Must-fire 1: break one of the shared-pure-layer equalities in only B02.
    mutated_pairs = {p: {e: {k: dict(v) for k, v in cells.items()}
                         for e, cells in restrictions[p].items()} for p in PAIRS}
    mutated_pairs[(0, 2)][(0, 1)][(0, 0)] = lp_const(2)
    mutation_bad = compatibility_failures(mutated_pairs)
    require(mutation_bad, "compatibility mutation was not rejected")
    result["must_fire_overlap_mutation"] = {
        "ok": True,
        "mutation": "B02_(0,1)[0,0]: 1 -> 2 while B01 is unchanged",
        "failures": mutation_bad,
    }
    mark("must_fire_overlap_mutation")

    # Must-fire 2: break a pure equation of the amalgamated source.
    mutated_src = family_source()
    mutated_src[(0, 1)][0][0] = lp_const(2)
    mutation_exact_bad = {}
    for p in ((0, 1), (0, 2)):
        checked, bad = audit_binary_pair(extract_pair(mutated_src, p), p)
        mutation_exact_bad[str(p)] = {"words_checked": checked,
                                      "failures": bad}
        require(bad, f"exactness mutation did not fire on {p}")
    result["must_fire_exactness_mutation"] = {
        "ok": True,
        "mutation": "A_(0,1)[0,0]: 1 -> 2",
        "affected_pair_results": mutation_exact_bad,
    }
    mark("must_fire_exactness_mutation")

    # Enumerate the omitted off=5 family equations symbolically as the sharp
    # boundary: binary compatibility, even plus X4, does not cover these.
    n5, bad5 = audit_level(src, 5)
    require(n5 == 3 ** N, "level 5 must be full exactness at N=8,d=3")
    require(bad5, "unexpected fully exact ternary source")
    require(all(x["off"] == 5 for x in bad5), "non-level5 failure escaped X4")
    result["main_counterexample_decision"] = {
        "ok": True,
        "verdict": ("COUNTEREXAMPLE: compatible exact binary triples exist; "
                    "the incompatibility route is false as a standalone theorem"),
        "stronger_fact": "a 4-dimensional Laurent family satisfies all X4 equations",
        "not_claimed": "the family is not a fully exact ternary source",
        "full_word_checks": n5,
        "symbolic_full_exactness_failures": bad5,
        "missing_profiles": sorted({tuple(sorted(
            (x["word"].count(c) for c in COLORS), reverse=True)) for x in bad5}),
    }
    mark("main_counterexample_decision")

    require(executed == declared,
            f"control manifest mismatch: executed={executed}, declared={declared}")
    result["manifest"] = {"ok": True, "declared": declared,
                          "executed": list(executed)}
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    out = HERE / "results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "verdict": result["main_counterexample_decision"]["verdict"],
        "pair_word_checks": result["symbolic_binary_exactness"]["total_pair_word_checks"],
        "level4_word_checks": n4,
        "full_failures": len(bad5),
        "manifest": result["manifest"],
        "output": str(out),
    }, indent=2))


if __name__ == "__main__":
    main()
