# Triangle-plus-pendant `P26!=0` exact characteristic-zero gate

Status: **UNAUDITED exact characteristic-zero branch closure.**

## Result

Let `R8,R9,R10,R11,R13,R15,R17,R19,R21` be the nine exact transported
Cramer rows and let

```text
L = F0*A3hat*P26*N4*N5*A2hat,
F0 = b0*b1*b3*d4*d5*(b1*d4+b0*d5).
```

Then the literal characteristic-zero computation proves

```text
V_Qbar(R8,R9,R10,R11,R13,R15,R17,R19,R21) intersect D(L) = empty.
```

The Rabinowitsch coefficient contains every frozen open-chart factor.  This
is therefore a theorem on the fully-live `P26!=0` Cramer chart, not the
unsound `N5`-only localization and not a statement at `P26=0`.

## Exact gate

- Canonical input: `tp_p26_interior_char0.msolve`, SHA
  `6c8d379f399465c73e475c09314bee3a315f8f89ca40e941fcff845f561fbd73`.
- Variables: `z,b0,b1,b3,d4,d5`; characteristic zero; nine transported rows
  plus one expanded Rabinowitsch row.
- Source row term counts are
  `(80,106,61,222,262,164,122,91,101)`.
- The factor profiles `(terms,degree)` in product order are
  `F0=(2,7)`, `A3hat=(8,4)`, `P26=(26,7)`, `N4=(18,7)`,
  `N5=(46,8)`, `A2hat=(31,7)`.
- The fully expanded coefficient `L` has 8,506 terms and degree 40; its
  normalized polynomial SHA is
  `8ad34518de21be8f18bab49dd5641da20ab6d1e8efcac01b7c732b96815a0f72`.
- Guarded msolve 0.10.1, seed 1, eight threads, and explicit exact-Q mode
  returned literal `[-1]:` in 14.286 seconds.  Manifest logical SHA:
  `2ca019ebd396746cd525d4eca2ac5a4cc4afbd59e27d55ad43d698ca3fa35466`.

The old boundary manifest's two-term `z` coefficient agrees exactly with the
`F0` factor in `L`; the new coefficient is its exact factor extension by
`A3hat*P26*N4*N5*A2hat`.

## Independent replay

`audit_tp_p26_interior_char0_empty.py` independently reruns the exact Cramer
ledger, reconstructs every source coefficient, multiplies and checks all six
Rabinowitsch factors, verifies the input/output bytes and guarded manifest,
and accepts only the literal exact-Q empty sentinel.  All modes pass:

```text
standard  b018155692b0956fdb948fd9c082d3c9563d8d977eb6b65746042cbce7cc8ecf
-O        575184d5efc66bb41f282d60e0647f8cad40cf3a2751810855ee535374a90c71
-I-S      c593fe9cb878e7fa2ea42cf122cbb7c5b1f4013466d9a8f8a97cde4972ca4f13
```

Must-fire controls mutate a transported source coefficient, mutate `P26`
inside the full live product, reject a positive-dimensional sentinel, and
reject historical characteristic-zero `[1]` output.

## Coverage with `P26=0`

The complementary exact gate in
`../unaudited-codex-tp-p26-boundary-char0-2026-08-21/` proves emptiness on
`P26=0,F0!=0`, with no `A3hat`, `N4`, or `A2hat` localization.  Its manifest
logical SHA is
`62019cf3279c50d713b276bd28bcf0abbcb4b6658f342dfae1f8a8316602a2aa`.
Consequently the two exact gates cover the frozen triangle-plus-pendant
stratum according as `P26=0` or `P26!=0`.

Within the `P26!=0` gate, the divisors `A3hat=0`, `N4=0`, `N5=0`, and
`A2hat=0` are excluded.  They are not unresolved triangle-plus-pendant
subcharts: each violates a frozen live/support antecedent (`N4/P26` and
`N5/P26` are the transported live `a4,a5` values).  No divisor subchart
compatible with the declared TP stratum remains outside the combined ledger.
