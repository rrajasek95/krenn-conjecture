# Twelve no-anchor rectangle transport census

Status: **PASS exact transport census; rank three closes all twelve records;
rank one/two remain exact designs only; no solve was run.**

The twelve no-anchor rectangle records split into exactly two source-support
isomorphism classes.  With `A12` present the class is records
`{0,1,4,5,8,9}`; with `A12` absent it is `{2,3,6,7,10,11}`.  Exhaustive
enumeration of all `8!` site permutations finds one and only one map between
each ordered pair inside a class and none across the two classes.  Every map
preserves the fixed family `{03,16,27,45}`, the full variable family
`{04,12,35,67}`, the added support, and the actual variable support.

For every record, all six simultaneous colour permutations were replayed on
all `3^8=6,561` word-labelled full-X5 amplitudes.  The replay includes endpoint
reversal/transposition of every matrix factor.  The formal guard response set
and the selected cap-27/star-1 identity-cap carrier were also carried
literally.  Thus this is a polynomial/source-label transport, not merely an
unlabelled support match.

The representatives are record 0 (`A12` present) and record 2 (`A12` absent).
Their mapped outside factors are:

| records | outside factor | companion factor |
|---|---:|---:|
| 0, 2 | `A47` | `A46` |
| 1, 3 | `A46` | `A47` |
| 4, 6 | `A37` | `A36` |
| 5, 7 | `A36` | `A37` |
| 8, 10 | `A56` | `A57` |
| 9, 11 | `A57` | `A56` |

Consequently, the sealed exact-Q rank-three unit certificate transports to
all twelve records, with rank imposed on the corresponding outside factor.
The sealed rank-one and rank-two chart constructions transport to all twelve
as well: respectively 76 variables/6,571 generators and 80 variables/6,574
generators, each with 27 raw charts and five simultaneous-colour orbits.
Those lower-rank ideals have not been solved, so this package makes no closure
claim for them.

There is deliberately no source-support automorphism across the two `A12`
states.  Their *reduced polynomial ideals* are nevertheless identical because
`A12` appears in no supported perfect matching, selected guard, or carrier;
solutions lift separately with `A12=I3` or `A12=0`.  This distinction is kept
explicit rather than calling the two source records directly automorphic.

All twelve no-anchor rectangle records are now accounted for by the rank
dichotomy.  Four other records in the parent unmapped-16 ledger lie outside
this rectangle scope.  This census neither solves rank one/two nor closes
those four records or the conjecture.
