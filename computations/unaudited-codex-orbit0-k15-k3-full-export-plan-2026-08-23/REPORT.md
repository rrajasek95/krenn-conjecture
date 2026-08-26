# K15/K3 full profile-export plan (no full run)

## Verdict

`PASS_PLAN_ONLY`. The existing shared exporter is safe to run as independent
one-record shards with two workers and a one-million-key flush cap. Split the
485 records into two gated stages, `[0,242)` and `[242,485)`. Each accepted
record gets an atomic manifest and verified sorted parts; no full job was run.

## Exact workload and measured guard

All 485 frozen R8 records have the same anchor signature
`100100100100`. Consequently each record has exactly 3,690,496 generated K18
parents, 1,903,616 pivotable parents, and 4,861,952 outgoing K2-pivot uses.
The full totals are therefore exactly 1,789,890,560 / 923,253,760 /
2,358,046,720.

Four complete one-record probes (indices 0, 241, 242, 484) took
1.360–1.529 seconds of exporter time and emitted 13.66–55.86 MB each at a
one-million-key cap. The mean linear projection is 699.17 seconds on one
worker; the maximum-sample projection is 741.67 seconds. Two workers put each
half-stage near 185 seconds before command/catalog overhead, leaving ample
room under each 600-second gate. A failed RSS poll was discarded; the layout
probe instead gives 112 bytes per key/value tuple, and the conservative
hash-bucket-plus-sort core at the cap is about 0.35 GB per worker. Two workers
are far below the 16 GB gate.

## Exact two-stage execution plan

Stage 1 exports one-record shards 0–241: exactly 893,100,032 generated,
460,675,072 pivotable, and 1,176,592,384 outgoing uses. Stage 2 exports shards
242–484: exactly 896,790,528 / 462,578,688 / 1,181,454,336. Use a two-process
work queue, unique `record_NNN_attempt_M` prefixes, `PARENT_CAP=0`, and
`KEY_CAP=1000000`. Stop scheduling at 540 seconds and finish only the current
short shards before the hard 600-second gate.

A shard is accepted only if `complete_source_range=true`, every part passes
the exporter's reverse-tail/key verifier, and a stage catalog records all part
hashes. An orphan part without its manifest is ignored; retry under the next
attempt prefix rather than overwriting. Shared frozen inputs are read-only and
all worker outputs are disjoint, so two-way generation is race-free.

The set of verified sorted runs is a complete linear export. The eventual
scalar response consumer may evaluate each run independently and add the exact
subtotals; a global merge is unnecessary by linearity. If a globally unique
profile checkpoint is desired, that is a separate merge gate.

## Disk and symmetry

The exact pessimistic unmerged ceiling is 245,236,858,880 bytes (104 bytes for
every outgoing use), split 122,365,607,936 / 122,871,250,944 by stage. The
older prefix-ratio estimate is 34,987,181,424 bytes; the four complete-record
probes project 15,090,786,640 bytes. Provision 70 GB as the operational
estimate, but after stage 1 require at least 143 GB free before authorizing
stage 2 so even its hard ceiling plus a 20 GB margin fits.

Do not H-canonicalize the authoritative export. The order-384 action permutes
the three packet labels `223/232/322`, while the current grouped scalar key has
one aggregate weight and only one minimal witness packet—not a three-component
equivariant weight. H compression is safe only as a derived, explicitly
refereed quotient for an H-invariant grouped scalar response; it is not
source-faithful for the three individual IDs.

Exact machine-readable figures are in `results_k15_k3_full_export_plan.json`.
