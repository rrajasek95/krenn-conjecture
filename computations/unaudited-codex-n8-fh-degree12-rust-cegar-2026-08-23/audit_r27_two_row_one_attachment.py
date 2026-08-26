#!/usr/bin/env python3
"""One bounded attachment of the sparse r27 homology seed; no next shell."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
DRIVER_PATH = HERE / "run_fh_degree12_incremental.py"
HOMOLOGY = HERE / "results_r27_extended_dual_homology.json"
SHELL = HERE / "r27_selected_top_owner_core.txt"
CERTIFICATE = HERE / "r27_two_row_one_attachment.txt"
RESULT = HERE / "results_r27_two_row_one_attachment.json"
WALL_CAP_SECONDS = 300
EXPECTED_LOGICAL_SHA256 = "cb5d5fb70a8b70b32bd0928e504ceaf4f8d86720d81d3fec193c6ba817167da0"


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


def exact_solve(equations):
    """Sparse exact row echelon; return a free-zero particular solution."""
    pivots = {}
    for source, source_rhs, label in equations:
        vector = {index: Fraction(value) for index, value in source.items()
                  if value}
        rhs = Fraction(source_rhs)
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = 1 / value
                pivots[pivot] = (
                    {index: coefficient * inverse
                     for index, coefficient in vector.items()},
                    rhs * inverse,
                    label,
                )
                break
            basis, basis_rhs, _basis_label = pivots[pivot]
            for index, coefficient in basis.items():
                result = vector.get(index, Fraction(0)) - value * coefficient
                if result:
                    vector[index] = result
                else:
                    vector.pop(index, None)
            rhs -= value * basis_rhs
        if not vector and rhs:
            return None, {"label": label, "residual": [rhs.numerator,
                                                         rhs.denominator]}
    solution = {}
    for pivot in sorted(pivots, reverse=True):
        vector, rhs, _label = pivots[pivot]
        value = rhs - sum(coefficient * solution.get(index, Fraction(0))
                          for index, coefficient in vector.items()
                          if index != pivot)
        if value:
            solution[pivot] = value
    return solution, {"rank": len(pivots)}


def audit():
    started = monotonic()
    driver = load(DRIVER_PATH, "r27_attachment_driver")
    source_api, module = driver.ROOT_STAR.load_source()
    homology = json.loads(HOMOLOGY.read_text())
    detector = {
        bytes.fromhex(row_hex): Fraction(coefficient)
        for _row, row_hex, coefficient, _mu
        in homology["sparsest_target_coupled_class"]["detector_rows"]
    }
    require(len(detector) == 2 and set(detector.values()) == {Fraction(-1),
                                                               Fraction(1)},
            "two-row detector changed")
    owner_columns = {
        (record["word_code"], bytes.fromhex(record["multiplier_hex"]))
        for record in homology["first_escaping_external_columns"]
    }
    require(len(owner_columns) == 20, "escaping-owner attachment changed")

    shell_columns = set()
    for line in SHELL.read_text().splitlines():
        shell_columns.update(parse_column(field) for field in line.split()[2:])
    require(len(shell_columns) == 58_497, "frozen shell column census changed")
    round_rows = set(driver.load_rows_from(driver.ROUND_ROWS))

    escape_rows = set()
    owner_outputs = {}
    for column in owner_columns:
        entries = source_api.invariant_entries(module, column)
        owner_outputs[column] = entries
        escape_rows.update(row for row in entries if row not in round_rows)
    require(escape_rows, "20 owners lost their escaping outputs")
    ordered_escape_rows = tuple(sorted(escape_rows, key=lambda row: (-len(row), row)))
    escape_index = {row: index for index, row in enumerate(ordered_escape_rows)}

    support_probe = dict(detector)
    support_probe.update({row: Fraction(1) for row in escape_rows})
    incident = module.bounded_incident_columns(support_probe,
                                               maximum_output_degree=12)
    relevant_columns = sorted(incident & shell_columns)
    require(owner_columns <= set(relevant_columns),
            "attachment misses a named owner")

    equations = []
    for column in relevant_columns:
        entries = owner_outputs.get(column)
        if entries is None:
            entries = source_api.invariant_entries(module, column)
        vector = {escape_index[row]: coefficient
                  for row, coefficient in entries.items()
                  if row in escape_index}
        detector_pairing = sum(coefficient * detector.get(row, Fraction(0))
                               for row, coefficient in entries.items())
        if vector or detector_pairing:
            equations.append((vector, -detector_pairing, column_text(column)))
    solution, solve_record = exact_solve(equations)

    if solution is None:
        status = "DIES_ON_FIRST_ATTACHMENT"
        attached = dict(detector)
        integer_attached = None
        next_columns = set()
    else:
        attached = dict(detector)
        attached.update({ordered_escape_rows[index]: value
                         for index, value in solution.items() if value})
        for column in relevant_columns:
            entries = owner_outputs.get(column)
            if entries is None:
                entries = source_api.invariant_entries(module, column)
            require(sum(Fraction(coefficient) * attached.get(row, Fraction(0))
                        for row, coefficient in entries.items()) == 0,
                    "attached functional misses a frozen-shell column")
        denominator = lcm(*(value.denominator for value in attached.values()))
        integer_attached = {row: int(value * denominator)
                            for row, value in attached.items()}
        divisor = 0
        for value in integer_attached.values():
            divisor = gcd(divisor, abs(value))
        require(divisor, "attached functional vanished")
        integer_attached = {row: value // divisor
                            for row, value in integer_attached.items()}
        first_value = integer_attached[min(integer_attached)]
        if first_value < 0:
            integer_attached = {row: -value
                                for row, value in integer_attached.items()}
        # Count, but deliberately do not expand, the next external column shell.
        next_columns = (module.bounded_incident_columns(
            integer_attached, maximum_output_degree=12) - shell_columns)
        status = ("MIGRATES_SPARSE_EXACT_Z" if len(integer_attached) <= 64
                  else "MIGRATES_WITH_SUPPORT_EXPLOSION")

    certificate_lines = [
        f"STATUS {status}",
        f"DETECTOR_SUPPORT {len(detector)}",
        f"ATTACHMENT_OWNERS {len(owner_columns)}",
        f"ESCAPE_ROWS {len(escape_rows)}",
        f"RELEVANT_FROZEN_COLUMNS {len(relevant_columns)}",
        f"EQUATIONS {len(equations)}",
    ]
    if integer_attached is not None:
        certificate_lines.append(f"ATTACHED_SUPPORT {len(integer_attached)}")
        certificate_lines.append(f"NEXT_UNEXPANDED_COLUMNS {len(next_columns)}")
        certificate_lines.extend(
            f"VALUE {row.hex()} {value}"
            for row, value in sorted(integer_attached.items())
        )
    else:
        certificate_lines.append("INCONSISTENT " + json.dumps(
            solve_record, sort_keys=True, separators=(",", ":")))
    CERTIFICATE.write_text("\n".join(certificate_lines) + "\n")

    result = {
        "format": "n8-fh-d12-r27-two-row-one-attachment-v1",
        "status": status,
        "scope": (
            "one exact attachment through the 20 named escaping owner columns; "
            "all frozen-shell columns incident to the collected output rows are "
            "imposed; any next columns are counted but never expanded"
        ),
        "input": {
            "detector_support": len(detector),
            "escaping_owner_columns": len(owner_columns),
            "collected_escape_rows": len(escape_rows),
            "relevant_frozen_shell_columns": len(relevant_columns),
            "equations": len(equations),
        },
        "solve": solve_record,
        "output": ({
            "exact_integer_support": len(integer_attached),
            "coefficient_maximum_absolute": max(map(abs,
                                                      integer_attached.values())),
            "next_external_column_orbits_unexpanded": len(next_columns),
            "integer_functional": [[row.hex(), value]
                                   for row, value in sorted(
                                       integer_attached.items())],
        } if integer_attached is not None else None),
        "certificate_file": CERTIFICATE.name,
        "certificate_sha256": sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "elapsed_seconds_nonlogical": monotonic() - started,
        "theorem": (
            "The exact terminal status states whether the canonical two-row "
            "class dies or migrates after precisely one frozen-shell attachment; "
            "no inference is made about the counted unexpanded next shell."
        ),
    }
    logical_payload = dict(result)
    logical_payload.pop("elapsed_seconds_nonlogical")
    encoded = json.dumps(logical_payload, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "one-attachment result changed")
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("ATTACHMENT", status, result["input"], result["solve"])
    if result["output"]:
        print("OUTPUT", result["output"]["exact_integer_support"],
              result["output"]["coefficient_maximum_absolute"],
              result["output"]["next_external_column_orbits_unexpanded"])
    print("logical", result["logical_sha256"])
    return result


if __name__ == "__main__":
    audit()
