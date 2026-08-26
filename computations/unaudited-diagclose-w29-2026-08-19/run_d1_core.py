#!/usr/bin/env python3
"""W29 D1 -- a MINIMAL UNSAT CORE for the abstraction, plus an INDEPENDENT
DPLL that re-decides it without any external SAT solver.

The headline verdict is "UNSAT" from a third-party solver, which is exactly
the kind of thing ledger 5/13/16 says not to trust on its own.  So:

 1. group the clauses by the mathematical constraint they came from;
 2. extract an UNSAT core over those groups and shrink it by deletion until
    every remaining group is necessary;
 3. re-decide the core with a DPLL written here from scratch (unit
    propagation + branching, no pysat), and re-decide the FULL clause set the
    same way;
 4. print the core in mathematical language.

argv: [case] e.g. "" for the singleton case, "3|4|5" for R=({3},{4},{5}).
"""
from __future__ import annotations

import json
import sys
import time

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import run_c2_unified as U                                          # noqa: E402

RES, RAN = {}, []
OUT = None


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# ---------------------------------------------------------------- own DPLL
def dpll(clauses, nv):
    """Independent SAT decision: returns True iff SATISFIABLE."""
    occ = {}
    cls = []
    for cl in clauses:
        s = set(cl)
        if any(-l in s for l in s):
            continue                      # tautology
        cls.append(tuple(s))
    for i, cl in enumerate(cls):
        for l in cl:
            occ.setdefault(l, []).append(i)
    assign = {}

    def prop(stack):
        added = []
        while stack:
            l = stack.pop()
            v, s = abs(l), l > 0
            if v in assign:
                if assign[v] != s:
                    return None
                continue
            assign[v] = s
            added.append(v)
            for i in occ.get(-l, ()):
                cl = cls[i]
                unassigned, sat = [], False
                for m in cl:
                    av = assign.get(abs(m))
                    if av is None:
                        unassigned.append(m)
                    elif av == (m > 0):
                        sat = True
                        break
                if sat:
                    continue
                if not unassigned:
                    for v2 in added:
                        del assign[v2]
                    return None
                if len(unassigned) == 1:
                    stack.append(unassigned[0])
        return added

    def choose():
        best, cnt = None, -1
        for i, cl in enumerate(cls):
            un = []
            sat = False
            for m in cl:
                av = assign.get(abs(m))
                if av is None:
                    un.append(m)
                elif av == (m > 0):
                    sat = True
                    break
            if sat or not un:
                continue
            if best is None or len(un) < cnt:
                best, cnt = un[0], len(un)
                if cnt == 2:
                    break
        return best

    def rec(depth):
        l = choose()
        if l is None:
            for cl in cls:
                if not any(assign.get(abs(m)) == (m > 0) for m in cl):
                    return False
            return True
        for lit in (l, -l):
            added = prop([lit])
            if added is not None:
                if rec(depth + 1):
                    return True
                for v in added:
                    del assign[v]
        return False

    sys.setrecursionlimit(100000)
    return rec(0)


# ------------------------------------------------------------ core extraction
def group_key(tag):
    if tag[0] == "A3q":
        return ("A3",) + tag[1:4]
    if tag[0] == "A3":
        return tuple(tag[:4])
    return tuple(tag)


def extract_core(van, mandatory=("A0", "A3")):
    from pysat.solvers import Cadical153
    groups = {}
    for tag, cl in van.tagged:
        groups.setdefault(group_key(tag), []).append(cl)
    keys = [k for k in groups if k[0] not in mandatory]
    base = [cl for k in groups if k[0] in mandatory for cl in groups[k]]
    act = {}
    nv = van.nvars
    soft = []
    for k in keys:
        nv += 1
        act[k] = nv
        for cl in groups[k]:
            soft.append(list(cl) + [-nv])
    with Cadical153(bootstrap_with=base + soft) as S:
        assum = [act[k] for k in keys]
        assert not S.solve(assumptions=assum), "core: expected UNSAT"
        core = [k for k in keys if -act[k] in set(S.get_core() or [])] \
            or list(keys)
        cur = list(core)
        i = 0
        while i < len(cur):
            trial = cur[:i] + cur[i + 1:]
            if not S.solve(assumptions=[act[k] for k in trial]):
                cur = trial
            else:
                i += 1
    return cur, groups, base


def pretty(k):
    if k[0] == "A1":
        return f"haf(T^{k[1]}|V) = 1  (the pure word)"
    if k[0] == "A2":
        return (f"partition condition: haf(T^0|{list(k[1])}) "
                f"haf(T^1|{list(k[2])}) haf(T^2|{list(k[3])}) = 0")
    if k[0] == "A3":
        return (f"Laplace: haf(T^{k[1]}|{list(k[2])}) expanded at site {k[3]}")
    if k[0] == "CASE0":
        return f"star vanishing: x^{k[1]}_{k[2]} = 0 (site not free)"
    if k[0] == "CASEnz":
        return f"x^{k[1]}_{{y_{k[1]}}} != 0  (choice of y_c)"
    if k[0] == "CASEh":
        return f"h_{k[1]}(y_{k[1]}) != 0  (choice of y_c)"
    if k[0] == "FREE":
        return (f"free set: colour {k[1]} at site {k[2]}, split "
                f"{list(k[3])}|{list(k[4])}")
    if k[0] == "XF":
        return (f"x^{k[1]}_{{y_{k[1]}}} != 0 collapses "
                f"haf(T^{k[1]}|{list(k[2])}+z)")
    return str(k)


def main():
    global OUT
    spec = sys.argv[1] if len(sys.argv) > 1 else ""
    Rs = tuple(tuple(int(ch) for ch in part) if part else ()
               for part in (spec.split("|") + ["", "", ""])[:3])
    OUT = f"{BASE}/results_d1_core_{spec.replace('|','_') or 'singleton'}.json"
    t0 = time.time()
    van = U.build_van(8, Rs)
    print(f"case Rs={Rs}: {van.nvars} vars, {len(van.cls)} clauses",
          flush=True)
    RES["case"] = {"Rs": [list(r) for r in Rs], "nvars": van.nvars,
                   "nclauses": len(van.cls)}
    ck("setup")

    t1 = time.time()
    core, groups, base = extract_core(van)
    kinds = {}
    for k in core:
        kinds[k[0]] = kinds.get(k[0], 0) + 1
    print(f"[core] {len(core)} groups, kinds {kinds} "
          f"({round(time.time()-t1,1)}s)", flush=True)
    RES["core"] = {"n_groups": len(core), "kinds": kinds,
                   "groups": [pretty(k) for k in core]}
    RAN.append("core")
    ck("core")

    corecls = base + [cl for k in core for cl in groups[k]]
    used = sorted({abs(l) for cl in corecls for l in cl})
    RES["core_clauses"] = {"n_clauses": len(corecls), "n_vars": len(used)}
    print(f"[core] as clauses: {len(corecls)} clauses over {len(used)} "
          f"variables", flush=True)

    t1 = time.time()
    own_core = dpll(corecls, van.nvars)
    print(f"[own DPLL] core satisfiable? {own_core} (want False) "
          f"({round(time.time()-t1,1)}s)", flush=True)
    RES["own_dpll_core_sat"] = own_core
    RAN.append("own_dpll_core")
    ck("dpll_core")

    t1 = time.time()
    own_full = dpll(van.cls, van.nvars)
    print(f"[own DPLL] FULL clause set satisfiable? {own_full} (want False) "
          f"({round(time.time()-t1,1)}s)", flush=True)
    RES["own_dpll_full_sat"] = own_full
    RAN.append("own_dpll_full")

    RES["PASS"] = (own_core is False and own_full is False)
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
