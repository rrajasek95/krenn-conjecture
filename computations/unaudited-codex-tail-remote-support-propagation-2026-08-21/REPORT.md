# Remote tail support propagation

Status: **exact support audit PASS; fixed-point enumeration stopped by the
prescribed 500-orbit guard**.  No coefficient solve was launched, and no
support-only cap-activity inference is made.

## Literal transported rows

The `B4 x S3` orbit of `F_02222212` has 144 rows: 24 cross-block exceptional
edges times six ordered exceptional-colour assignments.  Its stabilizer has
order 16.  Every row is expanded from the 105 literal perfect matchings as

```text
15 linear terms + 90 quadratic terms.
```

For exceptional endpoint colours `i,j` and majority colour `k`, this gives
the exact conditional support implication

```text
a_uv_ij != 0 and h^k_uv != 0
  => at least one of the 90 literal quadratic monomials is live.
```

There are 30 distinct cross-factor pairs among the 90 monomials.  The result
JSON freezes all 144 source labels and their cofactor atoms.

The projected graph has 168 cross-colour cell atoms.  The 611 orbit alone has
one 144-node cross-block SCC and 24 same-block sinks, 1,728 arcs, and 720
mutual two-cycles in two orbits.  The faithful two-factor clauses have one
144-member orbit of terminal size-3 supports and one 576-member orbit of
two-source size-4 supports.

## X5 sink orbit and first shell

The terminal representative is

```text
{a_06_01, a_01_02, a_67_12}.
```

The two same-block cells activate the `B4 x S3` orbit of `F_00112212`.
That orbit also has 144 rows, six per same-block sink cell.  The live anchor
matching is one term, so X5 forces one of the other 104 literal matchings.
The per-row cross-degree histogram is `1:9, 2:18, 3:42, 4:36`.

Adding this orbit makes all 168 atoms one projected SCC with 4,056 arcs.  It
kills the 611-only terminal support internally: across its 144 translates,
zero of 1,728 sink clauses has an alternative term supported inside the
three cells.

For the canonical terminal support, exact minimum-union search of its twelve
sink clauses proves that at least six new cross cells are required.  There
are 484 labelled minimum supports (nine total cross cells) and 75 orbits
under the order-16 terminal stabilizer.  The orbit-size histogram is

```text
1:6, 2:15, 4:8, 8:40, 16:6.
```

Every orbit record includes twelve literal source/matching witnesses and
their diagonal factors, making it suitable as a coefficient-unit seed.

## Existing support routing and stop certificate

Six of the 75 first-shell orbits are compatible with an aligned frozen
support-6 diagonal signature (indices `3,6,17,39,51,74`).  Conditional on
coefficient compatibility, those enter the existing support-6
arbitrary-mate closure.  No source-labelled support-8 signature interface is
frozen in the tail package, so no support-8 match is asserted.  Active-cap
status is a rank/row-span condition and is not decided from support.

The remaining propagation cannot be kept below the requested 500-orbit
threshold.  First-shell orbit 56 is not aligned-support6-compatible.  On the
all-live diagonal support—an exact support-level witness for the
pure/permanent/triangle clauses—it has four new must-fire 611 sources:

```text
a_07_01, a_16_01, a_17_12, a_17_20.
```

Each has ten inclusion-minimal rescue choices after already-live factors are
removed.  Their Cartesian unions give 10,000 distinct inclusion-minimal
labelled branches, with added-cell histogram

```text
4:625, 5:2500, 6:3750, 7:2500, 8:625.
```

Since the terminal stabilizer has order 16, this is at least 625 orbits from
one first-shell representative alone.  The fixed-point expansion therefore
stops at the mandated guard.  This is a finite exact obstruction ledger, not
a support-only proof or counterexample: all implications remain conditional
on the displayed cofactors, and coefficient cancellation has not been
solved.

## Replay

```sh
python3 computations/unaudited-codex-tail-remote-support-propagation-2026-08-21/audit_tail_remote_support_propagation.py --write-results
python3 -O computations/unaudited-codex-tail-remote-support-propagation-2026-08-21/audit_tail_remote_support_propagation.py --write-results
python3 -I -S computations/unaudited-codex-tail-remote-support-propagation-2026-08-21/audit_tail_remote_support_propagation.py --write-results
```

