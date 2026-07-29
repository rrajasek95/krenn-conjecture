# Two-vertex annihilation: the anchor tautology and the one-hole strengthening

## 1. Outcome and scope

Let `B` be an even set, `|B|=n>=4`, let every ordered pair of distinct
vertices carry an aggregate matrix

\[
 A_{xy}\in V_x\otimes V_y\simeq \mathbb C^{3\times3},
 \qquad A_{yx}=A_{xy}^{T},                                  \tag{1}
\]

and suppose

\[
 H_B(A)=\sum_{M\in\operatorname{PM}(B)}\ \bigotimes_{xy\in M}A_{xy}
       =\Delta_{B,3}:=\sum_{r=0}^2e_r^{\otimes B}.          \tag{2}
\]

This note proves three exact identities obtained by annihilating all
matchings which avoid a fixed edge `pq`.

The first, most obvious identity says that a bilinear polynomial divides a
three-term product sum.  The forced incident-edge theorem of
`notes/slice-cover.md` makes that divisibility completely tautological.  It
therefore gives no new obstruction by itself.

Leaving one outside site uncontracted is substantially sharper.  It splits
the three-term relation into three separate monomial divisibilities.  In
particular, if `rank A_pq>=2`, then for each color `r` there are at least two
different outside vertices `u` for which

\[
 A_{pu}K_rA_{qu}^{T}\in\mathbb C A_{pq}.                   \tag{3}
\]

If `A_pq` is invertible, both matrices in (3) must be zero.  A two-hole
identity further implies that the vertices supporting the proportionalities
(3), as `r` varies, cannot be confined to only two outside vertices.

These are uniform necessary conditions for every even `n>=4`, with no
genericity, support, rank-one, or minimality assumption.  They do not by
themselves finish the conjecture: distinct forced anchors often supply the
required zero matrices automatically.  Section 8 isolates exactly the
anchor-collision branches in which the new conditions add information.

## 2. Orientation and cross-product convention

Matrices are always oriented by their displayed order: rows of `A_xy` are
at `x` and columns are at `y`.  For row vectors `a,b`, put

\[
 (a\mathbin\times b)_r=aK_rb^T,                             \tag{4}
\]

where

\[
K_0=\begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix},\quad
K_1=\begin{pmatrix}0&0&-1\\0&0&0\\1&0&0\end{pmatrix},\quad
K_2=\begin{pmatrix}0&1&0\\-1&0&0\\0&0&0\end{pmatrix}.  \tag{5}
\]

Thus (4) is the standard cross product

\[
 a\times b=(a_1b_2-a_2b_1,\ a_2b_0-a_0b_2,\
             a_0b_1-a_1b_0),                              \tag{6}
\]

and it annihilates both `a` and `b` under the coordinate dot product.

Fix different vertices `p,q`, write

\[
 R=B\setminus\{p,q\},\qquad m=|R|=n-2,                    \tag{7}
\]

and choose covectors `alpha` at `p` and `beta` at `q`.  Define

\[
 \begin{split}
 g(\alpha,\beta)&=\alpha^TA_{pq}\beta,\\
 a_u(\alpha)&=\alpha^TA_{pu},\\
 b_u(\beta)&=\beta^TA_{qu},\\
 \gamma_u(\alpha,\beta)&=a_u(\alpha)\times b_u(\beta)
 \quad(u\in R).
 \end{split}                                               \tag{8}
\]

In particular,

\[
 \gamma_{u,r}=\alpha^TC_{u,r}\beta,
 \qquad C_{u,r}:=A_{pu}K_rA_{qu}^T,                        \tag{9}
\]

which audits both transposes in the coefficient matrix.  Notice that
`rank C_{u,r}<=2`.

## 3. The no-hole identity and all rank-degenerate divisor cases

Contract (2) by `alpha,beta`, and by `gamma_u` at every `u in R`.  A
matching avoiding `pq` matches `p` to some `u` and `q` to a different
`v`.  Its `pu` factor is zero because
`a_u dot gamma_u=0` (and its `qv` factor is zero as well).  The surviving
matchings are exactly `pq` followed by a perfect matching of `R`.  Hence the
following is a polynomial identity, not merely an equality on a hypersurface:

\[
 \boxed{
 \sum_{r=0}^2\alpha_r\beta_r\prod_{u\in R}\gamma_{u,r}
 =g(\alpha,\beta)\,
   \left\langle H_R(A),\bigotimes_{u\in R}\gamma_u\right\rangle .}
                                                                    \tag{10}
\]

Call the left side `F_pq`.  Formula (10) immediately gives the following
complete rank audit.

**Lemma 3.1 (divisibility in every rank).**

* If `rank A_pq>=2`, the polynomial `g` is irreducible and `g|F_pq`.
* If `rank A_pq=1`, write `A_pq=ab^T`.  Then
  `g=(alpha^Ta)(b^T beta)`; the two relatively prime linear factors both
  divide `F_pq`, and hence `g|F_pq`.
* If `A_pq=0`, then `F_pq=0` identically.

**Proof.**  Only the irreducibility assertion needs comment.  A polynomial
of bidegree `(1,1)` can factor nontrivially only as a linear form in
`alpha` times a linear form in `beta`; its coefficient matrix then has rank
one.  Thus a bilinear form of matrix rank at least two is irreducible.  The
rank-one and rank-zero assertions follow directly from (10). `QED`

It is also possible to derive the first two bullets only from vanishing on
`g=0`: for rank at least two the hypersurface is irreducible, while in rank
one it is the union of the two displayed hyperplanes.  Identity (10) is
strictly stronger because it identifies the quotient as a pulled-back
hafnian.

## 4. Why the no-hole divisor is an anchor tautology

Recall the forced incident-edge theorem: for every vertex `p` and color
`r`, at least one active edge `pu` has

\[
 A_{pu}=x\,e_r^T\ne0.                                     \tag{11}
\]

Such an edge will be called a directed `r`-anchor from `p`.  If an
`r`-anchor `pu` lies in `R`, then

\[
 C_{u,r}=A_{pu}K_rA_{qu}^T=xe_r^TK_rA_{qu}^T=0,            \tag{12}
\]

so the `r`-summand of `F_pq` is already zero.  The same conclusion holds
when `qu` is a directed `r`-anchor from `q`, because `K_re_r=0`.

Suppose the `r`-summand of `F_pq` is not the zero polynomial.  Then no
directed `r`-anchor from either `p` or `q` can lie in `R`.  Existence of
anchors forces `pq` to be an `r`-anchor in both directions.  Consequently

\[
 A_{pq}=xe_r^T=e_ry^T\ne0,
 \qquad\text{hence}\qquad A_{pq}=\lambda e_re_r^T.         \tag{13}
\]

For a fixed nonzero edge (13) can hold for at most one color.  Every other
color summand is zero, while the possibly surviving summand contains
`alpha_r beta_r`; this is exactly `lambda^{-1}g`.  If `A_pq` is not a
coordinate projector, all three summands vanish.  If `A_pq=0`, all its
anchors lie outside and the same conclusion holds.

We have proved:

**Proposition 4.1 (anchor-tautology audit).**  Once the forced
incident-edge theorem is known, the bare assertion `g|F_pq` in Lemma 3.1
adds no information.  It follows term by term from forced anchors, without
using cancellation among the three colors.

This proposition is why one must not use (10), by itself, as a claimed new
uniform obstruction.

## 5. Leaving one site uncontracted

Fix `w in R`.  At every `u in R\{w}` use the cross-product covector
`gamma_u` from (8), but leave an arbitrary covector `delta` at `w`.
Every matching avoiding `pq` still vanishes.  Indeed, if `p` is matched to
`w`, then `q` is matched to some `v!=w` and the `qv` contraction vanishes;
if `q` is matched to `w`, the `p` edge vanishes; and if neither is matched
to `w`, at least the `p` edge vanishes.

Contracting (2) therefore gives

\[
 \sum_{r=0}^2\alpha_r\beta_r\delta_r
        \prod_{u\in R\setminus\{w\}}\gamma_{u,r}
 =g(\alpha,\beta)
   \left\langle H_R(A),
       \delta^{(w)}\otimes\!\bigotimes_{u\ne w}\gamma_u\right\rangle .
                                                                    \tag{14}
\]

Both sides are linear in the three independent coordinates of `delta`.
Comparison of the coefficient of `delta_r` proves the key identity

\[
 \boxed{
 \alpha_r\beta_r\prod_{u\in R\setminus\{w\}}
       \bigl(\alpha^TC_{u,r}\beta\bigr)
 =g(\alpha,\beta)\,T_{p q w r}(\alpha,\beta) }             \tag{15}
\]

for an explicitly defined contraction polynomial `T_pqwr`.  Unlike (10),
there is no sum over colors on the left of (15).

### 5.1 Rank at least two

**Theorem 5.1 (two witnesses per color).**  If `rank A_pq>=2`, then for
every color `r` the set

\[
 S_r(p,q)=\{u\in R:C_{u,r}\in\mathbb C A_{pq}\}            \tag{16}
\]

has at least two elements.

**Proof.**  The irreducible polynomial `g` is prime in
`C[alpha_0,alpha_1,alpha_2,beta_0,beta_1,beta_2]`.  It cannot divide the
factor `alpha_r` or `beta_r`.  By (15), for every omitted `w` it must
divide one of the bilinear factors with index `u!=w`.  Equal bidegree then
gives

\[
 \alpha^TC_{u,r}\beta=\lambda\alpha^TA_{pq}\beta,
 \quad\text{or equivalently}\quad C_{u,r}=\lambda A_{pq}.  \tag{17}
\]

If (16) had no element, (15) would fail for every `w`; if it had exactly
one element, omit that element.  Thus it has at least two. `QED`

**Corollary 5.2 (invertible-edge zero witnesses).**  If `A_pq` is
invertible, then for each `r` there are at least two different `u in R`
such that

\[
 A_{pu}K_rA_{qu}^T=0.                                     \tag{18}
\]

Indeed, the left side of (17) has rank at most two, whereas a nonzero
multiple of `A_pq` has rank three.

Write `I_r={0,1,2}\setminus{r}`, and let `P[:,I_r]` denote the two columns
of `P` outside color `r`.  Since the restriction of `K_r` to those two
coordinates is an invertible skew matrix `J_r`, (18) reads

\[
 A_{pu}[:,I_r]J_r A_{qu}[:,I_r]^T=0.                       \tag{19}
\]

Sylvester's rank inequality gives the useful concrete consequence

\[
 \operatorname{rank}A_{pu}[:,I_r]
 +\operatorname{rank}A_{qu}[:,I_r]\le2.                   \tag{20}
\]

In particular, if `A_pu` is invertible at such a witness, then all columns
of `A_qu` outside `r` vanish, so `A_qu=xe_r^T` has rank at most one; and
symmetrically with `p,q` interchanged.

### 5.2 Rank one and rank zero

The factor allocation in the remaining ranks is also exact.

**Theorem 5.3 (rank-one factor witnesses).**  Suppose
`A_pq=ab^T!=0`, and fix `r`.

* If `a` is not proportional to `e_r`, then at least two different
  `u in R` obey
  \[
       C_{u,r}=a d_u^T                                    \tag{21}
  \]
  for some `d_u`; equivalently `alpha^Ta` divides
  `alpha^TC_{u,r}beta`.
* If `b` is not proportional to `e_r`, then at least two different
  `u in R` obey
  \[
       C_{u,r}=c_u b^T.                                   \tag{22}
  \]
* If `a` (respectively `b`) is proportional to `e_r`, the corresponding
  factor of `g` is already supplied by `alpha_r` (respectively `beta_r`),
  and no witness of type (21) (respectively (22)) is forced.

**Proof.**  Put `L=alpha^Ta` and `M=b^Tbeta`.  They are relatively prime
linear polynomials.  In (15), `L` can divide `alpha_r` exactly when
`a` is proportional to `e_r`; otherwise it must divide some bilinear
factor.  A bilinear form `alpha^TCbeta` is divisible by `L` exactly when
`C=ad^T`.  The leave-one-out argument again forces at least two such
indices.  The proof for `M` is identical. `QED`

**Theorem 5.4 (zero edge).**  If `A_pq=0`, then for every `r` at least two
different outside vertices obey `C_{u,r}=0`.

**Proof.**  Equation (15) has zero right side.  Its left side is a product
in an integral domain, and `alpha_r,beta_r` are nonzero polynomials.  Thus,
for every omitted `w`, some remaining bilinear factor is zero.  The same
leave-one-out argument gives two indices. `QED`

Together, Theorems 5.1, 5.3, and 5.4 close every rank-degenerate case of
the one-hole identity.

## 6. Two holes and a rank-two correction

There is a second strengthening which detects when all one-hole witnesses
are concentrated at the same two vertices.  Fix distinct `w,z in R`, use
arbitrary covectors at those two sites, and use `gamma_u` at every
`u in S:=R\setminus{w,z}`.  After contracting at `p,q,S` but leaving the
two hole factors open, the target is the diagonal matrix

\[
 D_{wz}=\operatorname{diag}(t_0,t_1,t_2),\qquad
 t_r=\alpha_r\beta_r\prod_{u\in S}\gamma_{u,r}.            \tag{23}
\]

A matching avoiding `pq` can survive only by matching `p,q` to `w,z` in
one of the two orders.  Put

\[
 x_s=\alpha^TA_{ps},\qquad y_s=\beta^TA_{qs}\quad(s=w,z)   \tag{24}
\]

as row vectors at the indicated sites.  Both surviving assignments have
the same residual scalar

\[
 h_S=\left\langle H_S(A),\bigotimes_{u\in S}\gamma_u\right\rangle .
                                                                    \tag{25}
\]

Consequently the exact two-site tensor identity is

\[
 \boxed{
 D_{wz}=g\,Q_{wz}+h_S\bigl(x_w^Ty_z+y_w^Tx_z\bigr),}       \tag{26}
\]

where `Q_wz` is the contraction of `H_R(A)` at all sites except `w,z`.
The correction matrix in parentheses has rank at most two.

Assume `rank A_pq>=2`.  Reducing (26) modulo the prime `(g)` and taking
determinants gives

\[
 g\ \bigm|\ \prod_{r=0}^2t_r.                             \tag{27}
\]

As before, `g` cannot divide any coordinate linear factor, so it divides
some `gamma_{u,r}` with `u notin {w,z}`.  We obtain:

**Theorem 6.1 (three-vertex witness support).**  If `rank A_pq>=2`, then
for every two-element subset `{w,z}` of `R` there is a vertex
`u in R\setminus{w,z}` and a color `r` such that

\[
 C_{u,r}\in\mathbb C A_{pq}.                               \tag{28}
\]

In particular, the union `S_0(p,q) union S_1(p,q) union S_2(p,q)` contains
at least three different vertices.  If `A_pq` is invertible, every witness
in (28) is a zero matrix.

The last conclusion is slightly stronger than the three separate
two-witness statements: those six incidences could otherwise all have
been supported on the same two outside vertices.

The determinant argument also has exact singular-edge versions.

**Theorem 6.1a (two-hole singular-edge alternatives).**

* If `A_pq=ab^T!=0` and `a` is not proportional to any coordinate axis,
  then the union, over all colors, of the vertices satisfying
  \(C_{u,r}=a d^T\) has at least three elements.  If `b` is not
  proportional to any coordinate axis, the analogous union of vertices
  satisfying \(C_{u,r}=c b^T\) has at least three elements.
* If `A_pq=0`, the union, over all colors, of the zero-cross witnesses
  \(C_{u,r}=0\) has at least three elements.

**Proof.**  In the rank-one case reduce (26) first modulo
`L=alpha^T a` and then modulo `M=b^T beta`.  In either domain the diagonal
matrix has rank at most two, so the corresponding linear factor divides
`prod_r t_r`.  If `a` is noncoordinate, `L` divides none of
`alpha_0 alpha_1 alpha_2`, and therefore divides some cross factor outside
the two chosen holes.  Divisibility of that bilinear form is exactly
`C_u,r=a d^T`.  A set meeting the complement of every two holes has at
least three vertices.  The proof for `M` is symmetric.  When `A_pq=0`,
(26) itself has rank at most two, so `prod_r t_r=0`; the polynomial ring is
an integral domain, and some outside cross factor is zero. `QED`

### 6.1 The full two-hole matrix forces anchor rectangles

The determinant of (26) loses its most useful entrywise information.  The
following consequence retains the complete correction matrix.

Assume `rank A_pq>=2`, and for each color put

\[
 \mathcal S_c=\{t\in R:A_{pt}K_cA_{qt}^T\in\mathbb C A_{pq}\}. \tag{28d}
\]

Theorem 5.1 says `|S_c|>=2`.  Fix distinct holes `u,v` and define

\[
 J(u,v)=\{c:\mathcal S_c=\{u,v\}\}.                       \tag{28e}
\]

**Theorem 6.2 (two-hole anchor-rectangle alternative).**  Suppose `u` is
a directed `r`-anchor from `p`, `v` is a directed `r`-anchor from `q`, and

\[
 A_{pu}=ae_r^T\ne0,\qquad A_{qv}=be_r^T\ne0,
 \qquad \mathcal S_r=\{u,v\}.                             \tag{28f}
\]

Then exactly one of the following two structural conclusions holds.

1. `J(u,v)={r}`.  In this case either `A_qu=0`, or `A_pv=0`, or both
   opposite blocks are directed `r`-anchors:
   \[
       A_{qu}=a'e_r^T,\qquad A_{pv}=b'e_r^T.               \tag{28g}
   \]
2. `J(u,v)={r,s}` for one color `s!=r`.  Both opposite blocks are nonzero
   directed `s`-anchors:
   \[
       A_{qu}=a'e_s^T,\qquad A_{pv}=b'e_s^T.               \tag{28h}
   \]

In particular `J(u,v)` cannot contain all three colors.  For an invertible
`A_pq`, the sets `S_c` in (28d) are simply the zero-cross witness sets.

**Proof.**  Work in the integral domain

\[
 \mathcal R=\mathbb C[\alpha,\beta]/(g),
 \qquad g=\alpha^TA_{pq}\beta.                            \tag{28i}
\]

The diagonal entry

\[
 t_c=\alpha_c\beta_c\prod_{z\in R\setminus\{u,v\}}
       \alpha^T(A_{pz}K_cA_{qz}^T)\beta                   \tag{28j}
\]

is nonzero in `R` exactly when `S_c={u,v}`.  Indeed, `g` is prime, it
divides neither coordinate factor, and it divides a cross factor exactly
when that factor's matrix is proportional to `A_pq`.  The two-witness
theorem rules out a smaller witness set.

Write the four star vectors at the holes as

\[
 x_u=A_{pu}^T\alpha=(\alpha^Ta)e_r,\quad
 y_v=A_{qv}^T\beta=(\beta^Tb)e_r,
 \quad y_u=A_{qu}^T\beta,\quad x_v=A_{pv}^T\alpha.         \tag{28k}
\]

Modulo `g`, the full two-hole identity (26) is

\[
 \operatorname{diag}(t_0,t_1,t_2)
 =h\left((\alpha^Ta)(\beta^Tb)E_{rr}+y_ux_v^T\right).      \tag{28l}
\]

Here `h` is the residual contraction on `R\setminus{u,v}`.  Since
`r in J(u,v)`, the left side is nonzero, so `h` is nonzero in `R`.

Every off-diagonal entry of `y_u x_v^T` vanishes in `R`.  Such an entry is
a product of one beta-linear form and one alpha-linear form.  If its
polynomial were nonzero, primality of the rank-at-least-two bilinear `g`
would make `g` divide one of those linear factors, which is impossible.
Thus it vanishes as an ordinary polynomial.  The same argument applies to
every diagonal entry outside `J(u,v)` (the separate `E_rr` term affects
only the `r,r` cell).

A nonzero rank-one diagonal matrix has support at exactly one diagonal
cell.  The correction in (28l) is a sum of `E_rr` and that one rank-one
matrix, so it cannot have three nonzero diagonal cells.  If `J={r,s}`, the
outer product must be nonzero and supported at `s,s`; hence both of its
linear vector maps have image `C e_s`, which is exactly (28h).  If
`J={r}`, the outer product is either zero—meaning `A_qu=0` or `A_pv=0`—or
is supported at `r,r`, giving (28g). `QED`

Thus an invertible pair has the following sharp colorwise alternative:
there are at least three zero-cross witnesses, or its minimum two-witness
configuration closes to a same-color or color-swapped anchor rectangle
(unless an opposite block is zero).  The exact lifted web in
`notes/all-one-hole-system-countermodel.md` violates this completion and
is detected by the explicit two-hole residual there.

### 6.2 Three-hole rigidity at equality

The next hole number no longer gives a determinant obstruction, but the
equality case of the one-slice covering lemma classifies the smallest
possible witness support.

Let `W` be a three-element subset of `R`, put `S=R\setminus W`, contract
the sites in `S` by their cross products, and leave the three sites in `W`
open.  On the incidence hypersurface `g=0`, every surviving matching must
match `p` and `q` to two distinct vertices of `W`.  Grouping by the vertex
`w in W` matched to `p` gives an exact three-slice decomposition

\[
 \sum_{r=0}^2 t_r e_r^{\otimes W}
   =\sum_{w\in W}x_w^{(w)}\otimes P_w,
 \qquad
 t_r=\alpha_r\beta_r\prod_{u\in S}\gamma_{u,r},            \tag{28a}
\]

where `x_w=A_pw^T alpha` and `P_w` is a tensor on the other two hole
sites.  Grouping instead by the partner of `q` gives the analogous
decomposition with `y_w=A_qw^T beta`.

**Theorem 6.3 (minimal three-vertex witness pattern).**  Assume
`rank A_pq>=2`.  For every three-element `W subset R`, one of the following
holds.

1. Some `u in R\setminus W` and some color `r` obey
   \[
      C_{u,r}\in\mathbb C A_{pq}.
   \]
2. There are permutations `sigma,tau:W -> {0,1,2}` and nonzero vectors
   `a_w,b_w` such that
   \[
      A_{pw}=a_we_{\sigma(w)}^T,
      \qquad A_{qw}=b_we_{\tau(w)}^T                       \tag{28b}
   \]
   for every `w in W`; moreover, for each color `r`, the two vertices
   `sigma^{-1}(r)` and `tau^{-1}(r)` are distinct.

Consequently, if the full witness union in Theorem 6.1 has the minimum
possible size three, those three vertices are simultaneously the complete
three-color anchor targets displayed in (28b) for both endpoints.

**Proof.**  Suppose alternative 1 fails.  Then none of the nonzero
bilinear factors `gamma_u,r`, `u in S`, is divisible by the irreducible
polynomial `g`.  Hence every `t_r` in (28a) is a nonzero element of the
domain `C[alpha,beta]/(g)`.  There is a dense open subset of the irreducible
hypersurface `g=0` on which all three `t_r` are nonzero.

At every point of this open set, apply the one-slice covering lemma to the
right side of (28a).  Each of the three coordinate colors must occur as
the fixed vector of at least one of the three displayed slice terms.
There are exactly three terms, so all are nonzero and the three lines
`C x_w` are the three coordinate axes in some order.

Projection of `g=0` to the `alpha` projective plane is dominant.  Thus for
generic `alpha`, each linear vector-valued map
`alpha -> A_pw^T alpha` lands in the finite union of the three coordinate
lines.  Its irreducible image must lie in one fixed line.  Equivalently,
all but one column of `A_pw` vanish, giving the first formula (28b).  The
three selected coordinate lines are distinct, so `sigma` is a permutation.
The `q`-grouping proves the second formula and that `tau` is a permutation.

Fix a color `r`.  A constant-`r` matching term can use the `p` star only at
`sigma^{-1}(r)` and the `q` star only at `tau^{-1}(r)`.  These two partners
must be distinct in a perfect matching.  If they coincided, the constant
`r` coefficient of (28a) would be zero, contrary to `t_r!=0` on the chosen
open set.  This proves the last assertion. `QED`

For an invertible `A_pq`, every proportionality witness is a zero witness.
In the minimum-support branch of Theorem 6.3, `sigma(w)!=tau(w)` at every
`w`: two permutations of three objects with no color having the same
inverse image differ by a three-cycle.  Formula (9) then becomes

\[
 C_{w,r}=
 a_w\bigl(e_{\sigma(w)}^TK_re_{\tau(w)}\bigr)b_w^T.        \tag{28c}
\]

It vanishes exactly for the two colors `r=sigma(w),tau(w)` and is a
nonzero rank-one matrix for the third color.  Thus the three-vertex pattern
is completely explicit and realizes the two-zero-witness count for each
color with equality.

## 7. Coordinate-box specializations of the no-hole relation

For completeness, (10) also gives a useful hierarchy of restricted
factorizations.  Let `S,T` be nonempty subsets of the three colors with
`S intersect T={r}`.  Set all `alpha` coordinates outside `S` and all
`beta` coordinates outside `T` to zero.  Only target color `r` survives,
so

\[
 \alpha_r\beta_r\prod_{u\in R}
 \alpha_S^TC_{u,r}[S,T]\beta_T
 \quad\text{is divisible by}\quad
 \alpha_S^TA_{pq}[S,T]\beta_T.                            \tag{29}
\]

If the restricted matrix `A_pq[S,T]` has rank at least two, the divisor is
irreducible and must be proportional to one restricted cross matrix:

\[
 C_{u,r}[S,T]=\lambda A_{pq}[S,T]                          \tag{30}
\]

for some `u`.  The most informative proper boxes have
`S={0,1,2}\setminus{i}`, `T={0,1,2}\setminus{j}` with `i!=j`; then
`r` is the third color and (30) matches a full `2 by 2` block whenever the
corresponding off-diagonal cofactor of `A_pq` is nonzero.

If the restricted matrix has rank one, its two linear factors must be
allocated among `alpha_r,beta_r` and the restricted cross factors exactly
as in Theorem 5.3.  If it is zero, at least one restricted cross factor is
zero.  Thus (29) has no omitted singular case, although the global
one-hole identity (15) is usually stronger.

## 8. Interaction with forced anchors

An outside directed `r`-anchor from either `p` or `q` is automatically a
zero member of `S_r(p,q)` by (12).  Hence Theorem 5.1 is automatic when
`p` and `q` possess directed `r`-anchors at two distinct outside vertices.
The theorem adds information in precisely the collision branches:

1. If the only selected outside `r`-anchor of both `p` and `q` is the same
   vertex, that common anchor supplies only one zero witness; (15) forces a
   second proportionality witness.
2. If `pq=ab^T` is an `r`-anchor from `p` but not from `q`, then
   `b` is proportional to `e_r` while generically `a` is not.  Omitting
   the outside `r`-anchor from `q` in (15) forces an additional witness of
   type (21).  The transposed statement handles an anchor only from `q`.
3. If `pq` is an `r`-anchor in both directions, it is a coordinate
   projector and both rank-one factors are already present in
   `alpha_r beta_r`; this branch remains tautological.

Theorem 6.1 similarly adds information when all six directed anchor
incidences from `p,q` are concentrated on only two outside vertices: a
third vertex must carry a zero/proportional cross matrix.

These alternatives are exact, but they are not yet a global contradiction.
For example, if the directed anchor map for a fixed color is a permutation
of the vertices with no collisions, two different vertices usually have
distinct anchor targets and already supply the two zero witnesses.

There is a sharper exact warning against compressing the conclusions to
ranks and witness counts.  `notes/leave-one-out-rank-countermodel.md` gives
a zero-one array on `K_6` with three invertible blocks and twelve singleton
blocks.  It has forced active anchors, nonzero complementary cofactors, and
unimodular same-star contribution systems; nevertheless every outside
vertex is a zero witness for every color of each invertible edge, and every
rank-one factor-witness condition also holds.  The array is not a solution
of (2), but it proves that any continuation must retain the actual
contraction polynomials in (15), (26), or (28a), rather than only their
rank/activity shadows.

The uncompressed six-anchor analysis is continued in
`notes/one-hole-cofactor-kernel.md`.  In the transverse disjoint-anchor
branch at eight sites it classifies the quotient of the active cofactor as
a one-dimensional product of two cubic Koszul webs.  That quotient web is
itself exactly realizable by an eight-edge six-site matching tensor, so the
anchor-line lift and overlapping pair systems are essential.

## 9. Why one common hole is the maximal termwise construction

The one-hole argument is not an arbitrary choice.  Suppose at each
`u in R` a contraction is declared to kill the `pu` factor (`u in X`),
the `qu` factor (`u in Y`), both, or neither.  Killing every matching which
avoids `pq` term by term requires

\[
 u\in X\quad\text{or}\quad v\in Y
 \qquad\text{for every }u!=v.                              \tag{31}
\]

There can be no distinct `u in R\setminus X` and
`v in R\setminus Y`.  Therefore either `X=R`, or `Y=R`, or both complements
are contained in the same singleton.  In other words, at most one common
site can be left unannihilated.  Avoiding two distinct anchor sites requires
using cancellation between the two surviving assignments, whose exact
rank-two correction is (26); it cannot be achieved by a further pointwise
choice of covectors.

## 10. Exact local sharpness examples

The incidence divisor alone has abundant exact local models.  For example,
take `n=8`, `A_pq=I`, and at the six outside sites take

\[
 A_{pu}=A_{qu}=I,I,R,R,R^2,R^2,                            \tag{32}
\]

where `R` is the cyclic `3 by 3` permutation matrix.  If
`z=alpha cross beta`, then the six cross products are two copies of each
cyclic permutation of `z`; consequently

\[
 F_{pq}=(z_0z_1z_2)^2(\alpha^T\beta).                      \tag{33}
\]

Thus even an invertible `A_pq` and six invertible neighboring matrices can
satisfy the bare divisor identity.  This is not a candidate solution of
(2)—it violates the forced-anchor theorem—but it confirms that one must use
the full family of identities, not incidence-quadric factorization in
isolation.

At the opposite, anchor-rich extreme, give `p` and `q` distinct outside
`r`-anchors for every `r`.  Those six rank-one matrices make the two zero
witnesses in Corollary 5.2 termwise and show that its numerical lower bound
of two witnesses per color is sharp at the local-star level.

## 11. Machine audit

`computations/verify_two_vertex_annihilation_identities.py` performs exact
integer/rational checks of:

1. the orientation formula (9);
2. the no-hole identity (10) by enumerating all perfect matchings;
3. the one-hole identity (14), including coefficient comparison (15);
4. the two-hole tensor identity (26);
5. the cyclic-permutation factorization (33); and
6. the rank-one factor allocation and projected-rank implications used in
   Theorems 5.3 and Corollary 5.2; and
7. the exact zero/nonzero cross pattern (28c) in the minimal three-vertex
   branch.

The script is an audit of the formulas, not a substitute for the proofs
above.
