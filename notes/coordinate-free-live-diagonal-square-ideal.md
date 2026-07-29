# The live diagonal obstruction is coordinate-free

## 1. Statement

Let `U` be a set of `m>=2` sites, identify a three-dimensional vector
space `V` with every local space, and work in the site-square-zero algebra
on `U`.  Put

\[
                    p_c=\sum_{i\in U}e_c^{(i)},
        \qquad p(v)=\sum_{c=0}^2v_cp_c.                 \tag{1}
\]

At site `i`, let

\[
                   f_{i,0},f_{i,1},f_{i,2}              \tag{2}
\]

be an arbitrary basis of `V`, with no compatibility assumed between
different sites, and set

\[
                         X_c=\bigotimes_{i\in U}f_{i,c}. \tag{3}
\]

Let `R` have site degree `m-2`, let `T` be an arbitrary top-support
tensor, and let `B=(b_cd)` be symmetric.  Suppose

\[
 p_cp_dR+b_{cd}T=0\quad(c\ne d),                       \tag{4}
\]

and

\[
 p_c^2R+b_{cc}T=t_cX_c\quad(c=0,1,2).                 \tag{5}
\]

Then at most one of `t_0,t_1,t_2` is nonzero.  In fact, the following
sharper conclusions hold.

* If `T=0`, all three `t_c` vanish.
* If `t_c!=0`, then `T!=0` and the quadratic form represented by `B`
  is a nonzero scalar multiple of `v_c^2`.  Consequently every
  off-diagonal entry of `B` is zero and `t_d=0` for `d!=c`.
* In particular, if some off-diagonal entry of `B` is nonzero, all three
  `t_c` vanish.

This removes the alignment caveat in
[`aligned-live-diagonal-sector-lemma.md`](aligned-live-diagonal-sector-lemma.md).
After normalizing arbitrary invertible live matrices `P_i`, the marked
vectors become the common `e_c`, while the target factors become
`f_(i,c)=P_i^{-1}e_c`; (2) is exactly the general situation.

## 2. The second-order site subspace

For `0!=v in V`, define

\[
 J_v^{[2]}=
 \sum_{\{i,j\}\subset U}
   \mathbb Cv^{(i)}\otimes\mathbb Cv^{(j)}\otimes
   \bigotimes_{k\notin\{i,j\}}V_k
 \ \subseteq\ \bigotimes_{i\in U}V_i.                \tag{6}
\]

Thus `J_v^[2]` is the subspace spanned by tensors having a factor `v` at
at least two specified sites.  The defining feature of the common marked
linear form is

\[
                              p(v)^2R\in J_v^{[2]}.      \tag{7}
\]

We need three elementary facts about (6).

**Lemma 2.1 (one pure tensor).**  For a nonzero decomposable tensor
`X=\bigotimes_i x_i`,

\[
 X\in J_v^{[2]}
 \quad\Longleftrightarrow\quad
 \#\{i:x_i\in\mathbb Cv\}\ge2.                        \tag{8}
\]

**Proof.**  Choose a complement `V=Cv direct-sum W`.  The tensor product
has a direct grading by the number of factors in `Cv`, and `J_v^[2]` is
the sum of the pieces of degree at least two.  In the expansion of `X`,
the least possible degree is precisely the number of factors whose
projection to `W` is zero.  Its least-degree component is a nonzero pure
tensor, so it cannot cancel.  This proves (8). `QED`

**Lemma 2.2 (two pure tensors).**  Let
`X=\bigotimes_i x_i` and `Y=\bigotimes_i y_i` be nonzero and
nonproportional.  Suppose no `x_i` or `y_i` lies in `Cv`.  If
`alpha,beta` are nonzero, then

\[
                            \alpha X+\beta Y\notin J_v^{[2]}.       \tag{9}
\]

**Proof.**  Again choose `V=Cv direct-sum W`, and write

\[
                   x_i=a_iv+\bar x_i,
       \qquad      y_i=b_iv+\bar y_i,                  \tag{10}
\]

where every barred vector is nonzero.  If the tensor in (9) belonged to
`J_v^[2]`, its degree-zero component would vanish:

\[
        \alpha\bigotimes_i\bar x_i+
        \beta \bigotimes_i\bar y_i=0.                 \tag{11}
\]

Equality of two nonzero pure tensors gives nonzero scalars `r_i` with

\[
              \bar y_i=r_i\bar x_i,
       \qquad \beta\prod_i r_i=-\alpha.                \tag{12}
\]

The degree-one summands live in the direct sum indexed by the unique site
carrying `v`.  At site `i`, their vanishing and (12) give

\[
 0=\alpha a_i+
       \beta b_i\prod_{j\ne i}r_j
   =\alpha\left(a_i-{b_i\over r_i}\right).             \tag{13}
\]

Hence `b_i=r_i a_i` and therefore `y_i=r_ix_i` at every site.  This makes
`Y` proportional to `X`, a contradiction. `QED`

**Lemma 2.3 (three basis-labelled tensors).**  Assume `m>=2`, let the
three local factors in (2) be bases, and choose `v` not proportional to
any of them.  If all three scalars `alpha_c` are nonzero, then

\[
                         \sum_{c=0}^2\alpha_cX_c\notin J_v^{[2]}.
                                                                    \tag{14}
\]

**Proof.**  It is enough to show that the degree-zero projection of (14)
to `\bigotimes_i(V/Cv)` is nonzero.  At every site the three nonzero
images `\bar f_(i,c)` span the two-dimensional quotient.  Group the first
site against the remaining sites.  If the displayed degree-zero sum
vanished, it would be a matrix factorization

\[
 [\bar f_{1,0}\ \bar f_{1,1}\ \bar f_{1,2}]
       \operatorname {diag}(\alpha_0,\alpha_1,\alpha_2)
 [\bar X_{0,-1}\ \bar X_{1,-1}\ \bar X_{2,-1}]^{\mathsf T}=0.
                                                                    \tag{15}
\]

The first matrix has rank two.  The last matrix also has rank at least
two: rank one would make its three nonzero pure columns proportional,
and hence make the three local quotient vectors proportional at every
remaining site, contrary to their spanning a two-space.  Since the
middle diagonal matrix is invertible, the image of the right factor in
(15) has dimension at least two but would have to lie in the
one-dimensional kernel of the left factor.  This is impossible. `QED`

## 3. Isotropic directions remove the common tensor

Expand (4)--(5) at an arbitrary `v=(v_0,v_1,v_2)`.  Symmetry of `B`
gives

\[
 p(v)^2R+b(v)T=\sum_{c=0}^2t_cv_c^2X_c,
 \qquad
 b(v)=v^{\mathsf T}Bv.                                 \tag{16}
\]

On the projective conic

\[
                              C_B=\{[v]\in\mathbb P^2:b(v)=0\},   \tag{17}
\]

equations (7) and (16) imply

\[
                    \sum_{c=0}^2t_cv_c^2X_c\in J_v^{[2]}.         \tag{18}
\]

The same argument applies when `B=0`, interpreting `C_B` as all of
`P^2`.  Over `C`, a nonzero homogeneous quadratic has an infinite
projective zero locus.  We may therefore avoid the finite set of points

\[
                            \{[f_{i,c}]:i\in U,\ 0\le c\le2\}.     \tag{19}
\]

Let `A={c:t_c!=0}`.  Suppose first that `|A|=3`.  The locus in `P^2`
where at most one coordinate is nonzero consists of just the three
coordinate points.  Choose an isotropic `[v]` outside that finite locus
and (19).  If exactly two coordinates are nonzero, Lemma 2.2 contradicts
(18); if all three are nonzero, Lemma 2.3 does.  Thus three target values
cannot survive.

Suppose next that `A={c,d}` has size two.  If `C_B` has a point outside
(19) with `v_cv_d!=0`, Lemma 2.2 again contradicts (18).  Otherwise the
infinite conic is contained in the union of the two coordinate lines
`v_c=0` and `v_d=0`.  Unique factorization of the quadratic says

\[
                  b(v)\in
       \mathbb C^*v_c^2\ \cup\ \mathbb C^*v_cv_d\ \cup\
       \mathbb C^*v_d^2.                               \tag{20}
\]

Choose a generic point on one of its line components.  It avoids (19),
one active coordinate is zero, and the other is nonzero.  Equation (18)
then puts one nonzero pure tensor in `J_v^[2]`, while none of its local
factors is parallel to `v`.  This contradicts Lemma 2.1.  Hence

\[
                              |A|\le1.                  \tag{21}
\]

Finally suppose `A={c}`.  If the conic contains a point outside (19) with
`v_c!=0`, Lemma 2.1 gives the same contradiction.  Therefore its whole
infinite support lies on `v_c=0`, and unique factorization forces

\[
                              b(v)=\lambda v_c^2,
             \qquad \lambda\ne0.                       \tag{22}
\]

This also shows that `T` cannot be zero: if it were, (16) would permit us
to use the identically zero effective quadratic and choose a general
`v`.  Statements (21)--(22) prove all assertions in Section 1.

## 4. Exact application to the live-component cap equations

Normalize every invertible live matrix by applying `P_i^{-1}` at site
`i`.  Then

\[
                         p_c=\sum_{i\in U}e_c^{(i)},
       \qquad X_c=\bigotimes_{i\in U}(P_i^{-1}e_c),     \tag{23}
\]

and the three factors at each site in (23) form an arbitrary basis.  Write
`Z=W setminus U` and choose, independently at every outside site,

\[
                  \ell_z\in L_z:=
                    \operatorname {Ann}(\operatorname {im}P_z).
                                                                    \tag{24}
\]

Since `S_z=P_zDelta`, each `ell_z` kills both deleted-star rows.  Hence both
marked factors in every contracted product are forced onto `U`.  With

\[
\begin{aligned}
 R(\ell)&=
 \left\langle {q^{r-1}\over(r-1)!},
                    \bigotimes_{z\in Z}\ell_z\right\rangle,\\
 T(\ell)&=
 \left\langle {q^r\over r!},
                    \bigotimes_{z\in Z}\ell_z\right\rangle,
\end{aligned}                                                       \tag{25}
\]

the contracted polarized cap equations are exactly (4)--(5), with the
same symmetric direct-block matrix `B=A_pq Delta^{-1}` and

\[
              t_c(\ell)={1\over d_c}
                         \prod_{z\in Z}\ell_z(e_c).                  \tag{26}
\]

Here `1/d_c` is nonzero.  Thus the theorem is valid without any
target-alignment assumption: for every tuple `ell`, at most one of the
three values in (26) can be nonzero.

The parameter space

\[
                              \prod_{z\in Z}L_z                     \tag{27}
\]

is an irreducible affine space.  The product in (26) is a nonzero
polynomial exactly when

\[
                       e_c\notin\operatorname {im}P_z
                              \quad\hbox{for every }z\in Z.         \tag{28}
\]

Indeed, the factor `ell_z mapsto ell_z(e_c)` vanishes identically on `L_z`
exactly when `e_c` belongs to `L_z^perp=im P_z`.  If two of the three
polynomials (26) were nonzero, their nonvanishing open sets in (27) would
intersect, contrary to the theorem.  Hence at least two colours have a
covering outside site

\[
                              e_c\in\operatorname {im}P_z.          \tag{29}
\]

Thus the two-colour target-cover conclusion previously known for three
live sites holds for a live component of every size.  The sharper part of
the theorem gives the exact dependence on the direct block:

* if `B` is not a nonzero scalar multiple of one coordinate matrix
  `E_cc`, all three target axes must be covered by outside images;
* if `B=lambda E_cc` with `lambda!=0`, the two axes `e_d`, `d!=c`, must
  be covered, while `e_c` may remain uncovered;
* in particular `B=0` forces coverage of all three axes.

There is a tuple for which all three values (26) are nonzero if and only
if **no** outside image `im P_z` contains **any** of the three target
axes.  This is the precise hypothesis behind the instruction to choose
all three target contractions nonzero; it is not automatic for general
singular outside stars.

If all sites outside `U` are literal `P=S=0` sites, that hypothesis holds,
and a tuple with all three target coefficients nonzero contradicts (21).
Thus the zero-complement live residual is excluded for arbitrary
invertible `P_i`, not merely for target-aligned live bases.  The same
conclusion holds when `U=W`: the product in (26) is the empty product `1`,
so the uncontracted three target coefficients are all nonzero.

## 5. Low live sizes and the zero direct block

The proof above includes `m=2` without a convention exception.  There is
also a direct audit.  Here `R` is a scalar and the three tensors

\[
 e_0\otimes e_1+e_1\otimes e_0,\quad
 e_0\otimes e_2+e_2\otimes e_0,\quad
 e_1\otimes e_2+e_2\otimes e_1                         \tag{30}
\]

are linearly independent.  Since (4) puts their scalar multiples on the
one line `C T`, one gets `R=0`.  Equations (5) then put every surviving
target on `C T`, so at most one can survive.  If `B=0` or `T=0`, none
survives.

For `m=3`, write the three one-hole cofactors of `R` as `R_1,R_2,R_3`.
The exact three-site tensor lemma in
[`three-live-site-annihilator-diagonal-collapse.md`](three-live-site-annihilator-diagonal-collapse.md)
says that the three off-diagonal products can span a line only when all
three `R_i` vanish.  Again (5) leaves at most one target on `C T`, and
leaves none when `B=0` or `T=0`.  Thus the new proof agrees with, and
strictly generalizes, both previously audited low-size calculations.

For arbitrary `m`, the case `B=0` is worth isolating.  Equation (16) has
no `T` term for **every** `v`, so the isotropic set is all of `P^2`.
Choosing a general `v` in Sections 2--3 proves

\[
                              t_0=t_1=t_2=0.             \tag{31}
\]

Consequently every outside annihilator contraction of a live chart with
`A_pq=0` has zero diagonal target coefficients, and (26)--(29) force all
three target axes to occur in the images of outside singular stars.

## 6. Scope of the closure

Within the row--column-basis corank-two chart, assume the connected
spanning nonbipartite rank-three graph has a live relation edge.  The live
propagation theorem supplies `S_i=P_iDelta`, the invertible component `U`,
and the symmetric matrix `B`.  The present lemma closes exactly the
following subbranches:

1. `U=W` (the live component spans all internal sites);
2. every proper live component whose entire complement has `P_z=S_z=0`;
3. more generally, every proper live component for which fewer than two
   target axes are covered by outside images;
4. if `B` is not `lambda E_cc` for a nonzero `lambda`, every proper live
   component for which even one target axis is not covered outside.

No witness count is used in these closures.  What remains inside this live
corank-two branch is sharply identified: nonzero singular-star sites beyond
the literal zero boundary must cover at least two target axes, and must
cover all three unless `B=lambda E_cc`.  The annihilator contractions do
not separate the full outside tensor space in that escape, so this note
alone does not prove the uncontracted bound `rank(overline Phi)<=1` there.

The argument concerns the live alternative only.  It does not by itself
replace the separate all-dead product-geometry closure, nor the earlier
reductions needed when the excess quotient, row--column basis hypotheses,
or connected nonbipartite rank-three graph hypotheses fail.

## 7. Exact audit

[`verify_coordinate_free_live_diagonal_square_ideal.py`](../computations/verify_coordinate_free_live_diagonal_square_ideal.py)
checks the degree-zero and degree-one coefficient calculation in Lemma 2.2
symbolically, verifies the rank argument in Lemma 2.3 on generic exact
rational bases for `2<=m<=6`, audits the three quadratic factor forms in
(20), and checks the direct `m=2`, `m=3`, and `B=0` conclusions.
