# The minimal four-cell escape has a finite colour escalation

Status: **the minimal four-to-six-cell chain is proved exactly.**  A general
off-support monovariant or active-clean-cap theorem is not proved.  No CEGAR,
ideal solve, or D12 artifact was read.

## Residual-sector identity

Begin with the four-cell source isolated by the parent package:

```text
A03=A16=A27=A45=A67=I3,
A04[0,1]=A04[0,2]=+1,
A35[0,1]=A35[0,2]=-1.                                (1)
```

For `b,c in {0,1,2}` and `d,e in {1,2}`, put

```text
w(b,c;d,e)=(0,b,c,0,d,e,b,c).
```

There are exactly two possible physical terms: the base matching
`03|16|27|45` contributes `A45[d,e]`, while the residual matching
`04|16|27|35` contributes `-1`.  Hence the source-labelled identity is

```text
Phi(w(b,c;d,e)) = A45[d,e] - 1.                       (2)
```

Initially the `{1,2}` block of `A45` is `I2`.  Its two diagonal entries make
the `d=e` equations vanish, but (2) gives

```text
Phi(00001200)=Phi(00002100)=-1.                       (3)
```

## Exact one-cell classification

For `00001200`, an exhaustive scan of every source coordinate which could
occur in a perfect matching gives only two one-cell repairs:

```text
A45[1,2]=+1,  which preserves Phi(0^8)=Phi(1^8)=Phi(2^8)=1;
A12[0,0]=-1,  which changes the pure amplitudes to (0,1,1).
```

The second statement is also immediate algebraically.  The new matching
`04|12|35|67` contributes `-A12[0,0]` to `00001200`, so cancellation requires
`A12[0,0]=-1`; the pure matching `03|12|45|67` then contributes the same `-1`
to `Phi(0^8)`.

Thus `A45[1,2]=+1` is the unique pure-preserving minimal repair.  It cancels
the first word but leaves `Phi(00002100)=-1`.  Repeating the exact scan after
this repair again gives only

```text
A45[2,1]=+1,  pure preserving;
A12[0,0]=-1,  pure destroying.
```

Therefore the colour-reversed repair is also unique.

The simultaneous statement is exact, not an artefact of doing the two steps
in order.  Pairing every correction matching for the two words yields seven
matching pairs and five distinct supports with at most two new cells.  Every
competitor either contains `A12[0,0]`, which changes the pure-0 amplitude
linearly, or is `{A17[0,0],A26[0,0]}`.  For the latter, cancellation requires
the coefficient product `-1`, and the pure matching `03|17|26|45` adds that
same product to `Phi(0^8)`.  The unique pure-preserving two-cell support is

```text
{A45[1,2]=+1, A45[2,1]=+1}.                           (4)
```

## Restricted monovariant and six-cell boundary

Let `mu` be the number of missing ordered off-diagonal entries in the
`{1,2}` block of `A45`.  Along successive minimal, pure-preserving repairs of
the residual sector, the preceding classification proves

```text
mu: 2 -> 1 -> 0.                                      (5)
```

This is a finite monovariant for the minimal chain.  At `mu=0`, the six new
cells relative to the original physical support are

```text
A04[0,1], A35[0,1], A04[0,2], A35[0,2],
A45[1,2], A45[2,1]
```

with coefficients `+1,-1,+1,-1,+1,+1`.  All pure amplitudes remain one and
the formal triangle guard remains unchanged.  Both words in (3) vanish, but
this source is still far from X5: it has 96 nonzero mixed amplitudes.  Its
first is the unique-base identity

```text
Phi(00100001)=+1 from 03|16|27|45.                    (6)
```

No single absent source coordinate can change (6); every alternative perfect
matching is missing at least two cells.  This isolates the smallest
six-cell support which cleans both ordered residual cross-colour words.

For completeness, the next two-cell boundary was classified but not
followed.  Twelve alternative matchings are missing two cells; pure-row
normalization rejects six diagonal patterns.  Of the six survivors, three
preserve the formal triangle kernel and three create exactly one outside
response for `K=I`.  An outside response is not yet a certified active clean
cap.  More strongly, every one of all six patterns still has the common
unique-base obstruction

```text
Phi(00200002)=+1.                                     (7)
```

Equations (2)--(7) prove the requested minimal escape case and give a
source-labelled finite escalation.  They do not control nonminimal additions
which introduce several cancellation terms at once, so no general
off-support dichotomy or full-conjecture claim is made.  The sealed parent is
manifest `dca3d614af5203d5dc2e1b6adb4c2c3f1621d3b0cf368f68d079a376f979f779`.

