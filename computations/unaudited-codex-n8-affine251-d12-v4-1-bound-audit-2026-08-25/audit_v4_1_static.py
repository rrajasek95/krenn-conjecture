#!/usr/bin/env python3
"""Fail-closed byte-level source referee for v4.1."""
import hashlib, json, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/sealed_v4/main.rs"
NEW = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/sealed_v4_1/main.rs"
BIN = NEW.with_name("sparse_d12_dual")
SCHEMA = NEW.with_name("INDEX_SCHEMA.json")

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def need(ok, why):
    if not ok: raise SystemExit("REJECT: " + why)

old, new = BASE.read_text(), NEW.read_text()
needle, replacement = "|| round_cap > 1000", "|| round_cap > 10_000"
need(old.count(needle) == 1, "baseline bound occurrence")
need(new == old.replace(needle, replacement, 1), "source drift beyond sole bound patch")
need(sha(BASE) == "c83c6801ec2c09683c81773607fcf3babb538e34354dfd8f27d03aae0e22f102", "baseline source pin")
need(sha(NEW) == "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59", "v4.1 source pin")
need(sha(BIN) == "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048", "v4.1 binary pin")
need(sha(SCHEMA) == "abc718ee1e188be3d8e0558c4a40e5e4d3808a1347396c85d54f26811779a5a6", "schema pin")
out = {
  "schema": "KRENN_AFFINE251_D12_V4_1_BOUND_STATIC_REFEREE_V1",
  "status": "PASS_EXACT_SOLE_ROUND_CAP_BOUND_PATCH",
  "baseline_source_sha256": sha(BASE), "v4_1_source_sha256": sha(NEW),
  "v4_1_binary_sha256": sha(BIN), "index_schema_sha256": sha(SCHEMA),
  "exact_source_edit": {"old": needle, "new": replacement, "occurrences": 1},
  "unchanged_by_byte_equality_except_edit": ["modes", "rare-index", "persistence", "recurrence", "output schemas"]
}
tmp = HERE / "results_v4_1_static_audit.json.tmp"
tmp.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
os.replace(tmp, HERE / "results_v4_1_static_audit.json")
