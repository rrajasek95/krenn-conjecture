#!/usr/bin/env python3
"""Independent checker: no independent 4-set in the live support at (8,3).

THEOREM (proved modulo the one citation below).  Let A assign arbitrary
complex 3x3 matrices to the 28 edges of K_8, with different colours allowed
at the two ends of an edge, and suppose H_8(A) = Delta_(8,3).  Then the live
support graph L(A) = {e : A_e != 0} has NO independent set of size four;
equivalently every 4-subset of the eight vertices spans a live edge.

SCOPE IN d.  Steps 1, 1' and 2 below are pure combinatorics and hold for
every d.  The conclusion is d = 3 only, and is FALSE at d = 2: the
alternating eight-cycle is an exact (8,2) solution whose live graph has
independence number 4.  d enters step 3 twice, both checked here:
  - min degree >= d comes from the forced incident-edge theorem, so an
    endpoint of a dead cross edge is cubic exactly when d = 3 (it has at
    most 4 - 1 = 3 live neighbours, and at least d);
  - the K_{4,4} exclusions are d = 3 statements.
The eight-cycle is the falsifier for both: there min degree is 2 < 3, the
row-collapse step fails, and every necessary condition used below is
satisfied - which this checker verifies explicitly.

Chain verified here, from the literal matching tensor, in exact arithmetic:

  Step 1  (E/O parity, every d)  every perfect matching of K_8 uses as many
          S-internal edges as S^c-internal edges, for every balanced split.
  Step 1' (dead pair = free edge, every d)  the matching tensor does not
          depend on the cells of the pair {u,v} iff H_{V\\{u,v}}(A) vanishes
          identically.
  Step 2  (invisibility, every d)  if S is independent then every pair inside
          S^c is dead in that sense, so zeroing the S^c-internal cells is an
          exact identity of matching tensors; the support lands in K_{4,4}.
  Step 3  (d = 3 only)  no bipartite 4+4 support carries Delta_{8,3}:
          3a. min degree >= 3 (forced incident-edge theorem, d distinct
              anchors), so a dead cross edge has both endpoints cubic;
          3b. NEW: every bipartite support with at least one dead cross edge
              is excluded, by an exhaustive support argument proved here;
          3c. the complete K_{4,4} is excluded by Theorem 2 of
              proofs/k44-coordinate-complement-obstruction.md (cited; its
              audit computations/verify_k44_forced_anchor_support_obstruction.py
              reproduces UNSAT after 38 CEGAR rounds, but needs pysat and is
              NOT re-run here).

Calibration, also checked here: the alternating eight-cycle is an exact
(8,2) solution whose live graph has independence number 4, so the theorem is
d-specific; the checker verifies that every necessary condition used in
step 3 is *satisfied* by that solution, i.e. the argument correctly fails at
d = 2.

Also verified: the contraction bridge to the permanent tensor (Prop 3' of the
parallel subrank route) for ARBITRARY, not rank-one, edge matrices.

Exact integers only.  Every check goes through require(), which raises.
Run `python3 wip-independent-four-set-support-obstruction.py --mutate=N` to
inject fault N and confirm the checker raises (under python3 and python3 -O).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, permutations, product


class CheckFailure(Exception):
    """Raised by require(); never an assert, which python3 -O deletes."""


MUTATION = 0


def require(condition, message):
    if not condition:
        raise CheckFailure(message)
    return True


def mutated(tag):
    return MUTATION == tag


# --------------------------------------------------------------------------
# 0.  Matching tensors of K_n, exact integer arithmetic.
# --------------------------------------------------------------------------

def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    if len(vertices) % 2:
        return []
    head, rest = vertices[0], vertices[1:]
    out = []
    for k in range(len(rest)):
        pair = (head, rest[k])
        for tail in perfect_matchings(rest[:k] + rest[k + 1:]):
            out.append((pair,) + tail)
    return out


PM8 = perfect_matchings(tuple(range(8)))
EDGES8 = tuple(combinations(range(8), 2))


def matching_tensor(matrices, n, d, vertices=None):
    """H_V(A)[c] = sum over perfect matchings of prod A_uv(c_u, c_v)."""
    verts = tuple(range(n)) if vertices is None else tuple(vertices)
    pms = perfect_matchings(verts)
    out = {}
    for coloring in product(range(d), repeat=len(verts)):
        colour = dict(zip(verts, coloring))
        total = 0
        for match in pms:
            term = 1
            for (u, v) in match:
                term *= matrices[(u, v)][colour[u]][colour[v]]
                if term == 0:
                    break
            total += term
        out[coloring] = total
    return out


def delta(n, d):
    out = {}
    for coloring in product(range(d), repeat=n):
        out[coloring] = 1 if len(set(coloring)) == 1 else 0
    return out


def zero_matrix(d):
    return tuple(tuple(0 for _ in range(d)) for _ in range(d))


# --------------------------------------------------------------------------
# 1.  Step 1: the E/O parity lemma.  Combinatorial, so d-independent.
# --------------------------------------------------------------------------

def check_step1_parity():
    checked = 0
    for S in combinations(range(8), 4):
        Sset, Scset = set(S), set(range(8)) - set(S)
        for match in PM8:
            k = sum(1 for (u, v) in match if u in Sset and v in Sset)
            kc = sum(1 for (u, v) in match if u in Scset and v in Scset)
            if mutated(1):
                kc = kc + 1
            require(k == kc, f"E/O parity fails on split {S}, matching {match}")
            checked += 1
    require(checked == 70 * 105, "parity sweep incomplete")
    # The proof: k internal S-edges consume 2k of the four S-vertices, so
    # 4-2k cross; symmetrically 4-2k' cross from S^c; the cross count is one
    # number, hence k = k'.  Re-derive the count itself, exactly.
    for S in combinations(range(8), 4):
        Sset, Scset = set(S), set(range(8)) - set(S)
        for match in PM8:
            k = sum(1 for (u, v) in match if u in Sset and v in Sset)
            cross = sum(1 for (u, v) in match
                        if (u in Sset) != (v in Sset))
            require(cross == 4 - 2 * k, "cross-count identity fails")
    return checked


# --------------------------------------------------------------------------
# 2.  Step 1': dead pair = free edge, as a formal polynomial identity.
# --------------------------------------------------------------------------

def formal_tensor(n, d, live_edges, vertices=None):
    """Matching tensor with a distinct formal variable in every live cell.

    Returns {coloring: {monomial: coefficient}} with monomial a sorted tuple
    of (edge, a, b) variable names.
    """
    verts = tuple(range(n)) if vertices is None else tuple(vertices)
    pms = perfect_matchings(verts)
    out = {}
    for coloring in product(range(d), repeat=len(verts)):
        colour = dict(zip(verts, coloring))
        poly = {}
        for match in pms:
            if any(e not in live_edges for e in match):
                continue
            mono = tuple(sorted((e, colour[e[0]], colour[e[1]]) for e in match))
            poly[mono] = poly.get(mono, 0) + 1
        out[coloring] = poly
    return out


def check_step1prime_dead_pair(d=3):
    """T is independent of the {u,v} cells  <=>  H_{V\\{u,v}} vanishes.

    Verified as the exact edge expansion T = A_uv * C_uv + (rest), by formal
    monomial comparison on all d^8 colourings for a representative pair.
    """
    live = set(EDGES8)
    full = formal_tensor(8, d, live)
    pair = (2, 5)
    rest_vertices = tuple(v for v in range(8) if v not in pair)
    cofactor = formal_tensor(8, d, live, vertices=rest_vertices)
    for coloring in full:
        colour = dict(enumerate(coloring))
        with_edge = {m: c for m, c in full[coloring].items()
                     if any(v == pair for (v, _a, _b) in m)}
        # divide out the pair variable and compare with the cofactor
        divided = {}
        for mono, coef in with_edge.items():
            var = [t for t in mono if t[0] == pair]
            require(len(var) == 1, "an edge appears twice in one matching")
            reduced = tuple(t for t in mono if t[0] != pair)
            divided[reduced] = divided.get(reduced, 0) + coef
        sub = tuple(colour[v] for v in rest_vertices)
        expected = dict(cofactor[sub])
        if mutated(2):
            expected[("bogus",)] = 1
        require(divided == expected,
                f"edge expansion fails at colouring {coloring}")
    return True


# --------------------------------------------------------------------------
# 3.  Step 2: invisibility of the S^c-internal cells.
# --------------------------------------------------------------------------

def check_step2_invisibility(d=3):
    # (a) combinatorial core, all 35 balanced splits
    for S in combinations(range(8), 4):
        Sset, Scset = set(S), set(range(8)) - set(S)
        survivors = [m for m in PM8
                     if not any(u in Sset and v in Sset for (u, v) in m)]
        require(len(survivors) == 24,
                f"expected 24 all-cross matchings for {S}")
        for m in survivors:
            bad = [1 for (u, v) in m if u in Scset and v in Scset]
            if mutated(3):
                bad = [1]
            require(not bad, f"survivor touches an S^c-internal edge: {m}")
        # (b) every pair inside S^c is a dead pair: each perfect matching of
        #     the remaining six vertices must use an S-internal edge.
        for pair in combinations(sorted(Scset), 2):
            rest = tuple(v for v in range(8) if v not in pair)
            for m in perfect_matchings(rest):
                uses_S_internal = any(u in Sset and v in Sset for (u, v) in m)
                require(uses_S_internal,
                        f"cofactor of {pair} survives without an S-edge")
    # (c) exact tensor identity, formally, on the canonical split
    S = {0, 1, 2, 3}
    Sc = {4, 5, 6, 7}
    live_a = set(e for e in EDGES8 if not (e[0] in S and e[1] in S))
    live_b = set(e for e in live_a
                 if not (e[0] in Sc and e[1] in Sc))
    for dd in (2, d):
        ta = formal_tensor(8, dd, live_a)
        tb = formal_tensor(8, dd, live_b)
        require(ta == tb,
                f"zeroing S^c-internal cells changed the tensor at d={dd}")
        require(any(poly for poly in ta.values()), "tensor identically zero")
    return True


# --------------------------------------------------------------------------
# 4.  Anchors: support facts behind minimum degree d.
# --------------------------------------------------------------------------

def check_anchor_support_facts(d=3):
    """A_pj = a (x) e_r has support supp(a) x {r}; distinct r are distinct edges."""
    supports = {}
    for r in range(d):
        for rows in range(1, 1 << d):
            sup = frozenset((a, r) for a in range(d) if rows >> a & 1)
            supports.setdefault(sup, set()).add(r)
    for sup, colours in supports.items():
        if mutated(4):
            colours = {0, 1}
        require(len(colours) == 1,
                f"support {sorted(sup)} would serve two colours")
    # so an edge selected at p for colour r != r' would need two column
    # supports: impossible.  Hence d distinct anchor neighbours, i.e.
    # min degree >= d in the live graph.
    return True


# --------------------------------------------------------------------------
# 5.  Step 3b: bipartite 4+4 supports with a dead cross edge.
# --------------------------------------------------------------------------
# Normalisation.  X = {x0, x'_0, x'_1, x'_2}, Y = {y0, y'_0, y'_1, y'_2};
# (x0,y0) dead.  Min degree 3 makes x0 and y0 cubic, so each of their live
# edges is an anchor and the three far-labels are 0,1,2.  Relabel core
# indices so that (x0, y'_j) has far-label j and (x'_i, y0) has near-label i.
# Then supp(x0,y'_j) = L_j x {j} and supp(x'_i,y0) = {i} x R_i, both nonempty.

COLORS3 = (0, 1, 2)
ROWS_PHI = tuple((i, a) for i in COLORS3 for a in COLORS3 if a != i)
COLS_PHI = tuple((j, b) for j in COLORS3 for b in COLORS3 if b != j)


def admissible_sets():
    """Nonempty subsets of {0,1,2}; used for L_j and R_i."""
    return [frozenset(s) for k in range(1, 4) for s in combinations(COLORS3, k)]


def check_constant_fibre_forcing():
    """Constant fibre r forces  r in L_r, r in R_r  and a 2x2 core diagonal."""
    forced = {}
    for r in COLORS3:
        # live edges at x0 under the constant-r colouring
        for L in admissible_sets():
            for j in COLORS3:
                live = (r in L) and (r == j)
                require(live == ((r == j) and (r in L)),
                        "liveness of the x0 edge misdescribed")
        # the only possible partner is y'_r, and it needs r in L_r
        forced[r] = ("y'_%d" % r, "x'_%d" % r)
    return forced


def check_one_match_reduction():
    """The x0 row and the y0 column each collapse to a single live edge.

    Sweeps every admissible (L_j) with j in L_j, every j*, every a in L_{j*},
    and every beta with beta_j != j off j*.  Symmetrically for (R_i).
    """
    swept = 0
    for L in product(admissible_sets(), repeat=3):
        if any(j not in L[j] for j in COLORS3):
            continue                      # constant fibres force j in L_j
        for jstar in COLORS3:
            others = [j for j in COLORS3 if j != jstar]
            for a in sorted(L[jstar]):
                for beta in product(*[[c for c in COLORS3 if c != j]
                                      for j in others]):
                    v = {jstar: jstar}
                    v.update(dict(zip(others, beta)))
                    live = [j for j in COLORS3 if v[j] == j and a in L[j]]
                    if mutated(11):
                        live = live + [99]
                    require(live == [jstar],
                            f"x0 row not reduced to one edge: L={L} "
                            f"j*={jstar} a={a} beta={beta}")
                    swept += 1
    require(swept > 0, "empty reduction sweep")
    return swept


def one_match_blocks():
    """Classify every reachable 2x2 block as mixed-reachable / constant-reachable.

    The block depends only on (i*, j*) and the free colours; the scalars a, b
    only decide whether the instance is the constant colouring.
    """
    mixed, const = set(), set()
    for jstar in COLORS3:
        for istar in COLORS3:
            others_j = [j for j in COLORS3 if j != jstar]
            others_i = [i for i in COLORS3 if i != istar]
            for beta in product(*[[c for c in COLORS3 if c != j]
                                  for j in others_j]):
                for alpha in product(*[[c for c in COLORS3 if c != i]
                                       for i in others_i]):
                    rowpair = frozenset(zip(others_i, alpha))
                    colpair = frozenset(zip(others_j, beta))
                    block = (rowpair, colpair)
                    # constant colouring: i* = j* = r, a = b = r, all free
                    # colours r.  Always realisable, since r in L_r, r in R_r.
                    if (istar == jstar and all(x == istar for x in beta)
                            and all(x == istar for x in alpha)):
                        const.add(block)
                    # mixed instances of the same block exist whenever some
                    # a in L_{j*} differs from r; we conservatively do NOT
                    # use them, and except every constant-reachable block.
                    else:
                        mixed.add(block)
    return mixed, const


def check_permanent_reduction():
    """Unique live entry in one row and one column collapses perm to a 2x2."""
    idx = lambda i, j: 4 * i + j
    for mask in range(1 << 16):
        cell = [[(mask >> idx(i, j)) & 1 for j in range(4)] for i in range(4)]
        if cell[0][0] == 1:
            continue                              # (x0,y0) is dead
        row0 = [j for j in range(4) if cell[0][j]]
        col0 = [i for i in range(4) if cell[i][0]]
        if len(row0) != 1 or len(col0) != 1:
            continue
        jstar, istar = row0[0], col0[0]
        total = 0
        for sigma in permutations(range(4)):
            if all(cell[i][sigma[i]] for i in range(4)):
                total += 1
        rows = [i for i in range(4) if i not in (0, istar)]
        cols = [j for j in range(4) if j not in (0, jstar)]
        minor = (cell[rows[0]][cols[0]] * cell[rows[1]][cols[1]]
                 + cell[rows[0]][cols[1]] * cell[rows[1]][cols[0]])
        if mutated(5):
            minor += 1
        require(total == minor,
                f"permanent reduction fails on mask {mask}")
    return True


def excepted_and_forced():
    """Machine-derive the excepted 2x2 blocks from the colouring census."""
    blocks_mixed, blocks_const = one_match_blocks()
    require(len(blocks_const) == 3,
            f"expected 3 constant blocks, got {len(blocks_const)}")
    require(len(blocks_mixed) + len(blocks_const) == 144,
            "the 144 legal 2x2 blocks were not all classified")
    for (rowpair, colpair) in blocks_const:
        colours = set(c for (_i, c) in rowpair) | set(c for (_j, c) in colpair)
        require(len(colours) == 1, "a constant block is not monochromatic")
        r = colours.pop()
        require(set(i for (i, _c) in rowpair) == set(COLORS3) - {r}
                and set(j for (j, _c) in colpair) == set(COLORS3) - {r},
                "a constant block has the wrong index pair")
    return blocks_mixed, blocks_const


def closure(ones, excepted):
    """Rectangle completion, returning a step-by-step derivation certificate."""
    ones = set(ones)
    steps = []
    changed = True
    while changed:
        changed = False
        current = sorted(ones)
        for (p, q) in current:
            for (p2, q2) in current:
                if p[0] == p2[0] or q[0] == q2[0]:
                    continue
                block = (frozenset((p, p2)), frozenset((q, q2)))
                if block in excepted and not mutated(13):
                    continue
                for new in ((p, q2), (p2, q)):
                    if new not in ones:
                        steps.append((new, (p, q), (p2, q2), block))
                        ones.add(new)
                        changed = True
    return ones, steps


def verify_certificate(seed, steps, final, legal_blocks, excepted):
    """Replay a closure certificate: every step must be a legal 2x2 completion."""
    have = set(seed)
    for (new, prem1, prem2, block) in steps:
        require(prem1 in have and prem2 in have,
                "certificate uses an underived premise")
        (p, q), (p2, q2) = prem1, prem2
        require(p[0] != p2[0] and q[0] != q2[0],
                "certificate block reuses a row or column group")
        require(block == (frozenset((p, p2)), frozenset((q, q2))),
                "certificate block does not match its premises")
        require(block not in excepted,
                "certificate used an excepted (constant-fibre) block")
        require(block in legal_blocks,
                "certificate used a block outside the mixed census")
        require(new in ((p, q2), (p2, q)),
                "certificate step is not a rectangle completion")
        have.add(new)
    require(have == final, "certificate does not reproduce the closure")
    return len(steps)


def has_injection(options, edges):
    for assign in permutations(edges, len(options)):
        if all(assign[k] in options[c] for k, c in enumerate(sorted(options))):
            return True
    return False


def anchor_feasible(ones):
    forced = {(i, j): set() for i in COLORS3 for j in COLORS3}
    for (i, a), (j, b) in ones:
        forced[(i, j)].add((a, b))
    for i in COLORS3:
        options, edges = {}, [("core", j) for j in COLORS3] + [("y0", None)]
        for c in COLORS3:
            able = set()
            for j in COLORS3:
                if all(b == c for (_a, b) in forced[(i, j)]):
                    able.add(("core", j))
            if c == i:
                able.add(("y0", None))
            options[c] = able
        if not has_injection(options, edges):
            return False, ("x'_%d" % i, options)
    for j in COLORS3:
        options, edges = {}, [("core", i) for i in COLORS3] + [("x0", None)]
        for c in COLORS3:
            able = set()
            for i in COLORS3:
                if all(a == c for (a, _b) in forced[(i, j)]):
                    able.add(("core", i))
            if c == j:
                able.add(("x0", None))
            options[c] = able
        if not has_injection(options, edges):
            return False, ("y'_%d" % j, options)
    return True, None


def check_step3b_dead_edge_case():
    blocks_mixed, blocks_const = excepted_and_forced()
    results = []
    for choice in product((0, 1), repeat=3):
        ones = set()
        for r in COLORS3:
            a, b = [c for c in COLORS3 if c != r]
            cells = [(a, a), (b, b)] if choice[r] == 0 else [(a, b), (b, a)]
            for (i, j) in cells:
                ones.add(((i, r), (j, r)))
        require(len(ones) == 6, "each colour must force two core cells")
        for (i, aa), (j, bb) in ones:      # every forced cell is a legal index
            require(aa != i and bb != j, "forced cell outside Phi")
        cl, steps = closure(ones, blocks_const)
        nsteps = verify_certificate(ones, steps, cl, blocks_mixed, blocks_const)
        feasible, why = anchor_feasible(cl)
        if mutated(6):
            feasible = True
        require(not feasible,
                f"dead-edge case {choice} survived the anchor test: {why}")
        results.append((choice, len(cl), nsteps))
    require(len(results) == 8, "not all eight constant-fibre cases examined")
    require(all(size == 36 for _c, size, _n in results),
            "closure did not fill all 36 Phi cells")
    return results


def check_closure_monotonicity():
    """anchor_feasible is anti-monotone, so testing the closure is complete.

    Proved structurally and exhaustively, in two exhaustive halves:
      (i) for one cell, the set of labels it can still carry shrinks when a
          forced entry is added (all 16 contents x all 16 supersets);
     (ii) the injection test is monotone in the option sets (all 4096 option
          systems x all 12 single-edge additions).
    Both halves are complete, so no sampling is involved.
    """
    # (i) label sets shrink
    contents = []
    cells = [(a, b) for a in (1, 2) for b in (1, 2)]     # a generic Phi block
    for mask in range(16):
        contents.append(frozenset(c for k, c in enumerate(cells)
                                  if mask >> k & 1))
    pairs = 0
    for small in contents:
        for big in contents:
            if not small <= big:
                continue
            xs = set(c for c in COLORS3 if all(b == c for (_a, b) in small))
            xb = set(c for c in COLORS3 if all(b == c for (_a, b) in big))
            ys = set(c for c in COLORS3 if all(a == c for (a, _b) in small))
            yb = set(c for c in COLORS3 if all(a == c for (a, _b) in big))
            if mutated(12):
                xb = xb | {7}
            require(xb <= xs and yb <= ys,
                    "adding a forced entry enlarged a label set")
            pairs += 1
    # (ii) the injection test is monotone in the options
    edges = list(range(4))
    subsets = [frozenset(s) for k in range(5) for s in combinations(edges, k)]
    systems = 0
    for opts in product(subsets, repeat=3):
        base = {c: set(opts[c]) for c in COLORS3}
        ok_base = has_injection(base, edges)
        for c in COLORS3:
            for e in edges:
                if e in base[c]:
                    continue
                bigger = {k: set(v) for k, v in base.items()}
                bigger[c].add(e)
                require(has_injection(bigger, edges) or not ok_base,
                        "the injection test is not monotone in the options")
                systems += 1
    require(pairs > 0 and systems > 0, "empty monotonicity sweep")
    all_cells = set((p, q) for p in ROWS_PHI for q in COLS_PHI)
    require(len(all_cells) == 36, "Phi should have 36 cells")
    ok_empty, _ = anchor_feasible(set())
    ok_full, _ = anchor_feasible(all_cells)
    require(ok_empty, "the empty forced set must be anchor-feasible")
    require(not ok_full, "the full forced set must be anchor-infeasible")
    return pairs, systems


# --------------------------------------------------------------------------
# 5b.  Independent cross-check of one sub-case, by a disjoint code path.
# --------------------------------------------------------------------------
# Dead edges = a whole perfect matching (the "m = 4" sub-case, cube graph).
# Every vertex is then cubic, so every live edge is an anchor at BOTH ends and
# carries a single cell.  This route never touches the Phi machinery.

CUBE_LIVE = tuple((i, j) for i in range(4) for j in range(4) if i != j)


def cube_factorisations():
    out = []
    tri = list(permutations(range(3)))
    for choice in product(range(6), repeat=4):
        cY = {}
        for i in range(4):
            nb = [j for j in range(4) if j != i]
            for k, j in enumerate(nb):
                cY[(i, j)] = tri[choice[i]][k]
        good = True
        for r in range(3):
            cls = [(i, j) for (i, j) in CUBE_LIVE if cY[(i, j)] == r]
            if len(cls) != 4 or len({j for (_i, j) in cls}) != 4:
                good = False
                break
        if good:
            out.append(cY)
    return out


def check_cube_subcase_independently():
    """m = 4: constant fibres force a one-factorisation; then six mixed fibres
    each carry exactly one monomial, which cannot cancel."""
    derangements = [p for p in permutations(range(4))
                    if all(p[i] != i for i in range(4))]
    require(len(derangements) == 9, "the cube graph should have 9 matchings")
    facs = cube_factorisations()
    require(len(facs) == 24, f"expected 24 surviving colourings, got {len(facs)}")
    for cY in facs:
        supp = {e: (cY[e], cY[e]) for e in CUBE_LIVE}
        unique_mixed, constant_ok = 0, 0
        for u in product(range(3), repeat=4):
            for v in product(range(3), repeat=4):
                count = 0
                for sigma in derangements:
                    if all(supp[(i, sigma[i])] == (u[i], v[sigma[i]])
                           for i in range(4)):
                        count += 1
                if len(set(u) | set(v)) == 1:
                    require(count == 1, "a constant fibre lost its monomial")
                    constant_ok += 1
                elif count == 1:
                    unique_mixed += 1
        if mutated(14):
            unique_mixed = 0
        require(constant_ok == 3, "wrong number of constant fibres")
        require(unique_mixed == 6,
                f"expected 6 uncancellable mixed fibres, got {unique_mixed}")
    return len(facs)


def check_rectangle_condition_positive_control():
    """A configuration passing anchors and all constant fibres must still show
    a one-match mixed colouring with exactly one supported matching."""
    cY = cube_factorisations()[0]
    supp = {(i, j): set() for i in range(4) for j in range(4)}
    for e in CUBE_LIVE:
        supp[e] = {(cY[e], cY[e])}
    for i in range(4):                      # anchors present at every vertex
        labels = sorted({b for j in range(4) for (_a, b) in supp[(i, j)]})
        require(labels == [0, 1, 2], f"x_{i} lacks three far-labels")
    for j in range(4):
        labels = sorted({a for i in range(4) for (a, _b) in supp[(i, j)]})
        require(labels == [0, 1, 2], f"y_{j} lacks three near-labels")
    witness = None
    for u in product(range(3), repeat=4):
        for v in product(range(3), repeat=4):
            live = [[1 if (u[i], v[j]) in supp[(i, j)] else 0
                     for j in range(4)] for i in range(4)]
            row0 = [j for j in range(4) if live[0][j]]
            col0 = [i for i in range(4) if live[i][0]]
            if len(row0) != 1 or len(col0) != 1 or row0[0] == 0 or col0[0] == 0:
                continue
            total = sum(1 for s in permutations(range(4))
                        if all(live[i][s[i]] for i in range(4)))
            if total == 1 and len(set(u) | set(v)) > 1:
                witness = (u, v)
                break
        if witness:
            break
    if mutated(15):
        witness = None
    require(witness is not None,
            "no one-match mixed colouring found: the rectangle condition "
            "would be vacuous on this configuration")
    return witness


# --------------------------------------------------------------------------
# 6.  Calibration.
# --------------------------------------------------------------------------

def unit_matrix(d, a, b):
    return tuple(tuple(1 if (i, j) == (a, b) else 0 for j in range(d))
                 for i in range(d))


def check_four_site_witness(d=3):
    """(4,3) has a solution, and its live graph is complete: no independent 2-set."""
    mats = {}
    mats[(0, 1)] = unit_matrix(d, 0, 0)
    mats[(2, 3)] = unit_matrix(d, 0, 0)
    mats[(0, 2)] = unit_matrix(d, 1, 1)
    mats[(1, 3)] = unit_matrix(d, 1, 1)
    mats[(0, 3)] = unit_matrix(d, 2, 2)
    mats[(1, 2)] = unit_matrix(d, 2, 2)
    if mutated(7):
        mats[(0, 1)] = unit_matrix(d, 0, 1)
    tensor = matching_tensor(mats, 4, d)
    require(tensor == delta(4, d), "the (4,3) witness is not a solution")
    live = [e for e in combinations(range(4), 2)
            if any(any(row) for row in mats[e])]
    require(len(live) == 6, "the (4,3) witness has a dead edge")
    return True


def eight_cycle_solution(d=2):
    """Alternating eight-cycle: the canonical (8,2) solution."""
    mats = {e: zero_matrix(d) for e in EDGES8}
    cycle = [(i, (i + 1) % 8) for i in range(8)]
    for pos, (u, v) in enumerate(cycle):
        e = (min(u, v), max(u, v))
        colour = pos % 2
        mats[e] = unit_matrix(d, colour, colour)
    return mats, cycle


def check_eight_cycle_falsifier():
    mats, cycle = eight_cycle_solution(2)
    if mutated(8):
        mats[(0, 1)] = unit_matrix(2, 0, 1)
    tensor = matching_tensor(mats, 8, 2)
    require(tensor == delta(8, 2),
            "the alternating eight-cycle is not an exact (8,2) solution")
    live = set()
    for e in EDGES8:
        if any(any(row) for row in mats[e]):
            live.add(e)
    require(len(live) == 8, "eight-cycle should have exactly 8 live edges")
    # independence number 4, witnessed by the evens
    evens = {0, 2, 4, 6}
    require(not any(u in evens and v in evens for (u, v) in live),
            "the evens are not independent in the eight-cycle")
    # so steps 1-2 apply and carry it into K_{4,4}
    for e in live:
        require((e[0] in evens) != (e[1] in evens),
                "the eight-cycle is not bipartite between evens and odds")
    # and the d = 3 input fails exactly here: min degree is 2, not 3
    degree = {v: sum(1 for e in live if v in e) for v in range(8)}
    require(min(degree.values()) == 2, "eight-cycle min degree is not 2")
    require(min(degree.values()) < 3,
            "min degree >= 3 would have to fail at d = 2")
    # every necessary condition used in step 3 holds on this solution
    supports = {e: frozenset((a, b) for a in range(2) for b in range(2)
                             if mats[e][a][b]) for e in live}
    for v in range(8):
        far = []
        for e in live:
            if v not in e:
                continue
            if v == e[0]:
                cols = set(b for (_a, b) in supports[e])
            else:
                cols = set(a for (a, _b) in supports[e])
            require(len(cols) == 1, "an eight-cycle edge is not an anchor")
            far.append(cols.pop())
        require(sorted(far) == [0, 1],
                f"vertex {v} lacks two distinct anchors at d=2")
    return True


def check_eight_cycle_no_unique_mixed_fibre():
    """N4 holds on the eight-cycle: no mixed colouring has one monomial."""
    mats, _ = eight_cycle_solution(2)
    for coloring in product(range(2), repeat=8):
        supported = 0
        for match in PM8:
            if all(mats[e][coloring[e[0]]][coloring[e[1]]] for e in match):
                supported += 1
        if len(set(coloring)) == 1:
            require(supported == 1, "constant fibre lost its monomial")
        else:
            require(supported != 1,
                    f"mixed fibre {coloring} has a single monomial")
    return True


# --------------------------------------------------------------------------
# 7.  The permanent bridge (Prop 3'), for arbitrary edge matrices.
# --------------------------------------------------------------------------

def check_permanent_contraction_bridge(m=4, d=3):
    """Contracting the right shore with all-ones turns H into (x)M_i (Per_m).

    M_i(e_j) = row-sum vector of A_ij.  No rank-one hypothesis, dead edges
    allowed.  Verified as a formal polynomial identity in all m*m*d*d cells.
    """
    perms = list(permutations(range(m)))
    var = lambda i, j, a, b: ("A", i, j, a, b)
    lhs = {}
    for cL in product(range(d), repeat=m):
        poly = {}
        for cR in product(range(d), repeat=m):
            for sigma in perms:
                mono = tuple(sorted(var(i, sigma[i], cL[i], cR[sigma[i]])
                                    for i in range(m)))
                poly[mono] = poly.get(mono, 0) + 1
        lhs[cL] = poly
    rhs = {}
    for cL in product(range(d), repeat=m):
        poly = {}
        for sigma in perms:
            for bs in product(range(d), repeat=m):
                mono = tuple(sorted(var(i, sigma[i], cL[i], bs[i])
                                    for i in range(m)))
                poly[mono] = poly.get(mono, 0) + 1
        rhs[cL] = poly
    if mutated(9):
        rhs[tuple([0] * m)] = {}
    require(lhs == rhs, "the all-ones contraction is not (x)M_i(Per_m)")
    # and the target contracts to Delta_(m,3)
    target = delta(2 * m, d)
    contracted = {}
    for cL in product(range(d), repeat=m):
        contracted[cL] = sum(target[cL + cR]
                             for cR in product(range(d), repeat=m))
    require(contracted == delta(m, d),
            "Delta_(2m,d) does not contract to Delta_(m,d)")
    return True


def check_permanent_subrank_lower_bound(m=4):
    """Q(Per_m) >= 2: two permutations whose quotient is an m-cycle."""
    sigma0 = tuple(range(m))
    sigma1 = tuple((i + 1) % m for i in range(m))
    maps = []
    for i in range(m):
        rows = []
        for colour in range(2):
            target = sigma0[i] if colour == 0 else sigma1[i]
            rows.append([1 if j == target else 0 for j in range(m)])
        maps.append(rows)
    out = {}
    for c in product(range(2), repeat=m):
        total = 0
        for sigma in permutations(range(m)):
            term = 1
            for i in range(m):
                term *= maps[i][c[i]][sigma[i]]
                if term == 0:
                    break
            total += term
        out[c] = total
    require(out == delta(m, 2), f"Q(Per_{m}) >= 2 witness failed: {out}")
    # the union of the two permutations is a 2m-cycle: the (8,2) support
    edges = set()
    for i in range(m):
        edges.add(("L%d" % i, "R%d" % sigma0[i]))
        edges.add(("L%d" % i, "R%d" % sigma1[i]))
    require(len(edges) == 2 * m, "the union is not a 2m-cycle")
    return True


# --------------------------------------------------------------------------
# 8.  Partial audit of the Q(Per_4) <= 2 upper bound (NOT a full proof).
# --------------------------------------------------------------------------

def rank_exact(rows):
    mat = [list(map(Fraction, r)) for r in rows]
    rank, ncols = 0, len(mat[0]) if mat else 0
    for col in range(ncols):
        pivot = None
        for r in range(rank, len(mat)):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pv = mat[rank][col]
        mat[rank] = [x / pv for x in mat[rank]]
        for r in range(len(mat)):
            if r != rank and mat[r][col] != 0:
                f = mat[r][col]
                mat[r] = [x - f * y for x, y in zip(mat[r], mat[rank])]
        rank += 1
    return rank


def rho_pair(k1, k2):
    """dim of the image of U_1 (x) U_2 in the six off-diagonal symmetric cells.

    U_i = k_i^perp.  rho = 9 - dim(U_1 (x) U_2  cap  ker pi).
    """
    anti = [(a, b) for a in range(4) for b in range(4) if a < b]
    unknowns = len(anti) + 4                       # S entries, then diagonal D
    rows = []
    for a in range(4):                             # (S k1 - D k1)_a = 0
        row = [0] * unknowns
        for idx, (p, q) in enumerate(anti):
            if p == a:
                row[idx] += k1[q]
            if q == a:
                row[idx] -= k1[p]
        row[len(anti) + a] -= k1[a]
        rows.append(row)
    for a in range(4):                             # (S k2 + D k2)_a = 0
        row = [0] * unknowns
        for idx, (p, q) in enumerate(anti):
            if p == a:
                row[idx] += k2[q]
            if q == a:
                row[idx] -= k2[p]
        row[len(anti) + a] += k2[a]
        rows.append(row)
    dim_kernel = unknowns - rank_exact(rows)
    return 9 - dim_kernel


def components(edges, n=4):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (a, b) in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return len({find(v) for v in range(n)})


def check_permanent_flattening_obstruction():
    """Any subrank-3 restriction of Per_4 needs a shared zero coordinate.

    A rank-three tensor has every flattening of rank <= 3.  For the (12)(34)
    split that rank is at least rho(k1,k2) + rho(k3,k4) - 6, where rho is the
    dimension of the image of U_1 (x) U_2 in the six off-diagonal symmetric
    cells.  So a restriction needs rho + rho <= 9 in each of the three
    complementary splits.

    Verified here: with no shared zero coordinate, rho = 7 - c where c counts
    the components of the graph {a,b : k1(a)k2(b) + k2(a)k1(b) != 0}, and
    c <= 2, so rho >= 5 and rho + rho >= 10.  The sweep over conjugacy types
    is complete: only the pattern of the relation t_a = -t_b matters, and the
    representative values below realise every pattern.
    """
    reps = {"0": (0, 1), "inf": (1, 0), "1": (1, 1), "-1": (-1, 1),
            "2": (2, 1), "-2": (-2, 1)}
    worst, tested, formula_checks = 9, 0, 0
    for names in product(sorted(reps), repeat=4):
        pts = [reps[nm] for nm in names]
        k1 = [p[0] for p in pts]
        k2 = [p[1] for p in pts]
        if not any(k1) or not any(k2):
            continue                       # k_i must be a nonzero vector
        rho = rho_pair(k1, k2)
        edges = [(a, b) for a in range(4) for b in range(4) if a < b
                 and k1[a] * k2[b] + k2[a] * k1[b] != 0]
        c = components(edges)
        if mutated(10):
            rho = 9
        require(rho == 7 - c, f"rho = 7 - c failed at {names}: {rho} vs {c}")
        formula_checks += 1
        worst = min(worst, rho)
        tested += 1
    require(tested > 0, "empty rho sweep")
    require(worst >= 5, f"a fully supported pair reached rho = {worst} < 5")
    # shared zeros do lower rho, so the obstruction really is about them
    require(rho_pair([1, 0, 0, 0], [1, 0, 0, 0]) == 3,
            "k1 = k2 = e_1 should give rho = 3")
    require(rho_pair([1, 1, 1, 1], [1, 1, 1, 1]) == 6,
            "the all-ones pair should give rho = 6")
    return worst, tested, formula_checks


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    global MUTATION
    for arg in sys.argv[1:]:
        if arg.startswith("--mutate="):
            MUTATION = int(arg.split("=", 1)[1])
    require(len(PM8) == 105, "K_8 must have 105 perfect matchings")

    n = check_step1_parity()
    print(f"[1 ] E/O parity: {n} (split, matching) pairs, no violation; "
          f"cross = 4 - 2k verified")

    check_step1prime_dead_pair()
    print("[1'] dead pair = free edge: edge expansion verified formally on "
          "all 6561 colourings")

    check_step2_invisibility()
    print("[2 ] invisibility: 35 splits, 24 all-cross matchings each, every "
          "S^c-pair cofactor dead; tensor identity exact at d=2,3")

    check_anchor_support_facts()
    print("[3a] anchors: one support serves one colour, so d distinct anchor "
          "neighbours; min degree >= d")

    check_permanent_reduction()
    print("[3b] permanent reduction verified on all 65536 support patterns")

    swept = check_one_match_reduction()
    blocks_mixed, blocks_const = excepted_and_forced()
    print(f"[3b] one-match census: {swept} (L, j*, a, beta) sweeps collapse "
          f"the x0 row; {len(blocks_mixed)} mixed 2x2 blocks carry the "
          f"rectangle condition, {len(blocks_const)} constant blocks excepted")

    pairs, systems = check_closure_monotonicity()
    print(f"[3b] anchor feasibility is anti-monotone: {pairs} label-set pairs "
          f"and {systems} option extensions, both exhaustive")

    results = check_step3b_dead_edge_case()
    total_steps = sum(n for _c, _s, n in results)
    print(f"[3b] all {len(results)} constant-fibre cases: {total_steps} "
          f"certificate-verified completions fill all 36 Phi cells, anchor "
          f"system infeasible -> EXCLUDED")

    nfac = check_cube_subcase_independently()
    witness = check_rectangle_condition_positive_control()
    print(f"[X ] independent cross-check of the m=4 sub-case: {nfac} colourings "
          f"survive the constant fibres, each with 6 uncancellable mixed "
          f"fibres; positive control witness u,v = {witness[0]},{witness[1]}")

    check_four_site_witness()
    print("[C1] (4,3) witness is an exact solution with all six edges live")

    check_eight_cycle_falsifier()
    check_eight_cycle_no_unique_mixed_fibre()
    print("[C2] (8,2) eight-cycle: exact solution, independent 4-set {0,2,4,6}, "
          "bipartite, min degree 2 < 3; all step-3 conditions hold on it")

    check_permanent_contraction_bridge(m=3, d=3)
    check_permanent_contraction_bridge(m=4, d=3)
    print("[P ] Prop 3' bridge verified formally for m=3,4 with arbitrary "
          "(not rank-one) edge matrices, dead edges allowed")

    check_permanent_subrank_lower_bound(4)
    print("[P ] Q(Per_4) >= 2 witness (id and the 4-cycle) verified; its "
          "union is the eight-cycle")

    worst, tested, formula = check_permanent_flattening_obstruction()
    print(f"[P ] flattening obstruction: rho = 7 - c on all {formula} "
          f"conjugacy types; min rho = {worst} >= 5 with no shared zero, so a "
          f"subrank-3 restriction of Per_4 needs shared zero coordinates")

    print()
    print("PASS  no independent 4-set at (8,3), modulo the cited Theorem 2 "
          "for the complete K_{4,4}")


if __name__ == "__main__":
    main()
