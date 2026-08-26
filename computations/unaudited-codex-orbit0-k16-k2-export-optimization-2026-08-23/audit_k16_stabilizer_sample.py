#!/usr/bin/env python3
import collections
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRUCT = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
CHECKPOINT = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin"
OUT = Path(__file__).with_name("results_k16_stabilizer_sample.json")


def main():
    b = STRUCT.read_bytes(); p = 0
    assert b[:11] == b"K16DIRECT1\0"; p = 11
    nt, nr, np, na = struct.unpack_from("<4I", b, p); p += 16
    assert (nt, nr, np, na) == (384, 485, 78, 12)
    anchors = b[p:p+12]; p += 12
    pos = {c:i for i,c in enumerate(anchors)}
    transforms=[]; perms=[]
    for _ in range(nt):
        transforms.append(b[p:p+252]); p += 252
        perms.append(b[p:p+12]); p += 12
    p += nr * 24
    pivots=[]
    for _ in range(np): pivots.append(tuple(b[p:p+12])); p += 12
    pivot_index={x:i for i,x in enumerate(pivots)}

    d = CHECKPOINT.read_bytes(); assert d[:8] == b"K16DIR1\0"
    n = struct.unpack_from("<Q", d, 8)[0]; assert n == 24_097_095
    starts=[0,3_000_000,6_000_000,9_000_000,12_000_000,15_000_000,18_000_000,23_000_000]
    indices=[]
    for start in starts:
        indices.extend(start + (20_000*j)//128 for j in range(128))

    stab_hist=collections.Counter(); pivot_hist=collections.Counter(); orbit_hist=collections.Counter()
    total_avail=total_orbits=0; examples=[]
    for idx in indices:
        off=16+32*idx; row=tuple(d[off:off+24])
        sig=[0]*12
        for c in row:
            if c in pos: sig[pos[c]]+=1
        avail=[i for i,q in enumerate(pivots) if all(sig[j]>=q[j] for j in range(12))]
        stabs=[]
        for ai,t in enumerate(transforms):
            if tuple(sorted(t[c] for c in row)) == row: stabs.append(ai)
        # Stabilizer acts on available pivots through the exact 12-anchor permutation.
        edges={i:set() for i in avail}
        for ai in stabs:
            perm=perms[ai]
            for i in avail:
                moved=[0]*12
                for old,x in enumerate(pivots[i]): moved[perm[old]]=x
                j=pivot_index[tuple(moved)]; assert j in edges
                edges[i].add(j); edges[j].add(i)
        seen=set(); norb=0
        for seed in avail:
            if seed in seen: continue
            norb+=1; stack=[seed]; seen.add(seed)
            while stack:
                x=stack.pop()
                for y in edges[x]:
                    if y not in seen: seen.add(y); stack.append(y)
        stab_hist[len(stabs)]+=1; pivot_hist[len(avail)]+=1; orbit_hist[norb]+=1
        total_avail+=len(avail); total_orbits+=norb
        if len(stabs)>1 and len(examples)<12:
            examples.append({"checkpoint_index":idx,"stabilizer":len(stabs),"available_pivots":len(avail),"pivot_orbits":norb})

    out={
        "status":"PASS_BOUNDED_EXACT_STABILIZER_SAMPLE",
        "sample_rows":len(indices), "sample_ranges":starts,
        "stabilizer_histogram":dict(sorted(stab_hist.items())),
        "available_pivot_histogram":dict(sorted(pivot_hist.items())),
        "stabilizer_pivot_orbit_histogram":dict(sorted(orbit_hist.items())),
        "total_available_pivots":total_avail,
        "total_stabilizer_pivot_orbits":total_orbits,
        "orbit_compression":total_avail/total_orbits,
        "examples_nontrivial_stabilizer":examples,
        "scope_guard":"1024 deterministic rows only; no full checkpoint orbit claim",
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))


if __name__ == "__main__": main()
