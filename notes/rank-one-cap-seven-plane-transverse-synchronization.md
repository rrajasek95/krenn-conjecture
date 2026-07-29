# The rank-one cap torus misses exactly two transverse equations

## 1. Outcome

The target-compatible rank-one torus from
[the local \(N=8\) obstruction](n8-rank-one-clean-cap-local-torus-obstruction.md)
has a sharper linear interpretation.  Its matrices span exactly

\[
 \mathcal L
   =\{K\in\operatorname{Mat}_{3\times3}(\mathbb C):
                    K_{00}=K_{11}=K_{22}\},\qquad
 \dim\mathcal L=7.                                      \tag{1}
\]

The cap contraction is linear in \(K\).  Consequently compatibility on
the entire rank-one torus is already compatibility on \(\mathcal L\);
there are exactly two missing equations.  They may be represented by the
traceless diagonal normals

\[
                    N_1=E_{11}-E_{00},\qquad
                    N_2=E_{22}-E_{00}.                  \tag{2}
\]

For a physical pair cap, these are not abstract target equations.  If
\(x\) is the internal quadratic, \(a_{ij}\) is the direct block, and
\(p_i,q_j\) are the two literal star rows, then the two transverse
source-provenance equations are

\[
 \boxed{
 (a_{ii}-a_{00})H_6(x)
  +DH_6(x)[p_iq_i-p_0q_0]
       =X_i-X_0,\qquad i=1,2.}                          \tag{3}
\]

Either equation already kills the local dirty-torus countermodel; in fact
its two residuals are

\[
                 -2X_1-X_2,\qquad -X_1-2X_2.           \tag{4}
\]

Thus the countermodel cannot be extended in either normal direction to
the full bilinear cap identity.  This is a genuine synchronization
advance: a seven-dimensional apparently compatible cap family is reduced
to two explicit product-star tests.  It is not an active-clean-cap theorem
and it does not close an E1/E2 chart.

## 2. Seven-plane polarization lemma

Let

\[
 \epsilon=e_0^*+e_1^*+e_2^*.
\]

After projective normalization, the rank-one torus in question is
parameterized by

\[
\begin{aligned}
 \phi(a,b)&=(1,a,b),\\
 \psi(a,b)&=(1,a^{-1},b^{-1}),\\
 K(a,b)&=\phi(a,b)\otimes\psi(a,b),
 \qquad (a,b)\in(\mathbb C^*)^2.                        \tag{5}
\end{aligned}
\]

In matrix form,

\[
 K(a,b)=
 \begin{pmatrix}
 1&a^{-1}&b^{-1}\\
 a&1&ab^{-1}\\
 b&ba^{-1}&1
 \end{pmatrix}.                                         \tag{6}
\]

Every matrix in (6) has equal diagonal, so its span lies in
\(\mathcal L\).  Conversely, the seven matrix coordinates in (6) carry
the seven distinct Laurent characters

\[
                 1,\ a^{-1},\ b^{-1},\ a,\ ab^{-1},\
                 b,\ ba^{-1}.                           \tag{7}
\]

Distinct Laurent characters on \((\mathbb C^*)^2\) are linearly
independent.  Hence the matrices (6) span a seven-dimensional space, which
must be all of \(\mathcal L\).

This proves the following statement.

**Lemma 2.1 (seven-plane polarization).**  Let \(F,G\) be linear maps from
\(\operatorname{Mat}_{3\times3}(\mathbb C)\) to any vector space.  If

\[
                         F(K(a,b))=G(K(a,b))
 \quad\text{for all }(a,b)\in(\mathbb C^*)^2,            \tag{8}
\]

then \(F=G\) on \(\mathcal L\).  Moreover \(F=G\) everywhere if and only
if it also agrees on \(N_1,N_2\).

The last assertion follows because

\[
 \operatorname{Mat}_{3\times3}(\mathbb C)
             =\mathcal L\oplus\operatorname{span}\{N_1,N_2\}. \tag{9}
\]

This is linear polarization, not a dimension heuristic: (7) identifies
the complete character basis and (9) is a direct-sum equality.

## 3. The literal transverse source equations

Fix deleted sites \(p,q\) and write the source quadratic as

\[
 x+\sum_{i=0}^2e_i^{(p)}p_i
   +\sum_{j=0}^2e_j^{(q)}q_j
   +\sum_{i,j=0}^2a_{ij}e_i^{(p)}e_j^{(q)}.             \tag{10}
\]

Endpoint order is literal.  Sorting perfect matchings by the colors at
\(p,q\) gives the coefficient cap tensors

\[
 F_{ij}
   =a_{ij}H_6(x)+DH_6(x)[p_iq_j].                       \tag{11}
\]

Thus for an arbitrary bilinear covector \(K=(K_{ij})\),

\[
 \mathcal C_A(K)
   :=K\mathbin{\lrcorner}H_8(A)
    =\sum_{i,j}K_{ij}F_{ij}.                            \tag{12}
\]

The target cap map is

\[
 \mathcal T(K)=\sum_{i=0}^2K_{ii}X_i.                   \tag{13}
\]

Equations (11)--(13) prove that the full bilinear cap identity is
equivalent to the nine coefficient equations

\[
                         F_{ij}=\delta_{ij}X_i.          \tag{14}
\]

Suppose first that \(\mathcal C_A=\mathcal T\) on the rank-one torus.
Lemma 2.1 gives equality on \(\mathcal L\).  Along a transverse affine
line \(K+tN_i\), linearity makes the normal Jacobian constant:

\[
\begin{aligned}
 {d\over dt}\bigg|_{t=0}
   (\mathcal C_A-\mathcal T)(K+tN_i)
   &=(F_{ii}-F_{00})-(X_i-X_0)\\
   &=(a_{ii}-a_{00})H_6(x)
      +DH_6(x)[p_iq_i-p_0q_0]-(X_i-X_0).                \tag{15}
\end{aligned}
\]

Therefore vanishing of the two normal derivatives is exactly (3), and by
(9) it is necessary and sufficient for the full identity (14).  This is
the desired normal-bundle form.  Crucially, the two response directions in
(15) remain differences of the physical products \(p_iq_i\); replacing
them by arbitrary quadratic representatives would discard the provenance
which makes (3) useful.

## 4. Which normal kills the dirty-torus model

For the local model of the preceding note, every cap-incident endpoint has
color zero.  Its coefficient cap table is therefore

\[
                         F_{00}=\Delta_{6,3},\qquad
                         F_{ij}=0\quad(ij\ne00).         \tag{16}
\]

The rational polarized identity in that note proves the first equality
coefficientwise on all \(3^6\) words.  Equation (16) agrees with the target
on \(\mathcal L\): if the three diagonal entries of \(K\) equal
\(\lambda\), then

\[
 \mathcal C_A(K)=\lambda\Delta_{6,3}
                =\mathcal T(K).                         \tag{17}
\]

The first normal gives

\[
\begin{aligned}
 (\mathcal C_A-\mathcal T)(N_1)
  &=-\Delta_{6,3}-(X_1-X_0)\\
  &=-2X_1-X_2\ne0,                                      \tag{18}
\end{aligned}
\]

so the color-\(1\)-versus-color-\(0\) equation alone kills the model.
Independently,

\[
 (\mathcal C_A-\mathcal T)(N_2)
  =-\Delta_{6,3}-(X_2-X_0)
  =-X_1-2X_2\ne0.                                      \tag{19}
\]

Thus both normals fail, and neither failure uses the already known
nonzero clean error.  The obstruction occurs one logical layer earlier:
the seven-plane cap family does not synchronize to the full target map.

## 5. Exact implication for synchronization and E1/E2

For any candidate physical dirty torus there is now an exact dichotomy.

1. If either equation in (3) fails, the torus cannot be the restriction
   of a full exact source at that pair.
2. If both equations hold, Lemma 2.1 upgrades the torus identity to all
   bilinear \(K\), hence to the complete nine-cap system (14).

The second branch does **not** force \(\mathcal E_{p,q}(K)=0\).
The cap map (12) is linear in \(K\), while the clean error is a homogeneous
cubic at \(N=8\) and involves the higher products of the effective
quadratic.  Once (14) holds, a good pair may be passed into the existing
source-Hessian classification: the already closed regular and defect-one
branches leave E1 or defect at least two (E2).  The present lemma does not
force which survivor occurs and supplies no new rank-loss theorem inside
those charts.

Accordingly this result advances the **synchronization** side only.  It
removes the rank-one torus countermodel by two exact transverse equations
and shows that any stronger continuation must apply nonlinear
common-power/lower-cofactor information after (14), rather than another
top Bianchi reindexing.  The seven-plane lemma itself is uniform at every
even order because both the source cap and target cap remain linear in the
two deleted slots; only the subsequent clean-error polynomial changes
with the order.

The lightweight checker
[verify_rank_one_cap_seven_plane_transverse_synchronization.py](../computations/verify_rank_one_cap_seven_plane_transverse_synchronization.py)
uses exact rational arithmetic to verify a seven-point basis of
\(\mathcal L\), the direct sum (9), the 729-word identity \(F_{00}=\Delta\),
and the two residuals (18)--(19).
