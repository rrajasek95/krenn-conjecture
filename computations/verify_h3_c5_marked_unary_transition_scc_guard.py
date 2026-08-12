#!/usr/bin/env python3
r"""Source-labelled transition graph of the marked normalized-C5 unary rows.

For each reset face v, the complete unary word is zero at x and v and is
m=12112 elsewhere.  Relative to either off-cycle base occurrence, its
fourteen mates split as 2 same-reset, 4 translated C4, and 8 translated C6
terms.  Re-pivoting on any mate does not create a new equation: it is the
same complete unary coefficient.  Consequently the co-occurrence graph is
five disjoint 15-vertex components, one for each reset word.

The desired accessibility spoke q_xv^(0,m_v) N belongs to the full-m word,
not to a reset component.  Endpoint response brackets are also absent from
this q-only graph.  A simultaneous cyclotomic specialization leaves a
three-vertex silent component in every reset row, with values 1,w,w^2 and
1+w+w^2=0, while all translated spokes and desired full-m spokes vanish.
This is an exact typed unary counterguard, not a full-source point.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "c0035aea1dda69c7416711cffe672e877a3905156f913d930b9e5b05f3991459"
PINS = {
    "computations/verify_h3_c5_marked_unary_mate_accessibility_boundary.py":
        "8d46d410334fd197ddf96c18a7be32f9109f23b33112b1a773cff5ca1ec99c53",
    "notes/h3-c5-marked-unary-mate-accessibility-boundary.md":
        "112257542550db8143f810f5c05982a78ab82d2352b23d7c77cf61b1ae7e50bc",
    "computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py":
        "c431823ae3d7eed06b0df35f414d069a38f1fba3311a712e3dfce03c230b4016",
    "notes/h3-rootless-c5-universal-ten-tail-typed-quotient.md":
        "d44e8fef499b44e0a91e90a5be465b47c47c138cc43f6f0dcea13237ba16e912",
}

X = 0
ODD = (1, 2, 3, 4, 5)
M = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted(((first, second),) + tail)))
    return tuple(result)


def edge(left, right):
    return tuple(sorted((left, right)))


def reset_word(deleted):
    return tuple(0 if site in (X, deleted) else M[site]
                 for site in (X,) + ODD)


def full_m_word():
    return tuple([0] + [M[site] for site in ODD])


def decorated(matching, word):
    return tuple((left, right, word[left], word[right])
                 for left, right in matching)


def node_label(deleted, matching, word):
    return (
        deleted,
        tuple(decorated(matching, word)),
    )


def strongly_connected_components(vertices, adjacency):
    # Kosaraju, retained explicitly so the exact directed graph rather than
    # an undirected proxy is being certified.
    seen = set()
    order = []

    def visit(vertex):
        seen.add(vertex)
        for following in adjacency[vertex]:
            if following not in seen:
                visit(following)
        order.append(vertex)

    for vertex in vertices:
        if vertex not in seen:
            visit(vertex)

    reverse = {vertex: set() for vertex in vertices}
    for vertex in vertices:
        for following in adjacency[vertex]:
            reverse[following].add(vertex)

    components = []
    seen.clear()
    for start in reversed(order):
        if start in seen:
            continue
        component = []
        queue = [start]
        seen.add(start)
        while queue:
            vertex = queue.pop()
            component.append(vertex)
            for following in reverse[vertex]:
                if following not in seen:
                    seen.add(following)
                    queue.append(following)
        components.append(tuple(component))
    return tuple(components)


def classify_base_transition(deleted, base, mate, word, selected, residual):
    reset = edge(X, deleted)
    common = set(base) & set(mate)
    if reset in mate:
        require(len(common) == 1,
                "a same-reset mate shares an unexpected second edge")
        new_tail = tuple(item for item in mate if item != reset)
        require(new_tail == selected or new_tail in residual,
                "same-reset mate is not one of the three face tails")
        kind = "same_reset_changed_tail"
    else:
        require(len(common) in (0, 1),
                "a translated mate has unexpected overlap")
        kind = "translated_C4" if len(common) == 1 else "translated_C6"
        x_edge = next(item for item in mate if X in item)
        v_edge = next(item for item in mate if deleted in item)
        x_other = x_edge[1]
        v_other = v_edge[0] if v_edge[1] == deleted else v_edge[1]
        require((word[X], word[x_other]) == (0, M[x_other]),
                "translated x-spoke decoration changed")
        require((word[deleted], word[v_other]) == (0, M[v_other]),
                "translated deleted-site spoke decoration changed")

    return {
        "source_row": f"U[{''.join(map(str, word))}]",
        "reset_site": deleted,
        "output_word": "".join(map(str, word)),
        "from_matching": [list(item) for item in base],
        "from_decorated": [list(item) for item in decorated(base, word)],
        "to_matching": [list(item) for item in mate],
        "to_decorated": [list(item) for item in decorated(mate, word)],
        "transition_kind": kind,
        "GHZ_target_readout": 0,
        "endpoint_response_label": "absent (q-only unary coefficient)",
        "ordinary_residue_label": "not an augmented relative column",
    }


def transition_graph():
    vertices = []
    adjacency = defaultdict(set)
    transition_records = []
    classified = Counter()
    row_records = []

    for deleted in ODD:
        word = reset_word(deleted)
        matchings = perfect_matchings((X,) + ODD)
        require(len(matchings) == 15, "a six-site unary row lost a matching")
        labels = [node_label(deleted, matching, word) for matching in matchings]
        vertices.extend(labels)

        # Re-pivoting one complete coefficient on any of its nonzero terms
        # gives the same row.  Thus its source-valid transition relation is
        # the directed complete co-occurrence graph on these fifteen terms.
        for left in labels:
            for right in labels:
                if left != right:
                    adjacency[left].add(right)

        face = tuple(site for site in ODD if site != deleted)
        face_matchings = perfect_matchings(face)
        selected = next(matching for matching in face_matchings
                        if set(matching) <= CYCLE)
        residual = tuple(matching for matching in face_matchings
                         if matching != selected)
        bases = tuple(tuple(sorted((edge(X, deleted),) + tail))
                      for tail in residual)
        require(len(bases) == 2, "a face lost an off-cycle unary base")
        for base in bases:
            require(base in matchings, "an off-cycle base left its unary row")
            for mate in matchings:
                if mate == base:
                    continue
                record = classify_base_transition(
                    deleted, base, mate, word, selected, residual
                )
                transition_records.append(record)
                classified[record["transition_kind"]] += 1

        row_records.append({
            "source_row": f"U[{''.join(map(str, word))}]",
            "reset_site": deleted,
            "output_word": "".join(map(str, word)),
            "term_count": len(matchings),
            "off_cycle_base_count": len(bases),
            "target_readout": 0,
            "source_grade_invariant": f"site {deleted} remains colour 0",
        })

    require(len(vertices) == len(set(vertices)) == 75,
            "the five reset rows stopped having 75 distinct typed terms")
    require(len(transition_records) == 10 * 14,
            "the ten-base transition inventory changed")
    require(classified == Counter({
        "same_reset_changed_tail": 20,
        "translated_C4": 40,
        "translated_C6": 80,
    }), f"the 20/40/80 transition split changed: {classified}")
    require(sum(len(adjacency[vertex]) for vertex in vertices) == 5 * 15 * 14,
            "the repeated-row co-occurrence edge count changed")

    components = strongly_connected_components(tuple(vertices), adjacency)
    require(sorted(map(len, components)) == [15] * 5,
            "the marked unary graph lost its five 15-term SCCs")
    require(all(len({vertex[0] for vertex in component}) == 1
                for component in components),
            "a unary SCC crossed a reset word")

    desired_word = full_m_word()
    require(desired_word not in {reset_word(deleted) for deleted in ODD},
            "the desired accessibility word entered a reset component")
    desired_spokes = {
        (X, deleted, 0, M[deleted]) for deleted in ODD
    }
    reset_spokes = {
        (X, deleted, 0, 0) for deleted in ODD
    }
    require(desired_spokes.isdisjoint(reset_spokes),
            "desired and marked reset spokes collided")

    return {
        "rows": row_records,
        "vertices": len(vertices),
        "directed_repeated_row_edges": sum(len(adjacency[v]) for v in vertices),
        "strong_components": [
            {
                "reset_site": component[0][0],
                "size": len(component),
                "output_word": "".join(map(str, reset_word(component[0][0]))),
            }
            for component in sorted(components, key=lambda c: c[0][0])
        ],
        "classified_base_transitions": transition_records,
        "classified_counts": dict(sorted(classified.items())),
        "desired_output_word": "".join(map(str, desired_word)),
        "desired_spokes": [list(item) for item in sorted(desired_spokes)],
        "desired_word_reachable": False,
        "endpoint_response_bracket_present": False,
        "graph_invariant": (
            "every edge is co-occurrence inside one literal complete unary "
            "coefficient and preserves its reset site/output word"
        ),
    }


def cyclotomic_silent_guard():
    # Store a unit as its exponent of w in Z/3; w^3=1 and 1+w+w^2=0.
    edge_exponent = {}
    for left in ODD:
        for right in ODD:
            if left < right:
                edge_exponent[(left, right)] = 0 if (left, right) in CYCLE else 1

    records = []
    all_active = []
    for deleted in ODD:
        word = reset_word(deleted)
        face = tuple(site for site in ODD if site != deleted)
        face_matchings = perfect_matchings(face)
        values = []
        active_nodes = []
        for matching in face_matchings:
            exponent = sum(edge_exponent[item] for item in matching) % 3
            values.append(exponent)
            active = tuple(sorted((edge(X, deleted),) + matching))
            active_nodes.append(node_label(deleted, active, word))
        require(sorted(values) == [0, 1, 2],
                "a cyclotomic face stopped having values 1,w,w^2")
        all_active.extend(active_nodes)
        records.append({
            "reset_site": deleted,
            "source_row": f"U[{''.join(map(str, word))}]",
            "active_matching_values": [f"w^{value}" for value in values],
            "row_sum": "1+w+w^2=0",
            "active_component_size": len(active_nodes),
            "cycle_holonomy": "w*w*w=w^3=1",
        })

    require(len(all_active) == len(set(all_active)) == 15,
            "the five cyclotomic silent triangles collided")

    # All q_(xr)^(0,m_r) spokes are zero.  Hence every reset-moving C4/C6
    # term is zero, including every desired full-m q_(xv)^(0,m_v) spoke.
    translated_spokes = {
        (X, bright, 0, M[bright]) for bright in ODD
    }
    desired_spokes = set(translated_spokes)
    return {
        "coefficient_ring": "Z[w]/(w^2+w+1)",
        "selected_C5_edges": "1",
        "off_cycle_chords": "w",
        "marked_reset_spokes_q_xv_00": "1",
        "translated_spokes_q_xr_0m": "0",
        "desired_full_m_spokes": "0",
        "endpoint_star_components": "0 (typing guard only)",
        "active_vertices": len(all_active),
        "active_strong_components": 5,
        "active_component_sizes": [3] * 5,
        "faces": records,
        "all_five_marked_unary_rows_vanish": True,
        "all_ten_off_cycle_tail_values_nonzero": True,
        "translated_C4_C6_terms_vanish": True,
        "desired_spoke_or_response_visibility_forced": False,
    }


def main() -> None:
    pin_dependencies()
    graph = transition_graph()
    guard = cyclotomic_silent_guard()
    ledger = {
        "pins": PINS,
        "source_labelled_transition_graph": graph,
        "cyclotomic_silent_SCC_guard": guard,
        "verdict": (
            "repeated marked complete unary rows form five closed 15-term "
            "reset-word SCCs and do not force a full-m decorated spoke, an "
            "endpoint-visible response row, or a source-valid offanchor/Hall "
            "exit; a simultaneous 1,w,w^2 specialization leaves five silent "
            "active triangles"
        ),
        "scope": (
            "finite exact h=3 q-only marked-unary transition theorem; the "
            "cyclotomic specialization is a typed partial guard, not a full "
            "unary/four-response source, and q-incidence alone is not used "
            "to infer endpoint activity, goodness, or Hall routing"
        ),
        "minimal_new_input": (
            "one complete endpoint word-change/spoke-to-hole row changing "
            "the reset colour 0 at v to m_v while preserving the decorated "
            "tail, or an independently active response bracket at (x,v)"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"marked unary transition SCC ledger changed: {digest}")
    print("h3 C5 marked unary transition SCC guard: PASS")
    print("vertices=75 SCCs=5x15 repeated_row_edges=1050")
    print("classified=20 same-reset + 40 translated-C4 + 80 translated-C6")
    print("cyclotomic active guard=5xK3; desired spoke/response forced: no")
    print("ledger_sha256=", digest, sep="")


if __name__ == "__main__":
    main()
