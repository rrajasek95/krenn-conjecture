#!/usr/bin/env python3
"""Locate the r26->r27 corrected dual in the exact owner-core homology."""

from collections import defaultdict, deque
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
DRIVER_PATH = HERE / "run_fh_degree12_incremental.py"
RUST_CHECKPOINT = HERE / "checkpoint_fh_degree12_rust_cegar.json"
STRUCTURE = HERE / "results_r27_pending_structure.json"
SHELL = HERE / "r27_selected_top_owner_core.txt"
CORE = HERE / "r27_selected_owner_2core.txt"
CERTIFICATE = HERE / "r27_sparse_homology_seed.txt"
RESULT = HERE / "results_r27_extended_dual_homology.json"
PRIME = 1_073_741_827
WALL_CAP_SECONDS = 300
EXPECTED_LOGICAL_SHA256 = "701d9d866b1ab8cfdf13d52bd3a6b2e8ea340220403249f5ea07a8760ede35f9"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def parse_column(text):
    code, multiplier = text.split(":")
    return int(code), bytes.fromhex(multiplier)


def column_text(column):
    return f"{column[0]}:{column[1].hex()}"


def audit():
    started = monotonic()
    driver = load(DRIVER_PATH, "r27_homology_driver")
    source_api, module = driver.ROOT_STAR.load_source()
    checkpoint = json.loads(RUST_CHECKPOINT.read_text())
    require(checkpoint["ledger"][-1]["round"] == 26
            and checkpoint["ledger"][-1]["target_pairing_mod_prime"] == 1
            and len(checkpoint["last_dual"]) == 4_128,
            "stored r26 dual changed")
    lambda26 = {bytes.fromhex(row): value
                for row, value in checkpoint["last_dual"]}
    structure = json.loads(STRUCTURE.read_text())
    witnesses = structure["private_row_certificate"]["witnesses"]
    require(len(witnesses) == 7_316, "r27 private witness packet changed")

    pure_terms = tuple(tuple(sorted(
        module.normalized_generator(module.D5.word_code((colour,) * 8)).items(),
        key=lambda item: (len(item[0]), item[0]))) for colour in range(3))

    @lru_cache(None)
    def coefficient_fh(row, colours=(0, 1, 2)):
        if not colours:
            return int(not row)
        total = 0
        for term, coefficient in pure_terms[colours[0]]:
            if len(term) > len(row):
                break
            quotient = driver.ROOT_STAR.quotient_if_divides(row, term)
            if quotient is not None:
                total += coefficient * coefficient_fh(quotient, colours[1:])
        return total

    extended = dict(lambda26)
    correction = []
    r27_columns = set()
    correction_histogram = defaultdict(int)
    target_coefficient_histogram = defaultdict(int)
    target_delta = 0
    for index, witness in enumerate(witnesses):
        column = (witness["word_code"], bytes.fromhex(witness["multiplier_hex"]))
        private_row = bytes.fromhex(witness["private_row_hex"])
        entries = source_api.invariant_entries(module, column)
        old_pairing = sum(coefficient * lambda26.get(row, 0)
                          for row, coefficient in entries.items()) % PRIME
        target_coefficient = coefficient_fh(private_row)
        require(old_pairing and entries[private_row] == 1
                and private_row not in lambda26,
                "r27 private correction hypotheses changed")
        value = (-old_pairing) % PRIME
        extended[private_row] = value
        correction.append(value)
        correction_histogram[value] += 1
        target_coefficient_histogram[target_coefficient] += 1
        target_delta = (target_delta + value * target_coefficient) % PRIME
        r27_columns.add(column)
        if (index + 1) % 1024 == 0:
            print("CORRECT", index + 1, "/", len(witnesses), flush=True)
    require(len(extended) == 4_128 + 7_316,
            "extended dual support collided")
    for index, witness in enumerate(witnesses):
        column = (witness["word_code"], bytes.fromhex(witness["multiplier_hex"]))
        entries = source_api.invariant_entries(module, column)
        pairing = sum(coefficient * extended.get(row, 0)
                      for row, coefficient in entries.items()) % PRIME
        require(pairing == 0, "private correction misses an r27 column")
    extended_target_pairing = (1 + target_delta) % PRIME

    row_hexes = []
    owner_lists = []
    column_ids = {}
    columns = []
    for line in SHELL.read_text().splitlines():
        fields = line.split()
        row_hexes.append(fields[0])
        owners = [parse_column(field) for field in fields[2:]]
        owner_lists.append(owners)
        for owner in owners:
            if owner not in column_ids:
                column_ids[owner] = len(columns)
                columns.append(owner)
    require(len(row_hexes) == 7_316 and len(columns) == 58_497,
            "selected shell encoding changed")

    core_column_rows = defaultdict(dict)
    core_rows = set()
    for line in CORE.read_text().splitlines():
        fields = line.split()
        row, column, coefficient = map(int, fields[:3])
        require(coefficient == 1, "core coefficient changed")
        core_column_rows[column][row] = coefficient
        core_rows.add(row)
    require(len(core_rows) == 3_942 and len(core_column_rows) == 7_180,
            "owner 2-core changed")

    # Degree-two sign propagation realizes the exact 764-dimensional left
    # obstruction.  Components untouched by collapsed hyperedges already give
    # sparse integral null vectors.
    adjacency = defaultdict(list)
    for vector in core_column_rows.values():
        if len(vector) == 2:
            first, second = vector
            adjacency[first].append(second)
            adjacency[second].append(first)
    colour = {}
    parameter_vertices = []
    row_parameter = {}
    for seed in sorted(core_rows):
        if seed in colour:
            continue
        colour[seed] = 1
        queue = deque((seed,))
        vertices = []
        odd = False
        while queue:
            row = queue.popleft()
            vertices.append(row)
            for other in adjacency[row]:
                if other not in colour:
                    colour[other] = -colour[row]
                    queue.append(other)
                elif colour[other] != -colour[row]:
                    odd = True
        if not odd:
            parameter = len(parameter_vertices)
            parameter_vertices.append(vertices)
            for row in vertices:
                row_parameter[row] = parameter
    require(len(parameter_vertices) == 1_168,
            "degree-two free-parameter count changed")
    touched_parameters = set()
    for vector in core_column_rows.values():
        if len(vector) <= 2:
            continue
        collapsed = defaultdict(int)
        for row, coefficient in vector.items():
            if row in row_parameter:
                collapsed[row_parameter[row]] += coefficient * colour[row]
        for parameter, coefficient in collapsed.items():
            if coefficient:
                touched_parameters.add(parameter)
    isolated_parameters = set(range(len(parameter_vertices))) - touched_parameters
    require(len(isolated_parameters) == 619,
            "isolated sign-parameter count changed")

    candidates = []
    for parameter in isolated_parameters:
        vertices = parameter_vertices[parameter]
        detector = {row: colour[row] for row in vertices}
        pairing = sum(value * correction[row] for row, value in detector.items()) % PRIME
        if pairing:
            key = (len(detector), tuple(sorted(
                (row_hexes[row], value) for row, value in detector.items())))
            candidates.append((key, detector, pairing, parameter))
    require(candidates, "extended dual class vanished on sparse obstruction")
    candidates.sort(key=lambda item: item[0])
    _key, detector, detector_pairing, parameter = candidates[0]
    require(len(detector) == 2,
            "sparsest target-coupled obstruction changed support")
    for column, vector in core_column_rows.items():
        require(sum(detector.get(row, 0) * coefficient
                    for row, coefficient in vector.items()) == 0,
                "sparse detector misses a core column")
    require(all(vector for vector in core_column_rows.values()),
            "core acquired a zero column")

    core_crossings = []
    for column_index in sorted(core_column_rows):
        column = columns[column_index]
        entries = source_api.invariant_entries(module, column)
        pairing = sum(coefficient * extended.get(row, 0)
                      for row, coefficient in entries.items()) % PRIME
        if pairing:
            core_crossings.append((column_index, column, pairing))

    round_rows = set(driver.load_rows_from(driver.ROUND_ROWS))
    escaping = []
    detector_rows = set(detector)
    detector_owner_columns = set()
    for row in detector_rows:
        detector_owner_columns.update(owner_lists[row])
    for column in sorted(detector_owner_columns - r27_columns):
        entries = source_api.invariant_entries(module, column)
        outside = sorted(row for row in entries if row not in round_rows)
        if outside:
            pairing = sum(coefficient * extended.get(row, 0)
                          for row, coefficient in entries.items()) % PRIME
            escaping.append({
                "word_code": column[0], "multiplier_hex": column[1].hex(),
                "extended_dual_pairing_mod_prime": pairing,
                "escaping_rows": len(outside),
                "first_escaping_row_hex": outside[0].hex(),
            })
    require(escaping, "sparse obstruction lost its escaping external columns")

    detector_record = [[row, row_hexes[row], detector[row], correction[row]]
                       for row in sorted(detector)]
    certificate_lines = [
        f"PRIME {PRIME}",
        f"R26_DUAL_SUPPORT {len(lambda26)}",
        f"R27_CORRECTIONS {len(correction)}",
        f"EXTENDED_TARGET_PAIRING {extended_target_pairing}",
        f"CORE_ROWS {len(core_rows)} CORE_COLUMNS {len(core_column_rows)}",
        f"LEFT_NULLITY 764",
        f"SPARSE_PARAMETER {parameter}",
        f"CLASS_PAIRING {detector_pairing}",
    ]
    certificate_lines.extend(
        f"DETECTOR {row} {row_hex} {coefficient} MU {mu}"
        for row, row_hex, coefficient, mu in detector_record)
    certificate_lines.extend(
        "ESCAPE " + str(record["word_code"]) + ":"
        + record["multiplier_hex"] + " "
        + str(record["extended_dual_pairing_mod_prime"]) + " "
        + record["first_escaping_row_hex"]
        for record in escaping[:32])
    CERTIFICATE.write_text("\n".join(certificate_lines) + "\n")

    result = {
        "format": "n8-fh-d12-r27-extended-dual-homology-v1",
        "status": ("PASS_NONZERO_SPARSE_TARGET_COUPLED_CORE_CLASS"
                   if extended_target_pairing else
                   "PASS_SPARSE_CORE_CLASS_BUT_SELECTED_EXTENSION_LOST_TARGET"),
        "scope": (
            "stored p=1073741827 r26 dual, its unique selected-private-row "
            "extension across r27, and the frozen selected-owner 2-core only; "
            "no exact-Q lift, second-shell expansion, or saturation inference"
        ),
        "extended_dual": {
            "r26_support": len(lambda26),
            "private_corrections": len(correction),
            "support": len(extended),
            "target_pairing_mod_prime": extended_target_pairing,
            "all_r27_columns_annihilated": True,
            "correction_row_target_coefficients": [[str(key), value]
                                                    for key, value in sorted(
                                                        target_coefficient_histogram.items())],
            "correction_value_histogram": [[str(key), value]
                                           for key, value in sorted(
                                               correction_histogram.items())],
        },
        "core_restriction": {
            "rows": len(core_rows), "columns": len(core_column_rows),
            "left_obstruction_dimension": 764,
            "core_crossings_after_extension": len(core_crossings),
            "core_crossing_digest": sha256(json.dumps([
                [index, column[0], column[1].hex(), pairing]
                for index, column, pairing in core_crossings
            ], separators=(",", ":")).encode("ascii")).hexdigest(),
        },
        "sparsest_target_coupled_class": {
            "support": len(detector),
            "minimality": (
                "support one is impossible because every active core row is "
                "incident to a coefficient-one core column"
            ),
            "selection": (
                "lexicographically least normalized-row record among all "
                "minimum-support isolated sign parameters with nonzero pairing"
            ),
            "parameter": parameter,
            "detector_rows": detector_record,
            "annihilates_all_core_columns_over_Z": True,
            "pairing_with_extended_correction_mod_prime": detector_pairing,
            "target_coupled_is_nonzero": bool(extended_target_pairing),
        },
        "first_escaping_external_columns": escaping[:32],
        "escaping_external_columns_incident_to_detector": len(escaping),
        "certificate_file": CERTIFICATE.name,
        "certificate_sha256": sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "theorem": (
            "The packet-private extension of the stored r26 modular dual has "
            "a nonzero class in the exact 764-dimensional integer left "
            "obstruction.  Its lexicographically canonical sparsest detector "
            "has two rows with opposite signs; support one is impossible.  The "
            "exported external owners show where this class first escapes, "
            "without expanding the second shell.  Target coupling is stated "
            "only by the audited post-correction modular target pairing."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "extended-dual homology result changed")
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("EXTENDED", len(extended), "CORE_CROSSINGS", len(core_crossings))
    print("SPARSE", detector_record, "PAIRING", detector_pairing,
          "ESCAPES", len(escaping))
    print("logical", result["logical_sha256"])
    return result


if __name__ == "__main__":
    audit()
