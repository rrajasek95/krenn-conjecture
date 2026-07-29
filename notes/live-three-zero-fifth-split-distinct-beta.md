# The fifth split all-distinct stratum is uniformly injective

## 1. Outcome

Continue from the fourth split layer in
[live-three-zero-fourth-split-layer.md](live-three-zero-fourth-split-layer.md).
Put

\[
             t=r+6,\qquad p=r-1,\qquad k=r-6=p-5.              \tag{1}
\]

There are \(p+7\) exceptional live labels and \(k+1\) active star
sites.  This note treats the stratum on which all exceptional beta
values are distinct.

**Theorem 1.1 (fifth split, distinct beta values).**  For every
\(r\ge7\), the vanishing cyclic response is impossible on the
all-distinct exceptional-beta stratum.  Equivalently, some isolated-star
pivot is nonzero, so the standard row cleanup kills every residual
nonzero-to-\(z_0\) block and isolates \(z_0\) in \(G_3(q)\).

The residual numerator is now quadratic, so the two-row argument from
the preceding split no longer applies.  Three residue rows instead give
a rational determinant of degree six.  Comparing its residues at each
opposite pair of poles produces three incompatible linear equations.

## 2. The quadratic residual numerator

Fix five exceptional labels \(R\), put

\[
                         N=E\setminus R,\qquad |N|=p+2,         \tag{2}
\]

and delete a marked pair \(B\subset N\), leaving \(L=N\setminus B\)
of size \(p\).  The isolated-star pivot is the nonzero scalar multiple

\[
       C_{L\mid R}=2h_{01}^{\,p}\operatorname {per}{\cal C}_{L\mid R},
                                                                    \tag{3}
\]

where the columns of the \(p\times p\) Cauchy matrix are the five
values in \(R\) and \(k\) copies of the common value \(\mu\).  As in the
preceding layers, a single nonzero pivot completes all three target
rows at every active star site.  Suppose, for contradiction, that all
pivots (3) vanish.

For \(k=1\) this is ordinary Borchardt.  For \(k\ge2\), collide the
common columns after replacing them by the divided jets

\[
 {1\over j!}\partial_\mu^j{1\over z+\mu},\qquad
 {1\over j!}\partial_\mu^j{1\over(z+\mu)^2},
 \qquad 0\le j<k.                                             \tag{4}
\]

The confluent Cauchy denominator is nonzero: \(\mu\) is different from
every exceptional value, the five exceptional column values are
distinct, and every row--column sum is structurally nonzero.  Hence the
confluent determinant quotient is equivalent to the permanent, also at
the boundary \(k=1\).

Fix \(R\).  Confluent Borchardt turns the pivots obtained by varying
\(B\) into all maximal minors of the \((p+2)\times p\) global numerator
matrix.  They all vanish, so a nonzero column dependence gives a
rational function

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+\mu)^{k+1}\prod_{c\in R}(z+\nu_c)^2.                \tag{5}
\]

The partial fractions in this dependence are independent, so
\(Q_R\ne0\).  Moreover

\[
        \deg D_R=(k+1)+10=p+6,\qquad \deg Q_R\le p+4.          \tag{6}
\]

The function has the \(p+2\) distinct row zeros in \(N\).  Therefore

\[
 Q_R(z)=P_N(z)q_R(z),\qquad
 P_N(z)=\prod_{i\in N}(z-\nu_i),\qquad 0\ne q_R,\quad
 \deg q_R\le2.                                                \tag{7}
\]

## 3. Residues at the five exceptional columns

At a value \(a\in R\), the partial fraction expansion of \(F_R\) has a
double pole at \(-a\) but no simple pole.  Applying that condition to
(5)--(7) gives

\[
                    q_R'(-a)+Y_a(R)q_R(-a)=0,                 \tag{8}
\]

where

\[
 \begin{split}
 A_a&=-\sum_{i\in E\setminus\{a\}}{1\over a+\nu_i}
       -{k+1\over\mu-a},\\
 \psi(a,x)&={1\over a+x}-{2\over x-a}
            =-{x+3a\over x^2-a^2},\\
 Y_a(R)&=A_a+\sum_{c\in R\setminus\{a\}}\psi(a,c).
 \end{split}                                                   \tag{9}
\]

Indeed, if \(\widetilde D_a=D_R/(z+a)^2\), absence of the simple pole
is

\[
 0=\left({Q_R\over\widetilde D_a}\right)'\!(-a)
  ={P_N(-a)\over\widetilde D_a(-a)}
       \bigl(q_R'(-a)+Y_a(R)q_R(-a)\bigr).                    \tag{10}
\]

Every factor divided out in (10) is nonzero: the beta values are
distinct, no structural pair sum vanishes, and \(\mu-a\ne0\).

Choose four distinct nonzero exceptional values \(a,b,c,d\).  This is
possible because at most one value is zero and \(|E|=p+7\ge13\).  For
every exceptional value \(x\) outside this core, take

\[
                         R_x=\{a,b,c,d,x\}.                    \tag{11}
\]

Absorb the fixed terms in (9) into constants \(U,V,W\), so the three
anchor coefficients are

\[
       Y_a(x)=U+\psi(a,x),\quad
       Y_b(x)=V+\psi(b,x),\quad
       Y_c(x)=W+\psi(c,x).                                    \tag{12}
\]

Writing \(q_{R_x}(z)=u_xz^2+v_xz+w_x\), equation (8) at an anchor
\(s\in\{a,b,c\}\) is the row

\[
 \bigl(s^2Y_s(x)-2s,\ 1-sY_s(x),\ Y_s(x)\bigr)
             \begin{pmatrix}u_x\\v_x\\w_x\end{pmatrix}=0. \tag{13}
\]

Because \(q_{R_x}\ne0\), the determinant of these three rows vanishes.

## 4. More roots than the moving determinant can have

For abstract \(A,B,C\), the determinant in (13) is

\[
\begin{split}
 \Phi(A,B,C)={}&-\Delta ABC
 +(b-a)(a+b-2c)AB +(a-c)(a+c-2b)AC\\
 &+(c-b)(b+c-2a)BC
 +2(c-b)A+2(a-c)B+2(b-a)C,                         \tag{14}\\
 \Delta={}&(a-b)(a-c)(b-c).
\end{split}
\]

Substitute (12).  Multiplication by

\[
                 (x^2-a^2)(x^2-b^2)(x^2-c^2)                  \tag{15}
\]

clears the denominators and gives a polynomial of degree at most six.
It vanishes at all \(p+3\ge9\) exceptional values outside the
four-value core.  Those values are distinct and none is a pole: equality
with an anchor is excluded by construction, while equality with its
negative would make a structural pair sum zero.  Thus the polynomial,
and hence the rational determinant, is identically zero.

## 5. Opposite-pole residues are incompatible

The moving term has residues

\[
       \operatorname*{res}_{x=a}\psi(a,x)=-2,\qquad
       \operatorname*{res}_{x=-a}\psi(a,x)=1.                 \tag{16}
\]

At either pole only the \(A\)-argument of \(\Phi\) is singular.  Thus
the identity from Section 4 forces

\[
 \Phi_A\bigl(V+\psi(b,a),W+\psi(c,a)\bigr)=0,
 \quad
 \Phi_A\bigl(V+\psi(b,-a),W+\psi(c,-a)\bigr)=0.              \tag{17}
\]

Subtracting the two equations and simplifying gives

\[
 {2a(b-c)\over(a+b)(a+c)}L_a=0,
 \qquad
 L_a=(a^2-b^2)V+(a^2-c^2)W+2a-b-c.                            \tag{18}
\]

Every displayed prefactor is structurally nonzero.  Repeating the same
opposite-pole subtraction at \(b\) and \(c\) yields

\[
\begin{split}
 L_a&=(a^2-b^2)V+(a^2-c^2)W+2a-b-c=0,\\
 L_b&=(a^2-b^2)U+(c^2-b^2)W+a-2b+c=0,\\
 L_c&=(a^2-c^2)U+(b^2-c^2)V+a+b-2c=0.                         \tag{19}
\end{split}
\]

But their following linear combination contains no \(U,V,W\):

\[
 -(b^2-c^2)L_a-(a^2-c^2)L_b+(a^2-b^2)L_c
             =3(a-b)(a-c)(b-c).                              \tag{20}
\]

The right side is nonzero because the three anchor values are distinct.
Equations (19) are therefore inconsistent.  This contradicts the
assumption that every pivot vanishes and proves Theorem 1.1.

Notice that the argument never divides by a value of a limiting
quadratic.  It therefore includes the cases in which the quadratic in
(7) drops degree, has a repeated root, or vanishes at one of the three
anchor points.

## 6. Scope

The all-distinct stratum of the entire \(t=r+6\) layer is now closed,
uniformly for \(r\ge7\).  Collision strata in this fifth split layer
are not claimed here; they are the next remaining no-extra-singular
cases.

## 7. Exact audit

[verify_live_three-zero-fifth-split-distinct-beta.py](../computations/verify_live_three_zero_fifth_split_distinct_beta.py)
checks the degree counts, derives (14) directly from the three residue
rows, verifies the six pole residues, proves all three identities
(18)--(19) symbolically, audits every denominator used in the
opposite-pole comparison, and checks the incompatibility certificate
(20).
