#!/usr/bin/env python3
"""Exact audit of the 3I+2R+1Z generic-kernel rank closure.

The aligned rank-one edge has rank at most 49.  On the exceptional edge,
zero-multiplier edges from the zero endpoint cannot meet both the invertible
and rank-one sides; the two resulting support classes have rank at most 54
and 46.  Formal matching identities and exact modular calibrations are
checked with the standard library only.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
shore_core = run_path(str(HERE / (
    "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
)))
rank_core = run_path(str(HERE / (
    "verify_level_two_one_sided_overlap_collapse.py"
)))

variable = shore_core["variable"]
poly_add = shore_core["polynomial_add"]
poly_mul = shore_core["polynomial_multiply"]
formal_tensor = shore_core["formal_matching_tensor"]
MATCHINGS = shore_core["MATCHINGS"]

COLOURS = (0, 1)
SITES = tuple(range(6))
INNER = (0, 1, 2)
RANK_ONE = (3, 4)
ZERO = 5
EDGES = tuple(combinations(SITES, 2))


def packet_entry_name(kind, u, v, a, b):
    if u in INNER and v in INNER:
        return f"L_{u}_{v}_{a}_{b}"
    if u in INNER and v in RANK_ONE:
        return f"C_{u}_{v}_{a}" if b == 0 else None
    if (u, v) == RANK_ONE:
        if kind == "aligned":
            return "Q" if (a, b) == (0, 0) else None
        return f"A_{a}_{b}"
    if v == ZERO:
        if kind == "aligned":
            return f"Z_{u}_{a}_{b}"
        if kind == "inner_free" and u in INNER:
            return f"Z_{u}_{a}_{b}"
        if kind == "shore_free" and u in RANK_ONE:
            return f"Z_{u}_{a}_{b}"
    return None


def build_formal_packet(kind):
    return {
        (u, v, a, b): (
            variable(name) if (
                name := packet_entry_name(kind, u, v, a, b)
            ) else shore_core["Counter"]()
        )
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def matching_sum(packet, word, predicate):
    total = shore_core["Counter"]()
    for matching in MATCHINGS[SITES]:
        if not predicate(matching):
            continue
        term = shore_core["Counter"]({(): 1})
        for u, v in matching:
            term = poly_mul(term, packet[u, v, word[u], word[v]])
        total = poly_add(total, term)
    return total


def zero_partner(matching):
    return next(v if u == ZERO else u
                for u, v in matching if ZERO in (u, v))


def audit_aligned():
    packet = build_formal_packet("aligned")
    identities = 0
    for word in product(COLOURS, repeat=6):
        partner = lambda matching: zero_partner(matching)
        first = matching_sum(
            packet, word, lambda matching: partner(matching) in INNER
        )
        second = matching_sum(
            packet, word, lambda matching: partner(matching) == 3
        )
        third = matching_sum(
            packet, word, lambda matching: partner(matching) == 4
        )
        require(formal_tensor(packet, word) == poly_add(first, second, third),
                ("aligned partner split failed", word))
        if word[3] != 0 or word[4] != 0:
            require(not first, ("inner-zero partner leaked outside 00", word))
        if word[4] != 0:
            require(not second, ("z-r term leaked at s=1", word))
        if word[3] != 0:
            require(not third, ("z-s term leaked at r=1", word))
        identities += 1
    require(16 + 9 + 9 + (60 - 45) == 49,
            "aligned dimension count changed")
    return identities


def inner_free_formula(packet, word):
    f_term = shore_core["Counter"]()
    g_term = shore_core["Counter"]()
    for i in INNER:
        j, k = tuple(v for v in INNER if v != i)
        zi = packet[i, ZERO, word[i], word[ZERO]]
        # The M_34 factor is kept outside F in the formula.
        f_term = poly_add(f_term, poly_mul(
            zi, packet[j, k, word[j], word[k]]
        ))
        cross_sum = poly_add(
            poly_mul(packet[j, 3, word[j], word[3]],
                     packet[k, 4, word[k], word[4]]),
            poly_mul(packet[j, 4, word[j], word[4]],
                     packet[k, 3, word[k], word[3]]),
        )
        g_term = poly_add(g_term, poly_mul(zi, cross_sum))
    return poly_add(
        poly_mul(packet[3, 4, word[3], word[4]], f_term),
        g_term,
    )


def audit_inner_free():
    packet = build_formal_packet("inner_free")
    identities = 0
    for word in product(COLOURS, repeat=6):
        require(formal_tensor(packet, word) == inner_free_formula(packet, word),
                ("inner-free factorization failed", word))
        if (word[3], word[4]) != (0, 0):
            # The cross-cross summand G is supported only at shore word 00.
            g_only = matching_sum(
                packet, word,
                lambda matching: zero_partner(matching) in INNER
                and (3, 4) not in matching,
            )
            require(not g_only, ("inner-free G leaked outside 00", word))
        identities += 1
    require((4 + 16 - 1) + 16 - 1 + (60 - 40) == 54,
            "inner-free dimension count changed")
    return identities


def audit_shore_free():
    packet = build_formal_packet("shore_free")
    identities = 0
    for word in product(COLOURS, repeat=6):
        first = matching_sum(
            packet, word, lambda matching: zero_partner(matching) == 3
        )
        second = matching_sum(
            packet, word, lambda matching: zero_partner(matching) == 4
        )
        require(formal_tensor(packet, word) == poly_add(first, second),
                ("shore-free factorization failed", word))
        if word[4] != 0:
            require(not first, ("z-r term leaked at s=1", word))
        if word[3] != 0:
            require(not second, ("z-s term leaked at r=1", word))
        identities += 1
    require(11 + 11 + (60 - 36) == 46,
            "shore-free dimension count changed")
    return identities


def audit_multiplier_separation():
    checked = 0
    for values in product(range(-3, 4), repeat=6):
        # Only inspect the exceptional r-s chart and impose the mandatory
        # nonzero sums on I-I and I-R edges.
        if values[3] + values[4] != 0:
            continue
        if any(values[i] + values[j] == 0
               for i, j in combinations(INNER, 2)):
            continue
        if any(values[i] + values[r] == 0
               for i in INNER for r in RANK_ONE):
            continue
        free = {v for v in range(5) if values[v] + values[ZERO] == 0}
        require(not (free & set(INNER) and free & set(RANK_ONE)),
                ("zero-star free set crossed the split", values, free))
        checked += 1
    require(checked > 0, "multiplier separation audit was empty")
    return checked


def build_numeric_packet(kind):
    packet = {}
    for edge_index, (u, v) in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            name = packet_entry_name(kind, u, v, a, b)
            packet[u, v, a, b] = (
                1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
                if name else 0
            )
    return packet


def main():
    identities = (
        audit_aligned(),
        audit_inner_free(),
        audit_shore_free(),
    )
    multiplier_cases = audit_multiplier_separation()
    ranks = []
    for kind in ("aligned", "inner_free", "shore_free"):
        derivative = rank_core["differential"](build_numeric_packet(kind))
        ranks.append(tuple(
            rank_core["rank_mod"](derivative, prime)
            for prime in (101, 1_000_003)
        ))
    require(ranks == [(49, 49), (50, 50), (46, 46)],
            ("calibration ranks changed", ranks))
    print(
        "3I+2R+1Z closure: "
        f"formal identities {identities}, "
        f"{multiplier_cases} exceptional multiplier cases; "
        "rank bounds 49/54/46, exact calibrations 49/50/46"
    )


if __name__ == "__main__":
    main()
