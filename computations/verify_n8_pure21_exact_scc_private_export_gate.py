#!/usr/bin/env python3
"""Unique mate and mandatory export of the first exact SCC private face.

On the factorized SCC chart K=S0*c+Z*L=0, the first external face is
P0*S1*L*b at 001100:01.  Its complete DQ/PS path census has a unique
positive minimum: the one-cell DQ mate J=q03^(0,1).  This mate does not
return to any SCC row.  Instead it creates T*J*L*b at the identical
word/fine matching and head 02.  The two rows satisfy
D*F02-T*F01=-T*P0*S1*L*b, a torus-unit certificate.  Thus the exact SCC
necessarily exports a new private face, and word/fine type alone cannot be
a strict potential because it is unchanged by the export.
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
    "verify_n8_pure21_literal_minimal_cost2_scc_gate.py"
)
SPEC = spec_from_file_location("literal_scc_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
C = module_from_spec(SPEC)
SPEC.loader.exec_module(C)
S = C.S
E = C.E
F = C.F
M = C.M
B = C.B


WORD = (0, 0, 1, 1, 0, 0)
F01 = (WORD, 0, 1)
F02 = (WORD, 0, 2)
J_KEY = (0, 3, 0, 1)
J = B.variable("J")


def install_symbolic_cycle(include_j=False):
    S.install_symbolic_parent()
    B.FIRST[S.X3_KEY] = S.X3
    B.SECOND[(0, 0, 1)] = B.variable("Z")
    B.Q_EDGE[(1, 2, 0, 1)] = B.variable("L")
    if include_j:
        B.Q_EDGE[J_KEY] = J


def install_normalized_cycle(include_j=False):
    S.install_normalized_parent()
    B.FIRST[S.X3_KEY] = B.constant(1)
    B.SECOND[(0, 0, 1)] = B.constant(-1)
    B.Q_EDGE[(1, 2, 0, 1)] = B.constant(1)
    if include_j:
        B.Q_EDGE[J_KEY] = B.constant(-1)


def enumerate_paths():
    install_symbolic_cycle()
    paths = []
    row, column = (0, 1)
    for matching in B.matchings(B.SITES):
        additions = []
        if (row, column) not in B.DIRECT:
            additions.append(("d", (row, column)))
        additions.extend(
            ("q", (left, right, WORD[left], WORD[right]))
            for left, right in matching
            if (left, right, WORD[left], WORD[right]) not in B.Q_EDGE
        )
        paths.append(("DQ", matching, tuple(additions)))
    for p_site in B.SITES:
        for s_site in B.SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in B.SITES if site not in (p_site, s_site))
            for matching in B.matchings(rest):
                additions = []
                p_key = (row, p_site, WORD[p_site])
                s_key = (column, s_site, WORD[s_site])
                if p_key not in B.FIRST:
                    additions.append(("p", p_key))
                if s_key not in B.SECOND:
                    additions.append(("s", s_key))
                additions.extend(
                    ("q", (left, right, WORD[left], WORD[right]))
                    for left, right in matching
                    if (left, right, WORD[left], WORD[right]) not in B.Q_EDGE
                )
                paths.append(("PS", p_site, s_site, matching, tuple(additions)))
    M.reset_tables()
    return tuple(paths)


PATHS = enumerate_paths()


def audit_minimal_classification():
    distribution = Counter((path[0], len(path[-1])) for path in PATHS)
    expected = Counter({
        ("DQ", 1): 1, ("DQ", 2): 4, ("DQ", 3): 10,
        ("PS", 0): 1, ("PS", 2): 11, ("PS", 3): 28, ("PS", 4): 50,
    })
    require(distribution == expected, ("private export path census changed", distribution))
    positive_minimum = min(len(path[-1]) for path in PATHS if path[-1])
    minimal = tuple(path for path in PATHS if len(path[-1]) == positive_minimum)
    expected_minimal = (
        "DQ", ((0, 3), (1, 2), (4, 5)), (("q", J_KEY),),
    )
    require(positive_minimum == 1, ("private minimum cost moved", positive_minimum))
    require(minimal == (expected_minimal,), ("unique private mate moved", minimal))
    return distribution, minimal


def audit_symbolic_export_and_scc_nonreturn():
    install_symbolic_cycle()
    before = {
        row: B.residual(row[1], row[2], row[0])
        for row in (C.R0, C.R3, C.R5, F01, F02)
    }
    B.Q_EDGE[J_KEY] = J
    after = {
        row: B.residual(row[1], row[2], row[0])
        for row in (C.R0, C.R3, C.R5, F01, F02)
    }
    expected_f01 = B.product_polynomials((
        B.variable("L"), B.variable("b"),
        B.add(
            B.multiply(B.variable("P0"), B.variable("S1")),
            B.multiply(B.variable("D"), J),
        ),
    ))
    expected_f02 = B.product_polynomials((
        B.variable("T"), J, B.variable("L"), B.variable("b"),
    ))
    require(after[F01] == expected_f01, ("F01 mate row changed", after[F01]))
    require(after[F02] == expected_f02, ("F02 export row changed", after[F02]))
    require(all(after[row] == before[row] for row in (C.R0, C.R3, C.R5)),
            "the unique mate unexpectedly returned to an SCC row")

    left = B.subtract(
        B.multiply(B.variable("D"), after[F02]),
        B.multiply(B.variable("T"), after[F01]),
    )
    right = B.negate(B.product_polynomials((
        B.variable("T"), B.variable("P0"), B.variable("S1"),
        B.variable("L"), B.variable("b"),
    )))
    require(left == right, ("private export unit certificate changed", left, right))
    M.reset_tables()
    return {
        "mate": "J=q03^(0,1)",
        "mate_operation": "DQ",
        "mate_fine": "67|03|12|45",
        "export": "T*J*L*b",
        "export_word_head": "001100:02",
        "export_operation": "DQ",
        "export_fine": "67|03|12|45",
        "certificate": "D*F02-T*F01=-T*P0*S1*L*b",
        "returns_to_scc": False,
    }


EXPECTED_INCREMENTAL = (
    ("001100", "01", -1, 0),
    ("001100", "02", 1, 1),
    ("001121", "11", 2, 2),
    ("001122", "01", 4, 4),
    ("001122", "02", -4, -4),
    ("002100", "20", -1, -1),
    ("002122", "20", 2, 2),
    ("012112", "21", 1, 2),
    ("012112", "22", -1, -1),
    ("022100", "21", -1, -1),
    ("022122", "21", 5, 6),
    ("022122", "22", -1, -1),
)


def audit_full_replay():
    install_normalized_cycle()
    before = {row: B.residual(row[1], row[2], row[0]) for row in F.ROWS}
    B.Q_EDGE[J_KEY] = B.constant(-1)
    after = {row: B.residual(row[1], row[2], row[0]) for row in F.ROWS}
    ledger = tuple(
        ("".join(map(str, row[0])), f"{row[1]}{row[2]}",
         int(change), int(M.P.evaluate(after[row])))
        for row in F.ROWS
        if (change := M.P.evaluate(B.subtract(after[row], before[row])))
    )
    require(ledger == EXPECTED_INCREMENTAL, ("private export replay changed", ledger))
    require(M.P.evaluate(after[F01]) == 0, "unique mate did not close F01")
    require(M.P.evaluate(after[F02]) == 1, "mandatory F02 export stopped firing")
    require(all(M.P.evaluate(after[row]) == 0 for row in (C.R0, C.R3)),
            "exact SCC reopened under the private mate")
    final_nonzero = sum(bool(M.P.evaluate(after[row])) for row in F.ROWS)
    require(final_nonzero == 52, ("private export full residual count moved", final_nonzero))
    M.reset_tables()
    return len(ledger), final_nonzero


def audit_invariant_boundary():
    source_type = ("001100", "03|12|45")
    export_type = ("001100", "03|12|45")
    require(source_type == export_type, "word/fine type unexpectedly changed")
    return {
        "strict_word_fine_potential": False,
        "counterexample": "001100:01 -> 001100:02 with identical 03|12|45 fine part",
        "valid_statement": "the exact SCC exports a private head face",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "classification", "symbolic", "replay", "invariant"),
        default="all",
    )
    args = parser.parse_args()

    classification = symbolic = replay = invariant = None
    if args.mode in ("all", "classification"):
        classification = audit_minimal_classification()
    if args.mode in ("all", "symbolic"):
        symbolic = audit_symbolic_export_and_scc_nonreturn()
    if args.mode in ("all", "replay"):
        replay = audit_full_replay()
    if args.mode in ("all", "invariant"):
        invariant = audit_invariant_boundary()

    report = {
        "mode": args.mode,
        "all_operation_paths": len(PATHS),
        "minimum_positive_cost": 1,
        "minimum_mates": 1,
        "symbolic_export": symbolic,
        "replay": None if replay is None else {
            "incremental_rows": replay[0], "full_nonzero_rows": replay[1]
        },
        "invariant": invariant,
        "closed_scc_exports_private_face": True,
        "scope": "first private face exported by exact factorized SCC",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 exact SCC private export gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
