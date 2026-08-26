# Existing-theory survey for the remaining N=8,d=3 proof gap

Status date: 2026-08-21.  This is a discovery/triage ledger, not a proof
certificate.

## Exact target and selection rule

The current sufficient theorem is `X5-to-cap`: the three pure amplitudes are
one, all 6,558 mixed amplitudes vanish, and one must force an active clean cap
or a strict eight-to-six descent.  A useful theory must therefore retain the
252 source coordinates and the one-hot incidence maps.  It is not enough to
produce equations for the closed image of the top output tensor.

There is a decisive counterguard.  A source-faithful Laurent family has

`H_8(A(t)) = GHZ_3 + positive powers of t`,

while its full 24 by 24 covariance remains nonsingular.  Thus GHZ lies in the
ordinary and Zariski closure of the output image.  Every polynomial invariant
of the top tensor alone, every fixed contraction/flattening of it, and every
rational invariant regular at GHZ necessarily vanishes at GHZ if it vanishes
on all realizable tensors.  The problem is exact image membership versus
border membership.

## Ranked live ideas

### 0. Localized target-power filtration

The independent orbit-zero target-power identity has advanced from
`a*T in I_mix+K^14` to `a*T in I_mix+K^16`.  The old `K14` leading block
contained 838,080 exact relative factored products because only three
telescoping mixed rows were used.  Auditing all 78 orbit-zero `K0` mixed
generators gives each a unique anchor term and no `K1` term; every one of the
838,080 products is divisible by at least one such anchor, leaving zero
survivors.  This is source-labelled associated-graded divisibility, not a
Groebner membership claim.  The live target is the induced `K16` tail and the
separate lower-kernel transfer needed to promote the finite filtration to an
actual localized unit.

The promotion now replays in all three modes (logical digest `9d5e7a81...`).
At the next associated-graded layer, however, the singleton mechanism is not
self-iterating: the `K16` leading packet has 240 raw anchor signatures and
2,467,680 weighted occurrences, reducing to 50 factor-stabilizer orbits.
Among the 216 inherited `K14` signatures, 114 admit a pivot eliminating all
twelve `K2` tails, while 96 leave at least six and 6 leave at least ten.  An
exact rational affine-cover audit strengthens this obstruction: 19 of the 33
`K14` stabilizer types contain zero in the anchor-signature affine hull, while
14 do not; 40 deletion-minimal valid clauses have minimum hitting number 25.
Thus even arbitrary rational multipivots need at least 25 `K16` anchor-tail
orbits (the literal problem can only be harder), above the 20-orbit expansion
cap.  Three-mode digests are `9d5e7a81...` for the containment and
`a411a1c1...` for the obstruction.  No 25-orbit expansion or ideal-membership
claim has been made.

A proposed escape through the 31 pure-matching charts is also exactly
guarded.  Literal provenance was recovered for all 2,467,680 occurrences in
the source-faithful 25-orbit single-pivot lift, but 2,345,240 occurrences
contain no destination pure-chart product.  One relaxed anchor signature has
literal representatives with incompatible destination sets `{1}` and
`{1,2}`, and the remaining transition graph has nonidentity returns to chart
type 1.  Hence neither the relaxed signatures nor the literal packet carries
a strict chart-type/maximal-modulus potential.  Three-mode logical digest:
`4271578e...`.  The `K16` route now genuinely requires a different nonlinear
compression or lower-kernel theorem.

### 1. Equivariant Jacobian-rank contradiction

For the global amplitude map `F:E^252 -> W^6561`, equivariance gives
`dF_A(X.A)=0` for every infinitesimal symmetry of GHZ.  Its connected
stabilizer has dimension 21.  If `s` is the source stabilizer dimension, an
exact source must satisfy `rank(dF_A)-s<=231`, versus generic ranks as high as
245.  The live question is whether literal X5 plus the 728 no-cap conditions
force `rank(dF_A)-s>=232`, an impossible loss of one unavoidable torus tangent
direction.

The first shortcut is excluded: a carrier response matrix is a quotient of
the nine-dimensional cap dual, not a block in the 6,561-dimensional Jacobian
codomain.  Exactly, `Phi=H6*s_pq+sum H4*rho`; only `H6*s_pq` is a radial
Jacobian contraction.  The remaining route is an infinitesimal-rigidity or
Schur-complement theorem using literal derivative rows, with carrier
conditions only as coefficient hypotheses.  Exact controls give `rank-s=231`
on W40/X4 and 209 on the all-blocked W25/X3 chart.

The direct second-order carrier lift is also guarded.  Carrier `rho` is
indeed a Hessian block minus a direct rank-one term, but a blocker covector is
not a global conormal in `ker(J^T)`.  Pairwise ANOVA covectors glue through a
129-dimensional grade, and the compressed `252 x 129` transpose-Jacobian has
full rank 129 on both W40 and W25.  Any successful differential proof must
therefore construct a word-degree-at-least-three conormal or work on a
source-enriched normal flag; first/second-order carrier ranks alone do not
contradict the torus bound.

### 2. Doubled norm / positive Gram equality

The exact source target satisfies
`||F(A)||^2=sum_w |H_w(A)|^2=3` after the three pure amplitudes are normalized
to one.  Squaring removes phase cancellation and turns the problem into an
equality case of a positive doubled matching contraction.  The live question
is whether a source-faithful Gram, Cauchy--Schwarz, Gaussian, or
Brascamp--Lieb inequality has equality only on a clean-cap/descent locus,
rather than merely restating Bessel's inequality.  The raw Gram/Bessel screen
has now reached exactly that limit: `||F||^2=3+P_mixed`, and only the trivial
perfect-matching association-scheme sector contributes.  Exact balanced
controls initially suggested the sharper pattern `P_mixed=0,1,2` at
`n=4,6,8`, but the corresponding universal inequality is now **false**.
At the balanced Laurent point there are exact cross-colour leakage rays with
negative quadratic coefficient, as detailed below.  A weaker positive gap or
an equality classification may still be useful, but `P_mixed>=2` must not be
used as a proof target.

The sharp value is now exact on the leakage-free diagonal slice.  Fixing one
of the three pure perfect matchings and enumerating the remaining `105^2`
ordered pairs gives a minimum of exactly two mixed coloured perfect
matchings, attained 864 times.  Under `S8 x S3`, equality has exactly two
orbits: one has pair-cycle types `(4+4,8,8)` and four union triangles; the
other has types `(8,8,8)` and two union triangles and contains the frozen
Laurent support.  Structurally, any pair of pure matchings with at least two
alternating components already supplies two mixed switches; the
pairwise-Hamiltonian residual has 960 records, split into 576 with value two
and 384 with value three.  Moment balance and pure product one make every
one-factor cell unit magnitude, while an output word determines its unique
coloured matching, so phases cannot lower this count.  All 36 feasible
single-colour alternating-four-cycle perturbations at the Laurent orbit have
strictly positive quadratic coefficient with distribution
`2^6,3^10,4^7,5^6,6^3,7^4`.  All 1,260 signed sums of two distinct elementary
cycles also have positive coefficient, ranging from 4 to 14 (minimum 4 in 30
cases).  This covers the real diagonal off-support cycle cone tested, not the
full 252-cell Hessian.  Cross-colour leakage does lower the energy.  Among 72
feasible two-cell leakage rays, the exact quadratic distribution includes
four directions with coefficient `-3/2`, two with `-1`, eight with `-1/2`,
and two zero directions.  A representative is
`Y_02^(2,0)=1, Y_57^(0,2)=-1`.  It integrates exactly: for `r>1`, put
`s=r^-3`, `t^2=r^2-r^-6`, replace the colour-zero anchor `25` and the
colour-two anchor `07` by `s`, replace the other three anchors in each of
those colours by `r`, leave colour one unit, and add the two leakage cells
with values `+t,-t`.  Every relevant port energy is `r^2` and each pure
product is `r^3 s=1`; near `r=1` the mixed energy is
`2-(3/2)t^2+... < 2`.  With `x=r^2`, its exact energy is

```text
P(x)=x^3+x^2+x-3*x^-1-x^-2-x^-3+4*x^-5.
```

It has a unique global minimum at the unique root `x>1` of
`3x^8+2x^7+x^6+3x^4+2x^3+3x^2-20`, with
`1.073<x<1.074` and `P_min≈1.7980700759`; it never reaches zero because the
mixed amplitude `H_11111012=-t` is nonzero.  Crucially, the family is not on
the no-cap locus: six anchor pairs have star response support, nonzero scalar
blocker, and `kappa=(1,1,1)`, hence active clean caps.  Thus any useful norm
theorem must use the no-cap hypothesis.  The corrected live target is the
local/global implication “balanced and `P<2` forces a clean cap,” not the
false unconditional diagonal floor.

This corrected implication is now exact on every elementary two-cell
leakage ray at the Laurent orbit.  The 16 rays with nonpositive quadratic
coefficient split into five stabilizer orbits of sizes `2,4,4,2,4`, with
values `-3/2,-1,-1/2,0`; every one has a support-separated active `K=I`
response-star cap that persists under its exact algebraic balance lift.
Among the 56 positive rays, 52 also retain such a cap.  The only four
elementary rays without a frozen support-separated identity cap form two
stabilizer orbits and all have the phase-independent positive coefficient
five (`linear norm 4` plus forced correction 1).  The first unresolved local
question is therefore multi-ray interference: determine the
minimum combined leakage support that destroys all cap witnesses and test
the quadratic form on those support orbits.  The four exact audit digests are
`25fe798b...` (diagonal classification), `bbcf0283...` (diagonal Hessian),
`17b0d225...` (leakage rays), and `5533f6d0...` (integrated family).

The first multi-ray interference test illustrates why the full carrier
family is load-bearing.  Combining a positive no-star support
`{25^(1,2),46^(1,2)}` at amplitude `1/2` with the descending ray
`{02^(2,0),57^(0,2)}` at phases `+,-` gives exact quadratic coefficient
`5*(1/2)^2-3/2=-1/4` and destroys all six frozen response-star caps.
Nevertheless the full rational carrier audit finds two active `K=I`
response-triangle caps, at pair `23`/triangle `(0,4,5)` and pair
`57`/triangle `(0,2,6)`, both at rank zero.  Thus no genuinely no-carrier
negative tangent has survived.  The next local task is the finite hitting
problem for supports that destroy both star and triangle witnesses, followed
by exact minimization of the same quadratic form.

That finite hitting problem now has a tangent-level counterexample.  Adding
the balanced ray `-(04)^(2,0)+(37)^(0,2)` to the four-cell support destroys
both triangle witnesses.  On the three ray amplitudes `(A,D,E)` the exact
quadratic form is diagonal,

```text
Q=5*A^2-(3/2)*D^2-(1/2)*E^2,
```

so `(A,D,E)=(1/2,1,1/10)` gives `P2=-51/200`.  Exhaustive rational response
audits over all 28 pairs, all 6 stars, all 20 triangles, and arbitrary `3x3`
`K` find no carrier on this six-cell tangent support.  This falsifies the
elementary tangent version of “nonpositive implies cap.”  It does **not** yet
falsify a finite no-cap energy gap: exact nonlinear moment/pure normalization
and finite-parameter carrier ranks may obstruct or reroute the tangent.  An
exact algebraic lift is the current must-pass test.

That lift exists and remains no-carrier.  With leakage amplitudes
`(A,D,E)=(s/2,s,s/10)`, solve the three positive branches near one

```text
rho0^2 (rho0-s^2) (rho0-s^2/100)=1,
rho1^3 (rho1-s^2/4)=1,
rho2^2 (rho2-101s^2/100) (rho2-s^2/4)=1,
```

and set each diagonal anchor magnitude to the square root of its port energy
`rho_c` minus the incident leakage energy.  Then all ports are balanced and
all three pure amplitudes are exactly one.  There are 17 nonzero outputs
(3 pure, 14 mixed), and

```text
P=2-(51/200)s^2+(504459/160000)s^4+O(s^6),
```

so `P<2` for small nonzero `s`.  Every one of the 168 star and 560 triangle
carriers has a literal one-monomial forbidden row isolating a diagonal
blocker, so no arbitrary-`K` response carrier exists anywhere on the small
nonzero branch.  Thus the no-cap threshold two is definitively false.  The
live quantitative question is whether this exact family has a positive
global minimum or tends to zero on its maximal real branch.

That one-parameter question is now certified globally by outward-rounded
interval arithmetic.  The positive branch exists uniquely for every
`s>=0`, all 18 support coefficients remain nonzero for `s>0`, and the same
literal 728-carrier no-cap proof persists.  There is exactly one positive
critical point, with

```text
s^2 in [0.0397589013672, 0.0397589047241],
P_min in [1.99490005061, 1.99490202117],
P''_(s^2) in [6.52375467, 6.52377158].
```

The tail obeys `P ~ (1894177/2000000)*s^8`, and `s^2>=5` already gives
`P>4.7975`.  Hence this family has a unique attained positive minimum and no
escape to zero.  This is evidence for, but not a proof of, a global no-cap
gap; the next must-pass test is the smallest support enlargement.

That must-pass test is negative for stability.  Among 39 structurally
Gram-orthogonal elementary two-cell additions, twelve exact support/sign
classes have negative first coefficient at the certified six-cell minimum.
The best canonical addition is

```text
-(05)^(1,0) + (23)^(0,1),       dP/d(epsilon^2) approximately -1.46010.
```

It integrates without approximation by replacing the first two port-energy
equations with

```text
rho0^2 (rho0-u-v) (rho0-u/100)=1,
rho1^2 (rho1-v)   (rho1-u/4)=1,
```

and leaving `rho2` unchanged.  Thus balance and all three pure amplitudes
remain exact, the support has eight leakage cells, and the literal
one-monomial diagonal-blocker proof still excludes all 728 carriers.  The
six-cell positive minimum is therefore not a local minimum in the full
no-cap locus.  The global eight-cell branch minimum and the next enlargement
are the current quantitative tests; no uniform gap should be inferred from
the six-cell certificate.

The second diagonal equality orbit gives the same local conclusion with a
different spectrum.  Its canonical `(4+4,8,8)` matching triple has stabilizer
order eight and 72 minimal balanced two-cell rays with phase-minimized
quadratic distribution `0^12,1^4,2^8,3^40,4^8`.  The twelve nonpositive rays
are all zero directions, split into three stabilizer orbits of size four;
every one has a support-separated active `K=I` clean cap.  There are no
negative elementary rays.  Logical digest: `7187799b...`.  Thus the
elementary local energy-to-cap principle holds at both `S8 x S3` diagonal
equality orbits; multi-ray interference remains the common unresolved layer.

At the second orbit, multi-ray interference fails at the smallest possible
four-cell layer.  One canonical support
`{04^(0,1),07^(1,0),16^(0,1),26^(1,0)}` with phases `(+,+,-,-)` has exact
continuous quadratic coefficient zero.  A fraction-free audit of all 728
carriers, all three diagonal blockers, and the direct-pair blocker finds no
active carrier (64 rank/membership profile bins, all masks nonzero).  Logical
digest: `060577e1...`.  Its exact nonlinear balanced lift and first nonzero
higher energy coefficient are being computed separately.

That exact lift is now terminal and bends upward.  With
`t^2=r^2-r^(-2)`, the degree-zero ports have anchors `r` and the degree-one
ports have anchors `r^(-1)`; every port energy is `r^2` and all three pure
amplitudes stay one.  Literal replay gives

```text
P(r)=6-8*r^4+4*r^8 = 2+4*(r^4-1)^2.
```

Thus the Hessian-flat direction has quartic positive curvature, its unique
real minimum is two at `r=1`, and it is coercive.  Exact finite carrier audits
at `r=101/100` and `r=2` still find zero active carriers, so the upward bend
is not caused by leaving the no-cap stratum.  This contrasts sharply with the
three-colour six-cell family, whose quadratic coefficient is `-51/200`.

### 3. Kempf--Ness balancing and compact equality slice

The normalization-preserving torus is noncompact and the known Laurent family
approaches GHZ only at infinity.  A hypothetical exact source whose torus
orbit is closed has a moment-map-zero representative, characterized by equal
port energies for each colour.  Balance itself is not compact: a
pure-normalized moment-zero family with unit diagonal matching cells and a
common off-diagonal value `t` has norm `12+168t^2`.  It is not X5.  The only
live version is therefore mixed-amplitude coercivity using both moment zero
and all no-cap hypotheses, or an explicit balanced no-cap sequence with mixed
norm tending to zero.

Balancing loses no hypothetical exact source.  `T0` fixes GHZ, so if
`F(A)=GHZ`, every point in the closure of `T0.A` still maps to GHZ.  The
unique closed orbit in that closure therefore also lies in the exact fibre,
and Kempf--Ness supplies a moment-zero representative.  Consequently the
formerly proposed inequality `P_mixed>=2` would have proved the conjecture
directly, but the explicit balanced cross-colour family above refutes it.
Kempf--Ness remains useful only if one can prove a weaker positive gap on the
no-cap locus or exclude balanced base-locus jets with the full carrier data;
balance alone is insufficient.  The later exact six-cell family is itself
no-carrier and lies below two, so the sharper no-cap threshold two is also
false.  Its smallest support enlargement runs to an active-cap boundary,
which points toward a stratified boundary theorem rather than a fixed sharp
constant.

## Queued theories with distinct must-pass tests

### Exact-fibre Euclidean conormal / minimum-norm source

This is now the primary exact-fibre route.  The idea was already proved in
`notes/minimal-norm-gauge.md`: the exact fibre is affine closed, so the
coercive source norm attains a global minimum whenever the fibre is nonempty;
every full star and triangle is then the unique least-norm solution of its
exact affine block system, without any smoothness assumption.  The missing
connection was the certified six-site descent theorem.  At `N=8,D=3`, no
point of the exact fibre can have an active clean cap, since such a cap would
produce an impossible exact six-site source.  Hence minimizing over the
**entire** exact fibre safely retains every no-cap consequence.

Fritz--John stationarity supplies a global conormal

```text
alpha*A = J_A^* lambda,  (alpha,lambda) != 0,
```

including the singular `alpha=0` branch.  This is precisely the datum missing
from the earlier carrier-Hessian attempt: the 728 blockers do not glue into a
conormal by themselves, whereas the attained full-fibre minimum produces one.
The constrained Hessian can then consume the audited identity
`rho = D^2F slice - direct rank-one term`.  A proof needs only exclude the
resulting full-fibre minimum system; it does not need a finite-boundary or
infinity branch, because closedness and coercivity already give attainment.
The exact must-pass equations and singular guard are recorded in
`unaudited-codex-ed-conormal-gap-framework-2026-08-21/REPORT.md`.

At the full-fibre minimum this choice removes output-invisible
chords: whenever a coordinate can be erased while preserving the exact
output, a minimum-norm source cannot retain it.  The smallest controls are the
exact `n=4` GHZ fibre and the frozen invisible chord; W40/W25 remain hostile
non-fibre guards and must not trigger the implication.

### Positive matching-Gram association scheme

Keep the 105 source summands separately:
`v_M=tensor_(ij in M) A_ij`, so `F=sum_M v_M`.  Their Gram matrix
`G_MN=<v_M,v_N>` is positive semidefinite and its entries factor over the
alternating cycles of `M union N`.  Unlike the retired linear Brauer screen,
this remembers the nonlinear source decomposition.  The perfect-matching
association scheme has only the five sectors `[8]`, `[6,2]`, `[4,4]`,
`[4,2,2]`, and `[2,2,2,2]`.  The must-pass test is whether moment zero,
pure normalization, and no-cap force strictly positive Gram energy in a
nontrivial sector, with equality only on a cap/descent locus.  An arbitrary
PSD counterexample is irrelevant; the cycle-factorized Gram constraint is
load-bearing.

### Luna slice and second-order boundary obstruction

Any balanced sequence with mixed norm tending to zero must normalize to a
moment-zero base-locus point `B` with `F(B)=0`, followed by a higher jet whose
first nonzero image is GHZ.  The must-pass test is local and finite: on each
source-faithful balanced base-locus type compatible with no-cap, compute the
first nonzero normal form of `F` on the Luna slice and show that its image
cannot be the GHZ line.  This is stronger than ordinary Jacobian rank and
avoids claiming global compactness.  It is useful only if the no-cap
incidence conditions survive graph closure on the chosen slice.

At the phase `K4 disjoint-union K4` base this programme has advanced beyond
ordinary second variation.  Binary-word grading excludes arbitrary
multicolour escape at orders four and five.  The first response-only
order-six response-only channel is also empty: after the six `E2` equations
eliminate `L`, the six `E4` cokernel equations force every `L_I=0` whenever
`Haf(R) != 0`, contradicting the desired `Haf(L)Haf(R) != 0`.  This result is
channel-specific.  The first genuinely new `1+1+2+2` system has 60 variables
(54 after eliminating `L`) and `per2(X)=0`.  Its row-star and minimum-support
`2x2` types are exactly empty, but its column-star type has the explicit
family

```text
U_i4=U_i5=U_i6=z_i,  U_i7=0,
X_i4=z_i,  V_i5=z_i,  R45=R67=1,
L_ij=-2 z_i z_j.
```

It satisfies `E2=E3=E4=0` and has full pure coefficient
`-12*z0*z1*z2*z3`.  At `z_i=1` all 72 previously rank-zero carrier pivots
appear at valuation one.  It nevertheless fails the full source equations
before blocker branching.  For every left pair `I={i,k}`, an omitted binary
word has unavoidable coefficient
`[t^2]H_w=4*l_(I^c)*z_i*z_k`; all phase cofactors and all `z_i` are nonzero
when the pure coefficient is nonzero.  These six rows lie outside the base
derivative image, and third-colour cells cannot affect their binary words.
An independent literal replay from the 40 nonzero source cells recomputed all
6,561 amplitudes and found 30 nonzero mixed coefficients below order six
(earliest `[t^2]H_00111000=4`), while reproducing the pure coefficient `-12`.
Thus this column-star family is not a GHZ/no-cap arc.  Three-mode logical
digest for the frozen support resolution: `7923a469...`; independent packet
replay is being packaged separately.

The binary order-six topology ledger is now exhaustive on the
`Haf(L)Haf(R)!=0` open.  Partitions `1+1+1+3` are all impossible; every
`1+1+2+2` topology reduces to the coupled channel.  Its two-entry
column-star branch and all five denser-`R` support orbits are eliminated by
literal response rows, forcing `Haf(L)=0`; second-colour equations and the 72
blocker branches are never reached.  Three-mode digest: `34db8f2d...`.  The
formerly remaining product-zero divisor is now closed as well.  The complete
pure coefficient decomposes into the response product, a polar contraction,
and `[t^6]per4(tX+t^2V)`; the `E4` contraction makes the first two combine to
`-Haf(L)Haf(R)`, while `per2(X)=0` forces a zero two-row or two-column slice,
so the direct `per4` coefficient vanishes in every row-star, column-star, or
`2x2` type.  Hence the product-zero divisor has pure coefficient zero, and
the earlier six-branch theorem excludes the product-nonzero open.  No binary
order-six pure jet exists at all; third-colour and blocker branching cannot
alter the binary rows.  Three-mode digest: `32c52753...`.  The next target is
an order-independent valuated-permanent lemma (or, failing that, the finite
order-seven partitions `1+1+1+4` and `1+1+2+3`).

The first order-independent contraction already holds coefficientwise.  If
`E_I=L_I Haf(R)+sum_J R_(J^c) per2(C[I,J])` denotes the six literal
six-coloured-site rows, then
`sum_I L_(I^c) E_I=0` gives the universal relation
`k2=-2 Haf(L)Haf(R)`, hence
`H_pure=per4(C)-Haf(L)Haf(R)` at every valuation.  A fully universal closure
still needs control of response contamination in the four-coloured-site
rows.  At order seven, `1+1+1+4` is empty; the correctly exhaustive partition
list also includes `1+2+2+2` in addition to `1+1+2+3`.  The last two reduce
to eight primitive support/valuation types.  Seven are now closed exactly:
one is Laurent-singleton impossible and 114/114 coefficient targets for the
other six have exact `Q(omega)` unit ideals with no timeouts.  The last
`1+2+2+2`, `k=4` primitive is genuinely support-feasible.  A complete
696-Boolean support encoding is SAT; a verified greedy reduction gives an
inclusion-minimal 82-atom support with no mixed singleton and no earlier pure
monomial.  Its literal coefficient target has 82 nonzero variables, 1,220
mixed equations (2--24 terms), and a ten-term pure coefficient.  This exceeds
the broad-solve guard.  The current sound next step is Laurent-binomial
lattice/SNF compression before any exact coefficient gate, not a support
UNSAT claim.

### Fractional perfect matchings on the balanced base locus

On a leakage-free diagonal colour layer, moment zero is exactly a fractional
perfect-matching condition.  Its half-integral extreme points are disjoint
edges and half-weight odd cycles, so Tutte/Edmonds odd-set obstructions explain
the canonical `C3 disjoint-union C5` balanced base direction.  This is a useful
boundary stratifier, not a proof by itself.  Cross-colour leakage destroys the
separate diagonal degree equations, and phases defeat support even without
leakage: a unit-modulus K4 with matching products `1,omega,omega^2`, times a
second unit K4, is balanced, has nine full perfect matchings, and has zero
hafnian.  Any use of matching polytopes must therefore feed coefficient-level
Luna/jet equations rather than claim a support-only cap.

## Tested but sharply downgraded

### Phase-hyperfield Wick vectors

Signless hafnian cancellation does not satisfy the orthogonal-tract Wick
axioms.  Already on four ports, matching products `(1,-2,1)` sum to zero and
their phases satisfy the ordinary phase-hyperfield zero relation, while the
alternating four-point Wick expression has surviving phases `(-,-,-)` and
does not contain zero.  Unit tail edges embed the counterguard into eight
sites.  The sparse GHZ witness is exceptionally Pfaffian after orientation;
that does not globalize.

### Bosonic Gaussian annihilator equations

Projecting `(a-A a^dagger)|A>=0` gives exactly the literal Laplace recurrence.
Two and three annihilators reproduce the `15+90` and `45+60` matching splits,
and all commutator profiles through order four are ordinary Wick partial
matchings.  Collision sectors introduce unknown lower moments, while the
invisible chord changes `q,q^2,q^3` and leaves `q^4` unchanged without
violating any annihilator identity.  No new source relation appears.

### Arc spaces / integral closure as a finite census

Integral closure is still formally characterized by finitely many Rees
divisors, but there is no small source-relative blow-up presently available.
Explicit GHZ-reaching arcs have infinitely many inequivalent contact types
even modulo the source torus and permutations.  At a one-cell chart the base
ideal has 6,561 generators in 251 variables: 729 cubic-leading six-site
hafnians plus 5,832 quartic-leading rows, and the GHZ jet lies in the cubic
kernel, so the cubic truncation is insufficient.  The remote tail ideal is
already the unit ideal on the normalized exact-source ring and has no useful
Rees divisor.  Normalizing the full Rees algebra would simply restate the
global elimination problem.

### Source-constrained algebraic discrete Morse theory

The smallest Morse complex has one critical parallel-pair class `D`, not a
clean-pair cell.  Ordinary quotient cancellation produces `4[D]`, whereas
every literal source lift is a boundary; exact comparison identifies this
byte-for-byte with the already-frozen chart-25 Schur--Bockstein `4D` class.
Its four-element orbit sum remains nonboundary in a torsion-free cokernel, and
the path-forest archive contains no source-labelled map from `D` to the cap
module.  The named theory clarifies the obstruction but does not move it.

### Fourier `Z_3` virtual-symmetry pull-through

After Fourier transform, the exact local covariance exists, but no proper K4
or K8 blocked region is normal, injective, or even `Z_3`-injective.  Boundary
domain sizes are `4^b` while image ranks are only `3^r`; explicit invariant
kernel vectors exist for both parities of `r`.  Moreover virtual edge
cancellation would require `X A X^T=A`, which GHZ/X5 does not imply.  Thus the
fundamental PEPS symmetry theorem cannot be invoked.

### Connectedness / graded deformation of the remote idempotent

This has the wrong direction.  For the full 168 cross-colour tail ideal `J`
in the normalized N8 X5 fibre ring `A`, the audited diagonal theorem gives
`A/J=0`, hence `J=A`.  Thus any hypothetical nonzero fibre is entirely the
remote factor (`e=1`); connectedness cannot force it toward zero-tail.  At
`n=4` the standard witness lies on a smooth closed diagonal torus component,
while at `n=6` the normalized fibre is empty and its Laurent family escapes at
infinity.  A useful replacement would need properness plus a nonempty
zero-tail factor, and neither hypothesis holds.

### Brauer/partition-algebra decomposition

The exact perfect-matching module is multiplicity-free with dimensions
`1+20+14+56+14=105`, but the hafnian row map uses only its trivial one-line
summand.  The other 104 matching directions are unconstrained kernel, not
identities.  Pair/cell representation overlaps with the 1,638-row module are
only recombinations of existing rows; the full symmetry closure of the master
270 is already all 1,638 rows.  Thus representation theory organizes the
known equations but does not create the missing source coupling.

### Projective stabilizer-torus one-cell arc

The exact geometric reduction is valid but algebraically tautological.  All
252 source weights remain distinct modulo the three pure characters, so a
generic cocharacter exposes one live cell, and normalized pure matchings force
its minimum weight to be negative.  However every matching term of a fixed
word has exactly the same torus weight.  The resulting one-cell arc therefore
multiplies each original coefficient equation by one power of `t`; its initial
system selects no terms and gives no new local/Rees constraint.

### Genus-two Kasteleyn--Pfaffian resolution

The 16-sector Arf sum exactly reconstructs each hafnian, but edge deletion
twists its coefficient vector by the edge's `H^1` character: only 12 of 28
edges preserve the aggregate.  Surviving empty-base Plucker relations are the
four-site Pfaffian definition/Laplace rewrite, while nonempty-base relations
double a site degree and are not literal X5 rows.  Even the 82 untwisted first
reinsertion paths cancel termwise.  This is a 16-fold rewrite, not a new
clean-pair identity.

### Quantum max-flow/min-cut equality rigidity

The nominal cut capacities for `k=1,2,3,4` terminals are `3,9,27,81`, while
GHZ has rank three on every nontrivial cut.  But every minimum is attained at
the physical output legs, not an internal source cut, so equality gives no
internal bottleneck.  Adding the invisible chord raises one bond Schmidt rank
without changing the top tensor or any flattening.  Ordinary quantum
max-flow/min-cut therefore cannot see the source condition we need.

### Infinite-prime reduction

The abstract arithmetic implication is correct: geometric emptiness over
infinitely many residue characteristics would imply characteristic-zero
emptiness.  It supplies no present shortcut.  At fixed degree/support,
membership modulo infinitely many primes already lifts to characteristic
zero by an augmented-minor argument.  The every-odd-prime six-site boundary
identity refutes only local cap selection, inverse-hafnian degree `p-1`
identities are scalar tautologies, and the characteristic-three searches test
`F_3`-rational rather than algebraically closed points.  Only a genuinely
uniform `p`-dependent geometric certificate would revive this lane.

### Literal site-down / zeon contraction hierarchy

The hierarchy is source-faithful but linearly redundant.  For each fixed
contracted site set its exposed-colour and residual coordinates biject all
`3^8` source words, giving rank 6,561 (mixed rank 6,558); the one-, two-, and
three-site matching partitions are `105`, `15+90`, and `45+60`.  Archived
blocked-site, full-nine, and determinant `3+3` routes are projections of
these same layers.  The only new higher datum found is a nonlinear
second-response reinsertion scalar, but it has source degree five and repeats
both omitted endpoints, so it occurs in no literal quartic X5 row.

### Global minimal MPS / weighted automaton

The reachable/observable quotient does reduce GHZ to the three-state diagonal
copying automaton, but this discards exactly the source information needed for
a cap.  Already at `n=4`, different colour sectors occupy different boundary
types while producing the same minimal quotient.  On `K8` an invisible chord
creates a reachable but unobservable state and is erased by trimming.  Hence
minimal realization depends only on the top tensor and cannot control the
remote idempotent or literal source support.

### Labelled graph connection matrices

Connection algebras do not repair the MPS defect.  Their definition is the
labelled graph algebra modulo the radical of the gluing pairing; Lovasz's
factorization and twin reduction intrinsically discard null states.  Krenn
also supplies one fixed-`K8` block rather than all labelled gluings, and the
complex setting has no reflection positivity.  The invisible chord changes
`q,q^2,q^3` while leaving `q^4` fixed, so it is literally top-radical but
source-visible.  Only a lower-sector connection packet plus a proof that its
remaining radical is cap-benign would be new.

### Full `S8 x S3` degree-two syzygy compression

The exact symmetry closure has 60,440,688 degree-two row-multiplier objects.
The two target-relevant Hom spaces have dimensions 269,064 and 134,782, for
403,846 coefficients in total--over fifteen times the 25,901-orbit baseline.
Every target block occurs, and a separate degree-five/degree-six grading
mismatch requires an additional source-valid homogenizer.  Full symmetry is
therefore not a compression for this membership problem.

### Arithmetic product formula / first tropical cover

The exact characteristic-two lift evaluates on the normalized fibre as
`1=2R`, hence only as `R=1/2`; this is fully compatible with the product
formula.  A normalized polystable number-field family has arbitrarily negative
balanced 2-adic monomials, so local instability supplies no global height
contradiction.  The original 729 rows also fail to be a tropical basis on an
explicit two-edge-star cone.  Only genuinely higher filtered 2-adic jets could
refine this isolated-prime route.

### Port-balanced invariant semigroup / source quotient

The quotient is logically faithful but computationally worse.  Exact Hilbert
data in the first target box gives 108,617,671,890 primitive degree-12
balanced monomials, hence at least 47,143,087 `B4 x S3` orbits.  Even the
completed-cycle invariant mixes 144 primitive degree-12 terms with
decomposable terms.  Low-degree Hilbert/SAGBI enumeration therefore hits the
explosion guard before producing a power bound.

### One-hot PEPS/Holant canonical form

The local projector stabilizer is
`Ga^18 semidirect ((Gm)^7 x GL3)`, but every nonzero additive direction
creates forbidden half-edge monomers.  On literal bonds it reduces to
`T0 semidirect S3`.  Fixed-graph noninjectivity is explicit: an invisible
extra chord can leave the `K8` output unchanged without lying in the
restricted invertible gauge orbit.  Thus existing PEPS/Holant canonical
theorems control the wrong equivalence relation for exact Krenn membership.

### Global base-locus blow-up / border-versus-exact geometry

Write the amplitudes as the degree-four rational projective map

`H : P^251 -->> P^6560`.

The Laurent limit can reach GHZ only through the all-amplitudes-zero base
locus.  Resolve the map by the Rees algebra/blow-up of the base ideal, compute
the exceptional fiber over GHZ, and prove that the entire proper fiber is
boundary.  Equivalently, adapt border-rank boundary/substitution methods to
show that GHZ has a border realization but no finite realization.

The bounded test is terminal-negative as a global classifier.  Exact
GHZ-reaching arcs have inequivalent projective base supports of sizes one,
two, and three; the cubic exceptional fibre already contains a 24-dimensional
Segre family, larger than the 21-dimensional source torus, and the base locus
contains large site-isolation linear spaces.  There are infinitely many
primitive valuation orbits.  The useful residue is a source-cycle Rees ratio,
not a finite boundary-type theorem.

Theory leads:

- Buse--Jouanolou, *On the closed image of a rational map and the
  implicitization problem*, arXiv:math/0210096.
- Buczynska--Buczynski, *Apolarity, border rank and multigraded Hilbert
  scheme*, arXiv:1910.01944.
- Landsberg--Michalek, *On the geometry of border rank algorithms...*,
  arXiv:1601.08229.

### Intrinsic/top-only squarefree matching algebra

Let `B_i = C + V_i` with `V_i^2=0`, let `B=tensor_i B_i`, and put

`q = sum_(i<j) A_ij in B_2`.

Then the complete Krenn tensor is exactly `q^4/4! in B_8`; the conjectural
source would satisfy

`q^4/4! = e_0^tensor8 + e_1^tensor8 + e_2^tensor8`.

This retains the one-hot projection while making multiplication,
catalecticants, higher Hessians, Jordan type, and Lefschetz equality cases
available.  The useful target is not a top-tensor equation (impossible by the
closure counterguard), but a source-relative statement that equality of the
fourth power forces a singular multiplication map, a clean cap, or a boundary
valuation.

Bounded result: GHZ's apolar algebra is maximally Lefschetz, and the first
source multiplication map has full rank on active-cap, dense all-blocked, and
remote controls.  The natural degree-two apolar operators are not valid fiber
equations.  Intrinsic/top-only apolarity is therefore retired.  Only a genuinely
relative labelled identity involving `(q,q^2,q^3,q^4)`, a carrier, and full X5
remains possible.

Theory lead: Numata, *The Lefschetz property for an algebra defined by
matchings*, arXiv:2302.11039.

### Unrestricted Holant clone

The source is a tensor network with arbitrary binary edge signatures and a
fixed local exactly-one incidence tensor.  Arbitrary local projections are
too expressive: they generate ternary GHZ exactly from Bell-pair Gaussian
signatures.  Holant-clone or tensor-category theory is relevant only if it
keeps the one-hot local signature and the fixed one-vertex-per-party graph.

Cheapest test: compute the conservative Holant clone generated by the
one-hot tensor and arbitrary binary signatures under the restricted simple
graph realization, and ask whether equality/GHZ is in the exact clone or only
its orbit closure.  A general gadget realization does not settle the Krenn
problem because it may duplicate sites or accept multiple incidences.

Theory leads:

- Backens--Goldberg, *Holant clones and the approximability of conservative
  Holant problems*, arXiv:1811.00817.
- Cai--Young, *Vanishing Signatures, Orbit Closure, and the Converse of the
  Holant Theorem*, arXiv:2509.10991.

## Retired ideas

### Output-only Wick, cumulant, four-qubit, flattening, or matchgate invariants

Retired as global separators: GHZ lies in the output closure.  They remain
useful only after retaining lower sectors/source data or as chart-local
diagnostics.

### Ordinary torus/Hilbert--Mumford support degeneration

Exact audit: all 310 minimal zero-tail supports are polystable.  Their
nonzero one-parameter stabilizers fix every live coordinate and therefore do
not contract support.  A larger balanced support exists outside the 310.
No support-minimal degeneration lemma follows.

### Framed-quiver King stability

Exact audit: the intrinsic GHZ framing reduces the genuine source symmetry
to the already-tested torus (up to the finite colour permutation).  `K_8` is
not bipartite, so the bilinear edge tensors cannot be turned source-faithfully
into an ordinary primal/dual quiver representation.  Full cyclic framing
makes stability vacuous.

### Complete-collineation / naive Grassmann incidence compactification

The compactification is proper and equivariant, but rank-drop fibers retain
ghost blocker planes.  It helps only if a new Rees/tangent theorem proves
that the X5 graph closure excludes those ghosts.

### Algebraic-matroid stress alone

Carrier circuits restate the same 728 four-way blocker choices.  A dense
pure-normalized non-X5 witness has all blocker circuits, showing that the
matroid forgets the cross-carrier nonlinear source coupling.  Stress duality
can certify a proposed identity but does not generate the missing global
one.

## Recommended work order

1. Test the literal infinitesimal-rigidity inequality
   `rank(dF_A)-dim Stab_T0(A)>=232` under X5 plus no-cap, without identifying
   carrier response ranks with Jacobian ranks.
2. In parallel, test mixed-norm coercivity on the moment-zero,
   pure-normalized, no-cap slice; a balanced base-locus sequence would retire
   this route decisively.
3. If both fail, move to a second-order Luna-slice/Hessian obstruction that
   retains all 252 source coordinates.  Do not restart the output-only,
   broad-symmetry, or unlocalized Groebner lanes falsified above.
