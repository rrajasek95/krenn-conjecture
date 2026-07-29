# The generic and permutation-aligned three-field residuals are impossible

## 1. Setup and result

Let \(U\) be a six-set. At every site \(u\), let \(V_u\) have an ordered
basis

\[
                    a_0^{(u)},a_1^{(u)},a_2^{(u)},
\]

and write \(L_i^{(u)}=\mathbb C a_i^{(u)}\). For a pair \(P\subset U\),
put

\[
 A_i(P)=\bigotimes_{u\notin P}a_i^{(u)},\qquad
 F_i=\sum_{P\in\binom U2}\lambda_{iP}A_i(P),\qquad
 F=F_0+F_1+F_2.                                      \tag{1}
\]

The coefficients in (1) are arbitrary complex aggregate coefficients; in
particular they may vanish after cancellation. Set

\[
                         H_i=\{P:\lambda_{iP}\ne0\}.   \tag{2}
\]

At each site choose three independent target vectors
\(e_0^{(u)},e_1^{(u)},e_2^{(u)}\), and let

\[
                         X_i=\bigotimes_{u\in U}e_i^{(u)}.          \tag{3}
\]

Assume that the target frame has already been aligned with the three line
fields as in the three-frame lemma: after one global permutation,

\[
 D_i=\{u:e_i^{(u)}\notin L_i^{(u)}\},\qquad |D_i|\le2.             \tag{4}
\]

Allow arbitrary multi-site rows \(p_i,s_j\in\bigoplus_uV_u\), and impose
all nine exact responses and the two common-power equations

\[
 p_i s_jF=\delta_{ij}X_i,\qquad
 F=q^{[2]},\qquad q^{[3]}=0.                           \tag{5}
\]

Here \(q\) is an arbitrary quadratic in the site-square-zero algebra; its
endpoint blocks need not be decomposable, symmetric in their two colour
coordinates, nonzero, or generic.

**Theorem 1.1 (aligned three-field obstruction and residual).** Under
(1)--(5):

1. for every colour \(i\), at least one assigned-field coordinate vanishes,

   \[
       \prod_{u\in U}a_i^{(u)*}(e_i^{(u)})=0;                       \tag{6}
   \]

   in particular the generic subcase in which all eighteen assigned-field
   coordinates are nonzero is impossible;
2. if \(|D_0|=|D_1|=|D_2|=2\), then, after relabelling colours,

   \[
       D_0=D_1=P,\qquad D_2=Q\ne P,\qquad
       H_0\cup H_1\cup H_2\subseteq\{P,Q\};                        \tag{7}
   \]
3. if at every site the target frame is a permutation of the line-field
   frame,

   \[
                 e_i^{(u)}\in L_{\sigma_u(i)}^{(u)}
                 \quad(\sigma_u\in S_3),                           \tag{8}
   \]

   then (1)--(5) have no solution.

Thus the aligned three-field branch cannot survive generically, and it
cannot survive by merely permuting the three field axes at the deviant
sites. A remaining solution would have to use genuine linear mixtures at
hard zero-diagonal sites. The theorem does **not** exclude all such mixed
zero-diagonal configurations.

## 2. The nine responses split into three modules

Let

\[
 \mathcal O_2(L_i)=
 \sum_{P\in\binom U2}
 \left(\bigotimes_{u\in P}V_u\right)
 \otimes\left(\bigotimes_{u\notin P}L_i^{(u)}\right).              \tag{9}
\]

In the basis \(a_0,a_1,a_2\), this is the coordinate span of the words at
Hamming distance at most two from \(i^6\). The three word sets are
pairwise disjoint, since a common word would give

\[
 6=d(i^6,j^6)\le d(i^6,w)+d(w,j^6)\le4.                           \tag{10}
\]

Multiplication of \(F_i\) by two rows lies in \(\mathcal O_2(L_i)\).
Moreover, (4) gives \(X_i\in\mathcal O_2(L_i)\). Hence (5) splits
termwise:

\[
 p_i s_jF_r=
 \begin{cases}
 X_i,&i=j=r,\\
 0,&\text{otherwise}.
 \end{cases}                                                       \tag{11}
\]

In particular every \(H_i\) is nonempty. No cancellation between the
three line fields is discarded in deriving (11); it is coordinate-space
separation.

For \(P=\{a,b\}\), write the literal endpoint response

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}+s_{j,a}\otimes p_{i,b}
             \in V_a\otimes V_b.                                  \tag{12}
\]

Both endpoint orders in (12) will be retained throughout.

## 3. The common power forbids a system of distinct active pairs

The following observation uses only the power equations in (5).

**Lemma 3.1 (power Hall obstruction).** The three nonempty families
\(H_0,H_1,H_2\) have no system of distinct representatives.

**Proof.** Suppose that \(P_i\in H_i\) are pairwise distinct. At site
\(u\), define a linear map on the field basis by

\[
 \pi_u(a_i^{(u)})=
 \begin{cases}
 0,&u\in P_i,\\
 a_i^{(u)},&u\notin P_i.
 \end{cases}                                                       \tag{13}
\]

Every linear map on the square-zero ideal \(V_u\) extends, with
\(1\mapsto1\), to a unital algebra endomorphism. Thus
\(\Pi=\bigotimes_u\pi_u\) is an algebra endomorphism. For every pair \(P\),

\[
       \Pi(A_i(P))\ne0
       \quad\Longleftrightarrow\quad P_i\subseteq P
       \quad\Longleftrightarrow\quad P=P_i.                        \tag{14}
\]

Applying \(\Pi\) to the power equations gives

\[
 \Pi(q)^{[2]}=\sum_{i=0}^2\lambda_{iP_i}A_i(P_i),
 \qquad \Pi(q)^{[3]}=0.                                           \tag{15}
\]

All three coefficients in (15) are nonzero and the missing pairs are
distinct. This contradicts the independently audited
[distinct-missing-pair common-power obstruction](distinct-missing-pair-common-power-obstruction.md).
\(\square\)

For three nonempty set families, Hall's theorem specializes to

\[
 \boxed{\text{no SDR}\quad\Longleftrightarrow\quad
 \begin{array}{l}
 H_i=H_j=\{P\}\text{ for some }i\ne j,\ \text{or}\\
 |H_0\cup H_1\cup H_2|\le2.
 \end{array}}                                                     \tag{16}
\]

These are precisely the Hall failures on a two-colour subset or on all
three colours.

**Lemma 3.2 (singleton collisions cannot respond).** It is impossible
that \(H_i=H_j=\{P\}\) for distinct \(i,j\). More generally, it is
impossible that

\[
                  H_i=\{P\},\qquad P\in H_j,\qquad D_j=P.          \tag{17}
\]

**Proof.** In the first situation, the \((i,i)\) equation in the
\(i\)-module says \(B_{ii}(P)\ne0\), whereas the same row pair in the
\(j\)-module says \(B_{ii}(P)=0\). The nonzero aggregate coefficients and
the nonzero four-site field products can be cancelled from these two
statements.

For (17), the singleton \(i\)-module similarly gives \(B_{jj}(P)=0\).
Quotient the \(j\)-module equation at the two sites of \(P=D_j\) by the
lines \(L_j\). Only its \(P\)-term survives, and the image of \(X_j\) is a
nonzero pure tensor. Hence the image of \(B_{jj}(P)\), and therefore
\(B_{jj}(P)\) itself, is nonzero. This is a contradiction. \(\square\)

## 4. Nonzero assigned coordinates force private pairs

Let \(a_i^{(u)*}\) be the coordinate covector dual to \(a_i^{(u)}\), and
put

\[
 \alpha_{i,u}=a_i^{(u)*}(e_i^{(u)}),\qquad
 \gamma_i=\prod_{u\in U}\alpha_{i,u}.                             \tag{18}
\]

For \(P=\{a,b\}\), define

\[
 \beta_i(P)=
 (a_i^{(a)*}\otimes a_i^{(b)*})B_{ii}(P).                         \tag{19}
\]

If \(\gamma_i\ne0\), the coefficient of the central word
\(\bigotimes_ua_i^{(u)}\) in the \(i\)-module of (11) gives

\[
                         \sum_P\lambda_{iP}\beta_i(P)=\gamma_i\ne0.
                                                                        \tag{20}
\]

Fix \(r\ne i\) and an active pair \(P\in H_r\). In the zero equation
\(p_i s_iF_r=0\), inspect the word which is \(a_i\) at the two sites of
\(P\) and \(a_r\) at the other four sites. Its two deviations from the
\(r\)-centre determine \(P\) uniquely, so its coefficient is

\[
                            \lambda_{rP}\beta_i(P)=0.               \tag{21}
\]

Consequently \(\beta_i(P)=0\) whenever \(P\) is active in a field other
than \(i\). Equation (20) therefore supplies a private pair

\[
                 P_i\in H_i\setminus\bigcup_{r\ne i}H_r.           \tag{22}
\]

This uses an isolated coordinate word in the already split \(r\)-module;
it never infers termwise vanishing from an unseparated zero sum.

**Proposition 4.1 (every colour has a hard diagonal zero).** In any
solution of (1)--(5), \(\gamma_i=0\) for all three colours.

**Proof.** If two colours have nonzero \(\gamma_i\), choose their two
private pairs from (22). They are distinct, and every active pair of the
third colour is distinct from both. This gives an SDR, contrary to Lemma
3.1.

If exactly one colour \(i\) has nonzero \(\gamma_i\), choose its private
pair \(P_i\). The other two active families avoid \(P_i\). Unless those
two families are the same singleton \(\{Q\}\), they have distinct
representatives, which together with \(P_i\) give an SDR. The remaining
possibility is forbidden by Lemma 3.2. Thus no colour has nonzero
\(\gamma_i\). \(\square\)

Since a product over \(\mathbb C\) is zero only when one factor is zero,
this proves assertion (6). It is stronger than merely saying that the
all-generic chart is empty: every individual target colour must hit a
hard zero-diagonal chart.

## 5. Two-site deviations and shared-pair geometry

Let \(\rho_{i,u}:V_u\to V_u/L_i^{(u)}\) be the quotient map.

**Lemma 5.1 (a two-site deviant pair is active).** If \(D_i=P\) has two
sites, then \(P\in H_i\), and

\[
 (\rho_{i,a}\otimes\rho_{i,b})B_{ii}(P)
   \quad\text{is a nonzero scalar multiple of}\quad
 \rho_{i,a}(e_i^{(a)})\otimes\rho_{i,b}(e_i^{(b)}).                 \tag{23}
\]

**Proof.** Apply the two quotient maps at \(P\) to the \(i\)-module in
(11). A term with missing pair \(Q\) survives only if \(P\subseteq Q\),
hence only if \(Q=P\). The target quotient is nonzero at both deviant
sites, while its four outside factors lie on nonzero \(L_i\)-lines.
\(\square\)

There is also an exact restriction when another field uses the same pair.

**Lemma 5.2 (shared-pair cross).** Suppose \(D_i=P=\{a,b\}\), and let
\(\{i,r,s\}=\{0,1,2\}\). If \(P\in H_r\), then at least one endpoint obeys

\[
              e_i^{(a)}\in L_i^{(a)}+L_r^{(a)}
              \quad\text{or}\quad
              e_i^{(b)}\in L_i^{(b)}+L_r^{(b)}.                    \tag{24}
\]

If \(P\) is active in both competitor fields \(r\) and \(s\), then, up to
swapping \(a,b\),

\[
 \rho_{i,a}(e_i^{(a)})\in\mathbb C^*\rho_{i,a}(a_r^{(a)}),\qquad
 \rho_{i,b}(e_i^{(b)})\in\mathbb C^*\rho_{i,b}(a_s^{(b)}).         \tag{25}
\]

In this double-sharing case \(B_{ii}(P)\) itself is a nonzero pure tensor
on one of the two cells \(a_r\otimes a_s\) or \(a_s\otimes a_r\).

**Proof.** The quotient of the zero \(r\)-module equation at \(P\) gives

\[
 B_{ii}(P)\in
 C_r:=L_r^{(a)}\otimes V_b+V_a\otimes L_r^{(b)}.                    \tag{26}
\]

In the \(a_0,a_1,a_2\) coordinate matrix, \(C_r\) is the union of row
\(r\) and column \(r\). Modulo \(L_i\), write the two target quotient
factors from (23) in the basis \(r,s\). Membership in \(C_r\) says that
their \((s,s)\) product is zero, proving (24).

If the pair is also active in \(s\), then

\[
 C_r\cap C_s
   =\operatorname{span}\{a_r^{(a)}\otimes a_s^{(b)},
                           a_s^{(a)}\otimes a_r^{(b)}\}.            \tag{27}
\]

The nonzero quotient in (23) has rank one. A rank-one tensor in the
anti-diagonal two-cell space (27) occupies exactly one cell, proving (25)
and the last assertion. \(\square\)

The case where all three deviant pairs coincide is already impossible,
even before assuming that the target deviations are coordinate axes.

**Lemma 5.3 (three targets cannot share one deviant pair).** It is
impossible that

\[
                              D_0=D_1=D_2=P,\qquad |P|=2.           \tag{28}
\]

**Proof.** Lemma 5.1 makes \(P\) active in all three fields. Quotienting
at \(P\) in each of the three modules shows that, for \(i\ne j\),
\(B_{ij}(P)\) lies in all three cross spaces \(C_0,C_1,C_2\). Their
coordinate-cell intersection is zero, so

\[
                              B_{ij}(P)=0\quad(i\ne j).              \tag{29}
\]

For a diagonal \(B_{ii}(P)\), the two competitor equations and Lemma 5.2
put it on one nonzero pure coordinate cell. Choose endpoint covectors
\(\phi_a,\phi_b\) which are nonzero on the three respective endpoint
factors; this is possible over \(\mathbb C\), since only finitely many
hyperplanes must be avoided. The scalar matrix

\[
                 M_{ij}=(\phi_a\otimes\phi_b)B_{ij}(P)              \tag{30}
\]

is diagonal with three nonzero diagonal entries, hence has rank three.
On the other hand, (12) gives

\[
 M_{ij}=x_i v_j+y_i u_j,
\]

where \(x_i=\phi_a(p_{i,a})\), \(y_i=\phi_b(p_{i,b})\),
\(u_j=\phi_a(s_{j,a})\), and \(v_j=\phi_b(s_{j,b})\). Thus \(M\) is the
sum of two rank-one matrices and has rank at most two, a contradiction.
\(\square\)

We can now prove assertion (7). If all three \(D_i\)'s have size two,
Lemma 5.1 gives the three active representatives \(D_i\in H_i\). They
cannot be pairwise distinct by Lemma 3.1, and they cannot all coincide by
Lemma 5.3. Hence, after relabelling,

\[
                         D_0=D_1=P,\qquad D_2=Q\ne P.               \tag{31}
\]

Apply the Hall dichotomy (16). A two-family singleton failure could only
be \(H_0=H_1=\{P\}\), which Lemma 3.2 forbids. Therefore the total union
has size at most two. Since it already contains \(P,Q\), it is exactly
\(\{P,Q\}\), proving (7).

## 6. Coordinate-permutation deviations are impossible

Assume (8). Since the three target vectors at a site are independent,
each \(\sigma_u\) really is a permutation. Proposition 4.1 says that every
colour is moved at least once, while alignment says it is moved at most
twice:

\[
                              1\le |D_i|\le2.                         \tag{32}
\]

We need one additional consequence for a singleton deviation.

**Lemma 6.1 (singleton exclusion).** Suppose \(D_i=\{u\}\), put
\(t=\sigma_u(i)\ne i\), and let \(k\) be the third colour. Then

\[
                              H_i\setminus H_k\ne\varnothing.       \tag{33}
\]

**Proof.** The target word is \(t\) at \(u\) and \(i\) at the other five
sites. In the \(i\)-module, its coefficient is a sum over the missing
pairs \(P=\{u,v\}\), using the \((t,i)\) endpoint coordinate of
\(B_{ii}(P)\), and this sum is nonzero. In the zero \(k\)-module, the
hybrid word with endpoint symbols \(t,i\) and centre \(k\) elsewhere has
two deviations from \(k^6\). Those deviations uniquely determine \(P\).
Thus the relevant endpoint coefficient vanishes whenever \(P\in H_k\).
At least one nonzero contributor in the \(i\)-module therefore belongs to
\(H_i\setminus H_k\). \(\square\)

Ignore sites where \(\sigma_u\) is the identity. A nonidentity permutation
moves either two colours (a transposition) or three colours (a three-cycle).
The total number \(\sum_i|D_i|\) lies between three and six. There are five
possibilities.

### 6.1 One three-cycle

All three \(D_i\)'s are the same singleton. Orient the cycle so that
Lemma 6.1 gives cyclic strict differences

\[
                 H_0\setminus H_2\ne\varnothing,\qquad
                 H_1\setminus H_0\ne\varnothing,\qquad
                 H_2\setminus H_1\ne\varnothing.                  \tag{34}
\]

These three families have an SDR. To see this directly from (16), a
two-family singleton would equate two families joined by one of the
directed differences in (34). If their total union had at most two
elements, none of the three sets could be the full two-set, because every
set occurs as the predecessor on the right of one strict difference.
Thus all three would be singletons. The cyclic differences would then
require an odd cycle of pairwise different singletons chosen from a
two-set, also impossible. Lemma 3.1 gives the contradiction.

### 6.2 Two transpositions

The transpositions must be different, or one colour would never move.
Thus, for suitable colours \(i,j,k\) and sites \(u,v\),

\[
                 D_i=\{u\},\qquad D_j=\{v\},\qquad D_k=\{u,v\}.    \tag{35}
\]

Lemma 6.1 gives elements

\[
                         A\in H_i\setminus H_j,\qquad
                         B\in H_j\setminus H_i,                    \tag{36}
\]

and Lemma 5.1 gives \(P=\{u,v\}\in H_k\). Here \(A\ne B\). If Hall
fails on a two-family subset involving \(H_k\), the corresponding
singleton field is \(\{P\}\). If Hall instead fails on all three families,
their union is the two-set \(\{A,B\}\); according as \(P=A\) or \(P=B\),
\(H_i=\{P\}\) or \(H_j=\{P\}\). Every alternative contradicts (17),
because \(D_k=P\).

### 6.3 A three-cycle and a transposition

The colour \(i\) fixed by the transposition has a singleton deviant set;
the other two colours \(j,k\) have the same two-site deviant pair \(P\).
Lemma 6.1 can be oriented as

\[
                 A\in H_i\setminus H_k,\qquad
                 P\in H_j\cap H_k,\qquad A\ne P.                   \tag{37}
\]

If Hall fails on a pair of families, the only viable pair is
\(H_j=H_k=\{P\}\). If it fails on all three, their union is
\(\{A,P\}\), and \(A\notin H_k\) forces \(H_k=\{P\}\). In either case a
singleton field at \(P\) coexists with the active \(j\)-field whose
deviant pair is \(P\), contradicting (17).

### 6.4 Three transpositions

Every colour must be moved exactly twice, so the three transpositions are
the three different colour pairs. The resulting \(D_0,D_1,D_2\) are
three distinct two-sets. Lemma 5.1 supplies them as an SDR, contrary to
Lemma 3.1.

### 6.5 Two three-cycles

All three deviant sets are the same pair of sites, contrary to Lemma 5.3.
This exhausts the coordinate-permutation case and proves assertion (8) of
Theorem 1.1.

## 7. Exact scope and audit

The proof permits arbitrary aggregate complex coefficients, repeated
descriptions of a lift, arbitrary multi-site rows, both endpoint orders,
and arbitrary endpoint-ordered blocks of \(q\). The only external theorem
used is the already independently audited distinct-missing-pair power
obstruction, invoked after the explicit unital algebra projection (13).
There is no limit, orbit-closure, positivity, or generic-weight argument.

The remaining aligned three-field frontier is genuinely mixed. Every
target colour must have a zero coefficient on its assigned line at some
site. If all three deviant sets have size two, only the two-pair support
configuration (7) remains, and Lemma 5.2 forces additional coordinate-plane
incidences there. Configurations with one-site deviations also remain when
the deviant target vector is a nontrivial linear combination of the two
other field axes. Those cases require a new use of the shared-pair
equations or of the unprojected common-power blocks; the permutation proof
above must not be extended to them without such an argument.

The standalone checker
[verify_aligned_three_field_common_power_obstruction.py](../computations/verify_aligned_three_field_common_power_obstruction.py)
audits the three radius-two modules, every hybrid-word isolation, all
\(15^3=3375\) selected-pair projections, Hall's three-family classification,
the cross-space intersections and rank minors, and all \(6^6\) sitewise
permutation assignments. Exactly \(462\) assignments move every colour at
least once and at most twice; they fall into the five cases above with
counts \(12,90,180,120,60\).
