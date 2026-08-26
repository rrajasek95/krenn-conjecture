#!/usr/bin/env python3
"""W16 -- sub-alphabet BOX forcing tests for family (R).

SOUNDNESS.  Fix alphabets alpha_s subset {0,1,2} for the eight sites and let
Box = prod_s alpha_s.  Use as equations ONLY the words of Box that are
EFFECTIVELY CLEAN (fibre = F(Gamma); exact criterion, no proxy) -- each such
mixed word contributes the true equation Phi_w = 0.  Every Phi_w for w in Box
involves only cells A_uv[i][j] with i in alpha_u, j in alpha_v, so the whole
computation lives in that restricted variable set: using a SUBSET of the true
equations and the exact variables they involve.  Hence

  "Phi_target in sat(I_box, product of the box cells)"  ==>  Phi_target = 0
  on every source with this template,

which for a target with exactly ONE extra monomial gives  extra = 0  --
impossible (occupied cells are nonzero).  Fewer equations can only make the
test fail, never make it wrongly succeed.
"""
from __future__ import annotations
import os, sys, json, itertools, time
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (W8_IMMUNE, VarMap, phi_poly, full_pm_indices,
                      extras_at, MIXED, EDGES, FULL)
from w16_sing import run_singular, poly_str

HERE = os.path.dirname(os.path.abspath(__file__))


def kmap_of(T):
    fullm = full_pm_indices(T)
    return {w: len(extras_at(T, w, fullm)) for w in
            itertools.product(range(3), repeat=8)}, fullm


def box_data(T, kmap, fullm, alpha, target):
    ws = [w for w in itertools.product(*alpha)]
    assert tuple(target) in ws
    clean = [w for w in ws if w != tuple(target) and kmap[w] == 0
             and len(set(w)) > 1]
    vm = VarMap(T)
    eqs = [phi_poly(T, vm, w, fullm) for w in clean]
    tgt = phi_poly(T, vm, tuple(target), fullm)
    used = set()
    for p in eqs + [tgt]:
        for mon in p:
            used.update(mon)
    return clean, eqs, tgt, sorted(used), vm


def forcing(eqs, tgt, used, timeout=1200, mode="sat"):
    names = {v: "z%d" % i for i, v in enumerate(used)}
    ll = ['LIB "elim.lib";',
          "ring r = 0,(%s),dp;" % ",".join(names[v] for v in used)]
    for i, p in enumerate(eqs, 1):
        ll.append("poly g%d = %s;" % (i, poly_str(p, names)))
    ll.append("poly tt = %s;" % poly_str(tgt, names))
    ll.append("ideal Iid = %s;" % ",".join("g%d" % i
                                           for i in range(1, len(eqs) + 1)))
    ll.append("poly PP = %s;" % "*".join(names[v] for v in used))
    if mode == "sat":
        ll.append("ideal Jid = PP;")
        ll.append("list LL = sat(Iid,Jid);")
        ll.append("ideal SS = LL[1];")
        ll.append('"FORCED:"; (reduce(tt,groebner(SS))==0);')
    else:                                    # power / Rabinowitsch-lite
        ll.append("ideal GI = groebner(Iid);")
        ll.append("poly cur = tt;")
        for d in range(1, 5):
            ll.append("cur = cur*PP;")
            ll.append('"POW%d:"; (reduce(cur,GI)==0);' % d)
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    dt = time.time() - t0
    if st == "TIMEOUT":
        return None, dt
    if mode == "sat":
        return out.split("FORCED:")[1].strip().split()[0] == "1", dt
    for d in range(1, 5):
        if out.split("POW%d:" % d)[1].strip().split()[0] == "1":
            return True, dt
    return False, dt


def candidate_boxes(kmap, target, max_words=512):
    """alphabets containing the target; sites get 1, 2 or 3 colours."""
    out = []
    per_site = []
    for s in range(8):
        opts = [(target[s],)]
        for c in range(3):
            if c != target[s]:
                opts.append(tuple(sorted((target[s], c))))
        opts.append((0, 1, 2))
        per_site.append(opts)
    for alpha in itertools.product(*per_site):
        n = 1
        for a in alpha:
            n *= len(a)
        if n < 8 or n > max_words:
            continue
        ws = list(itertools.product(*alpha))
        nclean = sum(1 for w in ws if w != tuple(target) and kmap[w] == 0
                     and len(set(w)) > 1)
        if nclean >= 4:
            out.append((nclean, n, alpha))
    out.sort(key=lambda t: (-t[0], t[1]))
    return out


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    ktarget = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    nboxes = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    maxw = int(sys.argv[4]) if len(sys.argv) > 4 else 128
    T = W8_IMMUNE[m]
    kmap, fullm = kmap_of(T)
    tgts = [w for w in MIXED if kmap[w] == ktarget]
    print("m=%d |F(Gamma)|=%d  #targets(k=%d)=%d"
          % (m, len(fullm), ktarget, len(tgts)))
    results = []
    tried = 0
    for tgt in tgts:
        boxes = candidate_boxes(kmap, tgt, max_words=maxw)
        if not boxes:
            continue
        nclean, nw, alpha = boxes[0]
        clean, eqs, tt, used, vm = box_data(T, kmap, fullm, alpha, tgt)
        if len(used) > 60 or len(eqs) < 6:
            continue
        tried += 1
        if tried > nboxes:
            break
        v, dt = forcing(eqs, tt, used, timeout=900)
        rec = dict(target="".join(map(str, tgt)),
                   alphabet=[list(a) for a in alpha],
                   n_eqs=len(eqs), n_vars=len(used), forced=v, secs=round(dt, 1))
        print("  %s alpha=%s eqs=%d vars=%d -> forced=%s (%.1fs)"
              % (rec["target"], rec["alphabet"], rec["n_eqs"], rec["n_vars"],
                 v, dt))
        results.append(rec)
    json.dump(results, open(os.path.join(
        HERE, "results_box_m%d_k%d.json" % (m, ktarget)), "w"), indent=1)


if __name__ == "__main__":
    main()
