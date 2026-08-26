# K23 hidden-decorated pair exact charge

Status: **PASS** for exactly `D14:222|R:2-3-4` and `D14:222|R:2-4-3`.
This is a strict two-ID scalar fragment, not a complete K23, K24, row, or membership claim.

The frozen `H16ORM1` source has SHA-256
`22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8`,
101,545,723 records, 511,214,060 retained pair uses, and scaled pair mass
146,230,609,431,055,564,800.  Three atomic production intervals form the exact
no-gap partition `[0,33848574)`, `[33848574,67697148)`,
`[67697148,101545723)`.  Their elapsed times were 207.747471 s, 52.457090 s,
and 54.706159 s under the frozen eight-worker/cache-100000 producer.

## Exact result

| strict ID | terminal occurrences | scaled charge | exact charge |
|---|---:|---:|---:|
| `D14:222|R:2-3-4` | 106,483,282,080 | -292,869,665,337,482,477,568 | -127113570024948992/173867925 |
| `D14:222|R:2-4-3` | 32,363,679,360 | -119,114,845,190,185,844,736 | -4699922868930944/15806175 |

The strict subtotal is
`-411984510527668322304/U = -59604240527729792/57955975`, with
`U=400591699200`.  Full and irreducible counts and charges are identical.
Occurrencewise normalization uses `w3=-w2/m3`, and every realized divisor
satisfies exact `U/(m2*m3)` divisibility.  The second and third source intervals
have exactly zero realized `R:2-4-3` support; each zero-support claim was checked
by 257 independent literal replays.

## Referee and integration guards

Every shard's 257 distributed samples was independently reconstructed from
literal source bytes, including both possible response orders, terminal
nonpivotability, and abstract/literal cycle-key and charge equality.  The merger
pooled those 771 records and deterministically selected 257 globally distributed
records; the independent merged replay found 216 nonzero `R:2-3-4` and 41
nonzero `R:2-4-3` continuations.  The package verifier rehashes all shard evidence,
the source header and full source bytes, recomputes the witness selection, and
passes byte-identically under standard Python, `-O`, and `-I -S`.

The fragment manifest exposes two singleton scalar groups, so neither value can
be multiplied by packet cardinality.  Ingestion through the frozen strict K23
assembler together with the already sealed hidden-collected singleton gives the
current exact union `direct23(23) + directK16(18) + hidden-collected(1) +
hidden-decorated(2) = 44` distinct IDs.  The independent set referee proves
this 44-ID set and the explicit 15-ID gap partition the frozen 59-ID set, with
no duplicate or extra.  The assembler remains fail-closed at
`REJECT_INCOMPLETE_K23_59_ID_GATE`.
