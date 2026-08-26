# Independent K20 feed-DAG and sign referee

## Verdict

The corrected filtered recurrence has **eleven**, not ten, primitive K20
paths.  The initial Cycle interface (logical `ea7964f7...`) correctly includes
K17→K20, correctly excludes K19→K20, and correctly identifies its missing K18
profile data, but it uses the frozen K16 **normal** as though it retained the
chain provenance discarded while producing that normal.  This makes one
K14 path falsely zero and omits a second K14 path entirely.

The missing paths are load-bearing:

```text
K14 --K2--> K16 --K4--> K20                 increments (2,4)
K14 --K2--> K16 --K2--> K18 --K2--> K20     increments (2,2,2)
```

The first has negative sign relative to R8′; the second has positive sign.
The frozen literal collector discarded exactly 75,691,040 reducible K16 tail
occurrences, and the K16 filtered report explicitly says their higher tails
were not constructed.  Nonpivotability of the retained K16 normal therefore
does not make the discarded parents' K4/K2 descendants vanish.

Cycle accepted this referee and is superseding its ten-lineage ledger.

## Exact recurrence and signs

Write `D_d` for the direct Kd packet in

```text
P = -R8' E0 E1 E2,
```

and let `Piv(B_d)` be the pivotable part of the collected Kd bucket.  Under
the current deterministic policy,

```text
B_d = D_d + sum_(j=2,3,4) T_j(Piv(B_(d-j))),
T_j(c R) = -c/|pivots(R)| * sum_(Kj tails) tail.
```

K14 uses the frozen 25-cover-valid pivot average.  Every later page averages
over all literal dividing K0 pivots.  Each transition reverses sign.  Since
all direct packets have sign `-R8'`, the complete primitive paths to K20 are:

| direct root | increments | sign relative to R8′ | denominator depth |
|---:|---|---|---:|
| K14 | 2,2,2 | + | 3 |
| K14 | 2,4 | − | 2 |
| K14 | 3,3 | − | 2 |
| K14 | 4,2 | − | 2 |
| K15 | 2,3 | − | 2 |
| K15 | 3,2 | − | 2 |
| K16 | 2,2 | − | 2 |
| K16 | 4 | + | 1 |
| K17 | 3 | + | 1 |
| K18 | 2 | + | 1 |
| K20 | direct | − | 0 |

There is no K19 path: its smallest tail increment is two and lands in K21.
Odd parity is not itself an exclusion—K15 and K17 both feed K20.

## Direct packet census

For one of the 485 R8′ H-slices, the labeled E-degree packets are:

| K degree | E profile(s) | occurrences |
|---:|---|---:|
| 14 | 2+2+2 | 1,728 |
| 15 | 2+2+3 | 13,824 |
| 16 | 2+2+4; 2+3+3 | 25,920; 36,864 |
| 17 | 2+3+4; 3+3+3 | 138,240; 32,768 |
| 18 | 2+4+4; 3+3+4 | 129,600; 184,320 |
| 19 | 3+4+4 | 345,600 |
| 20 | 4+4+4 | 216,000 |

Thus direct K20 has 104,760,000 provider occurrences over all 485 slices,
agreeing with Cycle.

## Literal proof that the hidden paths are live

For the lex-first K14 head

```text
000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3
```

the frozen valid-pivot rule selects pivot 70, word `22220000`, anchor
`087dc6f3`.  Among its twelve K2 children, ten are nonpivotable but two have
three dividing K0 pivots each.  The first is

```text
tail 1150c6f3
row  0000040d111950556275757997c4c6cfd3d7e0e6eaeef2f3
pivots 8,26,35.
```

This row has 60 K4 tails per pivot, so the `(2,4)` transition is a literal
nonempty source packet.  Continuing instead through K2 tails gives 72
provider grandchildren for the two rows and their three pivots; eight remain
pivotable at K18.  The first is

```text
K16 pivot 8; tail 0a49c6f3
row 00040a0d111949505562757597c4c6cfd3d7e0e6eaeef2f3
K18 pivot 26.
```

Hence the triple `(2,2,2)` path is also literally live.  Global coefficient
collection might cancel some descendants, but no zero claim is sound without
that collection.

## Denominators

The maximum pivot-denominator depth at K20 is three, attained by
`K14→K16→K18→K20`.  If the three pivot counts are `q14,q16,q18`, the source
coefficient carries their product.  The one-step scale
Generic's independent arithmetic DP (logical `f77bc67518a...`) explicitly
propagates the hidden higher tails.  It finds 142 distinct depth-three products
at K20, with LCM

```text
U = 400,591,699,200.
```

Thus the existing global scale is certified even though the active residual
recurrence omitted the lineage.  The correction is to the feed/provenance DAG,
not to the denominator scale.

## Corrected missing interface

Before the existing four-lineage K18 profile census is sufficient, the full
chain must also reconstruct the discarded K14/K2 population:

1. retain every reducible K16 child with its K14 head, valid-pivot choice,
   coefficient and first denominator;
2. emit its K4 tails directly to K20 and its K2 tails to a K18 parent stream,
   using all-pivot averaging at K16;
3. retain the pivotable K18 descendants and emit their K2 tails to K20 with
   the three-denominator product; and
4. collect signed H-orbit masses before any profile or charge evaluation.

The frozen K18 pass additionally lacks outgoing pivot profiles for its four
previously known lineages.  Scalar charges and evaluation counts cannot
recover those profiles.

## Replay and scope

Run `audit_k20_feed_dag.py`.  It pins the current Cycle interface and the
frozen K16 reports, derives all direct packet counts and degree compositions,
and source-replays the literal live K14 sentinel.  It does not construct a
K20 row, charge, profile closure or coefficient-cancellation solve.
