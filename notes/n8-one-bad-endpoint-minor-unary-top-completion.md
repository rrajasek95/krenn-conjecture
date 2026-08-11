# The first unary-top completion kills the cofactor-invisible guard

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py`

## Exact bounded verdict

Start with the literal `fb8d482` four-response packet and add the minimum
possible common-`q` support capable of producing the missing unary target
`q^[3]=X0`.  Such an additive completion consists of three new `00`
decorated cells on one perfect matching of the six residual sites.  The
checker expands all `15` possibilities symbolically, with arbitrary nonzero
coefficients.

Exactly one matching produces no mixed unary-top word:

```text
03:00, 12:00, 45:00.
```

All other `14` supports have between one and three single-monomial mixed top
coefficients, so none can cancel at this support size.  The mixed-word-count
histogram is `0:1, 1:8, 2:2, 3:4`.

## The four responses cannot survive

Let the old `11` cells on `24,35` have weights `A,B`, the old `22` cells on
`05,14` have weights `C,D`, and the three new zero cells have weights
`u,v,w` in the displayed order.  Write the five star weights as
`p0,p5,p2,s1,s2`.  The two diagonal responses and unary top require

```text
A*B*p0*s1 = 1,      C*D*p2*s2 = 1,      u*v*w = 1.
```

Thus every factor except the optional `p5` is a unit.  On the unique clean
top support, literal matching expansion gives three new response terms:

```text
11 @ 011011 : A*p5*s1*u,
12 @ 100200 : p0*s2*v*w,
21 @ 012000 : p2*s1*u*w.
```

The first equation forces `p5=0`: the component which was invisible in
`fb8d482` becomes response-visible and is genuinely removable.  The two
crossed terms do not use `p5`; both are products of units and therefore
cannot vanish.  Hence there is no exact full-source guard on this first
top-compatible support.

The endpoint-minor alternative does not intervene.  Before deleting `p5`,
all six orientations of the three old nonzero minors still have zero
compatible cofactor.  After deletion, all four orientations of the two
remaining minors are likewise invisible.  The contradiction is already in
the two literal crossed-response rows, not an alternating-`C4` activation.

## Scope

This is the complete minimal **additive** unary completion of the pinned
four `q` cells, with exactly three new `00` cells and the pinned star support.
It allows arbitrary nonzero coefficients and therefore is not a unit-weight
specialization.  It does not classify a simultaneous enlargement by new
endpoint-star cells or a larger common-`q` support.  Those are the next
possible completion layers; no claim about them is made here.
