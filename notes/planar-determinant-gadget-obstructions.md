# Planar determinant gadgets: two exact obstructions

This note audits the most economical FKT counterexample route.  Let $G$
be a planar bipartite graph with shores $L,R$, $|L|=|R|=m$, and let

\[
             B_e:\{0,1,2\}^2\longrightarrow \mathbb C
\]

be an arbitrary color table on every edge.  For a coloring $x$ of all
vertices, put

\[
 Z_G(x)=\sum_{M\in {\rm PM}(G)}\prod_{e=uv\in M}B_e(x_u,x_v).       \tag{1}
\]

A Kasteleyn signing $(\kappa_e)$ of the bipartite adjacency matrix
makes

\[
 \det\bigl(\kappa_{ij}B_{ij}(x_i,x_j)\bigr)_{i\in L,j\in R}
                         =\epsilon Z_G(x),                         \tag{2}
\]

where $\epsilon\in\{\pm1\}$ is independent of $x$.  Thus a signed
determinant construction is exactly an unsigned dimer construction; the
signing does not provide color-dependent cancellation.  The two results
below rule out the cycle with completely arbitrary tables and the natural
four-parameter ladder ansatz.

## 1. A cycle cannot work, even with arbitrary edge tables

**Proposition 1.**  For every $m\geq4$, arbitrary complex $3\times3$
tables on $C_{2m}$ cannot satisfy

\[
                  Z_{C_{2m}}=\Delta_{2m,3}.                       \tag{3}
\]

In particular this excludes both $C_{10}$ and $C_{12}$.  For $C_{10}$,
with the checkerboard shores in cyclic order, the all-positive signing is
already Kasteleyn: the two determinant terms have the same sign.

**Proof.**  Write the two alternating perfect matchings as $P,Q$, and
write

\[
 p_c=\prod_{e\in P}B_e(c,c),\qquad
 q_c=\prod_{e\in Q}B_e(c,c).
\]

Equation (3) gives $p_c+q_c=1$, so for each of the three colors at least
one of $p_c,q_c$ is nonzero.  By the pigeonhole principle, two colors,
called $0,1$, have a common nonzero choice; interchange $P,Q$ if needed
so that $p_0p_1\ne0$.

Contract every edge of $P$ to one cyclic site.  For a binary cyclic word
$s=(s_0,\ldots,s_{m-1})$, color both endpoints of the $i$-th $P$-edge
by $s_i$.  Its $P$-monomial $p(s)$ is nonzero.  Let $q(s)$ be the
$Q$-monomial and set

\[
 R(s)=\frac{q(s)}{p(s)}
     =\prod_{i\in\mathbb Z/m\mathbb Z}r_i(s_i,s_{i+1}).             \tag{4}
\]

The local factors $r_i$ may be zero.  Every nonconstant word is a mixed
physical coloring, hence (3) says

\[
                              R(s)=-1.                              \tag{5}
\]

Choose two nonadjacent cyclic sites $i,j$, which is possible for
$m\geq4$.  Locality of the product (4) gives the exact rectangle identity

\[
 R(0^m)R(0^m+e_i+e_j)=R(0^m+e_i)R(0^m+e_j).                       \tag{6}
\]

The three nonconstant values in (6) are all $-1$, so
$R(0^m)=-1$.  But then the all-zero coefficient is

\[
              p(0^m)+q(0^m)=p(0^m)(1+R(0^m))=0,
\]

contrary to (3).  $\square$

This is stronger than failure of a translationally invariant cycle ansatz:
edge positions, orientations, zeros, and all nine entries of every table
were arbitrary.

## 2. Every open $2\times m$ ladder is impossible

Let the ladder have vertices $t_i,b_i$, $0\leq i<5$, with five rungs
and the eight horizontal rail edges.  Give every top rail edge sign $-1$
and every other edge sign $+1$.  Every bounded square then has sign
product $-1$, and direct determinant parity gives the same total sign for
all eight perfect matchings.

**Proposition 2.**  For every $m\geq3$, arbitrary complex $3\times3$ edge
tables on the open $2\times m$ ladder cannot realize
$\Delta_{2m,3}$.

**Proof.**  Group the two physical colors in column $i$ into a state
$s_i\in D=\{0,1,2\}^2$, and write $d_c=(c,c)$.  At the first column, a
perfect matching either uses the first rung or uses both rail edges from
column one to column two.  The complete matching tensor therefore has the
exact decomposition

\[
 F(s_1,s_2,z)=R(s_1)A(s_2,z)+W(s_1,s_2)C(z),                \tag{L1}
\]

where $z=(s_3,\ldots,s_m)$, $R$ is the first-rung table, $A$ and $C$ are
the matching tensors of the suffix ladders beginning in columns two and
three, and

\[
 W((a,b),(c,d))=B_{t_1t_2}(a,c)B_{b_1b_2}(b,d).             \tag{L2}
\]

No property of the factorization in (L2) will be needed.

First, $R$ is not the zero vector.  Otherwise (L1) is a product across the
partition consisting of the first two columns and the remaining columns,
so that flattening has rank at most one.  The corresponding flattening of
$\Delta_{2m,3}$ has rank three.

Suppose that $z$ is a nonconstant physical coloring of columns three
through $m$.  The target coefficient is then zero for every $s_1,s_2$, so
(L1), viewed as a $9\times9$ matrix in those two states, says

\[
                       R A_z^T+C(z)W=0.                    \tag{L3}
\]

If $C(z)\ne0$, equation (L3) forces $\operatorname{rank}(W)\leq1$.
But then both summands in (L1) have rank at most one across the partition
`first column | remaining columns`, while the target again has rank three.
This is impossible.  Hence $C(z)=0$ for every nonconstant $z$.

Set

\[
 \lambda_c=C(d_c,\ldots,d_c),\qquad
 A_c(s)=A(s,d_c,\ldots,d_c),
\]

and let $E_c=e_{d_c}e_{d_c}^T$ be the $9\times9$ matrix with its sole
nonzero entry at $(d_c,d_c)$.  Applying (L1) to each of the three constant
suffixes gives

\[
                         E_c=R A_c^T+\lambda_cW,
                         \qquad c=0,1,2.                   \tag{L4}
\]

Two of the scalars, say $\lambda_c,\lambda_d$, cannot both be nonzero:
eliminating $W$ from their equations gives

\[
 \lambda_dE_c-\lambda_cE_d
       =R(\lambda_dA_c-\lambda_cA_d)^T,                    \tag{L5}
\]

whose left side has rank two and whose right side has rank at most one.
Thus at most one $\lambda_c$ is nonzero.  At least two are consequently
zero.  For each zero scalar, (L4) says $E_c=RA_c^T$, forcing the fixed
column space $\mathbb C R$ to equal $\mathbb C e_{d_c}$.  Two distinct
colors force two distinct one-dimensional spaces, the final contradiction.
$\square$

The proof is a complete transfer-matrix classification for this topology;
it permits position-dependent, asymmetric, singular, and dense color
tables.  A weaker but sometimes portable consequence comes from any
interior column cut.  Matchings use either neither crossing rail edge or
both, so if those two tables are $A_t,A_b$, the output flattening rank is at
most

\[
                         \operatorname{rank}(A_t)
                         \operatorname{rank}(A_b)+1.               \tag{7}
\]

Every nontrivial flattening of $\Delta_{10,3}$ has rank three.  Thus at
every interior ladder cut the crossing-rank product must be at least two.
In particular, two rank-one crossing tables already give an independent
rank obstruction.

## 3. Independent four-parameter ladder audit

Consider the position-independent, color-permutation-symmetric ansatz

\[
 B_{t_ib_i}(a,b)=\begin{cases}V&a=b,\\X&a\ne b,\end{cases}
 \qquad
 B_{u_iu_{i+1}}(a,b)=\begin{cases}H&a=b,\\Y&a\ne b\end{cases}           \tag{9}
\]

on both rails $u=t,b$.  No reality or nonvanishing assumption is made on
$V,X,H,Y\in\mathbb C$.

**Proposition 3.**  The ansatz (9) cannot realize
$\Delta_{10,3}$.

**Proof.**  Domino tilings of a $2\times k$ prefix obey

\[
 F_k=r_kF_{k-1}+h^t_{k-1,k}h^b_{k-1,k}F_{k-2},\qquad F_0=1.       \tag{10}
\]

For the constant coloring, the eight tilings give

\[
 C=V^5+4V^3H^2+3VH^4
   =V(V^2+H^2)(V^2+3H^2).                                       \tag{11}
\]

The target requires $C=1$, in particular $C\ne0$.  Four mixed
colorings, written as `top | bottom`, have coefficients

\[
\begin{array}{c|l}
00000\mid11111 &X(X^2+H^2)(X^2+3H^2),\\
01010\mid02020 &V(VX+Y^2)(VX+3Y^2),\\
01010\mid01010 &V(V^2+Y^2)(V^2+3Y^2),\\
01010\mid10101 &X(X^2+Y^2)(X^2+3Y^2).
\end{array}                                                     \tag{12}
\]

All four expressions must vanish.  From (11), $V\ne0$.  Put
$z=Y^2/V^2$.  The third equation in (12) gives

\[
                         z\in\{-1,-1/3\}.                         \tag{13}
\]

In particular $Y\ne0$.  Put $r=X/V$.  The second equation gives
$r=-z$ or $r=-3z$, so $X\ne0$, while the fourth gives
$r^2=-z$ or $r^2=-3z$.  Checking the two values in (13) leaves only

\[
                                  r=1.                             \tag{14}
\]

Thus $X=V$.  The first expression in (12) is then exactly the nonzero
constant coefficient (11), a contradiction.  $\square$

`computations/verify_planar_determinant_obstructions.py` independently
enumerates the matchings, checks the Kasteleyn determinant signs, recovers
all five polynomials in (11)--(12), and verifies the local rectangle identity
used in Proposition 1.

## 4. Relation to the higher-domain matchgate no-go theorem

Fu's theorem (arXiv:1707.00373, Theorem 1.2) says that for $n,q\geq3$
there is no full-rank $q\times2^\ell$ matrix $M$ for which
$(=_n)M^{\otimes n}$ is a standard matchgate signature.  It therefore
rules out any proposed construction that first applies one shared
holographic encoding to every color leg and then realizes the result by a
planar matchgate.

It does **not**, without an additional reduction, rule out (1) with
arbitrary edge-specific bivariate tables.  In (1), changing the color at a
vertex simultaneously changes every incident internal edge through
different tables $B_e$; this is not the deletion-bit external-leg model
of a standard matchgate and need not factor through one common matrix
$M$.  Consequently the theorem explains the failure of shared-basis
ansatzes, but it should not be cited as a proof that every planar graph in
the present problem is impossible.
