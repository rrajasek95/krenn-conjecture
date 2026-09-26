# Independent audit of closed-neighborhood isotropy and strict color degree

**Verdict: COMPLETE INDEPENDENT PASS, without source correction.**
Auditor: `/root/recover_half_shore`, 2026-09-20, independently of author
`/root`. I read every source line and reconstructed every coefficient,
equality case, endpoint, nullity statement, and rank-two characterization.
The preliminary check mentioned in the source was not used as evidence.
This audit accepts the research composition; it does not formally certify
or resolve the general conjecture.

## 1. Exact frozen source and current inputs

Accepted source:
[CLOSED-NEIGHBORHOOD-ISOTROPY-AND-STRICT-COLOR-DEGREE-NEW-SOURCE.md](CLOSED-NEIGHBORHOOD-ISOTROPY-AND-STRICT-COLOR-DEGREE-NEW-SOURCE.md)
— 208 lines, 9498 bytes, SHA256
`e4ae380205cae410f46a8ba9dbf1e069c38ba185ce2a3ddf7855b2f4d74c5a36`.

Its complete [frozen input receipt](CLOSED-NEIGHBORHOOD-ISOTROPY-AND-STRICT-COLOR-DEGREE-NEW-SOURCE-FREEZE.json)
has 48 lines, 2218 bytes, SHA256
`69d4a0ccaeae2a5c83c438cac7909b7bbf173d03bf682baa06741f333fcea720`.
All seven records in that receipt match the current files in complete
SHA256, byte count, and line count. The six canonical input proof/audit
files were all read in full. The four global-monochromaticity and
rectangular-cofactor files were read during the immediately preceding
half-shore task, then checked to be byte-identical on this audit; the
two higher-response files were freshly read in full for this audit.

The exact inputs are original-basis diagonality and scalar cofactor
inversion; higher odd binary-palette response vanishing on an actual
three-active diagonal-response frame; and whole active-plane rectangular
cofactor nonvanishing for an actual balanced binary bipartite source.
Their independent audits were read alongside the proofs. This is an
audit of their stated composition, not a fresh formal certification of
every ancestral theorem in their dependency chains.

The original source has n=2m>=4 sites, local spaces exactly C^3, and
three nonzero whole pure amplitudes. These hypotheses supply every
invoked input. In particular deleting any root p gives actual rows
X_a,X_b,X_c whose responses are tau_h h^(V without p). Their image
has rank three, so the required all-three-active and rank premises
hold at that SAME odd core. Its half-order parameter is m-1; hence
the allowed higher-response range is 1<=r<=m-1 and its residual
quadratic power is m-1-r, as used throughout the new source.

## 2. The degree-three coefficient and closed-neighborhood isotropy

Fix h!=k, root p, and two distinct u,v outside p. In the binary word
having h precisely at u,v and k everywhere else off p, the two X_h
factors must occupy u and v. Global diagonality makes every component
of X_h have receiving color h; no other positions are possible.
These two ordered placements contribute the factor two. The X_k
factor occupies a unique t outside p,u,v. The remaining 2m-4 sites
are supplied by R_p^[m-2], with pure-k coefficient the actual hafnian
of M_k restricted off p,u,v,t. Therefore the coefficient is exactly

    2 M_h[p,u] M_h[p,v]
      sum_(t outside p,u,v) M_k[p,t]
          haf(M_k[V without p,u,v,t]).

The bracketed sum is C_k[u,v]: the actual cofactor defining it retains
p, and expansion at that retained p gives precisely these terms.
There is no additional half-factor and no independently specified
cofactor. The reviewed r=1 higher-response identity makes this entire
binary mixed coefficient zero. When n=4 the remaining hafnian is
haf(empty)=1 and the same ordered-placement normalization holds.

Independently, the original full word with h at p,u and k elsewhere
has coefficient M_h[p,u] C_k[p,u]. Diagonality forces the unique h
edge p--u, and the remaining complete k matching sum is the cofactor.
The original whole equation sets this mixed coefficient to zero.
Neither calculation asserts that individual remaining matching
monomials vanish.

Let S be p and all of its nonzero h-neighbors. For two distinct
neighbors, both scalar M_h factors in the first calculation are
nonzero, so C_k[u,v]=0. For p and a neighbor the second calculation
gives the same conclusion. The diagonal entries of C_k are zero by
definition. Thus C_k[S,S]=0 for each of the TWO colors k different
from h. Symmetry and invertibility of C_k follow from the reviewed
actual inverse-cofactor theorem and tau_k!=0.

Accordingly the coordinate subspace on S is contained in its own
orthogonal complement for the nondegenerate bilinear form C_k.
The dimensions are s and 2m-s, respectively, giving s<=m and
monochromatic degree at most m-1. This dimension argument is valid
over C and uses a bilinear form, with no conjugation or positivity.
Pairs at h-graph distance one are covered by the second calculation;
pairs at distance two are covered by the first. There is no converse
assertion that more distant cofactor entries must be nonzero.

## 3. The equality case and the actual balanced binary source

Assume s=m and write V=S disjoint-union T with |T|=m. For either
other color k, the cofactor matrix has the block form

    C_k=[[0,Z],[Z^T,H]].

If Z^T x=0, then C_k(x,0)=0; invertibility therefore forces x=0.
Z is square, so it is invertible. Its explicit block inverse is

    C_k^(-1)=[[-Z^(-T) H Z^(-1), Z^(-T)],
              [ Z^(-1),                    0      ]].

Direct multiplication gives the identity. Since M_k=tau_k C_k^(-1),
its T,T block is zero. This holds for both remaining colors b,c.

Project the original whole source to the b/c planes at all sites.
There are no internal T edges in either remaining color. Every T
vertex must therefore match across to S. Both shores have m vertices,
so all m matching edges cross; no internal S edge can occur. Thus
the original projected whole top is EXACTLY the top of the actual
crossing-only binary source B. It is tau_b b^V+tau_c c^V with both
amplitudes nonzero, and B is genuinely balanced bipartite.

The reviewed rectangular-cofactor theorem now makes every opposite-
shore deleted-pair cofactor F_st nonzero as a WHOLE b/c tensor.
This step is legitimate for every s in S,t in T, even when the
physical crossing edge s--t is absent. A nonzero individual pure
coefficient is neither supplied nor needed.

After deleting one s and one t, both shores still have the same
size. Their remaining T vertices still have no internal b/c edges,
so the b/c projection of the FULL original cofactor equals precisely
F_st of B. This verifies the source compatibility needed for the
next step; the cofactor was not fitted or transferred between
unrelated quadratics.

Slice the original whole source to color h at s,t and b/c elsewhere.
There are n-2>=2 remaining sites, so every original pure target is
killed by this slice. Diagonality forces s and t to match together;
its whole coefficient tensor is M_h[s,t] F_st. Since F_st!=0, the
scalar M_h[s,t] is zero. This proves M_h[S,T]=0 for every crossing
pair. The use of the WHOLE binary cofactor is what upgrades the
weaker products with potentially zero individual pure cofactors.

## 4. Parity and the higher pure response make the bound strict

The vanishing h crossing block factorizes the original pure amplitude:

    tau_h=haf(M_h[S]) haf(M_h[T]).

If m is odd, each factor is a hafnian on an odd number of vertices
and is zero, contrary to tau_h!=0. If m is even and n>=6, then
m>=4. Both displayed factors must be nonzero.

The original root row X_h has exactly m-1 nonzero components on
S without p, by the DEFINITION of the closed neighborhood, and none
on T. Set r=(m-2)/2. It is an integer at least one, within the
reviewed higher-response range. Then 2r+1=m-1 and the remaining
power at the odd root core is m-1-r=m/2. The higher pure-response
theorem says that the pure-h coefficient of

    X_h^(m-1) R_p^[m/2]

vanishes. But physical occupancy forces the m-1 row factors to use
all of S without p exactly once. Their ordered placements contribute
(m-1)!, their scalar factors are all nonzero, and the remaining
quadratic factors occupy exactly T. The coefficient is therefore

    (m-1)! product_(u in S without p) M_h[p,u] haf(M_h[T]),

which is nonzero over C. There are no alternative placements whose
cancellation was discarded. This contradicts higher pure vanishing
and excludes the remaining even-m equality case.

Thus every single-color degree is at most m-2 for n=2m>=6.
A zero row of M_h would eliminate every full h matching and make
tau_h zero (also contradicting invertibility), so every such degree
is at least one. At n=10 this gives degrees from one through three;
it does not place that bound on the physical union graph.

At n=4, m=2, equality corresponds to m-1=1 and r=0. The invoked
vanishing theorem applies only to positive higher r; the original
row response is nonzero. The three matching colors on K4 therefore
remain allowed and saturate the preliminary bound m-1, exactly as
the source states. No negative power or higher-response extrapolation
is used. The n=6 odd-m equality case is covered directly by parity.

## 5. Complementary nullities and the exact rank formula

For an arbitrary partition S,T and C=tau M^(-1) with tau!=0, define

    f:ker M[T,T] -> ker C[S,S],    f(x)=M[S,T]x.

If x lies in the first kernel, M(0,x)=(f(x),0), so multiplying by
C gives C(f(x),0)=tau(0,x). Its S component is zero, proving the
claimed range. If f(x)=0, invertibility of M gives x=0, so f is
injective. Conversely, for y in ker C[S,S], write C(y,0)=(0,z).
Then M(0,z)=tau(y,0); hence z lies in ker M[T,T] and f(z)=tau y.
Since tau is nonzero, z/tau is a preimage of y. This proves an
actual isomorphism, with the indicated scalar in its inverse.

For the closed neighborhood, C_k[S,S]=0 has nullity s. Therefore
M_k[T,T] has nullity s as well, on its n-s dimensional coordinate
space, and its rank is n-2s. This holds for each of the two other
colors and every closed neighborhood, with no equality assumption.
At degree m-2, s=m-1 and |T|=m+1, so the rank is exactly two.

## 6. Rank-two zero-diagonal symmetric matrices

I reconstructed the stated graph classification without a positivity
or real-spectral assumption. For any symmetric rank-two complex matrix
K, choose a matrix Y of column rank two spanning its column space and
a left inverse L with LY=I. Symmetry implies

    K=Y J Y^T,       J=L K L^T.

Indeed YLK=K, and transposing gives K L^T Y^T=K. J is symmetric
and must have rank two because K does. Thus J is a nondegenerate
symmetric form on C^2. Its isotropic cone is two distinct lines:
a nonsingular binary quadratic over C factors into two distinct
linear forms. A repeated factor would make J singular.

Zero diagonal of K means every nonzero row y_i of Y belongs to
one of those two isotropic lines. Pairings on the same line vanish.
The orthogonal complement of an isotropic line for a nondegenerate
form in dimension two is that line itself; hence pairings of nonzero
vectors on the two DIFFERENT lines are nonzero. Writing their rows
as nonzero scalar multiples of fixed line representatives makes
every crossing weight the product of the two scalars and one fixed
nonzero pairing. Zero rows of Y are precisely the isolated vertices.
Both line classes occur because Y has rank two.

Consequently K is a weighted complete bipartite graph with factorized
nonzero crossing weights, plus any isolated vertices. Applied at
n=10 to a cubic h vertex, each other-color block on the six remaining
vertices has exactly this structure. The two bipartitions can differ;
no conclusion that the physical union graph is bipartite follows.

## 7. Preservation, coverage, and verdict

This audit writes only a new audit file and its new receipt. The
208-line source, its original receipt, and all six bound canonical
inputs remain byte-identical. Every direct source link resolves to
the intended current file. The accompanying audit receipt records
exact hashes, sizes, and line counts; it makes no repository-wide
preservation claim and no claim to recover lost temporary files.

All coefficient identities, the maximal-isotropic equality exclusion,
the positive higher-response contradiction, the n=4 exception, the
complementary-nullity isomorphism, and the rank-two classification
pass. The result is an all-order necessary restriction. It does not
supply a general nonexistence proof, a universal shore, compatible
other-color bipartitions, or a closure of the remaining dense case.
