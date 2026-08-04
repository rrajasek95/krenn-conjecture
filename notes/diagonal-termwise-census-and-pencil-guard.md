# The diagonal termwise census, the pencil identity, and why the pencil form is not the target

Checker:
[`computations/verify_diagonal_termwise_census_and_pencil_guard.py`](../computations/verify_diagonal_termwise_census_and_pencil_guard.py).

This note audits, corrects and upgrades the four scratch claims that
section 6 of
[`notes/good-crossing-matching-forcing.md`](good-crossing-matching-forcing.md)
records as **unaudited** ("session scratch, not in the repository"): the
death of the shape \((0,2,N-2)\) on a Hamiltonian family, the
shape-restricted SAT result at \(N=8\), the unresolved \(N=10\)
instance, and the pencil identity with its two-colour shadow.  Three of
them survive audit and are strengthened here; the fourth needed a
correction, recorded in §7.

**Model.**  Sites carry endpoint-ordered aggregate blocks \(A_{uv}\) with
cells \(A_{uv}(i,j)\), \(i\) read at \(u\) and \(j\) at \(v\); exactness
is \(H_B(A)=\Delta_{B,3}\) over \(\mathbb C\).  Everything below lives in
the **MONOCHROMATIC-EDGE model**, i.e. \(A_{uv}\) diagonal with
\(W_c(u,v)=A_{uv}(c,c)\); equivalently these are statements about the
**diagonal shadow** of a general source, and they do **not** by
themselves constrain bicoloured sources.  In particular this is *not* an
attack on the open case: in the monochromatic-edge model \(N=8,d=3\) and
\(N=10,d=3\) are already closed by
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md).
The open case is the GENERAL / bicoloured one (DeepMind's Lean
`eqSystem8_no_solution_d3`, research open), in which the results below
enter only as a lever, through
[`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md).
See [`references/REFERENCES.md`](../references/REFERENCES.md).

All conventions are those of
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md):
\(V\) is a vertex set of even size \(n=2k\), \(W_0,W_1,W_2\) are
symmetric zero-diagonal scalar edge matrices over a field,
\(h_r(S)=\operatorname{haf}W_r[S]\) with \(h_r(\varnothing)=1\), and a
*split* is a proper ordered partition \(V=S_0\sqcup S_1\sqcup S_2\) into
even sets.  A split is **live** when \(h_0(S_0)h_1(S_1)h_2(S_2)\ne0\).
The shape-restricted SAT section imports the committed engine's own
encoder rather than re-implementing it, and requires that in the
unrestricted mode it reproduces that engine's CNF clause for clause.

**Status.**  The pencil identity, the two-colour realization, the
Hamiltonian-triple lemma and Lemma U2 are **hand proofs**, verified on
instances (and, for the identity, as a polynomial identity on nonvacuous
packets).  The shape-restricted verdicts are **machine theorems**, sound
in the same direction as the committed engine's: `UNSAT` of a relaxation
is an obstruction, `SAT` is only a support-level survivor.  The uniform
statement DIAG-\(\infty\) is **conjectured**; it is proved only at
\(k=3,4,5\), by the cited SAT theorem.  The \(n=10\) shape-restricted
instance is **unresolved**.  **Krenn's conjecture remains open.**

---

## 0. Summary of outcomes

**Proved.**

* **The pencil identity** (§1): a polynomial identity packaging every
  split product into one hafnian.
* **The two-colour realization** (§3): the alternating \(2k\)-cycle
  solves the two-colour problem, in both its summed and its termwise
  form, at **every** \(k\).
* **The Hamiltonian-triple lemma** (§4), with an explicit construction
  \(D(n)\) available at **every** even \(n\): three pairwise disjoint
  perfect matchings whose pairwise unions are single Hamiltonian cycles;
  for the \(0/1\) packet \(W_r=\operatorname{adj}(M_r)\) all three
  anchors are \(1\) and **every split with an empty part is dead**.  So
  the shape \((0,2,N-2)\) can never be *forced* live.
* **Lemma U2** (§5): under empty-part deadness, a pair lying in two
  co-supports is a non-edge of both colours; consequently the naive
  pair-deletion induction on \(n\) is never available.

**Machine theorems (SAT, sound direction).**

* \(n=8\), dropping the shape \((0,2,6)\): **UNSAT** (§6).  This is the
  result section 6 of the good-crossing note cites; it is reproduced
  here with the committed encoder.
* \(n=6\) unrestricted UNSAT (agreeing with the committed engine),
  \(n=6\) dropping \((0,2,4)\) SAT, \(n=8\) dropping both \(X\le2N\)
  shapes SAT, \(n=6,8\) keeping only the two-part clauses SAT.

**Corrected.**  The summed **pencil equation is not an obstruction at
all** (§2): it has solutions for every \(k\ge2\).  Section 6 of the
good-crossing note calls the termwise condition and the pencil equation
"exactly" the same; the implication holds in one direction only, and
this note replaces that sentence.

**Still open.**  DIAG-\(\infty\) for \(k\ge6\); the \(n=10\)
shape-restricted instance; and everything the committed cluster already
lists as open.

---

## 1. The pencil identity

**Identity (proved).**  For symmetric zero-diagonal \(W_0,W_1,W_2\) on
\(V\), \(|V|=n=2k\), and commuting indeterminates \(x_0,x_1,x_2\),

\[
 \operatorname{haf}\bigl(x_0W_0+x_1W_1+x_2W_2\bigr)[V]
 =\!\!\sum_{(S_0,S_1,S_2)}\!\!
   x_0^{|S_0|/2}x_1^{|S_1|/2}x_2^{|S_2|/2}\,
   h_0(S_0)h_1(S_1)h_2(S_2),                                    \tag{1}
\]

the sum running over **all** ordered partitions of \(V\) into three even
(possibly empty) sets.

*Proof.*  Expand the hafnian of the pencil over perfect matchings:

\[
 \operatorname{haf}\Bigl(\sum_rx_rW_r\Bigr)[V]
 =\sum_{M\in\operatorname{PM}(V)}\ \prod_{uv\in M}
   \bigl(x_0W_0(u,v)+x_1W_1(u,v)+x_2W_2(u,v)\bigr),
\]

and expand each factor.  A term of the resulting sum is a matching \(M\)
together with a **colour per edge**, i.e. a map \(c:M\to\{0,1,2\}\), and
its value is \(\prod_r x_r^{|c^{-1}(r)|}\prod_{uv\in M}W_{c(uv)}(u,v)\).
Group the terms by the triple of *vertex sets* \(S_r=V(c^{-1}(r))\).
Each \(S_r\) is even, the three are disjoint and cover \(V\), and
\(|c^{-1}(r)|=|S_r|/2\), so all terms in one group carry the same
monomial \(\prod_rx_r^{|S_r|/2}\).  Conversely, for a fixed ordered even
partition \((S_0,S_1,S_2)\) the coloured matchings with those class
vertex sets are exactly the triples \((M_0,M_1,M_2)\) of perfect
matchings of \(S_0,S_1,S_2\), and summing their weights factorizes as
\(h_0(S_0)h_1(S_1)h_2(S_2)\).  \(\square\)

Note what (1) is not: the coefficient of a fixed monomial is a **sum**
over all splits of that shape, not a single split product.  That is the
whole of §2.

*Verified*: as a polynomial identity at \(n=4,6,8\) on eight
deterministic packets (six integer, two over \(\mathbb Q\)), the two
sides computed by different routes — a polynomial hafnian recursion on
the left, per-colour scalar hafnian tables summed over the \(3^n\)
colourings on the right.  The checker counts the monomials of each side
and the nonzero split terms, requires every instance to carry at least
one **mixed** monomial (an instance whose only monomials are the three
pure ones would test nothing), and runs a **sharpness probe**: deleting
one nonzero split term from the right-hand side must make the two sides
disagree.

---

## 2. DIAG-\(\infty\): the termwise statement is the target, the pencil equation is a guard

Two conditions must be kept apart.

**\(T(k)\), termwise.**  There exist \(W_0,W_1,W_2\) on \(2k\) vertices
with

\[
 h_r(V)\ne0\ (r=0,1,2),\qquad
 h_0(S_0)h_1(S_1)h_2(S_2)=0\ \text{for every split}.        \tag{2}
\]

This is exactly the system (2) of
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md),
i.e. what a diagonal aggregate realization forces after its harmless
normalizations.

**\(P(k)\), summed.**
\(\operatorname{haf}(x_0W_0+x_1W_1+x_2W_2)=x_0^k+x_1^k+x_2^k\).

By (1), \(T(k)\Rightarrow P(k)\): if every split product vanishes and
the anchors are \(1\), then every mixed coefficient of (1) is a sum of
zeros.  **The converse is false, and badly so.**

**Guard (proved).**  \(P(k)\) has solutions for **every** \(k\ge2\).
Take the \(2k\)-cycle on \(0,1,\dots,2k-1\), let \(\zeta_0,\dots,
\zeta_{k-1}\) be the \(k\) roots of \(t^k=-1\), and put

\[
 L(2i,2i+1)=x_0,\qquad
 L(2i+1,2i+2\bmod 2k)=x_1-\zeta_ix_2 .                       \tag{3}
\]

A \(2k\)-cycle has exactly two perfect matchings, so the hafnian is the
sum of the two alternating products,

\[
 x_0^k+\prod_{i}(x_1-\zeta_ix_2)=x_0^k+x_1^k+x_2^k,
\]

the product being \(x_2^k\bigl((x_1/x_2)^k+1\bigr)\).  The three anchors
are \(1\) (for colour \(2\), \(\prod_i(-\zeta_i)=(-1)^k(-1)^k=1\)).
\(\square\)

*Verified* exactly for \(k=2,\dots,6\) in the cyclotomic field
\(\mathbb Q(\zeta_{2k})=\mathbb Q[s]/\Phi_{2k}(s)\), with
\(\Phi_{2k}\) computed by exact integer polynomial division rather than
tabulated, the roots \(\zeta_i=s^{2i+1}\) *checked* to satisfy
\(t^k=-1\) and to be distinct, and the two-perfect-matching mechanism
computed from the support graph.  The pencil equation is verified as an
**equality in \(\mathbb Q[s]/\Phi_{2k}(s)\)**, and an equality is
preserved by any ring homomorphism — in particular by
\(s\mapsto e^{i\pi/k}\) into \(\mathbb C\).  (Verifying it in
\(\mathbb Z[s]/(s^k+1)\) instead would *not* do: that quotient is not a
domain when \(s^k+1\) is reducible, and the equation is false there for
\(k=3,5,6\) — at \(k=3\) the coefficient of \(x_1^2x_2\) of
\(\prod_i(x_1-s^{2i+1}x_2)\) is \(1+s^2-s\ne0\) in
\(\mathbb Z[s]/(s^3+1)\), while it reduces to \(0\) modulo
\(\Phi_6=s^2-s+1\); the checker probes exactly this computation.)
Irreducibility of \(\Phi_{2k}\) over \(\mathbb Q\), which is classical,
is used only for the liveness counts below: a nonzero field element has
a nonzero complex image.

**These solutions are not termwise.**  Their live splits are counted:
\(2,6,14,30\) at \(k=2,3,4,5\).  They must be nonzero at \(k=3,4,5\),
since a termwise solution there would contradict the cited SAT theorem;
the checker *requires* it, so this is a consistency check between the
guard and the committed engine, not a decoration.  Two **rational**
solutions are also verified, so no field extension is needed to see the
gap: at \(k=2\) an explicit four-site packet (6 live splits) and at
\(k=3\) the packet \(D(6)\) of §4 with two cells added, one per colour
(3 live splits).  In both, the checker exhibits an exponent whose split
products are individually nonzero and **cancel** — the mechanism by
which \(P\) can hold while \(T\) fails.

**DIAG-\(\infty\) (conjectured).**  \(T(k)\) has no solution for any
\(k\ge3\).

* \(k=2\): \(T(2)\) **is** soluble — the three one-factors of \(K_4\);
  the census of §5 proves those are its only \(0/1\) solutions.
* \(k=3,4,5\): insoluble, by the theorem of
  [`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md)
  (cited; the \(n=6\) branch is re-run here as a cross-check of the
  encoder, the rest is not).
* \(k\ge6\): **open**.

**Consequence for proof strategy.**  Because \(P(k)\) is soluble at
every \(k\), no route through "the pencil equation is unsatisfiable"
can exist.  What the identity (1) does supply is the exact form of the
gap: a proof must use the *individual* vanishing of split products, not
the vanishing of their shape-sums.  The two-colour statement of §3 is
one instance of this, and the committed note's reading of it — "all the
content is in the simultaneous three-colour condition" — needs the same
sharpening: the content is in the **termwise** condition, since even the
simultaneous three-colour *equation* is always satisfiable.

---

## 3. Two colours are always satisfiable

**Proposition (proved).**  For every \(k\ge2\) the alternating
\(2k\)-cycle, with its two alternating perfect matchings \(M_0,M_1\) as
\(0/1\) matrices, satisfies

\[
 \operatorname{haf}(xW_0+yW_1)=x^k+y^k,
\]

\(h_0(V)=h_1(V)=1\), and **every** split with an empty part is dead.

*Proof.*  \(h_r(S)\ne0\) iff \(S\) is a union of \(M_r\)-edges.  A live
two-part split \((S\in\text{colour }r,\ V\setminus S\in\text{colour }s)\)
would make \(M_r|_S\cup M_s|_{V\setminus S}\) a perfect matching of the
cycle \(M_r\cup M_s\); a \(2k\)-cycle has exactly two, namely \(M_r\)
and \(M_s\), forcing \(S=V\) or \(S=\varnothing\).  The hafnian claim is
the same two-matchings fact.  \(\square\)

*Verified* exactly for \(k=2,\dots,6\), including the computed fact that
each cycle has exactly two perfect matchings.

**Consequence.**  Any argument that only ever inspects two colours at a
time — equivalently, any argument that only uses splits with an empty
part — is structurally insufficient: it is consistent with a realization
at every order.  Every uniform proof must be *three-colour
simultaneous*.  §4 and §6 give two independent quantitative versions of
this: an explicit family killing all empty-part splits at every order,
and the SAT fact that the two-part fragment of the committed engine is
satisfiable at \(n=6\) and \(n=8\).

---

## 4. Hamiltonian triples: the shape \((0,2,N-2)\) can never be forced

**Construction \(D(n)\).**  Let \(n\) be even, \(m=n-1\), and identify
\(V=\mathbb Z_m\cup\{\infty\}\).  For \(r\in\mathbb Z_m\) let \(F_r\) be
the round-robin factor

\[
 F_r=\bigl\{\{x,y\}: x+y\equiv 2r \bmod m,\ x\ne y\bigr\}
     \cup\bigl\{\{r,\infty\}\bigr\},
\]

a perfect matching because \(m\) is odd, and put
\(D(n)=(F_0,F_1,F_2)\) with \(W_r=\operatorname{adj}(F_r)\).

**Lemma H (proved).**  For every even \(n\ge4\) and \(r\ne s\) in
\(\{0,1,2\}\), the union \(F_r\cup F_s\) is a single Hamiltonian cycle.

*Proof.*  On \(\mathbb Z_m\), \(F_r\) is the graph of the reflection
\(\rho_r(x)=2r-x\) (whose unique fixed point \(r\) is matched to
\(\infty\)).  The union of two perfect matchings is a disjoint union of
cycles, and the cycle through \(\infty\) is traced by alternating
\(\rho_r,\rho_s\); two steps of that walk translate by
\(\rho_r\rho_s(x)=x+2(r-s)\).  Since \(m\) is odd and \(|r-s|\in
\{1,2\}\), \(\gcd(2(r-s),m)=\gcd(r-s,m)=1\), so the translation
generates \(\mathbb Z_m\): the walk visits every residue before
returning, and the cycle through \(\infty\) covers all \(n\) vertices.
\(\square\)

**Lemma H2 (proved).**  If \(M_0,M_1,M_2\) are pairwise disjoint perfect
matchings of \(V\) whose pairwise unions are single Hamiltonian cycles,
then for \(W_r=\operatorname{adj}(M_r)\):

1. \(h_r(V)=1\) for every \(r\);
2. \(h_r(S)\ne0\) iff \(S\) is a union of \(M_r\)-edges;
3. **every split with an empty part is dead** — in particular every
   split of shape \((0,2,n-2)\).

*Proof.*  (2) is immediate: the only matchings supported by
\(\operatorname{adj}(M_r)\) are subsets of \(M_r\), so \(h_r(S)\) is
\(1\) or \(0\) according as \(S\) is a union of \(M_r\)-edges or not;
(1) is the case \(S=V\).  For (3), a live split with \(S_t=\varnothing\)
gives \(S_r\) a union of \(M_r\)-edges and \(V\setminus S_r\) a union of
\(M_s\)-edges, so \(M_r|_{S_r}\cup M_s|_{V\setminus S_r}\) is a perfect
matching of the Hamiltonian cycle \(M_r\cup M_s\), which has exactly
two, namely \(M_r\) and \(M_s\); hence \(S_r\in\{\varnothing,V\}\),
excluded for a proper split.  \(\square\)

**Consequence (the inversion).**  Section 6 of the good-crossing note
warns against framing \((0,2,6)\) as "the case to prove live"; Lemma H2
makes that precise and uniform.  The shape \((0,2,N-2)\) — indeed every
shape with an empty part — is dead on an explicit family available at
**every** even order, so **no argument can force it live**.  The
residual question at \(N=8\) is therefore not "is \((0,2,6)\) live" but
"can a packet be live *only* at \((0,2,6)\)", which is what §6 answers.

*Verified*: the construction, the reflection description (so the hand
proof's model and the constructed object cannot drift apart), the
\(\gcd\) step, pairwise disjointness and the Hamiltonicity of all three
unions for every even \(n\) in \(4..24\); the anchors, the co-supports,
the exhaustive empty-part scan (all \(2^n\) masks, all six colour
orders, \(262\,044\) scanned in total, **zero** live) and the emptiness
of \(C_0\cap C_1\cap C_2\) for every even \(n\) in \(4..16\); the full
\(3^n\) split census for \(n\le12\).  \(D(n)\) is *not* termwise dead —
its live shapes are \((2,2,2)\) at \(n=6\), \((2,2,4)\) at \(n=8\),
\(\{(2,2,6),(2,4,4)\}\) at \(n=10\), \(\{(2,2,8),(4,4,4)\}\) at
\(n=12\), all with **no empty part** — which is exactly what the cited
SAT theorem demands at \(n=6,8,10\).

The empty-part scan is a scan that is supposed to report *nothing* on
\(D(n)\) and on the cycles of §3, so the checker also runs a **positive
control**: a four-site packet with one designed live empty-part split
whose colour \(1\) vanishes on the designed pair, which distinguishes a
complement scan from a same-mask scan (mutation M4 was silent before it
was added).  The same scan (`two_part_census`) is the *single*
implementation used everywhere an empty-part verdict is needed — in
particular the deadness test of the §5 censuses is routed through it
rather than re-implemented inline, so this control covers that path
too, and §5 adds a census-level control of its own: a designed packet
on which the same-mask and complement scans disagree on the verdict
itself.

**A second, independent witness.**  The \(K_4\)-block family (three
one-factors inside each block of four) at \(n=8,12\) has *live*
empty-part splits — of shapes \((0,4,4)\) and \((0,4,8)\) — and still
**no** live \((0,2,n-2)\).  So the death of \((0,2,n-2)\) is not an
artifact of "everything two-part is dead".

**The Boolean shadow.**  \(D(n)\) satisfies the recurrence rules
(5)–(7) of the committed engine, its units, and **all** its two-part
clauses, at every even \(n\) in \(4..16\) (computed from the actual
hafnians).  So the two-part fragment of the engine has an explicit model
at every audited order; its `UNSAT` genuinely consumes the three-part
clauses.  §6 confirms this from the solver side.

---

## 5. Lemma U2, and why pair-deletion inductions stall

For a packet write \(C_r=\{\,\{u,v\}: h_r(V\setminus\{u,v\})\ne0\,\}\)
for the **co-support** of colour \(r\).

**Lemma U2 (proved).**  Suppose every split with an empty part is dead.
If \(\{u,v\}\in C_r\cap C_s\) with \(r\ne s\), then
\(W_r(u,v)=W_s(u,v)=0\).

*Proof.*  Colour \(\{u,v\}\) with \(s\) and \(V\setminus\{u,v\}\) with
\(r\), leaving the third part empty: a proper even split, whose product
is \(h_r(V\setminus\{u,v\})\,h_s(\{u,v\})=h_r(V\setminus\{u,v\})\,
W_s(u,v)\).  Deadness kills it and the first factor is nonzero because
\(\{u,v\}\in C_r\), so \(W_s(u,v)=0\); exchanging \(r\) and \(s\) gives
\(W_r(u,v)=0\).  \(\square\)

**Corollary U2.1 (proved).**  Under the same hypothesis, expanding
\(h_r(V)\ne0\) at any pivot \(u\) produces a *carrier* pair
\(\{u,v\}\in C_r\) with \(W_r(u,v)\ne0\); by U2 no carrier of colour
\(r\) lies in any \(C_s\), \(s\ne r\).  Hence any pair deletable in all
three colours — i.e. in \(C_0\cap C_1\cap C_2\), which is what an
induction "delete a pair, keep the three anchors alive at \(n-2\)"
needs — is a **common non-edge of all three colours**, and in particular
is never an edge of a supported matching.  The natural pair-deletion
step is therefore never available.

This sharpens the committed proof's own statement of its obstacle to
induction ("a realization at larger order does not automatically
restrict to a common feasible principal set in all three colors"): the
obstacle is not a technicality of the encoding, it is forced by the
two-part clauses alone.  On \(D(n)\) one has \(C_r=M_r\) exactly, so the
three co-supports are pairwise disjoint and \(C_0\cap C_1\cap C_2=
\varnothing\) — verified for every even \(n\) in \(4..16\).

**Two exhaustive censuses, and a disclosed vacuity.**

| census | packets | empty-part-dead | with a co-support overlap | U2 violations | contrapositive instances |
|---|---|---|---|---|---|
| \(0/1\) packets at \(n=4\) (\(37^3\) of the \(64^3\): the \(37\) matrices with \(h\ne0\)) | \(50\,653\) | \(6\) | **0** | 0 | \(490\,176\) |
| one-factor-union packets at \(n=6\) (\(31^3\) of the \(32^3\)) | \(29\,791\) | \(60\) | **0** | 0 | \(1\,026\,720\) |

(The excluded matrices are those with \(h_r(V)=0\), which violate the
anchors outright; the censuses are exhaustive over the rest.)

The zeros in the fourth column mean that U2's hypothesis and a
co-support overlap are **never simultaneously realized** on these
families, so U2 itself is *vacuous* there; that is disclosed rather than
hidden, and it is unsurprising — U2 says that overlaps are precisely
what deadness forbids.  What the censuses do verify non-vacuously is the
lemma's **mechanism**, through the contrapositive: on every instance
where an overlapping pair carries a cell, the split named in the proof
above — the pair alone in the colour where it is an edge, its
complement in the other — is *required to be returned by the
independent empty-part scan* (`two_part_census`) on that packet.  The
check exercises the scan itself; recomputing the split *product* would
be tautological, since the antecedent (the pair lies in both
co-supports and is an edge of the sink colour) already forces it
nonzero.  The censuses' deadness verdict is routed through the same
scan, and a **census-level positive control** exhibits a packet on
which a same-mask scan and the complement scan disagree on the verdict:
no proper even mask is live in two colours at once, yet
\(S=\{0,1\}\) in colour \(0\) against \(\{2,3,4,5\}\) in colour \(1\)
is live, so the verdict is required to be *live* where a same-mask scan
would report *dead*.  Both censuses also
classify their solutions: the empty-part-dead packets are exactly the
ordered triples of **distinct one-factors** (\(6=3!\) at \(n=4\),
\(60=5\cdot4\cdot3\) at \(n=6\)).  At \(n=4\) every split is a two-part
split, so this is also a classification of the \(0/1\) solutions of
\(T(2)\).

---

## 6. The shape-restricted census

The committed engine forbids **every** proper split.  Restricting the
forbidden shapes asks a strictly harder question: is
\(\{\text{recurrence}+\text{units}+\text{clauses for shapes in }\Sigma\}\)
`UNSAT` for a proper subset \(\Sigma\)?  `UNSAT` there means: *every*
diagonal packet with the three pure anchors has a live split whose shape
is **outside** \(\Sigma\).

The encoder is the committed one — `even_masks`, `add_iff_and`,
`add_zero_forbids_unique`, `canonical_matching`, `integer_partitions`
and `matching_of_cycle_type` are imported from
[`computations/verify_diagonal_recurrence_obstruction.py`](../computations/verify_diagonal_recurrence_obstruction.py),
and in the unrestricted mode the produced CNF is required to be
**clause for clause identical** to that module's own, with the counts
published in
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md)
(\(n=6\): \(411\) variables, \(2\,904\) clauses, \(5\) branches;
\(n=8\): \(2\,988\) variables, \(23\,844\) clauses, \(9\) branches).
Symmetry breaking is the committed one, unchanged.

| \(n\) | dropped shapes | verdict | vars | clauses | split clauses kept | live shapes of the model |
|---|---|---|---|---|---|---|
| 6 | — | **UNSAT** | 411 | 2904 | 180 | — |
| 6 | \((0,2,4)\) | SAT | 411 | 2814 | 90 | \((0,2,4)\): 12 |
| 6 | \((2,2,2)\) (two-part only) | SAT | 411 | 2814 | 90 | \((2,2,2)\): 4 |
| 8 | \((0,2,6)\) | **UNSAT** | 2988 | 23676 | 1470 | — |
| 8 | \((0,2,6)\), \((0,4,4)\) | SAT | 2988 | 23466 | 1260 | \((0,2,6)\): 18, \((0,4,4)\): 15 |
| 8 | \((2,2,4)\) (two-part only) | SAT | 2988 | 22584 | 378 | \((2,2,4)\): 12 |
| 10 | \((0,2,8)\) | **unresolved** | — | — | — | — |

Every `SAT` model is independently re-audited: the recurrence rules are
recomputed from the model, every **kept** clause is checked, and the
model's live shapes are read off and required to lie among the
*dropped* shapes.  The \(n=6\) unrestricted run reproduces the committed
verdict and counts, as a cross-check of the encoder.

Three readings.

* **The new \(n=8\) theorem.**  Dropping only \((0,2,6)\) is `UNSAT`:
  every diagonal packet with the three pure anchors has a live split of
  some shape **other than** \((0,2,6)\).  This is the statement section
  6 of the good-crossing note cites as unaudited scratch.
* **The two-part fragment is satisfiable** at \(n=6\) and \(n=8\), which
  is the solver-side twin of §3 and §4: \(D(n)\)'s Boolean shadow is an
  explicit model of it at every order.  Any engine that forbids only
  empty-part splits cannot close.
* **\(n=10\) is unresolved.**  It is not attempted by the checker
  (opt-in `--n10`, which records **no expected verdict**: it reports
  what the solver returns without asserting it); the scratch run of the
  same instance did not terminate, and nothing here changes that.

---

## 7. Composition at \(N=8\), and what this changes in the committed cluster

**Composition (at \(N=8\)).**  Let \(A\) be an exact ternary source on
\(N=8\) sites, and let \(W_c\) be its diagonal shadow as in Theorem B of
[`notes/exact-source-live-split-forcing.md`](exact-source-live-split-forcing.md).
The anchors are \(1\) by Lemma 0, so by the \(n=8\) drop-\((0,2,6)\)
theorem the shadow has a live split of shape \(\ne(0,2,6)\).  The
\(N=8\) shapes are \((0,2,6)\), \((0,4,4)\), \((2,2,4)\), with
\(X=12,16,20\) crossing pairs; the last two satisfy \(X>3N/2=12\), so by
**C4′** of
[`notes/good-crossing-matching-forcing.md`](good-crossing-matching-forcing.md)
(\(\#\{\text{good crossing pairs}\}\ge X-3N/2\)) that split has a good
crossing pair.  Hence **at \(N=8\) a good crossing pair exists
unconditionally**, closing the one order that C5′ had left open.

**The caveat, in the committed note's own words.**  "A good crossing
pair exists" is *weaker* than what Theorem C delivers, namely a nonzero
crossing matching **all** of whose crossing edges are good.  The
counting route bounds the number of bad crossing pairs; it says nothing
about the cells of a prescribed matching, and the saturation analysis
that bridges the two is not closed.  This note does not touch that gap.

**The C4′/C5′ improvement is load-bearing, and the census proves it.**
With the committed C4/C5 bound (\(X\le2N\)) one would have to drop
\((0,4,4)\) as well — and that instance is `SAT`.  So the composition
above genuinely needs the sharper \(3N/2\) count of the good-crossing
note; with the older bound it fails at \(N=8\), and the failure is
exhibited by an audited countermodel rather than argued.

**Upgrade of the good-crossing note's section 6.**  That section records
four claims as unaudited session scratch.  Their status is now:

1. *"shape \((0,2,N-2)\) is provably dead on an explicit family at every
   even order"* — **audited and strengthened** (§4): the family is
   \(D(n)=(F_0,F_1,F_2)\), the Hamiltonicity is proved for all even
   \(n\) rather than searched, and the death covers every shape with an
   empty part.
2. *"dropping the shape \((0,2,6)\) is UNSAT at \(n=8\)"* — **audited**
   (§6), with the committed encoder reproduced clause for clause.
3. *"the \(n=10\) drop-\((0,2,N-2)\) run is unresolved"* — **confirmed**
   (§6); still unresolved.
4. *"the pencil identity … so 'all split products vanish and
   \(h_r(B)=1\)' is **exactly** \(\operatorname{haf}(\sum_rx_rW_r)=
   x_0^k+x_1^k+x_2^k\)"* — **corrected** (§1–§2).  The identity is
   proved and the forward implication is right; the word *exactly*
   overstates it.  The converse fails at every \(k\): the pencil
   equation has solutions for all \(k\ge2\), with live splits.  Its
   companion remark — that the two-colour shadow is always satisfiable,
   "which locates all the content in the simultaneous three-colour
   condition" — is confirmed but must be sharpened the same way: the
   content is in the **termwise** condition, not in the three-colour
   equation, which is also always satisfiable.

Nothing in the good-crossing note's theorems depends on the corrected
sentence: §6 is that note's outlook section, and its checker uses none
of it.

**Outlook (unaudited scratch, recorded for honesty).**  A parallel
session investigation reports that the Fermat-geometry constraints on
pencil solutions — every star has rank \(\ge2\); a rank-\(2\) star's
pencil point lies on the Fermat curve \(x_0^k+x_1^k+x_2^k=0\); and if
two adjacent sites share a pencil point then their edge form is the
tangent line there — are proved and are *satisfied* by the
counterexamples of §2.  Whether they collide with the **additional**
termwise vanishing conditions is the open question that route now faces.
This paragraph is not audited and is not used by the checker.

---

## 8. Scope

1. Everything here is about **diagonal** packets: symmetric
   zero-diagonal scalar edge matrices.  That is the shadow an exact
   ternary source induces (Theorem B of the committed note), not an
   exact source itself; no exact ternary source at \(N\in\{6,8,10\}\) is
   available to test on, since showing that none exists is the project's
   aim.
2. The `UNSAT` verdicts are used only in the sound direction, exactly as
   the committed proof states: the formula is a *relaxation* of
   arbitrary field-valued hafnian data, so `UNSAT` obstructs and `SAT`
   only survives at support level.  The audited countermodels are
   support assignments, not packets.
3. DIAG-\(\infty\) is proved only at \(k=3,4,5\), by the **cited** SAT
   theorem; \(k\ge6\) is open, and this note supplies no induction.
   Lemma U2 explains why the obvious induction step is unavailable; it
   does not replace it.
4. The composition of §7 delivers a good crossing **pair** at \(N=8\).
   It does **not** deliver Theorem C's matching-level conclusion, and it
   does not touch the saturating gap or the \(N\ge10\) uniformity
   question.
5. The \(n=10\) shape-restricted instance is unresolved, so the uniform
   composition is not closed at any \(N\ge10\) either — there it rests
   on C4′/C5′ alone, as the good-crossing note already states.
6. Lemma U2 is a hand proof; on the two censuses run here its hypothesis
   and its overlap conclusion are never simultaneously realizable, so
   only its contrapositive is exercised non-vacuously (§5).
7. Per project discipline this is a research reduction until
   independently audited.  **Krenn's conjecture remains open.**

---

## 9. Verification

~~~text
python3       computations/verify_diagonal_termwise_census_and_pencil_guard.py
python3 -O    computations/verify_diagonal_termwise_census_and_pencil_guard.py
python3 -I    computations/verify_diagonal_termwise_census_and_pencil_guard.py
python3 -S    computations/verify_diagonal_termwise_census_and_pencil_guard.py
python3 -I -S computations/verify_diagonal_termwise_census_and_pencil_guard.py
python3 -m py_compile computations/verify_diagonal_termwise_census_and_pencil_guard.py
~~~

Runtime is **under four seconds**, of which the six SAT calls take under
one.  (`python3 -I` does not prepend the script's directory to
`sys.path`, so the checker inserts its own directory, computed from
`__file__`, before importing the committed engine.)

**Solver availability, and what a run without one does establish.**  The
committed engine imports PySAT at module scope and dies without it.
Here the exact sections — the pencil identity, the pencil guard, the
two-colour proposition, \(D(n)\), the \(K_4\) blocks, Lemma U2 and the
shape arithmetic — need no solver and always run; §6 imports PySAT *and*
the committed engine lazily.  Under `python3 -S` site-packages is not on
the path and that import fails, which is not hypothetical but two of the
six commands above.  In that case the census is **skipped with a loud
flag**: the run prints that the four verdicts are `NOT ESTABLISHED` in
this run and that the \(N=8\) composition is therefore conditional, the
SAT ledger is not hashed, and no verdict is fabricated.  The exact
ledger and its digest are identical with and without the solver.  Run
with `--require-solver` to restore a hard failure, with the diagnostic
text used by the repository's other solver-dependent checkers, exit
code 1.

**Ledgers.**  Two frozen digests, both hashing *computed* content.  The
exact ledger records the pencil-identity instances with their monomial
and split-term counts and the dropped sharpness term; the cyclotomic
guards with their moduli, degrees, live-split counts and shapes,
together with the \(\mathbb Z[s]/(s^3+1)\) probe of §2; the
rational solutions with their packets and cancelling exponents; the
two-colour records; \(D(n)\)'s construction data, anchors, scans,
co-supports, live shapes and Boolean-shadow verdict; the empty-part
control; the \(K_4\)-block families; the U2 deadness control and both
U2 censuses; and the shape arithmetic to \(N=60\).  The SAT ledger records the encoder counts, and
for each run its mode, verdict, variable/clause/kept counts, dropped
shapes, branch counts and a hash of the audited countermodel.  Every
boolean in both is computed — there is no hard-coded truth value — and
the published counts of the committed engine are additionally required
to agree with that engine's *own* builder, so an upstream change breaks
this checker rather than drifting away from it.

~~~text
exact ledger : fb019894c5dbf111dd6536c870812c7c20a07919025d3ce0ad79dcf2b31a4a5c
SAT ledger   : da4b6196c5182b7d66e0f46f99e23e0409ef3486a907ba3882935790681f3b82
~~~

**Mutation-tested with twenty-two injections.  All twenty-two raise
under both `python3` and `python3 -O`, with the same message, naming the
broken property.**  Injections M11, M12 and M15 exercise §6 and are
therefore inert under `-S`, where that section is skipped — which is the
point of the skip flag.  M20–M22 exercise the probes added at audit:
in particular M21 is the same-mask corruption that was previously
*silent* when injected into the census's own inline deadness scan — it
now raises, because the deadness verdict is routed through the shared
scan and guarded by the census-level control.

| # | injection | message raised |
|---|---|---|
| M1 | the pencil's right-hand side groups splits by \(|S_r|\) instead of \(|S_r|/2\) | pencil identity failed at n=4 seed=11: the polynomial hafnian of the pencil differs from the sum over ordered even splits |
| M2 | the sharpness probe deletes nothing | pencil identity sharpness probe is vacuous at n=4 seed=11: deleting a nonzero split term left the two sides equal |
| M3 | the two-perfect-matching count of the \(2k\)-cycle reads one matching twice | the 4-cycle does not have exactly two perfect matchings |
| M4 | the empty-part scan compares a mask with itself, not its complement | two-part control: the empty-part scan missed the designed live split S_0={0,1}, S_1={2,3} |
| M5 | co-supports read \(h_r(V)\) instead of \(h_r(V\setminus\{u,v\})\) | D(4): the co-support of colour 0 is not its own matching |
| M6 | the reflection description of \(F_r\) is shifted by one | F_0 at n=4 is not the reflection x -> 2r-x plus the infinity edge, so the hand proof's model and the constructed object have drifted apart |
| M7 | a split counts as live when *any* colour factor is nonzero | D(4): a live shape has an empty part |
| M8 | Lemma U2's census drops its deadness hypothesis | n=4 0/1 census: Lemma U2 is violated -- a packet with every empty-part split dead has an overlapping co-support pair carrying a cell |
| M9 | Lemma U2's contrapositive instances are never counted | n=4 0/1 census: the Lemma U2 census is vacuous -- no overlapping co-support pair carrying a cell was ever exhibited |
| M10 | C5′ reverted to the committed \(X\le2N\) bound | C5' recomputation broken: N=8 does not leave exactly the shape (0,2,6) |
| M11 | the encoder drops the zero-forbids-unique clauses | the unrestricted encoder does not reproduce the committed engine's CNF at n=6 clause for clause |
| M12 | the drop-\((0,2,n-2)\) mode is inverted into keep-only-\((0,2,n-2)\) | shape-restricted census: n=8 mode=drop-0-2 returned SAT, not the recorded UNSAT |
| M13 | the frozen exact ledger digest is altered | diagonal termwise census and pencil guard ledger changed |
| M14 | the \(k=3\) rational solution loses its cancelling weight | strictness witness k=3 does not solve haf(pencil) = x_0^k + x_1^k + x_2^k |
| M15 | the frozen SAT ledger digest is altered | shape-restricted SAT census ledger changed |
| M16 | the cycle guard uses even powers of \(\zeta\), not roots of \(t^k=-1\) | cycle guard k=2: a designated weight is not a root of t^k = -1 |
| M17 | the cycle guard's colour-2 weight loses its sign | cycle guard k=3: haf(x_0W_0 + x_1W_1 + x_2W_2) is not x_0^k + x_1^k + x_2^k |
| M18 | the cyclotomic polynomial is built from \(s^{m}+1\) | an exact polynomial division left a remainder |
| M19 | the empty-part control loses its discriminating cell | two-part control is not discriminating: colour 1 is nonzero on the designed pair, so a same-mask scan would agree with a complement scan here |
| M20 | the \(\mathbb Z[s]/(s^3+1)\) probe reduces with \(s^3=+1\) instead of \(s^3=-1\) | Z[s]/(s^3+1) probe: the coefficient of x_1^2 x_2 of prod_i (x_1 - s^(2i+1) x_2) did not reduce to 1 - s + s^2 modulo s^3 + 1 |
| M21 | the shared U2 deadness helper compares a mask with itself, not its complement (the M4-class bug, injected into the census's own path) | U2 deadness control: the designed live split S={0,1} in colour 0 against its complement {2,3,4,5} in colour 1 was not returned by the deadness scan |
| M22 | the contrapositive check looks up the predicted split with its colours exchanged | n=4 0/1 census: the split predicted by Lemma U2's proof -- the overlapping pair alone in the colour where it is an edge, its complement in the other -- is not returned by the empty-part scan |
