# Current proof audit and next exact attacks

Audit date: 2026-07-28.

## 1. Bottom line

Krenn's conjecture is **not yet proved by the material in this workspace**.
The arbitrary-complex six-site obstruction and the four-site upper bound are
complete.  The missing theorem is the uniform upper bound for every even
order $n\ge8$.  In particular, the current live-three-zero calculations
close substantial local strata but do not by themselves supply an
all-even-to-six reduction.

The logical dependency is


\[
\text{decorated sources}
 \longrightarrow \text{endpoint-ordered aggregate matrices}
 \longrightarrow \text{a six-site ternary target}
 \longrightarrow \text{six-site impossibility}.
\]

The first and last arrows are rigorous.  The middle arrow is conditional:
[the six-boundary reduction](uniform-six-vertex-reduction.md) requires a cap
whose higher cumulants satisfy

\[
                         L_6+L_4(x+L_2)=0.                 \tag{1}
\]

An exact eight-site binary example in that note shows that an arbitrary cap
need not satisfy (1).  No current note proves that every hypothetical
ternary source has a suitable cap or gives a different unconditional
descent.

### 1.1 Audit update: concrete proof frontier

The prompt has been reread against the entire registry, including its
requirements for arbitrary finite and parallel sources, endpoint-asymmetric
colours, zero weights, complex cancellation, exact normalization, every even
order, and the supremum.  The mechanical registry replay passes with 21
unique route identifiers, 331 local Markdown links, and 114 backticked
artifact paths.  The semantic audit still finds no proof or exact
counterexample of the full conjecture.

What changed is the location of the gap.

1. Pair selection is complete for every allowed order, including
   \(N=8,10,12\): there are at least \(N(N-7)/2\) doubly
   aggregate-injective pairs, a good fan of degree at least \(N-7\), and a
   four-degenerate bad-pair graph.
2. The regular nonbipartite Hessian branch is empty, and the defect-one
   branch is now empty uniformly.  The
   [four-port balance theorem](good-pair-defect-one-four-port-elimination.md)
   closes every formerly residual proper disconnected bipartite component,
   at every shore size and even order, with an independent reconstruction.
   Thus every good pair for every even \(N\ge8\) lies in the extra-kernel
   or defect-at-least-two charts.
3. Inside the connected spanning nonbipartite E1 stratum, the
   [distinguished-span-two theorem](extra-kernel-distinguished-span-two-closure.md)
   converts the dense connected-nonbipartite subcase with distinguished
   off-diagonal Hessian span two by producing a literal zero-star site and
   hence a pure three-cross selector.  Within that graph stratum, its exact
   residuals are a deleted-star row supported on at most two sites or
   distinguished span at least three.  E1 charts whose rank-three graph is
   disconnected, nonspanning, or bipartite also remain live.  If two
   zero-star sites overlap at the same deleted pair, their two 27-packets
   are regradings of one exact 81-row four-cut system.  Three uncontracted
   rows now exclude two dark diagonal colours in either star pair, killing
   the recorded repeated-pair \(K_4\) cap boundary.  The dense residual has
   at least two live diagonal products in each pair; a second packet count
   still supplies no new equations.  A one-sided isotropic contraction now
   exports all nine opposite colour rows as one dressed cap with a shared
   four-star common-power multiplier.  It retains all three target colours
   unless the contracted direct block is a scalar matrix unit, where two
   remain.  The packet, rather than its consistent pure rank-one
   contraction, is the active dense E1 object.
4. For a fan center \(r\),
   [centered defect stability](centered-defect-stability.md) shows that E2
   abundance forces \(b(R-r)\ge2\) or \(\delta(R-r)\le2\); otherwise the
   fan already contains an E1 pair.  On the low-degree branch, a rank-two
   spoke is punched out at both deleted stars whenever the second star has
   rank at least two there.  Exact rank-one survivors show that diagonal
   target equations or overlapping 27-equation systems are still needed.
   For the explicit sharp survivor, the 27 rows compress to four common
   cofactors.  They admit an exact \(N=8\) common-`q` relaxation, but none
   of the 24 minimal three-private-coordinate packets has a shared-star lift,
   even modulo `Ann(q)`.  Thus a lift of that mask must use extra cells,
   non-coordinate or multisite forms, common-annihilator channels,
   cancellation, or higher powers.  Nevertheless, the two independent
   pure-response slices force at least two additional singular blocks at
   the exposed site for every realization of this sharp mask.  At \(N=8\)
   this gives a second rank-three-degree-at-most-two vertex.  The equality
   stratum at higher order and other rank-one masks remain open.
   On every gauge-rigid defect chart the defect coefficient vectors are
   now unique.  Defect exactly two forces a star row supported on at most
   two sites.  Across a good fan, exact defect two then occupies at most
   nine charts when both the center and the rank-three graph off the center
   have minimum degree at least three; otherwise it exposes a rank-three
   degree-at-most-two vertex.  The global sparse-center alternative is one
   synchronized factorized nine-row packet, which has an exact selected-row
   relaxation.  If defect three is fully dense, its six off-diagonal
   vectors span the full defect space.  A sharp common-restriction model
   shows that the full overlap equations, not the shared center star alone,
   must synchronize those coordinates.
5. On the sharp three-essential branch, every cubic nonneighbour forces a
   leave-one-anchor cofactor-nullity profile at least \((1,2,2)\).

The next proof-changing deliverables are therefore concrete: exclude the
full E1 isotropic dressed-cap packet using its common-power provenance;
close the
graph-degenerate, sparse-row, and span-at-least-three E1 residues; extend
the two-singular-spoke export through its equality stratum and other
rank-one masks, propagate defect-two sparsity beyond its
finite-nine/low-degree alternatives, or apply
the full overlap equations to faithful defect-three vectors in E2; and
use the cubic nine-equation two-crossing system on the faithful
\(P_c\ne0\) chart or its pure \(P_c=0\) boundary.  Aggregate rank, a second
reindexed pair chart, and an abstract response table are already known to
be insufficient.  A disproof remains a separate viable route only if it
produces exact finite source data satisfying every colouring coefficient.

The provenance and claim-by-claim comparison with the imported Claude work
is recorded in
[the integration record](claude-comparison-and-integration.md).

## 2. Audit against the prompt's quantifiers

| Required claim | Audited status | Evidence or missing step |
|---|---|---|
| Decorated graph equals an aggregate matching tensor | Proved | Section 2 of [the six-site theorem](../proofs/six-site-arbitrary-complex-obstruction.md) retains endpoint order, parallel sources, arbitrary finite multiplicity, zero blocks, and arbitrary complex weights including zero. |
| Complex cancellation | Explicitly retained | Parallel sources are aggregated only by physical pair and ordered endpoint-color pair.  Every matching fibre and every common-power coefficient is collected before a zero conclusion is drawn; no promoted argument infers summandwise vanishing from a cancelling complex sum. |
| $k_{\max}(2)=\infty$ | Proved construction | Arbitrarily many parallel monochromatic pairs. |
| $k_{\max}(4)=3$ | Proved | The three pairings give partition rank at most three; the diagonal tensor has partition rank equal to its palette size.  The $K_4$ one-factorization attains three; see [the tensor route](tensor-route.md). |
| $k_{\max}(6)=2$ | Proved | [The arbitrary-complex six-site obstruction](../proofs/six-site-arbitrary-complex-obstruction.md) excludes three chosen palette colors after coordinate projection.  The two alternating matchings of $C_6$ attain two. |
| Lower bound two for every even $n\ge6$ | Proved construction | The two alternating perfect matchings of $C_n$, with unit equal-endpoint colors. |
| Upper bound two for every even $n\ge8$ | **Open in this workspace** | The unconditional all-even reduction is missing.  Neither a finite list of collision orders nor a fixed specialization can discharge this quantifier. |
| Exact normalization and palette bookkeeping | Proved in the completed local theorems | The target is the full diagonal tensor with each constant coefficient exactly one.  Projection to any three palette colors preserves those three unit coefficients.  Global use still depends on the missing reduction. |
| Supremum rather than maximum | Not yet discharged globally | A uniform upper bound would rule out every finite source and hence settle the supremum.  Current local results do not do so for $n\ge8$. |
| Reduction validity | Audited locally; global reduction open | Aggregating parallel sources by endpoint-color pair and projecting to chosen target colors are functorial and preserve the coefficients used in the local obstructions.  Removing a palette color merely because its sources have zero weight is forbidden: its constant coefficient is still required to be one.  No existing local reduction supplies the missing all-even descent. |
| Counterexample standard | No workspace countermodel is a disproof | Every recorded countermodel only falsifies a proposed intermediate lemma and is explicitly scoped away from the full ternary monochromatic tensor.  A disproof would still require exact finite data $(A,B,E,k,w)$ and a symbolic or independently checkable certificate for every coloring coefficient. |

Thus the lower bounds and the $n=2,4,6$ cases are in hand; the substantive
unresolved part of the conjecture is exactly the uniform upper bound from
order eight onward.

## 3. Exact state of the main route

### 3.1 Six sites

[The six-site theorem](../proofs/six-site-arbitrary-complex-obstruction.md)
exhausts all nineteen maximum-degree-two defect graphs for arbitrary
$3\times3$ endpoint-ordered complex aggregate matrices, including zero
blocks.  Its persistent artifacts have the following audited SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| low-rank Laurent bundle | `83c4b90ab89d59b0543c40ba5c35aea3659bdcf1ffeb01ab597c9194e9cb70f0` |
| rank-one orbit CNF | `dae187d355193735c93058954cb0723b7ef3798c5935f777ed513e8e1e8df634` |
| rank-one orbit DRUP | `0da0eb641968a56d0b6ba56854fcd0f91640efb5a5c7ba2f38c3ad13ba99abfe` |
| exceptional-triangle CNF | `4961aeaad85296f4be4005e166880186f2ce5f995b595162bf673a7d3eda087c` |
| exceptional-triangle DRUP | `db3dfebc12e25f0be44477f8593e51d7793572cf5e3acd72a93f6b08eb7ca0fa` |

This theorem is a valid endpoint of a reduction; it is not itself a proof
for larger even orders.

### 3.2 Live-three-zero, no-extra-singular branch

Within the frozen $h=8$ collision classifier:

| Common-pole order | Current exact state |
|---|---|
| $k=2$ | Complete after the three-triple, one-triple, all-double, and double-single closures. |
| $k=3$ | Complete; the exact residual census is empty. |
| $k=4$ | Complete; all 46 frozen residual profiles are closed. |
| $k=5$ | Complete; all 44 frozen residual profiles are closed. |
| $k=6$ | Complete; the general-collision theorem closes five selection-free profiles and the independently audited $(3,3,3,1)$ role-lift theorem closes the final $4^3 3^4$ profile. |
| $k=7$ | Complete on the no-extra-singular collision stratum. |
| $k=8$ | Complete on the no-extra-singular collision stratum. |
| $k=9$ | Complete on the no-extra-singular collision stratum. |
| $k=10$ | Complete on the no-extra-singular collision stratum. |
| $k=11$ | Complete on the no-extra-singular collision stratum. |
| $k=12$ | Complete on the no-extra-singular collision stratum. |
| $k\ge13$ | Complete uniformly on the no-extra-singular collision stratum. |

The updated $k=5$ ledger is
[here](live-three-zero-eighth-split-k5-updated-census.md).  This audit first
credited $3^3 2^4 1^6$, $3^4 2 1^9$, and $3^3 2^7$, then an independently
audited unified pair-drop theorem closed seven more:
$3^5 2^2 1^4$, $3^5 2 1^6$, $3^5 1^8$, $3^4 2^3 1^5$,
$3^4 2^2 1^7$, $3^4 1^{11}$, and $3^3 2^6 1^2$.  A
separately audited second-jet argument then closed $3^3 2^3 1^8$.
Uniform selected-lift incidence subsequently closed 25 of the remaining 26
profiles, including $2^9 1^5$; the all-order five-double six-class residue
theorem closed the final $3^2 2^8 1$.  The historical
[parallelogram normal form](live-three-zero-eighth-split-k5-parallelogram-normal-form.md)
remains an exact reduction whose affine certificate was not completed, but
it is no longer needed for fifth-order closure.

The mixed-role theorem is now uniform in \(k\).  Selected incidence closes
every formal \(0\le d\le4\) selection: the final
[four-double/two-singleton theorem](live-three-zero-eighth-split-all-order-four-double-two-singleton-incidence-closure.md)
exhausts the two plane/hyperplane dimensions by exact parity and repeated-row
arguments.  The updated census therefore has no formally applicable open
tail.  Profiles without such a selection remain, including the persistent
near-all-double family.  A strict square-Wronskian version also applies to
qualifying five-class complements for arbitrary \(h\ge8\).  These theorems
still do not exhaust all higher-order profiles.  The independently audited
[higher-split low-role incidence theorem](live-three-zero-higher-split-low-role-selected-lift-incidence-closure.md)
now closes every \(d=0,1,2\) formal selection, with arbitrary complement,
for all \(k\) at \(9\le h\le12\), and for
\((h,k)=(13,\le4),(14,\le3),(15,\le2),(16,1)\).  At the next threshold a
five-dimensional osculating-Schubert model shows that row dimension plus
pair-lift incidence is insufficient by itself.  The uncovered higher-split
collision families therefore remain globally open.  A new exact
[truncated-mass theorem](live-three-zero-higher-split-row-relation-truncated-mass-bound.md)
uses the common complementary polynomial: a five-dimensional kernel needs
at least eighteen units of complementary mass after capping every
multiplicity at three.  On the first boundary \(h+k=18\), the resulting
[census](live-three-zero-higher-split-q5-boundary-census.md) closes almost
every applicable residual and leaves exactly fifty profiles in every row,
all of the form \(3^a2^b1^{h+u}\) with \(3a+2b+u=20\) and the audited
selection conditions.  Exact overlap theorems now close all three
[six-triple families](live-three-zero-higher-split-p18-six-triple-overlap-closure.md),
all four
[five-triple families](live-three-zero-higher-split-p18-five-triple-overlap-closure.md),
and all six four-triple families in
[the four-triple closure](live-three-zero-higher-split-p18-four-triple-overlap-closure.md).
The first
[three-triple overlap theorem](live-three-zero-higher-split-p18-three-triple-overlap-frontier.md)
then closes the \(b=0,1,2,3,4,5\) families by specialization-free
residue-pencil, singleton-anchor, tangent-parity-Wronskian, and
double-exchange arguments.  Its
[endpoint selected-pair closure](live-three-zero-higher-split-p18-b6-endpoint-selected-pair-closure.md)
compresses all fifteen \(b=6\) cubics and forces the six transformed
double values onto one nonzero quadratic.  Thus thirty symbolic equality
families remained at that stage.  The
[two-triple twelve-simple cofactor theorem](live-three-zero-higher-split-p18-two-triple-twelve-simple-cofactor-closure.md)
now closes \(a=2,b=0,1,2\), including the two low-singleton \(b=2\)
boundary rows via neighboring complementary-double corrections.  Its
[mixed-jet companion](live-three-zero-higher-split-p18-two-triple-six-simple-three-double-cofactor-closure.md)
closes \(a=2,b=3,4,5\) with the same bidegree-\((5,9)\) cofactor and two
normalized jets at each fixed double.  Its
[four-/five-double continuation](live-three-zero-higher-split-p18-two-triple-four-five-double-cofactor-closure.md)
then closes \(a=2,b=6,7\): the fixed anchor counts \((2,4)\) and \((0,5)\)
retain the same cofactor bidegree, and the two selected doubles supply the
two interpolation corrections.  Finally, the
[eight-double common-lift theorem](live-three-zero-higher-split-p18-two-triple-eight-double-common-lift-closure.md)
fixes one selected double, lifts two partner three-spaces by coprime
quintic factors into a common degree-nine kernel, and contradicts the
seven-node second-order Wronskian bound.  The
[complete low-triple common-lift theorem](live-three-zero-higher-split-p18-low-triple-singleton-common-lift-closure.md)
then closes all twenty-one residual families.  A fixed complementary
triple upgrades the moving-singleton Wronskian bound to
\(D^2+D\le19\), closing the full one-triple block, including its equality
endpoint by one explicit second-order row.  At the final
\(2^{11}1^{h-2}\) endpoint, pairwise quintic intersections and one common
second-order baseline force seven distinct values into a fibre of a
degree-two rational map.  Thus all fifty \(p=18\) equality families are
closed on every one of the five diagonal pairs.  The common units,
zero/nonopposition cases, endpoint intersections, and fibre count also pass
a [separate reconstruction](live-three-zero-higher-split-p18-low-triple-independent-audit.md).
The next diagonal is now substantially reduced.  The exact
[singleton-parity theorem](live-three-zero-higher-split-p19-singleton-parity-common-lift-closure.md)
moves one selected singleton and uses a five-capped-mass kernel bound plus a
sharp parity/gcd lemma to close 57 of the 94 \(p=19\) families.  The
[dense-double theorem](live-three-zero-higher-split-p19-double-common-lift-closure.md)
adds 14 disjoint families by coprime quintic intersections and the same
degree-two logarithmic-jet fibre mechanism, while the
[moving-triple theorem](live-three-zero-higher-split-p19-triple-common-lift-closure.md)
adds four more by exact even-quartic transport and a third-jet complete-graph
identity.  All three transports, Wronskian/gcd bounds, jet eliminations, and
the combined census passed an independent line audit.  The subsequent
[\(C=6\) parity-pencil coupling](live-three-zero-higher-split-p19-c6-parity-pencil-coupling.md)
closes all pool sizes two through five: small pools fail by coprime cubic
intersection, while the five-pool endpoint and one exact baseline row force
four distinct values into a degree-two rational fibre.  For pool size at
least six, it places every lifted square pencil in the kernel of one global
parity map and proves that map has rank at most three.  This result, its
zero/gcd branches, and its census passed a separate line audit.  Thus 81 of
94 families are closed and exactly 13 remain.  Four form the residual
\(C=6\), pool-size-six-through-eight plane-section block; two further
\(C=6\) profiles have pool size one and lie outside that coupling; four residuals
also lie on the degree-eleven quintic-pair-pencil surface.  The independently
audited
[saturated Klein-plane theorem](live-three-zero-higher-split-p19-c6-saturated-klein-plane-closure.md)
closes the four large-pool profiles.  Exact Wronskian equality excludes a
zero pool and every gcd, gives local sequence \((0,2,3,4)\), and leaves no
other ramification.  The degree-three secant-line curve then has span at
most a plane in the Klein quadric: flag and beta cases make the polynomial
basis dependent, the alpha case forces too many common cubic divisors, and
the genuine-conic case is a quadric ruling with no stationary section.
Thus 85 of 94 families are closed and exactly nine remain: two \(C=6\)
pool-one profiles, four \(C=7\), two \(C=8\), and one \(C=9\).  The
[undecic singleton--double coupling](live-three-zero-higher-split-p19-undecic-singleton-double-coupling-closure.md)
then closes the four profiles shared by the degree-nine singleton and
degree-eleven double boundaries.  Its pool-four branch uses a universal
cubic-pair three-space and an overfull Wronskian; its pool-three branch
uses six Vandermonde-independent quintics; and its pool-two branch forces
intrinsic pair lines whose exact second-row equations form a bidegree-six
nine-vertex clique.  Interpolation contradicts the nonconstant double-pole
coefficient.  The full dimension split and all structural denominators
passed an independent symbolic audit.  Thus 89 of 94 families are closed
and exactly five remain.  The independently reconstructed
[five-triple even-span theorem](live-three-zero-higher-split-p19-five-triple-even-span-closure.md)
then closes both one-quartic survivors.  Pairwise quartic transports from
four distinct triple values span the full five-space
\(\mathbb C[z^2]_{\le4}\); a nonzero triple value supplies
\((z^2-v^2)^3\), which violates its exact third-order baseline row.
The optional double and a relaxed zero-triple placement were checked
separately.  Thus 91 of 94 families are closed and exactly three remain:
\((0,9,3),(0,10,1),(1,8,2)\), all in the no-quartic block.  The
independently audited
[\(C=7\) developable-secant theorem](live-three-zero-higher-split-p19-c7-developable-secant-closure.md)
then closes \((0,9,3)\) and \((1,8,2)\).  Exact Wronskian saturation
turns their parity quotients into degree-at-most-four curves of lines;
five stationary pool sections force developability, and cone,
decomposable tangent-edge, and symplectic tangent-edge branches all fail
sharp bundle-degree counts.  Homogeneous degree drops, quotient gcds,
infinity, and both signed pool fibers passed a separate adversarial audit.
Thus 93 of 94 families are closed.  The sole survivor is
\((0,10,1)\), or \(2^{10}1^{h+1}\), the \(C=8\) degree-five endpoint.
[The singleton pair-line clique theorem](live-three-zero-higher-split-p19-c8-singleton-pair-line-clique-closure.md)
closes that endpoint using a different, one-double selection.  Ten
quintic-transported three-spaces lie in one degree-eleven kernel; the
common singleton row excludes full pair pencils and fixes every intrinsic
pair-line slope.  Each double row then gives one bidegree-\((6,6)\)
identity on a nine-vertex clique, whose excluded double-pole coefficient
has a nonzero linear term.  The formal selection, common units, all
kernel-dimension branches, interpolation thresholds, and the final pole
coefficient passed both the exact checker and a separate line audit.
Consequently all 94 \(p=19\) equality families are closed.
The independently audited
[uniform developable-secant lemma](live-three-zero-higher-split-uniform-developable-secant-lemma.md)
now extracts one parameter-independent consequence of the last diagonal.
In the moving-singleton common-lift setup it excludes every saturated
four-space with
\(M_4=19\), \(4\le C\le7\), and
\(P\ge\max(1,2C-9)\), including all common-factor, infinity, cone,
decomposable-tangent, and symplectic-tangent branches.  Its first genuinely
new application closes, for every \(13\le h\le19\), the four \(p=20\)
one-quintuple families
\(5\,2^7 1^{h+3}\), \(5\,3\,2^6 1^{h+2}\),
\(5\,3^2 2^5 1^{h+1}\), and \(5\,3^3 2^4 1^h\).
The [independent reconstruction](live-three-zero-higher-split-uniform-developable-secant-lemma-independent-audit.md)
also checks the selected-kernel dimension needed by this corollary.  This
does not cover the low-pool, \(C\ge8\), or unsaturated \(M_4=20\) branches.
The independently audited
[first six-kernel boundary](live-three-zero-higher-split-p28-six-kernel-boundary.md)
then locates the next dimension jump exactly: \(p=28\), with the six splits
\((h,k)=(22,6),\ldots,(27,1)\); dimension seven still has excess twelve.
Its exact common-lift census forces a selected dimension drop in 335 of the
344 profiles on the uniform \(d\le2\) slice, leaving nine tuples whose
natural saturated baselines are
\(3^{10}\), \(4^2 3^7 1\), \(4^3 3^6\), and \(4^7 1\).
The [independent reconstruction](live-three-zero-higher-split-p28-six-kernel-boundary-independent-audit.md)
checks every count and explicitly confirms that these are dimension drops,
not profile closures.  Two further independently audited overlap theorems
shrink that frontier.  The
[all-triple tangent-involution theorem](live-three-zero-higher-split-p28-all-triple-tangent-involution-drop.md)
uses eighteen signed tangent identifications against degree seventeen to
cover exactly \((0,10,0,0)\) and \((0,10,1,-2)\).  The
[\(4^3 3^6\) even--odd span theorem](live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop.md)
uses exact pair intersections and a nonzero five-product determinant to
cover \((3,6,0,0)\) and \((3,6,1,-2)\).  Their
[tangent audit](live-three-zero-higher-split-p28-all-triple-tangent-involution-drop-independent-audit.md)
and [span audit](live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop-independent-audit.md)
reconstruct every branch.
The independently audited
[all-triple residual-quartic theorem](live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier.md)
now finishes the selected-kernel classification on the \(3^{10}\) core:
the common kernel has dimension exactly six and every one of the ten
moving-triple selections is exactly \(q=5\).  Exact signed Hermite minors
leave a nonzero decomposable
\(\bigwedge^4\mathbb C^6\)-valued polynomial \(Q(t)\) of degree at most
four after the ten square factors are removed.  The
[independent reconstruction](live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier-independent-audit.md)
caught and corrected the cuspidal-sextic tangent-frame calculation and
rechecked every finite and infinite developable branch.  This is still a
Grassmannian-quartic frontier, not a closure of either \(3^{10}\) profile.
Its independently audited
[balanced-splitting corollary](live-three-zero-higher-split-p28-all-triple-residual-quartic-balanced-splitting.md)
removes every scalar basepoint and proves that the residual curve has exact
degree four with annihilator
\(\mathcal O(-2)\oplus\mathcal O(-2)\).  Equivalently, two quadratic
covector rows generate the annihilator and no nonzero row of degree zero or
one exists.  The
[bundle audit](live-three-zero-higher-split-p28-all-triple-residual-quartic-balanced-splitting-independent-audit.md)
checks the finite gcd, infinity fiber, determinant degree, and polynomial
minimal-basis step.  This is another strict frontier sharpening, not a
profile closure.
The independently audited
[balanced-annihilator closure](live-three-zero-higher-split-p28-all-triple-balanced-annihilator-closure.md)
now closes that frontier.  The derivative identities put \(E,O\) in the
kernel of \((\lambda,\mu,\lambda',\mu')\).  Generic tangent rank two
either kills the four-wedge or makes its scalar a square, contradicting the
ten distinct Hermite factors.  Generic tangent rank one reduces uniquely to
the rational-normal-cubic tangent family; its common-kernel normal form
contains \(A(z)\mathbb C[z^2]_{\le3}\) and therefore has an extra
Wronskian zero at \(z=0\).  The
[independent reconstruction](live-three-zero-higher-split-p28-all-triple-balanced-annihilator-closure-independent-audit.md)
checks every coefficient-span stratum, finite and infinite developable
branch, primitive scalar, and vanishing-sequence step.  Thus both
\(3^{10}\) tuples \((0,10,0,0)\) and \((0,10,1,-2)\) are actual profile
closures on all six equality splits.
The independently audited
[uniform critical moving-triple theorem](live-three-zero-higher-split-uniform-moving-triple-critical-span-bound.md)
now shows, at every first threshold \(p=r(r+3)\), that an exact common
lift with \(c\le r+4\) has at most one maximal selection and one with
\(c=r+5\) has at most three.  Its
[independent reconstruction](live-three-zero-higher-split-uniform-moving-triple-critical-span-bound-independent-audit.md)
checks the essential restored-row hypothesis and the full multiplication
span.  At \(p=28\) this sharpens the \(4^3 3^6\) core from one to at least
three selected kernels of dimension at most five, but still supplies no
profile closure.
The independently audited
[critical local-jet cap](live-three-zero-higher-split-critical-moving-triple-local-jet-q6-cap.md)
then uses an exact row that the span count discards.  Two maximal
transports would fill
\(B_iB_j\mathbb C[z]_{\le r-3}\); after division, the other relation
space would contain \(B_j(z-j)\), whose exact third jet is nonzero at the
complementary triple \(j\).  Its
[independent reconstruction](live-three-zero-higher-split-critical-moving-triple-local-jet-q6-cap-independent-audit.md)
checks the transport orientation and the regular nonzero local unit.
Thus at the critical class count there is in fact at most one maximal
selection.  For the \(4^3 3^6\) core, at least five of the six selections
are exactly \(q=5\).  This is a sharper dimension distribution, not yet a
profile closure.
The independently audited
[\(4^3 3^6\) \(q=5\) saturation theorem](live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation.md)
now completes that dimension distribution.  A cleared Robin family is
cubic in the partner square and has coefficient minor \(16i^2\), excluding
a common five-space; the same family makes a hypothetical sole \(q=6\)
relation four-space have a nonzero Wronskian of degree at most seven with
at least nine roots.  Hence the common kernel is exactly six-dimensional
and all six selections are \(q=5\).  Its signed derivative four-wedge is
nonzero, because both developable branches force an unlisted Wronskian zero
at \(z=0\).  In generic tangent rank two, scalar-gcd root accounting and
the exact second-fundamental bundle degrees leave only a primitive
degree-six residual with \(L\simeq\mathcal O(-4)^2\) and annihilator
splitting \((2,4)\) or \((3,3)\).  The
[independent reconstruction](live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation-independent-audit.md)
checks the full homogeneous and infinity bookkeeping.  This is still a
normal-form theorem, not a closure of either \(4^3 3^6\) profile.  In
particular, the degree-six conclusion is conditional on generic tangent
rank two; the saturation theorem itself does not treat generic tangent
rank one.
The independently audited
[rank-one residual closure](live-three-zero-higher-split-p28-three-quartic-six-triple-rank-one-closure.md)
now supplies that missing case.  The rank-one annihilator line curve is
developable.  Its cone branch contradicts negativity of the annihilator
bundle, while the complete tangent-edge ramification ledger leaves only
four- and five-dimensional edge spans.  The osculating-dual quotient in
the former and the rational-normal-quartic kernel frame in the latter both
produce a nonzero section of \({\cal K}\) vanishing to order at least six
at \(z=0\).  This is an unlisted Wronskian root after saturation.  The
[independent reconstruction](live-three-zero-higher-split-p28-three-quartic-six-triple-rank-one-closure-independent-audit.md)
also checks generic rank zero, infinity ramification, the homogeneous
bundle maps, and the exact quartic kernel module.  Hence the entire
residual problem is now reduced, without a tangent-rank qualification, to
the two generic-rank-two splittings \((2,4)\) and \((3,3)\).
The independently audited
[kernel-orientation countermodel](live-three-zero-higher-split-p28-kernel-orientation-countermodel.md)
shows that an exact moving-sheet triple together with an unramified
opposite sheet and a simple residual determinant zero does not select the
expected kernel point; its kernel can be \([0:1]\).  Thus the shortest
interpolation attack on the \((2,4)\) row is invalid.  On the \((3,3)\)
side, the independently audited
[cubic-pair intersection frontier](live-three-zero-higher-split-p28-three-quartic-cubic-pair-intersection-frontier.md)
constructs a transverse primitive rational model with the correct
six-dimensional coefficient span, echelon degrees, and squarefree residual
sextic, but a generic squarefree degree-twenty-four Wronskian.  Therefore
the two cubic four-spaces and their two-dimensional intersection are also
insufficient.  The remaining finite test must add the exact Wronskian
factorization and every triple/quartic jet-minor divisibility, not merely
the residual determinant.
Finally, the independently audited
[\(4^2 3^7 1\) Robin pair-plane theorem](live-three-zero-higher-split-p28-two-quartic-seven-triple-robin-pair-plane-drop.md)
shows that any four maximal moving-triple selections already force a
seven-dimensional Robin span (or an impossible even six-space at the
zero-singleton boundary).  Its
[independent audit](live-three-zero-higher-split-p28-two-quartic-seven-triple-robin-pair-plane-drop-independent-audit.md)
checks that no fifth through seventh active value is used.  Thus at least
four of the seven selections drop, covering the two \(4^2 3^7 1\) tuples.
The \(d\le2\) dimension-drop ledger is now \(341/344\); the only three
unreduced tuples restore to \(4^7 1\).  The ledger records only dimensions:
the two \(4^2 3^7 1\) tuples receive the separate profile closure below,
while the other 339 dimension drops are not thereby profile closures.  The
unrestricted-role \(p=28\) census remains much larger.
The independently audited
[singleton-swap cap](live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap.md)
then compares different complementary singleton choices.  For each fixed
triple, two \(q=6\) choices would fill a degree-nine four-space by two
coprime cubic transports and contradict the remaining fixed simple row.
Its
[independent audit](live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap-independent-audit.md)
re-derives the \(q=4\) exclusion at these higher splits and checks the
zero-singleton case.  Hence each triple has at most one \(q=6\) choice,
and at least \(h-6\) or \(h-8\) singleton columns are entirely \(q=5\).
The independently audited
[two-quartic \(q=5\) grid theorem](live-three-zero-higher-split-p28-two-quartic-q5-grid-closure.md)
now performs that coupling.  Pairwise singleton transports give one common
cubic plane for every fixed triple.  One all-\(q=5\) column then produces
seven double-square planes inside an exact degree-seven four-space; a
characteristic-zero parity classification forces the four-space to be
\((\alpha+\beta z)\mathbb C[z^2]_{\le3}\), contradicting a surviving exact
order-three row.  Its
[independent audit](live-three-zero-higher-split-p28-two-quartic-q5-grid-closure-independent-audit.md)
reconstructs the local unit, all projection-rank cases, and the terminal
derivative.  Thus the two \(4^2 3^7 1\) tuple families are actual profile
closures on all six equality splits.  This conclusion does not transfer to
the other 339 dimension drops or to unrestricted-role selections.
For the three remaining \(4^7 1\) tuples, the independently audited
[pure-fifth-pole frontier](live-three-zero-higher-split-p28-all-quartic-pure-fifth-pole-frontier.md)
proves that the full cubic relation image is equivalent to one degree-thirty
section lying in a seven-dimensional pure fifth-pole system.  Its
[independent audit](live-three-zero-higher-split-p28-all-quartic-pure-fifth-pole-frontier-independent-audit.md)
checks the local row reconstruction and twelve exact separated \(q=6\)
formal models, including every split in the no-double tuple.  They are not
tensor realizations, but they rule out any closure based only on the single
selected system's highest jets and common-pole consequence.  The next
input for \(4^7 1\) must therefore come from a second selection or from an
unreduced global equation.
Thus the uniform \(d\le2\) six-kernel slice is sharply localized, but the
arbitrary-role boundary remains open.  On the separate
\(h=8\) tail,
[the bounded swap frontier](live-three-zero-eighth-split-stable-double-five-set-swap-frontier.md)
puts every five-double relation pencil in degree seven, with five genuine
triple ramification points and only two residual ramification units; it
also proves that adjacent derivative pencils meet in dimension at most
one.  A different multi-pencil coupling now closes the first stable
all-double case: the
[common-octic lift](live-three-zero-eighth-split-sixth-order-twelve-double-common-lift-closure.md)
embeds all eight fifth choices over a fixed four-core in one
four-dimensional exactness kernel and excludes every parity-projection
rank.  The subsequent
[common-nonic theorem](live-three-zero-eighth-split-stable-double-nonic-common-lift-closures.md)
closes both $2^{13}$ and $2^{12}1$ by a global tangent-hyperplane
classification.  The
[decic four-space theorem](live-three-zero-eighth-split-stable-double-decic-four-space-closure.md)
then closes $2^{13}1$ and every dimension-at-most-four branch of
$2^{14}$, without any disjointness assumption on the lifted planes.  The
first surviving common-kernel boundary is therefore exactly the
five-dimensional saturated branch of $2^{14}$; its Wronskian and the
possible lines $\mathbb C A_aA_b$ attain equality simultaneously.  The
[five-space saturation closure](live-three-zero-eighth-split-fourteen-double-five-space-saturation-frontier.md)
first makes that equality exact: every local vanishing sequence is
$(0,1,3,4,5)$, the pair-intersection graph has maximum degree two, and an
exact empty-graph Grassmann model shows why incidence alone cannot finish
the proof.  The common polynomial coupling then factors the paired
five-jet determinant through the exact nonzero identity
$J=\kappa C(x)^2C(-x)$.  Parity ranks two and three violate corrected
Wronskian caps.  In rank four a degree-six scalar vanishes at nine pool
squares and forces $C$ even.  In rank five, a moving Taylor-basis cross
product obeys $P_0'=(L\times N)_0+3P_1$; its degree-four quotient vanishes
at all ten squares and again forces $C$ even.  Structural noncollision
excludes both alternatives, so $2^{14}$ is closed.  The empty
\(k=2,3,4,5\) ledgers must not be quoted as an all-even result.

The
[next stable undecic frontier](live-three-zero-eighth-split-next-stable-undecic-common-kernel-frontier.md)
now scopes \(2^{14}1\) and \(2^{15}\) exactly.  Both common kernels have
dimension at most five; dimensions two, three, and four close.  The last
four-space rank first obeys
\(\operatorname {rank}(E',O,O')\le2\) identically.  Its tangent
coefficient \(\beta=N/D\) has \(\deg D\le2\), \(\deg N\le3\) by the
eight-unit ramification divisor of a four-space of quintics.  The last
paired row would put at least seven pure-profile nodes, or six singleton
nodes in its only equality case, on the nonzero fibre
\(N(a^2)+aD(a^2)=0\); the respective degree bounds are six and two.
Thus dimension four is impossible.  In dimension five,
an invariant derivative of
\(*\!(E\wedge E'\wedge O\wedge O')\) closes every nonzero-cofactor
branch, including the globally zero paired determinant.  Before the final
uniform bound, only the five-space four-row tangent branch remained, with odd ranks
\(\{4,5\}\) for both profiles: in an odd-adapted basis, every mixed
four-by-four cofactor is the product of an odd Wronskian and a pure-even
Wronskian, so cofactor zero makes a pure-even kernel of dimension at least
two impossible.
The degree-eleven growth
\(A_aA_b\mathbb C[z]_{\leq1}\) explains why the decic product-line
argument no longer closes dimension four by itself.

The
[uniform fixed-numerator theorem](live-three-zero-eighth-split-stable-double-fixed-numerator-four-space-bound.md)
first closes both stable families \(2^m\) and \(2^m1\) for every
\(m\geq12\).  Normalizing
the rational primitive identifies the growing kernel with a subspace of
\(\mathbb C[z]_{\leq9}\).  Each of the four fixed double values gives two
independent jet equations, so a \(d\)-space would satisfy
\(8(d-1)\le d(10-d)\), forcing \(d\le4\).  The undecic analysis already
excludes dimensions two through four, while every lift plane forces
dimension at least two, closing \(2^{14}1\) and \(2^{15}\).
For the higher tail \(p\geq11\), the moving double-zero planes close
dimensions two and three.  Equality at dimension four uniquely gives
\({\cal W}=\langle\prod_{j\ne i}(z+r_j)^3:i=1,\ldots,4\rangle\).
The anchor equation is incompatible with swapping the fourth core value:
it would put all \(m-3\) eligible double values in one fibre of
\((x+5r)/(x^2-r^2)\), whose fibres have size at most two.  The lower
\(p=8,9,10\) cases are the already closed octic through first-undecic
profiles.

The
[general-collision extension](live-three-zero-eighth-split-general-collision-fixed-numerator-closure.md)
retains arbitrary fixed excess at every selected repeated class.  For a
fixed four-class formal-double core the common primitive denominator still
has degree \(k+10\), so subtraction of the value at \(-\mu\) again gives
a degree-nine numerator.  Three moving fifth choices exclude dimensions
two and three; equality in dimension four gives the same explicit basis,
and core swaps cancel all original multiplicities before producing the
quadratic-fibre contradiction.  Its exact count criterion is
\[
 \rho\ge7,\qquad n_1\ge2\ \hbox{or}\ n_2\ge6\ \hbox{or}\ n_3\ge5.
\]
After all-order mixed-role incidence, this closes every selection-free
baseline profile at \(k\ge7\).  A uniform size bound reduces every possible
exception to \(k\le44\), and exact enumeration shows that exceptions occur
only through \(k=6\).  At sixth order the sole remaining baseline profile
is \(4^3 3^4\).  The
[quadruple/triple role-lift theorem](live-three-zero-eighth-split-k6-quadruple-triple-role-closure.md)
now closes it.  Selecting three exact triples at role three and one
quadruple at role one puts all six legal pair drops in degree five.  A
sharp reflected-parity argument excludes kernel dimension three; dimension
four supplies two row relations whose differentiated numerators have the
exact degree-ten contact divisor and cannot both map injectively to
constants.  Its legality, regular-unit rows, Wronskian/gcd corrections,
projective-even reduction, and principal-part normalization passed an
independent line-by-line audit.  Consequently the complete selection-free
no-extra-singular \(h=8\) collision ledger is closed; this remains a local
classifier result, not the missing all-even descent.

### 3.3 Additional-singular-site escape

The axis-capacity, shared-star, and exact-family reductions are uniform and
healthy.  For a sole extra plane, all currently covered ranges are exact.
The entire first high-split sole-plane layer \(t=r+3\) is closed by a
uniform forced source-\(22\) argument.  The next point \((r,t)=(4,8)\) is
also closed structurally: triple classes fail a deletion system, the
all-distinct profile fails a projective quartic compatibility, and every
remaining profile fails a double-confluent quadratic residue fibre.  Its
literal response audit includes singleton zero-beta values, arbitrary direct
scale, and every row plane.  The same argument closes the whole boundary
layer $t=r+4$: triple-containing and at-least-seven-class profiles reduce to
the deletion quartic; the four six-class profiles reduce to an order-two
residue quartic; and the final $2^4 1$, $2^5$ profiles fail a quadratic
fixed-$b$ fibre.

The first point of the next layer, \((r,t)=(5,10)\), is also closed.  Its
twenty-three profiles reduce to fixed-special deletion for multiplicity at
least three, affine or quadratic Robin factors for zero through four double
classes, and a bad-pair matching lemma for the five-double profile.  The
all-distinct Robin nonidentity is an exact localized universal sextic
certificate.  The literal response retains zero beta, direct scale, and all
row planes.  A one-deletion Hermite lemma promotes this to the entire layer
\(t=r+5\): a four-anchor affine Robin resultant closes every collision with
at least five value classes, a direct exchange closes the four-class
boundary, and the same universal sextic closes the all-distinct branch.
The remaining sole-plane gap is therefore

\[
                    r\ge7,\qquad r+6\le t\le2r,
\]

with every surviving exceptional beta class of multiplicity at most
$r-1$.

The first layer of that gap, \(t=r+6\), is now reduced uniformly to a
finite dense-double tail.  Five-special deletion closes every class of
multiplicity at least three, and localized degree-eight determinants close
one double and all profiles with at least eleven value classes.  The
all-distinct cubic identity is closed by full DR4: under \(t_i=-a_i\) its
four cleared rows are exactly the DR4 rows, so all four core translations
vanish; overlapping four-cores then put at least nine values in one fibre
of a nonconstant quadratic rational map.  At the first point \((7,13)\),
the initial exact census was \(101=97+4\).  The three-double closure below
improves this to \(101=98+3\), with only
\(2^4 1^5,2^5 1^3,2^6 1\) remaining.  The layer's dense-double tail is
empty for \(r\ge15\).

For the first residual \(2^3 1^7\), the
[exact three-double frontier](live-three-zero-sole-plane-fourth-high-three-double-frontier.md)
now couples the three degree-eight pair determinants and both multiplier
identities, including all four selected-partner exchange equations.  Two
exact Singular lifts over \(\mathbb Q\) yield six necessary parameter
polynomials of degrees \(30,30,30,48,48,48\), with denominator lcm one
after only structural divisors are removed.  Their homogeneous leading
forms have gcd \(v^6w^6\), so the projective boundary is reduced exactly to
\([1:0]\) and \([0:1]\).  The
[independent audit](live-three-zero-sole-plane-fourth-high-three-double-frontier-independent-audit.md)
reconstructed the rows, lifts, cyclic normalizations, and boundary gcd.
This is a frontier only: the affine common-zero set and both boundary
directions remain open, and the finite-field unit calculation receives no
closure credit.

The subsequent independently audited
[three-double closure](live-three-zero-sole-plane-fourth-high-three-double-closure.md)
resolves that entire common-zero set over characteristic zero.  In degree
78, a good-prime Macaulay rank gives
\(\operatorname{HF}_J(78)\le318\).  Exact rational overideals \(A,B\)
have Hilbert values \(192,126\), both contain
\(t^{46}(L^h)^4\), and \(A+(t^{16})\) has zero degree-78 quotient.  The
intersection exact sequence therefore forces
\(J_{78}=(A\cap B)_{78}\), so \(L^4\in(h_1,h_2,h_3)\), contradicting
structural admissibility.  The
[independent audit](live-three-zero-sole-plane-fourth-high-three-double-closure-independent-audit.md)
uses prime 31991 and reversed orders and reproduces rank 2842 and all four
Hilbert values.  It also confirms that 126 is only the exact \(B\)-term;
no primary-component claim is needed.

For the first three-extra configuration

\[
 (M_{e_2},M_{e_0},M_{e_1})=(\{2\},\{0\},\{1\}),
 \qquad(r,t)=(1,0),
\]

the central cell and all 26 noncentral cells are now closed: 27 of 27 total.
The final $CCB/CBC/BCC$ orbit has an uninterrupted exact replay over
$\mathbb Q$ for each placement, using only direct-free maximal minors and
localized unit ideals.  Thus the complete minimal three-extra response is
uniformly injective for arbitrary direct $B_{01}$ scale.

The first two-extra configuration

\[
 (M_{e_2},M_{e_0})=(\{2\},\{0\}),\qquad(r,t)=(2,0),
\]

is also complete.  Its retained response keeps all seven nonzero sites and
has exactly 20 columns.  Exact direct-free unit-minor certificates close the
central cell and all eight ordered boundary cells, without exchanging the
inequivalent extra sites.  Larger two-extra cases, the sole-plane gap above,
larger three-extra cases, and the nonrescue families remain open.

### 3.4 Global descent diagnostics

The independently audited
[projective-height obstruction](cap-condition-projective-height-obstruction.md)
first closes a tempting dimension-only shortcut.  The denominator-cleared
clean-cap condition is the cubic
\(D=6s^2(C_6+C_4x)-3sC_2^2x-C_2^3\), but \(V(D)\) always contains
the large forbidden linear space \(\ker(s,C_2)\).  An exact abstract
signature satisfying every linear top GHZ contraction identity has
\(I_D=(s^2\kappa_0,s^2\kappa_1,s^2\kappa_2)\) and
\(I_D:(s\kappa_0\kappa_1\kappa_2)^\infty=(1)\).  The
[clean-room audit](cap-condition-projective-height-obstruction-independent-audit.md)
reconstructs the cube identity, the \(135/729\) coordinate counts, the
\(6424/5831\) projective bounds at eight capped sites, and the explicit
Rabinowitsch unit certificate.  It also tests a square-free \(x^3\) that
overlaps all three target directions.  The signature is deliberately
abstract, not a realizable common-edge source.  Thus projective height and
the top GHZ identity alone receive no descent credit; the exact remaining
gate is proper saturation forced by nonlinear common-edge relations.

The next independently audited result shows exactly how much more is
needed.  [The actual-cofactor cap cubic](actual-cofactor-cap-cubic-and-four-parameter-prism-barrier.md)
proves the intrinsic identity
\({\cal D}_{\rm src}=6(s^2F_U^K-H_6(A^K))\).  Its
[clean-room audit](actual-cofactor-cap-cubic-and-four-parameter-prism-barrier-independent-audit.md)
then reconstructs a genuine ten-site common-edge family with a
four-dimensional cap slice on which the top contraction is exactly
\(\sum_i\kappa_iX_i\) and
\(s,\kappa_0,\kappa_1,\kappa_2\) are independent.  Nevertheless the
cofactor family is the root-covered prism with mixed ideal
\((z_0z_1z_2)\) and unit active saturation.  Eight of the source's nine
top words are globally mixed, so this is not a Krenn counterexample and
does not satisfy the full large-source GHZ equation.  It proves that even
common-edge realizability plus exact contraction on one active cap subspace
is insufficient.  Priority must now go to the omitted transverse/all-cap
equations, equivalently extension to the full GHZ flattening.

The independently audited
[maximal transverse prism cap-slice countermodel](maximal-transverse-prism-cap-slice-countermodel.md)
closes the remaining dimension-count version of that proposal.  Its full
cap map has rank nine.  The unique maximal diagonal-image slice has
dimension \(75\), and the unique maximal slice satisfying the literal GHZ
cap formula has dimension \(73\); nevertheless the actual lower cofactor
image on both is exactly the same four-parameter prism with unit active
saturation.  On the GHZ-compatible slice the effective top-plus-cofactor
rank is only four and the common kernel has dimension \(69\).  Its
[clean-room audit](maximal-transverse-prism-cap-slice-countermodel-independent-audit.md)
also reconstructs the induced cap-adjugate identity: all six omitted
off-diagonal rows occur with nonzero coefficients, while the other two
missing rows relocate the colour-one and colour-two diagonals across the
extra capped sites.  This is not a global source and does not defeat a
theorem using many effective lower transverse directions.  It proves that
ambient cap dimension and the number of formally imposed cap equations are
irrelevant.  The finite sharp extension test is to cancel those eight rows
while simultaneously changing the shared lower cofactor determinant.

The independently audited
[eight-site polarized countermodel](polarized-eight-site-unrestricted-counterexample.md)
now sharply separates the unrestricted matching-power equation from the
actual shared pair-cap equations.  It gives integral quadratics \(q,z\) with

\[
                         zq^3/3!=\Delta_{8,3},
\]

using exactly three decorated terms.  Nevertheless a constant
rank-three cross minor of \(z-aq\) proves that no linear \(p,s\) and no
scalar \(a\) can satisfy \(z=aq+4ps\).  The
[clean-room reconstruction](polarized-eight-site-unrestricted-counterexample-independent-audit.md)
checks all 105 matchings, all 420 distinguished-edge positions, the
factorial normalization, and the symbolic rank-at-most-two pair-cap bound;
it also finds two mixed words in \(q^4/4!\).  Thus the model is neither a
Krenn counterexample nor a shared pair-cap model.  It rules out any proposed
uniform theorem based only on \(zq^{m-1}\); a viable cap continuation must
retain the literal low-rank form \(z=aq+mps\), compatibility of several
colour-pair rows, or overlap among distinct physical pairs.

The independently audited
[fixed-\(q\) pair-cap obstruction](polarized-eight-site-fixed-q-pair-cap-obstruction.md)
then allows every other quadratic \(z\) with the same nine-cell \(q\).
The nineteen terms of \(q^{[3]}\) give 171 pair--term incidences on 165
top words.  Three pure singleton coordinates and four mixed singleton
zeros force a seven-entry Gram system for the mode vectors
\((p_X,s_X)\in\mathbb C^2\); its exact characteristic-zero ideal is
\([1]\).  The
[independent reconstruction](polarized-eight-site-fixed-q-pair-cap-obstruction-independent-audit.md)
rebuilds the powers by repeated square-zero multiplication and confirms the
unit ideal in a different algebra system.  Thus adding an arbitrary kernel
element to the displayed \(z\) cannot repair this \(q\) into pair-cap form.
The statement remains fixed-\(q\); an arbitrary \(q\), several shared rows,
and physical-pair overlap remain open.

A different exact model shows that retaining one literal pair-cap factor is
still insufficient.  The independently audited
[shared pair-cap countermodel](polarized-eight-site-shared-pair-cap-countermodel.md)
has a twelve-cell \(q\), genuine global linear forms \(p,s\), and

\[
                 z=\tfrac14q+4ps,\qquad
                 zq^{[3]}=\Delta_{8,3}.
\]

Its [clean-room reconstruction](polarized-eight-site-shared-pair-cap-countermodel-independent-audit.md)
checks all 6,561 coefficients, all divided-power factors, and the two-cell
Gram cancellation.  For that same \(q\), however, 358 singleton rows expose
all 240 inactive response cells, forcing every surviving block onto one
rank-one line and contradicting the rank-two difference of two diagonal
targets.  That full-nine statement is the registered border pair-suspension
obstruction after exact site/color relabeling and normalization; only the
isolated aggregate pair-cap model is new.  The audit also catches and corrects
the overlap normalization: the second physical-pair equation has target
factor four in polarized form and factor one in raw matching form.

The subsequent [pair-slice exchange theorem](ten-site-overlapping-pair-exchange-redundancy.md),
independently replayed in a
[clean-room audit](ten-site-overlapping-pair-exchange-redundancy-independent-audit.md),
corrects the proposed next-filter interpretation.  A complete nine-row
tensor system for one deleted pair already lists every coefficient of the
ten-site GHZ residual.  The complete system for an overlapping or disjoint
pair is exactly the same list of 59,049 residual polynomials under
reindexing.  The second chart can expose useful elimination or localization
consequences, but it contributes no new ideal generators.  The useful next
layer is therefore a source-variable invariant derived
from that exchange presentation—not a second imposition of the same nine
tensor equations.

A new incidence invariant is now independently proved.  [The uniform full-nine
target-incidence theorem](uniform-full-nine-target-incidence-invariant.md),
with its [clean-room audit](uniform-full-nine-target-incidence-invariant-independent-audit.md),
uses the common cofactor matrix and cancellation-safe local ideals to show,
on every boundary of size \(2m\),

\[
 |D_i|\ge 2m-2,\qquad D_0\cup D_1\cup D_2=U,
 \qquad n_3\ge n_1+2m-6.
\]

Consequently every pair deletion from an \(N\)-site hypothetical source has
at least \(N-8\) internal sites whose aggregate incident span contains the
whole target frame.  This is genuine uniform progress: it uses all nine
rows, permits arbitrary endpoint-asymmetric blocks, zero blocks, and complex
cancellation, and grows with the source order.  It does not say that each
individual block row is nonzero.

The independently audited
[target-flattening essential-star theorem](target-flattening-essential-star-pair-bound.md)
then sharpens pair selection without any full-nine counting.  Mode
flattening forces the incident mode-support spaces at every endpoint to span
the target mode.  At most three neighbours are deletion-essential there, so
the number of unordered pairs whose two aggregate stars are injective is at
least
\[
  \binom N2-3N=\frac{N(N-7)}2
\]
for every even \(N\ge8\), and some vertex has at least \(N-7\) good
neighbours.  The [clean-room audit](target-flattening-essential-star-pair-bound-independent-audit.md)
also verifies the equality classification and the stronger graph
consequence: the bad-pair graph is four-degenerate, hence five-colourable,
so the good-pair graph has a clique of size at least \(\lceil N/5\rceil\)
(in particular, six mutually good sites for \(N\ge26\)).  If an endpoint
has three essential neighbours, the cubic-vertex equations force their
three nonzero supports onto the three same-colour coordinate cells.  These
claims remain aggregate and relative to a fixed ternary target projection;
they do not imply individual-block rank or simultaneous goodness for every
palette triple.

The independently audited
[injective-star Hessian bridge frontier](injective-star-hessian-bridge-frontier.md)
now identifies exactly what pair goodness does and does not buy.  Under
gauge-rigid connected third-colour support it produces a localized missing
row, while a connected non-bipartite support graph makes all six global
missing rows nonzero and sparse.  Exact binary target systems and an exact
fourteen-site structural family show that aggregate injectivity alone does
not force those graph hypotheses or a clean cap.  Thus pair selection was
already uniform even at \(N=8,10,12\).  At this intermediate stage the
gate was to use the mixed GHZ equations across a good fan or clique; the
later regular-branch and defect-one eliminations below resolve that gate
to the E1/E2 dichotomy.

That fan continuation is now independently audited.  [The good-pair fan
six-port reduction](good-pair-fan-six-port-triple-cofactor-reduction.md),
with its [clean-room audit](good-pair-fan-six-port-triple-cofactor-reduction-independent-audit.md),
proves that for \(N\ge16\) either at least \(N-15\) good fan pairs are in
the extra-kernel/disconnected/bipartite escape charts, or three literal
zero-block neighbours force an exact 27-row triple-cofactor system whose
centre rows live on at most six physical ports.  At \(N\ge24\), the three
neighbours can be made pairwise good unless at least \(N-23\) fan pairs
escape.  The resulting six-port response table is not itself
contradictory: an exact three-port abstract model passes all 27 rows.  At
that intermediate stage, a continuation had to retain the simultaneous
common quadratic and common physical cofactor factorizations across all
three neighbour pairs; the regular branch is subsequently eliminated.

The regular branch also has an independently audited growing-shore form.
[The induced-zero-shore hierarchy](good-pair-fan-induced-zero-four-cut-reduction.md),
with its [clean-room audit](good-pair-fan-induced-zero-four-cut-reduction-independent-audit.md),
proves that for every \(k\ge1\) and even \(N\ge7k+7\), either at least
\(N-7k-6\) fan pairs lie in the Hessian escape charts or there is an
aggregate-zero shore of \(h=k+1\) sparse injective vertices satisfying the
exact \(h\)-fold common-power identity.  At \(k=3\), either at least
\(N-27\) pairs escape or \(N\ge28\) has a literal zero \(K_4\).  A
cancellation-safe hole cap reduces that four-cut system to 81 equations on
at most 24 physical ports.  The cap retains provenance as a projection of
one common matching power but need not itself be a matching power, so an
abstract finite response classification alone still cannot close it.

That warning is exact rather than heuristic.  [The twelve-port capped-table
countermodel](zero-shore-four-cut-capped-table-countermodel.md), with its
[clean-room audit](zero-shore-four-cut-capped-table-countermodel-independent-audit.md),
uses twelve one-site coordinate rows in four injective frames and satisfies
all 81 capped equations with three unit diagonal responses and 78 literal
zeros.  It is not lifted from a common quadratic and hence is not a source.
An exact \(10{,}395\)-matching audit rules out only the narrow lift supported
on one fixed perfect matching.  General matching powers, cancellation, and
entangled caps were the exact unresolved interface of that intermediate
regular branch; the simultaneous exclusion below later retires the branch.

The escape side has also been sharply falsified at the right level.  [The
complete-bipartite all-pair countermodel](complete-bipartite-all-pair-hessian-escape-countermodel.md),
with its [independent audit](complete-bipartite-all-pair-hessian-escape-countermodel-independent-audit.md),
gives one actual common quadratic at every \(N=2s\ge6\) for which every
pair is doubly aggregate-injective, every pair-deleted rank-three graph is
connected bipartite, the graph has vertex connectivity \(s\), all pair
cofactor factorizations are literal, and the three pure target coefficients
are exactly one.  Its mixed coefficient \(2^{s-1}\) is nonzero, so it is
not a target source.  It proves that linearly many escape charts cannot be
converted by graph density, pure normalization, or pair exchange alone;
mixed GHZ vanishing must enter before the counting step.

That next step is now closed, and more strongly than required.  [The fan
six-port simultaneous exclusion](good-pair-fan-six-port-simultaneous-exclusion.md),
with its [clean-room audit](good-pair-fan-six-port-simultaneous-exclusion-independent-audit.md),
proves that the regular nonbipartite branch generating those tables is
empty: on any regular nonbipartite pair chart the nine pair-contraction
equations force every \(p_c\) one-site (annihilator dimensions \(0/1/3\)
for support \(\ge3/2/1\)), collapse the six mixed rows to one site
factor, and contradict the diagonal cofactor identities.  No good pair is
regular nonbipartite; the fan dichotomy is threshold-free for every even
\(N\ge8\); bridge-frontier stratum 4 is empty.  Priority 2's first clause
in Section 6 is therefore discharged.  The later escape-chart descent and
four-port balance theorem sharpen this further: the uniform descent must
now be extracted from only the extra-kernel (E1) and defect-at-least-two
(E2) charts.

[The distinguished-span-two E1 theorem](extra-kernel-distinguished-span-two-closure.md),
with an [independent audit](extra-kernel-distinguished-span-two-closure-independent-audit.md),
now converts the dense connected-nonbipartite E1 subcase with
\(\dim D_{pq}=2\) into a literal zero-star site and a pure three-cross
selector, without assuming that the full Hessian quotient has dimension
two.  Within this graph stratum, the remaining cases are exactly a
deleted-star row supported on at most two sites or \(\dim D_{pq}\ge3\).
E1 charts with a disconnected, nonspanning, or bipartite rank-three graph
remain separate residuals.  In the resolved span-two structural case,
the next export must keep the common-complement 27 equations across
overlapping zero-star triples rather than retaining only the abstract
selector row.

[The overlapping zero-star exchange theorem](overlapping-zero-star-four-cut-exchange.md),
independently reconstructed in
[its audit](overlapping-zero-star-four-cut-exchange-independent-audit.md),
identifies that export exactly.  Two zero-star sites for the same deleted
pair give one 81-row four-cut identity; resolving either remaining site in
its 27-packet produces the same rows, so the packets cannot be counted as
independent.  A repeated-pair \(K_4\) common-power model satisfies all five
selector-contracted row/column caps but not the full 81 rows.
[The uncontracted two-dark-colour theorem](uncontracted-four-cut-two-dark-colour-obstruction.md),
with an
[independent audit](uncontracted-four-cut-two-dark-colour-obstruction-independent-audit.md),
resolves that extension gate: three exact rows show that each of the two
star pairs has at most one vanishing diagonal colour product.  This kills
the \(K_4\) boundary, while leaving the generic two-/three-live-colour
four-cut system and the other E1 strata open.

[The isotropic dressed-cap theorem](uncontracted-four-cut-isotropic-dressed-cap.md),
with an
[independent audit](uncontracted-four-cut-isotropic-dressed-cap-independent-audit.md),
compresses that generic system without discarding its direct block.  One
isotropic contraction gives nine equations with the common multiplier
\(t(\alpha)v(\beta)z^{[m-4]}\) and dressed quadratics
\(x_ay_b+a_{ab}z/(m-3)\).  The target remains ternary unless the contracted
direct block is a scalar matrix unit, in which case it remains binary.
Exact binary and unstructured-multiplier guards show that the optional
second rank-one contraction is insufficient; the synchronized nine-row
packet and actual divided power are essential.  No registered theorem yet
excludes that packet.

[Centered defect stability](centered-defect-stability.md), with an
[independent audit](centered-defect-stability-independent-audit.md), gives
the parallel E2 reduction.  For a fan center \(r\), E2 abundance forces
\(b(R-r)\ge2\) or \(\delta(R-r)\le2\); if both fail, the fan already
contains E1.  The remaining tensor exports are exact: synchronize defect
coefficient vectors across the overlapping deletion charts in the first
alternative, or derive a centered low-degree mixed-equation contradiction
in the second, allowing that the selected site can still meet \(r\).

[The faithful defect-coefficient theorem](defect-coefficient-rank-and-two-defect-sparsity.md),
with an
[independent audit](defect-coefficient-rank-and-two-defect-sparsity-independent-audit.md),
now fixes the first export's coordinates.  Gauge rigidity makes the defect
expansion unique; a defect-two good chart has a star row supported on at
most two sites, while a fully dense defect-three chart uses the entire
three-dimensional defect space.  An exact odd-complement relaxation permits
unrelated vectors across two shared restrictions, but one pairwise-distinct
row of the full overlap system detects it with residual \(-6\).  Thus shared
center/quadratic data alone cannot perform the synchronization.

[The defect-two fan propagation theorem](defect-two-fan-sparsity-propagation.md)
globalizes the sparse-row conclusion without assuming coefficient
synchronization.  For a center \(r\), either \(\deg_R(r)\le2\), or all but
at most nine exact-defect-two fan endpoints have degree at most two in
\(R-r\).  In particular, if both relevant degree bounds are at least three,
at most nine fan charts have defect two and at least \(N-16\) have defect at
least three.  A globally two-site-supported center row persists across all
outside endpoint pairs as one factorized nine-row overlap packet.  An exact
selected-row realization shows that this packet still needs the other
eighteen triple rows, pair diagonals, or Hessian data.

[The centered low-degree rank tradeoff](centered-low-degree-rank-tradeoff.md),
with an
[independent audit](centered-low-degree-rank-tradeoff-independent-audit.md),
now sharpens the second alternative.  With \(A_{rx}\) invertible, every
rank-at-most-two spoke gives a two-row zero cover; if the spoke has rank two
and \(A_{ux}\) has rank at least two, all six endpoint rows vanish.  Exact
rank-two/rank-one and rank-one/invertible witnesses show both thresholds
are sharp.  Hence the remaining low-degree obstruction is specifically the
rank-one spoke mask, and it requires diagonal cells or overlapping full
27-equation compatibility.

[The centered rank-one overlap packet](centered-rank-one-overlap-packet.md),
with an
[independent audit](centered-rank-one-overlap-packet-independent-audit.md),
uses that compatibility on the explicit sharp mask.  Its 27 equations
contract to four shared cofactors on a two-plane.  A five-site common-`q`
relaxation satisfies the contracted table, so multiplication alone does not
close the branch.  After restoring the four shared star preimages, however,
none of the 24 minimal three-private-coordinate incidence designs lifts,
even modulo `Ann(q)`.  Any realization of this mask must therefore use
extra cells, non-coordinate or multisite forms, common-annihilator mixed
cofactors, or cancellation among multiple origins.  This does not eliminate
other rank-one local masks or higher-order versions of the packet.

[The two-star pure-response theorem](centered-rank-one-two-star-pure-response-obstruction.md)
extracts a support-free consequence from the same `hh` cofactor.  For
linear forms \(a,b\), a pure response \(aG=X\ne0\) together with \(bG=0\)
forces a site where their local rows are dependent; if that site is unique,
the target factor lies on the dependent line.  Applying this statement to
both independent colour slices forces at least two singular blocks incident
with `y`, with arbitrary cells and cancellation.  At \(N=8\), the three
named rank-one blocks then imply \(\deg_R(y)\le2\).  Above eight sites the
export is \(\deg_R(y)\le N-6\), so its equality cases still require graph
propagation.

The sharp three-essential equality stratum now has a separate uniform
constraint.  [The cubic leave-one-anchor nullity-web theorem](cubic-vertex-leave-one-anchor-nullity-web.md),
independently checked in a [clean-room audit](cubic-vertex-leave-one-anchor-nullity-web-independent-audit.md),
shows that for every nonneighbour of the cubic vertex all three
leave-one-anchor cofactor maps are singular and at least two have nullity
at least two.  The minimum profile \((1,2,2)\) follows from exact
wrong-colour equations and one shared double-deletion cofactor.  This is a
genuine common-cofactor corank web, but it is conditional on the cubic
equality stratum and does not yet lift a kernel direction to a cap or a
smaller source.

The independently audited
[cubic common-cofactor-zero boundary](cubic-nullity-common-cofactor-zero-boundary.md),
with its [clean-room audit](cubic-nullity-common-cofactor-zero-boundary-independent-audit.md),
then classifies the first two-nonneighbour comparison.  A local kernel port
exists exactly when the shared complete cofactor \(P_c\) vanishes; on
\(P_c\ne0\), common-star restriction is faithful.  A dense exact family
with \(P_c=0\), all lower double cofactors nonzero, and opposite local
three-port kernels shows that even nullity three on both maps gives no
shared exterior direction.  The family fails every cubic pure-cofactor
equation.  The remaining usable datum is therefore the nine pure
two-crossing Hessian equations with physical direct-block transpose
compatibility, not raw kernel dimension.

The independently audited
[weighted three-term exhaustion](polarized-eight-site-three-term-pair-cap-exhaustion.md)
closes the entire natural class containing that example.  Normalize one
flagged perfect matching and scan the \(420^2=176{,}400\) choices of the
other two.  Exactly \(9{,}888\) supports have only the three intended
decorated terms; \(7{,}968\) have the short Gram contradiction and the
remaining \(1{,}920\) close by projective orthogonality.  The
[clean-room audit](polarized-eight-site-three-term-pair-cap-exhaustion-independent-audit.md)
reproduces the ledger and hash through 96 odd-path and 1,824
isotropic-cycle certificates.  Each used coefficient is one nonzero
monomial, so arbitrary nonzero complex weights on the same supports are
allowed.  This remains a finite support-class theorem: extra or
endpoint-asymmetric cells, several decorated terms cancelling to one word,
and arbitrary \(q\) are not covered.

The independently audited
[one-cell invisible-direction theorem](polarized-eight-site-fixed-q-one-extra-pair-cap-obstruction.md)
now changes that sparse \(q\) itself in every single basis direction which
preserves the displayed polarized identity.  The exact census splits the 243
outside cells into 99 invisible directions on eleven physical pairs and 144
directions creating one or two mixed debts.  Of the 99, 66 retain the old
seven Gram coordinates; the other 15 asymmetric cases and 36 branches from
18 monochromatic cases all close by explicit projective zero triangles.  The
[clean-room replay](polarized-eight-site-single-invisible-cell-projective-closure-independent.md)
reconstructs the full census and all 51 hard certificates without importing
the primary code.  Thus no single invisible cell, at any complex scale, moves
the sparse polarized model into the pair-cap variety.  Simultaneous cells,
visible-debt cancellation, unrelated quadratics, and shared rows remain open.

The independently audited
[invisible full-block theorem](polarized-eight-site-invisible-full-block-pair-cap-obstruction.md)
now replaces a single cell by an arbitrary \(3\times3\) endpoint-colour block
on any one of the eleven invisible physical pairs.  Eleven independently
generated unsaturated affine ideals, each with 58 variables, reduce to
\([1]\), so zero entries and all exceptional complex ratios are included.
The
[projective-and-ideal replay](polarized-eight-site-invisible-full-block-projective-and-ideal-closure-independent.md)
independently closes 5,552 of 5,632 support strata by 11,056 explicit
orthogonality certificates and closes the remaining 80 pair-17 strata by a
separate 545-equation unit ideal.  This is a one-block theorem: cross terms
between two distinct physical blocks, visible-debt cancellation, unrelated
quadratics, and the global shared-cap descent remain open.

The clean-room
[exhaustive two-cell theorem](polarized-eight-site-two-cell-pair-cap-obstruction-independent-audit.md)
removes the next sparse ambiguity without presuming that the new cells are
individually invisible.  Exact row reduction over all 29,403 unordered pairs
finds exactly 3,960 nonzero-parameter polarized families; all have both
individual debts and their cross debt identically zero, so no pair of visible
debts cancels.  Projective parity closes 3,944 pair-cap systems and 16
independently ordered localized ideals close the residue with reduced basis
\([1]\).  This remains fixed-\((q,z)\) and exactly-two-cell: three-cell
cancellation, varying \(z\), arbitrary quadratics, and shared-cap overlap are
not covered.

The independently audited
[exact three-cell cancellation theorem](polarized-eight-site-fixed-q-three-extra-cancellation-frontier.md)
then exhausts all 2,362,041 triples of new cells.  Exact Laurent-debt
classification gives 2,274,826 singleton rejections, 87,027 identically
compatible triples, 187 genuinely new binomial cancellation families, and
one torus-inconsistent exceptional triple.  Projective parity closes 180 of
the 187 new pair-cap systems, and seven localized characteristic-zero unit
ideals close the remainder.  The
[clean-room reconstruction](polarized-eight-site-fixed-q-three-extra-cancellation-frontier-independent-audit.md)
independently rebuilds every divided power, all four exact ledgers, 202
parity certificates, and the seven ideals under reversed variable and
generator orders.  The theorem excludes only the 187 visible-debt
cancellation families at this fixed \((q,z)\).  The 87,027 identically
compatible triples remain outside that theorem's claim.

The independently audited
[compatible-three-cell obstruction](polarized-eight-site-fixed-q-compatible-three-extra-pair-cap-obstruction.md)
closes those 87,027 families.  Projective parity excludes 86,284; the sole
one-pair survivor is covered by the audited arbitrary pair-17 block theorem;
and all 742 multi-pair survivors have saturated unit ideals in both the
primary and independently reversed polynomial encodings.  The
[clean-room replay](polarized-eight-site-fixed-q-compatible-three-extra-projective-frontier-independent-audit.md)
reconstructs the complete compatibility graph, triangle census, projective
ledger, survivor list, and every ideal without importing the primary
verifiers.  Thus the displayed fixed \((q,z)\) has no exactly-three-cell
pair-cap deformation.  Four or more cells, varying \(z\), arbitrary
quadratics, and shared-cap overlap remain outside the combined claim.

The independently audited
[coordinate-monomial common-power obstruction](invertible-monomial-base-locus-common-power-obstruction.md)
also closes the exact formal base-locus escape isolated by the
invertible-monomial nine-cap classification.  For disjoint missing pairs,
the common-power equations kill the within-pair blocks and a crossing-factor
argument forces one local line to be two distinct colour axes.  With
arbitrary ordered missing pairs, the full nine-product table leaves only the
disjoint type and a directed two-edge path plus one disjoint edge; literal
four-support extraction excludes the second type.  The
[clean-room line audit](invertible-monomial-base-locus-common-power-obstruction-independent-audit.md)
checks the arbitrary-field tensor argument and all 27,000 labelled directed
triples.  Its coordinate-support restriction on the response rows has now
also been removed.  The stronger
[arbitrary-star monomial obstruction](arbitrary-star-monomial-base-locus-common-power-obstruction.md)
allows all six rows to have arbitrary multi-site support, arbitrary local
components, dependencies, degeneracies, and cancellations.  The literal
nine-product equations first rule out repeated missing pairs; a complete
\(15^3=3{,}375\) triple census then leaves only \(3K_2\) and
\(P_3+K_2\), and the common-power arguments exclude both without referring
to the response rows.  Its
[independent clean-room audit](arbitrary-star-monomial-base-locus-common-power-obstruction-independent-audit.md)
reconstructs the census, both positive response tables, three independently
ordered unsaturated unit ideals, and every tensor inference.  This closes
the single-pure-monomial lift model, not multi-term target lifts or the
unconditional U1 descent.

There is also a stronger power-only boundary.  The independently audited
[distinct-pair common-power obstruction](distinct-missing-pair-common-power-obstruction.md)
assumes only three distinct pure missing-pair lifts and
\(q^{[2]}=F,\ q^{[3]}=0\).  The relation \(qF=0\) kills their three edge
blocks, after which arbitrary-tensor arguments exclude all five support
graphs \(3K_2,P_3+K_2,P_4,K_{1,3},K_3\).  The
[independent line audit](distinct-missing-pair-common-power-obstruction-independent-audit.md)
reconstructs every graph case, interprets the star contraction through
one-dimensional square-zero local factors, and verifies exact formal
elimination syzygies.  Repeated missing pairs cannot be added to this
power-only statement because the ternary \(K_4\) construction is an exact
countermodel; the nine products rule them out in the preceding theorem.

The first genuine multi-term enlargement is also now closed.  The
independently audited
[one-multiterm obstruction](one-multiterm-monomial-common-power-obstruction.md)
allows two pure missing-pair lifts in one colour and one in each other
colour, with arbitrary nonzero complex weights and arbitrary multi-site
rows.  The products force all four supports to be distinct; an exact
target-preserving torus normalizes the weights; and the full \(qF=0\)
kernel has dimension 100 or 102 according as the two same-colour pairs are
disjoint or adjacent.  All 16,380 labelled supports reduce to 25 symmetry
orbits whose complete unsaturated characteristic-zero ideals are unit.  The
[independent reconstruction](one-multiterm-monomial-common-power-obstruction-independent-audit.md)
uses different representatives, edge and colour orders, kernel variables,
matching order, and generator stream and independently obtains all 25 unit
ideals.  This closes multiplicity profile \((2,1,1)\).

The next asymmetric enlargement is independently closed as well.  The
[three-term-in-one-colour obstruction](three-term-monomial-common-power-obstruction.md)
allows three pure missing-pair lifts in one colour and one in each other
colour.  The products force all five supports to be distinct, the exact
weighted \(qF=0\) system is the incidence kernel of the same-colour
three-edge graph, and the five graph types give full kernel dimensions
between 92 and 98.  A local torus normalizes all five weights.  All 60,060
labelled supports reduce to 70 symmetry orbits whose full unsaturated
characteristic-zero ideals are unit.  The
[independent reconstruction](three-term-monomial-common-power-obstruction-independent-audit.md)
uses different representatives, kernel coordinates, matching order, and
generator stream; it also records and invalidates its own early duplicated-
matching stream before recomputing all 70 ideals.  Thus, at that stage,
\((3,1,1)\) was closed while \((2,2,1)\), larger profiles, non-pure target
tensors, and the global descent remained open.

The finite pure-profile sequence is now subsumed by an independently audited
support-independent theorem.  The
[uniform pure-lift obstruction](uniform-pure-lift-private-edge-degeneration.md)
allows all 45 aggregate coefficients
\(\lambda_{cP}\), arbitrary support size, repeated colour/pair supports,
complex cancellation, arbitrary multi-site rows, and arbitrary
endpoint-ordered blocks of \(q\).  Literal response words force every colour
to have a private active pair \(P_c\).  The tensor product of local unital
square-zero algebra endomorphisms which kills the colour-\(c\) axis on
\(P_c\) retains exactly one pure lift per colour.  The three pairs are
distinct, so functoriality of matching powers reduces directly to the
distinct-missing-pair obstruction—without a limit, genericity, or orbit-
closure argument.  The
[independent clean-room audit](uniform-pure-lift-private-edge-degeneration-independent-audit.md)
reconstructs 20,250 response-provenance terms, all 2,730 ordered triples,
parallel aggregation, transverse coordinates, projection functoriality, and
the sharp repeated-pair \(K_4\) power witness.  Hence the full pure span is
closed; the remaining common-power frontier is genuinely non-pure.

That remaining branch cannot be attacked by scalar cofactor rank.  The
independently audited
[common-origin scalar countermodel](common-origin-factorization-rank-countermodel.md)
uses a weighted six-cycle with \(q^{[3]}=0\), an invertible cofactor matrix
of determinant \(-256\), and rational rows satisfying all nine equations
\(p_i s_jq^{[2]}=\delta_{ij}z_U\).  Associativity gives the proposed
middle-degree factorization \((p_iq)(s_jq)=2\delta_{ij}z_U\) with the same
common \(q\).  The
[clean-room audit](common-origin-factorization-rank-countermodel-independent-audit.md)
checks the symbolic determinant identity, both cancelling perfect matchings,
all 18 response/factor products, and 6,840 separate support factorizations.
Its target line is scalar, so it is not a Krenn counterexample; rather, it
shows that a valid non-pure proof must use the three sitewise-independent
target axes before contraction.

The independently audited
[one-/two-line-field response theorem](single-line-field-nonpure-response-obstruction.md)
now uses those axes directly.  No multiplier resolved by one or two coherent
local line fields can carry the three diagonal responses, even with arbitrary
coefficients, coincident fields, multi-site rows, and complex cancellation.
For three line fields which form a basis at every site, every target colour
must instead agree with a distinct field on at least four sites.  With all
nine responses, the three radius-two response modules split termwise, leaving
three aligned one-target components.  The
[clean-room audit](single-line-field-nonpure-response-obstruction-independent-audit.md)
checks the quotient argument, Segre secant rigidity, all 117,649 local support
boxes, and the direct-sum decomposition independently.  At that stage the next
exact common-power target was the aligned three-field residual: couple its at-most-two
deviant sites through \(F=q^{[2]}\), \(q^{[3]}=0\), or prove that an actual
edge quadratic cannot admit such a three-field resolution.  General
higher-rank edge blocks remain outside this theorem.

Two independently audited continuations now sharpen that frontier.  The
[sitewise common-power response filtration](sitewise-common-power-response-filtration.md)
defines \(W_u\) as the complete incident endpoint span, with no rank-one or
termwise support assumption.  Exact ideal orders force each target colour
into at least four of the six spaces and force the three incidence sets to
cover every site.  If every \(\dim W_u\le2\), equality is rigid: the \(W_u\)'s
are the three coordinate planes, omitted on three disjoint pairs, and the
single-colour four-site part is exactly the corresponding three lifts.
Its
[clean-room audit](sitewise-common-power-response-filtration-independent-audit.md)
reconstructs the determinant expansion, complementary-minor frontier,
plane census, arbitrary-rank chain identity, and sharp scalar-cycle model.
Mixed-colour four-site terms and any site with \(\dim W_u\ge3\) remain; the
filtration does not silently promote a leading minor to a nonzero term.

The independently audited
[coordinate-plane mixed-packet obstruction](coordinate-plane-mixed-packet-obstruction.md)
now closes the first of those two alternatives.  A double quotient forces
each complete omission-pair hole slice to be pure and makes every nonzero
mixed hole carry a zero response matrix.  Four-site target-apex rigidity
excludes all disconnected mixed-cofactor graphs; connectivity then propagates
the response vectors to common lines, contradicting the three diagonal
matrix units.  Its
[clean-room audit](coordinate-plane-mixed-packet-obstruction-independent-audit.md)
rebuilds every \(3+3\), \(2+2+2\), and \(2+4\) graph case and the sharp
two-triangle model independently.  Hence any surviving arbitrary-block
six-site response must have \(\dim W_u\ge3\) at some site (equivalently, full
rank three after projecting every local space to its target three-space).  This result allows
multi-site rows and arbitrary complex plane blocks and does not use
\(q^{[3]}=0\), but it does not itself produce an all-even cap.

The independently audited
[full-rank-site response frontier](full-rank-site-response-invisibility-countermodel.md)
now fixes the scope of the other alternative.  Exact rational models retain
one, and then two, independent target frames while satisfying \(q^{[3]}=0\),
all nine responses, the determinant and adjugate identities, generically
invertible cofactors, and the sitewise chains; nevertheless only one incident
space has rank three and the remaining incident spaces are lines.  The
[clean-room audit](full-rank-site-response-invisibility-countermodel-independent-audit.md)
rebuilds both square-zero algebras, all tensor responses, both cofactor
determinants, and every endpoint order.  These are not Krenn counterexamples:
their target ranks collapse at four or five sites and their endpoint-rank
budget is only eight.  They prove that a positive argument must use the
global four-cover, not one- or two-site scalar propagation.

That global input does leave a finite equality frontier.  Every genuine
response has \(\sum_u\dim W_u\ge12\).  When equality holds and some site has
rank three, the only rank-count triples are
\((1,4,1),(2,2,2),(3,0,3)\).  A typed double quotient makes the three
two-site omission sets pairwise distinct and forces each *entire* associated
four-site slice of \(F=q^{[2]}\) to be pure.  Thus the equality case has only
three overlap geometries: two pairs meeting once plus a disjoint pair, a
three-edge path, or a triangle.  Those three geometries and rank budget
strictly above twelve were the exact arbitrary-block residuals at that stage.

The independently audited
[typed exposed-grid obstruction](rank-budget-path-triangle-exposed-grid-obstruction.md)
now closes the path and triangle.  Each omission pair exposes its complete
grid of missing-colour quotient coordinates.  Two adjacent target corners
and their crossed zero corners force all four response points to be pure of
alternating types; an additional zero corner is then impossible in both
geometries.  The
[clean-room reconstruction](rank-budget-path-triangle-exposed-grid-obstruction-independent-audit.md)
checks every mixed and half-zero branch and independently obtains the two
UNSAT parity systems.  It also supplies four exact rational quotient-grid
witnesses for the wedge-plus-disjoint case, so that case is not silently
claimed closed by the quotient grid alone.  The
[unconditional wedge obstruction](wedge-equality-hole-block-resolution.md),
independently reconstructed in a
[clean-room audit](wedge-equality-hole-block-resolution-independent-audit.md),
now supplies the missing common-power step.  Five complete cofactor zeros,
the rank-one-site cubic, both single-survivor branches, and a final
twelve-component tensor syzygy exclude arbitrary
\(q_{ab},q_{bc},q_{de}\).  Hence every budget-twelve equality geometry
having a rank-three site is closed; rank budget strictly above twelve
remains.

Within the three-field resolution, the independently audited
[aligned common-power obstruction](aligned-three-field-common-power-obstruction.md)
uses the actual equations \(F=q^{[2]}\), \(q^{[3]}=0\).  Every target colour
must have an exactly zero assigned-field coordinate at some site.  If all
three deviant sets have size two, two coincide at a pair \(P\), the third is
a different pair \(Q\), and all active lift supports lie in \(\{P,Q\}\).
All 462 residuals in which the deviant target frames merely permute field
axes are impossible.  The
[independent audit](aligned-three-field-common-power-obstruction-independent-audit.md)
rechecks the module split, unital selected-pair projection, Hall alternatives,
shared-pair rank argument, and complete permutation census.  At that stage the
exact remaining aligned charts used genuine linear mixtures at hard-zero sites;
one-site deviations and the two-pair all-two-site stratum still had to be closed
without treating those mixtures as coordinate axes.

That last aligned residual is now closed.  The independently audited
[two-pair common-power theorem](two-pair-six-term-common-power-obstruction.md)
observes that the Hall alternative and singleton collision actually force
**every** aligned solution onto exactly two physical pairs, with only the
profiles \((2,1,1)\), \((2,2,1)\), and \((2,2,2)\).  The first profile
contradicts the split response equations directly.  In the other two, the
necessary equation \(qF=0\) has rank 18 on the active pair blocks, and all
adjacent and disjoint unsaturated \(q^{[2]}-F\) ideals are unit over
\(\mathbb Q\).  The
[clean-room reconstruction](two-pair-six-term-common-power-obstruction-independent-audit.md)
uses different coefficient and monomial orderings and independently obtains
all six unit ideals.  Consequently a multiplier resolved into three coherent
line fields forming a basis at every site is impossible, including all
genuine hard-zero mixtures.  The remaining coherent-field frontier at that
stage was local degeneracy of the three-field frame; beyond it lie
four-or-more-field and non-line-field mixed packets.

The independently audited
[degenerate three-line-field response normal form](degenerate-three-line-field-response-normal-form.md)
now resolves the response combinatorics at the first local rank drop.  If all
six local field spans have dimension at most two, projecting only \(q\) to
the forced coordinate planes leaves the original rows, targets, and power
equations unchanged, so the coordinate-plane theorem closes the branch.  If
exactly one site is deficient, the five good frames force every target box
to be axial or a unique binary bridge.  Boundary words then give the exact
active-pair families, singleton collisions, and layer-Hall alternatives.  A
[clean-room reconstruction](degenerate-three-line-field-response-normal-form-independent-audit.md)
checks all 759,375 ordered boxes, the \(6,093+423\) axial/bridge split, all
250,047 layer-Hall systems, and the \(141/110\) bridge census.  This theorem
does not cover two deficient sites.

At one deficient site, two exact theorems first reduce the problem to one
finite packet layer.  The independently reconstructed
[distinct-lift obstruction](sole-defect-distinct-lift-common-power-obstruction.md)
rules out every ordinary SDR whose selected pairs admit a locally separable
bad-site quotient; all 52 unsaturated common-power ideals are unit, including
the cases in which unused killed field images must be replaced by nonzero
dummies.  The independently reconstructed
[two-pair obstruction](sole-defect-two-pair-common-power-obstruction.md)
proves ordinary Hall failure impossible: all 105 simultaneous coefficient
normalizations have a unimodular good-site minor, and all 65 two-pair ideals
are unit over \(\mathbb Q\).  Therefore any sole-defect survivor has an
ordinary SDR.  The
[nonseparable-packet theorem](sole-defect-nonseparable-packet-common-power-obstruction.md)
and its independent
[clean-room reconstruction](sole-defect-nonseparable-packet-common-power-obstruction-independent-audit.md)
exhaust the remaining bad-site matroid patterns.  The exact orbit census is
\(1284\to157=145+12\): all 145 rational coefficient-normalized ideals are
unit, and the twelve full-packet families are unit over
\(\mathbb Q[\mu,\mu^{-1}]\).  The independent elimination inverted only
rational units and powers of \(\mu\), so no exceptional nonzero parameter
was discarded.  The response-to-Hall-to-packet implication was also
reconstructed line by line.  Thus the entire exactly-one-deficient-site
branch is empty.  The remaining coherent three-field cases have two through
five deficient sites and at least one full local frame; the all-six-deficient
case is already closed by the coordinate-plane theorem.

At exactly two deficient sites, the independently audited
[balanced-word coupling](two-deficient-balanced-word-coupling.md) keeps both
bad-site tensor factors.  A supported \(2+2\) word puts the target bad-site
product on the Segre line of the two corresponding coherent products.
The
[clean-room reconstruction](two-deficient-balanced-word-coupling-independent-audit.md)
checks all \(15^4=50,625\) support boxes and reduces the nonaxial
balanced-free escape to ten orbits (492 labelled boxes).  Their uniquely
centred words prove the
[double-bad-site coincidence theorem](two-deficient-exceptional-boundary-word-coincidence.md):
the same pair of field lines must coincide at both bad sites.  Axial boxes,
intersections of the balanced-word constraints, and the resulting
double-coincidence strata remain; no common-power or uniform conclusion is
claimed.

The sparse counterexample search has one independently audited positive
boundary result, but its scope is deliberately narrower.  The
[mixed-endpoint one-site support frontier](mixed-endpoint-one-site-support-frontier.md)
retains all 135 endpoint-ordered coordinate cells and reduces all 27,000
one-site coordinate-row triples to path--edge and matching geometries.  Its
[Laurent closure](mixed-endpoint-one-site-laurent-closure.md) proves exact
support lower bounds 33 and 34 respectively, using cancellation-aware cuts
which permit a third matching term to turn a binomial into a trinomial.  The
[clean-room audit](mixed-endpoint-one-site-laurent-closure-independent-audit.md)
rebuilds the row orbits and coefficient clauses, returns different valid HNF
circuits, and confirms the final UNSAT layers with a second solver.  This is
useful countermodel falsification only: it says nothing about multi-site
rows, non-coordinate endpoint blocks, or existence at the first surviving
support sizes.

The one-crossing factor criterion is now known to be unusable in the
ternary problem, not merely unproved.  For every five-set \(U\), the
[universal cofactor-annihilator theorem](five-set-universal-cofactor-annihilator.md)
uses the arbitrary-complex six-site obstruction dually to produce
\(\beta\in\ker {\cal B}_U\) with \(\delta_U(\beta)\ne0\).  Since every
one-crossing flattening factors as

\[
                         F_1=\Gamma_{C,U}{\cal B}_U,
\]

one has \(\ker F_1\not\subseteq\ker\delta_U\) for every edge family and
every five-set.  Thus no proof can obtain a successful cut by establishing
that kernel inclusion.  Under a hypothetical full GHZ identity, the same
target-active defect is instead routed entirely through the three- and
five-crossing sectors on every cut.  The viable continuation is to couple
those nonzero quotient maps across adjacent five-sets, where they reuse the
same aggregate edge factors.  A single-cut common-power or dimension
argument is structurally exhausted.

The first kernel-only version of that adjacent-cut continuation is also
false.  The exact
[adjacent five-cut countermodel](adjacent-five-cut-hessian-intersection-countermodel.md)
has two target-active adjacent defect spaces but a target-zero intersection
of their lifted six-site kernels.  The same note proves the useful
division-free identity

\[
                         \sum_{z\in S}T_{1,z}=6T_0+2T_2,
\]

so a target-active functional common to all six lifted kernels would indeed
exclude an eight-site GHZ tensor.  What fails is automatic existence, even
for one adjacent pair.  A surviving overlap theorem must therefore use the
actual shared three-crossing response maps, not just the cofactor kernels or
their target defect lines.

Even two complete adjacent response maps are insufficient.  The independently
audited
[complete high-sector countermodel](adjacent-five-cut-complete-high-sector-countermodel.md)
first proves the exact order-eight decompositions

\[
 T_{1,z}=T_0+\sum_{a\ne z}T_2^{za},\qquad
 T_{3,z}=\sum_{\{a,b\}\subset U_z}T_2^{ab},
\]

and a division-free summed-lift lemma.  One shared zero-one edge family then
satisfies the full restriction identity
\(T_{3,z}|K_{U_z}=\iota\delta_{U_z}|K_{U_z}\) on two adjacent cuts.  Its
lifted-kernel intersection is target-zero, while two explicit witnesses
still contract \(T_2\) to a nonzero diagonal target.  The family has two
mixed full-tensor coefficients and is therefore not a Krenn counterexample;
it exactly refutes the proposed two-cut implication.  Any surviving overlap
theorem must use at least three cuts or additional mixed-sector identities.

The first exact test at that threshold is positive but deliberately narrow.
The independently replayed
[three-cut one-factor exhaustion](three-cut-complete-high-sector-onefactor-exhaustion.md)
checks all 11,130 normalized triples of constant one-factors, allowing
overlapping factors and multicolor shared edges.  Exact rational row-space
tests show that at most two of the six cuts can satisfy the complete
restriction with target-active defect; two is attained.  This rules out a
three-cut countermodel in the smallest natural factor family, but it does
not establish the needed implication for arbitrary endpoint-ordered
aggregate matrices.

The wider
[two-extra one-factor reconnaissance](fourth-two-onefactor-three-cut-extension-reconnaissance.md)
starts from the sharp two-cut model and exhausts all 1,786,995 unordered
pairs of added constant-colour one-factors with weights
\(\{-3,-2,-1,1,2,3\}\).  Exact rational tests again find at most two
active complete cuts.  This remains finite reconnaissance, not a theorem
for arbitrary weights, nondiagonal cells, more factors, or general
aggregate matrices.

The unrestricted bare three-cut implication is now false as well.  The
independently audited
[three-adjacent-cut countermodel](three-adjacent-five-cut-complete-quotient-countermodel.md)
has twelve integral endpoint-decorated sources, one shared residual in all
three cofactor-insertion cylinders, and target-defect dimensions
\((1,1,2)\) on \(z=2,3,4\).  Its tensor is
\(e_1^{\otimes8}+e_2^{\otimes8}+e_{00210012}\), so it is not monochromatic
and is not a Krenn counterexample.  Two additional integral cells cancel
that mixed word while preserving all three quotient identities and move the
debt to three other mixed words.  The
[independent reconstruction](three-adjacent-five-cut-complete-quotient-countermodel-independent-audit.md)
checks the complete annihilators, literal cylinder decompositions, endpoint
order, parallel aggregation, defect dimensions, and repaired tensor over
\(\mathbb Q\).  Hence neither three complete cuts nor one selected mixed
coefficient can be the missing descent invariant.

The independently audited
[boundary-star strengthening](three-cut-boundary-star-strengthening-obstruction.md)
tests the first actual endpoint-factor continuation, rather than a formal
cut-space relaxation.  With every repaired nonstar block fixed, all 63
cells on either site-6 or site-7 star may vary arbitrarily over
\(\mathbb C\).  No such one-star family activates a fourth cut
\(z=0,1,5\), and exact support identities prevent cumulative vanishing of
the original mixed word and even the first repaired debt while retaining
the relevant old cut.  Its
[independent reconstruction](three-cut-boundary-star-strengthening-obstruction-independent-audit.md)
checks the full symbolic stars, the defect dimensions, and the distinction
between literal three-debt undo and cumulative repair.  This sharply
excludes one-star repairs of the sparse model; it says nothing global about
simultaneous two-star or internal-block changes.

The independently audited
[two-boundary-star countermodel](three-cut-two-boundary-star-cumulative-repair-countermodel.md)
shows that the four recorded mixed coordinates are not a coupled sector.
An actual thirteen-source decorated family preserves the three active cuts,
kills all four suffix-\(12\) debts, and moves the sole residual to suffix
\(21\); one direct boundary cell repeats the same debt transport there.
The [independent reconstruction](three-cut-two-boundary-star-cumulative-repair-countermodel-independent-audit.md)
checks every matching, cut, defect, and repaired word.  This is still not a
Krenn counterexample.

The fourth-cut branch is now exact for that same fixed interior.  The
[cylinder-intersection theorem](three-cut-fourth-cut-fixed-interior-intersection.md)
reduces cuts \(2,3,4,5\) to the residual line
\(\langle H_S\rangle\otimes V_{67}\), and cuts \(2,3,4,0\) or
\(2,3,4,1\) to a specific two-plane residual.  Its
[independent audit](three-cut-fourth-cut-fixed-interior-intersection-independent-audit.md)
uses direct primal intersections.  The independently audited
[two-star Segre obstruction](three-cut-two-boundary-star-fourth-cut-segre-obstruction.md)
then retains every complex entry on both shared stars, the direct boundary
block, all three unit diagonal targets, and all six off-diagonal fibers.
Exact component decomposition followed by 3,621 unit-ideal checks excludes
both residual normal forms.  Hence this repaired interior cannot be upgraded
to four cuts by any boundary-only change; the result does not constrain
simultaneous internal-block perturbations in an arbitrary Krenn instance.

The first controlled internal perturbation is now closed as well.  The
independently audited
[two-cell (23)-block theorem](three-cut-internal-23-two-cell-fourth-cut-obstruction.md)
allows

\[
                         A_{23}=tE_{21}+sE_{00}
\]

for arbitrary complex (t,s), while retaining all other interior cells,
both arbitrary boundary stars, the arbitrary direct boundary block, and all
nine target fibres.  A target-preserving diagonal torus reduces the family
to four support strata, and 12,032 exact component unit certificates exclude
cuts (0,1,5) in every stratum.  Its
[independent reconstruction](three-cut-internal-23-two-cell-fourth-cut-obstruction-independent-audit.md)
rebuilds the endpoint-ordered cofactors, cylinder intersections, torus
covariance, and the exceptional two-colour equivalence without importing the
primary checker.  This remains a theorem about one two-cell internal family,
not a general (3\times3) block or a global four-cut invariant.

The full natural five-cell plane-normal locus is now closed as well.  The
independently audited
[five-cell (23)-block theorem](three-cut-internal-23-plane-support-fourth-cut-obstruction.md)
allows

\[
 A_{23}\in\langle E_{00},E_{01},E_{02},E_{11},E_{21}\rangle_{\mathbb C}
\]

with the same arbitrary stars, direct block, and nine target fibres.  A
target-preserving torus exhausts the family by 32 support masks.  The five
variable cells contribute pairwise-disjoint 35-coordinate blocks, allowing
the masks to be partitioned into five exact quotient systems; their rational
ideals have 216, 268, 504, 484, and 588 generators and reduced standard
basis \([1]\).  The
[independent reconstruction](three-cut-internal-23-plane-support-fourth-cut-obstruction-independent-audit.md)
freshly verifies all 96 cylinder intersections, literal endpoint order, all
nine fibres, the support partition, and every unit ideal.

The full endpoint-ordered \((23)\) block is now closed on the same fixed
interior.  The independently audited
[arbitrary-(23)-block theorem](three-cut-internal-23-arbitrary-block-fourth-cut-obstruction.md)
allows \(A_{23}\in\operatorname{Mat}_{3\times3}(\mathbb C)\), with both
boundary stars, the direct boundary block, and all nine target fibres still
arbitrary.  The nine cell-dependent cofactor blocks are pairwise disjoint.
They reduce the 480 supports outside the old five-cell locus to 27 finite
torus charts and one cross-ratio chart; the former give 27 rational unit
ideals and the latter gives a 628-generator unit ideal in
\(\mathbb Q[\lambda]\).  The
[independent clean-room reconstruction](three-cut-internal-23-arbitrary-block-fourth-cut-obstruction-independent-audit.md)
rebuilds all 480 masks, the exact endpoint-ordered eight-site identity,
projected cylinder intersections, the 108 shared-star entries, and all 28
unit ideals through a different sparse-elimination route.  This exhausts all
512 supports of that one block, but it still fixes every other internal
block.  It is not a general six-site obstruction or a global fourth-cut
implication.

The first simultaneous internal perturbation is now closed on the same
background.  The independently audited
[adjacent two-block theorem](three-cut-internal-23-arbitrary-block-adjacent-25-line-fourth-cut-obstruction.md)
keeps \(A_{23}\) arbitrary and lets

\[
                         A_{25}=E_{00}+tE_{11}
\]

for arbitrary complex \(t\), while the other seven internal cells remain
fixed and both stars and \(A_{67}\) remain arbitrary.  The new coefficient
has an independent torus character, and edges 23 and 25 cannot coexist in a
matching, so no \(Xt\) term is hidden.  The \(t\ne0\) proof consists of five
old-locus, 27 finite outside-locus, and one symbolic cross-ratio unit ideal;
\(t=0\) is the preceding arbitrary-block theorem.  The
[clean-room reconstruction](three-cut-internal-23-arbitrary-block-adjacent-25-line-fourth-cut-obstruction-independent-audit.md)
rechecks the 512-mask modulus census, the 35-coordinate moving block and its
three nine-coordinate overlaps, safe projected normals, all 108 shared-star
entries, and all 33 exact ideals.  This is a one-dimensional affine slice in
the second block, not an arbitrary two-block theorem.

Four more adjacent directions are now closed on the same background.  The
independently audited
[four-off-diagonal-line theorem](three-cut-internal-23-arbitrary-block-adjacent-25-four-offdiagonal-lines-fourth-cut-obstruction.md)
allows

\[
 A_{25}=E_{00}+tE_{cd},\qquad
 (c,d)\in\{(0,1),(0,2),(1,2),(2,1)\},
\]

while \(A_{23}\), both boundary stars, and \(A_{67}\) remain arbitrary.
Each direction exhausts all 512 supports of \(A_{23}\) through five
inherited, 27 finite, and one symbolic cross-ratio chart.  Every one of the
\(132=4(5+27+1)\) characteristic-zero ideals is unit.  The
[independent reconstruction](three-cut-internal-23-arbitrary-block-adjacent-25-four-offdiagonal-lines-fourth-cut-obstruction-independent-audit.md)
regenerates the endpoint-ordered matching tensors, torus action, safe
projected normals, shared-star equations, and all 132 ideals under different
orders.  Together with the \(E_{11}\) theorem, exactly the directions
\(E_{10},E_{20},E_{22}\) remained open in this one-cell second-block
frontier at that stage.  The conclusion is still local to the fixed interior.

The independently audited
[adjacent \(E_{22}\) theorem](three-cut-internal-23-arbitrary-block-adjacent-25-22-fourth-cut-obstruction.md)
now closes one of those three directions.  It retains arbitrary \(A_{23}\),
both shared boundary stars, and arbitrary \(A_{67}\), and treats every
complex \(t\) in \(A_{25}=E_{00}+tE_{22}\).  Six symbolic open charts and
eight exact exceptional supports cover all 512 \(A_{23}\) supports.  The
proof uses 13 constant full-cylinder rank minors, a separate uniform cut-5
intersection through every rank jump, and 21 characteristic-zero unit
ideals for 30 chart/cut jobs.  The
[clean-room reconstruction](three-cut-internal-23-arbitrary-block-adjacent-25-22-fourth-cut-obstruction-independent-audit.md)
rebuilds endpoint order, the torus cover, true exceptional normals, all nine
literal fibres, and every ideal under different orderings and frozen
ledgers.  Exactly \(E_{10},E_{20}\) remain in this one-cell frontier.  On
their fully nonzero strata the stabilizer characters have rank five, with
\(\operatorname{wt}(t)=\operatorname{wt}(x_{10})-
\operatorname{wt}(x_{00})\) or
\(\operatorname{wt}(t)=\operatorname{wt}(x_{20})-
\operatorname{wt}(x_{00})\).  Hence the unavoidable parameters are
\(\lambda=t x_{00}/x_{10}\) and
\(\lambda=t x_{00}/x_{20}\), respectively.  The concrete next test is to
stratify coordinate vanishing first, then construct full-cylinder normal
certificates and shared-star unit ideals over \(\mathbb Q[\lambda]\), rather
than reuse an independent-\(t\) normalization.  This remains a fixed-interior
local result, not a global fourth-cut theorem.

This sharpens, but does not solve, the middle-arrow diagnosis from Section
1.  Product caps still reduce the target exactly to six sites while their
higher cumulants need not pairify; general five-cut one-crossing responses
now fail for the opposite universal reason.  An unconditional descent must
therefore use at least a fourth overlapping cut, a coupled packet of mixed
coefficients, the actual common-power condition, or a different global
invariant.

## 4. Route-registry audit

[The route registry](route-registry.md) is a chronological research log,
not a proof dependency graph.  Its completed local statements and its global
implications must therefore be read separately.  The initial audit made six
bookkeeping corrections:

1. removed the duplicated top-level route identifier `I1`;
2. updated the $k=5$ census first from $7/37$ to $10/34$, then through
   the independently audited $18/26$ frontier to the completed $44/0$
   ledger;
3. registered the mixed-linear, seven-double, historical parallelogram,
   all-order incidence/census, and five-double endpoint notes;
4. registered the all-order incidence, bounded numerator, and first
   $p=18$ overlap theorems without promoting their residual families; and
5. promoted the minimal three-extra frontier from $24/27$ to $27/27$ only
   after clean independent $CCB/CBC/BCC$ replays over $\mathbb Q$; and
6. registered the retained 20-column two-extra response and promoted its
   minimal $(2,0)$ case only after separate exact replays of the central
   divisor branches and all eight ordered boundary cells.

The 2026-07-26 continuation also refreshed the stale top-level `OC1` status:
on its fixed repaired interior the registry now records the arbitrary
\(A_{23}\) block and the initial adjacent \(A_{25}\) line closure.  The
2026-07-27 continuation adds four off-diagonal \(A_{25}\) lines and the
separately audited \(E_{22}\) line, while still
marking general simultaneous internal blocks and the full mixed-sector
implication open.

Subsequent promotions obeyed the same rule.  The registry now includes the
common octic and nonic closures, the decic four-space closure and its exact
five-space saturation closure, the undecic closure, the uniform
fixed-numerator closure of both stable tails for every $m\ge12$, and the
general-collision extension plus the independently audited quadruple/triple
role-lift closure, which together complete the selection-free eighth-split
ledger including $k=6$; the $p=18$
overlap closures through $a=3$, all nine $a=2$ families, and the complete
low-triple common-lift theorem, which together close all $50$ equality
families on the first saturated five-space diagonal; the three independently
audited $p=19$ common-lift, parity-pencil, saturated Klein-plane,
undecic singleton--double, five-triple even-span, developable-secant, and
singleton pair-line clique theorems, which close all 94 families on the
next diagonal; the uniform developable-secant extraction and its four
new $p=20$ one-quintuple exclusions; the exact $p=28$ six-kernel
frontier, the independently audited tangent-involution, even--odd span,
all-triple residual-quartic, balanced-splitting, and balanced-annihilator
closure, uniform critical moving-triple, critical local-jet,
three-quartic all-\(q=5\) saturation, two-quartic Robin pair-plane,
rank-one residual closure, two-quartic singleton-swap, and two-quartic
\(q=5\) grid theorems,
which bring its dimension-drop ledger to 341/344, force a six-dimensional
common kernel and all six exact \(q=5\) selections on the $4^3 3^6$ core,
narrow its full nondevelopable residual to the two degree-six rank-two
bundle splittings, independently falsify both the opposite-sheet
kernel-orientation shortcut and a bare cubic-pair intersection closure, and
turn both
$3^{10}$ and both $4^2 3^7 1$ families into actual profile closures;
the independently audited pure-fifth-pole frontier, which supplies exact
formal $q=6$ models for the remaining $4^7 1$ one-selection branch;
the independently audited three-adjacent-cut countermodel, which refutes
the bare three-cut quotient implication and its first one-coordinate mixed
strengthening without claiming a Krenn counterexample;
the independently audited boundary-star strengthening, which excludes
arbitrary one-star fourth-cut and cumulative-debt repairs only on that
fixed sparse background;
the independently audited two-boundary-star debt transport,
fourth-cut cylinder intersection, and exact Segre obstruction, which close
every boundary-only fourth-cut repair of that same fixed interior without
claiming a global obstruction;
the independently audited two-cell internal-(23) perturbation theorem,
which excludes all complex (tE_{21}+sE_{00}) repairs through the same
arbitrary stars and direct block but does not cover a general internal block;
the independently audited five-cell internal-(23) plane-locus theorem,
which closes all 32 complex support orbits in
\(\langle E_{00},E_{01},E_{02},E_{11},E_{21}\rangle\);
the independently audited arbitrary internal-(23) block theorem, which
adds all 480 outside-locus supports, including the exact
\(\mathbb Q[\lambda]\) cross-ratio wall, but still fixes the other eight
internal cells and therefore does not cover simultaneous internal
perturbations;
the independently audited adjacent two-block theorem, which retains an
arbitrary \(A_{23}\) while allowing \(A_{25}=E_{00}+tE_{11}\), but fixes the
other seven internal cells and does not allow a general second block;
the independently audited four-off-diagonal-line extension, which retains
arbitrary \(A_{23}\) and closes the \(01,02,12,21\) affine directions in
\(A_{25}\), leaving \(10,20,22\) outside its claim;
the independently audited adjacent-\(E_{22}\) theorem, which closes that
sixth affine line on all 512 \(A_{23}\) supports through full-cylinder
minors and 21 exact unit ideals, leaving \(10,20\) but not making
\(A_{25}\) arbitrary;
the independently audited projective-height obstruction, which proves that
the clean-cap cubic can have only forbidden-hyperplane components even under
the complete linear top GHZ identity, but uses an abstract rather than
common-edge signature;
the independently audited actual-cofactor prism barrier, which retains one
genuine common-edge cap subspace and independent active forms with unit
saturation, but is not globally GHZ outside that subspace;
the independently audited maximal transverse prism-slice countermodel,
which retains the same unit-saturation prism on the unique maximal
\(75\)-dimensional diagonal-image and \(73\)-dimensional literal-GHZ cap
slices, with effective rank four and a \(69\)-dimensional common kernel,
but leaves eight explicit transverse rows and is not a global source;
the independently audited literal shared pair-cap countermodel, which solves
one exact \(z=aq+4ps\) row while its fixed core fails all nine shared rows;
the independently audited pair-slice exchange theorem, which proves that a
second complete deleted-pair tensor system is a reindexing of the same
residual ideal and can help elimination but supplies no new equations;
the independently audited uniform full-nine target-incidence theorem, which
forces each target axis at all but two boundary sites, covers every site by
some target axis, gives at least \(N-8\) target-full internal sites after
every pair deletion, but does not convert aggregate target incidence to
blockwise nonzero rows or a clean cap;
the independently audited target-flattening essential-star theorem, which
gives at least \(N(N-7)/2\) doubly aggregate-injective pairs for every even
\(N\ge8\), a good fan of degree at least \(N-7\), a four-degenerate bad-pair
graph, and a good clique of size at least \(\lceil N/5\rceil\), but remains
aggregate and palette-relative;
the independently audited injective-star Hessian frontier, which derives
localized sparse missing rows under connected gauge-rigid support and all
six such rows under the non-bipartite hypothesis, while exact binary and
fourteen-site structural models prove that aggregate injectivity by itself
does not force those hypotheses;
the independently audited good-pair fan six-port reduction, which either
produces linearly many Hessian escape charts or three literal zero-block
neighbours with exact coupled triple-cofactor tables, but whose abstract
six-port response remains consistent until common physical cofactors are
used simultaneously;
the independently audited induced-zero-shore hierarchy, which either
produces linearly many Hessian escape charts or a linearly growing sparse
zero shore with an exact common-power identity, and caps the first zero
\(K_4\) case to at most 24 ports without claiming the capped tensor is
itself a matching power;
the independently audited twelve-port capped-table countermodel, which
satisfies all 81 rows with support-one anchored injective frames and proves
that the abstract finite response is consistent, while excluding only the
fixed-perfect-matching lift and leaving general common-power provenance
open;
the independently audited complete-bipartite all-pair countermodel, which
realizes every pair as a connected-bipartite good escape with one common
quadratic and exact pure normalization, but has mixed residual
\(2^{s-1}\), proving mixed GHZ vanishing is indispensable;
the independently audited cubic leave-one-anchor nullity web, which forces
minimum cofactor-nullity profile \((1,2,2)\) at every nonneighbour on the
three-essential equality stratum, but does not yet turn those kernels into
a cap or descent;
the independently audited cubic common-cofactor-zero boundary, which makes
common-star kernel restriction faithful when \(P_c\ne0\) and supplies a
dense all-even \(P_c=0\) family whose opposite local three-port kernels
show that raw nullity compatibility is insufficient;
the independently audited eight-site polarized countermodel, which proves
that the bare equation \(zq^3/3!=\Delta_{8,3}\) has an integral solution
but excludes that solution from \(z=aq+4ps\) by a rank-three cross minor;
the independently audited fixed-\(q\) strengthening, which excludes every
other target preimage for that same nine-cell \(q\) by a seven-entry
two-dimensional Gram contradiction, but does not vary \(q\);
the independently audited weighted three-term exhaustion, which excludes
all \(9{,}888\) combinatorially exact supports with arbitrary nonzero
weights but not extra cells or cancellation;
the independently audited one-cell invisible-direction theorem, which
excludes all 99 single-cell affine deformations preserving the sparse
polarized identity, including endpoint-asymmetric cells, but not simultaneous
deformations or visible-debt cancellation;
the independently audited invisible full-block theorem, which excludes an
arbitrary \(3\times3\) endpoint-colour block on any one of the eleven
invisible physical pairs, but not blocks on two distinct pairs;
the independently audited exhaustive two-cell theorem, which excludes all
3,960 exactly-two-new-cell polarized families and proves that none of the
other 25,443 pairs can preserve the displayed identity by visible-debt
cancellation, but does not treat three new cells or a varying \(z\);
the independently audited exact three-cell cancellation theorem, which
exhausts all 2,362,041 triples and excludes pair-cap lifts for all 187 new
visible-debt cancellation families;
the independently audited compatible-three-cell obstruction, which closes
the remaining 87,027 identically compatible triples through 86,284
projective certificates, the arbitrary pair-17 block theorem, and two
independent 742-unit-ideal batches, but does not treat four cells or varying
\(z\);
the independently audited coordinate-monomial common-power theorem, which
closes both ordered missing-pair types allowed by the full nine-product table
at six sites, but does not allow general multi-site star rows or multi-term
target lifts;
the independently audited arbitrary-star monomial common-power theorem,
which removes the support restriction on all six rows and the initial
distinct-pair assumption, but still requires exactly one pure four-site
monomial lift per target colour;
the independently audited distinct-pair power-only theorem, which excludes
all five simple three-edge support graphs without response rows but is
sharply false for repeated missing pairs;
the independently audited one-multiterm theorem, which closes all 16,380
labelled supports of the pure multiplicity profile \((2,1,1)\) through 25
full affine unit ideals, but does not cover larger profiles or non-pure
four-site tensors;
the independently audited three-term-in-one-colour theorem, which closes all
60,060 labelled supports of the pure multiplicity profile \((3,1,1)\)
through 70 full affine unit ideals, but does not cover \((2,2,1)\), larger
profiles, or non-pure four-site tensors;
the independently audited uniform pure-lift theorem, which subsumes all
finite pure profiles by closing the entire 45-dimensional aggregate pure
span, including arbitrary multiplicity, repeated supports, complex
cancellation, arbitrary multi-site rows, and endpoint-ordered blocks, but
does not cover non-pure four-site tensors;
the independently audited scalar common-origin countermodel, which refutes
every rank-only continuation after scalarizing the three target tensors but
is not a Krenn counterexample because its target is one-dimensional;
the independently audited one-/two-line-field theorem, which excludes those
coherent resolutions and aligns a full three-field frame outside at most two
sites per target colour, but does not classify its common-power residual;
the independently audited sitewise endpoint filtration, which forces a
four-cover and completely classifies the local-rank-at-most-two boundary but
initially retains its mixed-colour four-site packet and every local-rank-at-least-three
chart;
the independently audited coordinate-plane mixed-packet theorem, which
closes that entire rank-at-most-two boundary for arbitrary plane blocks and
multi-site rows without using \(q^{[3]}=0\), but leaves the incident-rank-at-least-three
escape and global descent;
the independently audited full-rank-site frontier, whose one- and two-site
countermodels rule out scalar determinant/adjugate propagation, while its
positive rank-budget theorem reduces the equality case to three distinct
omission-pair geometries with three complete pure hole slices; independently
audited typed-grid and hole-block arguments close path, triangle, and wedge,
leaving only budget strictly above twelve open;
the independently audited aligned three-field theorem, which forces one hard
zero per colour, confines the all-two-site branch to two physical pairs, and
eliminates all coordinate-permutation deviations;
the independently audited two-pair common-power theorem, which upgrades Hall
to a universal two-pair/profile reduction and closes all remaining aligned
full-rank three-field mixtures through one response contradiction and four
required unsaturated unit ideals (with two additional unit-ideal controls),
but does not force an arbitrary multiplier into that resolution;
the independently audited mixed-endpoint one-site Laurent frontier, which
proves support lower bounds 33 and 34 in its two coordinate-row geometries
but does not cover multi-site rows, non-coordinate blocks, or construct a
source at either threshold;
the final $p=19$ endpoint's
[independent audit](live-three-zero-higher-split-p19-c8-singleton-pair-line-clique-independent-audit.md)
rechecks every split, common-unit transport, dimension branch, grid degree,
and pole coefficient;
the uniform sole-plane layers $t=r+3,t=r+4,t=r+5$, together with the exact
closed sectors of the $t=r+6$ layer.  Each promoted statement has a
characteristic-zero or symbolic checker for its claimed parameter range.
Finite reconnaissance and the three dense-double sole-plane profiles
\(2^4 1^5,2^5 1^3,2^6 1\) remain labelled as frontiers rather than
closures.

[The mechanical registry checker](../computations/verify_route_registry_integrity.py)
verifies uniqueness of every top-level route identifier and checks every
linked local target and backticked artifact path.  It recomputes these
mechanical totals after every registry edit; it does not certify the many
mathematical census counts recorded elsewhere.  The
2026-07-28 replay passes with 21 unique top-level identifiers, 331 checked
Markdown links, and 114 checked backticked artifact paths.

The status labels that matter globally are still the `U1` warning.  The new
full-nine incidence and essential-star theorems supply uniform inputs—at
least \(N-8\) target-full internal sites per pair cap, at least
\(N(N-7)/2\) doubly aggregate-injective pairs for every even \(N\ge8\),
and a good clique of size at least \(\lceil N/5\rceil\)—but not the
aggregate-to-blockwise/Hessian conversion.  The mixed equations first
empty the regular nonbipartite branch, and the escape-chart plus four-port
theorems then empty defect one uniformly.  Therefore every good pair now
lies in exactly one of two live charts: an extra Hessian kernel direction
(E1), or at least two bipartite/isolated rank-three defects (E2).  The old
finite-port regular tables and induced-zero shores remain useful
historical reductions, but are no longer branches of the active descent.

Within the connected spanning nonbipartite E1 stratum, the independently
audited distinguished-span-two theorem now turns the dense equality case
into a zero-star triple and pure selector.  Its live residuals are sparse
deleted-star rows
or distinguished span at least three; E1 charts with disconnected,
nonspanning, or bipartite rank-three graphs remain separate.  Its exact
positive export is the full common-complement 27-equation system.  Within
E2, centered defect stability reduces a full fan to \(b(R-r)\ge2\),
\(\delta(R-r)\le2\), or
an E1 pair.  The four-cut exchange theorem shows that two overlapping E1
27-packets are one 81-row system and that selector-contracted caps alone
admit a repeated-pair filter; the uncontracted two-dark theorem proves that
filter cannot extend and forces two live diagonal colours in each star
pair.  One isotropic direct-block contraction further packages all nine
opposite rows into a common-power dressed cap, ternary off the scalar-unit
boundary and binary on it.  Its pure four-star contraction has sharp
consistency guards, so the full packet is essential.  The centered rank
tradeoff kills rank-two
E2 spokes with a rank-at-least-two second star, but exact rank-one survivors
remain.  For the explicit sharp survivor, the 27-row packet has no minimal
three-private-coordinate shared-star lift modulo `Ann(q)`, although its
common-`q` relaxation is exact; cancellation-rich, non-coordinate, and
higher-power lifts remain, but every such realization has two additional
singular spokes and at \(N=8\) has \(\deg_R(y)\le2\).  Other rank-one masks
remain.  Defect coordinates are
now faithful: defect two forces a sparse star row and, away from a
rank-three-degree-at-most-two vertex, can occupy at most nine charts of a
good fan.  The global sparse-center alternative is a synchronized nine-row
packet with an exact selected-row guard.  A dense defect-three chart spans
all three coordinates; the
shared-restriction relaxation fails one full overlap row by \(-6\).  The
active exports are therefore the E1 common-power dressed packet, the
finite-nine/low-degree E2 residual or full-overlap equations on its faithful
coordinates, and propagation of the sharp mask's singular spokes or a
classification of the other E2 rank-one masks.

The complete-bipartite family still explains why mixed GHZ vanishing was
essential: it satisfies the pure and common-quadratic relaxations but has
an explicit nonzero mixed residual, so it is not a target source.
Three or more literal zero sites and the general exceptional common-power
branch also remain open, although the full 45-dimensional pure six-site lift
branch is closed for arbitrary aggregate coefficients and multi-site rows,
as are the locally full-rank three-line-field resolution and the entire
incident-rank-at-most-two coordinate-plane boundary.  The conclusion of the
uniform reduction note remains conditional.  Several other routes contain
useful exact obstructions or countermodels, but none currently supplies the
missing all-even arrow.

### 4.1 Semantic route triage

The integrity checker certifies identifiers and paths, not mathematical
scope.  Reading the registry against the prompt gives the following shorter
dependency audit.

| Route cluster | Conjecture-level leverage | Concrete gate before more credit |
|---|---|---|
| `U1` with `S1/T1` | The only current cluster aimed directly at a uniform all-even-to-six implication; every good pair is E1 or E2, dense span-two E1 yields a zero-star selector and an exact 81-row overlap system, centered E2 stability plus the rank tradeoff removes rank-two spokes in the high-rank second-star regime, the sharp rank-one packet forces two additional singular spokes, and defect-two sparsity propagates to a finite-nine/low-degree fan residual | Exclude the synchronized E1 isotropic dressed-cap packet; close graph-degenerate, sparse-row, or span-at-least-three E1; propagate the two-singular-spoke equality stratum and classify other rank-one masks; consume the synchronized sparse-center packet or its finite-nine/low-degree alternative; or apply full overlap rows to the faithful defect-three coordinates. |
| `OC1/V1` | Can become uniform only through overlapping physical cuts with their shared aggregate factors | A fourth-cut invariant must survive the known two- and three-cut countermodels; isolated fixed-interior line closures do not suffice. |
| live-three-zero collision family | Contains genuine all-parameter incidence and Wronskian lemmas, but also a very large finite-order census | A new lemma must quantify over all split orders and collision profiles; another isolated \((p,h,k)\) row is reconnaissance rather than descent. |
| `K4C/PF1/T2` | Strong structural boundaries and sharp countermodels | Supply a theorem forcing an arbitrary hypothetical large source into the recorded boundary; without that bridge these remain local classifications. |
| `B1/X1/P1/NRM/N1` and restricted support routes | Valuable falsification and special-ansatz control | Reopen only with a new invariant that retains asymmetric endpoints, parallel aggregates, and arbitrary complex cancellation uniformly in \(n\). |

This triage no longer assigns primary proof value to another bounded pure
common-power profile: the full pure span is closed support-independently.
The next common-power target is the genuinely non-pure four-site component
outside the now-closed coherent-field charts.  One and two line fields are
excluded, and three line fields are excluded when all frames are full or
exactly one frame is deficient; the universal two-pair and 157-packet
theorems retain genuine hard-zero mixtures.  The remaining coherent
three-field cases have two through five deficient sites and at least one
full frame; the all-six-deficient case is already closed by the
coordinate-plane theorem.  Separately, arbitrary edge blocks with local
endpoint rank at most two are forced into the three coordinate-plane
omission-pair normal form, and the independently audited mixed-packet theorem
now excludes that form completely.  Thus the arbitrary-block escape requires
a site of incident rank at least three—full rank three after target-space
projection.  One- and two-site determinant propagation are exactly falsified.
At the sharp global rank budget, typed double quotients reduce to three
distinct omission-pair overlap geometries.  Independently audited
typed-grid and hole-block arguments close path, triangle, and
wedge-plus-disjoint; budget above twelve is not yet reduced to the equality
layer.  A uniform selection or cancellation theorem
is still needed; enumerating further pure multiplicity profiles
cannot close the prompt's all-even quantifier.

## 5. Evidence discipline

The following receive no closure credit unless lifted to a characteristic-
zero, parameter-uniform certificate:

- a Gröbner computation after fixing anchors or candidate values;
- absence of rational points over one finite field;
- generic full rank of a response matrix;
- a nonzero minor on one Zariski-open chart without exact treatment of its
  complement;
- a finite census at fixed $h$ or fixed common-pole order.

Finite-field row selection is acceptable only when every selected
determinant and the final unit ideal are reconstructed exactly over
$\mathbb Q$.  This distinction is respected by the accepted CBB, CCE, and
CCB/CBC/BCC cell certificates.  The former finite experiments on
$2^9 1^5$ received no proof credit;
that profile was later closed by uniform selected incidence.

## 6. Ranked concrete next steps

For a cap with boundary signature
\(C=C_0+C_2+C_4+C_6\) and \(s=C_0\), the first target can be tested
without logarithms.  Clearing denominators gives the homogeneous cubic
six-site tensor

\[
 {\cal D}(K)=
 6s^2(C_6+C_4x)-3sC_2^2x-C_2^3.                        \tag{2}
\]

Thus the direct cap condition is \({\cal D}(K)=0\), together with the
already controlled nonvanishing of the product cap.  A raw dimension count
on the cap space is insufficient: a cubic zero set can be a union of the
forbidden scalar/target hyperplanes, exactly as in the registered ternary
root-cover family.  Even one realizable common-edge cap subspace can have
that unit saturation.  The useful target is therefore a consequence of the
*full transverse cap equations* proving that this root cover cannot extend
simultaneously across the available flags.

The dependency-aware ranked short list is:

| Priority | Exact next deliverable | Why it can change the proof state |
|---:|---|---|
| 1 | Prove a uniform arbitrary-order theorem that some three-step product cap is clean, or that effective transverse/all-cap GHZ directions defeat every dirty-cap root cover; the recorded cancellation of six off-diagonal rows and two diagonal relocations is only the ten-site test case. | Height, top contraction, one realizable slice, and even a \(73\)-dimensional maximal GHZ-compatible cap slice admit the prism root cover because \(69\) directions lie in a common kernel.  A conjecture-level proof must change the effective lower cofactor family uniformly, not merely close that bounded prism. |
| 2 | On E1, exclude the ternary isotropic dressed-cap packet using its shared multiplier, six target-zero quadratics, and actual divided-power provenance; handle its scalar-matrix-unit binary boundary; in parallel close disconnected/nonspanning/bipartite graphs, sparse rows, or \(\dim D_{pq}\ge3\). | Three uncontracted rows exclude the repeated-pair \(K_4\) boundary, and one isotropic contraction now retains all nine opposite rows.  Exact guards show that its further pure four-star contraction is too weak, while no registered theorem consumes the synchronized dressed packet. |
| 3 | On E2, propagate the sharp witness's two-singular-spoke export through its higher-order equality stratum and classify the other rank-one masks; consume the synchronized sparse-center packet or finite-nine/low-degree defect-two residual; or apply full overlap rows to the faithful full-span defect-three coordinates. | Centered stability gives the global alternatives.  The rank tradeoff removes rank-two/high-second-star spokes; the sharp mask has two additional singular spokes with no support assumptions and gives \(\deg_R(y)\le2\) at \(N=8\); exact defect two occupies at most nine high-degree fan charts; and selected-row relaxations isolate the missing compatibility. |
| 4 | On the cubic branch, split \(P_c\ne0\), where common-star restriction is faithful, from \(P_c=0\), where the nine pure two-crossing Hessian equations and direct-block transpose compatibility must replace raw nullity. | The nullity web is uniform but conditional on the three-essential stratum.  Its remaining information is physical common-cofactor compatibility, not another kernel-dimension count. |
| 5 | Continue exact counterexample search on the unrestricted aggregate system \(H_8(A)=\Delta_{8,3}\), with lifting to finite decorated sources and independent exact certification. | A genuine exact point would disprove the conjecture; bounded support lower bounds and isolated polarized points cannot. |

The longer route-specific worklist below records the two active global
descent families and their exact frontier data.

1. **Extend the first uniform theorem across the six-kernel boundary.**
   The exact equality ledgers are \(50/50\) and \(94/94\), and the
   stationary-section mechanism has now been extracted uniformly: it closes
   four \(p=20\) one-quintuple families under the sharp conditions
   \(M_4=19\), \(4\le C\le7\), and
   \(P\ge\max(1,2C-9)\).  The next concrete targets are precisely its
   exposed gaps—\(C=6,P=2\), \(C=7,P\le4\), \(C\ge8\), and the
   unsaturated two-quartic branch \(M_4=20\)—together with a
   parameter-uniform version of the singleton-controlled quintic pair-line
   clique.  On the audited \(d\le2\) slice of the first six-kernel boundary
   \(p=28\), the \(3^{10}\) balanced-annihilator theorem and the
   \(4^2 3^7 1\) grid are now completed profile closures.  The two remaining
   core types require different mechanisms.  For \(4^3 3^6\), the common
   kernel is now proved six-dimensional and all six selections are
   \(q=5\); the developable and generic tangent-rank-one branches are
   closed, leaving exactly the primitive degree-six rank-two annihilator
   splittings \((2,4)\) and \((3,3)\).  Combine their
   row-degree \((2,4)\) or \((3,3)\) derivative matrices, whose determinant
   is the six moving-root polynomial, with the retained three quartic and
   six triple rows.  The opposite-sheet kernel orientation and the bare
   cubic-pair intersection have exact countermodels, so the concrete
   \((3,3)\) target is the finite system
   \(\operatorname{Wr}(F)=cT^3R^2\),
   \(\kappa(z^2)=c_1T(z)T(-z)\), together with the four- and five-jet
   minor divisibilities and all open guards.  For \(4^7 1\), add a
   second selection or an unreduced tensor equation: the audited
   pure-fifth-pole models prove that one-selection highest jets cannot
   suffice.  The first concrete second selection removes three selected
   singleton layers and inserts one quartic label; its residual must acquire
   the full cubic factor \((z-y)(z+y)^2\).  Either derive that divisibility
   by coupling several such cores to the pure-fifth-pole section, or build
   an exact compatible formal countermodel showing that this mechanism also
   stops.  Another isolated census is useful only if it exposes a
   parameter-uniform inequality.

2. **Advance the remaining additional-singular families in frontier order.**
   The minimal three-extra and two-extra responses and the first sole-plane
   high-$t$ layers $t=r+3$, $t=r+4$, and $t=r+5$ are complete.
   At the next sole-plane point $(7,13)$, the independently audited
   degree-78 Hilbert squeeze now closes \(2^3 1^7\), including its affine
   common-zero locus and both projective directions.  The remaining profiles
   are $2^4 1^5,2^5 1^3,2^6 1$.  Extend the cyclic-obstruction/Hilbert-squeeze
   construction to four, five, and six double pairs, while retaining the
   structural open factor and every projective chart.  Then continue to
   larger two-extra,
   larger three-extra, and nonrescue families.  The completed low-order templates do not by
   themselves close any larger-order response.

3. **Extract a genuinely uniform higher-order mechanism.**  Any successful
   continuation must either prove existence of a cap satisfying (1), retain
   and transport $L_4,L_6$, couple the forced nonzero high-crossing quotient
   maps across adjacent five-sets, or turn the live common-power collision
   lemmas into an all-$k$, all-$h$ theorem.  The audited eight-site
   polarized model shows that the isolated equation
   \(zq^3/3!=\Delta_{8,3}\) is consistent, so the cap route must retain the
   literal constraint \(z=aq+4ps\), at least two rows sharing the same
   stars, or overlapping adjugate identities from two physical pairs.  For
   the six-site monomial base locus, the actual common-power condition now
   excludes every missing-pair type permitted by all nine products even when
   the six response rows have arbitrary multi-site support.  More strongly,
   the independently audited private-pair projection closes the entire
   45-dimensional pure-lift span at once: literal responses select one
   private pair per colour, and a unital local algebra projection reduces to
   the distinct-missing-pair power obstruction.  The sharp repeated-pair
   \(K_4\) model explains why the products are essential, but no further pure
   multiplicity census is needed.  The concrete next common-power problem is
   non-pure.  Scalar cofactor rank is exactly falsified, while the
   independently audited response theorem excludes every one- or two-line-
   field resolution and aligns any full-rank three-field resolution with the
   three targets outside at most two sites per colour.  The sitewise
   filtration additionally forces a four-cover by the incident endpoint
   spaces and turns the local-rank-at-most-two boundary into three coordinate
   planes on three omission pairs.  The aligned full-rank three-field branch
   is now completely closed: Hall forces exactly two active physical pairs,
   the three support profiles are all impossible, and the exact power ideals
   were independently reconstructed.  At exactly one deficient site, the
   axial/bridge normal form, distinct-lift theorem, two-pair theorem, and
   157-case packet theorem now close the branch completely.  Move to exactly
   two deficient sites, but keep both bad-site tensor factors: the four-good-
   site field-only box condition is vacuous by pigeonhole.  In the
   arbitrary-block branch, the coordinate-plane packet is closed and exact
   countermodels rule out propagation from one or two scalarized sites.  Use
   the global rank budget instead: the independently audited typed-grid and
   hole-block theorems now close all three equality geometries, so control
   budget strictly above twelve without asserting an individual cofactor is
   nonzero.  For
   its nine-cell \(q\), the fixed-\(q\) theorem additionally excludes the
   entire affine target preimage, so a sparse countermodel search must
   change \(q\) itself rather than only its polarized factor \(z\).  The
   weighted three-term exhaustion closes every same-colour flagged-matching
   support of that form.  The one-cell invisible-direction theorem further
   closes all 99 individual endpoint-ordered additions which preserve the
   displayed polarized identity.  The invisible full-block theorem further
   closes an arbitrary endpoint-colour block on any one of the eleven
   physical pairs.  The exhaustive two-cell theorem further closes every
   deformation by two new cells and proves that two visible debts never
   cancel.  The exact three-cell theorem now closes every genuinely new
   visible-debt cancellation family among three added cells.  The compatible
   three-cell theorem closes the separate 87,027 identically compatible
   triples: projective parity leaves 742 multi-pair systems, and both full
   exact batches reduce all 742 to unit ideals.  The next sparse advance must
   therefore use at least four new cells, vary \(z\), or move to a larger
   shared-block family.  The
   universal cofactor
   annihilator rules out the former hope that one five-cut has a successful
   one-crossing kernel inclusion.  The two audited adjacent countermodels
   rule out both kernel-only overlap and any implication based solely on two
   complete high-sector quotient maps, even with a target-active summed lift.
   The exact twelve-source countermodel rules out the bare three-cut
   shared-cylinder condition, and its two-source repair rules out adding one
   selected mixed equation.  The fixed-background one-star theorem excludes
   both tests when only site 6 or only site 7 is changed.  The exact
   two-star model transports every recorded debt, while the independently
   audited cylinder/Segre theorem proves that even both arbitrary stars
   cannot activate a fourth cut on that fixed interior.  The audited
   two-cell and five-cell theorems exclude the first controlled internal
   families.  The independently audited arbitrary-block theorem now closes
   all 512 supports of
   \(A_{23}\in\operatorname{Mat}_{3\times3}(\mathbb C)\) on that same fixed
   six-site interior, including its one cross-ratio modulus.  Consequently,
   another one-block support refinement cannot advance this model.  The first
   adjacent second-block line \(A_{25}=E_{00}+tE_{11}\) is also now closed.
   Four independently audited extensions close the directions
   \(01,02,12,21\) as well, and the independently audited full-cylinder
   theorem closes \(22\).  The next finite extension must attack one of
   the two remaining directions \(10,20\), a two-dimensional affine
   slice in \(A_{25}\), or an internal edge disjoint from 23 where genuine
   mixed \(Xt\) terms appear, always retaining the diagonal
   targets, both shared boundary stars, and complete cut annihilators;
   alternatively it must replace the fixed interior altogether.  Beyond
   that, the viable tests are a
   permutation-stable whole mixed
   sector, or a genuinely global fourth-cut invariant.  Each must retain the
   shared aggregate factors and complete annihilators.  A further negative
   answer must again be an exact
   arbitrary-complex countermodel, not a discrete one-factor scan.
   Extending the census one order at a time is useful falsification work but
   cannot be the final uniform proof.

4. **Assemble and independently audit only after the middle arrow closes.**
   The final paper must combine aggregation, the elementary lower bounds,
   the partition-rank four-site proof, the six-site theorem, and the new
   uniform descent.  It then needs separate graph/perfect-matching and
   algebra/tensor line audits against every mandatory quantifier in the
   prompt.

The immediate high-payoff work is therefore: first, prove the direct
cap-selection or conditional cap-span-saturation theorem; second, extract it
as a genuine elimination consequence of the full nine shared-pair ideal and
its exchange charts, without double-counting a second complete pair slice;
third, build the alternate four-or-more-cut invariant with all high sectors
and mixed coefficients retained; fourth, require every two-defect,
rank-budget, or collision continuation to export one of those uniform
invariants; and fifth, run unrestricted exact \(n=8\) searches only to find a
fully liftable source.  The decic paired-osculating and undecic tangent
branches are closed and should be used as templates, not listed as open
targets.  The decisive global milestone remains an unconditional all-even
descent, not another finite-order census.
