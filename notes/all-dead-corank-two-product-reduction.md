# The all-dead corank-two branch is an exact rank-two product problem

## 1. Outcome

Retain the two-deletion notation of
[`extra-hessian-corank-two-propagation.md`](extra-hessian-corank-two-propagation.md).
Thus `W` has `2r` sites, the rank-three graph of `q` is connected,
spanning, and nonbipartite, and

\[
 \mathcal H_q(p_cs_d)+a_{cd}Q=\delta_{cd}X_c.          \tag{1}
\]

Suppose that the excess Hessian quotient has dimension two and all six
star rows reach at least three sites.  Let `mathscr D` be the
four-dimensional relation space among the six off-diagonal quotient
classes.  If every rank-three edge is dead for this relation space, then
the gauge terms disappear completely:

\[
 \boxed{\quad
  \sum_{c\ne d}m_{cd}p_cs_d=0
  \quad\text{for every }M=(m_{cd})\in\mathscr D.
 \quad}                                                 \tag{2}
\]

Moreover, the six products in (2) span exactly a two-space `E`, every
two products in one colour row or one colour column form a basis of `E`,
and `mathscr D` is their exact kernel.  This is the precise global
content of the all-dead alternative.

The raw product statement is sharp.  There are rational three-site
examples in which all six rows reach three sites, the six off-diagonal
products have exactly this configuration, and all nine products span a
three-space.  Thus (2) alone is not a contradiction.

The nine cap equations impose a further sharp dimension requirement.  If

\[
 V=\operatorname {span}\{p_cs_d:0\le c,d\le2\},
 \qquad E=\operatorname {span}\{p_cs_d:c\ne d\},        \tag{3}
\]

then any solution of (1) must satisfy

\[
 \dim V\ge
 \begin{cases}
 5,&Q=0\text{ or }Q\notin\operatorname {span}(X_0,X_1,X_2),\\
 4,&0\ne Q\in\operatorname {span}(X_0,X_1,X_2).
 \end{cases}                                           \tag{4}
\]

Consequently every raw configuration with `dim V<=3` is excluded,
including the exact three-site model below.  The case `Q=0` is covered
separately and gives the stronger lower bound five.

Finally, the ordinary-lift analysis closes every intersection dimension.
The common-span case is handled intrinsically below; a one-dimensional
intersection is impossible; the disjoint case is excluded by the
irreducible-algebra argument in the companion product-geometry note; and
the full-support chart of the aligned two-plane reduces to two finite site
patterns, both excluded exactly.  The support-two and singular
zero-row/zero-column boundaries are excluded in
[`aligned-two-plane-boundary-closure.md`](aligned-two-plane-boundary-closure.md).
In particular, if the two star spans
coincide,

\[
 P:=\operatorname {span}(p_0,p_1,p_2)
   =\operatorname {span}(s_0,s_1,s_2)=:S,              \tag{5}
\]

then necessarily `dim V<=3`.  This remains true when the transition from
the `p` basis to the `s` basis is not diagonal.  Hence the common-span
all-dead branch cannot satisfy the cap equations.  Sections 8--9 exclude
the intersection-one case and the normalized full-support aligned chart;
the companion boundary note completes every remaining zero pattern.

## 2. Gauge removal on the all-dead graph

For `c!=d`, put

\[
 K_{cd}=p_cs_d+\lambda_{cd}q,
 \qquad \lambda_{cd}=a_{cd}/r.                         \tag{6}
\]

The classes `u_cd=[K_cd]` lie in the two-dimensional excess quotient.
Let

\[
 Z_0=\{M\in\operatorname {Mat}_3:M_{00}=M_{11}=M_{22}=0\},
 \qquad
 \mathscr D=\ker\left(M\longmapsto
                  \sum_{c\ne d}m_{cd}u_{cd}\right).  \tag{7}
\]

The row-column basis lemma gives

\[
 \dim\mathscr D=4,
 \qquad \mathscr D\cap R_c=\mathscr D\cap C_d=0.     \tag{8}
\]

For `M in mathscr D`, there are site weights `alpha_i`, of sum zero,
such that

\[
 \sum_{c\ne d}m_{cd}K_{cd}=Z^\alpha,
 \qquad (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij}.     \tag{9}
\]

Write

\[
 \lambda(M)=\sum_{c\ne d}m_{cd}\lambda_{cd}.
\]

On a site pair `ij`, equation (9) reads

\[
 \mathcal L_{ij}(M)
    =(\alpha_i+\alpha_j-\lambda(M))q_{ij},             \tag{10}
\]

where

\[
 \mathcal L_{ij}(M)=P_iMS_j^{\mathsf T}
                       +S_iM^{\mathsf T}P_j^{\mathsf T}.
\]

On every rank-three edge the all-dead hypothesis makes the left side of
(10) zero.  Hence

\[
                         \alpha_i+\alpha_j=\lambda(M)  \tag{11}
\]

on the connected nonbipartite rank-three graph.  Put
`beta_i=alpha_i-lambda(M)/2`.  Then `beta_i+beta_j=0` on every graph
edge.  Connectedness and an odd cycle give `beta_i=0` for every `i`.
Since `|W|=2r` and `sum_i alpha_i=0`,

\[
                  0=\sum_i\alpha_i=r\lambda(M).
\]

Characteristic zero gives `lambda(M)=0`, and hence `alpha=0`.
Substitution in (9) proves (2) on every site pair, not only on the
rank-three graph.

## 3. The physical product map has exact rank two

Define

\[
 B:Z_0\longrightarrow(\mathcal R_W)_2,
 \qquad B(M)=\sum_{c\ne d}m_{cd}p_cs_d.                \tag{12}
\]

Equation (2) gives `mathscr D subseteq ker B`, so `rank B<=2`.
We show that no colour row or column collapses.

Suppose, for distinct `d,e!=c`, that

\[
                 \mu p_cs_d+\nu p_cs_e=0              \tag{13}
\]

for a nonzero pair `(mu,nu)`.  Multiplication by a linear element which
reaches at least three sites is injective on linear elements.  Thus
`mu s_d+nu s_e=0`; both coefficients are nonzero and `s_e=t s_d` for
some `t!=0`.  Use the diagonal and off-diagonal pair equations in the
two corresponding rows:

\[
\begin{aligned}
 \mathcal H_q(p_ds_d)+a_{dd}Q&=X_d,&
 \mathcal H_q(p_ds_e)+a_{de}Q&=0,\\
 \mathcal H_q(p_es_d)+a_{ed}Q&=0,&
 \mathcal H_q(p_es_e)+a_{ee}Q&=X_e.
\end{aligned}                                          \tag{14}
\]

The proportionality puts both `X_d` and `X_e` in `C Q` (and makes them
zero if `Q=0`), contradicting their independence.  Therefore every row
pair in (12) is independent.  Interchanging the two stars proves the
same assertion for every column pair.  Consequently

\[
                 \operatorname {rank}B=2,
 \qquad          \ker B=\mathscr D.                   \tag{15}
\]

In particular `P` and `S` each have dimension at least two.  If either
has dimension two, every diagonal product is already a combination of
off-diagonal products, so `V=E`; equation (4) then gives an immediate
contradiction.  Any residual cap solution therefore has
`dim P=dim S=3`.

## 4. The cap-dimension obstruction, including `Q=0`

Every off-diagonal equation in (1) gives

\[
                         \mathcal H_q(E)\subseteq\mathbb C Q.        \tag{16}
\]

Thus `mathcal H_q|V` induces a map

\[
 \overline{\mathcal H}_q:V/E
       \longrightarrow (\mathcal R_W)_{2r}/\mathbb C Q.             \tag{17}
\]

The diagonal equations say that the three classes `[X_c]` belong to its
image.  Since the `X_c` are independent, their images modulo `C Q` span
a three-space when `Q=0` or `Q` is outside their span, and a two-space
when `Q` is a nonzero member of their span.  Since `dim E=2`, (4)
follows.

No division by `Q` occurs here.  In particular, on the base locus
`Q=0`, (16) says literally `H_q(E)=0`, while the three diagonal products
must supply three independent target directions.  Hence `dim V>=5`.

## 5. A sharp rational raw-product model

Take three one-dimensional active site lines and write a linear element
as a row in `C^3`.  Let the three *site colour columns* be

\[
 v_1=(1,2,3)^{\mathsf T},\qquad
 v_2=(1,1,-3)^{\mathsf T},\qquad
 v_3=(7,-8,-1)^{\mathsf T}.                            \tag{18}
\]

Equivalently, put `s_c=p_c` and

\[
 \begin{pmatrix}p_0\\p_1\\p_2\end{pmatrix}
   =\begin{pmatrix}
       1&1&7\\
       2&1&-8\\
       3&-3&-1
     \end{pmatrix}.                                    \tag{19}
\]

In the coordinates `(12,13,23)` of the square-free quadratic algebra,

\[
\begin{aligned}
 p_0p_1&=(3,6,-1),\\
 p_0p_2&=(0,20,-22),\\
 p_1p_2&=(-3,-26,23),
\end{aligned}
\qquad
                 p_0p_1+p_0p_2+p_1p_2=0.              \tag{20}
\]

Every two of these three vectors are independent.  The six directed
off-diagonal products therefore span a two-space with the row-column
basis property; their kernel is the three-dimensional skew space plus
the symmetric relation in (20).  All three rows reach all three active
sites.  The three squares enlarge the total product span to exactly
three.  Adding zero components at further sites embeds this model in
every allowed even `W` with at least four sites.

The columns in (18), rather than the rows in (19), are the vectors which
are mutually orthogonal for

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix};
 \qquad
 [v_1\ v_2\ v_3]^{\mathsf T}H[v_1\ v_2\ v_3]
       =\operatorname {diag}(22,-10,-110).             \tag{21}
\]

This explains (20) and fixes the otherwise easy row/column orientation
ambiguity.

## 6. The kernel of square-free multiplication on one subspace

We use one elementary lemma.  Let

\[
 L=\bigoplus_iV_i,
 \qquad \pi:\operatorname {Sym}^2L\longrightarrow(\mathcal R_W)_2
\]

delete the same-site blocks, and let `U subseteq L`.  Then

\[
 \boxed{\quad
 \ker(\pi|_{\operatorname {Sym}^2U})
      =\bigoplus_i\operatorname {Sym}^2(U\cap V_i).
 \quad}                                                 \tag{22}
\]

Indeed, regard a symmetric tensor as a symmetric map `L^* to L`.  If it
lies in `Sym^2 U`, its image lies in `U`.  If it has only same-site
blocks, its `i`-th block has image in both `V_i` and `U`, hence in
`U intersection V_i`.  The reverse inclusion is immediate.

Write `d_i=dim(U intersection V_i)`.  Consequently

\[
 \dim\ker(\pi|_{\operatorname {Sym}^2U})
       =\sum_i {d_i+1\choose2}.                         \tag{23}
\]

If this kernel contains a nondegenerate quadratic tensor on a
three-space `U`, its image is all of `U`; the block decomposition then
gives

\[
                         U=\bigoplus_i(U\cap V_i).      \tag{24}
\]

If each member of a basis of `U` reaches at least three sites, (24)
has at least three nonzero summands.  Since `dim U=3`, it has exactly
three one-dimensional summands.  Equations (22)--(23) then make the
square-free image of `Sym^2 U` three-dimensional.

## 7. Common star span forces total rank at most three

**Theorem 7.1 (common-span product collapse).**  Suppose (15) holds,
all six rows reach at least three sites, and `P=S` as subspaces of
`(mathcal R_W)_1`.  Then

\[
 \dim\operatorname {span}\{p_cs_d:0\le c,d\le2\}\le3.              \tag{25}
\]

**Proof.**  Let

\[
 \mu:\operatorname {Sym}^2P\longrightarrow(\mathcal R_W)_2,
 \qquad \mathcal W=\operatorname {im}\mu,
 \qquad t=\dim\mathcal W.                             \tag{26}
\]

The products of the two bases span `mathcal W`, so the left side of
(25) is `t`.  Suppose for contradiction that `t>=4`.  The annihilator of
the off-diagonal product plane is

\[
 \mathcal A=\{H\in\mathcal W^*:H(E)=0\},
 \qquad \dim\mathcal A=t-2\ge2.                       \tag{27}
\]

Pull a functional back through `mu` and regard it as a symmetric
bilinear form on `P`.  In the `p` and `s` bases its cross matrix is
diagonal:

\[
                         H(p_c,s_d)=d_c(H)\delta_{cd}. \tag{28}
\]

The map `H mapsto d(H)` is injective, since the nine products of two
bases span `Sym^2 P` before applying `mu`.

First, `mathcal A` contains a nondegenerate form.  Otherwise its
at-least-two-dimensional space of diagonal vectors lies in
`{d_0d_1d_2=0}`.  A linear space over `C` contained in this union of
three coordinate hyperplanes lies in one of them, say `d_c=0`.
Then every member of `mathcal A` annihilates `p_cS`, so double
annihilation inside `mathcal W` gives

\[
                         \mu(p_cS)\subseteq E.          \tag{29}
\]

Multiplication by the at-least-three-site element `p_c` is injective on
linear elements.  The left side of (29) has dimension three, whereas
`E` has dimension two, a contradiction.

Write `s=pC` for an invertible transition matrix `C` and put
`T=C^{-1}`.  In the `p` basis the symmetric matrix of (28) is

\[
                         D T,
 \qquad D=\operatorname {diag}(d_0,d_1,d_2).
\]

Symmetry is exactly

\[
                         d_iT_{ij}=d_jT_{ji}\quad(i\ne j).           \tag{30}
\]

Choose the nondegenerate member above, whose three `d_i` are nonzero.
It follows that `T_ij` is nonzero exactly when `T_ji` is nonzero.  Make
an undirected graph on the three colours from these nonzero pairs.  On
each graph edge, (30) fixes the ratio `d_i/d_j` for every `d` arising
from `mathcal A`.  The graph cannot be connected, since then the space
of such `d` would be one-dimensional.  After a colour permutation there
are two cases.

If the graph has no edges, `C` is diagonal.  The six directed
off-diagonal products are nonzero scalar multiples of the three
unordered products

\[
                         p_0p_1,quad p_0p_2,quad p_1p_2.             \tag{31}
\]

They span the two-space `E`, and every pair in (31) is independent.
Their unique relation therefore has all three coefficients nonzero.
As a symmetric quadratic tensor on `P`, it is represented by an
invertible zero-diagonal `3 by 3` matrix.  It belongs to the kernel in
(22), so (24) and the support hypothesis make `t=3`, a contradiction.

It remains that the graph has one edge, say `01`, and isolated vertex
`2`.  Equation (30) then has a two-dimensional solution space.  Thus
`dim mathcal A=2`, `t=4`, and (22) has dimension `6-t=2`.  The diagonal
vector `(0,0,1)` satisfies (30); its form is a nonzero rank-one square
`ell^2`, with

\[
                         \ker\ell=\operatorname {span}(p_0,p_1).    \tag{32}
\]

Every pulled-back functional in `mathcal W^*` annihilates the kernel of
`mu`.  Hence `ell^2` annihilates every
`Sym^2(P intersection V_i)`, and therefore

\[
                         P\cap V_i\subseteq\ker\ell\quad\text{for all }i.
                                                               \tag{33}
\]

By (23), a two-dimensional kernel consists of exactly two
one-dimensional site summands.  They are independent, lie in the plane
(32), and hence span it.  Both `p_0` and `p_1` are supported on those
two sites, contradicting the support hypothesis.  The one-edge case is
also impossible.  Therefore `t<=3`, proving (25). `QED`

Combining Theorem 7.1 with (4) excludes the common-span all-dead branch
for every value of `Q`, including `Q=0` and the exceptional possibility
that a nonzero `Q` lies in the pure-target three-space.

## 8. A one-dimensional star intersection is impossible

The same ordinary lift excludes another whole branch.

**Lemma 8.1 (a regular four-plane contains a unit).**  Let
`D subset Mat_3(C)` have dimension four.  If, for every nonzero `w`,

\[
 \operatorname {rank}(M\mapsto Mw)\ge2,
 \qquad
 \operatorname {rank}(M\mapsto M^{\mathsf T}w)\ge2,   \tag{35}
\]

then `D` contains an invertible matrix.

**Proof.**  Suppose every member is singular.  The space contains a
rank-two matrix: otherwise two rank-one matrices with independent left
and right factors would have rank two, while sharing one factor confines
the whole space to dimension at most three.  Normalize a rank-two member
to

\[
                         A=\operatorname {diag}(1,1,0).
\]

Write every other member as

\[
 M=\begin{pmatrix}M_0&u\\v^{\mathsf T}&m\end{pmatrix}.
\]

The coefficient of the parameter in `det(A+tM)=0` gives `m=0`.
Polarizing the quadratic coefficient gives

\[
                         v_M^{\mathsf T}u_N+v_N^{\mathsf T}u_M=0
                         \quad(M,N\in D).              \tag{36}
\]

If the `u_M` span at most a line, evaluation at the last coordinate has
rank at most one; the same holds on the transpose side if the `v_M` span
at most a line.  Thus both would have to span `C^2`.  The image of
`M mapsto (u_M,v_M)` is then a maximal isotropic plane for the
nondegenerate split form in (36).  It is the graph

\[
                         v=Ju
\]

of an invertible alternating `2 by 2` matrix `J`.  Its kernel in `D` has
dimension at least two.  For a member `N` of this kernel, polarizing the
cubic coefficient of `det(A+sM+tN)` gives

\[
                         u^{\mathsf T}J^{\mathsf T}
                           \operatorname {adj}(N_0)u=0
                         \quad\text{for all }u\in\mathbb C^2.        \tag{37}
\]

Hence `J^T adj(N_0)` is alternating.  In `2 by 2` coordinates this says
that `N_0` is a scalar matrix.  The kernel in `D` would therefore have
dimension at most one, a contradiction.  Thus one of the two evaluation
maps violates (35), proving the lemma. `QED`

**Theorem 8.2 (intersection-one exclusion).**  Under (15) and the
six dense-row hypotheses,

\[
                         \dim(P\cap S)\ne1.             \tag{38}
\]

**Proof.**  Suppose `dim(P intersection S)=1` and put `U=P+S`, so
`dim U=5`.  Ordinary symmetrization

\[
 \theta:P\otimes S\longrightarrow\operatorname {Sym}^2U,
 \qquad p\otimes s\longmapsto p\mathbin\odot s        \tag{39}
\]

is injective: its kernel is
`wedge^2(P intersection S)=0`.  For `M in mathscr D`, the tensor

\[
                         B_M=PMS^{\mathsf T}+SM^{\mathsf T}P^{\mathsf T}
                                                               \tag{40}
\]

has only same-site blocks by (2).

We first choose `M_0 in mathscr D` for which `B_0=B_(M_0)` is
nondegenerate on `U`.  Lemma 8.1 applies to `mathscr D` by the evaluation
lemma for row-column-avoiding four-planes.  There is therefore an
`M in mathscr D` with `det M!=0`.

Choose coefficient bases adapted to the common line and write

\[
 M=\begin{pmatrix}a&b\\c&D\end{pmatrix},
 \qquad D\in\operatorname {Mat}_2.
\]

In the corresponding decomposition
`U=(P intersection S) direct-sum P' direct-sum S'`, direct calculation
gives

\[
 \det B_M=2\det(M)\det(D).                             \tag{41}
\]

The polynomial `det(D)` is not identically zero on `mathscr D`.
Otherwise its two-by-two compression image would be a linear space of
singular `2 by 2` matrices.  Such a space has a common right kernel or a
common left kernel.  In the first case some nonzero coefficient vector
`w` has `Mw` confined to the one-dimensional coefficient line of
`P intersection S` for every `M`; in the second case the transpose
version holds.  Either conclusion contradicts the two-regular evaluation
property (35).  Since neither factor on the right of (41) vanishes
identically on the four-space, their product does not vanish identically.
This supplies `M_0`.

Because `B_0` is nondegenerate and block diagonal by sites, (22) applied
to its image gives

\[
                         U=\bigoplus_i(U\cap V_i).      \tag{42}
\]

Every `B_M` is block diagonal for the same decomposition.  Thus the
endomorphisms

\[
                         A_M=B_MB_0^{-1}\in\operatorname {End}(U)   \tag{43}
\]

preserve every summand in (42).  Dense support requires at least three
nonzero site summands.  A partition of five into at least three positive
parts has a one-dimensional part; let `C u` be such a common invariant
line.  Put `phi=B_0^{-1}u in U^*`.  There is a linear functional
`lambda` on `mathscr D` such that

\[
                         B_M\phi=\lambda(M)B_0\phi.     \tag{44}
\]

Set `a=P^T phi` and `b=S^T phi`.  On the three-plane
`mathscr D'=ker lambda`, equation (44) becomes

\[
                         PMb+SM^{\mathsf T}a=0.         \tag{45}
\]

Neither `a` nor `b` is zero, by (35).  Cancellation in (45) takes place
in the one-dimensional intersection `P intersection S`.  Hence the map

\[
                         \mathscr D'\longrightarrow
                         (Mb,M^{\mathsf T}a)             \tag{46}
\]

has rank at most one.  Its kernel has dimension at least two.  Every
matrix in that kernel has right kernel containing `b` and left kernel
containing `a`; it is therefore a `2 by 2` matrix after fixed row and
column quotients.  A two-dimensional pencil of `2 by 2` matrices over
`C` contains a nonzero singular member, so `mathscr D` contains a
rank-one matrix.

Finally, a rank-one zero-diagonal matrix is `xy^T` with
`x_cy_c=0` for all three `c`.  The nonempty supports of `x` and `y` are
disjoint, so one has size one.  The matrix is contained in a single
coordinate row plane or coordinate column plane, contrary to (8).
This proves (38). `QED`

Thus the all-dead product boundary has now narrowed further to

\[
                         \dim(P\cap S)\in\{0,2\}.       \tag{47}
\]

## 9. The full-support aligned two-plane has only two site patterns

The disjoint case can be excluded by the irreducible-algebra argument in
[`all-dead-corank-two-product-geometry.md`](all-dead-corank-two-product-geometry.md).
We record here a reduction and one exact exclusion on the remaining
aligned two-plane.

On its full-support chart, diagonal rescaling puts the intrinsic ordinary
relation into the normal form

\[
                         s_c=p_c+v_ct,
 \qquad v_0v_1v_2\ne0,
 \qquad U=P+\mathbb Ct.                                \tag{48}
\]

Rescaling each pair `(p_c,s_c)` lets us take `v=(1,1,1)` without
changing supports or any product ranks.

For `M in mathscr D`, its ordinary lift `B_M` has only same-site blocks.
Put

\[
                         L_0=\bigoplus_i(U\cap V_i).    \tag{49}
\]

Every `B_M` has image in `L_0`.  In fact

\[
                         L_0=U.                         \tag{50}
\]

Otherwise choose a nonzero `x in U^*` annihilating `L_0`, and put
`a=P^T x`, `b=S^T x`.  Then

\[
                         P(Mb)+S(M^{\mathsf T}a)=B_Mx=0
                         \quad(M\in\mathscr D).         \tag{51}
\]

Neither `a` nor `b` vanishes, by two-regularity.  The image of
`M mapsto (Mb,M^T a)` lies in the two-dimensional anti-diagonal copy of
`P intersection S` inside the kernel of `P direct-sum S to U`.  Its
kernel in the four-plane `mathscr D` has dimension at least two and
consists of matrices with the fixed right kernel `b` and fixed left
kernel `a`.  As in Theorem 8.2, this two-dimensional `2 by 2` pencil
contains a nonzero rank-one matrix, contradicting row-column avoidance.
This proves (50).

The site summands in (50) have total dimension four.  Dense support
requires at least three nonzero sites, so only

\[
                         1+1+1+1
 \qquad\text{or}\qquad 2+1+1                         \tag{52}
\]

can occur.

**Proposition 9.1 (four-line exclusion).**  The `1+1+1+1` alternative
in (52) is incompatible with all six rows reaching three sites.

**Proof.**  Choose nonzero site vectors `u_i`, `0<=i<=3`, and write
their coordinates in the basis `(p_0,p_1,p_2,t)` as

\[
                         u_i=(a_{i0},a_{i1},a_{i2},\tau_i).
\]

The resulting `4 by 4` matrix is invertible.  A symmetric form on `U`
annihilates every off-diagonal product precisely when it has the shape

\[
 G(d,\lambda,z)=
 \begin{pmatrix}
  D-\lambda\mathbf1\mathbf1^{\mathsf T}&\lambda\mathbf1\\
  \lambda\mathbf1^{\mathsf T}&z
 \end{pmatrix},
 \qquad D=\operatorname {diag}(d_0,d_1,d_2),            \tag{53}
\]

and also has zero square on each site line.  The space in (53) has
dimension five.  The square-free quadratic space on four lines has
dimension six, while the off-diagonal products span exactly two;
therefore four independent forms of shape (53) vanish on the four site
lines.  Equivalently, the four rows

\[
 \left(
  a_{i0}^2,a_{i1}^2,a_{i2}^2,
  -w_i^2+2\tau_iw_i,\tau_i^2
 \right),
 \qquad w_i=a_{i0}+a_{i1}+a_{i2},                      \tag{54}
\]

span a line.

None of the rows in (54) is zero.  After rescaling each `u_i`, there are
nonzero `A_0,A_1,A_2,T` and signs `epsilon_ic in {+1,-1}` such that

\[
 u_i=(\epsilon_{i0}A_0,\epsilon_{i1}A_1,
       \epsilon_{i2}A_2,T).                            \tag{55}
\]

Thus the first three signs form four affinely independent vertices of
the sign cube.  The fourth coordinate in (54) says

\[
                         (w_i-T)^2\quad\text{is independent of }i.  \tag{56}
\]

We use the following elementary cube calculation.  Up to signed
coordinate permutations, the affine tetrahedra in `{+1,-1}^3` have the
four representatives in the first column below.  Factoring (56) as
`w_i-w_0=0` or `w_i+w_0=2T` gives the remaining columns.

| sign vertices (rows) | nonzero solution ratios `(A_0,A_1,A_2,T)` | forced site supports |
|---|---:|---:|
| `---,--+,-+-,+--` | `(-1/2,-1/2,-1/2,1)` | all three `p_c`: 2 |
| `---,--+,-+-,+-+` | none | impossible |
| `---,--+,-+-,+++` | `(-2,1,1,1)` | two `p_c` and two `s_c`: 2 |
| `---,-++,+-+,++-` | four signed variants of `(1,1,-1,1)` | all three `s_c`: 2 |

For clarity, the support entries follow by inverting

\[
 X=S\operatorname {diag}(A_0,A_1,A_2,T),              \tag{57}
\]

where the rows of `S` are the four augmented sign vertices.  The site
coordinates of `p_c` are row `c` of `X^{-1}`, and those of
`s_c=p_c+t` are the sum of rows `c` and `3`.  The four representatives
are exhaustive because the 58 affine tetrahedra form four orbits under
the signed permutation group.  Every possible row in the last column
violates the three-site support hypothesis.  This proves the
proposition. `QED`

It remains to exclude the `2+1+1` site decomposition.

**Proposition 9.2 (fat-plane exclusion).**  The `2+1+1` alternative in
(52) is also incompatible with all six rows reaching three sites.

**Proof.**  Work in the basis `(p_0,p_1,p_2,t)` of `U` and introduce
five linear forms

\[
 \ell_0=x_0,\quad \ell_1=x_1,\quad \ell_2=x_2,\quad
 \ell_3=x_0+x_1+x_2-x_3,\quad \ell_4=x_3.              \tag{58}
\]

They span `U^*` and have the unique circuit

\[
                 \ell_0+\ell_1+\ell_2-\ell_3-\ell_4=0.              \tag{59}
\]

The five-dimensional form space (53) is equivalently

\[
                         \operatorname {span}\{\ell_0^2,\ldots,
                                                   \ell_4^2\}.       \tag{60}
\]

Indeed its last two basis forms can be taken as
`(x_0+x_1+x_2-x_3)^2` and `x_3^2`.

Let `L` be the two-dimensional site summand and let `Ca,Cb` be the two
site lines.  The physical square-free quadratic space has dimension

\[
                         2\cdot1+2\cdot1+1\cdot1=5.    \tag{61}
\]

Its off-diagonal product subspace `E` has dimension two.  Therefore the
forms in (60) which vanish on `Sym^2 L`, `a^2`, and `b^2` form a
three-space.  Equivalently, the joint restriction map

\[
 \operatorname {span}\{\ell_j^2\}_{j=0}^4
       \longrightarrow \operatorname {Sym}^2L^*\oplus\mathbb C\oplus\mathbb C
                                                               \tag{62}
\]

has rank two.

In particular the five squares `(ell_j|L)^2` span at most a two-space.
Since the `ell_j` span `U^*`, their restrictions span `L^*`; there are
at least two nonproportional nonzero restrictions.  Two such squares are
independent, so the restriction to `Sym^2 L` already has rank two.
Consequently the two outside-line evaluation rows lie in that same
two-dimensional row space.  Three distinct squares of linear forms on a
two-plane are independent: in affine slope coordinates their coefficient
determinant is the Vandermonde determinant.  Hence the nonzero
restrictions `ell_j|L` occupy exactly two projective classes.  None can be
zero.  If
`ell_j|L=0`, then the `j`-th coordinate of every square vector in the
image of `Sym^2 L` is zero.  By (62), `ell_j(a)^2=ell_j(b)^2=0` as well,
so `ell_j` vanishes on `L+Ca+Cb=U`, impossible.

There are therefore exactly two nonempty projective classes.  Neither
can be a singleton: the kernel of restriction from the five named forms
to `L^*` consists of the within-class relations, while the global circuit
(59) has a nonzero coefficient on every form.  Thus the class sizes are

\[
                              2+3.                     \tag{63}
\]

Put `c=(1,1,1,-1,-1)`, the coefficient vector in (59), and let `A` be
the two-element class.  After scaling the two class generators, the
image of `L` in the circuit hyperplane of `C^5` has a basis

\[
 y_A=(k_j)_{j\in A},\qquad y_B=(l_j)_{j\notin A},       \tag{64}
\]

extended by zero off the indicated supports, where

\[
 \sum_{j\in A}c_jk_j=0,\qquad
 \sum_{j\notin A}c_jl_j=0,                             \tag{65}
\]

and every displayed coefficient is nonzero.

Equation (62) also says that the coordinatewise square vector of either
outside line belongs to the span of the coordinatewise squares of `y_A`
and `y_B`.  Thus its five
coordinates are independent sign twists of scalar multiples of the
entries in (64), subject only to the circuit (59).  The symmetry group
`S_3 x S_2` permutes the first three and last two circuit coordinates.
On the six named vectors it respectively permutes colours and exchanges
the two stars, so it preserves the dense-support question.  There are
only three orbits for the pair `A`: positive-positive (`PP`),
positive-negative (`PN`), and negative-negative (`NN`).

Normalize the triple coefficients in (65) with a parameter
`t` outside `{0,-1}`.  The following table lists a basis `(y_A,y_B)` for
`L` and all projectively distinct outside sign-twist lines.  Overall
nonzero factors are suppressed.

| type | `(y_A,y_B)` | possible outside lines |
|---|---|---|
| `PP` | `( (1,-1,0,0,0), (0,0,t+1,1,t) )` | `(t,t,-t-1,-1,t)`, `(1,1,-t-1,1,-t)`, `(t+1,t+1,-t-1,1,t)` |
| `PN` | `( (-1,0,0,-1,0), (0,1,t,0,t+1) )` | `(-t-1,1,t,t+1,-t-1)`, `(t,1,-t,-t,t+1)`, `(-1,1,-t,1,-t-1)`, `(t+1,-1,-t,-t-1,t+1)` |
| `NN` | `( (0,0,0,-1,1), (1,t,-t-1,0,0) )` | `(-1,-t,-t-1,-t-1,-t-1)`, `(-1,t,t+1,t,t)`, `(-1,t,-t-1,-1,-1)` |

This table follows directly by writing an outside vector as independent
signed scalar multiples of `y_A` on `A` and `y_B` off `A`, and imposing
(59).

For completeness, invert every pair of candidate outside lines together
with `(y_A,y_B)`.  A pair which does not span the circuit hyperplane is
marked `--`; otherwise the last column lists named global vectors whose
coordinate on one site summand vanishes.  Such a vector reaches at most
the fat site and one line, hence at most two sites.

| type | outside pair | forced at-most-two-site rows |
|---|---:|---|
| `PP` | `12` | `p_0,p_1,s_0,s_1` |
|  | `13` | `s_0,s_1` |
|  | `23` | `p_0,p_1` |
| `PN` | `12` | `p_0,p_2,s_0` |
|  | `13` | `p_0,p_1,s_0` |
|  | `14` | `--` |
|  | `23` | `p_0,p_1,p_2` |
|  | `24` | `p_0,p_2,s_0` |
|  | `34` | `p_0,p_1,s_0` |
| `NN` | `12` | `p_1,p_2,s_1,s_2` |
|  | `13` | `p_0,p_2,s_0,s_2` |
|  | `23` | `p_0,p_1,s_0,s_1` |

Here the six global vectors in the circuit hyperplane are especially
simple:

\[
                         p_c=e_c+e_3,
 \qquad                  s_c=e_c+e_4\qquad(0\le c\le2).             \tag{66}
\]

All nonzero four-by-four determinants in the inversion table are
`+/-4t(t+1)`, so no specialization allowed by (65) is lost.
Every spanning choice contradicts the dense-row hypothesis.  This proves
the proposition. `QED`

Propositions 9.1 and 9.2 exclude the normalized full-support chart of the
aligned two-plane.  The support-two regular chart and the singular
normalization boundary, where the intrinsic relation has both a zero row
and a zero column, are excluded in
[`aligned-two-plane-boundary-closure.md`](aligned-two-plane-boundary-closure.md).

## 10. Exact audit and precise boundary

The companion script
[`verify_all_dead_corank_two_product_reduction.py`](../computations/verify_all_dead_corank_two_product_reduction.py)
checks the orientation and every rank assertion in the rational model,
the four-dimensional row-column-avoiding relation space, the asymmetric
three-site model recorded during the search, the cap quotient dimensions,
the determinant/transition identities used in Theorem 7.1, the four
exact cube-tetrahedron orbits in Proposition 9.1, and every symbolic
PP/PN/NN inversion-table identity in Proposition 9.2.

Together with the boundary verifier
[`verify_aligned_two_plane_boundaries.py`](../computations/verify_aligned_two_plane_boundaries.py),
this closes the all-dead geometry: it is either impossible under the six
dense-row hypotheses or has `dim V<=3`, while the cap equations require
(4).  The cap obstruction itself treats every value and target position
of `Q`, including `Q=0`.
