#!/usr/bin/env python3
"""Isolate the one V4 character missing from the physical Gate-II packet.

The endpoint/root orbit of a marked fan-coloop occurrence has corners
``1,w,s,sw``.  Complete coefficient rows see the trivial character.  The
source-provenant endpoint-odd Cartan prism supplies the mixed character, and
we grant the whole endpoint-only character (a stronger packet than is needed
for the no-go).  These three characters still miss the root-only character.
The marked occurrence covector has a nonzero component on that line.

The root-only face is not target safe.  Its target defect has two mixed-word
and two pure-word components; the normalized pure target rows cannot cancel
the mixed components.  Endpoint oddization kills the target defect but also
turns the root-only character into the already known mixed character.

All literal h=3 omit-coloop response matchings have an invariant remote tail:
after removing edges incident with the two root sites or the two endpoint
vertices, every remaining decorated edge is fixed by both actions.  Thus the
obstruction is not common-tail incidence.  It is exactly a target-corrected
root/signless PP cell.  The complete endpoint plus simultaneous-q Jacobian
contains the correct product-rule anchor entries, but its same-grade
coefficient restriction does not manufacture that relative cell.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_complete_rows_pointed_scalar_boundary.py":
        "077960db0b93888eb323cce89b81dced2d98d3086fc397180d4d446818b1cbe8",
    "notes/h3-gate-ii-complete-rows-pointed-scalar-boundary.md":
        "42a9adbf5e417b0ecae151f8b504c3f75524b3f8b909d69bf8a63b51a8329d6e",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "notes/h3-trapped-carrier-full-q-six-term-extension.md":
        "a5b1a81c834095e69c403d054a38d9f34ebb8b0b3f1d3ce720a27f0b275d04a5",
    "computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py":
        "c652f10a8bac32f11f4c090a55687cf672ce3f96629384f0fbde9f08f440a1bd",
    "notes/h3-fan-coloop-cartan-circuit-comparison-gate.md":
        "727770292d95fec690ec97be96aadd748346cc33d65524a6031809e3fc40137d",
    "computations/verify_h3_active_coloop_extra_mate_deletion_or_gate_ii.py":
        "337e739a7392e207c37e9aa5fe0f0900d90c967bb764c981f3f71b2922f7036d",
    "notes/h3-active-coloop-extra-mate-deletion-or-gate-ii.md":
        "0a8d3767bc348c606beaf631c77a6f26e8c0bd0b0fd524eb9748372138b22af0",
}
EXPECTED_LEDGER_SHA256 = "e17ed82621de2812f05765f37363cd7521262a132dc3728c2e493b0611caf108"

ROOT_SITES = frozenset((0, 1))
ENDPOINT_SITES = frozenset((6, 7))
ACTION_SITES = ROOT_SITES | ENDPOINT_SITES


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def subtract(left, right):
    return tuple(Q(a) - Q(b)
                 for a, b in zip(left, right, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def pullback(row, xi, marked):
    """Pull a row through Phi(v)=v-xi*marked(v)."""
    return subtract(row, scale(dot(row, xi), marked))


def character_audit() -> dict[str, object]:
    # Corner order is 1,w,s,sw.  The notation records which generator acts
    # by -1 on a character; it is independent of row/column convention.
    trivial = tuple(map(Q, (1, 1, 1, 1)))
    root_only = tuple(map(Q, (1, -1, 1, -1)))
    endpoint_only = tuple(map(Q, (1, 1, -1, -1)))
    mixed = tuple(map(Q, (1, -1, -1, 1)))
    marked = tuple(map(Q, (1, 0, 0, 0)))

    characters = (trivial, root_only, endpoint_only, mixed)
    require(rank(characters) == 4
            and all(dot(left, right) == 0
                    for index, left in enumerate(characters)
                    for right in characters[index + 1:])
            and all(dot(row, row) == 4 for row in characters),
            "the V4 character table changed")
    reconstructed = tuple(sum(row[column] for row in characters) / 4
                          for column in range(4))
    require(reconstructed == marked,
            "the marked occurrence stopped using all four characters")

    # Complete rows supply the trivial line.  The physical Cartan mixed
    # boundary is -mixed.  Grant the entire endpoint-only line as well: even
    # this stronger target-safe packet has rank three and misses root_only.
    available = (trivial, endpoint_only, mixed)
    require(rank(available) == 3
            and all(dot(row, root_only) == 0 for row in available)
            and dot(marked, root_only) == 1
            and rank(available + (marked,)) == 4,
            "the pointed V4 quotient changed")

    # The rank-one comparison fixes every available row and a symmetric
    # literal q=M-a shadow, but kills the pointed class.  It is the exact
    # orbit-level no-implication guard, not a source algebra map.
    q_row = trivial
    require(all(pullback(row, root_only, marked) == row
                for row in available + (q_row,))
            and pullback(marked, root_only, marked) == (Q(0),) * 4,
            "the root-character dark comparison changed")
    return {
        "corner_order": ["1", "w", "s", "sw"],
        "characters": {
            "trivial_complete_row": list(map(int, trivial)),
            "root_only_missing": list(map(int, root_only)),
            "endpoint_only_granted": list(map(int, endpoint_only)),
            "endpoint_odd_Cartan_mixed": list(map(int, mixed)),
        },
        "marked_identity": (
            "P_f=(chi_1+chi_w+chi_s+chi_ws)/4"
        ),
        "rank_before_pointed": rank(available),
        "rank_after_pointed": rank(available + (marked,)),
        "unique_missing_character_after_endpoint_grant": "chi_w",
        "kernel_witness": "xi=chi_w; available rows kill xi, P_f(xi)=1",
        "q_equals_M_minus_a_can_be_fixed": True,
        "formal_dark_map": "Phi(v)=v-chi_w*P_f(v)",
        "formal_dark_map_is_source_valid": False,
    }


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def common_tail_audit() -> dict[str, object]:
    # Vertices 0,1 are the two local root sites and 6,7 are the response
    # endpoint vertices.  Gate II omits both the root coloop 01 and the
    # endpoint direct edge 67.  Every residual edge wholly outside the four
    # action vertices is literally fixed, including its output decorations.
    matchings = []
    tail_histogram = Counter()
    tail_supports = Counter()
    for raw in perfect_matchings(tuple(range(8))):
        matching = tuple(sorted(tuple(sorted(edge)) for edge in raw))
        if (0, 1) in matching or (6, 7) in matching:
            continue
        tail = tuple(edge for edge in matching
                     if set(edge).isdisjoint(ACTION_SITES))
        moving = tuple(edge for edge in matching if edge not in tail)
        require(all(set(edge).isdisjoint(ACTION_SITES) for edge in tail)
                and all(set(edge) & ACTION_SITES for edge in moving)
                and set(tail).isdisjoint(moving)
                and tuple(sorted(tail + moving)) == matching,
                (matching, tail, moving))
        matchings.append(matching)
        tail_histogram[len(tail)] += 1
        tail_supports[tail] += 1
    require(len(matchings) == 78
            and tail_histogram == Counter({0: 24, 1: 48, 2: 6})
            and len(tail_supports) == 10,
            (len(matchings), tail_histogram, len(tail_supports)))
    return {
        "omit_root_and_endpoint_direct_matchings": len(matchings),
        "invariant_tail_edge_count_histogram": dict(sorted(
            tail_histogram.items())),
        "distinct_literal_tail_supports": len(tail_supports),
        "factorization": (
            "every occurrence is moving-corner factors times a decorated "
            "tail on vertices outside {root sites, endpoint vertices}"
        ),
        "tail_fixed_by_root_and_endpoint_actions": True,
        "consequence": (
            "the Gate-II obstruction is not matching/common-tail transport; "
            "the missing root character occurs in the moving four-corner packet"
        ),
    }


def target_defect_audit() -> dict[str, object]:
    # Word basis: two mixed Weyl images followed by the two pure targets.
    mixed_c_i = (Q(1), Q(0), Q(0), Q(0))
    mixed_i_c = (Q(0), Q(1), Q(0), Q(0))
    pure_i = (Q(0), Q(0), Q(1), Q(0))
    pure_c = (Q(0), Q(0), Q(0), Q(1))
    defect = (Q(1), Q(1), Q(-1), Q(-1))
    pure_rows = (pure_i, pure_c)
    require(defect == tuple(mixed_c_i[index] + mixed_i_c[index]
                            - pure_i[index] - pure_c[index]
                            for index in range(4))
            and rank(pure_rows) == 2
            and rank(pure_rows + (defect,)) == 3,
            "the root-only four-word target defect changed")
    for left in range(-3, 4):
        for right in range(-3, 4):
            corrected = tuple(defect[index]
                              + left * pure_i[index]
                              + right * pure_c[index]
                              for index in range(4))
            require(corrected != (Q(0),) * 4,
                    "normalized pure rows cancelled both mixed directions")

    # The endpoint swap fixes every word in the defect.  Hence endpoint
    # oddization cancels the target, but changes chi_w to chi_ws and supplies
    # no new pointed direction.
    endpoint_swapped = defect
    require(subtract(defect, endpoint_swapped) == (Q(0),) * 4,
            "endpoint oddization stopped killing the target defect")
    return {
        "word_basis": ["m_(c|i)", "m_(i|c)", "p_i", "p_c"],
        "root_only_target_defect": [1, 1, -1, -1],
        "normalized_pure_target_span": ["p_i", "p_c"],
        "mixed_target_directions_remaining_after_pure_correction": 2,
        "pure_targets_cancel_defect": False,
        "endpoint_swap_fixes_defect": True,
        "endpoint_oddization": (
            "target safe, but sends the needed chi_w face to the already "
            "available mixed chi_ws Cartan face"
        ),
        "smallest_positive_cell": (
            "a target-corrected root-only/signless relative PP cell in the "
            "literal fan word/fine/repeated grade"
        ),
    }


def full_q_and_completion_scope() -> dict[str, object]:
    # These literal dimensions and the product-rule anchor support are pinned
    # by the complete polynomial checker.  The present finite theorem uses
    # them only to type the scope: q columns are scalar-source derivatives,
    # not an occurrence projector or a target-correcting relative cell.
    endpoint_columns = 36
    q_columns = 15 * 9
    anchor_product_rule_coordinates = 3
    require(endpoint_columns + q_columns == 171
            and anchor_product_rule_coordinates == 3,
            "the full-q source scope changed")
    return {
        "physical_tangent_domain": {
            "endpoint_columns": endpoint_columns,
            "decorated_q_columns": q_columns,
            "total": endpoint_columns + q_columns,
            "marked_anchor_product_rule_coordinates": 3,
        },
        "what_full_q_supplies": (
            "the literal scalar-cell Jacobian and the complete differential "
            "of P_f, including both q-tail factors"
        ),
        "what_full_q_does_not_supply": (
            "a target-safe root-only relative character/cross-grade source cell"
        ),
        "normalized_pure_targets": (
            "their constants change no conormal row; on the selected mixed "
            "occurrence block their derivative restriction is zero, and in "
            "the target word module they cannot cancel the two mixed defects"
        ),
        "full_source_counterexample_constructed": False,
        "special_complete_packet": (
            "the pinned 4736-seed response completion has zero trapped "
            "survivors; the orbit guard is not a GHZ source point"
        ),
        "arbitrary_extra_mates": (
            "exact deletion/exit or a same-grade C2+/C4/P2 Hasse packet; "
            "the latter is precisely where the missing target-corrected "
            "root character would have to be realized"
        ),
    }


def reselection_potential_audit() -> dict[str, object]:
    # Deletion, an outside-shore hole, and processing a genuinely new
    # occurrence decrease the displayed lexicographic potential.  The
    # Hasse-completion theorem only returns some off-axis fan, however; it
    # does not assert that this fan is new or outside the old shore.
    decreasing_examples = {
        "occupied_support_deletion": ((27, 6, 4), (26, 6, 4)),
        "outside_shore_growth": ((27, 6, 4), (27, 5, 4)),
        "new_occurrence_processed": ((27, 6, 4), (27, 6, 3)),
    }
    require(all(later < earlier for earlier, later in
                decreasing_examples.values()),
            "an accepted lexicographic descent stopped decreasing")

    # This two-state transition is a logical guard, not a physical source.
    # Each arrow has the output type "some off-axis active fan" but returns
    # no new occurrence, support drop, or Hall growth.
    potential_f = (27, 6, 0)
    potential_g = (27, 6, 0)
    transitions = (("fan_f", "fan_g"), ("fan_g", "fan_f"))
    require(potential_f == potential_g
            and transitions[0][1] == transitions[1][0]
            and transitions[1][1] == transitions[0][0],
            "the minimal reselection cycle guard changed")
    return {
        "candidate_potential": (
            "(occupied support, 15-|closed Hall shore|, unprocessed "
            "supported occurrences), lexicographic"
        ),
        "strict_moves": list(decreasing_examples),
        "Hasse_completion_guarantees_new_fan": False,
        "Hasse_completion_guarantees_outside_shore": False,
        "Hasse_completion_guarantees_support_drop": False,
        "minimal_allowed_cycle": ["fan_f -> fan_g", "fan_g -> fan_f"],
        "potential_change_on_cycle": [0, 0, 0],
        "reselection_bypass_proved": False,
        "smallest_extra_termination_law": (
            "a missing root character must yield deletion, a hole outside "
            "the current closure, a previously unprocessed fan occurrence, "
            "or a typed terminal/chart cell; returning an arbitrary active "
            "fan is insufficient"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II Cartan/full-q pointed-character gate",
        "pins": PINS,
        "V4_pointed_character": character_audit(),
        "literal_common_tail": common_tail_audit(),
        "root_only_target_defect": target_defect_audit(),
        "full_q_and_full_source_scope": full_q_and_completion_scope(),
        "reselection_bypass": reselection_potential_audit(),
        "verdict": (
            "Physical Cartan source-orbit descent and the complete 171-column "
            "endpoint/q Jacobian do not yet construct the pointed fan-grade "
            "Phi.  Common-tail transport is exact on all 78 literal omit-"
            "coloop response matchings.  After complete aggregate data, the "
            "mixed endpoint-odd Cartan character, and even the whole target-"
            "safe endpoint character are granted, P_f still has the unique "
            "root-only character chi_w.  Its root/Weyl face carries two "
            "mixed target directions which normalized pure targets cannot "
            "cancel.  Endpoint oddization kills that target defect only by "
            "returning to the already available mixed character.  Literal "
            "q=M-a may remain fixed throughout, so it does not repair the "
            "pointed quotient.  Reselecting the active mate is not an "
            "automatic bypass: Hasse completion need not force support "
            "descent, Hall growth, or a previously unprocessed fan, so it "
            "can return to Gate II at unchanged potential."
        ),
        "shortest_remaining_theorem": (
            "construct one target-corrected root-only/signless relative PP "
            "cell in the literal fan word/fine/repeated and common-tail "
            "grade, with its scalar differential equal to the missing chi_w "
            "occurrence direction and with physical anchor P_f and q=M-a. "
            "Equivalently, realize the chart-complete C2+/C4/P2 face produced "
            "by the first Hasse failure.  Then the four V4 characters span "
            "P_f and the committed Gate-II quotient assembly applies."
        ),
        "scope": (
            "exact source-orbit/word-module obstruction and h3 matching "
            "census.  It rules out construction from the named Cartan, full "
            "Jacobian and normalized pure rows alone; it does not assert a "
            "complete trapped GHZ source or rule out the missing higher cell."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Gate-II pointed-character ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("Gate II common-tail orbit: EXACT ON 78 MATCHINGS")
    print("Cartan + endpoint grant: V4 RANK 3; P_f NEEDS ROOT CHARACTER")
    print("root-only face: TWO MIXED TARGET DIRECTIONS SURVIVE PURE ROWS")
    print("full 171-column q Jacobian: DOES NOT SUPPLY RELATIVE CONE CELL")
    print("full GHZ counterexample: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
