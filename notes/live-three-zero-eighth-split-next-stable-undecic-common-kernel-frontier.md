# The eighth split: next stable undecic common-kernel frontier

## 1. Statement

The next two stable profiles after the decic closure are

\[
 (h,k;\lambda)=(8,11;2^{14}1),\qquad
 (h,k;\lambda)=(8,12;2^{15}).                         \tag{1}
\]

Use \(\epsilon=1\) for \(2^{14}1\) and \(\epsilon=0\) for \(2^{15}\).
After fixing four double values, let \(P\) be the remaining double-value
pool.  Then

\[
 p=|P|=11-\epsilon,\qquad N=p+\epsilon=11.             \tag{2}
\]

Every fifth choice again gives a two-plane

\[
 {\cal U}_a=A_a{\cal S}_a\subseteq{\cal K}
 \subseteq\mathbb C[z]_{\leq11},\qquad
 A_a=(z+a)^2(z-a)^3,\qquad \dim{\cal U}_a=2.           \tag{3}
\]

The parity and common-kernel analysis first gives:

1. \(\dim{\cal K}\leq5\), and a five-space is gcd-free;
2. dimensions two, three, and four are impossible;
3. a five-space can survive only when its four-row parity cofactor
   vanishes identically;
4. before the final dimension bound, the only conditional five-space odd
   ranks are
   \[
   \begin{array}{c|c}
   2^{14}1&r_o\in\{4,5\}\\
   2^{15}&r_o\in\{4,5\}.
   \end{array}                                        \tag{4}
   \]

A final fixed-numerator argument improves \(\dim{\cal K}\leq5\) to
\(\dim{\cal K}\leq4\).  Since every fifth choice already supplies the
two-plane (3), while dimensions two through four are impossible, both
profiles in (1) are closed.  The five-space tangent branches retained below
are structural intermediate results, but no longer actual survivors.

## 2. Wronskian ledger

For a gcd-free \(d\)-space, forced finite Wronskian weight minus the
ambient degree cap is

\[
 p(d-2)+\epsilon(d-1)-d(12-d)
                         =d^2-d-2p-\epsilon.           \tag{5}
\]

At \(d=6\), (5) is positive for both profiles, while at \(d=5\) the
available slack is

\[
\begin{array}{c|c|c|c}
\text{profile}&(p,\epsilon)&\text{forced weight}&
 5(12-5)-\text{forced}\\ \hline
2^{14}1&(10,1)&34&1\\
2^{15}&(11,0)&33&2.
\end{array}                                            \tag{6}
\]

A gcd root away from the marked nodes costs at least five units, and the
node gcd corrections cost still more.  Hence a five-space is gcd-free.
If \(C(x)=\prod_{a\in P}(x-a)\) and \(b\) is the singleton value, its
Wronskian has the form

\[
\begin{array}{ll}
2^{14}1:&
 \operatorname {Wr}({\cal K})
   =C(x)^3(x-b)^4S(x),\qquad \deg S\leq1,\\[2mm]
2^{15}:&
 \operatorname {Wr}({\cal K})
   =C(x)^3S(x),\qquad \deg S\leq2,
\end{array}                                            \tag{7}
\]

where part or all of the residual degree may occur at infinity.

The first new ambient phenomenon is already visible in pair
intersections:

\[
 \{F:\ A_aA_b\mid F,\ \deg F\leq11\}
                         =A_aA_b\,\mathbb C[z]_{\leq1}. \tag{8}
\]

This is two-dimensional, rather than the product line of the decic
case.  Thus the old dimension-three/four product-line argument does not
extend verbatim.

Dimension two is nevertheless impossible.  It would make every
\({\cal U}_a\) equal to \({\cal K}\); three choices would then give a
nonzero polynomial divisible by three coprime quintic factors, of degree
at least fifteen.

## 3. Refined parity caps

Write

\[
                         F(z)=E(w)+zO(w),\qquad w=z^2,
\]

where now both \(E\) and \(O\) are quintics in \(w\).  If \(r_o\) is the
odd-projection rank, the sharp degree caps for the Wronskian are

\[
\begin{array}{c|rrrrrr}
d\backslash r_o&0&1&2&3&4&5\\ \hline
3&21&26&27&27&&\\
4&22&29&32&32&32&\\
5&20&29&34&35&35&35.
\end{array}                                            \tag{9}
\]

For example, when \(d=5,r_o=2\), the three-dimensional pure-even kernel
uses degrees \(10,8,6\), while the two quotient vectors use degrees
\(11,9\), giving Wronskian degree \(44-10=34\).

The forced weights for \(d=3,4,5\) are respectively

\[
\begin{array}{c|ccc}
&d=3&d=4&d=5\\ \hline
2^{14}1&12&23&34\\
2^{15}&11&22&33.
\end{array}                                            \tag{10}
\]

Thus (9) immediately excludes \(r_o=0\) for a singleton four-space and
\(r_o=0,1\) for either five-space.

## 4. Dimensions three and four

For a \(d\)-space, the five paired jet rows have rank at most \(d-2\) at
every pool square.

### 4.1 Dimension three is impossible

At \(d=3\), the paired matrix has rank at most one.

- If \(r_o=3\), then \(O,O'\) have rank at most one at all ten or eleven
  squares.  This exceeds the degree-nine Wronskian cap of a three-space
  of quintics.
- If \(r_o=2\), the Wronskian of the two odd quintics has at least ten
  roots but degree at most eight.
- If \(r_o=1\), outside at most two common zeros of \(O_1,O_1'\), every
  member of the two-dimensional pure-even kernel has a triple zero.
- If \(r_o=0\), let \(L={\cal K}^{\perp}\), a three-space in the dual of
  \(\mathbb C[w]_{\leq5}\).  The two lift members give
  \[
   \dim\bigl({\cal K}\cap
      (w-s)^3\mathbb C[w]_{\leq2}\bigr)\geq2.
  \]
  Every two-by-two minor of \(L\) restricted to this moving three-space
  has degree at most six in \(s\), hence vanishes identically.  The span
  of
  \(\bigwedge^2((w-s)^3\mathbb C[w]_{\leq2})\) is the same
  codimension-one space as in the decic proof; its perpendicular
  alternating form has rank six.  No nonzero decomposable bivector can
  lie on that line, so every pair in \(L\) would be proportional, a
  contradiction.

Hence

\[
                         \boxed{\dim{\cal K}\ne3.}     \tag{11}
\]

### 4.2 A four-space is globally tangent

At \(d=4\), the paired matrix has rank at most two.  The same corrected
Wronskian counts as in the decic argument, with the quintic caps eight
and nine, exclude \(r_o=1,2,3\).  The pure-even branch is excluded by
(9) in the singleton profile and by the rank-six alternating-form lemma
in the pure profile.

It remains \(r_o=4\).  Define

\[
 M=*(E'\wedge O\wedge O').
\]

A two-quintic Wronskian has degree at most eight, so
\(\deg M_i\leq12\).  The pool conditions give

\[
 M=\Delta Q,\qquad
 \deg Q_i\leq
 \begin{cases}
 2,&2^{14}1,\\
 1,&2^{15},
 \end{cases}
 \qquad
 \Delta(w)=\prod_{a\in P}(w-a^2).                     \tag{12}
\]

Differentiating the exterior product and contracting with \(O''\) gives

\[
                         M'\mathbin{\cdot}O''
                 =\det(E'',O,O',O'').                 \tag{13}
\]

At a pool node, \(O,O',E''+aO''\) lie in a space of dimension at most
two, so the determinant in (13) vanishes.  Since the roots of \(\Delta\)
are simple, \(Q(s)\cdot O''(s)=0\) at every pool square.  Its degree is
at most five in the singleton profile and four in the pure profile, so

\[
                         Q\mathbin{\cdot}O''=0          \tag{14}
\]

identically.

Cofactor orthogonality and (14), followed by differentiation, make
\(O\) orthogonal to \(Q,Q',Q''\).  Writing
\(Q=q_0+wq_1+w^2q_2\), these equations successively give the fixed
relations

\[
                         Oq_2=Oq_1=Oq_0=0.
\]

Any nonzero \(Q\) would therefore make the four components of \(O\)
linearly dependent.  Hence \(Q=0\), and the exact surviving branch is

\[
 \boxed{\operatorname {rank}
    \begin{pmatrix}E'(w)\\O(w)\\O'(w)\end{pmatrix}\leq2
                         \quad\text{for every }w.}     \tag{15}
\]

This is the new four-space tangent problem: \(O\) is a four-space of
quintics, rather than the quartic hyperplane classified in the decic
tangent lemma.

### 4.3 The rational tangent coefficient closes the four-space

The apparent tangent survivor in fact admits a uniform classification.
Put \(L=E'\).  The two rows \(O,O'\) are independent over
\(\mathbb C(w)\), since the four components of \(O\) are linearly
independent.  Hence (15) has a unique expression

\[
                         L=\alpha O+\beta O',
                 \qquad \alpha,\beta\in\mathbb C(w).                \tag{15a}
\]

Write \(\beta=N/D\) in lowest terms.  The following degree bounds are
the key point:

\[
                         \deg D\leq2,
                 \qquad \deg N\leq3.                               \tag{15b}
\]

Here is an intrinsic proof.  At a finite point \(c\), choose a constant
basis of the four components of \(O\) with vanishing sequence

\[
                         \nu_0<\nu_1<\nu_2<\nu_3.
\]

The homogeneous Wronskian of this four-space of quintics has total
ramification weight eight.  Its local weight is

\[
                         \rho(c)=\sum_{i=0}^3(\nu_i-i).
\]

If \(\beta\) has a pole of order \(m_c\) at \(c\), compare the first two
adapted components in (15a).  With \(t=w-c\),

\[
 L_1-\frac{O_1}{O_0}L_0
   =\beta\left(O_1'-\frac{O_1}{O_0}O_0'\right).
\]

The factor in parentheses has order \(\nu_1-1\), while the left side is
regular.  Therefore

\[
                         m_c\leq\nu_1-1,
                 \qquad \rho(c)\geq3(\nu_1-1).                      \tag{15c}
\]

At infinity put \(t=1/w\),
\(\widehat O=t^5O(1/t)\), and \(\widehat L=t^5L(1/t)\).  Every component
of \(\widehat L\) vanishes at least once.  If
\(e_0<e_1<e_2<e_3\) is the infinity vanishing sequence, then (15a)
becomes

\[
 \widehat L=(\alpha+5t\beta)\widehat O
                 -t^2\beta\,\widehat O_t.
\]

The same two-component comparison, now using the extra zero of
\(\widehat L\), gives

\[
                  \deg N-\deg D\leq e_1,
              \qquad \rho(\infty)\geq3(e_1-1).                     \tag{15d}
\]

If \(m=\deg D=\sum_c m_c\), the total weight eight and
(15c)--(15d) imply

\[
 3m+3(e_1-1)\leq8,
                 \qquad m+e_1\leq3.
\]

This proves (15b).

Call a finite point second-jet bad when
\(\operatorname {rank}(O,O',O'')\leq2\).  In terms of its vanishing
sequence, at most two of the \(\nu_i\) are at most two.  Such a point has
weight at least two, with equality only for
\((0,1,3,4)\).  There are consequently at most four bad pool squares.

At every other pool square \(s=a^2\), differentiate (15a).  The final
paired row lies in \(\langle O,O'\rangle\), while

\[
 E''+aO''=\alpha'O+(\alpha+\beta')O'+(\beta+a)O''.
\]

The three rows \(O,O',O''\) are independent there, so

\[
                         N(a^2)+aD(a^2)=0.                            \tag{15e}
\]

The left side is a nonzero polynomial in \(a\), because its even and odd
parts are \(N(a^2)\) and \(aD(a^2)\), and its degree is at most six.
For the pure profile, at least seven of the eleven pool points are good,
contradicting (15e).  For the singleton profile, the same argument closes
the branch unless all four possible bad points occur.  In that equality
case they consume all eight ramification units, each has sequence
\((0,1,3,4)\), and infinity is ordinary.  Thus \(D\) is constant and
\(\deg N\leq1\); the polynomial in (15e) then has degree at most two but
still has the other six pool values as roots.  This is again impossible.
Therefore

\[
                         \boxed{\dim{\cal K}\ne4}.                    \tag{15f}
\]

## 5. Five-space: every nonzero cofactor branch closes

For \(d=5\), set

\[
 {\cal P}=*(E\wedge E'\wedge O\wedge O').
\]

The paired rank-three condition makes \({\cal P}\) vanish at every pool
square.  Two quintic Wronskian pairs give the component cap sixteen, so,
if \({\cal P}\ne0\),

\[
 {\cal P}=\Delta Q,\qquad
 \deg Q_i\leq
 \begin{cases}
 6,&2^{14}1,\\
 5,&2^{15}.
 \end{cases}                                           \tag{16}
\]

The paired determinant still satisfies

\[
 D_{\cal K}(x)=-64x^6J(x),\qquad
 J={\cal P}\mathbin{\cdot}(E''+xO'').                  \tag{17}
\]

For degree eleven, \(x^{-6}D_{\cal K}\) has degree at most thirty-five.
The corank-two roots and (16) imply that every nonzero \(J\) has the form

\[
 J(x)=C(x)^2C(-x)R(x)=\Delta(w)C(x)R(x),\qquad
 \deg R\leq
 \begin{cases}
 5,&2^{14}1,\\
 2,&2^{15}.
 \end{cases}                                           \tag{18}
\]

There is a useful invariant replacement for the rank-by-rank Taylor
calculation.  Differentiation gives

\[
 {\cal P}'\mathbin{\cdot}O''
   =\det(E,E'',O,O',O'').                              \tag{19}
\]

At a pool square, let \(A=\langle E,E',O,O'\rangle\).  If
\(\dim A=3\), then \(E''+aO''\in A\).  If \(\dim A\leq2\), then
\(\langle A,E''+aO'',O''\rangle\) has dimension at most four.  In either
case the determinant in (19) is zero.  Therefore

\[
 Q(s)\mathbin{\cdot}O''(s)=0
\]

at all pool squares.  Its degree is at most nine for \(2^{14}1\) and
eight for \(2^{15}\), strictly below the respective pool sizes ten and
eleven.  Hence

\[
                         Q\mathbin{\cdot}O''=0.         \tag{20}
\]

If \(J\ne0\), equations (17)--(20) make \(J\) even.  After cancelling
the even factor \(\Delta\) in (18), \(C(x)R(x)\) is even.  For every
\(a\in P\), this forces \(R(-a)=0\), because structural noncollision
gives \(C(-a)\ne0\).  But \(R\) has degree at most five or two, less than
\(|P|\).  This is impossible.

It remains to exclude \(J=0\) while \({\cal P}\ne0\).  Cofactor
orthogonality and (17) then give

\[
 Q\mathbin{\cdot}E''=Q\mathbin{\cdot}O''=0.
\]

For an independent parameter \(u\), the kernel member

\[
 G_u(z)=\sum_jQ_j(u)F_j(z)
\]

is divisible identically by \((z^2-u)^3\).  Thus

\[
 G_u(z)=(z^2-u)^3\sum_{j=0}^{m}u^jH_j(z),\qquad
 \deg_zH_j\leq5,\qquad
 m\leq
 \begin{cases}
 3,&2^{14}1,\\
 2,&2^{15}.
 \end{cases}                                           \tag{21}
\]

Every coefficient in \(u\) lies in \({\cal K}\).  In the singleton
profile, forced Wronskian degree at least thirty-four gives
\({\cal K}\cap\mathbb C[z]_{\leq5}=0\); the top coefficient
\(-H_m\) in (21) therefore vanishes, and descending kills every \(H_j\).

In the pure profile, the only degree sequence with Wronskian degree at
least thirty-three and a member of degree at most five is

\[
                         (5,8,9,10,11).                \tag{22}
\]

If the highest nonzero \(H_m\) existed, then
\(-H_m\in{\cal K}\cap\mathbb C[z]_{\leq5}\), while the next coefficient
\(3z^2H_m-H_{m-1}\) would lie in
\({\cal K}\cap\mathbb C[z]_{\leq7}=\mathbb C H_m\).
Equation (22) makes \(\deg H_m=5\), but the degree-seven leading term
cannot be cancelled by \(H_{m-1}\), whose degree is at most five.
This contradiction again descends through every coefficient.

Consequently every five-space survivor satisfies

\[
 \boxed{{\cal P}=*(E\wedge E'\wedge O\wedge O')\equiv0.}            \tag{23}
\]

The zero cofactor immediately removes every rank below four.  Indeed,
adapt the basis to the odd projection and write

\[
 O=({\bf O},0),\qquad E=(T,A),qquad
 A=(A_1,\ldots,A_{5-r_o}).
\]

The components of \({\bf O}\) are independent, as are the components of
\(A\).  Since \(r_o\geq2\) in every branch left by (9), some two-component
Wronskian of \({\bf O}\) is nonzero.  For any two components on each side,
the corresponding four-by-four minor in (23) factors as

\[
 \det\!\begin{pmatrix}
 T_i&T_j&A_k&A_l\\
 T_i'&T_j'&A_k'&A_l'\\
 O_i&O_j&0&0\\
 O_i'&O_j'&0&0
 \end{pmatrix}
 =\bigl(O_iO_j'-O_jO_i'\bigr)
    \bigl(A_kA_l'-A_lA_k'\bigr).                    \tag{24}
\]

Thus every pairwise Wronskian among the \(A_k\) vanishes.  In
characteristic zero all nonzero \(A_k\) are proportional, whereas the
pure-even kernel has dimension \(5-r_o\).  Therefore \(5-r_o\leq1\), so

\[
                         \boxed{r_o\in\{4,5\}}.       \tag{25}
\]

This proves the final list (4) simultaneously for both profiles.

## 6. What happened to the Taylor double-root identity

The moving-Taylor mechanism does extend, but it lands exactly on the new
frontier.  In the decic full-odd branch, the odd space was all of
\(\mathbb C[w]_{\leq4}\), and

\[
 (u-w)^2,\ (u-w)^3,\ (u-w)^4
\]

formed the canonical kernel of its value and derivative rows.  The
nonzero cross product \(L\times M=\Delta H\) then obeyed
\(P_0'=(L\times N)_0+3P_1\), forcing its first quotient component to
vanish.

At degree eleven, a full-rank odd projection of a five-space is a hyperplane
\({\cal O}\subset\mathbb C[w]_{\leq5}\).  At a noninflection point its
moving double-root space is

\[
 {\cal O}\cap (u-w)^2\mathbb C[u]_{\leq3},
\]

again of dimension three.  However, (23) says that the corresponding
first cross product already vanishes identically.  The old Taylor
identity therefore becomes a differentiated tangent identity with zero
left side; there is no nonzero \(\Delta\)-quotient left to count.

Thus a parity-only continuation would have had to classify the five-space
four-row tangent condition (23), retaining the last row \(E''+aO''\).
The rational tangent coefficient closes the four-space operator (15), and
the invariant derivative lemma (19) exhausts every nonzero-cofactor
five-space branch.  The next section bypasses the remaining zero-cofactor
classification by removing dimension five itself.

## 7. The fixed numerator closes both profiles

The common exactness kernel has a second realization which does not grow
with the order.  The full proof is
[the uniform fixed-numerator four-space bound](live-three-zero-eighth-split-stable-double-fixed-numerator-four-space-bound.md).
For every \(F\in{\cal K}\), normalize a rational primitive of \(HF\) at
\(-\mu\).  It has the unique form

\[
 G-G(-\mu)={ (z+\mu)^{k+1}n(z)\over C_P(z)^2L(z)},
                         \qquad \deg n\leq9.            \tag{26}
\]

Differentiation gives an injective linear identification of \({\cal K}\)
with a subspace \({\cal W}\subseteq\mathbb C[z]_{\leq9}\) satisfying

\[
 \begin{aligned}
 {\cal E}(n)={}&C_PL\bigl((z+\mu)n'+(k+1)n\bigr)\\
 &-(z+\mu)(2C_P'L+C_PL')n,\\
                         &Q_R^2\mid{\cal E}(n).
 \end{aligned}                                        \tag{27}
\]

At each of the four fixed values \(t=-r\), \(r\in R\), divisibility by
\((z+r)^2\) says \({\cal E}(n)(t)={\cal E}(n)'(t)=0\).  The coefficient
of \(n'\) in \({\cal E}\), and hence of \(n''\) in \({\cal E}'\), is

\[
                         (t+\mu)C_P(t)L(t)\ne0.         \tag{28}
\]

Therefore the two-jet image of a \(d\)-space \({\cal W}\) has rank at
most one at each fixed value.  Every value costs at least \(2(d-1)\)
Wronskian units.  Since a \(d\)-space of nonics has Wronskian degree at
most \(d(10-d)\),

\[
                         8(d-1)\leq d(10-d),            \tag{29}
\]

which forces \(d\leq4\).  Equations (11) and (15f) exclude every possible
dimension \(2\leq d\leq4\), while (3) ensures \(d\geq2\).  Consequently

\[
 \boxed{(8,11;2^{14}1)\text{ and }(8,12;2^{15})
                         \text{ are impossible}.}      \tag{30}
\]

## 8. Exact audit

[verify_live_three_zero_eighth_split_next_stable_undecic_common_kernel_frontier.py](../computations/verify_live_three_zero_eighth_split_next_stable_undecic_common_kernel_frontier.py)
checks the Wronskian and parity ledgers, the unchanged rank-six
pure-even wedge, all degree budgets in (12), (16), and (18), the
exterior-derivative contraction (19), the rational tangent coefficient and
second-jet ramification bounds, the global triple-factor coefficient
descent, and the final conditional dimension/parity table before the
fixed-numerator bound.

[verify_live_three_zero_eighth_split_stable_double_fixed_numerator_four_space_bound.py](../computations/verify_live_three_zero_eighth_split_stable_double_fixed_numerator_four_space_bound.py)
checks the normalized primitive, the fixed degree-nine operator, its two
nonzero jet pivots at each fixed value, and the final dimension-four bound.
