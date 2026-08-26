#!/usr/bin/env python3
"""W16 T3b -- explicit ODD-RELATION CERTIFICATES for the k=2 binomial systems.

Produces, for a site whose binomial system is unsatisfiable, an explicit
integer vector c with   sum_i c_i d_i = 0   and   sum_i c_i ODD, and
verifies it directly.  That certificate is checkable by hand/independently:
multiplying the relations  x^{d_i} = -1  to the powers c_i gives
1 = x^0 = (-1)^{sum c_i} = -1, a contradiction over any field of
characteristic != 2.
"""
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import W8_IMMUNE
from w16_k2lattice import binomials_at_site, _insert

HERE = os.path.dirname(os.path.abspath(__file__))


def certificate(diffs):
    if not diffs:
        return None
    n = len(diffs[0]); k = len(diffs)
    basis = {}
    for i, d in enumerate(diffs):
        row = list(d) + [1] + [1 if j == i else 0 for j in range(k)]
        _insert(basis, row, n + 1)
    best = None
    for c, row in basis.items():
        if c < n:
            continue
        s = row[n]
        if s % 2 == 1:
            best = row[n + 1:]
            break
    if best is None:
        return None
    # verify
    acc = [0] * n
    for i, ci in enumerate(best):
        if ci:
            for j in range(n):
                acc[j] += ci * diffs[i][j]
    ok = all(v == 0 for v in acc) and (sum(best) % 2 == 1)
    return dict(support=[(i, best[i]) for i in range(k) if best[i]],
                n_terms=sum(1 for v in best if v), coeff_sum=sum(best),
                verified=ok)


def main():
    out = {}
    for m in (28, 27, 25):
        for t in range(8):
            _, diffs, tags = binomials_at_site(W8_IMMUNE[m], t)
            cert = certificate(diffs)
            key = "m%d_site%d" % (m, t)
            if cert:
                out[key] = dict(n_binomials=len(diffs),
                                n_terms=cert["n_terms"],
                                coeff_sum=cert["coeff_sum"],
                                verified=cert["verified"],
                                first_terms=cert["support"][:6],
                                example_words=[tags[i] for i, _ in
                                               cert["support"][:3]])
                print("%s: certificate with %d terms, coeff sum %d, "
                      "VERIFIED=%s" % (key, cert["n_terms"],
                                       cert["coeff_sum"], cert["verified"]))
            else:
                out[key] = dict(n_binomials=len(diffs), certificate=None)
                print("%s: NO odd relation" % key)
    # negative control
    print("negative control [[1,-1,0],[0,1,-1]] ->",
          certificate([[1, -1, 0], [0, 1, -1]]), "(must be None)")
    out["negative_control"] = certificate([[1, -1, 0], [0, 1, -1]])
    json.dump(out, open(os.path.join(HERE, "results_k2cert.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
