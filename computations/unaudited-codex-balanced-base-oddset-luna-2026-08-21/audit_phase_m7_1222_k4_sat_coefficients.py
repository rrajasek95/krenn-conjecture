#!/usr/bin/env python3
"""Export the literal coefficient system on the complete-SMT support witness."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_phase_m7_support_coefficients import replay_model  # noqa: E402


INPUT = HERE / "results_phase_m7_1222_k4_sat_witness.json"
OUTPUT = HERE / "results_phase_m7_1222_k4_sat_coefficient_target.json"
PATTERN = re.compile(r"x_([0-7])_([0-7])_([01])_([01])_([1-7])")


def main():
    support_data = json.loads(INPUT.read_text())
    support = []
    for name in support_data["support"]:
        match = PATTERN.fullmatch(name)
        if match is None:
            raise ValueError(name)
        support.append(tuple(map(int, match.groups())))
    replay = replay_model(frozenset(support))
    if replay["singleton_rows"]:
        raise RuntimeError("SMT witness acquired a literal singleton")
    output = {
        "branch": "1222_k4_C1222",
        "source_support": INPUT.name,
        "coefficient_system": replay,
        "exact_gate_launched": False,
        "reason": (
            "The complete support witness has more than 20 live coefficient "
            "variables; per the bounded guard no broad exact gate was launched."
        ),
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "variables": replay["variable_count"],
        "mixed_equations": replay["mixed_equation_count"],
        "term_profile": replay["mixed_term_count_profile"],
        "pure7_terms": replay["pure7_term_count"],
        "singletons": len(replay["singleton_rows"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
