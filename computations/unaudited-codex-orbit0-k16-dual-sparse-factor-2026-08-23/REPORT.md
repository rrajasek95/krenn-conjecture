# Sparse factorization of the 23-row K16 dual

## Result

After removing its exact monomial gcd, the full 23-term signed polynomial is
irreducible over `Q`.  The separate 15-term genuinely-new residual is also
irreducible over `Q`.  Therefore neither hides a binomial, Pluecker,
Pfaffian, or other lower-degree polynomial factor.

The exact interfaces are:

| polynomial | monomial gcd | gcd degree | primitive degree | terms | variables |
|---|---|---:|---:|---:|---:|
| full dual | `084c757d7dcefb` | 7 | 17 | 23 | 41 |
| new residual | `084c757d7dcecef3f7fbfb` | 11 | 13 | 15 | 33 |

Singular 4.4.1 exact factorization over `Q`, `F_1009`, and `F_1013`
returns only a unit and the original primitive polynomial, both with exponent
one.  Since the coefficients are primitive `+/-1` and degree is preserved
modulo either prime, finite-field irreducibility plus Gauss's lemma proves
irreducibility over `Q`.  A hostile positive control multiplies each input by
`x00+x01`; the same parser then returns nonconstant factors of degrees
`1+17` and `1+13`, respectively.

## Port-cycle census

Every one of the 23 monomials is exactly a balanced 2-regular graph on the 24
site-colour ports.  Its cycle-partition histogram is:

```text
9+7+2+2+2+2    1
9+9+2+2+2      1
12+4+2+2+2+2   1
13+3+2+2+2+2   1
14+2+2+2+2+2   1
14+4+2+2+2     3
15+3+2+2+2     1
16+2+2+2+2     5
18+2+2+2       6
18+4+2         1
20+2+2         2
```

Thus the sparse relation spans eleven cycle types, including odd port cycles;
it is not supported on one matching-exchange/Pfaffian cycle shape.  The JSON
ledger gives the literal partition for every signed row.

## Scope and replay

This proves only factor irreducibility of the two frozen sparse polynomials;
it says nothing about primality of a source ideal and performs no next-page
incidence expansion.

```text
python3 computations/unaudited-codex-orbit0-k16-dual-sparse-factor-2026-08-23/audit_k16_dual_sparse_factor.py
python3 -O computations/unaudited-codex-orbit0-k16-dual-sparse-factor-2026-08-23/audit_k16_dual_sparse_factor.py
python3 -I -S computations/unaudited-codex-orbit0-k16-dual-sparse-factor-2026-08-23/audit_k16_dual_sparse_factor.py
```

All modes pass; `--mutate` deletes one cell from a row and must fail the frozen
homogeneity/2-regular interface.  Logical digest:
`1080f3886801d39ec6a62e87daf5a75b086eb6701f536988fb232bb7cabaf6fd`.

