#!/usr/bin/env python3
"""Freeze an exact source lift of a live-factor power on the h branch."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROWS = HERE / "cofactor13_h_branch_rows.jsonl"
OUT = HERE / "certificate_cofactor13_h_branch_live_power.json"
AUDIT = HERE / "results_cofactor13_h_branch_certificate_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    records = [json.loads(line) for line in ROWS.read_text().splitlines()]
    generators = [row["polynomial"] for row in records]
    prints = ";".join(
        f'print("BEGIN_{index}");print(string(L[{index+1},1]));'
        f'print("END_{index}")'
        for index in range(len(records)))
    command = (
        "ring r=0,(b1,d1),dp;"
        "ideal I=" + ",".join(generators) + ";"
        "poly target=(b1+d1)^2;"
        "matrix L=lift(I,ideal(target));"
        "ideal C=matrix(I)*L;"
        'print("BEGIN_CHECK");print(string(C[1]-target));'
        'print("END_CHECK");' + prints + ";quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               capture_output=True, text=True, timeout=120,
                               check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular lift failed: " + completed.stderr[-1000:])
    require("BEGIN_CHECK\n0\nEND_CHECK" in completed.stdout,
            "lift did not replay exactly")
    coefficients = []
    for index in range(len(records)):
        begin = f"BEGIN_{index}\n"
        end = f"\nEND_{index}"
        require(begin in completed.stdout,
                f"missing coefficient begin marker {index}")
        tail = completed.stdout.split(begin, 1)[1]
        require(end in tail, f"missing coefficient end marker {index}")
        coefficients.append(tail.split(end, 1)[0].strip())
    nonzero = [index for index, coefficient in enumerate(coefficients)
               if coefficient != "0"]
    require(nonzero, "empty lift")
    certificate = {
        "status": "UNAUDITED exact-Q source lift",
        "ring": "Q[b1,d1]",
        "identity": "sum_i multiplier_i*row_i=(b1+d1)^2",
        "target": "(b1+d1)^2",
        "target_is_declared_live": True,
        "generators": [
            {**row, "multiplier": coefficient}
            for row, coefficient in zip(records, coefficients)
            if coefficient != "0"
        ],
        "source_row_count": len(records),
        "nonzero_source_row_count": len(nonzero),
        "nonzero_source_indices": nonzero,
        "scope": (
            "Together with the exact h/Q branch reduction and declared "
            "b1+d1 localization, this identity closes the h branch only."
        ),
    }
    logical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    certificate["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")

    # Independent replay in a fresh Singular invocation from the frozen
    # coefficient ledger, plus a sign mutation must-fire.
    active = certificate["generators"]
    replay = "+".join(
        f"({entry['multiplier']})*({entry['polynomial']})"
        for entry in active)
    mutated = list(active)
    mutation_index = 0
    mutation_replay = "+".join(
        f"({'-(' + entry['multiplier'] + ')' if index == mutation_index else entry['multiplier']})"
        f"*({entry['polynomial']})"
        for index, entry in enumerate(mutated)
    )
    audit_command = (
        "ring r=0,(b1,d1),dp;"
        f"poly residue=({replay})-(b1+d1)^2;"
        f"poly mutation=({mutation_replay})-(b1+d1)^2;"
        'print("RESIDUE");print(string(residue));'
        'print("MUTATION_ZERO");print(mutation==0);quit;'
    )
    audit_run = subprocess.run(["Singular", "-q", "-c", audit_command],
                               capture_output=True, text=True, timeout=120,
                               check=False)
    require(audit_run.returncode == 0 and not audit_run.stderr.strip()
            and "RESIDUE\n0\nMUTATION_ZERO\n0" in audit_run.stdout,
            "frozen certificate replay or mutation failed")
    audit = {
        "status": "UNAUDITED independent frozen-ledger replay PASS",
        "certificate_file_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "certificate_logical_sha256": certificate["result_sha256"],
        "exact_residual": 0,
        "sign_mutation_is_zero": False,
        "nonzero_source_labels": [entry["source_label"] for entry in active],
    }
    audit_logical = json.dumps(audit, sort_keys=True, separators=(",", ":"))
    audit["result_sha256"] = sha256(audit_logical.encode()).hexdigest()
    AUDIT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print("Cof13 h-branch exact live-power certificate: PASS")
    print("nonzero rows:", len(nonzero), audit["nonzero_source_labels"])
    print("certificate logical sha256:", certificate["result_sha256"])
    print("audit logical sha256:", audit["result_sha256"])


if __name__ == "__main__":
    main()
