# The P-containing double-live residue has rank at most \(49\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Continue in the double-live one-column branch

\[
 P_t=0,\qquad Q_t\ne0,\qquad
 B_4=M_{t4}\ne0,\qquad B_5=M_{t5}\ne0,                         \tag{1}
\]

after the
[factor-complete reduction](level-two-three-invertible-one-column-double-live-factor-complete-closure.md)
and the
[mixed-residue reduction](level-two-three-invertible-one-column-double-live-mixed-residue-reduction.md).
Each zero is inactive (I) or active P/V (P), every active live block is
misaligned with its P/V zero factor, and mixed L0 leaves one pure correction
colour. The remaining type charts are

\[
                         (\mathrm I,\mathrm P),\quad
                         (\mathrm P,\mathrm I),\quad
                         (\mathrm P,\mathrm P).                  \tag{2}
\]

> **P-residue closure.** Every packet in (2) satisfies
> \[
>                         \operatorname{rank}d\Psi_M\le49.       \tag{3}
> \]

Together with the prior closure of the inactive-inactive chart, this closes
the full double-live one-column residue. The selected-family symmetric case
\(Q_t=0,\ P_t\ne0\) follows by interchanging
\((P,U,v)\leftrightarrow(Q,V,u)\).

## The double-P chart is already a coordinate-shore path

At an active P/V zero \(z\), L1 gives

\[
                         M_{iz}=m_iP_iv_z^{\mathsf T}
                         \qquad(i\in I),                         \tag{4}
\]

so all three \(I\)-spokes have the fixed physical factor \(v_z\) at \(z\).
The one-column blocks \(M_{it}\) have fixed factor \(Q_t\) at \(t\), and the
selected zero-zero equation gives \(M_{45}=0\). Therefore in the
\((\mathrm P,\mathrm P)\) chart the three-site shore

\[
                              T=\{t,4,5\}                        \tag{5}
\]

has fixed factors \(Q_t,v_4,v_5\) on every cross block from \(I\). Its only
arbitrary internal blocks are \(B_4\) and \(B_5\), the exceptional path

\[
                              4-t-5.                             \tag{6}
\]

The exact coordinate-shore path theorem immediately gives

\[
                         \operatorname{rank}d\Psi_M\le49.       \tag{7}
\]

No mixed-L0 tensor separation or alignment of either \(B_z\) is needed for
this chart. In particular, the arbitrary exceptional path blocks may be
rank two and physically misaligned.

## The exact one-P matching split

Now let \(z\) be the unique active P/V zero and \(w\) the inactive zero.
Place the \(z\)-factor first and regard \(B_z\) as a tensor in
\(V_z\otimes V_t\). Of the fifteen perfect matchings:

- three use \(t z\), giving \(B_z\otimes C\), where \(C\) is the four-site
  matching tensor on \(I\sqcup\{w\}\);
- nine use an \(I z\) spoke and hence have factor \(v_z\); and
- three use the dead block \(M_{zw}=0\).

Thus, for a five-site tensor \(L\),

\[
                         H=\Psi(M)=B_z\otimes C+v_z\otimes L.   \tag{8}
\]

Let \(T_z,T_w\) denote the radial tangents carrying the physical live
blocks \(B_z,B_w\), and let \(S_z\) be the P/V endpoint star. The derivative
of \(T_z\) is the same \(B_z\otimes C\). Every term from \(S_z\) has factor
\(v_z\) at its tangent endpoint, while every cofactor term from \(T_w\)
uses an \(I z\) spoke and has that factor as well. Consequently the sole
pure correction isolated by mixed L0 has the exact form

\[
 e_k^{\otimes6}-\kappa H
       =-c B_z\otimes C+v_z\otimes D,
 \qquad k=1-s,\qquad H=h e_s^{\otimes6},\quad h\ne0.             \tag{9}
\]

Here \(c\) absorbs the surviving endpoint coefficient \(a_k\), and \(D\)
absorbs the correspondingly scaled \(S_z\)- and \(T_w\)-source terms. This
is only scalar bookkeeping; the \(T_z\) component retains the same
\(B_z\otimes C\) factor that occurs in (8).

This is a matching-support identity, not a claimed independence of the
three physical shores in the double-P decomposition.

## The active factor is the complementary physical colour

Substitute (8) into (9). With \(F=D+cL\),

\[
 e_k^{\otimes6}+(c-\kappa)h e_s^{\otimes6}
                              =v_z\otimes F.                    \tag{10}
\]

Flatten at the physical site \(z\). The two terms on the left occupy the
independent row/column corners

\[
 e_k\otimes e_k^{\otimes5},\qquad
 e_s\otimes e_s^{\otimes5}.                                    \tag{11}
\]

Their \(2\times2\) minor is, up to sign, \((c-\kappa)h\). The right side
has flattening rank at most one, so

\[
                         \kappa=c,\qquad v_z\parallel e_k.       \tag{12}
\]

The second conclusion follows because (10) then becomes the nonzero
rank-one tensor \(e_k^{\otimes6}=v_z\otimes F\). This use of \(e_s,e_k\)
is in the original physical target coordinates; no selected-basis vector
is identified with a pure target axis.

Choose the harmless nonzero representative \(v_z=e_k\), inversely
rescaling the active P/V coefficients and renaming \(L,D\) so that
(8)--(10) are unchanged. Write the two \(z\)-rows of \(B_z\) as
\(b_s,b_k\in V_t\). The \(s\)-row of (8) is

\[
                         b_s\otimes C=h e_s^{\otimes5}.          \tag{13}
\]

Both factors are nonzero, and the tensor on the right has singleton
support. Hence for a nonzero scalar \(\gamma\),

\[
                         C=\gamma e_s^{\otimes4},\qquad
                         b_s=(h/\gamma)e_s.                      \tag{14}
\]

Equivalently, rescale only the displayed factor pair
\(B_z\otimes C=(\gamma B_z)\otimes e_s^{\otimes4}\). There is a vector
\(\ell_t\in V_t\) for which the normalized decomposition is

\[
 \widehat B_z=\gamma B_z
        =h e_se_s^{\mathsf T}-e_k\ell_t^{\mathsf T},\qquad
 L=\ell_t\otimes e_s^{\otimes4}.                                \tag{15}
\]

Here the first factor of each rank-one matrix term is at \(z\), and the
second is at \(t\). Equation (15) is an algebraic representative of (8),
not a change to the physical packet. It records in particular that the
non-\(t z\) component is \(\ell_t\otimes e_s^{\otimes4}\). Equation (9)
then has

\[
                         D=e_k^{\otimes5}-cL.                    \tag{16}
\]

The proof of (3) needs only the first conclusion in (14).

## Purity supplies the inactive fixed shore

The tensor \(C\) is the four-site hafnian on \(I\sqcup\{w\}\). For a
physical colour \(a\) at \(w\), its slice is

\[
 C^a(x_I)=\sum_{i\in I}M_{iw}(x_i,a)M_{jk}(x_j,x_k)
                         =\Phi(U_w^a),\qquad\{i,j,k\}=I,         \tag{17}
\]

where \(U_w^a\) is the triple of \(a\)-columns of the \(I\)-to-\(w\)
blocks. The triangle cofactor map \(\Phi\) is injective. This is a covariant
fact: local bases on the three invertible sites may normalize the triangle
to audit injectivity, but they are not used to identify any selected line
with the physical vectors \(e_s,e_k\).

By (14), \(C^k=0\). Injectivity in (17) gives \(U_w^k=0\), so every inactive
spoke has the physical fixed shore

\[
                              M_{iw}=u_i e_s^{\mathsf T}.         \tag{18}
\]

The shore \(\{t,z,w\}\) now has fixed cross factors

\[
                              Q_t,\qquad e_k,\qquad e_s,         \tag{19}
\]

respectively. Its internal blocks \(B_z,B_w\) are the two arbitrary path
edges and \(M_{zw}=0\). The coordinate-shore path theorem gives (7) again,
closing both one-P charts.

The local shore bases used inside that rank theorem preserve differential
rank only. No R2 witness or physical pure-column statement is transported
through them.

## Exact audit

The standard-library checker
[verify_level_two_three_invertible_one_column_double_live_p_residue_closure.py](../computations/verify_level_two_three_invertible_one_column_double_live_p_residue_closure.py)

- audits the \(3+9+3\) one-P matching split and the exact
  \(T_z/S_z/T_w=3/9/3\) derivative split;
- verifies the flattening minor forcing (12), all 256 coordinates of the
  normalized identities (15)--(16), and the unique singleton support in
  (14);
- imports the exact rank-six triangle-cofactor map and the 64 formal
  coordinate-shore path identities giving \(28+21=49\); and
- checks all three P-containing chart labels and the selected-family
  symmetric dictionary.

It passes normal, optimized, and isolated Python.
