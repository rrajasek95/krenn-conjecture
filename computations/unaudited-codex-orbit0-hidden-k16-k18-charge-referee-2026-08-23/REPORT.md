# Complete K18 charge referee

## Verdict

**PASS.**  The hidden `[2,2]` repair, 17-lineage K18 assembly, and corrected
through-K19 cumulative charge are exact under the frozen filtered recurrence.

The referee independently evaluates the 77-cycle functional on all `694,172`
rows of Cycle's literal prefix checkpoint.  It reproduces scaled full charge
`5001460982954459136`, irreducible charge `3397187219754516480`, and `408,972`
pivotable rows.  This supplies an independent literal control for the profile
linearity used by the full pass without duplicating its 6.23M-key computation.

Exact repaired values:

- hidden K18 `[2,2]` irreducible:
  `41042551470843904/24838275`;
- complete 17-path K18 irreducible:
  `109863564487489024/24838275`;
- corrected complete K19 irreducible:
  `-2117855228554753792/173867925`;
- cumulative K14 through K19:
  `-514174021726888448/57955975`.

Therefore a completed filtered reduction must contribute
`+514174021726888448/57955975` over K20--K24.  K20 is still incomplete: the
current repair supplies hidden `[2,4]` only.  No K18 row-membership or later
tail claim is made.

Replay with `audit_complete_k18_charge.py`; machine-readable logical digest
`16545784802980260c704bb42622d6f37bb7a8770dd2eeedc1db9a417a6f27ce`.
