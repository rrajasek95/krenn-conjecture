# A three-site selector exposes a double Macaulay jet, but the off-diagonal rows have only a hexagon

## 1. Outcome

Let \(W\) have \(2h\) sites, \(h\geq3\), and assume the complete pair
equations

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                              \tag{1}
\]

On a canonical rootless line, write \(\sigma=\sigma(K)\),
\(r=r(K)=\sum K_{ij}p_i s_j\), and

\[
 {\cal E}(K)=\sum_{j=2}^{h}\sigma^{h-j}q^{[h-j]}r^{[j]}.
                                                               \tag{2}
\]

The audited full-nine closure gives a three-site selector at each
injective endpoint.  This note records the exact incidence consequence of
one such selector and tests the suggested fixed-label rectangle mechanism.

There are two conclusions.

1.  Let \(A\subset W\) be the three sites of either endpoint selector.
    At \(x\in A\), quotient the local physical space by the span of **all
    six** endpoint-star values at \(x\).  In the resulting top-tensor
    quotient, the clean error is divisible by \(\sigma^2\).  Consequently
    the unexposed part of its degree-\(h\) Macaulay matrix has rank at most
    \(2h-2\).  Every nonzero \(2h\)-column minor therefore uses at least two
    selector-exposed columns.  Equivalently, rootlessness forces those
    exposed columns to surject onto the two-dimensional first-jet quotient

    \[
       J_2=\operatorname {Sym}^{2h-1}\mathbb C^2/
       \sigma^2\operatorname {Sym}^{2h-3}\mathbb C^2.          \tag{3}
    \]

    At \(h=3\), the unexposed clean error is identically zero.  The whole
    rank-six certificate is carried by the selector-exposed tensor
    subspace.  This incidence does **not** kill the minor: the nonzero
    scalar-zero packet automatically makes one exposed coefficient block
    surject onto (3).
2.  The six off-diagonal equations in (1) cannot supply the two exposed
    dependencies by a type-3-style \(2\times2\) rectangle.  After the
    natural normalization, they are indexed by the zero-diagonal subspace
    of \(3\times3\) matrices.  That subspace contains no product rectangle
    \(U\otimes V\) with \(\dim U,\dim V\geq2\).  An oblique selector change
    imports the three diagonal target anchors instead of repairing this.
    The only support-free source-index relation among the six off-diagonal
    products is the cubic six-cycle, or hexagon, relation (15) below.

The double-jet incidence is sharp as linear algebra and is automatically
saturated by the physical nonnilpotence \(r_*^{[h]}\ne0\).  A family
divisible by \(\sigma^2\), together with one exposed degree-\(h\) form
which is nonzero at the scalar-zero point, can still have full Macaulay
rank.  A literal six-site response guard in Section 6 has
coordinate-compatible selectors, satisfies all six off-diagonal rows, obeys
the hexagon, and has the two coprime clean coordinates \(u^3,v^3\).  It
fails exactly the three diagonal target anchors, so it is not a source.

Thus “every full minor meets the selector” is the wrong closing statement:
the required meeting is forced, but the scalar-zero packet fills precisely
the missing jet directions.  After choosing one exposed scalar coefficient
\(f\) with \(f(K_*)\ne0\), the exact residual is the \(h\)-dimensional
quotient

\[
 \operatorname {Sym}^{2h-1}\mathbb C^2/
        f\operatorname {Sym}^{h-1}\mathbb C^2.                  \tag{3a}
\]

At \(h=3\) this is a three-dimensional residual.  The off-diagonal
annihilator rows and their cyclic Koszul relation impose no rank loss on
it.  A positive proof has to feed at least one literal diagonal target row
through a coefficient cut such as the audited four-cut ledger.

## 2. The normalized full-nine quadratics

Put

\[
                 B_{ij}=p_i s_j+{a_{ij}\over h}q.                \tag{4}
\]

The divided-power identity \(q q^{[h-1]}=h q^{[h]}\) turns all nine pair
equations into

\[
                 B_{ij}q^{[h-1]}=\delta_{ij}X_i.                \tag{5}
\]

Hence the six \(B_{ij}\), \(i\ne j\), lie in
\(\operatorname {Ann}(q^{[h-1]})\), while the three diagonal cells are
literal, independently labelled anchors.  This is the correct normalization
for testing a rectangle: no direct term has been dropped, and no common
power has been cancelled.

Let \(R,S\in\operatorname {GL}_3(\mathbb C)\), and define oblique endpoint
rows

\[
 \widetilde p_k=\sum_iR_{ki}p_i,
 \qquad
 \widetilde s_l=\sum_jS_{lj}s_j.                              \tag{6}
\]

The corresponding transformed source-provenant quadratic is

\[
 \widetilde B_{kl}
 =\widetilde p_k\widetilde s_l
   +{(RaS^{\mathsf T})_{kl}\over h}q
 =\sum_{i,j}R_{ki}S_{lj}B_{ij}.                               \tag{7}
\]

Multiplying by the common power and using (5) gives the fixed-label
identity

\[
 \boxed{
 \widetilde B_{kl}q^{[h-1]}
       =\sum_{i=0}^2R_{ki}S_{li}X_i.}                          \tag{8}
\]

Since \(X_0,X_1,X_2\) are independent, the transformed cell is an
annihilator exactly when

\[
                         R_{ki}S_{li}=0\qquad(i=0,1,2).         \tag{9}
\]

Thus oblique selector coordinates do not turn the off-diagonal six-cycle
into a target-free rectangle.  Formula (8) is also the precise point at
which the type-3 proof cannot be copied: there the annihilator-plane
identity forced an oblique two-plane to become one fixed coordinate plane;
here no such flag has occurred, and all three anchors remain visible.

## 3. There is no fixed-label \(2\times2\) annihilator rectangle

Let \(C,D\cong\mathbb C^3\) have the fixed row and column labels, and put

\[
 Z=\operatorname {span}\{E_{ij}:i\ne j\}
       \subset C^*\otimes D^*.                                \tag{10}
\]

This is the zero-diagonal coefficient space of the six annihilator cells.

**Lemma 3.1 (zero-diagonal product spaces).**  If
\(U\subset C^*\), \(V\subset D^*\), and \(U\otimes V\subset Z\), then

\[
                         \dim U+\dim V\leq3.                   \tag{11}
\]

In particular, \(Z\) contains no \(2\times2\) product rectangle.

**Proof.**  For a subspace \(U\), let

\[
 I(U)=\{i:\text{some }u\in U\text{ has }u_i\ne0\}.
\]

If \(i\in I(U)\cap I(V)\), choose \(u\in U,v\in V\) with
\(u_i v_i\ne0\).  The rank-one matrix \(u\otimes v\) then has a nonzero
\((i,i)\)-entry, contrary to \(U\otimes V\subset Z\).  Hence
\(I(U)\cap I(V)=\varnothing\).  Moreover
\(\dim U\leq|I(U)|\) and \(\dim V\leq|I(V)|\).  Their disjoint union is
contained in a three-set, proving (11).  \(\square\)

The lemma applies after arbitrary independent selector changes.  Indeed,
the row spans of any proposed \(2\times2\) transformed rectangle would be
two-dimensional spaces \(U,V\) satisfying (9) for every pair of rows,
equivalently \(U\otimes V\subset Z\), which Lemma 3.1 forbids.

There is an equally concrete source-level way to see the contamination.
Keeping only the six off-diagonal cells in (7) gives

\[
 \sum_{i\ne j}R_{ki}S_{lj}p_i s_j
 =\widetilde p_k\widetilde s_l
   -\sum_iR_{ki}S_{li}p_i s_i.                                \tag{12}
\]

The last sum is exactly the missing diagonal channel.  Adding it back
restores a product but changes its common-power row from zero to the three
independent targets in (8).  No scalar cancellation among the labels is
available.

## 4. The natural cyclic replacement is only the hexagon syzygy

Write \(b_{ij}=a_{ij}/h\) and

\[
                         x_{ij}=B_{ij}-b_{ij}q=p_i s_j.          \tag{13}
\]

Commutativity gives the universal six-cycle identity

\[
                  x_{01}x_{12}x_{20}=x_{02}x_{21}x_{10},       \tag{14}
\]

because both sides are
\(p_0p_1p_2s_0s_1s_2\).  In the normalized physical cells this is

\[
\boxed{
 \begin{aligned}
 &(B_{01}-b_{01}q)(B_{12}-b_{12}q)(B_{20}-b_{20}q)\\
 &\qquad=(B_{02}-b_{02}q)(B_{21}-b_{21}q)(B_{10}-b_{10}q).
 \end{aligned}}                                                \tag{15}
\]

This is precisely the proposed cyclic/Koszul replacement for a rectangle.
It is also the only support-free Segre relation among the six unshifted
products.  Indeed, in the polynomial ring on formal \(P_i,S_j\), the map

\[
 \mathbb C[z_{ij}:i\ne j]\longrightarrow
 \mathbb C[P_0,P_1,P_2,S_0,S_1,S_2],
 \qquad z_{ij}\longmapsto P_iS_j                              \tag{16}
\]

is the edge map of the bipartite six-cycle
\(K_{3,3}\setminus\{00,11,22\}\).  An equality of two monomials has an
integer exponent difference with zero sum at every one of its six
vertices.  Walking once around the cycle forces that difference to be a
multiple of the alternating cycle vector.  Hence the kernel lattice has
rank one and its primitive binomial is (14).  Further relations in the
site-square-zero algebra must therefore use actual site incidence,
top-degree truncation, or the common quadratic; they are not consequences
of the six source labels alone.

Equation (15) does not give a linear Macaulay constraint.  It is cubic in
quadratics and is true before (5) is used.  At \(h=3\) it is already a
top-degree tautology; at higher order, multiplying it by a common power
keeps it a tautology.  The diagonal anchors cannot be inserted by simply
multiplying (5): every \(X_i\) is top degree, so \(X_iZ=0\) for every
positive-degree \(Z\).  Such a multiplication turns both sides into zero.
To make a diagonal anchor interact nontrivially with (15), one must first
take literal site coefficients, where the product rule produces the
four-cut rows.  There is no uncontracted three-anchor cancellation.

## 5. The selector-exposure filtration and the double jet

The failure of the rectangle does not make selectors invisible.  They
give the following uniform incidence theorem.

For a site \(x\), let

\[
 U_x=\operatorname {span}\{p_{0,x},p_{1,x},p_{2,x},
                            s_{0,x},s_{1,x},s_{2,x}\}\subseteq V_x.
                                                                  \tag{17}
\]

For \(A\subseteq W\), let \(\Pi_A\) be the tensor product of the quotient
maps \(V_x\to V_x/U_x\) at \(x\in A\) and the identity maps elsewhere.
It is a homomorphism between the corresponding site-square-zero algebras.
Its kernel in top degree is the canonical exposed subspace

\[
 {\cal X}_A=\sum_{x\in A}
 U_x\otimes\bigotimes_{y\ne x}V_y.                            \tag{18}
\]

The use of the combined span \(U_x\), rather than only the selected
endpoint's image, is necessary: a response edge can place either named
endpoint star at \(x\).  Thus \(A\) comes from one endpoint selector, but
the local quotient is a combined-\(P,S\) quotient.  Quotienting only by
\(\operatorname {im}P_x\) would leave the terms in which the \(S\)-star
occupies \(x\), and the divisibility below would fail.

The map \(\Pi_A\) is not asserted to preserve the three target tensors.
Depending on the actual local star spans, \(\Pi_A(X_i)\) may survive,
change to a quotient-axis tensor, or vanish.  The construction is applied
only to the already audited target-free identity (2), which was derived
from the complete equations before taking any quotient.  It must not be
applied to (1) while silently replacing \(\Pi_A(X_i)\) by \(X_i\).

**Theorem 5.1 (selector-exposure divisibility).**  Let \(A\subseteq W\),
put \(t=|A|\) and \(d=\lceil t/2\rceil\).  On every physical cap line,

\[
             \Pi_A{\cal E}(u,v)=\sigma(u,v)^dG(u,v)             \tag{19}
\]

for a vector-valued binary form \(G\) of degree \(h-d\).  If
\(d>h-2\), the left side is identically zero.

**Proof.**  Reindex (2) by \(k=h-j\):

\[
 {\cal E}(K)=\sum_{k=0}^{h-2}
       \sigma(K)^kq^{[k]}r(K)^{[h-k]}.                         \tag{20}
\]

Every local factor of a response edge at \(x\in A\) belongs to \(U_x\).
Thus \(\Pi_A r(K)\) has no edge incident to any site of \(A\).  A
top-degree monomial in
\(\Pi_A(q^{[k]}r(K)^{[h-k]})\) would therefore have to cover all \(t\)
sites of \(A\) with its \(k\) quadratic \(q\)-edges.  This is impossible
when \(2k<t\).  Hence every term with \(k<d\) vanishes after the quotient,
and every remaining term in (20) contains \(\sigma^d\).  There are no
remaining terms when \(d>h-2\).  \(\square\)

Take \(A\) to be the three distinct sites of one Hall--Rado selector.  Then
\(d=2\).  Let \(L_{\rm un}\subseteq\operatorname {Sym}^h\mathbb C^2\)
be the span of the scalar coordinates of \(\Pi_A{\cal E}\).  Theorem 5.1
gives

\[
 L_{\rm un}\operatorname {Sym}^{h-1}\mathbb C^2
 \subseteq
 \sigma^2\operatorname {Sym}^{2h-3}\mathbb C^2,               \tag{21}
\]

and the space on the right has dimension \(2h-2\).

Choose any top-tensor basis adapted to
\({\cal X}_A\subseteq\bigotimes_{x\in W}V_x\).  Call the scalar coordinate
forms on \({\cal X}_A\) exposed and the quotient coordinates unexposed.
Equation (21) proves:

**Corollary 5.2 (two-column incidence).**  Every nonzero maximal minor of
the degree-\(h\) Macaulay matrix uses at least two shifted columns from
exposed coefficient forms.  If the whole Macaulay map has rank \(2h\),
the exposed columns surject onto the two-dimensional quotient \(J_2\) in
(3).

The statement is basis-free in its quotient form.  The language of
individual exposed columns refers to a basis adapted to (18); a generic
change of tensor coordinates mixes those columns and should not be read as
a literal support assertion in the fixed colour-word basis.

More generally, using the union of the two three-site selector sets gives
\(3\leq t\leq6\) and \(d=2\) or \(3\).  Every full minor then needs at
least \(d\) columns from the corresponding larger exposed subspace, and
those columns must span the \(d\)-dimensional \((d-1)\)-jet quotient

\[
 J_d=\operatorname {Sym}^{2h-1}\mathbb C^2/
       \sigma^d\operatorname {Sym}^{2h-d-1}\mathbb C^2.        \tag{22}
\]

At the first boundary \(h=3\), already one three-site selector has
\(d=2>h-2\).  Hence \(\Pi_A{\cal E}=0\): every rank-six certificate is
carried by the canonical exposed subspace (18).

There is a decisive limitation to this incidence.

**Proposition 5.3 (the scalar-zero packet fills the exposed jet).**  Let
\(K_*\) be the scalar-zero point, so \(\sigma(K_*)=0\), and suppose

\[
                         {\cal E}(K_*)=r_*^{[h]}\ne0.            \tag{22a}
\]

For any set \(A\) in Theorem 5.1 with \(d\leq h\), the exposed
multiplication columns surject onto \(J_d\).  In fact, one exposed scalar
coordinate form already does so.

**Proof.**  Equation (19) gives \(\Pi_A{\cal E}(K_*)=0\), so the nonzero
tensor (22a) lies in the exposed subspace \({\cal X}_A\).  In an adapted
basis, choose an exposed scalar coordinate \(f\) with
\(f(K_*)\ne0\).  Choose a binary linear form \(t\) independent of
\(\sigma\), with \(t(K_*)\ne0\).  For \(0\leq k<d\), consider the shifted
columns

\[
                  f\,\sigma^kt^{h-1-k}.                         \tag{22b}
\]

Modulo \(\sigma^d\), their orders at \(K_*\) are respectively
\(0,1,\ldots,d-1\), and their leading coefficients are all nonzero
multiples of \(f(K_*)\).  They therefore form a triangular basis of
\(J_d\).  \(\square\)

Thus the necessary jet surjectivity in Corollary 5.2 is not an additional
rootless burden.  It follows already from the nonnilpotent scalar-zero
packet.  Selector incidence reaches the correct columns, but it reaches
them at the one point where the packet guarantees that they repair the
Macaulay defect.

## 6. Sharp guards

### 6.1 The Macaulay incidence bound is sharp

Let \(\sigma,t\) be independent binary linear forms, and let
\(1\leq d\leq h\).  Take

\[
 L_{\rm un}=\sigma^d\operatorname {Sym}^{h-d}\mathbb C^2,
 \qquad g=t^h.                                                \tag{23}
\]

Then

\[
 L_{\rm un}\operatorname {Sym}^{h-1}
 =\sigma^d\operatorname {Sym}^{2h-d-1}                        \tag{24}
\]

has dimension \(2h-d\).  Also

\[
 g\operatorname {Sym}^{h-1}
 \cap \sigma^d\operatorname {Sym}^{2h-d-1}
 =\sigma^dt^h\operatorname {Sym}^{h-d-1},                     \tag{25}
\]

with dimension \(h-d\) (zero when \(d=h\)).  Therefore the sum of the
two multiplication images has dimension

\[
                    (2h-d)+h-(h-d)=2h.                         \tag{26}
\]

Equivalently, \(\sigma^h\in L_{\rm un}\) and \(t^h\) have nonzero
resultant.  Exactly \(d\) suitable shifts of the single exposed form
\(t^h\) fill the missing jet quotient.  Thus “every full minor meets the
selector exposure” is not itself a vanishing theorem; a physical syzygy
must lower the exposed jet rank.

### 6.2 Six off-diagonal rows and aligned selectors can still be rootless

The following six-site guard shows that the hexagon supplies no such
syzygy.  It is deliberately not a full-nine source.

Let

\[
 W=A\sqcup B,
 \qquad A=\{A_0,A_1,A_2\},\quad B=\{B_0,B_1,B_2\}.
\]

At \(A_k\) and \(B_k\), cyclically name the physical coordinate vectors

\[
 U_k=e_k,\qquad V_k=e_{k+1},\qquad Z_k=e_{k+2}
 \quad(\text{indices modulo }3).                              \tag{27}
\]

Define the first endpoint star, supported on \(A\), by

\[
 p_i|_{A_k}=\delta_{i0}U_k+\delta_{i2}V_k+\delta_{ik}Z_k,
 \qquad p_i|_B=0,                                             \tag{28}
\]

and the second, supported on \(B\), by

\[
 s_j|_{B_k}=\delta_{j1}U_k+\delta_{j2}V_k+\delta_{jk}Z_k,
 \qquad s_j|_A=0.                                             \tag{29}
\]

The three covectors \(Z_k^*\) pull the first star back to the three fixed
row coordinates, and do the same for the second star.  Thus both stars are
injective and have coordinate-compatible three-site selectors.

Set \(q=0\), let the direct matrix have sole nonzero entry \(a_{01}=1\),
and take

\[
                         K(u,v)=uE_{01}+vI.                     \tag{30}
\]

Its scalar is \(\sigma=u\), its response is
\(r(K)=\sum K_{ij}p_i s_j\), and its target is
\(T(K)=v(X_0+X_1+X_2)\).  The clean-error definition is

\[
                         {\cal E}(K)=r(K)^{[3]}-u^2T(K).        \tag{31}
\]

On the mixed physical word selecting \(U_k\) at every \(A_k,B_k\), every
scalarized \(A\)-row is the fixed row coordinate \(0\), every \(B\)-row
is coordinate \(1\), and the \(3\times3\) cross matrix of \(r(K)\) is
the all-\(u\) matrix.  Hence this clean coordinate is

\[
                              3!u^3.                            \tag{32}
\]

On the mixed word selecting all \(V_k\), both shores scalarize to row
coordinate \(2\), so the cross matrix is all \(v\) and the clean
coordinate is

\[
                              3!v^3.                            \tag{33}
\]

The target term vanishes on both words because the cyclic words are mixed.
Thus the vector cubic has gcd one, and its Macaulay matrix has rank six.

Since \(q^{[2]}=q^{[3]}=0\), all six off-diagonal instances of (1) hold
exactly.  The source products obey the hexagon (14), and the selectors are
already aligned with the fixed row labels.  The three diagonal equations
fail as \(0=X_i\).  This is an exact guard to any implication using only

\[
 \{\text{six off-diagonal annihilator rows},\
   \text{source factorization},\
   \text{three-site selectors},\
   \text{hexagon syzygy}\}
 \Longrightarrow \operatorname {rank}\mu_{\cal E}<6.          \tag{34}
\]

It does not guard a coefficient-cut argument which genuinely uses a
diagonal anchor.

## 7. Exact residual after the automatically filled jet

Proposition 5.3 rules out the tempting final step
“selector incidence forces the exposed jet to lose rank.”  The exposed jet
has full rank for the simplest possible reason: the scalar-zero packet is
nonzero.  The remaining Macaulay question can instead be stated after
removing that one known block.

Choose an exposed scalar coordinate form \(f\) with \(f(K_*)\ne0\), as in
Proposition 5.3, and put

\[
 Q_f=
 \operatorname {Sym}^{2h-1}\mathbb C^2/
 f\operatorname {Sym}^{h-1}\mathbb C^2.                       \tag{35}
\]

Multiplication by the nonzero degree-\(h\) form \(f\) is injective on
\(\operatorname {Sym}^{h-1}\), so \(Q_f\) has dimension \(h\).  Extend
\(f\) to a basis of the scalar-coordinate span and call the span of the
remaining basis forms \(L'\).  The full Macaulay map has rank \(2h\) if
and only if

\[
 L'\otimes\operatorname {Sym}^{h-1}\mathbb C^2
       \longrightarrow Q_f                                  \tag{36}
\]

is surjective.  This is just quotienting the \(2h\)-dimensional target by
the known \(h\)-dimensional block
\(f\operatorname {Sym}^{h-1}\).

The selector factor \(\sigma^d\) gives no further rank loss in (36).
Indeed \(f(K_*)\ne0\) says \(\gcd(f,\sigma)=1\).  For every
\(1\leq d\leq h\), multiplication by \(\sigma^d\) induces an isomorphism

\[
 \frac{\operatorname {Sym}^{2h-1-d}\mathbb C^2}
      {f\operatorname {Sym}^{h-1-d}\mathbb C^2}
 \ \xrightarrow{\ \cdot\sigma^d\ }\
 Q_f,                                                        \tag{37}
\]

where a symmetric power with negative exponent is zero.  Injectivity
follows from
\(f\mid\sigma^dg\Rightarrow f\mid g\); both sides have dimension \(h\).
Thus a common \(\sigma^d\) factor is a unit on the complementary
Macaulay quotient once the nonvanishing block \(f\) has been removed.
Equations (23)--(26) realize this statement sharply.

At \(h=3\), the residual (36) is only three-dimensional, but all its
potential generators are selector-exposed because \(\Pi_A{\cal E}=0\).
A sufficient positive lemma is now the exact rank bound

\[
 \boxed{\operatorname {rank}\bigl(
 L'\operatorname {Sym}^{2}\longrightarrow Q_f\bigr)\leq2.}    \tag{38}
\]

Uniformly, the analogous bound is at most \(h-1\).  Unlike the false
exposed-jet bound, (38) is not contradicted merely by
\(r_*^{[h]}\ne0\).

Lemma 3.1, the hexagon calculation, and the guard prove that (38) cannot
come from the six off-diagonal rows alone.  Formula (8) identifies the
missing input exactly: a proof must retain a nonzero coefficient of at
least one of \(X_0,X_1,X_2\) while taking selector-adapted site
coefficients.  The literal two-site/four-cut equations are designed to do
this; multiplying the uncontracted top rows is not.

This is the narrow residual left by the selector--Macaulay attack: after
the scalar-zero coefficient supplies one full \(h\)-column block, rule out
surjectivity onto the complementary \(h\)-space using a fixed diagonal
anchor.  At the first boundary it is a rank-three quotient problem, not a
support-mask enumeration and not a \(6\times6\) determinant census.
