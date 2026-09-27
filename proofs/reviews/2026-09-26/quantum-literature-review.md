# Internal literature and attribution review: quantum-optics perspective

**Checked September 26, 2026.** This supplements [the quantum-optics presentation report](quantum-optics-review.md). It is an internal simulated review, not an external referee report or an exhaustive novelty certification. The comparison is to [the frozen baseline](reviewed-baseline.pdf); the manuscript is being revised separately.

I inspected the relevant sections of the primary papers and their publication records, including the published Quantum PDFs, the MFCS proceedings/full version, and the original graph-model papers. I visually inspected Quantum 2022 Figure 1 and Quantum 2024 Figure 5. For recent developments I checked the authors' public status page, arXiv metadata/text, and the public six-vertex proof repository. I did not rerun external formal artifacts or inspect any unavailable manuscript.

## Principal corrections

1. Credit the original graph–optics correspondence, rather than relying only on the later question paper and algorithm paper.
2. State restricted results with their restrictions: simple graphs and monochromatic-edge graphs are different classes.
3. Credit the existing uniqueness-before-Bogdanov strategy in the sparse-graph paper. The manuscript's proposed new contribution is its general algebraic route to that structure.
4. Update related work through the publicly announced 2026 bound and the released six-vertex formal artifact, distinguishing publication, announcement, and independently checked evidence.
5. Do not identify an in-preparation title as an available or accepted no-go paper, or infer its full theorem from the examples in another article.

## Primary-source audit

### Original physics mapping

Krenn, Gu and Zeilinger, *Quantum Experiments and Graphs: Multiparty States as Coherent Superpositions of Perfect Matchings*, **Physical Review Letters 119, 240403 (2017)**, is the direct original attribution for the experimental correspondence. Its Figure 1 and Table I connect paths, pair sources, coincidences, and matchings; its illustrated combinatorial argument concerns the specified disjoint-matching setting, not an unrestricted cancellation theorem. Add it to the first paragraph and bibliography. [Primary author manuscript](https://arxiv.org/pdf/1705.06646), [publication DOI](https://doi.org/10.1103/PhysRevLett.119.240403).

Gu, Erhard, Zeilinger and Krenn, *Quantum Experiments and Graphs II: Quantum Interference, Computation and State Generation*, **PNAS 116, 4147–4155 (2019)**, explicitly develops complex weights and interference between matching contributions. This is the appropriate additional citation if the introduction discusses the physical meaning of destructive cancellation, rather than only defines an abstract weighted graph. I checked the interference discussion and publication metadata, not every experimental extension. [Primary author manuscript](https://arxiv.org/pdf/1803.10736), [publication DOI](https://doi.org/10.1073/pnas.1815884116).

### Original weighted question and model boundaries

Krenn, Gu and Soltész, *Questions on the Structure of Perfect Matchings Inspired by Quantum Physics* (2019), Definitions 2.1–2.3 and Question 1, already specify complex weights, endpoint colours, and sums over inherited colourings; Figures 1 and 4 include multiple edges. Section 3 explicitly distinguishes Question 1 without trigger photons from Question 2 with heralding photons. Questions 3–4 concern approximation. Thus our theorem should be described as exact nonexistence in the stated matching model, not as a prohibition on GHZ preparation using all physical resources or as a quantitative fidelity bound. The baseline's citation to Question 1 is appropriate. [Primary paper, especially pp. 2–4 and 7–9](https://arxiv.org/pdf/1902.06023).

### Quantum 2022: what SAT established

Cervera-Lierta, Krenn and Aspuru-Guzik, *Design of quantum optical experiments with logic artificial intelligence*, **Quantum 6, 836 (2022)**, published October 13, 2022. Section 3.1 explains that satisfying its Boolean support conditions does not ensure that complex weights realize the target. Section 3.2 reports SAT exclusions at \((n,d)=(6,3),(8,4)\) **with monochromatic edges**; larger dimensions follow by colour restriction. The proposed all-orders \(d\ge n/2\) obstruction is a conjecture there. Do not cite it as a proof for arbitrary bicoloured edges.

Presentation lesson from the inspected PDF: Figure 1, p. 3, puts each inherited colouring beside its matching contributions and amplitude equation. Section 3 then teaches the Boolean representation before deploying it. Our two-copy construction should provide the equivalent explicit dictionary and one worked coefficient calculation. [Published PDF, §§2–3.2](https://quantum-journal.org/papers/q-2022-10-13-836/pdf/), [publication record](https://quantum-journal.org/papers/q-2022-10-13-836/).

### Quantum 2024: simple graphs, with bichromatic edges allowed

Chandran and Gajjala, *Graph-theoretic insights on the constructability of complex entangled states*, **Quantum 8, 1396 (2024)**, published July 3, 2024. Theorem 8, p. 8, excludes \(d\ge n/\sqrt2\) for simple graphs on \(n>4\) vertices. Complex weights and bichromatic edges are allowed; parallel edges are excluded. The scope table on p. 7 helps distinguish this theorem from monochromatic-edge SAT results.

Section 4.1 explains how two intermediate bounds combine before proving them. Figure 5, p. 13, shows a graph next to its representative sparse subgraph. This is a good model for our endpoint section: define the intended reduction, explain what survives, then calculate its coefficients. [Published PDF, Theorem 8 and §§4.1–4.3](https://quantum-journal.org/papers/q-2024-07-03-1396/pdf/), [publication record](https://quantum-journal.org/papers/q-2024-07-03-1396/).

### MFCS 2024: general weighted model and an existing endgame

Chandran, Gajjala and Illickan's **MFCS 2024** paper allows complex weights, bichromatic edges, and multigraphs. Its degree/connectivity restrictions concern the underlying simple skeleton. Theorems 9–11 give the low-connectivity/cubic results and a reduction implying four-connectivity of a minimum-vertex counterexample. Lemma 14 supplies the generalized-to-normalized GHZ equivalence. Their preliminaries also describe aggregating parallel edges with identical endpoint colours.

Crucial attribution: the proof of Theorem 11 already combines uniqueness of a matching for an inherited colouring with Bogdanov's obstruction to eliminate cancellation. This occurs in **§2.3, p. 41:11 of the proceedings version**; the full arXiv version calls it §3.3. Our paper should explicitly acknowledge that strategic precedent. This does not identify the two-copy algebra as previously proved. [Published proceedings PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol306-mfcs2024/LIPIcs.MFCS.2024.41/LIPIcs.MFCS.2024.41.pdf), [full version](https://arxiv.org/html/2407.00303v1).

## 2026 developments and discoverability

### AlphaProof Nexus and the in-preparation no-go manuscript

Tsoukalas et al., *Advancing Mathematics Research with AI-Driven Formal Proof Search*, arXiv:2605.22763v2, June 8, 2026, §4, reports quantum-graph results and singles out \(N=d\in\{4,6,10\}\). Reference 38 lists Krenn, Firsching, Tsoukalas, Gajjala, Gu and Chaudhuri, *A Tensor-Algebraic No-Go Theorem for High-Dimensional Photonic GHZ States*, as **in preparation**. It provides no linked standalone manuscript. The listed examples do not limit the announced manuscript's possible scope. [Primary text and bibliography](https://arxiv.org/html/2605.22763v2), [version metadata](https://arxiv.org/abs/2605.22763).

Krenn's own problem page separately reports that \(d\ge n\) is excluded for every even \(n\), under May 2026 progress and July 23, 2026 news. This is a primary author announcement, but it is a different source from the displayed instances in the Nexus article. Attribute the broader statement to the status page unless citing an exact public theorem artifact. [Krenn's problem/status page](https://mariokrenn.wordpress.com/graph-theory-question/).

Exact-title searches and searches combining these authors with GHZ/no-go/Krenn–Gu did not locate an available standalone version or a publisher record in this review. This is a bounded search result, not proof that no such manuscript exists. Do not claim to compare its method, assert disjoint scope, or assign priority on the basis of its title.

### Public six-vertex formal artifact

The repository **algal/krenn-gu-6x3-certificate** publicly exports a theorem for the exact complex-weight \(\mathrm{EqSystemN}\;6\;3\) statement. Its README describes an algebraic reduction, symmetry/orbit classification, and Lean replay of finite certificates. The companion explainer dates its release to July 2026 and explicitly limits the result to six vertices. It also discloses the native-compiler trust boundary. This is relevant prior formal work and should be cited as a public proof artifact, rather than omitted because it is not a journal paper. I checked the displayed statement and documentation, not a fresh build. [Primary repository](https://github.com/algal/krenn-gu-6x3-certificate), [author explainer](https://krenngufun.org/).

Other search hits included provisional public research repositories. They should not be promoted to established theorems based on search snippets. They also do not supply evidence about the unavailable no-go manuscript.

## Concrete manuscript changes

- **Introduction, first paragraph:** add the original PRL correspondence citation and, if discussing interference physically, the PNAS continuation. Keep the mathematical question citation separately attached to the conjecture's formulation.
- **Related work:** distinguish published structural theorems, finite computational exclusions, preprints, author announcements, and released formal artifacts. A compact table with columns “assumptions,” “conclusion,” and “evidence/source” would prevent accidental scope inflation.
- **Contribution paragraph:** add: “The final uniqueness-and-obstruction argument follows a strategy already used in the cubic case. Here the structural restriction is obtained algebraically without a sparsity assumption.” Cite the MFCS proof at its correct proceedings location.
- **Normalization and aggregation:** retain explicit proofs because they explain the exact interface to Lean; cite the prior standard reductions without treating them as new contributions.
- **Physics conclusion:** refer back to the precise state-amplitude model and exact solvability. The proof does not itself yield a fidelity gap, a success-rate inequality, or impossibility with auxiliary target-independent resources.
- **Recent literature paragraph:** acknowledge the announced dimensional bound and finite formal release with their source types. Refer to the no-go manuscript only as in preparation as cited by Nexus; no claim of having read it.
- **Internal-note citations:** retain provenance in an artifact/provenance paragraph. Lead technical sections with the mathematical purpose rather than the history of their discovery.

The revised literature discussion should identify what the new argument contributes beyond established strategies and should let readers verify every model restriction without opening several references. No conclusion about priority is warranted from this review alone.
