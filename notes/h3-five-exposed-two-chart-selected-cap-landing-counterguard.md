# The five-exposed selected-cap packet does not supply the grade-split landing

Research boundary only.  The unified full-nine theorem, **SP-CLEAN-BRIDGE**,
and Krenn's conjecture remain open.  No certified dependency is changed.

## 1. Outcome and exact scope

At \(h=3\), the smallest five-exposed two-chart coefficient packet still
does not imply

\[
                 \Theta-\chi_C\kappa=0.                    \tag{1}
\]

There is one exact rational shared-block packet with all of the following
properties.

1. One compatible separating residual word is used in both the `pq` and
   `pr` charts.
2. All nine selected scalar cap coefficients vanish in each chart: eighteen
   cap coefficients in total.
3. Both endpoint-star triples in both charts are injective.
4. The three diagonal target matrix units are retained in the anchor-frame
   reconstruction, and every one of their three frame defects contributes
   nontrivially to the anchor cycle.
5. The power-free connection, normal, curvature, and direct-double rows hold
   literally on the shared physical blocks.
6. One complete crossed four-index slice is target-zero.
7. The `pr` direct block is identically zero, while the physical curvature
   minor is nonzero.

Nevertheless

\[
       \Theta=0,
       \qquad \chi_C=1,
       \qquad \kappa=-\frac14,
       \qquad \Theta-\chi_C\kappa=\frac14.                \tag{2}
\]

The word **selected** is essential.  The eighteen rows here are the eighteen
scalar coefficients obtained after fixing one residual word, not the full
tensor-valued nine equations in each chart over every residual word.  At
\(h=3\), the tensor-valued nine-row system is the full eight-site exact-source
equation system.  Nothing below constructs a ternary source or a counterexample
to that system.

Thus (2) is a sharp bounded coefficient counterguard.  It rules out deriving
(1) from the selected five-site coefficients, the universal overlap rows, and
the diagonal anchor-frame bookkeeping alone.  A positive proof must use a
coupling between different residual words in the full EqSystem, the
maximum-anchor/minimum-support conditions, or a genuinely new grade-split
source identity.

## 2. The base `pq` chart

Use six residual ports \(0,1,2,3,4,5\) and the scalar quadratic

\[
 q=01+02+04+05+12+14+23+34+35.                              \tag{3}
\]

Give these ports the physical labels

\[
                         (0,1,2,0,1,2).                      \tag{4}
\]

The two endpoint-star triples are

\[
 x_0=e_0,\quad x_1=e_1,\quad x_2=e_2,
 \qquad
 y_0=e_3,\quad y_1=e_4,\quad y_2=e_5.                        \tag{5}
\]

They both have rank three.  Direct matching enumeration gives

\[
 \operatorname {Haf}(q)=4,
 \qquad
 H_\times=
 \begin{pmatrix}
 0&1&2\\0&2&2\\1&1&1
 \end{pmatrix}.                                             \tag{6}
\]

Put

\[
 A_{pq}=-\frac14H_\times
 =\begin{pmatrix}
 0&-1/4&-1/2\\
 0&-1/2&-1/2\\
 -1/4&-1/4&-1/4
 \end{pmatrix}.                                             \tag{7}
\]

For every \(i,j\in\{0,1,2\}\), the selected scalar full-nine coefficient is

\[
 A_{pq}(i,j)\operatorname {Haf}(q)
   +\sum_{u\ne v}x_i(u)y_j(v)
      \operatorname {Haf}(q|_{[6]\setminus\{u,v\}})=0.     \tag{8}
\]

Equation (8) is the exact scalar coefficient of the cap equation on the
mixed residual word (4).  Its target evaluation is zero, including when
\(i=j\).

## 3. A literal direct-free `pr` companion

Take

\[
                         r=3,\qquad s=2,\qquad x=0.           \tag{9}
\]

The exposed physical labels are

\[
                         (p,q,r,s)=(2,0,0,2).                 \tag{10}
\]

In the `pq` chart, order the residual sites as
\((r,s,x,1,4,5)\).  In the `pr` chart replace \(r\) by \(q\).  Both
selected residual words are

\[
                         (0,2,0,1,1,2),                      \tag{11}
\]

which is a permutation of \(001122\).  After exposing \(p,q,r,s,x\), the
common set \(D_5=\{1,4,5\}\) has three sites, as required at \(h=3\).

In the `pr` chart, the residual \(q\)-port is isolated in the internal
quadratic because \(y_0=e_3\) and port \(3=r\) has been deleted.  The three
\(p\)-stars are

\[
 \widetilde x_0=e_0,\qquad
 \widetilde x_1=e_1,\qquad
 \widetilde x_2=e_2-\frac14e_q,                             \tag{12}
\]

and the three \(r\)-stars are

\[
 t_0=e_q+e_2+e_4+e_5,
 \qquad t_1=e_0,
 \qquad t_2=e_1.                                            \tag{13}
\]

Both triples have rank three.  The five-port internal cofactor functional
on the common part is

\[
                  (t(0),t(1),t(2),t(4),t(5))
                     \longmapsto t(2)+t(4)+2t(5).            \tag{14}
\]

The \(e_q\)-term in \(t_0\) cancels the value of (14), while \(t_1,t_2\)
already lie in its kernel.  Hence every one of the nine `pr` response
coefficients is zero.  Taking

\[
                              A_{pr}=0                       \tag{15}
\]

gives all nine selected `pr` cap coefficients exactly.  The shared
\(p-r\) and \(q-r\) columns agree with (5)--(7), so (12)--(15) are not an
independently relabelled chart: they are entries of one physical scalar
block packet.

Together, (8) and (15) are the promised eighteen selected cap coefficients.
The checker also enumerates all \(3^4=81\) complementary words after fixing
(10); the complete crossed four-index tensor slice is zero.

## 4. The overlap rows and the nonzero minor

At the selected labels, use the standard notation

\[
 (A,B,C,E,F,U)
 =\bigl(A_{pq},A_{pr},A_{qr},A_{ps},A_{qs},A_{rs}\bigr).
\]

The packet gives

\[
        (A,B,C,E,F,U)=\left(-\frac14,0,1,1,0,1\right),
        \qquad \kappa=AU-BF=-\frac14.                       \tag{16}
\]

On the four-site complement of \(p,q,r,s\), put

\[
 z=01+04+05+14,
 \qquad \chi_C=\operatorname {Haf}(z)=1.                   \tag{17}
\]

Writing \(x,y,t,v\) for the selected endpoint stars restricted to this
four-site complement, direct expansion verifies

\[
\begin{aligned}
 (Az+xy)t-(Bz+xt)y&=(At-By)z,\\
 L_{pq;r}-L_{pr;q}&=-2(At-By),\\
 U(Az+xy)+tH-F(Bz+xt)-yN
   &=(At-By)v+\kappa z,\\
 M_{pq;rs}-M_{pr;qs}&=-2\kappa .                           \tag{18}
\end{aligned}
\]

Before the two Euler cancellations, the four top coefficients are

\[
          (\text{curvature},\text{direct},
            \text{connection},\text{normal})
       =\left(-\frac12,\frac12,-\frac34,\frac34\right).     \tag{19}
\]

Thus neither the high nor the low pair is vacuous.  The fact that the whole
`pr` direct block vanishes does not kill the curvature minor or any of the
literal triangular overlap rows.

## 5. The diagonal anchor cycle and the rank jump

Retain the three diagonal target frames

\[
                           E_{00},E_{11},E_{22}.              \tag{20}
\]

They are linearly independent.  Use the same exact cofactor-preserving
connections as in the adjacent-cycle audit:

\[
 X=\begin{pmatrix}1&1&-2\\1&1&-2\\1&1&-2\end{pmatrix},
 \qquad
 Y=\begin{pmatrix}
 5/2&10&25/2\\0&0&0\\-1/2&-2&-5/2
 \end{pmatrix}.                                             \tag{21}
\]

They satisfy

\[
             X^{\mathsf T}H_\times+H_\times Y=0,
 \qquad     X^{\mathsf T}A_{pq}+A_{pq}Y=0.                  \tag{22}
\]

Every diagonal frame defect

\[
              \Delta_c=-X^{\mathsf T}E_{cc}-E_{cc}Y         \tag{23}
\]

is nonzero.  After the division-free anchor reconstruction, their three
oriented cycle contributions are

\[
                     -\frac9{64},\qquad
                     -\frac3{32},\qquad
                      \frac{15}{64}.                         \tag{24}
\]

All three are nonzero and their sum is zero.  Consequently

\[
                    \Theta=4\Psi_C=0,
             \qquad \Xi=0,                                  \tag{25}
\]

where \(\Xi\) is the crossed cycle projection.

On coordinates

\[
                  (\Theta,\Xi,\kappa,C,D,L,N),              \tag{26}
\]

the retained grade rows are

\[
 R=\begin{pmatrix}
 1&-1&0&0&0&0&0\\
 0& 1&0&0&0&0&0\\
 0& 0&-2&1&0&0&0\\
 0& 0& 2&0&1&0&0\\
 0& 0& 0&0&0&1&1
 \end{pmatrix}.                                             \tag{27}
\]

The landing row is

\[
                         T=(1,0,-1,0,0,0,0).                 \tag{28}
\]

Exact rational elimination gives

\[
                  \operatorname {rank}R=5,
       \qquad \operatorname {rank}\binom RT=6.              \tag{29}
\]

The physical separating value vector is

\[
              w=\left(0,0,-\frac14,-\frac12,
                         \frac12,-\frac34,\frac34\right).    \tag{30}
\]

Every row of \(R\) kills \(w\), whereas

\[
                              T(w)=\frac14.                  \tag{31}
\]

The eighteen selected cap coefficients and the complete crossed slice are
already zero on this same shared-block packet.  The diagonal target matrices
are retained in (20)--(24), not discarded.  Equations (29)--(31) therefore
give the exact bounded row-span obstruction promised in Section 1.

## 6. A tilted auxiliary packet

The obstruction is not merely a consequence of having a zero selected
corner.  Keep \(q\) from (3), but tilt

\[
                  x_0=e_0+e_1,
          \qquad y_1=e_2+e_4,                               \tag{32}
\]

and now take \(r=1,s=2,x=0\) with exposed labels
\((p,q,r,s)=(0,1,1,2)\).  Solving the two selected cap tables gives

\[
 A_{pq}=\begin{pmatrix}
 0&-3/2&-1\\0&-1&-1/2\\-1/4&-1/4&-1/4
 \end{pmatrix},
 \qquad
 A_{pr}=\begin{pmatrix}
 0&1&1/4\\0&1&1/2\\-1/4&0&1/8
 \end{pmatrix}.                                             \tag{33}
\]

The second matrix has rank three, and both star triples in both charts still
have rank three.  At the selected square,

\[
             (A,B,F,U)=\left(-\frac32,1,1,1\right),
             \qquad \kappa=-\frac52.                        \tag{34}
\]

Here \(\chi_C=2\), and the four Euler top coefficients are

\[
                         (-10,10,-5,5).                      \tag{35}
\]

All eighteen selected cap coefficients and the complete crossed slice again
vanish.  This auxiliary is a coexistence calibration only: it verifies that
the selected-cap and overlap packet coexists with a fully tilted, active
second chart and a nonzero four-corner curvature square.  It is not a tilted
landing separator and is not used to transport the particular base-frame
normalization (21), so the explicit landing separator remains (30).

## 7. Consequence for the unified route

The bounded \(h=3\) coefficient flank has a negative answer: merely adding
the five-exposed selected cap coefficients to the adjacent-full-nine and
sum-channel guards does not manufacture the grade-split row.

This only kills the raw landing identity.  It does not rule out the weaker
filtered mechanism isolated in
[`filtered-d2-bockstein-fast-path.md`](filtered-d2-bockstein-fast-path.md):
the bad component may die on the first page while a nonzero second
differential survives in the low quotient.  The shortest next experiment is
therefore to construct the target-augmented three-step \(h=3\) source
complex, verify the components of \(d^2=0\), and compute its proposed
\(d_2\) together with the target/residue readout and first-page
zero-indeterminacy.

Only if that smaller filtered experiment fails to form a complex or cannot
settle the readout should one fall back to the complete tensor-valued
eight-site EqSystem: adjoin the maximum-anchor/minimum-support and good-star
standard opens, localize at the chosen curvature minor, and test the relevant
saturated ideal or source-row module.  A selected residual word cannot decide
either cross-word problem: (2) is its exact raw-row obstruction.

The dependency-free
[checker](../computations/verify_h3_five_exposed_two_chart_selected_cap_landing_counterguard.py)
enumerates the shared eight-site scalar matching coefficients.  It verifies
the \(9+9\) selected cap rows, all \(81\) coefficients of the crossed slice,
the four star ranks, the direct-free and tilted blocks, the overlap identities,
the three diagonal frame defects, and the rank jump (29) over
\(\mathbb Q\).
