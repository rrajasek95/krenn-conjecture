# Uniform one-site target incidence

Let `N>=2` be even, let the colour space have any dimension `d>=2`, fix a
site `v`, and fix a pure target colour `a`.  Expanding the matching sum by
the partner of `v` gives

```text
H_N = sum_(u != v) p_(vu,a)(site u) tensor C_u
    = e_a^tensor(N-1).
```

Here `p_(vu,a)` is the incident colour vector after fixing row colour `a` at
`v`, and `C_u` is the matching cofactor on the other `N-2` sites.

Suppose no nonzero incident vector lies on the target line `<e_a>`.  For
every nonzero route `u`, quotient the colour space at site `u` by the line
`<p_(vu,a)>`; use the identity map when the route is absent.  Tensor these
maps over all sites other than `v`.  The summand indexed by `u` dies in its
site-`u` factor.  The target survives, because every image of `e_a` is
nonzero, and a tensor product of nonzero vectors over a field is nonzero.
This is a contradiction.

Therefore some incident row-`a` vector is nonzero and is a scalar multiple
of `e_a`.  In exact-support language, at least one incident column is active
and target-only.  The matching identity is integral, and the proof works in
every characteristic; for localized coefficient functions one passes to the
fraction field of the integral domain.

This theorem is independent of `N=8` and the ternary palette.  The checker
audits the partner partition through `N=10`, the line/absent/non-target mask
trichotomy through palette dimension six, and imports the committed `N=8`,
`d=3` specialization and its 24 O4 support packets.

Reproduce with:

```bash
python3 computations/verify_uniform_even_n_palette_target_incidence.py
python3 -O computations/verify_uniform_even_n_palette_target_incidence.py
```
