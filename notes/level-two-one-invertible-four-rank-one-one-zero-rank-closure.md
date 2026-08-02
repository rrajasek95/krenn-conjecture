# One-invertible, four-rank-one, one-zero rank closure

This note closes the `1I+4R+1Z` endpoint stratum on the rank-55
generic-kernel/R2 branch before any `L0`, `L1`, or `R2` condition is used.
The companion checker is
[`verify_level_two_one_invertible_four_rank_one_one_zero_rank_closure.py`](../computations/verify_level_two_one_invertible_four_rank_one_one_zero_rank_closure.py).
This is research evidence, not a proof of Krenn's conjecture.

Let site 0 be invertible, let

\[
X_i=h_i b_i^T\ne0\qquad(1\le i\le4),
\]

and let `X_5=0`.  On sites `1,...,5`, put an edge `ij` in `E` when
`nu_i+nu_j=0`.  The generic-kernel equations say:

* `M_0i` is a fixed nonzero rank-one spoke for `1<=i<=4`, since
  `nu_0+nu_i` cannot vanish at an invertible root;
* a rank-one/rank-one edge in `E` is arbitrary and satisfies
  `b_i^T J b_j=0`; off `E` it is a fixed scalar multiple of
  `h_i h_j^T`;
* `M_i5` is arbitrary exactly on an edge `i5`, and is otherwise zero;
* `M_05` is arbitrary only on the special chart `nu_0=-nu_5`.

The last chart is admissible exactly when no rank-one potential equals
`nu_5`.  Whenever it is admissible, its arbitrary `M_05` family contains
the `M_05=0` family as a specialization.

## Complete potential-graph split

An isolated rank-one vertex of `E` is a fixed root, giving
`rank(dPsi)<=42`.  Zero-sum graphs are unions of a zero-potential clique
and complete bipartite opposition components.  With five potential
vertices, zero and two signed nonzero magnitudes realize every abstract
case.  Exhaustion modulo `S_4` on the rank-one sites leaves the following
fourteen no-isolate orbits.  Edge labels refer to the displayed potential
representative, not to an additional canonical relabelling.

| chart | `(nu_1,...,nu_5)` | free edges in `E` | `M_05` | bound/method |
|---|---:|---|---|---|
| `matching2` | `(-2,-1,1,2,0)` | `14,23` | arbitrary | 35, polynomial syzygies |
| `rstar3` | `(-2,-2,-2,2,-1)` | `14,24,34` | arbitrary | 34, polynomial syzygies |
| `rpath2_z` | `(-2,-2,-1,2,1)` | `14,24,35` | arbitrary | 49, path shore `1-4-2` |
| `matching2_z` | `(-2,-1,1,2,-2)` | `14,23,45` | zero | 49, path shore `1-4-5` |
| `redge_z2` | `(-2,-2,-1,1,2)` | `15,25,34` | arbitrary | 46, polynomial syzygies |
| `rstar3_z` | `(-2,-2,-2,2,-2)` | `14,24,34,45` | zero | 30, polynomial syzygies |
| `rtriangle_z` | `(-2,0,0,0,2)` | `15,23,24,34` | arbitrary | 51, constant triangle shore `234` |
| `rk22` | `(-2,-2,2,2,-1)` | `13,14,23,24` | arbitrary | 35, polynomial syzygies |
| `matching2_z2` | `(-2,0,0,2,0)` | `14,23,25,35` | zero | 46, polynomial syzygies |
| `zstar4` | `(-2,-2,-2,-2,2)` | `15,25,35,45` | arbitrary | 50, support slices |
| `rk4` | `(0,0,0,0,-2)` | all six rank-one edges | arbitrary | 36, polynomial syzygies |
| `k23_zsmall` | `(-2,-2,-2,2,2)` | `14,15,24,25,34,35` | zero | 49, polynomial syzygies |
| `k23_zlarge` | `(-2,-2,2,2,-2)` | `13,14,23,24,35,45` | zero | 43, polynomial syzygies |
| `k5` | `(0,0,0,0,0)` | all ten edges | zero | 42, fixed root 0 |

The three shore bounds are the previously audited coordinate-shore
factorizations.  In the triangle chart, sites 2,3,4 have one common
isotropic pencil line, so their normalized cross spokes are constant.

## The Z-centred star support bound

For `zstar4`, every block not incident with site 5 is supported in colour
zero at each rank-one endpoint.  An incident block at site 5 may be
arbitrary.  Sort the 64 differential rows by the number `k` of colour-one
entries among sites 1,2,3,4.

There are respectively `4,16,24,16,4` rows of weights `0,1,2,3,4`.  A
base matching can carry colour one at at most one rank-one endpoint,
through its unique edge incident with site 5.  Consequently every
weight-four differential row is zero.  In a weight-three row, the varied
edge must remove two colour-one rank-one endpoints.  All sixteen such rows
therefore use only the six global `RR(1,1)` columns.  The remaining 44
rows contribute at most 44, so

\[
\operatorname{rank}(d\Psi)\le 44+6=50.
\]

This argument permits arbitrary blocks on the whole site-5 star and makes
no endpoint-genericity or R2 assumption.

## Polynomial-kernel certificates

At each rank-one site, a local physical change sends `h_i` to `e_0`.
The four root-spoke lines are normalized projectively.  Four generic lines
become

\[
e_0,\quad e_1,\quad e_0+e_1,\quad e_0+t e_1,
\]

and the pencil graphs impose the displayed line coincidences in the
smaller profiles.  Coincident-line and vanishing-fixed-block cases follow
by polynomial closure.  Except in `k23_zsmall`, every nonfree
rank-one/rank-one block is promoted to an independent scalar `E_00`; these
are support supersets of the geometric charts.  In `k23_zsmall`, the
three nonfree blocks lie inside one equal-potential pencil shore and are
simultaneously normalized to `E_00`; their zero degeneration again follows
by closure.

For each of the nine remaining charts, the checker constructs the exact
`64 x 60` differential over a rational polynomial ring, asks Singular for
`Q=syz(D)`, verifies `D Q=0` entry by entry, and specializes all variables
to consecutive positive integers.  The payload is

| chart | syzygy generators | `rank(Q_specialized)` | `rank(D_specialized)` |
|---|---:|---:|---:|
| `matching2` | 28 | 25 | 35 |
| `rstar3` | 31 | 26 | 34 |
| `redge_z2` | 86 | 14 | 46 |
| `rstar3_z` | 31 | 30 | 30 |
| `rk22` | 30 | 25 | 35 |
| `matching2_z2` | 18 | 14 | 46 |
| `rk4` | 29 | 24 | 34 |
| `k23_zsmall` | 15 | 11 | 49 |
| `k23_zlarge` | 42 | 17 | 43 |

Thus `rank(D)<=60-rank(Q_specialized)` identically in each normalized
family.  The SHA-256 digest of the complete generated Singular program is

```text
b06872d9a6318a3c10a8d39eca66bd24b11d23da139a9df195049c73c5abc554
```

The checker regenerates this program and prints its digest together with
every payload and support size.

Finally, in the complete `k5` chart the four nonzero rank-one pencil
vectors are pairwise `J`-orthogonal, hence share one isotropic line.
All root-0 spokes share one factor and `M_05=0`, so root 0 is fixed and the
rank is at most 42.

Every chart is therefore below 55.  The `1I+4R+1Z` stratum contributes no
residual rank-55 chart to `L0`, `L1`, or literal `R2`.
