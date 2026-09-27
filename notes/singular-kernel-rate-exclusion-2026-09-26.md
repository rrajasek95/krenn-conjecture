# A full complex exclusion around a singular response

September 26, 2026. **Written research supported by an exact rational matrix
certificate; awaiting independent audit.**

[Explainer](../explainers/RATE-DESIGN-FRONTIER.md) ·
[Exact replay](../computations/rate-design-frontier-2026-09-26/README.md)

The earlier two-versus-four exclusion required an injective response. Here
the response has a nine-dimensional kernel. A second-order estimate controls
that kernel and excludes a full neighborhood, allowing all 135 complex cells.
This is one new boundary class, not a classification of all singular limits.

## 1. Base source and theorem

Split the sites into \(\{0,1\}\) and \(\{2,3,4,5\}\). Write \(B\)
for the eight crossing blocks, \(D\) for the six blocks within the four-site
side, and \(Z=A_{01}\). As before,

\[
 H=L_B(D)+Z\otimes H_4(D).                          \tag{1}
\]

At the base \(B_0\), put

\[
 B_{02}=B_{03}=B_{04}=B_{05}=B_{12}=B_{13}=I_3,
 \qquad B_{14}=B_{15}=0.
\]

Set \(D_0=0\). There is no perfect matching at this base and its output is
zero, independently of \(Z\). Its crossing squared norm is 18.

**Theorem.** If

\[
 \|B-B_0\|\le10^{-3},\qquad \|D\|\le10^{-3},\qquad \|Z\|\le1,
\]

then every nonzero output obeys

\[
 \boxed{F\le(82/93)^2=6724/8649<4/5.}               \tag{2}
\]

Norms are Euclidean on source cells. In particular, formerly zero blocks
\(B_{14},B_{15}\) may be arbitrary complex perturbations. They are not
required to stay zero.

At the six root choices, the old response/augmented ranks are
\((0,3),(0,3),(6,9),(6,9),(9,12),(9,12)\). All pass the previous
necessary rank filter. The map \(L_{B_0}\) has rank 45, so the old
injectivity exclusion does not apply either.

## 2. Separate the kernel and the newly opened edges

Decompose \(D=K+V\), with \(K\) supported on edge 23 and \(V_{23}=0\).
The exact matrix certificate proves

\[
 \ker L_{B_0}=\{K:K\text{ is supported on }23\},\qquad
 \|L_{B_0}V\|\ge2\|V\|.                           \tag{3}
\]

Let \(U=(B_{14},B_{15})\), and write \(k=\|K\|\), \(v=\|V\|\),
\(u=\|U\|\). The leading output produced by a kernel direction and
these newly opened edges is the bilinear tensor

\[
 \mathcal M(K,U)=K_{23}\otimes
        (I_{04}\otimes U_{15}+I_{05}\otimes U_{14}),               \tag{4}
\]

with tensor factors placed at their named sites. Direct contraction gives

\[
 \|I_{04}\otimes U_{15}+I_{05}\otimes U_{14}\|^2
 =3\|U_{14}\|^2+3\|U_{15}\|^2
      +2\operatorname{Re}\langle U_{14},U_{15}\rangle
 \le4u^2.
\]

Thus \(\|\mathcal M(K,U)\|\le2ku\).
Let \(P_L\) project onto \(\operatorname{im}L_{B_0}\). The critical
new lower bound is

\[
 \boxed{\|(I-P_L)\mathcal M(K,U)\|\ge ku.}          \tag{5}
\]

It holds for every complex \(K,U\), including arbitrary phases.

## 3. Why a matrix certificate proves the bilinear lower bound

Flatten \(K\) and \(U\) into vectors of dimensions 9 and 18. The linear
map on their formal tensor product is a real integer matrix
\(M:\mathbb C^{162}\to\mathbb C^{729}\). Set

\[
 J=M^*(I-P_L)M.
\]

For pairs of indices \((i,a),(j,b)\), define the partial transpose
\(J^\Gamma_{ia,jb}=J_{ja,ib}\). The exact certificate proves

\[
                             J^\Gamma-I_{162}\succeq0.           \tag{6}
\]

For a product vector, the elementary index identity is

\[
 (K\otimes U)^*J(K\otimes U)
 =(\overline K\otimes U)^*J^\Gamma(\overline K\otimes U).
\]

Equation (6) therefore implies (5). This step uses the fact that the
coefficients are products of an actual kernel vector and actual opening
edges. It would be false to claim \(J\succeq I\) on all 162 formal
coefficients; \(J\) has a kernel. The replay rejects that stronger claim.

The checker reconstructs \(L,M\) from their integer entries, verifies the
normal equations for the projection, and checks (6) by exact Schur pivots.
No numerical eigenvalue is used to accept positivity.

## 4. The enlarged output space still misses the target

Put \(Y=L_{B_0}V+\mathcal M(K,U)\). From (5),
\(\|Y\|\ge ku\). From (3) and the upper bound after (4),

\[
 2v\le\|L_{B_0}V\|\le\|Y\|+2ku\le3\|Y\|.       \tag{7}
\]

The certificate also computes the orthogonal projection of
\(\Delta=a^6+b^6+c^6\) onto the *linear span* of both maps \([L_{B_0},M]\).
Its squared norm is exactly \(33/20\). Since \(\|\Delta\|^2=3\),

\[
 F(Y)\le11/20,
 \qquad |\langle g,Y\rangle|\le\sqrt{11/20}\|Y\|<\tfrac34\|Y\|.
                                                               \tag{8}
\]

Enlarging from actual bilinear products to their linear span only makes this
upper bound more conservative. Equations (5) and (8) play different roles:
the first prevents the leading terms from cancelling to zero, and the second
keeps their direction away from the target.

## 5. Control every higher-order perturbation

Let \(\eta=10^{-3}\). The matching expansion gives

\[
 \|(L_B-L_{B_0})V\|
 \le2\sqrt6(2\sqrt{18}+\eta)\eta v<43\eta v.       \tag{9}
\]

For the kernel component, replacing the fixed \(I_{04},I_{05}\) in (4)
by their actual blocks costs at most \(\eta ku\), by Cauchy–Schwarz.
There is no other kernel term: a retained edge 23 leaves sites 4 and 5
to be matched to roots 0 and 1.

Finally \(H_4(K)=0\), since a single edge cannot match four sites.
Each of the three four-site matchings has derivative norm at most
\(\|D\|\|V\|\). Integrating along \(K+tV\), and using orthogonality
of \(K,V\), proves
\(\|H_4(K+V)\|\le3\|D\|v\le3\eta v\).
Thus (1), (7), and (9) give

\[
 \|H-Y\|\le46\eta v+\eta ku\le70\eta\|Y\|.       \tag{10}
\]

If \(Y=0\), equations (7)–(10) give \(H=0\). Otherwise combine (8)
and (10), dividing by \(\|H\|\ge(1-70\eta)\|Y\|\), to obtain (2).
This controls arbitrary complex perturbations, not only analytic paths or
a finite Taylor expansion.

## 6. What this changes

A singular response does not automatically leave higher-order escape routes.
Here a positive matrix after an index swap bounds the bilinear kernel
contribution, and the enlarged response space retains a strict fidelity gap.
The method supplies a new route to testing other singular boundaries.

This one class is now excluded. Other kernels may contain directions whose
bilinear output cancels or whose enlarged image reaches the target. The
unrestricted diagonal and full-complex square-root problems remain open.
