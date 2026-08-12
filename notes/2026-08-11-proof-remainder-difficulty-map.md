# Difficulty map for the remaining proof

This is a proof sketch and dependency audit, not a claim that the conjecture
is proved. Difficulty labels mean:

- **Established:** already proved with source-valid hypotheses.
- **Easy/formal:** a short argument once its inputs exist.
- **Medium:** a concrete local theorem with no conceptual ambiguity, but a
  nontrivial source calculation or compatibility proof remains.
- **Hard:** new global structure or a new physical chain map is required.

## 0. Global reduction to the live branches

### Established

The joint extraction and synchronization results reduce a maximal source to
source-faithful selected charts with the required full-nine systems, anchors,
good endpoint maps, overlap data, and curvature normalization. The remaining
proof is not another extraction or genericity argument.

The live conclusions are organized into:

1. one-bad/multisite affine accessibility (Theorem A);
2. rootless augmented-polar descent (Theorem B); and
3. one physical comparison coupling rootless and inactive projections
   (Theorem C).

### Easy after the branch theorems

Once an active clean cap is produced, the existing descent closes that
branch. Once the physical rootless polar map exists, Fredholm duality gives
either the relative generator or the annihilator. Once the common comparison
cell exists, its mapping-cone and inactive Omega/Bezout consequences are
formal.

## 1. Theorem A: affine accessibility

### Established

1. Minimum support gives independent occupied complete response columns and
   a unique full-support circuit modulo the target line.
2. In a three-column circuit, two literal mixed coordinates have a nonzero
   2x2 quotient minor.
3. A word-synchronized, oppositely oriented, typed single-C4 common-tail
   minor gives a source-valid active determinant/cofactor carrier.
4. Whole alternating components can be switched without new cells. A
   C_(2r) with a nonzero distance-three chord shortens to
   C4 + C_(2r-2).
5. Cross-intersecting selected hole families are exactly star, triangle, or
   K2,2 Hall forms.
6. The target-coloop route has been reduced to one local diagonal return.
   The nonzero P2:21 branch exits by a private target row.

### Easy

1. Given a synchronized shortening chord, iterate the cycle shortening to a
   C4 and invoke the common-tail theorem.
2. Given cross-intersection, invoke the finite star/triangle/K2,2
   classification.
3. In the final diagonal return, the E2 dichotomy is short. If the diagonal
   matching is nonzero in the pure-1 word, reselect it. Otherwise the pure
   and mixed bases have a nonzero matching-base E2 minor, hence a literal
   common-q exchange carrier.
4. Extending existence of a nonzero quotient minor from k=3 to k>3 is
   linear algebra. It does not by itself land the carrier.

### Medium

1. **Local cubical C4 landing and saturation.** The undivided E2/E3/E4
   cells form an exact relative coherence--curvature square. Nonzero
   Hamming-one curvature is a localized common-tail same-star Pluecker
   carrier. A single flat square, however, does not imply complete-column
   dependence: a literal edge-monomial packet can be flat at the base and
   every Hamming-one neighbour while failing at Hamming distance two. The
   correct theorem is Hamming-cube descent followed by primitive source
   saturation: the first nonflat face gives the carrier, while global
   flatness must lift to a complete one-sided column dependence and a
   nu-safe deletion.
2. **Hall consolidation.** Package the many proved strict Hall normal forms
   into one entry theorem and verify that each finite target-line movement
   preserves the synchronized anchor measure.

### Hard

1. **Word-synchronized chord-or-Hall.** The unary and companion rows must
   turn a chordless or unsynchronized C6/C8 determinant contribution into a
   same-word shortening chord, an off-anchor carrier, or cross-intersecting
   hole families. Aggregate response equations do not imply this.
2. **Diagonal lock-web theorem.** A full-source diagonal alternating web
   must have a same-star five-lock dependence, an opposite crossed mate, or
   an off-diagonal exit. Only primitive charts are currently closed.
3. **Arbitrary-k rank completion and termination.** A local active carrier
   may still have deleted-star profile (2,2,3,3), and coefficientwise
   contraction from k to 2 is false. A uniform circuit-transport theorem
   must create a transverse head or an anchor-safe simultaneous deformation,
   together with a genuinely decreasing global potential.

These are independent hard points. Theorem A is not currently one lemma from
completion.

## 2. Theorem B: physical rootless polar

### Established

1. The five-column augmented pentagon has an exact
   generator-or-annihilator alternative once the physical map P exists.
2. Presentation jets do not define P.
3. Site-Euler physical jets exist after localization, but satisfy
   anchor = ordinary residue and are augmented-gauge trivial.
4. A non-Euler colour-diagonal GHZ-stabilizer pair exists modulo site-Euler
   gauge. It has zero source, target, and all fifteen selected ordinary
   residues; its marked Hessian sector is h_v with coefficient one.
5. The full corrected mixed Hasse row is zero, so retaining h_v is a relative
   descent problem.

### Easy/formal

1. State the filtered/relative long exact sequence and its edge-map
   criterion.
2. Once one physical column P(e_v) is source-valid and zero-indeterminate,
   use symmetry to obtain the five columns.
3. Apply Fredholm duality: a nonzero-aggregate kernel produces the relative
   face; otherwise the aggregate factors to the terminal annihilator.

### Medium

Construct compatible one-marked nullhomotopies for the two first boundary
pieces A_v and B_v in the same augmented fine degree. This is a concrete
chain calculation, not yet a global theorem.

### Hard

1. **Marked-sector descent.** Resolve the overlap term C_v and prove that the
   other completion terms are boundaries in a source-labelled relative
   filtration while h_v survives.
2. **Terminal projection and zero indeterminacy.** The landing must preserve
   the physical word/anchor grade and annihilate the homology of the
   correction kernel. A formal associated-graded projection is insufficient.

These two items are the actual construction of P; the Fredholm step after
them is easy.

## 3. Theorem C: common rootless/inactive comparison

### Established

The desired readouts are precisely typed. On the inactive side the
residue-minimality, Omega/Bezout, and certificate-bracket prolongation are
proved once the first transgression value exists. On the rootless side
Theorem B specifies the required physical polar.

### Easy/formal

Once one physical horizontal cell has both projections and zero
indeterminacy, the mapping-cone argument and downstream contradictions are
formal.

### Medium

Synchronize labels and fine grades after Theorem B has supplied an actual
physical P, rather than a formal marked sector.

### Hard

Construct a single target/residue-augmented horizontal comparison that is
source-valid in both projections and kill indeterminacy in both. Separate
rootless and inactive symbols cannot simply be composed; existing formal
principal-parts, Schur, Hasse, and occupancy candidates fail exactly here.

The diagonal inactive branch also retains a separate source-level Rees
membership/routing obligation. The existing theorem supplies a criterion,
not the required membership.

## 4. Likely proof order

1. Prove local Hamming-cube C4 descent and primitive saturation. The
   undivided relative square is established; the remaining work is to rule
   out a primitive colon class on the special one-bad localized packet.
2. Prove word-synchronized chord-or-Hall for k=3.
3. Prove the diagonal lock-web theorem.
4. Prove arbitrary-k rank completion and a strict termination potential.
   This finishes Theorem A.
5. Construct the first two marked-sector nullhomotopies A_v,B_v, then solve
   the overlap C_v and zero indeterminacy. This finishes Theorem B.
6. Build the common horizontal comparison and handle the remaining diagonal
   inactive Rees routing. This finishes Theorem C and the branch coupling.
7. Invoke the already proved clean-cap descent, Fredholm alternative, and
   mapping-cone consequences.

## 5. Risk assessment

The most plausible near-term proof advance is local Hamming-cube C4 descent
plus saturation.
The greatest combinatorial risk is arbitrary-k termination in Theorem A.
The greatest homological risk is zero-indeterminate marked-sector descent in
Theorem B. The greatest overall risk is Theorem C: it asks for genuinely new
source-relative comparison data, not merely a better use of existing rows.
