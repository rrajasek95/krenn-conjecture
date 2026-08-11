# The dark Hall coloop reduces to an even alternating path

## Result

Let `M0` be a selected pure-zero residual matching containing the unary
escape `a-d`, and let `M2` be the selected pure-two near-matching with holes
`b,c`.  The two-coloured multigraph `M0 union M2` has one alternating path
from `b` to `c` and disjoint even alternating cycles.

This gives a complete source-labelled response split.

* If `a-d` lies on a cycle, switch that whole component from `M2` to `M0`.
  The result is a perfect matching on `U-{b,c}` containing `a-d`.  With the
  selected `p2(b)s2(c)` stars it is a nonzero mixed diagonal-`22` term, so
  the complete zero row forces a cancellation mate or a localized unit.
* If `a-d` lies on the `b-c` path, number its vertices from `b`.  Deleting
  `a,b` leaves two even path pieces exactly when the position of `a` is
  odd.  In that case the alternating pieces give a nonzero crossed-`21`
  term after attaching `p2(b)s1(a)`, and again the complete zero row forces
  a mate.
* The first companion-blind topology is therefore `a-d` on the path with
  `a` at even distance from `b`.

The same statement holds after interchanging the two colours/endpoints.
The proof is the elementary alternating-component decomposition, not a
finite support census.  The checker audits the parity assertion on all
matching pairs through eight residual sites.

Checker:
`computations/verify_uniform_hall_bridge_dark_alternating_path_boundary.py`.

## The first dual-blind web

At six residual sites the two path parities can be blind simultaneously.
A canonical physical skeleton is

```text
M0 = 03 | 14 | 25,
M1 = 24 | 35,
M2 = 15 | 34.
```

The first anchor-contained mates of its mixed diagonal debts are

```text
24:02, 35:20        on the pure-one anchor edges,
15:01, 34:10        on the pure-two anchor edges.
```

Choose signs so that they cancel the original `11:110220` and `22:202101`
terms.  Literal expansion of the **complete** unary and response rows does
not produce a guard.  It produces

```text
four unary singleton rows:
  000021, 001011, 020022, 021012;

six diagonal-response singleton rows:
  11: 110100, 110121, 111210,
  22: 202200, 202221, 222102.
```

Every response singleton has exactly one of the four displayed decorations
as its unique non-pure anchor cell.  Each decoration uses the two colours
different from its anchor colour.  Thus all four are source-active, but
none repairs the lost pure-anchor row at either endpoint.

## Consuming the six rows without another support layer

Use the complete mixed-word exchange of
`uniform-decorated-anchor-mixed-word-exchange.md`, with the non-pure-label
extension in `uniform-triple-shared-anchor-unary-escape.md`, on a selected
pure-`k` physical edge
`e`.  It applies to every decoration `(i,j)!=(k,k)`, including a wrong
diagonal decoration:

\[
                    0=q_e^{ij}C_e^k+R_e.             \tag{1}
\]

Here `C_e^k` is the complete pure-`k` two-hole cofactor and every matching
in `R_e` avoids `e`.

* If `C_e^k=0`, pure-target site recursion reselects a nonzero pure-`k`
  matching avoiding `e`, repairing the missing `k` column at both ends.
* If `C_e^k!=0`, (1) forces a nonzero avoiding mixed matching (or gives a
  localized unit).
* Any endpoint escape of that matching outside the selected anchor union
  is a nonanchor source-active good pair.

Therefore the six rows reduce the paired web to a precise incidence
boundary: every avoiding matching stays on the anchor union, and its two
endpoint labels are both different from `k`.  Such a third-colour escape
repairs neither deleted `k` column.  The next needed source coupling is an
opposite companion which supplies one `k`-labelled endpoint, or a dependence
among the same-star lock columns giving an anchor-safe deletion.  It is not
another unrestricted support layer.

## Scope

This is a uniform alternating-path reduction and a coefficient-complete
audit of the first paired web.  The displayed web is not a full one-bad
point: its four unary and six response singletons explicitly show why.  The
theorem consumes those singleton rows into pure reselection, an avoiding
matching, or a unit, but deliberately retains the anchor-contained
third-colour rank boundary.

Run

```text
python3 computations/verify_uniform_hall_bridge_dark_alternating_path_boundary.py
python3 -O computations/verify_uniform_hall_bridge_dark_alternating_path_boundary.py
python3 -I -S computations/verify_uniform_hall_bridge_dark_alternating_path_boundary.py
```

Frozen ledger SHA-256:

```text
13f4c57cd3f07095db65cde5233bfda870c8be3c6c3ae7da6b5b8d242b366ab9
```
