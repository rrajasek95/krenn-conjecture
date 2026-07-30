# Full missing-square caps reduce the nonzero-cross-block branch to one resonance

## 1. Outcome

Retain the double-hafnian-zero branch of the
[two-chart synchronization theorem](two-chart-hamming-one-gamma-synchronization.md),
and suppose that its pure-overlap alternative has selected the branch

\[
                              T\ne0,\qquad \chi=0.             \tag{1}
\]

Fix the \(pq\)-chart, write the pure colour as \(\delta\), and let

\[
                              M=\{\alpha,\beta\}
\]

be the other two physical labels.  Instead of retaining only the original
compression \(A\times B\subseteq M\times M\), use all four literal
full-nine rows indexed by \(M\times M\).  With residual sites \(r,s\), put

\[
\begin{aligned}
 C&=P_{M,M},\\
 H_{c,d}&=R_{M,c}Q_{M,d}^{\mathsf T},\\
 G_{c,d}&=E_{M,d}T_{M,c}^{\mathsf T},\\
 K_{c,d}&=U_{cd}C-H_{c,d}.
\end{aligned}                                                \tag{2}
\]

Here \(P=A_{pq},R=A_{pr},E=A_{ps},T=A_{qr},Q=A_{qs}\), and
\(U=A_{rs}\).  The matrix \(C\) is nonzero because it contains the
nonzero routed compression \(P_{A,B}\).  Both \(H_{c,d}\) and
\(G_{c,d}\) have rank at most one.  Define

\[
\begin{aligned}
 W_{c,d}&={U_{cd}\over h}C+H_{c,d}+G_{c,d},\\
 Z_{c,d}&={h+1\over h}U_{cd}C+G_{c,d}.
\end{aligned}                                                \tag{3}
\]

Then

\[
                         \boxed{W_{c,d}=-K_{c,d}+Z_{c,d}.}    \tag{4}
\]

For every matrix functional \(\ell\) on \(\operatorname{Mat}_{M,M}\),
the complete contracted cap

\[
 \widehat r_\ell={\ell(C)\over h}q+
                     \sum_{i,j\in M}\ell_{ij}p_i s_j        \tag{5}
\]

obeys

\[
 \boxed{
 \widehat r_\ell q^{[h-1]}
   =\ell(E_{\alpha\alpha})X_\alpha
      +\ell(E_{\beta\beta})X_\beta,\qquad
 [\widehat r_\ell]_{rs;c,d}=\ell(W_{c,d}).}                \tag{6}
\]

The enlargement from \(A\times B\) to \(M\times M\) is safe precisely
where it is needed here.  Although the added endpoint rows need not be
locally dark in colour \(\delta\), the zero cohafnian vectors together
with \(\chi=0\) make the pure-\(\delta\) coefficient of their three-site
normal row vanish term by term.  Thus the former rectangular and
one-coordinate compression cases are not separate obstructions on this
branch.

If \(K_{c,d}\ne0\), the matrix-space conclusion is exact.

* If \(K_{c,d}\notin\mathbb C Z_{c,d}\), one may choose \(\ell\) such
  that
  \[
     \ell(Z_{c,d})=0,\qquad \ell(K_{c,d})\ne0,
     \qquad \ell|_{\mathcal D}\ne0,
     \quad
     \mathcal D=\operatorname{span}
          \{E_{\alpha\alpha},E_{\beta\beta}\}.
                                                               \tag{7}
  \]
  Equations (4)--(6) then give the exact signed coefficient
  \[
                   [\widehat r_\ell]_{rs;c,d}
                         =-\ell(K_{c,d})\ne0.                 \tag{8}
  \]
* If \(K_{c,d}=\nu Z_{c,d}\) and \(W_{c,d}\ne0\), then
  \(\nu\ne0,1\) and
  \[
                   W_{c,d}={1-\nu\over\nu}K_{c,d}.           \tag{9}
  \]
  A functional can still detect this nonzero literal edge, the curvature,
  and a diagonal target simultaneously; the edge and curvature evaluations
  are now projectively, rather than signed, equal.
* The sole matrix-level failure of a complete missing-square cap to carry
  the selected edge is
  \[
       \boxed{W_{c,d}=0
       \quad\Longleftrightarrow\quad
       H_{c,d}+G_{c,d}=-{U_{cd}\over h}C.}                  \tag{10}
  \]

Equation (10) is the **full-cap carrier resonance**.  It is strictly
smaller than either span alignment left by the direct-zero selector in
[the curvature-bearing cap note](curvature-bearing-diagonal-anchor-selection.md).
It is not a contradiction.  An explicit off-diagonal matrix model below
shows that (10), nonzero selected curvature, nonzero \(T\), and the local
visibility zeros are compatible.

This still does not prove the conjecture.  A nonzero literal coefficient
must be transported to the required weighted \(K_6\) four-cycle normal
with its source grade preserved.  The theorem here sharpens the input to
that problem; it does not assert that every nonresonant carrier already has
the required normal.

## 2. The complete cap and its literal edge

The four rows indexed by \(i,j\in M\) are

\[
 P_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i.             \tag{11}
\]

Contracting (11) against \(\ell\) gives

\[
 \ell(C)q^{[h]}+
 \left(\sum_{i,j\in M}\ell_{ij}p_i s_j\right)q^{[h-1]}
 =\ell(E_{\alpha\alpha})X_\alpha
     +\ell(E_{\beta\beta})X_\beta.                        \tag{12}
\]

Since \(qq^{[h-1]}=h q^{[h]}\), equation (12) is exactly the
first identity in (6).

At the two residual sites \(r,s\), the local coefficients of the two
endpoint stars are

\[
 \begin{array}{c|cc}
       &r,c&s,d\\ \hline
 p_i&R_{ic}&E_{id}\\
 s_j&T_{jc}&Q_{jd}.
 \end{array}                                                \tag{13}
\]

The internal term in (5) contributes \(U_{cd}\ell(C)/h\).  The two
assignments of the endpoint stars contribute respectively
\(\ell(H_{c,d})\) and \(\ell(G_{c,d})\).  This proves the second identity
in (6).  Finally,

\[
\begin{aligned}
 W_{c,d}+K_{c,d}
 &=\left({1\over h}+1\right)U_{cd}C+G_{c,d}
  =Z_{c,d},
\end{aligned}
\]

which proves (4), including its sign and its factor \((h+1)/h\).

## 3. Why \(\chi=0\) permits the full missing square

Expose only the third site \(r\), and write \(z,x_i,y_j,t_k\) on the odd
residual set as in the
[diagonal-anchor descent](double-zero-diagonal-anchor-polar-descent.md).
For a functional on \(M\times M\), put

\[
\begin{aligned}
 c_\ell&=\ell(C),\\
 B_\ell&=\sum_{i,j\in M}\ell_{ij}x_i y_j,\\
 L_{\ell,k}&=\sum_{i,j\in M}\ell_{ij}
                   (R_{ik}y_j+T_{jk}x_i).
\end{aligned}                                                \tag{14}
\]

The literal 27-row identity gives

\[
 (c_\ell t_k+L_{\ell,k})z^{[h-1]}
       +B_\ell t_kz^{[h-2]}
 =\ell((E_{kk})_{M,M})X_k^D.                               \tag{15}
\]

On the double-zero branch define

\[
 \tau_k=[t_kz^{[h-1]}]_{\delta^D},\qquad
 \upsilon_j=[y_jz^{[h-1]}]_{\delta^D},\qquad
 \chi_i=[x_iz^{[h-1]}]_{\delta^D}.                         \tag{16}
\]

The two zero cohafnian covectors give \(\tau=\upsilon=0\); branch (1)
gives \(\chi=0\).  Moreover cross-site synchronization gives

\[
 [x_i y_jt_kz^{[h-2]}]_{\delta^D}
       =\delta_{i\delta}\delta_{j\delta}\delta_{k\delta}.
                                                               \tag{17}
\]

Take \(k=\delta\) and the pure-\(\delta\) coefficient in (15).  Its four
types of terms vanish separately:

\[
\begin{array}{c|c}
c_\ell t_\delta z^{[h-1]}&c_\ell\tau_\delta=0,\\
R_{i\delta}y_jz^{[h-1]}&R_{i\delta}\upsilon_j=0,\\
T_{j\delta}x_iz^{[h-1]}&T_{j\delta}\chi_i=0,\\
x_i y_jt_\delta z^{[h-2]}&0\quad(i,j\in M,\ \delta\notin M).
\end{array}                                                  \tag{18}
\]

The right side also vanishes because \((E_{\delta\delta})_{M,M}=0\).
This proves coefficient-level purity without claiming the stronger local
support equations \(x_i^\delta=y_j^\delta=0\) for every newly adjoined
row.  It is the exact role of \(\chi=0\) in the enlargement.

## 4. One-line selection and the true carrier obstruction

The following is just dual separation, but it removes both old two-plane
alignments at once.

**Lemma 4.1 (signed full-cap selection).**  Let
\(V=\operatorname{Mat}_{2\times2}(\mathbb C)\), let
\(\mathcal D\subset V\) be its diagonal plane, and let \(K\ne0,Z\in V\).
There is \(\ell\in V^*\) satisfying (7) if and only if

\[
                              K\notin\mathbb C Z.            \tag{19}
\]

**Proof.**  A functional annihilating \(Z\) but detecting \(K\) exists
exactly when \(K\notin\mathbb C Z\).  Inside the annihilator subspace
\((\mathbb C Z)^\perp\), the functionals that kill \(K\), and those that
kill all of \(\mathcal D\), are two proper linear subspaces.  They cannot
cover a complex vector space.  The second is proper because a
two-dimensional plane \(\mathcal D\) cannot lie in the line
\(\mathbb C Z\).  Choose \(\ell\) outside their union. \(\square\)

There is an even more basic carrier statement.  If \(K\ne0\) and
\(W\ne0\), the three proper subspaces

\[
 K^\perp,\qquad W^\perp,\qquad\mathcal D^\perp
\]

do not cover \(V^*\).  Hence one \(\ell\) detects the curvature, the
literal edge, and a diagonal target simultaneously.  Conversely,
functionals separate points of \(V\), so every cap (5) has zero
\((rs;c,d)\) coefficient exactly when \(W=0\).  This proves (10) as an
if-and-only-if carrier statement, not merely as a sufficient obstruction.

If \(K\in\mathbb C Z\), write \(K=\nu Z\).  The assumption \(K\ne0\)
gives \(Z\ne0\) and \(\nu\ne0\).  Equation (4) gives (9); its scalar
vanishes exactly when \(\nu=1\), equivalently \(W=0\).

## 5. The old span alignments in invariant form

The direct-zero selector in the curvature-bearing cap note imposed
\(\ell(C)=\ell(G)=0\).  On the full missing square its two failures were

\[
 K\in\operatorname{span}(C,G),\qquad
 \mathcal D\subseteq\operatorname{span}(C,G).               \tag{20}
\]

They have short invariant classifications.

First, since \(\dim\mathcal D=2\) and
\(\dim\operatorname{span}(C,G)\le2\), the second condition in (20) holds
if and only if those two planes are equal.  Because \(G\) has rank at most
one, after possibly exchanging \(\alpha,\beta\) this is exactly

\[
 G=gE_{\alpha\alpha},\qquad
 C=aE_{\alpha\alpha}+bE_{\beta\beta},qquad gb\ne0.          \tag{21}
\]

In particular a selected nonzero off-diagonal entry of \(C\) excludes
(21).  Rectangular and coordinate cases from the smaller compression do
not add new forms: adjoining the literal rows first always returns to this
single \(2\times2\) statement.

Second, write

\[
 H=r q^{\mathsf T},\qquad G=e t^{\mathsf T}.                 \tag{22}
\]

Since \(K=UC-H\), the first condition in (20) is equivalent to

\[
                         H\in\operatorname{span}(C,G).       \tag{23}
\]

If \(C,G\) are dependent, (23) says simply that \(H\) lies on the same
line.  If they are independent and \(H\in\mathbb C G\), (23) is automatic.
In the remaining case \(H,G\) are independent and (23) is equivalent to
\(C\in\operatorname{span}(H,G)\).  The pencil is controlled by

\[
 \boxed{\det(xH+yG)=xy\,(r\wedge e)(q\wedge t).}             \tag{24}
\]

Thus it is either a common-left/common-right-factor compression plane, or
a transverse secant plane.  In the transverse case changes of row and
column basis put \(H,G\) at \(E_{11},E_{22}\); a mixed member is
invertible, and the only singular members are the two generating lines.
This is the complete rank geometry behind (20), without a matching-support
case census.

Lemma 4.1 shows why neither plane in (20) is the final obstruction once the
forced internal-\(q\) term is retained.  Their common residual is the much
sharper equality (10).

## 6. Rank geometry of the carrier resonance

Abbreviate \(u=U_{cd}\), \(H=H_{c,d}\), and \(G=G_{c,d}\).  There are two
distinct branches of (10).

If \(u=0\), then

\[
                              H=-G.                          \tag{25}
\]

The selected assumption \(K=-H\ne0\) forces \(H,G\ne0\), but puts no
rank restriction on \(C\).  In particular \(C\) may be invertible.  This
assignment-cancellation branch must not be folded into the secant branch.

If \(u\ne0\), then

\[
                    C=-{h\over u}(H+G),\qquad H+G\ne0.       \tag{26}
\]

Using (22),

\[
                      \det(H+G)=(r\wedge e)(q\wedge t).      \tag{27}
\]

Consequently:

* if \(C\) is invertible, both wedge factors in (27) are nonzero, so
  \(H,G\) are nonzero transverse rank-one summands;
* if \(C\) has rank one, at least one wedge factor vanishes, so the two
  assignments have dependent left factors or dependent right factors
  (including the degenerate cases where one assignment is zero).

On the nonzero-\(u\) resonance the curvature is

\[
                         K=-(h+1)H-hG.                       \tag{28}
\]

In the invertible case (27) gives

\[
                  \det K=h(h+1)(r\wedge e)(q\wedge t)\ne0.  \tag{29}
\]

Thus invertibility and selected nonzero curvature do not contradict the
resonance; they make its transverse secant structure especially rigid.

## 7. An off-diagonal matrix-level survivor

For any \(h\ge3\), take

\[
 H=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
 G=\begin{pmatrix}0&0\\1&1\end{pmatrix},\qquad
 C=H+G=\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad
 u=-h.                                                       \tag{30}
\]

These have rank-one factorizations

\[
 H=\binom10(1,0),\qquad G=\binom01(1,1),                    \tag{31}
\]

with both left and right factor pairs independent.  Hence \(C\) is
invertible, and

\[
 W=-C+H+G=0,qquad
 K=-hC-H=
   \begin{pmatrix}-(h+1)&0\\-h&-h\end{pmatrix}.             \tag{32}
\]

The physical off-diagonal direct cell \((\beta,\alpha)\) has

\[
                         C_{\beta\alpha}=1,qquad
                         K_{\beta\alpha}=-h\ne0.             \tag{33}
\]

It may be realized at the finite-block level by choosing, for fixed
\(c,d\in M\),

\[
 R_{M,c}=Q_{M,d}=\binom10,qquad
 E_{M,d}=\binom01,qquad
 T_{M,c}=\binom11,qquad U_{cd}=-h.                         \tag{34}
\]

In particular the chosen column of \(T\) is nonzero.  The colour-\(\delta\)
columns can be set to zero, consistently with the local cross-visibility
conditions.

Equations (30)--(34) are deliberately only a **matrix-level resonance
guard**.  They do not specify the residual quadratic, do not verify
\(\chi=0\), and do not satisfy or claim the complete full-nine matching
tensor.  Their exact scope is to show that rank geometry, local visibility,
and a selected nonzero off-diagonal curvature do not by themselves rule out
(10).  A contradiction must use further source coefficients of the
full-nine rows, or transport (10) into the weighted four-cycle normal.

The dependency-free checker
[`verify_full_missing_square_cap_carrier_resonance.py`](../computations/verify_full_missing_square_cap_carrier_resonance.py)
audits (4), the finite-field selection statement, the target-plane
classification, the determinant formula (24), the two resonance branches,
and the exact model (30)--(34).  It performs no matching search.
