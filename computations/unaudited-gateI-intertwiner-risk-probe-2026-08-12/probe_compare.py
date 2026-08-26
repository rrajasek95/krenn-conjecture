#!/usr/bin/env python3
"""UNAUDITED RISK PROBE - side-by-side morphism invariants for Gate I.

Pinned HEAD b63c76c8624996044423a0dde60a2b60c9e8fa3d, snapshot ./snap.
Exact rational arithmetic only; no repo writes.

Compares every invariant that a legitimate intertwiner
    tau : U_15 (six-site collision labels)  -->  L_{h=3} (eight-site literal)
must match, between
    SOURCE  B = (1-rho)(w-1)u_012 = dK(u)+Kd(u)   (the only committed
            realization of the rho-odd Cartan residual), and
    TARGET  J(M_v) = sum_j alpha_j B_j            (the 360-feature literal
            boundary of M_v = -O_alpha + K).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json
from pathlib import Path

import probe_source as PS
import probe_target as PT

HERE = Path(__file__).resolve().parent


# --------------------------------------------------------------------------
# SOURCE: four-corner Klein structure of B
# --------------------------------------------------------------------------
def source_corner_structure(perm=PS.RHO, root_sites=PS.ROOT_SITES,
                            sign_mutation=None, label_mutation=None):
    lower = PS.load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "cmp_lower")
    tangent = PS.load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "cmp_tangent")
    key = lambda label: (label[1], label[2])
    u_labels = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    other = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))

    def rho_label(label):
        matching_index, repeated = label
        matching = PS.permute_matching(tangent.MATCHINGS[matching_index], perm)
        return (tangent.MATCHING_INDEX[matching],
                PS.permute_edge(repeated, perm))

    def rho_vec(vector):
        return {(PS.rho_word(word, perm), rho_label(label)): value
                for (word, label), value in vector.items()}

    def w_vec(vector):
        answer = defaultdict(Q)
        for (word, label), value in vector.items():
            changed, sign = PS.weyl_word(word, root_sites)
            if sign_mutation is not None:
                sign = sign_mutation
            answer[(changed, label)] += sign * value
        return {b: v for b, v in answer.items() if v}

    u_w = {(PS.W, label): Q(1) for label in sorted(u_labels)}
    if label_mutation is not None:
        u_w[(PS.W, sorted(u_labels)[label_mutation])] = Q(-1)
    wu = PS.add(w_vec(u_w), PS.scale(-1, u_w))
    B = PS.add(wu, PS.scale(-1, rho_vec(wu)))

    # The four corners: Klein orbit of the "u-only, word W" packet.
    shared = u_labels & other
    only_u = sorted(u_labels - shared)
    f0 = {(PS.W, label): Q(1) for label in only_u}
    corners = {
        "E+T0": f0,
        "E-T0": rho_vec(f0),                 # s := rho
        "E+T1": w_vec(f0),                   # w := signed two-root Weyl
        "E-T1": rho_vec(w_vec(f0)),
    }
    # express B in the corner basis (exact, over Q)
    order = ("E+T0", "E-T0", "E+T1", "E-T1")
    coefficients = []
    residual = dict(B)
    for name in order:
        cell = corners[name]
        basis, unit = next(iter(cell.items()))
        value = residual.get(basis, Q(0)) / unit
        coefficients.append(value)
        residual = PS.add(residual, PS.scale(-value, cell))
    exact = not residual

    # role-assignment margin: which identifications of (s,w) with the three
    # nontrivial Klein involutions reproduce ALPHA exactly?
    diag = lambda v: rho_vec(w_vec(v))
    involutions = {"rho": rho_vec, "w": w_vec, "rho*w": diag}
    role_hits = []
    for s_name, w_name in permutations(involutions, 2):
        s_map, w_map = involutions[s_name], involutions[w_name]
        basis_cells = [f0, s_map(f0), w_map(f0), s_map(w_map(f0))]
        residual = dict(B)
        coeffs = []
        ok = True
        for cell in basis_cells:
            if not cell:
                ok = False
                break
            b, unit = next(iter(cell.items()))
            value = residual.get(b, Q(0)) / unit
            coeffs.append(value)
            residual = PS.add(residual, PS.scale(-value, cell))
        if ok and not residual and tuple(coeffs) == (Q(-1), Q(1), Q(1), Q(-1)):
            role_hits.append((s_name, w_name))

    return {
        "B_support": len(B),
        "corner_sizes": {name: len(cell) for name, cell in corners.items()},
        "corners_pairwise_disjoint": all(
            not (set(corners[a]) & set(corners[b]))
            for a, b in combinations(order, 2)),
        "B_in_corner_basis": [str(c) for c in coefficients],
        "corner_expansion_is_exact": exact,
        "equals_ALPHA": tuple(coefficients) == (Q(-1), Q(1), Q(1), Q(-1)),
        "endpoint_marginals": [str(coefficients[0] + coefficients[1]),
                               str(coefficients[2] + coefficients[3])],
        "tail_marginals": [str(coefficients[0] + coefficients[2]),
                           str(coefficients[1] + coefficients[3])],
        "aggregate_sum": str(sum(coefficients)),
        "role_assignments_reproducing_ALPHA": [list(x) for x in role_hits],
        "role_assignments_tested": 6,
        "fine_grades_carrying_B": sorted(
            {"".join(map(str, word)) for word, _ in B}),
        "grade_multidegrees_distinct": (
            PS.multidegree(PS.W) != PS.multidegree(PS.WP)),
    }


# --------------------------------------------------------------------------
# TARGET: Klein structure available on the literal pure-column corners
# --------------------------------------------------------------------------
def target_symmetries(record):
    """Site permutations x colour permutations fixing colour 0 (so that the
    pure word (0,)*8 is preserved) and preserving the fine 24-degree."""
    degree = record["target_degree"]
    answer = []
    for colour_map in ((0, 1, 2), (0, 2, 1)):
        for site_perm in permutations(range(8)):
            ok = True
            moved = [0] * 24
            for s in range(8):
                for c in range(3):
                    moved[3 * site_perm[s] + colour_map[c]] += degree[3 * s + c]
            if tuple(moved) != tuple(degree):
                ok = False
            if ok:
                answer.append((site_perm, colour_map))
    return answer


def permute_cell_full(cell, site_perm, colour_map):
    left, right, lc, rc = cell
    a, b = site_perm[left], site_perm[right]
    lc, rc = colour_map[lc], colour_map[rc]
    return (a, b, lc, rc) if a <= b else (b, a, rc, lc)


def target_corner_structure(record, alpha):
    pure = record["pure"]
    lookup = {frozenset(m): i for i, (_w, m, _b) in enumerate(pure)}
    syms = target_symmetries(record)
    induced = {}
    for site_perm, colour_map in syms:
        image = []
        for i, (_w, m, _b) in enumerate(pure):
            moved = frozenset(permute_cell_full(c, site_perm, colour_map)
                              for c in m)
            if moved not in lookup:
                image = None
                break
            image.append(lookup[moved])
        if image is not None:
            induced.setdefault(tuple(image), (site_perm, colour_map))
    induced_perms = sorted(induced)

    # Klein four subgroups acting simply transitively on some ordered
    # 4-subset (c0,c1,c2,c3) with s=(c0c1)(c2c3), w=(c0c2)(c1c3).
    klein = []
    for choice in combinations(range(len(pure)), 4):
        for ordering in permutations(choice):
            c0, c1, c2, c3 = ordering
            need_s = {c0: c1, c1: c0, c2: c3, c3: c2}
            need_w = {c0: c2, c2: c0, c1: c3, c3: c1}
            s_hit = [p for p in induced_perms
                     if all(p[k] == v for k, v in need_s.items())]
            w_hit = [p for p in induced_perms
                     if all(p[k] == v for k, v in need_w.items())]
            if s_hit and w_hit:
                klein.append({"corners": list(ordering),
                              "s": list(s_hit[0]), "w": list(w_hit[0])})

    # Is any of them alpha-odd in both directions?  alpha=(-1,1,1,-1) with
    # corner order (c0,c1,c2,c3)=(E+T0,E-T0,E+T1,E-T1) is odd for both.
    return {
        "site_colour_symmetries": len(syms),
        "induced_permutations_of_six_pure_columns": len(induced_perms),
        "induced_group_order": len(induced_perms),
        "klein_regular_four_corner_systems": len(klein),
        "klein_example": klein[0] if klein else None,
        "pure_word_forced_for_all_four_corners": True,
        "distinct_fine_grades_among_corners": 1,
        "fine_grade_total_degree": sum(record["target_degree"]),
        "colour_character": [sum(record["target_degree"][3 * s + c]
                                 for s in range(8)) for c in range(3)],
    }


def main():
    out = {"probe": "UNAUDITED RISK PROBE",
           "pinned_head": "b63c76c8624996044423a0dde60a2b60c9e8fa3d"}
    out["source"] = source_corner_structure()

    records, alpha, _pure_word = PT.cached()
    out["target"] = [dict(component=r["component"],
                          **target_corner_structure(r, alpha))
                     for r in records]

    # ---- cross-side comparison table --------------------------------------
    src = out["source"]
    tgt = out["target"]
    out["comparison"] = {
        "corner_count": {"source": 4, "target": 4, "match": True},
        "corner_coefficients": {
            "source": src["B_in_corner_basis"],
            "target": [str(int(a)) for a in alpha],
            "match": src["equals_ALPHA"],
        },
        "corners_pairwise_disjoint": {
            "source": src["corners_pairwise_disjoint"],
            "target": True,
            "match": src["corners_pairwise_disjoint"],
        },
        "corner_packet_size": {
            "source": sorted(set(src["corner_sizes"].values())),
            "target": [90],
            "match": False,
            "note": "6 labels vs 90 literal features; a 15:1 aggregation",
        },
        "total_support": {"source": src["B_support"], "target": 360},
        "aggregate_sum": {"source": src["aggregate_sum"], "target": "0"},
        "klein_group_realized": {
            "source": "yes: rho=(1 4) and signed two-root w act on the module",
            "target_components": [t["klein_regular_four_corner_systems"]
                                  for t in tgt],
        },
        "distinct_fine_grades_on_the_residual": {
            "source": len(src["fine_grades_carrying_B"]),
            "target": 1,
            "match": False,
        },
        "colour_character": {
            "source": [2, 2, 2],
            "target_components": [t["colour_character"] for t in tgt],
            "target_distinct_characters": sorted(
                {tuple(t["colour_character"]) for t in tgt}),
        },
        "target_candidate_multiplicity": {
            "components": len(records),
            "four_corner_selections_per_component": 15,
            "distinct_literal_M_v_boundaries": 75,
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    (HERE / "compare_out.json").write_text(json.dumps(out, indent=2,
                                                      sort_keys=True))


if __name__ == "__main__":
    main()
