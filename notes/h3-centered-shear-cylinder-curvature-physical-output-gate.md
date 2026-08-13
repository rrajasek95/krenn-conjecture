# The cylinder curvature reduces to one P-half cap attachment

## Result

The exported cylinder curvature

\[
 t\,k_{ij}
\]

does not literally land in the existing offdiagonal decorated-cell/cofactor
rows.  Its coefficient factor has two unary `p/s` factors, two diagonal
`q:00` factors, and no offdiagonal edge.  Every target-augmented private-site
active term requires a named offdiagonal decorated edge.  Setting all such
edges to zero kills the complete active family while leaving a generic
`k_ij` nonzero.

There is a useful conditional positive statement: if the physical output
were a graded `A`-module with a target generator `t` in the exact required
word/fine/repeated grade, then `k_ij t` would automatically be a legal
Macaulay multiple.  The old cap graph supplies such a target correction in
its own physical grade.  In the response block, however, the mixed word
`110000` has GHZ target coefficient zero; the known endpoint target normal
occupies eighteen other words and the D4 target first appears at `111111`.
Thus the target family becomes automatic **after** the cap graph is placed
across this word change, not before.

Even when a target generator exists, module multiplication produces its
full source column, not a pure terminal.  If

\[
 d\theta=s+t,
\]

then

\[
 d(k_{ij}\theta)=k_{ij}s+k_{ij}t.                  \tag{1}
\]

For the physical cap graph `T+rho`, the companion is ordinary residue.  Its
multiple cancels the target curvature and leaves `-k_ij` in ordinary
residue.  That character is exactly the residual-`q` four-corner class and
is cancelled by the negative of the already physical endpoint-odd Cartan
packet once both objects are placed in the same grade.

The transpose defect is not an independent theorem.  The literal endpoint
transpose is a flat constant two-object groupoid with `d theta=0`.  One
canonical `P`-half attachment therefore generates its conjugate `S` half;
central `K_Eq`, physical `q`, and the ridge/eta/sigma rows transport
objectwise.  The shortest open datum is one source-labelled `P`-half cap
attachment with its full principal companion.

Checker:

```text
computations/verify_h3_centered_shear_cylinder_curvature_physical_output_gate.py
```

Frozen ledger digest:

```text
ffda8f30e304b5038c3b4c12b28e848f60cf2d6b1badd4ae8cd3d378a229fa29
```

## 1. Exact local character and grade

Write the fixed-endpoint Segre block as

\[
 (Aq_0,Aq_1,Aq_2,Bq_0,Bq_1,Bq_2).
\]

The three toric characters span a rank-two module.  For example,

\[
 \xi_{01}=(-1,1,0,1,-1,0).
\]

They annihilate all endpoint row sums and matching column sums.  Hence the
local representation is exactly

\[
 \text{endpoint-odd}\otimes\text{matching-standard}.              \tag{2}
\]

The global covariant orbit has rank thirty.

For the prototype,

\[
 k=(p_1@1^1s_1@0^1-p_1@0^1s_1@1^1)
   (q_{23}^{00}q_{45}^{00}-q_{24}^{00}q_{35}^{00}). \tag{3}
\]

Every term of (3) has word `110000`, unary/edge bidegree `(2,2)`, and no
offdiagonal edge decoration.  Its parent toric relation is homogeneous in
the literal doubled multidegree

```text
p1@0^1 s1@1^1 p1@1^1 s1@0^1
q23:00 q45:00 q24:00 q35:00,
```

with site word `220000`.  The cylinder proper face carries the corresponding
parameter-labelled first-PP grade.  It is not an unlabelled scalar output.

## 2. Why the private-site rows do not realize it

The physical private-site identity starts from a decorated offdiagonal cell

\[
 e=A_{vu}^{ba},\qquad a\ne b,
\]

and supplies an active term `Delta_us C_s`.  At `h=3` that product has four
edge-coefficient factors and no unary factor.  More decisively, it contains
the chosen offdiagonal reference/mixed edge.

Specialize all six offdiagonal decorated edge types to zero and retain the
diagonal/unary values

```text
p1@1=2, s1@0=3, p1@0=1, s1@1=5,
q23:00=7, q45:00=11, q24:00=13, q35:00=17.
```

Then every offdiagonal private-site active term is zero, whereas (3) equals
`-144`.  This proves nonmembership in the literal offdiagonal/cofactor
family without assuming a generic support census.

The only route from (3) to that family remains the open incidence square:

```text
endpoint unary wedge       -> decorated offdiagonal edge,
matching-standard q split  -> its physical cofactor.
```

Coefficient factorization is not this source-labelled map.

## 3. The exact target-word obstruction

The selected source object is `G11[110000]`.  Its GHZ target coefficient is
zero because `110000` is mixed.  The exact endpoint target-normal support is

```text
8 words with two selected ones,
8 complementary words with two selected zeros,
000000 and 111111,
```

for eighteen words total.  It does not contain `110000`.  The moving D4
orbit likewise has target profile

```text
0,0,0,0,1
```

from `110000` to `111111`.

Therefore the artificial cylinder coordinate `t` in `d epsilon=L-t` is not
already an object of the source word.  Source-ring multiplication acts on a
target basis object; it does not create a missing target basis word.  A
word-changing endpoint/D4/cap comparison must first place that object.  Once
it does, the whole mixed target family follows by homogeneous multiplication;
there is no further target-module theorem.

## 4. What `A`-module multiplication really proves

Suppose conditionally that `T=A t` is a genuine graded target module and
that `t` has already been placed in the required grade.  Then `k t` is
indeed a legal codomain element.  This does not prove it is nonzero in the
terminal cokernel.

A physical target normal arrives with a principal source companion.  In
the two coordinates

```text
(k*principal companion, k*target),
```

the full Macaulay column, desired pure target, and primitive dual are

```text
full column   (1,1)
pure target   (0,1)
dual         (-1,1).
```

The dual kills the full column and reads one on pure target.  Equivalently,
`k t` is in the old image if and only if the source companion `k s` can be
cancelled in the identical grade.  Multiplying by `k` is legitimate; dropping
`k s` is not.

This is the sharp local complete-output dual before cap placement.  With the
physical cap graph

```text
T+rho = (target,ordinary residue)=(1,1),
```

the multiple `-k(T+rho)` cancels the target curvature and leaves

```text
(target,ordinary residue)=(0,-k).
```

In the four-corner order

```text
(P+q00,P-q00,P+q11,P-q11),
```

this residue is `-delta=(-1,+1,+1,-1)`.  The committed physical endpoint-odd
Cartan cell `K` carries this same `-delta`, zero protected
`D,W,target,anchor,Eq`, and the commuting shifted ridge.  Use the equally
physical oppositely oriented cell `-K`, which carries `delta`.  Hence the
coefficient-level sum closes:

```text
cylinder        (target,residue) = (+k, 0)
-k(T+rho)                          (-k,-k)
negative Cartan -K                  ( 0,+k)
sum                                  ( 0, 0).
```

What is not yet supplied is the comparison placing all three terms in one
word/fine/repeated grade.

## 5. Exact remaining grade transport

The cylinder starts in the mixed `G11[110000]` occurrence block.  The
orbit-relative D4 cube transports pure-`00` occurrence tags from `110000`
to `111111`, changing the selected tail from

```text
q24:00 q35:00  ->  q24:11 q35:11.
```

The physical Cartan comparison lives after cap/root insertion in word
`01211222`—rootless `1211222`—and repeated grade `P3+K2`, with its second
tail

```text
q24:21 q35:12.
```

The displayed tail is one of two matching packets.  Writing
`M0=q23*q45` and `M1=q24*q35`, the full endpoint-odd residue is

```text
(M1^11-M1^decorated) - (M0^11-M0^decorated).
```

The two packets have disjoint matching labels and rank two.  Physical Cartan
descent is matching-covariant and supplies both once the canonical grade is
reached.  This is coefficient- and sign-exact evidence for the proposed
composition, but the existing D4 cube and Cartan theorem are separate source
objects.
The cap graph is physical in its own
`01211222 / t*q_(v,N) / P3+K2` object; it is only formally horizontal over
the response/D4 cube.  Thus D4 followed by Cartan does **not yet prove** the
cross-word chain map.

The sole grade clause is:

> Place the cap target graph as a horizontal source-labelled object across
> the response/D4 word change, so its pure-`11` top tail is the `q00` corner
> of the physical Cartan square and its `1<->2` tail transport is the `q11`
> corner.

After this clause, homogeneous multiplication cancels `t*k`, negative
Physical Cartan descent cancels `-k` residue, and the ridge theorem supplies
eta/sigma.

## 6. The transpose groupoid removes the second half

Let `g` be the canonical `P`-tail grade and `gT` its endpoint-transpose
`S`-tail grade.  The literal source involution is

```text
theta = [[0,1],[1,0]],  theta^2=1,  d theta=0.
```

It transports physical `q`, target, `W`, ordinary residue, ridge, eta and
sigma exactly, while `K_Eq` is central and objectwise.  Therefore one
source-labelled attachment at `g` has a forced attachment at `gT`; there is
no independent conjugate-grade comparison or holonomy class.

Combining this with the D4--Cartan bridge gives the shortest local theorem:

> Construct one canonical `P`-half cross-word cap attachment, including its
> full principal companion and its `ainc/q,W` values.  Apply `theta` for the
> `S` half, the central `K_Eq` cone objectwise, and the committed negative
> Cartan/ridge packet for residue and terminal closure.

## 7. Additional rows needed for promotion

The mixed character already has zero aggregate endpoint, matching, formal
anchor-incidence, and aggregate physical-`q` shadows.  Those zeros do not
define the missing augmented cell.  A positive construction of the one
canonical `P` half must carry:

1. the same-grade cross-word cap placement just stated;
2. the full principal/cap companion in the doubled grade;
3. an occurrence-local `ainc` value, hence physical `q=M-ainc`;
4. `W` on the same source-labelled cell.

The `S` half is then its `theta` image.  Ordinary residue is the already
constructed physical Cartan face, not a new generator.  Central `K_Eq` is
objectwise; the labelled shifted ridge is already part of the Cartan packet;
and eta/sigma are uniquely transported by the committed contraction law.
The missing cross-word placement must preserve these packets rather than
reconstruct their rows independently.

The dual alternative must annihilate all the same rows and every admitted
Macaulay multiplier while retaining its nonzero target-curvature pairing.
At present `(-1,+1)` is exact only in the local
companion/target quotient; its fully augmented physical extension remains
open.

## Scope

This is exact for the canonical `h=3` fixed-endpoint Segre response block.
It does not construct the one canonical `P`-half cross-word cap comparison,
its full companion, or its `ainc/q,W` values.  It proves that target
multiplication, the `S` half, ordinary residue, central `K_Eq`, and terminal
ridge transport are not independent new theorems after that attachment.

## Verification

Run normally, optimized, and isolated/no-site.  Expected headline:

```text
t*k offdiagonal/private-site landing: NO (literal grade mismatch)
A-module target cancellation: YES after cross-word cap placement
post-cap debt: -k residue = residual-q four-corner character
remaining face: one P-half cap placement; theta supplies S half
```
