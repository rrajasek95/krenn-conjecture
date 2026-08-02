#!/usr/bin/env python3
"""Exact obstruction to attaching the h=3 Reynolds q-zero symbol.

The checker derives the smallest cap differential from its graph cycle and
ordinary-response normalization, constructs the Reynolds-reduced formal
principal-parts differential from the complete denominator presentation,
and tests the literal chain-map equations.  It proves an obstruction only
inside this smallest combined complex.  It neither assigns a readout to a
new jet nor excludes a new chain supplied by the higher physical sector.
"""

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json


Q = Fraction
COLOURS = (0, 1, 2)
ODD = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
EXPECTED_DIGEST = "ee3699d5267fa63c896a50304f6548f565e6a09986fc5c54a9b6455928b3d5aa"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def coloured_matching(matching, colouring):
    return tuple(sorted(
        edge(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


def face(deleted):
    return tuple(site for site in ODD if site != deleted)


def face_polynomial(deleted):
    colouring = {site: MIXED[site] for site in face(deleted)}
    return {
        coloured_matching(matching, colouring): Q(1)
        for matching in matchings(face(deleted))
    }


def derivative(polynomial, variables):
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        rest = list(term)
        for variable in variables:
            if variable not in rest:
                break
            rest.remove(variable)
        else:
            answer[tuple(sorted(rest))] += coefficient
    return {term: value for term, value in answer.items() if value}


def reset_denominator_column(site, colour):
    """Selected-word coefficient of the complete denominator column."""
    if colour != MIXED[site]:
        return {}
    return face_polynomial(site)


def reynolds_operator(deleted, polynomial):
    """(1/3) sum over two-edge perfect-matching derivatives on F_deleted."""
    answer = defaultdict(Q)
    colouring = {site: MIXED[site] for site in face(deleted)}
    for matching in matchings(face(deleted)):
        variables = coloured_matching(matching, colouring)
        for term, coefficient in derivative(polynomial, variables).items():
            answer[term] += Q(1, 3) * coefficient
    return {term: value for term, value in answer.items() if value}


def denominator_reynolds_differential():
    """Derive the five formal PP top differentials; do not add cap readouts."""
    columns = tuple((site, colour) for site in ODD for colour in COLOURS)
    matrix = []
    records = []
    for deleted in ODD:
        row = []
        support = []
        for column in columns:
            value = reynolds_operator(
                deleted, reset_denominator_column(*column))
            require(set(value).issubset({()}), "Reynolds output is not q-zero")
            scalar = value.get((), Q(0))
            row.append(scalar)
            if scalar:
                support.append((column, scalar))
        expected = [((deleted, MIXED[deleted]), Q(1))]
        require(support == expected,
                f"face {deleted}: Reynolds denominator leakage")
        matrix.append(row)
        records.append({
            "deleted": deleted,
            "support_column": [deleted, MIXED[deleted]],
            "coefficient": 1,
            "internal_order": 2,
            "external_order": 2,
            "total_order": 4,
            "q_degree": 0,
        })

    # The selected five columns give the identity.  This is the differential
    # d_J(j_v)=y_v in the formal Reynolds-reduced PP symbol complex.
    selected_positions = [
        columns.index((site, MIXED[site])) for site in ODD
    ]
    selected = [
        [row[position] for position in selected_positions]
        for row in matrix
    ]
    identity = [
        [Q(1) if left == right else Q(0) for right in range(5)]
        for left in range(5)
    ]
    require(selected == identity, "formal Reynolds PP differential")
    return records, {
        "source_degree_one": ["j_1", "j_2", "j_3", "j_4", "j_5"],
        "source_degree_zero": ["y_1", "y_2", "y_3", "y_4", "y_5"],
        "d_J": "identity",
        "meaning": "formal PP symbol differential only",
    }


# Sparse univariate Q[Y] arithmetic.  A polynomial is {exponent: coefficient}.
ZERO = {}
ONE = {0: Q(1)}
YVAR = {1: Q(1)}


def pclean(polynomial):
    return {degree: Q(coefficient)
            for degree, coefficient in polynomial.items() if coefficient}


def padd(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for degree, coefficient in polynomial.items():
            answer[degree] += coefficient
    return pclean(answer)


def pscale(scalar, polynomial):
    return pclean({degree: Q(scalar) * coefficient
                   for degree, coefficient in polynomial.items()})


def pmul(left, right):
    answer = defaultdict(Q)
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            answer[left_degree + right_degree] += (
                left_coefficient * right_coefficient
            )
    return pclean(answer)


def pstring(polynomial):
    if not polynomial:
        return "0"
    pieces = []
    for degree in sorted(polynomial):
        coefficient = polynomial[degree]
        if degree == 0:
            monomial = "1"
        elif degree == 1:
            monomial = "Y"
        else:
            monomial = f"Y^{degree}"
        pieces.append(f"{coefficient}*{monomial}")
    return "+".join(pieces)


def cap_boundary(chain):
    """Differential forced by d(rho)=w and d(T+Y*rho)=0."""
    target_coefficient, response_coefficient = chain
    return padd(pscale(-1, pmul(YVAR, target_coefficient)),
                response_coefficient)


def physical_target(chain):
    """Projection to the physical-target summand R<T>."""
    return chain[0]


def ordinary_residue(chain):
    """Selected-word augmentation of the ordinary-response summand R<rho>."""
    return chain[1]


def rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    if not rows:
        return 0
    width = len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(rows))
             if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def finite_degree_system(max_degree, gamma_degree):
    """Linear equations for a*T+b*rho with boundary Y^gamma_degree.

    The system includes target=0 and ordinary residue=0.  It is used only as
    a finite-degree reflection of the exact split-projection proof.
    """
    width = 2 * (max_degree + 1)
    equations = []
    right_hand_side = []

    # target(a*T+b*rho)=a=0
    for degree in range(max_degree + 1):
        row = [Q(0)] * width
        row[degree] = Q(1)
        equations.append(row)
        right_hand_side.append(Q(0))

    # ores(a*T+b*rho)=b=0
    for degree in range(max_degree + 1):
        row = [Q(0)] * width
        row[max_degree + 1 + degree] = Q(1)
        equations.append(row)
        right_hand_side.append(Q(0))

    # -Y*a+b=Y^gamma_degree
    for degree in range(max_degree + 2):
        row = [Q(0)] * width
        if degree >= 1:
            row[degree - 1] = Q(-1)
        if degree <= max_degree:
            row[max_degree + 1 + degree] = Q(1)
        equations.append(row)
        right_hand_side.append(
            Q(1) if degree == gamma_degree else Q(0)
        )

    augmented = [
        row + [value] for row, value in zip(equations, right_hand_side)
    ]
    return rank(equations), rank(augmented), width


def derived_cap_and_attach_audit():
    # Derive d(T) rather than entering an augmented readout vector.  rho is
    # normalized by d(rho)=w, while g=T+Y*rho is the overlap graph cycle.
    T = (ONE, ZERO)
    rho = (ZERO, ONE)
    graph = (ONE, YVAR)
    require(cap_boundary(rho) == ONE, "ordinary response normalization")
    require(cap_boundary(graph) == ZERO, "cap graph is not a cycle")
    require(cap_boundary(T) == pscale(-1, YVAR),
            "d(T)=-Y*w was not forced by graph closure")
    require(physical_target(T) == ONE and physical_target(rho) == ZERO,
            "physical-target direct-sum projection")
    require(ordinary_residue(T) == ZERO and ordinary_residue(rho) == ONE,
            "ordinary selected-word augmentation")

    # Exact iff at zero desired scalar: the zero chain is invisible and has
    # zero boundary.  The nonzero cases below prove the converse.
    zero_chain = (ZERO, ZERO)
    require(cap_boundary(zero_chain) == ZERO and
            physical_target(zero_chain) == ZERO and
            ordinary_residue(zero_chain) == ZERO,
            "zero-scalar attaching base case")

    normalization_records = []
    for name, gamma in (("Y0_to_w", ONE), ("Y0_to_Yw", YVAR)):
        # With target zero, the chain equation has the unique old-cap
        # solution gamma*rho; its ordinary residue is gamma.
        graph_locked_lift = (ZERO, gamma)
        require(physical_target(graph_locked_lift) == ZERO,
                "target-zero old-cap lift")
        require(cap_boundary(graph_locked_lift) == gamma,
                "old-cap lift has wrong boundary")
        require(ordinary_residue(graph_locked_lift) == gamma,
                "ordinary-residue obstruction disappeared")

        # Imposing both augmentations kills both direct summands, so the
        # boundary becomes zero.  This is exact over every base ring.
        invisible_old_chain = (ZERO, ZERO)
        require(physical_target(invisible_old_chain) == ZERO and
                ordinary_residue(invisible_old_chain) == ZERO,
                "common augmentation kernel")
        require(cap_boundary(invisible_old_chain) == ZERO != gamma,
                "smallest cap unexpectedly supplied invisible boundary")

        normalization_records.append({
            "normalization": name,
            "desired_boundary": pstring(gamma),
            "unique_target_zero_old_lift": (
                "rho" if gamma == ONE else "Y*rho"
            ),
            "ordinary_residue": pstring(gamma),
            "invisible_old_lift": "none",
        })

    # No polynomial degree repairs the common-kernel obstruction.
    finite = []
    for max_degree in range(9):
        for gamma_degree in (0, 1):
            coefficient_rank, augmented_rank, variables = (
                finite_degree_system(max_degree, gamma_degree)
            )
            require(augmented_rank == coefficient_rank + 1,
                    "finite-degree invisible system became consistent")
            finite.append({
                "max_coefficient_degree": max_degree,
                "desired_Y_degree": gamma_degree,
                "variables": variables,
                "coefficient_rank": coefficient_rank,
                "augmented_rank": augmented_rank,
                "consistent": False,
            })

    # Five blocks: (target,ores): G^1 -> R^5+R^5 is literally the identity
    # after ordering T_1..T_5,rho_1..rho_5.  Its kernel is zero, whereas the
    # desired formal PP differential is gamma*I_5 and has rank five.
    augmentation_matrix = [
        [Q(1) if row == column else Q(0) for column in range(10)]
        for row in range(10)
    ]
    require(rank(augmentation_matrix) == 10,
            "five-block augmentation lost its split identity")
    desired_boundary = [
        [Q(1) if row == column else Q(0) for column in range(5)]
        for row in range(5)
    ]
    require(rank(desired_boundary) == 5,
            "five formal attaching obstructions lost rank")

    return {
        "cap_degree_one": ["T", "rho"],
        "cap_degree_zero": ["w"],
        "derived_differential": {"T": "-Y*w", "rho": "w"},
        "derived_target": {"T": "1", "rho": "0"},
        "derived_ordinary_residue": {"T": "0", "rho": "1"},
        "common_augmentation_kernel": 0,
        "bare_cap_invisible_attach_iff": "desired scalar gamma is zero",
        "normalizations": normalization_records,
        "finite_degree_systems": finite,
        "five_block_obstruction_rank": 5,
    }


def diagnostic_minimal_extension():
    # This is a type specification, not a construction from the source.
    # Adjoin n with maps derived by the desired chain equation and
    # augmentations.  Then j -> n is a chain map.
    records = []
    for name, gamma in (("normalized", ONE), ("cap_Y", YVAR)):
        differential_n = gamma
        target_n = ZERO
        ores_n = ZERO
        require(differential_n == gamma, "diagnostic new differential")
        require(target_n == ores_n == ZERO, "diagnostic invisibility")
        records.append({
            "normalization": name,
            "new_generator": "n",
            "cap_degree": 1,
            "total_PP_order": 4,
            "q_degree": 0,
            "d_n": pstring(gamma) + "*w",
            "target_n": "0",
            "ordinary_residue_n": "0",
            "status": "required type, not constructed",
        })
    return records


def main():
    denominator_records, formal_source = denominator_reynolds_differential()
    cap = derived_cap_and_attach_audit()
    missing = diagnostic_minimal_extension()
    certificate = {
        "denominator_reynolds": denominator_records,
        "formal_source_symbol_complex": formal_source,
        "smallest_derived_cap_complex": cap,
        "missing_generator": missing,
        "conclusion": {
            "A_attach_in_smallest_complex": "obstructed",
            "obstruction_class": "[gamma*w] in G0/d(ker(tgt,ores))",
            "obstruction_rank_five_blocks": 5,
            "sequential_construction": "impossible without a new cap-degree-one chain",
            "bare_cap_if_and_only_if": "invisible attach exists iff gamma=0",
            "first_candidate_total_PP_order": 4,
            "higher_physical_sector": "not tested",
        },
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"certificate digest changed: {digest}")
    print("h=3 Reynolds attaching comparison in the smallest cap complex: PASS")
    print("formal q-zero source symbol: d_J(j_v)=y_v with exact no leakage")
    print("derived old cap: d(T)=-Y*w, d(rho)=w, ker(target,ores)=0")
    print("A_attach: obstructed; target-zero lift gamma*rho has ores=gamma")
    print("first possible repair: new cap-degree-one chain at total PP order 4")
    print(f"certificate sha256 {digest}")


if __name__ == "__main__":
    main()
