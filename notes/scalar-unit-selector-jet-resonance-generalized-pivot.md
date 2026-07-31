# Scalar-unit selectors isolate radial resonance, but target jets need not gauge to a pivot

## 1. Outcome

Work at a good physical pair \(p,q\) of an exact ternary aggregate source,
in its intrinsic scalar-unit chart on \(2h\) residual sites, \(h\geq3\),
with

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0.                                      \tag{1}
\]

Put

\[
 Q=q^{[h]},\qquad D=\operatorname {span}\{X_0,X_1,X_2\},
 \qquad G=\alpha q+R_{aa},                                \tag{2}
\]

and remain on the clean unary branch

\[
 G^{[h]}=\alpha^{h-1}X_a.                                 \tag{3}
\]

As in the full normal-jet ledger, set

\[
 \Theta_a=G^{[h-1]}-\alpha^{h-1}q^{[h-1]},\qquad
 Z_{jk}=R_{jk}\Theta_a \quad(j,k\ne a).                   \tag{4}
\]

If, additionally, the ambient source maximizes the anchor potential \(\nu\)
among all exact sources of this fixed order, the global pivot theorem says
that the complementary \(2\)-by-\(2\) packet \(Z=(Z_{jk})\) is nonzero: if
all four entries vanished, (3) and the complementary pivot would give an
exact same-order descendant with one more mutual coordinate anchor.  This
maximum-\(\nu\) hypothesis is not supplied by the known minimum-entry-support
selection; every use of maximality below is conditional on the good
scalar-unit chart occurring on that representative.  The purpose of this
note is to determine exactly what the source-provenant top selectors can see
in this surviving packet and what target-valued blindness does and does not
buy.

Let \({\cal T}\) be the residual top coefficient space.  For a label \(i\),
define the affine selector family

\[
 {\cal A}_i(Q)=\{\nu\in{\cal T}^*:
      \nu(Q)=0,\ \nu(X_j)=\delta_{ij}\ (0\leq j\leq2)\}.  \tag{5}
\]

Every member is source-provenant: it is a finite linear combination of
literal top-word coefficient restrictions, and

\[
 \lambda_{i,\nu}(z)=\nu\bigl(zq^{[h-1]}\bigr)             \tag{6}
\]

has the exact response values

\[
 \lambda_{i,\nu}(q)=0,\qquad
 \lambda_{i,\nu}(R_{jk})=\delta_{ij}\delta_{ik}.          \tag{7}
\]

The complete selector result is as follows.

> **Theorem 1.1 (affine selectors and sharp resonance).**
>
> 1. If \(Q\notin D\), every label is admissible and
>    \({\cal A}_i(Q)\) is an affine translate of
>    \((D+\mathbb CQ)^\perp\).  A top vector \(Z\) is missed by every
>    selector in every label family if and only if
>    \[
>                              Z\in\mathbb CQ.             \tag{8}
>    \]
> 2. If \(Q=\sum_rv_rX_r\in D\), the admissible labels are exactly
>    \[
>                         I=\{i:v_i=0\}.                   \tag{9}
>    \]
>    If \(I\ne\varnothing\), a top vector \(Z\) is missed by every
>    admissible selector if and only if
>    \[
>        Z\in E_Q:=\operatorname {span}\{X_r:v_r\ne0\}.   \tag{10}
>    \]
>    In particular the joint blind space is already target-valued.  For
>    \(Q=0\) it is zero.  If \(I=\varnothing\), there is no selector
>    family, but the radial target-lock theorem has already produced the
>    raw order descent; within \(D\), the vacuous blind space is \(D\).

Thus, whenever an admissible family exists, a specified surviving jet has
the exact alternative

\[
 \boxed{
 \text{some source-provenant }\nu_i\text{ detects }Z_{jk}
 \quad\text{or}\quad
 \begin{cases}
 Z_{jk}\in\mathbb CQ,&Q\notin D,\\
 Z_{jk}\in E_Q,&Q\in D,\ I\ne\varnothing.
 \end{cases}}                                             \tag{11}
\]

If \(Q\in D\) has full target support, then \(I=\varnothing\), the common
blind space in the whole top space is vacuously \({\cal T}\), and (11) is
replaced by the already available raw order descent.  It is not legitimate
to infer \(Z_{jk}\in D=E_Q\) from an empty selector family.

Both alternatives are sharp.  In the transverse case, failure of all
selector detection really does force the proposed radial resonance
\(Z_{jk}\in\mathbb CQ\).  Moreover, if that jet is also target-only, then

\[
 Q\notin D,\quad Z_{jk}\in D,\quad
 \nu(Z_{jk})=0\ \text{for all admissible }\nu
 \quad\Longrightarrow\quad Z_{jk}=0.                     \tag{12}
\]

In the target case (10) cannot generally be sharpened to
\(\mathbb CQ\): when \(Q=X_b+X_c\), the only admissible label is \(a\),
and the whole plane \(\operatorname {span}\{X_b,X_c\}\), including
\(X_b-X_c\), is invisible.

There is also an exact answer to the proposed generalized pivot.  After
the basic internal replacement \(q^\sharp=\alpha^{-1}G\) and deletion of
the selected star rows, write the target-only complementary response as

\[
 T_{jk}=R_{jk}(q^\sharp)^{[h-1]}
       =\delta_{jk}X_j+\alpha^{1-h}Z_{jk}
       =\sum_{\ell=0}^2(A_\ell)_{jk}X_\ell.               \tag{13}
\]

Index every \(A_\ell\) by the ordered complementary labels \(b,c\).
There are endpoint row changes \(L,R\in GL_2\) which make (13) exactly the
two complementary target rows if and only if

\[
 \boxed{
 A_a=0,\qquad
 \operatorname {rank}A_b=\operatorname {rank}A_c=1,
 \qquad \det(A_b+A_c)\ne0.}                              \tag{14}
\]

With \(A_a=0\) understood, the remaining conditions are equivalently

\[
                    \det(xA_b+yA_c)=\kappa xy,
                    \qquad\kappa\ne0.                    \tag{15}
\]

Target-preserving monomial gauges do not weaken (14).  They only permute
and rescale the three coefficient matrices, so their ranks and the
root-multiplicity type of the pencil determinant are invariant.

Condition (14) is not forced by selector blindness or by target-onlyness.
There is an explicit packet-level guard with \(Q=X_b\) in which every
available selector misses every jet entry, the jet coefficient matrix even
has rank one, but \(A_b\) has rank two.  Hence neither endpoint \(GL_2\)
nor any monomial target gauge can absorb it.  This is a rigorous no-go for
the target-only inference, not a physical Krenn counterexample.

The stricter criterion for normalization by monomial endpoint matrices
alone is

\[
 A_a=0,\qquad
 A_b=\rho_bE_{r_b c_b},\qquad
 A_c=\rho_cE_{r_c c_c},                                  \tag{16}
\]

where \(\rho_b\rho_c\ne0\), \(r_b\ne r_c\), and \(c_b\ne c_c\).
But this smaller condition is not needed for the global potential.
A basis-free split-anchor lemma shows that exactness converts every old
anchor transported by dense endpoint \(GL_2\) matrices back into a
distinct monochromatic coordinate anchor.  Consequently every *actual*
packet satisfying (14) gives an exact generalized pivot with

\[
                         \nu(A^\sharp)\geq\nu(A)+1.       \tag{16a}
\]

It is excluded at a maximum-\(\nu\) representative whether or not its
normalizing matrices are monomial.  Dense row mixing can lower the visible
coordinate-anchor count before exactness is imposed; that raw incidence
phenomenon does not survive in an exact final source.

Consequently, on the maximum-\(\nu\) clean branch, a target-only surviving
packet in the transverse case \(Q\notin D\) must be detected by some
selector: complete blindness would make every entry zero by (12).  In the
target case \(Q\in D\) with \(I\ne\varnothing\), complete blindness places
every entry in \(E_Q\); the resulting coefficient triple must then fail
(14), or the exact generalized pivot would contradict maximality.  When
\(I=\varnothing\), the selector statement is replaced by the raw descent
above.

The result narrows the clean branch but does not close it: selector
detection remains a top-coefficient statement, radial/target resonance can
survive, and a target packet failing (14) needs an additional source-level
identity before either the four-cut transgression or a generalized pivot
can finish the argument.

## 2. The affine selector torsors

Let \(\pi_Y\) denote the literal coefficient restriction at a standard top
word \(Y\); in particular write \(\pi_i=\pi_{X_i}\).  All functionals on
\({\cal T}\) are finite linear combinations of these restrictions.

Suppose first that \(Q\notin D\).  Choose a top word
\(Y\notin\{X_0,X_1,X_2\}\) with \(\pi_Y(Q)\ne0\).  For every label \(i\),

\[
 \nu_i^Y=\pi_i-\frac{\pi_i(Q)}{\pi_Y(Q)}\pi_Y             \tag{17}
\]

belongs to \({\cal A}_i(Q)\).  Two members of (5) have the same values on
\(D+\mathbb CQ\), and their difference therefore annihilates that space.
Conversely, adding any such annihilator preserves all four prescribed
values.  Thus

\[
 \boxed{{\cal A}_i(Q)=\nu_i^Y+(D+\mathbb CQ)^\perp}
 \qquad(Q\notin D).                                      \tag{18}
\]

The choice of \(Y\) changes only the displayed base point, not the affine
family.

Now suppose \(Q=\sum_rv_rX_r\in D\).  Every functional with the three
target values in (5) necessarily has \(\nu(Q)=v_i\).  Hence (5) is
consistent exactly when \(v_i=0\), and then

\[
 \boxed{{\cal A}_i(Q)=\pi_i+D^\perp}
 \qquad(Q\in D,\ v_i=0).                                 \tag{19}
\]

This proves the existence and affine-family assertions without extending
a functional from the quadratic response quotient.  Applying (1) after
literal multiplication by \(q^{[h-1]}\) proves (7), exactly as in the
full-nine target-lock note.

## 3. The common blind spaces

The following elementary affine-duality lemma contains the whole
detection argument.

**Lemma 3.1.**  Let \(S\subseteq V\), let
\(\ell\in S^*\), and let

\[
                    {\cal F}=\{f\in V^*:f|_S=\ell\}.      \tag{20}
\]

Then

\[
                    \bigcap_{f\in{\cal F}}\ker f
                         =\ker\ell\subseteq S.            \tag{21}
\]

**Proof.**  Every extension has the form \(f_0+\eta\), with
\(\eta\in S^\perp\).  If \(z\notin S\), some \(\eta\in S^\perp\) has
\(\eta(z)\ne0\), so the affine line \(f_0+t\eta\) detects \(z\) for all
but at most one \(t\).  If \(z\in S\), every extension takes the common
value \(\ell(z)\).  This is zero exactly on \(\ker\ell\). \(\square\)

For \(Q\notin D\), take \(S=D\oplus\mathbb CQ\).  The fixed restriction of
\({\cal A}_i(Q)\) sends \(X_i\) to one and kills \(Q\) and the other two
target words.  Lemma 3.1 gives the single-label blind space

\[
 B_i=\bigcap_{\nu\in{\cal A}_i(Q)}\ker\nu
     =\operatorname {span}\bigl(\{Q\}\cup
          \{X_j:j\ne i\}\bigr).                          \tag{22}
\]

Intersecting (22) over all three labels kills every \(D\)-coordinate and
leaves exactly \(\mathbb CQ\), proving (8).

For \(Q\in D\) and \(i\in I\), use \(S=D\) and
\(\ell=\pi_i|_D\).  Then

\[
 B_i=\operatorname {span}\{X_j:j\ne i\}.                 \tag{23}
\]

Intersecting over the zero-coordinate labels imposes exactly those target
coordinates to be zero:

\[
             \bigcap_{i\in I}B_i
               =\operatorname {span}\{X_r:r\notin I\}
               =E_Q.                                     \tag{24}
\]

Equations (22)--(24) prove both directions of the alternatives, including
sharpness: every vector in the displayed resonance space is genuinely
missed by the whole affine family, not merely by one convenient selector.

The statement applies entrywise to the complementary packet.  Thus if no
pair \((i,\nu)\), with \(i\) admissible and
\(\nu\in{\cal A}_i(Q)\), detects any \(Z_{jk}\), then every packet entry
lies in (8) or (10).  In the transverse case
\(\mathbb CQ\cap D=0\), which proves (12).

No lower comparison is hidden here.  The number
\(\nu(R_{jk}\Theta_a)\) is a legal linear combination of literal top
coefficients, but (21) neither cancels a matching power nor constructs a
functional on \(R_{jk}H_a\) before top degree.  The four-cut
transgression problem from the normal-jet ledger remains separate.

## 4. The transformed complementary packet

Let \(C=\{b,c\}=\{0,1,2\}\setminus\{a\}\).  From (3), the basic internal
pivot

\[
                       q^\sharp=\alpha^{-1}G              \tag{25}
\]

satisfies \(\alpha(q^\sharp)^{[h]}=X_a\).  The adjacent-power identity is

\[
 (q^\sharp)^{[h-1]}
   =q^{[h-1]}+\alpha^{1-h}\Theta_a.                       \tag{26}
\]

Multiplying by \(R_{jk}\), \(j,k\in C\), gives (13).  If all \(Z_{jk}\)
are target-valued, write

\[
 \alpha^{1-h}Z_{jk}=\sum_{\ell=0}^2
                          z_{jk}^{(\ell)}X_\ell.          \tag{27}
\]

Then, in the \(b,c\) row and column order,

\[
 A_a=(z_{jk}^{(a)}),\qquad
 A_b=E_{bb}+(z_{jk}^{(b)}),\qquad
 A_c=E_{cc}+(z_{jk}^{(c)}).                               \tag{28}
\]

Replace the surviving endpoint rows by

\[
 \widetilde p_r=\sum_{j\in C}L_{rj}p_j,\qquad
 \widetilde s_r=\sum_{k\in C}R_{rk}s_k.                  \tag{29}
\]

The coefficient matrices in (13) transform simultaneously as

\[
                         A_\ell\longmapsto LA_\ell R^{\mathsf T}.
                                                                    \tag{30}
\]

The selected rows remain zero, the direct \(aa\)-cell is unchanged, and
the source is exact precisely when (30) is zero for \(\ell=a\) and the
two complementary matrices are the two diagonal matrix units.  Thus the
question is simultaneous left-right equivalence of a matrix pair, not
individual diagonalization of four target vectors.

This is exactly the endpoint-\(GL_2\)/monomial-gauge question: the direct
block remains the scalar unit.  If one also allowed an additive
complementary direct block, its product with
\((q^\sharp)^{[h]}=\alpha^{-1}X_a\) could cancel \(A_aX_a\).  That is a
different source surgery, not a gauge; it changes the direct block and its
support ledger.  The criterion below deliberately does not claim to
classify that broader operation.

## 5. Exact \(GL_2\)-absorption criterion

**Theorem 5.1.**  There are \(L,R\in GL_2(\mathbb C)\) such that

\[
 LA_aR^{\mathsf T}=0,\qquad
 LA_bR^{\mathsf T}=E_{bb},\qquad
 LA_cR^{\mathsf T}=E_{cc}                                \tag{31}
\]

if and only if (14) holds.  Permuting or nonzero-rescaling the two final
target rows gives the same criterion.

**Proof.**  Left and right multiplication by invertible matrices preserves
zero and rank.  It also preserves whether the column lines of two rank-one
matrices coincide and whether their row lines coincide.  The canonical
pair consists of two nonzero rank-one matrices with distinct column and
row lines, so (14) is necessary.

Conversely, factor

\[
                       A_b=u_bv_b^{\mathsf T},\qquad
                       A_c=u_cv_c^{\mathsf T}.             \tag{32}
\]

For rank-one matrices,

\[
 \det(A_b+A_c)\ne0
 \quad\Longleftrightarrow\quad
 (u_b,u_c)\text{ and }(v_b,v_c)\text{ are both bases}.    \tag{33}
\]

Let \(U=(u_b\ u_c)\), \(V=(v_b\ v_c)\), and take
\(L=U^{-1}\), \(R=V^{-1}\).  Equations (32) give (31).  This also proves
the determinant-pencil formulation (15). \(\square\)

A genuine target-stabilizer gauge cannot rescue a failure of (14).  On a
GHZ target with at least three physical sites, local stabilizers are
monomial.  Indeed, flatten at one site.  In the resulting span of the
remaining constant-colour words, the only decomposable tensor lines are
the coordinate lines; uniqueness forces every local map to permute those
lines consistently.  The finite part is therefore one common colour
permutation, while the diagonal part supplies balanced nonzero rescalings.
Such operations permute/rescale the \(A_\ell\); in particular they preserve
their ranks.  Even if one formally allowed a full third \(GL_2\) mixing
\(X_b,X_c\), the multiplicity pattern of the roots of
\(\det(xA_b+yA_c)\) would remain invariant under a projective change of
\([x:y]\).

The endpoint changes in Theorem 5.1 should therefore be called a row
rewrite, not automatically a target gauge.  They produce an exact source
because (31) is checked directly.  Their invertibility retains the two
surviving rank-two endpoint star maps and the essential selected direct
line.  Invertibility alone says nothing about coordinate support; exactness
of the final source supplies the basis-free anchor recovery proved next.

## 6. Exactness restores the anchor potential after every \(GL_2\) rewrite

The monomial criterion itself is elementary.  An invertible monomial
\(2\)-by-\(2\) matrix only permutes and rescales coordinate rows.  Hence
(31) can be achieved with monomial \(L,R\) exactly when (16) holds: the
two nonzero matrix units must use different row and column indices.

Dense matrices need a basis-free replacement for literal coordinate
anchors.  Let \(u,v\) be physical sites.  Call a nonzero rank-one summand
\(c\,x_u\otimes x_v\) of \(A_{uv}\) a **one-dimensional split edge
summand** if there are decompositions

\[
 V_u=L_u\oplus K_u,\qquad V_v=L_v\oplus K_v,\qquad
 L_u=\mathbb Cx_u,\quad L_v=\mathbb Cx_v,                 \tag{34}
\]

such that

\[
 \begin{aligned}
 A_{uv}-c\,x_u\otimes x_v&\in K_u\otimes K_v,\\
 A_{uw}&\in K_u\otimes V_w &&(w\ne u,v),\\
 A_{vw}&\in K_v\otimes V_w &&(w\ne u,v),
 \end{aligned}                                           \tag{35}
\]

with tensor order restored when the named endpoint is second.  This says
that the two displayed one-dimensional channels meet only each other, but
it does not assume that either line is a coordinate axis.

**Lemma 6.1 (exact split anchors are coordinate anchors).**  Let
\(|B|\geq4\), and suppose \(H_B(A)=\Delta_{B,3}\).  Every
one-dimensional split edge summand is a monochromatic mutual coordinate
anchor.  Conversely, every mutual coordinate anchor is a one-dimensional
split edge summand (the converse does not require exactness).

**Proof.**  Choose \(\phi\in V_u^*\) with
\(\ker\phi=K_u\) and \(\phi(x_u)=1\).  In the contraction of the matching
tensor at \(u\), every matching in which \(u\) is paired away from \(v\)
is killed by (35).  Hence, with \(W=B\setminus\{u,v\}\),

\[
 (\phi\otimes1)H_B(A)
       =c\,x_v\otimes H_W(A)
       =\sum_{i=0}^2\phi(e_i)e_i^{(v)}\otimes X_i^W.      \tag{36}
\]

The right side is nonzero because \(\phi\ne0\) and the one-site flattening
of \(\Delta_{B,3}\) is injective.  Since \(c\ne0\) and \(x_v\ne0\), the
equality also gives \(H_W(A)\ne0\).  Across the cut \(v\mid W\), the middle
term therefore has rank exactly one.  The rightmost term has rank equal to
the number of nonzero scalars \(\phi(e_i)\), since both the
\(e_i^{(v)}\) and, for \(|W|\geq2\), the \(X_i^W\) are independent.
Exactly one \(\phi(e_r)\) is therefore nonzero.  Thus

\[
                  \phi\in\mathbb C^*e_r^*,\qquad
                  K_u=\operatorname {span}\{e_i:i\ne r\},
                  \qquad x_v\in\mathbb C^*e_r.           \tag{37}
\]

Now choose \(\psi\in V_v^*\) with
\(\ker\psi=K_v\) and \(\psi(x_v)=1\), and contract at \(v\).
The symmetric rank-one argument makes \(\psi\) a nonzero coordinate
covector and \(x_u\) the corresponding coordinate vector.  Since
\(\psi(x_v)\ne0\) and \(x_v\) lies on the \(r\)-axis, that coordinate is
again \(r\).  Thus \(L_u=L_v=\mathbb Ce_r\) and both complementary planes
are the spans of the other two coordinate axes.  Equations (34)--(35)
then say exactly that the nonzero \(rr\)-cell on \(uv\) is the only cell
incident to either \((u,r)\) or \((v,r)\).  Conversely, for a mutual
coordinate anchor on the \(rr\)-cell, take \(L_u=L_v=\mathbb Ce_r\) and
take both \(K\)'s to be the spans of the other two coordinate axes.  The
degree-one condition gives (35), so the cell is a split summand. \(\square\)

Return to the generalized pivot.  Before applying \(L,R\), the structural
anchor-persistence argument for the basic pivot (25) preserves every old
mutual coordinate anchor and creates the new direct anchor

\[
                         (p,a)\mathbin{---}(q,a).          \tag{38}
\]

Goodness makes both selected star rows nonzero before the pivot, so (38)
was not already a mutual anchor; after those rows are deleted, it is the
only cell incident to either selected coordinate.  Apply the local maps
\(\operatorname {diag}(1,L)\) at \(p\) and
\(\operatorname {diag}(1,R)\) at \(q\), with the selected coordinate
listed first.  Every preserved anchor is transported injectively to a
one-dimensional split edge summand; anchors away from \(p,q\) are
unchanged, and (38) is fixed.  If (14) holds, Theorem 5.1 says that the
final source is exact.  Lemma 6.1 then turns every transported split
summand back into a mutual coordinate anchor.  At each endpoint, distinct
old anchor lines remain distinct under the invertible local map; physical
edges and all anchors away from \(p,q\) are unchanged.  No old anchor used
either selected coordinate, so the recovered old anchors and (38) are all
distinct.  Consequently

\[
                         \boxed{\nu(A^\sharp)\geq\nu(A)+1}.\tag{39}
\]

Thus every actual \(GL_2\)-absorbable packet, not merely a monomial one,
is excluded at a maximum-\(\nu\) exact representative.  No inequality for
\(\nu\) is asserted for the transformed packet before exactness is checked.

There is a useful guard on the role of exactness.  Start with two visible
coordinate anchors \(p_b=e_u\), \(p_c=e_v\) and apply the dense matrix

\[
                 L=\begin{pmatrix}1&1\\1&-1\end{pmatrix}.\tag{40}
\]

In the raw coordinate support graph the two transformed split lines each
use both \(p\)-coordinates, so the two visible coordinate anchors
disappear.  This is only a pre-exactness incidence model.  If the
transformed tensor were an exact source, Lemma 6.1 would force both split
lines to be coordinate lines and recover the anchors.  Hence the raw
example explains why literal support persistence is unavailable for dense
matrices; it is not a counterexample to (39).

## 7. Two sharp packet guards

The following guards live only at the algebraic top-response packet level
(13).  The first physical constraint they omit is simultaneous realization
by one actual site-square-zero tuple \(q,p_i,s_j\) and one common carrier
\(H_a\), with

\[
 Z_{jk}=R_{jk}\Theta_a=R_{ja}R_{ak}H_a,                  \tag{41}
\]

while those same rows satisfy all nine equations (1) and the clean unary
equation (3).  Rank one of one target coefficient matrix is not such a
common-carrier realization.  The guards are therefore not claimed to
realize a physical exact source or even the whole pre-top normal-jet
ledger.

First take \(Q=X_b\).  Then \(I=\{a,c\}\), and (24) says that every
admissible selector kills every multiple of \(X_b\).  In the \(b,c\)
packet order put

\[
 (z_{jk}^{(b)})=
 W:=\begin{pmatrix}-1&1\\1&-1\end{pmatrix},\qquad
 (z_{jk}^{(a)})=(z_{jk}^{(c)})=0.                         \tag{42}
\]

Equivalently, \(\alpha^{1-h}Z_{jk}=W_{jk}X_b\).  The jet
coefficient matrix \(W\) has rank one, but the corrected target matrices
are

\[
 A_a=0,\qquad
 A_b=\begin{pmatrix}0&1\\1&-1\end{pmatrix},\qquad
 A_c=\begin{pmatrix}0&0\\0&1\end{pmatrix}.               \tag{43}
\]

Thus \(\operatorname {rank}A_b=2\), which violates (14).  More strongly,

\[
                         \det(xA_b+yA_c)=-x^2,             \tag{44}
\]

whereas the exact complementary target has determinant \(xy\).  The
double root in (44) cannot be changed into two distinct roots even by a
formal \(GL_2\) change of the target pencil.  This is the promised
selector-blind, target-only, nonabsorbable guard.  Since \(W\) itself is
rank one, imposing a rank-one bilinear coefficient slice on the jet would
not remove it.

For the opposite boundary, take \(Q=X_b+X_c\), so \(I=\{a\}\) and every
target vector in \(\operatorname {span}\{X_b,X_c\}\) is selector-blind.
Set

\[
 A_a=0,\qquad
 A_b=\begin{pmatrix}1&0\\1&0\end{pmatrix},\qquad
 A_c=\begin{pmatrix}0&1\\0&-1\end{pmatrix}.              \tag{45}
\]

These matrices are transverse rank one, and

\[
 L={1\over2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},
 \qquad R=I_2                                             \tag{46}
\]

sends them to \(E_{bb},E_{cc}\).  Thus a genuine \(GL_2\) generalized
pivot can exist in the blind target plane.  Neither matrix in (45) is a
scalar matrix unit, so no monomial endpoint normalization exists.  This
guard shows that selector blindness does not obstruct an exact dense
row-rewrite pivot.  Any physical realization would still raise the anchor
potential by Lemma 6.1.

Together (42)--(46) show that the exact blind space (10) is the end of the
selector argument.  Inside it, both absorbable and nonabsorbable packets
occur at the top-response level.

## 8. Scope and audit

The affine selector theorem uses only finite-dimensional duality, the
literal coefficient basis, and the full-nine multiplication table.  The
clean condition is used to identify the surviving first-jet packet and to
write the transformed response (13).  Goodness is used to make the direct
anchor new and to retain the two complementary endpoint ranks.  Maximum-anchor
extremality is used only to ensure that this packet cannot vanish and,
through Lemma 6.1, to exclude every absorbable generalized pivot satisfying
(14).

The \(GL_2\) theorem is a complete simultaneous-equivalence classification
for a target-only \(2\)-by-\(2\) packet.  It does not say that an arbitrary
packet guard satisfies the first omitted simultaneous physical constraint
(41), or that it is realized by a physical exact source.  Conversely, if an
actual source produces matrices satisfying (14), equations (25)--(31)
are a literal exact source construction, not a heuristic gauge argument.

The dependency-free
[checker](../computations/verify_scalar_unit_selector_jet_resonance_generalized_pivot.py)
solves the affine selector constraints by exact rational row reduction,
computes every stated blind space, audits the transverse and target
regimes including \(Q=0\), verifies the \(GL_2\) normalizer and monomial
criterion, checks both packet guards, the determinant-pencil invariant, and
the \(\alpha^{1-h}\) adjacent-power scaling, and confirms both the
split-anchor flattening rank test and the pre-exactness anchor-loss incidence
example.  It uses explicit runtime failures throughout and remains active
under `python -O`.

This is a sharp continuation of the selector and pivot ledgers.  It does not
transport the known minimum-entry-support scalar-unit pair to a maximum-
\(\nu\) source or prove that one representative has both properties.  It is
not a cofactor-to-four-cut transgression, a recurrence theorem for arbitrary
exact \(GL_2\) rewrites, an order descent, or a proof of Krenn's conjecture.
