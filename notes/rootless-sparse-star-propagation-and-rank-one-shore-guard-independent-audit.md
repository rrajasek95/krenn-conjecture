# Independent audit: sparse-star propagation and the rank-one-shore guard

## 1. Verdict

**PASS.**  The type-2 pigeonhole, the type-3 response normal form, every
divided-power coefficient, and the explicit rational guard in
[the primary note](rootless-sparse-star-propagation-and-rank-one-shore-guard.md)
are correct.

The guard has exactly the stated scope.  It is one exact unary
\(K\)-contracted row with scalar-zero direct term; it is not the canonical
off-diagonal curvature cap and is not a solution of the nine physical pair
rows.  The primary note does not claim otherwise.

No mathematical repair is required.  Two optional clarifications would
make the bookkeeping completely explicit:

1. if the new first-star basis is \(\widetilde p=Bp\), the absorbed second
   triple is \(t=B^{-T}Ks\);
2. in the guard, \(K^{-1}=K\), so the original second star is
   \(s_0=t_0,\ s_1=t_2,\ s_2=t_1\).

The independent exact reconstruction in Sections 4--5 also identifies two
individual pair rows that fail.  Thus “does not satisfy the other eight
pair rows” can, if desired, be sharpened to a displayed certificate rather
than read merely as a statement that the remaining system is not imposed.

## 2. Type 2: the matching pigeonhole is uniform

Let \(W\) have \(2h\) sites and suppose the complete support of the
\(p\)-star is contained in \(S\subseteq W\).  Expand

\[
                       r=\sum_{i,j}K_{ij}p_i s_j.      \tag{A1}
\]

Every scalar decorated summand of an edge of \(r\) has the form

\[
 K_{ij}\,p_{i,x}s_{j,y}
 \quad\text{or}\quad
 K_{ij}\,p_{i,y}s_{j,x},                              \tag{A2}
\]

and its designated \(p\)-site belongs to \(S\).  A term in \(r^{[h]}\)
consists of \(h\) such oriented edge summands.  For the product to survive
the site-square-zero relations, all \(h\) designated \(p\)-sites must be
distinct.  Therefore

\[
                         |S|\leq h-1
          \quad\Longrightarrow\quad r^{[h]}=0.         \tag{A3}
\]

This is termwise zero before any aggregate cancellation, so arbitrary
complex coefficients and repeated decorated sources cause no problem.
The same proof applies after interchanging \(p\) and \(s\).  At the
six-site boundary \(h=3\), support on at most two sites is consequently
incompatible with the rootless condition \(r^{[3]}\ne0\).

The proof does not use invertibility of \(K\), the response equation, or
injectivity of the opposite star.  The uniform strengthening in the
primary note is therefore exact.

## 3. Type 3: basis normal form and divided powers

Let

\[
 P_{\ne x}:\mathbb C^3\longrightarrow
       \bigoplus_{y\ne x}V_y                              \tag{A4}
\]

be the restriction of the first endpoint star, and suppose
\(\operatorname {rank}P_{\ne x}\leq1\).  Its kernel has dimension at least
two.  Choose a basis whose last two vectors lie in that kernel.  In this
basis,

\[
             \widetilde p_0=L+\ell_x,\qquad
             \widetilde p_1,\widetilde p_2\in V_x,     \tag{A5}
\]

with \(L\) supported off \(x\).  This remains valid in rank zero, with
\(L=0\).

For complete transpose bookkeeping, write the original triples as column
vectors and let \(\widetilde p=Bp\).  Then

\[
\begin{aligned}
 r=p^TKs
   &=\widetilde p^{\,T}B^{-T}Ks
     =\sum_i\widetilde p_i t_i,\\
 t&=B^{-T}Ks.                                         \tag{A6}
\end{aligned}
\]

Both \(B\) and \(K\) are invertible.  Thus this absorption preserves the
rank and injectivity of the second triple.  It is a normalization of the
response \(r\); if one later uses the individual physical pair rows, their
indices and targets must of course be transported through the same basis
change.  The primary note uses the normal form only for \(r\).

Write \(t_0=M+m_x\), with \(M\) supported off \(x\).  Expanding the first
summand in (A6) gives

\[
 (L+\ell_x)(M+m_x)
   =LM+Lm_x+\ell_xM,                                  \tag{A7}
\]

because \(\ell_xm_x=0\).  Every term in
\(\widetilde p_1t_1+\widetilde p_2t_2\) is either zero at \(x\) or is an
edge incident with \(x\).  Consequently

\[
                         r=Q+E_x,\qquad Q=LM,          \tag{A8}
\]

where \(Q\) is supported on \(W\setminus\{x\}\) and every edge of \(E_x\)
contains \(x\).

Two edges from \(E_x\) collide at \(x\), so

\[
                         E_x^{[2]}=0
                         \quad\text{and hence}\quad
                         E_x^{[k]}=0\quad(k\geq2).     \tag{A9}
\]

At the first boundary \(W\setminus\{x\}\) has five sites.  Three disjoint
quadratic edges require six sites, and hence

\[
                              Q^{[3]}=0.               \tag{A10}
\]

The divided-power binomial identity has no missing numerical factors:

\[
\begin{aligned}
 (Q+E_x)^{[3]}
 &=Q^{[3]}+E_xQ^{[2]}+E_x^{[2]}Q+E_x^{[3]}\\
 &=E_xQ^{[2]}.                                        \tag{A11}
\end{aligned}
\]

Indeed, after replacing \(Z^{[k]}\) by \(Z^k/k!\), the four terms have
ordinary coefficients \(1/6,1/2,1/2,1/6\), exactly as in the expansion of
\((Q+E_x)^3/6\).

Thus \(r^{[3]}\ne0\) forces \(E_x\ne0\) and \(Q^{[2]}\ne0\), and every
surviving top matching has exactly one exceptional edge and two
\(LM\)-edges.  These are precisely the conclusions asserted in the
primary note.

The reason (A10), and hence the displayed cubic formula, is specific to
six residual sites is also correct.  With six sites available off \(x\),
take

\[
 L=u_1+u_2+u_3,\qquad M=v_1+v_2+v_3                     \tag{A12}
\]

on two disjoint three-sets.  Then \(Q=LM\) is the complete bipartite
quadratic and

\[
                         Q^{[3]}=3!\,
             u_1u_2u_3v_1v_2v_3\ne0.                 \tag{A13}
\]

So one cannot reuse (A11) for a cubic on a larger residual shore merely
from decomposability.  There is a separate uniform top-power identity
\(r^{[h]}=E_xQ^{[h-1]}\) on \(2h\) residual sites, but the primary note
neither needs nor claims it.

## 4. Exact reconstruction of the rational guard

Use the ordered row convention

\[
                 t_i=\sum_jK_{ij}s_j,\qquad
                 r=\sum_{i,j}K_{ij}p_i s_j
                   =\sum_i p_it_i.                   \tag{A14}
\]

The displayed cap matrix is

\[
 K=\begin{pmatrix}
 1&0&0\\
 0&0&1\\
 0&1&0
 \end{pmatrix}.                                      \tag{A15}
\]

It is the transposition of indices \(1,2\), so

\[
 K^{-1}=K,\qquad \det K=-1,\qquad
 \operatorname {diag}K=(1,0,0).                      \tag{A16}
\]

Given the displayed transformed rows

\[
\begin{aligned}
 t_0&=z_{30}+z_{40},&
 t_1&=\tfrac16z_{50},&
 t_2&=z_{02},
\end{aligned}                                        \tag{A17}
\]

the original second rows are

\[
 s=K^{-1}t=Kt,\qquad
 s_0=z_{30}+z_{40},\quad
 s_1=z_{02},\quad
 s_2=\tfrac16z_{50}.                                 \tag{A18}
\]

Applying \(K\) to (A18) returns (A17), so the index ordering in the
primary note is correct.

Both endpoint maps are injective.  For the first triple,

\[
 p_0=z_{10}+z_{20},\qquad p_1=z_{00},\qquad p_2=z_{01}, \tag{A19}
\]

the first vector has support away from site \(0\), while \(p_1,p_2\) are
independent colour axes at site \(0\).  For (A18), the three vectors have,
respectively, support on sites \(\{3,4\}\), site \(0\), and site \(5\).
No nontrivial linear relation is possible.  Restricting (A19) away from
site \(0\) leaves exactly the one-dimensional span of \(p_0\), as claimed.

Let \(a=(a_{ij})\) be the direct block.  The direct scalar in this cap is

\[
                         \sigma(K)=\sum_{i,j}K_{ij}a_{ij}.       \tag{A20}
\]

Taking \(a=0\), or any block in the hyperplane \(\sigma(K)=0\), makes the
row scalar-zero.  The target contraction is

\[
                         T(K)=\sum_iK_{ii}X_i=X_0.     \tag{A21}
\]

This is a valid scalar-zero physical cap row.  It is deliberately not a
canonical off-diagonal curvature cap: the latter has three equal nonzero
diagonal entries and comes from a direct block with a selected nonzero
off-diagonal entry.

Using (A14), the response is

\[
\begin{aligned}
 r
 &=p_0t_0+p_1t_1+p_2t_2\\
 &=(z_{10}+z_{20})(z_{30}+z_{40})
      +\tfrac16z_{00}z_{50}+z_{01}z_{02}.             \tag{A22}
\end{aligned}
\]

The last product has two factors at site \(0\), so it is zero.  Therefore,
with

\[
 Q=(z_{10}+z_{20})(z_{30}+z_{40}),\qquad
 E=\tfrac16z_{00}z_{50},                              \tag{A23}
\]

one has exactly

\[
                              r=q=Q+E.                 \tag{A24}
\]

No endpoint order or response summand has been omitted.

## 5. Independent coefficient check

The four edges of \(Q\) are

\[
                         13,\ 14,\ 23,\ 24             \tag{A25}
\]

with unit coefficient, all in colour zero.  There are exactly two perfect
matchings of sites \(\{1,2,3,4\}\) using these edges:

\[
                         \{13,24\},\qquad\{14,23\}.    \tag{A26}
\]

Consequently

\[
                  Q^{[2]}
                    =2z_{10}z_{20}z_{30}z_{40}.       \tag{A27}
\]

The only way to cover all six sites in \(r^{[3]}\) is to use the edge
\(05\) from \(E\) and one of the two matchings in (A26).  Thus

\[
\begin{aligned}
 r^{[3]}
   &=EQ^{[2]}\\
   &=\tfrac16\cdot2\,
       z_{00}z_{10}z_{20}z_{30}z_{40}z_{50}
     =\tfrac13X_0.                                    \tag{A28}
\end{aligned}
\]

The standard divided-power multiplication law gives

\[
                 r\,r^{[2]}=\binom31r^{[3]}=3r^{[3]}. \tag{A29}
\]

Since \(q=r\), equations (A21) and (A28)--(A29) give

\[
                         rq^{[2]}=X_0=T(K),            \tag{A30}
\]

with no other colour word.  This independently verifies every numerical
coefficient in the guard.

For a direct check that the complete pair system is absent, keep the
choice \(a=0\).  Since

\[
                       q^{[2]}=Q^{[2]}+QE,             \tag{A31}
\]

the \((0,0)\) pair response is

\[
 p_0s_0q^{[2]}=Qq^{[2]}=\tfrac23X_0,                  \tag{A32}
\]

rather than its required target \(X_0\).  The off-diagonal \((1,2)\) row
is

\[
 p_1s_2q^{[2]}=Eq^{[2]}=\tfrac13X_0,                  \tag{A33}
\]

rather than zero.  Their sum, with \(K_{00}=K_{12}=1\), is \(X_0\);
the remaining nonzero cap entry \(K_{21}=1\) multiplies
\(p_2s_1=p_2t_2=0\).  This reconstructs exactly how the contracted row
works while the physical nine-row system fails.

An independent exact square-free-algebra calculation over
\(\mathbb Q\) reproduced (A18), (A22), (A27)--(A30), and
(A32)--(A33).

## 6. Scope of the remaining claim

The primary note proves two statements:

1. type 2 is impossible in the rootless scalar-zero packet, uniformly by
   (A3);
2. at the six-site boundary, type 3 has the necessary form
   \(r^{[3]}=E_x(LM)^{[2]}\).

It does **not** claim that the type-3 form is contradictory.  Its remaining
positive target explicitly calls for information absent from the guard:
the full ternary response

\[
                 rq^{[2]}=-\alpha(X_0+X_1+X_2),       \tag{A34}
\]

the other eight pair rows, or a compatible overlapping canonical chart.
The guard has only the unary target \(X_0\), and (A32)--(A33) show exactly
why its contracted cancellation cannot be promoted to the complete pair
system.

Accordingly the final statement is correctly presented as an open bounded
coupling problem, not as a closure of type 3 or of the conjecture.  No
support enumeration, positivity, or inference from a cancelled aggregate
is hidden in the proved part.
