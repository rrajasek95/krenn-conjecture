# The full squarefree rectangle orbit closes; multiplicity two does not

## Outcome

The fourteen unaligned support-eight circuit classes admit no packet in the
natural source-provenant `K2,4` rectangle orbit.  This is true for both sharp
star orientations.  Permuting the canonical nineteen-cell rectangle through
all six residual sites gives 180 distinct supports, twelve above each omitted
perfect matching.  For either sharp star pattern the exact full-fibre census
is

| omitted matching relative to `F0=01|24|35` | supports | verdict |
|---|---:|---|
| disjoint | 96 | missing a required pure response target |
| shares one edge | 72 | missing a required pure response target |
| equal | 10 | missing a required pure response target |
| equal | 1 | two forbidden singleton coefficients |
| equal | 1 | semantic support, but shared-two-zero-fan unit |

Thus every one of the 180 supports is excluded coefficientwise or before
coefficients.  In particular, all `6+8=14` unaligned squarefree circuit
classes close on this complete relative rectangle lift.

The exact checker is
`computations/verify_n8_one_bad_relative_rectangle_orbit_closure.py`.

## What “relative” retains

The site permutation acts on every endpoint-ordered decorated cell but does
not move the selected star rows.  Hence it retains the load-bearing
difference between an abstract `S6` orbit and its position relative to the
fixed response holes.  Every support determines a unique omitted perfect
matching, and each of the fifteen matchings has twelve source-labelled
rectangle orientations.

The checker expands the entire six-site top tensor and all four response
rows, not only the eight abstract incidence terms.  It requires support for
all three desired coefficients and records every forbidden singleton
row-word label.  Endpoint colours and endpoint order are never collapsed.

## Why the unaligned classes die immediately

When the omitted matching is not `F0`, the permuted rectangle moves at least
one of the two diagonal carrier pairs away from the fixed star complement.
The full source expansion then has no monomial at one of

\[
              [q^{[3]}]_{a^6},\qquad
              [p_b s_bq^{[2]}]_{b^6},\qquad
              [p_c s_cq^{[2]}]_{c^6}.                 \tag{1}
\]

This is stronger than a mixed singleton: no choice of nonzero weights on
that support can create the missing target coefficient.  The exact census
shows it for all 168 unaligned supports per sharp star orientation.

## The aligned twelve

Ten aligned orientations also miss a target coefficient.  One orientation
supports all three targets but leaves two forbidden singleton fibres.  The
last orientation has the canonical sixteen-cell binary rectangle and a
three-cell pure top matching.  The two sharp star patterns can select different
pure top matchings here, but their binary cells are identical.  Every forbidden
live fibre is double, so support uniqueness cannot kill this orientation.  Its
binary coefficients are nevertheless impossible by the already proved tensor
equations

\[
 T_{24}=E_{bb},\qquad T_{35}=E_{cc},\qquad
 T_{23}=T_{25}=T_{34}=T_{45}=0.                        \tag{2}
\]

Any adjacent pair of zero tensors in (2) is a shared two-zero fan and gives
the unit ideal over `Q`.  Since this ideal uses only the sixteen binary cells,
it closes the sole semantic support for both star orientations independently
of which pure top matching they carry.

## Multiplicity-two is a different provenance problem

The thirty support-eleven circuits are replayed as one `S6` orbit.  Each has
one primitive coefficient of absolute value two and ten of absolute value
one.  Expanding multiplicity gives six exchange moves on each side.

Both sharp star patterns have the same unordered debt datum
`{01,24,35}` (they differ only in the order of the second response holes).
Consequently the doubled matching has, for each star pattern, the exact
relative split `equal/share-one/disjoint = 2/12/16`.

A literal hafnian coefficient contains a fixed decorated perfect-matching
monomial once.  Therefore the doubled matching in a support-eleven circuit
must be reused by two source-labelled exchange moves; it is not a squarefree
single-fibre rectangle packet.  Permuting the nineteen-cell squarefree
support cannot test it.

The precise remaining datum is now smaller than “all even circuits”: one
needs two row-word grades sharing the doubled matching and a translated-
target identity coupling those grades.  No coefficient feasibility or unit
is claimed for that repeated-provenance orbit here.

## Scope

This theorem closes the full site-permutation orbit of the canonical
source-provenant rectangle lift.  It does not prove that every possible
cross-word decoration of an abstract support-eight incidence circuit reduces
to that lift.  Such a reduction would itself be a source-provenance theorem.
The multiplicity-two orbit remains explicitly open for the reason above.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_relative_rectangle_orbit_closure.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_relative_rectangle_orbit_closure.py
```

Both modes freeze the ledger hash printed by the checker.
