#!/usr/bin/env python3
"""Fail-closed streaming materializer; default is small preflight only."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

from contract import *

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
PATCH = Path("/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-n8-x5-eight-nine-exact16-selector-patch-held-2026-08-26/selector_patch.cnfpart")
PATCH_MANIFEST = PATCH.parent / "MANIFEST.sha256"
TERMINAL = DEFAULT_ROOT / "docs/audits/eight-vertex-degree4-exact16-target-union-terminal-unsat-2026-08-26"
TERMINAL_MANIFEST = TERMINAL / "FINAL_MANIFEST.sha256"
TERMINAL_RESULT = TERMINAL / "TERMINAL_AUDIT_RESULT.json"


def atomic_json(path: Path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    need(not path.exists() and not temporary.exists(), ("refuse overwrite", str(path)))
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def small_preflight():
    need(sha256_file(PATCH_MANIFEST) == PATCH_PACKAGE_MANIFEST_SHA256, "patch manifest")
    validate_patch(PATCH)
    need(sha256_file(TERMINAL_MANIFEST) == TERMINAL_MANIFEST_SHA256, "terminal manifest")
    need(sha256_file(TERMINAL_RESULT) == TERMINAL_RESULT_SHA256, "terminal result")
    terminal = json.loads(TERMINAL_RESULT.read_text())
    need(terminal["status"] == "PASS_VERIFIED_UNSAT_AND_EIGHT_BLOCK_SUPPORT_FRONTIER_ONLY", "terminal status")
    need(terminal["checker"]["status"] == "VERIFIED" and terminal["checker"]["exit"] == 0, "checker status")
    template = json.loads((HERE / "CLEARANCE_TEMPLATE.json").read_text())
    need(template["exact16_terminal_manifest_sha256"] == TERMINAL_MANIFEST_SHA256, "terminal template pin")
    need(template["status"] == "HELD_DEPENDENCIES_BOUND_MANAGER_CLEARANCE_NULL", "template status")


def validate_clearance(path: Path):
    value = json.loads(path.read_text())
    required = {
        "schema", "status", "authorized_action", "nonce", "issued_utc", "expires_utc",
        "materializer_manifest_sha256", "patch_package_manifest_sha256",
        "exact16_terminal_manifest_sha256", "resource_clear", "no_overlap",
        "fresh_process_census", "free_disk_kib", "minimum_free_disk_kib",
        "base_relative_path", "output_relative_path", "result_relative_path",
    }
    need(set(value) == required, "clearance fields")
    need(value["schema"] == "n8-x5-combined-exact16-streaming-materialization-clearance-v1")
    need(value["status"] == "AUTHORIZED_ONE_MATERIALIZATION_NO_SOLVER")
    need(value["authorized_action"] == "STREAM_ORIGINAL_BASE_REPLACE_HEADER_APPEND_PATCH_NO_SOLVER")
    need(isinstance(value["nonce"], str) and len(value["nonce"]) >= 16 and value["nonce"].replace("-", "").isalnum(), "nonce")
    need(value["patch_package_manifest_sha256"] == PATCH_PACKAGE_MANIFEST_SHA256, "patch package pin")
    own_manifest = HERE / "MANIFEST.sha256"
    need(value["materializer_manifest_sha256"] == sha256_file(own_manifest), "materializer pin")
    terminal = value["exact16_terminal_manifest_sha256"]
    need(terminal == TERMINAL_MANIFEST_SHA256, "terminal pin")
    need(value["resource_clear"] is True and value["no_overlap"] is True, "resource clearance")
    need(value["fresh_process_census"] == 0, "process census")
    need(value["minimum_free_disk_kib"] == MINIMUM_FREE_DISK_KIB, "disk contract")
    need(value["free_disk_kib"] >= MINIMUM_FREE_DISK_KIB, "clearance disk")
    need(value["base_relative_path"] == BASE_RELATIVE, "base path")
    need(value["output_relative_path"] == OUTPUT_RELATIVE, "output path")
    need(value["result_relative_path"] == RESULT_RELATIVE, "result path")
    issued = datetime.fromisoformat(value["issued_utc"].replace("Z", "+00:00"))
    expires = datetime.fromisoformat(value["expires_utc"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    need(issued <= now < expires and (expires - issued).total_seconds() <= 3600, "expired/overlong clearance")
    return value


def process_census():
    observed = subprocess.run(
        ["/bin/ps", "-axo", "pid=,command="], capture_output=True, text=True, check=False
    )
    need(observed.returncode == 0, "process observer failure")
    bad = []
    tokens = ("cadical", "drat-trim", "singular", "eight_vertex_local_degree4_support.py")
    for line in observed.stdout.splitlines():
        fields = line.strip().split(maxsplit=1)
        if len(fields) != 2 or int(fields[0]) == os.getpid():
            continue
        lowered = fields[1].lower()
        if any(token in lowered for token in tokens):
            bad.append(line.strip())
    need(not bad, ("heavy process overlap", bad))


def execute(root: Path, clearance_path: Path):
    small_preflight()
    clearance = validate_clearance(clearance_path)
    process_census()
    need(shutil.disk_usage(root).free // 1024 >= MINIMUM_FREE_DISK_KIB, "live disk floor")

    base = (root / BASE_RELATIVE).resolve()
    narrow = (root / NARROW_RELATIVE).resolve()
    output = (root / OUTPUT_RELATIVE).resolve()
    result = (root / RESULT_RELATIVE).resolve()
    need(base != narrow and str(base).endswith(BASE_RELATIVE), "narrow/path substitution")
    need(base.is_file() and base.stat().st_size == BASE_BYTES, "base missing/bytes")
    need(not output.exists() and not result.exists(), "refuse overwrite")
    output.parent.mkdir(parents=True, exist_ok=True)
    nonce = clearance["nonce"]
    temporary = output.with_name(output.name + f".{nonce}.tmp")
    rejected = output.with_name(output.name + f".{nonce}.rejected")
    need(not temporary.exists() and not rejected.exists(), "stale temporary")

    base_hash = hashlib.sha256()
    output_hash = hashlib.sha256()
    base_bytes = 0
    body_clauses = 0
    output_bytes = 0
    try:
        with base.open("rb") as source, temporary.open("xb") as target:
            old_header = source.readline()
            need(old_header == BASE_HEADER, ("base header", old_header))
            base_hash.update(old_header)
            base_bytes += len(old_header)
            target.write(TARGET_HEADER)
            output_hash.update(TARGET_HEADER)
            output_bytes += len(TARGET_HEADER)
            while chunk := source.read(1 << 20):
                base_hash.update(chunk)
                base_bytes += len(chunk)
                body_clauses += chunk.count(b"\n")
                target.write(chunk)
                output_hash.update(chunk)
                output_bytes += len(chunk)
            need(base_hash.hexdigest() != NARROW_SHA256, "narrow CNF supplied as base")
            need(base_hash.hexdigest() == BASE_SHA256, "base hash")
            need(base_bytes == BASE_BYTES and body_clauses == BASE_CLAUSES, "base recount")
            with PATCH.open("rb") as patch_stream:
                while chunk := patch_stream.read(1 << 20):
                    target.write(chunk)
                    output_hash.update(chunk)
                    output_bytes += len(chunk)
            need(output_bytes == TARGET_BYTES, "output bytes")
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary, output)
        directory = os.open(output.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except Exception:
        if temporary.exists():
            os.replace(temporary, rejected)
        raise

    payload = {
        "schema": "n8-x5-combined-exact16-streaming-materialization-result-v1",
        "status": "MATERIALIZED_NOT_SOLVED__PENDING_INDEPENDENT_FULL_REPLAY",
        "clearance_sha256": sha256_file(clearance_path),
        "clearance_nonce": nonce,
        "exact16_terminal_manifest_sha256": clearance["exact16_terminal_manifest_sha256"],
        "base_relative_path": BASE_RELATIVE,
        "base_sha256": BASE_SHA256,
        "base_bytes": base_bytes,
        "base_header": {"variables": 428247, "clauses": BASE_CLAUSES},
        "base_body_clauses_recounted": body_clauses,
        "patch_sha256": PATCH_SHA256,
        "patch_clauses": PATCH_CLAUSES,
        "output_relative_path": OUTPUT_RELATIVE,
        "output_sha256": output_hash.hexdigest(),
        "output_bytes": output_bytes,
        "output_header": {"variables": TARGET_VARIABLES, "clauses": TARGET_CLAUSES},
        "atomic_temp_to_final": True,
        "solver_run": False,
        "independent_full_replay_required_before_solve": True,
    }
    atomic_json(result, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--clearance", type=Path)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    if not args.execute:
        need(args.clearance is None, "clearance supplied without --execute")
        small_preflight()
        print("HELD_SMALL_PREFLIGHT_PASS__NO_BASE_READ_NO_MATERIALIZATION")
        return
    need(args.clearance is not None, "--execute requires --clearance")
    execute(args.root.resolve(), args.clearance.resolve())


if __name__ == "__main__":
    main()
