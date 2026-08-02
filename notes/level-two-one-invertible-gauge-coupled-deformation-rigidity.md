# The minimal gauge-coupled (1I+5Z) packet is deformation-rigid at rank (38)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

The rank-(38) full-L0 construction from the
[minimal gauge-coupled family](level-two-one-invertible-minimal-gauge-coupled-l0-family.md)
has now been enlarged in both its residual blocks and endpoint-star
coefficients. On this natural sparse-support chart:

- five residual blocks are allowed to be arbitrary (2\times2) matrices;
- the four mixed cross blocks have independent scalar weights;
- all eight endpoint coefficients on the four minimal support lines vary;
- both pure L0 equations hold exactly; and
- the two mixed tangents may be arbitrary scalar multiples of the fixed
  canonical vertex gauge.

At the canonical point, the exact (40\times34) Jacobian has rank (25)
and nullity (9). Its residual projection has dimension (7), exactly the
tangent space of the integrated diagonal-torus residual family; the other
two tangent directions are endpoint-only rescalings. More strongly, the
nonlinear equations classify every solution on the nonzero local chart.
Every residual packet is in the same diagonal orbit and hence has

\[
 \operatorname{rank}d\Psi_M=38,
 \qquad \operatorname{rank}(d\Psi_M)_{\rm mixed}=36.            \tag{1}
\]

Thus this enlarged sparse deformation family has no infinitesimal or
integrated rank-raising direction.

This does **not** exclude deformations which activate the other six
residual edges, enlarge the endpoint support beyond the four minimal
lines, or use mixed kernel directions not proportional to the fixed
gauge. It does not close the all-zero-potential (1I+5Z) stratum.

## 1. The enlarged ansatz

Keep the gauge weights

\[
 g=(1,-1,-1,1,0,0).                                           \tag{2}
\]

Allow arbitrary (2\times2) residual blocks on

\[
 S=\{01,02,13,23,45\}.                                        \tag{3}
\]

On the four cross edges

\[
 C=\{04,05,14,15\},                                           \tag{4}
\]

put

\[
 M_{ij}=m_{ij}E_{01}.                                          \tag{5}
\]

All other residual blocks vanish. The endpoint stars retain only the
minimal physical support

\[
\begin{aligned}
 U_i^0&=a_i e_0,&V_i^0&=b_i e_0 &&(i=0,1),\\
 U_j^1&=c_j e_1,&V_j^1&=d_j e_1 &&(j=4,5),                    \tag{6}
\end{aligned}
\]

with every other endpoint row and the direct endpoint block zero. Put

\[
 n_{00}=a_0b_1+b_0a_1,qquad
 n_{11}=c_4d_5+d_4c_5.                                       \tag{7}
\]

The ansatz equations are

\[
 T_{00}=e_{0^6},\qquad T_{11}=e_{1^6},                         \tag{8}
\]

and

\[
 N^{01}=\lambda G(g;M),qquad
 N^{10}=\mu G(g;M).                                           \tag{9}
\]

There are (24) residual variables, eight endpoint coefficients, and
(lambda,\mu): (34) variables total. Equations (8) contribute two
sixteen-coordinate complement equations, and (9) contributes eight cross
equations, giving (40) polynomial equations.

The canonical packet and stars are the point

\[
\begin{gathered}
 M_{02}=M_{13}=E_{11},\quad M_{23}=M_{45}=E_{00},\quad
 m_{04}=m_{05}=m_{14}=m_{15}=1,\quad M_{01}=0,                 \tag{10}\\
 (a_0,a_1)=(1,-1),\quad (b_0,b_1)=(-\tfrac12,\tfrac12),\\
 (c_4,c_5)=(\tfrac12,\tfrac12),\quad(d_4,d_5)=(1,1),
 \quad(\lambda,\mu)=(1,-\tfrac14).
\end{gathered}
\]

## 2. Exact infinitesimal rigidity

Exact rational differentiation of the (40) equations at (10) gives

\[
 \operatorname{rank}J=25,
 \qquad \dim\ker J=34-25=9.                                  \tag{11}
\]

If all (24) residual variations are set to zero, the remaining
(40\times10) endpoint-and-gauge matrix has rank (8). Therefore the
endpoint-only part of the tangent kernel has dimension (2), and the
projection of (ker J) to residual space has dimension

\[
 9-2=7.                                                        \tag{12}
\]

Those seven residual directions obey exactly the following seventeen
independent linear equations:

\[
\begin{aligned}
 \dot M_{01}&=0,\\
 \dot M_{02}&\in\mathbf C E_{11},&
 \dot M_{13}&\in\mathbf C E_{11},\\
 \dot M_{23}&\in\mathbf C E_{00},&
 \dot M_{45}&\in\mathbf C E_{00},                             \tag{13}\\
 \dot m_{04}+\dot m_{15}-\dot m_{05}-\dot m_{14}&=0.
\end{aligned}
\]

The last equation is the tangent equation to the rank-one cross
rectangle. The checker proves that adjoining all seventeen rows to (J)
does not increase its rank. Since their common residual kernel has
dimension (24-17=7), (13) is not merely necessary: it is exactly the
residual projection of the infinitesimal solution space.

## 3. Nonlinear classification

Work on the local chart where the pure tangent coefficients, the four
cross weights, and (lambda,\mu) are nonzero.

On the complement (2345), the support permits only the matching
(23\mid45). The pure-zero equation is therefore

\[
 n_{00},M_{23}\otimes M_{45}=e_{0^4}.                         \tag{14}
\]

A nonzero decomposable tensor equals a pure coordinate tensor only if
both factors lie on the corresponding coordinate line. Hence

\[
 M_{23}=pE_{00},\qquad M_{45}=qE_{00},qquad n_{00}pq=1.       \tag{15}
\]

On the complement (0123), only (01\mid23) and (02\mid13)
survive:

\[
 n_{11}\bigl(M_{01}M_{23}+M_{02}M_{13}\bigr)=e_{1^4}.         \tag{16}
\]

Read (16) first on output pairs ((x_2,x_3)=(1,1),(1,0),(0,1)).
The first forces the column-one vectors of (M_{02}) and (M_{13}) to
be nonzero multiples of (e_1); the next two force both column-zero
vectors to vanish. The remaining ((0,0)) equation then forces
(M_{01}=0). Thus

\[
 M_{02}=\beta E_{11},\qquad
 M_{13}=\gamma E_{11},\qquad
 n_{11}\beta\gamma=1.                                       \tag{17}
\]

Finally, the first mixed equation in (9) reads

\[
 a_i d_j=\lambda\,g_i m_{ij}qquad(i=0,1; j=4,5).             \tag{18}
\]

It factors the cross-weight matrix, giving

\[
 m_{04}m_{15}=m_{05}m_{14}.                                  \tag{19}
\]

The second mixed equation gives the compatible factorization through
(b_i,c_j,\mu). Equations (15), (17), and (19) are exactly the integrated
forms of the infinitesimal constraints (13).

Every residual solution is a diagonal transform of the canonical packet.
Indeed, write the nonzero rank-one cross matrix as
(m_{ij}=r_i s_j). Independent diagonal scalings at sites (0,1,4,5)
realize (r_i,s_j); the remaining site-colour scalings independently
realize (p,q,\beta,\gamma). Differential covariance then proves (1) for
every classified member.

The two endpoint-only tangent directions in (12) integrate to reciprocal
rescalings of the two endpoint-factor pairs. They change neither residual
rank nor the four output slices.

## 4. An exact nontrivial integrated member

For a concrete audit, take

\[
 (p,q,\beta,\gamma)=(2,3,5,7),quad
 (r_0,r_1)=(11,13),quad(s_4,s_5)=(17,19).                     \tag{20}
\]

Thus (m_{ij}=r_i s_j). Choose

\[
\begin{aligned}
 (a_0,a_1)&=(r_0,-r_1),\\
 (b_0,b_1)&=\kappa(r_0,-r_1),
 &\kappa&=-\frac1{2r_0r_1pq},\\
 (c_4,c_5)&=\eta(s_4,s_5),
 &\eta&=\frac1{2s_4s_5\beta\gamma},\\
 (d_4,d_5)&=(s_4,s_5).                                       \tag{21}
\end{aligned}
\]

This one assignment realizes all four L0 slices exactly. Its residual
differential ranks over
(mathbf Q,mathbf F_{101},mathbf F_{32003},mathbf F_{1000003})
are (38) and (36) as in (1).

Put (X_2=I_2), all other (X_r=0), and all potentials zero. The selected
rows vanish. The internal blocks (M_{23}=2E_{00}) and
(M_{20}=5E_{11}) remain distinct pure-column R2 witnesses with nonzero
cofactors at the sole active root (2); the other five roots satisfy
preservation. Thus the deformation obstruction does retain the selected
(1I+5Z)/R2 data.

## 5. Exact audit

The standard-library checker
[verify_level_two_one_invertible_gauge_coupled_deformation_rigidity.py](../computations/verify_level_two_one_invertible_gauge_coupled_deformation_rigidity.py)

- differentiates all (40) equations with a rational first-jet algebra;
- verifies the Jacobian rank, nullity, residual projection, and
  endpoint-only tangent dimensions in (11)--(12);
- verifies that all seventeen independent rows in (13) are exact
  consequences of the Jacobian;
- constructs the nontrivial integrated member (20)--(21), checks its
  diagonal-orbit identity and all rational/modular ranks;
- directly sums all (256) binary eight-site slices; and
- audits the (1I+5Z) selected block and the six residual-R2 alternatives.

It passes normal, optimized, and isolated Python.
