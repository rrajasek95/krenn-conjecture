# Research checkpoint: terminal sync and the level-two differential

Checkpoint date: 2026-08-01.

## Status

Krenn's conjecture is **open**. The certified proof spine is unchanged:
`SP-CLEAN-BRIDGE` remains the missing conjecture-level implication. This note
is a synchronization and research checkpoint, not a supersession.

The substantial Claude chain from the terminal clone has been preserved
linearly through `c871c2c`. Its Git topology, provenance, and proof-status
labels were audited before integration; the load-bearing claims identified
below received separate mathematical audits. The synchronized research chain
then adds:

| Commit | Purpose |
|---|---|
| `9b38660` | Remove the only whitespace defect in the imported chain. |
| `04148e6` | Replace the sampled level-two slope check by an exhaustive formal proof over all 84 blocks and 64 words. Independently audited PASS. |
| `9ad3484` | Repair the provenance and scope defects in Claude's two certification records, without changing either mathematical statement. Independently audited PASS. |
| `01764c3` | Prove the R2 pair-pencil rank drop for the four-live/two-dead level-two family. Independently audited PASS. |

The user's two pre-existing, superseded double-polar drafts were not
overwritten. They remain recoverable in stash object
`2c348bed84e266e116460f0048b4fa48e5fd8a19`.

Four untracked Claude checkers were preserved, with exact hashes and trust
labels, on the pushed branch
`archive/claude-orphaned-checkers-2026-08-01` at `4fc726b`. They were not
mixed into the synchronized proof chain.

## Certification boundary

The baseline tag `certified-spine-2026-07-30` remains authoritative. Claude's
records `SUPERSESSION-2026-08-01-01` and `-02` used abbreviated hashes, had no
permanent independent reports, and omitted required scope/frontier updates.
Append-only records `-03` and `-04` procedurally replace them and pin the exact
replacement commits, artifact hashes, auditors, and unchanged statements.

No later research result in this checkpoint supersedes a named certified
dependency. In particular, neither the support theorems nor the level-two
differential currently proves `SP-CLEAN-BRIDGE`.

## What the synchronized work and recovered traces add

The strongest imported results are now:

1. Every vertex and every complementary colour pair is non-rigid. The old
   rigid/private-edge branch is vacuous.
2. At `(8,3)`, the live support graph has no independent four-set.
3. The 2,940 level-two words generate 84 overlapping blocks of 64, totaling
   5,376 incidences; words of colour-count type `(4,2,2)` occur in two blocks.
   In each block, the rare diagonal cell is affine with slope equal to the
   complementary six-vertex binary matching tensor.

The interrupted trace adds the following audited interpretation of those
blocks:

4. Writing the complementary tensor as `Psi(M)`, with endpoint columns
   `P_x,Q_x` and
   `N_xy = P_x Q_y^T + Q_x P_y^T`, the exact block equation is

       dPsi_M(N + (z/3) M) = 0.

5. Exact rank-55 witnesses show that a dense open locus has only the five
   trace-zero vertex-scaling kernel directions. On that locus the block takes
   the Cauchy-gauge form

       N_xy = (nu_x + nu_y) M_xy,    z = -sum_x nu_x.

This is structural progress, but a single block has positive-dimensional
solutions and therefore cannot yield the contradiction by itself.

## Result recovered and completed from the traces

The interrupted L2 trace is
`agent-a1dfcff36e4b0f443`. Its Steps 1--4 contain the sound differential
identity and generic-kernel calculation. Step 5 is invalid on nonempty
zero-sum graphs; Step 6 is a sample rather than a classification; and the
phrase "three-fold determination" is too strong when a slope vanishes.

The universal-rule trace `agent-aac438e5301d9721e` contains a complete hand
proof of R2 at eight vertices. Applying R2 to the rank-55 Cauchy-gauge branch
eliminates the five-invertible/one-dead family immediately. It forces the
four-invertible/two-dead family into 16 pure-column assignments.

The new theorem in
[`level-two-pair-pencil-rank-drop.md`](level-two-pair-pencil-rank-drop.md)
closes all 16 assignments without enumerating algebraic subcases:

- every assignment has an extra live-live tangent-kernel direction, so
  `rank dPsi <= 54`;
- a balanced 2+2 assignment has two extra directions, so
  `rank dPsi <= 53`.

The checker is stdlib-only, runs in about two seconds, and verifies 1,408
formal polynomial identities under normal, optimized, and isolated Python.
An independent agent re-derived R2, every kernel identity, orientation,
generic-to-all specialization, and the arbitrary-live-live scope before PASS.

## Trace results not promoted into the chain

- The independently audited scratch result `Q_C(Per_4)=2` would give a
  cleaner support-independent proof of the already-landed bipartite `4+4`
  exclusion. It does not advance beyond the no-independent-four-set theorem,
  so its interrupted author artifacts were not promoted.
- The heavy cross-colour terminal-class checker claims a useful local
  vanishing result, but its separate audit hit a session limit. It is archived,
  not accepted.
- The three-mode contraction proves the general bound `D <= N-1`; it also
  proves why slice rank is saturated and uninformative at `(8,3)`. It is a
  negative-route result and remains in the archive.
- The support-only 31-branch abstraction already fails at solved `(6,3)`.
  Its reported empirical counts have no committed replay artifact and remain
  soft-quarantined.

## The shortest live continuation

The new rank drop removes two named nontrivial families, but the interrupted
trace did not classify all rank patterns in the generic-kernel equation.
Three precise rocks remain:

1. **Classify without a census.** Derive a rank-pattern-independent
   consequence of `X_x J X_y^T = (nu_x+nu_y)M_xy`, using R2 before choosing
   normal forms. The desired lemma must cover rank-one and mixed-rank `X_x`,
   not just the sampled invertible/dead types.
2. **Use overlapping blocks.** For an edge entry, the valid cross-block
   statement is `F_c^{st}=A_e[s,t]H_c`: a live slope determines the entry,
   while `H_c=0` forces only `F_c^{st}=0`. Either prove enough slopes live or
   exploit the zero-slope branches directly. Do not assume all three slopes.
3. **Kill the trivial generic packet globally.** There is an exact rank-55
   selected-block packet with `P=Q=z=0` satisfying all current support rules,
   no-independent-four-set, and slice-cover activity, while failing 389 of the
   full 6,561 equations. This guard proves that another support theorem is not
   enough; the next argument must couple this block to other L2 blocks or to
   L0/L1 values.

The natural throughline is therefore value-sensitive global compatibility:
local differential normal form, R2-induced tangent rank drop, then overlapping
block consistency. Another support SAT census, a single-block contradiction,
or a return to the inactive terminal cap does not address the remaining guard.

Follow-up: [level-two-one-sided-rank55-guard.md](level-two-one-sided-rank55-guard.md)
strengthens item 3 in the selected block itself.  The equations vanish on the
entire linear family \(Q=z=0\), with arbitrary \(M,P\); an exact member has
every \(P_x\ne0\), all six \(X_x\) of rank one, an everywhere-live slope, and
\(\operatorname{rank}d\Psi_M=55\).  Its support completion also realizes the
literal residual R2 witnesses and a complete live graph.  It is not a full
solution or a replacement for the stronger all-support-rules packet above,
but it shows that cross-block coupling is needed even before both stars vanish.

Second follow-up:
[level-two-one-sided-overlap-collapse.md](level-two-one-sided-overlap-collapse.md)
performs that first coupling.  On the rank-$55$ locus where every residual
deletion graph is connected nonbipartite and every four-site binary cofactor
is live, L1 and the three-/four-rare-colour value rows force the remaining
one-sided star to vanish.  The exact witness in the first follow-up satisfies
these hypotheses: all six five-site cofactor maps have rank $10$, and all
$240$ four-site cofactor coordinates are nonzero.  Consequently that
nonzero-star witness is no longer a global guard.  The live obstruction is
now the zero-star packet $P=Q=z=0$, together with the zero-slope,
rank-deficient, bipartite-deletion, and vanishing-cofactor boundary strata.

Third follow-up:
[level-two-zero-star-four-c-obstruction.md](level-two-zero-star-four-c-obstruction.md)
closes the cofactor-open zero-star packet.  Its mixed four-rare-colour rows
force every symmetric endpoint-pair coefficient to vanish, while the
pure-colour row is exactly a linear combination of those same coefficients
and must equal one.  In addition, rank $55$ plus connected nonbipartite
deletion graphs automatically makes the slope and all four-site cofactors
live by a five-dimensional kernel-budget argument.  The entire generic
one-sided branch is therefore impossible in a full solution.  What remains
is the genuinely two-sided generic-kernel locus and the rank-deficient,
graph-degenerate, or cofactor-vanishing boundary.

Fourth follow-up:
[level-two-fully-invertible-residual-obstruction.md](level-two-fully-invertible-residual-obstruction.md)
closes the dense open residual locus without assuming a one-sided endpoint
pattern.  If all fifteen internal binary blocks are invertible, R2 forces
both endpoint stars to vanish at every residual root.  Rank \(55\) then makes
the slope and four-site cofactors live, so the zero-star theorem contradicts
the pure-colour row.  An exact integral witness verifies that this forbidden
locus is nonempty: every block determinant is nonzero, the differential rank
is \(55\), all \(64\) slope coordinates are live, and all \(240\) cofactor
coordinates are live.  Consequently every rank-\(55\) level-two block in a
hypothetical solution must contain a singular internal \(2\times2\) block.

Fifth follow-up:
[level-two-singular-star-budget-and-four-live-closure.md](level-two-singular-star-budget-and-four-live-closure.md)
quantifies that forced boundary.  At each residual root, the degree in the
internal singular-block graph is at least the number of nonzero endpoint
stars.  On the generic-kernel branch, a pure spoke from an invertible
endpoint matrix confines the neighboring rank-one matrix to the named
coordinate row.  This closes all four-invertible patterns: nonconstant spoke
assignments reduce to the earlier two-zero theorem, while constant assignments
have the sharp differential-rank bound \(50\), proved by a 34-plus-16 slice
factorization.  Thus a rank-\(55\) generic-kernel block has at most three
invertible endpoint matrices.

Sixth follow-up:
[level-two-cofactor-zero-rank-drop.md](level-two-cofactor-zero-rank-drop.md)
quantifies the formerly open cofactor boundary.  If one four-site cofactor
tensor vanishes while an endpoint deletion graph remains connected and
nonbipartite, its four edge-cell directions are transverse to the five gauge
kernels, so the differential rank is at most \(51\).  A sharp integral
witness has exactly one zero cofactor, full \(K_6\) live support, and exact
rank \(51\) modulo two primes.  Therefore at ranks \(52\) through \(55\), a
zero cofactor forces graph degeneration at both endpoint deletions.

Seventh follow-up:
[level-two-three-invertible-r2-guard.md](level-two-three-invertible-r2-guard.md)
shows that the at-most-three bound is locally sharp.  An exact packet with
endpoint-star ranks \((2,2,2,1,0,0)\) satisfies all \(60\) scalar
generic-kernel identities, all \(64\) selected level-two rows, differential
rank \(55\), and literal R2 exits at all six residual roots.  The escape is a
zero-multiplier cut: R2 uses some free spokes as pure witnesses while other
spokes to the zero-star vertices remain full and restore rank \(55\).  This
is a selected-block/R2 guard, not a full solution.  The next live target is
therefore an overlapping/L0/L1 obstruction to that mixed
three-invertible/one-rank-one/two-zero packet.

Eighth follow-up:
[level-two-three-invertible-l0-obstruction.md](level-two-three-invertible-l0-obstruction.md)
eliminates that exact guard before any L1 or overlapping-L2 analysis. For
every endpoint pair and binary colour pair in a full solution, the two
monochromatic six-bit basis vectors must lie in the image of the complementary
six-site differential: each fixed endpoint-colour slice is a tangent vector
by the $15+90$ matching partition and Euler's identity. Hence a rank-$55$
packet must have mixed-row differential rank exactly $53$. The displayed
guard instead has mixed-row rank $55$; adjoining either pure vector raises
the rank to $56$, and adjoining both raises it to $57$, over $\mathbb Q$
and two primes. Thus none of the 167 cells outside its minimal fixed packet
can repair it. The linear screen is sharp: a second exact integral packet has
full/mixed ranks $55/53$ and literal pure-vector tangent columns, although no
factored endpoint completion is asserted. The stratum-wide frontier is now
the locus of alternative zero-multiplier blocks satisfying tangent incidence
and the stronger factored two-star endpoint equations.

Ninth follow-up:
[level-two-factored-l0-cut-determinantal-obstruction.md](level-two-factored-l0-cut-determinantal-obstruction.md)
turns that factorization requirement into cut equations. On the rank-$55$
gauge-kernel chart, the four normalized L0 slices form a shared pencil
$B(A)=[U_L\ V_L]\left(\begin{smallmatrix}0&A\\A^{\mathsf T}&0\end{smallmatrix}\right)
[U_S\ V_S]^{\mathsf T}$. Hence every $5\times5$ minor vanishes, every
$4\times4$ minor is proportional to $\det(A)^2$, and every $3\times3$
minor is divisible by $\det(A)$. For a mixed slice with invertible residual
blocks, every live
$K_{2,2}$ forces scalar projective holonomy. On the four-cycle-generic chart
this leaves exactly 17 labelled gauge supports: the empty graph, six stars,
and ten copies of $K_3\sqcup K_3$. These are necessary screens, not a
stratum-wide contradiction.

Tenth follow-up:
[level-two-l0-sharp-factor-obstruction.md](level-two-l0-sharp-factor-obstruction.md)
closes the exact $55/53$ linear sharpness packet. After quotienting by its
five-dimensional gauge kernel, a four-edge subsystem with independent edge
scalars is already the unit ideal over $\mathbb Q$ and
$\mathbb F_{32003}$. The
[independent audit](level-two-l0-sharp-factor-obstruction-independent-audit.md)
uses only three slices and verifies an explicit rational certificate
$\sum c_kf_k=1$ with 38 equations and 124 multiplier monomials. Thus both
displayed survivors—the original $55/55$ R2 guard and the exact $55/53$
tangent-incidence sharpness guard—fail L0. The open target is now a
stratum-wide use of shared-factor cut constraints, not another isolated
completion test.

Eleventh follow-up:
[level-two-mixed-support-pair-collapse.md](level-two-mixed-support-pair-collapse.md)
collapses the generic factored mixed-slice split. A live mixed edge with an
invertible residual block makes both endpoint factor matrices invertible.
Every one of the sixteen nonempty allowed supports—six stars and ten copies
of $K_3\sqcup K_3$—spans all six vertices and has a dead edge between live
vertices, an immediate contradiction. Thus $288$ of the $17^2=289$ ordered
support pairs die. For the remaining empty--empty pair, one empty mixed slice
already implies that the two pure slices cannot both be blockwise invertible
on a common residual triangle. Every survivor therefore lies on twenty
explicit pure-triangle determinant hypersurfaces. This closes the dense pure
potential chart and transfers locally to singular packets whenever all blocks
on a nominally live mixed support are invertible; nominally live singular
edges and the closed pure-determinantal cover remain.

Twelfth follow-up:
[level-two-three-invertible-coordinate-shore-rank-drop.md](level-two-three-invertible-coordinate-shore-rank-drop.md)
closes the generic-kernel stratum with exactly three invertible endpoint
matrices and three nonzero rank-one endpoint matrices. If the zero-multiplier
graph on the rank-one shore has zero, one, or two path edges, direct
factorizations of the matching tensor give exact differential-rank bounds
$35,42,49$. If all three shore edges have zero multiplier, the rank-one
matrices share a right factor, the cross spokes become constant after local
basis changes, and a two-term tensor factorization bounds the rank by $51$.
Thus none of this stratum reaches rank $55$. Branches with one or more zero
endpoint matrices remain outside the theorem.

Thirteenth follow-up:
[binary-ghz8-residual-rank-census.md](binary-ghz8-residual-rank-census.md)
audits all 28 endpoint deletions of five sparse exact binary GHZ8 sources: the
alternating cycle, the switched family over both $\mathbb Q(\sqrt2)$ and
$\mathbb Q(\sqrt3)$, the rational cancellation source, and a new subdivision
of the active-rank-two six-site gadget. Their maximum residual differential
ranks are respectively $22,26,26,31,26$; all 140 deletions have the necessary
full/mixed rank gap two. This is a low-complexity baseline, not a
classification.

Fourteenth follow-up:
[binary-ghz8-exact-rank53-source.md](binary-ghz8-exact-rank53-source.md)
supersedes the sparse maximum. An explicit 26-parameter rational chart
realizes binary GHZ8 identically, verified over a Laurent function field.
A small rational specialization has a unique deletion with exact
full/mixed differential ranks $53/51$; the complete 28-deletion profile is
audited over $\mathbb Q$. Five formal gauges and two formal star columns show
that this deletion has rank at most $53$ identically throughout the chart,
so the bound is chart-wide and sharp. This proves that any unrestricted
universal rank bound must be at least $53$. Same-support controls have rank
$55$ off the GHZ fibre, while deterministic tangent corrections and restarts
found no rank $54$ or $55$ solution. Those failed searches remain evidence
only about other components. For the sharp deletion, the two adjusted mixed
endpoint packets span only one class modulo the five gauges, so a naive proof
by two independent mixed-kernel classes is false.

Fifteenth follow-up:
[binary-ghz8-rank53-star-lift-audit.md](binary-ghz8-rank53-star-lift-audit.md)
independently reconstructs the rational chart and the exact $53/51$ deletion.
It also identifies the missing kernel class. One adjusted mixed packet is
zero and the other is a nonzero rank-one star packet $S(e_0)$. For any
six-site residual source, a factored star kernel
$S(u)_{rz}=h_r u^{\mathsf T}$ satisfies
$D(S(u))=u\otimes F_h$; if $u\ne0$ and this vanishes, then
$D(S(\ell))=0$ for every endpoint column $\ell$. When the off-star live graph
is connected and nonbipartite, no nonzero gauge can be star-supported, so
the two star columns are independent modulo the five gauges and
$\operatorname{rank}D\le53$. This is a reusable branch theorem, not a
universal rank bound. At the exact source it is sharp and the kernel is
exactly the direct sum of the five gauges and the two star columns.

Sixteenth follow-up:
[level-two-three-invertible-two-rank-one-one-zero-closure.md](level-two-three-invertible-two-rank-one-one-zero-closure.md)
closes the adjacent generic-kernel endpoint pattern with three invertible,
two nonzero rank-one, and one zero matrix. If the rank-one shore edge has
nonzero multiplier, a three-term matching factorization gives rank at most
$49$. If its multiplier is zero, the zero endpoint's free-edge set cannot
meet both the invertible and rank-one sides; the two resulting tensor
factorizations give bounds $54$ and $46$. Thus the whole $3I+2R+1Z$ stratum
misses rank $55$, without R2. Within the exactly-three-invertible frontier,
the only neighboring pattern still known to attain rank $55$ is
$3I+1R+2Z$, represented by the earlier selected-block/R2 guard. The mixed
gauge equation alone does not create the nonzero star tangent needed by the
star-lift theorem there; an L0/L1 or overlapping-block equation must supply
the additional class or contradiction. The $3I+0R+3Z$ pattern and strata
with fewer than three invertible endpoint matrices remain outside these new
bounds as well.

Seventeenth follow-up:
[level-two-three-invertible-three-zero-closure.md](level-two-three-invertible-three-zero-closure.md)
closes the remaining zero shore.  The zero-sum equality classes for three
zero endpoint matrices embed, up to relabelling, in four maximal support
envelopes.  Their matching factorizations give differential-rank bounds
$44,54,43,28$, respectively, so the entire $3I+0R+3Z$ generic-kernel
stratum misses rank $55$.  Consequently the exactly-three-invertible
frontier has reduced to the single endpoint pattern $3I+1R+2Z$.  The exact
rank-$55$ guard in that pattern also shows that the generic-kernel equation
and R2 alone cannot force a star kernel; the remaining attack must use the
factored L0/L1 overlap equations or dispose of the singular-spoke boundary.
Strata with fewer than three invertible endpoint matrices remain outside
the current closure.

Eighteenth follow-up:
[binary-ghz8-rank53-two-cell-tangent-isolation.md](binary-ghz8-rank53-two-cell-tangent-isolation.md)
audits support openings at the exact rational rank-$53$ GHZ8 seed.  The
active-support equation Jacobian has rank $19$; adjoining any one of the
$67$ missing cells raises the rank to $20$, and adjoining any of the
$2211$ missing pairs raises it to $21$.  Thus no one- or two-cell support
opening occurs at first order at this seed.  The full missing-cell quotient
has rank $65$, leaving exactly two wider support-opening tangent classes;
the result is local and does not exclude higher-order arcs or distant
components.

Nineteenth follow-up:
[level-two-three-invertible-l1-l0-cut-normal-form.md](level-two-three-invertible-l1-l0-cut-normal-form.md)
normalizes the cross-invertible open subbranch of the surviving
$3I+1R+2Z$ pattern.  Overlapping L1 rows align all endpoint-star families
with the selected stars and kill their zero-site factors.  The two
target-zero mixed L0 slices are then core-versus-zero cut gauges, not
one-star kernels, and the pure-triangle determinant cover reduces to the
automatic scalar identity
$(a_0b_0)(a_1b_1)=(a_0b_1)(a_1b_0)$.  This explains why the existing
star-lift and triangle-cover arguments do not close the branch.  The
one-column rank-one-site and singular-cross-spoke boundaries remain.

Twentieth follow-up:
[level-two-two-invertible-r2-guard.md](level-two-two-invertible-r2-guard.md)
shows that no unconditional rank drop extends to exactly two invertible
endpoint matrices.  An exact $2I+2R+2Z$ packet satisfies the generic-kernel
equations, all selected L2 rows, literal R2 exits at all six roots, and has
differential rank $55$ with exactly the five gauge kernels.  Hence any
closure of the fewer-invertible frontier must again use L0/L1 or overlapping
blocks.

Twenty-first follow-up:
[level-two-two-invertible-l0-obstruction.md](level-two-two-invertible-l0-obstruction.md)
excludes that exact two-invertible guard from a full solution.  Its
full/mixed ranks are $55/55$, neither pure target lies in the tangent image,
and adjoining both raises the rank to $57$.  A replacement with the same
endpoint matrices and multipliers must change at least one of the eight free
zero-multiplier blocks and land on the rank-$55/53$ tangent-incidence locus.
This is an exact-packet obstruction, not a closure of the $2I+2R+2Z$
stratum.

Twenty-second follow-up:
[binary-ghz8-rank53-second-order-normal-obstruction.md](binary-ghz8-rank53-second-order-normal-obstruction.md)
resolves the two wider tangent classes at the exact rank-$53$ seed to the
next order.  The full tangent kernel splits as the $26$ chart directions
plus two exact normal lifts $T_0,T_1$.  Three sparse Jacobian-cokernel
functionals annihilate all $351$ chart--chart and all $52$ chart--normal
quadratic terms, while their values on
$H(T_0,T_0),B(T_0,T_1),H(T_1,T_1)$ form a nonsingular diagonal matrix.
Thus a first derivative with normal coordinates $(a,b)$ has unavoidable
second-order obstructions proportional to $a^2,ab,b^2$, and no such
derivative lifts to second order unless $a=b=0$.  This is a formal-local
result at one seed: it does not exclude an arc leaving after a chart-tangent
first jet or a distant rank-$54/55$ component.

Twenty-third follow-up:
[level-two-two-invertible-l0-incidence-survivor.md](level-two-two-invertible-l0-incidence-survivor.md)
shows that the linear L0 screen is genuinely sharp inside the
$2I+2R+2Z$ normal form.  Replacing the eight free zero-multiplier blocks
gives an exact packet with full/mixed ranks $55/53$, both pure targets in
the tangent image, exactly the five gauge kernels, and all selected L2 and
R2 equations.  A follow-up audit repaired a stale `run_path` globals
substitution in the checker; the replacement itself passes every audit,
with corrected slope support $29/64$, and no conclusion changed.

Twenty-fourth follow-up:
[level-two-two-invertible-factored-l0-cut-obstruction.md](level-two-two-invertible-factored-l0-cut-obstruction.md)
excludes that sharp linear survivor from a physical endpoint completion.
For the pure-zero preimage, the $224$ cubic rank-two minors on the cut
$\{0,1\}\mid\{2,3,4,5\}$ generate the unit ideal over both $\mathbb Q$
and $\mathbb F_{32003}$ in all six gauge variables.  Hence no gauge
representative has the two-star cut rank required by factored L0.  The
obstruction remains packet-specific rather than stratum-wide.

Twenty-fifth follow-up:
[level-two-three-invertible-l0-incidence-survivor.md](level-two-three-invertible-l0-incidence-survivor.md)
finds the analogous sharp point in the last exactly-three-invertible
pattern.  Changing only $M_{34}(1,0)$ from $2$ to $0$ in the original
$3I+1R+2Z$ guard changes the exact full/mixed ranks from $55/55$ to
$55/53$ and puts both pure targets in the tangent image, while preserving
the generic-kernel equations, the five-gauge kernel, selected L2, and all
six R2 exits.  Thus even on the hard frontier, tangent incidence alone is
not a contradiction.

Twenty-sixth follow-up:
[level-two-three-invertible-factored-l0-cut-obstruction.md](level-two-three-invertible-factored-l0-cut-obstruction.md)
excludes that one-scalar survivor at the first factored-L0 screen.  The same
pure-zero cut has $224$ cubic minors whose ideal is $(1)$ over $\mathbb Q$
and $\mathbb F_{32003}$ in the six unrestricted gauges.  No physical
shared endpoint-star factorization exists for this exact survivor; a
stratum-wide use of the cut-minor condition remains the open target.

Twenty-seventh follow-up:
[level-two-three-invertible-l1-pure-l0-collinearity-obstruction.md](level-two-three-invertible-l1-pure-l0-collinearity-obstruction.md)
closes the L1-aligned cross-invertible interior of the last
exactly-three-invertible pattern.  Under the two-column rank-one-site and
one-invertible-spoke-per-zero-site hypotheses, every endpoint slice is a
generalized cut gauge
$G(c(1,1,1,1,-1,-1))$.  Its weights sum to $2c$, so the slice output is
still a scalar multiple of the single residual slope $H$, rather than zero.
The two pure L0 equations would therefore make the same $H$ proportional
to both $e_{0^6}$ and $e_{1^6}$; an explicit four-equation unit certificate
gives the contradiction.  This is a genuine stratum-level closure.  The
remaining $3I+1R+2Z$ frontier is confined to a one-column rank-one site,
a zero site without an invertible triangle spoke, or a rank/kernel-drop
boundary.

Twenty-eighth follow-up:
[level-two-three-invertible-incidence-torus-cut-obstruction.md](level-two-three-invertible-incidence-torus-cut-obstruction.md)
upgrades the one-scalar incidence guard to an exact four-parameter family.
Independent nonzero color scalings at the two zero sites preserve the
$55/53$ ranks, both pure tangent incidences, generic kernel, and R2 by
invertible diagonal equivalence of the matching tensor and differential.
The pure-zero cut matrix changes only by invertible row/column factors and
gauge-variable rescaling, so its unit cut-minor ideal persists over the
whole torus.  This is a family obstruction, not the full empirically larger
incidence hyperplane.

Twenty-ninth follow-up:
[binary-ghz8-rank53-chart-jacobian.md](binary-ghz8-rank53-chart-jacobian.md)
proves that the full $256\times112$ GHZ8 Jacobian has Laurent-function-field
rank exactly $84$ on the exact $26$-parameter rank-$53$ chart.  Two explicit
Laurent kernel syzygies supplement the $26$ chart tangents, while the seed
has rank $84$.  Hence the rank is constantly $84$ near the rational seed.
Together with the diagonal quadratic normal obstruction, this closes the
higher-order gap: every formal GHZ8 arc through the seed remains inside the
rank-$53$ chart.  Distant components and rank-$54/55$ sources elsewhere
remain outside this local theorem.

Thirtieth follow-up:
[level-two-three-invertible-gauge-boundary-closure.md](level-two-three-invertible-gauge-boundary-closure.md)
removes the supposed gauge-dependence boundary at rank $55$.  The invertible
triangle and rank-one site form a forced nonbipartite core.  If either zero
site is unattached, only its twenty incident cell columns can contribute and
the differential rank is at most $20$; otherwise both sites attach to the
core, the live graph is connected and nonbipartite, and the five trace-zero
gauges are independent.  At rank $55$ they therefore exhaust the kernel.

Thirty-first follow-up:
[level-two-three-invertible-one-column-t-boundary.md](level-two-three-invertible-one-column-t-boundary.md)
reduces the one-column rank-one-site boundary.  With a dead $t$--zero star,
pure-slice collinearity closes the branch.  With a live star, mixed L0 kills
seven of nine scalar zero patterns.  Each of the two remaining labelled
charts forces the residual slope to be a pure six-site tensor in one color,
the selected vector at $t$ to be the opposite coordinate, and an explicit
five-site star cofactor to be pure in that opposite color.  These two
complementary-purity charts remain to be excluded or realized.

Thirty-second follow-up:
[level-two-three-invertible-singular-cross-l1-boundary.md](level-two-three-invertible-singular-cross-l1-boundary.md)
classifies a zero site without an invertible triangle spoke.  Active L1 data
have one of two mutually exclusive common-factor forms, P/V or Q/U; all
non-common-factor crosses force the zero-site endpoint vectors to vanish and
fall to pure-L0 collinearity.  Mixed L0 synchronizes all four spoke multiples
whenever the relevant physical endpoint product is nonzero.  The corrected
argument makes no R2 or pure-column inference after normalizing the
invertible triangle: independent local $GL_2$ changes do not preserve the
GHZ coordinate axes.  The exact $3I$ incidence survivor and its
four-parameter torus are non-common-factor and therefore fail L1
independently of their cut-minor obstruction.

Thirty-third follow-up:
[level-two-three-invertible-one-column-pure-tensor-obstruction.md](level-two-three-invertible-one-column-pure-tensor-obstruction.md)
excludes both complementary-purity charts left by the one-column reduction
when each zero shore has an invertible triangle spoke.  The triangle cofactor
map from six spoke-column coordinates to a three-site tensor is injective.
At the pure colour on the rank-one site, three zero shore corners then force
the fourth corner to vanish, contradicting the required nonzero pure tensor.
The additional pure five-site cofactor condition is not needed.

Thirty-fourth follow-up:
[level-two-three-invertible-one-column-singular-overlap.md](level-two-three-invertible-one-column-singular-overlap.md)
removes the invertible-spoke hypothesis from those terminal charts.  A
nonzero pure five-site cofactor makes both relevant shore slices nonzero.  If
either shore pair is independent, the same forbidden-corner argument closes
the chart; if both are dependent, injectivity gives a fixed physical factor
on each shore and the coordinate-shore path theorem bounds the differential
rank by $49$.  Thus the terminal one-column boundary has no singular-spoke
escape.  This does not yet derive the terminal conditions on the
double-boundary intersection where the rank-one site is one-column and a
zero site simultaneously lacks an invertible triangle spoke.

Thirty-fifth follow-up:
[level-two-three-invertible-common-factor-l1-closure.md](level-two-three-invertible-common-factor-l1-closure.md)
closes the common-factor singular-cross forms covariantly.  Uniform spoke
stars are radial gauges.  Every nonuniform same-type correction shares its
physical zero-site factor or factors, and every opposite-type correction,
including the zero--zero edge, shares one factor from each zero site.  Pure
flattening forces those factors onto one physical coordinate, while the
other pure slice requires a nonzero complementary coordinate that every
matching kills.  This proof supersedes the earlier normalized-coordinate
R2 shortcut and leaves the certified spine unchanged.

Thirty-sixth follow-up:
[level-two-two-invertible-l1-collinearity-obstruction.md](level-two-two-invertible-l1-collinearity-obstruction.md)
excludes the exact rank-$55/53$ two-invertible incidence survivor at
overlapping L1.  The single invertible core edge initially leaves two skew
modes, but either two-column rank-one neighbour kills both.  An invertible
core spoke then kills the endpoint factors at each zero site, making every
L0 slice collinear with one residual matching tensor and contradicting the
two physical pure targets.  The theorem covers the two-column,
invertible-spoke subbranch of $2I+2R+2Z$; its one-column and singular-cross
boundaries remain open.

Thirty-seventh follow-up:
[level-two-three-invertible-one-column-dead-tz-common-factor-closure.md](level-two-three-invertible-one-column-dead-tz-common-factor-closure.md)
closes the pre-terminal one-column/singular-cross intersection when both
rank-one-site-to-zero residual blocks vanish.  The exceptional $t$-star and
uniform P/V zero stars are radial gauges; mixed L0 kills every nonuniform
star in both mixed slices.  At most one pure correction remains, and its
physical common zero factors contradict the complementary pure coordinate.
The only exactly-three-invertible overlap still outside the combined
theorems has at least one live $t$-to-zero block.

Thirty-eighth follow-up:
[level-two-two-invertible-three-rank-one-one-zero-closure.md](level-two-two-invertible-three-rank-one-one-zero-closure.md)
bounds the determined-zero-shore subcase of $2I+3R+1Z$.  If every
$z$--$R$ multiplier is nonzero, those blocks vanish and the zero-sum graph
on the three rank-one sites gives the exact coordinate-shore bounds
$35,42,49$, or $51$.  The triangle case uses all three symmetric
$J$-orthogonality equations to force a common isotropic line.  Hence rank
$55$ requires a free zero-multiplier $z$--$R$ block; that is the sharply
isolated remaining boundary in this endpoint pattern.

Thirty-ninth follow-up:
[level-two-three-invertible-one-column-single-live-uniform-cross-closure.md](level-two-three-invertible-one-column-single-live-uniform-cross-closure.md)
closes the first live-$tZ$ part of the last exactly-three-invertible
intersection.  With one live block, one uniform active common-factor zero,
and the other zero endpoint inactive, two exact radial identities reduce
every slice modulo gauges to a literal edge tangent.  The first physical
flattening makes that edge and its four-site cofactor pure; the full
matching decomposition then equates a rank-one shore tensor to the
difference of two complementary nonzero pure tensors.  Remaining live
overlaps include nonuniform common-factor crosses, endpoint-inactive
singular shores outside that chart, and two active/live zero sites.

Fortieth follow-up:
[level-two-two-invertible-four-zero-potential-separation.md](level-two-two-invertible-four-zero-potential-separation.md)
closes the separated-potential part of $2I+4Z$.  Residual R2 partitions the
four zero endpoints into two witness pairs attached to the two invertible
sites.  Generic-kernel multipliers leave only three support envelopes, with
respectively $4,7,7$ edges whose complementary cofactor can be nonzero.
Thus the differential rank is at most $16,28,28$.  The only multiplier
boundary omitted by this argument is equality of the two invertible-site
potentials.

Forty-first follow-up:
[level-two-two-invertible-four-zero-equal-potential-closure.md](level-two-two-invertible-four-zero-equal-potential-closure.md)
closes that equal-potential boundary and hence the full $2I+4Z$ stratum.
The common R2 witness set contains two, three, or four zero endpoints.
Generic-kernel multipliers leave seven support envelopes; their exact
cofactor-edge counts are $6;3,12;1,5,10,6$, so the maximum differential
rank is $48$.  Together with the separated-potential bound, no
$2I+0R+4Z$ packet reaches rank $55$ before L0 or L1 is needed.

Forty-second follow-up:
[level-two-three-invertible-one-column-single-live-inactive-cross-closure.md](level-two-three-invertible-one-column-single-live-inactive-cross-closure.md)
closes the endpoint-inactive single-live part of the final $3I$ overlap,
with arbitrary singular triangle-to-zero spokes.  The exceptional $t$-star
again reduces modulo gauges to the literal live edge.  One flattening makes
that edge and its four-site cofactor pure, while the full $3+6+6$ matching
decomposition has a common physical factor at $t$ and contradicts the two
complementary pure tensors.  The live residue now requires active
nonuniform/opposite-type data or a second active/live zero site.

Forty-third follow-up:
[level-two-two-invertible-three-rank-one-one-zero-free-edge-closure.md](level-two-two-invertible-three-rank-one-one-zero-free-edge-closure.md)
closes the free-edge boundary and hence the full $2I+3R+1Z$
generic-kernel stratum.  The zero-to-rank-one free set and exceptional
rank-one-shore graph have exactly nine potential patterns.  Zero cofactor
columns, exact shore-slice counts, a three-free-edge Segre decomposition, a
two-kernel zero-potential triangle, and a one-dimensional composite-fiber
tangent give covariant bounds $44,51,46,54,50,53$ on the necessary
branches.  Their maximum is $54$, while the determined-zero-shore theorem
already bounds the complementary branch by $51$.

Forty-fourth follow-up:
[level-two-three-invertible-one-column-single-live-nonuniform-cross-closure.md](level-two-three-invertible-one-column-single-live-nonuniform-cross-closure.md)
closes the remaining single-live charts with the other zero endpoint
inactive.  Mixed localization separates the live-edge and nonuniform P/V
stars; exact pair-shore and selected-basis cofactor equations contradict
the only pure chart.  In the opposite Q/U type, L1 makes the live block and
every matching/derivative share one physical shore factor, immediately
contradicting the two pure targets.  The last exactly-three-invertible
overlap therefore has a second active zero endpoint or two live $tZ$
blocks.

Forty-fifth follow-up:
[level-two-two-invertible-four-rank-one-balanced-k22-closure.md](level-two-two-invertible-four-rank-one-balanced-k22-closure.md)
closes the balanced $K_{2,2}$ potential graph in $2I+4R$.  Its paired-shore
normal form has two coefficient-independent rectangle kernels transverse
to the five vertex gauges, so the differential rank is at most $53$.  An
exact physical-coordinate packet has rank $52$ and satisfies generic
kernel, all selected L2 rows, and literal R2 at all six roots; the extra
empirical kernel is not used in the theorem.  The isolated, disjoint-pair,
$K_{1,3}$, and all-zero potential graphs remain open.

Forty-sixth follow-up:
[level-two-three-invertible-one-column-single-live-other-active-cross-closure.md](level-two-three-invertible-one-column-single-live-other-active-cross-closure.md)
closes every exactly-one-live $tZ$ chart with the other zero endpoint
active.  L1 forces the dead-side activity to have P/V type; consequently
every base matching and every endpoint-tangent derivative carries its
fixed physical zero-site factor.  The two pure targets cannot share that
shore.  Together with the inactive, uniform, nonuniform, and opposite-type
single-live theorems, this leaves only the two-live $tZ$ pre-terminal
intersection in the exactly-three-invertible branch.

Forty-seventh follow-up:
[level-two-two-invertible-four-rank-one-disjoint-pair-closure.md](level-two-two-invertible-four-rank-one-disjoint-pair-closure.md)
sharply closes the disjoint-pair potential graph in $2I+4R$.  The covariant
support class has dimension 32, but its matching tensor factors through a
24-parameter six-tensor map with four universal scaling/translation
kernels.  Its support-preserving image has dimension at most 20; adding 28
transverse cell directions gives rank at most $48$.  An exact
physical-coordinate packet attains rank 48 and passes generic kernel,
selected L2, and literal six-root R2.  The $K_{1,3}$, all-zero, and
isolated-vertex potential graphs remain.

Forty-eighth follow-up:
[level-two-two-invertible-one-rank-one-three-zero-equal-core-potential-closure.md](level-two-two-invertible-one-rank-one-three-zero-equal-core-potential-closure.md)
closes the equal-core-potential subcase of $2I+1R+3Z$.  R2 forces at
least one zero endpoint with the opposite potential.  The resulting seven
support envelopes have active cell-column counts
$48,20,56,4,16,28,28$; in the sole 56-column envelope, four identically
zero edge columns are transverse to the five gauges, giving rank at most
$51$.  Every other envelope has a direct bound at most $48$.  Unequal core
potentials remain to be classified.

Forty-ninth follow-up:
[level-two-two-invertible-four-rank-one-k13-closure.md](level-two-two-invertible-four-rank-one-k13-closure.md)
closes the $K_{1,3}$ potential graph in $2I+4R$.  The 35-parameter
star-shore support factors through 28 effective parameters, with three
scaling and three distinguished-line translation kernels.  Its restricted
image has dimension at most 22; adding 25 transverse directions gives rank
at most $47$.  A physical-coordinate calibration has rank 44 and passes
generic kernel, selected L2, and literal R2.  Only all-zero and
isolated-vertex potential graphs remain in this endpoint pattern.

Fiftieth follow-up:
[level-two-three-invertible-one-column-double-live-factor-complete-closure.md](level-two-three-invertible-one-column-double-live-factor-complete-closure.md)
reduces the final two-live $3I$ intersection.  Any Q/U activity forces its
live block to share the physical zero-side factor, and the two pure targets
contradict the resulting fixed shore.  The same closes every aligned P/V
live block.  The exact remaining type grid is
$(I,I),(I,P),(P,I),(P,P)$, with every active P/V live block misaligned; the
three matching shores and all four star-derivative shore censuses are now
explicit for the next mixed-L0 step.

Fifty-first follow-up:
[level-two-two-invertible-one-rank-one-three-zero-distinct-invertible-potential-closure.md](level-two-two-invertible-one-rank-one-three-zero-distinct-invertible-potential-closure.md)
closes every $2I+1R+3Z$ branch with distinct invertible-site potentials.
R2 eliminates a noncoordinate rank-one shore factor; in the coordinate
case the two nonempty zero-attachment sets produce eleven inequivalent
zero-sum support envelopes.  Their exact active-cell counts range from 12
to 48, directly excluding rank 55.  Together with the equal-core theorem,
the sole remaining multiplier boundary is $\nu_0=\nu_1\ne\nu_r$.

Fifty-second follow-up:
[level-two-two-invertible-four-rank-one-all-zero-closure.md](level-two-two-invertible-four-rank-one-all-zero-closure.md)
closes the all-zero potential graph in $2I+4R$.  Pairwise symmetric-$J$
orthogonality forces all four rank-one source factors onto one isotropic
line, hence the spokes from either invertible site are constant across the
shore.  Four cross-spoke cancellation directions meet the five gauges in
one dimension, giving an eight-dimensional kernel and rank at most $52$.
An exact rank-42 physical packet passes generic kernel, selected L2, and
literal R2.  Only potential graphs with an isolated rank-one vertex remain
in this endpoint stratum.

Fifty-third follow-up:
[level-two-three-invertible-one-column-double-live-mixed-residue-reduction.md](level-two-three-invertible-one-column-double-live-mixed-residue-reduction.md)
computes the exact generalized-gauge quotient on the final two-live $3I$
type grid.  A nonzero gauge relation exists exactly when every active P/V
spoke triple is uniform and every inactive spoke shore vanishes.  Mixed L0
leaves one pure correction colour.  The inactive/inactive chart reaches the
covariant terminal theorem and closes; the P-containing charts retain an
exact three-shore source decomposition, with no unsupported independence
claim between its components.

Fifty-fourth follow-up:
[level-two-two-invertible-one-rank-one-three-zero-equal-invertible-potential-closure.md](level-two-two-invertible-one-rank-one-three-zero-equal-invertible-potential-closure.md)
closes $\nu_0=\nu_1\ne\nu_r$ and hence the full $2I+1R+3Z$
generic-kernel/R2 stratum.  Physical R2 gives a nonempty common
zero-attachment set, with threshold one for a coordinate rank-one shore
and two otherwise.  Thirteen zero-sum support envelopes remain; their
exact active-cell counts are all at most 48.  Combined with the equal-core
and distinct-invertible-potential theorems, no multiplier branch reaches
rank 55.

## Current level-two endpoint-rank map

The chronological results above now give the following compact map on the
rank-$55$ generic-kernel/R2 branch.

* Four or more invertible endpoint matrices are closed by the singular-star
  budget and pair-pencil/constant-spoke bounds.
* With exactly three invertible endpoints, the $3I+3R$, $3I+2R+1Z$, and
  $3I+3Z$ patterns are closed by coordinate-shore factorizations.  The sole
  pattern that reached rank 55, $3I+1R+2Z$, is now closed as well.  Its last
  one-column, double-live P/V residue has a three-site coordinate shore:
  directly in the double-P chart, and after pure-cofactor injectivity fixes
  the inactive shore in either one-P chart.  Thus the entire
  exactly-three-invertible endpoint regime is closed.
* With exactly two invertible endpoints, the full $2I+4R$,
  $2I+3R+1Z$, $2I+1R+3Z$, and $2I+4Z$ strata are closed.  The middle
  $2I+2R+2Z$ pattern still has genuine rank-$55$ guards.  Its exact linear
  incidence survivor is excluded both by a factored-L0 cut and by
  overlapping L1 on the two-column/invertible-spoke subbranch.  The complete
  same-missing-column boundary is closed: the nonzero-cross dense ray has
  rank at most 51, and all zero-cross envelopes have rank at most 52.
  On the transverse missing-column boundary, 38 of 39 potential envelopes
  have rank at most 52.  Its dense ray has an exact rank-55
  generic-kernel/R2 guard, although that fixed packet fails linear L0.  A
  second exact rank-55 packet attains the sharp 55/53 linear-incidence
  ranks but fails literal R2 only at root 0; whether the dense incidence
  locus meets full R2 remains open; all sixteen zero-cell affine lifts on
  the site-\(4\) and site-\(5\) spokes of the rank-\(54/52\) full-R2
  boundary are now excluded.  The first genuinely two-cell repair plane
  has full R2 on exactly two parameter lines, and a sixth polynomial kernel
  bounds the differential rank by 54 on both; the complementary point has
  rank \(55/53\) but fails R2.  The same conclusion holds for the other
  three sharp minimal two-cell repair planes, so all four one-cell
  rank-raising directions and their minimal alternate-spoke repairs are
  excluded.  In the
  asymmetric one-column/two-column
  chart, L1 closes all four active-active zero charts at rank at most 49,
  and the four one-active charts are closed at rank at most 42.  Full
  mixed-star purity now closes the inactive-inactive cofactor-kernel
  residue as well, so the entire asymmetric one-column/two-column chart is
  closed.  The two-column/two-column chart is also closed without any
  invertible-spoke hypothesis: an active zero gives rank at most 42, while
  two inactive zeros fail pure-L0 collinearity.  Thus the full-R2 dense
  transverse incidence intersection is the sole remaining
  exactly-two-invertible endpoint pattern.
* Endpoint patterns with at most one invertible matrix remain outside the
  current rank-pattern closure.  In particular, the all-zero-potential
  $1I+5Z$ component contains an exact rank-55 selected-block/R2 guard, so
  generic kernel and those residual R2 rows cannot close this regime.  That
  fixed packet nevertheless fails linear L0 because neither pure target
  lies in its residual differential image.  A second exact packet passes
  both pure-target incidence tests but fails the already known factored
  pure-zero cut.  On a third exact packet, each physical pure target
  separately has a literal shared-star preimage with all other slices zero,
  but the two assignments cannot be synchronized on that residual packet.
  A sparse minimal coupling does realize all four slices and residual R2,
  but its full diagonal-torus family has constant differential rank 38;
  the enlarged natural sparse-support deformation chart is rigid on that
  orbit as well.  The same construction and rigidity statement hold with
  one arbitrary rank-one selected matrix or with all selected matrices
  zero, uniformly covering \(1R+5Z\) and \(6Z\); two R2-capable roots may
  also be activated together on one isotropic pencil, reaching a shared
  \(2R+4Z\) full-L0 boundary at the same rank \(38/36\).  Both one-site
  patterns also reach
  the same rank-55/53 boundary as \(1I+5Z\), with separate literal
  factorizations of the two pure targets but the same fixed-packet
  simultaneous obstruction.  More generally, a common isotropic selected
  pencil on any subset of four R2-capable roots extends this rank-55/53
  boundary through every \(kR+(6-k)Z\) pattern with \(0\le k\le4\).  A
  two-block residual repair supplies the missing witnesses at the last two
  roots without changing rank or either factored pure tangent, extending
  the exact boundary through \(5R+1Z\) and \(6R\) as well.  The repaired
  packet still has no simultaneous four-slice compatibility: its modified
  weakened four-edge factor ideal is again the unit ideal over \(\mathbb Q\)
  and \(\mathbb F_{32003}\).  The first one-block escape,
  \(M_{05}=E_{01}\), makes that four-edge ideal non-unit without losing
  rank or R2, but adjoining the unchanged edge \(14\) restores the unit
  ideal.  Changing both \(M_{05}=M_{14}=E_{01}\) escapes every
  independent-edge equation on the full \(K_4\), but the actual
  vertex-sum gauge coupling again generates the unit ideal; a viable
  deformation must evade that coupling itself.
  In the separate
  \(1I+5R\) stratum, the zero-sum potential
  graph reduces every rank-55 survivor to the connected antipodal-pencil
  types \(K_{1,4}\) and \(K_{2,3}\); a five-site coordinate core now
  bounds the \(K_{1,4}\) type by 42, while nine exact polynomial syzygies
  bound the full \(K_{2,3}\) type by 51.  All other graph types have rank
  at most 51, so the complete \(1I+5R\) stratum is closed.
  The all-zero selected \(6Z\) chart inherits the two separate rank-55
  factored pure assignments and also admits the shared rank-38 coupling;
  the same enlarged sparse deformation chart is rigid on its diagonal
  orbit.  These endpoint strata therefore
  remain open beyond the audited simultaneous-compatibility families.

These statements are research evidence only.  They do not alter the
certified spine or prove **SP-CLEAN-BRIDGE**.

Fifty-fifth follow-up:
[level-two-two-invertible-four-rank-one-complete-closure.md](level-two-two-invertible-four-rank-one-complete-closure.md)
closes the full $2I+4R$ generic-kernel stratum at rank at most 53.  The
zero-sum graph on four rank-one sites has four no-isolated types:
$2K_2,K_{1,3},K_{2,2},K_4$.  This includes the omitted
$(0,0,\lambda,-\lambda)$ realization of $2K_2$.  Every other graph has an
isolated vertex; the other three sites form a coordinate shore with exact
bounds $35,42,49,51$, including the covariantly constant triangle case.
Together with the four graph-specific theorems, this exhausts the stratum.

Fifty-sixth follow-up:
[level-two-two-invertible-same-column-potential-boundary.md](level-two-two-invertible-same-column-potential-boundary.md)
classifies the same-column $2I+2R+2Z$ boundary when the rank-one cross
potential is nonzero.  A signed zero-sum census gives 39 covariant support
envelopes.  Thirty-eight have at most 52 active differential columns; the
unique dense envelope is
$\tau(1,1,1,1,-1,-1)$ and has an exact rank-55 calibration.  Thus support
alone cannot close that ray, while every non-dense potential pattern in
this boundary is eliminated.

Fifty-seventh follow-up:
[level-two-one-invertible-five-zero-r2-guard.md](level-two-one-invertible-five-zero-r2-guard.md)
exhibits an exact rank-55 packet in the all-zero-potential $1I+5Z$
component.  The generic-kernel and selected level-two equations are
identically zero for arbitrary residual $M$; the chosen packet realizes all
six audited residual R2 alternatives.  This is a selected-block guard only,
not an L0/L1, overlap, global-R2, or full-source construction.

Fifty-eighth follow-up:
[level-two-three-invertible-one-column-double-live-p-residue-closure.md](level-two-three-invertible-one-column-double-live-p-residue-closure.md)
closes all P-containing double-live charts at rank at most 49 and therefore
completes the exactly-three-invertible endpoint regime.  The double-P chart
is already a coordinate-shore path.  In either one-P chart, physical purity
forces the active factor to the complementary colour and makes the
four-site cofactor pure; injectivity fixes the inactive shore and reaches
the same path theorem.

Fifty-ninth follow-up:
[level-two-two-invertible-same-column-dense-ray-closure.md](level-two-two-invertible-same-column-dense-ray-closure.md)
closes the unique dense nonzero-cross same-column ray at rank at most 51.
The exact common-factor grid creates four universal differential syzygies
independent of the five vertex gauges.  This also explains why the enlarged
support calibration at rank 55 was not an exact generic-kernel packet on
the dense ray.

Sixtieth follow-up:
[level-two-two-invertible-same-column-zero-cross-closure.md](level-two-two-invertible-same-column-zero-cross-closure.md)
closes $\nu_2+\nu_3=0$ in the same-missing-column $2I+2R+2Z$ branch.
Eighteen of nineteen potential envelopes have at most 52 active columns.
The sole 60-column envelope has four rectangle syzygies whose intersection
with the five gauges is one-dimensional, again giving rank at most 52.
Together with the two nonzero-cross theorems, this closes every
same-missing-column chart.

Sixty-first follow-up:
[level-two-one-invertible-five-zero-l0-obstruction.md](level-two-one-invertible-five-zero-l0-obstruction.md)
excludes the exact $1I+5Z$ guard at linear L0.  Its residual differential
has rank 55, but adjoining either physical pure target raises rank to 56
and adjoining both raises it to 57, over the rationals and two prime
fields.  The universal endpoint-slice identity puts every completion slice
inside that differential image, so none of the 192 outside cells can repair
this packet.  The result is packet-specific; the all-zero-potential
$1I+5Z$ component remains open.

Sixty-second follow-up:
[level-two-two-invertible-transverse-column-potential-boundary.md](level-two-two-invertible-transverse-column-potential-boundary.md)
maps the opposite-missing-column $2I+2R+2Z$ chart.  Thirty-eight of its 39
potential envelopes have at most 52 active differential columns.  The
unique exception is again
$\tau(1,1,1,1,-1,-1)$, but here an exact normalized packet has rank 55,
satisfies all generic-kernel and selected rows, and realizes residual R2 at
all six roots with invertible spokes at both zero sites.  This dense ray is
a genuine L0/L1 frontier rather than a support-only artifact.

Sixty-third follow-up:
[level-two-two-invertible-transverse-column-l0-obstruction.md](level-two-two-invertible-transverse-column-l0-obstruction.md)
excludes the displayed dense transverse guard at linear L0.  Its mixed-row
rank remains 55 and adjoining the two pure targets raises rank to 57 over
the rationals and three primes.  This is packet-specific: the other 32-cell
choices on the same dense ray still require L0/L1 analysis.

Sixty-fourth follow-up:
[level-two-two-invertible-asymmetric-one-column-l1-boundary.md](level-two-two-invertible-asymmetric-one-column-l1-boundary.md)
maps the mixed one-column/two-column L1 geometry.  The two-column endpoint
kills both core skew modes; the one-column endpoint leaves exactly one
scalar star defect.  Both-zero-active charts have a three-site
coordinate-shore path and rank at most 49.  A rank-55 survivor must contain
an inactive zero whose three full-column spokes have no common right factor.

Sixty-fifth follow-up:
[level-two-one-invertible-five-zero-l0-incidence-survivor.md](level-two-one-invertible-five-zero-l0-incidence-survivor.md)
rebinds the exact two-invertible incidence-survivor residual packet to the
all-zero-potential $1I+5Z$ endpoint data.  It retains rank 55, selected R2,
mixed-row rank 53, and both pure targets in the differential image.  Thus
linear L0 incidence does not close this component.  The same residual
packet is already excluded by the factored pure-zero cut, so this remains a
sharp boundary witness rather than a full-source survivor.

Sixty-sixth follow-up:
[level-two-two-invertible-transverse-column-l0-incidence-survivor.md](level-two-two-invertible-transverse-column-l0-incidence-survivor.md)
exhibits a dense transverse packet with exact differential/mixed ranks
\(55/53\) and both physical pure targets in the differential image over the
rationals and three primes.  It preserves the generic kernel and selected
rows, but literal R2 fails exactly at invertible root 0.  Thus linear L0
incidence is nonempty on the dense ray, while its intersection with full R2
remains open.

Sixty-seventh follow-up:
[level-two-two-invertible-asymmetric-one-column-inactive-l0-reduction.md](level-two-two-invertible-asymmetric-one-column-inactive-l0-reduction.md)
reduces the asymmetric inactive-inactive chart to one covariant rank-five
cofactor map.  Its kernel is the antisymmetric line \((p,-p,0)\).  If no
zero shore carries a nonzero kernel column or kernel difference, both zero
shores factor and the coordinate-path theorem gives rank at most 49.
Accordingly every rank-55 survivor has an explicit nonzero carrier on the
two invertible spokes and no correction on the two-column spoke.

Sixty-eighth follow-up:
[level-two-two-invertible-asymmetric-one-active-cofactor-kernel-normal-form.md](level-two-two-invertible-asymmetric-one-active-cofactor-kernel-normal-form.md)
closes all four ordered one-active asymmetric charts.  In the P/V-active
case, pure L0 and a rank-five cofactor kernel force the two-column root to
have one fixed factor; in the separately derived Q/U-active case, L1 fixes
the active root directly.  The universal fixed-root count gives
\(\operatorname{rank}d\Psi_M\le32+10=42\) in every one-active chart.

Sixty-ninth follow-up:
[level-two-one-invertible-five-zero-factored-pure-slice-boundary.md](level-two-one-invertible-five-zero-factored-pure-slice-boundary.md)
rebinds the universal sharp-incidence packet to the all-zero-potential
\(1I+5Z\) chart.  Two separate literal endpoint-star assignments realize
\((e_{0^6},0,0,0)\) and \((0,0,0,e_{1^6})\), respectively, while retaining
rank \(55/53\), the selected rows, and residual R2.  The existing
unit-ideal certificate still excludes one assignment realizing all four
required slices simultaneously, locating the packet's obstruction at
shared four-slice compatibility rather than individual factorization.

Seventieth follow-up:
[level-two-two-invertible-asymmetric-one-column-inactive-l0-closure.md](level-two-two-invertible-asymmetric-one-column-inactive-l0-closure.md)
closes the final inactive-inactive asymmetric chart.  A literal cofactor
kernel column contradicts complementary physical roots by a
rank-two/rank-one star slice.  Full mixed-star purity sees the remaining
difference kernels, forces both zero cofactors onto one physical product
line, and then fixes every block incident with the two-column site to one
root.  The resulting bound is \(32+10=42\).  Together with the active
charts, this closes the full asymmetric one-column/two-column boundary.

Seventy-first follow-up:
[level-two-two-invertible-transverse-column-one-cell-r2-obstruction.md](level-two-two-invertible-transverse-column-one-cell-r2-obstruction.md)
excludes all eight affine one-cell lifts supported on zero entries of the
four site-\(4\) spokes from the rank-\(54/52\), full-R2 transverse boundary.
Four sharp \(55/53\) lifts destroy the sole R2 exit at root 0 or 1, three
lines retain a sixth polynomial kernel and rank at most 54, and two exact
mixed minors exclude the final line at every nonzero parameter.  General
multi-cell motion in the 32 free scalars remains open.

Seventy-second follow-up:
[level-two-two-invertible-two-column-singular-spoke-closure.md](level-two-two-invertible-two-column-singular-spoke-closure.md)
removes the invertible-spoke hypothesis from the two-column/two-column L1
theorem.  At each zero, overlapping L1 gives exact types I, P, and Q.  Any
P/Q-active zero fixes all four core spokes and, with \(M_{45}=0\), all five
incident blocks, so rank is at most \(32+10=42\).  If both zeros are
inactive, every endpoint slice is an aligned generalized gauge and the two
pure L0 targets are impossibly collinear.  This closes the complete
two-column/two-column boundary, including arbitrary singular spokes.

Seventy-third follow-up:
[level-two-two-invertible-transverse-column-site5-one-cell-r2-obstruction.md](level-two-two-invertible-transverse-column-site5-one-cell-r2-obstruction.md)
classifies all eight zero-entry affine lifts on the site-\(5\) spokes of
the full-R2 transverse boundary.  Every line preserves R2, the generic
kernel, and selected rows, but an exact sixth polynomial kernel of degree
at most three forces differential rank at most 54 for every parameter.
Together with the site-\(4\) theorem, all 16 zero-entry one-cell lifts are
excluded; the remaining search is genuinely multi-cell.

Seventy-fourth follow-up:
[level-two-one-invertible-minimal-gauge-coupled-l0-family.md](level-two-one-invertible-minimal-gauge-coupled-l0-family.md)
couples the two factored pure assignments into one exact endpoint-star
packet with both mixed tangents equal to vertex gauges.  It realizes all
four L0 slices and selected residual R2, but its differential rank is
\(38\), with mixed rank \(36\).  Diagonal covariance proves these ranks
are constant on the full 12-parameter torus family, rigorously excluding
this minimal coupling ansatz from the rank-55 frontier.

Seventy-fifth follow-up:
[level-two-zero-invertible-six-zero-factored-pure-slice-boundary.md](level-two-zero-invertible-six-zero-factored-pure-slice-boundary.md)
rebinds the sharp rank-\(55/53\) residual packet to \(X_0=\cdots=X_5=0\).
All selected equations vanish and all residual roots preserve the binary
pair, while the two separate factored pure assignments remain exact.
The same simultaneous unit-ideal obstruction applies to this residual
packet, so the \(6Z\) stratum reaches the individual factored faces but
not their intersection on this example.

Seventy-sixth follow-up:
[level-two-two-invertible-transverse-column-minimal-r2-restoration-plane.md](level-two-two-invertible-transverse-column-minimal-r2-restoration-plane.md)
classifies the first genuinely two-cell repair plane through the
rank-\(54/52\), full-R2 transverse boundary.  Full R2 occurs exactly on
two parameter lines, and exact polynomial sixth kernels of degrees one and
four force rank at most 54 throughout them.  The off-locus calibration has
the desired \(55/53\) incidence signature but fails only R2, so more general
multi-cell motion remains the transverse target.

Seventy-seventh follow-up:
[level-two-one-invertible-five-rank-one-potential-reduction.md](level-two-one-invertible-five-rank-one-potential-reduction.md)
maps the \(1I+5R\) zero-sum potential graph.  Isolated vertices and the
complete graph have rank at most 42; the two disconnected graphs have
coordinate-shore bounds 49 and 51.  Every rank-55 survivor is therefore a
connected \(K_{1,4}\) or \(K_{2,3}\) antipodal-pencil residue with two
nonisotropic shore lines, and literal R2 at the invertible root forces
distinct physical output-zero and output-one shore witnesses.

Seventy-eighth follow-up:
[level-two-one-invertible-gauge-coupled-deformation-rigidity.md](level-two-one-invertible-gauge-coupled-deformation-rigidity.md)
enlarges the rank-38 shared-L0 construction to arbitrary blocks on five
residual edges, four independent cross weights, and all eight minimal
endpoint coefficients.  Its exact \(40\)-by-\(34\) Jacobian has rank 25;
the seven residual tangent directions integrate only to the diagonal-torus
orbit, while two further directions are endpoint rescalings.  Hence the
entire nonzero sparse chart retains differential rank \(38/36\).

Seventy-ninth follow-up:
[level-two-zero-invertible-six-zero-gauge-coupled-deformation-rigidity.md](level-two-zero-invertible-six-zero-gauge-coupled-deformation-rigidity.md)
rebinds the shared four-slice construction and its enlarged deformation
chart to \(X_0=\cdots=X_5=0\).  All generic-kernel and selected rows vanish
and all six roots preserve the residual binary pair.  Thus \(6Z\) reaches
the simultaneous four-slice intersection, but the full nonzero sparse
chart still has constant differential rank \(38/36\); higher-support
residual or endpoint deformations remain open.

Eightieth follow-up:
[level-two-at-most-one-active-selected-matrix-gauge-coupled-family.md](level-two-at-most-one-active-selected-matrix-gauge-coupled-family.md)
observes that the shared rank-38 packet works with an arbitrary selected
matrix at one site and zero matrices elsewhere.  Pairwise generic-kernel
numerators and the rare/rare slice vanish identically, while two fixed
internal witnesses give residual R2 at the active root.  Hence one rigid
full-L0 family uniformly covers \(6Z\), \(1R+5Z\), and \(1I+5Z\), with
differential rank \(38/36\) throughout its enlarged sparse chart.

Eighty-first follow-up:
[level-two-at-most-one-active-selected-matrix-factored-pure-boundary.md](level-two-at-most-one-active-selected-matrix-factored-pure-boundary.md)
rebinds the sharp rank-\(55/53\) factored-pure packet across selected ranks
zero, one, and two at a single active site.  Thus \(1R+5Z\), like \(6Z\)
and \(1I+5Z\), has separate literal factorizations of both pure faces with
generic-kernel, selected, and residual-R2 data intact.  The four-edge
unit-ideal obstruction still excludes synchronizing those assignments on
this residual packet.

Eighty-second follow-up:
[level-two-up-to-four-rank-one-isotropic-pencil-factored-pure-boundary.md](level-two-up-to-four-rank-one-isotropic-pencil-factored-pure-boundary.md)
activates any subset of four roots of the sharp residual packet with
rank-one selected matrices on one common isotropic input line.  All
pair-pencil numerators and selected rows vanish, while each active root has
two internal pure-column witnesses with nonzero cofactors.  The resulting
sixteen exact guards put every \(kR+(6-k)Z\), \(0\le k\le4\), on the
rank-\(55/53\) separate-factored-pure boundary.  Roots 4 and 5 lack the
second residual witness, so the construction makes no claim for \(5R+1Z\)
or \(6R\).

Eighty-third follow-up:
[level-two-one-invertible-five-rank-one-k14-coordinate-core-closure.md](level-two-one-invertible-five-rank-one-k14-coordinate-core-closure.md)
closes the connected \(1I+5R\) \(K_{1,4}\) antipodal-pencil residue at
rank at most 42.  After covariant local changes, five sites form a
coordinate core and the remaining site is a hub.  Core weights zero/one,
two, and three contribute at most \(12,20,10\), respectively, and higher
weights vanish.  A sharp exact rank-42 calibration shows the support bound
is attained.  Only \(K_{2,3}\) remains in this potential frontier.

Eighty-fourth follow-up:
[level-two-two-invertible-transverse-column-remaining-minimal-r2-restoration-planes.md](level-two-two-invertible-transverse-column-remaining-minimal-r2-restoration-planes.md)
classifies the other three sharp minimal two-cell repair planes.  Each
full-R2 locus is the union of the unlifted axis and one alternate-witness
cancellation line; exact sixth polynomial kernels of degrees at most four
force rank at most 54 on all six lines.  Every off-locus unit calibration
has rank \(55/53\), contains both pure targets, and fails only the intended
R2 root.  More general multi-cell repairs remain open.

Eighty-fifth follow-up:
[level-two-one-invertible-k23-antipodal-pencil-rank-closure.md](level-two-one-invertible-k23-antipodal-pencil-rank-closure.md)
closes the last \(1I+5R\) residue.  In a covariant 24-parameter normal
form, eleven exact polynomial syzygy generators contain nine independent
relations, forcing differential rank at most 51 after every specialization
of the six arbitrary cross blocks.  An exact rank-51 calibration is sharp.
Together with the \(K_{1,4}\) theorem, this closes the full \(1I+5R\)
endpoint-rank stratum before L0, L1, or R2.

Eighty-sixth follow-up:
[level-two-six-rank-one-isotropic-pencil-repaired-factored-pure-boundary.md](level-two-six-rank-one-isotropic-pencil-repaired-factored-pure-boundary.md)
replaces blocks 04 and 15 of the sharp residual packet by oriented
\(E_{10}\) witnesses.  The packet retains differential rank \(55/53\) and
both localized factored pure faces, while all six roots now have two
internal R2 witnesses with nonzero cofactors.  Exhausting all 64 active
subsets on a common isotropic selected pencil puts every
\(kR+(6-k)Z\), \(0\le k\le6\), on this exact boundary.  Simultaneous
four-slice compatibility is excluded on this repaired packet by the next
result.

Eighty-seventh follow-up:
[level-two-six-rank-one-repaired-factor-obstruction.md](level-two-six-rank-one-repaired-factor-obstruction.md)
recomputes the shared factor ideal after the two-block repair.  The repaired
differential still has exactly the five-dimensional gauge kernel.  Even
after weakening all vertex-sum coefficients to independent edge scalars on
the four-edge core, the resulting 64 quadrics in 48 variables generate the
unit ideal over \(\mathbb Q\) and \(\mathbb F_{32003}\).  Thus the exact
\(6R\) boundary packet reaches both factored pure faces separately but has
no shared four-slice completion.

Eighty-eighth follow-up:
[level-two-six-rank-one-m05-near-escape-factor-obstruction.md](level-two-six-rank-one-m05-near-escape-factor-obstruction.md)
changes \(M_{05}\) to \(E_{01}\) on the repaired \(6R\) packet.  Rank
\(55/53\), both separate factored faces, and all six R2 witness pairs
survive.  The original four-edge factor ideal becomes non-unit with reduced
basis size 394, but adding the single unchanged edge \(14\) restores a unit
ideal over \(\mathbb Q\) and \(\mathbb F_{32003}\).  Thus the first local
factor escape cannot extend globally; future searches must move a coupled
core.

Eighty-ninth follow-up:
[level-two-six-rank-one-repaired-factor-obstruction-independent-audit.md](level-two-six-rank-one-repaired-factor-obstruction-independent-audit.md)
independently verifies the repaired factor obstruction using the alternate
core \(01,05,15,45\), which sees the second repaired block, and checks the
Euler/direct-cell gauge reduction explicitly.  It also analyzes the first
two-block escape \(M_{05}=M_{14}=E_{01}\): rank \(55/53\), both pure
incidences, and R2 survive; its full-\(K_4\) independent-edge ideal is
nonunit with basis size 99, but replacing the 24 edge scalars by the 16
actual vertex-sum variables restores a unit ideal over both fields.

Ninetieth follow-up:
[level-two-two-rank-one-four-zero-gauge-coupled-family.md](level-two-two-rank-one-four-zero-gauge-coupled-family.md)
activates either or both R2-capable roots of the shared gauge-coupled packet
with rank-one selected matrices on one isotropic line.  Every pairwise
selected numerator and the rare/rare slice vanish, while roots 2 and 3
retain two internal witnesses with nonzero cofactors.  Thus one shared
four-slice assignment reaches \(2R+4Z\), but only on the same rigid
rank-\(38/36\) sparse chart.

Ninety-first follow-up:
[level-two-one-invertible-three-rank-one-two-zero-potential-boundary.md](level-two-one-invertible-three-rank-one-two-zero-potential-boundary.md)
enumerates all 147 labelled generic-kernel support envelopes in the
\(1I+3R+2Z\) stratum.  Complement matching closes 136 directly, and
fixed-root or exact-syzygy arguments close ten of the eleven dense cases.
The sole residue is the all-spokes potential
\((\lambda,\lambda,\lambda,\lambda,-\lambda,-\lambda)\); an exact
rank-55 selected/R2 packet proves this residue is sharp before L0 or L1.

Ninety-second follow-up:
[level-two-four-rank-one-two-zero-gauge-coupled-repair.md](level-two-four-rank-one-two-zero-gauge-coupled-repair.md)
adds pure-zero cells on 03 and 12 to the shared gauge-coupled packet and
cancels their unwanted complementary matching with one 01 cell.  The same
endpoint stars retain all four literal L0 slices, while the differential
ranks rise to \(42/40\).  Roots 0 through 3 acquire complete R2 witness
pairs, so all sixteen common-isotropic active subsets work and the shared
construction reaches \(4R+2Z\).

Ninety-third follow-up:
[level-two-six-rank-one-gauge-coupled-repair.md](level-two-six-rank-one-gauge-coupled-repair.md)
adds ratio-coupled pure-one pairs and one left-weight pure-zero pair to the
rank-42 shared packet.  Their mixed contributions cancel and shared roots
prevent pure-slice quadratic pollution.  Roots 4 and 5 gain their missing
R2 witnesses, so all 64 common-isotropic active subsets share one literal
four-slice assignment.  This reaches every \(kR+(6-k)Z\) pattern,
including \(6R\), at differential rank \(51/49\).  The final lift is an
exact six-cell affine line through the rank-\(50/48\) packet.  Because all
six roots have R2, one arbitrary invertible selected matrix can also be
placed at any root, giving the same shared packet on \(1I+5Z\).  For the
all-six activation, however, the nonzero-column L1 system has no star mode,
so this packet remains strictly on the shared L0/R2 boundary.  Each of the
six single-invertible placements has two star modes in both L1 systems, but
all four cross-products map to zero and miss both pure targets.  Across all
64 common-isotropic rank-one subsets, only the zero-active \(6Z\) case has
both pure targets in its complete L1 factored-output span.

Ninety-fourth follow-up:
[level-two-one-invertible-two-rank-one-three-zero-potential-boundary.md](level-two-one-invertible-two-rank-one-three-zero-potential-boundary.md)
enumerates all 376 labelled generic-kernel support envelopes in the
\(1I+2R+3Z\) stratum.  Complement matching closes 372 directly.  Each of
the two remaining quotient types has one inactive tangent edge; its four
zero columns are independent of the five universal gauges because deleting
that edge leaves a connected nonbipartite base graph.  Rank is therefore at
most 51 on both dense types and at most 52 everywhere else, closing the
full stratum before L0, L1, or residual R2.

Ninety-fifth follow-up:
[level-two-repaired-full-k4-binary-pair-coupled-census.md](level-two-repaired-full-k4-binary-pair-coupled-census.md)
exhausts all \(16^2=256\) binary choices for the coupled blocks
\((M_{05},M_{14})\) on the repaired rank-one packet.  Eighty-four choices
drop below rank 55.  Each of the remaining 172 rank-55 packets retains the
fixed R2 witnesses but has a unit actual vertex-sum factor ideal already
over \(\mathbb F_{101}\).  Thus this complete discrete coupled box contains
no shared four-slice escape.

Ninety-sixth follow-up:
[level-two-one-invertible-four-rank-one-one-zero-rank-closure.md](level-two-one-invertible-four-rank-one-one-zero-rank-closure.md)
closes the full \(1I+4R+1Z\) generic-kernel stratum before L0, L1, or R2.
Its 621 labelled no-isolate assignments form 14 \(S_4\)-orbits.  Three
coordinate-shore charts, zero-star support counts, one fixed-root chart,
and nine exact polynomial-syzygy charts give
\(\operatorname{rank}d\Psi_M\le51\) throughout; the nine CAS certificates
have one pinned aggregate digest.

Ninety-seventh follow-up:
[level-two-one-invertible-one-rank-one-four-zero-potential-boundary.md](level-two-one-invertible-one-rank-one-four-zero-potential-boundary.md)
enumerates all 675 labelled generic-kernel support envelopes in the
\(1I+1R+4Z\) stratum.  Eighty-four of 85 quotient envelopes have at most
eleven active tangent edges and rank at most 44 directly.  The sole
twelve-edge orbit has an inactive three-edge shore; its twelve zero cell
columns and five gauges overlap in one dimension, again forcing rank at
most 44.  Thus the full stratum closes before L0, L1, or residual R2.

Ninety-eighth follow-up:
[level-two-one-invertible-three-rank-one-all-spokes-endpoint-compatibility.md](level-two-one-invertible-three-rank-one-all-spokes-endpoint-compatibility.md)
adds the missing endpoint equations to the exact rank-55/R2 guard in the
sole `1I+3R+2Z` all-spokes residue.  Both pure L0 targets miss the full
differential image: the mixed-row rank remains 55 and the two augmented
ranks are 56.  Independently, each overlapping L1 star system has two
genuine core modes and no zero-site star, while the enlarged span of all
four factored mode products has rank four and misses both pure targets.
The obstruction persists on the full nonzero local diagonal torus.  The
displayed sharp guard is therefore excluded; only the exceptional
rank-55/53 incidence locus outside that covariant family remains open.

Ninety-ninth follow-up:
[level-two-repaired-arbitrary-pair-coupled-obstruction.md](level-two-repaired-arbitrary-pair-coupled-obstruction.md)
replaces the finite binary \((M_{05},M_{14})\) census by the full
eight-dimensional affine two-block family.  A parameter-independent gauge
minor has determinant \(8\), so every rank-55 specialization has exactly
the vertex-gauge kernel.  Adjoining all eight block entries to the actual
full-\(K_4\), vertex-sum-coupled four-slice ideal gives the unit ideal over
\(\mathbb Q\), independently confirmed in reversed order over
\(\mathbb F_{32003}\).  Thus no rank-55/R2 member of this entire continuous
two-block family is a shared-factor escape; deformations of the other
thirteen residual blocks remain outside the certificate.

One-hundredth follow-up:
[level-two-one-invertible-three-rank-one-all-spokes-incidence-survivor-l1-obstruction.md](level-two-one-invertible-three-rank-one-all-spokes-incidence-survivor-l1-obstruction.md)
exhibits an exact point on the exceptional `1I+3R+2Z` all-spokes incidence
locus left by the Ninety-eighth result.  The single repair
\(M_{34}(0,1):3\mapsto0\) changes the differential profile from
\(55/54\) with only one pure target incident to \(55/53\) with both pure
targets incident.  Pinned maximal minors, rational pure-target preimages,
the exact five-dimensional gauge kernel, and live R2 cofactors certify the
linear-L0 survivor.  Both overlapping L1 systems still have only two
genuine star modes, however, and the four compatible factored products
miss both pure targets, excluding this point and its diagonal torus.  The
rest of the rank-55/53 incidence locus remains open.

One-hundred-first follow-up:
[level-two-six-rank-one-gauge-coupled-four-slice-local-geometry.md](level-two-six-rank-one-gauge-coupled-four-slice-local-geometry.md)
reconstructs the residual four-slice Jacobian at the rank-\(50/48\)
precursor: its exact profile is \(256\)-by-\(60\), rank 45, nullity 15.
The six quadratic exact-line conditions have reduced radial cone equal to
two 11-planes.  Exact function-field syzygies prove sharp differential
maxima \(50/48\) on the flat plane and \(51/49\) on the plane containing
the known lift.  Both sharp calibrations retain complete R2 witness pairs
at all six roots; no full formal-arc or component-wide R2 claim is made.

## Restart checks

1. Read this note, `notes/consolidated-proof-frontier.md`, and
   `certification/BASELINE.md`.
2. Confirm the Git head and preserve the stash; do not pop it over the
   corrected double-polar files.
3. Run `computations/verify_level_two_block_structure_at_eight.py` and
   `computations/verify_level_two_pair_pencil_rank_drop.py` under normal,
   `-O`, and `-I -S`.
4. Modify the certified spine only through an independently audited,
   append-only supersession of a named dependency.
