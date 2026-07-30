# Route registry

Current proof-state audit and ranked next actions:
[current-proof-audit-and-next-steps.md](current-proof-audit-and-next-steps.md).
The theorem-sized parallel portfolio is
[parallel-proof-attack-board.md](parallel-proof-attack-board.md).

| Route | Mechanism | Status | Required concrete output |
|---|---|---|---|
| OC1 | Five-set one-crossing cofactor quotient | One-, two-, and bare three-cut criteria impossible; on the fixed repaired interior, boundary-only changes, arbitrary A23, and six adjacent A25 affine lines are excluded; general simultaneous internal blocks/full mixed-sector compatibility open | `notes/five-set-universal-cofactor-annihilator.md` proves, by duality from the arbitrary-complex six-site theorem, that every ternary five-set has a target-active functional annihilating all five internal one-hole cofactors. Hence `F1 = Gamma B_U` gives `ker(F1) not subset ker(delta_U)` for every aggregate edge family and every five-cut. Six overlapping boundary-only witnesses likewise coexist universally, superseding the local incompatibility target in `notes/six-set-one-crossing-hessian-pullback.md`. `notes/adjacent-five-cut-hessian-intersection-countermodel.md` gives an exact sparse integral six-site family whose two adjacent five-set defect spaces are both target-active but whose lifted kernels have target-zero intersection; its checker also proves `sum_z T1,z = 6T0 + 2T2`. `notes/adjacent-five-cut-complete-high-sector-countermodel.md` goes further at order eight: it derives the atomwise `T1/T3` versus `T0/T2` formulas and a division-free summed-lift lemma, then gives one shared integral eight-site family on which two adjacent complete identities `T3,z|K_U = iota delta|K_U` coexist, their lifted intersection is target-zero, and two witnesses still contract `T2` to a nonzero diagonal target. This defeats any descent based only on two complete adjacent quotient maps; it is not a Krenn counterexample because its full tensor has two mixed coefficients. `notes/three-adjacent-five-cut-complete-quotient-countermodel.md` supplies a support-minimal twelve-source integral family with three active complete cuts and one mixed residual; two further cells kill that mixed coordinate while preserving the triple and moving the debt to three other words. Under hypothetical full GHZ, every five-set still forces a nonzero target quotient through its high sectors. A continuation must use at least four overlapping cuts, a coupled packet of mixed-sector equations, or another global invariant. Exact audits: `computations/verify_five_set_universal_cofactor_annihilator.py`, `computations/verify_adjacent_five_cut_hessian_intersection_countermodel.py`, `computations/verify_adjacent_five_cut_complete_high_sector_countermodel.py`, and `computations/verify_three_adjacent_five_cut_complete_quotient_countermodel_independent_audit.py`. |
| T1 | Tensor flattenings, exterior powers, representation theory | Promoted but incomplete | Partition-rank n=4 proof, border theorem, arbitrary-matrix prism rigidity, and one-slice anchors. `notes/source-hessian-bipartite-rankdrop.md` closes the gauge-rigid connected bipartite rank-drop branch whenever both deleted stars are row-full: all nine pair responses then have flattening rank at most two. Every pair must instead have an extra Hessian kernel, disconnected rank-three internal graph, or a zero star row. `notes/global-covariance-nonsingularity-boundary.md` shows that global-covariance nonsingularity is false for exact binary GHZ and remains false under all three exact ternary binary faces, while standard ternary `K_4` and the prism border have determinant `+1` and `-1`; it gives the exact kernel-star identity and an explicit pair-Hessian gauge-membership test for the still-plausible full ternary claim. |
| C1 | Support/cancellation combinatorics, minimal counterexample, matching identities | Global stub rewrite boundary isolated | Exact lemma retaining asymmetric endpoint colors. `notes/stub-matching-odd-cut-countermodule.md` gives the complete stub formulation and an exact rational six-site boundary: all 729 homogeneous fibres vanish, three selected constant monomials are individually one, and the bridgeless minimum-valuation prism rewrites only to bridged states (`1-3+1+1=0`). Odd-cut parity is invariant but slack changes by half the difference of the two transversal cut counts; any positive continuation must use the later inhomogeneous target-normalization layer. |
| X1 | Exact symbolic experiments for n=4 and n=6 | Restricted falsification only; no uniform leverage | Exact diagonal SAT obstruction; degree-9 ideal nonmembership; diagonal degree-18 certificate; full off-diagonal radical test open |
| A1 | Square-zero algebra and hafnian-power identities | Linear flag selection exhausted; nonlinear shared-edge step required | Exact cumulant formula in `notes/induction-route.md`; `notes/pair-covector-selection-obstruction.md` proves that even a tensor-active coordinate anchor can have unavoidable higher cumulant for every nondegenerate covector. `notes/odd-characteristic-six-boundary-barrier.md` gives the denominator-free six-site clean equation and an exact active binary pair whose defect is `-s^2 kappa_1` for every covector over every odd-characteristic extension. `notes/six-cap-flag-averaging-countermodel.md` proves the exact all-cut sector incidence formula and gives a complete ternary first-layer model with every local cap dirty. `notes/full-ghz-linear-flag-countermodule.md` goes further: even the full GHZ coefficient equations in the maximal formal matching-term relaxation satisfy all universal cut averages while all 56 one-cross criteria fail by three target rows; two genuine equal-output scalar sources also have different total nonlinear cap corrections. `notes/one-site-gluing-cubic-contamination.md` proves the arbitrary-covector edge formula and shows that it closes only the one-cross sector: canonical K4 self-gluing gives the 3-connected, tight-cut-free rank-one prism with exact output `Delta_6+e_012012`, while general K4 gluing is exact iff the nonlinear collision `L_0L_1L_2 q^(m-2)/(m-2)!` vanishes. Thus no linear combination of coefficient and cut-incidence identities can select a cap, and no formal tensor-contraction closure gives an amplification. A continuation must use nonlinear recombination of shared aggregate edge factors. |
| B1 | Binary restriction and constructive n=8 repairs | Sharp entry minimum; direct and bounded closure repairs closed exactly | `notes/binary-norm-equality-counterfamily.md` gives a uniform norm-flat `n+2`-cell exact family at the Hamilton norm and three simultaneous non-Hamilton binary restrictions at `n=6`. `notes/binary-rank3-projection-counterexample.md` gives an exact finite complex realization of `e0^6+e1^6+(e0+e1)^6`; `notes/binary-rank3-pair-suspension-obstruction.md` proves by an exact Hessian rank certificate that this particular point cannot be extended to the eight-site target by arbitrary new stars and a direct edge. `notes/binary-coordinate-projection-counterfamily.md` shows that every coordinate-line rank-two projection, including arbitrary site variation and degeneracy, has a finite `n+2`-cell source for every even `n>=8`. Separately, `notes/n8-binary-padding-seven-fibre-obstruction.md` gives solver-free zero/one/two-excess obstructions plus compact semantic and DRUP certificates through five excess cells for the rational n=8 seed. `notes/n8-border-seed-direct-repair.md` exhausts all `104^2` direct mates of the two sparse-border singleton fibres: every minimum four-cell repair creates 4--9 new singleton fibres. Its explicit 16-cell rational near-solution cancels all binomials and preserves the three pure coefficients but leaves exactly four singleton residuals. From that point the exact union repair needs at least six added cells (288 supports, 144 modulo the residual involution), every minimum support creates 14--29 fresh singleton fibres, no singleton-free extension exists through 25 total cells, and a structured closure search is UNSAT through 34; the first singleton-free 32-cell layer is killed by an explicit three-binomial odd Laurent triangle. `notes/n8-border-pair-suspension-obstruction.md` adds a full arbitrary-star theorem: the twelve-cell Laurent core cannot be extended to ten-site equality by two new vertices and a direct edge, because 358 singleton Hessian rows force all nine star products onto a port matching and their values collapse to one rank-one line. Arbitrary denser ternary repairs remain open. |
| K4C | Composition of two four-site ternary equality shores | At least ten singular cross blocks | `notes/two-k4-composition-sectors.md` gives the exact 0/2/4-cross formula, the 30/48/3 shore-word census, the 51-dimensional edge-cylinder boundary, and an exact obstruction to the full seven-parameter AGL chart. `notes/two-k4-low-matching-cross-obstruction.md` excludes every cross graph of matching number at most three. `notes/two-k4-unique-perfect-matching-cross-obstruction.md` excludes every cross graph with a unique transversal perfect matching (all six relative shore colourings have independently RUP-checked exact support certificates, and the bare four-edge chart has a hand live-box proof). `notes/two-k4-dead-slice-determinantal-boundary.md`, `notes/two-k4-two-singular-boundary.md`, and `notes/two-k4-no-exact-two-singular.md` force a determinantal boundary and close the exact-one and exact-two strata. `notes/two-k4-exact-three-incidence-boundary.md` classifies all 560 exact-three position supports. `notes/two-k4-exact-three-matching-obstruction.md` excludes the matching orbit by projective-frame singleton contractions; `notes/two-k4-exact-three-path-zero-collapse.md` forces every path block to zero; and `notes/two-k4-exact-three-allzero-path-obstruction.md` eliminates that final literal path via the exact one-defect `Per_3` dichotomy. Hence every dead-slab solution has at least four singular blocks. `notes/two-k4-four-singular-row-obstruction.md` brings in the omitted mixed sectors: a field-uniform six-cell Hessian-erasure lemma excludes any chart having two completely invertible block rows or columns, so every singular support meets at least three rows and columns. `notes/two-k4-exact-four-nonmatching-obstruction.md` extends erasure to a star with one arbitrary component; it excludes a completely invertible row/column paired with a row/column having at most one singular block. Consequently every exact-four support meets all four rows and columns and is a transversal perfect matching. `notes/two-k4-four-singular-matching-hessian-obstruction.md` closes that orbit for arbitrary ranks by a separated-defect eight-cell erasure theorem. The same theorem excludes exact five: its row and column degree partitions would be `(2,1,1,1)`, and two singleton rows necessarily have distinct defect columns. `notes/two-k4-coincident-defect-incident-obstruction.md` excludes the exact-six `K_(1,3) sqcup K_(3,1)` orbit. `notes/two-k4-six-cycle-two-defect-obstruction.md` proves a full-row/two-defect Hessian theorem that excludes both remaining exact-six orbits. Its separated one-plus-two extension then enumerates the exact-seven frontier: 816 labelled supports in three orbits (`C_4 sqcup P_4`, `C_6 sqcup K_2`, and `P_8`, of sizes 144, 96, and 576), and excludes all of them by the actual eight-cell two-/four-cross identities. `notes/two-k4-exact-eight-checkerboard-hessian-obstruction.md` reduces the exact-eight census to two disjoint-pair masks and one overlap-one mask. Exact plane-boundary factorization closes the formerly residual overlap branch, while the actual two-/four-cross sector kills all three masks, including arbitrary singular ranks and literal-zero degeneracies. Hence every two-`K_4` solution has at least nine singular cross blocks. `notes/two-k4-exact-nine-k33-frontier.md`, independently audited in `notes/two-k4-exact-nine-independent-audit.md`, enumerates nine exact-nine position orbits, closes seven by padded overlap-one incidence and one by a weighted division-free disjoint-pair certificate, and reduces the sole residual to a singular top-left `K_(3,3)` square with all seven blocks through the fourth row or column invertible. `notes/two-k4-k33-nonzero-star-erasure.md` then proves exact nonzero-, one-zero-, and two-zero star kernels for arbitrary unrelated erased planes. Endpoint-plane incidence forces every block in the singular square to be literal zero, and the remaining seven-edge graph has matching number two after an explicit diagonal shore-weight gauge. The independent proof and checker in `notes/two-k4-k33-two-zero-independent-closure.md` verify the final local kernel and weighted transfer. Thus exact nine is impossible. |
| PF1 | Transverse paired-Pfaffian localization | Matching-hole boundary reduced to three acyclic directed caps | `notes/matching-hole-zero-cross-pfaffian-obstruction.md` excludes the zero-cross chart over every field by a `5^3` exact flattening audit. `notes/matching-hole-directed-cycle-obstruction.md` adds a field-uniform local theorem: the three- and four-site equations forbid an alternating directed four-cycle between any two hole-matching edges, so the two opposite transversal Schur caps on a four-site union cannot both be nonzero. Any surviving matching-hole source must have a global decomposable correction `R_k` with a nonzero cross-site entry, while its directed cross graph has no such cycle. The remaining task is to couple the three allowed rank-two corrections across the full six-site face. |
| D1 | Diagonal-edge reduction followed by complementary hafnian minors | Recurrence shadow complete through `n=10`; deletion/cofactor matching shortcut blocked exactly | Exact 171-cover / 10-orbit support lemma and SAT audit in `computations/verify_diagonal_n6_obstruction.py`; `notes/diagonal-recurrence-unfolding-lemma.md` proves feasible-to-matchable and unique-matching-to-feasible uniformly. `notes/full-deletion-graph-no-perfect-matching.md` gives the decisive rational six-site obstruction to the proposed full-deletion 1-factor step: weights `1` on and across one triangle and `-2` on the other give full hafnian `-12` but `C=D=K_3 dotcup K_3`. Its exact audit also supplies three strongly private eight-site recurrence cofactor graphs, all without perfect matchings, while retaining 97 middle-rank covers. Thus any continuation must keep pivot labels/middle ranks; reduction from arbitrary endpoint matrices remains unjustified. |
| I1 | Source-ideal membership and first radical power | Complete at power one; diagonal quotient complete at power two | `P=F_{0^6}F_{1^6}F_{2^6}` is not in the full mixed ideal, while `P^2` belongs after diagonal specialization. Exact Reynolds/Macaulay audits are in `notes/ideal-membership-route.md`, `computations/test_degree9_source_ideal.py`, and `computations/test_diagonal_power2.py`. Full arbitrary-matrix radical membership remains open. |
| T2 | Target-torus closed orbit, pure-limit jets, and localized clean-fiber relations | Three-face cofactor-plane normal form; full uniform cyclic plane excluded; unrestricted noncyclic six-site system open | `notes/color-torus-pure-limit-two-jet-boundary.md` classifies the pure leading source and gives a dense rational simultaneous two-jet. `notes/cofactor-open-color-cloning-boundary.md` closes the two-face cubic step negatively: local color cloning makes both `01/02` faces exact while every mixed-with-zero layer vanishes. `notes/all-three-binary-cofactor-plane-boundary.md` then imposes the missing `12` face. It proves that the two first-jet rows span a two-plane in every cofactor kernel, rewrites the `12` source as the canonical restricted pairing tensor on those planes, and gives the exact connection-plus-permanent cubic Bianchi equations. The cofactor-open `n=4` chart is excluded by a symbolic nonzero `3x3` flattening minor. At `n=6` the survivor is reduced to `C` plus six planes in `Gr(2,4)`, two complete binary-contact sections, the binary-GHZ orbit condition, and 120 mixed cubics. `notes/uniform-dense-cyclic-contact-obstruction.md` first closes every one-dimensional cyclic eigensection. `notes/uniform-dense-cyclic-plane-obstruction.md` then excludes the full cyclic-equivariant plane chart, including a rotation which mixes or swaps the two contact lines: four pure cubic orbits have a three-line radical, and one mixed cubic forces the two character profiles to coincide and collapse every local plane. The standard three-factor source passes all faces and cubics only on the sharp twelve-zero-cofactor boundary, failing at one degree-four singleton. `notes/first-slice-cubic-three-factor-obstruction.md` proves that this phenomenon cannot persist after resolving all first-slice components: a one-/two-chord witness gives, for every colour, a singleton normalized-slice defect by degree three. The twelve-site balanced triple shows cubic is sharp and quadratic first-slice contact still supplies no factor-closed six-set. `notes/first-slice-bianchi-cancellation-mate-countermodel.md` marks the exact next boundary: an eight-site rank-one cube triple has pairwise `C4+C4` unions and a switch with one external opposite-weight mate; every local collision and iterated first-slice jet cancels on that same-colouring packet to all orders. Thus Bianchi derivatives cannot replace a nonlinear shared-edge coupling between distinct colouring fibres. A noncyclic cofactor-open exact binary six-site seed, or a proof none exists, remains missing. `notes/torus-polystable-fiber.md` strengthens balance to actual squared-magnitude balance. `proofs/uniform-five-factor-toric-obstruction.md` excludes a uniform strictly balanced five-factor chart. |
| NRM | Minimal-norm and Hermitian hafnian inequalities | Closed at all available stationarity equations | `notes/six-site-sharp-hafnian-norm-slack.md` proves the sharp complex six-site inequality `|haf x| <= (sum_e |x_e|^2)^(3/2)/sqrt(15)`, with equality exactly the dense vertex-gauge orbit, and hence the unconditional strict floor `||A||_F^2>3*15^(1/3)` for a ternary six-site preimage. Its algebraic family `b^3-a^2b=1` has all three pure coefficients one, full isotropy, injective star/triangle maps, gauge-only full derivative, and generic smooth local norm minimality, while every pure-slice energy tends to infinity. Thus balance, block normal equations, and local minimality cannot force the sharp equality case; a continuation must extract a new identity from simultaneous mixed GHZ vanishing. Exact audit: `computations/verify_six_site_hafnian_norm_slack.py`. |
| S1 | Simultaneous one-slice decompositions of diagonal tensors | Generic common-power branch globally excluded; exceptional branch needs a ternary row | `notes/slice-cover.md`: every vertex/color forces an active rank-one incident edge with a coordinate factor at the opposite endpoint. `notes/fixed-star-three-hole-gauge-dichotomy.md` uses the actual common powers `q^(m-1),q^(m-2)`: if all quotient three-hole catalecticants have only their universal expansion-gauge images and every deleted rank-three graph is connected nonbipartite, then every fixed-star row has one centre and the three complementary hafnians are pure. `notes/fixed-star-parabolic-gauge-audit.md` proves that the large one-row local parabolics do not automatically enlarge those kernels: at the quotient site they preserve the gauge image, elsewhere they move the catalecticant itself, and the simultaneous three-row stabilizer is only the diagonal target torus. If the generic hypotheses hold at every vertex, the source is three one-factors and a fourth matching contradicts GHZ. Hence every hypothetical source has an explicit extra catalecticant kernel or a low-rank/disconnected/bipartite deleted graph at some star. `notes/all-exceptional-star-rainbow-countermodel.md` shows the exceptional escape is real for every constant fiber, every exact binary face, and two complete rows at every overlapping star: one coherent rainbow matching is the first missing ternary equation. |
| O1 | Color-sensitive infinitesimal target stabilizer | First order useful; pure second-jet continuation closed | `notes/color-sensitive-averaging.md` gives the coordinatewise edge-deletion identity, while `notes/color-stabilizer-matroid-obstruction.md` gives its sharp dense support-matroid countermodel. `notes/color-stabilizer-second-jet-tautology.md` derives the exact polarized second derivative, quotients the ordinary vertex gauges, and proves that every coloring component—including the actual pair-deleted common-power expression—is only an Euler-weight product times the original coefficient equation. The color-sensitive quotient has dimension `2(n-1)` but identically zero second fundamental form; new progress must use a non-stabilizer tangent or independent source structure. |
| V1 | Three-shore contraction and vector-permanent slice spaces | Incomplete; fourth-cut/shared-sector invariant required | `notes/determinant-split-route.md`: every six-site vertex triple is torus-zero-free and the invertible-edge graph is triangle-free. `notes/five-set-contamination-normal-form.md`: at every order, failure of triple-shore descent is exactly a constant-row quotient; its mixed row rank is at most nine, it has a ten-word vector-permanent certificate, and an invertible internal edge forces either a pure three-cross selector or the cyclic staircase (32b). `notes/n8-five-degenerate-triple-shores.md`: every invertible `K_8` pair has at least five pure-selector triple shores. `notes/five-selector-all-complement-bridge.md`: those selectors cover all fifteen four-site complements; coherent open-slot gauges force termwise killing or a rank-one/single-edge star, and `m` nontermwise selectors force at least `ceil(m/2)` bad complements. `notes/selector-uncapped-pair-defects.md`: every nonconstant coefficient of the internal six-site tensor must have word-aligned rank-three extensions through both deleted stars; termwise selectors project away exactly the pair-used channel. `notes/n8-residual-mask-uncapped-vanishing.md`: erasing columns force a nine-word internal slice plus its four-site cofactor to vanish on 11 residual hard assignments and a three-word fibre to vanish on 24 more. `notes/n8-011166-full-row-square-obstruction.md` uses the full row to exclude the sole assignment missed by those erasures, reducing the union-five boundary to the other 35 assignments in 12 mask orbits. `notes/five-hole-monomial-factor-obstruction.md` excludes all 7,776 coordinate-monomial allocations of the resulting five-hole factorization by a 90-dimensional response decomposition and a directed-cut minimum-support-four lemma. `notes/five-hole-factorization-counterexample.md` gives an exact rational mixed-basis factorization of the five-hole diagonal with `011166` masks, proving that the common-annihilator row alone cannot finish. `notes/five-hole-factorization-two-hole-nonlift.md` then shows that this exact point cannot extend even through the first omitted two-hole layer: all five required scalar cofactors are nonzero, for every permutation of the three factor families. `notes/n8-witness-union-six-erasure.md`: on the separate union-six stratum, prior two-hole tests leave 597 hard assignments; four/five erasures force zero fibres on 580, leaving exactly 17 no-certificate assignments in 10 mask orbits. |
| L1 | Low-connectivity aggregate support | Complete through vertex cuts of order two; exact three-cut boundary isolated | `notes/series-parallel-support-obstruction.md`: every exact support is 3-vertex-connected, hence contains a `K_4` minor and is not series-parallel. The exact three-separator channel formula shows why a singleton odd lobe/cubic vertex survives slice rank; order-minimality only forces an all-three channel on nontrivial odd lobes. |
| P1 | Planar bipartite Kasteleyn determinant | Promoted through order twelve; open from fourteen | `notes/planar-kasteleyn-route.md`: unique-transversal triangularity and pure-star lemma; Euler/high-degree-core excludes `n=10`; exact graph and shell audit excludes `n=12`. Fu's higher-domain theorem applies only to the shared-basis holographic subansatz. Cai--Gorenstein character theory also stops before the essential block one-hot projections; doubled Bell paths explicitly give matchgate local images of `GHZ_3`. |
| DR1 | Bell-pair dual-rail padding | Exact local padding closed | `notes/dual-rail-padding-obstruction.md`: injective one-hot padding is the union of three one-factors and has an uncancellable fourth matching; signed copies to the same partner aggregate to one cell. Any escape needs a different-neighbour alternating cancellation cycle and must pass the global odd-circulation lattice test. |
| SV1 | Rank graph plus directed coordinate anchors on six vertices | Complete arbitrary-complex six-site theorem | `proofs/six-site-arbitrary-complex-obstruction.md` and `notes/six-site-rank-graph-assembly-audit.md` exhaust all nineteen maximum-degree-two defect graphs. Rank-one anchor fibres close `|F|=0`; a persistent 6,095-record Laurent bundle (SHA-256 `83c4b90ab89d59b0543c40ba5c35aea3659bdcf1ffeb01ab597c9194e9cb70f0`) plus the exceptional-triangle certificate closes `|F|<=3`; exact rectangle and transfer certificates close every `|F|=4,5,6` type. The rank-one orbit CNF has 123,666 clauses and a deletion-free 1,166,186-addition DRUP proof checked both upstream and in-repository. Thus `H_6(A) != Delta_(6,3)` for arbitrary complex endpoint-ordered aggregate matrices, including zero blocks. |
| U1 | Uniform all-even reduction to six vertices | Corank-two all-dead, one-/two-zero live, full pure-lift, locally full-rank aligned three-field, endpoint-rank-at-most-two, the entire sole-defect branch, rank-budget twelve, and uniform full-nine target incidence closed; aggregate-to-blockwise/Hessian conversion, multiple defects, budget above twelve, arbitrary blocks, and uniform descent open | `notes/uniform-six-vertex-reduction.md` gives `L6+L4(x+L2)=0`; exact binary examples falsify scalar/general-covector pair cleaning. `notes/source-hessian-bipartite-rankdrop.md` gives an all-even pair trichotomy with endpoint order and zero blocks retained. On the first non-gauge corank-two stratum, `notes/all-dead-corank-two-product-reduction.md` and `notes/aligned-two-plane-boundary-closure.md` exclude the complete all-dead branch over characteristic zero. In the live branch, `notes/live-component-zero-cut-propagation.md` produces one complete invertible component behind a literal zero-star cut. `notes/coordinate-free-live-diagonal-square-ideal.md` proves, for arbitrary local live bases, that every outside-annihilator contraction retains at most one diagonal target value and hence forces a two- or three-axis outside cover. `notes/live-isotropic-second-jet-cover-patterns.md` upgrades this to two distinct centres per active colour on each isotropic component. All six-centre cases contradict the uniform five-witness bound; only `B=lambda E_cc` and the rank-two/two-coordinate-factor configurations survive with four centres. `notes/live-four-centre-final-deviation-obstruction.md` closes both patterns when there is one literal zero. `notes/live-multiple-zero-hall-factorization.md` keeps the actual common power and arbitrary zero-incident blocks: for `s` zero sites it proves `|D_c|<=s` and `|D_c cap D_d|<=s-1`, and equality factors through the centre-to-zero permanent tensor. At `s=2` this immediately closes the rank-two/two-coordinate-factor pattern; two exact four-site pure-cap projection lemmas then exclude all eight incidence orbits of the coordinate-rank-one pattern, including rank-one singleton escapes and the mixed-type pure-color-zero case. `notes/cross-pair-pencil-cancellation.md` gives the exact mixed-gcd pencil criterion and a genuine binary source in which two dirty different-pair caps have two clean interior pencil points. `notes/global-cap-span-descent.md` upgrades this to the cap-cofactor saturation/Veronese criterion and supplies the sharp ternary prism root-cover plus a formal full-GHZ cap-family countermodel. `notes/uniform-cap-minor-hierarchy.md` restores shared-edge compatibility at every even order: all `1x1`, `2x2`, and `3x3` cap minors obey one factorially normalized determinant identity. `notes/polarized-eight-site-unrestricted-counterexample.md`, independently reconstructed in `notes/polarized-eight-site-unrestricted-counterexample-independent-audit.md`, gives an integral solution of the bare equation `z*q^3/3!=Delta_(8,3)` but a constant rank-three cross minor excludes `z=a*q+4*p*s`; therefore the literal pair-cap form, several shared rows, or overlapping physical-pair identities cannot be discarded. `notes/invertible-monomial-nine-cap-classification.md` classifies the diagonal and three-cycle direct-cap orbits. In the three-cycle orbit the diagonal products are the uncontaminated pure responses, but all lower cap minors reduce to the same first-jet equations; a six-site square-free countermodel proves that the remaining obstruction must use the actual common-power condition. The three-cycle is nevertheless excluded on the gauge-rigid connected nonbipartite chart, forces a literal zero row on the connected bipartite chart, and is impossible on a four-site boundary over every field. The support-independent private-pair projection now closes the entire 45-dimensional pure-lift span, with arbitrary multiplicity, repeated pairs, aggregate complex coefficients, multi-site rows, and endpoint-ordered blocks. The independently audited degenerate-field normal form and three sole-defect common-power theorems close exactly one deficient site: every response has an ordinary active-pair SDR, locally separable SDRs die by distinct lift, and all 157 locally nonseparable packet orbits have unit common-power ideals (145 rational cases and 12 Laurent-parameter cases). The remaining coherent-field cases have two through five deficient sites and at least one full local frame; the all-six-deficient case is closed. Arbitrary non-line-field packets and the all-even descent also remain open. Exact artifacts: `notes/sole-defect-nonseparable-packet-common-power-obstruction.md` and `notes/sole-defect-nonseparable-packet-common-power-obstruction-independent-audit.md`. |
| N1 | Nonarchimedean GIT and projective reduction | Exact conditional bridge; unconditional route blocked | `notes/nonarchimedean-git-bridge.md`: any primitive integral model whose special output remains in the GHZ orbit is, up to an integral basis change, a projective-stabilizer normalization and hence exactly the diagonal valuation LP. The rational q=1 exact point proves projective properness need not preserve nonzero matching output. `notes/ternary-semistable-base-locus-counterexample.md` strengthens the obstruction in the actual local dimension: the six invertible identity blocks on (K_3\sqcup K_3) have (H_6=0), while their determinant product is a nonzero (SL_3^6)-invariant. Thus even ternary source semistability does not avoid the matching base locus; a bridge must preserve a target-pullback invariant and exclude the target orbit boundary. |

**U1 status addendum (updated 2026-07-29).**  The chronological promotions below
supersede the older threshold language in the compact table row.  Pair
selection is now uniform for every even \(N\ge8\): there are at least
\(N(N-7)/2\) doubly aggregate-injective pairs and a good fan of degree
\(N-7\).  The mixed equations empty the regular nonbipartite branch, and
the escape-chart descent plus four-port balance theorem empty defect one
at every order.  Hence every good pair lies in exactly the extra-kernel
(E1) or defect-at-least-two (E2) chart; the former regular finite-port and
induced-zero-shore alternatives are retired.  On the three-essential
equality branch, every cubic nonneighbour carries a leave-one-anchor
nullity profile at least \((1,2,2)\).  The active gate is now to export
the E1/E2 structure through overlapping physical pair equations.

[The distinguished-span-two E1 promotion](extra-kernel-distinguished-span-two-closure.md)
turns every dense connected-nonbipartite E1 chart with
\(\dim D_{pq}=2\) into a zero-star triple and pure three-cross selector;
its residuals are a star row supported on at most two sites or
\(\dim D_{pq}\ge3\), and its exact export is the full common-complement
27-equation system.  Two overlapping zero-star exports form one 81-row
system; its uncontracted rows force at least two live diagonal colours in
each star pair and exclude the recorded repeated-pair filter.  One
isotropic contraction packages all nine opposite rows into a shared
common-power dressed cap, ternary except on the scalar-matrix-unit binary
boundary.  The
[four-site coordinate-monomial obstruction](four-site-coordinate-monomial-dressed-packet-obstruction.md)
closes its \(m=4\) ternary coordinate-monomial stratum for arbitrary
weights.  The complementary
[scalar-unit full-isotropic guard](uncontracted-four-cut-scalar-unit-full-isotropic-packet-guard.md)
satisfies every isotropic packet at \(m=5\), even after the opposite rows
are padded to be core-dense and injective, but it fails the full 81-row and E1
graph provenance.  Thus arbitrary local superpositions/higher powers and
the exceptional scalar-unit row coupled to the omitted provenance are the
active E1 exports.
[Centered E2 stability](centered-defect-stability.md)
reduces an E2 fan to \(b(R-r)\ge2\), \(\delta(R-r)\le2\), or an E1 pair.
The centered rank tradeoff closes its rank-two/rank-at-least-two local
branch.  [The centered rank-one overlap-packet theorem](centered-rank-one-overlap-packet.md)
takes the specific sharp witness through the complete 27-row system: its
contracted four-cofactor table has an exact \(N=8\) common-\(q\) relaxation,
yet none of the 24 minimal three-private-coordinate packets has a
shared-star lift modulo \(\operatorname{Ann}(q)\).  This closes only that
minimal stratum.  The two independent pure-response slices nevertheless
force at least two additional singular spokes for every realization of the
sharp mask; at \(N=8\), the exposed site has rank-three degree at most two.
Defect coefficients are faithful, defect two forces a
sparse star row, and a dense defect-three chart spans all three coefficient
directions.  Fan propagation confines exact defect two to nine high-degree
charts, or exposes a rank-three-degree-at-most-two vertex; its global
sparse-center alternative is a synchronized nine-row packet with an exact
selected-row guard.  The remaining E2 exports are the finite-nine/low-degree
residual, full-overlap compatibility for faithful coordinates, propagation
of the sharp mask's singular spokes, and classification of the other
rank-one masks.

[The canonical transition-pencil theorem](canonical-transition-pencil-fan-dichotomy.md)
now treats the physical inhomogeneous transition without choosing an
annihilator representative.  A flat good fan is centre-dark, so its centre
has block degree at most six outside the fan; a nonflat fan has a literal
nonzero \(2\times2\) source minor, an inverse two-flag selector, and a
generically active affine cap line.  Cleanliness on that line remains a
tensor-polynomial common-root problem.  Thus the two structural residuals
are the degree-three-through-six centre branch and the curved active-line
branch, rather than an abstract homogeneous acyclicity question.

For synchronized E2 responses,
[the universal inactive-core theorem](multiresponse-inactive-core-evacuation.md)
evacuates every block seen by at least one direction in a spanning defect
family.  In the nonsparse physical-row branch, the three normalized targets
give a three-set matching-saturation cover of the exact core \(K(D)\);
isolated rank-three vertices and shore ratios above three are impossible,
and \(K_{1,3}\) has explicit ternary coordinate anchors.  Synchronizing a
chartwise spanning family through one common plane bundle is still open.
[The augmented-gauge polynomial](augmented-e2-gauge-clean-cap-polynomial.md)
then identifies the nonlinear residue exactly: along an accessible defect
line, a clean active cap is equivalent to a nonconstant gcd after
saturating the vector-valued error coordinates by the activity linear
form.  Defect spanning supplies access, not that common divisor.

[The good-clique curvature-or-zero-shore theorem](good-clique-curvature-or-zero-shore.md)
now composes the four-degenerate bad-pair graph with the canonical physical
transition.  For every even \(N\ge16\), either a literal nonzero source minor
gives a generically active cap line, or a clique of
\(h=\lceil N/5\rceil\) sites is aggregate-zero internally and its arbitrary
star rows obey the complete \(3^h\)-equation common-power identity.  This
replaces a fixed exceptional-chart census on the high-order flat branch by
one growing zero shore.  On the degree-at-most-six flat branch,
[the three-anchor transversal theorem](flat-fan-low-degree-residual-transversal.md)
leaves only a three-anchor cofactor kernel, a shared rank-one centre line,
or a common rank-two centre plane.  The last two alternatives are sharp
Segre/Plücker circuits for one star and must be tested through overlapping
physical centres.

[The curved good-fan guard](curved-full-good-fan-pure-activity-root-guard.md)
shows that a full good fan, gauge rigidity, physical nonzero curvature, and
literal connection/Bianchi identities can still have clean error equal to
a pure power of the activity form.  Its transverse target rows fail, so a
positive common-root theorem must use them.  Independently,
[the differential Plücker closure](plucker-hessian-closure-and-defect-three-transition-guard.md)
uses the literal product rectangles \(Z_{ab}Z_{cd}=Z_{ad}Z_{cb}\) and gauge
integration by parts to couple distinct E2 directions through diagonal
products.  Its exact defect-three guard satisfies the six off-diagonal
identities and all associated unequal-endpoint transition rows but has a
visible extra Hessian class.  Thus transition flatness alone cannot
synchronize the planes; gauge rigidity supplies the next positive
classification constraint.

[The global flat-fan collapse](flat-good-fan-degeneracy-degree-four-collapse.md)
now supersedes the degree-five/six terminal language.  A vertex of bad-pair
degree at most four has at least three good neighbours at every even
\(N\ge8\).  If their fan is flat, all good blocks vanish and the forced
anchors leave block degree exactly three or four.  The cubic case has three
pure cofactors.  At degree four, dependent centre factors force the fourth
cofactor to be pure; independent factors make the deleted centre star
injective and export an essential direction transverse to a proper
opposite-star flag.  The later
[essential-edge purity and port-merging theorem](flat-degree-four-essential-purity-nullity-export.md)
now subsumes both cases: every bad pair has a nonzero monochromatic pure
cofactor, every bad-only star is a three-fibre pure-port partition, and one
representative per fibre replaces the whole star without changing the
matching tensor.  In an entry-minimal source, irredundancy already makes
each fibre a singleton.  Thus the complete primary flat endpoint is a
literal cubic exact source.  Its
[two-nonneighbour reduction](cubic-two-nonneighbour-faithful-surplus-dichotomy.md)
then yields either two faithful nullity-at-least-two Hessian spaces on one
exterior star or a pure two-crossing packet with eight zero responses and
one decomposable target; invertible residual blocks force the faithful
chart in the entry-minimal setting.

The flat endpoint is now closed completely.  The independently audited
[flat boundary-core theorem](flat-cubic-boundary-core-order-eight-reduction.md)
excludes every even order at least ten and reduces order eight to four
values of the number of cubic sites.  The independently audited
[small-core essential-complement obstruction](flat-n8-small-c-essential-complement-obstruction.md)
excludes one and two cubic sites, while the independently audited
[large-core matching-cut obstruction](flat-n8-large-c-matching-cut-obstruction.md)
excludes three and four.  Therefore the
[unconditional curvature-line selection theorem](unconditional-curvature-line-selection.md)
shows that whenever an exact source exists, every minimum-support
representative has a nonzero physical transition minor and a generically
active canonical cap line.  This is a representative-selection theorem;
it does not claim that every redundant presentation has nonzero curvature.

Independently, the audited
[cubic six-type propagation theorem](cubic-packet-six-type-boundary-core.md)
confines the nonfaithful pure-packet branch to order at most eighteen.  At
every even order at least twenty, a cubic-centred source has a faithful
residual pair; otherwise all residual activity meets six typed pure ports.

The auxiliary large-shore route also strengthens.
[Zero-shore internal-star saturation](zero-shore-hafnian-ideal-and-internal-star-saturation.md)
proves that at most \(h\) complement sites miss each target axis, so at
least \(N-4h\) have injective internal stars.  Unless a cross transition
returns an active cap line, the zero-shore interface to those sites has at
most \(3h+2\lfloor3h/(h-2)\rfloor\) nonzero blocks.  Exact scalarization
also puts all three target coordinate monomials in one hafnian ideal and
retains the full common-power apolar ladder.

On the curved branch,
[the inactive-root export](curved-cap-inactive-root-export-and-osculating-ledger.md)
shows that a clean but inactive cap must produce either an exact
lower-colour effective quadratic or a nonzero nilpotent response packet.
Repeated inactive roots obey an explicit polarization ledger; the
zero-data root of the curved guard fails a transverse pair row and is not
source-compatible.  The independently audited
[two-root polarization and curvature-square theorem](curved-two-root-polarization-and-four-cut-square.md)
then removes two known roots in one divided-power formula, reduces the
first boundary to the explicit wedge \(R_0\wedge R_1\), and couples
overlapping coordinate charts through shared \((L,M)\) data and the
physical square \(AU-BF\ne0\).  Its pure two-site rows exclude the old
scalar-zero zero-data guard, while a sharp selected-row square guard shows
that propagation to other colour squares or good-star injectivity is still
essential.

The independently audited
[uniform rootless-line theorem](curved-rootless-line-uniform-response-resultant.md)
now eliminates the target row from the clean error at every order:
\[
 {\cal E}(K)=\sum_{j=2}^{h}s(K)^{h-j}q^{[h-j]}r(K)^{[j]}.
\]
Gcd one is equivalent to a rank-\(2h\) Sylvester multiplication map.  At
the scalar-zero point of an off-diagonal canonical line it forces an
invertibly paired, nonnilpotent direct-free response
\(r_*q^{[h-1]}=-\alpha\Delta_{2h,3}\).  At \(N=8\), the independently
audited
[cubic Macaulay packet theorem](curved-no-root-macaulay-and-scalar-zero-packet.md)
turns this into a rank-six minor on literal four-cut rows and gives, at
each endpoint, a three-site selector or a sharp sparse shore.

Two further guards locate the exact coupling still absent.  The
independently audited
[two-chart unary-root guard](curved-n8-two-chart-unary-root-guard.md)
satisfies two complete clean unary root tensors, four good-star conditions,
the shared \((L,M)\) packet, and \(AU-BF=1\), while hiding its padding
colours from both roots.  Hence a positive inactive-root theorem must use a
complementary scalar-zero or binary-boundary row on each line.  The
independently audited
[symmetric-square selector obstruction](curvature-minor-symmetric-square-selector-obstruction.md)
separately shows that direct inversion of \(AU-BF\) cannot project a
matching response: curvature is exterior-square data, while the two-star
response has same-channel symmetric-square terms.  Those disappear only
after a physical one-site support or common-power annihilation theorem.

The independently audited
[complementary-row frontier](curved-complementary-row-coupling-frontier.md)
with its
[line audit](curved-complementary-row-coupling-frontier-independent-audit.md)
now shows exactly what the first omitted covector contributes.  A clean
unary point joined to a clean scalar-zero binary point has error
\(tu(t\Omega_0+u\Omega_1)\), and hence has an active root unless the two
residual tensors are independent or exactly one vanishes.  The complete
binary row rules out the old one-pair padding shore by flattening rank, but
an exact deconcentrated packet retains cleanliness and injective stars.  The
remaining positive statement must exclude those residual patterns on both
source-provenant charts sharing \(AU-BF\ne0\).

The independently audited
[sparse-star propagation theorem](rootless-sparse-star-propagation-and-rank-one-shore-guard.md)
and its
[coefficient audit](rootless-sparse-star-propagation-and-rank-one-shore-guard-independent-audit.md)
remove one Macaulay alternative outright: support of one endpoint star on
at most \(h-1\) sites forces \(r_*^{[h]}=0\).  At the six-site residual,
rank one away from \(x\) instead gives
\(r_*=LM+E_x\) and \(r_*^{[3]}=E_x(LM)^{[2]}\).  A rational unary
contracted-row guard realizes this factorization with both stars injective,
so its closure must use the full ternary diagonal, the omitted eight rows,
or an overlapping chart.

Finally, the independently audited
[scalar-zero tangent alternative](curved-scalar-zero-tangent-apolar-hall-alternative.md)
and its
[hafnian audit](curved-scalar-zero-tangent-apolar-hall-alternative-independent-audit.md)
retain the complete common power and all nine rows without a support
classification.  Wordwise they give
\(P_\omega^TH(Q_\omega)S_\omega
=D_\omega-\operatorname {haf}(Q_\omega)a\).  Either the top response has
only pure coordinates, with its ternary subcase furnishing the exact
descent, or one mixed word is simultaneously hafnian-nonnilpotent,
hafnian-apolar, and Hall-certified by a nonzero balanced star permanent.
Separate exact guards show that neither the common-power nor star side alone
is contradictory; their cohafnian compatibility is the live uniform
interface.

On the E2 side,
[the differential-Plücker separated-packet obstruction](differential-plucker-diagonal-escape-and-separated-packet.md)
turns a diagonal block escaping the \(q\)-line into two reverse-response
annihilations.  In the fully separated defect-three packet this forces
three shore deficits of two, surviving every pair deletion and
contradicting gauge-rigid activity.  The
[overlapping rank-two packet theorem](overlapping-rank-two-plucker-plane-packets.md)
then reduces every diagonally live rank-two block on the dense
six-primitive chart to a glued physical plane packet, a complement-sum
block, or an endpoint-hole collapse.  Complement-sum is empty when all
three defect components are imbalanced and equals the constrained universal
inactive core when all are balanced.  The remaining E2 work is zero
diagonals, rank-at-most-one blocks, mixed imbalance, hole propagation, and
differently labelled packet incidence.

Latest U1 cap refinement:
[the coordinate-monomial common-power obstruction](invertible-monomial-base-locus-common-power-obstruction.md)
closes the formal six-site base-locus escape left by the invertible-monomial
nine-cap classification.  For three disjoint missing pairs, the equations
\(F=q^{[2]}\) and \(q^{[3]}=0\) kill the three within-pair blocks; crossed
four-site coefficients then force one local line to be two distinct colour
axes.  Retaining all nine products for arbitrary ordered missing pairs leaves
only that matching type and a directed two-edge path plus one disjoint edge;
seven literal four-support equations exclude the latter.  The
[independent line audit](invertible-monomial-base-locus-common-power-obstruction-independent-audit.md)
reconstructs every tensor inference and exhausts all \(30^3=27{,}000\)
labelled directed triples, finding exactly 720 disjoint and 4,320
path-plus-edge solutions to the product table.  This closes only the
coordinate-monomial six-site submodel.  The next theorem removes the
multi-site star-row restriction; larger multi-term target lifts and the
global U1 descent remain open.

[The arbitrary-star monomial obstruction](arbitrary-star-monomial-base-locus-common-power-obstruction.md)
removes the coordinate-support hypothesis from all six response rows.  The
rows may be supported on any sites and may have arbitrary local components,
dependencies, degeneracies, and cancellations.  The literal nine-product
equations first exclude every repeated missing-pair triple.  Among the
remaining \(15^3\) colour-indexed triples, a complete graph census and three
unsaturated characteristic-zero unit ideals leave only \(3K_2\) and
\(P_3+K_2\); the common-power equations exclude both by tensor arguments
that no longer involve the response rows.  The
[independent clean-room audit](arbitrary-star-monomial-base-locus-common-power-obstruction-independent-audit.md)
reconstructs all 3,375 triples, both positive response witnesses, the three
impossible graph ideals under different orderings, and the common-power
proofs.  Thus the exact model with one pure four-site monomial lift per
target colour is closed.  A genuine multi-term target lift and the global
U1 descent remain open.

[The distinct-pair power-only obstruction](distinct-missing-pair-common-power-obstruction.md)
removes the response rows entirely when the three pure lifts have distinct
missing pairs.  From \(q^{[2]}=F\) and \(q^{[3]}=0\), the identity
\(qF=0\) kills the three missing-pair blocks.  The five possible support
graphs are then exhausted: the earlier \(3K_2\) and \(P_3+K_2\) arguments
combine with new arbitrary-tensor proofs for \(P_4,K_{1,3},K_3\).  The
[independent line audit](distinct-missing-pair-common-power-obstruction-independent-audit.md)
reconstructs every propagation and crossing argument, makes the star
contraction an explicit square-zero algebra map, checks all eight scalar
zero patterns, and verifies exact elimination syzygies.  Thus, in the
single-monomial model, the nine products are needed only to eliminate
repeated missing pairs; the exact repeated-pair \(K_4\) construction shows
that this qualification is sharp.  Larger multi-term lifts remain open.

[The first multi-term obstruction](one-multiterm-monomial-common-power-obstruction.md)
allows two distinct pure four-site lifts in one target colour and one in
each of the other two, with arbitrary nonzero complex weights and arbitrary
multi-site response rows.  The literal products force all four missing
pairs to be distinct.  A target-preserving diagonal automorphism normalizes
the weights, and \(qF=0\) has a complete 100- or 102-dimensional kernel
according as the same-colour pairs are disjoint or adjacent.  All 16,380
labelled supports form 25 symmetry orbits, and every full unsaturated
characteristic-zero ideal for \(q^{[2]}=F\) is unit.  The
[independent clean-room audit](one-multiterm-monomial-common-power-obstruction-independent-audit.md)
uses different representatives, variable order, matching order, coefficient
stream, and kernel elimination, and again obtains all 25 unit ideals with
separate frozen ledgers.  This closes exactly the multiplicity profile
\((2,1,1)\); larger or non-pure lifts and the global U1 descent remain open.

[The three-term-in-one-colour obstruction](three-term-monomial-common-power-obstruction.md)
next closes the pure multiplicity profile \((3,1,1)\).  The products force
all five missing pairs to be distinct.  The weighted equation \(qF=0\) is
the full vertex-incidence kernel of the three-edge same-colour support graph;
all five graph shapes have exact full kernel dimension between 92 and 98,
and a local diagonal torus normalizes every nonzero weight, including the
apparent \(3K_2\) square-root case.  The 60,060 labelled supports form 70
exact orbits, and every complete unsaturated characteristic-zero ideal is
unit.  The
[independent clean-room audit](three-term-monomial-common-power-obstruction-independent-audit.md)
uses reversed representatives and a different kernel/generator stream,
documents and invalidates an early duplicated-matching bug, structurally
guards all three four-site matchings, and independently obtains all 70 unit
ideals.  This closes \((3,1,1)\), not \((2,2,1)\), larger profiles,
non-pure lifts, or the global descent.

[The uniform pure-lift obstruction](uniform-pure-lift-private-edge-degeneration.md)
subsumes every finite pure multiplicity profile.  After aggregating equal
colour/pair coefficients, the literal diagonal responses force each colour
to have an active missing pair used by no other colour.  A unital local
square-zero algebra projection kills every nonselected pure lift and retains
exactly those three private lifts.  Their pairs are distinct, so the
independently audited power-only theorem gives a contradiction.  This treats
all 45 pure coefficients simultaneously, with arbitrary support, repeated
pairs, complex cancellation, multi-site rows, and arbitrary endpoint-ordered
blocks of the common quadratic.  The
[independent clean-room audit](uniform-pure-lift-private-edge-degeneration-independent-audit.md)
reconstructs 20,250 response-provenance terms, all 2,730 ordered private-pair
triples, functoriality of the projection, exact parallel aggregation, and the
sharp repeated-pair \(K_4\) witness.  The remaining common-power frontier is
therefore the genuinely non-pure four-site component, not another pure
multiplicity profile; the global U1 descent is still open.

[The scalar common-origin rank countermodel](common-origin-factorization-rank-countermodel.md)
closes a tempting but false continuation into the non-pure branch.  On a
weighted six-cycle it has \(q^{[3]}=0\) while the scalar hafnian-cofactor
matrix has determinant \(-256\); explicit rational rows satisfy
\(p_i s_jq^{[2]}=\delta_{ij}z_U\), and therefore
\((p_iq)(s_jq)=2\delta_{ij}z_U\), for all nine pairs.  The symbolic family
has \(\det C=-(ace-bdf)^4\) on
\(\operatorname{haf}(q)=ace+bdf=0\).  The
[independent audit](common-origin-factorization-rank-countermodel-independent-audit.md)
reconstructs the reverse-order cofactor block, all 18 products, and all
6,840 separate independent-target support factorizations.  This is not a
Krenn counterexample because its top-degree target space is one-dimensional.
It proves that a non-pure obstruction cannot scalarize the three \(X_i\) or
rely on catalecticant rank alone; their distinct local axes must be retained.

[The one-/two-line-field response obstruction](single-line-field-nonpure-response-obstruction.md)
is the first support-independent theorem in that genuinely non-pure branch.
If the four-site multiplier resolves into at most two coherent local line
fields, the three diagonal responses are impossible: quotient incidence
forces a partition by three omission pairs, an omission-pair quotient puts a
four-site target on a two-point Segre secant, and secant rigidity plus
pigeonhole gives the contradiction.  With three line fields forming a basis
at every site, the same argument gives a sharp residual normal form: after a
global permutation, target colour \(i\) agrees with field \(i\) at at least
four sites.  Under all nine responses the three radius-two modules then split
as a direct sum, so only their common-power coupling remains.  The
[independent clean-room audit](single-line-field-nonpure-response-obstruction-independent-audit.md)
reconstructs all 90 incidence cases, 3,100 finite-field secant flattenings,
all 117,649 frame-support boxes, and the 219-dimensional direct-sum word
space.  This does not classify three-field deviations or general higher-rank
edge blocks, and it is not an all-even descent.

[The sitewise common-power response filtration](sitewise-common-power-response-filtration.md)
adds a cancellation-safe endpoint-rank invariant for arbitrary edge blocks.
If \(W_u\) is the span of all incident endpoint directions at site \(u\),
each target axis lies in at least four of the six \(W_u\)'s and the three
incidence sets cover every site.  On the boundary \(\dim W_u\le2\), the six
spaces are forced to be the three coordinate planes, each omitted on one of
three disjoint site pairs; the single-colour part of \(q^{[2]}\) is then the
corresponding three pure four-site lifts, while mixed-colour terms remain.
The
[independent clean-room audit](sitewise-common-power-response-filtration-independent-audit.md)
reconstructs all 1,420 ordered Cauchy--Binet terms, the 120 complementary
leading terms, all 90 plane assignments, arbitrary-rank block/chain tests,
and the exact scalar-cycle sharpness model.  It confirms that no individual
minor or matching term has been selected from a cancelling sum.  Local rank at
least three and the mixed four-site packet remain open, so this is a six-site
filtration rather than a uniform descent.

[The coordinate-plane mixed-packet obstruction](coordinate-plane-mixed-packet-obstruction.md)
closes the entire equality boundary left by that filtration.  Double
quotients at the three omission pairs force the complete four-site hole
slices—not only their monochromatic coefficients—to be pure.  Nonzero mixed
holes then carry zero response matrices.  Pure-\(K_4\) apex rigidity excludes
every disconnected mixed-cofactor graph, while connectivity propagates all
row vectors to fixed lines and makes the three diagonal response units
proportional.  The
[independent clean-room audit](coordinate-plane-mixed-packet-obstruction-independent-audit.md)
rebuilds the four-site annihilator strata, all \(3+3\) and \(2+2+2\)
partitions, the \(2+4\) response argument, and the full graph frontier.
Thus any six-site common-power response has \(\dim W_u\ge3\) at some site,
equivalently rank three after projecting every local space to its target
three-space.
The obstruction retains arbitrary plane-valued endpoint blocks, multi-site
rows, and complex cancellation, and does not even use \(q^{[3]}=0\); it is
still a six-site structural theorem, not the missing all-even descent.

[The full-rank-site response frontier](full-rank-site-response-invisibility-countermodel.md),
independently reconstructed in
[its clean-room audit](full-rank-site-response-invisibility-countermodel-independent-audit.md),
shows exactly what cannot finish the other side.  Rational one- and
two-separated-target-site models have \(q^{[3]}=0\), all nine diagonal
responses, a generically invertible cofactor form, and incident rank three at
one site, yet the other incident spaces stay one-dimensional.  They violate
the global four-cover rank budget and are not Krenn counterexamples, but they
exclude any proof using only one- or two-site determinant, adjugate, cofactor,
or chain data.  Positively, every genuine response has
\(\sum_u\dim W_u\ge12\).  At equality with a rank-three site, only the rank
profiles \((1,4,1),(2,2,2),(3,0,3)\) occur.  Double quotients make the three
omission pairs distinct and purify their complete missing-pair slices,
leaving exactly the wedge-plus-disjoint, three-edge-path, and triangle
overlap geometries.  Rank budget above twelve and those three exact equality
geometries were the resulting frontier.

The independently reconstructed
[path/triangle exposed-grid obstruction](rank-budget-path-triangle-exposed-grid-obstruction.md)
uses the complete typed coordinates of those same quotient tensors.  A
crossed-target lemma forces the endpoint response points of adjacent target
grids to be pure of alternating types; one remaining zero corner then
contradicts both the three-edge path and the triangle.  The
[clean-room audit](rank-budget-path-triangle-exposed-grid-obstruction-independent-audit.md)
re-derives the quotient from all nine responses, checks every mixed and
half-zero branch, and obtains both contradictions by a different parity
system.  It also constructs all four exact rational solutions of the
wedge-plus-disjoint *quotient grid*, so it does not overclaim a wedge
obstruction.

The remaining geometry is now closed by the
[unconditional wedge hole-block obstruction](wedge-equality-hole-block-resolution.md)
and its independent
[clean-room audit](wedge-equality-hole-block-resolution-independent-audit.md).
The typed grids first force five complete cofactor zeros without assuming
any support for \(q\).  The rank-one-site cubic then allows at most one of
\(q_{ab},q_{bc}\); both single-survivor branches contradict exact quotient
coefficients, and after both vanish a twelve-component tensor syzygy forces
the nonzero \(F_{bc}\) target to be zero.  The third hole block \(q_{de}\)
remains arbitrary throughout.  Thus every rank-budget-twelve equality
geometry having a rank-three site is impossible.  Rank budget strictly
above twelve is the sole residual of this arbitrary-block budget route.

[The aligned three-field common-power obstruction](aligned-three-field-common-power-obstruction.md)
then couples the three radius-two modules to the actual power equations.  It
proves that every target colour has a hard zero on its assigned field, that
the all-two-site-deviation branch is supported on only two physical pairs,
and that every sitewise coordinate-permutation residual is impossible.  The
[independent adversarial audit](aligned-three-field-common-power-obstruction-independent-audit.md)
rechecks the unital power projection, 16,203 capped Hall systems, the
shared-pair rank obstruction, and all 462 permutation assignments.  The
remaining aligned branch requires genuine linear mixtures at hard-zero
sites; it is neither a complete non-pure classification nor an all-even
descent.

[The two-pair six-term common-power obstruction](two-pair-six-term-common-power-obstruction.md)
closes that residual and strengthens the Hall reduction.  No SDR together
with the singleton-response collision forces every aligned solution—not only
the all-two-deviation chart—onto exactly two physical pairs, with support
profile \((2,1,1)\), \((2,2,1)\), or \((2,2,2)\).  The first dies directly in
the split response modules.  For the latter profiles, exact \(qF=0\) has
rank 18 and kills both active pair blocks; all adjacent and disjoint
unsaturated \(q^{[2]}-F\) ideals are unit over \(\mathbb Q\).  The
[independent clean-room audit](two-pair-six-term-common-power-obstruction-independent-audit.md)
uses different site, colour, variable, equation, and monomial orders and
reconstructs all six unit ideals, the 117-dimensional residual coordinate
space, and the universal profile census.  Hence the full locally
basis-forming aligned three-field branch is impossible, including genuine
hard-zero mixtures.  The following sole-defect analysis now closes exactly
one deficient local frame; two-or-more deficient frames, arbitrary
non-line-field multipliers, and the all-even descent remain open.

[The degenerate three-line-field response normal form](degenerate-three-line-field-response-normal-form.md),
with a separate
[finite and symbolic reconstruction](degenerate-three-line-field-response-normal-form-independent-audit.md),
now resolves the first layer of that degeneracy without changing the response
rows or targets.  If every local field span has dimension at most two, the
coordinate-plane theorem applies after projecting only \(q\), so that branch is
empty.  With exactly one deficient site, the other five independent frames
force every target box to be axial or a unique binary bridge; exact boundary
words then force the active-pair families, singleton collisions, and the
complete layer-Hall alternatives.  The independent checker exhausts all
759,375 ordered boxes, the \(6,093+423\) axial/bridge split, all 250,047
layer-Hall systems, and the sharp \(141/110\) bridge census.  It does not cover
two deficient sites.

Two independently audited common-power theorems first narrow the sole-defect
branch.  [The distinct-lift obstruction](sole-defect-distinct-lift-common-power-obstruction.md)
proves that three distinct active pairs cannot be chosen with a locally
separable bad-site selector; its
[clean-room audit](sole-defect-distinct-lift-common-power-obstruction-independent-audit.md)
reconstructs 52 unsaturated unit ideals while retaining every \(q\)-coordinate
and explicitly handles selector-killed unused field vectors by nonzero
dummies.  [The two-pair obstruction](sole-defect-two-pair-common-power-obstruction.md)
and its
[independent audit](sole-defect-two-pair-common-power-obstruction-independent-audit.md)
prove that Hall failure is impossible: all 105 coefficient normalizations
have a unimodular good-site minor, and all 65 exact two-pair ideals are unit
over \(\mathbb Q\).  Consequently a surviving sole-defect response must have
an ordinary SDR.  [The nonseparable-packet obstruction](sole-defect-nonseparable-packet-common-power-obstruction.md),
with an independent [clean-room audit](sole-defect-nonseparable-packet-common-power-obstruction-independent-audit.md),
then exhausts the remaining bad-site matroid patterns.  Its orbit census is
\(1284\to157=145+12\): all 145 coefficient-normalizable rational ideals are
unit, and all twelve full-packet ideals are unit over
\(\mathbb Q[\mu,\mu^{-1}]\), with elimination inverting only rational units
and powers of \(\mu\).  Thus the entire exactly-one-deficient-site branch is
empty.  The remaining coherent three-line-field frontier has two through
five deficient sites and at least one full local frame; the all-six-deficient
case is already closed by the coordinate-plane obstruction.

The first exactly-two-defect layer now retains the information which the
four-good-site box projection loses.  The independently audited
[balanced-word coupling](two-deficient-balanced-word-coupling.md) proves
that every supported \(2+2\) field word puts the target tensor on the two
bad sites in the Segre line spanned by the corresponding two coherent field
tensors.  Its
[clean-room reconstruction](two-deficient-balanced-word-coupling-independent-audit.md)
checks all \(15^4=50,625\) good-site support boxes: 6,625 are response-valid,
and the 492 nonaxial balanced-free boxes form exactly ten
\(S_4\times S_3\)-orbits.  Exact uniquely centred boundary words then give
the sharper
[double-bad-site coincidence theorem](two-deficient-exceptional-boundary-word-coincidence.md):
every exceptional orbit forces the same pair of field lines to coincide at
both deficient sites.  The remaining two-defect cases are the axial boxes,
the intersections of the balanced-word Segre constraints, and these
double-coincidence strata.  This is a response-level reduction, not yet a
common-power contradiction or an all-even descent.

[The mixed-endpoint one-site support frontier](mixed-endpoint-one-site-support-frontier.md)
keeps all 135 endpoint-ordered coordinate cells and exact \(q^{[2]}\),
\(q^{[3]}\) support consequences while restricting the six response rows to
one-site coordinate axes.  Its 27,000 directed-row triples reduce to two
compatible geometries.  The subsequent
[exact Laurent closure](mixed-endpoint-one-site-laurent-closure.md)
uses sign-lattice certificates and third-term-aware CEGAR cuts to prove that
path--edge rows need at least 33 active aggregate cells and matching rows
need at least 34.  A
[clean-room independent audit](mixed-endpoint-one-site-laurent-closure-independent-audit.md)
rebuilds the 17 row orbits, Boolean coefficient formulae, exact HNF
relations, and final UNSAT bounds with different cut ledgers and a second SAT
engine.  These are cancellation-safe sparse lower bounds, not existence at
the thresholds; they do not cover multi-site rows or non-coordinate blocks
and therefore carry falsification rather than global-closure credit.

[The projective-height cap obstruction](cap-condition-projective-height-obstruction.md),
independently checked in a
[clean-room audit](cap-condition-projective-height-obstruction-independent-audit.md),
closes the dimension-only cap-selection proposal.  The cubic clean-cap
condition always contains the large forbidden linear locus
\(\ker(s,C_2)\).  More sharply, an exact abstract GHZ-compatible signature
has ideal \((s^2\kappa_0,s^2\kappa_1,s^2\kappa_2)\), whose saturation by
\(s\kappa_0\kappa_1\kappa_2\) is the unit ideal.  This is explicitly not
a realizable common-edge source; it proves that height and top GHZ alone
cannot select a cap.  A positive continuation must establish proper
saturation from nonlinear shared-edge identities.

[The actual-cofactor cap cubic](actual-cofactor-cap-cubic-and-four-parameter-prism-barrier.md),
with an independent
[clean-room audit](actual-cofactor-cap-cubic-and-four-parameter-prism-barrier-independent-audit.md),
identifies the exact source discrepancy
\({\cal D}_{\rm src}=6(s^2F_U^K-H_6(A^K))\) and closes a stronger
one-slice shortcut.  A genuine ten-site common-edge family has a
four-dimensional cap subspace with independent
\(s,\kappa_0,\kappa_1,\kappa_2\) and exact diagonal top contractions,
but its cofactor prism has mixed ideal \((z_0z_1z_2)\) and unit active
saturation.  The source is not globally GHZ: eight of its nine top words
are mixed.  Thus common-edge realizability and exact GHZ contraction on
one active cap subspace are still insufficient; a positive theorem must
use transverse/all-cap equations supplied by the full large-source target.

[The maximal transverse prism cap-slice countermodel](maximal-transverse-prism-cap-slice-countermodel.md),
with an independent
[clean-room audit](maximal-transverse-prism-cap-slice-countermodel-independent-audit.md),
shows that ambient cap dimension does not repair this failure.  A genuine
ten-site common-edge family has top cap-map rank nine; its unique maximal
diagonal-image and literal-GHZ-compatible slices have dimensions \(75\)
and \(73\), yet both retain exactly the four-parameter prism and its unit
active saturation.  The effective top-plus-cofactor rank on the latter
slice is only four, with a \(69\)-dimensional common kernel.  The induced
cap-adjugate identity detects all six omitted off-diagonal rows, while two
further rows are diagonal relocations across the extra capped sites.  The
model is not globally GHZ and does not obstruct a theorem using effective
lower transverse directions.  It rules out cap-count or ambient-codimension
arguments and makes cancellation of those eight transverse rows, with a
simultaneous change of the lower cofactor determinant, the exact remaining
prism-extension test.

[The exact shared pair-cap countermodel](polarized-eight-site-shared-pair-cap-countermodel.md),
with a separate
[clean-room audit](polarized-eight-site-shared-pair-cap-countermodel-independent-audit.md),
sharpens the isolated-equation boundary in the opposite direction.  Its
twelve-cell quadratic and a genuine global product satisfy
\(z=\tfrac14q+4ps\) and \(zq^{[3]}=\Delta_{8,3}\) over \(\mathbb Q\).
Thus even the literal low-rank pair-cap form is consistent for one aggregate
row.  The same \(q\) cannot satisfy all nine shared-row equations: 358
singleton response rows expose every one of the 240 inactive cells, after
which the twelve active responses collapse to one rank-one line and contradict
a rank-two target difference.  This full-nine obstruction is exactly the
already registered pair-suspension theorem after a decorated relabeling, not
a new mechanism.  The independently verified overlapping-pair substitutions
have target factors four in polarized form and one in raw matching form.
The later [pair-slice exchange theorem](ten-site-overlapping-pair-exchange-redundancy.md),
with an independent
[clean-room audit](ten-site-overlapping-pair-exchange-redundancy-independent-audit.md),
shows that a second *complete* nine-row tensor system adds no equations:
both pair charts are reindexings of the same full top-tensor residual ideal.
The overlap chart may aid elimination or a projected subsystem, but it is not
an independent filter.

[The uniform full-nine target-incidence invariant](uniform-full-nine-target-incidence-invariant.md),
with an independent
[clean-room audit](uniform-full-nine-target-incidence-invariant-independent-audit.md),
is a new cancellation-safe incidence consequence of that complete system
which is uniform in the boundary order.  On a boundary of size \(2m\), each
target axis occurs in the aggregate internal endpoint span at at least
\(2m-2\) sites, every site contains some target axis, and the incidence
counts obey \(n_3\ge n_1+2m-6\).  Thus every deleted pair in an
\(N\)-site hypothetical source exposes at least \(N-8\) target-full internal
sites.  This incidence statement is strictly weaker than blockwise nonzero
rows and does not itself select a pair or trigger the registered
source-Hessian obstruction.  Pair selection is supplied more sharply and
for every allowed order by the target-flattening theorem below; the
full-nine theorem's distinct value is its target-full internal-site supply.

[The target-flattening essential-star theorem](target-flattening-essential-star-pair-bound.md),
with an independent
[clean-room audit](target-flattening-essential-star-pair-bound-independent-audit.md),
strictly sharpens the pair selection without using the full-nine incidence
ledger.  At any endpoint, at most three neighbor mode-support subspaces are
essential under deletion.  Hence every even \(N\ge8\) has at least
\(N(N-7)/2\) pairs with injective aggregate stars at both endpoints and a
common-endpoint fan of degree at least \(N-7\).  The bad-pair graph is
\(4\)-degenerate, so the good graph contains a clique of size at least
\(\lceil N/5\rceil\), including six mutually good sites for \(N\ge26\).
The three-essential equality case is exactly a cubic rank-one selector;
aggregate injectivity still does not imply a rank-three block or blockwise
nonzero rows.

[The injective-star/Hessian bridge frontier](injective-star-hessian-bridge-frontier.md),
independently reconstructed in
[its clean-room audit](injective-star-hessian-bridge-frontier-independent-audit.md),
then determines what those good pairs buy.  On a gauge-rigid chart,
connectedness forces a localized missing row, while connected
nonbipartiteness forces all six nonzero global rows onto at most two sites
each.  An exact binary target shows aggregate injection cannot select a
clean cap without genuinely ternary input.  A normalized rational
fourteen-site family has all \(91\) pairs doubly injective but every internal
rank-three graph disconnected and every star locally row-deficient; its
mixed coefficient \(4/29\) is nonzero, so it is not a Krenn counterexample.
Thus ranks, zero masks, pure normalization, and exchange reindexing alone
stop exactly before the mixed GHZ equations.

[The good-pair fan six-port reduction](good-pair-fan-six-port-triple-cofactor-reduction.md),
with an independent
[clean-room audit](good-pair-fan-six-port-triple-cofactor-reduction-independent-audit.md),
turns that mixed-equation gate into a finite physical interface.  For
\(N\ge16\), either at least \(N-15\) good fan pairs lie in the
extra-kernel/disconnected/bipartite escape charts, or nine regular pairs
force three literal zero-block neighbours and sparse rows on at most six
ports.  For \(N\ge24\), either at least \(N-23\) pairs escape or the three
neighbours can be chosen pairwise good.  Each zero-neighbour pair obeys
the exact 27-row identity
\(p_c(b_{de}q^{[m-2]}+s_dt_e q^{[m-3]})=
\delta_{c=d=e}X_c\), and capping outside the six centre ports is
cancellation-safe.  The abstract response table has an exact three-port
model, so at this intermediate stage the gate was simultaneous common-\(q\)
and common physical-cofactor compatibility across the three pairs.  The
later simultaneous exclusion retires this regular branch.

[The induced-zero-shore hierarchy](good-pair-fan-induced-zero-four-cut-reduction.md),
with an independent
[clean-room audit](good-pair-fan-induced-zero-four-cut-reduction-independent-audit.md),
sharpens the regular fan branch further.  For every \(k\ge1\) and even
\(N\ge7k+7\), either at least \(N-7k-6\) fan pairs occupy the three
Hessian escape charts or there is a shore of \(h=k+1\) sparse injective
vertices whose every internal aggregate block is zero.  Its complete
source identity is
\((\prod_jp^{(j)}_{c_j})q^{[m-h]}=
\delta_{c_0=\cdots=c_{h-1}}X_{c_0}\).  The first new case gives a literal
zero \(K_4\) at \(N\ge28\), unless at least \(N-27\) pairs escape.  A
cancellation-safe hole-sector cap reduces a fixed \(h\) shore to at most
\(6h\) physical ports, hence the zero-\(K_4\) branch to 81 equations on at
most 24 ports.  The capped tensor is a projection of the one common
matching power, not automatically a new matching power; that provenance
was the remaining obstruction target for this intermediate regular branch.

[The twelve-port capped-table countermodel](zero-shore-four-cut-capped-table-countermodel.md),
with an independent
[clean-room audit](zero-shore-four-cut-capped-table-countermodel-independent-audit.md),
proves that the capped interface itself is sharp.  Three disjoint four-hole
sets, twelve one-site coordinate rows, four injective frames, and one
degree-eight response tensor satisfy all 81 rows exactly (three unit
diagonals and 78 literal zeros).  No common quadratic lift is supplied, so
this is not a target source.  A complete \(11!!=10{,}395\) audit excludes
the narrow lift in which the quadratic is supported on one fixed perfect
matching; arbitrary block graphs, complex cancellation, and caps of a
larger common power were not addressed there.  Thus physical common-power
provenance, not the abstract 24-port table, was the exact intermediate
gate; the later simultaneous exclusion retires the entire regular branch.

[The complete-bipartite all-pair escape countermodel](complete-bipartite-all-pair-hessian-escape-countermodel.md),
independently reconstructed in
[its clean-room audit](complete-bipartite-all-pair-hessian-escape-countermodel-independent-audit.md),
shows why the escape half cannot be closed by density or shared charts
alone.  For every \(N=2s\ge6\), one actual \(K_{s,s}\) aggregate source
has every pair doubly injective, every pair-deleted rank-three graph
connected bipartite, vertex connectivity \(s\), literal common-source
cofactor factorizations, and all three pure coefficients normalized to one.
It is not GHZ: a fixed off-diagonal mixed coefficient is
\(2^{s-1}\ne0\).  Thus a viable escape-chart theorem must insert mixed
GHZ vanishing before graph/Hessian counting; more overlapping charts or
pure normalization cannot suffice.

[The fan six-port simultaneous exclusion](good-pair-fan-six-port-simultaneous-exclusion.md)
now closes that gate by emptying its hypothesis: on any regular
nonbipartite pair chart of an exact ternary source, the nine
pair-contraction equations force every \(p_c\) one-site through the
annihilator trichotomy (support \(\ge3/2/1\) gives annihilator dimension
\(0/1/3\)), collapse all six mixed rows into one site factor, and then
contradict the three diagonal cofactor identities.  Hence no good pair is
regular nonbipartite, both deleted star triples are dependent, and the
three six-port response tables — pairwise equivalent through the shared
81-row four-slot origin — have no simultaneous or single physical
realization.  The fan dichotomy becomes threshold-free: for every even
\(N\ge8\), all \(\ge N-7\) fan pairs lie in the
extra-kernel/disconnected-or-nonspanning/bipartite-with-missing-row
escape charts, and bridge-frontier stratum 4 is empty.  The
[independent clean-room audit](good-pair-fan-six-port-simultaneous-exclusion-independent-audit.md)
reconstructs everything with scattered vertex labels, different deleted
pairs, a different prime, and reversed Singular orders (92 checks), and
its adversarial charts inside the hypotheses all collapse as predicted.
The abstract 81-row system without regular provenance is not excluded and
no longer needs to be.  At this stage the descent had to come from the
physical escape charts; the following theorems reduce those charts to E1
and E2.

[The escape-chart descent theorem](good-pair-fan-escape-chart-descent-theorem.md)
then empties defect zero, connected bipartite, isolated-vertex, and
single-edge defect-one charts.  Its order-ten supplement closes the sole
remaining \(|W|=8\) pattern family: all 24
\(K_{1,3}\sqcup K_4\) windows have a centre/third-leaf deletion for which
two retained leaves share one possible mate, so the complementary
six-site matching power is zero.  The resulting nine-dimensional block
kernel is disjoint from the seven-dimensional gauge space.  The primary
28-check replay and the project-independent clean-room reconstruction both
pass exactly.  Consequently every good pair at \(N=8\) or \(N=10\) lies in
the extra-kernel or defect-at-least-two charts.
[The four-port balance theorem](good-pair-defect-one-four-port-elimination.md),
with its
[independent audit](good-pair-defect-one-four-port-elimination-independent-audit.md),
now removes the order restriction: pair-complement activity plus one
physical four-port defect window excludes every larger disconnected
defect-one component as well.  Hence all good pairs at every even
\(N\ge8\) lie in exactly the extra-kernel or defect-at-least-two charts.

[The distinguished-span-two E1 theorem](extra-kernel-distinguished-span-two-closure.md),
with an
[independent audit](extra-kernel-distinguished-span-two-closure-independent-audit.md),
converts the dense equality case inside the connected spanning nonbipartite
E1 stratum.  If all six deleted-star rows reach at least three sites and
the six distinguished off-diagonal classes span a two-plane, a live-edge
relation propagates to a literal zero-star site.  Every direct block then
admits a same-support bilinear zero, producing a pure three-cross selector.
Within this graph stratum, the residuals are a star row supported on at
most two sites or distinguished span at least three.  E1 charts with a
disconnected, nonspanning, or bipartite rank-three graph remain separate
residuals.  The positive export must retain all 27 common-complement
equations across overlapping zero-star triples, including the direct-block
term and common triple-star power.

[The overlapping zero-star four-cut exchange](overlapping-zero-star-four-cut-exchange.md),
with its
[independent audit](overlapping-zero-star-four-cut-exchange-independent-audit.md),
shows that two such 27-packets are coefficient regradings of one exact
81-row identity, not independent constraints.  A six-site repeated-pair
\(K_4\) model satisfies the five selector-contracted row/column caps.
[The uncontracted two-dark-colour theorem](uncontracted-four-cut-two-dark-colour-obstruction.md),
with its
[independent reconstruction](uncontracted-four-cut-two-dark-colour-obstruction-independent-audit.md),
now proves that this model cannot extend to the full system: two diagonal
target rows and one mixed target-zero row imply that each zero-star pair
has at most one vanishing diagonal star product.  This is uniform in the
common complement and all powers.  The remaining dense four-cut case has
at least two live diagonal products in each star pair.

[The isotropic dressed-cap theorem](uncontracted-four-cut-isotropic-dressed-cap.md),
with an
[independent reconstruction](uncontracted-four-cut-isotropic-dressed-cap-independent-audit.md),
then contracts one direct block without discarding the other.  All nine
opposite colour rows share the multiplier
\(t(\alpha)v(\beta)z^{[m-4]}\) and retain the dressed direct terms
\(x_ay_b+a_{ab}z/(m-3)\).  A Laurent-unit classification makes this packet
ternary unless the contracted block is a scalar matrix unit, when it is
binary.  The
[four-site coordinate-monomial multiplier theorem](four-site-coordinate-monomial-dressed-packet-obstruction.md)
excludes the ternary \(m=4\) packet whenever both contracted multiplier
rows are sitewise coordinate monomials, with arbitrary weights.  The
[scalar-unit full-isotropic-packet guard](uncontracted-four-cut-scalar-unit-full-isotropic-packet-guard.md)
shows in the other direction that all isotropic packets at \(m=5\) can
coexist with \(z^{[2]}\ne0\), core-dense injective opposite rows, and nonzero
diagonal products.  That guard has an empty rank-three internal graph and
does not satisfy the complete four-cut identity.  No registered theorem
currently handles arbitrary local superpositions/higher powers or couples
the exceptional scalar-unit row to the full E1 provenance.

[The centered E2 stability theorem](centered-defect-stability.md), with an
[independent audit](centered-defect-stability-independent-audit.md),
supplies a uniform graph reduction for the other chart.  A graph on
\(n\ge7\) vertices with \(b(H)\le1\), minimum degree at least three, and
at least \(n-6\) deletion defects has at least seven safe vertices, a
contradiction.  Thus a good fan centered at \(r\) gives
\(b(R-r)\ge2\), \(\delta(R-r)\le2\), or an E1 pair.  The theorem is
sharp and leaves exactly two tensor exports: synchronize defect coefficient
vectors across overlapping charts when \(b(R-r)\ge2\), or exploit the
centered low-degree site when \(\delta(R-r)\le2\), allowing its possible
rank-three edge to \(r\).

[The faithful defect-coefficient theorem](defect-coefficient-rank-and-two-defect-sparsity.md),
with an
[independent reconstruction](defect-coefficient-rank-and-two-defect-sparsity-independent-audit.md),
sharpens the first export.  Gauge rigidity makes every defect expansion
unique.  A defect-two good chart has a star row supported on at most two
sites; if a defect-three chart is fully dense, its coefficient vectors span
the entire defect space.  A five-site common-restriction relaxation allows
unrelated coefficient vectors, but a pairwise-distinct row of the complete
overlap system has exact residual \(-6\).  Thus common center/quadratic data
alone cannot synchronize the charts; the direct blocks and full 27 rows are
essential.

[The defect-two fan propagation theorem](defect-two-fan-sparsity-propagation.md)
globalizes the sparse-row conclusion.  Either the fan center has
rank-three degree at most two, or all but at most nine exact-defect-two
endpoints have degree at most two off the center.  Hence under the two
degree-at-least-three hypotheses, at most nine fan charts have defect two
and at least \(N-16\) have defect at least three.  A globally sparse center
row becomes one synchronized factorized nine-row overlap packet for every
outside endpoint pair.  Its exact selected-row realization shows that the
remaining eighteen triple rows, pair diagonals, or Hessian data are
essential.

[The centered low-degree rank tradeoff](centered-low-degree-rank-tradeoff.md),
independently checked in
[its audit](centered-low-degree-rank-tradeoff-independent-audit.md),
sharpens the latter branch.  With \(A_{rx}\) invertible, a rank-two spoke
and rank-at-least-two \(A_{ux}\) force all six opposite endpoint rows to
zero.  Exact rank-one-star and rank-one-spoke witnesses show both thresholds
are sharp; local off-diagonal row counting cannot close the residual gate.

[The centered rank-one overlap-packet theorem](centered-rank-one-overlap-packet.md),
with an
[independent reconstruction](centered-rank-one-overlap-packet-independent-audit.md),
uses the complete 27 rows on the specific sharp witness.  They contract to
four common cofactors with an exact \(N=8\) common-\(q\) relaxation, but none
of the 24 minimal three-private-coordinate packets has a shared-star lift,
even modulo \(\operatorname{Ann}(q)\).  This closes only that minimal
stratum.  Extra-cell, non-coordinate or multisite, common-annihilator,
cancellation-rich, higher-power, and other rank-one masks remain open.

[The two-star pure-response theorem](centered-rank-one-two-star-pure-response-obstruction.md)
removes those support restrictions for one graph export.  A pure response
\(aG=X\ne0\) together with \(bG=0\) forces a site where the two local rows
are dependent; the unique-site case also places the target factor on that
line.  Applying the lemma to both colour slices of the sharp packet forces
at least two additional singular blocks at `y`, with arbitrary cells and
cancellation.  Thus \(\deg_R(y)\le2\) at \(N=8\), and more generally
\(\deg_R(y)\le N-6\).  The higher-order equality stratum and other rank-one
orbits remain open.

[The cubic leave-one-anchor nullity web](cubic-vertex-leave-one-anchor-nullity-web.md),
independently reconstructed in
[its clean-room audit](cubic-vertex-leave-one-anchor-nullity-web-independent-audit.md),
controls the sharp three-essential equality branch.  For every nonneighbour
\(q\) of a cubic vertex, all three leave-one-anchor cofactor maps are
singular and at least two have nullity at least two; their minimum nullity
profile is \((1,2,2)\).  The proof uses the two wrong-colour rows and the
shared double-deletion cofactors, with no genericity or noncancellation
assumption.  Cubicity is only forced on the three-essential stratum, and
the nullity web does not yet turn an extra kernel direction into a clean
cap or a descent.

[The cubic common-cofactor-zero boundary](cubic-nullity-common-cofactor-zero-boundary.md),
with an independent
[clean-room audit](cubic-nullity-common-cofactor-zero-boundary-independent-audit.md),
classifies what happens when two nonneighbours are compared.  For a fixed
anchor colour, a local three-port lies in the leave-one-anchor kernel
exactly when the shared complete cofactor \(P_c\) vanishes; when
\(P_c\ne0\), restriction to the common exterior star is faithful.  A
dense all-even cancellation family has \(P_c=0\), every lower double
cofactor nonzero, and the two kernels equal the two opposite local
three-ports, so raw nullity has no common-star direction.  That family
fails every cubic pure-cofactor equation and is not a target source.  The
surviving target input is the exact nine-equation pure two-crossing Hessian
system, including the physical direct-block transpose compatibility.

[The fixed-nine-cell pair-cap obstruction](polarized-eight-site-fixed-q-pair-cap-obstruction.md)
strengthens the unrestricted polarized countermodel for its displayed
quadratic \(q\).  All nineteen terms of \(q^{[3]}\) give 171 pair--term
incidences on 165 words.  Three pure singleton coordinates and four mixed
singleton zeros force a seven-entry Gram system in \(\mathbb C^2\), whose
exact characteristic-zero ideal is \([1]\).  Hence no other preimage of
\(\Delta_{8,3}\) for that fixed \(q\) lies in \(z=aq+4ps\).  The
[independent clean-room audit](polarized-eight-site-fixed-q-pair-cap-obstruction-independent-audit.md)
rebuilds the divided powers by repeated square-zero multiplication and
checks the same ideal with a different exact algebra system.  This is a
fixed-\(q\) obstruction, not an arbitrary pair-cap theorem or an all-even
descent.

[The weighted three-term pair-cap exhaustion](polarized-eight-site-three-term-pair-cap-exhaustion.md)
then ranges over the full natural class of three same-colour flagged
matchings.  After normalizing the first flag, all \(420^2=176{,}400\)
supports are scanned; exactly \(9{,}888\) have only the three intended
decorated terms.  Three nonzero pure Gram edges and support-forced mixed
zeros contradict every two-dimensional pair-cap realization:
\(7{,}968\) by the short pattern and \(1{,}920\) by general orthogonality
closure.  The
[independent audit](polarized-eight-site-three-term-pair-cap-exhaustion-independent-audit.md)
reproduces both counts and the ledger hash using projective odd paths and
isotropic cycles, with zero survivors.  Because every used coefficient is
a single nonzero monomial, the theorem allows arbitrary nonzero complex
weights on the same combinatorially exact supports.  Extra decorated terms,
cancellation, endpoint-asymmetric cells, and arbitrary \(q\) remain open.

[The one-cell invisible-direction theorem](polarized-eight-site-fixed-q-one-extra-pair-cap-obstruction.md)
then varies \(q\) itself.  Of the 243 cells outside the sparse seed, exactly
99 cells on eleven physical pairs preserve the displayed polarized identity;
the other 144 create one or two literal mixed debts.  Among the 99 invisible
directions, 66 retain the old seven-entry contradiction, all 15 altered
endpoint-asymmetric cases close projectively, and both nonzero alternatives
in the altered pure equation close for each of 18 monochromatic cases.  The
[independent clean-room replay](polarized-eight-site-single-invisible-cell-projective-closure-independent.md)
reconstructs all 99 directions and records 51 literal zero-triangle
certificates; the primary checker also supplies 33 optional saturated unit
ideals.  This excludes every complex point on each single-cell affine line,
but not simultaneous cells, visible-debt cancellation, or arbitrary \(q\).

[The invisible full-block theorem](polarized-eight-site-invisible-full-block-pair-cap-obstruction.md)
thickens each of those eleven physical directions to an arbitrary
\(3\times3\) endpoint-colour block.  One unsaturated affine ideal in 58
variables for each pair covers all coefficients, zero entries, and all 512
support strata; all eleven reduced bases are \([1]\).  The
[independent projective-and-ideal audit](polarized-eight-site-invisible-full-block-projective-and-ideal-closure-independent.md)
closes 5,552 of the 5,632 support strata by 11,056 replayable projective
certificates and closes the remaining 80 pair-17 strata with an independently
generated 545-equation unit ideal.  This allows one arbitrary physical block
at a time, not simultaneous blocks on distinct pairs, visible-debt
cancellation, or arbitrary \(q\).

[The exhaustive two-cell theorem](polarized-eight-site-two-cell-pair-cap-obstruction-independent-audit.md)
then scans all \(\binom{243}{2}=29{,}403\) pairs of new cells outside the
sparse seed without assuming individual invisibility.  Exactly 3,960 pairs
preserve the displayed polarized identity with both coefficients nonzero;
every one has zero individual and cross debt, so no visible-debt cancellation
occurs.  Projective parity closes 3,944 pair-cap systems, and independently
ordered localized characteristic-zero unit ideals close the remaining 16.
This is a fixed-\((q,z)\), exactly-two-new-cell theorem, not a result for
three cells, varying \(z\), arbitrary quadratics, or global shared caps.

[The exact three-cell cancellation theorem](polarized-eight-site-fixed-q-three-extra-cancellation-frontier.md)
next exhausts all \(\binom{243}{3}=2{,}362{,}041\) triples of new cells.
It finds 2,274,826 singleton-rejected triples, 87,027 identically compatible
triples, 187 genuinely new binomial cancellation families, and one
torus-inconsistent exceptional triple.  Projective Gram parity excludes
pair-cap lifts for 180 of the 187 new families, and seven localized
characteristic-zero unit ideals exclude the residue.  The
[independent clean-room audit](polarized-eight-site-fixed-q-three-extra-cancellation-frontier-independent-audit.md)
reconstructs the endpoint-ordered divided powers, all four census ledgers,
202 parity certificates, and all seven ideals with changed variable and
generator orders.  This closes only the 187 visible-debt cancellation
families at the fixed \((q,z)\); it makes no pair-cap claim for the 87,027
identically compatible triples, four or more new cells, varying \(z\), or
arbitrary quadratics.

[The compatible-three-cell obstruction](polarized-eight-site-fixed-q-compatible-three-extra-pair-cap-obstruction.md)
closes that remaining fixed-seed class.  Projective parity excludes 86,284
of the 87,027 identically compatible triples.  Of the 743 survivors, the
sole one-pair triple is a specialization of the audited arbitrary pair-17
block theorem; primary and independently reversed saturated
characteristic-zero ideals reduce to \([1]\) for all 742 multi-pair
survivors.  The
[clean-room audit](polarized-eight-site-fixed-q-compatible-three-extra-projective-frontier-independent-audit.md)
reconstructs the 99 cells, 3,960 compatibility edges, all 87,027 triangles,
the projective ledger, the exact 742-triple list, and every full ideal without
importing either primary three-cell verifier.  Together with the preceding
187-family theorem, this closes every exactly-three-added-cell deformation
at the displayed \((q,z)\).  Four or more cells, varying \(z\), arbitrary
quadratics, and the global descent remain open.

Latest OC1 refinement:
[three-cut-complete-high-sector-onefactor-exhaustion.md](three-cut-complete-high-sector-onefactor-exhaustion.md)
checks all 11,130 normalized triples of constant one-factors at order
eight, including overlapping factors and shared multicolor edges.  Exact
rational row-space tests show that none has three target-active complete
cuts, while two is sharp.  An independent replay recovered both maxima and
the 264/64 equality-record counts.  This is a restricted exhaustion, not a
three-cut theorem for arbitrary aggregate edge tensors; the general
three-cut/mixed-sector route remains open.
[fourth-two-onefactor-three-cut-extension-reconnaissance.md](fourth-two-onefactor-three-cut-extension-reconnaissance.md)
widens the same falsification test around the sharp two-cut base.  It scans
all 1,786,995 unordered pairs of two added constant-colour one-factors with
weights in \(\{-3,-2,-1,1,2,3\}\), using exact rational row-space tests;
the maximum remains two active complete cuts.  This is finite
reconnaissance only, with no implication for arbitrary weights,
nondiagonal cells, further factors, or general aggregate tensors.
[three-adjacent-five-cut-complete-quotient-countermodel.md](three-adjacent-five-cut-complete-quotient-countermodel.md)
then refutes the unrestricted bare three-cut implication.  A twelve-source
integral endpoint-decorated family has one common residual in all three
cofactor-insertion cylinders and target-defect dimensions \((1,1,2)\) on
the adjacent cuts \(z=2,3,4\).  Its full tensor is
\(e_1^{\otimes8}+e_2^{\otimes8}+e_{00210012}\), so it is not a Krenn
counterexample.  Two additional integral cells cancel that mixed word
exactly while preserving the three active quotients, but create three new
mixed words.  The
[independent audit](three-adjacent-five-cut-complete-quotient-countermodel-independent-audit.md)
reconstructs endpoint aggregation, annihilator duality, the three literal
cylinder decompositions, the defect spaces, the fixed-weight deletion-only
minimality, and the repair over \(\mathbb Q\).  Thus neither three complete
quotients nor one selected mixed equation suffices; a continuation must use
a fourth cut, a coupled mixed-support packet, or a different invariant.
[three-cut-boundary-star-strengthening-obstruction.md](three-cut-boundary-star-strengthening-obstruction.md)
then keeps the repaired nonstar blocks fixed while allowing arbitrary
complex values in all 63 endpoint-ordered cells on either boundary star.
No such one-star completion can activate any fourth cut
\(z\in\{0,1,5\}\): the internal annihilator retains an all-zero
functional while the fixed opposite boundary blocks make the full
all-zero coefficient identically zero.  Two exact support identities also
show that a single-star change cannot retain the killed original word and
kill even the first repaired debt while preserving the relevant old cut.
The
[independent audit](three-cut-boundary-star-strengthening-obstruction-independent-audit.md)
reconstructs all symbolic star coefficients, defect dimensions, kernel
witnesses, and the literal debt-undo countermodel.  This is an
arbitrary-complex theorem for the fixed sparse background, not a global
four-cut obstruction; simultaneous two-star or internal changes remain
live.
[three-cut-two-boundary-star-cumulative-repair-countermodel.md](three-cut-two-boundary-star-cumulative-repair-countermodel.md)
then gives an actual thirteen-source, endpoint-ordered two-star family with
the same three active cuts and defects \((1,1,2)\).  It kills all four
previous suffix-\(12\) debts at once and transports the sole mixed term to
\(00210021\); one direct \(67\) cell cancels that word and creates exactly
three suffix-\(21\) debts.  The
[independent audit](three-cut-two-boundary-star-cumulative-repair-countermodel-independent-audit.md)
re-expands all 105 matchings, all old and new debts, and every cut.  This is
a countermodel to the recorded finite debt packet, not a Krenn
counterexample or a whole-sector obstruction.
[three-cut-fourth-cut-fixed-interior-intersection.md](three-cut-fourth-cut-fixed-interior-intersection.md)
computes the exact residual left by a fourth cut.  For the repaired
six-site interior, cuts \(2,3,4,5\) force
\(H-\Delta=H_S\otimes R_{67}\), while cuts \(2,3,4,0\) or
\(2,3,4,1\) force a two-plane normal form.  Its
[independent reconstruction](three-cut-fourth-cut-fixed-interior-intersection-independent-audit.md)
intersects the primal cylinders directly and verifies the dimensions
\(8,2,2,1,1\).  A formal three-atom GHZ point shows why independently
freeing star cross-products cannot decide factorized realizability.
[three-cut-two-boundary-star-fourth-cut-segre-obstruction.md](three-cut-two-boundary-star-fourth-cut-segre-obstruction.md)
solves that remaining Segre problem over \(\mathbb C\).  All 108 entries on
both stars and all nine entries of the direct \(67\) block remain arbitrary;
exact minimal-component decompositions give \(891\) line-normal and
\(2730\) plane-normal triples, and every triple becomes the unit ideal after
the six off-diagonal fibers are imposed.  The
[independent audit](three-cut-two-boundary-star-fourth-cut-segre-obstruction-independent-audit.md)
reconstructs all 162 atoms, 126 coordinates, nine target fibers, component
counts, and 3,621 rational unit certificates without importing the primary
checker.  Thus no boundary-only perturbation of this fixed interior can
activate a fourth cut.

[The first controlled internal-block theorem](three-cut-internal-23-two-cell-fourth-cut-obstruction.md)
then replaces the internal cell (A_{23}) by the full complex family
(tE_{21}+sE_{00}), retaining all other interior cells, both arbitrary
boundary stars, the arbitrary direct (67) block, and all ordered target
fibres.  A target-preserving diagonal torus reduces the family to four
zero/nonzero strata; exact cylinder reconstruction and 12,032 rational
component unit certificates exclude cuts (0,1,5) on all four.  The
[independent audit](three-cut-internal-23-two-cell-fourth-cut-obstruction-independent-audit.md)
rebuilds the endpoint-ordered cofactors and torus covariance without the
primary code and verifies the exceptional two-colour reduction.  This is
an arbitrary-complex theorem for that two-cell family, not for a general
(3\times3) internal block.

[The five-cell plane-locus theorem](three-cut-internal-23-plane-support-fourth-cut-obstruction.md)
closes the entire natural extension
\(A_{23}\in\langle E_{00},E_{01},E_{02},E_{11},E_{21}\rangle\).
A target-preserving complex torus reduces it to 32 support orbits.  Five
pairwise-disjoint 35-coordinate cofactor blocks partition those orbits into
five quotient systems, whose exact characteristic-zero ideals have reduced
standard basis \([1]\).  The
[independent reconstruction](three-cut-internal-23-plane-support-fourth-cut-obstruction-independent-audit.md)
rebuilds all 96 four-cylinder intersections, all nine endpoint-ordered
fibres, the support partition, and the five unit ideals without importing
the primary code.

[The arbitrary-(23)-block theorem](three-cut-internal-23-arbitrary-block-fourth-cut-obstruction.md)
closes the four cells outside that plane and therefore allows an arbitrary
complex endpoint-ordered \(3\times3\) matrix \(A_{23}\), while the other
eight internal cells retain the displayed fixed values.  Nine disjoint
35-coordinate cofactor blocks partition all 480 new support masks into 27
finite torus charts and one cross-ratio family.  Every finite chart has an
exact rational unit ideal; the remaining family has a 628-generator unit
ideal over \(\mathbb Q[\lambda]\), so no exceptional complex value of the
cross-ratio survives.  The
[independent clean-room audit](three-cut-internal-23-arbitrary-block-fourth-cut-obstruction-independent-audit.md)
reconstructs the masks, endpoint order, projected cylinder intersections,
108 shared-star variables, and all 28 unit ideals by a different exact
linear-algebra route.  This exhausts all 512 supports of \(A_{23}\) only on
the fixed six-site interior.  A second perturbed internal block, a
replacement of that interior, and genuinely global mixed-sector invariants
remain open.

[The first adjacent two-block theorem](three-cut-internal-23-arbitrary-block-adjacent-25-line-fourth-cut-obstruction.md)
keeps \(A_{23}\) arbitrary and simultaneously allows
\(A_{25}=E_{00}+tE_{11}\), with the other seven internal cells fixed and
both boundary stars and \(A_{67}\) arbitrary.  A sixth torus character
normalizes every \(t\ne0\); adjacency of edges 23 and 25 eliminates all
mixed \(Xt\) terms.  Five old-locus, 27 finite outside-locus, and one
\(\mathbb Q[\lambda]\) unit ideal exclude a fourth cut on all 512 supports
of \(A_{23}\), while \(t=0\) is inherited from the preceding theorem.  The
[independent clean-room audit](three-cut-internal-23-arbitrary-block-adjacent-25-line-fourth-cut-obstruction-independent-audit.md)
reconstructs the six-character action, safe projected normals, all 108
shared-star entries, and all 33 ideals by different matching and linear-
algebra routes.  This proves only the displayed affine line in the second
block, not an arbitrary \(A_{25}\) or a global four-cut obstruction.

[The four-off-diagonal-line extension](three-cut-internal-23-arbitrary-block-adjacent-25-four-offdiagonal-lines-fourth-cut-obstruction.md)
keeps \(A_{23}\) arbitrary and closes the four additional families
\(A_{25}=E_{00}+tE_{cd}\) for
\((c,d)\in\{(0,1),(0,2),(1,2),(2,1)\}\).  For each direction, all 512
supports of \(A_{23}\) reduce to five inherited charts, 27 finite charts,
and one symbolic cross-ratio chart.  All
\(4(5+27+1)=132\) characteristic-zero ideals are unit; the combined
primary ledger is frozen before elimination.  The
[independent reconstruction](three-cut-internal-23-arbitrary-block-adjacent-25-four-offdiagonal-lines-fourth-cut-obstruction-independent-audit.md)
regenerates endpoint-ordered matchings, the torus census, safe projected
normals, arbitrary omitted coefficients, shared stars, and all 132 ideals
under different program orderings.  Together with the \(E_{11}\) line, this
leaves exactly \(E_{10},E_{20},E_{22}\) as unaudited one-cell directions in
the second block; it still does not make \(A_{25}\) arbitrary or prove a
global four-cut obstruction.

[The adjacent \(E_{22}\) theorem](three-cut-internal-23-arbitrary-block-adjacent-25-22-fourth-cut-obstruction.md)
closes a sixth affine line while retaining arbitrary \(A_{23}\), both
boundary stars, and \(A_{67}\).  For \(t\ne0\), an independent torus
character normalizes the moving coefficient without consuming an
\(A_{23}\) modulus.  Six symbolic open charts and eight exact exceptional
supports cover all 512 supports; 13 constant rank-176 minors, a uniform
all-\(X\) cut-5 rank-77/probe argument, and 30 chart/cut jobs reduce to 21
characteristic-zero unit ideals.  The
[independent clean-room audit](three-cut-internal-23-arbitrary-block-adjacent-25-22-fourth-cut-obstruction-independent-audit.md)
reverses matching, cylinder, variable, and generator orders, uses a different
cut-5 raw column, and independently obtains frozen rank and ideal ledgers.
Thus only \(E_{10},E_{20}\) remain among the one-cell directions in this
fixed-interior second block.  Their unavoidable torus invariants are,
respectively, \(\lambda=t x_{00}/x_{10}\) and
\(\lambda=t x_{00}/x_{20}\).  A valid continuation must first stratify the
coordinate-zero loci and then build full-cylinder normals and shared-star
certificates over \(\mathbb Q[\lambda]\); neither this local theorem nor the
eventual closure of those two lines would by itself give a global four-cut
invariant.

Latest U1 refinement: [rank-three-separator-collapse.md](rank-three-separator-collapse.md)
closes every connected global rank-three graph under all-pair Hessian
gauge rigidity.  A nonseparating deletion pair forces a zero row; its
boundary becomes a rank-three leaf, and a second-color overlap turns every
other incident block into a literal hole, contradicting cubic-vertex
rigidity.  Thus only the disconnected rank-three graph remains.  In its
row-full branch, a relevant internal graph needs at least three nontrivial
components (or an isolated rank site); two 2-connected components force a
whole-component missing color row.  Merging across rank-two and misaligned
rank-one blocks preserves the lower bound of three channels.  Globally,
either the rank-at-least-two graph is disconnected or some two-deletion
rank-three graph has an isolated site; connected rank-at-least-two support
with minimum rank-three degree three is impossible.  A double-invertible
isolated site with one invertible deleted star forces at least two literal
missing endpoint rows at every other internal site; the second invertible
star is needed only for all six rows, two direct holes, and the rank-two
spoke leaf.  The local six-row assertion, including arbitrary rank-zero,
rank-one, and rank-two second stars, has an independent equation-level and
finite-field audit in
[one-invertible-zero-cover-independent-audit.md](one-invertible-zero-cover-independent-audit.md);
its final neighborhood conclusion correctly retains the surrounding
all-pair gauge-rigidity hypothesis.  In particular, a 3-connected
rank-at-least-two graph forces a
globally rank-three-isolated vertex.  Thick disconnected rank-at-least-two
components are joined, when
at all, by complete bipartite rank-one blocks with fixed endpoint zero
masks; at six sites their only high-degree pattern is the already excluded
\(C_3\sqcup C_3\) saturated chart.  The empty-rank branch cannot be closed
from Hessians and support alone: an explicit nonnegative rank-one \(K_6\)
has all fifteen pair Hessians gauge-rigid (rank \(51/54\)) and satisfies
all eighteen active coordinate-anchor incidences; it fails a mixed target
coefficient, so fuller coefficient identities are essential for the
remaining step.  In fact, six-site empty-\(S\) rigidity makes all incident
rank-one endpoint lines distinct, so the eighteen anchors necessarily form
three directed derangements; every three incident lines are independent,
so each local family is a projective arc through the coordinate points.
The countermodel realizes this sharp normal form.  Coupling the
complete-join masks to the full triple-shore normal form now removes the
earlier invertible-edge hypothesis: every triple with two vertices in one
thick component and one in an adjacent component must be constant-row
degenerate and carries a pure three-cross selector.  In all three
normal-form dimensions, the nondegenerate branch gives incompatible masks
at the common outside endpoint.  This saturation is sharp but does not
align the selector colors: for a fixed common mask \(M\), every singleton
survivor set and every two-set meeting \(M\) occurs in the exact local
slice equation.  Nor does all-pair Hessian rigidity make the cross endpoint
lines injective: an exact \(K_4\sqcup K_4\) eight-site block model has a
complete full-mask rank-one join, a repeated endpoint line, and all 28
pair Hessians gauge-rigid of rank \(130/135\); a positive mixed coefficient
records precisely the missing target input.

On six vertices the Hessian hypothesis is no longer needed in the rank-one
branch.  `notes/rankone-anchor-fibre-cegar.md` keeps arbitrary sparse support
and asymmetric endpoint zero masks.  The one-centre anchors, unique-anchor
mutuality, pure nonemptiness, and mixed no-singleton rule reduce every chart
to one of seven nested-binomial/trinomial or two Laurent-rectangle fibre
orbits.  Their \(S_6\times S_3\) closure is an exact 123,666-clause UNSAT
certificate; both `drat-trim` and the repository's streaming checker verify
all 1,166,186 deletion-free RUP additions.  Hence no six-site source whose
aggregate blocks all have rank at most one can equal \(\Delta_{6,3}\).

In fact the full arbitrary-complex six-site theorem is now assembled and
adversarially checked in `notes/six-site-rank-graph-assembly-audit.md`.  Put
\(F=\{uv:\operatorname{rank}A_{uv}\ne1\}\), including zero blocks.  Forced
anchors give \(\Delta(F)\le2\) and \(|F|\le6\).  The exact graph census has
one, one, two, four, five, four, and two types for \(|F|=0,\ldots,6\),
respectively.  The new rank-one certificate closes \(f=0\); primitive
Laurent fibres and the exceptional-triangle stabilizer close \(f\le3\);
good-edge rectangles close \(f=4\); full-support rectangles and cancellation
transfers close \(f=5\); and the saturated support audits close \(f=6\).
Every semantic formula permits each exceptional block either to vanish or
to have rank at least two, except the saturated two-triangle checker, where
zero edges are first excluded by the torus-zero lemma.  Thus
\(H_6(A)\ne\Delta_{6,3}\) for arbitrary complex aggregate matrices.

For the all-even coordinate one-factor continuation,
`notes/uniform-cycle-switch-localization-countermodel.md` gives a uniform
Hamilton-winding countermodel to local mate selection and an exact
twelve-site even-holonomy recombination module: all eleven binomial rows
are phase-consistent, but one hundred other mixed fibres are singletons.
`notes/five-coordinate-factor-singleton-debt.md` isolates that boundary
for every union of three pure and two arbitrary coordinate one-factors.
For each perfect matching \(R\) of the pure union, its complete word fibre
is \(\operatorname {PM}(R\cup X_R)\); hence it is a singleton exactly when
its compatible extra edges contain no \(R\)-alternating cycle.  A double
count of the corresponding two-anchor cofactors gives a uniform lower
bound.  On the even-holonomy module the coarse, one-edge, and exact-cycle
bounds are respectively zero, three, and six canonical singleton fibres.
The stronger hope that every Hamiltonian three-factor cubic core leaves
one matching uncovered is false at the minimum orders.
[hamiltonian-cubic-cycle-cover-countermodels.md](hamiltonian-cubic-cycle-cover-countermodels.md)
introduces the exact port multigraph and cycle-cofactor bound, then gives a
five-factor eight-site module in which the two port-valid Hamilton cycles
cover all mixed core matchings.  The corresponding fibres are the only two
binomials, both cancel, and their Laurent rows are independent; the debt
moves to twenty-four new singleton words.  Exact colored-core exhaustion
at orders six and eight shows that two of the three eight-site core orbits
admit such a strong phased cover for every possible underlying extra pair.
The outward escape is nevertheless rigid.
[pure-safe-outward-debt-obstruction.md](pure-safe-outward-debt-obstruction.md)
allows every bichromatic coordinate cell on every pair, including multiple
cells per aggregate block, while keeping the original pure fibres
singleton.  No extension is possible at any size.  At six sites a
five-word propagation forces four repair cells absent and returns to the
seeded singleton; at eight sites the exact term-indicator formula has a
107-clause, 106-variable deletion-minimal unit core on 23 words.  Thus any
continuation of these cycle-cover seeds must activate new monochromatic
cells and control nontrivial pure cancellation.

For the six-site seed, allowing all monochromatic cells no longer makes the
support problem cheap.  [n6-unrestricted-minimum-closure-phase-obstruction.md](n6-unrestricted-minimum-closure-phase-obstruction.md)
proves by an exact lazy MaxSAT enumeration that a no-mixed-singleton closure
needs at least twenty added cells, and exhibits a sharp 35-cell support.  Its
71 mixed fibres are all binomial, but three exponent rows form an odd signed
circuit.  The exact optimizer finds all 73 unit three-row phase cores at that
support; their universal support-breaking clauses, followed by 75 further
singleton clauses, raise the phase-consistent lower bound to 22 additions
(37 total cells).  This applies even when other fibres contain three or more
terms.  The exact search is continuing above that bound.

The three-literal-zero live stratum is now closed beyond its
minority-exceptional beta range.
[live-three-zero-minority-exceptional-beta.md](live-three-zero-minority-exceptional-beta.md)
subsumes the common-beta and one-exceptional theorems: for an odd live shore
of size $2r-1$, $t\le r-1$ exceptional live beta values still force the
shared zero star to vanish.  Monochromatizing all exceptional sites makes
every balanced cofactor the same nonzero monomial, even when exceptional
values repeat, so fixed-cardinality subset incidence kills the first two
rows and one ternary-letter coefficient kills the last.
[live-three-zero-two-marked-exceptional-beta.md](live-three-zero-two-marked-exceptional-beta.md)
then forces two exceptional live sites to be the unique marked pair and
extends the contradiction through $t\le r+1$.  In the absence of
additional nonzero singular sites, the first unresolved Cauchy-cancellation
range is therefore $r+2\le t\le2r-1$; at the first nonminimal order it
consists only of the all-exceptional live shore.
[live-three-zero-all-exceptional-five-live.md](live-three-zero-all-exceptional-five-live.md)
closes that first split-exception boundary as well.  Three explicit diagonal
response minors have normalized pivots $g_i+g_j$; their signed combination is
$2g_i$, so simultaneous cancellation would force a forbidden live--live
denominator pole.  Thus the no-extra-singular three-zero branch is complete
for live shores of sizes three and five.
[live-three-zero-first-split-layers.md](live-three-zero-first-split-layers.md)
then closes the first two split-exception layers $t=r+2$ and $t=r+3$
uniformly.  A singleton-active colouring makes the complete response
triangular with pivots given by a fixed-subset incidence transform of
one- and two-column Cauchy permanents.  Point incidence has full column
rank; pair incidence is invertible, and simultaneous vanishing of its
two-column permanents would make three nonzero two-vectors pairwise
orthogonal for the swap form, which is impossible in characteristic zero.
Consequently every no-extra-singular stratum with $t\le r+3$ is closed,
including all live shores through size seven.  The first remaining range
is $t\ge r+4$.
[live-three-zero-all-exceptional-nine-live.md](live-three-zero-all-exceptional-nine-live.md)
closes the first case of that range, $r=5,t=9$.  Coupling every choice of
exceptional three-set gives a $1260$-by-$840$ integer incidence map with
full column rank (certified by a full-rank reduction modulo $1009$).
Common pivot cancellation would therefore kill every disjoint
$3$-by-$3$ permanent; fixing one column triple and applying the injective
triple-versus-pair incidence map on the other six rows reduces this to
three impossible nonzero ratio equations.  Thus all no-extra-singular
live shores through size nine are closed; the first unresolved size is
eleven.
[live-three-zero-third-split-distinct-beta.md](live-three-zero-third-split-distinct-beta.md)
extends the entire third split layer $t=r+4$ to arbitrary order when the
exceptional beta values are pairwise distinct.  A genuinely confluent
Borchardt quotient handles the repeated common-beta columns.  Rank loss
would produce a unique numerator of degree $p+2$; its forbidden simple
residues at three double poles imply
$((c-a)/(c+a))((d-a)/(d+a))=2$.  Comparing three distinct choices
contradicts injectivity of that Möbius map.
[live-three-zero-third-split-collision-beta.md](live-three-zero-third-split-collision-beta.md)
closes every collision stratum.  Multiplicity at least three reduces to
nonvanishing of a deleted-pair elementary symmetric function.  With only
single and double classes, double-confluent Borchardt turns the labeled
pivots into initial-jet minors; complementary-minor duality and a scaled
Vandermonde block force the same Hermite root polynomial and Möbius
contradiction.  Hence the whole $t=r+4$ layer is closed.  The first
remaining range begins at $t=r+5$.
[live-three-zero-all-exceptional-eleven-live.md](live-three-zero-all-exceptional-eleven-live.md)
closes the first case of that layer, including every repeated-beta
partition, by simultaneous row/column confluence and primal/dual Hermite
degree bounds.
[live-three-zero-fourth-split-layer.md](live-three-zero-fourth-split-layer.md)
then closes the full $t=r+5$ layer uniformly.  Multiplicity at least four,
the short two-class profiles, the one-double profile, the all-double
profile, and the all-distinct profile are handled separately; the final
distinct obstruction is a degree-four residue identity whose top two
coefficients leave an explicitly nonzero quadratic.
[live-three-zero-fifth-split-distinct-beta.md](live-three-zero-fifth-split-distinct-beta.md)
then closes the all-distinct stratum of $t=r+6$ uniformly for $r\ge7$.
Its residual numerator is quadratic, but a three-anchor determinant and
opposite-pole subtraction give three linear equations whose exact
combination is the nonzero anchor Vandermonde.  The independent audit in
[live-three-zero-fifth-split-distinct-beta-audit.md](live-three-zero-fifth-split-distinct-beta-audit.md)
checks the smallest confluent boundary, lower-degree residual quadratics,
zero exceptional values, and every denominator used in the pole comparison.
[live-three-zero-fifth-split-collision-beta.md](live-three-zero-fifth-split-collision-beta.md)
closes every repeated-value stratum in the same layer.  Maximum multiplicity
at least five falls to deleted-pair elementary-symmetric descent; all other
profiles route through a singleton Hermite-jet rank lemma and either an
immediate degree bound, a moving-class quadratic, or a two-anchor quartic.
Its independent audit in
[live-three-zero-fifth-split-collision-beta-audit.md](live-three-zero-fifth-split-collision-beta-audit.md)
verifies simultaneous row/column confluence and proves the profile census
uniformly.  Hence the full no-extra-singular range $t\le r+6$ is closed; the
next layer begins at $t=r+7$.
[live-three-zero-sixth-split-frontier.md](live-three-zero-sixth-split-frontier.md)
opens and closes that layer exactly.  Deleted-$e_6$ descent, short Hermite splits, and
constant, linear, and quadratic moving-class determinants close every
collision stratum.  The final five-double/five-single profile is killed by
a three-full-double split: complementary-pair subtraction forces three of
four values into one fibre of a nonconstant quadratic map.  On the
all-distinct stratum, all pivot vanishing first gives identically singular
four-anchor cubic residue pencils of cleared degree eight.
[live-three-zero-sixth-split-distinct-closure.md](live-three-zero-sixth-split-distinct-closure.md)
extracts one exact linear endpoint certificate from each pencil.  The five
certificates on a five-core form a hollow Cauchy system; fixing four nonzero
anchors and moving the fifth leaves at most six singular choices, hence at
least four invertible cores even if one exceptional value is zero.  Their
common translation equations contradict the two-point fibres of
\(\psi(a,y)=-(y+3a)/(y^2-a^2)\).  The independent audit in
[live-three-zero-sixth-split-five-core-cauchy-audit.md](live-three-zero-sixth-split-five-core-cauchy-audit.md)
checks the endpoint signs, zero-value bookkeeping, degree-six selection
polynomial, and fibre count.  Thus the full no-extra-singular range
\(t\le r+7\) is closed; pointwise DR4 is an optional stronger statement,
not a remaining proof obligation.
[live-three-zero-seventh-split-collision-frontier.md](live-three-zero-seventh-split-collision-frontier.md)
opens the next layer (t=r+8), whose feasible range is (p=r-1\ge8).
Deleted-(e_7) descent, the two-class Hermite bound, and exact constant,
linear, and quadratic moving-class determinants close every profile except
an explicitly enumerated triple/double/single list at the small orders and,
for (p\ge13), the seven uniform families
((2^d,1^{p+9-2d})), (1\le d\le7).  The independent dynamic-programming
audit in
[live-three-zero-seventh-split-collision-frontier-audit.md](live-three-zero-seventh-split-collision-frontier-audit.md)
reconstructs the census, zero-singleton legality, and finite-to-uniform
persistence without reusing the main partition enumerator.
[live-three-zero-seventh-split-bivariate-quartet-closure.md](live-three-zero-seventh-split-bivariate-quartet-closure.md)
then closes the all-distinct stratum and every residual double/single profile
with at least seventeen distinct beta classes.  Moving two exceptional
values makes the five-anchor quartic Robin determinant identically zero by a
strict bidegree-\((10,10)\) grid count.  Its opposite endpoints reduce to two
four-anchor cubic pencils; subtracting their proved linear quartet
certificates eliminates every unknown translation.  Fixing four nonzero
anchors and moving the fifth leaves a nonzero cubic with at least twelve
roots, a contradiction.  The independent audit in
[live-three-zero-seventh-split-bivariate-five-anchor-audit.md](live-three-zero-seventh-split-bivariate-five-anchor-audit.md)
checks the sharp interpolation threshold, endpoint signs and factors,
retained-double singleton legality, zero-value bookkeeping, and the exact
post-closure residual table.  Consequently all-distinct is closed, all
seven stable collision families are closed for \(p\ge15\), and only the
audited finite triple list together with the following double counts remain:
\(d=1,\ldots,8\) at \(p=8\); \(d=2,\ldots,9\) at \(p=9\);
\(d=3,\ldots,9\) at \(p=10\); \(d=4,5,6,7,9,10\) at
\(p=11\); \(d=5,6,7,10\) at \(p=12\); \(d=6,7\) at
\(p=13\); and \(d=7\) at \(p=14\).
[live-three-zero-seventh-split-repeated-anchor-bivariate-closure.md](live-three-zero-seventh-split-repeated-anchor-bivariate-closure.md)
pushes the collision threshold down once more, to sixteen distinct classes.
Selecting both copies of one double produces a genuine second-order
condition on the cubic residual.  Its minimally cleared row has sharp
bidegree \((4,4)\), so together with three simple rows the determinant has
sharp bidegree \((10,10)\).  The strict sixteen-class grid makes it
identically zero; either opposite endpoint leaves a forbidden identically
singular three-anchor quadratic pencil.  This closes every residual with
\(p\ge d+7\), including the final stable family at \(p=14\).  The remaining
double counts are now \(d=2,\ldots,8\) at \(p=8\),
\(d=3,\ldots,9\) at \(p=9\), \(d=4,\ldots,9\) at \(p=10\),
\(d=5,6,7,9,10\) at \(p=11\), \(d=6,7,10\) at \(p=12\),
and \(d=7\) at \(p=13\); there is no stable tail from \(p=14\) onward.
[live-three-zero-seventh-split-triple-repeated-anchor-closure.md](live-three-zero-seventh-split-triple-repeated-anchor-closure.md)
closes the entire residual triple list.  Three-class selections leave a
nonzero constant residual, while a partially selected triple supplies the
singleton row needed for simultaneous confluence.  The resulting second-
and third-order no-simple-pole conditions are nonzero quartics and sextics.
Strict root counts close seven profiles; the sharp six-triple and
\((3,3,2)\) cases have fixed endpoint ratios \(3/5\) and \(1/4\), whose
comparison for two omitted triples contradicts injectivity of
\((f-x)/(f+x)\).  A final \(3+2+2\) selection gives five roots of a
nonzero quartic and closes the last three profiles.  Thus only the finite
double/single list remains in the seventh collision layer.
[live-three-zero-seventh-split-double-pair-closures.md](live-three-zero-seventh-split-double-pair-closures.md)
then sharpens that finite double/single list by four independent repeated-
anchor determinants.  Two fully selected double anchors give a nonzero
degree-eight univariate minor, closing every profile with at least twelve
classes, three doubles, and two singletons.  Strict bidegree-six grids close
the two large near-all-double profiles and the all-double profile at
\(p=11\); a mixed second-order/simple bidegree-ten grid closes the isolated
\((p,d,s)=(8,2,13)\) case.  Exact endpoint reductions rule out every
putative identically singular pencil, including a zero singleton.  The
remaining frontier is exactly
\((p;d,s)=(8;6,5),(8;7,3),(8;8,1),(9;7,4),(9;8,2),(9;9,0),
(10;8,3),(10;9,1)\), with nothing left for \(p\ge11\).
[dr4-full-endpoint-rigidity.md](dr4-full-endpoint-rigidity.md) proves the
four-anchor cubic rigidity theorem used as an optional uniform collision
engine.  Sixteen endpoint equations linearize on the fifteen nonconstant
squarefree translation monomials.  Corrected generic minors give rank
fifteen off the three product-pairing divisors; homogeneous toric cofactor
certificates close those divisors, including their quadratic-field
exceptional curve.  The independent saturation audit in
[dr4-full-endpoint-rigidity-independent-audit.md](dr4-full-endpoint-rigidity-independent-audit.md)
eliminates the isolated bivariate intersections missed by a gcd-only
argument and verifies that the only candidates force the structural
boundaries \(b=0\) or \(b=-1\).  Its application in
[live-three-zero-seventh-split-repeated-double-dr4-closure.md](live-three-zero-seventh-split-repeated-double-dr4-closure.md)
therefore safely closes every double/single profile with at least fourteen
classes.
[live-three-zero-seventh-split-low-class-repeated-row-closure.md](live-three-zero-seventh-split-low-class-repeated-row-closure.md)
closes six of the eight finite profiles left above.  At the sharp
eight-root boundary, proportional degree-eight pair minors force a
constant polynomial-row relation; a coefficient-span minor and a
four-anchor comparison exclude it.  A separate seven-node Lagrange
endpoint identity excludes the near-all-double cases.  The note explicitly
keeps its three-simple equality calculation conditional, because selecting
all singleton guards would otherwise create a Hermite rank gap.  Its exact
unconditional frontier is only \((p,d,s)=(8,7,3),(8,8,1)\).
[live-three-zero-seventh-split-final-773-exchange-closure.md](live-three-zero-seventh-split-final-773-exchange-closure.md)
and
[live-three-zero-seventh-split-final-881-exchange-closure.md](live-three-zero-seventh-split-final-881-exchange-closure.md)
close those last two profiles without that gap.  Every seven-value core
leaves singleton mates, so cubic gauges propagate its Hermite residual to
the full value-class set.  The final lift span has dimension at least three.
After the remaining double mates are retained in the numerator, the
residue theorem supplies the common-pole node, giving respectively eleven
degree-nine or ten degree-eight common Robin nodes.  The gcd-corrected
Wronskian weight \(d-1\) at every nonbase node exceeds the global Wronskian
degree bound.  Thus **every collision stratum of the seventh split is
closed**; together with the all-distinct closure, the complete
no-extra-singular layer \(t=r+8\) is closed.
[live-three-zero-higher-split-all-distinct-exchange-closure.md](live-three-zero-higher-split-all-distinct-exchange-closure.md)
closes every all-distinct no-extra-singular layer at once for
\(7\le h=t-r-1\le r-2\).  Cubic gauges lift the deletion residuals from
an \(m\)-core into one Robin kernel on an \((m+1)\)-core.  Their span has
dimension at least three: a hypothetical two-dimensional span would give a
rational map with more paired fibers and ramification points than its
degree permits by Riemann--Hurwitz, including the possible zero anchor.
Cancelling the top two coefficients propagates a residual of degree
\(m-3\) all the way to the full exceptional set.  There a residue-multiplier
surjectivity argument forces the residual to vanish at every exceptional
node, contradicting its degree.  The independent reconstruction in
[live-three-zero-higher-split-all-distinct-exchange-audit.md](live-three-zero-higher-split-all-distinct-exchange-audit.md)
checks the Hermite quantifiers, projective/gcd and zero-node cases, terminal
multiplier, and inherited graph cleanup; its separate checker also scans
16,977 exact small Robin systems.  Hence all-distinct beta values are no
longer a frontier in any remaining split layer.
[live-three-zero-higher-split-collision-exchange-wronskian.md](live-three-zero-higher-split-collision-exchange-wronskian.md)
extends the cubic exchange to every collision profile for which all
one-label-per-class \(h\)-cores retain a singleton row.  The exact legality
criterion is \(n_1\ge h+1\) or \(n_2\ge c-h+1\).  At the full class set,
stationary polynomial multipliers expose all available common-pole jets;
the gcd-corrected missing-jet and exceptional-node weights give the exact
sufficient number
\(9-c+(\ell+1)\max(3-k+\ell,0)>0\), where
\(\ell=\max(0,c-2h-2)\).  The proof treats a gcd of order \(k\) at the
common pole as impossible, rather than silently dropping that condition.
A separate residue-multiplier Vandermonde argument closes every legal
profile with collision excess \(M-c\le2\).
[live-three-zero-higher-split-collision-frontier.md](live-three-zero-higher-split-collision-frontier.md)
then gives the exact higher-collision census after the large-class,
two-class Hermite, constant/linear/quadratic moving-class, and exchange--
Wronskian routes.  It proves that every residual still has a legal Hermite
core representing between three and \(h-1\) classes, but records broad
persistent double/single and small-part families; the sparse
\((2,1^{M-2})\) profile makes the upper bound sharp.  Thus this census is a
rigorous frontier, not a claimed closure.
[live-three-zero-eighth-split-433333-common-pole-closure.md](live-three-zero-eighth-split-433333-common-pole-closure.md)
closes the former first residual profile
\((h,k;\lambda)=(8,1;(4,3,3,3,3,3))\).  Legal \(3+3+2\) selections have a
nonzero constant residual.  Comparing the common-pole residue as the full
triple role moves forces four distinct values into one fibre of
\(-(x+7\mu)/(x^2-\mu^2)\), while every fibre has size at most two.
[live-three-zero-higher-split-k1-constant-core-role-swap.md](live-three-zero-higher-split-k1-constant-core-role-swap.md)
promotes that calculation to two uniform \(k=1\) theorems for every legal
three-class core.  Three interchangeable instances of one selected role
cannot fit in a quadratic fibre; swapping two unequal positive roles gives
the exact factor \(2\mu(r-s)(x-y)(x+y)\), forbidden by the nonzero common
value and the distinct/nonopposite conditions.  The literal profile audit
closes seventeen of the thirty-five former \(h=8,k=1\) residuals, including
the separate
[\(3^3 2^5\) closure](live-three-zero-eighth-split-33322222-common-pole-closure.md).
[live-three-zero-higher-split-constant-core-common-pole.md](live-three-zero-higher-split-constant-core-common-pole.md)
extends the interchangeable-role clause to every \(k\ge1\).  For a
constant three-class residual, the order-\(k\) common-pole coefficient,
after its structural denominators are cleared, is a nonzero polynomial of
degree at most \(2k\) in the moving value.  A triangular expansion at
infinity proves nonidentity for every fixed background.  Thus \(2k+1\)
interchangeable legal roles are impossible; the exact audit adds five old
residual closures at \(h=8,k=2\) and one at \(h=8,k=3\).
[live-three-zero-higher-split-antiderivative-wronskian.md](live-three-zero-higher-split-antiderivative-wronskian.md)
adds a dual collision-excess obstruction.  Every full-core rational
function has zero residues, so its unique primitive vanishing at infinity
has numerator degree at most \(e-1\), where \(e=M-c\).  At a repeated value
of excess multiplicity \(m\), the primitive space has missing jets of total
Wronskian weight \(m(d-1)\); absorbing that node into the gcd costs at least
\(m+1\) degrees.  The exact corrected deficit is at least \(d^2-e\), so
every legal exchanged profile with \(e\le8\) is closed.  Together with the
\(k=1\) role swaps this eliminates thirty-four of the thirty-five former
\(h=8,k=1\) residual profiles and all of their double/single cases.  The
only remaining profile in that layer is \(3\,2^4 1^8\), whose sole illegal
value core is the all-eight-singleton core.
[live-three-zero-eighth-split-one-bad-core-repair.md](live-three-zero-eighth-split-one-bad-core-repair.md)
repairs that sole illegal core, and in fact proves a uniform theorem whenever
there are exactly \(h\) singleton value classes.  For the exceptional
\((h+1)\)-core consisting of those singletons and one repeated class, the
available \(h\) deletion lifts span at least three dimensions.  A parity
determinant treats the possible zero singleton through its exact cubic gauge,
and the extra common Robin node then makes a hypothetical pencil violate
Riemann--Hurwitz.  The ordinary exchange propagates from size \(h+1\), so the
terminal deficit \(d^2-e>0\) closes \(3\,2^4 1^8\).  Thus all thirty-five
former collision residuals at the first higher frontier \((h,k)=(8,1)\) are
now eliminated; this statement does not yet include the \(k\ge2\) layers of
the eighth split.
[live-three-zero-higher-split-unique-bad-core-repair.md](live-three-zero-higher-split-unique-bad-core-repair.md)
observes that the partial-lift argument depends only on uniqueness of the
illegal \(h\)-core, not on all its values being singletons.  The exact number
of illegal cores is \(\binom{n_{\ge3}}{h-n_1}\), so uniqueness holds precisely
when \(n_1=h\) or \(n_1+n_{\ge3}=h\).  Repairing that core and applying the
same antiderivative deficit closes two additional frozen \(h=8,k=2\)
residuals, \(3^2 2^4 1^6\) and \(3\,2^5 1^7\).
[live-three-zero-higher-split-double-guard-shadow-bypass.md](live-three-zero-higher-split-double-guard-shadow-bypass.md)
removes the initial-core legality hypothesis altogether whenever
\(c\ge h+1\) and the profile has a double class.  The illegal cores are the
uniform Boolean shadow consisting of all singleton classes and a fixed-size
subset of the multiplicity-at-least-three classes.  One-missing lifts carry
this shadow upward until only the set of all nondouble classes remains; a
nonzero double guard bypasses that last hole.  Full exchange follows, so
the antiderivative theorem closes every such profile of collision excess at
most eight.  This includes the two-hole terminal profile
\(3^2 2^4 1^7\) at \(h=8,k=3\).
[live-three-zero-eighth-split-k2-updated-census.md](live-three-zero-eighth-split-k2-updated-census.md)
freezes the exact second higher layer before these newest incremental
closures.  The older moving-role, ordinary antiderivative, and
eight-singleton repair routes are pairwise disjoint on the old residual
slice and reduce its 42 profiles to an explicitly ordered list of 16.
[live-three-zero-eighth-split-443333-order-two-common-pole-closure.md](live-three-zero-eighth-split-443333-order-two-common-pole-closure.md)
closes the first profile on that list.  On each three-subset of the four
triple values, the three legal \((3,3,2)\) cores turn the order-two
common-pole equation into an affine expression in
\(d(x)=-2\mu/(x^2-\mu^2)\).  Its three distinct values fix both background
jets; comparison of the four subsets then puts four values in one fibre of
the degree-two function \(-(x+7\mu)/(x^2-\mu^2)\), an impossibility.  A
separate consecutive-swap calculation with the two quartic roles gives an
independent exact contradiction.
[live-three-zero-eighth-split-k2-post-role-census.md](live-three-zero-eighth-split-k2-post-role-census.md)
audits the full twelve-core hypothesis literally.  The four-role theorem
closes eight of the sixteen frozen profiles and the generalized unique-core
endpoint closes two more, leaving six exact residuals.
[live-three-zero-eighth-split-k2-three-triple-double-closure.md](live-three-zero-eighth-split-k2-three-triple-double-closure.md)
then closes both residuals containing three triples and at least two doubles.
The three triple-role permutations fix the two common-pole background jets.
For each double value the mixed equations give one cubic having all three
triple values as roots.  Its four coefficients are an invertible linear
transform (determinant \(1327104\)) of \((1,Y,Y^2,Y^3)\), so two distinct
double values cannot yield proportional copies of the same cubic.  The exact
\(h=8,k=2\) frontier is thereby reduced to
\(2^{10},3\,2^8 1,2^9 1^2,3\,2^7 1^3\).
[live-three-zero-eighth-split-k2-one-triple-partial-double-closure.md](live-three-zero-eighth-split-k2-one-triple-partial-double-closure.md)
closes the two one-triple profiles.  On any three double classes, upgrading
the partial role places three lifted residuals in one cubic kernel.  Four
exact order-two rows at distinct nodes force that kernel to be a pencil;
the cubic rank-one quadric then makes all three original linear residuals
proportional.  Fixing two doubles and moving the third produces five or six
roots of a nonzero degree-four row determinant.  Only \(2^{10}\) and
\(2^9 1^2\) now remain in the \(h=8,k=2\) collision layer.
[live-three-zero-eighth-split-all-double-second-order-closure.md](live-three-zero-eighth-split-all-double-second-order-closure.md)
closes \(2^{10}\).  On every five/five partition, the ten two-partial-double
residuals lift into a four-dimensional sextic kernel of six exact
second-order residue rows.  The two relations among the five value rows
dualize to a rational pencil which maps isomorphically onto
\(\mathbb C[z]_{\le1}\).  Its two rational derivatives force a Stieltjes
equation on every partition.  Swapping one value across the partition puts
the other nine values in one fibre of
\((5u+x)/(u^2-x^2)\), contradicting its degree-two fibre bound.  The note
also audits the unique global antiderivative/full-core Wronskian equality
case which the local relation pencil removes.
[live-three-zero-eighth-split-double-single-second-order-closure.md](live-three-zero-eighth-split-double-single-second-order-closure.md)
closes the last profile \(2^9 1^2\).  The same five-double lifts fill a
four-dimensional sextic kernel, while the two relation numerators now map
injectively to a plane in \(\mathbb C[z]_{\le2}\).  The two singleton poles
give proportional Robin rows on that plane.  Their exact proportionality
cancels the mutual-singleton term and produces a Stieltjes equation on every
five/four partition; partition swaps put all nine double values in one
degree-two fibre.  Thus the complete no-extra-singular \(h=8,k=2\)
collision frontier is closed.
[live-three-zero-higher-split-consecutive-role-transfer.md](live-three-zero-higher-split-consecutive-role-transfer.md)
provides an all-\(k\) constant-core theorem in the multiplicity direction.
Across \(k+1\) consecutive transfers of one selected label from a fixed
class \(B\) to a fixed class \(A\), the order-\(k\) common-pole residue is a
degree-\(k\) polynomial in the transfer count.  Its leading coefficient is
the \(k\)-th power of
\(2\mu(A-B)(A+B)/((A^2-\mu^2)(B^2-\mu^2))\), hence is structurally nonzero.
This independently recovers the quartic-role \(k=2\) check and closes the
first updated \(h=8,k=3\) residual \(4^3 3^3\).
[live-three-zero-eighth-split-k3-seven-triple-common-pole-closure.md](live-three-zero-eighth-split-k3-seven-triple-common-pole-closure.md)
proves a five-exact-triple theorem.  For every triple of those values, its
three legal \((3,3,2)\) roles make the cubic common-pole equation affine in
the role-drop jet and force \(V=T/\mu-T^2\).  Comparing overlapping triples
puts at least three distinct exceptional values in one fibre of the
degree-two role-three map.  This closes six old residuals at once:
\(3^7,3^5 2^3,3^6 2\,1,3^5 2^2 1^2,3^5 2\,1^4,3^5 1^6\).
[live-three-zero-eighth-split-k3-four-triple-cubic-jet-elimination.md](live-three-zero-eighth-split-k3-four-triple-cubic-jet-elimination.md)
closes all four residuals with exactly four triple classes.  Their four
overlapping three-sets are common roots of an explicit quartic and sextic.
An integral pseudo-remainder certificate forces the quartic leading
coefficient to vanish; the remaining nonzero cubic cannot have the four
distinct roots.  No genericity or exceptional-parameter division occurs.
[live-three-zero-eighth-split-k3-formal-five-double-duality.md](live-three-zero-eighth-split-k3-formal-five-double-duality.md)
uses ten two-partial formal-five-double lifts to build a common
four-dimensional sextic kernel.  Its two dual relations inject into
polynomials of degree \(c-4\), where \(c\) is the number of complementary
value classes.  Dimension, singleton Robin rows, partition swaps, and a
Boolean-slice mixed difference close six further third-order profiles:
\(3^3 2^6,3\,2^9,3^3 2^5 1^2,2^{10}1,3\,2^8 1^2,3^2 2^6 1^3\).
Its formal-layer extension lets a triple donate two labels while its fixed
excess stays in the complementary factor.  A simple-root Wronskian bound
then also closes \(3^2 2^5 1^5\) and \(3^3 2^4 1^4\).
[live-three-zero-eighth-split-all-order-formal-five-layer-duality.md](live-three-zero-eighth-split-all-order-formal-five-layer-duality.md)
shows that the same formal-five kernel and dual degree bound are independent
of the common-pole order \(k\).  The complementary factor has degree
\(k+8\), so differentiation of \((z+\mu)^{k+1}N/A\) always has leading
coefficient \(n-7\), leaving the same pencil in
\(\mathbb C[z]_{\le c-4}\).  Its simple-root Wronskian criterion closes six
frozen \(h=8,k=4\) residuals, including the smallest \(4\,3^6\).
[live-three-zero-eighth-split-k4-six-triple-common-pole-closure.md](live-three-zero-eighth-split-k4-six-triple-common-pole-closure.md)
extends the exact-triple role-drop cancellation to fourth order.  The
fourth Bell coefficient is again affine in the drop parameter.  A
three-direction Boolean difference over six exact triples is precisely six
times a product of three first-jet differences; the quadratic role-three
map permits a matching with all three differences nonzero.  This closes
\(3^7 1\), the remaining fourth-order profile with six exact triples.
[live-three-zero-eighth-split-k4-nine-double-singleton-square-closure.md](live-three-zero-eighth-split-k4-nine-double-singleton-square-closure.md)
closes \(3\,2^9 1\).  The all-order formal-five pencil is a plane in the
quadratics; its singleton Robin row inserts the singleton square and
cancels that pole.  The outside-double logarithmic equation
\(X^2+X'=0\), differenced across two partition swaps, forces seven double
values into one fibre of \((5u+x)/(u^2-x^2)\).
[live-three-zero-eighth-split-k4-two-triple-eight-double-closure.md](live-three-zero-eighth-split-k4-two-triple-eight-double-closure.md)
closes \(3^2 2^8\).  Five formal double layers leave a full linear
relation pencil.  Its two basis members kill the first two jets at every
outside double, and a single partition swap would put all seven other
double values in one quadratic fibre.
[live-three-zero-eighth-split-k4-all-double-row-boolean-closure.md](live-three-zero-eighth-split-k4-all-double-row-boolean-closure.md)
closes \(2^{11}\).  The six outside second-order rows have one common
quadratic kernel and are proportional.  Exact third and fourth Boolean
differences of two row minors have only the zero ratio ideal; a matching
extension then collapses nine values into one quadratic fibre.
[live-three-zero-eighth-split-k4-five-triple-robin-rectangle-closure.md](live-three-zero-eighth-split-k4-five-triple-robin-rectangle-closure.md)
closes \(3^5 2^2 1^3\).  Six simple complementary roots saturate the
quartic-pencil Wronskian.  The accessory-polynomial residue sum and a
three-slice rectangle force every four of the five triple values to sum
to zero, contradicting distinctness.
[live-three-zero-eighth-split-k4-ten-double-two-singleton-cubic-boolean-closure.md](live-three-zero-eighth-split-k4-ten-double-two-singleton-cubic-boolean-closure.md)
closes \(2^{10}1^2\).  Two singleton rows determine the cubic relation
pencil; a division-free member cancels one singleton and kills the other.
A third Boolean difference forces five points of
\(x\mapsto(\Phi_u(x),\Phi_s(x))\) onto a line whose pullback is a nonzero
quartic.
[live-three-zero-eighth-split-k4-two-triple-seven-double-two-singleton-square-closure.md](live-three-zero-eighth-split-k4-two-triple-seven-double-two-singleton-square-closure.md)
closes \(3^2 2^7 1^2\).  The quadratic relation pencil is spanned by the
two singleton squares.  Their outside-double jets and the swap of the
unique other outside double put six distinct values in one quadratic
fibre.
[live-three-zero-eighth-split-k4-saturated-quartic-moment-closures.md](live-three-zero-eighth-split-k4-saturated-quartic-moment-closures.md)
closes \(3^4 2^3 1^4\) and \(3^3 2^4 1^5\).  Six simple complementary
roots saturate the quartic relation-pencil Wronskian.  The first three
accessory residues give exact zeroth, first, and second Robin moments;
their partition rectangles force an even quartic in the choose-two case
and a nonzero quadratic through three distinct values in the choose-one
case.
[live-three-zero-eighth-split-k4-five-triple-monic-quadratic-closure.md](live-three-zero-eighth-split-k4-five-triple-monic-quadratic-closure.md)
proves that five exact triple classes are already impossible at fourth
order.  Fixed-fifth rectangles in the affine Bell identity make the five
role-jet points lie on a monic quadratic, including both possible double-
fibre patterns of the degree-two first-jet map.  Pulling that quadratic
back gives a nonzero quartic with five distinct roots.  This newly closes
\(3^5 2\,1^5\) and \(3^5 1^7\) on the sequential census frontier.
[live-three-zero-eighth-split-k4-three-triple-three-double-hyperplane-closure.md](live-three-zero-eighth-split-k4-three-triple-three-double-hyperplane-closure.md)
closes \(3^3 2^3 1^7\).  One formal double and seven singleton layers
give an exact three-dimensional kernel whose three row relations inject
into a cubic hyperplane shared by the two outside-double rows.  A
division-free characteristic-cubic invariant, compared over all three
formal-double choices, gives incompatible cyclic equations for the
three distinct double values.
[live-three-zero-eighth-split-k4-four-triple-mixed-layer-closure.md](live-three-zero-eighth-split-k4-four-triple-mixed-layer-closure.md)
closes \(3^4 2^2 1^6\).  Both double layers and all six singleton layers
give 28 legal pair-drop lifts in one degree-nine kernel.  The sharp
parity divisor and reduced-Wronskian argument make that kernel exactly
four-dimensional.  Its two row relations have degree-seven numerators;
the fourth-order cancellation \(n+5-12=n-7\) makes their differential
images multiples of one degree-ten contact divisor, forcing an
impossible injection into the constants.
[live-three-zero-eighth-split-k4-four-triple-single-double-pair-drop-closure.md](live-three-zero-eighth-split-k4-four-triple-single-double-pair-drop-closure.md)
closes \(3^4 2\,1^8\).  One double layer and eight singleton layers give
36 legal pair-drop lifts in a degree-ten kernel.  The sharp
degree-nineteen parity divisor and the eight singleton-square Wronskian
weights make that kernel exactly four-dimensional.  Its two row
relations would then inject into the constants.
[live-three-zero-eighth-split-k4-two-triple-five-double-linear-plane-closure.md](live-three-zero-eighth-split-k4-two-triple-five-double-linear-plane-closure.md)
closes \(3^2 2^5 1^6\).  Two selected doubles and all six singleton
layers give 28 pair-drop lifts in an exact four-dimensional degree-nine
kernel.  The two row relations fill a linear dual plane.  Every member
comes from an exact rational derivative, so its complementary
outside-double rows vanish; selected/outside swaps put four distinct
double values in one fibre of a quadratic rational map.
[live-three-zero-eighth-split-k4-nine-double-four-singleton-rainbow-closure.md](live-three-zero-eighth-split-k4-nine-double-four-singleton-rainbow-closure.md)
closes the terminal \(2^9 1^4\) profile.  Three selected doubles and all
four singleton layers give 21 pair-drop lifts in an exact
four-dimensional degree-eight kernel.  Its two relations fill a
quadratic dual plane, making six outside-double rows proportional.
Third differences across three disjoint swaps force a cube-root rainbow
coloring of \(K_6\); its three five-edge color classes would be disjoint
stars, which is impossible.
[live-three-zero-eighth-split-k5-eleven-double-one-singleton-matching-closure.md](live-three-zero-eighth-split-k5-eleven-double-one-singleton-matching-closure.md)
closes \(2^{11}1\), the all-double edge of the fifth-order pure frontier.
Five formal double layers give a relation pencil in the cubics.  After
quotienting by the singleton row, a fourth Boolean difference of one
outside-double row minor gives \(e_2=0\) on every near-perfect matching of
\(K_9\).  Quadratic fibres and an exact \(K_7\) incidence-rank lemma remove
all noncommon zero increments; a one-forbidden-edge propagation then makes
a four-matching monochromatic, contradicting \(e_2(t,t,t,t)=6t^2\).
[live-three-zero-eighth-split-k5-ten-double-three-singleton-projective-matching-closure.md](live-three-zero-eighth-split-k5-ten-double-three-singleton-projective-matching-closure.md)
closes \(2^{10}1^3\).  Four formal double layers and two formal singleton
layers give a relation pencil in the cubics.  Quotienting by the remaining
singleton row and taking a fourth Boolean difference produces the homogeneous
middle-coefficient equation on every perfect matching of \(K_8\).  For each
four/four split, its nondegenerate binary-quadratic pairing forces one side
to have a star/triangle equality pattern.  An exact 1,883-visit equality
backtrack forces a projectively monochromatic \(K_5\), contradicting the
quartic fibre bound for \(B\Phi_u-A\Phi_v\).
[live-three-zero-eighth-split-k5-formal-five-layer-increment.md](live-three-zero-eighth-split-k5-formal-five-layer-increment.md)
applies the all-order formal-five theorem exhaustively to the 42-profile
fifth-order ledger and closes exactly \(4^2 3^5\), \(3^5 2^4\), and
\(3^4 2^5 1\).  Their complementary root signatures are respectively
\((7,5),(5,1),(5,1)\), all with \(s>2c-10\).  The exact scan audits 1,365
five-layer choices and all 44,850 pair-core/zero-placement scenarios; no
other open profile passes the theorem.
[live-three-zero-eighth-split-k5-five-triple-saturated-cubic-robin-rectangle-closure.md](live-three-zero-eighth-split-k5-five-triple-saturated-cubic-robin-rectangle-closure.md)
closes \(3^5 2^3 1^2\) and \(3^4 2^4 1^3\).  In both cases the formal-five
complement is \(3^3 1^4\), whose four simple roots saturate the Wronskian
of a cubic relation pencil.  On the five-triple profile, the accessory
residue sum gives the same plus-pole Boolean rectangle as at fourth order.
On the four-triple profile, the top three accessory moments put all four
triple values on a fixed nonzero quadratic.  The checker also inventories
all 84 formal-five choices in the four open five-triple profiles.
[live-three-zero-eighth-split-k5-mixed-linear-plane-increment.md](live-three-zero-eighth-split-k5-mixed-linear-plane-increment.md)
closes \(3^3 2^4 1^6\) and \(3^4 2 1^9\).  Mixed role-two/role-one
pair drops make the common polynomial kernel exactly four-dimensional and
fill its entire linear dual plane.  Complementary residue rows then give a
quadratic-fibre contradiction in the first profile and a nonzero-unit
contradiction in the second.
[live-three-zero-eighth-split-k5-seven-double-formal-linear-plane-closure.md](live-three-zero-eighth-split-k5-seven-double-formal-linear-plane-closure.md)
closes \(3^3 2^7\).  Five selected doubles fill the same linear dual plane;
selected/complementary swaps would put six distinct double values in one
fibre of a nonzero quadratic rational map.
[live-three-zero-eighth-split-k5-unified-pair-drop-linear-plane-closure.md](live-three-zero-eighth-split-k5-unified-pair-drop-linear-plane-closure.md)
closes seven further profiles:
\(3^5 2^2 1^4,3^5 2\,1^6,3^5 1^8,3^4 2^3 1^5,
3^4 2^2 1^7,3^4 1^{11},3^3 2^6 1^2\).
The mixed role-two/role-one kernel remains four-dimensional even when the
triple--zero pair is the unique illegal core.  Five complementary classes
make its two dual relations the full linear plane; a simple-root residue
closes six profiles and a complementary-double swap closes the seventh.
The theorem and its 1,828,096-choice census were independently audited.
[live-three-zero-eighth-split-all-order-mixed-role-pair-drop-duality.md](live-three-zero-eighth-split-all-order-mixed-role-pair-drop-duality.md)
shows that the same kernel and dual target are independent of the
common-pole order: \(\deg A=k+8\) and the differentiated leading coefficient
is always \(n+(k+1)-(k+8)=n-7\).  It records local all-\(k\) consequences
without claiming that every higher-order profile admits the formal
selection.
[live-three-zero-higher-split-mixed-pair-drop-five-class-closure.md](live-three-zero-higher-split-mixed-pair-drop-five-class-closure.md)
extends the simple-root part to arbitrary \(h\ge8\).  With \(d\) role-two
layers, \(h+2-2d\) singleton layers, and at most one selected triple, the
strict square-Wronskian inequality displayed there forces a four-dimensional
lift span even after the possible triple--zero edge deletion.  A five-class
complement with a simple root is then impossible for every \(k\ge1\).
The proof was independently audited; it is a conditional profile theorem,
not an exhaustion of the higher-split frontier.
[live-three-zero-higher-split-low-role-selected-lift-incidence-closure.md](live-three-zero-higher-split-low-role-selected-lift-incidence-closure.md)
removes the five-class-complement hypothesis for \(d=0,1,2\) whenever
\(13-h+\max(0,5-k)>0\).  The exact common-pole order-\(k\) functional
forces the selected-row kernel to equal the four-dimensional lift span;
singleton quotient pencils and their hyperplane intersections then give a
contradiction for every complementary collision profile.  This covers all
\(k\) for \(9\le h\le12\), followed by the sharp small-order staircase
\((h,k)=(13,\le4),(14,\le3),(15,\le2),(16,1)\).  A five-space
osculating-Schubert model marks the boundary of pair incidence alone; it is
not asserted to realize a collision profile.
[live-three-zero-higher-split-row-relation-truncated-mass-bound.md](live-three-zero-higher-split-row-relation-truncated-mass-bound.md)
adds the complementary-polynomial compatibility missing from pair incidence.
If the selected-row kernel has dimension \(q\ge4\), its \(q-2\) exact row
relations inject into degree \(c-4\), and complementary jets force
\(\sum_i\min(m_i,q-2)\ge(q-2)(q+1)\).  In particular, a five-space needs
complementary mass at least eighteen after every multiplicity is capped at
three.  The same note audits why a naive triple drop would require an
unforced cubic divisor and therefore does not follow from the core Hermite
residual alone.
[live-three-zero-higher-split-q5-boundary-census.md](live-three-zero-higher-split-q5-boundary-census.md)
applies that bound exactly.  On the first unresolved diagonal \(h+k=18\),
it closes 417--649 applicable residual profiles in each row and leaves the
same fifty symbolic families \(3^a2^b1^{h+u}\), with
\(3a+2b+u=20\) and the stated \(d\le2\) applicability conditions.  At
\(h+k=19\) it leaves ninety-four families, allowing at most one part four.
The census explicitly stops giving standalone closure credit when a
six-dimensional selected kernel is no longer excluded.
[live-three-zero-higher-split-p18-six-triple-overlap-closure.md](live-three-zero-higher-split-p18-six-triple-overlap-closure.md)
and
[live-three-zero-higher-split-p18-five-triple-overlap-closure.md](live-three-zero-higher-split-p18-five-triple-overlap-closure.md)
begin the exact equality-case classification.  Simultaneous saturation of
the selected five-space and dual relation three-space gives canonical
low-degree Wronski fibres.  Comparing neighboring formal selections closes
all three six-triple families and all four five-triple families, uniformly
on the five \(h+k=18\) diagonal pairs.
[live-three-zero-higher-split-p18-four-triple-overlap-closure.md](live-three-zero-higher-split-p18-four-triple-overlap-closure.md)
closes the full four-triple range
\(3^4 2^b1^{h+8-2b}\), \(b=0,\ldots,5\).  At \(b=3\), eliminating the two
simple-root Robin rows gives a nonzero cubic which would have at least
fourteen singleton roots.  At \(b=4,5\), the canonical three-double
hyperplane and a selected/complementary swap force two distinct,
nonopposite values to have equal squares.  For \(b=0,1,2\), varying a sixth
singleton over a fixed five-row Robin space produces a pencil whose
Wronskian has too many roots.
[live-three-zero-higher-split-p18-three-triple-overlap-frontier.md](live-three-zero-higher-split-p18-three-triple-overlap-frontier.md)
closes the \(b=0,1,2,3,4,5\) profiles in the seven-family three-triple block.
Varying a third singleton puts the exact order-two residue numerator in a
fixed cubic two-jet kernel.  Letting the two anchors vary makes a fixed
Cauchy rational function constant on at least three singleton values; its
level set is a nonzero quadratic, closing \(b=3\) and independently
reclosing \(b=4,5\).  A selected/complementary double exchange supplies a
second audit of \(b=4,5\).  The note also records the sharp
\(3^3 2^4 1\) Schubert cubic and an admissible exact fibre.  On the
neighboring five-simple selection it obtains a fixed cubic pencil; its
local Schubert quadratic, varied over a third anchor, becomes a cubic
whose identical vanishing would force one scalar to equal both \(-3\)
and \(-4\).  This closes \(b=2\), but does not promote \(b=6\).
For \(b=1\), six fixed Robin anchors produce a sextic three-space whose
moving divisibility determinant vanishes identically.  Dividing its gcd
and applying the exact cross-product identity forces the primitive space
to be even; its Wronskian then has an extra factor \(z^3\), contradicting
the twelve nonzero-anchor weights that already exhaust its degree.  This
closes \(b=1\).  For \(b=0\), eight fixed singleton rows in the common
\(3^3 1^9\) complement produce two independent nonic numerator
relations.  Their fixed space is four-dimensional; every tangent-incidence
minor vanishes at the eight anchors and at least sixteen moving singleton
values, forcing the primitive space to be even.  Its extra Wronskian
factor \(z^6\) contradicts the twenty-four anchor weights that already
saturate the degree.
[live-three-zero-higher-split-p18-b6-two-simple-schubert-coupling.md](live-three-zero-higher-split-p18-b6-two-simple-schubert-coupling.md)
attacks that endpoint by coupling its \(3^3 2^4 1\) cubic selection to the
neighboring \(3^2 2^5 1^2\) selection through one shared accessory
baseline.  The normalized two-simple Wronski image has codimension two in
the quintics.  Its generic slope resultant has degree eleven, with both
singular slope charts audited separately; after the actual moving-root
substitution the degree budget is \(17+2+2\), so this is retained as a
frontier rather than promoted as a closure.  It does exclude a zero
singleton in the \(h=17\) endpoint and records the compact fifteen-pair
rational system for the next exact elimination.
[live-three-zero-higher-split-p18-b6-endpoint-selected-pair-closure.md](live-three-zero-higher-split-p18-b6-endpoint-selected-pair-closure.md)
performs that elimination without discarding any of the fifteen endpoint
pair equations.  After the Möbius change
\(t_v=2(r+v)/(r-v)\), each pair equation is a symmetric cubic in the
selected pair's sum and product.  Fixing one transformed double makes the
other five values roots of a common sextic; its constant and
next-leading coefficients force all six distinct values onto one nonzero
quadratic.  This closes \(b=6\).  Exactly thirty of the original fifty
symbolic families remain, all with at most two triples; every family with
at least three triples is closed.
[live-three-zero-higher-split-p18-two-triple-endpoint-frontier.md](live-three-zero-higher-split-p18-two-triple-endpoint-frontier.md)
audits the next nine-family block and separates it into the three common
complements \(3^2 1^{12}\), \(3^2 2^3 1^6\), and \(3^2 2^6\).  At the
high endpoint the bare \(\operatorname {Gr}(3,5)\)-to-sextic Wronski map
is dominant, with an exact squarefree, nonzero, nonopposite-root witness;
therefore no scalar Wronskian condition is credited.  The exact
second-jet residue rows nevertheless all lie in one annihilator plane,
giving a coupled rank-two system for all \(1+7+28\) endpoint selections.
The selected-triple neighbor \(3\,2^7 1\) maps birationally to an
irreducible quintic hypersurface in the septic coefficients, including
the zero-slope chart, and the \(b=8\) profile supplies sixteen coupled
copies with the same Cauchy exchange term as the preceding all-pair
closure.  This endpoint route is a frontier only and does not close
the endpoint by itself; its low packet is closed by the companions
immediately below, and only \(b=8\) remains after those companions.
[live-three-zero-higher-split-p18-two-triple-twelve-simple-cofactor-closure.md](live-three-zero-higher-split-p18-two-triple-twelve-simple-cofactor-closure.md)
closes the first common-complement packet \(a=2,b=0,1,2\).  Ten fixed
singleton anchors produce a six-space in degree fourteen.  The Wronskians
of its evaluation hyperplanes assemble into a bivariate cofactor; after
the ten anchor factors and the automatic diagonal factor are removed, it
has bidegree only \((5,9)\).  Moving singleton conditions force a reflected
fourth-power divisor.  For the two smallest \(b=2\) rows, the two
neighboring complementary-double selections supply the missing two
order-three interpolation points.  On the diagonal the reflected divisor
is incompatible with the ten nonzero anchor factors.  Thus twenty-three of
the fifty equality families are closed and twenty-seven remain; the
unresolved two-triple range is \(b=3,\ldots,8\).
[live-three-zero-higher-split-p18-two-triple-six-simple-three-double-cofactor-closure.md](live-three-zero-higher-split-p18-two-triple-six-simple-three-double-cofactor-closure.md)
closes the middle common-complement packet \(a=2,b=3,4,5\).  Four fixed
simple rows and the two normalized jets at each of three fixed doubles
again give effective weights ten and eleven in degrees fourteen and
thirteen.  The evaluation-hyperplane cofactor has fixed divisor
\(J_A^4V^8\) and the same quotient bidegree \((5,9)\).  For \(b=5\), the
two selected doubles are made complementary one at a time; multiplying
the three resulting relation numerators by
\((z-q)^3(z+q)^2\) supplies the two missing order-three interpolation
points.  The diagonal would force the degree-ten divisor \(J_AV^2\) into
\(z^4\) times a degree-six polynomial.  Thus twenty-six of the fifty
equality families are closed, twenty-four remain, and only \(b=6,7,8\)
survive in the two-triple block.
[live-three-zero-higher-split-p18-two-triple-four-five-double-cofactor-closure.md](live-three-zero-higher-split-p18-two-triple-four-five-double-cofactor-closure.md)
extends the invariant cofactor count to \(a=2,b=6,7\).  The two cases use
fixed simple/double anchor counts \((2,4)\) and \((0,5)\), so both have
effective weights eleven in degree thirteen and ten in degree fourteen.
Their evaluation-hyperplane quotient again has bidegree \((5,9)\).
Making either of the two selected doubles complementary supplies the two
order-three correction points, while the diagonal retains a nonzero
degree-ten divisor against a degree-six residual.  Thus twenty-eight of
the fifty equality families are closed, twenty-two remain, and only
\(a=2,b=8\) survives in the two-triple block.
[live-three-zero-higher-split-p18-two-triple-eight-double-common-lift-closure.md](live-three-zero-higher-split-p18-two-triple-eight-double-common-lift-closure.md)
closes that last two-triple endpoint.  Fixing one selected double and
multiplying each of the other seven endpoint three-spaces by its coprime
quintic exchange factor embeds them in one degree-nine kernel.  Any two
of the lifted three-spaces are disjoint, forcing kernel dimension at
least six, while the seven exact second-order residue rows contribute
Wronskian weight at least \(7(d-2)\) and force dimension at most five.
Thus all nine two-triple families are closed: twenty-nine of the fifty
equality families are closed and the twenty-one residual families have
at most one triple.
[live-three-zero-higher-split-p18-low-triple-singleton-common-lift-closure.md](live-three-zero-higher-split-p18-low-triple-singleton-common-lift-closure.md)
closes all twenty-one remaining equality families.  For every one-triple
profile and for the first ten zero-triple profiles, moving one selected
singleton transports the relation three-spaces by
\((z-q)^2(z+q)\) into a common kernel.  The complementary simple, double,
and fixed triple rows give the exact bound \(D^2+D\le19\), so the kernel is
the transported three-space.  Coprime cubic divisibility closes all but
\(3\,2^9 1^{h-1}\); there the kernel would be the full space of quadratic
multiples of two cubics, contradicting any complementary second-order row.
For \(2^{11}1^{h-2}\), fixing one selected double and moving the other ten
puts ten quintic three-spaces in a common degree-ten five-space.  Every
pairwise quintic product then belongs to the kernel.  At a third double,
the exact product-rule equations force seven values into one fibre of
\((5v+x)/(v^2-x^2)\), whose fibres have size at most two.  Hence all fifty
\(p=18\) equality families are closed for all five diagonal pairs.  A
[separate line-by-line reconstruction](live-three-zero-higher-split-p18-low-triple-independent-audit.md)
independently verifies the common triple row, both zero placements, the
sharp \(b=9\) test, and the eleven-double baseline and fibre count.
[live-three-zero-higher-split-p19-singleton-parity-common-lift-closure.md](live-three-zero-higher-split-p19-singleton-parity-common-lift-closure.md)
opens the next diagonal without a profile-specific Schubert calculation.
Moving one selected singleton transports its relation three-space by
\((z-q)^2(z+q)\) into a common kernel.  Five-capped complementary mass at
most 28 excludes a common five-space, so any two transported three-spaces
meet in a plane.  A sharp parity lemma, including the zero node and every
gcd stratum, shows that a degree-\(n\) three-space can carry cubic incidence
planes at at most \(n-2\) pairwise nonopposite values.  This closes 57 of
the 94 \(p=19\) families.
[live-three-zero-higher-split-p19-double-common-lift-closure.md](live-three-zero-higher-split-p19-double-common-lift-closure.md)
closes 14 disjoint dense-double families.  Fixing one selected double and
moving the second lifts the relation three-spaces by coprime quintics into
a kernel of dimension at most five.  Below degree ten their pairwise
intersection is impossible; at degree ten every pairwise quintic product
lies in the kernel, and one common exact second-order row forces three
distinct values into a fibre of \((5v+x)/(v^2-x^2)\), whose fibres have
size at most two.
[live-three-zero-higher-split-p19-triple-common-lift-closure.md](live-three-zero-higher-split-p19-triple-common-lift-closure.md)
adds four disjoint moving-triple families.  Its even quartic transport
converts the selected simple row to the baseline triple row exactly.
Subcritical degrees give disjointness; at degree eight the third-jet
complete graph makes every four transformed values have the same sum, so
five distinct values are impossible.  The three independently audited
theorems close 75 of 94 families.
[live-three-zero-higher-split-p19-c6-parity-pencil-coupling.md](live-three-zero-higher-split-p19-c6-parity-pencil-coupling.md)
then couples the first equality-pencil block.  The common transported
kernel is exactly four-dimensional.  Intersections of its moving
hyperplanes close pool sizes two through four by coprime cubic degree,
and at pool size five force all triple products into the kernel; one exact
baseline row would put four distinct values in a fibre of
\((3v+x)/(v^2-x^2)\), which has size at most two.  This closes six more
families.  For every remaining \(C=6\) pool, all lifted square pencils lie
in the kernel of one global parity map
\(\bigwedge^2K\to\mathbb C[x]_{\le3}\), and a Klein-line/gcd argument
forces that map to have rank at most three.  The theorem and its census
passed a separate line audit.  Thus 81 of 94 families are closed and the
residual 13-family census is exact: four \(C=6\) profiles have pool sizes
six through eight, two further \(C=6\) profiles have pool size one, and
seven profiles have \(C=7,8,9\).  Four residuals
also lie on the degree-eleven quintic-pair-pencil surface.  The resulting
plane section is classified in the next theorem.
[live-three-zero-higher-split-p19-c6-saturated-klein-plane-closure.md](live-three-zero-higher-split-p19-c6-saturated-klein-plane-closure.md)
closes all four residual \(C=6\) profiles with pool size six, seven, or
eight.  Their common four-space exactly saturates its Wronskian cap.  A
zero pool would already cost six rather than three ramification units, so
all pool points are nonzero; equality then makes the series base-point-free
with local sequence \((0,2,3,4)\) and no unlisted ramification.  After the
global parity divisor is removed, the secant lines of the evaluation curve
form a degree-at-most-three curve spanning at most a plane in the Klein
quadric.  Rank zero, Klein lines, and beta planes force degeneracy; an alpha
plane forces too many transported hyperplanes to coincide; and a genuine
conic is a quadric ruling admitting no stationary local section.  The
zero/gcd and degenerate-plane branches passed a separate line audit.  Thus
85 of 94 \(p=19\) families are closed and nine remain: two \(C=6\) pool-one
profiles, four \(C=7\), two \(C=8\), and one \(C=9\).
[live-three-zero-higher-split-p19-undecic-singleton-double-coupling-closure.md](live-three-zero-higher-split-p19-undecic-singleton-double-coupling-closure.md)
closes the four profiles lying simultaneously on the degree-nine
moving-singleton boundary and the degree-eleven moving-double boundary.
For pool size four, exact triple intersections make one universal
three-space of pairwise cubic products; varying the selected double pair
puts every double row on its degree-twelve Wronskian and exceeds the cap.
For pool size three, one fixed cubic-pair product times six moving
quintics violates a Vandermonde independence bound in the common
five-space.  At pool size two, every dense pair intersection is forced to
one intrinsic quintic-pair line.  Singleton first-jet symmetry determines
its linear factor, and the common double row gives a bidegree-\((6,6)\)
identity on a nine-vertex clique.  Interpolation makes that identity
global, while its exact double-pole coefficient has a nonzero linear term.
Every dimension, zero, and denominator branch passed a separate symbolic
audit.  Thus 89 of 94 \(p=19\) families are closed and exactly five remain.
[live-three-zero-higher-split-p19-five-triple-even-span-closure.md](live-three-zero-higher-split-p19-five-triple-even-span-closure.md)
closes the two one-quartic five-triple profiles.  Pairwise intersections of
the moving even-quartic transports put all off-diagonal products
\((z^2-a_i^2)^2(z^2-a_j^2)^2\) in one degree-eight kernel.  Four distinct
Veronese-conic points make those products span
\(\mathbb C[z^2]_{\le4}\), while \((z^2-v^2)^3\) at any nonzero triple
value violates the common exact third-order row.  The optional double,
formal selections, zero allowance, and full span were independently
reconstructed in
[the separate audit](live-three-zero-higher-split-p19-five-triple-even-span-independent-audit.md).
Thus 91 of 94 \(p=19\) families are closed and the exact remaining frontier
is \((0,9,3),(0,10,1),(1,8,2)\).
[live-three-zero-higher-split-p19-c7-developable-secant-closure.md](live-three-zero-higher-split-p19-c7-developable-secant-closure.md)
closes the two \(C=7\) profiles \((0,9,3)\) and \((1,8,2)\).
Their common four-spaces exactly saturate the Wronskian bound.  The parity
quotients give degree-at-most-four curves of secant lines with at least
five stationary pool sections, so the second fundamental determinant
vanishes identically.  Cones fail a direction-Wronskian and signed-zero
count; decomposable tangent edges become planar under projection from the
fixed line; and the sole symplectic splitting \((d,e)=(4,3)\) has too few
quotient zeros.  The separate audit in
[independent-audit-live-three-zero-higher-split-p19-c7-developable-secant-closure.md](independent-audit-live-three-zero-higher-split-p19-c7-developable-secant-closure.md)
checks homogeneous degree drops, common Pluecker factors, infinity, and the
distinct \(\pm q\) zeros.  Thus 93 of 94 \(p=19\) families are closed; the
sole survivor is \((0,10,1)\), namely \(2^{10}1^{h+1}\).
[live-three-zero-higher-split-p19-c8-singleton-pair-line-clique-closure.md](live-three-zero-higher-split-p19-c8-singleton-pair-line-clique-closure.md)
closes that final endpoint with the one-double formal complement
\(2^9 1\).  Removing the selected double transports ten relation
three-spaces by the quintics \((z-i)^3(z+i)^2\) into one degree-eleven
kernel.  Its common singleton row rules out every full pair pencil and
normalizes each intrinsic intersection line to slope
\(\Lambda-a_i-a_j\).  A common double row produces a cleared
bidegree-\((6,6)\) equation on the nine remaining double values; strict
grid interpolation makes it an identity, while the excluded-pole
coefficient has linear term \(-(v-r)x\ne0\).  The exact checker and an
[independent line audit](live-three-zero-higher-split-p19-c8-singleton-pair-line-clique-independent-audit.md)
cover all formal selections, common units,
dimension branches, zero-singleton placement, and the final pole limit.
Thus the complete \(p=19\) equality ledger is \(94/94\).
[live-three-zero-higher-split-uniform-developable-secant-lemma.md](live-three-zero-higher-split-uniform-developable-secant-lemma.md)
extracts the stationary-secant mechanism as a parameter-uniform theorem.
In the moving-singleton common-lift setup, four-capped complementary mass
\(M_4=19\), \(4\le C\le7\), and
\(P\ge\max(1,2C-9)\) force the common kernel to be a primitive saturated
four-space.  After every finite or infinite Pluecker gcd and degree drop is
removed, the parity quotient is a degree-at-most-\(C-3\) curve of lines;
the pool sections force it to be developable, and exact cone,
decomposable-tangent, and symplectic-tangent degree bounds exclude every
branch.  This closes, uniformly for \(13\le h\le19\), the four \(p=20\)
families
\(5\,2^7 1^{h+3}\), \(5\,3\,2^6 1^{h+2}\),
\(5\,3^2 2^5 1^{h+1}\), and \(5\,3^3 2^4 1^h\).
The
[independent audit](live-three-zero-higher-split-uniform-developable-secant-lemma-independent-audit.md)
reconstructs the common-lift hypotheses, Wronskian saturation, homogeneous
degree drops, all developable branches, and the selected-kernel dimension
needed by the \(p=20\) corollary.  The theorem does not cover \(C=6,P=2\),
\(C=7,P\le4\), \(C\ge8\), or unsaturated \(M_4=20\) families.
[live-three-zero-higher-split-p28-six-kernel-boundary.md](live-three-zero-higher-split-p28-six-kernel-boundary.md)
identifies the first selected six-dimensional-kernel boundary.  The
selected Wronskian gap excludes dimension six for \(p\le27\); at \(p=28\)
it is zero exactly for
\((h,k)=(22,6),(23,5),(24,4),(25,3),(26,2),(27,1)\), while dimension
seven still has excess twelve.  The exact split censuses have
824, 824, 872, 872, 920, and 920 candidates, all currently classified
\(R\).  Uniform moving-singleton cubic, moving-triple quartic, and
moving-double quintic lifts force an explicit selected kernel of dimension
at most five in 335 of the common 344-profile \(d\le2\) ledger.  The nine
residual tuples restore to the four saturated cores
\(3^{10}\), \(4^2 3^7 1\), \(4^3 3^6\), and \(4^7 1\).
The
[independent audit](live-three-zero-higher-split-p28-six-kernel-boundary-independent-audit.md)
reconstructs every formula, route status, count, transport threshold, and
residual core.  This is registered strictly as a dimension-drop frontier:
none of the 335 profiles is thereby closed, and the nine cores are not an
exhaustion of arbitrary-role selections.
[live-three-zero-higher-split-p28-all-triple-tangent-involution-drop.md](live-three-zero-higher-split-p28-all-triple-tangent-involution-drop.md)
forces the next two dimension drops.  If all ten moving-triple selections
over the \(3^{10}\) baseline had dimension six, each saturated relation
four-space would identify its tangent lines at nine opposite pairs.  After
the unique simple tangent base factor is removed, eighteen signed roots
force the degree-at-most-seventeen tangent cross-minors to vanish.  The
resulting involution is impossible: its generically distinct branch lies
in a fixed projective line, while its proportional branch is the complete
even cubic system and cannot be stationary at the selected nonzero point.
The
[independent audit](live-three-zero-higher-split-p28-all-triple-tangent-involution-drop-independent-audit.md)
checks every saturation, infinity, root-count, and proportionality branch.
It covers exactly \((0,10,0,0)\) and \((0,10,1,-2)\), bringing the
\(d\le2\) dimension-drop ledger to \(337/344\), not closing either profile.
[live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier.md](live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier.md)
then determines the complete selected-kernel distribution on that same
\(3^{10}\) core.  A five-dimensional common kernel would force at least
seven even relation transports into one even hyperplane and contradict the
ten exact order-three rows.  In dimension six, any hypothetical \(q=6\)
selection produces a developable line curve; the exact cone and tangent-edge
classification, including finite and infinite cuspidal branches, forces an
unlisted Wronskian zero.  Hence the common kernel has dimension exactly six
and all ten selections have \(q=5\).  Their signed Hermite four-minors factor
as
\(\prod_{\nu=1}^{10}(t-a_\nu^2)Q(t)\), where \(Q\) is a nonzero
decomposable \(\bigwedge^4\mathbb C^6\)-valued polynomial of degree at most
four.  The
[independent audit](live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier-independent-audit.md)
found and repaired a material tangent-frame error in the cuspidal-sextic
calculation, then reconstructed the corrected Wronskian obstruction and all
remaining branches.  This is a strict frontier sharpening, not a closure of
either all-triple profile; the residual Grassmannian quartic still requires
new incidence or an unreduced equation.
[live-three-zero-higher-split-p28-all-triple-residual-quartic-balanced-splitting.md](live-three-zero-higher-split-p28-all-triple-residual-quartic-balanced-splitting.md)
sharpens that survivor to one exact bundle type.  Removing the coordinate
gcd and the possible infinity basepoint gives a morphism
\(\mathbb P^1\to\operatorname{Gr}(4,6)\) of degree at most four.  A
constant annihilator row would be a relation among the six basis
polynomials; differentiating a linear row produces the same forbidden
constant relation.  Thus the rank-two annihilator bundle must split as
\(\mathcal O(-2)\oplus\mathcal O(-2)\), the projective degree is exactly
four, and the original residual coordinates have no scalar gcd.  The
[independent audit](live-three-zero-higher-split-p28-all-triple-residual-quartic-balanced-splitting-independent-audit.md)
checks scalar division, the homogeneous infinity fiber, determinant degree,
and the polynomial minimal row.  A basepoint-free quadratic-pair model shows
that the bundle statement alone is not contradictory; the next step must
combine its two quadratic rows with the derivative span and the ten exact
Hermite roots.
[live-three-zero-higher-split-p28-all-triple-balanced-annihilator-closure.md](live-three-zero-higher-split-p28-all-triple-balanced-annihilator-closure.md)
performs that final combination and closes both \(3^{10}\) residual tuples.
The identities
\(\lambda E=\lambda E'=0\) and
\(\mu E=\mu E'=0\), together with their odd counterparts, put \(E,O\)
in the derived kernel of the two quadratic annihilator rows.  At generic
tangent rank two, deficient coefficient span makes the derivative
four-wedge zero, while full span makes its scalar a polynomial square,
contradicting the ten distinct Hermite factors.  At generic tangent rank
one, the balanced developable classification leaves only tangent lines to
a rational normal cubic.  That normal form puts
\(A(z)\mathbb C[z^2]_{\le3}\) inside the common six-space and forces an
unlisted Wronskian zero at \(z=0\).  The
[independent audit](live-three-zero-higher-split-p28-all-triple-balanced-annihilator-closure-independent-audit.md)
reconstructs all coefficient-span strata, the primitive Hodge comparison,
the finite/infinite tangent classification, and the square-cover
ramification.  This is a profile closure exactly for
\((0,10,0,0)\) and \((0,10,1,-2)\) on the six \(p=28\) equality splits;
it does not close the \(4^3 3^6\), \(4^7 1\), or unrestricted-role
frontiers.
[live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop.md](live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop.md)
adds the two \(4^3 3^6\) tuples.  Every pair of active quartic transports
would fill the exact intersection
\(B_iB_j\mathbb C[z]_{\le1}\).  Five pair products from four distinct
squares span \(\mathbb C[z^2]_{\le4}\), and their odd multiples give a
ten-dimensional direct sum inside a kernel of dimension at most six.  The
[independent audit](live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop-independent-audit.md)
reconstructs the determinant and all selection bookkeeping.  Thus the
dimension-drop ledger is \(339/344\); the five unreduced tuples restore
only to \(4^2 3^7 1\) and \(4^7 1\).  These are still dimension-drop
statements, not profile closures.
[live-three-zero-higher-split-uniform-moving-triple-critical-span-bound.md](live-three-zero-higher-split-uniform-moving-triple-critical-span-bound.md)
extracts the pair-product mechanism at the first general row-relation
threshold \(p=r(r+3)\).  For an exact restored moving-triple baseline of
mass \((r+1)(r+2)\), at most one maximal \((r+2)\)-kernel selection can
occur when \(c\le r+4\), and at most three can occur when \(c=r+5\).
Four active values would make five even quartic pair products span
\(\mathbb C[z^2]_{\le4}\); their multiples through degree \(r-3\) fill
all of \(\mathbb C[z]_{\le r+5}\), contradicting the exact-row Wronskian
bound \(\dim\mathcal K\le r+2\).  The
[independent audit](live-three-zero-higher-split-uniform-moving-triple-critical-span-bound-independent-audit.md)
reconstructs the baseline-row/gcd scope, determinant, multiplication span,
and subcritical range.  At \(p=28\) it strengthens the \(4^3 3^6\)
conclusion to at least three selected kernels of dimension at most five;
it remains a dimension-drop theorem and says nothing for \(c\ge r+6\).
[live-three-zero-higher-split-critical-moving-triple-local-jet-q6-cap.md](live-three-zero-higher-split-critical-moving-triple-local-jet-q6-cap.md)
sharpens the critical \(c=r+5\) line from at most three maximal selections
to at most one.  If two maximal transports existed, their dimension lower
bound would fill
\(B_iB_j\mathbb C[z]_{\le r-3}\).  Dividing by \(B_i\) puts
\(B_j(z-j)\) in the relation space selected at \(i\), but the other moving
value \(j\) is still an exact complementary triple and its regular-unit
third-jet row is nonzero on that polynomial.  The
[independent audit](live-three-zero-higher-split-critical-moving-triple-local-jet-q6-cap-independent-audit.md)
checks the factor orientation, local unit, and both \(p=28\) tuple
families.  Hence the \(4^3 3^6\) core has at least five exact \(q=5\)
selections.  This sharpens only their dimension distribution and does not
close either profile.
[live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation.md](live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation.md)
then couples all six selections and proves the strict surviving normal
form.  A cleared Robin cubic has coefficient minor \(16i^2\), so four
partner squares exclude a five-dimensional common kernel.  If a sole
\(q=6\) selection remained, the same cubic family would span its relation
four-space; its nonzero degree-at-most-seven Wronskian would then have the
factor \(z(z-i)^3\) and five further complementary-triple roots, an
impossible total of nine.  Thus the common kernel is exactly six and all
six selections have \(q=5\).  Its signed residual four-wedge is nonzero:
the cone and tangent-line alternatives each force forbidden ramification
at the square-cover branch point.  After primitive-gcd removal, generic
tangent rank two forces degree six, \(L\simeq\mathcal O(-4)^2\), and only
annihilator splittings \((2,4)\) or \((3,3)\).  The
[independent audit](live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation-independent-audit.md)
reconstructs the Robin sign, Vandermonde, sole \(i=0\) rank exception,
Wronskian root count, homogeneous bundle ledger, and both developable
branches without importing the primary checker.  Exact artifacts
`computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_q5_saturation.py`
and
`computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_q5_saturation_independent_audit.py`
pass.  This is a strict normal-form theorem, not a closure of either
\(4^3 3^6\) profile; the generic tangent-rank-one branch and the two
generic-rank-two degree-six splittings remain live.
[live-three-zero-higher-split-p28-three-quartic-six-triple-rank-one-closure.md](live-three-zero-higher-split-p28-three-quartic-six-triple-rank-one-closure.md)
now closes the omitted generic-rank-one branch.  Duality turns the
rank-one second fundamental map into a developable annihilator line curve.
The cone would give a forbidden constant section of the negative
annihilator bundle.  The tangent-edge ramification ledger leaves only
edge-span dimensions four and five.  In dimension four, the
osculating-dual quotient supplies a nonzero square-pulled section of order
at least six at \(z=0\); in dimension five, the sole rational-normal
quartic frame gives the same \(z^6\) factor explicitly.  Either creates an
unlisted Wronskian root after the nine prescribed rows have saturated all
degree twenty-four.  The
[independent audit](live-three-zero-higher-split-p28-three-quartic-six-triple-rank-one-closure-independent-audit.md)
reconstructs the focal-line dichotomy, includes ramification at infinity,
checks the osculating-dual bundle map and the full quartic kernel module,
and also excludes generic rank zero.  Exact artifacts
`computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_rank_one_closure.py`
and
`computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_rank_one_closure_independent_audit.py`
pass.  Thus only the generic-rank-two splittings \((2,4)\) and \((3,3)\)
remain for this profile.
[live-three-zero-higher-split-p28-kernel-orientation-countermodel.md](live-three-zero-higher-split-p28-kernel-orientation-countermodel.md)
blocks one tempting shortcut on the \((2,4)\) branch.  At one moving
square it constructs an exact degree-nine local model whose positive sheet
has vanishing sequence \((0,1,2,4,5,6)\), whose opposite sheet is
unramified, and whose residual determinant has a simple zero, but the
derivative kernel is \([0:1]\), not the selected point \([1:1]\).  The
[independent audit](live-three-zero-higher-split-p28-kernel-orientation-countermodel-independent-audit.md)
reconstructs both sheet jets, the wedge gcd, the kernel, and polynomial
rank without importing the primary checker.  Thus opposite-sheet
minimality alone cannot orient the quadratic row.
[live-three-zero-higher-split-p28-three-quartic-cubic-pair-intersection-frontier.md](live-three-zero-higher-split-p28-three-quartic-cubic-pair-intersection-frontier.md)
then audits the \((3,3)\) intersection mechanism.  The elementary shifted
pair gives only the already excluded \((2,2)\) splitting and a square
four-wedge scalar.  A transverse exact rational pair does give primitive
splitting \((3,3)\), echelon degrees \(4,\ldots,9\), and a squarefree
residual sextic, while its ordinary degree-twenty-four Wronskian remains
squarefree.  Its
[independent audit](live-three-zero-higher-split-p28-three-quartic-cubic-pair-intersection-frontier-independent-audit.md)
checks the two coefficient spans, Crum constant, residual determinant,
endpoint guards, and the norm/jet-minor formulation.  Hence intersection
dimension alone is not a contradiction.  The finite next test must impose
simultaneously the norm factorization, exact Wronskian factorization, and
all triple/quartic jet-minor divisibilities, with their open guards.
[live-three-zero-higher-split-p28-two-quartic-seven-triple-robin-pair-plane-drop.md](live-three-zero-higher-split-p28-two-quartic-seven-triple-robin-pair-plane-drop.md)
closes the maximal-selection branch for the two residual
\(4^2 3^7 1\) tuples.  Four hypothetical six-dimensional selections
force every pair intersection to be its full fixed-singleton Robin plane.
Five even pair products supply a fixed five-space; when the singleton is
nonzero, two Robin quotient classes raise the span to seven, while the
zero-singleton branches have rank ten or force an even six-space whose
Wronskian misses every repeated node.  The
[independent audit](live-three-zero-higher-split-p28-two-quartic-seven-triple-robin-pair-plane-drop-independent-audit.md)
checks that only four active values are used.  Hence at most three of the
seven selections have dimension six and at least four have dimension at
most five.  The \(d\le2\) drop ledger is now \(341/344\), with precisely
the three \(4^7 1\) tuples unreduced; this still does not close either
\(4^2 3^7 1\) profile.
[live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap.md](live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap.md)
couples different complementary-singleton choices for each fixed triple.
The two moving-singleton transports lie in a degree-nine common kernel;
its exact restored rows exclude dimension five.  If two choices both had
dimension six, their transported four-spaces would fill the common kernel
and force the full cubic-multiple space, on which the fixed simple row is
nonzero.  The
[independent audit](live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap-independent-audit.md)
rechecks the role indexing, conditional \(q=4\) exclusion, gcd corrections,
and zero-singleton resultant.  Thus each triple row of the selection grid
has at most one \(q=6\) entry, and at least \(h-6\) or \(h-8\) singleton
columns are entirely \(q=5\).  This is the exact input for a new
multi-selection coupling, not a profile closure.
[live-three-zero-higher-split-p28-two-quartic-q5-grid-closure.md](live-three-zero-higher-split-p28-two-quartic-q5-grid-closure.md)
uses that full grid to close both residual \(4^2 3^7 1\) tuples.  Pairwise
singleton transport places every five-dimensional row-relation system over
one fixed triple above a common cubic plane.  An all-\(q=5\) singleton
column then gives seven planes in a four-space of degree-seven polynomials.
A characteristic-zero parity classification forces that four-space to be
\((\alpha+\beta z)\mathbb C[z^2]_{\le3}\), which violates one surviving
exact order-three row.  The
[independent audit](live-three-zero-higher-split-p28-two-quartic-q5-grid-closure-independent-audit.md)
reconstructs the selected/complementary indexing, the full local-unit
cancellation including a zero singleton, all five projection-rank branches,
and the terminal derivative.  This is a genuine profile closure only for
\((2,7,0,1)\) and \((2,7,1,-1)\) on the six \(p=28\) equality splits; it
does not close the unrestricted-role ledger or any other dimension drop.
[live-three-zero-higher-split-p28-all-quartic-pure-fifth-pole-frontier.md](live-three-zero-higher-split-p28-all-quartic-pure-fifth-pole-frontier.md)
shows sharply why the remaining \(4^7 1\) core does not drop by the same
one-selection method.  Its relation space is all of
\(\mathbb C[z]_{\le3}\) exactly when the degree-thirty selected section
lies in the seven-space of pure fifth-pole numerators
\(\operatorname{span}\{(B/(z-a_i))^5\}\).  The
[independent audit](live-three-zero-higher-split-p28-all-quartic-pure-fifth-pole-frontier-independent-audit.md)
proves both directions through local principal-part contact and moment
cancellation, and independently verifies twelve separated exact
\(q=6\) formal models: every \(d=0\) split, \(d=1\) for \(k\le4\), and
\(d=2\) for \(k\le2\).  These models are not tensor realizations, but they
prove that the selected highest jets and common-pole row alone cannot
force a dimension drop; a second selection or unreduced global equation
is essential.
[live-three-zero-eighth-split-k5-three-double-second-jet-closure.md](live-three-zero-eighth-split-k5-three-double-second-jet-closure.md)
closes \(3^3 2^3 1^8\).  The full linear dual space kills both logarithmic
jets at the two complementary doubles.  Swapping the selected and outside
double makes the three double values pairwise isotropic for
\(5a^2+2ab+5b^2\); subtracting the pair equations forces two distinct
values to coincide.  The elimination signs were independently audited.
[live-three-zero-eighth-split-k5-two-double-second-jet-boundary.md](live-three-zero-eighth-split-k5-two-double-second-jet-boundary.md)
shows sharply why the same direct-jet route stops at the
\(3^3 2^2 1^{10}\) profile.  An exact rational degree-ten singleton
polynomial is squarefree, coprime to its sign reversal, separated from all
structural values, and simultaneously satisfies all ten direct
complementary residue jets.  It is a local boundary model, not a profile
realization or counterexample; selected-lift incidence closes the profile
by a stronger mechanism below.
[live-three-zero-eighth-split-all-order-ten-singleton-incidence-closure.md](live-three-zero-eighth-split-all-order-ten-singleton-incidence-closure.md)
proves uniformly that every formal selection of ten singleton layers is
impossible.  Two quotient-pencil arguments use saturated parity, exact gcd
costs, and square-variable ramification: a degree-eight pencil can carry at
most six nonzero cubic nodes but receives at least eight, while the final
degree-five pencil can carry at most three but receives at least seven.
[live-three-zero-eighth-split-all-order-low-mixed-role-incidence-closure.md](live-three-zero-eighth-split-all-order-low-mixed-role-incidence-closure.md)
extends the selected-incidence obstruction to every formal selection with
\(d=1,2,3\) repeated role-two layers.  It includes the possible zero
singleton and unique triple--zero missing edge.  Singleton incidence planes
are excluded by parity and exact-row gcd costs; the remaining hyperplane
intersections demand products of three or four cubic factors beyond the
ambient degree.  The argument stops without credit at \(d=4\).
[live-three-zero-eighth-split-all-order-four-double-two-singleton-incidence-closure.md](live-three-zero-eighth-split-all-order-four-double-two-singleton-incidence-closure.md)
closes that final \(d=4\) boundary.  Neither singleton cubic can divide the
four-space.  Two incidence planes have incompatible canonical intersection
lines; one plane and one hyperplane are excluded by an exact quadratic
parity numerator followed by the selected order-two rows; and two
hyperplanes reduce to a nonzero bidegree-\((2,2)\) repeated-pair
determinant.  The proof includes both zero-singleton placements and the
unique missing triple--zero edge.
[live-three-zero-eighth-split-all-order-mixed-role-census.md](live-three-zero-eighth-split-all-order-mixed-role-census.md)
gives the exact all-order consequence census.  It separates formal
selection, \(c<5\), the \(c=5\) simple-root closure, the strict simple-root
Wronskian bound, first- and second-jet double swaps, and selected incidence.
All complementary-root closures lie in a rigorously finite low-order
window, while incidence now closes every \(d\le4\) selection uniformly.
There is no formally applicable open tail; the remaining profiles fail the
mixed-role selection criterion altogether.
[live-three-zero-eighth-split-all-order-five-double-six-class-residue-closure.md](live-three-zero-eighth-split-all-order-five-double-six-class-residue-closure.md)
extends the kernel and duality to five exact-double layers.  For
\(C=11,n_2\ge8,n_1\ge1\), a simple complementary root supplies the square
relation in a quadratic dual plane.  Varying three complementary doubles
then puts five or seven values in one fibre of a degree-two rational map.
At fifth order this closes the final profile \(3^2 2^8 1\).
[live-three-zero-eighth-split-stable-double-five-set-swap-frontier.md](live-three-zero-eighth-split-stable-double-five-set-swap-frontier.md)
keeps the same endpoint relation pencil in its fixed numerator space
\(\mathbb C[z]_{\le7}\), even when the complementary target grows.  Its
Wronskian is \(Q_T^2E_T\) with \(\deg E_T\le2\), and an exact Bezout
identity links it to the complementary image.  Riemann--Hurwitz plus the
contact operator excludes selected base points: the associated rational map
has degree six or seven, all five selected points have ramification weight
two, and at most two further ramification units remain.  The note also
proves that adjacent derivative pencils intersect in dimension at most one
and records the exact background-row rank condition.  These are bounded
overlap invariants for the persistent all-double tail, not yet its closure.
[live-three-zero-eighth-split-sixth-order-twelve-double-common-lift-closure.md](live-three-zero-eighth-split-sixth-order-twelve-double-common-lift-closure.md)
closes the first stable all-double case \((h,k;\lambda)=(8,6;2^{12})\).
Fixing four selected doubles and varying the fifth embeds eight cubic
multiplier pencils into one common octic exactness kernel.  Exact
order-two rows and pairwise-coprime fifth-value factors make that kernel
four-dimensional.  Its even/odd decomposition gives eight rank-two jet
conditions; the five possible odd-projection ranks are excluded by one
quartic fibre equation, three low-degree Wronskian bounds, and the pure-even
hyperplane span.  This is a characteristic-zero closure, not a finite
specialization, but its nonic successors still require a new argument.
[live-three-zero-eighth-split-stable-double-nonic-common-lift-closures.md](live-three-zero-eighth-split-stable-double-nonic-common-lift-closures.md)
closes both nonic successors, \(2^{13}\) at \(k=8\) and \(2^{12}1\) at
\(k=7\).  Their eight or nine fifth-choice planes lie in a common
four-dimensional nonic exactness kernel.  In the square variable, lower
odd-projection ranks violate corrected Wronskian bounds.  At full odd rank,
a degree-nine cofactor becomes globally tangent even in the eight-point
case; the exact tangent-hyperplane root classification then leaves a
nonzero quadratic or quartic fibre polynomial with too many
noninflection values.  The next common-kernel boundary is decic, where
five-dimensional equality and the lines \(\mathbb C A_aA_b\) first appear.
[live-three-zero-eighth-split-stable-double-decic-four-space-closure.md](live-three-zero-eighth-split-stable-double-decic-four-space-closure.md)
separates those two decic phenomena.  It excludes every common-kernel
dimension at most four without assuming that the lifted planes are
disjoint.  The singleton profile \(2^{13}1\) at \(k=9\) is therefore
closed outright.  For the pure profile \(2^{14}\) at \(k=10\), the only
surviving branch is a five-dimensional Wronskian equality.  The decic
parity proof uses a new codimension-two pure-even wedge obstruction and an
exact twenty-coefficient tangent lemma whose fibre bounds are four, six,
and six for the three binary-quartic inflection types.
[live-three-zero-eighth-split-fourteen-double-five-space-saturation-frontier.md](live-three-zero-eighth-split-fourteen-double-five-space-saturation-frontier.md)
closes the sole surviving pure decic branch.  Its common kernel would be a
gcd-free five-space with Wronskian exactly
\(c\prod_{a\in P}(z-a)^3\), local vanishing sequence
\((0,1,3,4,5)\), and a three-plane \({\cal V}_a\) whose opposite two-jet
has rank at most one.  The graph defined by
\({\cal U}_a\cap{\cal U}_b=\mathbb C A_aA_b\) has maximum degree two, but
an exact ten-node rational-normal-quartic Grassmann model realizes the
empty graph together with all abstract plane and rank incidences, so edge
counting alone cannot close \(2^{14}\).  The common polynomial origin of
the paired jets produces the exact covariant
\(D_{\cal K}(x)=x^6C(x)^2R(x)\) with \(\deg R\le10\).  Equal-degree
Plücker coordinates have different Wronskian and paired-covariant weights,
so \(R\) is not recoverable from \(\operatorname{Wr}({\cal K})=C^3\)
alone.  Four-row incidence supplies the missing factor and excludes the
zero alternative, giving
\(J=\kappa C(x)^2C(-x)\) and \(R=\kappa C(-x)\).
Corrected Wronskian caps exclude odd-projection ranks two and three.
For rank four, a cofactor quotient of component degree at most four makes
\(Q\cdot O''\) a degree-six scalar with nine roots, forcing \(C\) even.
For rank five, the moving Taylor basis
\((u-w)^2,(u-w)^3,(u-w)^4\) gives
\(P_0'=(L\times N)_0+3P_1\); the degree-four quotient of \(P_0\)
vanishes at all ten pool squares and again forces \(C\) even.  Both
contradict \(P\cap(-P)=\varnothing\), completing the pure profile
\(2^{14}\).
[live-three-zero-eighth-split-next-stable-undecic-common-kernel-frontier.md](live-three-zero-eighth-split-next-stable-undecic-common-kernel-frontier.md)
gives the exact next ledger for \(2^{14}1\) at \(k=11\) and \(2^{15}\)
at \(k=12\).  Both degree-eleven common kernels have dimension at most
five; dimensions two, three, and four are impossible.  The new pair-multiple
space is \(A_aA_b\mathbb C[z]_{\leq1}\), so the decic product-line
argument no longer removes dimension four by itself.  Corrected parity counts close
all four-space ranks except full odd rank, where
\(\operatorname {rank}(E',O,O')\le2\) holds identically.  Writing its
tangent coefficient as \(\beta=N/D\), the eight-unit Wronskian divisor of
the odd four-space gives \(\deg D\le2\), \(\deg N\le3\).  Second-jet-bad
pool points cost at least two ramification units.  The other nodes force
the degree-six equation \(N(a^2)+aD(a^2)=0\); seven regular nodes close the
pure profile, while the singleton equality case exhausts ramification and
improves this equation to degree two with six roots.  Thus no four-space
survives.  For a
five-space, differentiating the four-row cofactor
\({\cal P}=*(E\wedge E'\wedge O\wedge O')=\Delta Q\) gives
\({\cal P}'\cdot O''=\det(E,E'',O,O',O'')\).  Pool rank makes the right
side vanish, and the degree budget forces \(Q\cdot O''=0\).  This closes
every nonzero-cofactor branch: nonzero \(J\) would require a residual
polynomial with ten or eleven opposite roots, while \(J=0\) contradicts
the exact \((z^2-u)^3\) coefficient descent.  Thus five-space survivors
have \({\cal P}\equiv0\).  In an odd-adapted basis, every mixed
four-by-four cofactor factors into an odd and a pure-even two-function
Wronskian.  A nonzero odd factor therefore makes all pure-even components
proportional, closing ranks two and three.  Both profiles retain only odd
ranks \(\{4,5\}\) before the uniform dimension bound below.
[live-three-zero-eighth-split-stable-double-fixed-numerator-four-space-bound.md](live-three-zero-eighth-split-stable-double-fixed-numerator-four-space-bound.md)
removes every five-dimensional stable four-core kernel uniformly in the
order.  The normalized rational primitive identifies the growing exactness
kernel with
\({\cal W}\subseteq\mathbb C[z]_{\leq9}\), characterized by
\(Q_R^2\mid{\cal E}(n)\).  At each of the four fixed values, the two
conditions \({\cal E}(n)={\cal E}(n)'=0\) have nonzero successive
\(n',n''\) pivots.  A \(d\)-space therefore pays \(2(d-1)\) Wronskian
units four times, and \(8(d-1)\leq d(10-d)\) forces \(d\leq4\).  Combined
with the preceding exclusions of dimensions two through four, this closes
both \(2^{14}1\) and \(2^{15}\).  It also closes both stable families
uniformly for every \(m\geq12\).  For \(p\geq11\), moving double-zero
planes exclude dimensions two and three.  Equality in dimension four
forces the unique basis
\(R_i=\prod_{j\ne i}(z+r_j)^3\).  Its anchor equation, compared across a
swap of the fourth core value, makes all \(m-3\) eligible values lie in one
fibre of
\(g_r(x)=3/(x-r)-2/(x+r)=(x+5r)/(x^2-r^2)\).  Every fibre has at most two
points, a contradiction.  The cases \(p=8,9,10\) are precisely the earlier
octic, nonic, decic, and first-undecic closures.  Unrelated no-selection
profiles at the same orders are not covered.
[live-three-zero-eighth-split-general-collision-fixed-numerator-closure.md](live-three-zero-eighth-split-general-collision-fixed-numerator-closure.md)
extends the normalized primitive to arbitrary collision multiplicities.
For a fixed four-class formal-double core, the complementary primitive
denominator has degree \(k+10\), even when a selected triple or higher
class retains fixed excess.  Subtracting the value at \(-\mu\) therefore
again gives a numerator in \(\mathbb C[z]_{\leq9}\).  Four reflected
double-jet anchors bound the common kernel by four dimensions, while three
moving fifth choices exclude dimensions two and three.  Equality gives
the same basis \(R_i=\prod_{j\ne i}(z+r_j)^3\); swapping the fourth core
value cancels every original multiplicity and leaves the quadratic fibre
\((x+5r)/(x^2-r^2)\).  Hence every legal seven-universe is impossible.
The count criterion
\(\rho\ge7\) and
\((n_1\ge2\ \text{or}\ n_2\ge6\ \text{or}\ n_3\ge5)\)
closes every selection-free baseline profile at \(k\ge7\), uniformly in
the order.  Together with all-order mixed-role incidence, this completes
the no-extra-singular \(h=8\) collision ledger for every \(k\ge7\);
at \(k=6\) this theorem by itself leaves only \(4^3 3^4\).  The arbitrary-\(h\)
normalization has degree \(2h+1-A\) for fixed role mass \(A\), but the
four-space Wronskian acquires slack \(h-8\), so this theorem gives no
automatic closure credit on the \(p=18\) saturated five-space boundary.
[live-three-zero-eighth-split-k6-quadruple-triple-role-closure.md](live-three-zero-eighth-split-k6-quadruple-triple-role-closure.md)
closes that final \(4^3 3^4\) profile.  A \((3,3,3,1)\) formal target
gives six legal pair-drop lifts in \(\mathbb C[z]_{\le5}\).  Three exact
order-three rows and one reflected order-one row force the common kernel
to have dimension four: the only three-dimensional parity form would be
\((z+q)\mathbb C[z^2]_{\le2}\), which the reflected row does not
annihilate.  The resulting two row relations inject, after the exact
degree-seven numerator cancellation, into the one-dimensional constants.
The pair-drop legality, local-unit normalization, every gcd correction, and
the degree-ten contact divisor passed a separate line-by-line audit.  Thus
the complete selection-free no-extra-singular \(h=8\) collision ledger is
closed, including \(k=6\).
[live-three-zero-eighth-split-k5-parallelogram-normal-form.md](live-three-zero-eighth-split-k5-parallelogram-normal-form.md)
is a historically exact reduction for \(2^9 1^5\).  It rewrites every
five-candidate edge equation as a diagonal perturbation determinant,
identifies all four-cycle equations as second differences, and factors the
universal \(5\times6\) leading quadratic matrix.  Its affine certificate
was never completed; the all-order \(d=3\) incidence theorem now closes the
profile by a different exact route.
[live-three-zero-eighth-split-k5-updated-census.md](live-three-zero-eighth-split-k5-updated-census.md)
records the exact completed fifth-order ledger.  The slice has 44 frozen
profiles, attributed disjointly as 18 historical closures, 25 uniform
incidence closures, and one five-double endpoint closure.  No fifth-order
profile remains open.
[live-three-zero-eighth-split-k3-nine-double-three-singleton-pencil.md](live-three-zero-eighth-split-k3-nine-double-three-singleton-pencil.md)
closes the equality profile \(2^9 1^3\).  Its cubic relation pencil has
Wronskian equal to the singleton cubic times a linear factor.  Outside
double rows and a rectangular partition difference force five points of
\(x\mapsto(\Phi_u(x),\Phi_v(x))\) onto a line, although every line pulls
back to a nonzero polynomial of degree at most four.
[live-three-zero-eighth-split-k3-three-triple-mixed-layer-closure.md](live-three-zero-eighth-split-k3-three-triple-mixed-layer-closure.md)
closes \(3^3 2^3 1^6\).  Two full double layers and six singleton layers
give 28 legal pair-drop lifts in one degree-nine kernel.  A sharp mixed
parity and reduced-Wronskian argument makes that kernel four-dimensional;
the two value-row relations would then inject into the constants, an
impossibility.
[live-three-zero-eighth-split-k3-two-illegal-core-bypass.md](live-three-zero-eighth-split-k3-two-illegal-core-bypass.md)
closes the final profile \(3^2 2^4 1^7\) without constructing either of
its two illegal eight-cores.  One-missing lifts construct every nine-core
except their union and then every ten-core while skipping that lone hole.
Ordinary exchange resumes from size ten, and the full-core
antiderivative--Wronskian deficit is the strict number \(3^2-8=1\).
Consequently the complete no-extra-singular \(h=8,k=3\) collision census
is empty.

The additional-singular-site escape at three zeros is also finite.
[live-three-zero-extra-singular-axis-capacity.md](live-three-zero-extra-singular-axis-capacity.md)
combines the Hall--Schmidt bounds with the two forced type-`10` and two
forced type-`22` centres.  They already consume two of the three missing-axis
slots for every colour and saturate the joint `(0,1)` slot.  Hence at most
three further nonzero singular sites can occur; their nonempty missed-axis
sets are pairwise disjoint and none may contain both `0` and `1`.  Every
such site is incident to a rank-three edge toward the zero shore, so the
structural identity also synchronizes its beta value to the common centre
value $\mu$.
[live-three-zero-extra-singular-shared-star-reduction.md](live-three-zero-extra-singular-shared-star-reduction.md)
then contracts the already-vanishing shared-zero response at one extra
centre.  Whenever that centre misses binary axis $0$ or $1$, the
Hall--Schmidt equality factor is a nonzero pure residual cap, forcing its
block to the shared zero to have rank below three.  Therefore only one
extra rank-three rescue type remains: a single rank-two site with missed
set $\{2\}$ and image $\langle e_0,e_1\rangle$ (with arbitrary kernel).
[live-three-zero-minimal-extra-plane-all-exceptional.md](live-three-zero-minimal-extra-plane-all-exceptional.md)
closes its smallest parity-compatible residual when both live sites are
exceptional.  Row-reducing the arbitrary kernel gives three charts; one
has an exact diagonal nine-square response minor, while the other two
have eight structurally nonzero singleton pivots followed by one
triangular row.  Every pivot is independent of the kernel parameters and
of the direct-term scale.
[live-three-zero-minimal-extra-plane-one-exceptional.md](live-three-zero-minimal-extra-plane-one-exceptional.md)
closes the adjacent stratum with exactly one exceptional live site.  In
each of the same three arbitrary-kernel charts, an exact twelve-row response
minor is triangular with pivots in \(\{1,\alpha,3\alpha\}\), where
\(\alpha=2/(\nu+1)\ne0\).  Hence the common live block and all three
singular-star blocks vanish.
[live-three-zero-minimal-extra-plane-common.md](live-three-zero-minimal-extra-plane-common.md)
closes the last, all-common two-live stratum.  The complete response now has
fifteen columns.  The `12` and `02` kernel charts have parameter-independent
diagonal-source minors, while three exact minors cover the `01` chart by the
elementary split \(a\ne0\), \(a=0,b\ne-3\), and \((a,b)=(0,-3)\).
Consequently every beta stratum of the smallest residual containing the
extra plane is closed without using the direct-term scale.
[live-three-zero-extra-plane-common-beta-all-orders.md](live-three-zero-extra-plane-common-beta-all-orders.md)
removes the live-size restriction on the common-beta stratum with one extra
plane.  Two exact fixed-subset transforms kill the binary rows at all live
and type-`10` sites; arbitrary contraction then kills the entire extra
star.  If the source-side row plane of the extra centre is noncoordinate,
source-`2` rows give all live pair sums; if it is the coordinate plane, a
one-ternary-letter response is a singleton.  Thus the sole-extra-plane,
all-common branch is closed at every order.
[live-three-zero-extra-plane-minority-exceptional.md](live-three-zero-extra-plane-minority-exceptional.md)
extends the sole-extra-plane result to \(1\le t\le r-2\) exceptional
live beta values.  Monochromatizing the exceptional shore multiplies every
surviving cofactor by the same nonzero Cauchy monomial, leaving the same two
plane functionals as in the common-beta proof.  The extra block, centre
third rows, and live third rows then fall to the same contraction and
pair-sum cleanup.  No repetition or genericity condition is imposed on the
exceptional beta values.
[live-three-zero-extra-plane-two-marked-transverse.md](live-three-zero-extra-plane-two-marked-transverse.md)
uses two exceptional sites as the forced source-`22` marked pair.  For
\(2\le t\le\min(2r,r+2)\), it closes every extra row plane whose
intersection with the binary source plane contains a vector with both
binary coordinates nonzero.  The surviving kernel geometry in that range
is reduced to the two axial families whose intersection line is exactly
\(\mathbb C e_0\) or \(\mathbb C e_1\).  The independent response-level
audit in
[live-three-zero-extra-plane-independent-audit.md](live-three-zero-extra-plane-independent-audit.md)
checks all three uniform sole-extra-plane reductions, including repeated
exceptional values and endpoint subset sizes.
[live-three-zero-extra-plane-axial.md](live-three-zero-extra-plane-axial.md)
closes the two remaining axial row-plane families throughout the same range,
and also covers the missing endpoint $(r,t)=(2,1)$.  One exceptional site
and the extra plane form a forced marked pair independent of the axial
parameter.  Fixed-subset incidence handles $t\le r+1$; at $t=r+2$, the
one-point deletion system is the invertible matrix $J-I$.  Arbitrary
contraction and a triangular third-row cleanup then kill the complete extra
star.  The independent audit in
[live-three-zero-extra-plane-axial-independent-audit.md](live-three-zero-extra-plane-axial-independent-audit.md)
retains all contaminating star columns and verifies repeated beta values,
$u=0$, $r=2$, and the endpoint pivots.  Thus every sole-extra-plane row
geometry is closed for $0\le t\le\min(2r,r+2)$.
[live-three-zero-extra-singular-exact-frontier.md](live-three-zero-extra-singular-exact-frontier.md)
gives the exact remaining missed-axis census: eleven labelled nonempty
families, seven modulo the binary-axis swap, and only the sole type
\(\{2\}\) can still rescue the shared zero by a rank-three block.  The
sole-plane arbitrary-beta gap is precisely
\(r\ge3,\ r+3\le t\le2r\); the two multiple-rescue gaps start with
\(\{2\}+\{0\}\) at \((r,t)=(2,0)\) and
\(\{2\}+\{0\}+\{1\}\) at \((1,0)\).  Its new homogeneous-shore
coefficient closes every sole-plane high-\(t\) profile having an
exceptional beta class of multiplicity at least \(r\).  Hence every
surviving sole-plane class multiplicity is at most \(r-1\), while the
multiple-extra response-contamination branches remain explicit frontiers.
[live-three-zero-sole-plane-first-high-closure.md](live-three-zero-sole-plane-first-high-closure.md)
closes the first surviving sole-plane point \((r,t)=(3,6)\).  Three literal
forced-pair Cauchy-permanent families give one-common, opposite-common, and
two-equal-common pivots.  Their twelve localized numerator ideals are units
over \(\mathbb Q\) on the four possible profiles
\(2^3,2^2 1^2,2 1^4,1^6\).  The one-marked-extra construction closes every
noncoordinate row plane; a separate symmetric three-centre triangular
system closes the coordinate plane.  The response audit retains all active
contamination, singleton zero-beta boundaries, all three kernel charts, and
an arbitrary direct \(B_{01}\) scale.  The sole-plane frontier now begins at
the next split layer.
[live-three-zero-sole-plane-first-high-layer-uniform-closure.md](live-three-zero-sole-plane-first-high-layer-uniform-closure.md)
promotes that finite certificate to every \(r\ge3\) with \(t=r+3\).
The \(S_r\) pivots are a fixed-size subset-incidence transform, and
one-point deletion of the \(P_r\) pivots excludes the all-equal, mixed
repetition, and all-distinct beta branches.  On noncoordinate row planes,
\(P_r\) kills the common active rows and \(S_r\) kills the extra star; on the
coordinate plane, \(S_r\) also gives every zero-row and triangular
common-live cleanup.  The uniform exact response audit retains all active
contamination, zero beta, both binary orientations, and arbitrary direct
scale.
[live-three-zero-sole-plane-second-high-closure.md](live-three-zero-sole-plane-second-high-closure.md)
then closes \((r,t)=(4,8)\), the first point of the next split layer.  A
triple beta class is impossible by an elementary one-point-deletion system;
the all-distinct profile is excluded by a nonzero projective quartic; and a
double class produces a double-confluent Borchardt quotient whose residue at
the common pole has a quadratic fibre containing at least three distinct
values.  The literal response audit covers the new three-special-column
noncoordinate pivots, embeds the coordinate pivots in the earlier uniform
family, retains zero beta and direct scale, and covers every row plane.  The
same initial-jet mechanism closes the whole layer $t=r+4$: profiles with a
triple, at least seven classes, or exactly six classes are excluded by
deletion/residue quartics, while the last $2^4 1$ and $2^5$ profiles fail a
fixed-$b$ quadratic fibre.
[live-three-zero-sole-plane-third-high-first-point-closure.md](live-three-zero-sole-plane-third-high-first-point-closure.md)
then closes the first point of the next layer, \((r,t)=(5,10)\).  Its
twenty-three beta profiles are exhausted by fixed-special deletion for a
class of size at least three, affine and quadratic Robin factors for one
through four double classes, an exact localized universal sextic certificate
for the all-distinct profile, and a bad-pair matching lemma for five double
classes.  The inherited coordinate pivots and the literal noncoordinate
response retain singleton zero beta, arbitrary direct scale, and every row
plane.
[live-three-zero-sole-plane-third-high-layer-uniform-closure.md](live-three-zero-sole-plane-third-high-layer-uniform-closure.md)
promotes this point to the complete layer \(t=r+5\).  A one-deletion
Hermite lemma leaves residual degree \(m_R-2\) for four special columns.
Four equal columns fail an elementary symmetric deletion descent; every
collision with at least five value classes fails an undivided affine Robin
triangle resultant; and a direct exchange closes the four-repeated-class
boundary.  The all-distinct branch reuses the exact universal quadratic
Robin sextic.  The inherited \(S_r\) response retains zero beta, arbitrary
direct scale, all active contamination, and every row plane.  Hence the
remaining sole-plane frontier begins at \((r,t)=(7,13)\) and has
\(r\ge7,\ r+6\le t\le2r\).
[live-three-zero-sole-plane-fourth-high-frontier.md](live-three-zero-sole-plane-fourth-high-frontier.md)
opens the layer \(t=r+6\) and reduces it to an exact finite dense-double
tail.  Five special columns again leave residual degree \(m_R-2\).
Deletion and Robin exchange close every profile containing a class of
multiplicity at least three; localized degree-eight determinants close one
double and every profile with at least eleven value classes.  On the
all-distinct stratum, the degree-eight cubic determinant identity is exactly
the full DR4 pencil under \(t_i=-a_i\).  DR4 forces its four translations
to vanish, and overlapping four-cores contradict the two-point fibres of
\(\psi(a,y)\).  The application audit in
[verify_live_three_zero_sole_plane_fourth_high_all_distinct_dr4_closure.py](../computations/verify_live_three_zero_sole_plane_fourth_high_all_distinct_dr4_closure.py)
checks the sign bridge, sharp degree, strict root count, and fibre equation.
At \((7,13)\), exactly \(97\) of \(101\) profiles are closed; the residuals
are \(2^3 1^7,2^4 1^5,2^5 1^3,2^6 1\).  The analogous dense-double tail is
empty for \(r\ge15\), so no all-distinct or stable large-\(r\) branch remains
on this layer.
[live-three-zero-sole-plane-fourth-high-three-double-frontier.md](live-three-zero-sole-plane-fourth-high-three-double-frontier.md)
couples the first residual \(2^3 1^7\) across all three double pairs.  The
three degree-eight determinant factorizations, two multiplier identities,
and four exact selected-partner exchange rows admit two characteristic-zero
Singular lifts.  After structural-factor removal they produce six necessary
parameter polynomials of exact degrees \(30,30,30,48,48,48\), with
denominator lcm one.  The gcd of their homogeneous leading forms is
\(v^6w^6\), reducing the projective boundary to \([1:0]\) and \([0:1]\).
The
[independent audit](live-three-zero-sole-plane-fourth-high-three-double-frontier-independent-audit.md)
reconstructs the logarithmic rows, nonidentity argument, confluent
unisolvence, lift orientation, cyclic normalizations, degrees, and boundary
gcd; the
[exact checker](../computations/verify_live_three_zero_sole_plane_fourth_high_three_double_frontier.py)
passes.  This is not a closure: all affine fibres and both boundary
directions remain open, and the modular UNIT is discovery evidence only.
[live-three-zero-sole-plane-fourth-high-three-double-closure.md](live-three-zero-sole-plane-fourth-high-three-double-closure.md)
now closes this \(2^3 1^7\) profile in characteristic zero.  Homogenizing
the three cyclic degree-30 obstructions, a modular rank computation gives
the rigorous upper bound \(\operatorname{HF}_J(78)\le318\).  Two exact
rational overideals \(A,B\) have degree-78 Hilbert values \(192,126\),
contain the target \(t^{46}(L^h)^4\), and satisfy
\(\operatorname{HF}_{A+B}(78)=0\).  The exact-sequence squeeze forces
equality and hence \(L^4\in(h_1,h_2,h_3)\), contradicting the structural
open condition \(L\ne0\).  The
[independent audit](live-three-zero-sole-plane-fourth-high-three-double-closure-independent-audit.md)
uses a different prime and reversed variable orders, freshly obtaining
rank \(2842\) and Hilbert values \(318,192,0,126\).  The value \(126\) is
used only as the exact \(B\)-term, not as an asserted primary-component
multiplicity.  Thus the remaining \((7,13)\) profiles are
\(2^4 1^5,2^5 1^3,2^6 1\).
[live-three-zero-minimal-three-extra-response-frontier.md](live-three-zero-minimal-three-extra-response-frontier.md)
and
[live-three-zero-minimal-three-extra-boundary-cell-frontier.md](live-three-zero-minimal-three-extra-boundary-cell-frontier.md)
give the exact first three-extra response at
\((M_{e_2},M_{e_0},M_{e_1})=(\{2\},\{0\},\{1\})\), \((r,t)=(1,0)\).
The central cell is uniformly closed.  Exact unit-minor certificates,
including
[live-three-zero-minimal-three-extra-cbb-certificate.md](live-three-zero-minimal-three-extra-cbb-certificate.md)
and
[live-three-zero-minimal-three-extra-cce-certificate.md](live-three-zero-minimal-three-extra-cce-certificate.md),
and the final independent placement audit in
[live-three-zero-minimal-three-extra-ccb-certificate.md](live-three-zero-minimal-three-extra-ccb-certificate.md)
close all 26 noncentral cells, or all 27 cells in total.  Thus this first
minimal three-extra configuration is uniformly injective, with arbitrary
direct \(B_{01}\) scale.  This closure does not reach the two-extra
frontier, the sole-plane high-\(t\) frontier, larger three-extra profiles,
or the nonrescue families, which remain open.
[live-three-zero-minimal-two-extra-response-frontier.md](live-three-zero-minimal-two-extra-response-frontier.md)
then closes the first two-extra case
\((M_{e_2},M_{e_0})=(\{2\},\{0\})\), \((r,t)=(2,0)\).
The shared-star restriction removes only one star row, not a singular site:
all seven residual nonzero sites remain in the cofactors and the response
has exactly 20 columns.  One direct-free central minor has divisor
\(ac(b-d)(ac+3a+3c+6)\); exact rational unit ideals close its four
branches.  The ordered \(C/B/E\) decomposition has nine cells because the
two extras have different retained star dimensions.  The independent
boundary audit in
[live-three-zero-minimal-two-extra-boundary-certificate.md](live-three-zero-minimal-two-extra-boundary-certificate.md)
closes all eight noncentral cells over \(\mathbb Q\).  Thus the complete
minimal two-extra response is uniformly injective for arbitrary direct
\(B_{01}\) scale.  The larger two-extra rows in the exact frontier remain
open.

## Promotion rule

A route is promoted only after it yields a proved lemma that is strictly
stronger than a reformulation of the target.  New promotions at this proof
stage require an independent adversarial test against parallel sources,
asymmetric endpoint colors, zero weights, and complex cancellation.  Older
registry entries without an explicitly linked clean-room artifact remain
historical evidence rather than silently acquiring that audit status.
