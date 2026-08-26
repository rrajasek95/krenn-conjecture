# Exact grouped direct-K16 K22 charge: 18 IDs

Status: **PASS** for exactly three grouped scalars covering the 18 frozen direct-K16 K22 IDs. The checkpoint has no six-packet labels after canonical collection, so individual packet scalars are deliberately not reported.

The strict subtotal is

`1655651771674136248320 / U = 1591211034496/385`, where `U=400591699200`.

| sink | IDs | p1 | later selected pivots | terminal K22 | scaled charge | exact charge |
|---|---:|---:|---:|---:|---:|---:|
| R3-3 | 6 | 129,939,187 | p2=2,041,782,688 | 65,337,046,016 | 1094959064000491683840 | 1052341425152/385 |
| R4-2 | 6 | 129,939,187 | p2=1,186,804,200 | 14,241,650,400 | 44519435361881948160 | 3889696768/35 |
| R2-2-2 | 6 | 129,939,187 | p2=2,049,974,172; p3=2,745,607,644 | 32,947,291,728 | 516173272311762616320 | 6442635648/5 |

Each sink replays all 24,097,095 retained literal K16 rows, whose exact signed coefficient sum is 1,464,625,152 and L1 sum is 13,978,655,136. There are 24,003,767 pivotable rows and 129,939,187 first-pivot uses. Literal rows are retained through every later pivot choice; only the last response is cached by `(profile, literal signature, pivot, degree)`. Every terminal response asserts full count/charge equals irreducible count/charge.

Two responses give sign `+v/(m1*m2)` for R3-3/R4-2; three give `-v/(m1*m2*m3)` for R2-2-2. Every divisor product divides U occurrencewise.

The accepted distributed 800,000-record gates projected 430.00, 163.70, and 233.59 seconds. Successful full runtimes were 195.604 seconds (R3-3), 111.544 seconds (R4-2), and 148.696 seconds (R2-2-2), each under an external 600-second alarm. Observed RSS peaks were about 1.14 GiB, 0.92 GiB, and 0.25 GiB, respectively.

R4-2 nonzero response support is concentrated: equal global strata realize only bins 0--36. Two attempted arithmetic publications therefore failed closed at the provenance guard and emitted no result. A separate 0.704-second read-only census pinned 772 distinct nonzero candidates from those 37 realized bins and froze 257 by round-robin traversal with exhausted bins skipped. The one authorized final arithmetic run imported that frozen ledger byte-for-byte.

The independent referee replayed 771 witnesses (257 per sink) from checkpoint bytes: all literal replacements, pivot sets/divisors, every terminal K3/K2 child, 77-charge, irreducibility, sign, and exact U-scaled contribution passed.

This is a partial K22 fragment only. It makes no complete-76-ID, row-membership, or conjecture claim. K23/K24 were not multiplexed.

Recheck with:

```sh
python3 computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/verify_k22_direct_k16_18_package.py
computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/referee_k22_direct_k16_18_literals computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/results_k22_direct_k16_33.json.samples.tsv computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/results_k22_direct_k16_42.json.samples.tsv computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/results_k22_direct_k16_222.json.samples.tsv
python3 computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py --audit-incomplete computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/k22_direct_k16_18_fragment_manifest.json /tmp/k22_direct_k16_18_partial.json
```
