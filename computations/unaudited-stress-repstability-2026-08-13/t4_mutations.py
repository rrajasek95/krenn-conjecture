#!/usr/bin/env python3
"""T4: mutation controls.  Every check below MUST fail in the mutated setting;
if a mutation still 'passes', the corresponding positive test is vacuous.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import (  # noqa: E402
    edge, endpoint_neighbors, marked_occurrence, occurrences, perfect_matchings,
    switch_neighbors,
)
from scheme import Scheme  # noqa: E402
from t2_transfer_residuals import endpoint_projector_check, get_scheme  # noqa: E402
from transfer import one_step_row  # noqa: E402

RESULTS = {}


def record(name, mutated_fails, detail=""):
    RESULTS[name] = {"mutation_detected": bool(mutated_fails), "detail": detail}
    flag = "DETECTED" if mutated_fails else "*** NOT DETECTED ***"
    print(f"  {name:<52} {flag}  {detail}")


def main():
    h = 4
    scheme = get_scheme(h)
    space = scheme.space
    lam = h * h - 3 * h + 1

    print(f"T4 mutation controls at h={h}")

    # --- 1. wrong eigenvalue in the matching projector
    c = Q(1, 2 * h - 1)
    e1 = tuple(v - c for v in space.edge_indicator((0, 1)))
    good = space.apply_A(e1) == tuple(lam * v for v in e1)
    bad = [lam + d for d in (-2, -1, 1, 2)]
    bad_ok = any(space.apply_A(e1) == tuple(t * v for v in e1) for t in bad)
    record("E1 eigenvalue: correct lambda vs lambda+/-1,2", good and not bad_ok,
           f"lambda={lam}")

    # --- 2. wrong summand projection: [2h-4,4] and [2h-4,2,2] components of
    #        the transfer row must be zero; the level-2 part of a 2-edge
    #        indicator must be nonzero (positive control for the machinery)
    big_sites = tuple(range(2 * h + 2))
    marked = marked_occurrence(h)
    row, _ = one_step_row(h, marked, big_sites)
    rest = tuple(v for v in big_sites if v not in (marked[0], marked[1]))
    relabel = {v: i for i, v in enumerate(rest)}
    vector = [Q(0)] * len(space.points)
    for m in perfect_matchings(rest):
        canonical = tuple(sorted(edge(relabel[a], relabel[b]) for a, b in m))
        vector[space.index[canonical]] = Q(row.get((marked[0], marked[1], m), 0))
    content = scheme.shape_content(tuple(vector))
    absent = [(2 * h - 4, 4), (2 * h - 4, 2, 2)]
    record("transfer row has NO level-2 shapes",
           all(s not in content for s in absent), f"content={content}")

    two_edge = space.partial_matching_indicator([(0, 1), (2, 3)])
    content2 = scheme.shape_content(two_edge)
    record("machinery positive control: 2-edge indicator HAS level-2 shapes",
           any(s in content2 for s in absent), f"content={content2}")

    # --- 3. mutated matching projector must not flatten the fibres
    fibres_flat_good = endpoint_projector_check(row, h + 1, marked, big_sites)
    from lib_stress import switch_neighbors as sw
    occ = occurrences(big_sites)
    index = {o: i for i, o in enumerate(occ)}
    values = tuple(Q(row.get(o, 0)) for o in occ)
    A = tuple(tuple(index[(o[0], o[1], m)] for m in sw(o[2])) for o in occ)
    image = tuple(sum(values[j] for j in r) for r in A)
    mutated_flat = tuple(a - (lam + 1) * b for a, b in zip(image, values, strict=True))
    fibre = {mutated_flat[index[(marked[0], marked[1], m)]]
             for m in perfect_matchings(rest)}
    record("matching projector with lambda+1 fails to flatten",
           len(fibre) > 1 and fibres_flat_good["matching_projector_flattens_all_fibres"],
           f"{len(fibre)} distinct values in one fibre")

    # --- 4. mutated endpoint projector roots
    flat = tuple(a - lam * b for a, b in zip(image, values, strict=True))
    B = tuple(tuple(index[n] for n in endpoint_neighbors(o, big_sites)) for o in occ)
    def cubic(roots, start):
        cur = start
        for theta in roots:
            img = tuple(sum(cur[j] for j in r) for r in B)
            cur = tuple(a - theta * b for a, b in zip(img, cur, strict=True))
        return cur
    good_const = len(set(cubic((-2, 2 * h - 2, 2 * h), flat))) == 1
    bad_const = len(set(cubic((-2, 2 * h - 2, 2 * h + 2), flat))) == 1
    record("endpoint projector with a wrong root is not constant",
           good_const and not bad_const)

    # --- 5. mutated B_h (drop the s-endpoint half) breaks the five sectors
    def half_B(vector):
        out = []
        for o in occ:
            p, s, matching = o
            partner = {}
            for a, b in matching:
                partner[a] = b
                partner[b] = a
            total = Q(0)
            for t in big_sites:
                if t in (p, s):
                    continue
                u = partner[t]
                rest_m = tuple(e for e in matching if t not in e)
                total += vector[index[(t, s, tuple(sorted(rest_m + (edge(p, u),))))]]
            out.append(total)
        return tuple(out)
    std = lambda x: 1 if x == 0 else (-1 if x == 1 else 0)
    sym = tuple(Q(std(o[0]) + std(o[1])) for o in occ)
    broken = half_B(sym) == tuple((2 * h - 2) * v for v in sym)
    record("half-B_h loses the (2h-2,+) eigenvalue", not broken)

    # --- 6. broken spectator inclusion
    small = Scheme(h - 1)
    big = Scheme(h)
    spect = edge(2 * h - 2, 2 * h - 1)
    def good_iota(m):
        return tuple(sorted(m + (spect,)))
    def half_adjacency(points, index):
        rows = []
        for m in points:
            row = []
            for i, j in combinations(range(len(m)), 2):
                a, b = m[i]
                cc, d = m[j]
                keep = tuple(v for k, v in enumerate(m) if k not in (i, j))
                row.append(index[tuple(sorted(keep + (edge(a, cc), edge(b, d))))])
            rows.append(tuple(row))
        return tuple(rows)

    def check_iota(iota, permute_pull=False, half=False):
        embed = {small.index[m]: big.index[iota(m)] for m in small.points}
        big_adj = (half_adjacency(big.points, big.index) if half
                   else big.space.adjacency)
        small_adj = (half_adjacency(small.points, small.index) if half
                     else small.space.adjacency)
        order = list(range(len(small.points)))
        if permute_pull:
            order[0], order[1] = order[1], order[0]
        for i in range(len(small.points)):
            basis = [Q(0)] * len(small.points)
            basis[i] = Q(1)
            pushed = [Q(0)] * len(big.points)
            for k, v in enumerate(basis):
                pushed[embed[k]] += v
            img = tuple(sum(pushed[j] for j in r) for r in big_adj)
            pulled = tuple(img[embed[order[k]]] for k in range(len(small.points)))
            want = tuple(sum(basis[j] for j in r) for r in small_adj)
            if pulled != want:
                return False
        return True

    record("pi A iota = A has teeth (permuted pull fails)",
           check_iota(good_iota) and not check_iota(good_iota, permute_pull=True))
    # NOT a control: this one records that the corrected intertwining is a
    # generic property of local switch moves, not a property of A_h.
    generic = check_iota(good_iota, half=True)
    RESULTS["OBSERVATION pi X iota = X for the non-equivariant half-switch"] = {
        "mutation_detected": True,
        "holds_for_half_switch": bool(generic),
        "detail": ("the corrected intertwining pi X iota = X holds for ANY "
                   "operator whose moves either stay inside the residual or "
                   "destroy the spectator edge; it is therefore weak evidence"),
    }
    print(f"  {'OBSERVATION: pi X iota = X also for half-switch':<52} "
          f"{generic}")

    path = Path(__file__).resolve().parent / "t4_mutations.json"
    path.write_text(json.dumps(RESULTS, indent=1, sort_keys=True))
    print("wrote", path)
    assert all(v["mutation_detected"] for v in RESULTS.values()), "a control failed"


if __name__ == "__main__":
    main()
