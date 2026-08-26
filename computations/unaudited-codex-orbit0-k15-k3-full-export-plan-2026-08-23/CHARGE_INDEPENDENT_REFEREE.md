# Independent referee: K15/K3 grouped K20 charge

`PASS` for the exact grouped subtotal `D15:{223,232,322}|R:3-2`.
This is not a certificate for three separately identified charges: the merge
summed packet weights at equal profile keys and retained only the least witness,
so the individual packet scalars are genuinely unrecoverable and correctly
remain `null`.

The count and mass identities replay exactly at
`U=400591699200`: `306772692 = 12*25564391` profile tails,
`27742646256 = 12*2311887188` source occurrences, and
`22381186445623060070400 = 12*1865098870468588339200` signed
coefficient mass.  The reported irreducible counts are bounded by their full
counts.  The scaled full and irreducible cycle charges are respectively
`1505666730204685762560` and `1461387462129632378880`, or
`1697405675284864/451605` and `1647487669247872/451605` after dividing by
`U`.

The sign is consistent with the filtered recurrence.  A K15 head contributes
`+rho*U/m1` at K18; cancelling a pivotable K18 parent contributes
`-rho*U/(m1*m2)` to each K20 K2 tail.  That signed value is what the merged
record stores, and the evaluator multiplies it exactly once by the literal
12-tail cycle charge.  A child is classified irreducible precisely when its
literal response signature has no available K0 pivot.

An independent checker sought 256 distributed records in the merged binary,
reconstructed their rows, signatures, profiles, denominators and all 12 K2
children, and reproduced every full charge, irreducible charge, and
irreducible-tail count.  The packet census was `118/37/101` for
`322/232/223`, confirming the exact mapping `packet0=322`, `packet1=232`,
`packet2=223`; this validates the group label but does not undo aggregation.
The producer's exhaustive 25,564,391-key guards remain independently supported
by the previously passed full 485-way byte replay.

All 485 input parts (242 stage1 and 243 stage2) and the 2,658,696,792-byte
merged checkpoint remain present.  No producer inputs were cleaned, no full
charge run was duplicated, and no K21 tails or rows were generated.

Artifacts:

- `results_k15_group_charge_independent_referee.json`
- `audit_k15_group_charge_samples.rs`
- `results_k15_group_charge_sample_referee.json`

