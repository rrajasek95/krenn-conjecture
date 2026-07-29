# Balanced good-site words couple both deficient-site factors

## 1. Setup

Let \(U=G\sqcup\{o,t\}\), where \(|G|=4\).  Work in the
site-square-zero algebra

\[
 {\cal R}_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u).
\]

For \(r=0,1,2\), choose nonzero field vectors \(a_r^{(u)}\in V_u\).
Assume that

\[
 a_0^{(v)},a_1^{(v)},a_2^{(v)}
 \quad\hbox{are linearly independent for every }v\in G,       \tag{1}
\]

with no independence assumption at the two deficient sites \(o,t\).  For
\(P\in\binom U2\), put

\[
 A_r(P)=\bigotimes_{u\notin P}a_r^{(u)},\qquad
 F=\sum_{r=0}^2\sum_{P\in\binom U2}\lambda_{rP}A_r(P).          \tag{2}
\]

The coefficients in (2) are aggregate complex coefficients and may vanish.
Let the three target vectors at every site be independent, put

\[
 X_i=\bigotimes_{u\in U}e_i^{(u)},
\]

and suppose arbitrary multi-site rows satisfy

\[
                         p_i s_jF=\delta_{ij}X_i.                \tag{3}
\]

No common-power equation is used below.

At a good site, extend the three field vectors to a basis and write
\(\alpha_{i,v,r}\) for the coefficient of \(a_r^{(v)}\) in
\(e_i^{(v)}\).

## 2. The balanced-word coupling

**Lemma 2.1.**  Fix a target \(i\), distinct fields \(r,s\), and a
partition

\[
                         G=R\sqcup S,\qquad |R|=|S|=2.           \tag{4}
\]

If

\[
             \prod_{v\in R}\alpha_{i,v,r}
             \prod_{v\in S}\alpha_{i,v,s}\ne0,                  \tag{5}
\]

then

\[
 e_i^{(o)}\otimes e_i^{(t)}
 \in
 \operatorname {span}\!\left\{
 a_r^{(o)}\otimes a_r^{(t)},
 a_s^{(o)}\otimes a_s^{(t)}
 \right\}.                                                       \tag{6}
\]

**Proof.**  Extract from the diagonal equation \(p_i s_iF=X_i\) the
coefficient of the good-site coordinate word which is \(r\) on \(R\) and
\(s\) on \(S\).  Its target coefficient is the nonzero scalar in (5)
times \(e_i^{(o)}\otimes e_i^{(t)}\).

A field-\(r\) lift can produce this word only if its missing pair contains
the two \(s\)-positions.  Since the missing set itself is a pair, it must be
exactly \(S\).  The two row factors occupy those two good sites, in either
endpoint order, so the factors at \(o,t\) remain
\(a_r^{(o)}\otimes a_r^{(t)}\).  Symmetrically, a field-\(s\) contribution
must have missing pair \(R\) and retains
\(a_s^{(o)}\otimes a_s^{(t)}\).  A lift from the third field differs from
the displayed good word at all four good sites and cannot be changed by
only two row factors.  Thus the extracted equation has the form

\[
 \kappa\,e_i^{(o)}\otimes e_i^{(t)}
 =
 c_r\,a_r^{(o)}\otimes a_r^{(t)}
 +c_s\,a_s^{(o)}\otimes a_s^{(t)},\qquad \kappa\ne0,             \tag{7}
\]

where both endpoint orders and all aggregate cancellation are absorbed in
\(c_r,c_s\).  Division by \(\kappa\) gives (6).  \(\square\)

The conclusion has a useful exact classification.

**Lemma 2.2 (two-point Segre line).**  Let \(x_0,x_1\) and \(y_0,y_1\)
be nonzero vectors.  If a nonzero decomposable tensor \(x\otimes y\) lies
in

\[
 \operatorname {span}\{x_0\otimes y_0,x_1\otimes y_1\},          \tag{8}
\]

then:

1. if \(x_0,x_1\) and \(y_0,y_1\) are both independent,
   \(x\otimes y\) is proportional to one of the two displayed tensors;
2. if \(x_0,x_1\) are proportional, then \(x\) lies on their common line
   and \(y\in\operatorname {span}\{y_0,y_1\}\);
3. if \(y_0,y_1\) are proportional, the symmetric statement holds.

**Proof.**  In the first case choose bases beginning with the two \(x\)'s
and the two \(y\)'s.  A linear combination in (8) has a \(2\times2\)
flattening \(\operatorname {diag}(c_0,c_1)\).  Rank one forces
\(c_0c_1=0\).  In the second case (8) equals the common \(x\)-line
tensor \(\operatorname {span}\{y_0,y_1\}\); the third case is symmetric.
\(\square\)

Combining the lemmas, every supported balanced word either aligns the
target at both deficient sites with one field, or exposes an actual
coincidence among the two field lines at at least one deficient site.  This
is information that disappears if the two bad-site factors are projected
away.

## 3. Why a four-good-site box census alone is insufficient

For a field word \(w\in\{0,1,2\}^G\), let

\[
 {\cal B}_r=\{w:d(w,r^4)\le2\}.
\]

Every four-letter word over three fields repeats some field at least twice,
so

\[
                  \{0,1,2\}^G={\cal B}_0\cup{\cal B}_1\cup{\cal B}_2.
                                                                    \tag{9}
\]

Moreover,

\[
 {\cal B}_r\cap{\cal B}_s
 =
 \{w:w\hbox{ has exactly two }r\hbox{'s and two }s\hbox{'s}\},
 \qquad
 {\cal B}_0\cap{\cal B}_1\cap{\cal B}_2=\varnothing.              \tag{10}
\]

Thus, unlike the five-good-site case, containment of a field-only Cartesian
box in the union of the three radius-two balls imposes no restriction at
all.  The pairwise overlaps (10), rather than box containment, are the
first informative layer, and Lemma 2.1 records their missing two-site
tensor data exactly.

There is nevertheless a small exact exceptional list once transverse
coordinates are retained.  At each good site choose the transverse basis
vector, if any, so that the support of the target factor is a nonempty
subset of

\[
                         \{0,1,2,T\}.                            \tag{11}
\]

Here \(T\) is site-private and is different from every field symbol.  Call
a box **axial** if two sites have the same singleton support \(\{r\}\), and
call it **balanced-free** if it contains no word with two \(r\)'s and two
\(s\)'s for distinct fields.

**Lemma 3.1 (nonaxial balanced-free census).**  Suppose every word in a
four-site Cartesian box from (11) belongs to
\({\cal B}_0\cup{\cal B}_1\cup{\cal B}_2\).  If the box is nonaxial and
balanced-free, then, up to permuting the four sites and the three fields,
its four supports are exactly one of

\[
\begin{array}{c|c}
 &\text{support multiset}\\ \hline
1&0,\ 1,\ 01,\ 2\\
2&0,\ 1,\ 01,\ T\\
3&0,\ 1,\ 01,\ 2T\\
4&0,\ 1,\ 2,\ 012\\
5&0,\ 1,\ 02,\ 02\\
6&0,\ 01,\ 01,\ T\\
7&0,\ 01,\ 01,\ 2T\\
8&0,\ 12,\ 12,\ 12\\
9&01,\ 01,\ 01,\ T\\
10&01,\ 01,\ 01,\ 2T .
\end{array}                                                     \tag{12}
\]

Conversely, every box in (12) is valid, nonaxial, and balanced-free.

The assertion is a finite support statement.  A direct exhaustive proof
considers the fifteen nonempty supports at each site.  Reject a box exactly
when it has a choice word in which no field appears twice; reject it as
balanced exactly when it has a \(2+2\) field word; then quotient the
survivors by the literal action of \(S_4\times S_3\).  This gives

\[
\begin{array}{c|r}
\text{class}&\text{labelled boxes}\\ \hline
\text{valid}&6625\\
\text{valid axial}&3681\\
\text{valid nonaxial}&2944\\
\text{valid nonaxial balanced-free}&492,
\end{array}
\]

and the last 492 boxes form exactly the ten orbits (12), of respective
sizes

\[
                         72,72,72,24,72,72,72,12,12,12.          \tag{13}
\]

The checker performs every rejection and orbit comparison directly and
also verifies the converse for all ten representatives.

The accompanying checker
[verify_two_deficient_balanced_word_coupling.py](../computations/verify_two_deficient_balanced_word_coupling.py)
enumerates all field words, all balanced partitions, all missing pairs,
both row endpoint orders, and all \(15^4=50,625\) support boxes.  It
verifies (9)--(13) and that the only contributors to every balanced word
are precisely the two lifts used in (7).

## 4. Scope and concrete continuation

This note does not close the two-deficient branch.  It applies only after
the multiplier has been resolved into three coherent line fields, and it
does not assert that every target box contains a balanced word.

The next finite structural task is now sharper:

1. for supports containing balanced words, intersect the constraints (6)
   over all supported \(2+2\) words and all three targets, keeping the two
   deficient-site line matroids separate;
2. handle the ten nonaxial exceptional orbits (12) and the axial family by
   extracting their boundary-word response equations;
3. use those equations to force active-pair families, and only then impose
   \(F=q^{[2]}\), \(q^{[3]}=0\).

Any successful classification must use the factors at both \(o\) and \(t\);
repeating the five-site box argument after forgetting them cannot distinguish
the whole field-only support space.
