# Global cap spans and the exact Veronese descent test

## 1. Outcome

All caps of a hypothetical large source produce ordinary six-site edge
families, not merely top-order boundary tensors.  For a six-set `U`, its
complement `W`, and an arbitrary covector `K` on `W`, the relevant edge on
`uv subset U` is the contracted hafnian cofactor

\[
 A^{U,K}_{uv}=K\mathbin{\lrcorner}H_{W\cup\{u,v\}}(X).   \tag{1}
\]

After identifying several six-sets with one abstract six-set, every linear
combination of the families (1) is a legitimate six-site aggregate source.
This turns the global reduction question into an exact finite algebraic
test.  If

\[
 f_c(y)=H_6\left(\sum_{j=1}^r y_jA_j\right)_c,
 \quad
 J=(f_c:c\text{ mixed}),
 \quad
 h=\prod_{i=0}^2f_{i^6},                                  \tag{2}
\]

then the cap span contains a ternary six-site target, up to one-site
diagonal normalization, if and only if

\[
                   J:h^\infty\ne(1),
 \qquad\text{equivalently}\qquad h\notin\sqrt J.          \tag{3}
\]

Geometrically, the kernel of the mixed cubic polarization must meet the
cubic Veronese variety away from the three pure hypersurfaces.  For a
two-family span this specializes to the mixed-gcd criterion in
`cross-pair-pencil-cancellation.md`.

Condition (3) is not automatic even when the desired GHZ contraction is
exact at tensor level.  The canonical gluing of two ternary four-site GHZ
sources gives a four-dimensional **linear** prism family

\[
 H_6(D(a,z_0,z_1,z_2))
   =a^2\sum_{i=0}^2z_i e_i^{\otimes6}
       +z_0z_1z_2e_{012012}.                              \tag{4}
\]

Here `J=(z_0z_1z_2)` and
`h=a^6z_0z_1z_2`, so `J:h^infinity=(1)`.  On a generic affine
pencil, the three roots of the mixed gcd kill the three pure coefficients
one at a time.  This is the sharp ternary root-cover obstruction and shows
that merely forcing a common mixed root is insufficient.

The exact audit is
`computations/verify_global_cap_span_descent.py`.

## 2. Contracted hafnian cofactors are the boundary pair family

Let `B=U disjoint-union W`, where `|U|=6` and `|W|` is even.  Let `X_uv`
be arbitrary ordered aggregate edge tensors and let

\[
 K\in\left(\bigotimes_{w\in W}V_w\right)^*.              \tag{5}
\]

No product or nondegeneracy assumption on `K` is needed.  Define the
complete capped boundary signature

\[
 F^K_S=K\mathbin{\lrcorner}H_{W\cup S}(X)
       \quad(S\subseteq U,\ |S|\text{ even}),             \tag{6}
\]

where only edges induced by `W union S` occur in the hafnian.  In
particular,

\[
 s_K=F^K_\varnothing=K\mathbin{\lrcorner}H_W(X),
 \qquad A^{U,K}_{uv}=F^K_{\{u,v\}}.                       \tag{7}
\]

**Lemma 2.1 (cofactor form of the cap family).**  Equation (1) is exactly
the degree-two component of the full boundary signature.  More explicitly,

\[
 A^{U,K}_{uv}=s_KX_{uv}
 +K\mathbin{\lrcorner}
   \sum_{p\ne q\in W}X_{up}X_{vq}
       H_{W\setminus\{p,q\}}(X),                         \tag{8}
\]

where the ordered sum and endpoint slots are interpreted literally.

**Proof.**  In a perfect matching of `W union {u,v}`, either `u,v` are
matched to each other, leaving a matching of `W`, or they are matched to
two distinct vertices `p,q` of `W`, leaving a matching of
`W-{p,q}`.  These alternatives are disjoint and exhaustive.  Contracting
the `W` slots gives (8), while (6) gives (1). `QED`

If the original source is exact,

\[
                         H_B(X)=\Delta_{B,3},             \tag{9}
\]

then every cap also satisfies the full top contraction identity

\[
 F^K_U=K\mathbin{\lrcorner}H_B(X)
      =\sum_{i=0}^2K(e_i^{\otimes W})e_i^{\otimes U}.    \tag{10}
\]

Thus (1) and (10) are coupled polynomial data from the same edge family.
For a product cap `K= tensor_(w in W) ell_w`, the three coefficients in
(10) are `prod_w ell_w(e_i)`, but the cofactor construction and the descent
test allow arbitrary entangled `K` as well.

## 3. The finite cap-span theorem

Fix an abstract ordered six-set `Q`.  Choose finitely many cap data
`(U_j,K_j)` and color-preserving bijections `Q -> U_j`; use those
bijections to pull (1) back to edge families `A_j` on `Q`.  Put

\[
             A(y)=\sum_{j=1}^r y_jA_j.                   \tag{11}
\]

Every entry of `A(y)` is an arbitrary `3 by 3` aggregate matrix, so (11)
is an ordinary six-site source for each `y in C^r`.  Since a six-site
matching uses three edges, the coefficients `f_c` in (2) are homogeneous
cubics.

**Theorem 3.1 (cap-span saturation criterion).**  The following are
equivalent.

1. Some `y in C^r` satisfies `f_c(y)=0` for every mixed coloring and
   `f_{i^6}(y) ne 0` for all three colors.
2. `V(J)` meets the principal open set `D(h)`.
3. `J:h^infinity` is a proper ideal.
4. `h` is not in the radical of `J`.

Whenever these conditions hold, (11), followed by an invertible diagonal
change at one site, realizes `Delta_(6,3)`.

**Proof.**  The equivalence of the first two statements is the definition
of `J` and `h`.  Over `C`, the localization `(C[y]/J)_h` is nonzero exactly
when `V(J)` meets `D(h)`.  This is equivalent to the contraction
`J:h^infinity` being proper, and also to no power of `h` belonging to `J`,
which by the Nullstellensatz is `h notin sqrt(J)`.

At a point in `V(J) cap D(h)`, write

\[
 H_6(A(y))=\sum_{i=0}^2d_i e_i^{\otimes6},\qquad d_i\ne0.\tag{12}
\]

Multiplying every edge entry incident to one fixed site in color `i` by
`d_i^(-1)` multiplies every matching coefficient with that site colored
`i` by the same scalar.  It sends (12) to `Delta_(6,3)`. `QED`

There is an equivalent coordinate-free formulation.  Let

\[
 \mu_{\rm mix}:\operatorname{Sym}^3(C^r)\longrightarrow
       \operatorname{span}\{e_c:c\text{ mixed}\}        \tag{13}
\]

be the polarization of the mixed part of `H_6(A(y))`, and let
`nu_3:P^(r-1)->P(Sym^3 C^r)` be the cubic Veronese map.  Then (3) says

\[
 \text{there is }[y]\in P^{r-1}\text{ with }
 \nu_3([y])\in P(\ker\mu_{\rm mix})
 \quad\text{and}\quad h(y)\ne0.                         \tag{14}
\]

This separates the two genuinely different issues: global contraction
identities may put non-decomposable symmetric tensors in
`ker(mu_mix)`, but an ordinary six-site source requires a decomposable cube
`y^3` in that kernel.

**Corollary 3.2 (conditional uniform descent).**  If an exact ternary
source of any even order `n>=8` has a finite collection of cap cofactors
whose ideal satisfies (3), then it yields an exact ternary six-site source.
Consequently it contradicts the established six-site obstruction.

This is a finite, exact condition: a witness is either an explicit point
`y`, or a Groebner/saturation computation proving that the localized ideal
is proper.  The missing uniform theorem is now precise: prove that at least
one cap-generated span of every hypothetical larger source satisfies (3).

## 4. The sharp ternary root-cover family

Take sites `(x_0,x_1,x_2,y_0,y_1,y_2)`.  For each
`{i,j,k}={0,1,2}`, put `a e_i e_i` on both triangle edges `x_jx_k` and
`y_jy_k`, and put `z_i e_i e_i` on the spoke `x_i y_i`.  These nine
rank-one entries depend linearly on `(a,z_0,z_1,z_2)`.

There are exactly four supported perfect matchings.  The matching using
spoke `x_i y_i` and the two opposite triangle edges has constant color `i`
and weight `a^2z_i`.  The three-spoke matching has word `012012` and weight
`z_0z_1z_2`.  This proves (4), including the assertion that all other 725
mixed fibers vanish.

The mixed and pure data are therefore

\[
 J=(z_0z_1z_2),\qquad
 h=(a^2z_0)(a^2z_1)(a^2z_2)=a^6z_0z_1z_2.               \tag{15}
\]

Because `h in J`, the saturation in (3) is the unit ideal.  The obstruction
is set-theoretically transparent: killing the only mixed coefficient forces
some `z_i=0`, which kills the corresponding pure coefficient.

On the affine line

\[
 a=1,\qquad(z_0,z_1,z_2)=(1+t,1+2t,1+3t),               \tag{16}
\]

the mixed gcd is

\[
                  g(t)=(1+t)(1+2t)(1+3t),               \tag{17}
\]

and the pure product is the same polynomial.  Its three distinct roots
`-1,-1/2,-1/3` each kill exactly one pure amplitude.  Hence the divisibility
branch `g_sf | h` of the pencil criterion is attained with equality.

At `a=1`, this is the canonical effective prism obtained by contracting
one site of two exact four-site ternary GHZ sources.  Their tensor
contraction is exactly `Delta_(6,3)`; the aggregate-edge closure adds the
three-spoke term in (4).  Thus even exact GHZ contraction identities can
land on the unit-saturation branch.  Any global existence theorem must use
compatibility among several cap cofactors beyond their individual top
contractions (10).

## 5. An exact formal GHZ cap-family countermodel

The prism cap family is not an arbitrary assignment of lower boundary
data.  It is the literal pair-cofactor family of an eight-site shared-edge
system.  This gives a sharp countermodel to any argument using all top GHZ
contractions but not the nonlinear equality of top matching terms with
products of the same lower edges.

Take vertices

\[
                  (p,x_0,x_1,x_2,q,y_0,y_1,y_2).        \tag{18}
\]

On each four-set `{p,x_0,x_1,x_2}` and
`{q,y_0,y_1,y_2}`, put the canonical ternary `K_4` source: the star edge
to `x_i` or `y_i` has entry `e_i e_i`, and the opposite triangle edge has
the same entry.  Add the otherwise inactive direct block

\[
 X_{pq}=\begin{pmatrix}1&2&3\\4&5&7\\8&11&13\end{pmatrix},             \tag{19}
\]

and no other edges.  The edge (19) belongs to no supported eight-site
matching, because after using it the two three-vertex shores cannot be
matched internally.  The nine supported matchings instead choose one
canonical matching independently on each `K_4`, so the actual top tensor is

\[
 H_8^{\rm act}=\sum_{i,j=0}^2
 e_i^{\otimes\{p,x_0,x_1,x_2\}}
 e_j^{\otimes\{q,y_0,y_1,y_2\}}.                         \tag{20}
\]

Cap `p,q` by `K=diag(z_0,z_1,z_2)`.  Its direct-edge scalar is

\[
                           s=z_0+5z_1+13z_2.              \tag{21}
\]

Formula (8) gives the six triangle edges scaled by `s` and the three
spokes `x_i y_i` scaled by `z_i`.  Thus this actual cofactor map is exactly
the prism family `D(s,z_0,z_1,z_2)`, and

\[
 H_6(A^K)=s^2\sum_i z_i e_i^{\otimes6}
                +z_0z_1z_2e_{012012}.                   \tag{22}
\]

Its localized mixed base locus is empty for the same reason as (15).

Now retain this actual lower edge system and its cofactor map, but in the
formal matching-term relaxation replace (20) by

\[
 H_8^{\rm form}=H_8^{\rm act}
 -\sum_{i\ne j}e_i^{\otimes\{p,x_0,x_1,x_2\}}
                  e_j^{\otimes\{q,y_0,y_1,y_2\}}
 =\Delta_{8,3}.                                          \tag{23}
\]

Equivalently, assign the six displayed negative tensors to independent
formal top matching terms.  Then for **every** bilinear cap `K`, not only
the diagonal ones,

\[
 K\mathbin{\lrcorner}H_8^{\rm form}
             =\sum_iK(e_i,e_i)e_i^{\otimes6}.            \tag{24}
\]

Hence all coefficientwise top GHZ identities and all of their cap
contractions hold exactly, while the genuine lower cofactor subfamily (22)
still has unit saturation.  What fails is only the common-product equation
asserting that every formal top matching term is the product of the same
aggregate edges used in (1).  Therefore varying `K` and using (10) alone
cannot force (3); a positive theorem must use that nonlinear common-edge
compatibility.

The failure is detected exactly by the shared-edge adjugate identity in
`cap-adjugate-six-boundary-identity.md`.  All nine cofactors of (19) are
nonzero.  Retaining the lower cofactors while replacing (20) by (23)
violates that identity in precisely the six block rows with distinct shore
colors.  Thus the formal model evades descent only by breaking a concrete
nonlinear alternating-cycle relation, not by an unspecified compatibility.

This countermodel is deliberately not an eight-site aggregate realization
of `Delta_(8,3)`: its role is to locate the exact extra hypothesis which a
global cap-span proof must exploit.

## 6. Comparison with the binary cross-pair cancellation

The rational binary source in `cross-pair-pencil-cancellation.md` has the
opposite behavior.  Two genuinely different cap cofactors give a pencil
whose sole mixed polynomial has square-free factor

\[
                    (t-2)(t+2)(2t+1).                   \tag{25}
\]

Only the first root lies on a pure zero; the other two are points of the
localized mixed base locus.  The value `t=-2` gives

\[
                  -8e_0^{\otimes6}-15e_1^{\otimes6}.     \tag{26}
\]

The binary example proves that cross-pair compatibility can make the
saturation proper.  The ternary prism proves that common mixed factors can
instead be completely covered by pure zeros.  Distinguishing these two
possibilities from the global cofactor identities (1) and (10) is the
remaining substantive step.
