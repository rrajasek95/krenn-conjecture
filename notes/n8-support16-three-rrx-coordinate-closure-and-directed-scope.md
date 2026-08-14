# Closing the four support-16 seal-three coordinate branches

This note closes the four three-`RRX` graph orbits left by
[`n8-support16-two-rrx-coordinate-mixed-closure.md`](n8-support16-two-rrx-coordinate-mixed-closure.md)
under the same mutual-coordinate anchor hypothesis.  It also audits exactly
how far the arbitrary directed noncoordinate-anchor landing extends in the
22 two-`RRX` orbits, and freezes the finite incidence set it does not reach.

The exact checker is
[`verify_n8_support16_three_rrx_coordinate_closure_and_directed_scope.py`](../computations/verify_n8_support16_three_rrx_coordinate_closure_and_directed_scope.py).

## Outcome

The four seal-three orbits have no surviving mutual-coordinate completion:

```text
canonical completions modulo global S3       104,950
full-colour completions                       629,700
immediate mixed Laurent units                 104,802
one/two-binomial singleton closures               144
full support-CNF UNSAT closures                     4
survivors                                           0
```

The last four are all in the regular orbit of size `2520`.  They are not
numerical counterguards: the literal necessary nonzero-support consequences
of all `3^8` rows are UNSAT over every field.

For arbitrary directed anchors in the 22 two-`RRX` orbits, the exact local
statement is:

> A noncoordinate near vector on either marked private response edge of a
> two-`RRX` cubic/high face supplies an active rank-one cap immediately.

Cubic-incident blocks are already same-colour coordinate blocks.  Across the
22 representatives there are 488 directed incidences on the remaining
high/high edges.  Of these, 112 occur as marked private response roles in at
least one two-`RRX` face and are therefore landed by the theorem.  The other
376 form the exact finite unlanded directed-incidence register.  They include
shared roles invisible to the selected quadratic and anchors at high stars
not adjacent to a cubic cap.  No theorem here silently coordinates them.

## 1. The three-term matching map

At each selected degree-four--degree-four cap `pq`, the external shores have
the form

```text
P=N(p)-q={h0,h1,a},        S=N(q)-p={h0,h1,b}.
```

They overlap in `h0,h1`.  The two remaining physical vertices carry one live
edge `x`.  There is no `RRR` term and the three `RRX` terms are exactly the
three perfect matchings on `{h0,h1,a,b}`:

\[
 E_K=x\bigl(
 r_{h_0h_1}r_{ab}
 +r_{h_0b}r_{ah_1}
 +r_{h_0a}r_{h_1b}
 \bigr).                                                \tag{1}
\]

Thus (1) is the pullback of the three-term four-vertex matching
quadratic—the hafnian analogue of a `2x2` permanent, with the third pairing
retained.  The checker reconstructs the literal residual matchings for all
four representatives and verifies that the same `x` edge tags every term.

There is a useful scalar rank-stratum principle behind (1).  Once all six
response blocks are rank-one anchors, (1) becomes one scalar homogeneous
quadratic `q(K)` times nonzero far-coordinate factors.  Let `L` be the product
of the direct activity form and the three diagonal cap readouts.  Over
`C`, `q=0` has an active point unless every irreducible factor of `q` is one
of the protected linear factors of `L`; equivalently, the only scalar
exceptions are

\[
                  q=c\ell_i^2\quad\hbox{or}\quad
                  q=c\ell_i\ell_j.                    \tag{2}
\]

Indeed, if `V(q)` lies in the finite union `V(L)`, every irreducible component
of the quadric lies in one of those hyperplanes, so unique factorization gives
(2).  Otherwise a zero of `q` avoids all protected hyperplanes.  The mixed-row
census below closes the coordinate specializations, including the monomial
exceptions (2), without assuming a generic rank.

## 2. Complete mutual-coordinate census

An edge state is either a live unrestricted wildcard block `*`, with all nine
cells granted, or a nonzero scalar mutual coordinate anchor `0,1,2`.  Every
vertex must see all three anchor colours.  No local anchor placement is fixed:
the enumeration includes a wildcard cap, an anchored cap, and every possible
choice of the one optional nonanchor at either degree-four endpoint.

The global colour action is removed canonically.  Reading the support edges
in their fixed order, the first new anchor colour must be `0`, the next `1`,
and the next `2`.  Every full assignment has all three colours, so each `S_3`
orbit has exactly one representative.  The exact per-graph ledger is

| graph orbit | canonical | immediate | sparse | support-CNF |
|---:|---:|---:|---:|---:|
| 360 | 19,860 | 19,856 | 4 | 0 |
| 840 | 30,313 | 30,265 | 48 | 0 |
| 2,520 | 27,227 | 27,155 | 68 | 4 |
| 10,080 | 27,550 | 27,526 | 24 | 0 |

The immediate column is a mixed coefficient with one anchor-only matching,
so it is a Laurent unit required to vanish.  The sparse column uses the exact
propagation

\[
 A+X=0,qquad A\ne0\quad\Longrightarrow\quad X\ne0,
\]

followed after one step in 52 cases and two steps in 92 cases by a singleton
mixed monomial made entirely of known nonzero factors.

## 3. The last four and the full support-CNF

Sparse propagation stalls on four orbit-`2520` completions.  For each, the
checker builds a Boolean variable for every cell of every wildcard edge and
an auxiliary activation variable for every supported matching monomial.  It
then records only necessary consequences of an exact complex source:

1. an auxiliary is true exactly when all wildcard cells in its monomial are
   nonzero;
2. every wildcard support edge has at least one nonzero cell;
3. every pure coefficient has at least one nonzero matching monomial; and
4. a zero mixed coefficient cannot have exactly one nonzero matching
   monomial.

Condition 4 is weaker than the coefficient equation: two or more nonzero
terms are merely allowed to cancel.  Therefore UNSAT of this Boolean system
is a source-valid exclusion over arbitrary complex values.

The CNFs are checked by an in-file watched-literal DPLL.  It performs unit
propagation, branches on every unresolved base cell in both truth values, and
then branches on any remaining auxiliary; watches persist under standard
backtracking while the assignment trail is restored.  Small SAT and UNSAT
calibrations are checked independently, and every returned SAT calibration
is evaluated against every clause.  All four physical CNFs return UNSAT.

This is not a claimed full-source counterexample or a numerical search.  The
four guards fail before coefficients, ranks, or pure normalization values are
chosen.

## 4. Exact directed noncoordinate landing

For a two-`RRX` cubic/high face, the cubic endpoint supplies same-colour
coordinate blocks by the cubic-vertex lemma.  At the high endpoint the two
private response roles enter

\[
 F=a_0\otimes b_1+a_1\otimes b_0.
\]

If an anchored private block is `w tensor e_r` and `w` is noncoordinate, the
rank-one cap factorization supplies an active zero by choosing its right
vector in `ker(w)` while avoiding the protected activity hyperplanes.  This
is the already proved `anchored_near_vector_noncoordinate` rank stratum, now
checked at every literal face.

What it does **not** see is equally precise:

* the high endpoint's shared edge does not occur in the two crossed response
  pairings, so a noncoordinate near vector there is invisible to this `F`;
* a high/high edge not serving as a private response edge of any cubic/high
  two-`RRX` face is not landed; and
* a coordinate near vector with a different far endpoint label is a directed
  coordinate anchor, not a mutual same-colour anchor, so it is outside the
  mutual-coordinate census even though it is not part of the noncoordinate
  register.

The checker enumerates the first two bullets as directed pairs `(vertex,
edge)`, not as undirected support edges.  The totals are

```text
eligible directed high/high incidences      488
marked private roles, hence active-landed   112
finite unlanded directed incidences          376
```

For the two first support-16 graph orbits the records are

```text
orbit 60:  20 eligible, 8 landed, 12 unlanded
orbit 240: 20 eligible, 6 landed, 14 unlanded.
```

This is the sharp terminal alternative requested by the scope audit.  To
promote the support-16 coordinate closures to arbitrary exact-source closures,
one must either land one of these 376 directed incidences into a marked
private role by another cap, or prove that the three forced anchor colours at
each high vertex can be selected outside this register.  The present result
does not assume either statement.

## Reproduction

```sh
python3 computations/verify_n8_support16_three_rrx_coordinate_closure_and_directed_scope.py
python3 -O computations/verify_n8_support16_three_rrx_coordinate_closure_and_directed_scope.py
python3 -I -S computations/verify_n8_support16_three_rrx_coordinate_closure_and_directed_scope.py
```

The frozen ledger digest is
`edbbb640025dc393887eae711e218173bfea019a64ea58e2127dd8a7f618975f`.
