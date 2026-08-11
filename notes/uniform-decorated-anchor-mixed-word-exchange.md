# A decorated anchor edge forces an avoiding source matching

## Result

Let `e=uv` belong to a selected pure-`k` target matching and suppose the
same physical block contains a nonzero off-diagonal cell

\[
                         q_e^{ij},\qquad i\ne j.       \tag{1}
\]

Use the full output word which is `i` at `u`, `j` at `v`, and `k` at every
other site.  Its exact mixed-zero coefficient partitions by whether the
matching uses `e`:

\[
                   0=q_e^{ij}C_e^k+R_e.              \tag{2}
\]

Here `C_e^k` is the **complete** pure-`k` two-hole cofactor, while every
matching in `R_e` avoids `e`.  This gives a source-valid dichotomy.

1. If `C_e^k!=0`, then the first term of (2) is nonzero, so `R_e!=0`.
   A nonzero literal matching in `R_e` avoids the decorated anchor edge.
   If no such term exists, (2) is already a localized source unit.
2. If `C_e^k=0`, expand the pure-`k` target coefficient, which equals one,
   at either endpoint of `e`.  The `e` summand vanishes, so some other
   nonzero edge/cofactor product exists.  It selects a pure-`k` matching
   avoiding `e` and repairs the deleted pure-anchor column at both ends.

Thus a decorated anchor cell can never remain an isolated correction.  It
forces a pure avoiding anchor matching, a mixed avoiding matching, or an
immediate unit.

Checker:
`computations/verify_uniform_decorated_anchor_mixed_word_exchange.py`.

## Exact aggregate proof

Every matching which uses `e` contributes the same factor `q_e^{ij}`.  The
remaining sites all have colour `k`, so their complete sum is exactly
`C_e^k`.  All other perfect matchings avoid `e`; their complete sum is
`R_e`.  This proves (2) without selecting one tail or assuming a support
torus.

In the dark branch, the pure target site recursion is

\[
 1=q_{uv}^{kk}C_e^k+
   \sum_{w\ne u,v}q_{uw}^{kk}C_{uw}^k.                \tag{3}
\]

The first term is zero.  Some remaining product is nonzero, and a nonzero
monomial of its cofactor completes it to the required pure matching.
Equations (2)--(3) are valid over an arbitrary integral domain.

The checker audits the disjoint partition of all perfect matchings through
ten sites.  For `4,6,8,10` sites the `(all,through e,avoiding e)` counts are

```text
(3,1,2), (15,3,12), (105,15,90), (945,105,840).
```

## Physical exit and rank bookkeeping

An avoiding mixed matching must send `u` and `v` to new partners.  Those
two endpoint cells have labels `(i,k)` and `(j,k)`.  Since `i!=j`, at least
one is off-diagonal.

* If such an endpoint pair lies outside the three selected pure-anchor
  matchings, their three colour columns survive at both deleted endpoints.
  The pair has ranks `(3,3)`, and the nonzero matching tail makes it a free
  source-active carrier in the pinned nonanchor route.
* If `k` equals `i` or `j`, the avoiding mixed matching also replaces the
  lost pure-`k` column at the corresponding endpoint.  This is an exact
  one-sided rank repair.
* If `k` is the third colour, both endpoint escapes are off-diagonal but
  neither replaces the missing pure-`k` column.  If both pairs remain in
  the anchor union, this is the precise wrong-colour rank-deficient web.

The last case is not hidden by the theorem.  It names the companion row
still required for a two-sided repair.

## Application to the Hall-triangle lock

The three-term lock theorem produces a nonzero `10` or `20` internal cell
with a nonzero pure-zero response tail.  If its physical edge is already
off the anchor union, it entered the nonanchor route immediately.  If it
is an anchor edge, apply the present theorem to every selected anchor
colour using that edge:

```text
cofactor dark      -> reselect that pure anchor away from the edge;
cofactor non-dark  -> full mixed row supplies an avoiding matching;
no avoiding term   -> localized source unit.
```

Therefore the entire decorated-anchor residual is reduced without adding
support cells one at a time.  The only surviving configuration has every
forced mixed escape still on the anchor union and has only one-sided or
third-colour rank repair.  The other complete response companions must
mate those endpoint labels; this is strictly smaller than an arbitrary
decorated-anchor web.

## Scope

This is a complete source-row exchange theorem, not a proof that the final
wrong-colour web is empty.  It deliberately preserves aggregate
cancellation: `C_e^k=0` is handled by pure-target reselection rather than
by selecting a nonzero cofactor term.

Run

```text
python3 computations/verify_uniform_decorated_anchor_mixed_word_exchange.py
python3 -O computations/verify_uniform_decorated_anchor_mixed_word_exchange.py
python3 -I -S computations/verify_uniform_decorated_anchor_mixed_word_exchange.py
```

Frozen ledger SHA-256:

```text
78afb82462ae3795cc502cbd794e0e5aa71e1b408eb7c207f13a3b0516a859a2
```
