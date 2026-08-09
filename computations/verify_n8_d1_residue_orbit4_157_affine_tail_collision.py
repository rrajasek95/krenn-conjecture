#!/usr/bin/env python3
"""Generic affine-tail unit and the next 157-cell O4 closure."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import importlib
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED = {
    "verify_n8_d1_residue_orbit4_four_star_lemma.py":
        "cffd8ac0c5d54fddd365e4a610f2bed00881683a61733669e2bb41af972ecad1",
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py":
        "290195e979282bee0029a4cf02012b79ecba2212bf87daacb2710ff9cf6edf63",
    "verify_n8_d1_residue_orbit4_158_second_layer_collision.py":
        "5c47e1e72874afcc70ae7e4646e9f20acb2ba3a51a6b36c9451cc24ed1a0c4fa",
    "verify_n8_d1_residue_orbit4_158_character_graph_batch2.py":
        "e31e396c8441bcf08f4bd0f91f8a690fd9315a7c415d1788a8a1c5631b061405",
    "verify_n8_d1_residue_orbit4_157_affine_homogeneous_unit.py":
        "ee551156c49e4d3939f5a60647f989f491a7896325c9c4d2a220b5143521aba0",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned affine-tail source changed: " + filename)

F = importlib.import_module(
    "verify_n8_d1_residue_orbit4_four_star_lemma"
)
E = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent"
)
X = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_second_layer_collision"
)
H = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_character_graph_batch2"
)
AH = importlib.import_module(
    "verify_n8_d1_residue_orbit4_157_affine_homogeneous_unit"
)
S, C, D, V, O = F.S, F.C, F.D, F.V, F.O

MISSING = frozenset({
    (0, 1, 1, 0), (0, 2, 1, 0), (0, 3, 0, 1),
    (0, 4, 0, 1), (0, 4, 1, 0), (0, 5, 0, 1), (0, 5, 1, 0),
    (0, 6, 0, 1), (0, 6, 0, 2),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1), (1, 3, 1, 0), (1, 3, 1, 2),
    (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 7, 0, 1), (1, 7, 1, 0),
    (2, 6, 1, 0), (2, 6, 2, 0),
    (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
    (2, 7, 2, 0), (2, 7, 2, 1),
    (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
    (3, 6, 2, 0), (3, 6, 2, 1),
})
GENERATOR_SHA256 = (
    "2541cf4aa31003a53496be25826d7be1089f10c9039ff14fbfd178aef930177f"
)
SELECTED_AFFINE_RECORD = 2475
SELECTED_HOMOGENEOUS_RECORD = 2474
REPAIR_CELLS = frozenset({
    (0, 1, 1, 0), (0, 4, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1), (1, 6, 0, 0), (1, 6, 0, 1), (1, 7, 0, 1),
    (2, 6, 1, 0), (2, 7, 1, 1),
})
EXPECTED_COLLISION_SHA256 = (
    "31e9b9ee4e85356b5016e6ae22434baaf5a02d2af59752770bc4f526beb22cc8"
)
EXPECTED_LEDGER_SHA256 = (
    "a3b5bfe09405a21f20c00ba2605f175d69af49531579c3ebbc5e0190e15e1533"
)


def allowed_support():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(O.RESIDUE_HOLES)
               - set(S.BOUNDARY_OMISSIONS))
    require(len(allowed) == 193, "the O4 downset universe changed")
    return frozenset(allowed)


def initial_rows(records):
    """Normalize every distinct raw binomial as x^difference=constant."""
    rows = []
    seen = set()
    for record_index, record in enumerate(records):
        if len(record["terms"]) != 2:
            continue
        parsed = [(tuple(monomial), Fraction(coefficient))
                  for monomial, coefficient in record["terms"]]
        (first, first_coefficient), (second, second_coefficient) = parsed
        difference = E.L.exponent_difference(first, second)
        constant = -second_coefficient / first_coefficient
        key = E.canonical_row(difference, constant)
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "difference": difference,
            "constant": constant,
            "source_record": record_index,
            "divisor": tuple(second),
            "leading_coefficient": first_coefficient,
        })
    return rows


def base_relations(records, rows):
    relations = []
    for row in rows:
        difference = tuple(sorted(
            (name, exponent.numerator)
            for name, exponent in row["difference"].items()
        ))
        divisor = tuple(sorted(Counter(row["divisor"]).items()))
        certificate = {
            row["source_record"]: E.laurent_monomial(
                E.exponent_scale(divisor, -1),
                Fraction(1, row["leading_coefficient"]),
            )
        }
        expected = E.laurent_add(
            E.laurent_monomial(difference),
            E.laurent_monomial((), -row["constant"]),
        )
        require(E.evaluate_certificate(certificate, records) == expected,
                "an initial binomial failed source normalization")
        relations.append({
            "difference": difference,
            "constant": row["constant"],
            "certificate": certificate,
        })
    return relations


def normalized_laurent_shape(polynomial):
    """Canonicalize a nonzero Laurent polynomial up to shift and scalar."""
    require(polynomial, "the zero polynomial has no Laurent shape")
    base, coefficient = sorted(polynomial.items())[0]
    return tuple(sorted((
        E.exponent_add(monomial, E.exponent_scale(base, -1)),
        value / coefficient,
    ) for monomial, value in polynomial.items()))


def affine_tail_collisions(residuals):
    """Find f=c*m+tail and g with tail=scalar*shift*g.

    Every returned row is a Laurent unit consequence f-scalar*shift*g=c*m.
    This is a generic signed-group-algebra alternative to one-class rows,
    inconsistent characters, and parallel two-class collisions.
    """
    shape_rows = defaultdict(list)
    for record_index, polynomial in sorted(residuals.items()):
        shape_rows[normalized_laurent_shape(polynomial)].append(record_index)
    collisions = []
    for affine_index, polynomial in sorted(residuals.items()):
        if len(polynomial) < 2:
            continue
        for omitted, omitted_coefficient in sorted(polynomial.items()):
            tail = dict(polynomial)
            tail.pop(omitted)
            for homogeneous_index in shape_rows.get(
                    normalized_laurent_shape(tail), ()):
                homogeneous = residuals[homogeneous_index]
                tail_base, tail_coefficient = sorted(tail.items())[0]
                source_base, source_coefficient = sorted(
                    homogeneous.items()
                )[0]
                shift = E.exponent_add(
                    tail_base, E.exponent_scale(source_base, -1)
                )
                scale = tail_coefficient / source_coefficient
                multiplier = E.laurent_monomial(shift, scale)
                require(E.laurent_mul(homogeneous, multiplier) == tail,
                        "a normalized affine tail failed exact alignment")
                collisions.append({
                    "affine_record": affine_index,
                    "homogeneous_record": homogeneous_index,
                    "affine_classes": len(polynomial),
                    "homogeneous_classes": len(homogeneous),
                    "omitted_monomial": omitted,
                    "omitted_coefficient": omitted_coefficient,
                    "aligning_shift": shift,
                    "aligning_scale": scale,
                })
    return collisions


def collision_trace(collisions):
    return [{
        "affine_record": row["affine_record"],
        "homogeneous_record": row["homogeneous_record"],
        "classes": [row["affine_classes"], row["homogeneous_classes"]],
        "omitted": E.polynomial_trace(E.laurent_monomial(
            row["omitted_monomial"], row["omitted_coefficient"]
        )),
        "aligning_multiplier": E.polynomial_trace(E.laurent_monomial(
            row["aligning_shift"], row["aligning_scale"]
        )),
    } for row in collisions]


def certificate_input():
    support = allowed_support() - MISSING
    records = C.coefficient_generators(support)
    require(len(support) == 157 and len(records) == 4321
            and D.content_hash(records) == GENERATOR_SHA256,
            "the next O4 affine-tail coefficient input changed")
    rows = initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 55 and len(basis) == 21
            and len(dependencies) == 34
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the next O4 initial signed character changed")
    characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_row, representation) in basis.items()
    }
    residuals = {}
    reductions = {}
    histogram = Counter()
    for record_index, record in enumerate(records):
        reduced, traces, parents = E.reduce_record(record, basis, characters)
        histogram[len(reduced)] += 1
        if reduced:
            residuals[record_index] = reduced
            reductions[record_index] = (traces, parents)
    require(not histogram[1], "the affine-tail face already has a one-class unit")
    collisions = affine_tail_collisions(residuals)
    trace = collision_trace(collisions)
    require(len(collisions) == 36
            and all(row["affine_classes"] == 3
                    and row["homogeneous_classes"] == 2
                    for row in collisions),
            "the exact affine-tail collision census changed")
    if EXPECTED_COLLISION_SHA256 != "TO_BE_FROZEN":
        require(D.content_hash(trace) == EXPECTED_COLLISION_SHA256,
                "the exact affine-tail collision ledger changed")
    selected = collisions[0]
    require((selected["affine_record"], selected["homogeneous_record"])
            == (SELECTED_AFFINE_RECORD, SELECTED_HOMOGENEOUS_RECORD),
            "the selected affine-tail collision changed")
    relations = base_relations(records, rows)
    certificates = {}
    for record_index in (SELECTED_AFFINE_RECORD,
                         SELECTED_HOMOGENEOUS_RECORD):
        traces, _parents = reductions[record_index]
        certificates[record_index] = X.reduced_certificate(
            records, rows, basis, relations,
            record_index, residuals[record_index], traces,
        )
    multiplier = E.laurent_monomial(
        selected["aligning_shift"], selected["aligning_scale"]
    )
    certificate = E.certificate_add(
        certificates[SELECTED_AFFINE_RECORD],
        E.certificate_mul(
            certificates[SELECTED_HOMOGENEOUS_RECORD], multiplier
        ), -1,
    )
    target = E.laurent_monomial(
        selected["omitted_monomial"], selected["omitted_coefficient"]
    )
    require(E.evaluate_certificate(certificate, records) == target,
            "the selected affine-tail Laurent unit failed")
    ordinary = X.clear_to_saturation(certificate, target, support, records)
    require(ordinary == {
        "source_records": [2474, 2475, 3065, 3066,
                           3068, 3069, 3094, 3097],
        "laurent_cofactor_terms": 18,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_06_10", 1], ["x_13_22", 1],
            ["x_46_00", 1], ["x_47_02", 1], ["x_56_10", 1],
            ["x_57_22", 2],
        ],
        "ordinary_saturation_power": 2,
        "ordinary_cofactor_terms": 18,
        "ordinary_certificate_sha256":
            "1b62944c9ae68c40d81b1ceb5a479f73b5a7f2b39a903d217a1297fbfcd17575",
        "integral_coefficients": True,
    }, "the selected affine-tail ordinary U^2 identity changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    repair_masks = H.minimal_repair_masks(
        records, ordinary["source_records"], support
    )
    require(repair_masks == frozenset(
                frozenset((cell,)) for cell in REPAIR_CELLS
            ), "the affine-tail singleton repair chart changed")
    transported = AH.transported_clauses(REPAIR_CELLS, set(witnesses))
    require(len(transported) == 8
            and all(row["transport_multiplicity"] == 1
                    for row in transported),
            "the affine-tail D1 transport orbit changed")
    return {
        "support": support,
        "records": records,
        "rows": rows,
        "basis": basis,
        "dependencies": dependencies,
        "histogram": histogram,
        "residuals": residuals,
        "collisions": collisions,
        "collision_trace": trace,
        "selected": selected,
        "laurent_certificate_sha256": D.content_hash(
            E.certificate_trace(certificate)
        ),
        "ordinary": ordinary,
        "witnesses": witnesses,
        "repair_masks": repair_masks,
        "transported": transported,
    }


def transported_clause_audit():
    return certificate_input()["transported"]


def audit():
    started = monotonic()
    data = certificate_input()
    ledger = {
        "pinned_sources": PINNED,
        "frontier_missing_cells": [list(cell) for cell in sorted(MISSING)],
        "localized_cells": len(data["support"]),
        "complete_shadow": C.support_shadow_audit(data["support"]),
        "coefficient_generators": len(data["records"]),
        "generator_sha256": GENERATOR_SHA256,
        "initial_character": {
            "rows": len(data["rows"]), "rank": len(data["basis"]),
            "dependencies": len(data["dependencies"]),
            "inconsistent_dependencies": 0,
        },
        "residual_histogram": {
            str(size): count for size, count
            in sorted(data["histogram"].items())
        },
        "generic_affine_tail_oracle": {
            "collisions": len(data["collisions"]),
            "collision_sha256": D.content_hash(data["collision_trace"]),
            "class_pairs": [[3, 2]],
            "criterion": (
                "if f=c*m+S and g is a nonzero Laurent shift/scalar of S, "
                "then f-shift*g=c*m is a torus unit"
            ),
        },
        "selected_collision": {
            "affine_record": SELECTED_AFFINE_RECORD,
            "homogeneous_record": SELECTED_HOMOGENEOUS_RECORD,
            "omitted_unit": E.polynomial_trace(E.laurent_monomial(
                data["selected"]["omitted_monomial"],
                data["selected"]["omitted_coefficient"],
            )),
            "aligning_multiplier": E.polynomial_trace(E.laurent_monomial(
                data["selected"]["aligning_shift"],
                data["selected"]["aligning_scale"],
            )),
            "laurent_certificate_sha256":
                data["laurent_certificate_sha256"],
        },
        "ordinary_saturation_certificate": data["ordinary"],
        "localized_source_witnesses": [list(cell)
                                       for cell in data["witnesses"]],
        "minimal_repair_masks": [
            [list(cell) for cell in sorted(mask)]
            for mask in sorted(data["repair_masks"], key=repr)
        ],
        "distinct_transported_clauses": data["transported"],
        "characteristic_scope": "all characteristics",
        "status": (
            "the replacement 157-cell O4 maximum is empty by a generic "
            "three-class affine tail colliding with a two-class homogeneous "
            "row; the selected source expansion is integral U^2"
        ),
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_COLLISION_SHA256 == "TO_BE_FROZEN":
        print("collision sha256:", ledger[
            "generic_affine_tail_oracle"
        ]["collision_sha256"])
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the next O4 affine-tail ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("initial rank / affine-tail collisions: %d / %d" % (
        ledger["initial_character"]["rank"],
        ledger["generic_affine_tail_oracle"]["collisions"],
    ))
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
