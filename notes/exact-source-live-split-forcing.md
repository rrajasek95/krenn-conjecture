# Every exact ternary source at \(N\in\{6,8,10\}\) has a live split, and the split forces two off-diagonal cells

Checker:
[`computations/verify_exact_source_live_split_forcing.py`](../computations/verify_exact_source_live_split_forcing.py).

**Model.**  Sites carry endpoint-ordered aggregate blocks \(A_{uv}\) with
cells \(A_{uv}(i,j)\), \(i\) read at \(u\) and \(j\) at \(v\); exactness
is \(H_B(A)=\Delta_{B,3}\) over \(\mathbb C\).  This note works in the
**GENERAL (bicoloured) model**, where \(A_{uv}(i,j)\ne0\) is permitted for
\(i\ne j\) — the model of the open case \(N=8,d=3\) (DeepMind's Lean
`eqSystem8_no_solution_d3`, research open; see
[`references/REFERENCES.md`](../references/REFERENCES.md)), **not** the
monochromatic-edge restriction.  Diagonal results quoted here are used
only as necessary conditions on the diagonal shadow of a general source.

**Status.**  Lemma 0, Theorem A and the parity fact are *proved* (they
are polynomial identities and a counting argument); the checker verifies
them on matching-supported monomial and pseudorandom packets, counting
the nonvacuous equations (see the warning in §3).  The live-split
forcing theorem is *proved*, conditional on the already-established
UNSAT theorem of
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md),
hence available only at \(N\in\{6,8,10\}\) — and *vacuous* at \(N=6\),
where
[`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md)
Theorem 1.1 already excludes exact sources unconditionally.  The
essentiality structure lemma and its corollaries are *proved* by hand
here and *verified on instances* by the checker; C2 and C4 in particular
have **no** instance check on a packet satisfying their hypotheses (§8).
The full crossing-pairs-are-good lemma is **conjectured**, and its weak
form is **refuted** by the six-site guard of §7.2.  Krenn's conjecture
remains open.

## 1. Conventions

\(B\) is a site set of even size \(N\), \(V_u\cong\mathbb C^3\), and the
aggregate blocks \(A_{uv}\in V_u\otimes V_v\) are **endpoint-ordered**:
\(A_{uv}(i,j)\) reads \(i\) at \(u\) and \(j\) at \(v\), so
\(A_{vu}=A_{uv}^{\mathsf T}\).  This is the convention of
[`computations/verify_target_flattening_essential_star_pair_bound.py`](../computations/verify_target_flattening_essential_star_pair_bound.py)
(`oriented`, `perfect_matchings`, `matching_tensor`), and the checker
here re-implements those four functions verbatim in that convention.
Write

\[
 H_S(A)(w)=\sum_{M\in\operatorname{PM}(S)}\ \prod_{uv\in M}A_{uv}(w_u,w_v),
 \qquad H_\varnothing(A)=1,                                    \tag{1}
\]

and call \(A\) an **exact ternary source** on \(B\) when

\[
 H_B(A)=\Delta_{B,3}
   :=\textstyle\sum_{c=0}^{2}e_c^{\otimes B}.                   \tag{2}
\]

For a colour \(c\) put

\[
 W_c(u,v)=A_{uv}(c,c),\qquad
 h_c(S)=\operatorname{haf}W_c[S],\qquad h_c(\varnothing)=1.     \tag{3}
\]

The deleted endpoint star \(\sigma_u^{(v)}:V_u^*\to
\bigoplus_{x\notin\{u,v\}}V_x\),
\(\alpha\mapsto\bigoplus_x(\alpha\otimes\mathrm{id})A_{ux}\), is
equation (2) of
[`notes/target-flattening-essential-star-pair-bound.md`](target-flattening-essential-star-pair-bound.md).
Following that note, an unordered pair \(\{u,v\}\) is **good** when both
\(\sigma_u^{(v)}\) and \(\sigma_v^{(u)}\) are injective, and **bad**
otherwise; \(v\) is **essential at** \(u\) when
\(\ker\sigma_u^{(v)}\ne0\).

An **ordered even split** is an ordered partition
\(B=S_0\sqcup S_1\sqcup S_2\) into even (possibly empty) parts with no
part equal to \(B\); it carries the colouring \(\chi(u)=c\) for
\(u\in S_c\), which is non-constant.  The split is **live** when

\[
 h_0(S_0)\,h_1(S_1)\,h_2(S_2)\ne0.                              \tag{4}
\]

An edge \(uv\) is **crossing** for the split when \(\chi_u\ne\chi_v\).

## 2. Lemma 0 (the pure anchors)

**Lemma 0 (proved).**  For every block family and every colour \(c\),

\[
 H_B(A)(c,c,\dots,c)=h_c(B).                                    \tag{5}
\]

If \(A\) is an exact ternary source then \(h_c(B)=1\) for all three
colours.

*Proof.*  Put the constant word \(w\equiv c\) into (1).  Each matching
term becomes \(\prod_{uv\in M}A_{uv}(c,c)=\prod_{uv\in M}W_c(u,v)\), and
summing over all perfect matchings of \(B\) is by definition
\(\operatorname{haf}W_c[B]\).  Under (2) the left side is the coefficient
of \(e_c^{\otimes B}\) in \(\Delta_{B,3}\), namely \(1\).  \(\square\)

So exactness supplies the three **pure anchors** \(h_c(B)=1\) for free,
with no positivity and no cancellation hypothesis.  This is what feeds
the units of the Boolean system in §4.

## 3. Theorem A and the parity fact

**Theorem A (proved).**  For every block family and every ordered even
split with colouring \(\chi\),

\[
 H_B(A)(\chi)
  =h_0(S_0)h_1(S_1)h_2(S_2)
   +\!\!\sum_{M\ \text{crossing}}\ \prod_{uv\in M}A_{uv}(\chi_u,\chi_v),
                                                                \tag{6}
\]

the second sum running over perfect matchings with at least one crossing
edge.  If \(A\) is exact then, \(\chi\) being non-constant, the left side
is \(0\), so the crossing sum equals \(-h_0(S_0)h_1(S_1)h_2(S_2)\).

*Proof.*  Split \(\operatorname{PM}(B)\) into matchings all of whose
edges lie inside a part, and the rest.  A matching of the first kind is
exactly a triple of perfect matchings of \(S_0,S_1,S_2\); its weight is
\(\prod_c\prod_{uv\in M_c}A_{uv}(c,c)=\prod_c\prod_{uv\in M_c}W_c(u,v)\),
and summing over all such triples factors as the product of the three
hafnians.  The rest is the crossing sum.  \(\square\)

**Parity fact (proved).**  In any perfect matching \(M\) of \(B\) and any
part \(S_c\) of even size, the number of edges of \(M\) with exactly one
endpoint in \(S_c\) is even.  Consequently **a matching with at least one
crossing edge has at least two.**

*Proof.*  Every vertex of \(S_c\) is covered once; edges inside \(S_c\)
cover two of them, edges leaving cover one.  Hence
\(|S_c|=2\cdot(\text{inside})+(\text{leaving})\), so
\(\text{leaving}\equiv|S_c|\equiv0\pmod 2\).  If \(M\) had exactly one
crossing edge, joining \(S_a\) to \(S_b\) with \(a\ne b\), that edge
would be the only edge leaving \(S_a\), giving \(\text{leaving}(S_a)=1\),
odd.  \(\square\)

**A warning about vacuity.**  At \(N=4\) both sides of (5) and of (6) are
degree-two multilinear in the block entries, so a packet with a *single*
nonzero cell makes every matching term vanish: all such checks read
\(0=0\) and verify nothing.  (An earlier draft of this note used exactly
those \(54\) packets and claimed them as verification; that claim was
wrong and is retracted.)  The checker therefore uses
**matching-supported** degree-two monomials: for each of the three
perfect matchings of \(K_4\) and each of the \(9\times9\) cell choices,
put one cell on each matching edge.  The three perfect matchings of
\(K_4\) are pairwise edge-disjoint, so each of these \(243\) packets has
exactly one nonzero matching term and \(H_B(A)\ne0\).

On those packets the checker verifies (5) and (6) and counts the
**nonvacuous** equations — those whose common value is nonzero: \(54\)
for Theorem A (one per matching per ordered even split) and \(9\) for
Lemma 0 (one per matching per colour).  It refuses to pass if any of
these counts is zero.  It repeats the checks on deterministic
pseudorandom integer packets at \(N=4,6,8\) (\(18\), \(180\), \(1638\)
ordered even splits per packet, with \(210\), \(896\), \(3255\)
nonvacuous Theorem A equations), and verifies the parity fact
**exhaustively** over all \((\text{split},\text{matching})\) pairs at
\(N=4\) (\(54\)) and \(N=6\) (\(2700\)) — parity is a statement about
matchings alone, so that is a complete check of its combinatorial
content at those orders.

## 4. Live splits exist at \(N\in\{6,8,10\}\)

[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md)
proves a purely **Boolean** theorem.  Write \(z_c(S)=[\,h_c(S)\ne0\,]\).
Its system consists of

* the recurrence constraints (5)–(7) of that note: for every even \(S\),
  every pivot \(u\in S\) and \(t_c(S;u,v)=z_c(\{u,v\})\wedge
  z_c(S\setminus\{u,v\})\), (i) \(z_c(S)=1\) forces at least one true
  \(t_c\), and (ii) \(z_c(S)=0\) forbids **exactly one** true \(t_c\);
* the units \(z_c(\varnothing)=z_c(V)=1\);
* the clauses (8): \(\neg z_0(S_0)\vee\neg z_1(S_1)\vee\neg z_2(S_2)\)
  for every ordered even split.

**Theorem (cited, not re-verified here).**  That system is UNSAT for
\(n\in\{6,8,10\}\); the audit is
[`computations/verify_diagonal_recurrence_obstruction.py`](../computations/verify_diagonal_recurrence_obstruction.py).

**Theorem B (proved).**  Let \(A\) be an exact ternary source on \(B\)
with \(N=|B|\in\{6,8,10\}\).  Then \(A\) has a **live split**, and for
that split there is a perfect matching \(M\) of \(B\) with
\(\prod_{uv\in M}A_{uv}(\chi_u,\chi_v)\ne0\) and **at least two crossing
edges**.  In particular \(A\) has at least two nonzero **off-diagonal**
cells \(A_{uv}(\chi_u,\chi_v)\) with \(\chi_u\ne\chi_v\), lying on one
common nonzero matching.

*Proof.*  Each \(W_c\) of (3) is a symmetric zero-diagonal scalar edge
matrix over \(\mathbb C\) — symmetric because the endpoint-ordered
convention gives \(A_{vu}=A_{uv}^{\mathsf T}\), hence
\(W_c(v,u)=W_c(u,v)\) — so it is admissible data for the cited theorem.
Read the Boolean assignment \(z_c(S)=[\,h_c(S)\ne0\,]\) off the
actual matrices \(W_c\).  It satisfies the recurrence constraints:
they are the two support consequences of the pivot expansion
\(h_c(S)=\sum_{v\ne u}W_c(u,v)h_c(S\setminus\{u,v\})\) over a field —
(i) a nonzero sum needs a nonzero term, and (ii) a zero sum cannot have
exactly one nonzero term.  Lemma 0 supplies the units \(z_c(B)=1\), and
\(z_c(\varnothing)=1\) is the convention \(h_c(\varnothing)=1\).  If
every ordered even split satisfied \(h_0(S_0)h_1(S_1)h_2(S_2)=0\), all
clauses (8) would hold too and the assignment would be a model of an
UNSAT system.  Hence some ordered even split is live.  Apply Theorem A:
exactness makes the left side of (6) zero while the hafnian product is
nonzero, so the crossing sum is nonzero and some crossing matching \(M\)
has a nonzero term.  Every factor of that term is nonzero, and by the
parity fact \(M\) has at least two crossing edges.  \(\square\)

**Theorem B is vacuous at \(N=6\).**
[`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md),
Theorem 1.1, already proves **unconditionally** that no collection of
complex blocks satisfies \(H_6(A)=\Delta_{6,3}\).  So at \(N=6\)
Theorem B's hypothesis is empty and it says nothing new; its content is
at \(N=8\) and \(N=10\) only.  It is stated for \(\{6,8,10\}\) because
that is the range of the Boolean engine, not because \(N=6\) contributes.

The checker verifies its side of this: that the hafnian shadow of **each
of the seven tested block families** really is a model of the recurrence
constraints (5520 pivot constraints, exhaustive in \(S\), \(u\) and
\(c\) at \(N=4,6,8\)), and that Lemma 0's units hold on the exact
packet.  The statement for an *arbitrary* block family is the hand proof
above, not the machine check.  The checker does **not** re-run the SAT
proof.

## 5. The essentiality structure lemma

**Lemma E (proved).**  Let \(A\) be an exact ternary source on \(B\), let
\(u\ne v\), put \(B'=B\setminus\{u,v\}\), \(G=H_{B'}(A)\), and let
\(0\ne\varphi\in\ker\sigma_u^{(v)}\), i.e.
\((\varphi\otimes\mathrm{id})A_{ux}=0\) for every \(x\notin\{u,v\}\).
Put \(\psi=(\varphi\otimes\mathrm{id})A_{uv}\in V_v^*\).  Then, for every
colour \(j\) and every word \(y\) on \(B'\),

\[
 \boxed{\ \varphi_j\,[\,y\equiv j\,]=\psi(j)\,G(y).\ }          \tag{$*$}
\]

Consequently there is exactly one colour \(a\) with \(\varphi_a\ne0\),
and with \(\lambda=A_{uv}(a,a)\):

* **(E1)** row \(a\) of \(A_{ux}\) vanishes for every \(x\notin\{u,v\}\);
* **(E2)** row \(a\) of \(A_{uv}\) equals \(\lambda e_a\) with
  \(\lambda\ne0\);
* **(E3)** \(H_{B'}(A)=\lambda^{-1}e_a^{\otimes B'}\) — a **nonzero pure
  colour-\(a\)** tensor.

*Proof of \((*)\).*  Expand (1) at \(u\) by the partner of \(u\):

\[
 H_B(A)(i,j,y)=A_{uv}(i,j)\,H_{B'}(A)(y)
   +\sum_{x\in B'}A_{ux}(i,y_x)\,H_{B\setminus\{u,x\}}(A)(j,y|_{B'\setminus x}).
                                                                \tag{7}
\]

Contract the \(u\)-mode with \(\varphi\).  Every term of the sum over
\(x\in B'\) carries the factor \(\sum_i\varphi_iA_{ux}(i,y_x)=0\), so the
sum dies **term by term**; this is the star-contraction step, and it is
the crux.  The first term becomes \(\psi(j)G(y)\).  On the left,
\(\Delta_{B,3}(i,j,y)=[\,i=j\ \text{and}\ y\equiv j\,]\), so
\(\sum_i\varphi_i\Delta_{B,3}(i,j,y)=\varphi_j[\,y\equiv j\,]\).  This is
\((*)\).

*Proof of the consequences.*  Pick \(a\) with \(\varphi_a\ne0\).  Taking
\(j=a\), \(y\equiv a\) in \((*)\) gives
\(\varphi_a=\psi(a)G(a,\dots,a)\ne0\), so \(\psi(a)\ne0\) and
\(G(a,\dots,a)\ne0\).  Taking \(j=a\) and any \(y\not\equiv a\) gives
\(0=\psi(a)G(y)\), hence \(G(y)=0\): \(G\) is supported on the single
word \(a\dots a\).  For \(j\ne a\), taking \(y\equiv a\) gives
\(0=\psi(j)G(a,\dots,a)\), so \(\psi(j)=0\); then taking \(y\equiv j\)
gives \(\varphi_j=\psi(j)G(j,\dots,j)=0\).  So \(\varphi=\varphi_ae_a\)
is single-coloured.  (E1) is then
\(\varphi_aA_{ux}(a,\cdot)=0\).  (E2): \(\psi=\varphi_aA_{uv}(a,\cdot)\)
vanishes off \(a\) and is nonzero at \(a\), so row \(a\) of \(A_{uv}\) is
\(\lambda e_a\) with \(\lambda=A_{uv}(a,a)=\psi(a)/\varphi_a\ne0\).
(E3): \(\varphi_a=\psi(a)G(a,\dots,a)=\varphi_a\lambda\,G(a,\dots,a)\)
gives \(G(a,\dots,a)=\lambda^{-1}\).  \(\square\)

Call \(a\) the **essential colour** of the ordered pair \((u,v)\).

## 6. Corollaries

**C1 (colour injectivity; proved).**  Distinct essential neighbours of
\(u\) have distinct essential colours.  Hence a site has at most three
essential neighbours.

*Proof.*  Let \(v\ne v'\) both be essential at \(u\) with the same colour
\(a\).  (E1) for \((u,v)\) makes row \(a\) of \(A_{uv'}\) vanish (since
\(v'\notin\{u,v\}\)), while (E2) for \((u,v')\) makes it
\(\lambda'e_a\ne0\).  \(\square\)

This re-derives, from the exactness structure rather than from
\(\mathbb F_2\)-subspace combinatorics, the \(\le3\) bound of
[`notes/target-flattening-essential-star-pair-bound.md`](target-flattening-essential-star-pair-bound.md)
equation (3).

**C2 (the \(a=\chi_u\) branch; proved).**  Let \(A\) be exact, let
\((S_0,S_1,S_2)\) be a **live** split, let \(\{u,v\}\) be a **crossing**
pair, and let \(v\) be essential at \(u\) with essential colour \(a\).
Then \(a\ne\chi_u\).

*Proof.*  Suppose \(a=\chi_u\).  Liveness gives
\(h_{\chi_u}(S_{\chi_u})\ne0\), so some perfect matching \(M\) of
\(S_{\chi_u}\) has \(\prod_{xy\in M}A_{xy}(\chi_u,\chi_u)\ne0\).  In
\(M\), \(u\) is matched to some \(x\in S_{\chi_u}\); since \(\{u,v\}\) is
crossing, \(v\notin S_{\chi_u}\), so \(x\notin\{u,v\}\).  By (E1) row
\(a=\chi_u\) of \(A_{ux}\) vanishes, so
\(A_{ux}(\chi_u,\chi_u)=0\) and the product is zero.  \(\square\)

C2 is exactly the \(a=\chi_u\) branch of the crossing-pairs-are-good
question, and it is settled.  What remains open is the branch
\(a\notin\{\chi_u\}\) — see §8.

**C3 (disjoint-bad-pair rigidity; proved).**  Let \(A\) be exact and let
\(\{u,v\}\), \(\{u',v'\}\) be **disjoint** pairs with \(v\) essential at
\(u\) of colour \(a\) and \(v'\) essential at \(u'\) of colour \(a'\).
If \(a\ne a'\) then \(H_{B\setminus\{u,v,u',v'\}}(A)\equiv0\).

*Proof.*  By (E3) for \((u,v)\), \(G=H_{B\setminus\{u,v\}}(A)\) is
\(\mu\,e_a^{\otimes}\) with \(\mu=\lambda^{-1}\ne0\).  Expand \(G\) at
\(u'\) as in (7) — legitimate, since \(u',v'\) lie in
\(B\setminus\{u,v\}\) — and contract the \(u'\)-mode with
\(e_{a'}\).  All terms over \(x\in B\setminus\{u,v,u',v'\}\) die by (E1)
for \((u',v')\), leaving
\(e_{a'}\!\cdot\!G(\cdot,j,y)=\psi'(j)H_{B\setminus\{u,v,u',v'\}}(y)\).
The left side is \(\mu[\,a'=a\,][\,j=a\,][\,y\equiv a\,]=0\) because
\(a'\ne a\).  Taking \(j=a'\), where \(\psi'(a')=\lambda'\ne0\) by (E2),
forces \(H_{B\setminus\{u,v,u',v'\}}(y)=0\) for every \(y\).
\(\square\)

At \(N=4\) the deleted tensor is \(H_\varnothing=1\ne0\), so **disjoint
bad pairs of a four-site exact source must share their essential
colour** — the checker confirms this on the \(K_4\) source (three
disjoint bad-pair choices, all same-colour, zero distinct-colour
choices).

**C4 (counting bound; proved).**  Let \(A\) be exact and
\((S_0,S_1,S_2)\) live, with
\(X=|S_0||S_1|+|S_0||S_2|+|S_1||S_2|\) crossing pairs.  Then

\[
 \#\{\text{good crossing pairs}\}\ \ge\ X-2N.                   \tag{8}
\]

*Proof.*  Orient every bad crossing pair \(\{u,v\}\) toward an endpoint
witnessing badness (say \(u\), when \(v\) is essential at \(u\)); every
bad pair receives at least one orientation.  By C1 the essential colours
at \(u\) are distinct, and by C2 none of the crossing ones equals
\(\chi_u\); so at most \(2\) of the three colours are available and \(u\)
has out-degree \(\le2\).  Hence at most \(2N\) bad crossing pairs.
\(\square\)

**C5 (which shapes escape the count; proved).**  Write a shape as
\(a\le b\le c\), all even, \(a+b+c=N\), \(c\ne N\).  Then for every even
\(N\ge10\) the **only** shape with \(X\le2N\) is \((0,2,N-2)\), where
\(X=2N-4\).

*Proof.*  Two cases.

*Case \(a\ge2\).*  Rearranging,

\[
 X-2N=ab+ac+bc-2a-2b-2c=a(b-2)+b(c-2)+c(a-2).                   \tag{9}
\]

With \(a,b,c\ge2\) every summand in (9) is \(\ge0\), so \(X\ge2N\), and
equality forces \(a(b-2)=b(c-2)=c(a-2)=0\); since \(a,b,c\ne0\) this
means \(a=b=c=2\), i.e. \(N=6\).  Hence \(X>2N\) whenever \(a\ge2\) and
\(N\ge8\).

*Case \(a=0\).*  Then \(c\ne N\) forces \(b\ge2\), and \(X=bc=b(N-b)\),
which is strictly increasing in \(b\) on \([2,N/2]\).  At \(b=2\),
\(X=2N-4\le2N\) — the surviving shape.  At \(b=4\), \(X=4N-16>2N\)
exactly when \(N>8\).  So for \(N\ge10\) only \(b=2\) survives.
\(\square\)

The small orders are the exceptions, tabulated exhaustively by the
checker:

| \(N\) | shapes with \(X\le2N\) |
|---|---|
| 6 | \((0,2,4)\!:\!X=8\), \((2,2,2)\!:\!X=12\) |
| 8 | \((0,2,6)\!:\!X=12\), \((0,4,4)\!:\!X=16\) |
| \(\ge10\) | only \((0,2,N-2)\!:\!X=2N-4\) (C5) |

The checker also re-verifies C5's conclusion by exhaustion for every
even \(N\) up to \(200\) — a guard on the proof, not a substitute for it.

So for every live split whose shape is not in this list, a good crossing
pair exists **unconditionally**.  The counting route dies precisely on
the near-degenerate shapes — in particular on the whole family
\((0,2,N-2)\), which is a two-part split in disguise.

## 7. Two guards

### 7.1 The omega packet: it is (E3) that is not free

The eight-site integral aggregate packet of
[`notes/curved-two-chart-omega-diagonal-row-guard.md`](curved-two-chart-omega-diagonal-row-guard.md),
table (6), has all three pure anchors \(h_c(B)=1\), \(16\) good pairs of
\(28\), a **unique** live split up to part order (\(pacd\mid qbrs\), in
its six colourings), and its crossing graph **equals** its good-pair
graph.  It is diagonal, so its crossing sum vanishes identically and
Theorem A makes each of the six live-split words evaluate to \(1\) rather
than \(0\): those six words are exactly the packet's six exactness
defects.  The checker verifies all of this.

The packet's negative content must be stated precisely, and an earlier
draft of this note over-reached.  At all \(21\) of its essential ordered
pairs the kernel is one-dimensional, its basis covector **is**
single-coloured, and **(E1) and (E2) both hold**.  What fails — at all
\(21\) — is identity \((*)\) and **(E3)**.  So the correct statement is:

> the omega packet's satisfied rows do not imply **(E3)**.

Single-colouredness, (E1) and (E2) are not what Lemma E needs the omitted
equations for; the purity of \(H_{B\setminus\{u,v\}}(A)\) is.  The
checker computes all four properties at all \(21\) covectors and pins the
counts in the ledger.

**C2 and C4 are vacuous on this packet.**  Its crossing graph equals its
good-pair graph, so it has **zero** bad crossing pairs, and the C2/C4
requires read \(0\le16\) and \(16\ge0\).  They carry content only on the
six-site guard of §7.2 (12 ordered C2 instances there).  The checker
records the exercised-instance count per packet so this cannot be
mistaken for coverage.

### 7.2 The six-site guard: the weak lemma is refuted

Take \(B=\{0,\dots,5\}\) and the one-factorization of the **triangular
prism** (triangles \(\{0,2,3\}\) and \(\{1,4,5\}\), joined by
\(01\mid24\mid35\)) — a cubic subgraph of \(K_6\), not \(K_6\) itself,
which would need five one-factors:

\[
 c=0:\ 01\mid23\mid45,\qquad
 c=1:\ 24\mid03\mid15,\qquad
 c=2:\ 35\mid02\mid14,                                         \tag{10}
\]

each listed edge contributing the diagonal cell \(A_{uv}(c,c)=1\), plus
**two off-diagonal cells**

\[
 A_{03}(0,2)=1,\qquad A_{15}(0,2)=-1.                           \tag{11}
\]

The second value is not chosen: the checker solves the live-split
colouring equation \(H_B(A)(\chi)=0\) exactly for it (the coefficient is
affine in that cell) and obtains \(-1\).  This packet satisfies:

* all three pure anchors \(h_c(B)=1\) — the full conclusion of Lemma 0;
* \(S_0=\{0,1\}\), \(S_1=\{2,4\}\), \(S_2=\{3,5\}\) is live, with
  \(h_0h_1h_2=1\), and it is the **unique** live split;
* **727 of the 729** exactness equations \(H_B(A)(w)=\Delta_{B,3}(w)\),
  including every constant word and every live-split colouring equation;
* Theorem A with a nonzero crossing sum \(-1\), carried by the single
  nonzero crossing matching \(03\mid15\mid24\), whose two crossing edges
  are exactly the two carriers of (11) — the parity fact in action.

And yet **both** forced cells sit on **bad** crossing pairs: the good
pairs are \(01,04,05,12,13,25,34,35\), and \(\{0,3\}\), \(\{1,5\}\) are
not among them.  So

> the weak form of the crossing-pairs-are-good lemma — "the pure
> anchors plus the live-split colouring equations force a cell of a
> nonzero crossing matching onto a good pair" — is **false**.

The guard is consistent with everything proved above.  Every one of its
six bad crossing pairs has a single-coloured essential covector at both
endpoints, and in all twelve ordered cases the essential colour is the
**third** colour, distinct from both endpoints' part colours — C2 holds
with room to spare.  Its counting is also tight rather than violated:
\(X=12=2N\), and the maximum crossing-essential degree is exactly the
bound \(2\).  The shape is \((2,2,2)\), the first row of the §6 table —
precisely where counting alone gives nothing.

**What the guard breaks is (E3), and among the crossing pairs it breaks
it exactly at the two carriers.**  Single-colouredness, (E1) and (E2)
hold at all \(14\) essential ordered pairs of the packet (all kernels
one-dimensional).  Among the six **bad crossing** pairs, (E3) holds at
\(\{0,2\},\{1,4\},\{2,3\},\{4,5\}\) and fails at \(\{0,3\}\) and
\(\{1,5\}\) — the two pairs carrying the forced cells.  For
completeness: over *all* essential pairs, (E3) — and identity \((*)\)
with it — fails at three unordered pairs, \(\{0,3\}\), \(\{1,5\}\) and
\(\{2,4\}\); the third is a **non**-crossing pair (both endpoints lie in
\(S_1\)) and so plays no role in the crossing-pairs question.  The
checker's ledger records the full \(14\)-pair census, not only the
crossing slice.
Explicitly, at \(\{0,3\}\) with essential colour \(a=1\) and
\(\lambda=1\),

\[
 H_{B\setminus\{0,3\}}(A)
   =e_1^{\otimes\{1,2,4,5\}}\ -\ e_0\otimes e_1\otimes e_1\otimes e_2,
                                                                \tag{12}
\]

which is \(\lambda^{-1}e_a^{\otimes}\) **plus one impurity**; and the
impurity's word is the restriction to \(\{1,2,4,5\}\) of the packet's own
exactness defect \(w=(1,0,1,1,1,2)\).  At \(\{1,5\}\) the same thing
happens with the other defect \(w=(0,1,1,2,1,1)\):
\(H_{B\setminus\{1,5\}}(A)=e_1^{\otimes\{0,2,3,4\}}
+e_0\otimes e_1\otimes e_2\otimes e_1\).  So the guard
survives by spending exactly two of the \(729\) equations, and it spends
them where (E3) would otherwise bite.

## 8. What is proved, what is conjectured

**Proved.**  Lemma 0; Theorem A; the parity fact; Theorem B (live-split
forcing, at \(N\in\{6,8,10\}\), citing the SAT theorem — and *vacuous*
at \(N=6\), where
[`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md)
Theorem 1.1 already excludes exact sources unconditionally, so the real
content is at \(N=8,10\)); Lemma E \((*)\), (E1), (E2), (E3); C1 colour
injectivity; C2 the \(a=\chi_u\) branch; C3 disjoint-bad-pair rigidity;
C4 the \(\ge X-2N\) count; C5 the failing-shape classification.

**Verified on instances only, and the instances are uneven.**  §5 (Lemma
E: \((*)\), (E1)–(E3)), C1 and C3 are checked by machine on the exact
\(K_4\) three-one-factorization source — twelve essential ordered pairs,
every kernel one-dimensional.  **C2 and C4 are not exercised there at
all**: \(K_4\) has no live split, so there is no crossing pair to test.
They are also **vacuous on the omega guard**, whose crossing graph equals
its good-pair graph (zero bad crossing pairs).  The only packet on which
C2 and C4 carry content is the six-site guard of §7.2 (twelve ordered C2
instances), and that packet is **not exact** — it satisfies 727 of 729
exactness equations.  So C2 and C4, the two corollaries that actually
feed the crossing-pairs question, have no machine check on a packet
satisfying their hypotheses.  The hand proofs in §6 are what carries
them; the checker records the exercised-instance counts per packet so
this gap is visible in the ledger rather than hidden.

The universal quantifier over exact sources is *not* machine-verified
anywhere in this artifact.

**Conjectured (open).**

> **Crossing-pairs-are-good.**  Let \(A\) be an exact ternary source,
> \((S_0,S_1,S_2)\) a live split, \(M\) a nonzero crossing matching, and
> \(uv\in M\) a crossing edge.  Then \(\{u,v\}\) is a good pair.

Its weak form is refuted by §7.2, so any proof must consume exactness
equations beyond the anchors and the split colouring equations.  The
guard says precisely which: **(E3)**.

**The remaining crisp statement.**  By Lemma E, if such a \(\{u,v\}\)
were bad with \(v\) essential at \(u\) of colour \(a\), then
\(a\ne\chi_u\) (C2) and

\[
 H_{B\setminus\{u,v\}}(A)=\lambda^{-1}e_a^{\otimes(B\setminus\{u,v\})},
 \qquad \lambda=A_{uv}(a,a)\ne0.                                \tag{13}
\]

The whole question is whether (13) can coexist with the liveness of the
split, given that \(A_{uv}(\chi_u,\chi_v)\ne0\) with \(\chi_u\ne\chi_v\).
This is the E3-purity-versus-liveness statement.  Note that Theorem A
cannot be applied to \(B\setminus\{u,v\}\) directly: removing a crossing
pair leaves \(S_{\chi_u}\setminus\{u\}\) and \(S_{\chi_v}\setminus\{v\}\)
both of **odd** size, so the restricted colouring is not an even split.
Closing that gap is the open work.

**Uniformity in \(N\) is open.**  Theorem B is available only at
\(N\in\{6,8,10\}\), because that is where the Boolean engine of
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md)
closed.  That note states its own obstacle to induction: a realization at
larger order does not automatically restrict to a common feasible
principal set in all three colours.  Nothing here improves that.

**What the label-split application still needs.**  Theorem B delivers
*existence* of two off-diagonal cells on a common nonzero crossing
matching.  The application wants those cells to sit on **good** pairs, so
that the good-pair machinery of
[`notes/target-flattening-essential-star-pair-bound.md`](target-flattening-essential-star-pair-bound.md)
and the curvature selection of
[`notes/unconditional-curvature-line-selection.md`](unconditional-curvature-line-selection.md)
can be applied at those cells; that is exactly the conjecture above.  A
partial substitute is available and unconditional: if \(pq\) and \(rs\)
are two crossing edges of the *same* nonzero crossing matching, then
\(A_{pq}(\chi_p,\chi_q)A_{rs}(\chi_r,\chi_s)\ne0\), so the first product
of the literal source-block minor
\(A_{pq}(a,b)A_{rs}(c,d)-A_{pr}(a,c)A_{qs}(b,d)\) of
[`notes/unconditional-curvature-line-selection.md`](unconditional-curvature-line-selection.md)
equation (3) is nonzero, and the minor vanishes only through an exact
coincidence with the swapped product.  That observation does not need
goodness, but it also does not supply it.

## 9. Scope

1. Live-split existence holds only at \(N\in\{6,8,10\}\), and is
   **vacuous at \(N=6\)**
   ([`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md)
   Theorem 1.1 already excludes exact six-site sources unconditionally).
   Uniformity in \(N\) is open, and this note does not attempt it.
2. Lemma E and its corollaries are hand proofs.  The checker verifies
   them on instances (one genuinely exact source, two guards), not over
   all exact sources.
3. The \(K_4\) source is the only exact packet used, and \(N=4\) is
   outside \(\{6,8,10\}\): it has no live split at all, so it exercises
   Lemma E, C1 and C3 but **not** C2 or C4.  C2 and C4 are vacuous on
   the omega guard (zero bad crossing pairs) and are exercised only on
   the six-site guard, which is not exact.  No exact ternary source at
   \(N\in\{6,8,10\}\) is available to test on — showing that none exists
   is the project's aim — so the instance checks necessarily use a
   smaller exact source together with non-exact guards.
4. The SAT theorem is cited, not re-run; so is Theorem 1.1 of the
   six-site obstruction.
5. Two convention probes exist purely to keep otherwise-dead code
   honest: an endpoint-order probe (the transpose branch of `oriented`
   inside the star contraction is not exercised by any packet the note
   reasons about) and a multi-dimensional-kernel probe (Lemma E makes
   every essential kernel of an exact source one-dimensional, so the
   unsafe-read branch of the essential table would never fire).  They
   verify the code, not the mathematics.
6. Per project discipline this is a research reduction until
   independently audited.  Krenn's conjecture remains open.

## 10. Verification

~~~text
python3 computations/verify_exact_source_live_split_forcing.py
python3 -O computations/verify_exact_source_live_split_forcing.py
python3 -I computations/verify_exact_source_live_split_forcing.py
python3 -S computations/verify_exact_source_live_split_forcing.py
python3 -I -S computations/verify_exact_source_live_split_forcing.py
~~~

Runtime is about two seconds.  The ledger hashes the actual computed
data — the pseudorandom packets used for the identity checks **and**
those drawn for the Boolean-shadow section, the \(K_4\) blocks and its
computed matching tensor, its essential-colour table, both guards'
blocks, defect words and per-covector \((*)\)/(E1)/(E2)/(E3) tables, and
the failing-shape table — not hard-coded constants, and every ledger
boolean is computed.  Frozen digest:

~~~text
a0bf3107ad8a8c175bb5c905f725b458bd10c6bed44ddaf0273837c0a74bb5fd
~~~

Mutation-tested with fifteen injections; each raises under **both**
`python3` and `python3 -O`, with a message naming the broken property.
M11 and M12 are the two injections an independent audit found *silent*
against the first version of this artifact; the endpoint-order probe and
the Boolean-shadow packet hash were added to close them.

| # | injection | message raised |
|---|---|---|
| M1 | `oriented` drops the transpose (endpoint order destroyed) | six-site guard: a bad crossing endpoint has no single-colour essential covector |
| M2 | `hafnian` returns \(0\) on the empty set | Theorem A identity failed: split coefficient != product + crossing sum |
| M3 | deleted endpoint star keeps the omitted site | K_4: expected all twelve ordered pairs to be essential |
| M4 | one \(K_4\) one-factor edge recoloured | the K_4 one-factorization packet is not an exact ternary source |
| M5 | six-site guard's solved off-diagonal cell shifted by \(1\) | six-site guard: the live split violates its colouring equation |
| M6 | crossing-matching filter admits non-crossing matchings | Theorem A identity failed: split coefficient != product + crossing sum |
| M7 | Boolean shadow pivot term drops the pair literal | Boolean shadow: a dead hafnian had exactly one supported pivot term |
| M8 | identity \((*)\) declared to hold unconditionally | omega guard: identity (\*) or (E3) did not fail at every essential pair |
| M9 | crossing pairs read as same-part pairs | omega guard: the crossing graph is not the good-pair graph |
| M10 | frozen ledger digest altered | exact-source live-split forcing ledger changed |
| M11 | **(audit)** star contraction reads the raw block instead of `oriented` | endpoint order: contract at the right endpoint did not read the u-mode row of A_vu = A_uv^T |
| M12 | **(audit)** Boolean-shadow pseudorandom seed changed | exact-source live-split forcing ledger changed |
| M13 | monomial packets reverted to the vacuous single-cell form | matching-supported monomial packet has H_B = 0, so its identity checks would be vacuous |
| M14 | C5's boundary moved from \(N\ge10\) to \(N\ge8\) | failing-shape claim broken: some even N >= 10 has a shape other than (0, 2, N-2) with X <= 2N |
| M15 | essential table reads a colour off a multi-dimensional kernel | essential_table read a colour off a multi-dimensional kernel: a covector basis is not a canonical colour |
