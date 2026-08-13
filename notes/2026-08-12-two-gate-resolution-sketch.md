# Two-gate resolution sketch

Audit date: 2026-08-12.

This note is the shortest conjecture-level route after the exact
`15=1+9+5` source-entry split and the active-fan coloop theorem.  It is a
proof programme, not a claim that the two gates below are already proved.

## 1. The global spine is complete outside two gates

Assume a counterexample and choose a representative by

```text
maximum protected mutual anchors,
then minimum occupied scalar support.
```

The established circuit-cover and lift trichotomy attach every unwanted
occupied cell to the protected anchors by a primitive frame circuit.  There
are only three source types.

1. A squarefree circuit with a common tail enters one complete matching
   coefficient.
2. Failure of a tail is a Tutte/Hall accessibility barrier.
3. A repeated physical site is a Cartan--Spencer collision face.

At six residual sites the complete occurrence profile splits as

\[
              \mathbb Q[\mathcal M_6]
                =\mathbf1\oplus C_{\rm cut}^{0}\oplus D_{\rm alt},
              \qquad15=1+9+5.
\]

The centered cut sector has the constructive filtered cycle `(v,-v)`.  A
determinant-bright zero mixed row has a nonzero offdiagonal cell, hence a
source-provenant private-site fan.  Complete pure target supports make that
fan four-good unless one edge is a literal pure-colour coloop.  Therefore
the final proof needs only the following two gates.

## 2. Gate I: one protected physical comparison and anchor law

For the determinant-dark cut profile, the complete lower Hasse face has

```text
18 direction-labelled terms,
15 physical collision labels,
3 shared-label coherence equations,
12 nonzero collision coefficients.
```

Construct one source-valid comparison

\[
             \Phi:U_{15}\longrightarrow L_{h=3},
             \qquad J_3\Phi=A J_{\rm col},             \tag{1}
\]

whose one-face image is the already isolated literal mapping-cone packet:
the endpoint-odd `360`-term full-nine aggregate, Eq signature `-delta`, zero
protected target rows, and the prescribed eta/sigma terminal.  Equality on
the three shared labels is exactly the descent condition from the two cut
charts to the physical collision quotient.

Equation (1) does two jobs at once.

* It nullhomotopes the lower collision face of the determinant-dark filtered
  cycle, producing the complete marked kernel.
* It is the protected rootless/inactive comparison needed to define the
  physical polar map.

Exact terminal equality is unnecessary.  The proved quotient alternative
states:

```text
q-Phi defect nonzero on protected kernel -> physical relative generator;
q-Phi defect zero                       -> q transports -> Fredholm.
```

One independent row law remains.  The physical pure/target anchor must see
the corrected kernel.  It is enough to prove one of:

1. `ainc` transports separately modulo the protected rows;
2. fine grading makes `ainc` kill the collision correction; or
3. direct evaluation gives a nonzero anchor value.

Then the rectangular interference theorem gives either a rank-two localized
source unit or a unit-coordinate kernel absorbed by the same physical
terminal alternative.

This is the highest-leverage construction because it simultaneously closes
the determinant-dark source entry and both downstream comparison maps.

## 3. Gate II: saturated affine accessibility for a fan coloop

Let one edge of a source-provenant active fan be a pure-colour coloop.  The
normalized target-coloop, punctured-C4, and conjugate double-coloop packets
are already routed.  Their only general surviving output is the one-shared,
anchor-contained multisite affine/Hall interface.

The intended proof should be one saturated augmenting-path argument, not a
sequence of local case moves.

Fix `q` and the two opposite endpoint rows and form

\[
             L_s(v)=(vs_1q^{[h-1]},vs_2q^{[h-1]}).
\]

Take all literal source-certified common-tail, Cartan, and response
exchanges at once.  They form a finite directed graph on complete endpoint
columns.  Saturate the component reachable from the coloop fan.

* If the reachable component meets the required target-coordinate lines in
  both sequential affine fibres, perform the joint-kernel concentration.
* If it reaches a free active fan, complete pure supports give four-good or
  another named coloop already inside the same saturated component.
* If neither happens, the reachable set is tight for the two endpoint
  quotient matroids.  The matroid-intersection covector must be lifted
  through the complete source rows.  A proportional lift is the proved
  same-row support deletion; a nonproportional lift is another typed
  exchange, contradicting saturation; the remaining cross-intersecting
  shadows are precisely star, triangle, or `K2,2` Hall relations.

This formulation includes termination.  There is no iterative Hall cycle:
all reachable labels were saturated before duality was applied.  The output
is immediately one of

```text
target-line concentration,
four-good active pair,
anchor-safe support deletion,
anchor-preserving star/triangle/rectangle relation.
```

The load-bearing missing statement is source exhaustivity: the common
matroid covector or the next exchange must be represented by complete
physical rows with the correct word, tail, and endpoint labels.  Pure
matching matroids alone do not prove this.

## 4. Assembly

Assume Gates I and II.

1. Apply the source-entry split to the marked frame circuit.
2. The determinant-dark/collision branch is closed by Gate I and the
   rectangular/terminal alternative.
3. The determinant-bright branch gives four-good or a coloop; Gate II closes
   the coloop.
4. A support-deletion output contradicts minimum support.  A generator or
   separator closes the exhaustive no-active branch.  Otherwise a four-good
   active pair exists.
5. Apply the proved clean-cap descent, reducing the even order by two.
6. Repeat the maximum-anchor/minimum-support normalization and reach the
   proved six-site contradiction.

Accordingly the conjecture is not “a few finite cases” from completion.  It
is two structural source-typing theorems from completion.  Both are bounded
enough to attack explicitly: Gate I is a fifteen-label/three-coherence
comparison, and Gate II is a finite saturated exchange graph plus one
complete-row covector lift.

## 5. Parallel attack

The work can proceed independently.

* **Comparison lane:** construct (1), the literal mapping-cone image, and the
  separate anchor law.
* **Accessibility lane:** prove coloop normalization and the saturated
  source-typed tight-set alternative.
* **Adversarial lane:** attempt the smallest complete-source counterguards to
  either gate; projected matrices, bare matching supports, or chart-only
  terminals do not count.

No further extra-cell census or flat-cycle classification should be started
unless it directly tests one of these two gates.
