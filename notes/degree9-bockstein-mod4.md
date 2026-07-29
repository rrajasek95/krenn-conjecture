# Exact degree-nine two-adic obstruction

## Outcome

The characteristic-two identity for the six-site degree-nine source ideal
does not lift modulo four. More precisely, for the complete multigraded
Macaulay map $A$ and target $b=P$,

\[
 b\in A\mathbf Z^{\mathcal C}+2\mathbf Z^{\mathcal R},
 \qquad
 b\notin A\mathbf Z^{\mathcal C}+4\mathbf Z^{\mathcal R}. \tag{1}
\]

The second assertion is certified by a support-2,179 character modulo four.
It is independent of the chosen characteristic-two certificate and is
lossless before symmetry reduction. Thus the proposed coefficientwise
two-adic descent stops after its first step.

There is also an exact, primitive integral left-kernel functional whose
pairing with $b$ has two-adic valuation $12$. It annihilates the rational
saturation of the source image and gives a compatible obstruction at every
modulus at least $2^{13}$. The exact divisibility of $b$ in the saturated
free quotient is therefore between $2^1$ and $2^{12}$; the mod-four
character by itself does not show that the saturated depth is one.

## 1. Integral odd-order quotient

Let

\[
 H=\langle(012),(345)\rangle_{\rm vertex}
       \times\langle(012)\rangle_{\rm color},\qquad |H|=27. \tag{2}
\]

Write $R_r$ and $C_j$ for the sizes of a row orbit and a column orbit, and
let $m_{rj}\in\{0,\ldots,15\}$ be the raw incidence multiplicity stored in
computations/degree9_source_ideal_h27_integer.pkl. In orbit-sum bases the
integral map has entry $C_jm_{rj}/R_r$. Multiplying row $r$ by the odd unit
$R_r$ gives the equivalent power-of-two matrix

\[
 \bar A_{rj}=C_jm_{rj},\qquad
 \bar b_r=R_r[\text{$r$ is a target row}].                 \tag{3}
\]

All $R_r,C_j\in\{1,3,9,27\}$, so (3) loses no information modulo any power
of two. Since $27$ is a unit modulo $2^k$, Reynolds averaging is valid: a
solution in the full Macaulay domain would average to an $H$-invariant
solution. Every conclusion below therefore applies before quotienting by
$H$.

All rows have exactly the same multidegree. Each is a perfect matching of
the 18 stubs $(v,a)$, and hence has degree one at every vertex/color port.
The target $P=F_{0^6}F_{1^6}F_{2^6}$, every product $Q_cF_c$, and every
integral residual below lie in this one degree-nine multigraded component.

## 2. The first residual and the Bockstein character

The saved GF(2) membership certificate gives $x_0$ with

\[
                  \bar b-\bar A x_0=2\bar r.               \tag{4}
\]

The integral residual has 395,542 nonzero row orbits, coefficients between
$-12$ and $-1$, and 267,141 odd coefficients. The saved support-54 GF(2)
dual $y$ satisfies

\[
 y^T\bar A=0\pmod2,\qquad y^T\bar r=1\pmod2.               \tag{5}
\]

Thus this particular choice of $x_0$ cannot be iterated. That fact alone
would not exclude another mod-two solution: changing $x_0$ by an element
of $\ker(A\bmod2)$ changes the next residual by its Bockstein class.

To remove this dependence, define

\[
                   w_j={y^T\bar A_j\over2}\pmod2.          \tag{6}
\]

Exact sparse elimination solves $\bar A^Tu=w$ over GF(2). Consequently

\[
                         \lambda=y+2u                       \tag{7}
\]

has support 2,179 and obeys

\[
 \lambda^T\bar A=0\pmod4,\qquad
 \lambda^T\bar b=2\pmod4.                                 \tag{8}
\]

Equation (8) proves that $\bar A x=\bar b\pmod4$ has no solution. This is
the certificate-independent second assertion in (1).

The transpose has GF(2) rank 150,148 out of 162,672 equations. The
particular character (7) cannot be lifted to a character modulo eight: an
exact dependency of 69,904 transpose equations annihilates
$\bar A\bmod2$ but pairs to one with the next Bockstein right-hand side.
This proves that (7) is not the reduction of a $\mathbf Z_2$ left-kernel
functional. It does not exclude a different liftable mod-four character.

## 3. An exact saturated obstruction

The characteristic-zero $S_6\times S_3$ quotient has shape
$3102\times1314$. CRT and rational reconstruction of the same modular
echelon functional, followed by denominator clearing and division by the
coefficient gcd, gives a primitive integer vector $\ell$ with

\[
 \ell^TA=0\quad\text{over $\mathbf Z$},\qquad
 \nu_2(\ell^Tb)=12.                                       \tag{9}
\]

It has support 1,054 and coefficients of at most 209 bits. The independent
verifier checks (9) directly against all 16,343 integer matrix entries. An
invariant functional annihilating the averaged columns annihilates every
raw column, so (9) is an exact left-kernel functional for the full Macaulay
map as well.

Let $M$ be the integral row lattice, let
$L=A\mathbf Z^{\mathcal C}$, and put

\[
                    L^{\rm sat}=(L\otimes\mathbf Q)\cap M. \tag{10}
\]

If $s\in L^{\rm sat}$, some nonzero integer multiple of $s$ lies in $L$;
(9) then implies $\ell(s)=0$. Hence $\ell$ annihilates the rational
saturation. It follows from (9) that

\[
                         b\notin L^{\rm sat}+2^{13}M.       \tag{11}
\]

On the other hand (1) gives $b\in L^{\rm sat}+2M$. If $e$ is the two-adic
content of the nonzero image of $b$ in the free quotient
$M/L^{\rm sat}$, the present exact certificates establish

\[
                              1\le e\le12.                 \tag{12}
\]

The mod-four obstruction measures divisibility in the unsaturated cokernel
$M/L$, where the depth is exactly one. It may detect 2-primary torsion; the
failed lift of (7) shows why it cannot simply be identified with (12).

## 4. Why an infinite descent would work, and why this one cannot

Suppose integral, or merely $\mathbf Z_{(2)}$-coefficient, identities could
be iterated to give

\[
 P=\sum_c Q_{k,c}F_c+2^kR_k                               \tag{13}
\]

for every $k$, with all terms in the same degree-nine multigrading. The
source coordinates need not themselves be integral. A hypothetical
complex point with all mixed $F_c=0$ and $P\ne0$ yields an algebraic point
after adjoining an equation $tP-1=0$. Clear one common denominator so all
scaled coordinates are algebraic integers. Homogeneity and (13), evaluated
at a prime above two, would force the fixed nonzero left side to have
valuation at least $k$ for every $k$, a contradiction.

Thus nonintegrality of a hypothetical solution is not the obstruction to
an infinite integral polynomial descent. The obstruction is that the
identities do not exist: (8) stops them at modulus four, and (9) also shows
abstractly that the degree-nine class has a nonzero free component.

This says nothing by itself about radical membership, which moves to higher
degree. The one-variable-grade example

\[
                 I=(x-2y)\subset\mathbf Z[x,y],\qquad P=x \tag{14}
\]

is the minimal warning. Give $x,y$ the same degree. Modulo two, $P\in I$,
and integrally

\[
                         x-(x-2y)=2y.                      \tag{15}
\]

The residual $y$ is not in $(x)$ modulo two, while the
characteristic-zero point $x=1,y=1/2$ satisfies $x-2y=0$ and $P=1$.
Identical multidegree, symmetrization, and one exact factor of two do not
imply characteristic-zero or radical membership.

## 5. Exact artifacts

- computations/test_degree9_h27_mod4_bockstein.py
- computations/certificates/degree9_h27_integral_dual_mod4.pkl.gz
  (SHA-256 73a5dfe84a8233f08099c4f5ccc251fbaee9d7324d7b084e9032c967b7b3f08f)
- computations/verify_degree9_h27_power2_dual.py
- computations/certificates/degree9_h27_mod8_lift_obstruction.pkl.gz
  (SHA-256 498ff9ddbd81efd20b34d0e3a1f1141126be1182992c1d32a8a7143ed25c2b6c)
- computations/verify_degree9_h27_mod8_lift_obstruction.py
- computations/reconstruct_degree9_exact_integer_dual.py
- computations/certificates/degree9_exact_integer_dual.pkl.gz
  (SHA-256 78150f215e28f42ad3d105ea4d7dbaca949c57f3578f66a3c692a2b706d72dc7)
- computations/verify_degree9_exact_integer_dual.py

Run the independent verifiers with

~~~text
uv run python computations/verify_degree9_h27_power2_dual.py
uv run python computations/verify_degree9_h27_mod8_lift_obstruction.py
uv run python computations/verify_degree9_exact_integer_dual.py
~~~

They reconstruct every pairing from the saved integer matrices and do not
trust an elimination transcript.
