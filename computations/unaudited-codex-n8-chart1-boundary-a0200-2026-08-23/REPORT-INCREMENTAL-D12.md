# Chart 1 boundary D12 incremental CEGAR

## Terminal status

`BOUNDED_RESUMABLE_UNRESOLVED`.  The persistent modular basis exactly rebuilt
the frozen 2,613-column resume and accepted six further CEGAR batches through
round 12.  The atomic checkpoint contains 7,516 selected column orbits, all
independent over `p=1073741827`.  Round 13 was scanning a 1,204-orbit incident
set when the live-RSS guard stopped the process; no round-13 columns were
accepted and no membership/nonmembership claim follows.

The monitor observed 18,288,816,128 bytes at its first over-limit poll versus
the nominal 16 GiB limit 17,179,869,184.  This is a monitor-granularity
overshoot, not an allocator failure.  A resume must use bounded memoization and
finer polling before it is allowed to run.

## Accepted ledger

| round | rows before add | columns/rank | remainder | dual | incident | accepted | post-rank |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 125,328 | 2,613 | 34,312 | 8 | 530 | 523 | 3,136 |
| 8 | 155,063 | 3,136 | 34,400 | 9 | 649 | 639 | 3,775 |
| 9 | 186,995 | 3,775 | 34,462 | 22 | 856 | 708 | 4,483 |
| 10 | 197,380 | 4,483 | 34,609 | 45 | 2,402 | 2,025 | 6,508 |
| 11 | 249,354 | 6,508 | 34,733 | 29 | 1,247 | 969 | 7,477 |
| 12 | 273,788 | 7,477 | 34,595 | 1 | 39 | 39 | 7,516 |

For every accepted batch `accepted_rank_increment == accepted_columns` and
`accepted_zero_columns == 0`.  Thus the rapid growth is genuine column-space
growth in the chosen invariant quotient, not repeated dependent repairs.
Private-row ownership was not recorded by the first driver and is not claimed.

## Post-run no-solve shell-ownership theorem

The subsequent exact ownership replay removes that last uncertainty.  Relative
to the frozen 2,613-column/125,328-row interface, **every one of the 4,903
accepted repairs owns a target-zero row occurring in no other accepted repair**.
There are 151,184 distinct beyond-interface rows, 125,594 of ownership degree
one.  Coverage by round is respectively 523/523, 639/639, 708/708, 2,025/2,025,
969/969, and 39/39.

The unaccepted round-13 shell has the same form *internally*.  Replaying its saved modular
dual gives 1,204 incident column orbits, of which 1,186 are new violations;
all 1,186 own a row beyond the current 7,516-column interface.  That shell has
58,234 new rows, 54,575 of ownership degree one.  The lex-first witness is the
literal single source term
`(code=4,multiplier=0a51b7ea,term=125191eb,coefficient=+1)` on row
`0a12515191b7eaeb`.

Thus all observed rank growth is explained by a diagonal shell-private-row block.
These columns cannot participate with nonzero coefficients in a representation
of the old target.  They can instead be handled by a target-rooted dual/Morse
extension: use one private row per column to cancel its current dual pairing,
then expose later columns crossing those chosen rows.  It is not a terminal
separator: the lex-first shell-private row `0a12515291c1e5eb` is incident to 91
full D12 column orbits.  Besides its shell owner `(4,0a52b8ee)`, the lex-first
external owner `(4,0a12515291c1e5eb)` also has coefficient `+1`.
The complete bounded replay gives an external, unselected, outside-shell owner
for all 1,186 shell columns.  Chosen rows have 26--122 full incident column
orbits.  Artifact: `results_d12_shell_counterowners.json`, logical SHA-256
`d04715ede95aa4194acf0f2ee9dd829e568a1b09186c6cc6dfdf685375ed7444`.

Artifact: `results_d12_private_ownership.json`, logical SHA-256
`224bf26bbc8523b4c4f55d63d8b44236af63360063d8b1f1e403ae9fb79d88a1`.
Its fields named `global_private_new_row` mean global only within the explicitly
listed accepted/pending packet.  They are superseded for full-D12 incidence by
`results_d12_first_external_owner.json` and the counterowner census.

## Bounded-memory audit

The original memory growth was provider-side, not Rust elimination: it retained
the 992,250-term literal target, an unbounded row-orbit cache (up to 32 expanded
rows per key), and every invariant column output.  A no-solve replacement built
the invariant target directly, canonicalized row orbits without memoization,
and streamed column outputs.  It reproduced the complete frozen 2,613-column /
125,328-row interface in 127.9 seconds at 216,727,552 bytes peak RSS.

Artifact: `results_d12_bounded_memory_prefix.json`, logical SHA-256
`fa2bd5fcd64f0a6ea955d9332fcb26a916e1c0f45cf8e7f3c4758b1273108081`.
Any resume should use this streaming design, evict incident batches after each
round, and poll at most every 64 columns / one second.  The old unbounded-cache
driver must not be resumed as written.

## Replay interface

- Driver: `run_d12_incremental_cegar.py`
- Rust source: `rust-d12-incremental/src/main.rs`
- Atomic resume: `checkpoint_d12_incremental_cegar.json`
- Frozen result: `results_d12_incremental_cegar.json`
- Binary SHA-256: `98710ac0a0077aa904a5b9a56e4a86261dcc9475d343418dcb403f54ef079007`
- Result logical SHA-256: `c55e82c04368264ab978f45f9e41c7502194684182c9c994c2a15350d81b442b`

The Rust process retains pivots across `ADD` commands.  Python remains the
literal source/orbit provider.  Terminal modular stall/member status is not a
theorem: the driver requires a second-prime rational lift and exact expanded
literal-column replay for a separator, or an exact rational source combination
and literal expansion for membership.

## Exact scope

This is the homogeneous degree-12 `F^h` question in the normalized chart-1
boundary `A_02[0,0]=0`.  It is neither a saturation/radical certificate nor a
closure of the 31-chart atlas.  The current result is only a resumable modular
growth checkpoint.
