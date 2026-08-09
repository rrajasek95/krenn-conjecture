# Exact-ten least-cell cutoff from the mate hypergraph

The chart-26 exact-ten audit is naturally partitioned by the least of the
236 optional endpoint-colour cells.  Most of those blocks can be excluded
before solving any full matching-fibre formula.

The checker reconstructs the eleven singleton mate-requirement families of
the corrected sharp seed.  Their numbers of inclusion-minimal requirements
are

```text
72,72,92,72,92,47,92,72,92,92,92.
```

For a proposed least optional index `i`, every family must have a requirement
using only cells of index at least `i`.  Family 6 gives the sharp elementary
upper cutoff `i <= 142`; this alone excludes all 93 blocks `143..235`.

The checker then uses a small SAT encoding of only these eleven finite
families, together with the already certified 46 size-eight and 1,452
size-nine minimal repairs as upward-closure exclusions.  It does **not**
instantiate the 6,558 mixed fibre equations.  It also forces the proposed
least cell to be essential for one obligation, so irrelevant early cells are
not counted.  The exact possible least-index list is

```text
1,4,5,6,8,10,13,15,16,17,19,24,28,30,31,32,33,34,37,39,41,42,
46,49,50,51,52,54,57,58,61,62,65,68,74,79,84,88,94,97,98,103,
105,107,116,126,128,136,142
```

Thus only **49** least-cell blocks can contain an inclusion-minimal exact-ten
direct repair; the other 187 are structurally empty.  In particular block 7
is empty and block 8 is the next nonempty block after the certified block 6.

This is only a support-shadow cutoff.  Each possible block still requires an
integral signed-HNF or stronger coefficient certificate.

## Reproduction

```sh
uv run python computations/verify_n8_sharp_exact10_least_cell_cutoff.py
uv run python -O computations/verify_n8_sharp_exact10_least_cell_cutoff.py
```
