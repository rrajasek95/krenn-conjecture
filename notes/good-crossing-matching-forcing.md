# A nonzero crossing matching whose crossing edges are good: Theorem C, and the saturating obstruction

Checker:
[`computations/verify_good_crossing_matching_forcing.py`](../computations/verify_good_crossing_matching_forcing.py).

This note attacks the one conjectured statement of
[`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md)
("crossing-pairs-are-good").  **All** conventions, notation and cited
results — Lemma 0, Theorem A, the parity fact, Theorem B, Lemma E with
(E1)–(E3), C1–C5 — are that note's, and the checker here does not
re-implement any of its machinery: it **imports** `oriented`,
`perfect_matchings`, `matching_tensor`, `hafnian`, `even_splits`,
`good_pairs`, `is_good_pair`, `essential_covectors`, `require`, the
\(K_4\) source and the six-site guard from
[`computations/verify_exact_source_live_split_forcing.py`](../computations/verify_exact_source_live_split_forcing.py),
so the two artifacts cannot drift apart.  A conventions probe in the
checker re-derives, from scratch, that the imported symbols really are
the endpoint-ordered ones (\(A_{uv}(i,j)\) reads \(i\) at \(u\),
\(A_{vu}=A_{uv}^{\mathsf T}\); a pair is **good** iff both deleted
endpoint stars are injective), and the committed artifact's frozen
digest is recorded in this one's ledger.

**Model.**  Sites carry endpoint-ordered aggregate blocks \(A_{uv}\) with
cells \(A_{uv}(i,j)\), \(i\) read at \(u\) and \(j\) at \(v\); exactness
is \(H_B(A)=\Delta_{B,3}\) over \(\mathbb C\).  This note works in the
**GENERAL (bicoloured) model**, where \(A_{uv}(i,j)\ne0\) is permitted for
\(i\ne j\) — the model of the open case \(N=8,d=3\) (DeepMind's Lean
`eqSystem8_no_solution_d3`, research open; see
[`references/REFERENCES.md`](../references/REFERENCES.md)), **not** the
monochromatic-edge restriction.  Diagonal results quoted here are used
only as necessary conditions on the diagonal shadow of a general source.

**Status.**  The deletion identity is a *polynomial identity*, proved by
hand below and verified on instances.  Lemma F, Lemma G, C4′, C5′,
Theorem C and Corollaries C1–C3 are *hand proofs* about arbitrary exact
sources, *verified on instances only* — the exact \(K_4\) source,
constructed (E1)/(E2)/(E3) packets, and two non-exact guards.  The
saturating case of Theorem C, and with it the full
crossing-pairs-are-good lemma, remain **conjectured**; the new stall
guard of §4 shows they are not reachable from the anchors, the split
equation and (E1)–(E3) alone.  **Krenn's conjecture remains open.**

---

## 0. Summary of outcomes

**Proved (hand proofs, machine-verified on instances).**

* **Lemma F** (multi-deletion purity chain).  Deleting a *set* of
  pairwise disjoint bad pairs of an exact source leaves either the zero
  tensor or a nonzero **pure** colour-\(a\) tensor.  (C3 of the
  committed note is the two-pair, distinct-colour case.)
* **Lemma G** (one bad pair per site per colour).  Strengthens C1 from
  the ordered relation "\(v\) is essential at \(u\)" to the unordered
  pair.  Consequences: at most \(3N/2\) bad pairs in total (C4 gave
  \(2N\)), and the bad crossing pairs of a fixed essential colour form a
  **matching**.  The bound is **tight** on the exact \(K_4\) source.
* **C4′, C5′** (improved counting).  \(\#\{\text{good crossing pairs}\}
  \ge X-3N/2\), and the only shape with \(X\le3N/2\) is \((0,2,N-2)\)
  with \(N\le8\).  Since \(N=6\) is vacuous, **for every even \(N\ge10\)
  a good crossing pair exists unconditionally**, and at \(N=8\) only the
  shape \((0,2,6)\) survives the count.
* **Theorem C** (the main result).  The crossing sum restricted to
  matchings avoiding all bad crossing pairs equals \(-h_0h_1h_2\) plus a
  correction supported on *saturating* families, of which there are at
  most three — one per colour.
* **Corollary (unconditional).**  \(|T|=1\) can never saturate.  Hence
  for every bad crossing pair \(e\), the matchings through \(e\)
  contribute **zero** in total to the split equation.

**Refuted (new guard).**  A six-site packet — the **stall guard** —
satisfies all three pure anchors, the live-split colouring equation,
liveness, and **(E1), (E2) *and* (E3)** at both of its bad crossing
pairs, and still has **no** nonzero crossing matching whose crossing
edges are all good.  So the saturating gap of Theorem C **cannot** be
closed by the anchors, the split equations and the essentiality
structure lemma alone.  The committed \(727/729\) guard breaks (E3);
this one keeps it.  They are complementary.

---

## 1. Lemma F — the multi-deletion purity chain

**Lemma F (proved).**  Let \(A\) be an exact ternary source on \(B\) and
let \(T=\{e_1,\dots,e_k\}\) be pairwise disjoint **bad** pairs,
\(e_i=\{u_i,v_i\}\) with \(v_i\) essential at \(u_i\) of essential
colour \(a_i\) and \(\lambda_i=A_{u_iv_i}(a_i,a_i)\ne0\).  Then

* if the \(a_i\) are not all equal, \(H_{B\setminus V(T)}(A)\equiv0\);
* if \(a_i=a\) for all \(i\), then
  \(H_{B\setminus V(T)}(A)=\nu_T\,e_a^{\otimes}\) with
  \(\nu_T=\bigl(\prod_i\lambda_i\bigr)^{-1}\ne0\).

*Proof.*  Induction on \(k\); \(k=1\) is (E3).  Let \(S=B\setminus V(T)\)
be known and let \(e'=\{u',v'\}\) be disjoint from \(V(T)\), with
essential colour \(a'\) and covector \(\varphi'\).  Expand \(H_S\) at the
pivot \(u'\) — equation (7) of the committed note, applied inside \(S\)
— and contract the \(u'\)-mode with \(\varphi'\).  Every term over
\(x\in S\setminus\{u',v'\}\) dies by (E1) for \((u',v')\); this is
legitimate because (E1) kills row \(a'\) of \(A_{u'x}\) for **every**
\(x\) outside \(\{u',v'\}\) in \(B\), in particular for those inside
\(S\).  What is left is

\[
 (\varphi'\!\cdot\!H_S)(j,y)=\psi'(j)\,H_{S\setminus e'}(y),
 \qquad \psi'(j)=\varphi'_{a'}\lambda'\,[\,j=a'\,].            \tag{1}
\]

If \(H_S\equiv0\) the left side vanishes; taking \(j=a'\), where
\(\psi'(a')\ne0\), gives \(H_{S\setminus e'}\equiv0\).  If
\(H_S=\nu\,e_a^{\otimes}\), the left side is
\(\nu\varphi'_{a'}[a'=a][j=a][y\equiv a]\); for \(a'\ne a\) it vanishes
and \(j=a'\) again forces \(H_{S\setminus e'}\equiv0\), while for
\(a'=a\), \(j=a\) it gives \(H_{S\setminus e'}=(\nu/\lambda')
e_a^{\otimes}\).  The value of \(H_{B\setminus V(T)}\) does not depend on
the order of deletion, so if any two colours disagree we may delete those
two first and the tensor is zero from then on.  \(\square\)

**Verified on instances, both branches.**

*Equal colours.*  26 (packet, sub-family) instances on constructed
packets carrying two and three disjoint (E1)/(E2)/(E3) pairs at
\(N=6,8\).  Each carrier is checked to be a genuine **bad** pair, each
hypothesis ((E1), (E2), (E3)) is *computed* from the blocks rather than
assumed, and each residue tensor must equal the single pure word with the
predicted **nonzero** coefficient \(\prod_{i\in T}\lambda_i^{-1}\).

The exact \(K_4\) source carries the same chain, but with a caveat that
must be stated: at \(N=4\), deleting *two* disjoint pairs leaves the
**empty** residue, where \(H_\varnothing=\{()\mapsto v\}\) and the "pure
word" is \(()\) whatever the colour is.  **The purity (colour) claim of
the two-pair step is therefore unfalsifiable on \(K_4\)**; only the
coefficient \(1/(\lambda_1\lambda_2)\) has content there.  (An earlier
version of this artifact checked only `set(tensor) <= {pure word}` at
that step, which is *vacuously true* for every colour and every value —
an independent audit found the corresponding colour mutation silent.)
The checker now walks the chain step by step: the **first** deletion
leaves two sites, where the colour claim *is* falsifiable and is required
to be \(\lambda_1^{-1}e_{a}^{\otimes}\); the **second** is required to
equal \(\{()\mapsto1/(\lambda_1\lambda_2)\}\) exactly; and the ledger
records `two_pair_residue_is_empty = true` so the vacuity is visible
rather than implied.  The genuine multi-site purity content of Lemma F is
carried by the \(N=6,8\) packets, not by \(K_4\).

*Distinct colours.*  An eight-site instance with \(e_1=\{0,1\}\) of
colour \(a_1=0\) and \(e_2=\{2,3\}\) of colour \(a_2=1\), satisfying
(E1)+(E2) at both pairs and (E3) at \(e_1\) — exactly the hypotheses the
induction consumes at the mixed-colour step.  Its residue
\(R=\{4,5,6,7\}\) carries **six nonzero blocks** and **three nonzero
matching terms** \((1,1,-2)\) that cancel, so the forced conclusion
\(H_R\equiv0\) is a genuine cancellation, not a zeroed block.  A
**falsification probe** perturbs one residue cell so that \(H_R\ne0\),
and the checker requires that a *hypothesis* then breaks — (E3) at
\(e_1\) fails, while (E1) and (E2) at \(e_2\) still hold, so the probe
isolates (E3).  Without that probe the distinct-colour branch would be a
check of what the construction had already imposed.

Note what the mixed-colour branch does *not* need: (E3) at more than one
pair.  Indeed (E1)+(E2)+(E3) at two disjoint pairs of *different*
colours is already contradictory for an exact source, which is why the
instance carries (E3) at one pair only.

---

## 2. Lemma G — one bad pair per site per colour

**Lemma G (proved).**  Let \(A\) be exact.  For each site \(u\) and each
colour \(a\), at most one bad pair contains \(u\) and has essential
colour \(a\).  Hence \(u\) lies in at most three bad pairs, and

\[
 \#\{\text{bad pairs}\}\ \le\ 3N/2.                            \tag{2}
\]

*Proof.*  Suppose \(\{u,v\}\) and \(\{u,v'\}\), \(v\ne v'\), are both bad
of essential colour \(a\).  Three cases.

1. \(v\) essential at \(u\) and \(v'\) essential at \(u\): this is C1.
2. \(v\) essential at \(u\), \(u\) essential at \(v'\): (E1) for
   \((u,v)\) makes row \(a\) of \(A_{uv'}\) vanish, so
   \(A_{uv'}(a,a)=0\); (E2) for \((v',u)\) makes
   \(A_{v'u}(a,a)=\lambda'\ne0\).  These are the same scalar, since
   \(A_{v'u}=A_{uv'}^{\mathsf T}\).  Contradiction.
3. \(u\) essential at \(v\) and \(u\) essential at \(v'\): (E1) for
   \((v,u)\) gives \(W_a(v,z)=0\) for every \(z\ne u\), and likewise
   \(W_a(v',z)=0\) for \(z\ne u\).  In \(W_a\) both \(v\) and \(v'\) have
   \(u\) as their only neighbour, so no perfect matching of \(B\) is
   supported and \(h_a(B)=0\), contradicting Lemma 0.  \(\square\)

**Tightness (verified).**  On the exact \(K_4\) source every site lies in
exactly one bad pair of each colour — six bad pairs in all, which is
exactly \(3N/2\).  The checker computes the per-(site, colour) census
from the blocks and requires both that no site carries two pairs of one
colour and that the count *equals* the bound, so tightness is a positive
check, not an inequality that a bug could satisfy vacuously.

**C4′ (proved).**  \(\#\{\text{good crossing pairs}\}\ge X-3N/2\), where
\(X=|S_0||S_1|+|S_0||S_2|+|S_1||S_2|\) is the number of crossing pairs.

*Proof.*  A bad crossing pair is in particular a bad pair, so
\(\#\{\text{bad crossing}\}\le\#\{\text{bad}\}\le3N/2\) by (2); subtract
from \(X\).  \(\square\)  (This is where C4′ improves on C4: the
committed bound orients each bad crossing pair and caps out-degrees at
\(2\) using C1 + C2, giving \(2N\); Lemma G caps the *unordered*
incidence at one per colour, giving \(3N/2\), and needs no reference to
the split at all.)

**C5′ (proved).**  The only shape \(a\le b\le c\) (even, \(a+b+c=N\),
\(c\ne N\)) with \(X\le3N/2\) is \((0,2,N-2)\) with \(N\le8\).

*Proof.*  If \(a\ge2\) then \(ab\ge2b\), \(bc\ge2c\), \(ca\ge2a\), so
\(X\ge2N>3N/2\).  If \(a=0\) then \(c\ne N\) forces \(b\ge2\) and
\(X=b(N-b)\); \(b=2\) gives \(2N-4\le3N/2\) iff \(N\le8\), and \(b\ge4\)
gives \(X\ge4N-16>3N/2\) for every \(N\ge8\).  \(\square\)

Re-verified by exhaustion to \(N=200\), side by side with the committed
note's weaker \(X\le2N\) table; the checker requires that the sharper
bound actually *removes* shapes the committed one kept, so the
improvement cannot be a no-op:

| \(N\) | shapes with \(X\le2N\) (committed C5) | shapes with \(X\le3N/2\) (C5′) |
|---|---|---|
| 6 | \((0,2,4)\), \((2,2,2)\) | \((0,2,4)\) |
| 8 | \((0,2,6)\), \((0,4,4)\) | \((0,2,6)\) |
| \(\ge10\) | \((0,2,N-2)\) | **none** |

Since \(N=6\) is vacuous
([`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md)
Th. 1.1), the counting route now leaves **only the shape \((0,2,6)\) at
\(N=8\)**, where the committed note left \((0,2,N-2)\) for all
\(N\ge10\) plus \((0,4,4)\) and \((2,2,2)\).

---

## 3. Theorem C — the deletion identity with a saturating correction

**The identity (proved).**  For any block family, any edge set \(F\) and
any word \(w\),

\[
 \sum_{\substack{M\in\operatorname{PM}(B)\\ M\cap F=\varnothing}}
   \ \prod_{uv\in M}A_{uv}(w_u,w_v)
 \ =\ \sum_{\substack{T\subseteq F\\ T\ \text{a matching}}}
   (-1)^{|T|}\Bigl(\prod_{e\in T}A_e(w)\Bigr)H_{B\setminus V(T)}(w).
                                                               \tag{3}
\]

*Proof.*  Möbius inversion over the matching \(M\cap F\): classify each
\(M\) by \(T=M\cap F\) (a matching inside \(F\)) and use
\(\sum_{M\supseteq T}\prod A=\bigl(\prod_{e\in T}A_e\bigr)
H_{B\setminus V(T)}\).  \(\square\)

*Verified*: 196 pseudorandom instances at \(N=4,6,8\), of which 140 have
a nonzero common value and **153 have a nonzero \(T\ne\varnothing\)
correction**.  The checker refuses to pass if either count is zero — an
identity checked only where both sides read \(0=0\), or only at
\(F=\varnothing\), would verify nothing.

**Theorem C (proved).**  Let \(A\) be an exact ternary source,
\((S_0,S_1,S_2)\) a live split with colouring \(\chi\), and \(F\) the set
of **bad crossing pairs**.  Call a nonempty matching \(T\subseteq F\)
**saturating** when all its edges share one essential colour \(a\) and
\(B\setminus V(T)\subseteq S_a\).  Then

\[
 \sum_{\substack{M\ \text{crossing}\\ M\cap F=\varnothing}}\prod A(\chi)
 \ =\ -\,h_0(S_0)h_1(S_1)h_2(S_2)
  \ +\!\!\sum_{T\ \text{saturating}}\!\!(-1)^{|T|}
    \Bigl(\prod_{e\in T}A_e(\chi)\Bigr)h_a\bigl(B\setminus V(T)\bigr).
                                                               \tag{4}
\]

*Proof.*  Apply (3) with \(w=\chi\).  The term \(T=\varnothing\) is
\(H_B(\chi)=0\) by exactness, \(\chi\) being non-constant.  For
\(T\ne\varnothing\), Lemma F makes \(H_{B\setminus V(T)}\) either zero or
\(\nu_T e_a^{\otimes}\), so \(H_{B\setminus V(T)}(\chi)\) is
\(\nu_T[\,B\setminus V(T)\subseteq S_a\,]\) in the second case and \(0\)
in the first: only saturating \(T\) survive, and there
\(H_{B\setminus V(T)}(\chi)=h_a(B\setminus V(T))\).  On the left, the
matchings with no crossing edge are exactly the triples of within-part
matchings, they are automatically \(F\)-avoiding (\(F\) consists of
crossing pairs), and Theorem A says they total \(h_0h_1h_2\).
\(\square\)

**Corollary C1 (proved).**  If no saturating family exists, the left side
of (4) is \(-h_0h_1h_2\ne0\), so some perfect matching \(M\) has nonzero
\(\chi\)-weight, no bad crossing pair, and — by the parity fact — at
least two crossing edges.  **Every crossing cell of \(M\) sits on a good
pair.**  This is precisely the input the label-split application of the
committed note's §8 asks for.

**Corollary C2 (proved, unconditional).**  A saturating family has
\(|T|\ge2\).

*Proof.*  \(|T|=1\) needs \(B\setminus e\subseteq S_a\), i.e.
\(|B\setminus S_a|\le2\); it is even and \(S_a\ne B\), so it is exactly
\(2\); the two sites are the endpoints of the crossing edge \(e\), so
they lie in two different parts, each then of odd size \(1\).
Contradiction.  \(\square\)

Consequently \(\sum_{M\ni e}\prod A(\chi)=0\) for **every** bad crossing
pair \(e\): the crossing sum is carried entirely by matchings avoiding
\(e\), and there is always a nonzero crossing matching avoiding any one
prescribed bad crossing pair.

*Verified*: the combinatorial half exhaustively — zero size-one
saturating families over all \(16\,596\) ordered even splits and
\(475\,248\) crossing pairs at \(N=4,6,8,10\).  The algebraic half is
verified in the shape it is consumed, \(\sum_{M\ni e}=A_e(w)\,
H_{B\setminus e}(w)\), on 48 pseudorandom instances (43 nonvacuous) and
on every bad crossing pair of both guards.  Two of those guard instances
are **nonvacuous in the strong sense**: the crossing cell \(A_e(\chi)\)
is itself nonzero and (E3) holds, so "the sum through \(e\) vanishes" is
a statement about the deleted tensor and not about a zero factor.  Both
sit on the stall guard, at \(\{0,2\}\) and \(\{1,3\}\).

**Corollary C3 (proved).**  By Lemma G each colour class \(F_a\) of bad
crossing pairs is a matching, and every crossing edge meets
\(B\setminus S_a\); hence a saturating family of colour \(a\) must
contain the \(F_a\)-edge through each site of \(B\setminus S_a\), i.e.
it **is** \(F_a\).  So

* there are **at most three** saturating families, one per colour;
* colour \(a\) saturates **iff** \(F_a\) covers \(B\setminus S_a\);
* a hitting set \(H\) of one edge per saturating colour has \(|H|\le3\),
  and running (3) with \(F\setminus H\) in place of \(F\) gives a nonzero
  crossing matching whose crossing edges are good **except possibly those
  in \(H\)**.

In the shape \((0,2,N-2)\) — \(S_0=\varnothing\),
\(S_1=\{x_1,x_2\}\), \(S_2\) the remaining \(N-2\) sites — only the big
part's colour can saturate.  Every crossing pair here joins \(S_1\) to
\(S_2\), so \(F_a\) is a matching drawn from the \(2(N-2)\) edges through
\(x_1,x_2\) and therefore has **at most two edges**, covering at most two
sites of \(S_2\).  Colour \(0\) would need \(F_0\) to cover
\(B\setminus S_0=B\), all \(N\) sites; colour \(1\) would need \(F_1\) to
cover \(B\setminus S_1=S_2\), that is \(N-2\) sites of which \(F_1\)
reaches at most two.  Both are impossible for \(N\ge6\).  Colour \(2\)
needs only \(B\setminus S_2=\{x_1,x_2\}\) covered, which a two-edge
matching does.  So there \(|H|=1\) and one of the two crossing cells of
the matching is always good.

*Verified*: on both guards the checker brute-forces **every** nonempty
monochromatic matching \(T\subseteq F\) with \(B\setminus V(T)\subseteq
S_a\) and requires that the result is exactly the set of whole colour
classes.  On both guards, however, every colour class happens to cover
\(B\setminus S_a\), so the "iff" is never exercised in the negative
direction there; the checker therefore also runs a purely combinatorial
probe (a split, three bad crossing pairs, two colours) with **one
covering and one non-covering class**, and requires that the brute-force
enumeration returns exactly the covering one.  Without that probe the
covering condition could be replaced by `True` and nothing would notice
— this was found by mutation testing (M8) and is now closed.

---

## 4. The stall guard: the saturating gap is real

\(N=6\), split \(S_0=\varnothing\), \(S_1=\{0,1\}\),
\(S_2=\{2,3,4,5\}\) (shape \((0,2,4)\)), essential colour \(a=2\), bad
crossing pairs \(\{0,2\}\) and \(\{1,3\}\).  The construction imposes the
purity of the two deleted-pair tensors:

\[
\begin{aligned}
 &A_{45}=\nu E_{22},\quad A_{15}=0,\quad A_{14}=u\otimes e_2,\quad
   A_{35}=v\otimes e_2,\quad A_{13}=(\mu_1E_{22}-u\otimes v)/\nu,\\
 &A_{04}=0,\quad A_{05}=w\otimes e_2,\quad A_{24}=z\otimes e_2,\quad
   A_{02}=(\mu_2E_{22}-w\otimes z)/\nu,
\end{aligned}                                                  \tag{5}
\]

with \(u_2=w_2=0\) (that is (E1) at row \(a\)), \(\lambda_1\lambda_2\nu=1\)
and \(\mu_i=\lambda_i^{-1}\); \(A_{01},A_{03},A_{12},A_{23},A_{25},
A_{34}\) stay free.

**The solve.**  Write \(C\) for the crossing sum of Theorem A.  Every
crossing matching pairs \(x_1=0\) and \(x_2=1\) into the big part, so
\(C=\sum_{r\ne s}\alpha_r\beta_s\,h_2(S_2\setminus\{r,s\})\) with
\(\alpha_r=A_{0r}(1,2)\), \(\beta_s=A_{1s}(1,2)\); it does **not** depend
on \(A_{01}\), which is an inside-\(S_1\) block.  The **stall condition**
is that every crossing term avoiding both designed carriers vanish — this
is a condition on the free cells, and the checker *requires* it (it holds
because \(A_{23}(2,2)=A_{25}(2,2)=0\)); it does **not** leave \(C\) with a
single term.  Here \(C\) has three nonzero terms,
\((r,s)=(2,3)\!:+1\), \((2,4)\!:-1\), \((5,3)\!:-1\), so \(C=-1\).
Theorem A then reads

\[
 0=H_B(\chi)=h_0(S_0)h_1(S_1)h_2(S_2)+C=A_{01}(1,1)\,h_2(S_2)+C,
\]

i.e. the split colouring equation is \(h_1(S_1)h_2(S_2)=-C\), with the
unique solution \(A_{01}(1,1)=-C/h_2(S_2)=1\).  The checker computes
\(C\) as an actual crossing sum over matchings and solves this equation;
it also verifies uniqueness by checking that \(A_{01}(1,1)+1\) makes
\(H_B(\chi)\ne0\).

*(An earlier version of this artifact used the formula
\(A_{01}(1,1)=+\alpha_p\beta_q h_2(S_2\setminus\{p,q\})/h_2(S_2)\),
which is wrong twice over — it drops the sign and it pretends \(C\) has
only the \((p,q)\) term.  On this packet the two errors cancel and it
returns the same value \(1\), so **no mutation can distinguish the two
formulas here**; the formula was therefore replaced outright rather than
merely guarded, and what the checker enforces downstream is the equation
itself, \(h_1(S_1)h_2(S_2)=-C\) and \(H_B(\chi)=0\), on the final
packet.)*

**Two cells are fixed by the solve, not one.**  Setting \(A_{01}(1,1)\)
moves the colour-1 anchor \(h_1(B)=A_{01}(1,1)A_{25}(1,1)A_{34}(1,1)\),
so \(A_{25}(1,1)\) is coupled to it as \(1/A_{01}(1,1)\) to keep
\(h_1(B)=1\).  The construction is that much less free than the block
table below suggests; both cells are reported in the ledger, and the
anchors are recomputed from the final blocks afterwards.  The resulting
blocks (endpoint-ordered, \(A_{uv}(i,j)\) reads \(i\) at \(u\)) are

~~~text
A_01(0,0)= 1  A_01(1,1)= 1
A_02(1,2)=-1  A_02(2,2)= 1
A_03(1,2)=-1
A_05(1,2)= 1
A_13(1,2)=-1  A_13(2,2)= 1
A_14(1,2)= 1
A_24(2,2)= 1
A_25(0,0)= 1  A_25(1,1)= 1
A_34(0,0)= 1  A_34(1,1)= 1  A_34(2,2)= 1
A_35(2,2)= 1
A_45(2,2)= 1
~~~

**Machine-verified properties, all computed from those blocks** (no
property is asserted; the checker recomputes each one and hashes the
result into the frozen ledger):

* all three pure anchors \(h_c(B)=1\) — the full conclusion of Lemma 0;
* the split is **live**, \(h_0h_1h_2=1\), and satisfies its colouring
  equation \(H_B(\chi)=0\);
* \(\{0,2\}\) and \(\{1,3\}\) are **bad crossing pairs**, each with a
  one-dimensional single-coloured kernel, and **(E1), (E2) and (E3) all
  hold at both** (essential colour \(2\), \(\lambda=1\));
* \(720\) of the \(729\) exactness equations hold, and **every** equation
  with \(w_0=2\) or \(w_1=2\) holds — as (E1)+(E2)+(E3) force;
* there are three nonzero crossing matchings and **none** of them has all
  its crossing edges good;
* Theorem C's ledger has exactly one surviving term, the saturating
  family \(F_2=\{\{0,2\},\{1,3\}\}\), of value \(+1\), which cancels
  \(-h_0h_1h_2=-1\) exactly; the crossing part of the \(F\)-avoiding sum
  is \(0\).

So the stall is not an artifact of a weak proof: the correction term is
genuinely there and genuinely equal to the main term.  Its scalar content
is the identity

\[
 h_1(S_1)\,h_2(S_2)\ =\ A_{x_1p}(\chi)\,A_{x_2q}(\chi)\,
   h_2\bigl(S_2\setminus\{p,q\}\bigr),                         \tag{6}
\]

where \(p,q\) are the colour-\(2\) essential partners of \(x_1,x_2\)
(here \(1\cdot1=(-1)(-1)\cdot1\); the checker requires both sides nonzero
so that (6) is not a \(0=0\) coincidence).  **Any proof of the conjecture
must exclude that one scalar coincidence, and it cannot do so from the
anchors, the split equations and (E1)–(E3).**

**This packet is a GUARD, not a source.**  No exact ternary source exists
at \(N=6\) at all:
[`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md)
Theorem 1.1 (cited, not re-run) excludes every complex block family with
\(H_6(A)=\Delta_{6,3}\).  The checker *requires* that the packet is
**not** exact, with a message saying exactly this, so it can never be
mistaken for a counterexample to the six-site theorem.

**Comparison with the committed guard** (both verified side by side):

| | committed \(727/729\) guard | new stall guard |
|---|---|---|
| shape | \((2,2,2)\) | \((0,2,4)\) |
| exactness equations | \(727/729\) | \(720/729\) |
| (E3) at the bad crossing pairs | **fails** at both carriers | **holds** at both |
| saturating colour classes | all three | one (\(a=2\)) |
| surviving identity terms | \(\{03\}\), \(\{15\}\), \(\{03,15\}\) | \(\{02,13\}\) only |
| good-only crossing matching | none | none |

The committed guard defeats the *weak* lemma by spending two exactness
equations on (E3); the new guard keeps (E3) and defeats *Theorem C* on
the saturating term instead.  They are therefore **complementary**, not
comparable: together they show that a proof must use exactness equations
beyond (E3) **and** rule out saturation.

---

## 5. What this changes in the committed cluster

* **C4 is strengthened**, \(2N\to3N/2\), and the new bound is *tight*
  (the exact \(K_4\) source attains it).  The mechanism is different:
  C4 orients each bad crossing pair and bounds out-degrees by \(2\)
  using C1 + C2; Lemma G bounds the *unordered* incidence by \(1\) per
  colour, which needs the two mixed-orientation cases and \(h_a(B)=1\).
* **The failing-shape table shrinks** from
  \(\{(0,2,N-2)\ \text{for all}\ N\}\cup\{(0,4,4),(2,2,2)\}\) to
  \(\{(0,2,6)\ \text{at}\ N=8\}\).  In particular the whole family
  \((0,2,N-2)\), \(N\ge10\), which the committed note called "a two-part
  split in disguise" and could not dispose of, is now disposed of by
  counting alone.
* **The §7.2 guard is joined by a complementary one.**  The committed
  note's negative statement was "the weak lemma is false; what a proof
  must consume is (E3)".  The new statement is sharper: (E3) is *not
  enough either*; what remains is exactly saturation.
* **Nothing here improves Theorem B.**  Theorem C is uniform in \(N\);
  the supply of a live split is still restricted to \(N\in\{6,8,10\}\).

A bookkeeping correction worth recording: an early draft of this
artifact (in scratch) classified a pair as bad only when it exhibited a
*one-dimensional single-coloured* essential covector, which silently
counted a pair with a higher-dimensional kernel as **good**.  The
checker here defines badness as `not is_good_pair` — the committed
definition — records the essential colour as `None` when it is not
canonically readable, and *requires* that the bad crossing pairs read off
the good-pair graph agree with the bad-pair table.  Under the corrected
definition the stall guard has five bad pairs (two of them without a
clean colour), not three.  Three of the five are the ones the earlier
count saw; the two extra pairs, \(\{2,5\}\) and \(\{3,4\}\), are
**non-crossing** (both endpoints lie in \(S_2\)), so the bad *crossing*
pairs are still exactly \(\{0,2\}\) and \(\{1,3\}\) and no statement of
this note changes — but the ledger now reports the honest count.

---

## 6. Composition, and what is still open

**Unconditional at \(N\ge10\) (counting only).**  By C4′+C5′, every live
split at even \(N\ge10\) has \(X>3N/2\) and therefore a good crossing
*pair*.  At \(N=8\) the same argument leaves only the shape \((0,2,6)\).

**But "a good crossing pair exists" is weaker than what Theorem C
delivers**, namely a nonzero crossing matching *all* of whose crossing
edges are good.  The counting route bounds the number of bad crossing
pairs; it says nothing about the cells of a prescribed matching.  The
saturation analysis of §3 is the bridge between the two, and it is the
part that is not closed.

**Do not frame \((0,2,6)\) as "the case to prove live".**  A parallel,
**unaudited** investigation (session scratch, **not in the repository**)
shows that shape
\((0,2,N-2)\) — indeed every split with an empty part — is provably
**dead** on an explicit family available at every even order: three
pairwise disjoint perfect matchings whose pairwise unions are single
Hamiltonian cycles.  For the 0/1 packet \(W_r=\mathrm{adj}(M_r)\) one has
\(h_r(S)\ne0\) iff \(S\) is a union of \(M_r\)-edges, and a live two-part
split would produce a third perfect matching of the cycle
\(M_r\cup M_s\), which has exactly two.  So the residual question at
\(N=8\) is not "is \((0,2,6)\) live".

**The \(N=8\) composition instead runs through a new SAT result**
(also *unaudited*, session scratch, **not in the repository**; a
shape-restricted variant of the committed engine, run in mode
"drop the shape \((0,2,n-2)\)"):
dropping the shape \((0,2,6)\) from the constraint system is **UNSAT at
\(n=8\)**, i.e. every diagonal packet with the three pure anchors has a
live split of some shape *other than* \((0,2,6)\) — and by C5′ every such
shape has \(X>3N/2\), hence a good crossing pair unconditionally.  With
the caveat of the previous paragraph, this composes to: *at \(N=8\), a
good crossing pair exists unconditionally*, but **not** yet to the
matching-level statement Theorem C wants.

**At \(N\ge10\) the analogous instance is open** (the \(n=10\)
drop-\((0,2,N-2)\) run is unresolved), so the uniform composition is not
closed.  The residual open statements are therefore

1. the saturating case of Theorem C — equivalently, excluding the scalar
   coincidence (6) for an *exact* source with a saturating colour class
   (the stall guard shows this needs exactness equations beyond
   (E1)–(E3));
2. the drop-\((0,2,N-2)\) SAT instance at \(n=10\), or a general-shape
   saturation argument that replaces it;
3. **uniformity of live-split existence itself**, which is Theorem B's
   own restriction to \(N\in\{6,8,10\}\) and is untouched here.

One further unaudited scratch observation, recorded because it
reformulates the engine uniformly: the **pencil identity**

\[
 \operatorname{haf}\bigl(x_0W_0+x_1W_1+x_2W_2\bigr)[B]
 =\sum_{(S_0,S_1,S_2)}x_0^{|S_0|/2}x_1^{|S_1|/2}x_2^{|S_2|/2}
   h_0(S_0)h_1(S_1)h_2(S_2),
\]

so "all split products vanish and \(h_r(B)=1\)" is exactly
\(\operatorname{haf}(\sum_rx_rW_r)=x_0^{k}+x_1^{k}+x_2^{k}\),
\(k=N/2\).
*(Corrected on audit: "exactly" overstates it — only the forward
implication holds; see §7.4 of
[`diagonal-termwise-census-and-pencil-guard.md`](diagonal-termwise-census-and-pencil-guard.md).)*
Its **two-colour shadow is always satisfiable** (the
alternating \(2k\)-cycle realises \(\operatorname{haf}(xA+yB)=x^k+y^k\)
for every \(k\ge2\)), which locates all the content in the simultaneous
three-colour condition and explains why no argument looking at two
colours at a time — equivalently at splits with an empty part — can
close the obstruction.

None of the four claims in this section is audited, and none of them is
used by the checker; they are recorded to keep the outlook honest.

---

## 7. Dead ends recorded

* **The Boolean route.**  Adding (E1)/(E2)/(E3) and liveness to the
  recurrence shadow of
  [`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md)
  cannot work: without the clauses (8) — which encode the *absence* of a
  live split — the all-ones assignment already models the recurrence, and
  (E1) only forces \(z_a(S)=0\) for \(u\in S\), \(v\notin S\), which the
  "zero forbids exactly one true term" clause accepts with **zero** true
  terms.
* **R1 in isolation.**  Every exactness equation with \(w_u=a\) is
  identically satisfied once (E1), (E2), (E3) hold — the stall guard's
  \(720/729\) is exactly this, and the checker verifies that no defect
  word has \(w_0=a\) or \(w_1=a\).  So the uncontracted expansion at
  \(u\) supplies nothing beyond (E3); the content lives in the words with
  \(w_u\ne a\), which is where the stall guard was built.
* **Random search for the stall.**  A naive randomised search does *not*
  find the stall configuration: purity of the deleted tensors imposes the
  linear conditions \(\sum_z\beta_zh_2(\text{big}\setminus\{p,z\})=0\)
  and its mirror, which random crossing rows violate.  The guard is
  constructed, not sampled.

---

## 8. Scope

1. Every statement about *exact* sources is a hand proof.  The machine
   checks are on instances: one genuinely exact source (\(K_4\) at
   \(N=4\), which has **no live split**, so Theorem C is *vacuous*
   there), constructed packets satisfying (E1)–(E3), and two **non-exact**
   guards.  As in the committed note, **no exact ternary source at
   \(N\in\{8,10\}\) is available** — showing that none exists is the
   project's aim — so the universal quantifier over exact sources is
   **not** machine-verified anywhere in this artifact.
2. Which statements are *required* where, precisely.  Lemma G's
   per-(site, colour) bound, the \(3N/2\) count and its tightness are
   required **only** on \(K_4\), the one packet satisfying the
   hypothesis; on the guards those are computed and reported, not
   required.  But the two *consequences* of Lemma G that Theorem C's
   ledger uses — "every colour class of bad crossing pairs is a
   matching" and Corollary C3's characterisation of the saturating
   families — **are** required on both guards as well, together with
   C4′ and the single-bad-pair identity.  That is over-checking:
   those packets are not exact, so the requirement is not entailed by
   the hypotheses, and it passes only because it happens to hold there.
   It is harmless (a failure would mean a genuine surprise worth
   investigating) but it should not be read as evidence for the lemma.
3. Theorem C is uniform in \(N\); the supply of a live split is not.
   Live-split existence remains Theorem B's, at \(N\in\{6,8,10\}\) and
   vacuous at \(N=6\).
4. Three residual soft spots in the machine checking, all disclosed
   above rather than hidden: the two-pair purity claim is *vacuous in
   the colour dimension* on \(K_4\) (§1), the stall guard's solved
   scalar cannot distinguish the correct formula from an earlier wrong
   one that happens to agree on this packet (§9, S1), and the stall
   construction is one degree less free than its block table suggests —
   the solve fixes \(A_{01}(1,1)\) **and** the coupled \(A_{25}(1,1)\)
   (§4).
5. The six-site non-existence theorem and the SAT theorem are **cited,
   not re-run**.
6. The scratch results quoted in §6 are **unaudited** and are not used by
   the checker.
7. Per project discipline this is a research reduction until
   independently audited.  **Krenn's conjecture remains open.**

---

## 9. Verification

~~~text
python3    computations/verify_good_crossing_matching_forcing.py
python3 -O computations/verify_good_crossing_matching_forcing.py
python3 -I computations/verify_good_crossing_matching_forcing.py
python3 -S computations/verify_good_crossing_matching_forcing.py
python3 -I -S computations/verify_good_crossing_matching_forcing.py
python3 -m py_compile computations/verify_good_crossing_matching_forcing.py
~~~

Runtime is **under two seconds**.  (`python3 -I` does not prepend the
script's directory to `sys.path`, so the checker inserts its own
directory, computed from `__file__`, before importing the committed
companion.)

The ledger hashes the **actual computed content**: the 196 deletion-identity
instances with their forbidden sets, words, values and corrections; the
Lemma F packets and their computed residue tensors; the distinct-colour
packet, its residue matching terms and its falsification probe; the
\(K_4\) blocks, matching tensor, per-(site, colour) census and full
deletion chain; both shape tables; the saturation-characterisation probe;
the conventions probes including the asymmetric-star packet and its
positive control; both guards' blocks, defect words, structure tables and
full Theorem C term lists; and the stall guard's crossing sum, **both**
solved cells, the one-step-off uniqueness value, anchors, structure and
scalar identity.  Every ledger boolean is computed — there is no
hard-coded truth value anywhere — and the committed companion's own
frozen digest is recorded, so a change of conventions upstream changes
this digest too.  Frozen digest:

~~~text
5d2ba758792054b0ddcf3bdee9dc81235bca91d8c1fe3ab8697db5644501fc73
~~~

Mutation-tested with **twenty** injections.  Nineteen raise under
**both** `python3` and `python3 -O`, with the **same** message, naming
the broken property; the twentieth (S1) is *silent by numerical
coincidence* and is listed as such — hiding it would be the more
dishonest choice.  Four entries come from audits of earlier versions of
this artifact:

* **M8/M16.**  The "saturating iff \(F_a\) covers \(B\setminus S_a\)"
  condition was never exercised in the negative direction on either
  guard; the combinatorial probe of §3 closes that hole.
* **A8/A8b.**  The \(K_4\) two-pair chain check was *vacuous* (empty
  residue, so any colour passed); the step-by-step chain of §1 closes it.
* **B14.**  The conventions probe pinned only the *first* deleted
  endpoint star, so a goodness test that ignored the second was
  invisible; the asymmetric-star packet with its positive control closes
  it.
* **S1.**  Reverting the stall solve to the earlier (wrong) formula
  \(+\alpha_p\beta_qh_2(S_2\setminus\{p,q\})/h_2(S_2)\) is **silent**,
  because on this packet its two errors cancel and it returns the same
  value \(1\).  No test can separate two formulas that agree on the only
  input they are given; what the checker enforces instead is the
  *equation* — \(h_1(S_1)h_2(S_2)=-C\) and \(H_B(\chi)=0\) on the final
  packet, plus the one-step-off uniqueness probe — and the formula was
  replaced outright rather than guarded.

| # | injection | message raised |
|---|---|---|
| M1 | `matchings_inside` drops the empty family \(T=\varnothing\) | deletion identity failed: the F-avoiding matching sum differs from the signed T-family sum |
| M2 | inclusion–exclusion sign dropped | deletion identity failed: the F-avoiding matching sum differs from the signed T-family sum |
| M3 | single-edge identity reads \(H_B\) instead of \(H_{B\setminus e}\) | single-edge deletion identity failed: the sum through an edge differs from A_e(w) H_{B minus e}(w) |
| M4 | identity family restricted to \(F=\varnothing\) | deletion identity checks never exercised a nonempty T: the identity would reduce to H_B = H_B and verify nothing about the correction |
| M5 | chain packet puts \(\lambda\) off the cell \((a,a)\) | Lemma F instance: (E2) is broken by the construction |
| M6 | Lemma F falsification probe stops perturbing the residue | Lemma F falsification probe is vacuous: perturbing the residue did not make the deleted tensor nonzero |
| M7 | deleted endpoint star keeps the omitted site | Lemma F distinct-colour instance: the two carriers are not bad pairs of distinct essential colours |
| M8 | **(audit; was silent)** saturation test drops the covering condition | the saturation characterisation probe is vacuous: every colour class covers B minus S_a, so the covering condition is never tested in the negative direction |
| M9 | (E3) declared to hold unconditionally | Lemma F falsification probe: a packet with a nonzero deleted tensor still satisfied (E3) at the first pair — the lemma's hypotheses would then not be load-bearing |
| M10 | the \(3N/2\) census reverted to the committed \(2N\) bound | C5' broken: a shape with X <= 3N/2 survives at some even N >= 10, so the unconditional good-crossing-pair claim at N >= 10 would fail |
| M11 | stall guard's solved cell shifted by one | stall guard: a pure anchor h_c(B) is not 1, so Lemma 0's full conclusion fails |
| M12 | stall guard's \(A_{13}\) purity correction \(u\otimes v\) dropped | stall guard: an exactness equation with w_0 = a or w_1 = a fails, although (E1)+(E2)+(E3) at both carriers force all of them |
| M13 | frozen ledger digest altered | good-crossing-matching forcing ledger changed |
| M14 | endpoint order destroyed in the imported machinery | conventions: oriented(v,u) with u < v must be the transpose |
| M15 | stall guard's free cell \(A_{03}(1,2)\) sign flipped | good-crossing-matching forcing ledger changed |
| M16 | **(audit)** the C3 probe loses its non-covering colour class | the saturation characterisation probe is vacuous: every colour class covers B minus S_a, so the covering condition is never tested in the negative direction |
| A8 | **(audit; was silent)** \(K_4\) chain expects a shifted residue colour | Lemma F failed on K_4: deleting one bad pair does not leave the pure colour-a tensor with coefficient 1/lambda |
| A8b | **(audit; was silent)** \(K_4\) two-pair chain coefficient perturbed | Lemma F failed on K_4: the two-pair same-colour chain is not the pure tensor with coefficient 1/(lambda_1 lambda_2) |
| B14 | **(audit; was silent)** goodness read from the first star only | conventions: is_good_pair ignored the second deleted endpoint star — a pair with one non-injective star was called good |
| S1 | **(audit)** stall solve reverted to the earlier wrong formula | **SILENT** — the two formulas agree on this packet (see above) |

| # | injection | message raised |
|---|---|---|
| M1 | `matchings_inside` drops the empty family \(T=\varnothing\) | deletion identity failed: the F-avoiding matching sum differs from the signed T-family sum |
| M2 | inclusion–exclusion sign dropped | deletion identity failed: the F-avoiding matching sum differs from the signed T-family sum |
| M3 | single-edge identity reads \(H_B\) instead of \(H_{B\setminus e}\) | single-edge deletion identity failed: the sum through an edge differs from A_e(w) H_{B minus e}(w) |
| M4 | identity family restricted to \(F=\varnothing\) | deletion identity checks never exercised a nonempty T: the identity would reduce to H_B = H_B and verify nothing about the correction |
| M5 | chain packet puts \(\lambda\) off the cell \((a,a)\) | Lemma F instance: (E2) is broken by the construction |
| M6 | Lemma F falsification probe stops perturbing the residue | Lemma F falsification probe is vacuous: perturbing the residue did not make the deleted tensor nonzero |
| M7 | deleted endpoint star keeps the omitted site | Lemma F distinct-colour instance: the two carriers are not bad pairs of distinct essential colours |
| M8 | **(found silent first)** saturation test drops the covering condition | the saturation characterisation probe is vacuous: every colour class covers B minus S_a, so the covering condition is never tested in the negative direction |
| M9 | (E3) declared to hold unconditionally | Lemma F falsification probe: a packet with a nonzero deleted tensor still satisfied (E3) at the first pair — the lemma's hypotheses would then not be load-bearing |
| M10 | the \(3N/2\) census reverted to the committed \(2N\) bound | C5' broken: a shape with X <= 3N/2 survives at some even N >= 10, so the unconditional good-crossing-pair claim at N >= 10 would fail |
| M11 | stall guard's solved cell shifted by one | stall guard: a pure anchor h_c(B) is not 1, so Lemma 0's full conclusion fails |
| M12 | stall guard's \(A_{13}\) purity correction \(u\otimes v\) dropped | stall guard: the solved cell A_01(1,1) is zero, so the split would not be live |
| M13 | frozen ledger digest altered | good-crossing-matching forcing ledger changed |
| M14 | endpoint order destroyed in the imported machinery | conventions: oriented(v,u) with u < v must be the transpose |
| M15 | stall guard's free cell \(A_{03}(1,2)\) sign flipped | good-crossing-matching forcing ledger changed |
| M16 | the C3 probe loses its non-covering colour class | the saturation characterisation probe is vacuous: every colour class covers B minus S_a, so the covering condition is never tested in the negative direction |
