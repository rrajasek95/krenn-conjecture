# Five-row locks propagate by a simultaneous switch or a crossed port wedge

## Result

The leading lock branch left by `7249462` has a source-valid linear
reduction.  Let `D` be a family of normalized switch directions supported
on one physical residual star, and let

\[
 \mathcal L:D\longrightarrow
 T_{\rm unary}\oplus T_{11}\oplus T_{12}\oplus T_{21}\oplus T_{22}
                                                               \tag{1}
\]

be the unary plus four companion lock map.

1. Every linear combination `d in D` still has `d^[2]=0`.  Therefore
   `L` is an **exact linear map**, not merely a tangent map.  A nonzero
   vector in `ker L` gives a simultaneous anchor-safe switch; after scaling
   one blocker coefficient to its negative source value, it deletes that
   blocker and only resizes already supported factor cells.
2. In the axis-purified branch, suppose a nonzero component of `L_12` is
   carried by an off-anchor port pair `r-s`, while a nonzero component of
   `L_21` is carried by another off-anchor pair `r-t`.  The two pairs share
   `r`.  Then the three selected pure target matchings give rank three at
   all four deleted stars, the lock components give nonzero cofactors, and
   the two centre heads are the distinct target axes.  This is a
   distinct-head four-good active overlap.

Thus the exact residual is smaller than an arbitrary five-row lock web:

\[
 \boxed{\mathcal L\text{ injective, and its crossed port-incidence graph
 has no complementary off-anchor wedge}.}              \tag{2}
\]

Checker: `computations/verify_uniform_five_lock_wedge_or_switch.py`.

## Why the simultaneous switch is exact

If every cell of `d_1,...,d_m` meets the same physical site, then

\[
             \left(\sum_i c_i d_i\right)^{[2]}=0.       \tag{3}
\]

Consequently the complete finite differences are

\[
\begin{aligned}
 T_0(q+d)-T_0(q)&=dq^{[h-1]},\\
 T_{ij}(q+d)-T_{ij}(q)&=p_i s_j d q^{[h-2]}.
\end{aligned}                                          \tag{4}

Both sides are linear in `d`.  The checker uses the physical diagonal web
of `f9b51a9`, combines two independent same-star directions with rational
coefficients, and verifies (4) for the unary row and all four ordered
response rows at every `3 <= h <= 8`.

At a maximum-anchor/minimum-support source, a kernel vector can be scaled so
one of its blocker entries is deleted.  The companion factor entries were
already supported, and all changed cells share a coordinate, so no old
mutual anchor is lost.  This is precisely the simultaneous descent that an
individual nonzero lock can hide.

## Why the crossed wedge is four-good and active

Choose one pure matching `Q_c` in each target colour.  If a physical pair
`rs` belongs to none of them, then after deleting `rs`, each `Q_c` supplies
one surviving coordinate column at both endpoints.  The three columns have
disjoint `(neighbour,colour)` supports, hence both deleted stars have rank
three.  This is the matching-coordinate argument of `336492c`, applied to
the port pair selected by the crossed lock rather than to a pre-existing
internal off-diagonal cell.

Now take nonzero collected components

\[
 [\mathcal L_{12}]_{rs}\ne0,\qquad
 [\mathcal L_{21}]_{rt}\ne0,                           \tag{5}
\]

with `s != t` and both pairs off the anchor union.  Equation (5) gives the
two nonzero cofactor witnesses.  Axis purification makes their heads at the
shared site `r` equal to `e_1` and `e_2`; their `2 x 2` minor is one after
coordinate normalization.  The overlapping pairs are therefore active,
four-good, and distinct-head.

The checker audits the rank statement on a canonical triple of pure
matchings.  This is only a coordinate normalization: the proof uses the
three disjoint colour columns and applies to every order and every matching
triple.

## Sharp remaining incidence condition

Nonzero five-row locks alone do not force either conclusion.  The checker
freezes the smallest abstract source-labelled module with two switch
directions:

```text
d1 -> nonzero unary lock,
d2 -> one nonzero L12 component,
no L21 component.
```

Its lock map is injective, so there is no simultaneous switch, and its
crossed incidence graph has no complementary wedge.  This is not claimed to
be a full one-bad source.  It proves exactly what the remaining physical
rows must supply:

> the common matching provenance must either create a dependence among
> same-star lock columns or mate every surviving crossed component with the
> opposite crossed row at a shared off-anchor port.

The first new hypothesis is therefore an incidence/mating statement for
the two crossed zero rows, not another Rees order or a larger diagonal-cycle
census.  Unary and diagonal locks may remain as coordinates of the
injective map, but cannot by themselves produce the four-good overlap.

## Scope and verification

This theorem is exact and source-labelled at the lock level.  It does not
prove that every full one-bad lock web satisfies the crossed mating
hypothesis; (2) is the sharply named residual.  It also does not turn a
single good active pair into curvature without the complementary crossed
component.

Run

```text
python3 computations/verify_uniform_five_lock_wedge_or_switch.py
python3 -O computations/verify_uniform_five_lock_wedge_or_switch.py
python3 -I -S computations/verify_uniform_five_lock_wedge_or_switch.py
```

The checker pins `7249462`, `f9b51a9`, and `336492c`, verifies exact
same-star linearity, audits the four rank-three deleted stars and transverse
centre minor, and freezes the first injective no-wedge lock module.

Frozen ledger SHA-256:

```text
74e798509caf61d60ae99657e33019a9a1ad00187c7b5fa8db133184c7961137
```
