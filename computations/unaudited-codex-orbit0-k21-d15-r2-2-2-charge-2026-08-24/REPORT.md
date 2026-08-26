# Grouped D15 R2-2-2 K21 charge

Status: `PASS_STRICT_GROUPED_D15_R_2_2_2_K21_CHARGE_AND_INDEPENDENT_257_LITERAL_REFEREE`.

This package covers exactly
`D15:{223,232,322}|R:2-2-2`.  The three packet labels are retained as
source witnesses, but the frozen 485-record R8 orbit masses permute those
labels.  Consequently the only source-faithful output is the grouped scalar;
`individual_id_charges` is deliberately null.

## Exact result

- Scale `U = 400591699200`.
- Scaled full = irreducible charge:
  `-2089490736287288328192`.
- Reduced charge: `-4849716689615104/929775`.
- Source: 485 R8 slices, 6,704,640 direct-K15 heads, signed mass
  `322486272`, literal precollection L1 `3085516800`.
- Recurrence census: 55,934,080 first pivots; 671,208,960 K17 children;
  451,445,760 pivotable K17 children; 1,876,057,600 second pivots;
  22,512,691,200 K19 children; 6,774,666,240 pivotable K19 children;
  11,437,867,520 third pivots; 137,254,410,240 K21 children.
- Exact sign: a direct-K15 term is `-positive`; three response steps flip
  the sign three times, leaving `+positive/(m1*m2*m3)` times the terminal
  cycle charge.  Every observed product divides U exactly.
- All K21 outputs are terminal because the anchor sum is
  `9-4+2-4+2-4+2 = 3`, below the sum 4 of every K0 pivot.  Literal full and
  irreducible counts and charges therefore agree.

## Resource and independent guards

The 32-slice gate took 27.806505 seconds, projected 421.442344 seconds, and
was observed at about 675,600 KiB RSS.  The accepted full pass took
414.206370 seconds with eight workers, under the 600-second/16-GB bounds.

The first full pass intentionally published no partial result when a hostile
L1 guard compared the literal precollection stream (`3085516800`) with the
collected checkpoint L1 (`3083240448`).  Equal-row cancellation explains the
difference; their signed mass agrees.  The corrected guard preserves this
interface distinction in `hostile_l1_guard_evidence.json`.

An independent source rebuild selected the 257 evenly distributed R8 slices
`j*484/256`, cycled across packet witnesses 322/232/223, and found one
nonzero K19-to-K21 continuation in each.  It reconstructed both earlier
pivots literally, checked all divisions, and evaluated 4,116 literal K21
children; every child was terminal.  The TSV preserves all source slice,
packet, factor-tail, pivot-tail, denominator, and charge fields.

The strict audit pins all sources and results, rejects missing, duplicated,
or reordered lineage IDs, and guards against interpreting packet diagnostics
as individual lineage scalars.  Logical SHA-256:
`0cfafb9430b2817532a0c8a424b46bdc7d0286915eebff29717ebf815e07922a`.

Scope stops at this exact grouped K21 scalar.  No K21 rows were retained and
no K22 computation or broader conjecture verdict is claimed.
