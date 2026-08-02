# The rank-\((1,1)\) scalar gate is one adjacent-power comparison

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Work on the maximal \(b=3\), rank-\((1,1)\) shore and its four-dimensional
clean double-annihilator plane \({\cal Q}_{\lambda,\mu}\).  On the scalar
gate,

\[
 \sigma\big|_{{\cal Q}_{\lambda,\mu}}=0.                   \tag{1}
\]

Choose \(K_0\in{\cal Q}_{\lambda,\mu}\) away from the three coordinate
gates, and write \(r_0=r(K_0)\).  Then \(r_0\) is supported on the
three-site complement \(B\), so

\[
                         r_0^{[2]}=0.                       \tag{2}
\]

Let \(N\) be any physical cap direction with

\[
 s=\sigma(N)\ne0,\qquad r_1=r(N),\qquad K_\tau=K_0+\tau N. \tag{3}
\]

Define two literal source classes

\[
\begin{aligned}
 A_N&=
 r_0\sum_{k=1}^{h-1}
       s^{h-1-k}q^{[h-1-k]}r_1^{[k]},\\
 B_N&=
 \sum_{j=2}^{h}
       s^{h-j}q^{[h-j]}r_1^{[j]}
       ={\cal E}(N).
\end{aligned}                                               \tag{4}
\]

Then the entire homogeneous clean error on the scalar-activating line is

\[
\boxed{
 {\cal E}(K_\tau)=
       \tau^{h-1}\bigl(A_N+\tau B_N\bigr).}                 \tag{5}
\]

Thus the order-\((h-1)\) collision at the clean but scalar-inactive plane
is automatic.  After removing it, the formerly high-degree vector
equation is only one affine comparison between two adjacent-power source
classes.  A nonzero clean member exists on this line exactly when

\[
                         A_N+\tau B_N=0                     \tag{6}
\]

for some \(\tau\ne0\); it is active provided the three diagonal entries of
\(K_0+\tau N\) remain nonzero.  Equivalently, either both classes vanish,
or they are nonzero and proportional with the required nonzero ratio.

The first class is the literal adjacent-power transgression

\[
 A_N=r_0\left[
     s^{h-1}\left(q+\frac{r_1}{s}\right)^{[h-1]}
       -s^{h-1}q^{[h-1]}\right].                            \tag{7}
\]

The second is the ordinary clean error of the activating direction.
Equation (5) therefore gives the precise Bockstein/Yoneda-type comparison
that was missing from the scalar-gate description: it is not necessary to
construct an abstract secondary operation before identifying its two
source representatives.

This does not prove that a suitable direction \(N\) exists.  The remaining
task is to force the proportionality (6), with an admissible ratio, from
the complete one-bright rows or to show that failure of proportionality
creates a source-provenant annihilator.  The reduction is uniform in
\(h\ge3\) and retains arbitrary complex cancellation.

## Exact derivation

Linearity gives

\[
 \sigma(K_\tau)=\tau s,\qquad
 r(K_\tau)=r_0+\tau r_1.
\]

The divided-power binomial rule and (2) leave only the terms containing
zero or one copy of \(r_0\):

\[
 (r_0+\tau r_1)^{[j]}
 =\tau^{j-1}r_0r_1^{[j-1]}+\tau^jr_1^{[j]}
 \qquad(j\ge2).                                             \tag{8}
\]

Substituting (8) into

\[
 {\cal E}(K_\tau)=\sum_{j=2}^h
  (\tau s)^{h-j}q^{[h-j]}
       (r_0+\tau r_1)^{[j]}
\]

puts every first summand at order \(\tau^{h-1}\) and every second summand
at order \(\tau^h\).  Reindexing the first sum by \(k=j-1\) gives (4)--(5).
The divided-power expansion of
\((q+r_1/s)^{[h-1]}\) gives (7).

## Exact audit

The standard-library checker
[verify_rank_one_rank_one_scalar_gate_adjacent_power_comparison.py](../computations/verify_rank_one_rank_one_scalar_gate_adjacent_power_comparison.py)
works in the universal site-square-zero support algebra over exact
rationals.  It constructs three-site square-zero base responses, arbitrary
normal responses, and full quadratics; then it checks (5) at six parameter
values for \(h=3,4,5\).  All 12 deterministic rational packets have both
adjacent classes nonzero.  One aggregate SHA-256 digest pins the exact
coefficient ledger.  The checker passes normally, with -O, and with
-I -S.
