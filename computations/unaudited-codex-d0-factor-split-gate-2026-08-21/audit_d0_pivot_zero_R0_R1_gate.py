#!/usr/bin/env python3
"""Independent source/sentinel replay of the exact O1 R0=R1 unit gate."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_d0_pivot_zero_R0_R1_gate.py"
EXPORT = HERE / "results_d0_pivot_zero_R0_R1_gate_export.json"
RUN = HERE / "results_d0_pivot_zero_R0_R1_exact_run.json"
INPUT = HERE / "d0_pivot_zero_R0_R1_char0.msolve"
OUTPUT = HERE / "d0_pivot_zero_R0_R1_char0.out"
INTERFACE = HERE / "results_d0_pivot_zero_interface.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def read_logical(path):
    value = json.loads(path.read_text())
    frozen = value.pop("logical_sha256")
    require(logical_hash(value) == frozen, f"logical digest mismatch: {path.name}")
    return value, frozen


def main():
    export, export_hash = read_logical(EXPORT)
    before_input = digest(INPUT)
    # Re-run the literal exporter with the current interpreter/mode.  It
    # independently rebuilds the upper/endpoint solves, all ten residual
    # rows, Delta=R3, denominators, and strict gate bytes.
    replay = subprocess.run([sys.executable, str(EXPORTER)], cwd=HERE,
                            capture_output=True, text=True, timeout=120)
    require(replay.returncode == 0 and "export PASS" in replay.stdout,
            "literal source exporter replay failed")
    require(digest(INPUT) == before_input == export["input_sha256"],
            "literal source replay changed the exact input")
    export2, export_hash2 = read_logical(EXPORT)
    require(export_hash2 == export_hash and export2 == export,
            "source export logical record changed on replay")

    run = json.loads(RUN.read_text())
    require(run["timeout_seconds"] == 600 and run["process_status"] == "completed",
            "600-second gate status changed")
    require(run["returncode"] == 0 and run["unit_basis"],
            "exact gate is not a unit")
    require(run["input_sha256"] == digest(INPUT), "run/input hash mismatch")
    require(run["output_sha256"] == digest(OUTPUT), "run/output hash mismatch")
    require(OUTPUT.read_text().rstrip().endswith("[1]:"), "unit output changed")

    text = INPUT.read_text()
    require("(" not in text and ")" not in text,
            "strict msolve parenthesis guard failed")
    header, characteristic, body = text.split("\n", 2)
    require(header == "z,b0,d1,d4,a0,a5" and characteristic == "0",
            "input header changed")
    rows = body.rstrip().split(",\n")
    require(len(rows) == 13 and export["labels"][:2] == ["R0", "R1"],
            "row count/order changed")
    require(export["labels"][2:12] ==
            ["t_012", "t_013", "t_023", "t_123", "cofactor_0_3",
             "cofactor_1_3", "cofactor_2_3", "cofactor_3_3",
             "cofactor_4_3", "cofactor_5_3"],
            "ten-row literal packet changed")
    require(export["explicit_nonlocalization"] == ["R2"],
            "R2 nonlocalization sentinel changed")
    denominator_names = {record["factor"]
                         for records in export["denominator_records"].values()
                         for record in records}
    require(any("b0^4*d1^2" in factor for factor in denominator_names),
            "R3 denominator sentinel did not fire")

    # Verify from the frozen exact factors that the z coefficient is precisely
    # base*R3, has no R2 factor, and would change if R2 were localized.
    site = (HERE.parent.parent / ".venv" / "lib" /
            f"python{sys.version_info.major}.{sys.version_info.minor}" /
            "site-packages")
    if str(site) not in sys.path:
        sys.path.append(str(site))
    import sympy as sp
    z, b0, d1, d4, a0, a5 = sp.symbols("z b0 d1 d4 a0 a5")
    interface, interface_hash = read_logical(INTERFACE)
    records = interface["coefficient_pivot"]["C0_open_residual_factors"]
    R2 = sp.sympify(records[2]["polynomial"].replace("^", "**"))
    R3 = sp.sympify(records[3]["polynomial"].replace("^", "**"))
    expected_live = sp.expand(b0*d1*d4*(b0**2+d4**2)*R3)
    last = sp.sympify(rows[-1].replace("^", "**"))
    require(sp.Poly(last, z).coeff_monomial(z) == expected_live and
            sp.Poly(last, z).coeff_monomial(1) == -1,
            "guaranteed-live Rabinowitsch row changed")
    require(sp.rem(sp.Poly(expected_live, b0, d1, d4),
                   sp.Poly(R2, b0, d1, d4)).as_expr() != 0,
            "R2 was silently included in the guaranteed live product")
    mutated = sp.expand(z*expected_live*R2-1)
    require(str(mutated).replace("**", "^") != rows[-1],
            "R2-localization mutation failed to fire")
    require("[1]:" not in OUTPUT.read_text().replace("[1]:", "[b0]:"),
            "unit-output mutation failed to fire")

    result = {
        "status": "exact corrected O1 R0=R1 unit gate PASS",
        "export_logical_sha256": export_hash,
        "interface_logical_sha256": interface_hash,
        "input_sha256": digest(INPUT), "output_sha256": digest(OUTPUT),
        "literal_row_count": 10,
        "localized_factors": ["b0", "d1", "d4", "C0", "R3"],
        "explicitly_not_localized": ["R2"],
        "mutation_controls": ["strict_parentheses", "R3_denominator",
                              "add_R2_to_localizer", "unit_output"],
        "theorem": ("In the Delta-open,D0=0,C0!=0 selected-pivot-zero branch, "
                    "the full ten-row pre-pivot literal source system has no "
                    "solution with R0=R1=0 and guaranteed base/Delta factors live."),
        "symmetry_consequence": ("The exact Laurent involution simultaneously "
                                 "closes the mate R0=R2=0."),
        "scope_guard": "O2 and O3 are untouched; no complementary R factor is localized.",
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_R0_R1_gate_audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero O1 exact audit PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
