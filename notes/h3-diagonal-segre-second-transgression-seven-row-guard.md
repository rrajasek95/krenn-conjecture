# One diagonal anchor and all off-diagonal rows do not define the \(h=3\) second transgression

## 1. Outcome

There is an actual eight-site decorated block array whose matching tensor is

\[
                         H_8(A)=X_2 .                    \tag{1}
\]

On the chart obtained by deleting its two distinguished endpoints, it has

* good endpoint-star triples and literal shared-star/Segre factorization;
* a nonzero selected direct scalar \(d_{01}=1\);
* all six off-diagonal rows correct on all \(3^6\) residual words;
* the complete \(22\) diagonal row equal to \(X_2\); and
* only the two missing GHZ residuals \(-X_0\) and \(-X_1\), in rows \(00\)
  and \(11\), respectively.

Nevertheless, for the selected row \((a,b)=(0,1)\) on the pure physical
colour \(c=2\),

\[
 d_{01}q^{[3]}+p_0s_1q^{[2]}=0                         \tag{2}
\]

as a complete all-word tensor identity, while

\[
 \boxed{(q+p_0s_1)^{[3]}=-2X_2.}                       \tag{3}
\]

Thus every selected Hamming-two coefficient is zero, but the nonlinear
clean tail is nonzero. One literal adjacent \(27\)-row decomposition of
the same physical block array also holds; its target is the partial target
\(X_2\), not the full ternary GHZ target.

The exact logical boundary is

\[
 \boxed{
 \begin{gathered}
 \text{selected all-word row}+\text{all six off-diagonal rows}
 +X_2\text{ anchor}\\
 {}+\text{good Segre stars}+\text{one literal adjacent decomposition}
 \end{gathered}
 \not\Longrightarrow
 \alpha R^{[2]}q+R^{[3]}=0 .}                            \tag{4}
\]

The guard is not a full-nine GHZ source: it misses exactly \(X_0\) and
\(X_1\). Therefore (4) does not refute a second-transgression operator
which genuinely uses the complete three-diagonal target sector. It proves
that the \(X_2\) anchor cannot be transported to the clean tail using only
the selected Hamming-two row and the local Segre rectangle. Some
complementary diagonal target-purity input, or a cross-chart operation which
really imports it, is essential.

The guard also falsifies a tempting extrapolation from the committed
\(\chi=-4\) Hamming-one boundary. In that packet the unweighted sum of the
selected distance-two residuals happens to be \(\chi/4=-1\). Here that sum
is zero while \(\chi=-2\). Hence the numerical relation is packet-specific,
not a universal Hamming-two transgression formula.

## 2. Exact physical packet

Let the six residual sites be \(0,\ldots,5\). All displayed residual
variables below have physical colour \(2\); write \(z_x=z_x^2\). Put

\[
                         q=z_0z_1+z_4z_5,
             \qquad d=E_{01}.                            \tag{5}
\]

The two endpoint-star triples are

\[
\begin{aligned}
 p_0&=z_0+z_1,&p_1&=z_4,&p_2&=z_2+z_3,\\
 s_0&=z_5,&s_1&=z_2-z_3,&s_2&={1\over2}(z_2+z_3).
\end{aligned}                                           \tag{6}
\]

These are literal rows of the blocks incident with two new sites \(p,q\),
and \(d=A_{pq}\). Thus the packet is a physical decorated edge array, not
a formal assignment of nine response tensors. Both triples in (6) are
linearly independent. Since every response is the actual product

\[
                         R_{ij}=p_is_j,                  \tag{7}
\]

all Segre rectangles

\[
                         R_{ij}R_{k\ell}=R_{i\ell}R_{kj} \tag{8}
\]

hold in the site-square-zero algebra.

The internal quadratic has only two disjoint edges, so

\[
                         q^{[3]}=0,
             \qquad q^{[2]}=z_0z_1z_4z_5.              \tag{9}
\]

Every response product in (7), after multiplication by \(q^{[2]}\),
vanishes except \(R_{22}\). The two potentially relevant products are

\[
\begin{aligned}
 p_2s_1&=(z_2+z_3)(z_2-z_3)=0,\\
 p_2s_2&={1\over2}(z_2+z_3)^2=z_2z_3 .
\end{aligned}                                           \tag{10}
\]

Every other response either occupies a site already used by (9), or has no
matching on the complement. Consequently

\[
 d_{ij}q^{[3]}+p_is_jq^{[2]}
 =\begin{cases}
 X_2,&(i,j)=(2,2),\\
 0,&\text{otherwise}.
 \end{cases}                                            \tag{11}
\]

This identity holds on all \(729\) residual colour words. Since the nine
endpoint contractions form the complete coefficient basis at \(p,q\),
(11) is equivalent to the physical eight-site statement (1). Relative to
the desired full-nine target, its complete failure ledger is precisely

\[
             (00,0^6,-1),\qquad(11,1^6,-1).             \tag{12}
\]

In particular, there are no hidden mixed-word failures in any supplied
row.

## 3. The selected row has no Hamming-two detector

Take

\[
                  \alpha=d_{01}=1,
             \qquad R=p_0s_1=(z_0+z_1)(z_2-z_3).       \tag{13}
\]

Equation (9) makes \(Rq^{[2]}=0\): every edge of \(R\) meets one of the
sites \(0,1\) already occupied by \(q^{[2]}\). Hence (2) holds as a
polynomial identity, not only through Hamming distance two.

The second response layer is different. On sites \(0,1,2,3\), the two
response matchings have weights

\[
                         (02\mid13)=-1,
             \qquad     (03\mid12)=-1.                 \tag{14}
\]

Therefore

\[
                         R^{[2]}=-2z_0z_1z_2z_3,
             \qquad R^{[2]}q=-2X_2.                    \tag{15}
\]

The response is supported on only four sites, so \(R^{[3]}=0\). The
four response-order layers of the clean cap are

\[
  \bigl(q^{[3]},Rq^{[2]},R^{[2]}q,R^{[3]}\bigr)
                         =(0,0,-2X_2,0),                \tag{16}
\]

which proves (3).

There are \(\binom62\cdot2^2=60\) literal words at Hamming distance two
from \(2^6\). Every selected \(01\)-coefficient on those words is zero by
(2). Thus no linear combination, response-dependent weighting, or
ordinary contraction of the selected Hamming-two rows alone can equal the
tail in (16) on all such packets.

## 4. What this says about a second-transgression operator

At \(h=3\), the desired weak replacement for a full site derivation is a
source-provenant degree-preserving operation \(\mathcal L_R\) satisfying

\[
 \mathcal L_R(q^{[3]})=R^{[2]}q,
 \qquad
 \mathcal L_R(Rq^{[2]})=R^{[3]},                        \tag{17}
\]

and killing the relevant target term. Applied to the selected off-diagonal
row, (17) would give

\[
                 \mathcal L_R(\alpha q^{[3]}+Rq^{[2]})
                         =\alpha R^{[2]}q+R^{[3]}.       \tag{18}
\]

The present packet proves that such an operation is not well-defined on
the quotient generated only by the relations retained in (4). The left
side of the selected source row is zero there, whereas its prescribed image
would be \(-2X_2\).

This does not obstruct an operator on the complete full-nine source
complex. Equations (12) identify exactly where extra information can
enter: the \(00\) and \(11\) target directions. The guard has both of them
missing, so it does not decide whether either one alone suffices. It does
decide that the already restored \(22\) anchor, even together with every
off-diagonal row, is not enough.

The output-label geometry explains the boundary. The selected response
uses the first-star label \(0\) and second-star label \(1\), while the
\(22\) anchor occupies a different row and column. Segre factorization
identifies products of response cells, but it supplies no target-bearing
relation in the two missing complementary diagonal directions. A valid
transgression must use those target relations before passing to the clean
response grade; multiplying saturated top-degree equations cannot create
them.

## 5. Adjacent-chart provenance and exact scope

Choose residual site \(2\) as a third exposed site and let \(D\) be the
remaining five sites. The same physical block array has the literal
three-site expansion

\[
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[2]}
       +x_iy_jt_kz
   =\mathbf1_{i=j=k=2}X_2^D .                            \tag{19}
\]

The checker verifies all \(27\cdot3^5\) coefficients of (19). Thus the
guard is not defeated by merely asking that the one-chart data arise from
one genuine adjacent decomposition. Its limitation remains target
provenance: (19) has only the \(2\)-target, whereas a complete source would
have all three independent diagonal targets.

This is complementary to the committed all-word \(8/9\) guard. That
packet supplies \(X_0,X_1\) and omits \(X_2\); the present packet supplies
\(X_2\) and omits \(X_0,X_1\). Together they show:

1. the third diagonal target cannot be discarded;
2. restoring that target in isolation does not produce the clean tail; and
3. the remaining proof must use simultaneous diagonal target-purity on the
   same shared-star carrier, rather than splice conclusions from separate
   partial packets.

No certified dependency is changed. The conjecture remains open.

## 6. Exact audit

The dependency-free checker
[verify_h3_diagonal_segre_second_transgression_seven_row_guard.py](../computations/verify_h3_diagonal_segre_second_transgression_seven_row_guard.py)
verifies

* the complete \(H_8(A)=X_2\) endpoint-slice ledger;
* all \(7\cdot729\) supplied row coefficients and the two-entry GHZ failure
  ledger (12);
* both star ranks and every literal Segre rectangle;
* the selected all-word and \(60\)-word Hamming-two zero ledgers;
* the exact layers \((0,0,-2,0)\);
* all \(27\cdot243\) coefficients of the adjacent decomposition (19); and
* sign and target-edge mutation guards.

It uses only the Python standard library and runs unchanged under optimized
and isolated Python.
