# Proof-first endgame after the order-six audits

## 1. The global spine

The conjecture-level argument should remain organized around the already
proved descent spine

\[
 \text{minimum counterexample}
 \longrightarrow
 \text{maximum-anchor/minimum-support packet}
 \longrightarrow
 \text{active clean pair}
 \longrightarrow
 \text{exact }(N-2)\text{-vertex descent}
 \longrightarrow
 \text{the proved six-site contradiction}.
\]

The only dashed arrow is the production of the active clean pair.  The many
local audits should be read as evidence about that arrow, not as independent
lemmas which must all be iterated in the final proof.

The shortest plausible proof has two new structural inputs:

1. an **augmented interchange alternative**, which produces the physically
   typed residual comparison or turns its obstruction into a terminal class;
2. a **transverse landing theorem**, which turns the resulting carrier into
   a clean pair or a support-reducing dependence.

Everything after these two statements is already formal or proved.

## 2. Structural theorem I: augmented interchange alternative

Let `C_phys` be the literal source-labelled complex in the repeated
`P3+K2` grade.  It must retain physical word, chart, target, ordinary
residue, `W`, and anchor rows.  Let

- `Theta_6` be the complete order-six Hasse source cycle;
- `gamma_v=-dOmega_v` be the shifted endpoint/ridge first jet; and
- `K_v` be the relative mapping cone of the physical source inclusion in
  this grade.

The desired local statement is:

> **Augmented interchange alternative.**  The endpoint principal-parts
> differential and tail covariance define a square in the complete physical
> labelled complex.  Its total class either has a representative `M_v` with
>
> ```text
> source boundary = 0,          residue = -delta,
> D = W = target = anchor = 0,
> eta_z = 1 + delta_(vz) u_z/t, sigma = -q_pq:22,
> ```
>
> or its obstruction class in `H_1(K_v)` has nonzero physical terminal
> readout and therefore normalizes to the required relative generator.

This statement is deliberately an alternative.  It is unnecessary to prove
that every formal Spencer face vanishes.  A nonzero obstruction is useful if
the physical terminal sees it; if the terminal kills the obstruction, the
comparison descends and the Fredholm construction is well defined.

### Constructive proof sketch

1. Work first in the universal principal-parts/Hasse bicomplex, before
   quotienting by physical matching rows.
2. Put tail covariance in one direction and endpoint principal parts in the
   other.  Equality of mixed coefficient operations gives the strict
   commutator relation on the universal complex.
3. Filter by repeated-site degree.  `Theta_6` is the source face and
   `gamma_v` is the terminal ridge face of one total cycle.
4. Prove that the kernel of the map to the physical labelled complex is a
   filtered subcomplex.  This is the real descent assertion: complete source
   rows, rather than individual matching monomials, must be stable under both
   differentials.
5. The induced long exact sequence gives the alternative above.  A zero
   connecting class supplies `M_v`; a nonzero class is tested by the physical
   anchor/terminal readout.
6. Verify `W`, target, ordinary residue, and anchor on the total cycle, not on
   a chosen sparse representative of `Theta_6`.

The universal part of steps 1--3 is now closed by the
[Spencer Euler contraction](h3-universal-spencer-euler-contraction.md).
For normally ordered differential symbols, successive coefficient faces are
the polynomial de Rham differential, and contraction with the Euler field
gives `dH+Hd=1` in every positive total degree.  Thus no further universal
Spencer layer can obstruct.  Step 4—the physically labelled comparison and
its relative homology—is the whole remaining local content.

The existing computations support this outline.  The order-five defect has
an exact repair, the complete order-six Hasse tower exists, and tail
covariance commutes with the ridge jet on all 8,580 eligible operators.  An
exact 343-term affine representative also kills every first
coefficient-prolonging face.  A diagnostic imposing both the first and
second faces has modular rank jump `8102 -> 8103`; this is evidence that a
single order-six representative is too small, not yet a characteristic-zero
no-go for the total bicomplex.  Universal Spencer acyclicity proves that the
correct target is the connecting morphism in step 5 rather than further
face-by-face enumeration.

There is now a second formal reduction on the augmented side.  Let `s`
interchange the two endpoint orientations and let `H_w` be the universal
tail-colour Weyl prism.  The
[endpoint-odd Cartan lemma](h3-endpoint-odd-cartan-prism-augmentation.md)
gives

\[
 K=(1-s)H_w,
 \qquad dK+Kd=(1-s)(w-1).
\]

Its boundary is the exact four-corner `-delta` packet.  Every protected
readout `D`, `W`, target, anchor incidence, and pure-Eq aggregate is
endpoint-even, hence kills `K` identically.  This does not construct the
physical source-labelled root contraction, but it removes all five
protected readouts as separate descent problems.  Step 4 above should now
be read as a single source-comparison theorem plus the already commuting
eta/sigma ridge factor, not as five independent cancellation lemmas.

The source-side sign totalization is now closed as well.  The
[Hasse coproduct theorem](h3-hasse-coproduct-cosimplicial-totalization.md)
retains the six derivative occurrences as labelled slots.  Their Boolean
Hasse coproduct is coassociative, so its reduced cobar differential has the
canonical alternating signs and squares to zero.  Symmetrizing the slots
gives exactly `down(L_(k+1))=(6-k)L_k`, including repeated derivative
directions.  Since Hasse translation is an algebra map, complete source rows
and all their polynomial multiples stay in the principal-parts source
resolution.  Thus neither alternating signs, higher-face compatibility, nor
product-rule source closure remains part of step 4.  Step 4 is strictly the
comparison from this canonical source resolution to the physical augmented
correction complex and the interpretation of its terminal readout.

### Dual proof sketch

Instead of constructing `M_v`, compute the obstruction class in the relative
cone.  There are then only two physical outcomes.

- If the terminal is nonzero on correction homology, normalize that class;
  it is already the relative generator.
- If the terminal kills correction homology, it descends to the cokernel.
  The augmented Fredholm alternative produces either the corrected generator
  or the terminal annihilator.

Thus both solvability and nonsolvability can advance the proof, provided the
complex and terminal are physically typed.  A quotient-level or chart-odd
functional is insufficient.

The six-term physical covector makes this alternative stable under the
entire relative extension.  If `J_0` is the complete protected map and `q`
the six-term anchor readout, then either `q` is nonzero on `ker J_0` and
normalizes the relative generator, or `q=lambda J_0` and `(-lambda,1)` is
the physical left separator of every augmented relative column.  Thus no
future bar/Cartan cell needs a separate census.  The only remaining content
is defining `J_0` and `q` in one common physical repeated grade.

## 3. Structural theorem II: transverse landing by augmenting paths

Once the comparison supplies a nonzero common-tail/Fitting carrier, the
remaining problem should be phrased as matroid intersection rather than a
list of star, triangle, and `K2,2` diagrams.

For the two endpoint shores, take the linear matroids of occupied complete
columns after quotienting by their deficient anchor spans.  Form the directed
exchange graph whose edges are source-certified common-tail exchanges.  The
residual comparison supplies the first directed edge.

> **Transverse landing theorem.**  At a maximum-anchor/minimum-support
> representative, a nonzero typed carrier either lies on an augmenting path
> which reaches both deficient endpoint quotients, or the reachable set is a
> tight Hall set whose annihilator gives a complete-column dependence.  In
> the first case the augmenting path supplies the two missing transverse
> heads and hence an active clean pair.  In the second case the dependence
> deletes an occupied cell while preserving the source tensors and anchors,
> contradicting minimum support.

### Proof sketch

1. Contract the already selected anchors and retain the two one-dimensional
   deficient quotient directions.
2. Orient a certified exchange toward the shore whose quotient rank it can
   increase.  Common-tail typing ensures that each edge is a literal source
   move, not merely physical matching adjacency.
3. If the reachable set meets both quotient directions, compose the exchange
   path.  The two endpoint minors are nonzero, yielding the required
   `(3,3)` transverse landing.
4. Otherwise apply the matroid-intersection augmenting-path theorem.  The
   reachable set determines a tight set and a common covector.
5. Lift that covector through the complete source rows.  Proportional columns
   give the already proved anchor-safe deletion; nonproportional columns give
   the typed carrier which enlarges the reachable set, a contradiction.

This formulation explains the observed finite cases.  Stars, triangles, and
`K2,2` webs are the smallest tight sets; off-anchor exits are length-one
augmenting paths; reciprocal five-locks are exchange components which have
not yet been shown to meet a deficient quotient.  Their enumeration is
useful for checking the theorem, but should not be its proof.

It also supplies termination without an ad hoc case potential.  Either an
augmenting path gives the clean pair immediately, or the tight-set dependence
strictly lowers support.  Re-maximizing anchors and re-minimizing support is
the existing global well-founded order.

## 4. Assembly of the conjecture

Assume the two structural theorems.

1. Choose a minimum counterexample and then a maximum-anchor,
   minimum-support representative.
2. Curvature-line selection supplies the selected physical cap packet.
3. Apply the augmented interchange alternative.  A terminal-visible
   obstruction is already the required relative generator; otherwise obtain
   the physical comparison/carrier.
4. Apply transverse landing.  The deletion branch contradicts minimality;
   therefore an active clean pair exists.
5. Use exact clean-pair descent to remove two vertices.
6. Repeat the same lexicographic choice after descent.
7. Reach the proved arbitrary-complex six-site contradiction.

For the downstream rootless/inactive maps, the same physically typed
comparison defines the five columns `P(e_v)`.  The Fredholm alternative then
removes all rank cases.  Only the already isolated horizontal compatibility
and diagonal inactive routing remain; they should not be mixed into the
construction of the local comparison.

## 5. Proper role of computation

Finite computation remains valuable for:

- discovering the correct boundary and terminal signatures;
- verifying universal coordinate formulas;
- testing the smallest tight sets and augmenting paths;
- falsifying an overstrong descent or rank claim; and
- checking that the structural theorem covers every normalized base case.

It should no longer be used to enumerate larger support tiers or successive
Spencer layers as the primary proof.  Those calculations grow because they
are resolving a filtered complex one matrix at a time.  The proof should
identify that complex, use its long exact sequence, and exploit either side
of the resulting homological alternative.
