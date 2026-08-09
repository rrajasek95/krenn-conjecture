# The anchored smooth germ is not a target-torus basin

## Verdict

The target-stabilizing diagonal torus cannot supply the missing global
accessibility theorem for the smooth anchored germ of
[`n8-three-cut-full-fibre-tangent-and-zero-stratum-radical.md`](n8-three-cut-full-fibre-tangent-and-zero-stratum-radical.md).
In fact, the strongest honest minimum-support normalization points in the
opposite direction:

> **Minimum-support no-go.**  If the ternary exact fibre at `N=8` is
> nonempty and `A` has inclusion-minimal aggregate support in that fibre,
> then no target-stabilizing one-parameter subgroup has a nontrivial finite
> limit on `A`.

Thus such a normalization cannot degenerate `A` into the anchored boundary
plane.  The local theorem at commit `ece62cf` remains exact and useful, but a
global proof now needs a combinatorial cover by source charts (or a non-torus
normal-form operation), not a universal Hilbert--Mumford basin.

The exact census is reproduced by
[`verify_n8_anchored_hilbert_mumford_accessibility.py`](../computations/verify_n8_anchored_hilbert_mumford_accessibility.py).

## 1. Endpoint-ordered aggregate characters

Write a source coordinate in canonical endpoint order as

```text
s = (u,v;i,j),  u < v,
```

where `i` is the colour at `u` and `j` the colour at `v`.  Reversing an edge
also reverses the two colour slots; this convention is important for mixed
cells.  If the original graph has parallel edges, first sum the parallel
entries with the same ordered endpoints and endpoint colours.  Every summand
has the same character, so their aggregate cell transforms as one scalar;
complex cancellation inside the aggregate is neither broken nor created by
the target torus.

The target-stabilizing torus is

\[
 T_\Delta=\{(\lambda_{v,i}):\prod_v\lambda_{v,i}=1
                         \text{ for }i=0,1,2\},
\]

and the aggregate cell has character

\[
 a_s=e_{u,i}+e_{v,j}.
\]

A cocharacter is an integral array `h(v,i)` satisfying
`sum_v h(v,i)=0` separately for the three colours.  Its weight on `s` is

\[
             w_h(s)=h(u,i)+h(v,j).                         \tag{1}
\]

For a fixed source `A`, a finite limit as `t -> 0` exists exactly when
`w_h(s) >= 0` on every nonzero aggregate cell.  Cells of positive weight
vanish and cells of weight zero survive.

## 2. Why minimum support forbids accessibility

Suppose `Phi(A)=Delta`.  Equivariance and target stabilization give

\[
              \Phi(h(t)A)=h(t)\Phi(A)=\Delta              \tag{2}
\]

for every nonzero `t`.  If all supported weights are nonnegative, polynomial
continuity extends (2) to the finite limit.  If at least one weight is
positive, that limit is another exact source with strictly smaller aggregate
support.  This contradicts inclusion minimality.

Consequently every finite cocharacter on a minimum-support exact source has
weight zero on its entire support.  Equivalently, zero lies in the relative
interior of the convex hull of its restricted support characters; the orbit
is closed and the support has a strictly positive port-incidence balance.
This is the support-minimal form of the polystable-fibre theorem in
[`torus-polystable-fiber.md`](torus-polystable-fiber.md).

The same proof covers target-torus Puiseux arcs.  After a finite base change,
a diagonal torus arc factors as `u(t)t^h`, where every component of `u(t)` is
a unit with a nonzero limit.  The unit factor cannot delete a nonzero
aggregate coordinate.  The valuation factor `t^h` is governed by (1), hence
is trivial on the support by the preceding paragraph.  The limit remains in
the same torus orbit.

Arbitrary complex matching cancellations do not open a loophole.  All
perfect-matching monomials contributing to a fixed output word have the same
target-torus character, namely the character of that word.  Equation (2)
therefore holds before any cancellation is evaluated.  It is not a
termwise-genericity argument.

The result is stronger than what a lexicographic "maximum anchors, then
minimum support" choice alone justifies.  A degeneration can leave that
lexicographic stratum, so relative minimality there gives no basin theorem.
Global inclusion-minimality is rigorous, and it rules out rather than forces
the desired degeneration.  Moreover the `ece62cf` germ has empty full-GHZ
intersection, so even a weight-zero unit limit cannot land there.

## 3. Exact anchored weight census

The audited anchored cylinder source has 16 aggregate cells.  Modulo the
three target characters its support-character rank is 12, and its
target-torus stabilizer has dimension 9.  The following integral
cocharacter is an exact Farkas certificate that the support is not balanced:

```text
colour 0: (-1,  1, 0,  0, -1,  1, -1,  1)
colour 1: (-1, -1, 1, -1,  1, -1,  1,  1)
colour 2: (-1, -1, 1,  1,  1, -1,  1, -1)
```

The three rows sum to zero.  In sorted support order its 16 cell weights are

```text
(0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0).
```

The unique positive cell is `(2,5;0,0)`.  The finite initial form deletes
that cell, retains the three pure coefficients `(1,1,1)`, and changes exactly
two mixed full-tensor coefficients.  Of the three active complete cuts
`(2,3,4)`, cuts 2 and 3 remain active-complete while cut 4 drops out.  Thus
even the anchored countermodel's own torus orbit runs toward a different
rank stratum, not inward through the audited active germ.  This is an
exact-arithmetic HM orbit calculation on a cylinder source, not a
ternary-GHZ counterexample.

There are also six absent cells whose characters already lie in the span of
the anchor characters and the target constraints:

```text
(2,4;2,0) (2,6;0,1) (3,4;0,0)
(3,7;0,2) (4,6;0,1) (5,7;0,2).
```

Every cocharacter that fixes the anchored support has weight zero on these
cells, so it cannot remove them.  The remaining quotient characters form
136 signed rays and contain 292 literal opposing pairs; the first is
`(0,1;0,1)` against `(1,4;0,1)`.  No cocharacter finite on both can make both
strictly positive.  After adjoining all 15 `ece62cf` plane directions, the
character rank is 21 and only a 3-dimensional target stabilizer remains.
Among the 222 absent cells outside that plane, 111 are invisible to this
residual stabilizer and 111 are nonzero rays.  These are exact obstructions
to treating the plane as a torus-attracting chart.

## 4. D1 semantic support

The current D1 `m=10` candidate is a 77-cell semantic support whose localized
coefficient ideal is already proved empty.  It is therefore not an exact
source and cannot itself certify a closed exact orbit.  Its HM support audit
is nevertheless useful: the integral cocharacter

```text
colour 0: (0,0,0,0, 0, 0,0,0)
colour 1: (0,1,0,1,-1,-1,0,0)
colour 2: (0,0,0,0, 0, 0,0,0)
```

has weights `0^54, 1^22, 2^1` on its 77 cells.  Hence that semantic support
is also unstable, rather than a polystable support away from the anchored
plane.  This does not rescue accessibility: any hypothetical exact fibre
still has a closed/minimum-support orbit by Section 2, whether or not either
known semantic chart contains it.

## 5. Replacement global target

The viable global statement is a chart-cover theorem, not a one-chart basin:

1. choose an inclusion-minimal exact representative and retain its certified
   positive port-incidence balance;
2. choose the pure matching anchors, respecting endpoint order and aggregate
   parallel cells;
3. quotient the resulting balanced support charts by vertex/colour symmetry;
4. on each structural chart, apply a source-ideal identity (clean-fibre
   toric circuit, D1 saturation circuit, four-cylinder/Fitting identity), or
   a non-torus normal form that is proved to land in an audited empty germ.

The missing theorem is a finite structural cover in step 3: every balanced
anchored support must expose one of the known ideal certificates, or a new
explicit exceptional chart.  Hilbert--Mumford faces cannot provide that
cover, because a minimum-support exact representative has no proper finite
target-torus face at all.

## Scope

This note rules out the proposed target-torus accessibility mechanism.  It
does not rule out the conjecture, exhibit an `N=8` ternary-GHZ realization,
or prove that every hypothetical source is globally disconnected from the
anchored component by arbitrary non-torus deformations.
