#!/usr/bin/env python3
"""Independent direct audit of a SAT support result and PyTheus baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from w3w3_support_core import (
    PYTHEUS_TEN_SOURCE_SOLUTION,
    audit_occurrence_support,
)


def require(condition: bool, detail) -> None:
    if not condition:
        raise RuntimeError(detail)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path, nargs="?")
    arguments = parser.parse_args()

    baseline = audit_occurrence_support(PYTHEUS_TEN_SOURCE_SOLUTION, 10)
    require(baseline["forbidden_nonzero_words"] == [], baseline)
    require(set(baseline["target_multiplicities"].values()) == {1}, baseline)
    print("PyTheus ten-source baseline: verified exact occurrence support")

    if arguments.result is None:
        return
    payload = json.loads(arguments.result.read_text(encoding="utf-8"))
    require(payload["schema"] == "w3w3-occurrence-support-v1", payload)
    if payload["status"] == "sat":
        support = payload["audited_model"]["support"]
        audited = audit_occurrence_support(support, payload["maximum_sources"])
        require(audited == payload["audited_model"], (audited, payload))
        print(
            f"SAT model: independently verified {audited['source_count']} sources"
        )
    else:
        require(payload["status"] == "unsat", payload["status"])
        print("UNSAT result requires replay of the accompanying CNF proof")


if __name__ == "__main__":
    main()
