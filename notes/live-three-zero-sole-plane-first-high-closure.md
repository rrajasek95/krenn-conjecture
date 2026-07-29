# The first sole-plane high-split response is injective

## 1. Outcome

Continue from
[live-three-zero-extra-singular-exact-frontier.md](live-three-zero-extra-singular-exact-frontier.md).
The first sole-extra-plane case not covered by the subset arguments is

\[
                         (r,t)=(3,6).                            \tag{1}
\]

Thus all six live sites are exceptional.  The heavy-class theorem says
that no exceptional beta value occurs three times, so the only equality
profiles are

\[
                   2^3,\qquad 2^2 1^2,\qquad
                   2 1^4,\qquad 1^6.                            \tag{2}
\]

**Theorem 1.1 (first high-split sole-plane closure).**  For every profile
in (2), every structurally admissible choice of exceptional beta values,
and every source-side row plane of the sole extra site, the complete
nine-column residual response has rank nine.  The statement is independent
of the direct \(B_{01}\) scale.  Hence the residual shared zero has no
rank-three neighbour, and (1) is impossible.

The proof uses three finite families of literal \(3\)-by-\(3\) Cauchy
permanents.  Exact localized ideals over \(\mathbb Q\), rather than a
generic determinant or a finite-field search, prove that the required
pivots cannot vanish simultaneously.  Singleton beta classes are allowed
to have value zero.

## 2. Response and the three permanent families

Normalize

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 \mu=1,\qquad P_i=I\ (i\in E),\qquad
 P_c=P_d=D=\operatorname {diag}(1,1,0),                         \tag{3}
\]

where \(E=\{0,\ldots,5\}\) is the exceptional live shore, with beta
values \(\nu_i\), and \(e\) is the sole extra site.  The active response
columns are precisely the three output rows at each of \(c,d,e\).  Every
exceptional live star is already zero by

\[
                         (\nu_i-1)q_{i z_0}=0.                   \tag{4}
\]

For two tuples \(X=(x_1,x_2,x_3)\) and \(Y=(y_1,y_2,y_3)\), put

\[
                     \mathcal C(X\mid Y)
       =\operatorname {per}\left({1\over x_i+y_j}\right)_{i,j=1}^3.
                                                                    \tag{5}
\]

All denominators below are structural denominators.  Define:

1. for \(m\in E\) and
   \(E\setminus\{m\}=L\sqcup R\), \(|L|=3,|R|=2\),

   \[
       P_{m;L\mid R}=\mathcal C(\nu_L\mid(1,\nu_R));             \tag{6}
   \]

2. for \(B\subset E\), \(|B|=2\), and
   \(E\setminus B=L\sqcup R\), \(|L|=|R|=2\),

   \[
       R_{B;L\mid R}=\mathcal C((1,\nu_L)\mid(1,\nu_R));        \tag{7}
   \]

3. for \(B\subset E\), \(|B|=2\), and
   \(E\setminus B=L\sqcup\{o\}\), \(|L|=3\),

   \[
       S_{B;L,o}=\mathcal C(\nu_L\mid(1,1,\nu_o)).              \tag{8}
   \]

The letters indicate their uses below: \(P\) is the one-common-column
pivot, \(R\) has one common value on each shore, and \(S\) has two equal
common columns on one shore.

## 3. Exact noncancellation on all four profiles

For a profile with distinct class variables \(x_0,\ldots,x_{s-1}\) and
multiplicities \(m_i\), use the localizer

\[
 \Delta=
 \prod_i(x_i-1)(x_i+1)
 \prod_{i<j}(x_i-x_j)(x_i+x_j)
 \prod_{m_i\ge2}x_i.                                            \tag{9}
\]

The first factors record exceptional values and live--centre
denominators, the pair factors record the exact equality profile and
nonopposite classes, and the final factors are present only when two
labels share a class.  In particular, no factor \(x_i\) is inserted for
a singleton class: such a beta value may be zero.

Substitute the profile into (6)--(8), clear the structural denominators,
and retain the distinct primitive numerators.  Singular's exact
characteristic-zero `modStd` computation gives

\[
 \langle\operatorname {num}(F):F\in\mathcal F\rangle
       +\langle1-\tau\Delta\rangle=\langle1\rangle              \tag{10}
\]

for each \(\mathcal F\in\{\mathcal P,\mathcal R,\mathcal S\}\) and each
profile.  The complete ledger is

\[
\begin{array}{c|ccc}
 \text{profile}&|\mathcal P|&|\mathcal R|&|\mathcal S|\\ \hline
 2^3       &15&12&15\\
 2^2 1^2   &24&17&24\\
 2 1^4     &38&27&38\\
 1^6       &60&45&60
\end{array}                                                       \tag{11}
\]

Therefore at every admissible point at least one member of each of the
three families is nonzero.  These are three separate existence statements;
their marked sets and partitions need not coincide.

## 4. Every noncoordinate row plane

Let \(R_e=\operatorname {row}P_e\).  Suppose first that

\[
                  R_e\ne\langle e_0,e_1\rangle .                \tag{12}
\]

Choose \(p=(p_0,p_1,p_2)\in R_e\) with \(p_2\ne0\), contract the output
at \(e\) to \(p\), give one exceptional label \(m\) output colour \(2\),
and use source \(22\).  No other label is given a nonzero source-2 row.
Thus \(\{m,e\}\) is the unique marked pair and its marked coefficient is
\(2p_2\).  The direct term is absent because \(B_{22}=0\).

Choose a nonzero pivot (6).  To isolate row zero at \(c\), give \(L\)
colour zero and give \(d\sqcup R\) colour one.  Removing \(m,e,c\)
leaves a balanced \(3\)-against-\(3\) binary cofactor, whereas moving the
star to \(d\) leaves shore sizes four and two.  Modulo (4), the response is

\[
                       2p_2P_{m;L\mid R} Z_{c,0}=0.              \tag{13}
\]

Swapping binary colours gives the same permanent by transposition and
kills \(Z_{c,1}\).  Giving \(c\) its zero local row kills every off-star
cofactor and gives the same pivot for \(Z_{c,2}\).  Interchanging \(c,d\)
kills all six centre rows.

Now choose a nonzero pivot (7).  Give the two labels of \(B\) colour two,
give \(c\sqcup L\) colour zero, and give \(d\sqcup R\) colour one.  Contract
the output at \(e\) by an arbitrary covector \(\eta\).  In the star-at-\(e\)
term, \(B\) is the unique marked pair and

\[
                     2R_{B;L\mid R}\,\eta^{\mathsf T}q_{e z_0}=0.\tag{14}
\]

Terms at \(c,d\), including those in which \(e\) participates in another
marked pair, are retained but vanish by (13); exceptional-star terms vanish
by (4).  Since \(\eta\) is arbitrary, (14) kills the full extra block.

## 5. The coordinate row plane

It remains to take

\[
                         R_e=\langle e_0,e_1\rangle .            \tag{15}
\]

An output change puts \(P_e=D\), so \(c,d,e\) are three symmetric active
binary-coordinate centres.  Choose a nonzero pivot (8).  Give \(B\) colour
two.  For a target \(v\in\{c,d,e\}\), give \(v\sqcup L\) colour zero and
give the other two active sites together with \(o\) colour one.  Source
\(22\) forces the marked pair \(B\).  Only the star at \(v\) leaves a
balanced cofactor, and the literal response is

\[
                              2S_{B;L,o}Z_{v,0}=0.               \tag{16}
\]

Swapping the two binary colours gives the transpose of (8) and kills
\(Z_{v,1}\).  This works for every target and both orientations, so all six
binary active rows vanish.

Finally choose a nonzero pivot (7).  Give a target \(v\) its zero local
row, put the other two active sites on opposite binary shores, and split
the four unmarked exceptional labels as \(L\sqcup R\).  Every off-star
cofactor contains the zero row at \(v\), while the target coefficient is

\[
                              2R_{B;L\mid R}Z_{v,2}=0.            \tag{17}
\]

This kills the remaining three rows and proves Theorem 1.1 on (15).

## 6. Kernel charts, direct scale, and exact audit

The usual three row-plane charts may be written

\[
 \begin{array}{c|c}
 01&\begin{pmatrix}1&0&a\\0&1&b\end{pmatrix}\\[2mm]
 12&\begin{pmatrix}a&1&0\\b&0&1\end{pmatrix}\\[2mm]
 02&\begin{pmatrix}1&a&0\\0&b&1\end{pmatrix}.
 \end{array}                                                     \tag{18}
\]

The \(12\) and \(02\) charts have a literal row with nonzero source-2
entry.  In the \(01\) chart, row zero works when \(a\ne0\), row one works
when \(a=0,b\ne0\), and \((a,b)=(0,0)\) is exactly (15).  Thus Sections
4--5 cover all three charts without a missing divisor branch.

[verify_live_three_zero_sole_plane_first_high_closure.py](../computations/verify_live_three_zero_sole_plane_first_high_closure.py)
reconstructs the actual nine-site marked-matching response.  It checks all
six noncoordinate centre rows, the contaminated triangular cleanup (14),
all targets and both binary orientations in (16)--(17), the three chart
cover, every denominator factor in (9), and every admissible singleton
zero-beta boundary.  It then reruns all twelve exact localized ideals in
(10).  The arbitrary direct scale is a symbolic variable in the response;
every selected row uses source \(22\), so its coefficient is identically
zero rather than specialized.

[explore_live_three_zero_sole_plane_first_high_permanents.py](../computations/explore_live_three_zero_sole_plane_first_high_permanents.py)
is the smaller profile/family-level ideal driver.  The earlier
[explore_live_three_zero_sole_plane_first_high_response.py](../computations/explore_live_three_zero_sole_plane_first_high_response.py)
provides independent full-rank reconnaissance on every chart and profile,
but no finite-field result is used in the proof.
