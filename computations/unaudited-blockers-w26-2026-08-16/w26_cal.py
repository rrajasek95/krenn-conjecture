#!/usr/bin/env python3
"""W26 -- CALIBRATION on the adversarial battery.  UNAUDITED.  Exact only.

The three constructed points (adv lane):
  P1  m=25  Case-2b clean point, OFF the vanishing stratum
  P2  m=26  (1,6)- and (2,6)-solo families SURVIVE (constant ratio 2)
  P3  m=27  same
On all three the FULL residual degree-<=1 system is INCONSISTENT
(rank = #unknowns + 1).  This file extracts, exactly, a FARKAS CERTIFICATE
for that inconsistency: a set of rows and rational multipliers lambda with
  sum lambda_r * (coefficient row_r) = 0    and    sum lambda_r * (-Phi_r) != 0.
The certificate's SUPPORT is the word family that breaks consistency; the
point of the calibration is to read off its structure and then prove such a
family always exists.

Incremental elimination keeps at most (#unknowns + 1) pivot rows, each
carrying its provenance as a rational combination of ORIGINAL rows, so the
certificate is produced directly and is small.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_sub as SB                                              # noqa: E402

ADV = os.path.join(HERE, "adv")


def load_pt(path, *keys):
    d = json.load(open(path))
    for k in keys:
        d = d[k]
    return {tuple(int(t) for t in k.strip("()").split(",")):
            [[Fraction(x) for x in row] for row in v] for k, v in d.items()}


def rows_of(m, bl):
    """the full residual system: [(word, coeffvector, const)]."""
    return C.residual_rows(m, bl)


def farkas(cells, rows):
    """returns (certificate, pivots) -- certificate = [(row_index, lambda)]
    with sum lambda * coeff = 0 and sum lambda * (-const) != 0, or None."""
    n = len(cells)
    basis = []                       # (pivotcol, augrow, provenance dict)
    for ri, (w, v, c) in enumerate(rows):
        cur = [Fraction(x) for x in v] + [Fraction(-c)]
        prov = {ri: Fraction(1)}
        for pc, brow, bprov in basis:
            if cur[pc] != 0:
                f = cur[pc] / brow[pc]
                cur = [a - f * b for a, b in zip(cur, brow)]
                for k2, val in bprov.items():
                    prov[k2] = prov.get(k2, Fraction(0)) - f * val
        piv = next((j for j in range(n + 1) if cur[j] != 0), None)
        if piv is None:
            continue
        if piv == n:                                    # 0 ... 0 | nonzero
            return [(k2, val) for k2, val in prov.items() if val != 0], basis
        basis.append((piv, cur, prov))
    return None, basis


def describe(m, rows, cert):
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    out = []
    for ri, lam in cert:
        w, v, c = rows[ri]
        act = tuple(f for f in lv
                    if w[f[0]] == sing[f][0] and w[f[1]] == sing[f][1])
        out.append(dict(word=list(w), lam=str(lam),
                        active=[str(e) for e in act],
                        const_Phi=str(c),
                        nz_coeffs=[str(C.live_singles(m)[i])
                                   for i in range(len(v)) if v[i] != 0]))
    return out


def main():
    OUT = {"_header": "UNAUDITED W26 calibration: Farkas certificates on "
                      "the adversarial battery."}
    battery = [
        ("P1_m25_case2b", 25,
         os.path.join(ADV, "results_case2b.json"), ("main", "point")),
        ("P2_m26_solo", 26,
         os.path.join(ADV, "results_solo.json"), ("m26", "point")),
        ("P3_m27_solo", 27,
         os.path.join(ADV, "results_solo.json"), ("m27", "point")),
    ]
    for name, m, path, keys in battery:
        if not os.path.exists(path):
            print("MISSING", path)
            continue
        bl = load_pt(path, *keys)
        gs = set(C.gamma_edges(C.TEMPLATES[m]))
        allnz = all(bl[e][i][j] != 0 for e in gs
                    for i in range(3) for j in range(3))
        clean = all(C.phi(bl, gs, w) == 0 for w in C.clean_words(m))
        van = all(C.phi(bl, gs, w) == 0 for w in C.WORDS)
        cells, rows = rows_of(m, bl)
        cert, basis = farkas(cells, rows)
        rec = dict(m=m, all_cells_nonzero=allnz, is_clean=clean,
                   vanishing_stratum=van, n_unknowns=len(cells),
                   n_rows=len(rows), rank_A_aug=len(basis) + (1 if cert else 0),
                   inconsistent=bool(cert))
        print("=" * 74)
        print("%s  m=%d  allnz=%s clean=%s vanishing=%s  unknowns=%d rows=%d"
              % (name, m, allnz, clean, van, len(cells), len(rows)))
        if cert:
            desc = describe(m, rows, cert)
            rec["certificate_size"] = len(cert)
            rec["certificate"] = desc
            # exact re-verification of the certificate
            n = len(cells)
            chk = [Fraction(0)] * n
            rhs = Fraction(0)
            for ri, lam in cert:
                w, v, c = rows[ri]
                for j in range(n):
                    chk[j] += lam * v[j]
                rhs += lam * (-c)
            rec["cert_coeff_sum_zero"] = all(z == 0 for z in chk)
            rec["cert_const_sum"] = str(rhs)
            print("  FARKAS CERTIFICATE: %d rows;  sum lam*coeff = 0 : %s ;"
                  "  sum lam*(-Phi) = %s" % (len(cert),
                                             all(z == 0 for z in chk), rhs))
            for d in desc:
                print("    lam=%-10s word=%s  active=%s  Phi=%s"
                      % (d["lam"], d["word"], d["active"], d["const_Phi"]))
        else:
            print("  CONSISTENT (no Farkas certificate) -- rank %d" % len(basis))
        # solo survivors, for the record
        rec["solo"] = {str(e): SB.solo_report(m, bl, e)
                       for e in C.live_singles(m)}
        rec["solo_survivors"] = [k for k, v in rec["solo"].items()
                                 if v["survives"]]
        print("  solo survivors:", rec["solo_survivors"])
        OUT[name] = rec
        json.dump(OUT, open(os.path.join(HERE, "results_cal.json"), "w"),
                  indent=1, default=str)
    print("wrote results_cal.json")


if __name__ == "__main__":
    main()
