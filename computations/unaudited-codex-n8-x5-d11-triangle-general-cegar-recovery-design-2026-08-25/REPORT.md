# Held D11 triangle general-CEGAR recovery

## Status

`PASS_HELD`: the recovery is compiled, pinned, and clearance-gated. No arithmetic has been launched. It is exactly one p=1073741827 triangle-endpoint-colour run from the frozen 76-column D10-transport checkpoint; there is no second-prime or D12 action.

## Frozen geometry

- Native wall: 590 seconds; wrapper wall: 600 seconds.
- RSS watchdog: 12 GiB; column cap remains 500,000.
- Provider SHA: `06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c`.
- Seed selected SHA: `3eab0267866718ca21259e9daffac6f15161438b6348a25fe3de3ded08aaf10a`.
- Seed dual SHA: `4eb560af124b6f046ae67b447988c0b0713822da852f2a1f6fa0307f6ca390b0`.
- Source SHA: `521e8f503f900c15b9b0668f60095fae120b6f47e44666076179fbc2058d9120`; binary SHA: `a2ce6120a4d04683ef4238ef3ec2b4733ad1c2df186e5a838f740fd524f4d5f8`.

Static normalization proves the arithmetic/provider source is byte-identical to the sealed 180-second engine except for the wall guard and periodic checkpoint writes. Every 30 seconds, the current modular dual is atomically renamed before its selected-column checkpoint. Thus any observable pair is restart-safe: a newer dual annihilates an older selected subset, and the engine replays every selected pairing on resume.

The prior lane reached 8,397,664 KiB at 174.594 seconds. Linear extrapolation reaches 12 GiB near 261.8 seconds, so terminality is not projected; the likely useful outcome is a restart checkpoint before an RSS stop. The watchdog distinguishes terminal PASS, native-wall restart PASS, resource failure with checkpoint available, and failure without a checkpoint.

## Clearance

`run_recovery.py` refuses to run unless `CLEARANCE.json` is created after the exclusive slot is granted. Its exact required object is:

```json
{
  "schema": "KRENN_X5_D11_TRIANGLE_RECOVERY_CLEARANCE_V1",
  "authorized_manifest_sha256": "<SHA256 of MANIFEST.sha256>",
  "exclusive_slot": true,
  "launch": true
}
```

The clearance file and production directory are intentionally absent. `results_design_audit.json` proves the hold, exact source delta, hashes, resource geometry, and no-launch state.
