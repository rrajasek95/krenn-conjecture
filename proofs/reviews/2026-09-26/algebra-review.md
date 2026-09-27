# Internal referee report: algebra, mathematical physics, and notation

**Recommendation on the reviewed version: major revision (Quantum's “Revise and resubmit”). Overall presentation rating: 2/5.**

This is an internal, simulated referee report commissioned to improve the manuscript, not external peer review, acceptance, or an independent certification of its principal theorem. It reviews `reviewed-baseline.tex` and the corresponding 15-page `reviewed-baseline.pdf` saved on September 26, 2026. Section, equation, page, and source-line references below refer to that baseline, not subsequent revisions.

The review follows the questions in [Quantum's referee form](https://quantum-journal.org/instructions/referees/): summary and significance, extent of technical checking, presentation and assumptions, reproducibility, and specific revisions. Quantum requests an overall 1–5 rating and an editorial recommendation. The category scores below are our **diagnostic extension**, not official journal scoring categories. The report also follows [APS guidance on structuring a referee report](https://journals.aps.org/structuring-report), particularly its emphasis on substantiated technical concerns, logical flow, and the information value of figures.

## Assessment and checking performed

The manuscript proposes a strong structural route to the Krenn–Gu conjecture: arbitrary aggregate endpoint-colour weights become diagonal; every supported monochromatic edge accounts for the entire monochromatic matching amplitude; each active colour therefore forms a perfect matching; the remaining graph obstruction gives a mixed contribution that cannot cancel. The introduction now explains the cancellation obstacle and the degree-one endgame effectively. If the full stated argument is correct, its claimed scope would be highly significant.

I read the full source, with close checking of Sections 2–7. I checked the types and meaning of the objects, the local coefficient/pairing correspondences, the advertised uses of parity and nonzero amplitudes, the support-counting argument, and the logic of the graph conclusion. I rendered and visually inspected PDF pages **3, 6, 7, 9, 10, 11, 12, and 13**, including both panels of Figure 1 and the dense algebraic pages. I did not independently rerun the Lean build or reconstruct every coefficient identity from the formal development. This report therefore does not upgrade the mathematical verification status claimed by the authors.

The main obstacle to publication as presented is not the size of the machinery. It is that the manuscript repeatedly uses a construction before specifying its objects and operations. A reader cannot tell whether a “row” is a matrix row or a polynomial, whether a “copy” is another graph or a family of formal generators, or whether a “mean” is an expectation or an auxiliary scalar shift. These ambiguities occur at the interfaces carrying the argument, not just in peripheral terminology.

| Diagnostic criterion | Score, 1 poor–5 excellent | Reason |
|---|---:|---|
| Conceptual clarity | 2 | Excellent cancellation/endgame overview; several central algebraic transitions remain implicit. |
| Notation and definitions | 1 | Rows, words, tensors, copy indices, pairing domains, derivatives, and group actions require reconstruction. |
| Terminology and scope | 2 | “Independent,” “covariance,” “mean,” “source,” and “kernel” borrow different meanings without sufficient local definitions. |
| Organization | 3 | The large-scale proof order is sensible; two long technical arguments lack intermediate signposts and division of labour. |
| Figures | 3 | Figure 1 is clean and correct; it does not yet visualize any of the unfamiliar machinery. |
| Reproducibility presentation | 4 | Exact theorem, pinned artifacts, and normalization scope are identified; the written-to-formal map is still difficult to navigate. Build not rerun in this review. |
| Overall presentation | 2 | Major exposition revisions should make the work assessable by the intended mathematical-physics audience. |

## Priority 1: define the mathematical objects at their first use

### A1. Separate the site algebra from the ordinary polynomial ring of Wick symbols

**Anchors:** §2.1, baseline lines 273–318; §2.3, lines 337–357; §3 proof, page 7.

The quotient algebra enforces that a site is used once. The later Wick symbols do not satisfy those quotient relations. This distinction must be explicit: the Wick functional generally **does not descend to the site quotient**. For example, with two symbols having zero self-pairings and cross-pairing \(c_{uv}\),

\[
\mathcal W(X_u^2X_v^2)=2c_{uv}^2,
\]

whereas the corresponding monomial vanishes in the site algebra. The argument uses matching coefficients with one chosen coordinate at each site, where the two constructions agree; it must not suggest a linear functional on the quotient itself.

Suggested definition text:

> For any subset \(S\subseteq V\), let \(\mathcal A_S\) be the same site algebra restricted to vertices in \(S\). A colour word is a function \(\kappa:S\to\{a,b,c\}\); its monomial is \(x^\kappa=\prod_{v\in S}x_{v,\kappa(v)}\). Write \([\kappa]F\) for the coefficient of this monomial in \(F\). The subspace spanned by all such monomials is denoted \(\mathcal T_S\). Thus an element of \(\mathcal T_S\) is an array with one coefficient for each vertex colouring. We call it a tensor only in this sense.

Then, before formal Wick moments:

> The following symbols belong to an ordinary commutative polynomial ring, not to the site quotient. Pairing sums on these symbols will calculate coefficients of elements of \(\mathcal T_S\).

This is a **mathematical typing concern**, not evidence that a claimed identity is false. Resolving it is necessary for an unambiguous exposition.

### A2. Define a copy by its generators and pairing table

**Anchors:** §2.4, lines 361–392, PDF page 6; §3, “two independent identical replicas,” page 7.

The user's quoted sentence is exactly where the text stops being self-contained. “Take two copies” does not identify what is copied. The index \(i\) also silently changes from an arbitrary symbol label to a vertex label, and then \(X_{i,h}\) acquires a second index.

Suggested replacement:

> Let \(\Lambda\) be the label set for the symbols; for a coloured graph a label is a pair \(\lambda=(v,h)\) consisting of a vertex and a colour. Introduce two disjoint families of commuting symbols, \(X_\lambda\) and \(Y_\lambda\). Equip their span with the symmetric bilinear pairing \(C\) specified by
> \[
> C(X_\lambda,X_\mu)=C(Y_\lambda,Y_\mu)=c_{\lambda\mu},
> \qquad C(X_\lambda,Y_\mu)=0.
> \]
> These two families are called copies because they have the same internal pairing coefficients. They are auxiliary algebraic symbols; no additional physical graph or random sampling is involved. A pairing term connecting different families has weight zero. Consequently \(\mathcal W(F(X)G(Y))=\mathcal W(F(X))\mathcal W(G(Y))\).

The factorization is the exact property later needed from “independence.” Prefer “uncoupled formal copies” or just “copies with zero cross-pairings” to “independent replicas.” If “independent” is retained, explicitly declare that it means this pairing-factorization property here.

Show one covariance calculation after the displayed 45-degree transformation. Define

\[
\mathrm O(2,\mathbb C)=\{O\in\mathbb C^{2\times2}:O^TO=I_2\},
\qquad \mathrm{SO}(2,\mathbb C)=\{O\in\mathrm O(2,\mathbb C):\det O=1\}.
\]

The transpose and pairing are **bilinear, with no complex conjugation**. This is essential for physics readers accustomed to unitary transformations and Hermitian covariance matrices. State that \(O\) acts on the two-dimensional copy index and simultaneously on every symbol label, including the auxiliary symbols \(g_1,g_2\) in §3.

### A3. Define a row, a response, and the root decomposition before Lemma 3.1

**Anchors:** §3 heading and Lemma 3.1, lines 394–416, PDF pages 6–7; the paragraph following its proof, lines 499–502.

Suggested definitions:

> A row on \(S\) is a degree-one element
> \[
> L=\sum_{v\in S}\sum_{h\in\{a,b,c\}}L_v(h)x_{v,h}\in(\mathcal A_S)_1.
> \]
> Its coefficients specify the possible connections from one omitted root to the retained vertices. If a root \(p\) is removed from the edge polynomial, there is a unique decomposition
> \[
> A=R+\sum_h x_{p,h}L_h^{(p)},\qquad
> L_h^{(p)}=\sum_{v\ne p}\sum_k A_{pv}(h,k)x_{v,k}.
> \]
> Here \(R\) contains only edges with both endpoints different from \(p\). The response \(LR^{[m]}\) records all matching contributions that use one root connection from \(L\) and match the remaining vertices through \(R\).

Then let \(D\) be a linear subspace of \((\mathcal A_\Omega)_1\), explicitly over \(\mathbb C\). The functions \(f_h:D\to\mathbb C\) in (2) are linear coefficient maps. Define \(\mathbb C[D]\) as the polynomial ring in the coordinates of a row in any basis of the finite-dimensional space \(D\). “Independent” means linearly independent functions, not stochastic independence.

Move the actual-root application to *before* the abstract lemma or announce it before the lemma and prove it immediately afterward. Otherwise readers cannot see why the strong pure-response hypothesis (2) is available.

Define “higher response”: \(H_p(L)\) chooses \(p\) row factors and pairs the other vertices using \(R\). Clarify that these are algebraic bookkeeping expressions; they do not represent \(p\) physical photons emitted from one original root. State the range as “for every odd \(p\) with \(3\le p\le2m+1\).”

### A4. Give the alternating pairing explicitly and identify its domain

**Anchors:** §3 last paragraph of page 7, lines 478–491; §4 proof, page 8; §5, page 10.

“The product of local alternating pairings” is not a definition for the intended audience. Introduce a fixed binary palette \(\{a,b\}\), its projection \(\pi_{ab}:\mathcal T_S\to\mathcal T_S^{ab}\), and

\[
\varepsilon(a,b)=1,\quad\varepsilon(b,a)=-1,\quad
\varepsilon(a,a)=\varepsilon(b,b)=0,
\]
\[
K_S(x^\kappa,x^\lambda)
=\prod_{v\in S}\varepsilon(\kappa(v),\lambda(v)),
\]

extended bilinearly. Thus

\[
K_S(F,G)=\sum_{\kappa:S\to\{a,b\}}
(-1)^{|\kappa^{-1}(b)|}[\kappa]F[\bar\kappa]G,
\]

where \(\bar\kappa\) exchanges the two colours. This immediately explains the parity rule \(K_S(G,F)=(-1)^{|S|}K_S(F,G)\), coefficient extraction against a pure word, and the determinant in §3. There is no complex conjugation here either.

Avoid leaving “all binary projections implicit” throughout an entire proof. State once that the arguments of \(K_S\) are projected by definition, or show the projection in the first substantial identity. The unprojected tensor may still have three-colour coefficients; an equality valid after projection must not appear to assert equality of the full tensors.

### A5. Define shifts (“means”) and directional derivatives with one coefficient identity

**Anchors:** §3 “Wick moments with shifted variables \(X_i+L_i\),” pages 7–8; §4 \(E_{V_h}\), page 8; §5 derivatives in (7)–(8).

The index-free shift \(X_i+L_i\) adds things of unspecified types. The following unifying identity supplies the missing bridge. For a quadratic \(R\) on \(S\), define

\[
\mathcal F_{S,R}(L)
=\sum_{j=0}^{\lfloor|S|/2\rfloor}
\frac{L^{|S|-2j}}{(|S|-2j)!}R^{[j]}.
\]

For a word \(\kappa\),

\[
[\kappa]\mathcal F_{S,R}(L)
=\mathcal W_R\left(\prod_{v\in S}
\bigl(Z_{v,\kappa(v)}+L_v(\kappa(v))\bigr)\right).
\]

Explain in words: choose which factors supply scalar shifts; pair the others. The factorials on the left precisely remove the ordering of the chosen row factors and pairs. The odd case is \(\Psi\); the even case is \(E\). A “mean” in this paper is just the scalar shift vector \((L_v(h))\), not a probabilistic expectation. “Shift row” is a less loaded default term.

At the first derivative, write

\[
E_V(U)=\left.\frac{d}{dt}E(U+tV)\right|_{t=0},
\qquad
E_{VW}(U)=\left.\frac{\partial^2}{\partial s\partial t}
E(U+sV+tW)\right|_{s=t=0}.
\]

These are derivatives of a finite polynomial map between complex vector spaces, with \(Q\) fixed. They do not differentiate the original edge weights. Define polarization by substituting \(L=\sum_jt_jL_j\) and taking the coefficient of \(\prod_jt_j\); division by the resulting nonzero factorial is permitted over \(\mathbb C\).

## Priority 2: make the technical sections navigable

### A6. Split Lemma 3.1 into visible subarguments

**Anchors:** entire §3, especially (3) and the transition to \(g(L/\sqrt2)^2=g(L)\).

The proof currently hides five separate ideas in continuous prose: pairing representation; odd reflection; common pure factor and mixed-coefficient vanishing; even determinant-preserving rotation; finite-degree rigidity. Use short internal headings or separate lemmas. The reader should know what survives after each step:

1. Reflection relates every pure response coefficient to a common polynomial factor and kills mixed binary coefficients.
2. Consequently the binary projection has exactly two pure terms multiplied by \(g(L)\).
3. The second copy symmetry forces the functional equation for \(g\).
4. Finite degree forces \(g=1\), which removes every positive higher response.

Name the arbitrary-row extension as a final polarization step. Define “terminal response” as the largest allowed row degree, where no \(R\) factor remains. Define “isotropic” if used: \(s^2+t^2=0\). Explain that an identity between polynomials proved on the nonvanishing-denominator set extends to all parameter values.

There is a useful normalization detail worth stating: extracting \(s^pt\) from the displayed moment first produces a nonzero scalar binomial factor \(p+1\); removing it gives (3). There is no apparent contradiction here, but writing the factor once helps readers audit the combinatorics.

### A7. Introduce omission as coefficient extraction, then connect it to the matrix identity

**Anchors:** §4, (4)–(6), PDF pages 8–9.

The decomposition should say exactly what its terms mean: \(Q\) is \(R\) restricted to the vertices other than \(q\); \(V_h\) is the row at the omitted vertex in colour \(h\); \(U(L)\) is the restriction of \(L\) to the retained vertices; \(d_h(L)\) is its scalar coefficient at \(q,h\). This also prevents readers mistaking \(U\) for an independent variable unrelated to \(L\).

In the proof choose \(h\ne k\) explicitly. Then the binary-projection statement follows from the already stated support of \(\Psi\), including why the pure \(k^\Omega\) term vanishes when extracting \(q=h\).

Before Lemma 4.2, explain that \(C_h[r,q]\) is a **deletion matching amplitude**, often called a hafnian cofactor; it is not initially known to be an adjugate or inverse. State that the matrices have rows and columns indexed by \(V\). Define \(A_{vu}(j,i)=A_{uv}(i,j)\) to extend the originally ordered-edge notation, and define the Kronecker delta if used.

Replace “one-defect word at \(p\)” by “the colouring assigning \(i\) to \(p\) and \(h\) to every other vertex.” Before (6), state the goal: show that the off-diagonal entries of \(B_{ih}C_h\) vanish. After (6), the existing inverse argument is short and effective.

### A8. Reorganize §5 around the purpose of each construction

**Anchors:** §5, lines 613–803, PDF pages 10–12.

Start with a one-paragraph plan: four rooted identities constrain a matrix of two-copy insertion coefficients; orthogonal symmetry restricts its form; a derivative identity removes its rank-one part; a second derivative identity determines its scalar part; evaluating at zero yields the edge subtotal. This is the hardest part of the proof and needs this roadmap.

Make \(B,H\) explicitly the two symmetric zero-diagonal weight matrices, with the corresponding site variables \(b_i,h_i\). Replace “literal binary quadratic” by the actual definition

\[
Q=\sum_{i<j,\ i,j\in U}(B_{ij}b_ib_j+H_{ij}h_ih_j).
\]

Group the notation by role: retained vertices; two fixed edge weights; full/deleted amplitudes; four fixed rows; auxiliary scalar parameters. State \(d\ne0\), \(\beta\ne0\), and \(\eta\ne0\) explicitly; \(e\) may vanish. The theorem itself should repeat its source and diagonalization hypotheses rather than relying entirely on the preceding paragraph.

Derive the first identity of (7) once. At root \(p\), the chosen two-colour row is

\[
s(db_q+x)+t(eh_q+u).
\]

Extract its \(b_q\) coefficient after applying the higher-response result. The direct \(pq\) edge produces \(dsE(sx+tu)\), while a connection from \(q\) into \(U\) produces \(E_y(sx+tu)\). Their sum is \(s\beta b^U\). The remaining three identities follow by exchanging roots or colours. This one calculation explains what (7) means far better than calling the identities “exact.”

Keep the newly added explanation of \(T=M+efI\): it is valuable. But introduce the columns \(P,Q_c,R_c,S_c\) as **eight independent scalar indeterminates grouped in pairs**, and say that their components index copies 1 and 2. Otherwise “independent columns in \(\mathbb C^2\)” can be misread as linearly independent columns, which cannot apply simultaneously to four columns and conflicts with later specialization to zero.

“Kernel matrix” should be defined or replaced by “matrix of insertion coefficients.” It is neither the nullspace of a map nor an analytic integral kernel. Invariance of scalar \(G\) and covariance of matrix \(M\) are different transformation laws; show them separately.

### A9. Reduce symbol collisions and explain the normal form

**Anchors:** §5 (7)–(9), Lemma 5.2, pages 10–11.

Current collisions impose unnecessary memory costs:

| Symbol | Baseline meanings | Recommended change |
|---|---|---|
| \(b\) | colour, site variable prefix, scalar parameter in (7), scalar coefficient in (9) | Keep colour \(b\); use \(r,t\) for scalar parameters and \(\mathfrak a,\mathfrak b\) or \(A_0,B_0\) for normal-form coefficients. |
| \(g\) | auxiliary Wick generator and common scalar polynomial \(g(L)\) | Use \(\zeta\) for the generator. |
| \(R\) | a quadratic and the coefficient domain of Lemma 5.3 | Use \(\mathscr R\) for the abstract coefficient domain. |
| \(Q\), \(Q_c\) | retained quadratic and copy-parameter column | Give the retained quadratic a subscript, or choose clearly distinct column labels. |
| \(c\) | third colour and a Gram coordinate | Use \(\rho=P\cdot Q_c\) for the Gram coordinate. |
| \(U\) | restricted row in §4 and retained vertex set in §5 | Use \(S\) for the retained set consistently. |

Define \(P\cdot Q_c=P_1(Q_c)_1+P_2(Q_c)_2\), \(I_2\), transpose, and the three Gram coordinates. A complex “orthonormal frame” refers to this bilinear form, not a Hermitian inner product. “Nonisotropic” means \(P\cdot P\ne0\).

Explain in words what (9) achieves: a matrix whose entries initially depend on four parameters has only a scalar-identity part and one rank-one part; their scalar coefficients depend on just the three pairing invariants. Then explain which derivative identity kills which part. Define \(a_c\) and \(b_c\) as partial derivatives, preferably using \(\partial_\rho\) after renaming.

The generic frame argument and elementary invariant-ring calculation are reasonable appendix material **after** the statement and its purpose are clear in the main text. Define \(q_\pm\), which are currently only named. “Weights \(+1,-1\)” means that a parameter \(z\in\mathbb C^\times\) scales the corresponding coordinates by \(z\) and \(z^{-1}\); say this if the invariant-ring proof remains in the main paper. “Polynomial normal form” should be described as an identity valid also at degenerate parameter values, not a choice of basis or diagonalization of the original graph.

### A10. Sharpen the final sections without inflating them

**Anchors:** §§6–8, PDF pages 12–14.

In Corollary 6.1 write “every **supported edge's** summand equals \(\beta\)” rather than “every nonzero summand,” since the theorem excludes a supported edge with a zero deletion amplitude. The intended inference is sound but can be made direct.

Replace “receiving colour word” with “prescribed vertex colouring.” Define the colour graph as the graph of nonzero aggregate weights for one colour. In Lemma 7.1, say “pairwise edge-disjoint,” since the matchings necessarily share all vertices. “Mixed” in this lemma means using edges from at least two of \(F,G,H\). The graph proof is concise and understandable once these terms are stated.

The formalization discussion usefully separates exact normalized scope from prose translations. Retain this. Move most internal research-note provenance out of the main argument; it currently interrupts §§3–5 before readers have learned what their results mean. Put a compact theorem-to-Lean-module table and exact reproduction commands in an appendix or artifact documentation. Do not use internal audit citations as proxies for missing exposition.

## Figures and typography: findings from visual inspection

**Figure 1, PDF page 3:** Both panels render cleanly; there are no missing labels or visible crossings mistaken for vertices. The split colouring of the vertical edges in (a) and the caption's explicit warning about the diagonal crossing in (b) are useful. The figure shows the correct graph configurations.

Its explanatory burden can still be improved. Add the two matchings from panel (a), for example \(M_+=\{12,34\}\) and \(M_-=\{13,24\}\), with their products \(+1\) and \(-1\). A small legend should distinguish endpoint colours from complex weights, since node-adjacent labels such as \(1:a\) otherwise look like an input vertex colouring rather than a colouring inherited by both matchings. The caption should explicitly say that the inherited colouring is the same for the two matchings. Maintain geometric distinctions or edge labels so the figure remains readable without colour.

**Missing conceptual figure:** The only figure explains the classical starting point. Add a two-copy schematic in §2.4: two columns of formal symbols, identical internal pairing coefficients, zero cross-pairings, and a small \(2\times2\) transformation acting on each row. Caption it as an algebraic construction. Do not draw it in a way that suggests a physically realizable duplicated experiment is being asserted.

**Useful second technical figure:** At the start of §5, show the two ways the roots contribute: direct edge \(pq\), and separate attachments from \(p,q\) into the retained vertex set. Label these \(eE\) and \(E_{uv}\). This explains the correction term before the four-column derivative notation appears.

**Optional graph figure:** A small cycle with an even-even and odd-odd interlacing chord would substantially reduce the verbal load in §7. Show the four residual even paths and why \(n>4\) leaves a cycle edge in the resulting matching. The \(n=4\) exception can be indicated in the caption.

**Equation typography:** The PDF is legible; I found no visibly clipped equations on the inspected pages. Nevertheless page 10 is especially dense: its opening notation block, four boundary identities, derivative consequences, two-copy columns, and matrix definition appear with almost no explanatory pause. Divide that material into subsections. The long inline definition of \(L_i\) should be displayed, with \(i\in\{1,2\}\) written explicitly. Page 9's cofactor display is already near the text width and would benefit from a preceding sentence naming its two summed edges. Page 11 packs the generic-frame proof, invariant theory, and polynomial-ODE lemma together; moving bookkeeping to an appendix is preferable to reducing font size.

## Suggested revised organization

1. Keep the current cancellation example and three-step graph-level overview.
2. In §2 define site coefficients, root rows, the ordinary Wick polynomial ring, copies, and shifts; include the copy schematic and one worked coefficient identity.
3. Present the odd-response lemma through three named stages: reflection, common factor, finite-degree rigidity. All hypotheses and the actual-root application must remain in the main text.
4. Explain omission as extraction at a second root, then present the cofactor matrix argument.
5. Give a one-paragraph endpoint roadmap, the direct-versus-attached-roots diagram, one derived boundary identity, the insertion matrix, the normal-form statement, and the two short degree arguments.
6. Put the general coefficient-extraction details, polarization bookkeeping, generic-to-polynomial extension, and invariant-ring proof in appendices with precise references from the main argument.
7. Keep the matching-rigidity and graph conclusions short. Close with an exact formalization statement and reproducibility pointer.

The main paper must still explain every new mechanism. Definitions, the meaning of the auxiliary objects, and the connection between two-copy symmetry and the supported-edge identity should not be relegated to an appendix.

## Mathematical concerns versus exposition concerns

- **No explicit counterexample or definite false theorem was found in this review.** I have not performed a full independent mathematical certification.
- The distinction between the site quotient and Wick polynomial ring is a genuine typing requirement. The manuscript must state the coefficient bridge rather than imply an ill-defined functional on the quotient.
- Binary projection must be made explicit wherever equalities discard possible three-colour coefficients.
- Nonzero amplitudes, supported-edge hypotheses, parity, and the use of a characteristic-zero polynomial domain should be visible at the points where cancellation and degree arguments rely on them.
- The other issues above are clarity, organization, or notation repairs. They should not be reported as discoveries of proof gaps merely because the baseline exposition makes them difficult to check.

## Concrete acceptance criteria for a revised presentation

A reader should be able to answer, without consulting repository notes: what the symbols in a copy are; which ring they live in; what a row encodes; how a tensor coefficient equals a Wick pairing sum; which two-dimensional space \(\mathrm O(2,\mathbb C)\) acts on; why the original graph is unchanged; what the insertion matrix measures; and how its two scalar coefficients yield the supported-edge identity. The revised figures should directly help answer at least two of those questions.
