# Nine-block residual 538: max-17 held bridge and four exceptions

Status: **PASS design-only; zero CNF materialization/read and zero solver runs**.

## Exact-17 degree-four lane

The 534 exact-17 degree-four records form exactly 267 two-member literal
guard orbits and 50 exhaustive unlabeled graph classes.  Eighty have no
unresolved eight-block deletion parent.  All record indices, graph members,
and guard members are sealed in the result.

`max17_current_source_held_contract.json` freezes a fresh-source pipeline:
current max-17 base generation, a pinned-nauty exact-17 catalogue, exact
Laurent conflict regeneration over all 11,051 canonical roles, selector
compilation, CaDiCaL decision, and independent DRAT replay.  Historical
dimensions are diagnostics only.  The contract has null max-15/max-16
resource-clear dependencies, no nauty/tool/resource pins, and no clearance;
it therefore refuses every launch.  No graph6, CNF, conflict batch, selector,
or proof was generated or read.

## Four non-degree-four exceptions

Records `1114,1978,2014,2036` all have 16 essential edges, 15 supported
perfect matchings, and degree sequence `(3^4,5^4)`.  They are one unlabeled
graph class and two formal guard orbits.  A larger exact eight-element site
symmetry group preserving the fixed identity matching and active variable
set `{04,35,67}` transports all four full source word systems to record 1114.
The explicit permutations and every matching bijection are replayed, so only
one full algebraic representative remains.

None of the known finite interfaces closes it:

- max-16/max-17 require a degree-four vertex;
- the graph is neither 4-regular nor 5-regular;
- degree-three exact-18/exact-19 theorems have the wrong edge count;
- the maximum-degree-five theorem additionally requires the simultaneous
  balanced all-bridge normal form, which is not established here.

The representative has 16 minimum-load-two triangle/star carriers.  Two
useful maps are

```text
cap01/star3: L(K)=(A04^T K, A04^T K A17),
cap25/star4: transpose-equivalent map with common A35 and identity A27.
```

The first is active on the exact open sublocus
`rank(A04)<3`, no coordinate axis lies in `Col(A04)`, and
`Col(A01)` is not contained in `Col(A04)`; the second has the analogous
`A35` incidence condition.  The cap67/triangle012 guard is explicitly

```text
A37^T + A17 A36^T = 0
A47^T + A17 A46^T = 0
A26 A37^T + A36^T = 0
A26 A47^T + A46^T = 0
A36 A47^T + A37 A46^T = 0.
```

If `A37` or `A47` is invertible, these equations force `A17,A26` invertible
and `A17 A26=I`.  The remaining finite obligation is therefore one
source-transport representative split by the rank/incidence strata of
`A04,A17,A35,A26`, with the full 6,561 X5 amplitudes.  The all-four-invertible
branch makes every minimum-load carrier kernel zero; higher-load carriers and
singular incidence subloci remain open.

Fourteen hostile mutations are rejected.  This package promotes no external
theorem and makes no residual or conjecture closure claim.
