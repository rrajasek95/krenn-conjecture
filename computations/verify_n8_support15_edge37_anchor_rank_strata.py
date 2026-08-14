#!/usr/bin/env python3
"""Exact rank-strata audit for the support-15 edge-37 quadratic.

The unique support-15 terminal has a two-matching response at edge 37.  This
checker audits:

* the tensor-rank classification of F=a0 tensor b1+a1 tensor b0;
* the rank-one cap factorization;
* the exact-source anchor-placement dichotomy at the degree-four endpoint;
* the complete one-anchor rank stratification, including the saturated
  coordinate obstruction; and
* a full support-labelled, anchor-valid, pure-normalized coefficient guard
  whose first failure is one literal mixed target word.

The last object is not an exact GHZ source.  It identifies the first full-row
hypothesis still needed to exclude the exceptional coordinate stratum.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "c439c1690057b817a7290c9f6d424ca3c0ada704ccfffd1a998fb97d72dfdc8f"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CENSUS = load_local(
    "n8_support15_census",
    "verify_n8_support15_clean_terminal_census.py",
)
N = 8
COLORS = range(3)
FULL_EDGES = CENSUS.UNRESOLVED_EDGES
NONANCHOR_EDGE = (1, 3)


def vector_rank(pair):
    first, second = pair
    if not any(first) and not any(second):
        return 0
    if not any(first) or not any(second):
        return 1
    return 1 if first[0] * second[1] == first[1] * second[0] else 2


def audit_tensor_rank_classification():
    """Exhaust the two-dimensional finite coefficient calibration.

    The proof over C is the standard pure-tensor argument recorded in the
    note.  This exact sweep catches signs and every zero-vector degeneration.
    """
    vectors = tuple(product((-1, 0, 1), repeat=2))
    zero_cases = 0
    nontrivial_rank_one_cases = 0
    for a0, a1, b0, b1 in product(vectors, repeat=4):
        tensor = tuple(
            a0[i] * b1[j] + a1[i] * b0[j]
            for i in range(2) for j in range(2)
        )
        if any(tensor):
            continue
        zero_cases += 1
        rank_a = vector_rank((a0, a1))
        rank_b = vector_rank((b0, b1))
        if rank_a == 2:
            require(not any(b0) and not any(b1),
                    ("independent a-side did not kill b-side", a0, a1, b0, b1))
        if rank_b == 2:
            require(not any(a0) and not any(a1),
                    ("independent b-side did not kill a-side", a0, a1, b0, b1))
        if rank_a == rank_b == 1 and any(a0 + a1) and any(b0 + b1):
            nontrivial_rank_one_cases += 1
    require(zero_cases == 417 and nontrivial_rank_one_cases == 256,
            ("tensor-rank calibration census changed",
             zero_cases, nontrivial_rank_one_cases))
    return {
        "finite_vectors": len(vectors),
        "zero_tensor_cases": zero_cases,
        "nontrivial_rank_one_side_cases": nontrivial_rank_one_cases,
    }


def polynomial_add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
        if answer[monomial] == 0:
            del answer[monomial]
    return answer


def polynomial_scale(polynomial, scalar):
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def polynomial_multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, 0)
                + left_coefficient * right_coefficient
            )
    return answer


def variable(name):
    return {(name,): 1}


def audit_rank_one_cap_and_saturation():
    """Check the universal rank-one factor and exceptional ideal certificate."""
    alpha0, alpha1 = variable("alpha0"), variable("alpha1")
    left = [variable(f"left{i}") for i in COLORS]
    right = [variable(f"right{i}") for i in COLORS]
    rank_one_components = {}
    for i in COLORS:
        for j in COLORS:
            first_matching = polynomial_multiply(
                polynomial_multiply(alpha0, left[i]),
                polynomial_multiply(alpha1, right[j]),
            )
            second_matching = polynomial_multiply(
                polynomial_multiply(alpha1, left[i]),
                polynomial_multiply(alpha0, right[j]),
            )
            component = polynomial_add(first_matching, second_matching)
            expected = polynomial_scale(
                polynomial_multiply(
                    polynomial_multiply(alpha0, alpha1),
                    polynomial_multiply(left[i], right[j]),
                ),
                2,
            )
            require(component == expected,
                    ("rank-one cap factorization changed", i, j))
            rank_one_components[i, j] = component

    # Exceptional normalization:
    # u0=e0, u1=e1, anchored near-vector w=e0, direct colour=2.
    # Put row0(K)=(a,b,c), row1(K)=(d,e,f).  After the anchor block,
    # g=(2ad, ae+bd, af+cd).  For invertible M the equation is g=0;
    # for rank-two M with left kernel <e2>, it again requires g0=g1=0.
    a, b, c, d, e, f = map(variable, ("a", "b", "c", "d", "e", "f"))
    g0 = polynomial_scale(polynomial_multiply(a, d), 2)
    g1 = polynomial_add(polynomial_multiply(a, e),
                        polynomial_multiply(b, d))
    g2 = polynomial_add(polynomial_multiply(a, f),
                        polynomial_multiply(c, d))
    ae = polynomial_multiply(a, e)
    certificate_left = polynomial_add(
        polynomial_scale(polynomial_multiply(ae, g1), 2),
        polynomial_scale(polynomial_multiply(
            polynomial_multiply(b, e), g0
        ), -1),
    )
    certificate_right = polynomial_scale(polynomial_multiply(ae, ae), 2)
    require(certificate_left == certificate_right,
            "one-anchor saturation certificate changed")

    return {
        "rank_one_components": len(rank_one_components),
        "rank_one_formula":
            "2*(u0.x)*(u1.x)*(y.M0 tensor y.M1)",
        "exceptional_g": (g0, g1, g2),
        "saturation_certificate":
            "2*(K00*K11)^2=2*(K00*K11)*g1-(K01*K11)*g0",
    }


def audit_anchor_placement_and_rank_strata():
    """Exhaust the source-anchor cases at the degree-four endpoint.

    The incident roles are direct, M0, M1, shared.  At least three must be
    anchors, hence at most one is non-anchor.
    """
    roles = ("direct", "M0", "M1", "shared")
    placements = []
    for mask in range(1 << len(roles)):
        anchors = frozenset(
            role for index, role in enumerate(roles) if (mask >> index) & 1
        )
        if len(anchors) < 3:
            continue
        if "direct" not in anchors:
            require({"M0", "M1", "shared"} <= anchors,
                    "non-anchor direct case lost its three other anchors")
            route = "both response blocks anchored: scalar permanent"
        elif {"M0", "M1"} <= anchors:
            route = "both response blocks anchored: scalar permanent"
        else:
            require(("M0" in anchors) != ("M1" in anchors)
                    and "shared" in anchors,
                    ("one-response-anchor placement changed", anchors))
            route = "one-anchor vector stratum"
        placements.append((tuple(sorted(anchors)), route))
    require(len(placements) == 5,
            ("anchor placement count changed", placements))
    require(sum(route == "one-anchor vector stratum"
                for _anchors, route in placements) == 2,
            "one-anchor placement count changed")

    # Complete algebraic classification in the one-anchor normalization.
    # Positive rank-one routes precede the remaining coordinate stratum.
    rank_strata = {
        "external_near_vector_noncoordinate":
            "active rank-one K via ker(u_i) meeting the coordinate torus",
        "anchored_near_vector_noncoordinate":
            "active rank-one K via ker(w) meeting the coordinate torus",
        "nonanchor_left_kernel_meets_torus":
            "active rank-one K via y*M=0",
        "coordinate_vectors_rank_M_le_1":
            "active general K; ker_left(M) contains a line other than <e_c>",
        "coordinate_vectors_rank_M_eq_2_generic_kernel":
            "active general K iff ker_left(M) != <e_c>",
        "coordinate_vectors_rank_M_eq_2_direct_kernel":
            "no active zero; saturation certificate",
        "coordinate_vectors_rank_M_eq_3":
            "no active zero; saturation certificate",
    }
    return {"anchor_placements": placements, "rank_strata": rank_strata}


ANCHOR_COLOURS = {
    (0, 1): 1,
    (0, 2): 1,
    (0, 3): 0,
    (0, 4): 2,
    (1, 2): 2,
    (1, 6): 0,
    (2, 4): 0,
    (2, 7): 0,
    (3, 5): 1,
    (3, 7): 2,
    (4, 5): 0,
    (4, 6): 1,
    (5, 6): 2,
    (5, 7): 1,
}


def coordinate_matrix(colour):
    return tuple(
        tuple(int(row == column == colour) for column in COLORS)
        for row in COLORS
    )


IDENTITY_MATRIX = tuple(
    tuple(int(row == column) for column in COLORS) for row in COLORS
)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


def coefficient(blocks, word):
    total = 0
    supporting = []
    for matching in perfect_matchings(tuple(range(N))):
        term = 1
        for u, v in matching:
            matrix = blocks.get(tuple(sorted((u, v))))
            if matrix is None:
                term = 0
                break
            term *= matrix[word[u]][word[v]]
            if term == 0:
                break
        total += term
        if term:
            supporting.append(matching)
    return total, tuple(supporting)


def audit_full_graph_anchor_guard():
    """A pure-normalized anchor-valid extension of the local obstruction."""
    blocks = {
        edge: (IDENTITY_MATRIX if edge == NONANCHOR_EDGE
               else coordinate_matrix(ANCHOR_COLOURS[edge]))
        for edge in FULL_EDGES
    }
    require(len(blocks) == 15 and set(blocks) == set(FULL_EDGES),
            "anchor guard support changed")

    # Every cubic vertex has exactly the three anchor colours.  Every
    # degree-four vertex also sees all three colours among its coordinate
    # anchor edges; edge 13 is the sole declared non-anchor.
    anchor_colour_ledger = {}
    for vertex in range(N):
        colours = {
            colour for edge, colour in ANCHOR_COLOURS.items() if vertex in edge
        }
        require(colours == set(COLORS),
                ("guard lost a source anchor colour", vertex, colours))
        anchor_colour_ledger[vertex] = tuple(sorted(colours))

    pure_ledger = []
    for colour in COLORS:
        value, supporting = coefficient(blocks, (colour,) * N)
        require(value == 1 and len(supporting) == 1,
                ("guard pure normalization changed", colour, value, supporting))
        pure_ledger.append((colour, supporting[0]))

    mixed = []
    for word in product(COLORS, repeat=N):
        if len(set(word)) == 1:
            continue
        value, supporting = coefficient(blocks, word)
        if value:
            require(value == 1 and len(supporting) == 1,
                    ("guard acquired a cancellable mixed fibre", word, value))
            mixed.append(("".join(map(str, word)), supporting[0]))
    require(len(mixed) == 11,
            ("guard mixed-row count changed", mixed))
    require(
        mixed[0]
        == ("00000101", ((0, 3), (1, 6), (2, 4), (5, 7))),
        ("guard first complete mixed-row failure changed", mixed[0]),
    )

    # The selected edge-37 data are exactly the exceptional rank-three
    # one-anchor normalization: u0=e0 on 72, u1=e1 on 75, direct=e2 on 73,
    # M0=e0e0^T on 30, and sole non-anchor M1=I on 31.
    require(ANCHOR_COLOURS[(2, 7)] == 0
            and ANCHOR_COLOURS[(5, 7)] == 1
            and ANCHOR_COLOURS[(3, 7)] == 2
            and ANCHOR_COLOURS[(0, 3)] == 0
            and blocks[(1, 3)] == IDENTITY_MATRIX,
            "guard left the exceptional edge-37 stratum")

    return {
        "support_edges": FULL_EDGES,
        "sole_nonanchor_edge": NONANCHOR_EDGE,
        "anchor_colours": ANCHOR_COLOURS,
        "anchor_colour_ledger": anchor_colour_ledger,
        "pure_ledger": pure_ledger,
        "mixed_unique_fibres": mixed,
        "first_complete_mixed_failure": mixed[0],
        "is_exact_source": False,
    }


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    ledger = canonical(
        {
            "tensor_rank_classification": audit_tensor_rank_classification(),
            "rank_one_and_saturation": audit_rank_one_cap_and_saturation(),
            "anchor_rank_strata": audit_anchor_placement_and_rank_strata(),
            "full_graph_anchor_guard": audit_full_graph_anchor_guard(),
        }
    )
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("edge-37 anchor rank ledger changed", digest))

    print("N=8 support-15 edge-37 anchor rank strata: PASS")
    print("  exact anchor placements at degree-four endpoint: 5")
    print("  scalar-permanent placements / one-anchor placements: 3 / 2")
    print("  one-anchor active-zero rank strata: all but 2 exceptional strata")
    print("  exceptions: coordinate anchors and rank(M)=3 or rank2 ker=<e_direct>")
    print("  pure-normalized full-graph anchor guard: yes")
    print("  first complete mixed-row failure: 00000101 (unique matching)")


if __name__ == "__main__":
    main()
