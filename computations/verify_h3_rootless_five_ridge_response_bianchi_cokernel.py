#!/usr/bin/env python3
"""Exact five-ridge response-companion/Bianchi cokernel at rootless h=3.

For every deleted odd site v and every perfect matching N of its four-site
complement, the literal colour-bar prism which repairs the ridge defect

    Omega_v=(pq:22-pq:00)-(xv:0m_v-xv:00)

has a compulsory all-derivation companion q_N.  In the source-labelled
ridge quotient its column is therefore (-Omega_v,q_N).  The q_N are fifteen
distinct labelled matching monomials.  The resulting integral matrix has
primitive cokernel Z^5, detected by

    lambda_v = coeff(Omega_v) + sum_N coeff(q_N).

Thus the five Omega defects are formally bar boundaries, but none can be
repaired with zero response companion.  This is the exact standard
response-companion/Bianchi module in the selected ridge degrees; it does
not exclude a new relative augmentation/higher source-resolution face.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "eebec6188542c7bd652d622b3603762e4973578c8ed2976010982421d410919b"
PINS = {
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "computations/verify_h3_sitewise_gl3_covariance_face_tau_no_go.py":
        "bda92248adc08434896a99d5dfd241321e9be926ab7e8117daf55ee9df74c685",
    "computations/verify_h3_rootless_first_bianchi_selector_operation_no_go.py":
        "98691b0cc5e3b89ebf3373c207cba15953ee0a4cce4dbf7708602d23a9268073",
}

SITES = tuple(range(8))
X = 0
ODD = (1, 2, 3, 4, 5)
P = 6
QSITE = 7
MIXED = (0, 1, 2, 1, 1, 2, 2, 2)
ZERO = Q(0)
ONE = Q(1)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        remainder = tuple(site for site in vertices
                          if site not in (first, second))
        for tail in perfect_matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge(left: int, right: int, left_colour: int, right_colour: int):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def matching_monomial(matching, word):
    return tuple(sorted(edge(left, right, word[left], word[right])
                        for left, right in matching))


def polynomial_add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def recolour_incident(variable, site, old_colour, new_colour):
    left, right, left_colour, right_colour = variable
    if site == left and left_colour == old_colour:
        return edge(left, right, new_colour, right_colour)
    if site == right and right_colour == old_colour:
        return edge(left, right, left_colour, new_colour)
    return None


def derive_polynomial(polynomial, site, old_colour, new_colour):
    answer = defaultdict(Q)
    for monomial, coefficient in polynomial.items():
        for index, variable in enumerate(monomial):
            replacement = recolour_incident(
                variable, site, old_colour, new_colour
            )
            if replacement is None:
                continue
            term = tuple(sorted(
                monomial[:index] + (replacement,) + monomial[index + 1:]
            ))
            answer[term] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def fixed_matching_tensor(face, matching):
    """Universal output tensor for one labelled physical matching."""
    answer = {}
    for colours in product((0, 1, 2), repeat=len(face)):
        word = dict(zip(face, colours, strict=True))
        output_word = tuple(colours)
        monomial = tuple(sorted(
            edge(left, right, word[left], word[right])
            for left, right in matching
        ))
        answer[output_word] = {monomial: ONE}
    return answer


def output_change(tensor, face, site, target_colour, source_colour):
    position = face.index(site)
    answer = {}
    for word, polynomial in tensor.items():
        if word[position] != source_colour:
            continue
        changed = list(word)
        changed[position] = target_colour
        changed = tuple(changed)
        answer[changed] = polynomial_add(answer.get(changed, {}), polynomial)
    return answer


def source_derivation(tensor, site, target_colour, source_colour):
    answer = {}
    for word, polynomial in tensor.items():
        derived = derive_polynomial(
            polynomial, site, target_colour, source_colour
        )
        if derived:
            answer[word] = derived
    return answer


def matching_covariance_corner(face, matching, choices):
    tensor = fixed_matching_tensor(face, matching)
    for site, choice in zip(face, choices, strict=True):
        source_colour = MIXED[site]
        if choice == "L":
            tensor = output_change(tensor, face, site, 0, source_colour)
        elif choice == "D":
            tensor = source_derivation(tensor, site, 0, source_colour)
        else:
            raise RuntimeError(("unknown covariance corner", choice))
    return tensor


def add_sparse(target, source, scalar=ONE):
    for basis, coefficient in source.items():
        value = target.get(basis, ZERO) + scalar * coefficient
        if value:
            target[basis] = value
        elif basis in target:
            del target[basis]


def edge_boundary(left, right):
    """Oriented interval from left to right."""
    return {right: ONE, left: -ONE}


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), ZERO)


def endpoint_ridge_paths():
    """The complete literal pq square and xv interval.

    The two pq orders have the same boundary; their difference is the
    Bianchi square boundary.  Subtracting the xv path gives -Omega_v.
    """
    t22 = "pq:22"
    t02 = "pq:02"
    t20 = "pq:20"
    t00 = "pq:00"
    pq_first_p = {}
    add_sparse(pq_first_p, edge_boundary(t22, t02))
    add_sparse(pq_first_p, edge_boundary(t02, t00))
    pq_first_q = {}
    add_sparse(pq_first_q, edge_boundary(t22, t20))
    add_sparse(pq_first_q, edge_boundary(t20, t00))
    require(pq_first_p == pq_first_q == {t00: ONE, t22: -ONE},
            "pq colour-square paths disagree")

    records = []
    for v in ODD:
        old = f"x{v}:0{MIXED[v]}"
        new = f"x{v}:00"
        xv = edge_boundary(old, new)
        correction = dict(pq_first_p)
        add_sparse(correction, xv, -ONE)
        omega = {t22: ONE, t00: -ONE, old: -ONE, new: ONE}
        require(correction == {basis: -coefficient
                               for basis, coefficient in omega.items()},
                ("endpoint prism stopped repairing Omega", v, correction))
        records.append({
            "v": v,
            "middle_colour": MIXED[v],
            "omega": {basis: int(coefficient)
                      for basis, coefficient in omega.items()},
            "pq_paths": 2,
            "pq_square_path_difference": 0,
            "xv_paths": 1,
            "correction_boundary": "-Omega_v",
        })
    return records


def covariance_companions():
    """Build the fifteen termwise all-D companions q_N.

    On the four residual sites F_v, every L/D corner of local covariance
    has the same matching monomial.  It is enough to verify this on each
    fixed matching: an L choice reads its mixed coefficient, while a D
    choice replaces the corresponding zero endpoint by its mixed colour.
    Both give the same decorated edge at every site.
    """
    companions = []
    target_records = []
    for v in ODD:
        face = tuple(site for site in ODD if site != v)
        tag = tuple(MIXED[site] for site in face)
        require(set(tag) == {1, 2}, ("face stopped being mixed", v, tag))
        for matching_index, matching in enumerate(perfect_matchings(face)):
            mixed_monomial = matching_monomial(matching, MIXED)
            require(len(mixed_monomial) == 2, "face matching degree changed")

            # Each of the 16 L/D corners acts once at every residual site.
            # This is evaluated on the complete 3^4-output fixed-matching
            # tensor, not inferred from an unsigned support shadow.
            corner_values = set()
            for choices in product(("L", "D"), repeat=4):
                require(len(choices) == len(face), "corner arity")
                corner = matching_covariance_corner(face, matching, choices)
                pure_output = (0,) * 4
                expected = {pure_output: {mixed_monomial: ONE}}
                require(corner == expected,
                        ("termwise covariance corner failed", v, matching,
                         choices, corner))
                corner_values.add(next(iter(corner[pure_output])))
            require(corner_values == {mixed_monomial},
                    ("termwise covariance lock failed", v, matching))

            companions.append((v, matching_index, matching, mixed_monomial))

        # Completing the endpoint response by the four residual sites acts
        # on all seven nonzero input positions.  Both colours occur, so the
        # all-output endpoint kills ternary GHZ; every D-corner also kills it.
        acted = tuple(site for site in SITES if MIXED[site] != 0)
        source_colours = tuple(MIXED[site] for site in acted)
        require(len(acted) == 7 and set(source_colours) == {1, 2},
                "complete response word stopped being mixed")
        target_records.append({
            "v": v,
            "face_tag": "".join(map(str, tag)),
            "complete_acted_word": "".join(map(str, source_colours)),
            "target_terms": 0,
        })

    require(len(companions) == 15, "wrong companion count")
    monomials = [item[3] for item in companions]
    require(len(set(monomials)) == 15,
            "labelled response companions lost independence")
    return companions, target_records


def integral_cokernel(companions):
    """Exact matrix for all matching routes and all Bianchi differences."""
    ridge_index = {v: position for position, v in enumerate(ODD)}
    companion_index = {
        (v, matching_index): len(ODD) + position
        for position, (v, matching_index, _matching, _monomial)
        in enumerate(companions)
    }
    dimension = len(ODD) + len(companions)

    routes = []
    route_labels = []
    for v, matching_index, _matching, _monomial in companions:
        column = [ZERO] * dimension
        # Adding this route cancels +Omega_v and leaves its all-D companion.
        column[ridge_index[v]] = -ONE
        column[companion_index[(v, matching_index)]] = ONE
        routes.append(column)
        route_labels.append((v, matching_index))

    require(rank(routes) == 15, "route matrix lost full column rank")

    # Every matching switch and every pq shuffle/Bianchi difference is a
    # difference of route columns (or has zero projection).  Adjoining the
    # complete set cannot enlarge the route span.
    bianchi = []
    for v in ODD:
        indices = [index for index, label in enumerate(route_labels)
                   if label[0] == v]
        for left, right in combinations(indices, 2):
            bianchi.append([a - b for a, b in
                            zip(routes[left], routes[right], strict=True)])
    require(len(bianchi) == 15 and rank(routes + bianchi) == 15,
            "matching/Bianchi differences enlarged the complete module")

    desired = []
    separators = []
    for v in ODD:
        column = [ZERO] * dimension
        column[ridge_index[v]] = -ONE
        desired.append(column)

        covector = [ZERO] * dimension
        covector[ridge_index[v]] = ONE
        for matching_index in range(3):
            covector[companion_index[(v, matching_index)]] = ONE
        require(all(dot(covector, route) == 0 for route in routes + bianchi),
                ("primitive separator missed available route", v))
        require(dot(covector, column) == -ONE,
                ("primitive separator missed clean repair", v))
        separators.append(covector)

    require(rank(routes + desired) == dimension,
            "five clean repairs failed to span the cokernel")
    require(rank(separators) == 5, "primitive cokernel rank changed")

    # The matrix contains a unit pivot in every companion row.  Eliminating
    # those pivots identifies each companion with its Omega coordinate and
    # leaves five free primitive coordinates: coker is Z^5, with no torsion.
    unit_pivots = sum(
        1 for column in routes
        if sum(abs(int(value)) for value in column) == 2
        and sorted(value for value in column if value) == [-ONE, ONE]
    )
    require(unit_pivots == 15, "integral unit-pivot certificate changed")

    # A general normalized formal tail has coefficients c_v and anchor
    # incidence -sum c_v.  Ridge cancellation forces the total route
    # coefficient over matchings of v to equal c_v.  Its companion can be
    # zero only when every route coefficient, hence every c_v, is zero.
    # This contradicts the normalization sum c_v=1.
    sample_weights = (
        tuple(Q(1 if index == 0 else 0) for index in range(5)),
        tuple(Q(1, 5) for _ in range(5)),
        (Q(2), Q(-1), Q(3), Q(-4), Q(1)),
    )
    normalization_records = []
    for weights in sample_weights:
        require(sum(weights, ZERO) == ONE, "sample lost anchor normalization")
        # Reynolds route: split c_v equally among its three matching routes.
        correction = [ZERO] * dimension
        for v, weight in zip(ODD, weights, strict=True):
            for matching_index in range(3):
                route = routes[route_labels.index((v, matching_index))]
                correction = [left + weight * right / 3
                              for left, right in zip(correction, route, strict=True)]
        ridge = correction[:5]
        companion = correction[5:]
        require(ridge == [-weight for weight in weights],
                "Reynolds route failed to cancel weighted ridges")
        require(any(companion),
                "anchor-normalized response companion unexpectedly vanished")
        normalization_records.append({
            "weights": [str(value) for value in weights],
            "anchor_incidence": "-1",
            "ridge_cancelled": True,
            "nonzero_companion_terms": sum(bool(value) for value in companion),
        })

    return {
        "ambient_rank": dimension,
        "route_columns": len(routes),
        "matching_bianchi_differences": len(bianchi),
        "available_rank": rank(routes + bianchi),
        "rank_with_five_clean_repairs": rank(routes + bianchi + desired),
        "primitive_cokernel_rank": rank(separators),
        "integral_unit_pivots": unit_pivots,
        "cokernel": "Z^5",
        "separators": [
            f"lambda_{v}=Omega_{v}+sum_N companion_({v},N)" for v in ODD
        ],
        "anchor_normalized_samples": normalization_records,
    }


def main() -> None:
    pin_dependencies()
    endpoint_paths = endpoint_ridge_paths()
    companions, target_records = covariance_companions()
    cokernel = integral_cokernel(companions)

    ledger = {
        "pins": PINS,
        "physical_word": "".join(map(str, MIXED)),
        "endpoint_paths": endpoint_paths,
        "response_companions": [
            {
                "v": v,
                "matching_index": matching_index,
                "matching": [list(edge_pair) for edge_pair in matching],
                "monomial": [list(item) for item in monomial],
                "all_L_equals_all_D": True,
                "normalized_ordinary_residue": 1,
            }
            for v, matching_index, matching, monomial in companions
        ],
        "target_records": target_records,
        "module": cokernel,
        "coarse_signature_of_route": [0, 0, 0, "companion(q_N)"],
        "verdict": (
            "Omega_v is a formal colour-bar boundary, but every literal "
            "source-labelled repair leaves its independent all-D matching "
            "companion; coker is primitive Z^5"
        ),
        "minimal_new_face": (
            "for each v, a reduced relative ridge face with zero Omega, "
            "target, and cap boundary and augmentation -1 on the locked "
            "all-D companion"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED", ("pin ledger digest", digest))
    require(digest == EXPECTED_LEDGER_SHA256, ("ledger digest changed", digest))
    print("h=3 five-ridge response/Bianchi module: PASS")
    print("15 literal matching routes; available rank 15 in rank-20 module")
    print("five clean ridge repairs raise rank 15->20; primitive coker Z^5")
    print("all complete word changes target-zero; all-D companions remain")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
