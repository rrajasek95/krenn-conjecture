# Terminal joint-separator crossing by new mixed-X5 rows

## Outcome

The primitive 100-column integer separator frozen in
`results_closure22_joint_cegar.json` annihilates every abstract degree-13
translation of the existing 22-word closure, but it is crossed by new literal
mixed-X5 rows.  The smallest word-orbit shape that crosses is `[7,1]`
(full `S8 x S3` orbit size 48).  A bounded next CEGAR step can add the word
`00000200`: exactly four of its degree-nine translations cross, all with
integer pairing `-1`.

## Exact census

The calculation enumerates all `3^8-3 = 6558` mixed output words in the exact
joint semigroup of 28 physical-edge counts and 9 ordered-colour-pair counts.
It finds 4,294 new crossing words and 44,127 crossing translated rows.  There
are zero crossings from the frozen closure22 family, an explicit must-fire
guard on the terminal CEGAR claim.

| word shape | full orbit | crossing words | crossing translations |
|---|---:|---:|---:|
| 7+1 | 48 | 7 | 87 |
| 6+1+1 | 168 | 82 | 931 |
| 6+2 | 168 | 76 | 967 |
| 4+4 | 210 | 128 | 1,551 |
| 5+3 | 336 | 154 | 1,982 |
| 5+2+1 | 1,008 | 585 | 7,779 |
| 4+2+2 | 1,260 | 892 | 9,106 |
| 3+3+2 | 1,680 | 1,329 | 11,084 |
| 4+3+1 | 1,680 | 1,041 | 10,640 |

The result JSON exports the four translations of `00000200` individually,
including a literal nine-cell decorated multiplier for each.  Thus no inverse
reconstruction from the quotient key is needed by the next incremental
elimination.  If source symmetry is required from the outset, completing the
48-word `[7,1]` orbit requires 40 words beyond closure22; only seven of those
new words cross this pinned separator, in 87 translations total.

## Provenance and scope

Every exported row is the literal source equation `X_00000200=0` multiplied by
the displayed degree-nine decorated monomial; the audit independently checks
that its 37-coordinate semigroup key is the recorded translation.  One such
row kills this particular dual separator, but this does **not** prove target
membership after enlargement.  Also, `S8 x S3` numbers above are word-orbit
counts only: the joint quotient forgets edge/colour correlation and therefore
does not certify literal multiplier-orbit transport.

Replay:

```sh
python3 audit_separator_crossing_x5_words.py --check-results
```

Logical digest: `5f33323a4aebd81cf1c0656be1c21ee0cc3056afac9c1a184902cfcc39b5f81e`.

