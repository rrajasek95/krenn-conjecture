# Exact D12 round-850 portfolio audit

## Verdict

`PASS_EXACT_ONE_ROUND_PORTFOLIO_AUDIT`: after 118 intervening accepted rounds since the round-731 portfolio audit, the exact six-way tree portfolio at round 850 still selects **cold/rare**. The auto/best audit compared repair and cold bases under first, last, and rare pivots in parallel. It advanced the cloned state from round 849 / 460,676 columns / support 312 to round 850 / 461,464 columns / support 327, adding 788 columns.

A separately cloned fixed cold/rare replay produced byte-identical checkpoint and vector cache outputs. The non-timing round record also matches exactly: 461,464 columns, 788 new columns, support 327, 187 new support rows, strategy cold, pivot rare. Thus the portfolio choice changes only the audit configuration and timing metadata; it does not change the mathematical state selected by fixed cold/rare.

Production was not mutated. This is one round only, and both mathematical verdict fields remain null.

## Frozen provenance

- round-849 checkpoint SHA-256: `ce87c58cf79ddebbc0f9ce39eb36f08b6bf85a8f0f764f7728c3565da13fab49`;
- round-849 vector cache SHA-256: `040b1b59bad7693fbd7ed71d8ff9f760b39b30943c77f452eae3b4047b5ac254`;
- sealed-v3 source SHA-256: `173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a`;
- sealed-v3 binary SHA-256: `8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a`;
- provider SHA-256: `daa427528bbbeece064b09396023b66f32b804ba6d304178d19ced13e9b38a4e`;
- round-849 chain-audit manifest SHA-256: `30be587a44928b418ff51a6fa58791eff90f168a542c22e4d603e7fad72177d8`.

The frozen input chain independently replays all 460,676 round-849 columns and 46,796,079 terms with zero failures. `prepare_inputs.py` made two `/bin/cp -c` APFS clones and verified each against the source hashes before either run.

## Exact outputs and resources

| run | configuration | solve seconds | watched elapsed seconds | peak RSS KiB |
|---|---|---:|---:|---:|
| portfolio | auto/best, six tree tasks | 16.131222 | 25.563932 | 14,783,328 |
| selected replay | cold/rare, one tree task | 14.942081 | 23.679246 | 5,220,304 |

Both watchdogs report PASS, no breach, return code 0, and atomic clean outputs. Portfolio peak RSS was 14.0985 GiB and the fixed replay peak was 4.9785 GiB, both below the 36-GiB limit. The accepted output hashes are identical across the two runs:

- checkpoint: `c2ea7cc0b72218e06866c3db2bd3a269a7ccdbdbf276132e62415d23a23f0fa7`;
- vector cache: `df181c0b86de9a2827d1146a318682482b9af2cae66b470fdf5d11fa036d1ec4`.

The output vector cache contains 461,464 records and is 995,016,982 bytes. Exact result, telemetry, log, and state hashes are recorded in `results_round850_audit.json`.

## Watchdog retry disclosure

The first sandboxed watchdog attempt could not observe the child process group and then lacked permission to signal it. Although that child completed and also selected cold/rare, the run has no valid resource telemetry and is explicitly rejected. Its entire evidence is preserved under `portfolio_watchdog_observer_failure/`, pinned by `FAILURE.json`. A fresh portfolio clone was made from the frozen round-849 source and the identical command was rerun with process-observer access; only that watched retry is authoritative.

## Referee

`audit_round850.py` pins the provider, source, binary, round-849 chain audit, APFS-clone inputs, both result schemas, watchdog atomicity, exact state headers, and byte equality of checkpoint/cache outputs. `validate_round850.py` enforces cold/rare selection and the one-round scope. Ten hostile mutations reject fail-closed, including wrong selection, missing portfolio task, checkpoint/cache mismatch, input replay failure, production mutation, continuation, false terminality, and RSS overrun.

The result supports retaining cold/rare as the production heuristic between periodic portfolio audits. It is not a D12 membership or nonmembership result.
