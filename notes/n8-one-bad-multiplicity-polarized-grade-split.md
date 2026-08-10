# The doubled physical matching does not force a source collision

## Exact verdict

The support-eleven K6 incidence circuit does **not**, from its six polarized
circuit rows alone, force an ordinary parallel-collision or translated-target
unit once endpoint colours and source row words are restored.  The doubled
matching is only doubled after forgetting source provenance.  Its two
occurrences may lie in different decorated characters.

There is an exact minimal six-binomial lift of the canonical circuit into six
distinct mixed top words.  On the union of its 28 decorated cells, every one
of those six complete word fibres contains exactly its prescribed positive
and negative perfect matching and no other matching.  One private cell in
each negative monomial gives the rational coefficient assignment

\[
             M_i^+=1,\qquad M_i^-=-1\qquad(1\leq i\leq6).
\]

Thus all six mixed target rows vanish.  The six decorated exponent-difference
rows have rank six, while their projections to physical K6 edge incidence sum
to zero.  There is no decorated character dependency, odd holonomy, or forced
parallel tail to exploit.

The exact checker is
`computations/verify_n8_one_bad_multiplicity_polarized_grade_split.py`.

## Physical circuit and its polarization

For the canonical representative, using the standard ordering of the fifteen
perfect matchings of K6, the primitive coefficient map is

```text
positive:  2*M0 + M4 + M8 + M10 + M12
negative:    M1 + M2 + M3 + M6 + M11 + M14.
```

After expanding the coefficient two, pair the six positive occurrences with
the six negative occurrences in the displayed order.  The six endpoint-colour
words are

```text
102020   200101   000210   020111   121021   100012.
```

Every word is mixed, so each corresponding GHZ target coefficient is zero.
Decorate both matchings in row `i` by word `i`.  The resulting support has 28
cells.  A literal replay of all fifteen physical perfect matchings proves that
each of these word fibres is exactly the selected binomial.

The two occurrences of

```text
M0 = 01|23|45
```

occur in the first two words and share no decorated cell.  Hence even the
most obvious proposed collision—the repeated physical matching itself—has
split into two independent source characters.

## Why the binomial system is coefficient-feasible

Each negative decorated matching contains a cell unused by the other eleven
matching occurrences.  Set one such cell to `-1` in every negative term and
set all other occupied cells to `1`.  The private cells are distinct, so this
simultaneously evaluates every row to

\[
                         1+(-1)=0.
\]

Equivalently, the six signed decorated exponent rows contain six private
pivots and have full row rank.  This gives a nonzero rational point of the
six-row Laurent system, not merely a support shadow or a finite-field point.

Six is the minimum number of binomial polarization rows: the primitive
physical relation has total positive and negative multiplicity six.  No
minimality is claimed for the 28-cell realization.

## Orbit and sharp-star scope

Site permutations transport the construction through all thirty physical
support-eleven circuits.  The doubled matching is indexed two-to-one by the
fifteen K6 matchings.  Relative to the common unordered datum
`F0={01,24,35}` of either sharp star, the split remains

```text
equal / share one edge / disjoint = 2 / 12 / 16.
```

This transport statement is independent of the order of the response holes.
It proves that no member of the physical orbit can be killed **solely** because
one matching has coefficient two.

## Load-bearing scope guard

This is a full source-provenance packet for the six mixed top rows realizing
the circuit: endpoint order, endpoint colours, complete matching fibres, and
nonzero coefficients are retained.  It is not a solution of every top and
response equation of the one-bad packet and therefore is not a Krenn
counterexample.  The checker expands the other top words on the 28-cell union
and explicitly records surviving mixed rows.  Thus additional source rows do
introduce target debt here, just as in the successor parallel-collision guard.

Indeed, the frozen 28-cell realization has 56 singleton live top fibres and
20 double live fibres; at the displayed rational point, 60 other mixed rows
remain nonzero, starting with word `000010` and coefficient `1`.  Consequently
the remaining theorem cannot be an automatic polarization of the doubled
matching.  It must couple the six grades to these other full-packet
top/response rows, or prove a global target-migration identity.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_multiplicity_polarized_grade_split.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_multiplicity_polarized_grade_split.py
```

Both modes freeze the ledger digest printed by the checker.
