# Aggregate star injection stops before the Hessian hypotheses

## 1. Outcome

The target-incidence invariant gives more aggregate-injective pairs than
was previously recorded. If an exact ternary source has \(N\geq14\)
physical sites, then at least

\[
                     \boxed{\frac{N(N-13)}2}                 \tag{1}
\]

unordered physical pairs have injective aggregate star maps at both
endpoints. In particular, some vertex is the common endpoint of at least
\(N-13\) such pairs. Thus at \(N=14\) there is at least one pair, while at
the next even order \(N=16\) there is already a three-chart fan.

This does not by itself cross any of the local hypotheses in
[source-hessian-bipartite-rankdrop.md](source-hessian-bipartite-rankdrop.md).
Using the full nine equations gives the following exact frontier. On a
both-injective pair chart whose internal Hessian is gauge-rigid:

* if the internal rank-three graph is connected, some individual colour
  row of one deleted star is zero at an internal site;
* if that graph is also nonbipartite, every one of the six global colour
  rows is nonzero but supported on at most two internal sites. Hence each
  deleted star is identically zero on at least \(N-8\) internal sites.

Aggregate injection therefore converts a *global* zero row into an
impossibility, but it does not convert localized missing rows into
blockwise row-fullness. It also says nothing that forces the internal
rank-three graph to be connected.

The obstruction is sharp at the structural level. Section 6 gives an
exact rational fourteen-site edge family for which all \(91\) physical
pairs have aggregate-injective stars at both endpoints, yet every deleted
pair has a disconnected internal rank-three graph and at least two
internal blocks with two literal zero rows at each deleted endpoint. The
three constant coefficients are normalized to exactly one, endpoint order
is retained, and the pair-chart exchange identity holds exactly.

The family is deliberately **not** a ternary GHZ source: it has a positive
mixed coefficient. Consequently it is a countermodel to an inference from
aggregate injection, rank/support data, and exchange reindexing alone, not
to a consequence which genuinely uses vanishing of the full nine target
residuals. A physical countermodel retaining those residual equations
would already be a counterexample to Krenn's conjecture. The remaining
bridge must therefore be a new elimination consequence of their different
source-variable factorizations; merely imposing a second pair chart adds
no equation.

There is a separate exact warning for the clean-cap alternative. The
binary six-site source in Section 5 satisfies its complete target equation
and has aggregate-injective stars at both endpoints of the selected pair,
but that pair has a nonzero higher correction for every active covector
which retains both target colours. Hence aggregate rank plus the full top
equations does not force a clean cap by a palette-independent argument. A
ternary clean-cap bridge would have to use the third-colour equations
essentially.

## 2. Directed deficiencies give many good pairs

For distinct physical sites \(r,u\), use the notation of
[uniform-full-nine-target-incidence-invariant.md](uniform-full-nine-target-incidence-invariant.md):

\[
 S_u^{(r)}=
 \sum_{v\notin\{r,u\}}\operatorname{im}_u(A_{uv})\subseteq V_u. \tag{2}
\]

Call the directed pair \((r,u)\) deficient when \(S_u^{(r)}\ne V_u\).
The target-incidence double count proves that, for each fixed \(r\), at
most six sites \(u\) are deficient. There are consequently at most
\(6N\) directed deficiencies in total.

An unordered pair \(\{r,u\}\) fails to have injective aggregate stars at
both endpoints only if at least one of \((r,u)\) and \((u,r)\) is deficient.
Assign such a bad unordered pair to either one of its directed deficient
orientations. Distinct unordered pairs give distinct directed pairs, so
this gives

\[
 \#\{\hbox{both-injective pairs}\}
 \geq {N\choose2}-6N
 =\frac{N(N-13)}2,                                      \tag{3}
\]

which proves (1). The graph formed by the both-injective pairs has average
degree at least \(N-13\), so one vertex has degree at least \(N-13\).

No genericity or support selection enters this count. The spaces in (2)
are spans of the complete aggregated endpoint blocks, so parallel sources,
zero cells, asymmetric endpoint decorations, and arbitrary complex
cancellation have already been retained.

## 3. What the full nine equations add on a good chart

Fix a both-injective pair \(p,q\), put
\(W=B\setminus\{p,q\}\), and orient every incident block toward its named
deleted endpoint. Write

\[
 p_c=\sum_{i\in W}p_{c,i},\qquad
 s_d=\sum_{i\in W}s_{d,i}.                              \tag{4}
\]

The two aggregate star maps are injective exactly when the triples
\((p_0,p_1,p_2)\) and \((s_0,s_1,s_2)\) are linearly independent in
\(\bigoplus_{i\in W}V_i\). In particular, none of the six global rows is
zero. This is strictly weaker than the blockwise row-full condition

\[
                    p_{c,i}\ne0,\quad s_{d,i}\ne0
        \qquad(c,d=0,1,2,\ i\in W).                     \tag{5}
\]

Let \(q_0\) be the internal quadratic and put

\[
 Q=q_0^{[|W|/2]},\qquad F=q_0^{[|W|/2-1]}.
\]

The complete pair contraction is

\[
                 a_{cd}Q+p_cs_dF=\delta_{cd}X_c.        \tag{6}
\]

It retains the direct block, both endpoint orders, all zero blocks, and all
complex cancellation.

**Proposition 3.1 (injective-star/Hessian frontier).** Assume (6), assume
the source Hessian of \(q_0\) has only its vertex-gauge kernel, and let
\(G_3(q_0)\) be the internal graph of rank-three physical blocks.

1. If \(G_3(q_0)\) is connected, (5) is false.
2. If \(G_3(q_0)\) is connected and nonbipartite, then

   \[
       1\leq |\operatorname{supp}_s(p_c)|\leq2,
       \qquad
       1\leq |\operatorname{supp}_s(s_d)|\leq2          \tag{7}
   \]

   for all \(c,d\). Each deleted endpoint is therefore joined by a
   nonzero star block to at most six internal sites and is identically zero
   toward at least

   \[
                         |W|-6=N-8                       \tag{8}
   \]

   internal sites.

**Proof.** The connected bipartite rank-drop theorem applies to (6)
without any entry localization. If all vectors in (5) were nonzero, its
six-row synchronization would put the nine responses in a two-dimensional
output span, contradicting the rank-three diagonal target. This proves
the first assertion, whether the connected graph is bipartite or not.

On the connected nonbipartite chart, the source-derivative Hessian theorem
uses the six off-diagonal equations in (6), gauge rigidity, and the odd
cycle to prove the upper bounds in (7). Aggregate injectivity says that
the global rows in (4) are independent, so none is zero; this gives the
lower bounds. The union of the three row supports at one endpoint has
size at most six, proving (8). No term of (6) was selected before or after
cancellation. \(\square\)

Thus every both-injective pair in a hypothetical source lies on one of the
following exact escape strata:

1. an extra internal Hessian kernel;
2. a disconnected internal rank-three graph;
3. a connected bipartite graph with a localized missing row; or
4. the nonbipartite sparse-row pattern (7).

This is useful sharpening, but none of the four alternatives is a clean
cap or an all-even descent.

## 4. Pair-chart exchange supplies a syzygy, not another system

For a third physical site \(u\), the pair charts \((p,q)\) and \((p,u)\)
obey the exact exchange identity

\[
 \iota_{u,\alpha}\iota_{q,d}\iota_{p,c}H_B(A)
 =
 \iota_{q,d}\iota_{u,\alpha}\iota_{p,c}H_B(A).          \tag{9}
\]

After expanding either side into its direct-edge and two-star cases, (9)
is precisely the pair-chart exchange formula. It is polynomial over
\(\mathbb Z\) in the endpoint-ordered aggregate cells. Hence it survives
all specializations, zero blocks, and cancellations.

More importantly, a complete nine-row tensor system in one chart already
contains every coefficient of \(H_B(A)-\Delta_{B,3}\). A second complete
chart contains the same scalar residual polynomials with their coordinates
reindexed. Therefore the many pairs in (1) cannot be counted as
independent copies of the target equations.

The charts can still be useful because they factor the same residuals in
different source variables. A valid bridge must eliminate through those
factorizations. For example, it could prove that a localized missing row
on one good chart forces an extra Hessian direction or a clean cap on
another. Equation (9) alone does not do this.

## 5. Clean-cap injection already fails on the exact binary boundary

Take the rational six-site realization of the binary diagonal tensor from
[pair-covector-selection-obstruction.md](pair-covector-selection-obstruction.md),
and select its physical pair \(1,3\). On the four internal sites
\(2,4,5,6\), the star from endpoint \(1\) has two linearly independent
global rows: its colour-zero row reaches site \(2\), while its colour-one
row also reaches sites \(5,6\). The star from endpoint \(3\) has its two
independent rows on sites \(4\) and \(2\). Thus both aggregate maps have
the full binary rank two.

Write a completely general pair covector as

\[
                         K=\sum_{a,b=0}^1k_{ab}e_a^*e_b^*.
\]

For this pair the direct scalar and the two target scalars are

\[
                s(K)=-k_{10},\qquad
                \kappa_0(K)=k_{00},\qquad
                \kappa_1(K)=k_{11}.                     \tag{10}
\]

The exact four-site higher correction has the coefficient

\[
 [e_1^{(2)}e_0^{(4)}e_1^{(5)}e_1^{(6)}]H_4(R_K)
       =k_{10}k_{11}=-s(K)\kappa_1(K).                  \tag{11}
\]

Consequently \(s(K)\kappa_0(K)\kappa_1(K)\ne0\) makes the correction
nonzero. No nondegenerate covector cleans this active pair, even though
the original source satisfies every binary coefficient equation and both
aggregate stars are injective. This does not disprove a genuinely ternary
selection theorem; it proves that the missing input cannot be aggregate
rank, pair exchange, or the two-colour faces alone.

## 6. A fourteen-site exact structural countermodel

Partition the sites into two seven-sets

\[
 L=\{0,1,\ldots,6\},\qquad R=\{7,8,\ldots,13\}.          \tag{12}
\]

Put a cycle on each shore, with indices read modulo seven, and place the
same invertible matrix

\[
 D=\begin{pmatrix}
 1&1&1\\
 1&2&4\\
 1&3&9
 \end{pmatrix},\qquad \det D=2,                          \tag{13}
\]

on every cycle edge. The stored matrix is oriented from the numerically
smaller endpoint to the larger one; contraction from the other endpoint
uses \(D^{\mathsf T}\).

For \(c=0,1,2\), take the cross-shore one-factor

\[
 M_c=\bigl\{\,\{i,\,7+(i+c\bmod7)\}:0\leq i<7\,\bigr\}. \tag{14}
\]

and put \(E_{cc}\) on every edge of \(M_c\). The three one-factors are
edge-disjoint and disjoint from the two cycles. All other physical blocks
are zero.

For a constant colour \(c\), only the two cycles and \(M_c\) contribute.
If \(d=D_{cc}\), their exact matching polynomial is

\[
                         P(d)=1+7d^2+14d^4+7d^6.         \tag{15}
\]

At \(d=1,2,9\), this gives respectively

\[
                         29,\qquad701,\qquad3{,}812{,}509. \tag{16}
\]

Apply at site \(0\) the invertible diagonal map with entries equal to the
reciprocals in (16). Every perfect matching uses site \(0\), so the three
constant coefficients become exactly one. This local normalization does
not change any matrix rank or zero row.

Now delete any pair \(p,q\).

* Each endpoint has two cycle neighbors. At most one was deleted, so its
  star into the remaining twelve sites contains an invertible \(D\) or
  \(D^{\mathsf T}\) block. Both aggregate star maps are injective.
* Each endpoint has three distinct cross-anchor neighbors. At least two
  remain internal. Each corresponding \(E_{cc}\) block has two literal
  zero endpoint rows. Thus neither star is blockwise row-full.
* The rank-three graph consists only of the two shore cycles with \(p,q\)
  removed. Both shores retain at least five vertices, and there is no
  rank-three cross edge. The internal rank-three graph is disconnected.

These assertions hold simultaneously for all \({14\choose2}=91\) pairs,
not after independently choosing witnesses. They retain zero blocks and
endpoint reversal literally.

Finally, all nonzero entries are positive rational numbers. A supported
mixed matching therefore gives a strictly positive mixed coefficient, so
the family is not the ternary target. This last failure is essential: it
locates exactly the information which aggregate incidence and exchange do
not use.

## 7. Exact audit and next gate

The standalone checker
[verify_injective_star_hessian_bridge_frontier.py](../computations/verify_injective_star_hessian_bridge_frontier.py)

* verifies the directed count (1);
* independently expands all binary coefficients of the six-site source,
  checks rank two of both selected aggregate stars, and reconstructs the
  exact defect monomial (11);
* enumerates all \(13!!=135{,}135\) perfect matchings and checks (15)--(16)
  and the exact pure normalization;
* checks all \(91\) deleted pairs for two rank-three aggregate star maps,
  localized zero rows at both endpoints, and disconnected internal
  rank-three graph;
* exhibits and evaluates a positive mixed residual; and
* audits in two overlapping charts the universal partition into
  \(10{,}395\) direct-edge and \(124{,}740\) two-star matchings.

The concrete next step is not another incidence count. It is one of the
following source-specific eliminations:

1. propagate a localized missing row across the graph of both-injective
   pairs using the *factorized* forms of the shared residuals;
2. show that the extra-Hessian-kernel and disconnected-rank-three escapes
   cannot cover all of the at least \(N(N-13)/2\) good pairs; or
3. derive a cap-saturation or clean-cap condition from the common internal
   powers before passing to aggregate endpoint spans.

Any such step must use vanishing of mixed target coefficients. The exact
countermodel proves that aggregate ranks, zero masks, constant
normalization, and exchange reindexing do not contain that information.
