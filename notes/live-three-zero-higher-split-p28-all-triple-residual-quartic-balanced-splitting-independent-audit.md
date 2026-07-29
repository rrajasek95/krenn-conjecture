# Independent audit: balanced splitting of the all-triple residual quartic

## 1. Verdict and exact scope

I independently reconstructed
[the balanced-splitting corollary](live-three-zero-higher-split-p28-all-triple-residual-quartic-balanced-splitting.md).
It is sound:

\[
 \boxed{\deg\phi=4,\qquad
 {\cal A}\simeq{\cal O}_{\mathbb P^1}(-2)
                 \oplus{\cal O}_{\mathbb P^1}(-2).}          \tag{A1}
\]

Here \(\phi:\mathbb P^1\to\operatorname {Gr}(4,6)\) is the primitive
projective curve represented by the residual four-vector, and
\({\cal A}\) is its rank-two annihilator bundle.  The finite gcd,
possible infinity basepoint, determinant-degree identity, polynomial
minimal row, and differentiation step all survive audit.

This result is not a profile closure.  It replaces an arbitrary
degree-at-most-four decomposable residual by a basepoint-free balanced
quadratic annihilator pair.

## 2. Scalar division really gives a Grassmannian morphism

Let \(Q(t)\ne0\) be the polynomial four-vector from the audited
residual-quartic frontier.  Its Pluecker relations are polynomial
identities: they hold wherever \(Q(t)\ne0\), hence everywhere.  If
\(g(t)\) is the gcd of its coordinates and
\(\widetilde Q=Q/g\), then every quadratic Pluecker relation satisfies

\[
                  g(t)^2R(\widetilde Q(t))=R(Q(t))=0.
\]

The polynomial ring is a domain, so \(R(\widetilde Q)=0\).  Thus scalar
division preserves decomposability even at a formerly common zero.

The coordinates of \(\widetilde Q\) have no common finite zero.  Let
\(d\) be their actual maximum affine degree and homogenize every
coordinate to degree \(d\).  At least one coordinate has a nonzero
leading coefficient, so the homogenized vector does not vanish at
infinity.  It is therefore basepoint-free on the whole projective line
and defines

\[
                 \phi:\mathbb P^1\longrightarrow
                       \operatorname {Gr}(4,6),\qquad d\leq4. \tag{A2}
\]

This use of the actual maximum degree is essential: homogenizing
artificially to degree four before removing an infinity factor would
not compute the projective degree.

On the dense set where the derivative wedge is nonzero, its represented
plane is

\[
             W_t=\langle E(t),O(t),E'(t),O'(t)\rangle.       \tag{A3}
\]

The morphism supplies the limiting four-plane at exceptional points.
Only the generic identity (A3) is used in the annihilator argument, so
no equality with a rank-deficient displayed span is assumed at a root.

## 3. The determinant of the annihilator has degree \(d\)

Let \({\cal S}\) be the pulled-back tautological four-plane bundle and
let

\[
 0\longrightarrow{\cal A}\longrightarrow
   (\mathbb C^6)^*\otimes{\cal O}
   \longrightarrow{\cal S}^*\longrightarrow0               \tag{A4}
\]

define the annihilator.  Under the Pluecker embedding,

\[
                         \det{\cal S}={\cal O}(-d).
\]

Taking determinants in (A4) gives

\[
                         \det{\cal A}={\cal O}(-d).           \tag{A5}
\]

Birkhoff--Grothendieck therefore gives

\[
 {\cal A}\simeq{\cal O}(-\alpha)\oplus{\cal O}(-\beta),
 \quad0\leq\alpha\leq\beta,\quad\alpha+\beta=d.              \tag{A6}
\]

The nonnegativity follows because \({\cal A}\) is a subbundle of a
trivial bundle.  Equivalently, homogeneous rows representing the two
summands have degrees \(\alpha,\beta\); their two-by-two minors have
degree \(\alpha+\beta\).  They have no common projective zero, because
such a zero would make the inclusion (A4) drop fiber rank.  Hence no
unrecorded Pluecker gcd changes (A6).

## 4. A smallest summand gives a polynomial annihilator

The composite

\[
 {\cal O}(-\alpha)\longrightarrow{\cal A}
       \longrightarrow(\mathbb C^6)^*\otimes{\cal O}
\]

is represented by six homogeneous forms of degree \(\alpha\), with no
common projective zero.  On the affine chart it is a nonzero polynomial
covector

\[
                         \rho(t)\in(\mathbb C^6)^*[t],
                         \qquad\deg\rho\leq\alpha.            \tag{A7}
\]

It annihilates \(W_t\) for every regular fiber.  Using (A3) on a dense
set and polynomial continuation gives the four identities

\[
                  \rho E=\rho O=\rho E'=\rho O'=0.           \tag{A8}
\]

This establishes the needed polynomial minimal row directly from the
line summand; no choice of a rational frame or denominator clearing is
being hidden.

If \(\alpha=0\), then \(\rho\) is a nonzero constant covector and

\[
                       \rho F(z)=\rho E(z^2)+z\rho O(z^2)=0
\]

is a constant linear relation among the six basis polynomials of
\({\cal K}\), impossible.

If \(\alpha=1\), write \(\rho(t)=\rho_0+t\rho_1\).
Differentiating the first two equations in (A8) and subtracting the
last two gives

\[
                           \rho_1E=\rho_1O=0.                 \tag{A9}
\]

If \(\rho_1\ne0\), it is again a forbidden constant relation on \(F\).
If \(\rho_1=0\), then \(\rho=\rho_0\ne0\) already gives that relation.
In homogeneous language, a nominal degree-one row with
\(\rho_1=0\) would also vanish at the infinity fiber, so it could not
by itself represent a subbundle summand; the affine contradiction is
already sufficient.

Therefore \(\alpha\geq2\).  Combining this with
\(\alpha\leq\beta\) and \(\alpha+\beta=d\leq4\) leaves only

\[
                         d=4,\qquad\alpha=\beta=2.            \tag{A10}
\]

Finally, if the original coordinates of \(Q\), all of degree at most
four, had a finite gcd of positive degree \(r\), their primitive
quotient would have actual degree at most \(4-r<4\).  Equation (A10)
therefore forces \(r=0\).  It also rules out a degree drop at infinity.
This proves (A1) and the claimed primitivity of the original residual
quartic.

## 5. The balanced frontier is nonempty

The displayed model

\[
 \lambda=(1,t,t^2,0,0,0),\qquad
 \mu=(0,0,0,1,t,t^2)
\]

homogenizes to

\[
 \lambda_h=(s^2,su,u^2,0,0,0),\qquad
 \mu_h=(0,0,0,s^2,su,u^2).
\]

These rows have rank two at every finite point and at infinity
\([s:u]=[0:1]\).  Their minors have gcd one and actual degree four, so
their common kernel supplies a genuine \((2,2)\) Grassmannian quartic.
It confirms the stated scope: balanced splitting alone is not a
contradiction and is not a tensor countermodel.

## 6. Independent executable verification

[verify_live_three_zero_higher_split_p28_all_triple_residual_quartic_balanced_splitting_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_all_triple_residual_quartic_balanced_splitting_independent_audit.py)
imports none of the primary checker.  It verifies finite gcd division,
the actual-degree infinity chart, the determinant-degree ledger, the
homogeneous-to-affine minimal row, the degree-one differentiation
identity, and fiberwise rank of the balanced model including infinity.
