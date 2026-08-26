# Held v2 cap-exhaustion promotion contract

Status: `HELD_AWAIT_R1639_AUDIT_COMPACTION_AND_INDEPENDENT_CONTRACT_APPROVAL`.
No endpoint clone, large read, or arithmetic was performed.

This is deliberately not a byte-equivalence gate. The cap-4.0m control must
return `COLUMN_CAP` at round 1639 before column arithmetic and leave its input
checkpoint/cache byte-identical. A fresh cap-4.25m candidate may then run under
an otherwise identical command and must reach exactly round 1640 atomically,
preserve all 3,968,369 inherited cache records byte-for-byte in canonical order,
and pass a full cache replay with normalized target pairing 1 and zero failures.

The frozen-source static audit is PASS. `column_cap` occurs six times: field,
parse, validation, config construction, result serialization, and the one
runtime capacity guard. The only two `config.column_cap` reads are serialization
and the guard. The guard follows exact incident enumeration/sorting and precedes
invariant column arithmetic, ranking, elimination, backsolve, and verification;
its failure branch writes the unchanged state and returns. Four hostile source
mutations were rejected by the checker.

Under these hypotheses, candidate promotion is exact because raising the cap
admits the same deterministic whole next set that the lower cap rejected; it
does not alter enumeration or arithmetic. Independent audit must approve this
proof contract before either run and must independently verify the candidate
descendant scan and full replay. No continuation is authorized here.
