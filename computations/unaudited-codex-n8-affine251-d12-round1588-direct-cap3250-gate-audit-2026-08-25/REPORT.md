# Independent round-1588 direct cap-equivalence audit

Status: **PASS_EXACT_DIRECT_CAP3000_TO_CAP3250_EQUIVALENCE**.

The two producer lanes begin from the independently sealed round-1587 state
(`f8c33418...` checkpoint, `38a4ff6b...` cache; input audit
`f148d502...`, manifest `ba2235a3...`) and execute one round with the same
frozen source, binary, prime, cold/rare hierarchical configuration, 16
workers, 120-second native wall, 150-second watchdog, and 36-GiB RSS contract.
The normalized commands differ in exactly one argument:
`column_cap=3000000` versus `column_cap=3250000`.

Both outputs are round 1588 with 2,940,643 columns and dual support 5,029.
The independent audit read and hashed both 6,376,789,783-byte vector caches
and both 44,215,298-byte checkpoints.  They are byte-identical:

- checkpoint SHA-256:
  `e94a0965eb8d9a7bbb602726635093b9e0ca27a9d9af0ea38703a8bf3498d5b6`;
- vector-cache SHA-256:
  `c4ae2b91e86f4b373f078304d0d79416970bd636d97912b25eadc45c86428e05`.

The checkpoint header independently parses as prime 1,073,741,827, round
1588, 2,940,643 columns, and support 5,029.  Full result keysets and round
keysets are closed; after removing only the declared cap and measured timing /
RSS fields, the complete result objects agree.  The common round adds 13,629
columns and 3,257 support rows with the cold/rare choice.

Both watchdogs pass with return code zero, no breach, clean atomic outputs,
and no temporary or dual output.  Maximum wrapper elapsed time is 91.694039
seconds and maximum peak RSS is 23,434,048 KiB, below the frozen limits.  The
source, binary, watchdog, result, producer plan/result/report/manifest, input
seal, and compaction record are hash-pinned.  The compaction record SHA-256 is
`85b19435c78897bef899c28a71188983b46114fc24830fc142cbdba03d1018f7`.

The accepted restart is strictly
`candidate_cap3250/{checkpoint.bin,vectors.bin}` at the hashes above.  No
continuation beyond round 1588 was run or inferred.  The machine verdict is
`results_round1588_direct_cap3250_audit.json`, SHA-256
`199b17ef8c8ae718ff5644dd4cd0ecf63b1eb18fdb5663255783ca52539e1df5`.
