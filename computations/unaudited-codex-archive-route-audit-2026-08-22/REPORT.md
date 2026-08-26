# Archive route audit

Status date: 2026-08-22.  This report audits and deduplicates the existing
repository.  It introduces no new mathematical claim and runs no new solver.

## 1. Corpus and authority

The working tree contains 2,265 files under `notes/`, 183 lane `REPORT.md`
files under `computations/unaudited-*`, 28 proof files, and 16 certification
files.  These are not one flat body of equally current claims.

Two working-exact reports landed after the first archive census and are
incorporated below.  They do not change certification or close the
conjecture, but they supersede the older `728 blocked` and zero-tail task
wording:

- normalized full `X5` automatically gives a diagonal blocker for every one
  of the 168 star carriers, so the nontrivial finite-carrier residual has 560
  triangle clauses;
- if `J` is the ideal of all 168 cross-colour source cells, the certified
  block-diagonal theorem implies `I5+J=(1)`.  Thus an exact normalized `X5`
  point cannot have zero tail; the entire hypothetical fibre is the remote
  locus.

The source-level reports are the [five-set star reduction](../unaudited-codex-star-five-set-blocker-reduction-2026-08-22/REPORT.md)
and [full-tail entry audit](../unaudited-codex-full-tail-entry-incidence-2026-08-22/REPORT.md).

The authority order is:

1. `certification/BASELINE.md` and accepted records in
   `certification/SUPERSESSIONS.md`;
2. later audited proof files explicitly named by those records;
3. the 2026-08-21 handoff and the 91-addendum master plan as a historical
   campaign ledger, including its withdrawals and corrections;
4. `unaudited-codex-*` reports and old route notes as research evidence,
   exact computational lemmas, counterguards, or proposed dependencies—not
   certified spine merely because their local replay passes.

This distinction is load-bearing.  The chronological route registry warns
that its old `open` labels are not assignments.  The master plan retracts
earlier headlines inside the same file.  The later proof-spine review is an
append-only synthesis whose top-level corrections supersede some priority
lists retained farther down the document.

## 2. Stable core

The certified core still consists of:

- exact six-site impossibility for arbitrary complex endpoint-ordered
  `3 x 3` blocks (`SP-K6`);
- exact clean-pair descent (`SP-DESCENT`);
- a selected physical curvature/cap line (`SP-CURVATURE`);
- a long sequence of certified local refinements of the rootless and
  all-inactive boundary;
- the independently audited block-diagonal eight-site theorem and its slice
  machinery in the later supersession records.

The certified global missing arrow remains `SP-CLEAN-BRIDGE`: turn the
selected physical line, or an equivalent full-source structure, into an
active clean point.  Later Codex language `X5-to-cap` is a scope-correct
restatement for the complete eight-site mixed system, not a proof of that
arrow.

For the file-by-file authority hashes, certification conflicts, and the
current 14-route spine, see the companion
[current-route audit](../unaudited-codex-current-route-archive-audit-2026-08-22/REPORT.md).

## 3. Deduplicated route ledger

The status words below have deliberately narrow meanings.

- **Certified** means accepted by the certification ledger.
- **Exact local** means a source-labelled rational/characteristic-zero or
  symbolic result, but only on the displayed chart, filtration, or support
  stratum.
- **Bounded** means the stated finite shell was exhausted; it is not a
  statement about larger shells.
- **Support only** means a necessary Boolean or singleton condition was
  tested.  `SAT` in this column is not a graph realization and `UNSAT` is a
  coefficient theorem only when every coefficient cancellation has first
  been represented soundly.
- A finite-field `UNIT`, an RUR at one or two primes, a timeout, or a
  zero-byte solver output is discovery evidence unless an exact
  characteristic-zero replay is separately named.

### 3.1 Matching triples and the 31 charts

| Mechanism | Strongest surviving result | Status and exact scope guard | Authoritative files | Retired “next” |
|---|---|---|---|---|
| Matching-triple census | There are exactly **31** orbits of triples of perfect matchings under `S8 x S3` (and 8 at six sites). | Exact finite census.  The old 57 count used only `S8 x S2`. | [reconciled orbit count](../../notes/matching-triple-orbit-counts-reconciled.md), [31-orbit audit](../unaudited-codex-three-copy-31-rank-audit-2026-08-22/REPORT.md) | Do not reopen the 57-orbit enumeration. |
| Rank/rainbow refinement | All 31 eight-site orbits, and all 8 six-site controls, remain SAT in the support abstraction; exact diagonal realizations have nonzero `Phi` but singleton mixed terms. | **Support only / negative guard.** It proves the proposed rank-aware SAT refinement cannot distinguish exact sources. | [31-rank audit](../unaudited-codex-three-copy-31-rank-audit-2026-08-22/REPORT.md), [full-support SAT notebook](../../notes/n8-full-support-sat.md) | “Add rank and rerun SAT” is superseded. |
| No-fourth-matching shell | For the 12 triple orbits with no fourth physical matching, every one-cell and two-cell completion is excluded; the two-cell interface has 868 cases in 182 symmetry orbits. | **Exact bounded shell.** Additions of three or more cells, coefficient cancellations in arbitrary completions, and identification of a full-source witness remain outside it. | [first-shell report](../unaudited-codex-three-copy-first-shell-2026-08-22/REPORT.md) | Do not describe the 12 charts as closed. |
| Exchange-complex completion | The quadratic exchange complex rederives the bounded first shell.  A dense completion (`B=I+J` on every edge) has the required rank but no singleton, so no completion-independent singleton/cocycle/Farkas potential exists. | Exact counterguard to a **support-only** global completion argument.  It does not decide the coefficient fibre. | [exchange-complex report](../unaudited-codex-three-copy-exchange-complex-2026-08-22/REPORT.md) | Arbitrary-completion singleton certificates are retired; the residual is coefficient-sensitive fat-fibre analysis. |

**Deduplicated verdict.**  The 31-chart outer cover is classified, and its
first completion shell is closed.  The cover itself is not coefficient
closed.  None of the SAT statements supplies an exact GHZ source or an
emptiness certificate.

### 3.2 `D1`, singleton/support closures, and the phase-base `m=7` lane

| Mechanism | Strongest surviving result | Status and exact scope guard | Authoritative files | Retired “next” |
|---|---|---|---|---|
| `D1`, low off-support size | `m <= 6` is ideal-theoretically closed; `m=7` has 22 exact support-RUP closures; `m=8` has 165 and `m=9` has 1,071 unit-refuted support branches. | Exact on the named `D1` normal form and shells.  It is not a chart-wide statement for arbitrary off-support size. | [minimal ideal closure](../../notes/n8-d1-minimal-off-sigma-ideal-closure.md), [m7 closure](../../notes/n8-d1-m7-support-shadow-closure.md), [m8](../../notes/n8-d1-m8-support-shadow-closure.md), [m9](../../notes/n8-d1-m9-support-shadow-closure.md) | The older m7 timeout/frontier note is superseded by the m7 closure. |
| `D1`, `m=10,11` | All `m=10` symbolic branches and all 285 `m=11` branches (296,766 complete supports) are closed; the exceptional coefficient cases reduce to finitely many exact binomial contradictions. | Exact over characteristic not two, within the frozen `D1` support/normal-form hypotheses.  No implication for `m >= 12` or other charts. | [m10 full closure](../../notes/n8-d1-m10-334-full-closure.md), [m11 full closure](../../notes/n8-d1-m11-full-closure.md) | The old m10 “frontier” and branch-63 candidate are superseded. |
| Phase `K4 disjoint-union K4`, binary jets | All jets with first pure order `<6` are excluded and the `m=6` valuation partitions are exhausted.  At `m=7`, seven of eight primitive packets have bounded, exact `Q(omega)` unit closures. | Exact only for the binary, phase-base completed-local problem and the enumerated valuation/support packets.  It is not the general two-`K4` singular-block theorem below, nor an arbitrary multicolour Puiseux theorem. | [balanced-base/Luna report](../unaudited-codex-balanced-base-oddset-luna-2026-08-21/REPORT.md) | “m6 is the first survivor” and “all eight m7 packets are closed” are both retired. |
| Final primitive `1222-k4` | Lazy gain/toric CEGAR accumulated 4,055 sound guarded circuit cuts.  The final complete support solve is **SAT** and minimizes from 308 to **84 live atoms**, with 1,143 active mixed rows and 7 pure-order-seven terms. | **Support feasible, coefficient unresolved.** Earlier returned supports had exact constant-failure circuits, but the final 84-atom target has not had an exact toric/coefficient replay.  The complete gain SMT timed out; there is no finite circuit-basis or convergence theorem. | [phase-base report](../unaudited-codex-balanced-base-oddset-luna-2026-08-21/REPORT.md), [final support result](../unaudited-codex-balanced-base-oddset-luna-2026-08-21/results_phase_m7_1222_k4_cegar_batch4055_final.json), [unreplayed coefficient target](../unaudited-codex-balanced-base-oddset-luna-2026-08-21/results_phase_m7_1222_k4_cegar_final4055_coefficient_target.json) | Neither `SAT` nor 4,055 learned cuts closes the primitive.  One-cut CEGAR and the 478-MB complete-gain encoding are archived, not active proof steps. |

### 3.3 `K14/K16`, orbit zero, and the two-`K4` structural chain

| Mechanism | Strongest surviving result | Status and exact scope guard | Authoritative files | Retired “next” |
|---|---|---|---|---|
| Orbit-zero `K14` | The chart-local containment `a*T` in the mixed ideal plus `K^16` is source-replayed. | **Exact local**, on the frozen orbit-zero chart and multiplier.  It is not a collected `K16` remainder and not a 31-chart/global result. | [K14 interface audit](../unaudited-codex-orbit0-k14-interface-audit-2026-08-21/REPORT.md), [graded orbit-zero report](../unaudited-codex-n8-orbit0-t2-graded-2026-08-20/REPORT.md) | Do not promote `K14` containment directly to global radical membership. |
| `K16` chart transport | The projected tail has 50 provisional orbit types and an exact affine-cover lower bound of **25 necessary types**.  The literal minimum-25 packet contains 2,467,680 occurrences / 2,052,084 rows; 2,345,240 occurrences have no chart, the rest reach all 31 charts, and 6,810 are self-transitions of chart 1.  No strict chart potential exists. | Exact combinatorial/provenance audit, but the `K16` polynomial is **not collected** and no residual membership is proved. | [K16 transition audit](../unaudited-codex-k16-chart-transition-audit-2026-08-21/REPORT.md) | A 20-orbit singleton certificate is impossible.  The only honest continuations require new source columns/lower-filtration transfers or a proof of compression of the necessary 25 types. |
| Two-`K4` singular-block chain | The exact 0-through-9 singular strata are excluded.  The last nine-block `K3,3` residual is closed by the nonzero/one-zero/two-zero star kernels.  Therefore every solution in this model has at least **10 singular cross blocks**. | Exact symbolic theorem for the frozen two-`K4` composition/dead-slab model.  It is not an arbitrary eight-site theorem and does not exclude the strata with 10 or more singular blocks. | [route registry summary](../../notes/route-registry.md), [exact-nine audit](../../notes/two-k4-exact-nine-independent-audit.md), [two-zero closure](../../notes/two-k4-k33-two-zero-independent-closure.md) | “Finish the exact-nine residual” is superseded.  “The two-`K4` model is impossible” overstates the result. |

### 3.4 Six-site rank graphs

| Mechanism | Strongest surviving result | Status and exact scope guard | Authoritative files | Retired “next” |
|---|---|---|---|---|
| Six-site rank graph | Arbitrary complex endpoint-ordered `3 x 3` aggregate blocks on six sites are impossible.  The exact census uses the graph of blocks with rank not equal to one, maximum degree two, and all-zero versus rank-at-least-two semantics. | **Certified (`SP-K6`)**.  Arbitrary phases are included. | [certification baseline](../../certification/BASELINE.md), [assembly audit](../../notes/six-site-rank-graph-assembly-audit.md), [certified proof](../../proofs/six-site-arbitrary-complex-obstruction.md) | The lack of a compact all-35-clause DRUP is certificate engineering, not an open mathematical branch. |
| Cap-positive pullback | Chartwise Hermitian identities and localizer supports are exact, but they cannot be commonized and pulled back to a single eight-site source; the hostile mutation kills the attempted extension. | Exact negative route audit.  It neither weakens `SP-K6` nor supplies `SP-CLEAN-BRIDGE`. | [N6 pullback report](../unaudited-codex-n6-cap-positive-pullback-2026-08-22/REPORT.md) | Do not reopen local norm identities without a source-commonization lemma. |

### 3.5 Tail response, zero tail, carriers, and clean-cap descent

| Mechanism | Strongest surviving result | Status and exact scope guard | Authoritative files | Retired “next” |
|---|---|---|---|---|
| Carrier response | The 168 star and 560 triangle carriers give 728 finite sufficient tests, each with four blocker memberships.  On normalized full `X5`, the universal five-set annihilator automatically places one diagonal blocker in every star row space, leaving only the 560 triangle clauses nontrivial. `W40` has six active stars only because it is an `X4` control. | Working-exact finite surrogate.  The 560 residual tests still do **not** define all clean caps, and their simultaneous failure is weaker than global no-cap. | [response-star report](../unaudited-codex-response-star-2026-08-20/REPORT.md), [five-set star reduction](../unaudited-codex-star-five-set-blocker-reduction-2026-08-22/REPORT.md) | “Prove all 728 blocked” is superseded by “prove `X5` plus all 560 triangles blocked is impossible”; neither is the definition of the global no-cap locus. |
| Tail initial matrix | For every frozen tail pair, the literal `380 x 12` matrix (8 `7+1`, 12 `6+1+1`, 360 `3+3+2`) has rank 12 at zero tail.  The `6+1+1` determinant is the product of 12 diagonal Hafnian cofactors; the frozen response Hessian has determinant `-64` on support six (orientation-paired determinant `4096`).  Alternative minors cover all 126 missing-pattern opens. | Exact source labels, signs, `B4` covariance, and **associated-graded/Jacobian-at-zero-tail** theorem.  Only the 12 selected columns are eliminated; the global tail has 168 entries, and the rank is not a first-Jacobian lower bound for the full source quotient. | [tail-polar report](../unaudited-codex-tail-polar-source-lift-2026-08-21/REPORT.md) | The four remaining support-factor divisors are not the only global obstruction. |
| X5-to-tail interface | The 380 rows are literal members of the complete mixed system `X5`; 360 of them have off-count five. | Exact row-label/count correspondence and a **conditional** X5-to-cap implication.  Only 20 rows lie in `X4`; hence the stronger X4-to-cap use was unsound. | [X5 bridge report](../unaudited-codex-x5-tail-cap-bridge-2026-08-21/REPORT.md) | `X4-to-cap` is archived as an optional target requiring a new derivation. |
| Filtered lifting | The full tail equations have degrees through four. Initial full rank gives formal/local implicit elimination of selected columns, not literal zero tail. The full-tail audit now proves `I5+J=(1)`, so an exact zero-tail factor is empty and the remote locus is the entire hypothetical fibre. | Exact obstruction plus working-exact entry theorem. A route that proves `J=0` on the exact quotient would already prove the whole conjecture; it is not an intermediate lift. | [filtered-lift obstruction](../unaudited-codex-tail-filtered-lift-obstruction-2026-08-21/REPORT.md), [full-tail entry](../unaudited-codex-full-tail-entry-incidence-2026-08-22/REPORT.md) | The old task “enter zero tail and then lift” has the direction reversed. |
| Zero-tail packet | At zero tail there are 1,638 nontrivial diagonal rows, and the recorded 310 support-minimal strata are coefficient-closed. Independently and more globally, the certified block-diagonal theorem implies `I5+J=(1)`, excluding every exact normalized zero-tail point without a support-minimal degeneration. | The 310-orbit result remains exact only for its packet, but it is no longer needed to exclude zero tail inside the full exact `X5` fibre. It does not by itself prove the full-tail ideal identity. | [zero-tail assembly](../unaudited-codex-x5-zero-tail-assembly-2026-08-21/REPORT.md), [routing report](../unaudited-codex-x5-zero-tail-routing-2026-08-21/REPORT.md), [full-tail entry](../unaudited-codex-full-tail-entry-incidence-2026-08-22/REPORT.md) | “310/310 closes zero tail” remains an invalid description of that packet; exact-fibre zero-tail exclusion now comes from the certified diagonal theorem instead. |
| Idempotent/remote branch | The literal 168 `6+1+1` equations give `J=J^2` on the full cofactor open, while `I5+J=(1)` gives `JA=A` on the exact quotient. Hence every hypothetical exact point is remote. | This is entry and direction control, not a contradiction. The former fixed-star 355-variable core is tautological because every exact `X5` star is already diagonally blocked; the genuine finite linear incidence remainder is triangle-only. | [remote-idempotent report](../unaudited-codex-tail-idempotent-remote-2026-08-21/REPORT.md), [full-tail entry](../unaudited-codex-full-tail-entry-incidence-2026-08-22/REPORT.md), [five-set star reduction](../unaudited-codex-star-five-set-blocker-reduction-2026-08-22/REPORT.md) | The old fixed-star remote solve and connectedness route are retired. A direct remote contradiction or triangle/cancellation-clean cap remains. |
| Clean-cap descent | Once an active clean point exists, the certified descent reaches the six-site contradiction. | **Certified (`SP-DESCENT`) conditional on activity.**  The missing source-faithful production of that point is still `SP-CLEAN-BRIDGE`. | [certification baseline](../../certification/BASELINE.md), [proof-spine review](../unaudited-codex-proof-spine-review-2026-08-21/REPORT.md) | Tail rank plus all finite blockers does not by itself prove the bridge. |

### 3.6 Branch and localizer Groebner artifacts

| Branch library | Strongest exact conclusion | Scope guard / current state | Authoritative files |
|---|---|---|---|
| Triangle-pendant, `P26` split | Both `P26=0` on its frozen `F0 != 0` chart and `P26 != 0` after localizing the complete audited Cramer/live product have exact characteristic-zero `[-1]:` replays in standard, `-O`, and `-I -S` modes. | **Exact local closure** of the declared triangle-pendant stratum.  Its denominator factors are part of the antecedent; this does not close unrelated charts. | [boundary report](../unaudited-codex-tp-p26-boundary-char0-2026-08-21/REPORT.md), [interior report](../unaudited-codex-tp-p26-interior-char0-2026-08-21/REPORT.md) |
| `K4`-cycle/cofactor charts | Several named leaves, including the frozen `h=d1^2*x-1` cofactor-13 branch and a separate exact `Cof33`, `Delta=0` subtree, are characteristic-zero closed. | **Partial chart library.** Modular RUR components disappear when omitted cofactor rows are restored; two-prime units are not characteristic-zero proofs.  Generic open/localizer leaves and the whole `K4`-cycle chart are not thereby closed. | [cofactor-13 exact report](../unaudited-codex-k4-cycle-cofactor13-exact-2026-08-21/REPORT.md), [RUR referee](../unaudited-codex-k4-cycle-char0-rur-referee-2026-08-21/REPORT.md), [living dangerous-chart ledger](../unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/REPORT.md) |
| Face `0:31:30` | The `A`-open/R25 and `A=B=0` interfaces, pivots, omitted rows and localizers are source-frozen.  A later exact arbitrary-mate certificate closes the whole positive-dimensional `A=B=0` component. | **Partly open.** The `A`-open core/slice gates timed out and make no algebraic claim.  The earlier timed-out full `A=B` gate is not itself a closure, but its component was subsequently closed by a different mate argument. | [structural split](../unaudited-codex-face03130-structural-2026-08-21/REPORT.md), [A-open report](../unaudited-codex-face03130-aopen-char0-2026-08-21/REPORT.md), [`A=B=0` gate report](../unaudited-codex-face03130-A0B0-char0-2026-08-21/REPORT.md), [later exact closure](../unaudited-codex-proof-spine-review-2026-08-21/REPORT.md) |
| Face `0:31:15` | Exact fraction-free `R=0` split and source interfaces for `J=0`, `J!=0`, and `d2=1` are frozen. | **Open.** Their terminal characteristic-zero gates timed out; zero-byte outputs and finite-field leads are explicitly non-results. | [R-branch split](../unaudited-codex-face03115-R-branch-2026-08-21/REPORT.md), [J0](../unaudited-codex-face03115-R-J0-char0-2026-08-21/REPORT.md), [J-open](../unaudited-codex-face03115-R-Jopen-char0-2026-08-21/REPORT.md), [`d2=1`](../unaudited-codex-face03115-d2eq1-char0-2026-08-21/REPORT.md) |
| Face `0:63:31` | The structural `Delta` split and exact source export are frozen. | **Open.** The `Delta=0` characteristic-zero gate timed out at 600 seconds and the `Delta`-open report is structural only. | [structural report](../unaudited-codex-face06331-structural-2026-08-21/REPORT.md), [Delta-open](../unaudited-codex-face06331-deltaopen-structural-2026-08-21/REPORT.md), [Delta-zero timeout](../unaudited-codex-face06331-delta0-char0-2026-08-21/REPORT.md) |

These branch libraries are reusable exact interfaces, but they do not add
up to a global proof.  In particular, `F4SAT`/modular `UNIT` output is a
core-discovery device; exact source replay, the complete localizer product,
and an expanded Rabinowitsch sentinel are required before a leaf is called
closed.

### 3.7 Conceptual/theory routes after deduplication

The separate [conceptual route audit](../unaudited-codex-theory-route-archive-audit-2026-08-22/REPORT.md)
checks 38 live file links and groups the archive into nine mechanisms that
were repeatedly renamed:

| Renamed family | Archive verdict | Only version not already counterguarded |
|---|---|---|
| Wick / zeon / squarefree Artinian / bosonic Gaussian / apolar tower | Lower-sector identities are exact; top-output differentiation is not a fibre equation. | A relative source-labelled `(q,q^2,q^3,q^4)` identity coupled to X5 and a carrier. |
| Brauer / partition algebra / matching association scheme / equivariant syzygies | These are projections of the same perfect-matching module; nontrivial sectors are unconstrained kernels. | A nonlinear response/reinsertion map retaining source labels. |
| PEPS virtual `Z3` / Fourier pull-through / Fourier uncertainty | Sitewise Fourier covariance is exact, but it does not pull through individual edges; proper blocks are not injective. | A new source-relative kernel-lifting theorem, not a standard PEPS theorem. |
| Minimal MPS / automata / Hankel / connection matrices | The three-state GHZ quotient is exact but erases literal edges and reachable-unobservable states. | A radical-to-intersecting-block lifting lemma. |
| GIT / Kempf--Ness / scaling / capacity / moment polytope / Brascamp--Lieb | All reduce to port balance unless the mixed equations are added; balanced controls refute a bare moment conclusion. | No standalone moment-map route remains. |
| Minimum norm / ED / conormal / singular vectors | Exact block normality and attainment survive; regular KKT, trace/SOS, and first-Jacobian shortcuts do not force a cap. | The singular normal cone/local ideal, or a genuinely mixed nonlinear consequence. |
| Carrier rigidity / response matroid / stress / tail stiffness | Each linear matroid is exact but loses the shared source coupling. | A joint X5 carrier-tail algebraic matroid or word-degree-at-least-three conormal. |
| CP / Segre / secant / flattening | Target rank-three structure does not colocate channels on a physical edge. | A matching-compatible two-site secant/circuit theorem. |
| Alternating rainbow / fourth matching / support exchange | The 31 geometries and first shell are exact; a dense completion kills every support-only extension. | A coefficient-valued matching exchange/gain complex. |

Two further broad ideas remain logically untested but presently lack a small
interface: a degree-controlled global six-site Nullstellensatz certificate
compatible with block normality, and a source-labelled Rees exceptional-
fibre theorem.  Ordinary Pfaffian/Pluecker, phase-hyperfield, invariant-SDP,
and valuation-support versions have explicit archived counterguards.

### 3.8 Older named backstops

The [legacy/backstop audit](../unaudited-codex-theory-route-archive-audit-2026-08-22/LEGACY-BACKSTOPS.md)
classifies the route-registry families without treating their historical
`open` labels as assignments:

- `A1`, `S1`, and the selection/descent outputs of `U1`, `E1/E2`, pair-fan,
  and multi-pair incidence are absorbed by certified curvature, descent, and
  six-site results.
- `C1`, `B1`, and `D1` are retired as standalone global programmes.  Their
  exact restricted lemmas remain useful controls.
- `OC1`, `K4C`, `PF1`, and `T2` retain only special-chart residuals; each
  lacks an arbitrary-source entry theorem.
- The zero-shore construction is retired although its conditional
  common-power identity remains exact.  **Zero shore is not zero tail.**
- The E1/E2 overlap complex and source-level multi-pair incidence remain
  possible structural backstops, but neither has the transport needed for
  X5, minimum norm, or the tail theorem.

## 4. Stale or misleading route labels

The following should not be used as current assignments without reading
their later corrections:

- every `open` label in `notes/route-registry.md`;
- the old statement that the certified block-diagonal machine also closes
  `N=10`: the accepted supersession certifies only `N=8` for that machine;
  separate `D1` recurrence notes concern a narrower diagonal model and are
  not a certified uniform theorem;
- the old `D1` m7 SAT-frontier and m10 branch-candidate labels, superseded by
  the later exact m7 and full m10 closures;
- the inference that seven closed phase-base `m=7` packets close the eighth:
  `1222-k4` still has the unreplayed 84-atom coefficient target;
- pre-v12 phase-only/GIT conclusions in the master plan;
- pre-v34 and pre-v85 claims that the m=25 or m=28 delivery mechanisms close
  their intended global branch;
- the v58 `310/310` m19 headline, withdrawn at v61 to `267/310`;
- `X4-to-cap` as consumer of the 380-row tail theorem: 360 of those rows have
  off-count five, so the literal consumer is `X5`;
- the claim that closing four tail support divisors completes the global
  lift: the filtered equations allow remote idempotent components;
- any implication from the 310 minimal zero-tail support orbits to the whole
  zero-tail component without a support-minimal degeneration theorem;
- the common-matching source `A_01=A_23=A_45=A_67=I3` as an exact GHZ point:
  literal replay gives 78 mixed outputs;
- early `A=B=0` headings asking for an arbitrary mate: a later exact mate
  certificate closes that component, although the separate `A`-open face
  remains unresolved;
- 728 finite carrier blockers as the definition of no clean cap: they are a
  sound finite surrogate, strictly weaker than the full statement; on full
  `X5` the 168 star clauses are automatic, so only 560 triangle clauses are
  nontrivial;
- tail associated-graded rank or carrier Hessian rank as a first-Jacobian
  lower bound;
- the old wrong-cleared-Delta degree-11 component/RUR and its purported
  literal `H` values; the corrected identity is `DeltaN=C8*D10` and places
  that component on the excluded actual-Delta boundary;
- exponent-one orbit-zero membership such as `H0 H1 H2 in I_mix`; the valid
  archived statement is localized and powered, currently modulo `K^16`;
- “enumerate 20 `K16` orbits”: the exact cover lower bound is 25;
- any whole-chart conclusion from a modular `UNIT`, a one/two-prime RUR,
  a timeout, or a locally closed Groebner leaf.

## 5. Current genuine residuals

After deduplication there is one certified global gap, three current attack
interfaces, and a lower tier of local libraries.

### Global statement

The current working proof spine is exactly

```text
hypothetical exact N=8 source
  -> full X5 system
  -> if any carrier is active: certified descent -> certified N6 contradiction
  -> all 168 star carriers are automatically blocked on X5
  -> otherwise all 560 triangle carriers are blocked
```

Thus the smallest current finite-carrier implication is `X5 + all 560
triangle carriers blocked => contradiction`.  The original 728 tests remain
a finite sufficient-support cover, not the definition of every projective
clean cap; wider cancellation-clean caps are not represented by this
triangle-only statement.

### Three current interfaces

1. a nonlinear/Hermitian consequence of attained exact-fibre minimum norm,
   using the full mixed equations and the 560 triangle clauses, including the
   reduced singular normal-cone branch;
2. a direct contradiction on the remote full-tail locus, or a same-source
   triangle/cancellation-clean cap theorem. Full-tail entry is now solved;
   forcing the tail ideal to zero would already be the whole conjecture;
3. a collected, literal-provenance `K16` residual or a new localized
   compression theorem beyond the necessary 25 projected types.

### Independent conceptual hypotheses worth retaining

The audit found four other broad hypotheses with no decisive archive
counterexample: coefficient-valued matching exchange/gain; relative
source-labelled apolar/HPL; matching-compatible two-site secants; and a
source-labelled Rees exceptional-fibre theorem.  They are ideas for proving
one of the interfaces above, not additional established arrows.

### Local residuals only

- coefficient replay of the phase-base `m=7` `1222-k4` 84-atom target;
- the two-`K4` strata with at least ten singular cross blocks;
- `0:31:30` (`A`-open only), `0:31:15`, `0:63:31`, and the generic corrected
  `K4`-cycle/cofactor remainder;
- special-chart OC1/K4C/PF1/T2 and E1/E2 overlap packets.

Closing any local residual alone does not prove the global statement without
an audited source transport.

## 6. Audit rule for future work

Before reopening an idea, require a five-field record:

`mechanism / strongest exact result / decisive counterguard / precise
remaining hypothesis / authority level`.

Search labels, numerical success, SAT feasibility, finite-field discovery,
or a locally unit ideal do not update the global spine without the missing
source transport and an accepted audit.

The interrupted directory
`unaudited-codex-orbit0-k16-literal-collection-2026-08-22` contains only a
working script and no report or result file. It is not an archive result and
must not be cited as one.
