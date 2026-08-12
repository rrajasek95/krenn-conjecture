# The singular weighted arcs have complete derived Hasse companions

## Universal companion

Let `H_A(tau)` be the four `u/t` Hasse coefficients of the shifted source
cycle, with `h=H_ut`, and write

```text
H_A(tau)=sum_i H_A,i tau^i.
```

In normal jet order `k`, introduce normal-indexed copies of the existing
source generators.  The complete chain is

```text
C_k = sum_(i=0)^k sum_A H_A,i r0[A,k-i]
      - F0 rm[k] - sum_(i=0)^k h_i T[k-i].             (1)
```

The principal-parts differential of the normal-indexed mixed row is

```text
d rm[k] = sum_(i=0)^k sum_A H_A,i Eq[A,k-i].           (2)
```

Equations (1)--(2) give, exactly,

```text
d C_k = sum_(i=0)^k h_i Yw[k-i],
tgt(C_k)=ores(C_k)=0,
chart(C_k)=-sum_(i=0)^k h_i S[k-i].                   (3)
```

The checker verifies (3) in a formal integral polynomial ring, with all
four `u/t` faces retained.  Orders one, two, and three contain respectively
11, 16, and 21 labelled source components.  The order-one instance is the
complete normal Hasse face constructed concretely in `827e329`; (1) is its
uniform principal-parts continuation.

## Assembly on every singular stratum

For each weighted arc of `d354257`, take `C_k` at its first new order `k`.
Every lower coefficient `h_i`, `i<k`, lies in the span of the already
normalized columns.  Subtract the corresponding earlier chain shifted by
normal grade `k-i`.  By (3), this simultaneously cancels its `Yw` boundary
and chart terminal, without introducing target or ordinary residue.

The remaining grade-zero boundary is precisely the new weighted face
column.  Exact Gaussian elimination yields the following complete bases:

```text
zero                       2,2,2,2,2
one edge                   1,1,1,3,3
two-star                   1,1,1,2,2
three-star                 1,1,1,1,3
triangle                   1,1,1,2,2
four-star                  1,1,1,1,2
cyclotomic isolated K4     1,1,1,1,2
```

For every row the derived boundary rank is five, target rank is zero, old
ordinary-residue rank is zero, and the normalized chart terminal is the
negative face basis.  Thus no further derived normal separator survives on
the singular strata.

## The first physical defect

This positive result is in the complete **derived principal-parts**
resolution.  It does not silently create a physical source cell.

The new component in (1) is the normal-indexed mixed row `rm[k]`.  A normal
index may repeat; a literal physical squarefree Hasse face cannot repeat a
site.  The exhaustive comparison audit pinned here proves that the first
homogeneous physical degree capable of changing this class is a repeated
site `P3 disjoint K2` collision.  An individual multiplied response route
there has a private ordinary-residue companion.  Only an adjacent two-face
S-pair cancels it, and that S-pair has physical anchor incidence zero.

Consequently the exact remaining cells are unchanged but now sharply
localized:

1. the zero-anchor site-collision cell `E_v` carrying that adjacent S-pair;
2. the separate primitive anchor cell; and
3. the comparison identifying derived `Yw` with physical cap `W`.

The second/third weighted-normal companions themselves exist and preserve
target/residue.  Their first failure is the physical comparison functor,
not a missing derived Hasse coefficient.

## Scope and verification

This is an exact source-chain theorem in the normal principal-parts
totalization.  It neither constructs the physical site-collision cells nor
identifies the physical cap.

```text
python3 computations/verify_h3_component_iv_weighted_normal_hasse_companions.py
python3 -O computations/verify_h3_component_iv_weighted_normal_hasse_companions.py
python3 -I -S computations/verify_h3_component_iv_weighted_normal_hasse_companions.py
```

Frozen ledger SHA-256:

```text
9b16481cf106fb836b4720ec83eb2d61b705eef4449ad3340f815a3afd096283
```
