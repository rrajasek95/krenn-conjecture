# O4 third incidence frontier: ordinary saturation

After the first two coefficient-face clauses, the O4 downset CEGAR exposes a
third 159-cell maximum with 4,321 exact coefficient generators.  The same
pivot-ordered Laurent engine closes it directly.

The 54 unique plus-binomial rows have rank 20.  Full-output record 3129
reduces to

```text
x05_02*x15_11*x27_01*x36_10*x47_02/x57_22.
```

The checker expands this rewrite back into the original equations, cancels
the cofactor expression to five source records, clears all negative
exponents, and verifies an ordinary ten-term polynomial identity putting
`U^2` in the original coefficient ideal.  All coefficients are integral, so
the certificate is valid in every characteristic.

Only 15 localized cells occur in the five source equations.  Together with
the 34 face omissions they give a support-faithful clause, with eight
distinct transports under the O4 universe automorphisms.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_third_incidence_frontier_saturation.py
python3 -O computations/verify_n8_d1_residue_orbit4_third_incidence_frontier_saturation.py
```
