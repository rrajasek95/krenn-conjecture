# The tau-plus debt factors through bare Q, but is not yet a complete chain

Put

\[
 \delta_+=\frac{-B_0+2B_1-B_2-B_3+2B_4-B_5}{4},\qquad
 D=4\delta_+=(-1,2,-1,-1,2,-1).                       \tag{1}
\]

The matching--Bianchi idea is correct at the endpoint-tail level.  Its
remaining common-tail comparison is essential, however; it is the first
literal obstruction, not a harmless relabelling.

## What is already physical

The four differences are genuine endpoint-bar cycles:

```text
B1-B0: face 5, common tail q45:12
B4-B0: face 3, common tail q34:11
B1-B5: face 2, common tail q24:21
B4-B5: face 3, common tail q34:11
```

Within each line, subtracting the two endpoint routes cancels Omega,
ordinary residue, target, anchor incidence, and `W`, leaving the bare
`Q_N-Q_M` tail.  All four decorated multipliers have the same canonical
faces-`(3,5)` repeated `P3+K2` target degree.

This also passes the source-covariance check.  The physical fine-grade
automorphism `s=(2 5)` acts on the six complete columns by

\[
                 (B_0\ B_5)(B_2\ B_3),\qquad B_1,B_4\text{ fixed}.
\]

Literal transport of all 90 boundary features in every `B_i` verifies

\[
 B_1-B_0\mapsto B_1-B_5,\qquad
 B_4-B_0\mapsto B_4-B_5.                               \tag{2}
\]

Thus the equivariant `H0/H5` factorization is not merely a calculation in
`Q^6`, and it uses no selected denominator transgression.

## The exact literal obstruction

The endpoint cycle contains a bare all-derivation tail `Q_i-Q_j`.  In the
comparison target, `B_i-B_j` means the difference of two complete 90-term
full-nine boundaries.  Equality of their matching graphs does not identify
these source types.

The integral complete boundary in direction (1) has 540 literal features:
360 have coefficient `-1` and 180 have coefficient `+2`.  Each of the six
pure columns has at least 45 features private against all 288 columns of the
complete component.

There is a useful adversarial strengthening.  At coefficient level,
`delta_+` is already a rational combination of five `M_v` alpha packets:

```text
 +(1/4) alpha[0,1,2,3]
 -(1/2) alpha[0,1,2,4]
 +(1/4) alpha[0,1,2,5]
 +(1/4) alpha[0,1,3,4]
 -(1/4) alpha[1,2,3,4].
```

The five coefficients sum to zero, so even granting compatible placements
with a common terminal packet would cancel that terminal.  But the literal
`M_v` law is

```text
complete lower boundary = alpha,
Eq row                 = alpha.
```

Consequently the displayed combination has lower `delta_+` and still has
`Eq=delta_+`.  It is not the required Eq-zero translation.

Choose one private pivot in each `B_i`.  The rho-even integral covector

\[
 \chi_D=\sum_iD_i\bigl(\operatorname{private}_i-operatorname{Eq}_i\bigr)
                                                               \tag{3}
\]

kills every complete `r0` column and every literal `M_v` packet, because
their private and Eq coefficients agree.  Cap, physical Cartan, bare-Q
endpoint, and two-chart difference columns have zero in both sets of rows.
On the desired integral common-tail bridge `(private=D,Eq=0)`,

\[
                             \chi_D=12.                \tag{4}
\]

This is a physically labelled dual for the committed same-grade inventory.
It is not claimed to annihilate an unknown higher relative resolution.

## Frontier

The Bianchi construction therefore gives a sharp factorization, not a
construction.  The remaining statement is exactly one of the equivalent
forms

```text
common-tail bridge: complete lower=delta+, Eq=0, protected rows=0;
reduced-Eq form:    cancel Eq=delta+ on the zero-total M_v combination.
```

It must be placed in the actual tau-plus word and repeated-edge source
grade, compatibly with (2).  Conditional on that bridge and the local C4
bypass, no separate weighted denominator membership is needed.  Without
it, `delta_+` is not physical in the current inventory.

The checker is
`computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py`.
Its ledger digest is
`85a9002daf41154cab2d6671917dc0d6b4b33ae3f841d478ed4a74043e42bf8e`.
