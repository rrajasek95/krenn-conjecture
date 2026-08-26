# Five-set response surjectivity

Status: **UNAUDITED exact two-prime PASS**.  This proves a useful open-chart
lemma for the triangle cross-word route.  It does not prove that a
hypothetical exact `X5` point lies on that open chart.

## Result

Fix a residual triangle `T`, a vertex `t in T`, the opposite edge
`xy=T\{t}`, the remaining three sites `O`, and

```text
W = {x,y} union O.
```

Let `S_W` be the span in the five-site word space of the fifteen literal
cofactor-insertion columns `e_(u,a) tensor H_(W\{u})`.  For a colour `c`,
adjoin the pure column `e_c^5`, and let `g_c` be the `t=c` slice of the
four-site tensor on `{t} union O`.  The nine opposite-edge response columns
are

```text
                         Z tensor g_c,  Z in Mat_3.
```

The Rust checker computes the exact finite-field rank increment

```text
rank(S_W, e_c^5, {Z tensor g_c}) - rank(S_W, e_c^5).     (1)
```

When (1) is nine, elementary duality says that

```text
{beta : beta(S_W)=0 and beta(e_c^5)=0}
       -> (Mat_3)^*,  beta |-> [Z |-> beta(Z tensor g_c)]
```

is surjective.  Combining this with the literal five-set annihilator
identity proves:

> On the rank-nine open, every coordinate functional of the omitted
> response edge `R_xy` belongs to the row span of the triangle carrier
> `L_T`.

Doing this for the three cyclic choices of `t` absorbs all three internal
triangle response edges.  This closes the previously informal `18`-term
part of the `60=6+18+36` cross-word decomposition on a precise determinantal
open.

## Census and interpretation

The program evaluates all

```text
28 cap pairs * 20 residual triangles * 3 cyclic vertices * 3 colours
  = 5,040
```

profiles per source.  The ledgers are byte-for-byte identical at primes
1009 and 1013.

| source | rank-nine profiles | all three cyclic maps rank nine |
|---|---:|---:|
| dense exact control | 5,040 / 5,040 | 1,680 / 1,680 |
| W40/X4 | 852 / 5,040 | 8 / 1,680 |
| W25/X3 | 1,663 / 5,040 | 157 / 1,680 |
| sparse triangle guard | 204 / 5,040 | 0 / 1,680 |
| old all-pair missing-row countermodel | 3,100 / 5,040 | 332 / 1,680 |

Thus the open is nonempty: a rank-nine modular instance certifies a nonzero
rational minor because nine is the absolute maximum.  The old structural
escape model has many rank-nine instances and many lower-rank instances at
both audit primes, so the test is not a density proxy.  The rank-nine
claims lift rigorously to characteristic zero; the lower-rank histogram is
a two-prime boundary screen, not yet a characteristic-zero upper-rank
certificate.  It does not by itself rule out the stubborn branch.

The remaining proof obligation has a sharper form: either force a relevant
triangle onto this simultaneous rank-nine open and finish the six direct
terms, or show that every exact point on the determinantal boundary yields
the old good-pair `E1/E2` degeneracy strongly enough to descend to a clean
cap.  This is now a finite rank-stratified problem rather than an unbounded
Groebner calculation.

## Implementation

The dependency-free Rust program enumerates matchings and performs modular
column reduction directly.  A complete source takes about 0.25--0.38
seconds in release mode on the audit machine.  Three unit tests pin perfect
matching counts, endpoint transposition, and modular column rank.

Replay:

```sh
python3 computations/unaudited-codex-five-set-response-surjectivity-2026-08-22/export_sources.py --prime 1009
python3 computations/unaudited-codex-five-set-response-surjectivity-2026-08-22/export_sources.py --prime 1013
cd computations/unaudited-codex-five-set-response-surjectivity-2026-08-22/rust-five-set
cargo test --release
cargo run --release -- ../sources_p1009.txt
cargo run --release -- ../sources_p1013.txt
```

Full ledgers and pinned hashes are in `results.json`.
