#!/usr/bin/env python3
"""Exact A=B component parametrization and compact-unit localizer faces."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_left_slices_export_mate.py"
BUILDER_PATH = HERE / "build_left_generic_slice.py"
OUT = HERE / "results_AB_component_localizer_faces.json"
COFACTOR_LOCALIZERS = (1, 2, 6, 10, 14, 18, 21, 22)
Q_LOCALIZERS = (15, 3, 10, 9)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("generic_cycle_face_audit", AUDIT_PATH)
BUILDER = load("generic_cycle_face_builder", BUILDER_PATH)
CORE = AUDIT.CORE


def raw_to_sympy(poly, entries):
    answer = sp.Integer(0)
    for monomial, coefficient in poly.items():
        term = sp.Rational(coefficient)
        for index in monomial:
            term *= entries[index]
        answer += term
    return sp.cancel(answer)


def reduce_r(expression, r, s, t):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    numerator = sp.Poly(numerator, r, domain=sp.QQ.frac_field(s, t)).rem(
        sp.Poly(r*r+2*r-1, r, domain=sp.QQ.frac_field(s, t))).as_expr()
    denominator = sp.Poly(denominator, r, domain=sp.QQ.frac_field(s, t)).rem(
        sp.Poly(r*r+2*r-1, r, domain=sp.QQ.frac_field(s, t))).as_expr()
    return sp.cancel(numerator/denominator)


def normalized_factor(expression, s, t):
    root2 = sp.sqrt(2)
    expression = sp.factor(expression, extension=root2)
    poly = sp.Poly(sp.expand(expression), s, t, extension=root2)
    return str(poly.monic().as_expr())


def irreducible_factors(expression, r, s, t):
    numerator = sp.cancel(expression).as_numer_denom()[0]
    specialized = sp.factor(numerator.subs(r, -1+sp.sqrt(2)),
                            extension=sp.sqrt(2))
    _, factors = sp.factor_list(specialized, s, t, extension=sp.sqrt(2))
    return tuple((normalized_factor(factor, s, t), multiplicity)
                 for factor, multiplicity in factors)


def cell_action(index, permutation, flips):
    edge_index, cell = divmod(index, 4)
    i, j = CORE.SUPER_EDGES[edge_index]
    a, b = divmod(cell, 2)
    ni, nj = permutation[i], permutation[j]
    na, nb = a ^ flips[i], b ^ flips[j]
    if ni > nj:
        ni, nj, na, nb = nj, ni, nb, na
    return 4*CORE.EDGE_INDEX[(ni, nj)] + 2*na + nb


def q_action(index, permutation, flips):
    old = tuple((index >> (3-site)) & 1 for site in range(4))
    new = [0]*4
    for site in range(4):
        new[permutation[site]] = old[site] ^ flips[site]
    return sum(bit << (3-site) for site, bit in enumerate(new))


def main():
    variables, generators, _, live = BUILDER.derive()
    b0, b1, b3, d1, d3, d4, z = variables
    r, s, t = sp.symbols("r s t")
    substitution = {
        b0: s,
        d1: r,
        d3: s,
        d4: -r*s,
        b3: t,
        b1: t*s*(r+2)-r-s-2,
    }
    live_param = reduce_r(live.subs(substitution), r, s, t)
    full_substitution = {**substitution, z: 1/live_param}
    source_remainders = [reduce_r(row.subs(full_substitution), r, s, t)
                         for row in generators]
    if any(remainder != 0 for remainder in source_remainders):
        raise RuntimeError("exact A=B component parametrization failed")

    parameters, entries = AUDIT.raw_left_expressions()
    if tuple(parameters) != tuple(variables[:-1]):
        raise RuntimeError("left parameter order changed")
    raw_h = CORE.pure_hafnian()
    raw_cofactors = tuple(AUDIT.PROBE.derivative(raw_h, index)
                          for index in range(24))
    raw_q = tuple(CORE.q_orientation(tuple(
        (index >> (3-site)) & 1 for site in range(4))) for index in range(16))
    covariants = {}
    for index in COFACTOR_LOCALIZERS:
        value = raw_to_sympy(raw_cofactors[index], entries)
        covariants[f"C{index}"] = reduce_r(value.subs(substitution), r, s, t)
    for index in Q_LOCALIZERS:
        value = raw_to_sympy(raw_q[index], entries)
        covariants[f"Q{index}"] = reduce_r(value.subs(substitution), r, s, t)

    # Original chart factors are units and hence cannot define new faces.
    chart_factors = {
        "b0": b0, "b1": b1, "b3": b3, "d1": d1, "d3": d3, "d4": d4,
        "Delta": b1*d3+b3*d1*d4,
        "D0": d1*d4+d3,
        "Bplus": b1+d1,
    }
    chart_factorization = {
        name: irreducible_factors(reduce_r(value.subs(substitution), r, s, t),
                                  r, s, t)
        for name, value in chart_factors.items()
    }
    chart_units = {factor for factors in chart_factorization.values()
                   for factor, _ in factors}
    records = {}
    face_to_localizers = {}
    for name, value in covariants.items():
        factors = irreducible_factors(value, r, s, t)
        nonunit_factors = tuple((factor, multiplicity)
                                for factor, multiplicity in factors
                                if factor not in chart_units)
        records[name] = {
            "expression": str(sp.factor(value)),
            "factors_over_Qsqrt2": [
                {"factor": factor, "multiplicity": multiplicity,
                 "chart_unit": factor in chart_units}
                for factor, multiplicity in factors
            ],
            "nonunit_face_factors": [factor for factor, _ in nonunit_factors],
        }
        for factor, _ in nonunit_factors:
            face_to_localizers.setdefault(factor, []).append(name)

    # Stabilizer of the generic full joint incidence signature.
    generic = json.loads((HERE /
        "results_generic_cycle_left_slices_mate_export.json").read_text())["records"][0]
    entry_support = frozenset(generic["entry_support"])
    cofactor_support = frozenset(generic["cofactor_support"])
    q_support = frozenset(generic["Q_support"])
    stabilizer = []
    for permutation in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            if ({cell_action(index, permutation, flips) for index in entry_support}
                    == entry_support and
                {cell_action(index, permutation, flips) for index in cofactor_support}
                    == cofactor_support and
                {q_action(index, permutation, flips) for index in q_support}
                    == q_support):
                stabilizer.append((permutation, flips))
    localizer_labels = set(records)
    label_orbits = []
    unseen = set(localizer_labels)
    while unseen:
        seed = min(unseen)
        family, index = seed[0], int(seed[1:])
        orbit = set()
        for permutation, flips in stabilizer:
            transformed = (cell_action(index, permutation, flips)
                           if family == "C" else
                           q_action(index, permutation, flips))
            label = family+str(transformed)
            if label in localizer_labels:
                orbit.add(label)
        # The restricted label set need not be invariant; retain only verified
        # images and never infer an unlisted factor.
        orbit.add(seed)
        label_orbits.append(sorted(orbit))
        unseen -= orbit

    result = {
        "status": "UNAUDITED exact A=B component/localizer face ledger PASS",
        "component_parametrization": {
            "minimal_polynomial": "r^2+2*r-1",
            "parameters": ["s", "t"],
            "map": {str(key): str(value) for key, value in substitution.items()},
            "live_product": str(sp.factor(live_param)),
            "all_source_rows_replay": True,
        },
        "antecedent_localizers": list(covariants),
        "deduplicated_chart_relations": {
            "Q15": "chart unit D0 (normal form -2*d4)",
            "Q9_equals_Q10": sp.cancel(covariants["Q9"]-covariants["Q10"]) == 0,
        },
        "chart_factorization": chart_factorization,
        "localizer_records": records,
        "minimal_face_antichain": [
            {"factor": factor, "localizers": sorted(labels)}
            for factor, labels in sorted(face_to_localizers.items())
        ],
        "component_signature_stabilizer_size": len(stabilizer),
        "restricted_localizer_label_orbits": sorted(label_orbits),
        "scope": (
            "Exact factor ledger in the irreducible component field "
            "Q(s,t)[r]/(r^2+2r-1), with the original nine chart factors "
            "removed as units. Stabilizer orbits use the complete generic "
            "entry/cofactor/Q incidence signature and do not assert that an "
            "unlisted source equation is transported within the same gauge."
        ),
        "source_hashes": {
            "audit": sha256(AUDIT_PATH.read_bytes()).hexdigest(),
            "builder": sha256(BUILDER_PATH.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("A=B component localizer face ledger PASS")
    print("stabilizer", len(stabilizer), "faces", len(face_to_localizers))
    for face, labels in sorted(face_to_localizers.items()):
        print(labels, face)
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
