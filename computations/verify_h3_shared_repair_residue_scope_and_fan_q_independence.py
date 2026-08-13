#!/usr/bin/env python3
"""Separate the Gate-I labelled-residue section from the Gate-II q square.

The shared-repair anchor-fibre theorem grants six multiplier-labelled pure
ordinary-residue columns.  The committed source inventory constructs only
one aggregate scalar ordinary-residue column; it does not construct a
section into the six pure multiplier labels.  The physical odd Cartan line
does not fill this gap.

Moreover, even a perfect protected comparison Phi with literal q=M-a rows
does not imply such a section.  A finite exact guard keeps J, Phi, M, a and
q fixed while changing the labelled-residue map from the identity to the
rank-one aggregate map.  Every q comparison remains exact, but all four
fixed/paired shared-repair directions leave the residue image.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py":
        "ee04e571ccd6eba9bac1bfbd9233a0d2adeb30c275e4156adefe75570c8911e6",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
    "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py":
        "7abab46d3ae648dd309c2fec3266e70dec5b95c5fd150fea2c8c6035840e9bd3",
    "computations/verify_h3_fan_coloop_packet_q_comparison_defect.py":
        "86db5c89196a183c5ddc2b1c2198029fa45ea1cdff1f7d239a74870cd4957e94",
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
}
EXPECTED_LEDGER_SHA256 = "ec9df0c2cd44e7631adeaa0ea9f4454a9598ad596ed8820dd580e551a93e8188"

N = 6


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def mat_mul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(dot(row, column) for column in columns)
                 for row in left)


def row_mat(row, matrix):
    return tuple(dot(row, column) for column in zip(*matrix, strict=True))


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


def unit(index):
    return tuple(Q(int(position == index)) for position in range(N))


def audit_committed_source_scope():
    fibre = load(
        "computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py",
        "repair_residue_scope_fibre",
    )
    clean = load(
        "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py",
        "repair_residue_scope_clean",
    )
    abcde = load(
        "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py",
        "repair_residue_scope_abcde",
    )
    cartan = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "repair_residue_scope_cartan",
    )

    fibre_ledger, fibre_digest = fibre.audit()
    cone = fibre_ledger["generous_complete_projected_cone"]
    require(fibre_digest == fibre.EXPECTED_LEDGER_SHA256
            and cone["column_families"]["pure_ores_Cartan_companion"] == 6
            and cone["strengthening"].startswith(
                "all labelwise pure-ores companions"),
            "the six residue columns stopped being an explicit grant")

    clean_typed = clean.typed_inventory_audit()
    clean_kernel = clean.stabilizer_kernel_no_go()
    require(clean_typed["row_order"][-3:] == ["ores", "ainc", "chart"]
            and clean_kernel["pure_ordinary_residue_columns"] == 1,
            "the committed aggregate residue inventory changed")

    abcde_records = abcde.target_normalized_lift()
    require(len(abcde_records) == 4
            and {record["formula"] for record in abcde_records}
                == {"x=R-T-Y*rho+Y*d_ores"},
            "the scalar target-normalization formula changed")

    cartan_ledger = cartan.audit()
    packet = cartan_ledger["physical_packet"]
    require(packet["ordinary_residue"] == [-1, 1, 1, -1]
            and packet["protected_D_W_target_anchor_Eq"] == 0,
            "the physical endpoint-odd Cartan residue line changed")

    candidates = {
        "fixed_B1": unit(1),
        "fixed_B4": unit(4),
        "paired_B0_B5": tuple(Q(int(index in (0, 5)), 2)
                                for index in range(N)),
        "paired_B2_B3": tuple(Q(int(index in (2, 3)), 2)
                                for index in range(N)),
    }
    aggregate = (Q(1),) * N
    cartan_line = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    require(rank((aggregate, cartan_line)) == 2
            and all(rank((aggregate, cartan_line, candidate)) == 3
                    for candidate in candidates.values()),
            "a repair residue direction entered the known aggregate/Cartan span")

    return {
        "conditional_anchor_fibre_grants_labelled_residue_columns": 6,
        "committed_aggregate_scalar_residue_columns": 1,
        "physical_Cartan_residue_line": [int(value) for value in cartan_line],
        "known_aggregate_plus_Cartan_rank": 2,
        "repair_directions": {
            name: [str(value) for value in candidate]
            for name, candidate in candidates.items()
        },
        "every_repair_direction_outside_known_residue_span": True,
        "missing_equivariant_sections": 2,
    }


def audit_q_comparison_independence():
    # Keep the complete protected square and literal q=M-a decomposition
    # fixed.  Only the independent labelled ordinary-residue map changes.
    identity = tuple(unit(index) for index in range(N))
    protected = (unit(0), unit(1))
    codomain_change = ((Q(1), Q(0)), (Q(0), Q(1)))
    phi = identity
    require(mat_mul(protected, phi)
            == mat_mul(codomain_change, protected),
            "the exact protected comparison guard changed")

    matching = tuple(map(Q, (1, 1, 0, 0, 0, 0)))
    anchor = tuple(map(Q, (0, 1, 0, 0, 0, 0)))
    q = tuple(left - right for left, right
              in zip(matching, anchor, strict=True))
    require(q == unit(0) and row_mat(q, phi) == q,
            "the literal q=M-a comparison stopped being exact")

    # Good residue map: identity.  Bad residue map: every source coordinate
    # lands on the same aggregate line.  The protected/q data above do not
    # see this replacement.
    aggregate = (Q(1),) * N
    residue_good = identity
    residue_bad = tuple(aggregate for _index in range(N))
    require(rank(residue_good) == N and rank(residue_bad) == 1,
            "the good/bad residue ranks changed")
    candidates = (
        unit(1), unit(4),
        tuple(Q(int(index in (0, 5)), 2) for index in range(N)),
        tuple(Q(int(index in (2, 3)), 2) for index in range(N)),
    )
    bad_span = (aggregate,)
    require(all(rank(bad_span + (candidate,)) == 2
                for candidate in candidates),
            "the rank-one residue guard acquired a repair section")

    return {
        "protected_square": "J0*Phi=A*J with Phi=I6",
        "literal_matching_row_M": [str(value) for value in matching],
        "literal_anchor_row_a": [str(value) for value in anchor],
        "q_equals_M_minus_a": [str(value) for value in q],
        "q_comparison_defect": [0] * N,
        "same_q_data_good_labelled_residue_rank": rank(residue_good),
        "same_q_data_bad_aggregate_residue_rank": rank(residue_bad),
        "bad_map_contains_fixed_or_paired_repair_direction": False,
        "conclusion": (
            "a protected Phi and literal q=M-a rows constrain dual packet "
            "readouts; they do not imply a primal section of the labelled "
            "ordinary-residue map"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "shared-repair residue scope and fan-q independence",
        "committed_source_scope": audit_committed_source_scope(),
        "exact_independence_guard": audit_q_comparison_independence(),
        "sharp_missing_statement": (
            "construct two rho-equivariant source chains in the canonical "
            "faces-(3,5) grade, one fixed and one paired, with zero lower/W/"
            "target/ainc output and labelled ordinary residue equal to the "
            "chosen fixed and paired repair directions, modulo the physical "
            "endpoint-odd Cartan residue line"
        ),
        "uniform_theorem_needed": (
            "a genuinely augmented shifted-label theorem must transport the "
            "central word/fine/tail labels and prove both the protected q "
            "square and a separate labelled-residue square with the required "
            "rank-two section.  The current Gate-II Phi/q hypothesis contains "
            "only the first square"
        ),
        "verdict": (
            "Gate I remains conditional on one two-orbit labelled-residue "
            "typing theorem.  Gate II's protected odd Phi with q=M-a does "
            "not imply it, even formally; unification requires strengthening "
            "the shifted-label theorem, not relabelling the existing q square"
        ),
        "scope": (
            "exact audit of committed residue inventories plus a finite "
            "linear independence guard; no nonexistence claim in a larger "
            "relative source resolution"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("shared-repair residue-scope ledger changed", digest))
    print("h3 shared-repair residue scope: ONE TWO-ORBIT TYPING REMAINS")
    print("physical Cartan line: proved; labelwise pure-ores section: absent")
    print("fan Phi plus q=M-a implies labelled residue section: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
