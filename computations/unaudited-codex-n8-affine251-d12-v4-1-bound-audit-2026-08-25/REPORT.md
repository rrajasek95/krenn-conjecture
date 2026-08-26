# Independent v4.1 round-cap bound audit

Verdict: `PASS_EXACT_V4_1_ROUND_CAP_BOUND_PATCH`.

The source diff is exactly one byte-level semantic edit: `round_cap > 1000` becomes `round_cap > 10_000`. Every other source byte is unchanged, so persistence schemas, rare-index logic, recurrence, modes, and fallback guards are inherited exactly from promoted v4. Source is pinned at `3139689f...`, binary at `79410bc8...`, and the unchanged index schema at `abc718ee...`. The hostile `round-cap=10001` rejected, while the original v4 refusal at cap 1060 remains preserved with no result.

Matched round-960 clones were advanced exactly once to round 961 by v4 and v4.1. Their final checkpoint and vector cache are byte-identical (`2fac10fb...`, `8bce26ef...`), with 577,645 columns, 1,244 new columns, and support 523. A fresh canonical `(frequency, Mono)` audit matched the incremental index on all 32,534,680 rows, order SHA `a8a82bda...`. Independent replay checked all 58,743,477 cached terms, target normalization, and zero pairing failures.

Both watchdog-v2 records passed with atomic outputs and no breach under 36 GiB. This audit authorizes the parser-bound patch only; it does not itself certify any continuation beyond round 961.
