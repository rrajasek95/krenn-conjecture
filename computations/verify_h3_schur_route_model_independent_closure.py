#!/usr/bin/env python3
"""The h=3 marked two-chart Schur comparison, closed for DERIVED material.

Model: the h=3 direct-free packet of
`verify_h3_direct_free_literal_four_face_full_nine_no_go.py` -- eight sites
x = 0, D = (1,2,3,4,5), p = 6, q = 7, r = 3 (r is an ODD site), marked odd
word m = 12112 -- run at BOTH specialisations of the p--r block:

    A_pr = 0     the DIRECT-FREE model, 90 of the 105 matchings survive;
    A_pr free    the TILTED model, all 105 survive.

`verify_h3_literal_full_nine_schur_polar_no_go.py` proves that the five
marked polar cochains Lambda_v have source-relative connecting matrix I_5,
so no Lambda_v lifts through the literal lower block.  Two escapes were left
open by that no-go and its companions: adjoin more comparison material, or
leave the direct-free specialisation.  This checker closes both, together,
for everything the repo admits as source material.

------------------------------------------------------------------ THE HEART

CHART-BLINDNESS OF THE ORIGINAL COLUMNS.  The repair covector is chart-ODD
and is supported on the FIVE ORIGINAL no-go columns:

    k_v = r_v^{pq} - r_v^{pr}  lies in ker A'',   and
    (Lambda_v T'')(k_v) = 1/2 - (-1/2) = 1 .

Those five rows are chart pairs of ONE global row -- the committed no-go's
own Fact A, re-derived here by calling its audit().  So every row of A'' has
EQUAL entries on each of the five {pq, pr} pairs, and a covector that is
chart-even there kills k_v.  Adjoining a column only APPENDS coordinates, on
which k_v is zero.  Therefore

    k_v stays in ker A'' and (Lambda_v T'')(k_v) stays 1
    under ANY adjunction whatsoever,

so Lambda_v T'' never lies in row(A''): not for DERIVED material, not for
boundary-MISMATCHED pairs, not for outright DECLARED columns.  Both inputs
of the one-line witness survive the tilt because the cap mark a_pq^00
occupies the site p, so no marked matching can also use the p--r edge.

That is the whole argument, and it is deliberately weaker in hypothesis than
it looks.  When every adjoined column additionally satisfies (D-i) below one
gets the STRONGER statement that ALL of row(A'') is chart-even -- measured
as chart-odd dimension 0 in all twelve derived augmentations -- but the
conclusion never uses it.  In the DERIVED augmentations the three readings
"A'' is constant on chart pairs", "k_v in ker A''" and "chart-odd part of
row(A'') has dimension 0" are THREE VIEWS OF ONE construction-forced fact
(the builder appends the same boundary dict twice), and they discriminate
only against a mutation of the builder.  The genuinely discriminating test
is the ADVERSARIAL ADJUNCTION PROBE: the builder is deliberately broken --
chart pairs whose two boundaries DISAGREE, and declared columns whose
boundary is a proper sub-sum of a row that is not a chart class, carrying
arbitrary chart-odd tails -- the chart-odd part of row(A'') is REQUIRED to
come out nonzero, and every verdict is unchanged.

WHAT "DERIVED" MEANS, precisely.  It is not what legitimises the quantifier
above -- that is the support of k_v -- but it is what makes the EXISTENCE
half of the tau story a completed classification rather than a search.  A
source datum is DERIVED iff

  (D-i)  its lower boundary is the literal global row H_w of a target-zero
         colour word w of the fixed eight-site geometry -- or a partition
         class (chart) of that row; and
  (D-ii) its leading tail is a literal iterated polar of that SAME row by
         edge variables, tagged by that chart's own sector labels.

Anything written down independently of a row is DECLARED, and declared
boundaries are inadmissible under the repo's mapping-cylinder exclusions
(`notes/h3-literal-full-nine-schur-polar-no-go.md` section 5;
`notes/n8-chart25-schur-bockstein-dual-lift.md` section 5) -- though by the
strengthening above they are covered anyway, as long as they are ADJOINED
rather than substituted for the original columns.  (D-ii) is what makes the
tau EXISTENCE question finitely decidable at h = 3:

  * homogeneity pins the number of marks.  H_w has edge-degree 4, a k-fold
    polar has edge-degree 4 - k, and the prescribed tails have edge-degree
    2, so k = 2 exactly.  Checked: every one-edge polar has edge-degree 3.
  * RESIDUAL FORCING pins the marking.  Exhaustively over all 17010
    vertex-disjoint two-edge markings -- one DETERMINISTIC RESIDUAL
    COLOURING per marking, the colour freedom being separately swept in
    full by the (b) classification, which forces the word -- a nonzero
    second polar is supported on monomials covering EXACTLY the four
    residual sites.  A prescribed
    2-edge tail therefore forces the marked pair to cover exactly the
    complementary four sites, and the search collapses to 3 matchings x 3^4
    colourings per pair -- run in full here.
  * the CAP family cover(marks) = {x, v, p, q} with w restricted to
    D\\{v} equal to m -- 1215 data, 2430 labelled chart columns -- is swept
    EXHAUSTIVELY.  That nothing OUTSIDE it can pair with a Lambda_v is
    corroborated ON INSTANCES ONLY (12 words x 210 markings x 5 sites,
    28 nonzero pairings, 0 outside), never exhaustively.  The closure
    does not rest on that direction.

--------------------------------------------------------- MODEL INDEPENDENCE

The tilt restores the p--r block.  Over all 3^8 = 6561 words the chart split
is uniform in both models and BOTH charts acquire a nonempty direct sector:

    A_pr = 0 :  row 90 = 15 + 75 (pq) = 0 + 90 (pr)
    A_pr free:  row 105 = 15 + 90 (pq) = 15 + 90 (pr)

so the tilt is not cosmetic.  Yet the no-go's marked tail does not move.
Split the marked matchings by their use of the site p:

    A = those using the pq edge,  B = those using the pr edge,  C = neither

(no matching uses both).  Then, as marked tails,

    (pq,direct) = A       (pq,two_star) = B + C
    (pr,direct) = B       (pr,two_star) = A + C

and the direct-free model is the same formula with B deleted.  Hence
TILTED - DIRECTFREE = (0, B, B, 0): the tilt injects B into exactly the two
sectors the no-go's ambient V does not have.  A closed form for B is proved
and machine-checked on 12180 (word, marking) pairs, and

    (pq,direct) - (pr,two_star) = A - (A + C) = -C

never contains B at all.  For the no-go's own marking (a_xv^00, a_pq^00) the
cap mark OCCUPIES p, so B = 0 identically: exhaustively over all 6561 x 5 =
32805 (word, site) data the four-sector marked profile is BIT-IDENTICAL
between the two models, and the tilt-only sector is empty in every one.  The
tilted connecting matrix under the no-go's own normalisation is therefore
still exactly I_5; every chart-ODD four-sector normalisation gives an
invertible diagonal, and only the chart-EVEN one gives 0 -- which the lower
layer excludes, since it forces (a + b) G_v = 0 with G_v the row's own
(105-term, nonzero) boundary.

------------------------------------------------------- THE TAU STORY: EXISTS
------------------------------------------------------- AND IS INERT

An UNAUDITED SCRATCH DERIVATION (scratchpad/o3map/, spec S10, UNCOMMITTED,
cited as motivation only) prescribes, for the FULL two-term block d_c, ten
extra source columns tau_{uv} -- one per unordered pair of odd sites --
whose leading tails are the Q-block entries of d_c at the single word row
m.  Nothing here imports it: d_c is rebuilt from the committed base
checker, the tails are read off its Q-block and identified independently
with the face hafnian, and the negative result above does not use it.
Those tails are the four-site face hafnians Haf({x} u D\\{u,v}); they are
x-BEARING, while the no-go's tails h_v = Haf(D\\{v}) are x-FREE.

  EXISTENCE, DERIVED.  Candidate (a) -- the no-go's own marking at other
  words -- is closed with a certificate: all 405 nonzero swept tails are
  x-free, so none can even meet a tau monomial.  Candidate (b) -- other
  markings -- SUCCEEDS, and the solution set is classified completely:
  2430 residual-forced candidates, 2106 solutions, splitting CAP 810 /
  CROSS 1296 (the deficit 1620 - 4 x 81 = 1296 is the direct-free block
  biting on the four pairs containing r).  Exactly the CAP family is
  V-admissible, because differentiating by a_pq forces the pq edge.  After
  cap normalisation there are nine colour choices per pair; three are named
  -- D1 (ten fresh double-deletion rows), D2 (the single fully-mixed parent
  w* = 01211200, of which each of the five committed no-go rows is a
  one-site reset), D3 (an existing no-go row per pair).  Candidate (c) --
  products and the denominator presentation -- is closed: no tau tail has a
  common edge factor, and the denominator l-block is entirely x-free.

  THE SCRATCH SPEC IS MET.  With the bare no-go source, Hom(d_c, source)
  on the FULL two-term block is 0 per sector.  With the derived tau
  columns adjoined it is 1 per sector, i.e. dimension 2, generated by
  psi_0 supported on the
  single word row m, with the ten Q-columns landing on the tau groups and
  the five l-columns on the h groups, all with coefficient 1.  The lower
  layer then forces a + b = 0 again, with an explicit Q-block certificate:
  27 of the 90 monomials of H_w are divisible by no Q-block cell.

  AND IT IS INERT.  In every one of the twelve named augmentations (four
  derivations x two models, plus the tilted CAP variants), in all nine
  uniform colour choices, and under the alternative single-column
  convention: connecting rank 5, no Lambda_v lifts, chart-odd part of
  row(A'') of dimension 0, and the exact Rouche-Capelli repair system
  INCONSISTENT.  The connecting sub-block is I_5 on the five OLD chart
  squares and identically 0 on the ten tau squares -- the matrix [I_5 | 0].
  The witness equation is indexed by the OLD kernel vector k_v, involves
  only the two h_v columns, contains NO new unknown at all, and reads
  0 = +/-1.  Adjoining material cannot change an equation it does not occur
  in.  (The tilted CAP columns DO pair nonzero with Lambda_v -- checked, and
  required to be nonzero somewhere so that the inertness verdict is tested
  against genuinely chart-sensitive material -- but each is a chart PAIR
  sharing one boundary, so its chart difference is again a kernel vector,
  which is exactly what the lemma covers.)

  A DERIVED CHART-ODD TAIL FORCES BOUNDARY ZERO.  Under the alternative
  convention of one tau column per pair carrying the chart-odd tail
  (e_pq - e_pr) (x) T_{uv}, the boundary is H_w - H_w = 0 BY CONSTRUCTION
  -- a difference of two identical dicts, which can never be nonzero; the
  record is labelled CONVENTION.  What is MEASURED is the consequence:
  the column is literally a rescaled kernel vector and the connecting
  verdict is unchanged (rank 5, no lift).  So a chart-odd placement is
  consistent with a derived boundary -- but only with the boundary ZERO.

--------------------------------------------------------------- WHAT IS NOT
--------------------------------------------------------------- A THEOREM HERE

Fact A -- "the two chart columns of a row share one lower boundary" -- is
TRUE BY CONSTRUCTION once a chart is defined as a partition of one global
row.  It is labelled `CONVENTION` in the ledger and stated as such in the
note.  Its content is not the identity but the provenance: the direct-free
branch is computed through the COMMITTED `BASE.chart_partition`, whose
output is additionally agreed against an independent flag-based split on all
6561 words; the sector tags are imported from the committed rigidity
checker; the committed no-go's own connecting matrix I_5 is re-derived from
its `audit()` here.  What is NOT true by construction, and is computed: the
cardinalities of the split, which differ between the two models and would
change under a different chart definition.  And the one chart definition
under which Fact A genuinely fails -- CONV-X5, dividing each direct monomial
by its chart's own edge -- is run as a flagged probe and REJECTED, because
it collapses the ten columns to rank 10 with zero kernel, so every cochain
lifts VACUOUSLY, IDENTICALLY in the two models.  It is not a tilt effect: it
is a different definition of a chart column, available and rejected already
at A_pr = 0, and it is not the definition used by the committed checkers.

Similarly labelled: `k_v in ker A''` is forced by Fact A (recomputed anyway
from the assembled A''), and the vanishing of the connecting map on the tau
squares follows from x-edge separation (measured independently anyway).

--------------------------------------------------------------- RECONCILIATION

  * `notes/h3-full-nine-connecting-class-rigidity.md`.  Its Facts A--D sweep
    the marking (a_xv^00, a_pq^00) over all 6561 words.  Every tail in that
    swept family is x-FREE; every tau tail is x-BEARING; the supports are
    disjoint (checked).  So the tau adjunction lies OUTSIDE its scope --
    exactly the case its own docstring leaves open, "an operation whose tail
    is NOT a literal chart-labelled source tail".  No contradiction.  But
    the tau columns satisfy the ANALOGUE of its Fact C: their two chart
    copies share one boundary, so every chart-odd tau combination is again
    T''(kappa) for kappa in ker A'' -- verified on 24 exact rational trials.
    Its Fact-B-style condition Lambda . B'' = 0 also survives the
    augmentation, by disjoint support.
  * `notes/h3-denominator-face-decoration-fork.md`.  The fork asks whether
    the denominator face carries a chart-neutral, single-sector, or
    chart-odd decoration, and records that the evidence points chart-odd,
    i.e. toward the escape being OPEN.  The forced chain map does resolve it
    chart-odd (a + b = 0).  This checker then shows the chart-odd cell has
    no DERIVED realisation with nonzero boundary.  So the fork's chart-odd
    branch closes NEGATIVELY for derived material -- it does not close it
    for a declared attaching map, which remains unconstructed.
  * `notes/h3-chart-parity-schur-repair-reduction.md`.  Its mass criterion
    is inherited unchanged; the tau tails carry pq-direct mass 0 on every
    h_v, because their supports are disjoint from every h_v.
  * NAMING COLLISION.  The committed ledger's
    `polar_audit()["required_additional_row"] = "tau_<deleted_site>"` is a
    FIVE-name object (read off the committed ledger here); S10's tau_{uv} is
    a TEN-name object indexed by odd pairs.  Different objects; nothing here
    assumes they coincide.

--------------------------------------------------------------------- SCOPE

CLOSES: the h=3 marked-chart Schur comparison mechanism against ANY
ADJUNCTION to the committed no-go source -- derived, boundary-mismatched or
declared -- at BOTH specialisations A_pr = 0 and A_pr free.

DOES NOT CLOSE: a REBUILT or REPLACED comparison, i.e. one that changes the
five original columns themselves rather than adding to them (adjunction is
closed; replacement is not); the dehomogenised chart-column convention
CONV-X5, which redefines what a chart column's boundary IS -- flagged and
rejected above, since it trivialises both models identically; the
COMPLETENESS direction of the CAP classification, verified on instances
only, though nothing here rests on it; the n = 8 two-chart structure, under
separate live investigation; and every non-Schur route -- Hamilton descent,
chart-26 propagation, the diagonal/pencil lane, and membership.  This closes
ONE mechanism of ONE route.  Krenn's conjecture remains open.

Everything is exact (Fraction / int).  Runtime is fifteen to
twenty seconds depending on the machine.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_LEDGER_SHA256 = (
    "f00ae560ab0df3c7d81ae35856f41d4c02820ab942cb22d4ca12fabd67df0890"
)

COLORS = (0, 1, 2)
SITES = tuple(range(8))

# --------------------------------------------------------------------
# LABEL TAXONOMY.  Every reported item carries exactly one of these.
# --------------------------------------------------------------------
PROVED = "proved (hand argument, all inputs machine-checked here)"
EXHAUSTIVE = "verified-exhaustively (complete finite family swept)"
INSTANCES = "verified-on-instances (named finite subfamily, not complete)"
CONVENTION = (
    "convention: TRUE BY CONSTRUCTION of the chart definition.  The content "
    "is not the identity but that this is the repo's own convention, used by "
    "the committed checkers cited in provenance"
)
CONSEQUENCE = (
    "consequence of a labelled fact above, recomputed independently here so "
    "that a mutation of either input is caught"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_model_independent_base",
    "verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
)
NOGO = load(
    "h3_model_independent_nogo",
    "verify_h3_literal_full_nine_schur_polar_no_go.py",
)
RIGIDITY = load(
    "h3_model_independent_rigidity",
    "verify_h3_full_nine_connecting_class_rigidity.py",
)

X = BASE.X
D = BASE.ODD
P = BASE.P
Q_SITE = BASE.Q_SITE
R_SITE = BASE.R
M = BASE.MIXED_ODD

PQ_PAIR = frozenset((P, Q_SITE))
PR_PAIR = frozenset((P, R_SITE))

# The two sector tags of the no-go's ambient V, taken from the COMMITTED
# rigidity checker rather than re-declared here.
PQD = RIGIDITY.PQ_SECTOR
PRS = RIGIDITY.PR_SECTOR
PQS = ("pq", "two_star")
PRD = ("pr", "direct")
FOUR_SECTORS = (PQD, PQS, PRD, PRS)

PAIRS = tuple(combinations(D, 2))
CAP_EDGE = BASE.edge(P, Q_SITE, 0, 0)
ALL_MATCHINGS = BASE.matchings(SITES)
USES_PQ = tuple(
    any(frozenset(pair) == PQ_PAIR for pair in matching)
    for matching in ALL_MATCHINGS
)
USES_PR = tuple(
    any(frozenset(pair) == PR_PAIR for pair in matching)
    for matching in ALL_MATCHINGS
)
DIRECT_FREE = "direct_free"
TILTED = "tilted"
MODELS = (DIRECT_FREE, TILTED)
W_STAR = tuple([0] + [M[index] for index in range(5)] + [0, 0])


# --------------------------------------------------------------------
# the two models
# --------------------------------------------------------------------

def model_row(model, word):
    """The literal global row of `word`: 90 monomials at A_pr = 0, 105 free."""
    if model == DIRECT_FREE:
        return tuple(BASE.full_nine_polynomial(word))
    terms = tuple(BASE.matching_monomial(matching, word)
                  for matching in ALL_MATCHINGS)
    require(len(set(terms)) == len(terms) == 105,
            "tilted row: the eight-site hafnian lost or collided monomials")
    return terms


def chart_split(model, word, pair):
    """The (direct, two_star) partition classes of ONE global row.

    At A_pr = 0 this is the COMMITTED BASE.chart_partition -- an artifact
    this checker did not author.  At A_pr free it is the same definition
    applied to the 105-term row; that branch is labelled CONVENTION.
    """
    if model == DIRECT_FREE:
        return BASE.chart_partition(word, pair)
    pair = frozenset(pair)
    direct, two_star = [], []
    for matching in ALL_MATCHINGS:
        monomial = BASE.matching_monomial(matching, word)
        if any(frozenset(edge_pair) == pair for edge_pair in matching):
            direct.append(monomial)
        else:
            two_star.append(monomial)
    return tuple(direct), tuple(two_star)


_SPLIT_CACHE = {}


def cached_split(model, word, pair):
    key = (model, word, pair)
    found = _SPLIT_CACHE.get(key)
    if found is None:
        found = chart_split(model, word, pair)
        _SPLIT_CACHE[key] = found
    return found


def sector_profile(model, word, marks):
    """Literal four-sector marked tail, each sector differentiated on its own
    partition class by the committed BASE.sparse_derivative."""
    pq_direct, pq_star = cached_split(model, word, (P, Q_SITE))
    pr_direct, pr_star = cached_split(model, word, (P, R_SITE))
    marks = tuple(marks)
    return (BASE.sparse_derivative(pq_direct, marks),
            BASE.sparse_derivative(pq_star, marks),
            BASE.sparse_derivative(pr_direct, marks),
            BASE.sparse_derivative(pr_star, marks))


def nogo_word(deleted_site):
    word = [0] * 8
    for site in D:
        if site != deleted_site:
            word[site] = M[site - 1]
    return tuple(word)


def nogo_marks(deleted_site):
    return (BASE.edge(X, deleted_site, 0, 0), CAP_EDGE)


def h_face(deleted_site):
    colours = tuple(M[site - 1] for site in D if site != deleted_site)
    return {monomial: 1
            for monomial in BASE.face_hafnian(deleted_site, colours)}


def face_hafnian_on(sites, word):
    out = {}
    for matching in BASE.matchings(tuple(sorted(sites))):
        key = tuple(sorted(BASE.edge(a, b, word[a], word[b])
                           for a, b in matching))
        out[key] = out.get(key, 0) + 1
    return out


def x_edges(monomial):
    return tuple(edge for edge in monomial if edge[0] == X or edge[1] == X)


def word_text(word):
    return "".join(map(str, word))


# --------------------------------------------------------------------
# exact rational linear algebra
# --------------------------------------------------------------------

def row_reduce(rows, width):
    """Gauss-Jordan over Q.  Returns (reduced rows, pivot columns)."""
    work = [[Q(entry) for entry in row] for row in rows]
    pivots = []
    rank = 0
    for column in range(width):
        chosen = None
        for index in range(rank, len(work)):
            if work[index][column]:
                chosen = index
                break
        if chosen is None:
            continue
        work[rank], work[chosen] = work[chosen], work[rank]
        inverse = Q(1) / work[rank][column]
        work[rank] = [entry * inverse for entry in work[rank]]
        for index in range(len(work)):
            if index != rank and work[index][column]:
                factor = work[index][column]
                work[index] = [a - factor * b
                               for a, b in zip(work[index], work[rank])]
        pivots.append(column)
        rank += 1
        if rank == len(work):
            break
    return work[:rank], pivots


def dense_rank(rows, width):
    if not rows:
        return 0
    return len(row_reduce(rows, width)[1])


def consistent(rows, width):
    """Rouche-Capelli on [coefficients | rhs]: is rank[M] == rank[M|b]?"""
    return width not in row_reduce(rows, width + 1)[1]


def column_matrix(columns):
    keys = sorted({key for column in columns for key in column}, key=repr)
    rows = [[Q(column.get(key, 0)) for column in columns] for key in keys]
    return keys, rows


def nullspace_of_columns(columns):
    """Exact basis of {c : sum_j c_j * columns[j] = 0}, plus rank and rows."""
    width = len(columns)
    keys, rows = column_matrix(columns)
    reduced, pivots = row_reduce(rows, width)
    free = [index for index in range(width) if index not in pivots]
    basis = []
    for index in free:
        vector = [Q(0)] * width
        vector[index] = Q(1)
        for position, pivot in enumerate(pivots):
            vector[pivot] = -reduced[position][index]
        basis.append(tuple(vector))
    return basis, len(pivots), keys, rows


class Sparse:
    """Exact sparse row echelon / nullspace over an ordered variable list."""

    def __init__(self, variables):
        self.variables = list(variables)
        self.index = {name: position
                      for position, name in enumerate(self.variables)}
        self.pivots = {}

    def _reduce(self, row):
        while row:
            hit = None
            for name in row:
                position = self.index[name]
                if position in self.pivots and (hit is None or position < hit):
                    hit = position
            if hit is None:
                return row
            name = self.variables[hit]
            factor = row[name]
            for key, value in self.pivots[hit].items():
                updated = row.get(key, Q(0)) - factor * value
                if updated:
                    row[key] = updated
                else:
                    row.pop(key, None)
        return row

    def add(self, row):
        row = {key: Q(value) for key, value in row.items() if value}
        row = self._reduce(row)
        if not row:
            return False
        position = min(self.index[key] for key in row)
        name = self.variables[position]
        factor = row[name]
        self.pivots[position] = {key: value / factor
                                 for key, value in row.items()}
        return True

    def rank(self):
        return len(self.pivots)

    def nullity(self):
        return len(self.variables) - len(self.pivots)

    def nullspace(self):
        order = sorted(self.pivots)
        for position in range(len(order) - 1, -1, -1):
            row = self.pivots[order[position]]
            for later in order[position + 1:]:
                name = self.variables[later]
                if name in row:
                    factor = row[name]
                    for key, value in self.pivots[later].items():
                        updated = row.get(key, Q(0)) - factor * value
                        if updated:
                            row[key] = updated
                        else:
                            row.pop(key, None)
            self.pivots[order[position]] = row
        free = [position for position in range(len(self.variables))
                if position not in self.pivots]
        basis = []
        for position in free:
            name = self.variables[position]
            vector = {name: Q(1)}
            for pivot, row in self.pivots.items():
                if name in row:
                    vector[self.variables[pivot]] = -row[name]
            basis.append(vector)
        return basis


def tagged(sector, polynomial):
    return {(sector, monomial): Q(value)
            for monomial, value in polynomial.items() if value}


def merged(*vectors):
    out = {}
    for vector in vectors:
        for key, value in vector.items():
            out[key] = out.get(key, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def pairing(vector, cochain):
    return sum((Q(value) * cochain.get(key, Q(0))
                for key, value in vector.items()), Q(0))


def content_hash(blocks):
    """sha256 of the actual computed content, not of its description."""
    hasher = sha256()
    for block in blocks:
        for item in block:
            hasher.update(repr(item).encode("ascii"))
            hasher.update(b";")
        hasher.update(b"|")
    return hasher.hexdigest()


# --------------------------------------------------------------------
# PROVENANCE: the convention is the repo's own
# --------------------------------------------------------------------

def provenance():
    nogo_ledger, nogo_digest = NOGO.audit()
    committed_connecting = [
        [Q(numerator, denominator) for numerator, denominator in row]
        for row in nogo_ledger["connecting_matrix"]
    ]
    identity = [[Q(1) if row == column else Q(0) for column in range(5)]
                for row in range(5)]
    require(committed_connecting == identity,
            "provenance: the committed no-go connecting matrix is not I_5")
    require(nogo_digest == NOGO.EXPECTED_LEDGER_SHA256,
            "provenance: the committed no-go ledger digest moved")
    require(nogo_ledger["lower_rank"] == 5
            and nogo_ledger["lower_kernel_dimension"] == 5,
            "provenance: the committed no-go lower block is not rank 5 / "
            "kernel 5")
    require(sorted(nogo_ledger["lower_terms_per_column"]) == [90],
            "provenance: the committed no-go lower columns are not 90-term")
    require(len(nogo_ledger["schur_lift_exists"]) == 5
            and sum(1 for flag in nogo_ledger["schur_lift_exists"]
                    if flag) == 0,
            "provenance: the committed no-go recorded a Schur lift")
    require((PQD, PRS) == (("pq", "direct"), ("pr", "two_star")),
            "provenance: the committed sector tags moved")
    require(BASE.DIRECT_FREE_PAIR == frozenset((P, R_SITE)),
            "provenance: the direct-free block is no longer {p, r}")
    require(R_SITE in D,
            "provenance: r stopped being an odd site")

    # The naming collision, read off the COMMITTED ledger rather than
    # asserted: polar_audit() names a FIVE-element family tau_<deleted_site>.
    ledger_tau_names = sorted(record["required_additional_row"]
                              for record in BASE.polar_audit())
    require(ledger_tau_names == sorted("tau_%d" % site for site in D),
            "naming collision: the committed ledger's required_additional_row "
            "family is no longer the five-name tau_<deleted_site>")
    require(len(ledger_tau_names) == 5 and len(PAIRS) == 10,
            "naming collision: the ledger's tau family and S10's tau_{uv} "
            "family stopped having 5 and 10 members")
    return {
        "base_checker": (
            "verify_h3_direct_free_literal_four_face_full_nine_no_go.py"),
        "no_go_checker": "verify_h3_literal_full_nine_schur_polar_no_go.py",
        "no_go_ledger_sha256": nogo_digest,
        "rigidity_checker": (
            "verify_h3_full_nine_connecting_class_rigidity.py"),
        "rigidity_checker_declared_digest": (
            RIGIDITY.EXPECTED_LEDGER_SHA256),
        "rigidity_checker_declared_digest_label": (
            "DECLARED CONSTANT copied from the committed module, NOT "
            "re-derived here -- unlike the no-go digest above, which is "
            "recomputed by calling that checker's own audit()"),
        "sector_tags_from_rigidity_checker": [list(PQD), list(PRS)],
        "committed_connecting_matrix": "I_5",
        "committed_lower_rank": nogo_ledger["lower_rank"],
        "committed_lower_kernel_dimension":
            nogo_ledger["lower_kernel_dimension"],
        "committed_schur_lifts": 0,
        "ledger_tau_family": ledger_tau_names,
        "ledger_tau_family_size": len(ledger_tau_names),
        "s10_tau_family_size": len(PAIRS),
        "label": PROVED,
    }


# --------------------------------------------------------------------
# T1 + T2: the exhaustive two-model chart census, and Fact B bit-identity
# --------------------------------------------------------------------

def chart_and_marked_tail_census():
    """One sweep over all 3^8 words.

    T1 (chart-blindness input).  In BOTH models the two charts are partitions
    of ONE global row, with cardinalities
        A_pr = 0 : 90 = 15 + 75 (pq)  and  90 = 0 + 90 (pr)
        A_pr free: 105 = 15 + 90 (pq) and 105 = 15 + 90 (pr).
    The PARTITION property is CONVENTION; the cardinalities are computed.

    T2 (tilt independence of the marked tail).  For the no-go's own marking
    (a_xv^00, a_pq^00) the four-sector marked tail is bit-identical between
    the two models at every one of the 6561 x 5 = 32805 (word, site) data,
    and the tilt-only sector B is empty in every one of them.
    """
    split_signatures = {}
    partition_failures = 0
    bit_identity_cases = 0
    bit_identity_failures = 0
    nonzero_tail_cases = 0
    tilt_only_nonempty = 0
    marked_support = {site: 0 for site in D}
    fused_tails = {}
    cross_checked = 0
    marks_by_site = {site: nogo_marks(site) for site in D}

    for word in product(COLORS, repeat=8):
        monomials = [BASE.matching_monomial(matching, word)
                     for matching in ALL_MATCHINGS]
        tilted_row = set(monomials)
        direct_free_row = {monomial for monomial in monomials
                           if not BASE.contains_direct_free_edge(monomial)}

        tilted_sectors = ([], [], [], [])
        direct_free_sectors = ([], [], [], [])
        for position, monomial in enumerate(monomials):
            uses_pq = USES_PQ[position]
            uses_pr = USES_PR[position]
            tilted_sectors[0 if uses_pq else 1].append(monomial)
            tilted_sectors[2 if uses_pr else 3].append(monomial)
            if uses_pr:
                continue
            direct_free_sectors[0 if uses_pq else 1].append(monomial)
            direct_free_sectors[3].append(monomial)

        committed_pq = BASE.chart_partition(word, (P, Q_SITE))
        committed_pr = BASE.chart_partition(word, (P, R_SITE))
        if (set(committed_pq[0]) != set(direct_free_sectors[0])
                or set(committed_pq[1]) != set(direct_free_sectors[1])
                or set(committed_pr[0]) != set(direct_free_sectors[2])
                or set(committed_pr[1]) != set(direct_free_sectors[3])):
            partition_failures += 1
        if (set(committed_pq[0]) | set(committed_pq[1]) != direct_free_row
                or set(committed_pr[0]) | set(committed_pr[1])
                != direct_free_row
                or set(committed_pq[0]) & set(committed_pq[1])
                or set(committed_pr[0]) & set(committed_pr[1])):
            partition_failures += 1
        if (set(tilted_sectors[0]) | set(tilted_sectors[1]) != tilted_row
                or set(tilted_sectors[2]) | set(tilted_sectors[3])
                != tilted_row
                or set(tilted_sectors[0]) & set(tilted_sectors[1])
                or set(tilted_sectors[2]) & set(tilted_sectors[3])):
            partition_failures += 1

        signature = (
            len(direct_free_row), len(direct_free_sectors[0]),
            len(direct_free_sectors[1]), len(direct_free_sectors[2]),
            len(direct_free_sectors[3]),
            len(tilted_row), len(tilted_sectors[0]), len(tilted_sectors[1]),
            len(tilted_sectors[2]), len(tilted_sectors[3]),
        )
        split_signatures[signature] = split_signatures.get(signature, 0) + 1

        for site in D:
            first, second = marks_by_site[site]
            tilted_pieces = ({}, {}, {}, {})
            direct_free_pieces = ({}, {}, {}, {})
            tilt_only = {}
            for position, monomial in enumerate(monomials):
                if first not in monomial or second not in monomial:
                    continue
                remainder = list(monomial)
                remainder.remove(first)
                remainder.remove(second)
                key = tuple(sorted(remainder))
                uses_pq = USES_PQ[position]
                uses_pr = USES_PR[position]
                tilted_pieces[0 if uses_pq else 1][key] = (
                    tilted_pieces[0 if uses_pq else 1].get(key, 0) + 1)
                tilted_pieces[2 if uses_pr else 3][key] = (
                    tilted_pieces[2 if uses_pr else 3].get(key, 0) + 1)
                if uses_pr:
                    tilt_only[key] = tilt_only.get(key, 0) + 1
                    continue
                direct_free_pieces[0 if uses_pq else 1][key] = (
                    direct_free_pieces[0 if uses_pq else 1].get(key, 0) + 1)
                direct_free_pieces[3][key] = (
                    direct_free_pieces[3].get(key, 0) + 1)
            bit_identity_cases += 1
            if tilted_pieces != direct_free_pieces:
                bit_identity_failures += 1
            if tilt_only:
                tilt_only_nonempty += 1
            if any(tilted_pieces):
                nonzero_tail_cases += 1
                marked_support[site] += 1
                fused_tails[(word, site)] = tuple(
                    dict(piece) for piece in tilted_pieces)

    require(partition_failures == 0,
            "chart partition: a chart stopped being a partition of one row, "
            "or the committed BASE.chart_partition disagreed with the "
            "flag-based split")
    require(len(split_signatures) == 1,
            "chart cardinality: the chart split is not uniform over the words")
    signature, occurrences = next(iter(split_signatures.items()))
    require(occurrences == 3 ** 8 == 6561,
            "chart cardinality: the global word sweep changed size")
    require(signature == (90, 15, 75, 0, 90, 105, 15, 90, 15, 90),
            "chart cardinality: the two-model chart split left "
            "90 = 15 + 75 / 0 + 90 and 105 = 15 + 90 / 15 + 90")
    require(bit_identity_cases == 5 * 6561 == 32805,
            "tilt independence: the (word, site) sweep changed size")
    require(bit_identity_failures == 0,
            "tilt independence: a marked four-sector profile differed between "
            "the two models")
    require(tilt_only_nonempty == 0,
            "tilt independence: the tilt-only sector B became nonempty for "
            "the no-go marking")
    require(nonzero_tail_cases == 405 and all(count == 81
                                              for count in
                                              marked_support.values()),
            "vacuity: the marked-tail support is not 5 x 81 = 405 nonzero "
            "instances")

    # Cross-check the fused single-pass tails against the LITERAL
    # sector-by-sector BASE.sparse_derivative on every nonzero instance.
    for (word, site), fused in sorted(fused_tails.items()):
        literal = sector_profile(TILTED, word, marks_by_site[site])
        require(tuple(literal) == fused,
                "fused marked tail: the single-pass four-sector tail differs "
                "from the literal per-sector BASE.sparse_derivative")
        cross_checked += 1
    require(cross_checked == 405,
            "vacuity: the fused/literal cross-check ran on no instances")

    # Fact B, exactly as the committed rigidity checker states it, but now
    # read off the four-sector profile in BOTH models.
    profile_shapes = set()
    for site in D:
        word = nogo_word(site)
        expected = h_face(site)
        for model in MODELS:
            pq_direct, pq_star, pr_direct, pr_star = sector_profile(
                model, word, marks_by_site[site])
            profile_shapes.add((len(pq_direct), len(pq_star),
                                len(pr_direct), len(pr_star)))
            require(pq_direct == expected and pr_star == expected
                    and not pq_star and not pr_direct,
                    "Fact B: the selected polar row lost the (h_v, 0, 0, h_v) "
                    "four-sector profile in model " + model)
    require(profile_shapes == {(3, 0, 0, 3)},
            "Fact B: the selected polar tails are not three-term hafnians in "
            "both sectors")

    return {
        "words_swept": occurrences,
        "direct_free_row_monomials": signature[0],
        "direct_free_pq_split": [signature[1], signature[2]],
        "direct_free_pr_split": [signature[3], signature[4]],
        "tilted_row_monomials": signature[5],
        "tilted_pq_split": [signature[6], signature[7]],
        "tilted_pr_split": [signature[8], signature[9]],
        "distinct_split_signatures": len(split_signatures),
        "partition_failures": partition_failures,
        "chart_is_a_partition_of_one_row": CONVENTION,
        "chart_cardinalities": EXHAUSTIVE,
        "marked_tail_cases": bit_identity_cases,
        "marked_tail_model_differences": bit_identity_failures,
        "tilt_only_sector_nonempty_cases": tilt_only_nonempty,
        "nonzero_marked_tail_instances": nonzero_tail_cases,
        "marked_support_per_site": sorted(marked_support.values()),
        "fused_vs_literal_cross_checks": cross_checked,
        "selected_row_profile": [3, 0, 0, 3],
        "tilt_independence_of_marked_tail": EXHAUSTIVE,
        "census_sha256": content_hash([
            [signature],
            sorted((word_text(word), site,
                    tuple(tuple(sorted(map(repr, piece))) for piece in fused))
                   for (word, site), fused in fused_tails.items()),
        ]),
    }


# --------------------------------------------------------------------
# T3: the ABC decomposition and the closed form of the tilt-only sector B
# --------------------------------------------------------------------

def abc_split(word, marks):
    """A (uses pq), B (uses pr), C (neither) of the marked matchings."""
    first, second = marks
    a, b, c = {}, {}, {}
    for position, matching in enumerate(ALL_MATCHINGS):
        monomial = BASE.matching_monomial(matching, word)
        if first not in monomial or second not in monomial:
            continue
        remainder = list(monomial)
        remainder.remove(first)
        remainder.remove(second)
        key = tuple(sorted(remainder))
        uses_pq = USES_PQ[position]
        uses_pr = USES_PR[position]
        require(not (uses_pq and uses_pr),
                "ABC split: one matching used both p-edges")
        bucket = a if uses_pq else (b if uses_pr else c)
        bucket[key] = bucket.get(key, 0) + 1
    return a, b, c


def add_counts(*polynomials):
    out = {}
    for polynomial in polynomials:
        for key, value in polynomial.items():
            out[key] = out.get(key, 0) + value
    return {key: value for key, value in out.items() if value}


def predicted_B(word, marks):
    """Closed form of the tilt-only sector B (proved; checked below)."""
    marks = tuple(marks)
    cover = set()
    for edge in marks:
        if word[edge[0]] != edge[2] or word[edge[1]] != edge[3]:
            return {}
        cover |= {edge[0], edge[1]}
    if len(cover) != 2 * len(marks):
        return {}
    pr_variable = BASE.edge(P, R_SITE, word[P], word[R_SITE])
    if pr_variable in marks:
        return face_hafnian_on(set(SITES) - cover, word)
    if cover & {P, R_SITE}:
        return {}
    small = face_hafnian_on(set(SITES) - cover - {P, R_SITE}, word)
    return {tuple(sorted(monomial + (pr_variable,))): value
            for monomial, value in small.items()}


def abc_sweep():
    """All 210 vertex-disjoint two-edge site-markings on a named 58-word
    sample: the ABC identity, the closed form of B, and the decisive
    identity (pq,direct) - (pr,two_star) = -C, which never contains B."""
    sample = [nogo_word(site) for site in D]
    sample.append(W_STAR)
    sample.append((0,) * 8)
    for (left, right) in PAIRS:
        word = list(W_STAR)
        word[left] = word[right] = 0
        sample.append(tuple(word))
    state = 20260803
    while len(sample) < 58:
        state = (1103515245 * state + 12345) % (1 << 31)
        digits = []
        value = state
        for _ in range(8):
            digits.append(value % 3)
            value //= 3
        sample.append(tuple(digits))
    sample = list(dict.fromkeys(sample))
    require(len(sample) == 58,
            "ABC sweep: the deterministic word sample is not 58 distinct "
            "words")

    site_markings = [((a, b), (c, d))
                     for (a, b), (c, d)
                     in combinations(combinations(SITES, 2), 2)
                     if len({a, b, c, d}) == 4]
    require(len(site_markings) == 210,
            "ABC sweep: the two-edge vertex-disjoint site-marking count "
            "changed")

    checked = 0
    abc_failures = 0
    closed_form_failures = 0
    tilt_difference_failures = 0
    sensitivity_failures = 0
    nonzero_B = 0
    b_term_counts = {}
    for word in sample:
        for (first_sites, second_sites) in site_markings:
            marks = (BASE.edge(first_sites[0], first_sites[1],
                               word[first_sites[0]], word[first_sites[1]]),
                     BASE.edge(second_sites[0], second_sites[1],
                               word[second_sites[0]], word[second_sites[1]]))
            a, b, c = abc_split(word, marks)
            tilted = sector_profile(TILTED, word, marks)
            direct_free = sector_profile(DIRECT_FREE, word, marks)
            checked += 1
            if tuple(tilted) != (a, add_counts(b, c), b, add_counts(a, c)):
                abc_failures += 1
            if tuple(direct_free) != (a, c, {}, add_counts(a, c)):
                abc_failures += 1
            if predicted_B(word, marks) != b:
                closed_form_failures += 1
            difference = tuple(
                add_counts(left, {key: -value
                                  for key, value in right.items()})
                for left, right in zip(tilted, direct_free))
            if difference != ({}, b, b, {}):
                tilt_difference_failures += 1
            sensitivity = add_counts(
                tilted[0], {key: -value for key, value in tilted[3].items()})
            if sensitivity != {key: -value for key, value in c.items()}:
                sensitivity_failures += 1
            if b:
                nonzero_B += 1
                b_term_counts[len(b)] = b_term_counts.get(len(b), 0) + 1

    require(checked == 58 * 210 == 12180,
            "ABC sweep: the (word, marking) sweep changed size")
    require(abc_failures == 0,
            "ABC identity: a four-sector tail is not (A, B+C, B, A+C) "
            "(tilted) / (A, C, 0, A+C) (direct-free)")
    require(closed_form_failures == 0,
            "closed form of B: the predicted tilt-only sector is wrong")
    require(tilt_difference_failures == 0,
            "tilt difference: TILTED - DIRECTFREE is not (0, B, B, 0)")
    require(sensitivity_failures == 0,
            "decisive identity: (pq,direct) - (pr,two_star) is not -C")
    require(nonzero_B > 0,
            "vacuity: the closed form of B was never exercised on a nonzero "
            "instance")
    require(set(b_term_counts) == {1, 3},
            "closed form of B: the nonzero shapes left {1, 3} terms")

    return {
        "words_in_sample": len(sample),
        "site_markings": len(site_markings),
        "pairs_checked": checked,
        "abc_identity_failures": abc_failures,
        "closed_form_failures": closed_form_failures,
        "tilt_difference_failures": tilt_difference_failures,
        "sensitivity_failures": sensitivity_failures,
        "markings_with_nonzero_B": nonzero_B,
        "nonzero_B_term_counts": sorted(b_term_counts.items()),
        "identity": "TILTED - DIRECTFREE = (0, B, B, 0)",
        "decisive_identity": "(pq,direct) - (pr,two_star) = A - (A + C) = -C",
        "label": EXHAUSTIVE,
        "sweep_scope": INSTANCES,
    }


# --------------------------------------------------------------------
# T4: the second-polar lemma and residual forcing
# --------------------------------------------------------------------

def closed_form_polar(word, marks):
    first, second = marks
    cover = {first[0], first[1], second[0], second[1]}
    if len(cover) != 4:
        return {}
    for edge in marks:
        if word[edge[0]] != edge[2] or word[edge[1]] != edge[3]:
            return {}
        if frozenset((edge[0], edge[1])) == BASE.DIRECT_FREE_PAIR:
            return {}
    out = {}
    for monomial, value in face_hafnian_on(set(SITES) - cover, word).items():
        if BASE.contains_direct_free_edge(monomial):
            continue
        out[monomial] = value
    return out


def second_polar_lemma():
    """Exhaustive over all 17010 vertex-disjoint two-edge markings of the
    direct-free geometry, one deterministic residual colouring each: the
    closed form of the second polar, and the residual-forcing corollary."""
    markings = []
    for quad in combinations(SITES, 4):
        for pairing_ in BASE.matchings(quad):
            (a1, b1), (a2, b2) = pairing_
            for colours in product(COLORS, repeat=4):
                markings.append((
                    BASE.edge(a1, b1, colours[0], colours[1]),
                    BASE.edge(a2, b2, colours[2], colours[3]),
                    quad,
                ))
    require(len(markings) == 70 * 3 * 81 == 17010,
            "second polar: the vertex-disjoint marking census changed")

    mismatches = 0
    cover_failures = 0
    nonzero = 0
    for index, (first, second, quad) in enumerate(markings):
        rest = tuple(site for site in SITES if site not in quad)
        word = [0] * 8
        for edge in (first, second):
            word[edge[0]] = edge[2]
            word[edge[1]] = edge[3]
        for position, site in enumerate(rest):
            word[site] = (position + index) % 3
        word = tuple(word)
        literal = BASE.sparse_derivative(
            BASE.full_nine_polynomial(word), (first, second))
        if literal != closed_form_polar(word, (first, second)):
            mismatches += 1
        if literal:
            nonzero += 1
            covered = set()
            for monomial in literal:
                for edge in monomial:
                    covered |= {edge[0], edge[1]}
            if covered != set(rest):
                cover_failures += 1

    require(mismatches == 0,
            "second polar: the closed form disagrees with the literal "
            "BASE.sparse_derivative")
    require(cover_failures == 0,
            "residual forcing: a nonzero second polar failed to cover exactly "
            "its four residual sites")
    require(nonzero > 0,
            "vacuity: no marking produced a nonzero second polar")

    # arity: the tail degree pins the number of marks to exactly two
    degrees = set()
    row = BASE.full_nine_polynomial(W_STAR)
    single_marks = 0
    for site_pair in combinations(SITES, 2):
        for colours in product(COLORS, repeat=2):
            edge = BASE.edge(site_pair[0], site_pair[1],
                             colours[0], colours[1])
            tail = BASE.sparse_derivative(row, (edge,))
            if tail:
                degrees |= {len(monomial) for monomial in tail}
                single_marks += 1
    require(degrees == {3},
            "arity: a one-edge marked polar did not have edge-degree three")
    require(single_marks > 0,
            "vacuity: no single-edge marking produced a nonzero tail")
    require({len(monomial) for monomial in row} == {4},
            "arity: the global row is not edge-degree four")

    return {
        "vertex_disjoint_markings": len(markings),
        "closed_form_mismatches": mismatches,
        "residual_cover_failures": cover_failures,
        "nonzero_polars": nonzero,
        "global_row_edge_degree": 4,
        "one_edge_tail_edge_degrees": sorted(degrees),
        "one_edge_markings_exercised": single_marks,
        "corollary": (
            "residual forcing: a nonzero second polar is supported on "
            "monomials covering EXACTLY the four residual sites, so a "
            "prescribed 2-edge tail forces the marked pair to cover exactly "
            "the complementary four sites -- which is what makes the "
            "derivation search finite and complete"
        ),
        "label": EXHAUSTIVE,
        "residual_colouring": (
            "one deterministic residual colouring per marking; the residual "
            "colour freedom is separately swept in full by the derivation "
            "classification below"
        ),
    }


# --------------------------------------------------------------------
# T5: the tau spec (S10) and its two constructions
# --------------------------------------------------------------------

def q0_square_coefficient(word, sites):
    out = {}
    for matching in BASE.matchings(tuple(sorted(sites))):
        key = tuple(sorted(BASE.edge(a, b, word[a], word[b])
                           for a, b in matching))
        out[key] = out.get(key, 0) + 1
    return out


def t_q0_coefficient(word, sites):
    out = {}
    for site in sites:
        left, right = sorted(set(sites) - {site})
        key = tuple(sorted((BASE.edge(X, site, 0, word[site]),
                            BASE.edge(left, right, word[left], word[right]))))
        out[key] = out.get(key, 0) + 1
    return out


def build_d_c():
    """The branch-2 inactive leading block d_c(l, Q) = l A + Q t_c B."""
    words = tuple(product(COLORS, repeat=len(D)))
    columns = {}
    for site in D:
        for colour in COLORS:
            column = {}
            face = tuple(other for other in D if other != site)
            for short in words:
                word = {place: short[position]
                        for position, place in enumerate(D)}
                if word[site] != colour:
                    continue
                column[short] = q0_square_coefficient(word, face)
            columns[("l", site, colour)] = column
    for left, right in PAIRS:
        for first, second in product(COLORS, repeat=2):
            column = {}
            rest = tuple(other for other in D if other not in (left, right))
            for short in words:
                word = {place: short[position]
                        for position, place in enumerate(D)}
                if word[left] != first or word[right] != second:
                    continue
                column[short] = t_q0_coefficient(word, rest)
            columns[("Q", left, right, first, second)] = column
    return columns, words


def tau_spec(columns):
    """T_{uv} = the Q-block entry of d_c at the single word row m, and the
    independent identification with the face hafnian of {x} u D\\{u,v}."""
    tails = {}
    keys = {}
    for (left, right) in PAIRS:
        key = ("Q", left, right, M[D.index(left)], M[D.index(right)])
        tails[(left, right)] = dict(columns[key][tuple(M)])
        keys[(left, right)] = key

    face_agreements = 0
    for (left, right) in PAIRS:
        face = (X,) + tuple(site for site in D
                            if site not in (left, right))
        word = [0] * 8
        for site in D:
            word[site] = M[site - 1]
        require(face_hafnian_on(face, tuple(word)) == tails[(left, right)],
                "tau spec: the Q-block entry is not the face hafnian of "
                "{x} u D\\{u,v}")
        face_agreements += 1

    monomials = sorted({monomial for tail in tails.values()
                        for monomial in tail}, key=repr)
    require(len(tails) == 10 and len(monomials) == 30,
            "tau spec: the ten tails no longer span 30 distinct monomials")
    require({value for tail in tails.values() for value in tail.values()}
            == {1},
            "tau spec: a tau coefficient left +1")
    require(sorted({len(tail) for tail in tails.values()}) == [3],
            "tau spec: a tau tail is not a three-term hafnian")
    rank_w = dense_rank(
        [[Q(tails[pair].get(monomial, 0)) for monomial in monomials]
         for pair in PAIRS], len(monomials))
    require(rank_w == 10,
            "tau spec: dim W = span of the ten tails left 10")
    overlaps = sum(1 for first in PAIRS for second in PAIRS
                   if first < second
                   and set(tails[first]) & set(tails[second]))
    require(overlaps == 0,
            "tau spec: two tau tails share a monomial")

    anatomy_failures = 0
    for (left, right), tail in tails.items():
        for monomial in tail:
            incident = x_edges(monomial)
            if len(incident) != 1 or len(monomial) != 2:
                anatomy_failures += 1
                continue
            odd_site = (incident[0][1] if incident[0][0] == X
                        else incident[0][0])
            other = [edge for edge in monomial if edge != incident[0]][0]
            if {odd_site, other[0], other[1]} != set(D) - {left, right}:
                anatomy_failures += 1
    require(anatomy_failures == 0,
            "tau spec: a tau monomial is not (one x-edge)*(one odd-odd edge) "
            "covering exactly D\\{u,v}")

    h_monomials = {monomial for site in D for monomial in h_face(site)}
    x_free_h = sum(1 for monomial in h_monomials if x_edges(monomial))
    x_bearing_tau = sum(1 for tail in tails.values() for monomial in tail
                        if x_edges(monomial))
    require(x_free_h == 0,
            "x-separation: an h_v monomial acquired an x-edge")
    require(x_bearing_tau == 30,
            "x-separation: a tau monomial lost its x-edge")
    require(not (h_monomials & set(monomials)),
            "x-separation: the h_v and tau supports met")

    l_cells, q_cells = set(), set()
    for key, column in columns.items():
        for entry in column.values():
            (l_cells if key[0] == "l" else q_cells).update(entry)
    require(not any(x_edges(monomial) for monomial in l_cells),
            "denominator block: an l-block monomial acquired an x-edge")
    require(all(len(x_edges(monomial)) == 1 for monomial in q_cells),
            "denominator block: a Q-block monomial lost its unique x-edge")
    require(not (set(monomials) & l_cells),
            "candidate (c): a tau monomial entered the denominator l-block")

    common_factors = 0
    for tail in tails.values():
        shared = None
        for monomial in tail:
            shared = (set(monomial) if shared is None
                      else shared & set(monomial))
        if shared:
            common_factors += 1
    require(common_factors == 0,
            "candidate (c): a tau tail became a multiple of an edge variable")

    return tails, keys, {
        "tau_columns": len(tails),
        "distinct_tau_monomials": len(monomials),
        "monomials_per_tail": 3,
        "dim_W": rank_w,
        "pairwise_support_overlaps": overlaps,
        "face_hafnian_agreements": face_agreements,
        "h_v_monomials_with_x_edge": x_free_h,
        "tau_monomials_with_x_edge": x_bearing_tau,
        "l_block_monomials": len(l_cells),
        "q_block_monomials": len(q_cells),
        "tau_monomials_inside_l_block": 0,
        "tau_tails_with_a_common_factor": common_factors,
        "naming_collision": (
            "SCRATCH PROVENANCE: the ten-column spec comes from an "
            "unaudited scratch derivation (scratchpad/o3map/, spec S10, "
            "UNCOMMITTED), cited as motivation only; the tails themselves "
            "are rebuilt here from the committed base checker's d_c and "
            "identified independently with the face hafnian.  "
            "The committed no-go ledger's polar_audit emits "
            "required_additional_row = 'tau_<deleted_site>', a FIVE-name "
            "object indexed by the deleted site (the missing Rees row that "
            "would make h_v a strict full-nine combination).  S10's tau_{uv} "
            "is a TEN-name object indexed by an unordered pair of odd sites "
            "(the missing source column carrying the Q-block entry of d_c).  "
            "These are different objects; the shared letter is a collision "
            "and nothing here assumes they coincide"
        ),
        "label": EXHAUSTIVE,
    }


# --------------------------------------------------------------------
# T6: the derivation classification -- what "DERIVED" quantifies over
# --------------------------------------------------------------------

def derivation_classification(tau_tails):
    """CANDIDATE (a): the no-go's own marking, swept over all 6561 words --
    every tail is x-FREE, so none can meet a tau tail.
    CANDIDATE (b): all markings, finite by residual forcing -- 2430 tested,
    2106 solutions, split CAP 810 / CROSS 1296, of which exactly the CAP
    family is V-admissible.
    """
    tau_monomials = {monomial for tail in tau_tails.values()
                     for monomial in tail}

    # candidate (a): reuse the exhaustive census result -- the 405 nonzero
    # tails are all x-free face hafnians h_v(w|face).
    candidate_a_hits = 0
    candidate_a_instances = 0
    for word in product(COLORS, repeat=8):
        for site in D:
            tail = BASE.sparse_derivative(
                BASE.full_nine_polynomial(word), nogo_marks(site))
            if not tail:
                continue
            candidate_a_instances += 1
            if set(tail) & tau_monomials:
                candidate_a_hits += 1
    require(candidate_a_instances == 405,
            "candidate (a): the swept nonzero tail count left 405")
    require(candidate_a_hits == 0,
            "candidate (a): a bare marked polar met a tau monomial")

    # candidate (b): exhaustive, made finite by residual forcing
    solutions = {pair: [] for pair in PAIRS}
    tested = 0
    for (left, right) in PAIRS:
        quad = tuple(sorted((left, right, P, Q_SITE)))
        for pairing_ in BASE.matchings(quad):
            uses_cap = (P, Q_SITE) in [tuple(sorted(sites))
                                       for sites in pairing_]
            for colours in product(COLORS, repeat=4):
                (a1, b1), (a2, b2) = pairing_
                first = BASE.edge(a1, b1, colours[0], colours[1])
                second = BASE.edge(a2, b2, colours[2], colours[3])
                word = [0] * 8
                for site in D:
                    if site not in (left, right):
                        word[site] = M[D.index(site)]
                for edge in (first, second):
                    word[edge[0]] = edge[2]
                    word[edge[1]] = edge[3]
                word = tuple(word)
                tested += 1
                tail = BASE.sparse_derivative(
                    BASE.full_nine_polynomial(word), (first, second))
                if tail == tau_tails[(left, right)]:
                    solutions[(left, right)].append(
                        (word, (first, second), uses_cap))
    require(tested == 10 * 3 * 81 == 2430,
            "candidate (b): the residual-forced search space changed size")

    cap_solutions = [item for pair in PAIRS for item in solutions[pair]
                     if item[2]]
    cross_solutions = [item for pair in PAIRS for item in solutions[pair]
                       if not item[2]]
    total = len(cap_solutions) + len(cross_solutions)
    require(len(cap_solutions) == 810 and len(cross_solutions) == 1296,
            "candidate (b): the CAP / CROSS solution split left 810 / 1296")
    require(total == 2106,
            "candidate (b): the second-polar solution count left 2106")
    require(sorted({len(solutions[pair]) for pair in PAIRS}) == [162, 243],
            "candidate (b): the per-pair solution counts left {162, 243}")
    pairs_with_r = sum(1 for pair in PAIRS if R_SITE in pair)
    require(pairs_with_r == 4
            and 10 * 2 * 81 - pairs_with_r * 81 == len(cross_solutions),
            "candidate (b): the direct-free deduction 1620 - 4*81 = 1296 "
            "failed")

    # V-admissibility
    admissible = {"CAP": [0, 0], "CROSS": [0, 0]}
    profiles = {}
    for family, items in (("CAP", cap_solutions), ("CROSS", cross_solutions)):
        for word, marks, _uses_cap in items:
            pq_direct, pq_star, pr_direct, pr_star = sector_profile(
                DIRECT_FREE, word, marks)
            good = (bool(pq_direct) and not pq_star and not pr_direct
                    and pr_star == pq_direct)
            admissible[family][0 if good else 1] += 1
            signature = (bool(pq_direct), bool(pq_star),
                         bool(pr_direct), bool(pr_star))
            profiles.setdefault((family, signature), (word, marks))
    require(admissible["CAP"] == [810, 0],
            "V-admissibility: a CAP solution left the no-go's ambient V")
    require(admissible["CROSS"] == [0, 1296],
            "V-admissibility: a CROSS solution entered the no-go's ambient V")

    # the cap-normalised sub-family and its named derivations
    cap_normalised = {}
    for (left, right) in PAIRS:
        for word, marks, uses_cap in solutions[(left, right)]:
            if not uses_cap:
                continue
            cap = [edge for edge in marks
                   if tuple(sorted((edge[0], edge[1]))) == (P, Q_SITE)][0]
            if cap[2] or cap[3]:
                continue
            cap_normalised.setdefault((left, right), []).append((word, marks))
    require(sorted({len(items) for items in cap_normalised.values()}) == [9],
            "cap normalisation: the colour freedom per pair left 9 choices")

    named = {}
    for (left, right), items in cap_normalised.items():
        for word, marks in items:
            colours = (word[left], word[right])
            mixed = (M[D.index(left)], M[D.index(right)])
            if colours == (0, 0):
                named.setdefault("D1", {})[(left, right)] = (word, marks)
            elif colours == mixed:
                named.setdefault("D2", {})[(left, right)] = (word, marks)
            elif colours == (0, mixed[1]):
                named.setdefault("D3", {})[(left, right)] = (word, marks)
            elif colours == (mixed[0], 0):
                named.setdefault("D3p", {})[(left, right)] = (word, marks)
    require(sorted(named) == ["D1", "D2", "D3", "D3p"],
            "named derivations: the D1/D2/D3/D3' family is incomplete")
    require(all(len(named[name]) == 10 for name in named),
            "named derivations: a family lost a pair")
    require(all(named["D2"][pair][0] == W_STAR for pair in PAIRS),
            "D2: the ten tau data do not share the single fully-mixed parent "
            "row w*")
    committed_rows = {tuple(int(digit) for digit in text): site
                      for site, text in BASE.EXPECTED_GLOBAL_ROWS.items()}
    d1_rows = {named["D1"][pair][0] for pair in PAIRS}
    d3_rows = {named["D3"][pair][0] for pair in PAIRS}
    require(len(d1_rows) == 10 and not (d1_rows & set(committed_rows)),
            "D1: the ten double-deletion rows are not ten fresh boundaries")
    require(d3_rows <= set(committed_rows),
            "D3: a row left the committed no-go global rows")
    require(W_STAR not in committed_rows,
            "D2: the fully-mixed parent coincided with a committed no-go row")
    require(all(word != (colour,) * 8
                for name in named for pair in PAIRS
                for colour in COLORS
                for word in (named[name][pair][0],)),
            "source validity: a derived tau row is a PURE (target-1) row")

    return named, {
        "candidate_a_nonzero_tails": candidate_a_instances,
        "candidate_a_tau_hits": candidate_a_hits,
        "candidate_b_tested": tested,
        "candidate_b_solutions": total,
        "cap_solutions": len(cap_solutions),
        "cross_solutions": len(cross_solutions),
        "per_pair_solution_counts": [162, 243],
        "pairs_containing_r": pairs_with_r,
        "cap_v_admissible": admissible["CAP"][0],
        "cap_v_inadmissible": admissible["CAP"][1],
        "cross_v_admissible": admissible["CROSS"][0],
        "cross_v_inadmissible": admissible["CROSS"][1],
        "profile_signatures": sorted(
            [family, list(signature)]
            for (family, signature) in profiles),
        "cap_normalised_per_pair": 9,
        "named_derivations": sorted(named),
        "d1_distinct_rows": len(d1_rows),
        "d2_parent_row": word_text(W_STAR),
        "d3_rows_are_committed_no_go_rows": len(d3_rows),
        "label": EXHAUSTIVE,
        "derived_quantifier": (
            "A source datum is DERIVED iff (D-i) its lower boundary is the "
            "literal global row H_w of a target-zero colour word w of the "
            "fixed eight-site geometry, or a partition class (chart) of that "
            "row, and (D-ii) its leading tail is a literal iterated polar of "
            "that SAME row by edge variables, tagged by that chart's own "
            "sector labels.  Anything written down independently of a row is "
            "DECLARED and inadmissible by the repo's mapping-cylinder "
            "exclusions.  Completeness at h=3: (D-ii) with a 2-edge tail "
            "forces exactly two marks by homogeneity; residual forcing then "
            "makes the marking search finite; both are swept exhaustively"
        ),
    }


# --------------------------------------------------------------------
# T7: the augmented complexes and the universal chart-blindness lemma
# --------------------------------------------------------------------

def chart_tail(chart, profile):
    pq_direct, pq_star, pr_direct, pr_star = profile
    if chart == "pq":
        return merged(tagged(PQD, pq_direct), tagged(PQS, pq_star))
    return merged(tagged(PRD, pr_direct), tagged(PRS, pr_star))


def lambda_cochain(deleted_site, weights):
    out = {}
    for monomial in h_face(deleted_site):
        for sector, weight in zip(FOUR_SECTORS, weights):
            if weight:
                out[(sector, monomial)] = Q(weight, 6)
    return out


NORMALISATIONS = (
    ("A pq-direct - pr-two_star [the no-go's own]", (1, 0, 0, -1)),
    ("B pq-direct - pr-direct", (1, 0, -1, 0)),
    ("C pq-two_star - pr-two_star", (0, 1, 0, -1)),
    ("D pq-total - pr-total", (1, 1, -1, -1)),
    ("E pq-direct + pr-two_star [chart-EVEN]", (1, 0, 0, 1)),
)


def cap_representatives():
    """The three cover-{x,v,p,q} marking patterns at the cap-normalised word,
    for each deletion site.  Pattern (a) IS the no-go's own column."""
    out = []
    for site in D:
        word = nogo_word(site)
        for name, sites in (("a", ((X, site), (P, Q_SITE))),
                            ("b", ((X, P), (site, Q_SITE))),
                            ("c", ((X, Q_SITE), (site, P)))):
            (a1, b1), (a2, b2) = sites
            marks = (BASE.edge(a1, b1, word[a1], word[b1]),
                     BASE.edge(a2, b2, word[a2], word[b2]))
            out.append((site, name, word, marks))
    return out


def build_augmented(model, tau_derivation, with_cap, tau_tails):
    names, lowers, tails = [], [], []
    for site in D:
        word = nogo_word(site)
        profile = sector_profile(model, word, nogo_marks(site))
        row = {monomial: 1 for monomial in model_row(model, word)}
        for chart in ("pq", "pr"):
            names.append(("h", site, chart))
            lowers.append(dict(row))
            tails.append(chart_tail(chart, profile))
    if tau_derivation is not None:
        for (left, right) in PAIRS:
            word, marks = tau_derivation[(left, right)]
            require(all(word != (colour,) * 8 for colour in COLORS),
                    "source validity: a derived tau row is a PURE row")
            profile = sector_profile(model, word, marks)
            require(profile[0] == tau_tails[(left, right)]
                    and profile[3] == tau_tails[(left, right)]
                    and not profile[1] and not profile[2],
                    "derived tau column: the prescribed sector profile "
                    "(T_uv, 0, 0, T_uv) was lost in model " + model)
            row = {monomial: 1 for monomial in model_row(model, word)}
            for chart in ("pq", "pr"):
                names.append(("tau", (left, right), chart))
                lowers.append(dict(row))
                tails.append(chart_tail(chart, profile))
    if with_cap:
        for site, pattern, word, marks in cap_representatives():
            if pattern == "a":
                continue
            profile = sector_profile(model, word, marks)
            row = {monomial: 1 for monomial in model_row(model, word)}
            for chart in ("pq", "pr"):
                names.append(("cap", (site, pattern), chart))
                lowers.append(dict(row))
                tails.append(chart_tail(chart, profile))
    return names, lowers, tails


def analyse_augmentation(model, names, lowers, tails, label):
    width = len(names)
    require(width % 2 == 0, "augmentation: columns do not come in chart pairs")
    basis, rank_a, keys, rows = nullspace_of_columns(lowers)
    require(rank_a + len(basis) == width,
            "augmentation: rank-nullity failed")

    # Fact A on the augmentation: consequence of (D-i), recomputed.
    chart_blind = sum(1 for index in range(0, width, 2)
                      if lowers[index] != lowers[index + 1])
    require(chart_blind == 0,
            "chart-blindness: a chart pair stopped sharing one lower boundary")

    squares = []
    for index in range(0, width, 2):
        vector = [Q(0)] * width
        vector[index], vector[index + 1] = Q(1), Q(-1)
        squares.append(tuple(vector))
    escaped = 0
    for vector in squares:
        image = {}
        for position, scalar in enumerate(vector):
            if not scalar:
                continue
            for monomial, value in lowers[position].items():
                image[monomial] = image.get(monomial, Q(0)) + scalar * value
        if any(image.values()):
            escaped += 1
    require(escaped == 0,
            "chart squares: a chart difference left ker A''")

    kinds = [names[2 * index][0] for index in range(width // 2)]
    require(kinds[:5] == ["h"] * 5,
            "augmentation: the five no-go chart pairs are not the first five")
    lam = {site: lambda_cochain(site, NORMALISATIONS[0][1]) for site in D}
    connecting = []
    old_block = []
    tau_block = []
    cap_block = []
    for site in D:
        values = [pairing(tail, lam[site]) for tail in tails]
        connecting.append([sum((values[index] * vector[index]
                                for index in range(width)), Q(0))
                           for vector in basis])
        row_by_kind = {"h": [], "tau": [], "cap": []}
        for position, vector in enumerate(squares):
            row_by_kind[kinds[position]].append(
                sum((values[index] * vector[index]
                     for index in range(width)), Q(0)))
        old_block.append(row_by_kind["h"])
        tau_block.append(row_by_kind["tau"])
        cap_block.append(row_by_kind["cap"])
    connecting_rank = dense_rank([list(row) for row in connecting],
                                 len(basis))
    identity = [[Q(1) if row == column else Q(0) for column in range(5)]
                for row in range(5)]
    require(connecting_rank == 5,
            "connecting map: the augmented connecting rank left 5")
    require(old_block == identity,
            "connecting map: the sub-block on the five OLD chart squares is "
            "not I_5")
    require(not any(any(row) for row in tau_block),
            "connecting map: a Lambda_v saw a tau chart square")
    cap_nonzero = sum(1 for row in cap_block for entry in row if entry)

    # Schur lift test: is Lambda_v . T'' in row(A'') ?
    base_rank = dense_rank([list(row) for row in rows], width)
    lifts = 0
    for site in D:
        values = [pairing(tail, lam[site]) for tail in tails]
        if dense_rank([list(row) for row in rows] + [values],
                      width) == base_rank:
            lifts += 1
    require(lifts == 0,
            "Schur lift: a polar cochain acquired a lift through the lower "
            "block")

    # the chart-odd part of row(A'') is zero -- the universal lemma, measured
    odd_rows = []
    for row in rows:
        odd_rows.append([row[index] - row[index + 1]
                         for index in range(0, width, 2)])
    odd_rank = dense_rank(odd_rows, width // 2)
    require(odd_rank == 0,
            "universal lemma: row(A'') acquired a chart-odd covector")

    # the one-line witness, computed
    witness = []
    for site in D:
        values = [pairing(tail, lam[site]) for tail in tails]
        witness.append(sum((values[index] * squares[site - 1][index]
                            for index in range(width)), Q(0)))
    require(witness == [Q(1)] * 5,
            "one-line witness: (Lambda_v T'')(k_v) left 1")

    # REPAIR TEST -- exact Rouche-Capelli on corrections drawn from the NEW
    # ambient coordinates only.
    old_coordinates = {key for tail in tails[:10] for key in tail}
    new_coordinates = sorted(
        {key for tail in tails[10:] for key in tail} - old_coordinates,
        key=repr)
    index_of = {key: position
                for position, key in enumerate(new_coordinates)}
    feasible = 0
    witness_equation = None
    for site in D:
        matrix = []
        for vector in basis:
            equation = [Q(0)] * len(new_coordinates)
            constant = Q(0)
            for position, scalar in enumerate(vector):
                if not scalar:
                    continue
                for key, value in tails[position].items():
                    constant += scalar * value * lam[site].get(key, Q(0))
                    if key in index_of:
                        equation[index_of[key]] += scalar * value
            matrix.append(equation + [-constant])
            if (site == D[0] and witness_equation is None
                    and constant and not any(equation)):
                witness_equation = {
                    "kernel_vector_support": [
                        str(names[position]) for position in range(width)
                        if vector[position]],
                    "reads": "0 = " + str(-constant),
                    "new_unknowns_in_this_equation": sum(
                        1 for entry in equation if entry),
                }
        if consistent(matrix, len(new_coordinates)):
            feasible += 1
    require(feasible == 0,
            "repair test: a correction drawn from the NEW material cancelled "
            "I_5")
    require(new_coordinates,
            "vacuity: the augmentation contributed no new ambient coordinate")
    require(witness_equation is not None,
            "repair test: no explicit inconsistent witness equation was found")
    require(witness_equation["new_unknowns_in_this_equation"] == 0,
            "repair test: the witness equation acquired a new unknown")
    require(witness_equation["reads"] in ("0 = 1", "0 = -1"),
            "repair test: the witness equation does not read 0 = +/-1")

    # tail side: Lambda_v is identically zero on every new coordinate
    tail_side = sum(1 for site in D for key in new_coordinates
                    if lam[site].get(key))
    require(tail_side == 0,
            "repair test (tail side): a Lambda_v met a new coordinate")

    tail_rank = None
    coordinates = sorted({key for tail in tails for key in tail}, key=repr)
    tail_rank = dense_rank(
        [[tail.get(key, Q(0)) for tail in tails] for key in coordinates],
        width)

    return {
        "augmentation": label,
        "model": model,
        "columns": width,
        "rank_A": rank_a,
        "kernel_dimension": len(basis),
        "rank_T": tail_rank,
        "chart_pairs_with_split_boundary": chart_blind,
        "chart_pairs_with_split_boundary_label": CONVENTION,
        "chart_squares_outside_kernel": escaped,
        "chart_squares_outside_kernel_label": CONSEQUENCE,
        "chart_odd_dimension_of_row_A_label": CONSEQUENCE,
        "connecting_rank": connecting_rank,
        "connecting_on_old_squares": "I_5",
        "connecting_on_tau_squares": "0",
        "connecting_on_tau_squares_label": CONSEQUENCE,
        "connecting_nonzero_entries_on_cap_squares": cap_nonzero,
        "schur_lifts": lifts,
        "chart_odd_dimension_of_row_A": odd_rank,
        "one_line_witness_values": [str(value) for value in witness],
        "new_ambient_coordinates": len(new_coordinates),
        "corrections_feasible": feasible,
        "witness_equation": witness_equation,
        "lambda_values_on_new_coordinates": tail_side,
    }


def tau_derivation_family(rule):
    left_rule, right_rule = rule
    out = {}
    for (left, right) in PAIRS:
        first = 0 if left_rule == "0" else M[D.index(left)]
        second = 0 if right_rule == "0" else M[D.index(right)]
        word = [0] * 8
        for site in D:
            word[site] = M[D.index(site)]
        word[left], word[right] = first, second
        out[(left, right)] = (tuple(word),
                              (BASE.edge(left, right, first, second),
                               CAP_EDGE))
    return out


NAMED_RULES = (
    ("D1 (0,0)", ("0", "0")),
    ("D2 (m,m)", ("m", "m")),
    ("D3 (0,m)", ("0", "m")),
    ("D3' (m,0)", ("m", "0")),
)


def repair_tests(tau_tails):
    records = []
    for model in MODELS:
        for label, rule in NAMED_RULES:
            derivation = tau_derivation_family(rule)
            for with_cap in ((False, True) if model == TILTED else (False,)):
                names, lowers, tails = build_augmented(
                    model, derivation, with_cap, tau_tails)
                records.append(analyse_augmentation(
                    model, names, lowers, tails,
                    label + (" + CAP" if with_cap else "")))
    require(len(records) == 12,
            "repair tests: the augmentation census changed size")
    require({record["connecting_rank"] for record in records} == {5},
            "repair tests: an augmentation lost connecting rank 5")
    require(sum(record["schur_lifts"] for record in records) == 0,
            "repair tests: an augmentation admitted a Schur lift")
    require(sum(record["corrections_feasible"] for record in records) == 0,
            "repair tests: an augmentation admitted a repair correction")
    require({record["chart_odd_dimension_of_row_A"]
             for record in records} == {0},
            "repair tests: row(A'') acquired a chart-odd covector somewhere")
    require(sum(record["connecting_nonzero_entries_on_cap_squares"]
                for record in records) > 0,
            "vacuity: no augmentation exercised a NEW chart square that a "
            "Lambda_v actually sees, so the inertness verdict was never "
            "tested against chart-sensitive material")
    return records


# --------------------------------------------------------------------
# THE STRENGTHENING: the conclusion does not need (D-i) at all
# --------------------------------------------------------------------

def adversarial_adjunction_probe(tau_tails):
    """The no-lift conclusion survives ILLEGAL adjunctions.

    k_v = r_v^{pq} - r_v^{pr} is supported on the FIVE ORIGINAL no-go
    columns.  Every row of A'' has EQUAL entries there, because those five
    rows are chart pairs of ONE row -- the committed no-go's own Fact A,
    re-derived in `provenance`.  Nothing that is merely ADJOINED can either
    remove k_v from ker A'' or change (Lambda_v T'')(k_v) = 1, because
    adjoining a column only appends coordinates on which k_v is zero.

    So the conclusion needs only the committed Fact A on the five original
    columns.  (D-i) upgrades it to the stronger statement that ALL of
    row(A'') is chart-even -- true, but not needed.

    This probe adjoins deliberately ILLEGAL material:

      MISMATCHED  chart pairs whose two boundaries DISAGREE (violating
                  (D-i): they are not two charts of one row);
      DECLARED    columns whose boundary is a proper sub-sum of a row that
                  is NOT a chart partition class, carrying an arbitrary
                  chart-odd tail written down independently of any row.

    Global chart-blindness is DESTROYED -- the chart-odd part of row(A'')
    is REQUIRED to be nonzero here, which is what makes the probe
    discriminating rather than another view of the builder -- and every
    verdict is nevertheless unchanged.
    """
    records = []
    lam = {site: lambda_cochain(site, NORMALISATIONS[0][1]) for site in D}
    for model in MODELS:
        for rule_label, rule in NAMED_RULES[:2]:
            derivation = tau_derivation_family(rule)
            base_names, base_lowers, base_tails = build_augmented(
                model, derivation, False, tau_tails)
            for variant in ("MISMATCHED", "DECLARED"):
                names = list(base_names[:10])
                lowers = [dict(column) for column in base_lowers[:10]]
                tails = [dict(tail) for tail in base_tails[:10]]
                for position, (left, right) in enumerate(PAIRS):
                    index = 10 + 2 * position
                    row = dict(base_lowers[index])
                    ordered = sorted(row, key=repr)
                    if variant == "MISMATCHED":
                        # two charts of DIFFERENT rows: drop one monomial
                        # from the pr copy only.
                        broken = {monomial: value
                                  for monomial, value in row.items()
                                  if monomial != ordered[position]}
                        boundaries = (row, broken)
                        pieces = (dict(base_tails[index]),
                                  dict(base_tails[index + 1]))
                    else:
                        # a DECLARED boundary: a proper sub-sum that is not
                        # a chart partition class, with a tail written down
                        # independently of it.
                        half = ordered[:len(ordered) // 2 + position]
                        declared = {monomial: 1 for monomial in half}
                        boundaries = (declared,
                                      {monomial: 1
                                       for monomial in ordered[position + 1:]})
                        odd = {}
                        for monomial in tau_tails[(left, right)]:
                            odd[(PQD, monomial)] = Q(1)
                            odd[(PRS, monomial)] = Q(-1)
                        pieces = (odd, {key: -value
                                        for key, value in odd.items()})
                    for chart, boundary, piece in (
                            ("pq", boundaries[0], pieces[0]),
                            ("pr", boundaries[1], pieces[1])):
                        names.append((variant.lower(), (left, right), chart))
                        lowers.append(dict(boundary))
                        tails.append(dict(piece))
                width = len(names)
                require(width == 30,
                        "adversarial probe: the illegal augmentation changed "
                        "size")

                mismatched_pairs = sum(
                    1 for index in range(10, width, 2)
                    if lowers[index] != lowers[index + 1])
                require(mismatched_pairs == len(PAIRS),
                        "adversarial probe: the adjoined pairs are not "
                        "boundary-mismatched, so (D-i) was not actually "
                        "violated")

                basis, rank_a, keys, rows = nullspace_of_columns(lowers)
                squares = []
                for index in range(5):
                    vector = [Q(0)] * width
                    vector[2 * index] = Q(1)
                    vector[2 * index + 1] = Q(-1)
                    squares.append(tuple(vector))

                # (i) the FIVE ORIGINAL squares are still in ker A''
                escaped = 0
                for vector in squares:
                    image = {}
                    for place, scalar in enumerate(vector):
                        if not scalar:
                            continue
                        for monomial, value in lowers[place].items():
                            image[monomial] = (image.get(monomial, Q(0))
                                               + scalar * value)
                    if any(image.values()):
                        escaped += 1
                require(escaped == 0,
                        "adversarial probe: an ORIGINAL chart square left "
                        "ker A'' under an illegal adjunction")

                # (ii) row(A'') IS chart-odd overall -- the probe bites --
                #      but chart-EVEN on the five original pairs.
                odd_all = dense_rank(
                    [[row[index] - row[index + 1]
                      for index in range(0, width, 2)] for row in rows],
                    width // 2)
                odd_original = dense_rank(
                    [[row[index] - row[index + 1]
                      for index in range(0, 10, 2)] for row in rows], 5)
                require(odd_all > 0,
                        "adversarial probe: the illegal adjunction failed to "
                        "put a chart-odd covector into row(A''), so the probe "
                        "is not discriminating")
                require(odd_original == 0,
                        "adversarial probe: row(A'') stopped being chart-even "
                        "on the five ORIGINAL columns, which is the only "
                        "input the conclusion uses")

                # (iii) every verdict unchanged
                witness = []
                connecting = []
                old_block = []
                for site in D:
                    values = [pairing(tail, lam[site]) for tail in tails]
                    connecting.append([
                        sum((values[index] * vector[index]
                             for index in range(width)), Q(0))
                        for vector in basis])
                    old_block.append([
                        sum((values[index] * vector[index]
                             for index in range(width)), Q(0))
                        for vector in squares])
                    witness.append(sum((values[index]
                                        * squares[site - 1][index]
                                        for index in range(width)), Q(0)))
                identity = [[Q(1) if a == b else Q(0) for b in range(5)]
                            for a in range(5)]
                connecting_rank = dense_rank(
                    [list(row) for row in connecting], len(basis))
                require(connecting_rank == 5,
                        "adversarial probe: the connecting rank left 5 under "
                        "an illegal adjunction")
                require(old_block == identity,
                        "adversarial probe: the sub-block on the five "
                        "ORIGINAL chart squares is not I_5")
                require(witness == [Q(1)] * 5,
                        "adversarial probe: (Lambda_v T'')(k_v) left 1 under "
                        "an illegal adjunction")

                base_rank = dense_rank([list(row) for row in rows], width)
                lifts = 0
                for site in D:
                    values = [pairing(tail, lam[site]) for tail in tails]
                    if dense_rank([list(row) for row in rows] + [values],
                                  width) == base_rank:
                        lifts += 1
                require(lifts == 0,
                        "adversarial probe: a polar cochain acquired a lift "
                        "under an illegal adjunction")

                old_coordinates = {key for tail in tails[:10] for key in tail}
                new_coordinates = sorted(
                    {key for tail in tails[10:] for key in tail}
                    - old_coordinates, key=repr)
                require(new_coordinates,
                        "vacuity: the illegal adjunction contributed no new "
                        "ambient coordinate")
                index_of = {key: place
                            for place, key in enumerate(new_coordinates)}
                feasible = 0
                probe_witness = None
                for site in D:
                    matrix = []
                    for vector in basis:
                        equation = [Q(0)] * len(new_coordinates)
                        constant = Q(0)
                        for place, scalar in enumerate(vector):
                            if not scalar:
                                continue
                            for key, value in tails[place].items():
                                constant += (scalar * value
                                             * lam[site].get(key, Q(0)))
                                if key in index_of:
                                    equation[index_of[key]] += scalar * value
                        matrix.append(equation + [-constant])
                        if (site == D[0] and probe_witness is None
                                and constant and not any(equation)):
                            probe_witness = {
                                "kernel_vector_support": [
                                    str(names[place])
                                    for place in range(width)
                                    if vector[place]],
                                "reads": "0 = " + str(-constant),
                                "new_unknowns_in_this_equation": 0,
                            }
                    if consistent(matrix, len(new_coordinates)):
                        feasible += 1
                require(feasible == 0,
                        "adversarial probe: an illegal adjunction repaired "
                        "I_5")
                require(probe_witness is not None
                        and probe_witness["reads"] in ("0 = 1", "0 = -1"),
                        "adversarial probe: the inconsistent witness equation "
                        "on k_v was lost")

                records.append({
                    "probe": variant,
                    "model": model,
                    "base_derivation": rule_label,
                    "columns": width,
                    "boundary_mismatched_pairs": mismatched_pairs,
                    "rank_A": rank_a,
                    "kernel_dimension": len(basis),
                    "chart_odd_dimension_of_row_A": odd_all,
                    "chart_odd_dimension_on_original_columns": odd_original,
                    "original_squares_outside_kernel": escaped,
                    "connecting_rank": connecting_rank,
                    "connecting_on_original_squares": "I_5",
                    "one_line_witness_values": [str(value)
                                                for value in witness],
                    "schur_lifts": lifts,
                    "new_ambient_coordinates": len(new_coordinates),
                    "corrections_feasible": feasible,
                    "witness_equation": probe_witness,
                })
    require(len(records) == 8,
            "adversarial probe: the illegal-adjunction census changed size")
    require(min(record["chart_odd_dimension_of_row_A"]
                for record in records) > 0,
            "adversarial probe: some illegal adjunction failed to break "
            "global chart-blindness")
    require({record["connecting_rank"] for record in records} == {5}
            and sum(record["schur_lifts"] for record in records) == 0
            and sum(record["corrections_feasible"]
                    for record in records) == 0,
            "adversarial probe: an illegal adjunction changed a verdict")
    return {
        "records": records,
        "strengthening": (
            "the no-lift conclusion uses ONLY the committed no-go's Fact A on "
            "the five ORIGINAL columns: k_v is supported there, every row of "
            "A'' has equal entries there, and adjoining a column only "
            "appends coordinates on which k_v vanishes.  Hence NO adjunction "
            "-- derived, boundary-mismatched, or outright DECLARED -- can "
            "remove k_v from ker A'' or change (Lambda_v T'')(k_v) = 1.  "
            "(D-i) gives the stronger fact that all of row(A'') is "
            "chart-even; the conclusion does not need it"
        ),
        "label": EXHAUSTIVE,
    }


def uniform_nine(tau_tails):
    """ALL nine uniform cap-normalised colour choices, direct-free model."""
    table = []
    for first in COLORS:
        for second in COLORS:
            derivation = {}
            for (left, right) in PAIRS:
                word = [0] * 8
                for site in D:
                    word[site] = M[D.index(site)]
                word[left], word[right] = first, second
                derivation[(left, right)] = (
                    tuple(word),
                    (BASE.edge(left, right, first, second), CAP_EDGE))
            names, lowers, tails = build_augmented(
                DIRECT_FREE, derivation, False, tau_tails)
            record = analyse_augmentation(
                DIRECT_FREE, names, lowers, tails,
                "uniform (%d,%d)" % (first, second))
            table.append({
                "choice": [first, second],
                "rank_A": record["rank_A"],
                "kernel_dimension": record["kernel_dimension"],
                "connecting_rank": record["connecting_rank"],
                "schur_lifts": record["schur_lifts"],
                "distinct_lower_boundaries": len(
                    {tuple(sorted(column)) for column in lowers}),
            })
    require(len(table) == 9,
            "uniform sweep: the nine cap-normalised choices changed count")
    require({row["connecting_rank"] for row in table} == {5},
            "uniform sweep: a uniform choice lost connecting rank 5")
    require(sum(row["schur_lifts"] for row in table) == 0,
            "uniform sweep: a uniform choice admitted a Schur lift")
    require(len({row["rank_A"] for row in table}) > 1,
            "vacuity: the nine uniform choices gave a single lower rank, so "
            "the sweep exercised nothing")
    return table


def chart_odd_single_column(tau_tails):
    """CONV-T4': ONE tau column per pair carrying the chart-ODD tail.

    Its lower boundary is FORCED to H_w - H_w = 0 by chart-blindness, and the
    column is then literally a rescaled kernel vector.  So a derived chart-odd
    tail is consistent -- but only with the boundary ZERO.
    """
    records = []
    for model in MODELS:
        for label, rule in NAMED_RULES:
            derivation = tau_derivation_family(rule)
            names, lowers, tails = build_augmented(
                model, derivation, False, tau_tails)
            width = len(names)
            reduced_names = list(names[:10])
            reduced_lowers = [dict(column) for column in lowers[:10]]
            reduced_tails = [dict(tail) for tail in tails[:10]]
            nonzero_boundaries = 0
            for index in range(10, width, 2):
                difference = {}
                for monomial in set(lowers[index]) | set(lowers[index + 1]):
                    value = (Q(lowers[index].get(monomial, 0))
                             - Q(lowers[index + 1].get(monomial, 0)))
                    if value:
                        difference[monomial] = value
                if difference:
                    nonzero_boundaries += 1
                odd = merged(tails[index],
                             {key: -value
                              for key, value in tails[index + 1].items()})
                reduced_names.append(("kappa", names[index][1]))
                reduced_lowers.append(difference)
                reduced_tails.append(odd)
            require(nonzero_boundaries == 0,
                    "CONV-T4': a derived chart-odd column acquired a nonzero "
                    "lower boundary")
            basis, rank_a, _keys, _rows = nullspace_of_columns(reduced_lowers)
            lam = {site: lambda_cochain(site, NORMALISATIONS[0][1])
                   for site in D}
            connecting = []
            for site in D:
                values = [pairing(tail, lam[site]) for tail in reduced_tails]
                connecting.append([
                    sum((values[index] * vector[index]
                         for index in range(len(reduced_names))), Q(0))
                    for vector in basis])
            connecting_rank = dense_rank([list(row) for row in connecting],
                                         len(basis))
            require(connecting_rank == 5,
                    "CONV-T4': the chart-odd single-column convention changed "
                    "the connecting verdict")
            # each chart-odd column IS a kernel vector of the augmented A''
            in_kernel = 0
            for index in range(10, len(reduced_names)):
                if not reduced_lowers[index]:
                    in_kernel += 1
            require(in_kernel == 10,
                    "CONV-T4': a chart-odd column is not a kernel vector")
            records.append({
                "model": model,
                "derivation": label,
                "label": CONVENTION,
                "columns": len(reduced_names),
                "chart_odd_columns_with_nonzero_boundary": nonzero_boundaries,
                "chart_odd_columns_in_kernel": in_kernel,
                "rank_A": rank_a,
                "kernel_dimension": len(basis),
                "connecting_rank": connecting_rank,
            })
    require(len(records) == 8,
            "CONV-T4': the census changed size")
    return records


# --------------------------------------------------------------------
# T8: the tilted four-sector normalisations, and the CAP-family census
# --------------------------------------------------------------------

def normalisation_table():
    names, lowers, tails = [], [], []
    for site in D:
        word = nogo_word(site)
        profile = sector_profile(TILTED, word, nogo_marks(site))
        row = {monomial: 1 for monomial in model_row(TILTED, word)}
        for chart in ("pq", "pr"):
            names.append(("h", site, chart))
            lowers.append(dict(row))
            tails.append(chart_tail(chart, profile))
    squares = []
    for index in range(5):
        vector = [Q(0)] * 10
        vector[2 * index], vector[2 * index + 1] = Q(1), Q(-1)
        squares.append(tuple(vector))

    pure_word = (0,) * 8
    pure_columns = []
    for site in D:
        profile = sector_profile(TILTED, pure_word, nogo_marks(site))
        pure_columns.append(merged(chart_tail("pq", profile),
                                   chart_tail("pr", profile)))
    require(all(column for column in pure_columns),
            "vacuity: the pure denominator leading block B' is empty")

    table = []
    for label, weights in NORMALISATIONS:
        lam = {site: lambda_cochain(site, weights) for site in D}
        matrix = []
        for site in D:
            values = [pairing(tail, lam[site]) for tail in tails]
            matrix.append([sum((values[index] * vector[index]
                                for index in range(10)), Q(0))
                           for vector in squares])
        rank_c = dense_rank([list(row) for row in matrix], 5)
        off_diagonal = sum(1 for row in range(5) for column in range(5)
                           if row != column and matrix[row][column])
        annihilates = sum(1 for site in D for column in pure_columns
                          if pairing(column, lam[site]))
        table.append({
            "normalisation": label,
            "connecting_rank": rank_c,
            "diagonal": [str(matrix[index][index]) for index in range(5)],
            "off_diagonal_nonzero_entries": off_diagonal,
            "lambda_B_prime_nonzero_entries": annihilates,
        })
    require(len(table) == 5, "normalisation table: the census changed size")
    first = table[0]
    require(first["connecting_rank"] == 5
            and first["diagonal"] == ["1"] * 5
            and first["off_diagonal_nonzero_entries"] == 0,
            "tilted connecting matrix: the no-go's own normalisation is not "
            "exactly I_5 in the tilted model")
    require(table[-1]["connecting_rank"] == 0,
            "normalisation table: the chart-EVEN normalisation is not "
            "degenerate")
    require(sum(row["lambda_B_prime_nonzero_entries"] for row in table) == 0,
            "normalisation table: a candidate cochain failed to annihilate "
            "the pure denominator block B'")
    require(min(len(column) for column in lowers) == 105,
            "a + b = 0: a tilted lower boundary vanished, so the lower layer "
            "no longer forces the chart-odd parity")
    return table


def cap_family_census():
    """Every derived column that can pair with any Lambda_v: cover(marks) =
    {x, v, p, q} and w restricted to D\\{v} the mixed word m."""
    family = []
    for site in D:
        free_sites = (X, site, P, Q_SITE)
        for colours in product(COLORS, repeat=4):
            word = [0] * 8
            for other in D:
                word[other] = M[other - 1]
            for place, colour in zip(free_sites, colours):
                word[place] = colour
            word = tuple(word)
            for name, sites in (("a", ((X, site), (P, Q_SITE))),
                                ("b", ((X, P), (site, Q_SITE))),
                                ("c", ((X, Q_SITE), (site, P)))):
                (a1, b1), (a2, b2) = sites
                marks = (BASE.edge(a1, b1, word[a1], word[b1]),
                         BASE.edge(a2, b2, word[a2], word[b2]))
                family.append((site, name, word, marks))
    require(len(family) == 5 * 81 * 3 == 1215,
            "CAP family: the exhaustive family size changed")

    census = {}
    pure_rows = 0
    tilt_changed = 0
    nonzero_tails = 0
    lam = {site: lambda_cochain(site, NORMALISATIONS[0][1]) for site in D}
    pairing_histogram = {}
    for site, pattern, word, marks in family:
        if any(word == (colour,) * 8 for colour in COLORS):
            pure_rows += 1
        tilted = sector_profile(TILTED, word, marks)
        direct_free = sector_profile(DIRECT_FREE, word, marks)
        if any(tilted):
            nonzero_tails += 1
        if tuple(tilted) != tuple(direct_free):
            tilt_changed += 1
        key = (pattern,
               tuple(1 if piece else 0 for piece in tilted),
               tuple(1 if piece else 0 for piece in direct_free))
        census[key] = census.get(key, 0) + 1
        value = (pairing(chart_tail("pq", tilted), lam[site])
                 - pairing(chart_tail("pr", tilted), lam[site]))
        pairing_histogram[str(value)] = (
            pairing_histogram.get(str(value), 0) + 1)
    require(pure_rows == 0,
            "CAP family: a pure (target-1) row entered the derived family")
    require(nonzero_tails == 1215,
            "CAP family: a member lost its marked tail")
    require(tilt_changed == 81,
            "CAP family: the tilt-sensitive class left 81 members")
    require(sum(1 for value in pairing_histogram
                if Q(value)) > 0,
            "vacuity: no CAP column paired nonzero with a Lambda_v")

    tilt_sensitive_classes = sorted(
        [list(key[0:1]) + [list(key[1]), list(key[2])], count]
        for key, count in census.items() if key[1] != key[2])
    require(len(tilt_sensitive_classes) == 1,
            "CAP family: the tilt-sensitive class is not unique")

    # bounded corroboration that nothing OUTSIDE the CAP family can pair
    site_markings = [((a, b), (c, d))
                     for (a, b), (c, d)
                     in combinations(combinations(SITES, 2), 2)
                     if len({a, b, c, d}) == 4]
    probe_words = [nogo_word(site) for site in D] + [W_STAR, (0,) * 8]
    state = 987654321
    while len(probe_words) < 12:
        state = (1103515245 * state + 12345) % (1 << 31)
        digits = []
        value = state
        for _ in range(8):
            digits.append(value % 3)
            value //= 3
        probe_words.append(tuple(digits))
    probe_words = list(dict.fromkeys(probe_words))
    hits = 0
    violations = 0
    for word in probe_words:
        for (first_sites, second_sites) in site_markings:
            marks = (BASE.edge(first_sites[0], first_sites[1],
                               word[first_sites[0]], word[first_sites[1]]),
                     BASE.edge(second_sites[0], second_sites[1],
                               word[second_sites[0]], word[second_sites[1]]))
            profile = sector_profile(TILTED, word, marks)
            if not any(profile):
                continue
            pq_tail = chart_tail("pq", profile)
            pr_tail = chart_tail("pr", profile)
            for site in D:
                if not (pairing(pq_tail, lam[site])
                        or pairing(pr_tail, lam[site])):
                    continue
                hits += 1
                cover = {marks[0][0], marks[0][1], marks[1][0], marks[1][1]}
                if not (cover == {X, site, P, Q_SITE}
                        and all(word[other] == M[other - 1]
                                for other in D if other != site)):
                    violations += 1
    require(hits > 0,
            "vacuity: the outside-CAP probe found no nonzero pairing at all")
    require(violations == 0,
            "CAP completeness: a column outside the CAP family paired with a "
            "Lambda_v")

    return {
        "family_size": len(family),
        "pure_rows": pure_rows,
        "members_with_nonzero_tail": nonzero_tails,
        "tilt_sensitive_members": tilt_changed,
        "tilt_sensitive_classes": tilt_sensitive_classes,
        "sector_profile_census": sorted(
            [list(key[0:1]) + [list(key[1]), list(key[2])], count]
            for key, count in census.items()),
        "chart_difference_pairings": sorted(pairing_histogram.items()),
        "probe_words": len(probe_words),
        "probe_site_markings": len(site_markings),
        "probe_nonzero_pairings": hits,
        "probe_outside_cap_family": violations,
        "cap_family_sweep_label": EXHAUSTIVE,
        "completeness_direction_label": INSTANCES,
        "completeness_direction": (
            "that NOTHING OUTSIDE the CAP family can pair with a "
            "Lambda_v is corroborated on instances only (12 words x 210 "
            "markings x 5 sites), never exhaustively.  The closure does "
            "not rest on it: the no-lift conclusion uses only the five "
            "ORIGINAL columns"),
    }


# --------------------------------------------------------------------
# T9: the dehomogenised chart convention -- flagged, and rejected
# --------------------------------------------------------------------

def dehomogenised_probe():
    """CONV-X5.  Divide every DIRECT monomial by its chart's own edge.  Fact A
    then fails BY CONSTRUCTION -- but the collapse is identical in the two
    models, so it is not a tilt effect: it is a different definition of a
    chart column, available and rejected already at A_pr = 0."""
    records = []
    for model in MODELS:
        columns = []
        for site in D:
            word = nogo_word(site)
            for pair in ((P, Q_SITE), (P, R_SITE)):
                reduced = {}
                for monomial in model_row(model, word):
                    hit = [edge for edge in monomial
                           if frozenset((edge[0], edge[1])) == frozenset(pair)]
                    key = monomial
                    if hit:
                        key = tuple(edge for edge in monomial
                                    if edge != hit[0])
                    reduced[key] = reduced.get(key, 0) + 1
                columns.append(reduced)
        fact_a_failures = sum(1 for index in range(5)
                              if columns[2 * index] != columns[2 * index + 1])
        basis, rank_a, _keys, rows = nullspace_of_columns(columns)
        lam = {site: lambda_cochain(site, NORMALISATIONS[0][1]) for site in D}
        names, _lowers, tails = build_augmented(model, None, False, {})
        base_rank = dense_rank([list(row) for row in rows], 10)
        lifts = 0
        for site in D:
            values = [pairing(tail, lam[site]) for tail in tails]
            if dense_rank([list(row) for row in rows] + [values],
                          10) == base_rank:
                lifts += 1
        records.append({
            "model": model,
            "fact_a_failures": fact_a_failures,
            "rank_A": rank_a,
            "kernel_dimension": len(basis),
            "cochains_that_lift": lifts,
        })
    require(len(records) == 2, "CONV-X5 probe: the model census changed size")
    require({record["fact_a_failures"] for record in records} == {5},
            "CONV-X5 probe: the dehomogenised convention did not break Fact A "
            "on all five rows")
    require({record["rank_A"] for record in records} == {10}
            and {record["kernel_dimension"] for record in records} == {0},
            "CONV-X5 probe: the dehomogenised columns are not independent")
    require({record["cochains_that_lift"] for record in records} == {5},
            "CONV-X5 probe: the vacuous lift did not occur in both models")
    require(records[0]["rank_A"] == records[1]["rank_A"]
            and records[0]["kernel_dimension"]
            == records[1]["kernel_dimension"],
            "CONV-X5 probe: the collapse is not identical in the two models")
    return {
        "records": records,
        "status": (
            "CONVENTION, FLAGGED AND REJECTED.  Under CONV-X5 the ten columns "
            "become independent, the kernel is zero, and every cochain lifts "
            "VACUOUSLY -- identically in the tilted and the direct-free "
            "model.  It is therefore not a tilt effect but a different "
            "definition of a chart column, and it is not the definition used "
            "by the committed checkers cited in provenance"
        ),
        "label": CONVENTION,
    }


# --------------------------------------------------------------------
# T10: the tau columns MEET the chain-map repair spec (Hom 0 -> 2)
# --------------------------------------------------------------------

def chain_map_repair_spec(columns, words, tau_tails):
    keys = sorted((key for key in columns if key[0] == "l"), key=repr) + \
        sorted((key for key in columns if key[0] == "Q"), key=repr)
    require(len(keys) == 105,
            "chain map: the d_c column census left 105")
    group_tails = [dict(h_face(site)) for site in D] + \
        [dict(tau_tails[pair]) for pair in PAIRS]
    group_names = ["h_%d" % site for site in D] + \
        ["T_%d%d" % pair for pair in PAIRS]

    def leading_system(tails):
        all_monomials = sorted({monomial for tail in tails
                                for monomial in tail}, key=repr)
        count = len(tails)
        variables = ([("c", key, index) for key in keys
                      for index in range(count)]
                     + [("p", word) for word in words])
        system = Sparse(variables)
        for key in keys:
            by_monomial = {}
            for word, entry in columns[key].items():
                for monomial, value in entry.items():
                    by_monomial.setdefault(monomial, {})[word] = value
            for monomial in set(by_monomial) | set(all_monomials):
                row = {}
                for word, value in by_monomial.get(monomial, {}).items():
                    row[("p", word)] = row.get(("p", word), Q(0)) + Q(value)
                for index in range(count):
                    if monomial in tails[index]:
                        row[("c", key, index)] = (
                            row.get(("c", key, index), Q(0))
                            - Q(tails[index][monomial]))
                system.add(row)
        return system, variables

    bare, bare_variables = leading_system([dict(h_face(site)) for site in D])
    augmented, augmented_variables = leading_system(group_tails)
    require(bare.nullity() == 0,
            "chain map: the BARE no-go source admitted a full-block chain "
            "map, so the repair spec was already met")
    require(augmented.nullity() == 1,
            "chain map: the augmented full-block Hom is not one per sector")

    generator = augmented.nullspace()[0]
    word_weights = {key: value for key, value in generator.items()
                    if key[0] == "p" and value}
    landings = {key: value for key, value in generator.items()
                if key[0] == "c" and value}
    require(set(word_weights) == {("p", tuple(M))},
            "chain map: psi_0 left the single word row m")
    landing_map = {}
    for key, value in landings.items():
        landing_map[str(key[1])] = (group_names[key[2]], str(value))
    require(len(landing_map) == 15,
            "chain map: psi_1 does not land on exactly the 15 distinguished "
            "columns")
    require({name for name, _ in landing_map.values()} == set(group_names),
            "chain map: psi_1 misses a source group")
    require({value for _, value in landing_map.values()} == {"1"},
            "chain map: a psi_1 coefficient left 1")

    # the lower layer forces a + b = 0 again -- a Q-block certificate
    q_cells = set()
    for key in keys:
        if key[0] != "Q":
            continue
        for entry in columns[key].values():
            q_cells |= set(entry)
    certificates = []
    for label, rule in NAMED_RULES[:2]:
        derivation = tau_derivation_family(rule)
        word, _marks = derivation[PAIRS[0]]
        row = BASE.full_nine_polynomial(word)
        unreachable = [monomial for monomial in row
                       if not any(set(cell) <= set(monomial)
                                  for cell in q_cells)]
        require(unreachable,
                "a + b = 0: every H_w monomial became reachable from the "
                "Q-block, so the coefficient equation is not forced")
        certificates.append({
            "derivation": label,
            "pair": list(PAIRS[0]),
            "row_monomials": len(row),
            "monomials_divisible_by_no_Q_cell": len(unreachable),
            "witness": BASE.monomial_text(sorted(unreachable)[0]),
            "coefficient_equation": "(a + b) = 0",
        })

    return {
        "d_c_columns": len(keys),
        "source_groups": len(group_tails),
        "bare_full_block_hom_per_sector": bare.nullity(),
        "augmented_full_block_hom_per_sector": augmented.nullity(),
        "augmented_full_block_hom_total": 2 * augmented.nullity(),
        "unknowns_per_sector": len(augmented_variables),
        "rank": augmented.rank(),
        "psi_0_support": [word_text(key[1]) for key in word_weights],
        "psi_1_landings": len(landing_map),
        "psi_1_map": sorted(landing_map.items()),
        "lower_layer_certificates": certificates,
        "verdict": (
            "the derived tau columns MEET S10's repair spec: the FULL "
            "two-term block d_c admits an R-linear chain map into the "
            "augmented source, of dimension exactly 2, which the bare no-go "
            "source did not (dimension 0); the lower layer then forces "
            "a + b = 0, so the augmented chain map is still chart-ODD"
        ),
        "label": PROVED,
    }


# --------------------------------------------------------------------
# T11: reconciliation with the committed companions
# --------------------------------------------------------------------

def reconciliations(tau_tails):
    swept_monomials = set()
    for word in product(COLORS, repeat=8):
        for site in D:
            tail = BASE.sparse_derivative(
                BASE.full_nine_polynomial(word), nogo_marks(site))
            swept_monomials |= set(tail)
    tau_monomials = {monomial for tail in tau_tails.values()
                     for monomial in tail}
    require(swept_monomials,
            "vacuity: the rigidity sweep produced no tails at all")
    require(not (swept_monomials & tau_monomials),
            "rigidity scope: a tau monomial entered the rigidity checker's "
            "swept family")
    require(not any(x_edges(monomial) for monomial in swept_monomials),
            "rigidity scope: a swept tail acquired an x-edge")
    require(all(x_edges(monomial) for monomial in tau_monomials),
            "rigidity scope: a tau monomial lost its x-edge")

    # Fact C analogue on the augmentation: the chart-odd part of an arbitrary
    # combination of the augmented columns is a kernel-vector tail.
    trials = 0
    for model in MODELS:
        for label, rule in NAMED_RULES:
            names, lowers, tails = build_augmented(
                model, tau_derivation_family(rule), False, tau_tails)
            width = len(names)
            for trial in range(3):
                combination = {}
                kernel = [Q(0)] * width
                for index in range(10, width, 2):
                    left = Q(index + 1 + trial, 2 * trial + 3)
                    right = Q(index - 2 * trial, 5 + trial)
                    combination = merged(
                        combination,
                        {key: left * value
                         for key, value in tails[index].items()},
                        {key: right * value
                         for key, value in tails[index + 1].items()})
                    kernel[index] += (left - right) / 2
                    kernel[index + 1] -= (left - right) / 2
                odd = {}
                for (sector, monomial), value in combination.items():
                    flipped = PRS if sector == PQD else PQD
                    odd[(sector, monomial)] = (
                        odd.get((sector, monomial), Q(0)) + value / 2)
                    odd[(flipped, monomial)] = (
                        odd.get((flipped, monomial), Q(0)) - value / 2)
                odd = {key: value for key, value in odd.items() if value}
                kernel_tail = {}
                for index in range(width):
                    if not kernel[index]:
                        continue
                    for key, value in tails[index].items():
                        kernel_tail[key] = (kernel_tail.get(key, Q(0))
                                            + kernel[index] * value)
                kernel_tail = {key: value
                               for key, value in kernel_tail.items() if value}
                require(odd == kernel_tail,
                        "Fact C analogue: a chart-odd tau combination is not "
                        "a kernel-vector tail")
                require(odd,
                        "vacuity: the Fact C analogue trial produced the zero "
                        "combination")
                trials += 1
    require(trials == 24,
            "Fact C analogue: the trial census changed size")

    # the pure denominator block B'' stays annihilated after augmentation
    lam = {site: lambda_cochain(site, NORMALISATIONS[0][1]) for site in D}
    b_columns = []
    for site in D:
        pure = {monomial: 1
                for monomial in BASE.face_hafnian(site, (0,) * 4)}
        b_columns.append(merged(tagged(PQD, pure), tagged(PRS, pure)))
    for (left, right) in PAIRS:
        face = (X,) + tuple(site for site in D if site not in (left, right))
        pure = face_hafnian_on(face, (0,) * 8)
        b_columns.append(merged(tagged(PQD, pure), tagged(PRS, pure)))
    require(all(column for column in b_columns),
            "vacuity: an augmented pure denominator column is empty")
    nonzero = sum(1 for site in D for column in b_columns
                  if pairing(column, lam[site]))
    require(nonzero == 0,
            "R3: a Lambda_v stopped annihilating the augmented pure "
            "denominator block B''")

    return {
        "rigidity_swept_tail_monomials": len(swept_monomials),
        "tau_tail_monomials": len(tau_monomials),
        "overlap": 0,
        "rigidity_scope": (
            "the committed rigidity checker sweeps the marking "
            "(a_xv^00, a_pq^00) over all 6561 words; every tail it sees is "
            "x-FREE, every tau tail is x-BEARING, so the tau adjunction lies "
            "OUTSIDE the swept family -- exactly the case that checker's own "
            "scope paragraph leaves open ('an operation whose tail is NOT a "
            "literal chart-labelled source tail')"
        ),
        "fact_c_analogue_trials": trials,
        "augmented_B_columns": len(b_columns),
        "lambda_B_nonzero_entries": nonzero,
        "decoration_fork": (
            "CONDITIONAL.  The forced chain map resolves the chart-parity "
            "fork chart-ODD (a + b = 0), and this checker shows that a "
            "chart-odd DERIVED source column has boundary zero (CONV-T4'). "
            "IF the fork's chart-odd decoration of the attaching cell's "
            "denominator face is realised by such a column, THEN the "
            "fork's chart-odd branch closes negatively.  That "
            "identification is an unverified hand step -- the attaching "
            "map is unconstructed -- and is listed in "
            "proof_status.hand_proved_over_machine_verified_inputs"
        ),
        "naming_collision": (
            "the committed ledger's tau_<deleted_site> is a 5-name object "
            "(read off polar_audit() in provenance); S10's tau_{uv} is a "
            "10-name object indexed by odd pairs.  Different objects, shared "
            "letter; nothing here assumes they coincide"
        ),
        "label": EXHAUSTIVE,
    }


# --------------------------------------------------------------------

def audit():
    prov = provenance()
    census = chart_and_marked_tail_census()
    abc = abc_sweep()
    polar = second_polar_lemma()
    columns, words = build_d_c()
    tau_tails, tau_keys, spec = tau_spec(columns)
    named, classification = derivation_classification(tau_tails)
    repairs = repair_tests(tau_tails)
    adversarial = adversarial_adjunction_probe(tau_tails)
    uniform = uniform_nine(tau_tails)
    single = chart_odd_single_column(tau_tails)
    normalisations = normalisation_table()
    cap_census = cap_family_census()
    dehomogenised = dehomogenised_probe()
    chain_map = chain_map_repair_spec(columns, words, tau_tails)
    reconcile = reconciliations(tau_tails)

    geometry_sha256 = content_hash([
        sorted(word_text(nogo_word(site)) for site in D),
        sorted(repr(sorted(h_face(site))) for site in D),
        sorted(repr((pair, sorted(tau_tails[pair]))) for pair in PAIRS),
        sorted(repr((name, pair, word_text(named[name][pair][0])))
               for name in sorted(named) for pair in PAIRS),
    ])
    repair_sha256 = content_hash([
        sorted(repr(record) for record in repairs),
        sorted(repr(record) for record in adversarial["records"]),
        sorted(repr(row) for row in uniform),
        sorted(repr(record) for record in single),
    ])

    ledger = {
        "model": (
            "h=3 direct-free packet of "
            "verify_h3_direct_free_literal_four_face_full_nine_no_go.py: "
            "eight sites x=0, D=(1,2,3,4,5), p=6, q=7, r=3, marked odd word "
            "m=12112, run at BOTH specialisations of the p--r block -- "
            "A_pr = 0 (direct-free, 90-term rows) and A_pr free (tilted, "
            "105-term rows)"
        ),
        "label_taxonomy": {
            "proved": PROVED,
            "verified_exhaustively": EXHAUSTIVE,
            "verified_on_instances": INSTANCES,
            "convention": CONVENTION,
            "consequence": CONSEQUENCE,
        },
        "provenance": prov,
        "chart_and_marked_tail_census": census,
        "abc_decomposition": abc,
        "second_polar_lemma": polar,
        "tau_spec": spec,
        "derivation_classification": classification,
        "augmented_repair_tests": repairs,
        "adversarial_adjunction_probe": adversarial,
        "uniform_nine_choices": uniform,
        "chart_odd_single_column": single,
        "tilted_normalisations": normalisations,
        "cap_family_census": cap_census,
        "dehomogenised_convention_probe": dehomogenised,
        "chain_map_repair_spec": chain_map,
        "reconciliations": reconcile,
        "geometry_sha256": geometry_sha256,
        "repair_sha256": repair_sha256,
        "theorem": (
            "CHART-BLINDNESS OF THE ORIGINAL COLUMNS.  The repair covector "
            "is chart-ODD and is supported on the FIVE ORIGINAL no-go "
            "columns: k_v = r_v^pq - r_v^pr with (Lambda_v T'')(k_v) = 1.  "
            "Those five rows are chart pairs of ONE global row -- the "
            "committed no-go's own Fact A -- so every row of A'' has EQUAL "
            "entries on each of the five {pq, pr} pairs, and ADJOINING a "
            "column only appends coordinates on which k_v vanishes.  Hence "
            "k_v stays in ker A'' and (Lambda_v T'')(k_v) stays 1 under ANY "
            "adjunction whatsoever -- DERIVED, boundary-MISMATCHED, or "
            "outright DECLARED -- so Lambda_v T'' never lies in row(A'') and "
            "the connecting matrix stays [I_5 | 0], at BOTH specialisations "
            "of A_pr.  Machine-checked against deliberately illegal "
            "adjunctions that DESTROY global chart-blindness (chart-odd part "
            "of row(A'') of dimension 10 and 4 in the probe records) and "
            "change no verdict.  When every adjoined column satisfies (D-i) "
            "one gets the STRONGER, but unnecessary, statement that all of "
            "row(A'') is chart-even (dimension 0 in all twelve derived "
            "augmentations).  The derived tau columns of the scratch repair "
            "spec EXIST (2106 second-polar solutions, exactly the 810 CAP "
            "ones V-admissible) and DO complete the chain-map comparison "
            "(full-block Hom 0 -> 2), yet are ORTHOGONAL to the obstruction: "
            "Lambda_v is supported on x-FREE monomials, every tau monomial is "
            "x-BEARING, and the inconsistent Rouche-Capelli equation on the "
            "OLD kernel vector k_v contains no new unknown at all, reading "
            "0 = +/-1"
        ),
        "scope": (
            "CLOSES the h=3 marked-chart Schur comparison mechanism against "
            "ANY ADJUNCTION to the committed no-go source -- derived, "
            "boundary-mismatched or declared -- at BOTH specialisations "
            "A_pr = 0 and A_pr free.  DOES NOT CLOSE: a REBUILT or REPLACED "
            "comparison, i.e. one that changes the five original columns "
            "themselves rather than adding to them (adjunction is what is "
            "closed; replacement is not); the dehomogenised chart-column "
            "convention CONV-X5, which redefines what a chart column's "
            "boundary IS -- it does break Fact A, but trivialises BOTH "
            "models identically (rank 10, kernel 0, vacuous lifts) and is "
            "not the convention of the committed checkers -- flagged as "
            "CONVENTION and rejected; the COMPLETENESS direction of the CAP "
            "classification (that nothing outside the CAP family can pair "
            "with a Lambda_v), which is verified-on-instances only, though "
            "the closure does not rest on it; the n=8 two-chart structure, "
            "under separate live investigation; and all non-Schur routes -- "
            "Hamilton descent, chart-26 propagation, the diagonal/pencil "
            "lane, and membership.  This closes ONE mechanism of ONE route.  "
            "Krenn's conjecture remains open"
        ),
        "proof_status": {
            "machine_verified": (
                "every census, cardinality, rank, kernel dimension, "
                "connecting matrix, Rouche-Capelli verdict and identity "
                "reported in this ledger, by exact Fraction/int arithmetic"
            ),
            "true_by_construction_and_labelled_as_such": [
                "Fact A -- 'the two chart columns of a row share one lower "
                "boundary' -- is a tautology of the chart convention.  Its "
                "CONTENT is that the convention is the repo's own: the "
                "direct-free branch is computed through the COMMITTED "
                "BASE.chart_partition and agreed against an independent "
                "flag-based split on all 6561 words, and the sector tags are "
                "imported from the committed rigidity checker.  The tilted "
                "branch applies the same definition to the 105-term row and "
                "is labelled CONVENTION",
                "in the DERIVED augmentations, 'A'' is constant on chart "
                "pairs', 'k_v in ker A''' and 'the chart-odd part of row(A'') "
                "has dimension 0' are THREE VIEWS OF ONE construction-forced "
                "fact -- build_augmented appends the same boundary dict "
                "twice.  They discriminate only against a mutation of the "
                "builder.  The genuinely discriminating test is the "
                "adversarial adjunction probe, where the builder is "
                "deliberately broken, the chart-odd dimension is REQUIRED to "
                "be nonzero, and the verdicts are unchanged",
                "CONV-T4' -- 'a chart-odd single column has boundary zero' -- "
                "is a difference of two identical dicts and can never be "
                "nonzero; it is labelled CONVENTION.  What is MEASURED there "
                "is the connecting verdict that follows",
                "the vanishing of the connecting sub-block on the NEW chart "
                "squares follows from x-edge separation; it is measured "
                "independently",
            ],
            "hand_proved_over_machine_verified_inputs": [
                "the universal quantifier 'under ANY adjunction': k_v is "
                "supported on the five ORIGINAL columns, every row of A'' has "
                "equal entries there by the committed no-go's Fact A, and "
                "adjoining a column only appends coordinates on which k_v "
                "vanishes.  The eight adversarial-probe runs, the twelve "
                "derived augmentations, the nine uniform choices and the "
                "eight CONV-T4' runs are instances, not the proof",
                "the closed form of the second polar and the residual-forcing "
                "corollary that makes the derivation search finite",
                "the closed form of the tilt-only sector B and the deduction "
                "B = 0 for the no-go marking from 'the cap mark a_pq^00 "
                "occupies the site p'",
                "the IDENTIFICATION of the decoration fork's chart-odd "
                "decoration of the attaching cell's denominator face with a "
                "chart-odd DERIVED source column of this comparison.  That "
                "identification is asserted, not verified: the fork's "
                "attaching map is unconstructed.  Section 6's fork claim is "
                "therefore CONDITIONAL on it",
            ],
            "status": (
                "research reduction until independently audited; the "
                "universally quantified steps above are arguments on paper "
                "whose every input is checked here"
            ),
        },
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 Schur route model-independent closure ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    census = ledger["chart_and_marked_tail_census"]
    classification = ledger["derivation_classification"]
    chain_map = ledger["chain_map_repair_spec"]
    print("h=3 Schur route, model-independent closure: PASS (exact, over Q)")
    print()
    print("CHART CENSUS (%d words, both models)" % census["words_swept"])
    print("  A_pr = 0 : row %d = %s (pq) = %s (pr)"
          % (census["direct_free_row_monomials"],
             " + ".join(map(str, census["direct_free_pq_split"])),
             " + ".join(map(str, census["direct_free_pr_split"]))))
    print("  A_pr free: row %d = %s (pq) = %s (pr)"
          % (census["tilted_row_monomials"],
             " + ".join(map(str, census["tilted_pq_split"])),
             " + ".join(map(str, census["tilted_pr_split"]))))
    print("  partition failures %d; marked-tail model differences %d of %d; "
          "tilt-only sector nonempty %d"
          % (census["partition_failures"],
             census["marked_tail_model_differences"],
             census["marked_tail_cases"],
             census["tilt_only_sector_nonempty_cases"]))
    print("  nonzero marked-tail instances %d (5 x 81)"
          % census["nonzero_marked_tail_instances"])
    print()
    abc = ledger["abc_decomposition"]
    print("ABC / tilt independence: %d (word, marking) pairs, %d ABC "
          "failures, %d closed-form failures, %d with B != 0"
          % (abc["pairs_checked"], abc["abc_identity_failures"],
             abc["closed_form_failures"], abc["markings_with_nonzero_B"]))
    polar = ledger["second_polar_lemma"]
    print("second polar: %d markings, %d mismatches, %d residual-cover "
          "failures, %d nonzero"
          % (polar["vertex_disjoint_markings"],
             polar["closed_form_mismatches"],
             polar["residual_cover_failures"], polar["nonzero_polars"]))
    print()
    print("DERIVATION CLASSIFICATION")
    print("  candidate (a): %d nonzero swept tails, %d meet a tau tail"
          % (classification["candidate_a_nonzero_tails"],
             classification["candidate_a_tau_hits"]))
    print("  candidate (b): %d tested, %d solutions = CAP %d + CROSS %d"
          % (classification["candidate_b_tested"],
             classification["candidate_b_solutions"],
             classification["cap_solutions"],
             classification["cross_solutions"]))
    print("  V-admissible: CAP %d / %d, CROSS %d / %d"
          % (classification["cap_v_admissible"],
             classification["cap_v_admissible"]
             + classification["cap_v_inadmissible"],
             classification["cross_v_admissible"],
             classification["cross_v_admissible"]
             + classification["cross_v_inadmissible"]))
    print("  named derivations %s; D2 parent row %s"
          % (classification["named_derivations"],
             classification["d2_parent_row"]))
    print()
    print("CHAIN-MAP REPAIR SPEC: full-block Hom per sector %d -> %d "
          "(total %d); psi_0 support %s; psi_1 landings %d"
          % (chain_map["bare_full_block_hom_per_sector"],
             chain_map["augmented_full_block_hom_per_sector"],
             chain_map["augmented_full_block_hom_total"],
             chain_map["psi_0_support"], chain_map["psi_1_landings"]))
    print()
    print("AUGMENTED REPAIR TESTS")
    print("  %-22s %-12s %5s %6s %7s %9s %6s %7s %6s"
          % ("augmentation", "model", "cols", "rankA", "dimker",
             "connrank", "lifts", "oddrow", "repair"))
    for record in ledger["augmented_repair_tests"]:
        print("  %-22s %-12s %5d %6d %7d %9d %6d %7d %6d"
              % (record["augmentation"], record["model"], record["columns"],
                 record["rank_A"], record["kernel_dimension"],
                 record["connecting_rank"], record["schur_lifts"],
                 record["chart_odd_dimension_of_row_A"],
                 record["corrections_feasible"]))
    witness = ledger["augmented_repair_tests"][0]["witness_equation"]
    print("  witness equation on %s reads %s with %d new unknowns"
          % (witness["kernel_vector_support"], witness["reads"],
             witness["new_unknowns_in_this_equation"]))
    print()
    print("ADVERSARIAL ADJUNCTION PROBE -- (D-i) DELIBERATELY VIOLATED")
    print("  %-11s %-12s %-10s %8s %9s %9s %6s %6s"
          % ("probe", "model", "base", "oddrow", "oddorig", "connrank",
             "lifts", "repair"))
    for record in ledger["adversarial_adjunction_probe"]["records"]:
        print("  %-11s %-12s %-10s %8d %9d %9d %6d %6d"
              % (record["probe"], record["model"],
                 record["base_derivation"],
                 record["chart_odd_dimension_of_row_A"],
                 record["chart_odd_dimension_on_original_columns"],
                 record["connecting_rank"], record["schur_lifts"],
                 record["corrections_feasible"]))
    print("  -> global chart-blindness DESTROYED (oddrow > 0), chart-even on")
    print("     the five ORIGINAL columns (oddorig = 0), every verdict "
          "unchanged.")
    print()
    print("TILTED NORMALISATIONS (connecting matrix on k_1..k_5)")
    for row in ledger["tilted_normalisations"]:
        print("  %-42s rank %d  diag %s  offdiag %d  Lambda.B' %d"
              % (row["normalisation"], row["connecting_rank"],
                 row["diagonal"], row["off_diagonal_nonzero_entries"],
                 row["lambda_B_prime_nonzero_entries"]))
    print()
    cap = ledger["cap_family_census"]
    print("CAP family: %d columns, %d tilt-sensitive, %d outside-family "
          "pairings among %d probe hits"
          % (cap["family_size"], cap["tilt_sensitive_members"],
             cap["probe_outside_cap_family"], cap["probe_nonzero_pairings"]))
    probe = ledger["dehomogenised_convention_probe"]
    print("CONV-X5 probe (flagged, rejected): %s"
          % [[record["model"], record["fact_a_failures"], record["rank_A"],
              record["kernel_dimension"], record["cochains_that_lift"]]
             for record in probe["records"]])
    print()
    print("geometry sha256:", ledger["geometry_sha256"])
    print("repair sha256:", ledger["repair_sha256"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
