# Rep1 next50 normalized-dependency superseding held package

This package repairs only the next25 dependency interface rejected by the binding audit manifest `18e93f3a...`. The sealed next25 terminal result correctly provides `groups_closed` but has no `closed_union` field. The adapter now derives that field from the independently sealed baseline groups `0..10,13,15` and terminal groups `11,12,14,16..37`, proving a disjoint 13+25 union exactly equal to `0..37`.

The adapter pins the baseline referee, next25 terminal referee, and satisfied-binding audit manifests and results. It verifies manifest membership before normalization. Twelve exact hostile tests reject missing, duplicate, extra, overlapping, reordered, skipped, wrong-status, and wrong-binding inputs. Its normalized output supplies the exact four-field projection that the superseded runner intended to consume.

All 50 group `38..87` sources and the source ledger are byte-identical to the superseded package. Runner v2 preserves the strict order, 240/250-second per-lane gates, 8 GiB direct-libproc process-group RSS, atomic results, stop-first behavior, and no skip/reorder/relaunch/parallel policy.

This is still a zero-run held package. A new independent acceptance and explicit clearance are absent and mandatory; no attempt, result, or solver run exists.
