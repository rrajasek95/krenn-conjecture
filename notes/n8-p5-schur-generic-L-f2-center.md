# P5 finite-Schur recovery of the generic-L second center

The finite first-Rees equations and the exact 207-row Schur graph recover the
second bend relation on the dense `L` component without importing any capped
or modular normal form.  The exact checker is
`computations/verify_n8_p5_schur_generic_L_f2_center.py`.

Start with

```text
L = z9*z25-z11*z46,
z46(tau) = z46 + tau*s + tau^2*t,
F1 = -z9*z29*z44 + z0*z11*z46 - z11*z24*z46
     + z11*z26*z54 + s*z11.
```

The checker solves the 196 identity-leading normal rows through graph order
five.  It does not divide the eleven transverse equations by
`b=z44+z45`: instead it forms their exact Schur compatibility numerators

```text
b * incoming_i - sum_j J_ij * pivot_incoming_j.
```

After reduction modulo `L`, exactly rows
`1,4,10,11,14,16,22,25,26,28,30,31,33,36,37,38` remain.  Removing the
common `z16^2*z41` and the first exact `b` factor from rows 30 and 33 gives
`R30,R33`.  Their difference is a 116-term polynomial, affine in `t`, with
SHA-256

```text
df03271b1d00e39ed3ede0d75b7031bdc751595c44d04ee3ffcd81b34de48bf8.
```

We use `F2=R30-R33`.  The older normalization is `F2/b`; these generate the
same localized ideal because `b` is a unit on this chart.  An exact
characteristic-zero Singular reduction proves all sixteen compatibility
numerators lie in

```text
<L,F1,F2,z11*w-1,b*q-1,z16*p16-1,z41*p41-1>,
```

and separately checks that this ideal is not the unit ideal.  The frozen
ledger SHA-256 is
`8e79e129660da84d1e852e1141e2ef04528fb858047bd8b5cb4c601f43a7058f`.

This is a source-faithful certificate through `F2`.  It does not yet recover
the next monic `G` row, nor prove scalar or conormal membership of the full
pure germs `H0,H1`.
