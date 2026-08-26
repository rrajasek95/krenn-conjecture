# D11 triangle cap-1,250,001 continuation result

Status: **FAIL_CLOSED_NO_PROGRESS; restart pair remains valid.**

The frozen run under manifest
`899bf084497c54401a0e61370000be791441b1dab2a026b64fee4b7cf1b8b093`
exited normally (`returncode=0`, no watchdog breach) at its column gate.  From
the 913,636-column / 924,170-support seed, its first scan found 336,366
violations against 336,365 remaining slots.  The engine therefore accepted no
partial batch and emitted a byte-identical restart pair.

Engine wall was 82.741334 seconds, wrapper wall 85.824261 seconds, and peak RSS
14,563,824 KiB under 38 GiB.  Independent literal replay again verified all
913,636 pairings with zero failures and `lambda(t^11)=1`.

- selected SHA-256: `81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8`
- dual SHA-256: `c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284`
- checkpoint audit SHA-256: `73b0307e8470f68b7e1d5a4ccb3a88b17f6e7b3602ada7c4067f7ce9a054b777`

This run adds zero accepted coverage and shows that further unit cap chasing is
not a progress mechanism: the violation frontier still exceeds the admitted
capacity.  No relaunch, p2, other branch, or D12 computation/read occurred.
