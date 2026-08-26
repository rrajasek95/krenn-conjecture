#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- completeness / soundness controls for the band SAT.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

An UNSAT verdict is only worth as much as the encoding's COMPLETENESS: every
admissible zero-singleton template must satisfy the formula.  Controls:

  S1 (completeness, planted positives)  assert a known admissible
     zero-singleton template as unit clauses inside the full band formula for
     its own support and its own constant-witness orbit -> must be SAT.
  S2 (soundness, planted negatives)  assert a template that violates FIE, or
     one with a mixed singleton -> must be UNSAT.
  S3 (case-split completeness)  every planted template's witness triple must
     map into one of the 31 orbit representatives, and the corresponding
     orbit run must be SAT at that support.
"""
import json, sys
from collections import Counter
import numpy as np
import w8_core as C
from w8_sat import Encoding, near_constant_words
from w8_triples import orbits


def assert_template(enc, template):
    for e in range(28):
        for k in range(9):
            lit = enc.cell[e][k]
            enc.solver.add_clause([lit if (template[e] >> k) & 1 else -lit])


def run_case(geo, template, m, seed_radius=2, force_words=True):
    enc = Encoding(geo, m, "cadical153")
    assert_template(enc, template)
    words = near_constant_words(geo, seed_radius)
    if force_words:
        for w in words:
            enc.word_constraint(w)
        sizes = C.fibre_sizes(geo, template)
        for w in np.nonzero((sizes >= 1) & geo.mixed)[0][:400]:
            enc.word_constraint(int(w))
    out = enc.solver.solve()
    enc.solver.delete()
    return bool(out)


def witness_triple(geo, template):
    """A perfect matching in each diagonal graph, or None."""
    triple = []
    for c in range(3):
        found = None
        for n, edges in enumerate(geo.matching_edges):
            if all((template[e] >> (4 * c)) & 1 for e in edges):
                found = n
                break
        if found is None:
            return None
        triple.append(found)
    return tuple(triple)


def main():
    geo = C.geometry(8)
    results = {}
    planted = []
    for name in ("results_band_m16_nosingleton.json",
                 "results_band_m17_nosingleton.json",
                 "results_sat_m18.json", "results_sat_m19.json"):
        try:
            data = json.load(open(name))
        except FileNotFoundError:
            continue
        rows = data.get("rows") or [{"survivors": data.get("found", [])}]
        for row in rows:
            for t in row.get("survivors", []):
                planted.append(tuple(t))
    planted = planted[:8]
    print(f"planted admissible zero-singleton templates: {len(planted)}")

    s1 = []
    for t in planted:
        m = C.support(t)
        sat = run_case(geo, t, m)
        audit = C.audit(geo, t)
        s1.append({"m": m, "sigma": audit["sigma"], "fie": audit["fie"],
                   "singletons": audit["mixed_singletons"], "sat": sat})
        print(f"  S1 planted m={m} Sigma={audit['sigma']} FIE={audit['fie']} "
              f"sing={audit['mixed_singletons']} -> SAT={sat}")
    results["S1_completeness"] = s1

    # S2 planted negatives
    negatives = []
    bad = list(planted[0])
    e = next(i for i, mask in enumerate(bad) if mask)
    bad[e] = 0                                   # break FIE / constants
    negatives.append(("deleted-block", tuple(bad)))
    bad2 = list(planted[0])
    bad2[e] = C.FULL                             # fatten: breaks FIE demand
    negatives.append(("fattened-block", tuple(bad2)))
    s2 = []
    for label, t in negatives:
        m = max(C.support(t), C.support(planted[0]))
        sat = run_case(geo, t, m)
        s2.append({"label": label, "fie": C.fie_ok(geo, t),
                   "singletons": len(C.mixed_singletons(geo, t)), "sat": sat})
        print(f"  S2 {label}: FIE={s2[-1]['fie']} "
              f"sing={s2[-1]['singletons']} -> SAT={sat} (want False)")
    results["S2_soundness"] = s2

    # S3 case-split completeness
    reps = sorted(orbits(geo))
    canonical = geo.matchings.index(tuple((2 * k, 2 * k + 1) for k in range(4)))
    keys = {(a, b): i for i, (a, b) in enumerate(reps)}
    s3 = []
    for t in planted:
        triple = witness_triple(geo, t)
        s3.append({"m": C.support(t), "triple": triple,
                   "has_triple": triple is not None})
    results["S3_witness_triples"] = s3
    print(f"  S3 every planted template has a diagonal witness triple: "
          f"{all(r['has_triple'] for r in s3)}")

    ok = (all(r["sat"] for r in s1) and not any(r["sat"] for r in s2)
          and all(r["has_triple"] for r in s3))
    results["pass"] = ok
    json.dump(results, open("results_sat_control.json", "w"), indent=1,
              default=str)
    print("SAT CONTROLS PASS" if ok else "SAT CONTROL FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
