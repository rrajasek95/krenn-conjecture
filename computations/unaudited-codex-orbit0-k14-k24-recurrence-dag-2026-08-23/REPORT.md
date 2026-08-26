# K14--K24 recurrence/provenance DAG

## Verdict

The ordered-shift recurrence is now explicit and machine checked at the
12-anchor-signature level.  There are 324 syntactic lineage nodes and 321
reachable nodes.  The complete required reachable-lineage counts at
K20--K24 are respectively `36,52,76,59,35`.

This is a provenance theorem, not a residual calculation.  It reconstructs
the exact reachable anchor-signature sets and pivot-denominator product
classes, but it does not enumerate any K20--K24 row stream or evaluate a new
charge.

## Missing-parent correction

The DAG makes the frozen omission literal.  The K14 direct packet `222`
emitted a K2 response, but the K16 artifact retained only its irreducible
normal and discarded the pivotable parent stream.  Consequently:

- K18 is missing lineage `D14:222|R:2-2`;
- K19 is missing lineage `D14:222|R:2-3`; and
- all 15 reachable descendants beginning with that discarded response are
  marked `MISSING_DISCARDED_K14_K2_PIVOTABLE_PARENT` through K24.

Therefore the former K18/K19 *full-page* charges and both cumulative charge
ledgers are retracted.  Their explicitly enumerated component scalars remain
exact partial subtotals.  The authoritative correction is
`../unaudited-codex-orbit0-hidden-k14-charge-supersession-2026-08-23/`.

## Exact recurrence

The 27 direct packets are the ordered triples in `{2,3,4}^3`.  A direct packet
has degree `8+sum(shifts)`, coefficient sign `-1`, and literal tail count equal
to the product of `12,32,60` for shifts `2,3,4`.  Every pivot response has
shift `2`, `3`, or `4`, flips the sign, and divides the parent coefficient by
the number of selected pivots.

K14 uses the frozen valid-pivot cover.  K15--K20 uses every literal dividing
pivot.  For every node, the JSON records the reachable signature count, exact
set of denominator products, maximum, LCM, checkpoint evidence, and whether
the parent stream was retained, retained only as a normal/charge, discarded,
or never run.  The depth-three K20 product class and depth-four K24 class both
divide the independently certified scale
`U=400591699200`.

## Completeness guard

`audit_recurrence_dag.py --verify-interface CLAIM.json` accepts a future
K20--K24 interface only when its lineage IDs equal the complete reachable set
for that degree.  Every claimed lineage must also name a coverage kind and a
64-hex evidence digest.  `interface_template_K20.json` is the exact 36-lineage
schema.  `--selftest-complete` passes; `--hostile` deletes one hidden
`D14:222|R:2-2-2` lineage and must fail.

Standard, optimized, and isolated replay agree.  The result logical digest is
`ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66`.

