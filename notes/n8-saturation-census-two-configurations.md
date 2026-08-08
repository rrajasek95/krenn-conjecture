# The N = 8 saturation census: Lemma H, identity (dagger), and the two surviving configurations

Checker:
[`computations/verify_n8_saturation_census_two_configurations.py`](../computations/verify_n8_saturation_census_two_configurations.py).

This note reduces the saturating gap of Theorem C — the one obstacle the
good-crossing cluster left standing at \(N=8\) — to **two explicit scalar
configurations**, D1 and D2, on a single split shape.  All conventions,
notation and cited results (Lemma 0, Theorems A/B, Lemma E with
(E1)–(E3), Lemma F, Lemma G, Theorem C, Corollaries C1–C3, the stall
guard) are those of
[`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md)
and
[`notes/good-crossing-matching-forcing.md`](good-crossing-matching-forcing.md);
the checker **imports** both committed checkers rather than
re-implementing anything, re-derives the endpoint-order and hafnian
conventions from scratch as probes, and **pins the sha256 digest of
every committed artifact it consumes or cites**, so upstream drift is a
loud failure here rather than a silent change of meaning.

**Model.**  Sites carry endpoint-ordered aggregate blocks \(A_{uv}\) with
cells \(A_{uv}(i,j)\), \(i\) read at \(u\) and \(j\) at \(v\); exactness
is \(H_B(A)=\Delta_{B,3}\) over \(\mathbb C\).  This note works in the
**GENERAL (bicoloured) model**, where \(A_{uv}(i,j)\ne0\) is permitted for
\(i\ne j\) — the model of the open case \(N=8,d=3\) (DeepMind's Lean
`eqSystem8_no_solution_d3`, research open; see
[`references/REFERENCES.md`](../references/REFERENCES.md)), **not** the
monochromatic-edge restriction.  Diagonal results quoted here are used
only as necessary conditions on the diagonal shadow of a general source.

**Status.**  Lemma H and identity (dagger) are *hand proofs* consuming
only committed Lemma F and Corollaries C2–C3, *verified on instances*
(constructed (E1)–(E3) packets, pseudorandom packets, the exact \(K_4\)
source, both committed guards).  The census and the D1/D2 geometry are
*exhaustive machine facts* over all ordered even splits at
\(N=6,8,10\).  The D1/D2 harmful conditions are *hand derivations* from
Theorem C (committed) plus the census, with their scalar shapes probed
positively and negatively.  The strengthened-SAT verdicts are *machine
facts in the weak (SAT) direction* — support-level survivors, not
theorems.  The companion
[`n8-d2-kill-and-monochrome-rigidity.md`](n8-d2-kill-and-monochrome-rigidity.md)
kills D2 on a swept branch class (subject to its explicit equivariance,
orientation and census caveats) and kills D1 on the support class
\(\Sigma\); the residual out-of-\(\Sigma\) D1 cell remains open.  The
drop-\((0,2,6)\) UNSAT theorem is **cited as committed**
(commit `1bbb4d9`,
[`notes/diagonal-termwise-census-and-pencil-guard.md`](diagonal-termwise-census-and-pencil-guard.md)
§6).  A complete ruling-out of D1 and D2 on an exact source remains
**open**.
**Krenn's conjecture remains open.**

---

## 0. Summary of outcomes

* **Lemma H (empty-residue collapse; proved).**  A saturating family
  whose residue \(R=B\setminus V(F_a)\) is *empty* contributes nothing:
  every one of its carriers has \(A_e(\chi)=0\), so Theorem C's
  correction vanishes identically and Corollary C1 holds anyway.
* **Identity (dagger; proved).**  The general-residue form of the same
  mechanism: \(A_e(\chi)\,h_a(R)\) equals an explicit sum over pairs of
  residue sites.  Lemma H is its case \(R=\varnothing\).
* **The census (exhaustive machine fact).**  Classifying, over *all*
  ordered even splits at \(N=6,8,10\), which \((\)shape\(,|S_a|)\) can
  carry a saturating family with **nonempty** residue — the only ones
  Lemma H leaves open — shows that at \(N=8\), after the committed
  drop-\((0,2,6)\) UNSAT theorem, exactly **two** configurations
  survive, both on shape \((2,2,4)\) with the saturating colour on the
  4-part: **D1** \((k,|R|,t)=(2,4,0)\) and **D2** \((3,2,2)\).  At
  \(N=10\) every shape is dangerous: the reduction is
  **\(N=8\)-specific**.
* **The scalar forms (hand derivations).**  D1 is harmful iff one
  literal source-block **minor** vanishes with both sides nonzero — the
  same minor shape as eq. (3) of
  [`notes/unconditional-curvature-line-selection.md`](unconditional-curvature-line-selection.md);
  D2 is harmful iff one explicit product identity holds.
* **The Boolean route is dead (SAT, weak direction).**  Loading *all*
  of Lemma F's residue purity, the carrier nonvanishing and the
  \(a\)-pendant support facts into the shape-restricted engine leaves
  the instance **SAT** (73 548 variables, 6 101 916 clauses), and still
  SAT with D2 disabled.  Disabling both options restores the committed
  drop-\((0,2,6)\) **UNSAT**, as an in-run cross-check.  What remains
  in D1 and D2 is **scalar**, not support-theoretic.
* **Consistency (required, not assumed).**  The committed stall guard
  satisfies everything Lemma H's proof consumes and escapes it *purely*
  on its residue count \(|R|=2\); its configuration, computed from its
  blocks, must equal the abstract census entry.  \(K_4\) (exact, no
  live split) and the omega guard (live splits, no bad crossing pair)
  are the vacuity controls.

---

## 1. Lemma H — the empty-residue collapse

**Lemma H (proved).**  Let \(A\) be an exact ternary source on \(B\),
\((S_0,S_1,S_2)\) a live split with colouring \(\chi\), and \(F_a\) a
saturating family of Theorem C — by Corollary C3 it is the whole
colour-\(a\) class of bad crossing pairs, and
\(B\setminus V(F_a)\subseteq S_a\).  If \(V(F_a)=B\), then
\(A_e(\chi)=0\) for **every** \(e\in F_a\); consequently the saturating
correction of Theorem C vanishes identically and Corollary C1's
conclusion (a nonzero crossing matching all of whose crossing edges are
good) holds unconditionally for this family.

*Proof.*  By Corollary C2, \(|F_a|\ge2\), so
\(T'=F_a\setminus\{e\}\) is a *nonempty* family of pairwise disjoint
bad pairs of the single essential colour \(a\).  Lemma F (equal-colour
branch) gives \(H_{B\setminus V(T')}=\nu'e_a^{\otimes}\) with
\(\nu'\ne0\).  But \(V(F_a)=B\) means
\(B\setminus V(T')=e=\{u,v\}\), and on two sites
\(H_{\{u,v\}}(i,j)=A_{uv}(i,j)\).  Hence \(A_{uv}=\nu'E_{aa}\).  The
pair is crossing, so \(\chi_u\ne\chi_v\), in particular
\((\chi_u,\chi_v)\ne(a,a)\): \(A_e(\chi)=0\).  \(\square\)

**Verified nonvacuously**: on chain packets at \((N,k)=(8,4)\) (two
\(\lambda\)-vectors) and \((6,3)\), all with
\(\prod_i\lambda_i=1\) so the family covers \(B\).  For every carrier
the checker *computes* (E1), (E2), (E3) from the blocks; recomputes the
Lemma-F step the proof consumes (dropping one carrier leaves exactly
that carrier's two sites, whose tensor must equal the **pure**
\(\nu E_{aa}\) with the predicted **nonzero**
\(\nu=\prod_{j\ne i}\lambda_j^{-1}\)); and sweeps all **six** crossing
cells of the carrier block to zero — 11 carrier instances, all
nonvacuous (\(\nu\in\{2,3,-1,-\frac16,-5,1,-\frac1{10},-2\}\), recorded
in the ledger).  A detector control perturbs one crossing cell of a
fresh carrier block and requires the sweep to *see* it, so the six-zero
check cannot pass by reading the wrong block.  Where the empty-residue
*hypothesis* is load-bearing the chain packets cannot show (they build
pure carrier blocks by hand even at \(2k<N\)); the witness is the
**stall guard** (§6): \(|R|=2\), (E1)–(E3) hold, and the carrier
crossing cells are **nonzero** — required there, not assumed.

---

## 2. Identity (dagger) — the general-residue form

**Identity (dagger) (proved).**  With the hypotheses of Lemma H but
\(R=B\setminus V(F_a)\) arbitrary, for every carrier
\(e=\{u,v\}\in F_a\):

\[
 A_e(\chi)\,h_a(R)\;=\;-\!\!\sum_{\substack{r,r'\in R\\ r\ne r'}}
   A_{ur}(\chi_u,a)\,A_{vr'}(\chi_v,a)\,
   h_a\bigl(R\setminus\{r,r'\}\bigr).                          \tag{1}
\]

*Proof.*  Lemma F on \(T'=F_a\setminus\{e\}\) gives
\(H_{R\cup e}=\nu'e_a^{\otimes}\).  Evaluate at the word (\(\chi\) on
\(e\), \(a\) on \(R\)): the word is impure because the pair is
crossing, so the value is \(0\).  Expanding the \((2+|R|)\)-site
matching sum by the partners of \(u\) and \(v\): the terms pairing
\(u\) with \(v\) total \(A_e(\chi)h_a(R)\), and the terms pairing
\(u\) with \(r\in R\) and \(v\) with \(r'\ne r\) total the right-hand
sum.  \(\square\)  Lemma H is the case \(R=\varnothing\) (the empty sum).

**Verified where it has content.**  The underlying expansion — for
*any* packet, prior to any purity —

\[
 H_{R\cup\{u,v\}}(\chi_u,\chi_v,a^{|R|})
 =A_{uv}(\chi_u,\chi_v)h_a(R)
 +\!\!\sum_{r\ne r'}A_{ur}(\chi_u,a)A_{vr'}(\chi_v,a)
   h_a(R\setminus\{r,r'\})
\]

is checked on pseudorandom packets at \(|R|=0,2,4,6\): 16 instances,
14 of them nonvacuous, **8 with a sub-hafnian
\(h_a(R\setminus\{r,r'\})\ne1\)**.  The \(|R|\ge4\) instances are
**required** — on \(|R|\le2\) every sub-hafnian is the empty hafnian
\(1\), so the factor is invisible there.  (An early scratch draft of
this artifact checked only \(|R|\le2\); the mutation dropping the
sub-hafnian factor was **silent**.  It is now caught twice over: the
checker requires \(\ge4\) instances with a nontrivial sub-hafnian, and
an in-run sharpness probe requires that replacing every sub-hafnian by
\(1\) actually changes the expansion on \(\ge4\) instances.)  Identity
(1) itself is verified nonvacuously on the stall guard at **both**
carriers (\(-1=-1\), both sides nonzero) and degenerately (\(0=0\), as
proved) at all 11 empty-residue carrier instances of §1.

---

## 3. The census: what can saturate, exhaustively

**What is enumerated (exhaustiveness convention).**  For every even
\(N\in\{6,8,10\}\): every **ordered** even split \((S_0,S_1,S_2)\) of
\(\{0,\dots,N-1\}\) produced by the committed `even_splits` (all
\(3^N\) colourings with all three parts even, the constant colourings
excluded — empty parts allowed), every colour \(a\), and every nonempty
matching \(T\) inside the split's **crossing pairs**.  \(T\) is counted
when \(B\setminus V(T)\subseteq S_a\), and classified by

\[
 (k,|R|,t)=\bigl(|T|,\;|B\setminus V(T)|,\;
 \#\{e\in T: e\cap S_a\ne\varnothing\}\bigr)
\]

under the key (sorted shape, \(|S_a|\)).  This is the **combinatorial
envelope** of Theorem C's saturating families: by Corollary C3 an
actual saturating family on an exact source *is* such a \(T\) (namely
the whole class \(F_a\)), so every \((\)shape\(,|S_a|)\) the census
clears carries no saturating family on **any** exact source; the
census does *not* assert that a listed configuration is realizable.
A configuration is **dangerous** iff \(|R|>0\) — Lemma H kills the
rest.

**The tables (computed; the ledger hashes them).**

| \(N\) | shape, \(|S_a|\) | all \((k,|R|,t)\) | dangerous |
|---|---|---|---|
| 6 | \((0,2,4)\), 4 | \((2,2,2)\) | \((2,2,2)\) — the stall guard |
| 6 | \((2,2,2)\), 2 | \((2,2,0)\), \((3,0,2)\) | \((2,2,0)\) |
| 8 | \((0,2,6)\), 6 | \((2,4,2)\) | \((2,4,2)\) — shape excluded by the committed drop-\((0,2,6)\) UNSAT |
| 8 | \((0,4,4)\), 0 | \((4,0,0)\) | — |
| 8 | \((0,4,4)\), 4 | \((4,0,4)\) | — |
| 8 | \((2,2,4)\), 2 | \((4,0,2)\) | — |
| 8 | \((2,2,4)\), 4 | \((2,4,0)\), \((3,2,2)\), \((4,0,4)\) | **\((2,4,0)=\) D1, \((3,2,2)=\) D2** |
| 10 | \((0,2,8)\), 8 | \((2,6,2)\) | \((2,6,2)\) |
| 10 | \((0,4,6)\), 6 | \((4,2,4)\) | \((4,2,4)\) |
| 10 | \((2,2,6)\), 6 | \((2,6,0)\), \((3,4,2)\), \((4,2,4)\) | all three |
| 10 | \((2,4,4)\), 2 | \((4,2,0)\), \((5,0,2)\) | \((4,2,0)\) |
| 10 | \((2,4,4)\), 4 | \((4,2,2)\), \((5,0,4)\) | \((4,2,2)\) |

The checker requires each \(N=8\) line exactly, requires the total of
7 configurations at \(N=8\) (so the clearing requirements cannot hold
vacuously on an emptied census), and requires that at \(N=10\)
**every** shape has a dangerous configuration — the reduction below is
\(N=8\)-specific and the artifact refuses to overstate it.  \(N=6\) is
vacuous for the conjecture
([`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md),
cited, not re-run) but not for consistency: the stall guard lives
there (§6).

**The geometry (canonical split \(S_b=\{0,1\}\), \(S_c=\{2,3\}\),
\(S_a=\{4,5,6,7\}\); computed and hashed).**

* **D1** \((2,4,0)\): the families are **exactly** the two perfect
  matchings between the two 2-parts,
  \(\{\{0,2\},\{1,3\}\}\) and \(\{\{0,3\},\{1,2\}\}\); the residue is
  the whole 4-part.
* **D2** \((3,2,2)\): **48** families — one 2-part-to-2-part carrier
  (4 choices), the two uncovered outside sites matched into
  \(S_a\) (12 attachments) — each with exactly one
  \(S_b\)–\(S_c\) edge, two \(S_a\)-to-outside edges, and residue a
  2-subset of \(S_a\).
* The empty-residue class \((4,0,4)\) and the \(|S_a|=2\) classes
  \((4,0,2)\) are recomputed as the perfect crossing matchings Lemma H
  disposes of.

The census, the geometry and the controls all run through a **single**
enumeration path (`saturating_families`); its positive/negative control
requires the explicitly named family \(\{\{0,2\},\{1,3\}\}\) to be
found and the explicitly named non-covering matching \(\{\{0,2\}\}\) to
be rejected, and the stall guard supplies a second, independent path
(§6).

---

## 4. The scalar forms of D1 and D2

Fix an exact source with live split of shape \((2,2,4)\),
\(S_b=\{p_1,p_2\}\), \(S_c=\{q_1,q_2\}\), \(S_a\) the 4-part, and
suppose colour \(a\) saturates (Corollary C3: \(F_a\) covers
\(B\setminus S_a\)).  By Lemma H and the census, the *only* possibly
nonzero corrections in Theorem C's identity (4) are the D1/D2 families
of §3; by Corollary C3 there is at most one family per colour, and the
other two colours' families (if they exist) have empty residue, hence
vanish.

**D1 (hand derivation).**  \(F_a=\{e_1,e_2\}\) a perfect matching
between the 2-parts, \(e_i=\{p_i,q_{\sigma(i)}\}\); relabel so
\(\sigma=\mathrm{id}\).  The correction is
\((-1)^2A_{e_1}(\chi)A_{e_2}(\chi)h_a(S_a)\), and the two-site hafnians
are single cells: \(h_b(S_b)=A_{p_1p_2}(b,b)\),
\(h_c(S_c)=A_{q_1q_2}(c,c)\).  Since the split is live,
\(h_a(S_a)\ne0\), and the corrected crossing sum vanishes **iff**

\[
 \boxed{\;A_{p_1q_1}(b,c)\,A_{p_2q_2}(b,c)
   \;=\;A_{p_1p_2}(b,b)\,A_{q_1q_2}(c,c)\;}                    \tag{2}
\]

— in which case liveness makes **both sides nonzero**.  Equation (2)
is *literally* one source-block minor of
[`notes/unconditional-curvature-line-selection.md`](unconditional-curvature-line-selection.md)
eq. (3) vanishing: under
\((p,q,r,s)\mapsto(p_1,q_1,p_2,q_2)\),
\((a,b,c,d)\mapsto(b,c,b,c)\), eq. (3) reads
\(A_{p_1q_1}(b,c)A_{p_2q_2}(b,c)-A_{p_1p_2}(b,b)A_{q_1q_2}(c,c)\ne0\).
The D1 attack surface is therefore the curvature-minor machinery.

**D2 (hand derivation).**  \(F_a=\{f_0,f_1,f_2\}\) with \(f_0\) the
\(S_b\)–\(S_c\) carrier, \(f_1=\{s_1,x\}\), \(f_2=\{s_2,y\}\)
(\(s_i\in S_a\), \(x\in S_b\), \(y\in S_c\)), \(R=S_a\setminus
\{s_1,s_2\}\).  The correction is
\((-1)^3A_{f_0}(\chi)A_{f_1}(\chi)A_{f_2}(\chi)h_a(R)\), so the
corrected crossing sum vanishes **iff**

\[
 \boxed{\;-\,A_{f_0}(\chi)\,A_{f_1}(\chi)\,A_{f_2}(\chi)\,h_a(R)
   \;=\;h_a(S_a)\,h_b(S_b)\,h_c(S_c).\;}                       \tag{3}
\]

*Machine content of this section* (labelled honestly: the derivations
are hand steps consuming committed Theorem C, definitional two-site
hafnians and the census): the checker recomputes the signs
\((-1)^k\) from the census's computed \(k\in\{2,3\}\), re-reads the
two-site hafnian convention \(h_b(S_b)=A_{p_1p_2}(b,b)\) nonvacuously
from a pseudorandom packet, and probes each boxed condition with a
positive instance (all factors nonzero, the Theorem-C total vanishes)
and a negative instance (one cell perturbed, the total is nonzero), so
a sign or transposition error in either statement is caught.  Whether
(2)/(3) can actually *hold* on an exact source is precisely what is
open; no fabricated packet can decide that.

---

## 5. The minimal open statement at N = 8, and the composition chain

Quoting the working attack map verbatim:

> MINIMAL OPEN STATEMENT AT N=8 (sharp): rule out D1 and D2 on an
> exact source with live split (4,2,2).  Everything else at N=8 is
> settled modulo auditing step 2.

"Step 2" — the \(n=8\) drop-\((0,2,6)\) UNSAT — has since been audited
and committed (commit `1bbb4d9`), so that caveat is discharged and the
statement stands as quoted, with shape \((4,2,2)\) written
\((2,2,4)\) in this note's sorted convention.  The chain:

1. **[committed]**  An exact ternary source at \(N=8\) has the three
   pure anchors and a diagonal shadow (Lemma 0, Theorem B —
   [`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md)).
2. **[committed]**  The shadow has a live split of shape
   \((0,4,4)\) or \((2,2,4)\): the drop-\((0,2,6)\) UNSAT machine
   theorem
   ([`notes/diagonal-termwise-census-and-pencil-guard.md`](diagonal-termwise-census-and-pencil-guard.md)
   §6, commit `1bbb4d9`; its checker's digest is pinned here, and the
   solver section's no-options pass re-derives the verdict
   semantically).
3. **[committed]**  On that live split, the \(F\)-avoiding crossing
   sum is \(-h_0h_1h_2\) plus corrections supported on at most three
   saturating families, one per colour, each the whole colour class
   \(F_a\), each of size \(\ge2\) (Theorem C, Corollaries C2–C3 —
   [`notes/good-crossing-matching-forcing.md`](good-crossing-matching-forcing.md)).
4. **[this artifact]**  Lemma H + the census: at shape \((0,4,4)\)
   every possible saturating family has empty residue, so every
   correction vanishes and Corollary C1 already yields a nonzero
   crossing matching all of whose crossing edges are good.  At shape
   \((2,2,4)\) the same holds unless the saturating colour is the
   4-part's colour, where the only dangerous configurations are
   **D1** and **D2**, harmful only under (2) resp. (3).
5. **[open]**  Rule out (2) and (3) — D1 and D2 — on an exact source
   with a live \((2,2,4)\) split.  Given this step, every exact
   \(N=8\) source would have a live split carrying a nonzero crossing
   matching whose crossing edges are all good: the
   crossing-pairs-are-good input of the committed cluster's
   label-split application, at \(N=8\).

At \(N=10\) the census shows dangerous configurations in **every**
shape, so no analogous reduction follows; the \(N\ge10\) story remains
what the committed notes say (good crossing *pair* unconditionally by
C4′/C5′; the matching-level statement open).

---

## 6. Consistency: the stall guard, K4, omega

The committed **stall guard** (\(N=6\), shape \((0,2,4)\), essential
colour 2) satisfies **everything Lemma H's proof consumes** — (E1),
(E2), (E3) at both carriers, computed and required — and still has
nonzero carrier crossing cells with a genuinely cancelling correction.
There is no contradiction, and the checker *requires* the exact reason:
its family has \((k,|R|,t)=(2,2,2)\), i.e. **residue count 2**, so
Lemma H's hypothesis \(V(F_a)=B\) fails; the escape is \(|R|=2\) and
nothing else.  In particular the guard's 9 exactness-defect words are
**not** the mechanism (none reads the essential colour at a carrier
site — that is (E1)+(E2)+(E3) doing exactly what they force, required).
Its Lemma-F residue tensor \(H_R=\nu E_{22}\), \(\nu=1\), its carrier
cells \(A_e(\chi)=-1\ne0\), and identity (1) at both carriers
(\(-1=-1\), nonvacuous) are all recomputed.  Finally the guard is the
**cross-implementation control** for the census: its configuration,
computed from its *blocks* (bad-pair table + crossing pairs), must
equal the unique entry the abstract split enumeration reports at
\(((0,2,4),4)\) — two independent paths to the same object, and the
in-census proof that the dangerous entry \((2,2,2)\) is *realizable* by
a packet satisfying (E1)–(E3).

The two vacuity controls, each required with its own reason: the exact
\(K_4\) source has **no live split** (Theorem C and Lemma H are vacuous
there for that reason and no other), and the omega guard has live
splits but **zero bad crossing pairs** on each (so \(F_a=\varnothing\),
no saturating family can exist, and Theorem C already yields the good
crossing matching).

---

## 7. The Boolean route is dead: the strengthened SAT instance

The solver section asks whether the *support-theoretic* content of this
note's reduction — everything Lemma F, Corollary C2's pendant
structure and the carrier nonvanishing say at the Boolean level —
already suffices to rule out D1/D2, the way the committed engine's
UNSAT verdicts rule out shapes.  It does **not**, and that is the
point: the residual content of D1/D2 is scalar.

**The instance** (built once; the committed engine's recurrence shadow,
units and symmetry branches are imported verbatim, and the committed
files' digests are pinned):

* shape \((0,2,6)\): its 168 colourings **dropped**, exactly as the
  committed drop-\((0,2,6)\) UNSAT mode does;
* every other non-\((2,2,4)\) shape (the 210 \((0,4,4)\) colourings):
  the plain **dead** clause — by §3 no dangerous family exists there;
* each of the 1260 \((2,2,4)\) colourings: **dead ∨ D1 ∨ D2**, where
  each option loads the *full* Boolean shadow of its configuration:
  residue purity \(z_a(\mathrm{res})=1\),
  \(z_b(\mathrm{res})=z_c(\mathrm{res})=0\) for the residue of **every
  nonempty sub-family** (Lemma F), carrier nonvanishing
  \(z_a(\mathrm{carrier})=1\) (\(\lambda\ne0\)), and the
  \(a\)-pendant facts (from (E1): \(z_a(T)=0\) for every even \(T\)
  containing a pendant but not its partner) — 8 D1 options (2
  matchings × 4 pendant orientations) and 48 D2 options (6 residues ×
  4 carriers × 2 attachments) per colouring.

Size (pinned by a `require`, computed): **73 548 variables,
6 101 916 clauses**; 10 080 D1 and 60 480 D2 option variables; the
committed 9 symmetry branches.  Three assumption regimes over one CNF:

| regime | verdict | meaning |
|---|---|---|
| strengthened | **SAT** (branch 1) | the Boolean route is dead: all loaded support facts coexist with a live \((2,2,4)\) split saved by D1 |
| every D2 option disabled | **SAT** (branch 1) | D1 alone saturates the relaxation — killing D2 first would not close the Boolean gap either |
| every option disabled | **UNSAT** (9/9 branches) | semantically the committed drop-\((0,2,6)\) instance: the in-run cross-check tying this encoder to the committed machine theorem, and the proof that the D1/D2 escapes are load-bearing |

Every SAT model is independently re-audited: all 6.1M clauses and all
assumptions are re-checked semantically, every Boolean-live
\((2,2,4)\) colouring must be discharged by a true option, and the
model's live shapes are read off and confined to
\(\{(0,2,6),(2,2,4)\}\).  The live-colouring scan itself carries a
positive control: since the no-options regime is UNSAT, every SAT
model *must* be Boolean-live at some \((2,2,4)\) colouring, and the
checker requires the scan to find one (a blind scan would make the
danger-clause audit pass vacuously); the option-table scan and the
family scan are additionally required to agree on the live count.  In
the audited models both Boolean-live \((2,2,4)\) colourings are saved
by **D1** options (none by D2, even when D2 is available) — recorded
in the SAT ledger.

**Sound direction, stated plainly.**  SAT is the *weak* direction: a
support-level survivor, exactly as the committed engine's SAT rows are.
It proves nothing about exact sources; it proves that no argument at
the level of hafnian *supports* — however much of Lemma F and the
pendant structure it loads — can rule D1/D2 out.  The UNSAT row is
used in the sound direction and only as a consistency cross-check of a
committed theorem.

**Gating.**  Exactly as in the committed census pair: the solver
section imports PySAT and the committed engine lazily; under
`python3 -S` (two of the six verification commands) the import fails
and the section is **skipped with a loud flag** — the run prints that
the three verdicts are NOT ESTABLISHED and that the "Boolean route is
dead" claim is conditional in that run; the SAT ledger is not hashed;
no verdict is fabricated.  `--require-solver` restores a hard failure
(exit 1) with the diagnostic text the repository's other
solver-dependent checkers use.

---

## 8. D1/D2 attack status

The subsequent committed attack is
[`n8-d2-kill-and-monochrome-rigidity.md`](n8-d2-kill-and-monochrome-rigidity.md).
It kills D2 on its swept branch class, modulo the hand Signature Lemma
and the explicit equivariance/orientation caveats recorded there.  It
also proves that D1 is impossible on the a-column support class
\(\Sigma\), while leaving the out-of-\(\Sigma\) D1 supports open.  Those
partial outcomes do not alter this census or its checker: D1 and D2 are
still the two configurations the reduction must dispatch, and no exact
ternary source at \(N=8\) is claimed.

---

## 9. Scope

1. Lemma H, identity (dagger) and the D1/D2 reductions are statements
   about *exact* sources; they are hand proofs consuming committed
   hand proofs (Lemma F, C2, C3, Theorem C), and the machine checks
   are on instances — constructed packets, pseudorandom packets, one
   genuinely exact source (\(K_4\), where everything is vacuous for
   the required reason) and two non-exact guards.  **No exact ternary
   source at \(N=8\) is available to test on** — showing none exists
   is the project's aim — so the universal quantifier over exact
   sources is not machine-verified anywhere here.
2. The census is exhaustive *combinatorics of splits*, not of sources:
   it bounds what saturating families can look like (a necessary
   condition via Corollary C3), so its *clearings* are sound for every
   exact source, while its *dangerous* entries are not claimed
   realizable — except \((2,2,2)\) at \(N=6\), realized by the stall
   guard with (E1)–(E3).
3. The strengthened SAT verdicts are support-level and
   solver-dependent (§7); the drop-\((0,2,6)\) UNSAT is **cited as
   committed**, and re-derived here only semantically (no-options
   regime), not clause-for-clause — the clause-for-clause encoder
   check is the committed census pair's.
4. Everything at \(N\ge10\) is untouched: the census *requires* that
   every \(N=10\) shape stays dangerous, so no claim of this note
   extends past \(N=8\).  Theorem B's live-split supply and the
   \(n=10\) shape-restricted instance remain as the committed notes
   state.
5. Per project discipline this is a research reduction until
   independently audited.  **Krenn's conjecture remains open.**

---

## 10. Verification

~~~text
python3       computations/verify_n8_saturation_census_two_configurations.py
python3 -O    computations/verify_n8_saturation_census_two_configurations.py
python3 -I    computations/verify_n8_saturation_census_two_configurations.py
python3 -S    computations/verify_n8_saturation_census_two_configurations.py
python3 -I -S computations/verify_n8_saturation_census_two_configurations.py
python3 -m py_compile computations/verify_n8_saturation_census_two_configurations.py
~~~

Runtime is about **2 minutes 20 seconds** with a solver (the \(N=10\)
census dominates at roughly two minutes; the whole solver section —
build, three regimes, 6.1M-clause model audits — takes about 20
seconds), and about two minutes under `-S`, where the solver section is
skipped loudly.  (`python3 -I` does not prepend the script's
directory; the checker inserts its own directory, computed from
`__file__`, before importing the committed companions, and **pins**
their digests — see the ledger's `conventions` block — so it refuses
to run against drifted committed artifacts.)

**Ledgers.**  Two frozen digests, both hashing *computed* content
through the committed `content_hash` (exact values, `Fraction`s as
tagged strings; no hard-coded truth value anywhere).  The exact ledger
records the pinned committed digests and convention probes; the full
census tables and dangerous sub-tables at \(N=6,8,10\); the canonical
split's D1 families (as edge lists), all 48 D2 families (as edge lists
with residues) and the empty-residue counts; the (dagger) expansion
instance counts including the nontrivial-sub-hafnian and sharpness
tallies; the 11 Lemma-H carrier rows with their computed \(\nu\); the
scalar-form signs, conditions and probe instances; the stall guard's
structure, residue tensor, carrier cells, dagger values, defect words
and (E1)–(E3) status; and both vacuity controls.  The SAT ledger
records the instance size and colouring census, the three regimes'
verdicts, branches solved, disabled-option counts, and each SAT
model's audit (live \((2,2,4)\) count, saved-by-D1/D2 counts, live
shapes, model hash).

~~~text
exact ledger : 7819357369b7c17a16e6e62bf4bd8c0f837bd6479f2b79f395d562bc8a4b21ac
SAT ledger   : 2b38816182bc6f54a156a4b354a91f14899d4e73f8e48d6ac27248eb8488d488
~~~

**Mutation-tested with nine injections, four of them
fabricated-geometry.  All nine raise under both `python3` and
`python3 -O`, with the same message, naming the broken property.**
MU9 exercises the solver section and is therefore inert under `-S`,
where that section is skipped — which is the point of the skip flag.
The scratch ancestor's silent mutation (the sub-hafnian drop at
\(|R|\le2\); see §2) is the reason MU2's guards exist.

| # | injection | message raised |
|---|---|---|
| MU1 | the Lemma-H clearing claim extended to the dangerous key \(((2,2,4),4)\) | N=8 census: shape (2, 2, 4) with \|S_a\|=4 acquired a saturating family with nonempty residue, so Lemma H no longer clears it |
| MU2 | the sub-hafnian factor dropped from the (dagger) expansion | the (dagger) hafnian expansion failed: the two-endpoint pivot of H_{R u e} does not reproduce the packet coefficient |
| MU3 | the carrier cell of identity (dagger) read transposed | identity (dagger) failed on the stall guard at carrier (0, 2) |
| MU4 | the census enumerator's covering condition dropped | N=8 census: the set of (shape, \|S_a\|) admitting a saturating family changed |
| MU5 | **(fabricated geometry)** a bogus family injected into the single enumeration path | N=8 census: the set of (shape, \|S_a\|) admitting a saturating family changed |
| MU6 | **(fabricated geometry)** a residue cell of the stall guard perturbed after the solve | stall guard: H_R is not the pure colour-a tensor Lemma F predicts |
| MU7 | **(fabricated geometry)** a crossing cell injected into a Lemma-H carrier block | Lemma H packet: (E3) is broken by the construction |
| MU8 | frozen exact ledger digest altered | n8 saturation census ledger changed |
| MU9 | **(fabricated geometry)** both danger options assert purity of the wrong residue (the \(b\)-part instead of the \(a\)-residue; variable and clause counts unchanged) | the strengthened n=8 instance (all Lemma F residue purity, carrier nonvanishing and a-pendant facts loaded) is no longer SAT: the Boolean route would not be dead and the reduction to scalar content would be understated |
