# Equal-partition zero holonomy has one diagonal `C4` geometry

## Outcome

The first even-interference branch is substantially smaller than the raw
four/six/eight-site alternating-core census suggests.  Take a literal
zero-Fitting two-row block and apply the proved spectator factorization

\[
 A=GU,\qquad B=GV,\qquad C=HU,\qquad D=HV.              \tag{1}
\]

The two source words agree on the alternating core supporting `U,V`; they
can differ only on the spectator sites supporting `G,H`.  If their global
colour multiplicity partitions differ, the existing colour-partition order
orients the transport.  If the partitions are equal and the rows are
distinct, the complete `N=8` classification is:

1. a six-site core has two spectator sites, and their colours are
   transposed.  The unique spectator edge is off-diagonal;
2. an eight-site core has no spectator sites, so there are no two distinct
   literal source rows; and
3. a four-site core either contains an off-diagonal spectator cell, or the
   two spectator words both have type `2+2`.  In the latter branch `G,H`
   are diagonal and either form one physical `C4`, or have the same skeleton
   with the two diagonal colours exchanged between its edges.  Every unused
   `K4` matching is off-diagonal in both words.

Thus every equal-partition zero two-cycle enters the already isolated
bidirectional off-diagonal fan/endpoint-holonomy interface except for one
geometry: a diagonal `2+2` spectator switch whose unused pairings are the
conjugate off-diagonal routes.

Checker:
[`verify_oo_zero_holonomy_equal_partition_reduction.py`](../computations/verify_oo_zero_holonomy_equal_partition_reduction.py).

## Why the word difference lives on the spectators

In the free cell monoid, `AD=BC` makes the signed exponent differences
`A-B` and `C-D` equal.  Removing their positive and negative parts gives
(1).  The decorated core monomials `U,V` are literally the same in both
rows.  Hence every core-site endpoint colour is the same in the two output
words.  Only the complement matching can change the word.

At `N=8` the complement has respectively four, two, or zero sites when the
alternating core has four, six, or eight sites.  This makes the
equal-partition classification elementary but load-bearing: it is a
statement about source words and decorated cells, not merely about the
uncoloured symmetric difference of two matchings.

## The exact finite split

For two spectator sites there are six ordered distinct words with the same
colour multiset:

```text
(a,b) -> (b,a),  a != b.
```

All six use the unique physical edge with an off-diagonal cell.

For four spectator sites, enumerate the three physical perfect matchings
and every ordered pair of distinct ternary words with the same colour
multiset.  The `5,022` decorated pairs split as

```text
4,932  at least one of G,H contains an off-diagonal cell,
   90  both G and H are diagonal:
       72 physical C4 switches,
       18 same-skeleton colour swaps.
```

In all ninety diagonal cases the word type is exactly `2+2`.  For a fixed
word its diagonal perfect matching is unique: it pairs the two sites of one
colour and the two sites of the other.  In 72 cases the two word partitions
give different physical matchings; they form one alternating `C4`, and the
third matching pairs unlike colours in both words.  In the remaining 18
cases the site partition is unchanged but the names of its two colours are
exchanged.  Then `G,H` have the same physical skeleton with different
diagonal cells, and both other physical K4 matchings pair unlike colours in
both words.

The same-skeleton branch is not a physical matching flip, so it must not be
silently merged with the 72 `C4` cases.  It is a two-edge colour-holonomy
switch.  Both subtypes nevertheless ask for the same source input: an
off-diagonal companion route through the four spectator sites.

There is no zero-spectator case because then the two words are identical.
A reduced module may contain repeated or derived copies of one literal row,
but that is not a new two-row source occurrence and is outside this theorem.

## Interaction with the active curved-overlap proof

Any off-diagonal spectator factor in (1) is a nonzero physical cell
`A_vu^(ba)`, `a != b`.  The two target-augmented private-site identities
already force transposed active fans at `v` and `u`.

* If either fan leaves the selected anchor union, the pinned uniform theorem
  gives a distinct-head active four-good overlap.
* If both are trapped in the anchor web, their marked component is exactly
  the bidirectional five-lock endpoint-holonomy interface.  Equal literal
  tails give the alternating endpoint boundary; unequal tails are the
  residual source-typed Kodaira--Spencer comparison already isolated on the
  rootless side.

So an arbitrary six-site even core is not a separate global holonomy
problem at the literal two-cycle level.  It feeds the common endpoint-word
change theorem.  The genuinely new even geometry is the diagonal `2+2`
four-site switch, including the same-skeleton colour-swap subtype.  Its
unused matchings are already the desired conjugate off-diagonal routes; the
next proof step is to show that the complete crossed
rows either activate that route, give an odd three-pair unit, or produce a
support-reducing complete-column dependence.

## Scope

This is a classification and reduction theorem, not closure of curved OO.
It assumes a literal zero-Fitting **two-row** block after the established
spectator factorization.  A general critical SCC may have more rows, and
row reduction may create derived copies not corresponding to distinct
physical coefficients.  The diagonal `2+2` switch and the common
endpoint-holonomy comparison remain open.  No claim of an active clean cap
or of Krenn's conjecture is made here.

Reproduce with

```text
python3 computations/verify_oo_zero_holonomy_equal_partition_reduction.py
python3 -O computations/verify_oo_zero_holonomy_equal_partition_reduction.py
python3 -I -S computations/verify_oo_zero_holonomy_equal_partition_reduction.py
```

Frozen ledger SHA-256:

```text
21c0911170844030c7585dae964e5a5456685a87b65911b5e0ed54f508293d62
```
