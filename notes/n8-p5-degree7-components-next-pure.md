# N=8 P5 degree-seven components and next pure reductions

## Corrected result

The three degree-six P5 components all admit the next mixed finite-jet lift
on the chart

$$
b=z_{44}+z_{45}\ne0.
$$

After a cache-safety correction, the next pure calculation advances local
membership rather than exposing a new class:

- the H1 normal form at original degree seven is identically zero;
- the H0 normal form at original degree eight has 56 terms and factors as
  $z_{16}^2z_{41}L$ times a 28-term polynomial, where
  $L=z_9z_{25}-z_{11}z_{46}$.

Consequently H0 also vanishes on each of the three degree-six components
$z_{16}=0$, $z_{41}=0$, and $L=0$.  In particular, the generic $L=0$
component does **not** currently carry the previously reported H0/H1 pure
witnesses.

The exact checker is
`computations/verify_n8_p5_degree7_components_next_pure.py`; its streamed
compatibility helper is
`computations/analyze_n8_p5_degree7_compatibility_tails.py`.

This remains a finite filtered, formal-local statement on the P5 $b$-chart.
It is not an all-orders standard-basis computation or a global proof.

## Regression correction

The original version cached P5 restrictions and weighted derivatives under
the bare integer `id(source)` of a polynomial dictionary.  Some obstruction
multipliers are short-lived dictionaries.  CPython 3.13 reused their object
identities during the same projection, so the cache returned restrictions of
earlier, unrelated polynomials.  The erroneous output depended on allocator
behavior: it produced a 201-term H1 form and a 268-term H0 form under one
interpreter run, while clean Python 3.13 runs produced other inconsistent
forms.

The cache now retains a strong reference to every source together with its
result and checks object identity on every hit.  An identity therefore cannot
be recycled while its entry is live.  Python 3.13 and 3.14 then agree on the
corrected exact polynomials and component restrictions.  The earlier pure
hashes and the claim that generic $L=0$ was a construction lane are withdrawn.

## Degree-seven compatibility tails

Starting from the committed 39 degree-seven mixed tails, the checker solves
the eleven $b$-diagonal pivots through strict order four and projects strict
order five to the 28 compatibility directions.  Exactly 16 normalized
compatibilities remain, in equations

$$
1,4,10,11,14,16,22,25,26,28,30,31,33,36,37,38.
$$

All 16 contain the common factor $z_{16}^2z_{41}$.  Fourteen also contain
$L$.  Only $h_{30}$ and $h_{33}$ are exceptional.  With

$$
u=z_{26}+z_{45},\qquad v=z_{26}-z_{44},
$$

exact polynomial division gives

$$
v h_{30}-u h_{33}\in(L).
$$

The quotient has 16 terms.  On $L=0$, the old degree-six compatibility pair
is proportional to $(u,v)$ under a bend transverse to $L$.  Since $u-v=b$ is
a unit on this chart, this relation is exactly the consistency condition for
one free bend to solve both exceptional tails.  Thus $z_{16}=0$, $z_{41}=0$,
and $L=0$ all persist through mixed degree seven.

The 16 normalized compatibility polynomials retain SHA-256
`c29ec3c357a4982003b998261128bf7da3b1c8ac5578c2e734ac7b687fdd3b0e`.

## Corrected next pure normal forms

For H1, the degree-six tangent residual has 573 terms and divides by the
quadratic obstructions with 426 quotients and zero remainder.  The exact
degree-seven continuation combines:

- 14,208 old degree-seven terms;
- 14,213 weighted derivative terms;
- a 277-term obstruction tail;
- a 406-term weighted obstruction derivative.

These cancel identically.  The empty polynomial has SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

For H0, the checker first reproduces the exact eight-term degree-seven class.
It then streams the degree-eight continuation and incorporates the lifted
tail of the compatibility identity that killed that class,

$$
2(z_{53}-z_{51})(h_{30}-h_{33}).
$$

Before this compatibility tail the corrected next form has 80 terms.  The
tail has 98 terms, and cancellation leaves 56 terms.  Exact division verifies

$$
H0^{(8)}\in(z_{16}^2z_{41}L).
$$

Its SHA-256 is
`2bc2656e3a30d11acbc42c63165a227df03b2c72c8a5ca5fe4186f312d8fdf34`.
The 28-term factor quotient has SHA-256
`47cdc891c6df189a947a1d40bb58a5d3fb66d9be8eb03fd7c99c32696ccfa1b5`.

The corrected full regression ledger has SHA-256
`a5881582d5f8a581596f370d1526da6cf7c64b4fa2b6d9d37f2fbd6844397854`.

## Consequence and next frontier

No checked P5 component supplies a new pure witness at these orders.  For a
counterexample construction, one must continue the mixed recursion until a
later H0 or H1 coefficient survives on an indefinitely liftable component,
or move to another branch.  For a local membership proof, this result is
positive evidence: H1 membership advances through degree seven and H0
vanishes through degree eight after imposing the next component relations.

The next exact P5 calculation is the following mixed compatibility order on
these components, followed by the next nonzero filtered H0/H1 normal forms.
