#!/usr/bin/env python3
"""Hostile contract tests for the K24 atomic result validator."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "validate_k24_factorized_bounded_result.py"
ENGINE = HERE / "run_k24_factorized_direct_d17_d18.rs"


def load_validator():
    spec = importlib.util.spec_from_file_location("k24_atomic_validator", SOURCE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


V = load_validator()


def must_reject(label, action):
    try:
        action()
    except V.ValidationError:
        return label
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def main():
    rejected = []
    rejected.append(must_reject(
        "wrong_literal_samples_type",
        lambda: V.validate_witness(Path("/definitely/missing"), [])))
    rejected.append(must_reject(
        "extra_top_level_property",
        lambda: V.exact_keys({"hostile_extra": True}, set(), "hostile")))
    rejected.append(must_reject(
        "missing_required_property",
        lambda: V.exact_keys({}, {"degree"}, "hostile")))
    rejected.append(must_reject(
        "wrong_engine_hash",
        lambda: V.require(V.sha256(ENGINE) == "0" * 64, "hostile engine hash")))
    with tempfile.TemporaryDirectory(prefix="k24-orbit-division-hostile-") as temporary:
        bad = Path(temporary) / "bad.columns.tsv"
        # W=1 but alpha=1 for a 384-element orbit: deliberately inexact.
        bad.write_text("00000001:" + "00" * 20 + "\t384\t1\t1\t1\t1\n",
                       encoding="ascii")
        digest = hashlib.sha256(bad.read_bytes()).hexdigest()
        rejected.append(must_reject(
            "inexact_orbit_division",
            lambda: V.validate_tsv(bad, digest, bad.stat().st_size, 1, {"384": 1})))
    V.validate_contract_schema()
    print(json.dumps({
        "status": "PASS_HOSTILE_FAIL_CLOSED_VALIDATOR_TESTS",
        "rejected": rejected,
        "schema_validator_keysets_locked": True,
        "old_design_schema_supersession_locked": True,
    }, indent=2))


if __name__ == "__main__":
    main()
