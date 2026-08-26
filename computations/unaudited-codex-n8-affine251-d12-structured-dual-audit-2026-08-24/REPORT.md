# D12 round-659/660 structured-dual shortcut audit

Status: **negative structural diagnosis**. No tested low-dimensional template
bypasses the sequential CEGAR process.

The read-only audit pinned the exact round-659 and round-660 checkpoints and
recomputed orbit-column incidences directly from the authoritative provider at
prime 1,073,741,827. It did not load the 505 MiB vector cache, advance a CEGAR
round, launch full closure, or run a second prime.

The round-660 candidate has 352 support rows, grouped by `t` exponent as
335 at exponent 0, 9 at exponent 1, 5 at exponent 4, 2 at exponent 8, and the
normalized target at exponent 12. Only four of the shifted D8–D11 seven-row
template survive. The eight high-`t` rows are identical between rounds 659 and
660, but they are not an independent dual.

The low-`t` portion is highly unstable: of 384 round-659 and 352 round-660
support rows, only 143 overlap; 241 disappear and 209 appear, with just 139
common rows retaining their coefficient. This is evidence against a stationary
support recurrence.

Exact incidence results:

- Full round-660 candidate: all 430 cached incident columns annihilate, as
  required, but its support has 1,354 global incident columns. Of 924 not yet
  cached, 913 violate the candidate. The first exact pairing is `2/2 = 1`.
- Shifted seven-row rational template: 10 of its 17 incident columns already
  violate it in the cached system; the first exact pairing is `-4/2 = -2`,
  reproducing the known D12 counterwitness.
- Stable high-`t` eight-row core: 13 of 20 cached incident columns violate it;
  the first exact pairing is `-32/2 = -16`.

Coefficient ansätze constant on `t` exponent (5 groups), `t` exponent plus
multiplicity partition (9 groups), and a coarse orbit signature (83 groups)
are each inconsistent even on the cached equations, hence also globally.
All modular pairings were independently replayed as exact half-integral
pairings (reported as integer numerators over 2).

The primary audit took 2.139 seconds. An independent replay matched every
mathematical field, taking 2.357 seconds with peak RSS 176,406,528 bytes, below
the 120-second/4 GiB contract.
