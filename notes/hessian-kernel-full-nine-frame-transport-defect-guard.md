# Full-nine Hessian-kernel jets do not horizontally transport the diagonal frames

## 1. Outcome

Work at a separating mixed selector on six residual sites.  Let

\[
 T_c(t)=A(t)^{-\mathsf T}E_{cc}B(t)^{-1},
 \qquad c=0,1,2,                                      \tag{1}
\]

and normalize \(A(0)=B(0)=I\).  Put

\[
 X=A^{-1}\dot A,\qquad Y=B^{-1}\dot B.                \tag{2}
\]

The exact pulled-back frame defect is

\[
 \boxed{
 \Delta_c:=\dot T_c
   =-X^{\mathsf T}E_{cc}-E_{cc}Y.}                     \tag{3}
\]

At a nonnormalized point, the right side of (3) is conjugated by
\(A^{-\mathsf T}\) and \(B^{-1}\).  The three frames are horizontal if
and only if

\[
 X=\operatorname {diag}(d_0,d_1,d_2),
 \qquad Y=-X.                                          \tag{4}
\]

The mixed full-nine first jet does **not** force (4), even after imposing
all of the following stronger conditions:

* the internal tangent is nonzero and lies in the Hessian kernel of
  \(\operatorname {Haf}_6\);
* the six-site hafnian and every raw four-site cofactor are constant on
  the whole physical line;
* all nine mixed full-nine rows hold identically on that line;
* the selector stays separated, so normalized cofactor leakage is zero;
* the normalized direct block is constant; and
* the blocks come from one literal fixed-block array, so the certified
  power-free source-overlap identities hold coefficientwise.

Section 4 gives such a rational guard.  All three matrices in (3) are
nonzero there.

There is nevertheless a smaller positive statement.  The frame defect
canonically determines the leakage connection modulo a colour coboundary.
Its supported two- and three-cycle holonomies equal those of the actual
normalized leakage.  Hence zero leakage forces the cycle projections to
vanish even though the frames need not be horizontal.  In the guard the
resulting matrix is nonzero, and the cancellations are nonvacuous.

Thus full horizontality is too strong as the next source target.  For a
downstream four-cut transgression, the minimal live statement is transport
of the selected two- or three-cycle projection.  If literal horizontality
is desired instead, two regular diagonal polar transport rows are
sufficient and, without a target-aligned form already present, one is not.
No adjacent-chart full-nine completion or closure of Krenn's conjecture is
claimed.

## 2. The coordinate-free frame-defect lemma

Let \(L,R\) be the two three-dimensional endpoint row spaces and let the
three labelled rank-one targets be the paired frames
\(e_c^L\otimes e_c^R\).  A moving selector gives isomorphisms represented
by \(A(t),B(t)\).  Differentiating (1) at an arbitrary point gives

\[
 \dot T_c=-A^{-\mathsf T}
  \left(X^{\mathsf T}E_{cc}+E_{cc}Y\right)B^{-1},
 \qquad X=A^{-1}\dot A,\qquad Y=B^{-1}\dot B.          \tag{5}
\]

This is intrinsic: \(X,Y\) are the two selector connections, and the
middle tensor in (5) is their action on the labelled target frame.

**Lemma 2.1 (horizontal kernel).**  The linear map

\[
 \partial_{\rm fr}(X,Y)=
 \left(X^{\mathsf T}E_{cc}+E_{cc}Y\right)_{c=0}^2        \tag{6}
\]

has rank fifteen.  Its kernel is the three-dimensional reciprocal
diagonal algebra in (4).

**Proof.**  In the \(c\)-th component, the entries in column \(c\) are
the \(c\)-th row of \(X\), while the entries in row \(c\) are the
\(c\)-th row of \(Y\).  Vanishing away from \((c,c)\) makes both rows
diagonal, and the remaining entry is \(X_{cc}+Y_{cc}\).  Doing this for
all three colours proves (4).  The ambient connection space has dimension
eighteen, so the rank is fifteen.  \(\square\)

This shows exactly why constancy of one matrix such as the normalized
direct block is weaker.  If \(H_\times\) is the physical cross-cofactor
matrix, zero leakage gives only

\[
                  X^{\mathsf T}H_\times+H_\times Y=0.   \tag{7}
\]

When \(H_\times\) is invertible, (7) leaves the full nine-dimensional
stabilizer

\[
             Y=-H_\times^{-1}X^{\mathsf T}H_\times.     \tag{8}
\]

Nothing in (8) selects the three physical target axes.

## 3. What the named source equations actually imply

Use the notation of
[the anchored leakage note](hessian-kernel-anchored-selector-leakage-coboundary.md).
At a separating normalized base, let \(F=\operatorname {Haf}_6(q)\), let
\(H_\times\) be the raw cofactor submatrix between the two selector
shores, and let \(a\) be the fixed direct block.  The mixed full-nine row
is

\[
                         H_\times=-Fa.                  \tag{9}
\]

Suppose a physical fixed-block tangent induces \(z\) with
\(H_qz=0\), and is tangent to the pure-target-zero locus.  Then
\(\dot F=0\) and every raw cofactor is stationary.  Differentiating the
nine source rows and normalizing therefore gives exactly

\[
 \boxed{
 {\Lambda\over F}=X^{\mathsf T}a+aY.}                  \tag{10}
\]

Equation (10) is all that the mixed top rows say about the selector
connection.  The power-free source-overlap equations, namely (7) of
[the automatic two-chart packet](two-chart-joint-hypothesis-extraction.md)
and equivalently the representatives (20)--(23) of
[the filtered-provenance note](hessian-pullback-filtered-source-provenance.md),
retain the direct, star, and internal companions of the same fixed blocks.
They do not insert a nonzero diagonal target tensor at a mixed word whose
target and target tangent are both zero.  The fixed-block guard below
satisfies those universal overlap equations and still has nonzero (3).

There is, however, a quotient of (3) which (10) controls.  Define

\[
 \begin{aligned}
 \Phi_{ij}(\Delta,a)={}&
 -\sum_{k\ne i}(\Delta_k)_{ik}a_{kj}
 -\sum_{k\ne j}a_{ik}(\Delta_k)_{kj}
 -a_{ij}(\Delta_j)_{jj}.                             \tag{11}
 \end{aligned}
\]

Writing \(d_i=X_{ii}\), direct substitution of (3) gives

\[
 \boxed{
 \left({\Lambda\over F}\right)_{ij}
   =\Phi_{ij}(\Delta,a)+(d_i-d_j)a_{ij}}                \tag{12}
\]

The unobservable split of
\(X_{ii}+Y_{ii}=-(\Delta_i)_{ii}\) is precisely the colour potential
\(d\).  Thus \(\Phi\) reconstructs the connection modulo the exact
coboundary \((d_i-d_j)a_{ij}\).

For distinct labels, put

\[
 \begin{aligned}
 \mathcal H^{(2)}_{ij}(Z)
   &=a_{ji}Z_{ij}+a_{ij}Z_{ji},\\
 \mathcal H^{(3)}_{ijk}(Z)
   &=a_{jk}a_{ki}Z_{ij}
     +a_{ki}a_{ij}Z_{jk}
     +a_{ij}a_{jk}Z_{ki}.                              \tag{13}
 \end{aligned}
\]

The coboundary in (12) telescopes, so

\[
 \boxed{
 \mathcal H^{(r)}(\Phi(\Delta,a))
   =\mathcal H^{(r)}(\Lambda/F),
 \qquad r=2,3.}                                        \tag{14}
\]

Equivalently,

\[
 F\,\mathcal H^{(r)}(\Phi(\Delta,a))
       =\mathcal H^{(r)}(\Lambda),\qquad r=2,3,          \tag{14a}
\]

which is the division-free form of the two- and three-cycle identities in
the anchored leakage note, now expressed solely through the moving target
frames.  In particular, \(\Lambda=0\) makes all these projections zero
without making any individual \(\Delta_c\) zero.

## 4. An exact physical rotating-frame guard

Take residual sites \(0,\ldots,5\), with shores

\[
                         X=(0,1,2),\qquad Y=(3,4,5).    \tag{15}
\]

In the scalar site-square-zero algebra put

\[
 \begin{aligned}
 q={}&x_0x_1+x_0x_2+x_0x_4+x_0x_5+x_1x_2
       +x_1x_4+x_2x_3+x_3x_4+x_3x_5,\\
 z={}&x_0x_1-x_1x_3=x_1(x_0-x_3).                      \tag{16}
 \end{aligned}
\]

Direct multiplication gives

\[
                         zq=0,\qquad z^{[2]}=0.         \tag{17}
\]

Consequently the whole line \(q_t=q+tz\) has constant divided square and
cube.  In particular,

\[
 F=\operatorname {Haf}_6(q_t)=4,\qquad
 H(q_t)=H(q),                                           \tag{18}
\]

so \(z\ne0\) is a genuine Hessian-kernel tangent and every raw cofactor is
constant, not merely stationary.  The cross-cofactor matrix is

\[
 H_\times=
 \begin{pmatrix}
 0&1&2\\
 0&2&2\\
 1&1&1
 \end{pmatrix},\qquad \det H_\times=-2,                \tag{19}
\]

and take the fixed direct block \(a=-H_\times/4\).

Let

\[
 N=\begin{pmatrix}
 1&1&-2\\1&1&-2\\1&1&-2
 \end{pmatrix},\qquad N^2=0,                           \tag{20}
\]

and define

\[
 \begin{aligned}
 A(t)&=I+tN,\\
 B(t)&=H_\times^{-1}A(t)^{-\mathsf T}H_\times=I+tY,\\
 Y&=\begin{pmatrix}
 \tfrac52&10&\tfrac{25}2\\
 0&0&0\\
 -\tfrac12&-2&-\tfrac52
 \end{pmatrix},\qquad Y^2=0.                           \tag{21}
 \end{aligned}
\]

Support the first endpoint star only on \(X\), with selected row matrix
\(A(t)\), and support the second only on \(Y\), with selected row matrix
\(B(t)\).  The selector remains separated.  Equations (19)--(21) give

\[
 P(t)^{\mathsf T}H(q_t)S(t)
     =A(t)^{\mathsf T}H_\times B(t)=H_\times=-Fa.       \tag{22}
\]

Thus all nine mixed full-nine equations hold identically, including their
second jet.  Moreover,

\[
 A(t)^{-\mathsf T}H_\times B(t)^{-1}=H_\times,
 \qquad A(t)^{-\mathsf T}aB(t)^{-1}=a.                  \tag{23}
\]

Hence \(\Lambda=0\), the normalized cofactor is constant, and the
normalized direct block is constant.

This packet is literally fixed-block.  Choose physical probes

\[
 \begin{array}{c|cccccc}
 i&0&1&2&3&4&5\\ \hline
 u_i&e_0&e_0&e_1&e_1&e_2&e_2\\
 v_i&e_1&e_1&e_2&e_2&e_0&e_0
 \end{array}                                             \tag{24}
\]

and use the line \(u_i(t)=u_i+tv_i\).  Each \((u_i,v_i)\) extends to a
local basis.  In those adapted bases, give the internal block on \(ij\)
the values

\[
 Q_{ij}(u_i,u_j)=q_{ij},\quad
 Q_{ij}(v_i,u_j)=z_{ij},\quad
 Q_{ij}(u_i,v_j)=Q_{ij}(v_i,v_j)=0.                    \tag{25}
\]

Give the two endpoint blocks their constant and tangent selected rows from
\((I,N)\) and \((I,Y)\), respectively, and set every opposite-shore star
row to zero.  These prescriptions are entries of fixed bilinear matrices;
they produce exactly (16) and (21).  For each physical colour there are
two sites at which both its \(u_i\)- and \(v_i\)-coordinates vanish, so all
three pure target monomials vanish identically on the line.

Because this is one fixed block array, the power-free overlap identities
hold before evaluation.  The checker verifies all 108 instances of the
two identities in (7) of the automatic two-chart packet for the exposed
sites \(p,q,0,1\) and every repeated or distinct colour choice.

Nevertheless (3) gives

\[
 \begin{aligned}
 \Delta_0&=
 \begin{pmatrix}-\tfrac72&-10&-\tfrac{25}2\\-1&0&0\\2&0&0\end{pmatrix},&
 \Delta_1&=
 \begin{pmatrix}0&-1&0\\0&-1&0\\0&2&0\end{pmatrix},\\[2mm]
 \Delta_2&=
 \begin{pmatrix}0&0&-1\\0&0&-1\\\tfrac12&2&\tfrac92\end{pmatrix}.
                                                               \tag{26}
 \end{aligned}
\]

All three frames rotate.  With \(d=(1,1,-2)\), formula (11) gives the
nonzero matrix

\[
 \Phi(\Delta,a)=
 \begin{pmatrix}
 0&0&\tfrac32\\
 0&0&\tfrac32\\
 -\tfrac34&-\tfrac34&0
 \end{pmatrix},                                        \tag{27}
\]

and (12) is the exact identity

\[
             0={\Lambda\over F}
               =\Phi(\Delta,a)+(d_i-d_j)a_{ij}.        \tag{28}
\]

The two-cycle cancellations on \(0\leftrightarrow2\) and
\(1\leftrightarrow2\), and the directed three-cycle cancellation, each
contain nonzero summands.  Thus (14) is not vacuous: the frame defect is
visible, but its cycle class is zero.

## 5. The smallest additional transport input

For literal horizontality there is a sharp basis-free two-polar test.
Let

\[
 D_\rho=\sum_c\rho_cE_{cc},\qquad
 D_\sigma=\sum_c\sigma_cE_{cc},                         \tag{29}
\]

with every \(\rho_c\ne0\) and the three ratios
\(\sigma_c/\rho_c\) pairwise distinct.

**Lemma 5.1 (two regular polars).**  The two matrix transport rows

\[
 X^{\mathsf T}D_\rho+D_\rho Y=0,\qquad
 X^{\mathsf T}D_\sigma+D_\sigma Y=0                    \tag{30}
\]

hold if and only if all three labelled frames are horizontal.

**Proof.**  The first equation gives
\(Y=-D_\rho^{-1}X^{\mathsf T}D_\rho\).  Substitution in the second says
that \(X^{\mathsf T}\) commutes with the simple-spectrum diagonal
operator \(D_\sigma D_\rho^{-1}\).  Hence \(X\) is diagonal, and the
first equation gives \(Y=-X\).  The converse is immediate.  \(\square\)

One nondegenerate polar row leaves arbitrary \(X\) and determines only
\(Y\), so it has a nine-dimensional kernel and cannot imply (4).  The two
rows in (30) have rank fifteen and their kernel is exactly (4).  Thus two
transported diagonal polars are the smallest universally sufficient
physical compatibility for full horizontality.  If (7) is already a
target-diagonal regular polar, one further row can suffice on that special
aligned chart.  The dense matrix (19) is not such a chart.

The source statement still missing is not the existence of the three
diagonal top rows at their constant words.  It is the faithful transport
of two regular linear combinations of those rows into the same mixed
selector chart.  The mixed target-zero rows and the universal Bianchi
identities do not perform that transport, as the guard proves.

For the cycle-based continuation, (30) is unnecessary.  Equation (14)
shows that the strictly smaller input is one source-provenant comparison
which identifies the chosen physical four-cut curvature row with a
nonzero \(\mathcal H^{(2)}\) or \(\mathcal H^{(3)}\) projection.  That
single cycle row is invariant under the surviving colour potential and is
therefore the minimal live anchor-transport gate exposed here.

## 6. Audit and scope

The dependency-free checker
[verify_hessian_kernel_full_nine_frame_transport_defect_guard.py](../computations/verify_hessian_kernel_full_nine_frame_transport_defect_guard.py)
audits over the rationals:

* (17)--(19), including the nonzero Hessian-kernel tangent and constancy of
  every raw cofactor on four rational points of the exact line;
* a literal fixed-block realization of (16), (20)--(25), all nine mixed
  rows, and all 108 power-free overlap identities;
* the exact three nonzero defects (26), the exact matrix (27), the
  reconstruction (12), and every two- and oriented three-cycle identity
  (14), including the nonvacuous \(0\to1\to2\to0\) cancellation;
* rank fifteen of the complete frame-defect map, rank nine for one polar,
  and equality of the two-regular-polar kernel with the horizontal kernel.

The guard satisfies one complete mixed \(pq\) full-nine system on the
displayed physical line and all universal source-overlap identities of its
fixed block array.  It does **not** satisfy or claim the complete target
full-nine systems on every adjacent deleted-pair chart, nor the all-probe
ternary source identity.  Those additional physical coefficient rows may
still supply the cycle-projected transport gate.  Accordingly this is a
sharp first-jet and overlap boundary, not a full source, a no-source
theorem, or a proof of Krenn's conjecture.
