# Axis-pure cancellations require at least seventeen decorated coordinates

## Result

The sole branch left by `80732b0` has no full-source-compatible support
through `16` decorated coordinates.  This is an exact support theorem, not a
random coefficient search.

Work with

\[
 q^{[3]}=X_0,\qquad
 p_i s_jq^{[2]}=\delta_{ij}X_i,quad i,j\in\{1,2\},
\]

in the axis-purified chart: every `q` cell is colour-diagonal and endpoint
row `i` is supported only in colour `i`.  Then

\[
\boxed{|\operatorname{supp}(q,p_1,s_1,p_2,s_2)|\ge17}
\]

for every exact source over a field.

Checker:

```text
computations/verify_h3_axis_pure_cancellation_support_lower_bound.py
```

Frozen ledger digest:

```text
144a19ff9a970d26add55bcd3b3a953e742695a772e64be23649d82ba112f4d0
```

## Why singleton matching fibres are decisive

Every occupied coordinate has nonzero value.  Therefore a coefficient that
contains exactly one supported matching monomial is nonzero: it is a product
of nonzero source coordinates and cannot cancel.  Every off-target
coefficient of the five displayed tensors must be zero, so its matching
fibre must contain either zero or at least two monomials.

Each nonzero target coefficient contains at least one supported target
monomial.  Choose one in each of `X0,X1,X2`.  These three monomials form an
eleven-coordinate target skeleton:

```text
3 q:00,
2 q:11 + p1 + s1,
2 q:22 + p2 + s2.
```

Fixing the `X0` matching as `01|23|45`, there are `8,100` labelled target
skeletons.  Its site stabilizer has order `48`, leaving `185` orbits.  Thus
every axis-pure support is represented by one of these skeletons plus its
extra coordinates.

The checker builds all `3,645` matching monomials in all `849` output
fibres.  It then enforces only the necessary no-singleton condition; it does
not assume generic coefficients or termwise vanishing.

## The first circuit layer is a lock cascade

No skeleton can repair all of its original singleton fibres with one, two,
or three added coordinates.  Four added coordinates produce the first
possible matching-circuit layer:

```text
21 skeleton orbits,
98 minimal four-coordinate repair cores.
```

None of the corresponding support-`15` packets is globally
cancellation-compatible.  Each repair core creates new singleton unary or
response fibres.  This is the literal five-row lock phenomenon: cancelling
one alternating matching circuit exposes a proper face elsewhere.

Adding one arbitrary fifth coordinate gives all `5,292` support-`16`
placements capable of repairing the old skeleton locks.  None is globally
compatible.  Even the closest packet retains five singleton full-row
coefficients.

Thus a hypothetical exact axis-purified source begins only at support `17`
or higher.

## Relation to maximum-anchor/minimum-support

The lower bound holds for every exact axis-purified source; it does not use
the lexicographic extremal choice.  At a maximum-anchor/minimum-support
source it says that the remaining occupied support must carry genuine
coupled circuits, not merely one cancellable `C4`.

A two-monomial zero fibre has the usual alternating-cycle toric resize.  But
the complete finite difference consists of the unary row and all four
response rows.  The 98-case cascade shows concretely why preserving one
fibre is insufficient: its other full-row faces need not vanish.

The shortest remaining theorem is therefore:

> For an axis-purified exact support of size at least `17`, the coupled
> matching-fibre circuit hypergraph has an anchor-safe toric direction, or
> one nonzero cycle lock supplies an existing unit, literal coloop, or active
> common-`q` carrier.

No support-`17` guard is constructed here, and no emptiness claim for the
full ternary source locus is made.
