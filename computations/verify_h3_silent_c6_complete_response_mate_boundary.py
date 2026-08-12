#!/usr/bin/env python3
"""Complete literal mate census and fixed-port bright closure for silent C6.

In the branch PS=q04=q13=0, enumerate every perfect-matching term in
G11[110000] and G22[000220], retaining endpoint heads and q decorations.
The calculation separates genuine same-word C4 bridges from physical-graph
adjacencies whose common edges change decoration.  It also exhibits the
three-term diagonal-cofactor cancellation which prevents the selected
nonzero monomial from forcing a new endpoint carrier by itself.

After adjoining the missing bright targets on the four fixed endpoint
ports, each of the nine pairs of residual target matchings has a private
non-target response coefficient.  Both alternative residual matchings for
that coefficient require an off-diagonal cell on a physical edge outside
the selected pure-anchor union.  Thus exactness gives a localized unit or
the certified nonanchor active-carrier route.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
Q = Fraction
EXPECTED_LEDGER_SHA256 = "67b4468bf0b7d6c8b69d52fe46abf90516ff6f25cef1b7d949bf3e4b8b105eef"
PINS = {
    "computations/verify_h3_four_base_silent_c6_response_lock.py":
        "dc4daa2d200f184b5d00d29c4db175320935a189f5590836afa0c724d3fdac8a",
    "notes/h3-four-base-silent-c6-response-lock.md":
        "54d7278e49e8195ed2262fa37cc89936f718b3bcd192884c6473c736a68354b8",
    "computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py":
        "59dd21c4664e8ccd88f771d0191d3db32e5fdb832e2c6de1f169cb197f9a3038",
    "notes/uniform-hall-k22-outside-endpoint-component-wedge.md":
        "cd3807d8f3f4f3d8ccda38e23c5ff291d3f0e3f1a33b69f3d2ef061b117d3347",
    "computations/verify_uniform_axis_k3_unequal_tail_reduction.py":
        "ef4c7bc9554fbf6fc5a65aef754d35359c46e0bb67014bd20060114a34cd1843",
    "notes/uniform-axis-k3-unequal-tail-reduction.md":
        "352e02a73da833fb159b24d581e7a91653fe195a76fbe3cc5aa531fd3e141993",
    "computations/verify_h3_silent_c6_five_lock_injective_no_wedge_guard.py":
        "0b4345441622f1defe74dd64c1b1877a70d2916e91df2df22ba13fa25000d702",
    "notes/h3-silent-c6-five-lock-injective-no-wedge-guard.md":
        "3853adf6006c66f2e69de4162babc00090c8257acfd9cf337e29752a68153fe0",
    "computations/verify_h3_silent_c6_first_bright_unary_escape.py":
        "bf0100b52bd21f412f8e09ebb8017d4465a8be849ae2b9c0e8a2dbe679725d35",
    "notes/h3-silent-c6-first-bright-unary-escape.md":
        "13bbba4edca4854eb484dbf8050532a480fb8e81605d57f85738d80d71b12e70",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}

VERTICES = ("P", "S", 0, 1, 2, 3, 4, 5)
FORBIDDEN_Q = {frozenset((0, 4)), frozenset((1, 3))}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def edge(left, right):
    return tuple(sorted((left, right), key=repr))


def matching(*edges):
    return tuple(sorted(edges, key=repr))


Q00_WEIGHTS = {
    edge(0, 1): Q(-2), edge(0, 2): Q(1), edge(0, 3): Q(1),
    edge(0, 5): Q(1), edge(1, 2): Q(1), edge(1, 4): Q(-3),
    edge(1, 5): Q(1), edge(2, 3): Q(-1), edge(2, 4): Q(-1),
    edge(2, 5): Q(1), edge(3, 4): Q(2), edge(3, 5): Q(1),
    edge(4, 5): Q(1),
}
BRIGHT_TAILS = {
    1: (
        (edge(2, 3), edge(4, 5)),
        (edge(2, 4), edge(3, 5)),
        (edge(2, 5), edge(3, 4)),
    ),
    2: (
        (edge(0, 1), edge(2, 5)),
        (edge(0, 2), edge(1, 5)),
        (edge(0, 5), edge(1, 2)),
    ),
}
FIXED_ROWS = {
    "G11": (0, 1, 1, 1),
    "G12": (0, 4, 1, 2),
    "G21": (3, 1, 2, 1),
    "G22": (3, 4, 2, 2),
}
UNARY_ANCHOR = frozenset((edge(0, 3), edge(1, 4), edge(2, 5)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(matching(edge(first, second), *tail))
    return tuple(answer)


MATCHINGS = perfect_matchings(VERTICES)
require(len(MATCHINGS) == 105, "the eight-vertex matching universe changed")


def full_matching(p_site, s_site, tail):
    return matching(edge("P", p_site), edge("S", s_site), *tail)


ROW_DATA = {
    "G11": {
        "word": (1, 1, 0, 0, 0, 0),
        "head": 1,
        "own_ports": frozenset((0, 1)),
        "opposite_ports": frozenset((3, 4)),
        "selected_ports": (0, 1),
        "tails": (
            (edge(2, 3), edge(4, 5)),
            (edge(2, 4), edge(3, 5)),
            (edge(2, 5), edge(3, 4)),
        ),
        "selected_tail": (edge(2, 5), edge(3, 4)),
    },
    "G22": {
        "word": (0, 0, 0, 2, 2, 0),
        "head": 2,
        "own_ports": frozenset((3, 4)),
        "opposite_ports": frozenset((0, 1)),
        "selected_ports": (3, 4),
        "tails": (
            (edge(0, 1), edge(2, 5)),
            (edge(0, 2), edge(1, 5)),
            (edge(0, 5), edge(1, 2)),
        ),
        "selected_tail": (edge(0, 1), edge(2, 5)),
    },
}


def endpoint_site(matching_value, endpoint):
    selected = next(item for item in matching_value if endpoint in item)
    return next(item for item in selected if item != endpoint)


def residual_tail(matching_value):
    return tuple(item for item in matching_value
                 if "P" not in item and "S" not in item)


def uses_physical_pair(matching_value, pair):
    pair = frozenset(pair)
    return any(frozenset(item) == pair for item in matching_value)


def decorated_term(row, matching_value):
    word = row["word"]
    head = row["head"]
    answer = []
    for left, right in matching_value:
        if left == "P" or right == "P":
            site = right if left == "P" else left
            answer.append(("p", head, site, word[site]))
        elif left == "S" or right == "S":
            site = right if left == "S" else left
            answer.append(("s", head, site, word[site]))
        else:
            answer.append(("q", left, right, word[left], word[right]))
    return tuple(sorted(answer, key=repr))


def is_c4(left, right):
    return len(set(left) ^ set(right)) == 4


def selected_bases(row):
    p_site, s_site = row["selected_ports"]
    return tuple(full_matching(p_site, s_site, tail) for tail in row["tails"])


def classify_row(name, row, other_row):
    p_selected, s_selected = row["selected_ports"]
    selected = full_matching(p_selected, s_selected, row["selected_tail"])
    own_bases = selected_bases(row)
    other_bases = selected_bases(other_row)
    selected_decorated = decorated_term(row, selected)

    forbidden = []
    records = []
    counts = Counter()
    for matching_value in MATCHINGS:
        if uses_physical_pair(matching_value, ("P", "S")):
            forbidden.append(("PS", matching_value))
            continue
        if any(uses_physical_pair(matching_value, pair)
               for pair in FORBIDDEN_Q):
            forbidden.append(("q04_or_q13", matching_value))
            continue

        p_site = endpoint_site(matching_value, "P")
        s_site = endpoint_site(matching_value, "S")
        decorated = decorated_term(row, matching_value)
        if p_site in (2, 5) or s_site in (2, 5):
            kind = "outside_endpoint_port"
        elif {p_site, s_site} <= set(row["own_ports"]):
            kind = "diagonal_cofactor_fibre"
        elif any(is_c4(matching_value, base) for base in own_bases):
            kind = "literal_same_word_C4_bridge"
        else:
            kind = "long_or_cross_word_lock"
        counts[kind] += 1

        own_adjacent = tuple(index for index, base in enumerate(own_bases)
                             if is_c4(matching_value, base))
        other_adjacent = tuple(index for index, base in enumerate(other_bases)
                               if is_c4(matching_value, base))
        identical_other_common = 0
        if other_adjacent:
            # Compare literal decorated factors, not physical edges only.
            identical_other_common = max(
                len(set(decorated) & set(decorated_term(other_row, other_bases[i])))
                for i in other_adjacent
            )
        records.append({
            "matching": matching_value,
            "decorated_term": decorated,
            "ports": (p_site, s_site),
            "tail": residual_tail(matching_value),
            "kind": kind,
            "is_selected": matching_value == selected,
            "own_word_C4_bases": own_adjacent,
            "other_word_graph_C4_bases": other_adjacent,
            "max_identical_common_factors_other_word": identical_other_common,
        })

    require(Counter(kind for kind, _matching in forbidden)
            == Counter({"PS": 15, "q04_or_q13": 22}),
            f"{name}: forbidden matching split changed")
    require(len(records) == 68, f"{name}: allowed term count changed")
    require(counts == Counter({
        "outside_endpoint_port": 36,
        "long_or_cross_word_lock": 16,
        "literal_same_word_C4_bridge": 10,
        "diagonal_cofactor_fibre": 6,
    }), f"{name}: complete mate split changed: {counts}")
    require(sum(record["is_selected"] for record in records) == 1,
            f"{name}: selected term multiplicity changed")

    bridges = [record for record in records
               if record["kind"] == "literal_same_word_C4_bridge"]
    require(all(len(record["own_word_C4_bases"]) == 1 for record in bridges),
            f"{name}: a typed bridge lost its unique base")
    for record in bridges:
        base = own_bases[record["own_word_C4_bases"][0]]
        common = set(record["decorated_term"]) & set(decorated_term(row, base))
        require(len(common) == 2,
                f"{name}: same-word C4 lost two literal common factors")

    long_records = [record for record in records
                    if record["kind"] == "long_or_cross_word_lock"]
    require(all(not record["own_word_C4_bases"] for record in long_records),
            f"{name}: a residual has a hidden same-word C4")
    graph_only = [record for record in long_records
                  if record["other_word_graph_C4_bases"]]
    require(len(graph_only) == 12,
            f"{name}: graph-only cross-word adjacency count changed")
    require(all(record["max_identical_common_factors_other_word"] <= 1
                for record in graph_only),
            f"{name}: a graph-only adjacency acquired a literal common tail")
    require(len(long_records) - len(graph_only) == 4,
            f"{name}: fully long residual count changed")

    diagonal = [record for record in records
                if record["kind"] == "diagonal_cofactor_fibre"]
    orientations = Counter(record["ports"] for record in diagonal)
    require(orientations == Counter({
        (p_selected, s_selected): 3,
        (s_selected, p_selected): 3,
    }), f"{name}: diagonal orientation split changed")
    require({record["tail"] for record in diagonal} == set(row["tails"]),
            f"{name}: diagonal fibre tails changed")

    return {
        "word": "".join(map(str, row["word"])),
        "selected_decorated_term": selected_decorated,
        "full_matching_terms": len(MATCHINGS),
        "killed_by_PS": 15,
        "killed_by_q04_or_q13_after_PS": 22,
        "surviving_terms": len(records),
        "surviving_type_counts": dict(sorted(counts.items())),
        "mate_type_counts_excluding_selected": {
            **dict(sorted(counts.items())),
            "diagonal_cofactor_fibre": 5,
        },
        "literal_same_word_C4_records": bridges,
        "long_or_cross_word_records": long_records,
        "diagonal_fibre_records": diagonal,
        "graph_only_cross_word_C4_count": len(graph_only),
        "graph_only_has_two_literal_common_factors": False,
    }


def diagonal_factor_guard():
    # Every displayed value is nonzero except the assumed q04,q13 and the
    # unused endpoint components.  The two three-term cofactors vanish:
    #   H01=1+1-2=0, H34=1+1-2=0.
    q = {edge(left, right): Q(1)
         for left in range(6) for right in range(left + 1, 6)}
    q[edge(0, 4)] = Q(0)
    q[edge(1, 3)] = Q(0)
    q[edge(3, 4)] = Q(-2)
    q[edge(1, 2)] = Q(-2)

    def tail_value(tail):
        value = Q(1)
        for item in tail:
            value *= q[item]
        return value

    h11_terms = tuple(tail_value(tail) for tail in ROW_DATA["G11"]["tails"])
    h22_terms = tuple(tail_value(tail) for tail in ROW_DATA["G22"]["tails"])
    require(h11_terms == (Q(1), Q(1), Q(-2)) and sum(h11_terms) == 0,
            "the G11 diagonal cofactor guard changed")
    require(h22_terms == (Q(1), Q(1), Q(-2)) and sum(h22_terms) == 0,
            "the G22 diagonal cofactor guard changed")
    require(h11_terms[2] and h22_terms[0],
            "a selected O monomial vanished in the guard")
    return {
        "q04": 0,
        "q13": 0,
        "q34": -2,
        "q12": -2,
        "all_other_q00": 1,
        "G11_diagonal_tail_values": [int(value) for value in h11_terms],
        "G22_diagonal_tail_values": [int(value) for value in h22_terms],
        "selected_O11_value": int(h11_terms[2]),
        "selected_O22_value": int(h22_terms[0]),
        "both_complete_diagonal_cofactors": 0,
        "meaning": (
            "the two selected nonzero monomials can be cancelled entirely "
            "by the other two terms of their own diagonal cofactors; row "
            "exactness alone does not force an endpoint mate"
        ),
    }


def response_support_terms(row_name, first_tail, second_tail):
    """Expand a fixed-port response on q00 plus two bright matchings."""

    p_site, s_site, p_colour, s_colour = FIXED_ROWS[row_name]
    q_cells = {physical: [(0, 0, value, "q%d%d:00" % physical)]
               for physical, value in Q00_WEIGHTS.items()}
    for colour, tail in ((1, first_tail), (2, second_tail)):
        for physical in tail:
            q_cells.setdefault(physical, []).append(
                (colour, colour, Q(1), "q%d%d:%d%d" % (
                    physical[0], physical[1], colour, colour
                ))
            )

    remaining = tuple(site for site in range(6)
                      if site not in (p_site, s_site))
    polynomials = {}
    for tail in perfect_matchings(remaining):
        choices = [q_cells.get(physical, ()) for physical in tail]
        if any(not options for options in choices):
            continue
        for selected in product(*choices):
            word = [None] * 6
            word[p_site] = p_colour
            word[s_site] = s_colour
            coefficient = Q(1)
            factors = []
            for physical, (left_colour, right_colour, value, name) in zip(
                    tail, selected, strict=True):
                word[physical[0]] = left_colour
                word[physical[1]] = right_colour
                coefficient *= value
                factors.append(name)
            key = tuple(word)
            polynomials.setdefault(key, []).append({
                "tail": tail,
                "factors": tuple(sorted(factors)),
                "coefficient": coefficient,
            })
    return polynomials, remaining


def prescribed_cells(word, tail):
    return tuple({
        "physical_edge": physical,
        "decoration": (word[physical[0]], word[physical[1]]),
        "offdiagonal": word[physical[0]] != word[physical[1]],
    } for physical in tail)


def fixed_port_bright_closure():
    """Choose one private row closing each of the nine bright pairs."""

    row_order = {name: index for index, name in enumerate(FIXED_ROWS)}
    records = []
    expected_witness = {
        1: ("G12", "101120"),
        2: ("G12", "100121"),
        3: ("G11", "110110"),
    }
    for first_index, first_tail in enumerate(BRIGHT_TAILS[1], 1):
        for second_index, second_tail in enumerate(BRIGHT_TAILS[2], 1):
            pure_anchors = frozenset(
                set(UNARY_ANCHOR)
                | {edge(0, 1), edge(3, 4)}
                | set(first_tail) | set(second_tail)
            )
            candidates = []
            for row_name in FIXED_ROWS:
                polynomials, remaining = response_support_terms(
                    row_name, first_tail, second_tail
                )
                target = ((1,) * 6 if row_name == "G11" else
                          (2,) * 6 if row_name == "G22" else None)
                for word, supported_terms in polynomials.items():
                    if word == target or len(supported_terms) != 1:
                        continue
                    selected = supported_terms[0]
                    alternatives = []
                    for alternate_tail in perfect_matchings(remaining):
                        if alternate_tail == selected["tail"]:
                            continue
                        cells = prescribed_cells(word, alternate_tail)
                        external = tuple(
                            cell_record for cell_record in cells
                            if cell_record["offdiagonal"]
                            and cell_record["physical_edge"] not in pure_anchors
                        )
                        alternatives.append({
                            "tail": alternate_tail,
                            "prescribed_cells": cells,
                            "external_offdiagonal_cells": external,
                        })
                    require(len(alternatives) == 2,
                            "a four-site response lost an alternate matching")
                    if all(item["external_offdiagonal_cells"]
                           for item in alternatives):
                        candidates.append((row_name, word, selected,
                                           alternatives))

            require(candidates,
                    "a bright pair lost every private nonanchor witness")
            candidates.sort(key=lambda item: (
                row_order[item[0]], item[1], item[2]["tail"],
                item[2]["factors"]
            ))
            row_name, word, selected, alternatives = candidates[0]
            word_string = "".join(map(str, word))
            require((row_name, word_string) == expected_witness[first_index],
                    "the canonical private witness changed")
            require(selected["coefficient"] == 1,
                    "the private supported monomial lost unit coefficient")
            require(all(
                any(cell_record["offdiagonal"]
                    and cell_record["physical_edge"] not in pure_anchors
                    for cell_record in alternate["prescribed_cells"])
                for alternate in alternatives
            ), "an alternate mate became anchor-contained")
            records.append({
                "X1_tail_index": first_index,
                "X2_tail_index": second_index,
                "selected_pure_anchors": tuple(sorted(pure_anchors)),
                "private_row": row_name,
                "private_word": word_string,
                "private_supported_tail": selected["tail"],
                "private_supported_factors": selected["factors"],
                "private_supported_coefficient": str(
                    selected["coefficient"]
                ),
                "alternate_mates": alternatives,
                "consequence": (
                    "if neither alternate monomial is present, this zero "
                    "coefficient is a localized ordinary source unit; "
                    "otherwise every present mate contains a nonanchor "
                    "offdiagonal q cell and enters the pinned active-carrier "
                    "route"
                ),
            })
    require(len(records) == 9,
            "the fixed-port bright-pair chart count changed")
    require(Counter((record["private_row"], record["private_word"])
                    for record in records) == Counter({
                        ("G12", "101120"): 3,
                        ("G12", "100121"): 3,
                        ("G11", "110110"): 3,
                    }), "the private-word orbit split changed")
    return records


def audit():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    rows = {
        "G11": classify_row("G11", ROW_DATA["G11"], ROW_DATA["G22"]),
        "G22": classify_row("G22", ROW_DATA["G22"], ROW_DATA["G11"]),
    }
    require(rows["G11"]["surviving_type_counts"]
            == rows["G22"]["surviving_type_counts"],
            "the two diagonal mate censuses stopped being symmetric")
    bright_records = fixed_port_bright_closure()
    ledger = {
        "branch": "PS=q04=q13=0",
        "literal_rows": rows,
        "diagonal_factor_guard": diagonal_factor_guard(),
        "fixed_port_bright_completion": {
            "records": bright_records,
            "pair_count": len(bright_records),
            "private_word_orbits": {
                "X1_tail_23_45": "G12[101120]",
                "X1_tail_24_35": "G12[100121]",
                "X1_tail_25_34": "G11[110110]",
            },
            "verdict": (
                "all nine simultaneous X1/X2 target-tail choices on the "
                "four fixed endpoint ports give an ordinary localized unit "
                "or a nonanchor offdiagonal active carrier"
            ),
        },
        "proved_routes": {
            "outside_endpoint_port": (
                "a nonzero mate has a literal nonzero complete cofactor on "
                "port 2 or 5, hence enters the pinned outside-endpoint "
                "joint-kernel/four-good dichotomy"
            ),
            "literal_same_word_C4_bridge": (
                "the mate and one selected diagonal base share exactly two "
                "identically decorated factors in the same word, so this is "
                "a source-valid typed C4 input"
            ),
        },
        "sharp_residual": {
            "long_or_cross_word_terms_per_row": 16,
            "of_which_graph_only_cross_word_C4": 12,
            "of_which_no_graph_C4_to_either_diagonal_family": 4,
            "diagonal_fibre_terms_per_row": 6,
            "diagonal_fibre_factorization": {
                "G11": "(p1_0^1*s1_1^1+p1_1^1*s1_0^1)*H01^0000",
                "G22": "(p2_3^2*s2_4^2+p2_4^2*s2_3^2)*H34^0000",
            },
            "next_needed_input": (
                "a complete companion identity synchronizing the 16 long "
                "terms with one diagonal word, or an exact same-star lock "
                "kernel; physical C4 adjacency to the other diagonal word "
                "is insufficient because it retains at most one identical "
                "decorated factor"
            ),
        },
        "verdict": (
            "complete literal mate boundary: 36 outside and 10 same-word "
            "C4 terms route per row; 16 long/cross-word terms plus the "
            "six-term diagonal cofactor fibre remain, and a rational "
            "two-row guard proves the selected O monomials do not force a "
            "new endpoint mate.  After the missing bright targets are "
            "adjoined on the four fixed ports, however, all nine target-tail "
            "pairs force a source unit or nonanchor active carrier"
        ),
        "scope": (
            "complete in the two displayed zero response coefficients; the "
            "rational two-row guard is not a full source.  The positive "
            "bright closure is complete only for p1@0,s1@1,p2@3,s2@4.  "
            "Additional endpoint components at outside sites 2 or 5 enter "
            "the pinned complete-column deletion/active-arm theorem; core-"
            "port endpoint reselections are not classified here"
        ),
        "pins": PINS,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"complete response-mate ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 silent-C6 complete response-mate boundary: PASS (exact)")
    print("per row: 105 total; 68 survive PS=q04=q13=0")
    print("per row: 36 outside, 10 literal C4, 16 long/cross-word, 6 diagonal")
    print("graph-only other-word C4s are not literal common-tail bridges")
    print("two-row rational guard: O11,O22 nonzero while both cofactors vanish")
    print("fixed-port bright completion: 9/9 unit or nonanchor active carrier")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
