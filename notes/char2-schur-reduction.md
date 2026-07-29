# Characteristic-two transverse Pfaffians reduce uniformly to six vertices

This note proves a uniform reduction over the algebraic closure
`K=overline(F_2)`.  It is deliberately separated from the unresolved
nonarchimedean normalization problem: no implication from a complex
realization to an integral characteristic-two realization is claimed.

## 1. The transverse Pfaffian identity

Let `n` be even and let `A_uv` be arbitrary `3 by 3` matrices, with the
endpoint order retained.  For a local column vector

\[
                 x_v=(x_{v,0},x_{v,1},x_{v,2})^T
\]

define the alternating `n by n` matrix

\[
 B(x)_{uv}=x_u^T A_{uv}x_v\quad(u<v),\qquad
 B(x)_{vu}=B(x)_{uv},\qquad B(x)_{uu}=0.                 \tag{1}
\]

Symmetry off the diagonal is the same as skew-symmetry in characteristic
two.  The signs in the Pfaffian expansion also disappear, so

\[
 \operatorname {Pf}B(x)
 =\sum_{M\in\operatorname {PM}([n])}
       \prod_{uv\in M}x_u^T A_{uv}x_v.                   \tag{2}
\]

The coefficient of `prod_v x_(v,c(v))` in (2) is exactly the matching
tensor coefficient at the coloring `c`.  Consequently

\[
 H_n(A)=\Delta_{n,3}
 \quad\Longleftrightarrow\quad
 \operatorname {Pf}B(x)=
       \sum_{a=0}^2\prod_{v=1}^n x_{v,a}.                 \tag{3}
\]

This is a polynomial identity, not merely an identity on `K`-points.
Conversely, coefficient comparison in (3) recovers the full matching
tensor identity.

## 2. A principal pivot of every smaller even order

We use the following elementary Pfaffian flag lemma.

**Lemma 2.1.**  If an alternating matrix `C` of even order `2m` over a
field has nonzero Pfaffian, then, for every `0<=j<=m`, it has a principal
submatrix of order `2m-2j` with nonzero Pfaffian.

**Proof.**  Pfaffian expansion at any fixed index `u` gives

\[
 \operatorname {Pf}C
   =\sum_{v\ne u}\epsilon_{uv}C_{uv}
          \operatorname {Pf}C[[2m]\setminus\{u,v\}].      \tag{4}
\]

If the left side is nonzero, at least one summand on the right is nonzero,
so its complementary principal Pfaffian is nonzero.  Iterate.  The signs
are immaterial, and the statement is valid in every characteristic. `QED`

Regard all coordinates `x_(v,a)` as algebraically independent and work
over the rational function field `K(x)`.  The right side of (3) is a
nonzero polynomial, so `B(x)` is nonsingular over `K(x)`.  Apply Lemma 2.1
until order `n-6`.  We obtain a vertex set `P` of cardinality `n-6` such
that

\[
                    \operatorname {Pf}B(x)[P]\ne0.        \tag{5}
\]

The polynomial in (5) uses only the variables at vertices in `P`.  Since
`K` is infinite and its coordinate torus is Zariski dense, there are
vectors

\[
                  \xi_p\in(K^*)^3\qquad(p\in P)           \tag{6}
\]

at which (5) remains nonzero.  Fix such a specialization.  Put

\[
 M=B(\xi)[P],\qquad d=\operatorname {Pf}M\ne0,             \tag{7}
\]

and let `R=[n]\setminus P`, so `|R|=6`.  When `n=6`, take `P` empty,
`M` the empty matrix, and `d=1`.

The all-nonzero requirement in (6) is essential below: it ensures that all
three target coefficients surviving the specialization are nonzero.

## 3. Alternating Schur complementation preserves vertex bilinearity

Order the vertices as `P,R`.  After (6), the scalar alternating matrix has
block form

\[
                         B=\begin{pmatrix}M&E\\E^T&D\end{pmatrix}. \tag{8}
\]

The column `E_r` is a vector of linear forms in the three coordinates of
`x_r`; write it as `L_r x_r`.  The `rs` entry of `D` is the original
bilinear form `x_r^T A_rs x_s`.

Set

\[
                         N=D+E^T M^{-1}E.                  \tag{9}
\]

The inverse of a nonsingular alternating matrix is alternating.  (For
example, its diagonal cofactors are determinants of odd alternating
matrices and hence vanish; symmetry is preserved by inversion.)  Therefore
`E_r^T M^{-1}E_r=0`, and `N` is alternating.  For distinct `r,s`,

\[
 N_{rs}=x_r^T\left(A_{rs}+L_r^T M^{-1}L_s\right)x_s.      \tag{10}
\]

Thus `N` is again a transverse scalar matrix arising from arbitrary
`3 by 3` aggregate matrices on the six vertices in `R`.

For completeness, the Pfaffian Schur identity has no square-root or sign
ambiguity here.  Congruence by the determinant-one block unitriangular
matrix

\[
 S=\begin{pmatrix}I&M^{-1}E\\0&I\end{pmatrix}
\]

gives

\[
 S^TBS=\begin{pmatrix}M&0\\0&N\end{pmatrix}.
\]

Using `Pf(S^TBS)=det(S)Pf(B)` and multiplicativity on block diagonals gives

\[
                         \operatorname {Pf}B
                    =d\operatorname {Pf}N.                \tag{11}
\]

## 4. The six-vertex identity and its normalization

Specializing (3) at the pivot vectors (6), and applying (11), yields

\[
 \operatorname {Pf}N(x_R)
   =\sum_{a=0}^2\lambda_a\prod_{r\in R}x_{r,a},
 \qquad
 \lambda_a=d^{-1}\prod_{p\in P}\xi_{p,a}.                \tag{12}
\]

Every `lambda_a` is nonzero.  Choose one vertex `r_0 in R` and make the
invertible diagonal change of local variables

\[
 y_{r_0,a}=\lambda_a x_{r_0,a},\qquad
 y_{r,a}=x_{r,a}\quad(r\ne r_0).                           \tag{13}
\]

Absorbing the inverse diagonal map into the matrices incident with `r_0`
preserves their arbitrary bilinear form.  Equation (12) becomes

\[
                \operatorname {Pf}N'(y_R)
                    =\sum_{a=0}^2\prod_{r\in R}y_{r,a}.   \tag{14}
\]

Coefficient comparison says exactly `H_6(A')=Delta_(6,3)`.

We have therefore proved:

**Theorem 4.1 (uniform characteristic-two reduction).**  Over any infinite
field of characteristic two, an arbitrary-matrix realization of
`Delta_(n,3)` at one even order `n>=6` implies an arbitrary-matrix
realization of `Delta_(6,3)`.

The proof uses characteristic two only in (2), where the unsigned matching
sum becomes a Pfaffian.  This is why the same Schur argument does not give a
complex all-order reduction.

## 5. What remains at six vertices

The theorem reduces the characteristic-two question uniformly, but a
field-independent six-vertex obstruction is still required.  It cannot be
quoted without audit from the existing complex proof.  In particular, the
residual one-exceptional-edge argument in
`proofs/one-exceptional-edge-obstruction.md` ends in `2r=0` and therefore
does not survive verbatim.

There is nevertheless a separate mod-two obstruction on each of the two
sparse support charts from that note.  Every mixed two-term coefficient
fiber identifies its two nonzero Laurent monomials in characteristic two.
For the `same` chart, these binomial identifications make two of the three
terms in the mixed fiber at coloring `002222` equal.  Their sum is therefore

\[
                            m_0+m+m=m_0\ne0,               \tag{15}
\]

a contradiction.  For the `different` chart, the same argument applies to
the mixed fiber at `001111`.  These implications are audited by
`computations/verify_one_exceptional_char2_obstruction.py`, which reduces
the relevant exponent difference modulo the integer lattice generated by
all two-term mixed fibers.  That lattice is saturated (all nonzero Smith
factors are one), so there is no hidden root-of-unity qualification.

The exact finite-extension diagnostic
`computations/search_one_exceptional_char2_extensions.py` independently
encodes all coefficient equations on these charts over `F_4`, `F_8`, and
`F_16`.  Finite-extension UNSAT is evidence only; it is not used as an
algebraic-closure proof.

A rerun of the broader support CEGAR with its color-sensitive affine systems
solved over `F_2` exposes new dense support survivors already for exceptional
graphs with one or two edges.  Thus rational color-sensitive stabilizers
also cannot be reduced modulo two without additional work.  At present the
safe conclusion is Theorem 4.1 plus the chart-specific obstruction (15),
not a complete six-vertex theorem and not a bridge back to characteristic
zero.
