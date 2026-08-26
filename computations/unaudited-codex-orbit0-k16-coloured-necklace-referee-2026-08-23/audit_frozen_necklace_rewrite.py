#!/usr/bin/env python3
"""Exact referee of the frozen deterministic coloured-necklace rewrite.

This deliberately proves only the finite selected-pivot statement.  It does
not claim confluence for alternative cuts or closure under inverse parents.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TAIL_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
SOURCE = TAIL_DIR / "audit_coloured_necklace_target_reduction.py"
FROZEN = TAIL_DIR / "results_coloured_necklace_target_reduction.json"
OUT = HERE / "results_frozen_necklace_rewrite_referee.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


SPEC = importlib.util.spec_from_file_location("necklace_referee_source", SOURCE)
NECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NECK)


class SignedVectorReducer:
    """Full signed normal vector under the chosen triangular rewrite.

    The Tail reducer used ``Counter += Counter()`` as zero cleanup, which also
    deletes every negative entry.  Explicit zero filtering keeps signed integer
    arithmetic exact.
    """

    def __init__(self):
        self.start = time.monotonic()
        self.memo = {}
        self.choices = {}
        self.relations = 0
        self.raw_children = 0

    def normal(self, state):
        if state in self.memo:
            return self.memo[state]
        if time.monotonic() - self.start > 170:
            raise RuntimeError("signed vector referee time cap")
        if len(state) <= 3:
            value = Counter({state: 1})
            self.memo[state] = value
            return value
        choice = next(NECK.all_valid_choices(state), None)
        require(choice is not None, ("no mixed four-cycle choice",
                                     NECK.state_text(state)))
        indices, cuts, _ = choice
        self.choices[state] = (indices, cuts)
        children = NECK.relation_children(state, indices, cuts)
        self.relations += 1
        self.raw_children += sum(count for _, count in children)
        value = Counter()
        for child, count in children:
            for terminal, coefficient in self.normal(child).items():
                value[terminal] -= count * coefficient
        value = Counter({key: coefficient for key, coefficient in value.items()
                         if coefficient != 0})
        self.memo[state] = value
        return value


def main():
    frozen = json.loads(FROZEN.read_text())
    target = NECK.initial_target()
    reducer = SignedVectorReducer()
    target_normal = Counter()
    for state, multiplicity in sorted(
            target.items(), key=lambda item: NECK.state_text(item[0])):
        for terminal, coefficient in reducer.normal(state).items():
            target_normal[terminal] += multiplicity * coefficient
    target_normal = Counter({key: coefficient
                             for key, coefficient in target_normal.items()
                             if coefficient != 0})

    require(len(reducer.memo) == 14_848, len(reducer.memo))
    require(reducer.relations == frozen["pivot_relations_used"] == 4_141,
            (reducer.relations, frozen["pivot_relations_used"]))
    require(len(target_normal) == frozen["terminal_normal_form_support"] == 10_354,
            (len(target_normal), frozen["terminal_normal_form_support"]))
    require(sum(abs(value) for value in target_normal.values()) ==
            frozen["terminal_coefficient_l1"] == 3_978_533_376,
            sum(abs(value) for value in target_normal.values()))
    base_states = len(reducer.memo)
    terminal, target_pairing = max(target_normal.items(),
                                   key=lambda item: (abs(item[1]), item[0]))

    # The terminal-coordinate coefficient of normal(state) is an exact dual
    # for the selected triangular relation system.
    dual = {state: normal.get(terminal, 0)
            for state, normal in reducer.memo.items()}
    selected_pairings = []
    missing_children = set()
    cycle_drop_histogram = Counter()
    raw_relation_mass_histogram = Counter()
    for parent, (indices, cuts) in reducer.choices.items():
        children = NECK.relation_children(parent, indices, cuts)
        value = dual[parent]
        raw_mass = 1
        for child, multiplicity in children:
            if child not in dual:
                missing_children.add(child)
                continue
            value += multiplicity * dual[child]
            raw_mass += multiplicity
            cycle_drop_histogram[len(parent) - len(child)] += 1
        raw_relation_mass_histogram[raw_mass] += 1
        selected_pairings.append(value)
    require(not missing_children, len(missing_children))
    require(len(selected_pairings) == 4_141, len(selected_pairings))
    require(set(selected_pairings) == {0}, Counter(selected_pairings))
    require(raw_relation_mass_histogram == {105: 4_141},
            raw_relation_mass_histogram)
    require(min(cycle_drop_histogram) >= 1, cycle_drop_histogram)

    # Unique leading parents make these 4,141 selected relations independent.
    pivot_parents = set(reducer.choices)
    require(len(pivot_parents) == 4_141, len(pivot_parents))
    require(all(parent not in dict(NECK.relation_children(parent, *choice))
                for parent, choice in reducer.choices.items()),
            "leading parent survived in nonleading child ledger")

    # Independently replay Tail's lex-first alternative-cut diamond.
    mismatch = frozen["first_confluence_mismatch"]
    require(mismatch["state"] == "00.00.11112222.000011112222",
            mismatch["state"])
    diamond_state = NECK.canonical_state(
        tuple(tuple(map(int, word)) for word in mismatch["state"].split(".")))
    alternative_cuts = tuple(mismatch["cuts"])
    alternative_indices = tuple(mismatch["indices"])
    expected = reducer.normal(diamond_state)
    alternative = Counter()
    for child, count in NECK.relation_children(
            diamond_state, alternative_indices, alternative_cuts):
        for row, coefficient in reducer.normal(child).items():
            alternative[row] -= count * coefficient
    alternative = Counter({key: coefficient
                           for key, coefficient in alternative.items()
                           if coefficient != 0})
    delta = Counter(expected)
    for row, coefficient in alternative.items():
        delta[row] -= coefficient
    delta = Counter({key: coefficient for key, coefficient in delta.items()
                     if coefficient != 0})
    require(delta, "alternative cut unexpectedly confluent")
    require([[NECK.state_text(row), coefficient]
             for row, coefficient in sorted(expected.items(),
                                             key=lambda item: NECK.state_text(item[0]))]
            == mismatch["expected"], "expected diamond ledger differs")
    require([[NECK.state_text(row), coefficient]
             for row, coefficient in sorted(alternative.items(),
                                             key=lambda item: NECK.state_text(item[0]))]
            == mismatch["alternative"], "alternative diamond ledger differs")

    nonzero_dual = {state: value for state, value in dual.items() if value}
    result = {
        "schema": "orbit0-k16-frozen-coloured-necklace-referee-v1",
        "status": "FAIL_ALTERNATIVE_CUT_DIAMOND__NO_FULL_SEPARATOR",
        "frozen_stage": {
            "states": base_states,
            "selected_relations": reducer.relations,
            "selected_relation_rank_over_Q": len(pivot_parents),
            "all_selected_relations_annihilated": len(selected_pairings),
            "dual_nonzero_support_on_frozen_states": len(nonzero_dual),
            "dual_max_abs": max(map(abs, nonzero_dual.values())),
            "target_terminal": NECK.state_text(terminal),
            "target_pairing": target_pairing,
            "target_normal_form_support": len(target_normal),
            "target_normal_form_l1": sum(abs(value)
                                            for value in target_normal.values()),
        },
        "diamond_counterguard": {
            "state": NECK.state_text(diamond_state),
            "alternative_indices": list(alternative_indices),
            "alternative_cuts": list(alternative_cuts),
            "expected_support": len(expected),
            "alternative_support": len(alternative),
            "difference_support": len(delta),
            "difference_l1": sum(abs(value) for value in delta.values()),
            "new_states_needed_for_alternative": len(reducer.memo) - base_states,
            "states_after_alternative": len(reducer.memo),
            "consequence": (
                "Two allowed relation vectors have the same leading state but "
                "different signed normal forms. Their difference cancels the "
                "leading state, so the selected terminal-coordinate dual does "
                "not annihilate the full relation family."
            ),
        },
        "relation_audit": {
            "perfect_matching_terms_per_relation": 105,
            "leading_term_multiplicity": 1,
            "strict_cycle_count_descent": True,
            "termination": True,
            "source_projection_scope": (
                "For a literal balanced source column whose four path endpoints "
                "are the eight distinct physical sites, forgetting site labels "
                "gives exactly this 105-completion necklace relation. The code's "
                "all_valid_choices retains only colours, not physical-site labels "
                "or orbit masses, so arbitrary generated choices are an abstract "
                "enlargement and are not individually certified literal lifts."
            ),
        },
        "separator_condition": {
            "sufficient": (
                "Either prove global confluence of the terminating rewrite for "
                "every projected source relation, or extend the terminal-coordinate "
                "dual to the inverse-parent/full relation closure and verify it "
                "annihilates every relation vector there while pairing the target "
                "nonzero."
            ),
            "not_sufficient": (
                "Agreement of alternative cuts only on the downward target-reached "
                "states: relations rooted outside that set can cancel their common "
                "leading parent and feed a new lower-state relation into the target "
                "component."
            ),
        },
        "terminal_scope": (
            "The signed nonzero normal form proves nonmembership only in the span "
            "of the 4,141 selected triangular relations. The explicit diamond "
            "terminally invalidates it as a separator for the complete necklace "
            "relation module or the literal K16 source module."
        ),
        "pinned": {
            str(SOURCE.relative_to(ROOT)): file_sha256(SOURCE),
            str(FROZEN.relative_to(ROOT)): file_sha256(FROZEN),
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "frozen_states": base_states,
        "states_after_alternative": len(reducer.memo),
        "relations": reducer.relations,
        "selected_dual_support": len(nonzero_dual),
        "target_pairing": target_pairing,
        "diamond_difference_support": len(delta),
        "logical_sha256": logical,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
