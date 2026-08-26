# One-site star CP/slice-space rigidity audit

Status: **terminal provenance countermodel; CP uniqueness cannot select a
matching edge.**

Fix `v` and define, in the tensor space on the other sites,

```text
U_q = span_b { e_b(q) tensor H_(V-{v,q}) },
R_v = direct_sum_(q != v) U_q.
```

The literal star equation is

```text
Phi(A)[a,*] = R_v x_a,
x_a[(q,b)] = A_vq[a,b].                              (1)
```

Moreover `L_v = I_3 tensor R_v`.  Thus injectivity of `L_v` makes the
coordinates `x_a` unique, but it does not imply that the three vectors
`x_0,x_1,x_2` occupy one common neighbor block.  This is a direct-sum
coordinate statement, not a CP-identifiability statement.

## Exact `n=4` GHZ guard

The three perfect matchings of `K4`, one per colour, give exact ternary GHZ.
At every fixed site:

```text
rank R_v = 9,        rank L_v = 27,
dim(U_q intersect P) = (1,1,1),
P = span{e_0^tensor3,e_1^tensor3,e_2^tensor3}.
```

Each pure site slice has rank one across every split
`q | (the other two sites)`, so the rank-three GHZ CP decomposition is fully
in its uniqueness regime.  Nevertheless each edge block has rank one and
the three pure components are routed through three different neighbors.
All six global colour relabellings preserve the identical GHZ output and
realize all six neighbor-routing permutations.  CP uniqueness recovers the
three pure tensors, but their tensor values contain no record of which
matching edge supplied them.

This control still allows an active cap: with `K=I`, every pair has `s=1`
and `kappa=(1,1,1)`; at `n=4` the homogeneous cap-error sum is empty.  Thus
the counterguard rejects only the proposed inference that one edge must
carry all three channels, not clean-cap existence.

## Exact phased `n=6` guard

Under the valid exact specialization `Z[omega] -> F_7`, `omega -> 2`, the
phased non-GHZ source has

```text
rank R_v = 15,       rank L_v = 45,
rank span{Phi(A)[0,*],Phi(A)[1,*],Phi(A)[2,*]} = 3.
```

The script computes every mixed output and every fixed-slice flattening.
Although all three pure coefficients equal one, the site slices contain
mixed words and at least one `q | remaining` flattening has rank greater
than one.  Hence these slices are not the three Segre points of GHZ: the
Kruskal/CP premise fails specifically at the mixed-output rows, as required.

## Consequence

The smallest useful invariant is already the one-neighbor slice profile

```text
dim(U_q intersect P),
rank(Phi(A)[a,*] flattened across q | rest).
```

It distinguishes GHZ slices from the phased control, but its exact GHZ
profile `(1,1,1)` disproves the hoped-for `(3,0,...)` colocation.  Higher
2-, 3-, or 4-site flattenings cannot restore the erased edge label: they are
functions of the same top tensor, and the six source routings have identical
top tensor.  A successful clean-cap argument must therefore use occurrence
provenance or the source coefficient equations, not CP uniqueness.
