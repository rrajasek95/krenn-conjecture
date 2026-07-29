# A collision rerouting circuit need not lift from its internal pair equations

## Outcome

The proposed local transport step is false, already on six sites.  There is
an exact rational binary base with an even alternating four-cycle, a
one-`z` tangent satisfying the full tangent equation, and an exactly-two-`z`
correction satisfying all six
prescribed `X_2/2` pair equations internal to that cycle.  Every one of the
four support-reducing star moves around the cycle nevertheless fails the
first lift equation

\[
                         F_0D_1=-F_1D_0.                 \tag{1}
\]

The failure is witnessed by a single coordinate, not by a dimension count.
Consequently the second equation

\[
              F_0D_2=-F_1D_1-F_2D_0                     \tag{2}
\]

is never reached.  This is not a collision two-jet, because a pair equation
joining the cycle to the two-site complement fails.  It is an exact
countermodel to any argument which tries to lift a rerouting circuit using
only the pair equations supported on that circuit.  A successful transport
proof must use complement data explicitly.

## 1. The six-site jet fragment

Let the sites be `0,...,5`, and use local symbols `x,y,z`.  Put unit `xx`
cells on

\[
                         01,23,45,02,13                  \tag{3}
\]

and unit `yy` cells on

\[
                              12,34,05.                  \tag{4}
\]

Call the resulting source `q_0`.  Its two all-`x` matchings and its one
all-`y` matching are

\[
             01\mid23\mid45,\qquad 02\mid13\mid45,
             \qquad 12\mid34\mid05,                     \tag{5}
\]

and it has no mixed matching.  Hence

\[
                              H(q_0)=2X+Y.                \tag{6}
\]

The switched core `S={0,1,2,3}` is the even alternating cycle

\[
                              0-1-3-2-0.                 \tag{7}
\]

Take the tangent

\[
\begin{aligned}
 Z=\frac12(&-z_0x_1+z_0x_2-z_1x_0+z_1x_3\\
            &+z_2x_0-z_2x_3+z_3x_1-z_3x_2)              \tag{8}
\end{aligned}
\]

and the exactly-two-`z` term

\[
 W=\frac14(z_0z_1+z_0z_2+z_1z_3+z_2z_3).               \tag{9}
\]

Direct matching expansion gives the complete tangent identity

\[
                              dH_{q_0}(Z)=0.              \tag{10}
\]

Moreover, for every pair `i<j` in `S`, and not merely in its all-`x`
coordinate,

\[
 [z_i z_j]\left(dH_{q_0}(W)+\frac12d^2H_{q_0}(Z,Z)\right)
       =\frac12\prod_{v\ne i,j}x_v.                     \tag{11}
\]

Here (11) is an equality after allowing every binary coloring of the four
unmarked sites: its all-`x` coefficient is `1/2` and all its other binary
coefficients are zero.  Thus all six prescribed pair sectors on the
rerouting cycle are present, with the normalized half-shift scalar.

## 2. Four exact support-reducing star circuits

For a star cell write `E_{pj}^{xx}` for its unit variation.  At the four
core centers take

\[
\begin{array}{c|c|c}
 p&D_0&\text{opposite core site }r\\ \hline
 0&E_{01}^{xx}-E_{02}^{xx}&3\\
 1&E_{10}^{xx}-E_{13}^{xx}&2\\
 2&E_{23}^{xx}-E_{20}^{xx}&1\\
 3&E_{32}^{xx}-E_{31}^{xx}&0.
\end{array}                                               \tag{12}
\]

In each row, the two displayed cells have the same full derivative tensor,
namely `X`, because their complementary `xx` edges complete the two
matchings in (5).  Therefore

\[
                               F_0D_0=0.                  \tag{13}
\]

This is not merely infinitesimal.  No perfect matching can contain two
cells from a fixed star, so

\[
                         H(q_0+sD_0)=H(q_0)               \tag{14}
\]

for every scalar `s`.  At `s=1` the negatively varied unit cell disappears.
Each row of (12) is therefore an exact support-reducing base-fiber move.
They are the four star views of the alternating circuit (7).

## 3. A one-coordinate obstruction to the first lift

Expand the deleted-star cofactor map along the jet

\[
             F_p(t)=F_0+tF_1+t^2F_2.                    \tag{15}
\]

A transported graded star move would have

\[
 D(t)=D_0+tD_1+t^2D_2,                                  \tag{16}
\]

where every cell of `D_1` has exactly one `z` and every cell of `D_2` has
two.  Equating coefficients gives (13), (1), and (2).

Fix a row of (12), and let

\[
                         \chi_r=z_r\prod_{v\ne r}x_v     \tag{17}
\]

for its opposite core site `r`.  Directly from (8), the two deleted-star
cofactors give

\[
                              [\chi_r]F_1D_0=-1.          \tag{18}
\]

For example, at `p=0`, the `z_3` tangent cells on `23` and `13` have
coefficients `-1/2` and `+1/2`; the signs in
`D_0=E_{01}^{xx}-E_{02}^{xx}` turn their difference into `-1`.

On the other hand,

\[
                              [\chi_r]F_0D_1=0            \tag{19}
\]

for every possible one-`z` star variation `D_1`, including cells outside
the current support.  Indeed, the only star cell compatible with (17) is
`x_pz_r` on `pr`.  Its all-`x` cofactor is on the other two core sites and
the tail sites `4,5`.  The tail can be matched only by `45`, while the two
remaining core sites are `12` or `03`; neither is an `xx` cell of (3).
The cofactor is therefore zero.

Equations (18)--(19) make (1) read `0=1` in the single coordinate
`chi_r`.  Thus none of the four exact base-star moves lifts even to first
order.  In particular no choice of `D_1`, and hence no subsequent choice of
`D_2`, can solve the coupled system (1)--(2).

## 4. The exact missing complement equation

The fragment above is deliberately not a full collision jet.  For the pair
`{0,4}`, the coefficient of

\[
                              z_0z_4x_1x_2x_3x_5         \tag{20}
\]

on the left of the second collision equation is zero: (8) has no `z_4`
sector, and the direct `z_0z_4` cofactor leaves site `5` without an `xx`
partner.  Its prescribed value is `1/2`.

This locates the logical boundary exactly.  The alternating-circuit
combinatorics, the full tangent equation, and all normalized pair equations
whose marked sites lie on the circuit do not force transport.  The first
available obstruction lies across the cut from the circuit to its
complement.  The even-cycle alternative already defeats the local claim,
so analyzing odd-handcuff closure cannot repair that claim without adding
such external equations.

[`verify_collision_rerouting_transport_countermodel.py`](../computations/verify_collision_rerouting_transport_countermodel.py)
checks (6), every coordinate of (10), all binary coordinates of the six
identities (11), all four support-reducing moves (12), the explicit
coefficient certificate (18)--(19), and the failed external coefficient
(20), using exact rational arithmetic.  As a redundant audit, it also
forms the complete linear systems for `D_1,D_2`; their coefficient and
augmented ranks differ by one at every center.
