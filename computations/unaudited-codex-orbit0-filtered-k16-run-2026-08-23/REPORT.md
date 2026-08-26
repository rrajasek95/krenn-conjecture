# Orbit-zero filtered reduction through K16

## Verdict

`PASS`, for the deliberately bounded scope through completed `K16`.  The one
Rust collection/reduction run finished in 13.656 seconds.  Its exact streaming
finalizer replays all saved buckets, verifies the sign convention, and confirms
that the reduced `K16` checkpoint contains no remaining `K0`-pivotable row.

This is not a `K17+` computation and is not an ideal-membership statement:
higher tails emitted by the `K15`/`K16` pivots have not yet been constructed.

## Sign convention (load-bearing)

The requested residual is

```text
P = -R8' E0 E1 E2.
```

For a coefficient `r` of `R8'`, the K14 head in `P` is `-r*head`.  Literal
division by the normalized source column `head+tail` gives

```text
(-r*head) - (-r)*(head+tail) = +r*tail.
```

The frozen collector used `pair_mass=+r` and `pivot_weight=-r`; its stored
response is therefore `-r*tail`, the normal response for the opposite positive
input.  Consequently the source-correct K16 bucket is

```text
direct negative seed - frozen stored response.
```

This agrees with the independent sign referee.  Adding the frozen response
would have been unsound.

## Exact checkpoints

All triples below are `(nonzero H-orbits, signed mass, L1 mass)`.

- K14: 838,080 raw H-slice/head pairs reduce to zero.  The isolated K2-tail
  response has 1,848,174 H-orbits.  Frozen byte SHA-256 is
  `28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189`;
  logical SHA-256 is
  `8eb9f7dbb220afd759533c10a4881a502a43bdb3bfa28c36e3b89cf98a4ee58c`.
- K15 direct: `(5,311,211, 322,486,272, 3,083,240,448)`.  Every row is
  K0-pivotable, so the reduced K15 checkpoint is empty.
- K16 direct: `(24,097,095, 1,464,625,152, 13,978,655,136)` from 30,450,240
  raw direct occurrences.
- Frozen stored response: `(1,848,174, 118,692,864, 1,134,990,336)`.
  Direct and frozen supports are disjoint: overlap `0`, exact cancellations
  `0`.
- K16 combined before reduction:
  `(25,945,269, 1,345,932,288, 15,113,645,472)`.
- Removed as K0-pivotable:
  `(24,003,767, 1,459,026,432, 13,925,880,960)`.
- Reduced K16:
  `(1,941,502, -113,094,144, 1,187,764,512)`.

The actual 77-coordinate cycle functional on that reduced K16 bucket is
`+375,127,296`; this is separate from the signed coefficient mass.  It sees
121 nonzero cycle partitions.  The dual file SHA-256 is
`fea91d03250128fa6ea99252659ddd2b46329a9318916a19d6dae0ecfb69dd84`.

## Replay and artifacts

- Input exporter: `export_filtered_k16_inputs.py`, SHA-256
  `f4eb39b00daf3191a7516c6deab443463ba02644cd380fe8a6620f8349dcf361`.
- Rust driver: `run_filtered_k16.rs`, SHA-256
  `85f9a3f1c18491bab52d06a0b25c9c88cc191ea55cb8eb666a70a62a36555432`.
- Exact finalizer: `finalize_filtered_k16_run.py`, SHA-256
  `bea07e823daa07ebada6789d6ccfba8da909334e0c2b94c19eb78b58fa6744ee`.
- Result: `results_filtered_k16_run.json`, byte SHA-256
  `ff4505a44cc76894ede59f4c642d385cf21ecffd5ac0aae875f7652c4966b861`,
  logical SHA-256
  `f5852b3bb53e727aea56b495bfcab4bbf5f6c40ce46f64eaae0a875ded75ac59`.
- Reduced K16 checkpoint SHA-256:
  `9a4dd3561a0952c85e4e12c9dbb7e2509317c79b50589479aaefd387cc52fa06`.

The finalizer independently re-filters the reduced K16 file and finds zero
additional pivotable rows.  No K17 or higher bucket is emitted in this report.
