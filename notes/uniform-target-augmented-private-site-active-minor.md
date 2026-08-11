# Target augmentation forces every off-diagonal endpoint cell active

Date: 2026-08-11

Checker:
`computations/verify_uniform_target_augmented_private_site_active_minor.py`

## The all-order identity

Fix a site `v`, a pure target colour `a`, and a different colour `b`.  Let
the pure word be `a...a`, and let the mixed companion change only site `v`
to `b`.  On the edge from `v` to `s`, write

```text
p_s = A_vs[a,a],       q_s = A_vs[b,a],
```

and let `C_s` be the coefficient of the all-`a` word in the common hafnian
cofactor after deleting `v,s`.  Hafnian recursion gives

\[
 H_{\rm pure}=\sum_s p_sC_s,
 \qquad H_{\rm mixed}=\sum_s q_sC_s.
\]

For a reference neighbour `u`, put

\[
             \Delta_{us}=p_uq_s-q_up_s.
\]

Because the source equations are

\[
 G_{\rm pure}=H_{\rm pure}-1=0,
 \qquad G_{\rm mixed}=H_{\rm mixed}=0,
\]

the target-augmented private-site identity is

\[
 p_uG_{\rm mixed}-q_uG_{\rm pure}
   =q_u+\sum_{s\ne u,v}\Delta_{us}C_s.                 \tag{1}
\]

Thus every exact source satisfies

\[
             \boxed{\sum_{s\ne u,v}\Delta_{us}C_s=-q_u.} \tag{2}
\]

If the off-diagonal cell

\[
                         q_u=A_{vu}[b,a]
\]

is nonzero, (2) says that at least one literal
`Delta_us*C_s` is nonzero.  Equivalently, after localizing `q_u`, the source
rows together with the equations `Delta_us*C_s=0` generate the unit ideal.
No support minimality is required.

The checker expands (1) over `Q` at orders `N=2,4,6,8,10`.  The proof for
all even orders is the displayed recursion, so this is not a finite-order
inference.

## Exact ternary consequence

There are six ordered off-diagonal endpoint cell types `(b,a)`, `b!=a`.
Each is the reference cell of exactly one pure-`a`/mixed-`b` comparison.
Therefore, at every site and on the direct edge as well as every star edge,

```text
some off-diagonal cell A_vu[b,a] is nonzero
    => an active determinant/cofactor product exists.
```

If this alternative never occurs, every incident row is axis-purified:
row `a` is supported only in neighbour colour `a`.

This is the source-valid endpoint/direct dichotomy that the homogeneous
formula alone misses.  It uses both literal target rows: the constant term
in the pure equation is exactly what produces `q_u` on the right of (1).

## Why the previous guard does not contradict it

The packet from `fb8d482` has endpoint cells

```text
P:  P0:11, P5:11, P2:22,
Q:  Q1:11, Q3:22.
```

They are all diagonal.  Its three rank-two minors compare `(1,1)` and
`(2,2)` ports, so the neighbour colours differ.  Such a pair cannot occur
in one private-site identity: two full words differing only at `v` have the
same colour at every neighbour.  Those cross-colour rank minors are
therefore untyped, not counterexamples to (2).

This explains the earlier `0/6` compatible-cofactor census exactly.  The
packet also lacks the unary target `q^[3]=X0`, but the more immediate typing
issue is that it contains no off-diagonal reference cell.

## What remains

Equation (2) closes the cofactor-invisible **off-diagonal** deformation.  It
does not yet prove either of the two stronger downstream statements:

1. an active determinant/cofactor product need not by itself furnish the
   rank-three deleted stars and nonflatness required by the curved OO theorem;
2. an axis-purified row may remain supported at several physical sites, so
   its square need not vanish and the permanent-null cap need not yet be
   clean.

The remaining theorem is consequently narrower than “remove every invisible
minor.”  It is the axis-purified carrier-exchange/concentration statement:
use common-`q` provenance and minimum support to concentrate each diagonal
row, or route its nonzero self-square to an already certified curved/clean
packet.  Cross-colour diagonal rank minors should not be fed back into (1),
because they do not have a common residual word.

## Reproduction

```sh
python3 computations/verify_uniform_target_augmented_private_site_active_minor.py
python3 -O computations/verify_uniform_target_augmented_private_site_active_minor.py
python3 -I -S computations/verify_uniform_target_augmented_private_site_active_minor.py
```
