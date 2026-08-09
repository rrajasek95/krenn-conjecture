# Axis-purified one-sided essential edges cannot carry three pure rows

## Statement

Let `B` have eight sites.  At every site `u` fix a target-axis line

\[
                         L_u=\mathbb C e_{\ell(u)},
             \qquad \ell(u)\in\{0,1,2\}.
\]

Suppose every physical block has the following one-sided property: if its
`(c,c)` cell is nonzero, then at least one endpoint has `L=e_c`.  If the
aggregate matching tensor has a nonzero pure coefficient in each of the
three colours, these hypotheses are inconsistent.

This is the exact coefficient lemma needed on a sharp essential-incidence
packet once two further facts have been proved there:

1. the common nonessential line at every site is a coordinate axis; and
2. no physical edge is essential at both endpoints.

Indeed, a nonzero `(c,c)` cell whose endpoint line is not `e_c` makes that
edge essential at that endpoint.  The second condition then gives the
one-sided property above.  The lemma does not assert either hypothesis for
an arbitrary reciprocal packet.

## Proof

Fix a colour `c`.  Its nonzero pure coefficient contains at least one
supported perfect-matching monomial.  Every edge of that matching has a
`c`-labelled endpoint.  Since the four matching edges are disjoint, their
chosen endpoints are four distinct sites.  Hence

\[
                   |\{u:\ell(u)=c\}|\ge4.
\]

Applying this to all three colours requires at least twelve sites, but
`|B|=8`.  This is a termwise support contradiction; cancellation among
other pure or mixed monomials is irrelevant.

The bound is sharp for two colours: a `4+4` labelling has exactly `4!=24`
compatible crossing perfect matchings for either colour.

## Scope in the reciprocal program

The lemma closes any `r=4` equality face on which the four common lines are
coordinate-purified at all eight sites and all sixteen essential incidences
are already used one per bad edge.  It does **not** close a face whose
common lines are arbitrary projective lines: a line such as
`C(e_0+e_1)` has nonzero coefficients in two pure colours.  Thus an
application must explicitly obtain axis purification from incoming
source-labelled witnesses, for example from a good reciprocal matching or
from nonessential incoming single arcs.

## Reproduction

```text
python3 computations/verify_axis_purified_one_sided_pure_cover.py
python3 -O computations/verify_axis_purified_one_sided_pure_cover.py
```

The checker enumerates all `3^8=6561` axis labellings and all 105 perfect
matchings, and separately freezes the sharp two-colour `4+4` boundary.
