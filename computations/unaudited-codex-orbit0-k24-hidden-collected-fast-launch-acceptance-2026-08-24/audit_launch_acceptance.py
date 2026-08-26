#!/usr/bin/env python3
"""Replay the frozen launch acceptance without starting the full producer."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
def req(x,m):
 if not x:raise RuntimeError(m)
a=json.loads((HERE/"launch_acceptance.json").read_text())
for key in ("source","binary","input"):
 p=ROOT/a[key]["path"];req(sha(p)==a[key]["sha256"],key+" pin")
pins={"control_prefix1000000.json":a["bounded_gate"]["result_sha256"],"control_prefix1000000.json.samples.tsv":a["bounded_gate"]["samples_sha256"],"validate_hidden_collected_fast.py":a["validation"]["validator_sha256"],"referee_hidden_collected_fast.rs":a["validation"]["literal_referee_source_sha256"],"referee_hidden_collected_fast":a["validation"]["literal_referee_binary_sha256"],"results_hostile_selftest.json":a["validation"]["hostile_result_sha256"]}
for n,h in pins.items():req(sha(HERE/n)==h,n+" pin")
gate=json.loads((HERE/"control_prefix1000000.json").read_text());req(gate["projected_full_seconds"]<600 and gate["literal_sample_source_records"]==257,"bounded gate")
v=json.loads((HERE/"control_prefix1000000.validation.json").read_text());l=json.loads((HERE/"control_prefix1000000.literal_referee.json").read_text());h=json.loads((HERE/"results_hostile_selftest.json").read_text());req(v["status"].startswith("PASS") and v["witnesses"]==257,"structure");req(l["status"].startswith("PASS") and l["witnesses_replayed"]==257 and l["terminal_K4_exhaustive"],"literal");req(h["status"].startswith("PASS") and len(h["cases"])==16,"hostiles")
src=(ROOT/a["source"]["path"]).read_text();guard="assert_eq!(sink.terminal,34_216_879_080)";old="assert_eq!(sink.terminal,18_249_002_176)";sample="assert_eq!(lines.len(),258)";write="std::fs::write(&tmp";req(guard in src and old not in src,"full K4 pin");req(src.index(sample)<src.index(guard)<src.index(write),"fail-closed write order");req("terminal_K4_children" in src and "terminal_K3_children" not in src,"ledger degree")
out={"status":"PASS_FROZEN_HIDDEN_COLLECTED_FAST_LAUNCH_AUDIT","verdict":a["verdict"],"source_sha256":a["source"]["sha256"],"binary_sha256":a["binary"]["sha256"],"input_sha256":a["input"]["sha256"],"projected_full_seconds":gate["projected_full_seconds"],"literal_replays":257,"hostile_cases":16,"full_production_launched":False};(HERE/"results_launch_acceptance_audit.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
