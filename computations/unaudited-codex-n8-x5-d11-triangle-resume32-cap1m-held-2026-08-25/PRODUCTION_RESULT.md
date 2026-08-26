# D11 triangle cap-1m continuation result

Status: **PASS restart checkpoint / fail-closed mathematical verdict.**

The frozen run cleared under design manifest
`d70e0ef9f83c02391d34e45baab8e3173b68093e626ca7b7c69cbbeba853665e`
terminated normally (`returncode=0`, no watchdog breach) at the exact column
gate.  It advanced from 515,869 selected / 427,712 support to 913,636 selected
/ 924,170 support.  Round zero added 397,767 columns.  The following scan found
86,365 violations against only 86,364 remaining slots, so none of that batch
was accepted.

Engine wall was 128.545263 seconds, wrapper wall 133.237202 seconds, and peak
process-group RSS 20,707,504 KiB under 32 GiB.  The frozen watchdog conservatively
labels `INCOMPLETE_COLUMN_CAP` as `FAIL_CLOSED` because that engine status is not
one of its accepted terminal/restart classes; there was no resource breach.

Independent literal replay parsed every emitted row and column and verified all
913,636 pairings with zero failures, exact preservation of the 515,869-column
seed subset, and `lambda(t^11)=1`.

Authoritative restart pair:

- selected SHA-256: `81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8`
- dual SHA-256: `c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284`
- checkpoint audit SHA-256: `db6d963a6971ad25d9d3b71502807f1f079539607ca4ada9f6c82f354c52a1dc`

There is no global terminal scan and no mathematical verdict.  No p2, other
branch, relaunch, or D12 computation/read occurred.
