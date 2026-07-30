# Rank-two alignment kernels produce a mixed full-nine cap

## 1. Outcome

Work at the first \(8\to6\) boundary, on one of the two literal pair
charts supplied by the
[joint-extraction theorem](two-chart-joint-hypothesis-extraction.md).  Write

\[
 d_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2,                                  \tag{1}
\]

and at a residual site \(x\) put

\[
 P=P_x,\qquad S=S_x,\qquad
 N_{x,e}=P^{\mathsf T}J_eS .                              \tag{2}
\]

Suppose \(d\) has rank two and a target \(e\) is aligned with nonzero
proportionality,

\[
                         N_{x,e}=\lambda_xd,
                         \qquad\lambda_x\ne0.             \tag{3}
\]

Let \(\xi\) and \(\eta\) span the literal left and right kernel lines

\[
                 \ker d^{\mathsf T}=\mathbb C\xi,
                 \qquad \ker d=\mathbb C\eta.             \tag{4}
\]

Then the complete nine rows have a canonical rank-one contraction

\[
 \boxed{
 p(\xi)s(\eta)q^{[2]}
       =\sum_{c=0}^2\xi_c\eta_cX_c .}                     \tag{5}
\]

This is the missing diagonal--off-diagonal coupling in the alignment
ledger.  For every \(c\) with \(\xi_c\eta_c\ne0\), the contraction contains
the \((c,c)\) diagonal anchor.  Unless
\(\xi=\eta\in\mathbb C^*e_c\), it also contains at least one literal
off-diagonal row with nonzero coefficient.  The exceptional coincident
coordinate-kernel case already gives (5) from the direct-zero \((c,c)\)
row alone.

The local effect of (3) is equally rigid:

\[
                         P\xi\in\mathbb Ce_e,
                         \qquad S\eta\in\mathbb Ce_e.       \tag{6}
\]

Consequently a nonzero alignment at target \(e\ne c\) is a genuinely
\(c\)-dark site for the cap in (5).  Three such sites force a physical
dark cut, without cancelling \(q^{[2]}\): a nonzero coefficient of
\(X_c\) contains a cap edge avoiding all three sites and a complementary
two-edge physical \(q\)-matching; one of those two edges joins two dark
sites.

This closes a substantial part of the rank-two alignment survivor.
Precisely, define

\[
 T_e^\times=\{x:N_{x,e}\in\mathbb C^*d\}.                 \tag{7}
\]

If all physical dark cuts fail, then for every
\(c\in\operatorname {supp}\xi\cap\operatorname {supp}\eta\),

\[
 \boxed{
 \left|\bigcup_{e\ne c}T_e^\times\right|\leq2.}           \tag{8}
\]

Here all sets refer to the same chart and the same fixed rank-two direct
block \(d\).  If total selector-dark-cut failure also supplies the
full-nine selector bounds \(|T_e|\geq3\), where
\(T_e=\{x:N_{x,e}\in\mathbb Cd\}\), then for this fixed
\(c\in\operatorname {supp}\xi\cap\operatorname {supp}\eta\) and for
each of the two labels \(e\ne c\), some aligned site must lie in the
literal zero branch:

\[
 \boxed{\text{for every }e\ne c\text{ there is }x_e\in T_e
                  \text{ with }N_{x_e,e}=0.}             \tag{8a}
\]

Thus a targetful rank-two kernel does not leave a purely proportional
residue.  It either produces the dark cut or descends to zero endpoint
wedges for both other target labels.  If the same site realizes both
zeros, the coordinate-plane/low-rank classification of the alignment note
applies there immediately.

If, moreover, \(P_x\) and \(S_x\) have rank two at a nonzero aligned
site, that site is dark also when its alignment label equals \(c\).  Thus
three such sites for the same fixed \(d\) close (5) for every colour in
the kernel-support intersection.  Their alignment labels may differ; what
is shared is the direct block and hence the kernel cap.  In particular, on
the two-target nonzero branch of the
[alignment normal form](two-chart-alignment-curvature-normal-form.md),
three such sites and failure of every physical dark cut force

\[
             \operatorname {supp}\xi\cap
             \operatorname {supp}\eta=\varnothing.         \tag{9}
\]

For nonzero vectors in three coordinates, (9) has the case-free
consequence

\[
 \boxed{\text{the direct block has a literal zero row or a literal zero
 column.}}                                                  \tag{10}
\]

There is a sharper two-chart conclusion for the targetless-kernel-cap
branch.  If the \(pq\)- and \(pr\)-charts are nonzero-aligned at the same
target and common site, their shared physical \(p\)-star gives one common
left kernel \(\mathbb C\xi\).  If both kernel contractions in (5) have
zero target, then either

\[
 \begin{array}{ll}
 \xi\text{ is coordinate},
   &d,d'\text{ have the same literal zero row};\\
 \xi\text{ is noncoordinate},
   &d,d'\text{ have the same literal zero column}.
 \end{array}                                                \tag{11}
\]

Thus the targetless part of the low-rank shared-kernel survivor descends to
a fixed-label row/column hook; it is not a free rank-two matrix pair.  A
targetful kernel contraction is instead routed by (8), and closes as soon
as three kernel-dark sites occur.  If the remaining support has no
off-target kernel colour, the only additional support form is the
target-centred cross

\[
 \operatorname {supp}\xi=\{e,a\},\qquad
 \operatorname {supp}\eta,
 \operatorname {supp}\eta'\subseteq\{e,b\},
 \qquad\{e,a,b\}=\{0,1,2\}.                               \tag{12}
\]

When both right kernels in (12) specialize to the same complementary
coordinate, that specialization is already the common-zero-column
alternative.

The selected curvature is retained throughout.  If
\(A=d_{ij}\ne0\), the common zero row in (11) is not row \(i\), and the
common zero column is not column \(j\).  If also
\(B=d'_{ik}\ne0\), that column is not \(k\) either.  Nothing here replaces
the physical scalar \(AU-BF\) by a source minor.

## 2. The adjugate identifies the kernel selector

For every \(3\times3\) matrix, the polynomial adjugate identity gives

\[
\begin{aligned}
 \operatorname {adj}(P^{\mathsf T}J_eS)
 &=\operatorname {adj}(S)\operatorname {adj}(J_e)
       \operatorname {adj}(P)^{\mathsf T}\\
 &=(\operatorname {adj}(S)e_e)
       (\operatorname {adj}(P)e_e)^{\mathsf T}.             \tag{13}
\end{aligned}
\]

Since \(\operatorname {rank}d=2\), equation (3) implies

\[
 (\operatorname {adj}(S)e_e)
 (\operatorname {adj}(P)e_e)^{\mathsf T}
       =\lambda_x^2\operatorname {adj}(d)\ne0.              \tag{14}
\]

The column and row lines of \(\operatorname {adj}(d)\) are respectively
\(\ker d\) and \(\ker d^{\mathsf T}\).  After rescaling (4), therefore,

\[
              \eta=\operatorname {adj}(S)e_e,
              \qquad \xi=\operatorname {adj}(P)e_e.         \tag{15}
\]

Multiplying by \(P\) and \(S\), and using
\(M\operatorname {adj}(M)=\det(M)I\), proves (6).  This proof includes
both possible local ranks.  If \(P\) has rank two then \(P\xi=0\); if it
is invertible then \(P\xi\) is a nonzero multiple of \(e_e\).  The same
alternative holds for \(S\eta\).

If two distinct target labels are nonzero-aligned to the same rank-two
direct block at one site, then \(P\) and \(S\) must both have rank two.
Indeed, (15) sends two independent coordinate vectors to the same kernel
line, which an invertible adjugate cannot do.  Hence in that branch

\[
                              P\xi=S\eta=0.              \tag{16}
\]

This recovers the local rank assertion of the earlier alignment theorem
and records the stronger kernel information needed below.

## 3. The full-nine kernel cap

Contract all nine equations (1) against the rank-one matrix
\(\xi\eta^{\mathsf T}\).  Since

\[
                       \xi^{\mathsf T}d=0,
                       \qquad d\eta=0,                    \tag{17}
\]

the direct term vanishes before any common power is touched.  The response
term factors literally, and the diagonal targets retain their fixed
physical labels:

\[
\begin{aligned}
 0\cdot q^{[3]}+p(\xi)s(\eta)q^{[2]}
   &=\sum_{i,j}\xi_i\eta_j\delta_{ij}X_i\\
   &=\sum_c\xi_c\eta_cX_c.
\end{aligned}                                               \tag{18}
\]

This proves (5).  No cancellation of \(q^{[2]}\), row-basis change, or
abstract cap has occurred.  When a retained diagonal coefficient
\(\xi_c\eta_c\) is nonzero and either kernel vector has another supported
coordinate, the Cartesian support of \(\xi\eta^{\mathsf T}\) contains an
off-diagonal cell with nonzero coefficient.  Thus (18) visibly uses the
off-diagonal annihilator row and the \((c,c)\) anchor in one source-valid
identity.

## 4. Three kernel-dark sites give a physical cut

Put

\[
                         L=p(\xi),\qquad S_\eta=s(\eta),
                         \qquad\beta=LS_\eta.              \tag{19}
\]

Fix \(c\) with \(\xi_c\eta_c\ne0\).  At a site satisfying (3) with
\(e\ne c\), equation (6) gives

\[
                         L_{x,c}=(S_\eta)_{x,c}=0.           \tag{20}
\]

The coordinate probe \(e_c^*\) is therefore cap-dark there.  Equation
(20) also says that every pure-\(c\) coefficient of a cap edge incident
with \(x\) is zero.  If both local maps have rank two, (16) gives (20)
even when \(e=c\).

Suppose three distinct sites \(x_1,x_2,x_3\) satisfy (20).  Take the
\(X_c\)-coefficient of (5).  Its value is
\(\xi_c\eta_c\ne0\), so at least one individual matching summand is
nonzero.  Such a summand consists of one cap edge \(rs\) and a perfect
matching \(uv\mid zw\) of the four complementary sites.  The cap edge
avoids all three \(x_i\)'s by (20).  Hence all three lie among
\(\{u,v,z,w\}\).  A matching of four vertices with three marked vertices
has an edge whose two endpoints are marked; rename it \(uv\).  For the
chosen nonzero summand,

\[
                    \beta_{rs}(c,c)\ne0,
                    \qquad q_{uv}(c,c)\ne0.                \tag{21}
\]

At \(u,v\), the probes \(e_c^*\) annihilate both cap factors.  Probe the
cap endpoints \(r,s\) by the same coordinate covectors.  The four sites
\(r,s,u,v\) are distinct, and cap-darkness at \(u,v\) kills
\(\beta_{uv},\beta_{ru},\beta_{sv}\).  Thus (21) is exactly the literal
coefficient cut

\[
                         d\kappa_q(\beta)
                            =q_{uv}(c,c)\beta_{rs}(c,c)\ne0  \tag{22}
\]

from the
[physical dark-cut theorem](curvature-bearing-cap-to-k6-dark-cut.md).
The nonzero cap coefficient also detects one of its two oriented physical
transitions by equations (20)--(21) of the
[full-nine selector normal form](full-nine-isotropic-selector-blocking-normal-form.md),
the full \(3\times3\) version of the
[radial relocation identity](radial-common-line-curvature-relocation.md).
The selector is direct-zero by (17).  Hence this is a curvature-bearing
physical dark cut, not merely an aggregate matching.

Taking the contrapositive proves (8).  The same argument using (16) proves
the rank-two local refinement, even when the three sites have different
alignment labels.  Finally, for each fixed label \(e\),
\(T_e=T_e^\times\sqcup T_e^0\) with
\(T_e^0=\{x:N_{x,e}=0\}\).  Under the additional selector bound,
\(T_e^\times\) is a subset of the union in (8), so
\(|T_e^\times|\le2<|T_e|\) for every \(e\ne c\).  This proves (8a) with
the stated quantifiers.

## 5. The two-chart support normal form

Now use the literal \(pq\)- and \(pr\)-charts of one source.  At a common
residual site their \(p\)-endpoint matrix \(P_x\) is the same physical
block with the same source labels.  Suppose

\[
 P_x^{\mathsf T}J_eS_x=\lambda d,
 \qquad
 P_x^{\mathsf T}J_eR_x=\mu d',
 \qquad \lambda\mu\ne0,                                  \tag{23}
\]

with \(d,d'\) rank two.  Applying (14) to both equations shows that

\[
                  \ker d^{\mathsf T}
                    =\ker(d')^{\mathsf T}=\mathbb C\xi.    \tag{24}
\]

This is source-faithful synchronization: it uses the literally shared
\(P_x\), not an independent change of bases between two abstract charts.
Let \(\eta,\eta'\) span the right kernels of \(d,d'\).

Suppose first that both kernel contractions are targetless.  Equivalently,

\[
 \operatorname {supp}\xi\cap\operatorname {supp}\eta
 =\operatorname {supp}\xi\cap\operatorname {supp}\eta'
 =\varnothing.                                             \tag{25}
\]

If \(\xi\) is coordinate, (24) says that the corresponding literal row of
both direct blocks is zero.  If \(\xi\) is not coordinate, disjointness in
three coordinates forces \(\operatorname {supp}\xi\) to have size two
and both \(\eta,\eta'\) to be supported on the unique complementary
coordinate.  The corresponding literal column of both direct blocks is
zero.  This proves (11) without a matrix-entry census.

If either intersection in (25) is nonempty, the corresponding contraction
(5) is targetful instead.  Every nonzero alignment at a label different
from a retained kernel colour is dark for that colour.  An alignment at
the same label is also dark when both of its local endpoint maps have rank
two.  The three-site criterion of Section 4 applies to those sites; one
common site alone is not being promoted to a dark cut.

For completeness, assume the remaining support has no off-target kernel
colour.  (The three-site criterion routes such a colour whenever it occurs
at three kernel-dark sites.)  The support condition is then

\[
 \operatorname {supp}\xi\cap\operatorname {supp}\eta
 \subseteq\{e\},\qquad
 \operatorname {supp}\xi\cap\operatorname {supp}\eta'
 \subseteq\{e\}.                                          \tag{26}
\]

If \(\xi\) is coordinate, there is again a common zero row.  If it has
three supported coordinates, (26) forces both right kernels to be
\(\mathbb Ce_e\), giving a common zero column.  If it has two supported
coordinates not containing \(e\), both right kernels are the complementary
coordinate line, again giving a common zero column.  The only remaining
possibility is (12).  This is the promised target-centred cross.

The nonzero curvature minor from the joint-extraction theorem is untouched.
For its normalized nonzero entry \(A=d_{ij}\), a zero row or column simply
cannot be the selected row \(i\) or column \(j\).  If the second selected
entry \(B=d'_{ik}\) is also nonzero, the same observation applies to
column \(k\).  The power-free Bianchi identity is compatible with all
these alternatives and was not used as a substitute for (18).

## 6. The row/column boundary has an exact overlap descent

The common zero row or column in (11) is not merely a support label.  It
mixes with the literal 27-row overlap before any common power is cancelled.
Write \(P=d\), \(R=d'\), let \(T=A_{qr}\), and on the common complement of
\(p,q,r\) use the endpoint stars \(x_i,y_j,t_k\) and internal quadratic
\(z\).  The joint-extraction packet contains, for every \(i,j,k\),

\[
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[h-1]}
   +x_i y_jt_kz^{[h-2]}
       =\mathbf1_{i=j=k}X_i.                              \tag{27}
\]

Suppose first that the common zero label \(\rho\) is a row:

\[
                         P_{\rho *}=R_{\rho *}=0.          \tag{28}
\]

For every \(a\ne\rho\), the \(pq\)-functional

\[
                  e_\rho(e_\rho+u e_a)^{\mathsf T}       \tag{29}
\]

kills \(P\) and gives the same unary target \(X_\rho\) as the diagonal
\(pr\)-functional \(E_{\rho\rho}\).  Thus (29) is one diagonal anchor
plus the off-diagonal row \((\rho,a)\), not an abstract basis change.
Comparing their \(\rho\)-normal rows, or equivalently taking
\((i,j,k)=(\rho,a,\rho)\) in (27), gives

\[
 \boxed{
 x_\rho\left(y_at_\rho+{T_{a\rho}\over h-1}z\right)
          z^{[h-2]}=0.}                                   \tag{30}
\]

If \(\rho\) is instead a common zero column,

\[
                         P_{*\rho}=R_{*\rho}=0,            \tag{31}
\]

use \((e_\rho+u e_a)e_\rho^{\mathsf T}\) on the \(pq\)-chart and the
diagonal \(pr\)-functional.  The \((a,\rho,\rho)\) member of (27) is

\[
 \boxed{
 x_a\left(y_\rho t_\rho+{T_{\rho\rho}\over h-1}z\right)
          z^{[h-2]}=0
 \qquad(a\ne\rho).}                                     \tag{32}
\]

The factor \((h-1)^{-1}\) is forced by
\(zz^{[h-2]}=(h-1)z^{[h-1]}\).  At the present \(8\to6\) boundary,
\(h=3\), so (30)--(32) are explicit cubic annihilators with coefficient
\(1/2\).  They retain the direct/star/internal grading and visibly couple
an off-diagonal full-nine row to the diagonal target on the overlapping
chart.  They do not license cancellation of \(z^{[h-2]}\).  Thus the
row/column residue has descended to the already isolated filtered
overlap/Macaulay interface rather than remaining an unstructured alignment
case.

## 7. Exact scope

The proved output is a positive use of the complete full-nine source rows:

* the canonical kernel cap (5), including its explicit
  diagonal--off-diagonal coupling;
* the three-site physical dark-cut criterion (8), and the forced
  zero-wedge descent (8a) when the selector lower bounds are retained;
* reduction of any three-site two-target, rank-two nonzero alignment branch
  to a literal zero row or column;
* the two-chart targetless shared row/column normal form (11);
* after routing off-target kernel colours, the single target-centred cross
  (12); and
* the exact mixed-anchor overlap annihilators (30)--(32) on the common
  row/column boundary.

It does not claim that every set \(T_e\) has three nonzero proportionality
sites.  Zero proportionalities \(N_{x,e}=0\), the target-centred cross,
and the resulting fixed row/column hooks are the exact residues.  Nor does
the dark cut by itself solve the later Hessian-pullback, filtered source
provenance, or Macaulay prolongation problems.

The dependency-free
[checker](../computations/verify_rank_two_alignment_kernel_cap_descent.py)
audits the adjugate identity and target-line conclusion over finite fields,
exhausts the three-coordinate support classification, checks the
three-marked-site matching step, and verifies sharp local block models for
the zero-row, zero-column, and target-centred-cross residues.  Those local
models are not claimed to satisfy the global full-nine source equations.
