# The arbitrary-pure chart is formally rigid against positive-order mixed q

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_endpoint_minor_mixed_rees_first_order.py`

## Exact verdict

Around the arbitrary pure-zero completion of `260bb94`, adjoin with one
common filtration parameter `tau`

```text
90 off-diagonal decorated residual q cells,
72 arbitrary corrections to the four endpoint-star rows,
4 binary direct-edge corrections.
```

The checker expands `q^[3]` and all four response tensors exactly modulo
`tau^2`.  The first nonzero associated-graded crossed equations occur at
degree **zero**, before any new direction is visible:

```text
12 @ 100200 : p0*s2*(z12*z45 + z14*z25 + z15*z24),
21 @ 012000 : p2*s1*(z03*z45 + z04*z35 + z05*z34).
```

The exact pure-chart ideal certificate from `260bb94` reduces these to

```text
p0*s2*z12*z45,       p2*s1*z03*z45,
```

while `z03*z12*z45=1`.  The four star factors are units by the two diagonal
response anchors.  Both initial forms are therefore units in the localized
degree-zero quotient.

It follows immediately, in the complete Rees ring, that each corresponding
crossed response germ is a unit series.  No correction with positive
`tau`-valuation can cancel it.  This remains true after allowing every
source-valid endpoint-star and binary direct correction.

The explicit order-one expansion gives a useful provenance refinement:
none of the `90` mixed-q directions enters either selected pure-residual
crossed word at first order.  Endpoint corrections do enter at order one,
but cannot change a unit constant coefficient.

## Scope

This proves formal rigidity of the pinned arbitrary-pure chart against all
off-diagonal mixed-q deformations with positive common valuation.  It does
not cover new same-colour `11/22` q directions at degree zero, a chart in
which mixed cells themselves have valuation zero, negative valuations, or a
reselection of the endpoint stars.  Any genuine mixed completion must leave
this formal chart rather than deform it.
