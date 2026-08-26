# Exact 77-cycle charge ledger through K18

> **RETRACTED (2026-08-23).** K18 omitted K14 path `[2,2]`, so the cumulative
> and compensating-charge values below are incomplete.  See
> `../unaudited-codex-orbit0-hidden-k14-charge-supersession-2026-08-23/REPORT.md`.

## Verdict

The deterministic filtered normal has cumulative charge

```text
10,842,661,512,448 / 6,545
```

through K18.  Since the original structured `a*T` has charge zero and the
77-functional annihilates every complete balanced 105-term source column, a
completed reduction must carry aggregate K19–K24 normal charge

```text
-10,842,661,512,448 / 6,545.
```

This is an exact conservation requirement, not a prediction of how the charge
splits by degree and not a proof that the deterministic completion terminates
with a particular support.

## Degree ledger

| normal page | exact 77-charge |
|---:|---:|
| K14 | `0` |
| K15 | `0` |
| K16 | `375,127,296` |
| K17 | `-9,747,200,926,208/6,545` |
| K18 | `2,590,664,898,048/935` |
| **K14–K18 cumulative** | **`10,842,661,512,448/6,545`** |
| **required K19–K24 aggregate** | **`-10,842,661,512,448/6,545`** |

On common denominator 6,545, the three nonzero numerators are

```text
K16  +2,455,208,152,320
K17  -9,747,200,926,208
K18 +18,134,654,286,336
sum +10,842,661,512,448.
```

## Lower-page zero guards

- The dependency theorem `a*T in I_mix + K^14` supplies no K0–K13 normal.
  This package pins but does not replay that earlier reduction.
- Every K14 head is canceled by the frozen valid-pivot rule, and every response
  tail raises K-degree by at least two.  Hence no K14 normal remains.
- The exact K15 checkpoint contains 5,311,211 input H-orbits, all K0-pivotable;
  its reduced checkpoint is empty.  Hence no K15 normal remains.

The K18 entry is Cycle's independently source-refereed **irreducible** K18
charge, not its full pre-projection charge.

## Conservation scope

The charge functional annihilates a complete mixed source column, so subtracting
any signed or rational average of such columns preserves total charge across
all K-degrees.  The current pivot convention is H-equivariant but is not known
to be confluent or policy-independent.  Therefore the compensating value is
conditional on completing this same deterministic convention; another valid
pivot policy may redistribute intermediate page charges, although its fully
completed total must still be zero.

The required higher charge includes all future normals produced by:

- K17 pivots, whose first tails occur at K19;
- K18 pivots, whose first tails occur at K20;
- subsequent reductions through maximal K-degree 24.

It does not assert that any one page or support class carries the entire value.

## Replay and provenance

Run `audit_charge_ledger.py`.  It reads only frozen result ledgers and uses
exact `Fraction` arithmetic.

- result logical SHA-256:
  `14654799570c15330d08c585f88712cac36b91649be87b727fe2510c1ee9dc4f`;
- K16 input result SHA-256:
  `ff4505a44cc76894ede59f4c642d385cf21ecffd5ac0aae875f7652c4966b861`;
- K17 input result SHA-256:
  `b0918e220738c8818746f654fdfc4d2cc60a9f6269a3fb34da36eb84bf5dad49`;
- corrected K18 input result SHA-256:
  `eff58152c9b465b4fa770642898ada990f682bc677dac9363374f54aa65d5d47`;
- original structured-target referee SHA-256:
  `9418fda557577fdf8828bf9a3faba595fba17c32e23c12ea8e9bccff8788d1aa`.
