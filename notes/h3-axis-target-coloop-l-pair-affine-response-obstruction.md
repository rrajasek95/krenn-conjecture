# The final two L-edge sums synchronize only to a rank-one affine block

## Result

The last sixteen slots of the target-coloop rainbow audit are, up to the
residual-site mirror, the literal top row

```text
output word: 00112200,
matching:    PS:00 | 05:02 | 14:02 | 23:11.
```

The two off-diagonal cells lie on the two `q`-tail edges of the selected
pure-one response matching

```text
L = 05 | 14 | P2 | S3.
```

Their complete decorated-edge avoiding aggregates are source-valid, and
they do have a common companion.  That companion leaves one exact
rank-one affine block rather than a unit or a four-good wedge.

Checker:
`computations/verify_h3_axis_target_coloop_l_pair_affine_response_obstruction.py`.

## The two complete avoiding rows

For `e=05`, use the full word

```text
01111211.
```

For `f=14`, use

```text
10112111.
```

(The mirror records give the corresponding site-swapped words.)  In each
case the complete hafnian partitions as

```text
0 = q_e^02 C_e^1 + R_e,
```

with `15` physical matchings through the named edge and `90` avoiding it.
The selected matching `L` supplies a literal nonzero term in the through
part: its other three factors are the pure-one `L` cofactor.  Hence the
pinned decorated-edge theorem applies separately to both edges: a dark
cofactor reselects the pure-one target away from the edge, while a non-dark
cofactor forces a nonzero avoiding aggregate.

These two rows live in different fine words, so they do not cancel each
other directly.

## The common `p1s1` companion

Both `02` cells occur together with the selected `P2:11,S3:11` endpoint
cells in the literal response word

```text
00112211.
```

The selected term is the physical matching `L`.  Across the four symmetry
records, its `356` alternate direct-free matching slots split exactly as

```text
external endpoint:        312,
external off-diagonal q:   32,
internal affine block:     12.
```

The external slots enter the already pinned routes.  There are exactly
three internal matching types per record:

```text
L ports + diagonal q tail 01|45,
M ports + diagonal q tail 23|45,
the physical M skeleton itself.
```

Thus the original two avoiding sums have been synchronized to a four-term
port/tail block; no support family remains hidden.

## Exact E2 cofactor and the type obstruction

On the `L`-port sector, the response coefficient factors through the
four-hole common-`q` cofactor

```text
C23 = x01^00*x45^22
    + x04^02*x15^02
    + x05^02*x14^02.
```

The last term is the selected two-`L`-edge product.  The middle term has two
external off-diagonal edges and routes.  The first term is the sole
diagonal affine return.

The same `L` ports also support the `R12` companion because `S3:21` was
selected by the first endpoint hybrid.  However both `R11` and `R12` have
the same `p1` head.  The opposite `R21` face on this cofactor would require
the literal endpoint component

```text
P2:21,
```

which is absent from the exact carrier.  Therefore any common covector in
the proved `R11,R12` span remains rank one at `P`; it cannot supply the
opposite crossed minor needed by the five-lock wedge theorem.

This is the first exact type obstruction.  It does not assert that a full
source cannot add `P2:21`; if it does, that is precisely the new
opposite-colour companion to analyze.  Without it, the diagonal term
`x01^00*x45^22` is a genuine affine target-line return rather than a source
unit.

## Scope

This theorem consumes the two separate decorated-edge avoiding sums and
reduces them to one literal coefficient block.  It applies the existing
nonanchor, decorated-edge, and five-lock hypotheses exactly; it does not
declare the rank-one block empty.  The remaining proof obligation is now
one typed statement:

> force `P2:21`, delete it by a joint-kernel/target-line modification, or
> show that the two `M`-port internal terms give a source unit.

No larger matching or support census is needed to state that obligation.

Run

```text
python3 computations/verify_h3_axis_target_coloop_l_pair_affine_response_obstruction.py
python3 -O computations/verify_h3_axis_target_coloop_l_pair_affine_response_obstruction.py
python3 -I -S computations/verify_h3_axis_target_coloop_l_pair_affine_response_obstruction.py
```

Frozen ledger SHA-256:

```text
fb44fd739a4a334be410ffe12b578d1cebc175abafb6ef65aade7ffd9c8088d3
```
