# Termwise-dead configurations are rank-3 and cubic, and \(K_4\) is the only cubic graph with exactly three perfect matchings

Checker:
[`computations/verify_termwise_rank3_cubic_uniqueness.py`](../computations/verify_termwise_rank3_cubic_uniqueness.py).

All conventions are those of
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md):
\(V\) is a vertex set of even size \(n=2k\), \(W_0,W_1,W_2\) are symmetric
zero-diagonal scalar edge matrices over a field \(K\),
\(h_c(S)=\operatorname{haf}W_c[S]\) with \(h_c(\varnothing)=1\), and a
*split* is a proper ordered partition \(V=S_0\sqcup S_1\sqcup S_2\) into
even sets — *proper* meaning no part equals \(V\).  A split is **live**
when \(h_0(S_0)h_1(S_1)h_2(S_2)\ne0\).  The packet is **anchored** when
\(h_c(V)\ne0\) for all three \(c\), and **termwise-dead** when it is
anchored and no split is live.  Termwise-deadness is exactly the
hypothesis system (2) of the committed proof, and its insolubility for
every \(k\ge3\) is DIAG-\(\infty\).

**Status.**  Theorems A, B and C below are **proved by hand** in this
note and verified on non-vacuous instances by the checker; Theorem B is
a standalone graph theorem and is stated self-contained.  The **stall**
of §5 is **open** and stated exactly, together with two proved
narrowings and a measurement that closes \(k=3\) without any
cancellation hypothesis and demonstrably fails to do so at \(k=4\).
Nothing here settles the termwise condition with arbitrary cancellation
for \(k\ge6\).  Per project discipline this is a research reduction
until independently audited.  **Krenn's conjecture remains open.**

**Companions.**

* [`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md)
  — the committed SAT theorem: termwise-deadness is impossible at
  \(n\in\{6,8,10\}\), i.e. \(k\le5\), **with arbitrary cancellation
  allowed**.  Theorem C here is the exactly complementary statement:
  every \(k\ge3\), **no cancellation allowed**.  Neither contains the
  other, and §4.5 spells out the shape of the gap.
* [`notes/diagonal-termwise-census-and-pencil-guard.md`](diagonal-termwise-census-and-pencil-guard.md)
  (committed, audited) — the census that identifies the six \(0/1\)
  termwise-dead packets at \(n=4\), proves the Hamiltonian-triple lemma
  for the round-robin family \(D(n)\) used throughout below, and audits
  the \(2k\)-cycle pencil solutions over \(\mathbb Q(\zeta_{2k})\) with a
  full polynomial hafnian.  Every statement this note borrows from it
  (the Hamiltonicity of the \(D(n)\) unions, the \(n=4\) census count,
  the pencil realization) is nevertheless **recomputed independently by
  this note's own checker**, over an integer ring rather than a field,
  so the two artifacts corroborate rather than depend on each other.
* [`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md)
  — its Theorem B is the reason diagonal packets are the right shadow to
  study: an exact ternary source induces one through
  \(W_c(u,v)=A_{uv}(c,c)\).  Everything below is about that shadow, not
  about exact sources.
* **Session scratch** (not in the repository): the Fermat/pencil
  geometry — pencil points, their Fermat membership, the tangent lemma,
  and the alternating \(2k\)-cycle counterexamples to the *summed*
  pencil form of DIAG-\(\infty\).  §2.6 shows Theorem A renders all of
  that **vacuous on termwise-dead configurations**, and the checker
  reproduces the counterexample family exactly, over
  \(\mathbb Z[\zeta_{2k}]\), for \(k=2,\dots,6\).

---

## 0. Summary

**Theorem A (proved, §2).**  Let the packet be anchored.  Then
termwise-deadness forces (A1) below, and (A1) alone — a strictly weaker
hypothesis — forces (A2)–(A5):

* **(A1) TW2 support constraint.**  \(W_c(u,v)\ne0\;\Rightarrow\;
  h_{c'}(V\setminus\{u,v\})=0\) for both \(c'\ne c\).
* **(A2)** every **essential** edge is monochromatic and the three
  essential graphs are pairwise disjoint;
* **(A3)** every vertex carries an essential edge of **every** colour;
* **(A4) every star has rank exactly 3** in the pencil
  \(L=x_0W_0+x_1W_1+x_2W_2\);
* **(A5)** a two-coloured edge is **triply inessential**.

**Theorem B (proved, §3; standalone graph theory).**  \(K_4\) is the
only cubic graph whose three perfect matchings form a proper
3-edge-colouring and are its only perfect matchings.

**Theorem C (proved, §4; uniform in \(k\)).**  For every \(k\ge3\) there
is **no anchored matching-faithful termwise-dead packet**.
Matching-faithfulness (§4.1) is implied by nonnegative entries, by
\(0/1\) entries, and by algebraically independent entries.  It is a real
hypothesis, not a formality: §4.4 exhibits, at \(n=8,10,12\), induced
parts that a colour perfectly matches and on which a single sign change
makes \(h_c(S_c)=0\).

**The stall (open, §5).**  What survives is a pure cancellation
question, narrowed by (S1) and (S2) and measured at \(k=3,4\).

**The \(k=2\) boundary (§6).**  \(K_4\) *is* termwise-dead; Theorem A
holds there, and inside Theorem B the hypothesis \(k\ge3\) enters at
exactly two places, (B1) and (B2)/(B3).

---

## 1. Two standing facts

**Fact 1 (pair hafnians).**  For a two-element set,
\(h_c(\{u,v\})=W_c(u,v)\); and \(h_c(\varnothing)=1\).  Both are
immediate from the definition.  The checker re-derives the first from its
hafnian table rather than assuming it, but only where it is used: on all
600 signed packets (every pair, every colour) and at every pair named by
a TW2 violation.  It is *not* re-derived on every packet the checker
builds.

**Fact 2 (Laplace at a chosen pivot).**  For every even \(S\) and every
\(u\in S\),

\[
 h_c(S)=\sum_{v\in S\setminus\{u\}}W_c(u,v)\,h_c(S\setminus\{u,v\}).
 \tag{1}
\]

This is the hafnian expansion the committed engine's recurrence shadow
is built from.

---

## 2. Theorem A

Throughout §2, \(k\ge2\) and the packet is anchored.

### 2.1 (A1): termwise-deadness implies TW2

**(A1).**  *If the packet is termwise-dead and \(W_c(u,v)\ne0\), then
\(h_{c'}(V\setminus\{u,v\})=0\) for both \(c'\ne c\).*

*Proof.*  Suppose \(W_c(u,v)\ne0\) and \(h_{c'}(V\setminus\{u,v\})\ne0\)
for some \(c'\ne c\).  Take \(S_c=\{u,v\}\), \(S_{c'}=V\setminus\{u,v\}\),
and the third part empty.  All three parts are even; since \(n\ge4\),
neither \(\{u,v\}\) nor \(V\setminus\{u,v\}\) is \(V\), so the split is
proper.  Its product is
\(W_c(u,v)\cdot h_{c'}(V\setminus\{u,v\})\cdot 1\ne0\) by Fact 1 — a
live split, contradiction. \(\square\)

So TW2 is a **consequence**, not an extra hypothesis.  It is however
strictly weaker than termwise-deadness (it only forbids the splits of
shape \((0,2,n-2)\)), and every claim below is proved from **anchored +
TW2**.  That matters for the audit: the checker can then exercise
(A2)–(A5) on hundreds of packets that are *not* dead, instead of only on
the \(K_4\) one-factorisation.

Write \(C_c=\{\,uv:h_c(V\setminus\{u,v\})\ne0\,\}\) for the
**co-support** of colour \(c\) and

\[
 E_c=\{\,uv:W_c(u,v)\ne0\ \text{and}\ h_c(V\setminus\{u,v\})\ne0\,\}
   =\operatorname{supp}(W_c)\cap C_c
 \tag{2}
\]

for its **essential** edges.  TW2 says exactly:
\(\operatorname{supp}(W_c)\cap C_{c'}=\varnothing\) for \(c\ne c'\).

### 2.2 (A2): essential edges are monochromatic, essential graphs disjoint

**(A2).**  *Assume anchored + TW2.  If \(uv\in E_c\) then
\(W_{c'}(u,v)=0\) for both \(c'\ne c\).  Consequently \(E_0,E_1,E_2\) are
pairwise disjoint.*

*Proof.*  Let \(uv\in E_c\), so \(h_c(V\setminus\{u,v\})\ne0\), i.e.
\(uv\in C_c\).  If \(W_{c'}(u,v)\ne0\) for some \(c'\ne c\), then
\(uv\in\operatorname{supp}(W_{c'})\cap C_c\), which TW2 forbids.  For
disjointness: \(uv\in E_c\cap E_{c'}\) with \(c\ne c'\) would in
particular give \(W_{c'}(u,v)\ne0\). \(\square\)

### 2.3 (A3): every vertex meets every essential graph

**(A3).**  *Assume anchored + TW2.  For every vertex \(u\) and every
colour \(c\) there is a \(v\) with \(uv\in E_c\).*

*Proof.*  Apply (1) with \(S=V\) and pivot \(u\).  The left side
\(h_c(V)\) is nonzero, so at least one summand is nonzero: there is a
\(v\) with \(W_c(u,v)\ne0\) **and** \(h_c(V\setminus\{u,v\})\ne0\), which
is \(uv\in E_c\). \(\square\)

(Anchoredness is used here and only here; TW2 is not needed for (A3).)

### 2.4 (A4): every star has rank exactly 3

For a vertex \(u\), the **star** at \(u\) is the family of vectors

\[
 r_v=\bigl(W_0(u,v),\,W_1(u,v),\,W_2(u,v)\bigr)\in K^3,
 \qquad v\ne u,
 \tag{3}
\]

i.e. the rows of the \(u\)-th row of the pencil
\(L=x_0W_0+x_1W_1+x_2W_2\) read as coefficient vectors.  Its **rank** is
the dimension of their span.

**(A4).**  *Assume anchored + TW2.  Then every star has rank exactly
3.*

*Proof.*  By (A3) pick, for each \(c\), a vertex \(v_c\) with
\(uv_c\in E_c\).  By (A2), \(W_{c'}(u,v_c)=0\) for \(c'\ne c\), so

\[
 r_{v_c}=W_c(u,v_c)\,e_c,\qquad W_c(u,v_c)\ne0,
\]

a nonzero multiple of the \(c\)-th standard basis vector.  The three
\(v_c\) are distinct: \(v_c=v_{c'}\) with \(c\ne c'\) would put the edge
\(uv_c\) in \(E_c\cap E_{c'}\), which (A2) forbids.  Hence the star
contains nonzero multiples of \(e_0,e_1,e_2\) and has rank \(3\); it
cannot exceed \(3\).  \(\square\)

Two corollaries worth recording.  First, every vertex has at least three
distinct neighbours in \(\bigcup_c\operatorname{supp}(W_c)\), so that
union graph has **minimum degree \(\ge3\)** — in particular \(n\ge4\),
i.e. \(k\ge2\).  Second, the three edges \(uv_0,uv_1,uv_2\) are
monochromatic and of distinct colours, which is the germ of the cubic
graph of Theorem C.

### 2.5 (A5): two-coloured edges are triply inessential

**(A5).**  *Assume anchored + TW2.  If the edge \(uv\) carries at least
two colours, then \(h_c(V\setminus\{u,v\})=0\) for **all three** \(c\).*

*Proof.*  Say \(W_a(u,v)\ne0\) and \(W_b(u,v)\ne0\) with \(a\ne b\).  Fix
any \(c\).  If \(c\ne a\), TW2 applied to the colour-\(a\) cell gives
\(h_c(V\setminus\{u,v\})=0\).  If \(c=a\), then \(c\ne b\), and TW2
applied to the colour-\(b\) cell gives the same. \(\square\)

Equivalently: \(uv\in E_c\) for no \(c\) at all.  Combined with (A2)
this is a clean dichotomy — **every edge is either monochromatic, or
essential for nobody.**

### 2.6 Consequence: the rank-2 pencil geometry is vacuous here

The session-scratch Fermat/pencil analysis is driven entirely by
**rank-2 stars**.  When the star at \(u\) has rank \(2\) its span is a
plane in \(K^3\), whose annihilator is a single point
\(p_u\in\mathbb P^2\) — the **pencil point** of \(u\).  On that footing
the scratch proves that \(p_u\) lies on the Fermat curve
\(x_0^k+x_1^k+x_2^k=0\), that an edge whose two endpoints share a pencil
point carries the tangent line to the curve at that point, and the
attendant collinearity relations.

**(A4) says a termwise-dead configuration has no rank-2 star at all.**
Every one of those statements is therefore vacuous on termwise-dead
configurations: there are no pencil points, hence no Fermat membership
to exploit, no shared-point edges, no tangent lemma, no collinearity.
This is a *mutual exclusivity*, and it cuts both ways — it says the
rank-2 route cannot reach DIAG-\(\infty\), and it says the rank-2
objects that do exist are certainly not termwise-dead.

The second half is the sharper one, and the checker makes it concrete.
The scratch's counterexample family — the alternating \(2k\)-cycle over
\(\mathbb Q(\zeta_{2k})\) with odd edges \(x_0\) and \(i\)-th even edge
\(x_1-\zeta_ix_2\), the \(\zeta_i\) being the \(k\) roots of
\(t^k=-1\) — realizes
\(\operatorname{haf}(L)=x_0^k+x_1^k+x_2^k\) at every \(k\ge2\), and is
the reason the *summed* pencil equation obstructs nothing.  Section R of
the checker rebuilds it over the integer ring
\(\mathbb Z[s]/\Phi_{2k}(s)\) and finds, for \(k=2,\dots,6\):

| \(k\) | anchors | star ranks | TW2 violations |
|---|---|---|---|
| 2 | all nonzero | \(\{2\}\) | 4 |
| 3 | all nonzero | \(\{2\}\) | 6 |
| 4 | all nonzero | \(\{2\}\) | 8 |
| 5 | all nonzero | \(\{2\}\) | 10 |
| 6 | all nonzero | \(\{2\}\) | 12 |

Every star has rank exactly \(2\), so by (A4) **not one member of the
family is termwise-dead** — and independently, each already violates
TW2, so it fails at shape \((0,2,n-2)\) as well.  The checker exhibits
the live split that the TW2 violation's own proof names, and it
verifies the mechanism of the construction from the packet's own weights:
\(\prod_{i}(x_1-\zeta_ix_2)=x_1^k+x_2^k\), together with the fact that
the support \(2k\)-cycle has exactly two perfect matchings.

*Why an integer ring and not a field.*  The only field operation the
argument needs is a zero test, because the rank is computed from
\(2\times2\) and \(3\times3\) **minors**, never by elimination.
\(\Phi_{2k}\) is irreducible over \(\mathbb Q\), so
\(\mathbb Z[s]/\Phi_{2k}(s)\) is an integral domain embedded in
\(\mathbb Q(\zeta_{2k})\subset\mathbb C\), and a minor vanishes there
exactly when it vanishes in \(\mathbb C\).  The minor-based rank routine
is cross-validated against an independent Gaussian elimination over
\(\mathbb Q\) on 7 designed cases and 400 deterministic integer cases,
with all four ranks \(0,1,2,3\) occurring.

### 2.7 What the machine checked

| family | instances | outcome |
|---|---|---|
| \(K_4\) one-factorisation (\(k=2\)) | 1 | termwise-**dead**, TW2-clean, \(\lvert E_c\rvert=(2,2,2)\), all stars rank 3, union has exactly 3 perfect matchings, \(\operatorname{haf}(L)=x_0^2+x_1^2+x_2^2\) |
| \(D(n)\), \(n=6,8,10,12\) | 4 | anchored, TW2-clean, all stars rank 3, **not** dead; \(\#\text{live}=\#\mathrm{PM}(\text{union})-3\) exactly, at \(4,5,7,10\) matchings |
| **exhaustive** \(0/1\) packets at \(n=4\) | \(2^{18}=262144\) | 50653 anchored, 6 also TW2-clean, **exactly 6** termwise-dead — and all 6 are ordered triples of distinct one-factors of \(K_4\) |
| deterministic **signed** packets at \(n=6,8\) | 600 | 598 anchored, **75** also TW2-clean; (A2)–(A5) verified on all 75, star-rank profile \(\{3\}\) throughout |

The signed family is the reason (A1) is worth separating from
termwise-deadness: it supplies 75 non-vacuous instances of the
hypotheses at \(n=6,8\), where no termwise-dead packet exists at all.

**Negative probes.**  Each pins one direction of a definition that would
otherwise be checked in one direction only.

* **P1** — paint a second colour onto an essential edge of \(K_4\).
  (A2)'s conclusion must now fail, the TW2 scan must fire, and the
  packet must lose termwise-deadness.  All three are required.
* **P2** — a designed anchored packet at \(n=4\) whose star at vertex 0
  has rank exactly 2.  The rank routine must report 2 (not 3), and the
  packet must not be termwise-dead.
* **P3** — delete colour 2 from vertex 0's star.  The anchor \(h_2(V)\)
  must vanish — which is precisely the Laplace mechanism of (A3) — and
  colour 2 must lose all its essential edges.

**What the (A2) and (A5) checks are, and are not.**  Both are evaluated
only on packets that the same hafnian tables have already certified
TW2-clean, and both are logical consequences of that gate: (A2) is
literally the TW2 condition read at an essential edge, and (A5) is TW2
applied twice.  So on the instance families they cannot fail — they are
**mutation tripwires**, not falsifiable instance checks, and their value
is that a corrupted essential-edge set or a corrupted TW2 scan makes
them fire (injections M1, M2, M4 of §8).  The falsifiable Theorem A
content on the 75 signed instances is **(A3) and (A4)**: the existence
of an essential edge of every colour at every vertex, and rank exactly
3, are read off data the gate does not determine.  The negative probes
P1–P3 supply the failing side that the gate excludes.

One further inertness is disclosed rather than removed: in the \(n=6\)
Theorem C censuses the aggregate `require(live == packets)` cannot be
false, because the per-packet `require` inside the loop has already
raised on any packet without a live split.  It is kept as a second
tripwire — it is what catches an injection that disables the inner
check — and not counted as independent evidence.

---

## 3. Theorem B, self-contained

> **Theorem B.**  Let \(G\) be a cubic graph carrying a proper
> 3-edge-colouring with colour classes \(M_0,M_1,M_2\).  If
> \(M_0,M_1,M_2\) are the **only** perfect matchings of \(G\), then
> \(G=K_4\).

Equivalently: \(K_4\) is the unique cubic graph with exactly three
perfect matchings all of which are colour classes of a proper
3-edge-colouring.  (The three colour classes of a proper 3-edge-colouring
of a cubic graph are automatically perfect matchings, so "exactly three"
is the whole content.)  Nothing in the proof refers to hafnians; it is
ordinary graph theory, and is used in §4 as a black box.

### 3.1 (B0) Every union of two colour classes is a Hamiltonian cycle

\(M_i\cup M_j\) (\(i\ne j\)) is a disjoint union of even cycles covering
\(V\), because every vertex has degree exactly 2 in it and the two
matchings are disjoint.  Suppose it has \(\ge2\) components and let
\(C\) be one of them.  Then

\[
 M=(M_i\setminus E(C))\cup(M_j\cap E(C))
\]

is a perfect matching: on \(C\) it uses \(M_j\), off \(C\) it uses
\(M_i\).  It differs from \(M_i\) (on \(C\)) and from \(M_j\) (off
\(C\), which is non-empty since \(C\) is a proper subgraph), and it is
contained in \(M_i\cup M_j\), which is disjoint from \(M_l\) for the
third colour \(l\); so \(M\ne M_l\).  That is a fourth perfect matching.
Hence each \(M_i\cup M_j\) is a **single Hamiltonian cycle**.

### 3.2 The subset characterisation

Label \(V=\{0,1,\dots,2k-1\}\) along the Hamiltonian cycle
\(C=M_0\cup M_1\), so that \(M_0\) is the set of even edges
\(\{0\,1\},\{2\,3\},\dots\) and \(M_1\) the odd edges.  \(M_2\) is
disjoint from both, so it is a perfect matching of **chords** of \(C\).

> **Characterisation.**  The perfect matchings of \(G=C\cup M_2\) are in
> bijection with the subsets \(A\subseteq M_2\) such that every arc of
> \(C\) left by deleting \(V(A)\) has an **even** number of vertices —
> except that \(A=\varnothing\) contributes **two** matchings, namely
> \(M_0\) and \(M_1\).

*Proof.*  A perfect matching \(P\) of \(G\) uses a subset
\(A=P\cap M_2\) of chords; the rest of \(P\) perfectly matches
\(V\setminus V(A)\) using only cycle edges, i.e. matches each arc
internally, which is possible iff the arc has an even number of vertices
and then in exactly one way.  For \(A=\varnothing\) the whole cycle must
be matched by cycle edges, and a \(2k\)-cycle has exactly the two
alternating matchings.  \(\square\)

Note \(A=\varnothing\) and \(A=M_2\) are always admissible, so
\(\#\mathrm{PM}(G)\ge3\) always, with equality **iff no proper non-empty
\(A\subseteq M_2\) is admissible.**  That is the hypothesis to
contradict.

*Verified*: the subset count is compared against a direct hafnian
perfect-matching count on **every** chord matching of \(C_{2k}\) for
\(k=2,3,4,5\) — \(1,4,31,293\) of them — and the two agree everywhere.
At \(k\ge3\) the counts genuinely vary (\(\{4,6\}\), \(\{5,6,7,9\}\),
\(\{6,\dots,13\}\)), so the comparison is discriminating.

### 3.3 (B1) Singleton chords: a parity obstruction

Let \(A=\{\gamma\}\), \(\gamma=\{a,b\}\) with \(a<b\).  Deleting \(a,b\)
leaves two arcs, with \(b-a-1\) and \(2k-(b-a)-1\) vertices.  Both are
even iff \(b-a\) is odd, i.e. iff \(a\) and \(b\) have **opposite**
parity.

Since \(k\ge2\) means \(\lvert M_2\rvert=k\ge2\), a singleton is a
proper subset, so:

> **(B1).**  Exactly-three forces **every chord of \(M_2\) to join two
> vertices of equal parity.**  Since \(M_2\) is a perfect matching, the
> \(k\) even vertices are then matched among themselves, so **\(k\) is
> even.**  In particular no configuration exists for odd \(k\ge3\).

*Verified*: on every chord of every chord matching at \(k=3,4,5,6\),
"joins opposite parities" and "is a live singleton" agree — with both
outcomes occurring (\(6/6\), \(48/76\), \(635/830\), \(8892/11064\)
live/dead) — and every chord matching containing an opposite-parity
chord is confirmed to have \(>3\) perfect matchings (\(4,22,293,3101\)
of them at \(k=3,4,5,6\)).

### 3.4 (B2) Balanced crossing

Split the chords into \(P_e\) (both endpoints even) and \(P_o\) (both
odd); by (B1) there are no others.

> **Alternation.**  A set \(R\subseteq V\) leaves all arcs of \(C\) even
> iff, read cyclically, the elements of \(R\) **alternate in parity**.

Indeed the gap between cyclically consecutive removed vertices \(a,b\)
has \(b-a-1\bmod 2k\) vertices, even iff \(a,b\) have opposite parity.

Applying this to \(R=V(A)\): the removed vertices alternate parity
around the cycle, so \(\lvert R\cap\text{even}\rvert=\lvert
R\cap\text{odd}\rvert\).  Each chord contributes two vertices of one
parity, whence

> **(B2a) Balance.**  Every admissible \(A\) has
> \(\lvert A\cap P_e\rvert=\lvert A\cap P_o\rvert\).

The smallest non-empty balanced set is a **mixed pair**
\(A=\{\alpha,\beta\}\) with \(\alpha\in P_e\), \(\beta\in P_o\).  Its
four removed vertices alternate parity around the cycle exactly when
\(\alpha\) and \(\beta\) interleave, i.e.

> **(B2b) Crossing.**  A mixed pair is admissible **iff the two chords
> cross.**

If \(k\ge3\) then \(\lvert M_2\rvert=k\ge3>2\), so a mixed pair is a
**proper** subset and hence forbidden.  Therefore:

> **(B2).**  For \(k\ge3\), exactly-three forces **every even chord to
> be non-crossing with every odd chord.**

*Verified*: at \(k=3,4,5,6\), "crosses" and "is a live pair" agree on
every mixed pair, with both outcomes occurring (\(20\) live and \(16\)
dead at \(k=4\); \(945\) live and \(1080\) dead at \(k=6\); odd \(k\)
has no same-parity matchings at all, hence no mixed pairs).  Every live
mixed pair at \(k\ge3\) is confirmed to be a proper subset.

### 3.5 (B3) The minimal arc

Now assume \(k\) even, \(k\ge4\), with \(M_2=P_e\sqcup P_o\),
\(\lvert P_e\rvert=\lvert P_o\rvert=k/2\), and every even chord
non-crossing with every odd chord.  For a chord \(\gamma\) and one of
its two sides, let the *inner count* be the number of vertices strictly
inside that side.  Let \(s\) be the **minimum** inner count over all
(chord, side) pairs, realised by \((\gamma,I)\).

Say \(\gamma\in P_e\) (the case \(\gamma\in P_o\) is symmetric).  Rotating
the labelling by an even amount and, if necessary, reversing the
orientation — both preserve the parity classes and the whole
configuration — we may take \(I\) to be the *increasing* arc between
\(\gamma\)'s endpoints, and write \(\gamma=\{2p,2q\}\) with \(p<q\) so that
\(I=\{2p+1,\dots,2q-1\}\).  Then \(I\) contains \(m=q-p\) odd vertices and
\(m-1\) even ones, so \(s=2m-1\).  Nothing below depends on which of
\(\gamma\)'s two sides was named \(I\); only its minimality is used.

Each odd vertex of \(I\) is matched by \(P_o\) to another odd vertex,
and that partner must **also lie in \(I\)** — otherwise the odd chord
would cross \(\gamma\).  So \(P_o\) restricts to a perfect matching of
the \(m\) odd vertices of \(I\), forcing \(m\) **even**; and \(m\ge1\)
since \(p<q\), so \(m\ge2\).  In particular \(I\) contains at least one
odd chord \(\delta\) entirely.

Both endpoints of \(\delta\) lie in the arc \(I\), so one of \(\delta\)'s
two sides is contained in \(I\) minus \(\delta\)'s two endpoints, and
has inner count \(\le s-2<s\).  That contradicts the minimality of
\(s\).

> **(B3).**  No configuration exists for even \(k\ge4\).

Combining: odd \(k\ge3\) dies at (B1); even \(k\ge4\) dies at (B3);
\(k=2\) survives, and there \(C_4\) plus its unique chord matching is
\(K_4\), with exactly three perfect matchings.  \(\blacksquare\)

### 3.6 The machine audit of Theorem B

**A reformulation used by the search.**  Index the even vertices
\(0,\dots,k-1\) (vertex \(2p\) has index \(p\)) and the odd vertices
likewise.  An even chord \(\{2p,2q\}\), \(p<q\), contains the odd vertex
\(2i+1\) on the side \(\{2p+1,\dots,2q-1\}\) exactly when \(p\le i<q\).
Define the **signature** of odd index \(i\) as the set of even chords
whose interval \([p,q-1]\) contains \(i\).  Which of a chord's two sides
is called "inside" is immaterial: swapping them complements that chord's
bit in every signature at once, which permutes the signature classes
without changing their sizes.  Two odd vertices are non-crossing with
every even chord precisely when they have the **same signature**.
Hence:

> a compatible non-crossing odd matching exists **iff every signature
> class has even size.**

This is what (B3) denies.  The reformulation turns an
exponential-per-instance search into an \(O(k^2)\) test, and it is
**validated against the direct search** over all odd matchings on 88
even-arc systems at \(k=2,4,6\) — deliberately including non-matching
arc systems so that both answers occur (14 yes, 74 no).

| audit | range | result |
|---|---|---|
| subset-A count vs. direct hafnian count | \(k=2,3,4,5\) (\(1,4,31,293\) chord matchings) | identical everywhere |
| (B1), (B2) both directions | \(k=3,4,5,6\) | agree on every chord and every mixed pair |
| **exhaustive** over Hamiltonian-cycle cubic graphs | \(k=2\dots6\) (\(1,4,31,293,3326\) graphs) | exactly-three occurs **only** at \(k=2\); minima \(3,4,5,6,6\) |
| staged (B1)+(B2) prune | \(k=7\dots10\) | (B1) survivors \(0,11025,0,893025\); **(B1)+(B2) survivors \(0\)** at each |
| **(B3) minimal-arc search** | \(k=2,4,6,8,10,12,14\) | \(1,3,15,105,945,10395,135135\) even-chord matchings scanned; **0** admit a non-crossing partner |
| **exhaustive over ALL disjoint PM triples** (no Hamiltonicity assumed) | \(n=4,6,8\) (\(2,32,1884\) triples) | exactly-three only at \(n=4\), and those triples are pairwise Hamiltonian — an independent confirmation of (B0) |

**The packet dictionary.**  For a \(0/1\) packet whose colour supports
are three disjoint perfect matchings \(M_c\), \(h_c(S)\ne0\) iff \(S\) is
a union of \(M_c\)-edges, and then \(h_c(S)=1\).  So live splits biject
with perfect matchings of the union that are not colour classes:

\[
 \#\{\text{live splits}\}=\#\mathrm{PM}(M_0\cup M_1\cup M_2)-3,
 \qquad
 \text{termwise-dead}\iff\#\mathrm{PM}=3.
 \tag{4}
\]

Verified on **all** disjoint triples at \(n=4\) and \(n=6\), with the
dead ones exactly the two at \(n=4\), and on \(D(n)\) for
\(n=6,8,10,12\).  Identity (4) is what turns Theorem B into a statement
about packets.

---

## 4. Theorem C

### 4.1 Matching-faithfulness

Write \(G_c=\operatorname{supp}(W_c)\).

> **Definition.**  \(W_c\) is **matching-faithful** when, for every even
> \(S\subseteq V\), the existence of a perfect matching of \(G_c[S]\)
> implies \(h_c(S)\ne0\).

The converse implication is free: \(h_c(S)\ne0\) forces a nonzero
matching term, hence a perfect matching of \(G_c[S]\).  So faithfulness
says exactly that **no cancellation occurs**: the support decides the
vanishing.

Three sufficient conditions, all standard:

1. **Nonnegative entries.**  \(h_c(S)\) is a sum of products of
   nonnegative numbers, one per perfect matching of \(G_c[S]\); if one
   matching exists, its term is positive and no term is negative.
2. **\(0/1\) entries.**  A special case of 1.
3. **Algebraically independent (generic) entries.**  \(h_c(S)\) is a
   polynomial in the entries which is *not identically zero* whenever
   \(G_c[S]\) has a perfect matching (that matching contributes a
   monomial no other matching can cancel), so it does not vanish at an
   algebraically independent point.

The checker pins the definition **both ways**: a designed nonnegative
matrix is confirmed faithful on 6 matched even sets (a positive control
that is required to be non-vacuous), and a designed signed matrix — the
\(4\)-cycle with weights \(1,1,1,-1\) — is confirmed **not** faithful,
failing on the full vertex set and on that set only.

### 4.2 The theorem

> **Theorem C.**  Let \(k\ge3\), and let \(W_0,W_1,W_2\) be anchored
> with all three colours matching-faithful.  Then some split is live;
> i.e. the packet is **not** termwise-dead.

*Proof.*

**Step 1 (anchors give matchings).**  \(h_c(V)\ne0\) forces a nonzero
matching term, so \(G_c\) has a perfect matching \(M_c\).

**Step 2 (essential, monochromatic, disjoint).**  Let \(uv\in M_c\).
Then \(M_c\setminus\{uv\}\) is a perfect matching of
\(G_c[V\setminus\{u,v\}]\), so by faithfulness
\(h_c(V\setminus\{u,v\})\ne0\); i.e. \(uv\in E_c\).  If
\(W_{c'}(u,v)\ne0\) for some \(c'\ne c\), then the split
\((\{u,v\}\ \text{in colour}\ c',\ V\setminus\{u,v\}\ \text{in colour}\
c,\ \varnothing)\) is live by Fact 1 — done.  Otherwise every
\(M_c\)-edge is monochromatic, and therefore \(M_0,M_1,M_2\) are
pairwise disjoint (a shared edge would be bichromatic).

**Step 3 (cubic union, Theorem B).**  \(G:=M_0\cup M_1\cup M_2\) has
every vertex on exactly one edge of each \(M_c\), and those three edges
are distinct, so \(G\) is cubic and the \(M_c\) are the classes of a
proper 3-edge-colouring.  If \(\mathrm{PM}(G)=\{M_0,M_1,M_2\}\) then
Theorem B gives \(G=K_4\), i.e. \(k=2\), contradicting \(k\ge3\).  So
there is a fourth perfect matching \(P\) of \(G\).

**Step 4 (faithfulness makes its split live).**  Put
\(S_c=V(P\cap M_c)\).  Each \(P\cap M_c\) is a matching, so \(S_c\) is
even; every edge of \(P\) lies in exactly one \(M_c\), so the \(S_c\)
partition \(V\).  If \(S_c=V\) then \(P\cap M_c\) is a perfect matching
of \(V\) contained in \(M_c\), hence equal to \(M_c\), hence \(P=M_c\) —
excluded.  So the split is proper.  Finally \(P\cap M_c\) is a perfect
matching of \(G_c[S_c]\), so faithfulness gives \(h_c(S_c)\ne0\) for
each \(c\).  The split is live. \(\blacksquare\)

Note that the theorem is **uniform in \(k\)**: no order-by-order search,
no solver, no characteristic assumption on \(K\).

### 4.3 What the machine checked

* **Steps 1–4 on 300 deterministic nonnegative packets** at \(n=6,8\)
  (three one-factors with positive weights plus up to three extra
  positive edges per colour).  All 300 are anchored; 188 exit at Step 2
  through a bichromatic anchor edge — and for those the checker verifies
  that the split Step 2 names really is live — and 112 run the full
  chain, every one of them confirmed not termwise-dead by a full split
  census.

  **On this family faithfulness is inert, and the checker says so.**  An
  earlier draft of this note claimed 13 "load-bearing" parts here.  That
  claim was wrong and an independent audit caught it: the criterion used
  was "the part carries a colour-\(c\) edge beyond the anchor matching",
  which is *not* the criterion (S2) supplies.  Every one of those 13
  parts is perfectly matched by \(G_c\) in exactly **one** way, so
  \(h_c(S_c)\) is a single product of nonzero cells and (S2) alone
  already makes it nonzero — no faithfulness hypothesis is used.  A
  neutered faithfulness step passed on all 13.  The criterion is now
  the right one, \(\lvert\mathrm{PM}(G_c[S_c])\rvert\ge2\), and on this
  family it is met **zero** times; the count is recorded in the ledger,
  not required to be positive.
* **Exhaustive \(0/1\) census at \(n=6\)**, two versions.  For every
  ordered triple of pairwise disjoint perfect matchings (\(M_0\) fixed,
  32 triples): **131072** packets assigning each of the six remaining
  edges to one colour or to none (\(32\times4^6\)), and **16384**
  packets letting each of a **three**-edge sub-pool carry any subset of
  the three colours (\(32\times8^3\)) — the second covers the
  multi-coloured extras the first excludes, at the cost of a smaller
  pool.  Every single packet has a live Step-4 split; a subsample (32
  and 4 respectively) is additionally checked by a full census over all
  \(3^6\) colourings, so the shortcut is never trusted alone.

  **Disclosed limitation.**  At \(n=6\) every extra matching has profile
  \((2,2,2)\) (§5.1), so these two censuses are settled by (S1) alone and
  do **not** exercise faithfulness either.  Nothing exhaustive in this
  note exercises faithfulness.
* Every family above is required to be non-vacuous by an explicit count,
  and \(D(n)\) at \(n=6,8,10,12\) — a \(0/1\), hence faithful, packet —
  is separately required *not* to be termwise-dead.

### 4.4 Where faithfulness is actually load-bearing

The right criterion is (S2)'s: faithfulness does work on the part
\(S_c\) exactly when \(G_c[S_c]\) has **two or more** perfect matchings,
so that \(h_c(S_c)\) is a sum with something to cancel against.  Two
measured facts explain why the families above never meet it.

| \(n\) | induced parts of size \(\ge4\) | of those, admitting a second perfect matching whose edges all avoid the anchor union |
|---|---|---|
| 6 | **0** | 0 |
| 8 | 8208 | **4608** |

At \(n=6\) there is no part of size \(\ge4\) at all, so cancellation is
*structurally* impossible.  At \(n=8\) it is perfectly possible — over
half the size-\(\ge4\) parts admit a second matching realisable by edges
outside the anchor union, which is the constraint that matters (an edge
*inside* the union belongs to another colour, so adding it would make an
anchor edge bichromatic and Step 2 would have fired already).  What the
deterministic positive-weight family never does is *realise* one: it
would have to place its two extra edges exactly on an alternative
pairing of one induced part, which random draws essentially never hit.

So the instances are built by hand.  Each names an anchor triple, a
colour, an induced part, and two extra edges outside the union which
give \(G_c[S_c]\) a second perfect matching.  Each is then run **twice**:
once with positive weights (matching-faithful) and once as its
**cancelling twin** — the same support with a single weight negated.

| instance | \(\lvert\mathrm{PM}(G_c[S_c])\rvert\) | positive \(h_c(S_c)\) | twin \(h_c(S_c)\) |
|---|---|---|---|
| \(n=8\) block triple, colour 0, part \(\{0,1,2,3\}\), extras \(\{0,3\},\{1,2\}\) | 2 | 2 | **0** |
| \(D(10)\), colour 1, part \(\{0,1,2,4,7,9\}\), extras \(\{0,7\},\{2,4\}\) | 2 | 2 | **0** |
| \(D(12)\), colour 0, part \(\{3,4,7,8\}\), extras \(\{3,7\},\{4,8\}\) | 2 | 2 | **0** |

The Step-4 faithfulness test is written as a **verdict-returning
function**, not a bare assertion, and the checker requires it to answer
`True` on the positive packet and `False` on the twin.  That is what
makes it falsifiable: neutering the test into a constant `True` passes
the positive half silently and is caught by the negative half —
injection M21 of §8, which now raises.  The twin is additionally
required to be a genuine, non-degenerate failure of
matching-faithfulness (it cancels on the named part, and on strictly
fewer than all of its matched sets).

Cancellation on a matched part is therefore **not** a hypothetical: it
happens, at every order from \(n=8\) up, on the same supports the proof
walks through.  Faithfulness is exactly the hypothesis that rules it
out, and §5 is exactly the question of whether it can be arranged
everywhere at once.

### 4.5 Complementarity with the SAT theorem

| | cancellation | orders reached |
|---|---|---|
| [`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md) | **arbitrary** | \(n\in\{6,8,10\}\), i.e. \(k\le5\) |
| **Theorem C** | **none** (matching-faithful) | **every** \(k\ge3\) |

Neither statement implies the other.  Together they leave exactly one
gap: **\(k\ge6\) with cancellation**.  That gap is the stall.

---

## 5. The stall, stated exactly

Fix \(k\ge3\) and suppose, for contradiction, that a termwise-dead
packet exists.  By (A3) each colour has an anchor perfect matching
\(M_c\subseteq E_c\); by (A2) these are monochromatic and pairwise
disjoint; by Theorem B their union \(G\) has a fourth perfect matching
\(P\).  Step 4 of Theorem C then produces a proper split
\(S_c=V(P\cap M_c)\) which \(G_c\) perfectly matches — so the *only*
escape is cancellation:

> **The stall (open).**  Can \(h_c(S_c)=0\) be arranged, for **some**
> colour \(c\), on a set \(S_c\) that \(G_c[S_c]\) does perfectly
> match — simultaneously for **every** fourth perfect matching \(P\) of
> \(G\) and **every** admissible choice of anchor matchings
> \(M_0,M_1,M_2\)?

Two narrowings are proved.

**(S1) A cancelling part has \(\lvert S_c\rvert\ge4\).**  If
\(S_c=\varnothing\) then \(h_c(S_c)=1\).  If \(S_c=\{u,v\}\) then
\(uv\in P\cap M_c\subseteq G_c\), so \(h_c(S_c)=W_c(u,v)\ne0\) by
Fact 1.  Neither can cancel.

**(S2) The cancelling colour needs a non-anchor edge inside \(S_c\).**
If \(G_c[S_c]\) has only the one perfect matching \(P\cap M_c\), then
\(h_c(S_c)\) is that single product of nonzero cells, hence nonzero.  So
cancellation requires \(G_c[S_c]\) to carry at least two perfect
matchings, hence an edge of \(G_c\) inside \(S_c\) outside \(M_c\).

Both are verified as computations: (S1) on 288 two-element parts of the
\(n=6\) dictionary family, (S2) on the 14 extra-matching splits of
\(D(6),D(8),D(10),D(12)\), where the anchor-only packets are confirmed
to have every such split live.  How far (S2) reaches is measured
separately in §4.4: no part at \(n=6\) can cancel at all, while 4608 of
the 8208 size-\(\ge4\) parts at \(n=8\) could in principle, and §4.4's
three hand-built instances show cancellation actually occurring.

### 5.1 The \((2,2,2)\)-profile measurement

Call the **profile** of an extra matching \(P\) the multiset
\((\lvert S_0\rvert,\lvert S_1\rvert,\lvert S_2\rvert)\), and call \(P\)
**unkillable** when every part has size \(\le2\): by (S1) no colour can
then cancel, so the split is live **with no faithfulness hypothesis at
all.**

Exhaustively, over every anchor cubic graph (= every ordered triple of
pairwise disjoint perfect matchings, \(M_0\) fixed):

| \(k\) | anchor cubic graphs | extra matchings | unkillable | graphs all of whose extras are unkillable | profiles |
|---|---|---|---|---|---|
| 3 | 32 | 48 | **48** | **32 (all)** | \((2,2,2)\times48\) |
| 4 | 1884 | 5832 | **0** | 0 | \((0,4,4)\times2376\), \((2,2,4)\times3456\) |

So at \(k=3\) **every** anchor cubic graph has *only* unkillable extra
matchings, and the termwise condition falls at \(k=3\) with the
cancellation hypothesis removed entirely — a route independent of the
SAT theorem, though it reproves a result the SAT theorem already has.

**Why this does not reprove \(k=4,5\).**  At \(k=4\), not one of the
5832 extra matchings is unkillable: every profile carries a part of size
\(\ge4\), so (S1) blocks nothing and cancellation is conceivable at
every single split.  \(k=5\) is worse, since \(n=10\) admits still more
part sizes.  The \(k=3\) argument is therefore a genuinely
order-specific accident, and the SAT theorem remains the only thing
covering \(k=4,5\) with cancellation.  For the record, the round-robin
family shows the same picture:

| | \(\#\mathrm{PM}\) | extra matchings | profiles |
|---|---|---|---|
| \(D(6)\) | 4 | 1 | \((2,2,2)\) |
| \(D(8)\) | 5 | 2 | \((2,2,4)\times2\) |
| \(D(10)\) | 7 | 4 | \((2,2,6)\times3,\ (2,4,4)\) |
| \(D(12)\) | 10 | 7 | \((2,2,8)\times4,\ (4,4,4)\times3\) |

### 5.2 What would close it

By (S2) the cancelling colour must carry an edge inside \(S_c\) beyond
its anchor matching.  But by (A2)/(A5) such an edge is either
monochromatic, or essential for nobody; and by (A1) any monochromatic
cell \(W_c(u,v)\ne0\) kills \(h_{c'}(V\setminus\{u,v\})\) for both other
colours.  A quantitative version of that tension — enough non-anchor
edges to cancel with, few enough to keep all the co-supports empty —
is what an induction would need.  This note does not supply it.

---

## 6. The \(k=2\) boundary

\(K_4\) with its three one-factors **is** termwise-dead, so no theorem
here may exclude it.  It does not get excluded, and the escape is
localised.

* **Theorem A holds at \(k=2\).**  \(K_4\) is anchored and TW2-clean,
  \(\lvert E_c\rvert=2\) for each colour, and every star has rank
  exactly 3 — each vertex of \(K_4\) has three neighbours, one per
  colour, contributing \(e_0,e_1,e_2\).  Verified.
* **Theorem C is stated for \(k\ge3\)** and says nothing at \(k=2\).
  Indeed \(K_4\)'s packet is \(0/1\), hence matching-faithful, and it
  *is* dead: the hypothesis \(k\ge3\) is not decoration.
* **Inside Theorem B, \(k\ge3\) enters at exactly two places.**
  * **(B1)** rules out odd \(k\ge3\).  It does not touch \(k=2\), which
    is even; and \(C_4\)'s unique chord matching \(\{\{0,2\},\{1,3\}\}\)
    is indeed same-parity.  Verified.
  * **(B2)** needs \(\lvert M_2\rvert=k\ge3\) for a mixed pair to be a
    **proper** subset.  At \(k=2\) the unique mixed crossing pair **is
    all of \(M_2\)**, so it yields \(M_2\) itself rather than a fourth
    matching.  That is precisely how \(K_4\) escapes.  Verified, along
    with 965 proper crossing mixed pairs at \(k=3,\dots,6\) to show the
    \(k\ge3\) entry point is non-vacuous.
  * **(B3)** is stated for even \(k\ge4\) and its hypothesis (every even
    chord non-crossing with every odd chord) is *false* at \(k=2\),
    where the two chords cross — consistent, since (B2) does not force
    non-crossing there.

---

## 7. Scope

1. Everything here concerns **diagonal** packets: symmetric
   zero-diagonal scalar edge matrices \(W_0,W_1,W_2\).  That is the
   shadow an exact ternary source induces through Theorem B of
   [`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md),
   not an exact source itself.
2. Theorem C assumes **matching-faithfulness**.  It says nothing about
   packets with cancellation, and at \(k\ge6\) nothing else does either.
3. The \(k=3\) cancellation-free argument of §5.1 is an
   order-specific accident, measured to fail already at \(k=4\).  It
   reproves nothing the committed SAT theorem does not already have.
4. The rank-2 vacuity of §2.6 is a statement **about termwise-dead
   configurations only**.  The rank-2 pencil geometry is perfectly
   non-vacuous elsewhere — the \(2k\)-cycle family is entirely rank-2 —
   and the two simply never meet.
5. The pencil counterexamples themselves come from **session scratch**
   and from the committed census note; this note's checker rebuilds them
   and verifies the properties it uses (roots of \(t^k=-1\), the product
   identity, two perfect matchings of the support, nonzero anchors, all
   stars rank 2), but the full polynomial hafnian
   \(\operatorname{haf}(L)=x_0^k+x_1^k+x_2^k\) is verified in that
   companion, not here.
6. No claim in this note *depends* on the census note: the \(n=4\)
   census count, the Hamiltonicity of the \(D(n)\) unions and the pencil
   family are all recomputed here by independent code, so agreement
   between the two artifacts is corroboration.
7. Theorem B is ordinary graph theory and is likely known; the proof is
   given in full because the audit needs it stated, not because
   priority is claimed.
8. This note has been through one independent audit, which returned
   **FAIL** on packaging while confirming every hand proof.  Two
   substantive defects were fixed: the "load-bearing" criterion of §4.3
   was wrong and made faithfulness untested (now §4.4, with three
   instances and their cancelling twins), and the rank routine's
   \(3\times3\) determinant had an undetectable sign (now closed by the
   cofactor-position controls).  A further audit is still wanted; per
   project discipline this is a research reduction until independently
   audited.  **Krenn's conjecture remains open.**

---

## 8. Verification

~~~text
python3       computations/verify_termwise_rank3_cubic_uniqueness.py
python3 -O    computations/verify_termwise_rank3_cubic_uniqueness.py
python3 -I    computations/verify_termwise_rank3_cubic_uniqueness.py
python3 -S    computations/verify_termwise_rank3_cubic_uniqueness.py
python3 -I -S computations/verify_termwise_rank3_cubic_uniqueness.py
python3 -m py_compile computations/verify_termwise_rank3_cubic_uniqueness.py
~~~

Runtime is **about four and a half seconds**, of which the exhaustive
\(2^{18}\) census at \(n=4\), the \(k=14\) minimal-arc scan, the
147456-packet \(n=6\) census and the (S2)-reach sweep over all 1884
anchor triples at \(n=8\) are the largest items.  Exact stdlib arithmetic
only — `int`, `Fraction`, and an integer cyclotomic ring
\(\mathbb Z[s]/\Phi_m(s)\) built in the checker.  No floats, no `numpy`,
no `random`, no SAT solver, no third-party import at all, so all five
interpreter modes run every section and produce the **same digest**.
There are no bare `assert`s: every check goes through `require`, which
raises a `RuntimeError` and therefore survives `-O`.

**Ledger.**  One frozen digest, hashing *computed* content: the rank
cross-validation histogram; \(K_4\)'s structure record with its pencil
hafnian; \(D(n)\)'s anchors, TW2 counts, star ranks, live-split counts
and shape histograms; the \(2^{18}\) census counts and its
classification of the dead packets; the signed-packet counts and
rank profile; the three negative probes; the cyclotomic guards with
their moduli, degrees, star ranks, TW2 counts and witness splits; every
Theorem B audit table above; the faithfulness probes; the Theorem C
instance and census counts; the (S2)-reach counts; the three
load-bearing instances with their positive and cancelling hafnians; the
stall's profile histograms; and the \(k=2\) boundary record.  **Every
boolean in it is computed** — the two literal `False`s the audit found
in the negative-probe records (P1 and P2 stored their `termwise_dead`
verdict as a constant rather than the computed one) have been
replaced.

~~~text
ledger : 021aa7b60891b2268578d96191dfeedbe7d001d64ca8e73c2862c28dfb75d619
~~~

**Mutation-tested with twenty-three injections.  All twenty-three raise
under both `python3` and `python3 -O`, with the same message, naming the
broken property.**

| # | injection | message raised |
|---|---|---|
| M1 | the essential set drops its cofactor condition | A2 fails on signed packet 19: the essential edge (1,6) of colour 0 also carries colour 1, so essential edges are not monochromatic |
| M2 | (A2) is checked against the same colour instead of the others | A2 fails on K_4 one-factorisation: the essential edge (1,2) of colour 0 also carries colour 0, so essential edges are not monochromatic |
| M3 | the star-rank routine never certifies rank 3 | minor_rank returned 2 on a designed rank-3 input, so the rank routine is not pinned |
| M4 | the TW2 scan compares a colour with itself | A1 fails on K_4 one-factorisation: the packet is termwise-dead yet a pair carries colour 2 while its complement stays alive in colour 2 |
| M5 | the deleted-pair cofactor reads \(h_c(\{u,v\})\) instead of \(h_c(V\setminus\{u,v\})\) | probe P3: colour 2 still has an essential edge although its anchor vanished |
| M6 | the subset-A parity filter accepts odd arcs and rejects even nonzero ones | the subset-A characterisation disagrees with the direct hafnian perfect-matching count at k=2 on the chord matching ((0, 2), (1, 3)): 3 against 5 |
| M7 | (B1)'s parity test is inverted | B1 fails at k=3 on the chord (0, 2): joining opposite parities is True but being a live singleton is False |
| M8 | two chords count as crossing when neither endpoint is inside | B2 fails at k=4 on the mixed pair (0, 2),(1, 3): crossing is False but liveness is True |
| M9 | the (B3) signature classes are required odd, not even | the signature criterion disagrees with the direct non-crossing search at k=2 on the arc system (): False against True |
| M10 | the (B3) gap interval is extended by one endpoint | the signature criterion disagrees with the direct non-crossing search at k=2 on the arc system ((0, 1),): True against False |
| M11 | Theorem C step 4 assigns each edge of \(P\) to the colours it is **not** in | step 4 fails on nonnegative packet 0: the induced parts do not partition V |
| M12 | the non-faithfulness probe is given a cancellation-free matrix | the NEGATIVE faithfulness probe is vacuous: the designed cancelling matrix is matching-faithful after all, so the definition is pinned in one direction only |
| M13 | the frozen ledger digest is altered | termwise rank-3 cubic uniqueness ledger changed |
| M14 | the cycle counterexample's colour-2 weight loses its sign | cycle pencil k=3: prod_i (x_1 - zeta_i x_2) is not x_1^k + x_2^k, so the counterexample's mechanism is broken |
| M15 | the (S1) unkillability bound is relaxed from parts \(\le2\) to parts \(\le4\) | the k=4 measurement fails: 1884 anchor cubic graphs have an extra matching with every part <= 2, so the cancellation-free argument would extend to k=4 after all |
| M16 | the \(n=4\) census is restricted to the anchored matrices | the n=4 census examined 50653 packets, not the 2^18 = 262144 it advertises |
| M17 | the \(n=6\) census tests the step-4 split against swapped colours | the n=6 Theorem C census (one colour per extra edge) found a 0/1 packet with no live step-4 split, which would contradict Theorem C |
| M18 | the cyclotomic modulus is built from \(s^m+1\) | an exact polynomial division left a remainder |
| M19 | the packet dictionary offsets by two colour classes, not three | the packet dictionary fails at n=4: 0 live splits against 3 perfect matchings of the union |
| M20 | a split counts as live when **any** colour factor is nonzero | D(6): the packet dictionary fails -- 136 live splits against 4 perfect matchings of the union |
| M21 | the Step-4 faithfulness test is neutered into a constant TRUE | n=8 block triple, colour 0, part {0,1,2,3}: the Step-4 faithfulness test still answers TRUE on the CANCELLING TWIN, so the test is inert and faithfulness is not what excludes cancellation here |
| M22 | the third cofactor of the \(3\times3\) determinant has its sign flipped | minor_rank returned 3 on a designed rank-2 input, so the rank routine is not pinned |
| M23 | a load-bearing instance loses one of its two extra edges | D(12), colour 0, part {3,4,7,8}: G_c[S_c] has 1 perfect matching(s), so (S2) already forces h_c(S_c) != 0 and faithfulness is not load-bearing here |

Injections must be **detected defects**, not inert edits: disabling a
`require` that never fires on correct data proves nothing.  M5, M11, M14
and M17 were rewritten for that reason during the first build, and M14
and M17 in doing so exposed two real checker weaknesses (the cycle
product identity was checked against independently written weights
rather than the packet's own; the \(n=6\) census recorded its live-split
count without reference to whether one had been found).  The
independent audit then found two more, both now fixed and both now
carrying an injection of their own:

* **M21** — the Step-4 faithfulness test could be neutered into a
  constant `True` and the entire checker still passed, because no
  instance ever put it under strain.  §4.4's cancelling twins fix that.
* **M22** — the sign of the third cofactor in the \(3\times3\)
  determinant could be flipped and the entire checker still passed, with
  an unchanged digest, although \([[0,1,1],[1,0,1],[1,1,2]]\) is rank 2
  and the mutant calls it rank 3.  (A4) rests on that routine.  Three
  designed singular all-nonzero-row matrices, between them carrying a
  nonzero cofactor at each of the three positions, plus a second batch
  of 393 deterministic cases with no row zeroed, now close it.

Two further descriptions were corrected against what the injections
actually do: M6 rejects even **nonzero** arcs (a clean inversion also
raises, with different counts, and disabling the filter raises too), and
M10 **extends** the interval by one endpoint rather than shifting it — a
symmetric shift `range(p+1, q+1)` is extensionally identical, since it
merely renames which side of each chord is called inside, and correctly
does **not** raise.
