# The E14 first-hit dual survives every committed literal endpoint/`q` interface

## Result

In the canonical chart `(1,1)`, the word-`000101` unary/`G11` first-hit
presentation still has

```text
269 columns, rank 269; target-augmented rank 270.
```

Its pinned rational cokernel covector `lambda_E14` has support 22 and reads
`-1` on the twelve-tail target.  The new sharp fact is that this entire
pairing comes from one unary S-pair companion:

```text
(p1_0_1,s1_1_1) u05_01 v13_01 v24_11       target coefficient -1
lambda_E14                                      coefficient +1.
```

The decorated rootless core

```text
(p1_0_1,s1_1_1) u05_01 v24_11 v34_10
```

has covector value zero.  Thus identifying the shared decorated `2K2`
monomial does not land the exact E14 obstruction.

Checker:
[`verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py`](../computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py).

## 1. The companion is present in old rows, but always cancelled

Exactly 22 of the complete old columns contain the visible companion:

```text
17 unary columns + 5 G11 columns.
```

Every one is killed by `lambda_E14`.  In particular, the canonical
word-`000101` unary column with multiplier `v24_11` has exactly two nonzero
covector contributions:

```text
- (p1_0_1,s1_1_1) u05_01 v13_01 v24_11       -> -1
+ (p1_0_1,s1_1_1) u35_11 v04_00 v24_11       -> +1.
```

They cancel.  Hence the next column cannot merely be “a row containing the
companion”: the complete old source already contains 22 such columns.  It
must break this precise 22-support cancellation while retaining every forced
proper face.

This explains the earlier private-rewrite result.  The first unary pivot
breaks the response-only orientation cycle but produces a genuine
unary-times-`q` S-pair; it does not reduce the resulting tail in the complete
old module.

## 2. What was actually appended

There is an important typing distinction between a literal column and an
identity in a routed quotient.

The complete committed bounded endpoint inventory supplies no additional
column in the exact `000101` E14 first-hit codomain:

| committed interface | physical/source words | E14 effect |
|---|---|---|
| complete unary/`G11` rows | `000101` | already all 269 columns |
| centered/rootless carrier | `01211222` | decorated core has `lambda=0` |
| normalized GL3 covariance endpoint | `00000000` | different word summand |
| Component-IV covariance | `11211200 -> 01211200` | different fixed K8 pair |
| residual-`q` KS | routed endpoint/tail quotient | no full Spencer column |
| physical six-term `q` | row on a source domain | needs a whole-domain `Phi` |

The exact physical transport law is

```text
q_placed = q_h3 Phi  on the whole source domain.
```

No such `Phi` from the `01211222` comparison presentation into the 4180-row
E14 first-hit presentation is committed.  Therefore inserting the `q` row as
though it were an E14 boundary column would be a variance error.

On the literal combined presentation presently available, the honest
extension is a direct sum, and `lambda_E14` extends by zero over the separate
endpoint/rootless/physical-`q` blocks.  It continues to read `-1` on the E14
target.

This does **not** make it a physical terminal.  It says precisely that the
currently committed comparison maps do not yet pose the extension equations
which could kill it.

## 3. Why the routed KS closure is insufficient

Conditional residual-`q` KS gives the endpoint difference

```text
D = E_plus - E_minus
```

and, together with the signless response `S`, closes the routed two-coordinate
endpoint quotient.  The KS checker correctly limits this to that quotient
and does not claim a full Spencer lift.

That limitation is load-bearing here.  Two full completions may have the same
coarse `D` coordinate while differing by the S-pair companion coordinate;
`lambda_E14` reads `0` on one and `1` on the other.  Thus coarse endpoint data
cannot decide extension of the exact first-hit covector.

## 4. Deleting the visible `v13` factor only moves the obstruction

The tempting specialisation `v13*=0` removes the unique visible target
companion, but it does not close the target:

```text
specialisation                    old rank     residual target_unary support
v13*=0                            211          9
v04*=v13*=0                       185          8
```

All residual coordinates are pure `target_unary` readouts.  In particular,
the decorated core reappears among the target-normal debts.  Thus the
obstruction migrates from the companion to target normal data; it is not
removed by a zero-`q13` support argument.

## 5. First possible killing datum

The exact linear criterion is now minimal.  A new literal augmented column
`b` kills this seed only if

```text
lambda_E14(b_E14) != 0.
```

At coefficient level the smallest model is the unit vector on
`u05_01 v13_01 v24_11`, with pairing `+1`.  Source-validly, however, the
needed object is a **target-bearing endpoint-word-change/unary-times-`q`
comparison cone** whose full E14 projection breaks the old cancellation and
whose `q`, target, labelled-residue, anchor, physical-`W`, eta and sigma faces
are all included.

The target-bearing qualification is forced by the deletion computation: if
the visible companion is suppressed without the cone, 8 or 9 target-normal
readouts survive.

## Proof-frontier consequence

The shortest remaining attack is no longer “find any endpoint difference” or
“identify the common decorated monomial.”  Both are too coarse.  Construct
the one promoted unary S-pair comparison totalization and evaluate its full
E14 boundary under the 22-support covector:

- nonzero pairing identifies the first column which kills the seed and gives
  the missing comparison coefficient;
- zero pairing extends the seed one layer farther, after which its target and
  physical-`q` components can be tested against the accepted terminal rows.

## Scope

This is exact for the canonical chart-`(1,1)` 269-column E14 module and every
currently pinned bounded endpoint/word/physical-`q` interface listed above.
It is not an all-resolution no-go, a full physical separator, or a claim that
no future source-valid comparison cone can kill the covector.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
076a7b7cafb8b94bfa218a5fd1b8324c446c98f114f38fa8a70242cb2303fbba
```
