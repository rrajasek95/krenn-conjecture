#!/usr/bin/env python3
"""Reduce the P2:21=0 affine boundary to one common-q lifting lemma.

Modulo the already routed external endpoint/q terms, the four response
coefficients at residual word 001122 are the sum of two rank-one blocks:

    E_ij = p_i*s_j*C + a_i*b_j*D.

Here (p,s) are the L ports P2,S3, (a,b) the M ports P0,S1, and C,D
are the literal three-term four-hole cofactors.  The proved nonzero-P2:21
closure gives p_2=0.  Exact 2x2 syzygies show that C!=0 reduces to complete
column proportionality/nonproportionality.  The sole new datum is therefore
the physical lifting of the scalar C=0 diagonal return.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_p2_21_private_row_closure.py":
        "e7760cf62c9a24f635f67174913f6fc5c7af45735a1979d96469bf254abcdc1f",
    "notes/h3-axis-target-coloop-p2-21-private-row-closure.md":
        "23b9c9c7cb02afb0aefe2e0c76fd1b46461bf8443aab14052c96bd9a35d96120",
    "computations/verify_h3_axis_target_coloop_common_covector_synchronization.py":
        "cb834de7584912dc8c4f650a0504326cf8badb7f4c4e9e823bad5068a53e7d31",
    "notes/h3-axis-target-coloop-common-covector-synchronization.md":
        "59d0b3778a1a86febdda55a428083e1e756131bf45e4e8a1c5883e30cc08d33c",
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
    "notes/h3-axis-target-coloop-proportional-nu-safe-reduction.md":
        "8e9ba2c477be06a022f1c86f334d45a95b1ff7d9393b7134c6f38aa21d797f14",
    "computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py":
        "6cb34278cccf9327bdfccdece0b254f3eff95d179e512e80e1c938d4fe0eef62",
    "notes/h3-axis-target-coloop-one-sided-companion-boundary.md":
        "ce93379f949002eaf05f24975b902760d9dcd7095e4150bf132259c73a498393",
}
EXPECTED_LEDGER_SHA256 = (
    "67057359d8266b234a06cb50ec10bf009d482ecba0ba614da33e1741b7ad3f2a"
)

P, S = 6, 7
WORD = (0, 0, 1, 1, 2, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def monomial(*variables):
    return tuple(sorted(variables))


def polynomial(*terms):
    result = Counter()
    for coefficient, variables in terms:
        result[monomial(*variables)] += coefficient
    return +result


def add(*scaled):
    result = Counter()
    for coefficient, value in scaled:
        for term, old in value.items():
            result[term] += coefficient * old
    return +result


def multiply(left, right):
    result = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            result[monomial(*(left_term + right_term))] += (
                left_value * right_value
            )
    return +result


def variable(name):
    return polynomial((1, (name,)))


def audit_rank_one_syzygies():
    names = "p1 s1 s2 a1 a2 b1 b2 C D".split()
    p1, s1, s2, a1, a2, b1, b2, C, D = map(variable, names)
    E11 = add((1, multiply(multiply(p1, s1), C)),
              (1, multiply(multiply(a1, b1), D)))
    E12 = add((1, multiply(multiply(p1, s2), C)),
              (1, multiply(multiply(a1, b2), D)))
    E21 = multiply(multiply(a2, b1), D)
    E22 = multiply(multiply(a2, b2), D)

    shore = add(
        (1, multiply(s2, E11)),
        (-1, multiply(s1, E12)),
    )
    shore_expected = multiply(multiply(a1, D), add(
        (1, multiply(b1, s2)), (-1, multiply(b2, s1))))
    p_axis_1 = add(
        (1, multiply(a2, E11)), (-1, multiply(a1, E21)))
    p_axis_1_expected = multiply(multiply(multiply(a2, p1), s1), C)
    p_axis_2 = add(
        (1, multiply(a2, E12)), (-1, multiply(a1, E22)))
    p_axis_2_expected = multiply(multiply(multiply(a2, p1), s2), C)
    require(shore == shore_expected
            and p_axis_1 == p_axis_1_expected
            and p_axis_2 == p_axis_2_expected,
            "the two-rank-one response syzygies changed")
    return {
        "response_block": "E_ij=p_i*s_j*C+a_i*b_j*D with p2=0",
        "shore_syzygy": "s2*E11-s1*E12=a1*D*(b1*s2-b2*s1)",
        "P_axis_syzygies": [
            "a2*E11-a1*E21=a2*p1*s1*C",
            "a2*E12-a1*E22=a2*p1*s2*C",
        ],
        "C_nonzero_consequence": (
            "when p1,s1,s2,C are nonzero and all Eij vanish, a2=0; "
            "the nonzero first row then forces (b1,b2) proportional to "
            "(s1,s2)"
        ),
    }


def audit():
    affine = load(
        "computations/verify_h3_axis_target_coloop_l_pair_affine_response_obstruction.py",
        "l_pair_affine_dependency",
    )
    top = load(
        "computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py",
        "return_top_dependency",
    )
    second = load(
        "computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py",
        "second_hybrid_dependency",
    )
    first = load(
        "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py",
        "first_hybrid_dependency",
    )
    routing = load(
        "computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py",
        "routing_dependency",
    )
    records = affine.boundary_records(top, second, first, routing)

    cofactor_types = Counter()
    representatives = {}
    for residual, _candidate in records:
        L, M, K = (residual[key] for key in ("L", "M", "K"))
        anchor_union = set(L) | set(M) | set(K)
        for shore, matching, holes in (
                ("C_L_ports_P2_S3", L, (0, 1, 4, 5)),
                ("D_M_ports_P0_S1", M, (2, 3, 4, 5))):
            port_tail = tuple(edge for edge in matching
                              if P not in edge and S not in edge)
            terms = []
            for hole_matching in routing.perfect_matchings(holes):
                labels = tuple(
                    (edge, (WORD[edge[0]], WORD[edge[1]]))
                    for edge in hole_matching
                )
                if set(hole_matching) == set(port_tail):
                    kind = "selected"
                elif all(left_colour == right_colour
                         for _edge, (left_colour, right_colour) in labels):
                    kind = "diagonal_return"
                else:
                    require(any(edge not in anchor_union
                                for edge, _label in labels),
                            "a third cofactor term stopped being external")
                    kind = "external_offdiagonal"
                cofactor_types[(shore, kind)] += 1
                terms.append({
                    "matching": hole_matching,
                    "labels": labels,
                    "kind": kind,
                })
            require(Counter(term["kind"] for term in terms) == Counter({
                "selected": 1,
                "diagonal_return": 1,
                "external_offdiagonal": 1,
            }), f"the {shore} three-term cofactor changed")
            representatives.setdefault(shore, terms)

    expected = Counter()
    for shore in ("C_L_ports_P2_S3", "D_M_ports_P0_S1"):
        for kind in ("selected", "diagonal_return", "external_offdiagonal"):
            expected[(shore, kind)] = 4
    require(cofactor_types == expected,
            f"the physical cofactor ledger changed: {cofactor_types}")

    syzygies = audit_rank_one_syzygies()
    ledger = {
        "records": len(records),
        "physical_four_hole_blocks": {
            shore: terms for shore, terms in sorted(representatives.items())
        },
        "cofactor_type_counts": {
            f"{shore}:{kind}": count
            for (shore, kind), count in sorted(cofactor_types.items())
        },
        "rank_one_response_syzygies": syzygies,
        "proved_reduction": (
            "after external terms route and the nonzero P2:21 branch closes, "
            "the response block has p2=0. If C is nonzero, the exact "
            "syzygies reduce it to complete-column proportionality versus "
            "nonproportional common-covector activity. The sole scalar "
            "boundary is C=0"
        ),
        "diagonal_boundary": {
            "equation": (
                "x01^00*x45^22 + x05^02*x14^02 = 0 "
                "after x04^02*x15^02 routes"
            ),
            "localized_consequence": (
                "the diagonal product is nonzero and equals the negative "
                "selected L-only product"
            ),
        },
        "single_missing_lemma": (
            "common-q affine lifting for the C=0 face: in a maximum-anchor, "
            "minimum-support exact five-tensor source, the displayed "
            "diagonal relation must either lift to a finite one-sided "
            "joint-kernel target-line modification/reselection, or create "
            "a nonproportional complete shore or an offanchor active carrier"
        ),
        "scope": (
            "the checker proves the physical factorization and syzygies, "
            "not the stated common-q affine lifting lemma"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the frozen zero-face affine ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 target-coloop zero-face affine reduction: PASS")


if __name__ == "__main__":
    main()
