#!/usr/bin/env python3
"""Replay the two support-28 orbit-exhaustion RUP certificates.

Structural mode is stdlib-only and pins/reconstructs every input.  Proof mode
additionally requires the repository PySAT environment and checks every
deletion-free RUP addition through the empty clause.
"""

from __future__ import annotations

import argparse
import gzip
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "computations"
CERTIFICATES = HERE / "certificates"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_generator():
    path = HERE / "generate_n8_full_support_affine_guard_certificate.py"
    spec = spec_from_file_location("n8_affine_guard_generator", path)
    require(spec is not None and spec.loader is not None, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


G = load_generator()


CASES = {
    "12": {
        "target": (1, 2),
        "stem": "n8_full_support_affine_guard_exhaustion",
        "cnf_sha256":
            "0ccfe9546726557bf3bda33c99ebcde331f5f99b714c3e8ed0eb95f37eba9205",
        "proof_raw_sha256":
            "558f8d3cb85ddd530ea386ee5f475fc258d20c4b980b6e462d71cd612a4cfab4",
        "proof_gzip_sha256":
            "fd2d4cdffa1221daa399187368116a5ee876632ab1416abf9576438c0f6f7f5b",
        "proof_additions": 140722,
    },
    "012": {
        "target": (0, 1, 2),
        "stem": "n8_full_support_affine_guard_target012_exhaustion",
        "cnf_sha256":
            "25fe817b47ea1fa05f7637de549adb20dfe71a8f999c7e583b97ebde3021d949",
        "proof_raw_sha256":
            "54bed8a5f4adbeaf06deb9fa6665c458352169fa9d5de3d07c959712709dc2cb",
        "proof_gzip_sha256":
            "845c6504fe4d25d9f465be843afa4c5dae9a5707b46c61717ea5503898e4bfb1",
        "proof_additions": 101748,
    },
}


def structural(case_name):
    case = CASES[case_name]
    cnf = G.build_exhaustion_cnf(case["target"])
    require(len(cnf.names) == 9383, len(cnf.names))
    require(len(cnf.clauses) == 57731, len(cnf.clauses))
    require(len(G.orbit(case["target"])) == 720, case_name)
    cnf_bytes = cnf.dimacs().encode("ascii")
    require(sha256(cnf_bytes).hexdigest() == case["cnf_sha256"],
            (case_name, "CNF changed"))

    proof_path = CERTIFICATES / (case["stem"] + ".drup.gz")
    compressed = proof_path.read_bytes()
    require(sha256(compressed).hexdigest() == case["proof_gzip_sha256"],
            (case_name, "compressed proof changed"))
    raw = gzip.decompress(compressed)
    require(sha256(raw).hexdigest() == case["proof_raw_sha256"],
            (case_name, "raw proof changed"))
    lines = raw.splitlines()
    require(len(lines) == case["proof_additions"],
            (case_name, len(lines)))
    require(lines[-1].strip() == b"0", (case_name, lines[-1][-80:]))
    require(not any(line.startswith(b"d ") for line in lines),
            (case_name, "proof has deletions"))
    return cnf_bytes, raw


def replay(case_name, cnf_bytes, raw):
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import verify_drup_certificate

    with tempfile.TemporaryDirectory(prefix="n8-affine-rup-") as directory:
        directory = Path(directory)
        cnf_path = directory / "input.cnf"
        proof_path = directory / "proof.drup"
        cnf_path.write_bytes(cnf_bytes)
        proof_path.write_bytes(raw)
        verify_drup_certificate.verify(
            cnf_path, proof_path, solver_name="cadical195"
        )
    print("proof replay", case_name, "PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "proof"),
                        default="structural")
    parser.add_argument("--case", choices=("12", "012", "both"),
                        default="both")
    arguments = parser.parse_args()
    names = tuple(CASES) if arguments.case == "both" else (arguments.case,)
    for name in names:
        cnf_bytes, raw = structural(name)
        print("structural", name, "PASS",
              "orbit=720", "clauses=57731",
              "proof_additions=" + str(CASES[name]["proof_additions"]))
        if arguments.mode == "proof":
            replay(name, cnf_bytes, raw)


if __name__ == "__main__":
    main()
