# Packed complete-closure production sibling: D10 terminal, D11 closure-only

Status: **D10 PASS; D11 closure-only PASS and full-degree NONPROMOTION. No D12 run is authorized.**

## Provenance and implementation

This package was cloned from the restored original `affine251` source at SHA-256 `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`. The parent package was not edited.

`src/main.rs` is the later promotion candidate. It changes only the complete-closure expansion path:

- workers emit naturally ordered fixed-degree `u128` row/column keys into contiguous vectors;
- eight/worker-count chunks sort in parallel and an exact k-way merge deduplicates them;
- unpacked keys still enter the inherited persistent closure `HashSet`, and the inherited checkpoint writer supplies the authoritative natural sort;
- row canonicalization can claim one process-global, 10,000-candidate probe for a 400,000-entry orbit memo. It enables only at >=90% hit rate and globally falls back to the inherited exact-input cache otherwise;
- sub-10k worker chunks use the inherited exact cache directly;
- the linear-membership and dual-construction path is inherited unchanged;
- `getrusage` enforces and reports the live RSS cap when sandboxed `ps` is unavailable.

The exact source of the completed D11 control is preserved as `src/main_repeated_probe_control.rs`, SHA `b42a41e97e52117c2d115fe253c3a620c94e52fa41c34d34ebd7dd9367dda60f`. It predates the process-global probe fix and is retained solely to pin that result's provenance. The promotion candidate is SHA `7a2f5e6c23535e005ac4a6ebc63c50d35a57dedc173103b1c120a8dff9afa628`.

## D10 exact terminal equivalence

The final promotion-candidate binary ran a fresh D10 closure and the full degree computation under 300s/8GiB.

- closure: 36,475 rows, 2,120 columns, complete;
- checkpoint SHA `2a05d97ce8d58d9d25ac8fddd01eba2ff87b2367949f6d573c0923ea653e4fa2`, byte-identical to the retained checkpoint;
- rank 2,014; matrix NNZ 101,283; target residual NNZ 1; target pairing 1; nonmember modulo 1,073,741,827;
- dual SHA `27b47b61238044c739daa5941ad80782d249cdea4e115e07043472b507eb0d87`, byte-identical to the retained dual;
- elapsed 2.015005s, peak RSS 179,648KiB, versus retained result 8.142970s / 158,432KiB.

The wall comparison is not claimed as a paired cold benchmark because the retained run's checkpoint-start state is not recorded. It does show that the optimized fresh run is comfortably bounded. D10's chunks were below the memo-probe threshold, so this is a packed-collector equivalence result (`memo_probe_candidates=0`).

## D11 exact closure-only result

The completed cold D11 process reached the exact terminal closure at 193.718s, then entered the unchanged matrix phase. The 295s live gate stopped it atomically before a linear result:

- complete closure: 3,722,556 rows and 195,924 columns;
- authoritative checkpoint `closure_d11_repeated_probe_control.bin`: exactly 51,332,134 bytes and SHA `2d9c7b2907b813834ed226c258a7f681fdd6cb8836cff9ad74c148eb1e76ef6f`;
- the retained parent checkpoint has the same size and SHA and passes bytewise `cmp`;
- process terminal status `INCOMPLETE_RESOURCE_GATE/WALL_CAP`, elapsed 295.144301s, peak RSS 1,650,000KiB;
- rank, matrix NNZ, residual, pairing are all `-1`; membership is `null`; no D11 dual was produced or accepted.

The repeated-probe source tested 4,000,000 candidates across 400 worker-local probes and observed only 401,088 hits (10.03%); it enabled zero workers and fell back all 400 times. This implementation is therefore not promotable despite exact closure output.

The process-global fix was compiled and passed the exact D10 result. A D11 follow-up had already begun when the stop instruction arrived; it was interrupted immediately after round 6. Its partial checkpoint is explicitly quarantined at `interrupted_global_probe_gate/closure_d11_round6.bin`, 26,106,037 bytes, SHA `ba6219b5c99c0caa39798113bbb6cfef1667833918af3e63a32a37e29d88dc28`. Its 10.664s round-6 checkpoint is diagnostic only and is not a D11 equivalence result.

There is no retained cold baseline phase timing that isolates original D11 closure construction, so the 193.718s closure time cannot support a speedup claim. The retained full D11 result/dual remain authoritative for the degree computation.

## Verdict

- The packed implementation is ready for a later bounded integration review based on terminal D10 equivalence.
- The conditional memo remains exact but has no accepted production benefit on D10/D11: D10 never probes, and the completed D11 control rejects it.
- D11 validates closure semantics only. It does not validate a new degree result or dual and does not justify promotion for full D11.
- No D12 closure, warm linear pass, or other broad run was launched.

`audit_equivalence.py` pins the sources, binary, input, checkpoints, results, and scope. Ten hostile mutations, including a complete/partial checkpoint swap and false D11 linear acceptance, are rejected.

