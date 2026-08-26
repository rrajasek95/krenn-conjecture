#!/usr/bin/env python3
"""Independent one-pass byte/structure replay of the combined exact16 CNF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CONJECTURE = Path("/Users/rishi/workplace/krenn-conjecture")
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
MATERIALIZER = CONJECTURE / "computations/unaudited-codex-n8-x5-combined-exact16-streaming-materializer-held-2026-08-26"
PATCH_PACKAGE = CONJECTURE / "computations/unaudited-codex-n8-x5-eight-nine-exact16-selector-patch-held-2026-08-26"
TERMINAL = CROSS / "docs/audits/eight-vertex-degree4-exact16-target-union-terminal-unsat-2026-08-26"

BASE = CROSS / "tmp/eight_vertex_local_degree4_full_local_max16_current.cnf"
OUTPUT = CROSS / "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_target_union_current.cnf"
BUILD = Path(str(OUTPUT) + ".build.json")
PATCH = PATCH_PACKAGE / "selector_patch.cnfpart"
LEDGER = PATCH_PACKAGE / "combined_target_supports.ledger"

BASE_HEADER = b"p cnf 428247 3083172\n"
OUTPUT_HEADER = b"p cnf 464139 3980473\n"
BASE_SHA256 = "9e057710afe016609c31ae4c0cb45b1a948ca48b74426d390a2a9209035dd547"
OUTPUT_SHA256 = "c96d4ac1ac70abd8bfcf3b2b7228a94963a8c0fc52c8a891e502122be857da12"
PATCH_SHA256 = "2ac0e05c9599f09066fc6b0bdd5812ac78e85328ec3928ef3f3f6498e7af2059"
PATCH_MANIFEST_SHA256 = "745f5fa186c05d265cb521bfbf1f3c9d485ac3779a7cfbee82cbdfc50c68eee8"
MATERIALIZER_MANIFEST_SHA256 = "cf720d0e1d8516f9f5a942be72bc20de5e14104eb9832607472385f7c9733f37"
CLEARANCE_SHA256 = "477098f5fb987dba245da3ff2db0ec994c6e33da17e9fa5b32209027bb1419e9"
TERMINAL_MANIFEST_SHA256 = "bcd2cc5f92bd2ddb7e52decfc65b68e430b2312281d5b1d181fa639c35d6416e"
TERMINAL_RESULT_SHA256 = "3264b7a8ae5a40c6c3cfb42f5fc4b19bd5193efcd39777782dae579b4db67808"
BUILD_SHA256 = "e68b8d0b547e14662e7b771e44f5bb3bf4d2ea720b8d23d7b95a86a4a96bcd0e"
LEDGER_SHA256 = "6bffb2962242725f8bd0603dfaeb91f64c2ee0e4430632b445b42e44d4a424d5"

BASE_BYTES = 231_480_677
OUTPUT_BYTES = 244_617_151
PATCH_BYTES = 13_136_474
BASE_CLAUSES = 3_083_172
PATCH_CLAUSES = 897_301
OUTPUT_CLAUSES = 3_980_473
FIRST_SELECTOR = 428_248
LAST_SELECTOR = 464_139

EDGES = (
    "01", "02", "03", "04", "12", "13", "14", "15", "16", "17",
    "23", "24", "25", "26", "27", "34", "35", "36", "37", "45",
    "46", "47", "56", "57", "67",
)
BLOCK_VAR = dict(zip(EDGES, range(226, 251), strict=True))


def need(value, detail):
    if not value:
        raise RuntimeError(detail)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


class ClauseReplay:
    def __init__(self):
        self.buffer = b""
        self.lines = 0
        self.max_variable = 0

    def feed(self, chunk: bytes):
        data = self.buffer + chunk
        pieces = data.split(b"\n")
        self.buffer = pieces.pop()
        for line in pieces:
            need(line, ("empty clause line", self.lines + 1))
            tokens = line.split()
            need(tokens and tokens[-1] == b"0", ("unterminated clause", self.lines + 1))
            need(b"0" not in tokens[:-1], ("interior zero", self.lines + 1))
            try:
                literals = tuple(map(int, tokens[:-1]))
            except ValueError as exc:
                raise RuntimeError(("noninteger clause", self.lines + 1)) from exc
            need(literals, ("empty DIMACS clause", self.lines + 1))
            local_max = max(map(abs, literals))
            need(local_max <= 464_139, ("variable out of range", self.lines + 1, local_max))
            self.max_variable = max(self.max_variable, local_max)
            self.lines += 1

    def finish(self):
        need(not self.buffer, ("missing terminal newline", self.buffer[:80]))


def parse_ledger():
    raw = LEDGER.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == LEDGER_SHA256, "ledger hash")
    need(raw.endswith(b"\n"), "ledger newline")
    lines = raw.decode("ascii").splitlines()
    need(len(lines) == 35_892 and lines == sorted(lines) and len(set(lines)) == 35_892, "ledger census")
    supports = []
    for index, line in enumerate(lines):
        support = tuple(line.split("|"))
        need(len(support) == 16 and support == tuple(sorted(support)) and len(set(support)) == 16,
             ("support form", index))
        need(set(support) <= set(EDGES) and set(support) >= {"01", "02", "03", "04"},
             ("support universe", index))
        supports.append(support)
    return supports


def replay_patch_semantics(supports):
    patch_hash = hashlib.sha256()
    line_count = 0
    with PATCH.open("rb") as stream:
        for offset, support in enumerate(supports):
            selector = FIRST_SELECTOR + offset
            chosen = set(support)
            for edge in EDGES:
                line = stream.readline()
                need(line, ("early patch EOF", offset, edge))
                patch_hash.update(line)
                expected_literal = BLOCK_VAR[edge] if edge in chosen else -BLOCK_VAR[edge]
                expected = f"-{selector} {expected_literal} 0\n".encode("ascii")
                need(line == expected, ("selector implication mismatch", offset, edge))
                line_count += 1
        global_or = stream.readline()
        patch_hash.update(global_or)
        expected_or = (" ".join(map(str, range(FIRST_SELECTOR, LAST_SELECTOR + 1))) + " 0\n").encode("ascii")
        need(global_or == expected_or, "global selector OR")
        line_count += 1
        need(stream.read(1) == b"", "trailing patch byte")
    need(line_count == PATCH_CLAUSES, "patch line count")
    need(patch_hash.hexdigest() == PATCH_SHA256, "patch semantic replay hash")


def replay_derivation():
    base_hash = hashlib.sha256()
    output_hash = hashlib.sha256()
    patch_hash = hashlib.sha256()
    clauses = ClauseReplay()
    base_body_bytes = BASE_BYTES - len(BASE_HEADER)

    with BASE.open("rb") as base, OUTPUT.open("rb") as output, PATCH.open("rb") as patch:
        base_header = base.readline()
        output_header = output.readline()
        need(base_header == BASE_HEADER, "base header")
        need(output_header == OUTPUT_HEADER, "output header")
        base_hash.update(base_header)
        output_hash.update(output_header)

        remaining = base_body_bytes
        while remaining:
            size = min(1 << 20, remaining)
            base_chunk = base.read(size)
            output_chunk = output.read(size)
            need(len(base_chunk) == size and output_chunk == base_chunk, ("base body divergence", base_body_bytes - remaining))
            base_hash.update(base_chunk)
            output_hash.update(output_chunk)
            clauses.feed(output_chunk)
            remaining -= size
        need(base.read(1) == b"", "trailing base byte")

        while True:
            patch_chunk = patch.read(1 << 20)
            if not patch_chunk:
                break
            output_chunk = output.read(len(patch_chunk))
            need(output_chunk == patch_chunk, "patch suffix divergence")
            patch_hash.update(patch_chunk)
            output_hash.update(output_chunk)
            clauses.feed(output_chunk)
        need(output.read(1) == b"", "trailing output byte")

    clauses.finish()
    need(clauses.lines == OUTPUT_CLAUSES, ("output clause count", clauses.lines))
    need(clauses.max_variable == LAST_SELECTOR, ("max variable", clauses.max_variable))
    need(base_hash.hexdigest() == BASE_SHA256, "base hash")
    need(patch_hash.hexdigest() == PATCH_SHA256, "patch suffix hash")
    need(output_hash.hexdigest() == OUTPUT_SHA256, "output hash")
    return clauses.max_variable


def main():
    fixed_hashes = {
        MATERIALIZER / "MANIFEST.sha256": MATERIALIZER_MANIFEST_SHA256,
        MATERIALIZER / "CLEARANCE.json": CLEARANCE_SHA256,
        PATCH_PACKAGE / "MANIFEST.sha256": PATCH_MANIFEST_SHA256,
        TERMINAL / "FINAL_MANIFEST.sha256": TERMINAL_MANIFEST_SHA256,
        TERMINAL / "TERMINAL_AUDIT_RESULT.json": TERMINAL_RESULT_SHA256,
        BUILD: BUILD_SHA256,
    }
    for path, expected in fixed_hashes.items():
        need(sha256(path) == expected, ("dependency hash", str(path)))
    need(BASE.stat().st_size == BASE_BYTES, "base bytes")
    need(PATCH.stat().st_size == PATCH_BYTES, "patch bytes")
    need(OUTPUT.stat().st_size == OUTPUT_BYTES, "output bytes")

    clearance = json.loads((MATERIALIZER / "CLEARANCE.json").read_text())
    build = json.loads(BUILD.read_text())
    terminal = json.loads((TERMINAL / "TERMINAL_AUDIT_RESULT.json").read_text())
    need(clearance["materializer_manifest_sha256"] == MATERIALIZER_MANIFEST_SHA256, "clearance materializer binding")
    need(clearance["exact16_terminal_manifest_sha256"] == TERMINAL_MANIFEST_SHA256, "clearance terminal binding")
    need(clearance["patch_package_manifest_sha256"] == PATCH_MANIFEST_SHA256, "clearance patch binding")
    need(clearance["authorized_action"] == "STREAM_ORIGINAL_BASE_REPLACE_HEADER_APPEND_PATCH_NO_SOLVER", "action")
    need(clearance["base_relative_path"].endswith("max16_current.cnf"), "original base path")
    need("exact16_target_union_current.cnf" not in clearance["base_relative_path"], "narrow substitution")
    need(clearance["resource_clear"] is True and clearance["no_overlap"] is True and clearance["fresh_process_census"] == 0,
         "materialization clearance")
    need(terminal["status"] == "PASS_VERIFIED_UNSAT_AND_EIGHT_BLOCK_SUPPORT_FRONTIER_ONLY", "terminal scope")
    need(terminal["checker"] == {**terminal["checker"], "exit": 0, "status": "VERIFIED"}, "terminal checker")
    need(build["status"] == "MATERIALIZED_NOT_SOLVED__PENDING_INDEPENDENT_FULL_REPLAY", "build status")
    need(build["clearance_sha256"] == CLEARANCE_SHA256 and build["solver_run"] is False, "build clearance/no solver")
    need(build["base_sha256"] == BASE_SHA256 and build["patch_sha256"] == PATCH_SHA256, "build ingredients")
    need(build["output_sha256"] == OUTPUT_SHA256 and build["output_bytes"] == OUTPUT_BYTES, "build output")
    need(build["output_header"] == {"variables": 464139, "clauses": OUTPUT_CLAUSES}, "build header")
    need(build["atomic_temp_to_final"] is True and build["independent_full_replay_required_before_solve"] is True, "atomic/replay")

    supports = parse_ledger()
    replay_patch_semantics(supports)
    maximum = replay_derivation()
    result = {
        "schema": "n8-x5-combined-exact16-materialization-referee-v1",
        "status": "PASS_EXACT_STREAM_DERIVATION_HELD_NO_SOLVER",
        "scope": "materialization correctness and held solver contract only; no SAT/UNSAT theorem claim",
        "dependencies": {
            "materializer_manifest_sha256": MATERIALIZER_MANIFEST_SHA256,
            "clearance_sha256": CLEARANCE_SHA256,
            "patch_manifest_sha256": PATCH_MANIFEST_SHA256,
            "exact16_terminal_manifest_sha256": TERMINAL_MANIFEST_SHA256,
            "exact16_terminal_result_sha256": TERMINAL_RESULT_SHA256,
            "build_record_sha256": BUILD_SHA256,
        },
        "base": {"sha256": BASE_SHA256, "bytes": BASE_BYTES, "variables": 428247, "clauses": BASE_CLAUSES},
        "patch": {
            "sha256": PATCH_SHA256,
            "bytes": PATCH_BYTES,
            "clauses": PATCH_CLAUSES,
            "supports": len(supports),
            "implications_per_support": 25,
            "global_or_clauses": 1,
            "semantic_replay": "PASS_BYTE_EXACT_ALL_IMPLICATIONS_AND_GLOBAL_OR",
        },
        "output": {
            "sha256": OUTPUT_SHA256,
            "bytes": OUTPUT_BYTES,
            "variables": 464139,
            "clauses": OUTPUT_CLAUSES,
            "maximum_variable_replayed": maximum,
        },
        "derivation": {
            "header_replacement_only": True,
            "original_base_body_byte_identical": True,
            "patch_suffix_byte_identical": True,
            "trailing_bytes": 0,
            "all_dimacs_clause_lines_replayed": OUTPUT_CLAUSES,
        },
        "runtime": {"solver_runs": 0, "solver_plan_held": True},
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
