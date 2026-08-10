# The second one-bad exchange arrow still has a private top boundary

## Verdict

The direct second cancellation route does not close any of the eight
first-mate charts.  More precisely, take any private mixed top word created
by the first cross-response mate and add any other endpoint-coloured perfect
matching for that same six-site word.  The enlarged source always has a
**new** mixed top word with exactly one matching decomposition.

\[
 \boxed{\text{the first two direct matching-exchange arrows never close.}}
                                                               \tag{1}
\]

This is stronger than finding a leftover response singleton: the obstruction
already remains in the top tensor.  There is therefore no signed-holonomy
cycle at depth two; a third coupled route is required before a Laurent sign
circuit can even arise.

The exact checker is
`computations/verify_n8_one_bad_second_top_mate_exchange.py`.

## Exact finite reduction

The two sharp source-oriented orbits give eight first-mate charts.  Four
charts create two private mixed top words and four create one, hence there
are twelve private words.  A word on six sites has fifteen physical perfect
matchings.  One is the current private route, leaving fourteen direct mates:

```text
12 private top words * 14 alternate matchings = 168 second-route charts.
```

Endpoint order and both endpoint colours of every source cell are retained.
Among the 168 charts:

| sharp orbit | two new cells | three new cells | total |
|---:|---:|---:|---:|
| 0 | 48 | 64 | 112 |
| 1 | 24 | 32 | 56 |
| **total** | **72** | **96** | **168** |

No alternate matching needs only one new coordinate.  Each supplies a
second monomial for the targeted top coefficient, so its product can in
principle be chosen with the opposite sign.  But every chart simultaneously
creates at least one different mixed word whose coefficient is a single
nonzero matching product.  That word is not merely another private word
already present before the second route, and its unique decomposition uses
a newly added cell.

## Exchange interpretation

The first theorem says that the alternating `C4` repair of a private cross
row transgresses to a private top row.  The present theorem says that an
alternate six-site perfect matching for that top row transgresses again to
a new private top row.  Thus the source-labelled exchange graph has no loop
of length two based at the sharp seven-cell boundary.

This is a propagation theorem, not yet a global descending-order theorem.
It does not exclude a simultaneous collection of three or more routes, and
it does not justify an unsigned support search.  The next structural
question is whether repeated top switches strictly lower a normalized
matching potential or eventually form a signed odd-holonomy circuit.  No
third layer is audited here.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_second_top_mate_exchange.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_second_top_mate_exchange.py
```

Both modes freeze the ledger hash printed by the checker.
