# A flat good wedge need not give a rank-three selector cut

## 1. Outcome

The flat-wedge theorem says that two adjacent flat rank-one good arms force
their opposite chord to have rank at least two, and rank three when their
shared-site factors are independent.  Applying the full-nine selector
theorem to that chord does not, from goodness and orientation alone, bound
one of its universal alignment sets by two.

There is a literal eight-site aggregate packet with

* two flat, doubly-good rank-one arms `pq,pr`;
* independent shared-`p` factors and distinct outgoing coordinate heads;
* an invertible opposite chord `A_qr=I`; and
* chord-chart alignment-set sizes

\[
                         (|T_0|,|T_1|,|T_2|)=(6,6,5).       \tag{1}
\]

Thus the rank-at-least-two selector theorem returns its large-alignment
alternative for every target.  A uniform reduction from arbitrary flat
overlaps to a dark cut must use the full source equations or another
incidence hypothesis; it cannot follow from the flat-wedge rank conclusion
and the two good-arm conditions.

The packet is a structural counterguard, not a ternary source and not a
Krenn counterexample.

## 2. The packet

Use sites `p,q,r,u,v,w,x,y`.  Put

\[
 A_{pq}=E_{00},\qquad A_{pr}=E_{11},\qquad A_{qr}=I.       \tag{2}
\]

Add

\[
 A_{pu}=e_2e_0^{\mathsf T},\qquad
 A_{pv}=(e_0+e_1)e_0^{\mathsf T},                         \tag{3}
\]

and set every other block to zero.  After deleting `q`, the `p`-star sees
the three independent shared-site factors `e_1,e_2,e_0+e_1`; after deleting
`r`, it sees `e_0,e_2,e_0+e_1`.  At the remote endpoints, the invertible
block `A_qr` already makes both deleted stars injective.  Hence the four
goodness ranks are `(3,3,3,3)`.

On the common complement of `p,q,r`, both the `q`- and `r`-stars vanish.
Every canonical transition between the two arms is therefore zero.  Their
shared-`p` factors `e_0,e_1` are independent, and the forced chord in (2)
has rank three, exactly the sharp independent-factor branch of the
flat-wedge theorem.

## 3. The chord selector sees five universal sites

View `qr` as the direct pair.  At the five residual sites other than `p`,
one or both endpoint-star maps are zero, so

\[
                         N_{z,e}=0\qquad(e=0,1,2).          \tag{4}
\]

At `p`, the two local factors are `e_0,e_1`.  Therefore

\[
 N_{p,0}=N_{p,1}=0,\qquad N_{p,2}\ne0.                    \tag{5}
\]

Since `A_qr=I` has rank three while every `N_{z,e}` has rank at most two,
membership in `C A_qr` is equivalent to being zero.  Equations (4)--(5)
give (1).

This identifies the missing implication precisely.  The two original good
arms control injectivity through the opposite chord, but they do not force
the chord endpoints to have any support on the five-site common complement.
Only source exactness could prohibit the five zero local wedges.

## 4. Consequence for the uniform split

At general even order, a flat adjacent good-rank-one wedge cannot yet be
discarded in favour of the curved-overlap branch.  The correct possible
strengthening is conditional:

> prove from the literal full-nine rows that the rank-two/rank-three
> opposite chord in a flat good wedge has some target with at most two
> aligned sites, or derive a smaller exact source directly.

The present packet stops any proof which uses only block ranks, goodness,
selected head axes, and the rank-one flat-transition identity.

## 5. Reproduction

```sh
python3 computations/verify_flat_good_wedge_rank3_selector_counterguard.py
python3 -O computations/verify_flat_good_wedge_rank3_selector_counterguard.py
```

The checker audits endpoint order, both direct ranks, all four star ranks,
literal flatness on the common complement, and all eighteen chord-chart
wedge matrices over the rationals.
