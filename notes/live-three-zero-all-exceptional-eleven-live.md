# The all-exceptional eleven-live three-zero response is injective

## 1. Outcome

The third split layer \(t=r+4\) is closed in
[live-three-zero-third-split-distinct-beta.md](live-three-zero-third-split-distinct-beta.md)
and
[live-three-zero-third-split-collision-beta.md](live-three-zero-third-split-collision-beta.md).
The first case of the next layer is

\[
                 r=6,\qquad |U|=11,\qquad t=11=r+5.             \tag{1}
\]

Thus all eleven live sites are exceptional and the only active star
sites are the two type-\(10\) centres.

**Theorem 1.1 (all-exceptional eleven-live injectivity).**  On the full
structurally admissible locus, with arbitrary repetitions among the
eleven exceptional beta values, the complete six-column zero-star
response has rank six.  Hence every residual nonzero-to-\(z_0\) block
vanishes and \(z_0\) is isolated in \(G_3(q)\), a contradiction.

The proof uses the double-confluent Borchardt quotient on the collision
strata.  It does not pass from distinct beta values to collisions by
density.

## 2. The isolated-centre pivots

Let \(E\) be the eleven exceptional labels and let \(c_1,c_2\) be the
type-\(10\) centres.  Fix a partition

\[
                 E=R\sqcup L\sqcup B,\qquad
                 |R|=4,\quad |L|=5,\quad |B|=2.                 \tag{2}
\]

Give \(B\) colour \(2\) and use it as the unique marked pair.  To
isolate row zero at one centre, give \(L\) and the target colour zero,
and give \(R\) and the other centre colour one.  Removing the marked
pair and target star leaves balanced shores of size five.

Let \({\cal C}_{L\mid R}\) be the \(5\times5\) Cauchy matrix with row
parameters \(\{\nu_\ell:\ell\in L\}\) and column parameters

\[
                         \{\nu_c:c\in R\}\sqcup\{\mu\}.          \tag{3}
\]

The exact isolated pivot is

\[
                         C_{L\mid R}
                         =2h_{01}^{\,5}
                           \operatorname {per}{\cal C}_{L\mid R}. \tag{4}
\]

Swapping binary colours gives row one, and giving the target centre
colour \(2\) gives row two with the same pivot.  Thus the six selected
rows form

\[
                              C_{L\mid R}I_6.                    \tag{5}
\]

The direct coordinate-factor term is exactly zero in these rows because
\(B_{22}=0\).  The complete evaluator, including nonzero direct terms
on other source rows, is audited separately.  It remains to show that
some pivot (4) is nonzero.

## 3. Why incidence alone no longer finishes

Put

\[
 H_{ic}={\nu_i+\mu\over\nu_i+\nu_c}.
\]

Expanding the single common-\(\mu\) column in (4), and removing a
nonzero factor independent of the summation set, gives

\[
 G_{L\mid R}
   =\sum_{\substack{J\subset L\\|J|=4}}
        \operatorname {per}H[J,R].                              \tag{6}
\]

For disjoint four-sets \(J,R\), the symmetrically rescaled variable is

\[
 X_{\{J,R\}}
 =\left(\prod_{c\in R}(\nu_c+\mu)\right)
      \operatorname {per}H[J,R]
 =\left(\prod_{i\in J\sqcup R}(\nu_i+\mu)\right)
      \operatorname {per}
       \left({1\over\nu_i+\nu_c}\right)_{i\in J,\ c\in R}.       \tag{7}
\]

The last Cauchy permanent makes \(X\) symmetric in \(J,R\).  Multiplying
(6) by the nonzero \(R\)-product turns it into a zero-one incidence
equation in the \(X\)'s.

There are \(5775\) unordered disjoint-four-set variables and \(6930\)
ordered-\(R\), marked-pair equations.  Exact sparse elimination over
\(\mathbb F_{1009}\) gives rank \(5313\).  Thus the previous nine-live
full-column modular certificate does not recur here; the Cauchy
relations must be used.

For orientation, if the incidence equations did force every \(X\) to
zero, a local permanental descent would finish.  Fixing \(R\) gives a
nonzero-entry \(7\times4\) matrix.  Normalize its last column to one.
Expansion along that column and invertibility of
\(W_{4,3}(7)\) force all three-row permanents of the first three
columns to vanish.  Normalizing once more, the full-column rank of
\(W_{3,2}(7)\) gives the same pair-form contradiction as in the
nine-live proof.  The exact audit verifies both inclusion ranks.

## 4. A double-confluent initial-jet lemma

Suppose, toward a contradiction, that every pivot (4) vanishes.  Fix a
possibly repeated-value four-set \(R\), and let

\[
                         N=E\setminus R,\qquad |N|=7.            \tag{8}
\]

Group the values in \(R\) into distinct classes \(y\) of multiplicities
\(r_y\).  The common value \(\mu\) has column multiplicity one.  For a
row value \(x\) of multiplicity \(q_x\) in \(L\), form the divided
mixed derivatives

\[
 {1\over s!\,j!}
 \partial_x^s\partial_y^j{1\over x+y},
 \qquad
 {1\over s!\,j!}
 \partial_x^s\partial_y^j{1\over(x+y)^2},                       \tag{9}
\]

for \(0\le s<q_x\) and \(0\le j<r_y\), together with the ordinary
\(\mu\) column.  Call the resulting denominator and numerator matrices
\({\cal E}^{H}_L\) and \({\cal A}^{H}_L\).  Simultaneous row and column
confluence in Borchardt's identity gives the exact quotient

\[
 \operatorname {per}{\cal C}_{L\mid R}
             ={\det{\cal A}^{H}_L\over\det{\cal E}^{H}_L}.       \tag{10}
\]

The double-confluent Cauchy denominator is nonzero on the structural
locus.

Form the \(7\times5\) global numerator jet matrix
\({\cal A}^{H}_N\).  In each row-value class, call the highest jet its
top row.  Deleting one label from each of two distinct classes deletes
exactly their two top rows.  Hence every corresponding maximal minor
vanishes.

**Lemma 4.1 (singleton initial-jet rank).**  If \(N\) has a singleton
value class, then

\[
                         \operatorname {rank}{\cal A}^{H}_N<5.  \tag{11}
\]

If the rank were five, its two-dimensional left kernel would have all
Plücker coordinates on pairs of top rows equal to zero.  Its projection
onto the top coordinates would have rank at most one, so some nonzero
left-kernel vector would be supported on the non-top rows.

Those non-top rows are independent.  To see this without a generic
minor, interpret such a row relation as the rational function of \(y\)

\[
 G(y)=\sum_{\substack{x:q_x\ge2\\0\le s\le q_x-2}}
       z_{x,s}{1\over s!}\partial_x^s{1\over(x+y)^2}.            \tag{12}
\]

Its principal parts make \(G\ne0\).  The relation against all five
column jets says that \(G\) has five zeros counting multiplicity.  A
common denominator for (12) is

\[
                    \prod_{x:q_x\ge2}(x+y)^{q_x}.               \tag{13}
\]

Because \(N\) contains a singleton, at most six of its seven labels
belong to repeated classes.  The numerator in (12) therefore has degree
at most four, and cannot have five zeros.  This proves the lemma.

Once (11) holds, a nonzero column dependence gives a rational function
\(F_R(x)\) vanishing at the seven labels of \(N\), with their full
Hermite multiplicities.  If \(m_R\) is the number of distinct
exceptional values represented in \(R\), its denominator has degree

\[
                   \sum_y(r_y+1)+2=6+m_R,                      \tag{14}
\]

and its numerator has degree at most \(4+m_R\).  In particular, if
\(m_R\le2\), this degree is at most six, contradicting the seven roots.

## 5. Every genuine collision is closed

There are three cases.

### 5.1 A value occurs at least four times

Choose four equal-valued labels for \(R\), with common value \(a\).
The four columns in (6) are identical.  Setting

\[
                           h_i={\nu_i+\mu\over\nu_i+a}\ne0,
\]

gives

\[
                         G_{L\mid R}=4!\,e_4(h_i:i\in L).        \tag{15}
\]

These quantities cannot vanish for all two-label deletions
\(L=N\setminus B\).  Indeed, if all \(h_i\) are equal, (15) is visibly
nonzero.  Otherwise choose \(h_j\ne h_k\).  Comparing the deletions
\(\{i,j\}\) and \(\{i,k\}\) gives

\[
             (h_k-h_j)e_3(h_u:u\notin\{i,j,k\})=0.              \tag{16}
\]

On the remaining five-label set \(W\), all one-deletion \(e_3\)'s
vanish.  Summing them first forces \(e_3(W)=0\), and then division by
the nonzero \(h_i\)'s successively forces all one-deletion
\(e_2\)'s and \(e_1\)'s to vanish.  Finally \(h_i=0\), a contradiction.

### 5.2 At least two repeated classes, or one triple class

Assume all multiplicities are at most three, excluding for the moment
the pattern consisting of one double class and nine singletons.
One can select four labels from at most two value classes so that the
seven-label complement \(N\) contains a singleton:

- if a triple class and another repeated class exist, take two labels
  from each, leaving one label of the triple;
- if the triple is the only repeated class, take all three of it and
  one singleton;
- if there is no triple but at least two double classes, take both
  labels from two doubles.  Since eleven is odd, an untouched singleton
  remains.

Thus \(m_R\le2\) and Lemma 4.1 applies.  The degree bound after (14)
then gives the immediate seven-root contradiction.  This covers all
fourteen intermediate multiplicity partitions.

### 5.3 Exactly one double class

Let the repeated value be \(a\), and choose

\[
                            R=\{a,a,b,c\},                       \tag{17}
\]

where \(b,c\) are singleton values.  The complement \(N\) consists of
seven distinct singleton values, so all ordinary maximal minors vanish
and the global matrix has rank below five.  Here (14) gives numerator
degree at most seven.  Its seven roots force

\[
                         Q_R(x)=\lambda P_R(x),\qquad
 P_R(x)=\prod_{i\in N}(x-\nu_i).                                \tag{18}
\]

There is no simple-pole basis term at \(-b\).  The zero-residue
condition there is

\[
 -\sum_{i\in N}{1\over b+\nu_i}
 = {2\over\mu-b}+{3\over a-b}+{2\over c-b}.                     \tag{19}
\]

Replace \(c\) successively by two other singleton values \(d,e\).
Subtracting (19) for \(c\) and \(d\) gives

\[
 {1\over b+c}-{1\over b+d}
       =2\left({1\over c-b}-{1\over d-b}\right),                \tag{20}
\]

or

\[
                  \rho_b(c)\rho_b(d)=2,\qquad
                  \rho_b(x)={x-b\over x+b}.                    \tag{21}
\]

The comparison with \(e\) gives
\(\rho_b(c)\rho_b(e)=2\).  If \(b=0\), (21) says \(1=2\); otherwise
\(\rho_b\) is injective and forces \(d=e\).  Both are impossible.

## 6. The distinct-value quartic obstruction

It remains to treat eleven distinct exceptional values.  This argument
already works uniformly at \(t=r+5\) for every \(r\ge6\).

For a distinct four-set \(R\), all \(5\times5\) numerator minors on the
seven nodes in \(N\) vanish, so a nonzero column dependence exists.  Its
denominator is

\[
                    D_R(x)=(x+\mu)^2
                            \prod_{c\in R}(x+\nu_c)^2,           \tag{22}
\]

of degree ten.  The numerator has degree at most eight and has the
seven roots in \(N\).  Therefore

\[
                    Q_R(x)=P_R(x)\ell_R(x),\qquad
                    \deg\ell_R\le1,\quad \ell_R\ne0.            \tag{23}
\]

For the uniform layer, the exponent \(2\) on \(x+\mu\) in (22) becomes
\(k+1\); the degree excess and the linear factor in (23) are unchanged.

Fix three exceptional values \(a,b,c\), and let
\(R_x=\{a,b,c,x\}\) as \(x\) ranges over every other exceptional value.
Write

\[
 A_a=-\sum_{i\ne a}{1\over a+\nu_i}-{k+1\over\mu-a},\qquad
 \psi(a,x)={1\over a+x}-{2\over x-a}
           =-{x+3a\over x^2-a^2},                              \tag{24}
\]

and absorb the two fixed-core contributions into a constant \(U_a\):

\[
                         Y_a(x)=U_a+\psi(a,x).                  \tag{25}
\]

If \(\ell_{R_x}(z)=u_xz+v_x\), the zero-residue equation at \(-a\),
written without dividing by \(\ell_{R_x}(-a)\), is

\[
                   u_x+Y_a(x)(v_x-au_x)=0.                     \tag{26}
\]

The analogous equation at \(-b\) has a constant \(U_b\).  A common
nonzero pair \((u_x,v_x)\) requires

\[
 Y_b(x)-Y_a(x)+(b-a)Y_a(x)Y_b(x)=0.                            \tag{27}
\]

After multiplying by \((x^2-a^2)(x^2-b^2)\), equation (27) is a
polynomial \(K_{a,b}(x)\) of degree at most four.  At \(r=6\) it
vanishes at the eight distinct exceptional values outside
\(\{a,b,c\}\); uniformly it has \(p+3\ge8\) roots.  Hence it would have
to vanish identically.

This is impossible.  Writing \(U=U_a,V=U_b\), the \(x^3\) and \(x^4\)
coefficients are

\[
                 (a-b)(U+V),\qquad UV(b-a)-U+V.                 \tag{28}
\]

Since \(a\ne b\), identity vanishing first gives \(V=-U\), and then
either \(U=0\) or \(U=-2/(b-a)\).  In the first case the polynomial is

\[
             2(a-b)\bigl(x^2-(a+b)x-3ab\bigr),                 \tag{29}
\]

and in the second it is

\[
            -4(a-b)\bigl(x^2+(a+b)x+3ab\bigr).                 \tag{30}
\]

Neither can be the zero polynomial.  This closes the distinct stratum
and completes the proof of Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_all_exceptional_eleven_live.py](../computations/verify_live_three_zero_all_exceptional_eleven_live.py)
reconstructs the complete selected response and verifies the diagonal
minor (5), while separately exercising a nonzero direct response term.
It checks an exact five-square double-confluent Borchardt quotient,
the deletion identities in (16), all fourteen intermediate collision
partitions, the one-double residue subtraction, and the quartic
coefficients (28)--(30).

It also reports the \(6930\times5775\) incidence rank over
\(\mathbb F_{1009}\) and verifies the two local inclusion ranks used in
Section 3.

The uniform continuation, including every collision stratum, is
[live-three-zero-fourth-split-layer.md](live-three-zero-fourth-split-layer.md).
