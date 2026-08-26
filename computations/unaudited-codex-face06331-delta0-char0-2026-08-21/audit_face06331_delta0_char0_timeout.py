#!/usr/bin/env python3
"""Audit the frozen k5 delta=0 source interface and timeout terminal."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
INPUT = HERE / "face06331_delta0_full_source_char0.msolve"
LABELS = HERE / "face06331_delta0_full_source_char0_labels.json"
EXPORT = HERE / "results_face06331_delta0_char0_export.json"
OUTPUT = HERE / "results_face06331_delta0_full_source_char0.param.out"
MANIFEST = HERE / "results_face06331_delta0_full_source_char0.manifest.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
PARAM = REPO / "computations/toolkit/groebner/run_msolve_parametrize.py"
RESULT_PREFIX = HERE / "results_face06331_delta0_char0_timeout_replay"
INPUT_SHA = "6120bec2f1c4d9c38aeb44f2dd853ff48f6925066f709629d977a39c9a0a1252"
MANIFEST_LOGICAL = "1549ee4cbcb66979e93e7c1e99dd90e1d636d41b7f53c675cda7d1536a7e54c5"
EXPORT_LOGICAL = "d6b035ed2be1e2b343fabea0639bd009dd7a866582dbd88b4e306c8be529d24c"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


IO = load("face06331_delta0_timeout_io", TOOLKIT)
sys.path.insert(0, str(TOOLKIT.parent))
P = load("face06331_delta0_timeout_param", PARAM)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    require(sha256(INPUT.read_bytes()).hexdigest() == INPUT_SHA,
            "frozen input changed")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.characteristic == 0 and len(parsed.variables) == 13 and
            len(parsed.polynomials) == 17,
            "strict source interface changed")
    labels = json.loads(LABELS.read_text())
    export = json.loads(EXPORT.read_text())
    require(labels["raw_source_indices"] == list(range(6, 22)) and
            labels["branch_substitution"] == "d2=d1" and
            export["retained_raw_indices"] == list(range(6, 22)) and
            export["raw8_is_four_term_residual"] and
            export["localizer_terms"] == 2464 and
            export["result_sha256"] == EXPORT_LOGICAL and
            export["input_file_sha256"] == INPUT_SHA and
            tuple(export["input_polynomial_sha256"]) ==
            tuple(parsed.polynomial_sha256),
            "three-mode source-export ledger changed")
    manifest = json.loads(MANIFEST.read_text())
    require(manifest["logical_sha256"] == MANIFEST_LOGICAL and
            manifest["status"] == "timeout" and
            manifest["elapsed_seconds"] >= 600 and
            manifest["returncode"] == -15 and
            manifest["solution"] is None and
            manifest["input"]["sha256"] == INPUT_SHA,
            "terminal timeout manifest changed")
    require(OUTPUT.is_file() and OUTPUT.stat().st_size == 0,
            "timeout unexpectedly produced output")
    rejected = False
    try:
        P.parse_parametrization(OUTPUT, 0, len(parsed.variables))
    except ValueError:
        rejected = True
    require(rejected, "zero-byte output accepted as sentinel")
    first = parsed.polynomials[0]
    mutated_first = ("-"+first if not first.startswith("-") else first[1:])
    mutated_rab = parsed.polynomials[-1].replace("-1", "+1")
    require(IO.polynomial_sha256(mutated_first) !=
            parsed.polynomial_sha256[0] and
            IO.polynomial_sha256(mutated_rab) !=
            parsed.polynomial_sha256[-1], "mutation guard failed")
    result = {
        "status": "UNAUDITED source ledger PASS; exact gate TIMEOUT",
        "mode": args.mode, "state": "0:63:31", "branch": "d1=d2",
        "raw_source_indices": list(range(6, 22)),
        "variables": parsed.variables, "localizer_terms": 2464,
        "input_sha256": INPUT_SHA,
        "source_export_logical_sha256": EXPORT_LOGICAL,
        "manifest_logical_sha256": MANIFEST_LOGICAL,
        "terminal": "600s timeout; zero-byte output; no sentinel",
        "must_fire": ["source sign mutation", "Rabinowitsch mutation",
                      "zero-byte sentinel rejection"],
        "scope_guard": "No algebraic verdict; d1-d2!=0 untouched.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    Path(str(RESULT_PREFIX)+"_"+suffix+".json").write_text(
        json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
