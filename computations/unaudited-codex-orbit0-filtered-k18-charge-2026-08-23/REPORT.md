# Exact K18 charge-only referee

The four frozen recurrence components were streamed through the 77-cycle
functional without collecting K18 rows.  The exact component charges are:

| component | full occurrences | irreducible occurrences | full charge | K18-irreducible charge |
|---|---:|---:|---:|---:|
| direct | 152,251,200 | 14,433,600 | -272,994,816 | -95,224,320 |
| K14/K4 | 397,156,800 | 39,576,000 | 502619274240/4301 | 2000304128/35 |
| K15/K3 | 1,789,890,560 | 866,636,800 | 278243265136128/150535 | 7884015145472/6545 |
| K16/K2 | 1,559,270,244 | 751,770,626 | 830890978048/385 | 617636790784/385 |
| **total** | **3,898,568,804** | **1,672,417,026** | **82802576789248/21505** | **2590664898048/935** |

The cache key is theorem-sound: after deleting the pivot anchor it retains
the eight labelled path endpoints and path lengths plus the closed-cycle
multiset, so each fixed tail determines the child cycle partition.  The
separate 12-anchor signature determines whether that child is still K18
pivotable.  Thus the rightmost column is the exact charge after deleting all
K18-pivotable children, not a sampling estimate.

Compact-level guard: 44,342,881 is the collected K15 H-orbit pivot-use count,
whereas 55,934,080 is the precollection source-pair count used by this
source-linear stream.  The resulting 1,789,890,560 K3 evaluations are exact
for this implementation, but totals across the table mix compact levels and
are engineering counts, not a common literal census.  K17 cannot feed K18
because every pivot tail raises K by at least two.  Scope remains charge-only:
no K18 residual collection and no ideal-membership claim.

Replay hardening: the frozen run omitted one explicit K15 remainder assertion
and two auxiliary magic-header checks.  The scale is the audited LCM and all
input hashes are pinned, so this does not change the exact charge verdict.

Replay with `finalize_k18_charge.py`; the frozen logical digest is
`da7f6ccc7638621ca7f13213d40be7e8afe2c38decb3663efbdb1f4ea3408413`.
