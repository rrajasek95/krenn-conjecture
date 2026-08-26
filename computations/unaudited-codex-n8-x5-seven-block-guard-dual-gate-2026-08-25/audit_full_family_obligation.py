#!/usr/bin/env python3
"""Freeze the exact six-representative star/full-X5 counter-obligation."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SANDWICH_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-two-sandwich-reduction-2026-08-25/MANIFEST.sha256"
SANDWICH_RESULT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-two-sandwich-reduction-2026-08-25/results_two_sandwich_reduction.json"
MODULAR_RESULT = HERE / "results_guard_dual_p32003.json"
PINS = {
    SANDWICH_MANIFEST: "056d73cd56818a18e2976707815f902cc433839ce69b192a88b118b7a9a5d707",
    SANDWICH_RESULT: "1d94711066e002f9f827ce4ce392526d0cb46c5b5c0f5eaba584af571561d19c",
}

SITES = tuple(range(8))
COLORS = tuple(range(3))
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
REPS = (
    ((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7)),
    ((0, 6), (1, 3), (1, 7), (2, 5), (2, 6), (4, 6), (4, 7)),
    ((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)),
    ((0, 6), (1, 4), (1, 7), (2, 5), (2, 6), (3, 6), (3, 7)),
    ((0, 6), (1, 5), (1, 7), (2, 3), (2, 6), (4, 6), (4, 7)),
    ((0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 6), (3, 7)),
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def edge_text(edge):
    return "".join(map(str, edge))


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(matchings(SITES)))
assert len(PM8) == 105


def supported_terms(support, cap, center):
    p, q = cap
    residual = tuple(site for site in SITES if site not in cap)
    terms = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
        if pa in support and qb in support:
            terms.append((a, b, "direct", pa, qb))
        pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
        if pb in support and qa in support:
            terms.append((a, b, "switched", pb, qa))
    return tuple(terms)


def left_effective(edge, cap_site):
    # get(p,x,i,alpha) enters as M^T on the left of K.
    return f"A{edge_text(edge)}^T" if cap_site == edge[0] else f"A{edge_text(edge)}"


def right_effective(edge, cap_site):
    # get(q,x,j,beta) enters as M on the right of K.
    return f"A{edge_text(edge)}" if cap_site == edge[0] else f"A{edge_text(edge)}^T"


def all_two_sandwiches(support):
    records = []
    for cap in sorted(support):
        for center in SITES:
            if center in cap:
                continue
            terms = supported_terms(support, cap, center)
            if len(terms) != 2:
                continue
            # The two terms must occupy distinct response matrices, so their
            # row spaces add without coefficient cancellation.
            assert terms[0][:2] != terms[1][:2]
            for common_slot, side in ((3, "left"), (4, "right")):
                if terms[0][common_slot] != terms[1][common_slot]:
                    continue
                common = terms[0][common_slot]
                if side == "left":
                    partners = tuple(term[4] for term in terms)
                    U = left_effective(common, cap[0])
                    Bs = tuple(right_effective(edge, cap[1]) for edge in partners)
                    factorization = f"{U}*K*[{'|'.join(Bs)}]"
                    P = f"Row({U})"
                    Q = f"ColSpan({','.join(Bs)})"
                else:
                    partners = tuple(term[3] for term in terms)
                    Us = tuple(left_effective(edge, cap[0]) for edge in partners)
                    B = right_effective(common, cap[1])
                    factorization = f"[{'|'.join(Us)}]*K*{B}"
                    P = f"RowSpan({','.join(Us)})"
                    Q = f"Col({B})"
                records.append({
                    "cap": edge_text(cap),
                    "star_center": center,
                    "common_side": side,
                    "common_block": edge_text(common),
                    "partner_blocks": list(map(edge_text, partners)),
                    "factorization_up_to_output_permutation": factorization,
                    "P": P,
                    "Q": Q,
                    "response_row_space": "P tensor Q",
                    "inactivity_clause": [
                        "e0 in P and e0 in Q",
                        "e1 in P and e1 in Q",
                        "e2 in P and e2 in Q",
                        f"Col(A{edge_text(cap)}) subset P and Row(A{edge_text(cap)}) subset Q",
                    ],
                    "supported_forbidden_terms": [
                        {
                            "response_pair": f"{a}{b}",
                            "orientation": orientation,
                            "left_block": edge_text(left),
                            "right_block": edge_text(right),
                        }
                        for a, b, orientation, left, right in terms
                    ],
                })
    return records


def amplitude_terms(support, word):
    answer = []
    for matching in PM8:
        if not set(matching) <= support:
            continue
        factors = []
        for edge in matching:
            a, b = word[edge[0]], word[edge[1]]
            if edge in FIXED:
                if a != b:
                    break
            else:
                factors.append(f"A{edge_text(edge)}[{a}{b}]")
        else:
            answer.append({
                "matching": "|".join(map(edge_text, matching)),
                "monomial": "*".join(factors) or "1",
            })
    return answer


def full_ideal_digest(support):
    records = []
    term_census = Counter()
    for word in itertools.product(COLORS, repeat=8):
        terms = amplitude_terms(support, word)
        target = 1 if len(set(word)) == 1 else 0
        term_census[len(terms)] += 1
        records.append(("".join(map(str, word)), target, tuple(item["monomial"] for item in terms)))
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), dict(sorted(term_census.items()))


def guard_record(support):
    equations = []
    outside_site = None
    for a, b in itertools.combinations(range(6), 2):
        if {a, b} <= {0, 1, 2}:
            continue
        terms = []
        if tuple(sorted((a, 6))) in support and tuple(sorted((b, 7))) in support:
            terms.append(f"A{a}6*A{b}7^T")
        if tuple(sorted((a, 7))) in support and tuple(sorted((b, 6))) in support:
            terms.append(f"A{a}7*A{b}6^T")
        if terms:
            equations.append({"response": f"R{a}{b}", "equation": "+".join(terms) + "=0"})
            outside_site = b if b >= 3 else a
    assert len(equations) == 3 and outside_site in (3, 4, 5)
    r = outside_site
    expected = [
        {"response": f"R0{r}", "equation": f"A06*A{r}7^T=0"},
        {"response": f"R1{r}", "equation": f"A16*A{r}7^T+A17*A{r}6^T=0"},
        {"response": f"R2{r}", "equation": f"A26*A{r}7^T+A27*A{r}6^T=0"},
    ]
    assert equations == expected
    return {
        "outside_site": r,
        "exact_matrix_equations": equations,
        "fixed_identity_substitution": [
            f"A06*A{r}7^T=0",
            f"A{r}7^T+A17*A{r}6^T=0",
            f"A26*A{r}7^T+A{r}6^T=0",
        ],
        "derived": [
            f"A{r}6^T=-A26*A{r}7^T",
            f"(I-A17*A26)*A{r}7^T=0",
            f"A06*A{r}7^T=0",
        ],
        "cap67_response_map": [
            f"R0{r}(K)=A06*K*A{r}7^T",
            f"R1{r}(K)=K*A{r}7^T+A17*K^T*A{r}6^T",
            f"R2{r}(K)=A26*K*A{r}7^T+K^T*A{r}6^T",
        ],
        "cap67_pairing_failure_adjoint": (
            f"exists X,Y,Z: A67=A06^T*X*A{r}7+Y*A{r}7+"
            f"A{r}6^T*Y^T*A17+A26^T*Z*A{r}7+A{r}6^T*Z^T"
        ),
    }


def main():
    for path, digest in PINS.items():
        assert sha256(path) == digest
    parent = json.loads(SANDWICH_RESULT.read_text())
    assert parent["status"] == "PASS_ALL_64_REDUCE_TO_13_TWO_SANDWICH_STAR_PATTERNS"
    assert parent["census"]["unresolved_strata"] == 64
    modular = json.loads(MODULAR_RESULT.read_text())
    assert modular["status"] == "INCOMPLETE_WALL_GATE"
    assert modular["mathematical_coverage"] is False

    parent_full = {
        (tuple(record["added"]), tuple(record["nonzero_variable_blocks"]))
        for record in parent["reductions"] if len(record["nonzero_variable_blocks"]) == 4
    }
    representative_records = []
    candidate_count_census = Counter()
    all_candidate_labels = Counter()
    for rep_id, added in enumerate(REPS):
        support = FIXED | VARIABLE | set(added)
        key = (tuple(map(edge_text, added)), tuple(map(edge_text, sorted(VARIABLE))))
        assert key in parent_full
        candidates = all_two_sandwiches(support)
        assert len(candidates) in (8, 10)
        candidate_count_census[len(candidates)] += 1
        for item in candidates:
            all_candidate_labels[(item["cap"], item["star_center"], item["common_block"])] += 1
        supported_matchings = tuple(matching for matching in PM8 if set(matching) <= support)
        pure = {
            str(colour): amplitude_terms(support, (colour,) * 8)
            for colour in COLORS
        }
        residuals = []
        for a, b in itertools.permutations(COLORS, 2):
            word = (a, b, b, a, a, a, b, b)
            residuals.append({
                "word": "".join(map(str, word)),
                "target": 0,
                "terms": amplitude_terms(support, word),
            })
        digest, term_census = full_ideal_digest(support)
        representative_records.append({
            "representative_id": rep_id,
            "added": list(map(edge_text, added)),
            "supported_perfect_matchings": len(supported_matchings),
            "guard": guard_record(support),
            "two_sandwich_stars": candidates,
            "candidate_count": len(candidates),
            "pure_equations_target_one": pure,
            "six_distinguished_residual_equations_target_zero": residuals,
            "full_x5_6561_equation_sha256": digest,
            "full_x5_term_count_census": term_census,
        })

    assert candidate_count_census == {8: 2, 10: 4}

    canonical_support = FIXED | VARIABLE | set(REPS[0])
    canonical_three_terms = supported_terms(canonical_support, (4, 5), 2)
    assert canonical_three_terms == (
        (0, 3, "direct", (0, 4), (3, 5)),
        (0, 6, "direct", (0, 4), (5, 6)),
        (0, 7, "direct", (0, 4), (5, 7)),
    )
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_FULL_FAMILY_INCIDENCE_OBLIGATION_V1",
        "status": "PASS_EXACT_SIX_REPRESENTATIVE_REDUCTION_GENERAL_DICHOTOMY_OPEN",
        "dependencies": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "six_full_family_representatives": representative_records,
        "census": {
            "full_family_representatives": 6,
            "full_family_supports_with_guard_mates": 12,
            "two_sandwich_candidates_on_representatives": sum(
                item["candidate_count"] for item in representative_records
            ),
            "candidate_count_by_representative": dict(sorted(candidate_count_census.items())),
            "candidate_label_census": [
                {"cap": cap, "center": center, "common": common, "count": count}
                for (cap, center, common), count in sorted(all_candidate_labels.items())
            ],
        },
        "uniform_guard_rectangle_lemma": {
            "statement": (
                "For every full-family representative, one outside site r in {3,4,5} gives exactly "
                "R0r=A06*A_r7^T, R1r=A_r7^T+A17*A_r6^T, "
                "R2r=A26*A_r7^T+A_r6^T at K=I."
            ),
            "consequences": (
                "A_r6^T=-A26*A_r7^T, (I-A17*A26)*A_r7^T=0, A06*A_r7^T=0"
            ),
            "guard_mates": "the order-two guard symmetry supplies the other six supports",
        },
        "cap67_triangle_failure_lemma": {
            "I_in_kernel": True,
            "rank_at_most": 8,
            "all_diagonal_activities_live": True,
            "only_failure": "A67 belongs to Row(L67)",
            "exact_existential_certificate": (
                "the X,Y,Z adjoint identities stored per representative; pairing with I also forces trace(A67)=0"
            ),
        },
        "canonical_cap45_star2_lemma": {
            "exact_map": "K -> A04*K*[A35^T|A56|A57]",
            "forbidden_response_pairs": ["03", "06", "07"],
            "P": "Row(A04)",
            "Q_before_guard": "ColSpan(A35^T,A56,A57)",
            "guard_simplification": (
                "A56=-A57*A26^T, hence Q=ColSpan(A35^T,A57); "
                "A06*A57^T=0 with A06 nonzero also gives rank(A57)<=2"
            ),
            "response_row_space": "P tensor Q",
            "active_criterion_for_fixed_A45_I": (
                "P and Q are not both Q^3 and no coordinate e_i belongs to both P and Q"
            ),
            "negative_control_application": (
                "the sealed witness has P=<e0> while e0 is not in Q, so this star is active"
            ),
        },
        "two_sandwich_activity_lemma": parent["abstract_activity_lemma"],
        "remaining_exact_dichotomy": {
            "branches": [
                "A67 is outside Row(L67): cap67/triangle012 is active",
                "A67 is in Row(L67), but some listed two-sandwich star has all four activities live: active star",
                "A67 is in Row(L67), every listed star satisfies one stored inactivity incidence, and the full-X5 ideal must be shown inconsistent",
            ],
            "first_unproved_system": (
                "For each of six representatives, combine its three exact guard matrices, its cap67 adjoint "
                "identity, one inactivity clause for every listed star, and all 6,561 full-X5 equations."
            ),
            "why_finite": (
                "the guard symmetry reduces 12 supports to six representatives; each has only 8 or 10 "
                "two-sandwich candidates and four explicitly stated inactivity alternatives per candidate"
            ),
            "not_proved": True,
        },
        "bounded_groebner_diagnostic": {
            "scope": "canonical representative, full X5 + guard + cap67 pairing failure; star clauses omitted",
            "ring": "F_32003",
            "status": modular["status"],
            "wall_seconds": modular["wall_seconds"],
            "peak_rss_raw_darwin_bytes": modular["peak_rss_raw_darwin_bytes"],
            "mathematical_coverage": False,
            "rational_run_skipped": "the easier modular gate did not terminate inside 120 seconds",
        },
        "scope": {
            "all_64_inherited_from_two_sandwich": True,
            "six_full_family_representatives_expanded": True,
            "exact_source_labelled_polynomials": True,
            "broad_cegar": False,
            "D12_read": False,
            "full_seven_block_closure": False,
        },
    }
    output = HERE / "results_full_family_obligation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"],
        "representatives": 6,
        "candidate_counts": [item["candidate_count"] for item in representative_records],
        "groebner": modular["status"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
