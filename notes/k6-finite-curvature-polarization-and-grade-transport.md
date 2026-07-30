# Finite curvature has an exact K6 polarization; grade transport is the gap

## 1. Outcome

The distinction between the finite curvature coefficient

\[
                         \kappa=AU-BF\ne0                     \tag{1}
\]

and the linearized four-cycle normal in the weighted \(K_6\) matching
algebra is not an abstract algebraic obstruction.  Every invertible
\(2\times2\) curvature rectangle admits a case-free decomposition into two
rank-one rectangles, and its finite determinant is exactly the derivative in
the second rank-one direction.

More precisely, write

\[
 M=\begin{pmatrix}A&B\\F&U\end{pmatrix},\qquad \det M=\kappa,
                                                                  \tag{2}
\]

with rows indexed by \(x,w\) and columns by \(y,z\).  There are nonzero
rank-one matrices \(Q,R\) such that

\[
 M=Q+R,\qquad Q_{ij}=t_it_j,\qquad t_x,t_w,t_y,t_z\ne0,       \tag{3}
\]

and

\[
                         \det(Q+sR)=s\kappa.                    \tag{4}
\]

After extending \(Q\) to a nonzero vertex-factor edge array \(q\) on
\(K_6\), and extending the four entries of \(R\) to any edge array
\(\widetilde R\), the four complementary-cut functional from the
[source-provenance guard](k6-lefschetz-source-provenance-guard.md) detects
the displayed part of \(\widetilde R\) with value

\[
                  \mu^{\mathsf T}T_q\widetilde R
                     ={\kappa\over t_xt_yt_zt_w}\ne0.           \tag{5}
\]

Thus finite-to-linear polarization is complete at the aggregate layer.  The
remaining theorem is source-provenant and grade-sensitive: before the common
matching power is introduced, the physical direct/star/internal overlap must
produce a correction array whose four-cycle derivative is \(AU-BF\).  The
literal internal term \((AU-BF)z\) cannot simply be declared to be that
correction; its aggregate radial analogue is killed by the four-cycle
functional.

## 2. A case-free two-rank-one decomposition

**Theorem 2.1 (finite curvature polarization).**  Let \(M\in
\operatorname{Mat}_{2\times2}(\mathbb C)\) be invertible.  There are
rank-one matrices \(Q,R\), with every entry of \(Q\) nonzero, such that
\(M=Q+R\) and (4) holds.

**Proof.**  The conditions

\[
                 u\in(\mathbb C^*)^2,\qquad
                 M^{-1}u\in(\mathbb C^*)^2                  \tag{6}
\]

exclude only four proper lines from \(\mathbb C^2\), so choose such a
vector \(u\).  Put \(a=M^{-1}u\).  The affine line

\[
                         v^{\mathsf T}a=1                    \tag{7}
\]

is not contained in either coordinate axis, because both entries of \(a\)
are nonzero.  Choose \(v\) on it with both entries nonzero, and define

\[
                         Q=uv^{\mathsf T},\qquad R=M-Q.       \tag{8}
\]

Every entry of \(Q\) is nonzero.  The matrix determinant lemma gives

\[
 \det R=\det M\bigl(1-v^{\mathsf T}M^{-1}u\bigr)=0.          \tag{9}
\]

The matrix \(R\) is not zero, since otherwise the invertible matrix \(M\)
would equal the rank-one matrix \(Q\).  Hence \(Q,R\) both have rank one.
For two \(2\times2\) rank-one matrices, \(\det(Q+sR)\) has zero constant
and quadratic coefficients.  Its value at \(s=1\) is \(\det M=\kappa\),
which proves (4).  \(\square\)

Writing

\[
 u=(t_x,t_w)^{\mathsf T},\qquad v=(t_y,t_z)^{\mathsf T}      \tag{10}
\]

gives the vertex-factor form in (3).  The four factors are nonzero by
construction.

The second rectangle has a compatible labelled factorization as well.  Write
\(a=(a_y,a_z)^{\mathsf T}\) and \(v=(v_y,v_z)^{\mathsf T}\).  Equation (7)
gives

\[
 I-av^{\mathsf T}
  =\binom{v_z}{-v_y}\begin{pmatrix}a_z&-a_y\end{pmatrix},
\qquad
 R=M\binom{v_z}{-v_y}\begin{pmatrix}a_z&-a_y\end{pmatrix}. \tag{10a}
\]

Its row factors may contain a zero; no density of the second profile is
claimed or needed below.

## 3. Exact transport through the weighted K6 inverse

Extend the four nonzero factors in (10) by arbitrary nonzero values at two
additional vertices, and put

\[
                         q_{ij}=t_it_j                       \tag{11}
\]

on all edges of \(K_6\).  Let \(\widetilde R\) be any edge array whose four
displayed cycle entries agree with the rectangle \(R\), and define the
weighted cycle covector

\[
 \lambda_{xy}=q_{xy}^{-1},\quad
 \lambda_{wz}=q_{wz}^{-1},\quad
 \lambda_{xz}=-q_{xz}^{-1},\quad
 \lambda_{wy}=-q_{wy}^{-1},                                \tag{12}
\]

with every other coordinate zero.  The complementary-cut covector is

\[
                         \mu_V={c_{V^c}\over t_V},           \tag{13}
\]

where \(c\) has signs \(+,+,-,-\) on
\(xy,wz,xz,wy\), and \(t_V=\prod_{i\in V}t_i\).  The weighted inverse
identity gives

\[
                         \mu^{\mathsf T}T_q=\lambda^{\mathsf T}. \tag{14}
\]

Let

\[
                 \kappa(a)=a_{xy}a_{wz}-a_{xz}a_{wy}.        \tag{15}
\]

Only the four cycle entries of \(\widetilde R\) occur in either side of

\[
\begin{aligned}
 d\kappa_q(\widetilde R)
   ={}&q_{wz}\widetilde R_{xy}+q_{xy}\widetilde R_{wz}\\
     &-q_{wy}\widetilde R_{xz}-q_{xz}\widetilde R_{wy}.    \tag{16}
\end{aligned}
\]

Equations (4) and (15)--(16) therefore give

\[
 d\kappa_q(\widetilde R)=\kappa,\qquad
 \mu^{\mathsf T}T_q\widetilde R
   =\lambda(\widetilde R)
   ={\kappa\over t_xt_yt_zt_w}.                             \tag{17}
\]

The unspecified eleven entries of \(\widetilde R\) do not affect (17),
because both \(\lambda\) and the derivative (16) are supported on the
four-cycle.  The operator \(T_q\) and covector \(\mu\) do depend on the
chosen nonzero completion \(q\), but (14)--(17) use that same completion
throughout.

## 4. Two algebraic rank-one profiles and their factorization gauge

Suppose the two algebraic rank-one rectangles are presented as labelled
factor profiles

\[
 Q_{ij}=t_i^{(0)}t_j^{(0)},\qquad
 R_{ij}=t_i^{(1)}t_j^{(1)},                                  \tag{18}
\]

and put \(\rho_i=t_i^{(1)}/t_i^{(0)}\).  The numerator factors may vanish;
the ratios remain defined because every denominator factor belongs to the
dense base profile \(Q\).  With \(q\) and \(\widetilde R\) denoting any
extensions as in Section 3, the four-cycle evaluation is

\[
\begin{aligned}
 \mu^{\mathsf T}T_q\widetilde R
  &=\rho_x\rho_y+\rho_w\rho_z
       -\rho_x\rho_z-\rho_w\rho_y\\
  &=(\rho_x-\rho_w)(\rho_y-\rho_z),                         \tag{19}
\end{aligned}
\]

and direct expansion gives

\[
 \det(Q+R)
 =t_x^{(0)}t_y^{(0)}t_z^{(0)}t_w^{(0)}
       (\rho_x-\rho_w)(\rho_y-\rho_z).                      \tag{20}
\]

The factorization of a rank-one rectangle has a reciprocal row/column
gauge.  Under independent such gauges for the two algebraic profiles, the
first parenthesis in (19) and the second acquire reciprocal factors.  Their
product, and hence the determinant class, is invariant.

This is only algebraic factorization gauge.  It neither identifies these
profiles with two physical labelled anchors nor proves any statement about
an individual physical crossed cofactor or first jet.  In particular it
does not make a crossed target-zero row sufficient: a source theorem must
still identify the second algebraic profile with the correction term of the
literal decorated overlap.

## 5. The exact missing source identity

At the aggregate level, a four-cycle correction \(\beta_{\rm src}\)
represents the finite curvature class exactly when

\[
\boxed{
 q_{wz}(\beta_{\rm src})_{xy}
 +q_{xy}(\beta_{\rm src})_{wz}
 -q_{wy}(\beta_{\rm src})_{xz}
 -q_{xz}(\beta_{\rm src})_{wy}=AU-BF.
}                                                            \tag{21}
\]

Equivalently, if \(\widetilde R\) is any \(K_6\) extension of a polarization
supplied by Theorem 2.1, then

\[
 \beta_{\rm src}\equiv\widetilde R
                       \pmod{\ker d\kappa_q}.               \tag{22}
\]

Equations (21)--(22) are necessary and sufficient for equality with the
specified finite curvature class at this aggregate four-cycle layer.  What
is not proved is that the two physical labelled anchors and crossed row
construct such a \(\beta_{\rm src}\) before multiplication by the common
power, with overlap coboundaries landing in \(\ker d\kappa_q\) and with the
direct, star, and internal grades preserved.  The base array \(q\) here is
existentially constructed from \(M\); it has not been identified with a
literal physical internal profile.

There is an important wrong identification to exclude.  If one maps the
literal internal overlap term \((AU-BF)z\) to the radial array

\[
                         \beta=(AU-BF)q,                      \tag{23}
\]

then

\[
                  d\kappa_q(\beta)=0,\qquad
                  \mu^{\mathsf T}T_q\beta=0.                 \tag{24}
\]

Indeed the radial line through \(q\) has rank at most one, equivalently its
determinant vanishes identically.  In the vertex-factor model \(q\) lies in
the tangent image \(J_t\) by taking every logarithmic site
variation equal to \(1/2\), while \((AU-BF)q\) uses the constant variation
\((AU-BF)/2\).  This is not an identification with the tangent space of an
arbitrary physical source.  Hence the finite coefficient \(AU-BF\) cannot be sent
directly to a multiple of the base internal quadratic.  A successful
source theorem must show that a transverse second-anchor correction—not the
radial curvature term—survives the decorated overlap with its grading.

The algebra above proves that such a correction would be sufficient at the
weighted \(K_6\) layer.  It does not construct it from an exact ternary
source, and therefore does not close the conjecture.
