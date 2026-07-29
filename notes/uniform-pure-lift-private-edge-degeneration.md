# Private edges close the full pure-lift common-power branch

## 1. Result

Let \(U\) be a six-set. At every site \(u\), let \(V_u\) contain three
distinguished independent vectors

\[
                         e_0^{(u)},e_1^{(u)},e_2^{(u)}.
\]

For a pair \(P\subset U\), put

\[
 E_c(P)=\bigotimes_{u\notin P}e_c^{(u)},
 \qquad X_c=\bigotimes_{u\in U}e_c^{(u)}.              \tag{1}
\]

Consider the completely arbitrary pure-lift multiplier

\[
 F=\sum_{c=0}^2\ \sum_{P\in\binom U2}\lambda_{cP}E_c(P),
 \qquad \lambda_{cP}\in\mathbb C.                     \tag{2}
\]

If several descriptions contribute to the same \(E_c(P)\), first combine
them into the aggregate coefficient \(\lambda_{cP}\); a cancelled aggregate
is zero. Thus (2) retains repeated sources and all complex cancellation.
Let

\[
 p_0,p_1,p_2,s_0,s_1,s_2\in\bigoplus_{u\in U}V_u
\]

be arbitrary multi-site rows, and impose all nine products

\[
                         p_i s_jF=\delta_{ij}X_i.       \tag{3}
\]

**Theorem 1.1 (uniform pure-lift obstruction).** There is no quadratic
\(q\) in the site-square-zero algebra for which

\[
                         q^{[2]}=F,\qquad q^{[3]}=0.    \tag{4}
\]

This closes all \(45\) pure coefficients at once. It includes arbitrary
support sizes, arbitrary nonzero aggregate weights, every repeated-pair
pattern, arbitrary endpoint-ordered blocks of \(q\), arbitrary local
dimensions, zero components, and arbitrary complex cancellation. It is not
a finite multiplicity-profile computation.

The proof has two short steps. First, (3) forces every colour to have a
missing pair used by no other colour. Second, a local algebra projection
keeps exactly one such private term per colour. Its image would be a common
power with three distinct pure lifts, contradicting the distinct-missing-
pair theorem.

## 2. Literal responses force a private pair in every colour

Work in

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                      \tag{5}
\]

For \(P=\{a,b\}\), multiplication by \(E_d(P)\) retains exactly the two
endpoint orders

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}
              +s_{j,a}\otimes p_{i,b}\in V_a\otimes V_b. \tag{6}
\]

Extend the three displayed vectors at each site to a basis, and let
\(e_c^*\) denote the corresponding coordinate covector. Define

\[
 \beta_c(P)=
 (e_c^*\otimes e_c^*)B_{cc}(P).                        \tag{7}
\]

Response spaces belonging to different base colours have disjoint
coordinate-word supports. Indeed, for \(c\ne d\) and pairs \(P,Q\), at
least two sites lie outside \(P\cup Q\); a word from the first response
space is fixed to \(e_c\) there, while a word from the second is fixed to
\(e_d\). Hence the coefficient of \(X_c\) in the \((c,c)\) equation of
(3) is

\[
                    \sum_P\lambda_{cP}\beta_c(P)=1.    \tag{8}
\]

No other base colour contributes to this word.

Now suppose that \(\lambda_{dP}\ne0\) for some \(d\ne c\). In the
colour-\(d\) part of the same \((c,c)\) response, inspect the word

\[
 Y_{c,d,P}=
 \left(\bigotimes_{u\in P}e_c^{(u)}\right)
 \otimes
 \left(\bigotimes_{u\notin P}e_d^{(u)}\right).         \tag{9}
\]

This word can arise from no missing pair other than \(P\): its two sites
different from the base colour \(d\) determine the missing pair. It can
also arise from no other base colour. This remains true for arbitrary
multi-site and transverse components of the rows, since selecting the
literal word (9) applies the coordinate covector \(e_c^*\) at both missing
sites. Its coefficient in (3) is therefore

\[
                         \lambda_{dP}\beta_c(P)=0,
\]

and hence

\[
 \beta_c(P)=0
 \quad\text{whenever }P\text{ is active in a colour }d\ne c.       \tag{10}
\]

Let

\[
 H_c=\{P:\lambda_{cP}\ne0\},\qquad
 H_c^{\mathrm{priv}}=H_c\setminus\bigcup_{d\ne c}H_d.  \tag{11}
\]

Equations (8)--(10) give the stronger identity

\[
              \sum_{P\in H_c^{\mathrm{priv}}}
                    \lambda_{cP}\beta_c(P)=1.           \tag{12}
\]

Consequently \(H_c^{\mathrm{priv}}\ne\varnothing\) for every \(c\).
Choose

\[
                         P_c\in H_c^{\mathrm{priv}}.    \tag{13}
\]

The three pairs \(P_0,P_1,P_2\) are automatically distinct. Notice that
this argument keeps both endpoint orders in (6), and it does not infer
termwise vanishing from an arbitrary zero sum: the term in (10) is isolated
by the literal coordinate word (9).

## 3. A local algebra projection selects the private pairs

At each site \(u\), define a linear map \(\pi_u:V_u\to V_u\) by

\[
 \pi_u(e_c^{(u)})=
 \begin{cases}
   0,&u\in P_c,\\
   e_c^{(u)},&u\notin P_c,
 \end{cases}                                           \tag{14}
\]

and let \(\pi_u\) fix a chosen complement of the three target axes. Since
the product of any two elements of \(V_u\) is zero, every linear map on
\(V_u\) extends, together with \(1\mapsto1\), to a unital algebra
endomorphism of \(\mathbb C\oplus V_u\). Their tensor product is therefore
an algebra endomorphism

\[
                 \Pi:\mathcal R_U\longrightarrow\mathcal R_U.    \tag{15}
\]

For a colour-\(c\) lift, \(\Pi(E_c(P))\) survives precisely when none of
the killed axes occurs in its four-site support. Equivalently,

\[
 \Pi(E_c(P))\ne0
 \quad\Longleftrightarrow\quad P_c\subseteq P
 \quad\Longleftrightarrow\quad P=P_c,                 \tag{16}
\]

where the last equivalence uses that both sets are pairs. Thus, with
\(q_0=\Pi(q)\), functoriality of matching powers gives directly

\[
 q_0^{[2]}=\Pi(F)=
     \lambda_{0P_0}E_0(P_0)
    +\lambda_{1P_1}E_1(P_1)
    +\lambda_{2P_2}E_2(P_2),
 \qquad q_0^{[3]}=\Pi(q^{[3]})=0.                     \tag{17}
\]

The three displayed coefficients are nonzero and their missing pairs are
distinct. But
[the distinct-missing-pair common-power obstruction](distinct-missing-pair-common-power-obstruction.md)
proves, for arbitrary endpoint-ordered tensor blocks and arbitrary local
dimensions, that (17) has no solution over \(\mathbb C\). This contradiction
proves Theorem 1.1.

Only the original rows are used to obtain the private pairs in (13). The
endomorphism is then applied solely to the power equations (4); no row
limit, target-preserving normalization, orbit closure, or genericity
argument is involved. Equivalently, \(\Pi\) is the \(t=0\) member of the
nonnegative filtration used in Section 6.

## 4. Repeated pairs and the sharp \(K_4\) power solution

The repeated-pair issue is real before the products are imposed. Fix a
pair \(P=\{4,5\}\), and on the complementary four sites use the three
one-factors

\[
 \{01,23\},\qquad \{02,13\},\qquad \{03,12\}           \tag{20}
\]

in colours \(0,1,2\), respectively, with unit weights. Let \(q\) be the
sum of the resulting six pure edge tensors. Edges from different
one-factors always meet, while the two edges in each one-factor are
disjoint. Hence exactly

\[
 q^{[2]}=E_0(P)+E_1(P)+E_2(P),\qquad q^{[3]}=0.         \tag{21}
\]

Thus no power-only argument can forbid repeated supports. In (21),
however, every \(H_c\) is the same singleton \(\{P\}\), so no colour has a
private pair. Equations (8)--(10) give the direct contradiction that the
same \(\beta_c(P)\) must both contribute to \(X_c\) and vanish in either
other colour response.

More generally, repeated \(K_4\)-type pieces may coexist formally with
additional pure lifts. The proof does not try to split them off. The
nine products first supply one private pair in each colour, and the
projection (14)--(16) erases every repeated and nonselected term at once. This
is the promised uniform treatment of all repeated-pair strata.

## 5. Scope and exact audit

The theorem closes the full pure span

\[
                 \operatorname{span}\{E_c(P):
                   0\le c\le2,\ P\in\tbinom U2\},      \tag{22}
\]

which has dimension \(45\). It does not treat a four-site coefficient of
\(F\) that is itself non-pure, such as a mixed coordinate word or a sum of
general rank-one tensors in moving local directions. That non-pure branch
remains a separate descent problem.

The standalone checker
[verify_uniform_pure_lift_private_edge_degeneration.py](../computations/verify_uniform_pure_lift_private_edge_degeneration.py)
audits all coordinate-word separation claims, all \(2{,}730\) ordered
choices of distinct private pairs, the projection criterion (16), the five
support-graph types of the selected triple, functorial matching weights,
and the exact repeated-pair \(K_4\) witness.

## 6. The exact non-pure jet left by the associated filtration

Replace each zero in the projection (14) by multiplication by a parameter
\(t\); call the resulting local-axis automorphism \(T_t\) for \(t\ne0\).
This filtration still makes sense for a general, non-pure degree-four tensor
once three distinct pairs \(P_c\) have been selected by some other argument.
Purity was essential above for deriving the private pairs and for identifying
the weight-zero image, not for the filtration itself.

Write the exact finite expansions

\[
 T_t(F)=\sum_{r=0}^4t^rF^{(r)},\qquad
 T_t(p_i)=p_i^{(0)}+tp_i^{(1)},\qquad
 T_t(s_j)=s_j^{(0)}+ts_j^{(1)}.                       \tag{23}
\]

Because \(T_t(X_i)=t^2X_i\), coefficient comparison in the transformed
product equation gives

\[
 p_i^{(0)}s_j^{(0)}F^{(0)}=0,                         \tag{24}
\]

\[
 (p_i^{(1)}s_j^{(0)}+p_i^{(0)}s_j^{(1)})F^{(0)}
       +p_i^{(0)}s_j^{(0)}F^{(1)}=0,                  \tag{25}
\]

and

\[
\begin{aligned}
 p_i^{(1)}s_j^{(1)}F^{(0)}
 &+(p_i^{(1)}s_j^{(0)}+p_i^{(0)}s_j^{(1)})F^{(1)}\\
 &+p_i^{(0)}s_j^{(0)}F^{(2)}
   =\delta_{ij}X_i.                                   \tag{26}
\end{aligned}
\]

Every coefficient of order greater than two is zero. The transformed
quadratic similarly has degrees zero, one, and two, so \(q_t^{[2]}=T_t(F)\)
and \(q_t^{[3]}=0\) give a parallel finite power-jet hierarchy.

For non-pure \(F\), the tensor \(F^{(0)}\) can contain mixed coordinate
words, so the three-pure-lift conclusion (17) no longer follows and the
present theorem cannot be invoked.
Equations (24)--(26), organized by the five graph shapes of the selected
pairs, are a concrete next frontier rather than a claimed closure.
