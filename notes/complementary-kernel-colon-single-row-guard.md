# Complementary kernel packets leave one sharp colon row

## 1. Outcome

Work on the five-site common complement \(D\) at the first \(8\to6\)
boundary.  At \(h=3\), the literal 27-row overlap is

\[
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[2]}
       +x_i y_jt_kz=\mathbf1_{i=j=k}X_i .                 \tag{1}
\]

Assume that the two rank-two direct blocks have a shared left kernel and
the target-centred complementary right kernels

\[
 \xi^{\mathsf T}P=\xi^{\mathsf T}R=0,
 \qquad P\eta=0,
 \qquad R\eta'=0,                                        \tag{2}
\]

with

\[
 \operatorname {supp}\xi=\{e,a\},\qquad
 \operatorname {supp}\eta=
 \operatorname {supp}\eta'=\{e,b\},
 \qquad\{e,a,b\}=\{0,1,2\}.                             \tag{3}
\]

Put \(L=x(\xi)\), \(y(\eta)=\sum_j\eta_jy_j\), and similarly
for \(t(\eta')\).  Contracting (1) literally gives both packets

\[
 \boxed{
 L\left(y_jt_k+{T_{jk}\over2}z\right)z
       =\delta_{jk}\xi_jX_j,}                             \tag{4L}
\]

and

\[
 \boxed{
 x_i\left(y(\eta)t(\eta')
       +{\eta^{\mathsf T}T\eta'\over2}z\right)z
       =\eta_i\eta'_iX_i.}                               \tag{4R}
\]

These complementary two-anchor packets do **not** force the generic
selector-provenance generator to vanish, do not by themselves give its
filtered source lift, and do not produce a degree-five Macaulay dual.
Their exact case-free consequence is only

\[
 \boxed{
 \omega_{T_{\{e,a\}}}(yt)
  :=T_{ae}y_et_a-T_{ea}y_at_e
       \in\operatorname {Ann}_2(Lz).}                     \tag{5}
\]

Thus (4L)--(4R) give the sharp alternative

\[
\omega_{T_{\{e,a\}}}(yt)=0
\quad\text{or}\quad
0\ne\omega_{T_{\{e,a\}}}(yt)
       \in\operatorname {Ann}_2(Lz).                      \tag{6}
\]

This is the \(h=3\) member of a uniform odd-complement statement.  For the
general \(2h-1\)-site overlap, replace \(Lz\) by
\(Lz^{[h-2]}\) and \(1/2\) by \(1/(h-1)\).  The same weighted subtraction
puts \(\omega\) in
\(\operatorname {Ann}_2(Lz^{[h-2]})\).  The missing parameter-side input
is then a source-faithful prolongation

\[
 {\cal E}\otimes\operatorname {Sym}^{h-1}\mathbb C^2
       \longrightarrow\operatorname {Sym}^{2h-1}\mathbb C^2, \tag{6a}
\]

not another site-algebra contraction.  At \(h=3\), (6a) is exactly the
three \(u^2,uv,v^2\) shifts into binary quintics.

The right packet has one common \(e\)-anchor syzygy with the left packet;
its other rows split the \(\{e,b\}\)-quadratic against the individual
\(x_i\)'s.  None contains either \(y_et_a\) or \(y_at_e\), so it does not
remove the class in (5).

There is a site-minimal integral guard proving sharpness.  It has

* five square-zero sites, the minimum compatible with nonzero degree-five
  targets;
* noncoordinate \(\xi,\eta,\eta'\) with the supports in (3);
* rank-two \(P,R\), an invertible completed \(T_{\{e,a\}}\), and selected
  curvature \(AU-BF=1\);
* both complete contraction tables (4L)--(4R);
* a nonzero \(\omega\) for which \(\omega z\ne0\) but \(L\omega z=0\); and
* 26 of the 27 uncontracted rows (1).

Its sole uncontracted residual is exactly

\[
                         (i,j,k)=(b,e,a).                  \tag{7}
\]

That residual is invisible to both contraction tensors because
\(\xi_b=0\) and \(\eta'_a=0\).  It is also exactly the missing summand in
the weighted full-source row whose quadratic component is
\(x_b\omega z\).  Consequently the first positive continuation is not
another contraction: it must use the literal \((b,e,a)\) row with its
direct--star companion.  Even that row would only provide the filtered
relation; the common \(u^2,uv,v^2\) Macaulay prolongation would remain a
separate step.

## 2. Derivation of the two literal contractions

Multiply (1) by \(\xi_i\) and sum over \(i\).  The \(P\)- and \(R\)-terms
vanish separately by (2).  The remaining equation is

\[
             T_{jk}Lz^{[2]}+Ly_jt_kz
                  =\delta_{jk}\xi_jX_j.                  \tag{8}
\]

In the commutative divided-power normalization,
\(z^2=2z^{[2]}\).  Hence (8) is precisely (4L).  No \(L\) or \(z\) has
been cancelled.

Instead multiply (1) by \(\eta_j\eta'_k\) and sum over \(j,k\).  The
\(P\)-term contains \(P\eta\), and the \(R\)-term contains \(R\eta'\), so
both vanish before any common power is touched.  The target term is

\[
 \sum_{j,k}\eta_j\eta'_k\mathbf1_{i=j=k}X_i
                   =\eta_i\eta'_iX_i.                    \tag{9}
\]

This proves (4R), including the literal coefficient \(1/2\).

The two packets are not independent at their shared target.  Contracting
(4R) by \(\xi_i\) gives

\[
 L\left(y(\eta)t(\eta')
       +{\eta^{\mathsf T}T\eta'\over2}z\right)z
       =\xi_e\eta_e\eta'_eX_e.                            \tag{10}
\]

The same identity is obtained by contracting (4L) by
\(\eta_j\eta'_k\).  This is the unique common contraction forced by the
support cross (3).  In particular, noncoordinate \(\eta,\eta'\) add the
\(b\)-anchor in (4R), but they do not add a second equation involving an
\(a\)-crossed product.

### Uniform odd-complement form

For clarity, the cancellation above is not peculiar to \(h=3\).  On the
odd common complement of size \(2h-1\), the literal rows are

\[
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[h-1]}
       +x_iy_jt_kz^{[h-2]}
          =\mathbf1_{i=j=k}X_i.                           \tag{10a}
\]

Since

\[
                       zz^{[h-2]}=(h-1)z^{[h-1]},          \tag{10b}
\]

the two contractions become

\[
 L\left(y_jt_k+{T_{jk}\over h-1}z\right)z^{[h-2]}
       =\delta_{jk}\xi_jX_j                               \tag{10c}
\]

and

\[
 x_i\left(y(\eta)t(\eta')
       +{\eta^{\mathsf T}T\eta'\over h-1}z\right)z^{[h-2]}
       =\eta_i\eta'_iX_i.                                 \tag{10d}
\]

Consequently, with

\[
 K^{(h)}_{L,z}
   :=\operatorname {Ann}_2\!\left(Lz^{[h-2]}\right),      \tag{10e}
\]

the same crossed subtraction gives

\[
                         \omega_{T_{\{e,a\}}}(yt)
                               \in K^{(h)}_{L,z}.           \tag{10f}
\]

No case distinction or cancellation of \(z^{[h-2]}\) is involved.  The
five-site theorem and guard below specialize (10a)--(10f) to \(h=3\).

## 3. The kill-or-explicit-colon theorem

Order the completed left-kernel square by \((e,a)\) and write

\[
 T_{\{e,a\}}=
   \begin{pmatrix}A&B\\ C&D\end{pmatrix},
 \qquad B=T_{ea},\quad C=T_{ae}.                           \tag{11}
\]

The two crossed members of (4L) are

\[
 L\left(y_et_a+{B\over2}z\right)z=0,
 \qquad
 L\left(y_at_e+{C\over2}z\right)z=0.                    \tag{12}
\]

Multiply the first equation by \(C\), the second by \(B\), and subtract.
The two radial terms cancel literally, proving (5).  When
\((B,C)\ne(0,0)\), the covector

\[
                 (0,C,-B,0)                               \tag{13}
\]

spans the annihilator of
\(\Delta+\mathbb CT_{\{e,a\}}\subseteq\operatorname {Mat}_2\).
Therefore (5) is exactly the generic one-dimensional selector quotient,
not merely an arbitrary crossed combination.

This proves a genuine kill-or-colon theorem without a support census.  It
does not prove the first alternative in (6), because multiplication by
\(Lz\) need not be injective in the five-site square-zero algebra.  The
right packet cannot repair that logical gap: its quadratic uses only
\(y_e,y_b,t_e,t_b\), whereas (13) uses the two \(a\)-crossed products.
Equation (10) is the complete overlap between the two contracted packets.

There is a precise uncontracted row behind the missing grade.  Let
\(\mathscr R_{ijk}\) denote the left side of (1) minus its right side.
The weighted pair at the complementary first label \(b\) expands to

\[
\begin{aligned}
 C\mathscr R_{bea}-B\mathscr R_{bae}
  ={}&x_b\bigl(Cy_et_a-By_at_e\bigr)z\\
   &+\bigl[
       C(P_{be}t_a+R_{ba}y_e)
       -B(P_{ba}t_e+R_{be}y_a)
     \bigr]z^{[2]}.                                      \tag{14}
\end{aligned}
\]

The \(BCx_bz^{[2]}\) terms cancel.  Thus (14) is the first literal
full-source relation carrying \(x_b\omega z\) together with its exact
direct--star companion.  Neither (4L) nor (4R) contains it.

At the level of row tensors this omission is forced cleanly.  The left
packet tests a residual tensor against
\(\xi\otimes E_{jk}\), while the right packet tests it against
\(E_i\otimes\eta\otimes\eta'\).  The elementary tensor

\[
                         E_{bea}                           \tag{15}
\]

is killed by both tests, since \(\xi_b=0\) and \(\eta'_a=0\).  The guard
below realizes exactly this one-dimensional residual and no other row
error.

### Rank-at-most-one corollary

There is a useful case-free extension upstream.  If both direct blocks
have rank at most one, then

\[
 \dim\ker P^{\mathsf T}\ge2,
 \qquad \dim\ker R^{\mathsf T}\ge2,
\]

so their left-kernel planes intersect nontrivially in three dimensions.
Any nonzero \(\xi\) in that intersection produces (4L) without a ruling-
alignment hypothesis.  A full-support \(\xi\) anchors all three labels,
support two gives the rectangle (11)--(13), and a coordinate \(\xi\)
gives the one-anchor specialization.  On the support-two branch the same
kill-or-colon theorem applies verbatim; the extra left-kernel dimension
does not license cancellation of \(Lz\).

## 4. A five-site integral guard with only one missing row

Let

\[
 {\cal A}=\mathbb Q[u_0,u_1,u_2,u_3,u_4]/(u_0^2,\ldots,u_4^2),
 \qquad \Omega=u_0u_1u_2u_3u_4,                           \tag{16}
\]

and set

\[
                         z=u_1u_3+u_2u_4,
 \qquad z^{[2]}=u_1u_2u_3u_4.                             \tag{17}
\]

Use labels \(e=0,a=1,b=2\).  Define the endpoint stars

\[
\begin{array}{lll}
 x_0=-u_4,&x_1=u_0+u_4,&x_2=-u_3,\\
 y_0=u_0+u_2,&y_1=-u_1,&y_2=u_1+u_2-u_3,\\
 t_0=-u_2+u_3+u_4,&t_1=u_4,&
 t_2=-u_0-u_1-u_2+u_3.
\end{array}                                                \tag{18}
\]

Take

\[
 P=\begin{pmatrix}
 -1&0&1\\ 1&0&-1\\ 1&-1&-1
 \end{pmatrix},\qquad
 R=\begin{pmatrix}
 3&0&-3\\ -3&0&3\\ 0&-1&0
 \end{pmatrix},\qquad
 T=\begin{pmatrix}
 3&-1&0\\ 1&-1&1\\ -2&-1&-2
 \end{pmatrix}.                                           \tag{19}
\]

Finally put

\[
 \xi=(1,1,0)^{\mathsf T},\qquad
 \eta=\eta'=(1,0,1)^{\mathsf T},\qquad
 (X_0,X_1,X_2)=(4\Omega,-\Omega,2\Omega).                \tag{20}
\]

Direct calculation gives

\[
 \xi^{\mathsf T}P=\xi^{\mathsf T}R=0,
 \qquad P\eta=R\eta'=0,
 \qquad \operatorname {rank}P=\operatorname {rank}R=2.  \tag{21}
\]

The completed selector square is genuinely generic:

\[
 T_{\{e,a\}}=\begin{pmatrix}3&-1\\1&-1\end{pmatrix},
 \qquad \det T_{\{e,a\}}=-2,
 \qquad (B,C)=(-1,1).                                    \tag{22}
\]

Substitution into all 27 expressions in (1) yields the exact residual
table

\[
 \boxed{
 \mathscr R_{ijk}=0\quad\text{for }(i,j,k)\ne(b,e,a),
 \qquad
 \mathscr R_{bea}=-\Omega.}                              \tag{23}
\]

In particular, this is stronger than a guard made only from the two
contraction tables: every other uncontracted overlap row is already
present.  Contracting (23) by \(\xi_i\) or by
\(\eta_j\eta'_k\) gives zero, so both (4L) and (4R) hold exactly.

The selector generator is

\[
\begin{aligned}
 \omega
 &=y_0t_1+y_1t_0\\
 &=u_0u_4+u_2u_4+u_1u_2-u_1u_3-u_1u_4.                  \tag{24}
\end{aligned}
\]

It is nonzero, and its colon behavior is sharp:

\[
             \omega z=u_0u_1u_3u_4\ne0,
 \qquad L\omega z=u_0\omega z=0.                        \tag{25}
\]

Thus neither \(\omega=0\) nor the stronger accidental relation
\(\omega z=0\) explains the contracted tables.

For (14), the companion row \((b,a,e)\) holds while the other one does
not:

\[
 \mathscr R_{bae}=0,
 \qquad
 C\mathscr R_{bea}-B\mathscr R_{bae}=-\Omega.             \tag{26}
\]

Equation (26) identifies the precise missing full-source row, with its
orientation and coefficient.  It is not a generic statement that “some
other row” may help.

The selected curvature can coexist with the guard.  Choose the selected
entries in the omitted row and expose the literal site \(u_4\).  From
(18),

\[
 \begin{gathered}
 A=P_{be}=1,\qquad B_{\rm sel}=R_{ba}=-1,\\
 F=[u_4]y_e=0,\qquad U=[u_4]t_a=1.
 \end{gathered}
\]

Then

\[
                         AU-B_{\rm sel}F=1.                \tag{27}
\]

No source minor has been substituted for this physical scalar.

Five sites are minimal in site count: in a square-zero algebra on at most
four sites the degree-five component is zero, whereas (20) has three
nonzero degree-five anchors.  No claim is made that (18)--(19) minimize
the number or height of integer coefficients.

## 5. Why no Macaulay functional follows

The site degree in (4L)--(4R) is five, but this is not the parameter degree
of a binary clean line.  The packets specify no map from their five-site
colon module to
\((\operatorname {Sym}^5\mathbb C^2)^*\).  Noncoordinate
\(\eta,\eta'\) add the \(b\)-anchor; they do not define the three shifts
\(u^2,uv,v^2\) of every cubic clean coordinate.

This logical independence has a minimal formal test.  Decorate the static
guard, without changing any datum above, by the rootless binary cubics

\[
                              f=s^3,\qquad g=t^3.           \tag{28}
\]

Their six quadratic shifts are

\[
 s^5,s^4t,s^3t^2,s^2t^3,st^4,t^5,                        \tag{29}
\]

the full monomial basis of \(\operatorname {Sym}^5\mathbb Q^2\).
Consequently the degree-five Macaulay matrix has rank six and its dual
kernel is zero.  Since (28) is independent decoration, this is not claimed
to arise from a complete Krenn source.  Its exact role is to rule out a
formal implication from the static contracted packets to a nonzero
Macaulay dual.  A positive proof must first construct the missing
source-faithful chain map; it cannot infer that map from the coincidence
of the number five in the two gradings.

Uniformly, a binary clean coordinate has parameter degree \(h\).  The
rootless Macaulay step asks whether the multiplication map

\[
 \operatorname {span}({\cal E})\otimes
       \operatorname {Sym}^{h-1}\mathbb C^2
       \longrightarrow\operatorname {Sym}^{2h-1}\mathbb C^2            \tag{30}
\]

is surjective, or dually for one common nonzero functional annihilating
its image.  Equations (10c)--(10f) live in site degree \(2h-1\), but do not
define (30).  This is the exact point at which the missing
\(\operatorname {Sym}^{h-1}\)-prolongation enters.  For \(h=3\), (30)
reduces to the six-column matrix tested in (28)--(29).

## 6. Exact scope

The positive theorem is (4L)--(6): the full left-kernel rectangle and its
right-kernel companion give all three target labels on the target-centred
cross, but force only an explicit selector colon class.  The negative
statement is sharp in three ways:

1. the guard is site-minimal;
2. \(T_{\{e,a\}}\) is invertible and both crossed weights are nonzero; and
3. 26 of the 27 literal rows hold, with the sole invisible residual
   \(E_{bea}\).

The guard is not a complete full-source counterexample, precisely because
of (23).  It therefore leaves open a positive argument using the missing
\((b,e,a)\) row and its companions.  It proves that complementary kernel
anchors, noncoordinate right kernels, selected nonzero curvature, and the
other 26 rows cannot replace that input.  After the filtered row is
restored, the common degree-two Macaulay prolongation is still an
additional theorem.

The dependency-free
[checker](../computations/verify_complementary_kernel_colon_single_row_guard.py)
audits the rank-two kernels, the generic selector square, the selected
curvature, both literal contraction tables, all 27 uncontracted residuals,
the sharp colon calculation (25), the weighted missing row (26), and the
rank-six formal Macaulay test (29), all over exact rational arithmetic.
