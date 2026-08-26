# Seeded X5 degree-11 gate: fail-closed coloured result

## Outcome

Overall status is `FAIL_CLOSED_COLOURED_D11_UNRESOLVED`. The direct branch is an exact characteristic-zero D11 obstruction, but the three coloured branches are not accepted. The four-branch first-prime condition failed, so no second-prime run was authorized. No D12 computation was launched.

## Exact transport

Appending `t=361` to the sealed D10 integer certificates gives exact D11 transports with violation counts:

| Branch | D10 support | Exact transported violations |
|---|---:|---:|
| direct | 243 | 0 |
| triangle endpoint colour | 251 | 76 |
| third colour | 253 | 76 |
| cap endpoint colour | 247 | 70 |

All nonzero offenders are literal t-free generator multiples. The direct transport therefore needs no repair. Independent integer replay checks all 326 incident columns with zero failures and target coefficient `lambda(t^11)=1`; certificate SHA is `d631677cef2be77de0f2f28e815bdb50ef93da484e0d2a548c6f8287f22f4c87`.

## Coloured triangle failures

The original general CEGAR emitted no result and was killed by the hard RSS gate after 174.594 seconds at 8,397,664 KiB. It contributes zero accepted coverage.

Two smaller exact formulations were tested under the same 180-second/8-GiB/500k-column contract:

- The transported support plus rows of its 76 offending columns yields 9,638 allowed rows and 20,636 incident equations. The target-normalized restricted system is exactly inconsistent (rank 8,717; 8.303 seconds; peak 328,392 KiB).
- The complete span of all 362 variable shifts of the D10 dual has union support 90,862 and 21,680 nonzero equation columns. It is exactly inconsistent at p=1073741827 (rank 283; 160.976 seconds; peak 514,536 KiB).

A wrapper-less one-hop census was rejected after exceeding 180 seconds; it emitted no result, has no accepted coverage, and is recorded explicitly in `one_hop_census_failure.json`.

Because the ordered triangle lane did not close, third-colour and cap-endpoint-colour repairs were not launched and the second prime was not run. This is a computational limitation, not a membership verdict for any coloured D11 branch.

## Pins and validation

Accepted engine source SHA is `57127904ab633bb5e9c58af1e66fe41cfae169659a32220a4460c998c54ef66d`; binary SHA is `faf03447eb47bfc5cdeeea8feba7a4027160504a6622161baea595f5becb24d5`. `results_final_audit.json` verifies the exact direct certificate, all no-result/resource guards, the two structured inconsistencies, absence of second-prime and D12 outputs, and the strict accepted/unresolved branch partition.
