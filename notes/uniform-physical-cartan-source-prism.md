# The physical Cartan source prism is uniform in the order

## Result

Let `H_N` be the complete decorated perfect-matching tensor at any even
order.  Choose two root sites `x,y` and a physical site transposition `s`
disjoint from them.  Let `w` be the simultaneous signed Weyl action on the
two local colour spaces.  Then

\[
                         K=(1-s)H_w                    \tag{1}
\]

is a source-provenant, target-preserving relative Cartan prism.  The result
also holds in a direct-free presentation whenever `s` fixes the removed
physical edge.

Thus the Cartan connector itself is not restricted to the canonical `h=3`
packet.  What remains component-specific is its fine-label projection,
terminal grading, and transverse visibility.

Checker:
[`verify_uniform_physical_cartan_source_prism.py`](../computations/verify_uniform_physical_cartan_source_prism.py).

## Local covariance is exact on every matching row

The product group `GL(3)^N` acts on physical decorated edge coefficients and
on the output tensor.  Every perfect matching contains exactly one edge at
site `v`, so for every local root field

\[
                      X_{\rm src}H_z=H_{X_{\rm out}z}. \tag{2}

This is termwise: differentiating the unique incident edge reconstructs the
complete coefficient with the colour at `v` changed.  It neither chooses a
matching nor assumes noncancellation.

Functions and their differentials generate the principal-parts algebra.
Pullback along the equivariant hafnian map therefore commutes with exterior
differentiation and contraction by the related vector fields.  Consequently
the root homotopies in (1) live in the complete physical source resolution,
not in a formal target mapping cylinder.

## Endpoint oddization kills the target defect

A physical site permutation transports perfect matchings literally.  If it
fixes the removed edge, it also preserves a direct-free chart.  The GHZ
target is invariant under every site permutation.

The Weyl action at `x,y` need not preserve the GHZ target separately, but its
defect is unchanged by any transposition `s` disjoint from `x,y`: the two
transposed sites have equal colours in every monochromatic target word.
Therefore

\[
                         (1-s)(w-1)\Delta=0 .          \tag{3}

Equations (2)--(3) prove (1) uniformly.  The checker audits all complete and
direct-free rows at orders six and eight, including every output word and
matching term.  The proof itself is independent of the order.

## Effect on the proof frontier

For a minimal zero-holonomy matching component `M`, the Schur theorem asks
for a physical word-changing connector `g`.  Equation (1) now constructs the
ambient source connector at every order.  The remaining choice problem is:

> choose `x,y,s` so that the projection of (1) to the marked critical
> component is nonzero and fine-label saturated, or its complementary
> residual is a typed exit visible in the deficient star quotients.

If the Cartan charge is nonzero, the rank-one adjugate formula gives the
Schur/Fitting unit.  If it is zero, the complete-lift residual

\[
                             R=G-Cy                     \tag{4}

vanishes on the critical component.  A saturated nonzero `R` is a literal
typed exit.  A zero residual is a protected kernel class in the complete
augmented comparison; it must be handled by an occupied-row deletion or by
the physical generator/annihilator alternative, rather than inferred from
`My=g` alone.

This replaces “construct Cartan at arbitrary order” by the narrower
**component incidence and augmented typing theorem**.

## Scope

The theorem does not assert that (1) is an occupied scalar source cell, that
its projection meets every critical component, or that canonical `h=3`
residue and terminal readouts transport automatically to every branch.
Those are exactly the remaining source-homological inputs.

## Verification

Run:

```text
python3 computations/verify_uniform_physical_cartan_source_prism.py
python3 -O computations/verify_uniform_physical_cartan_source_prism.py
python3 -I -S computations/verify_uniform_physical_cartan_source_prism.py
```

Frozen ledger SHA-256:

```text
23516fe5ff27fda7e9906b5a0da9dcdbec3103a85b52d0006b972c856c3e5258
```
