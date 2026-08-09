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
annihilator.  There is now a strong unconditional supply theorem at eight
sites.  Either a directed colour witness is reciprocal, giving a literal
nonzero coordinate block, or there are at least seven active rank-one pairs
whose deleted endpoint stars are both injective.  The bound seven is sharp
for the available incidence data.  More strongly, two adjacent such pairs
can be selected with a nonzero canonical transition.  If every adjacent
rank-one-good wedge were flat, each length-two path would force a higher-rank
opposite chord; the only four-chord extremal graphs contradict the
essential-incidence budget.  Thus the remaining gate is no longer curvature
selection: it is the full-nine clean-cap/contradiction theorem on this literal
curved rank-one/rank-one overlap, together with the separate reciprocal
coordinate-block branch.  Once that implication is proved, exact clean-pair
descent and the six-site terminal obstruction finish the induction.  The
same conclusion survives one or two reciprocal witness pairs; three
reciprocal pairs are the first sharp incidence frontier, with only
`3K2+2K1` and `4K2` good-edge shapes at the lower bound.

There is also a uniform-order structural version.  With no reciprocal
witnesses at order `N`, if `t` sites have three essential neighbours then at
least `N-t` selected rank-one pairs are good.  Hence either two good
rank-one witnesses overlap or at least half the sites are literal coordinate
cubic sites.  The cross-only majority-cubic case is impossible: the three
pure matchings make a simple 3-regular bipartite graph, any additional
perfect matching has a uniquely determined mixed colouring and cannot
cancel, while such a graph has more than three perfect matchings.  Therefore
the majority-cubic branch contains an internal cubic--cubic coordinate edge.
That boundary is now closed by an exact two-vertex descent.  If `d,e` are
the colours other than the direct colour `c`, insert on the residual sites
the two same-colour port-pair edges and the two crossed port-pair edges, with
the sign of one crossed edge reversed.  The same-colour linear terms recover
`X_d,X_e`; the crossed linear terms vanish by the two off-diagonal full-nine
rows; and the only possible quadratic terms are the same-pair product and
the crossed-pair product, which have equal magnitude and opposite sign.  If
ports collide the same-colour edges overlap and no quadratic term exists.
After a one-site diagonal normalization this produces an exact ternary source
on `N-2` sites.  Hence a minimal-order counterexample cannot use the
majority-cubic alternative.  Uniformly, the no-reciprocal branch is now
forced into two adjacent selected rank-one good witnesses.  At `N=8` they
can also be forced to have nonzero canonical transition; extending that
curvature conclusion, or exploiting a flat overlap directly, remains an
all-order issue.

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

At the exact dense-L rational point, the full finite source exporter now
confirms that every source row is genuinely affine in the third bend.  The
207-row Schur basis is immediate, and adjoining the full M30 row produces
one new lead, a nonzero scalar times `tau^6*r`.  Thus the sixth saturated
initial is the expected Weierstrass pivot; this is a full-germ result, not
another finite jet.  The corrected `tau^-6` row and the other 27 memberships
have not yet been materialized.  A potentially smaller all-order target is a
Nakayama recurrence: in the completed Schur quotient, with J generated by
the 28 mixed germs and g the saturated M30 germ, prove

```
M_i = c_i*g + tau*sum_j B_ij*M_j.
```

Then `J/(g)=tau J/(g)` and Nakayama gives `J=(g)` without 27 independent
large normal forms.  The same contraction form can test H0 and H1.  This is
a candidate all-order statement, but its first nontrivial layer is now an
exact certificate.  On the dense `L/F1/F2` chart, after additionally
inverting `z26+z45`, all 26 nonzero mixed germs (including `M33`) lie in
`<M30>` modulo `tau^2`; there is no second pair lead.  All available pure
dual windows through graph order seven reduce to zero as well.  Thus the
open step is no longer the initial Nakayama relation: it is to promote this
mod-`tau^2` contraction to the completed quotient, either by another finite
filtered-standard-basis layer or by the exact site-7 Ward/shear action behind
the affine bend coordinate.

That Ward action is now source-faithful.  The square-zero site-7 shear
`E20+E21` fixes the translated centre and preserves P5; on its tangent chart
it sends `z46` to `z46+rho*(z44+z45)`.  It induces 31 square-zero arrows on
the 196 normal quotient, with only two `z24` tangent remainders, and all
6,561 output words obey the expected Ward identity.  In particular the two
near-pure mixed rows differentiate to `H0` and `H1` modulo mixed rows.  The
guard is equally exact: the shear is transverse to the generic component,
`delta L=-z11*(z44+z45)`, and the raw `M30/M33` functionals do not contain
the pure Ward term.  The useful theorem must therefore lift a
Koszul-corrected derivation through the 207-row Schur graph and the monic `G`
equation; a bare equivariance argument is false.

The first corrected Ward step is now exact, and its Weierstrass half is
all-order.  Adding the fourth bend gives a localized unit coefficient in
`M30`; correcting the Ward field by that bend kills `M30`, `M33`, all other
mixed rows, and every available pure dual window through graph order seven.
More generally, the implicit 207-row graph shows that a future bend
`delta z46 = eta*tau^k` produces `delta u = eta*tau^k V(tau)`, independent
of `k`.  A source audit finds no compatibility response at relative offsets
zero through two and the same localized-unit `M30` response at offset three.
Since the source rows are affine in `z46`, no nonlinear term can contaminate
the first response for `k >= 4`.  Thus every newest bend enters `M30`
monically at the required order.

This leaves one precise algebraic half, rather than an unbounded jet search:
prove that the post-Schur mixed ideal is generated by `M30`.  A sufficient
finite complete-local certificate is

```
M_i = a_i*M30 + tau*sum_j B_ij*M_j
```

for all 27 other rows.  Nakayama then gives principality.  The already checked
mod-`tau^2` relations supply the first layer, but one must prove divisibility
by `tau*I`, not merely by `tau` in the ambient ring.  A source-level Bianchi
identity, a Ward-compatible relation module, or the first nonzero
S-polynomial obstruction will decide this promotion.

The first sign-sensitive S-polynomial now has exactly the required ideal
scope.  Put `u=z26+b-z44` and `v=z26-z44`.  In the post-207 generic-`L`
centre, localized as above, an exact characteristic-zero calculation gives

```
v*M30 - u*M33 in tau*I  (mod tau^2),
```

where `I` is generated by the 26 nonzero mixed germs, not the ambient ring.
The ideal remains nonunit.  Reversing the sign leaves an 80-term normal form,
so this is a genuine oriented source relation rather than accidental order
vanishing.  The current certificate establishes the first Nakayama layer;
the sharp theorem target is to identify its multiplier vector with a
Ward/Koszul relation that is invariant under every later bend, thereby
upgrading the displayed congruence to the completed quotient.

The relation is even more local: the same reduction succeeds with only
`tau*M30` and `tau*M33`.  Thus

```
v*M30-u*M33 in tau*(M30,M33)  (mod tau^2),
```

and, because `u` is a unit, this is the first layer of a two-row connection
expressing `M33` through `M30`.  The general saturated-special-fibre
Nakayama criterion in
[`tau-saturated-special-fibre-nakayama-criterion.md`](tau-saturated-special-fibre-nakayama-criterion.md)
shows that explicit all-order multiplier formulas are unnecessary: it is
enough to prove that the stable `tau`-colon special fibres of the mixed ideal
and of the two pure-augmented ideals are all exactly `(G)`.

The first actual colon is now sharper than this two-row formulation.  With

```
W = r4+(z0+z30+z52)*r3
       +(z0*z30+z0*z52+z30*z52)*t
       +z0*z30*z52*s,
```

the two selected initials are unit multiples `C*u*W` and `C*v*W`.  Exact
reduction gives

```
v*M30-u*M33 in tau*(M30)  (mod tau^2),
tau*W in (tau*M30),        W not in (tau*M30).
```

Thus the first `tau`-colon introduces the single monic Weierstrass equation
`W`; it does not introduce an independent `M33` equation.  The elementary-
symmetric shape of `W` suggests a fixed three-step Cayley--Hamilton recurrence
for later bends.  The next coefficient has now been checked source-faithfully:
if `e1,e2,e3` are the elementary symmetric polynomials in
`z0,z30,z52`, then

```
W4 = r4+e1*r3+e2*t+e3*s,
W5 = r5+e1*r4+e2*r3+e3*t,
```

and the complete order-eight `M30/M33` rows are the same localized-unit
multipliers times `W5`.  This is strong evidence for the transfer polynomial
`(1+z0*T)(1+z30*T)(1+z52*T)`, but two coefficients are still a prefix, not an
all-order theorem.  The finite target is now to extract the three-state
transfer/continuant matrix from the 207-row graph and apply Cayley--Hamilton.
An independent sufficient target uses affine-bend Wronskians: before graph
substitution all strict rows are affine in the newest bend, so their
cross-products with `M30` are bend-free.  Membership of those 27
cross-products in the saturated graph/centre ideal would prove
principalization without constructing further bends; failure of the raw
test is only a guard, since the implicit graph may require the lifted total
derivative.

The first literal transfer realization has now been ruled out cleanly.  The
obvious raw `2+1` Schur cascade has poles `-z10,-z37,z40`, generically
coprime to the observed recurrence poles `-z0,-z30,-z52`.  Enlarging to all
22 coordinates visible at relative order three does not repair this: the
next exact response retains those 22 coordinates and activates 26 more.
Thus there is no time-homogeneous endomorphism on that proposed state set.
The bounded target is instead the finite rational Rees substitution

```
R(T)=N(T)/((1+z0*T)(1+z30*T)(1+z52*T)).
```

Every source equation has degree at most four, so clearing the fourth power
of the denominator produces a finite polynomial membership problem.  This
test can certify the whole recurrence or expose a nonzero numerator without
constructing `W6,W7,...`; failure of selected raw state blocks is not an
obstruction to pole cancellation in the full quotient.

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

There is now a second global cut.  Expanding the target at one site and one
pure colour, then quotienting each possible partner space by its incident
colour vector, proves that some incident vector is nonzero and lies on the
target line.  The O4 specialization gives 24 exact target-incidence packets.
Adding them raises the maximum-support frontier from 20 to 34 omissions and
leaves a 159-cell face with exactly one target-only arc per site/colour.
That face is coefficient-empty: three full-output plus binomials have one
odd exponent dependency, yielding an ordinary `U^3` saturation certificate.
The face clause is support-faithful and is being fed back into the downset
CEGAR.  The circuit uses ten localized witnesses and is not yet a theorem
about mutual target arcs alone.

The four symmetry transports of that clause do not terminate the frontier.
The next maximum again has 159 live cells and the same three mutual
target-incidence cycles, but its exact coefficient oracle gives 306 plus
binomials of exponent rank 20, a consistent sign character, and no
one-class residual under the original rational-echelon reduction.  That
apparent third type was a useful algorithmic counterguard, not a surviving
coefficient stratum: an integral pivot-ordered Laurent reduction sends one
three-term full-output row directly to a localized monomial.  Expanding the
rewrites and clearing denominators gives an ordinary `U` certificate in the
original ideal using only seven source records, with integral coefficients
and hence every-characteristic scope.  The lesson is structural: Laurent
oracles must compute the actual integer exponent lattice (or reconstruct a
direct telescoping identity); a convenient rational row echelon can miss
same-character monomials and report false third types.

The one-site incidence theorem itself is now uniform: for every even order,
every palette dimension at least two, every site, and every pure target
colour, some nonzero incident row lies on the corresponding target line.
This is a useful all-order input, although choosing one such row per
site/colour supplies only a functional digraph, not yet a clean pair.

The O4 downset has now advanced through the complete 158-cell layer.  Two
ordinary source certificates have been strengthened by enumerating every
perfect-matching repair: each has exactly nine inclusion-minimal repair
masks, all single cells.  These two nine-visible-cell atoms make omission
bounds 33, 34, and 35 unsatisfiable at once.  The first remaining support has
157 live cells.  The first such face had no one-class row, but its complete
integral two-class system was still inconsistent: three dependencies had
character `-1`.

After those repairs were promoted, the next 157-cell face did pass the
entire two-class character test and initially left a 99-dimensional active
nonlinear Laurent quotient.  That apparent nonlinear frontier is now closed
by a much smaller cross-layer identity.  One residue-purity row is

```
-1 + A+B+C = 0,
```

while one homogeneous full-output row is a localized nonzero monomial times
`A+B+C=0`.  Subtracting them gives a Laurent unit.  Expanding through all 97
previous character/resultant rows and clearing denominators yields an
integral, all-characteristic ordinary `U^1` certificate using ten source
records and 24 cofactor terms.  Only five singleton cells can repair it, so
the result is an upward chart atom, not merely a certificate for one support.
This is an important oracle lesson: after character reduction, compare
affine and homogeneous fibres across different term counts before promoting
a large residual ideal to a genuinely nonlinear candidate.

This suggests a sharper candidate oracle theorem: every support-shadow
survivor activates one of finitely many visible-cell atoms, or has odd signed
lattice holonomy, a one-class residual, or an opposite-signed parallel edge
in the quotient-character graph.  The first quotient graph violating all of
these is the correct stopping point; until then, the CEGAR layers are evidence
for one finite signed group-algebra/repair-cover lemma rather than independent
cardinality accidents.

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
two mechanisms.  The family hypergraph first cuts the 236 least-cell blocks
to 49 possible blocks.  Blocks 0 through 8 have now been exhausted where
nonempty: 11,578 supports give 8,523 sign units and 3,055 one-class units,
with no integral-HNF third type.  Forty-four possible blocks remain.  This is
a certified prefix, not yet the complete exact-ten stratum.

## 3. The plausible high-level proof mechanisms

The repeated computations point to four mechanisms worth promoting to
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
4. **Curved rank-one overlap.**  The no-reciprocal structural branch contains
   a nonzero canonical transition on two adjacent, doubly injective, active
   rank-one pairs.  This is now a theorem, not a candidate selection
   principle.  It feeds the exact two-chart selector/alignment machinery:
   each rank-one direct block has two isotropic rulings, failure of a dark cut
   forces two three-site alignment packets, and the known guards fail exactly
   the omitted off-diagonal full-nine rows.  The next finite statement is to
   show that the complete off-diagonal common-power packet eliminates every
   such curved overlap or produces an active clean cap.

The cubic descent suggests a signed permanent-null completion, but its naive
multisite version is false.  An exact source-row packet with a `2x2`
permanent-zero coefficient matrix retains seven higher matching defects.  The
subsequent one- and two-anchor OO packets also fail to close the rank,
alignment, and curvature relaxation.  Their decisive limitation is now
audited: the apparent direct arms have zero deleted cofactors, so none lies in
the active selected-witness stratum.  They disprove an activity-free lemma,
not the conjecture-level overlap statement.

Adding activity is already restrictive on the nearest boundary.  Every one
of the 4,815 two-cell attempts to activate both cofactors still misses the
remaining pure target.  Exactly 30 three-cell supports complete that target;
19 activate both arms, and every one is coefficient-empty by a mixed Laurent
monomial (the smallest certificate is `xyz=1` from the pure row and `yz=0`
from a mixed row).  More strongly, every subset of the 54 opposite-shore
activity additions has a private mixed singleton.  The exact private-row
repair problem is now closed through seven added cells.  At the seventh
layer every one of the 7,200 four-cell parents has 2,852 possible
three-new-cell repairs of a selected terminal row, but none repairs all its
other inherited private rows.  The contradiction is local: minimal Hall
certificates use two mixed fibres for 6,905 parents, three for 293, and four
for only two exceptional parents.  Hence a genuine multiclass active OO
guard needs at least eight added cells.  The small Hall cores suggest a
compound-matrix theorem: two active rank-one quotient maps force rank at most
one on a `2x2` target block, while the two relevant diagonal anchors force
its determinant to be nonzero.

The first compound-matrix formulations are now sharply guarded.  Among 114
doubly-active regression profiles, a single localized cofactor leader has
transverse rank at most one.  Passing to common-word discrete Hessians is
more promising: every short Hamming-distance square has nonzero Hessian in
both active cofactors, and the literal commutator is nonzero on 51 clean
faces.  But 47 main faces put the exclusive leader in colour channel `r=2`;
changing it to the desired diagonal `r=1` makes the Hessian identically zero.
Neither a good-star Cramer minor nor the full-nine star adjugate transports
the mixed `E12` tensor grade to diagonal `E11`—this has been checked on all
47 profiles.  The exact missing statement is therefore a source-graded
Ward/Bianchi identity coupling the off-diagonal fibre to the diagonal
anchor; ordinary matrix inversion cannot supply it.

For heads `0,1`, the smallest local guard-separating datum remains the full
`22` diagonal anchor together with the literal `21` word
`(cs)_(2,1)(ad)_2(br)_1`.  The corrected bounded target must additionally
localize one nonzero cofactor coordinate on each arm, then transport this
coefficient through both right-ruling target-2 alignment ledgers and nonzero
curvature.  The exact identity
`(A*t-B*y)z^[2]=A*Q_pq-B*Q_pr` gives a useful activity split on the common
five-site complement; the annihilated/proportional branch remains open.

The D1 incidence face and the chart-26 exact-ten blocks now exhibit the same
third mechanism in literal form.  Binomial cancellation rows define a
central sign extension of their exponent lattice.  A lattice dependency with
odd total sign gives `1=-1`; if the sign class is trivial, a further fibre
whose terms occupy one quotient character gives a nonzero monomial residual.
The chart-26 exact prefixes have produced only these two outcomes.  The
second D1 incidence face initially seemed to refute the dichotomy, but its
direct `U` certificate instead exposes the necessary integral formulation:
the relevant object is the full signed partial character on the integer
exponent lattice, not a basis-dependent rational reduction.  A chart-26
theorem may identify its ten-cell/eleven-defect dependency as a relative
cycle whose character is inconsistent or whose sharp fibre has one true
lattice class.  All future finite classifications must use HNF/SNF or an
expanded source identity before declaring a third type.

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
