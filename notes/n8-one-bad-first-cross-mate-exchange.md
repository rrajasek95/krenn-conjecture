# The first private-cross mate transgresses to the top row

## Statement

Start with any of the `1,440` sharp seven-cell one-bad packets classified in
`n8-one-bad-binary-projection-minimal-counterguards.md`.  It has one
all-`a` perfect matching, one `b` near-perfect matching, one `c`
near-perfect matching, and a private unit monomial in each ordered cross
response.

Fix either private cross monomial.  Its two star holes leave four residual
sites.  The private route is one perfect matching of those four sites.  A
direct cancellation mate must use one of the other two perfect matchings,
with endpoint colours fixed by the same output word.  Then:

\[
 \boxed{\text{each direct first mate creates a private nonzero mixed
 top coefficient.}}                                      \tag{1}
\]

Consequently a single alternate matching cannot repair a sharp packet.
Any larger completion must add another, coupled route cancelling the new
top coefficient (or move to a different leading/anchor chart).

The exact checker is
`computations/verify_n8_one_bad_first_cross_mate_exchange.py`.

## Why the mate list is finite

Two distinct perfect matchings on four vertices are edge-disjoint and their
union is an alternating `C4`.  Hence every private response route has
exactly two direct mate matchings.  The prior exact census has two
source-oriented orbits and two ordered cross rows per packet, so only

```text
2 sharp orbits * 2 cross rows * 2 C4 mates = 8 charts
```

need inspection.  These charts represent
`1,440*2*2=5,760` labelled first-mate choices.

The checker retains physical pairs, endpoint colours, the full six-site
output word, and the actual three-edge source decomposition.  It does not
use an unsigned support shadow.

## The two exchange signatures

The eight charts split evenly:

| representative charts | mixed top words created | extra pure-`a` route |
|---:|---:|---:|
| 4 | 2 | 0 |
| 4 | 1 | 1 |

In the second sharp orbit the cross output happens to decorate both mate
edges by `a`.  The mate therefore supplies an alternate all-`a` perfect
matching as well as a private mixed top word.  In the first orbit it creates
two private mixed top words.  In both cases at least one mixed coefficient
has exactly one matching decomposition and contains a new mate cell.  On
the nonzero-weight torus its coefficient cannot vanish.

This is the promised matching-exchange statement: cancelling a private
cross boundary transgresses, through an alternating `C4`, to a private top
boundary.  There is no source switch that repairs the cross row while
leaving the top row unchanged at this first step.

## Exact scope and next residual

Equation (1) is not an exclusion of arbitrary support above seven cells.
Several new cells introduced simultaneously could cancel both the private
cross monomial and the induced top monomial.  The theorem identifies the
smallest genuine coupled residual packet:

1. an old private cross route;
2. an alternate `C4` mate with opposite product coefficient; and
3. a second route for the mate-induced private top word.

Thus a support-level eighth-cell search is not the right next move: one
should classify the alternating path/cycle carrying item 3 and ask whether
its switch returns to a previous row with odd holonomy, lowers the leading
matching, or creates another private boundary.  The present theorem is the
well-founded first arrow of that source-labelled exchange complex.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_first_cross_mate_exchange.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_first_cross_mate_exchange.py
```

Both modes freeze the ledger hash printed by the checker.
