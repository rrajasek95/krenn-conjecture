# Bidirectional private-site fans isolate the endpoint-attachment residual

## The source identity already supplies transverse heads

Let a nonzero off-diagonal physical cell be

\[
                         e=A_{vu}^{ba},\qquad a\ne b.
\]

Apply the target-augmented private-site identity to the pure-`a` row,
changing site `v` to `b`.  Exact source provenance gives

\[
 \sum_{s\ne u,v}\Delta^{v}_{us}C^a_{vs}=-A_{vu}^{ba}.       \tag{1}
\]

Every nonzero summand in (1) is an active two-edge fan at `v`.  Its two
heads at `v` are `a,b`; both outer heads are `a`.  Now transpose `u,v` and
apply the same identity to the pure-`b` row, changing `u` to `a`:

\[
 \sum_{t\ne u,v}\Delta^{u}_{vt}C^b_{ut}=-A_{uv}^{ab}.       \tag{2}
\]

The right sides of (1) and (2) are the same physical cell.  Equation (2)
is the dual active fan: its centre heads at `u` are `b,a` and its outer
heads lie on `b`.  Thus a same-head Fitting carrier does **not** lack a
second head at coefficient level.  The full unary and pure diagonal rows
already force transverse heads at both endpoints.  The remaining issue is
deleted-star goodness and escape from the selected-anchor web.

The exact checker is
`computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py`.

## Off-anchor fans land immediately

Choose one nonzero pure matching in each target colour.  If one nonzero
summand of (1) uses two physical edges outside the union of those three
matchings, then every deleted endpoint star retains one coordinate column
in each target colour.  All four ranks are three.  Since the determinant in
that summand is nonzero and its two centre heads are distinct, the two
edges form a distinct-head four-good active overlap.

This argument is uniform in the order.  The checker exhausts all 31
`S8 x S3` anchor orbits and every ordered two-edge off-anchor fan at `N=8`;
the minimum of all four deleted-star ranks is three.

Consequently the sharp residual has both bidirectional fans trapped in the
selected-anchor web.  There the five-lock theorem gives the exact split:

1. a same-star lock kernel is an exact anchor-safe support deletion;
2. complementary crossed off-anchor components give the four-good wedge;
3. otherwise the lock map is injective and has no complementary wedge.

The third case is the finite Hall/lock residual, not a missing transverse
coefficient.

## Same-cell companions cannot repair the residual

Every complete row containing the fixed cell `A_vu^{ba}` retains endpoint
labels `b,a`, regardless of its complement matching.  It may change the
physical partners but cannot create a pure-`k` endpoint row for
`k notin {a,b}`.  The pinned six-site guard cancels all three rest-colour
companion rows inside the anchor union and still has deleted ranks `(2,3)`.
This is a complete three-row guard, not a full GHZ source.

Hence the smallest remaining full-source implication is precise:

> In an injective no-wedge anchor web, the unary row and the opposite
> diagonal/crossed rows must produce a differently labelled endpoint
> component, a pure-anchor reselection, or an effective Hall carrier.

Additional tails of the same decorated cell cannot prove this implication.

## Relation to the 2c/66a attachment gates

The `2c981a6` silent-`C6` reduction has a degree-zero endpoint-grade
cokernel: its complete first-hit unary/`G11` columns return to the same
private generator, while `G22` can enter only through an endpoint-word
change.  The present rank residual asks for exactly the degree-zero shadow
of such an attachment.

The `66af3a5` rootless third-cofactor gate is strictly stronger.  Its
candidate must be a relative chain cell in repeated-site `P3 disjoint K2`
degree and must cancel the selected source unit, `Omega_v`, and `q_(v,N)`
with zero target and ordinary-residue readouts.  An ordinary matching-row
identity does not supply those boundaries.

Therefore the two gates can be closed by one theorem only in the following
chain-level form:

> A source-labelled endpoint-word-change homotopy, natural under common-tail
> multiplication, has a degree-zero shadow that supplies the missing endpoint
> head, and a relative degree-one boundary that cancels the rootless unit and
> ridge companions with `W=tgt=ores=0`.

The checker proves that same-cell companions cannot be this homotopy.  It
does not construct the homotopy, so it does not promote the rank boundary
or the rootless comparison to a global closure.

## Verification

Run

```text
python3 computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py
python3 -O computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py
python3 -I -S computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py
```

Frozen ledger SHA-256:

```text
1fa9293975fa0a52088996b521e258dae1664fbe71daf6885549d856353eeeb4
```
