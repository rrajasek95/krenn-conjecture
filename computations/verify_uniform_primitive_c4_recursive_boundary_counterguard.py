#!/usr/bin/env python3
"""Exact recursive boundary guard above the primitive-C4 wandering packet.

The first six singleton debts of the six-site wandering packet have a
unique support-minimal simultaneous C4 completion.  We give its forced
products, one normalized Gaussian realization, and an integral four-cell
completion of the reopened pure-zero and two boundary rows.  The resulting
26-cell packet has all three normalized pure rows and eleven cancelling
mixed rows, but 33 residual mixed debts.

Every residual debt still admits an anchor-contained C4 occurrence whose
least active core is a single matching-covered four-cycle.  Thus neither
physical-window intersection nor support size gives a descending recursive
potential.  The signed exponent system of the thirteen primitive binomial
subrows has no odd dependency.  Its smallest recurrences are two literal
two-row, path-independent common-core components, with fixed physical tail
02 (tail colours 00/11) or 15 (tail colours 00/22).

This is a finite-layer counterguard, not an exact ternary source.  It pins
the missing full-completion theorem: complete-row equations must either
make an anchor-contained common core projectable despite arbitrary extra
terms, or force a unit / active outside fan.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = (
    "computations/"
    "verify_uniform_primitive_c4_source_label_wandering_counterguard.py"
)
PINS = {
    BASE_PATH:
        "f5a780c40f7be8a959e56e47ce06ff04ae644694d0f30c20180df0bd1259491b",
    "notes/uniform-primitive-c4-source-label-wandering-counterguard.md":
        "2422da8b68fb85dc58bfa33a95af5fe66c717c621d2c866338610c586d9341aa",
}
EXPECTED_LEDGER_SHA256 = (
    "c20f8a765d0c744414dc766a0e9afe2981bf0f222687c5e76f48d92afdf498b1"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def word_text(word):
    return "".join(map(str, word))


def matching_text(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def build_second_layer(base):
    cells, anchors = base.build_packet()

    # Unique seven-cell support-minimal simultaneous C4 completion of the
    # six singleton debts.  This is one gauge normalization of the forced
    # product equations ab=1, ac=i, d=1, ef=i, eg=-1.
    additions = {
        (0, 3, 0, 1): base.ONE,
        (2, 5, 0, 1): base.ONE,
        (2, 4, 2, 0): base.I,
        (3, 4, 0, 0): base.ONE,
        (1, 4, 0, 2): base.ONE,
        (3, 5, 0, 1): base.I,
        (2, 5, 2, 0): (-1, 0),
    }

    # A support-minimal four-cell closure of the pure-zero deficit and the
    # two reopened L/R boundary rows.  It also creates the two further
    # cancelling boundary faces 000020 and 000100.
    closure = {
        (2, 4, 0, 0): base.ONE,
        (3, 5, 0, 0): base.ONE,
        (3, 5, 1, 0): (-1, 0),
        (2, 4, 0, 2): base.ONE,
    }
    for label, value in additions.items():
        base.add_cell(cells, label, value)
    for label, value in closure.items():
        base.add_cell(cells, label, value)
    require(len(cells) == 26, "the second-layer packet lost a cell")
    return cells, anchors, additions, closure


def six_debt_c4_candidates(base, cells):
    original, _ = base.build_packet()
    fibres = base.live_fibres(original)
    matchings = tuple(base.perfect_matchings(range(6)))
    debt_words = (
        "010111", "020002", "022102",
        "101000", "101021", "202220",
    )
    candidates = {}
    for text in debt_words:
        word = tuple(map(int, text))
        selected = fibres[word][0][0]
        records = []
        for matching in matchings:
            if matching == selected or len(set(matching) & set(selected)) != 1:
                continue
            labels = tuple(base.cell(left, right, word[left], word[right])
                           for left, right in matching)
            new = frozenset(label for label in labels if label not in original)
            records.append((matching, new))
        require(len(records) == 6,
                f"the C4 mate count changed for {text}")
        candidates[text] = tuple(records)

    minimum = 10**9
    minimizers = []
    for choice in itertools.product(*(candidates[text] for text in debt_words)):
        support = frozenset().union(*(record[1] for record in choice))
        if len(support) < minimum:
            minimum = len(support)
            minimizers = [(choice, support)]
        elif len(support) == minimum:
            minimizers.append((choice, support))
    require(minimum == 7 and len(minimizers) == 1,
            f"the unique seven-cell completion changed: {minimum}, "
            f"{len(minimizers)}")
    actual_new = frozenset(cells) - frozenset(original)
    seven = minimizers[0][1]
    require(seven <= actual_new,
            "the frozen packet stopped containing the unique minimizer")
    return {
        "debt_words": list(debt_words),
        "C4_choices_per_debt": 6,
        "simultaneous_choices_audited": 6**6,
        "minimum_new_cells": minimum,
        "number_of_minimizers": len(minimizers),
        "unique_new_support": [list(label) for label in sorted(seven)],
    }


def audit_forced_product_theorem(base, additions):
    a = additions[(0, 3, 0, 1)]
    b = additions[(2, 5, 0, 1)]
    c = additions[(2, 4, 2, 0)]
    d = additions[(3, 4, 0, 0)]
    e = additions[(1, 4, 0, 2)]
    f = additions[(3, 5, 0, 1)]
    g = additions[(2, 5, 2, 0)]
    products = {
        "a*b": base.gmul(a, b),
        "a*c": base.gmul(a, c),
        "d": d,
        "e*f": base.gmul(e, f),
        "e*g": base.gmul(e, g),
    }
    require(products == {
        "a*b": base.ONE,
        "a*c": base.I,
        "d": base.ONE,
        "e*f": base.I,
        "e*g": (-1, 0),
    }, f"the six-debt product equations changed: {products}")

    # These two products are precisely the two new common C4 core terms.
    # Their old opposite terms are (-1)*i=-i, so both recurrent cores cancel
    # for every nonzero factorization satisfying the displayed equations,
    # not only for the chosen gauge a=e=1.
    old_opposite = base.gmul((-1, 0), base.I)
    require(products["a*c"] == products["e*f"]
            == base.gneg(old_opposite) == base.I,
            "the forced common-core cancellation changed")
    return {
        "variables": {
            "a": "03:01", "b": "25:01", "c": "24:20",
            "d": "34:00", "e": "14:02", "f": "35:01",
            "g": "25:20",
        },
        "forced_product_equations": {
            name: base.gtext(value) for name, value in products.items()
        },
        "restricted_uniform_conclusion": (
            "every support-minimal one-C4-mate completion of all six debts "
            "contains both fixed-tail path-independent common-core "
            "recurrences, independent of the two residual gauge choices"
        ),
    }


def audit_packet(base, cells):
    fibres = base.live_fibres(cells)
    sums = {word_text(word): base.gsum(term[1] for term in terms)
            for word, terms in fibres.items()}
    pure = {text: base.gtext(sums[text])
            for text in ("000000", "111111", "222222")}
    require(pure == {"000000": "1", "111111": "1", "222222": "1"},
            f"a normalized row changed: {pure}")

    cancelled = {
        text: fibres[tuple(map(int, text))]
        for text in (
            "000020", "000021", "000100", "002100", "002121",
            "010111", "020002", "022102", "101000", "101021",
            "202220",
        )
    }
    require(all(base.gsum(term[1] for term in terms) == base.ZERO
                for terms in cancelled.values()),
            "a frozen second-layer cancellation reopened")
    require(Counter(map(len, cancelled.values())) == Counter({2: 9, 4: 2}),
            "the binomial/four-term cancellation histogram changed")

    debts = {
        word: (terms, sums[word_text(word)])
        for word, terms in fibres.items()
        if len(set(word)) > 1 and sums[word_text(word)] != base.ZERO
    }
    require(len(debts) == 33,
            f"the recursive mixed debt count changed: {len(debts)}")
    require(Counter(len(terms) for terms, _ in debts.values())
            == Counter({1: 28, 3: 5}),
            "the recursive debt occurrence histogram changed")
    return fibres, cancelled, debts, {
        "decorated_cells": len(cells),
        "nonzero_supported_word_fibres": len(fibres),
        "normalized_pure_rows": pure,
        "cancelled_mixed_rows": len(cancelled),
        "cancelled_row_size_histogram": dict(sorted(
            Counter(map(len, cancelled.values())).items())),
        "residual_mixed_debts": len(debts),
        "residual_debt_size_histogram": dict(sorted(
            Counter(len(terms) for terms, _ in debts.values()).items())),
    }


def c4_core(base, left, right):
    tail, window = base.c4_data(left, right)
    symmetric = set(left) ^ set(right)
    degree = Counter(site for pair in symmetric for site in pair)
    require(set(degree) == set(window) and set(degree.values()) == {2},
            "a primitive core stopped being a four-cycle")
    # A C4 is connected, every edge lies in one of its two perfect matchings,
    # and hence is matching-covered.  This is exactly the cycle branch of
    # the read-only U7H least-core theorem.
    require(len(symmetric) == 4,
            "the primitive core stopped having four allowed edges")
    return tail, window


def c4_bipartition(left, right):
    edges = set(left) ^ set(right)
    vertices = sorted(set().union(*edges))
    colour = {vertices[0]: 0}
    frontier = [vertices[0]]
    while frontier:
        vertex = frontier.pop()
        for edge in edges:
            if vertex not in edge:
                continue
            neighbour = edge[0] if edge[1] == vertex else edge[1]
            expected = 1 - colour[vertex]
            if neighbour in colour:
                require(colour[neighbour] == expected,
                        "a C4 core lost bipartiteness")
            else:
                colour[neighbour] = expected
                frontier.append(neighbour)
    shores = tuple(sorted(
        tuple(sorted(vertex for vertex in vertices if colour[vertex] == side))
        for side in (0, 1)
    ))
    require(tuple(map(len, shores)) == (2, 2),
            "a C4 core lost its two bistar shores")
    return shores


def recursive_completion_audit(base, cells, anchors, fibres, debts):
    matchings = tuple(base.perfect_matchings(range(6)))
    anchor_union = {pair for matching in anchors.values() for pair in matching}
    histogram = Counter()
    selected_windows = []
    records = []
    for word in sorted(debts):
        terms, value = debts[word]
        live = {term[0] for term in terms}
        candidates = []
        for matching in matchings:
            if matching in live:
                continue
            neighbours = [term for term in terms
                          if len(set(matching) & set(term[0])) == 1]
            if not neighbours:
                continue
            labels = tuple(base.cell(left, right, word[left], word[right])
                           for left, right in matching)
            new = frozenset(label for label in labels if label not in cells)
            escaping = frozenset(
                label for label in new
                if label[:2] not in anchor_union and label[2] != label[3]
            )
            if escaping:
                continue
            neighbour = min(neighbours, key=lambda term: term[0])
            tail, window = c4_core(base, neighbour[0], matching)
            candidates.append((len(new), matching, new, neighbour, tail, window))
        require(candidates,
                f"a residual debt forced an outside offdiagonal cell: "
                f"{word_text(word)}")
        chosen = min(candidates, key=lambda item: (item[0], item[1]))
        histogram[(len(candidates), chosen[0])] += 1
        selected_windows.append(set(chosen[5]))
        records.append({
            "word": word_text(word),
            "current_occurrences": len(terms),
            "current_sum": base.gtext(value),
            "anchor_contained_C4_choices": len(candidates),
            "least_new_cells": chosen[0],
            "reference_matching": matching_text(chosen[3][0]),
            "repair_matching": matching_text(chosen[1]),
            "tail": list(chosen[4]),
            "window": list(chosen[5]),
        })
    common = set.intersection(*selected_windows)
    require(not common,
            f"the deterministic recursive windows acquired a common site: "
            f"{common}")
    require(histogram == Counter({
        (3, 1): 6, (4, 1): 5, (2, 2): 5, (2, 1): 4,
        (4, 2): 4, (3, 2): 3, (8, 1): 2, (5, 1): 2,
        (1, 2): 2,
    }), f"the recursive C4 completion histogram changed: {histogram}")
    return {
        "residual_debts_audited": len(records),
        "every_debt_has_anchor_contained_C4_completion": True,
        "candidate_count_and_least_new_cell_histogram": [
            [list(key), count] for key, count in sorted(histogram.items())
        ],
        "least_core_type": (
            "single C4: connected, matching-covered, degree two, two PMs"
        ),
        "deterministic_repair_window_intersection": sorted(common),
        "records": records,
    }


def paired_subrows(base, cancelled):
    pairs = []
    for text, terms in sorted(cancelled.items()):
        if len(terms) == 2:
            pairs.append((text, terms[0], terms[1]))
            continue
        positive = [term for term in terms if term[1] in (base.ONE, base.I)]
        negative = [term for term in terms
                    if term[1] in ((-1, 0), (0, -1))]
        require(len(positive) == len(negative) == 2,
                f"the four-term sign split changed on {text}")
        matching = min(
            itertools.permutations(negative),
            key=lambda permutation: sum(
                len(set(left[2]) ^ set(right[2]))
                for left, right in zip(positive, permutation, strict=True)
            ),
        )
        for index, (left, right) in enumerate(
                zip(positive, matching, strict=True)):
            pairs.append((f"{text}{chr(ord('a') + index)}", left, right))
    require(len(pairs) == 13,
            f"the primitive paired subrow count changed: {len(pairs)}")
    require(all(len(set(left[2]) ^ set(right[2])) == 4
                for _, left, right in pairs),
            "a paired subrow stopped being a primitive decorated C4")
    return pairs


def gf2_rank(rows):
    rows = [sum((int(value) & 1) << column
                for column, value in enumerate(row)) for row in rows]
    rank = 0
    column = 0
    width = max((row.bit_length() for row in rows), default=0)
    while column < width:
        pivot = next((index for index in range(rank, len(rows))
                      if rows[index] & (1 << column)), None)
        if pivot is None:
            column += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(len(rows)):
            if index != rank and rows[index] & (1 << column):
                rows[index] ^= rows[rank]
        rank += 1
        column += 1
    return rank


def holonomy_audit(base, cells, pairs):
    labels = sorted(cells)
    exponent_rows = [
        [int(label in left[2]) - int(label in right[2])
         for _, left, right in pairs]
        for label in labels
    ]
    rank = gf2_rank(exponent_rows)
    augmented_rank = gf2_rank(exponent_rows + [[1] * len(pairs)])
    require(rank == augmented_rank == 10,
            "an odd signed dependency appeared in the paired component")

    # Identify exact repeated exponent columns, including orientation.
    columns = [tuple(row[column] for row in exponent_rows)
               for column in range(len(pairs))]
    duplicates = []
    for left_index, right_index in itertools.combinations(range(len(pairs)), 2):
        if columns[left_index] == columns[right_index]:
            duplicates.append((pairs[left_index], pairs[right_index]))
    duplicate_names = [tuple(record[0] for record in duplicate)
                       for duplicate in duplicates]
    require(duplicate_names == [
        ("000021b", "101021"),
        ("002100b", "022102"),
    ], f"the exact two-row recurrences changed: {duplicate_names}")

    recurrent = []
    expected = {
        ("000021b", "101021"): (
            (0, 2), (0, 0), (1, 1), (1, 3, 4, 5), ((1, 5), (3, 4))),
        ("002100b", "022102"): (
            (1, 5), (0, 0), (2, 2), (0, 2, 3, 4), ((0, 2), (3, 4))),
    }
    for first, second in duplicates:
        first_name, first_left, first_right = first
        second_name, second_left, second_right = second
        first_tail, first_window = c4_core(
            base, first_left[0], first_right[0])
        second_tail, second_window = c4_core(
            base, second_left[0], second_right[0])
        require((first_tail, first_window) == (second_tail, second_window),
                "a repeated exponent row lost physical placement")
        tail_label_1 = next(label for label in first_left[2]
                            if label[:2] == first_tail)
        tail_label_2 = next(label for label in second_left[2]
                            if label[:2] == second_tail)
        shores = c4_bipartition(first_left[0], first_right[0])
        observed = (
            first_tail, tail_label_1[2:], tail_label_2[2:],
            first_window, shores,
        )
        require(observed == expected[(first_name, second_name)],
                f"the recurrent endpoint/tail labels changed: {observed}")
        recurrent.append({
            "rows": [first_name, second_name],
            "fixed_tail": list(first_tail),
            "tail_colours": [list(tail_label_1[2:]), list(tail_label_2[2:])],
            "fixed_C4_window": list(first_window),
            "fixed_bistar_shores": [list(shore) for shore in shores],
            "chosen_ordered_bistar_endpoints": list(shores[0]),
            "common_decorated_exponent_difference": True,
            "signed_holonomy": "+1",
        })
    return {
        "primitive_binomial_subrows": len(pairs),
        "GF2_exponent_rank": rank,
        "GF2_rank_after_odd_character_row": augmented_rank,
        "odd_integer_holonomy_possible": False,
        "smallest_recurrent_cycles": recurrent,
    }


def main():
    pin_dependencies()
    base = load(BASE_PATH, "recursive_primitive_c4_base")
    cells, anchors, additions, closure = build_second_layer(base)
    minimum = six_debt_c4_candidates(base, cells)
    forced_products = audit_forced_product_theorem(base, additions)
    fibres, cancelled, debts, packet = audit_packet(base, cells)
    recursive = recursive_completion_audit(
        base, cells, anchors, fibres, debts)
    holonomy = holonomy_audit(base, cells, paired_subrows(base, cancelled))
    ledger = {
        "pins": PINS,
        "second_layer_packet": packet,
        "unique_first_six_debt_completion": minimum,
        "forced_product_theorem": forced_products,
        "seven_cell_values": {
            str(label): base.gtext(value)
            for label, value in sorted(additions.items())
        },
        "four_cell_normalization_boundary_closure": {
            str(label): base.gtext(value)
            for label, value in sorted(closure.items())
        },
        "recursive_residual_audit": recursive,
        "signed_holonomy": holonomy,
        "read_only_U7H_use": (
            "each chosen least repair core is independently verified here "
            "to be the single-C4 cycle branch; U7H supplies no relation "
            "between distinct colouring fibres"
        ),
        "counterguard": (
            "all 33 residual mixed debts admit an anchor-contained C4 "
            "completion, the selected physical windows have empty total "
            "intersection, support only increases, and the present exact "
            "exponent component has no odd character"
        ),
        "positive_routing_output": (
            "two exact two-row recurrent components already have a fixed "
            "physical tail, fixed C4 window, path-independent decorated "
            "core, and two distinct pure tail colours"
        ),
        "missing_full_completion_theorem": (
            "in a complete source row web, a recurrent fixed-tail common-"
            "core component either admits a source-provenant projector "
            "through all extra matching terms, or those extra terms force "
            "an odd Laurent unit, an anchor-safe deletion, or an active "
            "outside private-site fan"
        ),
        "scope": (
            "finite exact recursive boundary counterguard, not an exact "
            "ternary source and not a proof that arbitrary multiterm row "
            "completion preserves the displayed projector"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"recursive C4 ledger changed: {digest}")
    print("primitive-C4 recursive boundary routing: COUNTERGUARD")
    print("26 cells; pure rows normalized; 11 mixed rows cancelled")
    print("33 residual debts: each has an anchor-contained least C4 core")
    print("13 paired relations: no odd holonomy; two exact 2-row recurrences")
    print("positive exit: fixed-tail, path-independent common-core components")
    print("missing: complete-row projection or unit/deletion/active-fan theorem")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
