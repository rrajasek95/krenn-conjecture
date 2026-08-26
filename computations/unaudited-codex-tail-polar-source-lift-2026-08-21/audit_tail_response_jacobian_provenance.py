#!/usr/bin/env python3
"""Audit whether the frozen 380x12 tail matrix is a global Jacobian block."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_tail_response_jacobian_provenance.json"
UPSTREAM = HERE / "results_tail_polar_source_lift.json"
RESCUE = HERE / "results_tail_response_rescue_theorem.json"
SUPPORT = HERE / "results_tail_support_boundary_orbits.json"
FILTERED = (HERE.parent / "unaudited-codex-tail-filtered-lift-obstruction-2026-08-21"
            / "results_tail_filtered_lift_obstruction.json")
PINS = {
    UPSTREAM: "b97ef0b72d6e87ed3f1ffc61de4b5e237a71423fa31f47afd79b2e4ee64abbef",
    RESCUE: "d532c624f0076868d58e09e8725b1755379fddaf7ceb780cb6a5c007e4ca7087",
    SUPPORT: "747f27617f023a1b718a01205afac7411900ccf093e8518c4ff5103aab82dca3",
    FILTERED: "51a282ba6e866693cc12c5fafc73d77e12f3a437823cae4e54d6b85fa041604c",
}
SITES = tuple(range(8))
COLOURS = tuple(range(3))
WANTED = {(7, 1), (6, 1, 1), (3, 3, 2)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def normalized_cell(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


def canonical_column(name):
    require(name[0] in "yz", name)
    residual = int(name[1:])
    tail = 6 if name[0] == "y" else 7
    return normalized_cell(residual, tail, 0, 1)


def diagonal_derivative_terms(word, coordinate):
    u, v, a, b = coordinate
    if word[u] != a or word[v] != b:
        return ()
    residual = tuple(site for site in SITES if site not in (u, v))
    answer = []
    for matching in perfect_matchings(residual):
        if not all(word[x] == word[y] for x, y in matching):
            continue
        answer.append(tuple(sorted((word[x], x, y) for x, y in matching)))
    return tuple(sorted(answer))


def canonical_provenance(upstream):
    ledger = upstream["row_ledger"]
    require(len(ledger) == 380, len(ledger))
    occurrences = 0
    nonzero_entries = 0
    profile_entries = Counter()
    provenance = []
    all_columns = tuple(canonical_column(name)
                        for name in upstream["retained_star_columns"])
    for record in ledger:
        word = tuple(map(int, record["source_label"][2:]))
        expected = {}
        for name, coordinate in zip(upstream["retained_star_columns"],
                                    all_columns, strict=True):
            terms = diagonal_derivative_terms(word, coordinate)
            if terms:
                expected[name] = terms
                occurrences += len(terms)
        actual_names = set(record["nonzero_columns"])
        require(set(expected) == actual_names,
                (record["source_label"], set(expected), actual_names))
        nonzero_entries += len(expected)
        profile_entries[record["profile"]] += len(expected)
        provenance.append({
            "global_J_row": record["source_label"],
            "global_J_columns": [list(canonical_column(name))
                                 for name in sorted(expected)],
            "diagonal_specialization_monomial_count":
                sum(len(terms) for terms in expected.values()),
        })
    require(occurrences == 1620, occurrences)
    return {
        "canonical_rows": len(ledger),
        "canonical_columns": len(all_columns),
        "nonzero_matrix_entries": nonzero_entries,
        "literal_matching_occurrences": occurrences,
        "nonzero_entries_by_profile": dict(sorted(profile_entries.items())),
        "row_column_map": provenance,
        "identity": (
            "M_380x12(w,e) = (partial F_w / partial A_e) evaluated after "
            "setting every cross-colour source cell T to zero."
        ),
    }


def transported_column_census():
    # Transport the canonical cut columns by every site choice and every
    # ordered colour pair. The companion tail vertex records the 12-fold
    # overlap of the fixed-pair slices.
    multiplicity = Counter()
    for p, q in combinations(SITES, 2):
        tail_pair = (p, q)
        for residual in (site for site in SITES if site not in tail_pair):
            for tail in tail_pair:
                for a, b in product(COLOURS, repeat=2):
                    if a == b:
                        continue
                    multiplicity[normalized_cell(residual, tail, a, b)] += 1
    off_diagonal = tuple((u, v, a, b)
                         for u, v in combinations(SITES, 2)
                         for a, b in product(COLOURS, repeat=2) if a != b)
    require(set(multiplicity) == set(off_diagonal),
            (len(multiplicity), len(off_diagonal)))
    require(set(multiplicity.values()) == {12},
            Counter(multiplicity.values()))
    return off_diagonal, multiplicity


def global_structural_screen(off_diagonal):
    # Each 6+1+1 word is the unique pivot row for one off-diagonal cell:
    # the other six sites have the third colour. This gives a literal
    # 168x168 Jacobian minor whose T=0 specialization is diagonal.
    pivot_rows = {}
    for coordinate in off_diagonal:
        u, v, a, b = coordinate
        third = next(colour for colour in COLOURS if colour not in (a, b))
        word = [third] * 8
        word[u], word[v] = a, b
        word = tuple(word)
        require(profile(word) == (6, 1, 1), word)
        require(word not in pivot_rows, (word, coordinate, pivot_rows.get(word)))
        pivot_rows[word] = coordinate
    require(len(pivot_rows) == 168, len(pivot_rows))

    selected_rows = [word for word in product(COLOURS, repeat=8)
                     if profile(word) in WANTED]
    adjacency = {}
    for word in selected_rows:
        neighbours = []
        for coordinate in off_diagonal:
            if diagonal_derivative_terms(word, coordinate):
                neighbours.append(coordinate)
        if neighbours:
            adjacency[word] = tuple(neighbours)

    # Deterministic bipartite matching; the singleton 611 rows already
    # exhibit the perfect column matching, but replay the full support graph.
    match = {}

    def augment(row, seen):
        for column in adjacency[row]:
            if column in seen:
                continue
            seen.add(column)
            if column not in match or augment(match[column], seen):
                match[column] = row
                return True
        return False

    matching = 0
    for row in sorted(adjacency):
        matching += int(augment(row, set()))
    require(matching == 168, matching)

    return {
        "transported_distinct_off_diagonal_columns": len(off_diagonal),
        "transported_slice_occurrences": 2016,
        "multiplicity_of_each_column_across_fixed_pair_slices": 12,
        "selected_profile_global_rows_with_nonzero_T0_derivative":
            len(adjacency),
        "maximum_support_matching": matching,
        "generic_T0_specialized_rank": 168,
        "rank_upper_bound_from_column_count": 168,
        "explicit_lower_minor": (
            "Use all 168 profile-6+1+1 words. For coordinate "
            "A_uv[a,b], a!=b, the pivot word has colours a,b at u,v and "
            "the third colour on the other six sites. The T=0 determinant "
            "is product_(uv,a!=b) Haf(G_third on V\\{u,v}), a nonzero "
            "polynomial over the independent diagonal-graph field."
        ),
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def build_result(mutate=False):
    for path, digest in PINS.items():
        require(file_sha(path) == digest, (str(path), file_sha(path), digest))
    upstream = json.loads(UPSTREAM.read_text())
    rescue = json.loads(RESCUE.read_text())
    support = json.loads(SUPPORT.read_text())
    filtered = json.loads(FILTERED.read_text())
    require(rescue["tail_missing_pattern_orbits"] == 126,
            rescue["tail_missing_pattern_orbits"])
    require("No tail-response divisor remains" in support["remaining_global_work"],
            support["remaining_global_work"])
    require("associated-graded" in upstream["scope_guard"],
            upstream["scope_guard"])
    require("formal/local implicit solvability" in filtered["scope_verdict"],
            filtered["scope_verdict"])

    canonical = canonical_provenance(upstream)
    if mutate:
        canonical["literal_matching_occurrences"] -= 1
    require(canonical["literal_matching_occurrences"] == 1620, canonical)
    off_diagonal, multiplicity = transported_column_census()
    global_screen = global_structural_screen(off_diagonal)

    payload = {
        "status": "PASS exact provenance; terminal 168-column/associated-graded obstruction",
        "canonical_380x12_provenance": canonical,
        "global_transport_screen": global_screen,
        "literal_vs_associated_graded": {
            "six_one_one_pivot": (
                "The displayed pivot entry itself is a literal global "
                "Jacobian coefficient: differentiating the two singleton "
                "sites leaves a monochromatic six-site Hafnian. The 168 "
                "transported pivots therefore define a genuine global "
                "Jacobian minor polynomial, generically nonzero."
            ),
            "full_380x12_matrix": (
                "Not a literal global Jacobian block away from T=0. Its "
                "3+3+2 entries retain only the diagonal matching in the "
                "six-site derivative cofactor and discard higher-tail "
                "matching terms. It is exactly J specialized at T=0, or "
                "equivalently the tail-degree-zero part of those J entries."
            ),
            "lex_first_discarded_J_term": {
                "row": "F_00011212",
                "column": "A_06[0,1] (y0)",
                "retained_T0_term": "A_12[0,0]*A_34[1,1]*A_57[2,2]",
                "discarded_full_J_term": "A_12[0,0]*A_35[1,2]*A_47[1,2]",
                "meaning": (
                    "The discarded term is present in partial F_00011212 / "
                    "partial A_06[0,1] and vanishes only after T=0."
                ),
            },
        },
        "quotient_by_T0": {
            "at_diagonal_source": (
                "Every off-diagonal source coordinate is zero, so every "
                "T0 orbit tangent G_A(X) is supported in the 84 diagonal "
                "source coordinates. The 168 tail columns are disjoint "
                "from im(G_A); quotienting by im(G_A) leaves their rank "
                "and their 168-column cap unchanged."
            ),
            "tail_rank_mod_imG_upper_bound": 168,
            "required_direct_contradiction_rank_minus_s": 232,
            "gap": 64,
        },
        "closure_scope": {
            "fixed_tail_missing_pattern_orbits": 126,
            "support_factor_result": support["terminal_tail_boundary_theorem"],
            "what_it_proves": (
                "The rescue/support closure controls rank loss of the "
                "associated-graded 12-column slices on the normalized "
                "diagonal chart. It neither promotes the 3+3+2 leading "
                "coefficients to the full J at T!=0 nor excludes the remote "
                "tail components isolated by the filtered-lift obstruction."
            ),
        },
        "terminal_obstruction": (
            "Even granting every transported slice at full rank, their union "
            "has only the 168 off-diagonal source columns. Hence they can "
            "contribute at most 168 to rank(J) modulo im(G), strictly below "
            "the direct target rank(J)-s>=232. Adding the 84 diagonal columns "
            "is a logically new block; at an exact GHZ point its quotient "
            "dimension is only 63+s, and equivariance caps the entire quotient "
            "rank at 231+s. No sum of the frozen tail slice ranks proves the "
            "forbidden extra rank."
        ),
        "smallest_missing_coefficient_target": (
            "There is no useful 232+s tail minor to verify. The smallest "
            "nonlinear promotion target would instead be a saturation proving "
            "that the global X5+blocked ideal forces T=0; only then may the "
            "literal 168x168 profile-611 minor be combined with a separately "
            "audited diagonal quotient-Jacobian block. The frozen filtered "
            "audit gives an explicit remote-component obstruction to this "
            "promotion."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-occurrence-count", action="store_true")
    args = parser.parse_args()
    payload = build_result(args.mutate_occurrence_count)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("transport rank/cap",
          payload["global_transport_screen"]["generic_T0_specialized_rank"],
          payload["global_transport_screen"]["rank_upper_bound_from_column_count"])
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
