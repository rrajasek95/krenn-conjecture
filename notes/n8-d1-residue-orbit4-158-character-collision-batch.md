# O4 later 158-cell character collision

This is the first later O4 face with no one-class row after quotienting by its
complete rank-25 plus-binomial lattice.  It is nevertheless still decided by
the exact two-class criterion: among 256 two-class rows, records 1260 and 1269
have the same displacement and opposite characters.

The checker expands both reductions through the original plus equations,
aligns one endpoint, cancels it, and obtains twice the other Laurent monomial.
After clearing every negative exponent and saturating by the 158 localized
variables it verifies an ordinary `U^2` identity using 13 original generators.
The final division by two makes the certificate valid in characteristic not
two, in particular over `C`.  Eight support-faithful O4 transports are emitted.

Thus this face is not yet the stopping case: it has no one-class row, but its
two-class character system already has a nontrivial length-two holonomy.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_158_character_collision_batch.py
python3 -O computations/verify_n8_d1_residue_orbit4_158_character_collision_batch.py
```
