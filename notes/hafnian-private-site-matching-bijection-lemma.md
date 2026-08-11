# Private-site matching bijection and the first determinant obstruction

Date: 2026-08-11

Checker:
`computations/verify_hafnian_private_site_matching_bijection_lemma.py`

## The support-independent identity

Let two full words differ only at one physical site `v`.  Write `p_s` and
`q_s` for the two source-labelled entries on edge `vs`, and let `C_s` be the
common hafnian cofactor after deleting `v,s`.  Hafnian recursion at `v` gives

```text
H_pure  = sum_s p_s C_s,
H_mixed = sum_s q_s C_s.
```

Fix a reference partner `u`.  Then, over every commutative ring,

```text
p_u H_mixed - q_u H_pure
  = sum_{s != u,v} (p_u q_s - q_u p_s) C_s.                 (1)
```

If the first word is a pure target and the second is mixed, their source
generators are `G_pure=H_pure-1` and `G_mixed=H_mixed`, so

```text
p_u G_mixed - q_u G_pure
  = q_u + sum_{s != u,v} (p_u q_s - q_u p_s) C_s.          (2)
```

Thus the exact common-tail condition is

```text
sum_s Delta_s C_s = 0,  Delta_s=p_u q_s-q_u p_s.           (3)
```

This is more precise than requiring a unique matching.  A sufficient
matching-bijection hypothesis is that `uv` is a coloop in both word fibres:
every supported matching uses `uv`.  Equivalently, every alternate cofactor
`C_s` vanishes.  More generally, the unit still survives if every active
alternate route has proportional incident labels `Delta_s=0`, or if the sum
in (3) cancels for a separately certified source reason.

The checker expands (1) symbolically for `N=2,4,6,8,10`.  The proof for all
even `N` is the displayed recursion itself: matchings are partitioned by the
partner of `v`, and the `s=u` summand cancels identically.

## Matching and alternating-cycle interpretation

Under the coloop hypothesis, deleting `uv` is a weight-preserving bijection
between the pure and mixed matching sets.  The two tails therefore differ
only by `p_u` versus `q_u`.

The first failure occurs when a matching sends `v` to an alternate partner
`s`.  Comparing it to a private matching, the symmetric difference contains
an even alternating cycle through `v`.  On the minimal cycle `v-s-t-u-v` the
uncancelled term is exactly

```text
(p_u q_s - q_u p_s) x_ut.                                  (4)
```

Equation (4) is the first source-labelled determinant obstruction.  Longer
alternating cycles merely multiply or sum this determinant against the
appropriate common cofactor `C_s`; they do not introduce a new local
invariant.

## Consequence for the same-hole common-q branch

For each of the three packets from `9a81c82`, retain its carrier/outer cells
and allow an arbitrary subset of all 90 decorated cells on the five common
sites, with arbitrary coefficients.  On the maximal support the two words

```text
00000000, 00000001
```

have exactly the same three matchings:

```text
01|27|34|56,
03|14|27|56,
04|13|27|56.
```

Every matching contains the private edge `27`.  Common-q additions are all
internal to sites `0,...,4`, so they can neither change the incident labels at
site 7 nor create an alternate partner there.  Any smaller common-q support
selects the same subset of these three matchings in both words.  Therefore
the termwise bijection, and hence the original identity,

```text
ra G_mixed - rc G_pure = rc,
```

holds on every support in the three cubes.  With the fixed normalization
`ra=1, rc=-2`, this remains the ordinary unit

```text
1 = (-1/2) G_mixed - G_pure.
```

The covered optional-support cubes have dimensions `83,83,81`, respectively.
This replaces the one-cell and six two-cell cardinality checks by one exact
all-support theorem for arbitrary common-q additions.

## Scope

The theorem permits arbitrary support and coefficients away from the changed
private site.  It does not declare arbitrary new cells incident to site 7
harmless.  Such a cell creates an alternate route and must satisfy the
determinant/cofactor condition (3); the alternating-C4 calculation shows this
hypothesis is sharp.
