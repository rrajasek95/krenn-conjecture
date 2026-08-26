#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 2 (Gap B): the higher certificate layers.

For a source, the error ideal is I = <E_w>, generated in degree h.  Its
degree-(h+r) graded piece is S^r * span{E_w}, and span{E_w} = L_h(A) for
generic sources (W13).  So the UNIVERSAL (source-independent) layer is

    J_{h+r}(A) := S^r(V (x) W) * L_h(A) ,    L_h(A) = sum_k s^{h-k} Sigma_k.

m not in J_{h+r}(A)  =>  m can NEVER be a degree-(h+r) blocking certificate
for any source with that A_pq  (universal exclusion).

Representation-theoretic upper bound (Schur + Pieri, proved in REPORT):

    S^r(V(x)W) * Sigma_k  is contained in  (+)_{lambda |- k+r,
                                             lambda_2 + lambda_3 <= r} S_l V (x) S_l W

so the only universal obstructions live in the isotypic components with
lambda_2 + lambda_3 > r.  At r = 1 that is exactly the 3-row components,
i.e. the apolar perp of the DETERMINANT ideal.

This script decides, exactly over Q (Singular), the layers at
  * h = 2 (P2's six-site setting), degrees 3, 4, 5;
  * h = 3 (N = 8), degrees 4, 5;
on W13's strata battery, and compares with P2's measured certificates.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from itertools import combinations_with_replacement, permutations

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)

from w14_core import (COLORS, NCAP, det3, iota, kidx, l_monomials, mono_name,
                      mono_poly, monomial_index, monomials, poly_mul, poly_pow,
                      poly_row, rank3, require, rref_exact, sigma_basis)

VARS = [f"k{n}" for n in range(NCAP)]


# ------------------------------------------------------------------ Singular

def run_singular(script, timeout=1800):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if proc.returncode != 0:
        raise RuntimeError(f"Singular failed: {proc.stderr[:1500]}")
    return proc.stdout


def poly_str(poly):
    parts = []
    for m, c in sorted(poly.items()):
        term = "*".join(VARS[v] for v in m)
        parts.append(f"({c})*{term}" if term else f"({c})")
    return "+".join(parts) if parts else "0"


# --------------------------------------------------------------- generators

def L_generators(h, A):
    """A spanning set of L_h(A) as polynomials (dicts)."""
    s_vec = [A[i][j] for i in COLORS for j in COLORS]
    sp = {(n,): s_vec[n] for n in range(NCAP) if s_vec[n]}
    out = []
    for k in range(2, h + 1):
        spow = poly_pow(sp, h - k)
        for mu, nu in sigma_basis(k):
            poly = dict(iota(k, mu, nu))
            if h - k:
                poly = poly_mul(poly, spow)
            if poly:
                out.append(poly)
    return out


def layer_query(h, A, degrees, label):
    gens = L_generators(h, A)
    lines = [f'ring R=0,({",".join(VARS)}),dp;',
             "ideal I=" + ",".join(poly_str(g) for g in gens) + ";",
             "ideal G=std(I);",
             f'"DIM {label} "+string(dim(G));']
    for d in degrees:
        lines.append(f'"HF {label} {d} "+string(size(kbase(G,{d})));')
        for a, b in l_monomials(d):
            poly = mono_poly(a, b, [A[i][j] for i in COLORS for j in COLORS])
            if not poly:
                continue
            lines.append(f'"MEM {label} {d} {mono_name(a, b)} "'
                         f"+string(reduce({poly_str(poly)},G)==0);")
    return "\n".join(lines)


def parse(out):
    table = {}
    for line in out.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "DIM":
            table.setdefault(f[1], {})["cone_dim"] = int(f[2])
        elif f[0] == "HF":
            table.setdefault(f[1], {}).setdefault("codim", {})[int(f[2])] = int(f[3])
        elif f[0] == "MEM":
            table.setdefault(f[1], {}).setdefault("mem", {}).setdefault(
                int(f[2]), {})[f[3]] = (f[4] == "1")
    return table


# ------------------------------------------------- the determinant criterion

def det_operator_apply(poly, degree):
    """det(d/dK) applied to a polynomial of degree >= 3 (exact)."""
    terms = {}
    for pi in permutations(range(3)):
        inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
        key = tuple(sorted(kidx(i, pi[i]) for i in range(3)))
        terms[key] = terms.get(key, 0) + (-1 if inv % 2 else 1)
    out = {}
    for mono, coeff in poly.items():
        for key, sgn in terms.items():
            rest = list(mono)
            ok = True
            mult = 1
            for v in key:
                if v in rest:
                    # d/dK_v of K_v^e gives e * K_v^{e-1}
                    mult *= rest.count(v)
                    rest.remove(v)
                else:
                    ok = False
                    break
            if ok:
                k = tuple(sorted(rest))
                out[k] = out.get(k, 0) + sgn * coeff * mult
    return {m: c for m, c in out.items() if c}


def det_criterion_table(h, A, degree):
    """{monomial: det(d)m == 0} -- the predicted degree-(h+1) taxonomy."""
    s_vec = [A[i][j] for i in COLORS for j in COLORS]
    out = {}
    for a, b in l_monomials(degree):
        poly = mono_poly(a, b, s_vec)
        if not poly:
            out[mono_name(a, b)] = None
            continue
        out[mono_name(a, b)] = (det_operator_apply(poly, degree) == {})
    return out


# --------------------------------------------------------------- the battery

def battery_from_w13():
    path = (HERE + "/../unaudited-induction-w13-2026-08-15/results_taxonomy.json")
    data = json.load(open(path))
    out = []
    for label, rec in data["h3"].items():
        A = [[int(x) for x in row] for row in rec["A"]]
        out.append((label, A))
    return out


def main():
    t0 = time.time()
    results = {}
    battery = battery_from_w13()

    print("== W14 Task 2: universal certificate layers, exact over Q "
          "(Singular) ==")
    for h, degrees in ((2, (2, 3, 4, 5)), (3, (3, 4, 5))):
        print(f"\n===== h = {h} (N = {2 * h + 2}): layers of degree "
              f"{degrees[1:]} =====")
        ambient = {d: len(monomials(NCAP, d)) for d in degrees}
        print(f"  ambient dims: {ambient}")
        for label, A in battery:
            tag = f"h{h}_" + label.split()[0].replace("(", "").replace(",", "")
            tag = "".join(ch for ch in tag if ch.isalnum() or ch == "_")
            script = layer_query(h, A, degrees, tag)
            try:
                table = parse(run_singular(script))[tag]
            except Exception as exc:                       # noqa: BLE001
                print(f"  {label}: SINGULAR ERROR {exc}")
                continue
            rec = {"A": A, "rank": rank3(A), "det": det3(A),
                   "cone_dim": table.get("cone_dim"),
                   "codim_of_layer": table.get("codim", {}),
                   "mem": table.get("mem", {})}
            # cross-check the det criterion at degree h+1
            pred = det_criterion_table(h, A, h + 1)
            meas = table.get("mem", {}).get(h + 1, {})
            agree = all(pred[m] == meas.get(m) for m in meas if m in pred)
            rec["det_criterion_matches_degree_h+1"] = agree
            rec["det_criterion"] = pred
            results[f"h{h}|{label}"] = rec
            print(f"\n  A_pq: {label}  (rank {rank3(A)}, det {det3(A)})")
            print(f"     codim of S/(ideal) in each degree: "
                  f"{table.get('codim')}   cone dim {table.get('cone_dim')}")
            for d in degrees:
                mem = table.get("mem", {}).get(d, {})
                inn = sorted(m for m, v in mem.items() if v)
                outm = sorted(m for m, v in mem.items() if not v)
                print(f"     degree {d}: IN {len(inn)}/{len(mem)}   "
                      f"EXCLUDED: {', '.join(outm) if outm else '(none)'}")
            print(f"     det(d)m = 0 criterion reproduces degree-{h + 1} "
                  f"table: {agree}")

    with open(HERE + "/results_task2_layers.json", "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    print(f"\nwrote results_task2_layers.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
