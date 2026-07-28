# Transverse cap rows at silent capped sites: two exclusion theorems, exact witnesses, and the sharpened saturation frontier

## 1. Outcome

This note attacks Priority 1 of
[the ranked list](current-proof-audit-and-next-steps.md): use effective
transverse/all-cap GHZ directions to cancel the six adjugate-visible
off-diagonal rows and the two diagonal relocations of the
[maximal transverse prism cap-slice countermodel](maximal-transverse-prism-cap-slice-countermodel.md)
while forcing proper mixed saturation.  The answer splits into two exact
exclusion theorems, two exact witnesses, and one exhaustive in-class
trade-off.  Together they determine exactly what the transverse cap
equations force on the eight explicit transverse rows.

Fix \(B=W\mathbin{\dot\cup}U\) with \(|U|=6\), and call a capped site
**boundary-silent** if all of its blocks toward \(U\) vanish.  The three
**pure-word transverse rows** are the tensor equations

\[
 G_i:=\iota_{U,i^6}H_B(A)=e_i^{\otimes W}\qquad(i=0,1,2),      \tag{1}
\]

the coefficient slices of the top tensor at the three pure boundary
words.  They contain both diagonal relocations of the maximal-slice
countermodel and are a small subsystem of one complete deleted-pair
tensor system; no second pair slice is ever imposed.

1. **Theorem 1 (no boundary-silent capped pair).**  At \(N=10\), with
   \(W=\{p,q,r,s\}\) and \(A_{ru}=A_{su}=0\) for all \(u\in U\), the
   three rows (1) are inconsistent — for arbitrary complex blocks
   everywhere else, with endpoint order, parallel sources, zero blocks,
   and cancellation retained.  Both prism guard families are
   boundary-silent at \(\{r,s\}\), so the entire geometry class that
   carries the known unit-saturation root covers is excluded by the
   pure-word part of the transverse rows alone.  Theorem 1′ extends this
   to every even \(N\ge10\): no hypothetical source has two capped sites
   \(r,s\) whose allowed blocks all stay inside one four-set
   \(\{p,q,r,s\}\).
2. **Theorem 2 (no pendant capped site).**  Under (1) alone, a capped
   site of degree at most one in the allowed block graph is impossible,
   at every even \(N\ge10\).
3. **Witness W0 (one silent site, full transverse system).**  One
   boundary-silent site is genuinely different: an exact fifteen-cell
   ten-site family has a silent site \(s\) of internal degree three and
   satisfies all three rows (1) coefficientwise, and its top tensor
   contains **no impure \(W\)-word at all** — every capped pair is
   pair-diagonal, so all six adjugate-visible off-diagonal rows and both
   relocations hold at every pair simultaneously.  Its only failures of
   the full GHZ equation are nine mixed boundary-word coefficients, each
   a product of two colour-needed cells: the root-cover pattern
   relocated into the boundary sector.  W0 has \(H_W=0\), so its scalar
   cofactor sector is empty.
4. **Witness W1 (the eight rows cancelled, active forms independent).**
   Adding the top-invisible-at-pure-words diagonal direct block
   \(A_{pq}=\operatorname{diag}(1,2,3)\) gives
   \(s(K)=K_{0000}+2K_{1100}+3K_{2200}\), so
   \(s,\kappa_0,\kappa_1,\kappa_2\) are independent linear forms on the
   cap space.  W1 still satisfies all three rows (1), both relocations,
   and complete pair-diagonality at the deleted pair \((p,q)\) and at
   \((r,s)\); in particular **all six adjugate-visible off-diagonal rows
   and both diagonal relocations of the maximal-slice countermodel are
   cancelled**, on a realizable common-edge family with a changed
   effective lower cofactor family.  Nevertheless the GHZ-form cap cubic
   \({\cal D}_{\rm ghz}(K)=6(s^2\sum_i\kappa_iX_i-H_6(A^K))\) has unit
   active saturation (Singular, characteristic zero).  Hence the eight
   transverse rows cannot force proper mixed saturation; a precise exact
   countermodel to that natural cap-selection statement.
5. **The cap condition itself is not the obstruction.**  The
   source-form cubic
   \({\cal D}_{\rm src}(K)=6(s^2F_U^K-H_6(A^K))\) of W1 saturates
   **properly**: the explicit rational cap
   \(K_{0000}=K_{1111}=K_{2222}=K_{0222}=K_{0100}=K_{1121}=1\),
   \(K_{2000}=K_{1011}=K_{2212}=K_{1021}=K_{0212}=-1\) (all other
   coordinates zero) is an active zero with \(h=s\kappa_0\kappa_1\kappa_2=1\).
   An active cap makes W1's cofactor family realize its own capped top
   tensor exactly.  The entire obstruction content of W1 sits in the
   seventeen mixed boundary-word defects of its top tensor.
6. **In-class trade-off (measured).**  In the three-channel class with
   unit weights, an exhaustive search over all \(729{,}000\) designs
   finds no family with a silent site, full \(W\)-purity, and
   top-invisible direct blocks: within this class one cannot have both
   the complete transverse \(W\)-row system and a nondegenerate scalar
   sector.  W0 and W1 realize the two extremes.

Exact artifacts, all new:

* [`cap_selection_lib.py`](../computations/cap_selection_lib.py) —
  fresh square-free site-algebra layer (no reuse of existing verifiers);
* [`cap_selection_reconstruct_shared_pair_ideal_and_exchange.py`](../computations/cap_selection_reconstruct_shared_pair_ideal_and_exchange.py)
  — independent reconstruction of the nine shared-pair rows, the
  overlapping-pair exchange chart and triple-slice identity, all
  countermodel invariants of the prism guard families
  (\(81/9/75/73/4/69\), prism image, \((z_0z_1z_2)\), adjugate matrix,
  the eight transverse rows), and the boundary-silent slice
  decomposition;
* [`cap_selection_transverse_row_forcing.py`](../computations/cap_selection_transverse_row_forcing.py)
  — Theorems 1 and 2 with characteristic-zero Singular certificates
  (`cap_selection_thm1_*.sing`, `cap_selection_thm2_*.sing`);
* [`cap_selection_one_silent_transverse_witness.py`](../computations/cap_selection_one_silent_transverse_witness.py)
  — witnesses W0, W1, their exhaustive coefficient censuses, both cap
  cubics, both saturation certificates
  (`cap_selection_witness_w1_ghz.sing`, `cap_selection_witness_w1_src.sing`),
  and the explicit clean source-form cap;
* [`cap_selection_full_w_purity_search.py`](../computations/cap_selection_full_w_purity_search.py)
  — the exhaustive three-channel trade-off search
  (`cap_selection_w2_ghz.sing` is written only if a witness exists;
  none does).

## 2. Setting and discipline

Work in the site-square-zero algebra with endpoint-ordered aggregate
blocks.  For \(W=\{p,q,r,s\}\), the transverse data of the maximal-slice
countermodel are coefficients of \(H_{10}(A)\): the six off-diagonal
rows are the coefficients whose \((p,q)\)-colours differ, and the two
diagonal relocations say the colour-\(c\) diagonal word sits at
\((c,c,c,c)\), not \((c,c,0,0)\), against the pure boundary word
\(X_c\).  The rows (1) are the complete pure-boundary-word part of this
system.

All hypotheses used below are coefficient subsets of the single
ten-site top tensor, equivalently of one complete deleted-pair tensor
system.  The
[pair-slice exchange theorem](ten-site-overlapping-pair-exchange-redundancy.md)
is respected: slicing (1) at \(s\), or at \((r,s)\), is a reindexing of
the same residual list into overlapping pair charts — the exchange
syzygy is used to identify the slice tensors as pair-chart data of the
three overlapping pairs, never to impose a second complete system.  The
reconstruction script replays the nine rows
\(R^{rt}_{ij}=a_{ij}Q+p_is_jF\), the redecomposition formulas for the
overlapping pair, and the triple-slice identity
\(\iota_{0,\alpha}R^{rt}_{ij}=\iota_{t,j}R^{r0}_{i\alpha}\) on random
exact data before anything else is trusted.

## 3. Theorem 1: no boundary-silent capped pair

**Theorem 1.**  Let \(A\) be any ten-site aggregate family,
\(U\) a six-set, \(W=\{p,q,r,s\}\).  If \(A_{ru}=A_{su}=0\) for every
\(u\in U\), then the three rows (1) are inconsistent.

**Proof.**  Because \(r,s\) are boundary-silent, every perfect matching
of \(B\) pairs \(r\) and \(s\) inside \(W\).  Sorting matchings by that
pattern gives the exact decomposition (verified by literal enumeration
in the reconstruction script, including degenerate data):

\[
 G_i=\theta_i\,\mathbb H_W
   +\sum_{j,k}M^{(i)}_{jk}\,e_j^{(p)}e_k^{(q)}\otimes A_{rs},
 \qquad
 \theta_i=[X_i]x^{[3]},\quad
 M^{(i)}_{jk}=[X_i]\bigl(\ell_jm_kx^{[2]}\bigr),               \tag{2}
\]

where \(x,\ell,m\) are the \((p,q)\) pair-chart data of the boundary and
\(\mathbb H_W\) is the internal four-site hafnian tensor.  Write
\(R=A_{rs}\in V_r\otimes V_s\) and let \(N_{cc}\) be the
\((p,q)=(c,c)\) slice of \(\mathbb H_W\).  Reading (1) at the diagonal
\((p,q)\)-slices only, every hypothesis point satisfies, in
\(V_r\otimes V_s\),

\[
 \theta_i N_{cc}+M^{(i)}_{cc}R=\delta_{ic}\,e_ce_c
 \qquad(i,c=0,1,2).                                            \tag{3}
\]

Case split on the number of nonzero \(\theta_i\).  If at least two are
nonzero, then for each \(c\) some \(i'\ne c\) has \(\theta_{i'}\ne0\),
and the \((i',c)\) equation puts \(N_{cc}\in\operatorname{span}(R)\);
the \((c,c)\) equation then puts \(e_ce_c\in\operatorname{span}(R)\) for
all three \(c\) — impossible, since \(e_0e_0,e_1e_1,e_2e_2\) are
independent and \(\operatorname{span}(R)\) has dimension at most one.
If exactly one \(\theta_a\ne0\), the two colours \(b\ne a\) give
\(M^{(b)}_{bb}R=e_be_b\), so two independent tensors lie in
\(\operatorname{span}(R)\).  If all \(\theta_i=0\), all three do.  In
every case, contradiction.  \(\square\)

The machine certificate treats \(\theta\), \(M\), the direct block, and
the four internal star rows as free variables — a sound weakening,
since any actual family satisfying the hypotheses projects onto an
abstract solution — and proves the unit ideal over \(\mathbb Q\) on the
four-stratum cover \(\{\theta_0\ne0\}\), \(\{\theta_1\ne0\}\),
\(\{\theta_2\ne0\}\), \(\{\theta=0\}\), by one saturation
\(I:\theta_i^\infty=(1)\) per open stratum and one unit ideal on the
closed stratum.  No finite-field step occurs anywhere.

**Theorem 1′ (all even \(N\ge10\)).**  If two capped sites \(r,s\) have
all their allowed blocks inside \(\{p,q,r,s\}\) for some further sites
\(p,q\in W\), the rows (1) are inconsistent.

**Proof.**  The same pattern decomposition gives, for the
\((p,q,r,s)=(c,c,\alpha,\beta)\) slices with values in
\(\bigotimes_{W'}V\), \(W'=W\setminus\{p,q,r,s\}\),

\[
 R_{\alpha\beta}\,[\Phi_i]_{cc}
 +\bigl(u_{c\alpha}v_{c\beta}+w_{c\beta}z_{c\alpha}\bigr)\,\Xi_i
 =\delta_{ic}\delta_{c\alpha}\delta_{c\beta}\,e_c^{\otimes W'},
\]

with \(\Phi_i=\iota_{U,i^6}H_{B\setminus\{r,s\}}\),
\(\Xi_i=\iota_{U,i^6}H_{B\setminus\{p,q,r,s\}}\), and
\(u,v,w,z\) the four internal star matrices of \(r,s\).  Packaging the
\((\alpha,\beta)\)-dependence as tensors
\(T^{(c)}_i=R\otimes[\Phi_i]_{cc}+(u_c\otimes v_c+z_c\otimes w_c)\otimes\Xi_i\),
the hypothesis reads \(T^{(c)}_i=\delta_{ic}\,e_ce_c\otimes e_c^{\otimes W'}\).
If \(\Xi_{i'}\ne0\) for some \(i'\ne c\), a \(W'\)-contraction with
\(\Lambda(\Xi_{i'})=1\) gives
\(u_c\otimes v_c+z_c\otimes w_c\in\operatorname{span}(R)\), and the
colour-\(c\) equation forces \(e_ce_c\in\operatorname{span}(R)\); if
\(\Xi_b=0\), the colour-\(b\) equation directly forces
\(e_be_b\in\operatorname{span}(R)\).  Counting nonzero \(\Xi_i\) exactly
as in Theorem 1 always places two independent tensors in the span of
one vector.  \(\square\)

At \(N=10\) the hypothesis of Theorem 1′ is exactly boundary-silence of
\(\{r,s\}\); at larger \(N\) it also requires silence toward the other
capped sites, and is stated in that stronger form.

**Consequence for the prism guards.**  The
[four-parameter barrier](actual-cofactor-cap-cubic-and-four-parameter-prism-barrier.md)
and the maximal-slice countermodel both have \(r,s\) attached only to
\(\{p,q,r,s\}\).  Theorem 1 proves their observed relocation failure
\(G_i=e_ie_ie_0e_0\) is forced: **no** family in their geometry class
can satisfy the transverse pure-word rows.  Any family compatible with
the transverse rows must activate boundary stars at the extra capped
sites, which inserts new star-response directions into every cofactor
block \(A^K_{uv}\).  "The transverse equations change the effective
lower cofactor family" is now a theorem, not a hope.

## 4. Theorem 2: no pendant capped site

**Theorem 2.**  Under (1) alone — every other block fully arbitrary —
no capped site can have degree at most one in the allowed block graph,
at any even \(N\ge10\).

**Proof.**  For a pendant site \(s\) attached only to \(w\), every
matching pairs \(s\) with \(w\), so the \((w,s)=(\gamma,\beta)\) slice
of (1) reads \(A_{ws}[\gamma,\beta]\,\Phi_i=\delta_{i\gamma}\delta_{i\beta}
e_i^{\otimes W\setminus\{w,s\}}\).  Colour \(i\) at \((i,i)\) forces
\(\Phi_i\ne0\); colour \(i\) at any \((\gamma,\beta)\ne(i,i)\) then
forces \(A_{ws}[\gamma,\beta]=0\).  Applying this for two distinct
colours annihilates every cell each colour needs.  \(\square\)

The two \(N=10\) instances (pendant to the other extra site, pendant to
a pair site) carry standalone Singular unit-ideal certificates over
\(\mathbb Q\), after the slice shapes are re-verified against literal
enumeration on random families.

## 5. One silent site is realizable: witnesses W0 and W1

Theorem 1 cannot be strengthened to one silent site.  The abstract
\(s\)-slice system of (1) — nine tensor equations in
\(V_p\otimes V_q\otimes V_r\) coupling the three attachment blocks of
\(s\) to the pure-word contractions \(g_i,g'_i,g''_i\) of the three
eight-site subfamilies obtained by deleting \(\{r,s\}\), \(\{p,s\}\),
\(\{q,s\}\) — has the colour-separated solution

\[
 A_{rs}=e_0e_0,\quad A_{ps}=e_1e_1,\quad A_{qs}=e_2e_2,\qquad
 g_0=e_0e_0,\quad g'_1=e_1e_1,\quad g''_2=e_2e_2,              \tag{4}
\]

with all other slice data zero: each colour uses its own channel.  The
silent site acquires exactly the rank-one same-colour degree-three
attachment pattern of the cubic-vertex lemma
([prism-plus-one-edge-obstruction](../proofs/prism-plus-one-edge-obstruction.md)),
now derived from the pure-word rows alone.  The realization problem for
(4) is three simultaneous pure-word conditions on three overlapping
eight-site subfamilies of one nine-site family, and it is solvable:

**Witness W0.**  \(U=(x_0,x_1,x_2,y_0,y_1,y_2)\), all weights one:

\[
\begin{array}{lll}
 ps=(1,1),& qs=(2,2),& rs=(0,0),\\
 p\,y_1=(0,0),\ q\,y_2=(0,0),& q\,x_0=(1,1),\ r\,x_1=(1,1),&
 p\,x_2=(2,2),\ r\,y_0=(2,2),\\
 x_0x_1\in\{(0,0),(2,2)\},&
 x_2y_0\in\{(0,0),(1,1)\},&
 y_1y_2\in\{(1,1),(2,2)\}.
\end{array}                                                    \tag{5}
\]

Exhaustive enumeration gives \(H_{10}(\mathrm{W0})\) with exactly twelve
monomials: the three pure targets \(e_i^{\otimes10}\) with coefficient
one, and nine mixed defects, all of the form
\(e_i^{\otimes W}\otimes(\hbox{mixed boundary word})\).  There is **no
impure \(W\)-word at all**: all six capped pairs are pair-diagonal, all
six adjugate-visible rows and both relocations hold at every pair, and
all three rows (1) hold coefficientwise.  Each mixed defect mixes cells
that different colours need — the root cover relocated into the
boundary sector.  For example the defect
\(e_0^{\otimes W}\otimes e_{001100}\) comes from the colour-0 route
(crosses \(p\,y_1,q\,y_2\) and cell \(x_0x_1{:}00\), all needed for the
colour-0 target) completed by the colour-1-needed cell
\(x_2y_0{:}11\); every factor is needed by some pure target, so no
choice of nonzero weights kills it.  W0 has \(H_W=0\): every internal four-site
matching crosses a missing edge, so \(s(K)\equiv0\) and the active
sector is empty.

**Witness W1.**  Add \(A_{pq}=\operatorname{diag}(1,2,3)\).  The new
top routes traverse \(pq\), \(rs\), and a full internal boundary
matching, so:

* all three rows (1) are unchanged (no pure boundary word completes);
* both relocations and the full pair-diagonality at \((p,q)\) and at
  \((r,s)\) survive: the top tensor still has no \(W\)-word with
  \(p,q\) colours (or \(r,s\) colours) unequal — the **eight transverse
  rows of the maximal-slice countermodel are all cancelled**;
* \(H_W=\sum_it_i\,e_ie_ie_0e_0\) with \(t=(1,2,3)\), so
  \(s(K)=K_{0000}+2K_{1100}+3K_{2200}\) and
  \((s,\kappa_0,\kappa_1,\kappa_2)\) has rank four: independent active
  forms;
* the price is exact and measured: sixteen new monomials with impure
  \(W\)-words \((1,1,0,0)\) and \((2,2,0,0)\) at mixed boundary words —
  transverse rows of the four cross pairs \((p,r),(p,s),(q,r),(q,s)\),
  never of the deleted pair.

The effective cap coordinates of W1 are the fourteen words listed by
the script.  Its two denominator-cleared cubics behave oppositely:

\[
\begin{array}{ll}
 {\cal D}_{\rm ghz}=6\bigl(s^2\textstyle\sum_i\kappa_iX_i-H_6(A^K)\bigr):&
 I:h^\infty=(1)\ \hbox{(Singular, char }0),\\[2pt]
 {\cal D}_{\rm src}=6\bigl(s^2F_U^K-H_6(A^K)\bigr):&
 I:h^\infty\ \hbox{proper, with the explicit active zero of Section 1.}
\end{array}
\]

The first line is the countermodel content: a realizable common-edge
family with independent active forms, a boundary-silent site, and
**every one of the eight transverse rows cancelled**, whose GHZ-form
cap cubic still has unit active saturation.  The natural cap-selection
statement "cancelling the six adjugate-visible off-diagonal rows and
the two diagonal relocations forces proper mixed saturation" is false.
The second line sharpens where the obstruction lives: W1 even admits a
clean *source-form* cap — the cap condition itself is solvable — so the
whole obstruction content of this family sits in the seventeen mixed
boundary-word defects of its top tensor, exactly the six-site residue
that the transverse \(W\)-sector cannot see.

Also verified: the mixed part of \({\cal D}_{\rm src}\) factors through
\(s\) on six of its seven coordinates
(\(-6s\cdot(K_{0000}K_{2222}+K_{0222}K_{2000})\) and cyclic patterns),
with one genuinely trilinear coupling coordinate; the pure coordinates
vanish identically, i.e. the capped pure sector automatically equals
\(s^2\kappa_i\) for this family.

## 6. The measured trade-off: full \(W\)-purity taxes the scalar sector

W0 satisfies the complete transverse \(W\)-row system at all six pairs
but has \(s\equiv0\); W1 has independent active forms but reintroduces
impure \(W\)-words at four pairs.  Inside the natural three-channel
class — silent \(s\) with the cubic-vertex attachments, one
colour-\((c,c)\) cross cell from each channel site at chosen boundary
sites, two colour-\((c,c)\) internal cells tiling the complement, unit
weights, and direct blocks made top-invisible by the absence of an
internal boundary matching — the trade-off is forced:

* all \(729{,}000\) designs (ordered cross-site choices times internal
  pairings) fail the support conditions for full \(W\)-purity with
  top-invisible direct blocks; the nine kill conditions (each wrong
  cross-colour combination must not complete) and the no-boundary-
  matching condition are jointly unsatisfiable;
* structurally, a *visible* direct cell preserves \(W\)-purity only if
  colour-aligned, and colour-aligned visible cells contribute only
  \(\kappa\)-multiples to \(s(K)\), collapsing the active-form rank to
  three.

This is measured in-class data, not a theorem: arbitrary weights (with
cancellation between distinct completions), non-channel supports, and
entangled attachments are outside the exhaustion.  The exact open
statement is recorded in Section 8.

## 7. Countermodel-guard audit

* **Projective-height obstruction**: no dimension or height count is
  used anywhere; Theorems 1, 1′, 2 are derived from the nonlinear
  matching decomposition of one pair chart, and the certificates are
  Nullstellensatz unit ideals in characteristic zero.
* **Actual-cofactor prism barrier / maximal-slice countermodel**: both
  lie in the two-silent stratum killed by Theorem 1; the theorems
  explain their relocation failure instead of contradicting them.  The
  new witnesses do not weaken either guard: they satisfy a different,
  incomparable hypothesis set (transverse rows closed, literal GHZ cap
  formula on large slices open), and the pair of guard families now
  brackets the frontier from both sides.
* **Literal shared pair-cap countermodel (\(N=8\))**: \(W\) has no
  extra capped sites there; Theorems 1 and 2 are silent about it, and
  nothing here relies on \(zq^{[m-1]}\)-only reasoning.
* **Pair-slice exchange**: only subsystems of one complete pair system
  are imposed; slices are chart reindexings (the exchange syzygy), and
  no dimension count ever adds a second complete slice.
* **Unit-saturation universality**: respected and re-certified — the
  GHZ-form cubic of W1 saturates to the unit ideal, as the six-site
  theorem demands of every actual family; no proper-GHZ-saturation
  claim is made for any realizable family.
* **Root-cover family**: the witnesses' boundary defects are products
  of colour-needed cells — the same root-cover mechanism, now confined
  to the mixed boundary sector; no claim that killing one mixed
  coefficient retains the pures.
* **No fixed-anchor conclusions**: Theorems 1, 1′, 2 hold for arbitrary
  complex blocks in their strata; the witnesses are constructions and
  are labelled as such; the exhaustion of Section 6 is explicitly
  class-restricted.

## 8. Exact remaining frontier

The Priority-1 question is now answered at the transverse layer and
relocated:

1. **Answered negatively**: cancelling the six adjugate-visible
   off-diagonal rows and both relocations — even with independent
   active forms, realizability, and a changed effective cofactor
   family — cannot force proper mixed saturation (witness W1 plus its
   Singular certificate).  Any cap-selection or cap-span-saturation
   derivation must use coefficients outside the transverse
   \(W\)-sector.
2. **Answered positively**: the transverse pure-word rows do force
   structure — no two-silent capped pair (Theorems 1, 1′), no pendant
   capped site (Theorem 2), and at a single silent site the
   cubic-vertex colour-channel attachment (4).  Every surviving
   configuration must activate boundary stars at the extra capped
   sites, inserting star-response directions into all cofactor blocks.
3. **The load-bearing sector**: for the witness class the entire
   remaining GHZ obstruction is the mixed boundary-word sector — nine
   (W0) or seventeen (W1) defect coefficients, each a product of
   colour-needed cells.  The next exact targets, in order:
   * prove or refute, beyond the three-channel class, the trade-off of
     Section 6: *a boundary-silent capped site plus full \(W\)-purity
     forces \(s(K)\in\operatorname{span}(\kappa_0,\kappa_1,\kappa_2)\)*
     — a cancellation-aware version of the \(729{,}000\)-design
     exhaustion; a proof would make the scalar sector degenerate on the
     entire silent stratum and push every viable source geometry to
     zero silent sites;
   * characterize the abstract solution variety of the \(s\)-slice
     system beyond the channel component (4) — in particular whether
     the pure-word rows force the rank-one same-colour attachment
     pattern at every silent site, upgrading (4) from a witness to a
     normal form;
   * couple the forced boundary-star activation of item 2 to the mixed
     boundary defects: the star responses that Theorems 1--2 force into
     the cofactor blocks are new effective directions the prism slices
     never had, and the open question is whether the full nine-row
     ideal makes them cancel the boundary-sector root cover — this is
     the exact residue of the cap-selection theorem, now stripped of
     its transverse-row component.

None of this touches the fan escape charts; the silent-site theorems
are cap-side statements about capped-region geometry, and their only
interface to the fan side is the shared conclusion that degenerate
attachment patterns are impossible for hypothetical sources.
