#!/usr/bin/env python3
"""Produce a dynamic-state scanner from the pinned independent r1600 parser."""
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1600-cap3250-audit-2026-08-25/scan_chain_once.rs"
EXPECTED = "27d84ba2d29b8561a4f69a24d9711eb4138762142bac3d408e176ee1349fb446"
raw = BASE.read_bytes()
assert sha256(raw).hexdigest() == EXPECTED
s = raw.decode()
replacements = {
    "if pairs.len() != 7 { fail(\"exactly seven states required\"); }":
        "if pairs.len() < 2 { fail(\"at least two states required\"); }",
    "for edge in 0..6 {": "for edge in 0..pairs.len() - 1 {",
    "let mut origin = [0usize; 7];":
        "let mut origin = vec![0usize; pairs.len()];",
    "(0..7).map(|_| vec![0u8; 21 * 65_536])":
        "(0..pairs.len()).map(|_| vec![0u8; 21 * 65_536])",
    "if present != (first..7).collect::<Vec<_>>()":
        "if present != (first..pairs.len()).collect::<Vec<_>>()",
    "if final_fingerprint != readers[6].expected_fingerprint":
        "if final_fingerprint != readers.last().unwrap().expected_fingerprint",
    "for state in 0..7 {": "for state in 0..pairs.len() {",
    "\\\"status\\\": \\\"PASS_SIX_DESCENDANT_EDGES_AND_ALL_COLUMNS\\\"":
        "\\\"status\\\": \\\"PASS_ALL_DESCENDANT_EDGES_AND_ALL_COLUMNS\\\"",
    "writeln!(out, \"  \\\"checkpoint_descendant_edges\\\": 6,\").unwrap();":
        "writeln!(out, \"  \\\"checkpoint_descendant_edges\\\": {},\", pairs.len()-1).unwrap();",
    "writeln!(out, \"  \\\"cache_descendant_edges\\\": 6,\").unwrap();":
        "writeln!(out, \"  \\\"cache_descendant_edges\\\": {},\", pairs.len()-1).unwrap();",
    "println!(\"PASS six edges, {} columns, {} terms, {:.3}s\", counts[6], terms, seconds);":
        "println!(\"PASS {} edges, {} columns, {} terms, {:.3}s\", pairs.len()-1, counts.last().unwrap(), terms, seconds);",
}
for old, new in replacements.items():
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)
(HERE / "scan_chain_once.rs").write_text(s)
print(sha256(s.encode()).hexdigest())
