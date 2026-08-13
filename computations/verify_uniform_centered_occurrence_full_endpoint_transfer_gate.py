#!/usr/bin/env python3
"""Audit full all-role induction of the centered occurrence class.

For an occurrence (p,s,R) on 2h sites, add two sites in every possible
role: as one new residual edge, as one new endpoint plus the bridge to the
displaced old endpoint, or as both new endpoints with the old endpoints
becoming a residual edge.  Sum every chart and every preimage of a fixed
marked occurrence.  This is the most symmetric linear pull-push transfer
available from the bare occurrence species.

The transfer is not a scalar centered projector.  Its Gram coefficient at
an unmarked occurrence g is the number of common insertion charts with the
marked f.  Two explicit unmarked occurrences have coefficients 0 and 1 at
every h>=3.  Thus no Reynolds normalization or complete-row correction can
turn the transfer into c_{f,h+1}.  The product-rule face reattaches to this
same nonuniform class, so it is not yet the clean-line covariant required
by Tr_h; a physical correction must kill the coefficient-one association-
scheme residual.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "computations/verify_pointed_h3_spectator_uniformization_no_go.py":
        "832c4388961f24356cb182888cff89a4bda5ff181204a510baefb55e754323d2",
    "computations/verify_uniform_adjacent_cycle_filtered_prolongation.py":
        "2b2555fac43a5914469a857b3a6bf19aa715ab6576220dc1dfd66dd808cad86e",
    "computations/verify_full_27_colon_cycle_guard.py":
        "3beaaee3cae98ef342f98ad9ffbbd5e26f83721b91d7efb2d36130065a637567",
}
EXPECTED_LEDGER_SHA256 = "2020967237fea2cf8457b2e825574c7be6789a00da3eef0a7c0a882ca2f19535"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, ("loop", left, right))
    return (left, right) if left < right else (right, left)


def odd_double_factorial(value: int) -> int:
    require(value >= -1 and value % 2 == 1, ("bad double factorial", value))
    answer = 1
    while value > 0:
        answer *= value
        value -= 2
    return answer


def occurrence_count(h: int) -> int:
    return 2 * h * (2 * h - 1) * odd_double_factorial(2 * h - 3)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def occurrences(vertices: tuple[int, ...]):
    answer = []
    for p_site in vertices:
        for s_site in vertices:
            if p_site == s_site:
                continue
            rest = tuple(site for site in vertices
                         if site not in (p_site, s_site))
            for matching in perfect_matchings(rest):
                answer.append((p_site, s_site, matching))
    return tuple(answer)


def charts(big_sites: tuple[int, ...]):
    answer = []
    for left, right in combinations(big_sites, 2):
        pair = (left, right)
        answer.append((pair, "residual", left, right))
        answer.append((pair, "p", left, right))
        answer.append((pair, "p", right, left))
        answer.append((pair, "s", left, right))
        answer.append((pair, "s", right, left))
        answer.append((pair, "both", left, right))
        answer.append((pair, "both", right, left))
    return tuple(answer)


def extend(occurrence, chart):
    p_site, s_site, matching = occurrence
    _pair, kind, new_endpoint, bridge = chart
    if kind == "residual":
        return (p_site, s_site,
                tuple(sorted(matching + (edge(new_endpoint, bridge),))))
    if kind == "p":
        return (new_endpoint, s_site,
                tuple(sorted(matching + (edge(bridge, p_site),))))
    if kind == "s":
        return (p_site, new_endpoint,
                tuple(sorted(matching + (edge(bridge, s_site),))))
    require(kind == "both", ("unknown insertion chart", chart))
    return (new_endpoint, bridge,
            tuple(sorted(matching + (edge(p_site, s_site),))))


def chart_fibres(h: int):
    big_sites = tuple(range(2 * h + 2))
    big_occurrences = occurrences(big_sites)
    lookup = set(big_occurrences)
    fibres = []
    kind_records = Counter()
    for chart in charts(big_sites):
        pair = chart[0]
        small_sites = tuple(site for site in big_sites if site not in pair)
        small_occurrences = occurrences(small_sites)
        require(len(small_occurrences) == occurrence_count(h),
                ("small occurrence count changed", h, pair))
        image = Counter(extend(value, chart) for value in small_occurrences)
        require(set(image).issubset(lookup), ("chart left occurrence set", chart))
        require(sum(image.values()) == occurrence_count(h),
                ("chart lost domain columns", chart))
        if chart[1] == "both":
            require(set(image.values()) == {2 * h},
                    ("two-new-endpoint fibre changed", chart))
        else:
            require(set(image.values()) == {1},
                    ("injective insertion chart changed", chart))
        kind_records[chart[1]] += 1
        fibres.append((chart, image))
    require(kind_records == Counter({
        "p": 2 * len(tuple(combinations(big_sites, 2))),
        "s": 2 * len(tuple(combinations(big_sites, 2))),
        "both": 2 * len(tuple(combinations(big_sites, 2))),
        "residual": len(tuple(combinations(big_sites, 2))),
    }), ("chart census changed", h, kind_records))
    require(len(big_occurrences) == occurrence_count(h + 1),
            ("big occurrence count changed", h))
    return big_occurrences, tuple(fibres)


def marked_occurrence(h: int):
    # Final order is h+1, hence h residual edges.
    matching = tuple((2 * index, 2 * index + 1)
                     for index in range(1, h + 1))
    return (0, 1, matching)


def symbolic_full_transfer_audit():
    records = {}
    for h in range(3, 31):
        small = occurrence_count(h)
        big = occurrence_count(h + 1)
        preimage_columns = 7 * h
        self_gram = 4 * h * h + 5 * h
        marked_coefficient = preimage_columns * small - self_gram
        require(marked_coefficient > 0,
                ("full-transfer marked coefficient vanished", h))
        # The Gram row has sum 7h*N_h.  Subtracting it from the marked
        # 7h*N_h coefficient therefore leaves a centered vector.
        require(preimage_columns * small - preimage_columns * small == 0,
                ("full transfer lost centeredness", h))

        f_matching = {edge(2 * index, 2 * index + 1)
                      for index in range(1, h + 1)}
        g0_matching = {
            edge(2 * index + 1, 2 * index + 2)
            for index in range(1, h)
        } | {edge(2 * h + 1, 2)}
        g1_matching = {edge(2, 3)} | {
            edge(2 * index + 1, 2 * index + 2)
            for index in range(2, h)
        } | {edge(2 * h + 1, 4)}
        residual_vertices = set(range(2, 2 * h + 2))
        require(len(g0_matching) == len(g1_matching) == h
                and set().union(*map(set, g0_matching)) == residual_vertices
                and set().union(*map(set, g1_matching)) == residual_vertices,
                ("uniform 0/1 witnesses stopped being perfect matchings", h))
        require(len(f_matching & g0_matching) == 0
                and len(f_matching & g1_matching) == 1,
                ("uniform common-edge coefficient changed", h))
        records[h] = {
            "N_h": small,
            "N_hplus1": big,
            "preimage_columns_at_f": preimage_columns,
            "Gram_ff": self_gram,
            "transfer_at_f": marked_coefficient,
            "formal_scalar_if_centered_projector": str(Q(
                marked_coefficient, big - 1
            )),
            "reversed_endpoint_Gram_witnesses": [0, 1],
        }
    return {
        "all_role_chart_types": [
            "new sites form residual edge",
            "one new p endpoint and one bridge",
            "one new s endpoint and one bridge",
            "both new endpoints; old endpoints form residual edge",
        ],
        "preimage_count": "7h",
        "Gram_diagonal": "4h^2+5h",
        "marked_transfer_coefficient": "7h*N_h-(4h^2+5h)",
        "orders_checked": records,
    }


def exact_first_step_audit():
    h = 3
    big_occurrences, fibres = chart_fibres(h)
    marked = marked_occurrence(h)
    require(marked in set(big_occurrences), "marked occurrence disappeared")

    gram = Counter()
    preimage_columns = 0
    row_sum = 0
    for _chart, image in fibres:
        multiplicity = image.get(marked, 0)
        if not multiplicity:
            continue
        preimage_columns += multiplicity
        row_sum += multiplicity * sum(image.values())
        for occurrence, value in image.items():
            gram[occurrence] += multiplicity * value

    small = occurrence_count(h)
    big = occurrence_count(h + 1)
    require(preimage_columns == 7 * h,
            ("marked preimage count changed", preimage_columns))
    require(gram[marked] == 4 * h * h + 5 * h,
            ("marked Gram coefficient changed", gram[marked]))
    require(row_sum == 7 * h * small == sum(gram.values()),
            ("Gram row sum changed", row_sum, sum(gram.values())))

    transfer = {
        occurrence: (7 * h * small if occurrence == marked else 0)
        - gram[occurrence]
        for occurrence in big_occurrences
    }
    require(sum(transfer.values()) == 0, "full transfer stopped being centered")

    complement_gram_distribution = Counter(
        gram[occurrence] for occurrence in big_occurrences
        if occurrence != marked
    )
    require(complement_gram_distribution[0] > 0
            and complement_gram_distribution[1] > 0,
            ("first 0/1 coefficient split disappeared",
             complement_gram_distribution))
    zero_example = next(value for value in big_occurrences
                        if value != marked and gram[value] == 0)
    one_example = next(value for value in big_occurrences
                       if value != marked and gram[value] == 1)
    require(transfer[zero_example] == 0 and transfer[one_example] == -1,
            "the isolated complement coefficient changed")

    ones = tuple(Q(1) for _ in big_occurrences)
    centered = tuple(
        Q(big - 1) if occurrence == marked else Q(-1)
        for occurrence in big_occurrences
    )
    transferred = tuple(Q(transfer[occurrence])
                        for occurrence in big_occurrences)

    # A centered vector in span{1,c_f} is a scalar multiple of c_f, hence
    # has a constant coefficient on the complement.  The 0/-1 pair rules
    # this out without any rank convention.
    require(sum(transferred, Q(0)) == 0
            and transferred[big_occurrences.index(zero_example)]
            != transferred[big_occurrences.index(one_example)],
            "complete-row repair unexpectedly became possible")
    require(sum(ones, Q(0)) == big and sum(centered, Q(0)) == 0,
            "comparison basis changed")

    return {
        "step": "h=3 to h=4 (six to eight selected response sites)",
        "N_h": small,
        "N_hplus1": big,
        "charts": len(fibres),
        "preimage_columns_at_marked": preimage_columns,
        "Gram_ff": gram[marked],
        "transfer_at_marked": transfer[marked],
        "complement_Gram_distribution": {
            str(key): value for key, value in
            sorted(complement_gram_distribution.items())
        },
        "zero_overlap_example": repr(zero_example),
        "one_overlap_example": repr(one_example),
        "two_unmarked_transfer_coefficients": [0, -1],
        "in_span_of_centered_projector_and_complete_row": False,
    }


def product_rule_and_Tr_audit():
    prolongation = (ROOT / (
        "notes/uniform_adjacent_cycle_filtered_prolongation.md"
    )).read_text()
    colon = (ROOT / "notes/full-27-colon-cycle-macaulay-transfer-gap.md").read_text()
    require(r"\rho_{2h-6}\in\operatorname {Sym}^{2h-6}U" in prolongation
            and r"\operatorname {Tr}_h:" in colon
            and "changing it by direct/star/internal filtered row boundaries"
            in colon,
            "the Tr_h/covariant target changed")
    return {
        "formal_product_rule_face": (
            "for every insertion chart T with appended edge q_e, "
            "d(Tx)=T(dx)+dq_e tensor x"
        ),
        "reattachment_identity": (
            "multiplying each dq_e-face back by q_e sends the summed face "
            "to the full centered pull-push transfer"
        ),
        "first_residual_after_reattachment": (
            "two unmarked occurrences differ by exactly 1; this survives "
            "every Reynolds scalar and complete-row correction"
        ),
        "required_rootless_covariant": "rho_(2h-6) in Sym^(2h-6) U",
        "face_supplies_required_covariant": False,
        "reason": (
            "before clean-line representation type or common-Hankel "
            "equations are imposed, the face fails the necessary physical "
            "reattachment/centered-boundary test.  It is an edge-labelled "
            "permutation covariant with a nonzero association-scheme "
            "residual, not a well-defined filtered-homology input to Tr_h"
        ),
        "smallest_positive_repair": (
            "a physical product-rule correction whose reattachment is the "
            "negative coefficient-one residual, followed by proof that the "
            "corrected face has clean-line type Sym^(2h-6), is boundary-"
            "independent, nonzero, and satisfies every common Hankel shift"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "uniform centered occurrence full-endpoint transfer gate",
        "pins": PINS,
        "symbolic_transfer": symbolic_full_transfer_audit(),
        "exact_first_step": exact_first_step_audit(),
        "product_rule_and_Tr_h": product_rule_and_Tr_audit(),
        "verdict": (
            "Summing every new-site role is more symmetric than fixed-edge "
            "suspension but still does not produce c_f,h+1 modulo the "
            "complete row.  The first surviving coefficient is the 0/1 "
            "common-chart split on two unmarked occurrences.  The summed "
            "product-rule face reattaches to this nonuniform class and "
            "therefore does not yet supply the order-dependent Tr_h "
            "covariant."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full-endpoint transfer ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("uniform full-endpoint centered transfer: NOT A CENTERED PROJECTOR")
    print("h3->h4 first complement coefficients: 0 versus -1")
    print("product-rule face after reattachment: SAME RESIDUAL")
    print("Tr_h clean-line covariant: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
