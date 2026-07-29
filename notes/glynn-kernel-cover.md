# Glynn kernel covers do not lift to the incidence tensor

## 1. What the cover would prove

For normalized signs `delta_0=1`, Glynn's identity is the tensor identity

\[
 \operatorname {Per}_m=2^{1-m}\sum_\delta
 \left(\prod_i\delta_i\right)\delta^{\otimes m}.             \tag{1}
\]

Suppose three sign vectors `s_0,s_1,s_2` survive and, at mode `j`, a
codimension-three kernel `K_j` contains its assigned killed signs and is
complementary to `S=span(s_0,s_1,s_2)`.  The quotient map can then be
postcomposed with the inverse of its restriction to `S`, so that it sends
`s_r` to a chosen nonzero multiple of `e_r`.  If the union of the kernels
contains every other sign, (1) leaves exactly three diagonal terms.  Mode
scalings normalize their coefficients.  Thus the proposed finite cover
really would prove

\[
                 \operatorname {Per}_m\longrightarrow\Delta_{m,3}. \tag{2}
\]

For `m=8`, however, even the underlying affine cover is impossible with
eight kernels.  The normalized signs form `F_2^7`, and each three-equality
kernel cuts out a 16-point affine codimension-three flat.  Eight such flats
covering exactly 125 points would have overlap excess `128-125=3`.  If two
codimension-three flats in `F_2^7` meet, their intersection has dimension at
least one and hence at least two points.  In each connected component of the
intersection graph, order the flats along a spanning tree.  Every flat after
the first overlaps the preceding union in at least two points.  A component
of at least three flats therefore has excess at least four, while a component
of two has excess equal to a power of two and cannot have excess three.
Several nontrivial components again have total excess at least four.  Hence
eight flats cannot have union size 125; this signed-forest construction needs
at least nine kernels at `m=8`.

## 2. Why (2) does not give a `K_{m,m}` counterexample

The full perfect-matching incidence tensor has twice as many modes:

\[
 T_{K_{m,m}}=\sum_{\sigma\in S_m}
 \left(\bigotimes_{i\in L}e_{\sigma(i)}\right)\otimes
 \left(\bigotimes_{j\in R}e_{\sigma^{-1}(j)}\right).         \tag{3}
\]

Contracting either shore against all-ones covectors gives the `m`-mode
permanent tensor, but a restriction of that contraction is not a restriction
of (3).  Before the other shore is contracted, its `m!` displayed basis
tensors distinguish all permutations.  The cancellations in Glynn's formula
therefore do not occur term by term in (3).

There is a second way to see the gap.  Let `Q_j:C^m -> C^3` be the quotient
maps from a cover and try the natural diagonal edge lift

\[
 A_{ij}=\sum_{r=0}^2 Q_j(r,i)e_r\otimes e_r.                 \tag{4}
\]

For a left coloring with classes `I_r` and a right coloring with classes
`J_r`, its coefficient is

\[
       \prod_{r=0}^2 \operatorname {per}
       \bigl(Q_j(r,i)\bigr)_{i\in I_r,j\in J_r}.             \tag{5}
\]

The mixed-coordinate equation in (2) only says that the sum of (5) over all
compatible left colorings is zero.  The `2m`-mode diagonal target requires
every individual expression (5) to vanish.  Thus neither the quotient maps
nor their evident diagonal edge lift supplies the missing shore.  The phrase
"hence a `K_{m,m}` counterexample" is unjustified.

## 3. Exact obstruction to the cyclic Fourier ansatz on `K_{5,5}`

Index both shores by `F_5` and let `zeta` be a primitive fifth root of unity.
The multiplicity-free cyclic-character ansatz, including arbitrary nonzero
vertex/color gauges, is

\[
 L_i e_j=\sum_{r=0}^2\lambda_{i,r}
          \zeta^{p_r(j-i)}e_r,\qquad
 R_j e_i=\sum_{r=0}^2\mu_{j,r}
          \zeta^{q_r(i-j)}e_r.                              \tag{6}
\]

The three `q_r` must be distinct.  Otherwise every right local map has two
proportional rows and rank at most two, whereas every mode flattening of
`Delta_{10,3}` has rank three.  Also every gauge in (6) is nonzero: the
coefficient of the all-`r` coloring is
`5! product_i lambda_(i,r) product_j mu_(j,r)` and must be nonzero.

All three-subsets of `F_5` are equivalent under `q -> aq+b`: their
two-element complements are, and the affine group is transitive on unordered
pairs.  Normalize the right characters to `{0,1,2}`.  Color every left
vertex by one fixed color and give right vertices `0,...,4` the character
values

\[
                         (0,0,2,1,2).                       \tag{7}
\]

The left phase in (6) is zero because
`sum_i(sigma(i)-i)=0`.  Direct exact enumeration of the 120 permutations
gives the following multiplicities for the right phase

\[
 \sum_jq_{d_j}(\sigma^{-1}(j)-j)\pmod 5:
                         (40,20,20,20,20).                  \tag{8}
\]

Consequently the mixed coefficient is a nonzero gauge product times

\[
 40+20(\zeta+\zeta^2+\zeta^3+\zeta^4)=20,                 \tag{9}
\]

although `Delta_{10,3}` requires it to vanish.  Affine translation of the
characters cancels from the phase, and affine scaling only permutes the four
nonzero residue bins.  This excludes every choice of three cyclic characters
on the right, independently of the left characters.

The exact integer audit is
`computations/verify_k55_fourier_obstruction.py`.
