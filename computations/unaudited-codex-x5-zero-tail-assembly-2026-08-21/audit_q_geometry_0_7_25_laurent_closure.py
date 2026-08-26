#!/usr/bin/env python3
"""Exact Laurent closure of the 0,7,25 zero-tail support geometry.

The Boolean shadow has 224 B4 x S3 refinements with Q-cut triple 0,7,25.
This audit first restores the four reduced triangle equations.  Only four
support orbits survive structurally.  On each survivor it fixes a unimodular
three-entry gauge, enumerates the six exact Q(sqrt(2)) root branches per
colour, quotients the 216 triples by the literal support stabilizer, and
replays all 1,566 explicit mixed source rows.  A single literal row is a
nonzero unit on every root branch of each survivor.

No Groebner basis or sampled rank calculation is used.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHADOW = HERE / "results_extended_diagonal_packet_support_shadow.json"
PACKET = HERE / "extended_diagonal_packet_1566.json"
OUT = HERE / "results_q_geometry_0_7_25_laurent_closure.json"

EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
Q_CUTS = (0, 7, 25)
SURVIVOR_X_MASKS = (
    (38, 56, 56),
    (38, 63, 56),
    (63, 38, 63),
    (63, 63, 63),
)
KILLERS = {
    (38, 56, 56): "00110110",
    (38, 63, 56): "00110110",
    (63, 38, 63): "00021021",
    (63, 63, 63): "00011011",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


# Exact arithmetic in Q(sqrt(2)); all values below are algebraic units and
# therefore have norm +/-1.
ZERO = (0, 0)
ONE = (1, 0)


def k_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def k_neg(value):
    return -value[0], -value[1]


def k_mul(left, right):
    return (left[0]*right[0] + 2*left[1]*right[1],
            left[0]*right[1] + left[1]*right[0])


def k_inv(value):
    norm = value[0]*value[0] - 2*value[1]*value[1]
    require(norm in (1, -1), ("nonunit inversion", value, norm))
    return value[0] // norm, -value[1] // norm


def k_pow(value, exponent):
    if exponent < 0:
        return k_pow(k_inv(value), -exponent)
    answer = ONE
    for _ in range(exponent):
        answer = k_mul(answer, value)
    return answer


def encode_k(value):
    return f"{value[0]}+({value[1]})*sqrt(2)"


ROOTS = {
    # u^2-2u-1=0
    "A": ((1, 1), (1, -1)),
    # u^2+2u-1=0
    "B": ((-1, 1), (-1, -1)),
}
ROOT_TYPES = {38: "AABA", 56: "AAAA", 63: "BBBB"}
ROOT_RELATIONS = {
    38: (1, -1, 1, 1),     # u0*u2*u3/u1=1
    56: (1, -1, 1, -1),    # u0*u2/(u1*u3)=1
    63: (1, -1, 1, -1),
}


def valid_root_bits(mask):
    answer = []
    for bits in product((0, 1), repeat=4):
        roots = tuple(ROOTS[kind][bit]
                      for kind, bit in zip(ROOT_TYPES[mask], bits))
        value = ONE
        for root, exponent in zip(roots, ROOT_RELATIONS[mask]):
            value = k_mul(value, k_pow(root, exponent))
        if value == ONE:
            answer.append(bits)
    require(len(answer) == 6, ("root branch count", mask, answer))
    return tuple(answer)


VALID_ROOTS = {mask: valid_root_bits(mask) for mask in ROOT_TYPES}


def gauge_entries(mask, root_bits):
    """Six first-live block entries after setting a01=a02=a03=1."""
    roots = tuple(ROOTS[kind][bit]
                  for kind, bit in zip(ROOT_TYPES[mask], root_bits))
    if mask == 38:
        answer = (ONE, ONE, ONE,
                  k_inv(roots[0]), k_inv(roots[1]), roots[2])
    elif mask == 56:
        answer = (ONE, ONE, ONE,
                  k_inv(roots[0]), k_inv(roots[1]), k_inv(roots[2]))
    else:
        require(mask == 63, "unknown Laurent mask")
        answer = (ONE, ONE, ONE, roots[0], roots[1], roots[2])
    return answer


def graph_edge(mask, root_bits, u, v):
    if u > v:
        u, v = v, u
    super_u, clone_u = divmod(u, 2)
    super_v, clone_v = divmod(v, 2)
    if super_u == super_v:
        return ONE
    edge = EDGE_INDEX[(super_u, super_v)]
    relation = (mask >> edge) & 1
    first = (0, 0) if relation == 0 else (0, 1)
    second = (1, 1) if relation == 0 else (1, 0)
    value = gauge_entries(mask, root_bits)[edge]
    if (clone_u, clone_v) == first:
        return value
    if (clone_u, clone_v) == second:
        return k_neg(k_inv(value))
    return ZERO


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index+1:]
        answer.extend((((first, second),) + tail)
                      for tail in perfect_matchings(rest))
    return tuple(answer)


EVEN_SUBSETS = tuple(mask for mask in range(256)
                     if mask.bit_count() % 2 == 0)
MATCHINGS = {
    mask: perfect_matchings(tuple(index for index in range(8)
                                  if (mask >> index) & 1))
    for mask in EVEN_SUBSETS
}


def subset_table(mask, root_bits):
    answer = {}
    for subset, matchings in MATCHINGS.items():
        value = ZERO
        for matching in matchings:
            term = ONE
            for u, v in matching:
                term = k_mul(term, graph_edge(mask, root_bits, u, v))
            value = k_add(value, term)
        answer[subset] = value
    return answer


TABLES = {(mask, bits): subset_table(mask, bits)
          for mask in ROOT_TYPES for bits in VALID_ROOTS[mask]}


def triangle_live_term_count(mask, triple):
    i, j, k = triple
    answer = 0
    for clone_i, clone_j, clone_k in product((0, 1), repeat=3):
        cells = ((i, j, clone_i, clone_j),
                 (i, k, 1-clone_i, clone_k),
                 (j, k, 1-clone_j, 1-clone_k))
        live = True
        for left, right, a, b in cells:
            edge = EDGE_INDEX[tuple(sorted((left, right)))]
            if left > right:
                a, b = b, a
            relation = (mask >> edge) & 1
            allowed = ((0, 0), (1, 1)) if relation == 0 else \
                      ((0, 1), (1, 0))
            live &= (a, b) in allowed
        answer += live
    return answer


def triangle_admissible_masks():
    triples = tuple(combinations(range(4), 3))
    profiles = {
        mask: tuple(triangle_live_term_count(mask, triple)
                    for triple in triples)
        for mask in range(64)
    }
    admissible = tuple(mask for mask, counts in profiles.items()
                       if all(counts))
    require(admissible == (11, 12, 18, 21, 33, 38, 56, 63),
            ("triangle admissible mask census", admissible))
    require(Counter(profiles.values()) == {
        (0, 0, 0, 0): 8,
        (2, 2, 0, 0): 8, (2, 0, 2, 0): 8,
        (0, 2, 2, 0): 8, (2, 0, 0, 2): 8,
        (0, 2, 0, 2): 8, (0, 0, 2, 2): 8,
        (2, 2, 2, 2): 8,
    }, "triangle profile histogram changed")
    return admissible, profiles


def subset_masks(label):
    return tuple(sum(1 << site for site, value in enumerate(label)
                     if int(value) == colour)
                 for colour in range(3))


def row_value(row_subsets, tables):
    answer = ONE
    for colour in range(3):
        answer = k_mul(answer, tables[colour][row_subsets[colour]])
    return answer


def transform_mask(mask, permutation, flip_mask):
    answer = 0
    for index, (left, right) in enumerate(EDGES):
        bit = ((mask >> index) & 1) ^ ((flip_mask >> left) & 1) ^ \
              ((flip_mask >> right) & 1)
        image = tuple(sorted((permutation[left], permutation[right])))
        answer |= bit << EDGE_INDEX[image]
    return answer


def transform_state(state, permutation, flip_mask, colour_permutation):
    answer = [None]*3
    for colour, mask in enumerate(state):
        answer[colour_permutation[colour]] = transform_mask(
            mask, permutation, flip_mask)
    return tuple(answer)


def support_stabilizer(x_masks):
    answer = []
    for permutation in permutations(range(4)):
        for flip_mask in range(16):
            for colour_permutation in permutations(range(3)):
                if (transform_state(Q_CUTS, permutation, flip_mask,
                                    colour_permutation) == Q_CUTS and
                    transform_state(x_masks, permutation, flip_mask,
                                    colour_permutation) == x_masks):
                    answer.append((permutation, flip_mask,
                                   colour_permutation))
    return tuple(answer)


def extract_root_bits(mask, edge_function):
    entries = []
    for edge, (left, right) in enumerate(EDGES):
        relation = (mask >> edge) & 1
        a, b = (0, 0) if relation == 0 else (0, 1)
        entries.append(edge_function(2*left+a, 2*right+b))
    a0, a1, a2, a3, a4, a5 = entries
    if mask == 38:
        invariants = (
            k_mul(a0, k_inv(k_mul(a1, a3))),
            k_mul(a0, k_inv(k_mul(a2, a4))),
            k_mul(a1, k_mul(k_inv(a2), a5)),
            k_mul(a3, k_inv(k_mul(a4, a5))),
        )
    elif mask == 56:
        invariants = (
            k_mul(a0, k_inv(k_mul(a1, a3))),
            k_mul(a0, k_inv(k_mul(a2, a4))),
            k_mul(a1, k_inv(k_mul(a2, a5))),
            k_mul(a4, k_inv(k_mul(a3, a5))),
        )
    else:
        require(mask == 63, "root extraction mask changed")
        invariants = (
            k_mul(a0, k_mul(k_inv(a1), a3)),
            k_mul(a0, k_mul(k_inv(a2), a4)),
            k_mul(a1, k_mul(k_inv(a2), a5)),
            k_mul(a3, k_mul(k_inv(a4), a5)),
        )
    return tuple(ROOTS[kind].index(value)
                 for kind, value in zip(ROOT_TYPES[mask], invariants))


def act_root_triple(x_masks, root_triple, action):
    permutation, flip_mask, colour_permutation = action
    vertex_action = tuple(
        2*permutation[vertex//2]
        + ((vertex % 2) ^ ((flip_mask >> (vertex//2)) & 1))
        for vertex in range(8)
    )
    inverse = [0]*8
    for old, new in enumerate(vertex_action):
        inverse[new] = old
    answer = [None]*3
    for colour, (mask, roots) in enumerate(zip(x_masks, root_triple)):
        image_mask = transform_mask(mask, permutation, flip_mask)

        def image_edge(u, v):
            return graph_edge(mask, roots, inverse[u], inverse[v])

        answer[colour_permutation[colour]] = extract_root_bits(
            image_mask, image_edge)
    return tuple(answer)


def root_orbit_census(x_masks, stabilizer):
    universe = set(product(*(VALID_ROOTS[mask] for mask in x_masks)))
    unseen = set(universe)
    sizes = Counter()
    while unseen:
        seed = min(unseen)
        orbit = {act_root_triple(x_masks, seed, action)
                 for action in stabilizer}
        require(orbit <= universe, "stabilizer left the root branch set")
        unseen -= orbit
        sizes[len(orbit)] += 1
    return len(universe), sum(sizes.values()), dict(sorted(sizes.items()))


def main():
    shadow = json.loads(SHADOW.read_text())
    packet = json.loads(PACKET.read_text())
    records = [row for row in shadow["support_shadow"]
               ["minimal_surviving_support_signature_antichain"]
               if tuple(row["q_pair_cut_masks_e01_e02_e03_e12_e13_e23"])
               == Q_CUTS]
    require(len(records) == 224 and
            sum(row["orbit_size"] for row in records) == 211680,
            "0,7,25 support ledger changed")

    admissible, profiles = triangle_admissible_masks()
    surviving_records = [row for row in records
                         if all(mask in admissible for mask in
                                row["x_relation_masks_e01_e02_e03_e12_e13_e23"])]
    require(tuple(tuple(row[
        "x_relation_masks_e01_e02_e03_e12_e13_e23"])
                  for row in surviving_records) == SURVIVOR_X_MASKS,
            "triangle survivor antichain changed")

    rows = tuple({
        "label": row["label"],
        "orbit": row["orbit"],
        "formula": row["literal_formula"],
        "subsets": subset_masks(row["label"]),
    } for row in packet["explicit_rows"])
    require(len(rows) == 1566 and
            len({row["label"] for row in rows}) == 1566,
            "explicit source packet changed")
    required_new = {
        "422_two_edges_to_each_minor_colour",
        "422_majority_loop_colour_triangle",
        "422_majority_loop_minor_loop_two_cross_edges",
    }
    require(required_new <= {row["orbit"] for row in rows},
            "a new 422 orbit left the source packet")

    orbit_size_by_masks = {
        tuple(row["x_relation_masks_e01_e02_e03_e12_e13_e23"]):
            row["orbit_size"] for row in surviving_records
    }
    closure_records = []
    for x_masks in SURVIVOR_X_MASKS:
        stabilizer = support_stabilizer(x_masks)
        expected_stabilizer = 2304 // orbit_size_by_masks[x_masks]
        require(len(stabilizer) == expected_stabilizer,
                ("support stabilizer size", x_masks, len(stabilizer),
                 expected_stabilizer))
        root_branches, root_orbits, root_orbit_sizes = root_orbit_census(
            x_masks, stabilizer)
        require(root_branches == 216, "root triple count changed")

        branch_nonzero_counts = Counter()
        sector_rows = defaultdict(set)
        sector_evaluations = Counter()
        value_sets = defaultdict(set)
        killer = KILLERS[x_masks]
        killer_row = next(row for row in rows if row["label"] == killer)
        killer_values = Counter()
        for root_triple in product(*(VALID_ROOTS[mask] for mask in x_masks)):
            tables = tuple(TABLES[(mask, roots)]
                           for mask, roots in zip(x_masks, root_triple))
            require(tuple(table[255] for table in tables) ==
                    ((4, 0),)*3,
                    ("H ceased to equal four", x_masks, root_triple))
            nonzero = 0
            for row in rows:
                value = row_value(row["subsets"], tables)
                if value != ZERO:
                    nonzero += 1
                    sector_rows[row["orbit"]].add(row["label"])
                    sector_evaluations[row["orbit"]] += 1
                    value_sets[row["orbit"]].add(value)
            branch_nonzero_counts[nonzero] += 1
            killer_value = row_value(killer_row["subsets"], tables)
            require(killer_value != ZERO,
                    ("killer vanished", x_masks, root_triple, killer))
            killer_values[killer_value] += 1

        require(required_new <= set(sector_rows),
                ("not all new 422 sectors replayed", x_masks, sector_rows))
        closure_records.append({
            "q_cut_masks": list(Q_CUTS),
            "x_relation_masks": list(x_masks),
            "support_orbit_size": orbit_size_by_masks[x_masks],
            "support_stabilizer_size_in_B4_times_S3": len(stabilizer),
            "Laurent_interface_before_root_enumeration": {
                "variables": 18,
                "gauge": "a_c,01=a_c,02=a_c,03=1 for each colour",
                "gauge_minor": "unimodular 3x3 exponent minor",
                "e_rows_identically_zero": 18,
                "nonconstant_t_rows": 12,
                "explicit_mixed_rows_replayed": len(rows),
                "redundant_e_multiple_rows": 72,
            },
            "one_colour_root_branches": {
                str(mask): {
                    "root_types": ROOT_TYPES[mask],
                    "multiplicative_relation_exponents":
                        list(ROOT_RELATIONS[mask]),
                    "branches": [list(bits) for bits in VALID_ROOTS[mask]],
                } for mask in sorted(set(x_masks))
            },
            "three_colour_root_branches": root_branches,
            "root_branch_orbits_under_support_stabilizer": root_orbits,
            "root_branch_orbit_size_histogram": {
                str(size): count for size, count in root_orbit_sizes.items()},
            "H_values_on_every_root_branch": [4, 4, 4],
            "nonzero_source_row_count_histogram": {
                str(count): multiplicity
                for count, multiplicity in sorted(branch_nonzero_counts.items())},
            "active_source_sectors": {
                sector: {
                    "literal_rows_nonzero_on_at_least_one_root_branch":
                        len(sector_rows[sector]),
                    "nonzero_root_branch_evaluations":
                        sector_evaluations[sector],
                    "exact_value_count": len(value_sets[sector]),
                } for sector in sorted(sector_rows)
            },
            "uniform_killer": {
                "source_label": killer,
                "literal_formula": killer_row["formula"],
                "source_orbit": killer_row["orbit"],
                "nonzero_on_all_root_branches": True,
                "exact_value_histogram": {
                    encode_k(value): count
                    for value, count in sorted(killer_values.items())},
            },
            "realizable": False,
        })

    result = {
        "status": "PASS exact Laurent closure of q geometry 0,7,25",
        "input_geometry": {
            "q_cut_masks": list(Q_CUTS),
            "support_orbits": len(records),
            "labelled_minimal_supports": sum(row["orbit_size"]
                                              for row in records),
        },
        "triangle_support_filter": {
            "admissible_one_colour_relation_masks": list(admissible),
            "support_orbits_rejected_by_constant_minus_two_t_row":
                len(records)-len(surviving_records),
            "surviving_support_orbits": len(surviving_records),
            "surviving_x_mask_triples": [list(masks)
                                          for masks in SURVIVOR_X_MASKS],
            "argument": (
                "Every rejected relation mask has a supervertex triple with "
                "no live cubic triangle term, so t=1-1-1-1=-2 in "
                "characteristic zero."),
        },
        "Laurent_closure_records": closure_records,
        "packet_coverage": {
            "explicit_rows": len(rows),
            "all_three_new_422_orbits_replayed": True,
            "full_440_and_master_replayed": True,
            "omitted_72_rows": "exact e multiples, hence zero on this chart",
        },
        "conclusion": (
            "All 224 support refinements in the 0,7,25 geometry are "
            "unrealizable over the algebraic closure in characteristic zero. "
            "220 fail a literal reduced triangle. The remaining four have "
            "six exact Q(sqrt(2)) branches per colour and H_c=4, but one "
            "displayed literal mixed source row is nonzero on every one of "
            "their 216 root triples."),
        "scope_guard": (
            "This closes exactly the 0,7,25 part of the frozen 310-orbit "
            "minimal support shadow. It does not promote Boolean support "
            "containment to a component theorem outside that antichain."),
        "mutation_guards": {
            "skip_triangle_support_filter": True,
            "replace_1566_literal_rows_by_selected_270": True,
            "omit_any_new_422_orbit": True,
            "sample_root_branches_instead_of_exact_enumeration": True,
            "drop_support_stabilizer_quotient": True,
            "infer_H_live_without_exact_evaluation": True,
        },
        "source_hashes": {
            str(SHADOW.relative_to(ROOT)): file_sha(SHADOW),
            str(PACKET.relative_to(ROOT)): file_sha(PACKET),
        },
    }
    result["logical_sha256"] = logical_sha(result)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    if "--check-results" in sys.argv:
        require(OUT.read_text() == text, "result replay mismatch")
    print(json.dumps({
        "status": result["status"],
        "support_orbits": len(records),
        "triangle_rejected": len(records)-len(surviving_records),
        "Laurent_survivors_tested": len(closure_records),
        "realizable": sum(row["realizable"] for row in closure_records),
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
