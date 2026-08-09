# O4 second incidence frontier: iterated Laurent closure

The maximal plus-binomial character of the second 159-cell incidence face is
consistent, but a pivot-ordered Laurent reduction is already decisive.  Use
one representative of each of the 54 exact plus-binomial exponent rows.
Their rank is 20.  Reducing in ascending pivot order sends full-output record
1551 directly to

```text
x04_00*x15_12*x26_01*x37_00*x57_12/x57_22.
```

Every variable in this Laurent monomial is localized, so the normal form is
a unit.  To make the localization semantics completely explicit, the
checker expands each lattice row back into its source plus binomial, builds a
Laurent cofactor identity, clears all negative exponents, and multiplies the
resulting ordinary monomial identity to `U^k`, where `U` is the product of
all 159 localized variables.  It verifies the final ordinary polynomial
identity term by term.  Every coefficient is integral, so the closure is
valid in every characteristic.

The direct rewrite uses nine lattice rows plus record 1551; cancellation in
the expanded ordinary identity minimizes it further to seven original source
records.  In fact the final cleared identity already gives `U^1`.  The
checker emits a support-faithful face clause: either one of the 34 omitted
cells is restored or one of the named source-monomial witnesses is removed.
It also emits all eight distinct transports under the eight automorphisms of
the O4 universe.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py
python3 -O computations/verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py
```
