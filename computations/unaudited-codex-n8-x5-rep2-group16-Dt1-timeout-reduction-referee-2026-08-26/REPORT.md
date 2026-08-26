# Rep2 group16 D(t1) timeout-reduction referee

Verdict: **PASS design-only**, and the next exact cover is one held 61-variable
exact-Q lane.  No Singular process was launched.

The original timed-out `D(t1)` source has 64 variables and 6,569 generators.
Every generator was checked term-by-term to be homogeneous under all six
recorded integer grading directions.  Source generators 6567 and 6568 prove
that `sat`, `t1`, and `it1` are globally invertible; the `it1` and `sat`
character rows have rank two with gcd of maximal minors one.  Hence the torus
normalization `it1=sat=1`, with `t1=1` forced by `t1*it1=1`, is root-free and
global, not merely a generic-open branch.

Independent literal specialization reproduces the sealed slice exactly:
61 variables, 6,568 distinct generators, and 244,567 terms.  The held runtime
source differs only by the strong `slimgb`/`reduce(1,G)` transcript epilogue.
Its acceptance contract requires `GROEBNER_SIZE=1`, `UNIT_REMAINDER=0`, and
`STATUS=UNIT_IDEAL`; it is one fresh 480/510-second, 8-GiB, fail-closed lane.

The global group16 ledger has 57 original charts.  Refining one chart into the
four exact `t` strata gives 60; only the closed `V(t0,t1,t2)` chart and
`V(t1)D(t2)` lane are exact-Q closed.  Therefore 58 charts remain: this held
lane represents the failed `D(t1)` chart, `V(t1,t2)D(t0)` remains unrun, and 56
original charts are untouched.  Even a successful held lane would not close
group16 or rep2.
