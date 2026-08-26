# Exact K20 charge for the 17 profile-ready DAG paths

## Terminal result

`PASS_EXACT_K20_17_PATH_PROFILE_CHARGE_SUBTOTAL`.  The four frozen
source-compressed parent-profile interfaces were evaluated at their K20 tail
degrees in 128.176 seconds, within the 300-second / 8-GB gate.

The exact 17-path subtotal is:

| quantity | scaled by `U=400591699200` | reduced rational |
|---|---:|---:|
| full charge | `3803430392150074785792` | `7146296281547008/752675` |
| K20-irreducible charge | `3740606478166067085312` | `49197791432108416/5268725` |

This is a charge-only result.  It collects no parent rows, emits no K21
tails, and is not a complete K20 charge.

## Four exact groups

| group | DAG paths | keys | full / irreducible evaluations | full charge | irreducible charge |
|---|---:|---:|---:|---:|---:|
| K14 `[3,3]` | 1 | 13,844,092 | 443,010,944 / 401,361,864 | `8787057500429952/5268725` | `25515701152594816/15806175` |
| K15 `[2,3]` | 3 | 16,109,793 | 515,513,376 / 468,973,320 | `32241356998754944/5268725` | `94958335994277632/15806175` |
| direct K16 `[4]` | 6 | 1,033,323 | 61,999,380 / 50,670,420 | `1528336896/11` | `8174449152/55` |
| direct K17 `[3]` | 7 | 2,661,633 | 85,172,256 / 77,326,608 | `54895036416/35` | `54849089536/35` |

`results_k20_17_path_profile_charge.json` lists all 17 literal DAG IDs and
checks exact set equality with the certified availability ledger.

## Aggregation boundary

The K15, K16, and K17 profile files aggregated duplicate parent profiles
across their direct-packet groups before this evaluation.  Their charges are
therefore exact for the named disjoint sets of 3, 6, and 7 DAG IDs, but the
archive cannot recover an individual scalar for each member without
regenerating pre-aggregation weights.  The result records a group pointer for
every path and explicitly marks those individual scalars unavailable; it does
not copy a group charge onto each path.

## Exact arithmetic and signs

The frozen profile scale is
`281801520^2 = 79412096674310400 = 198237*U`.  Every one of the 33,648,841
stored nonzero profile weights was exactly divisible by 198,237 before
evaluation.  The profile weights already include all prior pivot signs and
denominators, so changing only the terminal tail degree introduces no new
sign or division.

All full counts equal `keys*32` for K3 or `keys*60` for K4.  The four group
sums reproduce the displayed subtotal exactly over Q.

## Literal guards

The evaluator replayed 83,968 raw-row comparisons covering K2, K3, and K4:
for every sampled literal child, the cycle partition computed from the
compressed profile equals the partition computed from the full child row.
This matches the independently frozen K19 self-test (SHA-256
`e680b930dd187f90c3fc001ecdb9e89fbb3f1710a06994efe24978aeefcfc6d8`).

## Artifacts

- Final result SHA-256:
  `48fdf06e272357bea970d00e9ec00631be1cbc024b9dfc6ee2ec61ba5f13835c`;
  logical digest
  `7e8b3d71621560cc866b9bc50b3fc99608371af02d43d3f371f98e6d3a595504`.
- Raw result SHA-256:
  `067d1ec92ad12f147a59d97df35e62abdc488080d198111a0c12203b35c05c12`.
- Rust evaluator source SHA-256:
  `5dc769d7acff8ed3937bfc70f4d9551cdfaa367d83b2a7952a745d3129de3f98`.

Replay the arithmetic/coverage finalizer with
`python3 finalize_k20_profile_charge.py`.  Re-running the 1.1-billion-tail
Rust evaluation is not required for ordinary result verification.
