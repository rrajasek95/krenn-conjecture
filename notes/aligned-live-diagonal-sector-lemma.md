# An aligned live component cannot carry two diagonal target values

## 1. Statement

Let `U` be a set of `m>=2` sites, with a fixed copy of
`V=C^3` at every site, and work in the site-square-zero algebra on `U`.
Put

\[
                         p(x)=\sum_{i\in U}x^{(i)}.       \tag{1}
\]

Let `R` have site degree `m-2`, let `T` be an arbitrary top-support
tensor, and let `B=(b_cd)` be symmetric.  Suppose

\[
 p(e_c)p(e_d)R+b_{cd}T=0\quad(c\ne d),                 \tag{2}
\]

and

 p(e_c)^2R+b_{cc}T=t_cX_c,qquad
 X_c=\bigotimes_{i\in U}e_c^{(i)}.                     \tag{3}
\]

Then at most one of `t_0,t_1,t_2` is nonzero.  More sharply:

* if `T=0`, all three `t_c` vanish;
* if some off-diagonal entry of `B` is nonzero, all three `t_c` vanish;
* if `T!=0` and `B` is diagonal, at most one `t_c` is nonzero.

This is an exact characteristic-zero coefficient lemma.  It applies after
an outside-star annihilator contraction whenever the live-site `p` bases
are aligned with the three local target bases.  That alignment hypothesis
is essential to this formulation: normalizing arbitrary invertible
matrices `P_i` sends the local target factors to `P_i^{-1}e_c`, so the
lemma must not be quoted for a general live component without an additional
alignment argument.

The required generalization is now proved in
[`coordinate-free-live-diagonal-square-ideal.md`](coordinate-free-live-diagonal-square-ideal.md).
It allows the three target factors `P_i^{-1}e_c` to form an arbitrary basis
at every live site.  The present colour-sector proof remains a useful
coefficient-level special case, but its former alignment caveat is no longer
a gap in the live-component argument.

## 2. The one-defect coefficients

Fix a colour `c`.  The pure-`c` part of `R` is uniquely

\[
 R^{(c)}=\sum_{\{i,j\}\subset U}r_{ij}^{(c)}
             \bigotimes_{k\in U\setminus\{i,j\}}e_c^{(k)}.          \tag{4}
\]

For `e!=c`, let `w_j(c,e)` be the full word which is `e` at site `j`
and `c` everywhere else.  Direct multiplication gives

\[
 [w_j(c,e)]\,p(e_c)p(e_e)R
       =\rho_j^{(c)},qquad
 \rho_j^{(c)}:=\sum_{i\ne j}r_{ij}^{(c)},               \tag{5}
\]

up to the one harmless common convention factor in the symmetrized
product.  Similarly,

\[
 [X_c],p(e_c)^2R
       =2\sum_{i<j}r_{ij}^{(c)}
       =\sum_j\rho_j^{(c)}.                              \tag{6}
\]

Equations (5)--(6) remain literal for `m=2`: there is one coefficient
`r_12`, the two row sums both equal it, and (6) is `2r_12`.  For `m=3`
they are the three pair coefficients and the familiar invertible
three-by-three row-sum system.  No separate low-order exception is hidden.

There is also a useful uniqueness observation.  Among the three
off-diagonal products, only `p(e_c)p(e_e)R` can contribute to the sector
with colour count

\[
                         (m-1)e_c+e_e.                  \tag{7}
\]

Indeed, either other off-diagonal pair inserts the third colour, so its
putative residual colour count has a negative coordinate.

## 3. Proof of the lemma

If `T=0`, (2) makes every off-diagonal product zero.  Equation (5), for
any `e!=c`, gives all `rho_j^(c)=0`; (6) then says that the `X_c`
coefficient of the left side of (3) is zero.  Since no other colour sector
contributes to `X_c`, one gets `t_c=0` for every `c`.

Assume now that `T!=0` and that some off-diagonal `b_cd` is nonzero.
No off-diagonal product has a monochromatic coefficient, so (2) first
gives

\[
                         [X_c]T=0\qquad(c=0,1,2).        \tag{8}
\]

We next make the row sums in (5) vanish.  If at least two of
`b_01,b_02,b_12` are nonzero, fix `c` and choose `e!=c`.  When `b_ce=0`,
(2) and (5) give `rho_j^(c)=0` directly.  When `b_ce!=0`, compare its
coefficient at `w_j(c,e)` with any other nonzero off-diagonal equation.
The uniqueness observation (7) says that the other product contributes
zero there; its nonzero coefficient of `T` therefore forces
`[w_j(c,e)]T=0`, and the `(c,e)` equation again gives
`rho_j^(c)=0`.

If exactly one off-diagonal entry is nonzero, each vertex of the
three-colour triangle is incident with a zero entry.  For each `c`, choose
such a zero incident pair `(c,e)` and apply (5) directly.  Thus in every
nonzero off-diagonal case

\[
                         \rho_j^{(c)}=0
                         \quad(j\in U, c=0,1,2).        \tag{9}
\]

Equations (6), (8), and (3) now give `t_c=0` for all three colours.

It remains that `B` is diagonal.  Equation (2) again gives (9), hence the
`X_c` coefficient of `p(e_c)^2R` is zero.  Moreover, for `d!=c`, the
product `p(e_d)^2R` has zero `X_c` coefficient simply because it inserts
two copies of colour `d`.  Taking the `X_c` coefficient in all three
instances of (3) therefore gives

\[
                         b_{cc}[X_c]T=t_c,qquad
                         b_{dd}[X_c]T=0\quad(d\ne c).    \tag{10}
\]

If `t_c!=0`, then both `b_cc` and `[X_c]T` are nonzero, while (10) forces
`b_dd=0` for the other two colours.  A second nonzero `t_d` would require
that same `b_dd` to be nonzero, a contradiction.  This proves the lemma.

## 4. Consequence for the aligned zero complement

Suppose a live component has arbitrary size `m>=2`, all sites outside it
have `P_z=S_z=0`, and after normalizing its invertible `P_i` the three
local target axes are still the common coordinate axes.  Contract every
outside site by arbitrary covectors `ell_z`.  Both marked `p` factors are
forced into the live set and

\[
 R=\left\langle {q^{r-1}\over(r-1)!},
                    \bigotimes_{z\notin U}\ell_z\right\rangle      \tag{11}
\]

has degree `m-2`.  The contracted cap equations are exactly (2)--(3),
with

\[
                         t_c=\prod_{z\notin U}\ell_z(e_c).          \tag{12}
\]

Choose all the factors in (12) nonzero.  The three `t_c` are then
simultaneously nonzero, contradicting the lemma.  Hence the all-zero
outside counterconfiguration cannot be repaired by changing its internal
perfect-matching blocks, for any size of the aligned live component.

## 5. Exact audit

[`verify_aligned_live_diagonal_sector.py`](../computations/verify_aligned_live_diagonal_sector.py)
checks (5)--(6) for `2<=m<=7` over the rationals and exhausts the eight
zero patterns of the three off-diagonal entries to verify the row-sum
choice used in Section 3.
