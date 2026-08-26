# Corrected complete filtered charge ledger through K21

The strict 52-lineage K21 assembly extends the corrected filtered 77-cycle
charge ledger by

```
K21 = -15276224591027275648 / 521603775.
```

The complete irreducible charges now pinned are:

| degree | exact charge |
|---|---:|
| K14 | `0` |
| K15 | `0` |
| K16 | `375127296` |
| K17 | `-9747200926208/6545` |
| K18 | `109863564487489024/24838275` |
| K19 | `-2117855228554753792/173867925` |
| K20 | `12162234158979734656/521603775` |
| K21 | `-15276224591027275648/521603775` |

Their cumulative charge is

```
-2580518875863179008 / 173867925.
```

Consequently, a completed reduction under the same convention must carry
aggregate K22--K24 charge

```
+2580518875863179008 / 173867925.
```

This is an aggregate conservation requirement only.  It is not a degreewise
prediction, a K24 residual, an ideal-membership or nonmembership certificate,
or a verdict on the conjecture.

The assembler pins the complete-through-K20 ledger, the strict 52-ID K21
manifest, and the byte-exact K21 result.  Standard, optimized (`-O`), and
isolated/no-site (`-I -S`) runs agree.  Self-tests delete a K21 path and mutate
the manifest; both fail closed in all modes.

Source SHA-256:
`7e4cc9c9301635e582b234edc1c15bed8c62fb02f0b6b698266acd1ab03c12b9`.
Result SHA-256:
`10d99f336bdbb0c98036cd9467a87c505a8b6a5ca5dff4623d6d399c95efb500`.
