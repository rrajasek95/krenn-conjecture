#!/usr/bin/env python3
"""Independent exact referee of rep2 group16 torus design and its guard-pivot intersection.

This script performs no Singular or ideal computation.  It reconstructs sources,
checks the torus and finite covers, and materializes one diagnostic intersection.
"""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import itertools
import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
H = Path(__file__).resolve().parent
ROOT = H.parents[1]
TOR = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26"
GUA = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26"
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25"
DES = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"

PINS = {
    TOR / "MANIFEST.sha256": "1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282",
    TOR / "results_design.json": "ee790ac911229e4aefb4d5e7a0c5dd4d7428ce006d40f1f62621fc3d34302360",
    TOR / "results_hostiles.json": "189f1bdbcc024cf78ab063461f5d6ddf6886f0f2300206ddb9972fb90e1e000d",
    TOR / "build_design.py": "e37512b9a3fe7d99774b833f1aed944de67e27f1a1758559ddfe6e4f787696ba",
    GUA / "MANIFEST.sha256": "6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee",
    GUA / "results_group16_design.json": "bd7002ac0452bc393205e4c8bde61351098f4d2daaee9c081301fab05f1148ce",
    GUA / "rep2_group016_guardpivot_k0_Q.sing": "0e2b917e37159a13cf7e670d29bc2f69427efd576d20585357bc7baa7d1c3ef6",
    GUA / "rep2_group016_guardpivot_k1_Q.sing": "d9fc75cc1a70b7fcf1fa95c4ab53c092f0414d3f817b72402dd8ef688d55f69b",
    GUA / "rep2_group016_guardpivot_k2_Q.sing": "28678ebcccfe054cb78a3f8ce8c0a87fe809fdf38ea5939b7ecb164cf6f4da3b",
    RUN / "TERMINAL_MANIFEST.sha256": "1aad2a2c87918d4ac1b931d97e5da09447b31fb7527fa35c7932fad52d7a2117",
    RUN / "batch_result.json": "1eb6d08fb79b44c76035dba1ed2542b8c006ab9cb4b8217452c01e3223c4ca05",
    RUN / "results/group016.json": "f26a09796fc02e930d069a6acd0a8d77bcefe29b7e35517c1f8ae0634fc5d760",
    RUN / "sources/rep2_group016_Q.sing": "79a2cf5c70cf939e434cf445c98d7a5e132f68ddd2253f7757d06d4450da01c8",
    DES / "generate_design.py": "ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_text(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def replay_manifest(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        target = (path.parent / name.strip()).resolve()
        assert target.is_file() and sha(target) == digest, (target, digest, sha(target))
        count += 1
    return count


def parse_source(path: Path) -> tuple[str, list[str], list[str]]:
    text = path.read_text()
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(";\nprint", 1)[0]
    equations: list[str] = []
    depth = 0
    start = 0
    for pos, char in enumerate(body):
        depth += char == "("
        depth -= char == ")"
        if char == "," and depth == 0:
            equations.append(body[start:pos].strip())
            start = pos + 1
    equations.append(body[start:].strip())
    assert depth == 0
    return text, variables, equations


def token_substitute(text: str, mapping: dict[str, str]) -> str:
    pattern = r"\b(?:" + "|".join(map(re.escape, sorted(mapping, key=len, reverse=True))) + r")\b"
    return re.sub(pattern, lambda match: mapping[match.group()], text)


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text))


def determinant3(matrix: list[list[int]]) -> int:
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def add_weight(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


class WeightParser:
    def __init__(self, text: str, weights: dict[str, tuple[int, ...]]):
        self.items = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]", text)
        self.index = 0
        self.weights = weights

    def expression(self) -> set[tuple[int, ...]]:
        result = self.term()
        while self.index < len(self.items) and self.items[self.index] in "+-":
            self.index += 1
            result |= self.term()
        return result

    def term(self) -> set[tuple[int, ...]]:
        result = self.factor()
        while self.index < len(self.items) and self.items[self.index] == "*":
            self.index += 1
            other = self.factor()
            result = {add_weight(a, b) for a in result for b in other}
        return result

    def factor(self) -> set[tuple[int, ...]]:
        item = self.items[self.index]
        if item == "-":
            self.index += 1
            return self.factor()
        if item == "(":
            self.index += 1
            result = self.expression()
            assert self.items[self.index] == ")"
            self.index += 1
            return result
        self.index += 1
        if item.isdigit():
            return {(0, 0, 0, 0)}
        return {self.weights[item]}


def homogeneous_histogram(
    variables: list[str], equations: list[str], sat_weight: tuple[int, int, int, int]
) -> list[dict[int, int]]:
    bases = {
        "lambda35": {"04": -1, "06": -1, "23": 1, "35": 1},
        "lambda56": {"06": 1, "14": -1, "17": -1, "26": 1, "56": 1},
        "lambda57": {"17": 1, "23": -1, "26": -1, "57": 1},
        "lambda67": {"12": -1, "67": 1},
    }
    names = tuple(bases)
    weights: dict[str, tuple[int, ...]] = {}
    for variable in variables:
        match = re.fullmatch(r"a(\d\d)_\d\d", variable)
        weights[variable] = (
            tuple(bases[name].get(match.group(1), 0) for name in names)
            if match
            else (0, 0, 0, 0)
        )
    for variable in variables:
        if variable.startswith("yn"):
            weights[variable] = (0, 0, 1, 0)
        if variable == "abar" or variable.startswith("t"):
            weights[variable] = (-1, 1, -1, 0)
        if variable == "beta":
            weights[variable] = (1, 0, 0, 0)
        if variable == "sat":
            weights[variable] = sat_weight
    equation_weights = []
    for equation in equations:
        parser = WeightParser(equation, weights)
        found = parser.expression()
        assert parser.index == len(parser.items) and len(found) == 1, (equation, found)
        equation_weights.append(next(iter(found)))
    return [dict(sorted(collections.Counter(x[i] for x in equation_weights).items())) for i in range(4)]


for path, digest in PINS.items():
    assert path.is_file() and sha(path) == digest, (path, sha(path), digest)
torus_manifest_entries = replay_manifest(TOR / "MANIFEST.sha256")
guard_manifest_entries = replay_manifest(GUA / "MANIFEST.sha256")
terminal_manifest_entries = replay_manifest(RUN / "TERMINAL_MANIFEST.sha256")

torus_result = json.loads((TOR / "results_design.json").read_text())
torus_hostiles = json.loads((TOR / "results_hostiles.json").read_text())
guard_result = json.loads((GUA / "results_group16_design.json").read_text())
assert torus_result["status"] == "PASS_EXACT_19_STRATUM_DESIGN_ZERO_SOLVES"
assert guard_result["status"] == "PASS_NO_PREFIX_TRANSPORT_STRICT_88_6574_THREE_CHART_QUOTIENT_ZERO_SOLVES"

# Independently rebuild the parent 91/6577 exact-Q source from the authoritative generator.
spec = importlib.util.spec_from_file_location("rep2_builder", DES / "generate_design.py")
assert spec and spec.loader
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
engine = builder.load_engine()
builder.configure_engine(engine)
record = (0, 0, 0, 1, "z", 2, 0, 1)
program = builder.build_program(engine, record)
epilogue = '''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
rebuilt_parent = (program[: -len("quit;\n")] + epilogue).encode()
parent_path = RUN / "sources/rep2_group016_Q.sing"
assert rebuilt_parent == parent_path.read_bytes()
parent_text, parent_variables, parent_equations = parse_source(parent_path)
assert len(parent_variables) == 91 and len(parent_equations) == len(set(parent_equations)) == 6577

# Recompute the physical character action and its integral (root-free) gauge slice.
bases = {
    "lambda35": {"04": -1, "06": -1, "23": 1, "35": 1},
    "lambda56": {"06": 1, "14": -1, "17": -1, "26": 1, "56": 1},
    "lambda57": {"17": 1, "23": -1, "26": -1, "57": 1},
    "lambda67": {"12": -1, "67": 1},
}
for base in bases.values():
    for matching in builder.SUPPORTED:
        assert sum(base.get("".join(map(str, edge)), 0) for edge in matching) == 0
    assert base.get("57", 0) == base.get("17", 0) + base.get("56", 0)
    assert base.get("56", 0) == base.get("26", 0) + base.get("57", 0)
parent_hist = homogeneous_histogram(parent_variables, parent_equations, (0, -1, -1, 0))
assert parent_hist == [{-1: 6, 0: 6571}, {0: 6571, 1: 6}, {0: 6562, 1: 15}, {0: 6577}]
gauge_matrix = [[1, 0, 0], [-1, 1, -1], [0, 0, 1]]
assert determinant3(gauge_matrix) == 1
# Coordinate exponents are ordered (beta, abar, a57_00).  These are the
# exponents of the chosen torus parameters in those coordinates.
parameter_exponents = {
    "lambda35": (-1, 0, 0),
    "lambda56": (-1, -1, -1),
    "lambda57": (0, 0, -1),
}
add3 = lambda *rows: tuple(sum(row[i] for row in rows) for i in range(3))
assert add3((1, 0, 0), parameter_exponents["lambda35"]) == (0, 0, 0)
assert add3(
    (0, 1, 0),
    tuple(-x for x in parameter_exponents["lambda35"]),
    parameter_exponents["lambda56"],
    tuple(-x for x in parameter_exponents["lambda57"]),
) == (0, 0, 0)
assert add3((0, 0, 1), parameter_exponents["lambda57"]) == (0, 0, 0)

# Rebuild all 19 producer sources byte-for-byte from the parent source.
a67 = [f"a67_{i}{j}" for i, j in itertools.product(range(3), repeat=2)]
a12 = [f"a12_{i}{j}" for i, j in itertools.product(range(3), repeat=2)]
base_gauge = {"beta": "1", "abar": "1", "a57_00": "1"}
strata: list[tuple[str, str | None, dict[str, str], str]] = []
for variable in a67:
    strata.append(("A67_entry_open", variable, {**base_gauge, variable: "1"}, f"group16_A67open_{variable[-2:]}_Q_design.sing"))
zero67 = {variable: "0" for variable in a67}
for variable in a12:
    strata.append(("A67_zero_A12_entry_open", variable, {**base_gauge, **zero67, variable: "1"}, f"group16_A67zero_A12open_{variable[-2:]}_Q_design.sing"))
strata.append(("A67_zero_A12_zero", None, {**base_gauge, **zero67, **{v: "0" for v in a12}}, "group16_A67zero_A12zero_Q_design.sing"))
producer_ledger = {(entry["kind"], entry["pivot"]): entry for entry in torus_result["decomposition"]["sources"]}
rebuilt_strata = []
for kind, pivot, mapping, filename in strata:
    new_variables = [variable for variable in parent_variables if variable not in mapping]
    new_equations = [token_substitute(equation, mapping) for equation in parent_equations]
    assert len(new_equations) == len(set(new_equations)) == 6577
    assert all(equation not in {"0", "1", "-1"} for equation in new_equations)
    expected = "\n".join(
        [
            "// REP2 GROUP16 TORUS-GAUGE DESIGN INPUT ONLY: zero ideal runs authorized.",
            "option(noredefine);",
            f"ring r=0,({','.join(new_variables)}),dp;",
            "ideal I=" + ",\n".join(new_equations) + ";",
            'print("INPUT_VARIABLES="+string(nvars(r)));',
            'print("INPUT_GENERATORS="+string(size(I)));',
            "quit;",
            "",
        ]
    )
    emitted = TOR / "sources" / filename
    assert emitted.read_text() == expected
    removed = set(mapping)
    assert not (tokens(expected) & removed)
    record_out = producer_ledger[(kind, pivot)]
    assert sha(emitted) == record_out["sha256"] and emitted.stat().st_size == record_out["bytes"]
    assert record_out["variables"] == len(new_variables) and record_out["generators"] == 6577
    rebuilt_strata.append(
        {
            "kind": kind,
            "pivot": pivot,
            "source": filename,
            "sha256": sha(emitted),
            "variables": len(new_variables),
            "generators": len(new_equations),
            "removed_symbol_count": len(removed),
            "removed_symbols_absent": True,
        }
    )
assert collections.Counter(x["variables"] for x in rebuilt_strata) == collections.Counter({87: 9, 78: 9, 70: 1})

# Check the exact finite cover, producer hostiles, and consumed timeout nonreuse.
assert len(strata) == 19 and len({filename for _, _, _, filename in strata}) == 19
assert torus_result["decomposition"]["cover_identity"] == "union_{i,j} D(A67_ij) plus V(A67) intersect union_{i,j} D(A12_ij) plus V(A67,A12)"
expected_hostiles = {
    "automorphism_overclaim", "closure", "drop_stratum", "duplicate_generator",
    "guard_weight", "matching_weight", "omit_unit", "performance", "relaunch",
    "run", "symmetry_overclaim", "trivial_generator", "variable_overclaim", "wrong_gauge_det",
}
assert torus_hostiles["status"] == "PASS_14_HOSTILES_ZERO_RUN"
assert torus_hostiles["hostile_count"] == 14
assert set(torus_hostiles["hostile_tests"]) == expected_hostiles
assert all(torus_hostiles["hostile_tests"].values())
lane = json.loads((RUN / "results/group016.json").read_text())
batch = json.loads((RUN / "batch_result.json").read_text())
assert lane["status"] == "FAIL_CLOSED_RESOURCE" and lane["termination"] == "NATIVE_WALL_CAP_240"
assert lane["automatic_relaunch"] is False and lane["source_sha256"] == sha(parent_path)
assert batch["stop"] == {"group_id": 16, "status": "FAIL_CLOSED_RESOURCE"} and batch["relaunch"] is False
assert torus_result["consumed_attempt"]["relaunch_authorized"] is False

# The three guard-pivot quotient ideals remain torus-homogeneous when their new
# inverse variable is assigned the correct weight -(wt(P)+wt(b_k)).  Thus the
# gauge slices and guard localizations commute as exact locally closed charts.
guard_sources = []
for k in range(3):
    path = GUA / f"rep2_group016_guardpivot_k{k}_Q.sing"
    text, variables, equations = parse_source(path)
    assert len(variables) == 88 and len(equations) == len(set(equations)) == 6574
    histogram = homogeneous_histogram(variables, equations, (0, -2, -1, 0))
    assert histogram == [{-1: 6, 0: 6568}, {0: 6568, 1: 6}, {0: 6562, 1: 12}, {0: 6574}]
    guard_sources.append((text, variables, equations, histogram))

# Intersect both exact covers.  Applying every torus specialization to each
# guard-pivot source produces 57 strict sources, all smaller than the parent.
intersection_ledger = []
materialized_candidates = []
for k, (guard_text, guard_variables, guard_equations, _) in enumerate(guard_sources):
    for stratum_index, (kind, pivot, mapping, filename) in enumerate(strata):
        new_variables = [variable for variable in guard_variables if variable not in mapping]
        new_equations = [token_substitute(equation, mapping) for equation in guard_equations]
        assert len(new_equations) == len(set(new_equations)) == 6574
        assert all(equation not in {"0", "1", "-1"} for equation in new_equations)
        assert not (tokens(" ".join(new_variables + new_equations)) & set(mapping))
        body = "\n".join(
            [
                "// REP2 GROUP16 TORUS x GUARD-PIVOT EXACT-Q PILOT INPUT; no run authorized.",
                "option(noredefine);",
                f"ring r=0,({','.join(new_variables)}),dp;",
                "ideal I=" + ",\n".join(new_equations) + ";",
                'print("INPUT_VARIABLES="+string(nvars(r)));',
                'print("INPUT_GENERATORS="+string(size(I)));',
                "ideal G=slimgb(I);",
                'print("GROEBNER_SIZE="+string(size(G)));',
                "poly remainder=reduce(1,G);",
                'print("UNIT_REMAINDER="+string(remainder));',
                'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
                "quit;",
                "",
            ]
        )
        equation_bytes = len(("\n".join(new_equations)).encode())
        record_out = {
            "guard_pivot_k": k,
            "torus_stratum_index": stratum_index,
            "torus_kind": kind,
            "torus_pivot": pivot,
            "torus_source": filename,
            "variables": len(new_variables),
            "generators": len(new_equations),
            "unique_generators": len(set(new_equations)),
            "trivial_generators": 0,
            "equation_bytes": equation_bytes,
            "prospective_source_bytes": len(body.encode()),
            "prospective_source_sha256": hashlib.sha256(body.encode()).hexdigest(),
        }
        intersection_ledger.append(record_out)
        materialized_candidates.append((record_out, body))
assert collections.Counter((x["variables"], x["generators"]) for x in intersection_ledger) == collections.Counter({(84, 6574): 27, (75, 6574): 27, (67, 6574): 3})

# Honest pilot selection: minimum variable count, then equation serialization,
# then the stable guard-pivot/stratum order.  A pilot only decides its one open;
# no single member of the 57-cover is logically sufficient for all group16.
selected_record, selected_body = min(
    materialized_candidates,
    key=lambda item: (
        item[0]["variables"], item[0]["equation_bytes"],
        item[0]["guard_pivot_k"], item[0]["torus_stratum_index"],
    ),
)
assert selected_record["variables"] == 67 and selected_record["guard_pivot_k"] == 0
assert selected_record["torus_kind"] == "A67_zero_A12_zero"
selected_name = "rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing"
atomic_text(H / selected_name, selected_body)
assert sha(H / selected_name) == selected_record["prospective_source_sha256"]
atomic_text(H / "combined_57_ledger.json", json.dumps(intersection_ledger, indent=2, sort_keys=True) + "\n")

result = {
    "schema": "KRENN_X5_REP2_GROUP16_TORUS_GAUGE_INDEPENDENT_REFEREE_COMPARISON_V1",
    "status": "PASS_TORUS_19_EXACT_AND_SOUND_57_INTERSECTION_ZERO_SOLVES",
    "producer_audit": {
        "manifest_sha256": sha(TOR / "MANIFEST.sha256"),
        "result_sha256": sha(TOR / "results_design.json"),
        "manifest_entries_replayed": torus_manifest_entries,
        "parent_source_byte_rebuilt": True,
        "parent_source_sha256": sha(parent_path),
        "parent_variables": len(parent_variables),
        "parent_generators": len(parent_equations),
        "character_matrix": gauge_matrix,
        "character_matrix_determinant": determinant3(gauge_matrix),
        "root_free_gauge_parameters": {
            "lambda35": "beta^-1",
            "lambda57": "a57_00^-1",
            "lambda56": "(abar*beta*a57_00)^-1",
        },
        "gauge_equivalence": "On D(beta*abar*a57_00), the displayed integral monomial parameters send all three coordinates to one; determinant 1 makes this a torus-coordinate isomorphism with an integral monomial inverse. Residual lambda67 then sets a nonzero A67 entry to one, or after A67=0 sets a nonzero A12 entry to one, without extracting roots.",
        "parent_polynomial_weight_histograms": parent_hist,
        "matching_weights_zero": True,
        "guard_equations_character_homogeneous": True,
        "source_rebuilds": rebuilt_strata,
        "source_histogram": {"87_variables": 9, "78_variables": 9, "70_variables": 1},
        "all_sources_6577_unique_nontrivial": True,
        "all_removed_symbols_token_absent": True,
        "finite_cover": "D(A67 entries) OR [A67=0 and D(A12 entries)] OR [A67=A12=0]",
        "finite_cover_exact": True,
        "hostile_count_replayed": 14,
        "hostile_names": sorted(expected_hostiles),
        "hostiles_all_pass": True,
        "consumed_timeout": "NATIVE_WALL_CAP_240",
        "consumed_timeout_mathematical_coverage": False,
        "timeout_reuse_or_relaunch_authorized": False,
        "singular_runs": 0,
    },
    "guard_pivot_audit": {
        "manifest_sha256": sha(GUA / "MANIFEST.sha256"),
        "manifest_entries_replayed": guard_manifest_entries,
        "chart_count": 3,
        "variables_each": 88,
        "generators_each": 6574,
        "cover": "D(b0) union D(b1) union D(b2)",
        "b_definition": "b_h=sum_l A26[h,l]*A57[0,l]",
        "b_character": "lambda56 (the same nonzero scalar character for all h)",
        "new_inverse_weight": [0, -2, -1, 0],
        "quotient_weight_histograms": guard_sources[0][3],
        "torus_stable": True,
    },
    "exact_comparison": {
        "commutation_proof": "The torus scales every b_h by the same lambda56 character, hence preserves each D(b_h). Localizing at a torus gauge coordinate and at b_h commutes. The guard monic substitution is equivariant with sat_new weight -(wt(P)+wt(b_h)); literal torus specialization of each exact guard source is therefore the intersection source.",
        "cover_identity": "X=(union_s T_s) intersect (union_k D(b_k))=union_{s,k}(T_s intersect D(b_k))",
        "intersection_chart_count": 57,
        "intersection_histogram": {"84_variables_6574_generators": 27, "75_variables_6574_generators": 27, "67_variables_6574_generators": 3},
        "all_unique_nontrivial": True,
        "combined_ledger": "combined_57_ledger.json",
        "combined_ledger_sha256": sha(H / "combined_57_ledger.json"),
        "strictly_smaller_per_chart": True,
        "chart_count_tradeoff": "19 torus charts or 3 guard charts become 57 intersection charts",
        "single_chart_closes_group16": False,
        "full_group16_requirement": "Every one of the 57 intersection ideals must be proved unit, absent a further valid implication or symmetry quotient.",
    },
    "smallest_exact_pilot": {
        **selected_record,
        "path": selected_name,
        "sha256": sha(H / selected_name),
        "selection_rule": "minimum variables, then equation bytes, then guard pivot k and torus stratum order",
        "logical_scope": "V(A67,A12) intersect D(b0) only",
        "sufficient_for_its_localization": True,
        "sufficient_for_group16": False,
        "solver_runs": 0,
        "launch_authorized": False,
    },
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "scope": {
        "design_referee_only": True,
        "singular_runs": 0,
        "ideal_runs": 0,
        "group16_closed": False,
        "rep2_closed": False,
        "pilot_launch_authorized": False,
    },
}
atomic_text(H / "results_referee_comparison.json", json.dumps(result, indent=2, sort_keys=True) + "\n")

report = f"""# Rep2 group16 torus-gauge independent referee and exact cover comparison

Status: **{result['status']}**.

The producer manifest and every pinned source replay.  The determinant-one character
matrix gives a root-free gauge fixing of `beta`, `abar`, and `a57_00`.  Independent
literal reconstruction reproduces all 19 sources byte-for-byte: nine 87-variable,
nine 78-variable, and one 70-variable source, each with 6,577 distinct nontrivial
generators and no removed variable token.  The 14 hostile outcomes pass.  The prior
group16 attempt remains a `NATIVE_WALL_CAP_240` with zero mathematical coverage and
explicit nonreuse.

The three guard-pivot quotients are equivariant after assigning their new inverse
variable weight `(0,-2,-1,0)`.  Since each `b_k` scales by the same nonzero
`lambda56` character, the two covers may be intersected exactly.  This yields 57
sources: 27 at 84/6574, 27 at 75/6574, and 3 at 67/6574.  The gain in per-source
size therefore costs a 57-chart cover; it is not a one-chart closure.

The deterministic smallest exact pilot is `{selected_name}` (SHA-256
`{sha(H / selected_name)}`), the 67-variable/6,574-generator `A67=A12=0`, `D(b0)`
intersection.  A UNIT result would close only that localization.  Closing group16
by this combined decomposition requires all 57 intersections unless a separate
exact implication or symmetry reduction is proved.

No Singular process or ideal computation was launched.
"""
atomic_text(H / "REPORT.md", report)
print(json.dumps({"status": result["status"], "strata": 19, "intersections": 57, "smallest": [67, 6574], "singular_runs": 0}, sort_keys=True))
