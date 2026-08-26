#!/usr/bin/env python3
"""Exact polynomial ideal certificate for the arbitrary cycle-block family."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT_DIR = HERE.parent / "unaudited-codex-n8-x5-cycle-residual-ledger-2026-08-25"
PARENT_MANIFEST = PARENT_DIR / "MANIFEST.sha256"
PARENT_MANIFEST_SHA256 = "a8de425bbe54221874b4c75cb45b8dd4a465f628c881536d2e4d785a9afe4ab1"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT_MANIFEST) == PARENT_MANIFEST_SHA256
assert sha256(CORE) == CORE_SHA256
spec = importlib.util.spec_from_file_location("x5_core", CORE)
assert spec is not None and spec.loader is not None
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


# Sparse integral polynomial ring.  A monomial is a sorted tuple of variable
# names; repetition represents exponent.
def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def constant(value):
    return {} if value == 0 else {(): value}


def variable(name):
    return {(name,): 1}


def add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
    return clean(answer)


def negate(poly):
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def subtract(left, right):
    return add(left, negate(right))


def multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = answer.get(monomial, 0) + left_coefficient * right_coefficient
    return clean(answer)


ONE = constant(1)
ZERO = constant(0)


def poly_string(poly):
    if not poly:
        return "0"
    terms = []
    for monomial, coefficient in sorted(poly.items()):
        factor = "*".join(monomial) if monomial else "1"
        terms.append(f"{coefficient:+d}*{factor}")
    return " ".join(terms).lstrip("+")


def evaluate(poly, assignment):
    total = Fraction(0)
    for monomial, coefficient in poly.items():
        term = Fraction(coefficient)
        for name in monomial:
            term *= assignment[name]
        total += term
    return total


def name(block, left, right):
    return f"{block}{left}{right}"


X = {(a, b): variable(name("X", a, b)) for a in core.COLORS for b in core.COLORS}
Y = {(a, b): variable(name("Y", a, b)) for a in core.COLORS for b in core.COLORS}
U = {(a, b): variable(name("U", a, b)) for a in core.COLORS for b in core.COLORS}
V = {(a, b): variable(name("V", a, b)) for a in core.COLORS for b in core.COLORS}


def factor(left_block, right_block, a, b):
    return add(ONE, multiply(left_block[(a, b)], right_block[(a, b)]))


P = {colour: factor(X, Y, colour, colour) for colour in core.COLORS}
Q = {colour: factor(U, V, colour, colour) for colour in core.COLORS}
PURE = {colour: subtract(multiply(P[colour], Q[colour]), ONE) for colour in core.COLORS}
RESIDUAL = {(a, b): multiply(P[a], Q[b]) for a in core.COLORS for b in core.COLORS if a != b}


def main():
    support_edges = {(0, 3), (1, 6), (2, 7), (4, 5), (0, 4), (1, 2), (3, 5), (6, 7)}
    supported_matchings = [matching for matching in core.PM8 if set(matching) <= support_edges]
    assert supported_matchings == [
        ((0, 3), (1, 2), (4, 5), (6, 7)),
        ((0, 3), (1, 6), (2, 7), (4, 5)),
        ((0, 4), (1, 2), (3, 5), (6, 7)),
        ((0, 4), (1, 6), (2, 7), (3, 5)),
    ]

    # Verify the four-term factorization for every base-sector word.
    factorization_records = []
    for a, b, c, d in itertools.product(core.COLORS, repeat=4):
        left = multiply(X[(a, d)], Y[(a, d)])
        right = multiply(U[(b, c)], V[(b, c)])
        matching_sum = add(add(ONE, left), add(right, multiply(left, right)))
        factored = multiply(add(ONE, left), add(ONE, right))
        assert matching_sum == factored
        factorization_records.append({
            "pair_colours": [a, b, c, d],
            "polynomial_sha256": hashlib.sha256(poly_string(factored).encode()).hexdigest(),
        })
    assert len(factorization_records) == 81

    # Each of the six cross residuals is a unit modulo the three pure-row
    # equations.  This is a literal Bezout certificate, not a Gröbner claim.
    certificates = []
    for (a, b), residual in sorted(RESIDUAL.items()):
        inverse = multiply(Q[a], P[b])
        left = subtract(multiply(residual, inverse), ONE)
        right = add(multiply(PURE[a], multiply(P[b], Q[b])), PURE[b])
        assert left == right
        certificates.append({
            "colours": [a, b],
            "residual": f"R_{a}{b}=P_{a}*Q_{b}",
            "inverse_mod_pure_ideal": f"Q_{a}*P_{b}",
            "certificate": (
                f"R_{a}{b}*(Q_{a}*P_{b})-1 = "
                f"(P_{a}*Q_{a}-1)*(P_{b}*Q_{b}) + (P_{b}*Q_{b}-1)"
            ),
            "identity_sha256": hashlib.sha256(poly_string(left).encode()).hexdigest(),
        })
    assert len(certificates) == 6

    # Exact 257-point rational replay of the diagonal extension.  Offdiagonal
    # values are arbitrary deterministic rationals; diagonal V is solved from
    # pure normalization.
    rational_records = []
    for sample in range(257):
        assignment = {}
        for block in "XYUV":
            for a, b in itertools.product(core.COLORS, repeat=2):
                numerator = (sample + 1) * (1 + a + 3 * b + 5 * ("XYUV".index(block) + 1))
                denominator = 17 + a + 3 * b + 7 * ("XYUV".index(block) + 1)
                assignment[name(block, a, b)] = Fraction(numerator, denominator)
        for colour in core.COLORS:
            p_value = evaluate(P[colour], assignment)
            assert p_value != 0
            u_name = name("U", colour, colour)
            v_name = name("V", colour, colour)
            u_value = assignment[u_name]
            assert u_value != 0
            assignment[v_name] = (Fraction(1, 1) / p_value - 1) / u_value
        assert all(evaluate(PURE[colour], assignment) == 0 for colour in core.COLORS)
        residual_values = {}
        for (a, b), residual in sorted(RESIDUAL.items()):
            value = evaluate(residual, assignment)
            inverse = evaluate(multiply(Q[a], P[b]), assignment)
            assert value != 0 and value * inverse == 1
            residual_values[f"R{a}{b}"] = str(value)

        source = core.base_source()
        for a, b in itertools.product(core.COLORS, repeat=2):
            core.put(source, 0, 4, a, b, assignment[name("X", a, b)])
            core.put(source, 3, 5, a, b, assignment[name("Y", a, b)])
            core.put(source, 1, 2, a, b, assignment[name("U", a, b)])
            core.put(source, 6, 7, a, b, assignment[name("V", a, b)])
        for a, b, c, d in itertools.product(core.COLORS, repeat=4):
            word = (a, b, c, a, d, d, b, c)
            literal = core.amplitude(source, word)
            symbolic = evaluate(multiply(factor(X, Y, a, d), factor(U, V, b, c)), assignment)
            assert literal == symbolic
        assert [core.amplitude(source, (colour,) * 8) for colour in core.COLORS] == [1, 1, 1]
        rational_records.append({"sample": sample, "residuals": residual_values})
    assert len(rational_records) == 257

    # The requested 24-cell guard family fixes diagonal X,Y,U to zero and
    # diagonal V to one, while all 24 offdiagonal entries are arbitrary.  Each
    # cross residual specializes literally to the constant polynomial one.
    offdiagonal_replays = []
    for sample in range(257):
        source = core.base_source()
        for a, b in itertools.permutations(core.COLORS, 2):
            values = {
                "X": Fraction(sample + 1 + a, 19 + b),
                "Y": Fraction(sample + 2 + b, 23 + a),
                "U": Fraction(sample + 3 + a + b, 29 + a),
                "V": Fraction(sample + 4 + 2 * a + b, 31 + b),
            }
            core.put(source, 0, 4, a, b, values["X"])
            core.put(source, 3, 5, a, b, values["Y"])
            core.put(source, 1, 2, a, b, values["U"])
            core.put(source, 6, 7, a, b, values["V"])
        residual_words = []
        for a, b in itertools.permutations(core.COLORS, 2):
            word = (a, b, b, a, a, a, b, b)
            assert core.amplitude_terms(source, word) == [(core.M0, 1)]
            residual_words.append(core.word_string(word))
        assert [core.amplitude(source, (colour,) * 8) for colour in core.COLORS] == [1, 1, 1]
        assert core.outside_response_count(source) == 0
        offdiagonal_replays.append({"sample": sample, "residual_words": residual_words})

    result = {
        "schema": "KRENN_X5_CYCLE_POLYNOMIAL_IDEAL_AUDIT_V1",
        "status": "PASS_RESIDUAL_IDEAL_IS_UNIT_IN_CYCLE_FAMILY",
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "core_sha256": CORE_SHA256,
        "support_family": {
            "fixed_physical_blocks": ["A03=I3", "A16=I3", "A27=I3", "A45=I3"],
            "arbitrary_cycle_blocks": ["X=A04", "Y=A35", "U=A12", "V=A67"],
            "supported_perfect_matchings": [core.matching_string(matching) for matching in supported_matchings],
            "same_source_reciprocity": "automatic by the sealed universal identity",
        },
        "factorization": {
            "word": "w(a,b,c,d)=(a,b,c,a,d,d,b,c)",
            "identity": "Phi(w)=(1+X[a,d]*Y[a,d])*(1+U[b,c]*V[b,c])",
            "words_verified_symbolically": len(factorization_records),
            "records": factorization_records,
        },
        "pure_normalization": {
            "P_t": "1+X[t,t]*Y[t,t]",
            "Q_t": "1+U[t,t]*V[t,t]",
            "equations": ["P_0*Q_0=1", "P_1*Q_1=1", "P_2*Q_2=1"],
        },
        "six_residual_ideal": {
            "residuals": "R_ab=P_a*Q_b for a!=b",
            "certificates": certificates,
            "ideal_in_pure_quotient": "unit ideal",
            "common_zero_over_nonzero_unital_ring": False,
        },
        "rational_replay": {
            "samples": len(rational_records),
            "all_81_literal_amplitudes_per_sample": True,
            "all_pure_rows": [1, 1, 1],
            "all_residual_inverse_certificates": True,
            "records_sha256": hashlib.sha256(json.dumps(rational_records, sort_keys=True).encode()).hexdigest(),
        },
        "arbitrary_24_offdiagonal_guard_family": {
            "variables": 24,
            "diagonal_specialization": "Xtt=Ytt=Utt=0, Vtt=1",
            "six_residual_polynomials": ["1", "1", "1", "1", "1", "1"],
            "pure_rows_automatic": [1, 1, 1],
            "formal_triangle_response_guard_preserved": True,
            "samples_replayed": len(offdiagonal_replays),
            "common_zero": False,
        },
        "scope": {
            "arbitrary_24_cell_saturated_family_proved": True,
            "diagonal_cycle_extension_under_pure_normalization_proved": True,
            "arbitrary_cells_outside_four_cycle_blocks_exhausted": False,
            "active_clean_cap_needed": False,
            "degree_twelve_read": False,
            "broad_cegar": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_cycle_polynomial_ideal.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_cycle_polynomial_ideal.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
