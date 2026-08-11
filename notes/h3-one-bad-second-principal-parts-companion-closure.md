# The physical companion row closes the smallest h=3 principal-parts module

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_second_principal_parts_companion_closure.py`

## Verdict

For the literal genuine-common-`q` packet isolated in `f7c15e8`, adding the
`(t,t)` target row and the `ca` mixed common-hole row does **not** by itself
kill the off-one-edge self-square.  The resulting localized scalar module
has a primitive one-dimensional cokernel

```text
lambda(S,O) = S-O,
S=Q0*Q1,  O=C.
```

However, `O` is not a hypothetical principal-parts generator.  It is the
actual mandatory mixed output coefficient with word

```text
21000121 = (06:22)(12:10)(34:00)(57:11).
```

This is the `(c,t,c)` row in the `pr`-diagonal companion sector.  On the
literal packet its coefficient is exactly `C`.  Adding this physical row
supplies the column `(S,O)=(0,1)`, kills the cokernel with determinant one,
and forces `Q1=0`.  The other three endpoint stars are already singleton,
so all four divided self-squares vanish while the `ca` row remains zero and
the `tt` row remains the pure target `X_t`.

Thus the smallest literal second-principal-parts gate is positive.  The
remaining uniform theorem question is narrower: classify the cancellation
mates which can occur in this same `(c,t,c)` coefficient for an arbitrary
full source.

## Exact scalar module

Use the seven common-site cells

```text
A=13:11, B=24:11, C=12:10, E=02:10,
D=34:00, F=01:00, G=23:22
```

and the five localized equations

```text
g1 = Q0*A*B - 1,
g2 = Q0*C + Q1*E,
g3 = Ra*F*D - 1,
g4 = Dca*E + Q0*Ra,
g5 = Pt*Qt*Rt*G - 1.
```

At

```text
A=B=C=D=F=G=Q0=Q1=Ra=Pt=Qt=Rt=Dca=1,
E=-1,
```

these encode

```text
Q_c q^[2] = X_c,
R_a q^[2] = X_a,
P_t(D_ca q^[2] + Q_c R_a q) = 0,
P_t Q_t R_t q = X_t.
```

The Jacobian columns `(B,E,F,Dca,G)` form a `5x5` minor of determinant
`-1`.  Hence every first- or second-order boundary tail in these five rows
can be corrected integrally without changing `Q0,Q1,C`, and therefore
without changing either `S` or `O`.  This proves that the `tt` target row
does not secretly remove the cokernel.

The exact relation

```text
E*S + Q0^2*O = Q0*g2
```

specializes to `S=O`.  Therefore `(1,-1)` is the saturated primitive
cokernel covector: it kills the available tangent class `(1,1)` and pairs
to one with the desired invisible self-square `(1,0)`.

## Physical provenance and integral closure

Embed the common packet in sites `0,...,7`, with outer sites `5,6,7`, by

```text
56:00, 57:11, 67:10,
15:22,
06:11, 16:11, 06:22,
27:00, 47:22.
```

The mixed output word `21000121` has exactly the matching displayed above,
so its coefficient is `C`.  It is a required zero coefficient of the
original endpoint-coloured matching tensor, not a declared jet column.
Its readout is `(0,1)`, and

```text
det [[1,1],[0,1]] = 1.
```

Consequently the physical companion row gives `C=0`; since `E` is a unit,
`g2=0` then gives `Q1=0`, hence `Q_c^[2]=0`.  The checker verifies directly
that setting `C=Q1=0` preserves both pure diagonal targets, the `ca` mixed
row, and the `tt` target.

## Scope guard

The displayed point with `C=Q1=1` satisfies the five selected scalar rows
but its `21000121` coefficient is one.  It is therefore **not** a full
source and not a counterexample.  The result proves closure only for this
small literal localized packet.

For a general source, the same physical coefficient can contain additional
matching monomials.  Those cancellation mates are source-valid, so one may
not replace the complete `(c,t,c)` row by `C=0` without classifying them.
The next bounded theorem-facing task is exactly that classification by
endpoint-use and internal-`q` grade.  No higher Hasse order, support CEGAR,
or global Groebner computation is indicated.
