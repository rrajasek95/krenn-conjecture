# A rank-one--rank-one shore contains a four-dimensional clean quotient plane

## 1. Outcome

Let \(W\) be the \(2h\)-site residual set of a physical pair cap,
\(h\geq3\), and suppose the complete fixed-label equations are

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                      \tag{1}
\]

Assume that a shore \(W=A\sqcup B\), with \(|B|\leq3\), has aggregate
endpoint ranks

\[
                 \operatorname {rank}P_A=
                 \operatorname {rank}S_A=1.                 \tag{2}
\]

Retaining the fixed physical label coordinates, choose nonzero label
vectors \(\lambda,\mu\in\mathbb C^3\) and shore forms \(U,V\) such
that

\[
                    p_i^A=\lambda_iU,
              \qquad s_j^A=\mu_jV.                          \tag{3}
\]

Define the four-dimensional matrix space

\[
 {\cal Q}_{\lambda,\mu}
   =\{K\in\operatorname {Mat}_{3\times3}(\mathbb C):
             \lambda^{\mathsf T}K=0,\ K\mu=0\}.            \tag{4}
\]

This note proves that every member of (4) is an exact clean physical cap.
Indeed, all response terms meeting \(A\) cancel, so

\[
                 r(K)=p_B^{\mathsf T}Ks_B                  \tag{5}
\]

is supported on at most three sites.  Hence \(r(K)^{[2]}=0\), and the
whole homogeneous clean error vanishes.

The activity conditions on this clean plane have an exact classification.
Put

\[
 \sigma(K)=\sum_{i,j}a_{ij}K_{ij},
 \qquad \kappa_i(K)=K_{ii}.                                 \tag{6}
\]

Then \({\cal Q}_{\lambda,\mu}\) contains an active clean cap if and only
if

\[
 \sigma\big|_{{\cal Q}_{\lambda,\mu}}\ne0                  \tag{7}
\]

and neither \(\lambda\) nor \(\mu\) is proportional to a fixed
coordinate vector \(e_i\), for any \(i\in\{0,1,2\}\).  Equivalently,
absence of an active clean cap in (4)—and, in particular, absence of any
active clean cap—forces one of the following exact gates:

\[
 \boxed{
 \begin{array}{ll}
 \text{scalar gate:}&
 a=\lambda x^{\mathsf T}+y\mu^{\mathsf T}
       \text{ for some }x,y\in\mathbb C^3;\\[2mm]
 \text{coordinate gate:}&
 \lambda\parallel e_i\text{ or }\mu\parallel e_i
       \text{ for some fixed label }i.
 \end{array}}                                               \tag{8}
\]

Thus the maximal \(b=3\), rank-\((1,1)\) shore is generically finished
before any cofactor collision or one-bright jet is needed.  What remains is
not an arbitrary dark shore: it is either the five-dimensional
direct-scalar annihilator condition (the first line of (8)) or a literal
fixed-row/fixed-column endpoint (the second line).

For the maximal \(b=3\) branch, the note does **not** prove that the two
gates in (8) are impossible.  In the scalar gate, all clean caps in (4)
have zero direct scalar and are therefore inactive.  The complete rows
then give the additional linear packet

\[
   (p_B^{\mathsf T}Ks_B)q^{[h-1]}
      =\sum_iK_{ii}X_i
      \qquad(K\in{\cal Q}_{\lambda,\mu}),                  \tag{9}
\]

which must be coupled to the one-bright cofactor jet.  Equation (9), or a
fixed coordinate endpoint in (8), is the exact downstream target.

## 2. Physical cap contraction and clean error

For any matrix \(K=(K_{ij})\), contract (1) to obtain

\[
 \sigma(K)q^{[h]}+r(K)q^{[h-1]}
       =\sum_i\kappa_i(K)X_i,                               \tag{10}
\]

where

\[
 r(K)=\sum_{i,j}K_{ij}p_i s_j.                              \tag{11}
\]

The denominator-cleared canonical clean error is

\[
 {\cal E}(K)=\sum_{j=2}^{h}
       \sigma(K)^{h-j}q^{[h-j]}r(K)^{[j]}.                  \tag{12}
\]

This is the exact error in the clean-pair descent theorem.  The cap is
active precisely when

\[
       \sigma(K)K_{00}K_{11}K_{22}\ne0.                    \tag{13}
\]

No basis change in either label space is allowed in (13).

## 3. The double-annihilator plane is clean

Write

\[
 p_i=\lambda_iU+p_i^B,
 \qquad s_j=\mu_jV+s_j^B.                                  \tag{14}
\]

Expanding (11) gives

\[
\begin{aligned}
 r(K)={}&(\lambda^{\mathsf T}K\mu)UV
     +U\sum_j(\lambda^{\mathsf T}K)_j s_j^B\\
 &+V\sum_i(K\mu)_i p_i^B
     +\sum_{i,j}K_{ij}p_i^Bs_j^B.                           \tag{15}
\end{aligned}
\]

For \(K\in{\cal Q}_{\lambda,\mu}\), the first three terms vanish
literally, proving (5).  Every monomial of the last term uses two distinct
sites of \(B\).  Two such monomials cannot be disjoint when \(|B|\leq3\),
so

\[
                         r(K)^{[2]}=0.                       \tag{16}
\]

Every summand of (12) contains \(r(K)^{[j]}\) with \(j\geq2\).
Consequently

\[
                 \boxed{{\cal E}(K)=0
                    \quad(K\in{\cal Q}_{\lambda,\mu}).}   \tag{17}
\]

The dimension assertion is equally literal.  The rank-one matrices

\[
                 xy^{\mathsf T},qquad
 x\in\ker\lambda^{\mathsf T},\quad
 y\in\ker\mu^{\mathsf T},                                  \tag{18}
\]

span (4), and identify it with the tensor product of two two-dimensional
spaces.  Hence

\[
                    \dim{\cal Q}_{\lambda,\mu}=4.           \tag{19}
\]

## 4. Exact diagonal activity gates

Fix a label \(i\).  On a rank-one generator (18),

\[
                    \kappa_i(xy^{\mathsf T})=x_i y_i.        \tag{20}
\]

There exists \(x\in\ker\lambda^{\mathsf T}\) with \(x_i\ne0\) if
and only if \(\lambda\not\parallel e_i\).  Indeed, failure means that
the coordinate functional \(x\mapsto x_i\) vanishes on the hyperplane
\(\ker\lambda^{\mathsf T}\), hence is proportional to
\(\lambda^{\mathsf T}\).  The same argument gives a
\(y\in\ker\mu^{\mathsf T}\) with \(y_i\ne0\) if and only if
\(\mu\not\parallel e_i\).

It follows that

\[
 \boxed{
 \kappa_i\big|_{{\cal Q}_{\lambda,\mu}}=0
 \quad\Longleftrightarrow\quad
 \lambda\parallel e_i\text{ or }\mu\parallel e_i.}       \tag{21}
\]

This conclusion is in the original fixed target coordinates.  It is not a
normal-form statement obtained by rotating \(\lambda\) or \(\mu\).

## 5. Exact direct-scalar gate

Use the bilinear matrix pairing

\[
                       \langle a,K\rangle
                          =\sum_{i,j}a_{ij}K_{ij}.            \tag{22}
\]

The annihilator of the tensor product in (18) is

\[
 {\cal Q}_{\lambda,\mu}^{\perp}
   =(\mathbb C\lambda)\otimes\mathbb C^3
      +\mathbb C^3\otimes(\mathbb C\mu).                   \tag{23}
\]

One inclusion is immediate: if
\(a=\lambda x^{\mathsf T}+y\mu^{\mathsf T}\), then for every
\(K\in{\cal Q}_{\lambda,\mu}\),

\[
 \langle a,K\rangle
 =x^{\mathsf T}(\lambda^{\mathsf T}K)^{\mathsf T}
       +y^{\mathsf T}K\mu=0.                               \tag{24}
\]

The space on the right of (23) has dimension \(3+3-1=5\), while the
annihilator of the four-dimensional space (4) also has dimension five.
Thus equality holds, and

\[
 \boxed{
 \sigma\big|_{{\cal Q}_{\lambda,\mu}}=0
 \quad\Longleftrightarrow\quad
 a=\lambda x^{\mathsf T}+y\mu^{\mathsf T}
 \text{ for some }x,y.}                                    \tag{25}
\]

Endpoint order is retained in (23)--(25); transposition is not being
silently imposed.

## 6. Finite-hyperplane completion

The four activity factors

\[
       \sigma\big|_{\cal Q},\quad
       \kappa_0\big|_{\cal Q},\quad
       \kappa_1\big|_{\cal Q},\quad
       \kappa_2\big|_{\cal Q}                             \tag{26}
\]

are linear functionals on the four-dimensional vector space \({\cal Q}\).
Over \(\mathbb C\), a finite union of proper linear hyperplanes cannot
cover \({\cal Q}\).  Therefore a \(K\in{\cal Q}\) makes all four
factors nonzero if and only if none of the four functionals in (26) is
identically zero.

Equations (21) and (25) now prove the equivalence (7)--(8).  By (17), the
resulting active member is automatically clean, and the exact cap descent
applies.

## 7. Remaining packet on the scalar gate

For the rest of this section, assume the maximal shore
\(|B|=3\).  If \(|B|\leq2\), the scalar gate with no coordinate gate is
already impossible: the three nonzero diagonal functionals admit a common
\(K\in{\cal Q}\) with \(K_{00}K_{11}K_{22}\ne0\).  For \(|B|\leq1\),
the quadratic \(r(K)\) is zero, contradicting the independent nonzero
targets in (9).  For \(|B|=2\), equation (9) equates a tensor of Schmidt
rank at most one across \(B\mid A\) with a tensor of rank three.

Suppose the first line of (8) holds while no coordinate gate holds.  Then
every diagonal functional on \({\cal Q}\) is nonzero, but
\(\sigma(K)=0\) for every \(K\in{\cal Q}\).  Contracting the physical row
(10) gives exactly (9).

The right side of (9) can carry three independent constant-colour tensors.
Unlike the two-site-complement clean pencil, support alone does not force
the left side to have Schmidt rank at most one across \(B\mid A\): an edge
of \(r(K)\) occupies two of the three sites of \(B\), leaving the third
site available to the \((h-1)\)-st power of \(q\).  Thus the scalar gate
is not removed by the two-site flattening argument.

This identifies the correct next input.  One must combine the linear family
(9) with either

1. the one-bright four-site equations obtained by freeing one shore site;
   or
2. the four adjacent response catalecticant columns of the rank-\((1,1)\)
   shore.

The coordinate gate has a similarly literal meaning: one endpoint on the
large shore is supported in one fixed physical row or column.  Neither gate
requires a support census, and neither is declared closed here.
