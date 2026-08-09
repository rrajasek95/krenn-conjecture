# P5 generic-L three-step bend recurrence through W5

The next exact selected compatibility equation repeats the symmetric
three-step recurrence visible in the first-colon equation.  This is now
verified by a streamed triangular quotient rather than a capped global
Groebner reduction.

## Exact triangular quotient

After the 207-row Schur graph, the localized centre equations are successively
affine and monic in

```text
z46, s, t, r3, r4.
```

Their coefficients are inverted using only `z11*w=1` and `b*q=1`.  The
checker solves `L,F1,F2,G,W4` in that order and substitutes the solutions
directly.  This is exact normal-form computation in the localized triangular
quotient; it does not specialize a parameter or use floating/modular
arithmetic.

For

```text
e1 = z0+z30+z52,
e2 = z0*z30+z0*z52+z30*z52,
e3 = z0*z30*z52,
```

the two consecutive selected equations are

```text
W4 = r4 + e1*r3 + e2*t  + e3*s,
W5 = r5 + e1*r4 + e2*r3 + e3*t.
```

The full 276,850-term Q8 compatibility family gives the exact localized
factorizations

```text
Q8_M30 = (1/2)*z11*z16^2*z41*(z26+b-z44)*W5,
Q8_M33 = (1/2)*z11*z16^2*z41*(z26-z44)*W5
```

modulo `L,F1,F2,G,W4`.  Both remainders are zero.  The streamed M30
difference shrinks through the five substitutions as

```text
39220, 19654, 7345, 2321, 556, 0 terms,
```

and M33 as

```text
21301, 10409, 3860, 1252, 324, 0 terms.
```

## Interpretation and remaining theorem

Together with the all-order newest-bend coefficient theorem, this identifies
two consecutive coefficients of the proposed transfer law

```text
(1+z0*T)*(1+z30*T)*(1+z52*T)*R(T).
```

It strongly suggests the fixed Cayley--Hamilton recurrence

```text
r_k + e1*r_(k-1) + e2*r_(k-2) + e3*r_(k-3) = 0
```

for every later bend.  The present calculation proves the `W4` and `W5`
instances only.  An all-order result still requires deriving the finite
post-Schur transfer function (the three linear propagation channels) from
the source equations.  Brute-force construction of W6 would be another
positive prefix, not that theorem.

The exact checker is
`computations/verify_n8_p5_generic_L_three_step_bend_recurrence.py`.  Its
frozen ledger has SHA-256
`6070cd95bdaa51bc6610df37a4f6748a8e98c63f21e20412152c0f7e4856b0ac`.
