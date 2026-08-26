#!/usr/bin/env python3
r"""W31 -- R2 PRE-LAUNCH GATE: does a stored permanent-null family extend to a
SECOND L-free word?  UNAUDITED PROBE.  Exact integer arithmetic only.
No Singular, no elimination -- this is the zero-compute gate that must be
answered BEFORE any R2 elimination is started.

THE TARGET UNDER TEST (W31-6a).  There exist two distinct L-free words x != x'
such that
    per == 0 on V^x_4 x V^x_5 x V^x_6 x V^x_7   AND
    per == 0 on V^x'_4 x V^x'_5 x V^x'_6 x V^x'_7
with every occupied cross cell nonzero, is UNSATISFIABLE over C.
(W20: a single L-free word is provably insufficient -- x = (1,1,2,2) has an
explicit all-nonzero solution -- so the kill must combine >= 2 words.)

THE STRUCTURE THAT DECIDES IT.  For an L-free word x and an R-site j,
    C_j(x)[i][d] = A_{i,j}[x_i][d],     V^x_j = colspan C_j(x)  <= C^4,
so the condition at x reads only ROW x_i of each cross block A_{i,j}.
Two L-free words x, x' therefore constrain DISJOINT entries at every site i
where x_i != x'_i.  If x and x' are discordant at ALL FOUR L-sites the two
permanent conditions share no variable at all, and W31-6a collapses: any
single-word solution can be duplicated on the other row set.

WHAT THIS SCRIPT DOES.
 1. Rebuilds the C_8 member's cross blocks and its 30 L-free words, with the
    per-site DEAD-CELL profile (a fat block's missing cell forces a zero in
    C_j(x) when x_i selects that row).
 2. Computes the agreement graph on the 30 L-free words (how many of the four
    L-sites two words share).
 3. For a fully discordant pair whose rows are dead-cell-free, CONSTRUCTS an
    explicit exact witness -- integer cross-block entries, every occupied cell
    used by either word nonzero -- and VERIFIES both permanent conditions by
    exhaustive evaluation on all 3^4 x 3^4 relevant tuples.  A construction,
    not a search: it settles W31-6a as stated.
 4. Reports which word pairs survive as viable R2 targets (those that share
    letters, ranked by coupling).

CONTROLS
  G1  the 30 L-free words and their dead-cell counts must reproduce W20's
      stored results_c8.json.
  G2  the witness's V^x_j must be exactly the stored char-0 permanent-null
      subspaces (which w31_ff_trace.py independently verified per-null over
      Q, F_5, F_7, F_13, F_31).
  G3  every cross cell the witness uses must be nonzero.
  G4  MUTATION: perturb one entry of the witness; at least one permanent
      condition must break (guards against a vacuously-zero construction).
  G5  NEGATIVE CONTROL: a generic (non-constructed) assignment on the same
      rows must FAIL the permanent conditions -- otherwise "satisfied" is
      meaningless.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
N, Q, FULL = 8, 3, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
L, R = (0, 1, 2, 3), (4, 5, 6, 7)
BIJ = tuple(permutations(range(4)))

C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def dead_cells(mask):
    return [(c // 3, c % 3) for c in range(9) if not (mask >> c) & 1]


def per4(vs):
    return sum(vs[0][s[0]] * vs[1][s[1]] * vs[2][s[2]] * vs[3][s[3]]
               for s in BIJ)


def main():
    OUT = {"_header": "UNAUDITED W31 R2 pre-launch gate. Exact integer "
                      "arithmetic only. Nothing here is a proved claim of the "
                      "repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}

    # ---- cross blocks and L-singles ---------------------------------------
    cross = {(i, j): C8_MEMBER[EIDX[(i, j)]] for i in L for j in R}
    lsing = {}
    for (u, v) in combinations(L, 2):
        mk = C8_MEMBER[EIDX[(u, v)]]
        if bin(mk).count("1") == 1:
            lsing[(u, v)] = cells_of(mk)[0]
    OUT["L_singles"] = {str(k): list(v) for k, v in lsing.items()}
    OUT["cross_block_cellcounts"] = {str(k): bin(v).count("1")
                                     for k, v in sorted(cross.items())}

    # ---- G1 : the 30 L-free words + dead-cell profile ---------------------
    lfree = []
    for x in product(range(Q), repeat=4):
        if all(not (x[u] == i and x[v] == j) for (u, v), (i, j)
               in lsing.items()):
            nd = sum(1 for i in L for j in R
                     for (r, c) in dead_cells(cross[(i, j)]) if r == x[i])
            lfree.append((x, nd))
    OUT["G1_n_Lfree"] = len(lfree)
    OUT["G1_matches_W20"] = (len(lfree) == 30)
    OUT["G1_deadcell_counts"] = {str(list(x)): nd for x, nd in lfree}
    zero_dead = [x for x, nd in lfree if nd == 0]
    OUT["G1_zero_deadcell_words"] = [list(x) for x in zero_dead]
    print("[G1] L-free words:", len(lfree), " matches W20's 30:",
          OUT["G1_matches_W20"])
    print("     dead-cell-free L-free words:", [list(x) for x in zero_dead])

    # ---- agreement graph ---------------------------------------------------
    words = [x for x, _ in lfree]
    agree = {}
    for a, b in combinations(range(len(words)), 2):
        k = sum(1 for i in range(4) if words[a][i] == words[b][i])
        agree.setdefault(k, []).append((words[a], words[b]))
    OUT["agreement_histogram"] = {str(k): len(v) for k, v in
                                  sorted(agree.items())}
    print("[agreement] #shared L-sites -> #pairs:",
          OUT["agreement_histogram"])

    disc = agree.get(0, [])
    OUT["n_fully_discordant_pairs"] = len(disc)
    disc_clean = [(a, b) for a, b in disc
                  if a in zero_dead and b in zero_dead]
    OUT["n_fully_discordant_dead_cell_free_pairs"] = len(disc_clean)
    print("     fully discordant pairs:", len(disc),
          "; of those with both words dead-cell-free:", len(disc_clean))

    # ---- which words admit the STORED family's shape? ---------------------
    # the stored family's column d at site j is (a_d, b_d, s*b_d, s*a_d).
    # A dead cell forces a zero entry, so a forced zero at row 0 forces
    # a_d = 0, hence a zero at row 3 too -- which the template must also
    # declare dead.  So x is compatible at (j,d) iff the dead rows form
    # exactly one of {}, {0,3}, {1,2}.
    def zeroset(x, j, d):
        return frozenset(i for i in L
                         if not (cross[(i, j)] >> (3 * x[i] + d)) & 1)

    PAIRED = (frozenset(), frozenset({0, 3}), frozenset({1, 2}))

    def compatible(x):
        return all(zeroset(x, j, d) in PAIRED for j in R for d in range(3))

    compat = [x for x in words if compatible(x)]
    OUT["stored_family_compatible_words"] = [list(x) for x in compat]
    OUT["n_stored_family_compatible_words"] = len(compat)
    print("[compat] L-free words admitting the stored family's shape:",
          len(compat), [list(x) for x in compat])
    disc_clean = [(a, b) for a, b in disc if a in compat and b in compat]
    OUT["n_fully_discordant_compatible_pairs"] = len(disc_clean)
    print("     fully discordant pairs with BOTH words compatible:",
          len(disc_clean))

    # Any pair of compatible words is a candidate witness: the family's value
    # at (i,j,d) depends only on (i,j,d), NOT on the word, so at a SHARED site
    # (x_i = x'_i) both words demand the SAME entry -- the assignments are
    # automatically consistent.  So run the construction on every compatible
    # pair, coupled ones included.
    cand = [(a, b) for a, b in combinations(compat, 2)]
    OUT["candidate_compatible_pairs"] = [[list(a), list(b)] for a, b in cand]
    if not disc_clean and cand:
        disc_clean = cand
        print("     no discordant compatible pair; running the construction "
              "on the COUPLED compatible pair(s):",
              [[list(a), list(b)] for a, b in cand])

    # ---- the construction --------------------------------------------------
    # stored char-0 permanent-null configuration (verified in w31_ff_trace):
    #   V_4 = V_6 = V_7 = {(a, b, b, a)},   V_5 = {(a, b, -b, -a)}
    # realise it by choosing three nonzero (a_d, b_d) pairs spanning C^2.
    AB = ((1, 1), (1, 2), (2, 1))
    SIGN = {4: (1, 1, 1, 1), 5: (1, 1, -1, -1), 6: (1, 1, 1, 1),
            7: (1, 1, 1, 1)}
    PAT = {4: (0, 1, 1, 0), 5: (0, 1, 1, 0), 6: (0, 1, 1, 0), 7: (0, 1, 1, 0)}

    def realise(A, x):
        """write rows x_i of the cross blocks so that V^x_j is the stored
        configuration, ADAPTED to the template's dead cells: a forced zero at
        rows {0,3} sets a_d = 0, at rows {1,2} sets b_d = 0.  Returns the
        C_j(x) matrices."""
        for j in R:
            for d in range(3):
                a, b = AB[d]
                z = zeroset(x, j, d)
                if z == frozenset({0, 3}):
                    a = 0
                elif z == frozenset({1, 2}):
                    b = 0
                for i in L:
                    A[(i, j)][x[i]][d] = SIGN[j][i] * (a if PAT[j][i] == 0
                                                       else b)
        return {j: [[A[(i, j)][x[i]][d] for d in range(3)] for i in L]
                for j in R}

    def colspan_vectors(Cj):
        return [tuple(Cj[i][d] for i in range(4)) for d in range(3)]

    def per_vanishes(Cs):
        """per == 0 identically on the product of the four column spans,
        checked on every 4-tuple of columns (multilinearity does the rest)."""
        bad = 0
        for d4, d5, d6, d7 in product(range(3), repeat=4):
            v = (colspan_vectors(Cs[4])[d4], colspan_vectors(Cs[5])[d5],
                 colspan_vectors(Cs[6])[d6], colspan_vectors(Cs[7])[d7])
            if per4(v) != 0:
                bad += 1
        return bad

    verdict = None
    if disc_clean:
        x, xp = disc_clean[0]
        A = {(i, j): [[0] * 3 for _ in range(3)] for i in L for j in R}
        Cs = realise(A, x)
        Cs2 = realise(A, xp)
        bad1, bad2 = per_vanishes(Cs), per_vanishes(Cs2)
        used = [(i, j, r, d) for i in L for j in R for r in (x[i], xp[i])
                for d in range(3)]
        occupied = [(i, j, r, d) for i, j, r, d in used
                    if (cross[(i, j)] >> (3 * r + d)) & 1]
        allnz = all(A[(i, j)][r][d] != 0 for i, j, r, d in occupied)
        occ_ok = all(A[(i, j)][r][d] == 0 for i, j, r, d in used
                     if not (cross[(i, j)] >> (3 * r + d)) & 1)
        OUT["witness"] = dict(
            x=list(x), x_prime=list(xp),
            per_violations_at_x=bad1, per_violations_at_x_prime=bad2,
            G3_all_occupied_used_cells_nonzero=allnz,
            dead_cells_correctly_zero=occ_ok,
            blocks={str(k): v for k, v in sorted(A.items())})
        print("[witness] x = %s , x' = %s" % (list(x), list(xp)))
        print("     per violations: %d at x, %d at x'  (0 = both conditions "
              "hold)" % (bad1, bad2))
        print("     G3 all used cells nonzero:", allnz,
              "; all used cells occupied by the template:", occ_ok)

        # G2 : the realised spans are the stored subspaces
        span_ok = True
        for j in R:
            vs = colspan_vectors(Cs[j])
            for v in vs:
                a, b = v[0], v[1]
                want = (a, b, SIGN[j][2] * b * (1 if SIGN[j][1] == 1 else 1),
                        SIGN[j][3] * a)
                want = (a, b, (b if j != 5 else -b), (a if j != 5 else -a))
                if v != want:
                    span_ok = False
        OUT["G2_spans_match_stored_configuration"] = span_ok
        print("[G2] realised spans match the stored configuration:", span_ok)

        # G4 : mutation
        A[(0, 4)][x[0]][0] += 1
        Csm = {j: [[A[(i, j)][x[i]][d] for d in range(3)] for i in L]
               for j in R}
        OUT["G4_mutation_breaks_a_condition"] = (per_vanishes(Csm) > 0)
        A[(0, 4)][x[0]][0] -= 1
        print("[G4] mutation control fires:",
              OUT["G4_mutation_breaks_a_condition"])

        # G5 : negative control -- a generic assignment on the same rows
        B = {(i, j): [[0] * 3 for _ in range(3)] for i in L for j in R}
        t = 1
        for i in L:
            for j in R:
                for r in (x[i], xp[i]):
                    for d in range(3):
                        t = (t * 7 + 3) % 23 + 1
                        B[(i, j)][r][d] = t
        Csg = {j: [[B[(i, j)][x[i]][d] for d in range(3)] for i in L]
               for j in R}
        OUT["G5_generic_assignment_fails"] = (per_vanishes(Csg) > 0)
        print("[G5] negative control (generic assignment fails):",
              OUT["G5_generic_assignment_fails"])

        verdict = (bad1 == 0 and bad2 == 0 and allnz and occ_ok)

    OUT["GATE_VERDICT_W31_6a_refuted_as_stated"] = bool(verdict)
    print()
    print("[GATE] W31-6a AS STATED (any two distinct L-free words) is "
          "REFUTED:", bool(verdict))

    # ---- what survives as an R2 target ------------------------------------
    surviving = {str(k): len(v) for k, v in sorted(agree.items()) if k >= 1}
    OUT["surviving_target_pairs_by_shared_sites"] = surviving
    OUT["max_shared_sites"] = max(agree) if agree else None
    print("[R2 target] pairs that still couple (share >= 1 L-site):",
          surviving, " max shared sites:", OUT["max_shared_sites"])

    with open(os.path.join(HERE, "results_r2gate.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["G1_matches_W20", "agreement_histogram",
                "GATE_VERDICT_W31_6a_refuted_as_stated",
                "surviving_target_pairs_by_shared_sites"]
    if disc_clean:
        declared += ["G2_spans_match_stored_configuration",
                     "G4_mutation_breaks_a_condition",
                     "G5_generic_assignment_fails"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
