#!/usr/bin/env python3
"""The symmetrized apolarity operator: feasible on A, infeasible on I^2.

Model and conventions are the fourth-Hasse audit's
(`verify_h3_full_hasse_cone_d4_descent_obstruction.py`):  h = 3,
direct-free, bounded, word m_8 = 01211222,

    A = H_MIXED   (the direct-free mixed hafnian: 90 squarefree quartic
                   monomials in 27 mixed edge variables),
    B = H_PURE - u  (the descent defect),
    I = (A, B).

The four-cube branch asks for an order-four operator in the mixed edge
directions,

    D = sum_M c_M partial_M,   M a 4-subset of the 27 mixed edges,

that lowers the I-filtration with a unit source, D(A) = 1.  The main
computation takes the c_M CONSTANT; the weight-splitting section below
shows that arbitrary polynomial coefficients reduce to that case at this
order, so nothing is lost.  This checker decides the question at two
different strengths and finds them to disagree.  Everything below is
proved OVER Q by exact rational arithmetic; the mod-p statements are
labelled as such and are redundant cross-checks of a rank already
established over Q.

GENERATOR LEVEL (FEASIBLE over Q).  Write

    Q_M := sum over proper nonempty S in M of (partial_S A)(partial_{M\\S} A),

so that partial_M(A^2) = 2 A partial_M A + Q_M and the generator-level
condition "D(A^2) in (A) + Q.A" is the linear system sum_M c_M Q_M =
alpha A with unit trace sum_{M in mon(A)} c_M = 1.  The symmetrized
apolarity operator

    D = (1/90) A(partial) = (1/90) sum_{M in mon(A)} partial_M

solves it, with alpha = 26/15 FORCED, because of the integral identity

    sum_{M in mon(A)} Q_M = 156 A.

Structure: the 11790 x 14610 system block-diagonalizes by site
multidegree into 1107 blocks, and only the 1^8 block -- whose index set
is exactly mon(A) -- touches A or the trace functional; the other 1106
blocks are homogeneous and solved by c_M = 0.  The 1^8 block is the
90 x 90 matrix K[m][M] = [Q_M]_m: symmetric, diagonal 14, off-diagonal
in {0, 2, 6}, rank 34, with K 1 = 156 . 1.  That same identity kills
every Farkas certificate in one line: a certificate mu would need
K mu = 1_A and 1^T mu = 0, but 156 (1^T mu) = 1^T K mu = 90, so
1^T mu = 15/26 =/= 0.  That settles the dual side by finite-dimensional
linear algebra over Q, and feasibility is constructive anyway; the
point-evaluation picture below is a remark, not a load-bearing step.
(Remark: A is squarefree -- certified here by a line restriction with
gcd(f, f') constant -- so (A) is radical and evaluations at points of
V(A) SPAN exactly the hyperplane {lambda : lambda(A) = 0}.  That
spanning statement needs V(A) taken over an algebraically closed field;
over Q alone the Nullstellensatz argument does not apply, which is one
more reason the verdict is not routed through it.)  Symmetrization
is essential: not one of the 90 single-monomial selections works --
cross(M) lies outside span{A, B} for every M in mon(A), which contains
the 15 selections the fourth-Hasse audit actually uses.  On the other
generators D behaves exactly: D(A) = 1, D(AB) = B, D(B^2) = 0.

IDEAL LEVEL (INFEASIBLE over Q).  Ask instead for D(I^2) subseteq I as
IDEALS.  Since I^2 = (A^2, AB, B^2), Leibniz gives

    D(f G) = sum_{|S| <= 4} (partial_S f) E_S[G],
    E_S[G] := sum_{M contains S} c_M partial_{M\\S} G,

and testing on the squarefree mixed monomials f = x^S, upward on |S|,
shows D(I^2) subseteq I <=> E_S[G] in I for every S with |S| <= 4 and
every G in {A^2, AB, B^2}.  Three of those layers are free for EVERY c
(G = B^2 has no mixed derivative; G = AB has partial_T(AB) = B partial_T A
so E_S[AB] in (B); |S| = 3 has partial_e(A^2) = 2 A partial_e A; |S| = 4 is
an identity).  The only live layer is |S| = 2 on G = A^2, and it is fatal:

  FORCING LEMMA.  Every element of (A) has site-degree >= 1 at every one
  of the eight sites, because A is site-multihomogeneous of degree
  (1,...,1).  The multidegree-(2.1 - delta) part of E_S[A^2] is
  2 sum_{sitedeg{e,f} = delta} c_{S+{e,f}} (partial_e A)(partial_f A) modulo
  (A).  If delta has a site of degree 2 then 2.1 - delta has a ZERO site,
  where (A) contributes nothing, so that component must vanish outright;
  and each of those 156 delta-classes contains EXACTLY ONE pair {e, f}.
  Hence c_{S + {e,f}} = 0 whenever e and f share a site: c is supported
  on perfect matchings, i.e. supp(c) subseteq mon(A), killing 17460 of
  the 17550 unknowns.

  Then the 195 remaining |S| = 2 conditions (disjoint pairs) finish the
  90 survivors with FULL LOCAL RANK -- each single condition kills every
  c_M it mentions (150 conditions with k = r = 3, 45 with k = r = 2) --
  and the checker exhibits, for all 90 M, an explicit rational pairing
  functional w_M with w_M((A)_6) = 0 and w_M(partial_{M'\\S}(A^2)) =
  delta_{M', M}.  Fifteen of the 90 read off a SINGLE degree-six monomial
  coefficient.  So c = 0 is forced and sum_{M in mon(A)} c_M = 0 =/= 1.

The split is a grading fact, hence stable: the generator condition sees
only the 1^8 block, precisely where the symmetrizing identity lives; the
ideal condition also probes multidegrees with a zero site, where (A) is
entirely absent and no cancellation is available.

VARIABLE COEFFICIENTS ARE NOT A WAY OUT, AT THIS ORDER.  Give R the
weight grading of T1: every edge variable weight 1, the homogenizer u
weight 4.  Both generators of I are weight-4 homogeneous (T1's fact,
re-verified here), so I and I^2 are weight-graded, and partial_T lowers
weight by exactly wt(T).  Split an arbitrary operator by weight shift,
D = sum_w D^(w) with D^(w) carrying weight-homogeneous coefficients of
weight wt(T) + w on the term c_T partial_T.  Since I is weight-graded,
D(I^2) subseteq I holds iff every D^(w)(I^2) subseteq I; and D(A) = 1
puts the unit entirely in the shift -4 part.  So the problem reduces to
D^(-4), whose coefficients are homogeneous of weight wt(T) - 4.  For a
multiset T of MIXED EDGES, wt(T) = |T|, so at order four this kills
|T| < 4 outright (no negative weights) and forces the |T| = 4
coefficients to be CONSTANTS -- with repeated directions now allowed,
which is why the forcing lemma is verified here over 2-multisets (all
183 blocked delta-classes are singletons, the 27 repeated directions
included) and 4-multisets (27405 = 27315 blocked + the 90 matchings).
Hence order-four mixed-edge operators with ARBITRARY polynomial
coefficients are closed too.

WHERE THAT STOPS.  The collapse needs wt(T) <= 4 across the support.
The weight-one coefficient space is nonzero (54 edge variables), so any
T with wt(T) >= 5 keeps genuinely variable coefficients and the
reduction fails.  That happens at order five in edge variables, and
already at order two once u is admitted (wt({u, e}) = 5); u alone has
wt = 4 at order one.  The reduction therefore does NOT generalize to
arbitrary order, and the operator route is NOT closed entirely.

Scope.  This closes order-four mixed-edge operators at the ideal level,
with arbitrary polynomial coefficients, inside the fourth-Hasse bounded
model.  It does NOT close hybrid operators involving partial_u
(partial_u B = -1 is a genuine filtration-lowering unit source; under
separate investigation), nor any order five or above, nor any question
outside this model.  The generator-level feasibility is not a repair --
it is exactly the input the R-linear prolongation attempt builds on.
Krenn's conjecture remains open.

Companion theorems, and what each forced about the operator's shape:

  * `notes/h3-source-valid-tower-first-obstruction.md` T1 -- the
    four-cube TEMPLATE cannot be coupled through a source-valid tower,
    since target zero forces lambda = D_J(A) in I while I has no nonzero
    element of weight < 4.  That is why the operator sought here is
    filtration-LOWERING (D(I^{n+1}) subseteq I^n with D(A) = 1) rather
    than source-valid (D(I) subseteq I).  T1 also supplies the weight
    grading used above; T1's own scope covers the template shape, not
    every chain in a prolonged complex.
  * Same note, T2 -- the phi-filtration puts the first source-validity
    bite, and the unit, at order four, both as hafnians of order-one
    data.  That is what fixes the operator's ORDER at four.  (The
    reduction to constant coefficients comes from T1's weight grading,
    not from T2.)
  * Same note, T3 -- the 360 order-one residuals are pairwise distinct,
    so constant-coefficient order-one faces carry no syzygy; mass has to
    enter at order four, which is the order this checker decides.
  * `notes/h3-prolonged-cascade-phi-closure.md` -- the prolonged
    squarefree lattice of four commuting source-valid derivations is
    phi-closed under the R-LINEAR coefficient convention.  Under that
    convention the differential applies D_S to the GENERATORS only, so
    the generator-level condition is what that note needs, and the
    generator-level feasibility above is what it can use.  The
    ideal-level condition decided below is what a coefficient-prolonging
    (Spencer) differential would require -- the convention that note
    explicitly excludes.  So the ideal-level section decides a condition
    strictly STRONGER than any cited companion currently requires; no
    companion forces it.
  * `notes/h3-descent-defect-row-space-invisibility.md` -- rows whose
    phi-image e_0-coefficients have every monomial of edge-degree >= 1
    cannot reach the defect (H_0 - u) e_0.  That is why the single
    selections are not enough and only a SYMMETRIZED combination over
    all 90 matchings has a chance: this checker confirms that all 90
    single selections fail at generator level too.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_LEDGER_SHA256 = (
    "5330ee72132733966ab93a86740a819ebc7341815122564721adbb8af332b4e5"
)

SITE_COUNT = 8
U_WEIGHT = 4
OPERATOR_ORDER = 4
CROSS_CHECK_PRIMES = (1009, 1013, 1019)
LINE_SEEDS = (20260803, 314159265, 2718281828)
WITNESS_SITE_PAIRS = ((0, 1), (2, 5), (3, 7), (4, 6))


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HASSE = load(
    "h3_apolarity_hasse",
    "verify_h3_full_hasse_cone_d4_descent_obstruction.py",
)

A = HASSE.H_MIXED
B = HASSE.B_PURE
MON_A = sorted(A)
SUPPORT = sorted({variable for term in MON_A for variable in term})


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# --------------------------------------------------------------------
# site multidegree
# --------------------------------------------------------------------

def site_degree(term):
    """Multidegree of a monomial for the eight-site grading."""
    degrees = [0] * SITE_COUNT
    for variable in term:
        degrees[variable[1]] += 1
        degrees[variable[2]] += 1
    return tuple(degrees)


def weight(term):
    """T1's weight grading: every edge variable 1, the homogenizer u 4."""
    return sum(U_WEIGHT if variable == HASSE.HOMOGENIZING_U else 1
               for variable in term)


# --------------------------------------------------------------------
# proper faces of A and the cross terms Q_M
# --------------------------------------------------------------------

def build_faces():
    """partial_S A for |S| = 1, 2, 3, keeping only the nonzero ones."""
    order_one = {}
    for variable in SUPPORT:
        face = HASSE.derivative(A, variable)
        if face:
            order_one[(variable,)] = face
    order_two = {}
    for pair in combinations(SUPPORT, 2):
        face = HASSE.derivatives(A, pair)
        if face:
            order_two[pair] = face
    order_three = {}
    for term in MON_A:
        for triple in combinations(term, 3):
            if triple in order_three:
                continue
            face = HASSE.derivatives(A, triple)
            if face:
                order_three[triple] = face
    return order_one, order_two, order_three


FACE1, FACE2, FACE3 = build_faces()
FACES = (FACE1, FACE2, FACE3)
_CROSS_CACHE = {}


def cross(subset):
    """Q_M = sum over proper nonempty S in M of
    (partial_S A)(partial_{M\\S} A).
    """
    key = tuple(sorted(subset))
    cached = _CROSS_CACHE.get(key)
    if cached is not None:
        return cached
    total = {}
    for size in (1, 2, 3):
        for chosen in combinations(key, size):
            rest = tuple(x for x in key if x not in chosen)
            left = FACES[size - 1].get(chosen)
            if not left:
                continue
            right = FACES[3 - size].get(rest)
            if not right:
                continue
            total = HASSE.add(total, HASSE.multiply(left, right))
    _CROSS_CACHE[key] = total
    return total


# --------------------------------------------------------------------
# exact linear algebra over Q
# --------------------------------------------------------------------

def row_reduce(rows, column_count):
    """In-place-free Gauss-Jordan over Q.  Returns (rows, pivot columns)."""
    rows = [[Q(entry) for entry in row] for row in rows]
    pivots = []
    rank = 0
    for column in range(column_count):
        chosen = None
        for index in range(rank, len(rows)):
            if rows[index][column]:
                chosen = index
                break
        if chosen is None:
            continue
        rows[rank], rows[chosen] = rows[chosen], rows[rank]
        inverse = Q(1) / rows[rank][column]
        rows[rank] = [entry * inverse for entry in rows[rank]]
        for index in range(len(rows)):
            if index != rank and rows[index][column]:
                factor = rows[index][column]
                rows[index] = [a - factor * b
                               for a, b in zip(rows[index], rows[rank])]
        pivots.append(column)
        rank += 1
        if rank == len(rows):
            break
    return rows, pivots


def rank_over_Q(rows, column_count):
    return len(row_reduce(rows, column_count)[1])


def rank_mod_p(rows, column_count, prime):
    rows = [[(int(entry.numerator)
              * pow(int(entry.denominator), prime - 2, prime)) % prime
             for entry in row] for row in rows]
    pivots = 0
    rank = 0
    for column in range(column_count):
        chosen = None
        for index in range(rank, len(rows)):
            if rows[index][column]:
                chosen = index
                break
        if chosen is None:
            continue
        rows[rank], rows[chosen] = rows[chosen], rows[rank]
        inverse = pow(rows[rank][column], prime - 2, prime)
        rows[rank] = [entry * inverse % prime for entry in rows[rank]]
        for index in range(len(rows)):
            if index != rank and rows[index][column]:
                factor = rows[index][column]
                rows[index] = [(a - factor * b) % prime
                               for a, b in zip(rows[index], rows[rank])]
        pivots += 1
        rank += 1
        if rank == len(rows):
            break
    return pivots


def solvable(rows, column_count):
    """Is the augmented system rows = [coefficients | rhs] consistent?"""
    _, pivots = row_reduce(rows, column_count + 1)
    return column_count not in pivots


def in_span(polynomial, basis):
    terms = sorted({term for poly in basis + [polynomial] for term in poly})
    rows = [[Q(poly.get(term, 0)) for poly in basis]
            + [Q(polynomial.get(term, 0))] for term in terms]
    return solvable(rows, len(basis))


def solve_functional(polynomials, targets):
    """A rational functional w with sum_m w[m] p[m] = target, or None."""
    terms = sorted({term for poly in polynomials for term in poly})
    rows = [[Q(poly.get(term, 0)) for term in terms] + [Q(target)]
            for poly, target in zip(polynomials, targets)]
    reduced, pivots = row_reduce(rows, len(terms) + 1)
    if len(terms) in pivots:
        return None
    functional = {}
    for index, column in enumerate(pivots):
        value = reduced[index][len(terms)]
        if value:
            functional[terms[column]] = value
    return functional


def apply_functional(functional, polynomial):
    return sum(value * Q(polynomial.get(term, 0))
               for term, value in functional.items())


def echelon_polynomials(polynomials):
    """Echelon basis of a span of polynomials, keyed by leading monomial."""
    basis = {}
    for polynomial in polynomials:
        working = {term: Q(value) for term, value in polynomial.items()
                   if value}
        while working:
            pivot = max(working)
            if pivot in basis:
                factor = working[pivot]
                for term, value in basis[pivot].items():
                    updated = working.get(term, Q(0)) - factor * value
                    if updated:
                        working[term] = updated
                    elif term in working:
                        del working[term]
            else:
                inverse = Q(1) / working[pivot]
                basis[pivot] = {term: value * inverse
                                for term, value in working.items()}
                break
    return sorted(basis.items(), reverse=True)


def reduce_polynomial(polynomial, echelon):
    working = {term: Q(value) for term, value in polynomial.items() if value}
    for pivot, reducer in echelon:
        factor = working.get(pivot)
        if not factor:
            continue
        for term, value in reducer.items():
            updated = working.get(term, Q(0)) - factor * value
            if updated:
                working[term] = updated
            elif term in working:
                del working[term]
    return working


def content_hash(blocks):
    """sha256 of the actual computed geometry, not of its description."""
    hasher = sha256()
    for block in blocks:
        for item in block:
            hasher.update(repr(item).encode("ascii"))
            hasher.update(b";")
        hasher.update(b"|")
    return hasher.hexdigest()


# --------------------------------------------------------------------
# GENERATOR LEVEL
# --------------------------------------------------------------------

def deterministic_values(seed):
    """A reproducible integer point in [-5, 5]^SUPPORT (no RNG dependence)."""
    state = seed
    values = {}
    for variable in SUPPORT:
        state = (1103515245 * state + 12345) % (1 << 31)
        values[variable] = Q((state >> 7) % 11 - 5)
    return values


def restrict_A_to_line(base, direction):
    """A(base + t.direction) as an exact univariate quartic in t."""
    coefficients = [Q(0)] * 5
    for term, value in A.items():
        univariate = [Q(1)]
        for variable in term:
            extended = [Q(0)] * (len(univariate) + 1)
            for power, entry in enumerate(univariate):
                extended[power] += entry * base[variable]
                extended[power + 1] += entry * direction[variable]
            univariate = extended
        for power, entry in enumerate(univariate):
            coefficients[power] += value * entry
    return coefficients


def polynomial_gcd_degree(coefficients):
    """deg gcd(f, f') for an exact univariate f over Q."""
    def trim(poly):
        poly = list(poly)
        while poly and poly[-1] == 0:
            poly.pop()
        return poly

    def remainder(left, right):
        left = trim(left)
        right = trim(right)
        while left and len(left) >= len(right):
            factor = left[-1] / right[-1]
            shift = len(left) - len(right)
            for index, entry in enumerate(right):
                left[shift + index] -= factor * entry
            left = trim(left)
        return left

    first = trim(coefficients)
    second = trim([index * first[index] for index in range(1, len(first))])
    while second:
        first, second = second, remainder(first, second)
    return len(first) - 1


def generator_level():
    crosses = {}
    for subset in combinations(SUPPORT, 4):
        value = cross(subset)
        if value:
            crosses[subset] = value

    quartics = set(A)
    for value in crosses.values():
        quartics |= set(value)

    require(len(SUPPORT) == 27,
            "mixed-edge support size left 27")
    require(len(MON_A) == 90,
            "direct-free mixed hafnian left 90 monomials")
    require(len(FACE1) == 27 and len(FACE2) == 195 and len(FACE3) == 360,
            "nonzero proper face census left 27 + 195 + 360 = 582")
    require(len(crosses) == 11790,
            "nonzero cross-term census left 11790 unknowns")
    require(len(quartics) == 14610,
            "quartic equation census left 14610 equations")
    a_variables = {variable for term in A for variable in term}
    b_variables = {variable for term in B for variable in term}
    require(not (a_variables & b_variables),
            "beta = 0 forcing: A and B stopped having disjoint variables")

    # --- multidegree block decomposition -----------------------------
    ones = (1,) * SITE_COUNT
    for subset, value in crosses.items():
        target = tuple(2 - entry for entry in site_degree(subset))
        require({site_degree(term) for term in value} == {target},
                "cross-term site-multihomogeneity of degree 2.1 - deg(M)")
    require({site_degree(term) for term in A} == {ones},
            "A left site-multidegree (1,...,1)")
    blocks = {}
    for subset in crosses:
        blocks.setdefault(site_degree(subset), []).append(subset)
    require(len(blocks) == 1107,
            "site-multidegree block count left 1107")
    require(sorted(blocks[ones]) == MON_A,
            "the 1^8 block stopped being exactly mon(A)")
    require(sum(len(block) for degree, block in blocks.items()
                if degree != ones) == len(crosses) - 90,
            "the 1106 off-diagonal blocks stopped partitioning the rest")

    # --- the 90 x 90 block matrix K ----------------------------------
    matrix = [[Q(crosses[subset].get(term, 0)) for subset in MON_A]
              for term in MON_A]
    require(all(matrix[i][j] == matrix[j][i]
                for i in range(90) for j in range(90)),
            "K symmetry")
    require({matrix[i][i] for i in range(90)} == {14},
            "K diagonal left the constant 14")
    off_diagonal = {matrix[i][j] for i in range(90) for j in range(90)
                    if i != j}
    require(off_diagonal == {Q(0), Q(2), Q(6)},
            "K off-diagonal value set left {0, 2, 6}")
    row_sums = {sum(row) for row in matrix}
    column_sums = {sum(matrix[i][j] for i in range(90)) for j in range(90)}
    require(len(row_sums) == 1 and row_sums == column_sums,
            "the integral identity K.1 = 156.1 (constant row and column sums)")
    row_sum = int(next(iter(row_sums)))
    require(row_sum == 156,
            "the integral row sum left 156")
    matrix_rank = rank_over_Q(matrix, 90)
    require(matrix_rank == 34,
            "K rank left 34")

    # --- the explicit solution ---------------------------------------
    require(HASSE.add(*[cross(subset) for subset in MON_A])
            == HASSE.scale(row_sum, A),
            "the integral identity sum_{M in mon(A)} Q_M = 156 A")
    coefficient = Q(1, len(MON_A))
    combination = {}
    for subset in MON_A:
        combination = HASSE.add(combination,
                                HASSE.scale(coefficient, cross(subset)))
    # alpha is read off the computed row sum, not asserted.
    alpha = Q(row_sum, len(MON_A))
    require(HASSE.add(combination, HASSE.scale(-alpha, A)) == {},
            "the generator-level identity sum_M c_M Q_M = alpha A at the "
            "row-sum-derived alpha")
    require(sum(coefficient for _ in MON_A) == 1,
            "unit trace sum_{M in mon(A)} c_M = 1")

    square = HASSE.multiply(A, A)
    apolar_square = {}
    for subset in MON_A:
        apolar_square = HASSE.add(apolar_square,
                                  HASSE.derivatives(square, subset))
    # The multiple is read off the computed polynomial, then cross-checked
    # against 2 . |mon(A)| + row_sum, which is what (2) and (4) predict.
    require(A and all(term in A for term in apolar_square),
            "A(partial)(A^2) stayed a multiple of A on its monomial support")
    apolar_multiple = apolar_square[MON_A[0]] / A[MON_A[0]]
    require(apolar_square == HASSE.scale(apolar_multiple, A),
            "the independent replay A(partial)(A^2) is a scalar multiple of A")
    require(apolar_multiple == 2 * len(MON_A) + row_sum,
            "the replay multiple equals 2 |mon(A)| + row sum = 336")
    require(all(HASSE.derivatives(A, subset) == HASSE.constant()
                for subset in MON_A),
            "D(A) = 1 on every matching")
    mixed_product = HASSE.multiply(A, B)
    apolar_mixed = {}
    for subset in MON_A:
        apolar_mixed = HASSE.add(apolar_mixed,
                                 HASSE.derivatives(mixed_product, subset))
    require(HASSE.scale(coefficient, apolar_mixed) == B,
            "D(AB) = B exactly")
    defect_square = HASSE.multiply(B, B)
    apolar_defect = {}
    for subset in MON_A:
        apolar_defect = HASSE.add(apolar_defect,
                                  HASSE.derivatives(defect_square, subset))
    require(apolar_defect == {},
            "D(B^2) = 0 exactly")

    # --- symmetrization is essential: every single selection fails ----
    selections = [
        tuple(sorted(HASSE.selected_directions(deleted, matching)[0]))
        for deleted in HASSE.ODD
        for matching in HASSE.matchings(HASSE.face(deleted))]
    require(len(selections) == 15,
            "the fourth-Hasse selection census left 15")
    require(all(selection in A for selection in selections),
            "every fourth-Hasse selection is a monomial of A")
    require(set(selections) <= set(MON_A),
            "the 15 selections sit inside the 90 matchings")
    failing = [subset for subset in MON_A
               if not in_span(cross(subset), [A, B])]
    require(len(failing) == 90,
            "single-selection failure: all 90 cross(M) outside span{A, B}")

    # --- Farkas completeness and the one-line no-certificate proof ----
    gcd_degrees = []
    for seed in LINE_SEEDS:
        base = deterministic_values(seed)
        direction = deterministic_values(seed ^ 0x5F5E0FF)
        restriction = restrict_A_to_line(base, direction)
        require(len([1 for entry in restriction if entry]) > 0
                and restriction[4] != 0,
                "the test line stayed transverse (quartic leading term)")
        gcd_degrees.append(polynomial_gcd_degree(restriction))
    require(set(gcd_degrees) == {0},
            "A squarefree: gcd(f, f') constant on every test line")

    dual = [matrix[i][:] + [Q(1)] for i in range(90)]
    dual.append([Q(1)] * 90 + [Q(0)])
    require(not solvable(dual, 90),
            "no Farkas certificate: {K mu = 1_A, 1^T mu = 0} inconsistent")
    # K mu = 1_A forces row_sum . (1^T mu) = 1^T K mu = |mon(A)|, so the trace
    # of any solution is pinned, and it is nonzero.  Both facts are computed
    # from row_sum, not asserted.
    trace_of_any_solution = Q(len(MON_A), row_sum)
    require(row_sum * trace_of_any_solution == len(MON_A)
            and trace_of_any_solution != 0,
            "the one-line dual contradiction: row_sum (1^T mu) = |mon(A)| "
            "pins a nonzero trace, contradicting 1^T mu = 0")

    return {
        "support_size": len(SUPPORT),
        "hafnian_monomials": len(MON_A),
        "proper_faces_by_order": [len(FACE1), len(FACE2), len(FACE3)],
        "cross_terms_nonzero": len(crosses),
        "cross_terms_total": len(list(combinations(SUPPORT, 4))),
        "quartic_equations": len(quartics),
        "multidegree_blocks": len(blocks),
        "one_eight_block_size": len(blocks[ones]),
        "K_diagonal": sorted(int(matrix[i][i]) for i in range(90))[0],
        "K_off_diagonal_values": sorted(int(v) for v in off_diagonal),
        "K_row_sum": row_sum,
        "K_rank": matrix_rank,
        "alpha_forced": str(alpha),
        "apolar_square_multiple": str(apolar_multiple),
        "selections_checked": len(selections),
        "single_selections_failing": len(failing),
        "squarefree_line_gcd_degrees": gcd_degrees,
        "farkas_certificate_exists": int(solvable(dual, 90)),
        "forced_dual_trace": str(trace_of_any_solution),
        "K_content_sha256": content_hash(
            [[(MON_A[i], MON_A[j], int(matrix[i][j]))
              for i in range(90) for j in range(90) if matrix[i][j]]]),
    }


# --------------------------------------------------------------------
# IDEAL LEVEL
# --------------------------------------------------------------------

def degree_two_monomials():
    products = [{tuple(sorted(pair)): Q(1)}
                for pair in combinations(SUPPORT, 2)]
    products += [{(variable, variable): Q(1)} for variable in SUPPORT]
    return products


def ideal_level():
    square = HASSE.multiply(A, A)
    mixed_product = HASSE.multiply(A, B)
    defect_square = HASSE.multiply(B, B)
    deg_two = degree_two_monomials()
    require(len(deg_two) == 378,
            "degree-two monomial census left 378")

    # --- the free layers ---------------------------------------------
    require(all(HASSE.derivative(defect_square, variable) == {}
                for variable in SUPPORT),
            "free layer G = B^2: no mixed derivative survives")
    singles = list(combinations(SUPPORT, 1))
    pairs = list(combinations(SUPPORT, 2))
    # The induction's base: B carries no mixed variable at all, so
    # partial_e(AB) = (partial_e A) B for every mixed e, and partial_T(AB) =
    # (partial_T A) B for every mixed multiset T follows by iterating.
    require(all(HASSE.derivative(B, variable) == {}
                for variable in SUPPORT),
            "free layer G = AB base case: B has no mixed variable, so "
            "partial_e B = 0 for all 27 mixed edges")
    require(all(HASSE.derivatives(mixed_product, subset)
                == HASSE.multiply(B, HASSE.derivatives(A, subset))
                for subset in singles + pairs),
            "free layer G = AB: partial_T(AB) = B partial_T A at |T| = 1, 2, "
            "hence E_S[AB] lies in (B)")
    # Exhaustive at |T| = 3 too.  |T| = 4 then follows from the same
    # induction: partial_e((partial_T' A) B) = (partial_e partial_T' A) B
    # because partial_e B = 0, checked above for all 27 mixed edges.  The
    # 90 matchings -- the only |T| = 4 sets that survive the forcing lemma
    # -- are additionally checked outright.
    order_three_checked = 0
    for triple in combinations(SUPPORT, 3):
        require(HASSE.derivatives(mixed_product, triple)
                == HASSE.multiply(B, HASSE.derivatives(A, triple)),
                "free layer G = AB at |T| = 3")
        order_three_checked += 1
    order_four_checked = 0
    for subset in MON_A:
        require(HASSE.derivatives(mixed_product, subset)
                == HASSE.multiply(B, HASSE.derivatives(A, subset)),
                "free layer G = AB at |T| = 4 on the matchings")
        order_four_checked += 1
    require(order_three_checked == 2925 and order_four_checked == len(MON_A),
            "free layer G = AB swept all 2925 triples and the 90 matchings")
    require(all(HASSE.derivative(square, variable)
                == HASSE.scale(2, HASSE.multiply(
                    A, HASSE.derivative(A, variable)))
                for variable in SUPPORT),
            "free layer |S| = 3: partial_e(A^2) = 2 A partial_e A for every c")

    # --- the forcing lemma -------------------------------------------
    by_delta = {}
    for pair in pairs:
        by_delta.setdefault(site_degree(pair), []).append(pair)
    sharing = {delta: found for delta, found in by_delta.items()
               if max(delta) == 2}
    disjoint = {delta: found for delta, found in by_delta.items()
                if max(delta) == 1}
    require(len(sharing) == 156 and all(len(found) == 1
                                        for found in sharing.values()),
            "singleton delta-classes: 156 shared-site classes, each of size 1")
    disjoint_pairs = sum(len(found) for found in disjoint.values())
    require(disjoint_pairs == 195,
            "disjoint-pair census left 195 live |S| = 2 conditions")
    require(len(sharing) + disjoint_pairs == len(pairs) == 351,
            "the delta-class partition of the 351 edge pairs")
    require(len(sharing) + len(disjoint) == len(by_delta) == 226,
            "the delta-class census left 226 classes")
    require(all(HASSE.derivatives(A, found[0]) == {}
                for found in sharing.values()),
            "shared-site second faces of A vanish")
    require(all(HASSE.derivative(A, variable) for variable in SUPPORT),
            "every order-one face of A is nonzero")
    minimum_site_degree = min(
        min(site_degree(term))
        for factor in deg_two
        for term in HASSE.multiply(A, factor))
    require(minimum_site_degree >= 1,
            "the zero-site invisibility of (A): every degree-six element of "
            "(A) has site-degree >= 1 at every site")
    non_matchings = sum(
        1 for subset in combinations(SUPPORT, 4)
        if len({site for variable in subset
                for site in (variable[1], variable[2])}) != SITE_COUNT)
    require(non_matchings == 17460 and 17550 - non_matchings == len(MON_A),
            "the forcing lemma kills 17460 of 17550 supports, leaving mon(A)")

    # --- local rank of each single |S| = 2 condition -------------------
    null_space = [HASSE.multiply(A, factor) for factor in deg_two]
    shape_counts = {}
    covered = set()
    conditions = 0
    for pair in pairs:
        if max(site_degree(pair)) != 1:
            continue
        conditions += 1
        containing = [subset for subset in MON_A
                      if pair[0] in subset and pair[1] in subset]
        columns = [HASSE.derivatives(
            square, tuple(x for x in subset if x not in pair))
            for subset in containing]
        target = site_degree(next(iter(columns[0])))
        echelon = echelon_polynomials(
            [poly for poly in null_space
             if poly and site_degree(next(iter(poly))) == target])
        reduced = [reduce_polynomial(poly, echelon) for poly in columns]
        terms = sorted({term for poly in reduced for term in poly})
        width = len(reduced)
        local_rank = rank_over_Q(
            [[poly.get(term, Q(0)) for poly in reduced] for term in terms],
            width)
        shape_counts[(width, local_rank)] = (
            shape_counts.get((width, local_rank), 0) + 1)
        if local_rank == width:
            covered |= set(containing)
    require(conditions == 195,
            "the live |S| = 2 layer left 195 conditions")
    require(shape_counts == {(3, 3): 150, (2, 2): 45},
            "full local rank on every |S| = 2 condition (150 of shape 3, "
            "45 of shape 2)")
    require(len(covered) == 90,
            "every matching coefficient is killed by a single local condition")

    # --- explicit pairing certificates, all 90 ------------------------
    certificates = {}
    for subset in MON_A:
        pair = (subset[0], subset[1])
        containing = [other for other in MON_A
                      if pair[0] in other and pair[1] in other]
        columns = [HASSE.derivatives(
            square, tuple(x for x in other if x not in pair))
            for other in containing]
        reach = set().union(*[set(column) for column in columns])
        nulls = [poly for poly in
                 (HASSE.multiply(A, factor) for factor in deg_two)
                 if poly and set(poly) & reach]
        functional = solve_functional(
            columns + nulls,
            [Q(1 if other == subset else 0) for other in containing]
            + [Q(0)] * len(nulls))
        require(functional is not None,
                "pairing certificate w_M exists for every matching")
        require(all(apply_functional(functional,
                                     HASSE.multiply(A, factor)) == 0
                    for factor in deg_two),
                "pairing certificate annihilates A times all 378 degree-two "
                "monomials")
        require(all(apply_functional(functional, columns[index])
                    == (1 if containing[index] == subset else 0)
                    for index in range(len(containing))),
                "pairing certificate reproduces the Kronecker delta on "
                "partial_{M'\\S}(A^2)")
        certificates[subset] = functional
    require(len(certificates) == 90,
            "all 90 pairing certificates built and verified")
    supports = sorted(len(w) for w in certificates.values())
    single_monomial = [subset for subset, w in certificates.items()
                       if len(w) == 1]
    require(supports[0] == 1 and supports[-1] == 4,
            "pairing certificate supports left the range 1..4 monomials")
    require(len(single_monomial) == 15,
            "the single-monomial certificate census left 15")

    witness = None
    for subset in sorted(single_monomial):
        pairs_of = tuple(sorted((variable[1], variable[2])
                                for variable in subset))
        if pairs_of == WITNESS_SITE_PAIRS:
            witness = subset
            break
    require(witness is not None,
            "the named single-monomial witness M is still single-monomial")
    witness_pair = (witness[0], witness[1])
    witness_containing = [other for other in MON_A
                          if witness_pair[0] in other
                          and witness_pair[1] in other]
    witness_monomial = next(iter(certificates[witness]))
    witness_scale = certificates[witness][witness_monomial]
    witness_readings = [
        int(HASSE.derivatives(
            square, tuple(x for x in other if x not in witness_pair)
        ).get(witness_monomial, 0)) for other in witness_containing]
    require(all(HASSE.multiply(A, factor).get(witness_monomial, 0) == 0
                for factor in deg_two),
            "the witness monomial has zero coefficient throughout (A)_6")
    require(sum(1 for value in witness_readings if value) == 1,
            "the witness monomial reads exactly one matching coefficient")

    # --- the assembled ideal-level system -----------------------------
    index_of = {subset: index for index, subset in enumerate(MON_A)}
    layers = []

    def add_condition(columns, nulls, layer):
        columns = [(subset, poly) for subset, poly in columns.items() if poly]
        if not columns:
            return
        target = site_degree(next(iter(columns[0][1])))
        echelon = echelon_polynomials(
            [poly for poly in nulls
             if poly and site_degree(next(iter(poly))) == target])
        reduced = [(subset, reduce_polynomial(poly, echelon))
                   for subset, poly in columns]
        terms = sorted({term for _, poly in reduced for term in poly})
        rows = [[poly.get(term, Q(0)) for _, poly in reduced]
                for term in terms]
        echelon_rows, pivots = row_reduce(rows, len(reduced))
        for index in range(len(pivots)):
            equation = [Q(0)] * 90
            for position, (subset, _) in enumerate(reduced):
                equation[index_of[subset]] = echelon_rows[index][position]
            layers.append((layer, equation))

    null4 = [A]
    null5 = [HASSE.multiply(A, {(variable,): Q(1)}) for variable in SUPPORT]
    null6 = [HASSE.multiply(A, factor) for factor in deg_two]
    add_condition({subset: cross(subset) for subset in MON_A}, null4, 0)
    for variable in SUPPORT:
        add_condition(
            {subset: HASSE.derivatives(
                square, tuple(x for x in subset if x != variable))
             for subset in MON_A if variable in subset},
            null5, 1)
    for pair in pairs:
        if max(site_degree(pair)) != 1:
            continue
        add_condition(
            {subset: HASSE.derivatives(
                square, tuple(x for x in subset if x not in pair))
             for subset in MON_A if pair[0] in subset and pair[1] in subset},
            null6, 2)

    by_layer = {}
    for layer, _ in layers:
        by_layer[layer] = by_layer.get(layer, 0) + 1
    require(by_layer == {0: 33, 1: 255, 2: 540} and len(layers) == 828,
            "the assembled ideal-level system left 33 + 255 + 540 = 828 "
            "equations")
    layer_two_rank = rank_over_Q(
        [equation for layer, equation in layers if layer == 2], 90)
    require(layer_two_rank == 90,
            "the |S| = 2 layer alone has rank 90 over Q")
    total_rank = rank_over_Q([equation for _, equation in layers], 90)
    require(total_rank == 90,
            "the assembled ideal-level system has rank 90 over Q, forcing "
            "c = 0")
    # Solve the homogeneous system outright and read the trace off its unique
    # solution, rather than asserting the value zero.
    augmented = [equation + [Q(0)] for _, equation in layers]
    reduced_rows, solution_pivots = row_reduce(augmented, 91)
    require(sorted(solution_pivots) == list(range(90)),
            "the ideal-level system pivots on every matching coefficient, so "
            "its solution space is a single point")
    solution = [Q(0)] * 90
    for index, column in enumerate(solution_pivots):
        solution[column] = reduced_rows[index][90]
    forced_trace = sum(solution)
    require(all(value == 0 for value in solution),
            "the unique ideal-level solution is c = 0")
    modular_ranks = {}
    for prime in CROSS_CHECK_PRIMES:
        modular_ranks[prime] = rank_mod_p(
            [equation for _, equation in layers], 90, prime)
    require(set(modular_ranks.values()) == {90},
            "mod-p cross-check of the ideal-level rank")

    # --- what the generator-level solution does here ------------------
    uniform = [Q(1, 90)] * 90
    violated = {}
    for layer, equation in layers:
        if sum(a * b for a, b in zip(equation, uniform)):
            violated[layer] = violated.get(layer, 0) + 1
    require(violated.get(0, 0) == 0,
            "the symmetrized solution still satisfies the generator layer")
    require(violated.get(1, 0) > 0 and violated.get(2, 0) > 0,
            "the symmetrized solution fails the |S| = 1 and |S| = 2 layers")

    return {
        "degree_two_monomials": len(deg_two),
        "shared_site_delta_classes": len(sharing),
        "disjoint_delta_classes": len(disjoint),
        "disjoint_pairs": disjoint_pairs,
        "supports_killed_by_forcing": non_matchings,
        "supports_surviving": 17550 - non_matchings,
        "minimum_site_degree_in_ideal": minimum_site_degree,
        "live_conditions": conditions,
        "local_shape_counts": sorted(
            [list(key) + [value] for key, value in shape_counts.items()]),
        "matchings_locally_covered": len(covered),
        "pairing_certificates": len(certificates),
        "certificate_support_range": [supports[0], supports[-1]],
        "single_monomial_certificates": len(single_monomial),
        "witness_site_pairs": [list(p) for p in WITNESS_SITE_PAIRS],
        "witness_monomial": repr(witness_monomial),
        "witness_scale": str(witness_scale),
        "witness_readings": witness_readings,
        "equations_by_layer": sorted(by_layer.items()),
        "layer_two_rank_over_Q": layer_two_rank,
        "assembled_rank_over_Q": total_rank,
        "assembled_rank_mod_p": sorted(modular_ranks.items()),
        "uniform_solution_violations": sorted(violated.items()),
        "forced_trace": str(forced_trace),
        "abs_free_layer_orders_swept": [len(singles), len(pairs),
                                        order_three_checked,
                                        order_four_checked],
        "certificate_content_sha256": content_hash(
            [[(subset, sorted((repr(term), str(value))
                              for term, value in certificates[subset].items()))
              for subset in MON_A]]),
    }


# --------------------------------------------------------------------
# WEIGHT SPLITTING: variable coefficients at order four, and the exact
# point where the reduction stops generalizing to higher order.
# --------------------------------------------------------------------

def weight_reduction():
    pure_support = sorted({variable for term in HASSE.H_PURE
                           for variable in term})
    all_variables = sorted(set(SUPPORT) | set(pure_support)
                           | {HASSE.HOMOGENIZING_U})

    # --- the grading is T1's, and both generators are homogeneous ------
    require({weight(term) for term in A} == {4},
            "T1's weight grading: A is weight-4 homogeneous")
    require({weight(term) for term in B} == {4},
            "T1's weight grading: B = H_0 - u is weight-4 homogeneous")
    require(weight((HASSE.HOMOGENIZING_U,)) == U_WEIGHT,
            "the homogenizer u carries weight four")
    square = HASSE.multiply(A, A)
    for generator, name in ((square, "A^2"),
                            (HASSE.multiply(A, B), "AB"),
                            (HASSE.multiply(B, B), "B^2")):
        require({weight(term) for term in generator} == {8},
                "I^2 is weight-graded: its generator " + name
                + " is weight-8 homogeneous")

    # --- every condition family is weight-homogeneous ------------------
    # The structural fact first: partial_v lowers weight by exactly wt(v),
    # checked on every one of the 55 ring variables against every generator
    # of I^2.  Weight-homogeneity of the condition families follows, and is
    # then swept directly at the orders the |S| = 2, 1, 0 conditions use.
    for variable in all_variables:
        for generator in (square, HASSE.multiply(A, B), HASSE.multiply(B, B)):
            derived = HASSE.derivative(generator, variable)
            if derived:
                require({weight(term) for term in derived}
                        == {8 - weight((variable,))},
                        "partial_v lowers weight by exactly wt(v) on the "
                        "generators of I^2")
    condition_weights = {}
    for order, family in ((2, list(combinations(SUPPORT, 2))),
                          (3, sorted(FACE3)),
                          (4, MON_A)):
        seen = set()
        for subset in family:
            derived = HASSE.derivatives(square, subset)
            if derived:
                seen |= {weight(term) for term in derived}
        require(seen == {8 - order},
                "the |S| = %d condition family is weight-homogeneous of "
                "weight %d" % (4 - order, 8 - order))
        condition_weights[order] = sorted(seen)

    # --- multiset extension of the forcing lemma -----------------------
    # Variable coefficients admit repeated directions, so the forcing lemma
    # has to hold over multisets, not just subsets.
    require(all(len(set(term)) == OPERATOR_ORDER for term in A),
            "A is multilinear, so partial_T A = 0 for every repeated T")
    require(len({(variable[1], variable[2]) for variable in SUPPORT})
            == len(SUPPORT),
            "mixed edge variables correspond bijectively to site pairs")
    multiset_classes = {}
    for multiset in combinations_with_replacement(SUPPORT, 2):
        multiset_classes.setdefault(site_degree(multiset),
                                    []).append(multiset)
    total_multisets = sum(len(found) for found in multiset_classes.values())
    blocked = {delta: found for delta, found in multiset_classes.items()
               if max(delta) == 2}
    squares = [found for delta, found in blocked.items()
               if found[0][0] == found[0][1]]
    require(total_multisets == 378 and len(multiset_classes) == 253,
            "the 2-multiset census left 378 multisets in 253 delta-classes")
    require(len(blocked) == 183 and all(len(found) == 1
                                        for found in blocked.values()),
            "singleton delta-classes over MULTISETS: all 183 classes with a "
            "degree-2 site hold exactly one 2-multiset")
    require(len(squares) == 27,
            "the 27 repeated directions are among the blocked classes")

    four_multisets = 0
    four_matchings = 0
    four_blocked = 0
    for multiset in combinations_with_replacement(SUPPORT, OPERATOR_ORDER):
        four_multisets += 1
        if any(max(site_degree(pair)) == 2
               for pair in combinations(multiset, 2)):
            four_blocked += 1
        else:
            four_matchings += 1
    require(four_multisets == 27405,
            "the 4-multiset census over the 27 mixed edges left 27405")
    require(four_matchings == len(MON_A)
            and four_blocked + four_matchings == four_multisets,
            "the multiset forcing lemma partitions the 27405 four-multisets "
            "into 27315 blocked and exactly the 90 perfect matchings")

    # --- where the reduction to constant coefficients holds ------------
    # For a multiset T of mixed edges, wt(T) = |T|.  Weight-shift -4 needs
    # coefficients homogeneous of weight wt(T) - 4, so |T| < 4 is killed
    # (no negative weights) and |T| = 4 is constant.
    edge_multiset_weights = {}
    for order in range(0, OPERATOR_ORDER + 1):
        for multiset in combinations_with_replacement(SUPPORT, order):
            edge_multiset_weights.setdefault(order, set()).add(
                weight(multiset))
    require(all(found == {order}
                for order, found in edge_multiset_weights.items()),
            "wt(T) = |T| for every mixed-edge multiset, so order four is "
            "exactly weight four")
    require(edge_multiset_weights[OPERATOR_ORDER] == {U_WEIGHT},
            "only order four attains the weight that a unit source needs")

    # --- and where it stops ---------------------------------------------
    # The collapse needs wt(T) <= 4 across the support.  Coefficients of
    # weight w > 0 form a NONZERO space, so any T with wt(T) >= 5 keeps
    # genuinely variable coefficients.  Two independent ways to reach
    # wt(T) >= 5: order five in edges, or order two once u is admitted.
    weight_one_space = [variable for variable in all_variables
                        if weight((variable,)) == 1]
    require(len(weight_one_space) == 54,
            "the weight-one coefficient space is nonzero (54 edge "
            "variables), so weight-shift -4 does not force constants above "
            "weight four")
    order_five_weight = weight(tuple(SUPPORT[:5]))
    require(order_five_weight == 5,
            "an order-five edge multiset has weight five, one above the "
            "constant-coefficient threshold")
    u_pair_weight = weight((HASSE.HOMOGENIZING_U, SUPPORT[0]))
    require(u_pair_weight == U_WEIGHT + 1 == 5,
            "an order-two multiset containing u already has weight five, so "
            "admitting u breaks the collapse at order two")
    require(weight((HASSE.HOMOGENIZING_U,)) == U_WEIGHT == OPERATOR_ORDER,
            "the single direction u already carries the full unit weight at "
            "order one, which is why the hybrid class is not decided here")

    return {
        "weight_of_u": U_WEIGHT,
        "generator_weights": [4, 4],
        "square_generator_weight": 8,
        "condition_family_weights": sorted(condition_weights.items()),
        "two_multisets": total_multisets,
        "two_multiset_classes": len(multiset_classes),
        "blocked_multiset_classes": len(blocked),
        "repeated_direction_classes": len(squares),
        "four_multisets": four_multisets,
        "four_multisets_blocked": four_blocked,
        "four_multisets_surviving": four_matchings,
        "weight_one_coefficient_space": len(weight_one_space),
        "order_five_weight": order_five_weight,
        "u_pair_weight": u_pair_weight,
        "variables_in_ring": len(all_variables),
        "closes": (
            "order-four operators in the mixed edge directions with "
            "ARBITRARY polynomial coefficients, via weight splitting plus "
            "the multiset forcing lemma"
        ),
        "does_not_close": (
            "any support containing a direction multiset of weight >= 5 -- "
            "order five and above in edge variables, and order two and "
            "above once u (weight 4) is admitted -- because there the "
            "weight-shift -4 coefficients are homogeneous of positive "
            "weight and the reduction to constant coefficients fails"
        ),
    }


# --------------------------------------------------------------------

def audit():
    generator = generator_level()
    ideal = ideal_level()
    weights = weight_reduction()

    geometry_sha256 = content_hash([
        MON_A,
        sorted(B),
        SUPPORT,
        sorted((term, str(value)) for term, value in A.items()),
        sorted((repr(term), str(value)) for term, value in B.items()),
    ])

    ledger = {
        "model": (
            "fourth-Hasse bounded h=3 direct-free model, word m8=01211222, "
            "A = H_MIXED, B = H_PURE - u, I = (A, B)"
        ),
        "operator_class": (
            "constant-coefficient order-four operators D = sum_M c_M "
            "partial_M in the 27 mixed edge directions"
        ),
        "generator_level": generator,
        "ideal_level": ideal,
        "weight_reduction": weights,
        "generator_level_verdict": "FEASIBLE, proved over Q",
        "ideal_level_verdict": "INFEASIBLE, proved over Q",
        "proof_status": {
            "machine_verified_over_Q": (
                "every census, rank, identity, certificate and weight "
                "statement reported in this ledger, by exact rational "
                "arithmetic"
            ),
            "hand_proved_over_machine_verified_inputs": [
                "the reduction D(I^2) subseteq I <=> E_S[G] in I for all "
                "|S| <= 4 (Leibniz plus upward induction on squarefree "
                "mixed test monomials; note section 2.1)",
                "the forcing lemma c_M = 0 for every non-matching support "
                "(multidegree splitting of E_S[A^2] against the zero-site "
                "invisibility of (A); note section 2.3)",
                "the weight-splitting reduction of variable-coefficient "
                "operators to their weight-shift -4 part (note section 3.1)",
            ],
            "status": (
                "research reduction until independently audited; the three "
                "steps above are proofs on paper whose every input is "
                "checked here, not machine-checked theorems"
            ),
        },
        "modular_status": (
            "every rank is established over Q by exact rational Gauss-Jordan; "
            "the mod 1009 / 1013 / 1019 ranks are redundant cross-checks and "
            "carry no independent weight"
        ),
        "geometry_sha256": geometry_sha256,
        "theorem": (
            "D = (1/90) sum_{M in mon(A)} partial_M satisfies sum_M c_M Q_M = "
            "(26/15) A with unit trace, D(A) = 1, D(AB) = B, D(B^2) = 0, and "
            "alpha = 26/15 is forced by K.1 = 156.1; but no constant-"
            "coefficient order-four operator in the mixed edge directions "
            "satisfies D(I^2) subseteq I with unit trace, because the "
            "site-multidegree forcing lemma confines supp(c) to mon(A) and "
            "the 195 disjoint-pair |S| = 2 conditions then have full local "
            "rank, forcing c = 0"
        ),
        "scope": (
            "closes order-four mixed-edge operators at ideal level inside "
            "this bounded model, with ARBITRARY polynomial coefficients "
            "(weight splitting reduces them to the constant-coefficient "
            "case decided here); does NOT close any support containing a "
            "direction multiset of weight >= 5 -- order five and above in "
            "edge variables, or order two and above once u is admitted -- "
            "so the hybrid partial_u class and all higher orders remain "
            "open, and the operator route is NOT closed entirely; the "
            "generator-level feasibility is the input the R-linear "
            "prolongation attempt builds on, not a repair; Krenn's "
            "conjecture remains open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 apolarity operator split-verdict ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    generator = ledger["generator_level"]
    ideal = ledger["ideal_level"]
    print("h=3 apolarity operator split verdict: PASS (exact, over Q)")
    print()
    print("GENERATOR LEVEL --", ledger["generator_level_verdict"])
    print("  system:                    %d unknowns x %d equations"
          % (generator["cross_terms_nonzero"], generator["quartic_equations"]))
    print("  site-multidegree blocks:    %d (only the 1^8 block, size %d, "
          "meets A)"
          % (generator["multidegree_blocks"],
             generator["one_eight_block_size"]))
    print("  K: diag %d, off-diag %s, row sum %d, rank %d"
          % (generator["K_diagonal"], generator["K_off_diagonal_values"],
             generator["K_row_sum"], generator["K_rank"]))
    print("  D = (1/90) A(partial): alpha forced = %s, A(partial)(A^2) = %s A"
          % (generator["alpha_forced"], generator["apolar_square_multiple"]))
    print("  single selections failing:  %d / %d (the 15 audit selections "
          "included)"
          % (generator["single_selections_failing"],
             generator["hafnian_monomials"]))
    print("  A squarefree (line gcd degrees %s) => point-evaluation dual "
          "is complete" % generator["squarefree_line_gcd_degrees"])
    print("  Farkas certificates: %d (156 . 1^T mu = 90 forces 1^T mu = %s)"
          % (generator["farkas_certificate_exists"],
             generator["forced_dual_trace"]))
    print()
    print("IDEAL LEVEL --", ledger["ideal_level_verdict"])
    print("  forcing lemma: %d singleton delta-classes kill %d of %d supports"
          % (ideal["shared_site_delta_classes"],
             ideal["supports_killed_by_forcing"],
             ideal["supports_killed_by_forcing"]
             + ideal["supports_surviving"]))
    print("  live |S|=2 conditions:      %d, local shapes %s"
          % (ideal["live_conditions"], ideal["local_shape_counts"]))
    print("  pairing certificates:       %d / 90 (supports %s, %d "
          "single-monomial)"
          % (ideal["pairing_certificates"], ideal["certificate_support_range"],
             ideal["single_monomial_certificates"]))
    print("  witness M (site pairs %s): m* = %s, scale %s, readings %s"
          % (ideal["witness_site_pairs"], ideal["witness_monomial"],
             ideal["witness_scale"], ideal["witness_readings"]))
    print("  assembled system:           %s, rank %d over Q, mod-p %s"
          % (ideal["equations_by_layer"], ideal["assembled_rank_over_Q"],
             ideal["assembled_rank_mod_p"]))
    print("  forced trace:               %s (unit trace impossible)"
          % ideal["forced_trace"])
    print()
    weights = ledger["weight_reduction"]
    print("WEIGHT SPLITTING -- variable coefficients at order four")
    print("  generators weight-4, I^2 weight-8; condition families %s"
          % weights["condition_family_weights"])
    print("  multiset forcing: %d blocked classes of %d; %d four-multisets "
          "split %d blocked / %d matchings"
          % (weights["blocked_multiset_classes"],
             weights["two_multiset_classes"], weights["four_multisets"],
             weights["four_multisets_blocked"],
             weights["four_multisets_surviving"]))
    print("  CLOSES:", weights["closes"])
    print("  STOPS AT:", weights["does_not_close"])
    print()
    print("geometry sha256:", ledger["geometry_sha256"])
    print("K content sha256:", generator["K_content_sha256"])
    print("certificate content sha256:", ideal["certificate_content_sha256"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
