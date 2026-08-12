#!/usr/bin/env python3
r"""Augmented-Jacobian visibility of every normalized-C5 residual tail.

For the six-site one-bad packet, each nonzero monomial in R_v-R_w contains
an off-cycle q-cell e.  Hafnian matching polynomials are affine in one
physical q-cell.  Hence setting e to zero changes the unary top and all four
binary responses by exactly the complete augmented column

    C_e=(D_e q^[3], D_e(p_i s_j q^[2])_(i,j=1,2)).

If C_e=0, the cell is deleted exactly.  The deletion is mutual-anchor safe
on the normalized C5 because both endpoint coordinate axes retain their two
selected cycle incidences.  At a minimum-support representative C_e is
therefore nonzero.  A nonzero top component contains an external x-spoke;
a nonzero response component contains a literal oriented endpoint product.
Thus a bare response-dark residual tail must export an active top/response
carrier unless it is deletable.

The theorem routes to the existing attachment/affine/Hall interface.  It
does not prove the downstream Fitting carrier has four-good rank.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "85d75d8d4473ac94433228d17c8304ab3f18ad913561ade12beb025d84edea71"
PINS = {
    "computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py":
        "ef235f2e17b7f62a7160bdc9fccd18efae5842c00ae2fc4ae7d900de34255f0d",
    "computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py":
        "c431823ae3d7eed06b0df35f414d069a38f1fba3311a712e3dfce03c230b4016",
    "computations/verify_h3_c5_marked_unary_mate_accessibility_boundary.py":
        "8d46d410334fd197ddf96c18a7be32f9109f23b33112b1a773cff5ca1ec99c53",
    "computations/verify_h3_c5_marked_unary_transition_scc_guard.py":
        "0950308ee449fabb0090d4cc81b968eeb1b771effa776b42197057079a225a73",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
}

X = 0
ODD = (1, 2, 3, 4, 5)
SITES = (X,) + ODD
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot load dependency", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        remainder = tuple(site for site in vertices
                          if site not in (first, second))
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def tail_occurrences():
    records = []
    for deleted in ODD:
        face = tuple(site for site in ODD if site != deleted)
        matchings = perfect_matchings(face)
        selected = tuple(matching for matching in matchings
                         if set(matching) <= CYCLE)
        residual = tuple(matching for matching in matchings
                         if matching not in selected)
        require(len(selected) == 1 and len(residual) == 2,
                "a normalized C5 face lost its 1+2 split")
        for local_index, matching in enumerate(residual):
            chords = tuple(item for item in matching if item not in CYCLE)
            require(chords, "a residual matching contains no off-cycle cell")
            records.append({
                "deleted": deleted,
                "local_index": local_index,
                "matching": matching,
                "chords": chords,
            })
    require(len(records) == 10, "the ten residual occurrences changed")
    histogram = Counter(len(record["chords"]) for record in records)
    require(histogram == Counter({1: 5, 2: 5}),
            ("linear/quadratic chord split changed", histogram))
    return records, histogram


def anchor_safe_chord_deletion(chord):
    # Every odd selected-colour axis has the two incident nonzero C5 edges.
    # An off-cycle chord uses those same m-labelled axes.  Removing it leaves
    # selected degree two at each endpoint, so no degree-one mutual anchor is
    # destroyed.
    endpoint_degrees = {}
    for endpoint in chord:
        selected_incident = tuple(item for item in CYCLE if endpoint in item)
        require(len(selected_incident) == 2,
                "a C5 vertex stopped having two selected incidences")
        endpoint_degrees[endpoint] = {
            "coordinate_colour": MIDDLE[endpoint],
            "selected_degree_before_and_after_deletion": 2,
            "selected_edges": selected_incident,
        }
    return endpoint_degrees


def visibility_records(records):
    answer = []
    counts = Counter()
    for record in records:
        deleted = record["deleted"]
        matching = record["matching"]
        for chord in record["chords"]:
            complement = tuple(site for site in SITES if site not in chord)

            # D_e(q^[3]) is the complete two-edge hafnian on the four-site
            # complement.  Each matching necessarily has an x-spoke because
            # the complement consists of x and three odd sites.
            top_completions = perfect_matchings(complement)
            require(len(top_completions) == 3,
                    "a chord derivative lost its three top completions")
            top_spokes = []
            for completion in top_completions:
                x_spoke = next(item for item in completion if X in item)
                require(x_spoke[0] == X and x_spoke[1] in ODD,
                        "a top carrier lost its external spoke")
                top_spokes.append(x_spoke)

            # D_e(p_i s_j q^[2]) chooses one q edge f on the complement and
            # leaves its other two sites as the ordered endpoint holes.
            response_completions = []
            for q_edge in (edge(left, right)
                           for position, left in enumerate(complement)
                           for right in complement[position + 1:]):
                holes = tuple(site for site in complement
                              if site not in q_edge)
                require(len(holes) == 2,
                        "a response derivative stopped leaving two holes")
                response_completions.append((q_edge, holes))
            require(len(response_completions) == 6,
                    "a chord derivative lost its six response completions")

            other_edge = next(item for item in matching if item != chord)
            desired = tuple(item for item in response_completions
                            if item[0] == other_edge)
            require(desired == ((other_edge, (X, deleted)),),
                    ("the original residual tail lost its forced hole",
                     record, chord, desired))

            safety = anchor_safe_chord_deletion(chord)
            answer.append({
                "deleted_face": deleted,
                "tail_index": record["local_index"],
                "tail_matching": [list(item) for item in matching],
                "chosen_off_cycle_cell": list(chord),
                "cell_decoration": [MIDDLE[chord[0]], MIDDLE[chord[1]]],
                "top_derivative_completions": [
                    [list(item) for item in completion]
                    for completion in top_completions
                ],
                "top_external_spokes": [list(item) for item in top_spokes],
                "response_derivative_completions": [
                    {"q_edge": list(q_edge), "endpoint_holes": list(holes)}
                    for q_edge, holes in response_completions
                ],
                "original_tail_forced_hole": [X, deleted],
                "anchor_safe_deletion": {
                    str(site): {
                        "coordinate_colour": data["coordinate_colour"],
                        "selected_degree_before_and_after_deletion": 2,
                        "selected_edges": [list(item)
                                           for item in data["selected_edges"]],
                    }
                    for site, data in safety.items()
                },
            })
            counts.update({
                "off_cycle_cell_occurrences": 1,
                "top_matching_completions": len(top_completions),
                "response_q_edge_completions": len(response_completions),
                "original_forced_hole_completions": len(desired),
            })
    require(counts == Counter({
        "off_cycle_cell_occurrences": 15,
        "top_matching_completions": 45,
        "response_q_edge_completions": 90,
        "original_forced_hole_completions": 15,
    }), ("augmented visibility counts changed", counts))
    return answer, counts


def exact_multiaffine_and_affine_interface():
    # A perfect matching never repeats one physical edge.  Therefore every
    # top/response monomial has exponent zero or one in a chosen q cell.
    top = perfect_matchings(SITES)
    require(len(top) == 15 and all(len(set(matching)) == len(matching)
                                   for matching in top),
            "six-site top stopped being square-free in physical edges")

    # Endpoint insertions are linear in each one-star row.  A change in the
    # joint kernel against both opposite rows is therefore a finite exact
    # modification; there is no second-order same-star term.
    return {
        "augmented_column": (
            "C_e=(D_e q^[3], D_e(p_1s_1q^[2]), "
            "D_e(p_1s_2q^[2]), D_e(p_2s_1q^[2]), "
            "D_e(p_2s_2q^[2]))"
        ),
        "exact_q_deletion_identity":
            "F(q-q_e*e,p,s)=F(q,p,s)-q_e*C_e",
        "higher_q_e_terms": 0,
        "one_star_exact_move": (
            "p_i->p_i+k is exact iff k*s_1*q^[2]=k*s_2*q^[2]=0; "
            "symmetrically after recomputing the opposite affine fibres"
        ),
        "affine_failure_normal_form": (
            "at minimum support, no target-line point leaves a unique "
            "full-support quotient circuit; a free nonzero circuit minor "
            "is the Fitting/active carrier, while an anchor-contained one "
            "is the existing star/triangle/K2,2 Hall gate"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    # Replay the pinned ten-tail and transition inventories before composing
    # them with the new cellwise augmented-column argument.
    tails = load(
        "computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py",
        "residual_visibility_tails",
    )
    tail_ledger, tail_digest = tails.audit()
    require(tail_ledger["Q_tail_rank_over_Q"] == 4,
            "the bare residual-tail quotient changed")
    require(tail_digest == tails.EXPECTED_LEDGER_SHA256,
            "the pinned ten-tail replay changed digest")

    records, histogram = tail_occurrences()
    visibility, counts = visibility_records(records)
    ledger = {
        "theorem": "normalized C5 residual-tail augmented visibility",
        "pins": PINS,
        "tail_degree_histogram": dict(sorted(histogram.items())),
        "visibility_records": visibility,
        "counts": dict(sorted(counts.items())),
        "exact_source_linearity": exact_multiaffine_and_affine_interface(),
        "minimum_support_dichotomy": {
            "zero_augmented_q_column": (
                "delete the off-cycle cell exactly; selected C5 and mutual "
                "anchors are unchanged, contradicting support minimality"
            ),
            "nonzero_top_component": (
                "one literal matching contains the chord and an external "
                "x-spoke; this is a source-active unary carrier.  The full-m "
                "label is direct accessibility, any other label is the "
                "translated/off-axis active branch"
            ),
            "nonzero_response_component": (
                "one literal oriented endpoint product and q-edge are "
                "nonzero.  At the original complement this is the forced "
                "hole used by 8771755; otherwise it is an alternate active "
                "hole/tail.  A mixed output has a source-forced mate and "
                "enters the complete-row C4/Fitting/Hall gate, while a pure "
                "diagonal output is already a bright response carrier"
            ),
        },
        "interaction_with_unary_SCC_guard": (
            "the f3e4b01 cyclotomic reset-word packet is not a counterexample: "
            "its nonzero marked q_xv^00 spokes are precisely top-carrier "
            "outputs of this dichotomy.  The SCC theorem only says those "
            "carriers do not restore the desired full-m word by unary "
            "re-pivoting alone"
        ),
        "verdict": (
            "at a minimum-support normalized-C5 one-bad source, a nonzero "
            "R_v-R_w cannot remain a bare response-dark tail: some chord is "
            "exactly deletable or exports a literal active unary/response "
            "carrier.  Direct target-line concentration and four-good rank "
            "landing remain the downstream affine/Fitting/Hall interface"
        ),
        "scope": (
            "exact for the unary top plus four binary responses on the "
            "six-site h=3 normalized C5 chart.  It routes rather than closes "
            "the active carrier, and assumes support minimality in the full "
            "five-tensor packet"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 rootless C5 residual-tail visibility: ROUTED")
    print("tail chord occurrences=15 top completions=45 response completions=90")
    print("zero augmented q column -> exact anchor-safe deletion")
    print("nonzero column -> literal unary/response active carrier")
    print("direct affine line hit / four-good landing: DOWNSTREAM")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
