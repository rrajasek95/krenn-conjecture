# Bipartite color components: exact boundary ranks and a crown-plus-edge exclusion

**Status.** Independently audited all-order research theorem, 2026-09-20.
[Complete independent audit PASS](../unaudited-codex-diagonal-continuation-2026-09-20/BIPARTITE-COLOR-COMPONENT-BOUNDARY-AND-CROWN-EXCLUSION-AUDIT.md); the parent read
the complete frozen source and audit and accepted its stated mathematical scope.
The frozen source and audit remain unchanged in the staging folder.
The general conjecture remains open; formal certification status is unchanged.

## 1. Actual source and inputs

Let an ordinary complex ternary source on V, |V|=n=2m>=4, have whole top

    A^[m]=tau_a a^V+tau_b b^V+tau_c c^V,
    tau_a tau_b tau_c!=0.

Products are in the commutative physical-site-square-zero algebra and
Q^[j]=Q^j/j!. Use the reviewed global diagonality theorem in the original
target bases. For each color h, let M_h be its symmetric zero-diagonal
scalar adjacency, and let C_h be its ACTUAL deleted-pair hafnian matrix,
with C_h[u,u]=0 by definition. The reviewed conclusions are

    haf(M_h)=tau_h,       C_h=tau_h M_h^(-1),
    product_h haf(M_h[S_h])=0
        for every nonconstant color partition V=disjoint_union_h S_h. (1)

The additional reviewed inputs are:

- Closed h-neighborhoods are totally isotropic for C_k when k!=h.
  In particular C_k[u,v]=0 if u,v are h-adjacent or share an h neighbor.
- For any scalar M with its actual C satisfying MC=haf(M)I!=0,
  a degree-one vertex belongs to an isolated edge, and degree two is
  impossible. These lemmas do not require other colors.
- A balanced bipartite source with two nonzero pure targets has a
  nonzero whole active-plane cofactor after deleting every opposite-
  shore pair. This last input is used only in the spanning corollary.

The exact source/audit records are bound in the [accompanying freeze
receipt](../unaudited-codex-diagonal-continuation-2026-09-20/component_boundary_and_crown_exclusion_freeze_receipt.json). The global, neighborhood, and scalar-degree source texts were
read completely; their relevant arguments were reconstructed by the
present author during the preceding audits. No finite census is an input.

Write G_h for the support graph of M_h. Haf(empty)=1; odd hafnians vanish.
Every connected component of G_h has a nonzero pure h hafnian, since
haf(M_h) factors over its components and is nonzero. In particular every
component has even size, and every bipartite component has balanced shores.

## 2. Every proper union of one color's components couples to both others

Let S be a nonempty proper union of connected components of G_h and
let R=V without S. For each k!=h, both

    M_k[S,R]!=0,          C_k[S,R]!=0.                         (2)

Indeed, if M_k[S,R]=0, then its nonzero hafnian factors into nonzero
hafnians on S and R. The h hafnian on S is nonzero as well. The word
with color h on S and k on R then has the nonzero coefficient
haf(M_h[S]) haf(M_k[R]), contradicting (1).

If C_k[S,R]=0, its symmetry makes C_k block diagonal. Invertibility
then makes its inverse M_k/tau_k block diagonal too, contradicting the
first conclusion. This uses actual scalar cofactor inversion, not an
independent assignment of a second matrix.

Consequently the support graph of either other cofactor, after the
h-components are contracted to vertices, is connected. In particular,
a proper component's exterior cofactor block cannot simply be discarded.
The same cut statement holds for the other adjacency graph itself.

## 3. Common-neighbor coverage gives exact exterior ranks

Suppose S is a bipartite h-component with shores U,T, |U|=|T|=r.
Assume that every pair of distinct vertices in U shares an h neighbor,
and the same holds for every pair in T. Put R=V without S, q=|R|.
For either k!=h, neighborhood isotropy gives

    C_k[S,S] = [[0,Z_k],[Z_k^T,0]],
    Z_k[u,t]=0 whenever M_h[u,t]!=0.                         (3)

Let z_k=rank Z_k. Then

    rank M_k[R,R] = q-2(r-z_k),
    rank C_k[R,S] >= 2(r-z_k),
    q >= 2(r-z_k).                                          (4)

To check the first identity, use the following exact complementary-
nullity fact. If M is invertible and C=tau M^(-1), then

    ker(M[R,R]) -> ker(C[S,S]),     x -> M[S,R]x

is an isomorphism up to multiplication by the nonzero scalar tau.
Indeed M(0,x)=(y,0) implies C(y,0)=tau(0,x); injectivity follows
from invertibility. Conversely, C(y,0)=(0,z) implies
M(0,z)=tau(y,0), yielding the inverse up to tau. Thus the nullities
are equal. The block in (3) has rank 2z_k and nullity 2(r-z_k),
which proves the first identity in (4).

For the second, restriction of C_k[R,S] to ker(C_k[S,S]) is injective:
a vector in both kernels would be a full kernel vector of C_k supported
on S. Its domain has dimension 2(r-z_k). This proves both remaining
claims. These are ordinary scalar ranks; no rank is inferred from a
nonzero permanent or from the support of a sum of matchings.

One useful support corollary follows. Let nu be the maximum matching
size in the bipartite pattern of pairs U--T where the h cell is zero.
Since Z_k is supported in that pattern, z_k<=nu: any nonzero determinant
minor would supply a supported permutation. Consequently

    q >= 2(r-nu).                                          (5)

For an h-component that is complete bipartite, nu=0, so its exterior
must contain at least as many vertices as the component itself.
This is a necessary size bound, not an existence theorem.

When Z_k is invertible, (4) instead says M_k[R,R] is invertible
(with the empty-matrix convention if R is empty). The exact Schur
complement on S is

    K_k=M_k[S,S]-M_k[S,R] M_k[R,R]^(-1) M_k[R,S]
       =tau_k (C_k[S,S])^(-1).                             (6)

Its U,U and T,T blocks vanish. Equivalently, the uncorrected internal
blocks satisfy

    M_k[U,U]=M_k[U,R] M_k[R,R]^(-1) M_k[R,U],
    M_k[T,T]=M_k[T,R] M_k[R,R]^(-1) M_k[R,T].              (7)

Thus a proper component supplies a bipartite Schur complement, not
automatically a bipartite actual induced source. No hafnian Schur
factorization, actual source operation, or vanishing of the boundary
terms in (7) is asserted. For singular Z_k, the kernel-to-boundary
coupling in (4) is the corresponding exact obstruction to such a step.

## 4. The spanning common-neighbor case is excluded

If S=V, (4) forces z_k=r. Equation (6) has no boundary correction,
so both other M_k are bipartite on the SAME shores U,T as M_h.
The full ternary source would therefore be bipartite on these shores.

For completeness, project to the other two colors b,c. The resulting
balanced bipartite quadratic B has whole top tau_b b^V+tau_c c^V.
For every u in U,t in T its actual whole b/c deleted-pair cofactor
F_ut is nonzero by the reviewed two-active cofactor theorem. Project
the original full source to h at u,t and b/c elsewhere. Only an
h edge joining u,t can contribute, so its exact tensor is

    0=M_h[u,t] F_ut.

Every h crossing cell is therefore zero, contradicting tau_h!=0.
This proves the spanning exclusion. It uses whole cofactor nonvanishing
and does not replace a hafnian cancellation by a support exclusion.

## 5. A crown component with one exterior edge is impossible at all orders

**Theorem.** For every r>=3, a full ordinary ternary source on
n=2r+2 vertices cannot have the following color-h support:

    S=U union T, U={u_1,...,u_r}, T={t_1,...,t_r};
    M_h[u_i,t_j]!=0 exactly when i!=j;
    the remaining R={x,y} has one nonzero h edge x--y;
    there are no other h edges.

All nonzero weights may be arbitrary complex numbers. The graph on
S is the complete bipartite graph with one perfect matching removed
(a crown graph); it is connected for r>=3. No corresponding restriction
on the other two color supports is assumed.

Fix either k!=h. Two distinct U vertices have r-2 common h neighbors,
and similarly on T. Equation (3) therefore applies. Its crossing
block is diagonal in the displayed pairing:

    Z_k=diag(z_1,...,z_r),                                (8)

since every off-diagonal U--T pair is an h edge.

Both the k adjacency and cofactor vanish on the exterior pair:

    M_k[R,R]=0,       C_k[R,R]=0.                         (9)

For the first statement, the h hafnian on S is nonzero because the
full pure h hafnian is M_h[x,y] haf(M_h[S])!=0. The mixed word
k on R and h on S gives M_k[x,y] haf(M_h[S])=0.
For the second, the word h on R and k on S gives
M_h[x,y] haf(M_k[S])=0, and haf(M_k[S]) is exactly C_k[x,y].
The two diagonal entries in each block are already zero by definition.

Insert rank M_k[R,R]=0 and q=2 in (4). It follows that

    rank Z_k=r-1.                                         (10)

Thus exactly one z_i is zero. Let K={u_i,t_i} be this unique pair,
and let F=S without K. In the order F,K,R, the actual cofactor is

    C_k = [[J,0,B],
           [0,0,D],
           [B^T,D^T,0]],                                (11)

where J is the invertible weighted matching matrix on the other
r-1 missing crown pairs. Invertibility of C_k forces the 2-by-2
matrix D to be invertible: any nonzero vector in ker(D^T) would
give a full kernel vector supported on K.

The K row-block of C_k M_k=tau_k I now gives

    M_k[R,F]=0,      D M_k[R,K]=tau_k I_2.                (12)

Together with (9), every vertex of R has nonzero k degree at most
two, with all neighbors in K. The reviewed scalar degree-two lemma
forces each degree to be one. The scalar leaf lemma makes those
edges isolated. Invertibility of the second block in (12) ensures
that the two exterior vertices match to different vertices of K.

Hence K union R splits off as two isolated k edges. On F, equation
C_k M_k=tau_k I reduces to J M_k[F,F]=tau_k I. Therefore

    M_k[F,F]=tau_k J^(-1),                               (13)

which is a weighted matching on the r-1 pairs u_j--t_j with j!=i.
The WHOLE k graph is consequently a perfect matching consisting of
all but one missing crown pair, with its remaining two endpoints
matched to x,y in one of the two possible ways. This conclusion
was proved separately for each of the other two colors b,c.

Each such matching contains r-1 of the same r missing crown pairs.
Thus the b and c matchings share at least r-2>=1 edges. Choose one
shared pair e. The word with color b exactly on e and color c at all
other vertices has coefficient

    M_b[e] haf(M_c[V without e]) != 0.                   (14)

The first factor is a nonzero edge weight. The second is the product
of the remaining c matching weights, all nonzero; it has a UNIQUE
matching term. Both color classes are nonempty. This contradicts (1)
and proves the theorem. No census, positivity assumption, graph
classification, or inference from a vanishing permanent is used.

For r=4 this excludes a monochromatic cube component together with
one isolated edge at n=10. The proof is the uniform r>=3 argument,
not a separate ten-vertex enumeration.

## 6. Exact controls and the remaining obstruction

The [companion checker](../unaudited-codex-diagonal-continuation-2026-09-20/verify_component_boundary_controls.py) verifies two scope guards using actual hafnians.
First, the allowed K4 ternary source has an h component that is a
single edge. Its same-shore pair-coverage hypothesis is vacuous, and
its exterior cofactor blocks for both other colors are nonzero.
Thus proper-component coupling cannot be discarded in general.

Second, take the scalar eight-vertex cubic block with bipartite matrix

    W=[[0,1,1,1],[1,0,1,-1],[1,-1,0,1],[1,1,-1,0]],
    H=[[0,W],[W^T,0]],

and add an isolated scalar edge of weight five. The resulting scalar
M has exactly the r=4 support excluded above, yet its actual hafnian
is 15 and its actual cofactor satisfies MC=15I. Its higher single-color
star sums also vanish. Thus the exclusion requires compatibility with
both other target colors; the original scalar inverse identity alone
does not exclude this support.

For a general proper h component, (4) and (7) retain all exterior
coupling. Larger exteriors need not force an other-color exterior
vertex to have degree at most two, which is the decisive additional
step in Section 5. No universal closure of those boundary terms or
coverage of arbitrary dense weighted sources is claimed.

**Integration provenance.** Frozen mathematical source: [BIPARTITE-COLOR-COMPONENT-BOUNDARY-AND-CROWN-EXCLUSION.md](../unaudited-codex-diagonal-continuation-2026-09-20/BIPARTITE-COLOR-COMPONENT-BOUNDARY-AND-CROWN-EXCLUSION.md),
SHA256 `7a48cf15c3ee7f13b9aafc5b15855b1765995f6c17a26390a9e7f6c11e7129fd`. Only review status, relative dependency links,
and this provenance paragraph changed. The complete audit linked above remains byte-identical.
