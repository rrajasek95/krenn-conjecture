# The split spoke guard reduces to a finite diagonal closed-star recurrence

## Base complete-row scan

Pin the literal rank-two split guard `a8ef1a4`.  Its occupied target-zero
response blocks are

```text
R21[000001], R21[000100],
```

each with two cancelling occurrences.  A complete scan of all `729` unary
words and all four response heads finds

```text
mixed unary coefficients with an occurrence      0
mixed response coefficients with an occurrence   2
nonzero target-zero coefficients                  0
private target-zero coefficients                  0.
```

Thus the support displayed in `a8ef1a4` does not itself force a mate.  The
next mandatory row is instead a missing constant-colour normalization; take
the pure-one target `H[111111]=1`.

Checker:
[verify_h3_active_coloop_spoke_split_guard_complete_row_recurrence.py](../computations/verify_h3_active_coloop_spoke_split_guard_complete_row_recurrence.py).

## Adjoining the pure-one target

There are fifteen possible all-one perfect matchings.  Give one of them
unit coefficient, retaining the split guard.  Across all fifteen choices,
the complete unary/four-response scan contains

```text
57 nonzero mixed unary rows,  of which 48 are private;
36 nonzero mixed response rows, all 36 private.
```

The numbers of private unary rows per pure-one matching are

```text
2 rows for 3 matchings,
3 rows for 9 matchings,
5 rows for 3 matchings.
```

The private response-row counts per matching are distributed as

```text
1 row for 4 matchings,
2 rows for 5 matchings,
3 rows for 2 matchings,
4 rows for 4 matchings.
```

Each private coefficient is target-zero and nonzero.  A complete source
must add at least one alternate occurrence to it.

## Exact unary-mate classification

Every private unary row has fourteen alternate perfect matchings.  The
`48*14=672` choices split as

| alternate class | count |
|---|---:|
| two cross-colour edges, at least one outside star `0` | 576 |
| all diagonal and destroys the pure-zero coloop `01` | 36 |
| all diagonal, preserves `01`, remains trapped | 60 |

The first class gives strict Hall-shore growth as well as an offdiagonal
carrier.  In the second class, the new pure-zero cells form a nonzero
perfect matching omitting `01`, so the named coloop is gone.

The remaining sixty are genuine recurrence cases.  Of their alternate
matchings, eighteen retain `01` and forty-two omit it without completing a
nonzero pure-zero matching.  They cannot be discarded by a support-only
coloop test.

## Exact response-mate classification

A fixed response coefficient has

```text
15 direct d*q^3 occurrences + 90 ordered endpoint p*s*q^2 occurrences.
```

After deleting the one selected occurrence, each private response row has
`104` structural alternates.  The `36*104=3744` choices split as

| alternate class | count |
|---|---:|
| a certified cross edge or endpoint hole outside star `0` | 3240 |
| offdiagonal tail, but every certified edge stays in star `0` | 180 |
| diagonal endpoint occurrence inside star `0` | 324 |

The first class gives strict closed-shore growth.  The second is physically
typed for the target-augmented private-site/active-fan alternative, but it
is not called a final four-good landing here: its active carrier may remain
in the same star.  The last `324` choices are the response analogue of the
diagonal unary recurrence.

Hence the first pure-one completion leaves a finite trapped core of

```text
60 unary matching mates + 324 response occurrences.
```

## Frontier effect

The full scan improves the block counterguard in two ways.

1. It proves that the counterguard cannot persist after target completion
   without creating literal private rows.
2. It proves that most mates of those rows already enter the committed
   outside-shore/offdiagonal or named-coloop-destruction routes.

It does **not** yet prove synchronization with the special three-row
processor of `93cf9ae`.  A diagonal, closed-star, coloop-preserving
recurrence survives in both unary and response sectors.

The shortest next calculation is simultaneous colour completion: adjoin
the independent pure-two target matching and scan these `60+324` trapped
choices against all unary and four response rows.  Either the second colour
anchor forces an outside/offdiagonal/coloop exit, or it leaves a finite
two-colour trapped core whose literal support can be fed to the existing
closed-shore response processor.

This is an exact h=3 support and coefficient scan.  A unit value is assigned
to each tested pure-one matching; the resulting packets are not asserted to
satisfy all source equations before their forced mates are added.
