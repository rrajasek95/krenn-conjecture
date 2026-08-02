# The terminal one-column charts do not acquire a singular-spoke escape

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Consider the terminal conditions isolated on the one-column rank-one-site
boundary:

\[
 Q_t=q e_r,\qquad H=\Psi(M)=h e_s^{\otimes6},\qquad
 C_t=c e_r^{\otimes5},\qquad r=1-s,\quad qhc\ne0.       \tag{1}
\]

Drop the earlier assumption that each zero site has an invertible spoke to
the invertible triangle. There is still no differential-rank-55 packet:

* if either zero shore has two independent triangle-cofactor slices, the
  pure-shore argument gives a direct contradiction; and
* if both shores have dependent slices, the packet lies in the two-edge
  coordinate-shore path class and has
  \(\operatorname{rank}d\Psi_M\le49\).

This is a covariant terminal-chart closure. The normalization
\(X_i=I_2\) below is used only to prove injectivity of a cofactor map. It
does not identify \(P_i=e_0\) or \(Q_i=e_1\) with physical pure target
coordinates. Thus none of the non-covariant R2 complement shortcuts is used.

The statement closes the intersection of the complementary-purity terminal
charts with the singular-spoke boundary. It does not assert that every
active singular-cross L1 configuration reaches the terminal conditions (1);
such configurations must first pass the separate L1/L0 reductions.

## A covariant cofactor map

For a zero site \(z\in\{4,5\}\) and physical zero-site colour \(a\), put

\[
 U_z^a=\bigl(M_{0z}(-,a),M_{1z}(-,a),M_{2z}(-,a)\bigr)
 \in W:=V_0^*\oplus V_1^*\oplus V_2^*.                 \tag{2}
\]

Pairing one of these spoke columns with the opposite triangle edge defines

\[
 L_z^a(x_I)=\sum_{i\in I}M_{iz}(x_i,a)M_{jk}(x_j,x_k)
             =\Phi(U_z^a),\qquad \{i,j,k\}=I.          \tag{3}
\]

The map \(\Phi:W\to V_0^*\otimes V_1^*\otimes V_2^*\) is injective. This
was proved in the
[pure-tensor shore obstruction](level-two-three-invertible-one-column-pure-tensor-obstruction.md)
by normalizing the invertible triangle and explicitly recovering all six
input coordinates. Because normalization is an invertible change of basis
on the source and target of \(\Phi\), injectivity is covariant.

The coefficient of \(C_t\) at zero-shore word \((r,r)\) is

\[
 C_t^{rr}(x_I)=\sum_{i\in I}P_i(x_i)
 \left(
 M_{j4}(x_j,r)M_{k5}(x_k,r)
 +M_{j5}(x_j,r)M_{k4}(x_k,r)
 \right).                                               \tag{4}
\]

Every summand contains one \(r\)-column from each zero shore. Since (1)
makes (4) a nonzero tensor, neither \(U_4^r\) nor \(U_5^r\) is zero.
Injectivity gives

\[
                         L_4^r\ne0,\qquad L_5^r\ne0.    \tag{5}
\]

## Independent slices give the shore contradiction

At colour \(s\) on site \(t\), the one-column generic-kernel blocks
\(M_{it}\) vanish because they contain \(Q_t(s)=0\). Also \(M_{45}=0\).
Writing

\[
 x_a=M_{t4}(s,a),\qquad y_b=M_{t5}(s,b),
\]

the four physical zero-shore slices are

\[
                         T_{ab}=x_aL_5^b+y_bL_4^a.     \tag{6}
\]

Suppose first that \(L_4^s,L_4^r\) are independent. Together with
\(L_5^r\ne0\), the three equations

\[
                         T_{sr}=T_{rs}=T_{rr}=0        \tag{7}
\]

force \(x_s=x_r=y_s=y_r=0\), as in the earlier forbidden-corner lemma.
This contradicts the required nonzero corner \(T_{ss}\). If the independent
pair occurs at site 5 instead, interchange the two zero shores and use
\(L_4^r\ne0\). Therefore a terminal survivor would require

\[
 \dim\langle L_z^s,L_z^r\rangle=1
                         \quad(z=4,5).                 \tag{8}
\]

## Two dependent shores have rank at most 49

By injectivity of \(\Phi\), condition (8) is equivalent to dependence of
\(U_z^s,U_z^r\). The second vector is nonzero by (5), so for some scalar
\(\alpha_z\),

\[
                         U_z^s=\alpha_zU_z^r.          \tag{9}
\]

Componentwise, (9) says that every block on the \(I\)-to-\(z\) shore has
one fixed right factor at \(z\):

\[
                         M_{iz}=u_{iz}v_z^{\mathsf T}
                         \quad(i\in I).                \tag{10}
\]

This is a basis-free fixed-shore-factor conclusion. It uses neither a P/V
or Q/U orientation nor an R2 complement claim, and it does not choose a
selected line at the \(I\) sites.

Now take the three-site shore \(T=\{t,4,5\}\). The \(I\)-to-\(t\) blocks
already have the fixed right factor \(Q_t\), equations (10) give fixed
right factors at 4 and 5, and \(M_{45}=0\) has the required coordinate
support. Only \(M_{t4}\) and \(M_{t5}\) remain arbitrary. They form the
two-edge exceptional path

\[
                              4-t-5.
\]

The exact
[coordinate-shore path theorem](level-two-three-invertible-coordinate-shore-rank-drop.md)
therefore applies. Its support-preserving image has dimension at most 28
and there are 21 transverse cell directions, giving

\[
                         \operatorname{rank}d\Psi_M\le28+21=49.  \tag{11}
\]

This contradicts rank 55 and closes the dependent-dependent alternative.

## Exact audit

The standard-library checker
[verify_level_two_three_invertible_one_column_singular_overlap.py](../computations/verify_level_two_three_invertible_one_column_singular_overlap.py)
audits every formal monomial of (4), the dependent-column factorization,
all four independence patterns, the 64 exact pure-shore identities and
rank-six cofactor map, and the 64 formal path-factorization identities
behind (11). It passes normal, optimized, and isolated Python.
