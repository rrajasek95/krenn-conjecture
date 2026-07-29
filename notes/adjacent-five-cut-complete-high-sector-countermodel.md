# Two adjacent complete high-sector identities coexist at order eight

## 1. Outcome

Let

\[
 B=S\mathbin{\dot\cup}R,
 \qquad |S|=6,\qquad R=\{p,q\}.
\]

For \(z\in S\), put

\[
 U_z=S\setminus\{z\},\qquad C_z=R\cup\{z\}.
\]

At order eight the three-crossing tensor for the odd cut
\(C_z\mid U_z\) is exactly the part of the two-crossing tensor for
\(R\mid S\) whose two crossing sites avoid \(z\).  This gives a simple
division-free replacement for a common lifted cofactor-kernel element.
If \(\beta_z\in K_{U_z}\) satisfies the complete high-sector restriction
identity and \(\lambda_z\in V_z^*\), then the lifted covectors
\(\eta_z=\lambda_z\otimes\beta_z\) obey

\[
 \left(\sum_z\eta_z\otimes\operatorname{id}_R\right)T_2
   =\sum_{r=0}^2\left(
      \sum_z\lambda_z(e_r)\beta_z(e_r^{\otimes U_z})
     \right)e_r^{\otimes R}.                              \tag{1}
\]

Thus target noncancellation in the displayed three-vector is already a
sufficient compatibility condition.  No division and no common element of
the lifted kernels is required.

The condition is genuinely weaker, but it is not yet an obstruction.  An
explicit zero-one eight-site edge family below satisfies the **complete**
restriction identities

\[
 \left.(T_{3,z})^\flat\right|_{K_{U_z}}
    =\left.\iota_{C_z}\delta_{U_z}\right|_{K_{U_z}}       \tag{2}
\]

on the two adjacent cuts \(z=2,3\).  Their defect spaces are respectively
\(\langle e_1\rangle\) and \(\langle e_2\rangle\), and the two explicit
witnesses combine through (1) to

\[
 (e_{1^S}^*+e_{2^S}^*)\mathbin{\lrcorner_S}T_2
                  =e_1^{\otimes R}+e_2^{\otimes R}.      \tag{3}
\]

Consequently two adjacent complete high-crossing quotient maps, even with
a target-active compatible sum, do not contradict the matching equations
by themselves.  A successful continuation must use at least a third cut,
an additional relation among the quotient maps, or mixed equations not
contained in (2).

## 2. Exact adjacent-cut sector formulas

For \(\{a,b\}\subset S\), let \(T_2^{ab}\) be the part of the even-cut
two-crossing tensor in which \(a,b\) are the two sites of \(S\) matched to
\(R\).  With endpoint slots restored to their named sites,

\[
 T_2^{ab}=\left(A_{pa}\otimes A_{qb}
                    +A_{pb}\otimes A_{qa}\right)
                         \otimes H_{S\setminus\{a,b\}}(A). \tag{4}
\]

Also

\[
 T_0=A_{pq}\otimes H_S(A),\qquad
 T_2=\sum_{\{a,b\}\subset S}T_2^{ab}.                   \tag{5}
\]

For the odd cut \(C_z\mid U_z\), a zero-crossing matching for
\(R\mid S\) acquires the one crossing edge incident to \(z\).  A
two-crossing matching has one crossing relative to \(C_z\mid U_z\) when
\(z\) is one of its two \(S\)-crossing sites, and three crossings when it
is not.  Hence, atom by atom and with arbitrary aggregate edge tensors,

\[
 \boxed{
 \begin{aligned}
 T_{1,z}&=T_0+\sum_{a\in S\setminus\{z\}}T_2^{za},\\
 T_{3,z}&=\sum_{\{a,b\}\subset U_z}T_2^{ab}.
 \end{aligned}}                                         \tag{6}
\]

The second formula may also be grouped by the unique edge left internal to
the five-shore.  For \(\{u,v\}\subset U_z\), put

\[
 P_z^{uv}=\sum_{\pi:C_z\mathbin{\simto}
                         U_z\setminus\{u,v\}}
             \bigotimes_{c\in C_z}A_{c,\pi(c)}.          \tag{7}
\]

Then the complete, uncapped three-crossing response is

\[
 \boxed{
 T_{3,z}=\sum_{\{u,v\}\subset U_z}A_{uv}\otimes P_z^{uv}.} \tag{8}
\]

Equations (4), (6), and (8) are the same tensor after regrouping its
matching atoms.  Formula (8) makes explicit that adjacent cuts reuse both
the four-site internal cofactors and the actual aggregate edge entries;
no abstract matching-term replacement has been made.

## 3. A summed-lift compatibility lemma

For a five-set \(U\), write

\[
 {\cal S}_U=\sum_{u\in U}V_u\otimes H_{U\setminus\{u\}}(A),
 \qquad K_U={\cal S}_U^\perp.                             \tag{9}
\]

The one-crossing flattening on \(C_z\mid U_z\) factors through the
cofactor insertion space in (9), so every \(\beta\in K_{U_z}\) kills it.
Moreover expansion at \(z\) gives

\[
 H_S(A)=\sum_{u\in U_z}A_{zu}\otimes
                    H_{U_z\setminus\{u\}}(A),           \tag{10}
\]

and hence \((\operatorname{id}_{V_z}\otimes\beta)H_S=0\).

**Lemma 3.1 (summed high-sector lifts).**  Let \(Z\subseteq S\).  Suppose
that for every \(z\in Z\) the complete restriction identity

\[
 (\operatorname{id}_{C_z}\otimes\beta)T_{3,z}
   =\sum_{r=0}^2\beta(e_r^{\otimes U_z})
                         e_r^{\otimes C_z}
             \qquad(\beta\in K_{U_z})                  \tag{11}
\]

holds.  Choose arbitrary \(\beta_z\in K_{U_z}\) and
\(\lambda_z\in V_z^*\), and set

\[
 \eta_z=\lambda_z\otimes\beta_z,\qquad
 \eta=\sum_{z\in Z}\eta_z,
 \qquad
 d_r=\sum_{z\in Z}\lambda_z(e_r)
                  \beta_z(e_r^{\otimes U_z}).           \tag{12}
\]

Then

\[
 (\eta\otimes\operatorname{id}_R)T_0=0,
 \qquad
 (\eta\otimes\operatorname{id}_R)T_2
                  =\sum_{r=0}^2d_r e_r^{\otimes R}.     \tag{13}
\]

In particular, \(d\ne0\) gives a target-active contraction of \(T_2\).

**Proof.**  Fix \(z\).  Equation (10) says that \(\eta_z\) kills
\(T_0=A_{pq}\otimes H_S\).  Since \(\beta_z\) kills \(T_{1,z}\), the
first identity in (6) then gives

\[
 \eta_z\mathbin{\lrcorner_S}
       \sum_{a\ne z}T_2^{za}=0.                          \tag{14}
\]

Contracting (11) by \(\lambda_z\) in the \(z\)-slot and using the second
identity in (6) gives

\[
 \eta_z\mathbin{\lrcorner_S}
       \sum_{\{a,b\}\subset U_z}T_2^{ab}
   =\sum_r\lambda_z(e_r)\beta_z(e_r^{\otimes U_z})
                         e_r^{\otimes R}.                \tag{15}
\]

The two sums in (14)--(15) partition \(T_2\).  Add over \(z\).  This
proves (13) without selecting a pivot or dividing by an edge entry.
\(\square\)

The only compatibility demanded by this lemma is the noncancellation
\(d\ne0\).  It is strictly weaker than asking for one target-active
functional in \(\bigcap_z(V_z^*\otimes K_{U_z})\).

## 4. An exact eight-site two-cut model

Take

\[
 S=\{0,1,2,3,4,5\},\qquad R=\{6,7\}.
\]

Let \(E_{rr}=e_r\otimes e_r\).  Put \(A_{uv}=E_{rr}\) on the edges of
the following three one-factors and put every omitted block equal to zero:

\[
\begin{array}{c|c}
r&M_r\\ \hline
0&01,23,45,67\\
1&02,14,36,57\\
2&04,13,27,56.
\end{array}                                               \tag{16}
\]

The supported graph has exactly five decorated perfect matchings.  Direct
expansion gives, in site order \(0,1,\ldots,7\),

\[
 H_B= e_{00000000}+e_{11111111}+e_{22222222}
           +e_{00210012}+e_{12120000}.                  \tag{17}
\]

Thus this is not a GHZ source.  The two extra matchings are respectively

\[
 \{01,45,36,27\},\qquad \{02,13,45,67\}.                \tag{18}
\]

Nevertheless they lie entirely in the one-crossing sector for each of the
two adjacent cuts below, and their five-shore rows are genuine cofactor
insertions.

### 4.1 The cut \(U_2=\{0,1,3,4,5\}\)

Use the site order \((0,1,3,4,5)\) on \(U_2\).  Its only nonzero
four-site cofactors are

\[
 H_{1345}=e_{2200},\qquad
 H_{0145}=e_{0000},\qquad
 H_{0134}=e_{2222}.                                     \tag{19}
\]

Consequently \({\cal S}_{U_2}\) is the nine-dimensional coordinate span

\[
 \begin{aligned}
 &e_t^{(0)}e_2^{(1)}e_2^{(3)}e_0^{(4)}e_0^{(5)},\\
 &e_0^{(0)}e_0^{(1)}e_t^{(3)}e_0^{(4)}e_0^{(5)},\\
 &e_2^{(0)}e_2^{(1)}e_2^{(3)}e_2^{(4)}e_t^{(5)},
 \end{aligned}
 \qquad t=0,1,2.                                        \tag{20}
\]

It contains \(e_{0^{U_2}}\) and \(e_{2^{U_2}}\), but not
\(e_{1^{U_2}}\).  Hence

\[
 \delta_{U_2}(K_{U_2})=\langle e_1\rangle,
 \qquad \beta_2=e_{1^{U_2}}^*\in K_{U_2}.               \tag{21}
\]

Relative to \(C_2=(2,6,7)\), the residual in (17) has the exact
cofactor-row decomposition

\[
 H_B-\Delta_{B,3}
  =e_{212}^{C_2}\otimes
       \bigl(e_1^{(3)}\otimes H_{0145}\bigr)
   +e_{100}^{C_2}\otimes
       \bigl(e_1^{(0)}\otimes H_{1345}\bigr).           \tag{22}
\]

Both brackets belong to \({\cal S}_{U_2}\).  More explicitly, sector
classification gives

\[
                         T_{3,2}=e_{1^B}.                \tag{23}
\]

For every \(\beta\in K_{U_2}\), equations (20)--(23) therefore give

\[
 (\operatorname{id}_{C_2}\otimes\beta)T_{3,2}
       =\beta(e_{1^{U_2}})e_{1^{C_2}}
       =(\iota_{C_2}\delta_{U_2})(\beta).               \tag{24}
\]

This is the full map identity, not only its value at \(\beta_2\).

### 4.2 The adjacent cut \(U_3=\{0,1,2,4,5\}\)

In site order \((0,1,2,4,5)\), the nonzero four-site cofactors are

\[
 H_{0245}=e_{1100},\qquad
 H_{0145}=e_{0000},\qquad
 H_{0124}=e_{1111}.                                     \tag{25}
\]

Thus \({\cal S}_{U_3}\) is spanned by

\[
 \begin{aligned}
 &e_1^{(0)}e_t^{(1)}e_1^{(2)}e_0^{(4)}e_0^{(5)},\\
 &e_0^{(0)}e_0^{(1)}e_t^{(2)}e_0^{(4)}e_0^{(5)},\\
 &e_1^{(0)}e_1^{(1)}e_1^{(2)}e_1^{(4)}e_t^{(5)},
 \end{aligned}
 \qquad t=0,1,2.                                        \tag{26}
\]

It contains the color-zero and color-one constants and misses the
color-two constant.  Therefore

\[
 \delta_{U_3}(K_{U_3})=\langle e_2\rangle,
 \qquad \beta_3=e_{2^{U_3}}^*\in K_{U_3}.               \tag{27}
\]

For \(C_3=(3,6,7)\),

\[
 H_B-\Delta_{B,3}
  =e_{112}^{C_3}\otimes
       \bigl(e_2^{(2)}\otimes H_{0145}\bigr)
   +e_{200}^{C_3}\otimes
       \bigl(e_2^{(1)}\otimes H_{0245}\bigr),           \tag{28}
\]

and sector classification gives

\[
                         T_{3,3}=e_{2^B}.                \tag{29}
\]

Hence, for every \(\beta\in K_{U_3}\),

\[
 (\operatorname{id}_{C_3}\otimes\beta)T_{3,3}
       =\beta(e_{2^{U_3}})e_{2^{C_3}}
       =(\iota_{C_3}\delta_{U_3})(\beta).               \tag{30}
\]

The sets \(U_2,U_3\) share the complete four-set \(\{0,1,4,5\}\), and
all tensors in (22), (28), and (30) come from the one common edge family
(16).

The replacement is strict in this same model.  If

\[
 L_2=V_2^*\otimes K_{U_2},\qquad
 L_3=V_3^*\otimes K_{U_3},
\]

then (21) and (27) give

\[
 \delta_S(L_2)\subseteq\langle e_1\rangle,
 \qquad
 \delta_S(L_3)\subseteq\langle e_2\rangle.
\]

Therefore \(L_2\cap L_3\subseteq\ker\delta_S\): there is no
target-active common lifted-kernel element, even though the two complete
high-sector maps coexist.

## 5. The compatible target-active sum

Take

\[
 \lambda_2=e_1^*,\qquad \lambda_3=e_2^*,\qquad
 \eta_2=e_{1^S}^*,\qquad \eta_3=e_{2^S}^*.              \tag{31}
\]

Equations (21), (27), and Lemma 3.1 give

\[
 ((\eta_2+\eta_3)\otimes\operatorname{id}_R)T_0=0,
 \qquad
 ((\eta_2+\eta_3)\otimes\operatorname{id}_R)T_2
                   =e_1^{\otimes R}+e_2^{\otimes R}.    \tag{32}
\]

This realizes the requested weaker compatibility mechanism exactly.  It
is strictly beyond common lifted-kernel intersection because the preceding
paragraph proves that intersection target-zero.  It also locates the new
mechanism's limit: (32) is perfectly consistent with both complete
high-sector identities, while the two mixed coefficients in (17) remain.
The next obstruction must couple more of the full GHZ coefficient system
than two adjacent restrictions of the form (2).

## 6. Exact audit

[`verify_adjacent_five_cut_complete_high_sector_countermodel.py`](../computations/verify_adjacent_five_cut_complete_high_sector_countermodel.py)
enumerates all decorated perfect matchings, reconstructs (4), (6), and
(8), checks every four-site cofactor and both nine-dimensional insertion
spaces, verifies (22) and (28) coefficientwise, tests (24) and (30) on a
basis of each complete kernel, and checks the target-active sum (32) over
the integers.
