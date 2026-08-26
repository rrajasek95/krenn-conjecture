# Independent r1641 support-cap promotion referee

Status: **APPROVE_HELD_SUPPORT200K_DIRECT_PROMOTION**. No clone, large endpoint read, or arithmetic launch was performed.

The frozen source has seven `support_cap` tokens on six lines and exactly two `config.support_cap` reads: result serialization and the sole semantic guard `next.len() > config.support_cap`. That strict guard occurs after new-column materialization, elimination/backsolve/verification, and deterministic next selection, but before `candidate=next` and round commit. Thus the normalized 100k-to-200k change affects admission only; all provider, ordering, elimination, solution, resource, column-cap, and round-cap fields remain byte-pinned.

A low-cap control is not necessary. It would perform nearly the whole round and, if exhausted, write a hybrid clone with extended columns/cache but the old candidate and round. It cannot establish byte equivalence and must never be resumed. Static single-use proof plus a fresh 200k candidate, strict inherited-byte/descendant validation, and full all-column replay is the sound contract.

The resource projection is exact arithmetic but not a growth theorem: `76616 + ceil(43912*5/4) = 131506`, leaving 68,494 below 200k. Acceptance requires only r1641, `ROUND_CAP`, no r1642, all 4,069,711 inherited records byte-identical, a strict checkpoint descendant, normalized target 1 with zero replay failures, atomic watchdog/resource PASS, and an independent postrun seal. Any `SUPPORT_CAP` output is quarantined zero-r1641 evidence; `COLUMN_CAP` remains its distinct pre-arithmetic unchanged-input outcome.
