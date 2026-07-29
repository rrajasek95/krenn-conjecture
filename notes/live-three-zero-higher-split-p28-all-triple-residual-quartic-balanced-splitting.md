# The \(p=28\) all-triple residual quartic has balanced splitting

## 1. Result and scope

Assume the exact residual-quartic conclusion of the
[all-triple \(q=5\) frontier](live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier.md).
Thus a saturated six-space \({\cal K}\subseteq\mathbb C[z]_{\leq10}\)
has a basis evaluation vector

\[
 F(z)=E(t)+zO(t),\qquad t=z^2,
\]

and

\[
 E\wedge O\wedge E'\wedge O'
   =\prod_{\nu=1}^{10}(t-a_\nu^2)\,Q(t),\qquad
 0\ne Q(t)\in\bigwedge^4\mathbb C^6[t],\quad\deg Q\leq4. \tag{1}
\]

Every nonzero value of \(Q\) is decomposable.

**Theorem 1.1 (balanced residual splitting).**  The coordinates of
\(Q\) have no nonconstant common factor, its projective degree is exactly
four, and the rank-two annihilator bundle of its four-planes splits as

\[
                         {\cal A}\simeq
                  {\cal O}_{\mathbb P^1}(-2)\oplus
                  {\cal O}_{\mathbb P^1}(-2).              \tag{2}
\]

Equivalently, after choosing a polynomial minimal basis there are two
independent quadratic covectors

\[
 \lambda(t)=\lambda_0+t\lambda_1+t^2\lambda_2,\qquad
 \mu(t)=\mu_0+t\mu_1+t^2\mu_2                         \tag{3}
\]

whose common kernel is the four-plane represented by \(Q(t)\), and no
nonzero annihilating covector of degree zero or one exists.

This is a strict sharpening of the residual frontier, not a profile
closure.  A balanced quadratic pair is a genuine nonconstant
Grassmannian quartic, so a further argument must use the ten exact
order-three rows, another selection family, or an unreduced tensor
equation.

## 2. Remove a possible scalar gcd

Let \(g(t)\) be the gcd of the Pluecker coordinates of \(Q(t)\), and put
\(\widetilde Q=Q/g\).  Homogenize its coordinates to their actual maximum
degree \(d\).  Primitivity removes every finite common zero, and the use of
the actual maximum degree removes a common zero at infinity.  Hence
\(\widetilde Q\) defines a morphism

\[
 \phi:\mathbb P^1\longrightarrow\operatorname {Gr}(4,6)
\]

of Pluecker degree

\[
                              d\leq4.                       \tag{4}
\]

For generic \(t\), the represented four-plane is

\[
              W_t=\langle E(t),O(t),E'(t),O'(t)\rangle.    \tag{5}
\]

The equality extends through the exceptional points as a limiting
four-plane, but only the generic equality is needed below.

## 3. The annihilator bundle

Let \({\cal A}\) be the pullback of the rank-two tautological bundle on
the dual Grassmannian:

\[
              {\cal A}_t=W_t^\perp\subset(\mathbb C^6)^*.
\]

By Birkhoff--Grothendieck, after ordering the two summands,

\[
 {\cal A}\simeq{\cal O}(-\alpha)\oplus{\cal O}(-\beta),
 \qquad0\leq\alpha\leq\beta,\qquad
 \alpha+\beta=d.                                          \tag{6}
\]

The last equality is the definition of the Pluecker degree through
\(\det({\cal A})^*\).

A generator of the first summand is a nonzero polynomial covector
\(\rho(t)\) of degree at most \(\alpha\).  Since it annihilates (5),

\[
 \rho E=\rho O=\rho E'=\rho O'=0                         \tag{7}
\]

as polynomial identities.

## 4. Degree zero and one are impossible

If \(\deg\rho=0\), equations (7) give

\[
                       \rho F(z)=\rho E(z^2)+z\rho O(z^2)=0
\]

identically.  This is a constant linear relation among the six basis
polynomials of \({\cal K}\), impossible.

Suppose instead that \(\deg\rho=1\).  Differentiating the first two
identities in (7), and using the last two, gives

\[
                         \rho'E=\rho'O=0.                  \tag{8}
\]

The covector \(\rho'\) is constant.  If it is nonzero, (8) again gives
the forbidden constant relation \(\rho'F=0\).  If it is zero, then
\(\rho\) was constant and the preceding paragraph applies.

Thus \(\alpha\geq2\).  Equation (6), together with \(d\leq4\) and
\(\alpha\leq\beta\), forces

\[
                         \alpha=\beta=2,\qquad d=4.        \tag{9}
\]

In particular \(g\) is constant: otherwise the primitive quotient would
have degree \(d<4\), contradicting (9).  This proves Theorem 1.1.

## 5. Why the new frontier is still nonempty

The splitting type in (2) exists abstractly.  For example, in a dual
basis put

\[
 \lambda(t)=(1,t,t^2,0,0,0),\qquad
 \mu(t)=(0,0,0,1,t,t^2).                                  \tag{10}
\]

Their wedge has Pluecker degree four and is everywhere nonzero; its Hodge
dual is an everywhere decomposable \(\bigwedge^4\)-valued quartic with
annihilator splitting \((2,2)\).  This example is not asserted to equal
the particular derivative wedge in (1), and it is not a formal tensor
countermodel.  It shows why (2) is a frontier rather than a contradiction.

The next exact target is to combine (3) with the ten simple Hermite roots.
At each \(t=a_\nu^2\), the limiting four-plane contains the signed
three-jet span and its first transverse derivative.  Translating that
incidence into the six coefficient covectors in (3) is the smallest
remaining algebraic problem on the \(3^{10}\) core.

## 6. Exact arithmetic audit

[verify_live_three_zero_higher_split_p28_all_triple_residual_quartic_balanced_splitting.py](../computations/verify_live_three_zero_higher_split_p28_all_triple_residual_quartic_balanced_splitting.py)
checks the complete splitting ledger, the differentiation identity that
excludes degrees zero and one, and a full-rank decomposable
\((2,2)\)-quartic model.

The
[independent audit](live-three-zero-higher-split-p28-all-triple-residual-quartic-balanced-splitting-independent-audit.md)
checks finite gcd removal, the infinity fiber, the determinant-degree
identity, existence of the polynomial minimal row, and the degree-one
differentiation obstruction without importing the primary checker.
