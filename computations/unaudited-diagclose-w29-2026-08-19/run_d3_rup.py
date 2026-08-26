#!/usr/bin/env python3
"""W29 D3 -- verify the UNSAT with an OWN RUP PROOF CHECKER (ledger 5/16).

pysat+cadical proof files are known to truncate silently (ledger 5), and a
passing certificate from the solver's own checker vindicates nothing.  So:
ask the solver for a DRUP proof, then REPLAY every lemma here with a checker
written from scratch -- each lemma must be a reverse-unit-propagation
consequence of the clauses verified so far, and the replay must end by
deriving the EMPTY CLAUSE.  Truncation shows up as "no empty clause".
Deletion lines are ignored, which is sound (RUP against a superset is still
RUP, and every clause in the database has already been verified).
"""
import json, sys, time
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
sys.path.insert(0, BASE)
import run_c2_unified as U
import run_d1_core as D
from pysat.solvers import Solver

def rup_check(orig, lemmas):
    """True iff every lemma is RUP and the empty clause is derived."""
    db = [tuple(sorted(set(c), key=abs)) for c in orig]
    watch = {}
    for i, c in enumerate(db):
        for l in c:
            watch.setdefault(l, []).append(i)
    def propagate(assump):
        val = {}
        stack = list(assump)
        for l in assump:
            if val.get(-l): return True
            val[l] = True
        # seed with every UNIT clause already in the database -- without this
        # a proof step with an empty assumption propagates nothing
        for c in db:
            if len(c) == 1:
                l = c[0]
                if val.get(-l): return True
                if not val.get(l):
                    val[l] = True
                    stack.append(l)
        while stack:
            l = stack.pop()
            for i in watch.get(-l, ()):
                c = db[i]
                un, sat = None, False
                cnt = 0
                for m in c:
                    if val.get(m): sat = True; break
                    if not val.get(-m): un = m; cnt += 1
                    if cnt > 1: break
                if sat or cnt > 1: continue
                if cnt == 0: return True
                if val.get(-un): return True
                val[un] = True
                stack.append(un)
        return False
    empty = False
    for lem in lemmas:
        if not lem:
            if propagate([]): empty = True; break
            return False, False
        if not propagate([-l for l in lem]):
            return False, False
        c = tuple(sorted(set(lem), key=abs))
        db.append(c)
        for l in c:
            watch.setdefault(l, []).append(len(db) - 1)
    return True, empty

def main():
    spec = sys.argv[1] if len(sys.argv) > 1 else ""
    Rs = tuple(tuple(int(ch) for ch in p) if p else ()
               for p in (spec.split("|") + ["", "", ""])[:3])
    OUT = f"{BASE}/results_d3_rup_{spec.replace('|','_') or 'singleton'}.json"
    RES = {}
    t0 = time.time()
    van = U.build_van(8, Rs)
    core, groups, base = D.extract_core(van, mandatory=())
    corecls = [list(cl) for k in core for cl in groups[k]]
    RES["core"] = {"n_groups": len(core), "n_clauses": len(corecls)}
    print(f"core: {len(core)} groups, {len(corecls)} clauses", flush=True)
    SOLV = sys.argv[2] if len(sys.argv) > 2 else "glucose42"
    for target, cls in (("core", corecls), ("full", [list(c) for c in van.cls])):
        with Solver(name=SOLV, bootstrap_with=cls,
                    with_proof=True) as S:
            sat = S.solve()
            proof = S.get_proof()
        lemmas = []
        for ln in proof:
            ln = ln.strip()
            if ln.startswith("d "): continue
            toks = ln.split()
            if toks and toks[-1] == "0": toks = toks[:-1]
            try: lemmas.append([int(x) for x in toks])
            except ValueError:
                RES.setdefault(target, {})["parse_error"] = ln[:80]; break
        ok, empty = rup_check(cls, lemmas)
        RES[target] = {"solver_sat": sat, "n_lemmas": len(lemmas),
                       "all_lemmas_RUP": ok, "empty_clause_derived": empty,
                       "VERIFIED_UNSAT": (sat is False) and ok and empty}
        print(f"[{target}] solver SAT={sat}; {len(lemmas)} lemmas; all RUP="
              f"{ok}; empty clause={empty}", flush=True)
        json.dump(RES, open(OUT, "w"), indent=1, default=str)
    RES["seconds"] = round(time.time() - t0, 1)
    json.dump(RES, open(OUT, "w"), indent=1, default=str)
    print(f"wrote {OUT} ({RES['seconds']}s)")

if __name__ == "__main__":
    main()
