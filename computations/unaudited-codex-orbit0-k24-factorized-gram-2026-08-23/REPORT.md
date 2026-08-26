# Factorized H-invariant K24 Gram interface

## Verdict: the proposed 1,757-square Gram is not a source matrix

The number 1,757 is the H-orbit count of the 569,736 anchor-free **decorated
matching terms** `(w,M)`.  A literal degree-24 source column is instead
`(w,U)`, where U is a 20-cell multiplier.  The decoration does not determine
U, its row support, or its column orbit.

This distinction is already numerically load-bearing.  Fix

```text
w = 01010101,
M = the w-coloured term on 01|23|45|67.
```

M is anchor-free.  For every anchor-free perfect matching P of the remaining
16 ports, the multiplier

```text
U = 2P - M
```

(with the four fixed M edges included in P) gives a distinct literal column
`(w,U)` and a doubled-matching K24 output.  A 1,596-state exact matching DP
counts 890,713 such columns.  Since an H-orbit has size at most 384, this
single fixed decoration meets at least 2,320 H-column orbits.  Therefore a
1,757 by 1,757 matrix necessarily identifies distinct source columns and
cannot decide terminal membership.

No modular rank was run on that matrix.  A rank result for it would not be a
rank result for the literal mixed ideal.

## Exact multiplier-aware Gram

For a literal column `C=(w,U)`, write

```text
top(C) = sum_(M anchor-free term of H_w) [U+M].
```

For two literal columns, their Gram entry is the finite convolution

```text
<top(w,U), top(w',U')>
  = #{(M,M') : M-M' = U'-U},
```

where M and M' range over the anchor-free terms of their literal word rows.
Thus each word-pair kernel costs at most `105^2=11,025` matching-pair tests
and can be cached by `(w,w',U'-U)`.  For the fixed word above, all 105 terms
are top terms; its self-kernel has exactly 10,081 difference keys with
coefficient histogram

```text
1: 9,660 keys; 3: 420 keys; 105: 1 key.
```

For H-invariant calculation, use the unnormalised orbit-sum column

```text
v_[C] = sum_(c in Orb_H(C)) top(c).
```

Store `v_[C]` as its total mass `m_C(r)` on every H-row orbit `r`.  If `|r|`
is that orbit size, then the exact rational formulas are

```text
G_[C],[D] = sum_r m_C(r)m_D(r)/|r|,
b_[C]     = sum_r m_C(r)m_R(r)/|r|,
||R||^2   = sum_r m_R(r)^2/|r|.
```

The provider checks divisibility of each orbit mass by `|r|`.  On the frozen
sample, the column orbit has size 384, its orbit vector has 105 row-orbit
coordinates, and its exact self-Gram is 40,320.

Over Q these Gram matrices may be regarded over R with the ordinary positive
inner product.  Hence, for a **complete Gram-connected column component**, an
H-invariant target R belongs to its column span iff adjoining R does not
increase Gram rank.  Equivalently, after solving `Gx=b`, one must also verify
`||R||^2=b^T x`; normal-equation solvability alone is automatic and is not a
membership test.

## Restartable exact interface

`k24_factorized_gram_provider.py` supplies:

- exact K24 output rows of `(w,U)`;
- H-canonical column and row orbits;
- sparse orbit-sum vectors and exact Gram/target pairings;
- every H-column orbit sharing an output with a given column; and
- a restartable JSON closure of the target-rooted Gram component.

For a representative column, it is enough to inverse-expand the at most 105
outputs of that representative: H-transports produce the same canonical
neighbour orbits.  This avoids ambient row enumeration.  Per orbit vector the
raw emission bound is `384*105=40,320` top terms, followed by H-row
canonicalization.  A Gram entry is then a sparse merge on common row-orbit
coordinates.

The validation seed

```text
01010303101047477676a3a3aaaac7c7e2e2f2f2f4f4f9f9
```

starts with four incident H-column orbits.  Processing only the first orbit
already discovers 1,032 column orbits, so the cap-50 run terminalizes
`COLUMN_CAP` with 1 processed and 1,031 queued.  This is a valid resumable
size result, not a rank or nonmembership claim.

## Source-faithful terminal criterion

Once K19--K23 produce a frozen H-invariant residual R24:

1. seed the provider with every literal column incident to `supp(R24)`;
2. close every reached H-column Gram component;
3. accumulate the factored R24 orbit masses only on those components;
4. build the sparse exact/modular orbit Gram and augmented target Gram; and
5. replay any rank equality or separator over Q.

`COMPLETE` is load-bearing.  A capped component gives no membership verdict.
The 1,757 decoration orbits remain useful as local convolution-kernel cache
types, but never as the global column index.

## Replay

Run `audit_k24_factorized_gram.py`.  It pins the terminal-structure packet,
replays the fixed-decoration lower bound, the exact convolution kernel, and a
literal H-orbit vector/Gram entry.  The restartable closure checkpoint is
`checkpoint_sample_k24_column_closure.json`.
