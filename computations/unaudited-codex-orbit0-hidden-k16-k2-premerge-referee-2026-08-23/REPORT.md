# Independent referee: full hidden-K16 K2 premerge

## Verdict

**PASS, scoped to the complete premerge state; the hardened driver is safe to
launch for the one 291-way merge.**  This is not yet a claim about the merged
K18 pivotable/irreducible checkpoints.

The referee independently checked all 31 exact-run headers and the disjoint
source interval `[0,485)`, the full decorated-pair ledger, all 291 child-chunk
headers and the exact interval `[0,101545723)`, and 873 nested literal child
witnesses (first/middle/last in every chunk).  The frozen totals agree:

- `75,691,040` hidden K16 parents and `511,477,120` second-pivot uses;
- `101,545,723` nonzero decorated pair H-orbits, coefficient mass
  `146230609431055564800` at `U=400591699200`;
- stabilizers `{1:99314228,2:2212958,4:16210,8:2099,16:224,32:4}`, with
  `orbit_size*stabilizer=384` for every pair record;
- `1,218,548,676` emitted K2 children, `516,225,702` within-chunk nonzero
  rows, and coefficient mass `1754767313172666777600 = 12` times pair mass.

## Resume and recovery safety

The shared validator now checks magic, scale, reserved/schema fields, exact
interval, raw count, record count, and byte size on both skip and merge paths.
The full pair scan restores strict key order, mass, and stabilizer histogram.
Hostile truncation, empty-histogram reset, and premature-cleanup tests all
fail closed; all 291 chunks remain after the cleanup hostile test.

The earlier eager deletion was corrected.  Normal merge retains every child
chunk.  Cleanup is a separate command requiring both validated final
checkpoints and an independent-referee marker containing their digests.
Therefore merge launch is accepted.

## Scope guards

Child chunks have no stored per-file content hashes.  Their provenance is the
atomic generator plus strict structural guards, and the merge must stream all
records before any later cleanup.  The 873 replayed witnesses prove literal
support landing, not a decomposition of each aggregate coefficient into all
raw occurrences.  The cross-chunk zero count and final K18
pivotable/irreducible counts, masses, and hashes remain unfrozen until merge.

Replay: `audit_premerge.py`; exact result: `results_premerge_referee.json`.

