# Exact local closure of the 34-column chart-26 degree-eight antichain

## Outcome

The exact 34-column complement left by the complete degree-five Buchberger
layer has a finite source-labelled local correction.  Twenty-three columns
have globally private degree-eight output rows.  The remaining eleven close
after four explicit exchange/Bockstein residual cells, followed by a
43-row exact rational correction on a `2,995 x 1,846` row-column interface.

This is an exact theorem about the 34-column complement.  It does **not**
contract the other 218 columns of the second boundary and therefore does not
decide `t^8` membership or chart-26 saturation.

## Degree-six source-cell census

The checker reconstructs all 6,558 degree-four leads and 84,005 degree-five
leads.  It tests literal source legs, through every normalized
support-stabilizer translate, rather than comparing only word labels.

| packet | newly touched columns | literal source-leg incidences |
|---|---:|---:|
| degree-six `4--4` cells | 21 | 31 |
| degree-six `4--5` cells | 8 | 10 |
| degree-six `5--5` cells | 0 | 0 |
| untouched by these degree-six cells | 5 | — |

Here *touch* means that the crossing is a translated source leg of the
cell.  It is not silently promoted to an exact correction.

The five degree-six-untouched canonical columns are

```text
12000000 88a7eaf4   profile 611   top multi:C6+P2
12011010 0c4c8ad5   profile 431   top squarefree branched G8
12012000 0e4cbaf6   profile 422   top squarefree branched G8
12111000 7e80b4ea   profile 431   top multi:C4+P2+P2
12111220 808dc4e4   profile 431   top squarefree branched G6+P2
```

All five nevertheless have globally private top rows.  The exact ledger in
[`results_degree8_antichain_cells.json`](results_degree8_antichain_cells.json)
records every one of the 34 word profiles, multiplier/top skeletons,
repeated coordinates, and `4--4`/`4--5`/`5--5` incidence counts.

## Leaf packet and hard eleven

For every top row of every antichain column, the checker exhausts all
degree-eight incident columns.  Exactly 23 antichain columns admit a row
whose global incidence is the singleton containing that column.  Choosing
one per column gives a literal diagonal leaf repair.  The hard eleven have
no such row.

Starting with the 677 top rows of those eleven, exact linear algebra over
`Q`, independently rank-checked modulo `1,073,741,827`, gives:

| round | rows | columns | rank | result | next top rows |
|---:|---:|---:|---:|---|---:|
| 0 | 677 | 792 | 602 | 4-column separator | 224 |
| 1 | 901 | 832 | 663 | 4-column separator | 256 |
| 2 | 1,157 | 988 | 846 | 5-column separator | 430 |
| 3 | 1,587 | 1,352 | 1,144 | 22-column separator | 1,408 |
| 4 | 2,995 | 1,846 | 1,694 | exact 43-row solution | — |

The four separator target pairings are respectively `2,2,-2,2`.  Thus they
are not output-free syzygies: they are the successive target-relevant
boundaries of the exact normalized residual from the full-source
degree-five pure-product lift.  Every residual polynomial and all terminal
row coefficients are frozen literally in the result JSON.

Combining the 23 leaf weights with the 43-row hard correction annihilates
all 1,867 degree-eight columns incident to the packet, including all 34
antichain columns.  Canonical invariant rows and normalized column-orbit
expansions make the packet complete under the chart support stabilizer.

## Gain-graph/theta audit

On the rows admitted at each obstructed round, every active row meets
exactly two separator columns and both entries are `+1`.  The separator
signs are a nonzero vertex potential.  The four induced gain graphs have

```text
(vertices,edges,components,cycle-rank)
  (4,4,1,1), (4,3,1,0), (5,4,1,0), (22,40,1,19).
```

Consequently every edge gain is an exact coboundary, every cycle is
balanced, and the biased-graph theta axiom holds literally.  This explains
the small signed exchange cells, but it is not a general NBC/Orlik--Solomon
termination theorem: rounds 1 and 2 are trees, and the exterior residual
rows create a new graph rather than straighten inside the old cycle
matroid.  The finite closure above is therefore the exact positive lemma;
no universal finite-generation claim is made.

The all-twelve-support-cells-equal-one presentation is legitimate for this
localized mixed-ideal/pure-product radical question by
[`n8-support-normalization-is-exact-localization.md`](../../notes/n8-support-normalization-is-exact-localization.md).
It does not assert that the three pure amplitudes may simultaneously be
set to one in the physical fibre.

## Replay and scope guards

```text
python3 audit_degree8_antichain_cells.py --check-results
python3 -O audit_degree8_antichain_cells.py --check-results
python3 -I -S audit_degree8_antichain_cells.py --check-results
python3 audit_degree8_antichain_cells.py --mutate   # must fail
```

Logical result digest:

```text
4b33611aa61c89ea34de63a4a07b002d0dfde8c7960151a88d888efb305edea2
```

The checker deliberately keeps the remaining 218-column contraction and
every degree-nine-or-higher question outside its conclusion.
