# D12 r1641 support-cap promotion design — HELD

Status: **HELD_AWAIT_INDEPENDENT_SYMBOLIC_REFEREE_AND_EXPLICIT_MANAGER_CLEARANCE**. No large endpoint read, clone, lower-cap control, or candidate arithmetic has occurred. The prior support100k r1641 plan (`e32a0a3...`) is pinned but must not be launched.

## Static theorem

The frozen source `3139689f...` contains seven `support_cap` tokens on six lines plus one CLI flag literal. There are exactly two `config.support_cap` reads: result serialization and the sole semantic guard, `if next.len() > config.support_cap`. The guard runs only after new columns and invariant vectors are materialized, frequencies are updated, elimination/backsolve/verification completes, and a deterministic `next` is selected; it runs before `candidate=next` and the round increment. No provider, column arithmetic, ranking, elimination, verification, or choice logic reads the cap.

Consequently, increasing the literal preserves the provider and mathematical computation of `next`. But a lower-cap control is not byte-unchanged: before `SUPPORT_CAP` returns, the clone's columns and vector cache have already been extended, while the candidate and round remain old. Such a result is a hybrid, non-resumable diagnostic. It could witness exhaustion only in a quarantined fresh clone, at nearly full-round cost, and adds no valid byte-equivalence proof. This design therefore forbids the lower-cap control and uses a direct source-theorem plus strict-descendant/full-replay contract.

## Derived cap

r1640 support is 76,616 and the previous growth was 43,912. The one-round conservative growth is `ceil(43912*1.25)=54890`, giving an inclusive minimum cap of `76616+54890=131506`. Equality is admitted because the source guard uses strict `>`.

The selected cap is 200,000. It deliberately leaves 68,494 rows beyond projected support; the smaller 150,000 round-number choice would leave only 18,494. Raw input headroom is 123,384. The cap literal does not preallocate memory or broaden the provider; it only admits the already-computed candidate. Although two projected support increments would fit under 200k, r1642 remains forbidden because the separate column-headroom contract supports only one projected round.

If independently approved and manager-cleared, a single fresh r1640 clone may run with support200k, cap4.25m, exact r1641, native210/wrapper240/RSS36, and otherwise frozen cold/rare/hierarchical/16/nonincremental settings. Acceptance requires atomic `ROUND_CAP` at exactly r1641, no r1642, all 4,069,711 inherited records byte-identical, a strict checkpoint descendant, and full replay target 1 with zero failures. Any `SUPPORT_CAP` output is zero coverage and a quarantined hybrid; any other unplanned status is held for a new referee.

Free space was 153,585,356KiB at design time, above the 88,080,384KiB floor, but it must be remeasured and the r1640 input rehashed immediately before any authorized clone. No payload is eligible for deletion before exact enumeration and explicit authorization.
