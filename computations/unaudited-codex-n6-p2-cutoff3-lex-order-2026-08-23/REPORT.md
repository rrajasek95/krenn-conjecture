# N6 cutoff-three collapse: no simple lexicographic monovariant

Status: **exact bounded audit of the frozen 9,528-pivot DFS certificate.**

## Outcome

The computational collapse height cannot be replaced by any fixed
lexicographic order built from

```text
off-degree, off-cell multiset, diagonal graph code,
```

even after allowing all six priority orders and independently reversing each
feature.  All 48 orders fail on the exact 10,764 dependency edges.  Adding the
source-word profile does not help: it is a property of the pivot column and is
therefore identical for the pivot and every output dependency on an edge.

The best tested rule was

```text
descending off-degree, then ascending diagonal graph code,
then ascending off-cell multiset,
```

and it still reverses 1,305 dependencies.

## Smallest counterwitness

Two degree-zero, profile-`42` dependency edges already defeat the whole tested
family.  Since off-degree and off multiset tie on both, only the last diagonal
graph code distinguishes their endpoints:

```text
pivot #4:  (empty; 43902,43902,48222)
    -> #2: (empty; 43902,43902,43902)       [graph code decreases]

pivot #12: (empty; 43902,48222,48222)
    -> #8:  (empty; 43902,48222,4824604)    [graph code increases]
```

Thus one edge requires the graph-code direction to be ascending and the other
requires it to be descending.  Moving off-degree or off multiset earlier
cannot break either tie; inserting word profile cannot either.  This is the
minimum two-edge **comparison reversal**.  It is deliberately not called a
cycle in the DFS dependency graph, which is acyclic by construction.

The exact source columns are frozen in the result JSON.  Both are literal
profile-`42` columns, so the reversal is coefficient/source-labelled rather
than a projected support artifact.

## What remains positive

The pivot index itself remains a valid well-founded integer statistic: every
dependency has smaller index.  It is a certificate-defined collapse height,
not a closed formula in the obvious row data.  The full sign census is notably
small:

```text
(degree tie, off tie, graph decreases): 1,314
(degree tie, off tie, graph increases): 1,305
(degree/off/graph all increase):        8,145
```

This suggests that any human homotopy needs at least a state-dependent
orientation on the diagonal graph exchange; a fixed lex potential is too
coarse.

## Cutoff-four boundary

No cutoff-four failing target/component artifact was available at freeze time,
so this report makes no extrapolation.  The deterministic winning *approximate*
rule and the exact two-edge reversal are packaged for literal replay on the
first cutoff-four component.  If the component has the same reversal, the lex
route is retired there immediately; otherwise its first new sign pattern is
the precise next datum.

## Replay

```sh
.venv/bin/python computations/unaudited-codex-n6-p2-cutoff3-lex-order-2026-08-23/audit_cutoff3_lex_order.py --check-results
.venv/bin/python -O computations/unaudited-codex-n6-p2-cutoff3-lex-order-2026-08-23/audit_cutoff3_lex_order.py --check-results
.venv/bin/python -I -S computations/unaudited-codex-n6-p2-cutoff3-lex-order-2026-08-23/audit_cutoff3_lex_order.py --check-results
```

The hostile mutation asserts that a lex monovariant exists and must fail.
Logical digest:
`787ba41dfe8b80ccad8d18514591a567e11a0541838c44cac1b2b4af595497c8`.
