# Closed neighborhoods are isotropic and monochromatic degrees are strictly bounded

**Status.** New all-order research proof, 2026-09-20, by `/root`.
The degree argument received a preliminary independent check from
`/root/scalar_pencil_coupling`; a complete audit of this frozen text is
pending. Nothing here constitutes formal certification of the conjecture.

## 1. Full source and reviewed inputs

Let V have n=2m>=4 vertices, with local spaces exactly C^3 and fixed
bases a,b,c. Work in the commutative physical-site-square-zero algebra.
An ordinary complex quadratic A satisfies the WHOLE equality

    A^[m] = sum_(h=a,b,c) tau_h h^V,   tau_a tau_b tau_c != 0,   (1)

where Q^[j]=Q^j/j! and Q^[0]=1. Three reviewed results are inputs.

1. [Global diagonality and actual cofactor inversion](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-GLOBAL-EDGE-MONOCHROMATICITY-AND-COFACTOR-INVERSE.md)
   makes every edge diagonal in these ORIGINAL bases. Define the
   symmetric zero-diagonal scalar adjacency M_h by its h-h cells,
   and the symmetric matrix C_h by

       C_h[u,v]=haf(M_h[V without {u,v}])  for u!=v,
       C_h[u,u]=0.

   Then haf(M_h)=tau_h and M_h C_h=tau_h I. In particular both
   scalar matrices are invertible. These are actual cofactors of A.

2. [Higher odd response vanishing](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md)
   applies at every root p. Write R_p=A restricted off p and
   X_h=sum_(v!=p) M_h[p,v] h_v. The rows X_a,X_b,X_c have the three
   original pure responses, and span a full diagonal-response frame.
   For 1<=r<=m-1 and any 2r+1 rows from their span, their product
   with R_p^[m-1-r] has zero projection to EVERY binary palette.
   This includes its pure coefficients and all two-color mixed words.
   It does not make its all-three-color coefficients vanish.

3. [Balanced binary cofactor nonvanishing](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-BIPARTITE-TWO-ACTIVE-RECTANGULAR-COFACTOR-NONVANISHING.md)
   says that an ACTUAL balanced bipartite quadratic B on r+r sites,
   with whole top sigma_b b^V+sigma_c c^V and both amplitudes
   nonzero, has a nonzero whole b/c-projected cofactor after deleting
   EVERY opposite-shore pair. For r>=2 this is its balanced-source
   corollary; r=1 is the empty unit. It does not assert that either
   individual pure coefficient of that cofactor is nonzero.

All hafnians include the empty value one and the odd-order value zero.
Graph G_h below records only the nonzero h-h cells of M_h. Its degree
is a single-color degree, not the physical union degree of A.

## 2. Closed neighborhoods are totally isotropic for both other cofactors

Fix distinct colors h,k, a vertex p, and distinct u,v outside p.
The binary projection of X_h X_h X_k R_p^[m-2] vanishes by input 2.
Extract the word with h at u,v and k at every other site of V\{p}.
Global diagonality forces both X_h factors to occupy u and v and
the X_k factor to occupy a site t outside p,u,v. The exact coefficient is

    0 = 2 M_h[p,u] M_h[p,v]
          sum_(t outside {p,u,v}) M_k[p,t]
                    haf(M_k[V without {p,u,v,t}])
      = 2 M_h[p,u] M_h[p,v] C_k[u,v].                         (2)

The final equality expands the actual cofactor C_k[u,v] at its
retained vertex p. The factor two is from the two ordered X_h rows;
the residual divided power counts every remaining matching once.
At n=4 its four-deletion hafnian is one, and the formula still holds.

Separately, the original whole mixed word with h only at p,u and
k at every other vertex gives

    M_h[p,u] C_k[p,u] = 0.                                  (3)

No termwise matching exclusion has been used. Both (2) and (3) concern
whole coefficients, with every cancellation inside C_k retained.

Let S={p} union N_(G_h)(p) be the closed h-neighborhood. Equations
(2), (3), and the defined zero diagonal of C_k give

    C_k[S,S]=0           for BOTH colors k!=h.               (4)

Thus the coordinate subspace C^S is totally isotropic for each of two
nondegenerate symmetric bilinear forms. Since the orthogonal
complement of an s-dimensional subspace of a nondegenerate space of
dimension 2m has dimension 2m-s, its containment in that complement
implies 2s<=2m. In particular

    deg_(G_h)(p) <= m-1.                                    (5)

Equivalently, supp(C_k) excludes every pair at G_h-distance one or
two. This does not claim that C_k is nonzero on all more distant pairs.

## 3. Equality in (5) would split off a balanced binary source

Suppose |S|=m and let T=V\S, also of size m. In the ordering S,T,
the invertible cofactor matrix for either k!=h has block form

    C_k = [[0,Z_k],[Z_k^T,H_k]].                             (6)

The square matrix Z_k is invertible: a vector in ker(Z_k^T) would
give a null vector of C_k supported in S. Its block inverse has
zero T,T block, as direct multiplication shows. Consequently

    M_k[T,T]=0                 for BOTH k!=h,               (7)

because M_k=tau_k C_k^(-1).

Denote the other two colors by b,c and project (1) to their local
planes. By (7), all T vertices can be occupied only by edges to S.
Since the shores have equal size, every matching uses only crossing
edges. Internal S edges never contribute. Therefore the crossing-only
quadratic B obtained from these b-b and c-c cells has WHOLE top

    B^[m]=tau_b b^V+tau_c c^V.                              (8)

Input 3 gives, for EVERY s in S and t in T,

    F_st=(B restricted off {s,t})^[m-1] != 0.               (9)

B already uses only colors b,c, so this is precisely its active-plane
projection. It is also the b/c projection of the full cofactor of A
off {s,t}: after this deletion the shores still have equal sizes,
T has no internal b/c edge, and every matching must cross.

Now slice (1) to h at s,t and to b/c at all other vertices. Since
only two vertices carry h and A is diagonal, the exact whole slice is

    0 = M_h[s,t] F_st.                                     (10)

Its right factor is a nonzero tensor by (9), so M_h[s,t]=0. This holds
for every crossing pair, proving

    M_h[S,T]=0.                                           (11)

Unlike (3), this conclusion uses a whole binary cofactor rather than
one possibly vanishing pure coefficient.

## 4. Higher pure vanishing excludes equality except at four sites

Equation (11) factorizes the nonzero pure h top:

    tau_h=haf(M_h[S]) haf(M_h[T]) != 0.                    (12)

If m is odd, both shores have odd size and (12) is impossible.
If m is even and n>=6, necessarily m>=4. By the definition of S,
the row X_h at p has exactly m-1 nonzero components, at S\{p},
and no components at T. Use input 2 with

    2r+1=m-1,      r=(m-2)/2>=1,
    m-1-r=m/2.

It asserts that the pure h coefficient of X_h^(m-1) R_p^[m/2]
is zero. But that coefficient is exactly

    (m-1)! (product_(u in S\{p}) M_h[p,u]) haf(M_h[T]),     (13)

which is nonzero by the definition of the neighborhood and (12).
All row factors fill S\{p}; the remaining sites are exactly T, so no
other placement or matching can contribute to (13). This contradiction
excludes equality in (5) at every n>=6.

**Theorem.** Every full ternary source on n=2m>=6 obeys

    1 <= deg_(G_h)(p) <= m-2

for every vertex p and every color h. The lower bound follows because
a zero row of M_h would make its pure hafnian zero. The upper bound
is a necessary condition and by itself is not a nonexistence theorem.
At n=10 it bounds every single-color degree by three. It does not
bound the physical union degree by three.

At n=4, the allowed source consisting of the three distinct perfect
matchings of K4 has degree one in each color. It attains m-1. The
last argument cannot be used there, since m-1=1 is the original row
response, not a higher odd response. Thus the exception is explicit.

## 5. A precise complementary-rank consequence

For any closed h-neighborhood S, put s=|S| and T=V\S. Equation (4)
and invertibility determine the rank of the OTHER color matrices:

    rank M_k[T,T]=n-2s,       k!=h.                        (14)

Here is a direct kernel proof, without an extra matrix-theory input.
For any invertible M and C=tau M^(-1), the map

    ker(M[T,T]) -> ker(C[S,S]),       x -> M[S,T]x

is an isomorphism up to the nonzero scalar tau. In fact M(0,x)=(y,0)
implies C(y,0)=tau(0,x). The map is injective by invertibility of M.
Conversely if C(y,0)=(0,z), then M(0,z)=tau(y,0), recovering a
kernel vector z. Thus the two nullities agree. Since C[S,S]=0,
its nullity is s, proving (14).

At the allowed extremal degree m-2, one has s=m-1 and |T|=m+1,
so BOTH other-color blocks on T have rank exactly two. Any complex
symmetric zero-diagonal rank-two matrix is a weighted complete
bipartite graph with factorized nonzero weights, plus isolated
vertices. To see this, write it as Y J Y^T with Y of column rank two
and J a nondegenerate symmetric 2-by-2 form. Over C, the isotropic
cone of J is the union of two lines. Zero diagonal puts each nonzero
row of Y on one of these lines. Pairings within a line are zero,
between the lines are nonzero and factorize; zero rows are isolated.
Both lines occur because Y has rank two.

At n=10 a cubic h vertex therefore leaves, on its six-vertex
complementary set T, two such rank-two bipartite scalar blocks.
Their bipartitions need not agree, and this does not show that the
whole physical graph is bipartite. Their coupling to S remains open.
