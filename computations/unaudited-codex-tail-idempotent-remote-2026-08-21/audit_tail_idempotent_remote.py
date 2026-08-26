#!/usr/bin/env python3
"""Exact idempotent split and carrier-independence controls.

This is a finite structural audit.  It does not solve the X5 remote branch.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import pathlib
import sys


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESPONSE = ROOT / "computations/unaudited-codex-response-star-2026-08-20"
FILTERED = ROOT / "computations/unaudited-codex-tail-filtered-lift-obstruction-2026-08-21"
OUT = HERE / "results_tail_idempotent_remote.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def logical_sha(payload) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def cyclic_f(point):
    x, y, z = point
    return x - y * z, y - x * z, z - x * y


def first_augmented_minor(row_labels, rows, ell):
    for row_index, row in enumerate(rows):
        for left, right in itertools.combinations(range(9), 2):
            value = row[left] * ell[right] - row[right] * ell[left]
            if value:
                return {
                    "response_row_label": row_labels[row_index],
                    "columns": [left, right],
                    "determinant": str(value),
                }
    raise RuntimeError("no nonzero augmented 2x2 minor")


def main() -> None:
    audit_response = load_module(
        "tail_idempotent_audit_response",
        RESPONSE / "audit_response_star.py",
    )
    core = sys.modules["response_star_core"]

    # Exact cyclic idempotent.  In A=Q[x,y,z]/(x-yz,y-xz,z-xy), the matrix
    # relation T=B*T can be chosen with
    # B=[[0,z,0],[z,0,0],[y,0,0]], so e=1-det(I-B)=z^2.
    for point in itertools.product(range(-2, 3), repeat=3):
        x, y, z = point
        f1, f2, f3 = cyclic_f(point)
        e = z * z
        require(x * (1 - e) == f1 + z * f2,
                "cyclic idempotent failed on x")
        require(y * (1 - e) == f2 + z * f1,
                "cyclic idempotent failed on y")
        z_cubic = (z * z - 1) * f3 - y * f1 - z * y * f2
        require(z * z * z - z == z_cubic,
                "cyclic z cubic identity failed")
        require(e * e - e == z * z_cubic,
                "cyclic idempotence identity failed")

    cyclic_points = [
        (0, 0, 0), (1, 1, 1), (-1, -1, 1),
        (1, -1, -1), (-1, 1, -1),
    ]
    require([point for point in cyclic_points if point[2] ** 2 == 0] ==
            [(0, 0, 0)], "cyclic zero-tail factor changed")
    require(all(point[2] ** 2 == 1 for point in cyclic_points[1:]),
            "cyclic remote factor changed")

    # W40: exact active-cap positive control, but it is outside X5 and the
    # fixed D611 chart.  This guards against treating the tail determinant as
    # necessary for cap activity.
    w40, _ = audit_response.load_sources()
    word2 = (2,) * 8
    w40_cofactors = {}
    for a in range(6):
        for tail in (6, 7):
            vertices = tuple(v for v in range(8) if v not in (a, tail))
            w40_cofactors[f"h2_{a}{tail}"] = core.hafnian(
                w40, word2, vertices
            )
    require(sum(value != 0 for value in w40_cofactors.values()) == 2,
            "W40 fixed-tail cofactor signature changed")
    w40_labels, w40_L = core.response_star_matrix(w40, 6, 7, 5)
    require(len(core.rref(w40_L)[1]) == 1, "W40 active carrier rank changed")
    w40_activity = core.activity_rows(w40, 6, 7)
    w40_augmented = [
        first_augmented_minor(w40_labels, w40_L, ell)
        for ell in w40_activity
    ]
    require([entry["determinant"] for entry in w40_augmented] ==
            ["1", "1", "-1", "1"], "W40 activity minors changed")
    w40_failure = core.hafnian(w40, tuple(map(int, "20002111")))
    require(w40_failure == -1, "W40 selected 332 failure changed")

    # A deterministic dense original-coordinate source: all twelve D611
    # cofactors are nonzero, yet every star and triangle L has full rank 9,
    # so every activity functional is in its row space.  This is not an X5
    # source (all entries are positive); it disproves a determinant-only
    # implication before source equations are imposed.
    edges = list(itertools.combinations(range(8), 2))
    dense = {
        edge: [
            [Fraction(1 + ((index + i + 2 * j + i * j) % 13))
             for j in range(3)]
            for i in range(3)
        ]
        for index, edge in enumerate(edges)
    }
    dense_cofactors = []
    for a in range(6):
        for tail in (6, 7):
            vertices = tuple(v for v in range(8) if v not in (a, tail))
            dense_cofactors.append(core.hafnian(dense, word2, vertices))
    require(all(value != 0 for value in dense_cofactors),
            "dense determinant-only control left D611")

    star_ranks = Counter()
    triangle_ranks = Counter()
    for p, q in edges:
        residual = [v for v in range(8) if v not in (p, q)]
        for centre in residual:
            _, rows = core.response_star_matrix(dense, p, q, centre)
            star_ranks[len(core.rref(rows)[1])] += 1
        for triangle in itertools.combinations(residual, 3):
            _, rows = core.response_triangle_matrix(dense, p, q, triangle)
            triangle_ranks[len(core.rref(rows)[1])] += 1
    require(star_ranks == Counter({9: 168}),
            "dense star full-rank control changed")
    require(triangle_ranks == Counter({9: 560}),
            "dense triangle full-rank control changed")

    # Exact classification of the nontrivial diagonal rows.
    diagonal_profiles = Counter()
    for word in itertools.product(range(3), repeat=8):
        counts = tuple(word.count(c) for c in range(3))
        if max(counts) < 8 and all(count % 2 == 0 for count in counts):
            diagonal_profiles[tuple(sorted(counts, reverse=True))] += 1
    require(diagonal_profiles == Counter({(4, 2, 2): 1260,
                                          (4, 4, 0): 210,
                                          (6, 2, 0): 168}),
            "diagonal profile routing census changed")

    upstream = [
        RESPONSE / "results_response_star.json",
        FILTERED / "results_tail_filtered_lift_obstruction.json",
    ]
    payload = {
        "status": "PASS exact idempotent split and carrier-independence audit",
        "idempotent_splitting_theorem": {
            "hypothesis": (
                "In A=R/I let J=(T_1,...,T_n) be finitely generated and "
                "suppose J=J^2. Choose B with entries in J and T=B*T."
            ),
            "construction": (
                "d=det(I-B) annihilates J and d=1 mod J; "
                "e=1-d lies in J, e^2=e, and J=eA."
            ),
            "split": "A = A/(e) x A/(1-e)",
            "zero_tail_factor": "A/(e), where J=0",
            "remote_factor": "A/(1-e), where e=1 and J=A",
            "scope_guard": (
                "The current 380x12 theorem does not itself prove J=J^2 "
                "for all 168 tail generators; the construction applies once "
                "the full triangular hypothesis is supplied."
            ),
        },
        "cyclic_explicit_split": {
            "ring": "Q[x,y,z]/(x-yz,y-xz,z-xy)",
            "relation_matrix": [["0", "z", "0"],
                                ["z", "0", "0"],
                                ["y", "0", "0"]],
            "idempotent": "e=z^2=1-det(I-B)",
            "zero_tail_points": [[0, 0, 0]],
            "remote_points": [list(point) for point in cyclic_points[1:]],
            "blocked_cap_extension": (
                "Adjoining an independent cap module with L=I_9 puts all "
                "four activity forms in rowspan(L) on e=1. Thus the "
                "idempotent theorem alone cannot force a carrier cap."
            ),
        },
        "W40_positive_control": {
            "scope": "X4 but not X5; positive cap control only",
            "fixed_tail_D611": "zero (10 of 12 factors vanish)",
            "cofactor_values": {key: str(value)
                                for key, value in w40_cofactors.items()},
            "selected_required_332_row": "F_20002111=-1",
            "active_carrier": "star pair 67, centre 5",
            "carrier_rank": 1,
            "four_augmented_2x2_minors": w40_augmented,
            "verdict": "cap activity does not require the generic tail determinant",
        },
        "dense_source_coordinate_control": {
            "definition": (
                "For lexicographic edge index k, "
                "A_edge[i,j]=1+((k+i+2*j+i*j) mod 13)."
            ),
            "D611_cofactors": [str(value) for value in dense_cofactors],
            "star_rank_histogram": {str(k): v for k, v in sorted(star_ranks.items())},
            "triangle_rank_histogram": {
                str(k): v for k, v in sorted(triangle_ranks.items())
            },
            "X5_status": "fails every mixed target because all 252 cells are positive",
            "verdict": (
                "D611 nonzero does not force any carrier activity before "
                "the X5 equations are used: rank(L)=9 makes all blockers."
            ),
        },
        "remote_blocker_pullback": {
            "ring": "A_remote=A/(1-e)",
            "carrier_data": (
                "Reduce each 90x9 or 108x9 L_C and the four ell_i modulo "
                "1-e. Activity still means ell_i not in rowspan(L_C) for "
                "all four i; e=1 supplies no such augmented minor."
            ),
            "determinant_independence": (
                "The tail-source maximal minors are Fitting minors of a "
                "380x12 coefficient module. Carrier blockers are augmented "
                "minors of unrelated 90x9/108x9 cap-response matrices. No "
                "source identity connecting these Fitting ideals is frozen."
            ),
        },
        "finite_exact_remote_target": {
            "idempotent_form": (
                "For every rank-stratified blocker branch beta, prove "
                "1 in (I_X5 + I_rank(beta) + I_membership(beta) + <1-e>) "
                "localized at the tail rescue factors and chosen nonzero "
                "rank minors of all L_C."
            ),
            "pointwise_Rabinowitsch_form": (
                "Equivalently introduce lambda_1,...,lambda_168 and add "
                "1-sum(lambda_j*T_j)=0 to isolate the nonzero-tail locus, "
                "then exclude it together with X5 and the no-cap branches."
            ),
            "rank_branch_definition": (
                "For carrier C of declared rank r, invert one r-minor of "
                "L_C, kill all (r+1)-minors of L_C, choose one blocker i_C, "
                "and kill all (r+1)-minors of [L_C;ell_i_C]."
            ),
        },
        "diagonal_1638_routing": {
            "6+2+0": {
                "count": 168,
                "formula": "Haf(G_c[V\\{a,b}])*g^d_ab",
                "existing_interface": "directional entry/cofactor clauses",
                "coverage": "proper chart/mate closures only",
            },
            "4+4+0": {
                "count": 210,
                "formula": "Haf(G_c[S])*Haf(G_d[S^c])",
                "existing_interface": "polarized complementary-Q/Q mate rows",
                "coverage": "twisted-44 and other proper support charts only",
            },
            "4+2+2": {
                "count": 1260,
                "formula": "Haf(G_c[S])*g^d_ab*g^e_cd",
                "existing_interface": "trichromatic Q/edge/edge diagonal rows",
                "coverage": "no global three-colour chart closure",
            },
            "global_status": (
                "The types match existing local chart interfaces, but the "
                "repository has no exhaustive containment of their common "
                "diagonal scheme in the carrier activity open."
            ),
        },
        "mutation_guards": {
            "replace_e_z2_by_z": True,
            "declare_W40_in_D611_open": True,
            "drop_dense_triangle_rank_control": True,
            "identify_tail_and_carrier_Fitting_minors": True,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path) for path in upstream
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
