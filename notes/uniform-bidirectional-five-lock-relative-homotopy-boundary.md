# The bidirectional five-lock has one relative endpoint holonomy

## Outcome

After the same-star kernel and opposite crossed-wedge exits, the two
transposed private-site fans do not create a new Hall topology.  On the
literal common-tail submodule, the full unary plus four response rows form a
relative signless-incidence component with two marked ends.  Its alternating
boundary is

\[
                         D=E_+-E_- .                    \tag{1}
\]

Combining (1) with the existing rootless bar

\[
                         B=-\Omega+q_{\rm comp}
\]

gives exactly the shared attachment

\[
       A=D-B=E_+-E_-+\Omega-q_{\rm comp}=(1,-1,1,-1). \tag{2}
\]

Thus common matching provenance closes the injective/no-wedge residual into
the proposed endpoint-word-change homotopy.  The remaining issue is sharp:
the physical full rows must force equal literal tail weights and the correct
source-word parity.  One unequal tail leaves a one-dimensional endpoint
holonomy separator, even when every one of the five row types occurs.

Checker:
`computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py`.

## 1. Why there are two marked ends

For a nonzero off-diagonal cell

\[
                         e=A_{vu}^{ba},\qquad a\ne b,
\]

the two target-augmented private-site identities of `44dbdfd` are

\[
 \sum_s\Delta^v_{us}C^a_{vs}=-e,
 \qquad
 \sum_t\Delta^u_{vt}C^b_{ut}=-e.                       \tag{3}
\]

They use the same physical cell and have transposed distinct centre heads.
Subtracting (3) cancels the inhomogeneous term.  Off-anchor summands already
land in the four-good active branch.  If both fans are anchor-contained,
`016886b` leaves exactly the injective five-lock with no complementary
crossed wedge.

Now expand the unary, `11`, `12`, `21`, and `22` rows by literal decorated
matching tail.  A coefficient containing exactly two surviving lock columns
on the same tail, with the common cofactor left uncollected, is a signless
incidence row

\[
                              z_x+z_y.                  \tag{4}
\]

All closed components of (4) are already handled by `f3716b2`: a bipartite
component has its alternating exact switch, while an odd component gives a
localized `2z` pivot.  Hence, after those exits, the component containing a
fan mark is relative.  Complete incidence gives it precisely the two marks
from (3).

## 2. The relative path identity

Write the marked component as an ordered path

```text
E+ = z0 -- z1 -- ... -- z_(2r) = E-.
```

The two marks have the same source-word parity: transposition changes which
endpoint carries the head, not the common residual word.  The path length is
therefore even.  Alternately add and subtract its rows:

\[
 \sum_{i=0}^{2r-1}(-1)^i(z_i+z_{i+1})=z_0-z_{2r}
                                                =E_+-E_-. \tag{5}
\]

This is an integral row identity.  The internal-column restriction of a path
has full column rank, so (5) is not disguising a same-star lock dependence.
It is the genuine relative alternative.

Equation (2) now follows from the already existing bar.  Together with the
signless endpoint row

\[
                              S=E_++E_-,                \tag{6}
\]

the endpoint determinant is `-2`; over the complex source field, `S,D`
isolate the two endpoint orientations.  This is precisely the four-coordinate
gate of `744cd9a`, now identified as the endpoint of the bidirectional Hall
path.

## 3. The exact holonomy boundary

Physical incidence is not enough.  If a literal row is

\[
                             a_i z_i+b_i z_{i+1},       \tag{7}
\]

the dual propagates by

\[
                 \lambda_{i+1}=-(a_i/b_i)\lambda_i.   \tag{8}
\]

For an even marked path, (5) belongs to the row span exactly when

\[
                           \lambda(E_+)=\lambda(E_-).  \tag{9}
\]

Equal common matching tails make `a_i=b_i` and force (9).  One unequal tail
may violate it.  The checker freezes a six-edge path using all five row
types

```text
unary, 11, 12, unary, 21, 22
```

with distinct physical ports assigned to `12` and `21`.  All rows have
weights `(1,1)` except the middle unary row, which has `(1,2)`.  The internal
five-column lock matrix has rank five, the two crossed rows have no shared
port, and the propagated endpoint values are

\[
                         \lambda(E_+)=1,
                         \qquad\lambda(E_-)=\tfrac12. \tag{10}
\]

Therefore `D` is not in the row span.  Equalizing the one tail changes the
right value in (10) to one and recovers (5).

This is an exact rational source-labelled lock-module guard.  It is not a
physical common-`q` GHZ source.  Its purpose is to show that the load-bearing
hypothesis is literal cofactor equality, not the presence of all five
aggregate row names or the abstract Hall graph.

## 4. Hasse--Bianchi equation (3) has the right shadow but not the lift

The reciprocal Hasse--Bianchi identity of `b7f5856` is

\[
 D_{kl}E_{ij}-D_{ij}E_{kl}
 =d_{ij}\delta_{kl}X_k-d_{kl}\delta_{ij}X_i.           \tag{11}
\]

For the off-diagonal direct cell `d=-E_10` and a diagonal row `cc`, its
left side has the degree-zero endpoint-orientation shadow `D` in (1), while
its right side is `-X_c`.  The checker replays all three choices

\[
                         c=0,1,2,                       \tag{12}
\]

and each target is nonzero.  Hence (11) cannot be read as an existing source
boundary: if both residual insertions lifted to tangent variations of the
full unary/four-response fibre, both derivative defects on the left would
vanish, contradicting (12).

The bidirectional fans do not cure this.  They land nonzero
determinant/cofactor **values** in degree zero through (3).  They do not
construct corrected source variations with

```text
q-dot = r_cc   or   q-dot = r_10
```

while simultaneously killing the unary and all four response derivatives.
Thus Hasse--Bianchi supplies exactly the desired curvature shadow, but the
same tangent-lift obstruction persists.  In the four-coordinate quotient it
raises the formal rank from two to three; in the physical source-row image it
does not adjoin `D`.

## 5. Fastest remaining lemma

The residual is now a single source-provenance statement, not another rank or
Hall classification:

> In the marked component of the two transposed fans, every unequal,
> unmatched, or wrong-parity full-row occurrence either routes to a proved
> endpoint/direct-cell, crossed-wedge, or localized-unit branch, or supplies
> a corrected tangent lift of one Hasse direction.  Otherwise all rows have
> equal common-tail provenance, and (5)--(2) construct `A`.

A successful proof may be phrased either as literal tail synchronization or
as a connection/Kodaira--Spencer lift for (11).  The calculation above shows
that these are the same endpoint-holonomy obstruction.  Merely invoking
ordinary differentiation, aggregate row cancellation, or physical Hall
incidence does not resolve it.

## Verification

Run

```text
python3 computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py
python3 -O computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py
python3 -I -S computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py
```

The checker pins the two transposed source identities, the five-lock and
signless Hall theorems, the four-coordinate attachment gate, and the typed
Hasse--Bianchi identity.  It audits equal-tail relative paths, closed-cycle
certificates, the exact all-five unequal-tail guard, and the distinction
between formal curvature shadow and physical tangent lift.
