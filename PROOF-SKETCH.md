# A descent program for the Krenn–Gu conjecture

*Proof-architecture companion to the [README](README.md). Statements
are labelled **[P]** proved (exact checker and independent audit),
**[G]** generation-side (checker-backed, awaiting independent
re-audit), or **[O]** open. Full statements and certificates are in the
linked repository notes. Last synchronized: 2026-08-13.*

## 1. Introduction

Krenn, Gu, and Zeilinger [1] observed that a large class of
linear-optical experiments is faithfully encoded by edge-weighted
graphs: vertices are photon paths, an edge $uv$ is a photon-pair
source, and an $n$-photon coincidence event corresponds to a perfect
matching of $K_n$. The prepared state is the coherent superposition of
all perfect matchings, weighted multiplicatively by the edge
amplitudes. Which Greenberger–Horne–Zeilinger states are reachable in
this scheme is governed by a conjecture of Krenn and Gu ([2]; see also
[3]), which we treat in its strongest form, allowing complex
amplitudes that depend on both endpoint colours.

Let $n$ be even and $d \ge 2$. A *bicoloured weighting* of $K_n$ in
$d$ colours assigns to each edge $uv$ and each ordered colour pair
$(i,j) \in \{0,\dots,d-1\}^2$ a complex weight $w_{uv}(i,j)$; this
subsumes multigraphs, since parallel edges aggregate into a single
weight. A perfect matching $M$, with one colour pair chosen per edge,
*induces* the vertex colouring $c$ that assigns each vertex the colour
it receives from its matching edge; the amplitude of the pair $(M,c)$
is $w(M,c) = \prod_{uv \in M} w_{uv}\bigl(c(u), c(v)\bigr)$. For a
vertex colouring $c \colon V \to \{0,\dots,d-1\}$ set

$$\Phi(c) \;=\; \sum_{M \in \mathcal{M}(K_n)} w(M,c).$$

The weighting is a **GHZ weighting of dimension** $d$ if

$$\Phi(c) = \begin{cases} 1, & c \text{ constant},\\[2pt] 0, & c \text{ non-constant.}\end{cases} \tag{1}$$

**Conjecture (Krenn–Gu).** For even $n \ge 6$ and $d \ge 3$, no
bicoloured complex weighting of $K_n$ satisfies $(1)$.

In the notation of [1, 2], the conjecture asserts $k_{\max}(n) = 2$
for even $n \ge 6$, while $k_{\max}(4) = 3$ via the known exceptional
weighting of $K_4$.

The known partial results frame the difficulty. For weightings whose
matchings are forced to interfere constructively — in particular
nonnegative real weights — the conjecture follows from Bogdanov's
theorem [4] that a graph on at least six vertices in which every
perfect matching is monochromatic admits at most two colours on its
edge set (equivalently: three pairwise edge-disjoint perfect matchings
of $K_n$, $n \ge 6$, always admit a further perfect matching inside
their union). Chandran and Gajjala [3] developed the graph-theoretic
framework for the weighted problem, and with Illickan [5] proved the
conjecture for all experiment graphs of vertex connectivity at most
$2$, and unconditionally for maximum degree at most $3$ — the latter
already for complex weights and bicoloured multigraphs. In the
opposite regime of many colours, the automated formal-proof system of
[6] certified the diagonal cases $n = d \in \{4, 6, 10\}$ together
with an explicit certificate family for $d = n$ at every even $n$, and
further instances with $d > n$; a solver-free argument over arbitrary
integral domains [12] yields the general bound $k_{\max}(n) \le n-2$.
A tensor-algebraic no-go theorem by Krenn, Firsching, Tsoukalas,
Gajjala, Gu, and Chaudhuri is announced as in preparation in [6]. The
smallest case left open by all of the above — here and in the
`formal-conjectures` registry [7] — is $n = 8$, $d = 3$.

Restricting $(1)$ to any three colours shows that it suffices to treat
$d = 3$ **[P]**. Throughout, a *word* is a vertex colouring
$c \in \{0,1,2\}^n$, and we write $\Phi_c$ for $\Phi(c)$.

This document records the architecture of a proof by induction on
$n$: its proved components, the method, and the single open statement
(Section 6) to which the program has reduced the conjecture.

## 2. Interference, gauge freedom, and sign obstructions

**Forced interference.** By Bogdanov's theorem [4], any weighting
satisfying the three monochromatic equations of $(1)$ carries
nonvanishing mixed terms: the three families of monochromatic
matchings force further perfect matchings whose induced colourings are
non-constant, so the mixed equations can never hold term by term
**[P]**. A putative GHZ weighting is therefore an exact
destructive-interference pattern among forced terms, and the program
is a theory of the obstructions to such patterns. Genuinely analytic
approaches are unavailable for a structural reason: the GHZ tensor
$\Delta = \sum_c e_c^{\otimes n}$ lies in the *closure* of the set of
matching tensors **[P]**, so no argument by dimension count, flattening
rank, or Zariski-closed condition can separate it — consistent with
the numerical observation that approach to $\Delta$ requires
amplitudes diverging polynomially in the inverse residual.

**Gauge action.** The torus $(\mathbb{C}^\times)^{n \times 3}$ acts by
$w_{uv}(i,j) \mapsto b_{u,i}\, b_{v,j}\, w_{uv}(i,j)$, rescaling all
terms of a fixed word equally, so it permutes solutions of $(1)$ up to
normalization. The gauge-invariant data of a *support* $S$ (a set of
cells $(uv, i, j)$ permitted to be nonzero) is carried by the lattice

$$L_S = \ker\bigl(\mathbb{Z}^S \to \mathbb{Z}^{V \times 3}\bigr)$$

of the unsigned cell–incidence map. In Zaslavsky's theory of signed
graphs [8], $L_S$ is the lattice of the frame (even-cycle) matroid of
the *cell graph* of $S$: its circuits are the balanced (even) closed
walks together with pairs of unbalanced (odd) cycles joined by a path.
The odd-handcuff circuits exist precisely because the cell graph is
non-bipartite, and they carry the sign phenomena below. For the full
ternary support at $n = 8$ the lattice has rank $228$ **[P]**.

**Sign obstructions.** When a mixed word $c$ retains exactly two terms
$(M, c)$ and $(M', c)$, the equation $\Phi_c = 0$ forces
$w(M,c) = -\,w(M',c)$. Recording the exponent vector
$\delta_{M,M'} = \mathbf{1}_{(M,c)} - \mathbf{1}_{(M',c)} \in
\mathbb{Z}^S$ together with the sign $-1$, and accumulating over all
two-term fibres, produces a homomorphism $\varepsilon \colon L' \to
\{\pm 1\}$ on a sublattice $L' \le L_S$ — a *partial character* in the
sense of Eisenbud and Sturmfels [9], who showed that such characters
on lattices govern the primary structure of binomial ideals; here the
character is enriched by a sign, as in the parity binomial edge ideals
of Kahle, Sarmiento, and Windisch [10], where the same
even/odd-walk dichotomy controls the primary decomposition. Two
mechanisms refute a support outright:

- **(O1)** *odd holonomy*: integers $\lambda_1, \dots, \lambda_k$ with
  $\sum_k \lambda_k \delta_k = 0$ in $\mathbb{Z}^S$ and $\sum_k
  \lambda_k$ odd; multiplying the forced relations yields
  $1 = (-1)^{\sum\lambda_k} = -1$;
- **(O2)** *singleton fibre*: a mixed word retaining exactly one term,
  whose nonzero amplitude cannot vanish.

Across the certified censuses — the six-site classification of
Section 3, the $n = 8$ chart censuses ($11{,}578$ supports), and
cross-validation against an independent research program — these two
mechanisms, together with a finite list of ordinary integral
certificates, account for every refuted support **[P]**. Both are
sharp: there are supports with identical unsigned data refuted by (O1)
and (O2) respectively, so the sign enrichment is essential; and there
is an explicit satisfiable $8$-vertex configuration carrying an odd
cycle of holonomy $-1$ whose relation vectors are linearly
independent — without a lattice dependency, odd holonomy is a value,
not a contradiction **[P]**.

## 3. Descent and the base case

**Theorem A (six-site obstruction) [P].** No bicoloured complex
weighting of $K_6$ satisfies the ternary system $(1)$.

The proof stratifies the $3 \times 3$ endpoint data into $19$
rank/defect types and refutes each stratum by exact certificates over
the $15$ matchings and $3^6$ words
(`proofs/six-site-arbitrary-complex-obstruction.md`); it has been
independently re-audited. It is corroborated by a concurrent and
independent Lean 4 certificate of its normalized fiber [11], obtained
by a different decomposition (support orbits rather than rank strata);
the solver-free full-column anchor lemma of [12] subsumes the
forced-incidence step used by both developments.

**Theorem B (clean-pair descent) [P].** Call adjacent sites $u, v$ an
**active clean pair** if the two $3 \times 3$ overlap caps at $uv$ — the
arrays of anchored matching sums seen from $u$ and from $v$ — both
have rank $3$. Contracting $u, v$ through $w_{uv}$ then yields a
bicoloured weighting of $K_{n-2}$ satisfying the same system $(1)$.

Iterating Theorem B from a minimal counterexample terminates at
Theorem A, so the conjecture reduces to:

**(Clean-pair existence) [O; reduced in §6].** Every minimal
counterexample, normalized to maximal protected anchors and then
minimal support, admits an active clean pair — or is refuted directly
by the mechanisms of Section 2.

**The local funnel [P]/[G].** At a normalized minimal counterexample
the support geometry divides as follows. All-axis branches are empty:
exhaustive specialization censuses through three simultaneous cells
($1{,}020$, $57{,}291$, and $2{,}126{,}208$ cases) reduce every branch
to a unit, and multiaffinity of the cubic system bounds the stratum
depth **[P]**. Off-axis support forces an *active fan*: whenever a
vanishing mixed word has a nonzero balanced-cut determinant it has a
nonzero off-diagonal cell — proved exhaustively over all $3^{15}$ sign
patterns of the six-site window **[P]** — and the resulting fan
produces a clean pair unless an edge is a pure-colour coloop. Coloop
recurrences terminate: the $5{,}141$ cross-intersecting six-site
configurations close into $446$ saturated concepts falling into six
symmetry types **[P]**, each of which is routed. A single branch
survives; Section 6 identifies its obstruction class exactly.

## 4. Certificates as constrained homotopies

Fix a word $c$ and regard the terms of $\Phi_c$ as *occurrences*
$(M, c)$. For an $M$-alternating cycle $C$, the exchange $M \mapsto
M \mathbin{\triangle} C$ relates occurrences sharing their off-cycle
factor, with amplitude ratio

$$\frac{w(M \mathbin{\triangle} C,\, c)}{w(M, c)} \;=\; \prod_{e \in C \setminus M} w_e(c) \Big/ \prod_{e \in C \cap M} w_e(c),$$

an explicit Laurent monomial in the cells. Exchanges connect the
matchings of $K_{2m}$ — the two-switch exchange graph is in fact
Hamilton-connected [13] — and every certificate produced by this
program, in particular every (O1) refutation, is a chain of exchange
binomials with tracked coefficients.

Homologically, the vanishing of all mixed coefficients is the
vanishing of an augmentation, and its consequences are organized by
contracting the occurrence complex. The decisive subtlety is that the
*unconstrained* contraction exists and proves nothing: under the
normalization $\Phi_{c^n} = 1$ the full matching complex is explicitly
contractible **[P]**. A certificate arises only from a contraction
whose every map is *equation-derived and label-preserving* — word,
fine multidegree, repeated-site grade, and provenance are all tracked.
This constrained transfer problem has antecedents in two literatures:
in rewriting theory, where Squier's finiteness theory and the
polygraphic resolutions of Guiraud and Malbos build contracting
homotopies literally from the defining relations, with the gap between
relation-derived and abstract homological data measured by exact
sequences of Pride–Guba–Sapir type, recently extended to associative
algebras by Steinberg [14, 15]; and in combinatorial infeasibility,
where the linear-algebra Nullstellensatz certificates of De Loera,
Lee, Malkin, and Margulies [16] are precisely degree-bounded
nullhomotopies of a Koszul complex. Equivariant resolutions of
permanent-type ideals, the closest commutative-algebra relatives of
the matching system, appear in [17].

The program's *fencing theorems* **[P]** make the necessity of the
constraint exact, through one mechanism applied uniformly: the
residual class of Section 6 is antisymmetric under a chart involution,
whereas every matching-side operation — Koszul resolutions, diagonal
all-matching contractions, group averaging, all bipartition
flattenings imposed simultaneously (each unordered cut retains an
independent $GL_3$ gauge **[P]**), and pure-target normalization — is
symmetric under it. No symmetric operation produces an antisymmetric
class.

The constrained theory is implemented as an equivariant
Cartan–Spencer calculus on the principal-parts resolution of the
source equations **[G]**, with its load-bearing identities audited: a
Ward identity $X_{\mathrm{src}}\Phi_c = \Phi_{Xc}$ for the colour-root
fields, verified termwise **[P]**; the Cartan homotopy $K = (1-s)H_w$
with $dK + Kd = (1-s)(w-1)$, annihilating the endpoint-even summand;
and a secondary-transfer computation identifying the local residue
class $-\delta = (-1, +1, +1, -1)$, which is forced and unique
**[P]**.

## 5. Uniformity in the order

Perfect matchings of $K_{2h}$ under $S_{2h}$ form the association
scheme graded by union cycle type, whose eigenvalue theory is
developed in Godsil and Meagher [18, Ch. 15]. The operators used by
the transfer — the two-switch adjacency $A_h$ and the endpoint-change
operator $B_h$ — act on isotypic summands indexed by even partitions
padding with $h$, with exact polynomial eigenvalues; for instance

$$A_h\big|_{[2h-2,\,2]} = h^2 - 3h + 1,$$

verified together with the five-sector spectrum of $B_h$ and the
composite transfer constant $56h^3(2h-1)$, out of sample through
$h = 12$ **[P]**. One-step transfer residuals lie in
$[2h] \oplus [2h-2,2]$ with multiplicity one at every computed order;
each composed transfer step raises the isotypic level by exactly one;
and the add-a-spectator embedding $\iota$ satisfies
$\pi A_{h+1} \iota = A_h$ exactly while itself raising the level by
one. The coefficient layer is thus finitely generated in the sense of
representation stability — the eventual-polynomiality phenomenon of
Church, Ellenberg, and Farb [19] — and uniformity in $h$ is invoked
*per composed step*: naturality along $\iota$ alone does not transport
the $[2h-2,2]$ statement **[P]**. Granted the family of Section 6, the
two window primitives descend to a carrier $\Gamma$ with
$d\Gamma = r - 2q$, and a Rodrigues-type moment identity **[G]**
annihilates the full tower of higher-moment conditions, producing the
clean pair at every order.

## 6. The remaining statement

The surviving branch of Section 3 localizes to a four-site residual
window whose channel amplitudes, with $H$ the common tail factor, are

$$A = D\,q_{01}\,H, \qquad B = p_0\,s_1\,H, \qquad C = p_1\,s_0\,H,$$

the doubled channel $A$ carrying its two endpoint orderings
(*charts*) $A_{[a|b]}$ and $A_{[b|a]}$. The equation-derived relations
among the channels are the four *primitive mate rows*

$$A_{[a|b]} + B, \qquad A_{[b|a]} + C, \qquad A_{[a|b]} + C, \qquad A_{[b|a]} + B,$$

of rank $3$ in the chart space with ordered basis
$\bigl(A_{[a|b]}, A_{[b|a]}, B, C\bigr)$. Their unique annihilator
**[P]** is

$$z \;=\; (1,\,1,\,-1,\,-1) \;=\; (1,-1)_{\text{chart}} \otimes (1,1)_{\text{matching}},$$

antisymmetric in the chart involution and symmetric on the matching
side — the source of the fencing theorems of Section 4. Three a priori
distinct obstructions coincide with $z$ **[P]**: the direction charge
of the trapped-coloop branch, the missing direction of the balanced
recurrent $K_{2,2}$ companion square, and the chart-sign class of the
all-order Bianchi comparison. Gauging by the shore sign
$\operatorname{diag}(1,1,-1,-1)$ carries the four columns to oriented
incidence columns and $z$ to $(1,1,1,1)$; as the oriented incidence
image is exactly the kernel of the vertex augmentation, the local
problem is to exhibit a single equation-derived column of nonzero
augmentation.

**Balanced chart-square saturation [O].** In every physical
fixed-tail occurrence of the window, construct a source-valid relative
cell with boundary $z \otimes (\text{local } C_4 \text{ tail})$,
natural under restriction, reinsertion, and chart overlap and
preserving the protected readouts (target, $q$, anchor, $W$, residue,
ridge) — or prove that the normalized dual
$\psi_z = \tfrac14(1,1,-1,-1)$, which annihilates every presently
constructed physical column **[P]**, extends to the accepted physical
terminal $q = \sum_{j=1}^{6} m_j - \mathrm{ainc}$, itself proved to
annihilate the complete $8{,}580$-column operator block and all $288$
repeated columns **[P]**.

Either branch completes the proof. A filler closes the trapped branch,
the $K_{2,2}$ square, and the Bianchi class at every order
simultaneously, and the clean pair follows by Section 5. A terminal
extension of $\psi_z$ is a Fredholm-type separator — a covector
certified against the system and nonzero on a class the
counterexample requires to be a boundary — refuting the support
directly, in the same logical shape as an (O1) refutation one level
up. Exact counterguards **[P]** exclude the known shortcuts: pure
normalization has $du = 0$; the $171$-column $q$-Jacobian admits no
restriction face into the square; and internal $K_{2,2}$ components
can be perfectly centered, so the required coupling must come from
global routing rather than local normalization.

## 7. Assembly

$$\text{minimal counterexample } (n \ge 8) \xrightarrow{\;\S 3\;} \text{clean pair, or the window of } \S 6 \xrightarrow{\;\S 6\;} \text{clean pair (via } \S 5\text{) or contradiction} \xrightarrow{\;\text{Thm B}\;} n-2 \longrightarrow \cdots \longrightarrow K_6 \text{ (Thm A)}.$$

Together with the reduction to $d = 3$, the bound of [12], the known
lower bounds, and the $n = 4$ exceptional analysis, this yields the
conjecture and the value of $k_{\max}(n)$.

| open item | status |
|---|---|
| balanced chart-square saturation (§6) | **[O]** — both branches under active attack |
| remaining window faces and placement maps | **[G]**; mechanical constructions in progress |
| per-step uniformity argument (§5) | coefficient half **[P]**; physical half rides on §6 |
| independent re-audit of the newest layer | in progress (`computations/unaudited-*`) |

**Summary.** By proved descent (Theorem B) to a proved base case
(Theorem A), through a proved local funnel and proved fencing
theorems, the Krenn–Gu conjecture reduces to a single alternative
concerning a single sign class on one four-site window: either
$z = (1,1,-1,-1)$ bounds an equation-derived cell, or its dual extends
to the certified terminal covector. Either resolution, made uniform in
the order as in Section 5, completes the proof.

## References

[1] M. Krenn, X. Gu, A. Zeilinger, *Quantum experiments and graphs:
Multiparty states as coherent superpositions of perfect matchings*,
Phys. Rev. Lett. **119**, 240403 (2017).

[2] M. Krenn, *A prized graph-theory question inspired by quantum
physics*, problem page:
[mariokrenn.wordpress.com/graph-theory-question](https://mariokrenn.wordpress.com/graph-theory-question/).

[3] L. S. Chandran, R. Gajjala, *Graph-theoretic insights on the
constructability of complex entangled states*, arXiv:2202.05562.

[4] I. Bogdanov, *Graphs with only monochromatic perfect matchings*,
MathOverflow (2017); see the account and extensions in [3].

[5] L. S. Chandran, R. Gajjala, A. M. Illickan, *The Krenn–Gu
conjecture for sparse graphs*, MFCS 2024; arXiv:2407.00303.

[6] G. Tsoukalas et al., *Advancing mathematics research with
AI-driven formal proof search*, arXiv:2605.22763 (2026).

[7] Google DeepMind, `formal-conjectures`,
`FormalConjectures/Paper/MonochromaticQuantumGraph.lean`
([github.com/google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)).

[8] T. Zaslavsky, *Signed graphs*, Discrete Appl. Math. **4** (1982),
47–74.

[9] D. Eisenbud, B. Sturmfels, *Binomial ideals*, Duke Math. J.
**84** (1996), 1–45.

[10] T. Kahle, C. Sarmiento, T. Windisch, *Parity binomial edge
ideals*, J. Algebraic Combin. (2016); arXiv:1503.00584.

[11] Lean 4 certificate of the normalized six-site fiber
(`eqSystem6_no_solution_d3` over $\mathbb{C}$), formal-conjectures
pull request #4610 (2026); developed independently and concurrently.

[12] Formal-conjectures pull request #4661 (2026): the bound
$k_{\max}(n) \le n - 2$ over arbitrary integral domains, via a
solver-free full-column anchor lemma.

[13] Brenner et al., *Hamilton connectivity of the matching flip
graphs of $K_{2n}$*, arXiv:2607.04687.

[14] Y. Guiraud, P. Malbos, *Higher-dimensional normalisation
strategies for acyclicity*, Adv. Math. **231** (2012), 2294–2351;
arXiv:1011.0558.

[15] B. Steinberg, *A Pride–Guba–Sapir exact sequence for the relation
bimodule of an associative algebra*, arXiv:2407.11879 (2024); with
Y. Kobayashi, F. Otto, J. Pure Appl. Algebra (2003) for the monoid
case originating in C. Squier's finiteness theory.

[16] J. A. De Loera, J. Lee, P. N. Malkin, S. Margulies, *Hilbert's
Nullstellensatz and an algorithm for proving combinatorial
infeasibility*, ISSAC 2008.

[17] F. Gesmundo, H. Huang, H. Schenck, J. Weyman, *Bernstein–
Gelfand–Gelfand meets geometric complexity theory: resolving the
$2 \times 2$ permanents of a $2 \times n$ matrix*, Trans. Amer. Math.
Soc. **378** (2025); arXiv:2312.12247.

[18] C. Godsil, K. Meagher, *Erdős–Ko–Rado Theorems: Algebraic
Approaches*, Cambridge Univ. Press (2016), Ch. 15.

[19] T. Church, J. S. Ellenberg, B. Farb, *FI-modules and stability
for representations of symmetric groups*, Duke Math. J. **164**
(2015), 1833–1910; arXiv:1204.4533.
