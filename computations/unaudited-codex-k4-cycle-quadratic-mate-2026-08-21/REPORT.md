# k4-cycle modular component source referee

## Terminal verdict

The frozen `all_minor_components` factors are **not** full one-colour packet
points.  At each of the two primes, all 16 decoded RUR factors satisfy the
reduced rank interface, but every factor violates every omitted literal row
`cofactor_e_3` for `e=1,...,5`.  Therefore the proposed fixed-left arbitrary-
mate solve has no valid input among these components and was not launched.

This corrects only the scope of the finite component export.  The exact
characteristic-zero all-minor solve is positive-dimensional, so this modular
rejection is not an emptiness theorem for that scheme.

## Literal replay

The referee preserves the p-coordinate order

`(p1,p2,p3,p4,a0,a5,b0,b1,b3,d1,d3,d4)`

and replays 22 source rows on every factor:

- six permanent equations `1+a_e*d_e+b_e*c_e=0`, which are exact identities
  under the chart definition of `c_e`;
- the four raw triple rows `t_012,t_013,t_023,t_123`;
- `cofactor_e_0` and `cofactor_e_3` for all six edges.

The 11 displayed rank-interface rows vanish on every factor.  The five rows
omitted by the producer checker are nonzero on all 16 factors at both primes:

| prime | factor-degree profile | nonzero count for each omitted row |
|---|---|---|
| 1073741827 | 2:6, 6:2, 24:4, 28:2, 46:2 | 16/16 |
| 1073741789 | 2:6, 4:6, 10:2, 106:2 | 16/16 |

Literal `H`, `p_i`, `1+p_i`, and `b0,b1,b3,d1,d3,d4` are nonzero on every
factor, so rejection is genuinely by the omitted source equations rather
than by failure of a selected-live guard.

## Targeted quotient certificate

Among the omitted rows, `cofactor_1_3` is selected by the deterministic cost
key `(term count, total degree, serialized length, label)`: it has 17 exact
terms and cleared total degree 6.  (The other degree-6/17-term tie has a
longer serialization.)

For each prime the script evaluates that exact source polynomial in the
complete squarefree degree-268 RUR quotient.  The residue is dense of degree
267, and extended gcd returns `1`; the exported dense degree-267 inverse
replays `residue * inverse = 1 mod eliminant`.  Per-factor residue, gcd,
inverse degree/support, and hashes are also frozen.  This is the appropriate
targeted modular certificate to compare with a future canonical char-zero
RUR; no new Groebner basis was computed.

## Controls and replay

- Negating the lexicographically first coefficient of literal
  `cofactor_1_3` changes its evaluated residue (must-fire).
- Omitting the five lower cofactors accepts all frozen components; restoring
  the full 22-row ledger rejects all of them (scope must-fire).
- Both checkers have identical logical result hashes under standard,
  optimized, and isolated/no-site Python; see `results_three_mode_replay.json`.

Run from the repository root:

```text
.venv/bin/python computations/unaudited-codex-k4-cycle-quadratic-mate-2026-08-21/audit_all_minor_components_literal_rows.py
.venv/bin/python computations/unaudited-codex-k4-cycle-quadratic-mate-2026-08-21/certify_cheapest_omitted_row_unit.py
```

## Stable artifacts

- `audit_all_minor_components_literal_rows.py` logical result
  `a7b8e6da0183042fe50bacc9c6a308659b32ab7800d5b4018d03697f9bef8fa3`
- `results_all_minor_components_literal_rows.json` file SHA256
  `9300fd93b7884a891eccefd066afed8564184f8c9b583a6c33154480159deebe`
- `certify_cheapest_omitted_row_unit.py` logical result
  `3379f0b177829a37cfa97c6e640bd8aa763afb1af1cda7432f180652fc5ec34b`
- `results_cheapest_omitted_row_unit.json` file SHA256
  `a9bc9149502e7b9333da07b7db3787c7be029996eb7fdbfa8d0fef6421fc4e0d`

`audit_quadratic_component_mates.py` is an abandoned setup draft from before
the source-scope defect was found; it is not a result and must not be used.
