# K16 23-row dual: literal class identification

## Verdict

The new exact 23-row `K10..K16` cochain is **not** merely the archived
cutoff-nine separator in a different representative.  It has an eight-row
shadow of the old class, but also a literal 15-row component outside the full
labelled cutoff-nine and sparse `R8'` product support.  The precise verdict is
`GENUINELY_NEW_CLASS_WITH_OLD_EIGHT_ROW_SHADOW`.

This is a bounded comparison theorem only.  It attaches no new incident
source page.

## Old overlap and exact H-module counterguard

Expanding the frozen interfaces gives:

- cutoff-nine 37-row dual: 69,264 labelled rows;
- sparse `R8'`: 148,176 labelled rows;
- intersection: exactly 2,304 rows, one full `S8 x S3` orbit, with coefficient
  `+1` in both interfaces.

Exactly eight of the 23 new rows are divisible by an old labelled row.  In
every case the divisor is the same literal row
`080915515e7d93c0cedce2fb`, lying in that unique common orbit.  The other 15
rows have no divisor anywhere in either complete old labelled support.  Only
one of the eight quotient monomials belongs to the frozen 1,728-row `K6`
packet.

Under the factor stabilizer `H` of order 384, all 23 seed rows have free,
pairwise-distinct orbits.  Hence the old-shadow span and the new-residual span
each have exact rank 384 and occupy disjoint `H`-stable coordinate blocks;
their direct sum has rank 768.  This rules out an old separator product or an
`H`-transport as the full new cochain.

## K14/K16 transfer comparison

At the canonical type-6 factorized head there are five same-head raw tail
columns.  Their exact rank is 5 and their four differences have rank 4.  The
new functional evaluates every raw tail at `-1`, so each actual `q+B_p`
source column pairs zero, and every transfer difference pairs zero.

After the archived second-singleton reduction, the five tail columns have
rank 4, their differences rank 3, and the new functional pairs every one with
zero.  Thus the class is a persistent descendant with respect to this local
same-head transfer, even though its literal 15-row summand is new.  It has no
direct row overlap with the old type-6 literal dual and shares only `q` with
the preceding four-row replacement dual.

## Six-site-fibre guard

The count 15 is not one translated six-site perfect-matching fibre.  Such a
degree-24 fibre would share a degree-21 multiplier before its three-cell PM
terms.  The 15-row residual has maximal common multiset factor of degree only
11; one explicit pair already has gcd degree only 16.  This is invariant under
`H`, and also excludes a signed puncturing of one common PM6 fibre.

## Replay

Run:

```text
python3 computations/unaudited-codex-orbit0-k16-dual-class-identification-2026-08-23/audit_k16_dual_class_identification.py
python3 -O computations/unaudited-codex-orbit0-k16-dual-class-identification-2026-08-23/audit_k16_dual_class_identification.py
python3 -I -S computations/unaudited-codex-orbit0-k16-dual-class-identification-2026-08-23/audit_k16_dual_class_identification.py
```

All three modes pass identically.  `--mutate` changes the coefficient of `q`
and must fail the exact same-head transfer check.

Logical digest:
`720d7ff3507221b4074e198bc838f58b804444302c934d29d45997ea3f113a81`.

