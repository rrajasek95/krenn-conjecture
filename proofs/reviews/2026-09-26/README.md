# Manuscript review and revision record — 2026-09-26

Read the [revised paper](../../krenn-gu-all-orders-paper.pdf), or its
[LaTeX source](../../krenn-gu-all-orders-paper.tex). The final presentation has
22 pages, three figures, sixteen cited references, one named definition,
three theorems, eight lemmas, and three corollaries.

## Review process and limits

Three agents reviewed the manuscript from quantum optics, algebra/mathematical
physics, and graph theory/theoretical computer science perspectives. Each read
the paper, consulted primary literature, inspected rendered figures using
vision, made concrete recommendations, and rereviewed a frozen revision.
These are **internal simulated referee reports**, not external peer review or
journal acceptance. The reviewers had project context; one explicitly records
prior participation in the proof work. Their reports state which mathematical
interfaces they checked. They did not rerun Lean or independently verify every
step of the complete proof during this presentation review.

The reports use [Quantum's referee instructions](https://quantum-journal.org/instructions/referees/)
and [APS's guidance for structuring a report](https://journals.aps.org/structuring-report).
Quantum's overall 1–5 rating and recommendation are distinguished from the
additional diagnostic categories created for this exercise. A score measures
the reviewer's assessment of that version, not an acceptance probability.

## Reports and actual scores

| Perspective | Baseline report | Literature review | Revision-1 report | Overall score, baseline → revision 1 | Figure score, baseline → revision 1 |
|---|---|---|---|---|---|
| Quantum optics | [Initial review](quantum-optics-review.md) | [Literature](quantum-literature-review.md) | [Rereview](quantum-revision-review.md) | 2 → 4 | 3 → 4 |
| Algebra and mathematical physics | [Initial review](algebra-review.md) | [Literature](algebra-literature-review.md) | [Rereview](algebra-revision-review.md) | 2 → 4 | 3 → 4 |
| Graph theory and theoretical CS | [Initial review](structure-and-figures-review.md) | [Literature](structure-literature-review.md) | [Rereview](structure-revision-review.md) | 4 → 4 | 2 → 4 |

All baseline reports requested revision. The rereviews describe the major
exposition issues as resolved and request localized further edits. Those
edits were incorporated in the final version below. **The displayed scores
apply to revision 1, not to a newly scored final version.** The graph review's
separate significance score of 5 must not be confused with its figure or
overall score of 4.

## Responses incorporated in the final paper

| Review request | Concrete revision and location |
|---|---|
| Explain the physical model and normalize terminology | §1.1 displays the postselected state and defines paths, modes, amplitudes, the endpoint palette, and perfect matchings. Lemma 2.2 distinguishes algebraic weight rescaling from state-norm normalization. |
| Explain what is copied | §2.5 constructs two disjoint symbol families with the same vertex–colour labels, displays their block pairing table, proves factorization and a transformed pairing calculation, and defines the complex orthogonal group. Figure 2 illustrates this precise operation. The abstract uses the same meaning. |
| Distinguish the two algebraic settings | §§2.2–2.4 define rows, colour words, tensors and coefficient extraction, and distinguish the site quotient from the ordinary polynomial ring used by the Wick functional. The repeated-symbol example shows why the latter does not descend to the former. |
| Define shifts, pairings and derivatives | §2.6 gives the shifted coefficient identity, the local alternating pairing and its signed word formula, parity conventions, and directional derivatives. “Mean” is explicitly a scalar shift. |
| Explain roots, responses and terminal terms | §3.1 derives incident rows from the original graph. §3.2 defines the parameter ring, explains polynomial cancellation and polarization, and separates reflection, common-factor and finite-degree arguments. Repeated occurrences of a symbol are distinguished from copies of a family. |
| Make binary scope exact | The root and omission calculations explicitly use binary projections. §4 chooses distinct colours, quantifies the derivative direction and defines deletion cofactors. Lemma 4.2 applies to distinct vertices. |
| Explain the endpoint construction before manipulating it | §5.1 fixes the two roots, retained vertex set, all scalars and a four-row dictionary. Lemma 5.2 proves the two-root identities; Corollary 5.3 derives their specializations. §5.2 explains every copy index and the direct-edge correction in the insertion matrix. |
| Separate classical invariant theory from the new matrix restriction | Lemma 5.4 and its main-text explanation identify both symmetry and matching-specific divisibility. The scalar invariant theorem is not presented as proving the matrix form. Appendix A gives the full coordinate argument, explicit nonzero conditions and polynomial extension. |
| Expose the differential-equation mechanism | §5.4 states the elementary polynomial lemma, displays the Gram-coordinate chain rule, and separates elimination of the rank-one part from determination of the scalar part. |
| Label results and their dependencies | Named definitions, theorems, lemmas and corollaries use a shared section-based numbering scheme. The supported-edge result is Theorem 5.1; degree one and uniqueness are Corollaries 6.1–6.2. Each has its own proof or an explicit pointer to it. |
| Make support counting and graph disjointness precise | §6 counts every supported edge, proves uniqueness before noncancellation, and excludes two colours sharing an unordered vertex pair. §7 defines a mixed matching and attributes the graph argument. |
| Improve figures and inspect them visually | Figure 1 includes explicit matching sets and products, line-style cues usable without colour, and a standalone non-GHZ qualification. Figure 2 explains copies. Figure 3 gives two correct eight-cycle matching constructions with dashed chords, solid selected cycle edges and an explicit crossing convention. |
| Keep technical detail and reproducibility available | Appendix A contains the normal-form coordinates. Appendix B records the exact Lean statement, its verification boundary, pinned artifact links and executable reproduction commands. Main-text motivation remains next to each construction. |

The final rendering also keeps §6's first corollary with its short proof,
the reproduction lead-ins with their command blocks, and the sixteen
references on one page. All original numbered equations (1)–(10) remain.

## Literature and attribution corrections

The three literature reports record the primary sources and the scope actually
checked. The manuscript now:

- Credits the original graph/physics correspondence and the weighted-interference formulation separately.
- Credits Chandran–Gajjala–Illickan for aggregation, normalization equivalence and the cubic uniqueness-to-Bogdanov strategy, with the relevant published locations.
- Attributes the alternating-cycle/minimal-arc obstruction to Bogdanov, and distinguishes it from the unrestricted algebraic reduction claimed in this paper.
- Distinguishes the simple-graph dimension bound, the monochromatic-edge SAT exclusions, and the separate EJC 2026 classification paper.
- Cites the actual Isserlis pairing formula and the appropriate polarization and scalar orthogonal-invariant sections of Kraft–Procesi. The formal complex pairing definition and the additional matrix argument are explained in the paper.
- Distinguishes a public six-vertex artifact, Krenn's announced general dimension bound, and the explicit examples in the Nexus preprint. The external six-vertex artifact is pinned to revision `c04696e515e0c02be140353fb52ea60c62e827b1`; it was not independently rebuilt here.
- Acknowledges the accepted FSTTCS 2026 connectivity paper only at the level supported by its official listing. No method or theorem is inferred from its title. The similarly unavailable tensor-algebraic manuscript remains identified as in preparation.

The literature search is bounded, not a certification of exhaustive novelty.
The optional suggestions of a fourth figure for the direct-edge insertion term,
a shorter repeated overview, and a fuller account of the EJC classification's
weighted-transfer hypotheses were not adopted in this pass. The current text
explains the correction term in prose and equations and makes only the broader,
supported statement that the classification gives weighted consequences.

## Versions and validation

Baseline: [TeX](reviewed-baseline.tex), [PDF](reviewed-baseline.pdf), 15 pages.
Revision 1: [TeX](reviewed-revision-1.tex), [PDF](reviewed-revision-1.pdf), 22 pages.
The reports' page numbers refer to their explicitly named frozen version.

| Artifact | SHA-256 |
|---|---|
| Baseline TeX | `88c09b6468a721d92a68051459b1656a1c6a9cd78fca89c2759e84d582a64988` |
| Baseline PDF | `015b5b4ed08b095346f899d5ab3963d75ff055677888e0ed6ec2eb2e11628363` |
| Revision-1 TeX | `8301d26ba9d424a08ce7d8bf4642e568e9c2f98f67ef1fa6d1e22e9ac659db39` |
| Revision-1 PDF | `b46baec2b1ee27e72caf493875a878ba42b623acf942952ca450e12843b7f53a` |
| Final TeX | `c4ddd41bb4ae362ca760bfd5a7bf7c22d3d4d6b18069de8e7e4fd0ce25f9812e` |
| Final PDF | `77541fe720739777f04d5a851dcfb07d5129e3934305c6281ce6451a8a093359` |
| Unchanged frozen mathematical source | `fb0fa1e9447d8044981692d6e9bbbeff8e6a2cfc90119b6a296cbf506b9a3c9d` |

The final paper was rebuilt with `python3 -B proofs/build_krenn_gu_paper.py`:
all sixteen references are cited, with no citation, cross-reference or layout
warnings. All three reviewers visually inspected the revision-1 figures;
the graph reviewer inspected every revision-1 page. After the final edits, the
editor rendered and visually checked pages 3, 8, 17–22, including all three
figures, the revised coefficient argument, both appendices and the bibliography.
No clipping or figure-label collisions were observed. The two illustrated
matching sets were checked for vertex coverage.

The frozen proof's hash is unchanged. The Lean sources were not edited, and
this presentation pass did not rerun the complete Lean verification. Existing
formal verification, internal exposition review and future external peer review
are separate records.
