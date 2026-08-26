# Exact literal orbit-zero \(K^{16}\) collection

## Verdict

The provenance-safe \(K^{14}\to K^{16}\) reduction does **not** close or
compress orbit zero.  After literal coefficients are collected, the residual
is nonzero and has 1,848,174 orbits under the order-384 factor stabilizer,
covering 701,717,184 labelled rows.  The earlier 25-orbit result survives only
after forgetting the 16 nonanchor labels; it is not a small literal packet.

This terminally retires literal expansion of this filtered route as the next
proof step.  It is a negative complexity result, not evidence that the target
ideal is nonunit.

## Exact construction

The checker starts from the frozen leading polynomial

\[
  -R'_8 E_{0,2}E_{1,2}E_{2,2}
\]

on the orbit-zero chart.  For every literal \(K^{14}\) row it averages over
all 78 mixed \(K^0\) singleton pivots whose irreducible \(K^{16}\) signature
tails lie in the frozen exact 25-signature cover.  Each pivot carries its
literal twelve-row \(K^2\) tail packet.  Coefficients are collected before
projection to anchor signatures, and rows still divisible by a \(K^0\) mixed
singleton are then discarded.

The pivot rule is equivariant under the full factor stabilizer.  This gives a
canonical result relative to the frozen 25-signature cover, while preserving
every source label used in the reduction.

## Census

| quantity | exact value |
|---|---:|
| input \(R'_8\) stabilizer orbits | 485 |
| input \(R'_8\) labelled rows | 148,176 |
| leading packet rows | 1,728 |
| factored stabilizer-slice pairs | 838,080 |
| literal pivot uses | 6,619,280 |
| reducible \(K^{16}\) tail occurrences | 75,691,040 |
| irreducible occurrences before collection | 3,740,320 |
| nonzero literal orbits after collection | 1,848,174 |
| anchor-signature orbits after projection | 25 |
| labelled support after collection | 701,717,184 |

The literal orbit-size histogram is

```text
24:       24
48:       36
96:      394
192:  40,872
384: 1,806,848
```

The residual is therefore overwhelmingly generic under the stabilizer; the
25 projected signatures hide rather than remove the literal complexity.

## Scope

This audit treats one canonical stabilizer-equivariant reduction on orbit
zero.  It does not prove pivot-independence, does not add unrecorded lower
filtration initial forms, and does not address the other 30 pure-matching
charts.  Its valid conclusion is narrower and decisive: the proposed literal
\(K^{16}\) expansion is not a bounded proof certificate.

## Replay

```bash
python3 computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/collect_orbit0_k16_literal_residual.py
```

The committed exact output is
`results_orbit0_k16_literal_residual.json`.  Its logical SHA-256 is
`8eb9f7dbb220afd759533c10a4881a502a43bdb3bfa28c36e3b89cf98a4ee58c`.
The script SHA-256 is
`05f194e27220bacc48c43a9076cab30732462a4d1f42e5ae93623409c4b8500c`;
the result-file SHA-256 is
`28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189`.
