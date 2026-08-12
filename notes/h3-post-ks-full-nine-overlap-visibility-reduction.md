# Full-nine incidence turns post-KS double darkness into one-sided overlaps

## Outcome

The post-KS rank boundary does not require one physical arm to repair both
deficient quotients of the original cap.  On an eight-site boundary, the
uniform full-nine incidence theorem forces at least two internal sites whose
aggregate incident `q`-span contains all three target axes.  If `u` is such
a site in the cap deleting `P,S`, then the endpoint star at `u` remains rank
three in both overlapping caps deleting `P,u` and `S,u`.

Consequently, a source-faithful transport of the active/common-`q` class to
one of those overlapping caps needs to pass only one quotient test.  For
example, in the cap `P,u`, the `u` endpoint is already rank three.  If the
transported physical column is nonzero in the one-dimensional deficient
quotient at `P`, the cap has ranks `(3,3)` and is eligible for the global
active-clean descent.  The original cap need not be repaired.

Checker:
`computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py`.

## Exact incidence input

For the eight internal sites write

\[
 D_i=\{u:e_i^{(u)}\text{ belongs to the complete incident }q\text{-span at }u\}.
\]

The full-nine equations give

\[
 |D_i|\geq6,\qquad D_0\cup D_1\cup D_2=U,
 \qquad n_3\geq n_1+2.                                  \tag{1}
\]

In particular `n_3>=2`.  The checker exhausts the `46,585` possible triples
of incidence sets satisfying the first two conditions and recovers the same
minimum.  This uses no matching-term noncancellation and no blockwise-rank
hypothesis.

If `u` is target-full in the `P,S` cap, its incident span uses only edges
from `u` to the other internal sites.  All of those direct-sum components
are still present when `u` becomes an endpoint of the `P,u` or `S,u` cap.
Adding the remaining endpoint component cannot lower rank.  Thus the
aggregate `u`-star in each overlapping cap is injective.

## The one-sided quotient test

Let the other endpoint star in an overlap have rank-two image `W` in a
three-dimensional target, and choose its quotient covector `lambda`.  A
transported active column `z` gives

\[
 \operatorname{rank}(W+\langle z\rangle)=3
 \quad\Longleftrightarrow\quad \lambda(z)\ne0.          \tag{2}
\]

The target-full endpoint already has rank three, so (2) is the entire rank
test.  The checker freezes the exact profiles

```text
before transport:       (2,3)
quotient-dark transport:(2,3)
quotient-visible:       (3,3).
```

This is strictly weaker than the earlier local target of repairing both
deficient quotient lines of the original `(2,2,3,3)` cap.  For the global
proof, a good active overlapping cap is enough.

## What remains open

The incidence theorem is aggregate.  It does not construct the physical
overlap transport, and it does not say that one individual block or
source-labelled column is nonzero in (2).  The exact next theorem is:

> **One-sided active-overlap theorem.**  Let `P,S` carry the selected
> active/common-`q` class after endpoint holonomy has been resolved.  For at
> least one target-full internal site `u`, the literal full-nine overlap
> transports that class to `P,u` or `S,u` with nonzero outer deficient-
> quotient image; otherwise the complete rows give a same-row dependence or
> a source-visible endpoint-dark/maximal-shore relation.

The support-dependence alternative is already closed: a complete same-row
kernel vector touching the carrier gives an exact anchor-safe deletion.
Thus the genuine residue is the simultaneous darkness of every legitimate
transport through at least two target-full sites.  This is a one-sided
overlap/maximal-shore problem, not a demand for a miraculous double-
transverse arm.

The residual-`q` covariance--curvature homotopy supplies the natural
candidate transport at the source-symbol level.  Its physical terminal
fiber-product gluing and this one-sided visibility statement are therefore
the two compatible halves of one overlap theorem: first construct the
source-faithful transport, then show it cannot be dark at every full site.

## Scope

This is an exact consequence of the proved full-nine incidence invariant
and elementary rank algebra.  It does **not** prove blockwise activity,
construct the residual-`q` relative cell, or close the endpoint-dark shore.
It narrows the post-KS rank theorem and changes the preferred proof target.

Run:

```text
python3 computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py
python3 -O computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py
python3 -I -S computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py
```

Frozen ledger SHA-256:

```text
efcf8f7ee13b735f1db707abdd6c6089d9e1fb2b6f78b46a432ef538f639c157
```
