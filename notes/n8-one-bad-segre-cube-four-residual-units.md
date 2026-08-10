# The four residual Segre--K4 one-cell charts are unit ideals

## Exact result

The degree-filtered unary identities close 72 of the 76 one-coordinate
deformations of the full diagonal-carrier Segre--K4 chart.  The four residual
directions are

```text
02:20, 03:10, 04:20, 05:10.
```

For each direction, form every nonzero coefficient of \(q^{[3]}-X_0\).
There are 411 source-labelled rows and 901 terms.  Exact characteristic-zero
standard-basis lifting gives an integral combination equal to the constant
2.  The certificates use respectively 14, 15, 14, and 15 source rows.

The checker
`computations/verify_n8_one_bad_segre_cube_four_residual_units.py` invokes
Singular `liftstd`, verifies `matrix(I)*L=matrix(G)` exactly, checks that the
unique basis element is 2, and pins every active source label and full lift
hash.

Consequently every one-cell extension of the 45-variable chart

\[
H+\sum d_{ij}(00)+\sum a_{ij}(11)+\sum b_{ij}(22)
\]

is top-empty over \(\mathbb Q\), and hence over \(\mathbb C\).  The one-bad
response equations are not needed for this conclusion.

## Remaining scope

This exhausts first support order around the fixed Segre--K4 initial form,
but not simultaneous deformations.  Two or more added mixed cells can create
new matchings that no one-cell certificate sees.  The next theorem should
be an initial-form/chart-cover statement showing that an arbitrary common-q
one-bad packet degenerates to this chart, or a source-labelled critical-pair
analysis for the first simultaneous deformation.  Another unstructured
support-cardinality search would not globalize the result.
