# Independent grouped D15 R2-2-2 K21 referee

Status: **PASS** for exactly the grouped scalar

```text
D15:{223,232,322}|R:2-2-2
```

The retained R8 orbit masses permute packet labels, so the package certifies
one three-ID scalar and deliberately reports no individual-ID charges.

At `U = 400591699200`, full and irreducible charges are both

```text
-2089490736287288328192 / U
= -4849716689615104/929775.
```

The referee independently reconstructed the 485-slice source mass, checked the
full atomic interval `[0,485)`, all `[0,1)`, `[0,8)`, and `[0,32)` prefix
guards, every count identity, the complete denominator histogram, and the
three packet diagnostics summing back to the grouped result.  Exact counts are
6,704,640 source heads, 55,934,080 first-pivot uses, 671,208,960 K17 children,
451,445,760 pivotable K17 children, 1,876,057,600 second-pivot uses,
22,512,691,200 K19 children, 6,774,666,240 pivotable K19 children,
11,437,867,520 third-pivot uses, and 137,254,410,240 terminal K21 occurrences.

The sign is source-faithful: direct K15 coefficient `-positive` undergoes three
response sign changes, giving terminal coefficient
`+positive/(m1*m2*m3)`.  Every observed product divides `U`.  Signature mass
changes `9 -> 7 -> 5 -> 3`; since every frozen pivot has mass four, every K21
child is terminal and full equals irreducible.

The producer's 257 distributed source-slice witnesses account for 4,116
literal terminal children.  A separate referee in this package sampled 257
equal bins across all 6,704,640 source heads, scanned only 1,444 heads, required
a nonzero terminal cycle response, and literally replayed 3,084 more terminal
children.  It did not rerun the full fold and did not enter K22.

Replay:

```bash
python3 computations/unaudited-codex-orbit0-k21-d15-r2-2-2-referee-2026-08-24/audit_d15_r2_2_2.py
```

Logical SHA-256:
`7d9fef5ed2796f7e09b45ccbc7bc55af7f126cfeb2916cb15750f498fd328b27`.
