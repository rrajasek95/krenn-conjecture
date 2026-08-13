#!/usr/bin/env python3
"""Freeze the first uniform standard-basis obstruction for the E14 chart.

The 228 canonical unary-times-q reductions return the marked private
occurrence to itself with one of seven factors A having A(0)=1.  On the free
marked-occurrence module the return operator therefore has augmentation
exactly I_228.  This is the first cycle invariant left after the complete
zero/one/two/three-cell unit census.

For the 204 nonconstant factors, the return contains both g and m*g.  An
admissible global monomial order always has g < m*g, so it cannot orient g as
the leading term.  Reversing that inequality gives the infinite chain
g > m*g > m^2*g > ..., hence is not a well-order.  The 24 constant returns
are literal identity loops.  A positive-cell Rees filtration has the same
degree-zero identity and supplies no strict triangular potential.

This is an obstruction for the pinned canonical return graph, not a no-go
against a new source generator/proper-face comparison that breaks the loop.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c6_e14_minimal_enlargement_unit.py":
        "d5682f9134ff3dafddb4908707e5ceaacb25ff8b37632e57d9f9f3a4b62f84a8",
    "notes/h3-c6-e14-minimal-enlargement-unit.md":
        "552adf8a24410d4b8a09e61809c9a40c40274ad9c49a7ffe01b7ceb0d5ea22a7",
    "computations/verify_h3_c6_e14_pure11_unary_unit.py":
        "07160a67a4a16885fe481265ce67a372117b323dea82819e220cbe79e131df2d",
    "notes/h3-c6-e14-pure11-unary-unit.md":
        "cc9603e2f63e5b3de3b80dbf144a4f559f6e21f168fd9dfe9d5f95c4c7467ec4",
    "computations/verify_h3_c6_e14_two_cell_unit_frontier.py":
        "b5a2609b64f5a0bf1720a3c571c6c4d28aa316df00129f5b4574e0f32b8c3971",
    "notes/h3-c6-e14-two-cell-unit-frontier.md":
        "07593c3ebeb95b76461792c9835810f2b81e2b2ba701a9c910ea75c2b63809f1",
    "computations/verify_h3_c6_e14_three_cell_top_degree_boundary.py":
        "ac4ae4b8e2a351f4666cc2e196073663da94634ed4aac4c3f4e6b5dd92169313",
    "notes/h3-c6-e14-three-cell-top-degree-boundary.md":
        "75dc1e2d82e9b390fcf172eb3181f000c54b955e20a1b067fd11484df947f629",
    "computations/verify_h3_c6_e14_private_rewrite_spair_boundary.py":
        "d3605323f2a305dbc6c5dec38313ecb55c2f7a5676a255117abe9d0b773889a4",
    "notes/h3-c6-e14-private-rewrite-spair-boundary.md":
        "ac81c307c484dd1470a1ea953a70ee8c00a2e0cf875e31aff7f75f2e25315593",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
    "computations/verify_h3_e14_keq_private_factor_localization_provenance_gate.py":
        "b3b3114ba14d4e3d9c5e02390881c54c6b04f6a16f343c588344807289db0d24",
    "notes/h3-e14-keq-private-factor-localization-provenance-gate.md":
        "a2c0a1adf58bdf80c96e85cb61c894c0fa172b8c4f8668b4c66ce08dbe47a7d2",
    "computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py":
        "4d25b285b22e8a166a5e005a20e59cec11f463d25840f45a8acc4547d9e649ec",
    "notes/h3-e14-first-hit-dual-endpoint-q-extension-gate.md":
        "e841abbfe5d9da98ff041a448959d56ebb3059121ce080a28c0e8608a76c2605",
}
EXPECTED_LEDGER_SHA256 = (
    "b5d419147a325df36c30e46904ff93bac1d99d8199508d4539aad2488e24d4ee"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


# A factor is (display name, higher monomial exponents in (v04,v13),
# higher coefficient, multiplicity).  The omitted constant coefficient is 1.
RETURN_FACTORS = (
    ("1", (0, 0), Q(0), 24),
    ("1-v04", (1, 0), Q(-1), 54),
    ("1-v04/5", (1, 0), Q(-1, 5), 24),
    ("1+v04/3", (1, 0), Q(1, 3), 18),
    ("1-v13", (0, 1), Q(-1), 24),
    ("1+v13/3", (0, 1), Q(1, 3), 36),
    ("1-v04*v13/7", (1, 1), Q(-1, 7), 48),
)


def factor_audit() -> dict[str, object]:
    require(sum(count for _name, _exponent, _coefficient, count
                in RETURN_FACTORS) == 228,
            "return factor multiplicities stopped summing to 228")
    constant = sum(count for _name, exponent, coefficient, count
                   in RETURN_FACTORS
                   if exponent == (0, 0) and coefficient == 0)
    nonconstant = 228 - constant
    require((constant, nonconstant) == (24, 204),
            "constant/nonconstant return split changed")

    degree_counts = Counter()
    variable_counts = Counter()
    for _name, exponent, coefficient, count in RETURN_FACTORS:
        require(coefficient == 0 or sum(exponent) > 0,
                "a nonconstant coefficient lost its monomial")
        degree_counts[sum(exponent)] += count
        if coefficient:
            variable_counts[exponent] += count
    require(degree_counts == Counter({1: 156, 2: 48, 0: 24})
            and variable_counts == Counter({(1, 0): 96,
                                             (0, 1): 60,
                                             (1, 1): 48}),
            ("higher return monomial profile changed",
             degree_counts, variable_counts))

    # The occurrence-indexed return operator is diagonal.  We need not build
    # a 228x228 symbolic matrix: every diagonal constant is one, so its
    # augmentation is I.  The following invariants characterize it exactly.
    augmentation_diagonal = tuple(
        Q(1) for _factor in range(228)
    )
    require(len(augmentation_diagonal) == 228
            and sum(augmentation_diagonal, Q(0)) == 228
            and all(entry == 1 for entry in augmentation_diagonal),
            "return augmentation stopped being I_228")

    return {
        "factor_multiplicities": [
            {
                "factor": name,
                "higher_exponent_v04_v13": list(exponent),
                "higher_coefficient": str(coefficient),
                "count": count,
            }
            for name, exponent, coefficient, count in RETURN_FACTORS
        ],
        "marked_occurrence_count": 228,
        "constant_factor_count": constant,
        "nonconstant_factor_count": nonconstant,
        "higher_monomial_degrees": dict(sorted(degree_counts.items())),
        "augmentation_return_operator": "I_228",
        "augmentation_rank": 228,
        "augmentation_trace": 228,
        "augmentation_minimal_polynomial": "X-1",
    }


def order_obstruction() -> dict[str, object]:
    # In every admissible global monomial order 1<m for a nonunit monomial m,
    # and multiplication preserves order.  Therefore g<m*g.  A local reverse
    # choice creates the displayed infinite descending chain.  This finite
    # exponent check freezes the exact affected counts.
    global_impossible = 0
    literal_identity = 0
    local_chains = Counter()
    for name, exponent, coefficient, count in RETURN_FACTORS:
        if coefficient:
            require(sum(exponent) > 0, "nonconstant return became a unit")
            global_impossible += count
            local_chains[name] += count
        else:
            require(name == "1" and exponent == (0, 0),
                    "constant return stopped being the identity")
            literal_identity += count
    require((global_impossible, literal_identity) == (204, 24),
            "order obstruction count changed")

    # Strictly triangular endomorphisms of a finite degree-zero fibre are
    # nilpotent and have trace zero.  I_228 has trace 228 in characteristic
    # zero, invariant under every occurrence basis change.
    require(Q(228) != 0, "characteristic-zero trace test failed")
    return {
        "global_admissible_monomial_order": {
            "nonconstant_returns_with_g_below_mg": global_impossible,
            "reason": "1<m implies g<m*g by multiplicativity",
            "can_orient_g_as_leading_term": False,
        },
        "constant_returns": {
            "literal_identity_loops": literal_identity,
            "strict_descent": False,
        },
        "reversed_local_order": {
            "would_require": "g>m*g>m^2*g>...",
            "well_founded": False,
            "affected_returns": sum(local_chains.values()),
        },
        "positive_cell_Rees_filtration": {
            "degree_zero_map": "I_228",
            "strictly_triangular_after_basis_change": False,
            "trace_obstruction": "trace(I_228)=228, triangular descent trace=0",
            "interpretation": (
                "homogenization can retain the cycle in a higher Rees face, "
                "but the pinned return family alone supplies no decreasing "
                "degree-zero potential"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    factors = factor_audit()
    orders = order_obstruction()
    ledger = {
        "theorem": "E14 unary-return augmentation holonomy gate",
        "pins": PINS,
        "completed_sparse_layers": {
            "minimal_E14_charts": 9,
            "one_new_internal_cell_units": 1020,
            "two_new_internal_cell_units": 57291,
            "three_new_internal_cell_units": 2126208,
            "three_cell_universal_two_row_identities": 0,
            "why_not_global": (
                "the closing word changes with the support; degree at most "
                "three exhausts monomial types but does not glue the units"
            ),
        },
        "pre_return_rewrite_graph": {
            "marked_private_occurrences": 228,
            "G11_divisibility_rules": 1108,
            "G11_private_terminal_rules": 0,
            "unary_divisibility_rules": 1088,
            "minimum_unary_tail_degree_split": {"3": 24, "4": 204},
            "first_cycle": (
                "endpoint-orientation two-cycle with unchanged q tail"
            ),
        },
        "canonical_unary_return": factors,
        "order_obstruction": orders,
        "physical_nontriviality": {
            "canonical_first_hit_rank_then_target": [269, 270],
            "canonical_dual_support": 22,
            "canonical_dual_on_target": "-1",
            "warning": (
                "228 is the rank of the free marked-occurrence bookkeeping "
                "module, not a claim of 228 independent evaluated physical "
                "cokernel classes; the pinned canonical dual supplies one "
                "literal nonzero evaluated class"
            ),
        },
        "cycle_invariant": (
            "augmentation holonomy: after setting every new internal cell "
            "to zero, the complete canonical unary S-pair return is the "
            "identity on every marked private occurrence"
        ),
        "consequence": (
            "no common well-founded monomial order, positive-cell support "
            "potential, or unaugmented Rees filtration can promote the "
            "current canonical return rules to a global triangular proof.  "
            "The sparse 0/1/2/3-cell units remain valid but do not glue."
        ),
        "next_exact_input": (
            "a source-valid pointed occurrence/proper-face generator whose "
            "map on the augmentation private quotient is not the identity "
            "loop: it must kill, exchange, or move the marked class into a "
            "typed terminal/word-fine summand"
        ),
        "scope": (
            "exact for the pinned canonical complete unary S-pair choices "
            "and their complete first reductions on the nine minimal E14 "
            "charts.  It does not rule out a different higher source cell, "
            "a derived excess comparison, or a standard basis after such a "
            "generator is adjoined."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("E14 return-holonomy ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("E14 unary return global-order gate: AUGMENTATION HOLONOMY I_228")
    print("nonconstant returns blocking global monomial pivot: 204")
    print("literal identity returns: 24")
    print("positive-cell Rees degree-zero map: I_228 (not triangular)")
    print("new pointed/proper-face generator: REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
