# Referee — smallest rep5 open84 modular pilot

Verdict: **PASS held approval only; no launch**. All six open84 sources tie exactly on bytes, generator count, and factored operator count. The frozen source-SHA tiebreak uniquely selects `k=2,t=1` (`Q 1e2f72c9…`).

The p32003 source (`fd182135…`) reverses byte-for-byte to the selected Q source after the sole ring-characteristic substitution. It parses as 84 variables / 6,562 generators, and the complete `slimgb`, unit-reduction, and status epilogue is preserved.

Runner `e459c779…` enforces a fresh libproc process census, process-group RSS, 300/315-second and 8-GiB limits, single-use markers, and one atomic terminal result. The v2 producer/referee and consumed k0 timeout are pinned; neither old k0 source is reused.

The approval remains only in this referee package. The held producer has no acceptance, clearance, attempt, or result, so execution remains impossible until a new explicit clearance workflow.
