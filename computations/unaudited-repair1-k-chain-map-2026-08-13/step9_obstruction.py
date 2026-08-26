#!/usr/bin/env python3
"""STEP 9: is a CHAIN MAP possible at all (not just on the one class)?

A comparison map Phi : (operator module) -> (physical module) with
shadow_2 o Phi = D2 exists on all of ker(source,D1) iff
    S = D2(ker(source,D1))  is contained in  W = shadow_2(physical module).
No physical chain can ever put weight on a pair of cells that is not a pair
of DISJOINT cells of a direct-free matching.  So if S leaves the physical
coordinate subspace P, the chain map is obstructed for EVERY physical
inventory in every grade, and the offending coordinate is a separator.
"""
from collections import defaultdict
import json
import pickle

import common as C

PRIMES = [1_000_003, 999_983]


def order(row):
    return (row[0] >= 2, repr(row))


def reduce_mod(vector, basis, p):
    vector = {r: v % p for r, v in vector.items() if v % p}
    while vector:
        piv = min(vector, key=order)
        if piv not in basis:
            return vector, piv
        c = vector[piv]
        for r, v in basis[piv].items():
            x = (vector.get(r, 0) - c * v) % p
            if x:
                vector[r] = x
            else:
                vector.pop(r, None)
    return {}, None


def insert(vector, basis, p):
    red, piv = reduce_mod(vector, basis, p)
    if not red:
        return False, None
    inv = pow(red[piv], p - 2, p)
    basis[piv] = {r: v * inv % p for r, v in red.items()}
    return True, piv


m = C.modules()
cols, shifts = C.build_operator_columns(m, verbose=False)
base, cm = m["base"], m["commutator"]


def physical_pair(pair):
    (a1, b1, _x, _y), (a2, b2, _z, _w) = pair
    if len({a1, b1, a2, b2}) != 4:
        return False
    if frozenset((a1, b1)) == base.DIRECT_FREE_PAIR:
        return False
    if frozenset((a2, b2)) == base.DIRECT_FREE_PAIR:
        return False
    return True


out = []
for p in PRIMES:
    by_shift = defaultdict(list)
    for (_md, col), sh in zip(cols, shifts):
        by_shift[repr(sh)].append(col)
    Svecs = []
    for key in sorted(by_shift):
        basis = {}
        for col in by_shift[key]:
            added, piv = insert(dict(col), basis, p)
            if added and piv[0] == 2:
                Svecs.append(basis[piv])
    S = {}
    for v in Svecs:
        insert(dict(v), S, p)
    dimS = len(S)

    # project S onto the NON-physical pair coordinates
    nonphys_rows = []
    for v in S.values():
        w = {r: x for r, x in v.items() if not physical_pair(r[1])}
        nonphys_rows.append(w)
    NP = {}
    for w in nonphys_rows:
        insert(dict(w), NP, p)
    rank_nonphys = len(NP)

    # explicit separator: a single non-physical pair coordinate that S hits
    hit = sorted({r for v in S.values() for r in v
                  if not physical_pair(r[1])}, key=repr)
    rec = {
        "prime": p,
        "dim_S": dimS,
        "rank_of_S_projected_to_NON-physical_pair_coordinates": rank_nonphys,
        "dim_S_cap_physical_coordinate_subspace": dimS - rank_nonphys,
        "S_is_contained_in_physical_coordinates": rank_nonphys == 0,
        "example_separator_coordinates": [repr(r) for r in hit[:5]],
        "number_of_non_physical_coordinates_hit_by_S": len(hit),
    }
    print(json.dumps(rec, indent=1, sort_keys=True), flush=True)
    out.append(rec)

json.dump(out, open("step9_obstruction.json", "w"), indent=1, sort_keys=True)
