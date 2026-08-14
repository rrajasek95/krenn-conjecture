# The shortest source route to `Phi_KS,r0` stops at the operation switch

## Verdict

There is no route to `Phi_KS,r0` obtained by composing the currently
implemented response roots/Weyl maps, restriction/reinsertion maps,
occurrence projectors, fixed-window PP/Hasse maps, and cap `r0` maps.
This is an exact reachability statement for those source APIs, not a claim
that an unregistered physical primitive cannot exist.

The literal response word starts at

```text
11110000
```

and the cap `r0` word is

```text
01211222
```

The actual response `D4` cube has 16 vertices and 32 edges.  Generously
closing it under both audited tail roots at sites 2 and 5 and the physical
endpoint swap produces 48 words.  The cap word is absent.  Two immediate
separators are that site 0 remains colour 1 although the cap has colour 0,
and sites 6 and 7 remain binary although the cap has colour 2.

More strongly, grant every possible one-site ternary root on the response
object.  Then the shortest word path has length six:

```text
11110000
01110000
01210000
01211000
01211200
01211220
01211222
```

This deliberately enlarged root graph contains all `3^8=6561` response
words.  It still has no cap-`r0` vertex, because roots preserve the
matching/repeated-edge source grade and the response operation parent.  At
the last displayed word the four remaining mismatched tags are

```text
fine, repeated, operation, window.
```

Thus the shortest path in the graph augmented by one same-word operation
switch has length seven: six roots followed by `Phi_KS,r0`.

Exact checker:
[`verify_h3_phi_ks_r0_word_operation_reachability_no_go.py`](../computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py).

## Why the other implemented maps do not provide the switch

Every inspected constructor remains diagonal in its literal source object:

- At occurrence order three, restriction/reinsertion satisfies
  `sum_e I_e D_e = 2 id`, but the marked restriction still has two lower
  centered cuts and remains in the occurrence/PP object.
- The centered occurrence projector has rank 89.  The selected arrow is not
  in its image; the missing coefficient line is the aggregate
  `sum_i d_i`.
- The normalized covariance bar genuinely gives the word shadow
  `01211222 -> 00000000`, but it acts on the complete response row.  It does
  not select the promoted occurrence or change its operation parent to cap
  `r0`.
- The implemented cap, `K_Eq`, normalizer, Cartan/Weyl, and Macaulay maps are
  cap-internal.  The response roots/Weyl and KS maps are response-internal.

Consequently the operation graph is presently a disjoint union of response
and cap components.  Composition cannot manufacture an off-diagonal matrix
unit from diagonal ones.  In the literal implemented grammar,

```text
Hom^0(response KS, cap r0) = 0.
```

## The first new edge

After the six-root word landing, the missing edge is exactly

\[
 \Phi_{KS,r0}:\quad
 \bigl(01211222,\;\text{root-transported response occurrence}\bigr)
 \longrightarrow
 \bigl(01211222,\;\text{cap }r_0\bigr).                \tag{1}
\]

In the fixed `2345` window, the first local representative can be chosen as

```text
A_[a|b] -> B.
```

The current fixed-window constructor has 100 columns of rank 46 and contains
none of the four operation-profile switches

```text
A_[a|b] -> B       A_[a|b] -> C
A_[b|a] -> B       A_[b|a] -> C.
```

A source-natural version of (1) must supply all four, equivalently the two
face-complete families

```text
(A+B)*H_2345,       A = D*q01, B = p0*s1,
(A+C)*H_2345,       A = D*q01, C = p1*s0.
```

This identifies both the shortest no-go and the minimal positive extension:
the missing object is not another word root or another centered projector,
but the response-to-cap operation arrow itself.  Conditional on adding its
normalized naturality schema and proper faces, the existing comparison
checker gives all eight `kappa_mix` charges equal to zero.

## Reproduction

```bash
python3 computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py --mode all
python3 computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py --mode words
python3 computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py --mode operations
python3 -O computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py --mode all
python3 -I -S computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py --mode all
```

Frozen ledger:

```text
c7f94180bc4c5be5fbf719c5836a115459f52d918a9ff73b88897f5e18325b5b
```
