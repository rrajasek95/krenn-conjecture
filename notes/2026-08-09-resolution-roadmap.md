# Resolution roadmap after the N=8 parallel attacks

Status date: 2026-08-09.  The conjecture remains open.  This note separates
the exact advances from the candidate structural statements that would turn
them into a proof or a counterexample.

## 1. What a complete resolution still has to do

At eight sites, choosing one nonzero pure matching monomial in each colour
gives the exact 31-chart localization cover.  A proof of the eight-site case
must therefore establish

\[
 H_0H_1H_2\in\sqrt{I_{\rm mix}R[P_j^{-1}]}
\]

for every one of the 31 anchor charts, or replace that list by another proved
exhaustive cover.  D1, D2, P5, and the corrected sharp chart-26 seed are
currently certified local strata or counterexample searches; they are not an
exhaustive relabelling of the 31 charts.

The cover now has one global structural split.  Among its 404 mixed anchor
factors, 396 have an all-even complementary two-factor, and every chart
except chart 26 contains at least one.  An even complement splits into two
perfect matchings, so its mixed-coefficient rewrite stays inside the
three-copy matching expansion.  This reduces the plausible global proof to
a signed source-labelled Morse contraction on those rewrites plus the unique
odd `(5,3)` chart-26 critical complex.  Acyclicity and the descendant
critical-state census remain open; the earlier unsigned leading-incidence
contraction is known to be insufficient.

An eight-site proof alone does not prove the all-even conjecture.  The proved
descent spine still has one conjecture-level gap: a selected curvature/cap
line must produce an active clean pair, or an equivalent source-provenant
annihilator.  Once that implication is proved, exact clean-pair descent and
the six-site terminal obstruction finish the induction.

A disproof can stop at eight sites.  It requires an exact common zero of all
mixed coefficients with all three pure coefficients nonzero, followed by the
full endpoint-coloured verification.  A support-shadow survivor, a finite jet,
or a modular point without a local lifting certificate is not enough.

## 2. Three finite N=8 decision problems now exposed

### P5: component-local Schur/conormal theorem

The finite first Rees chart has 253 variables.  The exact 207-row Schur block
has pairwise-coprime local leads (196 ambient normals and 11 transverse
pivots), so it is an all-order local standard basis and leaves only the 45
P5 base coordinates and the Rees parameter.  The remaining source-faithful
input is 28 mixed germs plus H0 and H1.

The next statement is finite and precise:

> **P5 component theorem.**  After tau-saturation and localization on each
> component of the 28-germ quotient, either a pure coefficient is a unit/nonzero
> survivor on a formally liftable component, or both pure coefficients lie in
> the component ideal.  On the generic-L component it is enough, in
> characteristic zero, to prove irreducibility/formal smoothness, one zero
> basepoint, and the conormal memberships dHc in dK_L.

The strict-order-seven identity dH0 = U dG modulo G is the initial layer of
this proposed conormal certificate.  The finite Schur graph now recovers the
entire triangular centre `L,F1,F2,G` source-faithfully through graph order
six.  The successive bend equations are affine, and `dG/dr=-1`; all 26
remaining order-six compatibility rows reduce after adjoining G.  The next
finite promotion test retains r as a coordinate, uses one full strict
transform with initial G as a Weierstrass equation, and reduces the other 27
full mixed germs and H0,H1 in that quotient.  This avoids an unjustified
infinite bend recurrence.  Raw global normal-form timeouts give no
mathematical verdict.

### D1: residue maxima plus a projection-degenerate tripod lemma

The all-size monochrome anchor theorem reduces D1 to 312 anchor charts.  Five
of the six inclusion-maximal residue-support orbits are coefficient-empty.
The sixth, O4, has an exact 14-parameter residue family, but its maximal
external chart is empty by the checked W1 six-site tensor argument.

The remaining issue is downward support closure.  The first checked
replacement for cardinality-by-cardinality CEGAR is:

> **Four-star tripod lemma.**  On the O4 residue stratum, assume
> the four residue cells witnessing injectivity of Phi and four specified
> boundary-star cells are nonzero.  Then the W1 equations are inconsistent
> over characteristic zero, whether or not the direct boundary coefficient
> z is present.

Indeed the dependent projection branch has

\[
 w e_2^3+\tau\Phi(P)-2\Psi(P)=0.
\]

For nonzero tau, the already checked tensor-line quotient gives the O4
contradiction without using w.  For tau=0, the colour-zero slice gives
P4=kappa c and P5=-kappa e, while the target slice is
w e_2^2+2kappa^2 c\otimes e=0.  If w is nonzero, quotienting by the line c
kills it; if w=0, the second term is itself impossible.  Commit `40114d1`
checks the raw 81 coefficients and both scalar branches.  Commit `3298295`
then transports the argument across the target-cross minors, producing 576
checked source-faithful clauses over every field of characteristic other
than two.  A separate target-aligned normal form closes both exceptional
alignment flags and contributes 384 further clauses in characteristic zero.
These clauses now supply rank/profile cuts rather than new support layers.

### Corrected sharp chart-26 seed: alternating-cycle character theorem

The exact 16-cell seed has eleven singleton mixed fibres and one repaired
binomial fibre.  Every no-singleton extension has at least 26 cells.  More
sharply, all 1,498 inclusion-minimal direct repairs using at most nine new
cells are closed even after spending the remaining cap-26 budget.  Hence a
26-cell survivor must be an inclusion-minimal ten-cell coupled repair.

For a fixed word, repairing a unique perfect matching is the same as adding
an alternating cycle.  This suggests the finite statement:

> **Alternating-cycle character propagation lemma (candidate).**  Eleven
> seed defects repaired with ten new cells either give an inconsistent signed
> Laurent character, or some other mixed fibre has a singleton Laurent class
> after quotienting by the maximal binomial lattice.

The naive version using only the original binomials is false: some repairs
create multiterm fibres and some sampled binomial systems are character-
consistent.  More strongly, commit `f3641c7` exhibits two minimal repairs
with identical labelled essential-incidence matrices, overlap graphs, ranks,
and alternating-cycle censuses, while one is killed by a one-class residual
and the other by signed odd holonomy.  Thus unsigned incidence/cycle data
cannot select the branch.  The refined statement must retain the full signed
Laurent row matroid and allow both alternatives.  The first 1,000
solver-directed ten-cell transversals were all coefficient-killed by these
two mechanisms.  The first six exact least-cell blocks have now been
exhausted independently: 4,550 supports give 3,355 sign units and 1,195
one-class units, with no third type.  This is a certified prefix, not yet the
complete exact-ten stratum.

## 3. The plausible high-level proof mechanisms

The repeated computations point to three mechanisms worth promoting to
lemmas.

1. **Koszul/conormal transgression.**  On P5, an apparent pure survivor is
   repeatedly the next mixed compatibility equation times a localized unit.
   A completed-local conormal identity would prove all-order constancy and
   replace jet chasing.
2. **Tripod rank and quotient geometry.**  In D1, residue purity produces a
   small tensor normal form; external exactness is controlled by injectivity
   of one tripod map and rank-one quotient alternatives.  Classifying its
   projection-degenerate strata is more scalable than support cardinality.
3. **Matching-exchange local systems.**  A mixed fibre with one term is a
   unique-perfect-matching obstruction.  Alternating-cycle repairs carry
   signed Laurent holonomy.  Odd holonomy or a singleton character class is
   an exact coefficient obstruction.  A source-faithful propagation theorem
   could turn bounded repair censuses into a uniform chart lemma.

None of these mechanisms currently supplies the global 31-chart cover or the
all-order clean-pair descent.  They are, however, concrete statements with
exact finite inputs and clear proof/disproof outcomes, rather than open-ended
search directions.

## 4. Parallel stopping rules

* P5 stops decisively when every component of the tau-saturated 28-germ
  quotient has a pure-membership certificate, or when one component has a
  formally smooth point with both pure coefficients nonzero.
* D1 stops decisively when the six maximal residue orbits are closed under
  all support degenerations, preferably by a finite tripod-rank clause
  family.
* The sharp seed stops decisively when all ten-cell direct transversals are
  support- or coefficient-closed, or one yields an exact liftable torus
  solution.
* A proof of the conjecture still needs an exhaustive N=8 chart theorem and
  the source-provenant active-clean-pair implication for descent.
