# Corrected direct-K19 and downstream charge-ledger referee

## Verdict

PASS.  The historical direct-K19 traversal duplicated the K3 action on
factor 0 and omitted factor 2.  An independent full replay with the three
factor positions enumerated once each gives

- 167,616,000 full evaluations and charge `174465024`;
- 55,872,000 irreducible evaluations and charge `126418944`;
- pivotable charge `48046080`.

Relative to the historical result, the full, irreducible, and pivotable
charge corrections are respectively `-27813888`, `-15151104`, and
`-12662784`.  A separate one-record literal control replayed 230,400 pivot
uses and found zero parent-versus-tail conservation failures.

## Corrected ledgers

Applying only the irreducible K19 correction (K20--K24 producer charges are
unchanged) gives the corrected complete 24-path K19 charge
`-2120489519568692992/173867925`.  The cumulative exact ledgers are:

| endpoint | cumulative charge |
| --- | ---: |
| K19 | `-515052118731534848/57955975` |
| K20 | `7526765090395921024/521603775` |
| K21 | `-2583153166877118208/173867925` |
| K22 | `144688922407749152/11591195` |
| K23 | `-832059102095222912/173867925` |
| K24 | `4564224` |

The actual K24 charge remains
`832852674251338112/173867925`.  The K24 value that would make the retained
K14--K24 ledger sum to zero is
`832059102095222912/173867925`; their difference is exactly `4564224`
(`1828390247689420800` after multiplication by U = `400591699200`).

## Meaning of the remaining scalar

The remaining `4564224` is neither a sign error nor another transition
failure.  An independent correct enumeration of all 27 raw packets gives

`230092800 - 539203584 + 388502016 + 53763072 - 272994816 + 174465024 - 30060288 = 4564224`.

Thus the corrected filtered K14--K24 ledger conserves the actual truncated
`-R8prime*E0*E1*E2` input exactly; its unexplained residual against that
input is zero.  The pinned source interface explicitly says that `R8prime`
is only the cutoff-nine K8 representative and can omit a K9 tail requiring
a separate full-column expansion.  A zero-charge conclusion belongs to the
full lifted `a*T`, not automatically to this truncated packet.  A missing
lift correction of charge `-4564224` is required if the full lift is to have
zero charge, but this package does not compute or assert that correction.

## Reproducibility and guards

`assemble_corrected_k19_through_k24_ledgers.py` pins the historical direct
result, complete K19 result, through-K23 ledger, accepted K24 result, sparse
R8prime representative, and its cutoff-interface declaration by SHA-256.
It rejects wrong corrected K19 values, wrong transition deltas, a forced
zero packet charge, a broken K19 ledger link, a changed K24 scalar, and an
erased K9-tail guard.  All six hostile cases pass under standard Python,
`python -O`, and `python -I -S`.

Scope is exact scalar correction and conservation only.  This package does
not recompute unrelated charge families, construct the omitted K9+ lift,
prove membership, or claim the conjecture.
