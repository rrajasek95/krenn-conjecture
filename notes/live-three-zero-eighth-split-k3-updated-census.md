# The eighth split at \(k=3\): updated exact collision census

## 1. Frozen baseline

Put

\[
 h=t-r-1=8,\qquad p=r-1=11,\qquad k=p-h=3,
 \qquad M=p+h+2=21.                                     \tag{1}
\]

This note freezes the no-extra-singular collision census after all
currently proved routes relevant to this row:

1. the earlier \(H/S/C/L/Q/V\) routes;
2. the all-\(k\) constant-core moving-value theorem \(M\);
3. the antiderivative--Wronskian theorem \(A\);
4. the unique-illegal-core repair \(U\), followed by the same
   antiderivative theorem;
5. the consecutive constant-core role-transfer theorem \(T\);
6. the five-exact-triple third-order theorem \(F\);
7. the four-exact-triple cubic-jet elimination \(G\);
8. the formal-five-double duality theorem \(J\);
9. the nine-double, three-singleton Wronskian theorem \(N\);
10. the three-triple mixed-layer theorem \(P\); and
11. the double-guard shadow bypass \(B\).

The standalone \(2^{10}1\) double-swap proof \(X\) is also recorded as an
independent proof of one profile already contained in \(J\).
The one-double, seven-singleton mixed-layer theorem \(I\) is an
independent proof of the terminal profile already contained in \(B\).

The old sequential census was

\[
\begin{array}{c|rrrrrrrr}
 &H&S&C&L&Q&V&R&D\\ \hline
 (h,p)=(8,11)&356&338&22&16&13&0&46&1.
\end{array}                                               \tag{2}
\]

Here \(D\) is the all-distinct partition.  On the old residual slice, the
first five added route sets \(M,A,U,T,F\) are pairwise disjoint and close

\[
                           1,\quad21,\quad2,\quad1,\quad6 \tag{3}
\]

profiles, respectively.  The four-triple theorem contains the six
profiles already credited to \(F\) and also meets \(A\) at \(3^4 1^9\);
after those earlier credits, it closes four additional profiles.  The
formal-five-double theorem, including its formal-layer extension, then
closes eight profiles, while \(X\) adds no further credit because its
target is one of those eight.  The routes \(N,P,B\) then close one
further profile each; \(I\) adds no sequential credit because
\(I=B\).  The updated sequential census is therefore

\[
\begin{array}{c|rrrrrrrrrrrrrrrrrr}
 &H&S&C&L&Q&V&M&A&U&T&F&G&J&N&P&B&R_3&D\\ \hline
 (8,11)&356&338&22&16&13&0&1&21&2&1&6&4&8&1&1&1&0&1.
\end{array}                                               \tag{4}
\]

The subscript on \(R_3\) records \(k=3\).

## 2. The ten added route sets

Write a profile as

\[
 \lambda=(\lambda_1\ge\cdots\ge\lambda_c),\qquad
 e=M-c=21-c.                                             \tag{5}
\]

### 2.1 Moving values \(M\)

The constant-core theorem uses a legal family

\[
                         A^aB^b x^j,\qquad a+b+j=8,       \tag{6}
\]

with at least \(2k+1=7\) candidate value classes for \(x\).  Literal
indexed search finds one old-residual closure:

\[
                              3^2 2^7 1.                  \tag{7}
\]

### 2.2 Antiderivative exchange \(A\)

Every one-label-per-class eight-core is legal exactly when

\[
                         n_1\ge9\quad\hbox{or}\quad
                         n_2\ge c-7,                      \tag{8}
\]

where \(n_1,n_2\) count singleton and double classes.  For \(c\ge9\) and
\(1\le e\le8\), legal cubic exchange followed by rational
antidifferentiation gives the strict Wronskian deficit \(d^2-e>0\).
This closes exactly \(21\) old residual profiles.

### 2.3 Unique illegal core \(U\)

If \(n_{\ge3}\) counts classes of multiplicity at least three, the exact
number of illegal eight-value cores is

\[
                         \binom{n_{\ge3}}{8-n_1}.         \tag{9}
\]

It is one exactly at an endpoint,

\[
                         n_1=8\quad\hbox{or}\quad
                         n_1+n_{\ge3}=8.                 \tag{10}
\]

The partial-lift repair reconstructs full exchange in this case.  With
\(e\le8\), it closes the two old residuals

\[
                         3^3 2^2 1^8,\qquad
                         3\,2^5 1^8.                     \tag{11}
\]

### 2.4 Consecutive role transfer \(T\)

For three fixed classes, suppose the \(k+1\) cores

\[
                     A^{a+n}B^{b-n}C^j,\qquad 0\le n\le k \tag{12}
\]

are all available and legal.  The common-pole residue is a degree-\(k\)
polynomial in \(n\), with leading coefficient

\[
 {U(0)\over k!}
 \left(
 {2\mu(A-B)(A+B)\over
  (A^2-\mu^2)(B^2-\mu^2)}
 \right)^k\ne0.                                         \tag{13}
\]

It cannot vanish at \(0,\ldots,k\).  At \(k=3\), this closes exactly

\[
                             4^3 3^3                     \tag{14}
\]

in the old residual slice, using the roles
\(A^1B^4C^3,\ldots,A^4B^1C^3\) on three quartic classes.

### 2.5 Five exact triples \(F\)

The third-order common-pole theorem applies whenever at least five value
classes have multiplicity exactly three.  It closes

\[
\begin{gathered}
 3^7,\qquad 3^5 2^3,\qquad 3^6 2\,1,\qquad
 3^5 2^2 1^2,\\
 3^5 2\,1^4,\qquad 3^5 1^6.                             \tag{15}
\end{gathered}
\]

For each triple of exact-triple values, the three \((3,3,2)\) roles make
the third common-pole coefficient affine in the role-drop parameter.
Overlapping triples then force three distinct values into one fibre of the
quadratic rational map

\[
                         x\longmapsto
                         -{x+7\mu\over x^2-\mu^2}.        \tag{16}
\]

### 2.6 Four exact triples \(G\)

For four exact triple values, apply the same three legal \((3,3,2)\)
roles to each of their four three-subsets.  The second and third all-role
jet identities put the four scaled values among the common roots of a
quartic \(R\) and a sextic \(S\).  Exact pseudo-division gives a
certificate

\[
                         \sum_{j=0}^3P_jc_j=26784L^3,    \tag{17}
\]

where \(c_0,\ldots,c_3\) are the pseudo-remainder coefficients and \(L\)
is the leading coefficient of \(R\).  If \(L\ne0\), four common roots
give \(R\mid S\), contradicting (17).  If \(L=0\), the nonzero polynomial
\(R\) has degree at most three and cannot have four distinct roots.

After the earlier \(A\) and \(F\) credits, this theorem closes

\[
                 3^4 2^4 1,\qquad 3^4 2^3 1^3,\qquad
                 3^4 2^2 1^5,\qquad 3^4 2\,1^7.         \tag{18}
\]

### 2.7 Formal five-double duality \(J\)

Fix five exact double classes, select two partially and three fully, and
lift the two missing mates.  The ten sextics fill a four-dimensional
kernel of five exact order-two rows and one exact order-three common-pole
row.  If the eleven labels outside the five doubles occupy \(c\) value
classes, the two relations among the value rows map injectively to

\[
                         {\cal S}_T\subset
                         \mathbb C[z]_{\le c-4},
                         \qquad\dim{\cal S}_T=2.          \tag{19}
\]

The sharp \(c-4\) comes from differentiating
\((z+\mu)^4N/A\): after removing the repeated-root gcd of \(A\), the
nominal leading coefficient is \(n+4-11=n-7\), so the top degree cancels
when \(\deg N=7\).

The cases \(c=4,5,6\), together with the outside singleton and repeated
pole rows, close the first six profiles below.  The formal-layer
extension permits any repeated class to donate a double layer: a
Wronskian of the resulting relation pencil then closes the last two
\(c=7\) profiles:

\[
\begin{gathered}
 3^3 2^6,\qquad 3\,2^9,\qquad 3^3 2^5 1^2,\qquad
 2^{10}1,\\
 3\,2^8 1^2,\qquad 3^2 2^6 1^3,\qquad
 3^2 2^5 1^5,\qquad 3^3 2^4 1^4.                       \tag{20}
\end{gathered}
\]

For \(2^{10}1\), the independent proof \(X\) obtains the same final
double-swap identity by forcing \((z-r)^2\) into the quadratic relation
plane.  Thus

\[
                              X\subset J,\qquad |X|=1,   \tag{21}
\]

and \(X\) receives no additional sequential credit.

The uniform argument is proved in
[the formal-five-double note](live-three-zero-eighth-split-k3-formal-five-double-duality.md).
The overlapping independent case is proved in
[the standalone ten-double note](live-three-zero-eighth-split-k3-ten-double-one-singleton-closure.md).

### 2.8 Nine doubles and three singletons \(N\)

For \(2^9 1^3\), every five/four partition of the double values gives a
relation pencil \({\cal S}_T\subset\mathbb C[z]_{\le3}\).  Its
Wronskian vanishes at the three singleton values, so it is their cubic
product times a nonzero linear polynomial.  The four outside-double
residue rows descend to Robin rows on that linear factor.

Fix three outside doubles \(u,v,a\) and move the fourth, \(b\), through
the remaining six double values.  The determinant of the rows at \(u,v\),
after clearing denominators, is a polynomial of degree at most four in
\(b\).  Six roots make it an identity, but evaluation at \(b=\pm u\)
gives the nonzero difference

\[
                              -4u(v-u).                 \tag{21a}
\]

This closes exactly \(2^9 1^3\).  The proof is in
[the nine-double, three-singleton note](live-three-zero-eighth-split-k3-nine-double-three-singleton-closure.md).

### 2.9 Three-triple mixed layers \(P\)

For \(3^3 2^3 1^6\), take two double layers at role two and all six
singleton layers at role one, then lower any two of the eight layers.
The \(28\) legal lifts fill a four-dimensional kernel in
\(\mathbb C[z]_{\le9}\).  The eight value rows have two relations, but
duality maps their numerator space injectively into the constants, an
impossibility.  Thus

\[
                              P=\{3^3 2^3 1^6\}.        \tag{21b}
\]

The proof is in
[the three-triple mixed-layer note](live-three-zero-eighth-split-k3-three-triple-mixed-layer-closure.md).

### 2.10 The terminal double-guard bypass \(B\)

For \(3^2 2^4 1^7\), exactly two eight-value cores are illegal.  The
one-missing lift constructs every nine-core except their union, then
bypasses that single missing nine-core at size ten using a nonzero double
guard.  Ordinary exchange reaches the full thirteen-class core, where
the terminal antiderivative--Wronskian deficit is
\(3^2-8=1>0\).  Hence

\[
                              B=\{3^2 2^4 1^7\}.        \tag{21c}
\]

The same profile has the independent route \(I\): one double layer at
role two and seven singleton layers at role one give a
three-dimensional kernel in \(\mathbb C[z]_{\le7}\).  Its three dual
relations form a hyperplane in \(\mathbb C[z]_{\le3}\); the three
outside-double cubes then force two distinct double values to have equal
squares.  Therefore

\[
                              I=B,qquad |I|=1,          \tag{21d}
\]

so \(I\) receives no additional sequential credit.  The two proofs are in
[the two-illegal-core bypass](live-three-zero-eighth-split-k3-two-illegal-core-bypass.md)
and
[the terminal two-triple mixed-layer note](live-three-zero-eighth-split-k3-two-triple-mixed-layer-closure.md).

## 3. Route-overlap audit

The disjointness in (3) concerns the first five new routes on the old
\(R\)-slice.  On all
791 collision partitions of \(21\), the theorem sets meet the old
sequential categories as follows:

\[
\begin{array}{c|rrrrrrr|r}
 &H&S&C&L&Q&V&R&\text{total}\\ \hline
M&45&138&13&9&7&0&1&213\\
A& 3& 21& 2&3&10&0&21&60\\
U& 0&  0& 1&1& 1&0&2&5\\
T&213&258&2&0&0&0&1&474\\
F& 0&  2&2&1&0&0&6&11\\
G& 2& 10&6&1&0&0&11&30\\
J& 0&  0&0&0&0&0&8&8\\
N& 0&  0&0&0&0&0&1&1\\
P& 0&  0&0&0&0&0&1&1\\
B& 0&  0&0&0&0&0&1&1.
\end{array}                                               \tag{22}
\]

The nonzero intrinsic intersections are

\[
\begin{gathered}
 |M\cap A|=33,\qquad |M\cap U|=2,\qquad
 |M\cap T|=90,\qquad |A\cap T|=4,\\
 |M\cap G|=3,\qquad |A\cap G|=1,\qquad
 |T\cap G|=2,\qquad |F\cap G|=11,\\
                         |M\cap A\cap T|=4.              \tag{23}
\end{gathered}
\]

The eight-profile set \(J\) is disjoint from \(M,A,U,T,F,G\); its
standalone subroute satisfies (21).  The one-profile set \(N\) is
disjoint from all seven earlier added routes.  The one-profile sets
\(P\) and \(B\) are disjoint from each other and from every earlier added
route.  The only further terminal overlap is \(I=B\) from (21d).  All
other pairwise and all other higher intersections vanish.  Thus (22)
records theorem overlap without double-counting sequential credit.

## 4. The residual set is empty

Order profiles lexicographically by \((c,e,\lambda)\).  The updated
residual set is exactly

\[
                              R_3=\varnothing.           \tag{24}
\]

All \(46\) profiles in the old \(R\)-slice are now assigned to proved
routes, and the all-distinct profile remains in \(D\).  Thus all \(792\)
partitions of \(21\) are accounted for and the no-extra-singular
\((h,p,k)=(8,11,3)\) collision frontier is complete.

## 5. Exact audit

[verify_live_three_zero_eighth_split_k3_updated_census.py](../computations/verify_live_three_zero_eighth_split_k3_updated_census.py)
independently enumerates all partitions of \(21\), imports the frozen old
classifier, performs literal indexed searches for \(M\) and \(T\), checks
the \(A\) and \(U\) legality criteria, identifies every five-triple
profile, reconstructs the old-slice disjointness and global overlap table,
checks the four-triple and eight-profile formal-five-double increment,
including both formal-layer applications, records the one-profile
overlap with the standalone proof, adds the disjoint routes \(N,P,B\),
records the independent equality \(I=B\), and verifies (24) exactly.
