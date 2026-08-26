#!/usr/bin/env python3
"""Cheap exact referee for the frozen exhaustive Rust cycle-Morse census."""

from collections import Counter, defaultdict
from hashlib import sha256
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "census_k16_cycle_morse.rs"
RESULT = HERE / "results_k16_cycle_morse_census.json"
INPUT = (ROOT / "computations"
         / "unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
         / "weighted_k16_literal_orbits.dafsa")

def require(x,msg):
    if not x: raise RuntimeError(msg)

def digest(path): return sha256(path.read_bytes()).hexdigest()

def decode(cell):
    edge,a,b=cell//9,(cell%9)//3,cell%3;seen=0
    for u in range(8):
        for v in range(u+1,8):
            if seen==edge:return u,v,a,b
            seen+=1
    raise RuntimeError(cell)

def graph_data(row):
    adj=defaultdict(list)
    for cell in row:
        u,v,a,b=decode(cell);x=(u,a);y=(v,b);adj[x].append(y);adj[y].append(x)
    require(len(adj)==24 and set(map(len,adj.values()))=={2},"not balanced")
    seen=set();components=[];owner={}
    for start in sorted(adj):
        if start in seen:continue
        stack=[start];seen.add(start);vertices=[]
        while stack:
            x=stack.pop();vertices.append(x)
            for y in adj[x]:
                if y not in seen:seen.add(y);stack.append(y)
        number=len(components)
        for x in vertices:owner[x]=number
        components.append(len(vertices))
    return tuple(sorted(components)),owner

def pivot_flags(row):
    partition,owner=graph_data(row);by_site=defaultdict(list)
    for cell in row:
        u,v,a,b=decode(cell);record=(v,a,b,owner[(u,a)])
        if record not in by_site[u]:by_site[u].append(record)
        record=(u,b,a,owner[(v,b)])
        if record not in by_site[v]:by_site[v].append(record)
    def rec(mask,cycles,colors):
        if mask==255:
            return (True,len(set(colors))>1)
        u=next(i for i in range(8) if not mask>>i&1);any_pm=False
        for v,a,b,cycle in by_site[u]:
            if mask>>v&1 or cycles>>cycle&1:continue
            nxt=list(colors);nxt[u]=a;nxt[v]=b
            any_child,mixed=rec(mask|(1<<u)|(1<<v),cycles|(1<<cycle),nxt)
            any_pm|=any_child
            if mixed:return True,True
        return any_pm,False
    return partition,rec(0,0,[0]*8)

def build(mutate=False):
    require(digest(SOURCE)=="634f8a5dc15f51eae377aa68551a921ee7e612707166b8d2f78ae32afb2bde3f","source drift")
    require(digest(RESULT)=="ec51e2eaa42ceddf69038c537b61a879ff2413a1d3a325e98f4316ad227a1d5e","result drift")
    require(digest(INPUT)=="5efddefa05c48099a54b5bc6ffad08ce0171f211e266ca5e938977f2d9aa12b9","input drift")
    r=json.loads(RESULT.read_text());
    if mutate:r["total"]["pivotable_orbits"]-=1
    require((r["input_rows"],r["total"]["pivotable_orbits"],r["total"]["unpivotable_orbits"])==(1848174,751988,1096186),"total mutation")
    require(r["reason_counts"]=={"fewer_than_four_cycles":889820,"no_physical_pm_across_four_cycles":206366,"pivotable":751988},"reason census")
    require(sum(x["orbits"] for x in r["by_cycle_count"].values())==1848174,"cycle count total")
    require(sum(x["orbits"] for x in r["by_cycle_partition"].values())==1848174 and len(r["by_cycle_partition"])==120,"partition total")
    blocker=r["first_unpivotable"];brow=bytes.fromhex(blocker["row"]);bp,bflags=pivot_flags(brow)
    require(list(bp)==blocker["cycle_partition"] and bflags==(False,False) and blocker["reason"]=="no_physical_pm_across_four_cycles","blocker replay")
    witness=r["first_pivotable_witness"];row=bytes.fromhex(witness["row"]);selected=bytes.fromhex(witness["selected_cells"]);mult=bytes.fromhex(witness["multiplier"])
    require(Counter(row)==Counter(selected+mult) and len(selected)==4 and len(mult)==20,"witness factorization")
    sites=set();colors=[];_part,owner=graph_data(row);cycles=set()
    for cell in selected:
        u,v,a,b=decode(cell);sites.update((u,v));colors.extend((a,b));cycles.add(owner[(u,a)])
    require(sites==set(range(8)) and len(cycles)==4 and len(set(colors))>1 and "".join(map(str,[next(a if u==i else b for cell in selected for u,v,a,b in [decode(cell)] if i in (u,v)) for i in range(8)]))==witness["mixed_word"],"pivot witness")
    return {"status":"PASS","logical_sha256":"ba1e0e39def4378e5d0b2da7a8600a6d5486d44b0bfb23a264aadf65449612af"}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--mutate",action="store_true");a=p.parse_args();print(json.dumps(build(a.mutate),sort_keys=True))
