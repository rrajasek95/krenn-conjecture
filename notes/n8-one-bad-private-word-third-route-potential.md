# The first post-second private-word mates strictly increase the label potential

## Result

Take the smallest two-cell second repair from
`n8-one-bad-second-coupled-repair-residual.md`.  Its localized support has
eleven decorated internal cells and two fresh private mixed top words.  For
each word, adjoin each of the fourteen other decorated perfect matchings of
that word.  This gives exactly twenty-eight direct third-route moves.

None closes a private-word cycle.  Every move

* adds two or three cells that were not already supported; and
* creates at least five singleton row-word labels not seen earlier on this
  branch.

The exact censuses are

| support increment | moves |
|---:|---:|
| 2 | 12 |
| 3 | 16 |

and

| new singleton labels | moves |
|---:|---:|
| 5 | 8 |
| 6 | 4 |
| 8 | 2 |
| 10 | 4 |
| 12 | 10 |

Thus the first possible cycle does not occur at the layer immediately above
the direct second repair.

## Finite potential

For a localized branch state, retain

\[
 \mathcal P=(S,L),                                      \tag{1}
\]

where `S` is its decorated-cell support and `L` is the cumulative set of
source-labelled `(row, output word)` singleton labels encountered along the
branch.  Order both entries by inclusion.

A direct mate of a currently private word cannot already be supported, so
`S` strictly increases.  The checker additionally proves, on all twenty-eight
moves here, that the newly created private labels are disjoint from the six
ancestor labels (the original cross label, both first-mate top labels, and
the four singletons present after the second repair).  Hence `L` strictly
increases as well:

\[
                         \mathcal P_{n+1}>\mathcal P_n.  \tag{2}
\]

Both universes are finite: there are only ninety endpoint-coloured physical
cells on six sites and finitely many top/response row-word labels.  Equation
(2) is therefore a genuine finite termination candidate, not a numerical
size heuristic.  What is not yet proved is that label novelty persists at
every later repair layer.  A later transition may revisit a prior label with
a larger support; that first repetition is precisely where a signed
holonomy calculation becomes available.

## Scope

This audit follows only the two fresh singleton words on the smallest
second-route chart.  It does not enumerate arbitrary larger supports or all
simultaneous repairs.  Its exact conclusion is bounded but sharp:

```text
first post-second layer: no label cycle, potential increases on all 28 moves
```

The next useful calculation is not another unconstrained support layer.  It
is to prove label novelty abstractly from alternating-cycle exchange, or to
follow the first route at which a previously seen label returns and compute
the Laurent sign around that cycle.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_private_word_third_route_potential.py
.venv/bin/python -O computations/verify_n8_one_bad_private_word_third_route_potential.py
```

Both modes freeze

```text
33334cdddef689629e5fc4d830c154070937abd2bd2fca0ff8753ee530d4ebbf
```
