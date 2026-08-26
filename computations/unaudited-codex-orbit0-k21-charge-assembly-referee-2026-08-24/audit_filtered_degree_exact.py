#!/usr/bin/env python3
"""Independent referee for the generic K20--K24 exact-Q assembler.

No charge evaluator is invoked.  This checks the frozen DAG, exact scalar
assembly, deterministic authoritative replays, and fail-closed CLI behavior.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSEMBLY = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24"
SOURCE = ASSEMBLY / "assemble_filtered_degree_exact.py"
DAG_PATH = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
K20_DIR = ROOT / "computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23"
K20_MANIFEST = K20_DIR / "k20_path_manifest_complete.json"
K20_AUTH = K20_DIR / "results_complete_k20_36path_charge.json"
K21_MANIFEST = ASSEMBLY / "k21_manifest_47_of_52_partial.json"
K21_AUTH = ASSEMBLY / "results_k21_47_of_52_5_gap.json"
K21_GENERIC = ASSEMBLY / "results_k21_47_of_52_5_gap_generic.json"
OUT = HERE / "results_filtered_degree_exact_referee.json"

EXPECTED_COUNTS = {20: 36, 21: 52, 22: 76, 23: 59, 24: 35}
EXPECTED_MISSING_K21 = [
    "D14:222|R:2-3-2",
    "D14:222|R:3-2-2",
    "D15:223|R:2-2-2",
    "D15:232|R:2-2-2",
    "D15:322|R:2-2-2",
]
PINS = {
    SOURCE: "cf4a5214a15081b91d89c90fc4b79c39e0d54e9b183f442131eec258bf1bce69",
    DAG_PATH: "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
    K20_MANIFEST: "cc12715158c85ee111f7a5522363c7f38ed06232a1f779a7392575860f792e48",
    K20_AUTH: "ea4ccd5af21312fa1bd9b73e274c9a0ceea493560315b30bfb1b588d69b70b32",
    K21_MANIFEST: "1bacbb09d64027fc409c66fb7dbe47942b80a7c4225a9d8fdd4d07385fb59d84",
    K21_AUTH: "07ddcf48d7ed2614d4376c762effb4edb5dfcd9a582ab656b97df5e42849541b",
    K21_GENERIC: "fb80865e12ac44d46a9425f7b8e2d16d9331e34a98eb35270860a0a906a5b31a",
}
MODES = {
    "standard": [],
    "optimized": ["-O"],
    "isolated_no_site": ["-I", "-S"],
}


def require(ok, detail):
    if not ok:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def q(value):
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, dict):
        require(set(value) >= {"numerator", "denominator"}, value)
        return Fraction(int(value["numerator"]), int(value["denominator"]))
    raise TypeError(value)


def ids(entry):
    require(("id" in entry) != ("ids" in entry), entry)
    value = [entry["id"]] if "id" in entry else entry["ids"]
    require(isinstance(value, list) and value and
            all(isinstance(x, str) for x in value), value)
    require(len(value) == len(set(value)), value)
    return value


def independent_expected(degree, manifest, required, allow_partial):
    require(("groups" in manifest) != ("paths" in manifest), manifest.keys())
    entries = manifest["groups"] if "groups" in manifest else manifest["paths"]
    flat = [x for entry in entries for x in ids(entry)]
    counts = Counter(flat)
    duplicate = sorted(x for x, n in counts.items() if n != 1)
    extra = sorted(set(flat) - set(required))
    missing = [x for x in required if x not in set(flat)]
    require(not duplicate and not extra, (duplicate, extra))
    require(allow_partial or not missing, missing)
    full = sum((q(entry["full"]) for entry in entries), Fraction())
    irr = sum((q(entry["irreducible"]) for entry in entries), Fraction())
    def render(x):
        return {"numerator": x.numerator, "denominator": x.denominator, "text": str(x)}
    complete = not missing
    return {
        "status": (f"PASS_COMPLETE_K{degree}_{len(required)}_ID_EXACT_Q" if complete
                   else f"REJECT_INCOMPLETE_K{degree}_{len(required)}_ID_GATE"),
        "complete_claim": complete,
        "degree": degree,
        "required_paths": len(required),
        "covered_paths": len(flat),
        "scalar_groups": len(entries),
        "missing_paths": missing,
        "duplicate_paths": duplicate,
        "extra_paths": extra,
        "full": render(full),
        "irreducible": render(irr),
        "covered_ids": flat,
        "dag_logical_sha256": DAG["logical_sha256"],
        "manifest_logical_sha256": sha256(json.dumps(
            manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
    }


def canonical_bytes(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()


def command(mode, *args):
    return [sys.executable, *MODES[mode], str(SOURCE), *map(str, args)]


def invoke(mode, *args):
    return subprocess.run(command(mode, *args), cwd=ROOT, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=30, check=False)


def mutate_manifests(base):
    def clone():
        return json.loads(json.dumps(base))
    missing = clone()
    last = missing["paths"][-1]
    if "ids" in last and len(last["ids"]) > 1:
        last["ids"].pop()
    else:
        missing["paths"].pop()
    duplicate = clone(); duplicate["paths"].append(json.loads(json.dumps(duplicate["paths"][-1])))
    extra = clone()
    target = extra["paths"][-1]
    if "id" in target:
        target["id"] = "D99:hostile|R:20"
    else:
        target["ids"][-1] = "D99:hostile|R:20"
    bad_digest = clone(); bad_digest["paths"][0]["evidence_sha256"] = "A" * 64
    ambiguous = {"paths": clone()["paths"], "groups": clone()["paths"]}
    return {
        "missing": missing,
        "duplicate": duplicate,
        "extra": extra,
        "bad_digest": bad_digest,
        "ambiguous_schema": ambiguous,
    }


def verify_dag():
    raw = json.loads(DAG_PATH.read_text())
    claimed = raw.pop("logical_sha256")
    calculated = sha256(json.dumps(raw, sort_keys=True,
                                   separators=(",", ":")).encode()).hexdigest()
    require(claimed == calculated ==
            "ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66",
            (claimed, calculated))
    raw["logical_sha256"] = claimed
    node_ids = Counter(node["id"] for node in raw["nodes"])
    require(max(node_ids.values()) == 1, node_ids)
    sets = {}
    for degree, expected_count in EXPECTED_COUNTS.items():
        from_nodes = sorted(node["id"] for node in raw["nodes"]
                            if node["reachable"] and node["degree"] == degree)
        declared = raw["required_reachable_lineage_ids_by_degree"][str(degree)]
        require(from_nodes == declared, (degree, from_nodes, declared))
        require(len(from_nodes) == len(set(from_nodes)) == expected_count,
                (degree, len(from_nodes), len(set(from_nodes))))
        require(raw["counts"]["reachable_lineages_by_degree"][str(degree)] == expected_count,
                (degree, raw["counts"]))
        sets[str(degree)] = from_nodes
    edge_children = {edge["child"] for edge in raw["edges"] if edge["child_reachable"]}
    for degree in range(21, 25):
        require(set(sets[str(degree)]) <= edge_children,
                (degree, set(sets[str(degree)]) - edge_children))
    return raw, sets


def main():
    for path, expected in PINS.items():
        require(digest(path) == expected, (path, digest(path), expected))
    global DAG
    DAG, dag_sets = verify_dag()
    k20_manifest = json.loads(K20_MANIFEST.read_text())
    k21_manifest = json.loads(K21_MANIFEST.read_text())
    expected20 = independent_expected(20, k20_manifest, dag_sets["20"], False)
    expected21 = independent_expected(21, k21_manifest, dag_sets["21"], True)
    require((expected20["covered_paths"], expected20["scalar_groups"]) == (36, 11), expected20)
    require((expected21["covered_paths"], expected21["scalar_groups"]) == (47, 12), expected21)
    require(expected21["missing_paths"] == EXPECTED_MISSING_K21, expected21)
    require(expected20["full"]["text"] == "12488470121433187072/521603775", expected20)
    require(expected20["irreducible"]["text"] == "12162234158979734656/521603775", expected20)
    require(expected21["full"]["text"] == expected21["irreducible"]["text"] ==
            "-448972336918014464/22678425", expected21)

    old20 = json.loads(K20_AUTH.read_text())
    old21 = json.loads(K21_AUTH.read_text())
    for expected, old, degree in ((expected20, old20, 20), (expected21, old21, 21)):
        require(expected["covered_ids"] == old["covered_ids"], degree)
        require(expected["missing_paths"] == old["missing_paths"], degree)
        require(expected["full"] == old["full"] and
                expected["irreducible"] == old["irreducible"], degree)
        require(expected["dag_logical_sha256"] == old["dag_logical_sha256"], degree)

    selftests = {}
    hostile_matrix = {}
    replay_hashes = {}
    with tempfile.TemporaryDirectory(prefix="k21-assembler-referee-") as td:
        temp = Path(td)
        hostiles = mutate_manifests(k20_manifest)
        hostile_paths = {}
        for name, obj in hostiles.items():
            path = temp / f"hostile_{name}.json"
            path.write_text(json.dumps(obj))
            hostile_paths[name] = path
        for mode in MODES:
            proc = invoke(mode, "--self-test")
            require(proc.returncode == 0 and not proc.stderr, (mode, proc.returncode, proc.stderr))
            payload = json.loads(proc.stdout)
            require(payload["status"] == "PASS_FILTERED_DEGREE_ASSEMBLER_SELFTEST", payload)
            require(payload["tested_required_path_counts"] ==
                    {str(k): v for k, v in EXPECTED_COUNTS.items()}, payload)
            require(all(payload[k] is True for k in (
                "group_scalar_once", "missing_rejected", "duplicate_rejected",
                "extra_rejected", "bad_digest_rejected", "ambiguous_schema_rejected")), payload)
            selftests[mode] = sha256(proc.stdout.encode()).hexdigest()

            out20 = temp / f"k20_{mode}.json"
            p20 = invoke(mode, "--degree", "20", K20_MANIFEST, out20)
            require(p20.returncode == 0 and out20.read_bytes() == canonical_bytes(expected20),
                    (mode, p20.returncode, p20.stdout, p20.stderr))
            out21 = temp / f"k21_{mode}.json"
            p21 = invoke(mode, "--audit-incomplete", "--degree", "21", K21_MANIFEST, out21)
            require(p21.returncode == 0 and out21.read_bytes() == canonical_bytes(expected21),
                    (mode, p21.returncode, p21.stdout, p21.stderr))
            require(out21.read_bytes() == K21_GENERIC.read_bytes(), mode)
            strict_out = temp / f"strict_k21_{mode}.json"
            strict = invoke(mode, "--degree", "21", K21_MANIFEST, strict_out)
            require(strict.returncode == 2 and not strict_out.exists() and
                    strict.stdout.startswith("REJECT: missing 5 K21 IDs:"),
                    (mode, strict.returncode, strict.stdout, strict.stderr))
            replay_hashes[mode] = {
                "K20_generic_bytes": digest(out20),
                "K21_generic_bytes": digest(out21),
            }

            hostile_matrix[mode] = {}
            for name, path in hostile_paths.items():
                hostile_out = temp / f"{mode}_{name}.json"
                hostile = invoke(mode, "--degree", "20", path, hostile_out)
                require(hostile.returncode == 2 and not hostile_out.exists() and
                        hostile.stdout.startswith("REJECT:"),
                        (mode, name, hostile.returncode, hostile.stdout, hostile.stderr))
                hostile_matrix[mode][name] = "REJECT_EXIT_2_NO_OUTPUT"
            unsupported_out = temp / f"unsupported_{mode}.json"
            unsupported = invoke(mode, "--degree", "19", K20_MANIFEST, unsupported_out)
            require(unsupported.returncode == 2 and not unsupported_out.exists(),
                    (mode, unsupported.returncode, unsupported.stdout, unsupported.stderr))
            hostile_matrix[mode]["unsupported_degree"] = "REJECT_EXIT_2_NO_OUTPUT"

    require(len(set(selftests.values())) == 1, selftests)
    require(len({x["K20_generic_bytes"] for x in replay_hashes.values()}) == 1,
            replay_hashes)
    require(len({x["K21_generic_bytes"] for x in replay_hashes.values()}) == 1,
            replay_hashes)
    report = {
        "status": "PASS_INDEPENDENT_FILTERED_DEGREE_EXACT_ASSEMBLER_REFEREE",
        "frozen_DAG": {
            "logical_sha256": DAG["logical_sha256"],
            "required_counts": {str(k): v for k, v in EXPECTED_COUNTS.items()},
            "sets_rederived_from_reachable_nodes": True,
            "declared_sets_exactly_match_rederived_sets": True,
        },
        "grouped_scalar_semantics": {
            "K20": {"covered_ids": 36, "scalar_groups_added_once": 11},
            "K21": {"covered_ids": 47, "scalar_groups_added_once": 12},
            "per_ID_scalar_multiplication": False,
            "independent_Fraction_sums_match": True,
        },
        "authoritative_replay": {
            "K20": {
                "complete": True,
                "full": expected20["full"]["text"],
                "irreducible": expected20["irreducible"]["text"],
                "covered_ids": 36,
                "generic_bytes_identical_across_modes": True,
                "generic_sha256": replay_hashes["standard"]["K20_generic_bytes"],
                "exact_fields_match_authoritative_result": True,
            },
            "K21": {
                "complete": False,
                "covered_ids": 47,
                "required_ids": 52,
                "missing_ids": EXPECTED_MISSING_K21,
                "partial_full_and_irreducible": expected21["full"]["text"],
                "fresh_output_byte_identical_to_frozen_generic_artifact": True,
                "generic_sha256": replay_hashes["standard"]["K21_generic_bytes"],
                "strict_mode_exit_2_no_output": True,
            },
        },
        "interpreter_modes": list(MODES),
        "selftest_stdout_sha256": selftests,
        "hostile_matrix": hostile_matrix,
        "no_charge_run": True,
        "pinned": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    }
    logical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    DAG = None
    main()
