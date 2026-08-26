# Full normalized Fh degree-12 CEGAR

## Terminal result

`BOUNDED_UNRESOLVED`: neither membership nor nonmembership is claimed.

The exact target-rooted invariant CEGAR completed rounds 0 through 22.  Its
last accepted interface has 355,170 canonical rows and 4,200 independent
admitted source-column orbits (rank 4,200).  The resulting 625-row functional
pairs nontrivially with the actual normalized `F^h`, but its exhaustive
incident scan finds 4,112 column orbits, including 2,048 new crossings.
Therefore it is not a full separator.

The next exact-Q solve was a monolithic call.  It returned at 369.13 seconds,
after the requested 300-second wall gate, and its output was discarded.  Peak
RSS was 2.21 GB, below the 12-GiB memory cap.  No rerun and no degree-13 or
saturation inference was made.

## Frozen interface

- Driver: `audit_fh_degree12_full_cegar.py`.
- Terminal record: `results_fh_degree12_full_cegar.json`.
- Round-by-round exact census: `run_ledger.txt`.
- Frozen root authority: logical digest
  `57a5bb5aa092a6edb79644be16f8b07908f8533b6c59e33e1ef4727771b6aad1`.

Every completed round used exact rational elimination.  Each dual was scanned
against every homogeneous degree-12 normalized source-column orbit incident
to its support; all violations were admitted in the next round.  The ledger
is a bounded progress certificate only, not an ideal-membership certificate.
