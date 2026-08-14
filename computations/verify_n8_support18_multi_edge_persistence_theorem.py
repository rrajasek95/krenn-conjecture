#!/usr/bin/env python3
"""Prove framed two-edge persistence through support 18.

The support-17 theorem has three witness mechanisms: private contraction
ideal, singleton/pure row, and complementary binary cap.  None is formally
monotone under a second edge addition.  This checker forms every directed
support-18 descendant of the 502 nonprivate support-17 link types, quotients
by directed graph isomorphism, and proves by exact finite-domain solving that
no full-support coordinate-anchor chart simultaneously avoids every
mechanism.  The solver assertion for each mixed word is its literal decorated
matching-occurrence multiplicity not being one.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "ca0c641fb16ef47aa1cb6a3220556b1e34a95de5f5e413324217f969f2a9eabb"
N = 8


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


ANCHOR = load_local(
    "n8_support17_anchor_for_support18_first_guard",
    "verify_n8_support17_hard_landed_parent_anchor_closure.py",
)
BINARY = ANCHOR.BINARY
PERSIST = ANCHOR.PERSIST
PROTOTYPE = ANCHOR.PROTOTYPE
ORBIT = ANCHOR.ORBIT


PINNED_DEPENDENCIES = {
    "support17-anchor-closure": (
        ANCHOR,
        "2a5e85d8b4863bcf9c9f2a95229642b9f6531cdfd7e8bc7e5b8f6fdfd03dceb0",
    ),
    "support17-persistence-register": (
        PERSIST,
        "005230a4aed405107975d9eda404ef2949be10f36fd191a5468cf6eb707b0e45",
    ),
    "support16-binary-landing": (
        BINARY,
        "7c3e00333001f5beb18b0f5538ac96885e556f153ca3459d02873221b132d20c",
    ),
}


def audit_dependency_pins():
    ledger = []
    for name, (module, expected) in PINNED_DEPENDENCIES.items():
        require(module.EXPECTED_SHA256 == expected,
                ("support18 dependency pin changed", name,
                 module.EXPECTED_SHA256, expected))
        ledger.append((name, expected))
    return tuple(sorted(ledger))


def canonical_descendants():
    parents = ANCHOR.hard_directed_types()
    require(len(parents) == 502,
            ("support17 directed type count changed", len(parents)))
    all_edges = {
        (left, right)
        for left in range(N) for right in range(left + 1, N)
    }
    descendants = {}
    multiplicity = Counter()
    for parent_index, item in enumerate(parents):
        parent_edges = tuple(tuple(edge) for edge in item["augmented_edges"])
        for second_edge in sorted(all_edges - set(parent_edges)):
            support18 = tuple(sorted(parent_edges + (second_edge,)))
            key = PERSIST.canonical_directed_key(
                support18, tuple(item["incidence"])
            )
            multiplicity[key] += 1
            descendants.setdefault(key, {
                "parent_type_index": parent_index,
                "parent_route": item["parent_route"],
                "parent_edges": parent_edges,
                "parent_incidence": tuple(item["incidence"]),
                "first_added_edge": tuple(item["new_edge"]),
                "second_added_edge": second_edge,
            })
    require(sum(multiplicity.values()) == 502 * 11,
            ("support18 descendant entry count changed",
             sum(multiplicity.values())))
    return tuple(
        {
            "canonical_edges": key,
            "canonical_incidence": (0, (0, 1)),
            "descendant_multiplicity": multiplicity[key],
            **descendants[key],
        }
        for key in sorted(descendants)
    )


def response_data(edges, incidence):
    adjacency = ORBIT.adjacency_from_edges(edges)
    shapes = []
    private_caps = []
    for cap_edge in edges:
        if incidence[0] not in cap_edge:
            continue
        through, residue = PROTOTYPE.cap_shape(
            adjacency, edges, incidence, cap_edge
        )
        if not through:
            continue
        shapes.append((cap_edge, len(through), len(residue)))
        if not residue:
            private_caps.append(cap_edge)
    faces = BINARY.binary_faces(
        adjacency, edges, incidence, tuple(shapes)
    )
    return tuple(shapes), tuple(private_caps), tuple(faces)


def smt_and(items):
    items = tuple(items)
    if not items:
        return "true"
    if len(items) == 1:
        return items[0]
    return f"(and {' '.join(items)})"


def smt_or(items):
    items = tuple(items)
    if not items:
        return "false"
    if len(items) == 1:
        return items[0]
    return f"(or {' '.join(items)})"


def multi_matching_word_histogram(matchings, states, nonanchor_supports):
    words = Counter()
    for matching in matchings:
        choices = tuple(
            (nonanchor_supports[edge] if edge in nonanchor_supports
             else (states[edge],))
            for edge in matching
        )
        for colours in product(*choices):
            word = [None] * N
            for edge, colour in zip(matching, colours):
                word[edge[0]] = colour
                word[edge[1]] = colour
            require(None not in word,
                    ("multi-nonanchor word left a site blank", matching,
                     colours))
            words[tuple(word)] += 1
    return words


def exact_smt_occurrence_completion(edges, faces, nonanchor_supports,
                                    zero_coordinate, symmetry,
                                    timeout_seconds=30):
    """Solve the full-support occurrence guard CSP with Z3.

    For each possible decorated word, its multiplicity is the sum of Boolean
    perfect-matching occurrence conditions.  Requiring that sum not equal to
    one is exactly the absence of mixed singleton fibres.
    """
    edge_set = set(edges)
    nonanchor_supports = {
        tuple(edge): tuple(support)
        for edge, support in nonanchor_supports.items()
    }
    require(set(nonanchor_supports).issubset(edge_set),
            ("nonanchor outside support18 graph", nonanchor_supports, edges))
    anchor_edges = tuple(
        edge for edge in edges if edge not in nonanchor_supports
    )
    require(anchor_edges, ("support18 chart has no coordinate anchors", edges,
                           nonanchor_supports))
    variable = {edge: f"x{index}" for index, edge in enumerate(anchor_edges)}
    matchings = tuple(
        matching
        for raw in ORBIT.BASE.perfect_matchings(tuple(range(N)))
        for matching in (tuple(tuple(sorted(edge)) for edge in raw),)
        if all(edge in edge_set for edge in matching)
    )
    require(matchings, ("support18 graph has no perfect matching", edges))

    word_occurrences = {}
    for matching in matchings:
        choices = tuple(
            nonanchor_supports.get(edge, range(3)) for edge in matching
        )
        for colours in product(*choices):
            assigned = dict(zip(matching, colours))
            word = [None] * N
            for edge in matching:
                colour = assigned[edge]
                word[edge[0]] = colour
                word[edge[1]] = colour
            require(None not in word,
                    ("SMT occurrence left a site blank", matching, assigned))
            constraints = tuple(sorted(
                (variable[edge], assigned[edge]) for edge in matching
                if edge in variable
            ))
            word_occurrences.setdefault(tuple(word), []).append(constraints)

    lines = ["(set-logic QF_LIA)", "(set-option :produce-models true)"]
    for name in variable.values():
        lines.append(f"(declare-const {name} Int)")
        lines.append(f"(assert (and (<= 0 {name}) (<= {name} 2)))")
    if symmetry == "full":
        # Full target support has the complete S3 frame symmetry.
        lines.append(f"(assert (= {variable[anchor_edges[0]]} 0))")
    elif symmetry == "missing-zero":
        # Missing colour zero leaves only the transposition 1<->2.  The first
        # anchor therefore has two inequivalent classes: zero and nonzero.
        lines.append(f"(assert (<= {variable[anchor_edges[0]]} 1))")
    else:
        require(symmetry == "none", ("unknown colour symmetry", symmetry))

    # Every site sees the complete framed coordinate support among anchors.
    for vertex in range(N):
        incident = tuple(edge for edge in anchor_edges if vertex in edge)
        for colour in range(3):
            if colour == zero_coordinate:
                continue
            lines.append("(assert " + smt_or(
                f"(= {variable[edge]} {colour})" for edge in incident
            ) + ")")

    # Avoid each exact complementary crossed-binary landing.
    for face in faces:
        relevant_edges = ((face["cap_edge"],)
                          + face["p_shore_edges"] + face["q_shore_edges"])
        if not all(edge in variable for edge in relevant_edges):
            # The rank-two binary theorem needs literal coordinate factors on
            # all five displayed roles.  A nonanchor role is not a landing.
            continue
        direct = variable[face["cap_edge"]]
        p0, p1 = (variable[edge] for edge in face["p_shore_edges"])
        q0, q1 = (variable[edge] for edge in face["q_shore_edges"])
        landings = []
        for colour in range(3):
            first, second = tuple(sorted(set(range(3)) - {colour}))
            p_cross = smt_or((
                smt_and((f"(= {p0} {first})", f"(= {p1} {second})")),
                smt_and((f"(= {p0} {second})", f"(= {p1} {first})")),
            ))
            q_cross = smt_or((
                smt_and((f"(= {q0} {first})", f"(= {q1} {second})")),
                smt_and((f"(= {q0} {second})", f"(= {q1} {first})")),
            ))
            landings.append(smt_and(
                (f"(= {direct} {colour})", p_cross, q_cross)
            ))
        lines.append(f"(assert (not {smt_or(landings)}))")

    pure_words = {tuple([colour] * N) for colour in range(3)}
    for word in sorted(pure_words):
        if word not in word_occurrences:
            lines.append("(assert false)")
    for word, occurrences in sorted(word_occurrences.items()):
        terms = []
        for constraints in occurrences:
            condition = smt_and(
                f"(= {name} {colour})" for name, colour in constraints
            )
            terms.append(f"(ite {condition} 1 0)")
        total = terms[0] if len(terms) == 1 else f"(+ {' '.join(terms)})"
        if word in pure_words:
            lines.append(f"(assert (>= {total} 1))")
        elif len(set(word)) > 1:
            lines.append(f"(assert (not (= {total} 1)))")
    lines.extend(("(check-sat)", "(get-model)"))
    completed = subprocess.run(
        ("z3", "-in", f"-T:{timeout_seconds}"),
        input="\n".join(lines), text=True, capture_output=True,
        check=False,
    )
    output = completed.stdout
    first = output.splitlines()[0].strip() if output.splitlines() else ""
    require(first in ("sat", "unsat", "unknown"),
            ("unexpected z3 result", completed.returncode,
             completed.stdout[-2000:], completed.stderr[-2000:]))
    if first != "sat":
        return first, None, {
            "matching_count": len(matchings),
            "word_constraint_count": len(word_occurrences),
            "smt_bytes": sum(len(line) + 1 for line in lines),
        }
    assignments = {
        name: int(value)
        for name, value in re.findall(
            r"\(define-fun\s+(x\d+)\s+\(\)\s+Int\s+(-?\d+)\s*\)",
            output,
        )
    }
    require(set(assignments) == set(variable.values()),
            ("incomplete z3 model", assignments, variable, output[-2000:]))
    states = {edge: assignments[name] for edge, name in variable.items()}
    words = multi_matching_word_histogram(
        matchings, states, nonanchor_supports
    )
    pure = tuple(words[(colour,) * N] for colour in range(3))
    singletons = tuple(
        word for word, multiplicity in words.items()
        if len(set(word)) > 1 and multiplicity == 1
    )
    require(all(pure) and not singletons,
            ("z3 model failed exact occurrence check", pure, singletons,
             states))
    require(not any(
        all(edge in states for edge in (
            (face["cap_edge"],)
            + face["p_shore_edges"] + face["q_shore_edges"]
        )) and BINARY.face_lands(face, states, zero_coordinate)
        for face in faces
    ), ("z3 model retained binary landing", faces, states))
    return first, {
        "completion": tuple(sorted(states.items())),
        "pure_support": pure,
        "word_histogram": tuple(sorted(words.items())),
    }, {
        "matching_count": len(matchings),
        "word_constraint_count": len(word_occurrences),
        "smt_bytes": sum(len(line) + 1 for line in lines),
    }


def audit_all_smt_occurrence_guards(descendants):
    outcomes = Counter()
    solver_stats = Counter()
    for type_index, item in enumerate(descendants):
        edges = tuple(item["canonical_edges"])
        incidence = tuple(item["canonical_incidence"])
        shapes, private_caps, faces = response_data(edges, incidence)
        if private_caps:
            outcomes["private-cap"] += 1
            continue
        for chart_name, target_support, zero_coordinate in (
                ("support-two", (1, 2), 0),
                ("support-three", (0, 1, 2), None)):
            status, witness, statistics = exact_smt_occurrence_completion(
                edges, faces, {incidence[1]: target_support},
                zero_coordinate,
                "missing-zero" if zero_coordinate == 0 else "full",
            )
            outcomes[(chart_name, f"z3-{status}")] += 1
            solver_stats[(chart_name, "matching_count")] += statistics[
                "matching_count"
            ]
            solver_stats[(chart_name, "word_constraint_count")] += statistics[
                "word_constraint_count"
            ]
            solver_stats[(chart_name, "smt_bytes")] += statistics["smt_bytes"]
            require(status != "unknown",
                    ("z3 timed out on support18 directed type", type_index,
                     chart_name, statistics))
            if witness is None:
                continue
            words = dict(witness["word_histogram"])
            multiplicities = Counter(
                value for word, value in words.items()
                if len(set(word)) > 1
            )
            guard = {
                "directed_type_index": type_index,
                "chart": chart_name,
                "canonical_edges": edges,
                "canonical_incidence": incidence,
                "response_shapes": shapes,
                "binary_faces": faces,
                **witness,
                "mixed_multiplicity_histogram": tuple(sorted(
                    multiplicities.items()
                )),
                "ancestry": {
                    key: value for key, value in item.items()
                    if key not in ("canonical_edges", "canonical_incidence")
                },
                "prefix_outcomes": tuple(sorted(outcomes.items())),
                "solver_statistics": tuple(sorted(solver_stats.items())),
                "status": (
                    "exact occurrence guard; coefficient cancellation of "
                    "the multi-occurrence fibres remains to be solved"
                ),
            }
            return {
                "outcomes": tuple(sorted(outcomes.items())),
                "solver_statistics": tuple(sorted(solver_stats.items())),
                "necessary_guard": guard,
            }
    return {
        "outcomes": tuple(sorted(outcomes.items())),
        "solver_statistics": tuple(sorted(solver_stats.items())),
        "necessary_guard": None,
    }


def audit_full_support_three_nonanchor_probe(descendants):
    """Test one marked two-edge ancestry per unmarked directed type.

    This is the first genuinely multi-block chart: the target and both added
    edges have full noncoordinate support.  A SAT result is a sharp guard to
    extending the coordinate-anchor theorem; UNSAT is only a marked probe,
    not yet an exhaustion of every support assignment and ancestry.
    """
    outcomes = Counter()
    for type_index, item in enumerate(descendants):
        edges = tuple(sorted(
            tuple(item["parent_edges"]) + (tuple(item["second_added_edge"]),)
        ))
        incidence = tuple(item["parent_incidence"])
        first_edge = tuple(item["first_added_edge"])
        second_edge = tuple(item["second_added_edge"])
        require(first_edge != second_edge
                and first_edge != incidence[1]
                and second_edge != incidence[1],
                ("marked support18 edges collide", item))
        shapes, private_caps, faces = response_data(edges, incidence)
        require(not private_caps,
                ("nonprivate support17 type acquired a private cap", item,
                 private_caps))
        supports = {
            incidence[1]: (0, 1, 2),
            first_edge: (0, 1, 2),
            second_edge: (0, 1, 2),
        }
        status, witness, statistics = exact_smt_occurrence_completion(
            edges, faces, supports, None, "full"
        )
        outcomes[f"z3-{status}"] += 1
        require(status != "unknown",
                ("three-nonanchor probe timed out", type_index, statistics))
        if witness is not None:
            return {
                "outcomes": tuple(sorted(outcomes.items())),
                "necessary_guard": {
                    "directed_type_index": type_index,
                    "parent_route": item["parent_route"],
                    "edges": edges,
                    "incidence": incidence,
                    "first_added_edge": first_edge,
                    "second_added_edge": second_edge,
                    "nonanchor_supports": tuple(sorted(supports.items())),
                    "response_shapes": shapes,
                    "binary_faces": faces,
                    **witness,
                    "solver_statistics": tuple(sorted(statistics.items())),
                    "status": (
                        "exact source-labelled occurrence guard to the "
                        "coordinate-anchor support18 theorem; coefficient "
                        "cancellation remains unproved"
                    ),
                },
            }
    return {
        "outcomes": tuple(sorted(outcomes.items())),
        "necessary_guard": None,
    }


def audit_nonmonotonicity_logic():
    """Record why no potential on the three certificate sets is monotone."""
    transitions = (
        {
            "certificate": "private contraction ideal",
            "repair": (
                "a later response increment may lie outside I_X, so the "
                "old kernel does not annihilate the augmented response"
            ),
        },
        {
            "certificate": "singleton debt set",
            "repair": (
                "a later edge link may contain the last singleton word and "
                "raise its occurrence multiplicity from one to two"
            ),
        },
        {
            "certificate": "complementary binary face",
            "repair": (
                "a later edge may add a third star-zero residue monomial, "
                "so the crossed 2x2 permanent identity no longer closes it"
            ),
        },
    )
    return {
        "transitions": transitions,
        "conclusion": (
            "the tuple (private ideal membership, singleton set, one-edge "
            "link support) has no componentwise well-founded monotonicity; "
            "multi-edge persistence requires new response information"
        ),
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
    descendants = canonical_descendants()
    audit = audit_all_smt_occurrence_guards(descendants)
    require(audit["necessary_guard"] is None,
            ("support18 occurrence guard survived the framed exits",
             audit["necessary_guard"]))
    outcome_counts = dict(audit["outcomes"])
    require(sum(outcome_counts.values()) == 2 * len(descendants),
            ("support18 outcome partition incomplete", outcome_counts,
             len(descendants)))
    three_nonanchor_probe = audit_full_support_three_nonanchor_probe(
        descendants
    )
    ledger = canonical({
        "dependency_pins": audit_dependency_pins(),
        "nonmonotonicity": audit_nonmonotonicity_logic(),
        "support17_parent_types": 502,
        "support18_descendant_entries": 502 * 11,
        "support18_directed_types": len(descendants),
        "descendant_multiplicity_histogram": tuple(sorted(Counter(
            item["descendant_multiplicity"] for item in descendants
        ).items())),
        "exact_occurrence_audit": audit,
        "full_support_three_nonanchor_probe": three_nonanchor_probe,
        "theorem": (
            "every two- or three-target-support coordinate-anchor support18 "
            "descendant of the 502 support17 directed link types has a "
            "private cap, complementary binary cap, missing normalized "
            "pure row, or mixed singleton fibre"
        ),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("support18 first-guard ledger changed", digest))
    print("N=8 support-18 multi-edge persistence audit: PASS")
    print("  directed descendants:", len(descendants))
    print("  outcome partition:", audit["outcomes"])
    print("  necessary occurrence guards: 0")
    print("  three-nonanchor marked probe guard:",
          three_nonanchor_probe["necessary_guard"] is not None)


if __name__ == "__main__":
    main()
