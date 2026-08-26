# N6 full-`P^2` filtration: exact lower contraction and first possible core

Status: **bounded exact theorem-shape audit.**  This report neither proves nor
disproves `P^2` membership in the full arbitrary-matrix ideal.

## Outcome

There is now an exact coefficient-aware contraction of the full target through
K-degree three.  A frozen triangular certificate uses 9,528 literal
`S6 x S3` orbit columns.  Its pivot diagonals are `1` 9,409 times and `2` 119
times, so back-substitution proves

```text
P^2 in I + K^4  over Q (indeed over Z[1/2]).
```

The well-founded statistic is the **relative collapse height** supplied by the
pivot ledger: give a row the index at which it is appended.  The pivot column
for that row has, among outputs of K-degree at most three, only the pivot row
and rows of smaller height.  Back-substitution is therefore a contracting
homotopy.  This is coefficient-aware, not a support-only matching argument.

Consequently a characteristic-zero exponent-two obstruction cannot first
occur in K-degrees zero through three.  The first possible target-relevant
relative `2`-core is at K-degree four.

## Frozen global certificate

The certificate
[cutoff3_dfs.txt](../unaudited-codex-p2-k6-global-2026-08-23/cutoff3_dfs.txt)
has SHA-256
`4985027e5f91bb462960f3e3dcd3c77edd181bc9e8ace1d938c7b506ff974222`.
It starts from 663 exact target row orbits in seed SHA-256
`2c425920e4f803272361100c2bcd22c758c47ff09328b96855d8421a0e1fe37b`.
The pivot K-degree census is

```text
degree 0:   868
degree 2: 7,421
degree 3: 1,239
```

Every pivot row and pivot column is distinct.  The producer replays every
literal matching output and checks triangularity before writing the ledger;
this audit independently freezes the hashes, header, distinctness, degree
census, and diagonal coefficients.

A producer checkpoint also reports that the entire target-rooted closures
have empty singleton-peel cores at cutoffs two and three (respectively
76,987/637,696 and 543,640/4,424,353 row/column orbits).  Those full-peel
counts remain non-load-bearing here until their peel JSON/pivot provenance is
packaged.  The 9,528-pivot DFS ledger above is the load-bearing target
contraction.

## What happens at frozen K-degree six

The prior coefficient-aware `p=1009` lower lift was replayed unchanged and its
degree-six remainder was serialized.  It contains 366,992 nonzero row orbits:

```text
rainbow-cone rows        189,182
noncone rows             177,810
dead coordinate rows           0
one-incident-column rows       10
maximum incident degree        38
```

Thus there is no coordinate separator in this selected K6 lift.  The easy
lex-first `420` leaf has an exact integral homotopy: 36 noncone dependencies
and 45 rainbow-cone corrections give an 81-column identity with coefficients
only `+/-1` (certificate SHA-256
`d56070190ae143360aacf6c93d21f97ffcced4723490042dc3ef0107f0c50bd2`).

The first local escape is the lex-first `330` fan.  Its literal relations are

```text
C330 = T + 2B + 2C + 2D + E + F,
C321 = C + D + E.
```

On the frozen remainder, eliminating `T` leaves

```text
284(B+D) + 142(E+F)  in F_1009.
```

No correction confined to the six-row fan can leave fewer than four live
arms, while the projections of all eleven incident columns have rank six over
`Q`.  Hence the fan has no locally supported dual: a negative class must
propagate outward, and a positive contraction must use external columns.

## Literal-provenance guard

The K6 fan is **not** literally killed by the cutoff-three certificate.  Its
rows and source columns have K-degree six, whereas every cutoff-three pivot
has degree zero, two, or three.  The truncated producer deliberately omits
outputs of degree at least four.  There is therefore no fan row/pivot match
and no sound multiplication or symmetry transport from the fixed fine-degree
cutoff-three ledger to this fan.

The lower certificate only changes the global interpretation: the four-arm
fan is the first *local K6 escape* of one modular lift, not the first global
unresolved filtration object.  The precise smallest unresolved layer is K4.
The next decisive test is the target-rooted cutoff-four-to-six relative core;
at K6 it must either give literal external pivots contracting the four arms or
an exact rational dual that also annihilates all lower-filtration kernel
transfers.

## Replay

```sh
.venv/bin/python computations/unaudited-codex-n6-p2-degree6-relative-incidence-2026-08-23/audit_degree6_relative_incidence.py --check-results
.venv/bin/python -O computations/unaudited-codex-n6-p2-degree6-relative-incidence-2026-08-23/audit_degree6_relative_incidence.py --check-results
.venv/bin/python -I -S computations/unaudited-codex-n6-p2-degree6-relative-incidence-2026-08-23/audit_degree6_relative_incidence.py --check-results
```

The hostile mutation changes the four-arm minimum and is rejected.  Result
logical digest:
`4b598330430c12fac07b68d864a09729ab1130d96984837aebf6a922c561b2a4`.
