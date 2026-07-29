# The eighth split: mixed-layer closure of the terminal two-triple profile

## 1. Result

At \(h=8,k=3\), consider

\[
                         \lambda=3^2 2^4 1^7.            \tag{1}
\]

Write \(a,b\) for the two triple values, \({\cal D}\) for the four
double values, and \({\cal R}\) for the seven singleton values.  Every
repeated value is nonzero; one member of \({\cal R}\) may be zero.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

Choose one double at formal role two and all seven singleton layers at
formal role one.  Lowering one role gives legal eight-label cores, except
that an omitted zero singleton is simply discarded.  Their lifted
residuals fill a three-dimensional kernel in
\(\mathbb C[z]_{\le7}\).  The three relations among its eight value rows
dualize injectively to a hyperplane in \(\mathbb C[z]_{\le3}\).

The three outside-double residue rows all have that hyperplane as their
kernel.  Consequently the cube centred at each outside double lies in
the common hyperplane.  This determines the first logarithmic jet of
each row.  Comparing it for two choices of the formally selected double
forces two distinct double values to be equal or opposite, contrary to
the standing structural assumptions.

## 2. One double layer and seven singleton layers

Fix \(x\in{\cal D}\), put \(C={\cal D}\setminus\{x\}\), and define

\[
\begin{aligned}
 H(z)&=\prod_{r\in{\cal R}}(z+r),\\
 A(z)&=(z-a)^3(z-b)^3\prod_{u\in C}(z-u)^2.
\end{aligned}                                           \tag{2}
\]

The formal target assigns role two to \(x\) and role one to each member
of \({\cal R}\), for total role

\[
                              2+7=9.                    \tag{3}
\]

For the double layer and the singleton layers respectively, set

\[
 f_x(z)=z^2-x^2,
 \qquad f_r(z)=(z-r)(z+r)^2.                            \tag{4}
\]

First lower the role at \(x\).  The resulting core selects one label at
\(x\) and all seven singleton labels.  Its complement contains the
nonzero mate at \(x\), so the simultaneous-Hermite reduction gives

\[
                         0\ne q_x\in\mathbb C[z]_{\le5}. \tag{5}
\]

Alternatively, lower the role at a nonzero singleton \(r\).  The core
selects both labels at \(x\), omits \(r\), and selects the other six
singleton labels.  The omitted nonzero singleton is a guard, hence

\[
                         0\ne q_r\in\mathbb C[z]_{\le4}. \tag{6}
\]

If one singleton value is zero, the single core which omits it need not
be used.  All other cores remain legal.  The exact lift identities

\[
 {z-x\over(z+x)^2}={z^2-x^2\over(z+x)^3},
 \qquad
 z-r={(z-r)(z+r)^2\over(z+r)^2}                         \tag{7}
\]

give

\[
 P_x=f_xq_x,qquad P_r=f_rq_r,qquad
                         0\ne P_i\in\mathbb C[z]_{\le7}. \tag{8}
\]

Every lifted rational dependence has the common form

\[
 F_P(z)={A(z)P(z)\over
              (z+\mu)^4(z+x)^3H(z)^2}.                 \tag{9}
\]

The numerator and denominator degrees are at most nineteen and
twenty-one, so \(F_P=O(z^{-2})\).

Define

\[
\begin{aligned}
 K_x={}&\{P\in\mathbb C[z]_{\le7}:
       \operatorname {res}_{z=-x}F_P=0,\ 
       \operatorname {res}_{z=-r}F_P=0\ (r\in{\cal R})\},\\
 W_x={}&\operatorname {span}\bigl(\{P_x\}\cup
                   \{P_r:r\in{\cal R},\ r\ne0\}\bigr).
\end{aligned}                                           \tag{10}
\]

Thus \(W_x\subseteq K_x\).  The row at \(-x\) has exact differential
order two and the seven rows at \(-r\) have exact order one.  The residue
theorem also supplies the exact order-three common-pole row, although it
is not needed for the next dimension bound.

## 3. The kernel has dimension at most three

Let \(d=\dim K_x\), remove its polynomial gcd, and first suppose that
the gcd is a unit at all eight value nodes.  The order-two row forces
Wronskian weight \(d-2\), while the seven order-one rows force
\(7(d-1)\).  The Wronskian degree cap for a \(d\)-space in
\(\mathbb C[z]_{\le7}\) is \(d(8-d)\).  The forced weight minus this cap
is

\[
                  (d-2)+7(d-1)-d(8-d)=d^2-9,           \tag{11}
\]

which is positive for every \(d\ge4\).

The gcd corrections only strengthen (11).  At the order-two node, a
simple gcd zero increases the deficit by \(d+1\), an order-two zero is
impossible after gcd removal, and an absorbed zero of order at least
three increases it by at least \(2d+2\).  At an order-one node, a simple
gcd zero is impossible and an absorbed zero of order at least two
increases the deficit by at least \(d+1\).  Roots away from the eight
nodes only lower the degree cap.  Therefore

\[
                              \dim K_x\le3.              \tag{12}
\]

## 4. The lifts span three dimensions

Put \({\cal R}^{\times}={\cal R}\setminus\{0\}\) and
\(s=|{\cal R}^{\times}|\), so \(s=6\) or \(7\).  The polynomials

\[
                         f_x,\qquad f_r\ (r\in{\cal R}^{\times}) 
                                                               \tag{13}
\]

are pairwise coprime, and their product has degree

\[
                              2+3s\ge20>7.              \tag{14}
\]

Hence \(W_x\) is not a line.  Suppose it were a pencil, with basis
\({\bf P}(z)=(P_0(z),P_1(z))\).  For every available layer value
\(v\in\{x\}\cup{\cal R}^{\times}\), a nonzero member of the pencil is
divisible by \(f_v\).  The two evaluation vectors
\({\bf P}(v),{\bf P}(-v)\) are therefore proportional, so the odd parity
minor

\[
                 D(z)=P_0(z)P_1(-z)-P_0(-z)P_1(z)       \tag{15}
\]

vanishes at \(\pm v\).  It also vanishes at zero and has degree at most
thirteen.  But (15) has at least

\[
                         2(s+1)+1\ge15                 \tag{16}
\]

distinct roots.  Thus \(D=0\).

Remove the gcd \(G\) of the pencil.  Its primitive basis is projectively
even; the odd alternative would leave a common factor \(z\).  Hence

\[
                         W_x=G(z){\cal E}(z^2),          \tag{17}
\]

where \({\cal E}\subset\mathbb C[t]\) is a primitive
two-dimensional space.  Write \(g=\deg G\), and let \(m\) count the
members \(r\in{\cal R}^{\times}\) for which \(G(-r)=0\).  Then \(g\ge m\)
and the maximum degree in \({\cal E}\) is at most

\[
                         n\le\left\lfloor{7-m\over2}\right\rfloor. 
                                                               \tag{18}
\]

For every one of the other \(s-m\) singleton values, the image in
\({\cal E}\) of \(P_r/G\) is divisible by \((t-r^2)^2\).  Primitivity
supplies another member which is a unit at \(t=r^2\), so the Wronskian of
\({\cal E}\) has weight at least one there.  The squared values are
distinct, and consequently

\[
 s-m\le\deg\operatorname {Wr}({\cal E})
       \le2(n-1)
       \le2\left(\left\lfloor{7-m\over2}\right\rfloor-1\right). 
                                                               \tag{19}
\]

For \(s=6\) or \(7\), (19) fails for every \(0\le m\le5\); when
\(m\ge6\), (18) cannot support a two-dimensional \({\cal E}\).  Thus
\(W_x\) is not a pencil.  Combining this with (12) gives

\[
                         W_x=K_x,\qquad \dim K_x=3.      \tag{20}
\]

## 5. Duality gives a cubic hyperplane

Put

\[
                 \Omega_x(z)={A(z)\over
                 (z+\mu)^4(z+x)^3H(z)^2}.              \tag{21}
\]

The eight selected value rows act on the eight-dimensional space
\(\mathbb C[z]_{\le7}\).  By (20), their rank is five, so their relation
space is three-dimensional.  For a relation \(c\), sum the corresponding
principal parts of \(\Omega_x\) at \(-x\) and the seven nodes \(-r\).
The relation annihilates \(1,z,\ldots,z^7\), hence the sum is

\[
                  J_c(z)={N_c(z)\over(z+x)^3H(z)^2},
                  \qquad \deg N_c\le8.                 \tag{22}
\]

Disjoint principal-part supports make \(c\mapsto N_c\) injective.  Divide
by (21):

\[
                         G_N(z)={(z+\mu)^4N(z)\over A(z)}. \tag{23}
\]

At \(-x\), the derivative \(G_N'\) has a double zero; at every \(-r\),
it has a simple zero.  Define

\[
 g_A=(z-a)^2(z-b)^2\prod_{u\in C}(z-u),\qquad
 R_A={A\over g_A},\qquad D_A={A'\over g_A}.             \tag{24}
\]

Here \(\deg R_A=5\), \(\deg D_A=4\), and the leading coefficient of
\(D_A\) is twelve.  Direct differentiation gives

\[
 G_N'={(z+\mu)^3g_A\over A^2}{\cal E}_A(N),             \tag{25}
\]

where

\[
 {\cal E}_A(N)=R_A\bigl((z+\mu)N'+4N\bigr)
                    -(z+\mu)D_A N.                     \tag{26}
\]

If \(n=\deg N\le8\), the nominal leading coefficient in degree \(n+5\)
is \(n+4-12=n-8\).  It cancels for \(n=8\), while for \(n\le7\) the
nominal degree is already at most twelve.  Therefore the selected-node
zeros imply

\[
                         {\cal E}_A(N)=(z+x)^2H(z)S_N(z),
             \qquad S_N\in\mathbb C[z]_{\le3}.         \tag{27}
\]

The map \(N\mapsto S_N\) is injective.  If \(S_N=0\), then (25) makes
\(G_N\) constant, and evaluation of
\((z+\mu)^4N=\gamma A\) at \(-\mu\) forces \(\gamma=N=0\).  The
three-dimensional relation space therefore maps to a hyperplane

\[
                         {\cal S}_x\subset\mathbb C[z]_{\le3},
                         \qquad\dim{\cal S}_x=3.         \tag{28}
\]

## 6. Outside-double cubes and the partition swap

Substituting (27) into (25) gives, for every
\(S\in{\cal S}_x\),

\[
 G_S'(z)={ (z+\mu)^3(z+x)^2H(z)S(z)\over
            (z-a)^4(z-b)^4\displaystyle\prod_{u\in C}(z-u)^3}. 
                                                               \tag{29}
\]

Fix \(u\in C\), write \(C=\{u,v,w\}\), and let \(B_u\) be the regular
factor in (29) after removing \((z-u)^{-3}\).  Put

\[
                         X_u={B_u'(u)\over B_u(u)},
             \qquad Z_u={B_u''(u)\over B_u(u)}.          \tag{30}
\]

The zero residue at the triple pole is the nonzero row

\[
                         S''(u)+2X_uS'(u)+Z_uS(u)=0.     \tag{31}
\]

It annihilates the hyperplane (28), so its kernel is exactly
\({\cal S}_x\).  In particular, the row at \(v\) puts
\((z-v)^3\) in \({\cal S}_x\), and similarly for \(w\).  Applying the
row at \(u\) to these two cubics shows that both \(u-v\) and \(u-w\) are
roots of

\[
                         6+6X_u\delta+Z_u\delta^2.       \tag{32}
\]

Their product is nonzero, so comparison of coefficients yields

\[
                         X_u=-{1\over u-v}-{1\over u-w}. \tag{33}
\]

On the other hand, logarithmic differentiation of the regular factor in
(29) gives

\[
 X_u={3\over u+\mu}+{2\over u+x}
      +\sum_{r\in{\cal R}}{1\over u+r}
      -{4\over u-a}-{4\over u-b}
      -3\sum_{t\in C\setminus\{u\}}{1\over u-t}.       \tag{34}
\]

Let

\[
 \Gamma(u)={3\over u+\mu}
      +\sum_{r\in{\cal R}}{1\over u+r}
      -{4\over u-a}-{4\over u-b}.                      \tag{35}
\]

Equations (33)--(34) imply, for every ordered pair of distinct double
values \(u,x\),

\[
 \Gamma(u)+{2\over u+x}
      -2\sum_{t\in{\cal D}\setminus\{u,x\}}{1\over u-t}=0. 
                                                               \tag{36}
\]

Fix \(u\), and choose two distinct values \(x,y\in{\cal D}\setminus
\{u\}\) as the formally selected double.  Subtracting the two instances
of (36) cancels \(\Gamma(u)\) and the fourth double, leaving

\[
 {1\over u+x}+{1\over u-x}
       ={1\over u+y}+{1\over u-y}.                      \tag{37}
\]

Since \(u\ne0\), this is

\[
                         {2u\over u^2-x^2}
                              ={2u\over u^2-y^2},       \tag{38}
\]

and hence \(x^2=y^2\).  The double values are distinct and
nonopposite, a contradiction.  This proves Theorem 1.1, uniformly when
one singleton is zero.

## 7. Census consequence and exact audit

Theorem 1.1 closes the terminal profile \(3^2 2^4 1^7\).

[verify_live_three_zero_eighth_split_k3_two_triple_mixed_layer_closure.py](../computations/verify_live_three_zero_eighth_split_k3_two_triple_mixed_layer_closure.py)
checks every legal single-drop core in both zero-singleton cases, the
lift and degree identities, all gcd-corrected kernel bounds, the parity
root count and reduced-Wronskian obstruction, the three-dimensional
relation count, the differential degree cancellation and injectivity,
the outside-cube row calculation, and the final partition swap.
