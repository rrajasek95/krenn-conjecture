# N=8 P5 component-local next pure coefficients

## Result

The P5 pure membership calculation advances one further order on both
symbolic coordinate components and at the exact twice-bent point of the
$L=0$ component certified by the degree-eight mixed checker:

- H1 at degree eight vanishes symbolically on all three degree-six
  components;
- H0 at degree nine vanishes symbolically on $z_{16}=0$ and $z_{41}=0$;
- H0 at degree nine also evaluates to zero at the certified rational $L$
  point after both required free bends.

No new pure survivor is certified.  The H0 statement on $L=0$ is still a
one-point result, not a symbolic identity on the generic component.

The exact checker is
`computations/verify_n8_p5_component_local_next_pure.py`.  Its ledger has
SHA-256
`923aa11aeedcb2d89bd9a6777812f4f6106d63b79d3d56a2de7186bf7fd0552c`.

## Why a component-local calculation works

The global degree-seven tangent standard basis is not yet available.  That
does not prevent evaluation on the already certified mixed Hensel branches.
After the lower pure corrections are installed, every remaining correction
is a multiple of a mixed equation and therefore vanishes along such a
branch.  The checker pulls the factorized pure residual back to the same
bigraded jet used for the degree-eight mixed calculation:

- ambient normal-graph order through two;
- strict P5 arc order through two.

It first requires the previously certified H1 degree-seven coefficient to be
zero.  The following coefficient is then the sum of the degree-six
strict-order-two, degree-seven strict-order-one, and degree-eight base terms.
For H0, the analogous next coefficient combines residual degrees seven,
eight, and nine after retaining all 105 degree-seven obstruction quotients.
The eight-term H0 remainder itself is not discarded; its value and strict
derivatives are evaluated on the component arcs.

## H1 degree eight

The degree-six H1 tangent residual has 573 terms and is removed by 426
quadratic-obstruction quotients.  The next component-local polynomial has the
exact factorization

$$
H1^{(8)}=
2z_4z_{16}^2z_{41}^2(z_{44}+z_{45})
(z_9z_{25}-z_{11}z_{46}).
$$

Thus it has four expanded terms and vanishes on

$$
z_{16}=0,\qquad z_{41}=0,\qquad L=0.
$$

Its SHA-256 is
`74c1b3a29d77292d38c25d539352519c32b78f2175c6d4f51010948cecd338fd`.
When the two free $z_{46}$ bends are included explicitly, the corresponding
618-term expression evaluates exactly to zero at the certified rational
$L$ point.

## H0 degree nine

The degree-seven H0 tangent residual has 134 terms.  Its quadratic reduction
has 105 quotients and the previously certified eight-term remainder.  After
retaining those quotients, the raw degree-eight component-local expression
has 80 terms.  The next degree-nine expression has 424 terms and SHA-256
`c5c43bc8e8cf27bf8560b3623770a811c1ffb106ab619bb37a54df25032f0399`.

Exact restriction gives

$$
H0^{(9)}|_{z_{16}=0}=0,
\qquad
H0^{(9)}|_{z_{41}=0}=0.
$$

The unreduced symbolic polynomial is not an $L$ multiple, so the checker does
not claim generic $L$ vanishing.  Instead it rebuilds the exact point with

$$
z_{46}^{(1)}=\frac{2430}{13},
\qquad
z_{46}^{(2)}=\frac{317140}{13},
$$

recomputes the local pure jet, and verifies that both its degree-eight and
degree-nine values are zero.  The degree-nine point expression has 1,095
terms and SHA-256
`2dca8fdedf5c85086b4f4023f79cb7522b72ecf91ec638130c73155520fe12a2`.

## Consequence and frontier

The two symbolic coordinate components now have no H1 witness through degree
eight and no H0 witness through degree nine.  The known rational $L$ lift has
neither witness at the same orders.  This is positive evidence for local
membership, but it is finite-order evidence only.

The most useful next step is to symbolize the twice-bent generic $L$
component.  That would decide whether the H0 degree-nine zero seen at the
rational point is an identity or a special sublocus.  In parallel, a later
pure survivor on $z_{16}$ or $z_{41}$ would require the third normal-graph
coefficient and the next mixed compatibility order.
