# Laurent-fiber obstruction for rank graphs with at most three edges

## Outcome and scope

Let $A_{uv}$ be arbitrary complex $3\times3$ matrices on the pairs of
$\{0,\ldots,5\}$, and let

\[
 H_6(A)=\sum_{M\in\operatorname{PM}(6)}\ \bigotimes_{uv\in M}A_{uv}.
 \tag{1}
\]

Put

\[
 F=\{uv:\operatorname{rank}A_{uv}\ne1\};                 \tag{2}
\]

thus $F$ contains both the zero matrices and the matrices of rank at
least two.  The exact computations described below prove:

**Theorem (low-rank-graph obstruction).**  If $0\leq |F|\leq3$, then

\[
 H_6(A)\ne\Delta_{6,3}:=\sum_{c=0}^2 e_c^{\otimes6}.       \tag{3}
\]

The maximum-degree-two theorem for $F$ leaves one graph type at each of
sizes zero and one, two graph types at size two, and four at size three.
The seven nontriangle types are excluded by the
Laurent-fiber enumeration in
`computations/verify_f3_toric_obstruction.py`.  The remaining triangle is
excluded by the independent 32-block certificate in
`proofs/exceptional-triangle-obstruction.md`.

Together with the previously proved four-, five-, and six-edge rank-graph
obstructions, this yields the following six-site result.

**Corollary (arbitrary complex six-site theorem).**  No collection of
arbitrary complex $3\times3$ aggregate edge matrices satisfies
$H_6(A)=\Delta_{6,3}$.

Indeed, the forced-anchor theorem gives maximum degree at most two in $F$,
so $|F|\leq6$.  The theorem above handles $|F|\leq3$;
`proofs/four-edge-rank-graph-obstruction.md`,
`proofs/five-edge-rank-graph-obstruction.md`, and
`proofs/saturated-rank-graph-obstruction.md` handle $|F|=4,5,6$.

## 1. The necessary support relaxation

Fix a candidate graph $F$.  On an edge $uv\notin F$, write the nonzero
rank-one matrix as

\[
 A_{uv}=a_{uv,u}\otimes a_{uv,v}.                           \tag{4}
\]

The Boolean formula records the nonzero coordinates of the two endpoint
factors.  On $uv\in F$, it instead records the nine entry supports of an
arbitrary matrix.  If the latter matrix is nonzero of rank at least two,
its support contains two cells in distinct rows and distinct columns; a
zero matrix has empty support.  The formula allows both alternatives and
is therefore an overapproximation of every matrix family having rank graph
$F$.

The formula also records the following necessary conditions.

1. Every rank-one endpoint factor is nonempty.
2. The forced incident-edge theorem supplies, for each ordered pair
   $(v,c)$, a rank-one edge $vu$ whose factor at the opposite endpoint
   $u$ has support exactly $\{c\}$.
3. A perfect-matching monomial is marked supported if and only if all its
   local factors or exceptional entries are supported.
4. Every constant-color coefficient has at least one supported matching.
   Every mixed coefficient has either zero or at least two supported
   matchings, since a single nonzero complex monomial cannot sum to zero.

Consequently, an UNSAT result for this Boolean overapproximation, after
adding only valid algebraic clauses, excludes an actual complex solution.

## 2. Primitive binomial lattices

On a fixed support chart, give every supported exceptional entry and every
supported coordinate of every rank-one endpoint factor its own nonzero
variable.  Write these variables as $x_1,\ldots,x_N$.  Every supported
matching term is then a Laurent-torus monomial $x^a$ with
$a\in\mathbb Z^N$ (in fact its original exponent vector is nonnegative).

If a mixed coefficient has exactly two supported matching terms, its exact
equation is

\[
 x^{a_i}+x^{b_i}=0,
 \qquad x^{d_i}=-1,
 \qquad d_i=a_i-b_i.                                       \tag{5}
\]

Choose linearly independent rows $d_1,\ldots,d_r$, put them into a matrix
$B$, and suppose some $r\times r$ coordinate minor $B_J$ has
determinant $\pm1$.  Then

\[
 L:=\operatorname{rowspan}_{\mathbb Q}(B)\cap\mathbb Z^N
   =\operatorname{rowspan}_{\mathbb Z}(B).                 \tag{6}
\]

Indeed, if $t\in\mathbb Z^N$ lies in the rational row span and
$t=cB$, restriction to the coordinates $J$ gives
$c=t_JB_J^{-1}\in\mathbb Z^r$.  Thus the chosen rows span the complete
integer lattice in their rational subspace; no saturation step is being
silently used.

Equation (5) defines on this lattice the putative sign character

\[
 \chi\!\left(\sum_i c_i d_i\right)=(-1)^{\sum_i c_i}.       \tag{7}
\]

Every other two-term relation $x^d=-1$ has unique integral coordinates
$d=\sum_i c_i d_i$.  If $\sum_i c_i$ is even, (5) predicts
$x^d=+1$, a contradiction.  This is the `odd-binomial` branch of
`single_fiber_laurent_conflict`.  If every redundant relation has odd
coordinate sum, (7) is consistent with all of them.

The unimodular-minor check is important.  If the selected rows span a
nonprimitive sublattice, the implementation declines the chart rather than
identify that lattice with its saturation.

## 3. The single-fiber Laurent lemma

Consider any other mixed coefficient fiber

\[
 \sum_{j=1}^s x^{a_j}=0.                                   \tag{8}
\]

Partition its terms by

\[
 j\sim k\quad\Longleftrightarrow\quad a_j-a_k\in L.        \tag{9}
\]

For a class $C$, choose a representative $j_C$.  By (6), write

\[
 a_j-a_{j_C}=\sum_i c_{j,i}d_i
 \quad(j\in C).
\]

The binomial equations give the exact Laurent identity

\[
 x^{a_j}=(-1)^{\sum_i c_{j,i}}x^{a_{j_C}}.                 \tag{10}
\]

Hence (8) reduces to

\[
 \sum_C m_C x^{a_{j_C}}=0,
 \qquad
 m_C=\sum_{j\in C}(-1)^{\sum_i c_{j,i}}\in\mathbb Z.      \tag{11}
\]

**Lemma (single-fiber Laurent conflict).**  Over a characteristic-zero
field, the chart is impossible if exactly one integer $m_C$ in (11) is
nonzero.

**Proof.**  Every class with $m_C=0$ cancels identically by (10).  Equation
(11) is then $m_Cx^{a_{j_C}}=0$ for the unique remaining class.  Both
factors are nonzero: $m_C\ne0$ in characteristic zero, and a Laurent
monomial is nonzero on the support torus.  This is impossible. QED

Only the exact two-term fibers actually used with nonzero coordinates in
(10), together with the target fiber (8), enter the learned clause.  Thus
the cut forbids precisely the simultaneous occurrence of a finite list of
exact coefficient supports; it makes no assertion about neighboring
support charts.

There is one further direct Laurent certificate in the recorded $F=0$
trajectory.  It is genuinely a two-fiber statement and is kept separate
from the preceding count.  Suppose two exact three-term mixed fibers,
after choosing and permuting their terms, are

\[
 1+r_1+r_2=0,
 \qquad
 1+\epsilon_1r_1+\epsilon_2r_2=0,                         \tag{11a}
\]

modulo the binomial lattice, where each
`epsilon_j in {+1,-1}` is obtained from the integral sign character (7).
If at least one sign is negative, the chart is impossible: with one sign
change, subtracting the equations gives `2r_j=0`; with two sign changes,
adding them gives `2=0`.  The factors `r_j` are Laurent monomials and hence
nonzero.  The implementation checks the two translated exponent
differences and their parities with the same unimodular integer-coordinate
oracle used above, and its learned clause lists both trinomials and only the
binomial fibers used in those two translations.

## 4. Exact-fiber clauses and symmetry breaking

For a coloring $c$ and matching set $S$, the checker introduces a
Tseitin variable $I_{c,S}$ with

\[
 I_{c,S}\quad\Longleftrightarrow\quad
 \bigwedge_{M\in S}z_{c,M}\ \wedge\!
 \bigwedge_{M\notin S}\neg z_{c,M}.                        \tag{12}
\]

If the Laurent certificate uses fibers
$(c_1,S_1),\ldots,(c_t,S_t)$, the
single learned clause is

\[
 \neg I_{c_1,S_1}\vee\cdots\vee\neg I_{c_t,S_t}.          \tag{13}
\]

The encoding of (12) has one forward implication for every support bit and
one reverse clause for their conjunction.  It was checked after flipping
each of the fifteen matching bits, and a learned two-fiber clause was
checked both on its forbidden conjunction and on every one-pattern escape.

The cancellation transfers used before and between Laurent cuts are exact
polynomial implications.  Two exponent fibers with the same translated
shape differ by multiplication by one Laurent monomial, so the vanishing of
one forces the vanishing of the other.  More generally, if disjoint
translated mixed-zero fibers cover a constant fiber, they force its nonzero
coefficient to vanish; if they cover all but one term of a mixed fiber, they
leave one nonzero Laurent monomial.  The checker blocks only the exact
source and target supports used in such an implication.

To avoid relearning labeled copies, let

\[
 \Gamma=\operatorname{Aut}(F)\times S_3                   \tag{14}
\]

act on the ordered vector $z$ of primitive support bits.  The checker
adds the ordinary lex-leader constraints

\[
 z\le_{\mathrm{lex}}\gamma z
 \qquad(1\ne\gamma\in\Gamma).                              \tag{15}
\]

These constraints cannot remove every representative of a support orbit:
the lexicographically least vector in each finite orbit satisfies all of
(15).  Endpoint reversal transposes the row and column colors of an
exceptional matrix, while a directed rank-one factor maps by applying the
vertex permutation to both its tail and head.  These are exactly the two
mapping rules in the implementation.

For each bit comparison, four clauses make the auxiliary `equal` variable
equivalent to equality of the two bits.  Three more clauses make the next
`prefix` variable equivalent to the conjunction of the previous prefix and
`equal`; an equal prefix forbids the first differing pair `1,0`.  This CNF
and the endpoint-reversal mapping were independently tested on random
orbits as described in Section 6.

The learned Laurent clauses in the recorded runs are direct clauses, not
symmetry-orbit clauses.  This is sound because every clause (13) is itself
an algebraic impossibility; lex leaders are used only to choose which
support representatives the solver must enumerate.

## 5. Exhaustive results

The seven nontriangle runs used PySAT `1.9.dev7` with its `cadical195` backend,
the full lex leaders from (15), no learned-cut symmetry orbit, and no periodic static
solver rebuild.  All exponent arithmetic, lattice membership, determinants,
and parity checks were performed exactly by SymPy and Python integers.
SciPy's floating-point MILP proposal routines produced no learned cut in
these runs.  Nor did the older odd-cycle, toric-minor, or color-sensitive
support routines produce a cut.  Apart from the initial necessary CNF, the
only used clauses were exact cancellation transfers, the lemma of Section
3, and three translated two-trinomial certificates of type (11a).  No
floating-point proposal, toric-minor, odd-cycle, generalized-elimination,
or support witness produces a learned clause in these recorded runs.

\[
\begin{array}{c|c|c|c|c|c}
|F|&F&|\operatorname{Aut}(F)|&\text{cancellation transfers}
   &\text{single-fiber cuts}&\text{translated trinomials}\\ \hline
3&3P_2&48&14&1171&0\\
3&P_3\sqcup P_2\sqcup P_1&4&2&882&0\\
3&P_4\sqcup2P_1&4&11&196&0\\
2&2P_2\sqcup2P_1&16&17&1475&0\\
2&P_3\sqcup3P_1&12&0&698&1\\
1&P_2\sqcup4P_1&48&23&1108&1\\
0&6P_1&720&12&483&1
\end{array}                                                 \tag{16}
\]

After the indicated cuts, CaDiCaL reported the remaining CNF UNSAT in each
row.  The cut counts are model-enumeration trajectory metadata rather than
part of the certificate semantics: a current isolated rerun of the shortest
row $P_4\sqcup2P_1$ reproduced 23 lex comparisons, 11 transfers, 196
single-fiber cuts, no other learned-cut type, and UNSAT.

The isolated $6P_1$ rerun reproduced its two-trinomial clause.  The two
colorings were

\[
 (0,0,0,2,0,0),\qquad(2,0,0,0,0,1),
\]

the translated parities were $(1,0)$, and the two exact lattice
certificates used respectively five and four basis relations (seven exact
fibers after deduplication).  It then terminated UNSAT with 483
single-fiber cuts, 12 transfers, and exactly this one translated-trinomial
cut.  The current deterministic $P_3\sqcup3P_1$ and
$P_2\sqcup4P_1$ trajectories each use one additional certificate of the
same proved type; their named fibres are retained in the persistent bundle.

For the remaining three-edge type $C_3\sqcup3P_1$, the separate exact audit
uses 29 exceptional-triangle rigidity blocks and 3 partition-rank blocks,
then reaches UNSAT after 32 support representatives and zero cancellation
transfers.  Its proof is given in
`proofs/exceptional-triangle-obstruction.md`.
The historical 192- and 29-block transcripts in earlier drafts are stale:
the current stronger orbit blocking deterministically produces the 32-block
line (`3` partition-rank and `29` triangle-rank representatives) without
changing the two underlying algebraic witnesses.

The reproducibility wrapper

```sh
.venv/bin/python computations/verify_low_rank_graph_laurent_obstruction.py
```

runs all eight graph types and checks UNSAT together with the absence of
the MILP toric/odd and color-sensitive support fallback families.  The
exact translated-trinomial count is displayed, and its recorded value is
checked with the other trajectory metadata only when
`--strict-recorded-counts` is requested.  A shorter independent
smoke audit is

```sh
.venv/bin/python computations/verify_low_rank_graph_laurent_obstruction.py \
  --quick
```

The persistent semantic certificate is generated and replayed by

```sh
.venv/bin/python computations/certify_low_rank_graph_laurent.py
```

It contains 6,095 named records.  The independent replay reconstructs each
translated-zero transfer from exponent multisets, recomputes every
single-fiber class sum from integral coordinates in the named binomial
relations, checks every translated-trinomial sign comparison, and rebuilds
the exact-fiber Tseitin CNF.  In particular the character values, including
relations with negative Laurent coordinates, are computed by integer parity
and are always integers.  The seven reconstructed CNFs have the following
SHA-256 hashes:

\[
\begin{array}{c|c}
F&\text{canonical CNF SHA-256}\\ \hline
3P_2&\texttt{1a4e398da3a95ea2a30c8105bc43540ebca4c7b4dcdc90d1b6b468973d90e617}\\
P_3\sqcup P_2\sqcup P_1&\texttt{c3d13c78ba83aa91a310554521a6a517add3e3b007b97e2d9ac08e74bf6edb86}\\
P_4\sqcup2P_1&\texttt{ba2829c813bdb246ef4b708aa760657fd812197504b1c72a09cbdfc859f2b355}\\
2P_2\sqcup2P_1&\texttt{b4ba959ebbd9c69eeece7ee8a637fa022b4e21e5ea484ff0e6634dfe7e2602fc}\\
P_3\sqcup3P_1&\texttt{5d659c0c3aefee237a55aaba595913f2fcbf74fe0e504d86f5dd6e728fa7b644}\\
P_2\sqcup4P_1&\texttt{5294c493ccc71a541f74830c46f6492f285fc2a57418678da56b46b15777c74c}\\
6P_1&\texttt{948e918326dacb9883b69e14ff2abb38e025cf13026661569f29ba8d51e0126c}
\end{array}
\]

The JSON bundle itself has SHA-256
`83c4b90ab89d59b0543c40ba5c35aea3659bdcf1ffeb01ab597c9194e9cb70f0`.
Each final propositional formula is independently reported UNSAT by
`cadical195` and `kissat404`.  Thus the trusted boundary consists of the
small exact semantic replay plus two exact SAT implementations.  No DRAT
trace is claimed for these seven formulas; the exceptional triangle has its
own separately checked DRUP certificate.

## 6. Adversarial audit

Run

```sh
.venv/bin/python computations/test_single_fiber_laurent_conflict.py
```

It checks:

* a primitive one-class contradiction;
* exact four-term internal cancellation, which must not be cut;
* a fiber with multiple surviving Laurent classes, which must not be cut;
* conservative refusal of a nonprimitive lattice;
* an inconsistent redundant binomial;
* negative Laurent coordinates;
* forty random unimodular shears with negative entries;
* eighty random target fibers compared against an independently computed
  signed-class-sum oracle, including both conflicts and nonconflicts;
* translated trinomials with one and two sign changes, an even-sign
  nonconflict, and conservative refusal of a nonprimitive lattice;
* every support bit in the exact-fiber Tseitin equivalence and the exact
  conjunction excluded by (13); and
* twelve random 90-bit charts under endpoint reversal and every global
  color permutation, for which the orbit minimum is SAT and every strictly
  larger image is UNSAT under the lex leaders.

These tests passed independently of the seven Laurent exhaustive searches.

Small solver-independent chart certificates for both two-edge types, the
one-edge type, the empty graph, and a generalized `3P2` chart are recorded
in `proofs/representative-low-rank-laurent-certificates.md`.  Their three
verifiers reconstruct all 729 coefficient fibers and check the displayed
integer exponent identities without invoking a SAT solver.

Combining the eight rows exhausts every maximum-degree-two graph with at
most three edges, proving the theorem and, with the earlier higher-rank
strata, the arbitrary complex six-site corollary.
