#!/usr/bin/env python3
"""Compact contract for the combined exact-16 selector fragment."""

from __future__ import annotations

import hashlib
from pathlib import Path

BASE_VARIABLES = 428_247
BASE_CLAUSES = 3_083_172
BASE_BYTES = 231_480_677
BASE_SHA256 = "9e057710afe016609c31ae4c0cb45b1a948ca48b74426d390a2a9209035dd547"
BASE_RELATIVE_PATH = "tmp/eight_vertex_local_degree4_full_local_max16_current.cnf"
NARROW_SHA256 = "dc5cd1cad3a062dc66a5788413e5c1e1799a1ed07e66266ad25cc195b470aafa"
NARROW_RELATIVE_PATH = "tmp/eight_vertex_local_degree4_full_local_max16_exact16_target_union_current.cnf"

LEDGER_SHA256 = "6bffb2962242725f8bd0603dfaeb91f64c2ee0e4430632b445b42e44d4a424d5"
REFEREE_MANIFEST_SHA256 = "46a29e7f0780f076aded01e3dd8e554ad44449cf7b79e4842434dce789b680b5"
REFEREE_RESULT_SHA256 = "230245d3a5a1a57dcb433572fe4f4f1ceb33edea6c3a9a682b583c3b689866a5"

BLOCK_EDGES = (
    "01", "02", "03", "04", "12", "13", "14", "15", "16", "17",
    "23", "24", "25", "26", "27", "34", "35", "36", "37", "45",
    "46", "47", "56", "57", "67",
)
BLOCK_VARIABLES = dict(zip(BLOCK_EDGES, range(226, 251), strict=True))
TARGET_COUNT = 35_892
SELECTOR_FIRST = BASE_VARIABLES + 1
SELECTOR_LAST = BASE_VARIABLES + TARGET_COUNT
ADDED_IMPLICATIONS = TARGET_COUNT * 25
ADDED_CLAUSES = ADDED_IMPLICATIONS + 1
TARGET_VARIABLES = SELECTOR_LAST
TARGET_CLAUSES = BASE_CLAUSES + ADDED_CLAUSES


def need(value, detail="contract failure"):
    if not value:
        raise RuntimeError(detail)


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def parse_ledger(data: bytes):
    need(hashlib.sha256(data).hexdigest() == LEDGER_SHA256, "ledger hash")
    need(data.endswith(b"\n"), "ledger newline")
    raw = data.decode("ascii").splitlines()
    need(len(raw) == TARGET_COUNT and raw == sorted(raw) and len(set(raw)) == TARGET_COUNT, "ledger order/count")
    allowed = set(BLOCK_EDGES)
    supports = []
    for line in raw:
        edges = tuple(line.split("|"))
        need(len(edges) == 16 and edges == tuple(sorted(edges)) and len(set(edges)) == 16, ("support", line))
        need(set(edges) <= allowed and set(edges) >= {"01", "02", "03", "04"}, ("edge universe", line))
        supports.append(edges)
    return tuple(supports)


def make_patch(supports):
    need(len(supports) == TARGET_COUNT)
    lines = []
    for offset, support in enumerate(supports):
        selector = SELECTOR_FIRST + offset
        chosen = set(support)
        for edge in BLOCK_EDGES:
            literal = BLOCK_VARIABLES[edge] if edge in chosen else -BLOCK_VARIABLES[edge]
            lines.append(f"-{selector} {literal} 0\n")
    lines.append(" ".join(map(str, range(SELECTOR_FIRST, SELECTOR_LAST + 1))) + " 0\n")
    need(len(lines) == ADDED_CLAUSES)
    return "".join(lines).encode("ascii")


def validate_patch(data, supports):
    need(data == make_patch(supports), "patch bytes")
    need(data.count(b"\n") == ADDED_CLAUSES)
    need((ADDED_IMPLICATIONS, ADDED_CLAUSES) == (897_300, 897_301))
    need((TARGET_VARIABLES, TARGET_CLAUSES) == (464_139, 3_980_473))
