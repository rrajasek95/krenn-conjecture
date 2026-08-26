# Global orbit-zero residual interface audit

## Terminal result

The archive does **not** determine a provenance-safe residual iterator from
`K16` through `K24`.  The exact pre-reduction identity is available:

```text
-R8' * E0 * E1 * E2,
R8' supported only at K8,
Ei profile K2:12, K3:32, K4:60.
```

Thus the full input already occupies `K14..K20`; the `E0E1E2` occurrence
profile is

```text
K6:1728, K7:13824, K8:62784, K9:171008,
K10:313920, K11:345600, K12:216000.
```

The frozen `1,848,174`-orbit object was replayed byte-for-byte: its literal
stream SHA-256 is
`f92c91ad239f112185b29ec53157bfb02931b06bf481d71e3878b2c31e298328`.
Its scope is only the irreducible `K2`-tail response obtained by cancelling
the leading `-R8'E0_2E1_2E2_2` `K14` block.  It is not the full filtered `K16`
slice: the latter also has direct `2+2+4` and `2+3+3` input terms.

## Precise missing provenance

The first missing ledger is at `K15`: no source-labelled choice/weight rule
was frozen for reducing the genuine `K15` layer of the full E product.  In
addition, the collector did not freeze a collected `K17/K18` state from the
`K3/K4` tails of its averaged `K14` pivots.  Finally, it discarded
`75,691,040` reducible `K16` tail occurrences modulo the K0 initial ideal
without recording the singleton pivot choices that generate their
`K18..K20` transfer tails.

Consequently the only certified cycle charge is the isolated frozen `K16`
response charge `-311,258,112`.  A charge series by `K` degree is undefined;
choosing new pivots now would define a new normal form rather than reconstruct
the archived one.

## Minimal continuation

Freeze one H-equivariant ascending-K policy beginning at `K15`, recording
every literal pivot coefficient and all `K2/K3/K4` outputs.  Then replay the
full `K16` layer as the sum of the direct E-product input and the `K14` pivot
response before proceeding upward.

Replay:

```text
python3 computations/unaudited-codex-orbit0-global-residual-interface-audit-2026-08-23/audit_global_residual_interface.py --write-results
```

Logical digest:
`e37e85a338fcd16825ea2993fb2f395112dc826c9b76424f9eedcf8d78ad4645`.
