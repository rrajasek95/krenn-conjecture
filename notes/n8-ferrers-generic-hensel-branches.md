# All five Ferrers branches have candidate generic Hensel pivots

## Generic strict-transform smoothness

Let \(P_1,\ldots,P_5\) be the five linear minimal primes of the radical of
the 39-quadratic second-lift obstruction ideal.  At deterministic rational
points of these primes, the exact Jacobian ranks of the 39 quadrics are

\[
 5,\quad 9,\quad 10,\quad 11,\quad 11,
\]

exactly their codimensions.  Pivot normal variables can be chosen as

\[
\begin{aligned}
P_1:&\ 25,26,27,44,46,\\
P_2:&\ 12,13,15,18,19,25,26,44,46,\\
P_3:&\ 12,13,14,15,17,18,19,20,44,46,\\
P_4:&\ 12,13,14,15,17,18,19,20,21,22,44,\\
P_5:&\ 12,13,14,15,17,18,19,20,21,22,23.
\end{aligned}
\]

A nonzero rational minor remains nonzero over the function field of the
corresponding linear branch.  Therefore the scheme cut out by the 39 known
tangent equations is generically smooth on every reduced component.  After
the 196 smooth ambient normal variables are removed, these minors supply
the branch-normal variables for a strict-transform implicit-function test.

There is an important guard: rank alone does **not** prove that every
candidate component lifts to the full mixed fibre.  An additional higher
initial equation could cut its generic point.  A genuine generic lift
follows after proving localized flatness of the Rees deformation relative
to this candidate tangent scheme, or after verifying that all remaining
strict-transform equations vanish once the pivot equations are solved.

## First bend of the \(P_2\) branch

The \(P_2\) prime is

\[
 (a,b,d,e,q_0,q_1,q_3,q_5,q_6).
\]

Although 21 of the 39 cubic mixed tails remain nonzero after the straight
linear restriction, their full 535-term deformation vector is an exact
Jacobian coboundary modulo \(P_2\).  The checker constructs and replays a
369-column lift; its exact module standard basis has 360 elements.  Thus a
quadratic coordinate bend lifts the branch through the first nontrivial
strict-transform order.

For the local pure class \(H_1\), normal elimination by the 196 smooth
directions alone gives term counts

\[
 0, 0, 4, 24
\]

in degrees one through four.  Both its cubic and quartic restrictions to
the straight \(P_2\) branch vanish.  More importantly, after applying the
same quadratic coordinate bend that kills the cubic mixed deformation, the
corrected quartic still reduces exactly to zero modulo \(P_2\).  Hence

\[
 H_1=O(t^5)
\]

on the order-four candidate lift of \(P_2\).  This proves survival and pure
vanishing through the first bend, not the existence of an all-orders
component.

## Remaining all-orders target

The branchwise route now has a precise finite start: all five candidate
components have generic pivot minors, and \(P_2\) survives through its first
bend while preserving pure vanishing.  What is not yet proved is localized
Rees flatness, or that \(H_0\) or \(H_1\) vanishes identically on every
generic formal component that survives.  The next useful calculation is the
strict-transform recursion over each branch function field, retaining only
the codimension-many branch-normal variables.  That is much smaller than
the 252-variable local standard basis and avoids nilpotent intersections,
which are irrelevant for radical membership.

## Reproduction

```sh
python3 computations/verify_n8_ferrers_generic_hensel_and_p2_bend.py
```

All arithmetic, rank minors, module reductions, and lift reconstruction are
exact over \(\mathbb Q\).
