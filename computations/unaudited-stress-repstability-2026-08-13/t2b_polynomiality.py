#!/usr/bin/env python3
"""T2b: polynomiality in h of every scalar the construction produces.

Two families are fitted and then *verified* beyond the fitting range:

  (1) the association-scheme eigenvalue of the two-switch adjacency A_h on
      each padded shape [2h-2|mu|, 2mu]  (data from t1_matching_scheme*.json),
  (2) the fibre constants of the flattened transfer row and the value of the
      composite projector Pi_end Pi_match k_f.

For (2) a reduced ordered-pair model is used: after the matching projector
the row is a function of the ordered endpoints only -- verified exactly
against the true transfer row at h=3,4,5 by t2_transfer_residuals.py -- so
B_h acts as the ordered-pair endpoint operator on 2h+2 sites and the whole
composite is computable for every h up to ~20.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import difference_table, fit_polynomial, poly_str  # noqa: E402

HERE = Path(__file__).resolve().parent


# ------------------------------------------------------------------ model

def flat_row_values(h):
    """(A_h - lambda_h) k_f on the ordered-pair module, from the note's (13)-(15)."""
    n = 2 * h + 2
    marked_p, marked_s = 0, 1
    marked_matching = [(2 * i, 2 * i + 1) for i in range(1, h + 1)]
    values = {}
    for p in range(n):
        for s in range(n):
            if p == s:
                continue
            q = sum(int(p not in e and s not in e) for e in marked_matching)
            if (p, s) == (marked_p, marked_s):
                c = 4 * h * h + 4 * h
            elif p == marked_p or s == marked_s:
                c = 2 * h - 1
            else:
                c = 0
            values[(p, s)] = Q(q + (2 * h - 1) * c)
    return values


def endpoint_apply(values, n):
    out = {}
    for (p, s) in values:
        total = Q(0)
        for t in range(n):
            if t in (p, s):
                continue
            total += values[(t, s)] + values[(p, t)]
        out[(p, s)] = total
    return out


def composite_constant(h):
    n = 2 * h + 2
    current = flat_row_values(h)
    for theta in (-2, 2 * h - 2, 2 * h):
        image = endpoint_apply(current, n)
        current = {k: image[k] - theta * current[k] for k in current}
    distinct = set(current.values())
    assert len(distinct) == 1, ("composite projector not constant", h, len(distinct))
    return distinct.pop()


def fibre_constant_families(h):
    """The distinct flattened fibre constants, keyed by fibre type."""
    values = flat_row_values(h)
    marked_matching = [(2 * i, 2 * i + 1) for i in range(1, h + 1)]
    def tag(p, s):
        code = lambda v: "pf" if v == 0 else ("sf" if v == 1 else "r")
        t = (code(p), code(s))
        if t == ("r", "r"):
            return t + ("mates" if any(p in e and s in e
                                       for e in marked_matching) else "apart",)
        return t
    out = {}
    for (p, s), value in values.items():
        key = str(tag(p, s))
        out.setdefault(key, set()).add(value)
    assert all(len(v) == 1 for v in out.values())
    return {k: next(iter(v)) for k, v in out.items()}


# ------------------------------------------------------------------- fits

def fit_and_verify(name, data, fit_range, check_range):
    """data: {h: value}.  Fit on fit_range, verify exactly on check_range."""
    points = [(h, data[h]) for h in fit_range]
    coeffs = fit_polynomial(points)
    ok = True
    failures = []
    for h in check_range:
        if h not in data:
            continue
        predicted = sum(c * Q(h) ** k for k, c in enumerate(coeffs))
        if predicted != data[h]:
            ok = False
            failures.append((h, str(predicted), str(data[h])))
    diffs = difference_table([data[h] for h in sorted(data)])
    terminating = any(all(v == 0 for v in row) for row in diffs)
    print(f"  {name:<34} {poly_str(coeffs):<40} "
          f"verified={ok} on {list(check_range)}"
          + (f" FAILURES={failures}" if failures else ""))
    return {
        "name": name,
        "data": {str(h): str(v) for h, v in sorted(data.items())},
        "fitted_on": list(fit_range),
        "coefficients": [str(c) for c in coeffs],
        "polynomial": poly_str(coeffs),
        "verified_on": [h for h in check_range if h in data],
        "verified": ok,
        "failures": failures,
        "difference_table_terminates": terminating,
        "difference_table": [[str(v) for v in row] for row in diffs],
    }


def main():
    out = {}

    # ---- (1) A_h eigenvalues per padded shape
    tables = {}
    for path in [HERE / "t1_matching_scheme.json", HERE / "t1_matching_scheme_h7.json"]:
        if path.exists():
            for h, record in json.loads(path.read_text()).items():
                tables[int(h)] = record
    families = {}
    for h, record in tables.items():
        for row in record["eigen_table"]:
            shape = row["shape_2lam"]
            if shape is None:
                continue
            mu = tuple(shape[1:])
            if shape[0] != 2 * h - sum(mu):
                continue          # not in padded range at this h
            families.setdefault(mu, {})[h] = Q(row["A_eigenvalue"])
    print("A_h eigenvalue per padded shape [2h-|2mu|, 2mu]:")
    fits = []
    for mu in sorted(families, key=lambda m: (sum(m), m)):
        data = families[mu]
        if len(data) < 3:
            print(f"  mu={list(mu)}: only {sorted(data)} -- too few orders to fit")
            continue
        hs = sorted(data)
        fits.append(fit_and_verify(f"shape [2h-{sum(mu)*1}|mu={list(mu)}]",
                                   data, hs[:3], hs[3:]))
    out["A_eigenvalue_families"] = fits

    # ---- (2) transfer constants
    print("\nflattened transfer fibre constants (reduced ordered-pair model):")
    fibre_data = {}
    for h in range(3, 15):
        for key, value in fibre_constant_families(h).items():
            fibre_data.setdefault(key, {})[h] = value
    fibre_fits = []
    for key in sorted(fibre_data):
        data = fibre_data[key]
        fibre_fits.append(fit_and_verify(key, data, range(3, 7), range(7, 15)))
    out["fibre_constants"] = fibre_fits

    print("\ncomposite projector constant Pi_end Pi_match k_f:")
    comp = {h: composite_constant(h) for h in range(3, 13)}
    out["composite_constant"] = fit_and_verify(
        "Pi_end Pi_match k_f", comp, range(3, 10), range(10, 13))

    # the marked mass, for contrast: NOT polynomial
    from lib_stress import occurrence_count
    mass = {h: Q((2 * h - 1) * 7 * h * occurrence_count(h)) for h in range(3, 13)}
    out["marked_mass"] = fit_and_verify(
        "(2h-1)R_h  [normalisation]", mass, range(3, 10), range(10, 13))

    path = HERE / "t2b_polynomiality.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True))
    print("wrote", path)


if __name__ == "__main__":
    main()
