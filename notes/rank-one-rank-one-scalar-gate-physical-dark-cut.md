# Every maximal rank-\((1,1)\) scalar gate exports a physical dark cut

Research evidence only.  Krenn's conjecture and `SP-CLEAN-BRIDGE` remain
open, and no certified dependency changes.

## Outcome

Combine the scalar-shore clean quotient with the previously proved
blocked-target coefficient cut.  The result is uniform and removes the
scalar gate from the one-bright queue:

> **Theorem.**  On the maximal three-site-complement rank-\((1,1)\)
> scalar gate, away from the already named coordinate gates, a literal
> rank-one cap with all three diagonal targets active has a nonzero physical
> dark-cut matching and hence a nonzero physical four-cycle differential.

This is stronger than merely producing a fixed-label blocker.  It does not
yet turn the physical differential into an active clean cap; the remaining
step is the source-faithful comparison/grade transport already isolated in
the dark-cut theorem.

## 1. The rank-one scalar cap

Write the maximal shore as (W=A\sqcup B), \(|B|=3\), with

\[
 p_j^A=\lambda_jU,\qquad s_j^A=\mu_jV.                  \tag{1}
\]

On the scalar gate the direct matrix annihilates

\[
 {\cal Q}_{\lambda,\mu}
   =\{K:\lambda^{\mathsf T}K=0,\ K\mu=0\}.             \tag{2}
\]

Away from a coordinate gate, finite hyperplane avoidance chooses

\[
 x\in\ker\lambda^{\mathsf T},\qquad
 y\in\ker\mu^{\mathsf T}                               \tag{3}
\]

with every (x_i,y_i\ne0\).  Put (K=xy^{\mathsf T}\).  Then (K\in
{\cal Q}_{\lambda,\mu}\), its three diagonal coordinates
\(\kappa_i=x_iy_i\) are nonzero, and its direct scalar is zero.  The two
annihilator equations remove every response term meeting (A), leaving

\[
 r(K)=P_B(x)S_B(y)=LS.                                  \tag{4}
\]

The literal contracted full-nine row is therefore

\[
                      LSq^{[2]}=\sum_{i=0}^2\kappa_iX_i. \tag{5}
\]

All three target colours in (5) are active.

## 2. Three sites cannot block all three targets

For (e\in\{0,1,2\}), let

\[
 B_e=\{z\in W:e_e^{(z)}\in
       \operatorname {span}(L_z,S_z)\}.                 \tag{6}
\]

The two-site blocked-target theorem says that if \(|B_e|\le2\), the same
physical cap (LS) has a nonzero coefficient on two retained sites and the
physical (q)-blocks on their four-site dark complement contain a perfect
matching.  This is exactly a physical dark cut and yields the one-term
nonzero four-cycle differential.

Assume no such cut exists.  Since every target in (5) is active, the
contrapositive of that theorem gives

\[
                         |B_e|\ge3\qquad(e=0,1,2).       \tag{7}
\]

But (L,S\) are supported on (B), so no site of (A) is blocked.  Hence
every (B_e\subseteq B\), and \(|B|=3\) turns (7) into

\[
                         B_0=B_1=B_2=B.                  \tag{8}
\]

At each (z\in B\), equation (8) says that the two-dimensional-or-smaller
space \(\operatorname {span}(L_z,S_z)\) contains all three independent
coordinate axes.  This is impossible.  The assumed failure of the physical
dark cut is therefore false.

## 3. Proof impact and exact scope

The scalar branch now has two complementary exact outputs:

1. the cofactor-unit calculation forces a lost fixed target label; and
2. the blocked-target argument above unconditionally exports a physical
   dark cut before that one-bright analysis is needed.

For the shortest proof spine, (2) is the stronger routing statement.  At
eight sites the released-site zero-support split proves that no one-site
release sees all three target labels.  Hence blocker incidences occupy at
least two shore sites.  The complete incidence argument now forces a literal
target coordinate plane on either the dark shore or the physical
three-site complement; transporting that plane remains relevant to the
coordinate and endpoint-dark gates.

The output here is not an active clean cap.  The physical dark-cut theorem
explicitly leaves one load-bearing comparison: identify the sparse physical
four-cycle differential with a source-provenant residual Macaulay/weighted
selector class, or derive the clean cap directly from the same coefficient
cut.  No abstract replacement of the physical (q) by a dense
vertex-factor array is allowed.

## Exact audit

[`verify_rank_one_rank_one_scalar_gate_physical_dark_cut.py`](../computations/verify_rank_one_rank_one_scalar_gate_physical_dark_cut.py)
pins the scalar-cycle, blocked-target, and physical dark-cut dependencies.
It exhausts full-support annihilator choices over \(\mathbb F_5\) and all
512 three-site/three-colour blocker masks.  The incidence proof above is
field-independent over \(\mathbb C\); the finite audit is a regression
check, not a substitute for it.
