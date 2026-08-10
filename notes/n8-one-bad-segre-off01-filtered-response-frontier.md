# N=8 off-01 filtered-response frontier

## Result

The common cocharacter

```text
((0,0,0),(0,1,1),(0,1,0),(0,0,1),(0,1,0),(0,0,1))
```

has grade zero on the fixed Segre matching `H` and the 24 optional mixed
cells of the off-01 face.  Among the 45 diagonal cells, 21 have grade zero,
18 have grade one, and 6 have grade two.  Including mixed and diagonal
cells, the positive q universe is

```text
62 of grade 1, 14 of grade 2.
```

The pure word weights are `(0,3,3)`. Thus a compatible filtration of a
diagonal response row has star shifts `a_i+b_i=-3` for `i=1,2`; every
monomial in one fixed response word has the same total grade.  This is why
the affine optional-face theorem `4a213d8` cannot simply discard the 76
positive-grade q cells when the four response rows are retained.

`computations/verify_n8_one_bad_segre_off01_filtered_response_frontier.py`
builds the complete top and four-response source-support shadow. Each
odd-triangle clause from the maximal off-01 face with all diagonal cells is
weakened by precisely the additional physical monomials in its three source
rows. Its q-factor, including any positive-grade diagonal cells, remains in
the antecedent. The resulting
formula has

```text
35,583 variables
230,918 clauses
27,512 conditional odd-triangle clauses
formula SHA256 c8eba8e4cfb2303f965f6094fec67417113db6e4558760d9a437853730d619f6
```

Its exact minimum number of live positive-grade q cells is six. The
strict `<=5` formula is UNSAT. Glucose emits a deletion-free proof with
222,654 additions; the checker parses it, independently RUP-replays every
addition with CaDiCaL, and requires the terminal empty clause.

```text
bounded-formula SHA256
  1688d15a9fc8597c96b3c41726b7396cc0ae8c6bdf7b15927f89cc52dca740a2
proof SHA256
  f8a416b6dd65b335f55d66a54c86a7ae7eb18cf18bbb791728e04246acf0569a
ledger SHA256
  0428b66afaa140021ab8db49d8ace6dd7b872940e6857fdba96243e804894b2c
```

## Minimum-support census

The decorated weighted site stabilizer of `H` is trivial (all 720 site
permutations are checked). Consequently the 20 feasible six-cell supports
are already the exact orbit census:

```text
02:01 12:01 14:22 23:11 24:12 25:11
03:02 13:02 15:11 23:22 34:22 35:21
04:01 12:22 14:01 24:21 34:11 45:11
05:02 13:11 15:02 25:22 35:12 45:22
12:01 14:22 23:10 23:11 24:12 25:11
12:01 14:22 23:10 23:11 25:10 25:11
12:01 14:22 23:11 24:10 24:12 25:11
12:01 14:22 23:11 24:12 25:10 25:11
12:22 14:01 24:01 24:21 34:11 45:11
12:22 14:01 24:21 34:01 34:11 45:11
12:22 14:01 24:21 34:11 45:10 45:11
12:22 14:01 34:01 34:11 45:10 45:11
13:02 15:11 23:02 23:22 34:20 34:22
13:02 15:11 23:02 23:22 34:22 35:21
13:02 15:11 23:22 34:20 34:22 35:21
13:02 15:11 23:22 34:22 35:20 35:21
13:11 15:02 25:02 25:22 35:12 45:22
13:11 15:02 25:02 25:22 45:02 45:22
13:11 15:02 25:22 35:02 35:12 45:22
13:11 15:02 25:22 35:12 45:02 45:22
```

The checker emits the complete canonical `{high, face, diagonal, stars}`
model above each support. Their ordered JSON digest is

```text
8b6577626d4c5dfc439ffdd6da8242b857d384a5b160c237d5befccd6dc547de
```

and the six-cell-support digest is

```text
34511470fe2bde5aaa0a34228500608f927565ef8f94e1e61709ac06136fb240
```

## Scope

This artifact is the exact associated-graded support lower bound and the
complete minimum-support census. It makes no coefficient-level claim about
the 20 supports. Coefficient saturation of the full grade-zero envelopes is
a separate downstream theorem and should use the six positive cells as the
only localization hypotheses.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_off01_filtered_response_frontier.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_off01_filtered_response_frontier.py --skip-rup
```

The first command performs the independent 222,654-addition RUP replay.
`--skip-rup` is an explicitly separate, pinned optimized-mode check of the
formula, proof generation, minimum, and complete census.
