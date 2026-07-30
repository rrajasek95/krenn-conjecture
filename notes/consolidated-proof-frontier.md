# Consolidated proof frontier

Audit date: 2026-07-29.

This is the compact task-allocation map.  The conjecture is still open.
The longer [supersession audit](proof-route-supersession-audit.md) records
why older routes are closed, guarded, or demoted; it should not be read as a
list of independent remaining obligations.

## 1. One missing conjecture-level implication

After selecting three palette colours, write the endpoint-ordered aggregate
matching equation as

\[
                         H_B(A)=\Delta_{B,3}.
\tag{1}
\]

For every even \(|B|\geq8\), the proved spine is

\[
\begin{aligned}
(1)
&\Longrightarrow
 \text{a minimum-entry-support representative}\\
&\Longrightarrow
 \text{a nonzero physical minor and a generically active cap line}\\
&\dashrightarrow
 \text{an active zero of the clean error }{\cal E}_{p,q}\\
&\Longrightarrow
 H_{B\setminus\{p,q\}}(A')=\Delta_{B\setminus\{p,q\},3}\\
&\Longrightarrow
 \text{the proved six-site contradiction after repeated descent and re-minimization}.
\end{aligned}
\tag{2}
\]

The first two arrows are the
[unconditional curvature-line theorem](unconditional-curvature-line-selection.md).
The fourth arrow is the
[exact clean-pair descent](clean-pair-cap-exact-descent-target.md), and the
last arrow uses the
[arbitrary-complex six-site obstruction](../proofs/six-site-arbitrary-complex-obstruction.md).
After each descent one chooses a minimum-entry-support representative at the
new order before applying curvature selection again; equivalently, the
conditional resolution may be phrased as a minimal-order contradiction.
The dashed arrow is the only missing conjecture-level implication on this
spine.  The order-two and order-four cases and all displayed lower
constructions are already complete; order six is the terminal ternary
obstruction.

In particular, the following are not additional top-level obligations:
global flat-fan classification, E1/E2 selection, pairification of every
higher cumulant, or another six-site support census.  They are proved inputs,
superseded targets, or independent ways to attack the dashed arrow.

## 2. Exact split of the dashed arrow

On a selected physical line, failure to find an active clean point has two
exhaustive forms.

1. **Rootless:** the scalar coordinates of \({\cal E}\) have gcd one.  The
   residual Sylvester/Macaulay multiplication map is then surjective.  Its
   abstract rank--gcd algebra is complete; what is missing is a
   source-provenant annihilator built from the literal nine rows.
2. **Roots exist, but all are inactive:** the common divisor is supported on
   the activity divisor.  On the proved diagonal unary--complementary
   subpacket, the interpolation has an exact \(\Omega\)-boundary form and
   absence of an active torus root has the bounded certificate
   \((tu)^{h-2}\in I_\Omega\).  No theorem yet routes every inactive selected
   line into two such subpackets.  Conditional on that routing, the missing
   input is a two-chart physical overlap which makes the surviving
   boundary-polar defect a coboundary.

These are different local ledgers.  A single two-chart theorem may close
both, but that unification remains to be proved.

The label split is also real.  A selected line has the form
\(K_z=E_{ab}+zI\), without a proof that \(a\ne b\).  The off-diagonal
scalar-zero/rootless packet requires \(a\ne b\); the diagonal cell has its
own ternary/binary boundary.  A uniform closure must handle both cases or
prove an off-diagonal selection lemma.

## 3. Rootless selector frontier

In the off-diagonal rootless packet, the two endpoint Rado matroids either
have disjoint bases or they do not.

The independently audited
[automatic two-chart extraction theorem](two-chart-joint-hypothesis-extraction.md)
proves that every rootless selected chart already has an ordinary three-site
selector at both endpoints, including when its selected cell is diagonal.
The split below concerns compatibility between those selectors, not their
individual existence.

* **Disjoint bases:** ordinary Hall data are insufficient.  The missing
  result is a diagonal-anchored own-edge coefficient lift, or an equivalent
  full-nine overlap equation which constructs an annihilator in the
  residual Macaulay quotient.
* **No disjoint bases:** the
  [uniform maximal-shore theorem](uniform-selector-union-maximal-defect-shore.md)
  gives the following exhaustive local boundary list on the complete
  residual ground set.

| Boundary | What is proved | Exact residue |
|---|---|---|
| [Common coloop](common-coloop-clean-cap-affine-fibre.md), \(b=1\) | A five-dimensional clean subspace; after the support-cover/directly-active cases descend, the clean condition on a fixed affine fibre is a degree-at-most-\(h-2\) univariate family of linear systems | Compare the anchor action through \(A=q_0^{[h-1]}\) with the polar-difference action through \(D_{\bar K}(z)\), with the same scalar/response parameters and all three diagonal base loci; this reduction has not yet received a standalone independent audit |
| [Line plus plane](line-plus-plane-shore-clean-cap-pencil.md), \(b=2\) | A whole projective clean pencil; its generic member is active | A kernel line missing one fixed diagonal label, or a rank-one endpoint confined to one fixed row, together with the endpoint-transposed versions |
| [Rank \((1,1)\)](rank-one-rank-one-shore-clean-quotient-plane.md), maximal \(b=3\) endpoint-dark refinement | A four-dimensional clean double-annihilator plane; its generic member is active | A fixed coordinate row/column, or \(a=\lambda x^{\mathsf T}+y\mu^{\mathsf T}\); without a coordinate gate, the scalar gate is already impossible for \(b\leq2\), while overlaps of the gates remain unclassified |
| [Endpoint-dark shore](endpoint-dark-shore-consecutive-power-jet.md) | Every fully dark contraction factors the fixed target through one literal consecutive-power cofactor map | A kernel/target separation in the one-bright four-site jet; two-site compatibility is needed only if every one-bright jet stays aligned |

Thus the generic \(b=2\) and rank-\((1,1)\), \(b=3\) geometries are
finished.  Agents should work only on the displayed fixed-coordinate,
scalar, cofactor, and affine-fibre gates—not on the old unrestricted shore
classification.

## 4. The common mechanism exposed by the guards

The recent exact guards all fail at the same interface.

* A Hall permanent, separated selectors, six off-diagonal rows, or one
  diagonal anchor do not supply an own-edge lift.  Two anchors still leave a
  relative torus unless a source-faithful overlap equation fixes it.
* [Top apolar membership for the generic
  hafnian](shafiei-generic-hafnian-apolar-lift-obstruction.md) reduces to the
  original scalar tangent equation.  It loses the lower-degree lift and
  cross-word information.
* [Three-channel factorization, endpoint injectivity, response purity, and a
  common-power equation](curved-pure-binary-three-channel-response-guard.md)
  can hold simultaneously in an exact contracted guard.  The guard fails an
  uncontracted full row.
* The independently audited
  [pure-slice routing lemma](full-nine-pure-slice-channel-routing.md) uses
  that missing row to rule out a colour hidden in the same wrong singleton
  channel at both endpoints, for every replacement common quadratic and
  every direct block with off-diagonal curvature.  Its surviving exits are
  curvature-routed channels, a correctly labelled hafnian-zero slice, or
  deconcentrated channel support.
* Fully dark shore contractions can attain equality.  In the sharp equality
  guard, the first row that detects the defect is the one-bright,
  uncontracted four-site jet.
* The independently audited
  [common-coloop counterguard](common-coloop-a-to-D-overlap-attack.md) proves
  that multiplication by the first common power \(A\) does not by itself
  control the second-polar part of multiplication by the polar difference
  \(D_{\bar K}(z)\).  Any successful transfer must use omitted full-nine
  rows or a nonflat second chart before multiplying by \(A\).  This is a
  negative guard, not a full-nine common-coloop theorem.

The shared lesson is not merely that “more equations are needed.”  Within
the focused anchored program, the surviving candidate mechanism is
consistently **source-relative full-nine overlap before contraction by the
common power**.  The current reductions do not prove that every possible
route to the dashed arrow must use this mechanism.

## 5. The natural breakthrough theorem

The independently audited
[joint-extraction theorem](two-chart-joint-hypothesis-extraction.md) now
removes most of the proposed theorem's extraction ledger.  One selected
minor automatically supplies both physical-label full-nine systems, their
diagonal anchors, all four good endpoint maps, the all-label power-free
overlap and shared \((L,M)\) packet, first-chart activity, and ordinary
rootless selectors.  What it does not force is:

1. activity of the second chart—equivalently
   \((B,\operatorname{tr}A_{pr})\ne(0,0)\);
2. fixed-label, separated, disjoint, or own-edge compatibility stronger than
   the individual selectors; or
3. the branch-specific clean diagonal routing used by the inactive-
   \(\Omega\) packet, including its distinct trace-only boundary.

The strongest literature-derived candidate for item 2 is the audited
[explicit \(K_6\) matching-Lefschetz inverse](related-work-and-lean-artifacts.md#2-matching-algebra-lefschetz-inverse).
It inverts the aggregated edge-to-four-set incidence exactly.  The missing
comparison theorem must show that this inverse preserves a coefficient's
fixed-label source provenance through the nine physical rows.

The most coherent main target is the proposed
[diagonal-anchored two-chart overlap--jet saturation lemma](adjacent-literature-and-anchored-overlap-jet-lemma.md):

> Two overlapping physical cap charts selected by one nonzero source minor,
> carrying the automatic joint packet above and the remaining
> branch-specific activity, selector-compatibility, and complementary-row
> hypotheses, cannot both have activity-saturated clean ideals equal to the
> unit ideal.

Equivalently, at least one chart contains an active clean cap.  This is a
proposed lemma, not a proved consequence of a standard determinantal
complex.  The extraction problem is now precisely the three-item residual
above, rather than an unspecified demand for all hypotheses at once.

It has two concrete outputs rather than a new case census.

* In the rootless ledger, it forces a rank defect in the residual quotient
  after the known nonvanishing Macaulay block is removed—equivalently, it
  constructs the required physical annihilator.
* In the inactive-root ledger, its displayed \(\Omega\)-pair conclusion is
  the first boundary \(h=3\) normal form: it prevents both
  source-provenant charts from realizing the independent or
  exactly-one-zero alternatives.  A uniform theorem must replace this by
  the degree-\((h-2)\) boundary certificate.

The shore gates in Section 3 are local normal forms on which this theorem
must be proved or tested.  They are not four unrelated conjecture-level
lemmas.

## 6. Work that should not be reopened

Unless a new invariant connects it directly to the dashed arrow in (2), do
not allocate agents to:

* finding a curved pair or reclassifying the globally flat branch;
* forcing the stronger identity \(r^2=0\);
* another fixed six-site pure-lift or coordinate-plane profile;
* Hall-, selector-, one-anchor-, or top-apolar-only implications;
* another fully dark rank refinement without a one-bright row;
* deriving \(A\)-to-\(D(z)\) transfer from \(A\)-annihilation alone; or
* another isolated collision cell with no all-order mechanism.

## 7. Parallel attacks that remain genuinely independent

The main two-chart overlap theorem should receive most effort.  The useful
independent backstops are narrower:

1. a cross-word, full-nine cohafnian/Jacobian identity retaining the
   source-factorization of the response and excluding the remaining
   curvature-routed, aligned hafnian-zero, and deconcentrated pure slices;
2. an E1/E2 physical overlap packet which directly yields a clean cap or a
   source contradiction, rather than merely selecting a line;
3. a four-cut/full-mixed-sector invariant or a genuinely uniform collision
   theorem; and
4. exact unrestricted counterexample search, accepted only with a finite
   decorated lift satisfying every colouring coefficient.

Any success in the main theorem or a backstop that produces one active
clean point immediately returns to the proved descent in (2); no further
global structural classification is then needed.
