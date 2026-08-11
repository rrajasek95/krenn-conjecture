# Nonanchor off-diagonal cells reselect to a good pair

Date: 2026-08-11

Checker:
`computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py`

## Uniform lemma

Choose one nonzero perfect-matching monomial in each of the three pure target
coefficients of an exact ternary source.  Denote the physical matchings by

\[
                         Q_0,Q_1,Q_2.
\]

Suppose a nonzero off-diagonal decorated cell

\[
                         A_{uv}(b,a),\qquad b\ne a,
\]

lies on a physical pair `uv` used by none of the three chosen matchings.
Reselect `uv` as the physical pair.  At endpoint `u`, matching `Q_c` supplies
one nonzero diagonal star coordinate

\[
                  A_{u,Q_c(u)}(c,c),\qquad c=0,1,2.
\]

None is deleted because `uv` is absent from every `Q_c`.  The three images
occupy the distinct codomain coordinates `(Q_c(u),c)`, even when two
matchings use the same physical neighbour.  Hence the deleted star at `u`
has rank three.  The same argument at `v` gives

\[
                  \operatorname{rank}P_{uv}
                   =\operatorname{rank}S_{uv}=3.       \tag{1}
\]

This is source-preserving and anchor-safe: only the selected pair changes;
no coefficient is modified or deleted.

Apply the target-augmented private-site identity to the same off-diagonal
direct cell.  It gives

\[
             \sum_s\Delta_{us}C_s=-A_{uv}(b,a)\ne0.    \tag{2}
\]

Therefore at least one literal determinant/cofactor product is nonzero.
Combining (1) and (2), every such cell re-enters the good active-minor route.
The proof works at every even order and uses no minimum-support hypothesis.

## Chart-cover consequence

In the projection-degenerate axis-purified one-bad route, choose a unary
target monomial and one monomial in each diagonal response.  After restoring
the two deleted endpoints, these are exactly three pure target matchings.
Consequently an unresolved cancellation web may be confined to

- diagonal decorated cells; and
- off-diagonal decorations of physical edges already belonging to at least
  one of the three chosen matchings.

Every off-diagonal cell on any other physical pair produces a good pair by
reselection and a nonzero source-provenant active minor.  Thus the genuinely
singular chart-cover problem lives on the three-coloured anchor multigraph,
not on the complete physical graph.

This does not finish the bridge.  A good pair plus a nonzero
determinant/cofactor product is not yet an active clean cap, and it does not
automatically give the distinct-head curved doubly-good OO packet.  The
remaining theorem must either complete that rank/curvature promotion or
handle the decorated-anchor-edge diagonal alternating-cycle web directly.

## Exact finite audit

At eight sites the checker traverses all 31 `S8 x S3` pure-anchor orbits and
every physical pair outside their union.  For each pair it constructs the
three literal surviving anchor coordinates at both endpoints and verifies
rank `(3,3)`.  It then replays the exact symbolic target-augmented identity
at order eight.  The enumeration is only an audit of the uniform argument;
the proof is the matching-coordinate argument above.

Reproduce with

```sh
python3 computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py
python3 -O computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py
python3 -I -S computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py
```
