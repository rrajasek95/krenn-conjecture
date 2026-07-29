# The uniform cap-minor hierarchy

## 1. Outcome

The cap-adjugate identity is not special to an eight-site source.  Let an
exact source have two distinguished sites `p,q` and an even boundary `U`
of size `2m`.  If `a=A_pq`, `x` is the internal boundary quadratic, and
`r=(r_ij)=ell m^T` is the common two-star response, then every square
submatrix of `a` gives a denominator-free identity coupling its top pair
slices.

For equally sized index sets `I,J subset {0,1,2}`, put `d=|I|=|J|` and
assume `1<=d<=min(3,m)`.  In the square-free boundary algebra,

\[
 \boxed{
 {d\over m!}x^{m-d}
 \det\!\left(xa_{I,J}+{m\over d}r_{I,J}\right)
 =\sum_{i\in I,\,j\in J}
       \operatorname {Cof}^{I,J}_{ij}(a)D_{ij}. }
 \tag{1}
\]

Here

\[
 D_{ij}=(e_i^*\otimes e_j^*)\mathbin\lrcorner H_{2m+2}(A)
 =a_{ij}{x^m\over m!}+r_{ij}{x^{m-1}\over(m-1)!}.       \tag{2}
\]

Thus, under `H_(2m+2)(A)=Delta_(2m+2,3)`, the right side of (1) is

\[
 \sum_{i\in I\cap J}
       \operatorname {Cof}^{I,J}_{ii}(a)e_i^{\otimes U}. \tag{3}
\]

The case `d=3` is the uniform adjugate identity

\[
 {3\over m!}x^{m-3}
 \det\!\left(xa+{m\over3}\ell m^{\mathsf T}\right)
 =\sum_{i=0}^2\operatorname {Cof}_{ii}(a)e_i^{\otimes U}. \tag{4}
\]

At `m=3`, (4) is exactly the six-boundary identity in
`cap-adjugate-six-boundary-identity.md`.  The factor `m/3` is the unique
rescaling which removes the internal-boundary term at every order.  Thus
the cancellation is uniform, rather than a coincidence of degree six.

When `a` is invertible, (4) becomes the explicit polarized equation

\[
 {3\det a\over m}\,
 {x^{m-1}\over(m-1)!}
 \left(x+{m\over3}m^{\mathsf T}a^{-1}\ell\right)
 =\sum_i\operatorname {Cof}_{ii}(a)e_i^{\otimes U}.      \tag{5}
\]

This does not alone give an ordinary lower-order hafnian: the last factor
in (5) need not equal `x`, and exact polarized counterexamples show that a
single such equation is possible.  Its value is that every hypothetical
source must satisfy (1) simultaneously for all physical pairs and all cap
minors, with the same internal `x` and the same two star rows.

The audit is `computations/verify_uniform_cap_minor_hierarchy.py`.

## 2. Pair slices

Write the matching quadratic on the boundary as

\[
 x=\sum_{u<v\in U}A_{uv}.
\]

Orient all blocks away from `p,q` and define

\[
 \ell_i=\sum_{u\in U}(e_i^*\otimes\operatorname{id})A_{p|u},
 \qquad
 m_j=\sum_{u\in U}(e_j^*\otimes\operatorname{id})A_{q|u},
 \qquad r_{ij}=\ell_i m_j.                               \tag{6}
\]

A perfect matching either uses `pq`, leaving `m` internal boundary edges,
or sends `p,q` to two boundary sites, leaving `m-1` internal boundary
edges.  This gives (2) exactly.  It retains arbitrary endpoint order,
parallel sources, zero blocks, and complex cancellation.

## 3. A rank-one-update lemma for every minor

Let `b` be a `d by d` matrix over a commutative ring and let `uv^T` have
rank one in the formal sense.  Multilinearity and alternation of the
determinant give

\[
 \det(tb+suv^{\mathsf T})
 =t^d\det b+s t^{d-1}
   \sum_{i,j}\operatorname {Cof}_{ij}(b)u_i v_j.         \tag{7}
\]

Indeed, every term using two columns from `uv^T` has two proportional
columns and vanishes.  This is a polynomial identity and requires neither
invertibility nor a reduced coefficient ring.

Apply (7) to `b=a_(I,J)`, `t=x`, `s=m/d`, and the restricted star rows.
It gives

\[
 \det\!\left(xa_{I,J}+{m\over d}r_{I,J}\right)
 =x^d\det(a_{I,J})+{m\over d}x^{d-1}
   \sum_{i,j}\operatorname {Cof}^{I,J}_{ij}(a)r_{ij}.    \tag{8}
\]

Multiplying by `d x^(m-d)/m!` turns (8) into

\[
 d\det(a_{I,J}){x^m\over m!}
 +\sum_{i,j}\operatorname {Cof}^{I,J}_{ij}(a)r_{ij}
       {x^{m-1}\over(m-1)!}.                             \tag{9}
\]

Euler's identity for the homogeneous determinant says

\[
 \sum_{i,j}\operatorname {Cof}^{I,J}_{ij}(a)a_{ij}
 =d\det(a_{I,J}).                                        \tag{10}
\]

Substitution of (2) in the right side of (1), followed by (10), gives
exactly (9).  This proves (1).

If the full tensor is ternary GHZ, its pair slices obey

\[
                         D_{ij}=\delta_{ij}e_i^{\otimes U}.
\]

Equation (3), and hence (4), follows immediately.  If `a` is invertible,
the matrix determinant lemma in polynomial form gives

\[
 \det\!\left(xa+{m\over3}\ell m^{\mathsf T}\right)
 =\det(a)x^2\left(x+{m\over3}m^{\mathsf T}a^{-1}\ell\right),
\]

which reduces (4) to (5).

## 4. The lower minors and the exact remaining gap

For a principal two-color set `{i,j}`, the `d=2` member reads

\[
 {2\over m!}x^{m-2}
 \det\!\left(
 x\begin{pmatrix}a_{ii}&a_{ij}\\a_{ji}&a_{jj}\end{pmatrix}
 +{m\over2}
 \begin{pmatrix}r_{ii}&r_{ij}\\r_{ji}&r_{jj}\end{pmatrix}
 \right)
 =a_{jj}e_i^{\otimes U}+a_{ii}e_j^{\otimes U}.           \tag{11}
\]

Nonprincipal minors give either one pure row or zero.  These identities
record constraints which disappear if the nine pair caps are treated as
independent boundary families.

What is still missing is a rigidity theorem for the simultaneous system
(1): either it must force one clean Veronese point, contradicting the
six-site theorem after a valid descent, or it must force every physical
pair into an explicit cofactor-degenerate configuration.  Equation (5)
alone cannot supply that theorem, because the isolated polarized equation
`z x^(m-1)/(m-1)! = Delta` has sparse rational solutions already at
`m=3`.  Any continuation must use overlap between different pairs or two
or more members of the minor hierarchy for the same pair.
