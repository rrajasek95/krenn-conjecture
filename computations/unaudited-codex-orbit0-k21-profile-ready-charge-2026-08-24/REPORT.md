# Exact K21 charge for the 14 profile-ready derived lineages

## Terminal verdict

`PASS_EXACT_K21_14_PROFILE_READY_77_CHARGE_SUBTOTAL`.

The exact full and K0-irreducible 77-charges are equal:

| quantity | value |
|---|---:|
| charge scaled by `U=400591699200` | `-4387451501777688723456` |
| reduced unscaled charge | `-24730854875640832/2258025` |
| source-compressed keys | `80,611,762` |
| exact profile-tail evaluations | `3,418,285,164` |

Every evaluated K21 child is K0-irreducible.  This is a strict 14-lineage
subtotal, not a complete K21 page.

## Strict coverage

The result and referee enforce ordered set equality, uniqueness, and count 14
for exactly these IDs:

1. `D14:222|R:3-4`
2. `D14:222|R:4-3`
3. `D15:223|R:2-4`
4. `D15:232|R:2-4`
5. `D15:322|R:2-4`
6. `D15:223|R:3-3`
7. `D15:232|R:3-3`
8. `D15:322|R:3-3`
9. `D16:224|R:2-3`
10. `D16:233|R:2-3`
11. `D16:242|R:2-3`
12. `D16:323|R:2-3`
13. `D16:332|R:2-3`
14. `D16:422|R:2-3`

No other lineage is read, inferred, or charged by this package.

## Five frozen groups

| lineage group | target | keys | tail evaluations | exact charge at scale U |
|---|---:|---:|---:|---:|
| `D14:222|R:3-4` | K4 | 13,844,092 | 830,645,520 | `-79090847743946784768` |
| `D14:222|R:4-3` | K3 | 18,217,226 | 582,951,232 | `-91407703075561635840` |
| `D15:{223,232,322}|R:2-4` | K4 | 16,109,793 | 966,587,580 | `-257936332936328183808` |
| `D15:{223,232,322}|R:3-3` | K3 | 25,564,391 | 818,060,512 | `-1658448665087993856000` |
| `D16:{224,233,242,323,332,422}|R:2-3` | K3 | 6,876,260 | 220,040,320 | `-2300567952933858263040` |

The first and third inputs are the frozen `K19SUM1` interfaces
`weights_k17_k14_k2.bin` and `weights_k17_k15_k2.bin`.  Their signed weights
at scale `281801520^2` were each divided exactly by
`198237 = 281801520^2/U` before their K4 evaluations.  The other three merged
profile checkpoints are already at scale U.  All five inputs already contain
the frozen signs and all earlier pivot denominators; changing only the final
tail degree introduces no new sign or division.

The D15 three-ID producers and D16 six-ID producer intentionally aggregated
equal-key weights before this run.  Their displayed group charges are exact,
but individual member scalars cannot be reconstructed source-faithfully from
these interfaces.  The two singleton D14 charges are individually exact.

## No-row-collection evaluator

The evaluator streams each frozen key once and computes cycle partitions from
the stored 29-byte open-path profile plus a K3 or K4 response tail.  It never
collects or emits parent or child rows.  The three checkpoint formats contain
a reversible witness row per key; those witnesses are read transiently only
to validate the stored signature/profile/pivot and literal cycle response.

The optimized cycle evaluator was checked against literal row replacement in
86,733 comparisons: 83,968 common K2/K3/K4 self-test comparisons and 2,765
distributed comparisons on actual checkpoint witnesses.  It also performed:

- exhaustive profile-structure, signature, pivot, order, and nonzero-weight
  guards on all 80,611,762 keys;
- literal witness-to-profile replay on all 50,657,877 checkpoint keys;
- exact merged header, record-count, use-count, weight-sum, scale, and file-size
  checks; and
- exact full/irreducible equality for each group and the subtotal.

The terminal run used eight workers and took 23.553501 seconds.  The
independent finalizer pins all five interfaces plus the structure, cycle-dual,
and K4-tail auxiliaries by SHA-256; it checks every group constant, strict ID
coverage, and group-to-subtotal arithmetic.

## Artifacts and replay

- final result: `results_k21_profile_ready_charge.json`, SHA-256
  `fb6ffb58271d96498d8219f4c23dc55664031ab279d589211e17e65d75392452`;
- raw producer result: `results_k21_profile_ready_charge.raw.json`, SHA-256
  `569d529bddae5101b5affdfadc4d5d523292cacf804d8483781335f050e97f24`;
- Rust producer: `run_k21_profile_ready_charge.rs`, SHA-256
  `cb0fc33783de0777ee65a9405e082b23baff222b7b08bd4faccca4b1853754ed`;
- arithmetic/hash referee: `finalize_k21_profile_ready_charge.py`, SHA-256
  `a566c40e20f305fec4549279cb4e9afc16b6b863261e53b9cf02573ef327a434`;
- referee result: `results_k21_profile_ready_charge_audit.json`, SHA-256
  `b3fab7f3f959f0aaa473549965e5e509ca6c8fe49299e54f37c34b6410a6649f`;
- logical result digest:
  `97bcd555f7f65d45f46b85c669cc361c01cd6d9aac65c95e610c63f529afc207`.

Replay the fast coverage/arithmetic/hash referee with:

```sh
python3 computations/unaudited-codex-orbit0-k21-profile-ready-charge-2026-08-24/finalize_k21_profile_ready_charge.py
```

Recompile and rerun the full exact evaluator with:

```sh
rustc -O computations/unaudited-codex-orbit0-k21-profile-ready-charge-2026-08-24/run_k21_profile_ready_charge.rs \
  -o computations/unaudited-codex-orbit0-k21-profile-ready-charge-2026-08-24/run_k21_profile_ready_charge
computations/unaudited-codex-orbit0-k21-profile-ready-charge-2026-08-24/run_k21_profile_ready_charge
```

## Scope boundary

This package proves only the exact 77-charge subtotal for the 14 named
profile-ready derived K21 lineages.  It does not charge the other K21
lineages, emit K22/K23/K24 tails, perform the terminal image-membership test,
or prove/disprove the conjecture.
