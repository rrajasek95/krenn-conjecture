# Higher splits: the \(p=18\) two-triple endpoint frontier

## 1. The exact nine-family block

Work on the no-extra-singular live-three-zero stratum with

\[
                     p=h+k=18,\qquad 13\leq h\leq17.              \tag{1}
\]

After the closure of every family with at least three triples, the next
block consists of the nine profiles

\[
                    3^2 2^b1^{h+14-2b},\qquad 0\leq b\leq8.       \tag{2}
\]

Indeed, \(3a+2b+u=20\) gives \(u=14-2b\) at \(a=2\), and the
formal-selection applicability alternatives stop exactly at \(b=8\).
Write \(d\in\{0,1,2\}\) for the number of role-two layers and
\(t\in\{0,1\}\) for the number of selected exact triples.  The full
selection table is

\[
\begin{array}{c|l}
b&(d,t):\text{ complementary profile}\\ \hline
0&(0,0):3^2 1^{12};\ (1,1):3 1^{15}\\
1&(0,0):3^2 2 1^{10};\ (1,0):3^2 1^{12};\
  (1,1):3 2 1^{13};\ (2,1):3 1^{15}\\
2&(0,0):3^2 2^2 1^8;\ (1,0):3^2 2 1^{10};\
  (1,1):3 2^2 1^{11};\ (2,0):3^2 1^{12};\
  (2,1):3 2 1^{13}\\
3&(0,0):3^2 2^3 1^6;\ (1,0):3^2 2^2 1^8;\
  (1,1):3 2^3 1^9;\ (2,0):3^2 2 1^{10};\
  (2,1):3 2^2 1^{11}\\
4&(0,0):3^2 2^4 1^4;\ (1,0):3^2 2^3 1^6;\
  (1,1):3 2^4 1^7;\ (2,0):3^2 2^2 1^8;\
  (2,1):3 2^3 1^9\\
5&(0,0):3^2 2^5 1^2;\ (1,0):3^2 2^4 1^4;\
  (1,1):3 2^5 1^5;\ (2,0):3^2 2^3 1^6;\
  (2,1):3 2^4 1^7\\
6&(0,0):3^2 2^6;\ (1,0):3^2 2^5 1^2;\
  (1,1):3 2^6 1^3;\ (2,0):3^2 2^4 1^4;\
  (2,1):3 2^5 1^5\\
7&(1,0):3^2 2^6;\ (1,1):3 2^7 1;\
  (2,0):3^2 2^5 1^2;\ (2,1):3 2^6 1^3\\
8&(2,0):3^2 2^6;\ (2,1):3 2^7 1.
\end{array}                                                       \tag{3}
\]

As in the preceding overlap notes, simultaneous equality gives a
three-dimensional gcd-free relation space

\[
                    {\cal S}\subseteq\mathbb C[z]_{\leq c-4},    \tag{4}
\]

whose Wronskian has weight two at each simple complementary value and
weight one at each double complementary value.

There is useful hidden repetition in (3).  The no-selected-triple
choices divide the block into three consecutive packets:

\[
\begin{array}{c|c|c}
b&d&\text{common complement}\\ \hline
0,1,2&b&3^2 1^{12}\\
3,4,5&b-3&3^2 2^3 1^6\\
6,7,8&b-6&3^2 2^6.
\end{array}                                                       \tag{5}
\]

Thus selected-double exchange can be carried out inside each packet
without changing the complementary Schubert type.

## 2. The bare \(3^2 2^6\) Wronski problem is dominant

For the endpoint complement

\[
                         3^2 2_{v_1}\cdots2_{v_6},                \tag{6}
\]

one has \(c=8\), so \({\cal S}\) is a three-space in
\(\mathbb C[z]_{\leq4}\), and saturation says only

\[
                 \operatorname {Wr}({\cal S})
                         =C\prod_{i=1}^6(z-v_i).                  \tag{7}
\]

Unlike the preceding \(3^3 2^4 1\) endpoint, (7) supplies no scalar
Schubert equation.  This can be seen without a dimension heuristic.
On the standard affine chart of \(\operatorname {Gr}(3,5)\), put

\[
\begin{split}
 f_0&=1+x_0z^3+x_1z^4,\\
 f_1&=z+x_2z^3+x_3z^4,\\
 f_2&=z^2+x_4z^3+x_5z^4.
\end{split}                                                       \tag{8}
\]

The constant coefficient of \(\operatorname {Wr}(f_0,f_1,f_2)\) is
two.  At

\[
                 (x_0,\ldots,x_5)=(-2,-2,-2,-1,-2,-2),           \tag{9}
\]

the Jacobian of its six remaining coefficients has determinant

\[
                              -1430784\ne0.                       \tag{10}
\]

Hence the Wronski map is dominant.  The same witness gives

\[
 \operatorname {Wr}(f_0,f_1,f_2)
   =-2(2z^6-6z^4-6z^3+6z^2+6z-1),                               \tag{11}
\]

which is squarefree, has nonzero constant term, and is coprime to its
sign reversal.  Thus even the distinct, nonzero, pairwise-nonopposite
root conditions do not repair a Wronskian-only argument.  Equation (11)
is a local Schubert witness, not a realization of the collision profile:
the exact residue rows below retain additional data.

## 3. The neighboring \(3\,2^7 1\) image is a quintic

The selected-triple neighbor in the last two rows of (3) has complement

\[
                        3_x\,2_{v_1}\cdots2_{v_7}\,1_r.          \tag{12}
\]

Shift \(r\) to zero.  The simple-root residue row is

\[
                         D_0+\beta E_0,                           \tag{13}
\]

so its kernel in \(\mathbb C[z]_{\leq5}\) has basis

\[
              h_0=1-\beta z,\qquad h_1=z^2,\quad h_2=z^3,
                         \quad h_3=z^4,\quad h_4=z^5.             \tag{14}
\]

For \(I=\{i,j,k\}\), put

\[
                   W_I={\operatorname {Wr}(h_i,h_j,h_k)\over z^2}.
\]

In lexicographic order on the ten triples, the exact coordinate
Wronskians are

\[
\begin{array}{c|l}
012&-2(\beta z-3)\\
013&-2z(3\beta z-8)\\
014&-6z^2(2\beta z-5)\\
023&-6z^2(\beta z-2)\\
024&-2z^3(8\beta z-15)\\
034&-4z^4(3\beta z-5)\\
123&2z^4\\
124&6z^5\\
134&6z^6\\
234&2z^7.
\end{array}                                                       \tag{15}
\]

They span all eight septic coefficients for every \(\beta\).  If
\(p_I\) are the Pluecker coordinates of a three-space in the hyperplane
(13), its normalized Wronskian is

\[
                         \sum_Ip_IW_I.                            \tag{16}
\]

Equations (15)--(16), together with the five Pluecker quadrics, give a
compact exact presentation of the unique implicit equation.  Explicitly,
put

\[
 q_{ij}=(-1)^{i+j}p_{\{0,1,2,3,4\}\setminus\{i,j\}}.
\]

Then for every \(i<j<k<l\),

\[
                  q_{ij}q_{kl}-q_{ik}q_{jl}+q_{il}q_{jk}=0.      \tag{17}
\]

Eliminating the two-dimensional affine fibre of (16) from (17) gives an
irreducible quintic hypersurface

\[
               {\mathfrak Q}_\beta(c_0,\ldots,c_7)=0             \tag{18}
\]

in the septic coefficients.  Here is a short degree proof which also
covers \(\beta=0\).  The map in (16) is a surjective linear projection
\(\mathbb P^9\dashrightarrow\mathbb P^7\).  Its centre misses
\(\operatorname {Gr}(3,5)\), because the Wronskian of three independent
characteristic-zero polynomials is nonzero.  On the affine Grassmannian
chart obtained by adding arbitrary multiples of \(h_3,h_4\) to
\(h_0,h_1,h_2\), an exact Jacobian witness has rank six for every
\(\beta\).  Thus the image has dimension six.  It spans \(\mathbb P^7\),
so it is not a linear hyperplane.  Finally,

\[
                         \deg\operatorname {Gr}(3,5)=5.           \tag{19}
\]

The generic projection degree times the hypersurface degree is five;
therefore the projection is birational and (18) has degree five.

## 4. The selected-triple slope and the shared exchange term

The singleton in (12) is precisely the one copy left after assigning
role two to the triple at \(r\).  It is therefore nonzero.  Let \(x\) be
the other triple value, let \(D\) be the original double set, and let
\(H\) be the product of all original singleton plus-pole factors.

For \(b=7\), selecting only the triple at \(r\) gives

\[
 \beta_r={k\over r+\mu}+{1\over r}
       +\sum_{y\in H}{1\over r+y}-{4\over r-x}
       -3\sum_{v\in D}{1\over r-v}.                              \tag{20}
\]

The term \(1/r\) is the logarithmic derivative of the selected
\((z+r)^2\) factor at \(z=r\).  For \(b=8\), also select a double
\(u\in D\).  Relative to the baseline in (20), removing \(u\) from the
complement and inserting its plus-pole square gives

\[
 \boxed{\quad
 \beta_{r,u}=\Omega_r+\phi_u(r),\qquad
 \phi_u(r)={3\over r-u}+{2\over r+u}
           ={5r+u\over r^2-u^2}.
 \quad}                                                          \tag{21}
\]

This is exactly the exchange function used in the
\(a=3,b=6\) all-pair closure.  The new obstruction is geometric rather
than local: its target is now the quintic (18), not the earlier Schubert
cubic.  For each of the two choices of selected triple and each of the
eight selected doubles, the coefficient vector of

\[
             \prod_{v\in D\setminus\{u\}}
                    \bigl(z-(v-r)\bigr)                           \tag{22}
\]

must satisfy \({\mathfrak Q}_{\beta_{r,u}}=0\).  These are sixteen
coupled quintics.  The presentation (15)--(17) includes the zero-slope
chart and is preferable to an expanded implicit polynomial.

## 5. The stronger endpoint condition: six rows in one plane

The dominance in Section 2 shows what must be retained at the bare
endpoint.  Let \(R(z)=(z-x_1)(z-x_2)\) be the product of the two
complementary triple factors, let \(B\) be the six complementary double
values, let \(Q\) be the set of selected doubles, and put

\[
 U_{v,Q}(z)=
 { (z+\mu)^k\displaystyle\prod_{q\in Q}(z+q)^2H(z)
   \over
   R(z)^4\displaystyle\prod_{w\in B\setminus\{v\}}(z-w)^3},
                         \qquad v\in B.                           \tag{23}
\]

This is a unit at \(v\).  Define

\[
 \alpha_{v,Q}={U'_{v,Q}(v)\over U_{v,Q}(v)},\qquad
 \delta_{v,Q}={U''_{v,Q}(v)\over U_{v,Q}(v)}.                    \tag{24}
\]

The coefficient of \((z-v)^{-1}\) in the exact differential identity
is one half of \((U_{v,Q}S)''(v)\).  Consequently every member of the
relation space is killed by

\[
 J_{v,Q}=D_v^2+2\alpha_{v,Q}D_v+\delta_{v,Q}E_v.                 \tag{25}
\]

Since \({\cal S}\subseteq\mathbb C[z]_{\leq4}\) has dimension three,
its annihilator has dimension two.  Therefore

\[
 \boxed{\qquad
       \operatorname {rank}\{J_{v,Q}:v\in B\}\leq2.
 \qquad}                                                         \tag{26}
\]

In the monomial basis \(1,z,\ldots,z^4\), the \(j\)-th entry of this
row is

\[
 j(j-1)v^{j-2}+2\alpha_{v,Q}jv^{j-1}
                         +\delta_{v,Q}v^j,\qquad 0\leq j\leq4.  \tag{27}
\]

Thus (26) is the explicit vanishing of all \(3\)-by-\(3\) minors of a
six-by-five rational matrix.

There is again a compact exchange law.  If \(\alpha_{v,\varnothing}\)
and \(\eta_{v,\varnothing}\) denote the regular logarithmic first and
second derivatives before selecting any double, then for \(v\notin Q\),

\[
\begin{split}
 \alpha_{v,Q}&=\alpha_{v,\varnothing}
       +\sum_{q\in Q}\left({3\over v-q}+{2\over v+q}\right),\\
 \eta_{v,Q}&=\eta_{v,\varnothing}
       +\sum_{q\in Q}\left(-{3\over(v-q)^2}-{2\over(v+q)^2}\right),\\
 \delta_{v,Q}&=\alpha_{v,Q}^2+\eta_{v,Q}.
\end{split}                                                       \tag{28}
\]

For \(b=6,7,8\), equation (26) applies respectively to one, seven, and
twenty-eight choices of \(Q\), of sizes zero, one, and two.  This
rank-two system is strictly stronger than the dominant Wronskian datum
(7), and it is the most economical exact endpoint target currently
available.

## 6. Concrete continuation

The next elimination should proceed in the following order.

1. For \(b=8\), fix three complementary double anchors.  Among the five
   remaining doubles there are ten selected pairs.  Apply (26)--(28) to
   the same anchored \(3\)-by-\(3\) minor for all ten pairs, then take
   Boolean pair differences before expanding denominators.  This retains
   both logarithmic jets and has only the shared Cauchy exchange function
   (21).
2. If a residual branch survives, add the sixteen neighboring quintics
   (15)--(22).  Eliminate the two accessory Pluecker fibre coordinates
   only after symmetric compression across the eight omitted roots; the
   isolated quintic has too high a moving-root degree for a root count.
3. The low packet \(b=0,1,2\) is closed by the companion
   [twelve-simple cofactor theorem](live-three-zero-higher-split-p18-two-triple-twelve-simple-cofactor-closure.md).
   Ten fixed anchors produce a bivariate cofactor of bidegree \((5,9)\);
   moving singletons, supplemented by the two double values in the
   smallest \(b=2\) cases, force a reflected fourth-power divisor and an
   impossible diagonal Wronskian.  The mixed
   [six-simple/three-double cofactor theorem](live-three-zero-higher-split-p18-two-triple-six-simple-three-double-cofactor-closure.md)
   applies the same bidegree reduction with two normalized jets at each
   of the three doubles and closes \(b=3,4,5\).

The same invariant cofactor count extends one step farther than the three
common-complement packets suggest.  The
[four-/five-double cofactor theorem](live-three-zero-higher-split-p18-two-triple-four-five-double-cofactor-closure.md)
uses the \(d=2\) complements \(3^2 2^4 1^4\) and \(3^2 2^5 1^2\).
Their fixed simple/double anchor counts are respectively \((2,4)\) and
\((0,5)\), so both again have effective weight ten.  The same
bidegree-\((5,9)\) cofactor, with the two selected doubles supplying the
two missing interpolation points, closes \(b=6,7\).

The endpoint family \(b=8\) is not closed by the scalar Wronskian or
cofactor routes above.  It is subsequently closed by the
[common-lift theorem](live-three-zero-higher-split-p18-two-triple-eight-double-common-lift-closure.md):
fixing one selected double transports the other seven pair spaces into a
single degree-nine second-order residue kernel, where two coprime lifts
force dimension six but seven local rows force dimension at most five.
Sections 2--5 remain the exact frontier audit that supplies those rows.

## 7. Exact audit

[verify_live_three_zero_higher_split_p18_two_triple_endpoint_frontier.py](../computations/verify_live_three_zero_higher_split_p18_two_triple_endpoint_frontier.py)
reconstructs the nine-family selection table, verifies the three common
complement packets, certifies the dominant endpoint Jacobian and its
structural witness, computes all ten normalized coordinate Wronskians,
checks surjectivity and the all-slope rank-six Jacobian witness for the
neighboring image, audits \(\deg\operatorname {Gr}(3,5)=5\), and verifies
the first- and second-logarithmic exchange formulas.
