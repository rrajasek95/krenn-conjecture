#!/usr/bin/env python3
"""Exact reduced-C2 evaluation and all-carrier rank counterguard."""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERT = (ROOT / "computations" /
        "unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23" /
        "certificate_dag.json")
PRIOR = (ROOT / "computations" /
         "unaudited-codex-n8-orbit85-tail-extraction-audit-2026-08-23" /
         "results_orbit85_tail_extraction.json")
RESPONSE_CORE = (ROOT / "computations" /
                 "unaudited-codex-response-star-2026-08-20" /
                 "response_star_core.py")
OUT = HERE / "results_orbit85_tail2_carrier_counterguard.json"
EXPECTED = {
    CERT: "d5effbf6447c7b74b8bcd9ae1370bc2e498f15cd8e95fae60576cf657907db96",
    PRIOR: "8794a314a3cdd178d3d643e6d1eda7bcc9692b70a64eda84c13fd88b495c28c6",
    RESPONSE_CORE: "89aa79a15fd9a98b16529cf69f8158b348d68902729cde0ea24b363fce5f2c59",
}
EDGES = tuple(combinations(range(8), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
GRAPH_MASKS = (0xA800C0, 0x8885002, 0xAA1001)
TARGET_FREE_SETS = (
    frozenset((0, 3, 4, 5)),
    frozenset((1, 3, 4, 5, 6)),
    frozenset((2, 3, 4, 5, 6)),
)
PRIME = 1_000_003


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
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


def canonical_edge(u, v):
    return (u, v) if u < v else (v, u)


def diagonal_cell(u, v, colour):
    edge = canonical_edge(u, v)
    return int(bool(GRAPH_MASKS[colour] & (1 << EDGE_INDEX[edge])))


def tail_cell(u, v, first_colour, second_colour, mutate=False):
    if u > v:
        u, v, first_colour, second_colour = v, u, second_colour, first_colour
    value = (17 * u + 31 * v + 43 * first_colour + 59 * second_colour
             + 7 * first_colour * second_colour + 11 * u * v) % 97 + 1
    if mutate and (u, v, first_colour, second_colour) == (0, 3, 0, 1):
        value += 1
    return value


def source_cell(u, v, first_colour, second_colour, mutate=False):
    if first_colour == second_colour:
        return diagonal_cell(u, v, first_colour)
    return tail_cell(u, v, first_colour, second_colour, mutate)


def diagonal_hafnian(colour, mask):
    sites = tuple(site for site in range(8) if mask & (1 << site))
    return sum(
        all(diagonal_cell(u, v, colour) for u, v in matching)
        for matching in perfect_matchings(sites)
    )


def free_sets():
    answer = []
    full = (1 << 8) - 1
    for colour in range(3):
        other = tuple(c for c in range(3) if c != colour)
        free = set()
        for site in range(7):
            residual = full & ~(1 << 7) & ~(1 << site)
            all_zero = True
            split = residual
            while True:
                if split.bit_count() % 2 == 0:
                    complement = residual ^ split
                    if (diagonal_hafnian(other[0], split)
                            * diagonal_hafnian(other[1], complement)):
                        all_zero = False
                        break
                if split == 0:
                    break
                split = (split - 1) & residual
            if all_zero:
                free.add(site)
        answer.append(frozenset(free))
    return tuple(answer)


def word_from_masks(masks):
    word = [None] * 8
    for colour, mask in enumerate(masks):
        for site in range(8):
            if mask & (1 << site):
                require(word[site] is None, (masks, site))
                word[site] = colour
    require(all(entry is not None for entry in word), masks)
    return tuple(word)


def tail2(masks, mutate=False):
    word = word_from_masks(masks)
    total = 0
    for matching in perfect_matchings(tuple(range(8))):
        if sum(word[u] != word[v] for u, v in matching) != 2:
            continue
        term = 1
        for u, v in matching:
            if word[u] == word[v]:
                term *= diagonal_cell(u, v, word[u])
            else:
                term *= tail_cell(u, v, word[u], word[v], mutate)
        total += term
    return total


def canonical_selector_assignment(certificate):
    values = {}
    for antecedent in certificate["antecedents"]:
        if antecedent["kind"] != "selector_zero_link":
            continue
        _, colour, mask = antecedent["p_key"]
        values[antecedent["variable"]] = int(
            diagonal_hafnian(colour, mask) != 0)
    for antecedent in certificate["antecedents"]:
        if antecedent["kind"] != "laplace_witness_definition":
            continue
        first, second = antecedent["factor_selectors"]
        values[antecedent["variable"]] = values[first] * values[second]
    require(len(values) == 5592, len(values))
    return values


def falsity(literal, values):
    value = values[abs(literal)]
    return 1 - value if literal > 0 else value


def reverse_leaf_weights(certificate, values):
    nodes = certificate["proof_nodes"]
    adjoint = {certificate["root"]: 1}
    for node in reversed(nodes):
        weight = adjoint.get(node["id"], 0)
        if not weight or node["op"] == "compile_clause":
            continue
        if node["op"] == "resolve_polynomials":
            left_factor = right_factor = 1
            for literal in node["left_falsity_factors"]:
                left_factor *= falsity(literal, values)
            for literal in node["right_falsity_factors"]:
                right_factor *= falsity(literal, values)
            adjoint[node["left"]] = (adjoint.get(node["left"], 0)
                                      + weight * left_factor)
            adjoint[node["right"]] = (adjoint.get(node["right"], 0)
                                       + weight * right_factor)
        elif node["op"] == "weaken_polynomial":
            factor = 1
            for literal in node["added_falsity_factors"]:
                factor *= falsity(literal, values)
            adjoint[node["input"]] = (adjoint.get(node["input"], 0)
                                       + weight * factor)
        else:
            raise RuntimeError(node["op"])
    return {
        node["cnf_clause_id"]: adjoint.get(node["id"], 0)
        for node in nodes if node["op"] == "compile_clause"
        and adjoint.get(node["id"], 0)
    }


def reduced_c2(certificate, values, mutate=False):
    nodes = {node.get("cnf_clause_id"): node
             for node in certificate["proof_nodes"]
             if node["op"] == "compile_clause"}
    weights = reverse_leaf_weights(certificate, values)
    sensitive = Counter()
    contributions = []
    for clause_id, weight in weights.items():
        node = nodes[clause_id]
        family = node["compiler"]["schema"]
        if family not in ("A2", "C0", "XF"):
            continue
        sensitive[family] += 1
        if family == "A2":
            masks = tuple(node["compiler"]["tag"][1])
            multiplier = 1
            for literal in node["clause"]:
                variable = abs(literal)
                require(values[variable] == 1, (clause_id, variable))
                # Every live p-Hafnian here has value one, hence inverse one.
                p_key = next(row["p_key"] for row in certificate["antecedents"]
                             if row["kind"] == "selector_zero_link"
                             and row["variable"] == variable)
                require(diagonal_hafnian(p_key[1], p_key[2]) == 1,
                        (clause_id, p_key))
            coefficient = weight * multiplier * tail2(masks, mutate)
            contributions.append({
                "clause_id": clause_id,
                "family": family,
                "weight": weight,
                "masks": list(masks),
                "word": "".join(map(str, word_from_masks(masks))),
                "tail2": tail2(masks, mutate),
                "coefficient": coefficient,
            })
        elif family == "C0":
            star_selector = abs(node["clause"][0])
            # The C0 compiler's tail multiplier is p_x*u_x.  Every C0 leaf
            # reached by the reduced proof has p_x=0 at this branch point.
            require(values[star_selector] == 0,
                    (clause_id, star_selector, values[star_selector]))
        else:
            # Both XF compiler formulas carry their clause falsity product:
            # a(1-b) or (1-a)b.  It vanishes at each reached XF leaf.
            clause_factor = 1
            for literal in node["clause"]:
                clause_factor *= falsity(literal, values)
            require(clause_factor == 0, (clause_id, node["clause"]))
    require(sensitive == Counter({"A2": 1, "C0": 4, "XF": 3}), sensitive)
    require(len(contributions) == 1, contributions)
    total = sum(row["coefficient"] for row in contributions)
    require(total == (19146 if not mutate else 19147), total)
    return total, contributions, weights


def response_row(p, q, a, b, alpha, beta, mutate=False):
    row = []
    for first_colour in range(3):
        for second_colour in range(3):
            row.append(
                source_cell(p, a, first_colour, alpha, mutate)
                * source_cell(q, b, second_colour, beta, mutate)
                + source_cell(p, b, first_colour, beta, mutate)
                * source_cell(q, a, second_colour, alpha, mutate)
            )
    return row


def modular_pivot_rows(rows):
    basis = {}
    pivot_rows = []
    for row_index, raw in enumerate(rows):
        row = [value % PRIME for value in raw]
        for column in range(9):
            if not row[column]:
                continue
            if column not in basis:
                inverse = pow(row[column], PRIME - 2, PRIME)
                basis[column] = [(value * inverse) % PRIME for value in row]
                pivot_rows.append(row_index)
                break
            scale = row[column]
            row = [(left - scale * right) % PRIME
                   for left, right in zip(row, basis[column])]
        if len(basis) == 9:
            return tuple(pivot_rows)
    return tuple(pivot_rows)


def bareiss_determinant(matrix):
    work = [list(map(int, row)) for row in matrix]
    sign = 1
    denominator = 1
    size = len(work)
    for column in range(size - 1):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        for row in range(column + 1, size):
            for later in range(column + 1, size):
                work[row][later] = (
                    work[row][later] * pivot_value
                    - work[row][column] * work[column][later]
                ) // denominator
            work[row][column] = 0
        denominator = pivot_value
    return sign * work[-1][-1]


def carrier_records(mutate=False):
    records = []
    for p, q in EDGES:
        residual = tuple(site for site in range(8) if site not in (p, q))
        carriers = [("star", (centre,)) for centre in residual]
        carriers += [("triangle", triangle)
                     for triangle in combinations(residual, 3)]
        for kind, support in carriers:
            if kind == "star":
                response_edges = [edge for edge in combinations(residual, 2)
                                  if support[0] not in edge]
            else:
                allowed = set(combinations(support, 2))
                response_edges = [edge for edge in combinations(residual, 2)
                                  if edge not in allowed]
            rows = [response_row(p, q, a, b, alpha, beta, mutate)
                    for a, b in response_edges
                    for alpha in range(3) for beta in range(3)]
            pivots = modular_pivot_rows(rows)
            require(len(pivots) == 9, (p, q, kind, support, len(pivots)))
            determinant = bareiss_determinant([rows[index] for index in pivots])
            require(determinant and determinant % PRIME,
                    (p, q, kind, support, determinant))
            records.append({
                "pair": [p, q],
                "kind": kind,
                "support": list(support),
                "pivot_row_indices": list(pivots),
                "determinant": str(determinant),
                "determinant_mod_1000003": determinant % PRIME,
            })
    require(Counter(row["kind"] for row in records)
            == Counter({"triangle": 560, "star": 168}), len(records))
    return records


def full_amplitude(word, mutate=False):
    return sum(
        product_int(source_cell(u, v, word[u], word[v], mutate)
                    for u, v in matching)
        for matching in perfect_matchings(tuple(range(8)))
    )


def product_int(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    certificate = json.loads(CERT.read_text())
    require(free_sets() == TARGET_FREE_SETS, free_sets())
    open_values = []
    for colour in range(3):
        pure = diagonal_hafnian(colour, 255)
        star = diagonal_hafnian(colour, (1 << 7) | (1 << colour))
        cofactor = diagonal_hafnian(
            colour, 255 & ~(1 << 7) & ~(1 << colour))
        open_values.append((pure, star, cofactor))
    require(open_values == [(1, 1, 1)] * 3, open_values)

    selectors = canonical_selector_assignment(certificate)
    c2, contributions, weights = reduced_c2(certificate, selectors, mutate)
    carriers = carrier_records(mutate)
    carrier_digest = sha256(json.dumps(
        carriers, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()

    mixed_counts = Counter()
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        value = full_amplitude(word, mutate)
        off_count = 8 - max(word.count(colour) for colour in range(3))
        mixed_counts[(off_count, value == 0)] += 1
    require(sum(count for (off, zero), count in mixed_counts.items() if zero) == 0,
            mixed_counts)

    result = {
        "status": "PASS nonzero orbit85 C2 and all-carrier rank-nine counterguard",
        "diagonal_branch_control": {
            "graph_masks_hex": [hex(mask) for mask in GRAPH_MASKS],
            "graph_edges": [[list(EDGES[index]) for index in range(28)
                             if mask & (1 << index)] for mask in GRAPH_MASKS],
            "free_sets": [sorted(free) for free in free_sets()],
            "orbit85_case": [[3, 4, 5], [3, 4, 5, 6], [3, 4, 5, 6]],
            "pure_star_cofactor_values_by_colour": [list(row)
                                                     for row in open_values],
            "pure_normalized": True,
        },
        "tail_formula": (
            "T_ij^(ab)=1+((17i+31j+43a+59b+7ab+11ij) mod 97), i<j,a!=b"
        ),
        "reduced_C2": {
            "canonical_boolean_selector_assignment": True,
            "nonzero_tail_sensitive_leaf_weights": {
                "A2": {"12979": 1},
                "C0": {"13429": 2, "13430": 2, "13431": 2,
                       "13738": 1},
                "XF": {"13562": 1, "13565": 2, "13566": 1},
            },
            "C0_contributions_zero_because_star_selector_zero": True,
            "XF_contributions_zero_because_clause_falsity_factor_zero": True,
            "unique_contribution": contributions[0],
            "value": c2,
            "nonzero": True,
        },
        "carrier_counterguard": {
            "star_carriers": 168,
            "triangle_carriers": 560,
            "rank_histogram": {"9": 728},
            "all_four_blockers_in_rowspan_for_every_carrier": True,
            "active_star_carriers": 0,
            "active_triangle_carriers": 0,
            "minor_prime": PRIME,
            "exact_integer_minor_records": carriers,
            "minor_ledger_sha256": carrier_digest,
        },
        "x5_scope_guard": {
            "mixed_amplitude_zero_counts_by_offcount": {
                str(off): {"zero": sum(count for (o, zero), count
                                      in mixed_counts.items()
                                      if o == off and zero),
                           "nonzero": sum(count for (o, zero), count
                                         in mixed_counts.items()
                                         if o == off and not zero)}
                for off in range(1, 6)
            },
            "is_X5_source": False,
            "meaning": (
                "This source-faithful point proves that orbit85 branch support "
                "plus a nonzero parallel Tail2/C2 witness does not force an "
                "active carrier. It is not a GHZ/X5 solution and does not "
                "refute a future implication using all full mixed equations."
            ),
        },
        "fr_scope_guard": (
            "The 448 FR leaves remain epsilon-constant diagonal branch "
            "equations; none is replaced by a full X5 amplitude."
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-tail", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_tail)
    if args.check_results:
        require(OUT.exists() and json.loads(OUT.read_text()) == result,
                "stored result drift")
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("C2", result["reduced_C2"]["value"])
    print("carrier rank histogram", result["carrier_counterguard"]["rank_histogram"])
    print("minor digest", result["carrier_counterguard"]["minor_ledger_sha256"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
