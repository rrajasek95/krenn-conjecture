# The endpoint-to-collision comparison has a pure-Eq edge defect and a primitive vertex defect

## Exact comparison

Fix a deleted face (v), one selected residual matching (N), and the
incident C5 multiplier (t_v) which moves the route into the first repeated
(P_3\sqcup K_2) degree.  The complete endpoint bar has typed boundary

\[
 B_{v,N}=(-t_v\Omega_v,+Q_{v,N};\operatorname{ores}=1),
 \qquad Q_{v,N}=t_vq_{v,N},                            \tag{1}
\]

where

\[
 \Omega_v=(q_{pq}^{22}-q_{pq}^{00})
            -(q_{xv}^{0m_v}-q_{xv}^{00}).              \tag{2}
\]

The rootless collision presentation of the same multiplier route is

\[
 P_{v,N}=(-r_v,+Q_{v,N};\operatorname{ores}=1).        \tag{3}
\]

Thus their formal difference is exactly

\[
 \boxed{P_{v,N}-B_{v,N}=t_v\Omega_v-r_v.}              \tag{4}
\]

Both the matching companion and ordinary residue cancel.  Equation (4) is
the desired comparison boundary, with zero target and (W) as well.

It is not yet a source chain.  Equations (1) and (3) are two target
presentations of the same marked multiplier route, not two independent
literal source cells.  Subtracting them is precisely the chain homotopy to
be constructed.  Calling that subtraction an available source combination
would assume the sought comparison.

## Literal endpoint boundary

After factoring the common selected (t_vN), the four endpoint terms in
(-t_v\Omega_v) are

\[
 -t_vq_{pq}^{22}+t_vq_{pq}^{00}
 +t_vq_{xv}^{0m_v}-t_vq_{xv}^{00}.                    \tag{5}
\]

The two paths through (pq:02) and (pq:20) give the same first and last
terms; their difference is the ordinary Bianchi square.  Completing the
four residual sites gives the same (Q_{v,N}) in (1).  Hence (4) has no
hidden endpoint-order or matching sign.

For adjacent faces, the selected face monomials have a cubic lcm.  On the
five odd sites its degree profile is

\[
                         (2,1,1,1,1),                  \tag{6}
\]

up to order.  This is the first physical degree in which (1) and the
rootless collision ridge can meet.

## What the first genuine source square gives

Put

\[
                         C_v=t_v\Omega_v-r_v.           \tag{7}
\]

The first source-labelled object is not a vertex (C_v).  It is the
adjacent denominator/PP square.  In the strict two-chart symbol its
comparison boundary is (C_v-C_w).  Physical descent adds the known pure
Eq face:

\[
 dS_{vw}=C_v-C_w+\delta_{vw}(H_0-u)e_{\rm Eq},          \tag{8}
\]

where cyclically

\[
 (\delta_{vw})=(a-b,c-d,e-a,b-c,d-e).                  \tag{9}
\]

This answers the source-typing question sharply.  The unmatched term in
the first actual square is not another response companion: those cancelled
already in (4).  It is the reduced pure-Eq face in (8).

The pinned complete full-nine/cap calculation separates the required
correction by

\[
                  \text{pure Eq}+\operatorname{ainc}. \tag{10}
\]

Every admitted correction is killed by (10), while
(-\delta_{vw}(H_0-u)e_{\rm Eq}) is read nontrivially.  Therefore the old
normal, response, full-nine, and cap rows do not turn (8) into a clean
comparison edge.  A zero-anchor reduced pure-Eq face is the first new
source datum.

## The next obstruction is the comparison aggregate

Even grant all five reduced Eq faces and delete the last term of (8).  The
five remaining boundaries (C_v-C_w) form the oriented incidence matrix of
(C_5).  Their image has saturated rank four, and the primitive covector

\[
                            \sum_v C_v^*               \tag{11}
\]

kills every edge.  It reads one on a single desired comparison (C_v).
Thus adjacent squares can synchronize all five endpoint/rootless typings,
but cannot choose the common diagonal value.  One genuine source-labelled
vertex comparison—or equivalently a generator with nonzero aggregate—is
still required.

There are therefore two distinct missing data, in order:

1. a zero-anchor reduced pure-Eq correction for each physical adjacent PP
   square;
2. after those are supplied, one primitive vertex/aggregate
   (Omega\)-to-(r) comparison generator.

The second must not be identified with the primitive physical anchor
incidence used by Component III; its target, (W), ordinary residue, and
anchor incidence are all zero.

## Scope and verification

This is an exact no-go for the committed endpoint bars, matching/Bianchi
companions, first repeated (P_3\sqcup K_2) PP degree, and complete bounded
full-nine/cap descent.  It does not exclude a new relative source-resolution
generator of either type above.

Run:

```text
python3 computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py
python3 -O computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py
python3 -I -S computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py
```

The checker pins the complete endpoint, first-collision, zero-anchor
descent, typed-composition, and denominator/PP audits.  It expands all five
literal endpoint ridges, reconstructs the common repeated degrees, verifies
the formal comparison difference, replays the pure-Eq/anchor separator, and
proves the primitive rank-four C5 comparison cokernel.

Frozen ledger SHA-256:

```text
531f6e1ed9d2bc058ad4fba551e84663e397830de818ce310532a41338b2351c
```
