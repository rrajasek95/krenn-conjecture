#!/usr/bin/env python3
"""Exact essential-skeleton census and one reduced eight-block held chart.

This is a design-only bridge.  It deliberately does not import any legacy
degree-four SAT theorem and it never invokes Singular.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-eight-block-first-induction-interface-2026-08-26"
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
PREFLIGHT = CROSS / "docs/audits/eight-vertex-degree4-at-most15-regeneration-preflight-2026-08-26"

PINS = {
    "corrected_parent_manifest": (
        PARENT / "MANIFEST.sha256",
        "4334804545c7f2a73189137f47bfa1105905db4d6b2c52de0d140217d9ae4a10",
    ),
    "corrected_parent_result": (
        PARENT / "results_eight_block_interface.json",
        "886ae50bede93dd21bf0ea5dda7ed9154a58a9caf532aabc306537640473cf25",
    ),
    "corrected_parent_source": (
        PARENT / "build_interface.py",
        "3467f0b2b5997d1739d76a50d7ec0ae0734b4f099608a511d893309a488e5894",
    ),
    "max15_prelaunch_manifest": (
        PREFLIGHT / "PRELAUNCH_MANIFEST.sha256",
        "c7863b379226664cffd7c176d364840a75bae494c1ecd6584b1ce75a78eac627",
    ),
    "max15_preflight_report": (
        PREFLIGHT / "REPORT.md",
        "bbc084d1dfa7ad986553819f1ff95566cbf1273855a173f731fb146dbc7c159e",
    ),
    "max15_resource_plan": (
        PREFLIGHT / "RESOURCE_PLAN.json",
        "e1242c22b86358a1debd37726fdfe097dbde4ed667f8d26d58e1ac2d39ed6768",
    ),
    "max15_soundness_audit": (
        PREFLIGHT / "SOUNDNESS_AUDIT.md",
        "e7c7568398a7c337f999bd89cfd8cd84081d34f8a18a287be0e56964e63530fb",
    ),
    # These identify historical exact-16/17 interfaces only.  Their proof
    # bundles are not imported as accepted premises by this package.
    "historical_exact16_generator": (
        CROSS / "claims/finite/n08/eight_vertex_16edge_catalogue_cnf.py",
        "d895292ad695a243e8962c10941cb491bb28e757629e6c289911ee6952c1e7b8",
    ),
    "historical_exact16_verifier": (
        CROSS / "claims/finite/n08/verify_eight_vertex_16edge.py",
        "c821c7fe44581483630fd0406e0a683dc0d5384f0469ef80c247de1f3aeaaf0e",
    ),
    "historical_exact17_verifier": (
        CROSS / "claims/finite/n08/verify_eight_vertex_degree4_e17.py",
        "eb02bfafed67f827675a663a1bd7b06391ddbe30f8a29876957fe90cee21330a",
    ),
    "historical_exact17_map": (
        CROSS / "claims/finite/n08/EIGHT_VERTEX_17EDGE_CERTIFICATE.md",
        "c66bb3be46ff52b453af7e3db6aa1ea46a3a87f11bd1d80d5508d9d7bb1931bd",
    ),
}

FIXED = frozenset(("03", "16", "27", "45"))
GUARD_PERMUTATION = (0, 2, 1, 3, 4, 5, 7, 6)
ORBIT1_MATCHINGS = (
    "01|26|35|47",
    "01|27|35|46",
    "03|15|26|47",
    "03|15|27|46",
    "03|16|27|45",
    "03|17|26|45",
    "07|15|23|46",
    "07|16|23|45",
)
ORBIT1_BLOCKS = ("01", "07", "15", "17", "23", "26", "35", "46", "47")
ORBIT1_TORUS_BASIS = (
    (0, -1, 0, 0, 1, 0, 0, 0, 0),
    (-1, 0, 0, 0, 0, 0, 1, 0, 0),
    (-1, 0, -1, -1, 0, 1, 0, 1, 0),
    (0, 0, 0, 1, 0, -1, 0, 0, 1),
)


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_hash(value) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def edge_tuple(edge: str) -> tuple[int, int]:
    require(len(edge) == 2 and edge[0] < edge[1], ("bad edge", edge))
    return int(edge[0]), int(edge[1])


def permute_edge(edge: str) -> str:
    a, b = edge_tuple(edge)
    a, b = GUARD_PERMUTATION[a], GUARD_PERMUTATION[b]
    return f"{min(a, b)}{max(a, b)}"


def essential_edges(record) -> tuple[str, ...]:
    answer = set()
    for matching in record["supported_perfect_matchings"]:
        edges = matching.split("|")
        require(len(edges) == 4)
        vertices = [v for edge in edges for v in edge_tuple(edge)]
        require(sorted(vertices) == list(range(8)), ("not perfect", matching))
        answer.update(edges)
    return tuple(sorted(answer))


def degree_sequence(edges: tuple[str, ...]) -> tuple[int, ...]:
    degree = Counter(v for edge in edges for v in edge_tuple(edge))
    require(set(degree) == set(range(8)))
    return tuple(sorted(degree.values()))


def canonical_unlabelled_graph(edges: tuple[str, ...]) -> tuple[tuple[int, int], ...]:
    """Canonical graph key, exhaustively within invariant degree cells.

    Canonical positions are ordered by degree.  Every graph isomorphism maps
    equal-degree cells to equal-degree cells, so the product of within-cell
    permutations is exhaustive, not a heuristic hash.
    """
    parsed = tuple(map(edge_tuple, edges))
    degree = {v: sum(v in edge for edge in parsed) for v in range(8)}
    cells = tuple(tuple(v for v in range(8) if degree[v] == d)
                  for d in sorted(set(degree.values())))
    best = None
    for choices in itertools.product(*(itertools.permutations(cell) for cell in cells)):
        order = tuple(itertools.chain.from_iterable(choices))
        position = {old: new for new, old in enumerate(order)}
        key = tuple(sorted(
            (min(position[a], position[b]), max(position[a], position[b]))
            for a, b in parsed
        ))
        if best is None or key < best:
            best = key
    require(best is not None)
    return best


def det(matrix: tuple[tuple[int, ...], ...]) -> int:
    # Tiny exact Bareiss-free expansion (only 4x4 here).
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        ((-1) ** j) * matrix[0][j] * det(tuple(
            tuple(row[k] for k in range(len(matrix)) if k != j)
            for row in matrix[1:]
        ))
        for j in range(len(matrix))
    )


def add_poly(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, 0) + coefficient
        if not out[monomial]:
            del out[monomial]
    return out


def mul_poly(left, right):
    out = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(sorted(lm + rm))
            out[monomial] = out.get(monomial, 0) + lc * rc
    return {m: c for m, c in out.items() if c}


def const_poly(value):
    return {(): value} if value else {}


def var_poly(name):
    return {(name,): 1}


def orbit1_entry(edge: str, row: int, column: int):
    if edge in FIXED:
        return const_poly(int(row == column))
    if edge in ("35", "46", "47") and row == column == 0:
        return const_poly(1)
    if edge == "07" and column == 0:
        answer = const_poly(int(row == 0))
        answer = add_poly(answer, {(f"a07_{row}1", "x1"): -1})
        answer = add_poly(answer, {(f"a07_{row}2", "x2"): -1})
        return answer
    return var_poly(f"a{edge}_{row}{column}")


def orbit1_amplitude_polynomials():
    polynomials = []
    for word in itertools.product(range(3), repeat=8):
        equation = {}
        for matching in ORBIT1_MATCHINGS:
            term = const_poly(1)
            for edge in matching.split("|"):
                term = mul_poly(term, orbit1_entry(edge, word[int(edge[0])], word[int(edge[1])]))
                if not term:
                    break
            equation = add_poly(equation, term)
        equation = add_poly(equation, const_poly(-int(len(set(word)) == 1)))
        polynomials.append(equation)
    for edge in ("01", "15", "17", "23", "26"):
        polynomials.append({(f"inv{edge}", f"a{edge}_00"): 1, (): -1})
    return polynomials


def polynomial_string(poly) -> str:
    if not poly:
        return "0"
    pieces = []
    for monomial in sorted(poly, key=lambda m: (len(m), m)):
        coefficient = poly[monomial]
        body = "*".join(monomial) if monomial else "1"
        if not pieces:
            if coefficient == -1:
                pieces.append(f"-{body}")
            elif coefficient == 1:
                pieces.append(body)
            else:
                pieces.append(f"{coefficient}*{body}")
        elif coefficient < 0:
            magnitude = -coefficient
            pieces.append(f"-{body}" if magnitude == 1 else f"-{magnitude}*{body}")
        else:
            pieces.append(f"+{body}" if coefficient == 1 else f"+{coefficient}*{body}")
    return "".join(pieces)


def source_text(characteristic: int, polynomials, variables) -> str:
    lines = [
        "// GENERATED DESIGN-ONLY SOURCE; DO NOT CLAIM COVERAGE WITHOUT A TERMINAL UNIT TRANSCRIPT.",
        f"ring r={characteristic},({','.join(variables)}),dp;",
        "option(redSB);",
        "ideal I =",
    ]
    for index, polynomial in enumerate(polynomials):
        suffix = "," if index + 1 < len(polynomials) else ";"
        lines.append(f"  {polynomial_string(polynomial)}{suffix}")
    lines.extend([
        "ideal G=slimgb(I);",
        'print("STATUS_BEGIN");',
        'print("INPUT_GENERATORS="+string(size(I)));',
        'print("BASIS_SIZE="+string(size(G)));',
        "poly unit_remainder=reduce(1,G);",
        'print("REDUCE_ONE="+string(unit_remainder));',
        'if (unit_remainder==0) { print("STATUS=UNIT_IDEAL"); }',
        'else { print("STATUS=NONUNIT_OR_INCOMPLETE"); }',
        'print("STATUS_END");',
        "quit;",
        "",
    ])
    return "\n".join(lines)


def make_result():
    for name, (path, expected) in PINS.items():
        require(path.is_file(), (name, "missing", str(path)))
        observed = sha(path)
        require(observed == expected, (name, observed, expected))

    parent = json.loads((PARENT / "results_eight_block_interface.json").read_text())
    require(parent["enumeration"]["unresolved_strata"] == 616)
    require(parent["scope"]["eight_block_layer_closed"] is False)
    require(parent["first_unproved_induction_interface"]["smallest_new_rank_key"] == [8, 1, 66])

    records = parent["unresolved_records"]
    essential_histogram = Counter()
    matching_histogram = Counter()
    raw_histogram = Counter()
    signature_census = Counter()
    details = []
    key_to_index = {}
    graph_members = {}
    for index, record in enumerate(records):
        edges = essential_edges(record)
        degree = Counter(v for edge in edges for v in edge_tuple(edge))
        raw = tuple(sorted(FIXED | set(record["added"]) | set(record["nonzero_variable_blocks"])))
        require(set(edges) <= set(raw), (index, "essential outside raw"))
        require(4 in degree.values(), (index, "no degree-four vertex"))
        essential_histogram[len(edges)] += 1
        matching_histogram[len(record["supported_perfect_matchings"])] += 1
        raw_histogram[len(raw)] += 1
        signature = (len(raw), len(edges), len(record["supported_perfect_matchings"]), tuple(sorted(degree.values())))
        signature_census[signature] += 1
        key = (tuple(record["added"]), tuple(record["nonzero_variable_blocks"]))
        require(key not in key_to_index)
        key_to_index[key] = index
        graph_key = canonical_unlabelled_graph(edges)
        graph_id = canonical_json_hash(graph_key)
        graph_members.setdefault(graph_id, {"canonical_edges": graph_key, "members": []})["members"].append(index)
        details.append({
            "record_index": index,
            "added": record["added"],
            "nonzero_variable_blocks": record["nonzero_variable_blocks"],
            "raw_support_edges": list(raw),
            "raw_support_count": len(raw),
            "essential_edges": list(edges),
            "essential_edge_count": len(edges),
            "degree_sequence": list(sorted(degree.values())),
            "degree_four_vertices": sorted(v for v, d in degree.items() if d == 4),
            "supported_perfect_matching_count": len(record["supported_perfect_matchings"]),
            "unlabelled_graph_id": graph_id,
        })

    require(essential_histogram == {12: 88, 13: 104, 14: 124, 15: 184, 16: 116})
    require(sum(count for size, count in essential_histogram.items() if size <= 15) == 500)
    require(len(signature_census) == 32)
    require(len(graph_members) == 51)

    exact16 = [detail for detail in details if detail["essential_edge_count"] == 16]
    require(len(exact16) == 116)
    require(all(detail["raw_support_count"] == 16 for detail in exact16))
    require(all(len(detail["nonzero_variable_blocks"]) == 4 for detail in exact16))
    exact16_graphs = {}
    for detail in exact16:
        exact16_graphs.setdefault(detail["unlabelled_graph_id"], []).append(detail["record_index"])
    require(len(exact16_graphs) == 16)
    require(Counter(map(len, exact16_graphs.values())) == {4: 5, 8: 10, 16: 1})

    # Literal source/guard symmetry, not arbitrary graph isomorphism.
    exact16_indices = {detail["record_index"] for detail in exact16}
    guard_seen = set()
    guard_orbits = []
    for detail in exact16:
        index = detail["record_index"]
        if index in guard_seen:
            continue
        record = records[index]
        mate_key = (
            tuple(sorted(permute_edge(edge) for edge in record["added"])),
            tuple(sorted(permute_edge(edge) for edge in record["nonzero_variable_blocks"])),
        )
        require(mate_key in key_to_index, (index, "guard mate missing", mate_key))
        mate = key_to_index[mate_key]
        require(mate in exact16_indices, (index, mate, "guard leaves exact16"))
        orbit = sorted({index, mate})
        require(len(orbit) == 2, (index, "unexpected fixed guard orbit"))
        guard_seen.update(orbit)
        guard_orbits.append({
            "orbit_id": len(guard_orbits),
            "record_indices": orbit,
            "unlabelled_graph_id": details[index]["unlabelled_graph_id"],
        })
    require(guard_seen == exact16_indices)
    require(len(guard_orbits) == 58)
    require(all(details[o["record_indices"][0]]["unlabelled_graph_id"] ==
                details[o["record_indices"][1]]["unlabelled_graph_id"] for o in guard_orbits))

    # Recheck the orbit-1 torus contraction and materialize a single held
    # diagonal-failure chart.  This is only one chart, not orbit coverage.
    incidence = []
    for matching in ORBIT1_MATCHINGS:
        row = tuple(int(block in matching.split("|")) for block in ORBIT1_BLOCKS)
        incidence.append(row)
    require(all(sum(row[j] * basis[j] for j in range(9)) == 0
                for row in incidence for basis in ORBIT1_TORUS_BASIS))
    selected_rows = tuple(ORBIT1_BLOCKS.index(edge) for edge in ("07", "35", "46", "47"))
    selected_weight_matrix = tuple(
        tuple(basis[row] for basis in ORBIT1_TORUS_BASIS)
        for row in selected_rows
    )
    require(abs(det(selected_weight_matrix)) == 1, selected_weight_matrix)

    polynomials = orbit1_amplitude_polynomials()
    variables = sorted({variable for polynomial in polynomials for monomial in polynomial for variable in monomial})
    require(len(polynomials) == 6566)
    require(len(variables) == 82)
    require(sum(len(poly) for poly in polynomials) == 23011)
    require(max(map(len, polynomials)) == 12)
    monic_pivots = []
    for p_index, polynomial in enumerate(polynomials):
        for variable in variables:
            if polynomial.get((variable,)) in (1, -1) and not any(
                    variable in monomial for monomial in polynomial if monomial != (variable,)):
                monic_pivots.append((p_index, variable))
    require(not monic_pivots)

    q_source = source_text(0, polynomials, variables)
    p_source = source_text(32003, polynomials, variables)
    (HERE / "orbit1_diagonal_i0_k0_all00_q.sing").write_text(q_source)
    (HERE / "orbit1_diagonal_i0_k0_all00_p32003.sing").write_text(p_source)

    plan = {
        "schema": "n8-x5-eight-block-orbit1-diagonal-held-pilot-v1",
        "status": "HELD_ZERO_RUN_NO_CLEARANCE",
        "source": "orbit1_diagonal_i0_k0_all00_p32003.sing",
        "source_sha256": sha(HERE / "orbit1_diagonal_i0_k0_all00_p32003.sing"),
        "q_source": "orbit1_diagonal_i0_k0_all00_q.sing",
        "q_source_sha256": sha(HERE / "orbit1_diagonal_i0_k0_all00_q.sing"),
        "ring_variables": 82,
        "listed_generators": 6566,
        "term_count": 23011,
        "chart": {
            "orbit": 1,
            "failure": "diagonal K00 identically zero",
            "incidence": "A07*x=e0",
            "witness_chart": "x0!=0; normalized x0=1 and substituted A07[:,0]=e0-A07[:,1]*x1-A07[:,2]*x2",
            "torus_chart": "A35[0,0],A46[0,0],A47[0,0] nonzero and normalized to 1",
            "block_nonzero_charts": "A01[0,0],A15[0,0],A17[0,0],A23[0,0],A26[0,0] nonzero via five inverses",
            "coverage": "one diagnostic chart only; no other witness/entry charts are inferred",
        },
        "proposed_resource_gate": {
            "characteristic": 32003,
            "native_wall_seconds": 240,
            "wrapper_wall_seconds": 255,
            "rss_bytes": 8589934592,
            "sequential_single_use": True,
        },
        "acceptance": "terminal UNIT_IDEAL plus exact transcript/pins would close only this chart",
        "refusal": "no clearance artifact; no runner; zero Singular process and zero arithmetic coverage",
    }
    (HERE / "held_pilot_plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")

    result = {
        "schema": "n8-x5-eight-block-essential-skeleton-contraction-design-v1",
        "status": "PASS_EXACT_CENSUS__HELD_ONE_CHART_ZERO_RUN",
        "pins": {name: {"path": str(path), "sha256": expected} for name, (path, expected) in PINS.items()},
        "essential_skeleton_census": {
            "definition": "union of raw support edges occurring in at least one supported perfect matching",
            "unresolved_records": 616,
            "all_have_degree_four_vertex": True,
            "essential_edge_histogram": {str(k): v for k, v in sorted(essential_histogram.items())},
            "at_most_15_records": 500,
            "exact_16_records": 116,
            "diagnostic_signature_classes": len(signature_census),
            "diagnostic_signature_note": "tuple(raw size, essential size, PM count, degree sequence), not graph isomorphism",
            "unlabelled_graph_classes_all": len(graph_members),
            "unlabelled_graph_classes_exact16": len(exact16_graphs),
            "exact16_graph_class_size_census": {str(k): v for k, v in sorted(Counter(map(len, exact16_graphs.values())).items())},
            "exact16_literal_guard_orbits": len(guard_orbits),
            "exact16_guard_orbit_size": 2,
            "exact16_supported_matching_histogram": {
                str(k): v for k, v in sorted(Counter(
                    details[index]["supported_perfect_matching_count"]
                    for index in exact16_indices
                ).items())
            },
            "records_sha256": canonical_json_hash(details),
            "exact16_guard_orbits_sha256": canonical_json_hash(guard_orbits),
        },
        "degree_four_interfaces": {
            "fresh_at_most15": {
                "eligible_current_records": 500,
                "proof_status": "ACTIVE_UNPROMOTED_PRELAUNCH_ONLY",
                "accepted_coverage_now": 0,
                "conditional_coverage_after_current_cnf_drat_replay": 500,
                "current_cnf": {
                    "variables": 428223,
                    "clauses": 3083125,
                    "bytes": 231408707,
                    "sha256": "f18ad14a17d31819dec64d40d6e3754f3ff93424fbefe6ad63379a73d321c7b2",
                },
                "legacy_cnf_and_proof": "REJECTED_BY_PINNED_PREFLIGHT; not imported",
            },
            "historical_exact16": {
                "eligible_current_records": 116,
                "logical_increment_if_freshly_replayed": 116,
                "status_here": "IDENTIFIED_HYPOTHESIS_ONLY__NOT_IMPORTED_OR_REPLAYED",
            },
            "historical_exact17": {
                "eligible_current_records": 0,
                "logical_increment_on_this_616_record_ledger": 0,
                "status_here": "IDENTIFIED_HYPOTHESIS_ONLY__NOT_IMPORTED_OR_REPLAYED",
            },
            "unconditional_closed_by_external_interfaces_now": 0,
        },
        "exact16_graph_classes": [
            {
                "graph_id": graph_id,
                "canonical_edges": [list(edge) for edge in graph_members[graph_id]["canonical_edges"]],
                "record_indices": sorted(indices),
            }
            for graph_id, indices in sorted(exact16_graphs.items())
        ],
        "exact16_guard_orbits": guard_orbits,
        "all_record_details": details,
        "smallest_contracted_held_chart": {
            "orbit": 1,
            "branch": "diagonal incidence i=k=0, all selected entry charts 00",
            "full_source_equations": "all 8 matching tensors equal normalized GHZ, including corrected 4-pair equality base",
            "fixed_base_words": 81,
            "fixed_base_pure_words": 3,
            "fixed_base_mixed_words": 78,
            "torus_rank": 4,
            "torus_selected_blocks": ["07", "35", "46", "47"],
            "torus_selected_weight_matrix": selected_weight_matrix,
            "torus_selected_minor_determinant": det(selected_weight_matrix),
            "pre_substitution_variables": 171,
            "contracted_variables": 82,
            "listed_generators": 6566,
            "expanded_polynomial_terms": 23011,
            "largest_generator_terms": 12,
            "further_constant_coefficient_monic_pivots": 0,
            "q_source_sha256": plan["q_source_sha256"],
            "p32003_source_sha256": plan["source_sha256"],
            "solve_status": "ZERO_RUN_HELD",
            "scope": "one exact diagnostic chart; not the other chart or orbit strata",
        },
        "scope": {
            "legacy_theorem_imported": False,
            "fresh_drat_result_imported": False,
            "singular_runs": 0,
            "heavy_solver_runs": 0,
            "deletion_monotonicity_claim": False,
            "eight_block_layer_closed": False,
            "full_conjecture_claim": False,
        },
    }
    return result


if __name__ == "__main__":
    output = make_result()
    (HERE / "results_essential_skeleton_contraction_design.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "status": output["status"],
        "at_most15": output["essential_skeleton_census"]["at_most_15_records"],
        "exact16": output["essential_skeleton_census"]["exact_16_records"],
        "exact16_graph_classes": output["essential_skeleton_census"]["unlabelled_graph_classes_exact16"],
        "exact16_guard_orbits": output["essential_skeleton_census"]["exact16_literal_guard_orbits"],
        "held_chart": output["smallest_contracted_held_chart"],
    }, indent=2, sort_keys=True))
