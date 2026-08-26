#!/usr/bin/env python3
"""UNAUDITED RISK PROBE - isotypic bookkeeping + mutation controls.

Pinned HEAD b63c76c8624996044423a0dde60a2b60c9e8fa3d, snapshot ./snap.
Exact rational arithmetic only.

Part 1: Klein-isotypic decomposition of both sides and the exact
        dim Hom_V / constraint count ("how overdetermined is the match?").
Part 2: mutation controls - every invariant claim is re-run on deliberately
        corrupted data and must flip.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations
import json
from pathlib import Path

import probe_source as PS
import probe_target as PT
import probe_compare as PC

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- part 1 ---
def klein_isotypic_on_columns(component_index):
    records, alpha, _pure = PT.cached()
    record = records[component_index]
    complete = PS.load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "iso_complete")
    base = PS.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "iso_base")
    block = complete.component(base, record["target_degree"])
    labels = list(block["labels"])
    index = {label: i for i, label in enumerate(labels)}
    pure_positions = [index[(w, m)] for w, m, _b in record["pure"]]

    induced = {}
    for site_perm, colour_map in PC.target_symmetries(record):
        image, ok = [], True
        for word, multiplier in labels:
            new_word = tuple(colour_map[word[site_perm.index(s)]]
                             for s in range(8))
            new_multiplier = tuple(sorted(
                PC.permute_cell_full(cell, site_perm, colour_map)
                for cell in multiplier))
            if (new_word, new_multiplier) not in index:
                ok = False
                break
            image.append(index[(new_word, new_multiplier)])
        if ok:
            induced.setdefault(tuple(image), (site_perm, colour_map))
    induced_perms = sorted(induced)

    # find a regular Klein four-corner system among the pure columns
    system = None
    for choice in combinations(range(6), 4):
        for ordering in permutations(choice):
            c0, c1, c2, c3 = (pure_positions[i] for i in ordering)
            need_s = {c0: c1, c1: c0, c2: c3, c3: c2}
            need_w = {c0: c2, c2: c0, c1: c3, c3: c1}
            s = next((p for p in induced_perms
                      if all(p[k] == v for k, v in need_s.items())), None)
            w = next((p for p in induced_perms
                      if all(p[k] == v for k, v in need_w.items())), None)
            if s is not None and w is not None:
                system = (ordering, (c0, c1, c2, c3), s, w)
                break
        if system:
            break
    if system is None:
        return {"component": component_index,
                "regular_klein_four_corner_system": False,
                "induced_group_order": len(induced_perms)}

    ordering, corners, s, w = system
    sw = tuple(s[w[i]] for i in range(len(labels)))
    traces = {"1": len(labels),
              "s": sum(1 for i in range(len(labels)) if s[i] == i),
              "w": sum(1 for i in range(len(labels)) if w[i] == i),
              "sw": sum(1 for i in range(len(labels)) if sw[i] == i)}
    iso = {}
    for a in (1, -1):
        for b in (1, -1):
            iso[f"s{'+' if a > 0 else '-'}_w{'+' if b > 0 else '-'}"] = Q(
                traces["1"] + a * traces["s"] + b * traces["w"]
                + a * b * traces["sw"], 4)

    # J(M_v) as an alpha-combination on the regular orbit: check its type
    vector = defaultdict(Q)
    for position, column in enumerate(corners):
        vector[column] += alpha[position]
    def act(perm, vec):
        out = defaultdict(Q)
        for column, value in vec.items():
            out[perm[column]] += value
        return {k: v for k, v in out.items() if v}
    vec = {k: v for k, v in vector.items() if v}
    s_image, w_image = act(s, vec), act(w, vec)
    parity = {
        "s": "odd" if s_image == {k: -v for k, v in vec.items()} else
             "even" if s_image == vec else "mixed",
        "w": "odd" if w_image == {k: -v for k, v in vec.items()} else
             "even" if w_image == vec else "mixed",
    }
    return {
        "component": component_index,
        "regular_klein_four_corner_system": True,
        "induced_group_order": len(induced_perms),
        "corner_columns": list(corners),
        "traces_on_288_columns": traces,
        "klein_isotypic_dimensions_of_column_space": {k: str(v)
                                                      for k, v in iso.items()},
        "J_Mv_parity": parity,
        "J_Mv_isotypic": "s-_w-" if parity == {"s": "odd", "w": "odd"} else
                         str(parity),
        "target_isotypic_dim_for_residual": str(iso["s-_w-"]),
    }


def hom_count(component_index=1):
    src = {"rho+_w+": 7, "rho+_w-": 8, "rho-_w+": 8, "rho-_w-": 7}
    tgt_record = klein_isotypic_on_columns(component_index)
    if not tgt_record.get("regular_klein_four_corner_system"):
        return {"component": component_index, "available": False,
                "reason": "no regular Klein four-corner system on this component"}
    tgt = {k: int(Q(v)) for k, v in
           tgt_record["klein_isotypic_dimensions_of_column_space"].items()}
    pairs = [("rho+_w+", "s+_w+"), ("rho+_w-", "s+_w-"),
             ("rho-_w+", "s-_w+"), ("rho-_w-", "s-_w-")]
    total = sum(src[a] * tgt[b] for a, b in pairs)
    residual_block = src["rho-_w-"] * tgt["s-_w-"]
    return {
        "component": component_index,
        "available": True,
        "source_isotypic": src,
        "target_isotypic": tgt,
        "dim_Hom_Klein_graded30_to_288columns": total,
        "dim_Hom_on_the_residual_isotypic_only": residual_block,
        "constraints_from_the_single_required_equality": tgt["s-_w-"],
        "residual_solution_space_dimension":
            residual_block - tgt["s-_w-"],
        "overdetermination": "none - underdetermined",
    }


# ---------------------------------------------------------------- part 2 ---
def weyl_sign_control():
    """Expand the signed and the unsigned Cartan boundary in ONE fixed corner
    basis (the one built from the signed two-root Weyl operator)."""
    lower = PS.load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "ctl_lower")
    tangent = PS.load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "ctl_tangent")
    key = lambda label: (label[1], label[2])
    u_labels = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    other = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))

    def rho_label(label):
        matching_index, repeated = label
        matching = PS.permute_matching(tangent.MATCHINGS[matching_index], PS.RHO)
        return (tangent.MATCHING_INDEX[matching],
                PS.permute_edge(repeated, PS.RHO))

    def rho_vec(vector):
        return {(PS.rho_word(word), rho_label(label)): value
                for (word, label), value in vector.items()}

    def w_vec(vector, forced_sign=None):
        answer = defaultdict(Q)
        for (word, label), value in vector.items():
            changed, sign = PS.weyl_word(word)
            answer[(changed, label)] += (forced_sign
                                         if forced_sign is not None
                                         else sign) * value
        return {b: v for b, v in answer.items() if v}

    shared = u_labels & other
    f0 = {(PS.W, label): Q(1) for label in sorted(u_labels - shared)}
    basis = [f0, rho_vec(f0), w_vec(f0), rho_vec(w_vec(f0))]

    def expand(vector):
        residual, coefficients = dict(vector), []
        for cell in basis:
            b, unit = next(iter(cell.items()))
            value = residual.get(b, Q(0)) / unit
            coefficients.append(value)
            residual = PS.add(residual, PS.scale(-value, cell))
        return coefficients, not residual

    u_w = {(PS.W, label): Q(1) for label in sorted(u_labels)}
    signed = PS.add(PS.add(w_vec(u_w), PS.scale(-1, u_w)),
                    PS.scale(-1, rho_vec(PS.add(w_vec(u_w),
                                                PS.scale(-1, u_w)))))
    unsigned_wu = PS.add(w_vec(u_w, forced_sign=1), PS.scale(-1, u_w))
    unsigned = PS.add(unsigned_wu, PS.scale(-1, rho_vec(unsigned_wu)))
    signed_coeffs, signed_exact = expand(signed)
    unsigned_coeffs, unsigned_exact = expand(unsigned)
    return {
        "signed_in_reference_basis": [str(c) for c in signed_coeffs],
        "signed_exact": signed_exact,
        "unsigned_in_reference_basis": [str(c) for c in unsigned_coeffs],
        "unsigned_exact": unsigned_exact,
        "detected": tuple(unsigned_coeffs) != (Q(-1), Q(1), Q(1), Q(-1)),
    }


def mutations():
    results = {}

    # baseline
    base = PC.source_corner_structure()
    results["M0_baseline"] = {
        "corner_coefficients": base["B_in_corner_basis"],
        "equals_ALPHA": base["equals_ALPHA"],
        "endpoint_marginals": base["endpoint_marginals"],
        "tail_marginals": base["tail_marginals"],
        "detects": None,
    }

    # M1: flip the sign of one of the nine seed labels of u_012
    m1 = PC.source_corner_structure(label_mutation=0)
    results["M1_flip_one_seed_label_sign"] = {
        "corner_coefficients": m1["B_in_corner_basis"],
        "corner_expansion_is_exact": m1["corner_expansion_is_exact"],
        "equals_ALPHA": m1["equals_ALPHA"],
        "B_support": m1["B_support"],
        "detected": (not m1["equals_ALPHA"]) or (not m1["corner_expansion_is_exact"]),
    }

    # M2: strip the Weyl sign (use the unsigned word swap)
    m2 = PC.source_corner_structure(sign_mutation=1)
    results["M2_unsigned_Weyl"] = {
        "corner_coefficients": m2["B_in_corner_basis"],
        "equals_ALPHA": m2["equals_ALPHA"],
        "endpoint_marginals": m2["endpoint_marginals"],
        "tail_marginals": m2["tail_marginals"],
        "detected": not m2["equals_ALPHA"],
    }

    # M2b: same mutation, but expanded in the UNMUTATED corner basis.  This
    # is the control that actually tests the Weyl sign convention; M2 alone
    # cannot, because it rebuilds the corner basis with the mutated operator.
    results["M2b_unsigned_Weyl_in_reference_basis"] = weyl_sign_control()

    # M3: wrong rho -- transpose sites (1 2) instead of (1 4)
    wrong_rho = (0, 2, 1, 3, 4, 5)
    try:
        m3 = PS.build(perm=wrong_rho)[0]
        detected = (not m3["rho_closed_on_15_labels"]
                    or m3["rho_cycle_type_on_labels"] != {1: 1, 2: 7}
                    or not m3["rho_maps_u012_packet_to_u024_packet"]
                    or m3["l_support"] != 12)
        results["M3_wrong_rho_(1 2)"] = {
            "rho_closed_on_15_labels": m3["rho_closed_on_15_labels"],
            "rho_cycle_type": m3["rho_cycle_type_on_labels"],
            "maps_u012_to_u024": m3["rho_maps_u012_packet_to_u024_packet"],
            "l_support": m3["l_support"],
            "detected": detected,
        }
    except Exception as error:                       # noqa: BLE001
        results["M3_wrong_rho_(1 2)"] = {"raised": repr(error),
                                         "detected": True}

    # M4: wrong root sites for w -- use sites (2,3) instead of (1,4)
    try:
        m4 = PC.source_corner_structure(root_sites=(2, 3))
        results["M4_wrong_root_sites_(2 3)"] = {
            "corner_coefficients": m4["B_in_corner_basis"],
            "corner_expansion_is_exact": m4["corner_expansion_is_exact"],
            "equals_ALPHA": m4["equals_ALPHA"],
            "B_support": m4["B_support"],
            "detected": not m4["equals_ALPHA"],
        }
    except Exception as error:                       # noqa: BLE001
        results["M4_wrong_root_sites_(2 3)"] = {"raised": repr(error),
                                                "detected": True}

    # M5/M6: target-side alpha mutations on the regular Klein orbit
    records, alpha, _pure = PT.cached()
    reference = klein_isotypic_on_columns(1)
    corners = reference["corner_columns"]
    complete = PS.load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "mut_complete")
    base_mod = PS.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "mut_base")
    block = complete.component(base_mod, records[1]["target_degree"])
    labels = list(block["labels"])
    index = {label: i for i, label in enumerate(labels)}
    induced = {}
    for site_perm, colour_map in PC.target_symmetries(records[1]):
        image, ok = [], True
        for word, multiplier in labels:
            new_word = tuple(colour_map[word[site_perm.index(s)]]
                             for s in range(8))
            new_multiplier = tuple(sorted(
                PC.permute_cell_full(cell, site_perm, colour_map)
                for cell in multiplier))
            if (new_word, new_multiplier) not in index:
                ok = False
                break
            image.append(index[(new_word, new_multiplier)])
        if ok:
            induced.setdefault(tuple(image), (site_perm, colour_map))
    perms = sorted(induced)
    c0, c1, c2, c3 = corners
    s = next(p for p in perms if p[c0] == c1 and p[c2] == c3)
    w = next(p for p in perms if p[c0] == c2 and p[c1] == c3)

    def parity_of(coeffs):
        vec = {}
        for position, column in enumerate(corners):
            vec[column] = Q(coeffs[position])
        def act(perm):
            out = defaultdict(Q)
            for column, value in vec.items():
                out[perm[column]] += value
            return {k: v for k, v in out.items() if v}
        negative = {k: -v for k, v in vec.items() if v}
        vec_clean = {k: v for k, v in vec.items() if v}
        return {
            "s": "odd" if act(s) == negative else
                 "even" if act(s) == vec_clean else "mixed",
            "w": "odd" if act(w) == negative else
                 "even" if act(w) == vec_clean else "mixed",
        }

    results["M5_target_true_alpha"] = {
        "coefficients": [-1, 1, 1, -1],
        "parity": parity_of([-1, 1, 1, -1]),
        "detected": None,
    }
    for name, coeffs in (("M6_target_sign_flip", [-1, 1, -1, 1]),
                         ("M7_target_swap_two_corners", [1, -1, 1, -1]),
                         ("M8_target_all_plus", [1, 1, 1, 1])):
        parity = parity_of(coeffs)
        results[name] = {
            "coefficients": coeffs,
            "parity": parity,
            "detected": parity != {"s": "odd", "w": "odd"},
        }
    return results


def main():
    out = {
        "probe": "UNAUDITED RISK PROBE",
        "pinned_head": "b63c76c8624996044423a0dde60a2b60c9e8fa3d",
        "target_isotypic": [klein_isotypic_on_columns(i) for i in range(5)],
        "hom_counts": [hom_count(i) for i in range(5)],
        "mutation_controls": mutations(),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    (HERE / "isotypic_mutations_out.json").write_text(
        json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
