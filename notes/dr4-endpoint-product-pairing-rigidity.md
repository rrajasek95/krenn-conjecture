# DR4 endpoint rigidity on the product-pairing exception

## 1. Scope

Let $t_0,t_1,t_2,t_3$ be four distinct nonzero anchors, with
$t_i+t_j\ne0$.  In the endpoint-linearization route to DR4, the generic
coefficient span can drop rank on a product-pairing divisor

\[
                         t_0t_3=t_1t_2.                       \tag{1}
\]

After a permutation and a common scaling, write

\[
                         (t_0,t_1,t_2,t_3)=(1,a,b,ab).        \tag{2}
\]

The first toric compatibility minor for the one-dimensional endpoint
kernel is, up to structural nonzero factors,

\[
                         H(a,b)=(a+1)^2(b+1)^2-16ab.          \tag{3}
\]

Thus $H\ne0$ already contradicts a nonzero translation vector.  This
note closes the exceptional subcurve $H=0$.  It is independent of a
choice of pivot minor: the certificate uses homogeneous cofactor vectors
from two overlapping charts.

## 2. The sixteen endpoint rows

For each omitted anchor $t_i$, let $J_i=\{0,1,2,3\}\setminus\{i\}$ and
let $T^{(i)}$ be the nodal differentiation matrix on the three nodes in
$J_i$.  The two endpoint residues at $x=\pm t_i$ give

\[
 E_i^\pm(U)=\det\bigl(T^{(i)}+\operatorname {diag}
             (V_{ij}^\pm:j\in J_i)\bigr)=0,                 \tag{4}
\]

where

\[
 V_{ij}^+=U_j-{2\over t_j+t_i},\qquad
 V_{ij}^-=U_j-{1\over t_j+t_i}-{1\over t_j-t_i}.            \tag{5}
\]

Conjugating $T^{(i)}$ by its barycentric weights gives a matrix whose
off-diagonal entries are $1/(t_j-t_k)$ and hence skew-symmetric.  If
$J_i=\{j,k,\ell\}$ and $m_h$ denotes the resulting diagonal entry after
the shift in (5), then

\[
 E_i^\pm=
 U_jU_kU_\ell+
 \sum_{\{j,k\}\subset J_i}m_\ell U_jU_k+
 \sum_{j\in J_i}
 \left(m_km_\ell+{1\over(t_k-t_\ell)^2}\right)U_j.          \tag{6}
\]

The constant term vanishes because $U=0$ has the canonical endpoint
kernel.  Consequently the eight polynomials $E_i^\pm$ and the eight
consequences $U_iE_i^\pm$ are linear forms in the fifteen nonconstant
squarefree monomials

\[
                    U_S=\prod_{i\in S}U_i,qquad
                    \varnothing\ne S\subseteq\{0,1,2,3\}.   \tag{7}
\]

Let $M(a,b)$ be their $16\times15$ coefficient matrix, with rows ordered

\[
 E_i^+,\ U_iE_i^+,\ E_i^-,\ U_iE_i^-\qquad(i=0,1,2,3).     \tag{8}
\]

Any endpoint solution gives a vector
$m(U)=(U_S)_{S\ne\varnothing}$ in $\ker M$.

## 3. Passing to the quadratic exceptional curve

On $H=0$, the element $b$ obeys

\[
 b^2+c(a)b+1=0,qquad
 c(a)={2(a^2-6a+1)\over(a+1)^2}.                            \tag{9}
\]

We work over the quadratic function field

\[
                 K=\mathbb Q(a)[b]/(b^2+c(a)b+1).            \tag{10}
\]

The conjugate of $b$ is $b^{-1}=-c-b$.  Thus for $q=r+sb\in K$,

\[
                 \operatorname {Nm}(q)=r^2-crs+s^2.         \tag{11}
\]

The discriminant is

\[
                  c(a)^2-4={-64a(a-1)^2\over(a+1)^4}.        \tag{12}
\]

Its degeneracies are structural: $a=0$ violates nonzero anchors,
$a=1$ collides two anchors, and $a=-1$ is already excluded by
$t_0+t_1\ne0$.

## 4. Homogeneous cofactor certificate

Take two fourteen-row submatrices of $M$:

\[
 N_1=M\text{ with rows }0,1\text{ removed},\qquad
 N_2=M\text{ with rows }0,2\text{ removed}.                 \tag{13}
\]

For $h=1,2$, let $v^{(h)}=(v_S^{(h)})$ be the vector of signed
$14\times14$ column cofactors of $N_h$.  This definition is homogeneous
and remains valid when any particular pivot minor vanishes.  It gives

\[
                              N_hv^{(h)}=0.                  \tag{14}
\]

Every genuine monomial vector satisfies, for any two pairs
$\{i,j\}$ and $\{k,\ell\}$,

\[
 B_{ij,k\ell}(m):=
 m_{ij}m_km_\ell-m_{k\ell}m_im_j=0.                         \tag{15}
\]

The exact cofactor calculation in $K$ gives, up to nonzero rational
constants and structural denominator factors,

\[
\begin{split}
 \gcd_{ij,k\ell}\operatorname {Nm}
       B_{ij,k\ell}(v^{(1)})
   &=(a+1)^{62}P_{16}(a)^3,\\
 \gcd_{ij,k\ell}\operatorname {Nm}
       B_{ij,k\ell}(v^{(2)})
   &=(a+1)^{68}Q_4(a)^6R_4(a)^3,                             \tag{16}
\end{split}
\]

where

\[
\begin{split}
P_{16}(a)={}&9a^{16}+520a^{15}+13592a^{14}+200920a^{13}
 +1823420a^{12}+10125640a^{11}\\
&+34858664a^{10}+74460120a^9+96772854a^8
 +74460120a^7+34858664a^6\\
&+10125640a^5+1823420a^4+200920a^3+13592a^2+520a+9,\\
Q_4(a)={}&a^4+2a^3+18a^2+2a+1,\\
R_4(a)={}&a^4+5a^3+24a^2+5a+1.
\end{split}                                                   \tag{17}
\]

Most importantly, the two chart gcds have

\[
 \gcd\left(gcd\operatorname {Nm}B(v^{(1)}),
            \gcd\operatorname {Nm}B(v^{(2)})\right)
                         =(a+1)^{62}.                         \tag{18}
\]

For an admissible $a$, (18) says that some cofactor vector $v^{(h)}$ is
nonzero and has a nonzero toric binomial.  Indeed a nonzero norm is
nonzero at both quadratic conjugates.  That $N_h$ has rank fourteen, so
any nonzero vector in its kernel is proportional to $v^{(h)}$.

If $U\ne0$, then $m(U)\ne0$ and (14) gives
$m(U)=\theta v^{(h)}$ with $\theta\ne0$.  But (15) and homogeneity give

\[
                0=B_{ij,k\ell}(m(U))
                  =\theta^3B_{ij,k\ell}(v^{(h)}),            \tag{19}
\]

contradicting the chosen nonzero cofactor binomial.  Hence $U=0$.

**Endpoint product-pairing lemma.**  The product-pairing rank-drop
stratum (1) has no nonzero DR4 translation vector.  On the only residual
subcurve (3), the conclusion follows from the two-chart cofactor
certificate (16)--(19).

## 5. Exact audit

[verify_dr4_endpoint_product_pairing_rigidity.py](../computations/verify_dr4_endpoint_product_pairing_rigidity.py)
constructs (6) directly in the quadratic field (10), checks (12), forms
both homogeneous cofactor vectors, verifies (14), computes every toric
binomial in (15), and reproduces the three factorizations (16) and (18).
