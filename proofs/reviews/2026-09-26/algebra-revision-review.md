# Algebra referee rereview: revision 1

**Presentation recommendation: minor revision; overall presentation rating 4/5, improved from 2/5.** In the terminology of the Quantum referee form, the remaining recommendation is “Revise and resubmit,” now for localized presentation repairs rather than a foundational exposition rewrite. This is an internal simulated review, not a journal decision or an independent certification of the theorem.

## Reviewed version and extent of checking

The stable files reviewed were `reviewed-revision-1.tex` and `reviewed-revision-1.pdf` in this directory. Their SHA-256 values match those supplied for review:

- TeX: `8301d26ba9d424a08ce7d8bf4642e568e9c2f98f67ef1fa6d1e22e9ac659db39`
- PDF: `b46baec2b1ee27e72caf493875a878ba42b623acf942952ca450e12843b7f53a`

The PDF has 22 pages. I read the revised source throughout, checked the new definitions against their uses in Sections 3–7 and Appendix A, and visually inspected rendered pages **3, 8, 9, 14, 15, 16, 17, 19, and 20**. This includes all three figures and the principal dense algebra pages. I checked the normalization construction, coefficient/pairing bridge, explicit binary projections, boundary-identity derivation, division of the matrix argument between main text and appendix, and the local logic of the endpoint conclusion. I did not rebuild the Lean development or independently certify the full matching theorem, and I did not repeat the entire external graph/physics literature audit.

The rating follows the overall scale of [Quantum's referee form](https://quantum-journal.org/instructions/referees/). Per-category scores below are an internal diagnostic extension, not official journal scoring categories.

## Assessment

The revision directly addresses the user's example and the most serious issues from the first review. “Two copies” now means two specified symbol families with a block-diagonal pairing table. The paper distinguishes the ordinary Wick polynomial ring from the site quotient and gives their exact coefficient correspondence. A reader no longer has to infer whether the symbols describe photons, random variables, or auxiliary algebra.

The endpoint section is also materially easier to follow: fixed graph data are separated from variable copy parameters; the four rows have a table; the first boundary identity is derived; the insertion matrix is interpreted; and the proof says which differential identity eliminates which matrix coefficient. The scalar invariant theorem is correctly distinguished from the stronger source-specific matrix restriction.

I found **no definite new false mathematical assertion or substantive algebraic regression** introduced by the revision. The few remaining issues are localized typing, terminology, and explanatory details. The conditional nature of this statement matters: it does not amount to an independent proof audit of every coefficient calculation.

| Diagnostic criterion | Baseline | Revision 1 | Assessment |
|---|---:|---:|---|
| Conceptual clarity | 2 | 4 | The roles of copies, shifts, rows, and insertion coefficients are now explicit. |
| Notation and definitions | 1 | 4 | Most objects have their types and operations defined before substantive use. A few small residual terms remain. |
| Terminology and scope | 2 | 4 | Bilinear versus Hermitian, algebraic versus probabilistic, normalized existence, and scalar FFT scope are now distinguished accurately. |
| Organization | 3 | 4 | Named stages and new lemmas expose the proof's dependencies. Appendix A contains the appropriate coordinate detail. |
| Figures | 3 | 4 | The copy figure teaches the new construction; the graph figure illustrates the final obstruction. |
| Reproducibility presentation | 4 | 4 | Exact theorem and commands are now in a dedicated appendix. I did not execute the commands. |
| Overall presentation | 2 | 4 | A substantially stronger manuscript; the remaining requested repairs are small enough to address directly. |

## Baseline and literature requests: resolution

| Previous request | Status in revision 1 |
|---|---|
| Distinguish site quotient from Wick polynomial ring | **Resolved.** §2.4 gives both the coefficient bridge and a concrete example showing why the Wick functional is not defined on the quotient. |
| Define copies and their joint pairing | **Resolved.** §2.5 specifies the two families, zero cross-pairings, factorization, and one explicit transformed-pairing calculation. |
| Define the complex orthogonal action | **Resolved.** The acting two-dimensional space, transpose convention, lack of conjugation, and fixed graph labels are all explicit. |
| Define rows, words, coefficient arrays, and coefficient extraction | **Resolved.** §2.2 provides these definitions, and §3.1 explains the actual incident rows before the abstract lemma. |
| Define shifts, the alternating pairing, derivatives, and polarization | **Resolved.** §2.6 gives formulas and domains; §3.2 spells out coefficient extraction and the factorial. |
| Make binary projections explicit | **Resolved.** The definition of K includes projection; the odd-response and omission identities now show the relevant projections and state their scope. |
| Explain normalization as an existence equivalence | **Resolved.** Lemma 2.2 uses a nonzero endpoint rescaling, explicitly separating it from state normalization or a unitary operation. |
| Explain the purpose of the endpoint matrix | **Largely resolved.** §5.2 identifies all indices and explains the correction term by the two-root matching expansion. A small diagram would still be helpful, but is no longer necessary to identify the construction. |
| Distinguish scalar FFT from the special matrix form | **Resolved.** §5.3 explains the additional divisibility input and includes the counterexample showing that covariance alone is insufficient. |
| Precise standard-tool attribution | **Resolved.** Isserlis is cited at the actual pairing formula, polarization has the precise Kraft–Procesi location, and the contribution paragraph separates classical tools from matching-specific deductions. |
| Separate main ideas from coordinate detail | **Resolved for the normal form.** The main text states why and how the restriction works; Appendix A contains its coordinate argument and scalar invariant specialization. |

## Remaining concrete revisions

### 1. Restrict the diagonal-block statement to distinct vertices

**Anchor:** Lemma 4.2, PDF page 13.

The statement currently says “For every pair of vertices p,r” and then uses \(A_{pr}(i,h)\). The manuscript defines these coefficients only for distinct vertices; \(A_{pp}\) has not been defined. Change the opening to:

> For every pair of distinct vertices \(p,r\), the colour-indexed matrix …

Alternatively explicitly define all self-edge coefficients to be zero, but the shorter restriction is preferable. This is a small mathematical typing repair, not a substantive obstruction to the argument.

### 2. Make the support-counting sentence logically exact

**Anchor:** proof of Corollary 6.1, PDF page 18.

The text still says “every nonzero summand equals β.” The inference counts **supported edges**, so say:

> Every supported edge contributes \(\beta\) by (10), and an unsupported edge contributes zero. Thus the expansion contains \(\deg_B(p)\) copies of \(\beta\).

This removes the unnecessary implicit step that a supported edge cannot have a zero deletion amplitude.

### 3. Use the new insertion-matrix terminology in the lemma title

**Anchor:** Lemma 5.4, PDF page 16.

The surrounding text now correctly calls T the corrected insertion matrix, but the title retains “Polynomial orthogonal kernel normal form.” The undefined term “kernel” is a remnant of the old exposition. Suggested title:

> Polynomial form of the corrected insertion matrix.

Likewise replace the last “original source rows” in §2.5 with “original incident rows.” Neither change requires new mathematical definitions.

### 4. Show the one-line chain rule producing the Gram-coordinate equations

**Anchor:** proof of Theorem 5.1, §5.4, PDF page 17.

The derivation is coherent, but a physics reader still has to reconstruct how differentiation in a column component becomes differentiation in \(\rho\). Insert:

\[
\partial_{(Q_c)_1}F(\sigma,\tau,\rho)
=2(Q_c)_1\,\partial_\tau F+P_1\,\partial_\rho F.
\]

At \((Q_c)_1=0\), only the second term remains. This explains the extra \(P_1\) in the rank-one equation and the scalar equation for \(\varphi\). It is especially useful because \(\partial_\rho\) holds the other Gram coordinates fixed, whereas \(\partial_{(Q_c)_1}\) is a derivative in the original parameter ring.

This is a request to expose a valid local calculation, not a claim that the displayed equations have the wrong factors.

### 5. Explain two remaining algebra terms in place

**Anchors:** §3.2, common-factor paragraph; Appendix A, opening paragraph.

- Replace “Two independent f's are coprime” with “Two independent linear polynomials have no nonconstant common factor.” A following sentence can retain the conventional term “coprime.”
- In Appendix A, specify the initial generic set, for example the set on which the two bilinear squares, \(P\cdot Q_c\), and \(\det[P\ Q_c]\) are nonzero. If the displayed quotient is first identified pointwise, also work where \(P_1(Q_c)_2\ne0\), then use the already proved polynomial divisibility to extend it.

The appendix argument is mathematically reasonable as written, but “the required determinants” is less precise than the revised main text elsewhere.

### 6. Clarify disjointness in the multigraph-to-simple-graph transition

**Anchor:** Corollary 6.2, PDF page 18.

Before this corollary, aggregate edges of different colours may still share the same unordered vertex pair. In a literal coloured multigraph these are different edges already, so “edge-disjoint” can obscure the actual additional conclusion. State:

> No unordered vertex pair belongs to two colour matchings. Thus their union, viewed on the original vertex set, is a simple cubic graph.

The unique-contribution argument can also be stated first, since it immediately justifies the nonzero mixed coefficient used to rule out a shared pair. The current proof contains that reasoning, but its order requires a short look-ahead.

### 7. Make the initial palette type explicit

**Anchor:** §1.1, first paragraph.

Write \(\chi_u(e),\chi_v(e)\in[d]\) when introducing the endpoint colours, or explicitly say that edges using colours outside the chosen palette can first be discarded. The normalization lemma subsequently uses \(\tau_i^{-1}\), so its palette should be unambiguous. This is a scope clarification; the intended model is clear from the rest of the text.

## Mathematical coherence of the principal revisions

**Pairing domains:** the new ordinary-polynomial and site-algebra distinction is correct. The coefficient correspondence uses one factor at each retained site and therefore avoids the previously ambiguous quotient-functional interpretation. The repeated-symbol example correctly illustrates why the distinction is needed.

**Binary projection:** K is defined on the full coefficient space through an explicit binary projection. Consequently the omission proof can substitute a projected response identity inside K without asserting that omitted three-colour components vanish. This resolves the most important scope ambiguity in the original exposition.

**Normalization:** rescaling incident edges at a fixed vertex multiplies each matching contribution to a given colouring by the same nonzero factor. The construction therefore preserves vanishing, makes the pure amplitudes one, and preserves edge support. The new text correctly identifies this as an existence equivalence, not a physically unitary transformation. In the theorem's nonempty vertex setting, the construction is coherent.

**New result labels:** separating the two-root equations into Lemma 5.2 and their differentiations into Corollary 5.3 improves proof navigation. The displayed specialization proof gives the correct parameter choices and derivatives. Theorem 5.1 is stated before those tools and proved afterward in a conventional order.

**Normal form and appendix:** the matrix divisibility argument precedes the scalar invariant-theory input. Appendix A defines the plus/minus coordinates and explains Gram-coordinate independence by an explicit realization. The matrix statement continues to depend on the matching-specific vanishing identities, and the revised attribution now makes this visible. I found no new mismatch between the main statement and appendix proof.

## Visual review

**Figure 1, page 3:** The added matching lists and signed products now show exactly what cancels. Both panels remain legible, and the caption distinguishes weights from endpoint colours. The diagram still communicates through geometric edge classes if its colours are not discernible.

**Figure 2, page 8:** This is the most useful new figure. The two symbol families, unchanged internal table, zero cross-pairings, and common transformation are all visible. The caption explicitly states that the arrow is a formal substitution. I saw no clipping, overlaps, or misleading graph-edge depiction. The figure now answers the user's question about “copies” alongside the formal definition.

**Figure 3, page 19:** The selected edges form perfect matchings in both panels. Dashed H edges and heavy cycle edges are distinguished by line style as well as colour; the crossing is not drawn as a vertex. The caption correctly describes these as proof configurations rather than GHZ examples.

**Algebra pages:** Pages 14–17 are dense but much easier to navigate than the baseline. The fixed-row table is helpful. The normal-form proof sketch is separated from its coordinate proof, and the two coefficient deductions have visible signposts. No visibly clipped formulas were found in the inspected pages. One remaining typographical improvement is to display the formula for \(L_i\) in §5.2 on its own line rather than embed it inside a long paragraph. A direct-edge-versus-two-attachments diagram in §5.1 would be a useful optional addition; its absence is not a blocker now that the first boundary identity is explained.

## Conclusion for this review pass

The revision fulfills the substantive algebraic definition and attribution requests. The original objection—having to guess what “two copies” means—is resolved through both definitions and a usable figure. The remaining items above are concrete local edits. After those changes, the presentation would be ready for substantive review by an external specialist; this internal rereview does not replace that mathematical assessment.
