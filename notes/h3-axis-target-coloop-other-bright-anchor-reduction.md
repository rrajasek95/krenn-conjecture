# The other bright anchor reduces the 50 no-cross triples to two word-change forms

## Result

Continue from the 50 physical three-base unions in the target-coloop
one-sided-column theorem.  Normalize the selected bases as

```text
M : selected bright target matching, ports P0,S1;
N : selected nonzero outside matching, ports P2,S3;
K : forced unary/direct matching, containing PS:00.
```

A full one-bad source also contains a selected pure target matching `L` for
the other bright colour.  Since the direct pair `PS` supports only `00`, `L`
is one of the 90 perfect matchings avoiding `PS`.  The checker superposes
all of them on all 50 no-cross triples:

```text
50 * 90 = 4500 quadruples (M,N,K,L).
```

The exact incidence partition is

| outcome | quadruples |
|---|---:|
| `M union K union L` contains a crossed response base | 612 |
| no such base; `N` has an endpoint edge outside the anchor union | 3778 |
| no such base; `N` has only residual-`q` edges outside the union | 48 |
| fully anchor-contained, `L=N` as physical matchings | 50 |
| fully anchor-contained, `L triangle N` one residual `C4` | 12 |

Checker:
`computations/verify_h3_axis_target_coloop_other_bright_anchor_reduction.py`.

## The graph-positive routes

First take crossed matchings only in the selected-anchor union
`M union K union L`; an edge supplied solely by `N` is not counted.  There
are 612 such quadruples, containing 644 crossed matchings.  Every edge of
each matching therefore has an already selected nonzero pure decoration.
Their induced endpoint-label histogram is exactly

```text
(2,1):322,  (1,2):322.
```

They are literal mixed monomials in genuine crossed zero rows and enter the
companion/lock exchange.  This is why the theorem counts 612 rather than
every graph-crossed matching in `M union N union K union L`.

Every decorated cell in the selected literal term `N` is nonzero.  In the
remaining 3778 endpoint-exit cases, an edge `P-u` or `S-u` of `N` belongs to none of
the three selected pure matchings.  At a support-minimal source its complete
response column cannot vanish, since then the occupied endpoint component
is exactly deletable.  The three selected anchors give three independent
surviving colour columns at both endpoints after deleting this physical
pair.  Thus it is a nonanchor active rank-`(3,3)` arm.  Its downstream mate
is the existing active-wedge/lock interface; no new graph classification is
needed.

The 48 residual-only exits require one scope split.  If an exposed residual
cell of `N` is off-diagonal, the uniform nonanchor off-diagonal theorem gives
a good pair and a target-augmented active minor.  A globally mixed word may,
however, colour every exposed residual edge diagonally.  Bare graph
incidence does not turn that diagonal residual cell into an endpoint arm or
an active minor.  Those diagonal residual-only exits remain a named
coefficient branch.

## The 62 fully anchor-contained no-cross forms

No arbitrary matching topology remains.  The 62 cases are exactly:

```text
50: L=N as undecorated physical matchings;
12: L and N have the same endpoint ports P2,S3 and differ by one residual C4.
```

Their canonical representatives are

```text
M = 06|17|23|45,
N = 01|26|37|45,
K = 01|23|45|67.
```

For the same-base form,

```text
L = N = 01|26|37|45.
```

For the `C4` form,

```text
L = 04|15|26|37,
N triangle L = {01,45,04,15}.
```

Here `M` carries one pure bright word, `K` carries `0^8`, `L` carries the
other pure bright word, and `N` carries the selected mixed zero-row word.
Thus the next coefficient theorem is sharply typed:

1. in the 50 same-base cases, transport between two decorations of one
   literal matching base;
2. in the 12 remaining cases, a source-labelled word change across one
   residual alternating `C4`.

A Hamming-one/private-site conclusion is not automatic.  If every changed
edge is diagonally decorated, a matching-base word change recolours both
ends of an edge at once.  The missing theorem must use the complete mixed
rows to split that diagonal change, or use the residual `C4` determinant.

## Scope

This is a matching-incidence theorem at `h=3`, not a support-cardinality
layer and not a declaration that every external physical edge is active.
It uses selected nonzero decorations only in the 644 explicitly reconstructed
crossed monomials.  The diagonal residual-`q` exit and the two final
word-change forms are retained honestly.

Run

```text
python3 computations/verify_h3_axis_target_coloop_other_bright_anchor_reduction.py
python3 -O computations/verify_h3_axis_target_coloop_other_bright_anchor_reduction.py
python3 -I -S computations/verify_h3_axis_target_coloop_other_bright_anchor_reduction.py
```

Frozen ledger SHA-256:

```text
f74c8f56ddb24cf6452eef80e7f89c346619683c99279cd81afd793b0e760af2
```
