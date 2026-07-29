# The eighth split: saturated-quartic moment closures

## 1. Result

At \((h,k)=(8,4)\), the two collision profiles

\[
                         3^4 2^3 1^4,
             \qquad      3^3 2^4 1^5                  \tag{1}
\]

are impossible on the no-extra-singular stratum.

In both cases, choose all double values and enough triple values to make
five formal layers.  The complementary polynomial has six simple roots
and two roots of multiplicity three, so the relation pencil lies in the
quartics and its Wronskian is exactly the product of the six simple-root
factors.  The top two coefficients of the accessory polynomial then give
two moment identities beyond the usual Robin residue sum.  On the
choose-two slice these moments make the quartic of triple values even;
on the choose-one slice they put three distinct triple values on a
nonzero quadratic.

## 2. Three saturated Robin moments

Let \(T\) be a legal formal-five set for which the complementary
polynomial is

\[
                  A(z)=L(z)(z-u)^3(z-v)^3,
       \qquad L(z)=\prod_{x\in X}(z-x),\quad |X|=6.    \tag{2}
\]

All six roots in \(X\) are simple.  All-order formal-five duality gives
an exact two-dimensional relation space

\[
                       {\cal S}_T\subset\mathbb C[z]_{\le4}. \tag{3}
\]

If \(f,g\) are a basis and

\[
 W=fg'-f'g,\qquad V=f'g''-f''g',                       \tag{4}
\]

then every simple-root Robin row

\[
                         P'(x)+Y_xP(x)=0               \tag{5}
\]

makes \(x\) a root of \(W\).  Thus, after rescaling the basis,

\[
                         W=L.                          \tag{6}
\]

The exact degree six in (6) lets us choose \(\deg f=3\) and
\(\deg g=4\).  If

\[
                  L=z^6+w_5z^5+\cdots,
\]

direct comparison of the top terms in (4) gives

\[
                  V=12z^4+8w_5z^3+O(z^2).             \tag{7}
\]

The accessory equation

\[
                         Wy''-W'y'+Vy=0                \tag{8}
\]

and (5) give \(V(x)=-L'(x)Y_x\).  Since \(\deg V<\deg L\), partial
fractions and expansion at infinity yield

\[
 {V(z)\over L(z)}=-\sum_{x\in X}{Y_x\over z-x},
\]

and hence the three saturated moments

\[
 \boxed{
 \sum_{x\in X}Y_x=0,\qquad
 \sum_{x\in X}xY_x=-12,\qquad
 \sum_{x\in X}x^2Y_x=-4\sum_{x\in X}x.}               \tag{9}
\]

## 3. The choose-two closure for \(3^4 2^3 1^4\)

Let \({\cal A}=\{a,b,c,d\}\) be the triple values, let \({\cal D}\)
be the three double values, and let \({\cal R}\) be the four singleton
values.  Choose

\[
                         T={\cal D}\cup S,
              \qquad S\in\binom{{\cal A}}2.           \tag{10}
\]

The simple-root set is \(X={\cal R}\cup S\), while the two unselected
triples are \(u,v\).  Every formal pair-drop core is legal because the
four original singleton classes remain outside it.

For \(p=0,1,2\), put

\[
                         E_p(S)=\sum_{x\in X}x^pY_x.   \tag{11}
\]

All dependence on selected-triple indicators is affine except for an
unordered selected pair \(\{x,y\}\).  Its exact quadratic coefficient is

\[
 C_p(x,y)=2{x^p+y^p\over x+y}
              +2{x^p-y^p\over x-y}.                   \tag{12}
\]

The first term comes from the two selected plus-poles.  The
selected-selected simple-root interaction contributes minus two times
the second quotient, while the selected-outside interaction contributes
plus four times that quotient.

Take the alternating rectangle on
\(\{a,c\},\{a,d\},\{b,c\},\{b,d\}\).  The right sides of all three
identities (9) are affine on this fixed-size slice.  For \(p=0\), exact
factorization gives

\[
 0={4(a-b)(c-d)(a+b+c+d)\over
          (a+c)(a+d)(b+c)(b+d)},                       \tag{13}
\]

so \(e_1(a,b,c,d)=0\).  For \(p=2\), it gives

\[
 0={-4(a-b)(c-d)
       (abc+abd+acd+bcd)\over
          (a+c)(a+d)(b+c)(b+d)},                       \tag{14}
\]

so \(e_3(a,b,c,d)=0\).  All displayed difference and sum factors are
nonzero under the standard distinct/nonopposite hypotheses.  Therefore

\[
          \prod_{x\in{\cal A}}(z-x)=z^4+e_2z^2+e_4    \tag{15}
\]

is even.  Its distinct roots must occur in opposite pairs (a zero root
would have even multiplicity), contradicting the nonopposite hypothesis.

## 4. The choose-one closure for \(3^3 2^4 1^5\)

Let \({\cal A}=\{a,b,c\}\) be the triple values, \({\cal D}\) the four
double values, and \({\cal R}\) the five singleton values.  For each
\(a\in{\cal A}\), choose

\[
                         T={\cal D}\cup\{a\}.          \tag{16}
\]

Again all ten cores are legal, and now \(X={\cal R}\cup\{a\}\).
Write

\[
 P_{\cal R}(z)=\prod_{r\in{\cal R}}(z-r),\qquad
 p_{\cal R}(z)={P_{\cal R}'(z)\over P_{\cal R}(z)},qquad
 \sigma_{\cal R}=\sum_{r\in{\cal R}}r.               \tag{17}
\]

For a fixed singleton \(r\), isolate the part of its Robin coefficient
which is independent of the selected triple:

\[
 K_r={4\over r+\mu}+2\sum_{d\in{\cal D}}{1\over r+d}
 -2\sum_{\rho\in{\cal R}\setminus\{r\}}{1\over r-\rho}
 -4\sum_{t\in{\cal A}}{1\over r-t}.                   \tag{18}
\]

Then

\[
                         Y_{a,r}=K_r+{2\over r+a}+{2\over r-a}. \tag{19}
\]

Put \(K_j=\sum_{r\in{\cal R}}r^jK_r\) and
\(F_j(a)=E_j(a)-K_j\).  The selected-root contribution cancels from
the following two combinations, leaving the exact identities

\[
\begin{aligned}
 F_1(a)-aF_0(a)&=20+4a\,p_{\cal R}(-a),\\
 F_2(a)-aF_1(a)&=4\sigma_{\cal R}-20a
                         -4a^2p_{\cal R}(-a).          \tag{20}
\end{aligned}
\]

The moments (9) say, for constants independent of \(a\),

\[
 F_0(a)=c_0,\qquad F_1(a)=c_1,
              \qquad F_2(a)+4a=c_2.                   \tag{21}
\]

The first line of (20) gives

\[
                         4a p_{\cal R}(-a)=c_1-20-ac_0. \tag{22}
\]

Substitute \(a\) times (22) into the second line of (20), without
dividing by \(a\).  Every selected triple satisfies

\[
                         c_0a^2+4a+4\sigma_{\cal R}-c_2=0. \tag{23}
\]

The coefficient of \(a\) is four, so (23) is a nonzero polynomial of
degree at most two.  It cannot contain the three distinct triple values.
This closes the second profile in (1), including the possibility that
one triple value is zero.

## 5. Exact audit

[verify_live_three_zero_eighth_split_k4_saturated_quartic_moment_closures.py](../computations/verify_live_three_zero_eighth_split_k4_saturated_quartic_moment_closures.py)
checks every legal formal core, the exact complementary multiplicities,
the two top accessory coefficients, all three moment signs, the complete
pair coefficient and both choose-two rectangle factors, and the
division-free choose-one quadratic elimination.
