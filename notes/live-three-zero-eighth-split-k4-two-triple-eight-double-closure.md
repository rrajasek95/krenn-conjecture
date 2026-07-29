# The eighth split at \(k=4\): two triples and eight doubles

## 1. Result

At \((h,k,M)=(8,4,22)\), consider the collision profile

\[
                              \lambda=3^2 2^8.           \tag{1}
\]

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

Choose any five of the eight double values as formal double layers.  The
all-order formal-five-layer theorem identifies the two relation
polynomials with the whole linear space \(\mathbb C[z]_{\le1}\).  At
each of the three outside doubles, the triple-pole residue then kills the
first two derivatives of its regular factor.  Comparing two five/three
partitions puts seven distinct double values in one fibre of a quadratic
rational map.

## 2. The full linear relation pencil

Write \({\cal D}\) for the eight double values and \(a,b\) for the two
triple values.  Fix a five-set \(T\subset{\cal D}\), let

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C(z)=\prod_{u\in{\cal D}\setminus T}(z-u),\qquad
 R(z)=(z-a)(z-b).                                      \tag{2}
\]

The ten formal-five cores lower two of the five double layers from role
two to role one.  Every such core is legal because the two partial
double mates are singleton complement rows.  After lifting, the common
sextic kernel has dimension four and the five value rows have two
relations.

The complementary polynomial is

\[
                              A=C^2R^3.                 \tag{3}
\]

It has degree twelve and exactly five distinct roots.  The all-order
duality theorem therefore maps the two relations injectively to

\[
                    {\cal S}_T\subset\mathbb C[z]_{\le5-4}.
                                                                    \tag{4}
\]

Both spaces in (4) have dimension two, so

\[
                              {\cal S}_T=\mathbb C[z]_{\le1}. 
                                                                    \tag{5}
\]

For every \(S\in{\cal S}_T\), the associated rational derivative is

\[
 G_S'(z)={ (z+\mu)^4Q_T(z)^2S(z)\over C(z)^3R(z)^4}.    \tag{6}
\]

## 3. The outside-double equation

Fix \(u\in{\cal D}\setminus T\), write \(C=(z-u)C_u\), and set

\[
 B_u(z)={ (z+\mu)^4Q_T(z)^2\over C_u(z)^3R(z)^4}.       \tag{7}
\]

This is a unit at \(u\).  Since (6) is a rational derivative, its
residue at the order-three pole \(u\) is zero:

\[
                              (B_uS)''(u)=0             \tag{8}
\]

for every linear \(S\).  Taking \(S=1\) and \(S=z-u\) in (8) gives

\[
                              B_u''(u)=B_u'(u)=0.        \tag{9}
\]

In particular, logarithmic differentiation of (7) gives

\[
 {4\over u+\mu}
 +2\sum_{t\in T}{1\over u+t}
 -3\sum_{v\in({\cal D}\setminus T)\setminus\{u\}}
                         {1\over u-v}
 -4\left({1\over u-a}+{1\over u-b}\right)=0.          \tag{10}
\]

## 4. The partition swap

Fix \(u\in{\cal D}\).  Given distinct values
\(x,y\in{\cal D}\setminus\{u\}\), choose a five/three partition with

\[
                          x\in T,\qquad y\notin T,\qquad u\notin T. \tag{11}
\]

Such a partition exists because five of the seven values other than
\(u\) lie in \(T\).  Swap \(x\) and \(y\) and subtract the two copies
of (10).  Every fixed term cancels, leaving

\[
 {2\over u+x}+{3\over u-x}
       ={2\over u+y}+{3\over u-y}.                      \tag{12}
\]

Thus all seven values in \({\cal D}\setminus\{u\}\) lie in one fibre
of

\[
                 \Phi_u(t)={2\over u+t}+{3\over u-t}
                           ={5u+t\over u^2-t^2}.         \tag{13}
\]

For a fibre value \(\lambda\), clearing the structurally nonzero
denominator gives

\[
                         \lambda(u^2-t^2)-5u-t=0.       \tag{14}
\]

This is a nonzero polynomial of degree at most two: its coefficient of
\(t\) is \(-1\).  It cannot have seven distinct roots.  This proves
Theorem 1.1.

## 5. Exact audit

[verify_live_three_zero_eighth_split_k4_two_triple_eight_double_closure.py](../computations/verify_live_three_zero_eighth_split_k4_two_triple_eight_double_closure.py)
checks all 560 legal formal-five cores, the complementary degrees, the
all-order derivative specialization, the exact triple-pole rows on
\(\mathbb C[z]_{\le1}\), every five/three swap, and the quadratic fibre
contradiction.
