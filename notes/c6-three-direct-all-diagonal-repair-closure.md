# Every diagonal repair of the three-direct `C6` escape ends in a source unit

## Result

The support-minimum conclusion of `3d78125` extends to every simultaneous
diagonal mate/escape repair.  Let a diagonal six-site support contain the
seven labelled cells

```text
cap 34:       34;0, 34;1, 34;2
core fine:    05;1, 12;1
mate fine:    01;1, 25;1
window/tail:  0125 / T,                                   (1)
```

and suppose it contains the cap-avoiding colour-one escape forced by the
three-direct identity.  If the three pure rows are present, choose one pure
perfect-matching witness in each colour.  There are

```text
colour 0: 15,   colour 1 avoiding 34: 12,   colour 2: 15,
```

hence 2,700 labelled initial witness unions.  Every one already has a
literal mixed singleton.  More importantly, recursively adjoining every
possible diagonal cancellation mate never reaches a singleton-free support.
The exact finite repair DAG contains 120,817 supports and has 46,702
terminal vertices, all carrying an unrepairable `2+2+2` singleton.

Consequently no diagonal exact source—support-minimal or otherwise—can
contain (1) together with its forced colour-one escape.  There is no larger
simultaneous diagonal guard to freeze.

The checker is
`computations/verify_c6_three_direct_all_diagonal_repair_closure.py`.

## 1. Literal source rows

A diagonal decorated cell is written `uv;c`; it can occur in an output word
only when both endpoints `u,v` have colour `c`.  For a fixed word, compatible
perfect matchings have the following forms.

* A pure word has all 15 matchings available.
* A `4+2` word has its minority edge fixed and has exactly three pairings on
  the four majority sites.
* A `2+2+2` word has exactly one compatible matching: the three prescribed
  same-colour pairs.

Every occupied cell has nonzero coefficient.  A supported mixed word with
one compatible matching therefore has a nonzero monomial coefficient, while
the GHZ target coefficient is zero.  This is a physical source unit, not an
occurrence-module projection.

All records retain

```text
output word, fine matching, literal coefficient operation,
cap 34, window 0125, tail T, and every decorated cell.       (2)
```

## 2. Initial pure-witness census

Pure normalization supplies some matching in colours zero and two.  The
already-forced escape supplies a matching in colour one avoiding cap `34`.
Taking their union with (1) produces 2,700 distinct labelled supports, with
cell-count distribution

```text
13:72,  14:612,  15:1440,  16:576.                         (3)
```

The 1,152 fifteen-cell packets of `3d78125` occur exactly as the subcensus in
which the colour-one escape shares one old residual edge and both other pure
witnesses avoid the cap.

Among all 2,700 unions, the number of immediate `2+2+2` singleton rows has
distribution

```text
0:16, 1:144, 2:716, 3:864, 4:572, 5:304, 6:76, 8:8.       (4)
```

The sixteen exceptions in the zero bin do not evade the source equations.
They all have fifteen cells and have `4+2` singleton rows instead.  Under
the order-eight stabilizer retaining the cap, core fine, and mate fine, they
form two orbits of size eight.  Canonical supports are

```text
01;1 02;0 02;2 03;1 05;1 12;1 13;0 13;2
14;1 25;1 34;0 34;1 34;2 45;0 45;2,                       (5)

01;1 02;0 02;2 03;1 05;1 12;1 14;0 14;2
25;1 34;0 34;1 34;2 35;0 35;2 45;1.                       (6)
```

Thus every first pure-witness realization, including every nonminimum one,
has an exact mixed-row consequence before any coefficient solving.

## 3. Exhaustive simultaneous-repair closure

An initial singleton does not by itself exclude a larger source: a full
support could add cancellation mates.  The closure therefore repeats the
following physical rule.

For the first current mixed singleton:

1. if its word is `4+2`, keep its minority edge and adjoin each of the other
   two majority-site pairings in turn;
2. each mate needs one or two missing decorated cells;
3. recompute every one of the 729 coefficient rows; and
4. stop if the first singleton is `2+2+2`, because its word has no second
   compatible diagonal matching.

Memoizing literal supports gives

```text
states visited                         120817
distinct generated children           118117
one-cell repair faces                  105162
two-cell repair faces                   43068
terminal 2+2+2 states                   46702
singleton-free states                       0
largest visited support                    31 cells.       (7)
```

A terminal example retains (2) with

```text
word       010212
fine       02|14|35
cells      02;0, 14;1, 35;2
operation  coefficient:010212.                              (8)
```

Because the three colour pairs in (8) are prescribed by the word, no
additional diagonal cell can produce another occurrence of that word.

## 4. Why the search is an exhaustive theorem

Suppose, for contradiction, that `T` is a singleton-free diagonal support
containing (1), a cap-avoiding colour-one escape, and all three pure rows.
Choose one supported pure witness in each colour and let `S` be their union
with (1).  Then `S` is one of the 2,700 initial vertices and `S subset T`.

If the current `S` has a `4+2` singleton, singleton-freeness of `T` forces at
least one of its two alternative pairings to be supported in `T`.  Follow
the corresponding repair edge.  The new partial support remains a subset of
`T`.  The relative potential

\[
                         \rho_T(S)=|T\setminus S|           \tag{9}
\]

strictly decreases by one or two.  Hence the process must terminate.  The
exhaustive closure has no singleton-free terminal vertex; every terminal is
a `2+2+2` unit, which remains a singleton in every diagonal superset.  This
contradicts the assumed exact source.

Equation (9) is the requested well-founded repair potential.  It also shows
why adding several mates simultaneously is covered: at each stage one of
the mates already contained in `T` can be followed, regardless of what
other cells were added at the same time.

## 5. Relation to physical derivative minimality

The theorem of `c8bc02f` remains the correct support-minimality interface.
On a tight cut, a relation among the complete physical derivative tensors
allows an affine coefficient move that deletes a live cell while preserving
the full source tensor.  Therefore a support-minimal source must have
independent live cut derivatives.

No derivative assumption is needed here.  In the diagonal repair universe,
even the independent alternative is eliminated by the monotone closure:
every possible mate chain reaches a physical mixed monomial.  Thus the local
dichotomy is sharper than requested:

```text
physical derivative dependence  -> smaller exact support (c8bc02f),
diagonal mate/escape completion  -> literal 2+2+2 source unit.             (10)
```

There is no recurrent diagonal guard in the second branch.

## Scope

The theorem covers every diagonal-cell superset of the labelled seven-cell
guard after the cap-avoiding colour-one escape has been forced.  Colours
zero and two may use cap-containing or cap-avoiding pure witnesses; no
minimum-completion assumption is made.

Arbitrary endpoint-offdiagonal repair cells are not enumerated.  Such a cell
can change the compatible-matching fibre of a `2+2+2` word, so the uniqueness
argument in (8) is no longer valid.  Promoting (10) to the full bicoloured
source therefore needs either a full endpoint-coloured repair census or a
physical derivative relation that deletes the offdiagonal repair.

## Reproduction

```text
python3 computations/verify_c6_three_direct_all_diagonal_repair_closure.py --mode structural
python3 -O computations/verify_c6_three_direct_all_diagonal_repair_closure.py --mode full
python3 -I -S computations/verify_c6_three_direct_all_diagonal_repair_closure.py --mode exhaustive
```

All modes return the same frozen ledger digest.
