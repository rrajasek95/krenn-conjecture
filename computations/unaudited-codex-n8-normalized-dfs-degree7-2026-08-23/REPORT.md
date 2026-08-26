# N8 normalized degree-seven target-rooted DFS

## Terminal verdict

The source-faithful Rust provider is implemented and agrees exactly with both
independent Python first-shell censuses.  The minimal 78-word packet has a
clean coordinatewise acyclic `DEAD_END` at the first tail root.  The single
authorized all-mixed DFS enters a substantially larger cyclic core and hits
its ten-million-call cap with no pivot assigned.  Those DFS results are only
route diagnostics.

The authoritative exact closure independently proves
`t^7 notin I^h_7`.  The first saturation step has now also terminalized: an
exact 561-row rational functional pairs to one with `t^8` and annihilates all
752 literal bounded degree-eight incident columns.  Hence
`t^8 notin I^h_8` on the frozen normalized chart 26.  This does not decide
degree nine or unrestricted `t`-saturation.  No Groebner basis or second
all-word DFS was run.

## Exact provider

[`src/main.rs`](src/main.rs) implements the degree-seven homogeneous provider
over the order-four stabilizer of the frozen support product.  A row is a
sorted byte string of raw nonsupport coordinate IDs; its `t` exponent is
`7-len(row)`.  A column is a base-three eight-site word plus a normalized
multiplier of degree at most three; its multiplier `t` exponent is
`3-len(multiplier)`.  All 105 matching terms are emitted, equal normalized
monomials are collected with integer multiplicity, and no output is
truncated.

The provider reuses the dependency-first `PIVOT` ledger and its exact audit:
every selected column is distinct, its displayed diagonal is nonzero, and
every other invariant output must precede the pivot.  On failure it emits the
root, terminal reason, call/row/depth/cache census, last dead end, and up to
256 live visiting rows.

[`export_degree7_inputs.py`](export_degree7_inputs.py) independently rebuilds
the frozen six-column contraction and exports:

* [`degree7_tail_seed.txt`](degree7_tail_seed.txt): 564 tail roots with the
  common denominator two cleared;
* [`degree7_word_packet.txt`](degree7_word_packet.txt):
  `closure22^H+C5^H`, 78 literal words / 22 stabilizer orbits;
* [`degree7_all_mixed_words.txt`](degree7_all_mixed_words.txt): all 6,558
  mixed words / 1,672 stabilizer orbits.

The target selected by lex order is

\[
t^5x_{01}^{12}x_{34}^{12},
\]

encoded by raw-ID hex `05a7`; its cleared tail coefficient is `+1` (original
coefficient `+1/2`).

## Provider validation

The minimal packet reproduces the frozen census exactly:

```text
target roots                         564
canonical root-incident columns      294
one-hop invariant rows             25153
one-hop degrees       0:1,2:16,3:70,4:419,5:2330,6:7906,7:14411
column supports             56:25,65:1,101:5,104:4,105:259
entry coefficients                              1:29383,2:198
```

The authoritative all-mixed provider independently reproduces:

```text
target roots                         564
canonical root-incident columns      902
one-hop invariant rows             78081
one-hop degrees      0:1,2:16,3:111,4:953,5:5837,6:23922,7:47241
column supports       55:1,56:27,65:2,99:2,101:8,104:7,105:855
entry coefficients                         1:92843,2:362,4:1
```

The complete option histograms are frozen in
[`results_degree7_dfs_gates.json`](results_degree7_dfs_gates.json).

## Minimal-packet gate

The first root has five canonical packet pivots:

```text
word      multiplier  diagonal  invariant support
00000012  07             1             56
12000000  a7             1             56
12012000  empty          1             56
12012000  05a7           1             56
12012000  07f8           1             56
```

The deterministic target-rooted DFS exhausts its packet recursion and returns

```text
terminal             DEAD_END
target               1 / 564, hex 05a7
calls                22487
assigned / used      0 / 0
maximum depth        25
cached rows/columns  592 / 310
```

The exact terminal artifact is
[`degree7_dfs_failure.txt`](degree7_dfs_failure.txt).  This excludes this
coordinatewise acyclic triangular construction in the 78-word packet.  It
does not exclude a coefficient combination with cyclic cancellations and is
not linear-span nonmembership.

## Single all-mixed root gate

After validating the 902/78,081 shell, exactly one all-mixed DFS was run on
root `05a7`, with caps of 290 seconds, 10,000,000 calls, and 500,000 assigned
rows.  It terminalized at the call cap:

```text
terminal                CALL_CAP
calls                   10000001
elapsed                 6.644 s
assigned / used         0 / 0
visiting rows           539
maximum depth           565
cached incident rows    1383
cached output columns   2305
last dead end            0106349bec (3 options)
```

The exact terminal artifact is
[`degree7_all_mixed_root05a7_failure.txt`](degree7_all_mixed_root05a7_failure.txt).
Because the cap fires inside a live recursion, this is only a scale result.
It proves neither an all-mixed DFS dead end nor membership/nonmembership of
the root.  Per the bounded-run guard, it was not restarted with a larger cap.

## Authoritative degree-seven theorem

The later DFS request was superseded as a membership question by the existing
exact theorem in
[`../../notes/n8-chart26-normalized-degree7-critical-closure.md`](../../notes/n8-chart26-normalized-degree7-critical-closure.md)
and its source checker
[`../verify_n8_chart26_normalized_degree7_closure.py`](../verify_n8_chart26_normalized_degree7_closure.py).
The exact 49-row functional pairs to one with `t^7` and annihilates every
degree-seven translation of all 6,558 mixed words.  Its digest is
`b0f137c8827d8da94525a53636bd30791e7c56722b09a74e8cdfd0c792e75fb3`.

## Exact first saturation step

The degree-eight boundary has 190 new multiplier-degree-four columns incident
to the frozen degree-seven functional; 146 initially pair nontrivially, and
they expose 10,440 top rows.  The exact initial packet is frozen in
[`results_degree8_initial_core.json`](results_degree8_initial_core.json),
with logical digest
`6ee3465a73beb17a871669ccb480e68a9f96867d95fd6eb51fba4fb75a68c9da`.

The first exact Python lazy CEGAR remained consistent through 48 completed
rounds and stopped at its wall cap with 1,983 selected columns.  Its last
completed system had 1,977 selected columns, 114,087 exposed rows, rank
1,977, a 416-row extension, and six new crossings.  The deterministic handoff
is frozen as
[`degree8_round47_state.json.gz`](degree8_round47_state.json.gz), with manifest
[`results_degree8_round47_state.json`](results_degree8_round47_state.json).
It includes every selected column, every exposed row, the exact extension,
and count validations for rounds 0 through 10 and round 47.

The Rust sparse continuation then reached zero crossings at round 197:

```text
selected columns                         3097
exposed degree-8 rows                  147521
relative nonzeros                      226338
rank                                     3097
new degree-8 extension weights            512
multiplier-degree-4 incident columns       696
remaining crossings                         0
```

The modular terminal was replayed over exact rationals with the literal
source provider.  The resulting functional has 561 weights: the 49 frozen
lower weights plus 512 degree-eight weights.  Its digest is
`561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d`.
The independent checker
[`verify_degree8_rust_cegar_exact.py`](verify_degree8_rust_cegar_exact.py)
exhausts all 752 bounded incident columns, with multiplier-degree histogram
`0:1,1:3,2:6,3:46,4:696`, and obtains zero nonzero exact pairings while
`lambda_8(t^8)=1`.

The hostile control changes the weight of row
`0103093349bfc6f6` from 2 to 3.  Exactly one bounded column becomes nonzero:
word 56, multiplier `02061ec0`, pairing 1.  The checker passes identically in
standard, `-O`, and `-I -S` modes.  Therefore

\[
t^8\notin I^h_8\quad\text{over }\mathbb Q
\]

on this normalized chart.  No conclusion is made for `t^N`, `N>=9`, or for
the unrestricted saturation `I^h:t^infinity`.

## Replay

From the repository root:

```sh
python3 computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/export_degree7_inputs.py

cargo run --release \
  --manifest-path computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/Cargo.toml -- \
  computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/degree7_tail_seed.txt \
  computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/degree7_word_packet.txt \
  --census

cargo run --release \
  --manifest-path computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/Cargo.toml -- \
  computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/degree7_tail_seed.txt \
  computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/degree7_all_mixed_words.txt \
  --census
```

The DFS commands and caps are recorded in the result manifest; they should
not be replayed as part of a routine checker.

The terminal degree-eight certificate can be replayed without rerunning
discovery:

```sh
python3 computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/verify_degree8_rust_cegar_exact.py
python3 -O computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/verify_degree8_rust_cegar_exact.py
python3 -I -S computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/verify_degree8_rust_cegar_exact.py
```

## Digests

```text
tail seed
  36523c54c1a6dd466f6fe2fe936c3bed1d815d18042fb4c93edc98f92d2c7171
78-word packet
  cc4fd5cf7119646f3722f5dbb32599741cf260116a3a367336fe1054a8b44ae1
all-mixed packet
  0ab11f34ec0b625df5bb73ff4a7e22e3be1b751e1a84fbfddd48f653e4fe4e61
minimal failure packet
  8d563ba17f5646d59b42959174cca8e4f08ac0ec1440b7cf2323e1593aedd970
all-mixed root failure packet
  a127ac676ca79d4969c01ade69035ea70b97a9ea1d569f1271aa5527b599ebec
Rust provider source
  6b55da42de2facfb8e69e7bcbe0aefb0f198e237a1e54d39dbc80850235e5617
round-47 compressed handoff
  fa33ba3ad4ce8b7c3e4165a9f862c8d424de6a5ae58f71801c926cff60d8e169
terminal exact degree-eight certificate
  5d39aa3d8d6ae83a8b2b357e148232fb1046e069c79bed5ff8e5ff970b6d8485
independent exact replay checker
  e9bafcefff70c621a523847f03e8ac5a7df6d2af252c99fc3c9db22746d165fa
independent exact replay result
  294e0036976060bf47d3f2eb4fcad44262449c39714ecd7832f0d7a92e64f5f1
```
