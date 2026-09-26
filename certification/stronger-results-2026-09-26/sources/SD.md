# Scalar pencil star invariance, principal cofactors, and scalar degree restrictions

**Status.** Independently audited all-order research theorem, 2026-09-20.
[Complete independent audit PASS](../unaudited-codex-diagonal-continuation-2026-09-20/SCALAR-PENCIL-STAR-INVARIANCE-AND-NEIGHBORHOOD-RANK-AUDIT.md); the parent read
the complete frozen source and audit and accepted the stated mathematical scope.
The frozen review objects remain unchanged in the staging folder.
The general conjecture remains open; formal certification status is unchanged.

## 1. Hypotheses and reviewed inputs

Let V have n=2m>=4 vertices. Work over C, with the ordinary commutative
physical-site-square-zero algebra and Q^[j]=Q^j/j!.
Assume an ACTUAL full ternary source whose whole output is

    A^[m] = tau_a a^V + tau_b b^V + tau_c c^V,
    tau_a tau_b tau_c != 0.                                    (1)

The reviewed global edge theorem gives diagonal original edge blocks.
Write the resulting three symmetric zero-diagonal scalar matrices as
M_a,M_b,M_c. Their actual zero-diagonal hafnian cofactor matrices are

    C_h[u,v] = haf(M_h[V without u,v])   (u!=v),
    C_h[u,u] = 0,
    M_h C_h = tau_h I,     C_h = tau_h M_h^(-1).                (2)

The zero diagonal in C_h is a definition, not a repeated-vertex deletion.
Here and below haf(empty)=1, and an odd restriction has hafnian zero.
For any partition V=S_a disjoint_union S_b disjoint_union S_c, the whole
coefficient is exactly product_h haf(M_h[S_h]). Thus

    product_h haf(M_h[S_h]) = 0
    for every partition with at least two nonempty parts.       (3)

For a root p put Omega=V without p, R=A restricted to Omega, and

    X_h = sum_(q!=p) M_h[p,q] h_q.

The reviewed higher-odd theorem says that for every 1<=r<=m-1 and any
2r+1 rows L_j in span{X_a,X_b,X_c}, the entire response

    (product_j L_j) R^[m-r-1]                                  (4)

has zero projection onto EVERY binary color palette, including its two
pure words. This combines higher pure vanishing and whole two-color
mixed vanishing. Its use requires the original three active targets.
A general binary source does not supply (4).

The dependencies and their exact current hashes are recorded in
[the frozen dependency record](../unaudited-codex-diagonal-continuation-2026-09-20/scalar_pencil_star_invariance_dependencies.json). Their mathematical
source texts were read for this derivation. Hashing the companion audits
records dependency provenance, not a new independent audit of them.

## 2. Two-color scalar pencils retain additional third-color constraints

Fix distinct colors a,b, write D=diag(z_v), and put

    L(z)=M_a + D M_b D,
    v_p=L(z)e_p,
    C(L)[u,v]=haf(L[V without u,v]) for u!=v,
    C(L)[u,u]=0.                                               (5)

The z_v can be arbitrary complex numbers, or independent indeterminates.
For 0<=r<=m-1 define the divided rooted response

    s_(p,r)(L) = sum_(T subset V without p, |T|=2r+1)
                    (product_(q in T) L[p,q])
                    haf(L[V without (T union {p})]).           (6)

Then the following are polynomial identities in all z_v:

    haf(L)=tau_a + tau_b product_v z_v,
    s_(p,0)(L)=haf(L),
    s_(p,r)(L)=0                         (1<=r<=m-1).           (7)

The first identity follows by expanding the choice of a- and b-colored
edges and applying (3). To prove the last identity, project the original
binary a,b palette on Omega to one scalar coordinate per site by
a_q -> x_q and b_q -> z_q x_q. Choose the original root row
X_a+z_p X_b. Its image is sum_(q!=p) L[p,q] x_q, and the projected core
is the scalar quadratic with matrix L[V without p]. The coefficient of
x^Omega in its raw (2r+1)-st response is (2r+1)! s_(p,r)(L). Equation
(4) makes it zero. The factorial is nonzero over C. This also proves
the claim when some z_v vanish, since it is a polynomial identity.

The third color c gives a separate cofactor constraint on the entire
pencil:

    M_c[u,v] C(L)[u,v]=0              for every u!=v.           (8)

Indeed the left side is the projection of the whole original slice
having c at precisely u,v and only a,b elsewhere. The c pair must use
the original edge u,v. Every resulting color word is mixed because
n>=4; its amplitude is zero by (3). Thus a nonzero c edge forces the
ACTUAL pencil cofactor polynomial at that pair to vanish identically.
No replacement of a hafnian by a determinant occurs here.

## 3. Matrix cubic identity and exact rank-one invariance

The cubic member of (7) is the concise matrix identity

    diag( L C(L) L ) = 0.                                     (9)

For verification, its p-th diagonal entry is
sum_(r,s) L[p,r] C(L)[r,s] L[s,p]. Terms containing p or r=s vanish.
In every remaining cofactor p is retained. Expanding at p gives the
sum over ORDERED distinct r,s,t outside p of

    L[p,r] L[p,s] L[p,t]
        haf(L[V without p,r,s,t]).

This is 3! s_(p,1)(L), including at n=4 where the last hafnian is 1.
Hence there is no omitted factor of two or six in (9).

More generally, regard haf as ignoring all diagonal matrix entries.
Then for every root p and scalar t,

    haf( L + t v_p v_p^T ) = haf(L).                          (10)

This is a statement about a SCALAR hafnian pencil, not an assertion
that the update preserves the full ternary source. In particular the
updated full matrix may have nonzero diagonal entries, which are ignored
by the hafnian. Deleting those entries has the same hafnian.

Here is the exact coefficient calculation. The coefficient of t^j in
haf(L+t v_p v_p^T), for 1<=j<=m-1, chooses 2j updated vertices U, matches
them using rank-one entries in (2j-1)!! ways, and matches the others
using L. Since (v_p)_p=L[p,p]=0, p is not in U. Expanding the remaining
hafnian at p selects another vertex q outside U. For any fixed set
T=U union {q} of size 2j+1 there are 2j+1 choices of q. Consequently

    [t^j] haf(L+t v_p v_p^T) = (2j+1)!! s_(p,j)(L)
                             = raw_response/(2^j j!).         (11)

The j=m coefficient is zero because it would include the p coordinate
of v_p; higher powers are absent by degree. Equations (7) and (11) prove (10), with no infinite series.
In particular the derivative at t=0 is

    (1/2) v_p^T C(L) v_p = 3 s_(p,1)(L),

which agrees with (9).

When L is invertible, (10) also reads

    haf((L^(-1)-t E_pp)^(-1)) = haf(L).                        (12)

Indeed Sherman--Morrison has denominator 1-t L[p,p]=1, so that the
inverse on the left is exactly L+t v_p v_p^T for every t. This is only
a one-coordinate inverse-diagonal deformation at this L. It does NOT
justify composing such deformations at different roots: the matrix
after the first deformation has not been shown to obey the hypotheses.
It does not assert L C(L)=haf(L)I for the two-color pencil.

## 4. All even neighbor subsets annihilate complementary hafnians

Fix distinct colors h,k and a root p. For EVERY nonempty even subset
U of N_(G_h)(p), the actual complementary principal hafnian satisfies

    haf(M_k[V without U])=0.                                  (13)

Indeed use |U| copies of X_h and one of X_k in (4). Extract the word
having h precisely on U and k on Omega without U. The h rows must fill
U, in |U|! orders. The remaining k row and k core expand the actual
k-hafnian off U at its retained vertex p. Thus the coefficient is

    |U|! (product_(u in U) M_h[p,u]) haf(M_k[V without U]).      (14)

Every product factor is nonzero. The word uses both h and k because
U is a nonempty even subset of the odd set Omega. The row order is
permitted because |U|+1<=n-1. Equation (4) makes (14) zero and proves
(13). These are hafnian cofactors, not determinant minors.

For |U|=2, (14) is the cubic observation communicated by `/root`:

    0=2 M_h[p,u] M_h[p,v] C_k[u,v].                            (15)

Together with the original mixed two-site coefficient
M_h[p,u] C_k[p,u]=0 and the defined zero diagonal of C_k, this gives
C_k[S,S]=0 for S={p} union N_(G_h)(p). The separate frozen source
[CLOSED-NEIGHBORHOOD-ISOTROPY-AND-STRICT-COLOR-DEGREE-NEW-SOURCE.md](../unaudited-codex-diagonal-continuation-2026-09-20/CLOSED-NEIGHBORHOOD-ISOTROPY-AND-STRICT-COLOR-DEGREE-NEW-SOURCE.md)
(SHA256 e4ae380205cae410f46a8ba9dbf1e069c38ba185ce2a3ddf7855b2f4d74c5a36,
208 lines, pending audit at its freezing and now independently accepted;
see the [reviewed degree theorem](UNIFORM-CLOSED-NEIGHBORHOOD-ISOTROPY-AND-COLOR-DEGREE-BOUND.md))
proves its complementary-rank, rank-two-support, and strict degree
consequences. Those additional conclusions are not used to prove any
claim in this note and are not duplicated here.

## 5. Independent scalar lemma: leaves are isolated edges; degree two is impossible

This section assumes ONLY a symmetric zero-diagonal scalar matrix M
of even order, its ACTUAL zero-diagonal hafnian cofactor C, and

    haf(M)=tau!=0,        M C=tau I.                          (16)

It does not need another color or the whole-binary higher identities.
Every vertex has degree at least one by the hafnian expansion.

First suppose p has the sole neighbor r, of weight a!=0. For q outside
{p,r}, expansion of C[p,q] at r gives

    C[p,q]=sum_(s outside p,r,q) M[r,s]
                         haf(M[V without p,r,q,s]).

In (M C)[r,q], the s=p summand is a C[p,q]. In every other contributing
cofactor C[s,q], the retained p must match r, giving the SAME sum once
more. Hence 0=(M C)[r,q]=2a C[p,q]. All those C[p,q] vanish, and
C[p,r]=tau/a!=0. Equation C M=tau I now forces M[r,q]=0 for every q!=p.
Thus a degree-one vertex belongs to an isolated two-vertex component.

Next suppose p has exactly two neighbors r,s with weights a,b!=0.
For q outside {p,r,s}, expand the retained p in C[r,q] and C[s,q].
Each expansion has only the other neighbor available, so

    0=(M C)[p,q]
      =2ab haf(M[V without p,q,r,s]).                        (17)

Therefore all the hafnians on the right vanish. Expanding C[p,r] at
retained s expresses it as a linear combination of those same zero
hafnians; expanding C[p,s] at retained r does the same. Thus both
C[p,r] and C[p,s] are zero. The p-th diagonal entry of (16) would be
tau=a C[p,r]+b C[p,s]=0, a contradiction.

Consequently every component is either an isolated matching edge or
has minimum degree at least THREE. If an independently supplied upper
bound makes every degree at most three, each nonmatching component is
cubic. A bound of at most two forces a union of isolated matching edges.
There is no claim that scalar identity (16) alone forces all components
to be matching edges; the exact cubic control below refutes that claim.

## 6. Exact controls and explicit nonclaims

The accompanying standard-library checker
[verify_scalar_pencil_star_invariance.py](../unaudited-codex-diagonal-continuation-2026-09-20/verify_scalar_pencil_star_invariance.py) uses exact integers and rational
matrix inversion. Its frozen output records the following controls.

1. The ordinary four-site three-colored matching source has all three
   target hafnians 1 and every mixed partition amplitude zero. For each
   pair of colors, (7), (9), and (10) hold at the tested integral choices
   of D and t. This verifies factors and the allowed four-site boundary;
   it is not the proof of the polynomial identities.

2. The binary eight-site control has M_a=[[0,H],[H^T,0]], where H is the
   Sylvester 4-by-4 Hadamard matrix, and M_b is the unit matching
   (0,1),(2,3),(4,5),(6,7). It has tau_a=8,tau_b=1, C_a=2M_a,
   C_b=M_b; all 254 mixed binary partition amplitudes vanish. Yet for
   L=M_a+M_b and p=0, s_(p,1)=2 and s_(p,2)=1. Thus

       (L C(L) L)[0,0]=12,
       haf(L+t v_0 v_0^T)=9+6t+15t^2.

   This exact control separates the new constraints from the binary
   pencil identity plus the two individual inverse identities. It is
   not a ternary counterexample.

3. The 4-by-4 integer matrix

       W=[[0,1,1,1],[1,0,1,-1],[1,-1,0,1],[1,1,-1,0]]

   has permanent 3, permanent-cofactor matrix W, and WW^T=3I.
   Hence M=[[0,W],[W^T,0]] is a scalar cubic graph on eight vertices
   satisfying haf(M)=3 and C=M, so MC=3I. This validates the sharp
   scalar distinction between forbidden degree two and allowed degree
   three. No compatible other colors are supplied.

Nothing here proves a common bipartition for a pair of colors, ordinary
matrix-rank control from a nonzero permanent, or a universal descent.
The one-root rank-one invariance is not a full-source preservation
theorem. The principal hafnian vanishing in (13) applies to neighbors of one
actual root, not to an arbitrary selected vertex set.
The remaining weighted ternary cancellation system is still open.

**Integration provenance.** Frozen mathematical source: [SCALAR-PENCIL-STAR-INVARIANCE-AND-NEIGHBORHOOD-RANK.md](../unaudited-codex-diagonal-continuation-2026-09-20/SCALAR-PENCIL-STAR-INVARIANCE-AND-NEIGHBORHOOD-RANK.md),
SHA256 `4ad27d6f2c4d3dae187d51a70e9d53d47875203c0b7f12fbba248c47b723f7a0`. Only review status, dependency links,
and this provenance paragraph changed. The complete audit linked above remains byte-identical.
