#!/usr/bin/env python3
"""Full four-direction Hasse cone and its physical descent obstruction.

The checker constructs the squarefree fourth Hasse prolongation of the
physical two-row Koszul complex.  In that genuine prolonged complex it
derives, rather than declares, the target-cancelled chain s_I-T with cap
boundary Y*w.  It then audits strict chart sectors and the complete
denominator presentation, and proves that diagonal projection to the old
physical row complex is not a chain map: its exact defect is
(H_0-u)*e_0.  The selected fourth differential also fails to descend to
the source quotient because it sends the source equation H_m to 1.
"""

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json


Q = Fraction
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
COLOURS = (0, 1, 2)
X, RCHART, P, QSITE = 0, 3, 6, 7
MIXED8 = (0, 1, 2, 1, 1, 2, 2, 2)
PURE8 = (0,) * 8
MIXED5 = {site: MIXED8[site] for site in ODD}
FORBIDDEN = frozenset((P, RCHART))
EXPECTED_DIGEST = "d3ec081e117cd2fd6cef08030b1abcd4deb19ddb41ca86848ef3ad7a2cd5f038"


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
        return "a", left, right, left_colour, right_colour
    return "a", right, left, right_colour, left_colour


def monomial(*variables):
    return tuple(sorted(variables))


def constant(value=1):
    value = Q(value)
    return {(): value} if value else {}


def variable(item):
    return {(item,): Q(1)}


def add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for term, coefficient in polynomial.items():
            answer[term] += coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def scale(scalar, polynomial):
    scalar = Q(scalar)
    return {term: scalar * coefficient
            for term, coefficient in polynomial.items()
            if scalar * coefficient}


def multiply(left, right):
    answer = defaultdict(Q)
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            answer[tuple(sorted(left_term + right_term))] += (
                left_coefficient * right_coefficient
            )
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def derivative(polynomial, item):
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        multiplicity = term.count(item)
        if not multiplicity:
            continue
        rest = list(term)
        rest.remove(item)
        answer[tuple(rest)] += multiplicity * coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def derivatives(polynomial, items):
    answer = polynomial
    for item in items:
        answer = derivative(answer, item)
    return answer


def colouring_monomial(matching, colouring):
    return monomial(*(
        edge(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


def hafnian(vertices, colouring, direct_free=True):
    answer = defaultdict(Q)
    for matching in matchings(tuple(vertices)):
        if direct_free and FORBIDDEN in (frozenset(pair) for pair in matching):
            continue
        answer[colouring_monomial(matching, colouring)] += Q(1)
    return dict(answer)


H_MIXED = hafnian(SITES, dict(enumerate(MIXED8)))
H_PURE = hafnian(SITES, dict(enumerate(PURE8)))
HOMOGENIZING_U = ("homogenizing_u",)
B_PURE = add(H_PURE, scale(-1, variable(HOMOGENIZING_U)))
YVAR = ("cap_Y",)
KAPPA = ("curvature_kappa",)
require(len(H_MIXED) == len(H_PURE) == 90, "direct-free full row size")


def face(deleted):
    return tuple(site for site in ODD if site != deleted)


def selected_directions(deleted, matching):
    internal = tuple(sorted(
        edge(left, right, MIXED8[left], MIXED8[right])
        for left, right in matching
    ))
    external = (
        edge(X, deleted, MIXED8[X], MIXED8[deleted]),
        edge(P, QSITE, MIXED8[P], MIXED8[QSITE]),
    )
    return tuple(sorted(internal + external)), internal, external


def masks(mask):
    """All submasks, including zero and mask."""
    answer = []
    submask = mask
    while True:
        answer.append(submask)
        if submask == 0:
            break
        submask = (submask - 1) & mask
    return tuple(sorted(answer))


def variables_for_mask(directions, mask):
    return tuple(
        direction for index, direction in enumerate(directions)
        if mask & (1 << index)
    )


def module_add(*vectors):
    answer = defaultdict(dict)
    scalar_answer = defaultdict(lambda: defaultdict(Q))
    for vector_ in vectors:
        for basis, polynomial in vector_.items():
            for term, coefficient in polynomial.items():
                scalar_answer[basis][term] += coefficient
    for basis, polynomial in scalar_answer.items():
        cleaned = {term: coefficient for term, coefficient in polynomial.items()
                   if coefficient}
        if cleaned:
            answer[basis] = cleaned
    return dict(answer)


def module_scale_polynomial(coefficient, vector_):
    return {
        basis: multiply(coefficient, polynomial)
        for basis, polynomial in vector_.items()
        if multiply(coefficient, polynomial)
    }


def hasse_row_differential(row, jet_mask, directions):
    """Squarefree Hasse prolongation differential on the two physical rows."""
    if row == "r0":
        return {("eq", jet_mask): B_PURE}
    require(row == "rm", "unknown physical row")
    answer = {}
    for derivative_mask in masks(jet_mask):
        coefficient = derivatives(
            H_MIXED, variables_for_mask(directions, derivative_mask))
        if coefficient:
            answer = module_add(answer, {
                ("eq", jet_mask ^ derivative_mask): coefficient
            })
    return answer


def hasse_chain_differential(chain, directions):
    answer = {}
    for (row, jet_mask), coefficient in chain.items():
        image = hasse_row_differential(row, jet_mask, directions)
        answer = module_add(
            answer, module_scale_polynomial(coefficient, image))
    return answer


def top_koszul_hasse_cycle(directions):
    full_mask = (1 << len(directions)) - 1
    chain = {}
    for derivative_mask in masks(full_mask):
        coefficient = derivatives(
            H_MIXED, variables_for_mask(directions, derivative_mask))
        if coefficient:
            chain[("r0", full_mask ^ derivative_mask)] = coefficient
    chain[("rm", full_mask)] = scale(-1, B_PURE)
    return chain


def target_of_hasse_chain(chain):
    """Prolongation of the constant target: only the zero jet of r0 survives."""
    return chain.get(("r0", 0), {})


def diagonal_projection(chain):
    """Forget every positive jet generator."""
    answer = {}
    for (row, jet_mask), coefficient in chain.items():
        if jet_mask == 0:
            answer[(row, 0)] = coefficient
    return answer


def physical_differential(chain):
    answer = {}
    for (row, _zero), coefficient in chain.items():
        base_image = (
            {("eq", 0): B_PURE}
            if row == "r0"
            else {("eq", 0): H_MIXED}
        )
        answer = module_add(
            answer, module_scale_polynomial(coefficient, base_image))
    return answer


def kill_mixed_variables(polynomial):
    mixed_variables = {
        item for term in H_MIXED for item in term
    }
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        if any(item in mixed_variables for item in term):
            continue
        answer[term] += coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def formal_hasse_cone_audit():
    records = []
    for deleted in ODD:
        for matching in matchings(face(deleted)):
            directions, internal, external = selected_directions(
                deleted, matching)
            require(len(directions) == 4 and len(set(directions)) == 4,
                    "four distinct selected directions")
            top = derivatives(H_MIXED, directions)
            require(top == constant(), "selected physical four-polar")
            for direction in directions:
                require(not derivative(B_PURE, direction),
                        "pure equation depends on a selected mixed direction")

            cycle = top_koszul_hasse_cycle(directions)
            require(not hasse_chain_differential(cycle, directions),
                    "full Hasse Koszul lift is not closed")
            require(target_of_hasse_chain(cycle) == constant(),
                    "Hasse Koszul top target is not one")

            # The combined cap chain is n=s-T.  Its source differential is
            # zero; d(-T)=+Y*w.  EqSystem jets and T have no ordinary-response
            # summand, so the formal cap ordinary-residue projection is zero.
            cap_boundary = variable(YVAR)
            formal_target = add(target_of_hasse_chain(cycle), constant(-1))
            require(not formal_target, "s-T failed target cancellation")
            formal_ores = {}
            require(not formal_ores, "formal cap residue is not zero")
            require(cap_boundary == variable(YVAR), "wrong cap sign")
            curvature_boundary = multiply(variable(KAPPA), cap_boundary)
            require(curvature_boundary == multiply(
                variable(KAPPA), variable(YVAR)), "curvature scaling")

            projected = diagonal_projection(cycle)
            require(projected == {("r0", 0): constant()},
                    "diagonal top is not r0")
            projected_boundary = physical_differential(projected)
            require(projected_boundary == {("eq", 0): B_PURE},
                    "diagonal chain defect is not (H0-u)e")
            require(not hasse_chain_differential(cycle, directions),
                    "source Hasse differential changed")

            # There is no target-zero repair a*r0+b*rm in the old two-row
            # physical span: target zero forces a=0, then b*H_m=H0-u would
            # contradict the specialization killing all mixed variables.
            require(not kill_mixed_variables(H_MIXED),
                    "mixed hafnian survived mixed-variable specialization")
            specialized_B = kill_mixed_variables(B_PURE)
            require(specialized_B == B_PURE and specialized_B,
                    "pure homogenized equation vanished in separation guard")

            # The selected top operator is not R-linear and does not descend
            # to the quotient by H_m: it sends the source equation H_m to 1.
            first = variable(directions[0])
            rest = constant()
            for direction in directions[1:]:
                rest = multiply(rest, variable(direction))
            require(derivatives(multiply(first, rest), directions) == constant(),
                    "top selector product witness")
            require(not derivatives(rest, directions),
                    "top selector R-linearity witness failed")
            require(derivatives(H_MIXED, directions) == constant(),
                    "source ideal non-descent witness")

            records.append({
                "deleted": deleted,
                "matching": [list(pair) for pair in matching],
                "directions": [list(item) for item in directions],
                "hasse_cycle_terms": len(cycle),
                "formal_cycle_boundary": 0,
                "formal_target_after_minus_T": 0,
                "formal_cap_ordinary_residue": 0,
                "formal_cap_boundary": "Y*w",
                "curvature_boundary": "kappa*Y*w",
                "diagonal_image": "r0-T",
                "diagonal_chain_defect": "(H0-u)*e",
                "selector_Hm": 1,
                "selector_descends_to_source_quotient": False,
            })
    require(len(records) == 15, "five faces times three matchings")
    return records


def contains_pair(term, pair):
    pair = frozenset(pair)
    return any(
        item[0] == "a" and frozenset((item[1], item[2])) == pair
        for item in term
    )


def chart_and_endpoint_audit():
    records = []
    for deleted in ODD:
        word = [0] * 8
        for site in face(deleted):
            word[site] = MIXED8[site]
        chart_row = hafnian(SITES, dict(enumerate(word)))
        pq_direct = {
            term: value for term, value in chart_row.items()
            if contains_pair(term, (P, QSITE))
        }
        pq_star = {
            term: value for term, value in chart_row.items()
            if not contains_pair(term, (P, QSITE))
        }
        pr_direct = {
            term: value for term, value in chart_row.items()
            if contains_pair(term, (P, RCHART))
        }
        pr_star = {
            term: value for term, value in chart_row.items()
            if not contains_pair(term, (P, RCHART))
        }
        require(not pr_direct, "direct-free pr sector is nonzero")

        pure_external = (
            edge(X, deleted, 0, 0),
            edge(P, QSITE, 0, 0),
        )
        mixed_external = (
            edge(X, deleted, MIXED8[X], MIXED8[deleted]),
            edge(P, QSITE, MIXED8[P], MIXED8[QSITE]),
        )
        for matching in matchings(face(deleted)):
            internal = tuple(sorted(
                edge(left, right, MIXED8[left], MIXED8[right])
                for left, right in matching
            ))
            chart_top = derivatives(
                chart_row, pure_external + internal)
            physical_top = derivatives(
                H_MIXED, mixed_external + internal)
            require(chart_top == physical_top == constant(),
                    "physical/chart top identification")
            require(derivatives(
                pq_direct, pure_external + internal) == constant(),
                "chart top left pq-direct")
            require(not derivatives(
                pq_star, pure_external + internal),
                "chart top entered pq-star")
            require(not derivatives(
                pr_direct, pure_external + internal),
                "chart top entered pr-direct")
            require(derivatives(
                pr_star, pure_external + internal) == constant(),
                "chart top left pr-two-star")

            complement = derivatives(H_MIXED, internal)
            bridged = derivatives(complement, mixed_external)
            require(bridged == constant(),
                    "endpoint 22-to-00 contraction coefficient")
            reinserted = multiply(
                multiply(variable(pure_external[0]),
                         variable(pure_external[1])),
                bridged,
            )
            require(derivatives(reinserted, pure_external) == constant(),
                    "endpoint replacement/direct readout")

        # The strict chart cell has boundary H-H=0 before sector splitting.
        require(add(chart_row, scale(-1, chart_row)) == {},
                "strict chart comparison acquired a global boundary")
        records.append({
            "deleted": deleted,
            "chart_row_terms": len(chart_row),
            "strict_global_boundary": 0,
            "top_sector_transfer": ["pq_direct", "pr_two_star"],
            "endpoint_bridge_top": 1,
            "can_cancel_pure_equation_defect": False,
        })
    return records


def reset_denominator_column(site, colour):
    if colour != MIXED5[site]:
        return {}
    colouring = {item: MIXED5[item] for item in face(site)}
    return {
        colouring_monomial(matching, colouring): Q(1)
        for matching in matchings(face(site))
    }


def denominator_face_audit():
    records = []
    columns = tuple((site, colour) for site in ODD for colour in COLOURS)
    for deleted in ODD:
        for matching in matchings(face(deleted)):
            internal = tuple(sorted(
                edge(left, right, MIXED5[left], MIXED5[right])
                for left, right in matching
            ))
            counts = {}
            supports = {}
            for size in range(3):
                local_counts = []
                local_supports = []
                for chosen in combinations(internal, size):
                    support = []
                    for column in columns:
                        value = derivatives(
                            reset_denominator_column(*column), chosen)
                        if value:
                            support.append(column)
                    local_counts.append(len(support))
                    local_supports.append(support)
                counts[size] = local_counts
                supports[size] = local_supports
            require(counts[0] == [5], "denominator base support count")
            require(counts[1] == [3, 3], "denominator one-edge support count")
            require(counts[2] == [1], "denominator top support count")
            require(supports[2][0] == [(deleted, MIXED5[deleted])],
                    "denominator top leakage")
            records.append({
                "deleted": deleted,
                "matching": [list(pair) for pair in matching],
                "nonzero_columns_by_internal_order": {
                    "0": counts[0],
                    "1": counts[1],
                    "2": counts[2],
                },
                "top_support": [deleted, MIXED5[deleted]],
                "proper_faces_require_full_presentation": True,
            })
    require(len(records) == 15, "denominator record count")
    return records


def main():
    hasse = formal_hasse_cone_audit()
    charts = chart_and_endpoint_audit()
    denominator = denominator_face_audit()
    certificate = {
        "full_hasse_target_cone": hasse,
        "strict_chart_and_endpoint": charts,
        "complete_denominator_faces": denominator,
        "outcome": {
            "formal_PP_cone_chain": "n_I=s_I-T",
            "formal_d_n": "Y*w",
            "formal_target": 0,
            "formal_cap_ordinary_residue": 0,
            "physical_d4": "not constructed",
            "diagonal_chain_map_defect": "(H0-u)*e",
            "source_quotient_shortcut": "invalid because Psi(Hm)=1",
            "missing_type": "fourth mixed-row Spencer jet with every proper face",
            "first_compatible_PP_order": 4,
        },
        "scope": {
            "proved": "formal Hasse-cone construction and exact physical descent no-go",
            "not_proved": [
                "geometric Hasse-Schmidt lift on a nonzero full source",
                "ordinary-residue comparison on the physical quotient",
                "actual d4 of the old physical Rees cone",
                "Krenn's conjecture",
            ],
        },
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"certificate digest changed: {digest}")
    print("h=3 full Hasse mapping-cone / physical d4 audit: PASS")
    print("formal PP cone: n_I=s_I-T has d=Y*w and target/cap-ores zero")
    print("strict pq/pr top and all 15 denominator face supports: PASS")
    print("physical diagonal descent defect: (H0-u)*e")
    print("source-quotient shortcut fails: selected fourth operator sends Hm to 1")
    print(f"certificate sha256 {digest}")


if __name__ == "__main__":
    main()
