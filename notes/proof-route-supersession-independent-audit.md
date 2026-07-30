# Independent audit of the proof-route supersession map

Audit date: 2026-07-29.

## Final disposition

**PASS after revision.**  The main map now incorporates every scope correction
identified below: the anchored program is sufficient rather than exhaustive;
the pure-lift, coordinate-plane, and coherent-field closures retain their
six-site packet scope; E1/E2, OC1/V1, and uniform collision routes are demoted
but not mathematically subsumed; and both anchored components must be uniform
in the residual degree.  I found no remaining substantive misclassification.

## Findings on the initial draft

The main compression in
[the supersession draft](proof-route-supersession-audit.md) is correct at
the level of the shortest proof spine: after passing to a minimum-entry-
support aggregate representative, curvature-line selection is proved, and
an active clean point would feed the proved exact descent.  The one missing
conjecture-level implication on that spine is therefore

\[
 \text{generically active physical cap line}
 \Longrightarrow
 \text{active clean point}.
\]

The audit initially found four overstatements.  The revised draft now
incorporates all four corrections.

1. The proposed diagonal-anchored two-chart program is a candidate
   sufficient proof of the missing implication, not a proved exhaustive
   decomposition of it into two necessary lemmas.  In particular the
   rootless and inactive-root packets still have different audited local
   forms.
2. The uniform pure-lift and coordinate-plane theorems are six-site
   common-power theorems.  They do not retire similarly named higher-order,
   E2, endpoint-star, or collision packets.
3. Unconditional curvature selection retires the globally flat branch as a
   **selection task**.  It does not mathematically subsume the structural
   E1/E2, OC1/V1, cubic-packet, or collision routes; those are demoted
   independent backstops.
4. The newest independent Hall/one-anchor audit validates the negative
   guards but corrects the claimed two-anchor threshold: two anchors give
   partial axis alignment only.  A crossed target-zero row is invariant
   under the surviving relative torus and is not, by itself, a scale-fixing
   equation.  Faithful overlap injectivity is still an unproved extra input.

With those changes, the revised draft is a sound strategic dependency and
task-allocation map.  Its focused anchored program remains a proposed
sufficient proof, so “authoritative” should describe route allocation rather
than promote that program to a proved theorem-level reduction.

## Evidence basis and chronology

The recent committed sequence supports the narrower reading.  Commit
`9ffb0c2` made curvature selection unconditional and explicitly moved the
cubic-packet, E2, and zero-shore programs to independent-backstop status.
Commits `89b1f49` and `a23a241` then split the remaining curved arrow into
rootless and inactive-root physical packets.  Commit `8011bb1` closed the
rank-at-most-one exceptional shore, `fb52702` isolated rather than solved the
anchored selector obstruction, and `e983ba7` proved the residual gcd/rank
identity while leaving physical annihilator construction open.  None of
those commits proves the proposed anchored overlap injectivity theorem.

In the present working tree, the changes to
[the current proof audit](current-proof-audit-and-next-steps.md),
[the attack board](parallel-proof-attack-board.md), and
[the route registry](route-registry.md) only add backlinks declaring the
supersession draft authoritative; they do not add an independent theorem or
semantic proof-state argument.  Those self-references are therefore not
independent evidence.  The theorem notes and the later uncommitted
Hall/one-anchor audit supply the substantive evidence for the revised
classifications; the latter narrows rather than strengthens the two-anchor
claim.

## Status convention

This audit uses the four requested categories componentwise.  A route can
legitimately receive more than one label when one of its proposed
implications has been guarded while a strengthened version remains viable.

* **A — positively superseded:** a stronger proved theorem already supplies
  the output for which the old task was being pursued.
* **B — negatively superseded:** an exact guard disproves the old implication
  at its stated hypothesis level.
* **C — demoted but independent:** it is no longer on the shortest spine,
  but no theorem subsumes it and it could still bypass the open arrow.
* **D — current:** it is either the open arrow itself or an unresolved,
  correctly scoped subproblem in a presently live attack on that arrow.

## Claim-by-claim classification

| Route or historical task | Status | Audited conclusion |
|---|---|---|
| Global curved/flat selection | **A** | [Unconditional curvature-line selection](unconditional-curvature-line-selection.md) proves that every hypothetical exact source has a **minimum-entry-support aggregate representative** with a nonzero physical transition minor and a generically active canonical cap line.  This retires further good-fan, low-degree flat-fan, cubic-core, and port-merging work whose sole purpose is to find a nonzero transition.  It does not say that every redundant presentation is curved and it does not find a clean point. |
| The cubic-centre packet route after flat selection | **C** | The flat branch is no longer a required alternative, but the faithful-Hessian/pure-packet theorems remain valid independent contradictions for a source which happens to have a cubic centre.  The curvature theorem does not subsume their conclusions. |
| Strong cap cleaning, separate pairification of higher cumulants, or forcing \(r^2=0\) | **A/B** | [Exact clean-pair descent](clean-pair-cap-exact-descent-target.md) gives the necessary-and-sufficient homogeneous top-support error \({\cal E}_{p,q}(K)\).  It positively supersedes stronger sufficient targets such as \(r^2=0\).  Exact dirty-cap guards negatively supersede the assertion that activity or an arbitrary cap implies cleanliness.  Existence of an active zero of \({\cal E}\) is **D**. |
| Rank-zero/rank-one exceptional endpoint shore in a rootless full-nine packet | **A** | [The uniform full-nine shore theorem](full-nine-type3-annihilator-plane-closure.md) proves \(\operatorname{rank}P_{\bar x},\operatorname{rank}S_{\bar x}\ge2\) for injective endpoint stars.  For \(h\ge3\), response nonnilpotence excludes endpoint support on at most two sites, so both stars have three-site selectors.  This conclusion requires all nine literal rows, global endpoint injectivity, and rootless nonnilpotence for the support step. |
| Rank-two shores and selector-union defects | **D** | [The rank-two shore theorem](full-nine-rank-two-shore-coordinate-support.md) only routes the common-exceptional-site case to a zero/unary/binary \(q^{[h]}\) or disjoint fixed-label kernel supports.  It does not close those alternatives.  It also does not cover the audited coloop-free deficient flat, so it does not imply the selector-matroid union inequalities. |
| Residual Macaulay algebra | **A** | [Residual rank equals gcd degree](residual-macaulay-quotient-is-the-common-divisor.md) proves \(\operatorname{rank}\mu_{f,L'}=h-\deg\gcd(f,L')\).  The algebraic meaning of a rank defect is finished. |
| Uniform physical Macaulay annihilator/lift | **D** | Producing a nonzero covector annihilating the residual image from literal source coefficients remains open.  It is already equivalent to producing a common root, so it is not an easier generic-rank surrogate.  Calling the whole “uniform Macaulay lift” positively superseded would be wrong; only its abstract algebra is finished. |
| Hall permanent \(\Rightarrow\) disjoint/separated selector bases | **B** | [The selector/Hall guard](selector-hall-base-packing-and-block-jacobian-guard.md) and its [independent audit](selector-hall-and-one-anchor-threshold-independent-audit.md) show that the exact condition is the full matroid-union inequality.  The coloop-free deficient-flat packet has a nonzero selected-word permanent but violates that inequality.  This packet is only one selected word, not a full tensor solution. |
| Separated selectors/Hall data \(\Rightarrow\) an own-edge lift | **B** | The complete-graph torus guard grants fixed-label shore separation, six off-diagonal tensor rows, all target-zero mixed scalar rows, and a nonzero permanent, yet every own-edge Jacobian column is obstructed by a four-cycle covector.  It misses exactly the three diagonal target tensors.  Own-edge transversality remains **D** only after adding a literal diagonal coefficient cut or a coefficient-dark bypass. |
| Selector exposure \(\Rightarrow\) raw Macaulay rank loss | **B** | [The selector double-jet theorem](selector-macaulay-double-jet-and-offdiagonal-hexagon.md) proves that every full minor meets exposed columns, but scalar-zero nonnilpotence automatically fills that jet.  The six off-diagonal rows have only the cubic hexagon, not a fixed-label rectangle.  The residual quotient \(Q_f\), rather than the raw exposed jet, is the current ledger. |
| One diagonal anchor \(\Rightarrow\) residual rank loss | **B** | The audited seven-row packet has all six off-diagonal rows, the complete \(X_0\) row, same-colour shore-separated selectors, and a literal four-cut \(X_0\) coefficient, while the residual map still has full rank three.  It misses \(X_1,X_2\). |
| Two anchors plus a crossed zero row are already sufficient | **Not proved; D as a proposed strengthened target** | Two transported labels align two distinct coordinate axes, but a relative diagonal torus survives.  The crossed zero target remains zero under that torus.  Moreover the four-index row \((r,r;s,s)\) used in the coefficient-dark lemma is not literally the endpoint cell \(E_{rs}\) in the flag calculation.  Only an additional source-provenant overlap map proved injective on the relevant correction module could turn this packet into a Macaulay annihilator.  “Smallest plausible input” is defensible; “minimal” or “sufficient” is not. |
| Diagonal rows alone or off-diagonal rows alone close the two-chart \(\Omega\) pencil | **B** | The independently audited complementary guards in [the two-chart note](curved-two-chart-offdiagonal-anchor-complementarity.md) show both failures.  Three diagonal rows can coexist with bad \(\Omega\) columns when the six off-diagonal rows fail; six off-diagonal rows, two-chart provenance, curvature, clean endpoints, and good stars can coexist with the bad strata when diagonal anchors fail.  The stronger off-diagonal guard retains \(X_0\) and \(q^{[2]}\ne0\) but misses \(X_1,X_2\).  It does not include the missing physical binary target rows.  Mixing both kinds of rows before top degree remains **D**. |
| Pure multiplicity/profile enumeration in the six-site common-power packet | **A, with narrow scope** | [The uniform pure-lift theorem](uniform-pure-lift-private-edge-degeneration.md) closes the entire 45-dimensional span \(F=\sum_{c,P}\lambda_{cP}E_c(P)\) on a six-set, assuming all nine responses, \(q^{[2]}=F\), and \(q^{[3]}=0\).  It allows arbitrary aggregate coefficients, repeated supports, cancellation, multi-site rows, and arbitrary endpoint-ordered blocks of \(q\).  It does **not** close non-pure four-site tensors, residual degree \(h>3\), E1 higher-power packets, or unrelated pure collision profiles. |
| Coordinate-plane boundary of the six-site sitewise filtration | **A, with narrow scope** | [The coordinate-plane mixed-packet theorem](coordinate-plane-mixed-packet-obstruction.md) closes the case in which every **internal quadratic incident space** \(W_u\) has dimension at most two, for a six-site system with \(F=q^{[2]}\) and all nine responses.  It allows arbitrary plane blocks and does not need \(q^{[3]}=0\).  It does not concern ranks of the endpoint-star maps \(P,S\), the full-nine rank-two-shore theorem, E2 rank-two response blocks, higher residual sizes, or the rank-budget-above-twelve branch.  Those similarly named coordinate-plane problems are not superseded. |
| One/two line fields, full three-field frames, exactly one deficient frame, and all-six-deficient coordinate planes | **A within the six-site common-power program** | The cited coherent-field and sole-defect theorems close precisely these strata.  Two through five deficient sites with at least one full frame, arbitrary non-line-field multipliers, and rank budget above twelve remain open.  The coherent-field family is therefore **C/D**, not globally closed. |
| E1/E2 good-pair fan classification | **A for selection; C for structural descent** | Once the unconditional curvature theorem supplies an active physical line, no global E1/E2 classification is needed merely to select a line.  However the E1 faithful-Hessian/dressed-packet and E2 plane/hole/inactive-core residuals are not consequences of curvature selection.  They remain independent ways to force a clean cap, sparse selector, or source contradiction.  The selected curved pair is itself a good physical pair, so its E1/E2 structure can still be used. |
| OC1/V1 short-cut implications | **B for the guarded versions; C for the route families** | Universal one-cut annihilation and exact two-/bare-three-cut countermodels rule out the advertised short implications.  They do not rule out a four-cut, full mixed-sector, shared-aggregate-factor invariant.  OC1 and V1 can still bypass the cap-line proof and are not mathematically subsumed by the proposed anchored overlap lemma. |
| Live-three-zero collision work | **A for each proved finite/uniform subfamily; C overall** | The many exact profile closures remain theorems.  Another isolated fixed \((p,h,k)\) cell does not settle the all-even quantifier, so the census is demoted in task allocation.  A genuine all-split/all-collision invariant could still provide a uniform contradiction or descent and has not been subsumed by curvature selection. |
| Generic-hafnian/top apolar lift from one mixed word | **B** | [The Shafiei apolar audit](shafiei-generic-hafnian-apolar-lift-obstruction.md) shows that the homogenized degree-three apolar membership is exactly the original scalar tangent equation and carries no extra support information.  A selected mixed-word packet can satisfy all nine scalar proportionalities, nonnilpotence, apolarity, and a Hall permanent. |
| Full all-word/full-nine cohafnian route | **C/D** | Cross-word compatibility, fixed pure anchors, and literal lower-degree source lifts are absent from the apolar guard.  A coupled full-nine cohafnian argument remains a viable independent proof of the open line-closure arrow.  The pure/binary response and common-power guards show that neither factorization nor the common-power row, even together in a contracted packet, replaces the other eight physical rows. |
| Exact counterexample search | **D as an independent disproof route** | No exact decorated lift satisfying every colouring coefficient has been found.  Bounded repairs, polarized identities, and partial cap packets close only their stated search families.  Unrestricted exact \(H_8(A)=\Delta_{8,3}\) search remains logically independent; only a finite exact aggregate point with a checkable decorated lift would disprove the conjecture. |

## Corrections audited in the revised draft

### 1. The open arrow has not been proved equivalent to two anchored lemmas

The earlier draft presented “anchored-chart extraction” and “anchored
overlap injectivity” as if they were the two remaining proof obligations.
The revision correctly calls them one well-motivated sufficient program.  The
[proposed overlap--jet lemma](adjacent-literature-and-anchored-overlap-jet-lemma.md)
explicitly labels itself unproved and assumes the full-nine rows, selectors,
the overlap connection, curvature, and complementary rows.  No cited theorem
derives all of those hypotheses from the selected line in one common chart,
nor proves that failure of this particular chart forces a clean point by
another argument.

Both candidate components must ultimately be uniform in (h).  The
degree-(h) Macaulay quotient makes that dependence especially visible in
the second component, but the current base-packing, one-anchor, and own-edge
guards are six-site (h=3) packets.  A positive first component still needs
either a uniform selector-incidence theorem on (2h) residual sites or a
proved reduction to six selected sites which faithfully retains the
remaining common power.  Uniformity cannot yet be assigned only to the
second component.

The branch distinction should remain visible:

* in the **rootless** branch, the residual Macaulay map is surjective and
  the task is to construct an annihilator from physical coefficients;
* in the **inactive-root** branch, exact roots already exist, but they export
  lower-colour or nilpotent packets, and the two-chart task is to rule out
  simultaneous independent/exactly-one-zero \(\Omega\) pairs.

An anchored overlap theorem could close both, but that unification is the
statement to be proved, not an audited reduction already in hand.

There is also a label case that the draft should not suppress.
[Unconditional selection](unconditional-curvature-line-selection.md) gives
\(K_z=E_{ab}+zI\) without proving \(a\ne b\).  The clean off-diagonal
scalar-zero packet

\[
 r_*q^{[h-1]}=-\alpha\Delta_{2h,3},\qquad r_*^{[h]}\ne0
\]

and the apolar--Hall theorem assume \(a\ne b\).  For \(a=b\),
[the rootless-line theorem](curved-rootless-line-uniform-response-resultant.md)
has a separate ternary/binary scalar-zero split, with a potentially singular
binary boundary.  Any universal “rootless packet” statement must include
that diagonal case or prove a new off-diagonal selection lemma.

### 2. Pure-lift and coordinate-plane scope must be frozen

Revised Section 4.4 now says “the six-site 45-dimensional pure
\(q^{[2]}\) lift span is closed,” rather than declaring all pure
common-power profile enumeration finished.  The theorem uses a six-set and
\(q^{[3]}=0\).
Finite pure enumerations inside exactly that packet are obsolete; higher-
degree and differently sourced pure packets are not.

Revised Section 4.5 likewise says “the six-site
internal-incident-rank-at-most-two boundary is closed.”  Its \(W_u\)'s are
the endpoint spans of the internal
quadratic blocks, not the endpoint-star shore ranks and not E2 response-block
ranks.  The sentence “any arbitrary block escape must contain an incident
rank-three site” is valid only inside that six-site nine-response system.

### 3. The newest Hall/one-anchor audit changes the wording

The earlier Sections 5.1 and 5.4 said that the dedicated audits were still
awaited.  The revision now cites the
[combined independent audit](selector-hall-and-one-anchor-threshold-independent-audit.md),
which gives the following exact ledger.

* The deficient-flat guard is only a realization of one selected mixed word.
* The torus/Jacobian guard satisfies the six off-diagonal tensor rows and all
  target-zero mixed scalar rows, but misses all three diagonal tensors.
* The one-anchor guard satisfies seven tensor rows and misses \(X_1,X_2\).
* The coefficient-dark Lemma 7.1 is a valid conditional full-nine
  contradiction, but its kernel, star-product, target-incidence, and direct-
  coefficient hypotheses are not consequences of Hall or selectors.
* Two anchors prove partial flag alignment only.  The crossed zero row does
  not itself remove relative torus drift, and the relevant four-index row is
  not the crossed endpoint matrix unit used in the flag calculation.

The revision accordingly replaces “the smallest surviving input is two
anchors plus their crossed zero row” by the defensible candidate of two
anchors plus a source-faithful crossed/overlap coefficient equation.

### 4. E1/E2, OC1/V1, and collision work is demoted, not subsumed

Revised Sections 6 and 7 correctly remove these routes from the shortest
task list while distinguishing that allocation decision from mathematical
retirement.

* E1/E2 work whose only goal was to select a nonzero transition is
  positively superseded.  The remaining E1/E2 packet theorems are
  independent backstops.
* The exact OC1/V1 guards retire one-, two-, and bare three-cut implications,
  not the full multi-cut route.  A fourth-cut/full-mixed-sector invariant
  could bypass line closure entirely.
* Fixed collision censuses are low-priority after unconditional selection,
  but a uniform collision theorem is still independent.  “Retired from the
  main line” is a task-allocation statement, not theorem-level supersession.

The same caution applies to broad registry labels such as `S1/T1`: some of
their theorems, notably target flattening and good-pair selection, are inputs
to the proved curvature theorem, while their residual E1/E2 programs are
backstops.  The whole route identifiers should not receive one blanket
supersession label.

## Correct status of the seven recently listed angles

| Listed angle | Correct audited status |
|---|---|
| Diagonal-forced incidence | **D.** A live candidate for obtaining selector base packing, fixed-label transport, or a coefficient-dark bypass.  It has not been proved to follow from the full-nine rows. |
| Own-edge transversality | **B/D.** Hall-, selector-, and ordinary-Jacobian-only versions are exactly guarded.  A diagonal-anchored physical column-membership theorem remains viable, but is one possible implementation rather than a separate conjecture-level obligation. |
| Anchored overlap injectivity | **D.** This is a proposed sufficient theorem.  Diagonal/off-diagonal complementarity shows why both row types are needed; no injectivity or \(H^1\) identification has been proved. |
| Uniform Macaulay lift | **A/D.** The gcd/rank algebra is complete.  Uniform source-provenant construction of an annihilator remains open and is already equivalent to the common-root conclusion. |
| Direct apolar/cohafnian route | **B/C.** The generic-hafnian one-word/top-apolar lift is retired.  A cross-word, full-nine, source-relative cohafnian argument remains independent. |
| Global E1/E2 fan route | **A/C.** Its selection role is superseded by unconditional curvature.  Its physical packet/overlap residuals remain independent and are not mathematically subsumed. |
| Exact counterexample search | **D, independent disproof.** No full exact lift is known; restricted negative searches do not supersede the unrestricted problem. |

Thus there is one open implication on the shortest affirmative spine, but
it is not yet justified to count exactly two mathematical proof obligations
or to identify all backstops as merely different languages for those two.

## Concise final dependency spine

The proved trunk is

\[
\begin{aligned}
 H_B(A)=\Delta_{B,3},\quad |B|\ge8
 &\Longrightarrow
 \text{choose a minimum-entry-support aggregate representative}\tag{proved}\\
 &\Longrightarrow
 \text{a nonzero physical minor and a generically active cap line}\tag{proved}\\
 &\dashrightarrow
 \text{an active zero of }{\cal E}_{p,q}\text{ on some physical line}\tag{open}\\
 &\Longrightarrow
 H_{B\setminus\{p,q\}}(A')=\Delta_{B\setminus\{p,q\},3}\tag{proved}\\
 &\Longrightarrow
 \text{six-site contradiction after repeated descent}.\tag{proved}
\end{aligned}
\]

The open arrow currently has two audited branch ledgers, not two proved
lemmas.

1. **No common root:** the Sylvester/Macaulay map is full rank; at scalar
   zero there is a nonnilpotent physical response.  Full-nine rows remove
   rank-at-most-one shores and give endpoint selectors.  What remains is a
   full-nine source-provenant failure of residual Macaulay surjectivity,
   with common rank-two and coloop-free selector defects treated explicitly.
2. **Only inactive common roots:** each root exports a lower-colour source
   or a nilpotent response packet.  The two-chart polarization leaves the
   bad \(\Omega\) alternatives.  What remains is a full transverse
   overlap/curvature theorem excluding those alternatives on both charts.

Diagonal anchoring plus faithful overlap is the most focused attempt to
close both ledgers.  E1/E2 packets, full-nine cohafnian coupling, OC1/V1
multi-cut invariants, a genuinely uniform collision theorem, and exact
counterexample search remain independent alternatives rather than already
superseded work.
