# Hidden-K14 charge-ledger supersession

## Verdict

The former full K18 charge and cumulative-through-K18 ledger are **retracted**.
The K14/K2 collector discarded 75,691,040 pivotable K16 occurrences without
emitting their later tails.  Hence K14 path `[2,2]` is absent from K18.  The
same gap also makes the former full K19 charge and through-K19 ledger incomplete
because K14 path `[2,3]` is absent.

## Exact retained scope

These stored claims remain exact:

| claim | retained value/scope |
|---|---|
| K14 normal charge | `0` |
| K15 normal charge | `0` |
| K16 normal charge | `375127296` |
| K17 normal charge | `-9747200926208/6545` |
| K18 visible subtotal | `2590664898048/935` for direct, K14 `[4]`, K15 `[3]`, and direct-K16 `[2]` components |
| K19 visible subtotal | `-14857399077330176/1436925` for the six enumerated component families excluding K14 `[2,3]` |
| global denominator scale | `U=400591699200` remains certified |

The component scalars survive because source collection, structural
pivotability projection, and the 77-functional are linear.  They must now be
called partial visible subtotals, not complete page charges.

## Retracted conclusions

The following are no longer load-bearing:

- `K18 = 2590664898048/935` as a **full** normal-page charge;
- cumulative K14--K18 charge `10842661512448/6545` and its proposed
  compensating K19--K24 value;
- `K19 = -14857399077330176/1436925` as a **full** normal-page charge; and
- cumulative K14--K19 charge and its proposed compensating K20--K24 value.

The exact missing inputs are K14 `[2]` pivotable K16 parents with K2 tails for
K18 and K3 tails for K19.  No missing contribution is evaluated here.

Run `audit_hidden_k14_charge_supersession.py` in standard, optimized, or
isolated mode for the machine-readable pinned scope correction.
