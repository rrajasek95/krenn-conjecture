#!/usr/bin/env python3
"""Referee the sound exact K4 leaf exports and char0 sentinels."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
EXPORT_RESULT = HERE / "results_branch0_cycle_generic_codim5_k4_leaf_export.json"
K5_INPUT = HERE / "branch0_cycle_generic_codim5_d10_k4_k5_exact.msolve"
N14_INPUT = HERE / "branch0_cycle_generic_codim5_d10_k4_n14_off_k5_exact.msolve"
K5_PREFIX = HERE / "results_branch0_cycle_generic_codim5_d10_k4_k5_exact"
N14_PREFIX = HERE / "results_branch0_cycle_generic_codim5_d10_k4_n14_off_k5_exact"
RESULT = HERE / "results_branch0_cycle_generic_codim5_k4_leaf_exact_audit.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text().splitlines()
    require(lines[1] == "0", f"{path.name} is not characteristic zero")
    body = "\n".join(lines[2:]).strip()
    require("(" not in body and "**" not in body,
            f"{path.name} is not strict canonical syntax")
    return lines[0].split(","), body.split(",\n")


def main() -> None:
    export = json.loads(EXPORT_RESULT.read_text())
    require(export["source_sha256"] == file_sha(SOURCE)
            and export["K5_input_sha256"] == file_sha(K5_INPUT)
            and export["N14_off_K5_input_sha256"] == file_sha(N14_INPUT),
            "export source/input hashes changed")
    require(export["source_row_count"] == 9
            and export["source_row_labels"]
            == ["P851", "P1342", "P324", "P1846", "Q4098",
                "R4885", "S4331", "T4750", "U3217"]
            and len(export["row_records"]) == 9,
            "nine-row source coverage changed")

    k5_variables, k5_rows = rows(K5_INPUT)
    n14_variables, n14_rows = rows(N14_INPUT)
    require(k5_variables == ["b0", "b1", "d1", "d4", "z"]
            and n14_variables == k5_variables,
            "leaf variable order changed")
    require(len(k5_rows) == 11 and len(n14_rows) == 12,
            "leaf gate row counts changed")
    # Rows 0..8 are the exact images of all original retained rows.  The
    # exporter records both pre-reduction and leaf-reduced hashes for each.
    require(all(record["mapped_raw_sha256"]
                and record["mapped_mod_K5_sha256"]
                for record in export["row_records"]),
            "mapped retained-row audit record missing")

    b0, b1, d1, d3, d4 = sp.symbols("b0 b1 d1 d3 d4")
    bplus = b1+d1
    d10 = (b0**2*b1*d1*d4 + 2*b0**2*b1*d3
           - b0**2*d1**2*d4 - b0*b1*d1*d4 + b0*b1*d3*d4
           - b0*d1**2*d4 - b0*d1*d3*d4 + 2*b1*d1*d4**2
           + b1*d3*d4 + d1*d3*d4)
    k4_leading = b0*(b0+d4)
    k4_constant = d1*d4*(b0**2+d4)
    k4 = sp.expand(k4_leading*d3+k4_constant)
    k5 = b0**4+b0**3+2*b0**2*d4-b0*d4**2+d4**2
    d10_poly = sp.Poly(d10, d3)
    cleared_d10 = sp.expand(
        d10_poly.coeff_monomial(1)*k4_leading
        - d10_poly.coeff_monomial(d3)*k4_constant)
    require(sp.expand(cleared_d10+d1*d4*bplus*k5) == 0,
            "exact D10/K4/K5 identity changed")
    exceptional_k4 = sp.factor(k4.subs(d4, -b0))
    exceptional_d10 = sp.factor(d10.subs({b0: 1, d4: -1}))
    require(exceptional_k4 == -b0**2*d1*(b0-1)
            and exceptional_d10 == 2*d1*bplus,
            "K4 pivot companion proof changed")

    k5_manifest = json.loads(Path(str(K5_PREFIX)+".manifest.json").read_text())
    n14_manifest = json.loads(Path(str(N14_PREFIX)+".manifest.json").read_text())
    require(k5_manifest["input"]["sha256"] == file_sha(K5_INPUT)
            and n14_manifest["input"]["sha256"] == file_sha(N14_INPUT),
            "runner input hashes changed")
    require(k5_manifest["status"]
            == "completed_characteristic_zero_parametrization"
            and k5_manifest["solution"]
            == {"degree": None, "kind": "positive_dimensional",
                "variable_count": 5}
            and Path(str(K5_PREFIX)+".param.out").read_text()
            == "[1, 5, -1, []]:\n",
            "K5 exact positive-dimensional sentinel changed")
    require(n14_manifest["status"]
            == "completed_characteristic_zero_parametrization"
            and n14_manifest["solution"]
            == {"degree": 0, "kind": "empty", "variable_count": 5}
            and Path(str(N14_PREFIX)+".param.out").read_text() == "[-1]:\n",
            "N14-off-K5 exact unit changed")

    result = {
        "status": "UNAUDITED exact-Q K4 leaf theorem/blocker referee",
        "source_sha256": file_sha(SOURCE),
        "export_result_sha256": export["result_sha256"],
        "structural_theorem": (
            "On K4=0 with b0,d1,d4,Bplus live, D10=0 forces K5=0. "
            "The N14 branch away from K5 and the b0+d4=0 pivot companion "
            "are empty over Q."),
        "K5_status": "exact msolve positive-dimensional sentinel",
        "K5_literal_output": "[1, 5, -1, []]:",
        "K5_runner_logical_sha256": k5_manifest["logical_sha256"],
        "K5_elapsed_seconds": k5_manifest["elapsed_seconds"],
        "N14_off_K5_status": "exact-Q UNIT",
        "N14_literal_output": "[-1]:",
        "N14_runner_logical_sha256": n14_manifest["logical_sha256"],
        "N14_elapsed_seconds": n14_manifest["elapsed_seconds"],
        "blocker": (
            "The only possible K4 leaf is K5, but the exact nine-row "
            "reduced interface remains positive-dimensional. Closing K4 "
            "requires an additional literal/source or Hcore restriction, "
            "not another N14 split."),
        "scope": (
            "Reduced nine-row A/B-open interface after the already-audited "
            "b3 pivot and the sound K4 d3 solve. This is not a claim that "
            "the K5 family satisfies any omitted source/Hcore equation."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("exact K4 leaf theorem/blocker referee: PASS")
    print("K5: positive-dimensional; N14-off-K5: UNIT")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
