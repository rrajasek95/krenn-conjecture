# Orbit-zero `K16`: post-singleton duals on the first literal source page

## Verdict

The fourteen affine duals from the archived post-second-singleton `19/14`
split are not stable literal obstructions.  For one canonical factorized
literal representative of each type, every old dual pairs nontrivially with
many direct source columns of minimum `K`-degree 16.

That does **not** fill the local target.  On every one of the fourteen bounded
incident pages, exact rational column rank increases by one when the local
`K14` head is adjoined.  Thus the old dual dies, but a replacement extended
dual survives.

## Exact construction

For each inconsistent canonical anchor signature, the checker rebuilds the
archived irreducible tail columns: all twelve `K2` tails are formed, then a
tail is removed precisely when another one of the 78 `K0` singleton anchors
divides it.  It solves

```text
B_irred^T lambda = 1
```

over `Q` and greedily deletes coordinates while preserving solvability.  A
final exhaustive single-deletion check proves support-minimality.  The result
is remarkably uniform:

- eleven types have three projected dual rows;
- three types have two projected dual rows;
- every retained coefficient is `1/2`;
- literal provenance splits these into six and four labelled rows,
  respectively.

The factorized source scan checks all `485*1728=838,080` frozen `K14` heads
and chooses a lex literal representative transported to each canonical
signature.  For every literal dual row, every incident degree-24 mixed source
column is recovered by exact perfect-matching divisors.  Every output through
`K16` is retained; nothing beyond that first incident page is expanded.

## Three distinct conclusions

1. **The archived duals die directly.** Each type has between 56 and 322
   incident columns whose individual minimum degree is already `K16` and whose
   pairing with the lifted dual is `1/2`.  One literal word, multiplier, hit
   row, and output count is frozen per type.

2. **Lower-kernel transfer does not kill these duals.** After removing the
   direct `K16` columns, let `A` be the complete `K<16` incidence matrix and
   `c=lambda B16`.  Exact sparse rational reduction finds `c` in the row span
   of `A` for all fourteen types.  Equivalently, `lambda` annihilates every
   first-page lower kernel; the transferred detection rank is zero.

3. **Killing an old dual is not a filler.** On the full restricted incident
   page, `rank([M|q])=rank(M)+1` for all fourteen representatives.  Each target
   remainder has support 12.  Therefore a new extended dual remains on every
   page.

The second point answers the motivating test negatively: at this bounded
stage the missing compression is not a hidden lower-filtration kernel.  New
direct `gr_K^16` columns invalidate the projected dual, but the first source
page still does not close the local target.

## Census

`dual` reports projected/literal support.  `lower` reports exact row
rank/kernel dimension for the lower-only page.  The last column is
`rank(M) -> rank([M|q])`.

| type | pivots | dual | incident cols | direct killers | lower | target rank |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 8 | 3/6 | 510 | 264 | 129/117 | 286->287 |
| 1 | 5 | 3/6 | 243 | 88 | 96/59 | 185->186 |
| 2 | 17 | 3/6 | 360 | 110 | 108/142 | 261->262 |
| 3 | 11 | 3/6 | 327 | 110 | 108/109 | 242->243 |
| 4 | 11 | 3/6 | 257 | 70 | 96/91 | 212->213 |
| 5 | 11 | 3/6 | 367 | 124 | 134/109 | 264->265 |
| 6 | 5 | 3/6 | 327 | 112 | 128/87 | 243->244 |
| 7 | 7 | 2/4 | 183 | 56 | 79/48 | 149->150 |
| 8 | 17 | 3/6 | 475 | 138 | 137/200 | 330->331 |
| 9 | 17 | 3/6 | 379 | 80 | 131/168 | 302->303 |
| 10 | 8 | 3/6 | 680 | 322 | 155/203 | 388->389 |
| 11 | 8 | 3/6 | 476 | 172 | 149/155 | 338->339 |
| 12 | 11 | 2/4 | 319 | 106 | 103/110 | 238->239 |
| 13 | 11 | 2/4 | 319 | 124 | 93/102 | 222->223 |

The JSON ledger records the literal `q`, every dual row and coefficient, the
complete minimum-degree/crossing histograms, and the direct source witness for
each type.

## Replacement-dual ledger

Exact back-substitution through the restricted source-page echelon bases gives
replacement dual support sizes

```text
4:2, 5:3, 6:1, 7:5, 9:1, 10:1, 73:1.
```

Thirteen of the fourteen canonical certificates remain very small; the lone
73-row certificate has degree profile `K14:18, K15:22, K16:33`.  The smallest
representative has support four and the particularly transparent profile
`K14:1, K16:3`, with coefficients `+1,-1,-1,-1`:

```text
+ 08090d151c214c515b5e60757d7d93c0cecedce2f3f7fbfb
- 08090d151c214c515b5e60757d7d93c0ced5dce2f0f7fbfb
- 08090d151c214c515b5e60757d7d93c0ced6dce2f1f3fbfb
- 08090d151c214c515b5e60757d7d93c0ced7dce2f2f3f7fb
```

It annihilates every column on its restricted incident page and pairs the
displayed `K14` head to one.  This is an exact bounded replacement obstruction,
not a full-component dual; no second page is attached.

## Scope

Each test is exact for one canonical literal factorized `q` and hence for its
order-384 factor-stabilizer orbit.  Anchor signatures forget nonanchor labels,
so the result does not automatically cover every non-`H`-equivalent literal
completion of the same signature.  Restricted-page nonmembership is not
full-component nonmembership: columns not incident to the old dual support
may enter a later closure.  No second page, 701-million-row residual,
localization, or other chart is tested.

## Replay

```sh
python3 audit_k16_second_page_duals.py
python3 -O audit_k16_second_page_duals.py
python3 -I -S audit_k16_second_page_duals.py
python3 audit_k16_second_page_duals.py --mutate  # must fail
```

Logical digest:

```text
65ff0ce73034f302ad2022d983b2e366e4d1226c4f1f7b26a7773fe6f1280b66
```
