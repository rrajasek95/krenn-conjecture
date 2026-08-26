# Independent referee: K15/K3 485-way signed merge

## Verdict

**PASS.**  The 485-way signed merge is byte-for-byte correct.  The referee
recomputed the complete merge from every retained stage-1 and stage-2 part,
compared every surviving output record, and independently reproduced every
exact-zero group and use count.  No charge evaluation, cleanup, K16 work, or
new producer run was performed.

## Full stream replay

The referee opened all 485 parts under a process-local 1,024 descriptor limit,
rechecked each input header, length, source witness, strict local key order,
nonzero signed weight, positive uses, outgoing pivot, denominator, and packet
label, then performed a fresh key-ordered signed merge.

For every nonzero group, the entire expected 104-byte record—key, summed
weight, summed uses, and lexicographically minimal 38-byte literal witness—was
compared with the checkpoint.  The replay reached exact EOF with:

| quantity | value |
|---|---:|
| input parts | 485 |
| input records | 202,344,547 |
| input uses | 2,358,046,720 |
| input scaled mass | 1,865,098,870,468,588,339,200 |
| output records | 25,564,391 |
| output uses | 2,311,887,188 |
| output scaled mass | 1,865,098,870,468,588,339,200 |
| exact-zero groups | 1,411,149 |
| exact-zero-group uses | 46,159,532 |

Thus output uses plus zero-group uses equal all input uses, and signed mass is
conserved exactly.  The full replay took 117.765961 seconds.

## Hash, order, and gate

The 2,658,696,792-byte checkpoint SHA-256 is
`8b05f3fb8edcda062111d20089309abb85d4ccd8675d289947178b437139c1db`.
The producer's independent output streamer and this referee both confirm
strict global key order, nonzero output weights, positive output uses, valid
denominators, and EOF.

The clean producer merge completed in 59.292303 seconds under its 600-second
gate.  The initial 256-FD preflight stopped before creating a temp/output file
or reading a row; the accepted run was a fresh 1,024-FD launch.  All 242
stage-1 and 243 stage-2 source parts remain present, and no merge temp file
remains.

Artifacts:

- `audit_k15_merge_full_stream.rs`
- `results_k15_merge_full_stream_referee.json`
- producer result `results_k15_k3_profile_merge.json`
- merged checkpoint `checkpoint_k15_k3_profiles_merged.bin`
