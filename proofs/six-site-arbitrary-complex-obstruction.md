# The arbitrary-complex six-site obstruction

## 1. Statement

Let (V_v=\mathbb C^3), with basis (e_0,e_1,e_2), for six named
vertices (v\in B).  Give every unordered pair (uv) an arbitrary
endpoint-ordered matrix

\[
                         A_{uv}\in V_u\otimes V_v
\]

(the matrix may be zero), and put

\[
 H_6(A)=\sum_{M\in\operatorname {PM}(B)}
                 \bigotimes_{uv\in M}A_{uv}.                 \tag{1}
\]

**Theorem 1.1.**  There is no collection of complex matrices (A_{uv})
such that

\[
                         H_6(A)=\Delta_{6,3}
                         :=\sum_{c=0}^2e_c^{\otimes6}.       \tag{2}
\]

Consequently, a decorated degree-two source on six output vertices cannot
be monochromatic with three or more colors.

This note assembles the proof and makes its finite boundary explicit.  The
algebraic and finite lemmas used in the individual rank strata are proved
in the cited companion notes; no genericity, positivity, or restriction on
the number of parallel sources is used.

## 2. Exact passage from decorated sources to aggregate matrices

For a source (a) with neighbours (u,v), endpoint colors (i,j), and
weight (w(a)), form

\[
                    w(a)e_i^{(u)}\otimes e_j^{(v)}.
\]

Sum these tensors over all sources with the same unordered neighbour pair,
retaining the endpoint order:

\[
 A_{uv}=\sum_{a:N(a)=\{u,v\}}
          w(a)e_{k(a,u)}^{(u)}\otimes e_{k(a,v)}^{(v)}.    \tag{3}
\]

Expanding one factor from (3) on every edge of a perfect matching gives
exactly one choice of a source above each matched pair.  Such choices are
in bijection with consistent source subsets.  Therefore the coefficient of
(e_{c(0)}\otimes\cdots\otimes e_{c(5)}) in (1) is (w_G(c)).
This proves the aggregate formulation even with parallel sources,
asymmetric endpoint colors, zero weights, and cancellations among sources
on the same pair.

If the original palette has (q\ge3) colors, monochromaticity says that
(w_G(c)=0) at every mixed (c) and that the constant coefficients are
some nonzero amplitudes (\lambda_0,\dots,\lambda_{q-1}); it does *not*
say they are equal.  Choose any three colors and project every local color
space onto their coordinate span.  Applying the six projections to (1)
merely replaces every (A_{uv}) by another arbitrary (3\times3) matrix,
and applying them to the target leaves
(\sum_{c\in S}\lambda_ce_c^{\otimes6}) over the three chosen colors
(S).

One diagonal rescaling removes the amplitudes.  Pick (\mu_c) with
(\mu_c^6=\lambda_c^{-1}), which exists over (\mathbb C), and apply
(e_c\mapsto\mu_ce_c) at all six vertices.  The target becomes exactly
(\Delta_{6,3}), while (A_{uv}) becomes (DA_{uv}D) with
(D=\operatorname{diag}(\mu_c)); since (D) is invertible this is again an
arbitrary matrix.  Thus Theorem 1.1 rules out every palette of size at
least three.

## 3. The rank-defect graph

Assume (2) for a contradiction.  Let

\[
 \begin{aligned}
 R&=\{uv:\operatorname {rank}A_{uv}=1\},\\
 F&=\{uv:\operatorname {rank}A_{uv}\ne1\}.
 \end{aligned}                                             \tag{4}
\]

Thus (R) contains precisely the nonzero rank-one matrices, while (F)
contains both zero matrices and matrices of rank at least two.

The forced incident-edge theorem of
[`slice-cover.md`](../notes/slice-cover.md) applies at every ordered
vertex/color pair.  It says that for every (v) and (c\in\{0,1,2\})
there is an active incident pair (vu) of rank one whose factor at (u)
is a nonzero multiple of (e_c).  The three witnesses at a fixed (v)
are distinct, because one rank-one endpoint factor cannot have two
different coordinate image lines.  Hence

\[
                         d_R(v)\ge3,
             \qquad      d_F(v)\le2                       \tag{5}
\]

for every vertex.  In particular

\[
                         0\le |F|\le6.                     \tag{6}
\]

Every graph of maximum degree two is a disjoint union of paths and cycles.
On six vertices, its isomorphism types in the seven possible edge counts
are the following:

\[
\begin{array}{c|l}
|F|&\text{types}\ \\ \hline
0&6P_1\\
1&P_2\sqcup4P_1\\
2&2P_2\sqcup2P_1,\quad P_3\sqcup3P_1\\
3&3P_2,\quad P_3\sqcup P_2\sqcup P_1,\quad
   P_4\sqcup2P_1,\quad C_3\sqcup3P_1\\
4&P_5\sqcup P_1,\quad P_4\sqcup P_2,\quad P_3\sqcup P_3,
   \quad C_3\sqcup P_2\sqcup P_1,\quad C_4\sqcup2P_1\\
5&P_6,\quad C_3\sqcup P_3,\quad C_4\sqcup P_2,
   \quad C_5\sqcup P_1\\
6&C_6,\quad C_3\sqcup C_3.
\end{array}                                                \tag{7}
\]

It remains to exclude exactly these nineteen graph types.

## 4. Exact support principles

All finite strata use the following one-sided support consequences of (2).
They are valid over (\mathbb C), despite arbitrary cancellation.

1. A nonzero rank-one block has independent nonempty endpoint supports,
   and its matrix support is their Cartesian product.
2. A nonzero matrix of rank at least two contains two supported entries in
   distinct rows and distinct columns.  An (F)-block is allowed instead
   to be identically zero.
3. Every constant-color coefficient has at least one supported perfect
   matching, because its value is one.
4. A mixed coefficient has either zero or at least two supported perfect
   matchings.  If it had exactly one, its value would be one nonzero
   monomial and could not be zero.
5. The three directed coordinate anchors at every vertex are imposed
   exactly as supplied by (5).
6. In the (|F|\le3) formulas an active (F)-block additionally carries a
   *minor witness*.  Its rank is at least two, so one of its nine
   (2\times2) minors is nonzero; an auxiliary variable records which one,
   and the only condition imposed is the necessary one that at least one of
   that minor's two diagonal products be supported
   (`add_minor_witnesses` in
   `computations/verify_f3_toric_obstruction.py`).  Any realization
   extends to a satisfying assignment of these variables, so they add no
   strength beyond rank at least two.

The Boolean formulas in the cited audits encode only these necessary
conditions, plus separately proved exact Laurent implications and the
lex-leader symmetry constraints, which cannot delete the lexicographically
least member of any support orbit.  Thus UNSAT of any such formula excludes
every complex realization mapping to it; SAT is never interpreted as a
realization.

Two elementary algebraic implications recur.  First, if a mixed
coefficient has exactly two supported terms (m_1,m_2), its equation is
(m_1+m_2=0).  Four such equations arranged as the corners of a
two-by-two entry rectangle force the corresponding matrix minor to vanish,
provided all divided factors are supported.  Second, multiplying every
term of a coefficient fiber by one common nonzero Laurent monomial
preserves whether its sum vanishes.  Hence a mixed zero fiber cannot be a
translated copy of a nonzero constant fiber, nor can one mixed zero fiber
be a translated copy of all but one term of another mixed zero fiber.
These statements concern exact finite fiber supports and make no termwise
claim about a fiber with additional terms.

The checker implements the second implication in its multi-source form,
stated in Section 4 of
[`low-rank-graph-laurent-obstruction.md`](low-rank-graph-laurent-obstruction.md):
if translated copies of several *pairwise disjoint* mixed zero fibers cover
a constant fiber, they force its coefficient — which is one — to vanish,
and if they cover all but one term of a mixed fiber, they leave a single
nonzero Laurent monomial equal to zero.  The one-source statement above is
the case of a single cover block.  In the shipped certificate all 79
transfer records have exactly one source, so the multi-source case is
dormant; it is recorded here because `audit_transfer` in
`computations/certify_low_rank_graph_laurent.py` would accept it.

## 5. Exhaustion of the rank strata

### 5.1 Four, five, and six defect edges

[`four-edge-rank-graph-obstruction.md`](four-edge-rank-graph-obstruction.md)
excludes all five (|F|=4) types.  After exact translated-fiber closure,
each surviving support chart has an active (F)-edge whose supported
two-by-two rectangles all occur in exact binomial coefficient rectangles.
Every supported minor of that edge is therefore zero, contradicting its
rank at least two.  One type is already support-UNSAT.

[`five-edge-rank-graph-obstruction.md`](five-edge-rank-graph-obstruction.md)
excludes all four (|F|=5) types.  The two disconnected-cycle types are
support-UNSAT.  In the (P_6) type, support propagation forces all five
exceptional matrices active and all forty-five entries nonzero; exact free
rectangles force every two-by-two minor to vanish.  In the
(C_4\sqcup P_2) type, a persistent 504-clause semantic certificate uses
only the two translated-fiber implications stated above.

[`saturated-rank-graph-obstruction.md`](saturated-rank-graph-obstruction.md)
excludes both (|F|=6) types.  In the (C_6) type, all fifty-four
exceptional entries are forced nonzero and free coefficient rectangles
again annihilate every minor.  In the (C_3\sqcup C_3) type, the support
relaxation that allows each internal matrix *either* to vanish *or* to have
rank at least two is UNSAT on all 134 asymmetric anchor-color orbits, under
two independent SAT backends; 56 of those orbits are already refuted by an
empty clause at construction, where a constant coloring admits no
compatible perfect matching at all.  Because the zero alternative is inside
the audited formula, this branch uses no separate argument excluding a zero
internal matrix.

### 5.2 Zero through three defect edges

The seven nontriangle types with (|F|\le3) are excluded by
[`low-rank-graph-laurent-obstruction.md`](low-rank-graph-laurent-obstruction.md).
On a fixed support torus, every exact two-term mixed fiber gives a primitive
binomial relation (x^d=-1).  The audit selects independent relations only
when an explicitly checked coordinate minor has determinant (\pm1), so
their integer lattice is saturated.  In any further mixed fiber, terms are
grouped modulo this lattice and their exact signed multiplicities are
computed.  A unique nonzero signed class is impossible in characteristic
zero.  Three of the seven types — (P_3\sqcup3P_1), (P_2\sqcup4P_1) and the
empty graph (6P_1) — each also use one explicitly checked pair of translated
trinomials.  Persistent semantic bundles reconstruct every lattice,
unimodular minor, parity, exact fiber, and learned clause before resolving
the final Boolean formula.

The remaining type (C_3\sqcup3P_1) is excluded by
[`exceptional-triangle-obstruction.md`](exceptional-triangle-obstruction.md).
A color-sensitive stabilizer either leaves at most two edge-partition terms,
contradicting partition rank three, or isolates the three exceptional
triangle terms.  Equality in the resulting three-term decomposition of
the diagonal tensor forces each exceptional block to be a coordinate
rank-one matrix, contrary to its membership in (F).  The finite support
audit has 32 semantic orbit blocks: 3 partition-rank and 29 triangle-rigidity
blocks.

Together these arguments exclude every row of (7), contradicting (2) and
proving Theorem 1.1.

## 6. Reproducibility boundary

The hand part of the proof consists of aggregation, forced anchors, the
defect budget, graph enumeration, rectangle/Laurent implications, primitive
lattice lemma, and exceptional-triangle rigidity.  The finite supplements
enumerate support charts and certify propositional exhaustion.  The main
entry points are

```text
python computations/verify_f4_support_obstruction.py
python computations/certify_f5_c4_p2_transfers.py
python computations/verify_saturated_rank_graph_obstruction.py
python computations/certify_low_rank_graph_laurent.py
python computations/certify_exceptional_triangle_obstruction.py
```

The forced-anchor step is proved by hand in
[`slice-cover.md`](../notes/slice-cover.md), and nothing in Theorem 1.1
depends on a machine check of it.  Because that proof is field-independent,
its three-term step admits an exhaustive confirmation over small finite
fields, which is a separate supplementary run:

```text
python computations/verify_slice_cover_three_term_step.py
```

The certificate replay above ends with the named support certificate for
the exceptional triangle.  A
resolution-level DRUP proof of the same CNF is optional and is not stored in
the repository, because `*.drup` is gitignored.  Regenerate the pair and
check it with

```text
python computations/certify_exceptional_triangle_obstruction.py \
  --proof-prefix computations/exceptional_triangle_support
python computations/verify_drup_certificate.py \
  computations/exceptional_triangle_support.cnf \
  computations/exceptional_triangle_support.drup
```

The `--proof-prefix` run rewrites `exceptional_triangle_support.cnf` and
emits the deletion-free DRUP file beside it; on the reference run both
reproduce the SHA-256 digests recorded in
[`exceptional-triangle-obstruction.md`](exceptional-triangle-obstruction.md)
byte for byte.

The low-rank wrapper

```text
python computations/verify_low_rank_graph_laurent_obstruction.py
```

independently regenerates the eight (|F|\le3) searches.  The persistent
certificates record exact semantics rather than trusting a sequence of SAT
models.

The floating-point boundary needs stating precisely rather than by
exclusion.  Two of the searched cut families in
`computations/verify_f3_toric_obstruction.py` *propose* their integer
certificates with `scipy.optimize.milp`: the toric minor-witness family,
counted as `toric_rank_cuts`, and the general odd-binomial family, counted
inside `odd_cuts`.  A proposal is never trusted; it is re-multiplied over
the integers, and its exponent identity and sign parity re-checked, before
any clause is added.  In the recorded runs neither family contributes a
clause at all: the wrapper asserts `toric_rank_cuts=0`, `odd_cuts=0`, and
`support_cuts=0` on the terminal line of every Laurent case, and the
certificate generator asserts those three together with
`generalized_cuts=0`.  The
replay entry point `certify_low_rank_graph_laurent.py` never reaches either
routine: importing the module still loads NumPy and SciPy, but no code path
in the replay calls a proposal routine.  It rebuilds the CNF, checks its
SHA-256 digest, and re-verifies every named Laurent record with SymPy
rationals and Python integers.  So no
floating-point value enters any accepted step of Theorem 1.1, and no
finite-field specialization, generic matrix choice, or positivity
assumption is used anywhere in it.
