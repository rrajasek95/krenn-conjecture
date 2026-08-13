# The third target colour kills the finite split-spoke recurrence

## Coefficient-valid first-colour core

The support census `b3cdd37` left `60` unary and `324` response
closed-star mate choices after adjoining one pure-one target matching.  To
continue the recurrence, the added occurrence must cancel its selected
target-zero coefficient while preserving

```text
H[000000]=1,
H[111111]=1,
the pure-zero coloop 01,
and the absence of an already outside-star response occurrence.
```

These equations sharply reduce the support census.

### Unary mates

All sixty diagonal unary mates can cancel their private mixed row, but the
same forced coefficient changes `H[111111]` from `1` to `0`.  Thus no unary
mate lies in the normalized recurrence.

### Response mates

Among the `324` structural diagonal endpoint/star choices,

```text
270  give the required exact response-coefficient cancellation;
 24  then destroy H[111111]=1;
126  already create a response occurrence with a certified edge outside
     the closed star at 0;
120  preserve both target normalizations, the coloop, and the closed star.
```

The last set consists of `120` labelled states and `100` distinct scalar
value packets.  These are the complete coefficient-valid finite core after
the first new target colour.

Checker:
[verify_h3_active_coloop_spoke_split_guard_three_colour_exit.py](../computations/verify_h3_active_coloop_spoke_split_guard_three_colour_exit.py).

## Add the mandatory pure-two target

A complete ternary source also has `H[222222]=1`.  Append each of the fifteen
possible unit pure-two perfect matchings to each of the `120` states.  This
gives

```text
1800 labelled three-colour packets,
1500 distinct scalar value packets.
```

Every packet contains a nonzero private mixed unary coefficient whose word
has colour multiplicities

```text
0^2 1^2 2^2.
```

The exact number of such private rows per labelled packet is

| private `2+2+2` rows | packets |
|---:|---:|
| 1 | 32 |
| 2 | 408 |
| 3 | 722 |
| 4 | 466 |
| 5 | 134 |
| 6 | 30 |
| 7 | 8 |

In particular, the intersection criterion requested at the frontier is
positive for every packet: each packet has at least one private row whose
every alternate is an exit.

## Why every alternate exits

For a word in which each of the three colours occurs twice, there is exactly
one all-diagonal perfect matching: pair the two sites of each colour.  The
private selected occurrence is this unique matching.  Every one of its
fourteen alternatives therefore contains a cross-colour edge.

Moreover, not all cross-colour edges of a perfect matching can lie in the
star at site `0`: distinct matching edges are disjoint, while all star edges
share `0`.  The checker verifies this literally for every private witness
and every alternate.  Hence every forced mate has an offdiagonal physical
edge outside the current closed star.  It enters strict Hall-closure growth
and the typed offdiagonal active-fan route.

Thus

\[
 \boxed{\text{the finite three-colour trapped core is empty}.}
\]

No arbitrary cross-product of mate choices is needed; a single exit-only
private row in each packet suffices.

## Scope and proof-frontier effect

This closes the smallest literal two-word/four-occurrence split-rank
counterguard of `a8ef1a4`.  It also explains why the guard exists at the
two-colour restriction level but cannot extend to a complete ternary target
packet: the third colour creates a rainbow private row with no diagonal
recurrence.

It does not yet prove the general homogeneous promotion theorem for an
arbitrary quotient-rank-two response packet.  The remaining uniform theorem
is:

> Reduce any two-block transverse cancellation packet, with arbitrary
> additional same-word occurrences and protected rows, either to this
> minimal split guard or directly to a homogeneous private row, typed
> outside-shore/offdiagonal exit, or augmented terminal.

What is now ruled out exactly is the smallest possible obstruction to that
reduction; there is no finite closed recurrence hidden behind it.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded in the checker.
