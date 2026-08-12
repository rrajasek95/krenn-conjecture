# Connected flat C4 bases propagate; source connectivity is the exact gate

## Conditional theorem

Fix one endpoint row and the complete labelled response map

\[
       \mathcal L(z)=(zs_1q^{[h-1]},zs_2q^{[h-1]}).
\]

Expand every occupied complete column into its literal matching-base
evaluation tensors `T_v`.  Form a graph `G` whose vertices are **all** those
bases and whose edges are certified typed C4 exchanges: the two bases have
one physical alternating C4, retain the same decorated complementary tail,
and their E2 minor is an ordinary source-labelled curvature carrier of
`uniform-axis-k3-minor-common-tail-boundary.md`.

Assume `G` is connected and source-exhaustive.  Then exactly one of the
following occurs.

1. Some edge `uv` has a nonzero minor

   \[
        T_u(c)T_v(d)-T_u(d)T_v(c)\ne0.                \tag{1}
   \]

   By the typed-edge hypothesis, (1) is the already proved literal
   common-tail active carrier.
2. Every edge minor vanishes.  Since all base tensors are nonzero, each
   edge has a unique transition scalar

   \[
                         T_v=\lambda_{uv}T_u.          \tag{2}
   \]

   Along a path from one root, (2) makes every base a scalar multiple of the
   root.  Actual tensors force the product around every cycle to be one, so
   there is no extra holonomy hypothesis.  Because the vertex inventory is
   source-exhaustive, summing the bases in each star component makes every
   complete column a multiple of the same tensor.  A zero column is directly
   deletable; two nonzero occupied columns are proportional.

In the latter case the exact finite one-star modification from
`h3-axis-target-coloop-proportional-nu-safe-reduction.md` deletes one
component while preserving all four response tensors and the unary top.
The components share the endpoint coordinate, so neither deleted cell is a
mutual anchor; the move is `nu`-safe.

Thus there is no further coefficient theorem once **connectedness,
typedness, and source exhaustivity** are supplied.  The checker is
`computations/verify_c4_base_exchange_connected_flat_propagation.py`.

## Why the hypotheses do not follow from common q

There is a literal eight-site common-`q` guard.  Its supported perfect
matchings are exactly

```text
A = 01 | 23 | 45 | 67,
B = 01 | 23 | 46 | 57,
K = 01 | 24 | 37 | 56,
L = 01 | 27 | 34 | 56.
```

The induced physical edge support has exactly these four perfect matchings.
The typed C4 graph is

```text
A -- B       K -- L,
```

with no cross-component C4.  Give every supported physical edge a nonzero
rank-one `3 x 3` table.  Use one set of vertex factors on the `A/B` edge
component and an independent set on the `K/L` component; the only shared
physical edge is `01`.  Choose the edge scalars so that

\[
                         T_B=-T_A,\qquad T_L=-T_K.     \tag{3}
\]

Then the literal common hafnian row is

\[
                         q^{[4]}=T_A+T_B+T_K+T_L=0     \tag{4}
\]

coefficientwise on all `3^8` words.  Both C4 components are completely
flat, but `T_A,T_K` are independent.  Hence local Segre gauges do not
propagate to one complete response line.

This is stronger than an abstract graph guard: the checker constructs the
physical edge tables, enumerates all 105 perfect matchings, verifies that
only the four displayed bases are supported, expands all 6,561 word
coefficients, and checks (3)--(4).  It is not a full one-bad packet:
`q^[4]` is zero, not the unary target, and the four response normalizations
are absent.  Those rows are therefore exactly the load-bearing input for a
positive connectivity theorem.

## Sharp source-exhaustivity lemma still needed

The remaining implication is now purely combinatorial/source-labelled:

> In the full unary plus four-response packet, every flat matching-base
> component outside the selected residual C4 is joined to it by a certified
> typed C4 edge, or its first separator is an unequal-tail `C6/C8`, changed
> decorated orientation, off-anchor carrier, or Hall incidence already
> routed elsewhere.

A term which is merely present in the same coefficient row need not be
C4-adjacent; the guard shows why ordinary source exactness does not create
the edge.  Conversely, once the displayed connectivity statement holds,
the conditional theorem proves complete-column dependence with no further
gauge or holonomy work.

This sharpens the word-synchronized chord-or-Hall lemma rather than
replacing it: a chord is precisely what turns an unequal-tail component
into the missing typed C4 edge.

## Scope guards

- A physical C4 edge is not enough unless its decorations make (1) the
  pinned common-tail/target-private carrier.
- Connectedness without source exhaustivity leaves unpaired bases in a
  complete column.
- Source exhaustivity without connectedness permits the guard (3)--(4).
- This theorem does not turn the residual q-edge `K2,2` directly into the
  endpoint-hole Hall `K2,2`; the companion rows must supply that lift.

## Verification

```text
python3 computations/verify_c4_base_exchange_connected_flat_propagation.py
python3 -O computations/verify_c4_base_exchange_connected_flat_propagation.py
python3 -I -S computations/verify_c4_base_exchange_connected_flat_propagation.py
```

Frozen ledger SHA-256:

```text
925fc1258cdde853c23b016f64f4c3c034c395193e0ddb49a4f3e488cc89da15
```
