# K24 hidden-collected fast singleton launch acceptance

Verdict: **ready for one full run after explicit resource clearance. No full production was launched.** The strict scope is the singleton `D14:222|R:2-2-2-4`.

## Corrected launch blocker

The prior fast source/binary (`47bd390f…` / `2f89d6b…`) was not launchable: its full-only terminal assertion retained the K23 count `32 × 570,281,318 = 18,249,002,176`. K24 has 60 terminal K4 tails per selected K20 pivot, so the exact count is `34,216,879,080`. The frozen source corrects this pin, corrects the stale K3 ledger label, checks exact input size/header, and requires exactly 257 ledger rows before either atomic write.

## Bounded acceptance

The corrected million-record control completed in 2.829644 seconds and projects 448.328749 seconds for the full 158,439,965-record scan. All recurrence/scalar fields exactly match the earlier million-record control. Its 257 evenly distributed records were independently sought in the 12.7 GB H18PIV2 input and replayed through every K2 intermediate and all 60 terminal K4 tails; source rows, retained witnesses, weights, orbit/stabilizer data, multiplicities, counts, signs, divisions, terminality, and charges agree.

The strict validator pins source, binary, input, both included recurrence sources, exact result keyset, singleton/U/sign/scope, full source/count pins, histogram/cache identities, and all 257 source records. Sixteen hostile cases reject structural and literal mutations after a strict hash-preflight baseline.

The exact launch and post-run validation commands are frozen in `launch_acceptance.json`. Acceptance requires a distinct atomic result, the companion 257-row ledger, the strict full validator, and the independent literal referee. The run remains gated at 600 seconds and 16 GiB with no concurrent heavy process.
