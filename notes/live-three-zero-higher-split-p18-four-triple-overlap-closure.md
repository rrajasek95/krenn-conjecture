# Higher splits: the \(p=18\) four-triple overlap closure

## 1. Result and exact family range

On the no-extra-singular live-three-zero stratum, let

\[
                  p=h+k=18,\qquad 13\leq h\leq17.                  \tag{1}
\]

The \(a=4\) part of the fifty-family boundary consists of exactly six
profiles:

\[
                    3^4\,2^b\,1^{\,h+8-2b},
                    \qquad b=0,1,2,3,4,5.                         \tag{2}
\]

Indeed, \(3a+2b+u=20\) gives \(u=8-2b\), and the applicability
alternatives stop exactly at \(b=5\).

All six families are impossible:

\[
 \boxed{\qquad 3^4\,2^b\,1^{\,h+8-2b}
                    \text{ is impossible for }0\leq b\leq5.\qquad}\tag{3}
\]

The exact proof routing within the \(a=4\) family is

\[
\begin{array}{c|c|c|c|c}
b&u&\text{convenient }(d,t)&\text{complement}&\text{status}\\ \hline
0& 8&(0,0)&3^4 1^6&\text{Section 6}\\
1& 6&(1,0)&3^4 1^6&\text{Section 6}\\
2& 4&(2,0)&3^4 1^6&\text{Section 6}\\
3& 2&(0,0)&3^4 2^3&\text{closed below}\\
4& 0&(1,0)&3^4 2^3&\text{closed below}\\
5&-2&(2,0)&3^4 2^3&\text{closed below}
\end{array}                                                       \tag{4}
\]

Thus no \(a=4\) family remains after this note.

Here \(t\) records a selected exact triple.  For completeness, the full
formal-selection classification, not merely the convenient column in
(4), is

\[
\begin{array}{c|l}
b&(d,t):\text{ complementary profile}\\ \hline
0&(0,0):3^4 1^6;\ (1,1):3^3 1^9\\
1&(0,0):3^4 2\,1^4;\ (1,0):3^4 1^6;\
  (1,1):3^3 2\,1^7;\ (2,1):3^3 1^9\\
2&(0,0):3^4 2^2 1^2;\ (1,0):3^4 2\,1^4;\
  (1,1):3^3 2^2 1^5;\ (2,0):3^4 1^6;\
  (2,1):3^3 2\,1^7\\
3&(0,0):3^4 2^3;\ (1,0):3^4 2^2 1^2;\
  (1,1):3^3 2^3 1^3;\ (2,0):3^4 2\,1^4;\
  (2,1):3^3 2^2 1^5\\
4&(1,0):3^4 2^3;\ (1,1):3^3 2^4 1;\
  (2,0):3^4 2^2 1^2;\ (2,1):3^3 2^3 1^3\\
5&(2,0):3^4 2^3;\ (2,1):3^3 2^4 1
\end{array}                                                       \tag{5}
\]

As in the
[six-triple overlap closure](live-three-zero-higher-split-p18-six-triple-overlap-closure.md),
every selection in (5) has a five-dimensional selected-row kernel and a
three-dimensional, gcd-free relation space

\[
                 \mathcal S\subseteq\mathbb C[z]_{\leq c-4}.       \tag{6}
\]

Its Wronskian is saturated, with a double zero at every simple
complementary root and a simple zero at every double complementary root.

## 2. A necessary quadratic for \(3^4 2^2 1^2\)

We first record the only degree-two Schubert calculation needed for
\(b=3\).  Let \(a,b\) be two complementary double values and \(r,s\)
two complementary singleton values.  A saturated relation three-space
for the profile \(3^4 2_a2_b1_r1_s\) lies in
\(\mathbb C[z]_{\leq4}\) and satisfies

\[
            \operatorname {Wr}(\mathcal S)
                  =C(z-r)^2(z-s)^2(z-a)(z-b).                     \tag{7}
\]

At the simple roots, exact residues give Robin functionals

\[
              L_r=D_r+\beta E_r,\qquad
              L_s=D_s+\gamma E_s                                \tag{8}
\]

which annihilate \(\mathcal S\).  They are independent, and hence

\[
                         \mathcal S=\ker L_r\cap\ker L_s.           \tag{9}
\]

Computing the Wronskian of (9), then requiring its remaining quadratic
factor to have roots \(a,b\), gives the following necessary quadratic
condition on \(\beta\):

\[
\begin{split}
0=P_{a,b;r,s}(\beta)
={}&(r-a)(r-b)(r-s)\beta^2\\
 &+\bigl(2ab-5r(a+b)+3s(a+b)+8r^2-6rs\bigr)\beta\\
 &+4(4r-2s-a-b).
\end{split}                                                       \tag{10}
\]

This is the exact two-valued Wronski fiber: eliminating \(\gamma\) from
the two coefficient equations gives
\(-3(r-s)P_{a,b;r,s}(\beta)\).

## 3. Singleton variation closes \(b=3\)

Consider

\[
                         3^4\,2_v2_a2_b\,1^{h+2}.                  \tag{11}
\]

Fix one double value \(v\), fix a nonzero singleton value \(r\), and let
\(s\) range over every other singleton value.  Such a nonzero \(r\)
exists because at most one singleton is zero.  Give role two to \(v\)
and select every singleton except \(r,s\).  This is a \(d=1\) formal
selection with complement

\[
                              3^4\,2_a2_b1_r1_s.                   \tag{12}
\]

Let \(X\) be the four complementary triple values and let \(H_{\rm all}\)
be the full set of \(h+2\) singleton values.  At the simple root \(r\),
the local unit in the exact differential identity is

\[
 U_r={ (z+\mu)^k(z+v)^2
              \displaystyle\prod_{y\in H_{\rm all}\setminus\{r,s\}}(z+y)
       \over
       \displaystyle\prod_{x\in X}(z-x)^4
       (z-a)^3(z-b)^3(z-s)^2}.                                   \tag{13}
\]

Consequently its Robin coefficient has the form

\[
                         \beta_r
             =\Lambda_r-{1\over r+s}-{2\over r-s},                 \tag{14}
\]

where the quantity independent of \(s\) is

\[
\begin{split}
\Lambda_r={}&{k\over r+\mu}+{2\over r+v}
 +\sum_{y\in H_{\rm all}\setminus\{r\}}{1\over r+y}
 -4\sum_{x\in X}{1\over r-x}\\
 &\hspace{35mm}-{3\over r-a}-{3\over r-b}.
\end{split}                                                       \tag{15}
\]

Substitute (14) into (10), and clear the structurally nonzero
denominator \((r+s)^2\).  The result is a polynomial

\[
                  {\cal N}_r(s)=c_3s^3+c_2s^2+c_1s+c_0            \tag{16}
\]

of degree at most three.  Put \(A=a-r\) and \(B=b-r\).  Direct expansion
gives

\[
\begin{split}
c_3&=-AB\Lambda_r^2+3(A+B)\Lambda_r-8,\\
c_2-r c_3&=-(A+B),\\
c_0-r c_1&=r\bigl(2AB+r(A+B)\bigr).
\end{split}                                                       \tag{17}
\]

This cubic cannot vanish identically.  If all four coefficients were
zero, the second identity would give \(A+B=0\); the third and \(r\ne0\)
would then give \(AB=0\).  Thus \(A=B=0\), contrary to the distinctness
of \(a,b,r\).

But every one of the \(h+1\geq14\) possible values of \(s\) must satisfy
(10), hence must be a root of the same nonzero cubic (16).  This is
impossible and closes \(b=3\).

## 4. The canonical three-double hyperplane

For \(b=4,5\), use the convenient selection in (4).  Its complement is

\[
                       A=R^3V^2,\qquad
                       V=\prod_{v\in B}(z-v),\qquad |B|=3,          \tag{18}
\]

where \(R\) is the product of the four triple factors.  Here \(c=7\), so
\(\mathcal S\) is a hyperplane in \(\mathbb C[z]_{\leq3}\).  Write

\[
                 V(z)=z^3-e_1z^2+e_2z-e_3.                        \tag{19}
\]

The Wronski map on these hyperplanes is linear.  Thus the saturated
Wronskian \(CV\) uniquely gives

\[
\begin{split}
\mathcal S&=\ker L_B,\\
L_B(p_0+p_1z+p_2z^2+p_3z^3)
          &=p_0+{e_1\over3}p_1+{e_2\over3}p_2+e_3p_3.
\end{split}                                                       \tag{20}
\]

Fix \(v\in B\), and write \(B\setminus\{v\}=\{a,b\}\).  If
\(\alpha_v=U_v'(v)/U_v(v)\), the exact double-root residue says that

\[
              D_v^2+2\alpha_vD_v+\delta_vE_v                       \tag{21}
\]

annihilates \(\mathcal S\).  Comparing (21) with (20) gives

\[
 \alpha_v=-{1\over v-a}-{1\over v-b},\qquad
 \delta_v={6\over(a-v)(b-v)}.                                    \tag{22}
\]

On the other hand, the local unit obtained from the exact differential
identity is

\[
                   U_v={ (z+\mu)^kQ^2H
                              \over R^4(z-a)^3(z-b)^3}.             \tag{23}
\]

Equating its logarithmic derivative with (22) leaves

\[
 {k\over v+\mu}
 +2\sum_{q\in Q}{1\over v+q}
 +\sum_{y\in H}{1\over v+y}
 -4\sum_{x\in X}{1\over v-x}
 -2\sum_{w\in B\setminus\{v\}}{1\over v-w}=0.                     \tag{24}
\]

## 5. Double exchange closes \(b=4,5\)

Both remaining profiles have at least one selected exact double in the
selection (4).  Choose a selected double \(r\), a complementary double
\(a\), and a second complementary double \(v\).  Exchange \(r\) and
\(a\), leaving all singleton roles and the other complementary values
unchanged.

Apply (24) at the common complementary double \(v\) before and after the
exchange.  All unchanged terms cancel, and one obtains

\[
 {1\over v+a}+{1\over v-a}
       ={1\over v+r}+{1\over v-r}.                                \tag{25}
\]

Because \(v\ne0\), this is equivalent to

\[
                         a^2=r^2.                                 \tag{26}
\]

Distinct value classes are neither equal nor opposite, so (26) is
impossible.  This closes \(b=4,5\), and together with Section 3 proves
(3).

## 6. A fixed accessory pencil closes \(b=0,1,2\)

For \(b\leq2\), select all \(b\) exact doubles at role two.  From the
full singleton set \(Y\), select all but six singleton values.  Every
six-element complementary set therefore gives the profile

\[
                              3^4 1^6.                              \tag{27}
\]

Fix five nonzero values

\[
                      R_0=\{r_1,\ldots,r_5\}\subset Y.              \tag{28}
\]

This is possible because at most one singleton value is zero.  Let \(s\)
range over \(Y\setminus R_0\), and use \(R_0\cup\{s\}\) as the six
complementary singleton values.  The number of available choices is

\[
                       |Y|-5=h+3-2b\geq12.                          \tag{29}
\]

For the saturated relation space
\(\mathcal S_s\subseteq\mathbb C[z]_{\leq6}\), the five fixed simple
roots give Robin rows

\[
                  L_i(s)=D_{r_i}+\beta_i(s)E_{r_i},
                  \qquad i=1,\ldots,5.                             \tag{30}
\]

They lie in the four-dimensional annihilator of \(\mathcal S_s\), so
they have a nontrivial relation.  Let \(J_0=\prod_i(z-r_i)\).  The exact
moment generating function of such a relation is

\[
 \sum_{i=1}^5c_i\left({1\over(z-r_i)^2}
                   +{\beta_i(s)\over z-r_i}\right)
                         ={N_s(z)\over J_0(z)^2}.                   \tag{31}
\]

The relation annihilates every polynomial of degree at most six, so the
left side is \(O(z^{-8})\).  Hence

\[
                              \deg N_s\leq2.                        \tag{32}
\]

Comparing the simple and double coefficients at \(r_i\) gives

\[
 {N_s'(r_i)\over N_s(r_i)}
       =\beta_i(s)+2\sum_{j\ne i}{1\over r_i-r_j},                  \tag{33}
\]

with the cross-multiplied identity valid even if \(N_s(r_i)=0\).

Let \(X\) be the four complementary triple values and let \(Q\) be the
fixed selected-double product.  Since the selected singleton set is
\(Y\setminus(R_0\cup\{s\})\), the local unit in the exact differential
identity gives

\[
 \beta_i(s)=\Lambda_i
       -2\sum_{j\ne i}{1\over r_i-r_j}
       -{1\over r_i+s}-{2\over r_i-s},                             \tag{34}
\]

where

\[
 \Lambda_i={k\over r_i+\mu}
       +2\sum_{q\in Q}{1\over r_i+q}
       +\sum_{y\in Y\setminus R_0}{1\over r_i+y}
       -4\sum_{x\in X}{1\over r_i-x}                               \tag{35}
\]

is independent of \(s\).

Put

\[
                  f_s(z)=(z-s)^2(z+s),\qquad
                  M_s=N_sf_s.                                    \tag{36}
\]

Equations (33)--(35) say exactly

\[
                         M_s'(r_i)=\Lambda_iM_s(r_i)
                         \qquad(i=1,\ldots,5).                      \tag{37}
\]

Thus every one of the at least twelve choices of \(s\) supplies a
nonzero member, divisible by \(f_s\), of the single fixed space

\[
 {\cal M}=\{M\in\mathbb C[z]_{\leq5}:
                 M'(r_i)=\Lambda_iM(r_i),\ i=1,\ldots,5\}.          \tag{38}
\]

This space has dimension at most two.  Indeed, if the five rows in (38)
had two independent relations on \(\mathbb C[z]_{\leq5}\), their
principal-part numerators \(U,V\) would have degree at most three.  Both
would satisfy the same five logarithmic-derivative conditions, so

\[
                              U'V-UV'                               \tag{39}
\]

would vanish at all five \(r_i\).  Its degree is at most four, hence it
would vanish identically.  In characteristic zero this makes \(U,V\)
proportional, a contradiction.

The space \(\mathcal M\) cannot be a line: two distinct values \(s,t\)
would make its generator divisible by the coprime degree-three
polynomials \(f_s,f_t\), whose product has degree six.  Therefore
\(\dim\mathcal M=2\).

Finally, the Wronskian of a pencil in
\(\mathbb C[z]_{\leq5}\) has degree at most eight.  For every allowed
\(s\), the pencil contains \(M_s\), which has a double zero at \(s\);
therefore its Wronskian vanishes at \(s\).  Equation (29) gives at least
twelve distinct roots, so that Wronskian would be identically zero.
Characteristic zero would then make the pencil one-dimensional.  This
last contradiction closes \(b=0,1,2\), and completes the proof of (3).

## 7. Exact audit

[verify_live_three_zero_higher_split_p18_four_triple_overlap_closure.py](../computations/verify_live_three_zero_higher_split_p18_four_triple_overlap_closure.py)
reconstructs all selections in (5), verifies the degree-two elimination
(10), audits the cubic identities (14)--(17), checks the canonical
hyperplane and its exact order-two Robin row, factors the double exchange
(25)--(26), and audits the quadratic-numerator/accessory-pencil closure
(27)--(39).
