# P5 rational-Rees point export and weak-normal-form counterguard

## Exact finite export

At the committed exact generic-`L` point

```text
z46=297/13,  s=2430/13,  t=317140/13,  r3=6630040/13,
```

set

```text
P=(1+z0*tau)*(1+z30*tau)*(1+z52*tau),
R=N/P,
```

where the degree-at-most-three numerator `N` is chosen so that the first
four coefficients of `R` are `z46,s,t,r3`.  The new exporter
`computations/analyze_n8_p5_rational_rees_point_targets.py` substitutes
this fraction into the full source-faithful first-Rees equations while
retaining all 196 normal and eleven transverse Schur variables.

Every source row is affine in `z46`.  If it is `A*z46+B`, then

```text
P^4*F(N/P)=P^3*(A*N+B*P).
```

Since `P(0)=1`, cancelling `P^3` is exact in the completed local ring.  The
resulting finite point export has 207 implicit rows and 817,627 terms.  Its
family SHA-256 is
`95b37e6aa7d4323ac66fbc779a91d4ad1d0c37f19433a68c3524063e4945f734`.
The selected rational numerators have 5,949 terms for `M30`, 6,548 for
`M33`, 2,737 for `H0`, and 5,736 for `H1`.

The formal affine identity

```text
A*(C*N+D*P)-C*(A*N+B*P)=P*(A*D-C*B)
```

certifies cancellation of the rational bend numerator before any expansion.
The four source blocks `(A,B,C,D)` have respectively
`(381,2143,381,2408)` terms.  Expanding the raw Wronskian produces
1,857,174 terms; its direct exact reduction was capped after the 207-row
standard basis had completed, so it yields no membership result.

## Exact counterguard to quotient multiplication

In Singular's local order the 207 transformed rows again have a 207-row
standard basis.  Reducing the four blocks separately gives the one-term
weak remainders

```text
A ->  21762*tau,       B -> -497178*tau,
C ->  21762*tau,       D -> -497178*tau.
```

Multiplying these displayed weak remainders would falsely suggest a zero
Wronskian and a three-term representative for each selected mixed row.
Direct reduction of the differences gives instead

```text
A-C: 17,909-term nonzero weak normal form, lead -21762*tau^2,
B-D: 70,242-term nonzero weak normal form, lead  27593379*tau^2.
```

Thus the separate local reductions carry different hidden unit multipliers;
they are valid zero tests but are not canonical quotient representatives
that may be multiplied.  The apparent zero block product is **not** a
Wronskian-membership theorem.  This is an exact counterguard to the proposed
quotient-arithmetic shortcut.

## Coordinate-map guard and remaining calculation

The weak reconstructed mixed expression is proportional to
`N-z46*P`; numerically `497178/21762=297/13=z46`.  Because the separate weak
remainders are not multiplication-safe, this is evidence for—not proof
of—a coordinate mismatch.  It suggests that directly placing the verified
`W4/W5` rational series into the raw first-Rees `z46` slot may conflate that
coordinate with the later iterated bend coordinate.

Direct reductions of the full 5,949-term `M30` numerator, both for the
recurrence `N/P` and for the raw constant root `N=z46*P`, were capped after
their 207-row bases completed.  Neither run returned a normal form.  No
claim about mixed membership or `H0/H1` follows.

The next bounded calculation should first audit and export the exact
coordinate map from the iterated bend variable to the raw first-Rees chart.
Alternatively,
one can obtain multiplication-safe representatives by tracking the local
unit multipliers (or by a homogenized/global lift certificate) for `A,B,C,D`.
Only after that correction is it valid to test the finite Wronskian and the
two pure numerators.
