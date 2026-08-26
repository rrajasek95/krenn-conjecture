#!/usr/bin/env python3
"""W9 Task B1 -- MECHANISM (1): (STAR)-pinning sparsity, pushed to a lemma.

W6's (STAR): for a mixed-exact source and any pair (p,q), every NON-CONSTANT
colouring v of U = B\\{p,q} satisfies

        C(v) * A_pq  =  - P(v) M(v) Q(v)^T ,
        P(v)[i][u] = A_pu[i][v_u],   Q(v)[j][u] = A_qu[j][v_u].

W9 LEMMA 1 (ROW DEATH).  If some non-constant v has C(v) != 0 and
p_i(v) := (A_pu[i][v_u])_{u in U} = 0, then ROW i of A_pq vanishes entirely:
C(v) A_pq[i][j] = -(p_i(v))^T M(v) q_j(v) = 0 for every j.
Dually for columns at q.

W9 COROLLARY 2 (conditional cell FLOOR).  Put
        n_pu(i) = #cells in row i of block A_pu,
        F_p(i)  = { u != p : n_pu(i) = 3 }   ("full rows at p in colour i").
{v : p_i(v) = 0} is nonempty iff F_p(i) is contained in {q}.  So, ASSUMING
(G) every nonempty such box contains a NON-CONSTANT v with C(v) != 0:
  * F_p(i) = {}      => row i of A_pq dies for EVERY q => slot (p,i) is
                        uncovered, contradicting the pure word c=i;
  * F_p(i) = {u0}    => row i of A_p,u0 dies, contradicting n_p,u0(i) = 3.
Hence |F_p(i)| >= 2 for every (p,i), so
        2 Sigma = sum_{p,i} n_p(i) >= sum_{p,i} 3|F_p(i)| >= 3*2*3N = 18N,
        Sigma >= 9N = 72 at N = 8.
This is a cell FLOOR, i.e. it pushes AGAINST H4's ceiling.

This script (a) verifies (STAR) and LEMMA 1 exactly on every calibration
object, (b) measures the F_p(i) profile, (c) measures how often (G) holds --
its failure is the honest soft spot.  Mutation controls included.
"""
from __future__ import annotations
import importlib, json, random, sys
from fractions import Fraction as F
from itertools import combinations, product
import w9_core as w9
from w9_core import COLORS, cells, hafnian, oriented, pair_expansion

SIZE = 8


def star_row_zeros(source, p, i, U):
    """Z_p(i,u) for u in U, and the box size."""
    Z = {}
    for u in U:
        blk = oriented(source, p, u)
        Z[u] = tuple(c for c in COLORS if blk[i][c] == 0)
    size = 1
    for u in U:
        size *= len(Z[u])
    return Z, size


def check_lemma1(source, size=SIZE, max_v=None, verbose=False):
    """Exhaustively verify LEMMA 1 on every (p,q,i) and every non-constant v
    with C(v)!=0 and p_i(v)=0.  Returns (#fires, #violations, detail)."""
    fires = viol = 0
    detail = []
    for p, q in combinations(range(size), 2):
        U = tuple(u for u in range(size) if u not in (p, q))
        blk = oriented(source, p, q)
        for vword in product(COLORS, repeat=len(U)):
            if len(set(vword)) == 1:
                continue
            v = {u: vword[n] for n, u in enumerate(U)}
            Cv = hafnian(source, U, v)
            if Cv == 0:
                continue
            for i in COLORS:
                if any(oriented(source, p, u)[i][v[u]] != 0 for u in U):
                    continue
                fires += 1
                bad = [j for j in COLORS if blk[i][j] != 0]
                if bad:
                    viol += 1
                    if len(detail) < 5:
                        detail.append({"p": p, "q": q, "i": i,
                                       "v": list(vword), "live_cols": bad})
    return fires, viol, detail


def F_profile(source, size=SIZE):
    out = {}
    for p in range(size):
        for i in COLORS:
            Fset = [u for u in range(size) if u != p
                    and sum(1 for c in COLORS if oriented(source, p, u)[i][c]) == 3]
            n_p_i = sum(1 for u in range(size) if u != p
                        for c in COLORS if oriented(source, p, u)[i][c])
            out[(p, i)] = {"F": Fset, "|F|": len(Fset), "n_p_i": n_p_i}
    return out


def genericity_G(source, size=SIZE):
    """For every (p,i,q) with a nonempty kill-box, does it contain a
    NON-CONSTANT v with C(v)!=0?  (G) is the escape hatch of Corollary 2."""
    tot = holds = empty_box = nonconst_absent = allC0 = 0
    for p in range(size):
        for q in range(size):
            if q == p:
                continue
            U = tuple(u for u in range(size) if u not in (p, q))
            for i in COLORS:
                Z, boxsize = star_row_zeros(source, p, i, U)
                tot += 1
                if boxsize == 0:
                    empty_box += 1
                    continue
                found = False
                anynonconst = False
                for vword in product(*[Z[u] for u in U]):
                    if len(set(vword)) == 1:
                        continue
                    anynonconst = True
                    v = {u: vword[n] for n, u in enumerate(U)}
                    if hafnian(source, U, v) != 0:
                        found = True
                        break
                if found:
                    holds += 1
                elif not anynonconst:
                    nonconst_absent += 1
                else:
                    allC0 += 1
    return {"triples": tot, "G_holds": holds, "box_empty": empty_box,
            "box_all_constant": nonconst_absent, "all_C_zero": allC0}


if __name__ == "__main__":
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

    def build(params):
        blocks = mod.build_stage_a(params)
        return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
                for u, v in combinations(range(8), 2)}
    BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
            (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
            (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))

    OUT = {}
    print("=" * 78)
    print("B1  MECHANISM (1): (STAR) pinning -> LEMMA 1 (row death).  Exact.")
    print("=" * 78)
    for lbl, src in (("STAGE_A_BASE", w9.load_stage_a()),
                     ("STAGE_A_GENERIC", build(BEST))):
        print(f"\n[{lbl}]")
        fires, viol, det = check_lemma1(src)
        print(f"   LEMMA 1 exhaustive check: fired {fires} times, "
              f"VIOLATIONS = {viol}   {'PASS' if viol == 0 else 'FAIL'}")
        prof = F_profile(src)
        sizes = sorted(d["|F|"] for d in prof.values())
        print(f"   |F_p(i)| over the 24 (vertex,colour) slots: {sizes}")
        print(f"      min = {min(sizes)}   #slots with |F|<2 = "
              f"{sum(1 for s in sizes if s < 2)}   (Corollary 2 predicts |F|>=2"
              f" for an EXACT source)")
        g = genericity_G(src)
        print(f"   genericity (G): {g}")
        Sigma = sum(len(cells(src[e])) for e in combinations(range(8), 2))
        floor = sum(3 * d["|F|"] for d in prof.values()) / 2
        print(f"   Sigma = {Sigma};  measured floor (3/2)*sum|F| = {floor}"
              f";  Corollary-2 floor for an exact source = 72")
        OUT[lbl] = {"lemma1_fires": fires, "lemma1_violations": viol,
                    "lemma1_detail": det, "F_sizes": sizes,
                    "min_F": min(sizes), "slots_below_2": sum(1 for s in sizes if s < 2),
                    "genericity": g, "Sigma": Sigma,
                    "measured_floor": floor,
                    "F_profile": {f"{p},{i}": d for (p, i), d in prof.items()}}

    # ---------------- MUTATION CONTROLS -----------------------------------
    print("\n" + "=" * 78)
    print("CONTROLS -- the checker must FIRE on objects where the lemma is false")
    print("=" * 78)
    rng = random.Random(4242)
    ctrl = {}
    # C1: a random (non-mixed-exact) source -- LEMMA 1's hypothesis uses (STAR),
    #     which needs mixed exactness, so violations MUST appear.
    bad = 0
    for t in range(3):
        src = {(u, v): [[F(rng.randint(-3, 3)) for _ in COLORS] for _ in COLORS]
               for u, v in combinations(range(8), 2)}
        # sparsify so that kill-boxes are nonempty
        for e in src:
            for i in COLORS:
                for j in COLORS:
                    if rng.random() < 0.55:
                        src[e][i][j] = F(0)
        f, v_, d = check_lemma1(src)
        print(f"   C1 random source #{t}: fires {f}, violations {v_} "
              f"{'-> control FIRES (good)' if v_ > 0 else '-> no violation'}")
        bad += (v_ > 0)
    ctrl["C1_random_violations_seen"] = bad
    # C2: perturb STAGE_A_GENERIC by one cell (breaks mixed exactness):
    src = build(BEST)
    mut = {k: [list(r) for r in v] for k, v in src.items()}
    tgt = next((k, i, j) for k in mut for i in COLORS for j in COLORS if mut[k][i][j])
    mut[tgt[0]][tgt[1]][tgt[2]] += F(1)
    print(f"   C2 mixed defects after 1-cell perturbation: "
          f"{w9.mixed_defect_count(mut)} (>0 required)")
    f, v_, d = check_lemma1(mut)
    print(f"   C2 LEMMA 1 on the perturbed source: fires {f}, violations {v_}")
    ctrl["C2_perturbed_violations"] = v_
    ctrl["C2_perturbed_fires"] = f
    OUT["controls"] = ctrl
    with open("results_b1_star_rowdeath.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("\nwrote results_b1_star_rowdeath.json")
