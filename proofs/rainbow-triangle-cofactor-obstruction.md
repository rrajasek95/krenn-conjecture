# A fixed rainbow triangle with an impossible pure cofactor

This note excludes the all-rank-one six-vertex support chart

\[
\begin{array}{c|ccccccccccccccc}
e&01&02&03&04&05&12&13&14&15&23&24&25&34&35&45\\ \hline
\operatorname{supp}A_e
&0\!\times\!012&00&11&22&0\!\times\!012
&012\!\times\!012&012\!\times\!2&11&012\!\times\!012
&012\!\times\!2&012\!\times\!1&012\!\times\!012
&00&22&1\!\times\!012.
\end{array}                                                    \tag{1}
\]

Every displayed endpoint factor coordinate is nonzero.  The argument uses
only exact tensor quotients.

## 1. A three-pure-term quotient lemma

Let `V_1,V_2,V_3` contain a distinguished nonzero vector `e`.  Suppose

\[
 x\otimes c\otimes d+b\otimes e\otimes f
       +a\otimes g\otimes h=\lambda e\otimes e\otimes e,
 \qquad \lambda\ne0.                                      \tag{2}
\]

Assume `c,g` are not proportional to `e`; `x` is not proportional to `e`;
and `f` is not proportional to `e`.  Then (2) is impossible.

Indeed, quotient the second mode by `C e`.  The first and third terms are
nonzero pure tensors and sum to zero.  Hence their factors in the other two
modes are proportional, in particular `x` is proportional to `a` and `d`
is proportional to `h`.  Now quotient the first mode by `C x`.  The first
and third terms vanish, while the target survives because `x` is not
proportional to `e`.  If the middle term also vanishes there is an immediate
contradiction.  Otherwise equality of the two surviving pure tensors forces
`f` to be proportional to `e`, again a contradiction.

The same proof works with additional spectator modes: equality of two
nonzero pure tensors after the first quotient makes every spectator factor
proportional, and a noncoordinate spectator factor of the middle term gives
the final contradiction.

## 2. The color-sensitive fixed triangle

For the chart (1), the color-sensitive stabilizer equations have the exact
solution

\[
\begin{array}{c|cccccc}
v&0&1&2&3&4&5\\ \hline
\alpha_v&(0,1-u,1-w)&(0,0,0)&(0,0,0)&(1-v,u,0)&(v,0,w)&(0,0,0).
\end{array}                                                   \tag{3}
\]

The three color sums are one.  On every supported cell outside the triangle
`03,04,34`, the multiplier `alpha_(u,i)+alpha_(v,j)` is zero.  On the three
triangle cells `11,22,00`, respectively, it is exactly one.  Thus the exact
color-sensitive identity becomes

\[
 \Delta_{6,3}=A_{03}\otimes H_{1245}
              +A_{04}\otimes H_{1235}
              +A_{34}\otimes H_{0125}.                    \tag{4}
\]

The three-slice-center rigidity lemma applies to (4).  Its three triangle
factors are the distinct same-color cells `11,22,00`, so their complementary
tensors are nonzero scalar multiples of

\[
 e_1^{\otimes\{1,2,4,5\}},\qquad
 e_2^{\otimes\{1,2,3,5\}},\qquad
 e_0^{\otimes\{0,1,2,5\}},                                \tag{5}
\]

respectively.

It is enough to inspect the last cofactor.  On vertices `0,1,2,5`, expansion
over the three perfect matchings gives, after suppressing nonzero scalars,

\[
 x_{01}\otimes c_{25}^{(2)}\otimes c_{25}^{(5)}
 +b_{15}^{(1)}\otimes e_0^{(2)}\otimes b_{15}^{(5)}
 +a_{12}^{(1)}\otimes a_{12}^{(2)}\otimes x_{05}
 =\lambda e_0^{(1)}\otimes e_0^{(2)}\otimes e_0^{(5)}.    \tag{6}
\]

(The common factor at vertex `0` has already been contracted out; an
equivalent ordering follows directly from the three matching terms.)  Every
vector in (6) except the displayed `e_0` has full three-coordinate support
by (1).  Equation (6) is therefore forbidden by the quotient lemma with the
second mode as the first quotient.  This contradicts (5), and hence (1)
cannot realize `Delta_(6,3)`.

## 3. Exact audit

`computations/verify_rainbow_triangle_cofactor.py` checks (3) cell by cell,
enumerates the three complementary matchings, verifies all factor-support
hypotheses of the quotient lemma, and invokes the reusable detector
`rainbow_triangle_cofactor_witness`.
