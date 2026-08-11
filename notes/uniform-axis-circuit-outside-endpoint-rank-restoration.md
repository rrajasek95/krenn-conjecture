# Outside affine-circuit components reduce to a target-coloop boundary

## Result

Let a minimum-support `k=3` response circuit contain an occupied endpoint
component whose physical arm `e` is outside the union of one chosen pure
matching in each target colour.  Its complete two-response column has the
same exact dichotomy as in the strict shore chart:

1. a zero column is an exact finite joint-kernel deletion;
2. a nonzero column has a nonzero literal matching summand, hence makes `e`
   support-active.

Minimum support excludes the first case.  Pair the active arm with a
selected arm `f` of the opposite diagonal colour.  At the common endpoint
their heads are distinct.  The exact remaining question is rank restoration.
For each target colour `c`, let `M_c` be the family of nonzero literal pure
target matchings of colour `c`.  Then the rank certified at either endpoint
after deleting `f` is

\[
 \operatorname{rank}_{\rm sel}(f)
 =\#\{c:\text{ some }Q\in M_c\text{ avoids }f\}.       \tag{1}
\]

Thus the pair is a distinct-head four-good active wedge whenever every
colour whose chosen matching uses `f` has an alternate matching avoiding
`f`.  If this fails, `f` is a physical coloop of at least one pure target
matching family.  That coloop is the exact full-row boundary; it is not a
new family of endpoint supports.

Checker:
`computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py`.

## Why (1) is exact

An avoiding pure-`c` matching supplies, at either deleted endpoint, the
literal deleted-star coordinate

```text
(physical neighbour chosen by the matching, target colour c).
```

Different target colours occupy disjoint coordinate rows, whether or not
their physical neighbours coincide.  Hence one avoiding matching contributes
one independent column, and a colour with no avoiding matching contributes
none at the selected-matching level.  This proves (1) simultaneously at both
ends of `f`.

The checker uses the canonical K8 triple

```text
Q0 = 01 | 23 | 45 | 67
Q1 = 02 | 13 | 46 | 57
Q2 = 03 | 12 | 47 | 56.
```

The outside arm `06` has ranks `(3,3)`.  Pair it with the selected colour-2
arm `56`.  The alternate pure-2 matching

```text
Q2' = 05 | 16 | 24 | 37
```

avoids `56`, so `Q0,Q1,Q2'` restore ranks `(3,3)` on the mate.  Removing
`Q2'` leaves ranks `(2,2)`.  The checker also audits the rank-count formula
at both endpoints of every K8 physical pair.

## Target matching and unary repairs

For a diagonal colour, expand the pure target coefficient by the endpoint
port used in each literal matching.  A nonzero block away from `f` contains
a nonzero matching summand and supplies the required alternate target
matching.  If all avoiding blocks vanish, the coefficient `1` is
concentrated on `f`: this is a normalized diagonal-port coloop.

Colour zero has the source-labelled hafnian recursion.  At a chosen site
`a`,

\[
  1=\operatorname{haf}(q^{00})
   =\sum_{b\ne a}q_{ab}^{00}H_{ab}^{0}.                \tag{2}
\]

If one block avoiding `f=a-b` is nonzero, choose a literal matching summand
from it and restore colour zero.  Otherwise (2) says exactly

\[
 q_{ab}^{00}H_{ab}^{0}=1,
 \qquad q_{ad}^{00}H_{ad}^{0}=0\quad(d\ne b),          \tag{3}
\]

so `f` is a unary coloop.  This is the same common-tail recursion already
used in the Hall dark-bridge theorem, now stated as the rank-restoration
alternative at the affine gate.

## Scope

This removes every outside endpoint component for which the chosen
opposite-colour arm is repairable.  It does **not** prove that an arbitrary
minimum `k=3` circuit has an outside component, nor that the coloop boundary
is empty.  Extra, nonselected source columns can raise the complete deleted-
star rank even when (1) is two; proving that raise or contradicting (3)
requires a literal crossed-response identity from the complete five-row
packet.  Minimum support and the common Hessian recurrence alone do not
supply it.

Run

```text
python3 computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py
python3 -O computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py
python3 -I -S computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py
```

Frozen ledger SHA-256:

```text
7acbb1bfdc0d59ce4bc79138cb0aff60536304c9c1bb7145292ded123e1990d5
```
