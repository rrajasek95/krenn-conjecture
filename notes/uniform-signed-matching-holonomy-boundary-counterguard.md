# Signed matching holonomy starts only after boundary-face completion

## Result

Three normalized constant-colour matching occurrences and one exact
alternating-fibre cancellation do **not** force signed holonomy.  The smallest
counterguard occurs at six sites and is completely rigid at its first step:

* among all `80` edge-disjoint triples of perfect matchings on `K6`, `60`
  have exactly one additional perfect matching in their union and `20` have
  three;
* for a minimum triple, cancelling its unique forced mixed occurrence needs
  at least two new decorated cells;
* a minimum two-cell repair is a single primitive `C4` binomial with no
  exponent circuit, odd or even;
* the repair necessarily exports two nonzero codimension-one mixed fibres.

The last point is uniform in the order.  It is the load-bearing positive
identity from this audit: **a diagonal primitive-`C4` repair forces both of
its boundary faces**.  Consequently the signed matching complex required by
a global proof must be closed under those boundary faces.  Tracking only the
cancelled top fibre loses precisely the rows that can later create odd
holonomy, a singleton unit, or a clean-cap landing.

Exact checker:
[`verify_uniform_signed_matching_holonomy_boundary_counterguard.py`](../computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py).

## The uniform boundary identity

Let two perfect matchings agree on a nonzero matching tail `t` and differ on
one alternating `C4`.  Write the two cells of the normalized horizontal
matching as `x0,y0`, the two recoloured repair cells on the same physical
edges as `x,y`, and the two cells of the forced opposite matching as `u,v`.
The five occurrence weights are

\[
 B=t x_0y_0,\quad D=txy,\quad F=tuv,\quad
 L=txy_0,\quad R=tx_0y.                              \tag{1}
\]

Here `B` is the normalized anchor, `D` the diagonal repair, `F` the forced
mixed occurrence, and `L,R` the two words obtained by recolouring only one
of the horizontal edges.  In the free commutative exponent monoid,

\[
                         LR=BD.                       \tag{2}
\]

If the top mixed coefficient is the binomial `D+F=0`, then

\[
                         LR=-BF.                      \tag{3}
\]

Thus `B,F != 0` implies `L,R != 0`.  This uses no positivity, genericity, or
division beyond localization at the five displayed live occurrences.  The
tail may be a perfect matching on any even number of additional sites, so
(2)--(3) hold at every even order.

Equation (3) gives a useful restricted propagation theorem:

> **Primitive-boundary theorem.**  A normalized anchor-union occurrence
> cancelled by a same-skeleton diagonal `C4` repair either has a cancellation
> mate on each of its two boundary words, or a boundary word is a singleton
> unit.  The top binomial alone has no holonomy circuit.  Any subsequent odd
> holonomy must use at least one of the two forced boundary fibres.

This is weaker than the desired global propagation theorem, but it is a
genuine uniform source identity rather than a reformulation of the
conjecture.

## Smallest exact counterguard

Take the three colour matchings

```text
M0 = 01|23|45,
M1 = 02|14|35,
M2 = 03|15|24,
```

and give their nine constant-colour cells weight `1`.  Their union has one
extra perfect matching

```text
F = 01|24|35,       word 002121,       weight 1.
```

Add only

```text
a23(2,1) = i,       a45(2,1) = i.
```

The same physical matching `M0` now has weight `i^2=-1` on `002121`, so the
forced fibre cancels exactly.  Exhausting all `3^6` words and all `15`
perfect matchings gives the complete nonzero ledger

```text
000000 :  1
111111 :  1
222222 :  1
002121 : -1 + 1 = 0
002100 :  i
000021 :  i
```

There is one nonzero exponent-difference row and hence no nonzero integral
dependency.  The signed partial character is flat.  The two boundary rows
are literal singleton debts, and their product is the instance

\[
                         i\,i=-1=-1\cdot1             \tag{4}
\]

of (3).

The repair is minimal.  A distinct perfect matching on six sites shares at
most one edge with `F`; exhaustive compatibility with the nine anchor cells
gives

```text
6 candidate mates need 2 new decorated cells,
8 candidate mates need 3 new decorated cells.
```

At four sites the three perfect matchings themselves realize exact ternary
GHZ and force no mixed matching, so six is the first order at which this
anchor-union holonomy question exists.

## Missing hypothesis and next attack

The counterguard is not a Krenn counterexample: the two displayed singleton
coefficients violate the full source equations.  Its point is sharper.  A
proof may not quotient away the boundary words after repairing the top
fibre.  The needed hypothesis is:

> **Boundary-face completeness.**  Whenever a live primitive alternating
> fibre is put into the signed exponent complex, include every nonzero
> one-edge recolouring face exported by (2), together with its cancellation
> mates and their labelled physical pair data.

With this completion, every primitive diagonal repair has two outgoing
faces.  The viable global iteration is therefore on the complete boundary
ledger, not on one fibre.  Its possible terminals are concrete:

1. an unmatched face is a singleton Laurent unit;
2. an odd exponent dependency is signed holonomy;
3. a normalized anchor-to-anchor path of incompatible parity is an ordinary
   unit;
4. a four-port boundary shore supported at one residual site per endpoint
   row enters the already proved square-zero one-bad active-cap lemma.

The unresolved step is to prove that repeated boundary completion cannot
remain forever in a flat even component without reaching item 4.  The
smallest guard shows exactly why an argument based only on the first
cancelled fibre or a local cycle parity cannot prove that statement.

## Relation to the global paired-Weyl telescope

There is a complementary uniform construction which should be retained.
Pair all `N` sites as `P_1,...,P_(N/2)`.  On a selected colour plane let the
one-site signed Weyl action be

```text
e_c -> -e_i,       e_i -> e_c,
```

and let `W_j` act at the two sites of `P_j`.  For physical Cartan homotopies
`h_j` with boundary `W_j-1`, set

\[
 P_0=1,\qquad P_j=W_1\cdots W_j,\qquad
 H_W=\sum_j P_{j-1}h_j.                              \tag{5}
\]

Then (5) telescopes to

\[
                       dH_W+H_Wd=P_{N/2}-1.           \tag{6}
\]

The final Weyl product exchanges the two selected monochromatic tensors:
on the `c` word its sign is `(-1)^N=1`, while on the `i` word its sign is
positive.  It fixes the third word.  Therefore (6) is target-safe for every
even `N`.

This does not contradict the boundary counterguard.  Each `h_j` is formed
from a complete response row, and local colour actions preserve the
underlying matching and repeated-edge labels.  Hence `H_W` is constant in
the matching-occurrence factor.  It supplies the **pure-Weyl marginal** left
open by the known uniform physical bar calculation, but it does not by
itself split a selected matching occurrence or produce the pointed
Gate-II direction `2A-B-C`.  That still requires a matching-centred
projector or a source-valid component splitter.  Equivalently, the paired
telescope solves the colour-holonomy factor, while boundary-face completion
controls the matching-holonomy factor.

## Reproduction

```sh
python3 computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py
python3 -O computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py
python3 -I -S computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py
```

Frozen ledger SHA-256:

```text
6e34e6ef4852fdfba8253bbd4fd7f0e6dafe62780e8d1a19a47329107ce83ee8
```
