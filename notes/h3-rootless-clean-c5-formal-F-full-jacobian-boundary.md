# The formal corrected aggregate (F) fails the full endpoint/q kernel

## The attractive scalar correction

Write

\[
 t=q_{pq}^{00},\qquad u_v=q_{xv}^{00},\qquad
 z=q_{pq}^{22},\qquad w_v=q_{xv}^{0m_v}.
\]

The formal aggregate proposed after the first stabilizer audit is

\[
\begin{aligned}
 F&=\sum_v\Omega_v+5t-\sum_vu_v\\
  &=5z-\sum_vw_v.                                    \tag{1}
\end{aligned}
\]

Equation (1) is correct.  It also exactly kills the five previously
displayed tangents

\[
 \eta_z=X_\mu/t,\qquad \mu_{p,0}=1,\quad\mu_{z,0}=-1.
\]

Those tangents move only (t,u_z), which have cancelled from (1).

The repair is not sufficient.  The full physical endpoint/q Jacobian has
additional colour-diagonal GHZ-stabilizer columns.

## First full-Jacobian failure

Take

\[
 \lambda_{p,2}=1,\qquad\lambda_{x,2}=-1              \tag{2}
\]

and every other weight zero.  Colourwise sums vanish, so the covariance
identity gives

\[
                         JX_\lambda=0                 \tag{3}
\]

on all (3^8=6561) complete output rows.  Both weighted sites are external
to the normalized odd-site C5.  Thus (2) fixes every selected cycle cell,
every off-cycle tail, and every (q_{v,N}) ordinary-residue companion.  It
has zero target and zero ordinary residue.  Nevertheless

\[
                         dF(X_\lambda)=5q_{pq}^{22}.  \tag{4}
\]

There is a complementary failure.  For

\[
 \nu_{x,0}=1,\qquad\nu_{p,0}=-1,                     \tag{5}
\]

the same complete-source, clean-C5, target, and residue assertions hold,
while

\[
                 dF(X_\nu)=-\sum_vq_{xv}^{0m_v}.     \tag{6}
\]

Hence invariance under just these two automatic physical kernel columns
would force

\[
 q_{pq}^{22}=0,\qquad\sum_vq_{xv}^{0m_v}=0,
 \qquad F=0.                                          \tag{7}
\]

A unit-normalized/nonzero terminal correction cannot therefore be obtained
from the scalar (1).

## Source typing fails independently

(F) is a legitimate degree-one polynomial in the coefficient ring.  It
is not a source-resolution cell with the required readouts.

At first endpoint degree the complete physical route is

\[
                    (-\Omega_v,+q_{v,N};\operatorname{ores}=1),       \tag{8}
\]

not ((-\Omega_v,0;0)).  The raw polynomial (5t-\sum u_v) does not
cancel the companion or ordinary residue in (8).  At the first common
rootless (P_3\sqcup K_2) degree, each (Omega_v) must moreover be
multiplied by its own labelled (t_vN).  The six monomials in (1) have no
common such multiplier or terminal word grade.

Consequently target, ordinary residue, anchor incidence, and (W) are not
zero readouts of (F); they are **undefined**, because no physical chain
having boundary (1) has been constructed.  The fact that the test tangents
(2), (5) themselves have zero target and ordinary residue makes (4), (6)
genuine zero-indeterminacy failures rather than a readout artefact.

## Exact remaining datum

The correction still required is source-relative: a repeated-grade cell
whose complete companions implement the

\[
                         \Omega_v\longrightarrow r_v
\]

comparison with target, ordinary residue, anchor incidence, and (W) all
zero.  A coefficient-ring primitive such as (1) cannot replace that cell.

This retires only the formal (F) proposal.  It does not say that no
differently corrected terminal functional exists, and it constructs no
full physical rootless source.

Run:

```text
python3 computations/verify_h3_rootless_clean_c5_formal_F_full_jacobian_boundary.py
python3 -O computations/verify_h3_rootless_clean_c5_formal_F_full_jacobian_boundary.py
python3 -I -S computations/verify_h3_rootless_clean_c5_formal_F_full_jacobian_boundary.py
```

Frozen ledger SHA-256:

```text
0f6a4a7162615595b0b727c6f6105b65df241ec40ba19fcb45baa427d737777e
```
