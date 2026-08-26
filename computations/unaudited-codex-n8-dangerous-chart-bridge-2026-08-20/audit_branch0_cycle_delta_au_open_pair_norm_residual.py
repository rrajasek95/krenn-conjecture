#!/usr/bin/env python3
"""Freeze the two-prime pair-norm residual for the Au-open Delta chart.

This checker validates the six independently exported non-live factors and
their irreducibility over F_1009/F_1013.  Their source derivation is the
literal quotient-resultant probe named below.  The conclusion is modular
discovery only: the full three-minor parameter projection is confined to the
finite triple intersection of factors of degrees 348, 340, and 351.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_delta_au_open_pair_norm_residual.json"
PAIRS = ("LR", "LT", "RT")
EXPECTED = {
    1009: {"LR": (21851, 348), "LT": (20820, 340),
           "RT": (21699, 351)},
    1013: {"LR": (21853, 348), "LT": (20821, 340),
           "RT": (21692, 351)},
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def check_factor(prime, pair):
    path = HERE / f"branch0_cycle_delta_au_open_norm_{pair}_p{prime}.factor"
    value = path.read_text().strip()
    terms, degree = EXPECTED[prime][pair]
    program = (
        f"ring R={prime},(d1,x),dp;poly f={value};"
        "list L=factorize(f);"
        'print("BEGIN");print(size(f));print(deg(f));print(size(L[1]));'
        "print(size(L[1][1]));print(size(L[1][2]));"
        "print(L[2][1]);print(L[2][2]);print(L[1][2]-f);"
        'print("END");quit;'
    )
    completed = subprocess.run(
        ["Singular", "-q", "--no-warn"], input=program, text=True,
        capture_output=True, timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"p{prime} {pair}: Singular failed")
    expected = f"BEGIN\n{terms}\n{degree}\n2\n1\n{terms}\n1\n1\n0\nEND"
    require(expected in completed.stdout,
            f"p{prime} {pair}: factor profile/irreducibility changed")
    return {
        "pair": pair,
        "path": path.name,
        "file_sha256": sha256(path.read_bytes()).hexdigest(),
        "terms": terms,
        "total_degree": degree,
        "irreducible": True,
        "multiplicity": 1,
    }


def main():
    records = {str(prime): [check_factor(prime, pair) for pair in PAIRS]
               for prime in sorted(EXPECTED)}
    result = {
        "status": "UNAUDITED modular pair-norm residual; not a Q theorem",
        "source_probe": "probe_branch0_cycle_delta_au_open_resultant.py",
        "minor_pairs": {
            "LR": [[2, 3, 4, 5], [0, 2, 3, 4]],
            "LT": [[2, 3, 4, 5], [1, 2, 3, 4]],
            "RT": [[0, 2, 3, 4], [1, 2, 3, 4]],
        },
        "norm_definition": (
            "For each pair, rho=NF_Q(Res_b1(minor_i,minor_j))="
            "rho1*b0+rho0 and N=num(x^2*A*rho0^2+C*rho1^2)."),
        "profiles": records,
        "common_live_factor_profiles": {
            "LR": "numerator unit*(x-1)*C^6*F348; denominator A^4",
            "LT": "numerator unit*(x-1)*C^6*F340; denominator A^4",
            "RT": "numerator unit*(x-1)*C^7*F351; denominator A^6",
        },
        "scope": (
            "On the declared A,x-1,C-open chart, a solution of the three "
            "minors must project into F348=F340=F351=0. Distinct "
            "irreducible degrees show there is no curve component at either "
            "prime; only a finite modular intersection remains. This is "
            "not a characteristic-zero emptiness theorem. The guarded "
            "three-minor msolve saturation completed with 193 basis rows, "
            "but elimination and the direct norm-triple bases timed out, "
            "so they contribute no further claim."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Au-open pair-norm residual: PASS")
    print("degrees:", [EXPECTED[1009][pair][1] for pair in PAIRS])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
