# X5 four-blocker homogeneous degree-eight two-prime gate

## Verdict

All four canonical branches have exact primitive integer dual certificates in
homogeneous degree eight.  Each satisfies `L(t^8)=1`, annihilates every literal
degree-eight source column, and reduces exactly to the two independently
produced modular duals.  Hence `t^8` is not in the degree-eight source span over
characteristic zero for any branch.

This is an exact bounded nonmembership result, not a proof of the conjecture.
The blocker branches remain open in unrestricted degree.  Degree nine was not
designed or launched.

| branch | selected columns at each prime | support | exact equations / rank | exhaustive incident replay |
|---|---:|---:|---:|---:|
| triangle endpoint colour | 4,309 | 52 | 67 / 52 | 66 |
| cap endpoint colour | 4,192 | 52 | 67 / 52 | 66 |
| third colour | 4,243 | 52 | 67 / 52 | 66 |
| direct | 2,512 | 38 | 47 / 38 | 46 |

Every exact integer coefficient is `+1` or `-1`; every target coefficient is
`1`.  Each exact system is full rank on the union of its two modular supports.

## Growth from degree seven

The three coloured branches grow from roughly 1,940 selected columns at degree
seven to 4,192--4,309 at degree eight, a factor of about 2.2.  Their supports
grow from 17--23 to 52.  The direct branch changes regime: 15 selected columns
and support 10 become 2,512 columns and support 38.

Despite that growth, every producer remains far inside the 500,000-column,
120-second, 8-GiB limits.  Maximum engine wall is 41.411 seconds and maximum
observed watchdog RSS is 227,824 KiB.  Both primes produce identical
branch-wise selected counts and supports.

## Exact computation

The sealed degree-eight engine accepts only primes `1,073,741,827` and
`1,000,000,007`, uses the exact 361-variable/6,571-equation providers, and emits
only homogeneous `t^8` CEGAR evidence.  The eight runs are strictly sequential.

For each branch `lift_characteristic_zero.py` forms the union of both final
supports and enumerates every literal source column incident to it.  Exact
rational RREF solves

```text
L(t^8) = 1
L(m * g_i) = 0
```

and primitive-normalizes the solution over the integers.  It then re-enumerates
the incident columns from the nonzero integer support and replays all pairings
over `Z`; any other degree-eight source column is support-disjoint.  Applying
`L` excludes any rational identity for `t^8`.

`validate.py` independently reparses both literal providers, reconstructs the
complete incident set, checks every integer pairing, verifies reduction to both
producer duals, and checks all watchdog contracts.  Standard and isolated
Python outputs agree.  Optimized Python fails closed because assertions would
be disabled.  Five hostile mutations are rejected.

## Scope

- exact conclusion: four characteristic-zero homogeneous degree-eight
  nonmembership theorems;
- no finite-field rank or target-pairing anomaly;
- no conclusion in degree nine or unrestricted degree;
- no D12 cache read or mutation;
- conjecture status remains open.
