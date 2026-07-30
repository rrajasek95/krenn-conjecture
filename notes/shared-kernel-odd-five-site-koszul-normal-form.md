# Shared kernels produce an odd five-site Koszul rectangle

## 1. Outcome

At the first \(8\to6\) pair boundary, expose a third endpoint.  Its common
complement \(D\) has five sites.  In the notation of the two-chart packet,
the complete 27 rows on \(D\) are

\[
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[2]}
       +x_i y_jt_kz=\mathbf1_{i=j=k}X_i .                 \tag{1}
\]

Suppose the two direct blocks \(P,R\) share a left kernel

\[
 \xi^{\mathsf T}P=\xi^{\mathsf T}R=0,\qquad
 L=x(\xi):=\sum_i\xi_i x_i.                                \tag{2}
\]

Contracting all of (1), not only its coordinate-kernel rows, gives

\[
 \boxed{
 L\left(y_jt_k+{T_{jk}\over2}z\right)z
       =\delta_{jk}\xi_jX_j
 \qquad(0\le j,k\le2).}                                    \tag{3}
\]

No factor \(L\) or \(z\) is cancelled.  If
\(I=\operatorname {supp}\xi\) has two elements, (3) is a literal
\(2\times2\) product rectangle with two differently labelled diagonal
anchors and both crossed zero rows.  The coordinate zero-row identities
in the alignment note are the \(|I|=1\) specialization of (3).

There is an exact quotient form.  In the five-site square-free algebra set

\[
 K_{L,z}=\operatorname {Ann}_2(Lz)
       =\{w\in{\cal A}_2(D):Lwz=0\}.                        \tag{4}
\]

For \(j\in I\), define

\[
 \gamma_j=\left[y_jt_j+{T_{jj}\over2}z\right]
       \in{\cal A}_2(D)/K_{L,z}.                            \tag{5}
\]

The \(\gamma_j\)'s are linearly independent and, for every matrix
\(H=(H_{jk})_{j,k\in I}\),

\[
 \boxed{
 \left[\sum_{j,k\in I}H_{jk}y_jt_k\right]
   =\sum_{j\in I}H_{jj}\gamma_j
      -{\langle H,T_I\rangle\over2}[z].}                   \tag{6}
\]

Thus every direct-zero selector \(\langle H,T_I\rangle=0\) has a literal
top realization after the one-hole map \(w\mapsto Lwz\).  For
\(I=\{e,a\}\), write

\[
 T_I=\begin{pmatrix}A&B\\ C&D\end{pmatrix},\qquad
 Y=(y_jt_k)_{j,k\in I},\qquad
 \omega_{T_I}(Y)=C\,Y_{ea}-B\,Y_{ae}.                      \tag{7}
\]

When \((B,C)\ne(0,0)\), this is the one-dimensional selector-family
provenance coordinate.  Equation (3) gives the exact kill-or-colon result

\[
 \boxed{\quad \omega_{T_I}(Y)\in K_{L,z}.\quad}            \tag{8}
\]

The selector covector in (7) is unique only up to scale.  Its physical
image may vanish; otherwise
\(\mathbb C\omega_{T_I}(Y)\) is an explicit one-dimensional lower-power
colon line.  The literal odd coefficient map kills that physical image,
but (8) does not license cancellation through the matching algebra.

If \(T_I\) is not supported on exactly one matrix cell, there are
\(u,v\in(\mathbb C^*)^I\) such that

\[
                         u^{\mathsf T}T_Iv=0.               \tag{9}
\]

The complete physical \(qr\)-chart contraction by \(uv^{\mathsf T}\) is
therefore a source-valid direct-zero rank-one cap whose target has every
label in \(I\) nonzero.  For \(|I|=2\) it is a binary scalar-zero cap.
The probe \(\xi\) is cap-dark at the exposed site \(p\), while both target
factors remain visible there.  If \(T_I\) is supported on one cell, no
torus rank-one selector can retain both diagonal target coefficients; this
is the exact complementary normal form.

For an invertible \(2\times2\) block, the isotropic Segre has a canonical
parametrization.  It identifies (8) with the third quadratic direction
missed by the two anchors.  It does not construct one common
\(\theta\in(\operatorname {Sym}^5\mathbb C^2)^*\) for the three
\(u^2,uv,v^2\) prolongations of a cubic clean error.  The unresolved
objects are precisely the possible nonzero physical colon line in (8) and
the missing chain map from a physical clean-error line to this odd
rectangle.

There is also a right-kernel companion.  If

\[
                  P\eta=0,\qquad R\eta'=0,                 \tag{10}
\]

then contraction of (1) in \(j,k\) gives

\[
 \boxed{
 x_i\left(y(\eta)t(\eta')
       +{\eta^{\mathsf T}T\eta'\over2}z\right)z
       =\eta_i\eta'_iX_i.}                                 \tag{11}
\]

Thus a noncoordinate common left kernel on \(\{e,a\}\) gives anchors
\(e,a\), while noncoordinate right kernels on \(\{e,b\}\) give anchors
\(e,b\).  On the target-centred cross the two packets jointly see all
three literal labels.  Converting that coverage into a common Macaulay
prolongation remains a separate gluing statement.

## 2. Derivation

Multiply (1) by \(\xi_i\) and sum over \(i\).  The \(P\)- and \(R\)-terms
vanish by (2), leaving

\[
 T_{jk}Lz^{[2]}+Ly_jt_kz=\delta_{jk}\xi_jX_j.              \tag{12}
\]

Since \(zz=2z^{[2]}\), equation (12) is (3).  Every term has site degree
five on \(D\); (3) was not obtained by dividing a six-site row by a common
power.  Contracting instead by \(\eta_j\eta'_k\) proves (11).

Let

\[
 m_{L,z}:{\cal A}_2(D)\longrightarrow{\cal A}_5(D),
 \qquad w\longmapsto Lwz.                                  \tag{13}
\]

Its kernel is (4), and (3) gives

\[
                         m_{L,z}(\gamma_j)=\xi_jX_j.        \tag{14}
\]

The \(X_j\)'s are independent and \(\xi_j\ne0\) for \(j\in I\), so the
\(\gamma_j\)'s are independent.  For \(j\ne k\), (3) says

\[
 \left[y_jt_k+{T_{jk}\over2}z\right]=0
              \quad\text{in }{\cal A}_2(D)/K_{L,z}.        \tag{15}
\]

Equations (5) and (15), summed with coefficients \(H_{jk}\), prove (6).
In particular, if \(\langle H,T_I\rangle=0\), applying \(m_{L,z}\) gives

\[
 L\left(\sum_{j,k\in I}H_{jk}y_jt_k\right)z
   =\sum_{j\in I}H_{jj}\xi_jX_j.                           \tag{16}
\]

No radial term remains and no common factor was cancelled.

For \(I=\{e,a\}\), the crossed cases of (15) are

\[
 [Y_{ea}]=-{B\over2}[z],\qquad
 [Y_{ae}]=-{C\over2}[z].                                   \tag{17}
\]

Multiply the first by \(C\), the second by \(B\), and subtract to obtain
(8).  Under entrywise pairing, the annihilator of

\[
 \Delta+\mathbb CT_I\subseteq\operatorname {Mat}_2         \tag{18}
\]

is the line \((0,C,-B,0)\) when \((B,C)\ne(0,0)\).  Thus (7)
is exactly the generic selector quotient, in the unchanged physical
labels.  We have proved the sharp alternative

\[
 \omega_{T_I}(Y)=0
 \quad\text{or}\quad
 0\ne\omega_{T_I}(Y)\in\operatorname {Ann}_2(Lz).          \tag{19}
\]

## 3. Rank-one direct-zero selectors

For \(|I|\ge2\), the Laurent polynomial
\[
                    F(u,v)=u^{\mathsf T}T_Iv               \tag{20}
\]
on the torus has one monomial for each nonzero cell of \(T_I\).  With no
monomials it is zero.  With at least two monomials, fix all but one ratio
generically and solve the remaining nonconstant linear equation; the
excluded zero coordinates form finitely many proper conditions.  With
exactly one monomial it never vanishes on the torus.  This proves (9) and
its one-cell exception.

Extend \(u,v\) by zero outside \(I\) and contract the complete \(qr\)
pair equations by \(H=uv^{\mathsf T}\).  The direct coefficient is zero,
the response is the product of the physical endpoint stars, and

\[
                              H_{jj}=u_jv_j\ne0\qquad(j\in I).
                                                                    \tag{21}
\]

At the exposed \(p\)-site the two cap factors are \(Pu\) and \(Rv\).
Both are annihilated by \(\xi^{\mathsf T}\), while all target labels in
\(I\) survive that probe.  Taking this coefficient of the cap equation
is exactly (16).

This cap is direct-zero.  For \(|I|=2\) it also misses the third ternary
target.  It is therefore not an active clean-pair cap; it is a physical
binary scalar-zero packet with one certified target-visible dark site.

For clarity, a nonzero singular rank-one \(2\times2\) block has the form
\(T_I=ab^{\mathsf T}\), and its isotropic locus is the union

\[
        (u^{\mathsf T}a)=0\quad\text{or}\quad(b^{\mathsf T}v)=0. \tag{21a}
\]

If the block has more than one nonzero cell, at least one of \(a,b\) has
two nonzero coordinates, so the corresponding ruling contains torus
points.  If the block has exactly one nonzero cell, neither ruling has a
point with all coordinates of both \(u,v\) nonzero.  For \(T_I=0\), every
torus pair is isotropic.  Thus the support criterion includes the
rank-one boundary exactly.  Formula (23) below is not a parametrization of
the singular union: at determinant zero it traces only one ruling (and
becomes the zero vector on the other), which is why Section 4 assumes
invertibility.

## 4. The invertible square and its third quadratic direction

Assume \(I=\{e,a\}\), use (7), and put

\[
                              \Delta_T=AD-BC\ne0.            \tag{22}
\]

The isotropic rank-one selectors are parametrized by

\[
 u(s,t)=\binom{s}{t},\qquad
 v(s,t)=\binom{-(Bs+Dt)}{As+Ct},                            \tag{23}
\]

for which \(u(s,t)^{\mathsf T}T_Iv(s,t)=0\).  Their two target
coefficients are

\[
 f_e=-Bs^2-Dst,\qquad f_a=Ast+Ct^2.                        \tag{24}
\]

When \((B,C)\ne(0,0)\), these are independent and their common
annihilator in the basis \((s^2,st,t^2)\) is

\[
                         \vartheta_2=(-DC,\ BC,\ -AB).      \tag{25}
\]

Expanding the physical product and applying (25) yields

\[
 \boxed{
 \vartheta_2\bigl(y(u)t(v)\bigr)
    =\Delta_T(BY_{ae}-CY_{ea})
    =-\Delta_T\,\omega_{T_I}(Y).}                          \tag{26}
\]

Thus the quadratic direction unseen by both anchors is exactly the
selector-provenance direction, and (8) sends it into the colon kernel.
This is the crossed-difference channel in the selector/Bianchi ledger.

If \(B=C=0\), both targets in (24) are multiples of \(st\); their
annihilator is two-dimensional, and
\(\operatorname {Mat}_2/(\Delta+\mathbb CT_I)\) has two off-diagonal
directions.  The one-scalar formula does not apply on this explicit
diagonal-square boundary.

## 5. Right-kernel packet and all-label coverage

Set

\[
 C_{\eta,\eta'}=y(\eta)t(\eta')
       +{\eta^{\mathsf T}T\eta'\over2}z,\qquad
 J=\operatorname {supp}\eta\cap\operatorname {supp}\eta'. \tag{27}
\]

Equation (11) says that multiplication by \(C_{\eta,\eta'}z\) kills
\(x_i\) for \(i\notin J\) and sends \(x_i\), \(i\in J\), to the nonzero
independent tensor \(\eta_i\eta'_iX_i\).  Hence the surviving classes
\([x_i]\), \(i\in J\), are independent modulo that multiplication
kernel.  The common coordinate zero-column formula is the stronger
specialization
\(\operatorname {supp}\eta=\operatorname {supp}\eta'=\{\rho\}\).
The condition \(J=\{\rho\}\) alone says only that this contraction has one
target anchor: the two kernel lines can still be noncoordinate, and
neither direct block need have a zero column.

On the target-centred cross, suppose

\[
 \operatorname {supp}\xi=\{e,a\},\qquad
 \operatorname {supp}\eta=\operatorname {supp}\eta'=\{e,b\},
 \qquad\{e,a,b\}=\{0,1,2\}.                                \tag{28}
\]

Then (3) anchors \(e,a\), while (11) anchors \(e,b\).  All three labels
occur in the same literal 27-row overlap, with the \(e\)-anchor shared.
This fixes the literal label bookkeeping on this subbranch, but it does
not prove that the left- and right-kernel packets share a flag or a common
Macaulay covector.  Converting the coverage into such a common
prolongation remains a separate gluing statement.

## 6. Why this is not yet a Macaulay functional

Equation (3) has site degree five in \({\cal A}(D)\).  The rootless
contradiction instead needs a functional of parameter degree five which
annihilates every cubic clean coordinate after the three shifts
\(u^2,uv,v^2\).  The covector \(\vartheta_2\) in (25) has parameter
degree two on the isotropic selector conic (23).  It neither defines a
functional on the six quintic monomials nor proves that the shifts of one
physical clean-error line factor through (3).

This is a type-and-provenance warning, not a proof that no degree-five
Macaulay functional exists.  It says only that the one-hole kernel
calculation has not constructed one.

The next positive statement must therefore be a gluing/prolongation lemma:
the same overlap must carry all three shifts of the clean cubic into the
left- and right-kernel packets with one common nonzero dual.  If
\(\omega_{T_I}(Y)=0\), the static selector obstruction is gone before
multiplication, but the prolongation is still needed.  If it is nonzero,
(19) names the single generic colon direction that the lemma must
eliminate.

In the language of the filtered Hessian-pullback criterion, (8) is a
lower one-hole torsion relation, not membership in the admitted top-source
row space.  A nonzero member of \(K_{L,z}\) cannot be declared
source-valid by cancelling \(Lz\).  Formula (26) also explains the match
with the cycle-mixing ledger: the two anchors control the two target
evaluations, while their remaining quadratic direction is precisely the
crossed-orientation difference.  More copies of that difference transport
the colon direction inside the colon module; they do not provide the
missing assignment-sum split or the three Macaulay shifts.

The dependency-free checker
[verify_shared_kernel_odd_five_site_koszul_normal_form.py](../computations/verify_shared_kernel_odd_five_site_koszul_normal_form.py)
audits (23)--(26), exhausts the generic selector quotient over a finite
field, tests the torus criterion on all small integral \(2\times2\)
blocks, and gives a five-site square-free example where the nonzero colon
direction in (19) is killed by \(Lz\).  That example is a
colon/cancellation guard, not a complete Krenn source.
