# The occurrence graph moves the Eq defect to a primitive diagonal

## Result

The derived tensor-product proposal has an exact positive algebraic part,
but it does not construct the physical reduced-Eq cell.  The issue is that
the occurrence graph coordinate and the physical homogenizing target are
different variables.

Write the literal direct-free pure hafnian as

\[
                         H_0=f+G,                           \tag{1}
\]

where `f` is one marked perfect-matching occurrence and `G` is the sum of
the other 89 occurrences.  Let `z` be the private coordinate of the
contractible occurrence graph, and reserve `U` for the physical target
coordinate in the pure source equation.  Then

\[
 E_g=f-z,qquad F_0=H_0-U=E_g+G+(z-U).                \tag{2}
\]

If `a` is the graph presentation generator with `d a=E_g` and the physical
Eq row has

\[
                         d r_0=F_0e_{\rm Eq},                 \tag{3}
\]

the honest tensor-cone element is

\[
 K=r_0-ae_{\rm Eq},qquad
 \boxed{dK=(G+z-U)e_{\rm Eq}.}                         \tag{4}
\]

Thus the hoped-for formula `dK=G e_Eq` silently identifies `z=U`.  That
identification is not part of the contractible occurrence graph: it imposes
the selected-occurrence equation `f=U`, whereas the physical source only
imposes the aggregate equation `H0=U`.

The checker gives a literal direct-free specialization showing the gap.  It
takes the union of two direct-free perfect matchings forming an eight-cycle,
sets its eight edge weights to one and every other pure edge to zero.  The
only surviving hafnian terms are the two alternating matchings, so

\[
                  H_0=U=2,qquad f=1,qquad G=1,qquad f-U=-1. \tag{5}
\]

Consequently `H0-U=0` does not imply `f-U=0`, even on an actual labelled
edge specialization.  The first new obstruction beyond the common Eq
coefficient is the occurrence-to-target diagonal

\[
                         \boxed{(z-U)e_{\rm Eq}.}             \tag{6}
\]

It is primitive, free, and beta-independent.  A physical construction of
`K_Eq(beta)` must supply (6) together with the already certified endpoint,
word, and descent corrections; the bare occurrence graph does not.

## 1. Exact integral tensor-cone module

Retain the three boundary coordinates

\[
       (E_ge_{\rm Eq},\;Ge_{\rm Eq},\;(z-U)e_{\rm Eq}).       \tag{7}
\]

The physical row, graph tensor, honest cone boundary, and hoped-for
boundary are respectively

\[
 r_0=(1,1,1),\qquad ae_{\rm Eq}=(1,0,0),
\]

\[
 dK=(0,1,1),\qquad G e_{\rm Eq}=(0,1,0).               \tag{8}
\]

The primitive covector

\[
                         \lambda=(0,1,-1)                    \tag{9}
\]

kills both available columns in (8), and hence their difference, but reads
one on the hoped-for `G`-only boundary.  The two available columns have a
unit maximal minor; adding the hoped-for column gives determinant `+/-1`.
Therefore the obstruction is a primitive free cokernel, not a torsion class.
Base change to `Z[beta]`, localization at nonzero beta, or specialization at
beta zero does not remove it.

There are only three interpretations of the ambiguous symbol `u` in the
informal graph formula `H0=u+G`:

1. `u=z` is the private graph coordinate.  Then (4), rather than
   `dK=G e_Eq`, is the correct boundary.
2. `u=U` is the physical target.  Then the graph equation is `f-U=0`,
   refuted by (5).
3. `G` is defined to be `H0-U`.  Then `dK=G e_Eq` simply restates the
   original Eq defect and performs no reduction.

This is why the formal Koszul calculation looks correct after forgetting
the origin of `u`: that forgetting identifies precisely the two coordinates
whose comparison is the missing theorem.

## 2. What a physical diagonal comparison must carry

The complete Hasse/Koszul and collision inventory already determines the
cost of promoting (6).

The smallest source-labelled endpoint word-change bar has

\[
 B_{v,N}=(-\Omega_v,+q_{v,N};
          W=\operatorname{ainc}=\operatorname{tgt}=0,
          \operatorname{ores}=1).                      \tag{10}
\]

Thus a physical occurrence-to-target comparison cannot be a bare scalar
face: its first realization carries the primitive endpoint ridge
`Omega_v`, a labelled companion, and ordinary residue.

The order-four Hasse top has the right scalar unit, but its physical audit
is

```text
source-valid                         false
endpoint-ridge space rank            6
primitive Omega rank                 5
selected midpoint source-word hits   0
fourth operator on H_m               1.
```

So the formal top forces three independent repairs: endpoint-ridge
homotopies, a residual-word comparison, and a source-valid descent of the
unit top.  Equality of its scalar coefficient with the desired face does
not supply any of them.

At the first repeated `P3 + K2` comparison degree, adjacent endpoint/rootless
faces have

\[
 dS_{vw}=C_v-C_w+\delta_{vw}(H_0-U)e_{\rm Eq}.          \tag{11}
\]

The last term in (11) requires the already isolated zero-anchor reduced-Eq
face; the primitive functional `pure Eq + physical ainc` separates it from
the complete bounded full-nine/cap correction module.  Even after formally
granting all five such faces, the clean `C_v-C_w` boundaries form the
oriented `C5` incidence lattice of rank four and leave the primitive
aggregate

\[
                              \sum_v C_v.                    \tag{12}
\]

Hence the occurrence graph does not bypass the collision program.  It
locates the next cell more sharply: a source-labelled occurrence-to-target
diagonal comparison in one word/fine/repeated grade, with zero net target,
ordinary residue, `W`, and anchor, whose ridge and word faces totalize and
whose transported comparison has nonzero aggregate (12).

## 3. Consequence for `K_Eq(beta)`

The common odd/even/Bockstein coefficient remains

\[
                         E=(H_0-U)e_{\rm Eq}.                 \tag{13}
\]

The graph calculation does not refute the three-projection theorem.  It
rules out one proposed construction of it.  A valid integral family must
contain more than the derived tensor product of the contractible occurrence
graph with the Eq presentation: it must also construct the diagonal (6) as
an actual physical comparison, with the complete corrections listed above.

If that diagonal is supplied, equation (4) genuinely reduces the Eq face
to the nonselected-occurrence aggregate `G e_Eq`, and the existing
endpoint/collision maps state exactly what remains to transport it.  Without
it, writing `dK=G e_Eq` is a source-invalid identification, not a new
boundary.

This result does not exclude a larger source resolution containing the
diagonal comparison, and it does not construct `K_Eq(beta)`.

## Verification

Run

```text
python3 computations/verify_h3_reduced_eq_occurrence_graph_tensor_gate.py
python3 -O computations/verify_h3_reduced_eq_occurrence_graph_tensor_gate.py
python3 -I -S computations/verify_h3_reduced_eq_occurrence_graph_tensor_gate.py
```

All modes print ledger digest
`462cc0b1fbf4508be717109daef03acd0ad2038143c7455a16856cab3dc907ff`.
