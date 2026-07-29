# Higher splits: a uniform developable-secant lemma

## 1. Result and scope

Work in the exact
[moving-singleton common-lift setup](live-three-zero-higher-split-p19-singleton-parity-common-lift-closure.md).
There are \(P\)
moving singleton value classes and \(C\) fixed complementary classes of
multiplicities

\[
                         m_1,\ldots,m_C.                       \tag{1}
\]

For every moving value \(q\), the selected relation three-space and its
cubic transport are

\[
 \mathcal S_q\subseteq\mathbb C[z]_{\leq P+C-5},\qquad
 \mathcal T_q=(z-q)^2(z+q)\mathcal S_q\subseteq\mathcal K
       \subseteq\mathbb C[z]_{\leq N},\qquad N=P+C-2.          \tag{2}
\]

The values satisfy the standard structural conditions: distinct value
classes are distinct and nonopposite, repeated values are nonzero, and
at most one moving singleton is zero.  The baseline rows are exact: they
have order one at each of the \(P\) moving values and order \(m_i\) at
the fixed values.

Define the four-capped complementary mass

\[
                   M_4=(P-1)+\sum_{i=1}^C\min(m_i,4).          \tag{3}
\]

**Theorem 1.1 (uniform developable-secant lemma).**  A configuration
as above is impossible if

\[
             \boxed{M_4=19,\qquad 4\leq C\leq7,\qquad
                    P\geq\max(1,2C-9).}                       \tag{4}
\]

This is a parameter-uniform form of the stationary-secant argument used
at \(p=19,C=7\).  It is not a theorem for arbitrary \(C\): the bound
\(C\leq7\) is exactly what forces the secant curve into a Klein
hyperplane.  Nor does it cover an unsaturated four-space with
\(M_4>19\).

The first new application beyond the completed \(p=19\) diagonal is the
\(p=20\) one-quintuple branch.

**Corollary 1.2 (four \(p=20\) families).**  For every
\(13\leq h\leq19\), none of

\[
 \boxed{
  5\,2^7 1^{h+3},\quad
  5\,3\,2^6 1^{h+2},\quad
  5\,3^2 2^5 1^{h+1},\quad
  5\,3^3 2^4 1^h
 }                                                            \tag{5}
\]

can occur in the exact higher-split configuration.

The proof below includes the common-factor and infinity cases and keeps
the actual Pluecker degree after every possible degree drop.

## 2. The common kernel is a saturated four-space

First, the five-space estimate from the singleton common-lift theorem
applies automatically.  Put

\[
                  M_5=(P-1)+\sum_i\min(m_i,5).                 \tag{6}
\]

Every fixed class contributes at most one unit more to \(M_5\) than to
\(M_4\), so (4) gives

\[
                         M_5\leq19+C\leq26<29.                 \tag{7}
\]

If \(\mathcal K\) contained a five-space, its exact rows would force
Wronskian weight

\[
             4P+\sum_i\max(0,5-m_i)=4P+5C-(M_5-P+1),          \tag{8}
\]

whereas its degree cap would be

\[
                         5(N+1-5)=5(P+C-6).                   \tag{9}
\]

The difference between (8) and (9) is \(29-M_5>0\).  Hence

\[
                              \dim\mathcal K\leq4.             \tag{10}
\]

Each \(\mathcal T_q\) is a three-space.  If
\(\dim\mathcal K=3\), all the \(\mathcal T_q\)'s equal
\(\mathcal K\).  The cubics

\[
                              f_q=(z-q)^2(z+q)                 \tag{11}
\]

are pairwise coprime by nonopposition.  Thus a three-space of degree at
most \(N\) would consist of multiples of their degree-\(3P\) product.
This requires

\[
                              3P\leq N-2.                      \tag{12}
\]

On the other hand, (4) implies \(2P>C-4\), and hence
\(3P>N-2=P+C-4\).  Therefore

\[
                              \dim\mathcal K=4.                \tag{13}
\]

For a four-space, an exact order-\(m\) row has minimal Wronskian
weight \(\max(0,4-m)\).  The finite forced weight is consequently

\[
 \begin{split}
  3P+\sum_i\max(0,4-m_i)
    &=3P+4C-\sum_i\min(m_i,4)\\
    &=4P+4C-20\\
    &=4(N+1-4),                                               \tag{14}
 \end{split}
\]

the full polynomial Wronskian cap.

There is no hidden common gcd.  If the gcd has order \(g>0\) at an
exact order-\(m\) row and \(g<m\), division changes the local lower
bound to

\[
                 4g+\max(0,4-(m-g))>\max(0,4-m).              \tag{15}
\]

If \(g=m\), the exact order-\(m\) equation kills the leading coefficient
of every reduced section, contradicting maximality of \(g\).  If
\(g>m\), the contribution \(4g\) is again strictly larger.  A gcd root
away from a displayed row costs at least four new units.  Thus
\(\mathcal K\) is primitive.

No moving value can be zero.  At \(q=0\), the three-space
\(\mathcal T_0=z^3\mathcal S_0\) would force local sequence at least
\((0,3,4,5)\), of weight six, in place of the three units in (14).
It follows that all pool values are nonzero and that the exact local
sequence at each of them is

\[
                              (0,2,3,4).                       \tag{16}
\]

There is no other ramification.  This includes infinity: if the
echelon degrees are \(n_0<\cdots<n_3\leq N\), then

\[
 \deg\operatorname{Wr}(\mathcal K)
          \leq\sum_i n_i-6\leq4N-12.                          \tag{17}
\]

The finite rows already contribute \(4N-12\), so the echelon degrees
are \((N-3,N-2,N-1,N)\), the top Wronskian coefficient is nonzero, and
the homogenized point map has neither a base point nor ramification at
infinity.  In particular its point line is

\[
                    \mathcal L_F=\mathcal O_{\mathbb P^1_z}(-N). \tag{18}
\]

Choose a basis of \(\mathcal K\) and let

\[
                           F(z)=(A_0(z),\ldots,A_3(z)).        \tag{19}
\]

The transported hyperplane \(\mathcal T_q\) is contained in both
evaluation kernels at \(q\) and \(-q\).  By (13) and primitivity,

\[
 \ker E_q=\mathcal T_q=\ker E_{-q},\qquad
 [F(q)]=[F(-q)],\qquad F'(q)\in\langle F(q)\rangle.             \tag{20}
\]

The negative point \(-q\) is unlisted by nonopposition.  Saturation
therefore gives

\[
                          F'(-q)\notin\langle F(-q)\rangle.    \tag{21}
\]

## 3. The secant curve, including all degree drops

Let

\[
 C_P(x)=\prod_{q\in P}(x-q^2),\qquad H_P(z)=zC_P(z^2).         \tag{22}
\]

The parity wedge

\[
                         W(z)=F(z)\wedge F(-z)                 \tag{23}
\]

is an odd vector polynomial, has degree at most \(2N-1\), and is
divisible by \(H_P\).  Therefore

\[
                     \frac{W(z)}{H_P(z)}=Q(z^2),\qquad
             Q\in\bigwedge^2\mathbb C^4\otimes
                       \mathbb C[x]_{\leq C-3}.               \tag{24}
\]

The root removed at every pool square is exactly simple as a vector
root.  After rescaling \(F(-q)=\mu F(q)\), equations (20)--(21) give

\[
 W'(q)=-F(q)\wedge F'(-q)\ne0                                \tag{25}
\]

up to the harmless nonzero rescaling term.  Hence no common factor of
the six coordinates of \(Q\) contains a pool square, and the divided
fiber represents

\[
                         \langle F(q),F'(-q)\rangle.           \tag{26}
\]

Remove the complete homogeneous gcd of the six coordinates, including
any factor at infinity, and lower the homogeneous degree if all leading
coefficients vanish.  This gives a base-point-free morphism

\[
 \ell:\mathbb P^1_x\longrightarrow\operatorname{Gr}(2,4),
                    \qquad d=\deg\ell\leq C-3,                \tag{27}
\]

whose pool fibers still contain \([F(q)]\).

The vector \(Q\) is not identically zero.  Otherwise primitivity would
give \(F(-z)=cF(z)\) with constant \(c=\pm1\).  The odd case gives the
forbidden common factor \(z\); in the even case stationarity at \(q\)
also forces stationarity at \(-q\), contrary to (21).  The morphism
\(\ell\) is not constant either, since then every generic \(F(z)\)
would lie in one fixed projective line and the four basis polynomials
would be dependent.

The six Pluecker coordinates in (24) lie in a vector space of dimension
at most \(C-2\leq5\).  Thus there is a nonzero alternating form
\(\omega\) whose Klein hyperplane contains the whole secant curve.  In
dimension four, \(\omega\) is either decomposable or symplectic.

## 4. Stationary sections force developability

Pull back the tautological sequence:

\[
 0\longrightarrow\mathcal S\longrightarrow V\otimes\mathcal O
   \longrightarrow\mathcal Q\longrightarrow0,\qquad
 \beta:\mathcal S\longrightarrow
              \mathcal Q\otimes\Omega^1_{\mathbb P^1}.       \tag{28}
\]

Here \(\det\mathcal S=\mathcal O(-d)\) and
\(\det\mathcal Q=\mathcal O(d)\), so

\[
              \det\beta\in H^0(\mathbb P^1,\mathcal O(2d-4)). \tag{29}
\]

Because every \(q\ne0\), \(x=z^2\) is a local coordinate at \(q\).
The local section \(F(\sqrt x)\) is projectively stationary, so its
pool fiber lies in \(\ker\beta\).  By (4) and (27),

\[
                 P\geq2C-9>2C-10\geq2d-4.                    \tag{30}
\]

Thus $\det\beta=0$.  Since $\ell$ is nonconstant, $\beta$ has
generic rank one.  Let

\[
                     \mathcal R=\ker\beta=\mathcal O(-e)      \tag{31}
\]

denote its saturated kernel.  The associated edge point curve
\(\gamma:\mathbb P^1\to\mathbb P(V)\) has its tangent direction in
\(\ell(x)\).  If \(\gamma\) is constant, \(\ell\) is a cone.  Otherwise
\(\ell\) is the tangent-line curve of \(\gamma\).  Isolated critical
points of either map do not affect this dichotomy.

## 5. Exact terminal inequalities

### 5.1 Cone branch

If the edge is a constant vertex, then \(\mathcal R=\mathcal O\) and
\(\mathcal S/\mathcal R=\mathcal O(-d)\).  A direction image contained
in a projective line would sweep one fixed projective plane and make the
four polynomials dependent.  Hence the direction curve is a
base-point-free spanning \(g^2_d\), in particular \(d\geq2\).

Let \(c\) be the number of pool squares at which the direction curve is
critical.  Its Wronskian has degree \(3(d-2)\), and each critical point
has weight at least two.  Therefore

\[
                              2c\leq3(d-2).                    \tag{32}
\]

After the square cover, projection away from the vertex is the nonzero
bundle map

\[
          \mathcal O(-N)\longrightarrow\mathcal O(-2d).      \tag{33}
\]

At every noncritical pool square, the stationary point must be the
vertex.  Both distinct signed points \(q,-q\) are zeros of (33), giving

\[
                            2(P-c)\leq N-2d.                   \tag{34}
\]

Combining (32)--(34) gives the exact relaxed cone obstruction

\[
                            P\leq C+d-8\leq2C-11.              \tag{35}
\]

This contradicts \(P\geq2C-9\).

### 5.2 Tangent edge in a decomposable Klein hyperplane

A planar edge again makes the basis dependent, so take a nonplanar
edge.  Then \(e\geq3\).  If
\(\omega=u\wedge v\) is decomposable, every tangent line meets the fixed
line cut out by \(u=v=0\).  The Schubert equation is

\[
 (u\circ\gamma)(v\circ\gamma)'
       -(v\circ\gamma)(u\circ\gamma)'=0.                      \tag{36}
\]

After cancelling any common factor, (36) says that the rational
projection \([u\circ\gamma:v\circ\gamma]\) has zero derivative.  In
characteristic zero it is constant.  Thus the edge lies in a projective
plane through the fixed line, a contradiction.  This also covers the
case in which the edge meets or lies in the projection center.

### 5.3 Tangent edge in a symplectic Klein hyperplane

If $\omega$ is symplectic, $\mathcal Q\simeq\mathcal S^*$ and
$\beta$ is symmetric.  Put

\[
                              k=d-e.                          \tag{37}
\]

The rank-one form descends to a nonzero section

\[
 \overline\beta\in H^0\!\left(
       ((\mathcal S/\mathcal R)^*)^{\otimes2}\otimes\Omega^1
                         \right)
       =H^0(\mathcal O(2k-2)).                                \tag{38}
\]

Consequently \(k\geq1\).  If \(s\) pool squares are zeros of
\(\overline\beta\), then

\[
                         s\leq2k-2.                           \tag{39}
\]

At every other pool square the stationary point is the edge point.
The nonzero quotient map

\[
       \mathcal O(-N)\longrightarrow
          \pi^*(\mathcal S/\mathcal R)=\mathcal O(-2k)       \tag{40}
\]

therefore has both signed pool points as zeros, and

\[
                       2(P-s)\leq N-2k.                       \tag{41}
\]

Equations (39)--(41) are the exact symplectic inequalities, including
possible zeros of the second fundamental form.  They imply the relaxed
bound

\[
                            P\leq C+2k-6.                      \tag{42}
\]

In the range of Theorem 1.1, \(d\leq C-3\leq4\), while \(e\geq3\) and
\(k\geq1\).  Thus the only possible degree pair is

\[
                         C=7,\qquad(d,e,k)=(4,3,1).            \tag{43}
\]

Now (38) has degree zero, so \(s=0\), and the sharper (41) gives

\[
                       2P\leq N-2=P+C-4,qquad P\leq C-4=3.   \tag{44}
\]

This contradicts \(P\geq2C-9=5\).  The cone, decomposable tangent, and
symplectic tangent cases exhaust the developable curve, proving
Theorem 1.1.

All zero counts above are on complete projective lines.  Zeros at
infinity only consume more of the available degree.  Likewise, a common
factor in (24) lowers \(d\) and strengthens (30), (35), and the list of
possible symplectic pairs; none of the arguments assumes raw degree
\(C-3\) is attained.

## 6. The first post-\(p=19\) application

At \(p=20\), the exact
[\(q=5\) boundary theorem](live-three-zero-higher-split-q5-boundary-census.md)
permits high excess at most two.
For \(13\leq h\leq19\), its selected-row \(q=6\) gap is

\[
                 22-h+\max(0,6-(20-h))>0.
\]

Thus the selected kernel has dimension at most five.  Pair drops give
dimension at least four, and the low-role incidence theorem excludes
dimension four; in a hypothetical surviving configuration it is exactly
five, so the relation three-spaces required in (2) are present.
The one-quintuple families have the form

\[
              5\,3^a2^b1^{h+u},\qquad3a+2b+u=17.             \tag{45}
\]

For the four choices

\[
                         b=7-a,qquad0\leq a\leq3,            \tag{46}
\]

select two doubles and fix all but one selected singleton.  The exact
data are

\[
\begin{array}{c|c|c|c|c|c}
a&b&u&P&N&\text{fixed multiplicities}\\ \hline
0&7&3&6&10&5,2,2,2,2,2\\
1&6&2&5&9&5,3,2,2,2,2\\
2&5&1&4&8&5,3,3,2,2,2\\
3&4&0&3&7&5,3,3,3,2,2.
\end{array}                                                   \tag{47}
\]

In every row \(C=6\), the five-capped complementary mass is \(20\),
and the four-capped mass is

\[
       (P-1)+4+3a+2(5-a)=19.                                 \tag{48}
\]

Also \(P=6-a\geq3=2C-9\).  Theorem 1.1 applies and gives precisely the
four profiles in (5).

This application is deliberately limited.  The next \(C=6\) quintuple
profile has \(P=2\); a degree-three secant curve may then have
\(\det\beta\in H^0(\mathcal O(2))\) vanishing at exactly the two pool
squares, so developability is not forced.  The \(C=7\) quintuple
profiles have \(P\leq4<5\).  For \(C\geq8\), the six quotient
coordinates need not satisfy any linear Klein equation.  Finally, the
other new \(p=20\) branch, containing two quadruple classes, has
\(M_4=20\), leaving one unused Wronskian unit; the saturation conclusions
of Section 2 do not apply.

## 7. Exact audit

[verify_live_three_zero_higher_split_uniform_developable_secant_lemma.py](../computations/verify_live_three_zero_higher_split_uniform_developable_secant_lemma.py)
checks the capped-mass algebra, gcd corrections, homogeneous parity
degree, exact pool-square division, all stationary/developable degree
inequalities, and every formal \(p=20\) selection in (47).

The
[independent adversarial audit](live-three-zero-higher-split-uniform-developable-secant-lemma-independent-audit.md)
reconstructs the proof and uses a checker that imports neither this
checker nor the census implementation.  It exhausts every attainable
four-capped multiplicity pattern, homogeneous degree drop, cone critical
budget, and symplectic edge degree.
