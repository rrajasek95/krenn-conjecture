# Degree-eight contraction module and pure-product scope audit

## Exact outcome

The compatible chart-26 pair `lambda7 <- lambda8` has a finite, exact
fixed-chart symmetry description, but it does **not** furnish an all-degree
transfer mechanism.  The 220 nonzero contractions of the new degree-eight
top layer are linearly independent and form a permutation module for the
order-four chart stabilizer `V4`.  They split into 61 coordinate orbits:
49 regular orbits of size four and 12 orbits of size two.  The permutation
character has traces

```text
[220, 8, 6, 10]
```

and hence one-dimensional character multiplicities

```text
(++,+-,-+,--) = (61,53,52,54).
```

The exact rank minor is `-2^-236`, and all `4*220=880` covariance checks
under the literal coordinate transforms pass.

## What the collision packet supplies

For a degree-six collision polynomial `R` and a top contraction
`C_x = x contraction lambda8`, the canonical inverse-system action is

```text
(R contraction C_x)(m) = lambda8(x*m*R).
```

Every right-hand side is a literal bounded degree-eight source column.
It is therefore zero for all 220 channels and every degree-one `m`.
Thus the known collision ideal annihilates this module by contraction.

This is not a nontrivial same-degree exchange law.  Contraction by `R`
maps degree seven to degree one, and the frozen 4-4/4-5 reductions contain
19 nonzero remainders among 22 representatives.  Two explicit guards are

```text
4-4: 0948cfed, 0948c7f4 -> 0951b4c7edf4
4-5: 0948c6f4, 0948c6d9e4 -> 0951acc6f4f4.
```

Reinterpreting these as internal exchange operators needs an additional
rehomogenizing lift/right inverse.  The degree-six theorem does not provide
one.  Accordingly the exact positive statement is only the finite `V4`
permutation module; there is no source-labelled `lambda9` prediction or
all-`k` recurrence.

## Actual pure-product pairing

Let `F` be the product of the three literal normalized pure coefficients.
Each factor has 105 terms with degree histogram

```text
degree 0: 1, degree 2: 12, degree 3: 32, degree 4: 60.
```

Exact target-specific multiplication gives

```text
                         F       F^2
lambda7                  1        1
lambda8                  1        1
new lambda8 top          0        0
nonzero new channels     0/220    0/220
```

These scalar values come solely from the constant monomial: neither `F`
nor `F^2` has a nonconstant monomial in the support of `lambda7` or
`lambda8`.  More sharply, none of the 16,092 distinct rows supporting the
220 new channels occurs in either pure product.

This is a no-go for using the displayed new directions as the missing pure
class.  Homogeneously, `F^h` has degree 12 and `(F^h)^2` degree 24, whereas
`lambda7`, `lambda8`, and the new channels have degrees 7, 8, and 7.
Same-degree pairing is unavailable, and contraction by either homogeneous
pure product is zero for degree reasons.  A target-relevant inverse-system
test must begin in degree at least 12 (or 24 for the square).

## Scope

The all-support normalization is the exact Laurent quotient for the mixed
ideal and pure-product nonvanishing.  This report does not additionally
impose the literal equations `H_c=1`.  Conversely, the `t=1` scalar
pairings above are truncated controls, not homogeneous saturation
certificates.

## Reproduction

```sh
python3 computations/unaudited-codex-n8-degree8-exchange-module-2026-08-23/audit_exchange_module.py --check-results
python3 computations/unaudited-codex-n8-degree8-exchange-module-2026-08-23/audit_pure_product_pairings.py --check-results
python3 -O computations/unaudited-codex-n8-degree8-exchange-module-2026-08-23/audit_exchange_module.py --check-results
python3 -I -S computations/unaudited-codex-n8-degree8-exchange-module-2026-08-23/audit_pure_product_pairings.py --check-results
```

Both checkers also have hostile mutation modes, `--mutate`, which must fail.

Frozen result digests:

```text
exchange logical: e0cb7e9a8ba4a3523ddf5c367b26b54853a31955d3cd4c97246075f6f7526b40
pure logical:     6f8723a57e923958915a3dd2e2781d0424dff7c6bf420627574d9d82eb0d45f3
collision ledger:e8384cac6824cb6a46c2f93f4cab8fbca100f76bba510699b058256ffc4d7fea
```
