# One or two non-pure line fields cannot carry three target responses

## 1. Result

Let \(U\) be a six-set.  At every site \(u\), let \(V_u\) contain three
independent target vectors

\[
                 e_0^{(u)},e_1^{(u)},e_2^{(u)}.
\]

Choose two arbitrary nonzero local vectors \(a_u,b_u\in V_u\), with no
assumption that their lines are distinct.  Put

\[
 A(P)=\bigotimes_{u\notin P}a_u,
 \qquad B(P)=\bigotimes_{u\notin P}b_u
 \quad(P\in\tbinom U2),                                 \tag{1}
\]

and allow the completely arbitrary two-field multiplier

\[
 F=\sum_{P\in\binom U2}\lambda_P A(P)
      +\sum_{P\in\binom U2}\mu_P B(P).                  \tag{2}
\]

The coefficients may vanish and may cancel after coincident terms are
combined.  The response rows may have arbitrary multi-site support and
arbitrary local components.  A one-field multiplier is included by taking
\(b_u=a_u\) and \(\mu_P=0\).

**Theorem 1.1 (one- and two-line-field obstruction).**  There are no rows
\(p_i,s_i\in\bigoplus_{u\in U}V_u\), for \(i=0,1,2\), such that

\[
                         p_i s_iF=X_i,
 \qquad X_i=\bigotimes_{u\in U}e_i^{(u)}.               \tag{3}
\]

Thus a non-pure six-site common-power escape satisfying the three diagonal
responses must use at least three incompatible local line fields, or edge
blocks which cannot be resolved into two common fields.  Neither the six
off-diagonal products nor \(F=q^{[2]},q^{[3]}=0\) is needed here.

The proof has three ingredients.  A quotient count first forces the two
line fields to span a target coordinate plane at every site.  Quotienting
at the two omitted sites then puts a four-site pure target on the secant
line through the two field products.  Elementary Segre rigidity makes it
one of the endpoints, and a final pigeonhole argument is impossible.

## 2. Two osculating spaces and the plane-incidence count

Write

\[
 L_u=\mathbb C a_u,\qquad
 M_u=\mathbb C b_u,\qquad
 W_u=L_u+M_u.                                           \tag{4}
\]

For a line field \(L=(L_u)\), define

\[
 \mathcal O_2(L)=
 \sum_{P\in\binom U2}
 \left(\bigotimes_{u\in P}V_u\right)
 \otimes\left(\bigotimes_{u\notin P}L_u\right).        \tag{5}
\]

Terms with fewer than two moving factors are already contained in (5), by
enlarging their moving set to a pair.  In the site-square-zero algebra,
multiplication of \(A(P)\) by two arbitrary linear rows retains only the
two endpoint orders.  Consequently multiplication of (2) gives

\[
                         p_i s_iF
       \in\mathcal O_2(L)+\mathcal O_2(M).              \tag{6}
\]

This inclusion retains all cancellation among pairs and between the two
fields.

**Lemma 2.1 (plane incidence).**  If a nonzero pure tensor

\[
                         x=\bigotimes_{u\in U}x_u
       \in\mathcal O_2(L)+\mathcal O_2(M),              \tag{7}
\]

then \(x_u\in W_u\) at least four sites.

**Proof.**  If \(x_u\notin W_u\) at three sites \(T\), apply
\(V_u\to V_u/W_u\) at the sites of \(T\) and the identity elsewhere.
Every summand in either osculating space moves at most two sites, so at
one site of \(T\) it retains a fixed vector in \(L_u\) or \(M_u\), and is
killed.  The image of \(x\) is a tensor product of six nonzero factors and
is nonzero.  This is a contradiction.  \(\square\)

Apply the lemma to the three tensors in (3), and set

\[
                         S_i=\{u:e_i^{(u)}\in W_u\}.    \tag{8}
\]

It gives \(|S_i|\ge4\) for every \(i\), hence at least twelve incidences
\((i,u)\).  But \(\dim W_u\le2\), so \(W_u\) contains at most two of the
three independent target axes at site \(u\).  There are at most twelve
incidences.  Equality is forced everywhere:

\[
 \boxed{
   |S_i|=4\text{ for every }i,\qquad
   \dim W_u=2\text{ and }W_u\text{ contains exactly two target axes
   for every }u.}                                      \tag{9}
\]

Consequently the omission sets

\[
                         P_i=U\setminus S_i             \tag{10}
\]

are three pairwise disjoint pairs which partition \(U\).  In particular,
\(L_u\ne M_u\) at every site; this conclusion was not assumed.  Notice
also that (9) already proves the one-field case, since then every \(W_u\)
has dimension one.

## 3. The quotient at an omission pair

Fix a colour \(i\), and apply the quotient maps

\[
 V_u\longrightarrow V_u/W_u\quad(u\in P_i)             \tag{11}
\]

and the identity maps at the other four sites.  The target \(X_i\)
survives because \(e_i^{(u)}\notin W_u\) precisely at the sites of \(P_i\).

In \(\mathcal O_2(L)\), a summand with moving pair \(P\) survives (11)
only if \(P_i\subseteq P\).  Since both are pairs, this means \(P=P_i\).
The same holds for \(\mathcal O_2(M)\).  Thus the image of (3), flattened
between \(P_i\) and its complement \(C_i=U\setminus P_i\), has the form

\[
 \bar X_{i,P_i}\otimes X_{i,C_i}
       =Z_L\otimes L_{C_i}+Z_M\otimes M_{C_i},          \tag{12}
\]

where

\[
 L_{C_i}=\bigotimes_{u\in C_i}a_u,\qquad
 M_{C_i}=\bigotimes_{u\in C_i}b_u,                     \tag{13}
\]

and \(Z_L,Z_M\) are arbitrary tensors in the two quotient slots.  The two
four-site products in (13) are linearly independent: proportional pure
tensors have proportional factors at every site, whereas (9) gives
\(L_u\ne M_u\) at all four sites.

Since the left side of (12) has flattening rank one and the two right
factors \(L_{C_i},M_{C_i}\) are independent, both \(Z_L,Z_M\) are scalar
multiples of \(\bar X_{i,P_i}\).  Explicitly, quotient the left flattening
space by \(\mathbb C\bar X_{i,P_i}\); independence of the two right factors
then kills the two quotient classes separately.  Therefore

\[
                         X_{i,C_i}
             \in\operatorname{span}\{L_{C_i},M_{C_i}\}.             \tag{14}
\]

We use the elementary secant fact that if two nonzero pure tensors
\(\bigotimes_{u\in C}l_u\) and \(\bigotimes_{u\in C}m_u\) have
nonproportional factors at two or more sites, their projective secant line
contains no third pure tensor.  Indeed, flatten at one such site against
the remaining sites.  A linear combination with both coefficients nonzero
is a sum of two rank-one matrices having independent left factors and
independent right factors, hence has matrix rank two.  A pure tensor has
rank one.

Here the factors differ at all four sites, so (14) implies one of the two
alternatives

\[
 \begin{array}{ll}
 e_i^{(u)}\in L_u&\text{for every }u\in C_i,\\
 \text{or}\qquad e_i^{(u)}\in M_u&\text{for every }u\in C_i.
 \end{array}                                             \tag{15}
\]

## 4. Pigeonhole contradiction

Assign each colour \(i\) one of the fields \(L,M\) supplied by (15).  Two
of the three colours, say \(i\ne j\), receive the same field.  Their
omission pairs \(P_i,P_j\) are disjoint by (10), so

\[
                    |C_i\cap C_j|
       =|U\setminus(P_i\cup P_j)|=2.                    \tag{16}
\]

At either site in this intersection, the same one-dimensional line would
contain both independent vectors \(e_i\) and \(e_j\), which is impossible.
This proves Theorem 1.1.

## 5. Why assigning a tensor to one field directly is invalid

A pure tensor in a sum of two osculating spaces need not belong to either
space separately when the fields coincide at some sites.  For example,
let the fields differ only at site \(0\), agree at sites \(1,\ldots,5\),
and choose transverse vectors \(t_4,t_5\) at the last two sites.  Then

\[
 (a_0+b_0)\otimes a_1\otimes a_2\otimes a_3\otimes t_4\otimes t_5
                                                                  \tag{17}
\]

is the sum of one tensor in \(\mathcal O_2(L)\) and one in
\(\mathcal O_2(M)\), but it deviates from each field at three sites and
belongs to neither osculating space by the one-field quotient lemma.

Thus a direct two-Hamming-ball assignment would be false.  The
plane-incidence equality (9), followed by the omission-pair quotient, is
what removes this genuine secant bridge.

## 6. Conditional three-field frame lemma

There is one clean further widening, but it leaves a real residual case.
Choose three line fields

\[
                         L_u^{(0)},L_u^{(1)},L_u^{(2)}              \tag{18}
\]

and assume that their three lines form a basis of \(V_u\) at every site.
Let

\[
                         F\in\sum_{r=0}^2
       \sum_{P\in\binom U2}
       \left(\bigotimes_{u\notin P}L_u^{(r)}\right),     \tag{19}
\]

where the two omitted slots are understood as absent, as in (1).

**Lemma 6.1 (three-frame alignment).**  If rows satisfy the three diagonal
responses \(p_i s_iF=X_i\), then, after one global permutation of the three
line fields, each target colour \(i\) obeys

\[
              e_i^{(u)}\in L_u^{(i)}
              \quad\text{at least four of the six sites}.          \tag{20}
\]

Equivalently, every target axis has a deviant set of size at most two from
its assigned field.  This is a conditional normal form, not a contradiction.

**Proof.**  Use the three field vectors as a local basis.  If a pure tensor
\(x=\bigotimes_u x_u\) belongs to
\(\sum_r\mathcal O_2(L^{(r)})\), let

\[
 S_u=\{r:\text{the }L_u^{(r)}\text{-coordinate of }x_u
                   \text{ is nonzero}\}.                \tag{21}
\]

The coordinate support of \(x\) is the Cartesian box
\(\prod_u S_u\).  Every word in this box must occur in the coordinate
support of one of the three osculating spaces.  Thus every such word has
some symbol occurring at least four times.

We claim that this forces \(S_u=\{r\}\) at least four sites for one
symbol \(r\).  Otherwise make a bipartite graph from the six sites to
three colours, with neighbours \(S_u\), and replace every colour by three
identical capacity slots.  Hall's condition can fail only for a set \(T\)
of sites with

\[
                         |T|>3\left|\bigcup_{u\in T}S_u\right|.     \tag{22}
\]

If the union has one colour, failure means that at least four of the
\(S_u\)'s are that singleton, contrary to the assumption.  A two-colour
union has capacity six, and a three-colour union has capacity nine, so
neither can fail on six sites.  Hall therefore supplies a word in
\(\prod_uS_u\) using every symbol at most three times, a contradiction.
The claim follows.

Apply the claim to each \(X_i\).  It assigns every target colour to a line
field on at least four sites.  Two independent target colours cannot be
assigned to the same field: their two agreement sets would overlap in at
least two sites, forcing one line to contain two independent axes.  The
three assignments are therefore a permutation, which proves (20).
\(\square\)

The unresolved three-field boundary is now precise.  The three deviant
sets in (20) may be arbitrary pairs or smaller sets, and the field
directions at those sites may be general.  Lemma 6.1 alone neither makes
the deviant pairs disjoint nor turns (19) into the target-pure span.  Any
continuation must use the off-diagonal responses or the common-power
relations to couple those residual deviations.

There is nevertheless an exact separation after the alignment.  In the
three-field basis, \(\mathcal O_2(L^{(r)})\) is spanned by coordinate words
at Hamming distance at most two from the constant word \(r^6\).  For
\(r\ne s\), these two word sets are disjoint: a common word would give

\[
          6=d(r^6,s^6)\le d(r^6,w)+d(w,s^6)\le4.        \tag{23}
\]

Thus the three osculating spaces form a direct sum.  Write \(F=\sum_rF_r\)
according to (19), and let \(\rho(i)\) be the field assigned to target
colour \(i\) in (20).  If, in addition to the three diagonal equations used
in Lemma 6.1, the six off-diagonal response equations also hold, then the
full nine equations split termwise as

\[
 p_i s_jF_r=
 \begin{cases}
   X_i,&i=j\text{ and }r=\rho(i),\\
   0,&\text{otherwise}.
 \end{cases}                                             \tag{24}
\]

This includes the off-diagonal equations, but it is not yet a
contradiction: each of the three field components carries exactly one
target rather than two.  The remaining mechanism must therefore couple the
three separated one-target modules through \(F=q^{[2]}\) and
\(q^{[3]}=0\), or prove that a three-field resolution of the actual edge
blocks cannot exist.

## 7. Scope and exact audit

The proof permits coincident fields, arbitrary transverse directions,
arbitrary zero coefficients, repeated descriptions, arbitrary complex
cancellation, and arbitrary endpoint orders in the rows.  It proves a
response theorem, not a power theorem: it does not assert that an arbitrary
four-site tensor is a sum of two coherent line fields, and it does not yet
classify sums of three fields or general rank-two edge blocks.

The standalone checker
[verify_single_line_field_nonpure_response_obstruction.py](../computations/verify_single_line_field_nonpure_response_obstruction.py)
audits the quotient-survivor rule, the complete incidence equality, the
rank-two secant minor, the final overlap, the genuine bridge (17), all
\(7^6=117{,}649\) local-support patterns in Lemma 6.1, and the disjoint
three-ball decomposition behind (24).
