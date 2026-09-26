# Complete independent audit of cubic scalar triangle exclusion

**Verdict: COMPLETE INDEPENDENT PASS, without source correction.**
Auditor: `/root/recover_half_shore`, 2026-09-20, independently of
`/root/scalar_pencil_coupling`. Every line of the frozen proof was read,
and every cofactor expansion and degree premise was reconstructed.
The core scalar proof is self-contained under its actual cofactor
identity. This audit does not resolve the general ternary conjecture.

## 1. Exact source, dependencies, and scope of the read

Accepted source:
[CUBIC-SCALAR-TRIANGLE-EXCLUSION-NEW-SOURCE.md](CUBIC-SCALAR-TRIANGLE-EXCLUSION-NEW-SOURCE.md)
— 173 lines, 7082 bytes, SHA256
`09477ab3dfae03d86b8dd700c2ce10d27f9dc34b731fae3e20bb571666051e02`.

The complete [source freeze receipt](cubic_scalar_triangle_freeze_receipt.json)
has SHA256
`249f7e0cc5366e662bc020ae77bb68fd2629898517ca4689f7a38a24f740f844`.
Its four records and all six records of the source's
[dependency inventory](cubic_scalar_triangle_dependencies.json)
match the current files in SHA256, byte count, and line count.
The inventories and all source control artifacts were read in full.

The six dependency texts and audits concern global original-basis
monochromaticity, scalar degree structure, and the strict color-degree
bound. They were all read in full during this continuous work. The
scalar-pencil independent audit was freshly read for this task; the
other five texts were read previously and remain byte-identical to
the inventoried current files. The strict-degree companion is my own
independent audit of the root's different proof. No lost temporary
artifact or whole-repository preservation claim is made here.

The core assumptions are a complex symmetric zero-diagonal scalar
matrix M on an even vertex set, its ACTUAL zero-diagonal hafnian
cofactor matrix C, a nonzero hafnian tau, and M C=tau I. Setting the
diagonal of C to zero is a definition, not a repeated-site cofactor.
Every expansion below uses the same actual M. Positivity, a second
color, or a source minimum is unnecessary for Sections 2--4.

## 2. The one-cubic-root calculation

Let p have precisely the three distinct neighbors r,s,t, with
nonzero weights a,b,c. Define H=haf(M off p,r,s,t). After deleting
s,r, the retained p can only match t, so C[s,r]=c H. Similarly,
after deleting t,r, p must match s, so C[t,r]=b H. No other term
can occur because the entire p row has been specified.

The off-diagonal entry (M C)[p,r] has the contribution a C[r,r]=0
from neighbor r; its other two contributions are b(c H) and c(b H).
It therefore equals 2bc H. Since p!=r, the assumed matrix identity
makes it zero. Division by the nonzero scalar 2bc over C gives H=0.

The same forced-partner calculation gives C[r,s]=c H,
C[r,t]=b H, C[s,t]=a H, so every cofactor between two neighbors of
p vanishes. This does not set any original edge between them to zero.
At order four the residual hafnian is the empty value one, and the
calculation already contradicts 2bc H=0. The endpoint is consistent;
there is no negative-order or repeated-vertex deletion.

## 3. Adjacent cubic vertices with a common neighbor

Write N(p)={q,r,s}, N(q)={p,r,t}, with weights a=M[p,q],
b=M[p,r], c=M[p,s], d=M[q,r], e=M[q,t], all nonzero. The vertices
s,t lie outside p,q,r but may coincide. Applying Section 2 at p
and at q gives precisely the six neighbor-neighbor cofactor zeros
listed in source (5). In particular C[p,r]=C[q,r]=0.

If s=t, these same zeros already include C[p,s]=C[q,t]=0.
The diagonal p equation reads a C[p,q]=tau. No distinct-spoke
identity or repeated deletion is used for this branch.

For s!=t, put H1=haf(M off p,q,r,t) and
H2=haf(M off p,q,s,t). I checked source (6) without assuming M C=tau I:

* In C[r,t], q is retained and both r,t are deleted. Its only
  remaining neighbor is p, so C[r,t]=a H1.
* In C[q,t], p is retained and its possible partners are exactly
  r and s. Expansion at p gives C[q,t]=b H1+c H2.
* In C[s,t], p and q are retained, each having only the other
  and r available. If either matches r, the other has no partner.
  Thus p--q is forced, and C[s,t]=a H2.

These cases exhaust all possible partners, regardless of any other
neighbors or degree at r, and regardless of edges in the remaining
core. The row p matrix product is consequently

    (M C)[p,t]
      =a C[q,t]+b C[r,t]+c C[s,t]
      =a(b H1+c H2)+ab H1+ac H2
      =2a C[q,t].

The factor two is the unsigned sum of the two identical expressions;
there is no determinant sign or unaccounted half-factor. This identity
is valid for ANY actual matrix with the two specified cubic rows.
The vertices p and t are distinct, so the scalar inverse identity
sets the left side to zero. Since a!=0, C[q,t]=0.
Interchanging p and q gives C[p,s]=0 by the same exhaustive argument.

Together with the first cofactor zeros, the four incident edges
other than p--q all have zero actual cofactors. The diagonal p
and q equations both give M[p,q] C[p,q]=tau!=0. Only these cofactor
values vanish; none of their associated original weights is removed.

## 4. Third cubic vertex, boundaries, and the source application

If r is also cubic, p and q are two neighbors of r. The one-root
calculation at r then gives C[p,q]=0, contradicting the preceding
nonzero product. This excludes every triangle all of whose three
vertices have degree exactly three, irrespective of the remaining
degrees, edges, or order. In particular each cubic component is
triangle-free. Both s=t and s!=t are covered before this final step.

A triangle cannot contain a leaf, and the reviewed scalar lemma
excludes degree two under the same actual scalar hypothesis. Therefore
any remaining scalar triangle must have a vertex of degree at least
four. This corollary does not exclude triangles at higher degrees.

For a full ternary source, the reviewed global theorem supplies the
scalar identity for each original monochromatic matrix. At n=10 the
strict all-order bound gives degree at most three in each color. The
reviewed scalar lemma says degree-one vertices form isolated matching
edges and forbids degree two; hence every remaining component is
cubic. Applying the theorem makes those components triangle-free.
This concerns each color separately. It neither excludes triangles
in the physical union graph nor proves any color component bipartite.
Odd cycles of length at least five are outside the argument.

## 5. Exact convention checks and a verified higher-degree guard

I read the entire 140-line source checker and reran it with a new
output path. Its [independent auditor output](cubic_scalar_triangle_independent_auditor_controls.json)
is byte-identical to the frozen output, SHA256
`6fd02fbf39541a44203d8badb242a8546793cf9ba6ce3b723be75a073ff46b17`.
All 132 exact identities pass: distinct and coincident external-neighbor
cases and forced triangle expansions at orders 6,8,10,12.
The arbitrary dense backgrounds permit unrestricted degrees at the
common neighbor and elsewhere. Those matrices are explicitly not
assumed to satisfy M C=tau I; the checks verify only the cofactor
identities used by the proof. They are not an existence census.

I also independently checked the higher-degree guard suggested by
`/root`, using an explicit list of perfect matchings rather than the
source checker's bitmask hafnian recurrence. On vertices {0,...,5},
put M[0,j]=M[j,0]=1 for j>0. On the other five vertices set
M[i,j]=chi(i-j modulo 5) for i!=j, where chi(1)=chi(4)=1 and
chi(2)=chi(3)=-1; all diagonal entries are zero.

The exact [guard record](cubic_scalar_triangle_degree_five_guard.json)
has SHA256
`7da6b45c4355820d3a01030fbc3c67c709078dfc489cd016fa9168cc58f868c5`.
Its 15 full perfect matchings and the three matchings per four-site
cofactor give

    haf(M)=5,     C=M,     M C=5I.

Every off-diagonal matrix entry is nonzero, so its support is K6,
every vertex has degree five, and all 20 triples are triangles.
Thus the scalar inverse-cofactor identity alone does permit triangles;
the cubic degree premises are essential. This guard is a scalar
example, not a full ternary source, and is not in conflict with the
strict ternary degree bound or the accepted theorem.

The previously reviewed eight-site cubic scalar conference example
is bipartite and hence triangle-free, so it remains consistent as well.
The all-order conclusion rests on the exact symbolic partner expansions,
not extrapolation from any of these finite convention checks.

## 6. Preservation and final verdict

The frozen source, author receipt, checker, frozen control output,
dependency inventory, and all six bound dependency records remain
unchanged. This task writes only the new audit, its receipt, one fresh
checker output, and the independently verified degree-five guard.
Every local link in this audit was checked to resolve.

The adjacent-cubic/common-neighbor lemma, its exact factor-two identity,
all endpoint cases, and the cubic-triangle contradiction pass completely.
The n=10 structural corollary has the stated reviewed inputs and scope.
No broader scalar triangle prohibition, bipartiteness conclusion,
universal descent, or resolution of the general conjecture follows.
