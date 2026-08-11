#!/usr/bin/env python3
"""E3 closes the h=3 single-even-cycle target-coloop exchange physically.

For coloop/outside matching bases M,N, let a,b be their complete five-word
evaluation vectors and h the exact source target vector.  The E3 matching-
exchange coefficients are the 3x3 minors det(a,b,h).  If one is nonzero,
perfect-matching expansion selects a third literal base K distinct from M,N.
Because M triangle N is one C6 or C8, every such K uses an edge outside the
two-base union.  It is therefore either off the selected three-anchor union
or explicitly carried by the third anchor/strict-Hall web.

An earlier version froze an abstract five-vector example with every E3
coefficient zero.  That example omitted a mandatory physical zero.  In the
augmented eight-site one-bad source, both response matchings avoid the direct
P--S edge, while endpoint colour zero is absent from every P/S star.  Hence
both matching monomials vanish on the literal unary word 0^8.  On the three
literal words (t^8,d,0^8), the E3 determinant is therefore exactly
a_t b_d, the already localized E2 minor, and is nonzero.  Its third matching
has nonzero 0^8 evaluation and must contain the direct cell P--S:00.

The abstract flat packet is retained only as a regression guard showing why
unlabelled five-vectors are insufficient.  It is not a physical boundary.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_four_hole_exchange.py":
        "5283fae67a31ea3c9794fc8bbf351f7da5bc8251490dbdffbef04bde1f2a987f",
    "notes/h3-axis-target-coloop-four-hole-exchange.md":
        "9aa3a6e9315cc52769f0124188a17e69b6165fd45c04b21aa7203a4d70d5e341",
    "computations/verify_n8_chart26_c4_exchange_3cell.py":
        "4398d15df3a5f0b34c2745fdb7087a289452ed03983d22431c4f20d116f019c6",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "4c8c63563892c8adb454098ea3508552e5afcb3c13d49e15058bdca38271eaaa"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def rank(rows):
    matrix = [[Q(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def det3(first, second, third, indices):
    i, j, k = indices
    return (
        first[i] * (second[j] * third[k] - second[k] * third[j])
        - first[j] * (second[i] * third[k] - second[k] * third[i])
        + first[k] * (second[i] * third[j] - second[j] * third[i])
    )


def all_e3(first, second, third):
    return {indices: det3(first, second, third, indices)
            for indices in combinations(range(len(first)), 3)}


def audit_e3_rank_dichotomy():
    # This is deliberately only the old *unlabelled* five-vector test.  The
    # physically labelled audit below proves that its flat sample violates
    # the mandatory unary-word zeros of response matching bases.
    target = (Q(1), Q(0), Q(0), Q(1), Q(1))

    # E3-flat boundary.  The outside vector has zero target entry but is
    # nonzero on a crossed word.  E2 is active, while h=a+b makes every E3
    # determinant zero.
    a_flat = (Q(1), Q(1), Q(2), Q(3), Q(4))
    b_flat = tuple(target[index] - a_flat[index]
                   for index in range(5))
    require(b_flat[0] == 0 and b_flat[1] != 0,
            "the flat coloop/outside evaluations changed")
    delta_flat = a_flat[0] * b_flat[1] - a_flat[1] * b_flat[0]
    require(delta_flat == -1,
            "the flat boundary lost its nonzero E2 exchange")
    flat_e3 = all_e3(a_flat, b_flat, target)
    require(not any(flat_e3.values())
            and rank((a_flat, b_flat, target)) == 2,
            "the exact E3-flat word plane changed")

    # Rank-three branch: one perturbation makes a literal E3 coefficient
    # nonzero.  The determinant is the coefficient with which a third
    # matching base can survive after M,N cancel separately.
    a_curved = a_flat
    b_curved = list(b_flat)
    b_curved[2] += 1
    b_curved = tuple(b_curved)
    curved_e3 = all_e3(a_curved, b_curved, target)
    nonzero = {indices: value for indices, value in curved_e3.items()
               if value}
    require(rank((a_curved, b_curved, target)) == 3 and nonzero,
            "the curved word plane lost its E3 detector")

    # If a,b are independent (guaranteed by the nonzero target/outside E2
    # minor), all E3 vanish iff h lies in span(a,b).
    require(rank((a_flat, b_flat)) == 2,
            "the E2-flat matching pair became dependent")
    require((not any(flat_e3.values()))
            == (rank((a_flat, b_flat, target)) == 2),
            "E3 vanishing stopped detecting the two-base target plane")
    require((not any(curved_e3.values()))
            == (rank((a_curved, b_curved, target)) == 2),
            "E3 rank detection failed on the curved sample")

    # E4 is the row-Laplace identity among the four 3x3 minors.  Verify it
    # for every four-state subset and both matching rows, in both strata.
    e4_checks = 0
    for first, second, e3 in (
            (a_flat, b_flat, flat_e3),
            (a_curved, b_curved, curved_e3)):
        for indices in combinations(range(5), 4):
            c, d, e, f = indices
            # C_cde is det(a,b,h) on those indices.  The standard maximal-
            # minor signs are (-,+,-,+) after deleting c,d,e,f.
            for row in (first, second):
                value = (
                    row[c] * e3[(d, e, f)]
                    - row[d] * e3[(c, e, f)]
                    + row[e] * e3[(c, d, f)]
                    - row[f] * e3[(c, d, e)]
                )
                require(value == 0, "the E4 Laplace coherence changed")
                e4_checks += 1

    return {
        "source_target_vector": [str(value) for value in target],
        "flat_matching_M": [str(value) for value in a_flat],
        "flat_matching_N": [str(value) for value in b_flat],
        "flat_E2_minor": str(delta_flat),
        "flat_E3_nonzero_count": 0,
        "flat_three_row_rank": 2,
        "flat_relation": "H=M+N",
        "curved_E3_nonzero": {
            str(indices): str(value) for indices, value in nonzero.items()
        },
        "curved_three_row_rank": 3,
        "E4_checks": e4_checks,
        "E4_effect_on_flat_stratum": "identically zero",
        "status": (
            "formal five-vector regression only; physically retracted by "
            "the mandatory response-base zeros on 0^8"
        ),
    }


P, S = 6, 7
TARGET_HOLES = (0, 1)
OUTSIDE_HOLES = (2, 3)
COMMON = (4, 5)


def augmented_cell_allowed(pair, word):
    """Whether the normalized one-bad source can have this decorated cell.

    Residual q-cells have arbitrary colour pairs.  The direct P--S cell is
    only 00.  Endpoint stars have endpoint colour 1 or 2, never colour 0.
    """
    left, right = pair
    colours = (word[left], word[right])
    if pair == edge(P, S):
        return colours == (0, 0)
    if left in (P, S):
        return colours[0] in (1, 2)
    if right in (P, S):
        return colours[1] in (1, 2)
    return True


def monomial_structurally_allowed(matching, word):
    return all(augmented_cell_allowed(pair, word) for pair in matching)


def audit_literal_source_words_and_unary_zero():
    # Site order in every printed word is 0,1,2,3,4,5,P,S.  The actual
    # outside-active residual word rho is selected from a nonzero complete
    # coefficient.  The displayed rho=012012 is a literal representative;
    # the proof below uses only its endpoint labels and works for every rho.
    rho = (0, 1, 2, 0, 1, 2)
    words = (
        (2,) * 8,                  # selected diagonal target t^8
        rho + (1, 2),              # selected mixed outside word d
        rho + (2, 1),              # opposite crossed word e
        (0,) * 8,                  # unary/direct word 0^8
        (1,) * 8,                  # the other diagonal target
    )
    labels = tuple("".join(map(str, word)) for word in words)
    target = (Q(1), Q(0), Q(0), Q(1), Q(1))
    require(labels == (
        "22222222", "01201212", "01201221", "00000000", "11111111",
    ), "the five literal eight-site words changed")

    target_tails = tuple(perfect_matchings(OUTSIDE_HOLES + COMMON))
    outside_tails = tuple(perfect_matchings(TARGET_HOLES + COMMON))
    records = []
    for target_tail in target_tails:
        for outside_tail in outside_tails:
            first = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            second = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles = cycle_lengths(first, second)
            if cycles not in ((6,), (8,)):
                continue
            require(edge(P, S) not in first and edge(P, S) not in second,
                    "a response base unexpectedly acquired the direct edge")
            require(not monomial_structurally_allowed(first, words[3])
                    and not monomial_structurally_allowed(second, words[3]),
                    "a response base acquired a physical 0^8 monomial")
            # All three nonzero endpoint labels t,d,e are structurally
            # permitted.  Their actual coefficients may of course vanish.
            require(all(monomial_structurally_allowed(matching, word)
                        for matching in (first, second)
                        for word in words[:3]),
                    "a bright/mixed response monomial became structurally forbidden")
            records.append({
                "M": first,
                "N": second,
                "cycle": cycles[0],
                "mu_M_0^8": 0,
                "mu_N_0^8": 0,
            })
    require(len(records) == 7,
            "the single-C6/C8 physical record count changed")
    require(sorted(record["cycle"] for record in records)
            == [6, 8, 8, 8, 8, 8, 8],
            "the seven physical cycle types changed")

    # Columns (t^8,d,0^8).  Coloop means b_t=0, outside activity means
    # b_d!=0, and the direct unary target is one.  With a_0=b_0=0 the
    # determinant is exactly a_t*b_d, independently of a_d.
    a = (Q(2), Q(3), Q(0))
    b = (Q(0), Q(5), Q(0))
    h = (Q(1), Q(0), Q(1))
    determinant = det3(a, b, h, (0, 1, 2))
    require(determinant == a[0] * b[1] == 10,
            "the physical E3 minor stopped being the E2 minor")
    basis = tuple(tuple(Q(int(index == column)) for index in range(3))
                  for column in range(3))
    expansion_weights = tuple(det3(a, b, vector, (0, 1, 2))
                              for vector in basis)
    require(expansion_weights == (Q(0), Q(0), determinant),
            "the third-base E3 expansion stopped depending only on 0^8")

    # A perfect matching can evaluate nontrivially on 0^8 exactly when it
    # contains P--S:00: otherwise its P-edge asks for the absent p_0 cell.
    matchings = tuple(perfect_matchings(range(8)))
    direct = edge(P, S)
    require(all(monomial_structurally_allowed(matching, words[3])
                == (direct in matching) for matching in matchings),
            "0^8 evaluation stopped detecting the unary/direct base")

    return {
        "site_order": [0, 1, 2, 3, 4, 5, "P", "S"],
        "word_family": [
            "t^8 with t=2",
            "rho_0...rho_5,1,2 (the selected outside-active word d)",
            "rho_0...rho_5,2,1 (an opposite crossed word e)",
            "0^8",
            "1^8",
        ],
        "literal_representative_rho_012012": list(labels),
        "target_vector": [str(value) for value in target],
        "single_cycle_records": records,
        "mandatory_source_zeros": "mu_M(0^8)=mu_N(0^8)=0",
        "physical_minor_columns": ["t^8", "d", "0^8"],
        "physical_E3_factor": "a_t*b_d",
        "sample_factor_value": str(determinant),
        "third_base_expansion_weights_on_(t,d,0)": [
            str(value) for value in expansion_weights
        ],
        "third_base_consequence": (
            "some K has mu_K(0^8)!=0, hence K contains P--S:00"
        ),
    }


def cycle_lengths(first, second):
    common = set(first) & set(second)
    symmetric = (set(first) | set(second)) - common
    adjacency = {}
    for left, right in symmetric:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    lengths = []
    unseen = set(adjacency)
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        length = 0
        while True:
            following = next(site for site in adjacency[current]
                             if site != previous)
            length += 1
            previous, current = current, following
            unseen.discard(previous)
            if current == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths))


def audit_third_base_must_leave_cycle():
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, "the K8 matching count changed")
    representatives = {
        "C8": (
            ((0, 6), (1, 7), (2, 3), (4, 5)),
            ((0, 4), (1, 5), (2, 6), (3, 7)),
        ),
        "C6": (
            ((0, 6), (1, 7), (2, 3), (4, 5)),
            ((0, 1), (2, 6), (3, 7), (4, 5)),
        ),
    }
    audits = {}
    for name, (first, second) in representatives.items():
        first, second = tuple(sorted(first)), tuple(sorted(second))
        expected_cycles = (8,) if name == "C8" else (6,)
        require(cycle_lengths(first, second) == expected_cycles,
                f"the {name} representative changed")
        union = set(first) | set(second)
        contained = tuple(matching for matching in matchings
                          if set(matching) <= union)
        require(set(contained) == {first, second},
                f"a third perfect matching stayed inside the {name} union")
        outside_counts = [len(set(matching) - union)
                          for matching in matchings if matching not in contained]
        require(outside_counts and min(outside_counts) == 1,
                f"the first third-base escape changed on {name}")
        audits[name] = {
            "base_union_edges": len(union),
            "perfect_matchings_contained_in_union": len(contained),
            "third_bases_audited": len(outside_counts),
            "minimum_new_physical_edges": min(outside_counts),
            "consequence": (
                "every E3-selected third matching has an edge outside M union N"
            ),
        }
    return audits


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "unlabelled_five_vector_regression": audit_e3_rank_dichotomy(),
        "literal_physical_five_words": audit_literal_source_words_and_unary_zero(),
        "single_cycle_third_base": audit_third_base_must_leave_cycle(),
        "positive_routing": (
            "if some E3 determinant is nonzero, its perfect-matching "
            "expansion cancels M,N separately and selects a third literal "
            "base K.  On a single C6/C8, K has a physical edge outside "
            "M union N.  If that edge is outside the three selected target "
            "matchings it enters the nonanchor four-good route; otherwise "
            "its exact provenance is carried by the third selected anchor "
            "and enters the anchor-contained strict-Hall exchange web"
        ),
        "physical_closure": (
            "the apparent E3-flat plane is incompatible with the normalized "
            "one-bad source.  Both response bases vanish on 0^8, so the "
            "E3 minor on (t^8,d,0^8) equals the localized E2 minor a_t*b_d. "
            "It selects a third matching with nonzero unary evaluation, "
            "which necessarily contains the direct P--S:00 anchor"
        ),
        "scope": (
            "physical closure of the seven single-C6/C8 target-coloop "
            "records in the normalized augmented one-bad packet.  It selects "
            "a unary/direct third base; downstream routing of that base is "
            "separate.  The old rational flat packet remains only as an "
            "explicitly retracted unlabelled-vector regression guard"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"h3 even-cycle E3 boundary ledger changed: {digest}")
    print("h3 target-coloop single-cycle physical E3 closure: PASS")
    print("seven C6/C8 response-base pairs vanish on literal 0^8")
    print("E3(t^8,d,0^8)=a_t*b_d != 0")
    print("third base: unary/direct P--S:00")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
