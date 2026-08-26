# Triangle-plus-pendant `P26=0` exact characteristic-zero gate

Status: **UNAUDITED exact characteristic-zero branch closure.**

## Result

On the triangle-plus-pendant reduction, let

```text
F0 = b0*b1*b3*d4*d5*(b1*d4+b0*d5).
```

The exact eight-row boundary core with source labels

```text
7, 8, 9, 10, 12, 15, 19, 101
```

where row `101` is `P26=0`, has no characteristic-zero solution on
`F0 != 0`.  Equivalently, after adjoining the expanded Rabinowitsch equation
`z*F0-1`, msolve returns the literal empty sentinel `[-1]:`.

This closes only the `P26=0` boundary under the previously proved base-live
hypotheses.  It does **not** touch the `P26!=0` chart or its `N5^3` target.

## Exact gate

- Canonical input: `tp_p26_base_core_char0.msolve`
  (`62540e25e6dd53a668e48bef2af2f0fe4dcbcd0008138b1f210ae1af9d2523f6`).
- Variables: `z,a4,a5,b0,b1,b3,d4,d5`; characteristic zero; nine expanded
  polynomials (eight source rows plus `z*F0-1`).
- The strict shared parser accepts the input and rejects parenthesized,
  `**`, and coefficient-after-symbol syntax.  In particular, the historical
  `z*2*monomial` ambiguity cannot occur.
- msolve 0.10.1, seed 1, eight threads, exact characteristic-zero mode,
  completed in 4.55 seconds and returned `[-1]:`
  (`0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490`).
- Guarded manifest logical digest:
  `62019cf3279c50d713b276bd28bcf0abbcb4b6658f342dfae1f8a8316602a2aa`.

## Independent replay

`audit_tp_p26_base_core_char0_empty.py` independently reconstructs every
primitive integer source monomial/coefficient from
`cramer_branch_system(7,12)`, checks the exact two-monomial expansion of
`F0`, checks the expanded Rabinowitsch row, and accepts only the literal
empty sentinel plus the guarded manifest.

All three modes pass:

```text
standard  aaf071d24978e96692b3dcb761495d739c4ca303aebfd675ad73b70b8537fdc2
-O        e7cda9deecd7814d2ffbe979cb98b33775d94e69bcce7eaa64ff56c262cc08f2
-I-S      4d1870347c4637ccd88e3547d9894d92f91417788a4f54593d36c44e817dadd8
```

Must-fire controls negate a source coefficient, negate one `F0` monomial,
reject the positive-dimensional sentinel, and reject the historical
characteristic-zero `[1]` output as an empty certificate.

## Scope

The statement proved by this computation is precisely

```text
V_Q(rows 7,8,9,10,12,15,19,101) intersect D(F0) = empty.
```

No unlisted live factor is inverted.  In particular `a4`, `a5`, `H`, and
`Cprod` are not localized.  This report makes no assertion about the
separate `P26!=0`/`N5^3` LinBox lane.
