# The primitive order-six face is relative, not an old correction column

## Exact result

The canonical order-six secondary class has symbolic primitive face

```text
07:11 wedge 24:11
```

with coefficient one.  This symbol is the correct endpoint-arm/disjoint-
cofactor topology for one-sided landing, but its literal polynomial face
must not be identified with an existing physical response column.

Remove these two directions from each of the 188 selected sixth-order
operators, apply the remaining four derivatives to the three quadratic
source products, and retain the quadratic coefficient.  The exact outputs
have the following inventories:

| source product | support | coefficient `l1` | fine degrees |
|---|---:|---:|---:|
| `A0^2` | 167 | `3272/3` | 1 |
| `A0*A1` | 343 | `3029/3` | 2 |
| `A1^2` | 191 | `950` | 1 |

Every monomial has site profile

```text
(2,1,2,1,2,1,1,2).
```

For each occurring fine degree, an old source boundary with this profile
would have to be a complete squarefree eight-site source row multiplied by
a decorated two-edge perfect matching on the four doubled sites.  There are
respectively only `3`, `9`, and `6` compatible columns.  The middle count is
`6+3` across its two distinct fine degrees; those columns cannot be merged
by forgetting their decorations.  In all three
products the literal primitive output contains respectively `71`, `148`,
and `83` monomials absent from every compatible column.  Therefore none of
the outputs lies in the old physical
full-row-multiplier span.

The signed support counts above correct an earlier verifier error: unary
`+Counter` was used as a zero filter, but Python also drops every negative
entry.  The old values `79,181,106` were exactly the positive-support counts.
The corrected checker filters only zero coefficients and retains the full
signed polynomial.  The symbolic pair shadow and the relative/nonmembership
conclusion are unchanged; the literal polynomial is larger.

Checker:
`computations/verify_h3_order6_primitive_face_literal_boundary.py`.

## Interpretation

This distinguishes two statements which had begun to blur together.

1. The symbolic pair shadow is exactly the required `-delta` face and its
   primitive term has the correct overlap topology.
2. The actual fourth-derivative face is a new relative/principal-parts
   boundary.  It is not a disguised 90-term response correction.

Hence the order-six construction should be inserted into the canonical
bar/principal-parts cone.  In that exhaustive cone, either its primitive
face is attached to the repeated physical grade by a higher boundary or a
dual cocycle detects the failure.  Directly declaring the symbol to be the
literal mapping-cone column would omit the private monomials above.

This supports the resolution-exhaustive proof architecture: the source-side
secondary class is genuine, but the comparison must be made by a relative
chain map or by its dual alternative, not by termwise identification.

## Scope

The theorem concerns the fixed canonical 188-term representative and its
common primitive face on the three quadratic source products.  It does not
rule out the higher relative attachment, construct the covariance-prism
endpoint gluing, or prove transverse landing.

Run:

```text
python3 computations/verify_h3_order6_primitive_face_literal_boundary.py
python3 -O computations/verify_h3_order6_primitive_face_literal_boundary.py
python3 -I -S computations/verify_h3_order6_primitive_face_literal_boundary.py
```

Frozen ledger SHA-256:

```text
b19c30d4d54a08c920dd53bc37e17606f4d6f29057aa89057e71f7c7d8c5e0df
```
