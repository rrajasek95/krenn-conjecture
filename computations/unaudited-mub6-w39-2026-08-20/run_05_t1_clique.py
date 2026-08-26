"""W39-T1 stage 2: from the CERTIFIED real-point count to the clique verdict.

PIPELINE (each step's soundness stated, because the verdict depends on it):

  (i)   Hermite trace form (run_04) gives the EXACT number N of distinct real
        points of the fibre V(H).  This is the completeness anchor.
  (ii)  Float Newton proposes approximate real points (untrusted).
  (iii) Exact rational Krawczyk certifies each proposal: EXACTLY ONE real
        solution in each box, boxes pairwise disjoint.  If we certify N
        disjoint boxes, the enumeration is PROVABLY COMPLETE by (i).
  (iv)  For every pair of boxes, rigorously enclose the two real quantities
            A(p,q) = sum_j ( 3 u^p_j u^q_j + v^p_j v^q_j )
            B(p,q) = sum_j (   u^p_j v^q_j - v^p_j u^q_j )
        (with (u_1,v_1) = (1,0)).  The two vectors are orthogonal iff
        A = B = 0.  If EITHER enclosure excludes 0, the pair is CERTIFIED
        NON-orthogonal.
  (v)   The "possible-edge" graph P contains the true orthogonality graph G as
        a subgraph, because every certified non-edge is a true non-edge.
        Therefore:  P has no 6-clique  ==>  G has no 6-clique  ==>  {I,H}
        extends to no MUB triple.  ONE-SIDED AND SOUND.
        The converse is NOT available: interval arithmetic can never certify
        an equality, so a 6-clique in P is only a CANDIDATE (that is exactly
        how the F_6 must-SAT calibration is read).

Ledger 18/21/23/26 apply: one-sided conclusions are labelled as such;
the control manifest is asserted at exit; outcomes are
verified / unchecked / refuted, never Boolean.
"""
import itertools
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "realroot"))

import numpy as np                                            # noqa: E402
from mub_systems import fibre_system, S6_EXP, F6_EXP, check_real_point  # noqa
from isolate import Iv, PolySystem, newton, krawczyk_certify  # noqa: E402

NV = 10
CKPT = os.path.join(HERE, "results_t1_clique.json")


# --------------------------------------------------------------------------
def parse_gens(gens):
    """Convert the Singular-syntax generators of mub_systems into the dense
    (coeff, exponent-tuple) form used by isolate.PolySystem, via sympy so the
    expansion is exact."""
    import sympy as sp
    names = [f"u{j}" for j in range(2, 7)] + [f"v{j}" for j in range(2, 7)]
    syms = sp.symbols(names)
    polys = []
    for g in gens:
        e = sp.expand(sp.sympify(g.replace("^", "**")))
        P = sp.Poly(e, *syms)
        polys.append([(Fraction(int(sp.numer(c)), int(sp.denom(c))), tuple(m))
                      for m, c in zip(P.monoms(), P.coeffs())])
    return PolySystem(polys, NV)


def propose(sysm, n_target, seed=0, max_tries=200000, report=None):
    """Float Newton from random starts on the torus; collect distinct hits."""
    rng = np.random.default_rng(seed)
    found = []
    tries = 0
    t0 = time.time()
    while len(found) < n_target and tries < max_tries:
        tries += 1
        th = rng.uniform(0, 2 * np.pi, 5)
        x0 = np.concatenate([np.cos(th), np.sqrt(3.0) * np.sin(th)])
        x, ok = newton(sysm, x0)
        if not ok:
            continue
        if not np.all(np.isfinite(x)):
            continue
        dup = False
        for y in found:
            if np.max(np.abs(np.array(y) - x)) < 1e-7:
                dup = True
                break
        if not dup:
            found.append(list(map(float, x)))
            if report:
                report(len(found), tries, time.time() - t0)
    return found, tries


def certify_all(sysm, approx, radii=(Fraction(1, 10**6), Fraction(1, 10**5),
                                     Fraction(1, 10**7), Fraction(1, 10**4))):
    boxes, failed = [], []
    for a in approx:
        c = [Fraction(float(t)).limit_denominator(10**14) for t in a]
        got = None
        for r in radii:
            got = krawczyk_certify(sysm, c, r)
            if got is not None:
                break
        if got is None:
            failed.append(a)
        else:
            boxes.append(got)
    return boxes, failed


def disjoint(boxes):
    n = len(boxes)
    for i in range(n):
        for j in range(i + 1, n):
            sep = False
            for k in range(NV):
                if boxes[i][k].hi < boxes[j][k].lo or boxes[j][k].hi < boxes[i][k].lo:
                    sep = True
                    break
            if not sep:
                return False, (i, j)
    return True, None


def AB_enclosures(bp, bq):
    """Rigorous enclosures of A and B for the pair of boxes (bp, bq)."""
    up = [Iv(1)] + list(bp[:5])
    vp = [Iv(0)] + list(bp[5:])
    uq = [Iv(1)] + list(bq[:5])
    vq = [Iv(0)] + list(bq[5:])
    A = Iv(0)
    B = Iv(0)
    for j in range(6):
        A = A + Iv(3) * up[j] * uq[j] + vp[j] * vq[j]
        B = B + up[j] * vq[j] - vp[j] * uq[j]
    return A, B


def find_cliques(adj, n, k=6, cap=200):
    """All k-cliques (up to `cap`) in the graph given by adjacency sets."""
    out = []

    def ext(cur, cand):
        if len(out) >= cap:
            return
        if len(cur) == k:
            out.append(tuple(cur))
            return
        if len(cur) + len(cand) < k:
            return
        cand = list(cand)
        for idx, v in enumerate(cand):
            ext(cur + [v], [w for w in cand[idx + 1:] if w in adj[v]])
            if len(out) >= cap:
                return

    ext([], range(n))
    return out


# --------------------------------------------------------------------------
def run_one(tag, exp, order, n_real, seed=0):
    gens, _ = fibre_system(exp, order)
    sysm = parse_gens(gens)
    rec = {"tag": tag, "n_real_from_hermite": n_real}
    t0 = time.time()
    approx, tries = propose(sysm, n_real, seed=seed)
    rec["n_proposed"] = len(approx)
    rec["newton_starts"] = tries
    rec["propose_seconds"] = round(time.time() - t0, 1)
    print(f"[{tag}] proposed {len(approx)}/{n_real} from {tries} starts "
          f"({rec['propose_seconds']}s)", flush=True)

    t0 = time.time()
    boxes, failed = certify_all(sysm, approx)
    rec["n_certified"] = len(boxes)
    rec["n_certify_failed"] = len(failed)
    rec["certify_seconds"] = round(time.time() - t0, 1)
    ok_disj, clash = disjoint(boxes)
    rec["boxes_pairwise_disjoint"] = ok_disj
    rec["disjoint_clash"] = clash
    complete = (len(boxes) == n_real and ok_disj)
    rec["enumeration_provably_complete"] = complete
    print(f"[{tag}] certified {len(boxes)} boxes, disjoint={ok_disj}, "
          f"complete={complete} ({rec['certify_seconds']}s)", flush=True)
    if not complete:
        rec["status"] = "UNCHECKED_INCOMPLETE_ENUMERATION"
        return rec

    t0 = time.time()
    n = len(boxes)
    adj = {i: set() for i in range(n)}
    n_certified_nonedges = 0
    for i, j in itertools.combinations(range(n), 2):
        A, B = AB_enclosures(boxes[i], boxes[j])
        if A.contains_zero() and B.contains_zero():
            adj[i].add(j)
            adj[j].add(i)
        else:
            n_certified_nonedges += 1
    rec["n_pairs"] = n * (n - 1) // 2
    rec["n_certified_nonedges"] = n_certified_nonedges
    rec["n_possible_edges"] = rec["n_pairs"] - n_certified_nonedges
    rec["max_degree_possible_graph"] = max(len(adj[i]) for i in range(n))
    rec["graph_seconds"] = round(time.time() - t0, 1)

    t0 = time.time()
    cl = find_cliques(adj, n, 6)
    rec["n_6cliques_in_possible_graph"] = len(cl)
    rec["clique_seconds"] = round(time.time() - t0, 1)
    rec["sample_cliques"] = [list(c) for c in cl[:5]]
    if len(cl) == 0:
        rec["status"] = "VERIFIED_NO_6CLIQUE"
    else:
        rec["status"] = "CANDIDATE_6CLIQUES_PRESENT"
    print(f"[{tag}] possible-edges={rec['n_possible_edges']} "
          f"maxdeg={rec['max_degree_possible_graph']} "
          f"6cliques={len(cl)} -> {rec['status']}", flush=True)
    return rec


def main():
    counts = json.load(open(os.path.join(HERE, "results_t1_counts.json")))
    st = {}
    if os.path.exists(CKPT):
        st = json.load(open(CKPT))
    declared = ["F6", "S6"]
    for tag, exp, order in [("F6", F6_EXP, 6), ("S6", S6_EXP, 3)]:
        if tag in st:
            print(f"[skip] {tag} checkpointed", flush=True)
            continue
        nr = counts["stages"][f"{tag}_viewA"]["n_real"]
        st[tag] = run_one(tag, exp, order, nr)
        with open(CKPT, "w") as fh:
            json.dump(st, fh, indent=2, default=str)
    missing = [d for d in declared if d not in st]
    if missing:
        print("CONTROL MANIFEST MISMATCH, missing:", missing)
        sys.exit(2)
    print("CONTROL MANIFEST OK:", sorted(st))
    print("\n=== CALIBRATION READ ===")
    print("F6 must-SAT  : expect CANDIDATE_6CLIQUES_PRESENT (>=16 second bases)"
          f" -> got {st['F6']['status']}, "
          f"{st['F6'].get('n_6cliques_in_possible_graph')} cliques")
    print("S6 target    : VERIFIED_NO_6CLIQUE would prove the exclusion"
          f" -> got {st['S6']['status']}")


if __name__ == "__main__":
    main()
