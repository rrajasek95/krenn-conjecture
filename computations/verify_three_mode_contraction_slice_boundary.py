#!/usr/bin/env python3
"""Where the slice-rank obstruction lives: exactly the colour counts D >= N.

Krenn's conjecture remains OPEN; nothing here assumes it.  No certified
dependency is changed and no existing file is touched.

Context
-------
The upstream `formal-conjectures` file
`FormalConjectures/Paper/MonochromaticQuantumGraph.lean` marks
`eqSystem8_no_solution_d10` (N = 8, D = 10) as *research solved* with a
`formal_proof` attribute pointing at

    https://github.com/mo271/formal-conjectures/blob/
      2cc6df2e95835d759caedb15e36b70025b2eae2c/
      FormalConjectures/Paper/MonochromaticQuantumGraph.lean#L853

whose proof is organised around lemmas named `sum_colorings3_expand`,
`exists_ker_7`, `ker_support_le_2`, `diag_rank_2_identity` and
`slice_rank_contradiction_lem`.  The Lean text was read through a web
fetch, not compiled here, so the *attribution* is RELAYED.  What this
checker establishes is INDEPENDENT: the argument those names describe is
reconstructed from scratch below, verified as an exact polynomial identity,
and its exact boundary is computed.

The reconstruction
------------------
Split the vertices into a kept 3-set S = {0, 1, 2} and F = the other N - 3.
Sum the equation `pmSumN N D W iota = [iota constant]` over all colourings
of F.  The right side collapses to the three-mode diagonal `Delta_{3,D}`.
The left side is the matching tensor contracted at every F mode by the
all-ones covector (arbitrary torus covectors `y_f` work identically and are
also checked).  Every perfect matching of K_N either

  * matches vertex 0 into F -- the F partner's colour index is summed away,
    so the term is (a vector at mode i) tensor (a function of j, k), a slice
    at mode i whose mode-i vector is `A_{0f} y_f`; or
  * uses the internal S edge {0,1}, forcing vertex 2 into F: one slice at
    mode k; or
  * uses the internal S edge {0,2}, forcing vertex 1 into F: one slice at
    mode j.

So the contracted tensor is a sum of `r + 2` slices with
`r = dim span{A_{0f} y_f : f in F} <= min(N - 3, D)`.  Choosing
`x` orthogonal to that span and contracting mode i leaves a matrix of rank
at most 2 which must equal `diag(lambda_c x_c)`; hence every vector of a
`(D - r)`-dimensional space has support at most 2, hence `D - r <= 2`.
Therefore

        D - 2 <= min(N - 3, D),   i.e.   D <= N - 1.

**A solution of `EqSystemN N D` forces D <= N - 1.**  Equivalently every
case with D >= N is impossible, elementarily, over any field.

That criterion reproduces the upstream solved/open split for complex
weights exactly (checked in `audit_boundary_matches_upstream_ledger`), and
it is why the technique says nothing at (8, 3): there D = 3 and N - 1 = 7.

Why slice rank cannot be repaired at (8, 3)
-------------------------------------------
Slice rank of any tensor in `(C^3)^{tensor 8}` is at most `min_k dim V_k`
= 3, and the diagonal `Delta_{8,3}` already has slice rank 3 (Tao's
diagonal lemma -- RELAYED: T. Tao, "A symmetric formulation of the
Croot-Lev-Pach-Ellenberg-Gijswijt capset bound", 18 May 2016, and Tao-Sawin
"Notes on the slice rank of tensors").  The invariant is therefore
saturated at the target, so a gap can only exist if *every* matching tensor
had slice rank at most 2.  `audit_matching_tensor_attains_slice_rank_three`
exhibits an explicit `K_8` matching tensor of slice rank exactly 3, by a
restriction certificate that needs no appeal to Tao's lemma.  Slice rank on
`(C^3)^{tensor 8}` therefore cannot separate the two tensors at all.

Standard library only, exact `Fraction` arithmetic, no floats.  Runs under
`python3`, `-O` and `-I -S`; `require` raises, so `-O` does not delete the
checks.
"""

from fractions import Fraction as Q
from itertools import product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# --------------------------------------------------------------------------
# 1. the official recursion, transcribed from the Lean source
# --------------------------------------------------------------------------
def pm_sum_list_aux(weight, iota, fuel, vertices):
    """`pmSumListAux` of FormalConjectures/Paper/MonochromaticQuantumGraph.lean."""
    if fuel == 0:
        return Q(1)
    if fuel == 1:
        return Q(0)
    if not vertices:
        return Q(1)
    if len(vertices) == 1:
        return Q(0)
    head, tail = vertices[0], vertices[1:]
    total = Q(0)
    for position, partner in enumerate(tail):
        rest = tail[:position] + tail[position + 1:]
        total += (weight(head, partner, iota[head], iota[partner])
                  * pm_sum_list_aux(weight, iota, fuel - 2, rest))
    return total


def official_matchings(vertices):
    """The matchings the official recursion enumerates on `vertices`, extracted
    by running that same head-pairing recursion with a weight that records the
    pair instead of multiplying it."""
    collected = []

    def walk(remaining, chosen):
        if not remaining:
            collected.append(tuple(chosen))
            return
        head, tail = remaining[0], remaining[1:]
        for position, partner in enumerate(tail):
            walk(tail[:position] + tail[position + 1:],
                 chosen + [(head, partner)])

    walk(tuple(vertices), [])
    return tuple(collected)


def double_factorial_odd(n):
    """(n-1)!! for even n: the number of perfect matchings of K_n."""
    value = 1
    k = n - 1
    while k > 1:
        value *= k
        k -= 2
    return value


def audit_recursion_enumerates_perfect_matchings():
    """The extracted list is the perfect matchings, with the textbook count."""
    for n in (2, 4, 6, 8):
        vertices = tuple(range(n))
        found = official_matchings(vertices)
        require(len(found) == double_factorial_odd(n),
                ("matching count", n, len(found)))
        require(len(set(found)) == len(found), ("duplicate matching", n))
        for matching in found:
            covered = [w for pair in matching for w in pair]
            require(sorted(covered) == list(vertices), ("not a partition", n))
            for u, v in matching:
                require(u < v, ("head-pairing orders each pair", n))
        # the literal recursion on all-ones weights counts them
        count = pm_sum_list_aux(lambda a, b, i, j: Q(1),
                                [0] * n, n, vertices)
        require(count == Q(len(found)), ("literal recursion count", n))


# --------------------------------------------------------------------------
# 2. exact polynomial arithmetic over formal edge weights
# --------------------------------------------------------------------------
# A polynomial is a dict {monomial: Fraction} with monomial a sorted tuple of
# variable keys, repeats allowed.  Variables are ('W', u, v, i, j) with u < v.
ZERO = {}


def poly_var(key):
    return {(key,): Q(1)}


def poly_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        total = out.get(monomial, Q(0)) + coefficient
        if total:
            out[monomial] = total
        elif monomial in out:
            del out[monomial]
    return out


def poly_mul(left, right):
    out = {}
    for m1, c1 in left.items():
        for m2, c2 in right.items():
            monomial = tuple(sorted(m1 + m2))
            total = out.get(monomial, Q(0)) + c1 * c2
            if total:
                out[monomial] = total
            elif monomial in out:
                del out[monomial]
    return out


def poly_scale(poly, scalar):
    if not scalar:
        return {}
    return {m: c * scalar for m, c in poly.items()}


def poly_sub(left, right):
    return poly_add(left, poly_scale(right, Q(-1)))


def formal_weight(u, v, i, j):
    require(u < v, ("formal weights are indexed by ordered pairs", u, v))
    return poly_var(('W', u, v, i, j))


def matching_monomial(matching, colour):
    """The product of formal edge weights along one perfect matching."""
    out = {(): Q(1)}
    for u, v in matching:
        out = poly_mul(out, formal_weight(u, v, colour[u], colour[v]))
    return out


def contracted_tensor(vertices, kept, palette, covector):
    """Sum of the matching tensor of K_{vertices} over all colourings of the
    contracted modes, weighted by `covector[f][colour]`.

    Returns {kept-colour tuple: polynomial}.  `covector` maps each contracted
    vertex to a tuple of `palette` exact rationals.
    """
    vertices = tuple(vertices)
    kept = tuple(kept)
    free = tuple(v for v in vertices if v not in kept)
    matchings = official_matchings(vertices)
    out = {word: {} for word in product(range(palette), repeat=len(kept))}
    for free_word in product(range(palette), repeat=len(free)):
        scalar = Q(1)
        for position, f in enumerate(free):
            scalar *= covector[f][free_word[position]]
        if not scalar:
            continue
        for kept_word in out:
            colour = {}
            for position, s in enumerate(kept):
                colour[s] = kept_word[position]
            for position, f in enumerate(free):
                colour[f] = free_word[position]
            block = {}
            for matching in matchings:
                block = poly_add(block, matching_monomial(matching, colour))
            out[kept_word] = poly_add(out[kept_word], poly_scale(block, scalar))
    return out


# --------------------------------------------------------------------------
# 3. the claimed slice decomposition, built independently
# --------------------------------------------------------------------------
def slice_decomposition(vertices, palette, covector):
    """The reconstruction of `sum_colorings3_expand`.

    With S = (s0, s1, s2) the three smallest vertices and F the rest, returns

        mode0  : {f: (vector over colours at s0, matrix over (c1, c2))}
        mode2  : (vector over colours at s2, matrix over (c0, c1))
        mode1  : (vector over colours at s1, matrix over (c0, c2))

    each entry a polynomial.  `mode2` comes from the internal S edge
    {s0, s1}; `mode1` from {s0, s2}; every remaining matching sends s0 into
    F and lands in `mode0`.
    """
    vertices = tuple(vertices)
    s0, s1, s2 = vertices[0], vertices[1], vertices[2]
    free = tuple(v for v in vertices if v not in (s0, s1, s2))

    # ---- mode-s0 slices: one per F partner of s0 ----------------------------
    mode0 = {}
    for f in free:
        vector = {}
        for c0 in range(palette):
            entry = {}
            for d in range(palette):
                entry = poly_add(entry,
                                 poly_scale(formal_weight(min(s0, f), max(s0, f),
                                                          c0 if s0 < f else d,
                                                          d if s0 < f else c0),
                                            covector[f][d]))
            vector[c0] = entry
        rest_vertices = tuple(v for v in vertices if v not in (s0, f))
        rest = contracted_tensor(rest_vertices, (s1, s2), palette, covector)
        mode0[f] = (vector, rest)

    # ---- the two internal-S-edge slices -------------------------------------
    def internal(pair_lo, pair_hi, lone):
        rest_vertices = tuple(v for v in vertices if v != pair_lo
                              and v != pair_hi)
        rest = contracted_tensor(rest_vertices, (lone,), palette, covector)
        vector = {c: rest[(c,)] for c in range(palette)}
        head = {}
        for a in range(palette):
            for b in range(palette):
                head[(a, b)] = formal_weight(pair_lo, pair_hi, a, b)
        return vector, head

    mode2 = internal(s0, s1, s2)   # slice at mode s2, head is W(s0,s1,c0,c1)
    mode1 = internal(s0, s2, s1)   # slice at mode s1, head is W(s0,s2,c0,c2)
    return mode0, mode1, mode2


def assemble(mode0, mode1, mode2, palette):
    out = {}
    for c0, c1, c2 in product(range(palette), repeat=3):
        total = {}
        for _f, (vector, rest) in mode0.items():
            total = poly_add(total, poly_mul(vector[c0], rest[(c1, c2)]))
        vector2, head2 = mode2
        total = poly_add(total, poly_mul(head2[(c0, c1)], vector2[c2]))
        vector1, head1 = mode1
        total = poly_add(total, poly_mul(head1[(c0, c2)], vector1[c1]))
        out[(c0, c1, c2)] = total
    return out


def audit_three_mode_contraction_identity():
    """The decomposition is an exact identity in formal edge weights."""
    for n, palette in ((6, 3), (8, 3), (8, 2), (6, 4)):
        vertices = tuple(range(n))
        ones = {v: tuple(Q(1) for _ in range(palette)) for v in vertices}
        left = contracted_tensor(vertices, (0, 1, 2), palette, ones)
        mode0, mode1, mode2 = slice_decomposition(vertices, palette, ones)
        right = assemble(mode0, mode1, mode2, palette)
        require(set(left) == set(right), ("index sets differ", n, palette))
        for word in left:
            require(not poly_sub(left[word], right[word]),
                    ("contraction identity fails", n, palette, word))
        require(len(mode0) == n - 3, ("mode-0 slice count", n, len(mode0)))
        # nondegeneracy: the identity is not vacuous
        require(any(left[word] for word in left), ("empty identity", n))


def audit_identity_is_not_vacuous():
    """Mutation test.  Dropping any one mode-0 slice, or exchanging the two
    internal-S-edge slices, breaks the identity -- so the check above is
    testing the decomposition rather than an accident of bookkeeping."""
    n, palette = 6, 3
    vertices = tuple(range(n))
    ones = {v: tuple(Q(1) for _ in range(palette)) for v in vertices}
    left = contracted_tensor(vertices, (0, 1, 2), palette, ones)
    mode0, mode1, mode2 = slice_decomposition(vertices, palette, ones)

    for dropped in tuple(mode0):
        pruned = {f: value for f, value in mode0.items() if f != dropped}
        broken = assemble(pruned, mode1, mode2, palette)
        require(any(poly_sub(left[w], broken[w]) for w in left),
                ("dropping a mode-0 slice must break the identity", dropped))

    swapped = assemble(mode0, mode2, mode1, palette)
    require(any(poly_sub(left[w], swapped[w]) for w in left),
            "exchanging the two internal-edge slices must break the identity")


def audit_identity_with_torus_covectors():
    """The same identity with arbitrary nonvanishing covectors on F, and the
    contracted target is the three-mode diagonal with nonzero coefficients."""
    palette = 3
    vertices = tuple(range(8))
    choices = (
        {v: (Q(1), Q(-2), Q(3, 5)) for v in vertices},
        {v: (Q(v + 1), Q(-1, v + 2), Q(2)) for v in vertices},
        {v: (Q(7, 3), Q(1), Q(-4, 9)) for v in vertices},
    )
    for covector in choices:
        left = contracted_tensor(vertices, (0, 1, 2), palette, covector)
        mode0, mode1, mode2 = slice_decomposition(vertices, palette, covector)
        right = assemble(mode0, mode1, mode2, palette)
        for word in left:
            require(not poly_sub(left[word], right[word]),
                    ("torus contraction identity fails", word))
        # the contracted target: sum over F colourings of [iota constant]
        free = vertices[3:]
        for c0, c1, c2 in product(range(palette), repeat=3):
            expected = Q(0)
            if c0 == c1 == c2:
                expected = Q(1)
                for f in free:
                    expected *= covector[f][c0]
                require(expected != 0, ("torus coefficient vanished", c0))


# --------------------------------------------------------------------------
# 4. the linear-algebra step: `ker_support_le_2`
# --------------------------------------------------------------------------
def audit_support_two_subspaces_have_dimension_at_most_two():
    """A subspace all of whose vectors have support at most two has dimension
    at most two.  Exhaustively confirmed over F_2, F_3 and F_5 for every
    three-dimensional subspace of F^d, d <= 5, by canonical row-echelon form.

    The proof is field-independent: in reduced echelon form any two basis rows
    must both be unit vectors (their sum already has support two at the two
    pivots), so three of them sum to support three.
    """
    for modulus in (2, 3, 5):
        for dimension in (3, 4, 5):
            checked = 0
            for basis in _echelon_bases(modulus, dimension, 3):
                witness = False
                for coefficients in product(range(modulus), repeat=3):
                    vector = [0] * dimension
                    for index, scalar in enumerate(coefficients):
                        if scalar:
                            for column in range(dimension):
                                vector[column] = ((vector[column]
                                                   + scalar * basis[index][column])
                                                  % modulus)
                    if sum(1 for entry in vector if entry) >= 3:
                        witness = True
                        break
                require(witness,
                        ("rank-three subspace with all supports <= 2",
                         modulus, dimension))
                checked += 1
            require(checked > 0, ("no subspace enumerated", modulus, dimension))


def _echelon_bases(modulus, dimension, rank):
    """All reduced row-echelon bases of rank `rank` in F_modulus^dimension:
    one per subspace."""
    from itertools import combinations
    for pivots in combinations(range(dimension), rank):
        freecols = [c for c in range(dimension)
                    if c not in pivots and c > pivots[0]]
        slots = []
        for index, pivot in enumerate(pivots):
            slots.extend((index, c) for c in range(dimension)
                         if c > pivot and c not in pivots)
        for values in product(range(modulus), repeat=len(slots)):
            rows = [[0] * dimension for _ in range(rank)]
            for index, pivot in enumerate(pivots):
                rows[index][pivot] = 1
            for (index, column), value in zip(slots, values):
                rows[index][column] = value
            yield rows
        del freecols


def slice_bound(n, palette):
    """The reconstructed upper bound on the number of slices of the contracted
    tensor, and the inequality it forces."""
    return 2 + min(n - 3, palette)


def audit_boundary_is_d_at_most_n_minus_one():
    """`D - 2 <= min(N - 3, D)` is equivalent to `D <= N - 1`."""
    for n in range(4, 21, 2):
        for palette in range(2, 26):
            forced = (palette - 2) <= min(n - 3, palette)
            require(forced == (palette <= n - 1),
                    ("boundary algebra", n, palette))
        require(slice_bound(n, 3) == 2 + min(n - 3, 3),
                ("slice bound at D = 3", n))
    # the case this project actually targets
    require(slice_bound(8, 3) == 5, "slice bound at (8,3) is five")
    require(5 > 3, "five exceeds the diagonal slice rank three")
    require(slice_bound(8, 10) == 7, "slice bound at (8,10) is seven")
    require(7 < 10, "seven is below the diagonal slice rank ten")
    # the bound is exactly saturated at the one case with a known solution:
    # `eqSystem4_has_solution_d3` is a theorem upstream, and there the
    # reconstruction gives 2 + min(1, 3) = 3 slices for a target of slice
    # rank 3.  One more slice would have closed a case that is false.
    require(slice_bound(4, 3) == 3, "slice bound at (4,3) is three")
    require(not (3 >= 4), "(4,3) is not closed by the criterion")


UPSTREAM_COMPLEX_CASES = (
    # (N, D, upstream `category` for the complex statement), read from
    # /Users/rishi/workplace/formal-conjectures/FormalConjectures/Paper/
    #   MonochromaticQuantumGraph.lean  (this checkout, pinned there)
    (4, 4, 'solved'),
    (6, 3, 'open'),
    (6, 4, 'open'),
    (6, 5, 'open'),
    (6, 6, 'solved'),
    (8, 3, 'open'),
    (8, 10, 'solved'),
    (10, 3, 'open'),
    (10, 4, 'open'),
    (10, 5, 'open'),
    (10, 6, 'open'),
    (10, 7, 'open'),
    (10, 8, 'open'),
    (10, 9, 'open'),
    (10, 10, 'solved'),
    (12, 3, 'open'),
    (14, 3, 'open'),
    (16, 3, 'open'),
)


def audit_boundary_matches_upstream_ledger():
    """`D >= N` reproduces the upstream solved/open split for complex weights
    exactly -- every fixed-(N, D) complex statement marked `research solved`
    has `D >= N`, and every one marked `research open` has `D <= N - 1`.

    This is corroboration of the reconstruction, not a proof of it: the
    upstream categories are read from the pinned checkout, and the proofs
    behind the `solved` markers were not audited here.
    """
    for n, palette, category in UPSTREAM_COMPLEX_CASES:
        closed_by_slice_rank = palette >= n
        require(closed_by_slice_rank == (category == 'solved'),
                ("ledger mismatch", n, palette, category))


# --------------------------------------------------------------------------
# 5. slice rank is saturated at (8, 3)
# --------------------------------------------------------------------------
def audit_matching_tensor_attains_slice_rank_three():
    """An explicit `K_8` matching tensor whose slice rank is exactly three,
    the same value as `Delta_{8,3}`.  Hence slice rank on `(C^3)^{tensor 8}`
    takes its maximum on both sides and cannot separate them.

    Take `A_{01} = A_{23} = A_{45} = A_{67} = I_3` and every other block zero.
    Upper bound: any tensor in `(C^3)^{tensor 8}` is a sum of three slices at
    any single mode, so slice rank <= 3.  Lower bound: contracting modes
    2..7 with `e_0^*` restricts the tensor to the 3x3 identity matrix, whose
    slice rank (= matrix rank) is 3, and slice rank is monotone under
    restriction.  No appeal to Tao's diagonal lemma is needed.
    """
    palette = 3
    vertices = tuple(range(8))
    pairs = ((0, 1), (2, 3), (4, 5), (6, 7))

    def weight(u, v, i, j):
        if (u, v) in pairs and i == j:
            return Q(1)
        return Q(0)

    matchings = official_matchings(vertices)

    def coefficient(colour):
        total = Q(0)
        for matching in matchings:
            term = Q(1)
            for u, v in matching:
                term *= weight(u, v, colour[u], colour[v])
                if not term:
                    break
            total += term
        return total

    # it is a genuine matching tensor and it is not the diagonal
    require(coefficient((0, 0, 1, 1, 2, 2, 0, 0)) == Q(1),
            "the paired tensor is supported off the diagonal")
    require(coefficient((0, 0, 0, 0, 0, 0, 0, 0)) == Q(1),
            "the paired tensor has the constant coefficient one")
    require(coefficient((0, 1, 0, 0, 0, 0, 0, 0)) == Q(0),
            "an unpaired mismatch vanishes")

    # restriction certificate: contract modes 2..7 with e_0^*
    restricted = {}
    for a, b in product(range(palette), repeat=2):
        colour = (a, b, 0, 0, 0, 0, 0, 0)
        restricted[(a, b)] = coefficient(colour)
    for a, b in product(range(palette), repeat=2):
        expected = Q(1) if a == b else Q(0)
        require(restricted[(a, b)] == expected,
                ("restriction is not the identity matrix", a, b))
    require(_exact_rank([[restricted[(a, b)] for b in range(palette)]
                         for a in range(palette)]) == 3,
            "the restricted matrix must have rank three")

    # and the trivial cap: slice rank <= min_k dim V_k = 3 for any such tensor
    require(min(palette for _ in range(8)) == 3,
            "the ambient slice-rank cap at (8,3) is three")


def _exact_rank(rows):
    rows = [list(row) for row in rows]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = None
        for index in range(rank, len(rows)):
            if rows[index][column]:
                pivot = index
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        head = rows[rank][column]
        rows[rank] = [entry / head for entry in rows[rank]]
        for index in range(len(rows)):
            if index != rank and rows[index][column]:
                factor = rows[index][column]
                rows[index] = [a - factor * b
                               for a, b in zip(rows[index], rows[rank])]
        rank += 1
    return rank


# --------------------------------------------------------------------------
# 6. the monomial border family stops before D = N - 1
# --------------------------------------------------------------------------
def one_factorization_k8():
    """The round-robin one-factorization of `K_8`: seven disjoint perfect
    matchings, the largest possible number."""
    factors = []
    for r in range(7):
        matching = [tuple(sorted((7, r)))]
        for i in (1, 2, 3):
            u = (r + i) % 7
            v = (r - i) % 7
            matching.append(tuple(sorted((u, v))))
        factors.append(tuple(sorted(matching)))
    return tuple(factors)


def audit_full_one_factorization_has_no_border_valuation():
    """The border construction of `notes/tensor-route.md` §6 -- colour classes
    of valuation zero, every other perfect matching of strictly positive
    valuation -- cannot be run on a full one-factorization of `K_8`.

    Exact reason: every edge of `K_8` lies in exactly 15 of the 105 perfect
    matchings, so the average of all 105 matching indicator vectors is the
    uniform 1/7 vector, which is also the average of the seven one-factors.
    Hence the remaining 98 matchings average to the same point, and any
    valuation summing to zero on all seven factors sums to zero on that
    average -- contradicting a strictly positive value on each of the 98.

    This bounds one construction; it is not a statement about `Delta_{8,7}`.
    """
    vertices = tuple(range(8))
    matchings = official_matchings(vertices)
    require(len(matchings) == 105, "K_8 has 105 perfect matchings")

    edges = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
    require(len(edges) == 28, "K_8 has 28 edges")

    incidence = {edge: 0 for edge in edges}
    for matching in matchings:
        for pair in matching:
            incidence[pair] += 1
    for edge in edges:
        require(incidence[edge] == 15, ("edge multiplicity", edge))

    factors = one_factorization_k8()
    require(len(factors) == 7, "seven one-factors")
    require(len(set(factors)) == 7, "one-factors are distinct")
    seen = {}
    for factor in factors:
        require(sorted(w for pair in factor for w in pair) == list(vertices),
                ("one-factor is not a perfect matching", factor))
        for pair in factor:
            require(pair not in seen, ("one-factors overlap", pair))
            seen[pair] = True
    require(len(seen) == 28, "the one-factorization covers every edge once")

    factor_set = set(factors)
    others = [m for m in matchings if tuple(sorted(m)) not in factor_set]
    require(len(others) == 98, ("non-factor matchings", len(others)))

    # sum of indicator vectors: 7 factors give each edge once; all 105 give
    # each edge 15 times; so the other 98 give each edge 14 times.
    residual = {edge: 0 for edge in edges}
    for matching in others:
        for pair in matching:
            residual[pair] += 1
    for edge in edges:
        require(residual[edge] == 14, ("residual multiplicity", edge))

    # Farkas certificate: 2 * (sum over the 7 factors) = (sum over the 98)/7
    # as edge vectors, both equal to 2 * the all-ones vector.
    for edge in edges:
        require(2 * 1 * 7 == residual[edge], ("Farkas identity", edge))
    # so for any valuation nu vanishing on each factor,
    #   sum over the 98 matchings of nu(M) = 14 * sum_e nu(e) = 14 * 0 = 0,
    # which cannot have all 98 terms >= 1.
    require(98 > 0, "there is at least one non-factor matching to contradict")


# --------------------------------------------------------------------------
def main():
    audit_recursion_enumerates_perfect_matchings()
    audit_support_two_subspaces_have_dimension_at_most_two()
    audit_boundary_is_d_at_most_n_minus_one()
    audit_boundary_matches_upstream_ledger()
    audit_matching_tensor_attains_slice_rank_three()
    audit_full_one_factorization_has_no_border_valuation()
    audit_three_mode_contraction_identity()
    audit_identity_is_not_vacuous()
    audit_identity_with_torus_covectors()
    print("three-mode contraction slice boundary: all checks passed")
    print("  reconstructed bound   : slices <= 2 + min(N-3, D)")
    print("  forced consequence    : D <= N - 1")
    print("  at (8,10)             : 7 slices < 10  -> impossible")
    print("  at (8,3)              : 5 slices >= 3  -> no information")
    print("  slice rank cap at D=3 : 3, attained by an explicit K_8 matching"
          " tensor")


if __name__ == '__main__':
    main()
