# D11 triangle cap-1.25m continuation result

Status: **FAIL_CLOSED_NO_PROGRESS; restart pair remains valid.**

The frozen run under manifest
`8b7f57884bd90865cd5fff5459b1219c82e861351de4b4aceb6bb9bc32a64d59`
exited normally (`returncode=0`, no watchdog breach) at its column gate.  From
the 913,636-column / 924,170-support seed, its first scan found 336,365
violations against 336,364 remaining slots.  The engine therefore accepted no
partial batch and emitted a byte-identical restart pair.

Engine wall was 77.835386 seconds, wrapper wall 79.779696 seconds, and peak RSS
21,473,088 KiB under 38 GiB.  Independent literal replay again verified all
913,636 pairings with zero failures and `lambda(t^11)=1`.

- selected SHA-256: `81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8`
- dual SHA-256: `c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284`
- checkpoint audit SHA-256: `68170d3b81f3e71e40ad2d00f6c034172deb88723f6764a4df7aa8838dee5669`

This run adds zero accepted coverage and provides no mathematical verdict.
No relaunch, p2, other branch, or D12 computation/read occurred.
