#!/usr/bin/env python3
"""Design-only split of the nine-block residual 538 records."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
NINE = REPO / "computations/unaudited-codex-n8-x5-nine-block-induction-census-design-2026-08-26"
EIGHT_SOURCE = REPO / "computations/unaudited-codex-n8-x5-eight-block-first-induction-interface-2026-08-26/build_interface.py"
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
N08 = CROSS / "claims/finite/n08"
PINS = {
    "nine_manifest": (NINE / "MANIFEST.sha256", "edd2a501351e72fa58b4fc1d60bf473693b1dafe7ad46d45941ffca28bafdbcb"),
    "nine_result": (NINE / "results_nine_block_induction_census.json", "3d5bbf37a8e897e0a1fed37583bc7585d871ee309501055bd98e8f0f3e7f6e57"),
    "corrected_carrier_source": (EIGHT_SOURCE, "3467f0b2b5997d1739d76a50d7ec0ae0734b4f099608a511d893309a488e5894"),
    "current_max17_base_generator": (N08 / "eight_vertex_local_degree4_support.py", "83996bdb4da059de2490549ed07fbb225b024e21763a8db4cf871fb0228cb0bb"),
    "current_support_library": (CROSS / "src/krenn_gu/rankone_support_sat.py", "c795681f2d13a7bc5044572ccf89a532402bb885dde7b5772898f156a6a8bed6"),
    "current_matching_library": (CROSS / "src/krenn_gu/search_witness.py", "bcf0a3fa7856638244f59a4c9e6d78618fe697317700fe88dcc7ff53bda37d45"),
    "current_bootstrap": (CROSS / "src/krenn_gu/bootstrap.py", "ad7cbde17b1a10ced86b925af649a0fe6f3a2630cc31445b580ce042ac97b7a7"),
    "current_skeleton_batch": (N08 / "eight_vertex_skeleton_laurent_batch.py", "46406e54a62d41f48ddee06263c2070fb26d3a35d83b72d57ac6528f3716d7fc"),
    "current_selector_builder": (N08 / "eight_vertex_16edge_catalogue_cnf.py", "d895292ad695a243e8962c10941cb491bb28e757629e6c289911ee6952c1e7b8"),
    "current_batch_verifier": (N08 / "verify_skeleton_laurent_batch.py", "081bcf474ba99f2aa1c7380de7c80d00acb0591ded1ff872d9a60f38047dc168"),
    "current_laurent_verifier": (N08 / "verify_laurent_batch_manifest.py", "a13249d1427d70738fdb0404275036fb7f39f8ca01dfb0c6c0aac24b90eacbf5"),
    "current_selector_verifier": (N08 / "verify_catalogue_selector.py", "95b2efa4bc1aeea53b25bee88d410e05e2fb07a4a5d0fb42262208f7c2804047"),
    "historical_e17_terminal_verifier": (N08 / "verify_eight_vertex_degree4_e17.py", "eb02bfafed67f827675a663a1bd7b06391ddbe30f8a29876957fe90cee21330a"),
    "four_regular_interface": (N08 / "EIGHT_VERTEX_4REGULAR_CERTIFICATE.md", "3a8effa369101ea218d4cce21c501e61c9211bbb15e2565a0f7099dffaf65f57"),
    "degree3_exact19_interface": (N08 / "EIGHT_VERTEX_DEGREE3_E19_CERTIFICATE.md", "8aa7430af239a661cf0d75951d36902f1d49bfec5c61b2ed1bd8e4a80ea2d240"),
    "max_degree5_balanced_bridge_interface": (CROSS / "claims/arbitrary-order/FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md", "4026b1b1c5dfa11b4b4b5ee4f96a9b5a67f8f598df5c16d997050856e8b671ea"),
}


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


for name, (path, expected) in PINS.items():
    require(path.is_file(), (name, "missing"))
    observed = sha(path)
    require(observed == expected, (name, observed, expected))

spec = importlib.util.spec_from_file_location("carrier_source", EIGHT_SOURCE)
require(spec is not None and spec.loader is not None)
carrier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(carrier)

FIXED = frozenset(tuple(map(int, edge)) for edge in ("03", "16", "27", "45"))
ACTIVE_VARIABLE = frozenset(tuple(map(int, edge)) for edge in ("04", "35", "67"))


def edge_string(edge):
    return "".join(map(str, edge))


def permute_edge(edge, permutation):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def permute_support(support, permutation):
    return frozenset(permute_edge(edge, permutation) for edge in support)


def perfect_matchings(support):
    return tuple(sorted(
        tuple(sorted(edge_string(edge) for edge in matching))
        for matching in carrier.five.core.PM8 if set(matching) <= support
    ))


def carrier_census(support):
    rows = []
    for cap in sorted(support):
        residual = tuple(vertex for vertex in range(8) if vertex not in cap)
        for triangle in itertools.combinations(residual, 3):
            load = carrier.carrier_term_count(support, cap, "triangle", triangle)
            rows.append((load, "triangle", edge_string(cap), "".join(map(str, triangle))))
        for center in residual:
            load = carrier.carrier_term_count(support, cap, "star", (center,))
            rows.append((load, "star", edge_string(cap), str(center)))
    minimum = min(row[0] for row in rows)
    return {
        "load_histogram": {str(k): v for k, v in sorted(Counter(row[0] for row in rows).items())},
        "minimum_load": minimum,
        "minimum_carriers": [list(row[1:]) for row in rows if row[0] == minimum],
    }


def response_terms(support, cap, response):
    return carrier.stored_product_terms(support, cap, response)


def make_result():
    nine = json.loads((NINE / "results_nine_block_induction_census.json").read_text())
    records = nine["records"]
    exact17 = [record for record in records if record["essential_edge_count"] == 17 and record["has_degree_four_vertex"]]
    exceptions = [record for record in records if not record["has_degree_four_vertex"]]
    require(len(exact17) == 534 and len(exceptions) == 4)

    exact17_indices = {record["record_index"] for record in exact17}
    exact17_orbits = [orbit for orbit in nine["literal_guard_orbits"] if set(orbit["record_indices"]) <= exact17_indices]
    require(len(exact17_orbits) == 267)
    require(all(len(orbit["record_indices"]) == 2 for orbit in exact17_orbits))
    require(set(i for orbit in exact17_orbits for i in orbit["record_indices"]) == exact17_indices)
    exact17_graphs = {}
    for record in exact17:
        exact17_graphs.setdefault(record["unlabelled_graph_id"], []).append(record["record_index"])
    require(len(exact17_graphs) == 50)
    require(Counter(map(len, exact17_graphs.values())) == {4: 5, 8: 26, 10: 1, 12: 3, 16: 14, 36: 1})
    require(Counter(len(record["unresolved_eight_deletion_parents"]) for record in exact17) == {0: 80, 1: 70, 2: 320, 3: 54, 4: 10})

    exception_indices = {record["record_index"] for record in exceptions}
    require(exception_indices == {1114, 1978, 2014, 2036})
    require({record["unlabelled_graph_id"] for record in exceptions} == {"4200930318e1e084e98b97bd783b8dfd0e3e809fd07f162b758ef6dd83cbe17c"})
    exception_orbits = [orbit for orbit in nine["literal_guard_orbits"] if set(orbit["record_indices"]) <= exception_indices]
    require([orbit["record_indices"] for orbit in exception_orbits] == [[1114, 1978], [2014, 2036]])

    exception_details = []
    support_by_index = {}
    for record in exceptions:
        support = frozenset(tuple(map(int, edge)) for edge in record["essential_edges"])
        support_by_index[record["record_index"]] = support
        degree = Counter(vertex for edge in support for vertex in edge)
        matchings = perfect_matchings(support)
        require(tuple(sorted(degree.values())) == (3, 3, 3, 3, 5, 5, 5, 5))
        require(len(matchings) == 15)
        census = carrier_census(support)
        require(census["minimum_load"] == 2 and len(census["minimum_carriers"]) == 16)
        exception_details.append({
            "record_index": record["record_index"],
            "added": record["added"],
            "active_variable_blocks": record["nonzero_variable_blocks"],
            "essential_edges": record["essential_edges"],
            "degree_by_vertex": {str(v): degree[v] for v in range(8)},
            "degree_sequence": list(sorted(degree.values())),
            "supported_perfect_matchings": ["|".join(matching) for matching in matchings],
            "unresolved_eight_deletion_parents": record["unresolved_eight_deletion_parents"],
            "carrier_census": census,
        })

    # Full source-site symmetry is larger than the formal guard symmetry.
    # It preserves the four fixed identity blocks and the active variable
    # family {04,35,67}; GHZ is invariant under every site permutation.
    transport_group = []
    for permutation in itertools.permutations(range(8)):
        if permute_support(FIXED, permutation) == FIXED and permute_support(ACTIVE_VARIABLE, permutation) == ACTIVE_VARIABLE:
            transport_group.append(permutation)
    require(len(transport_group) == 8)
    representative = support_by_index[1114]
    transport = {}
    for target in sorted(exception_indices):
        mapping = next((permutation for permutation in transport_group if permute_support(representative, permutation) == support_by_index[target]), None)
        require(mapping is not None, ("transport missing", target))
        # Literal matching transport checks the full degree-four monomial map.
        require(
            tuple(sorted(tuple(sorted(edge_string(permute_edge(tuple(map(int, edge)), mapping)) for edge in matching)) for matching in perfect_matchings(representative))) ==
            perfect_matchings(support_by_index[target])
        )
        transport[str(target)] = list(mapping)

    rep = representative
    selected_response_terms = {
        "cap01_star3_R46": response_terms(rep, (0, 1), (4, 6)),
        "cap01_star3_R47": response_terms(rep, (0, 1), (4, 7)),
        "cap25_star4_R36": response_terms(rep, (2, 5), (3, 6)),
        "cap25_star4_R37": response_terms(rep, (2, 5), (3, 7)),
    }
    require(selected_response_terms == {
        "cap01_star3_R46": [{"kind": "direct", "source_edges": ["04", "16"]}],
        "cap01_star3_R47": [{"kind": "direct", "source_edges": ["04", "17"]}],
        "cap25_star4_R36": [{"kind": "switched", "source_edges": ["26", "35"]}],
        "cap25_star4_R37": [{"kind": "switched", "source_edges": ["27", "35"]}],
    })

    held = {
        "schema": "n8-current-source-max17-regeneration-held-v1",
        "status": "HELD_ZERO_MATERIALIZATION_NO_CLEARANCE",
        "logical_scope": "exactly17 matching-essential edges with a degree-four vertex",
        "covered_current_nine_records_if_terminal": 534,
        "scheduling_dependencies": {
            "fresh_max15_terminal_manifest": None,
            "fresh_max16_terminal_manifest": None,
            "explicit_resource_clearance": None,
            "note": "scheduling hold only; max17 is logically a separate exact-edge theorem",
        },
        "commands": [
            {
                "stage": "base_current_source_cnf",
                "command": "python claims/finite/n08/eight_vertex_local_degree4_support.py --minimum-degree 3 --maximum-edges 17 --center-degree 4 --write-only --cnf SCRATCH/base_max17.cnf --output SCRATCH/base_max17.json",
                "acceptance": "current pinned sources; NOT_SOLVED; exact generated header/hash recorded atomically",
            },
            {
                "stage": "exact17_graph_catalogue",
                "command": "PINNED_GENG -c -d3 8 17:17 > SCRATCH/n8_mindeg3_e17.g6.tmp",
                "acceptance": "pinned nauty required; atomic graph6; independent decode gives 420 connected matching-covered degree4 skeletons",
            },
            {
                "stage": "current_exact_conflict_batch",
                "command": "python claims/finite/n08/eight_vertex_skeleton_laurent_batch.py --graph6 SCRATCH/n8_mindeg3_e17.g6 --target-edges 17 --center-degree 4 --cnf SCRATCH/base_max17.cnf --output SCRATCH/batch.json --learned-cnf SCRATCH/learned.cnf --learned-manifest SCRATCH/learned.json --prefer-transport --fallback-limit 1",
                "acceptance": "all 11051 canonical roles processed/UNSAT; zero unresolved fallback; every exact conflict independently replayable",
            },
            {
                "stage": "selector_compile",
                "command": "python claims/finite/n08/eight_vertex_16edge_catalogue_cnf.py --graph6 SCRATCH/n8_mindeg3_e17.g6 --target-edges 17 --center-degree 4 --expected-roles 11051 --base-cnf SCRATCH/learned.cnf --output SCRATCH/selector.cnf --manifest SCRATCH/selector.json",
                "acceptance": "source-rebuilt role union; base-prefix hash equality; atomic selector",
            },
            {
                "stage": "decision_and_independent_replay",
                "command": "PINNED_CADICAL SCRATCH/selector.cnf SCRATCH/proof.drat; PINNED_DRAT_TRIM SCRATCH/selector.cnf SCRATCH/proof.drat",
                "acceptance": "CaDiCaL UNSAT plus independent literal s VERIFIED; all current source/tool/input/output hashes sealed",
            },
        ],
        "required_new_pins_before_launch": ["nauty/geng binary", "scratch free-space floor", "watchdog wall/RSS geometry", "max15/max16 process-clear manifests", "fresh nonce clearance"],
        "historical_dimensions_are_diagnostics_only": {"roles": 11051, "selector_variables": 439322, "selector_clauses": 3349145, "proof_bytes": 853663837},
        "refusal": "do not generate or read base/selector CNF, graph6, conflict batch, or proof until dependencies and explicit clearance are non-null",
    }
    (HERE / "max17_current_source_held_contract.json").write_text(json.dumps(held, indent=2, sort_keys=True) + "\n")

    return {
        "schema": "n8-x5-nine-block-residual538-max17-held-design-v1",
        "status": "PASS_DESIGN_ONLY_ZERO_HEAVY_RUN",
        "pins": {name: {"path": str(path), "sha256": expected} for name, (path, expected) in PINS.items()},
        "residual_ledger": {
            "input_records": 538,
            "exact17_degree4_records": 534,
            "exact16_without_degree4_records": 4,
            "accepted_coverage_now": 0,
            "remaining_now": 538,
        },
        "exact17_degree4": {
            "records": 534,
            "literal_guard_orbits": 267,
            "unlabelled_graph_classes": 50,
            "graph_class_size_census": {str(k): v for k, v in sorted(Counter(map(len, exact17_graphs.values())).items())},
            "eight_parent_count_histogram": {str(k): v for k, v in sorted(Counter(len(record["unresolved_eight_deletion_parents"]) for record in exact17).items())},
            "new_minimal_records": 80,
            "supported_matching_histogram": {str(k): v for k, v in sorted(Counter(record["supported_perfect_matching_count"] for record in exact17).items())},
            "degree_sequence_histogram": {
                str(k): v for k, v in sorted(Counter(tuple(record["degree_sequence"]) for record in exact17).items())
            },
            "record_indices": sorted(exact17_indices),
            "record_indices_sha256": canonical_hash(sorted(exact17_indices)),
            "guard_orbits": exact17_orbits,
            "graph_classes": [{"graph_id": key, "record_indices": value} for key, value in sorted(exact17_graphs.items())],
            "held_contract": "max17_current_source_held_contract.json",
            "held_contract_sha256": sha(HERE / "max17_current_source_held_contract.json"),
        },
        "exact16_no_degree4": {
            "records": 4,
            "formal_guard_orbits": 2,
            "unlabelled_graph_classes": 1,
            "full_source_site_transport_orbits": 1,
            "source_site_transport_group_order": len(transport_group),
            "representative_record": 1114,
            "transport_from_representative": transport,
            "transport_proof": "permutation preserves fixed I blocks and active variable-family set; every supported matching maps bijectively; word permutation preserves GHZ, with edge reversals mapped by matrix transpose",
            "records_detail": exception_details,
            "known_interface_tests": {
                "degree4_max16_or_max17": "NOT_APPLICABLE: no degree-four vertex",
                "four_regular": "NOT_APPLICABLE: degree sequence is (3^4,5^4), not (4^8)",
                "five_regular": "NOT_APPLICABLE: neither (5^8) nor exact20",
                "degree3_exact18_or_exact19": "NOT_APPLICABLE: exactly16 edges",
                "max_degree5_balanced_all_bridge": "PREMISE_MISSING: maximum degree5 holds, but simultaneous balanced all-bridge normal form is not established for this source branch",
            },
            "representative_formal_guard_cap67_triangle012": [
                "R13: A37^T + A17*A36^T = 0",
                "R14: A47^T + A17*A46^T = 0",
                "R23: A26*A37^T + A36^T = 0",
                "R24: A26*A47^T + A46^T = 0",
                "R34: A36*A47^T + A37*A46^T = 0",
            ],
            "guard_rank_consequence": "if A37 or A47 is invertible, then A17 and A26 are invertible and A17*A26=I3",
            "selected_two_term_carriers": {
                "source_terms": selected_response_terms,
                "cap01_star3": "L(K)=(A04^T*K, A04^T*K*A17); W=Col(A04) tensor Q^3",
                "cap25_star4": "transpose-equivalent L with common A35 and identity partner A27",
                "activity_open_condition_cap01": "rank(A04)<3, no coordinate e_i lies in Col(A04), and Col(A01) is not contained in Col(A04)",
                "hard_boundary": "all minimum-load carriers have zero kernel when A04,A17,A35,A26 are invertible; incidence subloci when one is singular remain, and higher-load carriers were not eliminated",
            },
            "remaining_exact_obligation": "one source-transport representative, split by ranks/incidences of A04,A17,A35,A26 under the five displayed guards and all 6561 X5 amplitudes",
        },
        "scope": {
            "large_cnf_materialized_or_read": False,
            "sat_or_drat_runs": 0,
            "singular_runs": 0,
            "external_theorem_promoted": False,
            "residual_closed": False,
            "full_conjecture_claim": False,
        },
    }


if __name__ == "__main__":
    result = make_result()
    (HERE / "results_residual538_design.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "exact17": {k: result["exact17_degree4"][k] for k in ("records", "literal_guard_orbits", "unlabelled_graph_classes", "new_minimal_records")},
        "exceptions": {k: result["exact16_no_degree4"][k] for k in ("records", "formal_guard_orbits", "unlabelled_graph_classes", "full_source_site_transport_orbits", "representative_record")},
        "scope": result["scope"],
    }, indent=2, sort_keys=True))
