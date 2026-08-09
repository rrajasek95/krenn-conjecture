# N=8 P5 generic-L lift and H0 degree nine

## Result

The dense $L=0$ component of P5 has no H0 survivor through degree nine.
After retaining the first two free $z_{46}$ bends symbolically, the mixed
strict-transform equations lift on the chart

$$
z_{16}z_{41}z_{11}(z_{44}+z_{45})\ne0.
$$

Both the degree-eight and degree-nine component-local H0 coefficients belong
to the exact lifted compatibility ideal.  This resolves the generic-$L$ gap
left by the earlier one-point calculation.  It remains a finite-order
formal-local result, not an all-orders membership theorem.

The exact checker is
`computations/verify_n8_p5_generic_L_h0_degree9.py`.
Its frozen ledger has SHA-256
`736ee026e09a4ae5497d27d3affe757f77fa96ff810b9fb7d7e3a89ab08e63c1`.

## Symbolic bends

Write

$$
s=z_{46}^{(1)},\qquad t=z_{46}^{(2)},\qquad
L=z_9z_{25}-z_{11}z_{46},\qquad b=z_{44}+z_{45}.
$$

The checker recomputes the full streamed degree-eight mixed tails and solves
the eleven $b$-diagonal transverse pivots through strict order five.  On
$L=0$, strict order five has only Q30 and Q33 nonzero.  They factor as

$$
\frac12 z_{16}^2z_{41}uF,
\qquad
\frac12 z_{16}^2z_{41}vF,
$$

where $u=z_{26}+z_{45}$, $v=z_{26}-z_{44}$, $u-v=b$, and

$$
F=-z_9z_{29}z_{44}+z_0z_{11}z_{46}
-z_{11}z_{24}z_{46}+z_{11}z_{26}z_{54}+sz_{11}.
$$

Thus $F=0$ is the unique first-bend relation on the localized dense chart.
The two order-five remainders have ten terms each; $F$ has five terms and
SHA-256
`33dbb3d1710cf5d538248c90f1912089b1ae592ad08f674ae9d400ef0c33f4f1`.

## Strict order six

The cross-multiplied strict-order-six compatibility has sixteen nonzero rows
before reduction.  Fourteen are consequences of $L$ and $F$.  After removing
the open factors $z_{16}^2z_{41}b/2$, Q30 and Q33 give two linear
second-bend polynomials with respectively 109 and 98 terms.

In the localization at $b$, their difference divided by $b$ is a single
second-bend relation.  A bend-first exact Groebner calculation verifies that
both original Q30/Q33 polynomials reduce by this one relation.  Its leading
$t$ coefficient is a unit after also localizing at $z_{11}$, so the two bend
relations describe a genuine graph over the dense $L$ chart rather than a
special base sublocus.  The localized ideal is nonunit, and every original
order-five and order-six compatibility remainder reduces to zero in it.

## H0 membership

With the symbolic corrections $s$ and $t$ installed, the canonical
$L$-remainders of the component-local H0 coefficients have:

- degree eight: 20 terms, SHA-256
  `02ad3eaa8ea0d35ecc91c24176ece35c82e2977c619c13f8cef53ffd682efcdf`;
- degree nine: 196 terms, SHA-256
  `5280df44bf147322282b1e9b12782cf2bf275bcd8e25a36ac900c7fa32f2b3c7`.

Both reduce exactly to zero modulo

$$
(L,F,b^{-1}(R_{30}-R_{33}))
$$

with inverse equations for $z_{11}$ and $b$.  Therefore the zero previously
seen at the twice-bent rational point is the generic localized identity, not
an accidental specialization.

## Scope and next frontier

Together with the coordinate-component calculation, all three P5
degree-six components now have no H1 witness through degree eight and no H0
witness through degree nine on their checked liftable charts.  The next P5
pure question needs the third normal-graph coefficient and the strict
order-seven mixed compatibility.  No all-orders conclusion, global ideal
membership, or counterexample is claimed here.

Run the checker with Python 3.13 or 3.14; it invokes Singular 4.4.1 for the
final localized standard-basis membership test.
