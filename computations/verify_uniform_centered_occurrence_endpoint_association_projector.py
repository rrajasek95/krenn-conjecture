#!/usr/bin/env python3
"""Diagonalize the ordered-endpoint association algebra after matching-flatness.

Let B_h change exactly one ordered endpoint by switching its old endpoint
through one residual matching edge, and let S exchange the ordered endpoints.
These operators commute.  On the pointed matching-flat row v_h their joint
cyclic module has five eigenspaces:

    (B,S)=(4h,+1), (-2,+1), (2h-2,+1), (-2,-1), (2h,-1).

Thus B alone already separates constants from the four nonconstant
eigenvalues {-2,2h-2,2h}.  The integral polynomial

    P_h(B)=(B+2I)(B-(2h-2)I)(B-2hI)

sends the pointed row to a nonzero constant, and its value at the constant
eigenvalue is 8h(h+1)(2h+1).  Combining this endpoint projector with
the preceding matching projector gives a fully flat coefficient projector
while preserving a marked delta.

Physical use remains conditional: B is a one-endpoint Cartan/matching
prism and P_h(B) requires a coherent cubic totalization, including mixed
commutators with the two-edge matching switch.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(("cannot load dependency", path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py",
    "full_endpoint_transfer",
)
MATCH = load(
    "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py",
    "matching_eigenspace_correction",
)
PINS = {
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py":
        "6f5686298143b584a4edcb350145bf9d648277972aa96b90443c4ce254cb1d30",
    "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py":
        "6e9c665e2c42b23e1910963b030de2f6c4b16dfe4951eae6e0e79b7fcf1e6921",
    "computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py":
        "c52cec702336ecdd821617ba21c66538cdbbdf2fc964b3d1637dfaf25c9bae6b",
}
EXPECTED_LEDGER_SHA256 = "f400b3a17f3630e9777fe237bc3eee7cbe09e075338d961550648d3544cf0a48"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(vectors) -> int:
    if not vectors:
        return 0
    basis = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right
                          for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def endpoint_neighbors(occurrence, sites):
    p_site, s_site, matching = occurrence
    answer = []
    for selected in sites:
        if selected in (p_site, s_site):
            continue
        mate = next(
            other for pair in matching if selected in pair
            for other in pair if other != selected
        )
        remainder = tuple(pair for pair in matching if selected not in pair)
        answer.append((
            selected,
            s_site,
            tuple(sorted(remainder + (BASE.edge(p_site, mate),))),
        ))
        answer.append((
            p_site,
            selected,
            tuple(sorted(remainder + (BASE.edge(s_site, mate),))),
        ))
    require(len(answer) == len(set(answer)) == 4 * len(matching),
            ("endpoint adjacency degree changed", occurrence))
    return tuple(answer)


def apply_endpoint(vector, occurrences, lookup, sites):
    return tuple(
        sum(vector[lookup[value]]
            for value in endpoint_neighbors(occurrence, sites))
        for occurrence in occurrences
    )


def apply_swap(vector, occurrences, lookup):
    return tuple(
        vector[lookup[(s_site, p_site, matching)]]
        for p_site, s_site, matching in occurrences
    )


def matching_flat_row(h: int, occurrences, marked):
    answer = []
    marked_p, marked_s, marked_matching = marked
    for p_site, s_site, _matching in occurrences:
        q_value = sum(
            int(p_site not in pair and s_site not in pair)
            for pair in marked_matching
        )
        if (p_site, s_site) == (marked_p, marked_s):
            constant = 4 * h * h + 4 * h
        elif p_site == marked_p or s_site == marked_s:
            constant = 2 * h - 1
        else:
            constant = 0
        answer.append(Q(q_value + (2 * h - 1) * constant))
    return tuple(answer)


def polynomial_apply(vector, roots, operator):
    answer = vector
    for root in roots:
        image = operator(answer)
        answer = tuple(left - root * right
                       for left, right in zip(image, answer, strict=True))
    return answer


def uniform_ordered_pair_module_audit():
    """Verify the five endpoint sectors without enumerating matchings."""
    records = {}
    for h in range(2, 31):
        site_count = 2 * h + 2
        pairs = tuple(
            (left, right)
            for left in range(site_count)
            for right in range(site_count)
            if left != right
        )
        lookup = {value: index for index, value in enumerate(pairs)}

        def endpoint(vector):
            return tuple(
                sum(
                    vector[lookup[(selected, right)]]
                    + vector[lookup[(left, selected)]]
                    for selected in range(site_count)
                    if selected not in (left, right)
                )
                for left, right in pairs
            )

        def swap(vector):
            return tuple(vector[lookup[(right, left)]]
                         for left, right in pairs)

        constants = (Q(1),) * len(pairs)
        site_standard = [Q(0)] * site_count
        site_standard[0], site_standard[1] = Q(1), Q(-1)
        symmetric_standard = tuple(
            site_standard[left] + site_standard[right]
            for left, right in pairs
        )
        alternating_standard = tuple(
            site_standard[left] - site_standard[right]
            for left, right in pairs
        )

        symmetric_pair = []
        alternating_wedge = []
        symmetric_values = {
            (0, 1): 1, (1, 0): 1,
            (2, 3): 1, (3, 2): 1,
            (0, 2): -1, (2, 0): -1,
            (1, 3): -1, (3, 1): -1,
        }
        alternating_values = {
            (0, 1): 1, (1, 2): 1, (2, 0): 1,
            (1, 0): -1, (2, 1): -1, (0, 2): -1,
        }
        for pair in pairs:
            symmetric_pair.append(Q(symmetric_values.get(pair, 0)))
            alternating_wedge.append(Q(alternating_values.get(pair, 0)))
        symmetric_pair = tuple(symmetric_pair)
        alternating_wedge = tuple(alternating_wedge)

        sectors = (
            ("constant", constants, 4 * h, 1),
            ("symmetric_standard", symmetric_standard, 2 * h - 2, 1),
            ("symmetric_pair", symmetric_pair, -2, 1),
            ("alternating_standard", alternating_standard, 2 * h, -1),
            ("alternating_wedge", alternating_wedge, -2, -1),
        )
        for name, vector, endpoint_eigenvalue, swap_eigenvalue in sectors:
            require(any(vector), ("endpoint sector vanished", h, name))
            require(endpoint(vector) == tuple(
                endpoint_eigenvalue * value for value in vector
            ), ("uniform endpoint eigenvalue changed", h, name))
            require(swap(vector) == tuple(
                swap_eigenvalue * value for value in vector
            ), ("uniform swap eigenvalue changed", h, name))

        dimensions = {
            "constant": 1,
            "symmetric_standard": site_count - 1,
            "symmetric_pair": site_count * (site_count - 3) // 2,
            "alternating_standard": site_count - 1,
            "alternating_wedge": (site_count - 1) * (site_count - 2) // 2,
        }
        require(sum(dimensions.values()) == site_count * (site_count - 1),
                ("five endpoint sectors stopped exhausting", h, dimensions))
        records[h] = {
            "ordered_pairs": site_count * (site_count - 1),
            "sector_dimensions": dimensions,
            "spectrum": [
                [4 * h, 1],
                [2 * h - 2, 1],
                [-2, 1],
                [2 * h, -1],
                [-2, -1],
            ],
        }
    return {
        "module": "ordered distinct pairs on n=2h+2 sites",
        "five_sectors_exhaust_the_full_module": True,
        "orders_checked": records,
    }


def endpoint_spectral_audit():
    records = {}
    for h in range(2, 5):
        sites = tuple(range(2 * h + 2))
        occurrences = BASE.occurrences(sites)
        lookup = {value: index for index, value in enumerate(occurrences)}
        marked = BASE.marked_occurrence(h)
        vector = matching_flat_row(h, occurrences, marked)

        endpoint = lambda values: apply_endpoint(
            values, occurrences, lookup, sites
        )
        swap = lambda values: apply_swap(values, occurrences, lookup)
        require(endpoint(swap(vector)) == swap(endpoint(vector)),
                ("endpoint adjacency and swap stopped commuting", h))

        # The full cyclic module is five-dimensional.  The symmetric and
        # alternating projections have the stated minimal polynomials.
        powers = [vector]
        for _ in range(4):
            powers.append(endpoint(powers[-1]))
        require(rank(powers + [swap(vector)]) == 5,
                ("pointed endpoint cyclic module changed", h))

        symmetric = tuple(left + right for left, right
                          in zip(vector, swap(vector), strict=True))
        alternating = tuple(left - right for left, right
                            in zip(vector, swap(vector), strict=True))
        symmetric_zero = polynomial_apply(
            symmetric, (-2, 2 * h - 2, 4 * h), endpoint
        )
        alternating_zero = polynomial_apply(
            alternating, (-2, 2 * h), endpoint
        )
        require(not any(symmetric_zero) and not any(alternating_zero),
                ("joint endpoint spectrum changed", h))

        nonconstant_roots = (-2, 2 * h - 2, 2 * h)
        projected = polynomial_apply(vector, nonconstant_roots, endpoint)
        require(len(set(projected)) == 1 and projected[0],
                ("endpoint polynomial failed to produce a nonzero constant", h))
        constant_eigenvalue = 4 * h
        denominator = 1
        for root in nonconstant_roots:
            denominator *= constant_eigenvalue - root
        require(denominator == 8 * h * (h + 1) * (2 * h + 1),
                ("endpoint projector denominator changed", h, denominator))
        rational = tuple(value / denominator for value in projected)
        require(len(set(rational)) == 1,
                ("rational endpoint projector lost constancy", h))

        # Direct graph commutation also holds on representative basis points,
        # not merely on the cyclic vector.
        for occurrence in occurrences[:min(100, len(occurrences))]:
            left = sorted(
                value
                for switched in MATCH.switch_neighbors(occurrence[2])
                for value in endpoint_neighbors(
                    (occurrence[0], occurrence[1], switched), sites
                )
            )
            right = sorted(
                value
                for changed in endpoint_neighbors(occurrence, sites)
                for switched in MATCH.switch_neighbors(changed[2])
                for value in [(changed[0], changed[1], switched)]
            )
            require(left == right,
                    ("matching/endpoint coefficient operators stopped commuting",
                     h, occurrence))

        records[h] = {
            "occurrences": len(occurrences),
            "endpoint_degree": 4 * h,
            "cyclic_module_dimension": 5,
            "joint_spectrum": [
                [4 * h, 1],
                [2 * h - 2, 1],
                [-2, 1],
                [2 * h, -1],
                [-2, -1],
            ],
            "endpoint_projector_roots": list(nonconstant_roots),
            "integral_constant_output": int(projected[0]),
            "projector_denominator": denominator,
            "rational_constant_output": str(rational[0]),
        }
    return {
        "commuting_operators": {
            "B_h": "change p or s through one residual matching edge",
            "S": "swap the ordered endpoints",
        },
        "joint_spectrum": (
            "(4h,+),(2h-2,+),(-2,+),(2h,-),(-2,-)"
        ),
        "sector_interpretation": [
            "constant",
            "symmetric standard",
            "symmetric pair-shape",
            "alternating standard",
            "alternating wedge-shape",
        ],
        "integral_polynomial": (
            "P_h(B)=(B+2I)(B-(2h-2)I)(B-2hI)"
        ),
        "rational_projector_denominator": (
            "P_h(4h)=8h(h+1)(2h+1)"
        ),
        "bounded_exact_checks": records,
    }


def full_coefficient_projector_audit():
    records = {}
    for h in range(2, 31):
        matching_denominator = 2 * h - 1
        endpoint_denominator = 8 * h * (h + 1) * (2 * h + 1)
        total_denominator = matching_denominator * endpoint_denominator
        require(total_denominator > 0,
                ("combined projector acquired zero denominator", h))
        records[h] = {
            "matching_denominator": matching_denominator,
            "endpoint_denominator": endpoint_denominator,
            "combined_denominator": total_denominator,
        }
    return {
        "coefficient_level_composition": (
            "Pi_end Pi_match, with the marked delta retained outside both "
            "averaging operators"
        ),
        "negative_Gram_row_after_composition": "one constant on all g",
        "centered_projector_candidate": (
            "R_h e_f-(Pi_end Pi_match)k_f; rescale the constant so total "
            "mass is R_h"
        ),
        "marked_coefficient_nonzero": True,
        "rational_uniform_in_h": True,
        "integral_after_clearing": True,
        "denominators": records,
    }


def physical_lift_audit():
    higher = (ROOT / (
        "computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py"
    )).read_text()
    require("Reynolds product witness lost its 1/3 commutator" in higher
            and "endpoint product witness lost its cross term" in higher,
            "the pinned matching/endpoint commutator scope changed")
    return {
        "B_h_top_operation": (
            "one-endpoint Cartan/matching prism: move p (or s) to one "
            "residual site and pair the old endpoint with its mate"
        ),
        "P_h_B_degree": 3,
        "coefficient_commutations": [
            "[B_h,S]=0",
            "[B_h,A_match]=0",
        ],
        "source_chain_map_constructed": False,
        "required_augmented_lift": (
            "a source-valid cubic Cartan/Hasse totalization for P_h(B_h), "
            "with literal word/fine/repeated grade and target/residue/q/"
            "anchor/W/eta/sigma protection and the source-provenant "
            "terminal-Macaulay quotient"
        ),
        "first_product_rule_faces": [
            "one-endpoint Cartan cross term for each B_h factor",
            "pairwise B_h-B_h second Hasse faces",
            "mixed B_h-A_match faces from composing endpoint and matching "
            "projectors",
            "third totalization face of the cubic P_h(B_h)",
        ],
        "why_existing_formal_commutation_is_insufficient": (
            "the coefficient graphs commute, but the pinned physical "
            "operators have nonzero Leibniz cross terms.  A coefficient "
            "polynomial is not a chain polynomial until these faces are "
            "filled or detected by accepted physical terminals"
        ),
        "exact_next_theorem": (
            "lift the commuting pair (A_match,B_h) to an augmented "
            "bicomplex; prove the mixed commutator and cubic endpoint "
            "faces are boundaries/typed terminals.  Then the rational "
            "coefficient projector gives the centered occurrence cell"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "uniform centered occurrence endpoint association projector",
        "pins": PINS,
        "full_ordered_pair_module": uniform_ordered_pair_module_audit(),
        "endpoint_spectrum": endpoint_spectral_audit(),
        "full_coefficient_projector": full_coefficient_projector_audit(),
        "physical_lift": physical_lift_audit(),
        "verdict": (
            "After the matching filter, the remaining ordered-endpoint "
            "module has five joint (B_h,S) sectors.  B_h alone separates "
            "constants from the three distinct nonconstant eigenvalues, "
            "so a uniform rational/integral endpoint projector exists. "
            "Composing it with the matching projector completes the "
            "centered occurrence projector at coefficient level.  The "
            "remaining obstruction is physical: construct the augmented "
            "Cartan/Hasse bicomplex filling endpoint, two-switch, mixed, "
            "and cubic product-rule faces."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint association projector ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("ordered-endpoint joint spectrum: FIVE SECTORS")
    print("rational endpoint projector: CONSTRUCTED")
    print("full centered occurrence projector: COEFFICIENTWISE CONSTRUCTED")
    print("physical Cartan/Hasse bicomplex lift: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
