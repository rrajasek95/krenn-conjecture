#!/usr/bin/env python3
"""The two-colour restriction split of EqSystemN 8 3, and the null-row theorem.

Krenn's conjecture is OPEN.  Nothing here assumes it, nothing here decides
(8,3), and no certified dependency changes.  Standard library only, exact
integer / Fraction arithmetic, deterministic, live under ``python -O``.

Model (transcribed from the official EqSystemN, cf.
verify_chart_model_is_official_eqsystem.py): a cell (u, v, cu, cv) with u < v
carries the weight of the edge {u,v} read with colour cu at u and cv at v, and

    T(w) = sum over the 105 perfect matchings M of K_8
                of  prod_{(u,v) in M, u<v}  A(u, v)[w_u][w_v],

with target  T(w) = 1 if w is constant and 0 otherwise.

What is established here, all exactly:

  1. THE SPLIT.  Of the 6561 rows, 3 are monochromatic, 762 use exactly two
     colours and 5796 use all three; 3 + 762 = 765 = 3*2^8 - 3.  A row whose
     word takes values in a colour set S involves ONLY the cells of the
     S-block, and for |S| = 2 all 112 cells of that block occur.  The three
     pair blocks cover all 252 cells and meet pairwise exactly in the three
     monochromatic diagonals Z^0, Z^1, Z^2 (28 cells each).  So the 252
     unknowns are 84 shared (the three diagonals) + 168 private (the six
     cross blocks), and each colour pair sees an EqSystemN 8 2.

  2. THE PAIRWISE SUBSYSTEM IS SATISFIABLE AT EIGHT VERTICES.  Three
     pairwise-Hamiltonian one-factors of K_8 carried on the three diagonals
     solve all 765 at-most-two-colour equations exactly, and fail exactly 2 of
     the 5796 genuinely three-colour ones.  Hence at n = 8, as at n = 6, the
     whole obstruction sits in the three-colour equations: no argument using
     the two-colour restrictions alone can decide (8,3).

  3. THE NULL-ROW THEOREM (the exact compatibility interface).  Fix a vertex
     v, a colour c and the complementary pair {a,b}.  For every word w with
     w_v = c and w_u in {a,b} for u != v, expanding the matching sum along v
     gives the polynomial identity

         T(w) = sum_{u != v} A(v,u)[c][w_u] * T^{V\\{v,u}}(w),

     and the cofactor T^{V\\{v,u}} uses only cells of the {a,b}-block.  All
     those words are non-constant, so for a solution the cross row
         rho^c_v = ( A(v,u)[c][d] )_{u != v, d in {a,b}}   in C^14
     lies in the kernel of the linear map Phi^{ab}_v : C^14 -> (C^2)^{V\\{v}}
     determined by the {a,b}-restriction alone.  Equivalently rho^c_v is a
     direction in which the {a,b}-binary solution can be deformed by changing
     only its vertex-v row.  This is checked here as a formal polynomial
     identity in all 252 cell variables, for all 24 (v,c) and all 3072 words.

     Corollary: if the {a,b}-restriction admits no nonzero null row at v then
     A(v,u)[c][a] = A(v,u)[c][b] = 0 for every u; if that happens for every
     vertex and every colour, the solution is MONOCHROMATIC.

  4. NULL ROWS ARE NOT AUTOMATIC AND NOT ALWAYS PRESENT.  dim ker Phi_v is
     computed exactly for two binary solutions: 6 at every vertex of the
     alternating 8-cycle, but 0 at four of the eight vertices of the (proved)
     family in item 5.

  5. THE BINARY VARIETY IS NOT RIGID.  Split V = E + O into two 4-sets.  Every
     perfect matching of K_8 uses as many E-E edges as O-O edges, so if all
     O-O cells vanish then T does not depend on the E-E cells at all.  Taking
     the alternating 8-cycle for the bipartite part gives a family of binary
     solutions with 24 completely free cells (54 in the three-colour system),
     checked here as a formal polynomial identity.  Its dimension is 30, of
     which the gauge group accounts for 14, so the (8,2) variety has at least
     a 16-parameter family modulo gauge: there is no finite classification of
     the binary restrictions to enumerate.

  6. THE MONOCHROMATIC RESIDUAL.  With all cross cells zero,
     T(w) = prod_c haf(Z^c[V_c]) when every colour class V_c is even, and 0
     otherwise.  Exactly 1641 of the 6561 words have all classes even, so the
     monochromatic branch is haf(Z^c) = 1 for c = 0,1,2 together with 1638
     product equations.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


N = 8
D = 3
V = tuple(range(N))
EDGES = tuple(combinations(V, 2))
CELLS = tuple((u, v, cu, cv) for (u, v) in EDGES
              for cu in range(D) for cv in range(D))
CELL_INDEX = {c: i for i, c in enumerate(CELLS)}
INFINITY = 7


# ---------------------------------------------------------------- matchings
_MATCHINGS = {}


def matchings(vertices):
    vertices = tuple(vertices)
    cached = _MATCHINGS.get(vertices)
    if cached is not None:
        return cached
    if not vertices:
        answer = ((),)
    elif len(vertices) % 2:
        answer = ()
    else:
        head = vertices[0]
        acc = []
        for position in range(1, len(vertices)):
            partner = vertices[position]
            rest = vertices[1:position] + vertices[position + 1:]
            for tail in matchings(rest):
                acc.append(((head, partner),) + tail)
        answer = tuple(acc)
    _MATCHINGS[vertices] = answer
    return answer


PMS = matchings(V)


def cell(u, v, cu, cv):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return (u, v, cu, cv)


def tensor(values, word, vertices=V):
    """T(word) over the induced system on `vertices`; `values` maps cell->number."""
    total = 0
    for matching in matchings(tuple(vertices)):
        term = 1
        for u, v in matching:
            term *= values.get(cell(u, v, word[u], word[v]), 0)
            if term == 0:
                break
        total += term
    return total


def target(word):
    return 1 if len(set(word)) == 1 else 0


ALL_WORDS = tuple(product(range(D), repeat=N))


# --------------------------------------------------- 1. the split, exactly
def audit_split():
    census = {1: 0, 2: 0, 3: 0}
    for word in ALL_WORDS:
        census[len(set(word))] += 1
    require(len(ALL_WORDS) == 6561, "3^8 = 6561 rows")
    require(census == {1: 3, 2: 762, 3: 5796}, "colour-support census %r" % census)
    require(census[1] + census[2] == 765, "765 at-most-two-colour rows")
    require(3 * 2 ** N - 3 * 1 ** N == 765, "inclusion-exclusion 3*2^8-3 = 765")

    def cells_of_row(word):
        used = set()
        for matching in PMS:
            for u, v in matching:
                used.add(cell(u, v, word[u], word[v]))
        return used

    for word in ALL_WORDS:
        support = set(word)
        for (_, _, cu, cv) in cells_of_row(word):
            require(cu in support and cv in support,
                    "row %r reaches outside its colour support" % (word,))

    blocks = {}
    for pair in combinations(range(D), 2):
        pair_set = set(pair)
        rows = [w for w in ALL_WORDS if set(w) <= pair_set]
        require(len(rows) == 256, "256 rows per colour pair")
        used = set()
        for word in rows:
            used |= cells_of_row(word)
        block = {(u, v, cu, cv) for (u, v) in EDGES
                 for cu in pair for cv in pair}
        require(used == block, "pair %r rows use exactly its 112-cell block" % (pair,))
        require(len(block) == 112, "112 cells per pair block")
        blocks[pair] = block

    # the three-way accounting of the 6561 rows
    singleton = [w for w in ALL_WORDS if len(set(w)) == 3
                 and min(w.count(c) for c in set(w)) == 1]
    balanced = [w for w in ALL_WORDS if len(set(w)) == 3
                and min(w.count(c) for c in set(w)) >= 2]
    require(len(singleton) == 2856, "2856 mixed rows with a singleton colour class")
    require(len(balanced) == 2940, "2940 mixed rows with every class of size >= 2")
    require(765 + len(singleton) + len(balanced) == 6561, "the three parts exhaust")

    union = set()
    for block in blocks.values():
        union |= block
    require(union == set(CELLS), "the three pair blocks cover all 252 cells")
    for p, r in combinations(sorted(blocks), 2):
        shared = sorted(set(p) & set(r))
        require(len(shared) == 1, "two pairs share one colour")
        colour = shared[0]
        require(blocks[p] & blocks[r] ==
                {(u, v, colour, colour) for (u, v) in EDGES},
                "pairs %r and %r share exactly the colour-%d diagonal" % (p, r, colour))
    print("1. split: 3 + 762 = 765 at-most-two-colour rows, 5796 genuinely three-colour;")
    print("   pair-S rows use exactly the 112 cells of the S-block; the three blocks")
    print("   cover all 252 cells and meet in the three 28-cell diagonals Z^0,Z^1,Z^2.")
    print("   252 unknowns = 84 shared (diagonals) + 168 private (six cross blocks).")
    print("   Row accounting: 765 pairwise + 2856 with a singleton colour class")
    print("   + 2940 with every class of size >= 2  =  6561.")


# ------------------------------ 2. the pairwise subsystem is satisfiable
def one_factor(a):
    edges = {tuple(sorted((INFINITY, a)))}
    for j in (1, 2, 3):
        edges.add(tuple(sorted(((a + j) % 7, (a - j) % 7))))
    return frozenset(edges)


def audit_pairwise_witness():
    factors = [one_factor(a) for a in range(3)]
    for a in range(3):
        require(len(factors[a]) == 4, "P_%d has four edges" % a)
        covered = sorted(x for e in factors[a] for x in e)
        require(covered == list(V), "P_%d is a perfect matching" % a)
    for a, b in combinations(range(3), 2):
        require(not (factors[a] & factors[b]), "P_%d, P_%d disjoint" % (a, b))
        adjacency = {v: [] for v in V}
        for (u, v) in sorted(factors[a] | factors[b]):
            adjacency[u].append(v)
            adjacency[v].append(u)
        visited, current, previous = [0], 0, None
        while True:
            first, second = adjacency[current]
            nxt = first if first != previous else second
            if nxt == 0:
                break
            visited.append(nxt)
            previous, current = current, nxt
        require(len(visited) == N, "P_%d u P_%d is a Hamilton cycle" % (a, b))

    values = {}
    for a in range(3):
        for (u, v) in sorted(factors[a]):
            values[(u, v, a, a)] = 1

    failures = {2: [], 3: []}
    for word in ALL_WORDS:
        got = tensor(values, word)
        if got != target(word):
            failures[min(len(set(word)), 3) if len(set(word)) == 3 else 2].append(word)
    require(not failures[2], "the 765 pairwise equations are satisfied exactly")
    require(len(failures[3]) == 2, "exactly two three-colour failures, got %d"
            % len(failures[3]))

    union = factors[0] | factors[1] | factors[2]
    require(len(union) == 12, "the union is a cubic graph")
    supported = [m for m in PMS if all(tuple(sorted(e)) in union for e in m)]
    require(len(supported) == 3 + len(failures[3]),
            "#PM of the cubic union = 3 one-factors + #failing rows")
    print("2. three pairwise-Hamiltonian one-factors of K_8 on the diagonals solve all")
    print("   765 two-colour equations EXACTLY and fail exactly %d of the 5796"
          % len(failures[3]))
    print("   three-colour ones (the cubic union has %d perfect matchings)."
          % len(supported))
    print("   failing words:", ["".join(map(str, w)) for w in sorted(failures[3])])
    print("   => the two-colour subsystem carries no obstruction at eight vertices.")

    # local strength of the pairwise conditions there
    rows = []
    for word in ALL_WORDS:
        if len(set(word)) > 2:
            continue
        gradient = [0] * len(CELLS)
        for matching in PMS:
            legs = [CELL_INDEX[cell(u, v, word[u], word[v])] for (u, v) in matching]
            for position, i in enumerate(legs):
                factor = 1
                for other, j in enumerate(legs):
                    if other != position:
                        factor *= values.get(CELLS[j], 0)
                        if factor == 0:
                            break
                if factor:
                    gradient[i] += factor
        if any(gradient):
            rows.append([Q(g) for g in gradient])
    rank = 0
    for column in range(len(CELLS)):
        pivot = None
        for i in range(rank, len(rows)):
            if rows[i][column]:
                pivot = i
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = 1 / rows[rank][column]
        rows[rank] = [a * inverse for a in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                f = rows[i][column]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    require(rank == 157, "pairwise Jacobian rank at the witness is %d" % rank)
    print("   At that witness the 765 pairwise equations have Jacobian rank %d of 252,"
          % rank)
    print("   so they leave a 95-dimensional tangent space (gauge accounts for 9 of it).")

    # and two failures is optimal for this 0/1 monochromatic shape
    factor_sets = [frozenset(tuple(sorted(e)) for e in m) for m in PMS]
    require(len(factor_sets) == 105, "105 one-factors of K_8")

    def hamiltonian(first, second):
        adjacency = {v: [] for v in V}
        for (u, w) in sorted(first | second):
            adjacency[u].append(w)
            adjacency[w].append(u)
        if any(len(adjacency[v]) != 2 for v in V):
            return False
        seen, current, previous = 1, 0, None
        while True:
            x, y = adjacency[current]
            nxt = x if x != previous else y
            if nxt == 0:
                return seen == N
            seen += 1
            previous, current = current, nxt

    neighbours = {}
    for i, j in combinations(range(105), 2):
        if not (factor_sets[i] & factor_sets[j]) and hamiltonian(factor_sets[i],
                                                                 factor_sets[j]):
            neighbours.setdefault(i, set()).add(j)
            neighbours.setdefault(j, set()).add(i)
    census = {}
    triples = 0
    for i in sorted(neighbours):
        for j in sorted(x for x in neighbours[i] if x > i):
            for k in sorted(x for x in (neighbours[i] & neighbours[j]) if x > j):
                union = factor_sets[i] | factor_sets[j] | factor_sets[k]
                if len(union) != 12:
                    continue
                supported = sum(1 for m in factor_sets if all(e in union for e in m))
                census[supported - 3] = census.get(supported - 3, 0) + 1
                triples += 1
    require(triples == 16800, "16800 pairwise-Hamiltonian triples, got %d" % triples)
    require(sorted(census) == [2, 3], "failure census %r" % census)
    require(min(census) == 2, "two failures is the minimum")
    print("   Over ALL %d triples of one-factors of K_8 with pairwise Hamiltonian"
          % triples)
    print("   unions, the number of failing three-colour rows is %r -- so the 0/1"
          % dict(sorted(census.items())))
    print("   monochromatic shape gets within two equations and no closer.")
    return values


# ------------------------------------------------- formal polynomial layer
def poly_mul(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            key = tuple(sorted(ma + mb))
            out[key] = out.get(key, 0) + ca * cb
    return {m: c for m, c in out.items() if c}


def poly_add(a, b):
    out = dict(a)
    for m, c in b.items():
        total = out.get(m, 0) + c
        if total:
            out[m] = total
        elif m in out:
            del out[m]
    return out


def formal_row(cell_polynomials, word, vertices=V):
    total = {}
    for matching in matchings(tuple(vertices)):
        term = {(): 1}
        for u, v in matching:
            factor = cell_polynomials.get(cell(u, v, word[u], word[v]))
            if not factor:
                term = {}
                break
            term = poly_mul(term, factor)
        if term:
            total = poly_add(total, term)
    return total


FORMAL = {c: {(CELL_INDEX[c],): 1} for c in CELLS}


# ------------------------------------------- 3. the null-row theorem
def audit_null_row_identity():
    checked = 0
    for v in V:
        for c in range(D):
            pair = tuple(d for d in range(D) if d != c)
            others = [u for u in V if u != v]
            for assignment in product(pair, repeat=N - 1):
                word = [0] * N
                word[v] = c
                for u, d in zip(others, assignment):
                    word[u] = d
                word = tuple(word)
                left = formal_row(FORMAL, word)
                right = {}
                for u in others:
                    rest = tuple(x for x in V if x not in (v, u))
                    cofactor = formal_row(FORMAL, word, rest)
                    # the cofactor may only touch the {a,b}-block
                    for monomial in cofactor:
                        for i in monomial:
                            _, _, cu, cv = CELLS[i]
                            require(cu in pair and cv in pair,
                                    "cofactor leaves the pair block")
                    head = FORMAL[cell(v, u, c, word[u])]
                    right = poly_add(right, poly_mul(head, cofactor))
                require(left == right,
                        "Laplace expansion along v fails at v=%d word=%r" % (v, word))
                require(target(word) == 0, "these words are all non-constant")
                checked += 1
    require(checked == 24 * 2 ** (N - 1), "24 * 128 = 3072 identities")
    print("3. null-row theorem: all %d identities" % checked)
    print("   T(w) = sum_u A(v,u)[c][w_u] * T^{V-{v,u}}(w) hold as polynomials in the")
    print("   252 cell variables, with every cofactor inside the {a,b}-block, and every")
    print("   such word non-constant.  Hence in ANY solution the cross row rho^c_v is a")
    print("   null row of the {a,b}-binary restriction at v.  Null-row-free at v for all")
    print("   three pairs  =>  every cross cell at v vanishes.")


# ------------------------------- 4. null-row dimensions of binary solutions
def phi_rank(binary_values, v):
    """rank of Phi_v for a binary (colours 0,1) solution; domain has dim 14."""
    others = [u for u in V if u != v]
    columns = [(u, d) for u in others for d in (0, 1)]
    column_index = {col: i for i, col in enumerate(columns)}
    cofactors = {}
    for u in others:
        rest = tuple(x for x in V if x not in (v, u))
        table = {}
        for assignment in product((0, 1), repeat=len(rest)):
            word = dict(zip(rest, assignment))
            table[assignment] = tensor(binary_values, word, rest)
        cofactors[u] = (rest, table)
    rows = []
    for assignment in product((0, 1), repeat=N - 1):
        word = dict(zip(others, assignment))
        row = [Q(0)] * len(columns)
        for u in others:
            rest, table = cofactors[u]
            row[column_index[(u, word[u])]] = Q(table[tuple(word[x] for x in rest)])
        if any(row):
            rows.append(row)
    rank = 0
    for column in range(len(columns)):
        pivot = None
        for i in range(rank, len(rows)):
            if rows[i][column]:
                pivot = i
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = 1 / rows[rank][column]
        rows[rank] = [a * inverse for a in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                f = rows[i][column]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return len(columns) - rank


def alternating_cycle():
    values = {}
    for i in range(N):
        u, v = i, (i + 1) % N
        values[cell(u, v, i % 2, i % 2)] = 1
    return values


def check_binary_solution(values):
    for word in product((0, 1), repeat=N):
        require(tensor(values, word) == target(word),
                "not a binary solution at %r" % (word,))


EVEN = (0, 2, 4, 6)
ODD = (1, 3, 5, 7)
# a fixed, deterministic choice of values on the six E-E pairs
EE_VALUES = (3, -5, 2, 7, -1, 4, 6, -2, 5, 1, -7, 3,
             2, -4, 9, -3, 8, 5, -6, 2, 7, -9, 4, 1)


def cycle_plus_free_side():
    values = dict(alternating_cycle())
    k = 0
    for (u, v) in combinations(EVEN, 2):
        for cu in (0, 1):
            for cv in (0, 1):
                values[(u, v, cu, cv)] = EE_VALUES[k]
                k += 1
    require(k == 24, "24 E-E cells")
    return values


def audit_null_row_dimensions():
    cycle = alternating_cycle()
    check_binary_solution(cycle)
    dims = [phi_rank(cycle, v) for v in V]
    require(dims == [6] * N, "alternating cycle null-row profile %r" % dims)
    free = cycle_plus_free_side()
    check_binary_solution(free)
    dims_free = [phi_rank(free, v) for v in V]
    require(dims_free == [6, 0, 6, 0, 6, 0, 6, 0],
            "free-side family null-row profile %r" % dims_free)
    print("4. dim ker Phi_v (null rows) : alternating 8-cycle %r," % dims)
    print("   8-cycle with a generic free side %r -- so null-row-free" % dims_free)
    print("   vertices do occur, and at those vertices every cross cell must vanish.")


# ------------------------------------------- 5. the free-side family
def audit_free_side_family():
    for matching in PMS:
        inside_even = sum(1 for (u, v) in matching if u in EVEN and v in EVEN)
        inside_odd = sum(1 for (u, v) in matching if u in ODD and v in ODD)
        require(inside_even == inside_odd,
                "a matching with %d E-E and %d O-O edges" % (inside_even, inside_odd))
    # formal check in the three-colour system: 54 E-E cells are free
    cell_polynomials = {}
    free_cells = []
    for (u, v) in EDGES:
        for cu in range(D):
            for cv in range(D):
                if u in ODD and v in ODD:
                    continue
                if u in EVEN and v in EVEN:
                    free_cells.append((u, v, cu, cv))
                    cell_polynomials[(u, v, cu, cv)] = {(CELL_INDEX[(u, v, cu, cv)],): 1}
    require(len(free_cells) == 54, "54 free E-E cells in the three-colour system")
    cycle = alternating_cycle()
    for key, value in cycle.items():
        cell_polynomials[key] = {(): value}
    for word in product((0, 1), repeat=N):
        require(formal_row(cell_polynomials, word) ==
                ({(): 1} if target(word) else {}),
                "free-side family fails at %r" % (word,))
    # the cycle weights are free too, subject to the two product conditions,
    # so the binary family has 6 + 24 = 30 parameters
    weights = [Q(2), Q(3), Q(5), Q(7), Q(11), Q(13),
               Q(1, 2 * 5 * 11), Q(1, 3 * 7 * 13)]
    require(weights[0] * weights[2] * weights[4] * weights[6] == 1, "colour-0 product")
    require(weights[1] * weights[3] * weights[5] * weights[7] == 1, "colour-1 product")
    weighted = {}
    for i in range(N):
        weighted[cell(i, (i + 1) % N, i % 2, i % 2)] = weights[i]
    k = 0
    for (u, v) in combinations(EVEN, 2):
        for cu in (0, 1):
            for cv in (0, 1):
                weighted[(u, v, cu, cv)] = Q(EE_VALUES[k])
                k += 1
    check_binary_solution(weighted)

    # the gauge group  A(u,v)[cu][cv] -> mu_u^{cu} mu_v^{cv} A(u,v)[cu][cv],
    # prod_v mu_v^{(c)} = 1 for each colour, has dimension 2*8 - 2 = 14; its
    # orbit through a generic point of the family has that full dimension.
    binary_cells = [(u, v, cu, cv) for (u, v) in EDGES for cu in (0, 1) for cv in (0, 1)]
    index = {c: i for i, c in enumerate(binary_cells)}
    directions = []
    for colour in (0, 1):
        for site in range(N - 1):
            shift = [[0, 0] for _ in range(N)]
            shift[site][colour] = 1
            shift[N - 1][colour] = -1
            vector = [Q(0)] * len(binary_cells)
            for (u, v, cu, cv) in binary_cells:
                vector[index[(u, v, cu, cv)]] = ((shift[u][cu] + shift[v][cv])
                                                 * weighted.get((u, v, cu, cv), 0))
            directions.append(vector)
    rank = 0
    rows = [r[:] for r in directions]
    for column in range(len(binary_cells)):
        pivot = None
        for i in range(rank, len(rows)):
            if rows[i][column]:
                pivot = i
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = 1 / rows[rank][column]
        rows[rank] = [a * inverse for a in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                f = rows[i][column]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    require(rank == 14, "gauge orbit dimension %d, expected 14" % rank)
    print("5. every perfect matching of K_8 uses equally many E-E and O-O edges, so with")
    print("   the O-O cells zero the tensor is independent of all %d E-E cells."
          % len(free_cells))
    print("   With a weighted alternating 8-cycle as bipartite part this is a binary")
    print("   solution family of dimension 6 + 24 = 30, and the 14-dimensional gauge")
    print("   group acts on it with a %d-dimensional orbit at a generic point." % rank)
    print("   So the (8,2) variety carries at least a 16-parameter family modulo gauge:")
    print("   there is no finite classification of the binary restrictions.")


# ------------------------------------------- 6. the monochromatic residual
def audit_monochromatic_residual():
    even_class_words = [w for w in ALL_WORDS
                        if all(w.count(c) % 2 == 0 for c in range(D))]
    require(len(even_class_words) == 1641, "1641 all-even-class words")
    require(sum(1 for w in even_class_words if len(set(w)) == 1) == 3, "3 constant")
    # the collapse formula, checked on a deterministic dense diagonal packet
    state = 12345
    diagonals = {}
    for c in range(D):
        for (u, v) in EDGES:
            state = (1103515245 * state + 12345) % 2147483648
            diagonals[(u, v, c, c)] = (state >> 16) % 11 - 5
    for word in ALL_WORDS:
        product_form = 1
        for c in range(D):
            klass = tuple(x for x in V if word[x] == c)
            if len(klass) % 2:
                product_form = 0
                break
            product_form *= tensor(diagonals, [c] * N, klass)
        require(tensor(diagonals, word) == product_form,
                "monochromatic collapse fails at %r" % (word,))
    print("6. with every cross cell zero the system collapses to")
    print("   T(w) = prod_c haf(Z^c[V_c]) on the %d words with all classes even"
          % len(even_class_words))
    print("   (0 otherwise), i.e. haf(Z^c) = 1 for c = 0,1,2 plus 1638 product")
    print("   equations.  That is the residual left by the null-row corollary.")


def main():
    audit_split()
    print()
    audit_pairwise_witness()
    print()
    audit_null_row_identity()
    print()
    audit_null_row_dimensions()
    print()
    audit_free_side_family()
    print()
    audit_monochromatic_residual()
    print()
    print("all checks passed; Krenn's conjecture remains open and (8,3) undecided")


if __name__ == "__main__":
    main()
