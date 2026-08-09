# N=8 D1: full-support residue completion

The maximal 217-cell support in the hard D1 anchor chart is empty for a
structural reason.  This closes the endpoint reached by the support CEGAR;
it does not rely on another cardinality layer.

Write the residue `K4` slice equations as

```text
P_kl = F_kl A + B_k E_l^T + C_l D_k^T,
P_22 = E22,                 P_kl = 0 otherwise.     (1)
```

Every localized entry is nonzero.

## Every edge has rank at most two

For any edge, choose its opposite edge as the scalar block `F` in (1) and
choose a non-pure color slice.  The scalar is nonzero and the other two
terms have rank one, so the chosen edge has rank at most two.

## A rank-one edge is impossible

Suppose `A=a f^T` has rank one.  In each of the eight zero slices, a sum of
two nonzero rank-one matrices is a multiple of `a f^T`.  The elementary
minor identity

```text
minor(u v^T + x y^T) = (u wedge x)(v wedge y)
```

says that either the two left vectors lie on `a` or the two right vectors
lie on `f`.

Let `KB,LC` record the row and column colors producing the left alternative,
and `KD,LE` the right alternative.  Thus the punctured color grid satisfies

```text
[3]^2 - {(2,2)}  subset  (KB*LC) union (KD*LE).      (2)
```

There are 165 covers and exactly 14 inclusion-minimal covers.  Every minimal
cover has one of four terminals at the missing pure slice:

```text
B2,C2 lie on a;             D2,E2 lie on f;
B2,E2 align their term with A;  C2,D2 align their term with A.
```

The first two make the pure result retain the full-support line `a` or `f`,
not the target coordinate line.  In the latter two cases, combine the
aligned term with `F22*A`.  If it cancels, the remaining rank-one term has
full-support factors and is not `E22`; if it does not cancel, the rank-one
sum lemma again forces the wrong left or right line.  Hence no edge has rank
one.

## The rank-two component

All six edges therefore have rank two.  Each zero slice in (1) expresses a
rank-two matrix as two rank-one terms, so their left factors span its column
plane and their right factors span its row plane.  Varying `(k,l)` shows
that the three incident edge planes agree at every residue vertex.  Restrict
to those common two-planes.  Every edge form is invertible, and the
invertible-star theorem in
[`n8-d1-k4-invertible-star-pure-obstruction.md`](n8-d1-k4-invertible-star-pure-obstruction.md)
contradicts purity.

The exact checker
[`verify_n8_d1_residue_full_support_completion.py`](../computations/verify_n8_d1_residue_full_support_completion.py)
audits the full 217-cell support, all 8,100 matching fibres, the universal
minor identity, all 165 covers and 14 minimal covers, and the dependency on
the independently checked invertible-star lemma.  The argument holds over
every field.  Its frozen ledger is
`cf66a233b54535f6e8d812c91e618e4510614645ddd7a664accb1722ea33bca0`.
