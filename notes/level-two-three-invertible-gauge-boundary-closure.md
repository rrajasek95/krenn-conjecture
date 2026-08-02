# Rank 55 removes the gauge-dependence boundary in the three-invertible normal form

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

Consider the (3I+1R+2Z) generic-kernel normal form with

\[
 I=\{0,1,2\},\qquad t=3,\qquad Z=\{4,5\},
\]

and potentials

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0.
\]

If \(X_i\) is invertible for \(i\in I\), \(X_t\) is nonzero rank one,
and \(X_4=X_5=0\), then differential rank (55) automatically makes the
five trace-zero vertex gauges independent. Hence they exhaust the
five-dimensional differential kernel. The gauge-dependence boundary listed
in the earlier L1 normal form cannot occur at rank (55).

## Forced nonbipartite core

The generic-kernel equation is

\[
 X_rJX_u^{\mathsf T}=(\nu_r+\nu_u)M_{ru}.             \tag{1}
\]

For \(i,j\in I\), the numerator in (1) is invertible, so every \(M_{ij}\)
is invertible. For \(i\in I\), the numerator
\(X_iJX_t^{\mathsf T}\) is nonzero rank one, so every \(M_{it}\) is
nonzero. Thus the live-block graph contains the triangle on (I), joined
to (t).

Also \(\nu_4+\nu_5=-2\tau\ne0\), while the numerator on (45) is zero;
hence

\[
                              M_{45}=0.                \tag{2}
\]

## An unattached zero site forces rank at most 20

Suppose a zero site (z\in Z) has no nonzero block to the core
\(I\cup\{t\}). By (2), (z) is isolated in the residual packet. A
differential column belonging to an edge not incident with (z) leaves
(z) in the complementary four-site matching, where every possible
incident factor is zero. Such a column vanishes identically. Only the five
blocks incident with (z) can contribute, and they supply (5\cdot4=20)
cell columns. Therefore

\[
                         \operatorname{rank}d\Psi_M\le20.          \tag{3}
\]

At rank (55), each zero site must consequently have a live spoke to the
core. The full live graph is then connected and contains the triangle on
(I).

## Gauge independence

A trace-zero vertex gauge has blocks

\[
 G(\mu)_{ru}=(\mu_r+\mu_u)M_{ru},\qquad \sum_r\mu_r=0. \tag{4}
\]

If (G(\mu)=0), every live edge imposes
\(\mu_r+\mu_u=0\). On a connected graph containing an odd cycle, these
equations force every \(\mu_r=0\). Thus the five-dimensional trace-zero
gauge space injects into \(\ker d\Psi_M\). When the differential rank is
(55), its kernel has dimension (60-55=5), so the gauges are the entire
kernel.

The standard-library checker
[verify_level_two_three_invertible_gauge_boundary_closure.py](../computations/verify_level_two_three_invertible_gauge_boundary_closure.py)
enumerates all (15^2=225) nonempty spoke choices for the two zero sites,
verifies connected nonbipartiteness and rank five of the trace-zero gauge
map in every case, and audits the isolated-site differential-column count.

