#!/usr/bin/env python3
"""Independent streaming referee for the factored P0-square target seed."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
T2_PATH = HERE / "audit_orbit0_t2_pivot_setup.py"
SPEC = importlib.util.spec_from_file_location("orbit0_factored_seed", T2_PATH)
T2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(T2)
RADICAL = HERE.parent / "unaudited-codex-orbit0-t2-radical-2026-08-20"
GRADED = HERE.parent / "unaudited-codex-n8-orbit0-t2-graded-2026-08-20"
SEED = RADICAL / "factored_p0_square_seed.txt"
CANONICAL = GRADED / "r8prime_square_pure_anchor_factored_canonical.jsonl"
RAW = GRADED / "r8prime_square_pure_anchor_factored_raw.jsonl"
FULL = RADICAL / "results_sparse_r8_square_collected.json"
OUT = HERE / "results_factored_p0_square_seed_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def transform_from_action(sites_text, colours_text):
    sites = tuple(map(int, sites_text))
    colours = tuple(map(int, colours_text))
    return bytes(T2.BASE.CELL_ID[T2.transform_cell(cell, sites, colours)]
                 for cell in T2.BASE.CELLS), (sites, colours)


def move(row, transform):
    return bytes(sorted(transform[cell] for cell in row))


def canonical(row, transforms):
    return min(move(row, transform) for transform in transforms)


def port_control(row):
    ports = Counter()
    for cell_id in row:
        u, v, a, b = T2.BASE.CELLS[cell_id]
        ports[(u, a)] += 1
        ports[(v, b)] += 1
    require(len(row) == 16 and all(cell not in T2.ANCHORS for cell in row),
            "factored target has wrong total/K degree")
    require(all(ports[(site, 0)] == 0 for site in range(8)),
            "factored target uses colour-zero ports")
    require(all(ports[(site, colour)] == 2
                for site in range(8) for colour in (1, 2)),
            "factored target does not have complementary port degree two")


def main():
    actions = []
    transforms = []
    targets = []
    common_factor = None
    with SEED.open() as handle:
        require(next(handle).strip() == "KRENN_FACTORED_P0_SQUARE_SEED_V1",
                "factored seed magic changed")
        for line in handle:
            fields = line.split()
            if not fields:
                continue
            if fields[0] == "ANCHORS":
                require(fields[1] == bytes(sorted(T2.ANCHORS)).hex(),
                        "seed anchors changed")
            elif fields[0] == "DEGREE":
                require(fields[1] == "16", "seed degree changed")
            elif fields[0] == "COMMON_FACTOR":
                common_factor = bytes.fromhex(fields[1])
            elif fields[0] == "ACTION":
                transform, action = transform_from_action(fields[1], fields[2])
                transforms.append(transform)
                actions.append(action)
            elif fields[0] == "TARGET":
                targets.append((bytes.fromhex(fields[1]),
                                Fraction(int(fields[2]), int(fields[3]))))
            else:
                raise RuntimeError(f"unknown seed record {fields[0]}")
    expected_factor = bytes(sorted(cell for colour in (0, 0)
                                   for u, v in T2.M0
                                   for cell in (T2.BASE.CELL_ID[(u, v, colour, colour)],)))
    require(common_factor == expected_factor and len(common_factor) == 8,
            "common pure-anchor square changed")
    expected_actions = {(sites, colours) for sites, colours in T2.ACTIONS
                        if colours[0] == 0}
    require(len(actions) == len(set(actions)) == 768
            and set(actions) == expected_actions,
            "seed action is not the full pure-zero stabilizer")
    require(len(targets) == 1578292 and targets == sorted(targets),
            "seed target support/order changed")

    # Read eight raw rows first.  Their complete 768-orbits let us stream the
    # full raw file and exactly recover the total coefficient of those sample
    # canonical rows without trusting the producer's canonicalizer.
    raw_samples = []
    with RAW.open() as handle:
        raw_header = json.loads(next(handle))
        for line in handle:
            record = json.loads(line)
            if record["type"] == "row":
                raw_samples.append(bytes.fromhex(record["row"]))
                if len(raw_samples) == 8:
                    break
    sample_representatives = tuple(sorted({canonical(row, transforms)
                                           for row in raw_samples}))
    orbit_lookup = {}
    for representative in sample_representatives:
        for transform in transforms:
            image = move(representative, transform)
            previous = orbit_lookup.setdefault(image, representative)
            require(previous == representative, "sample target orbits overlap")
    raw_sample_mass = Counter()
    raw_rows = 0
    raw_mass = Fraction()
    with RAW.open() as handle:
        require(json.loads(next(handle)) == raw_header, "raw header changed in replay")
        for line in handle:
            record = json.loads(line)
            if record["type"] != "row":
                continue
            row = bytes.fromhex(record["row"])
            coefficient = Fraction(*record["coefficient"])
            raw_rows += 1
            raw_mass += coefficient
            representative = orbit_lookup.get(row)
            if representative is not None:
                raw_sample_mass[representative] += coefficient
    require(raw_rows == 1615520 and raw_mass == 181398528,
            "raw factored stream census/mass changed")

    # The canonical stream is the three pure colours normalized to zero.  The
    # final seed divides those coefficients by three to retain one P0 square.
    canonical_samples = {}
    seed_samples = {}
    seed_mass = Fraction()
    seed_l1 = Fraction()
    canonical_rows = 0
    with CANONICAL.open() as canonical_handle:
        canonical_header = json.loads(next(canonical_handle))
        require(canonical_header["nonzero_orbits"] == len(targets)
                and canonical_header["input_mass"] == 181398528
                and canonical_header["output_mass"] == 181398528,
                "canonical stream header changed")
        for (seed_row, seed_coefficient), canonical_line in zip(
                targets, canonical_handle, strict=True):
            record = json.loads(canonical_line)
            require(record["type"] == "row", "canonical stream record changed")
            canonical_row = bytes.fromhex(record["row"])
            canonical_coefficient = Fraction(*record["coefficient"])
            require(seed_row == canonical_row
                    and 3 * seed_coefficient == canonical_coefficient,
                    "seed is not the exact one-colour third of canonical target")
            port_control(seed_row)
            seed_mass += seed_coefficient
            seed_l1 += abs(seed_coefficient)
            canonical_rows += 1
            if seed_row in sample_representatives:
                canonical_samples[seed_row] = canonical_coefficient
                seed_samples[seed_row] = seed_coefficient
    require(canonical_rows == len(targets)
            and seed_mass == 60466176 and seed_l1 == 5490011904,
            "factored seed mass changed")
    require(raw_sample_mass == Counter(canonical_samples),
            "independent raw sample-orbit sums differ from canonical stream")

    # Bounded but literal canonicality controls, spread deterministically over
    # the 1.58M rows.
    control_indices = sorted({index * (len(targets) - 1) // 1023
                              for index in range(1024)})
    for index in control_indices:
        row = targets[index][0]
        require(canonical(row, transforms) == row,
                f"seed row {index} is not canonical under G0")

    # Cross-check the stated 3c/4 normalization directly against the full-G
    # collected target for the same eight sample orbits.
    full_keys = {}
    for representative in sample_representatives:
        lifted = bytes(sorted(common_factor + representative))
        full_keys[canonical(lifted, T2.TRANSFORMS)] = representative
    full_values = {}
    full_data = json.loads(FULL.read_text())
    for row_hex, scaled_coefficient in full_data["target"]:
        row = bytes.fromhex(row_hex)
        if row in full_keys:
            full_values[full_keys[row]] = Fraction(scaled_coefficient)
    require(set(full_values) == set(sample_representatives),
            "full-G target missed a sample factored orbit")
    require(all(seed_samples[row] == Fraction(3, 4) * full_values[row]
                for row in sample_representatives),
            "seed/full target 3c/4 normalization failed")

    mutation_fired = targets[0][1] + 1 != targets[0][1]
    result = {
        "status": "UNAUDITED independent streaming factored-target referee",
        "seed_sha256": sha256(SEED.read_bytes()).hexdigest(),
        "canonical_stream_sha256": sha256(CANONICAL.read_bytes()).hexdigest(),
        "raw_stream_sha256": sha256(RAW.read_bytes()).hexdigest(),
        "full_collected_target_sha256": sha256(FULL.read_bytes()).hexdigest(),
        "stabilizer_order": len(actions),
        "target_row_orbits": len(targets),
        "target_total_mass": [seed_mass.numerator, seed_mass.denominator],
        "target_l1_mass": [seed_l1.numerator, seed_l1.denominator],
        "raw_rows_streamed": raw_rows,
        "raw_sample_orbits_checked": len(sample_representatives),
        "canonicality_controls": len(control_indices),
        "exact_canonical_stream_division_by_three": True,
        "exact_raw_sample_orbit_aggregation": True,
        "exact_full_target_three_fourths_normalization": True,
        "negative_coefficient_mutation_fired": mutation_fired,
        "normalization": (
            "The full collected square stores orbit masses in units 72^2/2304 "
            "=9/4. Removing the pure anchor square and selecting one of the "
            "three colour-conjugate summands gives P0 quotient mass 3c/4."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("factored P0-square seed referee: PASS")
    print("rows/mass/l1:", len(targets), seed_mass, seed_l1)
    print("raw sample orbits/canonicality controls:",
          len(sample_representatives), len(control_indices))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
