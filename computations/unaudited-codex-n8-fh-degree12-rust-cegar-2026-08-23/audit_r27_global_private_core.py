#!/usr/bin/env python3
"""Global-owner referee for the packet-private r27 degree-12 rows."""

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
DRIVER_PATH = HERE / "run_fh_degree12_incremental.py"
STRUCTURE = HERE / "results_r27_pending_structure.json"
COUNTEROWNERS = HERE / "r27_private_counterowners.txt"
CORE = HERE / "r27_selected_top_owner_core.txt"
RESULT = HERE / "results_r27_global_private_core.json"
WALL_CAP_SECONDS = 300
EXPECTED_LOGICAL_SHA256 = "2b31f4252eb46d51bd81c31b9c4e585fec2a27e596f32bdf5f580039246705b7"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def column_text(column):
    return f"{column[0]}:{column[1].hex()}"


def first_alternative_owner(module, row, expected):
    """Return a literal distinct homogeneous-D12 owner, stopping immediately."""
    for size in range(min(4, len(row)) + 1):
        seen_terms = set()
        for positions in combinations(range(len(row)), size):
            selected = set(positions)
            term = bytes(row[position] for position in positions)
            if term in seen_terms:
                continue
            seen_terms.add(term)
            multiplier = bytes(row[position] for position in range(len(row))
                               if position not in selected)
            if len(multiplier) > 8:
                continue
            for code in module.codes_for_normalized_term(term):
                owner = module.canonical_normalized_column((code, multiplier))
                if owner != expected:
                    return owner
    return None


def counter_record(counter):
    return [[str(key), value] for key, value in sorted(
        counter.items(), key=lambda item: str(item[0]))]


def audit():
    started = monotonic()
    driver = load(DRIVER_PATH, "r27_global_driver")
    source_api, module = driver.ROOT_STAR.load_source()
    checkpoint = json.loads(driver.CHECKPOINT.read_text())
    pending = sorted(driver.parse_column(record)
                     for record in checkpoint["pending_columns"])
    pending_set = set(pending)
    old_rows = set(driver.load_rows())
    require(len(pending) == 7_316 and len(old_rows) == 1_473_022,
            "r27 global-owner interface changed")

    row_counts = {}
    for index, column in enumerate(pending, 1):
        for row in source_api.invariant_entries(module, column):
            if row not in old_rows:
                row_counts[row] = row_counts.get(row, 0) + 1
        if index % 1024 == 0:
            print("COUNT", index, "/", len(pending), flush=True)
    require(len(row_counts) == 524_268
            and sum(value == 1 for value in row_counts.values()) == 447_520,
            "packet-private row census changed")

    counter_digest = sha256()
    alternative_profiles = Counter()
    private_rows_per_column = Counter()
    globally_private_rows = []
    columns_with_global_private = set()
    examples = []
    with COUNTEROWNERS.open("w", encoding="ascii") as output:
        for column_id, column in enumerate(pending):
            local_private = 0
            for row in source_api.invariant_entries(module, column):
                if row_counts.get(row) != 1:
                    continue
                local_private += 1
                alternative = first_alternative_owner(module, row, column)
                if alternative is None:
                    globally_private_rows.append((column, row))
                    columns_with_global_private.add(column)
                    continue
                profile = tuple(sorted(Counter(
                    module.D5.decode_word(alternative[0])).values(), reverse=True))
                alternative_profiles[profile] += 1
                line = (f"{row.hex()} {column_text(column)} "
                        f"{column_text(alternative)}\n")
                output.write(line)
                counter_digest.update(line.encode("ascii"))
                if len(examples) < 64:
                    examples.append(line.strip().split())
            private_rows_per_column[local_private] += 1
            if (column_id + 1) % 512 == 0:
                print("GLOBAL", column_id + 1, "/", len(pending),
                      "global_private", len(globally_private_rows),
                      "elapsed", round(monotonic() - started, 3), flush=True)
            require(monotonic() - started < WALL_CAP_SECONDS,
                    "global-private audit exceeded 300 seconds")
    require(sum(key * value for key, value in private_rows_per_column.items())
            == 447_520, "private-row distribution lost rows")

    # Complete owner lists for the canonical selected +1 top witness of each
    # crossing column.  These rows form a small literal residual owner shell.
    structure = json.loads(STRUCTURE.read_text())
    witnesses = structure["private_row_certificate"]["witnesses"]
    require(len(witnesses) == len(pending), "selected witness census changed")
    owner_histogram = Counter()
    extra_owners = set()
    core_digest = sha256()
    core_edges = 0
    with CORE.open("w", encoding="ascii") as output:
        for witness in witnesses:
            row = bytes.fromhex(witness["private_row_hex"])
            expected = (witness["word_code"],
                        bytes.fromhex(witness["multiplier_hex"]))
            owners = tuple(sorted(module.top_incident_columns(row)))
            require(expected in owners and len(owners) >= 2,
                    "selected row lost its global owner collision")
            owner_histogram[len(owners)] += 1
            extra_owners.update(set(owners) - pending_set)
            core_edges += len(owners)
            line = (row.hex() + " " + column_text(expected) + " "
                    + " ".join(column_text(owner) for owner in owners) + "\n")
            output.write(line)
            core_digest.update(line.encode("ascii"))
    require(sum(owner_histogram.values()) == 7_316,
            "selected owner-shell row census changed")

    result = {
        "format": "n8-fh-d12-r27-global-private-core-v1",
        "status": "PASS_GLOBAL_PRIVATE_SHORTCUT_FAILS",
        "scope": (
            "complete homogeneous-D12 owner audit of every row private to the "
            "7,316-column r27 packet relative to accepted r26; no elimination"
        ),
        "packet": {
            "columns": 7_316, "new_rows": 524_268,
            "packet_private_rows": 447_520,
            "columns_with_packet_private_row": 7_316,
        },
        "global_referee": {
            "globally_private_rows": len(globally_private_rows),
            "columns_with_globally_private_row": len(columns_with_global_private),
            "private_rows_per_column": counter_record(private_rows_per_column),
            "alternative_owner_word_profiles": counter_record(alternative_profiles),
            "counterowner_file": COUNTEROWNERS.name,
            "counterowner_sha256": counter_digest.hexdigest(),
            "first_examples": examples,
        },
        "selected_top_residual_owner_shell": {
            "rows": 7_316, "incidence_edges": core_edges,
            "owner_count_histogram": counter_record(owner_histogram),
            "extra_column_orbits_beyond_r27": len(extra_owners),
            "extra_columns": [[code, multiplier.hex()]
                              for code, multiplier in sorted(extra_owners)],
            "file": CORE.name,
            "sha256": core_digest.hexdigest(),
        },
        "theorem": (
            "Packet-relative leaves prove r27 independence, but none of the "
            "447,520 leaf rows is globally private: each has a literal distinct "
            "homogeneous-D12 owner.  Therefore the proposed independent global "
            "dual correction fails, with the selected 7,316-row owner shell "
            "exported as the finite first collision core."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "global-private result changed")
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("GLOBAL_PRIVATE", len(globally_private_rows),
          "EXTRA", len(extra_owners), "EDGES", core_edges)
    print("logical", result["logical_sha256"])
    return result


if __name__ == "__main__":
    audit()
