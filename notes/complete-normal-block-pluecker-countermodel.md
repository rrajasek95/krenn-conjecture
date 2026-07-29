# Complete pure normal blocks still miss the cofactor quotient

## Outcome

Coupling the distinguished all-`x` third-Schmidt channels across every
overlapping cut is still not enough.  There is an exact rational six-site
binary base `q_0`, a homogeneous one-`z` tangent `K`, and direct two-`z`
cells `W` such that

\[
 H(q_0)=2X+Y,
 \qquad dH_{q_0}(K)=0,                                   \tag{1}
\]

and, for **every** pair `i<j`,

\[
 [z_i z_jX_{B\setminus\{i,j\}}]
 \left(dH_{q_0}(W)+\frac12d^2H_{q_0}(K,K)\right)=\frac12. \tag{2}
\]

Consequently, across every cut `L | R`, the leading pure normal block with
rows `z_iX_{L-i}` and columns `z_jX_{R-j}` is

\[
                         \frac12\mathbf1_L\mathbf1_R^T.  \tag{3}
\]

It is exactly the complete-graph rank-one block of the half-shift target;
all its `2 by 2` Pluecker minors vanish.  Nevertheless the full second
collision equation fails.  The failure is visible only after retaining a
second binary component of a deleted-pair cofactor.

Thus a Grassmann identity on the scalar pair pattern cannot prove the
conjecture.  The minimal viable object is the pairwise **cofactor quotient**,
not the all-`x` entry of the normal block.

## 1. The coordinate-free pair equation

Let

\[
 C_{ij}=H_{B\setminus\{i,j\}}(q_0)
 \in\bigotimes_{v\ne i,j}\langle x_v,y_v\rangle.          \tag{4}
\]

Write the site pieces of the homogeneous tangent as `K=sum_i z_i k_i`.
The Hessian contribution in the `z_i z_j` sector is a binary complement
tensor `B_ij(k_i,k_j)`.  The complete second equation in that sector is

\[
             \eta_{ij}C_{ij}+B_{ij}(k_i,k_j)
                    =\frac12X_{B\setminus\{i,j\}}.        \tag{5}
\]

If `C_ij` is nonzero, eliminating the direct cell `eta_ij` gives the exact
coordinate-free condition

\[
 C_{ij}\wedge
 \left(\frac12X_{B\setminus\{i,j\}}-B_{ij}(k_i,k_j)\right)=0. \tag{6}
\]

For every pair, including `C_ij=0`, the uniform exact formulation is in the
varying quotient space

\[
 Q_{ij}=\left(\bigotimes_{v\ne i,j}\langle x_v,y_v\rangle\right)
             /\mathbb C C_{ij},                           \tag{7}
\]

the second fundamental form must take the prescribed target class:

\[
 \left[\frac12X_{B\setminus\{i,j\}}-B_{ij}(k_i,k_j)\right]=0
 \quad\hbox{in }Q_{ij}.                                   \tag{7a}
\]

When `C_ij=0`, this requires literal equality of the two tensors; the wedge
in (6) would be vacuous and must not be used as a replacement for (7a).

The scalar block (3) applies only the all-`x` coordinate functional to
(5).  It forgets every other coordinate of (6), including the ratio in
which one direct `W_ij` cell contributes to different complement
colorings.

## 2. Exact dense rational base

Split the sites into `A=01`, `B=23`, `C=45`.  Put unit `yy` cells on the
three block edges.  The `xx` matrices on the three cross-blocks are

\[
 X_{AB}=\begin{pmatrix}-2/25&2/25\\-3/25&-3/25\end{pmatrix},
\quad
 X_{AC}=\begin{pmatrix}-1&-3\\1&-3\end{pmatrix},
\quad
 X_{BC}=\begin{pmatrix}1&1\\3&-3\end{pmatrix}.            \tag{8}
\]

Each displayed matrix has permanent zero.  Therefore every mixed binary
coefficient vanishes, while direct expansion gives all-`x` coefficient two
and all-`y` coefficient one.  Hence the first identity in (1) holds.

The tangent has only `zx` and `xz` cells on these twelve cross-block
edges.  In the table, the last two columns are respectively the
coefficients of `z_u x_v` and `x_u z_v` on edge `uv`:

\[
\begin{array}{c|rr@{\qquad}c|rr}
02&-1/25&8/525&03&1/25&21/200\\
04&1/3&8&05&1&-3/32\\
12&3/50&4/175&13&3/50&-63/400\\
14&3/4&-8&15&-9/4&-3/32\\
24&1&1/3&25&1&-3/4\\
34&-3/4&1&35&3/4&9/4
\end{array}                                                \tag{9}
\]

Expansion over all one-`z` colorings gives `dH_q0(K)=0`, the second
identity in (1).

Set the direct `zz` coefficients on `01,23,45` to zero and use

\[
\begin{array}{c|rr@{\qquad}c|rr}
02&-81/1400&&03&-77/200\\
04&31/4&&05&-269/192\\
12&-349/2100&&13&-299/1600\\
14&79/16&&15&-317/64\\
24&839/42&&25&587/224\\
34&223/48&&35&9037/512
\end{array}                                                \tag{10}
\]

for `eta_uv`.  Exact matching expansion proves all fifteen identities
(2), so (3) follows for all cuts at once.

## 3. The smallest missing complement wedge

Consider the pair `13`.  On the all-`x` complement coordinate, its direct
cofactor and Hessian entries are

\[
                  C_{13}^{X}=-4,
 \qquad           B_{13}^{X}=-\frac{99}{400}.             \tag{11}
\]

Thus `eta_13=-299/1600` makes

\[
                  \eta_{13}C_{13}^{X}+B_{13}^{X}=\frac12, \tag{12}
\]

as required by every pure normal block.

Now use the complement coloring

\[
                         x_0x_2y_4y_5.                    \tag{13}
\]

For the full coloring `x_0z_1x_2z_3y_4y_5`, the corresponding entries are

\[
                  C_{13}^{M}=-\frac2{25},
 \qquad           B_{13}^{M}=\frac{63}{10000}.            \tag{14}
\]

The target coefficient is zero, but (10) gives

\[
             \eta_{13}C_{13}^{M}+B_{13}^{M}
                         =\frac{17}{800}\ne0.             \tag{15}
\]

Equivalently, the two-coordinate minor of (6) is

\[
 C_{13}^{X}(-B_{13}^{M})
 -C_{13}^{M}\left(\frac12-B_{13}^{X}\right)
                         =\frac{17}{200}\ne0.             \tag{16}
\]

This is the complement coupling erased by (3).  The verifier finds exactly
twelve failed mixed components, although every pure pair channel is right.

## 4. Scope of a Pluecker refinement

If every site kernel is a line and each quotient equation (7a) reduces to
one nonzero scalar condition, choosing temporary kernel bases gives

\[
                              t_it_j=c_{ij}.               \tag{17}
\]

Then the overlap tetrads

\[
                      c_{ij}c_{kl}-c_{ik}c_{jl}=0          \tag{18}
\]

are coordinate-independent up to a common nonzero scale.  This is the
valid mechanism in the generic dense-diagonal theorem.

For an arbitrary binary fiber, however, the spaces `ker F_i` can have
dimension larger than one and (7a) can give several independent bilinear
forms.  The target classes also live in different quotient spaces `Q_ij`;
there is no canonical product between them.  Hence (18) is not a universal
identity before proving an additional line-kernel/decomposability lemma.

The exact lesson from (8)--(16) is sharper than the earlier one-channel
multiplicity countermodel:

* even the complete rank-one scalar pair pattern on all overlapping cuts
  can be faked;
* one must first impose the full cofactor quotient equations (7a), using
  the wedges (6) on nonzero-cofactor pairs;
* only after those wedges reduce to vertex-factorized scalar equations may
  Pluecker tetrads be invoked.

[`verify_complete_normal_block_countermodel.py`](../computations/verify_complete_normal_block_countermodel.py)
checks (1)--(16), every cut matrix (3), and all 240 two-`z` complement
coefficients over the rationals.
