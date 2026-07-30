# The target-centred cross descends to two suspended anchor packets

## 1. Outcome

Work at the first \(8\to6\) boundary in the two literal charts \(pq\)
and \(pr\).  Let

\[
 d=A_{pq},\qquad d'=A_{pr},
\]

and suppose the rank-two, same-target alignment residue has the common
left kernel

\[
 \ker d^{\mathsf T}=\ker(d')^{\mathsf T}=\mathbb C\xi,
 \qquad \operatorname {supp}\xi=\{e,a\}.                 \tag{1}
\]

Write \(b\) for the third physical label.  The target-centred cross also
has right kernels

\[
 \ker d=\mathbb C\eta,\qquad
 \ker d'=\mathbb C\eta',\qquad
 \operatorname {supp}\eta,
 \operatorname {supp}\eta'\subseteq\{e,b\}.              \tag{2}
\]

The complete 27-row overlap has two canonical contractions which were not
visible in the support normal form alone.

1. Contracting the common left kernel gives a normalized \(qr\)-matrix
   packet on the five common sites:

   \[
    \boxed{
    x(\xi)\left(y_jt_k+{T_{jk}\over h-1}z\right)
       z^{[h-2]}=\delta_{jk}\xi_jX_j .}                    \tag{3}
   \]

   At \(h=3\), putting \(M=x(\xi)z\), this is

   \[
      M\left(y_jt_k+{T_{jk}\over2}z\right)
             =\delta_{jk}\xi_jX_j.                         \tag{4}
   \]

   Thus the target-centred support in (1) produces two differently
   labelled anchors \(X_e,X_a\), all six oriented off-diagonal zero
   rows separately, and a zero \((b,b)\) row.  In particular both the
   assignment sum and the Bianchi difference occur in the span of literal
   filtered rows after the same suspension \(M\).  This is stronger than
   merely adjoining one formal crossed-difference class.

2. Contracting the two right kernels gives the companion packet

   \[
    \boxed{
    x_i\left(y(\eta)t(\eta')
          +{\eta^{\mathsf T}T\eta'\over h-1}z\right)
       z^{[h-2]}=\eta_i\eta'_iX_i.}                         \tag{5}
   \]

   If both right kernels have full support \(\{e,b\}\), (5) supplies
   the two anchors \(X_e,X_b\).  Equations (3) and (5) then put **all
   three physical diagonal labels** into one literal overlap packet,
   before a common factor or divided power is cancelled.

There is also a one-chart three-anchor consequence.  When
\(\operatorname {supp}\eta=\{e,b\}\), the complete \(pq\) full-nine
system contains the exact L-shaped packet

\[
\begin{aligned}
 x(\xi)s_aq^{[2]}&=\xi_aX_a,\\
 x(\xi)s(\eta)q^{[2]}&=\xi_e\eta_eX_e,\\
 p_bs(\eta)q^{[2]}&=\eta_bX_b.                              \tag{6}
\end{aligned}
\]

Thus the generic target-centred cross is not an unstructured matrix-pair
case.  It canonically routes to a full-label, multi-anchor overlap problem.

This is still not a proof of the conjecture.  Every row in (3) retains the
common factor \(x(\xi)z^{[h-2]}\), and every row in (5) retains its own
displayed common factor.  The equations do not license cancellation of
either.  At \(h=3\), the generic invertible \(2\times2\) \(\{e,a\}\)
compression of \(T=A_{qr}\) has two coprime anchor-response forms and one
unavoidable weighted crossed-difference annihilator.  Hence the contracted
packet alone does not manufacture a Macaulay root.  A sharp physical block
guard below also shows that the already selected curvature
\(AU-BF\ne0\) does not force that \(T\)-compression to be singular or
triangular.  The remaining task is now the coefficient/colon step which
uses the simultaneous packets (3) and (5), not another alignment census.

## 2. Literal derivation from the 27 rows

Let \(D\) be the common complement of \(p,q,r\).  In the notation of the
[rank-two kernel-cap descent](rank-two-alignment-kernel-cap-descent.md),
write \(x_i,y_j,t_k\) for the three endpoint stars on \(D\), \(z\) for
the internal quadratic, and

\[
                         T=A_{qr}.
\]

The literal triple rows are, for every \(i,j,k\),

\[
 (d_{ij}t_k+d'_{ik}y_j+T_{jk}x_i)z^{[h-1]}
   +x_iy_jt_kz^{[h-2]}
       =\mathbf1_{i=j=k}X_i.                                \tag{7}
\]

No top-tensor reconstruction is being assumed here: (7) is one of the
automatic source rows supplied by the two-chart extraction theorem.

Put

\[
                         L=x(\xi)=\sum_i\xi_ix_i.
\]

Multiply (7) by \(\xi_i\) and sum over \(i\).  Both direct terms vanish
because

\[
                         \xi^{\mathsf T}d
                           =\xi^{\mathsf T}d'=0.             \tag{8}
\]

The remaining identity is

\[
 L T_{jk}z^{[h-1]}+Ly_jt_kz^{[h-2]}
                    =\delta_{jk}\xi_jX_j.                   \tag{9}
\]

Using only

\[
                         zz^{[h-2]}=(h-1)z^{[h-1]}
\]

gives (3).  In particular, for \(j\ne k\), the two endpoint
orientations are individually source-valid:

\[
 L\left(y_jt_k+{T_{jk}\over h-1}z\right)z^{[h-2]}=0.       \tag{10}
\]

Taking \((j,k)=(e,a)\) and \((a,e)\), both their sum and their difference
are therefore source-valid linear combinations of literal rows.  This is
the exact sense in which the
assignment-sum provenance obstruction is removed on the *suspended*
packet.  It does not say that either quadratic in parentheses annihilates
\(z^{[h-2]}\) without the factor \(L\).

For the second contraction, multiply (7) by \(\eta_j\eta'_k\) and sum
over \(j,k\).  Now

\[
                         d\eta=0,\qquad d'\eta'=0,            \tag{11}
\]

so both direct terms again disappear.  The response target survives only
when \(i=j=k\), and is then \(\eta_i\eta'_iX_i\).  This proves (5).
Notice that (5) uses the actual right kernels of the two different charts;
replacing either one by an abstractly conjugate line would destroy (11).

At \(h=3\), \(|D|=5\), and the two packets take the particularly concrete
form

\[
\begin{aligned}
 Lz\left(y_jt_k+\tfrac12T_{jk}z\right)
    &=\delta_{jk}\xi_jX_j,\\
 x_i z\left(y(\eta)t(\eta')
              +\tfrac12\eta^{\mathsf T}T\eta' z\right)
    &=\eta_i\eta'_iX_i.                                    \tag{12}
\end{aligned}
\]

These are top-degree identities on the five common sites.  The factor
\(1/2\) is forced by divided powers; it is not a normalization choice.

## 3. The coordinate-boundary ledger for the right kernels

There is no large support case split in (5).  A nonzero line contained in
\(\operatorname {span}(e_e,e_b)\) is either one of the two coordinate
lines or has both coordinates nonzero.

* If both \(\eta,\eta'\) are noncoordinate, (5) has the two anchors
  \(e,b\).  Together with (3), all three labels occur.
* If exactly one is coordinate and the other is noncoordinate, (5) has
  the single anchor at that coordinate.  The corresponding chart has a
  literal zero column.
* If both are the same coordinate line, the two direct blocks have the
  same literal zero column.  This is the previously isolated common-zero-
  column boundary.
* If they are the two distinct coordinate lines, the direct blocks have
  split zero columns and (5) is target-free:

  \[
   x_i\left(y_e t_b+{T_{eb}\over h-1}z\right)
                     z^{[h-2]}=0\qquad(i=0,1,2),             \tag{13}
  \]

  up to exchanging \(e,b\).  This is a three-row common-factor
  annihilator, not a contradiction.

Thus the only branch not carrying the generic all-three-anchor overlap is
already equipped with one or two literal zero columns and, in the split
case, the extra target-free packet (13).

## 4. The one-chart three-anchor L shape

Assume \(\eta_e\eta_b\ne0\).  On the \(pq\) chart the complete rows are

\[
 d_{ij}q^{[3]}+p_is_jq^{[2]}=\delta_{ij}X_i.               \tag{14}
\]

Contract (14), respectively, against

\[
               \xi e_a^{\mathsf T},\qquad
               \xi\eta^{\mathsf T},\qquad
               e_b\eta^{\mathsf T}.
\]

Each matrix is direct-zero by (8) or (11).  Their diagonal target
contractions are exactly the three equations (6).  The fourth corner is

\[
                 d_{ba}q^{[3]}+p_bs_aq^{[2]}=0.             \tag{15}
\]

Equivalently, the normalized \(2\times2\) response rectangle is

\[
 \begin{pmatrix}
   Ls_a&Ls(\eta)\\
   p_bs_a+\frac{d_{ba}}3q&p_bs(\eta)
 \end{pmatrix}q^{[2]}
 =\begin{pmatrix}
   \xi_aX_a&\xi_e\eta_eX_e\\
   0&\eta_bX_b
  \end{pmatrix}.                                           \tag{16}
\]

This uses all four literal corners, including the radial term in (15).
It also explains why the cross contains more information than its single
kernel cap \(Ls(\eta)q^{[2]}=\xi_e\eta_eX_e\).

The following elementary support consequence is sometimes useful.

**Lemma 4.1 (pure-factor site).**  Let \(W\) be a finite site set, let
\(R_W=\bigotimes_{x\in W}(\mathbb C\oplus V_x)\), and let
\(L=\sum_xL_x\in(R_W)_1\).  If

\[
                          LH=\lambda X_c,qquad\lambda\ne0, \tag{17}
\]

in top degree, then \(L_x\in\mathbb C^*e_c^{(x)}\) for some site \(x\).

**Proof.**  Quotient every \(V_x\) by the line \(\mathbb CL_x\) (with
the zero line allowed).  The image of \(LH\) is zero.  If no nonzero
\(L_x\) is proportional to \(e_c^{(x)}\), every factor of the pure tensor
\(X_c\) remains nonzero in its local quotient, so the image of \(X_c\)
is nonzero, a contradiction.  \(\square\)

Applying the lemma to (6) shows that \(L\) has distinct literal
\(e\)-pure and \(a\)-pure sites, while \(s(\eta)\) has distinct
\(e\)-pure and \(b\)-pure sites.  This is necessary incidence data; it
does not by itself make either cap dark at three sites.

## 5. What the rank-one selector conic still leaves

The common factor in (4) cannot be discarded merely because two anchors
are present.  Restrict (4) to the labels \((e,a)\), write

\[
 T_{\{e,a\},\{e,a\}}
     =\begin{pmatrix}A&B\\ C&D\end{pmatrix},
 \qquad \Delta=AD-BC,                                      \tag{18}
\]

and keep \(M=Lz\).  Parameterize a direct-zero rank-one selector by

\[
 u=(r,s),\qquad
 v=(-(Br+Ds),Ar+Cs).                                      \tag{19}
\]

Then \(u^{\mathsf T}Tv=0\) identically.  Put

\[
 y(u)t(v)=\rho_0r^2+\rho_1rs+\rho_2s^2.
\]

Direct expansion gives

\[
\begin{aligned}
 \rho_0&=Ay_et_a-By_et_e,\\
 \rho_1&=Cy_et_a-Dy_et_e-By_at_e+Ay_at_a,\\
 \rho_2&=Cy_at_a-Dy_at_e.                                  \tag{20}
\end{aligned}
\]

Since the selector is direct-zero, (4) gives

\[
\begin{aligned}
 M\,y(u)t(v)
   ={}&-\xi_e r(Br+Ds)X_e
       +\xi_a s(Ar+Cs)X_a.                                 \tag{21}
\end{aligned}
\]

For \(\Delta BC\ne0\), the two displayed anchor forms are coprime in
\(\mathbb C[r,s]\).  Indeed their four linear factors are

\[
                  r,\quad Br+Ds,\quad s,\quad Ar+Cs.       \tag{22}
\]

Here \(C\ne0\) prevents \(r\) from being proportional to \(Ar+Cs\),
\(B\ne0\) prevents \(Br+Ds\) from being proportional to \(s\), and
the two latter forms are proportional only when \(\Delta=0\).  This
also covers \(A=0\) or \(D=0\), when one of those forms is coordinate.
Thus the generic conic does not produce a common projective anchor root.

There is nevertheless a canonical third coefficient.  The exact identity

\[
 -CD\rho_0+BC\rho_1-AB\rho_2
      =\Delta\bigl(By_at_e-Cy_et_a\bigr)                    \tag{23}
\]

and (21) imply

\[
              M\bigl(By_at_e-Cy_et_a\bigr)=0
                 \qquad(\Delta\ne0).                       \tag{24}
\]

This is precisely the weighted crossed-orientation difference.  It is
also obtained without parameterization by taking

\[
 B\left(y_at_e+\tfrac C2z\right)
   -C\left(y_et_a+\tfrac B2z\right)                         \tag{25}
\]

in the two individual off-diagonal rows of (4); the radial terms cancel.
The corresponding weighted sum does not cancel them.  Hence the
factorized direct-zero conic still sees the familiar difference channel,
even though the *effective suspended packet* contains both orientations
separately.  Turning the latter into an unsuspended Macaulay relation is
exactly the remaining coefficient/colon issue.

When \(\Delta=0\) and \(T\) has rank one, (19) has a base point at the
left-kernel line of \(T\).  The common factor of the two polynomials in
(21) at that base point comes from \(v=0\), not automatically from a
nonzero selector.  The two rulings of a rank-one \(T\) must therefore be
treated as rulings; the rank-zero compression is still more degenerate,
and no false common root is claimed in either case.

## 6. A fixed-kernel incidence refinement

The common left kernel also reduces the alignment incidence without
choosing its right kernel.  For \(c\in\{e,a\}\), on the \(pq\) chart put

\[
 U_c^q=\{x:\xi^{\mathsf T}N^q_{x,c}=0\},
 \qquad N^q_{x,c}=P_x^{\mathsf T}J_cS_x.                   \tag{26}
\]

Every selector \(\xi v^{\mathsf T}\) is direct-zero.  Intersecting the
finitely many nonvanishing opens

\[
                    \xi^{\mathsf T}N^q_{x,c}v\ne0
                    \quad(x\notin U_c^q)
\]

with \(v_c\ne0\) gives a target-active selector whose blocked sites are
contained in \(U_c^q\).  Therefore the two-site blocked-target descent
implies

\[
 \boxed{\text{failure of every physical dark cut forces }
              |U_e^q|,|U_a^q|\ge3,}                         \tag{27}
\]

and similarly in the \(pr\) chart.

At a site in \(U_e^q\cap U_a^q\), put \(u=P_x\xi\).  Then

\[
                  \det(u,S_xv,e_e)=\det(u,S_xv,e_a)=0
                       \qquad(v\in\mathbb C^3).             \tag{28}
\]

Consequently one of the following holds:

\[
 \boxed{\quad u=0,\qquad \operatorname {rank}S_x\le1,
 \qquad\text{or}\qquad
 \operatorname {rank}S_x=2, 
 u\in\operatorname {im}S_x=\operatorname {span}(e_e,e_a).
 \quad}                                                     \tag{29}
\]

To prove (29), if \(u\ne0\), the cross-product map
\(v\mapsto u\times v\) sends \(\operatorname {im}S_x\) into the line
\(\mathbb Ce_b\).  A two-plane not containing \(u\) would map
injectively to a two-plane.  A two-plane containing \(u\) maps to its
normal line, which is \(\mathbb Ce_b\) exactly when the plane is
\(\operatorname {span}(e_e,e_a)\).  Rank three is impossible.

The opposite deleted endpoint belongs to both universal sets because
\(\xi^{\mathsf T}d'=0\) (or \(\xi^{\mathsf T}d=0\) on the other chart).
Thus, for each target separately, (27) leaves at least two further
universal sites on the five-site common complement.  It does not force
those two pairs of sites to intersect.  Equation (29) is a strict local
normal form, but the rank-one alternative shows why it is not yet a
contradiction.

## 7. Curvature does not constrain the generic \(T\)-block

The following integral physical block packet guards the exact scope of the
descent.  Relabel \((e,a,b)=(0,1,2)\), put

\[
 J_0=\begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix},
 \qquad
 P=\begin{pmatrix}1&0&0\\1&-1&0\\0&0&1\end{pmatrix},       \tag{30}
\]

and, for \(u\ne0\), let

\[
 S(u)=\begin{pmatrix}1&0&0\\-u&0&1\\0&1&0\end{pmatrix}.
                                                                    \tag{31}
\]

Then

\[
 d(u)=P^{\mathsf T}J_0S(u)
   =\begin{pmatrix}0&1&0\\0&-1&0\\u&0&-1\end{pmatrix}.     \tag{32}
\]

It has rank two, left kernel \((1,1,0)\), and right kernel
\((1,0,u)\).  Moreover

\[
             P(1,1,0)^{\mathsf T}=e_0,qquad
             S(u)(1,0,u)^{\mathsf T}=e_0.                   \tag{33}
\]

Thus, at one common site \(x\), taking \(S(u)\) and \(S(v)\) for the two
endpoint blocks realizes the target-centred nonzero alignments

\[
 P^{\mathsf T}J_0S(u)=d(u),\qquad
 P^{\mathsf T}J_0S(v)=d(v).                                \tag{34}
\]

All three local matrices are invertible.  Choose the curvature site
\(s\ne x\), and independently choose the direct \(qr\)-block

\[
 T=\begin{pmatrix}1&1&0\\1&2&0\\0&0&1\end{pmatrix}.        \tag{35}
\]

Its \(\{e,a\}\)-compression has \(\Delta=1\) and \(B=C=1\), exactly
the coprime case of Section 5.  The selected direct entries

\[
                         A=d(u)_{01}=1,qquad
                         B_0=d(v)_{01}=1                    \tag{36}
\]

can coexist with nonzero curvature: at the distinct site \(s\), take the
fourth label \(l=0\), set the literal entries
\(U_{10}=A_{rs}(1,0)=1\), \(F_{10}=A_{qs}(1,0)=0\), and obtain

\[
                         AU_{10}-B_0F_{10}=1.               \tag{37}
\]

Because these are literal physical blocks, the power-free connection,
normal, and Bianchi formulas hold as polynomial identities.  The
invertible blocks at \(x\) also make all four deleted endpoint-star maps
injective after this packet is embedded in the corresponding residual
stars.

The guard is **not** a full-nine GHZ source, is not asserted to extend to
any global source, and does not satisfy the target equations (3) or (5).
It proves only the needed independence statement:
selected curvature, goodness, same-target alignment, and the universal
overlap identities do not force the generic \(T\)-compression out of the
coprime case.  Any such conclusion must use the literal suspended target
rows derived above.

## 8. Exact stopping point

The target-centred cross has now been reduced without a support census:

* the generic noncoordinate branch carries all three labels through the
  two simultaneous suspended packets (3) and (5), and already has the
  three-anchor L shape (16) in either full-support chart;
* coordinate right kernels give literal zero columns, with the sole split
  alternative carrying the target-free three-row packet (13);
* the common left-kernel selector family forces the incidence bound (27)
  and the local plane form (29); and
* the generic \(qr\) compression still has the coprime response and the
  crossed-difference residue (21)--(25).

What is not proved is cancellation of \(x(\xi)z^{[h-2]}\), cancellation
of the companion factor in (5), or a common degree-five Macaulay
functional.  The next lemma should use a literal coefficient cut to make
one of the all-three-anchor rows survive modulo those common factors.  It
must use the target equations: the physical guard shows that curvature and
Bianchi alone cannot do it.

The dependency-free
[checker](../computations/verify_target_centred_cross_odd_overlap_descent.py)
audits both kernel contractions, the coordinate-boundary ledger, the
rank-one selector parameterization and crossed-difference identity, the
fixed-kernel intersection classification over finite fields, and the
integral curvature guard.
