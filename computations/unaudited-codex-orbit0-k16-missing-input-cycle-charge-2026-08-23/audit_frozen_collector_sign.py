#!/usr/bin/env python3
"""Literal referee for the sign of the frozen K14-to-K16 collector."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_PATH = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
             / "audit_orbit0_k14_interface.py")
COLLECTOR = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
             / "collect_orbit0_k16_literal_residual.py")
FROZEN_RESULT = COLLECTOR.with_name("results_orbit0_k16_literal_residual.json")
OUT = HERE / "results_frozen_collector_sign_referee.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def subtract(row, divisor):
    value = Counter(row)
    value.subtract(divisor)
    require(all(coefficient >= 0 for coefficient in value.values()), "nondivisor")
    return bytes(sorted(cell for cell, coefficient in value.items()
                        for _ in range(coefficient)))


def main():
    k14 = load("collector_sign_k14", K14_PATH)
    frozen = k14.FROZEN
    source = COLLECTOR.read_text()
    require("pair_mass = coefficient * orbit_size * packet_coefficient" in source
            and "pivot_weight = -pair_mass / len(available)" in source,
            "collector sign lines changed")
    raw = json.loads(frozen.R8P.read_text())
    r8_row = bytes.fromhex(raw["residual"][0][0])
    full_orbit = frozen.EXPORT.row_orbit(r8_row)
    actual = Fraction(raw["residual"][0][1], raw["residual"][0][2]) / len(full_orbit)

    words = tuple(frozen.word_from_pair_colours(row) for row in frozen.PAIR_COLOURS)
    anchors = tuple(frozen.BASE.term_ids(word, frozen.M0) for word in words)
    e2 = tuple(Counter({term: 1 for term in frozen.BASE.word_terms(word)
                        if frozen.row_k_degree(term) == 2}) for word in words)
    packet = frozen.polynomial_product(frozen.polynomial_product(e2[0], e2[1]), e2[2])
    packet_row, packet_coefficient = min(packet.items())
    target = bytes(sorted(r8_row + packet_row))
    pair_mass = actual * len(full_orbit) * packet_coefficient
    require(pair_mass == Fraction(raw["residual"][0][1], raw["residual"][0][2]),
            pair_mass)

    mixed = []
    for c0 in range(3):
        for c1 in range(3):
            for c2 in range(3):
                for c3 in range(3):
                    colours = (c0, c1, c2, c3)
                    if len(set(colours)) == 1:
                        continue
                    word = frozen.word_from_pair_colours(colours)
                    head = frozen.BASE.term_ids(word, frozen.M0)
                    try:
                        quotient = subtract(target, head)
                    except RuntimeError:
                        continue
                    tails = tuple(term for term in frozen.BASE.word_terms(word)
                                  if frozen.row_k_degree(term) == 2)
                    mixed.append((colours, word, head, quotient, tails))
    require(mixed and all(len(record[4]) == 12 for record in mixed), len(mixed))
    colours, word, head, quotient, tails = mixed[0]

    # R = -m*qU. With H=q+sum(tails)=0, subtracting cH with c=-m
    # cancels qU and leaves +m times every tail. The frozen collector stores
    # -m/|available| instead, hence the entire averaged tail has opposite sign.
    target_coefficient = -pair_mass
    source_multiplier = target_coefficient
    replay = Counter({target: target_coefficient})
    replay[target] -= source_multiplier
    for tail in tails:
        replay[bytes(sorted(quotient + tail))] -= source_multiplier
    replay = Counter({row: coefficient for row, coefficient in replay.items()
                      if coefficient})
    require(target not in replay and set(replay.values()) == {pair_mass}
            and len(replay) == 12, "literal head cancellation sign failed")
    collector_tail_weight = -pair_mass
    require(collector_tail_weight == -next(iter(replay.values())),
            "collector did not have opposite literal tail sign")

    frozen_result = json.loads(FROZEN_RESULT.read_text())
    result = {
        "schema": "orbit0-k16-frozen-collector-sign-referee-v1",
        "status": "EXACT_FROZEN_COLLECTOR_GLOBAL_SIGN_REVERSED",
        "literal_R8_row": r8_row.hex(),
        "literal_K14_head": target.hex(),
        "literal_pivot_word": "".join(map(str, word)),
        "literal_pivot_pair_colours": list(colours),
        "pair_mass": str(pair_mass),
        "leading_target_coefficient": str(target_coefficient),
        "correct_tail_coefficient_per_selected_pivot": str(pair_mass),
        "frozen_collector_tail_coefficient_per_selected_pivot": str(collector_tail_weight),
        "literal_K2_tails": len(tails),
        "collector_formula_uniform_over_all_pairs": True,
        "frozen_stored_cycle_charge": -311_258_112,
        "sign_corrected_cycle_charge": 311_258_112,
        "collector_sha256": sha256(COLLECTOR.read_bytes()).hexdigest(),
        "frozen_result_sha256": sha256(FROZEN_RESULT.read_bytes()).hexdigest(),
        "frozen_result_logical": frozen_result["logical_sha256"],
        "scope_guard": ("Referees the global sign of the frozen K14-to-K16 "
                        "tail collection only; does not compute K18 tails."),
    }
    logical = dict(result)
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
