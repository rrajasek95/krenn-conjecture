# Half-shift collision: no splitting over a least-cell base

This note isolates a uniform part of the color-collision argument.  Over a
base point having the least possible number of scalar cells, the second jet
required to separate two coincident colors does not exist.  The proof is
valid for every even `n >= 4` and for arbitrary nonzero edge weights.  It is
not a proof for an arbitrary point of the fiber: the final section states
the exact two-step transport lemma still needed for that extension.

Throughout, the ground field has characteristic zero, `B` has even size
`n=2m`, and every local space has basis `x,y,z`.  It is convenient to work
in the squarefree commutative algebra

\[
 \mathcal R=\mathbb C[x_i,y_i,z_i:i\in B]/
 (u_i v_i:u_i,v_i\in\{x_i,y_i,z_i\}).                    \tag{1}
\]

A quadratic source `q` is supported on monomials with two different site
indices.  With

\[
                         H(q)=\frac{q^m}{m!},              \tag{2}
\]

the coefficient of a coloring is its usual weighted perfect-matching sum.
Put

\[
 X=\prod_i x_i,\qquad Y=\prod_i y_i,
 \qquad X_2=\sum_{i<j}z_i z_j\prod_{v\ne i,j}x_v.          \tag{3}
\]

## 1. The normalized collision equations

The symmetric half-shift of the two coincident `x` branches is

\[
 Y+\prod_i(x_i-tz_i/2)+\prod_i(x_i+tz_i/2)
       =2X+Y+\frac{t^2}{2}X_2+O(t^4).                     \tag{4}
\]

Consequently a source two-jet

\[
                         q(t)=q_0+tZ+t^2Y_2               \tag{5}
\]

would have to satisfy

\[
\begin{aligned}
 H(q_0)&=2X+Y,\\
 dH_{q_0}(Z)&=\frac{Zq_0^{m-1}}{(m-1)!}=0,\\
 dH_{q_0}(Y_2)+\frac12d^2H_{q_0}(Z,Z)
 &=\frac{Y_2q_0^{m-1}}{(m-1)!}
   +\frac{Z^2q_0^{m-2}}{2(m-2)!}
   =\frac12X_2.                                           \tag{6}
\end{aligned}
\]

These factorials matter.  Formula (6), rather than an unnormalized power
identity, is used below.

The half-shift also imposes an important source grading: `q_0` has
`z`-degree zero, `Z` has exactly one `z` on every cell, and `Y_2` has
exactly two.  Thus

\[
 Z=\sum_i z_i k_i,\qquad
 k_i\in\operatorname{span}\{x_j,y_j:j\ne i\},\qquad
 Y_2=\sum_{i<j}\eta_{ij}z_i z_j.                           \tag{6a}
\]

This is not an extra normal-form assumption: it is the degree decomposition
of a quadratic source under the local substitution used in (4).

## 2. Why a least-cell base is an alternating Hamilton cycle

Count a nonzero scalar matrix entry, rather than a nonzero underlying edge,
as one cell.  Call `q_0` **least-cell** if its cell count is minimum among
all sources satisfying `H(q_0)=2X+Y`.  This is stronger than mere
inclusion-minimality of its current support.

**Lemma 2.1 (sharp weighted binary normal form).**  A least-cell source for
`2X+Y` has exactly `n` cells.  They are

\[
 q_0=\sum_{uv\in P_x}a_{uv}x_ux_v
        +\sum_{uv\in P_y}b_{uv}y_uy_v,                    \tag{7}
\]

where `P_x` and `P_y` are edge-disjoint perfect matchings whose union is
one alternating Hamilton cycle, and

\[
                  \prod_{uv\in P_x}a_{uv}=2,
                  \qquad\prod_{uv\in P_y}b_{uv}=1.        \tag{8}
\]

**Proof.**  The nonzero coefficient `2` of `X` contains at least one
nonzero matching monomial; choose its `m` distinct `xx` cells and call its
matching `P_x`.  The coefficient `1` of `Y` similarly supplies `m`
distinct `yy` cells and a matching `P_y`.  The two cell sets are disjoint,
even if an underlying edge is shared, so every source has at least
`2m=n` cells.

Conversely, choose any alternating Hamilton cycle, put nonzero `xx` cells
on one factor and nonzero `yy` cells on the other, and choose their products
to be `2` and `1`.  The cycle has exactly its two alternating perfect
matchings, so this is an `n`-cell realization.  A least-cell source
therefore has exactly `n` cells, and the two selected constant matchings
exhaust its support.  In particular it has no mixed or `z` cell.

Regard differently colored cells on a shared underlying edge as distinct
edge occurrences.  The 2-regular occurrence graph `P_x union P_y` is a
disjoint union of alternating even cycles.  If it had more than one
component, use the `x` factor on a nonempty proper collection of components
and the `y` factor on the others.  At every vertex the prescribed color has
only its selected matching cell available, so this mixed coloring has one
contributing matching and a nonzero coefficient.  That contradicts
`H(q_0)=2X+Y`.  Hence the occurrence graph is connected.  For `n>=4` it is
an alternating Hamilton cycle and the matchings are edge-disjoint.  Its
only supported perfect matchings are `P_x,P_y`, so their weights are the
two target coefficients, giving (8).  \(\square\)

This is the weighted `2X+Y` version of the binary equality classification
in [`binary-entry-minimal-normal-form.md`](binary-entry-minimal-normal-form.md).
The proof was repeated because the distinction between least-cell and
inclusion-minimal is essential for collision transport.

## 3. Deleted-cycle cofactors

Number the vertices cyclically so that

\[
 P_x=01\mid23\mid\cdots\mid(n-2,n-1),\qquad
 P_y=12\mid34\mid\cdots\mid(n-1,0).                       \tag{9}
\]

For different vertices `i,j`, let

\[
 C_{ij}=H_{B\setminus\{i,j\}}(q_0)                        \tag{10}
\]

be the common cofactor.  The parity in the following lemma is the
bipartition parity of the Hamilton cycle.

**Lemma 3.1 (parity and domain walls).**

1. If `i` and `j` have the same parity, then `C_ij=0`.
2. If they have opposite parity, deleting them leaves two even paths.
   Each path has a unique perfect matching, so `C_ij` is one nonzero
   coordinate tensor.
3. For a fixed `i`, the `n` tensors

   \[
      z_i x_j C_{ij},\qquad z_i y_j C_{ij}
      \quad(j\text{ of parity opposite to }i)              \tag{11}
   \]

   are pairwise distinct coordinate tensors and hence linearly independent.

**Proof.**  Deleting two sites of a cycle produces the two open arcs
between them.  If the sites have the same bipartition parity, both arcs
have an odd number of remaining vertices and neither can be perfectly
matched.  If their parities differ, both arcs have even order and each has
the unique consecutive-edge matching.  Every chosen edge lies alternately
in `P_x` and `P_y`, proving the first two claims, including nonvanishing
because all weights in (7) are nonzero.

For the last claim, rotate by an even number of sites and take `i=0`; an
odd rotation merely interchanges `x` and `y`.  Write `j=2r+1`.  The forced
matching on the path `1,...,j-1` consists of the `P_y` edges, and the one on
`j+1,...,n-1` consists of the `P_x` edges.  Explicitly,

\[
 C_{0,2r+1}=
 \left(\prod_{s=0}^{r-1}b_{2s+1,2s+2}\right)
 \left(\prod_{s=r+1}^{m-1}a_{2s,2s+1}\right)
 \left(\prod_{v=1}^{2r}y_v\right)
 \left(\prod_{v=2r+2}^{n-1}x_v\right).
\]

Empty products are one.  On filling site `j` with `x_j` or `y_j`, the set
of `y`-colored sites in the ordered list `1,...,n-1` is respectively an
initial segment of length `2r` or `2r+1`.  As `r=0,...,m-1`, these are the
`n` different initial-segment lengths `0,...,n-1`.  Hence all tensors in
(11) are distinct.  Their displayed scalar factors are nonzero, proving
independence. \(\square\)

## 4. Exact one-`z` tangent kernel

For a fixed site `i`, write the sector of `Z` whose unique `z` occurs at
`i` as

\[
 Z_i=\sum_{j\ne i}z_i(\alpha_{ij}x_j+\beta_{ij}y_j).       \tag{12}
\]

The `z_i` sector of the tangent equation in (6) is

\[
          \sum_{j\ne i}z_i
             (\alpha_{ij}x_j+\beta_{ij}y_j)C_{ij}=0.       \tag{13}
\]

Lemma 3.1 shows immediately that

\[
 \alpha_{ij}=\beta_{ij}=0
       \quad\text{whenever }i,j\text{ have opposite parity}.           \tag{14}
\]

Conversely, every cell in (12) joining same-parity sites has zero cofactor
and is tangent-invisible.  Hence (14) is the complete exact-one-`z`
tangent-kernel classification: a `z` can be paired only with an `x` or `y`
on its own shore of the Hamilton bipartition.

## 5. The uniform second-order contradiction

**Theorem 5.1 (least-cell no-splitting theorem).**  Let `n>=4` be even and
let `q_0` be least-cell in the fiber `H(q_0)=2X+Y`.  There are no `Z,Y_2`
satisfying the collision equations (6) with the half-shift gradings (6a).

**Proof.**  Choose distinct same-parity sites `i,j`; such a pair exists for
`n>=4`.  Extract from the last equation of (6) the coefficient of

\[
                  z_i z_j\prod_{v\ne i,j}x_v.             \tag{15}
\]

The exactly-two-`z` part of `Y_2` can contribute to (15) only through its
cell `z_i z_j`.  Its derivative coefficient is the all-`x` coefficient of
`C_ij`, which is zero by Lemma 3.1.

It remains to inspect `Z^2`.  A nonzero contribution to (15) would use two
disjoint one-`z` cells

\[
                         z_i x_u,\qquad z_j x_v             \tag{16}
\]

and complete the remaining vertices using `xx` cells of `q_0`, namely
edges of `P_x`.  The factor `1/2` in (6) cancels the two orders of two
distinct tangent cells, so there is no hidden combinatorial scalar.  By
(14), `u` has the same parity as `i` and `v` the same
parity as `j`.  Thus all four removed sites `i,j,u,v` lie on the same shore
of the bipartition.  No collection of `P_x` edges can cover the remaining
vertices: every `P_x` edge joins opposite shores.  Overlaps among the four
sites make the product in (16) zero and do not create another case.

Both terms on the left side of the last equation in (6) therefore have
coefficient zero at (15), whereas the right side has coefficient `1/2`.
This is the desired contradiction. \(\square\)

The proof is weight-independent and uses no genericity.  The restriction
`n>=6` relevant to the Krenn problem is therefore comfortably inside its
range.  The known four-site collision arc lives over a nonminimal six-cell
base, so it does not contradict Theorem 5.1.

There is a small support-excess extension which does not require transport.

**Proposition 5.2 (one extra base cell still cannot split).**  For even
`n>=4`, no collision two-jet exists over an exact binary base with at most
`n+1` nonzero scalar cells.

**Proof.**  Theorem 5.1 handles `n` cells.  Suppose there are `n+1`.
Choose one nonzero all-`x` matching and one nonzero all-`y` matching; their
`n` scalar cells are distinct.  Their occurrence union must be Hamilton.
Indeed, if it had two components, choosing the `x` factor on some
components and the `y` factor on the others would give a mixed matching.
A cancellation mate differs on an alternating cycle and therefore needs at
least two cells outside the selected `n`, whereas only one is available.

Let `h` be the weighted Hamilton subsource on the selected cells and let
`E` be the remaining cell.  The cell `E` is tensor-inactive.  To see this,
fix the coloring of a matching using it.  Away from the endpoints of `E`,
each vertex has at most its unique compatible selected `P_x`- or `P_y`-cell.
Thus there is at most one supported matching using `E`; it cannot occur in
a mixed zero coefficient.  It also cannot give a second constant matching,
because two different perfect matchings differ on an alternating cycle and
hence each has at least two edges absent from the other.  Consequently
`dH_h(E)=0`, `H(h)=2X+Y`, and the endpoints `u,v` of `E` lie
on the same shore of the Hamilton cycle: by Lemma 3.1 an opposite-shore
cell has a nonzero coordinate cofactor.

Now use the pair `u,v` in the second collision equation.  Every cofactor in
the first tangent equation whose unique `z` is at `u` deletes `u`, and
therefore deletes `E`; that star equation is exactly the Hamilton one.
The same is true at `v`.  Hence Lemma 3.1 again forces the companion of
each one-`z` tangent cell at `u` or `v` to lie on the same cycle shore.
The direct `z_uz_v` second-order cell has zero cofactor, since deleting
`u,v` deletes `E` and leaves the two odd Hamilton paths.  Finally, a
quadratic tangent term already occupies `u,v`, so its remaining base
completion cannot use `E`; it reduces to the shore-imbalance argument in
Theorem 5.1.  The coefficient of
\(z_uz_v\prod_{w\ne u,v}x_w\) is again zero instead of `1/2`.
\(\square\)

Thus any putative six-or-more-site collision base must have at least two
cells beyond the sharp binary minimum.  This conclusion comes directly
from the jet equations; it does not move the base inside its fiber.

## 6. Exact transport equations for an arbitrary base

Theorem 5.1 becomes a theorem for arbitrary `q_0` if a collision two-jet
can always be transported to a least-cell base.  Here is the precise local
problem.

Let `D` be supported on one star, say all its cells meet `p`, and suppose

\[
                            dH_q(D)=0.                     \tag{17}
\]

Because `D^2=0` in the squarefree algebra,

\[
                         H(q+sD)=H(q)                      \tag{18}
\]

for every scalar `s`.  If `D` is supported on current nonzero cells, one
can choose `s` to delete a cell without adding a base cell.  Preserving the
collision jet is subtler.  Seek

\[
 Z_s=Z+sK+O(s^2),\qquad Y_s=Y_2+sL+O(s^2).                \tag{19}
\]

For an exact affine star transport, `K` and `L` are also required to be
supported on the `p`-star.  Allowing them in the full source space gives a
weaker necessary test but no longer by itself makes (18) valid for the
transported jet.

Differentiating the two equations in (6) with respect to `s` gives the
necessary infinitesimal transport equations

\[
\begin{aligned}
 dH_q(K)+d^2H_q(D,Z)&=0,                                  \tag{20}\\
 dH_q(L)+d^2H_q(D,Y_2)+d^2H_q(Z,K)
                  +\frac12d^3H_q(D,Z,Z)&=0.               \tag{21}
\end{aligned}
\]

Thus the first obstruction is the class

\[
 [d^2H_q(D,Z)]\in
 \operatorname{coker}\!\left(dH_q\big|_{\mathcal S_p}\right),         \tag{22}
\]

where `S_p` is the `p`-star source space, further restricted to the required
source grading.  Once `K` is chosen, (21) gives the second obstruction class
in the same cokernel.

There is an equivalent and more useful star-syzygy formulation.  Let
`F_p(t)` be the common-cofactor matrix that maps a `p`-star variation to
`dH_{q(t)}` of that variation, where

\[
 q(t)=q+tZ+t^2Y_2,\qquad
 F_p(t)=F_0+tF_1+t^2F_2\pmod {t^3}.                        \tag{23}
\]

With the normalization (2), its coefficients are

\[
 F_0(D)=dH_q(D),\qquad F_1(D)=d^2H_q(Z,D),\qquad
 F_2(D)=d^2H_q(Y_2,D)+\frac12d^3H_q(Z,Z,D).
\]

A star kernel vector `D_0` transports through the collision jet exactly
when it lifts to

\[
 D(t)=D_0+tD_1+t^2D_2,\qquad F_p(t)D(t)=0\pmod {t^3}.       \tag{24}
\]

Here `D_r` has `z`-degree `r`; this is the grading required for the
transported source still to be a half-shift jet.

Coefficient comparison gives

\[
\begin{aligned}
 F_0D_0&=0,\\
 F_0D_1&=-F_1D_0,\\
 F_0D_2&=-F_1D_1-F_2D_0.                                  \tag{25}
\end{aligned}
\]

The two cokernel classes in (25) are exactly the star-restricted versions
of (20)--(21), expressed before contracting the fixed star.  If (24) holds,
then

\[
                  q_s(t)=q(t)+sD(t)                       \tag{26}
\]

has the same target modulo `t^3` for every `s`, since every two terms of
`D(t)` meet at `p`.  Choosing `s` to kill a base cell transports the full
collision two-jet while decreasing the support of `q`.

The needed global statement is therefore the following.

**Transport lemma still open (`n>=6`).**  If a collision two-jet (6) exists
over a base with more than `n` cells, there is a vertex `p` and a nonzero
support-preserving `p`-star vector `D_0` such that:

1. `F_0D_0=0` and some scalar choice in (26) deletes a base cell; and
2. `D_0` lifts through both equations in (25).

Iterating this lemma reaches a least-cell base, where Theorem 5.1 gives a
contradiction.  Notice that item 1 itself is a global support-descent
assertion; inclusion-minimal points with more than `n` cells cannot simply
be assumed away.

The rerouting-circuit classification identifies, but does not yet kill,
the obstruction to item 2.  A nonzero coordinate of `F_1D_0` can be
followed through the zero mixed-color coefficient equations.  A
support-minimal cancellation web is either an even alternating cycle or
two odd cycles joined by a path (the path has twice the cycle magnitude).
Those are precisely the finite circuits described in
[`fixed-star-mixed-cofactor-chase.md`](fixed-star-mixed-cofactor-chase.md).
A clean closure supplies a local preimage candidate for `D_1`; if the web
reroutes in another color, it is the local manifestation of the cokernel
class in the second line of (25).  Assembling the local candidates into one
global preimage is an additional compatibility condition.  The third line
repeats the same question with one marked quadratic
interaction.  What remains is to prove that the prescribed nonzero
`X_2/2` coefficient forbids every fully rerouted cycle and odd handcuff,
or else forces one of them to close cleanly.  The Hamilton parity argument
above is exactly the terminal clean-closure calculation.

The restriction in this proposed transport lemma is genuine: transport is
not a formal consequence of `D_0^2=0`.  At four sites let

\[
 P_-=01\mid23,\qquad P_y=02\mid13,\qquad P_+=03\mid12,
\]

put \(\ell_i^\pm=x_i\pm t z_i/2\), and take

\[
 q(t)=\sum_{uv\in P_-}\ell_u^-\ell_v^-
      +\sum_{uv\in P_y}y_uy_v
      +\sum_{uv\in P_+}\ell_u^+\ell_v^+.
\]

The three perfect matchings of `K_4` show that this is an exact collision
arc.  At the star `p=0`, the only support-preserving base-star kernel is,
up to scale,

\[
                         D_0=x_0x_1-x_0x_3.
\]

Its first transport defect is

\[
 F_1D_0=-x_0x_1z_2x_3
         -\frac12x_0x_1x_2z_3
         -\frac12x_0z_1x_2x_3.
\]

In particular the coefficient at `x_0x_1z_2x_3` is `-1`.  Every one-`z`
0-star preimage of that coloring would have to use the cell `x_0z_2`, but
its complementary base cofactor is the `yy` cell on `13`.  Hence that
coefficient annihilates `im F_0`, and `[F_1D_0]` is nonzero.  By symmetry
the same holds at every star.  This explains simultaneously why the
four-site arc survives and why an `n>=6` argument must use the extra room in
the rerouting circuits.

[`verify_hamilton_collision_no_splitting.py`](../computations/verify_hamilton_collision_no_splitting.py)
audits every combinatorial assertion in Sections 2--5 for
`n=4,6,8,10,12`, including arbitrary deleted pairs and every possible
same-shore kernel-cell product.  It also verifies the displayed four-site
transport obstruction at all four stars.
