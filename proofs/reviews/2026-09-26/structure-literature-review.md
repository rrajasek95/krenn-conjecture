# Literature, attribution, and comparative exposition addendum

This is an **internal simulated referee addendum** to [structure-and-figures-review.md](structure-and-figures-review.md). It concerns the frozen `reviewed-baseline.tex` and `reviewed-baseline.pdf`, not the concurrent revision. The reviewer has participated in the project. I did not edit either manuscript, rerun the formalization, or conduct a new technical audit of every proof in the cited papers.

**Recommendation remains Revise and resubmit; overall 4/5.** The diagnostic scores in the first report remain unchanged: **figures 2/5, vision and significance 5/5**. These are distinct scores, not an overall-presentation/figure-score typo. The current sole figure needs the concrete modifications already listed. Literature and attribution adequacy is **3/5** under our additional diagnostic rubric: the central citations are sound, but one now-published relevant paper and several precise relationships should be added. This is not a finding of unattributed copying or of a prior proof of the full weighted theorem.

## Checked sources and version-sensitive citations

| Primary source | Verified publication and pinpoint | What it supports |
| --- | --- | --- |
| Mario Krenn, Xuemei Gu, and Dániel Soltész, *Questions on the Structure of Perfect Matchings inspired by Quantum Physics* | Proceedings of the 2nd Croatian Combinatorial Days, 57–70 (2019), DOI `10.5592/CO/CCD.2018.05`; the authors’ [arXiv v2](https://arxiv.org/abs/1902.06023v2) confirms this publication. Definitions 2.1–2.3 and Question 1, arXiv pp. 1–3. | Complex weights, different endpoint colours, inherited vertex colourings, their summed matching amplitudes, and the normalized monochromatic-target question. It also distinguishes heralded targets from the unheralded question. |
| L. Sunil Chandran, Rishikesh Gajjala, and Abraham M. Illickan, *Krenn–Gu Conjecture for Sparse Graphs* | MFCS 2024, LIPIcs 306, article 41, 41:1–41:15, [publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2024.41), DOI `10.4230/LIPIcs.MFCS.2024.41`. Use the **published** theorem numbers. | Published Theorem 7, p. 41:5, records Bogdanov’s coloured-multigraph obstruction. Theorems 9–11, p. 41:6, state the weighted sparse results. Aggregation is on p. 41:5; scaling is Lemma 14, p. 41:7; Corollary 17’s degree-one/unique-word close is on pp. 41:10–41:11. |
| L. Sunil Chandran and Rishikesh Gajjala, *Graph-theoretic insights on the constructability of complex entangled states* | **Quantum 8, 1396 (2024)**, published July 3, 2024; [official page](https://quantum-journal.org/papers/q-2024-07-03-1396/), DOI `10.22331/q-2024-07-03-1396`. Its eprint is **2304.06407v3**, not 2202.05562. | Simple-graph dimension bound, edge pruning, and colour-isolated edges. Relevant locations: §3; Definition 11, p. 9; Lemma 12 and Observation 13, pp. 10–11; Theorem 8, p. 8. |
| L. Sunil Chandran and Rishikesh Gajjala, *Edge-Coloured Graphs with only Monochromatic Perfect Matchings and Their Connection to Quantum Physics* | **Electronic Journal of Combinatorics 33(3) (2026), #P3.21**, published **August 7, 2026**; [official page](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i3p21), DOI `10.37236/12573`. This is the published development of **2202.05562**. | Theorem 4, p. 2: Bogdanov obstruction; Theorem 6, p. 4: structural classification; Theorem 34, p. 21, proved in §6.2, pp. 23–24: for **simple** graphs with unweighted matching index different from one, allowing endpoint colours and complex weights does not increase that index. |
| Ilya Bogdanov’s answer to Mario Krenn, *Graphs with only disjoint perfect matchings* | [Original MathOverflow answer](https://mathoverflow.net/questions/267002/graphs-with-only-disjoint-perfect-matchings), April 12, 2017. | The Hamilton-cycle, parity/chord, and minimum-arc argument behind the terminal obstruction. The original question concerns disjoint perfect matchings; the published CGI statement supplies the coloured-multigraph formulation. |

The EJC publication is a substantive bibliography update as of the review date, September 26, 2026. It is **not** the Quantum 2024 paper. Its 26-page published version has different numbering from the 18-page [arXiv v2](https://arxiv.org/abs/2202.05562v2): the latter’s Theorems 1, 2, and 4 correspond to published Theorems 4, 6, and 34. Do not attach the old theorem numbers to the new DOI. The published PDF and publication date were checked directly on the journal’s site.

## Attribution and scope corrections

### Baseline §1.3, pp. 3–4: add the earlier structural classification

The current related-work paragraph correctly separates the Quantum pruning paper from CGI’s weighted sparse results, but omits the other Chandran–Gajjala paper. Add the EJC publication and explain its restricted weighted transfer in one sentence. Its starting invariant is the maximum number of colours in an ordinary edge colouring for which every perfect matching is monochromatic; it is not the general complex-amplitude condition. Its weighted result leaves the simple-graph unweighted-index-one class unresolved. This distinction explains why the paper is relevant without treating it as an earlier solution of the manuscript’s all-orders claim. [EJC, Theorems 6 and 34](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i3p21/pdf/).

Avoid an unqualified phrase such as “the structure of GHZ graphs was already completely classified.” The classified object is the unweighted PMValid colouring problem. Also disambiguate matching-index notation if it is introduced: CGI uses `μ` for its weighted optimization, whereas the EJC paper distinguishes unweighted `μ` from weighted `μ̄`.

The baseline’s CGI references are accurate: low connectivity and bounded degree are assumptions on the underlying graph, not restrictions to real weights or monochromatic endpoint cells. The smallest-counterexample statement is a consequence of its reduction, not a theorem that every GHZ graph is four-connected. Keep the existing “counterexample with the fewest vertices” qualification. [CGI, §1.3, Theorems 9–11](https://drops.dagstuhl.de/storage/00lipics/lipics-vol306-mfcs2024/LIPIcs.MFCS.2024.41/LIPIcs.MFCS.2024.41.pdf).

### Baseline §1.4, p. 4: credit aggregation where it is used

The proof of aggregation is correct, but the reduction is already explicitly recorded by CGI on p. 41:5. Add a citation to that page at the first aggregation paragraph. Keep the distributivity explanation because the aggregate graph is a load-bearing interface to the formal statement. The useful feature here is its rigorous application to the arbitrary endpoint-colour cells and subsequent support assertions, not discovery of the reduction. [CGI, p. 41:5](https://drops.dagstuhl.de/storage/00lipics/lipics-vol306-mfcs2024/LIPIcs.MFCS.2024.41/LIPIcs.MFCS.2024.41.pdf).

Do not equate aggregation with pruning arbitrary weighted edges. Summing identical endpoint-colour cells preserves every colouring amplitude by distributivity; deleting a nonzero aggregate edge generally changes it. The later proof forces the original aggregate support to be rigid rather than constructing a sparser replacement.

### Baseline §2.2, p. 5: normalization is properly credited

The citation to CGI Lemma 14 is already appropriate. CGI proves equivalence of unequal nonzero pure amplitudes and normalized amplitudes by distributing colour-dependent complex root factors across all endpoints. The baseline scales one chosen vertex instead. That is a clean alternative proof of the same equivalence, with a simpler explicit factor `τ_{κ(r)}⁻¹`; it is not a new equivalence theorem. [CGI, §1.4, Lemma 14, p. 41:7](https://drops.dagstuhl.de/storage/00lipics/lipics-vol306-mfcs2024/LIPIcs.MFCS.2024.41/LIPIcs.MFCS.2024.41.pdf).

No revision to the mathematics is needed. “For completeness, we use the following single-vertex version of the scaling lemma” would make the relationship unmistakable. This is a statement about amplitude scaling in the matching model, not a physical implementation theorem for an arbitrary optical circuit.

### Baseline §§6–7, p. 13: distinguish new rigidity from an established closing mechanism

The baseline already attributes its graph lemma to Bogdanov through CGI Theorem 7; that attribution is correct. Its explicit Hamilton-cycle/minimal-arc proof also follows the structure of Bogdanov’s original argument. Strengthen the lead-in to say that the paper **adapts Bogdanov’s argument** to the three disjoint matchings obtained by the new weighted reduction, and optionally cite the original answer as well as the published theorem. [Bogdanov, 2017](https://mathoverflow.net/questions/267002/graphs-with-only-disjoint-perfect-matchings).

There is also a closer published predecessor to the terminal weighted deduction: CGI Corollary 17 derives one nonzero edge of each colour at a vertex under its maximum-degree-three hypothesis, then uses uniqueness of the matching for a receiving word and Bogdanov’s mixed matching to rule out cancellation. Explicitly acknowledge that parallel in the related-work discussion or at the beginning of §6. [CGI, Corollary 17, pp. 41:10–41:11](https://drops.dagstuhl.de/storage/00lipics/lipics-vol306-mfcs2024/LIPIcs.MFCS.2024.41/LIPIcs.MFCS.2024.41.pdf).

This does **not** diminish the proposed new theorem. In the baseline, the difficult implication is from unrestricted original complex GHZ equations to global monochromatic cells and the supported-edge identity, hence to degree one everywhere. It removes the sparse premise needed to reach the familiar closing mechanism. A graph-existence theorem by itself cannot substitute for that weighted reduction: distinct matchings with the same receiving word can cancel until uniqueness has been established.

### Relation to colour-isolated edges and pruning

Quantum’s Definition 11 names an edge colour-isolated when it is monochromatic and both endpoints have colour-degree one. Lemma 12 propagates a colour-degree-one half-edge to this situation for an **edge-minimum GHZ graph**, through a GHZ-preserving pruning argument. The baseline’s conclusion makes **every** retained aggregate colour edge isolated, without an edge-minimality assumption. This is a stronger original-source rigidity statement, not the same pruning operation. [Quantum, §3, pp. 9–11](https://quantum-journal.org/papers/q-2024-07-03-1396/pdf/).

A useful related-work sentence would connect these notions, then explain why the endpoint identity avoids choosing a minimum source. This comparison is my inference from the stated hypotheses and conclusions; I am not claiming that the earlier authors proposed the present replica-kernel proof.

## Concrete exposition lessons from the checked papers

These suggestions compare rendered documents rather than titles or abstracts. The baseline’s only figure was viewed in full; comparator figures cited here were also rendered with `pdftoppm` and inspected using `view_image`.

| Comparator location | Observed feature | Concrete change to this manuscript |
| --- | --- | --- |
| CGI pp. 41:3–41:4; Figures 1–2 | Small examples are adjacent to the graph/weight definitions and explain how matching events produce a colouring amplitude. | Keep the current cancellation example, but put Figure 1 beside §1.2 rather than within Related work. Its caption must independently state that the cancellation example is not a GHZ source. |
| CGI p. 41:6, §1.3 | Theorems with different graph hypotheses are separately stated before the reduction begins. | Give a compact scope table: positive-weight obstruction; simple-graph pruning bound; structural-class weighted transfer; low-connectivity/degree results; present unrestricted weighted claim. Use current publication dates and avoid a “proved/unknown” table copied from 2024. |
| Quantum pp. 6–7, Tables 1–2 | A graph/physics dictionary and a separate model-scope comparison prepare readers from different disciplines. | Replace some repeated introductory prose with a short dictionary for receiving word, matching amplitude, aggregate cell, response tensor, and formal replica. A full physics tutorial is unnecessary. |
| Quantum p. 10, Figure 4 | A three-panel picture illustrates the particular pruning operation immediately next to its lemma. | Add the proposed two-replica/corrected-kernel diagram at the first actual construction, with explicit retained set, two departures, and direct-edge correction. Show the operation that the reader must understand, not an unrelated illustrative graph. |
| EJC p. 5, Figure 1 | The same graph is displayed in two Hamiltonian orders with a worked edge correspondence in the caption. | A small parity-labelled cycle/chord figure can explain why the final graph proof changes viewpoint. State what the selected matching becomes under that ordering. Do not copy the comparator’s reliance on colour alone; use labels and line styles. |

The baseline has an advantage that should be preserved: it immediately explains why mere mixed-matching existence is insufficient with complex weights. The proposed revision should shorten repetition without removing that explanation. The new polynomial-kernel proof needs more reader preparation than the familiar terminal graph argument. Move elementary invariant-theory background and detailed artifact provenance to an appendix if space is needed; keep the endpoint theorem and its finite-degree mechanism in the main text.

## Suggested revision package

1. Add the EJC 2026 paper to §1.3 and the bibliography, using its published theorem numbers and restricted weighted scope.
2. Add the precise aggregation citation; retain the already-correct Lemma 14 normalization comparison.
3. Credit both Bogdanov’s argument and CGI’s bounded-degree unique-word closing mechanism. Frame the new contribution as the unrestricted original-source diagonal/endpoint reduction.
4. Connect the degree-one conclusion to the established colour-isolated-edge terminology, while explicitly distinguishing it from edge-minimum pruning.
5. Add a small scope/notation table and the load-bearing replica/kernel figure; implement the page-flow and grayscale fixes in the original report.

None of these requests changes the mathematical claim or identifies a proved prior result that supplies its new all-orders steps. They improve historical accuracy and make the claimed advance easier to assess.

## Extent and record of this addendum

I checked primary publication records and the relevant full-text passages: Krenn–Gu–Soltész definitions and Question 1; CGI §1.2–§1.4 and Corollary 17; Quantum §3 and its bound’s stated scope; the EJC introduction, classification statement, weighted theorem, and §6.2 proof. I read Bogdanov’s complete original answer. I did not independently reprove the full sparse reduction, the full PMValid classification, or the Quantum dimension bound. The comparative novelty statements above are restricted to the named results, not a claim that an exhaustive literature search was performed.

The newly inspected published EJC figure is p. 5; previously inspected comparator pages are CGI 41:3, 41:4, 41:6 and Quantum p. 10. The EJC arXiv version’s corresponding figure was also viewed; the published version is the citation authority. All pages of the 15-page reviewed baseline and its sole figure were viewed for the original report.

- Frozen TeX SHA256: `88c09b6468a721d92a68051459b1656a1c6a9cd78fca89c2759e84d582a64988`.
- Frozen PDF SHA256: `015b5b4ed08b095346f899d5ab3963d75ff055677888e0ed6ec2eb2e11628363`.
- Publication status verified on September 26, 2026. The EJC publication update supersedes an earlier preliminary message that had verified only the arXiv version.
- Only this addendum was written during this extension; no manuscript, figure source, existing report, or formal artifact was edited.
