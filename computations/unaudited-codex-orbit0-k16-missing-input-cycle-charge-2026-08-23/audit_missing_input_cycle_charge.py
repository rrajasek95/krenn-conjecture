#!/usr/bin/env python3
"""Exact factored 77-cycle charge of the omitted direct K16 input packet."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_PATH = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
             / "audit_orbit0_k14_interface.py")
R8_PATH = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
           / "results_orbit0_cutoff9_sparse_r8.json")
DUAL_PATH = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
             / "k16_cycle_partition_dual.tsv")
DUAL_RESULT = DUAL_PATH.with_name("results_k16_cycle_partition_quotient.json")
INPUT = HERE / "missing_input_cycle_charge_input.tsv"
DIRECT_RESIDUAL = HERE / "missing_direct_irreducible_H_orbits.tsv"
RUST = HERE / "pair_missing_input_cycle_charge.rs"
BIN = HERE / "pair_missing_input_cycle_charge"
OUT = HERE / "results_missing_input_cycle_charge.json"
SIGN_RESULT = HERE / "results_frozen_collector_sign_referee.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def matching_code(base, row):
    partner = [-1] * 24
    for cell in row:
        u, v, a, b = base.CELLS[cell]
        left, right = 3 * u + a, 3 * v + b
        require(left != right and partner[left] == partner[right] == -1,
                (row.hex(), cell, left, right))
        partner[left], partner[right] = right, left
    require(all(value >= 0 for value in partner), (row.hex(), partner))
    return bytes(partner)


def compose(left, right):
    return bytes(left[right[index]] for index in range(len(left)))


def generators(transforms):
    identity = bytes(range(len(transforms[0])))
    universe = set(transforms)
    require(identity in universe, "identity absent")
    generated = {identity}
    chosen = []
    while generated != universe:
        generator = min(universe - generated)
        chosen.append(generator)
        queue = list(generated)
        while queue:
            value = queue.pop()
            for operation in chosen:
                for image in (compose(value, operation), compose(operation, value)):
                    if image not in generated:
                        require(image in universe, "generated action left H")
                        generated.add(image)
                        queue.append(image)
    return tuple(chosen)


def build_input(mutate=False):
    k14 = load("missing_input_k14", K14_PATH)
    frozen = k14.FROZEN
    raw = json.loads(R8_PATH.read_text())
    dual_result = json.loads(DUAL_RESULT.read_text())
    require(dual_result["exact_target_pairing"] == -311_258_112,
            "frozen pivot-tail charge drift")

    words = tuple(frozen.word_from_pair_colours(colours)
                  for colours in frozen.PAIR_COLOURS)
    anchor_terms = tuple(frozen.BASE.term_ids(word, frozen.M0) for word in words)
    factors = []
    for word in words:
        by_degree = {}
        terms = frozen.BASE.word_terms(word)
        require(Counter(frozen.row_k_degree(term) for term in terms)
                == {0: 1, 2: 12, 3: 32, 4: 60}, "factor profile drift")
        for degree in (2, 3, 4):
            by_degree[degree] = tuple(term for term in terms
                                      if frozen.row_k_degree(term) == degree)
        factors.append(by_degree)

    # This is exactly the K8 part of E0*E1*E2: permutations of (2,2,4)
    # and (2,3,3), with all coefficients collected before pairing.
    packet = Counter()
    for distinguished in range(3):
        other = tuple(index for index in range(3) if index != distinguished)
        for first in factors[distinguished][4]:
            for second in factors[other[0]][2]:
                for third in factors[other[1]][2]:
                    packet[bytes(sorted(first + second + third))] += 1
        for first in factors[distinguished][2]:
            for second in factors[other[0]][3]:
                for third in factors[other[1]][3]:
                    packet[bytes(sorted(first + second + third))] += 1
    require(len(packet) == sum(packet.values()) == 62_784
            and set(packet.values()) == {1}, "K8 packet collection drift")

    factor_set = frozenset(anchor_terms)
    h_actions = tuple(action for action in range(len(frozen.EXPORT.STABILIZER))
                      if frozenset(frozen.move_row(term, action)
                                   for term in anchor_terms) == factor_set)
    require(len(h_actions) == 384, len(h_actions))
    h_transforms = tuple(frozen.EXPORT.TRANSFORMS[action] for action in h_actions)
    h_generators = generators(h_transforms)
    packet_keys = frozenset(packet)
    # A finite generator replay proves the collected homogeneous packet is
    # H-invariant, which licenses the orbit-mass evaluation below.
    for transform in h_generators:
        moved = {bytes(sorted(transform[cell] for cell in row)) for row in packet}
        require(moved == packet_keys, "K8 packet is not H-invariant")

    representatives = []
    full_mass = Fraction(0)
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        full_orbit = set(frozen.EXPORT.row_orbit(representative))
        actual = Fraction(numerator, denominator) / len(full_orbit)
        unseen = set(full_orbit)
        while unseen:
            seed = min(unseen)
            orbit = {frozen.move_row(seed, action) for action in h_actions}
            require(orbit <= full_orbit and orbit <= unseen, "H orbit split failed")
            mass = actual * len(orbit)
            require(mass.denominator == 1, (seed.hex(), mass))
            representatives.append((seed, mass.numerator, len(orbit)))
            full_mass += mass
            unseen.difference_update(orbit)
    require(len(representatives) == 485 and full_mass == -23_328,
            (len(representatives), full_mass))
    if mutate:
        first = representatives[0]
        representatives[0] = (first[0], first[1] + 1, first[2])

    lines = ["KRENN_MISSING_K16_CYCLE_CHARGE_V1",
             f"R {len(representatives)}", f"P {len(packet)}"]
    for pair, (u, v) in enumerate(frozen.M0):
        for colour in range(3):
            cell = frozen.BASE.CELL_ID[(u, v, colour, colour)]
            lines.append(f"A\t{cell}\t{pair}\t{colour}")
    for transform in h_transforms:
        lines.append(f"H\t{transform.hex()}")
    for cell, (u, v, a, b) in enumerate(frozen.BASE.CELLS):
        lines.append(f"C\t{cell}\t{3*u+a}\t{3*v+b}")
    for row, mass, orbit_size in sorted(representatives):
        lines.append(f"R\t{row.hex()}\t{matching_code(frozen.BASE, row).hex()}\t{mass}\t{orbit_size}")
    for row, coefficient in sorted(packet.items()):
        lines.append(f"P\t{row.hex()}\t{matching_code(frozen.BASE, row).hex()}\t{coefficient}")
    payload = "\n".join(lines) + "\n"
    INPUT.write_text(payload)
    return {
        "input_sha256": sha256(payload.encode()).hexdigest(),
        "R8_G_orbits": len(raw["residual"]),
        "R8_H_orbits": len(representatives),
        "R8_H_orbit_mass_sum": int(full_mass),
        "K8_packet_terms": len(packet),
        "K8_packet_raw_terms": sum(packet.values()),
        "H_order": len(h_actions),
        "H_generator_count": len(h_generators),
        "H_generator_packet_replay": True,
        "r8_sha256": sha256(R8_PATH.read_bytes()).hexdigest(),
        "dual_sha256": sha256(DUAL_PATH.read_bytes()).hexdigest(),
        "frozen_pivot_tail_charge": dual_result["exact_target_pairing"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    record = build_input(args.mutate)
    subprocess.run(["rustc", "-O", str(RUST), "-o", str(BIN)], check=True)
    process = subprocess.run([str(BIN), str(INPUT), str(DUAL_PATH),
                              str(DIRECT_RESIDUAL)], check=True,
                             text=True, capture_output=True)
    paired = json.loads(process.stdout)
    sign_referee = json.loads(SIGN_RESULT.read_text())
    require(sign_referee["status"] == "EXACT_FROZEN_COLLECTOR_GLOBAL_SIGN_REVERSED"
            and sign_referee["sign_corrected_cycle_charge"] == 311_258_112,
            "collector sign referee drift")
    record.update(paired)
    require(record["component_sign"] == -1, record)
    require(record["missing_direct_component_pairing"] == 388_502_016,
            "hostile mutation or missing-component charge drift")
    record["combined_with_frozen_pivot_tail_charge"] = (
        record["missing_direct_component_pairing"]
        + record["frozen_pivot_tail_charge"])
    require(record["combined_with_frozen_pivot_tail_charge"] == 77_243_904,
            "charge comparison drift")
    record["reduced_direct_plus_frozen_stored_tail_charge"] = (
        record["collected_missing_direct_irreducible_pairing"]
        + record["frozen_pivot_tail_charge"])
    record["sign_corrected_frozen_tail_charge"] = (
        sign_referee["sign_corrected_cycle_charge"])
    record["reduced_direct_plus_sign_corrected_tail_charge"] = (
        record["collected_missing_direct_irreducible_pairing"]
        + record["sign_corrected_frozen_tail_charge"])
    require(record["missing_direct_component_pairing"] ==
            record["missing_direct_pivotable_pairing"]
            + record["missing_direct_irreducible_pairing"],
            "pivot split does not replay raw charge")
    require(record["irreducible_collected_H_orbits"] == 93_328
            and record["reduced_direct_plus_frozen_stored_tail_charge"]
            == -247_388_928
            and record["reduced_direct_plus_sign_corrected_tail_charge"]
            == 375_127_296,
            "irreducible collection drift")
    record["collector_sign_referee_logical"] = sign_referee["logical_sha256"]
    record.update({
        "schema": "orbit0-k16-missing-direct-input-cycle-charge-v1",
        "status": "EXACT_SINGLETON_REDUCED_DIRECT_K16_WITH_SIGN_REFEREED_TAIL",
        "scope_guard": ("Exact cycle-partition pairing of only -R8prime times the "
                        "K8 homogeneous packet, split by literal K0 singleton "
                        "pivotability; no K18 tails or later frontier."),
    })
    logical = dict(record)
    record["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if not args.verify:
        OUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
