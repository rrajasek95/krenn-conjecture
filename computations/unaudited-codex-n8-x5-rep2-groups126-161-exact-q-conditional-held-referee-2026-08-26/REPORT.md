# Rep2 final groups126–161 conditional held-package referee

Verdict: **PASS / CONDITIONALLY HELD / ZERO RUNS**.

All 36 exact-Q sources for canonical groups126–161 were independently rebuilt
from authoritative census `5ee661f3...`.  They match ledger `c34b3616...`
byte-for-byte, total 66,529,596 bytes, with 91 variables and 6,577 generators
each.

The three required terminal pairs—groups1–25, groups26–75, and groups76–125
v2—are all null and all six referenced artifacts are absent.  Verifier
`b784729f...` requires exact manifest replay, result membership, top-level
hashes, terminal schemas/statuses/group lists, and duplicate-free union0–125.
Independent mutation replay matches all 21 packaged hostile rejections,
including a fabricated/stale normalized record whose plausible hashes cannot
substitute for the absent six artifacts.

Runner `07281312...` invokes that full six-artifact replay before its exclusive
attempt marker and sole process launch.  It is strict sequential stop-first
with 240/250-second and 8-GiB group-libproc gates; skip/reorder/relaunch/parallel
execution is forbidden.  No normalized dependency, acceptance, clearance,
attempt, result, temporary, or solver artifact exists.  This held seal adds no
mathematical coverage.
