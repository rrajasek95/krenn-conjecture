# Ternary reciprocal cap selection: the exact port-open obstruction and structural boundary

## Outcome

Let `p,q` be a literal reciprocal coordinate pair in a hypothetical exact
ternary source, let `W` be the residual sites, and let

\[
 p_0,p_1,p_2,\qquad s_0,s_1,s_2\in {\cal A}_1(W)
\]

be its two endpoint-star triples in the site-square-zero algebra.  For a
completely general cap (K=(k_{ij})\in\operatorname {Mat}_3), put

\[
 s(K)=\langle K,A_{pq}\rangle,qquad
 R_K=\sum_{i,j}k_{ij}p_i s_j,qquad
 \kappa_i(K)=k_{ii}.                                    \tag{1}
\]

The **ternary cap-selection variety** is

\[
 {\cal C}_{p,q}=\left\{K: R_K^{[2]}=0,\quad
 s(K)k_{00}k_{11}k_{22}\ne0\right\}.                   \tag{2}
\]

It is the right sufficient clean-cap locus: in characteristic zero,
(R_K^{[2]}=0) implies (R_K^2=0), hence every divided power
(R_K^{[j]}) with (j\ge2) vanishes.  The hafnian Schur update therefore
has no higher insertion tail at any even order.

Two exact conclusions hold.

1. **The six-distinct-port chart is empty.**  If the three (p_i) and the
   three (s_j) are literal nonzero one-site ports on six distinct residual
   sites, the nine coefficients of (R_K^{[2]}) are exactly the nine
   (2\times2) permanents of (K).  Their ideal, saturated by
   (k_{00}k_{11}k_{22}), is the unit ideal over every field of
   characteristic different from two.  Adding the reciprocal open condition
   (s(K)\ne0) cannot restore a point.
2. **Any clean cap forces a four-port degeneration.**  For arbitrary
   multisite stars, modulo products which repeat a (p)-label or an
   (s)-label, the equation (R_K^{[2]}=0) is a nontrivial linear relation
   among the nine four-port tensors
   (p_i p_k s_j s_l), (i<k,j<l).  Thus a clean active cap can exist only
   where the source-specific four-port product map has a kernel.  On a
   unique-fibre support stratum this says that the supported edges of (R_K)
   are pairwise intersecting, hence are contained in one star or one
   triangle.

This is the sharp theorem-level answer supplied by the local reciprocal
packet.  The third colour does not automatically create a clean cap: on the
port-open locus it makes the quadratic selection ideal empty.  It can only
help through a physical port collision or a source-specific four-site
cancellation.  Those are exactly the structural degenerations that must be
transported to the adjacent-cubic or curved-overlap branches.

The theorem does **not** prove that every reciprocal full-nine source lies on
the six-port-open locus, nor that every four-port kernel already gives an
adjacent cubic pair.  That conversion is the remaining uniform statement.

## The source-faithful cap packet

The full-nine pair equations have the exact source-labelled responses

\[
 r_{ij}=p_i s_j,qquad
 (A_{pq})_{ij}Q^{[h]}+r_{ij}Q^{[h-1]}=\delta_{ij}X_i.    \tag{3}
\]

Contracting the endpoint slots by (K) gives (1).  If
(A_{pq}=\lambda E_{ba}), then

\[
                         s(K)=\lambda k_{ba}.             \tag{4}
\]

Nothing in the definition of (R_K) treats the nine responses as abstract
replacement edges: they are the literal products of the two endpoint stars,
with same-site products killed before any coefficient is taken.  Thus (2)
is source-faithful and retains endpoint order.

The smallest fully separated ternary packet has six residual sites.  Put
(p_i) on site (P_i), (s_j) on site (S_j), with all six sites distinct.
Then (R_K) is the weighted complete bipartite port graph

\[
                         P_iS_j\quad\hbox{with weight }k_{ij}. \tag{5}
\]

For (i<k) and (j<l), the coefficient of the four-site word on
(P_i,P_k,S_j,S_l) is

\[
 [P_iP_kS_jS_l]R_K^{[2]}
       =k_{ij}k_{kl}+k_{il}k_{kj}.                       \tag{6}
\]

These are all nine (2\times2) permanents.  Distinct row/column pairs use
different physical four-sets, so no cross-coefficient cancellation is being
assumed away.

## Integral active-saturation certificate

Write

\[
 K=\begin{pmatrix}a&b&c\\d&e&f\\g&h&i\end{pmatrix}
\]

and select four permanent equations

\[
 F_{01}=ae+bd,quad G_1=af+cd,quad G_2=bf+ce,quad
 F_{02}=ai+cg.                                           \tag{7}
\]

They obey

\[
                    aG_2-bG_1+cF_{01}=2ace.              \tag{8}
\]

Consequently

\[
 ei\left(2aeF_{02}-g(aG_2-bG_1+cF_{01})\right)
                         =2(aei)^2.                       \tag{9}
\]

Thus ((aei)^2) belongs to the permanent ideal over characteristic not two.
After localizing the three diagonal cap values (a,e,i), the ideal is the
unit ideal.  The reciprocal scalar (\lambda k_{ba}) in (4) is an additional
factor in the activity polynomial and does not affect the contradiction.

This unnormalized certificate is stronger than choosing one numerical
completion matrix.  It decides the complete nine-variable cap variety on the
six-port-open chart.

## The exact structural boundary

For general multisite stars, let ({\cal A}(W)) be the site-square-zero
algebra and put

\[
 D=\operatorname {span}\{p_i^2s_js_l,\ p_ip_ks_j^2\}
                         \subset {\cal A}_4(W).           \tag{10}
\]

Modulo (D), direct expansion gives

\[
 R_K^{[2]}\equiv
 \sum_{i<k,\ j<l}
 (k_{ij}k_{kl}+k_{il}k_{kj}),p_ip_ks_js_l.              \tag{11}
\]

Define the four-port product map

\[
 \Theta:\mathbb C^9\longrightarrow {\cal A}_4(W)/D,qquad
 e_{ik;jl}\longmapsto[p_ip_ks_js_l].                    \tag{12}
\]

If (Theta) is injective, (11) forces all nine permanents to vanish, and
(9) excludes every cap with three nonzero diagonal values.  Therefore

\[
 \boxed{\ {\cal C}_{p,q}\ne\varnothing
          \quad\Longrightarrow\quad \ker\Theta\ne0.\ } \tag{13}
\]

More precisely, the permanent vector of the selected (K) is a nonzero
element of (ker\Theta); it cannot be zero by (9).  Equation (13) is not a
dimension heuristic.  It is the exact source-specific cancellation which a
positive reciprocal descent must exhibit.

There is a useful support form.  Suppose every decorated four-site word in
(R_K^{[2]}) has at most one supported perfect matching.  Then a pair of
disjoint supported (R_K)-edges would contribute a nonzero coefficient over
an integral domain.  Hence the edge support is pairwise intersecting.  Every
pairwise-intersecting simple edge family is contained in a star or triangle:
choose two meeting edges (ab,ac); any edge meeting both either contains
(a) or is (bc).  This gives the finite boundary

\[
             \text{star support}\quad\text{or}\quad
             \text{triangle support}\quad\text{or}\quad
             \text{a genuine four-site cancellation circuit}.             \tag{14}
\]

The literal six-port chart has none of these degenerations: repeated-label
products vanish and its nine four-port tensors occupy distinct four-sets.

## Proof-facing kernel alternatives

For use in the uniform proof, (13)--(14) should be read as the following
necessary trichotomy.  It is exhaustive at the source-faithful support level,
but only the first two cases presently close.

| four-port behaviour | exact consequence | status in the existing proof |
|---|---|---|
| The selected (R_K)-support is pairwise intersecting. | Its physical edge support is contained in a star or triangle, so (R_K^{[2]}=0) termwise and every higher insertion vanishes. | **Closed if activity holds:** the exact hafnian Schur update in `reciprocal-coordinate-hafnian-schur-counterguard.md` then gives the (N\mapsto N-2) source directly. No extra cubic hypothesis is needed. |
| A four-site fibre has the two opposite coordinate-port pairings with the signed two-colour cancellation. | This is the special four-port circuit used to add the two missing target colours. | **Closed in its literal cubic stratum:** `adjacent-cubic-pair-exact-descent.md` proves the cancellation in all port-collision patterns and constructs the smaller source. |
| A four-site fibre has a genuinely ternary exchange, or a distinct-label product cancels against the repeated-label span (D). | The permanent vector of (K) is a nonzero element of (ker\Theta); this is the source-specific circuit which evades the port-open unit. | **Open:** `n8-oriented-rankone-curvature-full-nine-frontier.md` can select a curved active rank-one overlap, but does not construct this (K) or prove the required four-port relation. The permanent-null no-go rules out replacing it by a universal (3\times3) coefficient identity. |

The support statement behind the table is elementary and source-faithful.
For any fixed decorated four-site word, there are only three possible
perfect matchings.  If exactly one is live, (R_K^{[2]}=0) is impossible.
If none is live, there is no condition.  If at least two are live, their
coefficient sum is a literal four-site cancellation circuit.  Hence the
only way to avoid both an intersecting support and a unique-matching
contradiction is the last row of the table.

This also states the remaining theorem without ambiguity.  It is **not**
enough to prove merely that (ker\Theta\ne0): the kernel must meet the
permanent image of an actual cap (K) with
(s(K)k_{00}k_{11}k_{22}\ne0).  The missing reciprocal lemma is therefore

\[
 \text{full-nine reciprocal provenance}
 \Longrightarrow
 \left\{
 \begin{array}{l}
 \text{an active star/triangle cap, or}\\
 \text{the literal two-colour cubic circuit, or}\\
 \text{an active ternary point of }\ker\Theta.
 \end{array}\right.                                      \tag{15}
\]

The first two outputs descend by committed theorems.  Only the last arrow is
new mathematics.  In particular, the curved-overlap branch is a possible
input to (15), not a claimed closure of it.

## Reproduction

```text
python3 computations/verify_reciprocal_ternary_cap_selection_variety.py
python3 -O computations/verify_reciprocal_ternary_cap_selection_variety.py
```

The checker independently enumerates (R_K^{[2]}), verifies all nine
permanent coefficients and the integral certificate (8)--(9), tests all
nine possible reciprocal coordinate positions, and exhausts all simple
six-site edge supports for the star/triangle classification.
