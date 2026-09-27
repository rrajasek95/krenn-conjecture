# Sharp-rate certificates: integral dependence, arcs, and an SOS obstruction

September 26, 2026. **Written research and exact supporting replay; awaiting
independent audit. The unrestricted square-root rate law remains open.**

[Guide](../explainers/METHOD-UTILITY.md) ·
[Replay](../computations/method-utility-2026-09-26/README.md)

## 1. The exact target for the next proof

For the six-site ternary model let
\(H(A)=\lambda(A)\Delta+E(A)\), with
\(\lambda=(H_{a^6}+H_{b^6}+H_{c^6})/3\), \(\Delta=a^6+b^6+c^6\),
and \(S=\sum|A_{uv}(i,j)|^2\). Set \(\epsilon=\|E\|_2\).
The sought estimate on \(S=1\) is

\[
             |\lambda|^3\le M\epsilon.               \tag{1}
\]

It would give

\[
 R\le3\sqrt3 M\frac{\sqrt{1-F}}{F^{3/2}}.             \tag{2}
\]

The unrestricted written estimate currently controls \(|\lambda|^{16}\),
which yields exponent \(1/15\). The prism forces any universal rate exponent
to be at most \(1/2\). Neither the following reformulation nor the example
certificates bridge that gap by themselves.

## 2. Integral dependence gives checkable sufficient certificates

Let \(J=(E_w)_w\) be the polynomial ideal of unwanted output coefficients,
and put \(f=\lambda^3\). Instead of requiring \(f\in J\), seek a monic
identity

\[
 f^r+a_1 f^{r-1}+\cdots+a_r=0,\qquad a_j\in J^j.       \tag{3}
\]

The condition is called integral dependence over the ideal. The link between
integral closure, local norm inequalities, and orders on analytic curves is
classical: [Lejeune-Jalabert--Teissier, §§2, 5--6](https://afst.centre-mersenne.org/articles/10.5802/afst.1203/).
We are applying that theory, not claiming a new general algebraic criterion.

Supply each \(a_j\) explicitly as a sum of polynomial multipliers times
products of exactly \(j\) error generators. On the source unit ball, an
upper bound \(b_j\) for the sum of the multipliers' coefficient magnitudes
gives \(|a_j|\le b_j\epsilon^j\). Choose a rational \(M>0\) with
\(\sum_j b_j/M^j\le1\). Equation (3) then implies (1): if
\(t=|f|/\epsilon>M\), division of (3) by \(|f|^r\) gives
\(1\le\sum_j b_j/t^j<1\). If \(\epsilon=0\), (3) directly forces \(f=0\).

The new checker verifies every polynomial coefficient of (3), the required
ideal-power factorizations, and the rational majorant. Complex coefficients
are Gaussian rationals, with \(|z|\le|\Re z|+|\Im z|\) for coefficient bounds.
An unrestricted certificate has not been found. No bounded monic degree or
practical search complexity is asserted.

Two examples exercise different cases:

- \(f=xy\), \(J=(x^2,y^2)\): \(f\notin J\), but
  \(f^2-x^2y^2=0\) is a genuine degree-two integral certificate.
- On the nine-cell prism only, write \(\tau_h=\lambda+e_h\),
  \(\sum e_h=0\), \(\mu=z_a z_b z_c\), and
  \(P=\prod_hx_hy_h\). Then
  \(\lambda^3-P\mu+\lambda\sum_{i<j}e_i e_j+e_a e_b e_c=0\).
  This is a degree-one certificate on that restricted architecture. It does
  not contradict the full-model nonmembership theorem. The coarse checker
  gives \(M=5\); the earlier prism analysis gives sharper constants.

## 3. Why a direct holomorphic sum-of-squares search cannot work

The [earlier exact dual](complex-rate-bound-2026-09-26.md#6-even-the-balanced-cubic-polynomial-shortcut-fails)
proves \(\lambda^3\notin J\), even on the 45 diagonal variables.

**Consequence.** For every constant \(C\ge0\), the homogeneous polynomial

\[
 P_C(A,\overline A)=C S^6\sum_w|E_w|^2-|\lambda^3|^2             \tag{4}
\]

is not a sum \(\sum_j|p_j(A)|^2\) of squared absolute values of holomorphic
polynomials. This excludes a common direct complex Gram-matrix certificate
for (1). It does not assert that (4) is negative somewhere.

**Proof.** Use the vector of all holomorphic monomials of degree nine.
The coefficient matrix of the first term of (4) is positive semidefinite,
with range spanned by coefficient vectors of \(A^\alpha E_w\),
\(|\alpha|=6\). This follows by expanding \(S^6\) with its positive
multinomial coefficients. The coefficient vector \(v\) of \(\lambda^3\)
is outside this range, by nonmembership. There is a vector \(u\) orthogonal
to the range with \(u^*v\ne0\). The coefficient matrix of (4) consequently
has quadratic form \(-|u^*v|^2<0\) on \(u\). A holomorphic squared-modulus
decomposition would require this matrix to be positive semidefinite.
Homogeneity forces every nonzero polynomial in such a decomposition to have
degree nine, so nonhomogeneous terms do not avoid the argument. Restriction
to the diagonal source variables rules out a decomposition in the full model
as well. \(\square\)

Real sums of squares in real and imaginary coordinates remain possible, as
do integral-dependence and local geometric arguments. The distinction is
already visible in

\[
 |x^2|^2+|y^2|^2-2|xy|^2=(|x|^2-|y|^2)^2\ge0.
\]

The right side is a real polynomial square; its left side has an indefinite
holomorphic coefficient matrix. The replay rechecks all 18,420 columns of the
previous nonmembership certificate, rather than merely trusting its receipt.
The analytic deduction about Gram matrices is given above.

## 4. Exact paths can refute the sharp exponent

Let \(A(t)\) be analytic, with \(A(0)\ne0\), and suppose

\[
 \lambda(A(t))=\Theta(t^r),\qquad
 \|E(A(t))\|=\Theta(|t|^s),\qquad s>r>0.
\]

Along positive real \(t\), source normalization has a finite nonzero limit,
so

\[
 R=\Theta(t^{2r}),\quad 1-F=\Theta(t^{2(s-r)}),\quad
 \boxed{R=\Theta((1-F)^{r/(s-r)})}.                 \tag{5}
\]

Thus any exact path with \(s>3r\) disproves the universal square-root law.
The analytic curve criterion says that local (1) is equivalent to
\(s\le3r\) on every relevant complex analytic curve. Applying the local
criterion on charts covering the normalized zero-output boundary, and then
compactness, is a route to a uniform inequality. The missing part is proving
the criterion on *all* those charts.

The new path checker accepts complete polynomial source paths and expands
every matching coefficient exactly. It never treats a truncated output
series as the entire output. It reports \(r,s\), the resulting rate exponent,
and whether \(s>3r\). The replay verifies ordinary prism paths, a time
reparametrization, and a path with exact destructive cancellation; all have
\(s/r=3\), not a violation.

Any analytic violating path with finite \(r,s\) can be truncated far enough
to preserve those orders. However, Gaussian-rational path coefficients are
only a subset of possible complex coefficients. The present checker is a
reliable verifier for supplied paths, not a complete search or a proof that
no counterexample exists.

## 5. What the machinery now rules in and rules out

The universal sharp inequality remains an open research target. We now have
a concrete acceptance format for one kind of positive certificate, a precise
counterexample format, and a rigorous reason to skip direct holomorphic SOS
searches. Successful restricted examples test those formats; they do not
certify the unrestricted claim.
