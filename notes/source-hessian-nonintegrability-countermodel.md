# Extra source-Hessian kernel need not integrate

## Outcome

The singular escape in `source-derivative-hessian-dichotomy.md` cannot be
closed by assuming that an extra Hessian-kernel vector integrates to a
constant-output deformation.  A uniform binary Hamilton source is exact
and entry-minimal, every one of its pair-deleted Hessians has extra kernel,
and an explicit extra direction is also tangent to the full matching-power
fiber but is obstructed at second order.  The obstruction is an individual
mixed-color coefficient, so no cancellation or genericity assumption is
involved.

This is a countermodel to the proposed deformation principle in the same
square-zero matching-power geometry.  It does not settle the genuinely
ternary singular locus; a successful continuation must use three-color
compatibility or prove structure on the all-pair determinantal locus.

## 1. The universal second-order obstruction

Let `q` be a quadratic on `2r` square-zero sites.  If

\[
 q(t)=q+tZ+t^2Y+O(t^3)
\]

and `q(t)^r=q^r`, then the first two nonconstant coefficients give

\[
 Zq^{r-1}=0,
 \qquad
 Yq^{r-1}+\frac{r-1}{2}Z^2q^{r-2}=0.                    \tag{1}
\]

Thus an element of `ker H_q` can integrate only if the class of
`Z^2q^(r-2)` vanishes in `coker H_q`.  This elementary obstruction remains
valid for formal, algebraic, or holomorphic arcs.

## 2. An entry-minimal exact family with all-pair degeneracy

Fix even `n=2m>=6`, label the vertices modulo `n`, and take

\[
 P_0=01|23|45|\cdots|(n-2,n-1),\qquad
 P_1=12|34|\cdots|(n-1,0).
\]

In the binary site algebra put

\[
 Q=\sum_{ij\in P_0}x_{i,0}x_{j,0}
   +\sum_{ij\in P_1}x_{i,1}x_{j,1}.                     \tag{2}
\]

The support is one alternating cycle and has exactly the two perfect
matchings `P_0,P_1`.  Hence

\[
 Q^m=m!\left(\prod_i x_{i,0}+\prod_i x_{i,1}\right)
     =m!\Delta_{B,2}.                                    \tag{3}
\]

The two constant coefficients require at least `m` nonzero `00` cells and
`m` nonzero `11` cells in any binary realization.  They are distinct
scalar cells, so (2), with exactly `n` cells, is entry-minimal.

Now delete arbitrary vertices `u,v`, let `W=B\{u,v}`, and let `q` be the
restriction of `Q` to `W`.  If `u,v` have opposite parity, choose two
remaining vertices `i,j` of the same parity.  If `u,v` have the same
parity, choose one remaining vertex of that parity and one of the opposite
parity.  Such choices exist for `n>=6`.  In both cases, after also deleting
`i,j`, the two parity classes have unequal sizes.  The remaining subgraph
of the bipartite cycle has no perfect matching.

Choose on `ij` a binary cell `z` not supported by `Q_ij`.  The preceding
parity imbalance gives

\[
                         zq^{m-2}=0.                      \tag{4}
\]

Every vertex gauge is supported on the cells of `q`, while `z` is not.
Thus every pair-deleted Hessian has kernel strictly larger than its gauge
kernel.

## 3. A full tangent which cannot lift to second order

Use the particular deletion `4,5` and set

\[
 z_0=x_{0,1}x_{2,1},\qquad
 z_1=x_{1,0}x_{3,0},\qquad Z=z_0+z_1.                    \tag{5}
\]

Deleting the two even endpoints of `z_0`, or the two odd endpoints of
`z_1`, leaves unequal parity-class sizes.  Therefore

\[
                       ZQ^{m-1}=0,
 \qquad                Zq^{m-2}=0.                       \tag{6}
\]

To make the direction explicitly point toward deletion of an existing
cell, take vertex-gauge parameters

\[
 \alpha_0=-1,\qquad\alpha_2=1,qquad\alpha_i=0\ (i\ne0,2)
\]

and put

\[
 G_{ij}=(\alpha_i+\alpha_j)Q_{ij},\qquad T=Z+G.           \tag{7}
\]

Both on all vertices and on `W=B\{4,5}`, the parameters sum to zero.
Consequently

\[
 TQ^{m-1}=0,\qquad (T|_W)q^{m-2}=0.                      \tag{8}
\]

The restriction is beyond gauge because of the two cells (5).  Moreover,
the coefficient of `T` on the existing cell `Q_01(0,0)=1` is `-1`.

Let `gamma` be the full coloring

\[
 \gamma_0=\gamma_2=1,qquad \gamma_i=0\quad(i\ne0,2).    \tag{9}
\]

Exactly `m-2` cells of `Q` are compatible with `gamma`: the `P_0` edges
other than `01` and `23`.  It follows that

\[
 [\gamma](YQ^{m-1})=0                                    \tag{10}
\]

for every quadratic `Y`, because the product would require `m-1`
compatible `Q` edges after using the one `Y` edge.  In contrast, the two
cells in (5), followed by all `m-2` compatible `P_0` edges, give

\[
 [\gamma](T^2Q^{m-2})=2(m-2)!\ne0.                       \tag{11}
\]

No term involving `G` is compatible with `gamma`.

Suppose a formal constant-output arc with this tangent existed:

\[
 Q(t)=Q+tT+t^2Y+O(t^3),\qquad Q(t)^m=Q^m.
\]

At order two it would satisfy

\[
 mYQ^{m-1}+\binom m2T^2Q^{m-2}=0.                        \tag{12}
\]

Taking the `gamma` coefficient gives `0+m!=0`, a contradiction.  Hence the
extra pair-Hessian direction extends to a full first-order tangent but not
to any formal fiber deformation.  In particular, entry-minimality does not
turn all-pair Hessian degeneracy into a removable entry.

`computations/verify_hessian_nonintegrable_hamilton.py` checks (3)--(12)
over the integers and audits every pair deletion for `n=6,8,10`.
