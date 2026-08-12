# The first repeated-grade bridge is a covariance--Spencer shift

## Exact grading theorem for the unrecoloured representative

The unrecoloured literal primitive order-six face has polynomial degree six and site
profile

```text
(2,1,2,1,2,1,1,2).
```

The five first rootless collision components have polynomial degree seven.
There is no fixed-label common-edge multiplier from any primitive fine
degree to any of those components.  More strongly, no one-edge promotion
exists after every residual-site permutation, endpoint swap, and independent
local colour permutation which preserves the normalized roles.

There is, however, one canonical *relative* bridge type.  Among the two
distinct primitive fine degrees, the mixed degree occurring in `A0*A1` and
`A1^2` reaches the repeated component joining faces `3` and `5` by

\[
 q_{13}^{00}q_{45}^{00}\,\partial_{07:11},              \tag{1}
\]

followed by the local Weyl transport `0<->1` at sites `0,2,6,7` and the
identity transport at the other four sites.  The normalized decorated
census has `48` presentations of (1), but they all have this same grading
type.  The checker finds exactly two records only because the same primitive
fine degree occurs in two source products.

Checker:
`computations/verify_h3_order6_to_repeated_grade_bridge.py`.

## Why this is the right structure

The endpoint sites `0,7` are doubled in the primitive literal face and are
squarefree in every first repeated component.  Conversely the repeated
component needs four additional internal incidences.  A polynomial
multiplier can only increase degrees, so it can never perform this move.
The minimal shift must remove the endpoint arm and insert a two-edge internal
tail; this is exactly the Spencer bidegree in (1).

The required local colour transport is not an arbitrary regrading.  At this
unrecoloured symbolic level it has the degree of a covariance--Spencer
transport.  It therefore proposes the form

```text
order-six principal-parts face
    -> local covariance transport
    -> q13*q45*partial_07 Spencer face
    -> repeated P3+K2 component (faces 3/5).
```

This removes two possible but false proof sketches for the unrecoloured
representative: the order-six face is
not an old response column, and it cannot be moved into the repeated grade
by a common monomial tail.

The first literal Spencer test is also exact.  Apply (1) to the two primitive
source-product pieces carrying the bridge degree and reduce against the
complete `288`-column faces-`3/5` component.  The two transformed outputs
have respectively

```text
07:11-divisible primitive terms      27       16
transformed support                   27       16
coefficient l1                     182/3      82
old-component remainder support     186      104
```

Neither belongs to the old component, and their quotient classes have rank
two.  Thus no scalar combination of these two literal faces repairs the
comparison inside the linear full-row module.  This is positive information
about the architecture: the required arrow is genuinely a higher bar/Tate
attachment (or its dual), not a concealed old-column relation.

## Physical scope correction and exact next theorem

The physical comparison uses the endpoint-recoloured, tail-antisymmetric
class.  Its separate audit is
`h3-endpoint-recoloured-primitive-face-grade.md`.  That class has the same
site profile and a unique normalized stub-level bridge to faces `(3,5)`, but
the abstract contracted edge is present in zero literal monomials.  Thus (1)
is a grading symbol, not literal differentiation of the physical output.

Equation (1) is a multigraded symbol identity for the unrecoloured
representative, not yet a relative chain.  The notation `partial_(07:11)`
refers to the distinguished order-six principal-parts direction.  Only `27`
and `16` terms of those unrecoloured outputs are divisible by `q07:11`, and
their transformed derivatives miss the old repeated-component image.

The next generator-level statement is therefore:

> Construct the endpoint-recoloured site-colour contraction in the complete
> order-six Hasse/principal-parts cone with the normalized faces-`3/5`
> bridge degree.  Its
> boundary in the faces-`3/5` repeated component is the required literal
> private-boundary aggregate, while `D,W,target,anchor` vanish and the
> commuting ridge supplies the pinned eta/sigma packet.

If that face is a boundary, it constructs the missing physical comparison.
If it is not, the exhaustive relative cone supplies the physical dual class.
Either outcome is useful only after the augmented readouts have been checked
as chain maps.

## Scope

This theorem is an exact fine-degree, normalized-symmetry, and first literal
membership classification of the unrecoloured representative.  It does not
construct the higher source
boundary, the covariance-prism chain map on the complete bar/Tate complex,
augmented readout compatibility, or transverse rank landing.

Run:

```text
python3 computations/verify_h3_order6_to_repeated_grade_bridge.py
python3 -O computations/verify_h3_order6_to_repeated_grade_bridge.py
python3 -I -S computations/verify_h3_order6_to_repeated_grade_bridge.py
```

Frozen ledger SHA-256:

```text
f31903449a1c8b4a343b95b9399fbe4677be22eb2050e2f5a5c4fc46f3a5adef
```
