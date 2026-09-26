# Complete independent audit of component boundary ranks and crown exclusion

**Verdict: COMPLETE INDEPENDENT PASS, without source correction.**
Auditor: `/root/recover_half_shore`, 2026-09-20, independently of source
author `/root/audit_global_foundation`. I read every line of the frozen
source and reconstructed its full proof, including every actual-source
cofactor identification and the isolated-matching step in Section 5.
This audit accepts the stated all-order crown family exclusion. It is
not an audit or certification of any separate complete H10 proof.

## 1. Exact frozen source and reviewed material

Accepted [source](BIPARTITE-COLOR-COMPONENT-BOUNDARY-AND-CROWN-EXCLUSION.md):
265 lines, 11971 bytes, SHA256
`7a48cf15c3ee7f13b9aafc5b15855b1765995f6c17a26390a9e7f6c11e7129fd`.

The complete [source receipt](component_boundary_and_crown_exclusion_freeze_receipt.json)
has SHA256
`5af5b65ae12c577cf64cb7eccdcbf42f4b0509d032720599e2d73e8937daed3e`.
All eleven bound records were checked against their current SHA256,
byte counts, and line counts. The entire receipt, 93-line checker,
and its frozen output were read. The eight input proof/audit texts
were read in full during this continuous work; the source author's
147-line foundation reconstruction and the exact 269-line frozen
scalar-pencil source were freshly read for this task. Previously read
inputs remain byte-identical to their receipt records.

The mathematical premises are an actual full ordinary complex ternary
source with all three pure amplitudes nonzero, the reviewed original-
basis global diagonality and actual inverse-cofactor identity, the
other-color cofactor zeros on monochromatic distance at most two,
and the reviewed scalar leaf and degree-two lemmas. Whole two-target
rectangular-cofactor nonvanishing is additionally used for the spanning
corollary; it is not needed in the crown-plus-edge proof in Section 5.
The strict color-degree upper bound is not required here either.

The scalar matrices and cofactors are those of the SAME original
source. The diagonal of each C_h is defined to be zero. Inverses are
ordinary complex matrix inverses, not physical-algebra inverses.
Nonzero hafnian sums are not treated as positive or uncancelled sums.

## 2. Proper unions of components must couple externally

Because G_h has no edges between components, its whole pure hafnian
is the product of the hafnians on those components. The nonzero pure
amplitude makes every factor nonzero. Thus every component has even
size, and a bipartite component must have balanced shores. Every
nonempty proper union S of h components has nonzero h hafnian.

If another M_k had zero crossing block on S,R=V without S, its nonzero
hafnian would similarly factor with BOTH factors nonzero. The original
word h on S and k on R would have coefficient
haf(M_h[S]) haf(M_k[R])!=0, a contradiction. Both color classes are
nonempty. This proves that the other adjacency crossing block is
nonzero for every such cut.

If the corresponding C_k crossing block were zero, symmetry would
make C_k block diagonal. Since it is invertible, each diagonal block
and its inverse are invertible, making M_k=tau_k C_k^(-1) block
diagonal as well, contrary to the preceding conclusion. This gives
the same nonzero crossing statement for actual cofactors.
Every nontrivial cut of the quotient by h components consequently has
an edge in either other adjacency or cofactor support graph. That is
exactly connectivity of the stated quotient support graphs. No claim
that every pair of components is directly coupled follows or is used.

## 3. Common-neighbor coverage and all boundary rank formulas

Let S=U union T be a balanced bipartite h component, with each shore
of size r, and with every same-shore pair sharing an h neighbor.
The distance-two cofactor rule kills C_k[U,U] and C_k[T,T] for k!=h;
their diagonals already vanish by definition. The original mixed-edge
rule kills each entry of the cross block Z_k at an h edge. Thus the
literal actual cofactor principal block is [[0,Z_k],[Z_k^T,0]].
Its rank is 2z_k and nullity 2(r-z_k), with z_k=rank Z_k.

I independently reconstructed the complementary-nullity identity.
For invertible M and C=tau M^(-1), take x in ker M[R,R] and set
y=M[S,R]x. Then M(0,x)=(y,0), so C(y,0)=tau(0,x), proving
C[S,S]y=0. This map is injective by invertibility of M. Conversely,
if C[S,S]y=0, write C(y,0)=(0,z). Then M(0,z)=tau(y,0), so
z belongs to ker M[R,R] and maps to tau y. Division by nonzero tau
proves surjectivity. Hence the nullities agree exactly.

It follows that rank M_k[R,R]=q-2(r-z_k), where q=|R|. Independently,
C_k[R,S] restricted to ker C_k[S,S] is injective: a vector in both
kernels would be a full null vector of C_k supported on S. Therefore
rank C_k[R,S]>=2(r-z_k), and q>=2(r-z_k). All three claims in source
(4) follow, including when Z_k is singular.

If nu is the maximum matching size of the zero-cell pattern of M_h
between U,T, then every nonzero minor of Z_k contains a supported
permutation and therefore a matching of that size. Thus z_k<=nu and
q>=2(r-nu). This is a determinant-minor support argument for an
ordinary scalar rank, not an inference from a hafnian or permanent.
For a complete bipartite h component, nu=0 gives q>=2r as claimed.

When z_k=r, the rank formula makes M_k[R,R] invertible. Its ordinary
Schur complement K_k on S satisfies (M_k^(-1))[S,S]=K_k^(-1).
Since C_k[S,S]=tau_k K_k^(-1), one obtains
K_k=tau_k(C_k[S,S])^(-1). The inverse of the displayed off-diagonal
block matrix has zero U,U and T,T blocks. Rearranging K_k's definition
therefore gives exactly both boundary identities in source (7), with
the stated positive right-hand sign. The empty exterior is allowed
with the empty inverse convention. No hafnian Schur factorization or
actual source modification is inferred from this matrix identity.

## 4. Spanning case and whole binary cofactor compatibility

If S=V, the nonnegative-rank formula with q=0 forces z_k=r. The Schur
boundary correction is absent; hence both other scalar matrices have
zero same-shore blocks on the same U,T as M_h. The full original
source is therefore bipartite on that one balanced cut.

Projecting to the other colors b,c gives an ACTUAL balanced binary
quadratic B with whole top tau_b b^V+tau_c c^V. The reviewed theorem
makes every opposite-shore deleted-pair cofactor nonzero as a whole
b/c tensor, whether or not its physical crossing edge is present.
This tensor is precisely the b/c projection of the corresponding
cofactor of the original A. Projecting commutes with deleting the two
sites and taking the divided power.

A whole original slice with h only at u,t forces their h edge, because
all original blocks are diagonal. Its coefficient tensor is M_h[u,t]
times that SAME projected cofactor. The source equation sets it to
zero; every pure target is killed because n>=4 and the remaining
sites are restricted to b/c. Thus all h crossing edges would be zero,
contradicting tau_h!=0. No particular pure coefficient of the nonzero
binary cofactor is assumed nonzero in this argument.

## 5. Crown component: two different original mixed words give two zeros

For the crown-plus-edge hypothesis, r>=3 and S has shores U,T of
size r. Each same-shore pair has r-2>=1 common h neighbors, so the
preceding principal-block conclusion applies. Its allowed cross
entries are exactly the missing pairs u_i,t_i, giving diagonal Z_k.
The nonzero h amplitude factors as M_h[x,y] haf(M_h[S]); hence both
factors are nonzero. No nonzero residual hafnian has been introduced
without this exact factorization from the stated h support.

For each other color k, the ORIGINAL word k on {x,y} and h on S
has coefficient M_k[x,y] haf(M_h[S]). Its vanishing proves
M_k[x,y]=0. A DIFFERENT original word, h on {x,y} and k on S,
has coefficient M_h[x,y] haf(M_k[S]), so haf(M_k[S])=0.
This last hafnian is precisely the actual cofactor C_k[x,y].
The defined zero diagonals now yield BOTH M_k[R,R]=0 and C_k[R,R]=0.
These statements refer to adjacency and cofactor separately; neither
has been substituted for the other without proof.

The rank formula with q=2 and rank M_k[R,R]=0 gives z_k=r-1.
Since Z_k is diagonal, exactly one diagonal entry vanishes and all
other r-1 entries are nonzero. Let K be that unique missing pair,
and F=S without K. Reordering actual vertices as F,K,R gives

    C_k=[[J,0,B],[0,0,D],[B^T,D^T,0]],

where J is an invertible weighted matching matrix. The zero F,K
block follows from the diagonal structure of Z_k and the same-shore
zero blocks. The zero R,R block is the separately proved actual
cofactor zero. If D^T had a nonzero kernel vector, placing it only
on K would give a full null vector of C_k. Therefore the square
2-by-2 matrix D is invertible.

## 6. Forced degree reduction and the actual isolated matchings

Symmetry or inversion gives C_k M_k=tau_k I as well as M_k C_k=tau_k I.
Its K row is [0,0,D]. Taking F columns gives D M_k[R,F]=0, hence
M_k[R,F]=0. Taking K columns gives D M_k[R,K]=tau_k I_2, so
M_k[R,K] is invertible. Together with M_k[R,R]=0, both vertices of
R have all their neighbors in the two-vertex set K, and neither row
is zero. Their actual k degrees are therefore either one or two.

This is where actual hafnian-cofactor compatibility is essential.
The reviewed scalar degree-two lemma applies to this SAME M_k,C_k
and forbids degree two. Both exterior vertices consequently have
degree one. Invertibility of M_k[R,K] forces their nonzero entries
to lie in distinct columns, so the two exterior vertices match to
different vertices of K. The scalar leaf lemma now says each of
those two edges is an ISOLATED component. In particular their K
partners have no additional edges to F or to one another.

The complete remaining block M_k[F,F] is then determined without
ignoring a boundary term. In the F,F block of C_k M_k, both products
with K and R vanish because the corresponding adjacency blocks have
just been shown zero. Hence J M_k[F,F]=tau_k I, and
M_k[F,F]=tau_k J^(-1). The inverse of J is again supported precisely
on its r-1 nonzero missing crown pairs. Thus the whole k graph is
a perfect matching: those r-1 pairs plus the two isolated exterior
edges. All its matching weights are nonzero.

This derivation is repeated separately for b and c, allowing their
unique exceptional indices and exterior orientations to differ.
Their sets of internal missing-pair edges have intersection of size
at least (r-1)+(r-1)-r=r-2>=1. For a shared pair e, the original
mixed word b on e and c elsewhere has coefficient
M_b[e] haf(M_c[V without e]). The second factor is the product of
the remaining nonzero c matching weights, with exactly one matching
term. It is nonzero, as is the first factor. The word is mixed, so
this contradicts the original source equation. This proves the full
r>=3 theorem without a graph census or a positivity assumption.

For r=4 the crown graph is the cube graph, so the stated cube-plus-
edge exclusion at n=10 follows. The argument does not claim that
this is the only possible ten-vertex support; such coverage belongs
to any separately proposed H10 proof and is outside this audit.
At r=3 all arguments remain valid; no r=2 crown/common-neighbor
extension is being asserted.

## 7. Exact scope controls and preservation

I reran the complete source checker with a new output path. The
[independent auditor output](component_boundary_independent_auditor_controls.json)
is byte-identical to the frozen source output, SHA256
`0692ca66ff046be5ea5252984844ad9314f6c5a49e1a63f990e6c24be38fa20d`.
It verifies all 81 unequal-weight K4 color words, the displayed two
nonzero exterior cofactor blocks, all 100 actual scalar inverse
entries for the crown-plus-edge control, and its 40 higher scalar
star sums. The scalar control has hafnian 15 with exterior edge
weight five and satisfies M C=15I. It confirms that the family is
not excluded by the individual scalar identity alone.

The K4 control confirms that the boundary terms of a proper component
cannot be discarded merely because same-shore cofactor blocks vanish.
The crown-plus-edge control has only one scalar color, so it is not
a counterexample to the full ternary theorem. These bounded checks
validate conventions and scope; the all-order proof is the reasoning
in Sections 2--6 above.

All eleven source-bound records and the original source receipt remain
unchanged. This task writes only a new full audit, its receipt, and a
fresh checker output. No canonical file, accepted proof, or frozen
source was edited. All local audit links resolve.

**Final verdict: COMPLETE PASS.** The general component coupling,
exact rank and Schur boundary formulas, spanning exclusion, and
uniform crown-plus-one-edge exclusion follow with their stated scopes.
No general elimination of larger boundary terms, complete H10 proof,
or all-order closure of the conjecture is claimed by this audit.
