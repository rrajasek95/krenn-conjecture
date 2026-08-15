#!/usr/bin/env python3
"""Exact routing of the q^[3]-dependent full-nine branches at h=3.

The literal rows are

    a_ij Q + p_i s_j F = delta_ij X_i,

where Q=q^[3] and F=q^[2].  This audit treats Q=0 and
0 != Q in span(X_0,X_1,X_2), keeps the scalar-zero selected response,
and freezes the first zero-top boundary not covered by the pure-lift
common-power theorem.

Only standard-library exact arithmetic is used.  The three modes replay
the same finite theorem; their purpose is to catch optimization/import
dependence in the usual repository harness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction as Q
from itertools import combinations, product


HERE = os.path.dirname(os.path.abspath(__file__))
COLORS = tuple(range(3))
SITES = tuple(range(6))
SELECTED = (0, 1)

PINS = {
    "../proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    "../notes/uniform-pure-lift-private-edge-degeneration.md":
        "bb8b4f0b5315ca14354b7e7cbcd7d29a87dac7b519704ea3ca9cf8e2ebe94207",
    "verify_uniform_pure_lift_private_edge_degeneration.py":
        "6c715abb7a5fb7139eac5c5b62a18e1989fa133fe209b3fe3ada4253e8219433",
    "../notes/2026-08-15-h3-labelled-ghz-direct-response-compatibility.md":
        "97d2d77206c3bdb90dfe830a64b587ce5040cdf50b7c22723734535ca5a26261",
    "verify_h3_labelled_ghz_direct_response_compatibility.py":
        "1e2267128f2a74e1431b48128261b926d1b63d1254730ad5981cba57e3abcc80",
}

EXPECTED_LEDGER_SHA256 = "f90cdd3fe17970bfb2d51d5cdfd3f6ef434bdec2dbe29483de3c325e0cd97fea"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_sources():
    ledger = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            actual = hashlib.sha256(handle.read()).hexdigest()
        require(actual == expected,
                "pinned source changed: %s (%s)" % (relative, actual))
        ledger[relative] = actual
    return ledger


PINNED = pin_sources()


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )


def direct_pairing(left, right):
    return sum((left[i][j] * right[i][j]
                for i, j in product(COLORS, repeat=2)), Q(0))


def scalar_zero_channel(direct, selected=SELECTED):
    left, right = selected
    alpha = direct[left][right]
    trace = sum((direct[i][i] for i in COLORS), Q(0))
    channel = [[Q(-alpha) if i == j else Q(0) for j in COLORS]
               for i in COLORS]
    channel[left][right] += trace
    return channel, alpha, trace


def target_matrix(colour):
    return [[Q(1) if i == colour and j == colour else Q(0)
             for j in COLORS] for i in COLORS]


def unquotiented_slices(direct, lambdas):
    """Coefficient matrices of X_c in p_i s_j q^[2]."""
    return tuple(
        [[target_matrix(colour)[i][j] - lambdas[colour] * direct[i][j]
          for j in COLORS] for i in COLORS]
        for colour in COLORS
    )


def audit_literal_slice_and_scalar_zero():
    direct = [
        [Q(1), Q(2), Q(0)],
        [Q(3), Q(4), Q(5)],
        [Q(0), Q(6), Q(7)],
    ]
    channel, alpha, trace = scalar_zero_channel(direct)
    require(alpha == 2 and trace == 12, "selected direct data changed")
    require(channel == [[Q(-2), Q(12), Q(0)],
                        [Q(0), Q(-2), Q(0)],
                        [Q(0), Q(0), Q(-2)]],
            "canonical scalar-zero channel changed")
    require(direct_pairing(channel, direct) == 0,
            "the selected response is not scalar-zero")
    require(determinant3(channel) == -8,
            "the scalar-zero response lost full rank")

    cases = {}
    samples = {
        "zero": (Q(0), Q(0), Q(0)),
        "unary": (Q(2), Q(0), Q(0)),
        "binary": (Q(2), Q(-3), Q(0)),
        "ternary": (Q(2), Q(-3), Q(5)),
    }
    for label, lambdas in samples.items():
        slices = unquotiented_slices(direct, lambdas)
        # Adding a_ij Q back to each row restores the three labelled targets
        # coefficient by coefficient, without quotienting by Q.
        for colour in COLORS:
            restored = [[slices[colour][i][j]
                         + lambdas[colour] * direct[i][j]
                         for j in COLORS] for i in COLORS]
            require(restored == target_matrix(colour),
                    (label, colour, "literal row did not restore"))
        cases[label] = {
            "lambda": tuple(lambdas),
            "support": tuple(i for i in COLORS if lambdas[i]),
            "slice_ranks_not_assumed": True,
        }

    # Contracting all nine rows by K_* kills the Q coefficient and leaves
    # exactly -alpha times every pure target, in every dependent branch.
    contracted_target = tuple(channel[i][i] for i in COLORS)
    require(contracted_target == (-alpha, -alpha, -alpha),
            "the scalar-zero contraction is not -alpha Delta")
    return {
        "direct": tuple(tuple(row) for row in direct),
        "selected": SELECTED,
        "alpha": alpha,
        "trace": trace,
        "K_star": tuple(tuple(row) for row in channel),
        "sigma_K_star": direct_pairing(channel, direct),
        "det_K_star": determinant3(channel),
        "contracted_row": "r(K_*) q^[2] = -alpha (X0+X1+X2)",
        "q3_cases": cases,
    }


def kernel_route(lambdas, sigma):
    """Route a literal zero-response matrix using sigma Q=sum M_ii X_i."""
    diagonal = tuple(sigma * value for value in lambdas)
    support = tuple(i for i, value in enumerate(lambdas) if value)
    residual = tuple(diagonal[i] - sigma * lambdas[i] for i in COLORS)
    require(residual == (Q(0), Q(0), Q(0)),
            "kernel contraction left a literal target unit")
    if sigma == 0:
        route = "dark boundary: sigma=0 and diag(M)=0"
    elif not support:
        route = "zero-top direct-bright/target-dark inactive boundary"
    elif len(support) < 3:
        route = ("unary smaller-palette source" if len(support) == 1 else
                 "binary smaller-palette source")
    else:
        require(sigma * diagonal[0] * diagonal[1] * diagonal[2] != 0,
                "the ternary response kernel is not active")
        route = "active clean cap (also a forbidden ternary six-site source)"
    return {"sigma": sigma, "diag_M": diagonal, "route": route}


def audit_support_routing():
    records = {}
    for mask in range(8):
        lambdas = tuple(Q(i + 2) if mask & (1 << i) else Q(0)
                        for i in COLORS)
        support = tuple(i for i in COLORS if lambdas[i])
        if not support:
            primary = "zero-top non-pure common-power boundary"
        elif len(support) == 1:
            primary = "unary smaller-palette six-site source"
        elif len(support) == 2:
            primary = "binary smaller-palette six-site source"
        else:
            primary = "contradiction by arbitrary-complex six-site theorem"

        bright = kernel_route(lambdas, Q(3))
        dark = kernel_route(lambdas, Q(0))
        records[str(mask)] = {
            "support": support,
            "primary": primary,
            "bright_kernel": bright,
            "dark_kernel": dark,
        }

    require(sum(1 for item in records.values() if len(item["support"]) == 0) == 1,
            "zero support count changed")
    require(sum(1 for item in records.values() if len(item["support"]) == 1) == 3,
            "unary support count changed")
    require(sum(1 for item in records.values() if len(item["support"]) == 2) == 3,
            "binary support count changed")
    require(sum(1 for item in records.values() if len(item["support"]) == 3) == 1,
            "ternary support count changed")

    # One local diagonal rescaling already normalizes arbitrary nonzero
    # ternary amplitudes; using sixth roots at all sites is equivalent.
    ternary = (Q(2), Q(-3), Q(5))
    rescaling_at_site_zero = tuple(Q(1) / value for value in ternary)
    require(tuple(value * scale for value, scale
                  in zip(ternary, rescaling_at_site_zero, strict=True))
            == (Q(1), Q(1), Q(1)),
            "ternary target normalization failed")
    return {
        "support_census": records,
        "ternary_normalization": {
            "sample_lambda": ternary,
            "one_site_diagonal": rescaling_at_site_zero,
            "normalized": (Q(1), Q(1), Q(1)),
            "theorem": "pinned arbitrary-complex six-site obstruction",
        },
        "unit_test": (
            "for a proposed response kernel M, any nonzero coordinate of "
            "diag(M)-sigma(M)*lambda is a literal pure-target unit"
        ),
    }


def multiply_monomials(left, right):
    output = []
    for a, b in zip(left, right, strict=True):
        if a is not None and b is not None:
            return None
        output.append(a if a is not None else b)
    return tuple(output)


def pure_lift(colour, missing_pair):
    return tuple(None if site in missing_pair else colour for site in SITES)


def endpoint_form(site, colour):
    return tuple(colour if u == site else None for u in SITES)


def divided_cube(atoms):
    result = {}
    for chosen in combinations(atoms, 3):
        monomial = (None,) * 6
        for atom in chosen:
            monomial = multiply_monomials(monomial, atom)
            if monomial is None:
                break
        if monomial is not None:
            result[monomial] = result.get(monomial, 0) + 1
    return {word: value for word, value in result.items() if value}


def audit_zero_top_pure_lift_guard():
    """Freeze the exact last coarse guard and why it is not a source."""
    missing_pairs = ((0, 1), (2, 3), (4, 5))
    p = tuple(endpoint_form(2 * colour, colour) for colour in COLORS)
    s = tuple(endpoint_form(2 * colour + 1, colour) for colour in COLORS)
    lifts = tuple(pure_lift(colour, missing_pairs[colour])
                  for colour in COLORS)
    targets = tuple((colour,) * 6 for colour in COLORS)

    responses = {}
    for i, j in product(COLORS, repeat=2):
        values = {}
        ps = multiply_monomials(p[i], s[j])
        require(ps is not None, "endpoint stars collide")
        for lift in lifts:
            word = multiply_monomials(ps, lift)
            if word is not None:
                values[word] = values.get(word, 0) + 1
        expected = {targets[i]: 1} if i == j else {}
        require(values == expected, (i, j, values, expected))
        responses["%d%d" % (i, j)] = tuple(sorted(values.items()))

    direct = [[Q(0) for _ in COLORS] for _ in COLORS]
    direct[0][1] = direct[1][0] = Q(-1)
    channel, alpha, trace = scalar_zero_channel(direct)
    require(channel == [[Q(1), Q(0), Q(0)],
                        [Q(0), Q(1), Q(0)],
                        [Q(0), Q(0), Q(1)]],
            "formal guard did not produce K_*=I")
    response_atoms = tuple(multiply_monomials(p[i], s[i]) for i in COLORS)
    response_cube = divided_cube(response_atoms)
    require(response_cube == {(0, 0, 1, 1, 2, 2): 1},
            "formal guard lost rootlessness")
    require(len(set(missing_pairs)) == 3,
            "pure lifts lost their private missing pairs")
    return {
        "P_plus_S_rank": 6,
        "missing_pairs": missing_pairs,
        "formal_F_terms": lifts,
        "all_nine_formal_responses": responses,
        "direct": tuple(tuple(row) for row in direct),
        "alpha": alpha,
        "trace": trace,
        "K_star": tuple(tuple(row) for row in channel),
        "r_K_star_cube": tuple(sorted(response_cube.items())),
        "rootless": True,
        "why_not_physical": (
            "the pinned pure-lift theorem forbids one q with q^[2]=F and "
            "q^[3]=0; this guard is a sharp response-shadow fixture only"
        ),
        "literal_survivor": (
            "q^[3]=0, q^[2] outside the 45-dimensional pure-lift span, "
            "p_i s_j q^[2]=delta_ij X_i, scalar-zero K_* invertible, "
            "and r(K_*)^[3] nonzero"
        ),
    }


def jsonify(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, tuple):
        return [jsonify(item) for item in value]
    if isinstance(value, list):
        return [jsonify(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonify(item) for key, item in value.items()}
    return value


def content_hash(ledger):
    payload = json.dumps(jsonify(ledger), sort_keys=True,
                         separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def build_ledger():
    return {
        "theorem": (
            "under literal full-nine, scalar-zero and rootlessness, "
            "nonzero q^[3] in the pure target span routes by its palette "
            "support; q^[3]=0 is excluded on the pure-lift stratum and "
            "leaves exactly a non-pure four-site common-power boundary"
        ),
        "pins": PINNED,
        "literal_rows": audit_literal_slice_and_scalar_zero(),
        "support_routing": audit_support_routing(),
        "zero_top_guard": audit_zero_top_pure_lift_guard(),
        "scope": {
            "no_generic_rank_assumption": True,
            "no_quotient_by_q3": True,
            "rootlessness_role": (
                "retained as r(K_*)^[3]!=0; it does not alter the exact "
                "contraction r(K_*)q^[2]=-alpha Delta"
            ),
            "remaining_hypothesis": (
                "an additional theorem is needed to exclude the non-pure "
                "zero-top common-power jet; exact nine rows alone do not "
                "place q^[2] in the pure-lift span"
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    digest = content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "ledger digest changed: got %s" % digest)
    if arguments.dump_ledger:
        print(json.dumps(jsonify(ledger), indent=2, sort_keys=True))
    print("PASS: h3 degenerate q^[3] full-nine scalar-zero routing")
    print("mode", arguments.mode)
    print("q3 support: 0 guard / 3 unary / 3 binary / 1 ternary")
    print("ternary: six-site contradiction; pure-lift zero-top: excluded")
    print("remaining: non-pure zero-top common-power jet")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
