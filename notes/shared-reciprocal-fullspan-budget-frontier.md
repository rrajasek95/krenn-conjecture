# The shared-reciprocal full-span frontier starts at budget thirteen

## 1. Result

The residual full-span side of the shared-reciprocal-pair argument does not
contain a rank-budget-twelve packet.  That layer was already eliminated by a
committed exact theorem chain:

1. the site-response four-cover gives
   \(\sum_{u=1}^6\dim W_u\ge 12\);
2. at equality, the coordinate-plane mixed-packet obstruction removes the
   case in which every \(W_u\) has dimension at most two;
3. with a rank-three site, Proposition 5.1 of
   [`full-rank-site-response-invisibility-countermodel.md`](full-rank-site-response-invisibility-countermodel.md)
   gives the three profiles
   \[
      (n_3,n_2,n_1)=(1,4,1),(2,2,2),(3,0,3),
   \]
   makes the three omission pairs distinct, and reduces them to the
   wedge-plus-disjoint, path, and triangle geometries;
4. the path and triangle are excluded by
   [`rank-budget-path-triangle-exposed-grid-obstruction.md`](rank-budget-path-triangle-exposed-grid-obstruction.md),
   and the wedge is excluded without a support assumption by
   [`wedge-equality-hole-block-resolution.md`](wedge-equality-hole-block-resolution.md).

Thus the equality layer is coefficient-empty, which is stronger than a
maximal-envelope support test.  In particular, for two overlapping
reciprocal-pair deletion charts, **each chart separately has rank budget at
least thirteen**.  It is not enough that only one chart leave equality.

The first strict-excess layer has exactly **nine** normal forms modulo the
six residual sites and three target colours.  Five are coordinate target-span
forms with colour-cover sizes \((5,4,4)\); four have cover sizes
\((4,4,4)\) and one rank-one target span enlarged by one transverse
direction.  The latter point is important: a rank-two target span cannot
acquire a transverse third direction while continuing to omit the remaining
target axis, since the local target space is three-dimensional.

This is the smallest surviving full-span packet.  Compatibility between the
two overlapping charts' nine forms is the next finite problem; the present
result does not claim that any of those forms is coefficient-feasible.

## 2. Why budget thirteen has only two strata

Let

\[
 r_u=\#\{i:e_i^{(u)}\in W_u\},\qquad d_u=\dim W_u.
\]

The full-nine four-cover gives

\[
              \sum_u r_u\ge 12,
       \qquad r_u\le d_u,
       \qquad \sum_u d_u=13.                    \tag{1}
\]

If \(\sum r_u=13\), equality \(r_u=d_u\) holds sitewise.  Every \(W_u\)
is therefore precisely the span of the target axes it contains.  There are
five omitted site-colour incidences in total, and no colour can be omitted
at more than two sites.  Hence the omission multiplicities are \((2,2,1)\),
or equivalently the cover sizes are \((4,4,5)\).

If \(\sum r_u=12\), every colour cover has size exactly four and
\(\sum(d_u-r_u)=1\).  There is a unique excess site.  Site cover gives
\(r_u\ge1\).  The excess site cannot have \(r_u=2,d_u=3\), because then
\(W_u\) is the complete three-dimensional target space and contains the
third target axis too.  Thus it has \(r_u=1,d_u=2\): one target line and one
genuinely transverse line.

In either stratum, writing \(n_j=\#\{u:d_u=j\}\) gives

\[
 n_1+n_2+n_3=6,qquad n_1+2n_2+3n_3=13,
\]

so \(n_3=n_1+1\).  The only rank profiles are

\[
                  (1,5,0),\qquad(2,3,1),\qquad(3,1,2). \tag{2}
\]

## 3. Exact orbit census

Encode a site by a three-bit omission mask.  In the transverse stratum, mark
the unique mask of weight two whose target line is enlarged.  Sorting the
six site records quotients by \(S_6\); minimizing over the six colour
permutations quotients by \(S_3\).

The exact labelled and orbit counts are:

| stratum | profile \((n_3,n_2,n_1)\) | labelled | orbits |
|---|---:|---:|---:|
| coordinate, cover \((5,4,4)\) | \((1,5,0)\) | 540 | 1 |
| coordinate, cover \((5,4,4)\) | \((2,3,1)\) | 2160 | 2 |
| coordinate, cover \((5,4,4)\) | \((3,1,2)\) | 900 | 2 |
| one transverse, cover \((4,4,4)\) | \((1,5,0)\) | 1080 | 1 |
| one transverse, cover \((4,4,4)\) | \((2,3,1)\) | 2700 | 2 |
| one transverse, cover \((4,4,4)\) | \((3,1,2)\) | 360 | 1 |
| **total** |  | **7740** | **9** |

The five coordinate representatives, written as sorted omission masks, are

```text
000 000 000 001 011 110
000 000 000 001 110 110
000 000 001 001 010 110
000 000 001 010 011 100
000 001 001 010 010 100
```

The four transverse representatives are

```text
000 000 000 011 101 110*
000 000 001 001 110 110*
000 000 001 010 101 110*
000 001 001 010 100 110*
```

where `*` marks the unique enlarged rank-one target span.  These are normal
forms for one deletion chart.  The common residual sites and distinguished
chords of two overlapping reciprocal charts still impose compatibility
conditions between two such rows; that coupled orbit census is not asserted
here.

## 4. Reproducible audit and scope

Run

```bash
python3 computations/verify_shared_reciprocal_fullspan_budget_frontier.py
python3 -O computations/verify_shared_reciprocal_fullspan_budget_frontier.py
```

The checker pins the five committed dependencies, independently reconstructs
the 2,280 labelled / three-orbit equality census, and enumerates all 7,740
labelled / nine-orbit budget-thirteen forms.  Both modes produce ledger

```text
0be34806754fdb6f63a777f9cc57da25984a40489c8156166dcdb2228394a54c
```

The equality algebra is inherited from the pinned exact checkers rather than
re-proved in this lightweight combinatorial audit.  The new conclusion is a
sharp finite frontier, not a closure of budget thirteen or of the full
shared-reciprocal branch.
