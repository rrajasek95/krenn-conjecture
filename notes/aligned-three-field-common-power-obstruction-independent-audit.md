# Independent audit of the aligned three-field common-power obstruction

## 1. Verdict

This is a clean-room, adversarial audit of
[the aligned three-field note](aligned-three-field-common-power-obstruction.md).
The three assertions in that note are correct under their stated hypotheses.
I found no arbitrary-vector, endpoint-order, aggregation, or complex-cancellation
gap.

The exact result is important.  It proves that every aligned target colour has
an assigned-field coordinate equal to zero somewhere; it classifies the branch
where all three deviant sets have size two; and it eliminates every residual in
which the target frame is obtained by sitewise permutations of the three line
fields.  It does **not** eliminate a deviant vector such as
\(a_1^{(u)}+\tau a_2^{(u)}\) with \(\tau\ne0\).  General linear mixtures on the
hard zero-diagonal sites remain open.

The companion
[independent checker](../computations/audit_aligned_three_field_common_power_obstruction_independent.py)
imports neither the primary checker nor project code.  It uses bit-mask pairs,
a coordinate alphabet with transverse directions, capped incidence profiles
and augmenting-path matchings, a dynamic-programming permutation census, and a
custom determinant expansion.

## 2. Ambient algebra and the exact three-module split

At a site \(u\), write

\[
 A_u=\mathbb C\oplus V_u,\qquad
 (\alpha,v)(\beta,w)=(\alpha\beta,\alpha w+\beta v).              \tag{A1}
\]

Thus \(V_u^2=0\), and the six-site algebra is
\(\mathcal R_U=\bigotimes_{u\in U}A_u\).  Extend the three displayed field
vectors \(a_0^{(u)},a_1^{(u)},a_2^{(u)}\) to a basis of \(V_u\).  The extra
basis directions are left arbitrary; they are useful for checking that no
three-dimensional local-space assumption has slipped into a coefficient
argument.

For \(P=\{a,b\}\), multiplication of a pure lift

\[
 A_r(P)=\bigotimes_{u\notin P}a_r^{(u)}                            \tag{A2}
\]

by arbitrary rows \(p_i=\sum_up_{i,u}\) and \(s_j=\sum_us_{j,u}\) kills every
row component at a site outside \(P\).  It also kills two components at the
same endpoint.  The complete surviving endpoint tensor is therefore

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}+s_{j,a}\otimes p_{i,b}.          \tag{A3}
\]

Both endpoint orders are present.  The rows were not assumed endpoint
supported: their other site components vanished by the local algebra law,
while every endpoint coordinate, including transverse coordinates, remains
inside the four vectors in (A3).

Let \(\mathcal O_2(L_r)\) be the coordinate span of tensor words differing
from \(a_r^{\otimes6}\) at no more than two sites.  Equation (A3) shows

\[
                         p_i s_jF_r\in\mathcal O_2(L_r).           \tag{A4}
\]

The three spaces are in direct sum.  Indeed, a coordinate word common to the
\(r\)- and \(t\)-spaces would satisfy

\[
 6=d(r^6,t^6)\le d(r^6,w)+d(w,t^6)\le4,                           \tag{A5}
\]

where transverse coordinate symbols are simply further letters in the local
alphabet.  Since \(|D_i|\le2\), expansion of the possibly mixed pure tensor
\(X_i=\bigotimes_ue_i^{(u)}\) also lies in \(\mathcal O_2(L_i)\).  Consequently
the nine response equations split coefficientwise as

\[
 p_i s_jF_r=\begin{cases}X_i,&i=j=r,\\0,&\text{otherwise}.
             \end{cases}                                         \tag{A6}
\]

This is a direct-sum projection, not a termwise inference from an unseparated
zero sum.  In particular, each aggregate active family

\[
                         H_r=\{P:\lambda_{rP}\ne0\}               \tag{A7}
\]

is nonempty because the corresponding diagonal target is nonzero.

## 3. The power projection and the complete Hall alternative

Assume that \(P_r\in H_r\) are pairwise distinct.  At each site define a
linear map on the full local ideal by

\[
 \pi_u(a_r^{(u)})=\begin{cases}
 0,&u\in P_r,\\
 a_r^{(u)},&u\notin P_r,
 \end{cases}                                                       \tag{A8}
\]

and, for definiteness, fix a chosen transverse complement.  Extending
\(\pi_u\) by \(1\mapsto1\) is a unital algebra endomorphism of \(A_u\): the
only product omitted from linearity is a product of two ideal vectors, and
both before and after applying \(\pi_u\) that product is zero.  Hence
\(\Pi=\bigotimes_u\pi_u\) is an algebra endomorphism of \(\mathcal R_U\).

For every pure lift,

\[
 \Pi(A_r(P))\ne0
 \Longleftrightarrow P_r\subseteq P
 \Longleftrightarrow P=P_r,                                      \tag{A9}
\]

where the last equivalence uses that both sets have size two.  Therefore

\[
 \Pi(F)=\sum_{r=0}^2\lambda_{rP_r}A_r(P_r),                       \tag{A10}
\]

with three nonzero coefficients and three distinct missing pairs.  No
restriction has been put on \(q\): every arbitrary endpoint-ordered block is
simply mapped by the corresponding tensor product of the local linear maps.
Algebra functoriality gives

\[
 (\Pi q)^{[2]}=\Pi(q^{[2]}),\qquad
 (\Pi q)^{[3]}=\Pi(q^{[3]}).                                     \tag{A11}
\]

Thus (A10)--(A11) contradict the already independently audited
[distinct-missing-pair common-power theorem](distinct-missing-pair-common-power-obstruction-independent-audit.md).
The imported theorem has precisely the needed scope: three independent local
field axes, distinct missing pairs, nonzero complex coefficients, and an
otherwise arbitrary quadratic \(q\).

It follows that \(H_0,H_1,H_2\) have no system of distinct representatives.
For three nonempty families, the complete form of Hall's theorem is

\[
 \text{no SDR}\quad\Longleftrightarrow\quad
 \left\{
 \begin{array}{l}
 H_i=H_j=\{P\}\text{ for some }i\ne j,\quad\text{or}\\
 |H_0\cup H_1\cup H_2|\le2.
 \end{array}\right.                                               \tag{A12}
\]

There is no missing one-family case because every \(H_i\) is nonempty.  A
two-family Hall failure means that their union has size at most one, hence
both are the same singleton.  A three-family failure means that the total
union has size at most two.  This also proves the converse in (A12).

## 4. Singleton collisions and private pairs

Two response facts remove the dangerous two-family Hall failures.

First suppose \(H_i=H_j=\{P\}\).  The diagonal \(i\)-module in (A6), after
canceling its nonzero aggregate coefficient and four nonzero outside field
factors, forces \(B_{ii}(P)\ne0\).  The zero \(j\)-module for the same row
pair has the single term \(P\) and forces \(B_{ii}(P)=0\).  This is an exact
contradiction.

More generally, suppose

\[
                         H_i=\{P\},\qquad P\in H_j,\qquad D_j=P.   \tag{A13}
\]

The singleton \(i\)-module gives \(B_{jj}(P)=0\).  Quotient the \(j\)-module
at both sites of \(P\) by the assigned lines \(L_j\).  Every term with
missing pair \(Q\ne P\) has a fixed \(a_j\)-factor at a site in
\(P\setminus Q\) and dies.  The \(P\)-term is active, while the target has a
nonzero quotient at both deviant sites.  Hence the quotient of
\(B_{jj}(P)\) is nonzero, contradicting its vanishing.  This proves both
singleton-collision statements without assuming anything about endpoint
decomposability.

Now let \(a_i^{(u)*}\) be the assigned coordinate covector and put

\[
 \alpha_{i,u}=a_i^{(u)*}(e_i^{(u)}),\qquad
 \gamma_i=\prod_{u\in U}\alpha_{i,u},\qquad
 \beta_i(P)=(a_i^*\otimes a_i^*)B_{ii}(P).                         \tag{A14}
\]

The coefficient of the central word \(a_i^{\otimes6}\) in the diagonal
\(i\)-module is

\[
                         \sum_P\lambda_{iP}\beta_i(P)=\gamma_i.  \tag{A15}
\]

Fix \(r\ne i\) and \(P\in H_r\).  In the zero \(r\)-module inspect the word
which is \(a_i\) at the two sites of \(P\) and \(a_r\) at the other four.
Its two deviations from the \(r\)-centre determine \(P\) uniquely, including
when arbitrary transverse endpoint coordinates and all other active pairs are
present.  Its coefficient is exactly

\[
                              \lambda_{rP}\beta_i(P)=0.            \tag{A16}
\]

Thus \(\beta_i(P)=0\) on every pair active in another field.  If
\(\gamma_i\ne0\), equation (A15) has a nonzero contributor and supplies a
private pair

\[
                       P_i\in H_i\setminus\bigcup_{r\ne i}H_r.    \tag{A17}
\]

Two colours with private pairs immediately give two distinct representatives,
and any representative of the third family is distinct from both.  This is
an SDR.  If only one colour \(i\) has a private pair \(P_i\), the other two
families avoid \(P_i\).  They have distinct representatives unless they are
the same singleton \(\{Q\}\); that last case is the singleton collision just
proved.  Therefore no \(\gamma_i\) can be nonzero:

\[
                              \gamma_0=\gamma_1=\gamma_2=0.        \tag{A18}
\]

Since the coefficient field is an integral domain, (A18) says separately
for each target colour that at least one assigned-field coordinate is exactly
zero.  It is not a generic-density or closure argument.

## 5. Two-site deviant sets and the common-pair rank obstruction

Suppose \(D_i=P=\{a,b\}\).  Quotienting the diagonal \(i\)-module by \(L_i\)
at \(a,b\) isolates the unique missing pair \(P\).  The target quotient is a
nonzero pure tensor, so

\[
 P\in H_i,\qquad
 (\rho_{i,a}\otimes\rho_{i,b})B_{ii}(P)\ne0,                       \tag{A19}
\]

and the latter tensor is proportional to the two endpoint target quotients.

If \(P\in H_r\) as well, quotienting the zero \(r\)-module at the same two
sites yields

\[
 B_{ii}(P)\in C_r
 :=L_r^{(a)}\otimes V_b+V_a\otimes L_r^{(b)}.                      \tag{A20}
\]

In the \(3\times3\) field-coordinate matrix, \(C_r\) is the span of row
\(r\) and column \(r\).  If \(s\) is the third colour, membership in \(C_r\)
sets the \((s,s)\) entry of the rank-one target quotient to zero.  Therefore
one endpoint target quotient lies on the \(r\)-axis, which is precisely the
coordinate-plane alternative stated in the primary note.

If \(P\) is active in both competitors \(r,s\), then

\[
 C_r\cap C_s
 =\operatorname{span}\{a_r^{(a)}\otimes a_s^{(b)},
                         a_s^{(a)}\otimes a_r^{(b)}\}.              \tag{A21}
\]

A nonzero pure tensor has rectangular coordinate support.  The only nonempty
rectangles contained in the two-cell anti-diagonal (A21) are its individual
cells.  Hence \(B_{ii}(P)\) occupies exactly one of those two cells.  This
argument is insensitive to cancellation between the two ordered terms in
(A3): it is applied to their already aggregated tensor \(B_{ii}(P)\).

Now assume \(D_0=D_1=D_2=P\).  Equation (A19) makes \(P\) active in every
field.  For \(i\ne j\), quotienting the zero response \(p_i s_jF_r=0\) at
\(P\) for each \(r\) puts \(B_{ij}(P)\) in all three crosses.  But

\[
                              C_0\cap C_1\cap C_2=0,               \tag{A22}
\]

so every off-diagonal \(B_{ij}(P)\) vanishes.  Each diagonal block is a
nonzero pure coordinate cell by (A19)--(A21).  Choose one covector at each
endpoint nonzero on all three diagonal endpoint factors; the complement of
finitely many hyperplanes is nonempty over \(\mathbb C\).  Applying these
covectors gives a scalar \(3\times3\) matrix \(M\) which is diagonal with
three nonzero diagonal entries.  Hence \(\operatorname{rank}M=3\).

On the other hand, the literal two endpoint orders (A3) give

\[
                              M=xv^{\mathsf T}+yu^{\mathsf T},     \tag{A23}
\]

so \(\operatorname{rank}M\le2\).  This contradiction excludes a common
two-site deviant pair for all three targets.

If all three \(|D_i|=2\), the designated choices \(D_i\in H_i\) from (A19)
cannot be pairwise distinct by the power Hall obstruction and cannot all be
equal by (A22)--(A23).  Thus, after relabelling,

\[
                              D_0=D_1=P,\qquad D_2=Q\ne P.         \tag{A24}
\]

The two-family branch of (A12) could only be
\(H_0=H_1=\{P\}\), which is the first singleton collision.  Therefore the
total union has size at most two.  It already contains \(P,Q\), so

\[
                       H_0\cup H_1\cup H_2\subseteq\{P,Q\}.       \tag{A25}
\]

In fact equality holds because both pairs are active.  This independently
recovers the complete all-\(|D|=2\) classification.

## 6. Coordinate-permutation residuals

Assume each target frame is a sitewise permutation of the line-field frame.
Independence of the three target vectors makes the local assignment a genuine
permutation.  Equation (A18) and the alignment hypothesis give

\[
                              1\le |D_i|\le2.                       \tag{A26}
\]

The following singleton consequence is the only new response input.  If
\(D_i=\{u\}\), let the target axis at \(u\) be \(t\ne i\), and let \(k\) be
the third colour.  The \(i\)-centred coefficient of the target word is a sum
over \(P=\{u,v\}\) of endpoint coordinates with labels \(t\) at \(u\) and
\(i\) at \(v\).  The sum is nonzero.  For any one such \(P\), the \(k\)-centred
word with those two endpoint labels and \(k\) at the other four sites has a
unique origin, namely \(P\), and occurs in a zero response.  If \(P\in H_k\),
the same endpoint coordinate must vanish.  At least one nonzero contributor
therefore obeys

\[
                              H_i\setminus H_k\ne\varnothing.      \tag{A27}
\]

This reasoning allows cancellation in the initial five-term target sum: it
only selects one actually nonzero aggregate contributor after observing that
the sum is nonzero.

A nonidentity local permutation is a transposition, moving two colours, or a
three-cycle, moving three.  Since the total number of moves lies between
three and six, (A26) leaves exactly five patterns.

1. **One three-cycle.**  Orienting it gives
   \(H_0\setminus H_2\ne\varnothing\),
   \(H_1\setminus H_0\ne\varnothing\), and
   \(H_2\setminus H_1\ne\varnothing\).  No two families joined by one of
   these directed differences can be the same singleton.  If their total
   union had size at most two, every family would have to be a singleton:
   a full two-set cannot be the right-hand predecessor in a strict
   difference.  Three singleton values on a two-set cannot satisfy the odd
   directed cycle.  Thus (A12) gives an SDR, a contradiction.

2. **Two distinct transpositions.**  The singleton colours \(i,j\) satisfy
   \(A\in H_i\setminus H_j\) and \(B\in H_j\setminus H_i\), while the colour
   moved twice has \(D_k=P=\{u,v\}\in H_k\).  Here \(A\ne B\).  A pairwise
   Hall failure involving \(H_k\) makes the other family the singleton
   \(\{P\}\).  In the total-union branch, the union is \(\{A,B\}\); if
   \(P=A\), then \(H_i=\{P\}\), and if \(P=B\), then \(H_j=\{P\}\).  Every
   alternative is exactly the forbidden configuration (A13) with
   \(D_k=P\).

3. **One three-cycle and one transposition.**  The colour fixed by the
   transposition has a singleton deviant set and, after orientation,
   \(A\in H_i\setminus H_k\).  The other two colours have the same deviant
   pair \(P\), so \(P\in H_j\cap H_k\) and \(A\ne P\).  In either branch of
   (A12), Hall failure forces \(H_k=\{P\}\).  This singleton coexists with
   \(P\in H_j\) and \(D_j=P\), contradicting (A13).

4. **Three transpositions.**  Every colour is moved exactly twice.  The
   three transpositions must be the three distinct colour pairs, so the
   three \(D_i\)'s are distinct two-sets.  The active choices
   \(D_i\in H_i\) form an SDR.

5. **Two three-cycles.**  All three deviant sets are the same two sites,
   contradicting the common-pair rank obstruction (A22)--(A23).

These five cases exhaust, rather than sample, the permutation residual.  A
dynamic-programming census in the independent checker finds exactly \(462\)
six-site assignments satisfying (A26), split as

\[
                              12+90+180+120+60=462.                \tag{A28}
\]

## 7. Cancellation and scope audit

Every coefficient used above is an aggregate coefficient after parallel
descriptions and complex cancellation.  The active sets are defined only
after this aggregation.  The arguments isolate either a direct-sum module,
a literal coordinate word with a unique missing-pair origin, or a quotient
which kills every other missing pair.  None promotes individual raw source
weights to nonzero quantities.

The endpoint block \(B_{ij}(P)\) always contains both ordered products and
may itself have arbitrary tensor rank before quotient restrictions are
applied.  The quadratic \(q\) retains arbitrary endpoint blocks and all
transverse coordinates under the unital projection.  There is no positivity,
generic-weight, decomposability, symmetry, orbit-closure, or limiting
assumption.

The remaining frontier is nevertheless real.  Equation (A18) only forces a
zero coefficient on the assigned field at one or two sites.  A nonzero vector
in the span of both competitor axes is not covered by the permutation census,
and the shared-cross lemma only supplies partial coordinate-plane incidences.
Closing those genuinely mixed hard-zero charts requires new response or
unprojected common-power information; it does not follow from this theorem.

The independent checker reports:

    aligned three-field obstruction independent audit: PASS
    five-letter radius-two modules: 3 disjoint spaces of dimension 265
    selected-pair triples: 3375 total; 2730 distinct
    capped-incidence Hall systems: 16203
    two-site deviation designations: 21
    permutation residuals: 462 = 12 + 90 + 180 + 120 + 60
    Hall implication witnesses: 13500 8 8
