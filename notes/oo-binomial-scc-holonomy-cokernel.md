# A zero-holonomy binomial SCC has one explicit terminal charge

## Outcome

After private matching classes have been peeled, suppose one connected
critical component consists of literal binomial source rows

\[
                       f_e=a_eX_u+b_eX_v,
              \qquad a_e b_e\ne0.                         \tag{1}
\]

Over the Laurent fraction field there are only two possibilities.

1. Some cycle has nontrivial signed holonomy.  Then the rows span every
   matching-class column in the component.  A target supported there gives
   an ordinary localized unit.
2. Every cycle has trivial signed holonomy.  Then the row span has
   codimension exactly one.  A spanning tree constructs its unique cokernel
   functional by the propagation rule

   \[
                       z_v=-{a_e\over b_e}z_u.             \tag{2}
   \]

Thus the arbitrary zero-Fitting alternative in the curved-OO source module
is not a family of unknown maximal minors.  It is one explicit terminal
charge per connected binomial component.  Closing the component is
equivalent to showing that one retained physical row has nonzero pairing
with that charge.

For physical plus-binomial rows whose monomial exponent ratios have trivial
unsigned holonomy, (2) reduces to the alternating sign on a bipartition.
An odd cycle therefore has determinant twice an active Laurent monomial, as
in the committed hafnian triangle; an even component has one alternating
charge.

This theorem strengthens the organization of
[`oo-curved-signed-cycle-fitting-lemma.md`](oo-curved-signed-cycle-fitting-lemma.md).
It does not prove that the crossed physical rows hit the terminal charge.

## 1. Exact rank theorem

Let `G` be the connected graph whose vertices are matching classes and whose
edges are the rows (1).  Give an edge an arbitrary orientation `u -> v`.
A vector `z` is in the right kernel of the row matrix precisely when it
satisfies (2) on every edge.

Choose a root and a spanning tree.  Starting with `z_root=1`, equation (2)
determines one nonzero value at every vertex.  A non-tree edge either agrees
with those values or does not.

* If one edge disagrees, no nonzero kernel vector exists.  Connectivity then
  gives full column rank.
* If every edge agrees, the propagated vector is a nonzero kernel vector.
  Every kernel vector is determined by its root value, so the kernel is
  one-dimensional and the row rank is `|V(G)|-1`.

Equivalently, for a directed cycle

\[
 v_0\mathbin{\mathop{-}^{e_0}}v_1\mathbin{\mathop{-}^{e_1}}
 \cdots\mathbin{\mathop{-}^{e_{r-1}}}v_r=v_0,
\]

the signed holonomy is the product of the successive transition factors in
(2).  The component has a surviving charge exactly when every such product
is one.  It is enough to test a cycle basis.

The unique functional is literal, not a dimension count.  If `t` is any
target or residual row on the same matching-class columns, then

\[
                        t\in\operatorname{rowspan}(f_e)
                  \quad\Longleftrightarrow\quad
                        \langle z,t\rangle=0.             \tag{3}
\]

Hence a nonzero value in (3) is the exact Fitting/unit certificate sought by
the global transport route.

## 2. The plus-hafnian specialization

Suppose each `a_e,b_e` is an active matching monomial with coefficient `+1`,
and the exponent ratios integrate around every cycle.  Their monomial parts
can be absorbed into column potentials.  Each traversal in (2) then
contributes only a minus sign.

Therefore compatible holonomy is possible precisely when the component is
bipartite.  Its cokernel vector is `+1` on one shore and `-1` on the other,
up to the absorbed monomial potentials.  A nonbipartite component contains
an odd cycle and is full rank in characteristic zero.  For a simple odd
cycle, this recovers

\[
                         \det M=2\prod_e m_e.             \tag{4}
\]

The theorem also covers coefficient characters: a complex phase can change
the holonomy, but it cannot create more than the same one-dimensional
terminal charge when all cycles are compatible.

## 3. Exact four-site core charge

Let `U,V,W` be the three perfect matchings of a four-site core.  Suppose two
source-labelled routes are available:

\[
                             U+V=0,\qquad V+W=0.           \tag{5}
\]

Their row matrix and unique charge are

\[
 \begin{pmatrix}1&1&0\\0&1&1\end{pmatrix},
               \qquad z=(1,-1,1).                        \tag{6}
\]

The second route is a genuine extra hypothesis.  A zero-Fitting two-row
block factors to one relation `U+V=0`; it does not automatically supply
`V+W=0`.  Before a second physical route is constructed, `W` is a separate
column component and there is no one-dimensional three-column charge to
which the calculation below can be applied.

The missing route and the full uncrossed hafnian have pairings

\[
 \langle z,W+U\rangle=2,
 \qquad
 \langle z,U+V+W\rangle=1.                               \tag{7}
\]

Thus the third pair route gives the familiar determinant-two unit.  More
importantly, if the complete physical top row is to survive without that
route, its two-cross/four-cross debt must carry charge exactly `-1` (or the
correspondingly scaled value before Laurent normalization).  The debt is no
longer merely "some contamination": it is forced to cancel a specified
one-dimensional class.

By
[`oo-four-site-core-cross-debt.md`](oo-four-site-core-cross-debt.md), the
physical top-row debt is `[xQ]_4+C_4`, where `Q=C_2` is the boundary
two-tensor and `x` is the internal quadratic on the other shore.
Independently, the canonical pair-conversion comparison reconstructs the
divided-square term `Q^[2]/h`; after clearing the active denominator its
non-pairwise residue is

\[
                              hC_4-Q^{[2]}.                \tag{8}
\]

Thus (8) is the general fourth-cumulant numerator.  In the additional
factorized four-star subclass recorded in the cross-debt note, its `h=0`
specialization is the negative of the eight repeated-label sectors of the
multisite one-bad cap.  A dense physical `U+V=0` counterguard in that note
does not admit the factorized signature, so zero Fitting alone does not
identify the arbitrary OO packet with that one-bad specialization.

There is an important scope boundary here.  The binomial-SCC calculation
proves that the critical component has one terminal charge, and the product-
cap calculation proves that (8) is the canonical non-pairwise residue.  It
does **not** supply the second route, construct a source-labelled map
identifying the resulting charge with the class of (8), or prove a
factorized four-star signature.  Those are separate missing physical steps.

## 4. Proof impact

The connected binomial subbranch in which a second four-core route has
already been sourced has an exact decision interface:

* a nontrivial cycle holonomy is already a unit;
* the third core route has charge two and is already a unit;
* otherwise there is one terminal charge, while (8) is the canonical
  crossed-debt residue that must be compared with it.

The proof-completing statement is therefore narrower than a global Fitting
calculation:

> Starting from one zero-Fitting route, use the full crossed ledger either
> to source a second core route or to close/descend the packet directly.  In
> the two-route case, construct the source-labelled comparison from the
> terminal binomial-SCC charge to the pair-conversion residue
> `hC_4-Q^[2]`; then kill or transport the resulting class.

The factorized `h=0` specialization meets the multisite one-bad defect, but
the arbitrary one-bad concentration theorem and the arbitrary OO packet
both require additional source provenance.  Six- and eight-site alternating
cores remain separate, as do non-binomial rows before peeling.  The result
here is a conditional positive reduction, not a proof of those assertions
or of Krenn's conjecture.

## Verification

Run

```text
.venv/bin/python computations/verify_oo_binomial_scc_holonomy_cokernel.py
.venv/bin/python -O computations/verify_oo_binomial_scc_holonomy_cokernel.py
```

The checker exhausts all 27,475 connected simple graphs on two through six
vertices and verifies that the signless incidence rank is `n-1` exactly for
bipartite graphs and `n` otherwise.  It separately audits general rational
coefficient packets, destroys one cycle holonomy and observes full rank,
and checks every pairing in (6)--(7).  Its frozen ledger is

```text
6eaa20c695eea7d925fc866bf3d59b328c27f01e601dc079cb4af17af851d495
```
