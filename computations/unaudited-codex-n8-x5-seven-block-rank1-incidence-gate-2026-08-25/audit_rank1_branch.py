#!/usr/bin/env python3
"""Independent exact audit of the canonical rank<=1 seven-block branch."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf"
METADATA = HERE / "rank1_ideal_metadata.json"
P_RESULT = HERE / "results_rank1_incidence_p32003.json"
Q_RESULT = HERE / "results_rank1_incidence_Q.json"
Q_STD_RESULT = HERE / "results_rank1_incidence_Q_std.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def matvec(matrix, vector):
    return [sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3)]


def outer(left, right):
    return [[left[i] * right[j] for j in range(3)] for i in range(3)]


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(3)] for i in range(3)]


def negate(matrix):
    return [[-value for value in row] for row in matrix]


def dot_matrix(left, right):
    return sum(left[i][j] * right[i][j] for i in range(3) for j in range(3))


def dot_vector(left, right):
    return sum(a * b for a, b in zip(left, right))


def deterministic_matrix(seed):
    return [[((seed + 11 * i + 17 * j + 7 * i * j) % 13) - 6 for j in range(3)] for i in range(3)]


def deterministic_vector(seed):
    return [((seed + 5 * i + 3 * i * i) % 11) - 5 for i in range(3)]


def response_and_adjoint_replay():
    records = []
    for sample in range(257):
        A06 = deterministic_matrix(13 + 19 * sample)
        A17 = deterministic_matrix(29 + 23 * sample)
        A26 = deterministic_matrix(41 + 31 * sample)
        K = deterministic_matrix(59 + 37 * sample)
        u = deterministic_vector(71 + 41 * sample)
        v = deterministic_vector(83 + 43 * sample)
        if not any(u):
            u[0] = 1
        if not any(v):
            v[1] = 1
        A57 = outer(u, v)
        w = matvec(A26, v)
        A56 = negate(outer(u, w))
        assert transpose(A56) == negate(matmul(A26, transpose(A57)))

        R05 = matmul(matmul(A06, K), transpose(A57))
        R15 = add(matmul(K, transpose(A57)), matmul(matmul(A17, transpose(K)), transpose(A56)))
        R25 = add(matmul(matmul(A26, K), transpose(A57)), matmul(transpose(K), transpose(A56)))
        K_v = matvec(K, v)
        Kt_w = matvec(transpose(K), w)
        reduced05 = matvec(matmul(A06, K), v)
        reduced15 = [K_v[i] - matvec(A17, Kt_w)[i] for i in range(3)]
        reduced25 = [matvec(A26, K_v)[i] - Kt_w[i] for i in range(3)]
        assert R05 == outer(reduced05, u)
        assert R15 == outer(reduced15, u)
        assert R25 == outer(reduced25, u)

        x = deterministic_vector(97 + 47 * sample)
        y = deterministic_vector(101 + 53 * sample)
        z = deterministic_vector(107 + 59 * sample)
        g = [
            matvec(transpose(A06), x)[i] + y[i] + matvec(transpose(A26), z)[i]
            for i in range(3)
        ]
        h = [matvec(transpose(A17), y)[i] + z[i] for i in range(3)]
        adjoint = add(outer(g, v), negate(outer(w, h)))
        assert (
            dot_vector(reduced05, x) + dot_vector(reduced15, y) + dot_vector(reduced25, z)
            == dot_matrix(K, adjoint)
        )
        if sample in (0, 64, 128, 192, 256):
            records.append({
                "sample": sample,
                "A57_sha256": hashlib.sha256(json.dumps(A57).encode()).hexdigest(),
                "adjoint_pairing": dot_matrix(K, adjoint),
            })
    return records


def normalized_program(text):
    lines = text.splitlines()
    assert lines[1].startswith("ring r=")
    lines[1] = lines[1].replace("ring r=32003,", "ring r=RING,").replace("ring r=0,", "ring r=RING,")
    return "\n".join(lines)


def main():
    assert sha256(PARENT_MANIFEST) == PARENT_SHA256
    metadata = json.loads(METADATA.read_text())
    p_result = json.loads(P_RESULT.read_text())
    q_result = json.loads(Q_RESULT.read_text())
    q_std_result = json.loads(Q_STD_RESULT.read_text())
    assert metadata["counts"]["variables"] == 103
    assert metadata["counts"]["equations"] == 6582
    for label in ("p32003", "Q", "Q_std"):
        path = HERE / metadata["inputs"][label]["path"]
        assert sha256(path) == metadata["inputs"][label]["sha256"]
    p_program = (HERE / metadata["inputs"]["p32003"]["path"]).read_text()
    q_program = (HERE / metadata["inputs"]["Q"]["path"]).read_text()
    assert normalized_program(p_program) == normalized_program(q_program)

    assert p_result["status"] == "PASS_MODULAR_UNIT_DIAGNOSTIC"
    assert p_result["stdout"] == "INPUT_GENERATORS=6582\nGROEBNER_SIZE=1\nUNIT_REMAINDER=0\nSTATUS=UNIT_IDEAL\n"
    assert p_result["mathematical_coverage"] is False
    assert q_result["status"] == "PASS_RATIONAL_UNIT_IDEAL"
    assert q_result["stdout"] == p_result["stdout"]
    assert q_result["mathematical_coverage"] is True
    assert q_std_result["status"] == "INCOMPLETE_WALL_GATE"
    assert q_std_result["mathematical_coverage"] is False

    replay = response_and_adjoint_replay()
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK1_BRANCH_AUDIT_V1",
        "status": "PASS_EXACT_CANONICAL_RANK_LE1_TRIANGLE_OR_STAR_BRANCH",
        "parent_manifest_sha256": PARENT_SHA256,
        "reduction": {
            "A57": "u*v^T",
            "A56": "-u*(A26*v)^T",
            "guard": ["A06*v=0", "(I-A17*A26)*v=0"],
            "response_dual_dimension": 9,
            "source_variables_plus_witnesses": 103,
            "equations": 6582,
        },
        "exact_rational_unit": {
            "input_sha256": q_result["input_sha256"],
            "groebner_size": 1,
            "unit_remainder": 0,
            "wall_seconds": q_result["wall_seconds"],
            "peak_rss_raw_darwin_bytes": q_result["peak_rss_raw_darwin_bytes"],
        },
        "branch_logic": {
            "cap67": "guard gives I in ker; if A67 pairing is live, triangle012 is active",
            "cap45": (
                "if cap67 pairing fails, cap45/star2 is active unless a coordinate e_i lies in both P and Q "
                "or its fixed-I pairing fails; fixed-I pairing failure forces P=Q=Q^3 and hence includes e0"
            ),
            "colour_symmetry": (
                "global S3 preserves the source equations and maps any shared coordinate e_i to e0; "
                "the rational unit ideal for e0 therefore closes all three diagonal-failure branches"
            ),
            "conclusion": (
                "on the canonical support with rank(A57)<=1, formal guard plus full X5 forces an active "
                "cap67 triangle or active cap45 star"
            ),
        },
        "literal_response_adjoint_replay": {
            "samples": 257,
            "distributed_records": replay,
            "exact_integer": True,
        },
        "std_crosscheck": {
            "status": q_std_result["status"],
            "mathematical_coverage": False,
            "note": "timed out; the completed exact-Q slimgb result is the proof-producing run",
        },
        "next_branch": {
            "rank": 2,
            "parameterization": "A57=U*V^T with U,V 3x2; A56=-U*(A26*V)^T",
            "guard": ["A06*V=0", "(I-A17*A26)*V=0"],
            "response_dual_variables": 18,
            "estimated_total_variables_with_e0_incidence": 119,
            "reason": "rank<=1 is now closed, and guard already excludes rank3 because A06 is nonzero",
        },
        "scope": {
            "canonical_support": True,
            "guard_mate_by_order_two_symmetry": True,
            "rank_le_one": True,
            "rank_two": False,
            "other_five_full_family_orbits": False,
            "all_64_loci": False,
            "D12_read": False,
        },
    }
    output = HERE / "results_rank1_branch_audit.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"],
        "variables": 103,
        "equations": 6582,
        "replay": 257,
        "next_rank": 2,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
