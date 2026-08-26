#!/usr/bin/env python3
"""Bounded dependency audit for the orbit-zero signed-Counter regression.

This does not recompute a Macaulay solve.  It replays the two small cutoff-7
checks without Counter's positive-part operator, reconstructs the cutoff-8
K8 residual before the offending cleanup, and pins the independent signed
R8' -> K14 -> literal-K16 chain by byte hash and provenance guards.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BRIDGE = ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
ANCHOR = ROOT / "computations/unaudited-codex-anchor-k-rust-2026-08-20"
T2 = ROOT / "computations/unaudited-codex-n8-orbit0-t2-graded-2026-08-20"
K14 = ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
K16 = ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
OUT = HERE / "results_signed_counter_dependency.json"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def digest(path: Path) -> str:
    state = sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            state.update(chunk)
    return state.hexdigest()


def contains_bytes(path: Path, needle: bytes) -> bool:
    carry = b""
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            block = carry + chunk
            if needle in block:
                return True
            carry = block[-len(needle):]
    return False


def raw_cutoff7_replay(matrix: Path, certificate: Path, fractional: bool):
    data = json.loads(certificate.read_text())
    if fractional:
        coefficients = {
            index: Fraction(numerator, denominator)
            for index, numerator, denominator in data["coefficients"]
        }
    else:
        coefficients = dict(data["solution"])
    replay = defaultdict(Fraction)
    with matrix.open() as stream:
        header = json.loads(next(stream))
        target = {
            row: Fraction(numerator, denominator)
            for row, numerator, denominator in header["target"]
        }
        for line in stream:
            column = json.loads(line)
            coefficient = coefficients.get(column["index"], 0)
            if coefficient:
                for row, value in column["entries"]:
                    replay[row] += coefficient * value
    replay = {row: value for row, value in replay.items() if value}
    require(replay == target, (matrix.name, "raw replay differs from target"))
    require(not any(value < 0 for value in replay.values()),
            (matrix.name, "raw replay has a negative coefficient"))
    return {
        "raw_nonzero_rows": len(replay),
        "raw_negative_rows": 0,
        "minimum_coefficient": str(min(replay.values())),
        "maximum_coefficient": str(max(replay.values())),
    }


def raw_cutoff8_residual():
    source = BRIDGE / "analyze_orbit0_cutoff8_leading_residual.py"
    spec = importlib.util.spec_from_file_location("cutoff8_bug_source", source)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    certificate = json.loads(module.CERTIFICATE.read_text())
    target = module.EXPORT.invariant_target(module.EXPORT.target_actual(9))
    residual = {
        row: Fraction(value)
        for row, value in target.items()
        if module.BASE.row_degree(row, module.EXPORT.ANCHORS) == 8
    }
    for term in certificate["terms"]:
        coefficient = Fraction(*term["coefficient"])
        word = tuple(map(int, term["word"]))
        multiplier = bytes(term["multiplier_cell_ids"])
        column = Counter()
        for output in module.BASE.column_rows((word, multiplier)):
            if module.BASE.row_degree(output, module.EXPORT.ANCHORS) == 8:
                column[module.IA.canonical_row(output)] += 1
        for row, value in column.items():
            updated = residual.get(row, 0) - coefficient * value
            if updated:
                residual[row] = updated
            else:
                residual.pop(row, None)
    positive = {row: value for row, value in residual.items() if value > 0}
    negative = {row: value for row, value in residual.items() if value < 0}
    frozen = json.loads((BRIDGE / "results_orbit0_cutoff8_leading_residual.json").read_text())
    frozen_rows = {bytes.fromhex(row): Fraction(n, d)
                   for row, n, d in frozen["residual"]}
    require(positive == frozen_rows, "frozen 301 rows are not exactly positive(raw)")
    require(len(residual) == 651 and len(positive) == 301 and len(negative) == 350,
            (len(residual), len(positive), len(negative)))
    return {
        "raw_nonzero_rows": len(residual),
        "raw_positive_rows": len(positive),
        "raw_negative_rows": len(negative),
        "raw_total_mass": str(sum(residual.values())),
        "deleted_negative_mass": str(sum(negative.values())),
        "minimum_coefficient": str(min(residual.values())),
        "maximum_coefficient": str(max(residual.values())),
        "frozen_is_exact_positive_part": True,
    }


def main() -> None:
    occurrence_sources = {
        "cutoff7_chart26": ANCHOR / "reconstruct_cutoff7_exact.py",
        "cutoff7_orbit0": ANCHOR / "verify_orbit0_cutoff7_exact_core.py",
        "dangerous_chart_degree2": BRIDGE / "audit_dangerous_charts.py",
        "cutoff8_positive_part": BRIDGE / "analyze_orbit0_cutoff8_leading_residual.py",
        "t2_positive_part": BRIDGE / "audit_orbit0_t2_pivot_setup.py",
    }
    counts = {
        name: path.read_text().count("+= Counter()")
        for name, path in occurrence_sources.items()
    }
    require(counts == {
        "cutoff7_chart26": 3,
        "cutoff7_orbit0": 2,
        "dangerous_chart_degree2": 2,
        "cutoff8_positive_part": 1,
        "t2_positive_part": 1,
    }, counts)

    cutoff7 = {
        "chart26": raw_cutoff7_replay(
            ANCHOR / "results_chart26_cutoff7_direct.jsonl",
            ANCHOR / "results_chart26_cutoff7_exact_core_certificate.json", True),
        "orbit0": raw_cutoff7_replay(
            ANCHOR / "results_orbit0_cutoff7_direct.jsonl",
            ANCHOR / "results_orbit0_cutoff7_exact_core_certificate.json", False),
    }
    cutoff8 = raw_cutoff8_residual()

    r8_path = BRIDGE / "results_orbit0_cutoff9_sparse_r8.json"
    r8 = json.loads(r8_path.read_text())
    masses = [Fraction(n, d) for _row, n, d in r8["residual"]]
    require(len(masses) == 120 and any(value < 0 for value in masses)
            and any(value > 0 for value in masses), "R8' ceased to be signed")
    require(sum(masses) == -23328, sum(masses))
    require("rebuild_r8(" not in
            (BRIDGE / "reconstruct_orbit0_cutoff9_sparse_r8.py").read_text(),
            "cutoff9 reconstruction started calling buggy rebuild_r8")

    r8_sha = digest(r8_path)
    require(r8_sha == "62013c8a8453ffe68e6ef08740859db6efecaf825f121c19dc885b6afa7feb4b",
            r8_sha)
    load_bearing = {
        "R8prime": r8_path,
        "chart_telescoping": T2 / "results_orbit0_chart_target_anchor_telescoping.json",
        "K14_interface": K14 / "results_orbit0_k14_interface.json",
        "literal_K16": K16 / "results_orbit0_k16_literal_residual.json",
    }
    for name in ("chart_telescoping", "K14_interface", "literal_K16"):
        require(contains_bytes(load_bearing[name], r8_sha.encode()),
                (name, "does not pin signed R8' byte hash"))
    require("+= Counter()" not in
            (K16 / "collect_orbit0_k16_literal_residual.py").read_text(),
            "literal K16 collector contains the offending idiom")

    invalid = {
        "cutoff8_positive_residual": BRIDGE / "results_orbit0_cutoff8_leading_residual.json",
        "t2_pivot_setup": BRIDGE / "results_orbit0_t2_pivot_setup.json",
        "r8_orbit_expansion": T2 / "results_r8_orbit_expansion.json",
        "r8_double_cosets": T2 / "results_r8_double_coset_count.json",
        "r8_square_unary": T2 / "results_r8_square_unary_packet_reduction.json",
        "r8_radical_seed": ROOT / "computations/unaudited-codex-orbit0-t2-radical-2026-08-20/results_r8_seed.json",
    }
    invalid_hashes = {name: digest(path) for name, path in invalid.items()}
    load_hashes = {name: digest(path) for name, path in load_bearing.items()}
    source_hashes = {name: digest(path) for name, path in occurrence_sources.items()}

    result = {
        "status": "PASS signed-Counter dependency/supersession audit",
        "counter_iadd_empty_occurrences": counts,
        "cutoff7_raw_replays": cutoff7,
        "cutoff8_raw_signed_residual": cutoff8,
        "classification": {
            "context_safe_occurrences": [
                "cutoff7_chart26 (raw replay independently nonnegative)",
                "cutoff7_orbit0 (raw replay independently nonnegative)",
                "dangerous_chart_degree2 (square system contains every supported d0/d2 row)"
            ],
            "unsound_occurrences": [
                "cutoff8_positive_part",
                "t2_positive_part"
            ],
            "invalid_artifacts": list(invalid),
            "load_bearing_chain": list(load_bearing),
        },
        "signed_R8prime": {
            "rows": len(masses),
            "positive_rows": sum(value > 0 for value in masses),
            "negative_rows": sum(value < 0 for value in masses),
            "total_mass": str(sum(masses)),
            "reconstruction_imports_buggy_module_for_helpers_only": True,
            "reconstruction_does_not_call_rebuild_r8": True,
        },
        "file_sha256": {
            "occurrence_sources": source_hashes,
            "invalid_artifacts": invalid_hashes,
            "load_bearing_chain": load_hashes,
        },
        "dependency_graph": [
            "cutoff8 exact 236-term raw certificate -> BUG positive K8 projection -> INVALID 301-row/T2 descendants",
            "cutoff9 two-prime core + literal source ledger -> safe signed 120-orbit R8prime",
            "signed R8prime -> chart telescoping -> K14 interface -> literal K16 collection",
        ],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("signed-Counter dependency audit: PASS")
    print("cutoff8 raw/positive/negative:", cutoff8["raw_nonzero_rows"],
          cutoff8["raw_positive_rows"], cutoff8["raw_negative_rows"])
    print("R8prime signed rows/mass:", len(masses), sum(masses))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
