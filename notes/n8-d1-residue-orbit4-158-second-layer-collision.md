# O4 158-cell second-layer character collision

The first 158-cell face that escapes the direct signed-Laurent oracle is
still coefficient-empty.  Modulo the rank-20 plus-binomial character,
full-output records 1551 and 1611 reduce to two Laurent binomials with the
same exponent difference and opposite constants.

After multiplying the first normal form by one Laurent monomial, one class
cancels in their sum and the other doubles.  The checker expands both normal
forms back through the original plus equations, verifies the collision in the
Laurent ring, clears all negative exponents, and multiplies to an ordinary
`U^k` identity in the original 4,321-generator ideal.  The only final
denominator is `1/2`, so the certificate is valid in characteristic not two,
in particular over the complex numbers.

This is the common transfer/holonomy determinant promised by the four
159-cell charts in its smallest form: the first character is consistent, but
two lifted rows assign opposite characters to the same next exponent class.
The emitted support clause includes every O4 automorphism transport.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_158_second_layer_collision.py
python3 -O computations/verify_n8_d1_residue_orbit4_158_second_layer_collision.py
```
