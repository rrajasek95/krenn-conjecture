# Two-gate resolution sketch

Audit date: 2026-08-12.

This note is the shortest route through the **canonical six-site core**
after the exact `15=1+9+5` occurrence split and the active-fan coloop
theorem.  It is a proof programme, not a claim that the two gates below are
already proved.  More importantly, these two gates do not by themselves
cover every synchronized ternary packet: a separate global-coverage theorem
is required in Section 4.

## 1. The canonical core is complete outside two gates

Assume that the global clean-point problem has already entered either a
synchronized one-bad packet or the corresponding rootless/inactive collision
chart, and choose a representative by

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
this canonical core needs only the following two gates.

## 2. Gate I: one protected physical comparison and anchor law

For the determinant-dark cut profile, the complete lower Hasse face has

```text
18 direction-labelled terms,
15 physical collision labels,
3 shared labels,
12 nonzero collision coefficients.
```

Their input geometry is now simpler than three independent equations
(`47582d4`).  On the fifteen-label quotient the lower face is

\[
                   (\rho-1)u_{012},\qquad \rho=(1\;4),
\]

with seven two-cycles and one fixed point.  The shared labels are one fixed
point and one two-cycle, so any genuinely `rho`-equivariant comparison
satisfies all three overlap coherences automatically.  The transposition is
not itself physical in the fixed source word: it changes `001122` to
`021102`, and every physical cut transport needs at least two local colour
repairs.  Thus Gate I has reduced from fifteen independent images to one
target-cancelled **two-local-root Cartan--Spencer attachment** and its
equivariant translates.

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

For the constructive Route A, one independent row law remains: the physical
pure/target anchor must see the corrected kernel.  It is enough to prove one
of:

1. `ainc` transports separately modulo the protected rows;
2. fine grading makes `ainc` kill the collision correction; or
3. direct evaluation gives a nonzero anchor value.

Then the rectangular interference theorem gives either a rank-two localized
source unit or a unit-coordinate kernel absorbed by the same physical
terminal alternative.

This separate anchor law is **not** a prerequisite for the rootless
generator/Fredholm dichotomy in Route B.  Once `Phi` is physical on the
complete protected domains, `7efd10d` already resolves either value of the
physical terminal defect.  The inactive extension must still identify the
physical cap/anchor coordinate on its own normal faces, but the rootless
branch should not be delayed by the constructive anchor pairing.

This is the highest-leverage construction because it closes the rootless
comparison immediately, supplies the common input for the inactive
extension, and leaves only the separate anchor law when one also wants the
constructive determinant-dark entry.

## 3. Gate II: saturated affine accessibility for a fan coloop

Let one edge of a source-provenant active fan be a pure-colour coloop.  The
complete later target-coloop chain, punctured-C4 theorem, and conjugate
double-coloop theorem fully consume a coloop once it has the normalized
common-`q`, endpoint-port, and response-head typing.  The earlier multisite
affine handoff in `0556512` is superseded inside that normalized chain.
Accordingly the live gate is normalization of an arbitrary fan coloop, not a
new branch after normalization.

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

The purely combinatorial termination statement is now exact (`32e07b5`).
The `5,141` cross-intersecting six-site inputs have `446` saturated closed
concepts and only six types modulo site symmetry and shore swap; every new
typed hole strictly enlarges the closure.  Thus there is no iterative Hall
cycle once the physical rows realize the saturation.  The intended output
is immediately one of

```text
target-line concentration,
four-good active pair,
anchor-safe support deletion,
anchor-preserving star/triangle/rectangle relation.
```

The load-bearing missing statement is now exactly the **complete-row
tight-set lift**: the common matroid covector or the next exchange must be
represented by complete physical rows with the correct word, common-`q`
tail, endpoint orientation/head, fine grade, and mutual-anchor protection.
Pure matching matroids alone do not prove this.  Once such a lift exists,
the target-augmented circuit theorem (`b6775b0`) turns an internal placed
Cartan direction into a normalized affine exchange or homogeneous
connector, while an external direction gives a target-dark separator.  Its
remaining independent condition is visibility of the target circuit under
the physical anchor row.

## 4. Global coverage: one of two routes must still be completed

The two local gates become a proof of the conjecture only after one of the
following exhaustive coverage routes is proved.

### Route A: uniform constructive entry

Starting from an arbitrary synchronized maximum-anchor/minimum-support
packet, prove that complete source rows either produce an active clean pair
directly or enter the canonical six-site fork above.  This includes the
uniform source-connectivity/endpoint-word theorem for long alternating
components and a well-founded decrease for affine/Hall returns.  Gate II is
the normalized coloop endpoint of this route; it is not a substitute for the
entry theorem.

### Route B: exhaustive rootless/inactive comparison

Use the proved gcd split: every line with no active clean zero is either
rootless on one chart or has roots which are all inactive.  Gate I supplies
the finite physical comparison required by the rootless branch only after
its anchor law is checked.  The same comparison must then:

1. extend over every normal face of the inactive zero locus, including the
   complete order-two/order-three Hasse companions;
2. identify derived `Yw` with physical `W` and the normalized chain with the
   physical inactive cap coordinate; and
3. support the final horizontal rootless/inactive comparison and the still
   open diagonal inactive Rees routing.

The derived normal systems are already complete.  What remains is physical
comparison and diagonal routing, not another support-stratum census.

Route B is presently the logically shortest global path because it is
already exhaustive and does not require proving uniform entry into the
one-bad normal form.  Route A remains valuable because its accessibility
theorem also supplies the source provenance and rank landing used inside
the comparison.

## 5. Conditional assembly

Assume Gates I and II and either global Route A or global Route B.

1. Use the chosen global-coverage route to reach the canonical collision or
   active-fan packet.
2. The determinant-dark/collision branch is closed by Gate I and the
   rectangular/terminal alternative.
3. The determinant-bright branch gives four-good or a coloop; Gate II closes
   the coloop.
4. A support-deletion output contradicts minimum support.  A physically
   typed generator or separator closes the exhaustive no-active branch.
   Otherwise a four-good active pair exists.
5. Apply the proved clean-cap descent, reducing the even order by two.
6. Repeat the maximum-anchor/minimum-support normalization and reach the
   proved six-site contradiction.

Accordingly the conjecture is not “a few finite cases” from completion.  Its
canonical core is two structural source-typing theorems from completion:
Gate I is one equivariant two-root comparison on a fifteen-label quotient,
and Gate II is a finite saturated exchange graph plus one complete-row
covector lift.  Globally, one
additional coverage theorem remains: uniform constructive entry, or the
inactive extension and diagonal routing of the exhaustive dual route.

## 6. Parallel attack

The work can proceed independently.

* **Comparison lane:** construct (1) and its literal mapping-cone image
  first.  Treat the separate anchor law as a constructive-Route-A add-on,
  not as a blocker for rootless Fredholm.
* **Accessibility lane:** prove coloop normalization and the saturated
  source-typed tight-set alternative.
* **Coverage lane:** first try to extend Gate I over all inactive normal
  faces and finish the diagonal Rees route.  In parallel, record exactly what
  would be required for uniform constructive entry, but do not silently use
  it.
* **Adversarial lane:** attempt the smallest complete-source counterguards to
  the gates and their global promotion; projected matrices, bare matching
  supports, or chart-only terminals do not count.

No further extra-cell census or flat-cycle classification should be started
unless it directly tests one of these gates or their global-coverage
promotion.
