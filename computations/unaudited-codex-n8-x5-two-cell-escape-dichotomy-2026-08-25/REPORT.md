# Every minimal two-cell escape forces a second X5 amplitude

Status: **exact minimal escape lemma proved; arbitrary off-support support is
not classified.**  No CEGAR, ideal solve, or D12 artifact was read.

## The exact lemma

Start from the pure-normalized source in the parent package,

```text
A03=A16=A27=A45=A67=I3,
all other source cells zero.
```

Its unique contribution to `Phi(00001100)` is

```text
M0 = 03|16|27|45,       coefficient +1.             (1)
```

Suppose exactly two previously zero source cells are made nonzero, the three
pure amplitudes remain one, and an alternative perfect matching cancels (1).
Then the two cells must both be off diagonal, must have endpoint colours
`0/1`, and their coefficient product must be `-1`.  Exhausting the 105
perfect matchings of eight labelled sites gives exactly eight possibilities:

```text
residual four-cycle:  04|16|27|35, 05|16|27|34       (2)
cap-star four-cycle:  03|14|27|56, 03|15|27|46,
                      03|16|24|57, 03|16|25|47       (4)
direct six-cycle:     03|14|25|67, 03|15|24|67       (2)
```

This is also a source-labelled proof, rather than an orbit or numerical
classification: the symmetric difference with `M0` is an alternating cycle,
and requiring only two missing cells restricts it to the displayed cycle
types.  Off-diagonality is necessary because a new diagonal cell could alter
a pure amplitude.

Now inspect the second mixed word `00002200`.  Every new cell above contains
an endpoint colour `1`, so none can occur in a term for this word.  On the
old support its only perfect matching is again `M0`.  Therefore, in every one
of the eight cases,

```text
Phi(00002200) = +1.                                   (2)
```

Thus **every pure-preserving minimal two-cell cancellation of
`00001100` forces another nonzero X5 amplitude.**  This proves the requested
minimal boundary case over every integral domain.  Four of the eight patterns
(the two residual and two direct-cycle patterns) preserve the parent's formal
triangle kernel.  Each cap-star pattern instead creates exactly one outside
response for `K=I`; this is a structural response branch, but the current
identities do not by themselves prove that it is an active clean cap.  The
stronger amplitude conclusion (2) holds in both branches.

## Exact census of the retained A04/A35 escape

For

```text
A04[0,1]=+1,  A35[0,1]=-1,
```

only `M0` and `04|16|27|35` contribute.  Parameterize an `M0` word by the
four matching-pair colours `(a,b,c,d)`:

```text
(a,b,c,a,d,d,b,c).
```

The new matching cancels exactly the nine-word slice `a=0,d=1`, with `b,c`
arbitrary.  Removing these nine words and the three normalized pure words
from the 81-word base sector leaves exactly 69 mixed violations, all with
coefficient `+1`:

```text
profile 6+2:    22
profile 4+4:    16
profile 4+2+2:  31
```

Swapping the colours on the matching pairs `16` and `27` is an exact word
symmetry.  The 69 words form 45 orbits under that involution (24 two-element
orbits and 21 fixed words).  The first forced word is precisely
`00002200`, as predicted by (2).

## Where the next boundary starts

Cancelling both `00001100` and `00002200` requires distinct `0/1` and `0/2`
source labels, hence at least four new cells in this residual-cycle family.
The smallest explicit extension is

```text
A04[0,1]=+1, A35[0,1]=-1,
A04[0,2]=+1, A35[0,2]=-1.
```

It preserves all three pure amplitudes and the formal triangle guard, and it
cancels the two named words.  It is still not X5: cross-colour terms create
`Phi(00001200)=-1`, and there are 78 nonzero mixed amplitudes.  This is the
smallest surviving support pattern isolated by the present proof.

The result does **not** classify cancellations using three or more new source
cells, does not prove a general active-cap dichotomy, and is not a conjecture
counterexample.  It closes exactly the minimal two-cell escape left open by
parent manifest
`0c6c164e7c1e6a37a369dfe509ec4145ae8d610a80a17d8b6ff0bb0a98a6d65b`.

