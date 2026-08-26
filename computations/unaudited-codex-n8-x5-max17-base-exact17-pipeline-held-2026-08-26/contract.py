#!/usr/bin/env python3
"""Pinned small-data contract for the held max17/exact17 pipeline."""

from __future__ import annotations

import hashlib
from pathlib import Path

REPO = Path("/Users/rishi/workplace/krenn-conjecture")
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26")
ROOT = CROSS / "yesterdays-lemon"

BASE_HELD = REPO / "computations/unaudited-codex-n8-x5-degree4-max17-base-generation-held-2026-08-26"
TARGET_REFEREE = REPO / "computations/unaudited-codex-n8-x5-nine-block-exact17-target-union-referee-2026-08-26"
GENERATOR = ROOT / "claims/finite/n08/eight_vertex_local_degree4_support.py"
SUPPORT_LIBRARY = ROOT / "src/krenn_gu/rankone_support_sat.py"
LEDGER = TARGET_REFEREE / "exact17_target_supports.ledger"

BASE_RELATIVE = "tmp/eight_vertex_local_degree4_full_local_max17_current.cnf"
BASE_BUILD_RELATIVE = BASE_RELATIVE + ".build.json"
TARGET_RELATIVE = "tmp/eight_vertex_local_degree4_full_local_max17_exact17_target_union_current.cnf"
TARGET_BUILD_RELATIVE = TARGET_RELATIVE + ".build.json"

BASE_HELD_MANIFEST_SHA = "91bb64c59be708cfb49faef38ee856dcccd432ac09c0ce0c84a2a3adc95811d0"
TARGET_REFEREE_MANIFEST_SHA = "5eb55e55fb77a2e04dfcd303febe0d2f0e608b6de605590c02f16c11d5dff28b"
TARGET_REFEREE_RESULT_SHA = "6073468021f927aa4ee7ea442a81ca46907cc1adb166b04a50df147483e6a857"
GENERATOR_SHA = "83996bdb4da059de2490549ed07fbb225b024e21763a8db4cf871fb0228cb0bb"
SUPPORT_LIBRARY_SHA = "c795681f2d13a7bc5044572ccf89a532402bb885dde7b5772898f156a6a8bed6"
LEDGER_SHA = "f280c2b3223a9673c80d2aa7bfed7f97c0558fbc2dcb80f4ecac88f16c4b9dd8"

BASE_VARIABLES = 428_271
BASE_CLAUSES = 3_083_219
BASE_HEADER = b"p cnf 428271 3083219\n"
SELECTOR_COUNT = 18_180
SELECTOR_FIRST = BASE_VARIABLES + 1
SELECTOR_LAST = BASE_VARIABLES + SELECTOR_COUNT
PATCH_IMPLICATIONS = SELECTOR_COUNT * 25
PATCH_CLAUSES = PATCH_IMPLICATIONS + 1
TARGET_VARIABLES = SELECTOR_LAST
TARGET_CLAUSES = BASE_CLAUSES + PATCH_CLAUSES
TARGET_HEADER = b"p cnf 446451 3537720\n"

BLOCK_EDGES = (
    "01", "02", "03", "04", "12", "13", "14", "15", "16", "17",
    "23", "24", "25", "26", "27", "34", "35", "36", "37", "45",
    "46", "47", "56", "57", "67",
)
BLOCK_VARIABLES = dict(zip(BLOCK_EDGES, range(226, 251), strict=True))

FORBIDDEN_BASE_HASHES = {
    "max16_base": "9e057710afe016609c31ae4c0cb45b1a948ca48b74426d390a2a9209035dd547",
    "max16_narrow_target": "dc5cd1cad3a062dc66a5788413e5c1e1799a1ed07e66266ad25cc195b470aafa",
    "max16_combined_target": "c96d4ac1ac70abd8bfcf3b2b7228a94963a8c0fc52c8a891e502122be857da12",
}


def need(value, detail="contract failure"):
    if not value:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def parse_ledger() -> list[str]:
    data = LEDGER.read_bytes()
    need(hashlib.sha256(data).hexdigest() == LEDGER_SHA, "ledger hash")
    need(data.endswith(b"\n"), "ledger newline")
    lines = data.decode("ascii").splitlines()
    need(len(lines) == SELECTOR_COUNT and lines == sorted(lines) and len(set(lines)) == SELECTOR_COUNT, "ledger count/order")
    allowed = set(BLOCK_EDGES)
    for index, line in enumerate(lines):
        edges = line.split("|")
        need(len(edges) == 17 and edges == sorted(edges) and len(set(edges)) == 17, ("support", index))
        need(set(edges) <= allowed and {"01", "02", "03", "04"} <= set(edges), ("support universe", index))
    return lines


def make_patch(ledger: list[str]) -> bytes:
    lines = []
    for offset, support_line in enumerate(ledger):
        support = set(support_line.split("|"))
        selector = SELECTOR_FIRST + offset
        for edge in BLOCK_EDGES:
            literal = BLOCK_VARIABLES[edge] if edge in support else -BLOCK_VARIABLES[edge]
            lines.append(f"-{selector} {literal} 0\n")
    lines.append(" ".join(map(str, range(SELECTOR_FIRST, SELECTOR_LAST + 1))) + " 0\n")
    need(len(lines) == PATCH_CLAUSES)
    return "".join(lines).encode("ascii")
