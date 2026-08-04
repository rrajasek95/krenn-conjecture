# Selected triples, exact rewrites, and the Petersen escape

This note records exactly what can be extracted from three selected
nonzero constant matching monomials.  There is a useful Laurent rewrite
and, in the binomial case, a genuine odd-cycle obstruction.  Two sharp
barriers remain: the rewrite is locally reversible, and it need not stay in
the part of the source seen by the three-copy alternating invariant.  The
second failure already occurs on a 3-connected, matching-covered,
tight-cut-free support.

Throughout, an **occurrence** means a nonzero aggregate coordinate

\[
                         x=(uv;i,j),\qquad A_{uv}(i,j)\ne0.
\]

Thus two coordinates on the same underlying pair are different
occurrences.  A decorated perfect matching `P` consists of one occurrence
at every vertex, and its monomial is denoted by `z(P)`.  Its endpoint
colors form a coloring `c_P`.

## 1. The exact fourth-matching rewrite

Choose, for each `r=0,1,2`, a perfect matching `P_r` whose constant
color-`r` monomial

\[
                              \mu_r=z(P_r)                 \tag{1}
\]

is nonzero.  Their occurrence-disjoint union `U` is a cubic multigraph: at
every vertex it has exactly one occurrence of each local color.  Put

\[
                         W(U)=\mu_0\mu_1\mu_2.             \tag{2}
\]

For even `n>=6`, the three-one-factors lemma gives a fourth perfect
matching `R` contained in `U`.  Let `c=c_R`, let

\[
                  r=z(R),\qquad Q=U\setminus R,
                  \qquad q=\prod_{x\in Q}A_x.             \tag{3}
\]

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017); the occurrence-multigraph form used here is Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303 (the simple-graph form is
Thm 1 of Chandran-Gajjala, arXiv:2202.05562).  See
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

Here `Q` is a two-factor of occurrences.  The coloring `c` is mixed, `R`
is the unique `c`-compatible matching contained in `U`, and

\[
                         \mu_0\mu_1\mu_2=rq.               \tag{4}
\]

Let `F_c^times` be the finite set of `c`-compatible perfect matchings with
nonzero monomial.  Exact monochromaticity gives

\[
                 0=\sum_{N\in F_c^\times}z(N)
                   =r+\sum_{N\ne R}z(N).                  \tag{5}
\]

Multiplying by the nonzero monomial `q` proves the promised identity.

**Lemma 1.1 (selected-triple rewrite).**

\[
 W(U)=-\sum_{\substack{N\in F_c^\times\\N\ne R}}
                         W(Q\mathbin\sqcup N),             \tag{6}
\]

where

\[
                         W(Q\mathbin\sqcup N)=qz(N).       \tag{7}
\]

Every `Q disjoint-union N` is again locally rainbow: its three incident
occurrences at a vertex have colors `0,1,2`.  Moreover every edge of
`N triangle R` belonging to `N` is outside `U`.

**Proof.**  Equations (4)--(5) give (6).  At a vertex of color `c(v)`,
`Q` contains the two selected occurrences of the other colors, while `N`
contains an occurrence of color `c(v)`.  This proves the local-rainbow
claim.  Within `U` there is only one occurrence at port `(v,c(v))`, namely
the `R`-occurrence.  A compatible matching using only occurrences of `U`
is consequently forced to equal `R`.  Thus every changed `N`-occurrence is
external. `QED`

This is stronger than the assertion that a mate exists: it rewrites the
product of the three selected constant terms as a sum of products of
locally rainbow cubic occurrence networks.

## 2. Replacement cliques and the only automatic cycle obstruction

Fix any locally rainbow cubic occurrence network `U`, a mixed perfect
matching `R` contained in it, and put `Q=U\setminus R`.  All nonzero matchings
in the coloring fiber of `R` give the replacement states

\[
                         U_N=Q\mathbin\sqcup N.             \tag{8}
\]

They obey the exact zero-sum relation

\[
                         \sum_N W(U_N)=0.                  \tag{9}
\]

The move is intrinsically reversible: `U_N` contains the mixed matching
`N`, and replacing it by `R` returns to `U`.  Thus a rewrite which merely
chooses one cancellation mate always admits an immediate two-cycle.  A
terminating rewrite needs an additional global order not supplied by (5).

There is one useful exact consequence when all fibers used by a sequence
are binomial.

**Lemma 2.1 (binomial replacement graph is bipartite).**  Form a graph
whose vertices are nonzero locally rainbow cubic occurrence networks and
whose edges replace a contained mixed matching `R` by its unique other
nonzero same-coloring mate `N`.  If the relevant mixed fibers are
binomial, this graph has no odd cycle.

**Proof.**  The binomial coefficient equation is `z(N)=-z(R)`.  Since the
unchanged complement has nonzero product,

\[
                             W(U_N)=-W(U).                 \tag{10}
\]

Along a closed walk of length `ell`, multiplication gives
`W(U)=(-1)^ell W(U)`.  The occurrence product is nonzero, so `ell` is even.
`QED`

Equivalently, an odd replacement cycle is a Laurent source-ideal
certificate.  This is the state-level form of the odd-circulation test for
binomial matching fibers.  It is a real obstruction, but the forced
two-cycle shows why one fourth matching does not supply it.

## 3. What the three-copy epsilon invariant sees

Let an ordered triple of decorated perfect matchings `(L_0,L_1,L_2)` be
**rainbow** if their three local colors are distinct at every vertex.  Its
coordinate term in the three-copy alternating invariant is

\[
 \sigma(L_0,L_1,L_2)z(L_0)z(L_1)z(L_2),\qquad
 \sigma=\prod_v\epsilon(c_{L_0}(v),c_{L_1}(v),c_{L_2}(v)). \tag{11}
\]

Suppose `L_1,L_2` are fixed and all matchings `N` in a coloring fiber can
occupy the first slot while keeping the triple rainbow.  The local color of
that slot is the same for every `N`, hence its epsilon sign is also the
same.  Therefore their complete contribution is

\[
 \sigma z(L_1)z(L_2)\sum_{N\in F_c^\times}z(N)=0.         \tag{12}
\]

This proves:

**Lemma 3.1 (epsilon neutrality).**  Replacing a matching by a
same-coloring cancellation mate never changes the local epsilon sign.  On
every replacement family which stays in one matching-triple slot, the
three-copy alternating relation is exactly the original mixed coefficient
equation multiplied by a common nonzero monomial.  It supplies no new
sign-reversing involution.

For the selected rewrite, (12) applies directly when the two-factor `Q`
has only even cycles: alternate each cycle to obtain two perfect matchings
`L_1,L_2`.  Changing the alternation on one even cycle swaps two epsilon
slots at an even number of vertices, so it does not change the total sign.

If `Q` has odd cycles, this particular factorization is unavailable.  This
is already the prism situation: the complement of its fourth matching is
two triangles.  More seriously, `Q disjoint-union N` itself can fail to
admit *any* decomposition into three perfect matchings.  Its occurrence
product then is not a monomial in the matching-triple expansion of the
three-copy epsilon invariant.  The next example shows that neither
matching-coveredness nor the absence of tight cuts prevents this escape.

## 4. A tight-cut-free Petersen escape

Use vertices `0,...,9` and select the following three constant matchings:

\[
\begin{aligned}
 P_0&=\{01,23,49,56,78\},\\
 P_1&=\{04,12,38,59,67\},\\
 P_2&=\{05,16,27,34,89\}.                                \tag{13}
\end{aligned}
\]

Put a color-`r,r` occurrence of weight one on every edge of `P_r`.
Their union is the pentagonal prism, with the two rim cycles

\[
 0-1-2-3-4-0,\qquad 5-6-7-8-9-5.              \tag{14}
\]

It contains the fourth matching

\[
                         R=\{05,16,27,38,49\}.             \tag{15}
\]

The induced mixed coloring is

\[
                         c=22210\,22210.                  \tag{16}
\]

Add the four aggregate cells

\[
\begin{array}{c|c|c}
\text{pair}&\text{endpoint colors}&\text{weight}\\ \hline
18&(2,1)&-1\\
26&(2,2)& 1\\
39&(1,0)& 1\\
47&(0,2)& 1.
\end{array}                                               \tag{17}
\]

Together with the already present occurrence `05;(2,2)`, they form

\[
                         N=\{05,18,26,39,47\}.             \tag{18}
\]

The three constant fibers are exactly `P_0,P_1,P_2`, each with coefficient
one.  Indeed, (17) adds no `(0,0)` or `(1,1)` occurrence.  Its only new
`(2,2)` occurrence is `26`; using it strands the selected partners `1` and
`7`, so it cannot replace `P_2` in a constant-color matching.

At the coloring (16), the selected prism supplies only the matching `R`.
The only additional allowed port occurrence at each changed vertex is the
one in `N`.  The symmetric difference `R triangle N` is a single
eight-cycle and `05` is shared, so the complete fiber consists of exactly
`R,N`.  Their weights are `1,-1`; hence this mixed coefficient vanishes
exactly.

Now remove `R` from the selected occurrence prism and insert `N`.  The
remaining ten selected occurrences are the two 5-cycles (14), while the
new cross matching is

\[
                 i\longmapsto 5+3i\pmod 5.                \tag{19}
\]

The resulting cubic graph is the Petersen graph.  It has six perfect
matchings, and the complement of each is two 5-cycles.  Consequently it is
not three-edge-colorable: in a three-edge-coloring, deleting any one color
class would leave a union of even alternating cycles.  Thus the right-hand
monomial `qz(N)` in (6) has left the matching-triple epsilon expansion.

This failure is not caused by a weak underlying support.  The full support
has nineteen pairs.  It contains the 3-connected pentagonal prism, every
prism edge belongs to one of (13), and every added edge belongs to (18), so
it is 3-connected and matching-covered.  It also has no nontrivial tight
cut.  One quick way to see the last assertion is that a tight odd shore
would be crossed once by each of `P_0,P_1,P_2`, making its boundary in the
cubic prism have size three; the pentagonal prism has no nontrivial
three-edge cut.  The finite audit cited below checks all odd shores
directly.

The model is deliberately not a Krenn counterexample.  For example the
mixed coloring `0000000222` has a singleton term of weight one.  What it
proves is sharper and appropriately limited: three exactly normalized
constant fibers, the selected fourth-matching factorization, an exact
opposite-weight cancellation mate, and the strongest current support-graph
normal forms do not keep the rewrite inside the source-epsilon sector.

## 5. Border scaling and the pole in the rewrite

The rewrite is Laurent rather than polynomially bounded.  In the usual
six-vertex prism degeneration one can normalize

\[
                  \mu_0\mu_1\mu_2=1,\qquad r=t,
                  \qquad q=t^{-1}.                         \tag{20}
\]

Thus the unwanted mixed term tends to zero while its complementary
two-factor diverges.  Multiplying a hypothetical exact cancellation
equation by `q` would turn a mate sum of order `t` into an order-one term.
At `t=0` the source expression is undefined even though the output limit is
finite.  This is exactly why (6) cannot become a polynomial output
invariant and why a rational invariant based on `q` must control its pole.

The ten-vertex model has the same local phenomenon for every `t!=0`.
Give selected edges `01,49` weights `t^{-1},t`, respectively, give the new
cell on `18` weight `-t`, and leave all other displayed weights one.  Then

\[
 \mu_0=\mu_1=\mu_2=1,\qquad z(R)=t,\qquad z(N)=-t,
 \qquad q=t^{-1},                                         \tag{21}
\]

so the chosen mixed fiber vanishes while the two sides of (6) stay `1`
and `-1`.  The source escapes to infinity as `t` tends to zero.  This does
not make the full output converge to the target; it is an exact audit of
the pole that any selected-triple rational invariant must handle.

## 6. Consequence for this route

The selected-triple mechanism yields two reusable facts:

1. the exact locally-rainbow rewrite (6); and
2. the odd-cycle obstruction of Lemma 2.1 whenever enough relevant fibers
   are binomial.

But neither a terminating rewrite nor an epsilon sign involution follows.
Replacement is reversible, epsilon signs are constant on same-coloring
families, and the Petersen model shows that a mate can leave the
three-perfect-matching expansion even on a 3-connected matching-covered
tight-cut-free support.  A successful continuation must therefore add one
of two genuinely new inputs: force an odd binomial circulation involving
several fibers, or control arbitrary locally-rainbow cubic occurrence
networks, including non-three-edge-colorable ones.  The ordinary
three-copy epsilon invariant does neither.

The dependency-free exact audit is
`computations/verify_triple_matching_rewrite.py`.  It checks the three
constant fibers, the complete two-term mixed cancellation, all Petersen
perfect matchings and odd complements, 3-connectivity, matching coverage,
and every nontrivial odd cut of the nineteen-edge support.
