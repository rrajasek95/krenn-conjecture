#!/usr/bin/env python3
"""Exact formal higher-Koszul/cap coupling and its descent obstruction.

The calculation is universal and presentation-level.  It derives the exact
second-order Leibniz commutators of the internal Reynolds operator and the
minimal direct-sector endpoint 22-to-00 operator.  Their composite selects the
pure row r_0 from the higher physical Koszul cell.  In the explicitly defined
formal principal-parts/endpoint-jet direct sum with the split cap block, this
row supplies the missing chain n=s-T with (d,tgt,ores)=(Y*w,0,0).

The same calculation gives literal non-R-linearity witnesses for both
second-order operators.  Thus the formal chain is not, by itself, a descended
chain in the physical EqSystem complex; promotion requires higher
Leibniz/A-infinity components and a two-chart comparison.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
X, P, QSITE = 0, 6, 7
PURE = (0,) * 8
MIXED = (0, 1, 2, 1, 1, 2, 2, 2)


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
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return "w", left, right, left_colour, right_colour
    return "w", right, left, right_colour, left_colour


def monomial(*variables):
    return tuple(sorted(variables))


def constant(value=ONE):
    return {(): Q(value)} if value else {}


def variable(item):
    return {monomial(item): ONE}


def add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for term, coefficient in polynomial.items():
            answer[term] += coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def scale(scalar, polynomial):
    return {term: Q(scalar) * coefficient
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
    """Ordinary derivative, including multiplicities in products."""
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        multiplicity = term.count(item)
        if not multiplicity:
            continue
        remainder = list(term)
        remainder.remove(item)
        answer[tuple(remainder)] += multiplicity * coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def derivatives(polynomial, items):
    answer = polynomial
    for item in items:
        answer = derivative(answer, item)
    return answer


def hafnian(vertices, colouring):
    answer = defaultdict(Q)
    for matching in matchings(tuple(vertices)):
        term = monomial(*(
            edge(left, right, colouring[left], colouring[right])
            for left, right in matching
        ))
        answer[term] += ONE
    return dict(answer)


H_MIXED = hafnian(SITES, dict(enumerate(MIXED)))
H_PURE = hafnian(SITES, dict(enumerate(PURE)))
require(len(H_MIXED) == len(H_PURE) == 105, "global hafnian size")


def face_matching_variables(deleted):
    face = tuple(site for site in ODD if site != deleted)
    colouring = {site: MIXED[site] for site in face}
    return tuple(
        monomial(*(
            edge(left, right, colouring[left], colouring[right])
            for left, right in matching
        ))
        for matching in matchings(face)
    )


def reynolds(deleted, polynomial):
    answer = {}
    for matching_variables in face_matching_variables(deleted):
        answer = add(
            answer,
            scale(Q(1, 3), derivatives(polynomial, matching_variables)),
        )
    return answer


def reynolds_cross(deleted, left, right):
    """The bilinear correction in L(ab)-L(a)b-aL(b)."""
    answer = {}
    for first, second in face_matching_variables(deleted):
        contribution = add(
            multiply(derivative(left, first), derivative(right, second)),
            multiply(derivative(left, second), derivative(right, first)),
        )
        answer = add(answer, scale(Q(1, 3), contribution))
    return answer


def endpoint_data(deleted):
    mixed_xv = edge(X, deleted, MIXED[X], MIXED[deleted])
    mixed_pq = edge(P, QSITE, MIXED[P], MIXED[QSITE])
    pure_xv = edge(X, deleted, 0, 0)
    pure_pq = edge(P, QSITE, 0, 0)
    return mixed_xv, mixed_pq, pure_xv, pure_pq


def multiply_many(*polynomials):
    answer = constant()
    for polynomial in polynomials:
        answer = multiply(answer, polynomial)
    return answer


def endpoint_bridge(deleted, polynomial):
    """M_(u_v t) partial_(xv,0m_v) partial_(pq,22)."""
    mixed_xv, mixed_pq, pure_xv, pure_pq = endpoint_data(deleted)
    return multiply_many(
        variable(pure_xv),
        variable(pure_pq),
        derivatives(polynomial, (mixed_xv, mixed_pq)),
    )


def endpoint_cross(deleted, left, right):
    mixed_xv, mixed_pq, pure_xv, pure_pq = endpoint_data(deleted)
    correction = add(
        multiply(derivative(left, mixed_xv), derivative(right, mixed_pq)),
        multiply(derivative(left, mixed_pq), derivative(right, mixed_xv)),
    )
    return multiply_many(variable(pure_xv), variable(pure_pq), correction)


def direct_pure_coefficient(deleted, polynomial):
    _mixed_xv, _mixed_pq, pure_xv, pure_pq = endpoint_data(deleted)
    return derivatives(polynomial, (pure_xv, pure_pq))


def selector(deleted, polynomial):
    return direct_pure_coefficient(
        deleted,
        endpoint_bridge(deleted, reynolds(deleted, polynomial)),
    )


def linear_image(element, generator_images):
    """Apply a module map whose coefficients lie in the sparse ring above."""
    answer = {}
    for generator, coefficient in element.items():
        answer = add(
            answer,
            multiply(coefficient, generator_images[generator]),
        )
    return answer


def complement_hafnian(deleted, colouring):
    complement = (X, deleted, P, QSITE)
    return hafnian(complement, colouring)


def audit_leibniz_identities():
    internal_variables = sorted({
        item
        for deleted in ODD
        for matching_variables in face_matching_variables(deleted)
        for item in matching_variables
    })
    tests = [constant()] + [variable(item) for item in internal_variables]
    tests += [
        hafnian(
            tuple(site for site in ODD if site != deleted),
            {site: MIXED[site] for site in ODD if site != deleted},
        )
        for deleted in ODD
    ]
    for deleted in ODD:
        for left in (H_MIXED, H_PURE):
            for right in tests:
                observed = reynolds(deleted, multiply(left, right))
                expected = add(
                    multiply(reynolds(deleted, left), right),
                    multiply(left, reynolds(deleted, right)),
                    reynolds_cross(deleted, left, right),
                )
                require(observed == expected, "Reynolds Leibniz identity")

        mixed_complement = complement_hafnian(
            deleted, dict(enumerate(MIXED))
        )
        endpoint_tests = [constant()]
        endpoint_tests += [variable(item) for item in endpoint_data(deleted)]
        for right in endpoint_tests:
            observed = endpoint_bridge(
                deleted, multiply(mixed_complement, right)
            )
            expected = add(
                multiply(endpoint_bridge(deleted, mixed_complement), right),
                multiply(mixed_complement, endpoint_bridge(deleted, right)),
                endpoint_cross(deleted, mixed_complement, right),
            )
            require(observed == expected, "endpoint Leibniz identity")


def audit_literal_non_linearity():
    """Exhibit exact product witnesses; neither selector stage is R-linear."""
    records = []
    for deleted in ODD:
        require(not selector(deleted, constant()),
                "combined selector unexpectedly sends one to a unit")
        require(selector(deleted, H_MIXED) == constant(),
                "combined selector lost its direct R-linearity witness")
        first, second = face_matching_variables(deleted)[0]
        first_factor = variable(first)
        second_factor = variable(second)
        require(not reynolds(deleted, first_factor),
                "Reynolds unexpectedly sees a first-order factor")
        require(not reynolds(deleted, second_factor),
                "Reynolds unexpectedly sees a first-order factor")
        require(
            reynolds(deleted, multiply(first_factor, second_factor))
            == constant(Q(1, 3)),
            "Reynolds product witness lost its 1/3 commutator",
        )
        require(
            reynolds_cross(deleted, first_factor, second_factor)
            == constant(Q(1, 3)),
            "Reynolds cross term does not account for the product witness",
        )

        mixed_xv, mixed_pq, _pure_xv, _pure_pq = endpoint_data(deleted)
        endpoint_left = variable(mixed_xv)
        endpoint_right = variable(mixed_pq)
        require(not endpoint_bridge(deleted, endpoint_left),
                "endpoint bridge unexpectedly sees one factor")
        require(not endpoint_bridge(deleted, endpoint_right),
                "endpoint bridge unexpectedly sees one factor")
        require(
            endpoint_bridge(
                deleted, multiply(endpoint_left, endpoint_right)
            )
            == multiply(variable(endpoint_data(deleted)[2]),
                        variable(endpoint_data(deleted)[3])),
            "endpoint product witness lost its cross term",
        )
        require(
            endpoint_cross(deleted, endpoint_left, endpoint_right)
            == endpoint_bridge(
                deleted, multiply(endpoint_left, endpoint_right)
            ),
            "endpoint cross term does not account for the product witness",
        )
        records.append({
            "deleted": deleted,
            "reynolds_factor_values": [0, 0],
            "reynolds_product_value": "1/3",
            "endpoint_factor_values": [0, 0],
            "endpoint_product_value": "u_v*t",
            "combined_selector_values": {"1": 0, "H_m": 1},
        })
    return records


def audit_higher_koszul_residual():
    records = []
    for deleted in ODD:
        mixed_complement = complement_hafnian(
            deleted, dict(enumerate(MIXED))
        )
        pure_complement = complement_hafnian(
            deleted, dict(enumerate(PURE))
        )
        require(reynolds(deleted, H_MIXED) == mixed_complement,
                "L_v(H_m) is not the mixed complement hafnian")
        require(not reynolds(deleted, H_PURE), "L_v(H_0) should vanish")

        mixed_xv, mixed_pq, pure_xv, pure_pq = endpoint_data(deleted)
        mixed_direct = monomial(mixed_xv, mixed_pq)
        pure_direct = monomial(pure_xv, pure_pq)
        require(mixed_complement.get(mixed_direct) == ONE,
                "mixed direct endpoint term is absent")
        require(sum(mixed_direct == term for term in mixed_complement) == 1,
                "mixed direct endpoint term is not unique")
        require(endpoint_bridge(deleted, mixed_complement) == {pure_direct: ONE},
                "endpoint 22-to-00 bridge has wrong image")
        require(direct_pure_coefficient(
            deleted, {pure_direct: ONE}) == constant(),
            "pure direct readout is not one")
        require(selector(deleted, H_MIXED) == constant(),
                "combined selector does not send H_m to one")
        require(not selector(deleted, H_PURE),
                "combined selector should kill H_0")

        # Coefficientwise application to
        #   K_m^phys = H_m r_0 + (u-H_0) r_m
        # leaves exactly r_0.  The homogenizing u is independent of every
        # internal and endpoint direction, so its selector is zero.
        homogenizing_u = variable(("homogenizing_u",))
        module_image = {
            "r_0": selector(deleted, H_MIXED),
            "r_m": selector(
                deleted, add(homogenizing_u, scale(-ONE, H_PURE))
            ),
        }
        require(module_image == {"r_0": constant(), "r_m": {}},
                "higher Koszul residual is not the pure row r_0")
        require(
            not selector(
                deleted,
                add(H_PURE, scale(-ONE, homogenizing_u)),
            ),
            "selected r_0 symbol is not closed under d(r_0)=H_0-u",
        )
        row_target = {"r_0": ONE, "r_m": ZERO}
        target = sum(
            row_target[row] * polynomial.get((), ZERO)
            for row, polynomial in module_image.items()
        )
        require(target == ONE, "pure residual lost its target augmentation")

        removed_slots = Counter(((X, 0), (deleted, MIXED[deleted]),
                                 (P, 2), (QSITE, 2)))
        inserted_slots = Counter(((X, 0), (deleted, 0), (P, 0), (QSITE, 0)))
        require(removed_slots != inserted_slots,
                "endpoint bridge unexpectedly preserves fine colour degree")
        records.append({
            "deleted": deleted,
            "mixed_complement_terms": len(mixed_complement),
            "pure_complement_terms": len(pure_complement),
            "endpoint_bridge": [list(mixed_xv), list(mixed_pq),
                                list(pure_xv), list(pure_pq)],
            "selector_Hm": 1,
            "selector_H0": 0,
            "koszul_residual": "r_0",
            "residual_target": 1,
        })
    return records


def audit_formal_jet_cap_cone():
    """Construct n=s-T in the stated formal direct-sum complex.

    This is deliberately a definition and audit of the selected jet symbol
    complex, not an assertion that the differential-operator selector has
    descended to an R-linear map on the physical EqSystem complex.
    """
    cap_y = variable(("cap", "Y"))
    kappa = variable(("curvature", "kappa"))

    # Degree-one formal generators are the selected pure Eq row s and the
    # split-cap generators T,rho; w is in degree two.  The ordinary-residue
    # projection is extended by zero on the *formal Eq-symbol summand*.
    differential = {
        "s": {},
        "T": scale(-ONE, cap_y),
        "rho": constant(),
    }
    target = {
        "s": constant(),
        "T": constant(),
        "rho": {},
    }
    ordinary_residue = {
        "s": {},
        "T": {},
        "rho": constant(),
    }

    graph = {
        "T": constant(),
        "rho": cap_y,
    }
    require(not linear_image(graph, differential),
            "same-power cap graph is not closed")
    require(linear_image(graph, target) == constant(),
            "same-power cap graph lost target one")
    require(linear_image(graph, ordinary_residue) == cap_y,
            "same-power cap graph lost residue Y")

    # The higher Koszul selector gives s.  Its target cancels the cap target,
    # while the sign dT=-Yw makes the boundary positive.
    missing_chain = {
        "s": constant(),
        "T": constant(-ONE),
    }
    require(linear_image(missing_chain, differential) == cap_y,
            "d(s-T) is not +Y*w")
    require(not linear_image(missing_chain, target),
            "s-T retained target")
    require(not linear_image(missing_chain, ordinary_residue),
            "s-T retained ordinary residue in the formal direct sum")

    scaled_missing_chain = {
        generator: multiply(kappa, coefficient)
        for generator, coefficient in missing_chain.items()
    }
    require(
        linear_image(scaled_missing_chain, differential)
        == multiply(kappa, cap_y),
        "curvature scaling of the missing boundary failed",
    )

    # Subtracting Y*rho produces the desired target-zero cycle and derives
    # its ordinary response rather than assuming a (kappa*Y,0,0) coordinate.
    response_cycle = add_chain_elements(
        scaled_missing_chain,
        {"rho": scale(-ONE, multiply(kappa, cap_y))},
    )
    require(not linear_image(response_cycle, differential),
            "kappa*(s-T-Y*rho) is not a cycle")
    require(not linear_image(response_cycle, target),
            "response cycle retained target")
    require(
        linear_image(response_cycle, ordinary_residue)
        == scale(-ONE, multiply(kappa, cap_y)),
        "response cycle has the wrong derived ordinary residue",
    )

    # Fine degree: deg(s)=mu(0), and the shifted cap generator has
    # deg(Y_0)+sigma=mu(0), where sigma occupies the three endpoint slots.
    mu_zero = Counter({(site, 0): 1 for site in SITES})
    degree_y_zero = Counter({(site, 0): 1 for site in ODD})
    cap_shift = Counter({(site, 0): 1 for site in (X, P, QSITE)})
    require(degree_y_zero + cap_shift == mu_zero,
            "selected Eq row and shifted cap generator have different degree")
    homological_degree = {"s": 1, "T": 1, "rho": 1, "w": 2}
    require(homological_degree["s"] == homological_degree["T"],
            "s and T do not lie in the same homological degree")

    # Formal attaching equation: d_J(j)=y, Phi_0(y)=Y*w and Phi_1(j)=s-T.
    # This is the finite selected-symbol equation; it does not assert descent.
    phi_zero_dj = cap_y
    d_phi_one = linear_image(missing_chain, differential)
    require(d_phi_one == phi_zero_dj,
            "formal attaching chain-map equation has the wrong sign")

    return {
        "formal_generators_degree_one": ["s", "T", "rho"],
        "formal_generator_degree_two": "w",
        "d_s_minus_T": "Y*w",
        "target_s_minus_T": 0,
        "ordinary_residue_s_minus_T": 0,
        "augmentation_scope": "formal direct-sum projection only",
        "scaled_cycle": "kappa*(s-T-Y*rho)",
        "scaled_cycle_ordinary_residue": "-kappa*Y",
        "physical_descent": "not asserted",
    }


def add_chain_elements(*elements):
    answer = {}
    for element in elements:
        for generator, coefficient in element.items():
            answer[generator] = add(answer.get(generator, {}), coefficient)
            if not answer[generator]:
                del answer[generator]
    return answer


def main():
    audit_leibniz_identities()
    non_linearity = audit_literal_non_linearity()
    records = audit_higher_koszul_residual()
    cone = audit_formal_jet_cap_cone()
    require(len(non_linearity) == 5, "non-linearity witness count")
    require(len(records) == 5, "face record count")
    require(cone["target_s_minus_T"] == 0, "formal cone result")
    print("Reynolds and endpoint second-order Leibniz identities: PASS")
    print("literal non-R-linearity witnesses for both selector stages: PASS")
    print("L_v(H_m)=three-term mixed endpoint hafnian; L_v(H_0)=0")
    print("minimal direct endpoint bridge 0m_v|22 -> 00|00: PASS")
    print("five coefficientwise higher-Koszul images are the pure row r_0")
    print("formal jet/cap cone: n=s-T has (d,tgt,ores)=(Y*w,0,0)")
    print("physical descent remains obstructed by nonzero Leibniz commutators")
    print("PASS: exact formal higher-Koszul coupling and descent obstruction")


if __name__ == "__main__":
    main()
