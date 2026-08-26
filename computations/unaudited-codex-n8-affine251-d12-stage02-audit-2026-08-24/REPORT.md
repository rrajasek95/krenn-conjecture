# D12 stage02 round778→805 audit

## Verdict

`PASS_EXACT_FULLY_TELEMETERED_RESUMABLE_STATE`.

Stage02 is accepted without a split or quarantine.  It is an exact continuation
checkpoint through round 805, and its v3 invocation, live resource gate, and
atomic outputs are all bound by complete watchdog-v2 telemetry.  The native
result remains `INCOMPLETE_RESOURCE_GATE/WALL_CAP`; this is a resumable exposed
state, not a terminal global dual.

## Algebra and exact ancestry

- The pinned stage01 inputs are checkpoint SHA-256
  `d8463c5aba89f3dde57ed9c92d57a4a8fb11fb2585a504b8e3b7f71078610345`
  and cache SHA-256
  `805a5bb3194f146c38a10483203a72847728d1178feca01d835e415dcd6607e5`.
- Stage02 has exactly 27 consecutive records, rounds 779 through 805.  Their
  `new_columns` sum is 36,827, taking the census from 368,432 to 405,259;
  final candidate support is 518.
- The native `AFF12CEG1` checkpoint header, canonical total orders, exact EOF,
  and target coefficient 1 all pass.
- All 368,432 input checkpoint columns remain present.  All corresponding
  cache records are preserved byte for byte, and exactly 36,827 new records
  are added.  Provider fingerprint is unchanged at
  `9218588987274412661`.
- Independent streaming replay covers all 405,259 cached columns and
  41,147,285 terms.  It finds 1,287 candidate-hit terms, target incidence in
  two cached terms, and zero pairing failures.

Authoritative stage02 hashes:

- `result.json`: `5d0d27971f8ddcb11f9e03e96afca5b952b6548e5dcf2de6bc682792b1facc1f`
- `checkpoint.bin`: `7cd46995e665591116cbb0f99fc087cd47688229082e55b92cdabeb7f2546415`
- `vectors.bin`: `c00f86587df398f59476b2fd3478b9ed1e449a65ecd8400ce6a711d68e380e57`
- `watchdog.json`: `c44df39a18b4e37f2d82b4d96d5ecea1e57486addec45ad9e73e84e311960a25`
- `stderr.log`: `47e49f02185cca6b431547a9892193b705db0a307c9543201553d4db28d2baae`
- empty `stdout.log`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Invocation and resource evidence

The telemetry pins source
`173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a`,
binary `8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a`,
and watchdog v2
`53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97`.
The full command is exact: prime, 16 workers, cold/rare hierarchical mode,
95-second native wall gate, 36-GiB RSS cap, and the stage02 output paths.

Watchdog status is `PASS`, breach is null, and child return code is zero.  Its
387 monotonically ordered libproc samples have peak 7,687,664 KiB, below the
37,748,736-KiB cap.  The last sample is at 98.364728 seconds and natural child
exit at 98.623315 seconds, a 0.258587-second gap.  Telemetry hashes the result
and final logs; `atomic_outputs_clean` is true, and no native or log `.tmp`
path remains.

## Scope

This referee parsed and hashed the supplied files, compared the complete
persisted prefix, and streamed the complete output cache.  It did not evaluate
provider columns, run elimination, or continue beyond round 805.

