# Total-sector odd-shore reduction to six sites

## Outcome

Let \(B=C\sqcup U\), where `C` is odd and `|U|=5`.  Group the
matching tensor according to the number of edges crossing the cut:

\[
                 H_B(A)=T_1+T_{\geq3},\qquad
                 T_{\geq3}=T_3+T_5.                       \tag{1}
\]

There is an exact six-site reduction if the three constant tensors on `C`
miss the **left Schmidt space of the single total tensor** `T_{>=3}`.  This
is strictly weaker than asking them to miss the sum of the left Schmidt
spaces of the individual high-crossing matching terms: every cancellation
inside `T_3+T_5` is retained.  It is nevertheless stronger than necessary.
The sharper kernel-only criterion and its exact strictness audit are in
[`one-crossing-kernel-collapse.md`](one-crossing-kernel-collapse.md).

The condition is not forced by the final flattening rank alone.  More
substantively, it is not forced by the known active rank-one anchors, even
when all three constant coefficients are exactly normalized and one may try
all choices of the five-set `U`.  An exact eight-vertex integer model below
fails the condition for every one of the `56` five-sets.  That model has
nonzero mixed coefficients, so it does not refute the conjecture.  It shows
that any theorem forcing the new separation must use the simultaneous mixed
coefficient cancellations, not merely anchor incidence or constant fibres.

## 1. The cancellation-sensitive local quotient

Write

\[
 V_C=\bigotimes_{v\in C}V_v,\qquad
 g_{C,r}=e_r^{\otimes C},\qquad
 \mathcal G_C=\operatorname{span}\{g_{C,0},g_{C,1},g_{C,2}\}. \tag{2}
\]

For a tensor `T in V_C tensor V_U`, let

\[
 \operatorname{LS}_C(T)
 =\{(\operatorname{id}_{V_C}\otimes\beta)T:\beta\in V_U^*\}
 \subseteq V_C                                                   \tag{3}
\]

be its left Schmidt space.  Because `|C|` and `|U|` are odd, every perfect
matching crosses the cut an odd number of times.  Since `|U|=5`, the only
possibilities are `1,3,5`, giving (1).

**Lemma 1.1 (total-sector quotient criterion).**  Put

\[
                         \mathcal W_C
              =\operatorname{LS}_C(T_{\geq3}).             \tag{4}
\]

There is a linear map `Phi:V_C -> C^3` such that

\[
 (\Phi\otimes\operatorname{id}_{V_U})T_{\geq3}=0,
 \qquad \Phi(g_{C,r})=e_r\quad(r=0,1,2)                    \tag{5}
\]

if and only if

\[
                  \boxed{\mathcal G_C\cap\mathcal W_C=0}. \tag{6}
\]

**Proof.**  The first equation in (5) is equivalent to
`W_C subseteq ker(Phi)`.  If (5) holds, a vector in the intersection (6)
is sent both to zero and, by the second equation, to the same nontrivial
linear combination of `e_0,e_1,e_2`; hence the intersection is zero.

Conversely, (6) says that the three classes of `g_{C,r}` are independent in
`V_C/W_C`.  Define a map on their span in the quotient by sending these
three classes to `e_r`, extend it linearly to the whole quotient, and compose
with the quotient map.  The resulting `Phi` satisfies (5).  `QED`

If `t_M` denotes an individual matching term, then

\[
 \operatorname{LS}_C\left(\sum_{M:\,|M\cap\delta(C)|\geq3}t_M\right)
 \subseteq
 \sum_{M:\,|M\cap\delta(C)|\geq3}\operatorname{LS}_C(t_M), \tag{7}
\]

and the inclusion can be strict because matching terms can cancel.  Thus
Lemma 1.1 genuinely strengthens the termwise odd-bag criterion.

## 2. The surviving one-crossing sector is a six-site matching tensor

Introduce one aggregate vertex `star` for `C`.  For `u in U`, define the
boundary tensor

\[
 K_u=\sum_{c\in C}\ \sum_{N\in\operatorname{PM}(C\setminus\{c\})}
 \left(\bigotimes_{xy\in N}A_{xy}\right)\otimes A_{cu}
 \ \in V_C\otimes V_u,                                    \tag{8}
\]

where all endpoint slots are restored to their natural order.  Given a map
`Phi` from Lemma 1.1, set

\[
       Y_{\star u}=(\Phi\otimes\operatorname{id}_{V_u})K_u,
       \qquad Y_{uv}=A_{uv}\quad(u,v\in U).                \tag{9}
\]

Every `Y` is an arbitrary element of the relevant tensor product, hence a
legitimate aggregate edge matrix.

**Theorem 2.1 (one-shore six-site reduction).**  If

\[
                       H_B(A)=\Delta_{B,3}                 \tag{10}
\]

and (6) holds for some five-set `U`, then

\[
                       H_{\{\star\}\cup U}(Y)=\Delta_{6,3}. \tag{11}
\]

**Proof.**  A matching crossing `C|U` exactly once has a unique crossing
edge `cu`.  Its remaining edges split uniquely into a perfect matching of
`C\setminus{c}` and one of `U\setminus{u}`.  Consequently the star expansion
of the left side of (11) gives the exact identity

\[
 H_{\{\star\}\cup U}(Y)
   =(\Phi\otimes\operatorname{id}_{V_U})T_1.               \tag{12}
\]

Lemma 1.1 kills the *total* tensor `T_{>=3}`, without requiring its
individual matching terms to vanish.  Applying the same map to (10) gives

\[
 (\Phi\otimes\operatorname{id})(T_1+T_{\geq3})
 =\sum_{r=0}^2\Phi(g_{C,r})\otimes e_r^{\otimes U}
 =\Delta_{6,3}.                                             \tag{13}
\]

Equations (12)--(13) prove (11).  `QED`

There is a useful formulation involving only the one-crossing sector.  Let

\[
 F_1:V_U^*\longrightarrow V_C,qquad
 F_h:V_U^*\longrightarrow V_C,qquad
 D:V_U^*\longrightarrow\mathcal G_C                    \tag{14}
\]

be the flattening maps of `T_1`, `T_{>=3}`, and `Delta`, respectively, and
let `pi:V_C -> V_C/G_C` be the quotient.  Exactness says
`D=F_1+F_h`, hence

\[
 \pi F_h=-\pi F_1,qquad
 K_U:=\ker(\pi F_1)=\ker(\pi F_h),qquad
 \mathcal G_C\cap\operatorname{im}F_h=F_h(K_U).           \tag{15}
\]

The last equality is exact in both directions: `F_h(beta)` is diagonal if
and only if `beta in K_U`.  Therefore (6) is equivalently

\[
                       (D-F_1)(K_U)=0.                     \tag{16}
\]

The one-crossing sector has much more structure than an arbitrary flattening.
Put

\[
 P_c=H_{C\setminus\{c\}}(A),\qquad
 R_c=\sum_{u\in U}A_{cu}\otimes H_{U\setminus\{u\}}(A).
                                                                    \tag{17}
\]

With natural slot ordering,

\[
 T_1=\sum_{c\in C}P_c\otimes R_c,qquad
 \operatorname{im}F_1\subseteq
 \sum_{c\in C}V_c\otimes P_c,qquad
 \operatorname{rank}F_1\leq3|C|.                           \tag{18}
\]

Hence `K_U` in (15) is normally large; the quotient criterion is not a
generic injectivity statement.  Instead it is the exact compatibility
`(D-F_1)(K_U)=0`.  A condition first recorded here as merely necessary is

\[
                         \ker F_1\subseteq\ker D,           \tag{19}
\]

because `F_h(beta)=D(beta)` on `ker F_1`.  Equivalently, each of the three
constant-color right functionals defining `D` must lie in the row space of
the aggregate one-crossing flattening.

The sharper observation in
[`one-crossing-kernel-collapse.md`](one-crossing-kernel-collapse.md) is that
(19) is already **sufficient for the six-site reduction**, without the
stronger quotient compatibility (16).  If `delta:V_U^* -> C^3` sends
`beta` to `sum_r beta(e_r^tensor U)e_r`, then `ker D=ker delta`, so (19)
makes `Phi(F_1 beta)=delta(beta)` well defined on `im F_1`.  Extending
`Phi` to `V_C` gives `(Phi tensor id)T_1=Delta_(6,3)`, and the star response
(8)--(12) closes directly.  No high-sector annihilation is needed.

The established six-site obstruction therefore gives a sharp necessary
condition on every hypothetical larger realization.

**Corollary 2.2 (simultaneous contamination).**  If an exact realization
exists on `|B|>6`, then for **every** five-set `U subset B`, with
`C=B\setminus U`,

\[
 \mathcal G_C\cap\operatorname{LS}_C(T_3^{C|U}+T_5^{C|U})\ne0. \tag{20}
\]

Thus varying `U` does not give a free choice: a putative counterexample must
satisfy the exceptional intersection (20) simultaneously on every five-set.
This simultaneous family is potentially useful, but proving that one of the
intersections vanishes is already enough to prove the conjecture.

## 3. What the exact output tensor alone does not say

Across `C|U`, write \(\gamma_r=e_r^{\otimes U}\).  The linear-algebra
decomposition

\[
 \Delta_{B,3}
 =\underbrace{g_{C,1}\otimes\gamma_1+g_{C,2}\otimes\gamma_2}_{T_1}
  +\underbrace{g_{C,0}\otimes\gamma_0}_{T_{\geq3}}         \tag{21}
\]

has the correct total tensor and has
`g_{C,0} in LS_C(T_{>=3})`.  Arbitrary cancelling tensors may be added to
the two summands.  This is not asserted to arise from one common edge
family; it isolates the precise missing information.  Flattening rank three
of the final GHZ tensor constrains `T_1+T_{>=3}`, not the two summands.

The remaining hope would be that the matching parametrization together with
the forced active rank-one anchors makes (6) true for at least one choice of
`U`.  The next exact model rules out any argument using just those anchor and
constant-fibre consequences.

## 4. An eight-vertex all-five-set anchor countermodel

Use vertices `0,...,7` and the following five edge-disjoint one-factors:

\[
\begin{aligned}
 P_0&=\{07,16,25,34\},& P_1&=\{02,17,36,45\},\\
 Q_0&=\{04,13,27,56\},& Q_1&=\{06,15,24,37\},\\
 Q_2&=\{01,26,35,47\}.&&                                  \tag{22}
\end{aligned}
\]

Let

\[
 S=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix},
 \qquad
 S^2=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}. \tag{23}
\]

Put `S` on the edges of `P_0`, `S^2` on the edges of `P_1`, and `E_ii`
on every edge of `Q_i`; all other matrices are zero.

This source has three exact properties.

1. At every vertex and for every color `i`, the incident `Q_i` edge is the
   same-color coordinate rank-one tensor \(e_i\otimes e_i\).  Its complementary
   six-site matching tensor is nonzero, so it is an active anchor of exactly
   the kind forced by the one-slice theorem.
2. Since `S` and `S^2` have zero diagonal, the only nonzero matching in the
   constant-color-`i` fibre is `Q_i`.  Hence all three constant coefficients
   are exactly one.
3. The source is not exact GHZ: for example, the mixed coefficient at
   `00000122` is one.

For every choice of a five-set `U`, let `C` be its three-vertex complement.
Here `T_5=0`, so the total high sector is simply `T_3`.  Exact integer row
reduction gives the following complete audit; the second coordinate is

\[
 d_C=\dim\left(\mathcal G_C\cap\operatorname{LS}_C(T_3)\right). \tag{24}
\]

\[
\begin{array}{c|c|c}
 \operatorname{rank}_C(T_3)&d_C&\text{number of three-sets }C\\ \hline
 27&3&50\\
 23&3&3\\
 24&3&1\\
 25&3&1\\
 21&2&1
\end{array}                                                  \tag{25}
\]

The six non-full-rank cuts are

\[
\begin{array}{c|c|c}
C&\operatorname{rank}_C(T_3)&d_C\\ \hline
017&23&3\\027&23&3\\136&24&3\\167&25&3\\
245&21&2\\345&23&3.
\end{array}                                                  \tag{26}
\]

For `C=245`, the two vectors `g_{C,0}` and `g_{C,2}` themselves lie in the
left Schmidt space; for every other cut the whole `G_C` lies in it.  Thus

\[
 \mathcal G_C\cap\operatorname{LS}_C(T_{\geq3})\ne0
 \quad\text{for all }\binom83=56\text{ choices of }C.       \tag{27}
\]

`computations/verify_total_sector_six_reduction.py` reconstructs the source,
checks the factorization, active anchors, normalized constant coefficients,
and surviving mixed coefficient, and audits all `56` flattenings.  For the
`50` full-rank cuts it finds a nonzero `27 by 27` minor modulo `1000003`,
which certifies full rank over the rationals.  It performs exact rational row
reduction on the other six cuts and verifies (25)--(26) and the two explicit
diagonal directions for `C=245`.

## 5. Remaining exact bottleneck

Theorem 2.1 is a genuine improvement over the six-odd-bag criterion: one
needs to separate `G_C` only from the Schmidt space after all high-sector
cancellations, and only one nonsingleton bag is involved.  The countermodel
shows, however, that none of the following forces such a separation:

* choosing the five exposed vertices after seeing the source;
* three active same-color coordinate anchors at every vertex;
* invertible non-anchor edges; or
* exact normalization of all three constant coefficients.

The unused hypothesis in that model is precisely the simultaneous vanishing
of every mixed coefficient.  A successful continuation must convert those
vanishing equations into the failure of at least one contamination condition
(20), or else combine the nonzero intersections for many overlapping
five-sets into a contradiction.  No implication of either kind is proved
here.
