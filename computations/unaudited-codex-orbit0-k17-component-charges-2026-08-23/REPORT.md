# Exact K17 component cycle charges

The two missing cancellation components were evaluated without collecting rows.  The evaluator removes a K0 head, contracts the remaining four path segments by DSU, looks up the resulting 77-cycle functional, and separately tests K17 K0-pivotability from the exact 12-anchor signature.

## Result

All values use the actual telescope sign.  `full = pivotable + irreducible`.

| component | full charge | K0-irreducible charge | K0-pivotable charge |
|---|---:|---:|---:|
| A: K14 cancellation, valid-pivot average, K3 tails | `-126414770788352/150535` | `-323083776` | `-77779354568192/150535` |
| B: K15 cancellation, all-dividing-pivot average, K2 tails | `-50760912704768/21505` | `-7224300090368/6545` | `-189167486854912/150535` |

Adding the independently frozen direct irreducible K17 charge `-62386176` gives

`-9747200926208/6545`.

The full-A/B bookkeeping sum with that same direct irreducible term is `-491132462725888/150535`; it is included only as a charge partition check.

## Exact guards

- A: `6,619,280` valid-pivot uses and `211,816,960` K3 tail occurrences.
- B: `5,311,211` K15 checkpoint rows and `532,114,572` K2 tail occurrences.  The complete pivot-count histogram is checked.
- Global clearing scale: `3,612,840`, divisible by every averaging denominator.
- The irreducible A/B values and their sum reproduce the independently frozen collected-row checkpoint exactly.
- Standard, `-O`, and `-I -S` replays have logical digest `11cfdaa2780d3f0d3f6301e494748d1d8cbdbb68f570ae7aa26b15f28c7091bd`; the hostile coefficient mutation fails.

## Scope

This is an exact linear charge projection and K0-pivotability split only.  It makes no claim about component support overlap, row cancellation, span membership, or K18+ tails.

