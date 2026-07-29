# Two exact obstructions for the full nine-cap compatibility equations

## 1. Scope and outcome

Fix the two deleted vertices of a hypothetical eight-site ternary source
and write its internal six-site quadratic as (q).  For a quadratic (Z)
on the remaining sites put

\[
  \mathcal H_q(Z):=\frac{Zq^2}{2}.
\]

If the deleted-star rows are (p_0,p_1,p_2) and
(s_0,s_1,s_2), and the direct deleted-pair matrix is
((a_{cd})), then the full two-deletion compatibility system is

\[
 \boxed{\quad
 \mathcal H_q\bigl(a_{cd}q+3p_cs_d\bigr)
   =\delta_{cd}X_c,
 \qquad 0\le c,d\le2,
 \quad}                                                     \tag{1}
\]

where (X_c=\prod_{i=0}^5x_{i,c}), and multiplication of two linear
forms is taken in the site-square-zero algebra.  Thus on (i<j),

\[
 (p_cs_d)_{ij}(\alpha,\beta)
 =p_{c,i,\alpha}s_{d,j,\beta}
  +p_{c,j,\beta}s_{d,i,\alpha}.                            \tag{2}
\]

This note proves that (1) is impossible for each of two fixed internal
quadratics:

1. the rational single-cap counterexample (q_{\rm rat}); and
2. the sparse core (q_{\rm sp}) made from the six internal edges of
   three completed monochromatic matchings.

For the first core, a left-kernel functional already excludes every
diagonal equation.  For the second, the off-diagonal cap equations force
an impossible triangle of polarized rank-one pairs.

These are **fixed-(q) subchart theorems**.  They do not show that an
arbitrary internal (q) of an eight-site source can be reduced to either
core, and hence are not a proof of the uniform conjecture.

## 2. The rational core is outside all three pure affine fibers

The nonzero cells of (q_{\rm rat}) are

\[
\begin{array}{c|r@{\qquad}c|r}
(ij;\alpha,\beta)&q_{ij}(\alpha,\beta)&
(ij;\alpha,\beta)&q_{ij}(\alpha,\beta)\\ \hline
(01;1,0)&-1 &(03;0,0)&1\\
(03;1,1)&1  &(04;1,0)&-1\\
(04;1,1)&1  &(05;2,2)&1\\
(12;0,1)&-1 &(12;2,2)&1\\
(13;0,1)&-1 &(14;2,0)&-1\\
(15;1,1)&1/3&(23;1,1)&1\\
(24;1,0)&-1 &(25;0,0)&1/6\\
(34;1,0)&-1 &(34;2,2)&1/3.
\end{array}                                                \tag{3}
\]

This is the same (q) for which one isolated polarized equation has the
rational solution recorded in
`notes/polarized-six-site-paircap-counterexample.md`.  Requiring all nine
caps changes the conclusion completely.

For a six-letter color word (gamma), let
([\gamma]T) denote its coefficient in a top-degree tensor (T).  Define
the following functional; omitted words have coefficient zero.

\[
\begin{array}{c|r@{\quad}c|r}
\gamma&\ell_\gamma&\gamma&\ell_\gamma\\ \hline
000000&1&011001&-1/2\\
011011&1&020000&1\\
100110&-1&111111&-1/2\\
112111&-1/2&120110&-1\\
201102&-1/6&201112&1/6\\
201222&-1/2&202112&-1/6\\
221102&-1/6&221112&1/6\\
221222&-1/2&222102&-1/6\\
222222&-1/2&&
\end{array}                                                \tag{4}
\]

Thus

\[
  \ell(T)=\sum_\gamma\ell_\gamma[\gamma]T.
\]

Direct substitution of (3) gives the finite identity

\[
               \ell\bigl(\mathcal H_{q_{\rm rat}}(Z)\bigr)=0
               \qquad\text{for every quadratic }Z.       \tag{5}
\]

There are only (15\cdot9=135) basis cells (Z_{ij}(\alpha,\beta));
after multiplying (4) by six, (5) is an integral coefficient check on
those 135 cells.  The exact audit cited below performs precisely this
check.  On the three pure tensors,

\[
       \ell(X_0)=1,
       \qquad \ell(X_1)=-\frac12,
       \qquad \ell(X_2)=-\frac12.                         \tag{6}
\]

If (c=d) in (1), its left side lies in the image of
(mathcal H_{q_{\rm rat}}), while its right side is (X_c).
Equations (5)--(6) are an immediate contradiction.  Notice that this
argument allows arbitrary complex (p_c,s_c,a_{cc}); the special
factorization of (Z) is not needed.

## 3. The sparse three-completed-matchings core

Let (q_{\rm sp}) have the following six unit cells:

\[
\begin{array}{c|c}
\text{color }0 &(23;0,0),(45;0,0)\\
\text{color }1 &(14;1,1),(35;1,1)\\
\text{color }2 &(05;2,2),(34;2,2).
\end{array}                                                \tag{7}
\]

Adding respectively the cells ((01;0,0)), ((02;1,1)), and
((12;2,2)) completes the three monochromatic perfect matchings.  The
six cells in (7) have exactly six disjoint pairs.  Three same-color pairs
expose the site pairs (01,02,12); explicitly, for every
(\alpha,\beta\),

\[
\begin{aligned}
 [\alpha\beta0000]\mathcal H_{q_{\rm sp}}(Z)
      &=Z_{01}(\alpha,\beta),\\
 [\alpha1\beta111]\mathcal H_{q_{\rm sp}}(Z)
      &=Z_{02}(\alpha,\beta),\\
 [2\alpha\beta222]\mathcal H_{q_{\rm sp}}(Z)
      &=Z_{12}(\alpha,\beta).
\end{aligned}                                             \tag{8}
\]

Every row in (8) has a unique contributing pair of (q)-cells.  The only
collision anywhere in the two-(q)-edge expansion is

\[
                     \gamma_* = 210012,                   \tag{9}
\]

where three terms meet.  In particular,

\[
 \mathcal H_{q_{\rm sp}}(q_{\rm sp})=3[\gamma_*],         \tag{10}
\]

so the central scalar (a_{cd}) affects none of the 27 rows in (8).

Package all cap indices at once.  For a site-local coordinate
((i,\alpha)), set

\[
 P_{i\alpha}=(p_{0,i,\alpha},p_{1,i,\alpha},p_{2,i,\alpha})^t,
 \qquad
 S_{i\alpha}=(s_{0,i,\alpha},s_{1,i,\alpha},s_{2,i,\alpha})^t,
\]

and write (x_{i\alpha}=(P_{i\alpha},S_{i\alpha})).  For two such
pairs define the (3\times3) matrix

\[
 \Phi\bigl((P,S),(P',S')\bigr)=PS'^t+P'S^t.               \tag{11}
\]

Using (2), the ((c,d))-entry of (11) is exactly the star-product cell
appearing in the ((c,d))-cap.  Equations (1) and (8) therefore imply

\[
\begin{aligned}
 \Phi(x_{0\alpha},x_{1\beta})
   &=\frac13\delta_{\alpha0}\delta_{\beta0}E_{00},\\
 \Phi(x_{0\alpha},x_{2\beta})
   &=\frac13\delta_{\alpha1}\delta_{\beta1}E_{11},\\
 \Phi(x_{1\alpha},x_{2\beta})
   &=\frac13\delta_{\alpha2}\delta_{\beta2}E_{22}.
\end{aligned}                                             \tag{12}
\]

Crucially, the zero matrices in (12) include all off-diagonal cap slices;
an isolated diagonal equation would not supply this compatibility.

## 4. The zero-triangle lemma

We use a two-line classification of the zero locus of (11).

**Lemma 4.1.**  Let (x,y,z\in U\oplus V) be nonzero, where

\[
 \Phi((P,S),(P',S'))=P\otimes S'+P'\otimes S.
\]

Over a field of characteristic different from two, if

\[
                 \Phi(x,y)=\Phi(x,z)=\Phi(y,z)=0,         \tag{13}
\]

then either all three points are (P)-pure ((S=0)) or all three are
(S)-pure ((P=0)).

**Proof.**  If (x=(P,0)) with (P\ne0), then
(Phi(x,y)=P\otimes S_y=0) and
(Phi(x,z)=P\otimes S_z=0), so (y,z) are also (P)-pure.
The (S)-pure case is symmetric.

It remains to exclude (P\ne0\ne S).  From (Phi(x,y)=0), a nonzero
(y) must also have both components nonzero.  Equality of the two
nonzero decomposable tensors gives

\[
                     y=\lambda(P,-S)
\]

for some (lambda\ne0).  Likewise
(z=\mu(P,-S)) with (mu\ne0).  But then

\[
             \Phi(y,z)=-2\lambda\mu P\otimes S\ne0,
\]

contrary to (13).  \(\square\)

## 5. Contradiction for the sparse core

Select the six pairs

\[
 A=x_{00},\quad B=x_{10},\quad
 C=x_{01},\quad D=x_{21},\quad
 E=x_{12},\quad F=x_{22}.                                \tag{14}
\]

The three nonzero equations in (12) say

\[
 \Phi(A,B)=\frac13E_{00},\qquad
 \Phi(C,D)=\frac13E_{11},\qquad
 \Phi(E,F)=\frac13E_{22}.                                \tag{15}
\]

Thus all six pairs are nonzero.  The remaining entries of (12) give two
zero triangles

\[
 \Phi(A,E)=\Phi(A,D)=\Phi(E,D)=0,                         \tag{16}
\]

\[
 \Phi(C,B)=\Phi(C,F)=\Phi(B,F)=0,                         \tag{17}
\]

as well as the bridge

\[
                         \Phi(A,F)=0.                     \tag{18}
\]

By Lemma 4.1, (A,E,D) are all pure of one type, and (C,B,F) are all
pure of one type.  Equation (18) forces those types to be the same: two
nonzero pure points of opposite type have a nonzero decomposable product.
Consequently (A) and (B) are pure of the same type, so
(Phi(A,B)=0), contradicting (15).  This proves that (1) has no complex
solution for (q=q_{\rm sp}).

## 6. Exact audit

Run

```text
uv run python computations/verify_n8_full_pair_suspension_subcharts.py
```

The script uses rational arithmetic to check:

1. all 135 basis-cell identities in (5), along with (6);
2. the 51 singleton quotient rows and sole three-term collision (9);
3. equation (10) and every exposed row in (8); and
4. the target, zero-triangle, and bridge incidences in (14)--(18).

