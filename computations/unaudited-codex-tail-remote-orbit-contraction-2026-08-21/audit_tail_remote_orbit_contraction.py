#!/usr/bin/env python3
"""Orbit-graded low-degree contraction screen for the remote tail branch."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_tail_remote_orbit_contraction.json"
TAIL_RESULT = (HERE.parent /
    "unaudited-codex-tail-polar-source-lift-2026-08-21" /
    "results_tail_polar_source_lift.json")
V = tuple(range(8))
COLORS = (0, 1, 2)
CELLS = tuple((u, v, i, j) for u, v in combinations(V, 2)
              for i in COLORS for j in COLORS)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def vertex_actions():
    answer = set()
    for block_perm in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            answer.add(tuple(
                2 * block_perm[v // 2] + ((v % 2) ^ flips[v // 2])
                for v in V
            ))
    require(len(answer) == 384, "B4 order changed")
    return tuple(sorted(answer))


def act_word(word, va, ca):
    image = [0] * 8
    for old in V:
        image[va[old]] = ca[word[old]]
    return tuple(image)


def cell(u, v, i, j):
    if u < v:
        return (u, v, i, j)
    return (v, u, j, i)


def act_cell(value, va, ca):
    u, v, i, j = value
    return cell(va[u], va[v], ca[i], ca[j])


def cell_label(value):
    u, v, i, j = value
    return f"a_{u}{v}_{i}{j}"


def grade_word(word):
    grade = [0] * 24
    for vertex, colour in enumerate(word):
        grade[3 * vertex + colour] += 1
    return tuple(grade)


def grade_cell(value):
    u, v, i, j = value
    grade = [0] * 24
    grade[3 * u + i] += 1
    grade[3 * v + j] += 1
    return tuple(grade)


def add_grade(left, right):
    return tuple(a + b for a, b in zip(left, right))


def row_polynomial(word, multiplier=None):
    monomials = set()
    for matching in perfect_matchings(V):
        factors = [cell(u, v, word[u], word[v]) for u, v in matching]
        if multiplier is not None:
            factors.append(multiplier)
        monomials.add(tuple(sorted(factors)))
    require(len(monomials) == 105, "source row monomials collided")
    return monomials


def sparse_rank(rows):
    pivots = {}
    for support in rows:
        vector = {monomial: Fraction(1) for monomial in support}
        while vector:
            pivot = min(vector)
            coefficient = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    monomial: value / coefficient
                    for monomial, value in vector.items()
                }
                break
            existing = pivots[pivot]
            for monomial, value in existing.items():
                vector[monomial] = vector.get(monomial, Fraction(0)) - coefficient * value
                if vector[monomial] == 0:
                    del vector[monomial]
    return len(pivots)


def quotient_objects(universe, actions, action):
    unseen = set(universe)
    ledger = []
    while unseen:
        representative = min(unseen)
        orbit = {action(representative, va, ca) for va, ca in actions}
        orbit &= unseen
        require(orbit, "empty object orbit")
        unseen -= orbit
        ledger.append((representative, len(orbit)))
    return ledger


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main(write_results=False):
    tail = json.loads(TAIL_RESULT.read_text())
    fixed = defaultdict(set)
    for record in tail["row_ledger"]:
        fixed[record["profile"]].add(tuple(map(int,
                                              record["source_label"][2:])))
    require({profile: len(rows) for profile, rows in fixed.items()} == {
        "7+1": 8, "6+1+1": 12, "3+3+2": 360,
    }, "fixed 380-row census changed")

    vas = vertex_actions()
    cas = tuple(permutations(COLORS))
    actions = tuple(product(vas, cas))
    require(len(actions) == 2304, "B4 x S3 order changed")

    full_rows = {}
    row_orbit_ledgers = {}
    for profile, seeds in fixed.items():
        universe = {
            act_word(word, va, ca)
            for word in seeds for va, ca in actions
        }
        full_rows[profile] = universe
        ledger = quotient_objects(
            universe, actions,
            lambda word, va, ca: act_word(word, va, ca),
        )
        row_orbit_ledgers[profile] = ledger
    require({profile: len(rows) for profile, rows in full_rows.items()} == {
        "7+1": 48, "6+1+1": 144, "3+3+2": 1680,
    }, "full transported row census changed")
    require({profile: len(ledger) for profile, ledger in
             row_orbit_ledgers.items()} == {
                 "7+1": 1, "6+1+1": 1, "3+3+2": 5,
             }, "transported row orbit census changed")

    # Exact degree-one multiplier orbit census.  The objects are quotiented
    # before any monomial expansion.
    multiplier_orbits = {}
    for profile, rows in full_rows.items():
        universe = {(word, multiplier) for word in rows for multiplier in CELLS}
        ledger = quotient_objects(
            universe, actions,
            lambda value, va, ca: (
                act_word(value[0], va, ca),
                act_cell(value[1], va, ca),
            ),
        )
        multiplier_orbits[profile] = ledger
    require({profile: len(ledger) for profile, ledger in
             multiplier_orbits.items()} == {
                 "7+1": 39, "6+1+1": 56, "3+3+2": 368,
             }, "degree-one multiplier orbit census changed")

    all_rows = [(profile, word) for profile, rows in full_rows.items()
                for word in rows]
    word_grades = {word: grade_word(word) for _, word in all_rows}
    cell_grades = {value: grade_cell(value) for value in CELLS}

    # Four B4 x S3 target orbits: same/cross physical edge times pure colour
    # equal to an endpoint or equal to the third colour.
    target_specs = (
        ("same_block_endpoint", (0, 1, 0, 1), 0, 48),
        ("same_block_third", (0, 1, 0, 1), 2, 24),
        ("cross_block_endpoint", (0, 2, 0, 1), 0, 288),
        ("cross_block_third", (0, 2, 0, 1), 2, 144),
    )
    target_blocks = []
    for name, tail_cell, pure_colour, orbit_size in target_specs:
        target_grade = add_grade(
            grade_word((pure_colour,) * 8), cell_grades[tail_cell]
        )
        candidates = [
            (profile, word, multiplier)
            for profile, word in all_rows for multiplier in CELLS
            if add_grade(word_grades[word], cell_grades[multiplier])
            == target_grade
        ]
        candidate_vectors = [row_polynomial(word, multiplier)
                             for _, word, multiplier in candidates]
        target_vector = row_polynomial((pure_colour,) * 8, tail_cell)
        columns = set(target_vector)
        for vector in candidate_vectors:
            columns.update(vector)
        rank = sparse_rank(candidate_vectors)
        augmented_rank = sparse_rank(candidate_vectors + [target_vector])
        candidate_union = set().union(*candidate_vectors) if candidate_vectors else set()
        exclusive = sorted(target_vector - candidate_union)
        require(augmented_rank == rank + 1 and exclusive,
                f"tail-H target unexpectedly entered span: {name}")
        dual = exclusive[0]
        target_blocks.append({
            "name": name,
            "target_orbit_size": orbit_size,
            "representative": {
                "tail_cell": cell_label(tail_cell),
                "pure_H_colour": pure_colour,
                "target": f"{cell_label(tail_cell)}*H{pure_colour}",
            },
            "candidate_rows": len(candidates),
            "candidate_profile_histogram": dict(sorted(Counter(
                profile for profile, _, _ in candidates).items())),
            "candidate_ledger": [{
                "profile": profile,
                "source_label": "F_" + "".join(map(str, word)),
                "multiplier": cell_label(multiplier),
            } for profile, word, multiplier in sorted(candidates)],
            "monomial_columns": len(columns),
            "rational_rank": rank,
            "augmented_rational_rank": augmented_rank,
            "target_exclusive_monomials": len(exclusive),
            "dual_witness_monomial": "*".join(cell_label(value)
                                                 for value in dual),
            "dual_witness": (
                "coefficient is 1 in the target and 0 in every grade-compatible "
                "mixed row times linear multiplier"
            ),
            "membership": False,
        })
    require([(block["candidate_rows"], block["monomial_columns"],
              block["rational_rank"], block["augmented_rational_rank"],
              block["target_exclusive_monomials"])
             for block in target_blocks] == [
                 (1, 195, 1, 2, 90),
                 (2, 300, 2, 3, 105),
                 (1, 195, 1, 2, 90),
                 (3, 390, 3, 4, 90),
             ], "target block matrices changed")

    # Degree zero: a mixed word and a pure word have different vertex-colour
    # grades, so the pure-H target block has no candidate row at all.
    pure_target = row_polynomial((0,) * 8)
    require(len(pure_target) == 105, "pure target monomial count changed")

    quadratic_multipliers = len(CELLS) * (len(CELLS) + 1) // 2
    degree2_objects = sum(map(len, full_rows.values())) * quadratic_multipliers
    degree2_orbit_lower_bound = (degree2_objects + len(actions) - 1) // len(actions)
    require(quadratic_multipliers == 31878 and
            degree2_objects == 59675616 and
            degree2_orbit_lower_bound == 25901,
            "degree-two size guard changed")

    result = {
        "status": "PASS exact low-degree orbit-contraction nonmembership audit",
        "symmetry": {
            "group": "B4 x S3", "group_order": len(actions),
            "fixed_row_counts": {profile: len(rows)
                                 for profile, rows in fixed.items()},
            "transported_row_counts": {profile: len(rows)
                                       for profile, rows in full_rows.items()},
            "transported_row_orbits": {
                profile: {
                    "count": len(ledger),
                    "size_histogram": dict(sorted(Counter(
                        size for _, size in ledger).items())),
                    "representatives": [
                        {"source_label": "F_" + "".join(map(str, word)),
                         "orbit_size": size}
                        for word, size in ledger
                    ],
                } for profile, ledger in row_orbit_ledgers.items()
            },
        },
        "degree_one_orbit_ansatz": {
            "literal_row_multiplier_objects": sum(
                len(rows) * len(CELLS) for rows in full_rows.values()),
            "row_multiplier_orbits": sum(map(len, multiplier_orbits.values())),
            "by_profile": {
                profile: {
                    "objects": len(full_rows[profile]) * len(CELLS),
                    "orbits": len(ledger),
                    "orbit_size_histogram": dict(sorted(Counter(
                        size for _, size in ledger).items())),
                } for profile, ledger in multiplier_orbits.items()
            },
            "vertex_colour_multigrading": (
                "F_w has grade sum_v e_(v,w_v); a linear edge-cell "
                "multiplier adds two endpoint colour degrees.  Therefore the "
                "global 463-orbit ansatz splits into independent exact grade blocks."
            ),
        },
        "degree_zero_pure_H_target": {
            "target_orbits": 1,
            "candidate_mixed_rows_in_grade": 0,
            "matrix_shape": [0, 105],
            "rational_rank": 0,
            "augmented_rational_rank": 1,
            "dual_witness": (
                "any pure matching monomial; no mixed source row has the "
                "pure vertex-colour grade"
            ),
            "membership": False,
        },
        "degree_one_tail_times_pure_H_targets": {
            "target_objects": 504,
            "target_orbits": 4,
            "blocks": target_blocks,
            "global_conclusion": (
                "No T_uv^ij*H_k target lies in the span of all transported "
                "71/611/332 rows with grade-compatible linear multipliers. "
                "Since this rejects the unrestricted canonical grade block, "
                "it also rejects every B4 x S3 orbit-symmetric ansatz."
            ),
            "332_role": (
                "No 332 row can enter these blocks: after one multiplier its "
                "base word would still differ from the pure colour at more "
                "than the two multiplier endpoints."
            ),
        },
        "scalar_zero_tail_target_guard": {
            "product": (
                "The product of the 168 tail cells vanishes when any one cell "
                "vanishes, not only on the zero-tail locus."
            ),
            "positive_sum": (
                "The source ideal is over characteristic-zero algebraic fields. "
                "A sum of squares has nonzero isotropic zeros after algebraic "
                "closure, and conjugate squares are not source polynomials."
            ),
            "geometric_obstruction": (
                "In A^168 over an algebraically closed field, one nonconstant "
                "polynomial defines a hypersurface and cannot have only the "
                "origin as its zero set.  A vector/ideal target is required."
            ),
        },
        "degree_two_size_guard": {
            "quadratic_cell_monomials_with_repetition": quadratic_multipliers,
            "literal_row_multiplier_objects": degree2_objects,
            "orbit_count_lower_bound": degree2_orbit_lower_bound,
            "launched": False,
            "reason": (
                "At least 25,901 B4 x S3 orbits is not a small ansatz, and no "
                "audited quadratic localizer target would turn such an identity "
                "into the individual 168 tail equations."
            ),
        },
        "terminal_verdict": (
            "Degree-zero/one Euler-contraction machinery cannot kill the remote "
            "factor or force support6/cap activity.  The exact dual monomial "
            "witnesses retire this ansatz.  The remaining route must use the "
            "boundary-valued substituted 332 system or a higher-degree identity "
            "with an explicitly audited unit/localizer."
        ),
        "scope_guard": (
            "This is exact rational linear nonmembership, not a statement that "
            "the full X5 remote ideal has a point.  Degree two was sized and "
            "rejected by the prescribed smallness guard, not algebraically solved."
        ),
    }
    result["logical_sha256"] = logical_hash(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "rows": sum(map(len, full_rows.values())),
        "row_orbits": sum(map(len, row_orbit_ledgers.values())),
        "degree1_objects": result["degree_one_orbit_ansatz"]["literal_row_multiplier_objects"],
        "degree1_orbits": result["degree_one_orbit_ansatz"]["row_multiplier_orbits"],
        "target_block_shapes": [
            [block["candidate_rows"], block["monomial_columns"]]
            for block in target_blocks
        ],
        "target_memberships": [block["membership"] for block in target_blocks],
        "degree2_orbit_lower_bound": degree2_orbit_lower_bound,
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
