# K15/K3 full signed profile merge

`PASS`. After independent acceptance of both producer stages (logical digests
`256bc673…` and `9498eec9…`), the 485 locally sorted parts were merged in
59.292303 seconds. The output checkpoint was atomically renamed only after all
input headers, lengths, source indices, strict key orders, witness pivots,
denominators, use counts, and signed masses reconciled.

The merge consumed 202,344,547 local records, 2,358,046,720 uses, and signed
scaled mass `1,865,098,870,468,588,339,200`. It produced 25,564,391 globally
unique nonzero profiles with 2,311,887,188 uses and the identical mass.
Exactly 1,411,149 profile groups canceled to zero, carrying 46,159,532 uses.

The 2,658,696,792-byte atomic checkpoint is
`checkpoint_k15_k3_profiles_merged.bin`, SHA-256
`8b05f3fb8edcda062111d20089309abb85d4ccd8675d289947178b437139c1db`.
An independent local output streamer rechecked all 25,564,391 records and EOF.

The initial preflight saw the default 256-file soft limit and stopped before
creating any temporary/output file or processing a row. The clean run used a
process-local limit of 1,024 (hard limit unlimited). This is not a partial-run
continuation.

All 242 stage-1 and 243 stage-2 parts remain present. No K2 charge evaluation,
cleanup, K16 work, or other downstream operation ran.
