#!/usr/bin/env python3
"""Independent K18 prefix/assembly referee; does not rerun the 6.23M pass."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NEW_DIR = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k18-complete-charge-2026-08-23"
NEW = NEW_DIR / "results_missing_k18_22_charge.json"
COMPLETE = NEW_DIR / "results_complete_k18_charge.json"
SOURCE = NEW_DIR / "run_full_hidden_k2_charge.rs"
ASSEMBLER = NEW_DIR / "assemble_complete_k18_charge.py"
OLD = ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
K2 = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/k18_k2_canonical_prefix.bin"
CYCLE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin"
K19_REF = ROOT / "computations/unaudited-codex-orbit0-hidden-children-prefix-referee-2026-08-23/results_hidden_children_prefix_referee.json"
OUT = HERE / "results_complete_k18_charge_referee.json"
U = 400_591_699_200


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def frac(record):
    return Fraction(record["numerator"], record["denominator"])


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def cycle_data():
    data = CYCLE.read_bytes()
    require(data[:8] == b"K17CYC1\0", data[:8])
    pos = 8
    cells = []
    for _ in range(252):
        cells.append(tuple(data[pos:pos + 4]))
        pos += 4
    n = int.from_bytes(data[pos:pos + 4], "little")
    pos += 4
    dual = {}
    for _ in range(n):
        key = bytes(data[pos:pos + 13])
        value = int.from_bytes(data[pos + 13:pos + 21], "little", signed=True)
        pos += 21
        dual[key] = value
    require(pos == len(data), (pos, len(data)))
    return cells, dual


def cycle_key(row, cells):
    adjacency = [[] for _ in range(24)]
    for cell in row:
        u, v, a, b = cells[cell]
        left, right = 3 * u + a, 3 * v + b
        adjacency[left].append(right)
        adjacency[right].append(left)
    require(all(len(x) == 2 for x in adjacency), row.hex())
    seen = set()
    parts = []
    for start in range(24):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            node = stack.pop()
            size += 1
            for other in adjacency[node]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        parts.append(size)
    parts.sort()
    return bytes([len(parts), *parts, *([0] * (12 - len(parts)))])


def replay_prefix():
    cells, dual = cycle_data()
    data = K2.read_bytes()
    require(data[:8] == b"H18K2P1\0" and
            int.from_bytes(data[8:24], "little", signed=True) == U, data[:24])
    n = int.from_bytes(data[48:56], "little")
    require((n, int.from_bytes(data[56:58], "little"), len(data)) ==
            (694_172, 76, 64 + 76 * 694_172), (n, len(data)))
    full = irreducible = 0
    pivotable = 0
    prior = None
    for rec in (data[64 + 76 * i:64 + 76 * (i + 1)] for i in range(n)):
        row = bytes(rec[:24])
        require(prior is None or prior < row, row.hex())
        prior = row
        weight = int.from_bytes(rec[24:40], "little", signed=True)
        stored_pivotable = bool(rec[40])
        pivotable += stored_pivotable
        q = dual.get(cycle_key(row, cells), 0)
        full += weight * q
        if not stored_pivotable:
            irreducible += weight * q
    return {"rows": n, "pivotable": pivotable,
            "full_scaled": full, "irreducible_scaled": irreducible}


def main():
    new = json.loads(NEW.read_text())
    complete = json.loads(COMPLETE.read_text())
    old = json.loads(OLD.read_text())
    dag = json.loads(DAG.read_text())
    k19 = json.loads(K19_REF.read_text())
    require(new["status"] == "PASS_FULL_MISSING_K18_22_IMMEDIATE_CHARGE", new["status"])
    require(complete["status"] == "PASS_COMPLETE_K18_PATH_CHARGE_ASSEMBLY", complete["status"])
    prefix = replay_prefix()
    expected_prefix = new["literal_prefix_guard"]
    require(prefix == {
        "rows": expected_prefix["canonical_rows"],
        "pivotable": expected_prefix["canonical_pivotable_rows"],
        "full_scaled": int(expected_prefix["full_charge_scaled"]),
        "irreducible_scaled": int(expected_prefix["irreducible_charge_scaled"]),
    }, (prefix, expected_prefix))

    hidden_full = Fraction(int(new["full_charge_scaled"]), U)
    hidden_irr = Fraction(int(new["irreducible_charge_scaled"]), U)
    require(hidden_irr == Fraction(41_042_551_470_843_904, 24_838_275), hidden_irr)
    old_full = frac(old["total"]["full_charge"])
    old_irr = frac(old["total"]["K18_irreducible_charge"])
    total_full, total_irr = old_full + hidden_full, old_irr + hidden_irr
    require(total_irr == Fraction(109_863_564_487_489_024, 24_838_275), total_irr)
    require(total_full == frac(complete["K18"]["corrected_complete_17_path_total"]["full"]) and
            total_irr == frac(complete["K18"]["corrected_complete_17_path_total"]["irreducible"]),
            (total_full, total_irr))
    required = set(dag["required_reachable_lineage_ids_by_degree"]["18"])
    covered = {x for rows in complete["dag_coverage"]["component_to_lineages"].values()
               for x in rows}
    require(required == covered and len(required) == 17, (required ^ covered, len(required)))

    complete_k19 = Fraction(k19["full_hidden_charge"]["corrected_K19_aggregate"])
    cumulative = (Fraction(375_127_296) -
                  Fraction(9_747_200_926_208, 6_545) + total_irr + complete_k19)
    require(cumulative == Fraction(-514_174_021_726_888_448, 57_955_975), cumulative)

    result = {
        "status": "PASS_INDEPENDENT_COMPLETE_K18_CHARGE_REFEREE",
        "scope": ("Independent literal replay of the complete Cycle prefix, exact source/"
                  "DAG/arithmetic audit of the full profile result; no duplicate 6.23M pass "
                  "and no K18 row/later-tail claim."),
        "prefix_independent_cycle_replay": prefix,
        "missing_path_22": {"full": str(hidden_full), "irreducible": str(hidden_irr)},
        "complete_K18_irreducible": str(total_irr),
        "covered_K18_lineages": len(required),
        "complete_K19_irreducible": str(complete_k19),
        "cumulative_K14_through_K19": str(cumulative),
        "required_compensating_K20_through_K24": str(-cumulative),
        "K20_scope": "Incomplete; only hidden path [2,4] has been repaired.",
        "pinned": {str(path.relative_to(ROOT)): digest(path) for path in
                   (NEW, COMPLETE, SOURCE, ASSEMBLER, OLD, DAG, K2, CYCLE, K19_REF)},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
