# Signed matching circuits cannot supply the missing conormal face

## Outcome

The signed-circuit atoms of `b942209` and `cd08db9` do not construct the
missing source row

\[
                 K=\sum_{|S|=3}(M_S+\alpha D_S)=0.
\]

There is an exact dichotomy.

1. An odd/valuation-holonomy circuit becomes a Laurent unit.  It then closes
   the packet directly: the localized mixed source ideal is the unit ideal,
   so no source point remains.  It can multiply (F_0) only in this already
   inconsistent quotient.
2. A source-compatible balanced circuit, including every four-corner debt
   of the multiplicity cube, stays entirely in mixed target-zero output
   grades.  Its selected-(u) conormal value is zero, so it cannot cancel
   (kappa[F_0]).

An adjacent-chart Bianchi comparison does reach the pure anchor, but only
as a difference of chart copies.  It transports the conormal class rather
than annihilating it.  The conserved quantity is total pure-anchor
incidence.

## Exact two-chart calculation

For chart (c\in\{D,L\}), the complete normal-incidence reinsertion from
`04abf04` is

\[
 \mathcal N_c=Y\mathcal M_c-\kappa Y\rho_c
              -\kappa T_c+\kappa r_{0,c},
\]

with reduced coordinates

\[
       ([F_{0,D}],[F_{0,L}],(\kappa Y)^{-1}d_w)
       (\mathcal N_D)=(1,0,1),\qquad
       (\mathcal N_L)=(0,1,1).                         \tag{1}
\]

The literal word-change/Bianchi interval (dE=L-D) has

\[
                         (-1,1,0).                     \tag{2}
\]

Thus every combination

\[
              a_D\mathcal N_D+a_L\mathcal N_L+z(L-D)
\]

has conormal coordinates

\[
                    (a_D-z,a_L+z)                     \tag{3}
\]

and normalized (w)-boundary (a_D+a_L).  Their sum is invariant:

\[
 \boxed{(a_D-z)+(a_L+z)=a_D+a_L.}                      \tag{4}
\]

Consequently a chain with the desired normalized (w)-boundary one has
total conormal one.  No Bianchi difference can make both chart components
zero.  In the three-coordinate presentation, the primitive separator

\[
                         \lambda=(1,1,-1)              \tag{5}
\]

kills both rows in (1) and the interval (2), but reads (-1) on the desired
class ((0,0,1)).  The available rank is two and rises to three after that
class is adjoined.

The same proof works on any graph of adjacent charts.  Each Bianchi edge is
an incidence vector with coordinate sum zero; every complete chart
candidate contributes the same amount to pure-anchor incidence and to the
normalized (w)-boundary.  Graph incidence can redistribute the anchor
class but cannot change its augmentation.

## Why the odd triangle does not evade (4)

The exact source identity from `b942209` is

\[
             DEf_0-BEf_1+BCf_2=2K_{\rm mon},           \tag{6}
\]

where the three literal words are

```text
20120121, 22100121, 22120101.
```

All are mixed.  Therefore every term in (6), including the contaminated
remainder version, has selected-(u) conormal value zero.  If the active
monomial (K_{\rm mon}) is inverted, (6) gives a unit in characteristic
zero.  This is a direct contradiction to the mixed source equations, not a
relative construction of (4).  Without that unit localization, (6) remains
inside the mixed ideal and cannot produce (F_0).

The `cd08db9` recombination cube is the balanced alternative.  Its four
uncancelled corners `001,010,101,110` are four distinct mixed output rows.
They are useful source debts, but each again has conormal value zero.  Adding
mates, further balanced circuits, or target-zero response companions never
changes (4).

The exact Segre coupling of `e3c52ae` does not alter this conclusion.  Full
source cancellation forces the aggregate mate array on all eight cube words
to be one dense rank-one tensor.  This couples the debts coefficientwise and
is substantially stronger than four independent mates, but all eight words
remain mixed.  Hence every tensor entry and every flattening minor still has
selected-\(u\) conormal value zero.  Segre coupling constrains the mixed
ideal; it does not create the missing pure-anchor incidence.

## Minimal missing source type

The result identifies the exact source type not present in these
mechanisms.  To cancel the candidate of `04abf04` before source base change,
one needs a lower face (C_{\rm rel}) with

\[
 \boxed{
 \text{total pure-anchor incidence}(dC_{\rm rel})=-1,qquad
 d_wC_{\rm rel}=\operatorname{tgt}C_{\rm rel}
               =\operatorname{ores}C_{\rm rel}=0.}    \tag{7}
\]

A mixed signed circuit has anchor incidence zero.  A Bianchi comparison has
incidence vector of total zero.  An odd circuit has the required freedom
only because it has already made the source ideal the unit ideal.  Hence
(7) is a genuinely new normal-incidence lower face, not another matching
circuit or ordinary adjacent-chart difference.

This is a no-go for the named mechanisms, not a theorem that no larger
source resolution can contain (7).  It sharpens the positive task: an exact
proof of (K=0) must break chart-incidence augmentation through a literal
target-normalized lower face while retaining zero target and residue.

## Verification

Run

    python3 computations/verify_h3_signed_circuit_conormal_transport_no_go.py
    python3 -O computations/verify_h3_signed_circuit_conormal_transport_no_go.py

The checker pins `04abf04`, `b942209`, `cd08db9`, `e3c52ae`, and the mixed
bar--curvature input; reconstructs the odd exponent triangle; audits the
four mixed cube debts; proves the two-chart rank/separator statement; checks
72 exact integer Bianchi combinations with normalized boundary one; and
tests the chart-incidence invariant on two through seven charts.

The frozen ledger digest is

    fa6e336d4c4373cee059a557ed572db01edb7e98021dccfd675b5938d2f7011f
