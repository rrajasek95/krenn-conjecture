# The actual cofactor cap cubic and a four-parameter common-edge barrier

## 1. Outcome

Let \(B=U\mathbin{\dot\cup}W\), where \(|U|=6\), and let \(K\) be a
covector on the \(W\)-slots.  The degree-two cofactor family

\[
 A^K_{uv}=K\mathbin{\lrcorner}H_{W\cup\{u,v\}}(A)
 \qquad (u<v\in U)
\]

is an ordinary six-site aggregate edge family.  If \(F_U^K\) denotes the
complete capped top tensor, then the denominator-cleared cap cubic has the
intrinsic common-edge form

\[
 \boxed{\;
 {\cal D}_{\rm src}(K)
   =6\left(s(K)^2F_U^K-H_6(A^K)\right).                 \tag{1}
 \;}
\]

When the large source obeys \(H_B(A)=\Delta_{B,3}\), one has

\[
 F_U^K=\sum_{i=0}^2\kappa_i(K)X_i,\qquad
 \kappa_i(K)=K(e_i^{\otimes W}),
\]

and therefore

\[
 \boxed{\;
 {\cal D}(K)
   =6\left(s(K)^2\sum_{i=0}^2\kappa_i(K)X_i-H_6(A^K)\right).
                                                               \tag{2}
 \;}
\]

This is the requested exact interpretation of the cap cubic for the
actual cofactor edge family.  It retains endpoint order, arbitrary
entangled caps, parallel aggregate entries, zero blocks, and complex
cancellation.

There is also a sharp negative result.  A genuine ten-site common-edge
family has a four-dimensional cap subspace on which

* every capped top tensor is exactly
  \(\sum_i\kappa_iX_i\);
* \(s,\kappa_0,\kappa_1,\kappa_2\) are independent linear forms; and
* the actual cofactor cubic has coordinate ideal

  \[
                 I_{\cal D}=(z_0z_1z_2),
  \qquad
  h=s\kappa_0\kappa_1\kappa_2
    =(z_0+t)z_0z_1z_2\in I_{\cal D}.                    \tag{3}
  \]

Thus \(I_{\cal D}:h^\infty=(1)\).  This is not an abstract boundary
signature: every lower cofactor and every top tensor is enumerated from
one aggregate edge family.  It disproves the plausible weaker assertion
that common-edge realizability, exact GHZ contraction on the cap space,
and independence of the four active forms already force proper
saturation.  A positive theorem must additionally use extension of the
GHZ contraction identity to all cap covectors, equivalently the full
large-source equation, or compatibility between several such cap spaces.

Finally, the known six-site theorem gives a universal radical identity in
the opposite direction: for every fixed linear edge family \(A^K\),
\[
                 I_{\cal D}:h^\infty=(1).                \tag{4}
\]
Consequently “proper saturation” cannot be a standalone identity true of
ordinary cofactor families.  It can only be a conditional consequence of
the hypothetical large GHZ equations, and deriving it already contradicts
the six-site theorem.

The exact audit is
[verify_actual_cofactor_cap_cubic_and_four_parameter_prism_barrier.py](../computations/verify_actual_cofactor_cap_cubic_and_four_parameter_prism_barrier.py).

## 2. Derivation of the actual cofactor cubic

Work in the square-free commutative tensor algebra on \(U\), and write

\[
 x=\sum_{u<v\in U}A_{uv},\qquad
 C=C_0+C_2+C_4+C_6,\qquad C_0=s.
\]

Here \(C_{2j}\) is the part of the capped boundary signature in which
exactly \(2j\) boundary sites are sent across the cut.  The complete top
tensor is

\[
 F_U^K=C_6+C_4x+\frac12C_2x^2+\frac16sx^3.              \tag{5}
\]

For a boundary pair \(u,v\), a matching of \(W\cup\{u,v\}\) either uses
the old edge \(uv\), contributing \(sA_{uv}\), or sends both endpoints
across the cut.  Hence

\[
                       \sum_{u<v}A^K_{uv}=sx+C_2.       \tag{6}
\]

Since a six-site hafnian is the third divided power,

\[
                         6H_6(A^K)=(sx+C_2)^3.          \tag{7}
\]

Substituting (5)--(7) into (1) gives

\[
\begin{aligned}
{\cal D}_{\rm src}
 &=6s^2(C_6+C_4x)
   +3s^2C_2x^2+s^3x^3-(sx+C_2)^3\\
 &=6s^2(C_6+C_4x)-3sC_2^2x-C_2^3.                      \tag{8}
\end{aligned}
\]

Thus (8) is exactly the earlier denominator-cleared cumulant formula, but
now expressed as the discrepancy between the actual capped top tensor and
the hafnian of the actual cofactor edges.  Under the large GHZ equation,
(5) becomes \(F_U^K=\sum_i\kappa_iX_i\), proving (2).

There is a useful specialization when \(W=\{p,q\}\).  Orient the two
deleted stars toward \(p,q\), put

\[
 s_K=K(A_{pq}),\qquad
 r_K=\sum_{i,j}K(e_i^{(p)}e_j^{(q)})\,\ell_i m_j,
\]

and retain \(x\) for the internal boundary quadratic.  Direct matching
decomposition gives

\[
 F_U^K=s_K\frac{x^3}{6}+r_K\frac{x^2}{2},
 \qquad
 \sum_{u<v}A^K_{uv}=s_Kx+r_K.
\]

Equation (1) then factors universally as

\[
 \boxed{\;
 {\cal D}_{\rm src}(K)
       =-r_K^2(3s_Kx+r_K).                               \tag{9}
 \;}
\]

This is genuine shared-star information, but it does not by itself force
an active zero of the cubic.

## 3. The universal radical pullback points the other way

Let \(Y\) be an arbitrary six-site edge family.  Write \(G_c(Y)\) for its
matching coefficient at the word \(c\), let \(I_{\rm mix}\) be generated
by all mixed \(G_c\), and set

\[
                         P(Y)=\prod_{i=0}^2G_{i^6}(Y).
\]

The arbitrary-complex six-site theorem and the Nullstellensatz give an
integer \(N\ge1\) and rational polynomials \(Q_c\) such that

\[
                         P(Y)^N
     =\sum_{c\ {\rm mixed}}Q_c(Y)G_c(Y).                \tag{10}
\]

Apply (10) to \(Y=A^K\), and define the target-form cubic coordinates

\[
 {\cal D}_c(K)
 =6\left(s^2\kappa_c-G_c(A^K)\right),
\]

where \(\kappa_c=\kappa_i\) for \(c=i^6\) and
\(\kappa_c=0\) for mixed \(c\).  Then

\[
\left\{\prod_{i=0}^2
 \left(s^2\kappa_i-\frac{{\cal D}_{i^6}}6\right)\right\}^{N}
 =-\frac16\sum_{c\ {\rm mixed}}Q_c(A^K){\cal D}_c.     \tag{11}
\]

Modulo the full coordinate ideal \(I_{\cal D}\), equation (11) says

\[
                       (s^6\kappa_0\kappa_1\kappa_2)^N
                         \in I_{\cal D}.                 \tag{12}
\]

For \(h=s\kappa_0\kappa_1\kappa_2\), multiplication by
\((\kappa_0\kappa_1\kappa_2)^{5N}\) yields

\[
                              h^{6N}\in I_{\cal D}.      \tag{13}
\]

This proves (4), with no common-edge hypothesis at all.  It is simply the
algebraic statement that an active zero of \({\cal D}\) would be a
forbidden six-site ternary source.

This observation fixes the logical role of the desired gate.  One cannot
discover a universal common-edge identity which makes the saturation
proper for an actually existing coefficient family.  Instead, one must
show that the additional large-source GHZ equations would force the
saturation to be proper.  Equations (10)--(13) would then make those
large-source equations inconsistent.

## 4. A realizable four-parameter common-edge barrier

Take capped sites

\[
                         W=\{p,q,r,s\}
\]

and boundary sites

\[
              U=\{x_0,x_1,x_2,y_0,y_1,y_2\}.
\]

All unlisted aggregate entries are zero.  Inside \(W\), put the four
rank-one cells

\[
\begin{array}{c|c}
pq&e_0^{(p)}e_0^{(q)}\\
rs&e_0^{(r)}e_0^{(s)}\\
pr&e_1^{(p)}e_1^{(r)}\\
qs&e_2^{(q)}e_2^{(s)}.
\end{array}                                               \tag{14}
\]

On \(\{p,x_0,x_1,x_2\}\), put the canonical ternary four-site source:
\(px_i\) has color \(i\) at both endpoints, and the triangle edge
opposite \(x_i\) has color \(i\) at both endpoints.  Put the identical
construction on \(\{q,y_0,y_1,y_2\}\).

For a \(W\)-word, retain the order \(p,q,r,s\).  Define a four-parameter
cap \(K_{z,t}\) by

\[
\begin{aligned}
 K_{z,t}(i,i,0,0)&=z_i &&(i=0,1,2),\\
 K_{z,t}(i,j,0,0)&=0   &&(i\ne j),\\
 K_{z,t}(1,1,1,1)&=z_1,\qquad
 K_{z,t}(2,2,2,2)=z_2,\\
 K_{z,t}(1,2,1,2)&=t,
\end{aligned}                                             \tag{15}
\]

and let it vanish on every other coordinate word.  The repeated
specification at \((0,0,0,0)\) is consistent.

There are exactly two supported perfect matchings inside \(W\):

\[
             pq\mid rs\longmapsto(0,0,0,0),\qquad
             pr\mid qs\longmapsto(1,2,1,2).
\]

Therefore

\[
             s(K_{z,t})=z_0+t,\qquad
             \kappa_i(K_{z,t})=K_{z,t}(i,i,i,i)=z_i.    \tag{16}
\]

The four displayed forms are independent.

Every supported ten-site matching sends \(p\) to one \(x_i\), sends
\(q\) to one \(y_j\), uses \(rs\), and uses the two opposite triangle
edges.  Consequently

\[
 K_{z,t}\mathbin{\lrcorner}H_{10}(A)
                 =\sum_{i=0}^2z_iX_i.                  \tag{17}
\]

Thus the full top contraction identity required in the cap calculation
holds identically on this four-dimensional cap space, even though the
ten-site source itself is not global GHZ.

The pair cofactors are equally explicit.  Every one of the six triangle
edges is multiplied by \(s=z_0+t\), and the only cross-shore edges are

\[
                         x_iy_i=z_i e_i e_i
                         \qquad(i=0,1,2).                \tag{18}
\]

These are precisely the edges of a triangular prism.  It has four perfect
matchings: three use one spoke and the two opposite triangle edges, while
the fourth uses all three spokes.  Hence

\[
 H_6(A^{K_{z,t}})
 =s^2\sum_{i=0}^2z_iX_i
  +z_0z_1z_2\,e_{012012},                               \tag{19}
\]

where the boundary order is
\((x_0,x_1,x_2,y_0,y_1,y_2)\).  Equations (2), (17), and (19) give

\[
                  {\cal D}(K_{z,t})
                  =-6z_0z_1z_2\,e_{012012}.             \tag{20}
\]

This proves (3).  The active locus \(h\ne0\) is nonempty, but the only
way to kill the mixed prism word is to kill one of its three pure spoke
coefficients.  The extra scalar direction \(t\) makes \(s\) independent;
it does not break the root cover.

## 5. Exact remaining input

The construction retains substantially more than the abstract signature
barrier:

1. every \(A^K_{uv}\) is a literal hafnian cofactor of one common
   aggregate edge family;
2. lower and top tensors use the same edge products;
3. the top GHZ contraction holds coefficientwise on the whole
   four-parameter cap space; and
4. the four active linear forms are independent.

What it does not retain is the top contraction identity for every
covector on \(\bigotimes_{w\in W}V_w\).  For a genuine large GHZ source,
that extension is automatic.  Therefore the next viable cap-saturation
statement must use this extension, or equivalently compare the selected
cap space with additional transverse caps whose top mixed rows also
vanish.  Common-edge realizability inside one active cap space is not
enough.
