# Axis purification does not imply toric access to the pure chart

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_chart_torus_accessibility.py`

## Exact weight system

Let `h(v,c)` be a site/colour cocharacter.  Introduce a scalar source-gauge
weight `mu` and explicit pure-target weights `T0,T1,T2`.  A source cell
`(uv;a,b)` has relative weight

```text
ell(uv;a,b) = h(u,a)+h(v,b)-mu.
```

The twelve cells of the endpoint-minor pure chart are required to have
`ell=0`.  Target compatibility is imposed without suppressing target
weights:

```text
Tc = sum_v h(v,c),       Tc = 4*mu,       c=0,1,2.
```

The second equality is the degree-four source scaling needed to keep the
three exact pure outputs after shifting retained source cells by `mu`.  The
complete rational system has `28` variables, `18` displayed equations,
rank `15`, and solution dimension `13`.

## Minimal leading-support obstruction

Adjoin just two internal mixed cells to the chart support:

```text
01:02,       34:02.
```

Their source characters obey the literal four-port circuit

```text
chi(01:02) + chi(34:02)
  = chi(03:00) + chi(14:22),
```

where both cells on the right are retained pure-chart anchors.  Therefore

```text
ell(01:02) + ell(34:02) = 0.
```

A finite toric limit on a source containing both extras requires both
relative weights to be nonnegative.  The identity forces both to be zero,
so both extras survive.  Asking that both be strictly positive is an exact
infeasible linear system.  Notice that the target equations are included;
the circuit is stronger because it already holds before they are used.

This obstruction is minimal in cell count.  The checker computes the exact
chart-character kernel and verifies that none of the `128` individual
residual non-anchor cells is forced to weight zero.  An explicit integral
cocharacter has relative weights `(+1,-1)` on the displayed pair, and its
negative reverses them.  Among all `90` off-diagonal residual cells there
are `22` opposing pairs; the displayed pair is the first canonical one.

## Gauge and permutation scope

The counterguard support has exactly one pure perfect matching in each
colour:

```text
0: 03,12,45,67
1: 06,17,24,35
2: 05,14,26,37.
```

Thus the pure anchors cannot be reselected inside this support.  Site or
colour permutations only relabel the same four-port character circuit.
Diagonal source gauges change coefficients, not aggregate support
characters, and do not remove the obstruction.

What is missing is genuinely non-toric: a source-valid matching exchange,
coefficient cancellation, or non-diagonal colour operation must remove one
member of every opposing carrier pair before `260bb94/9070e22` can apply.

## Logical scope

This refutes the proposed **automatic toric normalization from axis
purification alone**.  It is an exact leading-support/Farkas counterguard,
not an exact one-bad coefficient point: the checker does not assert that the
full source equations admit this 14-cell support.  A theorem using those
equations might still rule out every opposing pair, but that theorem is the
required non-toric carrier-exchange input rather than a consequence of
torus weights.
