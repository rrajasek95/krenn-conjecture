# N=8 P5 degree-seven components and next pure classes

## Result

The three degree-six P5 components all admit the next mixed finite-jet lift
on the chart

$$
b=z_{44}+z_{45}\ne0.
$$

They do not, however, advance pure membership uniformly.  A later pure class
survives generically on every component: H1 at original degree seven on
$z_{16}=0$, H0 at original degree eight on $z_{41}=0$, and both classes on
$L=z_9z_{25}-z_{11}z_{46}=0$.  For counterexample construction the last of
these is the promising outcome: the mixed equations lift while both missing
pure coefficients turn on.

The exact checker is
`computations/verify_n8_p5_degree7_components_next_pure.py`; its streamed
compatibility helper is
`computations/analyze_n8_p5_degree7_compatibility_tails.py`.

This is a finite filtered, formal-local statement on the P5 $b$-chart.  The
surviving polynomials can have further zero subloci, so this neither gives an
all-orders formal branch nor exhibits a counterexample.

## Degree-seven compatibility tails

Starting from the committed 39 degree-seven mixed tails, the checker solves
the eleven $b$-diagonal pivots through strict order four and projects strict
order five to the 28 compatibility directions.  Exactly 16 normalized
compatibilities remain, in equations

$$
1,4,10,11,14,16,22,25,26,28,30,31,33,36,37,38.
$$

All 16 contain the common factor $z_{16}^2z_{41}$.  Fourteen also contain

$$
L=z_9z_{25}-z_{11}z_{46}.
$$

Only $h_{30}$ and $h_{33}$ are exceptional.  With

$$
u=z_{26}+z_{45},\qquad v=z_{26}-z_{44},
$$

exact polynomial division gives

$$
v h_{30}-u h_{33}\in(L).
$$

The quotient has 16 terms.  On $L=0$, the old degree-six compatibility pair
is proportional to $(u,v)$ under a bend transverse to $L$.  Since $u-v=b$ is
a unit on this chart, the displayed relation is exactly the consistency
condition for the one free bend to solve both exceptional tails.  Thus:

- $z_{16}=0$ persists because all 16 tails have $z_{16}^2$;
- $z_{41}=0$ persists because all 16 tails have $z_{41}$;
- $L=0$ persists because the 14 ordinary tails vanish and the exceptional
  pair satisfies the single-bend relation.

The exact 39-polynomial mixed-tail input remains the previously frozen
degree-seven artifact.  The 16 normalized compatibility polynomials have
SHA-256
`c29ec3c357a4982003b998261128bf7da3b1c8ac5578c2e734ac7b687fdd3b0e`.

## Next pure normal forms

For H1, the degree-six tangent residual has 573 terms and divides by the
quadratic obstructions with 426 quotients and zero remainder.  The streamed
next-order formula combines 14,208 old degree-seven terms, 14,213 weighted
derivative terms, and a 72-term obstruction tail.  Cancellation leaves a
201-term polynomial.  It is divisible by $z_{41}$ but is nonzero modulo
$(z_{16})$ and modulo $(L)$.

For H0, the checker first reproduces the exact eight-term degree-seven class.
It then streams the degree-eight continuation and incorporates the lifted
tail of the compatibility identity that killed that class:

$$
2(z_{53}-z_{51})(h_{30}-h_{33}).
$$

Before this compatibility tail the next form has 275 terms; the tail has 98
terms, and cancellation leaves a 268-term polynomial.  It is divisible by
$z_{16}$ but is nonzero modulo $(z_{41})$ and modulo $(L)$.

The exact pure polynomial hashes are:

- H1 degree seven:
  `d659a2df5c91b7bde7b923f3e1f039cee7e8e35e665575075b7d70a6cbacf5c0`;
- H0 degree eight:
  `08ef1253ffa62448aa1b3c6fbe6c69ac4440c0b152f88935635c3dbfa0e0b716`.

The full regression ledger has SHA-256
`ebe384530dd3362b32f5719e573a4d95ef6b37aeb334bb7bd3af6aa5cfc5ac97`.

## Two interpretations and the next frontier

The P5 lane is no longer merely stalled at the killed eight-term H0 class:
the strict mixed recursion advances one order and exposes later pure
obstructions.  There are two distinct ways to use this result:

- For counterexample construction, one wants the mixed coefficients to keep
  vanishing while the missing pure coefficients are nonzero.  The generic
  $L=0$ component is therefore the leading P5 lane: both H1 at degree seven
  and H0 at degree eight are nonzero there.  Its next calculation is the
  generic-$L$ mixed strict transform at the following order.
- For a local ideal-membership or exclusion proof, these nonzero remainders
  are obstructions.  One would instead decompose their zero subloci and try
  to show that every indefinitely liftable mixed branch is forced into them
  and eventually makes the pure coefficients vanish.

The present finite-jet result chooses neither outcome: the generic $L=0$
branch must still satisfy every later mixed compatibility before it becomes
an all-orders formal counterexample.
