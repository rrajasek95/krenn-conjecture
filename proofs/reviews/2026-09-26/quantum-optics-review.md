# Internal simulated referee report: quantum-optics readership

**Manuscript reviewed:** *A two-replica proof of the Krenn–Gu conjecture*, September 26, 2026, 15-page PDF built at 21:42:16 PDT, preserved as [reviewed-baseline.pdf](reviewed-baseline.pdf) and [reviewed-baseline.tex](reviewed-baseline.tex). Page references below refer to that PDF, before subsequent revisions. Baseline PDF SHA-256: `015b5b4ed08b095346f899d5ab3963d75ff055677888e0ed6ec2eb2e11628363`.

**Role and limits:** This is an internal simulated journal referee report, written from the perspective of a quantum-optics researcher familiar with photonic state preparation and matching models but not the manuscript's auxiliary algebra. It is not external peer review, an acceptance prediction, or an independent certification of the proof. I read the complete LaTeX source and PDF text. I rendered and visually inspected PDF pages 3, 6, 7, 10, and 11, including both panels of the only figure. I did not rerun the Lean artifact.

**Recommendation as presented: Revise and resubmit (major revision); overall rating 2/5.** These fields follow [Quantum's official referee form](https://quantum-journal.org/instructions/referees/), consulted September 26, 2026. This presentation-focused rating is not an assessment of whether an independently validated result would meet the journal's scientific threshold. The cancellation-based overview and the short supported-edge-to-degree-one deduction are effective. The principal obstacle is the unexplained transition from physical graphs to a succession of formal constructions. Section 2 introduces some vocabulary, but Sections 3–5 repeatedly require new meanings of familiar words and unannounced changes of mathematical setting. A physics reader can follow the desired conclusion without being equipped to understand the argument that establishes it. The revision should repair those local transitions, not merely append a notation glossary.

**Summary and contribution:** The paper asks whether arbitrary complex matching amplitudes can realize a GHZ target with at least three active colours on more than four vertices. Its proposed route proves that each aggregate edge is monochromatic and each active colour is a perfect matching, eliminating cancellation before using a combinatorial obstruction. A verified resolution would be significant to this model of quantum-state construction. This report evaluates whether the manuscript communicates that route, without certifying novelty or validity independently.

**Assumptions, literature, and reproducibility:** The graph model and nonzero-amplitude assumptions are explicit, but their physical interpretation and the distinction between algebraic and state normalization need improvement. The cited matching-model, sparse-graph, and logic-design papers provide relevant orientation; I have not performed an exhaustive literature or priority audit. Internal notes are clearly identified as internal, but their prominent placement interrupts the exposition. There are no new numerical or laboratory experiments requiring reproduction here. Formal-proof documentation is substantial; its commands were not rerun in this review. I am available to rereview the revised exposition and figures.

## Scores

The categories below are a diagnostic extension to Quantum's official overall 1–5 rating, not additional official journal questions. The diagnostic scale is 1 = poor, 2 = substantial deficiencies, 3 = adequate but needs revision, 4 = strong, 5 = excellent.

| Criterion | Score / 5 | Reason |
|---|---:|---|
| Conceptual clarity | 2 | The initial cancellation problem and endgame are clear; the mathematical mechanisms producing the structural identities are insufficiently introduced. |
| Notation and definitions | 2 | Rows, words, tensors, coefficient evaluation, mean shifts, source families, and the alternating pairing lack adequate definitions at their first uses. |
| Terminology and scope | 2 | “Copies,” “independent,” “covariance,” “means,” “source,” and “response” carry physical or probabilistic meanings that differ from the intended formal meanings. |
| Organization | 3 | The overview has a good destination-first structure. Technical sections still follow research derivations rather than a sequence of questions a reader can answer. |
| Figures | 3 | Both existing panels are legible and useful. The unfamiliar replica construction and the final graph argument have no visual support. |
| Reproducibility documentation | 4 | The exact theorem, artifact, toolchain, and axiom audit are identified. This score assesses documentation, not a fresh build or source-to-paper verification. |
| Overall presentation | 2 | Promising exposition of the problem surrounds a technical core that is not yet accessible to the stated physics-journal audience. |

## Major issues and concrete repairs

### 1. Define the physical state and the scope of the no-go result

**Location:** abstract and Sections 1–1.1, pp. 1–2.

The graph-to-state bridge is stated verbally, but the reader is never shown the resulting state. Introduce the unnormalized postselected state explicitly:

\[
|\psi_G\rangle=\sum_{\kappa:V\to[d]}W(\kappa)\bigotimes_{v\in V}|\kappa(v)\rangle_v.
\]

Explain that a vertex labels an output subsystem/path and its endpoint colour labels an internal basis mode. An edge weight is a complex pair-production contribution, not a probability. The constant colourings give the GHZ-type state \(\sum_h\tau_h|h\rangle^{\otimes n}\).

Suggested prose:

> We study the state amplitudes described by this perfect-matching model, conditioned on one photon in each output path. All conclusions concern this model. The complex numbers \(W(\kappa)\) are unnormalized amplitudes; no probability interpretation is assigned to an individual matching weight.

In Section 2.2, distinguish setting the pure amplitudes to one from normalizing the quantum state's norm. The former changes weights and is an existence-preserving algebraic rescaling, generally not a unitary transformation of the state. The existing one-root formula is an excellent explanation once this distinction is stated.

### 2. Define what a “copy” is and write its pairing table

**Location:** Section 2.4, p. 6; Section 3 proof, p. 7.

“Take two copies \(X_i,Y_i\)” leaves unanswered: copies of which objects, what does \(i\) index, what mathematical relations do they satisfy, and what is meant by identical? The next display silently changes to \(X_{i,\alpha_i}\). “Independent identical replicas” can suggest independent random fields, repeated experiments, or copies of a quantum state. None is needed here.

Replace the opening of Section 2.4 with a construction such as:

> Let \(I\) be the set of vertex–colour labels \((v,h)\). For each label \(\ell\in I\), introduce two distinct formal symbols \(X_\ell\) and \(Y_\ell\). These are two copies of the symbol family: the same pairing coefficients are assigned within each family, and every pairing between families is zero. Explicitly, for the symmetric bilinear pairing \(C\),
> \[
> C(X_\ell,X_m)=C(Y_\ell,Y_m)=c_{\ell m},\qquad C(X_\ell,Y_m)=0.
> \]
> The word “copy” refers only to this duplicated algebraic data. No second physical experiment or independently prepared quantum state is introduced.

Then calculate at least one transformed coefficient:

\[
C(X'_\ell,Y'_m)=\tfrac12(c_{\ell m}-c_{\ell m})=0.
\]

State that the pairing is **complex bilinear**, not Hermitian. Define \(\mathrm O(2,\mathbb C)=\{O:O^TO=I\}\); the transpose contains no complex conjugation. This is why orthogonal, rather than unitary, changes appear. When the proof uses two copies of the auxiliary symbol \(g\), say that the whole family, including \(g\), is duplicated.

### 3. Separate the site algebra from the algebra of Wick symbols

**Location:** transition from Sections 2.1 to 2.3, pp. 5–6.

The lowercase site variables obey \(x_{v,h}x_{v,k}=0\). The later uppercase Wick symbols must not be understood to inherit these relations. For instance, if \(C(X_v,X_w)=c\) and self-pairings vanish, then \(\mathcal W(X_v^2X_w^2)=2c^2\), which need not vanish. Therefore the Wick functional is not simply a functional on the earlier quotient with its same-site products set to zero.

Add:

> The Wick symbols introduced next are ordinary commuting formal symbols, distinct from the site variables in \(\mathcal A_V\). They do not satisfy the site relations. The two descriptions agree on the specified matching coefficients because those expressions select one coordinate at each vertex.

Explain each passage between the two descriptions by the relevant coefficient identity. This is a conceptual ambiguity with potential mathematical consequences for a reader, not merely a preference in notation.

### 4. Introduce root rows and responses before stating the general lemma

**Location:** Section 3, pp. 6–8.

The heading “Whole binary higher responses vanish” and the first lemma presume a vocabulary never defined. “Row,” “word,” “tensor,” “response,” “polarization,” and \(H_p(L)(w)\) all arrive without adequate explanation. In optics, a “source” naturally means a pair emitter; here it means the entire matching polynomial satisfying the target equation.

Start from the graph construction:

\[
A=R+\sum_h x_{p,h}L_{p,h},\qquad
L_{p,h}=\sum_{v\ne p,k}A_{pv}(h,k)x_{v,k}.
\]

Explain that \(R\) consists of edges avoiding the chosen vertex \(p\), while \(L_{p,h}\) lists the ways an edge can leave \(p\) in colour \(h\). The product \(L_{p,h}R^{[m]}\) completes that incident edge to a full matching and records the remaining vertices' colours. This is the “response.” Only then generalize to a linear space \(D\) of such linear forms.

Define a word as a map from vertices to colours, and define \([w]T\) as its monomial coefficient. Explain that “tensor” here can be read as the array of these coefficients. Use one notation for coefficient extraction throughout; currently \(H_p(L)(w)\) and \([w]H_p\) alternate.

Give the combinatorial meaning of a higher response: several incident-row insertions replace several matching edges, with the remaining sites paired by \(R\). Such insertions are auxiliary algebra, not multiple physical uses of the same root.

Replace “whole binary higher-response vanishing” with a reader-facing heading such as “Vanishing identities after deleting one vertex,” preserving the technical name only after definition. Replace “source” with “matching polynomial” or “graph satisfying the target equations” unless its special meaning is explicitly introduced.

### 5. Define the alternating pairing, shifts, and derivatives locally

**Location:** Section 3, pp. 7–8; Section 4, pp. 8–9; Section 5, p. 10.

The sentence defining \(K\) as a product of local alternating pairings does not define a computable operation for the intended reader. Provide its local table on a binary colour basis:

\[
\epsilon(a,b)=1,\quad\epsilon(b,a)=-1,\quad
\epsilon(a,a)=\epsilon(b,b)=0,
\qquad K(x^{w},x^{w'})=\prod_{v}\epsilon(w(v),w'(v)),
\]

where \(x^w=\prod_v x_{v,w(v)}\), followed by bilinear extension. This immediately explains the odd/even parity of \(K\), why complementary colourings survive, and the normalization used later. There is no need to assume the reader knows a tensor contraction convention.

“Mean” should be introduced as a traditional name for an auxiliary scalar shift \(X_{v,h}\mapsto X_{v,h}+L_{v,h}\), not an expectation value of a physical field. Define

\[
E_V(U)=\left.\frac{d}{dt}E(U+tV)\right|_{t=0}
\]

before its first use, and state that \(Q\) is held fixed. Explain that each derivative inserts a specified row. Define “polarization” in the needed elementary form: substitute \(L=\sum_j t_jL_j\) into a homogeneous polynomial identity and compare the coefficient of a product of independent parameters.

The ordinary polynomial rings in the row parameters should be distinguished from the site algebra. Cancellation is valid in those parameter rings because they have no zero divisors; it is not being asserted in the nilpotent site algebra.

### 6. Reorganize the endpoint argument around its purpose

**Location:** Section 5, pp. 9–12.

The new paragraph explaining \(M+efI\) is useful, but it occurs after a dense block of definitions and four unmotivated boundary equations. “Literal binary quadratic,” “root row planes,” “mean parameters,” “kernel,” and “Gram coordinates” remain abrupt.

Recommended order:

1. Restate the goal: the subtotal through \(pq\) equals the full pure amplitude.
2. Distinguish the two ways to match the roots: directly to one another, or separately into the retained vertices.
3. Define \(B,H\) as the two symmetric edge-weight matrices and write the retained quadratic \(Q\) explicitly. Remove “literal.”
4. Define the four rows \(x,y,u,v\) in a small table, with columns for root, colour, and meaning. Use scalar parameter names that do not collide with the colour coordinates \(a,b\).
5. Explain \(E\) as a finite generating polynomial counting pairings plus scalar insertions. Define \(P,Q_c,R_c,S_c\) as columns of coefficients selecting which row is inserted in each of the two copies.
6. Show one boundary identity in detail as an expansion by how a root is matched. List the other three as its relabelings.
7. Introduce \(T\) and explain that symmetry restricts its possible dependence on these columns. Define a “kernel matrix” as this matrix of insertion coefficients, rather than relying on the overloaded word kernel.
8. Explain the two consequences separately: the rank-one coefficient is forced to zero; the remaining scalar coefficient is forced to a constant.

The invariant-theory coordinate calculation and the dense-open-set extension can move to an appendix after their logical role is stated. The definition of the construction and the polynomial-degree obstruction should remain in the main text.

### 7. Reduce historical proof narration and supply a conceptual map

**Location:** Sections 3–5 and 8, pp. 6–14.

Sections currently begin by identifying internal notes from which the arguments arose. This explains provenance but does not help a new reader understand the next step. Begin instead with the mathematical question being answered. Consolidate research-note provenance in one final note or the artifact appendix.

A useful main-text sequence is: model and cancellation; structural endgame; formal pairings and two-copy construction; rooted vanishing and diagonal reduction; endpoint identity; graph obstruction; formal verification. Divide the long Section 3 proof into three named stages: reflection gives a common factor; rotations constrain that factor; finite degree makes it constant. End each technical section by explicitly stating which step of the overview is now proved.

## Figure and visual presentation review

### Figure 1(a), p. 3: cancellation example

The rendered labels and weight signs are legible and do not overlap. The red/blue halves of the vertical edges agree with their endpoint colours, and both perfect matchings indeed induce the stated mixed colouring. However, the reader must mentally extract both matchings from the single square.

Concrete improvement: place the two matching sets or products directly beneath this panel, \(\{12,34\}:1\) and \(\{13,24\}:-1\). An alternative is two tiny matching diagrams separated by a plus sign. Explain \(1:a\) in the caption as “vertex 1, inherited colour a.” Preserve a non-colour cue, such as endpoint letter labels or line styles, for grayscale and colour-vision accessibility.

### Figure 1(b), p. 3: four-vertex example

This panel is visually clean. The caption correctly says that the crossing is not a vertex, and its matching decomposition is easy to check against the adjacent text. A single colour label represents a pair of equally coloured edges; this is adequate with the caption but a compact legend would be safer. State in the panel or caption that all edge weights are one and that the three pure amplitudes are each one. Keep the example: it explains a true boundary of the theorem rather than merely decorating the introduction.

### Missing figure: algebraic copies and pairings

Add a diagram in Section 2.4 with two rows of formal symbols, one labeled copy 1 and the other copy 2, the same within-row pairing coefficients, and zero cross-row pairings. Put the explicit pairing table beside it. An arrow labeled \(O^TO=I\) should act on the copy index while vertex/colour labels stay fixed. The caption must say it depicts an algebraic construction, not extra photons or a physical circuit. The diagram should avoid implying that an arbitrary complex orthogonal change is an implementable optical device.

### Optional figure: the graph endgame

Section 7, p. 13, asks the reader to track equal-parity chords, interlacing, and a minimal arc entirely in prose. A small alternating cycle with one opposite-parity chord and a second panel showing interlacing opposite-parity chords would make the local matching constructions checkable. A final shaded arc can explain the minimality contradiction. Do not reuse the colour coding for graph parity and matching colour without a legend.

### Typesetting observations

The inspected pages show no obvious clipping or overlapping equations. The difficulty is semantic density, especially p. 7 and the uninterrupted definition/identity sequence on p. 10. Local explanatory sentences and modest subsection breaks will help more than increased whitespace alone. The p. 6 lemma statement breaks onto p. 7; that is acceptable, but the introductory definitions should precede the statement rather than being dispersed through its proof.

## Minor revisions

- Define “active colour” at first use as one with nonzero pure amplitude; all target colours are active under the stated hypothesis.
- Extend \(A_{uv}(i,j)\) explicitly to both vertex orders by \(A_{vu}(j,i)=A_{uv}(i,j)\), since later formulas use arbitrary ordered pairs rather than only \(u<v\).
- Define “one-defect word” as the colouring that assigns \(i\) at one designated vertex and \(h\) at every other vertex.
- Define \(\mathbb C[D]\) as the ring of polynomial functions of coordinates on the row space; do not make the reader infer that \(D\) has become a parameter space.
- Explain “terminal” as the largest insertion degree, where no retained matching edges remain.
- Define “isotropic” when first needed, or move the technical qualification to the appendix. Over complex coefficients, a nonzero vector can have zero bilinear square.
- Define Gram variables using the bilinear dot product, \(P\cdot Q=P_1Q_1+P_2Q_2\), without complex conjugation.
- Replace vague “by extension” with the precise reason: a polynomial identity holding on the indicated dense open set holds identically.
- Avoid the collision of \(b\) as colour coordinate, scalar parameter, and normal-form coefficient; likewise clarify the successive uses of \(R,Q,U\).
- Keep the exact formal theorem and graph-to-normalized-interface distinction. Move filenames, axiom names, and reproduction details to an artifact appendix or boxed reproducibility note so they do not interrupt the mathematical conclusion.

## Mathematical concerns requiring clarification, not claimed counterexamples

I found no counterexample or demonstrated false theorem during this presentation review. The distinctions above—ordinary Wick symbols versus site variables, scalar parameter domains versus the quotient algebra, and bilinear versus Hermitian symmetry—are mathematically material and must be explicit. The reduction from displayed replica moments to the coefficient identity (3), and from the root identities to the four equations (7), presently proceeds too quickly for a physics referee to verify from the prose. At least one complete coefficient-counting example should be supplied; the full bookkeeping can be appended. A linked formal proof is valuable evidence but does not replace these explanations in a paper intended to communicate a new method.

## Minimum revision needed before rereview

1. Define copies by their symbol sets and pairing table, including the complex-bilinear convention.
2. Distinguish the two algebras and give the coefficient correspondence used between them.
3. Introduce root rows, words, responses, shifts, derivatives, and the alternating pairing before using them.
4. Reorganize the endpoint section around direct-root versus retained-vertex matchings and provide one full boundary-identity derivation.
5. Add the algebraic-copy figure; improve the cancellation panel's self-contained explanation.
6. Perform a sentence-by-sentence first-use audit throughout Sections 3–5, not just the introduction.

The manuscript's strongest explanatory asset is already present: once the supported-edge identity is understood, the obstruction follows in a few transparent lines. The revision should make every auxiliary construction answer a specific question on the route to that identity.
