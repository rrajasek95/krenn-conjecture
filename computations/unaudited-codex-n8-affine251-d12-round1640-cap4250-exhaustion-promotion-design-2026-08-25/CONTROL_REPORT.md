# Cap-4.0m exhaustion control

Producer verdict: `PASS_PRODUCER_LOWER_CAP_EXHAUSTION_WITNESS`.

The exact audited round-1639 state was cloned and run under cap 4,000,000 with
round cap 1640. The frozen engine returned `COLUMN_CAP` at round 1639 with no
round-1640 record: 3,968,369 columns, support 32,704, and all 3,968,369 cached
vectors loaded. The checkpoint and cache hashes are byte-identical to the input;
there were no temporary files. The hard watchdog passed atomically in
72.368616 seconds with peak RSS 20,924,976 KiB.

Together with the independently approved static source theorem, this is the
required lower-cap exhaustion witness: the complete deterministic next incident
set does not fit in the remaining 31,631 slots, and the engine returned before
column arithmetic without changing the accepted state.

The cap-4.25m candidate directory remains absent. Candidate launch is forbidden
until an independent control referee confirms this witness and the manager gives
explicit clearance.
