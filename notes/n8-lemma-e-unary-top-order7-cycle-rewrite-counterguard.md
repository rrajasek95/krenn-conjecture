# Primitive transition cycles do not give a strict global rewrite

## Exact counterguard

The natural attempt to promote the filtered result in
[`n8-lemma-e-unary-top-offdiagonal-filtered-lift.md`](n8-lemma-e-unary-top-offdiagonal-filtered-lift.md)
by orienting every doubled transition and three-colour triangle strictly
downward fails at the top plateau.

Every fine-degree monomial has even global colour counts `(6,4,4)`.  After
deleting its diagonal-colour cells, its transition multigraph on colours
`{0,1,2}` is Eulerian, hence decomposes into doubled edges and
`01-02-12` triangles.  At off-diagonal order seven the transition counts are
forced more sharply to

\[
                 (x_{01},x_{02},x_{12})=(3,3,1).       \tag{1}
\]

Thus every top monomial visibly contains the proposed primitive cycles.
Nevertheless, physical-site incidence prevents their source rows from
orienting the whole plateau.

Project every literal compatible mixed-top/direct-cofactor/cross-cofactor
multiple to its maximal order-seven part.  The exact integer matrix has

```text
rows (order-seven monomials):        3,570
maximal order-seven source columns:  9,164
rank over QQ:                        3,559
cokernel dimension:                     11.
```

The rank statement is exact.  Sparse elimination modulo `1,000,003` gives
rank at least `3,559` over `QQ`.  Back-substitution reconstructs eleven
linearly independent integral left annihilators, all with coefficients
`+1,-1`, having supports

```text
20, 38, 420, 420, 248, 248, 20, 38, 420, 420, 2130.
```

The checker pairs each annihilator with every one of the 9,164 literal
integer columns and obtains zero over `ZZ`.  These covectors give rank at
most `3,559`; together the two certificates prove equality over `QQ`.

## Consequence and scope

Cycle decomposition alone is therefore insufficient for a triangular
all-order lift.  A proof must either show that the particular high-order
tails generated while lifting the target avoid these eleven signed classes,
or introduce a source relation that pairs nontrivially with them.  Blindly
asserting that every high monomial contains a doubled transition or triangle
misses the site-incidence plateau.

This does **not** show that the pure target survives the full ideal.  The
target is at order zero, and its chosen lower-order lift may have a special
top tail orthogonal to all eleven covectors.  Nor does this address multisite
endpoint stars.  It is a sharp negative result only for the proposed strict
primitive-cycle rewrite in the concentrated fine degree.

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_unary_top_order7_cycle_rewrite_counterguard.py
.venv/bin/python -O computations/verify_n8_lemma_e_unary_top_order7_cycle_rewrite_counterguard.py
```

The frozen hashes are

```text
matrix:
bef3875c1056ce960d0347785e2144292e6948b6e1b03530a427fa544ea2dae4

integral cokernel:
c87d6575b7d604cec58a57cbe01397737a7ba07421e289955323f66830f07c5d

ledger:
3f86c920492d6d706722f9b3eb8325e5e90f18a241378e0515a8e6c15d8957d1
```
