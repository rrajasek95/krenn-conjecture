#!/usr/bin/env python3
"""Constants and compact-fragment checks for the streaming materializer."""

import hashlib
from pathlib import Path

PATCH_PACKAGE_MANIFEST_SHA256 = "745f5fa186c05d265cb521bfbf1f3c9d485ac3779a7cfbee82cbdfc50c68eee8"
PATCH_SHA256 = "2ac0e05c9599f09066fc6b0bdd5812ac78e85328ec3928ef3f3f6498e7af2059"
TERMINAL_MANIFEST_SHA256 = "bcd2cc5f92bd2ddb7e52decfc65b68e430b2312281d5b1d181fa639c35d6416e"
TERMINAL_RESULT_SHA256 = "3264b7a8ae5a40c6c3cfb42f5fc4b19bd5193efcd39777782dae579b4db67808"
PATCH_BYTES = 13_136_474
PATCH_CLAUSES = 897_301
BASE_RELATIVE = "tmp/eight_vertex_local_degree4_full_local_max16_current.cnf"
BASE_SHA256 = "9e057710afe016609c31ae4c0cb45b1a948ca48b74426d390a2a9209035dd547"
BASE_BYTES = 231_480_677
BASE_HEADER = b"p cnf 428247 3083172\n"
BASE_CLAUSES = 3_083_172
NARROW_RELATIVE = "tmp/eight_vertex_local_degree4_full_local_max16_exact16_target_union_current.cnf"
NARROW_SHA256 = "dc5cd1cad3a062dc66a5788413e5c1e1799a1ed07e66266ad25cc195b470aafa"
OUTPUT_RELATIVE = "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_target_union_current.cnf"
RESULT_RELATIVE = OUTPUT_RELATIVE + ".build.json"
TARGET_HEADER = b"p cnf 464139 3980473\n"
TARGET_VARIABLES = 464_139
TARGET_CLAUSES = 3_980_473
TARGET_BYTES = BASE_BYTES - len(BASE_HEADER) + len(TARGET_HEADER) + PATCH_BYTES
MINIMUM_FREE_DISK_KIB = 16 * 1024 * 1024


def need(value, detail="contract failure"):
    if not value:
        raise RuntimeError(detail)


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def validate_patch(path: Path):
    need(path.is_file(), ("missing patch", str(path)))
    need(path.stat().st_size == PATCH_BYTES, "patch bytes")
    need(sha256_file(path) == PATCH_SHA256, "patch hash")
    data = path.read_bytes()
    need(data.endswith(b"\n") and data.count(b"\n") == PATCH_CLAUSES, "patch clause count")
    last = data.rsplit(b"\n", 2)[-2].split()
    need(last[-1] == b"0" and len(last) == 35_893, "global OR")
    need(last[0] == b"428248" and last[-2] == b"464139", "selector range")
