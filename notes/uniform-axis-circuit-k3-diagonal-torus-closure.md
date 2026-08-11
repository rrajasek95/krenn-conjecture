# The unary unit closes the full coefficient torus of the primitive diagonal transfer

## Result

The pure-unary attachment unit `efac2b2` is not confined to the displayed
unit weights or to a quadratic with no colour-`2` cells.

1. The nonzero coefficient torus of the seven-edge `k=3` diagonal carrier
   has exactly two invariant characters.  The two literal mixed-response
   cancellations set both characters to `-1`, which is the normalized
   `efac2b2` orbit.  Hence every nonzero weighted realization of that
   support is coordinate-torus equivalent over `C` to the committed chart.
2. The 22-row integral unit uses only source coefficients whose output words
   contain colours `0` and `1`.  It therefore survives **every** decorated
   cell having at least one endpoint colour `2`--the ordered types
   `02,12,20,21,22` on all 28 physical pairs--as well as the already
   arbitrary `00` slice, without one correction term.

Consequently the nonzero primitive three-column diagonal lock cannot occur
in a full one-bad packet.  Its normalized `t=0` fibre is also contained in
the unit calculation; after deleting the response-invisible third star
component, the resulting minimum-support two-column landing is consumed by
the separately committed `k=2` clean closure.  The second-colour internal
slice and the second diagonal/crossed companion rows cannot rescue the
three-column chart: the contradiction already lies in the unary top and the
first aggregate diagonal response.

This closes one complete all-weight chart, not every diagonal lock web.
The remaining theorem must either reduce an arbitrary minimum lock to this
primitive carrier topology, or route an off-diagonal decoration on a
selected anchor edge to the good active overlap.

Checker:
[`verify_uniform_axis_circuit_k3_diagonal_torus_closure.py`](../computations/verify_uniform_axis_circuit_k3_diagonal_torus_closure.py).

## 1. The two response characters

Write the occupied colour-`1` coefficients as

```text
p0, p1, p2,
a12, b02, c56, d25, e36, f13, g14.
```

Include a formal endpoint vertex `P` for the three `p`-components.  The
incidence graph has vertices

```text
P,0,1,2,3,4,5,6
```

and edges

```text
P0, P1, P2, 12, 02, 56, 25, 36, 13, 14.
```

Its unsigned incidence matrix has rank eight.  Since it has ten edges, its
multiplicative quotient has rank two.  A primitive character basis is

\[
 \chi_Y={p_1b_{02}\over p_0a_{12}},\qquad
 \chi_Z={p_2c_{56}f_{13}\over p_1d_{25}e_{36}}.        \tag{1}
\]

The two mixed response coefficients are literally

\[
 p_0a_{12}+p_1b_{02}=0,qquad
 p_1d_{25}e_{36}+p_2f_{13}c_{56}=0.                    \tag{2}
\]

On the nonzero coefficient torus, (2) is equivalent to

\[
                         \chi_Y=\chi_Z=-1.              \tag{3}
\]

Those are the values of the normalized weights

```text
p0=p1=p2=a12=c56=d25=e36=g14=1,
b02=f13=-1.
```

The gcd of the maximal incidence minors is two.  This is the familiar
finite square-root ambiguity of a connected non-bipartite graph, not a new
orbit over `C`: every square has a root.  Thus (3) is sufficient, not only
necessary, for coordinate-torus equivalence to the normalized chart.

The opposite star is supported at one site and carries no additional
character.  Its coefficient and the nonzero pure response coefficient can
be normalized by the endpoint/target diagonal gauges.  Every `00` cell,
and every cell having endpoint colour `2`, is merely carried to another
arbitrary coefficient, so the permitted companion family remains complete
under this normalization.

## 2. Arbitrary cells containing colour 2 do not alter the unit

Adjoin independent cells

\[
 y_{uv}(02),y_{uv}(12),y_{uv}(20),y_{uv}(21),y_{uv}(22). \tag{4}
\]

on all 28 physical pairs to the source system of `efac2b2`.  Rebuild the
literal unary and aggregate-response coefficient rows, then replay the same
22 multipliers.

Every certified row label is a binary `0/1` word.  A cell with an endpoint
colour `2` cannot occur in a matching with such an output word.  Hence every
one of the 22 source generators is unchanged, coefficientwise, and the old
identity remains

\[
                        \sum_{r=1}^{22}m_rg_r=1.         \tag{5}
\]

The checker performs this extension before reconstructing the generators
and expands (5) literally.  It finds 28 arbitrary `z_uv(00)` variables,
140 arbitrary variables of the five types in (4), and zero new defect
monomials.  No second response equation, localization, or nonzero assumption
on any companion cell is used.

## 3. Consequence for the cycle-lock split

For the first genuine three-column transfer, the full-row alternatives are
now strict:

* a simultaneous common-`q` deformation to `k=2` is physically possible
  before the unary equation, as in `c536b88`;
* every nonzero weighting of that carrier support satisfying the required
  cancellations lies in the normalized torus orbit by (1)--(3);
* arbitrary pure-unary cells and arbitrary internal cells involving the
  second companion colour are impossible by (5).

Thus the nonzero `k=3` transfer is empty after unary attachment, while its
support-degenerate `k=2` endpoint enters the already-closed two-column lane;
neither is a surviving diagonal lock in the full one-bad packet.  The
all-weight torus assertion above applies to the nonzero three-column chart.
It does not silently identify an arbitrary response-invisible third star
component with a minimum-support two-column presentation.

What remains is a chart-cover statement, not another coefficient case on
this support.  An arbitrary minimum-support diagonal lock web may have more
occupied carrier cells or a different physical topology, and no theorem
currently reduces it to the ten-edge incidence graph above.  An
off-diagonal `01/10` cell on a nonanchor edge already routes to a good active
pair.  Such a decoration on an anchor edge still needs the alternating cycle
to restore the deleted anchor direction at both endpoints and then a
source-valid distinct-head/rank-completion transport.  Cells involving
colour `2` cannot rescue this primitive chart at all.  This note does not
claim the remaining anchor-edge implication.

## Verification

Run

```sh
python3 computations/verify_uniform_axis_circuit_k3_diagonal_torus_closure.py
python3 -O computations/verify_uniform_axis_circuit_k3_diagonal_torus_closure.py
python3 -I -S computations/verify_uniform_axis_circuit_k3_diagonal_torus_closure.py
```
