# Diagonal anchors descend the double-zero packet by two polar degrees

## 1. Outcome

Retain the double-hafnian-zero branch of the
[two-chart synchronization theorem](two-chart-hamming-one-gamma-synchronization.md).
On one deleted-pair chart, fix the pure colour \(\delta\), let \(I,J\)
be its two pure endpoint channels, and put

\[
 A=I^c,\qquad B=J^c,\qquad C=P_{A,B}\ne0.                 \tag{1}
\]

The synchronized branch has \(\delta\in I\cap J\), so \(A,B\) are
nonempty subsets of the other two physical labels.  Completing the
seven-row ledger with its two missing diagonal rows has three exact
consequences; the contractions below use the resulting full-nine system.

1. On every binary face \(\{\delta,e\}\), the uniform internal hafnian is
   divisible by \(t^2\) at the pure \(\delta\) point.  After factoring
   this guaranteed power, the compressed full-nine identity has degree at
   most \(2h-2\).  The zero may have higher order.
2. If a missing diagonal matrix unit survives modulo \(\mathbb C C\), it
   produces a literal full-binary, source-provenant cap
   \(r q_{\delta e}^{[h-1]}=X_e\).  More invariantly, a rank-one
   isotropic contraction of \(C\) gives a nonzero unary or binary
   full-colour cap unless \(C\) is in one of the two sharp coordinate-cell
   boundary cases.
3. If both chart compressions admit diagonal-detecting functionals
   normalized on the same missing label \(e\), their common three-site
   overlap has two exact normal rows.  Subtracting them leaves the
   grade-preserving cubic

   \[
   \boxed{
   \left(Ut_e-U'y_e+{L_e-L'_e\over h-1}z\right)z^{[h-2]}=0.}
                                                                  \tag{2}
   \]

No factor \(z^{[h-2]}\) may be cancelled.  Thus (2), rather than another
coefficient of the one-parameter contraction, is the first unresolved
source-relative anchor coefficient.

There are two further sharpenings.  Every nonzero isotropic target selects
an explicit pair which is a cofactor hole in the pure \(\delta\) slice and
active in the target-colour slice.  Also, the pure \(\delta\) coefficient
of the literal 27-row overlap gives

\[
             T_{jk}[x_i z^{[h-1]}]_{\delta^D}=0
             \quad\hbox{for all }i,j,k,                         \tag{3}
\]

so either the cross block \(T=A_{qr}\) vanishes or all common
\(p\)-star cohafnians vanish.

These statements do not close the packet.  A new exact eight-site guard
satisfies both missing diagonal rows, (1), the synchronized pure data,
four good stars, nonzero curvature, and the nonzero-\(T\) branch of (3),
while failing precisely the off-diagonal rows.  It is sharply
complementary to the seven-row guard, which satisfies the six
off-diagonal rows and the \(\delta\)-diagonal row but omits the other two
diagonal rows.  Therefore the next positive step must mix the diagonal
anchors with the off-diagonal rows before passing to the odd residue or
the common-power quotient.

## 2. The binary two-degree quotient

Let \(W\) be the residual set of one chart, \(|W|=2h\), with the inherited
range \(h=m-1\ge3\), and fix \(e\ne\delta\).  Work over \(\mathbb C\) in
the site-square-zero algebra, with all matching powers divided.  Write the
literal full-nine equations as

\[
 P_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                      \tag{4}
\]

Scalarize every residual colour space by

\[
 e_\delta\longmapsto z_x,\qquad
 e_e\longmapsto t z_x,\qquad
 e_f\longmapsto0\quad(f\notin\{\delta,e\}).             \tag{5}
\]

The scalarized internal quadratic and endpoint stars have the form

\[
 Q(t)=Q_0+tQ_1+t^2Q_2,qquad
 p_A(t)=tU,qquad s_B(t)=tV.                              \tag{6}
\]

The last two identities use the definitions of \(I,J\): every pure
\(\delta\) local coefficient of a row in \(A\), or a column in \(B\),
is zero.  Here \(U\) and \(V\) are respectively the site-by-\(A\) and
site-by-\(B\) coefficient matrices, and \(H(Q(t))\) is the residual-site
cohafnian matrix.  Put

\[
 F(t)=\operatorname {haf}Q(t).
\]

Compressing (4) to \(A\times B\) gives the exact polynomial identity

\[
 F(t)C+t^2U^{\mathsf T}H(Q(t))V
       =t^{2h}(E_{ee})_{A,B}.                              \tag{7}
\]

Choose a nonzero entry of \(C\).  The other two terms in that scalar
entry are divisible by \(t^2\), so \(F(t)=t^2G(t)\).  Hence

\[
 \boxed{
 G(t)C+U^{\mathsf T}H(Q(t))V
       =t^{2h-2}(E_{ee})_{A,B}.}                           \tag{8}
\]

This recovers the pure coefficient and the aggregate Hamming-one sum,
consistent with the already known coefficientwise Hamming-one vanishing.
The first coefficient of (8) is the sum of the Hamming-two rows; a uniform
one-parameter contraction does not separate their residual sites.  Return
instead to the unspecialized binary word equations.  For distinct
\(x,y\in W\), let

\[
 f_{xy}^{e}=[q^{[h]}]_{e_xe_y\delta^{W\setminus\{x,y\}}},
 \qquad
 h_{xy}^{\delta}
   =\operatorname {haf}(Q_\delta[W\setminus\{x,y\}]).       \tag{9}
\]

Then

\[
 f_{xy}^{e}C+h_{xy}^{\delta}
 \left(p_{A,x}(e)s_{B,y}(e)^{\mathsf T}
      +p_{A,y}(e)s_{B,x}(e)^{\mathsf T}\right)=0.          \tag{10}
\]

There is no factorial in (10): after the two outside-channel stars occupy
the two defect sites, the remaining sites are paired by one divided
matching power.

For reference, divided-power expansion of (6) gives

\[
 [t^k]F(t)
 =\sum_{a+b+c=h\atop b+2c=k}
       [Q_0^{[a]}Q_1^{[b]}Q_2^{[c]}].                       \tag{11}
\]

In particular

\[
\begin{aligned}
 [t^2]F&=[Q_2Q_0^{[h-1]}+Q_1^{[2]}Q_0^{[h-2]}],\\
 [t^3]F&=[Q_1Q_2Q_0^{[h-2]}+Q_1^{[3]}Q_0^{[h-3]}].          \tag{12}
\end{aligned}
\]

The quotient \(G\) is a global sum of two-defect coefficients.  It is not
in general the hafnian of a quadratic on a fixed \((2h-2)\)-site set.
Thus (8) is a two-degree polar descent, not an \(N\mapsto N-2\)
inductive descent.

## 3. Full binary caps and the coordinate-cell boundary

Let \(q_{\delta e},p_i^{\delta e},s_j^{\delta e}\) denote the literal
projection of the residual decorated source to colours \(\delta,e\).
Before uniform scalarization, (4) restricted to \(A\times B\) is

\[
 Cq_{\delta e}^{[h]}
 +p_A^{\delta e}(s_B^{\delta e})^{\mathsf T}
       q_{\delta e}^{[h-1]}
 =(E_{ee})_{A,B}X_e.                                      \tag{13}
\]

Consequently, if

\[
 \ell(C)=0,\qquad \ell((E_{ee})_{A,B})=1,                \tag{14}
\]

then

\[
 r_{\ell,e}q_{\delta e}^{[h-1]}=X_e,qquad
 r_{\ell,e}=\sum_{i\in A,j\in B}\ell_{ij}
          p_i^{\delta e}s_j^{\delta e}.                   \tag{15}
\]

This is a full binary tensor identity: all mixed \(\delta/e\) words
vanish.  Applying \(\ell\) to (4) before projecting gives the stronger
full-colour identity

\[
 \left(\sum_{i,j}\ell_{ij}p_is_j\right)q^{[h-1]}
   =\sum_{c\in A\cap B}\ell(E_{cc})X_c.                  \tag{16}
\]

There is a useful rank-one version.  For
\(\xi\in\mathbb C^A,\eta\in\mathbb C^B\), summing (4) against
\(\xi\eta^{\mathsf T}\) gives

\[
 (\xi^{\mathsf T}C\eta)q^{[h]}
 +p(\xi)s(\eta)q^{[h-1]}
 =\sum_{c\in A\cap B}\xi_c\eta_cX_c.                   \tag{17}
\]

Thus every isotropic pair \(\xi^{\mathsf T}C\eta=0\) with a nonzero
diagonal product produces a literal unary or binary rank-one cap.  Such a
pair fails to exist exactly in one of the following cases:

1. \(A\cap B=\varnothing\); since \(A,B\) are nonempty subsets of two
   labels, they are opposite singletons and \(C\) is their sole
   off-diagonal coordinate cell;
2. \(A\cap B=\{k\}\) and \(C\) is supported only at \((k,k)\).

Indeed, in the second case isotropy kills the only possible target
coefficient.  Conversely, if \(C\) has any other entry, its coefficient
can cancel \(C_{kk}\) while \(\xi_k\eta_k\ne0\).  If
\(A=B=\{e,f\}\), choose \(\eta\in(\mathbb C^*)^2\) with
\(C\eta\ne0\) and put

\[
 \xi=((C\eta)_f,-(C\eta)_e).
\]

Then \(\xi^{\mathsf T}C\eta=0\), and at least one of
\(\xi_e\eta_e,\xi_f\eta_f\) is nonzero.  This proves the remaining
case without genericity.  The rank-one statement promises some nonzero
missing-colour target, not a prescribed one: for example, if
\(A=B=\{e,f\}\) and \(C=E_{ee}\), every isotropic target with a nonzero
diagonal coefficient may be chosen on \(f\), while an \(e\)-target is
impossible.  The exact criterion for the prescribed label \(e\) is (14).

Equivalently, if both restricted missing diagonal units vanish in
\(\operatorname {Mat}_{A,B}/\mathbb C C\), then the compression is
exactly one of the two coordinate-cell boundaries above.  Notice that a
zero restriction \((E_{ee})_{A,B}=0\) is different from a nonzero unit
which lies in \(\mathbb C C\).

## 4. The selected cofactor hole

The cap (17) carries an additional source-level certificate.  Put
\(L=p(\xi)\), \(S=s(\eta)\).  Since \(\xi,\eta\) are supported on
\(A,B\),

\[
                         L_{x,\delta}=S_{x,\delta}=0
                         \quad(x\in W).                       \tag{18}
\]

For \(x<y\), define the endpoint-oriented response coefficient

\[
 R_{xy}(a,b)=L_{x,a}S_{y,b}+S_{x,a}L_{y,b}.              \tag{19}
\]

The coefficient of the word with \(a,b\ne\delta\) at \(x,y\) and
\(\delta\) elsewhere in (17) is

\[
 R_{xy}(a,b)H_\delta(x,y)=0,qquad
 H_c(x,y)=\operatorname {haf}
       (Q_c[W\setminus\{x,y\}]).                         \tag{20}
\]

If \(\lambda_c=\xi_c\eta_c\ne0\), the pure-\(c\) coefficient is

\[
 \lambda_c=\sum_{x<y}R_{xy}(c,c)H_c(x,y).                \tag{21}
\]

Some pair in (21) therefore has

\[
 R_{xy}(c,c)\ne0,\qquad H_c(x,y)\ne0,
 \qquad H_\delta(x,y)=0.                                  \tag{22}
\]

Thus every retained target colour selects an active pair which is a
literal pure-\(\delta\) cofactor hole.  This is sharp.  The unary guard in
Section 7 of
[the pure binary common-power audit](curved-pure-binary-three-channel-common-power-independent-audit.md)
has \(\delta=1\) and

\[
 p_1t_1=x_{1,0}x_{3,0}+x_{0,2}x_{2,2},\qquad
 p_1t_1q^{[2]}=X_0+X_2.                                  \tag{23}
\]

The pair \(13\) is active in colour zero but a colour-one cofactor hole;
the pair \(02\) is active in colour two but the same kind of hole.
That guard lacks a direct block and the other eight full-nine rows.  It
therefore guards cap-only and contracted-\(\Gamma\) inferences, not the
present full-nine packet.

## 5. The exact three-site overlap coefficient

Now use two charts \(pq,pr\).  Put

\[
 D=\mathcal V\setminus\{p,q,r\},\qquad |D|=2h-1,
\]

and on \(D\) write \(z,x_i,y_j,t_k\) for the internal quadratic and
the stars from \(p,q,r\).  Let

\[
 P=A_{pq},\qquad R=A_{pr},\qquad T=A_{qr}.
\]

The literal 27-row identity is

\[
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[h-1]}
 +x_iy_jt_kz^{[h-2]}
 =\mathbf1_{i=j=k}X_i^D.                                  \tag{24}
\]

For the \(pq\)-compression functional \(\ell(C)=0\), put

\[
 U=\sum_{i\in A,j\in B}\ell_{ij}x_iy_j,qquad
 L_k=\sum_{i,j}\ell_{ij}(R_{ik}y_j+T_{jk}x_i).          \tag{25}
\]

Applying \(\ell\) to (24) gives, for every physical label \(k\),

\[
 \boxed{L_kz^{[h-1]}+Ut_kz^{[h-2]}
      =\ell(E_{kk})X_k^D.}                               \tag{26}
\]

The double-zero visibility conditions give

\[
 R_{A,\delta}=0,qquad T_{B,\delta}=0,                  \tag{27}
\]

so \(L_\delta=0\) and (26) becomes

\[
                         Ut_\delta z^{[h-2]}=0.          \tag{28}
\]

If \(\ell(E_{ee})=1\), its first target-bearing row is

\[
                         L_ez^{[h-1]}+Ut_ez^{[h-2]}=X_e^D.
                                                                  \tag{29}
\]

For the \(pr\)-chart, take \(\ell'\) on its compression and define

\[
 U'=\sum_{i,k}\ell'_{ik}x_it_k,qquad
 L'_j=\sum_{i,k}\ell'_{ik}(P_{ij}t_k+T_{jk}x_i).        \tag{30}
\]

If this chart detects the same normalized anchor \(e\), it gives

\[
 L'_ez^{[h-1]}+U'y_ez^{[h-2]}=X_e^D.                   \tag{31}
\]

Subtract (31) from (29) and use

\[
                       zz^{[h-2]}=(h-1)z^{[h-1]}.
\]

This proves (2), including its factor \((h-1)^{-1}\).  Equation (2) is a
literal cubic before the common power, but only its product with
\(z^{[h-2]}\) is known to vanish.

There is also a cancellation-safe pure-\(\delta\) consequence.  Define

\[
 \tau_k=[t_kz^{[h-1]}]_{\delta^D},\quad
 \upsilon_j=[y_jz^{[h-1]}]_{\delta^D},\quad
 \chi_i=[x_iz^{[h-1]}]_{\delta^D}.                       \tag{32}
\]

The zero cohafnian covectors on the two charts give
\(\tau=\upsilon=0\).  Cross-site synchronization gives

\[
 [x_iy_jt_kz^{[h-2]}]_{\delta^D}
       =\delta_{i\delta}\delta_{j\delta}\delta_{k\delta}. \tag{33}
\]

Taking the pure coefficient in (24), (33) cancels its target and leaves
(3).  Since this is an outer product of the scalar array \(T\) and the
vector \(\chi\), either \(T=0\) or \(\chi=0\).

## 6. The odd residue is flat

This section is the present double-zero specialization of the
[common-coloop odd-residue transport](common-coloop-odd-residue-and-flat-overlap.md),
not a new overlap invariant.  The missing diagonal rows define its natural
odd residue, but the two charts carry the same class for a formal reason.
Put

\[
 \mathcal C_z=
 {({\cal R}_D)_{2h-1}\over({\cal R}_D)_1z^{[h-1]}},
 \qquad
 \operatorname {res}_z(Z;T)=[TZz^{[h-2]}]\in\mathcal C_z. \tag{34}
\]

Use the unnormalized pair cap

\[
 \mathcal P_{pq}^{ij}=hp_is_j+P_{ij}q_{pq},qquad
 \mathcal P_{pq}^{ij}q_{pq}^{[h-1]}=h\delta_{ij}X_i.    \tag{35}
\]

After exposing \(r\), its base quadratic and normal row are

\[
 \Pi_{pq}^{ij}=hx_iy_j+P_{ij}z,qquad
 \Lambda_k=h(R_{ik}y_j+T_{jk}x_i)+P_{ij}t_k.           \tag{36}
\]

The \(r,k\) coefficient of (35) is

\[
 \Lambda_kz^{[h-1]}+\Pi_{pq}^{ij}t_kz^{[h-2]}
    =h\delta_{ij}\delta_{ik}X_i^D.                     \tag{37}
\]

Modulo the denominator in (34),

\[
 \operatorname {res}_z(\Pi_{pq}^{ij};t_k)
   =h\delta_{ij}\delta_{ik}[X_i^D].                    \tag{38}
\]

The \(pr\)-chart gives the same class.  This is also immediate from the
power-free connection

\[
 \Pi_{pq}^{ij}t_k-\Pi_{pr}^{ik}y_j
       =(P_{ij}t_k-R_{ik}y_j)z                          \tag{39}
\]

and \(zz^{[h-2]}=(h-1)z^{[h-1]}\).  Hence equality of the two residues is
flat pair-chart transport, not a second constraint.  Moreover
\([X_e^D]\) can vanish in \(\mathcal C_z\), as the next guard shows.

### 6.1 Literal pure anchors remain nonzero

Vanishing of the odd residue does not mean that the diagonal row has no
source-supported anchor.  Let \(A^{(e)}_{uv}=A_{uv}(e,e)\) be the pure
\(e\) scalar block of the original source.  Its normalized all-\(e\)
coefficient is one, and Laplace expansion at the shared endpoint \(p\)
gives

\[
 1=\sum_{v\ne p}A_{pv}(e,e)\,
       \operatorname {haf}
       A^{(e)}[\mathcal V\setminus\{p,v\}].             \tag{39a}
\]

For each \(e\ne\delta\), some summand in (39a) therefore has both factors
nonzero.  The two missing diagonal rows supply two differently labelled
literal pure edges incident with \(p\), each with a nonzero complementary
cofactor.  At eight sites these are edge coordinates with nonzero six-site
complementary hafnians.

This is not yet the fixed-source probe-Jacobian own-edge lift required by
the K6 curvature argument.  Varying an aggregate edge weight is different
from varying the endpoint probes, and (39a) does not put the anchor in the
required direct/star/internal grade.  The guard below realizes both literal
anchors while both odd residue classes vanish.

## 7. A complementary diagonal-only guard

Take eight sites

\[
                         p,q,r,a,b,c,d,e
\]

and the following unit endpoint-ordered cells, with every unlisted cell
zero:

\[
\begin{array}{c|l}
0&(pa;00),(qb;00),(rc;00),(de;00),\\
1,2\text{ cross}&(pq;12),(pq;21),(pr;12),(pr;21),\\
qr&(qr;11),(qr;22),\\
1&(pe;11),(ab;11),(cd;11),\\
2&(pd;22),(ac;22),(be;22).
\end{array}                                                \tag{40}
\]

Its complete matching tensor has exactly eleven nonzero words, all with
coefficient one.  In site order \((p,q,r,a,b,c,d,e)\), they are

\[
\begin{gathered}
00000000,\quad11111111,\quad22222222,\\
01102112,\ 02202112,\ 10220200,\ 12011000,\\
12211111,\ 20120200,\ 21011000,\ 21122222.              \tag{41}
\end{gathered}
\]

The first three are the desired pure words.  Every other word is
off-diagonal on both \(pq\) and \(pr\).  Thus all three complete diagonal
rows hold in both charts, while every one of the six off-diagonal rows
fails.

For \(\delta=0\), all four channel sets are \(\{0\}\), and

\[
 P_{\{1,2\},\{1,2\}}
 =R_{\{1,2\},\{1,2\}}
 =\begin{pmatrix}0&1\\1&0\end{pmatrix}.                 \tag{42}
\]

Both pure internal hafnians and every Hamming-one internal coefficient
vanish.  The two pure response matrices are \(E_{00}\).  On
\(D=\{a,b,c,d,e\}\),

\[
 x_0=e_0^{(a)},\quad y_0=e_0^{(b)},\quad
 t_0=e_0^{(c)},\quad z_0=(de)_0,                         \tag{43}
\]

so the cross tensor is exactly \(E_{000}\).  All four endpoint-star maps
have rank three.  Choosing the fourth site \(c\) and selected labels
\((a,b,c,d)=(1,2,0,0)\) gives

\[
                         AU-BF=1.                       \tag{44}
\]

The cross block \(T=A_{qr}\) has nonzero lower diagonal, whereas
\(\tau=\upsilon=\chi=0\), so the guard realizes the \(\chi=0\) branch of
(3).  Finally

\[
 z=(de)_0+(ab)_1+(cd)_1+(ac)_2+(be)_2.                 \tag{45}
\]

The four off-exposed diagonal cap bases
\(\Pi_{pq}^{11},\Pi_{pq}^{22},\Pi_{pr}^{11},\Pi_{pr}^{22}\) vanish,
while their normal rows supply the targets.  In particular

\[
 e_1^{(e)}z^{[2]}=X_1^D,qquad
 e_2^{(d)}z^{[2]}=X_2^D,                               \tag{46}
\]

so \([X_1^D]=[X_2^D]=0\) in (34).  Both missing odd-residue anchors
therefore vanish despite (42)--(44).  The literal anchors from (39a) are
the edges \(pe\) in colour one and \(pd\) in colour two.

The dependency-free checker
[`verify_double_zero_diagonal_anchor_guard.py`](../computations/verify_double_zero_diagonal_anchor_guard.py)
enumerates (41), verifies both chart fibres, all double-zero data, the
four star ranks, curvature, (3), and (46).  The guard has bare
\(\Gamma\)-identities, not routed ones: its six failed rows are precisely
the full-nine antecedent missing from the routing theorem.

## 8. Exact remaining gate

The positive output is now source-relative and narrow.

* Off the coordinate-cell boundary, the completed full-nine system,
  contracted against a diagonal-detecting functional, exports a literal
  unary or binary cap and an active pure-\(\delta\) cofactor hole.
* On two charts, a common detected anchor exports the cubic (2).
* On the coordinate-cell boundary, the unreduced diagonal normal row in
  (24) remains available.
* The pure \(\delta\) overlap additionally gives the zero-block/cohafnian
  split (3).

The cap alone cannot supply the alternating K6 curvature class: two
scalar-zero caps sharing the common \(p\)-factor have flat power-free
overlap and zero four-cut curvature.  The exact missing theorem must mix
one of these diagonal anchors with a nonisotropic off-diagonal curvature
row before quotienting by \(z^{[h-2]}\), or construct the same
grade-preserving transverse correction by another source-faithful route.
The conjecture remains open at that step.
