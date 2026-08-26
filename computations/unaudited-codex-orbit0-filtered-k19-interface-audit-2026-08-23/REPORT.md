# K19 recurrence/interface audit

K19 has four graded input buckets, split into seven signed source lineages:

| lineage | sign | pivot-depth | provider-level work |
|---|---:|---:|---:|
| direct `3+4+4` | - | 0 | 167,616,000 exact |
| direct K15 then K4 | + | 1 | 3,356,044,800 exact |
| direct K16 then K3 | + | 1 | combined below |
| K14/K2 to K16, then K3 | - | 2 | combined K16: 4,158,053,984 exact |
| direct K17 then K2 | + | 1 | K17 reconstruction required |
| K14/K3 to K17, then K2 | - | 2 | K17 reconstruction required |
| K15/K2 to K17, then K2 | - | 2 | K17 reconstruction required |

Here “exact work” means the compact operations at that provider's level.  The
K15 count is precollection source-pair work, while K16 is collected H-orbit
work; they must not be interpreted as a common literal occurrence measure.

The frozen K17 artifacts are insufficient for the last bucket: they retain
only nonpivotable K17 children and explicitly omit the pivotable parents whose
K2 tails first appear at K19.  The full source precursor streams contain
965,964,800 compact occurrences.  Using the two frozen irreducible counts
gives a rigorous upper bound of 731,799,040 pivotable precursor occurrences,
or 684,963,901,440 uncached K2-tail operations (78 pivots times 12 tails).

The convention is now reconciled: the requested polynomial is
`-R8' E0 E1 E2`, and reducing a head coefficient `c` emits `-c/m` per chosen
pivot.  Thus the K16 bucket is `direct - frozen`; the K17 lineages are direct
negative and both prior responses positive.  Applying the next reduction
produces the signs in the table.

Uniform exact integer scale `281801520^2 = 79412096674310400` suffices because
no K19 lineage has more than two pivot averages.  Even the hostile all-
collision bound has an i128 safety margin of 366,148.

The smallest sound continuation is a profile-only census/replay of the three
pre-filter K17 source streams.  Process them separately by linearity, caching
the anchor signature, outgoing pivot, labelled endpoint path profile, and
closed-cycle multiset.  First gate only the unique-key census at 180s/8GB;
do not collect K19 rows.  Result logical digest:
`eab84f53b5811a73d0646b7bb38cdabee0343a759b6271a241596ad6bf5bdb6b`.
