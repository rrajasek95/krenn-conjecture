# The common-factor singular-cross L1 types do not survive pure L0

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Continue from [the singular-cross L1 classification](level-two-three-invertible-singular-cross-l1-boundary.md),
under the same rank-\(55\), two-column rank-one-site, and
kernel-equals-gauges hypotheses. The remaining active zero sites have one
of the two forms

\[
\begin{array}{ll}
\text{P/V:}&M_{rz}=m_{rz}P_rv_z^{\mathsf T},\quad
 U_z^s=0,\quad V_z^s=d_{zs}v_z,\\[2mm]
\text{Q/U:}&M_{rz}=m_{rz}Q_ru_z^{\mathsf T},\quad
 V_z^s=0,\quad U_z^s=d_{zs}u_z,
\end{array}                                           \tag{1}
\]

for \(r\in C=I\sqcup\{t\}\). This note closes all such
common-factor types, including:

* uniform and nonuniform spoke multiples;
* the scalar-degenerate R2 alternatives;
* one or two active zero sites; and
* same-type and opposite-type interactions between the two zero sites.

Together with the earlier non-common-factor closure, no boundary remains
from a zero site lacking an invertible \(I\)-spoke. The one-column
rank-one-site charts are separate and retain the scope stated in
[their reduction](level-two-three-invertible-one-column-t-boundary.md).

## Uniform multiples are radial gauges

Treat a P/V site; Q/U is symmetric. Define the \(z\)-star

\[
 (S_z)_{rz}=P_rv_z^{\mathsf T}\quad(r\in C),
 \qquad (S_z)_{uv}=0\quad\text{otherwise}.            \tag{2}
\]

The endpoint slice has the exact decomposition

\[
 N^{su}=a_sb_uG(\nu)+a_sd_{zu}S_z                 \tag{3}
\]

when \(z\) is the only active zero site. Contributions from a second
same-type site simply add a second star. Opposite types also have the
zero-zero interaction described below.

If all four spoke multiples at \(z\) have one value \(m_z\ne0\), then

\[
                         m_zS_z=G(e_z).               \tag{4}
\]

Indeed, both sides have the block \(M_{rz}\) on every core-to-\(z\)
edge and vanish elsewhere because \(M_{45}=0\). Thus a uniform star is a
generalized radial gauge. If all active sites have uniform multiples and
the two sites have the same type, every endpoint slice is a generalized
gauge. The two pure targets would both be collinear with
\(H=\Psi(M)\), which is impossible.

## Opposite active types close through their zero-zero interaction

Suppose one zero site has P/V type and the other Q/U type. On their mutual
edge, \(M_{45}=0\), while the endpoint packet has the rank-one block

\[
 N^{su}_{45}=d_{P,u}d_{Q,s}\,v_Pu_Q^{\mathsf T}.      \tag{5}
\]

Both target-zero mixed L0 equations require this block to vanish:

\[
 d_{P,1}d_{Q,0}=0,\qquad d_{P,0}d_{Q,1}=0.           \tag{6}
\]

Both endpoint families are active, so their supports are nonempty. The
only solutions of (6) are the two same-singleton charts

\[
 \operatorname{supp}d_P=\operatorname{supp}d_Q=\{k\},
 \qquad k=0\ \text{or}\ 1.                           \tag{7}
\]

R2 then forces the common selected line at the rank-one site to be the
complement:

\[
                             h\parallel e_{1-k}.       \tag{8}
\]

The pure slice \(1-k\) has no star or zero-zero correction. Its L0 equation
therefore forces \(H\) to be a nonzero multiple of
\(e_{1-k}^{\otimes6}\). But that coordinate of \(H\) vanishes term by
term. For \(k=0\), the P-type zero can meet only \(t\) at the all-one
word; the Q-type zero then meets an \(I\)-vertex, leaving two
\(I\)-vertices paired through the zero diagonal entry \(J_{11}\). For
\(k=1\), interchange P and Q and use \(J_{00}=0\). The same argument
works with the two active types interchanged. Hence no opposite-type
configuration survives, regardless of whether either spoke family is
uniform.

## Nonuniform same-type sites have one pure correction

It remains to treat one or two active sites of the same type, with at least
one nonuniform spoke family. For each nonuniform P/V site, the two mixed
L0 products from the previous classification vanish:

\[
                         a_0d_{z1}=a_1d_{z0}=0.       \tag{9}
\]

Thus all nongauge stars occur in at most one pure colour \(k\). If
different nonuniform sites tried to use different colours, (9) would force
\(a_0=a_1=0\), leaving both pure slices generalized gauges and giving the
immediate collinearity contradiction. The Q/U equations are the same with

\[
                         b_1d_{z0}=b_0d_{z1}=0.       \tag{10}
\]

After removing every uniform radial star, the other pure slice
\(r=1-k\) has no nongauge term and forces

\[
                              H=h_r e_r^{\otimes6},
 \qquad h_r\ne0.                                     \tag{11}
\]

The remaining pure-\(k\) correction has rank one across the active-zero
versus core cut. With one active zero this is the standard factorization

\[
                         d\Psi_M(S_z)=v_z\otimes C_z.
 \tag{12}
\]

With two same-type active zeros, every derivative term from either star
contains both common zero-site factors. The tangent star supplies one
factor; since \(M_{45}=0\), the other zero must meet the core in the
complementary matching and supplies the other. Therefore

\[
 d\Psi_M\!\left(q_4S_4+q_5S_5\right)
                       =v_4\otimes v_5\otimes C       \tag{13}
\]

in P/V type, with \(u_4\otimes u_5\) in Q/U type. Formula (13) also
applies when only one star is nonuniform and the other is uniform; its
radial contribution is removed, but its packet still supplies the second
factor in the cofactor matching.

Move the \(H\)-term in the pure-\(k\) equation to the target side. Across
the same cut, the two pure coordinates \(e_k^{\otimes6}\) and
\(e_r^{\otimes6}\) have a \(2\times2\) minor equal, up to sign, to the
nonzero coefficient of \(H\). The correction (12) or (13) has rank one,
so that coefficient must vanish. Singleton outer-product support then
forces every active common zero-site factor in the correction to be
\(e_k\), and forces the complementary cofactor to be pure \(k\).

Now evaluate (11). At any nonuniform active zero site, every incident
core block contains its factor \(e_k\), while \(M_{45}=0\). Every perfect
matching at the all-\(r\) word therefore has a zero edge at that site.
Thus the allegedly nonzero coordinate in (11) is actually zero, a final
contradiction.

The standard-library checker
[verify_level_two_three_invertible_common_factor_l1_closure.py](../computations/verify_level_two_three_invertible_common_factor_l1_closure.py)
audits the 15 uniform radial-gauge blocks, the exact opposite-type support
census and 60 termwise complementary-coordinate zeros, all one- and
two-site scalar-degenerate patterns, the common zero-factor in every
same-type star derivative term, the pure flattening minors, and the final
matching-coordinate vanishing. It passes normal, optimized, and isolated
Python.
