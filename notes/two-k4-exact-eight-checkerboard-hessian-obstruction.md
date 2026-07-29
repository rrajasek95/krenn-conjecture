# The exact-eight checkerboard Hessian obstruction

> **Status.**  Complete.  Sections 4.1--4.5 prove the common-site incidence
> assertion, including the residual transverse line--line branch.  Together
> with the exact support census, this proves the exact-eight obstruction.

## 1. Result

Work in the two-`K_4` chart and write `B_ij` for the `3 by 3` cross
block from left site `i` to right site `j`.  The exact-seven analysis
already shows that at least eight of the sixteen blocks are singular.
This note records the reduction of the exact-eight stratum.

The main local input is the following disjoint two-plus-two erasure
calculation.  Each of two stars has two regular components and two
arbitrary singular components, with the two exceptional pairs disjoint.
Erasing the eight input cells outside one cell leaves only the visibly
invisible opposite-edge blocks.

The second local input concerns exceptional pairs meeting in one site.
Full injectivity is false in that case.  The replacement needed by the
two-`K_4` application is that every erased-Hessian kernel vector vanishes
on the three edges incident with the common exceptional site.  Section 4.5
closes the final transverse line--line branch.

The resulting exact support census gives

\[
 \boxed{\#\{(i,j):\det B_{ij}=0\}\geq 9}.               \tag{1}
\]

The exact audit is
[`verify_two_k4_exact_eight_checkerboard_hessian.py`](../computations/verify_two_k4_exact_eight_checkerboard_hessian.py).

## 2. The square-free Hessian

Let

\[
 \mathcal R=\bigotimes_{i=0}^3(\mathbb F\oplus V_i),
 \qquad V_i^2=0,\qquad \dim V_i=3,                     \tag{2}
\]

over a characteristic-zero field.  Let `U,W` be three-spaces, let

\[
 p_x=\sum_iP_ix,\qquad s_y=\sum_iS_iy,                 \tag{3}
\]

and let `q in R_2`.  Fix nonzero covectors `ell in U*` and `m in W*`,
and put

\[
 K=\ker\ell,\qquad L=\ker m.                           \tag{4}
\]

The eight-cell erasure condition is

\[
 q p_xs_y=0\qquad\text{if }x\in K\text{ or }y\in L.   \tag{5}
\]

Equivalently, the bilinear tensor `(x,y) mapsto q p_xs_y` is a multiple
of `ell tensor m`.  Thus (5) is intrinsic: the notation “erase every
`(x,y)!=(e_0,e_0)`” only chooses complements to the two planes.

## 3. Disjoint two-plus-two erasure

Split the sites into

\[
 H=\{0,1\},\qquad R=\{2,3\}.                            \tag{6}
\]

Assume

\[
 \begin{array}{c|cc|cc}
       &0&1&2&3\\ \hline
 P_i&\text{singular}&\text{singular}&\text{invertible}&\text{invertible}\\
 S_i&\text{invertible}&\text{invertible}&\text{singular}&\text{singular}.
 \end{array}                                           \tag{7}
\]

Zero maps are allowed among the four singular components.

**Lemma 3.1 (disjoint two-plus-two erasure).**  The kernel of (5) is

\[
 \ker\beta=
 \begin{cases}
  0,&(P_0,P_1)\ne(0,0),\ (S_2,S_3)\ne(0,0),\\
  \mathcal R_{23},&(P_0,P_1)=(0,0),\ (S_2,S_3)\ne(0,0),\\
  \mathcal R_{01},&(P_0,P_1)\ne(0,0),\ (S_2,S_3)=(0,0),\\
  \mathcal R_{01}\oplus\mathcal R_{23},
       &(P_0,P_1)=(0,0),\ (S_2,S_3)=(0,0).
 \end{cases}                                           \tag{8}
\]

Here `R_ij=V_i tensor V_j`; consequently the four kernel dimensions are
`0,9,9,18`.  The two nonzero spaces in (8) are literal edge-block spaces,
not graphs of maps into the other four blocks.

### 3.1 Invariant coefficient reduction

Only the four isomorphisms in (7) are normalized.  Use `S_0,S_1` to
identify `V_0,V_1` with `W`, and use `P_2,P_3` to identify `V_2,V_3`
with `U`.  The four exceptional maps remain completely arbitrary:

\[
 A=S_0^{-1}P_0,\qquad B=S_1^{-1}P_1,\qquad
 C=P_2^{-1}S_2,\qquad D=P_3^{-1}S_3.                  \tag{9}
\]

In particular, no two singular maps have been diagonalized or put in
simultaneous normal form.  With tensor factors kept in site order, the
six complementary responses multiplying the six blocks of `q` are

\[
\begin{array}{c|l}
q_{01}&x\otimes Dy+Cy\otimes x\\
q_{02}&Bx\otimes Dy+y\otimes x\\
q_{03}&Bx\otimes Cy+y\otimes x\\
q_{12}&Ax\otimes Dy+y\otimes x\\
q_{13}&Ax\otimes Cy+y\otimes x\\
q_{23}&Ax\otimes y+y\otimes Bx.
\end{array}                                            \tag{10}
\]

Formula (10), followed by coefficient comparison modulo the single input
line `F(ell tensor m)`, is the whole calculation.  We record the
basis-free elimination because zero and nonzero singular maps must not be
conflated.

For an exceptional map `T`, filter the corresponding local dual space by
the intrinsic subspace `ker(T^*)`.  Apply these four filtrations to the
top-output dual, and compare successively the coefficients on

\[
 K\otimes L,qquad K\otimes (W/L),qquad
 (U/K)\otimes L.                                       \tag{11}
\]

The associated-graded pivots are

\[
\begin{array}{c|c|c}
\text{blocks being eliminated}&\text{pivot response}&\text{survivor}\\ \hline
02,03,12,13&S_hy\otimes P_rx&0\\
01&(C,D)&\mathcal R_{01}\text{ iff }C=D=0\\
23&(A,B)&\mathcal R_{23}\text{ iff }A=B=0.
\end{array}                                            \tag{12}
\]

More explicitly, after the four regular-cross blocks have been removed,
the remaining coefficient sequence is exact:

\[
0\longrightarrow\ker\beta\longrightarrow
 \mathcal R_{01}\oplus\mathcal R_{23}
 \xrightarrow{\ d\ }
 \begin{aligned}
 &\bigl(\mathcal R_{01}\otimes
       (\operatorname {Hom}(W,U)\oplus\operatorname {Hom}(W,U))\bigr)\\
 &\quad\oplus
 \bigl(\mathcal R_{23}\otimes
       (\operatorname {Hom}(U,W)\oplus\operatorname {Hom}(U,W))\bigr),
 \end{aligned}                                         \tag{13}
\]

where

\[
 d(Q,R)=\bigl((Q\otimes C,Q\otimes D),
               (R\otimes A,R\otimes B)\bigr).
\]

Tensoring a nonzero vector with a nonzero linear map is nonzero.  Hence
the first part of `d` has kernel `R_01` exactly when `C=D=0`, and the
second has kernel `R_23` exactly when `A=B=0`.  Thus (13) gives (8).

For completeness, there is one small point hidden by associated-graded
notation.  If the chosen nonzero coefficient of (say) `A` vanishes on
`K`, the six cells `K times W` can leave the usual two-plane Koszul
bridge.  Choose `x_0` outside `K` with `Ax_0!=0`.  After the earlier
pivots have been subtracted, the bridge coefficient on
`x_0 times L` is a tensor product of `Ax_0`, a freely varying vector
through one of the regular `S`-maps, and a nonzero alternating two-plane
coefficient.  It cannot vanish for every `y in L`.  The symmetric
argument applies when a nonzero coefficient of `C` or `D` vanishes on
`L`.  These are precisely the last pivots in (11).

In invariant shorthand, the detected coefficient has the form

\[
             (Ax_0)\otimes(S_hy)\otimes\Omega_K\ne0    \tag{14}
\]

for a regular site `h` and a nonzero Koszul boundary `Omega_K`; no
coordinate position of the nonzero entry of `A` is being prescribed.
All other entries of `A,B,C,D` occur above an already nonzero pivot and
are removed by back-substitution.  Hence the calculation depends only on
whether each exceptional pair is zero, not on ranks, images, kernels, or
relative bases.  This proves Lemma 3.1.

The inclusions in the last three rows of (8) are also immediate without
calculation.  If `P_0=P_1=0`, the star `p_x` is supported on sites `2,3`,
so every `q_23` is killed by the square-free relations.  If
`S_2=S_3=0`, the analogous invisible block is `q_01`.

## 4. One common exceptional site: proved reduction

The natural overlap-one strengthening of Lemma 3.1 is false.  The exact
statement needed below is the common-site incidence assertion

\[
                         q_{03}=q_{13}=q_{23}=0.        \tag{15}
\]

It is useful first to state exactly what remains to be proved.  Normalize
only the four regular maps and delete site `3`.  On the triangle `012` put

\[
 p_x=P_0x+P_1x+P_2x,\qquad
 s_y=S_0y+S_1y+S_2y,                                  \tag{15a}
\]

where `P_1,P_2,S_0,S_2` are isomorphisms and `P_0,S_1` are arbitrary.
Write

\[
 Q=q_{01}+q_{02}+q_{12},\qquad
 T=q_{03}+q_{13}+q_{23}.                               \tag{15b}
\]

For `phi in V_3^*`, contract the site-`3` factor and set

\[
 t_\phi=(\operatorname{id}\otimes\phi)T,\qquad
 c_\phi=\phi S_3,\qquad d_\phi=\phi P_3.              \tag{15c}
\]

The contraction of the four-site erased equation is exactly

\[
 t_\phi p_xs_y+c_\phi(y)Qp_x+d_\phi(x)Qs_y=0
       \qquad(x\in K\text{ or }y\in L).                \tag{15d}
\]

Thus (15) is equivalent to proving `t_phi=0` in (15d) for every `phi`.
This is the precise projected map/kernel statement; it retains all eight
cells and all triangle contamination.

### 4.1 A full-star quadratic annihilator

Let

\[
 \mathcal T=\bigotimes_{i=0}^2(\mathbb F\oplus V_i),
 \qquad \dim V_i=3.                                    \tag{15e}
\]

**Lemma 4.1 (two regular components).**  Suppose `S_0,S_2` are
isomorphisms and `S_1` is arbitrary.  For `H in T_2`,

\[
                         Hs_y=0\quad(y\in W)            \tag{15f}
\]

has the following solutions:

\[
 \{H:Hs_W=0\}= 
 \begin{cases}
  0,&S_1\ne0,\\
  V_0\otimes V_2,&S_1=0.
 \end{cases}                                           \tag{15g}
\]

**Proof.**  Normalize `S_0=S_2=I` and, using an independent basis at
site `1`, put `S_1=diag(I_r,0)`.  If
`H=H_01+H_02+H_12`, the coefficient of
`e_i tensor e_j tensor e_k` at input `e_b` is

\[
 (H_{01})_{ij}\delta_{kb}
 +(H_{02})_{ik}(S_1)_{jb}
 +\delta_{ib}(H_{12})_{jk}=0.                           \tag{15h}
\]

For `r=0`, take successively `k=b,i!=b` and `i=b,k!=b`.
Varying `b` gives `H_01=H_12=0`, while `H_02` is invisible.

Here are the remaining comparisons explicitly.  If `r=1`, label the
active column `0`.  The two zero columns `b=1,2`, with respectively
`k=b,i!=b` and `i=b,k!=b`, kill all of `H_01` and `H_12` (each row or
column is missed by one of the two choices).  Equation (15h) at `b=0`
then reads `(H_02)_{ik}delta_(j0)=0`, so `H_02=0`.

If `r=2`, label the zero column `2`.  Its equations leave only

\[
 (H_{01})_{2j}=z_j,\qquad (H_{12})_{j2}=-z_j.          \tag{15h'}
\]

The active column `b=0`, with `j=0`, kills the entries of `H_02` having
`i!=0,k!=0`; the column `b=1` does the same with `0` and `1` interchanged.
Taking also `k=b` in those two active columns kills the two remaining
off-diagonal entries.  Thus `H_02=0`.  Finally (15h) with
`(b,i,k)=(0,2,0)` gives every `z_j=0`.

If `r=3`, choose `i,j,k` pairwise distinct.  Taking in turn
`b=j,k,i` kills every off-diagonal entry of `H_02,H_01,H_12`.  For a
diagonal entry with color `a`, choose `b!=a`: the triples
`(i,j,k)=(a,a,b)`, `(a,b,a)`, and `(b,a,a)` kill respectively the
diagonal entries of `H_01,H_02,H_12`.  Hence all three blocks vanish.
The four cases are therefore

\[
\begin{array}{c|ccc}
r&H_{01}&H_{02}&H_{12}\\ \hline
0&0&\text{arbitrary}&0\\
1,2,3&0&0&0.
\end{array}                                             \tag{15i}
\]

Every step is a coefficient of (15h), so no simultaneous normal form with
another exceptional map is being used.  This proves (15g).

### 4.2 The two boundary contractions

**Lemma 4.2 (punctured triangle, one scalar component zero).**  In (15a),
let `K subset U` and `L subset W` be planes.  If

\[
 t p_xs_y+c(y)Qp_x+d(x)Qs_y=0
       \qquad(x\in K\text{ or }y\in L),                 \tag{15j}
\]

then `t=0` whenever `c=0` or `d=0`.

**Proof.**  It suffices by the symmetry
`p <-> s`, `0 <-> 1` to treat `c=0`.  For `x in K`, put

\[
                         H_x=tp_x+d(x)Q.                 \tag{15k}
\]

Equation (15j) says `H_xs_y=0` for every `y`.  Choose
`0!=x_0 in K intersect ker d`, and abbreviate
`a_i=P_ix_0`.  The vectors `a_1,a_2` are nonzero.

If `S_1!=0`, Lemma 4.1 gives `tp_(x_0)=0`.  Comparing its three edge
blocks shows that either `t=0`, or

\[
 P_0x_0=0,\qquad
       (t_0,t_1,t_2)=\lambda(0,a_1,-a_2).               \tag{15l}
\]

Indeed the `01` and `02` blocks first make `t_1,t_2` the indicated
multiples; if `P_0x_0!=0`, the `12` block is
`-2\lambda a_1 tensor a_2`, so `lambda=0`.

If `S_1=0`, Lemma 4.1 instead says that `tp_(x_0)` may have only its
`02` block.  Its `01` and `12` blocks give either `t=0`, (15l), or

\[
       (t_0,t_1,t_2)=\lambda(a_0,-a_1,a_2).             \tag{15m}
\]

Now choose `x_1 in ker d` independent of `x_0`.  Put
`a_i'=P_ix_1`.  Since `P_1,P_2` are isomorphisms,

\[
 \Omega_{12}=-a_1\otimes a_2'+a_1'\otimes a_2          \tag{15n}
\]

has mode rank two.  For every `y in L`, (15j) has no `Q` term.
In case (15m), where necessarily `S_1=0`, its left side is

\[
 \lambda\bigl((a_0\otimes a_1'-a_0'\otimes a_1)
                   \otimes S_2y
              +S_0y\otimes\Omega_{12}\bigr).           \tag{15o}
\]

The first summand has mode rank at most one at site `2`; the second has
mode rank two there.  They cannot cancel, so `lambda=0`.

In case (15l), the same coefficient is

\[
 \lambda\bigl(P_0x_1\otimes
       (a_1\otimes S_2y-S_1y\otimes a_2)
       +S_0y\otimes(a_1\otimes a_2'-a_1'\otimes a_2)
       \bigr).                                          \tag{15p}
\]

If `P_0x_1=0`, the second summand is already nonzero.  Otherwise quotient
the site-`0` factor by `F P_0x_1`.  Vanishing for every `y in L` would put
the two-plane `S_0(L)` in that line, impossible.  Hence `lambda=0` here as
well.  This proves the `c=0` case, and the stated symmetry proves `d=0`.

### 4.3 A plane-by-plane pivot

The scalar residual also has an exact closed boundary when either erasure
plane is the kernel of the corresponding scalar component.

For a plane `M subset W`, the same coefficient comparison as (15h), now
using only an ordered basis `y_0,y_1` of `M`, gives

\[
 \{H:Hs_M=0\}=
 \begin{cases}
  V_0\otimes V_2,&S_1|_M=0,\\
  \mathbb F(\Omega_{01},-\Omega_{02},\Omega_{12}),
       &S_1|_M\ne0,
 \end{cases}                                           \tag{15q}
\]

where

\[
 \Omega_{ij}=S_iy_0\otimes S_jy_1-S_iy_1\otimes S_jy_0.
                                                               \tag{15r}
\]

Indeed, after normalizing `S_0(M),S_2(M)` to the first two coordinate
planes, a zero restriction at site `1` leaves exactly the invisible `02`
block.  A nonzero restriction has rank one or two; comparing the
coefficients with third output color first kills every coordinate off the
three displayed alternating blocks, and either active coefficient of
`S_1|_M` makes their three remaining scalars equal with signs `+,-,+`.
Thus (15q) is exhaustive.  Notice that `Omega_02` has mode rank two.

**Lemma 4.3 (plane-by-plane injectivity).**  Let `X subset U` and
`Y subset W` be planes.  Under the regularity assumptions in (15a),

\[
                    tp_xs_y=0\qquad(x\in X, y\in Y)   \tag{15s}
\]

forces `t=0`.

**Proof.**  If `S_1|_Y=0`, (15q) says that the `12` block of `tp_x`
vanishes for every `x in X`:

\[
                  t_1\otimes P_2x+P_1x\otimes t_2=0.   \tag{15t}
\]

Apply this to two independent vectors of `X`.  Since `P_1,P_2` are
isomorphisms, the first equation can only make `t_1,t_2` proportional to
the two images of its input, while the second has independent images.
Hence `t_1=t_2=0`; the `01` block then gives `t_0=0`.

Suppose `S_1|_Y!=0`.  By (15q), there is a linear form `rho on X` such
that

\[
                  tp_x=\rho(x)(\Omega_{01},-Omega_{02},
                                      \Omega_{12}).     \tag{15u}
\]

Choose `0!=x_0 in ker rho`.  If `P_0x_0!=0`, comparison of the three
blocks of `tp_(x_0)=0` gives `t=0`: the first two blocks give alternating
multiples and the third is twice a nonzero pure tensor.  If `P_0x_0=0`,
the only possible nonzero vector is

\[
                  (t_0,t_1,t_2)=lambda
                       (0,P_1x_0,-P_2x_0).              \tag{15v}
\]

Choose `x_1 in X` independent of `x_0`.  The `02` block of `tp_(x_1)`
has rank at most one, whereas the `02` block on the right of (15u) has
rank two.  Hence `rho(x_1)=0` and `P_0x_1=0`.  The `12` block is then the
nonzero rank-two tensor

\[
 \lambda(P_1x_0\otimes P_2x_1-P_1x_1\otimes P_2x_0),
\]

a contradiction unless `lambda=0`.  This proves the lemma.

### 4.4 What the proved lemmas give in four sites

Apply Lemma 4.2 to (15d).  If `phi` annihilates `im S_3`, then
`c_phi=0`, hence `t_phi=0`.  If `phi` annihilates `im P_3`, then
`d_phi=0`, hence again `t_phi=0`.  Therefore, for `i=0,1,2`,

\[
 q_{i3}\in V_i\otimes
       (\operatorname {im}P_3\cap\operatorname {im}S_3).\tag{15w}
\]

In particular (15) is already proved whenever the two exceptional images
at the common site are disjoint.  A component on their common image reduces
to (15j).  Lemma 4.3 closes it if `K=ker d` or `L=ker c`, because
`t p_xs_y` then vanishes on the product of the two kernel planes.  It remains
in this subsection to close the transverse scalar locus

\[
 c,d\ne0,\qquad K\ne\ker d,\qquad L\ne\ker c.          \tag{15x}
\]

Choose bases adapted to the two transverse pairs:

\[
\begin{aligned}
 D:=\ker d&=\langle x_0,x_1\rangle,&
 K&=\langle x_0,x_2\rangle,&d(x_2)&=1,\\
 C:=\ker c&=\langle y_0,y_1\rangle,&
 L&=\langle y_0,y_2\rangle,&c(y_2)&=1.
\end{aligned}                                          \tag{15y}
\]

Let `A_s` be the quadratic annihilator of `s_C` and `A_p` that of
`p_D`.  Formula (15q) gives

\[
\begin{array}{c|c}
S_1|_C=0&\mathcal A_s=V_0\otimes V_2\\
S_1|_C\ne0&\mathcal A_s=\mathbb F\Omega_s
\end{array},\qquad
\begin{array}{c|c}
P_0|_D=0&\mathcal A_p=V_1\otimes V_2\\
P_0|_D\ne0&\mathcal A_p=\mathbb F\Omega_p.
\end{array}                                             \tag{15z}
\]

The seven erased cells other than `(x_2,y_2)` say exactly

\[
\begin{aligned}
 tp_{x_0},\ tp_{x_2}+Q&\in\mathcal A_s,\\
 ts_{y_0},\ ts_{y_2}+Q&\in\mathcal A_p.                \tag{15aa}
\end{aligned}
\]

If `S_1|_C=0`, the first membership in (15aa), on its `01` and `12`
blocks, makes every possible nonzero `t` a scalar multiple of

\[
 (P_0x_0,-P_1x_0,P_2x_0).                              \tag{15ab}
\]

If also `P_0|_D=0`, the `01` block of `ts_(y_0)` kills this scalar.  If
`P_0|_D!=0`, then `ts_(y_0)` is a multiple of `Omega_p`; its `12` block
has rank two, whereas the `12` block obtained from (15ab) is the pure
tensor `-P_1x_0 tensor S_2y_0`.  Its multiplier is therefore zero, and
the `01` block again kills (15ab).  The case `P_0|_D=0` is symmetric.
Thus only the line--line row of (15z) remains.

Put

\[
 \Delta_s=\Omega_s s_{y_2},\qquad
 \Delta_p=\Omega_p p_{x_2}.                            \tag{15ac}
\]

These are the generalized determinant tensors
`(S_0 tensor S_1 tensor S_2)epsilon` and
`(P_0 tensor P_1 tensor P_2)epsilon`, up to nonzero scalars.  Write the
four memberships in (15aa) as

\[
\begin{aligned}
tp_{x_0}&=\rho_0\Omega_s,&tp_{x_2}+Q&=\rho_2\Omega_s,\\
ts_{y_0}&=\sigma_0\Omega_p,&ts_{y_2}+Q&=\sigma_2\Omega_p.
\end{aligned}                                          \tag{15ad}
\]

Multiplying the first and third equations by the complementary outside
vectors, and using the erased cell `(x_2,y_2)` for the other two, gives

\[
\begin{aligned}
Qp_{x_r}&=-\rho_r\Delta_s&&(r=0,2),\\
Qs_{y_r}&=-\sigma_r\Delta_p&&(r=0,2).                  \tag{15ae}
\end{aligned}
\]

Equations (15ad)--(15ae), together with the displayed block definitions,
are the current exact parameterization of the residual line--line branch.
They retain the final erased cell and every contribution of `Q`.

A tempting shortcut here is false: for a fixed three-site star vector whose
three components are nonzero, the kernel of `Q \mapsto Qp_z` has dimension
eight, not two, and its response at an independent vector can have mode rank
three.  Thus determinant-line responses cannot be discarded by mode rank
alone.  The simultaneous crossed system (15ad)--(15ae) was the remaining
issue.  The following exact factorization argument closes that system.

### 4.5 Exact residual factorization

First extend the four scalars in (15ad) linearly to
\(\rho\in K^*\) and \(\sigma\in L^*\).  Equations
(15ad)--(15ae) are equivalently

\[
\begin{aligned}
 tp_x+d(x)Q&=\rho(x)\Omega_s,&
 Qp_x&=-\rho(x)\Delta_s &&(x\in K),\\
 ts_y+c(y)Q&=\sigma(y)\Omega_p,&
 Qs_y&=-\sigma(y)\Delta_p &&(y\in L).
\end{aligned}                                          \tag{15af}
\]

This form includes both coordinate slices, the final erased cell, and all
terms involving \(Q\).

**Lemma 4.4 (linear kernel of a plane boundary).**  Let \(M\) be a
two-plane, let \(R_0,R_2\) be injective on \(M\), and suppose
\(R_1|_M\ne0\).  For a basis \(u,v\) of \(M\), put

\[
\Omega_R=(u_0v_1-v_0u_1,\,-u_0v_2+v_0u_2,\,
                         u_1v_2-v_1u_2),               \tag{15ag}
\]

where \(u_i=R_i u\), \(v_i=R_i v\), and juxtaposition denotes tensor
product on the indicated sites.  Then, for arbitrary \(r_i\in V_i\),

\[
 \Omega_R(r_0+r_1+r_2)=0
 \quad\Longleftrightarrow\quad
 (r_0,r_1,r_2)=(R_0z,R_1z,R_2z)
 \quad\hbox{for some }z\in M.                          \tag{15ah}
\]

**Proof.**  If \(R_1|_M\) has rank two, normalize the three image planes
with the ordered bases \(u_i,v_i\).  Projection modulo these planes in
each tensor mode first puts every \(r_i\) in its corresponding image
plane.  Write \(r_i=\alpha_i u_i+\beta_i v_i\).  The six possibly
nonzero coefficients of \(\Omega_Rr\) are, up to their displayed signs,

\[
 \alpha_0-\alpha_1,\quad-\alpha_0+\alpha_2,\quad
 \alpha_1-\alpha_2,\qquad
 \beta_0-\beta_2,\quad-\beta_0+\beta_1,\quad
 -\beta_1+\beta_2.
\]

Thus all three \(\alpha_i\) agree and all three \(\beta_i\) agree, which
is (15ah).

If \(R_1|_M\) has rank one, choose \(u,v\) so that
\(u_1=b\ne0\) and \(v_1=0\).  The three blocks in (15ag) become

\[
       (-v_0b,\,-u_0v_2+v_0u_2,\,bv_2).               \tag{15ai}
\]

Projection away from
\(\langle u_0,v_0\rangle,\mathbb Fb,\langle u_2,v_2\rangle\)
again kills all outside components.  Writing

\[
 r_0=\alpha u_0+\beta v_0,\qquad
 r_1=\gamma b,\qquad
 r_2=\delta u_2+\varepsilon v_2,
\]

the coefficients of \(u_0bv_2,v_0bu_2,v_0bv_2\) give
\(\alpha=\gamma=\delta\) and \(\beta=\varepsilon\).  Hence
\(r=(R_0z,R_1z,R_2z)\) for
\(z=\gamma u+\varepsilon v\).  The reverse implication follows by direct
multiplication in both ranks.

**Lemma 4.5 (factorization of a plane boundary).**  In the setting of
Lemma 4.4, suppose

\[
             (t_0+t_1+t_2)(a_0+a_1+a_2)
                       =\lambda\Omega_R,\qquad\lambda\ne0. \tag{15aj}
\]

If \(R_1|_M\) has rank two, (15aj) has no solution.  If it has rank one
and \(a_1\ne0\), then

\[
                         t_1=0,\qquad t_0,t_2\ne0.      \tag{15ak}
\]

The corresponding statement holds after any permutation of the three
sites, with the exceptional component permuted in the same way.

**Proof.**  Divide \(t\) by \(\lambda\).  In the rank-two case every
block on the right has matrix rank two.  Therefore
\(\{t_i,a_i\}\) is a basis of the image plane at site \(i\).  In the
ordered bases \(u_i,v_i\), let \(M_i\) have columns \(t_i,a_i\), and put

\[
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 E=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

The three edge equations are

\[
 M_0JM_1^{\mathsf T}=E,\qquad
 M_0JM_2^{\mathsf T}=-E,\qquad
 M_1JM_2^{\mathsf T}=E.                               \tag{15al}
\]

The first two give \(M_2=-M_1\).  The left side of the third is then
\(-M_1JM_1^{\mathsf T}\), which is symmetric, whereas \(E\) is nonzero
and skew-symmetric.  This is impossible over \(\mathbb C\).

For rank one use (15ai).  The middle block has rank two, so
\(\{t_0,a_0\}\) and \(\{t_2,a_2\}\) are bases of the two regular image
planes.  The other two blocks imply
\(a_1=A b\), \(t_1=T b\).  Write

\[
 M_0=\begin{pmatrix}\alpha&\gamma\\ \beta&\delta\end{pmatrix},
 \qquad D=\alpha\delta-\beta\gamma,\qquad q=\binom A T.
\]

The three block equations in (15ai) say

\[
\begin{aligned}
 M_0J M_2^{\mathsf T}
   &=\begin{pmatrix}0&-1\\1&0\end{pmatrix},&
 M_0q&=\binom0{-1},&
 M_2q&=\binom01.
\end{aligned}                                         \tag{15am}
\]

The first two equations determine

\[
 M_2={1\over D}
       \begin{pmatrix}\alpha&-\gamma\\\beta&-\delta\end{pmatrix},
 \qquad
 q={1\over D}\binom{\gamma}{-\alpha}.
\]

The first coordinate of the last equation in (15am) is
\(2\alpha\gamma/D^2=0\).  Since
\(a_1=A b\ne0\), one has \(\gamma\ne0\), hence
\(\alpha=0\).  It follows that \(T=0\), while
\(D=-\beta\gamma\ne0\) makes the first columns of both
\(M_0\) and \(M_2\) nonzero.  The second coordinate gives
\(\beta\gamma=1\), so in fact
\(t=(\beta v_0,0,-\beta v_2)\).  This is (15ak).  Permuting tensor modes
only transports the signs in (15ag), and an overall sign is absorbed by
\(\lambda\).

It remains to audit the cases where a response vanishes on one or both
of the selected coordinate slices.

**Lemma 4.6 (the distinguished slices).**  In (15af), if
\(\rho(x_0)=0\) or \(\sigma(y_0)=0\), then \(t=0\).

**Proof.**  We prove the assertion for \(\rho\); the other assertion is
obtained by interchanging the two stars and sites \(0,1\).

First suppose \(\rho=0\).  Since \(d(x_0)=0\),
\(tp_{x_0}=0\).  Put \(a_i=P_i x_0\).  A comparison of its three blocks
shows that a nonzero \(t\) would require

\[
       a_0=0,\qquad t=\lambda(0,a_1,-a_2),\quad\lambda\ne0. \tag{15an}
\]

Indeed, if \(a_0\ne0\), the first two blocks give
\(t=(\mu a_0,-\mu a_1,-\mu a_2)\), and the last block is
\(-2\mu a_1a_2\).  If \(a_0=0\), the first and last blocks give exactly
(15an).

Put \(A_i=P_i x_2\).  The \(x_2\) equations give
\(Q=-tp_{x_2}\) and \(Qp_{x_2}=0\).  Direct multiplication gives

\[
 tp_{x_2}^2
   =2\lambda A_0\bigl(a_1A_2-A_1a_2\bigr).            \tag{15ao}
\]

The bracket has matrix rank two because \(P_1,P_2\) are isomorphisms and
\(x_0,x_2\) are independent.  Thus \(A_0=0\), so \(P_0|_K=0\), and
\(Q\) has only its \(12\) block.

Now \(P_0|_D\ne0\), so \(a'_0=P_0x_1\ne0\).  Relative to the basis
\(x_0,x_1\) of \(D\), the \(01\) block of \(\Omega_p\) is
\(-a'_0a_1\).  For each of the independent vectors \(y_0,y_2\), the
\(01\) block of

\[
                  ts_y+c(y)Q=\sigma(y)\Omega_p
\]

therefore says
\(\lambda S_0y\otimes a_1=-\sigma(y)a'_0\otimes a_1\).
It puts both \(S_0y_0\) and \(S_0y_2\) in
\(\mathbb F a'_0\), contradicting the injectivity of \(S_0\).

Finally suppose \(\rho(x_0)=0\) but \(\rho(x_2)\ne0\).  If \(t\ne0\),
the first part of the preceding block comparison again gives (15an).
Multiply

\[
                  tp_{x_2}+Q=\rho(x_2)\Omega_s
\]

by \(p_{x_0}\).  Associativity, \(tp_{x_0}=0\), and
\(Qp_{x_0}=0\) make the left side zero.  Lemma 4.4 gives
\(p_{x_0}=s_z\) for some \(z\in C\).  Its site-zero component is
\(0=P_0x_0=S_0z\), so \(z=0\); its site-one component would then also
vanish, contradicting \(P_1x_0\ne0\).  This proves the lemma in every
zero-slice case.

We can now apply the three lemmas to the residual system.  Suppose
\(t\ne0\).  Lemma 4.6 gives
\(\rho(x_0),\sigma(y_0)\ne0\).  The equation

\[
                         tp_{x_0}=\rho(x_0)\Omega_s
\]

and Lemma 4.5 exclude rank two for \(S_1|_C\).  Its rank is therefore
one, and \(P_1x_0\ne0\) makes the rank-one conclusion

\[
                         t_1=0,\qquad t_0,t_2\ne0.      \tag{15ap}
\]

Symmetrically,

\[
                         ts_{y_0}=\sigma(y_0)\Omega_p
\]

excludes rank two for \(P_0|_D\).  In rank one its exceptional factor
component is \(S_0y_0\ne0\), so the permuted rank-one conclusion is

\[
                         t_0=0,\qquad t_1,t_2\ne0,      \tag{15aq}
\]

contradicting (15ap).  Thus these coefficient calculations force \(t=0\)
also in the residual line--line branch.

The canonical identities in Lemmas 4.4--4.6 are checked exactly in
[verify_exact_eight_residual_factorization.py](../computations/verify_exact_eight_residual_factorization.py).
The checker is an audit of the displayed identities, not a replacement
for the invariant reductions above.

**Independent audit.**  A separate rederivation checked both ranks in
Lemma 4.4, the rank-one and rank-two factorizations in Lemma 4.5, every
zero-slice branch in Lemma 4.6, and the site-permuted application to
\(\Omega_p\).  Exact direct rank tests on transverse rank-one common images,
including degenerate Gaussian-rational source and image planes, also forced
all three common-site incident blocks to vanish.  No additional genericity
or division assumption is used.

Full injectivity cannot replace (15).  Take `ell=m=e_0^*`, put

\[
\begin{aligned}
P_0&=\begin{pmatrix}-1&0&2\\3&2&-1\\-2&0&4\end{pmatrix},&
P_1&=P_2=I,&
P_3&=\begin{pmatrix}2&0&0\\0&0&0\\2&0&0\end{pmatrix},\\
S_0&=S_2=I,&
S_1&=\begin{pmatrix}0&0&0\\-2&-2&2\\-4&-4&-6\end{pmatrix},&
S_3&=0.
\end{aligned}                                           \tag{16}
\]

Both exceptional pairs are nonzero, with ranks `(2,1)` and `(2,0)`, but
the eight-cell map has rank `53`.  A nonzero kernel vector is supported
on triangle `012`, with

\[
q_{01}=\begin{pmatrix}0&0&0\\0&-2&6\\0&-2&-4\end{pmatrix},\quad
q_{02}=\begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix},\quad
q_{12}=\begin{pmatrix}0&0&0\\0&2&2\\0&-6&4\end{pmatrix}.            \tag{17}
\]

All other blocks are zero.  Direct integer multiplication verifies all
eight erased cells.  Thus (16)--(17) falsifies the stronger overlap-one
claim while illustrating exactly why (15) is the stable conclusion.

## 5. The exact-eight support census

Apply all position consequences already used in the exact-seven proof,
on both shores.  Of the `binom(16,8)=12870` eight-position supports,
`4698` survive, in ten row/column/transpose orbits.  Lemma 6.1 of
[`two-k4-six-cycle-two-defect-obstruction.md`](two-k4-six-cycle-two-defect-obstruction.md)
removes every support containing a singleton row or column and a
degree-two row or column whose defect pair avoids the singleton defect.
Exactly `378` labelled supports remain, in three orbits:

\[
\begin{array}{c|c|c|c}
 &\text{orbit size}&\text{representative}&\text{degree type}\\ \hline
G_0&18&00,01,10,11,22,23,32,33&C_4\sqcup C_4\\
G_1&72&00,01,10,12,21,23,32,33&C_8\\
G_2&288&00,01,02,10,13,21,23,33&(3,2,2,1)\text{ on both shores}.
\end{array}                                             \tag{18}
\]

For `G_0`, rows `0,2` have disjoint exceptional pairs `{0,1}` and
`{2,3}`.  For `G_1`, rows `0,3` have the same two disjoint pairs.  For
`G_2`, rows `1,2` have pairs `{0,3}` and `{1,3}`, with common site `3`.

## 6. Pullback of the actual two-/four-cross sector

Choose complementary left row pairs `{a,b}` and `{r,s}` with

\[
                         c=\kappa(ab)=\kappa(rs).       \tag{19}
\]

On the four right sites put

\[
 p_{i,x}=\sum_j\operatorname {row}_x(B_{ij})^{(j)},
 \qquad
 q_{\rm eff}=\lambda_{ab}q_R+p_{a,c}p_{b,c}.           \tag{20}
\]

Exact grouping of the two- and four-cross matchings gives

\[
 q_{\rm eff}p_{r,x}p_{s,y}
   =\text{the complete two-/four-cross coefficient}    \tag{21}
\]

whenever `(x,y)!=(c,c)`.  The corresponding left word is nonconstant,
`ab` is its unique compatible internal edge, and neither the zero-cross
sector nor the target contributes.  Hence the tensor equations give the
eight erasures

\[
 q_{\rm eff}p_{r,x}p_{s,y}=0
                         \qquad((x,y)\ne(c,c)).         \tag{22}
\]

This is the actual sector identity; it is not a dead-slab relaxation.

## 7. The two 2-regular masks

Apply Lemma 3.1 to the row pairs specified after (18).

If both exceptional row pairs contain a nonzero block, (8) gives
`q_eff=0`.  If exactly one pair consists of two literal zero blocks,
`q_eff` is supported on one opposite edge.  In the latter case choose a
right endpoint outside that edge.  In either case there is a right site
at which all three incident blocks of `q_eff` vanish.

This is impossible.  The three incident blocks of
`lambda_ab q_R` have the three distinct coordinate endpoint lines

\[
                  \mathbb F e_{\kappa(ij)}\qquad(j\ne i),             \tag{23}
\]

whereas every incident block of the product correction in (20) has its
endpoint image in the fixed plane

\[
 \operatorname {span}\bigl(
   \operatorname {row}_c(B_{ai})^{\mathsf T},
   \operatorname {row}_c(B_{bi})^{\mathsf T}\bigr).   \tag{24}
\]

The three lines (23) cannot lie in (24).

If the first chosen disjoint row pair consists of two double-zero rows
but not all eight singular blocks are zero, choose the other disjoint
degree-two row pair containing a nonzero singular block.  The preceding
zero- or one-residual-edge argument applies.  It remains only to exclude
the case in which all eight singular blocks are literally zero.

For that last case, the two matching-edge blocks allowed by (8) are
invisible even at `(x,y)=(c,c)`.  The omitted constant-word equation,
after the harmless normalization of the nonzero internal pure cells, is

\[
                  q_Rp_{a,c}p_{b,c}+\Delta_R=X_c.      \tag{25}
\]

Equivalently, the two-edge-star response on the right is the nonzero pure
sum in the two colors different from `c`.  Lemma 7.1 of
[`two-k4-low-matching-cross-obstruction.md`](two-k4-low-matching-cross-obstruction.md)
then says that among

\[
 Z_v=\bigl[p_{a,c}^{(v)}\ \ p_{b,c}^{(v)}\bigr]
                         \qquad(v=0,1,2,3)              \tag{26}
\]

there is a unique matrix of rank two.

But in both masks the zero sets of the two complementary rows cover all
four right sites:

\[
\begin{array}{c|c|c}
 &a\text{ zero set}&b\text{ zero set}\\ \hline
C_4\sqcup C_4&\{0,1\}&\{2,3\}\\
C_8&\{0,2\}&\{1,3\}.
\end{array}                                             \tag{27}
\]

At every site one column of `Z_v` is therefore zero, so every `Z_v` has
rank at most one.  This contradicts the two-edge-star normal form and
closes both 2-regular orbits.

## 8. The overlap-one orbit

For `G_2`, take `(r,s)=(1,2)`, `(a,b)=(0,3)`, and common exceptional
right site `3`.  Equation (22) and the common-site incidence assertion
(15) give

\[
                  (q_{\rm eff})_{03}=(q_{\rm eff})_{13}
                    =(q_{\rm eff})_{23}=0.             \tag{28}
\]

At endpoint `3`, the three incident blocks of `q_R` again have the three
coordinate lines, while the product correction has endpoint image in the
two-plane (24).  Equation (28) is therefore impossible.  This closes the
last `288` supports in (18), and proves (1).

## 9. Exact audit

Run

```text
python computations/verify_two_k4_exact_eight_checkerboard_hessian.py
```

The checker verifies:

1. the four disjoint kernel dimensions `0,9,9,18`, their exact edge-block
   supports, and a unimodular full-rank minor in the minimally active case;
2. `625` zero/rank-one/rank-two disjoint normal-form combinations and a
   nontrivial relative-basis specialization;
3. the common-site incidence conclusion in `625` overlap-one strata;
4. the exact rank-`53` counterexample (16)--(17);
5. the census `4698 -> 378 = 18+72+288`; and
6. all `2187` coefficients of the actual sector identity (21) for the
   three representatives in (18).

The output is

```text
disjoint two-plus-two kernels: 0/9/9/18 exactly
minimal active disjoint minor: determinant 1
overlap-one injectivity: FALSE (exact rank-53 counterexample)
overlap-one common-site incident blocks: zero in all audited strata
exact-eight census: 4698 -> 378 = 18 + 72 + 288
exact-eight sector identities: 2187 exact coefficients
two-K4 exact-eight checkerboard Hessian audit: PASS
```
