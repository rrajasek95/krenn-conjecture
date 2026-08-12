# Proof-first primary theorems

This note reorganizes the frontier around the three statements that would
actually advance the proof. A computation is relevant only when it checks a
base case, proves a bounded classification used below, or falsifies a
proposed implication.

## Theorem A: source-faithful affine accessibility

### Target

For a synchronized maximum-anchor, minimum-support one-bad packet satisfying
the unary equation and all four response equations, every sequential affine
fibre

```text
p_i + ker(v -> (v s_1 q^[2], v s_2 q^[2]))
```

either meets a target-coordinate line anchor-safely, produces a literal free
active carrier and a distinct-head four-good pair, or admits an
anchor-preserving support reduction inside the star/triangle/K2,2 Hall normal
forms. Iteration then reaches the proved concentrated clean-cap or source-unit
packet.

### Proof structure

1. Minimum support makes the occupied complete response columns independent.
   Modulo the target line their coefficients give the unique full-support
   circuit.
2. For three occupied columns the target quotient has rank two, so two
   literal mixed output coordinates have a nonzero 2x2 minor. Select one
   nonzero monomial product in its genuine common-q expansion.
3. If the two selected matchings differ by a typed C4 and have the same
   decorated complementary tail, the target-private identity

   ```text
   p_u G_mix - q_u G_pure
     = q_u + (p_u q_s - q_u p_s) C_s
   ```

   gives a literal active carrier. This step is proved with the common-tail
   and opposite-orientation hypotheses stated explicitly.
4. For unequal tails, decompose the two matchings into alternating
   components. Switching any proper collection of whole components uses no
   new cell and reduces to one cycle. A `C_(2r)` with a nonzero
   distance-three chord shortens source-validly to `C4 + C_(2r-2)`. These
   reductions are proved. The remaining step is to force the chord or enter
   a strict Hall normal form.
5. For a diagonal component, the five-row lock gives either an anchor-safe
   kernel deletion or a complementary crossed wedge.
6. Order the process by total alternating-tail length and then endpoint
   support. Every nonterminal step must lower this lexicographic measure.

### Missing lemma

The unproved step is the **word-synchronized chord-or-Hall lemma**: the
second diagonal and crossed companion rows must synchronize the two
determinant orientations in one decorated word and force a shortening
chord, or force the selected hole families to be cross-intersecting. The
only honest residuals are a chordless synchronized `C6/C8`, an
unsynchronized cross orientation with a changed decorated tail, and the
coordinate-diagonal lock web.

The smallest current endpoint is the single word `00112200` with matching

```text
PS:00 | 05:02 | 14:02 | 23:11.
```

Its common response reduces to

```text
C23 = x01^00*x45^22 + x04^02*x15^02 + x05^02*x14^02.
```

The middle term routes. If `P2:21` is nonzero, its first private coefficient
gives a pure-1 reselection or a free active endpoint; this branch is proved.
Thus the first proof case is the rank-one diagonal return with `P2:21=0`,
not another target-coloop census.

## Theorem B: physical augmented polar or rootless annihilator

### Target

Construct in one physical rootless source complex an augmented correction
map `Jhat` and five labelled mixed-Hessian polar columns

```text
P : k^5 -> coker(Jhat),
```

where `Jhat` includes source boundary, target, and ordinary residue. Then
Fredholm duality gives exactly one useful outcome: a kernel combination of
nonzero pentagon aggregate, which is the corrected relative anchor face, or
a covector `lambda Jhat=0`, `lambda P=epsilon`, which is the terminal
Component-III annihilator. This alternative is proved; no rank case remains.

### Proof structure

1. Construct physical tangents `xi_v, eta_v` in `ker(Jhat)` with the marked
   leading components.
2. Solve `Jhat zeta_v = -Hhat(xi_v,eta_v)`.
3. Prove zero target and ordinary residue and transport the corrected class
   to the v-th pentagon terminal grade.
4. Prove zero indeterminacy by annihilating `ker(Jhat)` at the landing.
5. Apply the generator-or-annihilator alternative.

### Missing lemma

The presentation jets are not physical tangents. After localizing the marked
cells, physical site-Euler tangents and an explicit mixed Hasse correction
do exist, but they are integrable gauge directions. Their conservation law
is now proved. With normalized marked weights and cross-weights `b,c`,

```text
corrected anchor = ordinary residue = (1+b)(1+c).
```

Thus zero ordinary residue forces zero primitive anchor throughout the
site-Euler family. The missing lemma is now the **non-Euler jet theorem**:
in the localized physical tangent module modulo site-Euler gauge, construct
a marked tangent pair with zero residue and primitive corrected anchor, or
prove that a source covector forbids every such pair.

Formal polar, Tate, or presentation-row calculations do not address this
lemma.

## Theorem C: one source-relative comparison couples the branches

### Target

For a synchronized pair with one rootless chart and one all-inactive chart,
construct one source-labelled horizontal comparison cell whose rootless
projection is the physical map `P` from Theorem B, whose inactive projection
is the target-zero radial-to-response transgression, and whose first
indeterminacy vanishes in both projections.

The rootless projection then gives the relative generator or annihilator.
The inactive projection, together with the proved Omega/Bezout and
certificate-bracket prolongation, gives the clean-cap contradiction.

### Missing lemma

The missing object is a physical target/residue-augmented comparison map,
not another rank calculation. Existing principal-parts, Schur, formal Hasse,
and occupancy symbols fail source descent or omit the physical residue
readout. Theorem B should therefore be proved in the same complex intended
for Theorem C.

## Allocation

Proof effort now goes in this order:

1. alternating-tail shortening and Theorem A;
2. the non-Euler jet theorem and the first physical `P(e_v)`;
3. the common comparison map of Theorem C.

Every finite audit must name which proof step it proves or refutes.
