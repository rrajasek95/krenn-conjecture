# Local algebra of a star: degree four and the two-extra Koszul dichotomy

This note continues `notes/slice-cover.md`.  All edge tensors are arbitrary
matrices over `C`; endpoint order is retained.  The conclusions therefore do
not use symmetry, positivity, or a rank-one assumption.

## 1. The one-slice lemma is sharp

The one-slice covering lemma says that a decomposition

\[
 \Delta_{m,3}=\sum_{j=1}^m x_j^{(j)}\otimes P_j
\]

must contain a center proportional to each of the three coordinate vectors.
It cannot by itself say that all other slices vanish.  For example, on four
sites start with the three coordinate summands and choose arbitrary nonzero
`x in V_4` and `Q in V_2 tensor V_3`.  Then

\[
\begin{aligned}
 \Delta_{4,3}
 ={}&e_0^{(1)}\otimes(e_0^{\otimes3}-Q\otimes x)
   +e_1^{\otimes4}+e_2^{\otimes4}\\
  &+x^{(4)}\otimes(e_0^{(1)}\otimes Q).
\end{aligned}                                                   \tag{1}
\]

The last part is the elementary Koszul zero syzygy
`-e_0 tensor Q tensor x+x tensor e_0 tensor Q=0`, after reordering
the factors.  Thus a dense-support argument has to use the special fact that
the complementary tensors `P_j` are hafnian cofactors.

## 2. Classification of four pointwise covering maps

Let `T=(C^*)^3`, and suppose four linear maps
`L_0,L_1,L_2,L_*: C^3 -> C^3` have the following covering property:
for every `lambda in T` and every coordinate axis `C e_r`, at least one
nonzero `L_j(lambda)` lies on that axis.  Suppose the three maps supplied by
the generic irreducibility argument have been labeled

\[
 L_r(\lambda)=a_r(\lambda)e_r\quad(r=0,1,2),\qquad
 L_*(\lambda)=(b_0(\lambda),b_1(\lambda),b_2(\lambda)).       \tag{2}
\]

Here all `a_r` are nonzero linear forms.

**Lemma 2.1 (degree-four covering classification).**

1. At most two of the forms `a_r` have a zero on `T`.  Equivalently, at
   least one `a_r` is a scalar multiple of a coordinate functional.
2. If exactly two, say `a_0,a_1`, have torus zeros, then they are linearly
   independent and, for nonzero constants `c,d`,

   \[
       L_*(\lambda)=d a_1(\lambda)e_0+c a_0(\lambda)e_1,
       \qquad a_2\text{ is a coordinate functional}.         \tag{3}
   \]

**Proof.**  A nonzero linear form `a` has no zero on `T` exactly when it is
a scalar multiple of one coordinate functional.  If `a_r` has torus zeros,
its zero hyperplane meets `T` densely.  On that hyperplane the map `L_r`
vanishes, while none of the other two axis maps can cover the `r`-axis.
Consequently `L_*` is a nonzero `r`-axis there.  Polynomial continuation
gives

\[
 b_s\in\mathbb C a_r\qquad(s\ne r).                           \tag{4}
\]

If `a_r,a_t` both have torus zeros, they cannot be proportional: a common
torus zero would require the same nonzero vector `L_*(lambda)` to lie on two
different axes.  For the remaining index `s`, (4) says that `b_s` is
proportional to both independent forms, hence `b_s=0`.  The other two
coordinates in (3) are nonzero multiples, because they must do the covering
on the respective hyperplanes.  A third form `a_s` cannot then have a torus
zero, since `L_*` has identically zero `s`-coordinate.  This proves both
claims. \(\square\)

Applied to a star of active degree four in an exact matching-tensor
realization, (2) comes from the one-slice covering lemma.  Hence every such
vertex has an incident matrix which is a single decorated basis entry
`c e_i tensor e_r` (the two endpoint colors need not yet agree).

There is more rigidity in the exceptional case (3).  The four incident
matrices then have the form, after relabeling their opposite endpoints,

\[
 a_0\otimes e_0,quad a_1\otimes e_1,quad e_k\otimes e_2,quad
 d a_1\otimes e_0+c a_0\otimes e_1.                          \tag{5}
\]

Mode rank three of the target forces `a_0,a_1,e_k` to be a basis.  Contract
the center vertex by the dual covector which kills `a_0,a_1` and takes value
one on `e_k`.  Exactly the third star summand survives.  Its opposite-site
factor is `e_2`, whereas the contracted target is a linear combination of
the three constant tensors.  Comparing that opposite site forces the
coefficients of colors zero and one to vanish.  Thus the dual covector is a
multiple of `e_2^*`, whence `k=2`, and the surviving cofactor is a nonzero
multiple of `e_2^{tensor(n-2)}`.  After rescaling:

**Corollary 2.2.**  In the two-noncoordinate case, the coordinate anchor in
(5) is a same-color tensor `e_2 tensor e_2`, and its hafnian cofactor is the
pure constant tensor `e_2^{tensor(n-2)}`.

This is stronger than the bare existence of a decorated rank-one edge.  It
also explains the remaining danger: the other three star terms could in
principle form an exact two-color cancellation gadget.

## 3. Five active neighbors at six vertices

Fix a vertex `p` of a putative six-vertex realization and suppose all five
underlying pairs at `p` are active.  Choose three distinct anchor neighbors
`1,2,3` supplied by the slice-cover theorem, with opposite-end factors
`e_0,e_1,e_2`, and call the other neighbors `4,5`.  Put

\[
 C_j=H_{B\setminus\{p,j\}},\qquad
 x_j(\lambda)=(\lambda\otimes\mathrm{id})A_{pj}.             \tag{6}
\]

Let `pi_1,pi_2,pi_3` be the quotients by `C e_0,C e_1,C e_2`, respectively,
and put bars over tensors after applying these three quotients.  Contracting
the star at `p` by a torus covector `lambda`, and then quotienting, kills the
target and all three anchor terms.  Therefore

\[
 x_4(\lambda)^{(4)}\otimes\bar C_4+
 x_5(\lambda)^{(5)}\otimes\bar C_5=0                         \tag{7}
\]

for every `lambda`.

**Lemma 3.1 (two-extra Koszul dichotomy).**  Either

\[
 \bar C_4=\bar C_5=0,                                       \tag{8}
\]

or both extra incident matrices `A_p4,A_p5` have matrix rank one.

**Proof.**  If one barred cofactor vanishes, (7), evaluated at a generic
`lambda` for which both active edge maps are nonzero, forces the other to
vanish as well.  Otherwise a nonzero equality of a slice centered at site
four with a slice centered at site five lies in the intersection

\[
 (\mathbb Cx_4\otimes V_5\otimes R)
 \cap(V_4\otimes\mathbb Cx_5\otimes R)
 =\mathbb Cx_4\otimes\mathbb Cx_5\otimes R,
\]

where `R` is the tensor product of the three quotient spaces.  Hence, for a
nonzero tensor `T(lambda) in R`,

\[
 \bar C_4=T(\lambda)\otimes x_5(\lambda),\qquad
 \bar C_5=-T(\lambda)\otimes x_4(\lambda).                   \tag{9}
\]

The left sides are independent of `lambda`.  Their nonzero one-site factor
lines are therefore fixed on a dense open set, so each linear map
`lambda -> x_j(lambda)` has one-dimensional image.  This is exactly
`rank(A_pj)=1`. \(\square\)

The unresolved branch (8) is now very explicit.  For example

\[
\begin{aligned}
 \bar C_4={}&\bar A_{12}\otimes\bar A_{35}
 +\bar A_{13}\otimes\bar A_{25}
 +\bar A_{15}\otimes\bar A_{23}=0,\\
 \bar C_5={}&\bar A_{12}\otimes\bar A_{34}
 +\bar A_{13}\otimes\bar A_{24}
 +\bar A_{14}\otimes\bar A_{23}=0.                          \tag{10}
\end{aligned}
\]

Each is a four-party zero-hafnian identity on quotient dimensions
`2,2,2,3`.  These identities genuinely have a non-rank-one Pluecker branch:
on two-dimensional spaces the alternating brackets satisfy

\[
 [12][34]-[13][24]+[14][23]=0.                               \tag{11}
\]

Thus (8) cannot be disposed of by claiming that the three matching products
vanish termwise.  A completion of this route must exploit the two *shared*
identities in (10), or show that their Pluecker branches are incompatible
with the unquotiented target equations.

## 4. Exact classification of the nondegenerate shared branch

The word "Pluecker" in the preceding paragraph can be made precise.  This
both narrows the exceptional case and prevents a false termwise argument.

**Lemma 4.1 (triangle syzygy).**  Let `U_1,U_2,U_3` be two-dimensional and
let `B_12,B_13,B_23` be nondegenerate bilinear forms on the indicated pairs.
If nonzero linear forms `l_i in U_i^*`, not all zero, satisfy

\[
 B_{12}(u_1,u_2)l_3(u_3)+B_{13}(u_1,u_3)l_2(u_2)
 +l_1(u_1)B_{23}(u_2,u_3)=0,                                \tag{12}
\]

then, after isomorphisms of the three spaces with one two-dimensional space
`W` and harmless nonzero rescalings/sign changes, all three `B_ij` are the
same alternating bracket

\[
 B_{ij}(u_i,u_j)=[\phi_i(u_i),\phi_j(u_j)].                  \tag{13}
\]

The solution space of (12) is two-dimensional and consists of brackets with
one common vector of `W`.

**Proof.**  Use independent bases of `U_2,U_3` to normalize
`B_12=B_13=[\ ,\ ]`, keeping a fixed basis of `U_1`.  Write

\[
 B_{23}=m_{00}x_0y_0+m_{01}x_0y_1+m_{10}x_1y_0+m_{11}x_1y_1
\]

and `l_1=(a,b), l_2=(c,d), l_3=(e,f)`.  Equating the eight squarefree
cubic coefficients in (12) gives

\[
\begin{array}{c}
 am_{00}=0,\quad am_{01}+c=0,\quad am_{10}+e=0,\\
 am_{11}+d+f=0,\quad bm_{00}-c-e=0,\\
 bm_{01}-f=0,\quad bm_{10}-d=0,\quad bm_{11}=0.
\end{array}                                                   \tag{14}
\]

The middle equations give
`c=-am_01,e=-am_10,f=bm_01,d=bm_10`.  Since a nonzero solution has
`(a,b) != (0,0)` and `B_23` is nondegenerate, the remaining equations force

\[
 m_{00}=m_{11}=0,\qquad m_{10}=-m_{01}\ne0.                 \tag{15}
\]

Thus `B_23` is alternating in the normalized bases.  Conversely (14) then
has the two free parameters `a,b`, and its displayed formulas identify the
three forms with brackets against one common vector. \(\square\)

**Corollary 4.2 (shared Pluecker extension).**  In (10), suppose the three
shared projected matrices `bar A_12,bar A_13,bar A_23` all have rank two.
Then their three quotient spaces identify with a common two-space `W`, the
shared matrices are alternating brackets, and for each `x=4,5` there is a
linear map `phi_x:V_x -> W` such that all three matrices joining `x` to
`1,2,3` are pullbacks of the same bracket.  In particular the two equations
in (10) are ordinary Grassmann--Pluecker identities, not accidental
coefficient cancellations.

**Proof.**  Fixing the argument at site `x` in the corresponding equation
of (10) gives (12).  Lemma 4.1 first identifies the shared triangle.
Its two-dimensional solution space then says that the three linear forms
obtained from any vector at site `x` arise from a single vector of `W`.
Linearity in that vector gives `phi_x`. \(\square\)

Thus the genuinely dense exceptional branch of Lemma 3.1 is a coherent
two-dimensional matchgate layer living in the three quotient color spaces.
Any proposed completion must use the unquotiented equations to rule out (or
control) this layer; rank counting inside (10) alone is sharp and cannot do
so.

## 5. A finite obstruction in the prism-plus-skew-cycle chart

Here is an exact global obstruction to the most natural saturated `C_6`
Pluecker chart.  It is purely coefficientwise and therefore does not use
positivity or symmetry of the original aggregate matrices.

Put the following nonzero same-color basis matrices on the nine edges of a
triangular prism:

\[
 \begin{aligned}
 M_0&=\{04,12,35\},\\
 M_1&=\{05,14,23\},\\
 M_2&=\{03,15,24\}.
 \end{aligned}                                             \tag{16}
\]

Thus an edge in `M_r` is a nonzero scalar multiple of
`e_r tensor e_r`.  The complementary six-cycle is

\[
 C=\{01,02,13,25,34,45\}.                                  \tag{17}
\]

Suppose each matrix on `C` is skew-symmetric in the coordinate basis.  It
may have arbitrary complex entries and arbitrary support among the three
unordered pair-types `01,02,12`.

**Lemma 5.1 (alternating-matching singleton).**  Let

\[
 T_0=\{01,25,34\},\qquad T_1=\{02,13,45\}.                 \tag{18}
\]

For either `T_i`, choose one unordered pair-type in `01,02,12` on each of
its three edges.  The three pairs can be oriented at their endpoints so
that the resulting six-coloring is supported by `T_i` and by no other
perfect matching in the full chart (16)--(17).

**Proof.**  It is enough to check `T_0`, since the vertex permutation
`012345 -> 021543`, together with the color permutation `012 -> 021`,
preserves (16) and interchanges `T_0,T_1`.

For `T_0`, encode its three pair-types in edge order `01,25,34`, and encode
an orientation by three bits: bit zero puts the smaller color at the first
displayed endpoint and bit one reverses it.  The colored automorphisms of
(16) which preserve `T_0` have the following vertex and color permutations:

```
vertices   colors
012345     012
103254     210
250431     102
341520     120
435102     021
524013     201
```

Their seven orbits on the `3^3` triples have the representatives in the
first column below.  The second column gives a singleton orientation, and
the last column gives the resulting colors at vertices `0,...,5`.

\[
\begin{array}{c|c|c}
\text{pair-types}&\text{orientation}&\text{vertex colors}\\ \hline
01,01,02&000&010021\\
01,02,01&000&010012\\
01,12,01&010&012011\\
01,01,01&000&010011\\
02,12,01&010&022011\\
01,12,02&000&011022\\
01,02,12&000&010122
\end{array}                                                \tag{19}
\]

Direct inspection of the fifteen perfect matchings verifies the last
claim in each row.  For completeness, here is a short way to make that
inspection: a prism edge can occur only when both endpoint colors equal its
label in (16), while a cycle edge can occur only when its endpoint colors
are unequal.  Testing these conditions on the fifteen matchings leaves
only `01,25,34` in every row.  Applying the six displayed automorphisms
covers all twenty-seven triples.  This proves the lemma. \(\square\)

The finite inspection, including the second alternating matching, is also
implemented independently in
`computations/verify_skew_cycle_singletons.py`.

**Corollary 5.2 (no finite all-nonzero skew cycle).**  The chart
(16)--(17) cannot realize `Delta_(6,3)` if all six skew cycle matrices are
nonzero.  More precisely, any exact realization in this chart has a zero
matrix in each of `T_0` and `T_1`.

**Proof.**  If all three matrices on `T_i` are nonzero, choose a nonzero
unordered-pair entry from each.  Lemma 5.1 supplies an orientation whose
coloring has exactly one supported matching.  Its coefficient is the
product of three nonzero entries (with harmless skew signs), hence is
nonzero.  The coloring is nonconstant because the endpoints of every edge
of `T_i` have different colors, whereas its target coefficient is zero.
This is a contradiction.  Therefore at least one whole matrix on each
`T_i` is zero. \(\square\)

This corollary is a finite-versus-border statement: it rules out every
finite point with all six skew matrices nonzero, regardless of how small or
large their entries are.  It also explains why a numerical sequence can
approach the target while individual cycle entries tend to zero and other
parameters diverge.

## 6. Rank loss forced by every local `C_6` Pluecker equation

The degenerate local identities in the saturated six-cycle still have a
useful invariant which does not require their full classification.

**Lemma 6.1 (opposite-pair rank bound).**  Let `F_ij` be arbitrary
two-party tensors and suppose

\[
 F_{12}F_{34}+F_{13}F_{24}+F_{14}F_{23}=0.                 \tag{20}
\]

If `rank(F_13),rank(F_24)<=1`, where rank means matrix rank across the two
indicated sites, then

\[
       rank(F_{12})rank(F_{34})\le2.                        \tag{21}
\]

**Proof.**  Flatten (20) across the cut `14|23`.  The first summand has
matrix rank `rank(F_12)rank(F_34)`.  The second has rank
`rank(F_13)rank(F_24)<=1`.  The third is the simple tensor
`F_14 tensor F_23` across this cut and hence has rank at most one.  Matrix
rank subadditivity gives (21). \(\square\)

Apply this at a saturated `F=C_6` vertex.  Number vertices modulo six, put
`E_i={i,i+1}`, and fix a center `p`.  Its three basis anchors are the
chords from `p` to `p+2,p+3,p+4`.  Write `pi_j^p` for quotienting site `j`
by the coordinate factor at `j` of the chord `pj`.  The two barred-cofactor
identities of Lemma 3.1 and Lemma 6.1 give

\[
\begin{aligned}
 &rank((I\otimes\pi_{p+2}^p)A_{E_{p+1}})\,
  rank((\pi_{p+3}^p\otimes\pi_{p+4}^p)A_{E_{p+3}})\le2,\\
 &rank((\pi_{p+2}^p\otimes\pi_{p+3}^p)A_{E_{p+2}})\,
  rank((\pi_{p+4}^p\otimes I)A_{E_{p+4}})\le2.             \tag{22}
\end{aligned}
\]

Thus every one of the twelve local equations forces rank loss in one of a
specified pair of projected cycle matrices.  This can be translated into
kernel coordinates without any genericity.  If a `3 by 3` cycle matrix
`A` has rank two, write

\[
        \operatorname{adj}(A)=r l^T,
        \qquad Ar=0,\quad l^TA=0.                           \tag{23}
\]

Quotienting the first endpoint by `e_a` has rank at most one exactly when
`l_a=0`; quotienting the second endpoint by `e_b` has rank at most one
exactly when `r_b=0`; and quotienting both endpoints has rank at most one
exactly when

\[
                  l_a r_b=0.                               \tag{24}
\]

Indeed, the relevant `2 by 2` minors are respectively a column, a row, or
one entry of the adjugate (23).  For an invertible matrix, a one-end
quotient always has rank two, while the two-end condition is precisely the
vanishing of the corresponding cofactor.  Equations (22)--(24) reduce the
remaining globalization problem to a finite zero-pattern compatibility
problem for the six left and right kernel lines.

## 7. Overlapping Pluecker charts on `C_3 union C_3`

The fully nondegenerate Pluecker branch on the other saturated graph is
globally impossible.  This section gives an exact statement and proof.

Split the vertices as `L={0,1,2}` and `R={3,4,5}`.  The six internal edges
form the two higher-rank triangles, while every cross edge is a nonzero
basis matrix.  Write

\[
 A_{lr}=g_{lr}e_{\alpha_{lr}}\otimes e_{\beta_{lr}},
 \qquad g_{lr}\ne0.                                       \tag{25}
\]

The directed anchor condition says that every row
`(beta_(l,r):r in R)` is a permutation of the colors, and every column
`(alpha_(l,r):l in L)` is a permutation.

For `p in L`, quotient each `V_r`, `r in R`, by
`C e_(beta_(p,r))`.  Call `p` *R-regular* if all three internal `R`-edge
matrices still have rank two after the corresponding two endpoint
quotients.  Define *L-regular* vertices of `R` symmetrically, using the
`alpha` columns.

**Proposition 7.1 (no fully regular double triangle).**  It is impossible
that all three vertices of `L` are R-regular and all three vertices of `R`
are L-regular.

**Proof.**  First suppose all vertices of `L` are R-regular.  Take distinct
`p,y in L`.  One of the two barred cofactor equations at `p` is

\[
 \sum_{r\in R}\bar A_{yr}\,\bar B_{R\setminus\{r\}}=0,     \tag{26}
\]

where the bars use the quotients belonging to `p`, and the three `B`'s are
the internal edges of `R`.  The two permutation rows `beta_p,beta_y` agree
in zero, one, or three positions.  In the one-position case exactly two
cross forms in (26) survive.  Lemma 4.1 says that a nonzero syzygy among
three nondegenerate triangle forms is a common-bracket syzygy and has all
three one-site forms nonzero, so this case is impossible.  If the rows are
different they therefore agree nowhere.  All three cross forms survive,
and the same lemma says that their factors at `y` are proportional.  Since
they are coordinate factors, there is a color `c` such that

\[
                  \alpha_{yr}=c\quad(r\in R).              \tag{27}
\]

We claim that (27) contradicts R-regularity of `y`.  Because every `alpha`
column is a permutation, no cross edge at either other vertex of `L` has
color `c` at its `L` endpoint.  Fixing all three `L` colors to `c` in the
full six-party identity therefore leaves exactly the one-cross-edge
matchings whose cross edge starts at `y`.  Hence, for nonzero scalars
`s_r`, the internal triangle on `R` obeys

\[
 \sum_{r\in R}s_r e_{\beta_{yr}}^{(r)}
       \otimes B_{R\setminus\{r\}}=e_c^{\otimes R}.         \tag{28}
\]

(The common internal `L`-edge coefficient in (28) is nonzero, since the
constant-`c` coefficient on both sides is one.)

Fix `r`, and choose colors `a,b` at the other two sites which differ from
their respective `beta_y` entries.  In (28), at the `R`-coloring having
color `beta_(y,r)` at `r` and colors `a,b` elsewhere, only the summand
centered at `r` survives.  Its coefficient must vanish unless this is the
constant-`c` coloring.  It follows that, after quotienting the two endpoints
of `B_(R\setminus\{r\})` by their `beta_y` axes, its matrix has support on
at most the single entry `(c,c)`, and therefore rank at most one.  This
contradicts R-regularity of `y`.

Consequently all three `beta` rows must be equal.  The symmetric argument,
using L-regularity of every vertex in `R`, says that all three `alpha`
columns must be equal.  Thus there are permutations `(a_l)` and `(b_r)`
such that every cross edge has the endpoint-separable form

\[
             A_{lr}=g_{lr}e_{a_l}\otimes e_{b_r}.           \tag{29}
\]

It remains to rule out (29) under full regularity.  For every color `c`,
the constant global coloring has exactly one compatible underlying perfect
matching: its cross edge is `l_c r_c`, where `a_(l_c)=b_(r_c)=c`, and the
other two edges are internal to the two triangles.  Therefore

\[
 B_{R\setminus\{r_c\}}(c,c)\ne0.                           \tag{30}
\]

Fix `l in L` and colors at the other two `L` sites which avoid their axes
`a`.  Then `l` is the unique cross-eligible `L` vertex in the coloring
whose color at `l` is `a_l`.  Choose a color `c\ne a_l`, put color `c` on
all of `R`, and let `r_c` be as above.  There is now exactly one compatible
underlying matching.  Its coefficient is

\[
 g_{l r_c}\,
 A_{L\setminus\{l\}}(\text{the two chosen colors})\,
 B_{R\setminus\{r_c\}}(c,c).                              \tag{31}
\]

The first and third factors are nonzero, while the coloring is mixed, so
the middle factor must vanish.  This holds for all entries remaining after
quotienting by the two `a` axes.  The projected internal `L` edge is thus
zero, contradicting L-regularity. \(\square\)

Proposition 7.1 is the desired overlap obstruction for the genuinely dense
matchgate layer.  Any surviving `C_3 union C_3` realization must lie on a
coordinate-degenerate boundary: for at least one center, one internal edge
of the opposite triangle loses rank after the two prescribed coordinate
quotients.  For a rank-two edge this boundary is exactly one of the kernel
coordinate vanishings in (24).
