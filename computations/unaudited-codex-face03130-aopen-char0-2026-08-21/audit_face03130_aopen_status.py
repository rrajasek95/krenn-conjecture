#!/usr/bin/env python3
"""Independent interface/timeout audit for the unresolved 0:31:30 A-open lane."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
TOOLKIT = COMP / "toolkit/groebner/msolve_io.py"
EXPORT = HERE / "results_face03130_aopen_export.json"
RESULT_PREFIX = HERE / "results_face03130_aopen_status_replay"
INPUT_PAIRS = (
    ("base", "face03130_aopen_base_char0.msolve",
     "face03130_aopen_base_p1073741827.msolve", 16),
    ("full_product", "face03130_aopen_full_char0.msolve",
     "face03130_aopen_full_p1073741827.msolve", 16),
    ("split_live", "face03130_aopen_split_live_char0.msolve",
     "face03130_aopen_split_live_p1073741827.msolve", 18),
    ("core8_split_live", "face03130_aopen_core8_split_live_char0.msolve",
     "face03130_aopen_core8_split_live_p1073741827.msolve", 11),
)
TIMEOUTS = {
    "results_face03130_aopen_base_p1073741827.manifest.json":
        (120.0, "b632089dd01538c15f1766b649e84a223dd45e894005ab583f9512b0c93c8c4e"),
    "results_face03130_aopen_full_p1073741827.manifest.json":
        (120.0, "bc39bf866b210b46dbf8f5acfb879084a7c9260424f1b5c088986dbaf7e43f74"),
    "results_face03130_aopen_split_live_p1073741827.manifest.json":
        (120.0, "8ea8b557c6f2b3b5f9a5e5b91ef45ba54357a64fbd88f73affdb9b8c5a31acc2"),
    "results_face03130_aopen_core8_split_live_p1073741827.manifest.json":
        (60.0, "ceaba1fd8f7e06a567591f673014690a666540b86ae44ee9aeeb5ba9727c73f2"),
    "results_face03130_aopen_core8_split_live_char0.manifest.json":
        (120.0, "56c9b1120d7412ccecb71d5c1c0717736d107a4699d2ffeb615ea3f4219a9f4d"),
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    MSOLVE_IO = load("face03130_aopen_status_msolve_io", TOOLKIT)
    export = json.loads(EXPORT.read_text())
    require(export["result_sha256"] ==
            "38882f87ad3c77f8031cdf8bdb446e7c05e32ff92a198e9be7e3ad60d1bc819d",
            "exact export logical result changed")
    require(len(export["reduced_rows"]) == 15 and
            [row["raw_index"] for row in export["reduced_rows"]] ==
            [6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            "reduced source-row interface changed")
    require(export["core8_raw_indices"] == [6, 8, 12, 14, 16, 18, 19, 20],
            "core8 ranking changed")
    require([(row["maximum_row_terms"], row["maximum_live_terms"])
             for row in export["secondary_pivot_growth"]] ==
            [(262, 735), (425, 1103)],
            "secondary-pivot growth conclusion changed")

    pairs = []
    iteration = list(INPUT_PAIRS)
    if args.mode == "-O":
        iteration.reverse()
    for label, q_name, p_name, count in iteration:
        q_path, p_path = HERE / q_name, HERE / p_name
        q = MSOLVE_IO.read_msolve_input(
            q_path, strict=True, allow_characteristic_zero=True)
        p = MSOLVE_IO.read_msolve_input(p_path, strict=True)
        require(q.characteristic == 0 and p.characteristic == 1073741827 and
                q.variables == p.variables and q.polynomials == p.polynomials
                and q.polynomial_sha256 == p.polynomial_sha256 and
                len(q.polynomials) == count,
                f"{label} exact-Q/modular interface changed")
        pairs.append({"label": label, "polynomial_count": count,
                      "Q_sha256": q.file_sha256,
                      "modular_sha256": p.file_sha256,
                      "source_row_digest_prefix": list(q.polynomial_sha256[:2])})

    timeout_records = []
    timeout_iteration = list(TIMEOUTS.items())
    if args.mode == "-I-S":
        timeout_iteration.reverse()
    for name, (cap, logical) in timeout_iteration:
        path = HERE / name
        manifest = json.loads(path.read_text())
        require(manifest["status"] == "timeout" and
                manifest["timeout_seconds"] == cap and
                manifest["logical_sha256"] == logical and
                manifest["solution"] is None and
                manifest["output"]["bytes"] == 0,
                f"timeout manifest changed: {name}")
        if "char0" in name:
            require(manifest["characteristic_zero_explicit_opt_in"] is True and
                    manifest["command"][-2:] == ["-P", "1"],
                    "char0 core8 exact-mode guard changed")
        timeout_records.append({"manifest": name, "cap": cap,
                                "logical_sha256": logical})

    # Byte mutation must change a canonical source digest without touching
    # any frozen file.
    core_q = MSOLVE_IO.read_msolve_input(
        HERE / INPUT_PAIRS[-1][1], strict=True, allow_characteristic_zero=True)
    first = core_q.polynomials[0]
    mutated = ("-" + first[1:]) if first.startswith("+") else (
        first[1:] if first.startswith("-") else "-" + first)
    require(MSOLVE_IO.polynomial_sha256(mutated) !=
            core_q.polynomial_sha256[0], "source mutation did not fire")

    result = {
        "status": "UNAUDITED exact source/export and bounded-timeout replay PASS",
        "mode": args.mode,
        "branch": "k5 0:31:30 A-open/R25",
        "proved": (
            "raw7 A-open substitution, all fifteen reduced literal rows, "
            "all live-factor transports, and size/ranking profiles"),
        "not_proved": "emptiness or nonemptiness of the A-open branch",
        "input_pairs": pairs,
        "timeout_records": timeout_records,
        "core8_raw_indices": export["core8_raw_indices"],
        "secondary_pivot_growth": export["secondary_pivot_growth"],
        "precise_blocker": (
            "No modular unit, exact-Q unit, or positive-dimensional sentinel "
            "was produced within the declared caps. Literal raw16/a2 and "
            "raw20/b3 second solves increase row/live packets to 262/735 and "
            "425/1103 terms. The next route needs a component/slice or an "
            "alternate sparse row combination."),
        "export_file_sha256": file_sha(EXPORT),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    output = Path(str(RESULT_PREFIX) + "_" + suffix + ".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
