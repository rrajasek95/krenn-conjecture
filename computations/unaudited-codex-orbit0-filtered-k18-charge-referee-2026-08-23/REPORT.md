# Independent K18 charge-only source referee

> **RETRACTED AS A FULL K18 CLAIM (2026-08-23).** The four enumerated component
> charges below remain exact partial subtotals, but K14 path `[2,2]` was omitted.
> See `../unaudited-codex-orbit0-hidden-k14-charge-supersession-2026-08-23/REPORT.md`.

## Verdict

`PASS_WITH_SCOPE_CORRECTION`.  The load-bearing K18 charge is exact under the
stated deterministic pivot policies.  The four component formulas, telescope
signs, global denominator clearing, child-pivotability test, enriched cache key,
and signed-zero handling are sound.  The exact K18-irreducible charge remains

```text
2,590,664,898,048 / 935.
```

One non-load-bearing occurrence description must be corrected: `44,342,881`
is the number of pivot uses on the **collected K15 H-orbit representatives**,
not an “already-irreducible K17 child count.”  The driver’s `55,934,080` is the
precollection compact source-pair pivot-use count.  Consequently the displayed
component occurrence totals mix compact levels and are engineering/cost counts,
not a uniform literal-row census.  This does not affect any charge because the
response functional is H-invariant and linear.

## Four components and signs

For `P=-R8' E0 E1 E2`, literal cancellation of a parent coefficient `p`
produces response tails with coefficient `-p`.

1. Direct K18 is
   `-R8'*(three E2E4E4 orders + three E3E3E4 orders)`: negative sign.
2. K14/K4 uses the frozen 25-cover-valid pivot average.  The K14 parent has
   coefficient `-r`, hence its K4 response is `+r/choices`.
3. K15/K3 uses every dividing K0 pivot.  Direct K15 again has coefficient
   `-r`, hence response `+r/choices`.
4. K16/K2 first merges the exact parent coefficient as
   `v = direct - frozen_stored_response`, matching the corrected K16 telescope.
   It then uses `-v/choices`.  Rows with `v=0` are explicitly skipped before
   pivot selection.

K17 cannot feed K18 because the smallest tail increment is two; its first
response page is K19.

## Exact arithmetic

The driver uses signed `i128` with global scale `281,801,520`, the LCM of every
possible nonzero pivot count on the 4096 anchor supports.  Therefore K14, K15,
and K16 divisions on this page are exact.  The K14 and K16 divisions have
explicit remainder assertions.  K15 lacks the same runtime assertion, but its
divisor belongs to the pinned pivot-count set, so this is a replay-hardening
omission, not truncation in this result.

The component charges replay as:

| component | full charge | K18-irreducible charge |
|---|---:|---:|
| direct | `-272,994,816` | `-95,224,320` |
| K14/K4 | `502,619,274,240/4,301` | `2,000,304,128/35` |
| K15/K3 | `278,243,265,136,128/150,535` | `7,884,015,145,472/6,545` |
| K16/K2 | `830,890,978,048/385` | `617,636,790,784/385` |
| total | `82,802,576,789,248/21,505` | `2,590,664,898,048/935` |

## Cache-key proof

For a parent and pivot, deleting the four anchor edges leaves four paths plus
closed cycles.  The cache profile retains:

- the pairing of the eight pivot-labelled path endpoints;
- every endpoint-labelled path length;
- the sorted closed-cycle lengths;
- the parent 12-anchor signature;
- pivot identity and tail degree.

For a fixed pivot tail, this determines the child cycle partition, hence its
77-functional value.  The parent signature, pivot, and tail determine the child
anchor signature, hence whether it remains K0-pivotable.  No colour or internal
path data omitted by the key can affect either queried scalar.

## Counter/sign guards

- The Rust driver contains no `Counter`-style positive-only merge.
- Direct/K14/K15 contributions are accumulated linearly as signed `i128`
  scalars, so precollection duplicates and cancellations are safe.
- K16 is merged row-by-row with `direct - frozen`; exact signed zeros are
  removed before response evaluation.
- The K4 exporter writes literal source tails without coefficient collection.
- Pinned input hashes protect the two auxiliary binaries, although the driver
  should additionally assert their magic headers in a future replay.

## Occurrence-count scope correction

The full driver assertions are internally correct for its chosen stream:

- direct terms: `152,251,200`;
- K14/K4 precollection compact tails: `397,156,800`;
- K15/K3 precollection compact tails: `1,789,890,560 = 55,934,080*32`;
- K16/K2 collected-parent tails: `1,559,270,244`.

The earlier `44,342,881` K15 count is independently the sum of pivot counts on
the `5,311,211` collected K15 H-orbit representatives.  Neither that number nor
`55,934,080` is an irreducible K17-child count.  The mixed compact-level total
must not be used as a row-support or rank statement.

## Artifacts and scope

Load-bearing files:

- `computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs`,
  SHA-256 `24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045`;
- `results_k18_charge_raw.json`, SHA-256
  `1237988e4c80ba2aaca706e98b93f5a8e9f08ed69a25632823c3c7b552e27f16`;
- finalized `results_k18_charge.json`, byte SHA-256
  `eff58152c9b465b4fa770642898ada990f682bc677dac9363374f54aa65d5d47`,
  logical SHA-256
  `da7f6ccc7638621ca7f13213d40be7e8afe2c38decb3663efbdb1f4ea3408413`.

This validates only the frozen 77-functional before and after projecting away
K18-pivotable children.  It does not collect K18 rows, establish a K18 support
census, emit K20+ tails, or prove ideal membership.
