# D11 triangle cap-750 continuation result

Status: **PASS restart checkpoint / fail-closed mathematical verdict.**

The cleared frozen run from design manifest
`55c9d74da7c5900a6e764a0d26fa3b7f607a4c601f3f54ca9ed9fff610cc031b`
terminated normally (`returncode=0`, no watchdog breach) at the exact column
gate.  It advanced the checkpoint from 307,885 selected / 184,659 support to
515,869 selected / 427,712 support.  The first round added 207,984 columns;
the next exhaustive attempt found 234,132 violations, more than the 234,131
remaining slots, so no part of that second batch was accepted.

The engine wall was 70.285464 seconds; wrapper wall was 71.734376 seconds;
peak process-group RSS was 12,067,360 KiB under the 24-GiB cap.  The frozen
watchdog labels `INCOMPLETE_COLUMN_CAP` as `FAIL_CLOSED` because that engine
status is intentionally absent from its accepted terminal/restart classes.
This is not a process or resource breach.  The emitted pair was independently
parsed and all 515,869 literal source pairings replayed with zero failures;
the original 307,885 columns are an exact subset and `lambda(t^11)=1`.

Authoritative restart pair:

- selected SHA-256: `e19fbb6b57ae672a130c38c03783845e39dceaea795ff371ec07973f6d8e82d5`
- dual SHA-256: `c56be60d563a1494a572a7bd6c89f9b03e928fc7ae22414644c9109767566fe3`
- checkpoint audit SHA-256: `5e4918cc80a4a936b18a5add3f0d109af6d21af664cf67e65130ffe5ede3e6ab`

There is no global incident-scan terminality and no mathematical verdict.
No p2, other branch, or D12 computation/read was launched.
