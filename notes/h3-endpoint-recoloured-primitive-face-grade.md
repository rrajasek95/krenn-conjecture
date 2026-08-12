# The physical order-six bridge is a principal-parts contraction

## Exact grading audit

The bridge calculation must be applied to the endpoint-recoloured,
tail-antisymmetric order-six class, not merely to its unrecoloured primitive
representative.  After endpoint composition, removal of the primitive
directions `07:11` and `24:11`, and evaluation on the three quadratic source
products, the literal outputs are

```text
source product       operators       support       l1       fine degrees
A0^2                    168              21        663            1
A0*A1                   168              54      961/2            2
A1^2                    168              32        444            1
```

Every fine degree has site profile

```text
(2,1,2,1,2,1,1,2).
```

At the level of site/colour degree stubs, exactly one normalized bridge type
lands in repeated component `1`, joining faces `(3,5)`.  It removes the
abstract coloured arm `07:01`, inserts the tail `13:00|45:00`, and uses the
local colour permutations

```text
site 0: 0<->1       site 2: 0<->1
site 6: 0->1->2->0  site 7: 0->1->2->0,
```

with identity at the other sites.  There are `192` decorated presentations
for each of the two source-product occurrences.

For this sparse representative, the decisive literal test is negative: the
abstract contracted edge `07:01` occurs in **zero** terms of either relevant
physical output.  Direct differentiation by that abstract edge therefore
gives the zero polynomial.  The bridge is a principal-parts/site-colour
contraction, not a hidden `07:01` edge derivative, a common-tail matching
identity, or an old repeated-component column.

This is not a representative-independent vanishing statement.  The exact
first-Spencer-flat affine representative in
[`h3-first-flat-endpoint-bridge.md`](h3-first-flat-endpoint-bridge.md)
contains 48 literal presentations through the physical direction `07:11`.
None lies in the old repeated component, and the simultaneous exact bridge
system has zero pure aggregate.  Thus affine freedom restores the physical
face but still does not manufacture the missing relative aggregate vertex.

Checker:
`computations/verify_h3_endpoint_recoloured_primitive_face_grade.py`.

## Consequence for the proof

The grading calculation identifies the source and target of the desired
comparison but does not construct its arrow.  The correct local theorem is:

> In the exhaustive labelled principal-parts/bar cone, the site-colour
> contraction with the displayed degree has boundary equal to the physical
> endpoint-recoloured order-six face minus the faces-`3/5` repeated-grade
> comparison packet, with all protected augmented readouts zero and the
> prescribed ridge terminal.

This is a chain-level naturality statement.  It should be proved on the
universal operator symbols using the Spencer--Euler contraction and
covariance commutators, then descended to the physical labelled complex.
Searching for a literal matching edge cannot prove it, because that edge is
absent from the polynomial support.

The unrecoloured bridge and its cyclic rank-four incidence remain exact
grading models.  Their role is to specify the required symbolic comparison
cell and show that five faces leave only one aggregate class.  They are not
the physical comparison themselves.

## Scope

No relative boundary, terminal descent, rank landing, or clean overlap is
asserted here.  The result removes a false construction route and reduces
the first proof obligation to one explicit principal-parts comparison map.

Run:

```text
python3 computations/verify_h3_endpoint_recoloured_primitive_face_grade.py
python3 -O computations/verify_h3_endpoint_recoloured_primitive_face_grade.py
python3 -I -S computations/verify_h3_endpoint_recoloured_primitive_face_grade.py
```

Frozen ledger SHA-256:

```text
bee8fafb4de176d1049c816f0726870a9f001a44271cdde28c695c10ff533369
```
