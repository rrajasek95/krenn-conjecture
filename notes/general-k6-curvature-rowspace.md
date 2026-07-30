# General \(K_6\) curvature pullback is a Hessian row-space condition

## 1. Outcome

Let \(q=(q_{ij})\) be an arbitrary scalar edge array on six sites and let

\[
 T_q:\mathbb C^{\binom 62}\longrightarrow
       \mathbb C^{\binom 64},\qquad
 (T_q\beta)_V=\sum_{e\subset V}\beta_e q_{V\setminus e}.       \tag{1}
\]

After indexing a four-set row by its complementary edge, \(T_q\) becomes
the symmetric Hessian \(H_q\) of the six-site hafnian.  Consequently the
four-cycle covector

\[
 \lambda=d\kappa_q,qquad
 \kappa(a)=a_{rs}a_{uv}-a_{ru}a_{sv},                       \tag{2}
\]

has a four-set pullback if and only if

\[
 \boxed{\quad
 \lambda\in\operatorname {row}T_q
 \iff d\kappa_q(\ker H_q)=0.
 \quad}                                                     \tag{3}
\]

Thus an arbitrary invertible \(T_q\) is sufficient; no vertex-factor form
of \(q\) is needed.  The unique pullback is

\[
                         \mu=H_q^{-1}\lambda.                \tag{4}
\]

The nonzero complementary four-site hafnian forced by a cap equation does
not imply (3).  It supplies an invertible \(4\times4\) pivot in \(H_q\),
but the remaining condition is an exact Schur-complement compatibility.
Two \(0/1\) guards below show failure.  The sharper one has

\[
 \operatorname {rank}H_q=14,qquad
 \operatorname {rank}[H_q\mid\lambda]=15,                  \tag{5}
\]

so the obstruction persists at corank one and is detected by a nonzero
bordered determinant.  Therefore the remaining general-base **row-space**
obstruction is precisely the part of the Hessian discriminant on which the
selected curvature varies along an infinitesimal polar fibre.  The separate
source/grade obstruction remains even off that discriminant.

## 2. The complementary-edge Hessian

Write \(E=\binom{[6]}2\).  Identify a row
\(V\in\binom{[6]}4\) with the missing edge \(f=[6]\setminus V\).
In these coordinates (1) is the
square matrix

\[
 (H_q)_{f,e}=
 \begin{cases}
 q_{[6]\setminus(e\cup f)},&e\cap f=\varnothing,\\
 0,&e\cap f\ne\varnothing.
 \end{cases}                                                \tag{6}
\]

It is symmetric.  If

\[
             \operatorname {Haf}_6(a)
               =\sum_{\{e,f,g\}\text{ perfect matching}}
                    a_ea_fa_g,                              \tag{7}
\]

then \(H_q=\operatorname {Hess}(\operatorname {Haf}_6)|_q\).
The standard coordinate pairing therefore gives

\[
 \operatorname {row}T_q=\operatorname {im}H_q
                         =(\ker H_q)^\perp.                 \tag{8}
\]

Since the coordinate vector of \(d\kappa_q\) is

\[
 \lambda_{rs}=q_{uv},\quad
 \lambda_{uv}=q_{rs},\quad
 \lambda_{ru}=-q_{sv},\quad
 \lambda_{sv}=-q_{ru},                                     \tag{9}
\]

and is zero elsewhere, (8) proves (3).  In invariant language, \(H_q\) is
the differential at \(q\) of the quadratic polar map
\(a\mapsto\nabla\operatorname {Haf}_6(a)\).  Failure of (3) means that
\(\kappa\) is not infinitesimally constant on a fibre of that polar map.

The condition is unchanged by relabelling sites or by a nonzero vertex
rescaling \(q_{ij}\mapsto t_it_jq_{ij}\).  Indeed, if \(D_E\) has diagonal
entry \(t_it_j\) at \(ij\), then

\[
 H_{t\cdot q}=\Bigl(\prod_i t_i\Bigr)
               D_E^{-1}H_qD_E^{-1},                         \tag{10}
\]

while the four-cycle covector is transformed by a nonzero scalar times
\(D_E^{-1}\).

## 3. What the complementary hafnian actually gives

Let \(U=[6]\setminus\{r,s\}\).  If

\[
                         \operatorname {Haf}_U(q)\ne0,       \tag{11}
\]

then one perfect matching \(uv\mid zw\) of \(U\) has
\(q_{uv}q_{zw}\ne0\).  Use \(uv\) in (2), and order the four cycle edges as

\[
                         S=(rs,uv,ru,sv).                    \tag{12}
\]

For \(R=E\setminus S\), block (6) as

\[
 H_q=\begin{pmatrix}A&B\\B^{\mathsf T}&D\end{pmatrix},
 \qquad
 A=q_{zw}J,
 \qquad
 J=\begin{pmatrix}
 0&1&0&0\\1&0&0&0\\0&0&0&1\\0&0&1&0
 \end{pmatrix}.                                            \tag{13}
\]

Thus \(A^{-1}=q_{zw}^{-1}J\).  Define

\[
 \Sigma=D-B^{\mathsf T}A^{-1}B,
 \qquad
 b=B^{\mathsf T}A^{-1}\lambda_S.                           \tag{14}
\]

**Proposition 3.1 (sharp hafnian-pivot criterion).**  Under
\(q_{uv}q_{zw}\ne0\),

\[
 \boxed{\quad
 \lambda\in\operatorname {row}T_q
 \iff b\in\operatorname {im}\Sigma
 \iff b\perp\ker\Sigma.
 \quad}                                                     \tag{15}
\]

Moreover

\[
 \det H_q=q_{zw}^4\det\Sigma.                              \tag{16}
\]

**Proof.**  Write a prospective solution of
\(H_q(x,y)^{\mathsf T}=\lambda\) in the \(S\sqcup R\) decomposition.
Since \(\lambda_R=0\),

\[
 Ax+By=\lambda_S,qquad B^{\mathsf T}x+Dy=0.                \tag{17}
\]

Eliminating \(x=A^{-1}(\lambda_S-By)\) gives

\[
                         \Sigma y=-b.                       \tag{18}
\]

This proves the first equivalence.  The second uses symmetry of
\(\Sigma\).  The block determinant formula proves (16).  More explicitly,
every \(y\in\ker\Sigma\) gives

\[
 z=(-A^{-1}By,y)\in\ker H_q,qquad
 \lambda^{\mathsf T}z=-b^{\mathsf T}y,                     \tag{19}
\]

which is exactly the invariant obstruction (3).  \(\square\)

In particular, \(\det\Sigma\ne0\) is a sufficient open condition, and is
equivalent here to invertibility of \(T_q\).  It is not necessary for the
single covector: on the singular locus the weaker and exact condition is
\(b\perp\ker\Sigma\).  The uniform point \(q_e=1\) has
\(\det H_q=-1458\ne0\), so this positive branch is nonempty and Zariski
open.

If \(H_q\) has corank one, (3) also has the adjugate form

\[
 \lambda\in\operatorname {row}T_q
 \iff \operatorname {adj}(H_q)\lambda=0
 \iff
 \det\begin{pmatrix}H_q&\lambda\\
                     \lambda^{\mathsf T}&0\end{pmatrix}=0. \tag{20}
\]

The final scalar test is special to corank one.  For larger corank the
bordered determinant vanishes automatically and (3) or (15) must be used.

## 4. Two exact \(0/1\) guards

Take \(r=0,s=1,U=\{2,3,4,5\}\) and let

\[
                         \beta=\mathbf e_{01}.               \tag{21}
\]

Then the all-six-sites coefficient of \(\beta q^{[2]}\) is exactly
\(\operatorname {Haf}_U(q)\).  Thus the guards below satisfy both scalar
consequences supplied by the dark cap calculation: a nonzero top
coefficient and a nonzero four-cycle derivative.

### 4.1 A four-edge transparent guard

Put

\[
                 q_{03}=q_{14}=q_{23}=q_{45}=1              \tag{22}
\]

and set every other edge to zero.  Choose \(uv=23,zw=45\).  Then

\[
 \operatorname {Haf}_{2345}(q)=q_{23}q_{45}=1,
 \qquad
 \lambda=d(q_{01}q_{23}-q_{02}q_{13})_q=\mathbf e_{01},
 \qquad
 \lambda(\beta)=1.                                        \tag{23}
\]

Nevertheless

\[
 z=\mathbf e_{01}-\mathbf e_{05}-\mathbf e_{12}
                         +\mathbf e_{25}                    \tag{24}
\]

satisfies \(H_qz=0\) and \(\lambda(z)=1\).  Hence \(\lambda\) is not in
the row space.  Exact elimination gives

\[
               \operatorname {rank}H_q=10,qquad
               \operatorname {rank}[H_q\mid\lambda]=11.    \tag{25}
\]

This gives a transparent reason that (11) is insufficient: its
matching supplies the pivot \(A\), while a nonzero curvature derivative
survives on the Schur kernel.

### 4.2 A corank-one determinantal guard

Let \(q_e=1\) on

\[
 \{01,02,03,04,05,12,13,14,23,45\}                         \tag{26}
\]

and let it vanish on the other five edges.  Again

\[
 \operatorname {Haf}_{2345}(q)=1,
 \qquad
 \beta q^{[2]}|_{[6]}=1.                                   \tag{27}
\]

Here the selected base is itself four-cycle-flat,

\[
 q_{01}q_{23}-q_{02}q_{13}=0,
 \qquad
 \lambda=\mathbf e_{01}+\mathbf e_{23}
                   -\mathbf e_{02}-\mathbf e_{13},
 \qquad
 \lambda(\beta)=1.                                        \tag{28}
\]

The primitive kernel vector is

\[
                 z=\mathbf e_{02}-\mathbf e_{03}
                         -\mathbf e_{24}+\mathbf e_{34},    \tag{29}
\]

and \(H_qz=0\), while \(\lambda(z)=-1\).  Exact rational elimination gives

\[
 \operatorname {rank}H_q=14,
 \qquad
 \operatorname {rank}[H_q\mid\lambda]=15.                 \tag{30}
\]

The \((02,02)\) cofactor of \(H_q\) is \(-128\).  With the normalization
in (29),

\[
 \operatorname {adj}(H_q)=-128\,zz^{\mathsf T},qquad
 \det\begin{pmatrix}H_q&\lambda\\
                     \lambda^{\mathsf T}&0\end{pmatrix}=128. \tag{31}
\]

For the edge-coordinate direction \(\mathbf e_{15}\), direct
differentiation gives

\[
 z^{\mathsf T}H_{\mathbf e_{15}}z=4,
 \qquad \partial_{q_{15}}\det H_q=-512\ne0.                \tag{31a}
\]

Thus the failure is already present on the smooth corank-one part of the
Hessian discriminant; it is not caused only by the large kernel in the
four-edge packet.

## 5. Consequence for the proof frontier

Suppose a rank-one dark cut has produced \(\beta\) and a matching
\(uv\mid zw\) with

\[
 \lambda(\beta)=q_{uv}\beta_{rs}\ne0.                      \tag{32}
\]

If \(T_q\) is invertible—or, more sharply, if the Schur compatibility
(15) holds—then a four-set covector \(\mu\) exists and

\[
                  \mu^{\mathsf T}T_q\beta
                         =\lambda^{\mathsf T}\beta\ne0.     \tag{33}
\]

This closes only the **aggregate row-space pullback** on the
Hessian-nondegenerate open set and on the compatible part of its singular
boundary.  Even there, (33) does not construct the literal source-valid,
grade-preserving overlap required by the proof; aggregate invertibility
alone cannot supply that provenance.  On the incompatible singular
boundary, the cap identity's nonzero complementary hafnian is also
insufficient.  One still needs a physical reason that every
\(z\in\ker H_q\) is curvature-tangent, or an independent source row that
kills the offending Schur-kernel class in (19).

The guards are scalar \(K_6\) packets.  They audit exactly the proposed
implication from a nonzero complementary hafnian to row-space pullback;
they are not claimed to lift to complete decorated ternary full-nine
sources and do not disprove the conjecture.

The dependency-free checker
[verify_general_k6_curvature_rowspace.py](../computations/verify_general_k6_curvature_rowspace.py)
audits (6), the Schur criterion on exact rational packets, the uniform
determinant, both guards, the corank-one cofactor, and the bordered
determinant, including the restricted-family derivative (31a).
