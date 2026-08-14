#!/usr/bin/env python3
"""Unique PS mate of F02 and forced pure-word head-12 exit.

Retain the exact factor cycle and the unique J=q03^(0,1) mate of F01.  The
mandatory F02=T*J*L*b at 001100:02 has one unique positive minimum mate:
R=s_2(site 3, physical colour 1).  Its target contribution is P0*R*L*b.
The same R creates the private pure-word row G12=P1*R*c*e at 111111:12.
The exact identity P1*c*e*F02-P0*L*b*G12=P1*c*e*T*J*L*b has a torus-unit
right side.  Thus the head chase 01 -> 02 cannot recur inside the mixed
word/fine fibre: closing 02 exits to a pure colour-one response row.
"""

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_pure21_exact_scc_private_export_gate.py"
)
SPEC = spec_from_file_location("private_export_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
P = module_from_spec(SPEC)
SPEC.loader.exec_module(P)
C = P.C
S = P.S
E = P.E
F = P.F
M = P.M
B = P.B


R_KEY = (2, 3, 1)
R = B.variable("R")
PURE_ONE = (1,) * 6
G12 = (PURE_ONE, 1, 2)


def install_symbolic_head02(include_r=False):
    P.install_symbolic_cycle(include_j=True)
    if include_r:
        B.SECOND[R_KEY] = R


def install_normalized_head02(include_r=False):
    P.install_normalized_cycle(include_j=True)
    if include_r:
        B.SECOND[R_KEY] = B.constant(-1)


def enumerate_paths():
    install_symbolic_head02()
    word = P.WORD
    row, column = (0, 2)
    paths = []
    for matching in B.matchings(B.SITES):
        additions = []
        if (row, column) not in B.DIRECT:
            additions.append(("d", (row, column)))
        additions.extend(
            ("q", (left, right, word[left], word[right]))
            for left, right in matching
            if (left, right, word[left], word[right]) not in B.Q_EDGE
        )
        paths.append(("DQ", matching, tuple(additions)))
    for p_site in B.SITES:
        for s_site in B.SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in B.SITES if site not in (p_site, s_site))
            for matching in B.matchings(rest):
                additions = []
                p_key = (row, p_site, word[p_site])
                s_key = (column, s_site, word[s_site])
                if p_key not in B.FIRST:
                    additions.append(("p", p_key))
                if s_key not in B.SECOND:
                    additions.append(("s", s_key))
                additions.extend(
                    ("q", (left, right, word[left], word[right]))
                    for left, right in matching
                    if (left, right, word[left], word[right]) not in B.Q_EDGE
                )
                paths.append(("PS", p_site, s_site, matching, tuple(additions)))
    M.reset_tables()
    return tuple(paths)


PATHS = enumerate_paths()


def audit_minimal_classification():
    distribution = Counter((path[0], len(path[-1])) for path in PATHS)
    expected = Counter({
        ("DQ", 0): 1, ("DQ", 2): 6, ("DQ", 3): 8,
        ("PS", 1): 1, ("PS", 2): 9, ("PS", 3): 30, ("PS", 4): 50,
    })
    require(distribution == expected, ("head02 path census changed", distribution))
    positive_minimum = min(len(path[-1]) for path in PATHS if path[-1])
    minimal = tuple(path for path in PATHS if len(path[-1]) == positive_minimum)
    expected_minimal = (
        "PS", 0, 3, ((1, 2), (4, 5)), (("s", R_KEY),),
    )
    require(positive_minimum == 1, ("head02 minimum cost moved", positive_minimum))
    require(minimal == (expected_minimal,), ("unique head02 mate moved", minimal))
    return distribution, minimal


def audit_symbolic_pure_exit():
    install_symbolic_head02(include_r=True)
    f02 = B.residual(0, 2, P.WORD)
    g12 = B.residual(1, 2, PURE_ONE)
    expected_f02 = B.product_polynomials((
        B.variable("L"), B.variable("b"),
        B.add(
            B.multiply(B.variable("T"), P.J),
            B.multiply(B.variable("P0"), R),
        ),
    ))
    expected_g12 = B.product_polynomials((
        B.variable("P1"), R, B.variable("c"), B.variable("e"),
    ))
    require(f02 == expected_f02, ("head02 complete row changed", f02))
    require(g12 == expected_g12, ("pure head12 exit row changed", g12))

    left = B.subtract(
        B.multiply(B.product_polynomials((B.variable("P1"), B.variable("c"), B.variable("e"))), f02),
        B.multiply(B.product_polynomials((B.variable("P0"), B.variable("L"), B.variable("b"))), g12),
    )
    right = B.product_polynomials((
        B.variable("P1"), B.variable("c"), B.variable("e"),
        B.variable("T"), P.J, B.variable("L"), B.variable("b"),
    ))
    require(left == right, ("head02 pure-exit certificate changed", left, right))

    before_scc = {}
    P.install_symbolic_cycle(include_j=True)
    for row in (C.R0, C.R3):
        before_scc[row] = B.residual(row[1], row[2], row[0])
    B.SECOND[R_KEY] = R
    require(all(B.residual(row[1], row[2], row[0]) == before_scc[row]
                for row in (C.R0, C.R3)),
            "the head02 mate unexpectedly returned to the exact SCC")
    M.reset_tables()
    return {
        "mate": "R=s2(site3,colour1)",
        "mate_operation": "PS",
        "mate_fine": "60|73|12|45",
        "pure_exit": "P1*R*c*e",
        "pure_exit_word_head": "111111:12",
        "pure_exit_operation": "PS",
        "pure_exit_fine": "65|73|02|14",
        "certificate": "P1*c*e*F02-P0*L*b*G12=P1*c*e*T*J*L*b",
    }


EXPECTED_INCREMENTAL = (
    ("001100", "02", -1, 0),
    ("012112", "22", -1, -2),
    ("022122", "22", -1, -2),
    ("111111", "12", -1, -1),
    ("121121", "12", -1, -1),
    ("121122", "02", -2, -2),
    ("201121", "12", -1, -1),
    ("201122", "02", -2, -2),
    ("212112", "22", -1, -1),
    ("222100", "22", -1, -1),
)


def audit_full_replay():
    install_normalized_head02()
    before = {row: B.residual(row[1], row[2], row[0]) for row in F.ROWS}
    B.SECOND[R_KEY] = B.constant(-1)
    after = {row: B.residual(row[1], row[2], row[0]) for row in F.ROWS}
    ledger = tuple(
        ("".join(map(str, row[0])), f"{row[1]}{row[2]}",
         int(change), int(M.P.evaluate(after[row])))
        for row in F.ROWS
        if (change := M.P.evaluate(B.subtract(after[row], before[row])))
    )
    require(ledger == EXPECTED_INCREMENTAL, ("head02 replay changed", ledger))
    require(M.P.evaluate(after[P.F02]) == 0, "R=-1 did not close F02")
    require(M.P.evaluate(after[G12]) == -1, "pure head12 exit stopped firing")
    require(all(M.P.evaluate(after[row]) == 0 for row in (C.R0, C.R3, P.F01)),
            "earlier exact rows reopened under head02 mate")
    final_nonzero = sum(bool(M.P.evaluate(after[row])) for row in F.ROWS)
    require(final_nonzero == 58, ("head02 full residual count moved", final_nonzero))
    M.reset_tables()
    return len(ledger), final_nonzero


def audit_head_escalation_schema():
    return {
        "stage_1": "001100:01 PS -> unique DQ J",
        "stage_2": "001100:02 DQ -> unique PS R",
        "exit": "111111:12 pure-colour-one PS",
        "recurrent_same_word_head_cycle": False,
        "proof": [
            "D*F02-T*F01=-T*P0*S1*L*b",
            "P1*c*e*F02-P0*L*b*G12=P1*c*e*T*J*L*b",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "classification", "symbolic", "replay", "escalation"),
        default="all",
    )
    args = parser.parse_args()

    classification = symbolic = replay = escalation = None
    if args.mode in ("all", "classification"):
        classification = audit_minimal_classification()
    if args.mode in ("all", "symbolic"):
        symbolic = audit_symbolic_pure_exit()
    if args.mode in ("all", "replay"):
        replay = audit_full_replay()
    if args.mode in ("all", "escalation"):
        escalation = audit_head_escalation_schema()

    report = {
        "mode": args.mode,
        "all_operation_paths": len(PATHS),
        "minimum_positive_cost": 1,
        "minimum_mates": 1,
        "symbolic_pure_exit": symbolic,
        "replay": None if replay is None else {
            "incremental_rows": replay[0], "full_nonzero_rows": replay[1]
        },
        "head_escalation": escalation,
        "scope": "same-word head01/head02 chase from exact SCC private face",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 head02 pure-anchor exit gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
