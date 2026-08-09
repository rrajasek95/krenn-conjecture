# O4 fourth incidence frontier: odd circuit

The fourth 159-cell maximum left by the coefficient CEGAR has 4,317 exact
generators.  Three full-output plus binomials, records 3276, 2598, and 2496,
form an odd exponent circuit.  With the third row reversed, their first-term
product equals their second-term product.

The standard three-binomial identity gives twice that common localized
monomial.  The checker multiplies it to an explicit ordinary `U^3` identity
over all 159 localized variables.  This closes the face over every field of
characteristic different from two, including the complex numbers.

The circuit uses ten localized witness cells.  Together with the 34 face
omissions it gives a support-faithful clause.  The checker enumerates and
emits every distinct transport under the eight automorphisms of the O4
universe.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_fourth_incidence_frontier_odd_circuit.py
python3 -O computations/verify_n8_d1_residue_orbit4_fourth_incidence_frontier_odd_circuit.py
```
