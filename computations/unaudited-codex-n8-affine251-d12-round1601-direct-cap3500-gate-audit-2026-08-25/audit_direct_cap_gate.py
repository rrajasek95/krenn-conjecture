#!/usr/bin/env python3
"""Fail-closed independent audit of the r1601 3.25m -> 3.5m cap gate."""
import hashlib, json, os, struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PLAN = json.loads((HERE / "AUDIT_PLAN.json").read_text())
ROOT = REPO / PLAN["producer_root"]
CONTROL = PLAN["control"]["label"]
CANDIDATE = PLAN["candidate"]["label"]
LABELS = [CONTROL, CANDIDATE]
CAPS = {CONTROL: PLAN["control"]["column_cap"], CANDIDATE: PLAN["candidate"]["column_cap"]}
CONTRACT = PLAN["contract"]

def need(condition, message):
    if not condition:
        raise SystemExit("REJECT: " + message)

def load(path):
    return json.loads(path.read_text())

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            h.update(block)
    return h.hexdigest()

def arg(command, flag):
    need(command.count(flag) == 1, "command flag " + flag)
    return command[command.index(flag) + 1]

def checkpoint_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    need(data[:12] == b"AFF12CEG1\0\0\0", "checkpoint magic")
    prime, round_number, columns, support = struct.unpack_from("<QQQQ", data, 12)
    need(path.stat().st_size == 44 + 15 * columns + 21 * support, "checkpoint length")
    return {"prime": prime, "round": round_number, "columns": columns,
            "support": support, "bytes": path.stat().st_size}

def normalize_command(command, label):
    return [token.replace("/" + label + "/", "/RUN/") for token in command]

for name in ("audit", "replay", "manifest", "compaction_record"):
    path = REPO / PLAN["input"][name]
    need(path.is_file(), "missing input " + name)
    need(sha(path) == PLAN["input"][name + "_sha256"], "input pin " + name)

input_audit = load(REPO / PLAN["input"]["audit"])
input_replay = load(REPO / PLAN["input"]["replay"])
need(input_audit["status"] == "PASS_EXACT_FULLY_TELEMETERED_ROUND1600_CAP3250_CHAIN", "input audit status")
need(input_audit["final"]["round"] == 1600 and input_audit["final"]["columns"] == PLAN["input"]["columns"], "input audit endpoint")
need(input_audit["final"]["checkpoint_sha256"] == PLAN["input"]["checkpoint_sha256"], "input checkpoint pin")
need(input_audit["final"]["vectors_sha256"] == PLAN["input"]["vectors_sha256"], "input cache pin")
need(input_replay["status"] == "PASS_SIX_DESCENDANT_EDGES_AND_ALL_COLUMNS", "input replay status")
need(input_replay["columns"][-1] == PLAN["input"]["columns"] and input_replay["verification_failures"] == 0, "input replay contents")

for name, digest in PLAN["producer_pins"].items():
    need(sha(ROOT / name) == digest, "producer pin " + name)

required_result_keys = {
    "cached_vectors_loaded", "checkpoint", "column_cap", "column_orbits_exposed",
    "degree", "dual", "dual_support", "elapsed_seconds", "elimination_kernel",
    "global_annihilation", "group_order", "incomplete_reason", "incremental_basis",
    "peak_rss_kib", "pivot_mode", "portfolio_parallel", "portfolio_period", "prime",
    "provider_distinct_terms", "provider_equations", "provider_terms_parsed", "restore_seconds",
    "rounds", "rounds_completed", "rss_limit_gib", "schema", "seed_support", "status",
    "strategy", "support_cap", "target_pairing", "vector_cache", "vector_cache_bytes",
    "vector_cache_write_seconds", "vectors_materialized_on_restore", "wall_limit_seconds", "workers"
}
required_round_keys = {
    "round", "columns", "new_columns", "dual_support", "new_support_rows",
    "selected_strategy", "selected_pivot", "solve_seconds", "incident_seconds", "materialize_seconds"
}
semantic_fields = [
    "schema", "status", "incomplete_reason", "degree", "prime", "group_order",
    "provider_equations", "provider_terms_parsed", "provider_distinct_terms", "seed_support",
    "column_orbits_exposed", "dual_support", "rounds_completed", "global_annihilation",
    "target_pairing", "workers", "pivot_mode", "strategy", "elimination_kernel",
    "incremental_basis", "portfolio_period", "portfolio_parallel", "support_cap",
    "wall_limit_seconds", "rss_limit_gib", "cached_vectors_loaded",
    "vectors_materialized_on_restore", "vector_cache_bytes"
]
record_fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
                 "selected_strategy", "selected_pivot"]

results, watches, records, semantics = {}, {}, {}, {}
for label in LABELS:
    lane = ROOT / label
    for name in ("result.json", "checkpoint.bin", "vectors.bin", "watchdog.json", "stderr.log"):
        need((lane / name).is_file(), "missing " + label + "/" + name)
    need(not any(lane.glob("*.tmp")), "temporary output in " + label)
    need(not (lane / "dual.tsv").exists(), "unexpected dual output in " + label)
    results[label] = load(lane / "result.json")
    watches[label] = load(lane / "watchdog.json")
    result, watch = results[label], watches[label]
    need(set(result) == required_result_keys, label + " result schema")
    need(len(result["rounds"]) == 1 and set(result["rounds"][0]) == required_round_keys, label + " round schema")
    need((result["status"], result["incomplete_reason"], result["rounds_completed"]) ==
         ("INCOMPLETE_SEARCH_CAP", "ROUND_CAP", PLAN["target_round"]), label + " terminal state")
    need(result["column_cap"] == CAPS[label], label + " column cap")
    need(result["cached_vectors_loaded"] == PLAN["input"]["columns"] and
         result["vectors_materialized_on_restore"] == 0, label + " exact restore")
    need(watch["status"] == "PASS" and watch["returncode"] == 0 and watch["breach"] is None,
         label + " watchdog")
    need(watch["atomic_outputs_clean"] and watch["abort_final_output_absent"], label + " atomic")
    need(watch["elapsed_seconds"] < CONTRACT["wrapper_seconds"] and
         watch["peak_rss_kib"] < CONTRACT["rss_limit_kib"] and
         all(sample["rss_kib"] < CONTRACT["rss_limit_kib"] for sample in watch["samples"]),
         label + " resources")
    need((watch["source_sha256"], watch["binary_sha256"], watch["watchdog_sha256"]) ==
         (CONTRACT["source_sha256"], CONTRACT["binary_sha256"], CONTRACT["watchdog_sha256"]),
         label + " executable pins")
    need(watch["result_sha256"] == sha(lane / "result.json"), label + " result hash")
    expected_args = {
        "--round-cap": str(PLAN["target_round"]), "--column-cap": str(CAPS[label]),
        "--wall-seconds": str(CONTRACT["wall_seconds"]), "--rss-gib": "36",
        "--workers": str(CONTRACT["workers"]), "--pivot": CONTRACT["pivot"],
        "--strategy": CONTRACT["strategy"], "--elimination": CONTRACT["elimination"],
        "--incremental": CONTRACT["incremental"], "--prime": str(CONTRACT["prime"])
    }
    for flag, value in expected_args.items():
        need(arg(watch["command"], flag) == value, label + " " + flag)
    records[label] = {key: result["rounds"][0][key] for key in record_fields}
    semantics[label] = {key: result[key] for key in semantic_fields}

need(records[CONTROL] == records[CANDIDATE], "round record differs")
need(semantics[CONTROL] == semantics[CANDIDATE], "semantic fields differ")

def normalized_result(result):
    value = json.loads(json.dumps(result))
    for key in ("column_cap", "elapsed_seconds", "peak_rss_kib", "restore_seconds", "vector_cache_write_seconds"):
        value.pop(key)
    for row in value["rounds"]:
        for key in ("solve_seconds", "incident_seconds", "materialize_seconds"):
            row.pop(key)
    return value

need(normalized_result(results[CONTROL]) == normalized_result(results[CANDIDATE]), "normalized results differ")
left = normalize_command(watches[CONTROL]["command"], CONTROL)
right = normalize_command(watches[CANDIDATE]["command"], CANDIDATE)
need(len(left) == len(right), "command lengths differ")
differences = [(i, a, b) for i, (a, b) in enumerate(zip(left, right)) if a != b]
expected_index = left.index(str(CAPS[CONTROL]))
need(differences == [(expected_index, str(CAPS[CONTROL]), str(CAPS[CANDIDATE]))],
     "not sole cap difference: " + repr(differences))

checkpoint_hashes = {label: sha(ROOT / label / "checkpoint.bin") for label in LABELS}
vector_hashes = {label: sha(ROOT / label / "vectors.bin") for label in LABELS}
need(len(set(checkpoint_hashes.values())) == 1, "checkpoint bytes differ")
need(len(set(vector_hashes.values())) == 1, "cache bytes differ")
headers = {label: checkpoint_header(ROOT / label / "checkpoint.bin") for label in LABELS}
need(headers[CONTROL] == headers[CANDIDATE], "checkpoint headers differ")
header = headers[CONTROL]
record = records[CONTROL]
need((header["prime"], header["round"], header["columns"], header["support"]) ==
     (CONTRACT["prime"], PLAN["target_round"], record["columns"], record["dual_support"]),
     "checkpoint endpoint")

output = {
    "schema": "KRENN_AFFINE251_D12_ROUND1601_DIRECT_CAP3500_AUDIT_V1",
    "status": "PASS_EXACT_DIRECT_CAP3250_TO_CAP3500_EQUIVALENCE",
    "input": PLAN["input"], "round_record": record, "checkpoint_header": header,
    "checkpoint_sha256": checkpoint_hashes[CONTROL], "vectors_sha256": vector_hashes[CONTROL],
    "exact_byte_equality": {"checkpoint": True, "vectors": True},
    "only_normalized_command_difference_is_cap": True,
    "control_result_sha256": sha(ROOT / CONTROL / "result.json"),
    "candidate_result_sha256": sha(ROOT / CANDIDATE / "result.json"),
    "control_watchdog_sha256": sha(ROOT / CONTROL / "watchdog.json"),
    "candidate_watchdog_sha256": sha(ROOT / CANDIDATE / "watchdog.json"),
    "maximum_elapsed_seconds": max(watches[label]["elapsed_seconds"] for label in LABELS),
    "maximum_peak_rss_kib": max(watches[label]["peak_rss_kib"] for label in LABELS),
    "producer_pins": PLAN["producer_pins"], "dual_outputs_absent": True,
    "accepted_candidate": CANDIDATE, "continued_beyond_round1601": False,
    "production_mutated": False
}
temporary = HERE / "results_round1601_direct_cap3500_audit.json.tmp"
temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1601_direct_cap3500_audit.json")
print(json.dumps({"status": output["status"], "round": record["round"],
                  "columns": record["columns"], "support": record["dual_support"],
                  "max_elapsed": output["maximum_elapsed_seconds"],
                  "max_rss_kib": output["maximum_peak_rss_kib"]}, sort_keys=True))
