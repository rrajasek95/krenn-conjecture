# Rep2 group16 67-variable timeout: exact design-only reduction

Verdict: **PASS design only / no closure / no retry**.  The consumed
`V(A67,A12) intersect D(b0)` chart is bound to exact-Q source
`2403105f...` and terminal referee `d0f48380...` (native wall 240 s,
4,790,022,144-byte peak, zero mathematical coverage).  No Singular process
was launched here.

## Exact census and obstruction

The ideal has 67 variables, 6,561 literal amplitude equations (`3^8` color
words), 12 guards, and one saturation equation.  Exact sparse expansion gives
250,098 amplitude terms and 215,640 distinct monomials overall.  Every one of
the 67 coordinates occurs in an amplitude equation; there is no
amplitude-inactive matrix or coordinate and no monic graph generator in the
unlocalized 6,574-generator ideal.

The exact Q ranks are:

* amplitude coefficient span: **6,561**;
* generator/variable support incidence: **47**;
* monomial/exponent incidence: **67**;
* affine-linear coefficient part: **19**.

The first rank reaches the number of amplitude rows (also independently
witnessed modulo 1,000,003 and 1,000,033), so there is **zero constant-linear
redundancy among the 6,561 word equations**.  Consequently no literal subset
is claimed sufficient for the unit ideal.  Ideal-theoretic redundancy would
need an actual membership/unit certificate, which the timed-out lane did not
produce.  The full coefficient rank and full exponent-incidence rank also rule
out a sound coordinate-disjoint tensor/product split visible at literal level.

## Reversible guard factorization

For rows `r=1,2`, define

```
H_r=(-xn2*a57_01+a57_02)*a57_r0
    +(-xn0*a57_02+xn2)*a57_r1
    +(xn0*a57_01-1)*a57_r2.
```

Exact sparse identities verify the six first guards as

```
g0_r = a57_01*a57_r0-a57_r1+t0*H_r,
g1_r = t1*H_r,
g2_r = t2*H_r.
```

Writing `d=xn0*a57_01-1` and
`b0=a26_00+a26_01*a57_01+a26_02*a57_02`, the existing equation
`d*b0*sat-1=0` makes both `d` and `b0` units.  This produces the exhaustive,
disjoint cover

```
D(t1), V(t1)D(t2), V(t1,t2)D(t0), V(t0,t1,t2).
```

On either first open stratum, `H_r=0`, then `g0_r=0`, and the unit `d`
give the four graph substitutions
`a57_r1=a57_01*a57_r0`, `a57_r2=a57_02*a57_r0`.
On `V(t1,t2)D(t0)`, `t0` and `d` solve monically for `a57_12,a57_22`;
the recorded formula uses `it0=t0^-1` and `b0*sat=d^-1`.  On the closed
stratum, the two surviving `g0` equations graph-eliminate
`a57_11,a57_21` directly.

The four materialized exact-Q design sources have respectively
**64/6,569**, **63/6,569**, **64/6,569**, and **62/6,568**
variables/generators.  They contain only ideal declarations and census prints,
not a Groebner call.  The 64-variable `D(t0)` source is intentionally large
because its inverse substitution is fully expanded; it is an auditable
reference, not a performance claim.  The canonical expanded parent is likewise
byte-larger and explicitly not recommended as a runtime input.

## Scope

This cover is reversible and exhaustive for the one selected 67-variable
chart only.  It neither closes group16 nor proves any stratum unit, gives no
minimal unit subset, and authorizes no modular/exact-Q retry.  A future solve
would have to discharge every one of the four strata independently.
