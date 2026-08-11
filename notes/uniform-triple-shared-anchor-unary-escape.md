# Unary escape from a triple-shared selected-anchor edge

## Result

Let `e=uv` belong to all three selected pure target matchings.  Fix a
selected colour `a`, and suppose a nonzero cell on `e` has endpoint labels

```text
q_e^{ij} != 0,             (i,j) != (a,a).
```

In the complete output word with colours `i,j` at `u,v` and colour `a` at
every other site, the hafnian expansion partitions literally into

```text
0 = q_e^{ij} C_e^a + R_e,                         (1)
```

where `C_e^a` is the complete pure-`a` two-hole cofactor and `R_e` is the
sum of all matchings avoiding `e`.  This extends the off-diagonal exchange
of `8ef0754` to every non-pure label pair, including a wrong-colour
diagonal `i=j!=a`.

There are two cases over any integral domain after localizing the named
cell.

* If `C_e^a=0`, the pure-`a` target row has avoiding sum one.  Hence it
  reselects a pure-`a` matching avoiding `e`.
* If `C_e^a!=0`, (1) forces `R_e!=0`; otherwise its through term is an
  ordinary localized source unit.  Thus some nonzero mixed matching avoids
  `e`.

Because all three selected anchors contain `e`, their physical union has
no other edge incident to `u` or `v`.  Every matching avoiding `e`
therefore leaves that union at **both** endpoints.  Its endpoint cells have
labels `(i,a)` and `(j,a)`; since `(i,j)!=(a,a)`, at least one is
off-diagonal.  The non-dark branch consequently enters the pinned
off-anchor rank-three/active route, while the dark branch gives the
required pure-anchor reselection directly.

This is a complete-cofactor theorem.  It uses neither a support size nor a
minimal-cardinality hypothesis.

Checker:
`computations/verify_uniform_triple_shared_anchor_unary_escape.py`.

## The first genuine unary debt of the sharp guard

The source-row guard frozen in `1c08419` uses

```text
Q0 = 01 | 23 | 45,
Q1 = 02 | 13 | 45,
Q2 = 03 | 12 | 45.
```

Thus `45` is triple-shared.  The very first omitted genuine unary equation
is the mixed word

```text
000011.
```

Literal expansion of the frozen guard has exactly one nonzero term:

```text
q01_00 q23_00 q45_11 = 1.                         (2)
```

The full common-`q` source requires (2) to vanish.  Any cancellation mate
avoids `45`, so it uses two endpoint pairs outside the selected anchor
union.  Therefore the `1c08419` guard cannot be completed to a genuine
unary source without producing precisely the off-anchor escape that its
restricted companion rows omitted.  This is the load-bearing missing row,
not another tail containing the deficient decorated edge `01`.

## Uniform audits

The checker verifies:

* the exact through/avoiding matching partition at `4,6,8,10` sites;
* against the union of **all** matchings containing `e`, every avoiding
  matching has two off-union endpoint pairs;
* all `24` ternary triples `(a,i,j)` with `(i,j)!=(a,a)`, across every
  six-site avoiding matching (`288` labelled cases);
* the endpoint histogram: `144` cases have one mixed exit and one pure-row
  repair, and `144` have two mixed exits and no direct repair; and
* the unique literal monomial and coefficient in the `000011` debt.

## Sharp remaining boundary

If a pivot edge is shared by only two selected anchors, the third anchor
may provide the sole anchor-contained alternate endpoint routing.  The
same partition still forces that routing, but it need not yet leave the
anchor union.  What remains is the two-decorated-arm/alternating-path
propagation, not the triple-shared-edge guard above.

Run

```text
python3 computations/verify_uniform_triple_shared_anchor_unary_escape.py
python3 -O computations/verify_uniform_triple_shared_anchor_unary_escape.py
python3 -I -S computations/verify_uniform_triple_shared_anchor_unary_escape.py
```

Frozen ledger SHA-256:

```text
de76989a6a35b903eb08cf3357946dff097ca603d96ccdf982e40d0aa681f59e
```
