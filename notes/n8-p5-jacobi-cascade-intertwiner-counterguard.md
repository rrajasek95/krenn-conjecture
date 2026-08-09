# P5 Jacobi cascade: naive 3-state intertwiner counterguard

The first small Schur-coordinate cascade behind the newest-bend response is
now identified exactly.  It is **not** itself the three-state transfer which
produces the `W4/W5` recurrence: the two systems have generically disjoint
spectra.  Any successful transfer proof must include the new relative-order
three states and the localized center/output projection.

## Exact cascade blocks

Differentiate the exact 207-row graph with respect to the retained marker
`r4=z46^(4)`.  At relative orders one through three, the pivots

```text
y110, y113, y116
```

have respective amplitudes `A=z16*z25`, `z16*z26`, `z16*z27` times

```text
1,
-(z10+z37),
z10^2+z10*z37+z37^2.
```

Thus they are the initial coefficients of

```text
A / ((1+z10*T)*(1+z37*T))
```

and obey the exact two-state recurrence with roots `-z10,-z37`.

The pivots

```text
y155, y158, y161, y191, y197
```

have an initial amplitude followed by multiplication by `z40` at each of
the next two orders.  This supplies a one-state geometric channel with root
`z40`.  Together the evident `2+1` block has characteristic polynomial

```text
(lambda+z10)*(lambda+z37)*(lambda-z40).
```

## Exact obstruction to the direct intertwiner

The companion matrix suggested by the selected bend equations has
characteristic polynomial

```text
(lambda+z0)*(lambda+z30)*(lambda+z52).
```

Over the P5 rational function field, the Sylvester resultant of these two
cubics is the nonzero product

```text
(z0-z10)(z30-z10)(z52-z10)
(z0-z37)(z30-z37)(z52-z37)
(z40+z0)(z40+z30)(z40+z52).
```

Therefore the Sylvester equation `P*A=C*P` has only `P=0` for this naive
three-state raw block.  In particular it cannot be the desired transfer
under any invertible change of coordinates.  This is a counterguard to the
smallest proposed intertwiner, not to the all-order recurrence itself.

At relative order three, fourteen additional Schur coordinates turn on.
Those states, together with reduction by `L,F1,F2,G` and the selected output
functional, are the smallest remaining candidate for a nontrivial
intertwiner.  Alternatively one must prove the finite rational full-Rees
identity after clearing
`((1+z0*T)(1+z30*T)(1+z52*T))^4`.

The exact checker is
`computations/verify_n8_p5_jacobi_cascade_intertwiner_counterguard.py`.
Its frozen ledger SHA-256 is
`3577137dd710dfd15274c435c52be7b1ac207028b4847cb246a65b06e68135c4`.
