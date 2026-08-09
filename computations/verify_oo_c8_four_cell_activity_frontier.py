#!/usr/bin/env python3
"""Coefficient-aware four-cell frontier for the alternating-C8 OO chart."""

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product

import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


PURE_ONE = (1,) * 8


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pure_one_cores(blocks):
    cores = set()
    for matching in base.perfect_matchings(base.VERTICES):
        cells = tuple(sorted(base.key(u, v, 1, 1) for u, v in matching))
        missing = tuple(cell for cell in cells if cell not in blocks)
        require(len(missing) in (3, 4), "unexpected old pure-1 matching content")
        cores.add(missing)
    return tuple(sorted(cores))


def four_cell_completions(blocks):
    candidates = frontier.all_unoccupied_cells(blocks)
    supports = set()
    for core in pure_one_cores(blocks):
        if len(core) == 4:
            supports.add(core)
            continue
        core_set = set(core)
        for extra in candidates:
            if extra not in core_set:
                supports.add(tuple(sorted(core + (extra,))))
    return tuple(sorted(supports))


def cofactor_terms(blocks, added, deleted_pair):
    """Return source-labelled decorated matching terms of one arm cofactor."""

    residual = tuple(v for v in base.VERTICES if v not in deleted_pair)
    added_by_pair = defaultdict(list)
    for index, cell in enumerate(added):
        u, v, i, j = cell
        added_by_pair[(u, v)].append((i, j, 1 << index))
    terms = []
    for matching in base.perfect_matchings(residual):
        choices = []
        for u, v in matching:
            available = [
                (i, j, 0, value)
                for i in base.COLORS
                for j in base.COLORS
                if (value := base.entry(blocks, u, v, i, j))
            ]
            available.extend(
                (i, j, mask, F(1))
                for i, j, mask in added_by_pair[(u, v)]
            )
            if not available:
                choices = []
                break
            choices.append(available)
        for selected in product(*choices) if choices else ():
            word = [None] * len(residual)
            mask = 0
            coefficient = F(1)
            for (u, v), (i, j, local_mask, value) in zip(
                matching, selected, strict=True
            ):
                word[residual.index(u)] = i
                word[residual.index(v)] = j
                mask |= local_mask
                coefficient *= value
            terms.append((tuple(word), mask, tuple(matching), coefficient))
    return tuple(terms)


def leading_matching(blocks, added, arm):
    terms = cofactor_terms(blocks, added, arm)
    require(terms, f"empty cofactor at {arm}")
    # Variables are ordered by canonical cell order.  This is a fixed,
    # source-labelled lex order, followed by endpoint word and matching.
    def order(term):
        word, mask, matching, _coefficient = term
        exponent = tuple(bool(mask & (1 << index)) for index in range(len(added)))
        return exponent, word, matching

    return max(terms, key=order)


def matching_union_type(first, second):
    """Classify the two coloured matching union as path + even cycles."""

    tagged_edges = tuple((u, v, chart) for chart, matching in enumerate((first, second)) for u, v in matching)
    adjacency = defaultdict(list)
    for index, (u, v, _chart) in enumerate(tagged_edges):
        adjacency[u].append(index)
        adjacency[v].append(index)
    endpoints = sorted(vertex for vertex, edges in adjacency.items() if len(edges) == 1)
    require(endpoints == [base.Q, base.R], "cofactor union endpoints changed")
    require(all(len(edges) in (1, 2) for edges in adjacency.values()), "cofactor union is not path/cycles")

    unused = set(range(len(tagged_edges)))

    def consume(start):
        current = start
        previous_edge = None
        length = 0
        while True:
            next_edges = [edge for edge in adjacency[current] if edge in unused]
            if not next_edges:
                return length
            edge = min(next_edges)
            unused.remove(edge)
            u, v, _chart = tagged_edges[edge]
            current = v if current == u else u
            previous_edge = edge
            length += 1

    path_length = consume(base.Q)
    require(path_length > 0 and not any(edge in unused for edge in adjacency[base.R]), "q-r path failed")
    cycles = []
    while unused:
        edge = min(unused)
        cycles.append(consume(tagged_edges[edge][0]))
    require(path_length + sum(cycles) == 6, "cofactor union edge census changed")
    require(all(length % 2 == 0 for length in (path_length, *cycles)), "alternation parity failed")
    return path_length, tuple(sorted(cycles))


def main():
    blocks = base.build_packet()
    cores = pure_one_cores(blocks)
    core_sizes = Counter(map(len, cores))
    require(core_sizes == Counter({4: 75, 3: 30}), "pure-one core census changed")

    supports = four_cell_completions(blocks)
    activity = Counter()
    disposition = Counter()
    shore_types = Counter()
    unit_histogram = Counter()
    leading_union_types = Counter()
    leading_unit_relations = Counter()
    first_unrelated = None
    unrelated_records = []
    first_multiclass = None
    for added in supports:
        active_arms = tuple(
            arm
            for arm in frontier.ARMS
            if frontier.is_support_active(blocks, added, arm)
        )
        activity[active_arms] += 1
        if active_arms != frontier.ARMS:
            continue
        leading = tuple(leading_matching(blocks, added, arm) for arm in frontier.ARMS)
        union_type = matching_union_type(leading[0][2], leading[1][2])
        leading_union_types[union_type] += 1
        shore_types[tuple(sorted(frontier.shore_type(cell) for cell in added))] += 1

        residuals = frontier.target_residuals(
            frontier.tensor_polynomials(blocks, added)
        )
        pure_equation = residuals.get(PURE_ONE)
        require(pure_equation is not None and 0 in pure_equation, "missing X1 equation")
        unit_rows = tuple(
            (word, polynomial)
            for word, polynomial in residuals.items()
            if len(polynomial) == 1
        )
        unit_histogram[len(unit_rows)] += 1
        if unit_rows:
            unit_masks = {next(iter(polynomial)) for _, polynomial in unit_rows}
            first_mask, second_mask = leading[0][1], leading[1][1]
            if (first_mask | second_mask) in unit_masks:
                leading_unit_relations["union"] += 1
            elif first_mask in unit_masks or second_mask in unit_masks:
                leading_unit_relations["one-leading"] += 1
            elif (first_mask ^ second_mask) in unit_masks:
                leading_unit_relations["symmetric-difference"] += 1
            else:
                leading_unit_relations["unrelated"] += 1
                unrelated_records.append(
                    (added, union_type, (first_mask, second_mask), tuple(sorted(unit_masks)))
                )
                if first_unrelated is None:
                    first_unrelated = (added, leading, unit_rows)
            disposition["monomial_unit"] += 1
            continue
        disposition["true_multiclass_before_laurent"] += 1
        if first_multiclass is None:
            first_multiclass = (added, pure_equation, residuals)

    print("alternating-C8 four-cell active frontier: PASS")
    print(f"pure-one cores by missing-cell count={dict(sorted(core_sizes.items()))}")
    print(f"distinct four-cell supports carrying X1={len(supports)}")
    print(f"activity census={dict(sorted(activity.items(), key=str))}")
    print(f"both-active shore types={dict(sorted(shore_types.items()))}")
    print(f"both-active target disposition={dict(sorted(disposition.items()))}")
    print(f"unit-row-count histogram={dict(sorted(unit_histogram.items()))}")
    print(f"leading cofactor-union types={dict(sorted(leading_union_types.items()))}")
    print(f"leading/unit mask relations={dict(sorted(leading_unit_relations.items()))}")
    if first_unrelated is not None:
        print(f"first leading-mask counterguard={first_unrelated}")
        print(f"all leading-mask counterguard summaries={unrelated_records}")
    if first_multiclass is None:
        print("every both-active support has a literal Laurent monomial unit")
    else:
        added, pure_equation, residuals = first_multiclass
        print(f"first true multiclass support={added}")
        print(f"pure-one equation={pure_equation}")
        print(f"residual rows={len(residuals)}")

    require(len(supports) == 7200, "four-cell support census changed")
    require(
        activity
        == Counter({frontier.ARMS: 5110, (frontier.ARMS[1],): 1530,
                    (frontier.ARMS[0],): 530, (): 30}),
        "four-cell activity census changed",
    )
    require(
        disposition == Counter({"monomial_unit": 5110}),
        "a both-active four-cell support escaped the monomial layer",
    )
    require(
        leading_union_types
        == Counter({(2, (2, 2)): 2955, (4, (2,)): 1853, (6, ()): 302}),
        "leading cofactor-union census changed",
    )
    require(
        leading_unit_relations
        == Counter({"one-leading": 2923, "union": 2180, "unrelated": 7}),
        "leading/unit relation census changed",
    )
    for support, _union_type, _leading_masks, unit_masks in unrelated_records:
        exceptional = tuple(cell for cell in support if cell[2:] != (1, 1))
        require(
            exceptional == ((3, 4, 0, 1),),
            "a lex counterguard left the single 34:01 exceptional-cell chart",
        )
        exceptional_index = support.index(exceptional[0])
        require(
            (1 << exceptional_index) in unit_masks,
            "the alternate exceptional-cell private pivot disappeared",
        )


if __name__ == "__main__":
    main()
