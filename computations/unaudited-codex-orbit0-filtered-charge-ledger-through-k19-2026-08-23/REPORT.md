# Exact 77-cycle charge ledger through K19

> **RETRACTED (2026-08-23).** K18 omitted K14 path `[2,2]` and K19 omitted
> K14 path `[2,3]`; the cumulative and compensating-charge values below are
> incomplete.  See
> `../unaudited-codex-orbit0-hidden-k14-charge-supersession-2026-08-23/REPORT.md`.

## Verdict

Under the frozen deterministic averaging convention, the K14--K19 normal
has exact cumulative 77-charge

```text
-137,246,362,298,070,016 / 15,806,175.
```

The original structured target has charge zero, and the 77-functional
annihilates every complete balanced 105-term source column.  A completed
reduction under the same convention must therefore carry aggregate K20--K24
normal charge

```text
+137,246,362,298,070,016 / 15,806,175.
```

This is aggregate conservation only.  It is not a prediction of the charge on
any individual remaining page, a proof that the reduction terminates, or an
ideal-membership statement.

## Exact ledger

| normal page | exact 77-charge |
|---:|---:|
| K14 | `0` |
| K15 | `0` |
| K16 | `375,127,296` |
| K17 | `-9,747,200,926,208/6,545` |
| K18 | `2,590,664,898,048/935` |
| K19 | `-14,857,399,077,330,176/1,436,925` |
| **K14--K19 cumulative** | **`-137,246,362,298,070,016/15,806,175`** |
| **required K20--K24 aggregate** | **`+137,246,362,298,070,016/15,806,175`** |

The arithmetic is exactly

```text
10,842,661,512,448/6,545
  - 14,857,399,077,330,176/1,436,925
= -137,246,362,298,070,016/15,806,175.
```

The K19 term is the independently refereed **irreducible** K19 charge, not the
full prefilter charge.  It uses target `P=-R8prime*E0*E1*E2` and the same rule
that a coefficient `c` emits `-c/m` along each of its `m` chosen pivots.

## Scope and replay

The functional conserves charge only after all filtration pages of a complete
source column are included.  K20--K24 may therefore redistribute or cancel the
displayed requirement arbitrarily among themselves.  Another pivot policy may
also redistribute intermediate page charges; the zero total of a completed
reduction is the policy-independent statement.

Run `audit_charge_ledger.py`.  It reads the frozen through-K18 ledger and the
terminal K19 charge result, checks their exact statuses, convention scope, and
rational arithmetic, then emits the pinned ledger.  `--mutate` is a hostile
arithmetic guard and must fail.
