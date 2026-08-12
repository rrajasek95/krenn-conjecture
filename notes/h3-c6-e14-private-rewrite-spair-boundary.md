# H3 C6 E14 private rewrite / S-pair boundary

## Exact rewrite theorem

Across the nine universal minimal E14 charts, `G11[111111]` has 228
endpoint-labelled target-private monomials (24 or 26 per chart).  The complete
literal divisibility inventory contains 1,108 possible `G11` pivots on these
terms.  Every one has another private target monomial in its multiplied tail.
Consequently there is no `G11` leading-term matching whose private part is
triangular: every finite elimination order contains a directed cycle.

The smallest obstruction is already a two-cycle.  In chart `(1,1)`, for
example, the two private terms

```
(p1_0_1 s1_1_1) u35_11 v24_11,
(p1_1_1 s1_0_1) u35_11 v24_11
```

occur as the two endpoint orientations of the same bright tail.  The complete
zero row `G11[110011]`, multiplied by `u35_11 v24_11`, contains both with the
same nonzero coefficient, and therefore rewrites either one through the
other.  All nine charts contain an endpoint-orientation cycle of this type.
This is the invariant behind the failure of a response-only term order: the
q-tail is unchanged while the signless endpoint bracket is exchanged.

## What breaks the cycles

Unary rows do supply a private-terminal divisibility pivot for every one of
the 228 endpoint-private occurrences.  They do not make the preceding triple
census automatically global.  Multiplying the unary pivot by the missing
q-factor produces a genuine Buchberger S-pair:

- 204 private terms have least possible maximum tail degree four;
- 24 have least possible maximum tail degree three.

For the first displayed private term, `U[000101]` has pivot `-u35_11`.
Multiplication by `v24_11` cancels the private term but produces thirteen
nonprivate tails such as

```
u05_01 v13_01 v24_11,
u35_11 v04_00 v24_11,
v04_00 v13_01 v25_01 v24_11.
```

Thus the cycle is genuinely broken, but only in the next source-resolution
layer.  This does not contradict the `h=3` degree bound: the complete unary
row is cubic, while its Buchberger multiplier produces a quartic source
combination.  `G22` closes 959 specialized triples but is endpoint-colour-2
graded, so it is not the direct attachment for these endpoint-colour-1
private cycles.

## Proof frontier

The precise next lemma is now small and source-labelled: adjoin the complete
unary-times-`q` S-pairs and prove that all of their nonprivate degree-three
and degree-four tails reduce by the already available complete rows, with a
common terminating order.  A successful reduction gives the desired
triangular/Rees promotion; a surviving tail is the first new attaching
obstruction.  No larger support census is indicated.

This result is an exact rewrite theorem on the nine universal minimal E14
charts.  It does not yet assert reduction of the S-pair tails, arbitrary
simultaneous-cell emptiness, or a full-source counterexample.

Verified by
`computations/verify_h3_c6_e14_private_rewrite_spair_boundary.py`.
