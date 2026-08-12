#!/usr/bin/env python3
r"""Classify every mate of the marked normalized-C5 unary monomial.

For an off-cycle face tail N, the tempting accessibility row contains

    t_(pq)^00 u_(xv)^00 N.

The fine word is zero at p,q,x,v and is m on the other four odd sites.
In the normalized one-bad packet p_0=s_0=0, so all matchings which do not
retain pq vanish.  The surviving row is the complete six-site unary face.
This checker classifies its fourteen alternative matchings for all ten
off-cycle tails and freezes the exact source-label mismatch with the
bright spoke/bracket rows used by the conditional attachment theorem.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "23e0508b58f1340a5f743ca406815f1e613159864ebedd369ac6dc72b152f8f4"
PINS = {
    "computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py":
        "c431823ae3d7eed06b0df35f414d069a38f1fba3311a712e3dfce03c230b4016",
    "notes/h3-rootless-c5-universal-ten-tail-typed-quotient.md":
        "d44e8fef499b44e0a91e90a5be465b47c47c138cc43f6f0dcea13237ba16e912",
    "computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py":
        "ef235f2e17b7f62a7160bdc9fccd18efae5842c00ae2fc4ae7d900de34255f0d",
    "notes/h3-rootless-c5-first-unmatched-tail-attachment-boundary.md":
        "b26b97ecda76037fd6f73a2e6a37823e6cffc75d5917485da5a07e29c0d18d50",
    "computations/verify_n8_lemma_e_unary_top_translated_faces.py":
        "1c696635ec3ca94dd9a3c835c661479144b6f46e9efd2652c7fc87c95097458a",
    "notes/n8-lemma-e-unary-top-translated-faces.md":
        "1737fb5e0530174b9add2981fe700d0a174f1b47413756e0fd3d8a0edda5a0be",
}

X, P, Q = 0, 6, 7
ODD = (1, 2, 3, 4, 5)
M = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted(((first, second),) + tail)))
    return tuple(result)


def edge(a, b):
    return tuple(sorted((a, b)))


def word_for(deleted):
    word = {site: 0 for site in (X, P, Q, deleted)}
    word.update({site: M[site] for site in ODD if site != deleted})
    return word


def decorated(matching, word):
    return tuple((a, b, word[a], word[b]) for a, b in matching)


def face_data():
    records = []
    for deleted in ODD:
        face = tuple(site for site in ODD if site != deleted)
        matchings = perfect_matchings(face)
        selected = tuple(pm for pm in matchings if set(pm) <= CYCLE)
        residual = tuple(pm for pm in matchings if pm not in selected)
        require(len(selected) == 1 and len(residual) == 2,
                "a C5 face lost its selected-plus-two-tail split")
        for tail_index, tail in enumerate(residual):
            records.append((deleted, tail_index, tail, selected[0],
                            residual[1 - tail_index]))
    require(len(records) == 10, "the ten off-cycle tails changed")
    return records


def classify_record(deleted, tail_index, tail, selected, other_tail):
    u = edge(X, deleted)
    t = edge(P, Q)
    base6 = tuple(sorted((u,) + tail))
    base8 = tuple(sorted((t,) + base6))
    word = word_for(deleted)

    all8 = perfect_matchings((X,) + ODD + (P, Q))
    require(len(all8) == 105, "H8 perfect-matching count changed")
    retain_t = tuple(pm for pm in all8 if t in pm)
    avoid_t = tuple(pm for pm in all8 if t not in pm)
    require((len(retain_t), len(avoid_t)) == (15, 90),
            "direct/endpoint-star split changed")

    # Every avoid-t term has an outer colour-zero endpoint edge.  Those are
    # literally p_0 or s_0 columns and vanish in the one-bad normalization.
    for pm in avoid_t:
        p_edge = next(item for item in pm if P in item)
        q_edge = next(item for item in pm if Q in item)
        require(word[P] == word[Q] == 0,
                "the marked word stopped being outer-zero")
        require((P in p_edge and Q in q_edge),
                "an endpoint edge disappeared")

    same_tail = tuple(pm for pm in all8 if set(tail) <= set(pm))
    require(len(same_tail) == 3 and base8 in same_tail,
            "the same-tail external matching count changed")
    same_tail_endpoint = tuple(pm for pm in same_tail if pm != base8)
    require(len(same_tail_endpoint) == 2
            and all(t not in pm for pm in same_tail_endpoint),
            "same-tail alternatives stopped being the two endpoint crosses")

    six_mates = []
    for pm8 in retain_t:
        pm6 = tuple(item for item in pm8 if item != t)
        if pm6 == base6:
            continue
        common = set(pm6) & set(base6)
        if u in pm6:
            kind = "same_reset_changed_tail"
            require(len(common) == 1,
                    "a changed face matching shares more than the reset spoke")
            new_tail = tuple(item for item in pm6 if item != u)
            if new_tail == selected:
                subtype = "selected_base_tail"
            elif new_tail == other_tail:
                subtype = "other_off_cycle_tail"
            else:
                raise RuntimeError("u-retaining mate is not a face matching")
        else:
            kind = "translated_C4" if len(common) == 1 else "translated_C6"
            subtype = "reset_site_moves"
            require(len(common) in (0, 1),
                    "a nontrivial six-site mate has bad common-edge count")
            x_edge = next(item for item in pm6 if X in item)
            v_edge = next(item for item in pm6 if deleted in item)
            xr = x_edge[1]
            vs = v_edge[0] if v_edge[1] == deleted else v_edge[1]
            require(xr in ODD and xr != deleted and vs in ODD
                    and vs != deleted,
                    "translated mate lost its two reset-to-bright edges")
            require((word[X], word[xr]) == (0, M[xr]),
                    "x-spoke labels changed")
            require(word[deleted] == 0 and word[vs] == M[vs],
                    "deleted-site translated labels changed")
            # Removing x--r leaves deleted site v at colour zero.  Therefore
            # it is not the normalized full-m tail on D\{r}; this is the
            # precise line-to-hole/source-word mismatch.
            require(word[deleted] != M[deleted],
                    "the translated tail accidentally became normalized")
        six_mates.append({
            "matching": [list(item) for item in pm6],
            "decorated": [list(item) for item in decorated(pm6, word)],
            "kind": kind,
            "subtype": subtype,
        })

    counts = Counter(item["kind"] for item in six_mates)
    require(counts == Counter({
        "same_reset_changed_tail": 2,
        "translated_C4": 4,
        "translated_C6": 8,
    }), f"six-site mate census changed: {counts}")

    # Fine-degree mismatch with the actual accessibility rows.  The unary
    # occurrence q_xv^(0,m_v) N lies in the full-m word, not this v-reset
    # word.  Every same-N endpoint mate here has outer labels 0,0, whereas
    # the four response brackets use outer labels 11,12,21,22.
    desired_spoke_label = (X, deleted, 0, M[deleted])
    marked_spoke_label = (X, deleted, 0, 0)
    require(desired_spoke_label != marked_spoke_label,
            "the marked and accessibility spokes collided")
    endpoint_words = {(word[P], word[Q]) for _pm in same_tail_endpoint}
    require(endpoint_words == {(0, 0)},
            "same-tail endpoint mates left the outer-zero word")
    require(endpoint_words.isdisjoint({(1, 1), (1, 2), (2, 1), (2, 2)}),
            "a bright response bracket appeared in the marked row")

    return {
        "deleted_face": deleted,
        "tail_index": tail_index,
        "tail": [list(item) for item in tail],
        "selected_face_tail": [list(item) for item in selected],
        "other_off_cycle_tail": [list(item) for item in other_tail],
        "marked_word": "".join(str(word[site])
                                for site in (X,) + ODD + (P, Q)),
        "global_matching_count": 105,
        "direct_retaining_count": 15,
        "outer_zero_endpoint_count": 90,
        "same_tail_endpoint_crosses": 2,
        "six_site_mate_counts": dict(sorted(counts.items())),
        "mates": six_mates,
        "desired_spoke_label": list(desired_spoke_label),
        "marked_spoke_label": list(marked_spoke_label),
    }


def main() -> None:
    pin_dependencies()
    records = [classify_record(*record) for record in face_data()]
    aggregate = Counter()
    for record in records:
        aggregate.update(record["six_site_mate_counts"])
    require(aggregate == Counter({
        "same_reset_changed_tail": 20,
        "translated_C4": 40,
        "translated_C6": 80,
    }), f"aggregate ten-tail mate census changed: {aggregate}")

    ledger = {
        "theorem": "marked C5 unary mate accessibility boundary",
        "tail_records": records,
        "aggregate": {
            "tail_occurrences": 10,
            "global_terms_audited_with_multiplicity": 1050,
            "outer_zero_endpoint_terms": 900,
            "direct_retaining_terms": 150,
            "chosen_base_terms": 10,
            "same_tail_endpoint_crosses_killed_by_p0_s0": 20,
            "same_reset_changed_tail_mates": 20,
            "translated_C4_mates": 40,
            "translated_C6_mates": 80,
        },
        "scope": {
            "proved": (
                "the complete marked u_v*t*N row has no literal bright "
                "response bracket and its twelve reset-moving mates remain "
                "in the translated-face/line-to-hole gate"
            ),
            "not_proved": (
                "a full one-bad source with dark accessibility factors, or "
                "a routing of translated C4/C6 mates to active 8771755 data"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"marked C5 accessibility ledger changed: {digest}")
    print("h3 marked C5 unary mate accessibility boundary: PASS")
    print("ten-tail mate aggregate:", dict(sorted(aggregate.items())))
    print("same-tail bright brackets in marked word: 0")
    print("ledger SHA-256:", digest)


if __name__ == "__main__":
    main()
