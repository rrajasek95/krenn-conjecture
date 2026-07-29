# The seventh split: repeated-anchor bivariate closure at sixteen classes

## 1. Result and scope

Continue from
[live-three-zero-seventh-split-bivariate-quartet-closure.md](live-three-zero-seventh-split-bivariate-quartet-closure.md).
Put

\[
                         p=r-1\ge8.
\]

There are \(p+9\) exceptional labels.  Consider a residual double/single
profile

\[
                  (2^d,1^s),\qquad 2d+s=p+9,
                  \qquad c=d+s=p+9-d,                       \tag{1}
\]

where \(c\) is its number of distinct exceptional values.

**Theorem 1.1.**  Every such residual profile with

\[
                         c\ge16
                  \quad\Longleftrightarrow\quad
                         p\ge d+7                            \tag{2}
\]

is impossible.

The new ingredient is to select both copies of one double value.  Its
triple local pole supplies one second-order condition on the cubic
residual.  Together with three ordinary anchor conditions this gives a
four-row bivariate determinant.

The initially hoped-for bidegree \((8,8)\) does **not** occur.  The
repeated row has bidegree \((4,4)\), the other three rows have bidegree
\((2,2)\), and the determinant bound \((10,10)\) is sharp.  Thus this
argument reaches sixteen classes, not fourteen.  No closure at fourteen
or fifteen classes is asserted here.

## 2. A legal six-class selection

Choose a double value \(u\), and choose three further distinct nonzero
values \(a,b,c\).  Select

\[
                    R=\{u,u,a,b,c,x,y\},                    \tag{3}
\]

where \(x,y\) are distinct value classes outside the fixed set

\[
                         F=\{u,a,b,c\}.                     \tag{4}
\]

The structural pair-sum condition has three consequences used below:

\[
 u\ne0,\qquad s+t\ne0\text{ for distinct exceptional classes }s,t,
 \qquad\text{and at most one value class is zero}.           \tag{5}
\]

The simultaneous-Hermite singleton-row hypothesis can be retained
uniformly over all ordered pairs \(x\ne y\).

- If \(d\ge2\), take \(a\) from a second double class and select only one
  of its copies.  The other copy is a singleton class in every complement
  \(N=E\setminus R\).
- If \(d=1\), then \(s=c-1\ge15\).  Selection (3) uses at most five
  singleton classes, so an untouched singleton remains in every \(N\).

The fixed values \(a,b,c\) can be chosen nonzero even if the unique
possible zero class exists.  That zero may occur as \(x\) or \(y\);
it is not a pole of any row below.

Selection (3) represents six value classes.  The seventh-split Hermite
reduction therefore gives a nonzero residual polynomial

\[
                     0\ne q_{x,y}(z),\qquad \deg q_{x,y}\le3. \tag{6}
\]

## 3. The simple and repeated anchor equations

Use ascending cubic coefficients and write

\[
 B_t=(1,t,t^2,t^3),\qquad E_t=(0,1,2t,3t^2),                \tag{7}
\]

\[
 \psi_t(w)={1\over w-t}-{2\over w+t}
           ={3t-w\over w^2-t^2},                            \tag{8}
\]

and

\[
 \eta_t(w)=\partial_t\psi_t(w)
           ={1\over(w-t)^2}+{2\over(w+t)^2}
           ={3w^2-2tw+3t^2\over(w^2-t^2)^2}.               \tag{9}
\]

After absorbing all terms fixed by \(F\), each simple anchor
\(s\in\{a,b,c\}\) gives

\[
 q'(s)+\bigl(C_s+\psi_s(x)+\psi_s(y)\bigr)q(s)=0,            \tag{10}
\]

whose coefficient row is

\[
 R_s(x,y)=E_s+\bigl(C_s+\psi_s(x)+\psi_s(y)\bigr)B_s.        \tag{11}
\]

The fully selected double \(u\) has local pole order three.  The local
rational function may have pole orders three and two, but its simple-pole
coefficient is absent.  If its pole-free local numerator is written
\(H_u(z;x,y)q(z)\), that condition is

\[
                         (H_uq)''(u)=0.                     \tag{12}
\]

Here \(H_u(u;x,y)\ne0\) by the structural noncollision and pair-sum
conditions.  Put

\[
\begin{split}
 Y&={H_u'(u)\over H_u(u)}
      =A+\psi_u(x)+\psi_u(y),\\
 {H_u''(u)\over H_u(u)}
   &=Y^2+K+\eta_u(x)+\eta_u(y)=:M,                           \tag{13}
\end{split}
\]

where \(A,K\) contain only fixed contributions.  Expanding (12) and
dividing only by the known nonzero factor \(H_u(u)\) gives

\[
                      q''(u)+2Yq'(u)+Mq(u)=0.               \tag{14}
\]

In particular, no division by \(q(u)\), \(q'(u)\), or a leading
coefficient of \(q\) occurs.  The exact repeated-anchor row is

\[
 R_u(x,y)=
 \bigl(
 M,\;
 2Y+uM,\;
 2+4uY+u^2M,\;
 6u+6u^2Y+u^3M
 \bigr).                                                     \tag{15}
\]

Thus (15) remains valid if the residual drops degree, has a multiple
root, or vanishes at \(u\).

## 4. Minimal clearing and the sharp determinant degree

Set

\[
                            d_t(w)=w^2-t^2.                 \tag{16}
\]

The simple rows clear as

\[
\begin{split}
 \widehat R_s(x,y)
  ={}&d_s(x)d_s(y)(E_s+C_sB_s)\\
    &+(3s-x)d_s(y)B_s+(3s-y)d_s(x)B_s,                     \tag{17}
\end{split}
\]

so each entry has degree at most two separately in \(x\) and \(y\).
Because both \(Y^2\) and \(\eta_u\) have genuine double poles, the repeated
row requires

\[
                  \widehat R_u(x,y)
                    =d_u(x)^2d_u(y)^2R_u(x,y).              \tag{18}
\]

Equations (8)--(9) make (18) a polynomial row of bidegree at most
\((4,4)\).  The clearing is genuinely double: at the two opposite
endpoints,

\[
\begin{split}
 \widehat R_u(x,u)
    &=8u^2d_u(x)^2B_u,\\
 \widehat R_u(x,-u)
    &=24u^2d_u(x)^2B_u.                                    \tag{19}
\end{split}
\]

Both right sides are nonzero polynomial rows because \(u\ne0\).

Define the mixed determinant

\[
 \widehat D_F(x,y)=
 \det\!\begin{pmatrix}
 \widehat R_u(x,y)\\
 \widehat R_a(x,y)\\
 \widehat R_b(x,y)\\
 \widehat R_c(x,y)
 \end{pmatrix}.                                             \tag{20}
\]

One row contributes degree at most four in each variable and the other
three contribute at most two.  Hence

\[
                         \operatorname{bideg}\widehat D_F
                            \le(10,10).                     \tag{21}
\]

This bound cannot be replaced by a universal \((8,8)\) bound.  At the
rational specialization

\[
\begin{gathered}
 u=1,\quad (a,b,c)=(2,3,4),\quad A={2\over3},\quad K={5\over7},\\
 (C_a,C_b,C_c)=\left({3\over4},{4\over5},{5\over6}\right),
\end{gathered}                                               \tag{22}
\]

the exact determinant has degree ten in both variables and

\[
             [x^{10}y^{10}]\,\widehat D_F(x,y)
                         ={19133\over630}\ne0.               \tag{23}
\]

Thus any improvement to fourteen or fifteen classes needs an additional
identity not present in the universal four-row system.

## 5. Strict bivariate interpolation at sixteen classes

For every admissible ordered pair of distinct outside values \(x,y\), the
nonzero cubic (6) lies in the kernel of the four rational rows.  None of
their clearing factors vanishes on this grid, so

\[
                         \widehat D_F(x,y)=0.                \tag{24}
\]

There are

\[
                         M=c-4                              \tag{25}
\]

outside value classes.  Fix one of them as \(y\).  The other

\[
                         M-1=c-5\ge11                       \tag{26}
\]

values are distinct roots of the degree-at-most-ten polynomial
\(x\mapsto\widehat D_F(x,y)\).  Therefore that polynomial is zero.
This holds at all

\[
                         M=c-4\ge12                         \tag{27}
\]

values of \(y\).  Every coefficient in \(x\) has degree at most ten in
\(y\), so a second strict root count yields

\[
                         \boxed{\widehat D_F(x,y)\equiv0}.   \tag{28}
\]

The possible zero value causes no loss in (26)--(27).  Every fixed anchor
is nonzero, and distinctness together with (5) excludes all other poles.

## 6. Endpoint reduction to the proved three-anchor obstruction

Specialize (28) first at \(y=u\) and then at \(y=-u\).  By (19), canceling
only nonzero polynomial factors over the integral domain leaves a
four-row determinant whose first row is \(B_u\).  Hence its cubic kernel
lies in the hyperplane \(q(u)=0\).  Write

\[
                           q(z)=(z-u)r(z),\qquad\deg r\le2.  \tag{29}
\]

For a simple anchor \(s\), equation (10) then becomes

\[
 r'(s)+\left(
 C_s+\psi_s(x)+\psi_s(\pm u)+{1\over s-u}
 \right)r(s)=0.                                             \tag{30}
\]

The two endpoint shifts are

\[
\begin{split}
 \psi_s(u)+{1\over s-u}
      &=-{2\over s+u},\\
 \psi_s(-u)+{1\over s-u}
      &=-{1\over s+u}-{1\over s-u}.                         \tag{31}
\end{split}
\]

Thus each endpoint gives an identically singular three-anchor quadratic
Robin pencil with moving term \(\psi_s(x)\) and fixed translations

\[
\begin{split}
 C_s^+&=C_s-{2\over s+u},\\
 C_s^-&=C_s-{1\over s+u}-{1\over s-u}.                      \tag{32}
\end{split}
\]

This determinant reduction is exact.  Multiplication by \(z-u\) maps
ascending quadratic coefficients to ascending cubic coefficients by

\[
 T_u=
 \begin{pmatrix}
 -u&0&0\\
 1&-u&0\\
 0&1&-u\\
 0&0&1
 \end{pmatrix},\qquad B_uT_u=0.                             \tag{33}
\]

If \(R_s(Z)=E_s+ZB_s\), then

\[
 R_s(Z)T_u
  =(s-u)\left(
 Z+{1\over s-u},\
 1+s\left(Z+{1\over s-u}\right),\
 2s+s^2\left(Z+{1\over s-u}\right)
 \right).                                                    \tag{34}
\]

Consequently the four-by-four endpoint determinant is exactly
\((a-u)(b-u)(c-u)\) times the reduced three-by-three determinant.
Every scalar factor is nonzero.

But the fifth-split three-anchor certificate rules out such an identity
for arbitrary fixed translations.  For anchors \(a,b,c\) and translations
\(U,V,W\), identity of the quadratic Robin determinant would force

\[
\begin{split}
 L_a&=(a^2-b^2)V+(a^2-c^2)W+2a-b-c=0,\\
 L_b&=(a^2-b^2)U+(c^2-b^2)W+a-2b+c=0,\\
 L_c&=(a^2-c^2)U+(b^2-c^2)V+a+b-2c=0.                      \tag{35}
\end{split}
\]

These equations are incompatible because

\[
\begin{split}
 &-(b^2-c^2)L_a-(a^2-c^2)L_b+(a^2-b^2)L_c\\
 &\hspace{35mm}=3(a-b)(a-c)(b-c)\ne0.                       \tag{36}
\end{split}
\]

All denominator factors used in the opposite-pole certificate are
nonzero by the choice of distinct nonzero anchors and (5).  Either endpoint
already contradicts (35)--(36).  This proves Theorem 1.1.

## 7. Sharpened double/single frontier

Combining (2) with the preceding seventh-split collision census and the
seventeen-class bivariate closure leaves exactly the following
double/single values of \(d\), where \(s=p+9-2d\):

\[
\begin{array}{c|l}
p&\text{remaining }d\\ \hline
8&2,3,4,5,6,7,8\\
9&3,4,5,6,7,8,9\\
10&4,5,6,7,8,9\\
11&5,6,7,9,10\\
12&6,7,10\\
13&7.
\end{array}                                                   \tag{37}
\]

There are no remaining double/single residuals for \(p\ge14\).  The
all-distinct stratum was already closed by the preceding quartet argument.
The finite triple-containing residual list is unaffected by this note.

## 8. Exact audit

[verify_live_three_zero_seventh_split_repeated_anchor_bivariate_closure.py](../computations/verify_live_three_zero_seventh_split_repeated_anchor_bivariate_closure.py)
checks the nodal derivative (9), derives (15) directly from a symbolic
cubic, verifies the product rule without dividing by \(q\), proves the
minimal endpoint factors \(8\) and \(24\), checks the sharp degree-ten
specialization (22)--(23), verifies the endpoint shifts and exact basis
reduction (33)--(34), rechecks the incompatibility certificate (36), and
audits the strict class counts and residual table (37).
