# Exact obstruction for all four five-edge six-vertex rank graphs

This note continues `proofs/saturated-rank-graph-obstruction.md`.  It keeps
arbitrary complex entries and, unlike the saturated case, also keeps the
possible noncoordinate factors on the at most two defective rank-one
incidences.

Assume `H_6(A)=Delta_(6,3)`.  Let `R` be the nonzero rank-one graph and let
`F` consist of the zero and rank-at-least-two matrices.  If `|F|=5`, the
maximum-degree-two classification gives four possibilities:

\[
 P_6,\qquad C_3\sqcup P_3,\qquad C_4\sqcup P_2,
 \qquad C_5\sqcup P_1.                                    \tag{1}
\]

The exact checker `computations/search_f5_support_sat.py` proves that the
second and fourth support systems are inconsistent, that the first is
impossible after an exact two-matching rectangle argument, and that all
support survivors in the last case are killed by exact cancellation
transfers between coefficient fibers.

## 1. A global arbitrary-factor support relaxation

For every directed incidence `u -> v` of a rank-one edge, introduce three
Boolean variables recording the nonzero coordinates of its factor at `v`.
The support of the aggregate edge matrix is then exactly the Cartesian
product of its two nonempty factor supports.  No factor is assumed to be
coordinate.

For every ordered pair `(u,c)` of a vertex and a color, the forced-anchor
theorem supplies an incident rank-one edge whose factor at its opposite
endpoint is exactly the singleton `{c}`.  The checker encodes this finite
disjunction with witness variables.  Notice that when `d_R(u)=3`, the three
opposite factors are thereby forced to be the three coordinate axes; when
`d_R(u)=4`, the fourth factor remains completely arbitrary.

On an `F`-edge, Boolean entry variables are allowed either all to vanish or
to contain two nonzero cells in distinct rows and distinct columns.  The
latter is necessary for matrix rank at least two.  Finally, a perfect
matching monomial is declared supported exactly when all of its selected
factor coordinates and `F`-entries are nonzero.  The coefficient rules are
only

1. every constant coloring has at least one supported matching; and
2. every mixed coloring has either zero or at least two supported matchings.

Thus arbitrary cancellation among two or more nonzero complex monomials is
fully allowed.  Every genuine realization maps to a Boolean solution, so
UNSAT is an exact obstruction.

**Lemma 1.1 (finite support audit).**  The arbitrary-factor support formula
is UNSAT for `F=C_3 disjoint-union P_3` and for
`F=C_5 disjoint-union P_1`.

This is checked directly over all `3^6` colorings and all fifteen perfect
matchings, with no orbit reduction and no floating-point arithmetic.

## 2. The path normal form

Let

\[
 F=P_6=\{01,12,23,34,45\}.                                \tag{2}
\]

The same exact formula is satisfiable, but it forces much more than was put
into it.

**Lemma 2.1 (path support propagation).**  Every one of the five path
matrices is active and all of its nine entries are nonzero.

**Exact audit.**  Starting with one global formula in which each path matrix
may be zero, assume in turn that an active variable is false, and then that
each of the forty-five entry variables is false.  Every one of these exact
SAT calls is UNSAT.  In fact the only incidences which can have
noncoordinate rank-one factors are the two ends of edge `05`, and the
formula forces both of those factors to be noncoordinate.  Only the
all-entry conclusion is needed below. `QED`

There are two edge-disjoint perfect matchings

\[
 M=\{01,23,45\},\qquad N=\{05,12,34\}.                    \tag{3}
\]

Together they contain every path edge.

**Lemma 2.2 (two-matching rectangles).**  Fix a path edge `uv`, two colors
`i,k` at `u`, and two colors `j,l` at `v`.  In every Boolean support solution
there is an assignment of colors to the other four vertices such that all
four corner colorings

\[
 (c_u,c_v)\in\{(i,j),(i,l),(k,j),(k,l)\}                  \tag{4}
\]

are mixed and have exactly the two supported perfect matchings `M,N`.

**Exact audit.**  For each of the `5*3*3=45` choices, enumerate the
`3^4=81` assignments to the other vertices.  To assert that no assignment
works, add for every candidate one clause negating the conjunction that
`M,N` are supported and the other thirteen matchings are unsupported at all
four corners.  The resulting formula is UNSAT in all forty-five cases.
Selectors make these incremental exact SAT calls over one common base
formula. `QED`

**Proposition 2.3.**  The path case (2) is impossible.

**Proof.**  Choose a rectangle from Lemma 2.2.  At each corner the exact
mixed coefficient equation is

\[
                 \prod_{e\in M}A_e(c|_e)
                +\prod_{e\in N}A_e(c|_e)=0.               \tag{5}
\]

All displayed factors are nonzero: this is the meaning of supported, and
Lemma 2.1 gives it automatically on every path edge.  Suppose first that
`uv in M`.  The other two `M` factors are independent of the two corner
colors.  Since `M,N` are edge-disjoint, the two varying vertices occur on
two different `N`-edges, so the `N` product factors as a function of the
color at `u` times a function of the color at `v`.  Multiplying (5) at
corners `(i,j),(k,l)` and comparing with `(i,l),(k,j)` cancels all nonzero
factors except the four entries of `A_uv`, and gives

\[
 A_{uv}(i,j)A_{uv}(k,l)
 =A_{uv}(i,l)A_{uv}(k,j).                                  \tag{6}
\]

The argument is identical when `uv in N`, with `M,N` interchanged.  Every
`2 by 2` minor of every path matrix vanishes by Lemma 2.2.  Hence all five
path matrices have rank at most one, contradicting their forced activity in
`F`. \(\square\)

## 3. Cancellation transfers close `C_4 disjoint-union P_2`

Support singleton rules alone do not eliminate
`F=C_4 disjoint-union P_2`.  For example, a concrete survivor has

\[
 F=\{01,03,12,23,45\},                                    \tag{7}
\]

with exceptional supports

\[
\begin{array}{c|c}
01,12&\{0,2\}\mathbin\times\{0,2\}\\
03,23&\{0,2\}\mathbin\times\{0,1,2\}\\
45&\{(0,0),(1,1),(2,2)\},
\end{array}                                                \tag{8}
\]

and the ten basis-edge endpoint labels

\[
\begin{array}{c|cccccccccc}
e&02&04&05&13&14&15&24&25&34&35\\ \hline
(c_u,c_v)&11&22&20&11&12&10&02&00&10&12.
\end{array}                                                \tag{9}
\]

Every support in (8) contains a distinct-row/distinct-column pair.  The
checker fixes (8)--(9) exactly and verifies that all constant-support,
mixed-no-singleton, and anchor clauses are simultaneously satisfiable.
This is not a complex realization.  The following elementary Laurent
monomial observation eliminates it and every other support survivor.

For an `F`-edge use its selected matrix entry as a formal variable.  For a
rank-one edge, use separately the two selected endpoint-factor coordinates.
Thus every supported perfect matching has a formal monomial signature.  Two
finite sets of such monomials have the same *translated shape* if, after a
bijection, one set is a common Laurent monomial times the other:

\[
                    m_i=Q n_i\quad\hbox{for every }i.       \tag{10}
\]

The Laurent monomial `Q` is well-defined and nonzero at the realization,
because every variable appearing in the two supported fibers is nonzero.

**Lemma 3.1 (cancellation transfers).**

1. A constant coefficient fiber and a mixed coefficient fiber cannot be
   nonempty, have exactly the indicated supported matchings, and have the
   same translated shape.
2. Suppose a mixed coefficient fiber is a translated copy of all but one
   supported term of another mixed coefficient fiber.  This is impossible.

**Proof.**  In the first case, (10) makes the two coefficient sums nonzero
scalar multiples, whereas their required values are one and zero.  In the
second, the source sum is zero, so the copied subset of the target sum is
zero.  The target sum is therefore its one remaining supported monomial,
which is nonzero but is required to vanish. \(\square\)

**Lemma 3.2 (exact transfer audit).**  Every Boolean support solution for
`F=C_4 disjoint-union P_2` contains one of the two forbidden configurations
in Lemma 3.1.

**Exact audit.**  For each SAT support model, compute every nonempty
coefficient fiber's exponent-vector set modulo common translation.  If a
constant and mixed fiber have the same key, add the clause which forbids
their two exact supported-matching sets.  Otherwise find a mixed fiber for
which deleting one supported matching gives the same key as another mixed
fiber, and add the analogous clause.  Lemma 3.1 proves every added clause
for arbitrary nonzero complex values.  In the deterministic reference run,
re-solving and repeating produces 504 such exact clauses, after which the
common formula is UNSAT.  The script
asserts at every iteration that a forbidden transfer was actually found;
there is no numerical comparison, random choice, or tolerance. `QED`

Combining Lemmas 1.1, 2.1--2.2, and 3.2 gives:

**Theorem 3.3.**  The graph `F` cannot have five edges in a six-vertex,
three-color realization.

Run the audit with

```sh
uv run python computations/search_f5_support_sat.py
```

It reports the two direct UNSAT cases, the forty-five forced path
rectangles, the explicit twenty-three-entry support survivor (8), and its
final elimination together with all other survivors by cancellation
transfers.

For a persistent semantic certificate, run

```sh
uv run python computations/certify_f5_c4_p2_transfers.py
```

The checked-in JSON transcript names all 504 pairs of exact fibres.  Replay
reconstructs each blocking clause only after independently checking the
constant/mixed or delete-one Laurent exponent identity, verifies hashes of
the base and augmented DIMACS encodings, and confirms the final UNSAT result
with both Glucose 4 and CaDiCaL 1.9.5.  Regenerate the transcript with
`--generate`; the certificate is deterministic, while its number of cuts is
only solver-trajectory metadata and is not used by the proof.
