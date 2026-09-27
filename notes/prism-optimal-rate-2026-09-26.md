# The optimal leading rate coefficient within the prism architecture

September 26, 2026. **Written research; exact supporting checks; awaiting audit.**

[Explainer](../explainers/RATE-DESIGN-FRONTIER.md) ·
[Replay](../computations/rate-design-frontier-2026-09-26/README.md)

The earlier prism calculation established achievability of a square-root
rate. This note proves its leading coefficient is optimal over **all unequal
complex weights on the same nine colored cells**. It does not prove that
the prism is optimal among different architectures, or settle the square-root
law for all diagonal complex sources.

## 1. Exact output and a sharp architecture-specific inequality

Write the two internal weights of color \(h\) as \(x_h,y_h\), and its
vertical weight as \(z_h\). The matching expansion is exactly

\[
 H=\tau_a a^6+\tau_b b^6+\tau_c c^6+\mu\,bcabca,
 \quad \tau_h=x_hy_hz_h,\quad \mu=z_az_bz_c.
\]

Put \(S=\sum_h(|x_h|^2+|y_h|^2+|z_h|^2)\). Arithmetic–geometric mean
on the six internal squared magnitudes gives the polynomial product bound

\[
 |\tau_a\tau_b\tau_c|
 =|\mu|\prod_h|x_hy_h|
 \le |\mu|(S/6)^3.                                \tag{1}
\]

Let \(b(F)=\sqrt F-\sqrt{2(1-F)}\). For \(F>2/3\), the standard
target-orthogonal projection estimate gives
\(\prod_h|\tau_h|\ge(\|H\|/\sqrt3)^3 b(F)^3\).
Also \(|\mu|\le\sqrt{1-F}\|H\|\). Substitution into (1) proves

\[
 \boxed{R\le\frac{\sqrt3}{72}
       \frac{\sqrt{1-F}}{b(F)^3}.}                 \tag{2}
\]

This holds globally on the prism support, with arbitrary phases and unequal
pure amplitudes. The coefficient is approximately 0.0240563.

For \(x_h=y_h=1,z_h=t>0\),

\[
 F=\frac3{3+t^4},\qquad
 R=\frac{t^2(3+t^4)}{27(2+t^2)^3},\qquad
 \lim_{t\to0}\frac{R}{\sqrt{1-F}}=\frac{\sqrt3}{72}.
\]

Thus the leading coefficient in (2), not only its exponent, is optimal on
this architecture.

## 2. The complete frontier when pure amplitudes are balanced

If \(\tau_a=\tau_b=\tau_c=\lambda\ne0\), put
\(r=|\mu|/|\lambda|=\sqrt{3(1-F)/F}\).
Arithmetic–geometric mean separately on the internal and vertical weights gives

\[
 S\ge6(|\lambda|^3/|\mu|)^{1/3}+3|\mu|^{2/3}.
\]

Consequently

\[
 \boxed{R\le\frac{r(3+r^2)}{27(2+r)^3}.}           \tag{3}
\]

Equality is attained by equal internal weights and equal vertical weights
with squared magnitude ratio \(r\). Therefore (3) is the exact normalized
strength frontier at each specified fidelity among balanced prism sources.
For a fidelity floor rather than an exact fidelity, one must additionally
maximize this expression over the allowed fidelities.

## 3. Optimal Gaussian success probability to leading order

Now specify nine disjoint two-mode squeezed sources, one for each prism cell,
with no other pair cells and ideal exact-number selection. Each edge modulus
is less than one, and

\[
 P=\|H\|^2\prod_{e=1}^9(1-|w_e|^2).
\]

For \(0\le x<1\), \(x(1-x^2)\le2/(3\sqrt3)\). Applying this to the
six internal weights, and bounding each vertical vacuum factor by one, gives

\[
 \boxed{P\le\frac{64\sqrt3}{6561}
                  \frac{\sqrt{1-F}}{b(F)^3}.}     \tag{4}
\]

Indeed multiply the pure-product lower bound by the vacuum factors and use
\(\prod_h|\tau_h|/|\mu|=\prod_h|x_hy_h|\).
The leading coefficient is approximately 0.0168955. It is attained as
\(t\to0\) by \(x_h=y_h=1/\sqrt3,z_h=t/\sqrt3\).

There is also an asymptotic rigidity conclusion. Any prism family attaining
this leading coefficient as \(F\to1\) must have all six internal moduli
tending to \(1/\sqrt3\), and all three vertical moduli tending to zero.
Every factor used in the upper bound is individually bounded, so attaining
their product maximum forces each factor to attain its own maximum.
The elementary identity

\[
 \frac{2}{3\sqrt3}-x(1-x^2)
 =(x-1/\sqrt3)^2(x+2/\sqrt3)
\]

also gives quantitative control of departures from the optimal internal
moduli. Phases must still make the pure amplitudes approach the chosen GHZ
target, as required by \(F\to1\).

These probability claims use the specified nine-source Gaussian model.
They do not optimize over additional pair cells, ancillary modes, or other
detection protocols. The unrestricted diagonal square-root law remains open.
