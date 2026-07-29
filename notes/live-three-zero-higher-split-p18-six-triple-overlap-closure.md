# Higher splits: the \(p=18\) six-triple overlap closure

## 1. Result

Work on the no-extra-singular live-three-zero collision stratum.  On the
first five-dimensional boundary put

\[
             p=h+k=18,\qquad 13\leq h\leq17,\qquad k=18-h.          \tag{1}
\]

Then none of the three collision profiles

\[
 \boxed{\qquad 3^6\,2^d\,1^{\,h+2-2d},\qquad d=0,1,2,\qquad}       \tag{2}
\]

is possible.

These are three of the fifty symbolic families left by the exact
[\(q=5\) boundary census](live-three-zero-higher-split-q5-boundary-census.md).
The proof uses compatibility between different formal selections of the
same profile.  A selection leaving the six triples complementary first
forces a pure-fourth-pole normal form.  Promoting one complementary
triple to role two then forces an incompatible Robin coefficient in the
dual relation space.

All values below satisfy the standard structural conditions: distinct
value classes are distinct and pairwise nonopposite, a repeated value is
nonzero, and at most one singleton value is zero.

## 2. Every selection is on simultaneous equality

Fix any formal selection with \(d\leq2\) repeated layers and

\[
                         s=h+2-2d                                  \tag{3}
\]

singleton layers.  Its selected-row kernel \(K\subseteq
\mathbb C[z]_{\leq h+3-d}\) has dimension at least four by the pair-drop
theorem.  The selected Wronskian estimate at \(q=6\) is strict, since

\[
 6^2-2\cdot6-h-2+\max(0,6-k)=10>0.                                \tag{4}
\]

Thus \(\dim K\leq5\).  If \(\dim K=4\), Sections 4--5 of
[the low-role selected-lift incidence closure](live-three-zero-higher-split-low-role-selected-lift-incidence-closure.md)
give a contradiction: their incidence argument only needs \(K=W\),
which follows directly from the four-dimensional pair-drop span.
Consequently

\[
                              \dim K=5.                            \tag{5}
\]

The relation space of the selected rows therefore has dimension three.
The exact relation-to-polynomial map sends it injectively to

\[
                 \mathcal S\subseteq\mathbb C[z]_{\leq c-4},       \tag{6}
\]

where \(c\) is the number of complementary value classes.  If

\[
 A=\prod_{i=1}^c(z-a_i)^{m_i},\qquad
 g=\prod_{i=1}^c(z-a_i)^{m_i-1},                                  \tag{7}
\]

the exact differential identity is

\[
 {d\over dz}{(z+\mu)^{k+1}N\over A}
 ={(z+\mu)^kg\over A^2}\,Q^2H\,S,
 \qquad S\in\mathcal S.                                           \tag{8}
\]

Here \(Q=\prod(z+u)\) runs over selected role-two values and
\(H=\prod(z+r)\) runs over selected singleton values.

At \(p=18\), both Wronskian bounds are saturated.  In particular,
\(\mathcal S\) is gcd-free, and at a complementary root of multiplicity
\(m=1,2,3\) its vanishing sequence is respectively

\[
                  (0,2,3),\qquad(0,1,3),\qquad(0,1,2).              \tag{9}
\]

Its Wronskian has no zeros other than

\[
 \operatorname {Wr}(\mathcal S)=C
       \prod_{m_i=1}(z-a_i)^2\prod_{m_i=2}(z-a_i).                 \tag{10}
\]

## 3. The six-triple selection and its normal form

For any profile in (2), first select all \(d\) exact double classes and
the \(s\) singleton classes.  The complement consists of six exact
triples.  Write

\[
 X=\{x_1,\ldots,x_6\},\qquad
 R(z)=\prod_{x\in X}(z-x),\qquad A=R^3.                            \tag{11}
\]

Now \(c=6\), so (5)--(6) force

\[
                         \mathcal S=\mathbb C[z]_{\leq2}.           \tag{12}
\]

Set

\[
                         T=(z+\mu)^kQ^2H.                           \tag{13}
\]

The right side of (8) is

\[
                              {T\over R^4}S.                        \tag{14}
\]

At every \(x\in X\), its residue vanishes for every quadratic \(S\).
Testing the three independent local jets of \(S\) removes the
third-, second-, and first-order polar coefficients of \(T/R^4\).
Since \(\deg T=20<24=\deg R^4\), there is no polynomial part.  Hence

\[
 {T(z)\over R(z)^4}=\sum_{x\in X}{c_x\over(z-x)^4},
 \qquad
 \boxed{\quad T(z)=\sum_{x\in X}c_xR_x(z)^4,\quad
              R_x={R\over z-x}.\quad}                              \tag{15}
\]

The leading fourth-pole coefficients \(c_x\) are nonzero because all
factors in (13) are units at a complementary value.  In particular, the
unit \(T/R_x^4\) has zero first derivative at \(x\).  Taking a logarithmic
derivative gives the base-selection identity

\[
 {k\over x+\mu}
 +2\sum_{u\in Q}{1\over x+u}
 +\sum_{y\in H}{1\over x+y}
 -4\sum_{b\in X\setminus\{x\}}{1\over x-b}=0.                    \tag{16}
\]

Equation (15) is the exact algebraic normal form of the six-triple
boundary.  The rest of the proof shows that it cannot be compatible with
the neighboring selections belonging to the same profile.

## 4. Promoting a triple closes \(d=0,1\)

Assume first \(d\leq1\).  Choose \(x\in X\) and two selected singleton
values \(r,s\in H\).  Remove \(r,s\) from the selection and give role two
to the exact triple at \(x\).  This is again a legal formal selection,
now with \(d+1\leq2\) role-two layers.  Its complement is

\[
                         3^5\,1_x1_r1_s.                            \tag{17}
\]

Here \(c=8\), and the saturated three-space lies in
\(\mathbb C[z]_{\leq4}\).  The three simple complementary roots impose
three codimension-two osculating conditions.  Their intersection has
degree one, and direct Hermite interpolation gives the unique space

\[
 \mathcal S_{xrs}=\operatorname {span}\bigl\{
 (z-x)^2(z-r)^2,
 (z-x)^2(z-s)^2,
 (z-r)^2(z-s)^2\bigr\}.                                  \tag{18}
\]

Indeed,

\[
 \operatorname {Wr}(\mathcal S_{xrs})
       =C(z-x)^2(z-r)^2(z-s)^2.                                  \tag{19}
\]

At the simple root \(x\), only the last displayed section is nonzero.
If \(U_x\) is the local unit in (8), the exact residue condition
\((U_xS)'(x)=0\) therefore fixes its logarithmic derivative:

\[
 {U_x'(x)\over U_x(x)}
 =-{d\over dz}\log\bigl((z-r)^2(z-s)^2\bigr)\big|_{z=x}
 =-{2\over x-r}-{2\over x-s}.                                  \tag{20}
\]

For the promoted selection, the selected factors change by

\[
 Q\longmapsto Q(z+x),\qquad
 H\longmapsto {H\over(z+r)(z+s)},                                \tag{21}
\]

and the complementary polynomial is

\[
 A_1=R_x^3(z-x)(z-r)(z-s),\qquad g_1=R_x^2.                       \tag{22}
\]

Consequently the local unit at \(x\) is

\[
 U_x={ (z+\mu)^kQ^2(z+x)^2H
       \over (z+r)(z+s)R_x^4(z-r)^2(z-s)^2}.                       \tag{23}
\]

Taking its logarithmic derivative and using (20) cancels the last two
terms and gives

\[
 {k\over x+\mu}+2\sum_{u\in Q}{1\over x+u}
 +{1\over x}+\sum_{y\in H\setminus\{r,s\}}{1\over x+y}
 -4\sum_{b\ne x}{1\over x-b}=0.                                 \tag{24}
\]

Subtracting (16) yields

\[
 {1\over x}={1\over x+r}+{1\over x+s}
 \qquad\Longleftrightarrow\qquad rs=x^2.                          \tag{25}
\]

The pair \(r,s\) was arbitrary.  There are at least three nonzero
selected singleton values: \(s=h+2-2d\geq13\), and at most one is zero.
For three of them, (25) for two pairs sharing one value forces the other
two values to coincide.  This violates structural distinctness.  Thus
the profiles in (2) with \(d=0,1\) are impossible.

## 5. Exchanging a double closes \(d=2\)

It remains to treat

\[
                         3^6\,2_u2_v\,1^{h-2}.                      \tag{26}
\]

Start again from the six-triple complement and (16), so both double
values \(u,v\) occur in \(Q\).  Fix \(x\in X\).  In a second selection,
keep \(u\) at role two, remove \(v\) from the selection, and put the
triple \(x\) at role two.  The complement becomes

\[
                              3^5\,2_v\,1_x.                        \tag{27}
\]

Now \(c=7\), and \(\mathcal S\) is a hyperplane in
\(\mathbb C[z]_{\leq3}\) whose Wronskian is

\[
                       C(z-x)^2(z-v).                              \tag{28}
\]

Write \(P=p_0+p_1z+p_2z^2+p_3z^3\).  The Wronski map on hyperplanes in
this four-dimensional polynomial space is linear, so (28) uniquely
determines

\[
 \mathcal S=\ker L_{x,v},\qquad
 L_{x,v}(P)=p_0+{2x+v\over3}p_1
              +{x^2+2xv\over3}p_2+x^2v\,p_3.                     \tag{29}
\]

The simple-root residue at \(x\) says that
\(D_x+\beta E_x\) annihilates \(\mathcal S\), where
\(\beta=U_x'(x)/U_x(x)\).  Comparing this functional with (29) gives

\[
                              \beta={3\over v-x}.                   \tag{30}
\]

For this exchanged selection,

\[
 A_2=R_x^3(z-x)(z-v)^2,\qquad
 g_2=R_x^2(z-v),\qquad
 Q_2=(z+u)(z+x),                                                 \tag{31}
\]

while \(H\) is unchanged.  Therefore

\[
 {U_x'(x)\over U_x(x)}
 ={k\over x+\mu}+{2\over x+u}+{1\over x}
  +\sum_{y\in H}{1\over x+y}
  -4\sum_{b\ne x}{1\over x-b}-{3\over x-v}.                    \tag{32}
\]

Since \(3/(v-x)=-3/(x-v)\), equations (30)--(32) cancel the final term.
The base-selection equation (16), on the other hand, contains both
selected doubles.  Subtraction gives

\[
                         {1\over x}={2\over x+v},
 \qquad\text{hence}\qquad v=x.                                  \tag{33}
\]

But \(v\) and \(x\) are distinct value classes.  This contradiction
closes \(d=2\) and proves (2).

## 6. Exact audit

[verify_live_three_zero_higher_split_p18_six_triple_overlap_closure.py](../computations/verify_live_three_zero_higher_split_p18_six_triple_overlap_closure.py)
checks the degree and dimension equalities for all five diagonal pairs,
the two canonical dual Wronskians, the Robin functional (30), both local
unit calculations, and the factorizations in (25) and (33).
