# First nonlinear resultant frontier below O4

The torus-consistent 157-cell face does admit one further exact compression.
Four full-output trinomials (records 2381, 2810, 3569, 3596) share two terms
after Laurent alignment.  Their six pairwise resultants are reconstructed all
the way back to the original coefficient generators.  They are six consistent
binomials of character `+1`, adding rank three to the character lattice.

The extended lattice has 97 rows, rank 39, and 58 character-consistent
dependencies.  Every pivot is a unit, and the checker freezes and verifies an
explicit Laurent parametrization by 118 free nonzero parameters.  Reduction
of all 4,321 coefficient generators leaves 3,600 nonzero Laurent equations.
There are no one- or two-class rows.  Among the 233 trinomials, all 5,241
two-term alignments are exact Laurent shifts of the same equation; none yields
a new binomial.  Thus the cheap resultant closure has reached a genuine
nonlinear residual ideal, frozen under SHA-256
`47e42c702626087533e538c21e2fc72ed7a5fc2187de414ab581a300b5d564ea`.

The exponent differences of all remaining equations span rank 99 inside the
118-dimensional quotient torus.  Hence 19 torus directions are inert and can
be discarded, but the active nonlinear problem is still 99-dimensional.  The
rank is reconstructed from 22,728 distinct difference rows with unit pivots;
it is the current clean measure of counterexample proximity.

There is no cyclotomic shortcut.  Residual record 1768 has four Laurent
monomials with coefficients `1,1,1,6`.  On any unit-circle character, the last
term has modulus 6 while the other three sum to modulus at most 3.  Therefore
no root-of-unity character of any order can solve this residual ideal.  This
also explains why the exploratory `mu_3`, `mu_4`, and `mu_6` searches cannot
produce a point without relying on a solver verdict.

This is not an emptiness proof and not a coefficient point.  The next exact
lane is elimination/saturation in the 99-dimensional active quotient,
starting with the frozen three- and four-class rows.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_157_resultant_frontier.py
python3 -O computations/verify_n8_d1_residue_orbit4_157_resultant_frontier.py
```

Frozen ledger SHA-256:
`c80555e585d60739a9809404726251ce7a983175746b45a4c4d915991b6c18a0`.
