# N=8 D1: first m=10 3+3+4 coefficient candidate

The complete support-shadow method does not close all of m=10.  On symbolic
branch `334:63`, exact dynamic repair leaves one ten-cell off-Sigma support.
A Boolean model supplies 67 additional Sigma cells.  The checker
`computations/verify_n8_d1_m10_334_branch63_candidate.py` discards the
solver's auxiliary assignment and directly verifies the resulting semantic
77-cell support against every one of the 8,100 fibres.

All six pure fibres have exactly two live matching terms.  Every mixed fibre
has either zero or at least two live terms.  Thus this is a genuine complete
support-shadow candidate, rather than merely a failure of root unit
propagation.  The checker also reconstructs branch 63 from the committed
normal-form orbit and verifies that dynamic repair has exactly this one
off-Sigma residual.

The frozen artifact
`computations/certificates/n8_d1_m10_334_branch63_candidate.json` records the
exact support, declares every supported cell nonzero, and exports the full
sparse coefficient system.  It has 77 localized variables and 523 distinct
generators: 469 full-output equations, 52 six-site Lemma-F equations, one
residue-purity equation, two dagger equations, and the D1 harm equation.
All a-pendant equations vanish identically on this E1 support.  There are no
one-term generators, so the earlier monomial/unique-fibre obstruction cannot
decide this candidate.

The coefficient artifact SHA-256 is
`da34a34cbeac0e30309088f17007b63274cb65435719e3106515b18ede9ffccd`.
Its exact generator-record SHA-256 is
`ae7a0afb00dbe12c6b1a2acbe16b075e9726fae1888da752973c3468ce394419`,
and the checked ledger SHA-256 is
`52e8085fb995dd66fc1da7743cc172fac52bd8baa12da79ec46a0de1d4968c33`.
Normal and optimized replays recompute all equations and compare the complete
artifact byte-for-byte.

This support is not an N=8 counterexample.  The subsequent three-binomial
saturation certificate proves that its localized coefficient ideal is empty
over every field of characteristic other than two.  See
`notes/n8-d1-m10-334-branch63-ideal-closure.md`.
