# Simulated referee rereview: revision 1

This is an internal simulated rereview of the **frozen revision 1**, not an external journal report. It supplements, and does not replace, the two earlier reports. The reviewer has participated in the project. I read the revised TeX, rendered and individually viewed all 22 PDF pages with `pdftoppm` and `view_image`, and inspected all three figures. The focused technical checks were the new normalization lemma, the disjointness/uniqueness corollary, the graph argument and its diagrams, and the revised literature scope. I did not rerun Lean or undertake another full verification of the replica-kernel proof.

## Recommendation and honest revised scores

**Overall: 4/5. Recommendation: Revise and resubmit, with focused remaining edits.** This is a substantial improvement over the baseline. The previous request for a broad exposition rewrite has largely been met. I found no new mathematical regression in the checked passages; the remaining items concern precise model wording, figure accessibility, and a few page-layout decisions. This presentation review does not independently certify every formal-proof dependency.

The format follows the [Quantum referee instructions](https://quantum-journal.org/instructions/referees/). The diagnostic categories are our extension, not an official Quantum scorecard; 1 means seriously deficient and 5 excellent.

| Diagnostic category | Baseline | Revision 1 | Assessment |
| --- | ---: | ---: | --- |
| Clarity | 3 | **4** | Rows, receiving words, ordinary Wick variables, and replica operations now have explicit definitions. |
| Notation | 2 | **4** | The fixed-row table and derivative conventions make the central construction readable. A few overloaded letters remain, but their roles are now declared. |
| Terminology and scope | 3 | **4** | Original-source, formal-copy, bilinear, and terminal-degree qualifications are markedly better. The endpoint-palette wording still needs one clarification. |
| Structure | 3 | **4** | Named proof stages and the five-part endpoint section give a usable dependency spine. Background and artifact material are appropriately separated into appendices. |
| Figures | 2 | **4** | The replica diagram and correct chord constructions explain actual steps. Figure 1 remains colour-dependent and its caption could be more precise. |
| Reproduction | 4 | **4** | Exact commands and the formalization boundary are now in the PDF. I did not execute them during this rereview. |
| Vision and significance | 5 | **5** | The unrestricted weighted-to-degree-one reduction remains the conceptual contribution. No broader optical-architecture claim is needed. |

**The figure score is 4, not 5; the vision score is 5.** The official overall score remains 4. The unchanged overall number should not obscure the real improvement in the diagnostic categories.

## Improvements that should be retained

- **pp. 2–4, §1:** postselection is explained, amplitudes are distinguished from probabilities, and the contribution is separated from the established cubic closing strategy.
- **pp. 5–9, §2:** row and tensor definitions, explicit coefficient notation, the distinction between the site quotient and ordinary Wick symbols, replica factorization, and the signed finite pairing remove major interpretive ambiguities. The example `W(Z_u² Z_v²)=2c²` is particularly useful.
- **pp. 10–12, Lemma 3.1:** the reflection, common-factor, rotation, and polarization stages are identifiable. The coefficient ring is explicit, including why polynomial cancellation is legitimate despite zero divisors in the site algebra.
- **p. 12, Lemma 4.1:** the earlier missing colour inequality is now explicit: choose an active `h ≠ k`. The binary projection is declared and is not treated as a smaller GHZ graph.
- **pp. 14–17, §5:** the four-row dictionary, original retained-core qualification, corrected insertion matrix, divisibility input, scalar-invariant limitation, and polynomial ODE stages are well separated. The direct-edge term is explained instead of silently discarded.
- **pp. 19–21:** the normal-form coordinate proof and executable artifact instructions have useful appendix homes. Historical agent audits are still correctly described as internal records.

The added length, from 15 to 22 pages, mostly buys definitions and a genuine proof roadmap. Do not shorten it by deleting the quotient/Wick distinction or the original-source qualifications. The main text can still be trimmed modestly by reducing repeated previews in §1.4.

## Figures: actual inspection and mathematical checks

**Figure 1, p. 3.** The two matching products and receiving word are now written under panel (a), and all three `K₄` matching classes are listed under panel (b). Those additions help. The figure now precedes the Related work heading rather than interrupting its paragraphs. However, its caption still begins “The obstruction and the exceptional case” and does not independently say that panel (a) is only a cancellation example, not a GHZ source. Rename it “Cancellation example and the four-vertex exception” and add that qualification. Distinct dash/line styles or a labelled legend would improve grayscale use; the half-edge distinction and `K₄` colours still rely on red/blue/green.

**Figure 2, p. 8.** This is a useful, clean, grayscale-safe illustration of the formal-copy construction. Its caption correctly identifies the arrow as a variable change, not a graph edge or a physical operation; the same within-copy table `C` and zero cross-copy table appear on both sides. The diagram illustrates copy mixing, not the later corrected matrix `T=M+efI`. That is a valid choice. A small later inset showing the retained departures plus the direct `H` edge remains an optional improvement, rather than a prerequisite for acceptance.

**Figure 3, p. 19.** Both constructions are correct and substantially improve the final argument:

- Panel (a) selects `H:{03}` and cycle edges `{12,45,67}`. They are disjoint and cover all eight vertices. The chord endpoints have opposite parity.
- Panel (b) selects `H:{04,15}` and cycle edges `{23,67}`. The chord endpoints occur alternately around the cycle, with one even-even and one odd-odd chord. Again every vertex is covered once.

Dashed chords and heavy solid selected cycle edges distinguish roles without relying on colour. The caption correctly says that unselected `H` edges are omitted, the crossing is not a vertex, and these are local proof configurations rather than GHZ constructions. No inaccurate matching, parity, or crossing claim was found. The diagram is on the next page after the proof, but it remains close enough to its first reference and should not be moved away from §7.

## Normalization, uniqueness, and graph-proof regression check

**Lemma 2.2, p. 6, is correct on the declared target palette.** Every perfect matching uses one edge at the chosen root, so multiplying incident weights by the reciprocal of that root's requested pure amplitude gives `W′(κ)=τ_{κ(r)}⁻¹W(κ)`. All factors are nonzero, hence edge support is preserved. The converse is immediate. The paragraph now properly calls this an alternative realization of CGI Lemma 14 and distinguishes it from norm normalization or unitary state evolution.

**Corollaries 6.1–6.2, pp. 17–18, have no detected regression.** The endpoint identity plus the root hafnian expansion counts exactly one supported neighbour in each colour. A shared geometric edge between two colour matchings would produce the mixed receiving word that selects one colour on its endpoints and the other off them. Uniqueness follows from the prescribed colour fixing the sole incident edge at each vertex. This reasoning uses the diagonalized aggregate graph and nonzero matching weights; it is not a noncancellation assumption imposed at the outset.

**Lemma 7.1, p. 18, is correctly attributed and its proof still checks at this interface.** The alternating union must be one Hamilton cycle, opposite-parity chords give a mixed matching, interlacing opposite-parity chord pairs do the same, and the shortest-arc argument rules out the remaining possibility. At `n=4`, two third-colour chords exhaust the vertices, so the corresponding construction need not be mixed; the boundary paragraph on p. 19 preserves that exception. Odd order and `n=2` are separately treated. The new drawings do not smuggle in an assumption that the third matching has only the displayed edges.

## Literature and recent-result scope

The requested attribution corrections have been implemented accurately: aggregation now cites CGI p. 41:5; normalization cites Lemma 14; the cubic unique-word endgame cites §2.3, Corollary 17; and the graph proof explicitly adapts Bogdanov's alternating-cycle/minimal-arc argument. The EJC 2026 paper is now correctly identified in the bibliography as **33(3), P3.21**, DOI `10.37236/12573`, distinct from **Quantum 8, 1396 (2024)**. The revision does not call those published results proofs of the new unrestricted weighted reduction. [EJC publication record](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i3p21).

The recent-result paragraph on p. 3 is appropriately cautious. I checked that Krenn's progress page announces the all-even-order `d ≥ n` obstruction, while the Nexus preprint's §4 Quantum Optics paragraph explicitly displays `N=d∈{4,6,10}` and reference 38 lists the follow-up manuscript as in preparation. The revision distinguishes these claims and does not compare methods from an unavailable paper. [Author's announcement](https://mariokrenn.wordpress.com/graph-theory-question/), [Nexus v2, §4 and reference 38](https://arxiv.org/pdf/2605.22763v2).

The public six-site repository indeed exports the stated complex equation-system proposition in its README. Calling it a public formal artifact rather than a published external theorem, and disclosing that it was not rebuilt here, is accurate. Pin its commit or release in the bibliography for lasting reproducibility; the current link names a moving repository. [Six-site artifact](https://github.com/algal/krenn-gu-6x3-certificate).

One optional precision would strengthen the EJC sentence: its weighted transfer is for simple graphs with unweighted matching index different from one. “Derive weighted consequences” is true, but stating this condition would help readers understand exactly what remained beyond that classification. Likewise, mentioning the earlier colour-isolated-edge terminology would be useful, although the current wording does not falsely claim novelty for pruning.

## Remaining concrete edits, with exact locations

1. **§1.1, pp. 1–2; Lemma 2.2, p. 6:** explicitly say all endpoint colours belong to the target palette, or state that palette restriction is made first. If extra endpoint colours are allowed, rescale only palette-coloured endpoints and leave the others unchanged; structural conclusions then concern the retained aggregate cells. This is a model-interface precision, not a counterexample to the nonexistence theorem.
2. **Figure 1, p. 3:** revise its caption and add a grayscale-safe distinction as described above.
3. **p. 3→p. 4:** the final Related work paragraph is split, with only its last two lines at the top of p. 4. Keep that paragraph together if convenient. It is no longer disrupted by a float.
4. **p. 17→p. 18:** §6 and Corollary 6.1 sit at the foot of p. 17, while the short proof starts on p. 18. Keep the section, corollary, and proof together. The old lonely §5 heading has been fixed.
5. **Appendix B, pp. 20–21:** the reproduction command block starts on a new page after its lead-in. Keep the lead-in with the first command block. No clipped display or figure collision was observed anywhere.
6. **§1.3/references:** pin the recent six-site artifact and optionally give the precise EJC weighted-transfer condition. Do not upgrade the author-announced `d ≥ n` claim to a checked all-order theorem from the displayed Nexus instances.

The final reference page remains partially empty, but the excessive internal-provenance list is gone. That is a normal document-ending issue and should not drive artificial content or enlarged graphics.

## Review record

- Revision TeX SHA256: `8301d26ba9d424a08ce7d8bf4642e568e9c2f98f67ef1fa6d1e22e9ac659db39`.
- Revision PDF SHA256: `b46baec2b1ee27e72caf493875a878ba42b623acf942952ca450e12843b7f53a`.
- PDF: 22 pages; all rendered at 80 dpi and individually inspected; Figures 1, 2, 3 are on pp. 3, 8, 19.
- Earlier reports and both frozen manuscript versions were preserved. Only this fresh rereview report was written.
