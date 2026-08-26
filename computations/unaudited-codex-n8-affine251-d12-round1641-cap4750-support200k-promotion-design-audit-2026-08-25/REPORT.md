# Independent r1641 cap4.75m/support200k design referee

Status: **APPROVE_HELD_CAP4750_SUPPORT200K_ONE_ROUND**. No candidate clone, large candidate read, or launch was performed.

The independently sealed cap4.25m diagnostic is bound by result `d6b31a8c...` and manifest `edc643bb...`: unchanged audited r1640 input, zero rounds, and the exact lower bound `new_columns >= 180290`. The static source theorem confirms `column_cap` affects only serialization and the whole-next-set capacity guard after deterministic enumeration but before invariant-column materialization. Relative to the exhausted lane, the sole normalized command change is `--column-cap 4250000 -> 4750000`.

The declared shock policy is exact arithmetic but not a theorem: `ceil(180290*2*5/4)=450725`; with 4,069,711 input columns, the minimum policy cap is 4,520,436. Cap4.5m is short by 20,436; cap4.75m passes with 229,564 margin. Any larger actual frontier still fails closed without accepted coverage.

The 96-GiB preclone floor passed at design time but must be remeasured, together with all frozen hashes, immediately before a fresh r1640 clone. Acceptance requires exactly r1641/`ROUND_CAP`, no r1642, 4,069,711 inherited records byte-identical, a strict checkpoint descendant, full replay target 1 with zero failures, and atomic watchdog/resource PASS. `COLUMN_CAP`, `SUPPORT_CAP`, or resource failure remains zero coverage unless a separately audited exact atomic endpoint exists.

The producer plan's independent-diagnostic fields were null because it preceded the referee. This audit supplies those exact bindings; any launch record must pin both the producer design manifest and this audit manifest.
