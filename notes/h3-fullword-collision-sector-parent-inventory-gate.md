# The full physical word inventory misses the collision splitter

## Verdict

Fix the `E01` collision sector in response word `11:110000`: augmented
vertex `0` is missing and `S` is doubled.  Exhausting every coefficient
monomial in all `3^8=6561` physical output rows gives an exact negative
answer:

> The same word/fine/repeated-grade span does **not** contain the signed
> 24-term residual.

This is already forced by operation degree.  Every physical coefficient
monomial is a perfect matching, hence has squarefree degree

\[
                         (1,1,1,1,1,1,1,1),
\]

whereas every term of this collision sector has degree

\[
                         (1,2,0,1,1,1,1,1)
\]

in the order `(P,S,0,1,2,3,4,5)`.  The checker nevertheless materializes
all `688,905=6561*105` decorated terms in the complete `K8` inventory and
counts the `590,490=6561*90` terms in the direct-free inventory.  Their
projection to the sector is identically zero.  Thus neither the other
mixed output equations nor pure-target normalization hides an additional
collision row.

Exact checker:
[`verify_h3_fullword_collision_sector_parent_inventory_gate.py`](../computations/verify_h3_fullword_collision_sector_parent_inventory_gate.py).

## The parent-labelled calculation

The 45 collision skeletons each have two repairs: either of the two edges
incident with doubled `S` can be relabelled back to the missing `0`.
Retaining the repaired edge and physical parent matching therefore gives
90 operation-parent occurrences.

At the repeated word `11:110000`, both repairs collect to the same decorated
collision monomial because the `0` and `S` colours are both `1`.  The
parent-even collision vector is one on all 90 occurrences; collection is
the familiar symmetric vector with coefficient two on all 45 monomials.

The incomplete operation root is

\[
 \Xi_{01}
 =a_{PS}^{w_Pw_0}{\partial\over\partial a_{P0}^{w_Pw_0}}
  -a_{S1}^{w_0w_1}{\partial\over\partial a_{01}^{w_0w_1}}.       \tag{1}
\]

On the parent-labelled sector, `Xi_01(H_w)` has 15 occurrences of
coefficient `+1`, 15 of coefficient `-1`, and 60 zeros.  Three collected
monomials have both parents with opposite signs.  Collection cancels those
six occurrences and leaves exactly

```text
12 coefficients +1,  12 coefficients -1,  21 zeros,
```

the independently certified 24-term residual `R_01`.

This also answers the provenance question cleanly.  The residual is not a
pure-Weyl/Cartan marginal, nor a linear combination made visible by
forgetting output words.  It is an operation-parent-odd class.  Collection
forgets precisely the parent information responsible for the three local
cancellations, but it does not turn the remaining 24 terms into a physical
output equation.

## Exact ranks and duals

All 6561 projected physical columns are zero.  Adjoining the existing
parent-even collision column gives rank one.  The root packet raises the
rank to two.  Before collection the normalized dual is

\[
                         \widetilde\lambda={\Xi_{01}\over30};     \tag{2}
\]

it kills every physical row and the 90-occurrence parent-even vector, and
reads one on `Xi_01(H_w)`.  After collection the normalized dual is

\[
                              \lambda={R_{01}\over24};             \tag{3}
\]

it kills every physical row and the symmetric 45-term vector, and reads one
on `R_01`.  Thus the ranks are exactly

```text
parent-labelled: physical + even collision       rank 1
                 plus Xi_01(H_w)                  rank 2

collected:       physical + symmetric collision  rank 1
                 plus R_01                       rank 2.
```

The fixed response word is mixed, so its GHZ target coefficient is zero.
The three pure target rows lie in different word blocks, and their constant
normalizations lie in unit degree rather than collision degree.  All 6558
mixed zero-target equations and all three pure equations are therefore
annihilated by (2)--(3).

## First extra row family

The first possible rank-raising family is now forced: an
**occurrence-labelled first Spencer/root family** realizing (1) on every
physical word.  At `11:110000` its top must have the 30 signed parent
occurrences above and collected boundary `R_01`.  This is new chain data;
differentiating a polynomial output equation by (1) does not by itself make
the derivative a boundary in the fixed physical fibre.

Its augmentation cannot be top-only.  The 30 parent occurrences have four
first principal-parts flags each:

```text
120 parent-labelled flags total
 60 of topology 3K2
 60 of topology P3+K2.
```

After collection and the three double-parent cancellations, the nonzero
residual has 96 flags, 48 of each topology.  A source-valid family must keep
the response word, operation parent, root trigger, removed edge, fine
degree, and reinsertion edge on all 120 flags.  It must then extend through
the existing target, ordinary-residue, anchor, `q`, `W`, word-changing and
shifted-ridge augmentations.  This is exactly the occurrence-natural
Spencer/root landing missing from the present proof; no further scan of
ordinary output words can supply it.

## Scope

This is an exact finite `h=3` support and rational-rank theorem for one
45-term collision sector.  It is exhaustive over the full ternary output
inventory and checks both complete-105 and direct-free-90 presentations.
It proves the terminal alternative for the existing coefficient rows; it
does not construct the missing Spencer/root cell or certify its augmented
physical descent.

## Verification

Run

```text
python3 computations/verify_h3_fullword_collision_sector_parent_inventory_gate.py
python3 -O computations/verify_h3_fullword_collision_sector_parent_inventory_gate.py
python3 -I -S computations/verify_h3_fullword_collision_sector_parent_inventory_gate.py
```

Frozen ledger SHA-256:

```text
bfafda8698a3e58346212a8287729574ddaccdd9ce668d299479c28ba2f6b385
```
