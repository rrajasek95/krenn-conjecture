#!/usr/bin/env python3
"""UNAUDITED RISK PROBE - rank/dimension counts and missing-object audit.

Pinned HEAD b63c76c8624996044423a0dde60a2b60c9e8fa3d, snapshot ./snap.
Exact arithmetic (integers / Fraction) only.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import permutations
import json
from pathlib import Path

import probe_source as PS
import probe_target as PT
import probe_compare as PC

HERE = Path(__file__).resolve().parent


def cycle_type(perm_map, domain):
    seen, cycles = set(), []
    for item in domain:
        if item in seen:
            continue
        orbit, cursor = [item], item
        seen.add(item)
        cursor = perm_map[item]
        while cursor != item:
            orbit.append(cursor)
            seen.add(cursor)
            cursor = perm_map[cursor]
        cycles.append(len(orbit))
    return Counter(cycles)


def source_dimensions():
    lower = PS.load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "dim_lower")
    tangent = PS.load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "dim_tangent")
    key = lambda label: (label[1], label[2])
    u_labels = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    other = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))
    labels = tuple(sorted(u_labels | other))

    def rho_label(label):
        matching_index, repeated = label
        matching = PS.permute_matching(tangent.MATCHINGS[matching_index], PS.RHO)
        return (tangent.MATCHING_INDEX[matching],
                PS.permute_edge(repeated, PS.RHO))

    rho_on_labels = {label: rho_label(label) for label in labels}
    ct = cycle_type(rho_on_labels, labels)
    fixed = [label for label in labels if rho_on_labels[label] == label]
    shared = sorted(u_labels & other)
    shared_fixed = [label for label in shared if rho_on_labels[label] == label]

    # word-graded module U_15 (x) Q{W,W'}: rho acts diagonally, w = -swap.
    graded = [(word, label) for word in (PS.W, PS.WP) for label in labels]
    rho_g = {(word, label): (PS.rho_word(word), rho_label(label))
             for word, label in graded}
    ct_g = cycle_type(rho_g, graded)

    # Klein isotypic dimensions on the 30-dim graded module.
    # rho: 15 transpositions -> even 15 / odd 15.
    # w  : signed word swap  -> w = -(word swap); word swap has 15 transpositions
    #      so w-even = (swap)-odd = 15, w-odd = (swap)-even = 15.
    # Joint: compute exactly by projector traces.
    def rho_apply(basis):
        return rho_g[basis], 1

    def w_apply(basis):
        word, label = basis
        changed, sign = PS.weyl_word(word)
        return (changed, label), sign

    def trace(op):
        total = 0
        for basis in graded:
            image, sign = op(basis)
            if image == basis:
                total += sign
        return total

    def compose(f, g):
        def out(basis):
            b1, s1 = g(basis)
            b2, s2 = f(b1)
            return b2, s1 * s2
        return out

    t_id, t_rho = len(graded), trace(rho_apply)
    t_w = trace(w_apply)
    t_rw = trace(compose(rho_apply, w_apply))
    isotypic = {}
    for a in (1, -1):
        for b in (1, -1):
            isotypic[f"rho{'+' if a > 0 else '-'}_w{'+' if b > 0 else '-'}"] = (
                Q(t_id + a * t_rho + b * t_w + a * b * t_rw, 4))
    return {
        "U15_dimension": len(labels),
        "rho_cycle_type_on_U15": dict(sorted(ct.items())),
        "rho_even_dim_U15": ct[1] + ct[2],
        "rho_odd_dim_U15": ct[2],
        "rho_fixed_labels": [str(x) for x in fixed],
        "shared_labels": [str(x) for x in shared],
        "shared_labels_rho_fixed": [str(x) for x in shared_fixed],
        "shared_labels_form": (
            f"{len(shared_fixed)} rho-fixed + "
            f"{(len(shared) - len(shared_fixed)) // 2} rho-two-cycle"),
        "residual_support_meets_shared_labels": bool(
            {label for label in labels
             if (Q(int(label in frozenset(map(rho_label, u_labels))))
                 - Q(int(label in u_labels)))} & set(shared)),
        "graded_module_dimension": len(graded),
        "rho_cycle_type_on_graded": dict(sorted(ct_g.items())),
        "klein_isotypic_dimensions": {k: str(v) for k, v in isotypic.items()},
    }


def target_dimensions():
    records, alpha, _pure = PT.cached()
    out = []
    for record in records:
        pure = record["pure"]
        lookup = {frozenset(m): i for i, (_w, m, _b) in enumerate(pure)}
        syms = PC.target_symmetries(record)
        # induced action on *all* 288 columns, for each symmetry
        # (needed for the equivariant Hom count)
        out.append({
            "component": record["component"],
            "columns": record["columns"],
            "literal_features": record["feature_count"],
            "pure_columns": len(pure),
            "pure_column_boundary": 90,
            "site_colour_symmetries": len(syms),
        })
    return out


def equivariant_hom_counts(component_index=1):
    """dim Hom_G(U_15 (x) Q{W,W'}, column space) for the induced target Klein
    group, versus the number of constraints imposed by the required equality.
    """
    records, alpha, _pure = PT.cached()
    record = records[component_index]
    complete = PS.load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "dim_complete")
    base = PS.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "dim_base")
    block = complete.component(base, record["target_degree"])
    labels = list(block["labels"])
    index = {label: i for i, label in enumerate(labels)}
    syms = PC.target_symmetries(record)

    induced = {}
    for site_perm, colour_map in syms:
        image = []
        ok = True
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

    counts = {}
    for perm in induced_perms:
        ct = cycle_type({i: perm[i] for i in range(len(labels))},
                        range(len(labels)))
        counts[str(list(perm[:8])) + "..."] = {
            "cycle_type": dict(sorted(ct.items())),
            "trace": ct[1],
        }
    return {
        "component": component_index,
        "columns": len(labels),
        "induced_permutations_of_all_columns": len(induced_perms),
        "traces": {k: v["trace"] for k, v in counts.items()},
    }


def missing_objects():
    """What a legitimate intertwiner needs that no committed object supplies."""
    computations = PS.SNAP / "computations"
    text = {path.name: path.read_text() for path in computations.glob("*.py")}
    def mentions(needle):
        return sorted(name for name, body in text.items() if needle in body)
    return {
        "H_w_explicit_only_in": mentions("root_homotopy"),
        "H_w_ambient": (
            "verify_h3_sl2_weyl_cartan_prism.py builds H_w on polynomial "
            "differential forms in TWO variables (x,y), exterior degrees "
            "0..2, polynomial degree <=6.  It is not defined on the "
            "collision-label module, on U_15, or on the eight-site literal "
            "feature module."),
        "J_col_constructed": False,
        "d_on_collision_labels_constructed": False,
        "consequence": (
            "K d(u_012) itself is NOT computable from committed data.  Only "
            "dK(u)+Kd(u) = (1-rho)(w-1)u_012 is.  Every invariant reported "
            "for the 'residual' is therefore an invariant of the Cartan "
            "boundary (1-rho)(w-1)u, plus the structural facts that "
            "im K subset im(1-rho) and that d, K are rho- and w-equivariant."),
        "s_endpoint_swap_on_literal_module": False,
        "s_ambient": (
            "verify_h3_endpoint_odd_cartan_prism_augmentation.py realizes the "
            "endpoint swap s and tail swap w only as 4x4 permutation matrices "
            "on four FORMAL corners E+T0,E-T0,E+T1,E-T1.  No committed object "
            "makes s or w act on the 288 literal columns or the ~19116 "
            "eight-site features."),
        "corner_to_literal_column_dictionary": False,
        "corner_ambiguity": (
            "CORNERS=('P+q00','P-q00','P+q11','P-q11') are never matched to "
            "specific literal pure columns: verify_h3_literal_mv_cap_cartan_"
            "composition.py audits all 5 components x all 15 four-subsets = "
            "75 aggregates and requires their digests to be DISTINCT.  So "
            "'J(M_v)' names 75 different literal vectors."),
    }


def main():
    out = {
        "probe": "UNAUDITED RISK PROBE",
        "pinned_head": "b63c76c8624996044423a0dde60a2b60c9e8fa3d",
        "source": source_dimensions(),
        "target": target_dimensions(),
        "equivariant": equivariant_hom_counts(1),
        "missing": missing_objects(),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    (HERE / "dimensions_out.json").write_text(
        json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
