# Rep5 smallest-67 factor/determinant reduction

Verdict: **an exact strict factor cover exists; no source-literal determinant/rank split is smaller.**

The grading is full rank 67. There are no inactive coordinates, affine-linear generators, unit-monic graph substitutions, or interaction blocks. The exact constant-linear coefficient rank is 40 over `Q` (and at both audit primes).

All 36 two-by-two minors and four determinants of the complete `A12`, `A15`, `A24`, and `A67` 3×3 blocks were constructed exactly. None is constant, monomial, a generator up to sign, or an exact polynomial factor of any generator. Thus none gives a source-literal Cramer/rank split that is strictly smaller; this is not an ideal-membership or radical-membership claim.

Exactly 27 coordinates divide complete generators, each with maximum count 54. Exhaustive scoring selects the recorded coordinate. `D(x)` adjoins `inv_x*x=1` and divides all 54 factors; `V(x)` sets `x=0`, giving a strictly smaller branch. Both exact-Q sources replay forward and reverse. Nineteen hostiles reject. No Singular process, solve, coverage, or rep5 closure is claimed.
