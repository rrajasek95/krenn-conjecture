#!/usr/bin/env python3
"""Prove local hidden base copies change only dormant entrypoint names/include."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
up_filtered=ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/run_filtered_k17.rs"
up_hidden=ROOT/"computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
local_filtered=HERE/"k24_hidden_base_run_filtered_k17.rs"
local_hidden=HERE/"k24_hidden_base.rs"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
a=up_filtered.read_text().replace("fn main()","fn legacy_main_filtered()",1)
b=up_hidden.read_text().replace(
 'include!("../unaudited-codex-orbit0-filtered-k16-run-2026-08-23/run_filtered_k17.rs");',
 'include!("k24_hidden_base_run_filtered_k17.rs");',1).replace(
 "fn main()","fn legacy_main_hidden()",1)
assert local_filtered.read_text().rstrip("\n")==a.rstrip("\n")
assert local_hidden.read_text().rstrip("\n")==b.rstrip("\n")
out={"status":"PASS_HIDDEN_BASE_EXACT_REPLAY_ENTRYPOINT_ONLY_PATCH",
 "upstream_filtered_sha256":sha(up_filtered),"local_filtered_sha256":sha(local_filtered),
 "upstream_hidden_sha256":sha(up_hidden),"local_hidden_sha256":sha(local_hidden),
 "changes":["rename dormant filtered main","redirect local include","rename dormant hidden main"],
 "recurrence_logic_changed":False}
(HERE/"results_hidden_base_replay_audit.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps(out,indent=2,sort_keys=True))
