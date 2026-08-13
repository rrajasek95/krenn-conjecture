#!/usr/bin/env python3
"""Classify the endpoint-direction face of the uniform response chart.

For X={0,1,P,S}, write

    A=01*PS, B=0P*1S, C=1P*0S,
    L_h=(2A-B-C)H_Y.

Differentiating one of the two X-edges gives six labelled direction faces.
For every tail occurrence their coefficient vector is

    kappa=(2,2,-1,-1,-1,-1)

in the order dD,dq01,dp0,ds1,dp1,ds0.  Hence the whole direction face is
the rank-one tensor kappa (x) H_Y: it is one endpoint-even Spencer packet,
not six independent families and not a new coefficient species at each h.

Its next Hasse faces have only the known lower topologies.  Differentiating
the complementary X-edge gives a complete hafnian/C4-family coefficient.
Differentiating a Y-edge gives, according to the first X-label, a C4,
C2+, or P2-family coefficient.  The fixed zero-cross chart contains only
1/(2h-3) of each latter complete coefficient (one of three terms at h=3);
the omitted cross-chart response occurrences are mandatory.  Thus the
known lower packet census classifies the *next* face, but does not itself
construct the first-PP Spencer boundary.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_response_h2_chart_scalar_recursive_factorization.py":
        "f36f06303c6e482f96d4831fed5f80e86a1d2f04539826d467c82d8308f4ba7b",
    "notes/uniform-response-h2-chart-scalar-recursive-factorization.md":
        "c3c2405ff076b229a9fb1684afc2af0d7c65e8b0aeacc141c3c94f824f56ee8a",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "notes/h3-h2-l01-three-cap-first-pp-curvature-gate.md":
        "d43b196a448045b9cf40a9537e5a30d9aad658a9c8636047052a023b45c4db7f",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
}
EXPECTED_LEDGER_SHA256 = (
    "b9811e3842bfeaf3e0760127a1e2f92565de01337cb6f6e673ccd83656143906"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def odd_double_factorial(value: int) -> int:
    require(value >= -1 and value % 2 == 1, value)
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def rank(rows: tuple[tuple[Q, ...], ...]) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    answer = 0
    width = len(work[0])
    require(all(len(row) == width for row in work), "rank width")
    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


DIRECTION_ORDER = ("dD", "dq01", "dp0", "ds1", "dp1", "ds0")
KAPPA = (Q(2), Q(2), Q(-1), Q(-1), Q(-1), Q(-1))
SURVIVOR_OPERATION = {
    "dD": "Q", "dq01": "D",
    "dp0": "S", "ds1": "P",
    "dp1": "S", "ds0": "P",
}
VARIED_OPERATION = {
    "dD": "D", "dq01": "Q",
    "dp0": "P", "ds1": "S",
    "dp1": "P", "ds0": "S",
}
MIXED_LOWER_TYPE = {
    "dD": "DQ -> pure-hafnian/C4 family",
    "dq01": "QQ -> complete-response/C2plus family",
    "dp0": "PQ -> one-endpoint/P2 family",
    "ds1": "SQ -> one-endpoint/P2 family",
    "dp1": "PQ -> one-endpoint/P2 family",
    "ds0": "SQ -> one-endpoint/P2 family",
}


def audit_pinned_results() -> dict[str, str]:
    recursive = load(
        "computations/verify_uniform_response_h2_chart_scalar_recursive_factorization.py",
        "uniform_chart_recursive_pin",
    )
    _recursive_ledger, recursive_digest = recursive.audit()
    require(recursive_digest == recursive.EXPECTED_LEDGER_SHA256,
            recursive_digest)

    first_pp = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "uniform_chart_first_pp_pin",
    )
    first_ledger, first_digest = first_pp.audit()
    require(first_digest == first_pp.EXPECTED_LEDGER_SHA256,
            first_digest)
    marginals = first_ledger["literal_three_cap_and_first_PP"]["labelled_marginals"]
    require(marginals["primitive_direction_profile"] == list(map(int, KAPPA)),
            marginals)

    lower = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "uniform_chart_lower_packet_pin",
    )
    lower_ledger, lower_digest = lower.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256,
            lower_digest)
    profiles = lower_ledger["exact_census"]["response_nonzero_pair_profiles"]
    require(set(profiles) == {
        "QQ_disjoint_pairs_with_three_term_C2plus_tail",
        "D_Q_pairs_with_three_matching_C4_tail",
        "P_S_distinct_pairs_with_three_matching_C4_tail",
        "P_Q_disjoint_pairs_with_three_term_P2_tail",
        "S_Q_disjoint_pairs_with_three_term_P2_tail",
    }, profiles)
    return {
        "recursive_factorization_ledger": recursive_digest,
        "h3_first_PP_ledger": first_digest,
        "h3_lower_packet_census_ledger": lower_digest,
    }


def permute_profile(permutation: dict[str, str], profile: tuple[Q, ...]):
    values = dict(zip(DIRECTION_ORDER, profile, strict=True))
    return tuple(values[permutation[label]] for label in DIRECTION_ORDER)


def audit_order(h: int) -> dict[str, object]:
    y = tuple(range(2, 2 * h))
    tails = tuple(perfect_matchings(y))
    m = odd_double_factorial(2 * h - 3)
    require(len(tails) == len(set(tails)) == m, (h, len(tails), m))

    # The six-by-m coefficient matrix is the outer product kappa*1_H.
    coefficient_matrix = tuple(tuple(value for _tail in tails)
                               for value in KAPPA)
    require(rank(coefficient_matrix) == 1
            and all(tuple(row) == (KAPPA[index],) * m
                    for index, row in enumerate(coefficient_matrix)),
            (h, coefficient_matrix[:2]))
    flattened = tuple(coefficient_matrix[direction][tail]
                      for tail in range(m)
                      for direction in range(6))
    require(len(flattened) == 6 * m
            and sum(flattened, Q(0)) == 0,
            (h, len(flattened), sum(flattened, Q(0))))

    # It is endpoint-even for the two generators swapping 0<->1 and P<->S.
    swap_01 = {
        "dD": "dD", "dq01": "dq01",
        "dp0": "dp1", "ds1": "ds0",
        "dp1": "dp0", "ds0": "ds1",
    }
    swap_ps = {
        "dD": "dD", "dq01": "dq01",
        "dp0": "ds0", "ds1": "dp1",
        "dp1": "ds1", "ds0": "dp0",
    }
    require(permute_profile(swap_01, KAPPA) == KAPPA
            and permute_profile(swap_ps, KAPPA) == KAPPA,
            "endpoint parity changed")

    constant = (Q(1),) * 6
    cap_a = (Q(1), Q(1), Q(0), Q(0), Q(0), Q(0))
    require(rank((constant, KAPPA)) == 2
            and KAPPA == tuple(Q(3) * cap_a[index] - constant[index]
                               for index in range(6)),
            "kappa=3*A-direction-complete changed")

    # Product-rule face counts.  Every Y-edge lies in (2h-5)!! tails.
    y_edges = tuple((left, right) for place, left in enumerate(y)
                    for right in y[place + 1:])
    through_edge = odd_double_factorial(2 * h - 5)
    for edge in y_edges:
        incidence = sum(edge in tail for tail in tails)
        require(incidence == through_edge, (h, edge, incidence, through_edge))

    mixed_by_first_label = {
        label: len(y_edges) * through_edge for label in DIRECTION_ORDER
    }
    require(set(mixed_by_first_label.values()) == {(h - 1) * m},
            (h, mixed_by_first_label, m))
    fixed_mixed = sum(mixed_by_first_label.values())

    # In the complete response coefficient, fixing the two varied disjoint
    # edges leaves 2h-2 vertices, hence m matchings.  The fixed chart forces
    # one selected complement edge and retains only through_edge of them.
    complete_per_varied_pair = m
    fixed_per_varied_pair = through_edge
    require(complete_per_varied_pair
            == (2 * h - 3) * fixed_per_varied_pair,
            (h, complete_per_varied_pair, fixed_per_varied_pair))
    complete_mixed = 6 * len(y_edges) * complete_per_varied_pair
    missing_mixed = complete_mixed - fixed_mixed
    require(missing_mixed == (2 * h - 4) * fixed_mixed,
            (h, fixed_mixed, complete_mixed, missing_mixed))

    named_fixed_counts = {
        "DQ_C4_family": mixed_by_first_label["dD"],
        "QQ_C2plus_family": mixed_by_first_label["dq01"],
        "PQ_P2_family": (mixed_by_first_label["dp0"]
                           + mixed_by_first_label["dp1"]),
        "SQ_P2_family": (mixed_by_first_label["ds1"]
                           + mixed_by_first_label["ds0"]),
    }
    require(sum(named_fixed_counts.values()) == fixed_mixed,
            named_fixed_counts)

    # Differentiating the complementary selected edge instead has no omitted
    # cross-chart term: the remaining vertices are exactly Y.
    internal_pair_packets = {
        "DQ_C4_family_weight_2": m,
        "PS_C4_family_weight_minus_1_first_orientation": m,
        "PS_C4_family_weight_minus_1_second_orientation": m,
    }
    require(sum(internal_pair_packets.values()) == 3 * m,
            internal_pair_packets)

    # Tail differentiation of the top has 3*m*(h-1) labelled terms.  For
    # each tail label the three cap weights cancel, while the six direction
    # labels do not.
    top_tail_faces = 3 * m * (h - 1)
    top_direction_faces = 6 * m
    return {
        "h": h,
        "tail_sites": len(y),
        "lower_hafnian_order": h - 1,
        "tail_occurrences": m,
        "top_first_PP": {
            "tail_face_support": top_tail_faces,
            "tail_label_marginal": 0,
            "direction_face_support": top_direction_faces,
            "direction_tensor_rank": rank(coefficient_matrix),
            "primitive_profile": [int(value) for value in KAPPA],
        },
        "next_internal_pair_faces": internal_pair_packets,
        "next_mixed_direction_tail_faces": {
            "fixed_chart_incidences": fixed_mixed,
            "fixed_counts_by_named_family": named_fixed_counts,
            "complete_packet_incidences": complete_mixed,
            "missing_cross_chart_incidences": missing_mixed,
            "fixed_terms_per_varied_pair": fixed_per_varied_pair,
            "complete_terms_per_varied_pair": complete_per_varied_pair,
            "fixed_fraction": f"1/{2 * h - 3}",
        },
    }


def h3_literal_completion_audit() -> dict[str, object]:
    """Check the 36+72 split directly inside the 105 K8 occurrences."""
    sites = tuple(range(8))
    y = (2, 3, 4, 5)
    p_site, s_site = 6, 7
    full = tuple(perfect_matchings(sites))
    tails = tuple(perfect_matchings(y))
    require(len(full) == 105 and len(tails) == 3, (len(full), len(tails)))
    direction_edges = {
        "dD": (p_site, s_site),
        "dq01": (0, 1),
        "dp0": (0, p_site),
        "ds1": (1, s_site),
        "dp1": (1, p_site),
        "ds0": (0, s_site),
    }
    internal_pairs = (
        ((p_site, s_site), (0, 1)),
        ((0, p_site), (1, s_site)),
        ((1, p_site), (0, s_site)),
    )
    fixed = tuple(tuple(sorted(pair + tail))
                  for pair in internal_pairs for tail in tails)
    require(len(fixed) == len(set(fixed)) == 9
            and set(fixed).issubset(full), "h3 fixed block changed")
    tail_edges = tuple((left, right) for place, left in enumerate(y)
                       for right in y[place + 1:])

    records = []
    for label in DIRECTION_ORDER:
        direction = direction_edges[label]
        for tail_edge in tail_edges:
            pair = {direction, tail_edge}
            fixed_count = sum(pair.issubset(matching) for matching in fixed)
            full_count = sum(pair.issubset(matching) for matching in full)
            require((fixed_count, full_count) == (1, 3),
                    (label, tail_edge, fixed_count, full_count))
            records.append((label, tail_edge, fixed_count, full_count))
    require(len(records) == 36
            and sum(record[2] for record in records) == 36
            and sum(record[3] - record[2] for record in records) == 72,
            records)

    internal_records = []
    for pair in internal_pairs:
        selected = set(pair)
        fixed_count = sum(selected.issubset(matching) for matching in fixed)
        full_count = sum(selected.issubset(matching) for matching in full)
        require((fixed_count, full_count) == (3, 3),
                (pair, fixed_count, full_count))
        internal_records.append((repr(pair), fixed_count, full_count))
    return {
        "complete_response_occurrences": len(full),
        "fixed_zero_cross_occurrences": len(fixed),
        "mixed_varied_pairs": len(records),
        "fixed_mixed_pair_incidences": sum(record[2] for record in records),
        "cross_chart_companion_incidences": sum(
            record[3] - record[2] for record in records
        ),
        "complete_mixed_pair_incidences": sum(record[3] for record in records),
        "each_mixed_pair": "1 fixed occurrence + 2 cross-chart companions",
        "complementary_selected_pairs": internal_records,
        "each_complementary_pair": "3 fixed occurrences = complete C4 packet",
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    pinned = audit_pinned_results()
    orders = tuple(audit_order(h) for h in range(2, 7))
    h3 = orders[1]
    require(h3["top_first_PP"] == {
        "tail_face_support": 18,
        "tail_label_marginal": 0,
        "direction_face_support": 18,
        "direction_tensor_rank": 1,
        "primitive_profile": [2, 2, -1, -1, -1, -1],
    }, h3)
    require(h3["next_mixed_direction_tail_faces"] == {
        "fixed_chart_incidences": 36,
        "fixed_counts_by_named_family": {
            "DQ_C4_family": 6,
            "QQ_C2plus_family": 6,
            "PQ_P2_family": 12,
            "SQ_P2_family": 12,
        },
        "complete_packet_incidences": 108,
        "missing_cross_chart_incidences": 72,
        "fixed_terms_per_varied_pair": 1,
        "complete_terms_per_varied_pair": 3,
        "fixed_fraction": "1/3",
    }, h3)

    ledger = {
        "theorem": "uniform endpoint-even direction Spencer packet gate",
        "pins": PINS,
        "pinned_ledgers": pinned,
        "direction_packet": {
            "formula": "S_h=kappa tensor H_Y",
            "direction_order": list(DIRECTION_ORDER),
            "kappa": [int(value) for value in KAPPA],
            "tail": "complete lower hafnian H_Y of order h-1",
            "endpoint_parity": "fixed by 0<->1 and P<->S",
            "tail_matrix_rank": 1,
            "complete_direction_row_independent": True,
            "coefficient_identity": "kappa=3*(1,1,0,0,0,0)-(1,1,1,1,1,1)",
        },
        "orders_exhaustively_audited": orders,
        "h3_literal_K8_completion": h3_literal_completion_audit(),
        "next_face_classification": {
            "complementary_selected_edge": (
                "DQ or PS varied pair; complete pure-hafnian/C4-family coefficient"
            ),
            "direction_plus_tail_edge": MIXED_LOWER_TYPE,
            "no_fourth_pair_topology": True,
            "h3_fixed_chart_warning": (
                "each of the 36 mixed faces is one term of a three-term lower "
                "packet; the 72 companion terms lie in cross-chart response sectors"
            ),
            "uniform_warning": (
                "the fixed chart contains 1/(2h-3) of every complete mixed "
                "coefficient, so lower packet theorems apply only after a "
                "source-valid cross-chart completion"
            ),
        },
        "verdict": (
            "The 18 h=3 direction faces are three copies of one primitive "
            "six-label endpoint-even vector.  Uniformly they form the single "
            "rank-one packet kappa tensor H_(h-1), so there is no proliferation "
            "of higher-order coefficient invariants.  Its next Hasse faces have "
            "exactly C2plus/C4/P2 topology.  However the fixed chart gives only "
            "one third of each h=3 mixed packet (uniformly 1/(2h-3)); the named "
            "lower packets therefore classify but do not fill the first-PP "
            "direction curvature."
        ),
        "shortest_remaining_theorem": (
            "construct one endpoint-even, chart-complete Spencer/cobar family "
            "with boundary S_h, whose cross-chart product-rule companions "
            "complete the C2plus/C4/P2 coefficients and retain word/fine/"
            "repeated, q, anchor, W and ridge readouts; a separate cell for "
            "each of the 6*(2h-3)!! direction occurrences is unnecessary"
        ),
        "scope": (
            "exact complete-matching coefficient and first/second PP modules; "
            "no source-valid endpoint Spencer family or augmented terminal is constructed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("direction packet: kappa tensor H_(h-1), rank ONE")
    print("h3 first PP: 18 tail + 18 direction")
    print("h3 next mixed faces: 36 fixed + 72 cross-chart companions")
    print("next topology: C2plus / C4 / P2 only")
    print("physical chart-complete Spencer family: STILL REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
