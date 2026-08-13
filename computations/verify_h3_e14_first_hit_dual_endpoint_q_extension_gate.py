#!/usr/bin/env python3
"""Audit the E14 first-hit covector against committed endpoint/q interfaces.

This is deliberately an audit of *literal columns in one source map*.  A
coarse endpoint quotient, a source-domain q covector, or a word-changing bar
in another word summand is not silently inserted as a column of the 4180-row
E14 first-hit matrix.

The exact 22-support covector gets its entire value on the canonical target
from one unary S-pair companion.  Every old complete unary/G11 column which
contains that companion also contains compensating visible tails.  The
currently promoted decorated core is invisible.  No committed endpoint/q
interface supplies a full same-grade comparison column, so extension by zero
over those separately presented blocks survives.  This is not yet a physical
terminal; it isolates the first possible killing datum.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py":
        "37f571234346c8a90465a5e021bb5ed97b0caec68e31a8b80346d25f94c9f337",
    "notes/h3-relative-occurrence-e14-w-carrier-landing-gate.md":
        "a4a0e1be3cff6779f3641f6c3f1faa6431eac01b85a4cdf1bfbfc9d595d56888",
    "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py":
        "00db2478df3162a374434ea7d0ab285f770510d33b72619377560404c96b16e8",
    "computations/verify_h3_centered_projector_e14_word_arrow_gate.py":
        "e1b8b17c75292f55439652ac9e5dcb1a24a3e4079c2d378e9fa63544e5491b46",
    "notes/h3-centered-projector-e14-word-arrow-gate.md":
        "e0c5249f0e79551c87dbd1b25bc3e52501ea1ae7eac07484509bbd38d18cf3de",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "notes/h3-local-gl3-normalized-bar-word-change-obstruction.md":
        "a12f8685ecd98a1ad71a2e7829acbe00ba2db597559ad8e726d42105aed60d20",
    "computations/verify_h3_component_iv_cyclotomic_word_change_relation.py":
        "335c82b382dcb3b8d69cd57a4fa54185a0db96368b5413b218b7c0f8bf303dae",
    "notes/h3-component-iv-cyclotomic-word-change-relation.md":
        "ffae52a1adeb4eef3f94f550778b04bdcfdc2bd02fb65292c174fa3c54920975",
    "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py":
        "bc11c8fe61ec8c21a1850326de037a328ab7f7404bcf3902655f6541e496bc9f",
    "notes/h3-residual-q-ks-constructive-landing-boundary.md":
        "225f79e54f121c375771510b4a9a07c3b666e0ffc36b4b9ebfd589c9c475756b",
    "computations/verify_dark_cartan_physical_q_transport_gate.py":
        "8dc8e1e25316fd32ac27d86ebfff1ca77c870c302ff7becd9f10751d8567046c",
    "notes/dark-cartan-physical-q-transport-gate.md":
        "da4b08160796b659b42e891efaae08d5063693af704394b70ae6904faa1c4424",
    "computations/verify_h3_c6_e14_private_rewrite_spair_boundary.py":
        "d3605323f2a305dbc6c5dec38313ecb55c2f7a5676a255117abe9d0b773889a4",
    "notes/h3-c6-e14-private-rewrite-spair-boundary.md":
        "ac81c307c484dd1470a1ea953a70ee8c00a2e0cf875e31aff7f75f2e25315593",
}
EXPECTED_LEDGER_SHA256 = (
    "076a7b7cafb8b94bfa218a5fd1b8324c446c98f114f38fa8a70242cb2303fbba"
)

ENDPOINT = ("p1_0_1", "s1_1_1")
COMPANION = (ENDPOINT, ("u05_01", "v1301", "v2411"))
CORE = (ENDPOINT, ("u05_01", "v2411", "v3410"))
PRIVATE = (ENDPOINT, ("u35_11", "v0400", "v2411"))


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


def pair(dual, vector):
    return sum((coefficient * dual.get(coordinate, Q(0))
                for coordinate, coefficient in vector.items()), Q(0))


def projected_rank_and_remainder(first, columns, target, killed_prefixes):
    def survives(coordinate):
        monomial = coordinate[1]
        return not any(any(factor.startswith(prefix) for prefix in killed_prefixes)
                       for factor in monomial)

    projected_columns = []
    for column in columns.values():
        projected_columns.append({coordinate: coefficient
                                  for coordinate, coefficient in column.items()
                                  if survives(coordinate)})
    projected_target = {coordinate: coefficient
                        for coordinate, coefficient in target.items()
                        if survives(coordinate)}
    pivots = {}
    for column in projected_columns:
        first.add_exact_column(column, pivots)
    remainder = first.exact_reduce(projected_target, pivots)
    target_normal = {
        coordinate: coefficient for coordinate, coefficient in remainder.items()
        if coordinate[0][0] == "target_unary"
    }
    return len(pivots), remainder, target_normal


def reconstruct_first_hit():
    base = load(
        "computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py",
        "e14_endpoint_q_base",
    )
    # Replaying this first certifies the exact 269 -> 270 obstruction and its
    # pinned 22-support dual before we inspect individual sparse columns.
    base_ledger, base_digest = base.audit()
    require(base_digest == base.EXPECTED_LEDGER_SHA256,
            "relative E14 landing dependency changed")

    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "e14_endpoint_q_first",
    )
    rewrite = first.load(first.REWRITE_PATH, "e14_endpoint_q_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "e14_endpoint_q_top")
    two = top.load(top.TWO_CELL_PATH, "e14_endpoint_q_two")
    e14 = two.load(two.E14_PATH, "e14_endpoint_q_e14")
    b4 = e14.load(e14.B4_PATH, "e14_endpoint_q_b4")
    _candidates, _names, responses, unary = two.universal(e14, b4, 1, 1)

    pivot = ("u35_11",)
    multiplier = ("v2411",)
    word = (0, 0, 0, 1, 0, 1)
    factor, remainder = first.factor_unary(unary[word], pivot)
    require(factor == {(): Q(-1), ("v0400",): Q(1)}
            and len(remainder) == 12, "canonical unary factor changed")
    target = {
        (ENDPOINT, first.multiply_monomials(monomial, multiplier)): coefficient
        for monomial, coefficient in remainder.items()
    }

    response_rows = [(output_word, first.response_terms(row))
                     for output_word, row in responses.items()]
    unary_rows = [(output_word, tuple(polynomial.items()))
                  for output_word, polynomial in unary.items()]
    columns = {}
    for target_endpoint, target_monomial in target:
        for row_index, (output_word, row) in enumerate(response_rows):
            for row_endpoint, row_monomial, _coefficient in row:
                if row_endpoint != target_endpoint:
                    continue
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (output_endpoint,
                     first.multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_endpoint, output_monomial, output_coefficient in row
                }
                if output_word == (1,) * 6:
                    column[(("target_G11",), row_multiplier)] = Q(-1)
                columns[("G11", row_index, output_word,
                         row_multiplier)] = column
        for row_index, (output_word, row) in enumerate(unary_rows):
            for row_monomial, _coefficient in row:
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (target_endpoint,
                     first.multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_monomial, output_coefficient in row
                }
                if output_word == (0,) * 6:
                    column[(("target_unary",) + target_endpoint,
                            row_multiplier)] = Q(-1)
                columns[("unary", row_index, output_word, target_endpoint,
                         row_multiplier)] = column

    pivots = {}
    for column in columns.values():
        first.add_exact_column(column, pivots)
    reduced = first.exact_reduce(target, pivots)
    require(len(columns) == len(pivots) == 269 and len(reduced) == 2,
            "first-hit reconstruction changed")
    free = min(reduced)
    dual = {free: Q(1)}
    for leading in sorted(pivots, reverse=True):
        value = sum((coefficient * dual.get(coordinate, Q(0))
                     for coordinate, coefficient in pivots[leading].items()
                     if coordinate != leading), Q(0))
        if value:
            dual[leading] = -value
    require(len(dual) == 22 and pair(dual, target) == -1
            and all(pair(dual, column) == 0 for column in columns.values()),
            "first-hit dual changed")
    require(dual.get(COMPANION) == 1 and dual.get(CORE, 0) == 0,
            "companion/core values changed")

    target_contributions = {
        coordinate: coefficient * dual.get(coordinate, Q(0))
        for coordinate, coefficient in target.items()
        if coefficient * dual.get(coordinate, Q(0))
    }
    require(target_contributions == {COMPANION: Q(-1)},
            ("target pairing stopped being companion-local", target_contributions))

    hits = {name: column for name, column in columns.items()
            if column.get(COMPANION, 0)}
    type_count = Counter(name[0] for name in hits)
    require(type_count == {"unary": 17, "G11": 5}
            and all(pair(dual, column) == 0 for column in hits.values()),
            ("old companion-hit census changed", type_count))

    selected_name = next(name for name in hits
                         if name[0] == "unary" and name[2] == word
                         and name[-1] == multiplier)
    selected = hits[selected_name]
    selected_contributions = {
        coordinate: coefficient * dual.get(coordinate, Q(0))
        for coordinate, coefficient in selected.items()
        if coefficient * dual.get(coordinate, Q(0))
    }
    require(sum(selected_contributions.values(), Q(0)) == 0
            and COMPANION in selected_contributions
            and PRIVATE in selected_contributions,
            ("selected unary S-pair cancellation changed",
             selected_name, selected_contributions))

    q13_rank, q13_remainder, q13_target = projected_rank_and_remainder(
        first, columns, target, ("v13",))
    q0413_rank, q0413_remainder, q0413_target = projected_rank_and_remainder(
        first, columns, target, ("v04", "v13"))
    require((q13_rank, len(q13_target)) == (211, 9)
            and (q0413_rank, len(q0413_target)) == (185, 8),
            ("q13/v04 target-normal migration changed",
             q13_rank, len(q13_target), q0413_rank, len(q0413_target)))
    require(COMPANION not in q13_remainder and q13_target
            and q0413_target,
            "deleting the visible companion did not migrate to target debt")

    return {
        "first": first,
        "base_ledger": base_ledger,
        "target": target,
        "columns": columns,
        "dual": dual,
        "target_contributions": target_contributions,
        "hits": hits,
        "type_count": type_count,
        "selected_name": selected_name,
        "selected_contributions": selected_contributions,
        "q13": (q13_rank, q13_remainder, q13_target),
        "q0413": (q0413_rank, q0413_remainder, q0413_target),
    }


def audit_committed_extension_scope(data):
    inventory = load(
        "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py",
        "e14_endpoint_q_inventory",
    )
    inventory_ledger, inventory_digest = inventory.audit()
    require(inventory_digest == inventory.EXPECTED_LEDGER_SHA256
            and not inventory_ledger["smallest_new_datum"][
                "ordinary_existing_family"],
            "shared four-term bounded inventory changed")

    arrow = load(
        "computations/verify_h3_centered_projector_e14_word_arrow_gate.py",
        "e14_endpoint_q_arrow",
    )
    arrow_ledger, arrow_digest = arrow.audit()
    require(arrow_digest == arrow.EXPECTED_LEDGER_SHA256,
            "centered/E14 word-arrow dependency changed")
    word_gate = arrow_ledger["decorated_core_and_bar"]
    require(word_gate["root_source_word"] == "01211222"
            and word_gate["E14_unary_word"] == "000101"
            and word_gate["normalized_bar_constructs_01211222_to_00000000"]
            and not word_gate[
                "normalized_bar_constructs_E14_unary_G11_S_pair_transport"],
            ("centered/E14 word gate changed", word_gate))

    # The other committed word-change is a literal theorem, but for the fixed
    # K8 pair 11211200/01211200.  Pinning and checking its declared words is
    # enough to exclude it from this exact 000101/01211222 comparison grade.
    component_source = (ROOT / (
        "computations/verify_h3_component_iv_cyclotomic_word_change_relation.py"
    )).read_text()
    require('"11211200"' in component_source and '"01211200"' in component_source,
            "Component-IV word scope changed")

    # The KS checker itself limits its conclusion to the routed endpoint/tail
    # quotient and expressly withholds a full Spencer lift.  Coarse S,D data
    # cannot determine the E14 dual: two completions with the same D readout
    # may differ by the companion coordinate.
    coarse_D = (Q(1), Q(0))
    completion_dark = (Q(1), Q(0))
    completion_bright = (Q(1), Q(1))
    coarse_projection = lambda value: value[0]
    companion_dual = (Q(0), Q(1))
    require(coarse_projection(completion_dark) == coarse_D[0]
            == coarse_projection(completion_bright)
            and sum(a * b for a, b in zip(companion_dual, completion_dark)) == 0
            and sum(a * b for a, b in zip(companion_dual, completion_bright)) == 1,
            "coarse endpoint completion counterguard changed")
    ks_source = (ROOT / (
        "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py"
    )).read_text()
    require("not a reconstruction of the full Spencer lift" in ks_source,
            "KS checker scope changed")

    # Physical q is a source-domain row.  Its placement in another grade is
    # defined only after a whole-domain comparison Phi and the pullback law.
    # With no such comparison into the 4180-row E14 presentation, the honest
    # combined map is a direct sum and lambda extends by zero on the q block.
    q_source = (ROOT / "computations/verify_dark_cartan_physical_q_transport_gate.py").read_text()
    require("q_placed=q_h3 Phi on the whole source domain" in q_source,
            "physical-q transport law changed")
    q_test_columns = ((Q(1), Q(0)), (Q(1), Q(1)))
    extended_zero = (Q(0), Q(0))
    require(all(sum(a * b for a, b in zip(extended_zero, column)) == 0
                for column in q_test_columns),
            "zero extension over separate q block changed")

    return {
        "literal_E14_columns_added": 0,
        "complete_bounded_endpoint_inventory_digest": inventory_digest,
        "reason": (
            "all complete 000101 unary/G11 columns are already among the 269; "
            "the committed centered/rootless, GL3 and Component-IV arrows live "
            "in different word summands, KS is only a routed quotient, and q "
            "is a source row requiring a whole-domain Phi before pullback"
        ),
        "word_scopes": {
            "E14_first_hit": "000101",
            "centered_rootless": "01211222",
            "normalized_GL3_endpoint": "00000000",
            "Component_IV_pair": ["11211200", "01211200"],
        },
        "coarse_KS_same_D_has_dual_values": ["0", "1"],
        "physical_q_row_law": "q_placed=q_h3 Phi on the whole source domain",
        "whole_domain_Phi_to_E14_first_hit_committed": False,
        "strongest_literal_extension": (
            "direct-sum extension by zero; it kills every separately presented "
            "endpoint/q block and still reads -1 on w_E14"
        ),
        "is_physical_terminal": False,
    }


def display_coordinate(coordinate):
    return [list(coordinate[0]), list(coordinate[1])]


def display_sparse(vector):
    return [[display_coordinate(coordinate), str(coefficient)]
            for coordinate, coefficient in sorted(vector.items())]


def audit():
    pin_dependencies()
    data = reconstruct_first_hit()
    scope = audit_committed_extension_scope(data)
    q13_rank, q13_remainder, q13_target = data["q13"]
    q0413_rank, q0413_remainder, q0413_target = data["q0413"]

    ledger = {
        "theorem": "E14 first-hit dual endpoint/q extension gate",
        "pins": PINS,
        "exact_first_hit": {
            "word": "000101",
            "column_count": len(data["columns"]),
            "rank_Q": 269,
            "target_augmented_rank_Q": 270,
            "dual_support": len(data["dual"]),
            "dual_on_target": str(pair(data["dual"], data["target"])),
            "only_nonzero_target_contribution": display_sparse(
                data["target_contributions"]),
            "decorated_core": display_coordinate(CORE),
            "dual_on_decorated_core": str(data["dual"].get(CORE, 0)),
            "unary_S_pair_companion": display_coordinate(COMPANION),
            "dual_on_companion": str(data["dual"].get(COMPANION, 0)),
        },
        "complete_old_companion_hits": {
            "count": len(data["hits"]),
            "by_family": dict(data["type_count"]),
            "all_dual_pairings_zero": True,
            "selected_000101_unary_column": repr(data["selected_name"]),
            "selected_nonzero_dual_contributions": display_sparse(
                data["selected_contributions"]),
            "interpretation": (
                "the companion occurs in old complete rows, but never alone: "
                "each occurrence carries a compensating combination on the "
                "22-support covector"
            ),
        },
        "committed_endpoint_q_extension": scope,
        "tempting_q13_deletion": {
            "set_all_v13_star_to_zero": {
                "rank_Q": q13_rank,
                "rank_drop_from_269": 269 - q13_rank,
                "reduced_target_support": len(q13_remainder),
                "target_unary_readout_support": len(q13_target),
                "target_unary_remainder": display_sparse(q13_target),
            },
            "set_all_v04_star_and_v13_star_to_zero": {
                "rank_Q": q0413_rank,
                "rank_drop_from_269": 269 - q0413_rank,
                "reduced_target_support": len(q0413_remainder),
                "target_unary_readout_support": len(q0413_target),
                "target_unary_remainder": display_sparse(q0413_target),
            },
            "verdict": (
                "deleting the visible v1301 companion does not close the "
                "obstruction; it migrates to 9, respectively 8, pure "
                "target-unary normal/readout coordinates"
            ),
        },
        "first_possible_killing_datum": {
            "linear_criterion": (
                "a literal same-grade augmented column b with "
                "lambda_E14(b_E14) != 0"
            ),
            "minimal_coordinate_model": "e_(u05_01 v1301 v2411)",
            "minimal_model_pairing": "1",
            "source_valid_form_required": (
                "a target-bearing endpoint-word-change/unary-times-q cone "
                "whose full E14 projection breaks the existing 22-support "
                "cancellation; the proper q/target/residue/anchor/W faces "
                "must be included"
            ),
            "why_target_bearing": (
                "forcing the companion to zero only transfers the obstruction "
                "to target_unary readouts, so a q-only or endpoint-only "
                "quotient cannot be the full killing datum"
            ),
            "committed": False,
        },
        "verdict": (
            "No currently committed literal endpoint-word-change or physical-q "
            "column kills the 22-support E14 first-hit dual in the exact "
            "000101/01211222 comparison grade.  The strongest honest extension "
            "is by zero over separately presented blocks.  The first missing "
            "object is a full target-bearing unary S-pair comparison cone, not "
            "the decorated core and not the routed KS endpoint difference."
        ),
        "scope": (
            "Exact for the canonical chart-(1,1) 269-column E14 first-hit "
            "module and the pinned committed word/q interfaces.  This is not "
            "a full physical terminal: no complete 000101<->01211222 Phi has "
            "yet been constructed, so later columns may kill the seed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint/q extension ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("E14 22-support seed through committed literal endpoint/q map: SURVIVES")
    print("target pairing: companion only (-1); decorated core: 0")
    print("old companion-hit columns: 22 = 17 unary + 5 G11, all killed")
    print("v13*=0: rank 211, 9 target-unary debts")
    print("v04*=v13*=0: rank 185, 8 target-unary debts")
    print("next possible killer: full target-bearing unary S-pair comparison cone")
    print("physical terminal: NOT YET PROMOTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
