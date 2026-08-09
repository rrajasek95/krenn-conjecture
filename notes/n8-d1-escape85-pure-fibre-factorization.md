# N=8 D1: pure-fibre factorization closes escape 85

The `191`-variable maximal support left open by the escape-`85` residue
classification is empty.  The certificate uses two equations and is valid
over every field; no parameter substitution, normalization, or Groebner
basis is needed.

Let the pure residue coefficient be

```text
R = x45_22*x67_22 + x46_22*x57_22 + x47_22*x56_22.
```

Residue purity gives

```text
q = R-1 = 0.                                           (1)
```

Now take the mixed full word

```text
(2,2,0,0,2,2,2,2).
```

On the exact escape-`85` support, every live matching for this word first
pairs `0` with `2` and `1` with `3`; the four residue sites can then use any
of their three perfect matchings.  Therefore full-output record `3464` is
exactly

```text
g = x02_20*x13_20*R = 0.                               (2)
```

Both boundary cells are localized nonzero.  More explicitly, the ordinary
polynomial identity

```text
g - x02_20*x13_20*q = x02_20*x13_20                  (3)
```

puts a localized monomial in the coefficient ideal.  Equations (1)--(2)
are thus inconsistent.  This closes the support independently of the
ten-parameter residue classification and in every characteristic.

## Complete factorization census

The same mechanism occurs twelve times:

- four mixed six-site words, two for each boundary pair, factor as one
  localized boundary cell times `R`;
- eight mixed full words
  `(2,2,j,k,2,2,2,2)` with `(j,k)!=(2,2)` factor as
  `x02_2j*x13_2k*R`.

The exact record indices are

```text
3464, 3484, 3504, 3878, 4018, 4038,
4058, 4432, 4572, 4592, 6612, 6632.
```

Each factorization independently combines with (1) to put its localized
degree-one or degree-two boundary monomial in the ideal.  The rational
residue point in the previous audit merely exposes these twelve records as
raw monomials; the proof checks the universal symbolic factorizations and
does not use that point.

## The 80-word pure-lift theorem

The reusable statement is not tied to the escape orientation.  For any
boundary colours `(i,j,k,l)` other than `(2,2,2,2)`, suppose
`x02_ik,x13_jl` are localized and every full matching except `{02,13}` plus
a residue perfect matching is support-dead.  With target colour `2` on the
residue, mixed full exactness is

```text
x02_ik*x13_jl*H_R(2222)=0,
```

whereas residue purity is `H_R(2222)=1`.  Hence the localized coefficient
ideal is empty.  This applies to all `3^4-1=80` mixed boundary words, in any
support and without choosing an escape orientation.

For the maximal escape support, the checker audits the complete `81`-word
universe (including the pure boundary word).  All `81` boundary products
are localized; exactly nine words have every competing full matching dead:

```text
(2,2,j,k),  j,k in {0,1,2}.
```

Eight are mixed and give the full-output certificates above; the ninth is
the pure word.  The closing orientation is `(i,j,k,l)=(2,2,0,0)`.

The checker
[`verify_n8_d1_escape85_pure_fibre_factorization.py`](../computations/verify_n8_d1_escape85_pure_fibre_factorization.py)
reconstructs the maximal support and all `7,029` generators, verifies the
twelve universal factorizations and ordinary monomial certificates, audits
the full `81`-word lift census, and independently confirms the twelve-record
specialization census.
