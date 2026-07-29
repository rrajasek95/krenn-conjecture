# Higher epsilon powers, local `SL(3)` webs, and permanent bridge holes

## Outcome

Taking powers of the ordinary three-copy alternating invariant does **not**
repair the Petersen escape in the selected-triple rewrite.  More generally,
if `G` is a locally-rainbow cubic occurrence network, every nonzero block in
the ordinary `m`th power would itself be a decomposition of `G` into three
perfect matchings.  Thus a snark monomial remains absent at every power.

Allowing a different degree-`3m` epsilon-bracket contraction at each vertex
is genuinely stronger.  Edmonds' perfect-matching polytope shows that a
connected cubic graph has an incidence decomposition

\[
                 m\mathbf 1_{E(G)}=\sum_{j=1}^{3m}\chi_{M_j}       \tag{1}
\]

for some graph-dependent `m` exactly when it is bridgeless.  The endpoint
port labels can then be accommodated by local bracket partitions.  For the
decorated Petersen state from `notes/triple-matching-rewrite.md`, `m=2`
works, and an explicit degree-six local web has collected Petersen-square
coefficient `2` and target value `-6`.  Thus this is not merely a fractional
or pre-symmetrization observation: a genuine polynomial local invariant sees
the Petersen square.

There is nevertheless a permanent all-degree obstruction.  An exact
six-vertex binomial selected rewrite can produce a locally-rainbow cubic
**occurrence** network with a bridge, even though the full underlying pair
support is the 3-connected triangular prism.  Every perfect matching of the
replacement state uses the bridge.  Consequently (1) fails for every
positive `m`, and the pure power of that replacement monomial occurs in no
local epsilon-bracket web of any degree.

Hence neither ordinary powers nor the full local bracket hierarchy closes
all selected-triple rewrites.  Higher webs remove the particular Petersen
hole, but occurrence-level bridges give exact permanent holes.  This is a
counterexample to the proposed saturation step, not a counterexample to
Krenn's conjecture.

## 1. Local bracket invariants

Let `V=C^3`, with alternating form `epsilon`, and let

\[
                     T\in\bigotimes_{v\in B}V_v.            \tag{2}
\]

Fix `d=3m`.  At every vertex `v`, partition the global copy slots
`[d]={0,...,d-1}` into `m` ordered triples:

\[
                  \Pi_v=\{B_{v,1},\ldots,B_{v,m}\}.          \tag{3}
\]

The corresponding local bracket form is

\[
 \eta_{\Pi_v}(x_0,\ldots,x_{d-1})
   =\prod_{a=1}^m\epsilon\bigl(x_j:j\in B_{v,a}\bigr),       \tag{4}
\]

where the displayed order inside a block fixes its sign.  Define

\[
 J_{\boldsymbol\Pi}(T)
   =\left(\bigotimes_{v\in B}\eta_{\Pi_v}\right)
      \left(T^{\otimes d}\right).                            \tag{5}
\]

This is a homogeneous degree-`3m` polynomial invariant for the local
`SL(3)^B` action.  Products of epsilon brackets span the local invariant
space in this degree; web straightening only introduces linear relations
among forms of the shape (4).

If every `Pi_v` is the same standard partition

\[
 (012)\mid(345)\mid\cdots\mid(3m-3,3m-2,3m-1),              \tag{6}
\]

then (5) is the ordinary power

\[
                 J_{\boldsymbol\Pi}(T)=I_B(T)^m,
 \qquad I_B(T)=\epsilon^{\otimes B}(T,T,T).                 \tag{7}
\]

The freedom to vary `Pi_v` with `v` is therefore precisely the extra freedom
which ordinary powers do not use.

## 2. Decorated cubic monomials and ordinary-power rigidity

An occurrence `e=uv` consists of a nonzero aggregate coordinate

\[
        z_e=A_{uv}(\ell_u(e),\ell_v(e)),\qquad
        \ell_u(e),\ell_v(e)\in\{0,1,2\}.                    \tag{8}
\]

Let `G` be a cubic occurrence multigraph such that, at every vertex `v`, its
three incident occurrences have the three distinct local labels `0,1,2`.
Put

\[
                         w_G=\prod_{e\in E(G)}z_e.           \tag{9}
\]

Parallel occurrences on the same underlying pair are allowed as long as
they are different aggregate coordinates.  This is the exact object
produced by the selected-triple rewrite.

**Proposition 2.1 (ordinary powers do not saturate a snark ray).**
Let `c_G` be the coefficient of `w_G` in the source pullback
`I_B(H_B(A))`.  Then

\[
        [w_G^m]\,I_B(H_B(A))^m=c_G^m.                       \tag{10}
\]

In particular, if `G` has no decomposition into three perfect matchings,
then the coefficient in (10) is zero for every `m>=1`.

**Proof.**  A nonzero epsilon block uses one occurrence of each local port
label at every vertex.  Inside the support of `G`, there is exactly one
incident occurrence of each such label.  Hence every one of the `m` blocks
which contributes to the exponent vector `m\mathbf1_{E(G)}` is forced to
use every occurrence of `G` exactly once.  Its three global copy slots are
perfect matchings, so this block is a three-one-factor decomposition of
`G`.  Different blocks cannot exchange exponents: the unique occurrence at
each local port is used once in every block.  Thus the only contribution to
`w_G^m` is the product of `m` copies of the coefficient of `w_G`, proving
(10).  If `G` is not three-edge-colourable, there is no source term even
before collecting signs, so `c_G=0`. `QED`

The Petersen replacement is therefore absent from every ordinary power,
not just from the original three-copy expansion.  This conclusion uses the
endpoint port labels; treating the cubic network as an unlabelled edge
incidence vector loses the block-by-block forcing.

## 3. What arbitrary local webs can recover

For a general choice of local partitions, a source term contributing to
`w_G^m` consists of `3m` ordered perfect matchings and necessarily obeys
(1).  Conversely, suppose (1) holds.  At a fixed vertex, exactly `m` of the
matching slots use each of its three incident port occurrences.  Partition
the slots into `m` transversals of these three `m`-element classes.  Using
these transversals as `Pi_v` makes the chosen source term nonzero in every
local bracket.

One can simultaneously arrange a nonzero *raw* target term.  Colour the
`3m` global slots with `m` copies of each target colour.  At a vertex, form
the `3 by 3` count matrix between its source port classes and these global
target-colour classes.  All row and column sums are `m`, so the integer
Birkhoff decomposition partitions it into `m` permutation matrices.  Those
permutations give bracket blocks which are rainbow both for the chosen
source term and for the chosen constant-colour term of `Delta^{tensor 3m}`.
Collection can still introduce signs; Section 4 verifies directly that it
does not do so for one explicit Petersen web.

The graph-theoretic content of (1) is exact.

**Proposition 3.1 (Edmonds criterion for a scaled cubic state).**
For a connected cubic graph `G`, equation (1) holds for some positive integer
`m` if and only if `G` is bridgeless.

**Proof.**  If (1) holds, divide it by `3m`.  The uniform vector
`x_e=1/3` is a convex combination of perfect-matching incidence vectors.
It therefore satisfies every odd-cut inequality of the perfect-matching
polytope.  A bridge in a cubic graph separates an odd shore, and its cut has
`x`-weight `1/3`, a contradiction.

Conversely, assume `G` is bridgeless.  The uniform vector has
`x(delta(v))=1` for every vertex.  For every odd shore `S`, cubic parity
gives

\[
                    |\delta(S)|\equiv |S|\pmod2.            \tag{11}
\]

Thus its cut has odd size; bridgelessness excludes size one, so
`|delta(S)|>=3` and `x(delta(S))>=1`.  Edmonds' description of the
perfect-matching polytope puts `x` in that polytope.  Its vertices and `x`
are rational, so clear the denominators in a convex decomposition of `x`.
After also making the common denominator divisible by three, one obtains
(1). `QED`

The integer `m` supplied by this proof is graph-dependent.  In particular,
the assertion that `m=2` always works is precisely the six-perfect-matching
double-cover assertion for bridgeless cubic graphs.  Edmonds' theorem alone
does not provide a uniform all-order web degree.

## 4. A degree-six web which sees the Petersen square

Use the decorated Petersen replacement from
`notes/triple-matching-rewrite.md`.  In the following order, its six perfect
matchings are

\[
\begin{aligned}
 L_0&=01|23|47|56|89, &L_1&=01|26|34|59|78,\\
 L_2&=04|12|39|56|78, &L_3&=04|18|23|59|67,\\
 L_4&=05|12|34|67|89, &L_5&=05|18|26|39|47.
\end{aligned}                                               \tag{12}
\]

Every Petersen edge occurs in exactly two of these matchings.  Moreover,
the unique nonnegative integer solution which uses six matchings in total
and gives multiplicity two to every edge uses each `L_j` once.

For slots `0,...,5`, write `(abc|def)` for
`epsilon(x_a,x_b,x_c)epsilon(x_d,x_e,x_f)`.  Take the following local
degree-six brackets at vertices `0,...,9`:

\[
\begin{array}{c|c@\qquad c|c}
v&\Pi_v&v&\Pi_v\\ \hline
0&(025|134)&5&(015|234)\\
1&(023|145)&6&(013|245)\\
2&(025|134)&7&(023|145)\\
3&(015|234)&8&(023|145)\\
4&(013|245)&9&(015|234).
\end{array}                                                 \tag{13}
\]

Let `J_P` denote (5) for (13), with each displayed block ordered as written.
An exact enumeration gives

\[
                    J_P(\Delta_{10,3})=-6,                  \tag{14}
\]

and, in the source pullback,

\[
                 [w_{\rm Pet}^2]J_P(H_{10}(A))=2.           \tag{15}
\]

For (14), the enumeration is over the `3^6` assignments of a constant target
colour to each global copy slot.  For (15), uniqueness of the incidence
multiset reduces the calculation to the `6!` orders of (12).  Both are
signed integer sums; hence (14)--(15) verify that neither target collection
nor source symmetrization cancels the witness.

This cleanly separates ordinary powers from local web straightening:
`I_B^2` uses the same two slot triples at every site and has Petersen-square
coefficient zero by Proposition 2.1, while the vertex-dependent brackets
(13) have coefficient two.

## 5. An exact binomial replacement with a permanent bridge

The stronger obstruction already occurs on six vertices.  Select three
constant-colour matchings, all with unit occurrence weights,

\[
\begin{aligned}
 P_0&=04|12|35,\\
 P_1&=05|14|23,\\
 P_2&=03|15|24.
\end{aligned}                                               \tag{16}
\]

Their occurrence union is the triangular prism.  It contains the mixed
perfect matching

\[
 R=04_{00}|15_{22}|23_{11},\qquad
 c=(0,2,1,1,0,2).                                           \tag{17}
\]

Add two aggregate cells on already present underlying pairs,

\[
                    A_{12}(2,1)=-1,\qquad
                    A_{35}(1,2)=1.                           \tag{18}
\]

Together with the selected cell `A_04(0,0)=1`, they form the same-colouring
matching

\[
             N=04_{00}|12_{21}|35_{12},\qquad z(N)=-1.      \tag{19}
\]

The complete `c`-fibre consists of exactly `R` and `N`, with weights `1`
and `-1`.  Indeed, the port at vertex zero forces `04`, after which the four
remaining vertices have precisely the two displayed completions.  The
three constant fibres remain unique with coefficient one because the added
cells are off diagonal.  This is therefore an exact binomial instance of
the selected-triple rewrite.

Put `Q=(P_0 union P_1 union P_2) setminus R`.  The two-factor `Q` is the
disjoint union of the triangles

\[
                         0-3-5-0,\qquad1-2-4-1.             \tag{20}
\]

The replacement occurrence state

\[
                              G_{\rm br}=Q\sqcup N           \tag{21}
\]

is locally rainbow.  It has parallel occurrences on `12` and `35`, carrying
different endpoint labels, and the occurrence `04_00` is its unique edge
between the two shores in (20).  Hence it is a bridge.  There are exactly
four occurrence-perfect-matchings of `G_br`; all contain `04_00`.

Now consider any degree `3m` local bracket web.  A term with monomial
`w_{G_br}^m` would require `3m` perfect matchings supported on `G_br`.  Each
would use the bridge, so the exponent of its coordinate would be `3m`.
The requested monomial has bridge exponent only `m`.  This contradiction
proves

\[
 [w_{G_{\rm br}}^m]J_{\boldsymbol\Pi}(H_6(A))=0
 \quad\text{for every }m\ge1\text{ and every }
 \boldsymbol\Pi.                                            \tag{22}
\]

Notice that the added cells in (18) introduce no new underlying pair.  The
full pair support is still the 3-connected triangular prism.  Thus
3-connectivity, matching-coveredness, and bridge-freeness of the aggregate
pair support do not remove an occurrence-level bridge from an individual
rewrite state.

## 6. Consequence for radical and rewrite strategies

Multiplying the binomial mixed-fibre equation in Section 5 by the unchanged
two-factor monomial gives the exact selected-state relation

\[
                         w_U+w_{G_{\rm br}}=0.               \tag{23}
\]

Nevertheless, (22) says that the entire pure ray
`w_(G_br)^m`, `m>=1`, is absent from the term support of every local bracket
invariant.  Thus taking powers does not put this cancellation mate into the
saturation of the epsilon/web monomial support.  The Petersen state is a
hole only for ordinary aligned powers and is repaired by (13); the bridged
state is a hole for the full local bracket hierarchy.

This does not prove that no source-ideal certificate can combine several
states or use non-invariant covariants.  It proves the narrower and reusable
negative statement needed here: a certificate cannot be obtained merely by
powering selected-triple relations until every pure replacement monomial
becomes a rainbow matching tuple in some `SL(3)` bracket web.  Any successful
continuation must either control combinations of different replacement
states, eliminate occurrence-level bridges by additional target equations,
or use source information outside the local invariant web algebra.

The dependency-free exact audit is
`computations/verify_higher_epsilon_web_saturation.py`.  It verifies the Petersen
two-cover, the degree-six values (14)--(15), the complete six-vertex
binomial fibre, and the forced bridge in all four replacement-state perfect
matchings.
