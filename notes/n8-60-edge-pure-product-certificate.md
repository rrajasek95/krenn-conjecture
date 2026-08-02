# Exact pure-product membership on the eight-site 60-edge chart

## Result

Normalize the twelve nonzero boundary coordinates to one and set every
endpoint-colour variable outside the audited 60-edge set to zero.  The
remaining coordinate ring has 48 variables.  In this ring there is an exact
integer identity

\[
  \boxed{\sum_{i=1}^{73} A_i H_{c_i}
  =2H_{00000000}H_{11111111}H_{22222222},}
\]

where every \(c_i\) is mixed.  Consequently, in characteristic zero,

\[
  H_0H_1H_2\in I_{\mathrm{mix}}
\]

on the normalized 60-edge chart.  This is stronger than radical membership:
the pure product itself, not merely a power, lies in the restricted mixed
ideal.

Equivalently,

\[
  V(I_{\mathrm{mix}})\cap
  \{H_0H_1H_2\ne0\}=\varnothing
\]

on this entire chart, with no sparsity bound.  Thus the 30-coordinate torus
family of `aa4a731` correctly kills two pure coefficients; it cannot deform
elsewhere inside the 60-edge chart to a point with all three pure
coefficients nonzero.

## Why normalization is lossless

The twelve boundary variables form a perfect matching of the 24 coloured
ports.  When they are nonzero, the port torus independently scales them to
one.  Each coefficient \(H_c\) is multiplied by a nonzero word-dependent
scalar, so the conditions

\[
  H_c=0\text{ for every mixed }c,
  \qquad H_0H_1H_2\ne0
\]

are unchanged.  The normalized identity therefore rules out every
three-pure common zero in the boundary-localized 60-edge coordinate chart,
not only points already written in the chosen gauge.

## Certificate structure

Of the 6,558 mixed words, 928 have nonzero restrictions to the chart.  After
deduplicating equal restrictions, there are 900 mixed polynomials.  Order
them deterministically by their exact monomial representation.  The frozen
certificate uses 73 of these generators.  Across the 73 multipliers
\(A_i\), there are 282 nonzero monomial terms.

The certificate is stored as

```text
computations/certificates/n8_60_edge_pure_product_certificate.json
```

Each entry contains a one-based generator index and an integer sparse
multiplier.  Variable indices refer to the fixed ordered list of the 48
off-support coordinates in
`verify_n8_localized_dual_edge_sparse_no_go.py`.

The checker reconstructs all 900 mixed polynomials directly from their 105
perfect-matching expansions, reconstructs the three pure coefficients,
multiplies the sparse certificate over \(\mathbb Z\), and verifies literal
dictionary equality with \(2H_0H_1H_2\).  It also freezes both the
certificate file and the replay ledger by SHA-256.

No computer-algebra system is used during verification.  A Gröbner lift was
used only to discover the sparse identity.

## Port-torus structure

Although the displayed certificate was discovered after setting the twelve
support variables to one, it is not an untyped affine cancellation.  For a
multiplier monomial \(Q\) and mixed word \(c\), compare the degrees at the
two coloured ports paired by each boundary-support edge.  A Laurent power
of that support edge can balance \(QH_c\) precisely when those two degrees
agree.

The checker performs this test on all 282 multiplier terms.  Every term has
at least one valid mixed-word typing:

\[
  135\text{ terms have one typing},\qquad
  147\text{ terms have two typings}.
\]

The required Laurent exponents of support variables range only from
\(-2\) to \(1\).  Thus the identity rehomogenizes in the boundary-support
localization and is naturally a port-multigraded Laurent certificate.  Its
main structure comes from the support-pair torus grading; the sparse
Gröbner presentation itself is not visibly a single Plücker or Pfaffian
relation.

## Relation to the tangent calculation

At the exact torus family, the pure-map tangent has rank one and the two
missing pure differentials lie in the mixed conormal.  That calculation by
itself allowed a possible higher-order branch.  The present global chart
identity closes that loophole: even a higher-order deformation staying in
the 60-edge chart must satisfy

\[
  H_0H_1H_2=0.
\]

The identity also explains the colour-permuted one-pure tori.  They may or
may not lie on a common larger component of the mixed fibre, but no point on
that component inside this chart can have all three pure coordinates
nonzero.

## Scope

This settles the relevant pure-product saturation on the full 60-edge
ansatz, at arbitrary off-support sparsity.  It does **not** yet prove

\[
  H_0H_1H_2\in\sqrt{I_{\mathrm{mix}}}
\]

in the complete 252-variable ring.  A three-pure common zero could still
use a coordinate outside the dual's 60-edge support.  Any continuation of
the source-ideal attack must therefore enlarge the coordinate chart rather
than search more densely inside the same 60 edges.

A direct Laurent-homogeneous use of this certificate with the full hafnian
coefficients does not cancel the newly restored variables: with a fixed
valid typing it leaves 754 monomials at the first off-chart filtration
degree.  This is not a nonmembership proof—additional mixed syzygies could
repair the residual—but it shows that extension to 252 variables is a
genuine lifting problem, not a formal consequence of the 60-edge identity.

Nor can the identity be graph-independent for all even sizes without an
additional size hypothesis.  At two sites the pure coefficients are the
three independent diagonal coordinates \(x_{12}^{00},x_{12}^{11},
x_{12}^{22}\), while the mixed ideal contains only off-diagonal-colour
coordinates; their pure product is not even in its radical.  This elementary
counterexample does not address a possible uniform identity restricted to
the conjectural range of larger even \(n\), but it confirms that the present
certificate encodes real eight-site/chart structure.

## Reproduction

```sh
python3 computations/verify_n8_60_edge_pure_product_membership.py
python3 -O computations/verify_n8_60_edge_pure_product_membership.py
python3 -I computations/verify_n8_60_edge_pure_product_membership.py
python3 -S computations/verify_n8_60_edge_pure_product_membership.py
```

The replay reports 73 used mixed generators, 282 multiplier terms, and
certificate scalar two.
