# Held 16-GiB D11 triangle resume

## Verdict

`READY_HELD`: the smallest exact resume gate is frozen and clearance-gated. It uses the independently replayed 94,526-column / 13,116-support checkpoint, the same prime `1073741827`, provider, branch, column cap, and arithmetic as the sealed recovery. No arithmetic was launched, no D12 cache was read, and neither `CLEARANCE.json` nor a production output directory exists.

The source is an exact copy of the sealed recovery source with two audited operational changes: its native wall guard is reduced from 590 to 350 seconds, and the final checkpoint writes the dual before the selected set, matching the already-safe periodic order. There are no arithmetic or provider changes. The watchdog is an exact resource-only specialization from 12 GiB / 600 seconds to 16 GiB / 360 seconds. Source, binary, watchdog, provider, checkpoint, prior telemetry, and prior production manifest are SHA-pinned. The engine selftest passes, and the launcher was hostile-tested to refuse execution without explicit exclusive-slot clearance.

## Checkpoint-first persistence

The new package owns immutable copies of the accepted restart pair before a future output directory is created. Its audit records target coefficient 1 and zero failures over all 94,526 selected-column pairings. During a future run, the unchanged engine atomically renames the dual before the selected file; any visible output pair is therefore safe, and resume replays the whole selected subset. If the process dies before its first new output, the sealed input pair remains intact.

## Bounded geometry and expected value

The prior 12-GiB lane stopped at 255.670974 seconds and 12,626,848 KiB with no terminal result, but it left the accepted checkpoint. A deliberately crude time-proportional extrapolation reaches 16 GiB at 340.894632 seconds. The frozen 350-second native / 360-second wrapper limits are therefore sized to measured growth, with only 9.105368 seconds between the projected RSS point and native wall.

Useful progress is plausible but not guaranteed. Rebuilding the 94,526-column basis and completing at least one new incident-scan/repair round must fit inside the gate before a strictly newer checkpoint can land. The pivot geometry is rebuilt at resume time and can be nonlinear. This is a bounded restart-progress attempt, not a projected terminality run; failure without a newer pair does not invalidate the preserved input.

## Compression verdict

Support/incident compression is promising but rejected for this resume because exact equivalence is not yet gated. The separate design in `COMPRESSION_ASSESSMENT.md` uses comparator-ranked row interning, compact sparse rows, exact `u128` columns, and optional provider rematerialization. It must first pass 1,000/5,000-column candidate, support, order, and literal pairing equality with a material memory or throughput win.

## Future clearance

Only after an exclusive slot is explicit, create `CLEARANCE.json` containing the exact schema, this package's manifest SHA, and boolean `exclusive_slot`/`launch` fields required by `run_resume.py`. The launcher then runs only the frozen triangle p107 lane; it cannot launch a second prime, another branch, degree twelve, or overwrite existing output.
