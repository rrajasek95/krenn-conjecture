# D12 stage01 round749→778 split audit

## Verdict

`PASS_ALGEBRAIC_STATE_REJECT_RESOURCE_PROVENANCE`.

The supplied round-778 checkpoint/cache is an exact, normalized, resumable
algebraic state.  It may be used as a continuation input.  The stage01 run is
not accepted as evidence of compliance with the live 36-GiB watchdog contract:
there is no `watchdog.json`, both logs remain `.tmp`, and native RSS reporting
is zero.  This resource/provenance evidence is quarantined and must not be
represented as a watched production pass.

## Exact algebraic state

- Input is the sealed round-749 checkpoint/cache with 334,298 columns, SHA-256
  `dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621`
  and `93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1`.
- The result contains exactly 29 consecutive records, rounds 750 through 778.
  Their `new_columns` values sum to 34,134 and their running counts end at
  368,432 columns; final support is 556.
- The round-778 checkpoint has the native `AFF12CEG1` schema, prime
  1,073,741,827, total-order columns/rows, no trailing bytes, and target-row
  coefficient exactly 1.
- Every one of the 334,298 input columns is present in the output checkpoint.
  Every corresponding input vector-cache record is preserved byte for byte;
  the output adds exactly 34,134 records.
- An independent streaming replay checked all 368,432 cached columns and
  37,387,100 terms: target pairing is normalized and the candidate has zero
  pairing on every cached column (`verification_failures=0`).

Authoritative stage hashes:

- `result.json`: `e1f6ab7d31f84de44d4b2cee1b156fa6f924cce7e736b680323801d31e6f153d`
- `checkpoint.bin`: `d8463c5aba89f3dde57ed9c92d57a4a8fb11fb2585a504b8e3b7f71078610345`
- `vectors.bin`: `805a5bb3194f146c38a10483203a72847728d1178feca01d835e415dcd6607e5`
- `stderr.log.tmp`: `6119505476cc898c291738cb6a18d5fd778044d06c1cd810958dc79dc3713771`
- empty `stdout.log.tmp`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The supplied status is `INCOMPLETE_RESOURCE_GATE/WALL_CAP`, not a terminal
global dual.  It is accepted only as the exact exposed-system state at round
778.

## Native and watchdog provenance

The sealed v3 source and binary presently hash to
`173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a`
and `8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a`.
The state is content-descended from the pinned round-749 artifacts and its mode
fields/log syntax match v3.  However, stage01 contains no launch manifest or
watchdog telemetry binding that particular invocation to those executable and
input hashes.  Verifying the files now is not a substitute for an invocation
pin.

The native outputs themselves are structurally clean and no
`result.json.tmp`, `checkpoint.bin.tmp`, or `vectors.bin.tmp` remains.  That
proves parseable atomic final state, but it does not recover a missing live-RSS
trace or prove the wrapper stayed alive through natural child exit.

The corrected future wrapper is separately pinned at SHA-256
`53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97`.
Its bounded hostile suite passed one fast exit, 32 poll/exit race repetitions,
and a synthetic 32-MiB RSS overrun with a sampled breach and absent final
result.  These tests validate the corrected wrapper only; they do not apply
retroactively to stage01.

## Scope

This referee performed format parsing, content-descendant comparison, cache
streaming, and bounded watchdog hostiles.  It did not evaluate provider
columns, run elimination, or continue beyond round 778.

