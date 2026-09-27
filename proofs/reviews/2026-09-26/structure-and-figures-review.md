# Simulated referee report: graph theory, theoretical CS, structure, and figures

This is an **internal simulated review**, not an external Quantum referee report. The reviewer has participated in the project’s mathematical and formalization work; that relationship would require disclosure in an actual journal process. This report evaluates only the frozen `reviewed-baseline.tex` and `reviewed-baseline.pdf`, not the manuscript being revised concurrently.

The report follows the public [Quantum referee form](https://quantum-journal.org/instructions/referees/): scientific assessment, technical checking, presentation and scope, reproducibility, revisions, and an editorial recommendation. The additional category scores below are our diagnostic extension, not Quantum’s official rubric.

## Recommendation and scores

**Overall: 4/5. Recommendation: Revise and resubmit.** The claimed resolution and its structural method are potentially highly significant. The baseline needs a substantial exposition pass before a broad mathematical audience can assess the new argument efficiently. This recommendation is about the manuscript’s readiness, not a detected counterexample to the theorem.

Diagnostic scores use 1 = seriously deficient, 3 = serviceable but needs revision, and 5 = excellent.

| Category — our extension | Score | Reason |
| --- | ---: | --- |
| Clarity | 3/5 | Excellent explanation of cancellation and the endpoint subtotal; a steep transition to response tensors follows. |
| Notation | 2/5 | Several symbols change roles, and the central row/tensor/pairing objects lack a compact reference definition. |
| Terminology and scope | 3/5 | The complex-weight and original-source qualifications are good; “whole,” “response,” “row,” and “tensor” are introduced too quickly. |
| Proof structure | 3/5 | The logical spine is sound and visible in the overview, but the crucial higher-response and endpoint arguments need internal signposts. |
| Figures | 2/5 | The one figure is relevant and correct, but colour-dependent, displaced from its examples, and unrelated to the novel algebra. |
| Reproducibility | 4/5 | The exact Lean target, pinned links, and axiom scope are unusually helpful; the PDF itself lacks a short executable replay recipe. |
| Vision and significance | 5/5 | A universal weighted obstruction, obtained by forcing degree one rather than assuming noncancellation, is a strong conceptual contribution. |

## Summary and scientific assessment

The paper asks whether arbitrary complex weights in a loopless, endpoint-coloured matching model can preserve three nonzero constant-colour amplitudes while cancelling every mixed colouring on more than four vertices. Its answer is a structural reduction: aggregate parallel weights; prove that bichromatic aggregate cells vanish; prove that every supported monochromatic edge has matching subtotal equal to the entire pure amplitude; conclude that each colour is a perfect matching. A receiving colouring then determines at most one matching. The familiar three-matching obstruction produces a mixed matching whose nonzero amplitude cannot cancel.

The central novelty is the supported-edge identity, not the final graph lemma. The replica argument converts whole original-source response identities into an orthogonally covariant polynomial matrix. Its form and boundary equations reduce to polynomial differential equations, whose finite degree forces the endpoint identity. This addresses the complex-cancellation difficulty directly and has a clearer mathematical message than an extended catalogue of excluded graph classes.

The manuscript should make its broader vision explicit in one restrained paragraph: the method extracts rigidity of weighted matching supports from simultaneous amplitude equations, using finite replica symmetry rather than positivity or probabilistic covariance. It should not claim a general theorem about all photonic architectures, arbitrary target states, or other matching-signature models. The present model and GHZ target are the proved scope.

The Chandran–Gajjala–Illickan comparator is useful primarily as a model of audience preparation. Its rendered pp. 41:3–41:4 define half-edges, filtering, and matching weights next to examples; p. 41:6 separates its new weighted results from prior graph obstructions. This manuscript already explains cancellation better than a bare graph-theory introduction, but should similarly distinguish the new structural theorem from the published terminal obstruction. There is no reason to imitate its longer physics motivation or to dilute the present endpoint method.

## Extent of technical checking and actual mathematical concerns

I read the complete frozen TeX and all 15 rendered PDF pages. I inspected the complete Figure 1, and rendered/viewed comparator pp. 41:3, 41:4, and 41:6. I checked the aggregate-weight interpretation, palette restriction, single-vertex normalization, degree-one consequence, shared-edge contradiction, and minimal-arc graph proof. I also read the reflection/common-factor, omission, and polynomial-kernel arguments and checked their stated interfaces and parity conditions. I did not perform a new full line-by-line algebraic verification or rerun the Lean build during this presentation review; the existing formal verification is supporting evidence, not a substitute for explaining the written proof.

**No specific mathematical failure was found in this review.** The following are proof-interface clarifications that should be made explicit:

1. **Lemma 4.1, pp. 8–9:** fix the coefficient colour `k`, then explicitly choose a different active colour `h` before defining its binary alternating pairing. The current proof says “any palette h,k” without recording `h ≠ k`. The available three active colours supply this choice; this is a repair to the explanation, not a counterexample to the lemma.
2. **Lemma 3.1, pp. 6–8:** define the finite-dimensional row space and its coefficient ring. If `D` is the span of finitely many site rows, say so; then the uses of coprime linear forms and polynomial cancellation in `C[D]` have an explicit home. At the end, give the one-sentence reason the three original incident rows have independent pure-response functionals: their images are the three nonzero, distinct pure-word tensors.
3. **Lemma 5.2, p. 11:** state the generic open conditions used for the adapted-frame proof, including nonisotropy, independence of `P,Q_c`, and nonzero dot product. Clearly separate the rational/generic matrix identity from the polynomial extension justified by entry divisibility. The current argument is plausible and concise, but this is a load-bearing passage where a reader should not have to infer the exceptional locus.
4. **Graph model, pp. 2–4:** explicitly declare the endpoint palette or qualify every structural assertion as concerning the aggregate graph restricted to the retained palette. If other endpoint colours are permitted in the initial graph, the target equations on `[d]` do not constrain those discarded edges. The nonexistence theorem survives restriction; the wording “every edge is monochromatic” should not accidentally make a claim about discarded colours.
5. **Scope, pp. 13–14:** preserve the distinction already made between the exact normalized aggregate Lean statement and the written aggregation/general-amplitude translations. The submitted version should not compress these into an assertion that a single final Lean declaration literally takes multigraphs and unequal amplitudes as inputs.

The graph proof on p. 13 is short and checks out at the stated interface: after the first two matchings form a single alternating Hamilton cycle, the third matching consists of chords; opposite-parity chords or interlacing opposite-parity chord pairs give a mixed matching; the remaining case contradicts a shortest arc. The `n > 4` condition is needed when two third-colour chords leave some cycle edges. The p. 13 boundary paragraph correctly distinguishes `n = 4`, `n = 2`, and odd order.

## Presentation, assumptions, literature, and page layout

### What works well

- **Abstract and pp. 1–2:** the obstruction is stated in plain terms and arbitrary complex, parallel, and bichromatic weights are advertised. The cancellation example is explicitly not claimed to be a GHZ source.
- **Proof overview, pp. 3–4:** the subtotal `C_pq` and boxed `C_pq = beta` are the best organizing device in the paper. The immediate vertex-degree calculation explains why this identity is enough.
- **Sections 2.2–2.4, pp. 5–6:** normalization avoids unjustified choices of complex roots; the Wick discussion explicitly removes probabilistic positivity assumptions; the copies are formal and do not change the graph.
- **Sections 5–7, pp. 10–13:** the corrected matrix includes the direct-root edge term; derivatives keep the retained quadratic fixed; the graph obstruction is used only after cancellation has been removed. These distinctions should remain prominent.
- **Section 8:** the formal target and standard-axiom audit are clear, and internal agent audits are expressly not described as external peer review.

### Concrete problems and revisions

| Location in the baseline | Problem | Concrete revision |
| --- | --- | --- |
| pp. 1–4, §1 | The introduction occupies roughly four pages, with the final degree-one/graph deduction previewed more than once. | Retain the cancellation example and boxed endpoint identity; shorten the second telling of the graph close. Give a five-line proof dependency map instead of another narrative recap. |
| p. 2 to p. 3, §1.2–§1.3 | Figure 1 appears after both examples and interrupts the related-work paragraph. | Keep the figure with §1.2 and its first reference, before Related work; avoid placing a float between the two related-work paragraphs. |
| p. 4 to p. 5, §2.1 | “The algebra and its edge polynomial are” is separated from the defining display by a page break. | Keep this lead-in and the display together, or move the paragraph to the next page. |
| pp. 6–8, Lemma 3.1 | The lemma statement starts at the bottom of p. 6 and concludes on p. 7; its determinant-factor argument is split across pp. 7–8. | Start the lemma on a fresh suitable block of space. Divide its proof into named parts: reflection identity; common factor and mixed coefficients; rotation kills the factor; specialization to actual root rows. |
| pp. 7–8, §3 | “Tensor,” “word,” “row,” binary projection, and `K` carry the argument but are not given one reusable definition. | Define a tensor as its colouring-coefficient array and give an explicit signed finite-sum formula for `K`; state its symmetry/antisymmetry and pure-coefficient extraction immediately. Add a compact notation table. |
| p. 8, Lemma 4.1 | “All following pairings use this binary projection implicitly” hides a domain change. | Declare the projected tensor space once and write the projection in the first identity. State that projection is coefficient restriction, not a GHZ assumption on a smaller graph. |
| foot p. 9, §5 | The new section heading has only two introductory lines below it; all definitions start on p. 10. | Move §5 to p. 10 or keep its full definition block with the heading. |
| pp. 10–12, §5 | One dense setup introduces two roots, four rows, four columns, two matrices, three Gram coordinates, and several scalars. | Split into short subsections: original boundary identities; kernel construction; normal form; two finite-degree equations. Number the kernel definition and off-diagonal divisibility identities so the endpoint proof can cite them. |
| p. 11, Lemma 5.2 | The new matrix reduction and background invariant-ring calculation are adjacent, with similar emphasis. | Highlight the adapted-frame/divisibility reduction as the new load-bearing lemma. Move the elementary invariant-ring calculation to a short appendix if space is needed; retain its exact statement and citation in the main proof. |
| pp. 10–12 | Lower-case `b` is a colour coordinate and then a kernel coefficient; `c` is a colour and then a Gram variable; `a,b` are also mean parameters. Earlier `p` is both an odd response degree and a root. | Use a dedicated mean parameter pair, a response-degree letter such as `ell`, and kernel coefficients such as `A_0,B_0`; give a local dictionary for the four rows. Do not rely on typography alone. |
| p. 13, §7 | The parity/chord argument is entirely textual. | Add a small parity-labelled cycle diagram showing the opposite-parity chord and interlacing-chord cases, or put that worked diagram in an appendix referenced here. |
| pp. 14–15, references | Seven internal provenance entries and audit links occupy much of the bibliography; p. 15 is largely blank. | Consolidate historical notes/audits into one supplementary provenance index. Keep the primary literature and a single pinned formal-artifact reference in the main bibliography. Do not simply enlarge figures to fill the last page. |

All equation numbers and mathematical fonts render cleanly in the baseline. I saw no clipped equation, corrupted glyph, or figure overlap. The page issues are grouping and flow, not a broken PDF build.

## Figure review and proposed figure plan

**Figure 1, p. 3, is the manuscript’s only figure.** Panel (a) correctly has two perfect matchings with products `+1` and `-1`, and the split vertical edges encode different endpoint colours. Panel (b) correctly depicts the three `K_4` matchings, with no vertex at the diagonal crossing. The caption explains both of those potentially ambiguous details.

Its weaknesses are practical: the half-edge distinction and the three matching classes rely on red/blue/green; only representative edges carry colour labels in panel (b); panel (a) does not highlight its two complete matchings separately. The panel subtitle “The obstruction” in the overall caption can suggest that panel (a) is itself a GHZ obstruction even though the prose correctly says otherwise.

**Revise Figure 1:** use distinct dash/line styles as well as colour; label each matching class or provide a compact legend; explicitly mark the two products `+1` and `-1` and their common receiving colouring. Call the caption “Cancellation example and the four-vertex exception.” Keep the non-GHZ qualification in the caption so the figure is self-contained. Test it in grayscale at final print size.

**Add a priority replica/kernel figure:** one panel should show two formal copies, the two local colour selections, and the signed swap defining a local determinant. A second should show the fixed roots `p,q`, the retained set `U`, the two `H` departures, and the direct `H` edge. Connect the latter to “diagonal entry = two retained departures + direct edge `e`,” explaining `T = M + ef I`. Label the picture as formal pairing bookkeeping, not a second physical optical experiment. This would explain the most novel construction rather than merely decorate it.

**Add an optional small graph-closure figure:** draw an alternating cycle with parity-marked vertices and two interlacing chords of opposite parity. Highlight the remaining even paths and the resulting mixed matching. Include the `n = 4` exception where the two chords exhaust the vertices. Keep the shortest-arc argument in the text; a diagram should illustrate, not replace, the proof.

A dependency table may be more useful than a third elaborate algebra figure:

`original GHZ equations → whole binary responses → even omission → diagonal cells → polynomial kernel/ODE → endpoint subtotal → degree one → three-matching contradiction`.

Each arrow should name the corresponding lemma and what it establishes on the **original** source. In particular, no arrow should imply that a deleted core is again a GHZ source.

## Main text, appendix, and reproduction plan

Keep in the main text the precise graph model and cancellation example, the boxed endpoint subtotal, an explicit pairing definition, the three-part higher-response proof, the omission-to-diagonal argument, the corrected kernel and finite-degree argument, and the short degree-one/graph close. The central endpoint proof should not be sent to supplementary notes: it is the contribution a referee must judge.

Suitable appendix material is the elementary two-vector invariant-ring calculation, a longer matching-coefficient/Wick normalization example if desired, the formal-module correspondence table, the complete reproduction commands, and historical provenance. Preserve a short main-text explanation of every ingredient moved there.

There are no physical or numerical experiments to reproduce. The relevant artifact is the formal proof. Section 8 and reference [14] provide pinned sources, but readers should not have to follow several repository links to discover the minimal replay. Add a short artifact paragraph or appendix containing: repository commit; Lean and mathlib pins; the exact build and upstream-adapter commands; the final declaration’s full name; expected axiom output; and the explicit distinction between normalized aggregate inputs and the written multigraph/general-amplitude translations. A permanent archive of the reviewed source, PDF, and proof artifacts would further improve submission stability. I did not replay the artifact in this review, so its current linked command execution is not newly certified here.

## Priority revision list

1. Define the response tensor, row space, binary projection, and alternating pairing before Lemma 3.1; resolve overloaded symbols.
2. Split the higher-response and endpoint sections into clearly labelled stages and supply a dependency map.
3. Keep the original-source, terminal-degree, and direct-edge qualifications explicit at every transition.
4. Repair Figure 1’s position and grayscale readability; add a replica/corrected-kernel diagram.
5. Fix the identified page breaks and make the main bibliography distinguish primary results from internal provenance.
6. Add a concise, pinned formal replay appendix and retain the exact formalization boundary.

For the editor: the contribution merits another review after these revisions. An updated version would benefit from an independent specialist checking the replica/kernel argument and a separate artifact reviewer executing the pinned build. I would be willing to reassess the exposition and graph-theoretic interfaces of that version.

## Review record

- Frozen TeX SHA256: `88c09b6468a721d92a68051459b1656a1c6a9cd78fca89c2759e84d582a64988`.
- Frozen PDF SHA256: `015b5b4ed08b095346f899d5ab3963d75ff055677888e0ed6ec2eb2e11628363`.
- PDF: 15 pages; all rendered with `pdftoppm -png -r 105` and individually viewed using `view_image`; Figure 1 is on page 3 and was inspected in full.
- Comparator: supplied `gajjala-sparse.pdf`, rendered/viewed pages 3, 4, and 6 (printed page labels 41:3, 41:4, 41:6).
- Manuscript, figures, and baseline files were not edited. The only report written is this file.
