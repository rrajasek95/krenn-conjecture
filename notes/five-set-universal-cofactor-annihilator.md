# Every ternary five-set has a target-active cofactor annihilator

## 1. Outcome

Let \(U\) be a set of five ternary sites and let


\[
                         h_u=H_{U\setminus\{u\}}(A)
       \in \bigotimes_{v\in U\setminus\{u\}}V_v             \tag{1}
\]

be the four-site matching tensor formed from the edges internal to \(U\).
Define the internal cofactor-slice space

\[
 {\cal S}_U=\sum_{u\in U}V_u\otimes h_u\subseteq V_U          \tag{2}
\]

(with every tensor placed in its named slots), and define

\[
 \begin{aligned}
 {\cal B}_U:V_U^*&\longrightarrow\bigoplus_{u\in U}V_u^*,\\
 ({\cal B}_U\beta)_u(z)&=\beta(z^{(u)}\otimes h_u),           \tag{3}\\
 \delta_U:V_U^*&\longrightarrow\mathbb C^3,\\
 \delta_U(\beta)&=\sum_{r=0}^2\beta(e_r^{\otimes U})e_r.    \tag{4}
 \end{aligned}
\]

The arbitrary-complex six-site theorem has the following useful dual
consequence.

**Theorem 1.1 (universal five-set annihilator).**  For every choice of the
ten endpoint-ordered \(3\times3\) edge tensors internal to \(U\),

\[
             \ker {\cal B}_U\not\subseteq\ker\delta_U.       \tag{5}
\]

Equivalently, there is always a functional \(\beta_U\in V_U^*\) such that

\[
 \beta_U(V_u\otimes h_u)=0\quad\hbox{for every }u\in U,
 \qquad
 \delta_U(\beta_U)\ne0.                                    \tag{6}
\]

This is not a generic statement and has no nondegeneracy hypothesis.  It
allows zero and arbitrary-rank blocks and holds over the full complex
field.

Now put the five-set on one shore of any odd cut
\(B=C\mathbin{\dot\cup}U\), and let \(F_1:V_U^*\to V_C\) be the
one-crossing flattening.  Every
functional in \(\ker {\cal B}_U\) kills the one-crossing tensor
cofactor-block by cofactor-block.  Consequently

\[
                    \boxed{\ \ker F_1\not\subseteq\ker\delta_U\ }
                                                                    \tag{7}
\]

for **every** ternary aggregate edge family and **every** five-set \(U\),
whether or not the full matching tensor is GHZ.  Thus the middle-arrow
condition proposed in
[`one-crossing-kernel-collapse.md`](one-crossing-kernel-collapse.md) can
never actually hold in the ternary problem.  A proof that full GHZ forces
it would already be a proof by contradiction, not a construction of a
realizable successful cut.

The exact finite audit
`computations/verify_five_set_universal_cofactor_annihilator.py` checks the
cofactor factorization, constructs an exact target-active annihilator for a
dense integral internal family, and verifies directly on an eight-site
family the sum over all 45 one-crossing matchings.  The universal
existence statement itself is a formal corollary of the proved six-site
theorem, not a finite experiment.

## 2. The one-crossing sector factors through the internal cofactors

For \(u\in U\), collect the entire response on the other shore and the
exposed site \(u\) into

\[
 K_u=\sum_{c\in C} H_{C\setminus\{c\}}(A)\otimes A_{cu}
            \in V_C\otimes V_u.                            \tag{8}
\]

Here the factors in each summand are restored to the named \(C\)-slots.
A matching with exactly one edge across \(C|U\) has a unique exposed site
\(u\in U\).  The other four sites of \(U\) are matched internally.  Hence

\[
                         T_1=\sum_{u\in U}K_u\otimes h_u.    \tag{9}
\]

Equivalently, if

\[
 \Gamma_{C,U}:\bigoplus_{u\in U}V_u^*\longrightarrow V_C,
 \qquad
 \Gamma_{C,U}((\lambda_u)_u)
    =\sum_u(\operatorname{id}_{V_C}\otimes\lambda_u)K_u,   \tag{10}
\]

then the flattening factors exactly as

\[
                            F_1=\Gamma_{C,U}{\cal B}_U.     \tag{11}
\]

In particular,

\[
                            \ker {\cal B}_U\subseteq\ker F_1. \tag{12}
\]

This inclusion is cofactor-wise: (6) annihilates the complete internal
four-site cofactor attached to each possible exposed \(u\).  It uses no
cancellation between different exposed sites or different shore responses,
and it uses no equation for the full matching tensor.  Cancellation among
the three internal perfect matchings comprising one \(h_u\) remains fully
allowed.

## 3. Dual proof from six-site impossibility

Let

\[
                       g_{U,r}=e_r^{\otimes U},\qquad
                       {\cal G}_U=\langle g_{U,0},g_{U,1},g_{U,2}\rangle.
                                                                    \tag{13}
\]

The transpose of (3) is the cofactor insertion map

\[
 \begin{aligned}
 {\cal B}_U^*:\bigoplus_{u\in U}V_u&\longrightarrow V_U,\\
 (z_u)_u&\longmapsto\sum_{u\in U}z_u^{(u)}\otimes h_u,    \tag{14}
 \end{aligned}
\]

whose image is exactly \({\cal S}_U\).

Assume contrary to (5) that
\(\ker {\cal B}_U\subseteq\ker\delta_U\).  Finite-dimensional duality
then gives

\[
                       \operatorname{im}\delta_U^*
                          \subseteq\operatorname{im}{\cal B}_U^*.
                                                                    \tag{15}
\]

Since \(\operatorname{im}\delta_U^*={\cal G}_U\), for each \(r\) there
are vectors \(z_{r,u}\in V_u\) satisfying

\[
                  g_{U,r}=\sum_{u\in U}z_{r,u}^{(u)}\otimes h_u.     \tag{16}
\]

Add one new site \(\star\), retain all ten old internal edge tensors, and
put

\[
                       Y_{\star u}=\sum_{r=0}^2
                              e_r^{(\star)}\otimes z_{r,u}.          \tag{17}
\]

Expansion at the new site and (16) give

\[
 \begin{aligned}
 H_{\{\star\}\cup U}(Y)
   &=\sum_{u\in U}Y_{\star u}\otimes h_u\\
   &=\sum_{r=0}^2e_r^{(\star)}\otimes g_{U,r}
     =\Delta_{6,3}.                                      \tag{18}
 \end{aligned}
\]

This contradicts
[`the arbitrary-complex six-site obstruction`](../proofs/six-site-arbitrary-complex-obstruction.md),
which permits completely arbitrary endpoint-ordered complex matrices,
including the matrices (17).  This proves Theorem 1.1.  Combining (5)
with (12) proves (7).  Notice that ternarity is essential: binary six-site
GHZ sources exist, and indeed some binary cuts in
`one-crossing-kernel-collapse.md` pass the old test.

There is a useful quantitative form.  Put

\[
                     W_U=\delta_U(\ker {\cal B}_U)\subseteq\mathbb C^3.
                                                                    \tag{19}
\]

Under the natural identification \(\mathbb C^3\cong{\cal G}_U\),

\[
                  \dim W_U=3-\dim({\cal G}_U\cap{\cal S}_U)\ge1.   \tag{20}
\]

Thus the theorem supplies a canonical nonzero *space* of target defects,
not merely one fortuitous functional.

There is also an immediate six-overlap consequence.  Fix any six-set
\(S\subseteq B\), put \(U_x=S\setminus\{x\}\), and for every site
\(c\notin U_x\) form the complete boundary response

\[
 R_c^{U_x}=\sum_{u\in U_x}A_{cu}\otimes
                 H_{U_x\setminus\{u\}}(A)\in V_c\otimes V_{U_x}.   \tag{21}
\]

Apply Theorem 1.1 separately to the six internal five-sets.  The resulting
functionals may be chosen simultaneously and satisfy

\[
 \boxed{
 (\operatorname{id}_{V_c}\otimes\beta_x)R_c^{U_x}=0
       \quad(c\notin U_x),
 \qquad \delta_{U_x}(\beta_x)\ne0
       \quad(x\in S).}                                    \tag{22}
\]

Indeed, the \(u\)-th summand of the first contraction is the edge map
\(A_{cu}\) applied to \(({\cal B}_{U_x}\beta_x)_u=0\).  Thus six
target-active annihilators of *all* one-crossing boundary responses are not
merely compatible on a special identity-block model: they exist for every
aggregate edge family.  This supersedes the proposed local incompatibility
step in
[the six-set Hessian pullback](six-set-one-crossing-hessian-pullback.md).
Only equations that couple the different high-crossing responses (or impose
relations among choices from the six defect spaces \(W_{U_x}\)) can add
information.  The special averaging identity in
[the six-set overlap jet](six-set-beta-overlap-jet.md) still adds
information because its explicitly chosen identity-block functionals obey
a further linear relation; such a relation is not supplied by Theorem 1.1.

## 4. What the full mixed equations now say

Suppose, for contradiction, that a larger ternary source satisfies

\[
                              H_B(A)=\Delta_{B,3}.          \tag{23}
\]

For every five-set \(U\), contract (23) by the whole space
\(\ker {\cal B}_U\).  Equation (9) vanishes there, so all constant and
mixed coefficient equations together give the exact restriction identity

\[
 \left.(T_3+T_5)^\flat\right|_{\ker {\cal B}_U}
       =\left.\iota_C\delta_U\right|_{\ker {\cal B}_U},    \qquad
 \iota_C(e_r)=e_r^{\otimes C}.                            \tag{24}
\]

The right side is nonzero by Theorem 1.1.  Hence every five-cut is forced
to route a nonzero diagonal target quotient entirely through matchings
having three or five crossing edges.  This is the surviving content of the
middle-arrow route.

In the square-zero notation of
[`failed-five-set-high-sector-factorization.md`](failed-five-set-high-sector-factorization.md),
condition (6) is stronger than merely \(F_1\beta=0\): it gives

\[
                              p_1(\beta)=0                 \tag{25}
\]

before multiplication by any power of \(q_C\).  If
\(|C|=2s+1\ge5), choose \(\beta\in\ker{\cal B}_U\) with
\(b=\delta_U(\beta)\ne0\).  Then (24) becomes

\[
 \Delta_C(b)=\frac{q_C^{s-2}}{(s-2)!}
       \left(\frac{q_Cp_3(\beta)}{s-1}+p_5(\beta)\right),
 \qquad p_1(\beta)=0.                                    \tag{26}
\]

For \(|C|=3\), only the three-crossing sector remains and (24) is simply
\(\Delta_C(b)=p_3(\beta)\).  The standalone routing examples in the
failed-five-set note already allow \(p_1=0\), so (26) alone is still not a
contradiction.  Its new force is simultaneity: the nonzero defect space
\(W_U\) exists for every one of the overlapping five-sets and is defined
from their shared internal edge factors.

## 5. Concrete next attack

The successful-cut search should be retired.  A nonvacuous continuation
must use (24) simultaneously on overlapping five-sets.  The smallest
sharp test is order eight:

1. For every \(U\in\binom{B}{5}\), retain the full space
   \(K_U=\ker{\cal B}_U\) and the nonzero quotient map
   \(K_U\twoheadrightarrow W_U\), rather than selecting one \(\beta_U\).
2. Since the complementary shore has size three, (24) has only the
   three-cross sector.  Group it by its unique internal edge in \(U\) and
   its bijection from the other three \(U\)-vertices to \(C\).
3. Compare the resulting maps for adjacent five-sets
   \(U,U'\) with \(|U\cap U'|=4\).  Their cofactor maps share the complete
   four-set tensor \(H_{U\cap U'}\), while their three-cross responses
   reuse the same aggregate edge entries.  The concrete target is a
   division-free overlap identity forcing the images \(W_U,W_{U'}\) into
   incompatible coordinate subspaces.
4. Any proposed overlap lemma should first be tested against exact
   non-GHZ edge families satisfying all one-cut restriction identities
   under consideration.  A one-cut common-power or abstract matching-term
   model is already known to be too weak; shared aggregate edge products
   across at least two adjacent cuts are indispensable.

If this adjacent-cut theorem can be made uniform under adding matched
pairs to \(C\), it supplies the genuinely global step still missing from
the route registry.  Without such compatibility, (24) is only another
necessary reformulation of the full tensor equation.
