# Exact K17 component and policy referee

## Result

The next bucket is source-faithfully defined by exactly three components:

```text
direct K17:
  -R8' * (six ordered E2*E3*E4 terms + E3^3)

K14 -> K17:
  +R8' leading-head masses / frozen valid-pivot count
  times each selected pivot's 32 K3 tails

K15 -> K17:
  for collected K15 mass p, -p/(all dividing pivots)
  times each selected pivot's 12 K2 tails
```

There is no K16 feed because K16 pivots first emit at K18.  The exact raw
counts before collection are `82,938,880` direct occurrences and
`211,816,960` K14/K3 occurrences; the K15 interface contains `5,311,211`
H-orbits, all pivotable.

The K14 policy remains the frozen 25-cover-valid average.  K15 and the future
K17 projection use the declared average over all literal dividing K0 pivots.
This policy is H-equivariant: all K2/K3/K4 tail transports replay exactly
(`359,424`, `958,464`, and `1,797,120` checks).  It is a chosen normal form,
not a confluence theorem.

The next engine must support exact rationals.  Reducing K15 introduces
denominators `1,5,7,11,17,23`; an integer-only Rust accumulator would be
unsound.

No K17 collection or long run was launched.

## Exact integer clearing guard

`SCALE=281,801,520` is exactly the LCM of every nonzero all-pivot count on the
4,096 anchor supports, and every frozen K14-valid count divides it.  The
largest collected K15 orbit mass is 6,144, so one scaled contribution is at
most `1,731,388,538,880`.  Even the hostile bound in which 300 million such
terms collide is `5.19416561664e20`, a factor `3.2756e17` below `i128::MAX`.

The scale is certified for constructing the K17 bucket and its K17 normal.
It is not automatically sufficient for another pivot division at K17:
successive divisions can require repeated prime factors such as `5^2`.
Likewise, killing pivotable occurrences before H-canonical collection is
linear and sound for the K17 normal, but a full K24 transfer must emit their
K19/K20/K21 tails before dropping them.

Replay:

```text
python3 computations/unaudited-codex-orbit0-filtered-k17-interface-referee-2026-08-23/audit_filtered_k17_interface.py --write-results
```

Logical digest:
`5cc33c5ac5c9bdbca5ec4761dca504ce82eafc9ac4e8163968166752d0cfa565`.

Scale-guard logical digest:
`d5b7c8f17e833a81ed429b4f1779244cde7f511e6632a6fbb6d4063b9bc7380b`.
