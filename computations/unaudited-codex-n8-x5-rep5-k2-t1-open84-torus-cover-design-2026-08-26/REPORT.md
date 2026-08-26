# Rep5 k2/t1 open84 exact torus-cover design

Status: **exact 16-chart design / zero run / no closure**. This package binds the independently sealed consumed modular timeout: source `fd182135…`, result `eb9ced6f…`, terminal manifest `aa18079a…`, and referee manifest `0cb2ba30…`. The lane stopped fail-closed at its 300-second native wall (300.269 seconds observed, 4,339,458,048-byte peak RSS) and has no mathematical coverage or retry permission.

## Exact reduction

The authoritative Q source `1e2f72c9…` has 84 variables and 6,562 distinct generators. Exact structural parsing of every factored polynomial gives a rank-74 homogeneity constraint matrix and hence a ten-dimensional torus. The saturation equation localizes

`abar * beta * a37_00 * d * b2 * t1 * sat`,

where `d=a37_01-xn1*a37_00` and `b2=a26_20*a37_00+a26_21*a37_01+a26_22*a37_02`. The six characters of `beta, abar, a37_00, t1, sat, d` contain a determinant-one minor. Explicit root-free torus parameters normalize those six units; the saturation equation then forces `b2=1`. Triangular forward/reverse substitutions remove seven variables and the saturation generator, reducing 84/6,562 to 77/6,561.

Four residual torus factors have primitive coordinates `yn1, yn2, t0, t2`. Iterating the exact identity `D(q) union V(q)` and setting `q=1` on the open slice or `q=0` on the closed complement gives 16 exhaustive Q design sources. Every source has 73 variables and 6,561 distinct, syntactically nontrivial generators. All use the original `dp` order and omit any Groebner invocation.

## Scope

This is a reversible localized cover, not a unit-ideal certificate or performance result. It assumes neither transport to rep2 nor transport among rep5 strata. The consumed modular attempt was not reused or relaunched. Any pilot requires an independent design audit, a fresh held runner, and explicit manager clearance.
