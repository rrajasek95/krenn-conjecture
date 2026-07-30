# Independent audit: scalar-zero tangent apolar-Hall alternative

## 1. Verdict

**PASS.**  The divided-power and hafnian
normalizations, endpoint-index order, \(K_*\)-contraction, pure and mixed
derivative constants, pure projection, minimality scope, oriented
hafnian/permanent identity, Hall inference, and both guards in
[the primary note](curved-scalar-zero-tangent-apolar-hall-alternative.md)
all check.

One sentence in the outcome was weakened during audit.  A nonzero permanent
**implies** that the nonzero-entry graph has a perfect matching and hence
satisfies Hall's inequalities; it is not equivalent to that support
condition over \(\mathbb C\), because distinct permutation terms can
cancel.  The applied repair was

\[
 \text{replace “Equivalently” by “In particular” in the outcome.} \tag{A1}
\]

The theorem statement and proof already use only this correct forward
implication, so no promoted conclusion or subsequent equation changes.
For example, the full-support matrix

\[
 \begin{pmatrix}1&1\\1&-1\end{pmatrix}
\]

has a perfect matching in its support graph but permanent zero, showing
why the reverse implication must not be asserted.

After that repair, the audited primary has SHA-256

    fac1ddb2189437bd42d756a06043852a28ea41d60299968f4da19cd8d8eaa1f3  notes/curved-scalar-zero-tangent-apolar-hall-alternative.md

No positivity, genericity, termwise-vanishing inference, or unmentioned
support restriction is used.  The result is an alternative and an exact
remaining interface, not a closure of the scalar-zero branch.

## 2. Pair-row and cohafnian normalization

Write the coefficient of \(q_{xy}\) on a word \(\omega\) as
\((Q_\omega)_{xy}\), with the reverse entry defined by endpoint-ordered
transpose.  This gives a symmetric scalar matrix.  In the site-square-zero
algebra, the divided power \(q^{[h]}\) lists every perfect matching once:
the \(h!\) orderings in the ordinary power are removed by division by
\(h!\).  Therefore

\[
 [q^{[h]}]_\omega=\operatorname{haf}(Q_\omega).          \tag{A2}
\]

For fixed endpoint rows \(p_i,s_j\), the coefficient on a residual pair
\(\{x,y\}\) is

\[
 P_{x,i}S_{y,j}+P_{y,i}S_{x,j}.                         \tag{A3}
\]

Consequently

\[
\begin{aligned}
 [p_i s_jq^{[h-1]}]_\omega
 &=\sum_{x<y}
   (P_{x,i}S_{y,j}+P_{y,i}S_{x,j})
   H(Q_\omega)_{xy}\\
 &=\sum_{x,y}P_{x,i}H(Q_\omega)_{xy}S_{y,j}\\
 &=(P_\omega^TH(Q_\omega)S_\omega)_{ij}.                \tag{A4}
\end{aligned}
\]

There is no missing factor \(1/2\): the second line is an ordered
\(x,y\) sum, while the first line has already combined the two endpoint
orders on each unordered pair.  The diagonal of \(H\) is zero, so same-site
products are correctly omitted.

On a constant word \(c^{2h}\), the coordinate of
\(\delta_{ij}X_i\) is one only when \(i=j=c\); on a mixed word it is zero.
Thus the nine scalar equations are exactly

\[
 P_\omega^TH(Q_\omega)S_\omega
   =D_\omega-\operatorname{haf}(Q_\omega)a,             \tag{A5}
\]

with \(D_\omega=E_{cc}\) on the constant word and zero on a mixed word.
The \((i,j)\)-entry remains the literal \(p_i s_j\) row; no transpose of
the direct block or exchange of \(i,j\) has occurred.

## 3. The scalar-zero contraction and derivative constants

Let \(a\ne b\), \(\alpha=a_{ab}\ne0\), and

\[
 K_*=\tau E_{ab}-\alpha I,\qquad \tau=\operatorname{tr}a. \tag{A6}
\]

Because \(E_{ab}^2=0\),

\[
 K_*=-\alpha\left(I-\frac{\tau}{\alpha}E_{ab}\right),
\qquad
 K_*^{-1}=-\frac1\alpha
   \left(I+\frac{\tau}{\alpha}E_{ab}\right).            \tag{A7}
\]

Thus invertibility is exact and uses no generic condition on \(\tau\).
With the coefficient pairing used in the physical rows,

\[
 \sum_{i,j}(K_*)_{ij}a_{ij}
   =\tau a_{ab}-\alpha\operatorname{tr}a=0.             \tag{A8}
\]

The diagonal entries of \(K_*\) are all \(-\alpha\).  Contracting all nine
pair rows therefore gives

\[
 rq^{[h-1]}=-\alpha\sum_{c=0}^2X_c.                    \tag{A9}
\]

For a word \(\omega\), the scalar response edge is

\[
 (R_\omega)_{xy}
 =P_xK_*S_y^T+P_yK_*S_x^T.                             \tag{A10}
\]

This agrees with
\(r=\sum_{i,j}(K_*)_{ij}p_i s_j\): the first term in (A10) keeps \(p\) at
\(x\) and \(s\) at \(y\), while the second keeps the opposite physical
endpoint order.  Hence

\[
 [r^{[h]}]_\omega=\operatorname{haf}(R_\omega).         \tag{A11}
\]

The directional derivative normalization is

\[
 D\operatorname{haf}_{Q}(R)
 =\sum_{x<y}R_{xy}
   \operatorname{haf}(Q_{W\setminus\{x,y\}}).           \tag{A12}
\]

Every term chooses one distinguished \(R\)-edge and an unordered matching
of \(h-1\) \(Q\)-edges, so again there is no factor \(h\), \(2\), or
\((h-1)!\).  Substituting (A10) and using (A4) yields

\[
 D\operatorname{haf}_{Q_\omega}(R_\omega)
 =\sum_{i,j}(K_*)_{ij}
   (P_\omega^TH(Q_\omega)S_\omega)_{ij}.               \tag{A13}
\]

Equations (A5), (A8), and the diagonal of \(K_*\) now give exactly

\[
 D\operatorname{haf}_{Q_\omega}(R_\omega)
 =\begin{cases}
   -\alpha,&\omega=c^{2h},\\
   0,&\omega\text{ mixed}.
  \end{cases}                                           \tag{A14}
\]

This independently recovers (A9) coefficientwise.  In particular the
three pure derivative constants are all the same \(-\alpha\); there is no
lost trace term or colour-dependent sign.

## 4. Pure projection and the minimality branch

Assume every mixed coordinate of \(r^{[h]}\) is zero.  Since
\(r^{[h]}\ne0\), there is a nonempty set \(C\) and nonzero coefficients
\(\lambda_c\) such that

\[
 r^{[h]}=\sum_{c\in C}\lambda_cX_c.                    \tag{A15}
\]

Projecting every local colour space onto the axes in \(C\) is an algebra
endomorphism of the site-square-zero algebra.  If \(r'\) is the projected
quadratic, functoriality gives

\[
 (r')^{[h]}=\sum_{c\in C}\lambda_cX_c.                 \tag{A16}
\]

At one chosen site, scale its \(c\)-axis by \(\lambda_c^{-1}\).  Every
perfect matching uses that site exactly once, so this turns (A16) into

\[
                         \sum_{c\in C}X_c.              \tag{A17}
\]

No root extraction, positivity, or choice of individual matching summands
is involved.

The minimality statement has exactly the scope claimed:

* \(|C|=3\) gives an exact ternary aggregate source on the \(2h\) residual
  sites and hence a two-site descent;
* at \(h=3\), that source contradicts the proved arbitrary-complex
  six-site theorem;
* for \(h>3\), it contradicts order-minimality only when the ambient
  hypothetical ternary source was chosen of minimum order;
* \(|C|=1,2\) yields legitimate unary or binary sources and does not
  contradict ternary minimality.

Thus the primary does not silently promote the unary or binary pure branch
to a contradiction.

## 5. Oriented hafnians, permanents, and Hall

Put

\[
                         B_{xy}=P_xK_*S_y^T.            \tag{A18}
\]

Then \(R_{xy}=B_{xy}+B_{yx}\).  Expand one factor on every edge of a
perfect matching.  Each expanded term orients the edge from the endpoint
supplying \(P\) to the endpoint supplying \(S\).  The \(h\) \(P\)-endpoints
form a set \(A\), the \(S\)-endpoints form \(W\setminus A\), and the
oriented matching is a bijection

\[
                         \pi:A\longrightarrow W\setminus A.      \tag{A19}
\]

Conversely, a balanced set \(A\) and a bijection \(\pi\) determine one
oriented perfect matching term.  These operations are inverse.  Therefore

\[
 \operatorname{haf}(R)
 =\sum_{\substack{A\subseteq W\\|A|=h}}
   \sum_{\pi:A\overset{\sim}{\to}W\setminus A}
   \prod_{x\in A}B_{x,\pi(x)}
 =\sum_{\substack{A\subseteq W\\|A|=h}}
   \operatorname{per}(B_{A,W\setminus A}).             \tag{A20}
\]

There is no multiplicity factor.  Complementary sets \(A\) and
\(W\setminus A\) encode the two globally reversed orientations and are
supposed to occur separately.  A direct exact check at six sites with an
arbitrary nonsymmetric integer matrix also reproduces both sides of
(A20).

If the hafnian is nonzero, not every permanent in (A20) can vanish, even
over \(\mathbb C\).  For one selected \(A\), a nonzero permanent has at
least one nonzero permutation product.  Since \(\mathbb C\) has no zero
divisors, every edge in that product is nonzero, giving a perfect matching
in the support graph.  Hall's inequalities follow.  This uses only the
forward implication highlighted in the verdict; it never infers a
nonzero permanent merely from support.

The two advertised wordwise corollaries also follow.  A \(P\)-only site
cannot lie on the \(S\)-side of the selected permanent matrix, where its
entire column would be zero; therefore all \(P\)-only sites lie in \(A\)
and there are at most \(h\).  Similarly all \(S\)-only sites lie in the
complement and there are at most \(h\).  The proof does not assume that
global endpoint-star injectivity survives scalarization at the chosen
word; the primary explicitly warns that it need not.

## 6. The injective-star response guard

The pairs \(P_1,P_2\) are disjoint and \(P_0=\{a_0,b_0\}\) lies in their
complement, so \(P_0,P_1,P_2\) are pairwise disjoint.  This is possible
because \(h\ge3\).  For

\[
 F_c=\bigotimes_{x\notin P_c}e_c^{(x)},                \tag{A21}
\]

the only unoccupied sites are the two members of \(P_c\).  Consequently:

* \(p_0s_0F_0\) keeps only the term \(a_0b_0\) and equals \(X_0\);
* \(p_1s_1F_1=X_1\) and \(p_2s_2F_2=X_2\);
* every \(p_i s_jF_c\) with \(i\ne j\), or with \(c\ne i=j\),
  collides at at least one occupied site.

Thus all nine identities

\[
                         p_i s_jF=\delta_{ij}X_i        \tag{A22}
\]

hold termwise.  The \(p\)-rows have mutually disjoint nonzero supports
\(A_0,\{a_1\},\{a_2\}\), and the \(s\)-rows have supports
\(B_0,\{b_1\},\{b_2\}\), so both star triples are injective.

For the direct block with sole entry \(a_{ab}=-1\),

\[
 \alpha=-1,\qquad\tau=0,\qquad K_*=I,\qquad
 r=p_0s_0+p_1s_1+p_2s_2.                              \tag{A23}
\]

Equation (A22) gives \(rF=\Delta_{2h,3}\).  On the displayed mixed word,
the two private response edges \(a_1b_1,a_2b_2\) are forced.  The remaining
sites form \(A_0\sqcup B_0\), and the colour-zero response is the
complete bipartite graph between those shores with unit entries.  Its
perfect matchings are the \((h-2)!\) bijections, so

\[
                         [r^{[h]}]_\omega=(h-2)!\ne0.   \tag{A24}
\]

Divided powers count each matching once; the factorial in (A24) is the
number of different bijections, not a normalization artifact.

This guard uses formal \(Q=0\) and \(F\) in place of \(q^{[h]}\) and
\(q^{[h-1]}\).  It does not assert the existence of a quadratic \(q\)
with those two powers.  At \(h=3\), the cited uniform pure-lift theorem
indeed excludes such a \(q\) under the nine products (A22).  Hence the
guard establishes compatibility of the response rectangle, injective
stars, \(K_*^{-1}\), and response nonnilpotence only; it is not an exact
source or a counterexample.

## 7. The exact common-power guard

The source note
[on the polarized pair-cap example](polarized-six-site-paircap-counterexample.md)
lists the rational cells of \(z\).  On

\[
                         \omega=(0,1,1,0,0,1),          \tag{A25}
\]

direct comparison with that table leaves exactly

\[
 (03;0,0)=1,\qquad (15;1,1)=\frac13,\qquad
 (24;1,0)=2.                                           \tag{A26}
\]

All other listed \(z\)-cells disagree with at least one endpoint colour.
The three edges in (A26) are disjoint and cover all six sites.  They are
therefore the unique supported perfect matching on this word, with product

\[
                         1\cdot\frac13\cdot2=\frac23.   \tag{A27}
\]

Thus

\[
                         [z^{[3]}]_\omega=\frac23\ne0   \tag{A28}
\]

with no additional \(3!\): the divided power is the hafnian.  An exact
rational replay of all 729 words also verifies the source identity

\[
                         zq^{[2]}=\Delta_{6,3}.          \tag{A29}
\]

The coefficient of (A29) is the hafnian derivative in direction \(z\).
It is zero on every mixed word and one on each constant word, exactly as
claimed.

This guard supplies a genuine common quadratic \(q\), its common power,
and mixed tangent nonnilpotence.  It does not realize
\(z=\sum_{i,j}(K_*)_{ij}p_i s_j\) from two injective star triples, nor
does it satisfy one shared nine-row system.  Conversely, the Section 5
guard has the star factorization and formal nine products but deliberately
lacks the common power.  Their complementary scopes are stated correctly.

## 8. Scope of the remaining lemma

The mixed branch retains simultaneously:

\[
\begin{aligned}
 P_\omega^TH(Q_\omega)S_\omega
   &=-\operatorname{haf}(Q_\omega)a,\\
 \operatorname{haf}(R_\omega)&\ne0,\\
 D\operatorname{haf}_{Q_\omega}(R_\omega)&=0,
\end{aligned}                                                 \tag{A30}
\]

and the constant words replace the first right side by
\(E_{cc}-\operatorname{haf}(Q_c)a\) and the derivative by \(-\alpha\).
The proof does not derive cross-word compatibility beyond these equations.

Accordingly, the final proposed statement—using global rank-three stars
and the full cohafnian system to kill all mixed response hafnians and keep
all three pure ones—is explicitly a missing lemma.  If proved, and only
then, Theorem 4.1 would enter the ternary pure branch and minimality would
finish the scalar-zero packet.  Neither guard is claimed to satisfy both
sides of that interface, and no hidden genericity or support classification
is being used to bridge it.
