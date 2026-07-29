# Target flattenings force many doubly injective pair stars

## 1. Outcome

Let \(B\) have even size \(N\), let \(V_u\cong\mathbb C^3\), and let
arbitrary endpoint-ordered aggregate blocks \(A_{uv}\in V_u\otimes V_v\)
satisfy

\[
                       H_B(A)=\Delta_{B,3}.              \tag{1}
\]

For distinct sites \(v,u\), delete \(\{v,u\}\) and consider the
aggregate star at endpoint \(u\):

\[
 \sigma_u^{(v)}:V_u^*\longrightarrow
      \bigoplus_{x\notin\{u,v\}}V_x,\qquad
 \alpha\longmapsto
      \bigoplus_{x\notin\{u,v\}}
          (\alpha\otimes\operatorname{id})A_{ux}.       \tag{2}
\]

Then

\[
 \boxed{\text{for each fixed }u,\text{ at most three }v
        \text{ make }\sigma_u^{(v)}\text{ noninjective}.} \tag{3}
\]

Consequently the graph of unordered pairs for which both endpoint stars
are injective has at least

\[
          \boxed{\binom N2-3N=\frac{N(N-7)}2}            \tag{4}
\]

edges, and it has a vertex of degree at least \(N-7\). Thus a doubly
injective pair exists at every even order \(N\ge8\), with a
common-endpoint fan of sizes at least \(1,3,5,7\) at
\(N=8,10,12,14\), respectively.

The bad-pair graph is uniformly \(4\)-degenerate. Consequently the good
graph contains a clique of size at least \(\lceil N/5\rceil\); in
particular, every \(N\ge26\) source has six sites whose every physical pair
is doubly aggregate-injective.

This improves the earlier \(N\ge14\) existence threshold obtained from
the full-nine target-incidence theorem. The results contain different
information: this argument controls the two deleted endpoint stars, while
full-nine incidence additionally leaves at least \(N-8\) target-full
internal sites after every pair deletion.

The word **aggregate** is essential. Equation (3) does not say that one
block has rank three or that every colour row of every block is nonzero.
It supplies a stronger uniform input to the Hessian route, not the missing
Hessian or clean-cap conclusion.

## 2. Endpoint support and the target flattening

For an oriented block define its complete mode-\(u\) support

\[
 L_{u\leftarrow x}
  =\operatorname{im}\bigl(V_x^*\longrightarrow V_u,
       \ \beta\longmapsto
       (\operatorname{id}\otimes\beta)A_{ux}\bigr),    \tag{5}
\]

and put \(T_u=\sum_{x\ne u}L_{u\leftarrow x}\). Expanding the
matching tensor at \(u\) gives

\[
 H_B(A)=\sum_{x\ne u}
      A_{ux}\otimes H_{B\setminus\{u,x\}}(A),          \tag{6}
\]

with tensor slots restored to physical order. Every summand, flattened
with the \(u\)-mode on the left, has image in
\(L_{u\leftarrow x}\). Therefore

\[
        \operatorname{im}\operatorname{Flat}_u(H_B(A))
                           \subseteq T_u.                \tag{7}
\]

The corresponding flattening of the target is

\[
 \sum_{i=0}^2e_i^{(u)}\otimes
       e_i^{\otimes(B\setminus\{u\})}.                 \tag{8}
\]

Its three right factors are linearly independent, so its left image is
all of \(V_u\). Hence

\[
                              T_u=V_u.                    \tag{9}
\]

This uses the complete tensor identity. No matching term, parallel
source, or block entry has been selected from a cancelling sum.

## 3. The essential-subspace lemma

**Lemma 3.1.** Let a finite family of subspaces \((L_x)_{x\in I}\)
span a \(d\)-dimensional space \(V\). Call \(x\) essential if
\(\sum_{y\ne x}L_y\ne V\). There are at most \(d\) essential
indices.

**Proof.** For every essential \(x\), choose \(\phi_x\in V^*\)
which annihilates \(\sum_{y\ne x}L_y\) but not \(L_x\), and choose
\(z_x\in L_x\) with \(\phi_x(z_x)\ne0\). For \(y\ne x\),
the space \(L_x\) is among the summands annihilated by \(\phi_y\), so
\(\phi_y(z_x)=0\). Evaluating a relation among the \(\phi_y\)'s on
each \(z_x\) proves that these covectors are independent. Thus their
number is at most \(\dim V^*=d\). \(\square\)

If equality holds, the \(d\) covectors form a basis of \(V^*\). Every
nonessential \(L_y\) is annihilated by all of them and is zero. Each
essential \(L_x\) is annihilated by the other \(d-1\) covectors, so it
is the corresponding nonzero coordinate line. The essential subspaces
are therefore independent lines.

## 4. Star kernels and the pair count

For fixed \(u\), put

\[
              S_u^{(v)}=\sum_{x\notin\{u,v\}}
                              L_{u\leftarrow x}.          \tag{10}
\]

Because the codomain in (2) is a direct sum,

\[
                  \ker\sigma_u^{(v)}
                       =\operatorname{Ann}S_u^{(v)}.      \tag{11}
\]

Thus the star is injective exactly when \(S_u^{(v)}=V_u\). Apply
Lemma 3.1 to the neighbor supports, using (9) and \(d=3\). At most
three deleted neighbors make (10) proper, proving (3), including zero
blocks.

There are at most \(3N\) deficient directed pairs \((v,u)\). Every
unordered pair which is not doubly injective has a deficient orientation.
Assign it to either one; distinct unordered pairs give distinct directed
pairs. Hence there are at most \(3N\) bad unordered pairs. Subtracting
from \(\binom N2\) proves (4), and the average degree proves the fan
bound.

There is a sharper hereditary consequence. Let \({\cal B}\) be the bad-pair
graph, where essentiality is always computed in the full incident family,
and consider \({\cal B}[C]\). If one endpoint has three globally essential
neighbors, the equality case of Lemma 3.1 makes its entire aggregate support
degree three; hence its degree in \({\cal B}\) is at most three. Therefore
an induced bad subgraph of minimum degree at least five can contain no such
endpoint. Every remaining endpoint has at most two globally essential
neighbors. Assign each bad edge to one endpoint witnessing its deficiency.
Then \(|E({\cal B}[C])|\le2|C|\), contradicting minimum degree at least
five. Thus \({\cal B}\) is \(4\)-degenerate and \(5\)-colorable. A largest
color class is a clique in the good graph of size at least
\(\lceil N/5\rceil\).

## 5. The sharp three-essential endpoint

If a site \(u\) has three essential neighbors, the equality case of
Lemma 3.1 says that all other incident blocks are zero and the three
surviving blocks have one-dimensional mode-\(u\) support. The aggregate
support degree of \(u\) is exactly three and all three blocks have rank
one. The cubic-vertex lemma in
[the prism-plus-one-edge obstruction](../proofs/prism-plus-one-edge-obstruction.md)
then applies at the orders \(N\ge8\) under consideration and upgrades them,
using the full target equation, to three nonzero
same-colour coordinate cells with distinct colours at \(u\).

With two essential neighbors every other endpoint support lies in the
common kernel of two independent covectors, hence one line. With one
essential neighbor every other support lies in one plane. These exact
flags are concrete strata for a mixed-equation continuation.

## 6. Quantifiers and remaining gate

The proof is field-linear and uses no positivity or conjugation. It
allows arbitrary complex entries, zero blocks, endpoint asymmetry, and
parallel decorated sources after aggregation. For a palette of size at
least three, project functorially to any three palette colours; the
projected matching tensor is \(\Delta_{B,3}\), and zeroed cells remain
allowed.

The result does not complete the conjecture. On a gauge-rigid connected
internal chart, the registered Hessian theorems still leave localized zero
rows or row support at most two. A successful continuation must propagate
the essential-star flags across overlapping good pairs, exclude the
extra-kernel/disconnected escapes, or derive a clean cap from the different
source-variable factorizations of the shared mixed residuals.

## 7. Exact audit

The standalone checker
[verify_target_flattening_essential_star_pair_bound.py](../computations/verify_target_flattening_essential_star_pair_bound.py)

* verifies mode-flattening containment for exact rational asymmetric
  blocks at four and six sites;
* exhausts all multisets of subspaces of \(\mathbb F_2^3\) through seven
  neighbors and checks the essential bound and equality structure;
* checks the star-kernel/support-span equivalence on exact rational
  families, including zero blocks; and
* audits (4), its fan degrees, the good-clique threshold, and the even-order
  thresholds.

The finite checks audit the displayed algebra and extremal ledgers. Lemma
3.1 and the flattening argument give the uniform characteristic-zero
theorem.
