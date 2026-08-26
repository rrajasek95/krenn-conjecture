#!/usr/bin/env python3
"""Exact unit computations for the six branch-0 strata of size at most three.

Fix the off-diagonal permanent parametrization

    M_e = [[a_e,b_e],[-(1+a_e*d_e)/b_e,d_e]].

Thus ``1 + permanent(M_e)`` vanishes identically.  The six ``b_e`` are
localized.  Outside a chosen edge support S set ``d_e=0``; on S localize
``a_e*d_e``, so both permanent terms are live.  We also localize the pure
Hafnian.  This script derives the remaining branch-0 packet rows literally
from the 24-cell source and proves that all six S4 support-orbit
representatives of size at most three give the unit ideal over Q.

Every support of size at least four is deliberately absent: those cases
remain unresolved and earlier bounded Groebner runs timed out.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import sysconfig

PURELIB = sysconfig.get_paths().get("purelib")
VENV_PURELIB = (Path(sys.executable).parent.parent / "lib" /
                f"python{sys.version_info.major}.{sys.version_info.minor}" /
                "site-packages")
for package_path in (PURELIB, str(VENV_PURELIB)):
    if package_path and package_path not in sys.path:
        sys.path.append(package_path)
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCREEN_PATH = (ROOT / "computations" /
               "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
               "screen_lowq_joint_branch_orbits.py")
OUT = HERE / "results_branch0_both_live_easy_strata.json"
EDGE_ORDER = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EASY_REPRESENTATIVES = (
    ("one_edge", (0,), True),
    ("two_adjacent", (0, 1), True),
    ("two_disjoint", (0, 5), True),
    ("three_star", (0, 1, 2), True),
    # The exact unit basis is quick, but a direct source lift is much larger
    # and currently exceeds the bounded replay time.  Keep this distinction
    # explicit instead of silently treating a timeout as a certificate.
    ("three_path", (0, 3, 5), False),
    ("three_triangle", (0, 1, 3), False),
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SCREEN = load("root_branch0_both_live_screen", SCREEN_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def evaluate(raw_poly, entries):
    answer = 0
    for monomial, coefficient in raw_poly.items():
        term = sp.Integer(coefficient)
        for variable in monomial:
            term *= entries[variable]
        answer += term
    return sp.cancel(answer)


def numerator(expression, variables):
    result = sp.together(expression).as_numer_denom()[0]
    return sp.Poly(sp.expand(result), *variables).as_expr()


def singular(expression):
    return str(expression).replace("**", "^")


def derive(support):
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    d_all = sp.symbols("d0:6")
    entries = []
    for edge in range(6):
        d_value = d_all[edge] if edge in support else sp.Integer(0)
        entries.extend((a[edge], b[edge],
                        -(1 + a[edge] * d_value) / b[edge], d_value))
    variables = a + b + tuple(d_all[edge] for edge in support)
    raw_rows, raw_h = SCREEN.PROBE.equations(SCREEN.branch_bits(0))
    raw_labels = ([f"e_{left}{right}" for left, right in EDGE_ORDER]
                  + ["t_012", "t_013", "t_023", "t_123"]
                  + [f"cofactor_{edge}_{position}"
                     for edge in range(6) for position in (0, 3)])
    require(len(raw_rows) == len(raw_labels) == 22,
            "branch-0 raw row count changed")
    rows = []
    seen = set()
    for label, raw in zip(raw_labels, raw_rows):
        value = numerator(evaluate(raw, entries), variables)
        if value == 0:
            continue
        encoded = singular(value)
        if encoded in seen:
            continue
        seen.add(encoded)
        rows.append((label, value, encoded))
    h_value = numerator(evaluate(raw_h, entries), variables)
    return variables, rows, h_value


def exact_unit(name, support, require_source_lift):
    variables, rows, h_value = derive(support)
    ring_variables = list(map(str, variables)) + ["u", "z", "w"]
    b_product = "*".join(f"b{edge}" for edge in range(6))
    both_product = "*".join(f"a{edge}*d{edge}" for edge in support)
    generators = [encoded for _, _, encoded in rows]
    generators += [f"u*({singular(h_value)})-1",
                   f"z*{b_product}-1", f"w*{both_product}-1"]
    prefix = (f"ring R=0,({','.join(ring_variables)}),dp;"
              f"ideal I={','.join(generators)};")
    if require_source_lift:
        program = (
            prefix
            + "matrix L;ideal G=liftstd(I,L);"
            + 'print("BEGIN_STATUS");print(size(G));print(string(G[1]));'
              'print(dim(G));print("END_STATUS");'
            + "matrix C=matrix(I)*L;"
            + 'print("BEGIN_CHECK");print(string(C[1,1]));'
              'print("END_CHECK");'
            + "for(int i=1;i<=nrows(L);i++){if(L[i,1]!=0){"
              'print("BEGIN_MULT");print(i);print(string(L[i,1]));'
              'print("END_MULT");}};quit;'
        )
    else:
        program = (
            prefix
            + "ideal G=slimgb(I);poly q=reduce(1,G);"
            + 'print("BEGIN_STATUS");print(string(q));print(size(G));'
              'print(dim(G));print("END_STATUS");quit;'
        )
    completed = subprocess.run(["Singular", "-q", "-c", program],
                               text=True, capture_output=True,
                               timeout=180 if require_source_lift else 120,
                               check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"{name}: Singular failed: {completed.stderr[-500:]}")
    lines = [line.strip() for line in completed.stdout.splitlines()]
    begin = lines.index("BEGIN_STATUS")
    end = lines.index("END_STATUS")
    status_body = lines[begin + 1:end]
    if require_source_lift:
        require(len(status_body) == 3 and status_body[0] == "1"
                and status_body[1] not in ("", "0")
                and status_body[2] == "-1",
                f"{name}: expected nonzero-constant unit basis, got "
                f"{status_body}")
        target_constant = status_body[1]
    else:
        require(status_body == ["0", "1", "-1"],
                f"{name}: expected exact unit reduction, got {status_body}")
        return {
            "name": name,
            "support_edge_indices": list(support),
            "support_edges": [list(EDGE_ORDER[index]) for index in support],
            "specialized_distinct_row_count": len(rows),
            "specialized_row_labels": [label for label, _, _ in rows],
            "exact_unit_basis_over_Q": True,
            "source_lift_status": "not frozen; bounded direct lift timed out",
        }
    begin_check = lines.index("BEGIN_CHECK")
    end_check = lines.index("END_CHECK")
    require("".join(lines[begin_check + 1:end_check]) == target_constant,
            f"{name}: exact lift did not replay to its unit constant")
    multipliers = []
    cursor = 0
    labels = [label for label, _, _ in rows] + [
        "H_localizer", "b_product_localizer", "both_term_localizer"]
    while "BEGIN_MULT" in lines[cursor:]:
        begin_mult = lines.index("BEGIN_MULT", cursor)
        end_mult = lines.index("END_MULT", begin_mult)
        index = int(lines[begin_mult + 1]) - 1
        text = "".join(lines[begin_mult + 2:end_mult])
        require(text and text != "0", f"{name}: zero multiplier serialized")
        multipliers.append({"label": labels[index], "polynomial": text})
        cursor = end_mult + 1
    require(multipliers, f"{name}: empty exact lift")
    ledger = json.dumps(multipliers, sort_keys=True, separators=(",", ":"))
    return {
        "name": name,
        "support_edge_indices": list(support),
        "support_edges": [list(EDGE_ORDER[index]) for index in support],
        "specialized_distinct_row_count": len(rows),
        "specialized_row_labels": [label for label, _, _ in rows],
        "nonzero_lift_multiplier_count": len(multipliers),
        "used_generator_labels": [record["label"] for record in multipliers],
        "multiplier_ledger_sha256": sha256(ledger.encode("ascii")).hexdigest(),
        "exact_lift_target_constant": target_constant,
        "exact_lift_replays_to_nonzero_constant": True,
    }


def main():
    records = [exact_unit(name, support, require_source_lift)
               for name, support, require_source_lift
               in EASY_REPRESENTATIVES]
    result = {
        "status": "UNAUDITED exact easy both-live defect-stratum units",
        "branch_mask": 0,
        "edge_order": [list(edge) for edge in EDGE_ORDER],
        "substitution": "M_e=[[a_e,b_e],[-(1+a_e*d_e)/b_e,d_e]]",
        "localized": (
            "pure H, product of all b_e, and product of a_e*d_e on the "
            "displayed support; c_e and 1+a_e*d_e are not localized"
        ),
        "records": records,
        "proved_support_orbit_count": len(records),
        "unresolved_support_orbits": [
            {"name": "all supports of size at least four"},
        ],
        "scope": (
            "These six exact unit computations exclude every both-live "
            "support stratum of size at most three.  Four include source "
            "lifts; the three-path and three-triangle cases currently have "
            "exact-Q unit bases but no frozen lifts.  They do not settle "
            "size>=4, other cofactor branches, or the full diagonal packet."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 easy both-live strata: PASS")
    print("supports / lift sizes:", [
        (record["support_edge_indices"],
         record.get("nonzero_lift_multiplier_count", "basis-only"))
        for record in records])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
