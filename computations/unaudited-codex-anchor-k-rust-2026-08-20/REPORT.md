# Rust anchor-K accelerator report

Status: the no-crate Rust accelerator is qualified for sparse modular solves,
common-echelon projection, generic stabilizer-orbit closure, multiplicity-aware
incident columns, cascading singleton peeling, and reverse pivot provenance.
Rust output is discovery data; labelled exact-Q replay is still the proof gate.

## Correctness controls

- The early-stop regression leaves only the genuinely free row after reducing
  a higher pivot. The set-vs-multiplicity regression sums a duplicated entry.
- Python independently rebuilds each small common echelon, compares Rust
  residual/solution vectors, replays them on the original columns, and fires a
  solution mutation. Logical regression digest:
  `b6187821552add215f6c92a93c41374936f6fdf9b377fc96fd0b49017e82b93d`.
- At zero26/d6, Rust matches all 22 Python layer pairs, all closure/peel counts,
  both term histograms, and emits a byte-identical coupled interface at SHA
  `44f6b03db967e629cf01ab2cde304948acd27e8adccb342431c6fa985383bf61`.
- The restricted direct component has the exact-Q one-row dual `lambda=e_2`:
  all 8,889 serialized columns pair to zero and the target pairs to `-8`.
  Digest: `0bda602088c3c00b7d7520acb24bfeb597634bed2d036daf6b790560a7271345`.
  This is only a restricted-direct obstruction because lower-kernel tails were
  absent there.
- Standard, `-O`, and `-I -S` Python replays return the same two digests.

## Performance

The exact-order zero26/d6 closure took 4.235 s, cascading peel 0.661 s, and
5.416 s end-to-end including JSONL emission. The Python producer took 179.5 s,
so the end-to-end speedup is 33.1x. The sparse modular solve itself takes about
0.015--0.423 s on the tested matrices. Release builds took 1.52--2.22 s.

Peak RSS was not measurable: managed macOS `/usr/bin/time -l` failed its
`sysctl kern.clockrate` query. Artifact sizes and all timings are frozen in
`results_benchmarks.json`.

## Superseded chosen-section zero26 frontier

The producer seed combines the 12,705-row residual with the union of 123,620
lower-kernel transfer rows (124,184 distinct seed rows), SHA `a19f509e...`.
Rust closes this to 192,429 rows / 480,814 columns in nine layers and peels to
9,247 rows / 9,835 direct columns. It projects all 3,274 lower-kernel transfers;
2,316 remain nonzero with 48,142 entries. The 183,182-step pivot ledger records
the literal word, multiplier, pivot coefficient, and reverse order needed for
back-substitution.

The augmented 9,247 x 13,109 system has mod-1009 rank 7,773 and a 704-entry
target residual. A two-row modular dual `-e_4+e_318` annihilates every serialized
column and pairs `-8` with the target. This is not a Q obstruction: the transfer
basis itself was constructed modulo 1009, and the result has not been lifted
or independently rebuilt at another prime.

This construction is **incomplete and its obstruction is withdrawn**: the chosen min5
singleton corrections omitted the 36,755-dimensional intrinsic min5 kernel.
It is retained only as a regression showing why the direct cutoff closure is
necessary.

## Source-faithful cutoff 7 identity

The correction-free closure starts from all 1,017 target row orbits below
degree seven (actual mass 12,169), includes every incident source column of
minimum degree below seven, and retains every output below seven. It closes in
six layers at 218,187 rows / 558,104 columns in 10.4 s and peels to a
13,697 x 25,561 core.

A fixed 13,202-column minor solves at 32 compatible primes. CRT and rational
reconstruction give an 11,460-term exact core solution, replayed with Python
`Fraction` on every core coordinate. The independent dangerous-chart referee
then rebuilds literal columns from the 105 matchings and reverse-solves all
204,490 singleton pivots. It uses 125,231 nonzero pivot terms, for 136,691
orbit-average source terms total, and proves

`H0 H1 H2 in I_mix + K^7` over `Q` for zero26 / legacy29.

The normalized full-referee digest is
`01d802903ad2f51f1a4fc705d4447883311f7ebcca19009b3ed2874ebb96d752`.
The core interface is byte-identical to the independent producer at SHA
`487662cd76c11452bd8bf7feb343f290bffc3a623b18988c974d395ebdf55328`.
This advances the ladder but is not full localized membership; cutoffs 8--13
remain.

## Cutoff 8 scaling

Cutoff 8 has 2,725 target row orbits (actual mass 37,513). The direct closure
completes in nine layers at 2,248,460 rows / 4,137,457 columns, then peels to
680,620 rows / 935,795 columns. Closure took 115.8 s, peel 15.1 s, and total
time including the 166 MB JSONL was 208.7 s. Interface SHA:
`94e6eb39892534c1dc0b1d2523e2c464747e2f75ec3c1c96b3e9c7954cfeea`.
The current sparse echelon representation is not appropriate for that core;
the next accelerator needs block/component decomposition or a more compact
binary streaming matrix.

An exact structural pass shows that this peeled core is one connected
bipartite component with 4,426,334 nonzeros and all 1,181 target coordinates.
Its column support is at least two.  The complementary row-leaf peel starts
from 56 leaves and removes only 58 rows/columns, leaving one
680,562 x 935,737 component.  Thus neither connected components nor leaf
peeling explains the remaining zero26 cutoff-8 algebra.

## Maximally symmetric orbit0 ladder

Zero-based pure-matching orbit0 has three identical perfect matchings and a
2,304-element anchor stabilizer.  The generic reader accepts both producer
seed magics and both `ROW`/`TARGET` record names; canonicalizing an already
quotiented seed is idempotent.  A word-first column comparison plus bounded
row/column canonical caches preserve the cutoff-7 and cutoff-8 interface
digests while reducing runtimes from 40.4 to 4.1 seconds and from 221.8 to
23.7 seconds respectively.

At cutoff 7, 12,169 labelled target rows become 36 row orbits.  Closure is
2,438 rows / 14,369 columns and peeling gives a 363 x 1,519 core.  An exact
94-term integer core solution lifts through 2,075 pivots to 359 nonzero
integer orbit-average source terms.  The independent raw-105 referee replay
has stable digest `9aaab21c...`; the coupled interface SHA is
`bcd16826c7a30f7d1f0c1eb82229fde1ed5fdcf6f5b1f2a33244370b0d322f6d`.

At cutoff 8, closure is 19,210 / 68,372 and peeling gives a
5,515 x 15,240 core.  Three-prime CRT gives a 96-term integer core solution,
lifting to 370 integer source terms.  The independent raw-105 replay passes;
its result digest begins `f7b5b229`.  The interface SHA is
`c1a644fee353761db6d0d4d1a986697635f8781187cfc2462e321566c4693bed`.

Cutoff 9 is the terminal obstruction for this chart.  Closure is
152,386 / 275,495 and peeling gives an 80,894 x 115,839 core.  At primes 1009
and 1013 it has rank 50,420 and the same 37-row dual support.  Exact rational
reconstruction gives a half-integral dual that annihilates every core column
and pairs `2304` with the target.  Its pullback through all 71,492 pivots uses
zero new nonzero coefficients.  Standard, `-O`, and `-I -S` replay digest:
`f6b354c2f79823d69d0daaf3456fa8367fcce740dd2815da1a2e259e01091439`.
Therefore

`H0 H1 H2 notin I_mix + K_orbit0^9` over `Q`.

Because `I_mix` is contained in `I_mix + K_orbit0^9`, this also proves the
chart-independent negative statement `H0 H1 H2 notin I_mix`.  Orbit0 is
consequently an excellent low-cutoff control and a decisive falsifier of the
exponent-one global-target strategy.  A finishing argument must instead use a
target power, anchor saturation, or another genuinely localized unit.

## Main commands

```sh
cargo test
cargo build --release
target/release/anchor-k-echelon solve INPUT.jsonl OUTPUT.json 1009
target/release/anchor-k-echelon project BASIS.jsonl TRANSFERS.jsonl PROJECTED.jsonl 1009
target/release/orbit_closure SEED.txt DIRECT.jsonl RESULTS.json \
  LOWER_KERNEL.jsonl AUGMENTED.jsonl PIVOTS.jsonl
python3 verify_accelerator.py --write-results --exact-dual \
  ../unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/degree6_coupled_matrix.jsonl \
  results_degree6_core_p1009.json results_degree6_core_p1013.json
```
