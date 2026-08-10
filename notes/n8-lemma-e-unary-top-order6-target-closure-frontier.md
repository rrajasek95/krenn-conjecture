# The order-six target closure is essentially global

## Exact stopping result

The concentrated unary-top identity is certified through off-diagonal order
five, but its deterministic source lift does not give a small
support-restricted route through order six.

Rebuild the exact order-at-most-five elimination while retaining only an
acyclic recipe

\[
  P_j=c_j\left(C_j-\sum_{i<j}a_{ji}P_i\right)           \tag{1}
\]

for each pivot in terms of its literal source column and earlier pivots.
Back-substitution of the pure target uses 6,865 pivots directly.  The
transitive dependency closure of those pivots is

```text
all upstream pivots:             44,638
target closure pivot nodes:      44,203
distinct literal source columns: 44,203
closure fraction:                 99.03%.
```

Thus lazily computing only the particular target tail still requires nearly
the entire upstream graph before it even reaches the 4,917-coordinate
order-six quotient.  The hoped-for small reachable component does not exist
for this deterministic maximal-minor lift.

This is an exact finite-field provenance statement.  It is not an order-six
membership or obstruction result, and it does not say that every possible
rational lift has a 99% closure.

## Capped streaming reconnaissance

One memory-aware modular continuation was run under the explicit 4 GB / 10
minute guard.  It processed recipes topologically, reduced cached tails
lazily, and retained at most 4,917 quotient pivots; it never materialized the
57,558 by 96,922 truncated matrix.

At the last completed checkpoint,

```text
processed provenance events: 50,000 / 88,446
reachable order-six rank:      3,737 / 4,917
resident memory:               below 1 GB.
```

Subsequent reductions densified and no 55,000-event checkpoint completed
before the ten-minute cap.  The process was interrupted.  In particular,
the target order-six tail and its remainder were **not** computed.  The rank
3,737 is only a modular lower bound for this prefix, not the rank of the full
reachable map.

## Structural consequence

The concentrated lane now needs a source-level factorization, symmetry, or
transfer identity at order six; another generic transported sparse solve is
not a bounded next step.  More importantly, even complete concentrated ideal
membership would still not settle the general one-bad packet.  The fixed
spokes choose one ordered hole quadruple.  General endpoint stars require a
polarized sum over holes, and the multipliers in the successive Schur lifts
depend on those hole choices.  No common-denominator/natural source identity
has been proved that permits summing the concentrated lifts while preserving
the full nine response rows.

Therefore the proof-level alternatives are:

1. extract a natural order-six factorization which is equivariant under hole
   relabelling and can be polarized; or
2. prove a separate selection theorem reducing every one-bad packet to one
   concentrated response chart.

Without one of these steps, spending substantially more compute to close the
last two concentrated filtration layers would not close the theorem's sole
general packet.

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_unary_top_order6_target_closure_frontier.py
```

Frozen hashes:

```text
recipe graph:
96428a5a2a800fdefdcd79a6d9f0f37dbd063d137f4b6cb8d240e4e97a469f57

ledger:
b2f2811438615cfa3ddc564625493b225fdd88bf86a895d1054a0e8cbf2c7200
```
