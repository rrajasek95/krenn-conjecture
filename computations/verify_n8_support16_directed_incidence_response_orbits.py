#!/usr/bin/env python3
"""Classify and test the 376 support-16 directed landing incidences.

The preceding support-16 audit leaves 376 directed incidences on high/high
support edges which are not private high-endpoint roles of a minimum two-RRX
face.  This checker:

* quotients them by the literal automorphism stabilizer of each of the 22
  support representatives;
* records shared versus never-private role, endpoint degree pair, and every
  occurrence of the underlying block as an RRR/RRX response factor for a
  different cap edge; and
* freezes the smallest singleton orbit and checks the basis-free response-
  ideal obstruction to extending the private-factor kernel argument.

The last test is deliberately a no-go for one proof move, not an exact GHZ
counterexample.  Its two displayed polynomials are complete physical
response polynomials for their source-labelled cap faces.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "dcc23f485e692fa493b829ae5b73bb7ffef348d746bcebbfbb5301cce3373b54"


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


CLOSURE = load_local(
    "n8_support16_two_rrx_for_incidence_orbits",
    "verify_n8_support16_two_rrx_coordinate_mixed_closure.py",
)
SUPPORT16 = CLOSURE.SUPPORT16
SUPPORT15 = SUPPORT16.SUPPORT15
BASE = SUPPORT16.BASE
N = 8


def adjacency_from_edges(edges):
    return CLOSURE.adjacency_from_edges(edges)


def other_endpoint(vertex, edge):
    require(vertex in edge, ("directed incidence left its edge", vertex, edge))
    return edge[0] if edge[1] == vertex else edge[1]


def response_terms(adjacency, edges, cap_edge):
    """Return the complete free response monomials of one physical cap.

    A term is `(kind, live_tag, response_factors)`.  RRR has no live tag;
    RRX has exactly one source-support tag and two response factors.  We keep
    repeated tags belonging to distinct residual matchings as distinct
    physical terms.
    """
    source_edges = set(edges)
    p, q = cap_edge
    residual = tuple(vertex for vertex in range(N) if vertex not in cap_edge)
    p_external = {v for v in residual if (adjacency[p] >> v) & 1}
    q_external = {v for v in residual if (adjacency[q] >> v) & 1}
    response_edges = {
        tuple(sorted((left, right)))
        for left in p_external for right in q_external if left != right
    }
    terms = []
    for raw_matching in BASE.perfect_matchings(residual):
        matching = tuple(tuple(sorted(edge)) for edge in raw_matching)
        if all(edge in response_edges for edge in matching):
            terms.append(("RRR", None, matching))
        for index, tag in enumerate(matching):
            factors = tuple(
                matching[j] for j in range(3) if j != index
            )
            if tag in source_edges and all(
                    factor in response_edges for factor in factors):
                terms.append(("RRX", tag, factors))
    return tuple(terms)


def graph_stabilizer(adjacency, edges):
    degree_sequence = tuple(row.bit_count() for row in adjacency)
    edge_set = set(edges)
    return tuple(
        permutation
        for permutation in SUPPORT15.preserving_group(degree_sequence)
        if {
            tuple(sorted((permutation[u], permutation[v])))
            for u, v in edges
        } == edge_set
    )


def directed_image(incidence, permutation):
    vertex, edge = incidence
    return (
        permutation[vertex],
        tuple(sorted((permutation[edge[0]], permutation[edge[1]]))),
    )


def role_sets(adjacency, edges):
    """Return eligible, landed-private, and unlanded shared roles."""
    cubic_vertices = {
        vertex for vertex in range(N)
        if adjacency[vertex].bit_count() == 3
    }
    private = set()
    shared = set()
    for cap_edge in edges:
        rrr, rrx, rrx_matchings, _p, _q = (
            SUPPORT15.response_counts(adjacency, cap_edge)
        )
        degrees = sorted(
            adjacency[vertex].bit_count() for vertex in cap_edge
        )
        if degrees != [3, 4] or (rrr, rrx, rrx_matchings) != (0, 2, 2):
            continue
        geometry = CLOSURE.two_rrx_geometry(adjacency, edges, cap_edge)
        _cubic, high = geometry["cap_endpoints"]
        private.update(
            (high, tuple(sorted((high, external))))
            for external in geometry["high_privates"]
        )
        shared.add((
            high,
            tuple(sorted((high, geometry["shared_external"]))),
        ))
    eligible = {
        (vertex, edge)
        for edge in edges if not (set(edge) & cubic_vertices)
        for vertex in edge
    }
    # Some private roles themselves meet the other cubic vertex.  Those
    # blocks are already coordinate by the cubic lemma and never entered the
    # 488 high/high register, so intersect only after constructing roles.
    return eligible, private & eligible, shared & eligible


def response_occurrences(adjacency, edges):
    """Map each directed support incidence to all response-factor terms."""
    edge_set = set(edges)
    occurrences = defaultdict(list)
    for cap_edge in edges:
        for term_index, (kind, tag, factors) in enumerate(
                response_terms(adjacency, edges, cap_edge)):
            for factor in factors:
                if factor not in edge_set:
                    continue
                for vertex in factor:
                    occurrences[(vertex, factor)].append((
                        cap_edge, term_index, kind, tag, factors,
                    ))
    return {
        incidence: tuple(items)
        for incidence, items in occurrences.items()
    }


def terminal_two_rrx_records():
    census = SUPPORT16.audit_census_and_orbits()
    records = tuple(
        record for record in census["terminal_orbits"]
        if record["route"] == "unresolved"
        and record["exit_data"]["minimum_response"][0] == 2
    )
    require(len(records) == 22,
            ("two-RRX terminal count changed", len(records)))
    return records


def audit_orbits():
    incidence_counter = Counter()
    orbit_counter = Counter()
    orbit_size_counter = Counter()
    occurrence_cap_histogram = Counter()
    occurrence_term_histogram = Counter()
    graph_records = []
    all_orbits = []

    for graph_index, record in enumerate(terminal_two_rrx_records()):
        edges = tuple(record["representative_edges"])
        adjacency = adjacency_from_edges(edges)
        eligible, private, shared = role_sets(adjacency, edges)
        unresolved = eligible - private
        occurrences = response_occurrences(adjacency, edges)
        stabilizer = graph_stabilizer(adjacency, edges)
        require(stabilizer, ("empty graph stabilizer", graph_index))

        unseen = set(unresolved)
        graph_orbits = []
        while unseen:
            representative = min(unseen)
            orbit = frozenset(
                directed_image(representative, permutation)
                for permutation in stabilizer
            )
            require(orbit <= unresolved,
                    ("stabilizer left unresolved register", graph_index,
                     representative, orbit - unresolved))
            unseen -= orbit

            signatures = set()
            for incidence in orbit:
                vertex, edge = incidence
                other = other_endpoint(vertex, edge)
                role = "shared" if incidence in shared else "never-private"
                items = occurrences.get(incidence, ())
                cap_count = len({item[0] for item in items})
                signatures.add((
                    role,
                    tuple(sorted((
                        adjacency[vertex].bit_count(),
                        adjacency[other].bit_count(),
                    ))),
                    cap_count,
                    len(items),
                ))
            require(len(signatures) == 1,
                    ("orbit signature is not invariant", graph_index,
                     representative, signatures))
            role, degree_pair, cap_count, term_count = signatures.pop()
            require(cap_count >= 2 and term_count >= 2,
                    ("an unlanded block is response-invisible", graph_index,
                     representative, cap_count, term_count))

            orbit_record = {
                "size": len(orbit),
                "representative": representative,
                "role": role,
                "degree_pair": degree_pair,
                "response_cap_count": cap_count,
                "response_term_count": term_count,
            }
            graph_orbits.append(orbit_record)
            all_orbits.append((graph_index, orbit_record, edges))
            incidence_counter[role, degree_pair] += len(orbit)
            orbit_counter[role, degree_pair] += 1
            orbit_size_counter[len(orbit)] += 1
            occurrence_cap_histogram[cap_count] += len(orbit)
            occurrence_term_histogram[term_count] += len(orbit)

        graph_records.append({
            "graph_index": graph_index,
            "degree_sequence": record["degree_sequence"],
            "labelled_orbit_size": record["orbit_size"],
            "stabilizer_size": len(stabilizer),
            "eligible": len(eligible),
            "private_landed": len(eligible & private),
            "unlanded": len(unresolved),
            "stabilizer_orbits": tuple(sorted(
                graph_orbits,
                key=lambda item: (
                    item["size"], item["representative"], item["role"]
                ),
            )),
        })

    require(sum(incidence_counter.values()) == 376,
            ("unlanded incidence total changed", incidence_counter))
    require(incidence_counter == Counter({
        ("shared", (4, 4)): 18,
        ("shared", (4, 5)): 29,
        ("shared", (4, 6)): 5,
        ("never-private", (4, 4)): 137,
        ("never-private", (4, 5)): 156,
        ("never-private", (4, 6)): 11,
        ("never-private", (5, 5)): 20,
    }), ("role/degree incidence census changed", incidence_counter))
    require(orbit_counter == Counter({
        ("shared", (4, 4)): 15,
        ("shared", (4, 5)): 19,
        ("shared", (4, 6)): 2,
        ("never-private", (4, 4)): 106,
        ("never-private", (4, 5)): 114,
        ("never-private", (4, 6)): 8,
        ("never-private", (5, 5)): 17,
    }), ("role/degree orbit census changed", orbit_counter))
    require(orbit_size_counter == Counter({1: 208, 2: 62, 4: 11}),
            ("stabilizer orbit sizes changed", orbit_size_counter))
    require(occurrence_cap_histogram == Counter({
        2: 52, 3: 121, 4: 139, 5: 48, 6: 14, 7: 2,
    }), ("response-cap occurrence histogram changed",
         occurrence_cap_histogram))
    require(occurrence_term_histogram == Counter({
        2: 41, 3: 38, 4: 48, 5: 27, 6: 44, 7: 57, 8: 26,
        9: 34, 10: 22, 11: 13, 12: 9, 13: 6, 14: 8, 16: 2,
        17: 1,
    }), ("response-term occurrence histogram changed",
         occurrence_term_histogram))

    return {
        "graphs": tuple(graph_records),
        "incidence_role_degree": tuple(sorted(incidence_counter.items())),
        "stabilizer_orbit_role_degree": tuple(sorted(orbit_counter.items())),
        "stabilizer_orbit_sizes": tuple(sorted(orbit_size_counter.items())),
        "response_cap_histogram": tuple(sorted(occurrence_cap_histogram.items())),
        "response_term_histogram": tuple(
            sorted(occurrence_term_histogram.items())
        ),
        "all_orbits": tuple(all_orbits),
    }


def monomial_names(term):
    kind, tag, factors = term
    answer = [] if tag is None else [("x", tag)]
    answer.extend(("R", factor) for factor in factors)
    return tuple(answer)


def audit_smallest_orbit(orbit_audit):
    """Freeze the first singleton and its response-ideal obstruction.

    In a free tensor algebra, killing a contraction through a block M kills
    a response polynomial for arbitrary companion factors only if every
    physical monomial contains M.  Equivalently, the polynomial lies in the
    coordinate-free ideal generated by the image/contraction factors of M.
    Evaluating M=0 proves the converse.  This is the basis-free divisor
    criterion behind the private-role kernel proof.
    """
    candidates = sorted(
        orbit_audit["all_orbits"],
        key=lambda item: (
            item[1]["size"],
            item[1]["response_term_count"],
            item[1]["response_cap_count"],
            item[1]["role"] != "never-private",
            item[0],
            item[1]["representative"],
        ),
    )
    graph_index, orbit, edges = candidates[0]
    require(graph_index == 1
            and orbit["representative"] == (0, (0, 2))
            and orbit["size"] == 1
            and orbit["role"] == "never-private"
            and orbit["degree_pair"] == (4, 6)
            and orbit["response_cap_count"] == 2
            and orbit["response_term_count"] == 2,
            ("smallest singleton orbit changed", graph_index, orbit))
    adjacency = adjacency_from_edges(edges)
    target = orbit["representative"][1]
    faces = []
    for cap_edge in edges:
        terms = response_terms(adjacency, edges, cap_edge)
        containing = tuple(
            index for index, term in enumerate(terms)
            if target in term[2]
        )
        if not containing:
            continue
        residue = tuple(
            term for term in terms if target not in term[2]
        )
        require(residue,
                ("target unexpectedly divides complete response", cap_edge))
        faces.append({
            "cap_edge": cap_edge,
            "term_count": len(terms),
            "target_term_indices": containing,
            "monomials": tuple(monomial_names(term) for term in terms),
            "target_zero_residue": tuple(
                monomial_names(term) for term in residue
            ),
        })
    require(tuple(
        (item["cap_edge"], item["term_count"],
         len(item["target_term_indices"]),
         len(item["target_zero_residue"]))
        for item in faces
    ) == (((3, 5), 3, 1, 2), ((4, 5), 6, 1, 5)),
            ("minimal response faces changed", faces))
    expected_target_monomials = (
        (("x", (1, 7)), ("R", (0, 2)), ("R", (4, 6))),
        (("x", (1, 7)), ("R", (0, 2)), ("R", (3, 6))),
    )
    actual_target_monomials = tuple(
        item["monomials"][item["target_term_indices"][0]]
        for item in faces
    )
    require(actual_target_monomials == expected_target_monomials,
            ("minimal target monomials changed", actual_target_monomials))

    return {
        "graph_index": graph_index,
        "representative_edges": edges,
        "directed_incidence": orbit["representative"],
        "stabilizer_orbit_size": orbit["size"],
        "response_faces": tuple(faces),
        "basis_free_criterion": (
            "a companion-independent kernel landing through M requires "
            "the complete response polynomial to lie in the contraction "
            "ideal (M), equivalently every free physical monomial contains M"
        ),
        "criterion_result": (
            "fails at caps 35 and 45: setting R02=0 leaves respectively "
            "two and five nonzero free companion monomials"
        ),
        "is_exact_GHZ_counterexample": False,
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
    orbit_audit = audit_orbits()
    smallest = audit_smallest_orbit(orbit_audit)
    # Avoid serializing the redundant edge tuple stored only for the local
    # follow-up lookup.
    orbit_audit = dict(orbit_audit)
    del orbit_audit["all_orbits"]
    ledger = canonical({
        "directed_incidence_orbits": orbit_audit,
        "smallest_orbit_rank_test": smallest,
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("directed incidence response ledger changed", digest))

    print("N=8 support-16 directed response-orbit audit: PASS")
    print("  unlanded directed incidences / stabilizer orbits: 376 / 281")
    print("  shared / never-private incidences: 52 / 324")
    print("  response-visible for another cap: 376 / 376")
    print("  smallest response-sparse orbit: singleton 0->02, two faces")
    print("  private-factor kernel extension: fails response-ideal criterion")


if __name__ == "__main__":
    main()
