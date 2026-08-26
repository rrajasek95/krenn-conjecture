#!/usr/bin/env python3
"""Independent exact audit of the canonical rank-two seven-block branch."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GUARD_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/MANIFEST.sha256"
RANK1_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25/MANIFEST.sha256"
PINS = {
    GUARD_MANIFEST: "21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf",
    RANK1_MANIFEST: "45ab914ff35c446f67fcc2ec86a6d4201c8ddf3e0afed0b9420e269ad610daa9",
}
METADATA = HERE / "rank2_ideal_metadata.json"
CHARTS = (
    "all_equal",
    "incidence_eq_u",
    "incidence_eq_v",
    "minor_equal_not_incidence",
    "all_distinct",
)
EXPECTED_STDOUT = "INPUT_GENERATORS=6589\nGROEBNER_SIZE=1\nUNIT_REMAINDER=0\nSTATUS=UNIT_IDEAL\n"

FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
REPS = (
    frozenset(((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7))),
    frozenset(((0, 6), (1, 3), (1, 7), (2, 5), (2, 6), (4, 6), (4, 7))),
    frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7))),
    frozenset(((0, 6), (1, 4), (1, 7), (2, 5), (2, 6), (3, 6), (3, 7))),
    frozenset(((0, 6), (1, 5), (1, 7), (2, 3), (2, 6), (4, 6), (4, 7))),
    frozenset(((0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 6), (3, 7))),
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    width = len(right[0])
    inner = len(right)
    assert len(left[0]) == inner
    return [[sum(left[i][k] * right[k][j] for k in range(inner)) for j in range(width)] for i in range(len(left))]


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def subtract(left, right):
    return [[left[i][j] - right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def negate(matrix):
    return [[-value for value in row] for row in matrix]


def dot_matrix(left, right):
    return sum(left[i][j] * right[i][j] for i in range(len(left)) for j in range(len(left[0])))


def deterministic_matrix(seed, rows=3, columns=3):
    return [[((seed + 11 * i + 17 * j + 7 * i * j) % 13) - 6 for j in range(columns)] for i in range(rows)]


def full_rank_factor(seed):
    # The top 2x2 minor is one, so this is an exact rank-two factor.
    return [[1, 0], [0, 1], [((seed + 3) % 11) - 5, ((2 * seed + 7) % 13) - 6]]


def response_and_adjoint_replay():
    distributed = []
    for sample in range(257):
        A06 = deterministic_matrix(13 + 19 * sample)
        A17 = deterministic_matrix(29 + 23 * sample)
        A26 = deterministic_matrix(41 + 31 * sample)
        K = deterministic_matrix(59 + 37 * sample)
        U = full_rank_factor(71 + 41 * sample)
        V = full_rank_factor(83 + 43 * sample)
        A57 = matmul(U, transpose(V))
        W = matmul(A26, V)
        A56 = negate(matmul(U, transpose(W)))
        assert transpose(A56) == negate(matmul(A26, transpose(A57)))

        R05 = matmul(matmul(A06, K), transpose(A57))
        R15 = add(matmul(K, transpose(A57)), matmul(matmul(A17, transpose(K)), transpose(A56)))
        R25 = add(matmul(matmul(A26, K), transpose(A57)), matmul(transpose(K), transpose(A56)))
        reduced05 = matmul(matmul(A06, K), V)
        reduced15 = subtract(matmul(K, V), matmul(matmul(A17, transpose(K)), W))
        reduced25 = subtract(matmul(matmul(A26, K), V), matmul(transpose(K), W))
        assert R05 == matmul(reduced05, transpose(U))
        assert R15 == matmul(reduced15, transpose(U))
        assert R25 == matmul(reduced25, transpose(U))

        x = deterministic_matrix(97 + 47 * sample, 3, 2)
        y = deterministic_matrix(101 + 53 * sample, 3, 2)
        z = deterministic_matrix(107 + 59 * sample, 3, 2)
        G = add(add(matmul(transpose(A06), x), y), matmul(transpose(A26), z))
        H = add(matmul(transpose(A17), y), z)
        adjoint = subtract(matmul(G, transpose(V)), matmul(W, transpose(H)))
        lhs = dot_matrix(reduced05, x) + dot_matrix(reduced15, y) + dot_matrix(reduced25, z)
        assert lhs == dot_matrix(K, adjoint)
        if sample in (0, 64, 128, 192, 256):
            distributed.append({
                "sample": sample,
                "A57_sha256": hashlib.sha256(json.dumps(A57, separators=(",", ":")).encode()).hexdigest(),
                "adjoint_pairing": dot_matrix(K, adjoint),
            })
    return distributed


def normalized_program(text):
    lines = text.splitlines()
    assert lines[1].startswith("ring r=")
    lines[1] = lines[1].replace("ring r=32003,", "ring r=RING,").replace("ring r=0,", "ring r=RING,")
    return "\n".join(lines)


def equality_type(triple):
    i, r, s = triple
    if i == r == s:
        return "i=r=s"
    if i == r:
        return "i=r!=s"
    if i == s:
        return "i=s!=r"
    if r == s:
        return "r=s!=i"
    return "all distinct"


def chart_orbit_replay(metadata):
    triples = tuple(itertools.product(range(3), repeat=3))
    types = {name: [] for name in metadata["chart_orbit_proof"]["S3_orbits"]}
    for triple in triples:
        types[equality_type(triple)].append(triple)
    assert {name: len(items) for name, items in types.items()} == {
        "i=r=s": 3,
        "i=r!=s": 6,
        "i=s!=r": 6,
        "r=s!=i": 6,
        "all distinct": 6,
    }
    expected = {
        "all_equal": (0, 0, 0),
        "incidence_eq_u": (0, 0, 1),
        "incidence_eq_v": (0, 1, 0),
        "minor_equal_not_incidence": (0, 1, 1),
        "all_distinct": (0, 1, 2),
    }
    for chart in metadata["chart_orbit_proof"]["charts"]:
        omitted_u = ({0, 1, 2} - set(chart["u_rows"])).pop()
        omitted_v = ({0, 1, 2} - set(chart["v_rows"])).pop()
        assert (0, omitted_u, omitted_v) == expected[chart["id"]]
    return {name: len(items) for name, items in types.items()}


def image(edges, permutation):
    return frozenset(tuple(sorted((permutation[a], permutation[b]))) for a, b in edges)


def transport_replay():
    counts = []
    witnesses = []
    for target in REPS:
        matches = []
        for permutation in itertools.permutations(range(8)):
            if image(FIXED, permutation) != FIXED:
                continue
            if image(VARIABLE, permutation) != VARIABLE:
                continue
            if image(REPS[0], permutation) == target:
                matches.append(permutation)
        counts.append(len(matches))
        witnesses.append(list(matches[0]) if matches else None)
    assert counts == [1, 0, 0, 0, 0, 0]
    assert witnesses[0] == list(range(8))
    guard_mate = (0, 2, 1, 3, 4, 5, 7, 6)
    assert image(FIXED, guard_mate) == FIXED
    assert image(VARIABLE, guard_mate) == VARIABLE
    mate_added = image(REPS[0], guard_mate)
    assert mate_added not in REPS
    return {
        "permutation_search_space": 40320,
        "required_preservation": ["fixed identity edge set", "variable block family", "added support"],
        "canonical_to_representative_transport_counts": counts,
        "canonical_transport_witness": witnesses[0],
        "other_five_direct_transports": 0,
        "guard_mate_added": ["".join(map(str, edge)) for edge in sorted(mate_added)],
        "conclusion": (
            "No source/site permutation preserving the fixed and variable families carries the canonical proof "
            "to any of representatives 1..5; their ideals remain separate obligations."
        ),
    }


def main():
    for path, digest in PINS.items():
        assert sha256(path) == digest
    metadata = json.loads(METADATA.read_text())
    assert metadata["counts_per_chart"]["variables"] == 120
    assert metadata["counts_per_chart"]["equations"] == 6589
    assert metadata["counts_per_chart"]["reduced_response_dual_variables"] == 18
    assert metadata["substitutions"]["A56"] == "-U*(A26*V)^T"
    assert metadata["guard_after_substitution"] == ["A06*V=0", "(I-A17*A26)*V=0"]

    runs = {}
    for chart in CHARTS:
        runs[chart] = {}
        programs = {}
        for ring in ("p32003", "Q"):
            input_record = metadata["inputs"][chart][ring]
            source = HERE / input_record["path"]
            assert sha256(source) == input_record["sha256"]
            programs[ring] = source.read_text()
            result_path = HERE / f"results_rank2_{chart}_{ring}.json"
            result = json.loads(result_path.read_text())
            assert result["input_sha256"] == input_record["sha256"]
            assert result["returncode"] == 0 and result["timed_out"] is False
            assert result["unit_ideal"] is True and result["stdout"] == EXPECTED_STDOUT
            if ring == "Q":
                assert result["status"] == "PASS_RATIONAL_UNIT_IDEAL"
                assert result["mathematical_coverage"] is True
            else:
                assert result["status"] == "PASS_MODULAR_UNIT_DIAGNOSTIC"
                assert result["mathematical_coverage"] is False
            runs[chart][ring] = {
                "result_sha256": sha256(result_path),
                "input_sha256": result["input_sha256"],
                "wall_seconds": result["wall_seconds"],
                "peak_rss_raw_darwin_bytes": result["peak_rss_raw_darwin_bytes"],
                "mathematical_coverage": result["mathematical_coverage"],
            }
        assert normalized_program(programs["p32003"]) == normalized_program(programs["Q"])

    replay = response_and_adjoint_replay()
    orbit_counts = chart_orbit_replay(metadata)
    transport = transport_replay()
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK2_BRANCH_AUDIT_V1",
        "status": "PASS_EXACT_CANONICAL_ALL_RANKS_TRIANGLE_OR_STAR_BRANCH",
        "parent_manifest_sha256": {
            "guard_dual": PINS[GUARD_MANIFEST],
            "rank_le_one": PINS[RANK1_MANIFEST],
        },
        "rank_two_reduction": {
            "A57": "U*V^T; U,V are 3x2 full-column-rank",
            "A56": "-U*(A26*V)^T",
            "guard": ["A06*V=0", "(I-A17*A26)*V=0"],
            "response_dual_dimension": 18,
            "variables_per_chart": 120,
            "equations_per_chart": 6589,
            "minor_inverse": "eta*minor_U*minor_V-1=0",
        },
        "chart_coverage": {
            "ordered_failed_colour_and_minor_pairs": 27,
            "S3_orbit_counts": orbit_counts,
            "charts": list(CHARTS),
            "rational_unit_charts": 5,
            "modular_control_charts": 5,
        },
        "runs": runs,
        "literal_response_adjoint_replay": {
            "samples": 257,
            "exact_integer": True,
            "distributed_records": replay,
        },
        "canonical_branch_logic": {
            "rank_le_one": "closed by the independently pinned exact-Q rank<=1 package",
            "rank_two": "all five full-rank minor/incidence chart orbits are exact-Q unit ideals",
            "rank_three": (
                "excluded: A06*A57^T=0 and nonzero A06 imply rank(A57)<=2 by Sylvester rank inequality"
            ),
            "conclusion": (
                "the canonical full-family support forces an active cap67/triangle012 or cap45/star2 in every rank"
            ),
        },
        "transport_test": transport,
        "scope": {
            "canonical_representative_all_ranks": True,
            "canonical_guard_mate": True,
            "other_five_full_family_representatives": False,
            "all_64_loci": False,
            "D12_read": False,
        },
        "next_exact_obligation": {
            "representatives": [1, 2, 3, 4, 5],
            "smallest_same_shape_candidate": 2,
            "reason": (
                "representative 2 retains outside site 5 and the same rank-factor guard form, but its source support "
                "is not a legal permutation transport of representative 0"
            ),
        },
    }
    output = HERE / "results_rank2_branch_audit.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"],
        "rational_unit_charts": 5,
        "replay": 257,
        "other_five_direct_transports": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
