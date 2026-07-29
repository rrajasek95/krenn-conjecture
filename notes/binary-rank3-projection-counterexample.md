# An exact binary realization of the rank-three GHZ projection

Let the three ternary basis vectors be projected to the binary plane by

\[
 e_0\longmapsto u_0=(1,0),\qquad
 e_1\longmapsto u_1=(0,1),\qquad
 e_2\longmapsto u_2=(1,1).                                \tag{1}
\]

The projected six-site target is

\[
 T_6=u_0^{\otimes6}+u_1^{\otimes6}+u_2^{\otimes6}.        \tag{2}
\]

A possible uniform strategy was to show that this binary symmetric-rank
three tensor is not a matching tensor.  That statement is false over the
complex numbers: this note gives an exact finite source.

## 1. Compact `C_3`-equivariant construction

Put

\[
 r=2^{-1/3},\qquad q={r\over\sqrt3},\qquad
 h=\begin{pmatrix}0&1\\-1&1\end{pmatrix},
 \qquad \rho=(0\ 2\ 4)(1\ 3\ 5).                         \tag{3}
\]

Projectively, `h` cycles the three points in (1).  We specify five seed
matrices and generate the remaining ten by the combined color/vertex
symmetry.  The first three seeds are

\[
\begin{aligned}
 A_{01}&=\begin{pmatrix}
 r-iq&(r-iq)/2\\(r-iq)/2&-iq
 \end{pmatrix},\\[2mm]
 A_{03}&=\begin{pmatrix}
 q&q/2+ir/2\\q/2+ir/2&q+ir
 \end{pmatrix},\\[2mm]
 A_{05}&=\begin{pmatrix}
 iq&r/2+iq/2\\r/2+iq/2&iq
 \end{pmatrix}.                                          \tag{4}
\end{aligned}
\]

Let `t=2^(1/3)` and set

\[
 d=t\left(-{\sqrt3\over9}+{i\over6}\right),\qquad
 e=t\left({\sqrt3\over36}+{i\over12}\right).           \tag{5}
\]

The remaining seeds are

\[
 A_{02}=\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad
 A_{13}=\begin{pmatrix}d&d-e\\e&d\end{pmatrix}.          \tag{6}
\]

For an oriented edge, generate its two rotations by

\[
              A_{\rho u,\rho v}=\zeta_{uv},hA_{uv}h^T,  \tag{7}
\]

transposing when the rotated endpoint order is reversed.  The fourth-root
cocycle is listed by its five edge orbits:

\[
\begin{array}{c|ccc}
\text{orbit}&e&\rho e&\rho^2e\\ \hline
01,23,45&-i&1&i\\
02,24,04&i&-1&i\\
03,25,14&-i&i&1\\
05,12,34&1&1&1\\
13,35,15&-1&-i&-i.
\end{array}                                                \tag{8}
\]

Each row product is one, so (7) closes after three rotations because
`h^3=-I`.

**Theorem 1.1 (exact projected-rank-three source).**  The fifteen binary
matrices (4)--(8) satisfy

\[
                         H_6(A)=T_6.                       \tag{9}
\]

**Proof.**  There is a short exact elimination behind the displayed
constants.  Keep (4), but replace (6) by

\[
 A_{02}=\begin{pmatrix}a&a-c\\c&a\end{pmatrix},\qquad
 A_{13}=\begin{pmatrix}d&d-e\\e&d\end{pmatrix}.          \tag{10}
\]

Generate all edges by (7)--(8) and expand the fifteen perfect matchings.
The combined `C_3` symmetry reduces the 64 coefficient residuals to four
polynomials; two are scalar multiples of the first.  Their reduced
Groebner basis is

\[
 \boxed{\quad
 ad=-{2^{1/3}\sqrt3\over9}+{2^{1/3}i\over6},\qquad
 ce={2^{1/3}\sqrt3\over36}+{2^{1/3}i\over12}.
 \quad}                                                    \tag{11}
\]

Equations (5)--(6) are the specialization `a=c=1`, so every residual
vanishes.  This proves (9). `QED`

The symbolic derivation is
`computations/derive_binary_rank3_c3_exact.py`; the independent exact
coefficient audit is
`computations/verify_binary_rank3_projection_exact.py`.

## 2. Consequence for binary-restriction arguments

The obstruction is stronger than a border example.  All fifteen matrices
are finite, algebraic, and invertible, and (9) is an exact identity, not a
small-residual limit.  Therefore a fixed local projection of ternary GHZ
to two dimensions cannot prove the conjecture merely by claiming that the
resulting symmetric-rank-three binary tensor lies outside the binary
matching image.

This construction does not lift (9) back to a ternary realization of
`Delta_(6,3)`: the projection (1) has a kernel, and the unprojected mixed
coefficient data are precisely what it discards.  As with the simultaneous
binary equality examples in `notes/binary-norm-equality-counterfamily.md`,
the missing obstruction must retain genuinely ternary information.
