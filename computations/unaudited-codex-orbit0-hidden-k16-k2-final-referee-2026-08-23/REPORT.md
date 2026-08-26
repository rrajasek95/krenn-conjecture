# Independent final referee: hidden-K16 K2 merge

## Verdict

**PASS.**  A new read-only 291-way merge replay consumed all `516,225,702`
retained child records and compared every nonzero aggregate, including its
minimal provenance witness, record-for-record against the two final
checkpoints.

The replay independently recovered:

- pivotable: `158,439,965` rows, scaled mass
  `724159651336720220160`;
- irreducible: `110,465,931` rows, scaled mass
  `1030607661835946557440`;
- cross-chunk exact zeros: `3,346`;
- total scaled mass: `1754767313172666777600`.

All chunk and checkpoint streams were strictly ordered.  The pivotability of
every merged row was recomputed from the 78 literal K0 signatures, with 230
distinct signature states, and agreed with the checkpoint split.  A
deterministic sample of 2,690 final witnesses was binary-replayed into the
101,545,723-record decorated-parent ledger; pair metadata, denominator,
literal K2 tail, and H-canonical landing all agreed.

Independent streaming SHA-256 gives:

- pivotable: `442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8`;
- irreducible: `c60fd9763d604f27213542a3bec9376849e046be06edf4e68035c849b097e111`.

One-weight hostile mutations change both digests and are rejected.  All 291
input chunks remain present; this audit performed no cleanup and launched no
K20 work.

Replay sources are `referee_final_merge.rs` and `finalize_referee.py`.
Machine result: `results_final_merge_referee_final.json`, logical SHA-256
`9b2ab638c40cb0145814e86e55520884abc9ef0ea55d80bb76174fe4b094bca2`.

