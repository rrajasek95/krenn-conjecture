# Signed referee of the coloured-necklace reducer

## Terminal verdict

`FAIL_ALTERNATIVE_CUT_DIAMOND__NO_FULL_SEPARATOR`.

The original reducer used `Counter += Counter()` to remove zeros.  In Python
that operation removes every nonpositive entry, so its singleton normal form
was not signed arithmetic and is retracted.  The independent signed-vector
replay retains the same target-rooted DAG (`14,848` states and `4,141`
selected triangular relations), but the target normal form has support
`10,354` and L1 norm `3,978,533,376`.

The selected relations remain a sound terminating subsystem: each has `105`
perfect-matching terms, a coefficient-one leading parent, and strictly fewer
cycles in every other term.  Its rank is therefore exactly `4,141`, and a
479-state terminal-coordinate dual kills all selected relations while pairing
the target by `-8,467,968`.  This proves only nonmembership in that selected
subsystem.

The second distinct cut relation already breaks confluence.  At
`00.00.11112222.000011112222`, cuts `(0,0,0,0)` and `(0,0,0,1)` give signed
normal forms of support `20` and `19`; their difference has support `27` and
L1 norm `140`.  Thus their common leading state cancels while the proposed
normal-form dual does not.  A valid separator would instead require global
confluence or a dual checked on the inverse-parent/full relation closure.

## Literal source guard

The failed diamond is not merely an artifact of the unlabelled abstraction.
An explicit labelling of all 24 `(site,colour)` ports realizes the two cuts as
literal mixed source columns with words `00001202` and `00001200`.  Each has
exactly `105` literal outputs and the same coefficient-one parent.  Their
difference is an actual source syzygy: the parent cancels, leaving support
`180` and L1 norm `180`.

## Projection to Generic's 28 c6 boundary rows

The same literal parent-cancellation mechanism was enumerated on the frozen
28-coordinate c6 interface.  After H-canonicalizing the 28 WD representatives,
the `374` high-cycle K16 parents supply `14,816` literal source columns and
`303,870` two-column critical pairs.  Their `102` distinct primitive projected
vectors cover all 28 coordinates and have exact Q-rank `28`; adjoining the
28-coordinate target leaves the rank `28`.  Thus this boundary vector is in
the projected literal-syzygy span.  This is only a finite boundary projection,
not a global Schur closure or K16 membership statement.

One exact rational solution uses 26 of the 102 pair vectors.  Lifting those
pairs through their complete K<=16 source tails produces exterior support
`2,043`.  Applying 124 certified triangular c>=7 pivots leaves support `3,713`:
eight new unpivotable c7 rows (`K13:2`, `K14:4`, `K15:2`) and `3,705` c<=6
rows.  The backward feed therefore does not close; it exposes the next c7
boundary.

The eight rows all have cycle partition `2+2+2+2+2+2+12`.  Across their 294
incident mixed perfect-matching divisors (278 distinct literal columns), every
divisor meets exactly three port cycles—never four.  This is the exact reason
the certified distinct-cycle pivot fails at K13/K14/K15.  On the eight-row
projection the direct columns have rank 8.  More sharply, 99 shared literal
c>7 parents yield 344 critical pairs and five primitive vectors of rank 4;
the eight-row residual already lies in that rank-4 span.  Exterior tails are
again outside this projection and remain unresolved.

Lifting that rank-4 solution (deliberately not using the direct rank-8 fill)
needs only two common-parent pair vectors.  Its complete K<=16 exterior has
support `308` and contains no c>7 rows, hence no further certified high pivot
applies.  The next frontier is 24 c7 rows (`K15:20`, `K16:4`) plus 284 lower
rows (`K14c6:8`, `K15c5:16`, `K15c6:44`, `K16c5:128`, `K16c6:88`).  The
backward syzygy therefore moves the obstruction from 8 to 24 c7 coordinates;
it does not close it.

The 24-row frontier is genuinely new under the H action: it has no exact orbit
intersection, no equal anchor-stripped skeleton, and no one-sided K-shift
nonanchor divisibility against either earlier packet.  It splits evenly among
`2^5+3+11`, `2^5+4+10`, and `2^5+5+9`.  Unlike the preceding eight rows, all
24 now admit a certified four-distinct-cycle pivot.  Their 880 incident mixed
columns select 2, 3, and 4 cycles with multiplicities 48, 568, and 264.

Applying the 24 certified c7 pivots eliminates the entire c>=7 frontier.  The
result is an 884-row c<=6 packet:
`K13c6:6`, `K14c6:14`, `K15c5:100`, `K15c6:64`, `K16c4:144`,
`K16c5:324`, and `K16c6:232`.  Only two H-orbits overlap the original 28-row
c6 boundary, so this is predominantly a new, larger lower frontier rather
than a recurrence closure.

Applying the same four-distinct-cycle criterion to every row of that packet,
regardless of its cycle count, initially classifies 266 rows as pivotable and
618 as unpivotable.  One exact descending page uses 620 certified pivots
(`c6:190`, `c5:192`, `c4:238`); its support peaks at 4,612 and terminates at a
4,568-row packet on which no certified four-distinct-cycle pivot remains.  The
terminal cycle histogram is `c1:144`, `c2:1320`, `c3:1050`, `c4:1232`,
`c5:696`, `c6:126`; the exact `(K,c)` profile is
`K14:(c3:100,c5:16,c6:14)`,
`K15:(c1:16,c2:24,c3:27,c4:80,c5:138,c6:54)`, and
`K16:(c1:128,c2:1296,c3:923,c4:1152,c5:542,c6:58)`.  All coefficients remain
integral (L1 norm 1,754,112, maximum absolute value 384).  This is the exact
terminal scope of the present Morse rule, not an ideal-membership verdict.

This also resolves the apparent conflict with Tail's rank-zero result.  Tail's
1,114-column calculation is the deterministic *forward* c>=7 Schur projection.
The rank-28 vectors here are differences of two columns sharing, and cancelling,
an omitted higher-cycle parent: they are backward critical-pair feeds, not
direct-column images.  Their nonzero exterior residual is the load-bearing
distinction.

## Replay

```text
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_frozen_necklace_rewrite.py
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_first_diamond_literal_realizability.py
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_c6_boundary_literal_critical_pairs.py
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_c6_boundary_schur_lift.py
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_unpivotable_c7_boundary.py
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_c7_pair_schur_lift.py
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_boundary_recurrence.py
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_c7_pair_schur_lift.py --reduce-c7
python3 computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/audit_general_cycle_pivot_page.py
```

Results:

- signed referee logical digest:
  `09d33720b384017d8b8876554f4e3eff27622903ed3ed506d4da4fca34aa9948`;
- literal realization logical digest:
  `7b14de1a589ccd9cbf6964a8b122c7b77352136650ae91991c7df149071a895a`;
- c6 projection logical digest:
  `73f833a3404d2bc2f1a3a4162ba928e29497d458a08acf82c88ec903ff0bfee5`;
- lifted Schur page logical digest:
  `d53aad470b3db200ee0c9311548e237b7a748bfd9e5f25dd501ac902a75b73ff`;
- relative eight-row interface logical digest:
  `f0a879fbf0e7a25574f37bc1ef0c164e15fb66bb37f41896468a418423b8743c`;
- rank-4 pair lift logical digest:
  `c0cde2fba35dc9d6fa6ba39ba9f9524a6d7d106b3f0cc102d23a061a3522482a`;
- recurrence audit logical digest:
  `6f78a34724c6952de86cad5b6a258dff0a5481cebba568b1526566a840487a32`;
- certified c7 reduction logical digest:
  `e596e36bb447d354a94e60f11e1e291b729615763d9abff48122ae1035c38ecb`;
- general cycle-pivot page logical digest:
  `1398af98cb9c2d3a4b747f13c4e5e4ba4eeedef869c44bbcf580e46da20e838f`.
