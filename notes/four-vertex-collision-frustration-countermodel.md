# A six-site countermodel to four-vertex collision frustration

## Outcome

There is no universal contradiction obtained from the six collision pair
equations on one chosen four-vertex set after quotienting each equation by
its direct `Q_2` cofactor.  Already at `n=6`, an exact binary base
`H(q_0)=2X+Y` has a rational one-`z` tangent `Z` and direct two-`z`
coefficients on four core sites which solve **all six** second-order pair
equations on that core.

The same source fails on every core--tail pair.  Thus the genuine
obstruction is not an intrinsic Pluecker or sign-frustration identity on
four sites; it uses how those sites couple to the complement.

## 1. The exact binary base

On vertices `0,...,5`, put unit `xx` cells on

\[
             01,\ 23,\ 45,\ 02,\ 13                     \tag{1}
\]

and unit `yy` cells on

\[
                         12,\ 34,\ 05.                    \tag{2}
\]

The two all-`x` matchings are

\[
                  01\mid23\mid45,
 \qquad           02\mid13\mid45,                         \tag{3}
\]

and the only all-`y` matching is `12|34|05`.  There is no mixed
matching, so

\[
                             H(q_0)=2X+Y.                 \tag{4}
\]

This is the active `n+2` switched base.  Its switched core is
`S={0,1,2,3}` and `45` is the tail edge.

## 2. A rational tangent on the core

Define

\[
\begin{aligned}
 Z=\frac12(&-z_0x_1+z_0x_2-z_1x_0+z_1x_3\\
            &+z_2x_0-z_2x_3+z_3x_1-z_3x_2).              \tag{5}
\end{aligned}
\]

There is no `z` at vertices `4,5`.  The four site sectors in (5) are
respectively scalar multiples of

\[
\begin{array}{c|c}
0&z_0(-x_1+x_2),\\
1&z_1(-x_0+x_3),\\
2&z_2(-x_0+x_3),\\
3&z_3(-x_1+x_2).
\end{array}                                                \tag{6}
\]

Each displayed vector is in its complete one-`z` tangent kernel.  Exact
matching expansion gives

\[
                              dH_{q_0}(Z)=0.               \tag{7}
\]

No cancellation outside the displayed core is suppressed in (7); the
identity holds on every one-`z`, otherwise binary coloring of all six
vertices.

## 3. All six core pair equations hold

Put a direct `zz` coefficient in `W` on the four core vertices by

\[
 \eta_{01}=\eta_{02}=\eta_{13}=\eta_{23}=\frac14,
 \qquad
 \eta_{03}=\eta_{12}=0.                                  \tag{8}
\]

Then, for every pair `i<j` in `S` and every binary coloring of the other
four sites,

\[
 [z_i z_j]\left(
 dH_{q_0}(W)+\frac12d^2H_{q_0}(Z,Z)
 \right)
 =\frac12\prod_{v\ne i,j}x_v.                            \tag{9}
\]

Equivalently, after adjoining the free direct cofactor in each pair sector,
the quotient Hessian equations all have the required target class.

In coordinates adapted to the complete tangent kernels, retain only one
parameter at each core site.  Calling them `k_0,...,k_3`, the nontrivial
quotient equations reduce to

\[
                         -2k_0k_3=\frac12,
 \qquad                  -2k_1k_2=\frac12.                \tag{10}
\]

The choice

\[
                         k_0=k_1=\frac12,
 \qquad                  k_2=k_3=-\frac12                 \tag{11}
\]

is exactly (5); the remaining four all-`x` equations determine the four
nonzero values in (8).  Mixed binary coefficients force no further
condition when the unused tangent-kernel coordinates are zero.

## 4. Why the tail is essential

For example, consider the pair `{0,4}`.  In the coefficient

\[
                         z_0z_4x_1x_2x_3x_5,              \tag{12}
\]

a direct `W` cell has zero cofactor, because vertex `5` is left without an
`xx` neighbor.  The tangent (5) has no `z_4` sector, so its Hessian
contribution is also zero.  The required coefficient is `1/2`.

More generally, the switched-base obstruction factors every core--tail
coefficient through explicit tangent equations.  The core subsystem (9)
therefore does not merely miss a convenient proof: it is exactly soluble.

## 5. Consequence

Any successful four-vertex-looking invariant must retain complement data,
for example marked cofactors involving at least one external vertex.  An
identity formed only from the six pair equations on a quadruple, their
direct `Q_2` cofactor lines, and the four local tangent variables cannot
give a universal contradiction.

[`verify_four_vertex_collision_countermodel.py`](../computations/verify_four_vertex_collision_countermodel.py)
checks (4), (7), and every binary component of all six identities (9) over
the rationals, and checks the failed tail coefficient (12).
