# Progress reassessment after the terminal-Bianchi branch

Date: 2026-08-08.

This note assesses commits `f81f6cf..cf9b62c` against the certified
spine.  It is a research-allocation decision, not a supersession record and
not a new mathematical theorem.

## Executive verdict

The branch contains useful and reusable work, but it does **not** change the
certified conjecture frontier.  The certified spine still stops at
`SP-CLEAN-BRIDGE`: from a selected physical line, produce an active clean
point and descend.  At order eight that implication is equivalent to
emptiness, so describing it as one missing arrow must not be read as saying
that only a routine lemma remains.  Under the original research protocol, a
route whose missing lemma is theorem-strength must be marked blocked unless
it introduces a genuinely new invariant or mechanism.  The unified
two-chart theorem remains a valuable specification, but it should no longer
be the **sole proof allocation** in its present form.

The terminal-Bianchi / marked-chart h=3 work is primarily a negative result.
It closes the attempted Schur-comparison, prolonged-derivation and reset
mechanisms inside their stated models.  Those closures are worth retaining
because they prevent the same constructions from being reopened, but this
lane is not a positive route to continue unless a genuinely new physical
source operation evades the recorded ordinary-residue and source-validity
locks.

The branch's positive candidate is the separate N=8 saturation route:

1. the live-split and good-crossing machinery reduces the residual
   saturation obstruction to configurations D1 and D2;
2. the D2 checker obstructs 512 swept branch combinations and the note
   supplies a hand Signature Lemma intended to extend those certificates;
3. the D1 checker proves monochromatic rigidity on the support class
   \(\Sigma\), leaving out-of-\(\Sigma\) residue supports.

This is meaningful localization, not an N=8 proof.  D2 still depends on the
explicitly unverified orientation/equivariance passage and on a corrected
artifact that has not been independently re-audited.  D1 remains open
outside \(\Sigma\).  The N=10 census is dangerous in every shape, so this
route also has no all-order continuation yet.

## What to retain

- The literature attribution, model qualifiers and checker-hygiene repairs
  in `cf9b62c`.
- The h=3 artifacts as negative supersession candidates, after an audit of
  their exact model scopes.  They should be used to retire mechanisms, not
  advertised as progress across `SP-CLEAN-BRIDGE`.
- The termwise/diagonal results as exact information about the
  monochromatic-edge shadow and matching-faithful packets.  They are not
  evidence that the general bicoloured case is nearly closed.
- The N=8 D1/D2 package as the next bounded audit target and as a
  falsification/calibration suite for any proposed uniform clean bridge.

## What not to promote

- No commit in `f81f6cf..cf9b62c` has an accepted entry in
  `certification/SUPERSESSIONS.md`; the certified spine is therefore
  unchanged.
- The D2 conclusion must not be called unconditional until all 48 families,
  both orientations and the structural extension beyond the eight named
  support families are checked without an inspection-only step.
- The 139-line uncommitted attack-map update is not integrated.  Its new
  K4, forced-anchor and border claims cite absent scratch directories
  (`k4decide`, `anchor4`, `border`) and are not reproducible from either
  checkout.
- More h=3 comparison complexes, diagonal-only censuses or isolated chart
  cells should not be opened unless they provide a literal map into one of
  the remaining `SP-CLEAN-BRIDGE` components.

## Recommended allocation

The immediate task is an **N=8 closure audit**, not another expansion:

1. Independently rederive the census-to-D1/D2 implication in the general
   endpoint-ordered model and produce a permanent audit report.
2. Replace the D2 orientation and equivariance inspections by an exhaustive
   checker over all 48 families and both endpoint orientations.  Separately
   rederive the Signature Lemma over the intended field; the GF(2) census is
   evidence, not its proof.
3. Re-audit the corrected D2/Sigma artifact.  Only after steps 1--2 pass
   should it receive a supersession entry.
4. Attack the residual out-of-\(\Sigma\) D1 cell in two-sided fashion.  A
   finite exact survivor at N=8 would disprove the conjecture and finish the
   task, whereas an N=8 no-go alone would not establish all even orders.
   Search for an exact counterexample while deriving the source-level
   contradiction; another family census without a completeness theorem is
   not enough.

For the affirmative all-order side, retain the unified two-chart clean
bridge as a requirements document, not as a mechanism to prove directly.
Reopen a diverse uniform lane only around information that can distinguish
finite realizability from border realizability: a valuative/tropical
obstruction on a nonvanishing chart, a rational invariant with a controlled
pole, or a genuine minimal-counterexample deletion/descent invariant in the
general endpoint-coloured multigraph.  Ordinary output equations and closed
algebraic invariants cannot suffice because the committed border theorem
places \(\Delta_{n,3}\) in the image closure for every even \(n\ge6\).
Every new local lemma should state which `SP-CLEAN-BRIDGE` component it
closes or which new finite-versus-border invariant it supplies.  If the N=8
audit passes but the D1 cell remains the full emptiness problem in new
notation, stop calling the localization a near-completion.

## Bottom line

The repository has made substantial progress in eliminating plausible proof
mechanisms and in building exact regression infrastructure.  It has not made
comparable certified progress on the conjecture's core implication since the
2026-08-01 spine.  The right next move is to convert the N=8 localization
from author-checked research into an independently audited theorem or find
where it fails; the terminal-Bianchi comparison lane itself should be
closed.

## Verification performed for this handoff

All fifteen new `verify_*.py` programs in `f81f6cf..cf9b62c` completed
successfully in ordinary mode.  The Schur closure, termwise theorem, D2/Sigma
checker and 6.1-million-clause saturation census also completed under
`python -O`.  The three new analyzers completed on their frozen/default
inputs, including all balanced-port orders 2, 4 and 6.  The modified
publication-path regressions completed as well: direct Laurent tests, F4,
generalized 3P2, all eight low-rank graph audits, and the three-cut tight
boundary checker.  The new Python files compile cleanly.

These runs validate the programs against their frozen ledgers and stated
instances.  They do not discharge the hand-proof, orientation, equivariance
or independent-audit gaps identified above.
