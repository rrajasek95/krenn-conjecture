# Higher splits: the developable-secant closure at \(p=19, C=7\)

## 1. Result

Continue from the moving-singleton common-lift theorem and the exact
\(p=19\) residual census.  There are two no-quartic \(C=7\) profiles left
after the undecic singleton--double coupling.

**Theorem 1.1 (developable-secant closure).**  Neither of the profiles

\[
 \boxed{2^9 1^{h+3},\qquad 3\,2^8 1^{h+2}}                 \tag{1}
\]

can exist.  In the \((e;a,b,u)\) notation these are

\[
                    (0;0,9,3),\qquad(0;1,8,2).              \tag{2}
\]

Consequently the exact \(p=19\) ledger rises from \(89/94\) to
\(91/94\).  The remaining three profiles are

\[
 2^{10}1^{h+1},\qquad 4\,3^5 1^{h+2},\qquad
 4\,3^5 2\,1^h.                                             \tag{3}
\]

The independent five-triple even-span theorem closes the last two
profiles in (3).  Thus, after combining the two disjoint closures, the
ledger is \(93/94\) and only \(2^{10}1^{h+1}\) remains.  The subsequent
singleton pair-line clique theorem closes that endpoint, making the
combined \(p=19\) ledger \(94/94\).

The new point is that five stationary secants already make every
degree-at-most-four secant curve developable.  The cone and tangent-edge
branches can then be excluded by line-bundle degree, without a
classification of all rational quartics in a Klein hyperplane section.

## 2. The saturated common four-space

Use the same selection as in the singleton common-lift theorem: select
two exact doubles and fix all but one selected singleton.  Let \(P\) be
the moving singleton pool, \(C=7\) the number of fixed complementary
classes, and \({\cal K}\) the common transported kernel.  The exact data
are

\[
\begin{array}{c|c|c|c}
(a,b,u)&P&N&\text{fixed complementary multiplicities}\\ \hline
(0,9,3)&6&11&2,2,2,2,2,2,2\\
(1,8,2)&5&10&3,2,2,2,2,2,2.
\end{array}                                                   \tag{4}
\]

Here the selected relation spaces and their transports are

\[
 \begin{split}
  {\cal S}_q&\subseteq\mathbb C[z]_{\leq P+2},
       &\dim{\cal S}_q&=3,\\
  {\cal T}_q=f_q{\cal S}_q&\subseteq{\cal K}
       \subseteq\mathbb C[z]_{\leq N},
       &f_q&=(z-q)^2(z+q),\qquad N=P+5.                       \tag{5}
 \end{split}
\]

The five-space Wronskian estimate from the common-lift theorem gives
\(\dim{\cal K}\leq4\).  Dimension three is impossible: it would make
all \({\cal T}_q\) equal, so every member of that three-space would be
divisible by the product of the \(P\) pairwise coprime cubics \(f_q\),
whose degree \(3P\) is larger than \(N\).  Therefore

\[
                              \dim{\cal K}=4.                 \tag{6}
\]

An exact order-\(m\) row on a four-space has minimal vanishing sequence
obtained by omitting \(m\) from \((0,1,2,3,4)\), and hence has minimal
Wronskian weight \(4-m\).  The pool rows have order one.  The forced
finite weight in the two rows of (4) is respectively

\[
  6\cdot3+7\cdot2=32,
  \qquad
  5\cdot3+1+6\cdot2=28.                                    \tag{7}
\]

These are exactly the four-space caps

\[
                 4(N+1-4)=32,\qquad28.                       \tag{8}
\]

The equality is genuine.  A positive common-gcd order \(g<m\) at an
order-\(m\) row changes the local lower bound from \(4-m\) to

\[
                         4g+4-(m-g)=5g+4-m>4-m.              \tag{9}
\]

The case \(g=m\) contradicts maximality of the gcd because the exact
row kills the leading coefficient of every reduced section, and
\(g>m\) is still more expensive.  A gcd root away from the displayed
rows costs at least four units.  Thus \({\cal K}\) is base-point-free.

Nor can a pool value be zero.  The transported hyperplane at zero would
be \(z^3{\cal S}_0\), forcing a local sequence at least
\((0,3,4,5)\), of weight six rather than the three units used in (7).
This would exceed (8).  Equality now gives, at every pool value \(q\),

\[
                       (\nu_0,\nu_1,\nu_2,\nu_3)
                              =(0,2,3,4),                     \tag{10}
\]

and there is no other ramification, including at infinity.  In
particular every \(q\ne0\), and \(-q\) is a regular, unlisted point by
structural nonopposition.

Let \(V={\cal K}^*\), choose a basis \(A_0,\ldots,A_3\), and write

\[
                         F(z)=(A_0(z),\ldots,A_3(z))\in V.    \tag{11}
\]

Because \({\cal T}_q\) is a hyperplane contained in both evaluation
kernels at \(q\) and \(-q\), those kernels coincide.  Thus
\([F(q)]=[F(-q)]\).  Equation (10) says that \([F]\) is stationary at
\(q\), while the preceding paragraph says it is regular at \(-q\).

## 3. The quartic secant curve and its Klein hyperplane

Put

\[
                  C_P(x)=\prod_{q\text{ in the pool}}(x-q^2),
 \qquad H_P(z)=zC_P(z^2).                                   \tag{12}
\]

For every \(A,B\in{\cal K}\), the parity determinant

\[
                A(z)B(-z)-A(-z)B(z)                          \tag{13}
\]

is divisible by \(H_P\).  Since its degree is at most
\(2N-1=2P+9\), division gives an even polynomial of degree at most
eight, or a polynomial of degree at most four in \(x=z^2\).  We obtain

\[
 \Phi_{\cal K}:\bigwedge^2{\cal K}\longrightarrow
                         \mathbb C[x]_{\leq4}.                \tag{14}
\]

The domain has dimension six and the target dimension five, so choose

\[
                         0\ne\omega\in\ker\Phi_{\cal K}.     \tag{15}
\]

The image of \(\Phi_{\cal K}\) is not zero.  Otherwise every parity
minor would vanish.  Since \({\cal K}\) is primitive, proportionality of
\(F(z)\) and \(F(-z)\) would have a scalar ratio with constant
denominator; applying the involution twice makes the ratio \(1\) or
\(-1\).  The odd case has the forbidden common factor \(z\), while in
the even case projective ramification occurs at \(q\) and \(-q\)
simultaneously.  This contradicts stationarity at \(q\) and regularity at
\(-q\).  Thus at least one quotient minor below is nonzero.

After removing the common gcd of the six quotient minors, they define a
morphism

\[
 \ell:\mathbb P^1_x\longrightarrow
       \operatorname {Gr}(2,V)\subseteq\mathbb P(\bigwedge^2V),
                   \qquad \deg\ell=d\leq4.                  \tag{16}
\]

For generic \(x=z^2\), \(\ell(x)\) is the line spanned by \(F(z)\)
and \(F(-z)\).  At a pool square, stationarity on the positive branch
and regularity on the negative branch make the parity wedge vanish to
exactly first order.  Hence (16) is defined there and

\[
                             [F(q)]\in\ell(q^2).              \tag{17}
\]

The bivector \(\omega\in\bigwedge^2V^*\) cuts a Pluecker hyperplane,
and (15) says that all of (16) lies in it.  There are exactly two cases:
\(\omega\) is decomposable, in which case every line \(\ell(x)\) meets
one fixed projective line, or \(\omega\) is nondegenerate, in which case
it is a symplectic form and every \(\ell(x)\) is Lagrangian.

## 4. Five stationary squares force developability

We use a short ruled-surface lemma.

**Lemma 4.1 (stationary-section lemma).**  Let
\(\ell:\mathbb P^1\to\operatorname {Gr}(2,V)\) have Pluecker degree
\(d\), and let

\[
 0\longrightarrow{\cal S}\longrightarrow V\otimes{\cal O}
   \longrightarrow{\cal Q}\longrightarrow0                 \tag{18}
\]

be its pulled-back tautological sequence.  Its second fundamental map is

\[
             \beta:{\cal S}\longrightarrow
                         {\cal Q}\otimes\Omega^1_{\mathbb P^1}. \tag{19}
\]

If a local point section \(p(x)\in\mathbb P({\cal S}_x)\) is
projectively stationary in \(\mathbb P(V)\) at \(x_0\), then
\(\beta_{x_0}(p(x_0))=0\).  Moreover

\[
                   \det\beta\in H^0(\mathbb P^1,
                                      {\cal O}(2d-4)).        \tag{20}
\]

Indeed, the derivative of the point section modulo the moving line is
exactly \(\beta(p)\).  Also
\(\det{\cal S}={\cal O}(-d)\),
\(\det{\cal Q}={\cal O}(d)\), and
\((\Omega^1)^{\otimes2}={\cal O}(-4)\), which gives (20).
\(\square\)

Because \(q\ne0\), \(x=z^2\) is a local coordinate at each \(q\).
Thus \(F(\sqrt x)\) supplies the stationary point section in Lemma 4.1.
There are \(P\geq5\) distinct pool squares, whereas

\[
                           2d-4\leq4.                         \tag{21}
\]

It follows that \(\det\beta\equiv0\).  The map \(\ell\) cannot be
constant, since then all evaluation vectors would lie in one fixed
two-space and the four polynomials in (11) would be dependent.  Hence
\(\beta\) has generic rank one.

Let \({\cal R}=\ker\beta\subset{\cal S}\) be the saturated kernel line
bundle and let \(\gamma:\mathbb P^1\to\mathbb P(V)\) be the point curve
it defines.  Differentiating a local section of \({\cal R}\) and using
\(\beta({\cal R})=0\) shows that its tangent direction lies in
\(\ell(x)\).  Thus either \(\gamma\) is constant and \(\ell\) is a cone,
or \(\ell(x)\) is the tangent line of the edge curve \(\gamma\).

## 5. Cones are impossible

Suppose first that \(\gamma=[w]\) is constant.  Then
\({\cal R}={\cal O}\), all lines pass through \([w]\), and (16) is a
degree-\(d\) curve in the alpha plane of lines through \([w]\).  If its
image is contained in a line in that alpha plane, the swept lines lie in
one fixed projective plane, making the four polynomials in (11)
dependent.  We may therefore assume that the direction curve spans the
alpha plane \(\mathbb P^2\).

Let \(c\) be the number of pool squares at which this direction curve is
critical.  A spanning \(g^2_d\) has Wronskian degree \(3(d-2)\), and a
critical point has local sequence at least \((0,2,3)\), of weight at
least two.  Hence

\[
                              2c\leq3(d-2).                   \tag{22}
\]

Let \(\pi:\mathbb P^1_z\to\mathbb P^1_x\) be \(x=z^2\).  The polynomial
map (11) has degree exactly \(N\): otherwise the equality Wronskian in
(7)--(8) would have a base point at infinity.  Its point line bundle is
therefore \({\cal L}_F={\cal O}(-N)\subseteq\pi^*{\cal S}\).  Since
\({\cal S}/{\cal R}={\cal O}(-d)\), projection away from the vertex is a
map

\[
             {\cal O}(-N)\longrightarrow{\cal O}(-2d).      \tag{23}
\]

It is not identically zero, or \(F\) would be the constant point \([w]\).
At every noncritical pool square, Lemma 4.1 makes the stationary point
equal to the vertex.  Both \(z=q\) and \(z=-q\) are therefore zeros of
(23).  Consequently

\[
                 2(P-c)\leq N-2d.                            \tag{24}
\]

Combining (22)--(24) gives

\[
              2P\leq N+d-6=P+d-1,
                  \qquad\text{hence}\qquad P\leq d-1\leq3,  \tag{25}
\]

contrary to \(P\geq5\).

## 6. Tangent edges are impossible

Suppose now that \(\gamma\) is nonconstant.  If its image is planar,
all its tangent lines lie in that fixed plane and the basis in (11) is
again dependent.  Thus assume that \(\gamma\) is nonplanar.  Write

\[
              {\cal R}={\cal O}(-e),\qquad e\geq3.           \tag{26}
\]

If \(\omega\) is decomposable, its Klein hyperplane consists of the
lines meeting a fixed projective line \(L_0\).  Hence every tangent line
of \(\gamma\) meets \(L_0\).  Project from \(L_0\) to \(\mathbb P^1\).
The derivative of this projection along \(\gamma\) vanishes identically,
so in characteristic zero the projection is constant.  The edge curve
then lies in one plane through \(L_0\), contrary to nonplanarity.

It remains to take \(\omega\) nondegenerate.  All \({\cal S}_x\) are
then Lagrangian for the symplectic form \(\omega\).  Symplectic duality
identifies \({\cal Q}\simeq{\cal S}^*\), and the second fundamental form
is symmetric:

\[
                 \beta\in H^0(\operatorname {Sym}^2{\cal S}^*
                                      \otimes\Omega^1).       \tag{27}
\]

Since its kernel is \({\cal R}\), this rank-one form descends to a
nonzero section

\[
 \overline\beta\in H^0\!\left(
          (({\cal S}/{\cal R})^*)^{\otimes2}\otimes\Omega^1
                    \right)
       =H^0\bigl({\cal O}(2(d-e)-2)\bigr).                   \tag{28}
\]

Thus \(d-e\geq1\).  Equations (16) and (26) leave only

\[
                              d=4,\qquad e=3.                 \tag{29}
\]

In particular (28) has degree zero, so \(\beta\) has rank one at every
point.  This is the intrinsic form of the tangent-line curve of a
Legendrian twisted cubic; no choice of its normal form is required.

At every pool square, Lemma 4.1 now forces \([F(q)]\in\mathbb P({\cal
R}_{q^2})\).  Since \([F(-q)]=[F(q)]\), both signs are zeros of the
nonzero quotient map

\[
 {\cal L}_F={\cal O}(-N)\longrightarrow
     \pi^*({\cal S}/{\cal R})={\cal O}(-2).                  \tag{30}
\]

If (30) vanished identically, both branches would lie on the same edge
point \(\gamma(z^2)\), so their generic span would not be the line
\(\ell(z^2)\).  Therefore its zero divisor has degree \(N-2\), and

\[
                       2P\leq N-2=P+3.                       \tag{31}
\]

This is false for both \(P=5\) and \(P=6\).  The cone and tangent-edge
branches exhaust the developable curve, completing the proof of
Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_higher_split_p19_c7_developable_secant_closure.py](../computations/verify_live_three_zero_higher_split_p19_c7_developable_secant_closure.py)
reconstructs the two-profile census and the \(91/94\) ledger, checks the
saturated Wronskian and zero-pool exclusion, audits the quartic parity
quotient and the degree of \(\det\beta\), verifies every cone inequality,
and enumerates the unique nonplanar symplectic degree pair \((d,e)=(4,3)\)
together with its terminal quotient-line contradiction.

[The independent adversarial audit](independent-audit-live-three-zero-higher-split-p19-c7-developable-secant-closure.md)
separately reconstructs the homogeneous infinity argument, quotient-gcd
degree drops, exact divided pool fibers, and both signed terminal zero
counts.
