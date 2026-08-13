# A dark pointed occurrence lowers support only on an affine matching face

## Exact support-lowering lemma

Let `F` be the complete physical source map in scalar-cell coordinates and
let `xi` be a full-source tangent, `J_xF xi=0`, detected by the marked
pointed occurrence `P_f`.  Every coefficient of `F` is a sum of literal
matching monomials and hence is multiaffine in every scalar cell.

If every physical source monomial contains at most one cell from
`supp(xi)`, then there are no higher terms:

\[
                         F(x+t\xi)=F(x)+tJ_xF\xi=F(x). \tag{1}
\]

This hypothesis is automatic when the varied `q` cells lie in one physical
site star: a perfect matching uses at most one such edge.  It is also
automatic for cells of one fixed endpoint row, because a response
occurrence uses exactly one `p_i` and one `s_j` component.

Suppose in addition that

1. `supp(xi)` is contained in the already occupied scalar support;
2. it is zero on every protected mutual anchor; and
3. `xi_e != 0` on the marked occupied cell.

Taking `t=-x_e/xi_e` in (1) deletes `e`, activates no previously zero cell,
preserves every complete source equation and anchor, and contradicts the
minimum occupied scalar support.  This is the shortest valid use of
minimum support.

Checker:
[`verify_h3_pf_dark_kernel_support_lowering_hasse_coloop_gate.py`](../computations/verify_h3_pf_dark_kernel_support_lowering_hasse_coloop_gate.py).

## Why a bare `P_f`-dark kernel is insufficient

The exact duality statement `P_f notin row(J_xF)` produces some tangent
`xi in ker(J_xF)` with `P_f(xi) != 0`.  It does not say that `xi` is
supported on occupied columns.  If a direction deletes one occupied cell
but activates one formerly zero cell, the generic support does not fall.

Nor does first-order kernel membership prove (1).  Along an arbitrary
direction the matching expansion is

\[
 F(x+t\xi)=F(x)+tJ_xF\xi+
       \sum_{r\ge2}t^r H_r(\xi),                      \tag{2}
\]

where `H_r` is the literal sum over `r` pairwise co-occurring varied cells,
each multiplied by its complementary matching cofactor.  At `h=3`, target
and fixed-right response equations require only orders two and three, but
those orders need not vanish.  A formal local arc is not enough for minimum
support either: every occupied coordinate remains a unit in `k[[t]]`.
One needs an actual affine deletion or a separately controlled global
specialization.

## Literal nonlinear packet

There is a source-faithful six-site block showing the first alternative.
Use the pure-colour matching

```text
q01^00 = q23^00 = q45^00 = 1
```

and the two literal occurrences in one target-zero response coefficient

```text
f = p_i[0,0] s_j[1,0] q23^00 q45^00 =  1,
g = p_i[2,0] s_j[3,0] q01^00 q45^00 = -1.
```

Thus the complete selected rows are

\[
 T=q_{01}q_{23}q_{45}=1,
 \qquad R=f+g=0.                                      \tag{3}
\]

The tangent

```text
dq01=1, dq23=1, dq45=-2
```

kills both differentials.  It redistributes the occurrences by
`df=-1,dg=1`, so it is detected by the marked pointed face.  Nevertheless,
on the affine line,

\[
 T(x+t\xi)=1-3t^2-2t^3,\qquad R(x+t\xi)=0.           \tag{4}
\]

The first side effect is the physical pure-`000000` target row, not an
offdiagonal fan or four-good carrier.

The tangent does integrate exactly, but only through the torus family

\[
 q_{01}=q_{23}=a,qquad q_{45}=a^{-2}.                \tag{5}

Both equations (3) remain exact on `D(a)`.  The point `a=0` is absent, and
indeed the normalized target factorization in (3) makes all three cells
units.  This is precisely pure-target coloop saturation.  It demonstrates
that even an integrable occurrence redistribution need not lower support.

The packet is a literal complete target/response word block.  It is not
asserted to be a standalone full nine-row GHZ source; it is the exact
quotient guard showing what the presently known coloop and response rows
can and cannot force.

## Routing of side effects

The first nonzero `H_r` in (2) carries genuine source provenance: its cells,
word, fine grade, endpoint heads, and complementary matching tail are all
literal.  Existing branches consume it under one of the following extra
incidences:

- an offdiagonal moved cell has a nonzero private-site cofactor, giving the
  active-fan route;
- its complete endpoint hole lies outside the trapped shore, giving finite
  Hall/four-good saturation; or
- it is a unique normalized pure-target matching face, giving coloop
  saturation as in (3).

These outcomes are not consequences of `P_f` darkness alone.  The example
above already shows that a nonlinear face can be purely diagonal.  A zero
or cancelling complementary cofactor can also prevent the first two
landings.

Therefore the sole occurrence-isolation theorem can be stated sharply:

> For every `P_f`-visible full-source kernel, either find an occupied,
> anchor-safe representative supported on an occurrence-incompatible set,
> or show that its first nonzero labelled Hasse face has a nonzero
> private-site, outside-hole, or normalized-coloop landing.

The first arm gives an exact support deletion by (1).  The other arms are
already named physical branches.  What remains open is this representative
or incidence theorem; abstract kernel existence and formal integration are
strictly weaker.

## Scope

This is exact at canonical `h=3` for the matching-multiaffine source and for
the displayed literal target/response block.  It neither constructs the
missing `P_f` comparison nor asserts that every higher face lands.  It
identifies the minimum extra statement needed to make minimum occupied
support do work.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded by the checker.
