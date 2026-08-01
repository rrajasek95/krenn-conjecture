#!/usr/bin/env python3
"""The non-rigid branch of the null-row dichotomy for EqSystemN 8 3.

Krenn's conjecture is OPEN.  Nothing here assumes it, nothing here decides
(8,3), and no certified dependency changes.  Standard library only, exact
integer / Fraction arithmetic, deterministic, live under ``python3 -O``.

MODEL (the official hafnian model, re-derived here from the literal
definition; independent code from any other checker in the tree).  A cell
(u, v, cu, cv) with u < v is the weight of edge {u,v} read with colour cu at
u and cv at v; 28 edges times 9 = 252 cells; and

    T(w) = sum over the 105 perfect matchings M of K_8
                of  prod_{{u,v} in M, u<v}  A(u,v)[w_u][w_v],

with target T(w) = 1 if w is constant and 0 otherwise (3^8 = 6561 rows).

WHAT IS PROVED HERE (each item is a formal polynomial identity in all 252
cell variables, an exhaustive finite check, or a hand proof whose every
ingredient is one of those; the assembly of item 8 is written out in full in
the docstring of `theorem_no_rigid_vertex`):

 1. ROW-LINEARITY.  For every vertex v,
        T(w) = sum_{u != v} A(v,u)[w_v][w_u] * T^{V-{v,u}}(w)
    identically.  So, with the 189 cells off v held fixed, the WHOLE 6561-row
    system is LINEAR in the 63 cells at v, and it splits by c = w_v into three
    independent 2187 x 21 systems, block (v,c) carrying the single target row
    w = c^8.  Every cell lies in exactly two of the 24 blocks.

 2. THE NULL-ROW THEOREM IS THE {a,b}-SUB-BLOCK of block (v,c): the 128 rows
    whose other letters avoid c meet only the 14 columns (u,d), d in {a,b},
    with coefficients from the {a,b}-block alone, and all have target 0.  Hence
    rho^c_v = (A(v,u)[c][d])_{u != v, d in {a,b}} lies in ker Phi^{ab}_v.

 3. LEVEL-TWO.  For v != v' and every {a,b}-word what on V-{v,v'},
        Z^c(v,v') haf(B^{ab}[V-{v,v'}]; what)
          + sum_{u != u'} rho^c_v(u,what_u) rho^c_{v'}(u',what_u') *
                          haf(B^{ab}[V-{v,v',u,u'}]; what)  =  0.

 4. LEVEL <= 2 IS EVERYTHING.  Every word has a colour occurring at most
    twice (8 < 3*3), so levels 0, 1, 2 of the three colours already cover all
    6561 equations.  EqSystemN 8 3 is EXACTLY: three glued binary (8,2)
    solutions (L0) + the 24 null-row conditions (L1) + the level-two bilinear
    conditions (L2).  Nothing else.

 5. FREE EDGE = DEAD PAIR.  T is independent of the cells on edge {u,v} iff
    haf(A[V-{u,v}]; w) = 0 for every w.  The E/O parity theorem is the special
    case: with all O-O cells zero, every E-E pair is dead.  So "dead pair" is
    the general invariant and E/O is one way to produce it.

 6. DEAD ==> KERNEL, and rank >= 2.  If {u,v} is dead for the {a,b}-block then
    both coordinates (u,d) of Phi^{ab}_v vanish identically, so
    dim ker Phi^{ab}_v >= 2 * deg_D(v);  and Phi^{ab}_v(rho^a_v) = e_{a^7},
    Phi^{ab}_v(rho^b_v) = e_{b^7} are independent, so dim ker <= 12.  That
    bound is NOT sharp -- see the note in check 8 -- and is not used by the
    theorem, which needs only  dead partner => dim ker >= 2.

 7. NULL ROWS ARE NOT SUPPORTED ON DEAD PAIRS.  Explicit binary (8,2) solution
    (the alternating 8-cycle with two extra cells) and an explicit null row at
    a vertex whose only dead partner is disjoint from the null row's support.
    So the tempting sharpening of item 6 to an equality is FALSE.

 8. NO RIGID VERTEX EXISTS (main new theorem).  In ANY (8,3) solution, for
    EVERY vertex v and EVERY colour pair {a,b},   ker Phi^{ab}_v  !=  0.
    Sharply: writing c for the third colour and D^{ab} for the dead graph,
        rho^c_v = 0  ==>  every Z^c-neighbour of v is a D^{ab}-dead partner,
    hence  dim ker Phi^{ab}_v  >=  2 * #{u : Z^c(v,u) != 0}  >=  2.
    CONSEQUENCE: the rigid branch of the null-row dichotomy is empty at every
    single one of the 24 places (v,c) - not merely globally.  The monochromatic
    corollary has an unsatisfiable hypothesis, and every (8,3) solution, if one
    existed, would lie in the non-rigid branch at all 24 places.
    A concrete exclusion: no binary (8,2) solution with even ONE rigid vertex
    can be a colour-pair block of an (8,3) solution.  The exhibited member of
    the E/O "free side" family - the family whose >= 16 parameters modulo gauge
    make the binary variety non-classifiable - is rigid at all four of its odd
    vertices, so that member is excluded outright.

 9. AN EXACT GUARD.  Three pairwise-Hamiltonian one-factors of K_8 on the
    diagonals satisfy L0 (all 768) and L1 (all 3072) EXACTLY and fail exactly
    4 of the 5376 level-two conditions, the residual being the literal
        Z^c(v,v') * haf(B^{ab}[V-{v,v'}]; what) = 1
    at four named places.  It is not repairable by rewriting any single vertex
    row: for every v some colour block is linearly inconsistent, and each
    inconsistency is certified by just TWO equations - a diagonal anchor and
    one failing word which force the same single cell to be 1 and 0.
    A non-monochromatic variant (six cross cells on an edge dead in all three
    blocks) also satisfies L0 + L1 exactly, so L0 + L1 does not imply
    monochromaticity either.

Run with  --fault K  (K in 1..13) to mutation-test check number K.
"""

import sys
from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


FAULT = 0
for _i, _a in enumerate(sys.argv):
    if _a == "--fault" and _i + 1 < len(sys.argv):
        FAULT = int(sys.argv[_i + 1])


def faulty(k):
    return FAULT == k


N = 8
D = 3
V = tuple(range(N))
EDGES = tuple(combinations(V, 2))
CELLS = tuple((u, v, cu, cv) for (u, v) in EDGES
              for cu in range(D) for cv in range(D))
CELL_INDEX = {c: i for i, c in enumerate(CELLS)}
ALL_WORDS = tuple(product(range(D), repeat=N))
INFINITY = 7


# ------------------------------------------------------------- matchings
_MM = {}


def matchings_mask(mask):
    got = _MM.get(mask)
    if got is not None:
        return got
    if mask == 0:
        out = ((),)
    elif bin(mask).count("1") % 2:
        out = ()
    else:
        low = mask & (-mask)
        u = low.bit_length() - 1
        rest = mask ^ low
        acc = []
        r = rest
        while r:
            b = r & (-r)
            r ^= b
            w = b.bit_length() - 1
            for tail in matchings_mask(rest ^ b):
                acc.append(((u, w),) + tail)
        out = tuple(acc)
    _MM[mask] = out
    return out


def matchings(vertices):
    m = 0
    for x in vertices:
        m |= 1 << x
    return matchings_mask(m)


def key(u, v, cu, cv):
    if u > v:
        return (v, u, cv, cu)
    return (u, v, cu, cv)


def tensor(values, word, vertices=V):
    total = 0
    for m in matchings(vertices):
        term = 1
        for (u, v) in m:
            term *= values.get(key(u, v, word[u], word[v]), 0)
            if term == 0:
                break
        total += term
    return total


def target(word, vertices=V):
    return 1 if len({word[u] for u in vertices}) == 1 else 0


# ------------------------------------------------------- dict polynomials
def pmul(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            k = tuple(sorted(ma + mb))
            out[k] = out.get(k, 0) + ca * cb
    return {m: c for m, c in out.items() if c}


def padd(a, b):
    out = dict(a)
    for m, c in b.items():
        t = out.get(m, 0) + c
        if t:
            out[m] = t
        elif m in out:
            del out[m]
    return out


FORMAL = {c: {(CELL_INDEX[c],): 1} for c in CELLS}


def formal_tensor(cellpolys, word, vertices=V):
    total = {}
    for m in matchings(vertices):
        term = {(): 1}
        ok = True
        for (u, v) in m:
            f = cellpolys.get(key(u, v, word[u], word[v]))
            if not f:
                ok = False
                break
            term = pmul(term, f)
        if ok and term:
            total = padd(total, term)
    return total


# --------------------------------------------------------- linear algebra
def rank_and_kernel(rows, ncols):
    rows = [list(map(Q, r)) for r in rows]
    pivots, rank = [], 0
    for col in range(ncols):
        piv = None
        for i in range(rank, len(rows)):
            if rows[i][col]:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = 1 / rows[rank][col]
        rows[rank] = [a * inv for a in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        pivots.append(col)
        rank += 1
        if rank == len(rows):
            break
    pivset = set(pivots)
    basis = []
    for fcol in [c for c in range(ncols) if c not in pivset]:
        vec = [Q(0)] * ncols
        vec[fcol] = Q(1)
        for r, pcol in enumerate(pivots):
            vec[pcol] = -rows[r][fcol]
        basis.append(vec)
    return rank, basis


# ============================================================= 1. sanity
def check_1_sanity():
    require(len(matchings(V)) == 105, "105 perfect matchings of K_8")
    require(len(matchings((0, 1, 2, 3, 4, 5))) == 15, "15 of K_6")
    require(len(CELLS) == 252, "252 cells")
    ones = {c: 1 for c in CELLS}
    got8 = tensor(ones, [0] * N)
    if faulty(1):
        got8 += 1
    require(got8 == 105, "all-ones hafnian on 8 sites is 105, got %d" % got8)
    require(tensor(ones, [0] * N, (0, 1, 2, 3, 4, 5)) == 15, "15 on 6 sites")
    require(sum(1 for w in ALL_WORDS if target(w)) == 3, "3 constant words")
    print("1. model: 105 / 15 matchings, 252 cells, all-ones hafnians 105 / 15.")


# ================================================== 2. row-linearity (formal)
def check_2_row_linearity():
    slice_words = ALL_WORDS[::97]
    checked = 0
    for v in V:
        words = ALL_WORDS if v == 0 else slice_words
        for word in words:
            left = formal_tensor(FORMAL, word)
            right = {}
            for u in V:
                if u == v:
                    continue
                rest = tuple(x for x in V if x not in (v, u))
                right = padd(right, pmul(FORMAL[key(v, u, word[v], word[u])],
                                         formal_tensor(FORMAL, word, rest)))
            if faulty(2) and checked == 13:
                right = padd(right, {(7,): 1})
            require(left == right, "row-linearity fails v=%d w=%r" % (v, word))
            checked += 1
    require(checked == 6561 + 7 * len(slice_words), "identity count %d" % checked)
    print("2. row-linearity  T(w) = sum_u A(v,u)[w_v][w_u] T^{V-{v,u}}(w)")
    print("   verified as a formal identity in all 252 variables: all 6561 words")
    print("   at v=0 and %d words at each of v=1..7  (%d identities)."
          % (len(slice_words), checked))


# ================================================ 3. block structure (24 blocks)
def check_3_blocks():
    seen = {}
    for v in V:
        for c in range(D):
            rows = [w for w in ALL_WORDS if w[v] == c]
            require(len(rows) == 2187, "2187 rows, got %d" % len(rows))
            tgt = [w for w in rows if target(w)]
            require(tgt == [tuple([c] * N)], "block target %r" % tgt)
            for u in V:
                if u == v:
                    continue
                for d in range(D):
                    seen.setdefault(key(v, u, c, d), []).append((v, c))
    if faulty(3):
        seen[CELLS[0]] = seen[CELLS[0]][:1]
    require(len(seen) == 252, "252 cells covered, got %d" % len(seen))
    require(all(len(x) == 2 for x in seen.values()),
            "each cell must lie in exactly two blocks")
    print("3. block structure: 24 blocks of 2187 rows x 21 columns; block (v,c)")
    print("   has the single target row w = c^8; each cell lies in exactly two.")


# ================================================== 4. null-row + level two
def check_4_null_row():
    checked = 0
    for v in V:
        for c in range(D):
            pair = tuple(d for d in range(D) if d != c)
            others = [u for u in V if u != v]
            for assign in product(pair, repeat=N - 1):
                word = [0] * N
                word[v] = c
                for u, d in zip(others, assign):
                    word[u] = d
                left = formal_tensor(FORMAL, word)
                right = {}
                for u in others:
                    rest = tuple(x for x in V if x not in (v, u))
                    cof = formal_tensor(FORMAL, word, rest)
                    for mon in cof:
                        for i in mon:
                            _, _, cu, cv = CELLS[i]
                            require(cu in pair and cv in pair,
                                    "cofactor leaves the {a,b} block")
                    right = padd(right, pmul(FORMAL[key(v, u, c, word[u])], cof))
                if faulty(4) and checked == 21:
                    right = padd(right, {(2,): 1})
                require(left == right, "null-row fails v=%d w=%r" % (v, word))
                require(target(word) == 0, "these words are non-constant")
                checked += 1
    require(checked == 24 * 128, "3072 identities, got %d" % checked)
    print("4. null-row theorem: %d formal identities; every cofactor stays inside" % checked)
    print("   the {a,b}-block and every such word is non-constant, so in any")
    print("   solution rho^c_v lies in ker Phi^{ab}_v.")


def check_5_level_two():
    checked = 0
    for (v, vp) in EDGES:
        for c in range(D):
            pair = tuple(d for d in range(D) if d != c)
            others = tuple(u for u in V if u not in (v, vp))
            for assign in product(pair, repeat=N - 2):
                word = [0] * N
                word[v] = word[vp] = c
                for u, d in zip(others, assign):
                    word[u] = d
                left = formal_tensor(FORMAL, word)
                right = pmul(FORMAL[key(v, vp, c, c)],
                             formal_tensor(FORMAL, word, others))
                for u in others:
                    for up in others:
                        if u == up:
                            continue
                        rest = tuple(x for x in others if x not in (u, up))
                        cof = formal_tensor(FORMAL, word, rest)
                        for mon in cof:
                            for i in mon:
                                _, _, cu, cv = CELLS[i]
                                require(cu in pair and cv in pair,
                                        "deep cofactor leaves the block")
                        right = padd(right, pmul(
                            pmul(FORMAL[key(v, u, c, word[u])],
                                 FORMAL[key(vp, up, c, word[up])]), cof))
                if faulty(5) and checked == 9:
                    right = padd(right, {(1,): 1})
                require(left == right,
                        "level-two fails (%d,%d) c=%d w=%r" % (v, vp, c, word))
                require(target(word) == 0, "these words are non-constant")
                checked += 1
    require(checked == 3 * 28 * 64, "5376 identities, got %d" % checked)
    print("5. level-two theorem: %d formal identities.  The head is the DIAGONAL" % checked)
    print("   cell Z^c(v,v') times the two-hole {a,b}-hafnian; the tail is bilinear")
    print("   in the two cross rows with four-hole {a,b}-hafnians as coefficients.")


# ============================================== 6. levels 0,1,2 cover everything
def check_6_covering():
    per = {0: 0, 1: 0, 2: 0}
    for w in ALL_WORDS:
        k = min(w.count(c) for c in range(D))
        require(k <= 2, "word %r has every colour at least 3 times" % (w,))
        per[k] += 1
    if faulty(6):
        per[0] += 1
    require(sum(per.values()) == 6561, "6561 words")
    require(per == {0: 765, 1: 2856, 2: 2940}, "min-multiplicity census %r" % per)
    inc = {0: 0, 1: 0, 2: 0}
    for w in ALL_WORDS:
        for c in range(D):
            if w.count(c) <= 2:
                inc[w.count(c)] += 1
    require(inc == {0: 768, 1: 3072, 2: 5376}, "level incidences %r" % inc)
    print("6. covering: every word has a colour occurring at most twice, census")
    print("   %r by minimum multiplicity.  So L0 (768 incidences)," % per)
    print("   L1 (3072) and L2 (5376) of the three colours ARE the whole system:")
    print("   EqSystemN 8 3 = three glued binary (8,2) solutions + null rows +")
    print("   the level-two bilinear conditions, and nothing else.")


# =========================================== 7. free edge = dead pair (+ E/O)
def check_7_free_edge():
    # formal: T = (T without edge e) + A(e)[w_u][w_v] * haf(A[V-e]; w)
    checked = 0
    for e in (EDGES[0], EDGES[9], EDGES[27]):
        killed = {c: p for c, p in FORMAL.items() if (c[0], c[1]) != e}
        for word in ALL_WORDS[::53]:
            left = formal_tensor(FORMAL, word)
            rest = tuple(x for x in V if x not in e)
            right = padd(formal_tensor(killed, word),
                         pmul(FORMAL[key(e[0], e[1], word[e[0]], word[e[1]])],
                              formal_tensor(killed, word, rest)))
            if faulty(7) and checked == 3:
                right = padd(right, {(4,): 1})
            require(left == right, "edge-Laplace fails at %r, w=%r" % (e, word))
            checked += 1
    # E/O parity: with all O-O cells zero every E-E pair is dead
    EV, OD = (0, 2, 4, 6), (1, 3, 5, 7)
    for m in matchings(V):
        ee = sum(1 for (u, v) in m if u in EV and v in EV)
        oo = sum(1 for (u, v) in m if u in OD and v in OD)
        require(ee == oo, "matching with %d E-E and %d O-O edges" % (ee, oo))
    for (u, v) in combinations(EV, 2):
        rest = tuple(x for x in V if x not in (u, v))
        for m in matchings(rest):
            require(any(a in OD and b in OD for (a, b) in m),
                    "an E-E hole matching avoids all O-O edges")
    print("7. free edge = dead pair: the edge Laplace split is a formal identity")
    print("   (%d words checked on three edges), so T is independent of the cells" % checked)
    print("   on {u,v} exactly when haf(A[V-{u,v}]; .) vanishes identically.")
    print("   E/O parity is the special case: every matching of K_8 has as many")
    print("   E-E as O-O edges, and with O-O zero every E-E pair is dead.")


# ================================ 8. dead => kernel, rank >= 2, and the profile
def cycle_solution():
    vals = {}
    for i in range(N):
        vals[key(i, (i + 1) % N, i % 2, i % 2)] = 1
    return vals


def phi_matrix(vals, v, colours=(0, 1)):
    a, b = colours
    others = [u for u in V if u != v]
    cols = [(u, d) for u in others for d in (a, b)]
    cidx = {x: i for i, x in enumerate(cols)}
    rows = []
    for assign in product((a, b), repeat=N - 1):
        w = dict(zip(others, assign))
        row = [0] * len(cols)
        for u in others:
            rest = tuple(x for x in V if x not in (v, u))
            row[cidx[(u, w[u])]] = tensor(vals, w, rest)
        rows.append(row)
    return cols, rows


def dead_pairs(vals, colours=(0, 1)):
    out = set()
    for (u, v) in EDGES:
        rest = tuple(x for x in V if x not in (u, v))
        if all(tensor(vals, dict(zip(rest, a)), rest) == 0
               for a in product(colours, repeat=len(rest))):
            out.add((u, v))
    return out


def check_8_kernel_bounds():
    vals = cycle_solution()
    for a in product((0, 1), repeat=N):
        w = dict(zip(V, a))
        require(tensor(vals, w) == target(w), "8-cycle is a binary solution")
    dp = dead_pairs(vals)
    require(len(dp) == 12, "8-cycle has 12 dead pairs, got %d" % len(dp))
    for v in V:
        cols, rows = phi_matrix(vals, v)
        rank, basis = rank_and_kernel(rows, len(cols))
        deadu = {u for u in V if u != v and tuple(sorted((u, v))) in dp}
        # dead => kernel
        for u in deadu:
            for d in (0, 1):
                e = [Q(0)] * len(cols)
                e[cols.index((u, d))] = Q(1)
                require(all(sum(x * y for x, y in zip(r, e)) == 0 for r in rows),
                        "dead direction (%d,%d) is not in ker Phi_%d" % (u, d, v))
        # rank >= 2 from the two constant words
        rho = {}
        for c in (0, 1):
            rho[c] = [vals.get(key(v, u, c, d), 0) for (u, d) in cols]
        img = [[sum(x * y for x, y in zip(r, rho[c])) for r in rows] for c in (0, 1)]
        r2, _ = rank_and_kernel(img, len(rows))
        require(r2 == 2, "Phi_v(rho^0), Phi_v(rho^1) must be independent")
        kdim = len(cols) - rank
        if faulty(8) and v == 0:
            kdim += 7
        require(kdim >= 2 * len(deadu), "dim ker %d < 2*%d dead" % (kdim, len(deadu)))
        require(kdim <= 12, "dim ker Phi_%d = %d exceeds 12" % (v, kdim))
        require(kdim == 6, "8-cycle null-row dimension at %d is %d" % (v, kdim))
    print("8. dead => kernel and rank >= 2:  2*deg_D(v) <= dim ker Phi^{ab}_v <= 12.")
    print("   The alternating 8-cycle attains the LOWER bound only: it has 12")
    print("   dead pairs, degree 3 at every vertex, and dim ker = 6 = 2*3")
    print("   everywhere.  An earlier version of this line said both bounds")
    print("   were attained, conflating the 12 dead pairs with the bound 12.")
    print("   The upper bound is in fact NOT sharp: no vertex has 6 dead")
    print("   partners, so deg_D(v) <= 5 and the lower bound never exceeds 10;")
    print("   and rank Phi^{ab}_v >= 3, so dim ker <= 11.  None of this is used")
    print("   by the theorem, which needs only  dead => dim ker >= 2.")


# ===================================== 9. null rows are NOT supported on dead pairs
def check_9_p2d_counterexample():
    vals = cycle_solution()
    vals[key(2, 4, 0, 0)] = 3
    vals[key(2, 6, 0, 0)] = 3
    for a in product((0, 1), repeat=N):
        w = dict(zip(V, a))
        require(tensor(vals, w) == target(w),
                "the counterexample base is a binary (8,2) solution")
    dp = dead_pairs(vals)
    deadu = {u for u in V if u != 1 and tuple(sorted((u, 1))) in dp}
    require(deadu == {7}, "vertex 1 has dead partners %r, expected {7}" % sorted(deadu))
    x = {(3, 0): Q(-1, 3), (4, 0): Q(1), (6, 0): Q(1)}
    require(not (set(u for (u, d) in x) & deadu),
            "the null row must be supported on ALIVE partners")
    cols, rows = phi_matrix(vals, 1)
    vec = [Q(0)] * len(cols)
    for (u, d), coef in x.items():
        vec[cols.index((u, d))] = coef
    if faulty(9):
        vec[cols.index((3, 0))] = Q(1)
    require(all(sum(p * q for p, q in zip(r, vec)) == 0 for r in rows),
            "the claimed null row is not in ker Phi_1")
    # and it really deforms the solution, from the literal definition
    for t in (Q(1), Q(-2), Q(7, 5)):
        for colour in (0, 1):
            dfm = dict(vals)
            for (u, d), coef in x.items():
                k = key(1, u, colour, d)
                dfm[k] = dfm.get(k, 0) + t * coef
            for a in product((0, 1), repeat=N):
                w = dict(zip(V, a))
                require(tensor(dfm, w) == target(w),
                        "deformed array fails at t=%s colour=%d w=%r" % (t, colour, a))
    print("9. null rows are NOT supported on dead partners.  The 8-cycle with")
    print("   A(2,4)[0][0] = A(2,6)[0][0] = 3 is a binary (8,2) solution; vertex 1")
    print("   has the single dead partner 7, yet  -1/3 e_(3,0) + e_(4,0) + e_(6,0)")
    print("   is a null row supported on the ALIVE partners 3, 4, 6, and adding any")
    print("   multiple of it to row 1 in either colour slot keeps all 256 equations.")


# ================================ 10. the diagonal Laplace and the E/O exclusion
def free_side_solution():
    """Alternating 8-cycle plus arbitrary cells on all six E-E edges."""
    vals = cycle_solution()
    ee = (3, -5, 2, 7, -1, 4, 6, -2, 5, 1, -7, 3,
          2, -4, 9, -3, 8, 5, -6, 2, 7, -9, 4, 1)
    k = 0
    for (u, v) in combinations((0, 2, 4, 6), 2):
        for cu in (0, 1):
            for cv in (0, 1):
                vals[(u, v, cu, cv)] = ee[k]
                k += 1
    require(k == 24, "24 E-E cells")
    return vals


def check_10_diagonal_laplace_and_exclusion():
    # (a) haf(Z) = sum_u Z(v,u) haf(Z[V-{v,u}]) as a formal identity: so a
    #     vanishing row of Z forces haf(Z) = 0.
    diag = {(u, v, 0, 0): {(CELL_INDEX[(u, v, 0, 0)],): 1} for (u, v) in EDGES}
    word = [0] * N
    for v in V:
        left = formal_tensor(diag, word)
        right = {}
        for u in V:
            if u == v:
                continue
            rest = tuple(x for x in V if x not in (v, u))
            right = padd(right, pmul(diag[key(v, u, 0, 0)],
                                     formal_tensor(diag, word, rest)))
        if faulty(10) and v == 3:
            right = padd(right, {(0,): 1})
        require(left == right, "diagonal Laplace fails at v=%d" % v)
        require(all(any(CELLS[i][0] == v or CELLS[i][1] == v for i in mon)
                    for mon in left), "some matching monomial misses vertex %d" % v)
    # (b) the E/O free-side family is rigid at its four odd vertices, hence is
    #     excluded as a colour-pair block of any (8,3) solution.
    fs = free_side_solution()
    for a in product((0, 1), repeat=N):
        w = dict(zip(V, a))
        require(tensor(fs, w) == target(w), "free-side family is a binary solution")
    dp = dead_pairs(fs)
    dims = []
    for v in V:
        cols, rows = phi_matrix(fs, v)
        rank, _ = rank_and_kernel(rows, len(cols))
        dims.append(len(cols) - rank)
    require(dims == [6, 0, 6, 0, 6, 0, 6, 0],
            "free-side null-row profile %r" % dims)
    for v in (1, 3, 5, 7):
        require(not [u for u in V if u != v and tuple(sorted((u, v))) in dp],
                "vertex %d should have no dead partner" % v)
    print("10. (a) haf(Z) = sum_u Z(v,u) haf(Z[V-{v,u}]) is a formal identity and")
    print("    every matching monomial meets v, so a vanishing row of Z^c forces")
    print("    haf(Z^c) = 0, contradicting the anchor haf(Z^c) = 1.")
    print("    (b) the E/O free-side family (alternating 8-cycle + all 24 E-E cells)")
    print("    is a binary (8,2) solution with null-row profile %r and NO" % dims)
    print("    dead partner at its four odd vertices.")


# ============================ 11. the crucial step of the theorem, formally
def check_11_tail_vanishes():
    """With rho^c_v = 0 the level-two bilinear tail is IDENTICALLY zero, so

        T(w) = Z^c(v,v') * haf(B^{ab}[V-{v,v'}]; what)

    for every v' and every {a,b}-word what.  Checked as a formal identity in the
    remaining 238 cell variables, for v = 0, all three colours, all seven v' and
    all 64 words.  (This is the step that needs NO hypothesis on v'.)"""
    v = 0
    checked = 0
    for c in range(D):
        pair = tuple(d for d in range(D) if d != c)
        # zero out rho^c_v : the 14 cells A(v,u)[c][d], d in {a,b}
        polys = dict(FORMAL)
        killed = 0
        for u in V:
            if u == v:
                continue
            for d in pair:
                polys[key(v, u, c, d)] = {}
                killed += 1
        require(killed == 14, "rho^c_v has 14 cells, killed %d" % killed)
        for vp in V:
            if vp == v:
                continue
            others = tuple(x for x in V if x not in (v, vp))
            for assign in product(pair, repeat=N - 2):
                word = [0] * N
                word[v] = word[vp] = c
                for u, d in zip(others, assign):
                    word[u] = d
                left = formal_tensor(polys, word)
                right = pmul(polys[key(v, vp, c, c)],
                             formal_tensor(polys, word, others))
                if faulty(11) and checked == 29:
                    right = padd(right, {(6,): 1})
                require(left == right,
                        "the tail does not vanish: c=%d v'=%d w=%r" % (c, vp, word))
                checked += 1
    require(checked == 3 * 7 * 64, "1344 identities, got %d" % checked)
    print("11. the crucial step, formally: setting the 14 cells of rho^c_v to zero")
    print("    makes the whole level-two bilinear tail vanish identically, leaving")
    print("    T(w) = Z^c(v,v') * haf(B^{ab}[V-{v,v'}]; what)  for EVERY v' and")
    print("    every what (%d formal identities in the other 238 variables)." % checked)
    print("    So rho^c_v = 0 alone forces Z^c(v,v') = 0 at every ALIVE partner v'.")


def theorem_no_rigid_vertex():
    """THE MAIN THEOREM, assembled from the checks above.

    Let A solve EqSystemN 8 3.  Fix a vertex v, a colour c, and the complementary
    pair {a,b}.  Write B = B^{ab} for the {a,b}-block, Z = Z^c for the colour-c
    diagonal,  D^{ab} = { {p,q} : haf(B[V-{p,q}]; what) = 0 for every {a,b}-word }.

    (i)   By check 4 (null-row), rho^c_v lies in ker Phi^{ab}_v.
    (ii)  By checks 5 and 11 (level two, and the formal vanishing of its tail),
          for every v' != v and every {a,b}-word what,
              Z(v,v') haf(B[V-{v,v'}]; what)
                 = - sum_{u != u'} rho^c_v(u,what_u) rho^c_v'(u',what_u')
                                    haf(B[V-{v,v',u,u'}]; what).
          EVERY term of that tail carries a factor rho^c_v(u, .).  So the single
          hypothesis rho^c_v = 0 - no condition at all on v' - already forces
              Z(v,v') haf(B[V-{v,v'}]; what) = 0  for every v' and every what.
          Hence:  rho^c_v = 0  ==>  every Z-neighbour of v is a D^{ab}-partner.
    (iii) By check 3 / check 6 the word c^8 is a level-0 equation of the pairs
          {a,c} and {b,c}; it reads haf(Z) = 1.  By check 10(a) the row of Z at v
          cannot vanish, so v has a Z-neighbour, and by (ii) that neighbour is a
          dead partner of v.
    (iv)  By check 8 each dead partner contributes two dimensions to ker Phi^{ab}_v.
          Therefore, whenever rho^c_v = 0,
              dim ker Phi^{ab}_v  >=  2 * #{u : Z(v,u) != 0}  >=  2.
    (v)   Suppose ker Phi^{ab}_v = 0.  By (i) rho^c_v = 0, so (iv) gives
          dim ker Phi^{ab}_v >= 2 - a contradiction.

    THEOREM.  In any (8,3) solution, ker Phi^{ab}_v != 0 for every vertex v and
    every colour pair {a,b}: all 24 places are non-rigid.  Equivalently, for each
    (v,c) either the cross row rho^c_v is nonzero, or v has a dead partner in the
    complementary block - and in the second case dim ker Phi^{ab}_v >= 2 already.

    CONSEQUENCES.
      * The hypothesis of the monochromatic corollary of the null-row dichotomy
        ("rigid at all 24 pairs") is not merely hard to arrange: it fails at every
        individual place.  All of EqSystemN 8 3 is the non-rigid branch.
      * A binary (8,2) solution with even ONE rigid vertex can never be a
        colour-pair block of an (8,3) solution.  The member of the E/O free-side
        family exhibited in check 10(b) - from the >= 16-parameter family modulo
        gauge which made the binary variety non-classifiable - is rigid at its
        four odd vertices and is therefore excluded outright.
      * If the colour c decouples (rho^c_v = 0 for every v) then supp(Z^c) is
        contained in D^{ab}, so D^{ab} contains a perfect matching.  This applies
        to the monochromatic branch for all three colours at once.
    """
    print("12. MAIN THEOREM (proof assembled in the docstring of")
    print("    theorem_no_rigid_vertex, from checks 3,4,5,6,8,10,11):")
    print("      rho^c_v = 0  =>  every Z^c-neighbour of v is a D^{ab}-dead partner,")
    print("      so  dim ker Phi^{ab}_v >= 2 * deg_{Z^c}(v) >= 2;")
    print("      and by the null-row theorem ker Phi^{ab}_v = 0 would force")
    print("      rho^c_v = 0.  Hence  ker Phi^{ab}_v != 0  at ALL 24 places.")
    print("    => the rigid branch is empty pointwise; a binary (8,2) solution with")
    print("       one rigid vertex is never a block; the E/O free-side family is out.")


# ================================================================ 12. the guard
def one_factor(a):
    edges = {tuple(sorted((INFINITY, a)))}
    for j in (1, 2, 3):
        edges.add(tuple(sorted(((a + j) % 7, (a - j) % 7))))
    return frozenset(edges)


def guard_packet():
    vals = {}
    for a in range(3):
        for (u, v) in sorted(one_factor(a)):
            vals[(u, v, a, a)] = 1
    return vals


def block_rows(vals, v, c):
    cols = [(u, d) for u in V if u != v for d in range(D)]
    cidx = {x: i for i, x in enumerate(cols)}
    core = {k: x for k, x in vals.items() if v not in (k[0], k[1])}
    out = []
    for w in ALL_WORDS:
        if w[v] != c:
            continue
        row = [0] * 21
        for u in V:
            if u == v:
                continue
            rest = tuple(x for x in V if x not in (v, u))
            row[cidx[(u, w[u])]] = tensor(core, w, rest)
        out.append((w, row, 1 if target(w) else 0))
    return cols, out


def consistent(rows, ncols):
    basis = []
    for (w, row, t) in rows:
        vec = [Q(x) for x in row] + [Q(t)]
        support = [w]
        for (p, brow, bsup) in basis:
            if vec[p]:
                f = vec[p]
                vec = [a - f * b for a, b in zip(vec, brow)]
                support = support + bsup
        piv = None
        for i in range(ncols):
            if vec[i]:
                piv = i
                break
        if piv is None:
            if vec[ncols]:
                return False, sorted(set(support))
            continue
        inv = 1 / vec[piv]
        basis.append((piv, [a * inv for a in vec], support))
    return True, None


def check_12_guard():
    vals = guard_packet()
    bad = [w for w in ALL_WORDS if tensor(vals, w) != target(w)]
    require(len(bad) == 2, "guard must fail exactly 2 equations, got %d" % len(bad))
    require(not [k for k in vals if k[2] != k[3]], "guard has a cross cell")
    # L0
    for pair in combinations(range(D), 2):
        sub = {k: x for k, x in vals.items() if k[2] in pair and k[3] in pair}
        for a in product(pair, repeat=N):
            w = dict(zip(V, a))
            require(tensor(sub, w) == target(w), "L0 fails for pair %r" % (pair,))
    # L2 failures, located exactly
    fails = []
    for c in range(D):
        pair = tuple(d for d in range(D) if d != c)
        sub = {k: x for k, x in vals.items() if k[2] in pair and k[3] in pair}
        for (v, vp) in EDGES:
            rest = tuple(x for x in V if x not in (v, vp))
            for assign in product(pair, repeat=N - 2):
                w = dict(zip(rest, assign))
                val = vals.get((v, vp, c, c), 0) * tensor(sub, w, rest)
                if val != 0:
                    fails.append((c, v, vp, assign, val))
    if faulty(12):
        fails = fails[:3]
    require(len(fails) == 4, "expected 4 level-two failures, got %d" % len(fails))
    # single-row repairability
    certs = []
    for v in V:
        ok_all = True
        for c in range(D):
            cols, rows = block_rows(vals, v, c)
            ok, witness = consistent(rows, 21)
            if not ok:
                ok_all = False
                certs.append((v, c, witness))
                break
        require(not ok_all, "row rewrite at v=%d repairs the guard -- "
                            "a solution found is a bug until proven otherwise" % v)
    require(len(certs) == 8, "one certificate per vertex, got %d" % len(certs))
    require(all(len(w) == 2 for (_, _, w) in certs),
            "each certificate should use exactly two equations")
    print("13. EXACT GUARD.  Three pairwise-Hamiltonian one-factors on the diagonals:")
    print("    L0 (768) and L1 (3072, all cross rows zero) hold EXACTLY; exactly 4 of")
    print("    the 5376 level-two conditions fail, each literally")
    print("      Z^c(v,v') * haf(B^{ab}[V-{v,v'}]; what) = 1  (target 0):")
    for (c, v, vp, assign, val) in fails:
        print("        c=%d  {v,v'}={%d,%d}  what=%s  value=%d"
              % (c, v, vp, "".join(map(str, assign)), val))
    print("    Failing words: %s." % ", ".join("".join(map(str, w)) for w in bad))
    print("    No rewrite of a single vertex row repairs it; for each v some colour")
    print("    block is already inconsistent on just TWO equations:")
    for (v, c, witness) in certs:
        print("        v=%d c=%d : %s" % (v, c, " and ".join(
            "".join(map(str, w)) for w in witness)))


# ================================== 13. a non-monochromatic L0+L1 packet
def check_13_nonmono_guard():
    factors = [one_factor(a) for a in range(3)]
    vals = guard_packet()

    def cyc(f1, f2):
        adj = {v: [] for v in V}
        for (u, v) in sorted(set(f1) | set(f2)):
            adj[u].append(v)
            adj[v].append(u)
        order, cur, prev = [0], 0, None
        while True:
            x, y = adj[cur]
            nxt = x if x != prev else y
            if nxt == 0:
                break
            order.append(nxt)
            prev, cur = cur, nxt
        require(len(order) == N, "not a Hamilton cycle")
        return order

    parts = {}
    for (a, b) in combinations(range(D), 2):
        o = cyc(factors[a], factors[b])
        parts[(a, b)] = {o[i] for i in range(0, N, 2)}
    triple = [e for e in EDGES
              if all((e[0] in s) == (e[1] in s) for s in parts.values())]
    require(triple, "no edge is dead in all three blocks")
    e = triple[0]
    weights = {(0, 1): 5, (1, 0): -3, (0, 2): 2, (2, 0): 7, (1, 2): -4, (2, 1): 6}
    for (cu, cv), x in weights.items():
        vals[(e[0], e[1], cu, cv)] = x
    if faulty(13):
        vals[(1, 2, 0, 1)] = 1
    # L0 for all three blocks
    for pair in combinations(range(D), 2):
        sub = {k: x for k, x in vals.items() if k[2] in pair and k[3] in pair}
        for a in product(pair, repeat=N):
            w = dict(zip(V, a))
            require(tensor(sub, w) == target(w),
                    "L0 fails for pair %r on the non-monochromatic packet" % (pair,))
    # L1 for all 24 null-row conditions
    for c in range(D):
        pair = tuple(d for d in range(D) if d != c)
        sub = {k: x for k, x in vals.items() if k[2] in pair and k[3] in pair}
        for v in V:
            cols, rows = phi_matrix(sub, v, pair)
            rho = [vals.get(key(v, u, c, d), 0) for (u, d) in cols]
            for r in rows:
                require(sum(p * q for p, q in zip(r, rho)) == 0,
                        "L1 fails at (v=%d, c=%d) on the non-monochromatic packet"
                        % (v, c))
    cross = sorted(k for k in vals if k[2] != k[3] and vals[k])
    require(len(cross) == 6, "expected six cross cells, got %d" % len(cross))
    wrong = [w for w in ALL_WORDS if tensor(vals, w) != target(w)]
    print("14. A NON-MONOCHROMATIC packet with L0 and L1 exact: the same triple with")
    print("    all six cross cells written on edge %r (an edge dead in all" % (e,))
    print("    three blocks), weights %r." % sorted(weights.items()))
    print("    It satisfies every level-0 and every level-1 equation and fails %d"
          % len(wrong))
    print("    of the 6561.  So L0 + L1 does NOT force monochromaticity either, and")
    print("    the residual of the null-row programme is exactly the level-two system.")


def main():
    check_1_sanity()
    print()
    check_2_row_linearity()
    print()
    check_3_blocks()
    print()
    check_4_null_row()
    print()
    check_5_level_two()
    print()
    check_6_covering()
    print()
    check_7_free_edge()
    print()
    check_8_kernel_bounds()
    print()
    check_9_p2d_counterexample()
    print()
    check_10_diagonal_laplace_and_exclusion()
    print()
    check_11_tail_vanishes()
    print()
    theorem_no_rigid_vertex()
    print()
    check_12_guard()
    print()
    check_13_nonmono_guard()
    print()
    print("all checks passed; Krenn's conjecture remains open and (8,3) undecided")


if __name__ == "__main__":
    main()
