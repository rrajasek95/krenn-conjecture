# Finite versus border: an exact localized certificate and a GIT obstruction

## Outcome

There is a new arbitrary-matrix finite obstruction.  At any vertex with only
three nonzero underlying neighbors, exact equality forces the three incident
`3 by 3` matrices to be nonzero rank-one same-color basis tensors, using the
three colors once each.  It follows that no 3-regular matrix support can
realize the target for any even `n >= 6`.  At six vertices it also rules out
the triangular prism after **any one** of its six complementary pairs is
adjoined, even though the added matrix is completely arbitrary.  Thus the
known border point cannot be repaired by turning on just one new pair.

There is a simple degree-nine Nullstellensatz certificate on the sparse
diagonal triangular-prism chart.  It is genuinely parameter-dependent and
records exactly the `zero times infinity` mechanism of the known border
family.

There is also an exact obstruction to a tempting way of globalizing that
certificate.  For arbitrary edge matrices and every even number of vertices,
an exact three-color realization would necessarily be semistable for the
local `SL(3)` action: an explicit family of source invariants has sum `6` on
the target.  Moreover, the six-vertex prism border family is contained in a
single orbit of a one-parameter subgroup which both lies in the local
`SL(3)` group and stabilizes the target.  Consequently **every polynomial
invariant, and every invariant rational function where defined, is constant
along this degeneration**.  The prism source also has a nonzero degree-nine
invariant equal to `1` throughout.  Thus neither a nullcone argument nor the
invariant-theoretic quotient can distinguish the finite points from this
border limit.  Any successful Kempf--Ness/GIT proof has to retain a
non-invariant covariant or a gauge slice whose denominator develops a pole.

This note does not claim the still-missing all-support obstruction.  It gives
arbitrary-matrix rigidity on two substantial sparse classes, a proved
low-degree certificate on the basic chart, and an exact falsification of the
most direct invariant-theory route.

## 1. Setup

Let `B` have even cardinality `n=2m`, let each `V_v` be a copy of
`C^3`, and put

\[
 W=\bigoplus_{u<v}V_u\otimes V_v.
\]

An element `A=(A_uv)` of `W` is the collection of completely arbitrary
aggregate endpoint-color matrices.  Its matching tensor is the homogeneous
degree-`m` polynomial map

\[
 \Phi(A)=\sum_{M\in\operatorname{PM}(B)}
          \bigotimes_{uv\in M}A_{uv}
 \in\bigotimes_{v\in B}V_v.                                  \tag{1}
\]

This is the exact aggregated model, so no rank, symmetry, same-color, or
positivity assumption is made here.  Write

\[
 \Delta=\sum_{i=0}^2 e_i^{\otimes B}.                          \tag{2}
\]

The group

\[
 G=\prod_{v\in B}\operatorname{SL}(V_v)                       \tag{3}
\]

acts naturally on both spaces, and (1) is `G`-equivariant.

## 2. Epsilon invariants rule out a source-nullcone proof

Fix alternating volume forms `epsilon_v` with
`epsilon_v(e_0,e_1,e_2)=1`.  For an ordered triple of perfect matchings

\[
 \mathbf M=(M^{(0)},M^{(1)},M^{(2)}),
\]

take one copy of every edge tensor appearing in every matching, reorder the
three incident `V_v` factors at each vertex by the superscript `0,1,2`, and
define

\[
 I_{\mathbf M}(A)=
 \left(\bigotimes_{v\in B}\epsilon_v\right)
 \left(\bigotimes_{r=0}^2\ \bigotimes_{uv\in M^{(r)}}A_{uv}\right).
                                                                    \tag{4}
\]

Repeated underlying edges cause no problem: (4) simply uses multiple copies
of the same matrix.  It is a homogeneous polynomial of degree `3m` in the
source entries.

**Lemma 2.1 (exact semistability certificate).**  Each polynomial (4) is
`G`-invariant, and

\[
 \sum_{\mathbf M\in\operatorname{PM}(B)^3}I_{\mathbf M}(A)
 =\left(\bigotimes_{v\in B}\epsilon_v\right)
   \bigl(\Phi(A)^{\otimes3}\bigr).                             \tag{5}
\]

If all mixed coefficients of `Phi(A)` vanish and its three constant
coefficients are `p_0,p_1,p_2`, then, because `n` is even,

\[
 \sum_{\mathbf M}I_{\mathbf M}(A)=6p_0p_1p_2.                 \tag{6}
\]

In particular, if `Phi(A)=Delta`, then at least one genuine source invariant
`I_M(A)` is nonzero.

**Proof.**  At every vertex, `g_v in SL(V_v)` preserves `epsilon_v`, proving
the invariance of (4).  Expanding the three copies of the matching sum (1)
gives (5) term by term.  If the output is diagonal, a nonzero epsilon
contraction must use the three different constant-color summands.  The six
orders are indexed by `sigma in S_3`; each contributes

\[
 (\operatorname{sgn}\sigma)^n p_0p_1p_2=p_0p_1p_2,
\]

since `n` is even.  This proves (6). \(\square\)

Thus a hypothetical exact root cannot lie in the `G`-nullcone.  Indeed, the
left side of (5) is a nonzero invariant at such a root (and equals `6`).
Equivalently, if `0` lay in the closure of `G.A`, equivariance and continuity
would put `0` in the closure of `G.Delta`, contrary already to the nonzero
epsilon invariant of `Delta`.  This conclusion holds for arbitrary matrices
and every even `n`.

The sum in (5) factors through the output, so it is not being proposed as an
output obstruction.  Its role is the opposite: it exactly falsifies any
strategy whose missing step is that the mixed-coefficient equations force
all source invariants to vanish.

## 3. The prism border is one target-stabilizer orbit

Use vertices `0,...,5` and the three color matchings

\[
\begin{aligned}
 M_0&=\{04,12,35\},\\
 M_1&=\{05,14,23\},\\
 M_2&=\{03,15,24\}.
\end{aligned}                                                  \tag{7}
\]

Let `A_*` put the unit tensor `e_i tensor e_i` on every edge of `M_i` and
zero in every other coordinate.  The union has one additional perfect
matching

\[
 H=\{04,15,23\},
\]

and hence

\[
 \Phi(A_*)=\Delta+E,
 \qquad
 E=e_0\otimes e_2\otimes e_1\otimes e_1\otimes e_0\otimes e_2.
                                                                    \tag{8}
\]

Consider the following integer exponent matrix; rows are vertices and
columns are colors `0,1,2`:

\[
 (h_{v,i})=
 \begin{pmatrix}
  0&-1& 1\\
  1&-1& 0\\
  0& 1&-1\\
 -1& 1& 0\\
  0& 0& 0\\
  0& 0& 0
 \end{pmatrix}.                                                \tag{9}
\]

Every row sum and every column sum is zero.  Therefore

\[
 g_v(t)=\operatorname{diag}(t^{h_{v,0}},t^{h_{v,1}},t^{h_{v,2}})
                                                                    \tag{10}
\]

defines a one-parameter subgroup of `G`, and the column-sum conditions give

\[
 g(t)\Delta=\Delta.                                           \tag{11}
\]

On the nine nonzero coordinates of `A_*`, the exponents induced by (10) are

\[
\begin{array}{c|ccc}
0&04:0&12:1&35:-1\\
1&05:-1&14:-1&23:2\\
2&03:1&15:0&24:-1.
\end{array}                                                    \tag{12}
\]

The extra matching in (8) has total exponent `2`.  Equivariance now gives
the exact identity

\[
 \Phi(g(t)A_*)=g(t)(\Delta+E)=\Delta+t^2E.                    \tag{13}
\]

Thus the known border family is not merely explained by some abstract torus
scaling: it is contained in a single orbit of a one-parameter subgroup of
the local `SL(3)` group which fixes the target exactly.

It follows immediately that every polynomial `G`-invariant is constant on
the family (13).  The same is true for every invariant rational function at
points where it is defined.  It is also true for invariants of the larger
diagonal target-stabilizer torus

\[
 T_\Delta=\{(\lambda_{v,i}):\prod_v\lambda_{v,i}=1
                    \text{ for each }i\}.                     \tag{14}
\]

There is a particularly concrete degree-nine witness.  Order the three
matchings in (7) by their colors.  Then every local determinant in (4) is
`epsilon(e_0,e_1,e_2)=1`, and hence

\[
 I_{(M_0,M_1,M_2)}(g(t)A_*)
 =\prod_{e\in M_0\cup M_1\cup M_2}w_e(t)
 =\prod_{i=0}^2\prod_{e\in M_i}w_e(t)=1.                     \tag{15}
\]

Although some entries tend to zero and others to infinity, this source
invariant never tends to zero.

There is also no torus-support instability hidden here.  The nine coordinate
weights are `a_(uv;i)=e_(u,i)+e_(v,i)`.  Giving all nine weight `1` yields

\[
 \sum_{i=0}^2\sum_{uv\in M_i}a_{(uv;i)}
 =\sum_{v=0}^5\sum_{i=0}^2e_{v,i}.                            \tag{16}
\]

The right side pairs to zero with every cocharacter satisfying the three
column-sum conditions in (14).  Since every coefficient in (16) is strictly
positive, zero lies in the relative interior of the convex hull of the
projected support weights.  This is precisely the torus-polystable/balanced
condition.  Hence support minimization via Hilbert--Mumford cannot remove an
entry of this prism point.

## 4. The same failure persists for all even-order border families

The all-even border construction uses a properly three-edge-colored cubic
graph.  Its three color classes are perfect matchings `M_0,M_1,M_2`, the
only nonzero coordinate on an edge of `M_i` is its `(i,i)` entry, and each
color-matching product is normalized to `1`.

The same two calculations require no special feature of six vertices:

1. At every vertex there is exactly one selected occurrence of each color.
   Therefore equal positive coefficients on the support give the balanced
   vector `sum_(v,i)e_(v,i)`, just as in (16).
2. The degree-`3m` invariant attached to the ordered triple of color
   matchings is

   \[
    I_{(M_0,M_1,M_2)}(A(t))
      =\prod_{i=0}^2\prod_{e\in M_i}w_e(t)=1.                 \tag{17}
   \]

Consequently every border family produced by the vertex-to-triangle
expansion is supported on a torus-balanced point and carries a fixed nonzero
source invariant.  This applies for every even `n >= 6`.  A proposed global
finite-versus-border proof based only on showing torus imbalance or source
nullcone membership is therefore exactly falsified by the known family, not
merely left unproved.

## 5. Exact degree-nine certificate on the sparse prism chart

The preceding negative result does not erase the genuine localized
finite-versus-border obstruction.  Name the nine scalar diagonal entries

\[
\begin{array}{c|ccc}
0&a_{04}&a_{12}&a_{35}\\
1&b_{05}&b_{14}&b_{23}\\
2&c_{03}&c_{15}&c_{24}.
\end{array}
\]

Put

\[
\begin{aligned}
 p_0&=a_{04}a_{12}a_{35},\\
 p_1&=b_{05}b_{14}b_{23},\\
 p_2&=c_{03}c_{15}c_{24},\\
 r&=a_{04}c_{15}b_{23},\\
 q&=a_{12}a_{35}b_{05}b_{14}c_{03}c_{24}.
\end{aligned}                                                  \tag{18}
\]

Here `p_i` are the three constant output coefficients and `r` is the sole
mixed output coefficient.  Directly from the occurrence partition,

\[
 p_0p_1p_2=rq.                                                \tag{19}
\]

Let `f_i=p_i-1`.  The following polynomial identity over the integers is an
exact Nullstellensatz certificate:

\[
 \boxed{
 1=-f_0-p_0f_1-p_0p_1f_2+q r.}                               \tag{20}
\]

Indeed, the first three terms telescope to `1-p_0p_1p_2`, and (19)
supplies the remainder.  Thus the equations `p_0=p_1=p_2=1` and `r=0`
have no finite common zero on this chart.  The maximum source degree in
(20) is nine.

For the exponents in (12), `r=t^2` and `q=t^(-2)`, so `qr=1` identically.
The multiplier in the certificate is exactly the quantity which diverges at
the border.  Equivalently, on the nonvanishing chart `q != 0`, (19) is the
parameter-dependent rational obstruction

\[
 r=\frac{p_0p_1p_2}{q}.                                      \tag{21}
\]

This is the right shape for a finite-versus-border proof: it does not factor
through the output and its denominator records escape to infinity.  The
remaining global difficulty is that arbitrary matrices and additional
underlying pairs give several matching monomials in a mixed coefficient;
then the distinguished `r` in (19) may cancel inside that coefficient, and
the simple certificate (20) no longer belongs to the full mixed-coefficient
ideal.  The arbitrary-matrix rigidity theorem for the *nine-edge prism
support* in `notes/combinatorial-route.md` handles that one support by a
separate quotient-and-rank argument.  Neither result yet controls the
cancellation chains created by additional pairs.

## 6. Consequence for the next round

The exact facts above narrow the viable algebraic route:

* Do not try to prove that a hypothetical exact source is unstable for
  `SL(3)^B`; Lemma 2.1 proves the opposite.
* Do not expect the target-stabilizer quotient or Kempf--Ness normalization
  alone to expose the prism divergence; (9)--(15) show that the entire
  degeneration is one invariant-theoretic orbit with fixed nonzero
  invariants.
* A usable rational invariant must be a semi-invariant/covariant tied to a
  selected nonvanishing chart, or an ideal-membership certificate whose
  source multiplier has a pole along every border degeneration, as `q` does
  in (20).
* To globalize (20), one must control the extra terms in each mixed
  coefficient rather than replace that coefficient by a selected matching
  monomial.  That cancellation-control step is exactly the unresolved
  finite-versus-border problem.

## 7. Cubic-vertex rigidity and the prism plus one pair

The following lemma is independent of the prism and holds for arbitrary
matrices at every even order.

**Lemma 7.1 (cubic-vertex rigidity).**  Suppose `Phi(A)=Delta` for even
`n >= 6`, and a vertex `p` has only three possibly nonzero underlying
neighbors `j_0,j_1,j_2`.  Then, after indexing the neighbors suitably,

\[
 A_{p j_s}=w_s e_{r_s}^{(p)}\otimes e_{r_s}^{(j_s)},
 \qquad w_s\ne0,                                             \tag{22}
\]

where `(r_0,r_1,r_2)` is a permutation of `(0,1,2)`.

**Proof.**  The star expansion at `p` has three terms:

\[
 \Delta=\sum_{s=0}^2 A_{p j_s}\otimes
          H_{B\setminus\{p,j_s\}}.                           \tag{23}
\]

No displayed term can vanish, since otherwise the partition rank of the
right side would be at most two, whereas the diagonal tensor has partition
rank three.

Let `R=B\setminus\{p,j_0,j_1,j_2\}`.  For a covector `lambda` at `p` whose
three coordinates `lambda_i=lambda(e_i)` are nonzero, contract the sites in
`R` by

\[
 K_\lambda=\sum_{i=0}^2\lambda_i^{-1}(e_i^*)^{\otimes R}.
                                                                    \tag{24}
\]

After also contracting `p` by `lambda`, the left side of (23) becomes
`Delta_(3,3)` on the three neighbor sites.  The right side is a sum of three
slice terms, centered at the three different sites, whose center vectors are

\[
 L_s(\lambda)=(\lambda\otimes\operatorname{id})A_{p j_s}.
                                                                    \tag{25}
\]

The three-slice center lemma proved in `notes/tensor-route.md`, (25a)--(25b),
says that the three vectors (25) are nonzero multiples of three distinct
coordinate vectors.

This holds for every `lambda in (C^*)^3`.  For two distinct output
coordinates `a,b`, the product
`(L_s(lambda))_a (L_s(lambda))_b` therefore vanishes on the dense torus.
It is a polynomial, so it vanishes identically.  Since a polynomial ring is
an integral domain, at most one coordinate linear form of `L_s` is nonzero.
Thus `L_s` has a fixed coordinate image line and

\[
 A_{p j_s}=a_s\otimes e_{t_s}
\]

has rank one.  Moreover, (25) never vanishes on the torus.  A linear form
with two or more nonzero coefficients has a zero in `(C^*)^3`; hence `a_s`
is itself a multiple of one coordinate vector.  Mode rank three at `p`
forces the three resulting colors there to be distinct.  Finally contract
(23) at `p` by the dual vector selecting one of these colors.  Exactly one
term remains and equals `e_r^(tensor (n-1))`; its factor at `j_s` is
`e_(t_s)`, so `t_s=r`.  This proves (22). \(\square\)

This immediately gives an all-even arbitrary-matrix support theorem.

**Corollary 7.2 (3-regular supports are impossible).**  For every even
`n >= 6`, no collection of arbitrary aggregate matrices whose nonzero
underlying support graph is 3-regular can satisfy `Phi(A)=Delta`.

**Proof.**  Lemma 7.1 makes every supported matrix a same-color basis tensor,
and the three incident colors at every vertex are distinct.  The three color
classes are therefore perfect matchings `M_0,M_1,M_2`.  Any supported
perfect matching induces a unique coloring: at a vertex, its color selects
its unique incident edge.  Hence distinct matching terms cannot cancel.

It remains only to produce a fourth perfect matching.  This is
**Bogdanov's observation** (Bogdanov 2017), published as Thm 1 of
Chandran-Gajjala, arXiv:2202.05562, and in multigraph form as Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303; see
[`references/REFERENCES.md`](../references/REFERENCES.md).  **No priority
is claimed**: we give a self-contained proof only because the audit
discipline of this repository requires every consumed statement to be
either cited to a checked source or proved inside the artifact.  The
union
`M_0 union M_1` is a disjoint union of alternating even cycles.  If it has
at least two components, switch from `M_0` to `M_1` on a nonempty proper
set of components.  If it is one Hamilton cycle `C`, consider an edge of
`M_2`.  If one joins opposite parities on `C`, use it and match the two even
paths left over along `C`.  Otherwise `M_2` separately matches the even and
odd positions.  An even-position chord and an odd-position chord must
interlace.  Indeed, if no such pair interlaced, each chord would have an even
number of opposite-parity vertices on either side and hence would join
positions congruent modulo `4`.  Apply the same argument inside each pair of
adjacent residue classes to force congruence modulo `8`, then modulo `16`,
and so on.  At each stage the residue classes are internally perfectly
matched and therefore have even size, so this iteration would force `n` to
be divisible by arbitrarily large powers of two.  This is impossible.  Two
interlacing chords leave four even paths of `C`;
matching those paths along the cycle gives the required fourth perfect
matching.

The new matching uses more than one edge color, so its induced coloring is
mixed, and its coefficient is one nonzero monomial with no possible
cancellation. \(\square\)

At six vertices the cubic lemma survives one additional pair beyond the
prism.

**Theorem 7.3 (prism plus one arbitrary pair).**  Let

\[
 P=\{03,04,05,12,14,15,23,24,35\}.                           \tag{26}
\]

If every matrix outside `P union {e}` is zero, where `e` is any one of the
six pairs complementary to `P`, then no choices of the ten arbitrary
asymmetric `3 by 3` matrices realize `Delta_(6,3)`.

**Proof.**  By prism symmetry it is enough to take `e=01`.  The four prism
matchings and the sole new matching are

\[
\begin{aligned}
 M_A&=\{03,15,24\},&M_B&=\{04,12,35\},\\
 M_D&=\{04,15,23\},&M_C&=\{05,14,23\},\\
 N&=\{01,24,35\}.                                            \tag{27}
\end{aligned}
\]

Vertices `2,3,4,5` still have only three neighbors.  Lemma 7.1 therefore
forces every matrix on a prism edge to be a nonzero same-color basis tensor,
with three distinct incident colors at those four vertices.  Only `A_01`
remains arbitrary.

Permute colors so that the colors on `12,23,24` are `0,1,2`.  Denote the
colors on

\[
 (03,04,05,12,14,15,23,24,35)
\]

by `(a,b,c,0,e,f,1,2,i)`.  Properness at vertices `3,4,5` gives

\[
 \{a,i\}=\{0,2\},\qquad \{b,e\}=\{0,1\},\qquad
 \{c,f,i\}=\{0,1,2\}.                                      \tag{28}
\]

If `i=0`, then `a=2`, `{c,f}={1,2}`, and `{b,e}={0,1}`.  The
new matching `N`, regardless of `A_01`, is supported only on colorings

\[
 (*,*,2,0,2,0).                                               \tag{29}
\]

The all-2 coefficient can only come from `M_A`, forcing `f=2,c=1`.
The all-0 coefficient can only come from `M_B`, forcing `b=0,e=1`.
Then `M_C` is all 1, while `M_D` has the mixed coloring
`(0,2,1,1,0,2)`.  Its nonzero monomial cannot be canceled by `N`, whose
fixed coordinates (29) disagree.

If `i=2`, then `a=0`, `{c,f}={0,1}`, and `{b,e}={0,1}`.  Matching `N`
can be monochromatic only in color 2.  Matching `M_A` contains colors 0 and
2, as does `M_B`; and `M_C,M_D`, which contain edge `23`, can be
monochromatic only in color 1.  No term supplies the required all-0
coefficient, again a contradiction.

Finally, the complement of `P` is a six-cycle.  Its automorphism group is
transitive on its edges and also preserves its complement `P`, proving the
claim for every complementary pair. \(\square\)

The full proof is also isolated in
`proofs/prism-plus-one-edge-obstruction.md`.  The script
`computations/verify_prism_plus_one_combinatorics.py` independently
enumerates all `3^9` prism edge-color assignments, retains the 48 assignments
proper at the four cubic vertices, and checks the obstruction exactly.
