# Finite-abelian Fourier uncertainty: terminal source-lift no-go

For `G=(Z/3)^n`, ternary GHZ is the indicator of the diagonal subgroup:
its support has size 3.  Its unnormalized Fourier transform is 3 times the
indicator of the sum-zero subgroup, of size `3^(n-1)`.  Hence it saturates
Donoho--Stark, Parseval, and the `L1 -> Linf` Hausdorff--Young endpoint.

This equality does not add a source equation.  With `U=F_3/sqrt(3)`, put

`B_uv = U A_uv U^T`.

Termwise over perfect matchings,

`H_n(B)=U^tensor n H_n(A)`.

This is an isometric bijection of the two source fibres.  It preserves the
total Frobenius norm, full port isotropy, global and local minimum status,
and clean-cap existence (with the cap covector transformed
contravariantly).  Output uncertainty equality therefore merely identifies
the already-known target orbit.

The exact `n=4` must-pass control is decisive.  Its three-one-factor GHZ
source is a global norm minimum of squared norm 6 and has `R_v=I`.  After
Fourier transformation all six live edge matrices are dense rank one.  All
six fail both natural edgewise charge-conservation patterns, and each of the
three physical perfect matchings carries only one character channel—not a
common three-channel matching.  Nevertheless the source retains its active
cap: pair `01` with `K=I` gives residual
`E00+E11+E22=I`.  Thus any valid cap conclusion must use machinery beyond
output Fourier equality.

The frozen projective charge-lift theorem is stronger: an exact Fourier-GHZ
source cannot be made edgewise charge homogeneous even using vertex scalars
and target stabilizers.  Full isotropy does not reverse this.  The phased
six-site source remains an exact smooth local norm minimum for its own
non-GHZ output (`R_v=7I`, star ranks 45, triangle ranks 27), while the dense
eight-site `F_3` model has `R_v=21I` and no charge-conserving support.  The
invisible chord stays invisible under the invertible output transform;
minimum norm deletes that particular inactive chord but supplies no Fourier
character law.

Consequently a useful Fourier continuation would need a new
source-relative inequality coupling individual matching summands and the
mixed zero sums.  Donoho--Stark/Hausdorff--Young equality alone is exhausted.

Logical digest:
`d4f532513bdec735402325c2f44c62bfaba839c61883582fc9de1f8fe3a51c03`.
