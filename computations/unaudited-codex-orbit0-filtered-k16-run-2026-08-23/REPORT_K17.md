# Orbit-zero filtered reduction through K17

## Verdict

`PASS` for the single bounded K17 normal computation.  The source-correct run
finished in 64.528 seconds and stopped before K18.  An independent streaming
replay validates all saved rows as balanced K17 rows and evaluates the actual
77-coordinate cycle functional.

The result does **not** yet include the K19+ tails of the pivotable K17 rows.
It is therefore a K17 associated-graded normal, not a completed K24 reduction
or an ideal-membership certificate.

## Exact arithmetic and source components

All coefficients were multiplied by

```text
S = 281,801,520.
```

This is the LCM of every possible nonzero count of the 78 mixed pivots on all
4096 anchor-support patterns.  Hence every K14 valid-pivot average and every
K15 all-pivot average in this run is exact; no integer division is truncated.
All collection arithmetic uses signed `i128`.

The three literal sources of K17 are:

1. direct terms of tail profiles `2+3+4` and `3+3+3`;
2. K3 tails from canceling K14 via the frozen, equivariant valid-pivot rule;
3. K2 tails from canceling the wholly pivotable direct K15 bucket by averaging
   over all available literal pivots.

Occurrence-wise removal of K0-pivotable K17 children commutes with H-orbit
collection at this one graded page.  It does not authorize dropping their
higher tails.

## Census

Triples are `(support, signed mass, L1 mass)`, with masses still multiplied by
`S`.

- Direct K17: 82,938,880 irreducible occurrences collect to
  `(1,439,337, 25,243,644,896,870,400, 238,190,584,070,799,360)`.
- K14/K3 response: 14,402,560 irreducible occurrences collect to
  `(10,220,344, -132,228,616,126,464,000, 1,264,409,305,186,959,360)`.
- K15/K2 response: 219,763,200 irreducible occurrences collect to
  `(44,807,320, -405,581,228,009,717,760, 3,877,463,100,966,174,720)`.

The 56,467,001 component support slots have a 55,191,637-row union, with
1,275,364 overlap incidences.  Exactly 288 union rows cancel.  The reduced K17
normal is therefore

```text
(55,191,349, -512,566,199,239,311,360, 5,316,644,742,680,494,080) / S.
```

Equivalently, its signed mass is `-12,732,235,776/7` and its L1 mass is
`132,066,403,328/7`.

## Cycle charge

The exact unscaled 77-cycle-functional pairing of the combined K17 normal is

```text
-9,747,200,926,208 / 6,545.
```

It is nonzero and the projected normal has 183 nonzero cycle partitions.
Component pairings are:

- direct: `-62,386,176`;
- K14/K3: `-323,083,776`;
- K15/K2: `-7,224,300,090,368/6,545`.

As in the K16 page, nonzero charge at this truncated page is a migration datum,
not a full-polynomial separator: omitted higher filtration tails must eventually
carry the compensating charge.

## Artifacts and replay

- `results_filtered_k17_run.json`: byte SHA-256
  `b0918e220738c8818746f654fdfc4d2cc60a9f6269a3fb34da36eb84bf5dad49`,
  logical SHA-256
  `b9c68964bd437a351c7f2f0e76debaa923877b62f0a6ebec6db215276bec4d86`.
- Reduced K17 checkpoint SHA-256:
  `c1f4184bba99f4440ea1dafe2da93a90dcea815b104052967dfd64647bea5c05`.
- Direct / K14 / K15 component checkpoint SHA-256 values are respectively
  `0ac044a59f5c24ba7547ffcd95596a4f9696ea3717042d2d8916f6dccf3dc906`,
  `14ba9e46970287d4ef814b89764f272311f0a51a0245b24eaf570ff9eecdfe67`,
  and `f8845a8f16ba681a6ede91bed4c6905e2d270fa4d35f94bc1f824e34f25be0cb`.
- `run_filtered_k17.rs`: SHA-256
  `672f3925e5de1af03c3f9f75ab5e22893b713b8e64774e73abf174a6dffd87cf`.
- `audit_filtered_k17_checkpoints.rs`: SHA-256
  `a6e2c003a5c18c811c881047176e702109118d9922162e28b113fd0fbf43a89f`.
- `export_filtered_k17_aux.py`: SHA-256
  `c3ff1a90017df06b25e11ac4b6c489c37c10a9e8677451569ffd101eacd81354`.

The one-time scale `S` is certified for this construction/normal only.  A later
nested pivot division can require additional prime powers and must audit its
own denominator clearing.
