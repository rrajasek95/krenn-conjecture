# Pure binary response survives the channel and common-power tests separately

## 1. Outcome

At the first \(8\to6\) boundary, the unary/binary side of the
[pure-descent/apolar-Hall alternative](curved-scalar-zero-tangent-apolar-hall-alternative.md)
cannot be removed from either half of the scalar-zero interface separately.

First, there is an exact six-site quadratic

\[
                  r=\sum_{k=0}^2 p_k t_k                         \tag{1}
\]

such that both triples \((p_0,p_1,p_2)\) and
\((t_0,t_1,t_2)\) are injective and

\[
                         r^{[3]}=X_0+X_1.                        \tag{2}
\]

Thus an invertible three-channel pairing is compatible with a top matching
power having only pure coordinates and exactly two surviving colours.
Ordinary matrix-rank language is unnecessary and potentially misleading:
the factorization is literal in the site-square-zero algebra.

Second, a seven-edge response \(\widehat r\) and a six-edge common quadratic
\(\widehat q\) satisfy

\[
 \widehat r^{[3]}=X_0+X_1,
 \qquad
 \widehat r\widehat q^{[2]}=X_0+X_1+X_2.              \tag{3}
\]

Thus even the exact ternary common-power row does not force the third pure
coefficient of the clean error.  The two examples do not combine: an
invertible six-by-six alternating-shore flattening and one dark colour-two
port prove that \(\widehat r\) is not a sum of three products of linear
forms.  Neither example supplies the full nine physical pair rows.

The two constructions in this note originally left coupling the
three-channel star factorization to the common power as the next target.
That target is now negatively superseded by Section 7 of the
[independent audit](curved-pure-binary-three-channel-common-power-independent-audit.md),
which gives one exact simultaneous unary guard satisfying both conditions.
The positive input must therefore use the remaining uncontracted full-nine
rows or an equivalent cross-word physical relation.  Product rank,
endpoint-star injectivity, response purity, and the common-power tangent
equation are insufficient even when imposed together.

## 2. Alternating binary cycle

Let the residual sites be \(W=\{0,1,2,3,4,5\}\), and write \(x_{v,c}\)
for colour \(c\) at site \(v\).  Put unit colour-zero cells on

\[
                         P_0=01\mid23\mid45
\]

and unit colour-one cells on

\[
                         P_1=12\mid34\mid50.                     \tag{4}
\]

Their physical union is the six-cycle

\[
                         0-1-2-3-4-5-0.
\]

It has exactly the two perfect matchings displayed above.  Their endpoint colours
are respectively constant zero and constant one.  Therefore the quadratic

\[
\begin{aligned}
 r={}&x_{0,0}x_{1,0}+x_{2,0}x_{3,0}+x_{4,0}x_{5,0}\\
    &+x_{1,1}x_{2,1}+x_{3,1}x_{4,1}+x_{5,1}x_{0,1}
\end{aligned}                                                    \tag{5}
\]

satisfies (2) coefficientwise.  There are no cancelling or unlisted mixed
words: every supported perfect matching is one of the two displayed
matchings.

## 3. Exact three-channel factorization

Group one edge from each alternating matching and define

\[
\begin{array}{lll}
 u_0=x_{0,0}+x_{1,0},&&v_0=x_{1,1}+x_{2,1},\\
 u_1=x_{2,0}+x_{3,0},&&v_1=x_{3,1}+x_{4,1},\\
 u_2=x_{4,0}+x_{5,0},&&v_2=x_{5,1}+x_{0,1}.
\end{array}                                                    \tag{6}
\]

Over \(\mathbb C\), put

\[
                       p_k=u_k+i v_k,\qquad
                       t_k=\frac12(u_k-i v_k).                   \tag{7}
\]

Commutativity cancels the two cross terms, while the square of a local
port variable vanishes.  Hence

\[
\begin{aligned}
 p_kt_k
   &=\frac12(u_k^2+v_k^2)\\
   &=\text{the \(k\)-th colour-zero edge of \(P_0\)}
     +\text{the \(k\)-th colour-one edge of \(P_1\)}.             \tag{8}
\end{aligned}
\]

Summing (8) proves (1) and recovers (5) exactly.

The six sets of decorated ports appearing in the three pairs
\((u_k,v_k)\) are disjoint.  Projecting a linear relation among the \(p_k\)
onto any one of those sets kills the other two terms and forces its
coefficient to vanish.  Thus the \(p\)-triple is injective.  The same
argument applies to the \(t\)-triple.  Taking the channel matrix \(K=I_3\)
makes (1) an invertible pairing of the two triples.

The construction uses same-site components in \(u_k\) and \(v_k\), but
never multiplies two of them in a surviving term: the cross products cancel
in (8), and the remaining same-variable squares vanish.  It therefore
respects the same site-square-zero algebra and endpoint-colour conventions
as the physical response packet.

## 4. An exact common-power guard

Retain the six-cycle response (5) and add the colour-two chord \(02\):

\[
\begin{aligned}
 \widehat r={}&x_{0,0}x_{1,0}+x_{2,0}x_{3,0}
                 +x_{4,0}x_{5,0}\\
 &+x_{1,1}x_{2,1}+x_{3,1}x_{4,1}
                 +x_{5,1}x_{0,1}
   +x_{0,2}x_{2,2}.                                   \tag{9}
\end{aligned}
\]

The chord occurs in no perfect matching of the physical support: deleting
its endpoints leaves site \(1\) isolated.  The only perfect matchings are
still the two alternating one-factors displayed in Section 2.  Consequently

\[
                         \widehat r^{[3]}=X_0+X_1.     \tag{10}
\]

Now set

\[
\begin{aligned}
 \widehat q={}&x_{2,0}x_{3,0}+x_{4,0}x_{5,0}
                -x_{3,1}x_{4,1}-x_{5,1}x_{0,1}\\
              &+x_{1,2}x_{4,2}+x_{3,2}x_{5,2}.       \tag{11}
\end{aligned}
\]

There are exactly five distinguished-edge terms in
\(\widehat r\widehat q^{[2]}\).  Three are the constant words

\[
\begin{array}{c|c|c}
 \widehat r\text{-edge}&\widehat q\text{-edges}&\text{weight}\\ \hline
 01_0&23_0,45_0&1\\
 12_1&34_1,50_1&1\\
 02_2&14_2,35_2&1.
\end{array}                                                   \tag{12}
\]

The other two have the same word

\[
                         (1,2,0,0,2,1)                 \tag{13}
\]

and are

\[
 23_0\mid50_1\mid14_2\quad\hbox{of weight }-1,
 \qquad
 50_1\mid23_0\mid14_2\quad\hbox{of weight }+1.       \tag{14}
\]

They cancel exactly.  This proves the second identity in (3), with no
unlisted word and no positivity assumption.

### 4.1 Why this response is not a three-channel guard

The failure to combine the two examples is itself exact.  Suppose, more
generally, that

\[
                         \widehat r=\sum_{k=0}^2p_kt_k. \tag{15}
\]

For a decorated port \(z\), let \(P_z,T_z\in\mathbb C^3\) be its
coefficient rows in the two triples and put

\[
 g_z=(P_z,T_z)\in\mathbb C^6,
 \qquad
 J=\begin{pmatrix}0&I_3\\I_3&0\end{pmatrix}.          \tag{16}
\]

For ports on distinct physical sites, their edge coefficient is
\(g_zJg_w^{\mathsf T}\).  Take the six decorated endpoints of the cycle
on the even shore \(\{0,2,4\}\) and the corresponding six endpoints on
the odd shore \(\{1,3,5\}\).  The response matrix between these two
ordered port sets is a permutation matrix: the six cycle edges have unit
weight and every other cross entry is zero.  Hence the six odd-shore
vectors \(g_w\) form a basis of \(\mathbb C^6\).

The new port \(z=x_{0,2}\) has zero response against all six of those
odd-shore ports.  Equation (16) and nondegeneracy of \(J\) therefore force
\(g_z=0\).  This contradicts the unit coefficient of
\(x_{0,2}x_{2,2}\) in (9).  Thus (15) is impossible, even without asking
that either endpoint triple be injective.  The obstruction applies equally
to \(\sum_{ij}K_{ij}p_is_j\), since the channel matrix can be absorbed
into one triple.

This six-dimensional shore argument also explains why simply appending a
dark third-colour chord to the factorized alternating cycle cannot solve
the simultaneous problem: the binary cycle already saturates all six
available coefficient directions.

## 5. Exact remaining pure-branch attack

For a genuine off-diagonal scalar-zero cap one has, in addition to (1)--(2),

\[
                  rq^{[2]}=-\alpha(X_0+X_1+X_2),
                  \qquad \alpha\ne0,                            \tag{17}
\]

and all nine rows share the same endpoint stars, direct block, and
quadratic \(q\).  On the missing constant colour \(2\), equations (2) and
(17) say simultaneously

\[
 \operatorname {haf}(R_2)=0,\qquad
 D\operatorname {haf}_{Q_2}(R_2)=-\alpha.                       \tag{18}
\]

There is no contradiction in (18) for arbitrary scalar matrices, and
(9)--(14) show that there is no contradiction even for one global pair of
decorated quadratics satisfying every word of the common-power equation.
The usable theorem must propagate the three-channel factorization together
with the full wordwise cohafnian identities (or the other eight physical
rows) into this missing-colour slice.  If it forces the third pure
coefficient of \(r^{[3]}\) to be nonzero, the pure-descent alternative
becomes ternary and the exact \(N\mapsto N-2\) descent follows.

The two guards in this source note initially left the narrow attack of
classifying binary-pure three-channel responses sharing a ternary
common-power rectangle.  Section 7 of the independent audit now gives an
exact simultaneous counterguard to that implication as well.  The surviving
attack is the full-nine one stated in Section 8 of that audit: use the
uncontracted entries of the wordwise cohafnian system to forbid the
missing-colour cofactor-hole mechanism.  Arbitrary binary matching sources,
ordinary low-rank matrices, contracted common-power rectangles, and
arbitrary tangent pairs are all too weak.
