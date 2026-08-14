#!/usr/bin/env python3
"""Compare the executable Gamma_* map with the declared C1 grammar.

The operation census of 9ad603f is an exact theorem about its declared free
cellular grammar.  It is not, however, produced by an executable registry of
physical source generators.  The largest executable named map remains a
direct sum whose cross-word response-to-AugP2 object is explicitly absent.

This checker freezes that interface distinction and the smallest possible
guard: one additional total-degree-one source generator with the full
Gamma_* tag and augmented boundary B=delta, every other row zero.  It is a
primitive one-column extension of the current 27-row cap map, raises the
B/Eq rank 7 -> 8, and has normalized Psi=1.  The extension is not asserted
to be a GHZ source cell.  It proves that the current executable constructors
plus the declared census do not themselves establish essential surjectivity
from a full physical C1: a physical generator registry and comparison
functor are still required.
"""

from __future__ import annotations

import argparse
import ast
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import inspect
import json
from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
    "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py":
        "262e1dd08dd1842d60515d45aea53ea406d7e1e5ea55ab506bb6e81d64b07741",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py":
        "feb162f9d13d6debff78361fd28cada31a61bd9ccd57aab62f2722bf365c5064",
}
EXPECTED_LEDGER_SHA256 = "b069c7e0061f080507e3538288e57b20b2f4640f0b61898b9cee2333a832c53b"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4


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


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def declared_grammar_interface_audit(census) -> dict[str, object]:
    records = census.operation_census()
    grade = census.full_grade_audit()
    quotient = census.quotient_audit(records)

    # This is deliberately a source-code assertion, not a prose inference.
    # The census takes no source registry and its body calls no constructor:
    # it returns the fixed tuple of operation records displayed in 9ad603f.
    signature = inspect.signature(census.operation_census)
    syntax = ast.parse(textwrap.dedent(
        inspect.getsource(census.operation_census)))
    calls = tuple(node for node in ast.walk(syntax) if isinstance(node, ast.Call))
    returns = tuple(node for node in ast.walk(syntax)
                    if isinstance(node, ast.Return))
    require(not signature.parameters and not calls and len(returns) == 1,
            "operation_census stopped being a closed literal constructor")

    class_counts = {
        name: sum(record["class"] == name for record in records)
        for name in ("canonical", "dark", "off-grade", "kappa")
    }
    require(len(records) == 17
            and class_counts == {
                "canonical": 1, "dark": 9, "off-grade": 6, "kappa": 1,
            }
            and quotient["literal_kappa_count"] == 8
            and quotient["symbolic_quotient_rank_upper_bound"] == 8,
            (class_counts, quotient))

    return {
        "Gamma_star": {
            "word": grade["word"],
            "fine_lattice_width": grade["fine_lattice_coordinate_width"],
            "fine_packet_size": len(grade["fine_orbit"]),
            "repeated": grade["repeated"],
            "operation_parent": grade["operation_parent"],
            "window": grade["window"],
            "relative_total_degree": grade["relative_total_degree"],
        },
        "operation_census_parameters": 0,
        "operation_census_constructor_calls": 0,
        "operation_census_literal_return_count": 1,
        "record_count": len(records),
        "class_counts": class_counts,
        "kappa_instances": quotient["literal_kappa_words"],
        "formal_quotient_basis_rank":
            quotient["symbolic_quotient_rank_upper_bound"],
        "exact_reading": (
            "the rank-eight result is the free normal-form quotient of the "
            "declared records; operation_census does not enumerate a supplied "
            "physical C1 object"
        ),
    }


def executable_named_map_audit(maximal, private_eq, packaging) \
        -> tuple[tuple[tuple[Q, ...], ...], dict[str, object]]:
    maximal_ledger, maximal_digest = maximal.audit()
    require(maximal_digest == maximal.EXPECTED_LEDGER_SHA256,
            "maximal named map digest changed")
    packaging_ledger, packaging_digest = packaging.audit()
    require(packaging_digest == packaging.EXPECTED_LEDGER_SHA256,
            "packaging digest changed")

    named = maximal_ledger["maximal_named_literal_map"]
    typed = maximal_ledger["typed_projection_and_first_unmodeled_family"]
    package = packaging_ledger["augmented_packaging"]
    require(named["total_coordinates"] == 186
            and named["total_named_columns"] == 146
            and named["total_rank"] == 90
            and not named["compatibility_covector_is_physical_cross_word_terminal"]
            and typed["off_grade_named_columns_with_zero_B_Eq_projection"] == 121
            and not package["existing_AugP2_status"]
                ["constructed_literal_source_object"],
            (named, typed, package))

    cap_columns, cap_names = maximal.cap_named_columns(private_eq)
    delta = tuple(map(int, DELTA))
    psi = tuple(value / Q(4) for value in
                private_eq.vec(B=delta, Eq=tuple(-value for value in delta)))
    require(len(cap_columns) == len(cap_names) == 25
            and len(cap_columns[0]) == 27
            and rank(cap_columns) == 23
            and rank(tuple(column[:8] for column in cap_columns)) == 7
            and all(dot(psi, column) == 0 for column in cap_columns),
            "the executable named cap block changed")

    return cap_columns, {
        "executable_maximal_named_map": {
            "coordinates": named["total_coordinates"],
            "columns": named["total_named_columns"],
            "rank": named["total_rank"],
            "block_dimensions": named["block_dimensions"],
            "block_column_counts": named["block_column_counts"],
        },
        "Gamma_star_named_cap_block": {
            "coordinates": 27,
            "columns": len(cap_columns),
            "rank": rank(cap_columns),
            "B_Eq_projection_rank":
                rank(tuple(column[:8] for column in cap_columns)),
            "all_named_columns_Psi_dark": True,
            "names": list(cap_names),
        },
        "off_grade_named_columns":
            typed["off_grade_named_columns_with_zero_B_Eq_projection"],
        "cross_word_AugP2_source_object_constructed": False,
        "kappa_columns_present_in_executable_map": False,
        "reason": (
            "the executable maximal map remains a four-block direct sum; "
            "the response-to-AugP2 word/fine/repeated placement which would "
            "create the mixed kappa incidence is explicitly unconstructed"
        ),
    }


def one_generator_counterguard(private_eq, cap_columns, grade) \
        -> dict[str, object]:
    delta = tuple(map(int, DELTA))
    epsilon = private_eq.vec(B=delta)
    psi = tuple(value / Q(4) for value in
                private_eq.vec(B=delta, Eq=tuple(-value for value in delta)))

    projected = tuple(column[:8] for column in cap_columns)
    require(len(epsilon) == 27
            and epsilon[:8] == DELTA + ZERO4
            and epsilon[8:] == (Q(0),) * 19
            and rank(cap_columns) == 23
            and rank(cap_columns + (epsilon,)) == 24
            and rank(projected) == 7
            and rank(projected + (epsilon[:8],)) == 8
            and dot(psi, epsilon) == 1,
            "the one-column physical-row counterguard changed")

    # At source-quotient level the declared eight normal forms embed in a
    # nine-dimensional extension.  No combination of them gives epsilon.
    declared = tuple(
        tuple(Q(1 if row == column else 0) for row in range(9))
        for column in range(8)
    )
    exotic = (Q(0),) * 8 + (Q(1),)
    require(rank(declared) == 8
            and rank(declared + (exotic,)) == 9,
            "the minimal source quotient counterguard changed")

    return {
        "new_source_generator": "epsilon",
        "full_tag": {
            "word": grade["word"],
            "fine_lattice_width": grade["fine_lattice_width"],
            "fine_packet_size": grade["fine_packet_size"],
            "repeated": grade["repeated"],
            "operation_parent": grade["operation_parent"],
            "window": grade["window"],
            "relative_total_degree": 1,
        },
        "canonical_source_shadow": "zero",
        "augmented_row_order": (
            "B4,Eq4,target4,W4,ores4,M,ainc,q,Pf,ridge,eta,sigma"
        ),
        "boundary": {
            "B": [1, 1, -1, -1],
            "Eq": [0, 0, 0, 0],
            "all_other_19_rows": 0,
        },
        "q_equals_M_minus_ainc": True,
        "normalized_Psi": "1",
        "full_cap_rank_effect": [23, 24],
        "B_Eq_rank_effect": [7, 8],
        "declared_to_extended_source_quotient_ranks": [8, 9],
        "minimality": (
            "a non-surjective linear comparison needs cokernel dimension at "
            "least one; epsilon realizes dimension one with primitive integral "
            "B/Eq boundary"
        ),
        "scope_guard": (
            "epsilon is a source-interface countermodel, not a claimed "
            "source-provenant GHZ operation"
        ),
    }


def interface_theorem() -> dict[str, object]:
    return {
        "literal_essential_surjectivity_currently_proved": False,
        "why": (
            "the declared grammar census is a closed literal tuple, while "
            "the executable named map has no cross-word AugP2 object and no "
            "eight kappa columns; there is therefore no implemented domain "
            "C1_phys,Gamma* or comparison functor on which essential "
            "surjectivity could be checked"
        ),
        "sharp_additional_hypothesis": (
            "provide a finite executable registry Gen_phys(Gamma*) of every "
            "primitive physical total-degree-one constructor and a chain/"
            "augmentation-preserving comparison functor to the canonical "
            "cellular grammar; prove each registry entry is canonical, "
            "chi-dark, or one of the eight kappa instances"
        ),
        "shortest_attack": [
            "construct the missing literal 11110000 -> 01211222 PP/AugP2 placement",
            "generate its eight one-root K_Eq interchange cells with full tags",
            "make every physical C1 constructor register itself at fixed Gamma*",
            "run a finite factorization/chi test on the resulting registry",
        ],
        "terminal_alternative": (
            "one registered entry with nonzero delta.(B-Eq) is the actual "
            "bright filler; otherwise the registered comparison proves the "
            "desired essential-surjectivity/darkness terminal"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    census = load(
        "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py",
        "gamma_star_declared_census",
    )
    maximal = load(
        "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py",
        "gamma_star_executable_maximal",
    )
    private_eq = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "gamma_star_private_eq",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "gamma_star_packaging",
    )

    declared = declared_grammar_interface_audit(census)
    cap_columns, executable = executable_named_map_audit(
        maximal, private_eq, packaging)
    counterguard = one_generator_counterguard(
        private_eq, cap_columns, declared["Gamma_star"])
    ledger = {
        "theorem": "h3 Gamma-star physical C1 registry counterguard",
        "pins": PINS,
        "declared_grammar_interface": declared,
        "executable_named_source_row_map": executable,
        "smallest_unexcluded_extension": counterguard,
        "interface_verdict": interface_theorem(),
        "verdict": (
            "The 9ad603f census is exact for its declared free cellular "
            "grammar but is not literal essential surjectivity from the "
            "actual physical C1.  Its operation list is a zero-input closed "
            "tuple and its rank-eight quotient uses formal unit normal forms. "
            "The executable maximal named map still omits the cross-word "
            "AugP2 object and all kappa columns.  A single same-tag primitive "
            "extension with B=delta, all other physical rows zero, is invisible "
            "to that interface yet raises the B/Eq rank 7 to 8.  Excluding it "
            "requires an executable full physical generator registry and a "
            "proved comparison functor, not another prose operation pin."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "interface", "guard"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("Gamma-star C1 registry ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 Gamma_* physical C1 registry counterguard "
              f"({arguments.mode}): PASS")
        print("declared grammar -> physical C1 essential surjectivity: NOT PROVED")
        print("smallest unexcluded extension: one primitive Gamma_* column")
        print("B/Eq rank: 7 -> 8; normalized Psi(epsilon)=1")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
