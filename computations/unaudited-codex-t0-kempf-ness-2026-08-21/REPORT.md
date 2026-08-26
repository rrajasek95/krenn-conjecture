# T0 Kempf--Ness balance and mixed-norm coercivity audit

Status: **exact orbit theorem; sharpened coercivity remains open**.  Every
hypothetical exact source can be moved in its T0 orbit closure to a balanced
source, but pure normalization plus balance is neither compact nor
norm-coercive.  The known Laurent GHZ escape does become bounded after
balancing and its mixed norm jumps from `2t^2` to `2`; it is not a balanced
`P_mixed -> 0` counterfamily.

## 1. Exact torus criterion

For the normalization-preserving torus

```text
T0 = {(lambda_i,c): product_i lambda_i,c=1 for c=0,1,2},
```

the restricted weight of `A_ij^(a,b)` is
`e_(i,a)+e_(j,b)`.  Standard affine torus Kempf--Ness gives:

- `T0.A` is closed iff zero lies in the relative interior of the convex hull
  of its live restricted weights;
- a closed orbit contains a moment-map-zero point, unique modulo the compact
  torus and the point stabilizer;
- in coordinates, moment zero is exactly

```text
d_i,c = sum_(j,b) |A_ij^(c,b)|^2
```

being independent of `i` for each fixed colour `c`.

If `H_c=1`, at least one colour-c perfect-matching monomial is live.  Its four
weights sum to the pure character, which restricts to zero on T0.  Therefore
pure normalization puts zero in the support polytope and makes the point
semistable.  It does **not** put zero in the relative interior after other
support weights are included, so it does not by itself make the original
orbit closed.  Its closure nevertheless has a unique closed orbit, and the
pure invariants remain one there.  Thus any hypothetical exact source admits
a balanced exact degeneration.

For a fixed full-support orbit the archived rational Farkas certificate says
the support weights span all 21 dimensions and zero is interior.  The real
torus norm is then strictly coercive modulo the finite stabilizer.  This is an
orbitwise result, not compactness across different quotient points.

## 2. Balanced unbounded pure-normalized family

Put unit diagonal cells `E_cc` on the common matching
`01|23|45|67`.  On every one of the 28 edges put value `t` in each of the six
offdiagonal colour cells `a!=b`, and put all other diagonal cells to zero.
Then, exactly,

```text
H_0=H_1=H_2=1,
d_i,c=1+14t^2 for all i,c,
||A(t)||^2=12+168t^2.
```

The 180 support weights have rank 21.  Because the squared cell magnitudes
give a strictly positive zero combination of every live weight, zero is in
the interior of the support polytope.  Every `t!=0` point is already balanced
and has a closed orbit with finite stabilizer.  These are genuinely different
quotient points: their balanced norms differ and tend to infinity.

The exact mixed squared norm is

```text
P(t) = 78 + 1944t^2 + 3744t^3 + 35856t^4
      + 115200t^5 + 585792t^6 + 1555200t^7 + 3991680t^8.
```

Thus balance plus pure normalization is noncompact and noncoercive in source
norm.  This family does not defeat the sharpened mixed-norm proposal: its
mixed norm grows, and it is not on the no-cap/X5 locus.

## 3. The Laurent arc balances to a bounded point

For the archived 12-cell arc, the three diagonal matchings and valuations are

```text
M0: 12:-1, 36:+1, 45:0, 78:0,
M1: 14:0, 27:0, 35:0, 68:0,
M2: 18:0, 25:0, 34:0, 67:0.
```

On each matching edge `ij` of colour `c`, assign both endpoints the T0
exponent

```text
x_i,c=x_j,c=-v_ij,c/2.
```

For each colour, `sum_i x_i,c=-sum_(ij in Mc)v_ij,c=0`, so this is a literal
T0 one-parameter gauge.  Every transformed cell has valuation zero.  The
balanced representative therefore has

```text
||A_bal||^2=12,
P_mixed(A_bal)=2,
```

because the support has precisely two mixed matching monomials and both now
have unit magnitude.  Before balancing, `P_mixed=2t^2` tends to zero.

This also emphasizes that `P_mixed` is invariant under the compact torus but
not under the complex T0 action.  The known escape to infinity is removed by
Kempf--Ness balance and supplies no balanced small-P sequence.

## 4. Controls

- The exact K4 GHZ witness is balanced with norm squared 6.  Its support
  weight rank is 3 inside a 9-dimensional T0, so it has a 6-dimensional
  stabilizer.  It is the expected closed-orbit positive control.
- W40 has raw support/rank `20/12`, norm squared 20, and `P_mixed=3`; its raw
  port energies are not balanced.
- W25 has raw support/rank `38/20`, norm squared `356765/2304`, and
  `P_mixed=70873613/2304`; its raw port energies are not balanced.
- A unit colour-zero source on `C3 disjoint_union C5` is balanced, has support
  weight rank 7, and lies in the top base locus because neither odd component
  has a perfect matching.  Thus moment-zero base-locus directions genuinely
  exist.

## 5. Exact remaining properness target

Let `A_k` be balanced and pure-normalized, let
`R_k=||A_k|| -> infinity`, and suppose `P_mixed(A_k)->0`.  After a subsequence,
`B_k=A_k/R_k` converges to a nonzero `B_0`.  Homogeneity gives

```text
H(B_k)=H(A_k)/R_k^4 -> 0,
```

so `B_0` is a nonzero moment-zero point of the top base locus.  Its leading
support has these necessary properties:

- every active colour has equal positive leading port energy at all sites;
- the live weights admit a positive zero relation;
- every top word has no leading perfect-matching term or at least two terms
  which cancel; a singleton leading fibre is impossible.

The `C3 disjoint_union C5` control shows those conditions alone do not empty
the boundary.  What must be excluded is a **GHZ-accessible higher jet** over
this balanced base locus: the first nonzero top coefficient must give the
three normalized pure words while every mixed coefficient has strictly
higher order.

The no-cap condition creates one more load-bearing guard.  It is T0-invariant
at every finite point, but the archived rank-drop curve proves it is not
closed.  A boundary argument must carry the valuation of a nonzero response
pivot and its blocker membership into the initial Luna/Rees data.  Merely
requiring the limiting support to be no-cap is unsound.

Accordingly, no uniform positive lower bound for `P_mixed` on the balanced
pure no-cap slice is proved here, and no balanced no-cap `P_mixed->0`
counterfamily was found.  The precise next target is a Luna-slice or
second-variation exclusion of balanced GHZ-accessible jets, stratified by
the 728 carrier pivot ranks.

## Replay

```sh
python3 computations/unaudited-codex-t0-kempf-ness-2026-08-21/audit_t0_kempf_ness.py --write-results
python3 -O computations/unaudited-codex-t0-kempf-ness-2026-08-21/audit_t0_kempf_ness.py
python3 -I -S computations/unaudited-codex-t0-kempf-ness-2026-08-21/audit_t0_kempf_ness.py
```

Frozen logical digest:
`846cb61b4be9a83990f13c1742f82de05d71b0dcbe2798987d3d3ea05c60b619`.
