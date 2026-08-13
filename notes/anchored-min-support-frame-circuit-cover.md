# Minimum support forces an anchor-relative interference circuit through every cell

## Result

Fix an exact ternary GHZ source and choose one nonzero pure perfect-matching
monomial in each colour.  Let `Q` be the resulting twelve selected
endpoint-colour cells.  Among exact sources retaining every cell of `Q`
nonzero, choose one with minimum aggregate support `S`.

Then every occupied non-anchor cell lies in a primitive signed circuit of
the unsigned incidence graph on the site-colour ports `(v,i)`, and every
negative edge of that circuit is a selected anchor.  Consequently the
primitive support has exactly one of the classical frame-circuit shapes:

1. a parallel two-cycle;
2. an even cycle; or
3. two odd cycles meeting in one vertex or joined by a path (an odd
   handcuff).

On an even cycle the primitive coefficients alternate `+1,-1`.  On a loose
handcuff the joining path occurs with absolute coefficient two.  Thus every
occupied optical amplitude is attached to the pure anchors by one of two
interference geometries: an even loop or a coupled pair of odd loops.

This is the support-level circuit cover that the target torus actually
provides.  It is stronger than the existence of some balanced representative
and avoids the false claim that a minimum-support point should degenerate to
one preferred anchored chart.

Checker:
[`verify_anchored_min_support_frame_circuit_cover.py`](../computations/verify_anchored_min_support_frame_circuit_cover.py).

## 1. Relative Stiemke alternative

For a cell `s=(uv;i,j)`, write

\[
                       a_s=e_{u,i}+e_{v,j}
\]

for its unsigned port-incidence character.  Let `A` be the matrix whose
columns are the twelve `a_q`, `q in Q`, and let `q_s` denote the image of
`a_s` in the quotient by `span(A)`.

There cannot be a quotient cocharacter `h` such that

\[
       \langle h,q_s\rangle\geq0\quad(s\in S-Q),
\]

with one strict inequality.  Lift `h` to a port weight annihilating all
anchor characters.  The selected pure matchings imply

\[
       \sum_{q\in Q_i}a_q=\sum_v e_{v,i},
\]

so the lift also annihilates each target character.  The corresponding
target-stabilizing one-parameter subgroup has a finite limit, fixes every
selected anchor cell, and deletes at least one occupied non-anchor cell.
That is another exact source retaining `Q`, with smaller aggregate support,
a contradiction.

Stiemke's strict theorem of alternatives therefore gives

\[
                 \sum_{s\in S-Q}\alpha_s q_s=0,
                 \qquad \alpha_s>0\text{ for every }s.       \tag{1}
\]

Lifting (1) through the anchor span gives coefficients `beta_q` with

\[
       z=\sum_{s\in S-Q}\alpha_s e_s-
                         \sum_{q\in Q}\beta_qe_q,
       \qquad Bz=0,                                         \tag{2}
\]

where `B` is the complete unsigned port-incidence matrix.  Crucially,
`z_s>0` on **every** occupied non-anchor coordinate.  The anchor
coefficients may have either sign.

This argument uses minimum support only within the stratum retaining the
selected anchors.  It is therefore compatible with the maximum-anchor /
minimum-support normalization used by the descent proof; it does not require
a global Hilbert--Mumford basin.

## 2. Every occupied cell lies in a conformal circuit

Fix `s in S-Q`.  Consider kernel vectors of `B` which are sign-compatible
with `z`, contain `s`, and are normalized to have `s`-coordinate one.
Equation (2) makes this polyhedron nonempty.  Choose a vector `c` with
minimal support.

If the columns indexed by `supp(c)` had a kernel of dimension greater than
one, a second kernel vector could be combined with `c` to vanish at `s`.
A sufficiently small positive or negative perturbation would then preserve
all signs and remove another support coordinate while keeping the
`s`-coordinate one.  This contradicts minimality.  Hence `supp(c)` is a
matroid circuit and `c` is its primitive signed dependence.

Because `c` is sign-compatible with (2), every negative coordinate of `c`
belongs to `Q`: all non-anchor coordinates of `z` are strictly positive.
This proves the cellwise anchor-relative statement.

## 3. Why only cycles and handcuffs occur

The circuits of an unsigned graph-incidence matrix are elementary.  A
connected bipartite dependent support contains an even cycle; minimality
forces the support to be exactly that cycle.  A connected nonbipartite
support has full incidence rank, so a minimal dependency has cyclomatic
number two.  Minimality excludes a theta graph because one of its three
cycle pairs is even.  What remains is two odd cycles sharing a vertex or
joined by a path.  Balancing at the path vertices doubles the path
coefficients.

The exact checker reconstructs every minimally dependent simple graph on at
most six vertices.  Six vertices are the first size containing two disjoint
triangles joined by an edge.  It verifies the three shapes and their
primitive rational kernels, and separately checks the parallel two-cycle.

## 4. Connection to the proof frontier

This theorem removes arbitrary support topology from the first half of the
source-exhaustivity problem.  Every selected off-diagonal carrier is already
attached to the pure anchor system by a primitive interference circuit.
Together with the signed-holonomy and Schur results, the intended final
local alternative becomes

```text
odd circuit phase                         -> source unit
even coherent circuit, both amplitudes    -> Schur/Fitting unit
even circuit with a dark Cartan amplitude -> exact circuit potential
```

The remaining task is now sharply **source-homological**, not graph
topological: lift the port circuit to the complete labelled matching-row
complex.  The monomials on a handcuff or even cycle have equal port
multidegree, but they may repeat a physical site and need not be two terms of
one squarefree perfect-matching coefficient.  The lift must therefore come
from the complete principal-parts/bar source resolution (or its physical
dual), not from bare matching adjacency.

Once that lift is supplied, a dark even potential must either give the
already proved same-row support deletion or leave the circuit through a
typed exchange.  Transverse rank landing remains downstream and is not
claimed here.

## Scope

The result is valid for arbitrary complex coefficients, parallel sources
after aggregation, asymmetric endpoint colours, any even number of sites,
and any palette size for which one selected pure matching per colour is
retained.  It proves a circuit in the site-colour incidence/source
multidegree lattice.  It does **not** assert that the circuit itself is a
literal mixed coefficient, that its phase is already fixed by the source
rows, or that its Fitting carrier has transverse physical rank.

Run:

```text
python3 computations/verify_anchored_min_support_frame_circuit_cover.py
python3 -O computations/verify_anchored_min_support_frame_circuit_cover.py
python3 -I -S computations/verify_anchored_min_support_frame_circuit_cover.py
```

Frozen ledger SHA-256:

```text
25fa80c17f9a5488d2f7883d76b39cb8579a281be33afba6d0a92673e15ce82e
```
