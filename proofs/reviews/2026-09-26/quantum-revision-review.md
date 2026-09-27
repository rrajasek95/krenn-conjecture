# Internal simulated referee rereview: quantum-optics readership

**Version reviewed:** [reviewed-revision-1.pdf](reviewed-revision-1.pdf), 22 pages, and [reviewed-revision-1.tex](reviewed-revision-1.tex), September 26, 2026. PDF SHA-256: `b46baec2b1ee27e72caf493875a878ba42b623acf942952ca450e12843b7f53a`; TeX SHA-256: `8301d26ba9d424a08ce7d8bf4642e568e9c2f98f67ef1fa6d1e22e9ac659db39`.

**Outcome:** The major conceptual-clarity deficiencies identified in the baseline review have been addressed. The manuscript now defines its auxiliary objects well enough for a mathematically literate physics reader to follow the proof strategy. I found no remaining blocking physics-terminology or figure issue in this rereview. A short final consistency pass is still appropriate.

**Recommendation:** Revise and resubmit, with the remaining presentation changes assessed here as minor. **Overall presentation rating: 4/5**, up from 2/5. These use the recommendation choices and overall scale of [Quantum's referee form](https://quantum-journal.org/instructions/referees/). This is not a recommendation to accept the mathematics without independent technical review: the score assesses the exposition and interfaces that I inspected.

## Review performed and limits

I read the complete revised source, compared the repaired passages to the earlier report, and extracted the revised PDF text. I rendered and visually inspected all three figures on PDF pages 3, 8, and 19, including all their panels and captions. I also visually inspected the endpoint definitions on p. 14 and the normal-form discussion on p. 16. I checked the new MFCS pinpoint citation against the published PDF and verified the added Electronic Journal of Combinatorics bibliographic record against the publisher's indexed page. I did not rerun Lean, audit every formal dependency, rederive every invariant-theory assertion independently, check every bibliography URL, or certify novelty. The reports remain internal simulated reviews.

## Updated diagnostic scores

The category scores are our diagnostic extension, not additional official Quantum questions. Here 1 = poor, 2 = substantial deficiencies, 3 = adequate but needs revision, 4 = strong, 5 = excellent.

| Criterion | Baseline | Revision 1 | Assessment |
|---|---:|---:|---|
| Conceptual clarity | 2 | 4 | The model, the obstruction from cancellation, the two-copy construction, and the endpoint matrix now have explicit purposes and interpretations. |
| Notation and definitions | 2 | 4 | Rows, words, tensors, shifts, derivatives, pairings, and coefficient rings are introduced; a few inherited names remain to clean up. |
| Terminology and scope | 2 | 4 | Formal copies are distinguished from physical states; bilinear versus Hermitian pairings and graph versus state normalization are explicit. |
| Organization | 3 | 4 | The difficult section now progresses from goal to graph data to identities to matrix structure; detailed normal-form algebra has an appendix. |
| Figures | 3 | 4 | The examples, copy diagram, and chord constructions are readable and support three distinct explanatory tasks. |
| Reproducibility documentation | 4 | 4 | Exact formal scope and commands are accessible in an appendix; no fresh execution was performed in this review. |
| Overall presentation | 2 | 4 | The central conceptual barrier has been removed; the remaining concerns are localized rather than structural. |

## Implementation of the initial recommendations

**Physics model, §§1.1 and 2.3, pp. 2 and 6.** The displayed postselected state gives the graph coefficients a concrete meaning. The text explicitly identifies modes, paths, amplitudes, and the conditioning event. The normalization lemma now distinguishes rescaling graph weights from dividing a state's norm, including the fact that the operation need not be unitary. These changes resolve the original physical ambiguity.

**Two algebraic descriptions, §2.4, p. 7.** The definition of the Wick functional now gives its domain, index set, symmetric pairing table, odd/empty conventions, and its coefficient bridge to the site algebra. The example with a repeated formal symbol directly demonstrates why the ordinary symbol algebra differs from the nilpotent quotient. This addresses the most consequential mathematical-interface concern from the baseline.

**Meaning of copies, §2.5, pp. 7–8.** The paired symbol families, their joint table, factorization property, and change of variables are explicit. The text correctly uses complex bilinearity, defines the orthogonal group without conjugation, and says that the copies are not additional physical systems. A reader can now calculate a preserved covariance rather than merely being told that preservation holds.

**Rows, words, responses, shifts, and derivatives, §§2.2, 2.6 and 3.1, pp. 6, 9–10.** The new definitions are locally useful. The root expansion explains where a row comes from; the response interpretation explains what its coefficients count. The alternating pairing is computable from the displayed sign formula. Shift rows and directional derivatives have explicit definitions. The ordinary parameter-ring cancellation convention prevents an invalid interpretation in the nilpotent site algebra.

**Vanishing and omission arguments, §§3–4, pp. 10–13.** The three named stages of the vanishing proof improve navigation. The reflection's binomial factor and the polarization procedure are stated. Explicit binary projections in the omission proof make clear that no assertion is being made about discarded three-colour coefficients. This resolves a substantial source of reader uncertainty.

**Endpoint construction, §5, pp. 14–17.** The opening states the goal and the two possible ways of matching the roots. The row table separates root, colour, and coefficients. The first two-root identity is explained combinatorially. Copy-index matrices are distinguished from vertex-index matrices, and the correction term is motivated. The new paragraph explaining why covariance alone does not force the normal form is particularly valuable: it locates the contribution of the matching identities. Moving the coordinate proof to Appendix A preserves the main idea in the text while reducing interruption.

## Figure inspection

**Figure 1, p. 3.** Both panels are legible. The added matching sets and products make the cancellation example self-contained, and the four-vertex panel now gives its three matching classes explicitly. The caption correctly distinguishes edge weights from inherited vertex colours and identifies the crossing convention. The numerical and letter labels provide useful non-colour cues. No overlap or clipping was visible at the inspected scale.

**Figure 2, p. 8.** The new copy diagram is an appropriate algebraic schematic. Its boxes contain whole symbol families, the across-family pairing is labeled zero, and the same matrix acts at every label. The caption states that its arrow is a change of formal variables, not a graph edge or physical operation. Labels are readable and the diagram agrees with the adjacent formulas. It is less detailed than the pairing table, which is desirable: the table defines the operation and the diagram summarizes it.

**Figure 3, p. 19.** I checked both selected edge sets against the eight-cycle. Panel (a) contains the chord 03 and cycle edges 12, 45, 67; panel (b) contains chords 04, 15 and cycle edges 23, 67. Each collection covers every vertex exactly once and uses both chord and cycle edges. Dashed versus heavy-solid styles preserve the distinction without colour. The caption correctly explains that only selected H-edges are drawn and that these are local configurations, not claimed GHZ solutions. The figure supports the argument without falsely depicting a complete third matching.

## Remaining concrete revisions

1. **Define perfect matching at first use in §1.1.** This is the central graph object and currently receives only an implicit characterization through the unique incident edge. Add: “A perfect matching is a set of pairwise disjoint edges covering every vertex exactly once.”
2. **Make the abstract's copy description agree with §2.5.** “Two identical formal copies of the matching polynomial” can still suggest duplicating the physical object. Prefer “two formal symbol families with identical pairing coefficients,” followed by the statement that their pairing sums encode matching amplitudes. This is a precision edit; the main text already resolves the ambiguity.
3. **Remove residual undefined uses of “source.”** On p. 8, “original source rows” should be “original incident rows.” On p. 19, “permitted ternary source” can be “permitted three-colour construction,” and “odd-core lemma” can point directly to Lemma 3.1. This keeps the terminology consistent with the revised definitions.
4. **Introduce the direction V in equation (4), §4.1.** The derivative convention is defined, but this particular V is not explicitly quantified. Say “For any fixed row direction V on S, the two-copy rotation gives …”. This avoids confusion with the original vertex set V.
5. **Order Corollary 6.2's proof by dependency, p. 18.** Establish uniqueness for a prescribed colouring first, using one incident edge of each colour at each vertex. Then the proposed mixed matching from a shared edge has a nonzero coefficient. The current order is recoverable but initially asserts a nonzero coefficient before reminding the reader why cancellation is impossible.
6. **Name the normal-form lemma consistently, p. 16.** The title still says “kernel normal form,” although the body now uses “corrected insertion matrix.” “Polynomial normal form for the insertion matrix” avoids reviving an unexplained overloaded term.
7. **Define “mixed” for the three-matchings lemma.** The main model defines a mixed colouring; this lemma calls a matching mixed. Add “containing edges from at least two of F,G,H.” The intended meaning is clear but the formal definition would cost little.

These are local changes, not requests to expand the paper with another general glossary. The revised §2 is already substantial; avoid increasing length through repeated definitions that are now clear.

## Literature and attribution rereview

The revision adds the original physics correspondence and weighted-interference references, distinguishes the simple-graph sparsification result from the monochromatic-edge SAT exclusions, explicitly credits the prior uniqueness-and-obstruction endgame, and includes the recent public formal artifact and author-announced dimensional bound. These implement the substantive recommendations in the literature report.

The MFCS citation to **§2.3, Corollary 17** is correct for the proceedings version. The added classification article's **Electronic Journal of Combinatorics 33(3), P3.21 (2026), DOI 10.37236/12573** is confirmed by the publisher's record, which gives August 7, 2026 as publication date. [Publisher record](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i3p21).

A final targeted search identified another directly related accepted title: Chandran and Gajjala, **“Connectivity Bounds for GHZ Graphs,” FSTTCS 2026**. The official accepted-paper list and the author's page confirm the title and authors; the conference is scheduled for December 16–18, 2026. Neither inspected page links a manuscript, and the targeted search did not locate its theorem statements. It may be acknowledged as forthcoming, but no assertion about its bound or relation to the present method is supported by this review. [Official accepted papers](https://www.fsttcs.org.in/2026/papers.php), [author publication list](https://gajjala.in/).

The unavailable tensor-algebraic manuscript remains appropriately described as in preparation, with the displayed AlphaProof Nexus instances distinguished from the author-announced general bound. The current text makes no speculative priority claim.

## Final assessment within this review's scope

The paper now explains the actual objects used in the proof rather than relying on a reader to import meanings from probability, optics, or invariant theory. Its figures are consistent with that explanation. The remaining edits above would improve precision and remove small first-use obstacles. No new mathematical counterexample or demonstrated invalid inference was found in this presentation-focused rereview; this statement is deliberately narrower than full independent verification of the theorem.
