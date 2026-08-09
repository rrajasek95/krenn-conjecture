# Full-fibre tangent guard and the zero-stratum radical witness

## Outcome

The occupied-source idempotent found in the three-cylinder relaxation is
not tangent to a fixed full matching tensor.  Intersecting the exact
27-dimensional cylinder tangent with the Jacobian kernel of every full
tensor coefficient leaves dimension 7.  That 7-space is exactly the part of
the previously displayed gauge-plus-boundary span which fixes the full
tensor.  In particular the occupied direction `23;21`, whose derivative is

```text
00210000 - 00210012,
```

is excluded.

This removes the diagonal loop on the honest fixed-tensor tangent at the
anchored mixed source.  It does not by itself prove a local theorem at a GHZ
source: the anchor is the three-cylinder countermodel, whose full tensor is
not the target.

Two complementary exact results sharpen the geometry.

1. The literal GHZ fibre on the audited fifteen-parameter edge-23/edge-67
   plane is empty.  Its 107 mixed equations have unit ideal; more simply,
   the mixed coefficient `00000012` is identically `-1` on that plane.
2. On the occupied-weight-zero stratum, all twelve five-cross supports whose
   old positive-degree witness died have a new radical Fitting determinant
   which is a Laurent monomial.  Hence every one of those supports is still
   excluded for arbitrary nonzero cross weights.

Together these results distinguish the two phenomena cleanly.  The
idempotent is real in the relaxed cylinder algebra, but it neither belongs
to the fixed-full-tensor tangent nor creates a survivor on the twelve
degenerate five-cross tori.

## Fixed-full-tensor tangent

The full cylinder-plus-anchor tangent calculation has rank 225 on 252 old
decorated coordinates, hence dimension 27.  Appending the derivatives of
all full matching-tensor coefficients raises the constraint rank to 245,
so the fixed-full-tensor intersection has dimension 7.

Independently, restrict the 26-dimensional target-gauge plus absent-boundary
span by the same full-tensor derivative.  Its kernel also has dimension 7,
and exact rational containment holds in both directions.  Thus

```text
fixed-tensor cylinder tangent
    = fixed-tensor part of (target gauge + absent boundary directions)
```

at this anchored point.  The unique relaxed tangent quotient `23;21` is not
present.

This is a useful local model for an arbitrary-source theorem, but its scope
must remain explicit.  A tangent at a mixed countermodel is not the tangent
at a hypothetical realization.  The next calculation does promote the
anchored cylinder germ itself to a complete local statement; the global gap
is a degeneration theorem placing a hypothetical source in this germ.

## Coefficient-complete cylinder plane and the smooth germ

The full fifteen-variable edge-23/edge-67 plane lies in the three-cylinder
plus pure-anchor locus.  This is checked coefficient-completely, not on a
parameter grid.  Each matching coefficient has one of the 72 possible
constant, left-linear, right-linear, or cross-edge bilinear grades.  For
each cut and each of the 27 boundary words, the checker constructs polynomial
coefficients in a fixed fourteen-column frame for both the one-cross tensor
and the combined residual.

On every cut the moving frame is

```text
M(parameter) = M(0) (I + K(parameter)),    K^2 = 0.
```

Thus its inverse is the polynomial frame `(I-K) M(0)^-1`.  Literal
reconstruction at every one of the 243 interior coordinates proves that all
affine/bilinear coefficients of both cylinder identities vanish.  The three
pure-anchor polynomials are identically one.

The effective target-stabilizing gauge orbit has dimension 12.  Its product
with this exact 15-plane has differential rank 27, equal to the entire
cylinder tangent dimension.  Since the ambient 252-coordinate cylinder
scheme has Jacobian rank 225 at the anchor, the local dimension is squeezed
between 27 (the displayed family) and 27 (the tangent space).  The anchor is
therefore a smooth point, and the gauge-times-plane map is etale at that
point.  Equivalently, it identifies the completed local cylinder germ with
the completed gauge-times-plane germ.

On the plane the coefficient `00000012` is the unit `-1`; target gauge only
multiplies it by an invertible character.  Hence the full GHZ fibre has empty
intersection with this completed cylinder germ.  This is a legitimate local
exclusion theorem.  What remains global is to prove that an arbitrary
hypothetical source can be moved or degenerated into the anchored germ.

## Empty full-target fibre on the fifteen-parameter plane

Adjoin all fourteen absent boundary cells on physical edges 23 and 67 and
the occupied modulus `23;21`.  Matching dependence has exact bidegree at
most `(1,1)`, so the complete full tensor is recovered from the constant,
15 linear, and 56 cross-edge bilinear coefficients.

After subtracting the GHZ target there are 107 literal mixed word equations.
Every one of the fifteen variables occurs by itself as a forced coordinate.
More decisively, the word

```text
00000012
```

has constant coefficient `-1` and no variable term.  Thus the ideal is the
unit ideal before any localization.  An independent Singular Groebner
calculation returns `G[1]=1`; saturating by the physical occupied weight and
specializing that weight to zero both remain empty.

This rules out a full GHZ source on the audited plane.  It does not cover
the seven fixed-tensor tangent combinations involving target gauge, nor
directions on other physical edges.

## Exact full-source audit at occupied weight zero

Delete the old cell `23;21` and reconstruct the literal N=10 source on the
twelve cross supports where the earlier selected positive-degree jump died.
At the exact cross point `(1,2,3,5,7)`:

```text
pure anchors                         (1,1,1) on 12/12
one-cross out-of-span rows           0 on every support and every cut
target defect                        3 on every support and every cut
complete residual-cylinder cuts      none
mixed full-tensor words              40 on six, 48 on six
```

For cut 2, every support has cofactor rank 21 and exactly four out-of-span
combined-residual boundary rows.  On the first support, the first boundary
word is `000`; its exact quotient remainder is

```text
4:1, 8:1, 1008:3, 1010:5, 1014:6, 1016:10.
```

Thus the semisimple anchor/target-defect data pass, while the final linear
radical compatibility fails.  The lost positive-degree minor had deleted
the row carrying this complementary obstruction.

## Laurent-monomial radical semi-invariants

For each lost support, retain cut 2, boundary word `000`, the same 21
cofactor labels, and quotient pivot 4.  Reconstruct the complete five-cross
polynomial matrix from all 32 Boolean corners by exact Mobius inversion.
Its 22-by-22 augmented determinant factors into a Laurent monomial.

The twelve supports form three literal determinant classes:

| support class size | determinant up to sign |
|---:|---|
| 6 | `a^4 c^3 d` |
| 3 | `a^4 c^2 d^2` |
| 3 | `a^2 b^2 c^4` |

The fifth cross weight is absent in all three classes.  Every displayed
determinant is nonzero on the full five-dimensional cross torus.  Therefore
all twelve occupied-weight-zero supports are excluded for arbitrary nonzero
cross weights, not only at the sample point.

This is the requested source-dependent two-character/radical replacement
in bounded form: after the anchor/defect characters pass, one radical row is
a torus semi-invariant and cannot cancel.  It is not yet an arbitrary-support
or arbitrary-old-source theorem; it closes exactly the twelve supports
created by the occupied-modulus degeneration.

## Reproduction

```text
python3 computations/verify_n8_three_cut_exactness_tangent.py
python3 -O computations/verify_n8_three_cut_exactness_tangent.py
python3 computations/verify_n8_boundary_plane_full_tensor_fibre.py
python3 -O computations/verify_n8_boundary_plane_full_tensor_fibre.py
python3 computations/verify_n8_boundary_plane_full_cylinder_identity.py
python3 -O computations/verify_n8_boundary_plane_full_cylinder_identity.py
python3 computations/verify_n10_occupied_modulus_zero_stratum.py
python3 -O computations/verify_n10_occupied_modulus_zero_stratum.py
python3 computations/verify_n10_zero_stratum_first_symbolic_radical.py --all
python3 -O computations/verify_n10_zero_stratum_first_symbolic_radical.py --all
```

All matching expansions, tangent kernels, quotient remainders, Mobius
coefficients, determinants, ranks, and Groebner reductions are exact over
the rationals.
