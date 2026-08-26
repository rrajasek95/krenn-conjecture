# Current-route archive audit

Date: 2026-08-22  
Status: archive audit only; no new symbolic, SAT, Groebner, or theory experiment  
Purpose: deduplicate the current proof routes and separate certified facts from later working artifacts.

Post-census correction: later working-exact source replays prove that full
normalized `X5` automatically blocks all 168 star carriers and that the full
zero-tail ideal is excluded by the certified block-diagonal theorem.  The
nontrivial finite-carrier residual is therefore the 560 triangle clauses,
and every hypothetical exact point is on the remote full-tail locus.  These
working artifacts do not change the certification status.

## Inputs and authority

The following files were read in full.

| input | SHA-256 |
|---|---|
| `certification/BASELINE.md` | `2b3a966a7873a58569e1f4ae0d94d4f32c7139da4bcdaef2cef4bddb254b7f24` |
| `certification/SUPERSESSIONS.md` | `07ac9f0f8b92d991a7cac7a5b2d8f15fae5db44914a4166b21bdde0fba926a3c` |
| `notes/route-registry.md` | `762338a618244dba346d87a49e502f5053a80f5be7aef2d787691d4d03c49465` |
| `notes/consolidated-proof-frontier.md` | `ab5157fe32bd8ea930eebf0aca410d117520e4357f225815b96d677c562bb04e` |
| `notes/parallel-proof-attack-board.md` | `ddde4b567cec924bea964903d9003e1cf3173a8ea64c5bd772f52ea517c249a4` |
| `notes/proof-route-supersession-audit.md` | `adc00d83326b3ae9728077ebe1c5c5c8c6201f74cb13937a345d1f233754ff71` |
| `computations/unaudited-codex-proof-spine-review-2026-08-21/REPORT.md` | `7d7ebd367823cf1c1cbe7243391158f5a8249615b4a5f5fc339fb0209743fdb8` |

Authority is not chronological prose. The certification baseline is changed only by accepted entries in `certification/SUPERSESSIONS.md`. The notes and the August 21 proof-spine report are working syntheses; their exact computations can be useful, but they do not silently promote a theorem. In particular, the registry itself warns that old `open` and `next` labels are historical.

The certified theorem state remains:

1. the exact arbitrary-complex six-site obstruction `SP-K6` is certified;
2. an active clean cap at eight sites gives the certified descent to six sites;
3. the eight-site block-diagonal obstruction is certified;
4. `SLICE-MASTER` supplies certified identities and a rank bound, not protection closure;
5. corrected `ROUTE-A-RESIDUAL` statements are conditional delivery lemmas, not an unconditional closure;
6. the full eight-site conjecture remains open.

## Deduplicated current-route ledger

`Certified` below means recorded in the certification ledger. `Working exact` means source-replayed or exact in the August 21 working archive but not promoted by certification. `Counterguard` means the archived reason a tempting stronger inference is invalid.

| route / mechanism | strongest exact result now | terminal counterguard | exact remaining arrow | stale old `open/next` wording? |
|---|---|---|---|---|
| **1. Clean-cap descent and six-site base** | **Certified.** `SP-K6` excludes an exact six-site source over arbitrary complex weights. An active clean cap at eight sites descends source-faithfully to that forbidden six-site instance. | This is a conditional descent theorem; it does not itself manufacture an active cap. | Prove that an exact eight-site point has an active clean cap; within the finite carrier surrogate, rule out `X5 + all 560 triangle carriers blocked`. | **Partly.** The theorem is current. Wording that the old active-line-to-clean-line program is the sole allocation is stale; the current interface is the full `X5`/carrier problem. |
| **2. Full `X5` to active cap** | **Working exact.** `X5` is the full 6,558 mixed-row system plus three pure normalizations. The original cover has 168 star and 560 triangle carriers, but the universal five-set annihilator automatically gives a diagonal blocker for every star on normalized `X5`. | `X4` omits 360 off-count-five rows, so W40's active stars remain a valid truncated control. The 560 triangle clauses are still only a sufficient-support surrogate and omit wider cancellation-clean caps. | Establish `X5 + 560 triangle blockers => contradiction`, or manufacture a cancellation-clean cap. | **Yes.** `X4-to-cap` and `728 blocked` are both stale current targets. |
| **3. Tail entry and remote locus** | **Working exact.** The fixed-tail response has associated-graded rank 12, and the full literal 168 `6+1+1` rows give `J=J^2` on the cofactor open. More importantly, the certified block-diagonal theorem implies `I5+J=(1)`: exact normalized zero tail is empty. | The archived `t=t^2` examples remain valid guards against naive local lifting. Since `JA=A` on a hypothetical exact quotient, the entire possible fibre is remote; forcing `J=0` would already prove the whole conjecture. | Contradict the remote locus directly, or obtain a same-source triangle/cancellation-clean cap. | **Yes.** Carrier-to-tail entry is solved; “enter zero tail and lift back” has the direction reversed. |
| **4. Zero-tail diagonal packet** | **Working exact.** The full 1,638 nontrivial `e=t=0` rows and 310 support-minimal records remain exact in their stated packet. Separately, `I5+J=(1)` now excludes the entire exact normalized zero-tail fibre by invoking the certified block-diagonal theorem. | The 310 packet alone still does not cover arbitrary larger support or coefficient cancellation; it is not the proof of global zero-tail emptiness. | Use the packet only as a boundary library. Exact-fibre work must attack the remote locus, not seek a support-minimal zero-tail degeneration. | **Yes.** The old proof-spine summary was unsupported by its 310-orbit argument, but the later full-tail ideal argument establishes the conclusion from a different authority chain. |
| **5. Remote idempotent tail component** | **Working exact.** Fixed-tail symmetry is transitive; a representative reduces to a 355-variable/405-equation exact target. One propagation step gives `y0 h2_06` equal to one of 90 quadratic monomials. | The broad residual is not computationally small, and connectedness, minimal-automaton, and graph-quotient shortcuts erase source-labelled null states. The idempotent control is a literal obstruction to local nilpotence arguments. | Classify the finite source-labelled propagation cycles and add coefficient no-goods, or obtain an exact saturation of the reduced component. | **Yes.** “Use connectedness to kill the remote component” is terminally false; source-labelled propagation/saturation is the remaining route. |
| **6. Exact-fibre minimum norm / normal cone** | **Working exact.** A hypothetical exact fibre is closed and has a norm minimum. Stationarity gives torus balance and regularity-free block normality. A rank-free Hermitian Gram formulation encodes the 560 remaining triangle disjunctions, while the singular branch must use the reduced limiting conormal rather than raw Fritz--John. | Equivariance gives `rank(J)-s <= 231`; boundary pullbacks and carrier `rho` terms are not first-Jacobian rows. The raw `alpha=0` multiplier is tautological because the mixed left cokernel has dimension at least 6306. | Find a nonlinear/Hermitian identity coupling full mixed rows, triangle incidence and the reduced normal cone, or a stratum-safe negative second variation. | **Yes.** Raw global-Jacobian rank, carrier-as-Jacobian and redundant Fritz--John branches are retired. |
| **7. Orbit-zero filtered algebra, `K^14` to `K^16`** | **Working exact.** The archived promotion is `a*T in I_mix + K^16`; 838,080 relative `K^14` products are killed with a three-mode source/mutation replay. | Exponent-one membership `H0 H1 H2 in I_mix` is false. The next finite cover has a 25-orbit minimum beyond the bounded expansion cap. Projecting to 25 signatures loses nonanchor labels, and one projected signature has incompatible literal completions. | Preserve literal provenance and find a new symmetry/source-labelled compression of the `K^16` residual, or a lower-kernel transfer proving the needed localized power membership. | **Yes.** Expanding the 25 projected objects, or applying a cofactor/minimum-norm argument to them as if literal, is invalid. The target must remain localized/powered. |
| **8. Diagonal chart and arbitrary-mate boundary library** | **Certified/working mix.** The block-diagonal `N=8` obstruction is certified. Working exact artifacts close the `k4` triangle-pendant case, several cycle boundaries, the `A=B=0` positive-dimensional component by arbitrary-mate closure, and support-six/eight one-colour components by mate closure. | These are chart or boundary statements. They neither lift a general bicoloured source to a diagonal source nor globally close all tail strata. A nonempty one-colour component is not an exact counterexample when a mate is forced. | Use these results as literal no-goods/boundary closures inside a proved `X5` tail lift. | **Yes.** “Finish the diagonal census and the full theorem follows” is scope inflation without the lift. The `A=B=0` mate question is already closed, despite older headings calling it open. |
| **9. Corrected generic `k4` cycle chart** | **Working exact.** The true cleared localizer is `DeltaN=b0*A*b1*d3-B*d1*d4=C8*D10`. The prior degree-11 sliced factors are on the actual `Delta=0` boundary. The `C8` boundary and the `D10/K4/K5` boundary-control pieces are recorded. | The earlier exporter used the wrong cleared Delta. Its claimed live degree-11 component, RUR interpretation, and literal `H` replay are invalid on the corrected chart. Leafwise `D10` factor enumeration grows without addressing the unsaturated theorem target. | Prove an exact radical/resultant identity, such as `(C8*D10)^e` in the retained necessary ideal, preferably by a joint PRS/subresultant compression. | **Yes.** The old degree-11 live-component and `H` tasks are invalid, not merely unfinished. |
| **10. `k5/k6` face library** | **Working exact.** Several structural splits of the `0:31:15`, `0:31:30`, and `0:63:31` faces are frozen, and the P26 boundary/interior task is done. | Direct large gates and naive pivots time out or inflate without a component sentinel; these are boundary controls, not a global partition of the exact fibre. | Use representation changes and sparse combinations on named residual components; then route any surviving face into the tail/cap bridge. | **Partly.** P26-labelled `open` wording is stale. Remaining named residuals are real but demoted below the global bridge. |
| **11. Original active-line / anchored-overlap program** | **Certified/working mix.** The clean-cap descent and earlier curvature/selection machinery remain valid in their recorded scopes. The archive contains exact source-labelled overlap and anchor identities. | Hall selectors, one-anchor and top-apolar shortcuts, bare Bianchi, target-free packets, and ordinary-polynomial/Tate inventories all have explicit hostile controls or grading defects. | If reused, construct the missing source-labelled derived comparison/relative cap morphism rather than another target-free selector. | **Yes as a priority claim.** Statements that this is the “only” or “sole primary” conjecture-level arrow predate the August 21 `X5`/minimum-norm spine. They are historical, not current allocation. |
| **12. Border geometry, invariants, torus/GIT, and graph parameters** | **Working exact.** GHZ lies in the Zariski closure of the unrestricted top Wick image. A source-cycle invariant separates a known boundary source while vanishing on an exact fibre. Four-qubit invariant tuples diagnose recurring chart components. | Output-only invariants do not distinguish exact from border membership. Torus degeneration does not preserve the locally closed no-cap condition at rank drop. Quiver stability, base-locus classification, and connection/minimal-automaton shortcuts do not retain the necessary source data. Equality of four-qubit quotient invariants is not an orbit/source-chart equivalence. | Only a source-relative exact-vs-border identity tied to the source ideal, or a locally proved covariant transport, would reopen this route. | **Yes.** General invariant/GIT shortcuts are terminally negative as global bridges; local invariants remain diagnostics only. |
| **13. Hybrid support/SAT architecture** | **Certified/working mix.** The 31 pure-matching triples form a finite outer cover; exact coefficient identities close the recorded 310 zero-tail minimal supports. | The base CNF is satisfiable on every `N=8` branch and on solved `N=6` controls. Support data alone cannot see cancellation or chart denominators. | Use lazy SAT only to route literal supports, adding theorem-grade antecedents and exact coefficient no-goods; it cannot be the proof by itself. | **Yes.** Any wording that support SAT alone closes the conjecture is false. The hybrid implementation idea is still current. |
| **14. Certified `SLICE-MASTER` and corrected `ROUTE-A-RESIDUAL`** | **Certified.** The slice identities/rank bound and the corrected Route-A conditional delivery lemmas are available exactly under their listed hypotheses. | The ledger records failure of the W30-X `GL_3` claim, the `H`/cover gate, unary `R6`, and an omitted side condition, along with finite-characteristic/corpus limits. Neither entry certifies unconditional protection. | Enter only through the explicit certified hypotheses and prove the missing hypothesis in the current source chart. | **Yes.** Old unconditional W30/W36 protection or delivery claims are superseded; only the corrected conditional disjunctions survive. |

## Contradictions and scope inflation

### 1. The archived `N=10` diagonal claim contradicts certification

`notes/consolidated-proof-frontier.md` says the diagonal obstruction is closed for both `N=8` and `N=10`. Accepted supersession `SUPERSESSION-2026-08-20-01` explicitly withdraws the uniform-even-`N` claim, certifies only the block-diagonal `N=8` theorem, and leaves `N>=10` open for that machine. The `N=10` sentence is stale and must not be cited.

### 2. “Only/sole remaining arrow” is chronologically stale

The parallel board and the July supersession audit describe active-line-to-clean-line or the unified anchored overlap as the only conjecture-level arrow. The August 21 proof spine refactored the same obstruction into full `X5` plus 728 blocked carriers; the later five-set audit further reduces the nontrivial clauses to 560 triangles. The older formulation is not logically contradicted, but “only” and “sole primary allocation” are no longer accurate project-management claims.

### 3. The proof-spine report has an internal tail chronology conflict

An early section says four support-factor tail orbits remain. A later section records exact closure of all four, while the final priority list again asks to classify the four remaining orbits. The final priority item is stale. At the time, the real remainder was entry/order/lifting and the remote component; the later full-tail audit solves entry and shows the remote locus is the entire possible exact fibre.

### 4. The proof-spine report has stale `A=B=0` wording

Early wording and a heading still ask whether the positive-dimensional `A=B=0` component has a mate. The later replay records arbitrary-mate closure of the whole component. The early “open `H`” wording is stale.

### 5. “Zero-tail is empty” overstates the exact packet result

The proof-spine summary calls the zero-tail factor empty, but its detailed section closes only the 310 frozen minimal-support records. That inference is invalid inside the proof-spine report. A later independent argument now proves exact-fibre zero-tail emptiness from `I5+J=(1)` and the certified block-diagonal theorem; it must be cited instead.

### 6. `X4-to-cap` omits literal source equations

The older `X4` target excludes the 360 profile-`(3,3,2)` fixed-tail rows. Only `X5` equals the full mixed system at `N=8`. Any inference from W25 or another `X3/X4` all-blocked control to the exact fibre is scope inflation.

### 7. The wrong Delta invalidates, rather than merely weakens, prior chart conclusions

The corrected identity `DeltaN=C8*D10` places the old degree-11 sliced factors on the excluded actual-Delta boundary. Old descriptions of a live generic component, its RUR, or literal `H` values cannot remain in a current route ledger.

### 8. Block-diagonal and chartwise closure are not a full diagonal-to-source theorem

Certification covers the block-diagonal `N=8` theorem. Later chart and mate results are useful boundary controls. Neither proves that an arbitrary exact source is block diagonal or that a general `X5` tail specializes to a closed diagonal chart.

### 9. Certified machinery has repeatedly been promoted beyond its hypotheses in prose

`SLICE-MASTER` certifies identities and a rank bound, not protection. `ROUTE-A-RESIDUAL` certifies corrected conditional delivery lemmas, not an unconditional branch closure. The supersession ledger's explicit withdrawals control over older narrative claims.

### 10. Quotient/invariant data are repeatedly mistaken for source equivalence

Four-qubit invariant equality is quotient data, not proof of an orbit or source-chart transition. Likewise, the 25 projected `K^16` signatures discard nonanchor provenance, and the 1,638 boundary pullback rows and carrier `rho` blocks are not first-Jacobian rows. Conclusions requiring the discarded labels or a Jacobian minor are invalid.

### 11. Exact-fibre minimization must not be conflated with approximate energy gaps

Attainment of a norm minimum on a hypothetical exact fibre is sound. Negative/flat Laurent directions near known active-cap sources, or failure of a uniform `P-2` gap, do not refute that exact-fibre minimization. Conversely, exact-fibre stationarity alone does not supply a positive energy gap or make the blocker strata closed.

### 12. Exponent-one orbit-zero membership is false

The archive's valid target is localized/powered (`a*T in I_mix+K^16` at the current promotion). Any older step using `H0H1H2 in I_mix` at exponent one is superseded by an explicit obstruction.

## Current proof spine after deduplication

The current global implication is best stated without the historical detours:

```text
hypothetical exact N=8 source
        |
        v
full X5 system (all mixed amplitudes vanish; pure amplitudes normalized)
        |
        +-- if one of 560 triangle carriers is active --> certified clean-cap descent
        |                                       --> certified N=6 contradiction
        |
        `-- all 168 stars are automatically blocked on X5;
            hypothetical fibre lies in triangle-blocked incidence
                |
                +-- exact-fibre minimum/reduced-normal-cone nonlinear route
                +-- direct remote-locus contradiction or same-source cap
                `-- localized orbit-zero K^16 algebra / chart boundary library
```

Thus the one genuinely global missing arrow remains

```text
X5 + all 560 triangle carriers blocked  ==>  contradiction.
```

The three nonduplicate ways presently archived to attack it are:

1. a nonlinear/Hermitian consequence of minimum-norm stationarity that is sensitive to simultaneous mixed zeros, triangle blockers and the reduced normal cone;
2. a direct contradiction on the remote full-tail locus, or a same-source triangle/cancellation-clean cap theorem; tail entry itself is now solved;
3. a literal-provenance-preserving localized orbit-zero certificate beyond `K^16`.

The diagonal charts, corrected cycle residuals, `k5/k6` faces, four-qubit invariants, and SAT cover are supporting libraries for these arrows, not independent proofs of the global implication.

## Terminal audit verdict

No currently certified document closes the full eight-site conjecture. The archive contains substantial exact closures, but its main hazard is stale task language: old “open” labels sometimes name already closed subcases, while several old “closed” summaries silently exceed their certified or support-bounded scope. The authoritative finite-carrier target is now `X5 + 560 triangle blockers => contradiction`; all other live work should state explicitly which remaining arrow it advances and whether the input is certified or merely a working exact artifact.
