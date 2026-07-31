# Hessian-kernel selector leakage is an anchored colour coboundary

## 1. Outcome

Work at one mixed scalar word of a six-site full-nine chart.  Let \(q\) be
the resulting scalar edge array, let

\[
 F=\operatorname {Haf}_6(q),
\]

and suppose the two endpoint stars have a separating coordinate selector.
After normalizing its row matrices \(A,B\) to the identity, the mixed
full-nine identity is

\[
                 \widehat H=-FC,
 \qquad C=A^{-\mathsf T}aB^{-1}.                       \tag{1}
\]

Here \(\widehat H\) is the selector-normalized cofactor matrix and \(a\)
is the fixed direct block.  This note proves an exact infinitesimal bridge
between the scalar Hessian obstruction and the cross-word selector
connection.

Let \(z\) be the scalar internal variation induced by one fixed-block probe
tangent, and assume

\[
                         H_qz=0,                         \tag{2}
\]

where \(H_q\) is the \(15\times15\) Hessian of the six-site hafnian.
Then the raw hafnian and every raw four-site cofactor are stationary:

\[
                  \dot F=0,\qquad \dot H_{\rm raw}=0.   \tag{3}
\]

Consequently, if the mixed target is tangent-zero, the entire normalized
cofactor leakage is connection data:

\[
 \boxed{\quad
     \Lambda=-F\dot C
       =F\bigl(X^{\mathsf T}a+aY\bigr),
     \qquad X=\dot A,\quad Y=\dot B.
 \quad}                                                   \tag{4}
\]

Suppose, in addition, that the same overlap transports the three labelled
diagonal target frames horizontally:

\[
 {d\over dt}\bigg|_{0}
   A(t)^{-\mathsf T}E_{cc}B(t)^{-1}=0
       \qquad(c=0,1,2).                                  \tag{5}
\]

Then \(X=\operatorname {diag}(x_0,x_1,x_2)\) and \(Y=-X\).  Formula (4)
becomes

\[
 \boxed{\qquad
       \Lambda_{ij}=F(x_i-x_j)a_{ij}.
 \qquad}                                                   \tag{6}
\]

Thus, on the saturated chart \(F\ne0\), the normalized leakage ratios on
the directed support of \(a\) are one exact colour coboundary.  In
particular every supported two-cycle and three-cycle has zero holonomy.
The following division-free identities hold even without dividing by
\(F\); for distinct \(i,j,k\),

\[
 \boxed{
 \begin{aligned}
  a_{ji}\Lambda_{ij}+a_{ij}\Lambda_{ji}&=0,\\
  a_{jk}a_{ki}\Lambda_{ij}
   +a_{ki}a_{ij}\Lambda_{jk}
   +a_{ij}a_{jk}\Lambda_{ki}&=0.
 \end{aligned}}                                           \tag{7}
\]

The result does **not** prove that the physical full-nine overlap supplies
(5), nor that its curvature normal is a nonzero holonomy in (7).  Those
are now the two sharply separated tasks.  An exact corank-one scalar guard
has \(H_qz=0\) and nonzero four-cycle curvature on \(z\), showing that (2)
alone cannot provide either statement.  Hence this is a source-relative
reduction, not an active-clean-point theorem or a proof of Krenn's
conjecture.

## 2. Hessian-kernel variations freeze the raw matching data

Use the six-site square-zero algebra

\[
 {\cal A}=\mathbb C[x_0,\ldots,x_5]/(x_0^2,\ldots,x_5^2).
\]

Regard \(q,z\in{\cal A}_2\).  Multiplication by \(q\),

\[
 L_q:{\cal A}_2\longrightarrow{\cal A}_4,
 \qquad b\longmapsto bq,                                \tag{8}
\]

is the weighted \(K_6\) Hessian after indexing a four-set by its
complementary edge.  Therefore (2) is exactly

\[
                              zq=0.                       \tag{9}
\]

The raw cofactor vector is the coefficient vector of \(q^{[2]}\).  Its
derivative in direction \(z\) is \(zq\), proving the second equality in
(3).  The derivative of the top hafnian is the all-six-sites coefficient
of \(zq^{[2]}\).  But

\[
                    zq^{[2]}={1\over2}(zq)q=0,           \tag{10}
\]

so \(\dot F=0\) as well.  This proof uses no invertibility and remains
valid at every Hessian corank.

Notice the consequence for the literal top rows.  With direct and star
data fixed, their internal variation is

\[
 a_{ij}zq^{[2]}+p_is_jzq=0                               \tag{11}
\]

for all nine ordered labels.  Thus diagonal anchors are vertically blind
to a Hessian-kernel direction.  They can act only through the direct/star
companions forced by a source-faithful overlap.

## 3. The normalized leakage identity

Let \(M=P^{\mathsf T}H(q)S\) be the scalarized response-cofactor matrix.
On the inverse selector chart put

\[
 \widehat H=A^{-\mathsf T}MB^{-1},\qquad
 \widehat D=A^{-\mathsf T}{\cal D}B^{-1},\qquad
 C=A^{-\mathsf T}aB^{-1}.                                \tag{12}
\]

The full-nine word identity is

\[
                         \widehat H=\widehat D-FC.       \tag{13}
\]

At the mixed base word, \({\cal D}=0\).  Assume the chosen fixed-block
probe tangent is also tangent to the pure-target-zero locus, so

\[
                            \dot{\widehat D}=0.           \tag{14}
\]

Normalize \(A(0)=B(0)=I\) and write \(X=\dot A(0)\),
\(Y=\dot B(0)\).  Direct differentiation gives

\[
                         \dot C=-X^{\mathsf T}a-aY.      \tag{15}
\]

Let \(H_{\rm raw}\) be the physical \(3\times3\) cofactor submatrix
selected by the separating shores.  At the base point it equals
\(\widehat H\).  Define the leakage matrix by

\[
                         \Lambda=\dot{\widehat H}
                                     -\dot H_{\rm raw}. \tag{16}
\]

Equations (3), (13)--(16) yield

\[
 \Lambda=-\dot F C-F\dot C-\dot H_{\rm raw}
         =-F\dot C
         =F(X^{\mathsf T}a+aY),                          \tag{17}
\]

which is (4).  In particular, on a Hessian-kernel tangent there is no
remaining raw-cofactor or top-hafnian contribution hidden inside
\(\Lambda\).

## 4. Diagonal-anchor transport gives a reciprocal connection

For each physical label \(c\), put

\[
                         T_c(t)=A(t)^{-\mathsf T}
                                  E_{cc}B(t)^{-1}.       \tag{18}
\]

At the normalized base,

\[
                         \dot T_c=-X^{\mathsf T}E_{cc}
                                      -E_{cc}Y.          \tag{19}
\]

Assume (5).  Looking at the entries in column \(c\) of (19) shows
\(X_{ci}=0\) for \(i\ne c\).  Looking at its entries in row \(c\) shows
\(Y_{cj}=0\) for \(j\ne c\).  Its \((c,c)\)-entry gives
\(X_{cc}+Y_{cc}=0\).  Doing this for all three labels proves

\[
 X=\operatorname {diag}(x_0,x_1,x_2),\qquad Y=-X.       \tag{20}
\]

Substitution into (17) proves (6).  Summing \(x_i-x_j\) around a two- or
three-cycle gives zero; multiplying by the relevant entries of \(a\)
clears every denominator and proves (7).

More invariantly, when \(F\ne0\), for any directed support graph of \(a\),
the vector

\[
            \left({\Lambda_{ij}\over Fa_{ij}}
                 \right)_{a_{ij}\ne0}                  \tag{21}
\]

lies in the image of the vertex--edge incidence map.  Hence it annihilates
the directed cycle space.  Formula (7) is the complete palette-three
readout needed without division.

## 5. Sharp scalar boundary and remaining physical task

The corank-one packet in
[the general \(K_6\) curvature theorem](general-k6-curvature-rowspace.md)
has

\[
 q_e=1\quad\text{for }e\in
 \{01,02,03,04,05,12,13,14,23,45\},                    \tag{22}
\]

and zero otherwise.  Its Hessian kernel contains

\[
                    z=e_{02}-e_{03}-e_{24}+e_{34}.      \tag{23}
\]

For

\[
                    \kappa(q)=q_{01}q_{23}-q_{02}q_{13},
\]

one has

\[
                         d\kappa_q(z)=-1.               \tag{24}
\]

Thus raw vertical blindness (3) is compatible with nonzero transverse
curvature.  The scalar packet has no selector connection or transported
diagonal target frames, so it does not test (5)--(7).

The exact next source statement exposed by this note is:

1. transport the three labelled diagonal frames through the same
   fixed-block overlap, proving (5), or identify its precise defect; and
2. show that the selected physical curvature/assignment packet has a
   nonzero leakage holonomy in (7), or supplies an additional
   grade-preserving row representing that holonomy.

If both hold, the contradiction is division-free.  If the first fails,
its nonzero frame derivative is itself the missing anchor-connection
class.  If the second fails, the leakage is a reciprocal target-torus
gauge and cannot detect the selected curvature.  This is strictly sharper
than asking the diagonal anchors to kill an arbitrary Hessian kernel
directly, which (11) proves impossible.

The dependency-free checker
[verify_hessian_kernel_anchored_selector_leakage_coboundary.py](../computations/verify_hessian_kernel_anchored_selector_leakage_coboundary.py)
audits the corank-one Hessian kernel and nonzero curvature, equations
(3)--(7) on exact rational matrices, and mutations of both the Hessian
kernel and diagonal-frame transport.
