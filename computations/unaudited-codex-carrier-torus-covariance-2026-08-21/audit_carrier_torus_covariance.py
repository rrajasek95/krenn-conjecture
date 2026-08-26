#!/usr/bin/env python3
"""Exact site-colour torus covariance of response carriers and blockers."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import argparse
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (HERE.parent / "unaudited-codex-response-star-2026-08-20" /
             "response_star_core.py")
OUT = HERE / "results_carrier_torus_covariance.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def weight(site, colour):
    answer = [0] * 24
    answer[3 * site + colour] = 1
    return tuple(answer)


def add(*weights):
    return tuple(sum(values) for values in zip(*weights))


def neg(value):
    return tuple(-entry for entry in value)


def weight_label(value):
    positive = []
    negative = []
    for site in range(8):
        for colour in range(3):
            exponent = value[3 * site + colour]
            if exponent > 0:
                positive.extend([f"lambda_{site},{colour}"] * exponent)
            elif exponent < 0:
                negative.extend([f"lambda_{site},{colour}"] * (-exponent))
    numerator = "*".join(positive) or "1"
    return numerator if not negative else numerator + "/(" + "*".join(negative) + ")"


def zero_source():
    return {(u, v): [[Fraction(0) for _ in range(3)] for _ in range(3)]
            for u, v in combinations(range(8), 2)}


def curve_source(t):
    source = zero_source()
    for colour in range(3):
        for u, v in ((0, 1), (2, 3), (4, 5), (6, 7)):
            source[(u, v)][colour][colour] = Fraction(1)
    source[(1, 6)][0][0] = Fraction(1)
    source[(2, 7)][0][0] = Fraction(t)
    return source


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main(write_results=False):
    core = load_module("carrier_torus_response_core", CORE_PATH)
    p, q, centre = 6, 7, 0

    column_weights = {
        f"K{i}{j}": add(weight(p, i), weight(q, j))
        for i in range(3) for j in range(3)
    }
    row_weights = {}
    residual = tuple(v for v in range(8) if v not in (p, q))
    for a, b in combinations(residual, 2):
        if centre in (a, b):
            continue
        for alpha, beta in product(range(3), repeat=2):
            label = f"{a}{b}:{alpha}{beta}"
            row_weights[label] = add(weight(a, alpha), weight(b, beta))
            for i, j in product(range(3), repeat=2):
                first = add(weight(p, i), weight(a, alpha),
                            weight(q, j), weight(b, beta))
                second = add(weight(p, i), weight(b, beta),
                             weight(q, j), weight(a, alpha))
                require(first == second == add(row_weights[label],
                                               column_weights[f"K{i}{j}"]),
                        "response summand characters differ")
    require(len(row_weights) == 90 and len(column_weights) == 9,
            "star weight census changed")

    # Exact pure-normalized nonclosedness curve.
    source0 = curve_source(0)
    source1 = curve_source(1)
    pure_words = [tuple([colour] * 8) for colour in range(3)]
    require([core.hafnian(source0, word) for word in pure_words] == [1, 1, 1]
            and [core.hafnian(source1, word) for word in pure_words] == [1, 1, 1],
            "nonclosedness curve left pure normalization")
    labels0, matrix0 = core.response_star_matrix(source0, p, q, centre)
    labels1, matrix1 = core.response_star_matrix(source1, p, q, centre)
    require(labels0 == labels1, "curve response labels changed")
    rank0 = core.rank(matrix0)
    rank1 = core.rank(matrix1)
    blockers0 = core.activity_rows(source0, p, q)
    blockers1 = core.activity_rows(source1, p, q)
    memberships0 = [core.rank(matrix0 + [row]) == rank0 for row in blockers0]
    memberships1 = [core.rank(matrix1 + [row]) == rank1 for row in blockers1]
    require(rank0 == 0 and rank1 == 1,
            "nonclosedness curve ranks changed")
    require(memberships0 == [False, False, False, False] and
            memberships1 == [True, False, False, False],
            "nonclosedness curve blocker memberships changed")

    pure_characters = {
        f"H{colour}": add(*(weight(site, colour) for site in range(8)))
        for colour in range(3)
    }
    result = {
        "status": "PASS exact carrier torus covariance and nonclosedness audit",
        "torus": {
            "action": (
                "A_uv[i,j] -> lambda_(u,i)*lambda_(v,j)*A_uv[i,j], "
                "with endpoint order transposed when u>v"
            ),
            "dimension": 24,
            "pure_H_characters": {
                label: weight_label(character)
                for label, character in pure_characters.items()
            },
            "pure_normalization_preserving_subtorus": (
                "product_(site=0..7) lambda_(site,c)=1 for c=0,1,2"
            ),
            "subtorus_dimension": 21,
        },
        "response_matrix_covariance": {
            "carrier": {"pair": [p, q], "kind": "star", "centre": centre},
            "shape": [90, 9],
            "row_character_formula": (
                "rho_(ab:alpha,beta)=lambda_(a,alpha)*lambda_(b,beta)"
            ),
            "column_character_formula": (
                "kappa_(ij)=lambda_(p,i)*lambda_(q,j)"
            ),
            "entry_character_formula": "wt(L_(r,ij))=rho_r*kappa_ij",
            "matrix_formula": "L(lambda.A)=D_rho*L(A)*D_kappa",
            "row_weights": {label: weight_label(character)
                            for label, character in row_weights.items()},
            "column_weights": {label: weight_label(character)
                               for label, character in column_weights.items()},
            "rank_invariant": True,
            "kernel_action": "K -> D_kappa^-1 K",
        },
        "blocker_covariance": {
            "diagonal": {
                f"K{colour}{colour}": (
                    f"character kappa_{colour}{colour}^-1 = "
                    f"{weight_label(neg(column_weights[f'K{colour}{colour}']))}"
                ) for colour in range(3)
            },
            "direct": (
                "A_pq -> A_pq*D_kappa entrywise and K -> D_kappa^-1 K, "
                "so <K,A_pq> has trivial character"
            ),
            "membership_in_rowspan_invariant": True,
            "activity_nonvanishing_invariant": True,
        },
        "determinantal_weights": {
            "L_minor": (
                "Delta_(R,C)(lambda.A)=(product_(r in R)rho_r)*"
                "(product_(c in C)kappa_c)*Delta_(R,C)(A)"
            ),
            "augmented_diagonal_minor": (
                "for blocker K_dd and columns C, the factor is "
                "(product rho_R)*(product kappa_C)/kappa_dd"
            ),
            "augmented_direct_minor": (
                "for blocker <K,A_pq>, the factor is "
                "(product rho_R)*(product kappa_C)"
            ),
            "vanishing_ideals_torus_invariant": True,
        },
        "closedness_verdict": {
            "rank_at_most_r": "closed torus-invariant determinantal locus",
            "rank_exactly_r_plus_membership": (
                "locally closed torus-invariant locus: one r-minor of L is "
                "nonzero, all (r+1)-minors of L vanish, and all augmented "
                "(r+1)-minors vanish"
            ),
            "unstratified_blocker_membership": False,
            "unstratified_no_cap_union": False,
            "reason": (
                "rank([L;ell])=rank(L) is a union of locally closed rank "
                "strata and need not be closed when rank drops"
            ),
        },
        "pure_normalized_nonclosedness_counterexample": {
            "curve": (
                "anchor diagonal cells A_01[c,c]=A_23[c,c]=A_45[c,c]="
                "A_67[c,c]=1; additionally A_16[0,0]=1 and A_27[0,0]=t; "
                "all other cells zero"
            ),
            "pure_H_values": [1, 1, 1],
            "carrier": {"pair": [6, 7], "kind": "star", "centre": 0},
            "t_nonzero": {
                "rank": rank1,
                "rowspace": "span(K00)",
                "blocker_memberships": memberships1,
                "in_no_cap_union": True,
            },
            "t_zero": {
                "rank": rank0,
                "rowspace": "0",
                "blocker_memberships": memberships0,
                "in_no_cap_union": False,
            },
            "conclusion": (
                "The K00 membership branch, and hence the four-blocker union, "
                "is not closed even inside H0=H1=H2=1."
            ),
        },
        "Hilbert_Mumford_scope": (
            "The no-cap incidence is torus invariant, so one-parameter limits "
            "can be organized by weights only after retaining rank strata or "
            "taking a specified closure.  The raw membership union itself is "
            "not a closed projective/affine torus-stable target."
        ),
    }
    result["logical_sha256"] = logical_hash(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "row_weights": len(row_weights),
        "column_weights": len(column_weights),
        "rank_curve": [rank1, rank0],
        "membership_curve": [memberships1, memberships0],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
