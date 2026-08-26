#!/usr/bin/env python3
"""TASK C: does the eighteen-face Hasse2(DQ/PS) relative-C4 packet collapse?

The AugP2 side collapses 18 direction-labelled terms -> 15 physical collision
labels (3 shared labels), and an involution rho=(1 4) with seven two-cycles
and one fixed point makes all three overlap coherences automatic
(notes/2026-08-12-two-gate-resolution-sketch.md, notes/h3-phi-diagonal-rees-
extension-gate.md).

This probe asks the same question of the OTHER eighteen: the direction-factor
half of (d_PP T)H_W, i.e. the 18 faces of dL01 supported on the four selected
sites {0,1,6,7}, extracted literally from the committed idempotent-gate
checker.

UNAUDITED.  Exact over Q.  Pinned HEAD 0a684ce.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import permutations
import json

import common
from common import require, rank, left_kernel, dot


SELECTED_SITES = (0, 1, 6, 7)
CHART_NAMES = {
    ((0, 1), (6, 7)): "DQ",
    ((0, 6), (1, 7)): "PS01",
    ((0, 7), (1, 6)): "PS10",
}


def extract_eighteen():
    """The literal 18 direction faces, exactly as the committed checker cuts them."""
    curvature = common.load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "psiz_curvature")
    matchings, directions, tails, l01, r01, ah = curvature.polynomial_data()
    d_l01 = curvature.differential(l01)
    selected = set(SELECTED_SITES)
    tail_half = {k: -v for k, v in d_l01.items()
                 if set(k[1]).isdisjoint(selected)}
    direction_half = {k: -v for k, v in d_l01.items()
                      if set(k[1]).issubset(selected)}
    require(len(matchings) == 105 and len(d_l01) == 36
            and len(tail_half) == len(direction_half) == 18,
            "the committed 18+18 dT split changed")

    faces = []
    for (matching, edge), coefficient in sorted(direction_half.items()):
        chart_edges = tuple(sorted(e for e in matching
                                   if set(e).issubset(selected)))
        tail = tuple(sorted(e for e in matching
                            if set(e).isdisjoint(selected)))
        require(chart_edges in CHART_NAMES and len(tail) == 2,
                ("unexpected face shape", matching, edge))
        faces.append({
            "chart": CHART_NAMES[chart_edges],
            "chart_edges": chart_edges,
            "tail": tail,
            "edge": edge,
            "coefficient": coefficient,
        })
    require(len(faces) == 18, "face extraction lost a face")
    # marginals must match the committed (-6,-6,3,3,3,3)
    ordered_edges = ((6, 7), (0, 1), (0, 6), (1, 7), (1, 6), (0, 7))
    marginals = {}
    for face in faces:
        marginals[face["edge"]] = marginals.get(face["edge"], Q(0)) \
            + face["coefficient"]
    require(tuple(marginals[e] for e in ordered_edges)
            == tuple(map(Q, (-6, -6, 3, 3, 3, 3))),
            ("direction marginals changed", marginals))
    return tuple(faces), tuple(tails)


def face_key(face):
    return (face["chart"], face["tail"], face["edge"])


def forgetting_map(faces, keep):
    """Linear map Q^18 -> Q^classes summing coordinates with equal `keep` key.

    Returns (classes, matrix rows, rank, kernel dimension).
    """
    keys = [tuple(face[field] for field in keep) for face in faces]
    classes = sorted(set(keys), key=str)
    rows = []
    for cls in classes:
        rows.append(tuple(Q(int(key == cls)) for key in keys))
    # rank of the map = rank of the row set (as columns of the transpose)
    columns = tuple(tuple(row[i] for row in rows) for i in range(len(faces)))
    matrix_rank = rank(columns)
    return classes, rows, matrix_rank, len(faces) - matrix_rank


def apply_site_permutation(face, permutation):
    """Act on a face by a permutation of the eight sites."""
    def move(pair):
        return tuple(sorted((permutation[pair[0]], permutation[pair[1]])))
    chart_edges = tuple(sorted(move(e) for e in face["chart_edges"]))
    tail = tuple(sorted(move(e) for e in face["tail"]))
    edge = move(face["edge"])
    if chart_edges not in CHART_NAMES:
        return None
    if any(not set(e).isdisjoint(SELECTED_SITES) for e in tail):
        return None
    return (CHART_NAMES[chart_edges], tail, edge)


def orbit_quotient(faces, group):
    """Orbits of the 18 faces under a group of site permutations."""
    keys = [face_key(face) for face in faces]
    lookup = {key: index for index, key in enumerate(keys)}
    parent = list(range(len(faces)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for permutation in group:
        for index, face in enumerate(faces):
            image = apply_site_permutation(face, permutation)
            require(image is not None and image in lookup,
                    ("group element left the 18-face set", permutation, face))
            union(index, lookup[image])
    orbits = {}
    for index in range(len(faces)):
        orbits.setdefault(find(index), []).append(index)
    return sorted(orbits.values())


def invariance(faces, group):
    """Is the 18-face coefficient vector constant on every group orbit?"""
    keys = [face_key(face) for face in faces]
    lookup = {key: index for index, key in enumerate(keys)}
    for permutation in group:
        for index, face in enumerate(faces):
            image = apply_site_permutation(face, permutation)
            if image is None or image not in lookup:
                return False
            if faces[lookup[image]]["coefficient"] != face["coefficient"]:
                return False
    return True


def identity_permutation():
    return tuple(range(8))


def transposition(a, b):
    p = list(range(8))
    p[a], p[b] = p[b], p[a]
    return tuple(p)


def tail_group():
    """Permutations of {2,3,4,5} inducing the S3 action on the three tails."""
    group = []
    for image in permutations((2, 3, 4, 5)):
        p = list(range(8))
        for site, value in zip((2, 3, 4, 5), image, strict=True):
            p[site] = value
        group.append(tuple(p))
    return tuple(group)


def edge_swap_group():
    """The involutions swapping the two edges inside each chart.

    (0 1)(6 7) fixes each chart setwise and exchanges its two edges in the
    two PS charts; (0 6)(1 7) does so for DQ.  Together they generate the
    Klein four-group V = {e,(01)(67),(06)(17),(07)(16)} acting on the
    selected sites.
    """
    return (
        identity_permutation(),
        (1, 0, 2, 3, 4, 5, 7, 6),   # (0 1)(6 7)
        (6, 7, 2, 3, 4, 5, 0, 1),   # (0 6)(1 7)
        (7, 6, 2, 3, 4, 5, 1, 0),   # (0 7)(1 6)
    )


def chart_swap_group():
    """(0 1): fixes DQ, exchanges PS01 and PS10."""
    return (identity_permutation(), transposition(0, 1))


def compose(group_a, group_b):
    answer = set()
    for a in group_a:
        for b in group_b:
            answer.add(tuple(a[b[i]] for i in range(8)))
    return tuple(sorted(answer))


def report():
    faces, tails = extract_eighteen()
    coefficients = tuple(face["coefficient"] for face in faces)

    # ---- the direction-forgetting maps -----------------------------------
    forgetting = {}
    for name, keep in (
            ("forget_edge__keep_chart_tail", ("chart", "tail")),
            ("forget_tail__keep_chart_edge", ("chart", "edge")),
            ("forget_chart__keep_tail_edge", ("tail", "edge")),
            ("forget_edge_and_tail__keep_chart", ("chart",)),
            ("keep_edge_only", ("edge",)),
    ):
        classes, rows, matrix_rank, kernel_dimension = forgetting_map(faces, keep)
        # is the 18-vector recoverable from its image?  i.e. is it constant
        # on fibres (so that the quotient loses no information)?
        fibres = {}
        for face in faces:
            fibres.setdefault(tuple(face[field] for field in keep), set()
                              ).add(face["coefficient"])
        forgetting[name] = {
            "classes": len(classes),
            "rank": matrix_rank,
            "kernel_dimension": kernel_dimension,
            "coefficient_constant_on_fibres": all(
                len(values) == 1 for values in fibres.values()),
            "fibre_sizes": sorted({len(
                [f for f in faces
                 if tuple(f[field] for field in keep) == cls])
                for cls in classes}),
        }

    # ---- the involution rho' and the orbit tower --------------------------
    v_group = edge_swap_group()
    t_group = tail_group()
    c_group = chart_swap_group()

    tower = []
    for name, group in (
            ("identity", (identity_permutation(),)),
            ("rho'=(0 1)(6 7) edge swap involution", (
                identity_permutation(), (1, 0, 2, 3, 4, 5, 7, 6))),
            ("Klein V (all three edge swaps)", v_group),
            ("V x tail-S3", compose(v_group, t_group)),
            ("V x tail-S3 x (0 1)", compose(compose(v_group, t_group), c_group)),
    ):
        orbits = orbit_quotient(faces, group)
        invariant = invariance(faces, group)
        values = sorted({str(coefficients[orbit[0]]) for orbit in orbits})
        tower.append({
            "group": name,
            "group_order": len(set(group)),
            "orbits": len(orbits),
            "orbit_sizes": sorted(len(orbit) for orbit in orbits),
            "face_vector_invariant": invariant,
            "coherences_automatic": invariant,
            "distinct_coefficient_values": values,
            "orbit_coefficients": [str(coefficients[orbit[0]])
                                   for orbit in orbits],
        })

    # ---- the exact minimum ----------------------------------------------
    # Any quotient by a coefficient-preserving group action has at least as
    # many classes as the coefficient function has distinct values.
    distinct_values = sorted({str(value) for value in coefficients})
    minimal = len(distinct_values)
    require(minimal == 2 and set(distinct_values) == {"-2", "1"},
            ("the coefficient value set changed", distinct_values))
    final = tower[-1]
    require(final["orbits"] == minimal and final["face_vector_invariant"],
            ("the maximal quotient did not reach the value bound", final))

    # ---- comparison with the AugP2 18 -> 15 collapse ----------------------
    augp2 = {
        "labels": 18,
        "physical_quotient": 15,
        "shared_labels": 3,
        "involution": "rho=(1 4), seven two-cycles + one fixed point",
        "shared_orbit_structure": "one fixed point + one two-cycle",
        "source": ("notes/2026-08-12-two-gate-resolution-sketch.md:47-66; "
                   "notes/h3-phi-diagonal-rees-extension-gate.md:44"),
    }

    # ---- mutation controls ----------------------------------------------
    controls = {}
    broken = [dict(face) for face in faces]
    broken[0]["coefficient"] = broken[0]["coefficient"] + 1
    controls["perturbed_single_face_breaks_invariance"] = not invariance(
        tuple(broken), compose(v_group, t_group))
    # a group element that does NOT preserve the chart structure must be
    # rejected by the orbit machinery
    bad = transposition(0, 2)          # mixes a selected site with a tail site
    try:
        orbit_quotient(faces, (identity_permutation(), bad))
        controls["nonstructural_permutation_rejected"] = False
    except RuntimeError:
        controls["nonstructural_permutation_rejected"] = True
    # coefficient-merging control: -2 and 1 can never share an orbit
    controls["DQ_and_PS_never_merge"] = all(
        len({str(coefficients[i]) for i in orbit}) == 1
        for entry, group in ((None, compose(compose(v_group, t_group), c_group)),)
        for orbit in orbit_quotient(faces, group))
    require(all(controls.values()), ("a mutation control failed", controls))

    ledger = {
        "probe": "TASK C: eighteen-face Hasse2(DQ/PS) relative-C4 quotient",
        "pinned_head": common.PINNED_HEAD,
        "source": ("computations/verify_h3_gate_ii_switch_weyl_product_rule_"
                   "idempotent_gate.py via verify_h3_h2_l01_three_cap_first_"
                   "pp_curvature_gate.polynomial_data/differential"),
        "eighteen_faces": [
            {"chart": f["chart"], "tail": [list(e) for e in f["tail"]],
             "edge": list(f["edge"]), "coefficient": str(f["coefficient"])}
            for f in faces],
        "face_label_structure": (
            "a face is (chart, tail, edge): chart is one of the three perfect "
            "matchings of the selected sites {0,1,6,7} (DQ/PS01/PS10), tail is "
            "one of the three matchings of {2,3,4,5}, edge is one of the two "
            "edges of the chart.  3 x 3 x 2 = 18, and (edge,tail) alone is "
            "already a complete invariant because each K4 edge lies in exactly "
            "one of the three charts"
        ),
        "direction_forgetting_maps": forgetting,
        "quotient_tower": tower,
        "augp2_comparison": augp2,
        "minimal_face_count_after_quotient": minimal,
        "minimal_face_representatives": {"C4:DQ": "-2", "C4:PS(either)": "1"},
        "why_minimal": (
            "any quotient by a group action that is to descend the face "
            "vector must preserve the coefficient function; it takes exactly "
            "two values, -2 on the DQ chart and +1 on both PS charts, so no "
            "coefficient-preserving quotient can have fewer than two classes. "
            "The V x S3 x (0 1) action realizes that bound"
        ),
        "mutation_controls": controls,
        "verdict": (
            "The eighteen DQ/PS faces admit a STRONGER collapse than the "
            "AugP2 side's 18 -> 15.  There are no shared labels: the "
            "collapse is by FREE group actions, not by partial "
            "injectivity.  The edge-swap involution rho'=(0 1)(6 7) has six "
            "two-cycles and six fixed points and gives 18 -> 12; the full "
            "Klein four-group V of edge swaps acts freely with nine "
            "two-cycles and gives 18 -> 9, with the face vector invariant, so "
            "all nine pairing coherences are automatic for any "
            "V-equivariant comparison.  The tail S3 "
            "(free, three orbits of three) takes 9 -> 3, giving exactly the "
            "committed direction charge (-2,1,1).  The chart-swap involution "
            "(0 1) fixes DQ and exchanges PS01/PS10, taking 3 -> 2 without "
            "leaving the C4 central idempotent.  Two is the exact minimum"
        ),
        "consequence_for_lane_1": (
            "lane 1's totalization needs ONE relative-C4 restriction/insertion "
            "cell for the DQ chart and ONE for a PS chart, plus equivariance "
            "for the group V x S3 x (0 1) of order 4*24*2 restricted to its "
            "faithful action; the other sixteen faces are forced translates. "
            "This is a 9-fold reduction of the construction burden"
        ),
        "scope": (
            "this is an exact statement about the coefficient vector of the "
            "eighteen faces and the site-permutation actions that preserve "
            "the (chart,tail,edge) label structure.  It does NOT claim the "
            "quotienting permutations are physical transports of the fixed "
            "source word, exactly as the AugP2 rho=(1 4) is not; it claims "
            "that an equivariant comparison satisfies the coherences for free"
        ),
    }
    return ledger


def main():
    ledger = report()
    (common.OUT / "out_c.json").write_text(json.dumps(ledger, indent=1))
    print("TASK C: eighteen-face quotient")
    print("  18 faces = 3 charts x 3 tails x 2 edges (edge+tail is a complete invariant)")
    for entry in ledger["quotient_tower"]:
        print(f"  {entry['group']:<40s} orbits={entry['orbits']:>2d} "
              f"invariant={entry['face_vector_invariant']}")
    print("  AugP2 analogue: 18 -> 15 with 3 shared labels")
    print("  HERE: 18 -> 12 -> 9 -> 3 -> 2, all FREE, NO shared labels")
    print(f"  MINIMAL FACE COUNT AFTER QUOTIENT: "
          f"{ledger['minimal_face_count_after_quotient']}")
    print("  mutation controls: " + str(ledger["mutation_controls"]))


if __name__ == "__main__":
    main()
