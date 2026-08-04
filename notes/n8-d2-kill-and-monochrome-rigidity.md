# The N = 8 endgame: D2 dies on the swept class, and the monochromatic anchors are rigid on Sigma

Checker:
[`computations/verify_n8_d2_kill_and_monochrome_rigidity.py`](../computations/verify_n8_d2_kill_and_monochrome_rigidity.py).

Companion (the reduction this note attacks):
[`notes/n8-saturation-census-two-configurations.md`](n8-saturation-census-two-configurations.md),
which reduces Theorem C's saturating gap at \(N=8\) to exactly two
scalar configurations, **D1** \((k,|R|,t)=(2,4,0)\) and **D2**
\((3,2,2)\), both on the split shape \((2,2,4)\) with the saturating
colour on the 4-part.  **That companion pair — note and checker — is
untracked in git at the time of writing: it is packaged but not
committed, and its independent audit has not landed.**  Everything this
note says about D1/D2 is therefore conditional on a reduction that is
not yet part of the committed record.

This note kills **D2** on the swept branch class and proves that the
**monochromatic pair** \(b^8,c^8\) is rigidly unsatisfiable on the
a-column support class \(\Sigma\) of **D1** — localizing what is left of
\(N=8\) to out-of-\(\Sigma\) supports.

All conventions, notation and cited results (Lemma 0, Theorems A/B,
Lemma E with (E1)–(E3), Lemma F, Theorem C, Corollaries C1–C3) are
those of
[`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md)
and
[`notes/good-crossing-matching-forcing.md`](good-crossing-matching-forcing.md).
The checker **imports** both committed checkers through `importlib`,
**pins the sha256 digest** of each, and re-derives the census geometry
from the *same* committed enumerators (`crossing_pairs`,
`matchings_inside`) rather than importing the census pair — so the two
artifacts agree by construction without either depending on the other.
Both committed modules are stateless (pure functions over explicitly
passed block dictionaries), so a single import serves every
configuration; each configuration builds its own fresh blocks.

## Audit history

**An independent audit of the first packaging of this pair returned
FAIL, and this is the corrected version.**  The audit rebuilt the D2
geometry with its own matching enumerator over \(\mathrm{GF}(2^{61}-1)\)
— no polynomial ring at all — and reproduced every branch verdict
row-by-row; it also confirmed the pigeonhole, the relabelling orbit, the
genuinely-polynomial character of the rigidity identity, the
\(\ge 22\) dimension bound, and found no zero-fire guard among 97
`require` sites over 11 383 executions.  The **conclusions survived**.
What failed were claims *around* them, all corrected here:

* the claim that the six original support families were **complete
  under saturation** was **false** — the audit exhibited saturated
  U-system solutions outside them.  The sweep now runs over **eight**
  families (\(8^3=512\) combinations), and the completeness claim is
  replaced by the *signature reduction* of §2.5, which is what the
  certificates actually consume;
* the "saturation bridge on all 648 slots" was a **tautology**
  (\(\nu\,A_{up}(\chi)+s_e\,\nu\nu^{-1}\) with \(A_{up}(\chi)\) *defined*
  as \(-s_e\nu^{-1}\)); it tested the polynomial ring, not the
  mathematics.  It is gone, replaced by the non-trivial statements
  (§2.5);
* the ledger's "no hard-coded truth value or count" claim was false
  (two literals); the literals are gone and the sentence is now accurate;
* the witness-tensor cell counts were misstated as uniform;
* \(\chi\) was an unchecked constant — mutating it passed silently; it
  is now **required** to be the split's own part map;
* the four-pencil verdict was asserted in the note but only
  *existentially* required in the checker;
* the 272-word budget was asserted and never computed;
* the "cross-implementation control" of the matching sum was a
  transliteration sharing the committed enumerator, and is now
  described as what it is: a **ring validation**.

**Status, claim by claim.**

| claim | strength |
|---|---|
| D2 obstructed on all 512 branch combinations of the swept class | **machine fact** (exact polynomial identities, §2) |
| the three certificate mechanisms and their word budgets | **machine fact** (identities verified, not assumed; every certificate word required to lie in the computed 272-word budget, §2.3–2.4) |
| the eight swept families exhaust the U-system | **FALSE, withdrawn** — see §2.5 |
| the realizable two-colour column signatures are exactly seven, and no saturated solution feeds both residue sites | **hand proof** (§2.5), with a \(\mathrm{GF}(2)\) census of all 28 350 saturated solutions as **machine evidence over one finite field** |
| every two-endpoint signature carries the extended exchange structure | same: hand proof + \(\mathrm{GF}(2)\) census |
| equivariance of skeleton/certificates under relabelling; orientation inertness | **UNVERIFIED INSPECTION** — the sweep's coverage of all 48 census D2 families depends on it (§2.6) |
| \(H(b^8)=H(c^8)=0\) identically on \(\Sigma\) | **machine fact** (polynomial identity in all 89 free cells, §3) |
| the frozen-chart repair step is infeasible | **machine fact** (exact pencil-rank certificate, all four sharing pencils, §4.3) |
| the 6559/6561 family, its harmful member, local dimension \(\ge 22\) | **machine facts on instances** (§4) |
| D1 on out-of-\(\Sigma\) supports | **OPEN** (§5, §6) |
| Krenn's conjecture | **OPEN** |

Nothing here is a statement about an exact \(N=8\) source that has been
verified on one: **no exact ternary source at \(N=8\) is available to
test on** — showing none exists is the project's aim.  What is verified
is that certain *support classes* cannot carry one.

---

## 0. Summary of outcomes

* **Theorem 1 (D2 kill on the swept class).**  On the census-mirrored
  D2 geometry, imposing the D2 skeleton (Lemma F purity at every
  carrier pair-deletion, (E1) at the essential sites, \(A_{67}=\nu
  E_{aa}\)) and choosing one of eight support families per carrier,
  **all \(8^3=512\) branch combinations are obstructed**: 128
  anchor-dead, 192 by the \(\Gamma\)-certificate (3 words), 192 by the
  c-factor certificate (4 words), **0 survivors**.  The elimination
  engine is never needed; every kill is a certificate consuming at most
  four words of the 272-word pair-inside budget (membership required).
* **The mechanism is a pigeonhole.**  Three carriers feed two residue
  sites.  The computed feeder distribution over the 512 combinations is
  \((64,192,192,64)\) for \((\#\text{feeders at }6,\#\text{at }7)\in
  \{(0,3),(1,2),(2,1),(3,0)\}\): the **128 combinations that starve a
  residue site are exactly the 128 anchor-dead ones**, and the 384 with
  a singly-fed site are exactly the certificate kills.
* **The signature reduction (§2.5)** is what makes the sweep mean
  something beyond its own families: under saturation a carrier's
  U-system solution can feed two-colour cells into **at most one**
  residue site, its realizable signature is one of **seven**, and the
  two-endpoint signature forces the extended exchange structure.  Hand
  proof; \(\mathrm{GF}(2)\) census as evidence (28 350 saturated
  solutions, **zero** feeding both sites).
* **Theorem 2 (monochromatic rigidity on \(\Sigma\)).**  On the
  a-column support class \(\Sigma\) of the D1 geometry (89 free cells),
  \(H_B(b^8)=H_B(c^8)=0\) **identically** — every one of the 105
  perfect matchings contains at least two residue-incident edges, and
  every residue-incident edge is \((b,b)\)- and \((c,c)\)-dead.
  Exactness needs 1.  So **no exact source lives on \(\Sigma\)**.
* **Structural finding 3 (the near-miss family).**  An explicit
  rational family with **exact Jacobian rank 22** satisfies every
  census fact of the D1 configuration and **6559 of the 6561**
  exactness equations — the only defects being \(b^8, c^8\) — and has a
  member whose D1 rectangle is **degenerate with both products
  nonzero** (the harmful branch).  Together with §4.3 (the frozen-chart
  step is provably infeasible) this says: the two-carrier core words
  are **repairable**, the **anchors are not**, and the census fact set
  plus two-colour repairs **cannot decide D1**.
* **The endgame state.**  With the census: D2 is dead on the swept
  class, so **D1 is the sole remaining \(N=8\) obstruction**, and
  within D1 the killing family is the monochromatic pair, alive only on
  supports that leave \(\Sigma\).  §6 is a marked placeholder for the
  classification sweep of that cell, which is in progress.

---

## 1. Setting

Canonical split (the census's own, re-derived here from
`crossing_pairs` + `matchings_inside`):
\(S_b=\{0,1\}\), \(S_c=\{2,3\}\), \(S_a=\{4,5,6,7\}\), saturating
colour \(a=2\).  Colour codes are the committed ones: \(0=b\), \(1=c\),
\(2=a\).  The colour word \(\chi\) is **not a constant of this
artifact**: it is required to equal the word induced by the split
through the committed `part_map`, and the D2 saturation slots are
required to read \(\chi\) at the essential sites and their partners.

The saturating signatures of this split are exactly
\(\{(2,4,0),(3,2,2),(4,0,4)\}\) — D1, D2, and the empty-residue class
Lemma H kills.  The checker requires this, and controls the
enumeration path positively (the named D1 family \(\{\{0,2\},\{1,3\}\}\)
must appear) and negatively (the single edge \(\{0,2\}\), which leaves
sites 1 and 3 uncovered outside \(S_a\), must not).

**D2 representative.**  \(F_2=\{\{0,2\},\{1,4\},\{3,5\}\}\), residue
\(R=\{6,7\}\), signature \((3,2,2)\): one \(S_b\)–\(S_c\) carrier plus
two \(S_a\) carriers, each with exactly one endpoint in \(S_a\).  The
essential endpoints (the pendant choice) are \(0,1,3\), with partners
\(2,4,5\).  At each carrier \((\chi_u,\chi_p)\ne(a,a)\) — required, and
the reason the purity constant \(m_e\) drops out of the crossing cell.

**D1 / \(\Sigma\) geometry.**  \(F_a=\{\{0,2\},\{1,3\}\}\), residue
\(R=S_a\), essential endpoints \(0,1\) with partners \(2,3\).

**Word budget.**  The sharpened kernel's pair-inside budget — words with
the four non-residue letters in \(\{b,c\}\) and \(\rho\in\{b,c\}^4\cup
\{(a,a,a,a)\}\) — is **computed** to have 272 distinct words, all inside
the non-automatic slice; every certificate word produced by the sweep
(30 distinct words in all) is required to lie in it.

---

## 2. Theorem 1 — D2 dies on the swept class

### 2.1 The skeleton

Fix the geometry of §1 and an exact source with that live split and
saturating family.  The following are forced by committed results (see
the census note §3–4 and Lemma F):

* **(E1)** row \(a\) of \(A_{ux}\) vanishes for \(x\) not the partner
  of the essential site \(u\in\{0,1,3\}\);
* \(H_R = \nu E_{aa}\) with \(\nu\ne0\) — i.e. \(A_{67}=\nu E_{aa}\)
  (Lemma F on the full family);
* for each carrier \(e\), Lemma F on \(F_2\setminus\{e\}\) gives
  purity of the 4-site tensor \(H_{R\cup e}=m_e\,e_a^{\otimes4}\).

Splitting that 4-site purity at \(A_{67}=\nu E_{aa}\) gives two groups.
The **T-relations** (residue word \((a,a)\)) *define* the carrier block:

\[
  A_{up}(i,j)\;=\;\frac{m_e\,\delta_{(i,j),(a,a)}-s_e(i,j)}{\nu},
  \qquad
  s_e(i,j)=A_{u6}(i,a)A_{p7}(j,a)+A_{u7}(i,a)A_{p6}(j,a).
                                                            \tag{T}
\]

The **U-relations** (every residue word other than \((a,a)\)) constrain
the four residue-adjacent blocks:

\[
  A_{u6}(i,k)\,A_{p7}(j,l)+A_{u7}(i,l)\,A_{p6}(j,k)\;=\;0
  \qquad\text{for all } i,j \text{ and all } (k,l)\ne(a,a).
                                                            \tag{U}
\]

Since \((\chi_u,\chi_p)\ne(a,a)\), the saturating crossing cell is
\(A_{up}(\chi)=-s_e(\chi)/\nu\): **saturation is exactly
\(s_e(\chi)\ne0\)**.

### 2.2 The eight per-carrier support families

Per carrier \(e=\{u,p\}\), with \(\{keep,drop\}=\{6,7\}\):

| family | support |
|---|---|
| **g6 / g7** | \(A_{u,keep}\) a-column only; \(A_{u,drop}=0\); \(A_{p,drop}\) a-column only; \(A_{p,keep}\) **free** |
| **x6 / x7** | the rank-1 **exchange** pattern: \(A_{u,keep}(\cdot,k)=c_k w\) with a-column **zero**, \(A_{u,drop}(\cdot,a)=w\), \(A_{p,keep}(\cdot,k)=-c_k q\), \(A_{p,keep}(\cdot,a)=q_{\text{free}}\), \(A_{p,drop}(\cdot,a)=q\) |
| **xf6 / xf7** | the **extended exchange**: as x, but the a-column of \(A_{u,keep}\) is **free**.  (Added after the audit; §2.5 shows this is the family forced whenever both carrier endpoints feed one residue site.) |
| **d6 / d7** | the **free-column degenerate** family: \(A_{u,keep}\) has *free \(b,c\)-columns* (rank up to 2 — outside the exchange closure), a-column zero; \(A_{u,drop}\), \(A_{p,keep}\) a-column only; \(A_{p,drop}=0\) |

The d-families were found beyond the exchange closure (the earlier
\(N=6\) analysis did not carry them); the xf-families were found by the
audit.  Each of the eight is machine-verified to be saturable: its
\(s_e(\chi)\) is a **nonzero polynomial** on all \(3\times512=1536\)
(combination, carrier) slots.

### 2.3 The three certificates

Write \(P_r\) for the set of endpoints whose block toward residue site
\(r\) carries a \(\{b,c\}\times\{b,c\}\) cell.  Each carrier contributes
to exactly one residue site: g contributes \(\{p\}\), d contributes
\(\{u\}\), x and xf contribute \(\{u,p\}\).

1. **Anchor death** (\(P_r=\varnothing\)).  Every block into \(r\) is
   a-column-only or \(\nu E_{aa}\), so every matching term of
   \(H_B(c^8)\), \(c\in\{b,c\}\), contains a zero factor:
   \(H_B(b^8)=H_B(c^8)=0\) identically, contradicting exactness.
   *Certificate: the two anchors.*
2. **The \(\Gamma\)-certificate** (\(P_r=\{x\}\)).  Every two-colour
   word's matching terms contain the single factor \(A_{xr}\), so with
   \(\Gamma_c=H_{B\setminus\{x,r\}}(c\text{ everywhere})\):
   \[
     H_B(c^8)=A_{xr}(c,c)\,\Gamma_c,\qquad
     H_B(c^8|_{x,r\mapsto d})=A_{xr}(d,d)\,\Gamma_c .
   \]
   Exactness makes the first \(=1\) for both \(c\) (so \(\Gamma_b,
   \Gamma_c, A_{xr}(b,b), A_{xr}(c,c)\) are units) and the second
   \(=0\), forcing \(A_{xr}(d,d)=0\).  Contradiction.
   *Certificate: \(b^8\), \(c^8\), and one flip word* — three words.
3. **The c-factor certificate** (\(P_r=\{u,p\}\) from one carrier, of
   exchange type).  Both blocks into \(r\) have their \(b,c\)-columns of
   the form \(c_k\cdot(\text{vector independent of }k)\), so the
   exchange scalar \(c_{w_r}\) factors out of every word:
   \[
     H_B(c^8|_{r\mapsto d})\cdot c_c \;=\; H_B(c^8)\cdot c_d .
   \]
   Exactness gives \(c_d=0\) for both \(d\), while the anchors need
   \(c_c\ne0\).  Contradiction.  *Certificate: \(b^8\), \(c^8\) and two
   flip words* — four words.

**Both factorizations are verified as exact polynomial identities** in
the combination's parameter ring (a sparse multivariate polynomial ring
over \(\mathbb{Q}\) built in the checker from stdlib `Fraction` only),
for every combination that is classified by them.  A certificate that
fails its identity is *not* recorded as a kill: the classifier returns
"no certificate", which is what the designed negative probes exploit.

### 2.4 The sweep

~~~text
512 branch combinations (8 families x 3 carriers)
 128  ANCHOR-DEAD           certificate = {b^8, c^8}
 192  GAMMA                 certificate = {b^8, c^8, flip}          (3 words)
 192  C-FACTOR              certificate = {b^8, c^8, flip, flip'}   (4 words)
   0  survivors
~~~

Examples from the recorded ledger (combination, verdict, witness):

~~~text
02:g6,14:g6,35:g6   ANCHOR-DEAD   00000000, 11111111
02:g6,14:g6,35:g7   GAMMA         unique partner A_57 ; word 00000101
02:g6,14:g6,35:x7   C-FACTOR      exchange carrier (3,5) at residue 7 ;
                                  words 00000001, 11111110
02:g6,14:g6,35:d7   GAMMA         unique partner A_37 ; word 00010001
~~~

Two structural facts are required, not assumed:

* the feeder distribution over the 512 combinations is exactly
  \(\{(0,3):64,\ (1,2):192,\ (2,1):192,\ (3,0):64\}\) — the pigeonhole,
  computed;
* the 128 starved combinations are **exactly** the 128 anchor-dead ones
  (the implication "starved \(\Rightarrow\) both anchors identically
  zero" is required per combination).

Two independent computations of "who feeds \(r\)" (the feeder count and
the two-colour partner set) are cross-checked against each other on
every combination.

The sharpened-kernel question this sweep was built to answer — *can the
\(H_{0123}\)-mixing freedom or the three crossing-correction routes
reach the killing words?* — is answered **no**: the certificates live in
the single/double-site flip slice, which that freedom never touches.

### 2.5 What is actually exhaustive: the signature reduction

**The withdrawn claim.**  The first packaging asserted that the six
families \(\{g,x,d\}\times\{6,7\}\) were complete under saturation, via
a "slot dichotomy" excluding degenerate families.  **That is false.**
The audit exhibited saturated U-system solutions outside them: the
extended exchange xf (now swept), a d-variant with a free a-column, and
the solution in which all four residue-adjacent blocks are a-column
only.  No amount of sweeping named families will close that gap.

**What closes it** is that the certificates of §2.3 do not read the
families — they read the **two-colour column signature**
\((P_6,P_7)\), plus (for case 3) the exchange structure.  So the
exhaustive statement needed is about signatures:

> **Signature Lemma.**  Let \((A_{u6},A_{u7},A_{p6},A_{p7})\) satisfy
> (U) with \(A_{u6},A_{u7}\) having zero \(a\)-rows (E1).  If
> \(s_e\ne0\) then the two-colour feeds all go into **one** residue
> site; hence \((P_6,P_7)\) is one of **seven** signatures
> (\(\varnothing\), and \(\{u\},\{p\},\{u,p\}\) into exactly one site).
> Moreover if \(P_r=\{u,p\}\) then the solution has the extended
> exchange structure at \(r\): \(A_{u,r}(\cdot,k)=-c_k\,A_{u,\bar r}
> (\cdot,a)\), \(A_{p,r}(\cdot,k)=c_k\,A_{p,\bar r}(\cdot,a)\) for
> \(k\in\{b,c\}\), with the far blocks' two-colour columns identically
> zero and the a-column of \(A_{u,r}\) free.

*Proof.*  Write \(x_k=A_{u6}(\cdot,k)\), \(y_l=A_{u7}(\cdot,l)\),
\(z_k=A_{p6}(\cdot,k)\), \(w_l=A_{p7}(\cdot,l)\); (U) reads
\(x_k w_l^{T}=-\,y_l z_k^{T}\) for \((k,l)\ne(a,a)\), and
\(s_e=x_a w_a^{T}+y_a z_a^{T}\).

*(both sites, both fed from \(u\)).*  Suppose \(x_k\ne0\) and
\(y_l\ne0\) for some \(k,l\in\{b,c\}\).  If \(z_k=0\), then \((k,l')\)
for every \(l'\) gives \(x_k w_{l'}^{T}=0\), so \(W=0\); then
\((k',l)\) gives \(y_l z_{k'}^{T}=0\) for every \(k'\), so \(Z=0\), and
\(s_e=0\).  Otherwise pick \(j_0\) with \(z_k(j_0)\ne0\).  From
\((k,a)\), \(y_a=c\,x_k\) and \(w_a=-c\,z_k\) with
\(c=-w_a(j_0)/z_k(j_0)\); from \((k,l)\), \(y_l=c'x_k\) and
\(w_l=-c'z_k\) with \(c'=-w_l(j_0)/z_k(j_0)\), and \(c'\ne0\) because
\(y_l\ne0\).  Substituting into \((a,l)\) gives
\(c'\,(x_a z_k^{T}-x_k z_a^{T})=0\), so \(x_a z_k^{T}=x_k z_a^{T}\),
whence \(s_e=c\,(x_k z_a^{T}-x_a z_k^{T})=0\).

*(mixed).*  If \(x_k\ne0\) and \(w_l\ne0\) (\(u\) feeds 6, \(p\) feeds
7) then \((k,l)\) forces \(y_l\ne0\), reducing to the previous case;
symmetrically for \(z_k\ne0,\ y_l\ne0\).

*(both fed from \(p\)).*  If \(u\) feeds neither site — all
\(x_k=y_l=0\) for \(k,l\in\{b,c\}\) — while \(z_k\ne0\) and
\(w_l\ne0\), then \((k,a)\) gives \(y_a z_k^{T}=0\Rightarrow y_a=0\)
and \((a,l)\) gives \(x_a w_l^{T}=0\Rightarrow x_a=0\); so \(s_e=0\).

*(the two-endpoint case).*  Suppose \(P_6=\{u,p\}\) and \(s_e\ne0\).  By
the above, site 7 is unfed: \(y_l=0\) for \(l\in\{b,c\}\), and then
\((k,l)\) gives \(x_k w_l^{T}=0\), so \(w_l=0\) for \(l\in\{b,c\}\).
The remaining relations are \(x_k w_a^{T}=-y_a z_k^{T}\).  If \(y_a=0\)
then \(w_a=0\) and \(s_e=0\); so \(y_a\ne0\), and reading the relation
at a row where \(y_a\) is nonzero gives \(z_k=c_k w_a\), and — since
\(w_a\ne0\), because otherwise \(z_k=0\) for all \(k\in\{b,c\}\),
contradicting \(p\in P_6\) — also \(x_k=-c_k y_a\).  With \(w:=y_a\),
\(q:=w_a\) this is exactly the extended exchange pattern, the a-column
\(x_a\) remaining free. \(\square\)

**Machine evidence (one finite field).**  The checker enumerates
**every** solution of (U) over \(\mathrm{GF}(2)\) — 82 086 solutions
reached, of which **28 350 are saturated** — and finds:

~~~text
saturated solutions feeding BOTH residue sites : 0
realizable two-colour column signatures        : 7
  [[], []]           1890     (all four blocks a-column only)
  [['u'], []]        1530     [[], ['u']]        1530
  [['p'], []]       10080     [[], ['p']]       10080
  [['p','u'], []]    1620     [[], ['p','u']]    1620
solutions with a two-endpoint signature lacking
  the extended exchange structure               : 0
~~~

This is a **census over \(\mathrm{GF}(2)\)**, i.e. verified on one
finite field — evidence for the Signature Lemma, not a proof of it; the
proof above is the hand argument.  Controls: the GF(2) nullspace routine
is checked on designed systems (empty, rank-2, full rank); each of the
five designed family instances (g6, d6, x6, xf6, and the empty-signature
solution) is required to be a saturated U-solution — via a *second*,
direct-substitution implementation of (U) — with the signature the sweep
assigns to it, and to appear in the census; and the signature classifier
is required to flag a designed both-sites packet (so the zero count is
the census's finding, not a blind classifier).

**What this licenses.**  Anchor death and the \(\Gamma\)-certificate are
support-level facts depending only on the signature; the c-factor
certificate applies to *every* two-endpoint solution by the Signature
Lemma.  So the three certificates cover every saturated U-system
solution profile — while the 512-combination sweep verifies the
underlying polynomial identities on the eight named families.  The
residual gap is exactly this: the identities are verified on the swept
families, and extended to the rest by the (hand-proved) structural
statement, not by machine.

### 2.6 Caveats, stated precisely

1. **Family exhaustiveness is withdrawn** (§2.5).  The sweep covers
   eight named families; the extension to all saturated U-system
   solutions runs through the Signature Lemma (hand proof + GF(2)
   census), not through enumeration of families.
2. **Orientation.**  The badness orientation is fixed at the essential
   sites \(\{0,1,3\}\).  Re-orienting a carrier moves only (E1)'s
   a-row support; the three certificates read **only two-colour cells**,
   so they should be undisturbed.  This is an **inspection, not
   machine-verified**, and nothing in the checker would notice if it
   were wrong.
3. **One representative family.**  The checker sweeps one of the
   census's 48 families of signature \((3,2,2)\).  Its orbit under the
   split-preserving relabelling group \(S_2\times S_2\times S_4\)
   (order 96) is **machine-verified to be all 48** (with a negative
   control: the \(S_a\)-trivial subgroup reaches only 4).  **But the
   orbit alone does not license sweeping one representative**: that
   step also needs the D2 skeleton and the three certificates to be
   *equivariant* under the relabelling, which is an **unverified
   inspection**.  If equivariance failed, the sweep would cover one
   family and not the other 47.
4. **Conditional on the census.**  D2 is *a configuration of the census
   reduction*; killing it is only meaningful modulo that reduction —
   whose note and checker are **untracked in git** (see the header).

**Conclusion (Theorem 1).**  Under 1–4, no exact \(N=8\) source has a
saturating family of configuration D2 with the swept branch structure.
Combined with the census: **D1 is the sole surviving \(N=8\)
configuration.**

---

## 3. Theorem 2 — monochromatic rigidity on \(\Sigma\)

**The class.**  \(\Sigma\) is the a-column support class of the D1
geometry:

* small–small blocks (\(u,v\in\{0,1,2,3\}\)): arbitrary subject to the
  (E1) pendant rows (row \(a\) of \(A_{0x}\) zero for \(x\ne2\), of
  \(A_{1x}\) zero for \(x\ne3\));
* small–residue blocks \(A_{pr}\): **a-column only**
  (\(A_{pr}(\cdot,b)=A_{pr}(\cdot,c)=0\));
* residue–residue blocks: **\((a,a)\) cell only** — all six, not just
  the matching \(\{45,67\}\).

That is 89 free cells.  \(\Sigma\) contains the pinned-rectangle witness
and the entire near-miss family of §4.

**Theorem 2.**  \(H_B(b^8)=H_B(c^8)=0\) identically on \(\Sigma\).

*Proof (structural).*  Each of the 105 perfect matchings of 8 sites
contains at least two residue-incident edges (there are four residue
sites, so at least two edges touch them).  A residue-incident edge is
either residue–residue, whose \((b,b)\) and \((c,c)\) cells vanish on
\(\Sigma\), or small–residue, whose residue-side \(b\)- and
\(c\)-columns vanish.  Either way every matching term of \(H_B(b^8)\)
and \(H_B(c^8)\) contains a zero factor. \(\square\)

*Machine content.*  The minimum residue-incidence over all 105 matchings
is computed (\(\ge2\)), and the identity is verified **as a polynomial
identity** with an independent variable in each of the 89 free cells —
not on sampled points.  Controls:

* the incidence scan must be able to fail: run with a *single*
  designated residue site it reports a matching with fewer than two
  incident edges (so the scan reads the residue set it is given);
* non-degeneracy: the probe word \((b,b,c,c,a^4)\) is a nonzero
  polynomial on \(\Sigma\) (all 105 monomials survive), so the anchor
  statement is not vacuous;
* the committed `coefficient` oracle agrees on an instantiated
  \(\Sigma\) packet — anchors zero, probe word equal to the
  polynomial's value.

**Sharpness / negative probes.**  Reviving *one* residue–residue
two-colour cell \(A_{45}(b,b)\) leaves the anchor **identically zero**
(the parity fact: the crossing edges pair up, and sites 6, 7 still have
to be matched through dead cells).  Reviving **two disjoint** ones
\(A_{45}(b,b), A_{67}(b,b)\) revives it.  So the rigidity test is not
blind to out-of-\(\Sigma\) supports, and the escape route is precisely
"two disjoint revived residue-side two-colour cells", not one.

**Consequence.**  Any D1-route counterexample must leave \(\Sigma\): some
residue-side \(b/c\) cell must be nonzero — which re-activates the
residue-impure word classes and the Lemma-F purity system.

---

## 4. The near-miss family: 6559/6561, and why the anchors are the wall

### 4.1 The defect profile that set the aim

The pinned-rectangle witness (attack map §25c; the checker rebuilds it
for §4.3) satisfies every census fact of the D1 configuration.  Its
defect profile over all 6561 words — 6523 satisfied *identically*, i.e.
with no dependence on the free coordinates, 36 two-carrier core words
violated, plus \(b^8,c^8\) — is **cited** from the scratch profile run
and is not re-verified here; only the 36 live core words it points at
are recomputed (§4.3, where they are required to be exactly the words
with both essential sites two-coloured).  The repair programme was
therefore: fix the 36 core words, then see what is left.

### 4.2 The family (machine, on instances)

The closed-form repair uses cross-class proportionality
(\(c_p(\cdot,6)=s\,c_p(\cdot,4)\), \(c_p(\cdot,7)=s\mu\,c_p(\cdot,5)\))
plus carrier-site collinearity (\(c_0(\cdot,5)=\rho\,c_0(\cdot,4)\),
\(c_1(\cdot,5)=\rho'\,c_1(\cdot,4)\)), which makes the grouped
two-carrier system rank-\((1,1)\) and solvable in closed form.  The
checker builds the resulting packet in exact rationals and verifies, on
the **committed** oracles:

* **every census fact** — Lemma-F purity of \(H_{W_1}, H_{W_2}\) over
  all \(2\times729\) words; residue purity over all 81; (E1) at both
  essential endpoints; (E2) carrier nonvanishing; badness of both
  carriers; the a-pendant hafnian facts on *every* even subset;
  liveness \((h_a,h_b,h_c)=(1,-14,28)\); identity (dagger) at both
  carriers, nonvacuously;
* **6559 of the 6561 exactness equations**, the defect set being
  exactly \(\{b^8,c^8\}\) with (got, want) \(=(0,1)\);
* the same at a **second generic parameter point** (so this is a
  family, not a point);
* a **harmful member**: setting \(c_3(\cdot,5)_2=-61/27\) and the gauge
  \(t_1=5\) keeps every census fact and the 6559/6561 defect set while
  making the D1 rectangle degenerate — both products equal \(100/3\),
  i.e. \(A_{02}(b,c)A_{13}(b,c)=A_{01}(b,b)A_{23}(c,c)\ne0\), the exact
  harmful condition of census eq. (2).  (At the base point the rectangle
  is \(90\) vs \(-392\): non-degenerate, so the harmful point is a
  distinguished member, not the generic one.)
* **local dimension \(\ge22\)**: the exact Jacobian of the 22-parameter
  chart at the base point, computed with dual numbers over `Fraction`
  (no floating point), has rank **22**.  This is a *lower* bound on the
  dimension of the surviving variety — 22 is the rank of the chart, not
  a claim that the variety is exactly 22-dimensional.  Controls: the
  plain-dict replication must reproduce the swept construction cell by
  cell; the committed rank routine is exercised on seven designed
  matrices covering its branches (empty, all-zero, zero column before a
  pivot, repeated rows, full square, wide, rational); duplicating a
  Jacobian row must drop the rank to 21.

Controls on the sweep itself: perturbing one cell of the packet must
**enlarge** the defect set (it grows from 2 to 11), and the census-fact
checker must **reject** a designed (E2) violation.

The nonzero cells of the three witness packets are recorded in the
frozen ledger: **77** at the base point, **71** at the second generic
point, **77** at the harmful point.

### 4.3 Why the full chart was needed: the frozen-chart pencil is infeasible

Freeze the witness's carrier and carrier-to-residue data, leaving only
the 25 cross-block cells \(A_{01},A_{23},A_{03},A_{12}\) free.  Exact
finite differences through the committed oracle turn each of the 81 core
words into

\[
  V_1(x_0,x_1)V_2(x_2,x_3)+V_3(x_0,x_3)V_4(x_1,x_2)+K(x)=0 ,
\]

with \(V_i = A_i + B_i\) and \(K\) fixed rationals.  The checker
*requires* the structure it uses: each word is affine in each single
cell (no pure squares), the quadratic part is exactly
\(A_{01}A_{23}+A_{03}A_{12}\) with unit coefficients, the four
residue-completion tables \(B\) are well defined, exactly 36 words are
live, and every non-live core word is identically satisfied by the
witness.  All four \(K_{x_0x_1}\) have rank 3.

Eliminating \(V_2\) between two blocks sharing an index forces
\(\operatorname{rank}(K_X-sK_Y)\le1\) at \(s=V_1(X)/V_1(Y)\), i.e. all
nine \(2\times2\) minors of the pencil vanish at one \(s\).  For **all
four** sharing pairs — \(bc/bb\), \(cb/bb\), \(cc/cb\), \(cc/bc\) — the
gcd of the nine minor polynomials over \(\mathbb{Q}\) is the constant
\(1\): **no \(s\in\overline{\mathbb{Q}}\) works**, so the frozen-chart
repair is impossible.  (The checker requires *all four*, matching this
sentence.)  Controls: designed gcd cases (common factor, coprimality,
exact division) and a designed *feasible* pencil \(A=2B+(\text{rank
one})\), whose minor gcd must come out nonconstant — otherwise the
verdict could not distinguish the two cases.

**Reading.**  The two-carrier core words are repairable, but only by
moving the whole chart; and no amount of that repair touches the
anchors, which §3 shows are identically dead on the entire support
class the family lives in.  The census fact set plus two-colour repairs
**cannot decide D1** — the decision must come from out-of-\(\Sigma\)
supports.

---

## 5. The \(N=8\) endgame state

* **D2: dead** on the swept class (§2), modulo the caveats of §2.6 —
  in particular the unverified equivariance step — and the census
  reduction itself.
* **D1: alive only out of \(\Sigma\).**  Within D1, the killing family
  is the **monochromatic pair** \(b^8,c^8\), not the two-colour words —
  those are all repairable, and were repaired (§4).  On \(\Sigma\) the
  pair is rigidly unsatisfiable (§3).  So a D1 counterexample needs a
  residue-side \(b/c\) cell, i.e. a support that leaves \(\Sigma\),
  where the Lemma-F purity system couples the carriers.
* **Two independent lanes converged on that same cell**: the branch
  engine (D2 sweep and the D1 stratum work) and the counterexample hunt
  reached it from opposite directions.
* **Krenn's conjecture remains OPEN**, and the near-miss family is
  definitively *not* exact — it fails exactly two equations.

---

## 6. D1 status

**[PLACEHOLDER — classification sweep in progress at packaging time.]**

The D1 lane has advanced past what this artifact verifies, in scratch
work that is **not committed and not verified here** (attack map §25d,
§25g; cited only): the double-pure inside stratum is reported fully
killed (the non-degenerate locus of 1296 crossing-branch combinations
dying harm-free, and a census over all 9216 harm-legal degenerate
combinations with zero unresolved), a machine lemma R3
(\(\det(a\otimes b+c\otimes d)=0\)) is reported to reduce every inside
stratum with an invertible pair-block to the same U-system machinery
that killed D2, and the surviving D1 cell is reported to be exactly

> (non-double-pure inside strata) \(\times\) (out-of-\(\Sigma\)
> crossing supports),

with an agent extracting that cell's variety data.  Every certificate
found in that work anchors on the **monochromatic pair**, which is the
independent confirmation of §3's aim.  Note that the audit which
corrected this artifact has not examined that work, and the
family-completeness failure it found here (§2.5) applies *a fortiori*
to the degenerate-locus census quoted above, which is family-indexed:
those tallies should be read as covering their named families, not as
covering the strata.

This section will be amended with the outcome — and, if it lands, §5's
"D1: alive" line and the companion census note's §8 will be relabelled —
before or at the time that work is packaged.  **Nothing in §§2–4 depends
on it.**

---

## 7. Scope

1. §2 and §3 are statements about *support classes*: they say that no
   exact source has the stated support structure.  They are exact
   polynomial-identity facts, but they consume hand-proved committed
   inputs (Lemma F, Theorem C, Corollaries C2–C3) and the hand
   arguments of §2.5–2.6 — including two steps (equivariance,
   orientation inertness) that are **not machine verified at all**.
2. §4 is *verified on instances*: explicit rational packets, checked
   against the committed oracles.  A family passing 6559/6561 equations
   is not an exact source, and no claim is made that the remaining two
   can be repaired — §3 proves they cannot be, on that support class.
3. The census reduction to D1 and D2 is **cited** from the companion
   artifact, which is **untracked in git**: not committed, and its
   independent audit has not landed.  The placeholder in its §8 is
   where this note's Theorem 1 will land.
4. Exhaustiveness statements are precise where they are made: 512
   combinations of eight named families over three carriers on **one**
   census D2 family, whose relabelling orbit covers all 48 (modulo
   caveat §2.6.3); 105 matchings; 89 \(\Sigma\)-cells; 6561 words; 81
   core words with 36 live; 82 086 GF(2) U-solutions of which 28 350
   are saturated.  Nothing is claimed to be exhaustive over exact
   sources, supports, or splits beyond those.
5. Everything at \(N\ge10\) is untouched.
6. Per project discipline this is a research reduction until
   independently audited.  The first audit returned FAIL on the claims
   listed in the audit-history section above; this version corrects
   them and has **not** itself been re-audited.  **Krenn's conjecture
   remains open.**

---

## 8. Verification

~~~text
python3       computations/verify_n8_d2_kill_and_monochrome_rigidity.py
python3 -O    computations/verify_n8_d2_kill_and_monochrome_rigidity.py
python3 -I    computations/verify_n8_d2_kill_and_monochrome_rigidity.py
python3 -S    computations/verify_n8_d2_kill_and_monochrome_rigidity.py
python3 -I -S computations/verify_n8_d2_kill_and_monochrome_rigidity.py
python3 -m py_compile computations/verify_n8_d2_kill_and_monochrome_rigidity.py
~~~

Runtime is about **7–11 seconds** in every mode, depending on machine
load (the 512-combination polynomial sweep 2–3.5 s, the GF(2) U-system
census 0.3–0.6 s, the three 6561-word exactness sweeps of §4 4–6.5 s).
There is no
solver section and no external dependency: exact stdlib `int`/`Fraction`
only, plus a sparse multivariate polynomial ring and a GF(2) bitmask
nullspace routine built in the checker.  (`python3 -I` does not prepend
the script's directory; the checker inserts its own directory, computed
from `__file__`, before importing the committed companions, and
**pins** their digests — see the ledger's `conventions` block — so it
refuses to run against drifted committed artifacts.)

**Ledger.**  One frozen digest, hashing content through the committed
`content_hash` (exact values, `Fraction`s as tagged strings).  Every
entry is a *computed* value — polynomial fingerprints, tallies read off
the sweep, enumerated censuses, exact tensor entries; the two literals
the audit found (a hard-coded monomial count and four `True` probe
flags) have been replaced by the computed quantities they stood for.
The ledger records: the pinned committed digests and convention probes;
the canonical split, the \(\chi\) word induced by it, the computed
budget size, the swept D2 representative and its relabelling orbit
sizes, the D1 families and residues; the ring validation; **all 512
branch verdicts** with their certificate data (unique partner /
exchange carrier, the exact certificate words, the \(\Gamma\)-tensor
fingerprints) and both anchor polynomial fingerprints per combination;
the 1536 slot \((\dagger)\)-numerator and crossing-cell fingerprints;
the feeder distribution and pigeonhole tallies; the 30 distinct
certificate words; the GF(2) U-system census (enumerated, saturated and
both-sites counts, the seven-class signature census with
multiplicities, the designed family signatures); \(\Sigma\)'s free-cell
count, incidence minima and the anchor / probe / one-cell / two-cell
polynomial fingerprints; the rank-routine control table and the
dual-number probe; the near-miss family's liveness, defect sets at three
parameter points, rectangles, Jacobian rank and fingerprint, and the
three witness tensors with their cell counts (77 / 71 / 77); and the
frozen chart's \(K\) table, completion tables, block ranks, the four
pencil minor gcds and the control pencil's gcd degree.  A polynomial
"fingerprint" is the pair (number of monomials, value at a deterministic
rational probe point) — computed content; **no property is decided by a
fingerprint**, every property is decided by exact polynomial identity.

~~~text
exact ledger : d8e8ad7ace2e31e16ef0dfa64f0f7d31a7064dcb701503c46d8a7a5abc58e737
~~~

**In-run designed probes** (positive *and* negative, per property):
N1 the \(\Gamma\)-certificate must **refuse** on a designed
non-factoring packet (a second two-colour partner injected at residue
site 7); N2 the c-factor certificate must **refuse** when the exchange
rank-1 pattern is broken; N3 anchor death must **disappear** when a free
two-colour block is added at the starved residue site (and exactly the
one anchor revives); N4 a designed degenerate slot must have
\(s_e\equiv0\) while carrying a live a-column cell (so its vanishing is
not vacuous); the five designed U-system family instances and the
both-sites classifier probe (§2.5); plus the \(\Sigma\) one-cell /
two-cell revivals, the defect-sweep perturbation, the census-fact
rejection, the rank and gcd control tables and the designed feasible
pencil.

**Mutation-tested with ten injections, six of them
fabricated-geometry.  All ten raise under both `python3` and
`python3 -O`, with the same message, naming the broken property.**

| # | injection | message raised |
|---|---|---|
| MU1 | **(fabricated geometry)** a second two-colour partner injected into the g-branch's zero residue block | D2 pigeonhole: combo 02:g6,14:g6,35:g6 starves residue site [7] of two-colour feeders, yet an anchor is not identically zero |
| MU2 | **(fabricated geometry)** the exchange rank-1 pattern broken at the partner block | D2 sweep: 192 of the 512 branch combinations survived every certificate, so D2 is NOT killed on the swept class |
| MU3 | **(fabricated geometry)** the residue–residue block \(A_{67}\) given a two-colour cell | D2 pigeonhole: combo 02:g6,14:g6,35:g6 starves residue site [7] of two-colour feeders, yet an anchor is not identically zero |
| MU4 | **(fabricated geometry)** \(\Sigma\) widened by a \((b,b)\) cell on every residue–residue block | rigidity: H_B(b^8) is not identically zero on Sigma, so the monochromatic equations are not rigid there |
| MU5 | **(fabricated geometry)** the near-miss family's residue-internal cell \(A_{45}(a,a)\) changed from 1 to 3 | stage-A base point: Lemma-F purity of H_[0, 2, 4, 5, 6, 7] fails at (0, 0, 2, 2, 2, 2) (got -2) |
| MU6 | the pinned digest of a committed companion altered | pinned committed artifact verify_exact_source_live_split_forcing.py changed (sha256 …): the conventions or theorems this checker consumes may have drifted, so it refuses to run |
| MU7 | frozen exact ledger digest altered | n8 D2 kill and monochrome rigidity ledger changed |
| MU8 | **(fabricated geometry)** the extended exchange families collapsed back to the plain ones (the free a-column of \(A_{u,keep}\) removed) | n8 D2 kill and monochrome rigidity ledger changed |
| MU9 | one U-relation family dropped from the GF(2) census (the \((k,a)\) relations) | U-system census: 629370 saturated solutions feed two-colour cells into BOTH residue sites, so the pigeonhole the certificates rest on is not forced by the U-system |
| MU10 | the \(\chi\) word decoupled from the canonical split | geometry: the colour word chi = [0, 0, 0, 1, 2, 2, 2, 2] is not the word induced by the canonical split through the committed part_map ([0, 0, 1, 1, 2, 2, 2, 2]) |

MU1 and MU3 are caught *upstream* of the certificate stage, by the
pigeonhole cross-check, which is why the \(\Gamma\)-certificate's own
refusal is exercised separately, in-run, by probe N1.  **MU8 is caught
only by the ledger digest** — the tallies and verdicts are unchanged by
it, since xf and x are classified alike; the slot fingerprints and the
family list are what move.  That is precisely the hole the audit found
in the first packaging (where the omission of xf was invisible), and it
is now at least *visible*: the sweep's coverage is recorded in hashed,
computed content rather than asserted in prose.
