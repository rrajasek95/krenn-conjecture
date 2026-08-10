# The doubled carrier exports a four-corner full-row boundary

## Outcome

The surviving support-eleven/multiplicity-two incidence orbit has a finite
source-labelled invariant which is invisible after physical projection.
The two occurrences of its doubled physical matching lie in different
decorated output grades.  Edgewise recombination of those two occurrences
therefore produces a literal Boolean three-cube of eight matching monomials.

In the sharp exact grade-split counterguard from `a260f7a`, the full source
fibres on that cube are

```text
8 cube corners
  = 4 exact cancelling binomial fibres
  + 4 nonzero singleton mixed fibres.
```

The singleton corners are `001,010,101,110` in the three edge-choice bits.
Their coefficient vector at the pinned rational torus point is

\[
                              (1,1,1,1).               \tag{1}
\]

Thus the six polarized circuit equations do not close under the full source
map.  The minimal additional invariant is the four-coordinate full-row debt
(1), not the coefficient two in the physical incidence relation.

The exact checker is
`computations/verify_n8_one_bad_multiplicity_cube_boundary.py`.

## The uniform recombination lemma

Let a physical perfect matching `M` have `h` edges, and let two decorated
occurrences of `M` differ on exactly `k` of those edges.  Their union contains
both decorated cells on each differing edge.  Choosing either cell
independently gives exactly

\[
                               2^k                     \tag{2}
\]

decorated occurrences of the same physical matching.  This is a literal
source-support statement.  It does not use coefficients, a quotient, or a
matching-support search.

For the canonical `h=3` multiplicity circuit the two doubled occurrences are
cell-disjoint, hence `k=3`.  All eight recombination words are distinct and
mixed.  The complete fibre table is

| edge bits | full fibre | value at the exact guard |
|---|---:|---:|
| `000` | 2 terms | 0 |
| `001` | 1 term | 1 |
| `010` | 1 term | 1 |
| `011` | 2 terms | 0 |
| `100` | 2 terms | 0 |
| `101` | 1 term | 1 |
| `110` | 1 term | 1 |
| `111` | 2 terms | 0 |

The original two uses of the doubled matching are corners `000` and `111`.
Two hybrid corners already acquire cancelling mates from the other ten
physical terms of the circuit.  Four do not.

## The exact missing carrier invariant

The physical `K6` incidence quotient forgets the three independent choices
inside (2), so its multiplicity-two relation sees no boundary.  The six
polarized Laurent rows also miss it: their six declared output words are
different from the four singleton cube words.  Since target-word grades are
direct summands of the full coefficient module, combinations of those six
rows cannot erase (1).

Consequently any source-faithful reduction of the multiplicity orbit must do
one of the following:

1. produce a matching mate in each of the four cube-boundary word fibres;
2. identify a full-nine/translated-target identity coupling those four
   grades; or
3. derive a character inconsistency after the four mates are adjoined.

This is smaller and sharper than the 56-singleton histogram of the whole
28-cell guard: the four rows above are forced solely by the doubled carrier
and are already present before any wider debt census.

## Scope

This is a source-labelled theorem and a sharp counterguard to closing the
multiplicity-two orbit by physical incidence or by six independent
binomials.  It does not prove that arbitrary added mates cannot cancel the
four debts, does not construct the required full-nine relation, and is not a
one-bad packet or a Krenn counterexample.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_multiplicity_cube_boundary.py
.venv/bin/python -O computations/verify_n8_one_bad_multiplicity_cube_boundary.py
```
