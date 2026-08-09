# P5 full-germ rational-point Weierstrass initial

The finite full first-Rees equations can now be specialized at an exact point
of the dense generic-`L` center while retaining the third bend.  The bounded
exporter/checker is
`computations/analyze_n8_p5_full_point_weierstrass.py`.

The point is

```text
z46 = 297/13,  s = 2430/13,  t = 317140/13,
r0 = 6630040/13.
```

All other 44 free P5 coordinates take the deterministic values `zi=i+2`.
The localizers `b,z11,z16,z41` are nonzero.  Substitution of

```text
z46(tau)=z46+tau*s+tau^2*t+tau^3*r3
```

reduces the full input to a 12,896,151-byte characteristic-zero Singular
file (SHA-256
`55a2912b8800d0b3b426dd5f55a7c394b5120e10b81e745883d03067eb370e09`).
It contains 294,688 terms in the 196 normal rows, 34,516 in the eleven
transverse pivots, 49,365 in the 28 remaining mixed rows, and 3,264 in the
two pure rows.

The full source rows, before point evaluation, have degree at most one in
`z46`: the maxima for `(N,P,M,H)` are `(1,0,1,0)`.  Consequently every
point-arc row is affine in `r3`; this is an exact source-multiaffinity check,
not an inference from the evaluated coefficients.

Singular computes the selected 207-row standard basis immediately.  After
adjoining the full row `M30`, it computes a 209-row (not minimized) standard
basis in about twelve seconds.  Exactly one lead has degree greater than one:

```text
154714580602170274968750000000 * tau^6 * r3.
```

This is the exact full-germ counterpart of the source-certified monic `G`
initial.  After shifting `r3=r0+rho`, its sixth saturated initial is a unit
times `rho`.  Thus the associated sixth strict transform has the expected
Weierstrass pivot.

The result stops at the associated/saturated initial.  The raw standard-basis
row still contains lower terms reducible by the 207-row block and is not
itself exactly divisible by `tau^6`; computing its corrected normal form did
not finish in two minutes.  Direct full normal forms of `M1`, `M30`, and the
two pure rows were likewise capped, and imply no membership result.  The
other 27 mixed germs and `H0,H1` therefore remain outside the certified
scope.

Finally, P5 is a Ferrers component of the tangent-cone deformation used in
the ambient local matching model.  No checked coordinate map in this lane
identifies it with the separately normalized anchor `chart26`.  This result
must not be cited as closure of chart26.

Reproduce the bounded exact stage with

```sh
.venv/bin/python computations/analyze_n8_p5_full_point_weierstrass.py \
  /tmp/n8-p5-full-point.sing --run-singular
```
