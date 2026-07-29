# Full four-anchor endpoint rigidity

## 1. The theorem

Let \(t_0,t_1,t_2,t_3\) be distinct nonzero complex numbers satisfying

\[
                         t_i+t_j\ne0\qquad(i\ne j).           \tag{1}
\]

For a cubic \(q\), define the four cleared Robin rows

\[
 \mathcal R_i(x)q
 =(x^2-t_i^2)\bigl(q'(t_i)+U_iq(t_i)\bigr)
 -(x-3t_i)q(t_i).                                           \tag{2}
\]

**Theorem (DR4).**  If

\[
                  \det\bigl(\mathcal R_i(x)\bigr)_{i=0}^3
                  \equiv0
                  \quad\text{as a polynomial in }x,          \tag{3}
\]

then

\[
                              U_0=U_1=U_2=U_3=0.              \tag{4}
\]

This note assembles the corrected generic endpoint-span certificate with
the product-pairing exceptional certificate.  The latter is
[dr4-endpoint-product-pairing-rigidity.md](dr4-endpoint-product-pairing-rigidity.md).

## 2. The sixteen endpoint equations

At \(x=\pm t_i\), the \(i\)-th row of (2) becomes a nonzero multiple of
evaluation at \(t_i\).  Writing \(q(z)=(z-t_i)r(z)\) reduces the other three
rows to quadratic Robin rows with translations

\[
 V_{ij}^+=U_j-{2\over t_i+t_j},\qquad
 V_{ij}^-=U_j-{1\over t_i+t_j}-{1\over t_j-t_i}
 \qquad(j\ne i).                                             \tag{5}
\]

Hence (3) implies the eight cubic equations

\[
 E_i^\pm(U)=
 \det\left(
 V_{ij}^\pm,\ 1+t_jV_{ij}^\pm,\ 2t_j+t_j^2V_{ij}^\pm
 \right)_{j\ne i}=0.                                        \tag{6}
\]

The inherited order of the three indices is used in each determinant.
The coefficient of \(\prod_{j\ne i}U_j\) in \(E_i^\pm\) is a nonzero
Vandermonde factor.  Moreover, \(E_i^\pm\) contains only squarefree
monomials in the three variables \(U_j\), \(j\ne i\).  Thus the equations

\[
                         E_i^\pm=0,\qquad U_iE_i^\pm=0        \tag{7}
\]

are sixteen linear equations on the fifteen nonconstant squarefree
monomials

\[
                 m(U)=\left(\prod_{i\in S}U_i\right)_{
                 \varnothing\ne S\subseteq\{0,1,2,3\}}.      \tag{8}
\]

Let \(M(t)\) be their \(16\times15\) coefficient matrix.  If
\(\operatorname{rank}M(t)=15\), then (7) forces \(m(U)=0\), and its four
singleton coordinates give (4).

## 3. Generic rank fifteen

The system is invariant under a common nonzero scaling of the nodes, with
the inverse scaling of the translations.  Normalize

\[
                         (t_0,t_1,t_2,t_3)=(1,a,b,c).         \tag{9}
\]

All structural conditions in this chart are summarized by

\[
 \Omega=abc(a^2-1)(b^2-1)(c^2-1)
        (a^2-b^2)(a^2-c^2)(b^2-c^2)\ne0.                    \tag{10}
\]

Put

\[
               \rho=(a-bc)(ab-c)(ac-b).                     \tag{11}
\]

The exact endpoint-span reduction first uses the four normalized rows
\(E_i^+\) as the four cubic pivots and \(U_0E_0^+\) as the quartic pivot.
After removing those five columns, eleven rows remain on the ten quadratic
and linear monomials.  Two \(10\times10\) minors of that low block are

\[
\begin{split}
 M_8&=-{2^{17}3^3\,a b^2c^2\,\rho\,P_2\over D_8},\\
 M_9&={2^{17}3^3\,a^2bc^2(a-c)^2\,\rho\,P_3\over D_9},       \tag{12}
\end{split}
\]

where \(D_8,D_9\) are products only of the difference and pair-sum factors
appearing in \(\Omega\).  The corrected signs and the factor
\((a-c)^2\) in \(M_9\) are important.  The two explicit numerator
polynomials satisfy

\[
                         P_2+P_3
 =4c(a-b)(a+b)(ab-c).                                      \tag{13}
\]

All identities in (12)--(13) are checked over
\(\mathbb Q(a,b,c)\) by
[verify_dr4_endpoint_generic_rigidity.py](../computations/verify_dr4_endpoint_generic_rigidity.py).

If \(\rho\ne0\), the right side of (13) is structurally nonzero.  Therefore
\(P_2\) and \(P_3\) cannot both vanish.  Every other factor in the
corresponding minor (12) is nonzero by (10).  One low minor is nonzero, so
the low block has rank ten and \(M(t)\) has rank fifteen.  Section 2 then
gives \(U=0\).

## 4. Reduction of every rank-drop divisor

The three factors of \(\rho\) say, respectively,

\[
 t_0t_1=t_2t_3,\qquad
 t_0t_3=t_1t_2,\qquad
 t_0t_2=t_1t_3.                                             \tag{14}
\]

They are the three partitions of four indices into two pairs.  Permuting
the anchors therefore reduces any point of \(\rho=0\) to

\[
                         t_0t_3=t_1t_2.                      \tag{15}
\]

After the same common scaling as in (9), write

\[
                         (t_0,t_1,t_2,t_3)=(1,a,b,ab).       \tag{16}
\]

The complete structural divisor in this chart is

\[
 ab(a^2-1)(b^2-1)(a^2-b^2)(a^2b^2-1)\ne0.                  \tag{17}
\]

Thus no division or permutation in (15)--(16) loses an admissible point.

## 5. The product-pairing certificate

On (16), the product-pairing endpoint calculation has a one-dimensional
coefficient kernel away from further chart divisors.  Its homogeneous
toric compatibility certificate forces

\[
                         H(a,b)=(a+1)^2(b+1)^2-16ab=0        \tag{18}
\]

for any nonzero monomial vector \(m(U)\).  The computation is homogeneous
in the kernel cofactors, so zeros of a chosen pivot minor do not create an
exception.  Consequently \(H\ne0\) already gives \(m(U)=0\), hence \(U=0\).

It remains to treat \(H=0\).  Since \(a+1\ne0\), equation (18) is

\[
 b^2+\kappa(a)b+1=0,\qquad
 \kappa(a)={2(a^2-6a+1)\over(a+1)^2}.                        \tag{19}
\]

Work in the quadratic function field

\[
                   K=\mathbb Q(a)[b]/(b^2+\kappa b+1).       \tag{20}
\]

The discriminant

\[
                   \kappa(a)^2-4
 ={ -64a(a-1)^2\over(a+1)^4}                                \tag{21}
\]

degenerates only at \(a=0,1,-1\), all excluded by (17).

The product-pairing checker forms two fourteen-row submatrices of the
sixteen-row matrix \(M\) and their homogeneous signed cofactor kernels
\(v^{(1)},v^{(2)}\).  A genuine squarefree monomial vector obeys every
homogeneous toric binomial

\[
 B_{ij,k\ell}(m)
 =m_{ij}m_km_\ell-m_{k\ell}m_im_j=0.                         \tag{22}
\]

For each cofactor vector, take the gcd of the norms to \(\mathbb Q(a)\) of
all nonzero binomials (22).  The two exact gcds are

\[
\begin{split}
 G_1&=3^8(a+1)^{62}P_{16}(a)^3,\\
 G_2&=3^8(a+1)^{68}Q_4(a)^6R_4(a)^3,\\
 \gcd(G_1,G_2)&=3^8(a+1)^{62}.                              \tag{23}
\end{split}
\]

These identities, the quadratic-field arithmetic, and the cofactor kernel
equations are checked by
[verify_dr4_endpoint_product_pairing_rigidity.py](../computations/verify_dr4_endpoint_product_pairing_rigidity.py).

At an admissible point \(a+1\ne0\), (23) ensures that one chart has rank
fourteen and a cofactor vector with a nonzero toric binomial.  If \(U\ne0\),
then \(m(U)\ne0\), lies in that one-dimensional kernel, and equals
\(\theta v^{(h)}\) for some \(\theta\ne0\).  Homogeneity gives

\[
             0=B_{ij,k\ell}(m(U))
              =\theta^3B_{ij,k\ell}(v^{(h)})\ne0,            \tag{24}
\]

a contradiction.  Hence \(U=0\) also on \(H=0\).

## 6. Exhaustion and status

The alternatives are exhaustive:

1. \(\rho\ne0\): the corrected minors (12) give rank fifteen;
2. \(\rho=0\): permutation and scaling give (16);
3. on (16), \(H\ne0\) is excluded by the first homogeneous toric
   compatibility certificate;
4. on \(H=0\), the two-chart norm certificate (23) excludes \(U\ne0\).

Every denominator used is a factor of the structural products (10) or
(17).  The only degeneracies of the quadratic extension are likewise
structural.  This proves DR4 in full.
