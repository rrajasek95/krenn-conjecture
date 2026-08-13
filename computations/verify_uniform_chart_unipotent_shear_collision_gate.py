#!/usr/bin/env python3
"""Obstruct augmented-vertex unipotent shears by their collision face.

Write the complete response as the hafnian of the off-diagonal symmetric
matrix on augmented vertices P,S,0,... .  The projected elementary shear
E_(a<-b) acts by

    d x_(a,j) = x_(b,j),       d x_(i,j)=0 if a not in {i,j},

and d x_(a,b)=0 because the physical source has no loop x_(b,b).
Its exact finite pullback is R -> R+t C_(a,b).  Every term of C_(a,b) has
vertex degree zero at a, degree two at b, and degree one elsewhere.  These
multidegree sectors are disjoint for different ordered pairs (a,b), so no
nonzero combination of elementary shears is tangent to the response fibre.

For n=8, C_(a,b) has 45 monomials, each with coefficient two.  For the
representative P<-0 shear its selected chart term is

                   2*s0*q01*H2345.

On L01 itself the same shear gives s0*q01*H2345, not the squarefree
kappa packet.  Thus the first proper face is a missing-P/doubled-0
collision class.  It is outside the known squarefree pointed chart graph;
adding a graph coordinate for it is precisely a new non-diagonal Spencer
comparison, not an existing GL action.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_complete_torus_reynolds_gate.py":
        "5abf4da8fe5ee22a8f4dd47e2c84b7a7769b4ef9c3467a2a9c3494482021d457",
    "notes/uniform-chart-complete-torus-reynolds-gate.md":
        "c90ae8667121c78547974783c3879af9a0222723fc5fc666b3aeed1095863414",
    "computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py":
        "46b53933a080d0b8eeceee695ecd0d4c6d72224d7d0fea4352176b410b8b7fe4",
    "notes/uniform-response-h2-chart-direction-spencer-packet-gate.md":
        "d57b734cbbb99f5088cdd01e803522ffcd5b55dc2123525ae6d744de6e9a0445",
    "computations/verify_h3_h2_l01_endpoint_flag_s4_cplus_span_gate.py":
        "3ab94cb5293deeef5777588c15e308e4ac8974ffcff4272ee021432b6633089d",
    "notes/h3-h2-l01-endpoint-flag-s4-cplus-span-gate.md":
        "dcbb22545c23d209f2ee3cf654f00d4d76cae8b200dc886214abda9a7016c29f",
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "notes/uniform-physical-cartan-source-prism.md":
        "7d1da671c9203c7d6080d988fef662caba6024b65227881e111285ad35ba8067",
}
EXPECTED_LEDGER_SHA256 = (
    "d9b9196c3c1cb21e4bf1b76a743b32d3063acc3bcd310e1f0a67584c1e7086a8"
)

Edge = tuple[int, int]
Monomial = tuple[Edge, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> Edge:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def vertex_degree(monomial: Monomial, number_vertices: int) -> tuple[int, ...]:
    answer = [0] * number_vertices
    for left, right in monomial:
        answer[left] += 1
        answer[right] += 1
    return tuple(answer)


def shear_edge(value: Edge, source: int, replacement: int) -> Edge | None:
    if source not in value:
        return None
    other = value[1] if value[0] == source else value[0]
    # The congruence shear would produce the loop x_(replacement,replacement)
    # on edge (source,replacement).  It is absent on the physical
    # zero-diagonal matching source, so the projected derivation is zero.
    if other == replacement:
        return None
    return edge(replacement, other)


def shear_polynomial(matchings: tuple[Monomial, ...], source: int,
                     replacement: int) -> Counter[Monomial]:
    answer: Counter[Monomial] = Counter()
    for matching in matchings:
        incident = next(value for value in matching if source in value)
        moved = shear_edge(incident, source, replacement)
        if moved is None:
            continue
        monomial = tuple(sorted((moved,) + tuple(
            value for value in matching if value != incident
        )))
        answer[monomial] += 1
    return answer


def odd_double_factorial(value: int) -> int:
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def audit_order(number_vertices: int) -> dict[str, object]:
    require(number_vertices >= 6 and number_vertices % 2 == 0,
            number_vertices)
    vertices = tuple(range(number_vertices))
    matchings = tuple(perfect_matchings(vertices))
    expected_matchings = odd_double_factorial(number_vertices - 1)
    require(len(matchings) == expected_matchings, len(matchings))
    squarefree_degree = (1,) * number_vertices
    require({vertex_degree(matching, number_vertices)
             for matching in matchings} == {squarefree_degree},
            "a response matching stopped being squarefree by vertex")

    sectors = {}
    supports = {}
    expected_support = (
        math.comb(number_vertices - 2, 2)
        * odd_double_factorial(number_vertices - 5)
    )
    for source in vertices:
        for replacement in vertices:
            if source == replacement:
                continue
            polynomial = shear_polynomial(matchings, source, replacement)
            expected_degree = list(squarefree_degree)
            expected_degree[source] = 0
            expected_degree[replacement] = 2
            expected_degree = tuple(expected_degree)
            require(len(polynomial) == expected_support
                    and set(polynomial.values()) == {2}
                    and {vertex_degree(monomial, number_vertices)
                         for monomial in polynomial} == {expected_degree},
                    (number_vertices, source, replacement,
                     len(polynomial), Counter(polynomial.values())))
            key = (source, replacement)
            sectors[key] = expected_degree
            supports[key] = frozenset(polynomial)

    require(len(set(sectors.values())) == number_vertices * (number_vertices - 1),
            "ordered shear sectors stopped having distinct multidegrees")
    require(all(supports[left].isdisjoint(supports[right])
                for position, left in enumerate(supports)
                for right in tuple(supports)[position + 1:]),
            "two off-diagonal shear faces acquired common support")

    # Hence a linear combination sum n_ab C_ab vanishes iff every n_ab=0.
    # Diagonal vertex scalings send R to (sum a_i)R and are exactly the old
    # torus lane.
    return {
        "vertices": number_vertices,
        "response_matchings": len(matchings),
        "ordered_offdiagonal_shears": len(supports),
        "one_shear_collision_support": expected_support,
        "one_shear_coefficients": "all 2",
        "collision_multidegree": "one missing vertex, one doubled vertex",
        "pairwise_disjoint_shear_sectors": True,
        "offdiagonal_tangent_stabilizer_dimension": 0,
        "diagonal_semistabilizer": "vertex gauges; D(R)=(sum a_i)R",
        "affine_R_equals_1_diagonal_stabilizer_dimension": number_vertices - 1,
    }


def representative_h3_audit() -> dict[str, object]:
    # Vertex convention: P=0,S=1, physical sites 0,...,5 become 2,...,7.
    p_site, s_site = 0, 1
    zero, one, two, three, four, five = range(2, 8)
    matchings = tuple(perfect_matchings(tuple(range(8))))
    collision = shear_polynomial(matchings, p_site, zero)
    tails = tuple(perfect_matchings((two, three, four, five)))

    # A=Dq01, B=p0s1, C=p1s0.  P<-0 sends A and C to the same collision
    # monomial and kills B through the missing loop 00.
    direct = edge(p_site, s_site)
    q01 = edge(zero, one)
    p0 = edge(p_site, zero)
    s1 = edge(s_site, one)
    p1 = edge(p_site, one)
    s0 = edge(s_site, zero)
    local_collision_terms = tuple(tuple(sorted((s0, q01) + tail))
                                  for tail in tails)
    require(all(collision[monomial] == 2
                for monomial in local_collision_terms),
            "the selected P<-0 collision packet changed")

    def derivative_pair(pair: tuple[Edge, Edge]):
        answer: Counter[tuple[Edge, ...]] = Counter()
        for position, value in enumerate(pair):
            moved = shear_edge(value, p_site, zero)
            if moved is None:
                continue
            other = pair[1 - position]
            answer[tuple(sorted((moved, other)))] += 1
        return answer

    a_pair = (direct, q01)
    b_pair = (p0, s1)
    c_pair = (p1, s0)
    d_a = derivative_pair(a_pair)
    d_b = derivative_pair(b_pair)
    d_c = derivative_pair(c_pair)
    selected_pair = tuple(sorted((s0, q01)))
    require(d_a == Counter({selected_pair: 1})
            and not d_b
            and d_c == Counter({selected_pair: 1}),
            (d_a, d_b, d_c))
    d_l01 = Counter()
    for coefficient, derivative in ((2, d_a), (-1, d_b), (-1, d_c)):
        for monomial, value in derivative.items():
            d_l01[monomial] += coefficient * value
    d_l01 += Counter()
    require(d_l01 == Counter({selected_pair: 1}), d_l01)

    # No linear map from this collision sector to the squarefree first-PP
    # packet is supplied by multigrading: the former has degrees (0,2,1,...)
    # and the latter retains (1,...,1), merely marking one edge by d.
    collision_degree = vertex_degree(local_collision_terms[0], 8)
    squarefree_degree = (1,) * 8
    require(collision_degree == (0, 1, 2, 1, 1, 1, 1, 1)
            and collision_degree != squarefree_degree,
            collision_degree)
    return {
        "vertex_convention": "P,S,0,1,2,3,4,5",
        "transvection": "P<-0",
        "edge_action": {
            "D=PS": "s0=0S",
            "p0=P0": "loop 00, absent",
            "p1=P1": "q01=01",
            "p_j=Pj": "q0j",
        },
        "full_response_first_face": "C_(P,0)",
        "full_response_first_face_support": len(collision),
        "selected_chart_face": "2*s0*q01*H2345",
        "L01_shear_face": "s0*q01*H2345",
        "L01_face_tail_terms": len(local_collision_terms),
        "collision_vertex_degree": list(collision_degree),
        "desired_kappa_vertex_degree": list(squarefree_degree),
        "same_word_fine_repeated_grade": False,
        "primitive_sector_dual": (
            "project to vertex degree missing P/doubled 0; it detects only "
            "C_(P,0) and kills R, L01, the Kahler dL01 packet and every "
            "other shear sector"
        ),
    }


def physical_scope_audit() -> dict[str, object]:
    uniform = load(
        "computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py",
        "unipotent_uniform_packet",
    )
    uniform_ledger, uniform_digest = uniform.audit()
    require(uniform_digest == uniform.EXPECTED_LEDGER_SHA256
            and uniform_ledger["direction_packet"]["kappa"]
                == [2, 2, -1, -1, -1, -1],
            "the desired kappa packet changed")

    cartan = load(
        "computations/verify_uniform_physical_cartan_source_prism.py",
        "unipotent_physical_cartan",
    )
    # This historical checker prints its ledger rather than returning it;
    # content pins above are sufficient.  Its theorem concerns local colour
    # GL3 at physical sites, not GL of augmented operation vertices.
    require(cartan.EXPECTED_LEDGER_SHA256
            == "23516fe5ff27fda7e9906b5a0da9dcdbec3103a85b52d0006b972c856c3e5258",
            "the physical Cartan theorem changed")
    return {
        "desired_uniform_packet_ledger": uniform_digest,
        "local_colour_Cartan_distinction": (
            "sitewise GL3 root fields are related vector fields for the "
            "decorated source-to-target map; augmented-vertex P<-0 is not. "
            "It mixes operation types D/P/Q and leaves the response fibre"
        ),
        "GHZ_target_scope": (
            "P and S are operation/direction roles, not physical GHZ tensor "
            "sites.  There is no induced GHZ target transvection.  The "
            "source response already fails before target compatibility"
        ),
        "known_chart_graph_scope": (
            "the known pointed graph retains squarefree L01.  Filling "
            "C_(a,b), of missing/doubled vertex degree, requires a new "
            "collision graph/Tate coordinate; it is not a reset inside the "
            "same three-cap chart"
        ),
        "two_step_warning": (
            "opposite shears can return to squarefree degree only through a "
            "two-cell whose first boundary contains both collision sectors. "
            "Their disjoint first faces cannot be cancelled by signs"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    orders = tuple(audit_order(number_vertices)
                   for number_vertices in (6, 8, 10))
    require(orders[1]["response_matchings"] == 105
            and orders[1]["one_shear_collision_support"] == 45
            and orders[1]["ordered_offdiagonal_shears"] == 56,
            orders[1])
    ledger = {
        "theorem": "uniform augmented-vertex unipotent shear collision gate",
        "pins": PINS,
        "finite_orders": orders,
        "representative_h3": representative_h3_audit(),
        "physical_scope": physical_scope_audit(),
        "verdict": (
            "No nonzero projected elementary unipotent or linear combination of "
            "augmented-vertex shears preserves the complete hafnian response, "
            "even projectively.  E_(a<-b) has a nonzero first face C_(a,b) "
            "in the unique missing-a/doubled-b multidegree, so different "
            "shears cannot cancel.  For P<-0 the face is the 45-term "
            "collision packet with selected block 2*s0*q01*H2345; acting on "
            "L01 leaves s0*q01*H2345, not kappa tensor H."
        ),
        "minimal_no_go": (
            "one source-labelled collision/Tate generator for the "
            "missing-P/doubled-0 sector.  Without it the shear is not a map "
            "of the response fibre; with it one has merely restated the "
            "non-diagonal Spencer comparison to be constructed"
        ),
        "scope": (
            "exact complete off-diagonal hafnian algebra at even orders and "
            "the canonical h3 chart.  This does not exclude a higher "
            "Spencer/cobar totalization that explicitly includes the "
            "collision sectors and their target/augmented faces."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("augmented-vertex offdiagonal tangent stabilizer: ZERO")
    print("h3 one-shear first face: 45 collision monomials, coefficient 2")
    print("P<-0 selected face: 2*s0*q01*H2345")
    print("action on L01: s0*q01*H2345, not kappa")
    print("GHZ/augmented comparison: FAILS AT SOURCE RESPONSE FIRST")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
