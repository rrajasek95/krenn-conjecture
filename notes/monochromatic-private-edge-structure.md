# Private edges in the monochromatic branch, by Laplace alone

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  Nothing here is a partial
case of the conjecture and nothing here decides \((8,3)\).

## 1. Why this branch matters — corrected

An earlier version of this note justified the branch by a dichotomy: a solution
whose colour-pair binary restrictions are all **rigid** has every cross cell
zero, hence is monochromatic, so the monochromatic case was "one of the two
arms the whole problem splits into".

**That justification is dead.**  A subsequent result proves
\(\ker\Phi^{ab}_v\neq0\) at **every** vertex and **every** colour pair in any
solution — rigidity fails at each of the \(24\) places individually, not
merely globally.  So the rigid arm is *empty* and the dichotomy is vacuous:
all of \((8,3)\) is the non-rigid branch.

The monochromatic case remains a legitimate sub-case — a solution could happen
to have every edge matrix diagonal — but it is **not forced**, and nothing
below should be read as covering half the problem.

## 2. The collapse

Monochromatic means every edge matrix is diagonal, so only
\(Z^c_{uv}=A_{uv}[c][c]\) is live.  A matching monomial then survives only when
both ends of every matched edge carry the same colour, giving

\[
 T[\iota]=\prod_c\operatorname{haf}\bigl(Z^c[V_c]\bigr),
 \qquad V_c=\iota^{-1}(c).
\]

An odd class has no matching, so its coefficient vanishes for free.  The
\(6561\) equations therefore collapse to the \(1641\) even-class words:

\[
 \operatorname{haf}(Z^c)=1\ (c=0,1,2),
 \qquad
 \prod_c\operatorname{haf}(Z^c[V_c])=0\ \text{on the other }1638,
\]

in \(3\cdot28=84\) unknowns rather than \(252\).

**This collapse is not new.**  It is the encoding of
`computations/search_diagonal_f3_n8.py`, whose docstring states it.  It is
re-derived here from the literal matching tensor rather than assumed, because
everything below rests on it.

## 3. What follows, with no cancellation argument at all

Write \(\mathcal S_c=\{S\text{ even}:\operatorname{haf}(Z^c[S])\neq0\}\).

**A — the complement condition.**  The empty class contributes
\(\operatorname{haf}\) of the empty matrix, which is \(1\).  So a two-class
partition gives, for \(a\neq b\) and every even \(S\notin\{\emptyset,[8]\}\),

\[
 S\in\mathcal S_a\ \Longrightarrow\ [8]\setminus S\notin\mathcal S_b.
\]

**B.**  \(\mathcal S_c\) contains a \(2\)-set, since
\(\operatorname{haf}(Z^c[\{u,v\}])=Z^c_{uv}\) and \(Z^c=0\) would contradict
\(\operatorname{haf}(Z^c)=1\).

**C — the private-edge theorem.**  Laplace expansion along a vertex \(u\),

\[
 \operatorname{haf}(Z^c[S])=\sum_{v\in S\setminus u}Z^c_{uv}
   \operatorname{haf}\bigl(Z^c[S\setminus\{u,v\}]\bigr),
\]

applied at \(S=[8]\), where the value is \(1\), forces for **every** colour
\(c\) and **every** vertex \(u\) a partner \(v\) with \(Z^c_{uv}\neq0\) and
\([8]\setminus\{u,v\}\in\mathcal S_c\).  Both the \(2\)-set and its complement
then lie in \(\mathcal S_c\), so A pins the colour set of each to \(\{c\}\):

> the edge \(\{u,v\}\) is live in colour \(c\) and **dead in the other two**,
> and the complementary six-set has zero hafnian in the other two.

So each colour's private edges \(P_c\) cover all eight vertices, the three
\(P_c\) are pairwise disjoint, and every vertex has three private edges in
three different colours going to three **distinct** neighbours.

**D — the disjoint-private-pair lemma.**  For disjoint \(e_a\in P_a\),
\(e_b\in P_b\) with \(a\neq b\), the three-class partition
\((e_a,e_b,\text{rest})\) has two nonzero factors, so

\[
 \operatorname{haf}\bigl(Z^c[[8]\setminus(e_a\cup e_b)]\bigr)=0,
 \qquad c\ \text{the third colour.}
\]

Such a pair always exists: \(P_b\) covers the six vertices outside \(e_a\), at
most two of its edges meet \(e_a\), and six vertices need at least three edges.

## 4. How far this gets, measured

**Not far enough, and that is the point of recording it.**  Over all \(32{,}970\)
triples of pairwise edge-disjoint perfect matchings — the sparsest private
structure consistent with C, hence the one killing fewest four-sets — the
number of four-sets surviving for a colour is **\(62\) of \(70\)**.

Colour \(c\) needs a live four-set, by descending the Laplace expansion twice.
It comfortably has one.  **The private-edge structure does not close the
branch.**

## 5. What this does not say

1. Nothing about whether \((8,3)\) has a solution, and it does not decide the
   monochromatic branch.
2. A and D are **support** conditions.  The four-set conditions D produces are
   genuine **cancellation** conditions — the hafnian of a four-set is a sum of
   three products — and nothing here touches them.  That is where the
   difficulty actually sits.
3. The census in section 4 is over the sparsest private structure.  A denser
   one kills more; the bound is not claimed to be tight.

## 6. Audit

The dependency-free checker
[`verify_monochromatic_private_edge_structure.py`](../computations/verify_monochromatic_private_edge_structure.py)
verifies the collapse against the **literal** eight-vertex matching tensor at
every one of the \(6561\) words on random diagonal packets; the \(1641/3/1638\)
counts; that the empty hafnian is \(1\) and the two-set hafnian is the edge
weight; Laplace expansion at every vertex and every even set; that
\(\operatorname{haf}(Z)\neq0\) forces a Laplace partner at every vertex, with a
non-vacuous contrapositive; that every edge cover of \(K_8\) has an edge
disjoint from any fixed edge, exhaustively over \(5985\) covers; and the
four-set census of section 4.

Standard library only, exact integer arithmetic, no floats, no numpy, zero bare
asserts, passing `python3`, `-O` and `-I -S`, byte-identical across hash seeds
\(0,1,42\).

**Mutation-tested.**  Three injected faults — a wrong even-word count, a
negated collapse identity, and a negated Laplace-partner claim — each raise,
with exit code \(1\), under **both** `python3` and `python3 -O`.
