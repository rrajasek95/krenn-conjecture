# Independent audit: line--plus--plane clean-cap pencil

## 1. Verdict

**PASS.**  The cap contraction, homogeneous clean-error formula,
two-site support argument, activity polynomial, integral-domain step,

\[
                         B\mid A
\]

Schmidt-rank contradiction, and scalar-zero refinement in
[the source note](line-plus-plane-shore-clean-cap-pencil.md) are correct.
No missing divided-power coefficient, endpoint transpose, change of fixed
colour coordinates, or extra nonvanishing hypothesis is being used.

The two coordinate alternatives in source equations (6)--(7) are exactly
the remaining ways in which this particular clean pencil can have no active
member.  They are not proved impossible, and the source note correctly does
not claim otherwise.

No correction to the source note was necessary.  The audited source has
SHA-256

```text
bd8fede061931b7d2632788243d1cce6fed7c3c9d7259e691a9f259f883c5049
```

## 2. Assertion ledger

| Assertion | Verdict | Reason |
|---|---|---|
| Physical cap contraction | **PASS** | Bilinearity gives the stated scalar, response, and fixed diagonal target coefficients. |
| Homogeneous clean error | **PASS** | It is the denominator-cleared canonical error from the exact descent theorem, with divided powers already absorbing binomial coefficients. |
| Two-site response implies \(r^{[2]}=0\) | **PASS** | Every response monomial occupies both sites of \(B=\{u,v\}\), so every product of two response monomials repeats a site. |
| Activity criterion and polynomial | **PASS** | The exact descent theorem requires precisely \(\sigma\kappa_0\kappa_1\kappa_2\ne0\). |
| Integral-domain/hyperplane argument | **PASS** | The restrictions of the four linear factors live in the polynomial ring of the two-dimensional vector space \(C_0\), which is a domain. |
| Scalar-only degeneration | **PASS** | A scalar-zero cap with three nonzero diagonal target coefficients would equate a tensor of \(B\mid A\) Schmidt rank at most one with one of rank three. |
| Scalar-zero refinement | **PASS** | The same flattening has rank exactly the number of nonzero products \(c_i d_i\), hence at most one. |
| Claimed remaining gates | **PASS** | Under absence of an active clean cap, one has either \(d_i=0\) or \(C_0=\{c:c_i=0\}\), with the transposed alternatives when the endpoints are exchanged. |

There are no **FAIL** or **PARTIAL** algebraic items.  The unresolved
coordinate gates are an explicit downstream target, not an unproved step in
the reduction.

## 3. Shore ranks and fixed-label kernels: PASS

For a shore \(A\), write the first endpoint aggregate map as

\[
 P_A:C\longrightarrow\bigoplus_{x\in A}V_x,
 \qquad P_A(c)=\sum_i c_i(p_i|_A),                         \tag{A1}
\]

and similarly for \(S_A:D\to\bigoplus_{x\in A}V_x\).  The image of
\(P_A^*\) is

\[
                 \sum_{x\in A}L_x^P\subseteq C^*.           \tag{A2}
\]

In the maximal deficient shore supplied by
[the selector-union theorem](uniform-selector-union-maximal-defect-shore.md),
every minimizing Rado witness is all of \(A\).  Consequently its equation
(3) gives

\[
 \rho_P(A)=\dim\sum_{x\in A}L_x^P=\operatorname{rank}P_A,
 \qquad
 \rho_S(A)=\operatorname{rank}S_A.                          \tag{A3}
\]

Thus the \(b=2\) row \((\rho_P(A),\rho_S(A))=(1,2)\) really does give

\[
 \dim\ker P_A=2,
 \qquad
 \dim\ker S_A=1.                                           \tag{A4}
\]

This is an ordinary aggregate linear-rank conclusion, not an illicit
replacement of Rado rank by row-span rank.  Choosing a nonzero
\(d\in\ker S_A\) and setting \(C_0=\ker P_A\) changes no basis in the
fixed label spaces.  In particular, the later conditions \(d_i=0\) and
\(c_i=0\) refer to the original physical target labels.

The source assumes the orientation \((1,2)\) after exchanging the two
endpoints.  If the shore is initially of type \((2,1)\), the same proof
applies with \(P,C,c\) and \(S,D,d\) exchanged.  This is not a transpose
gap.

## 4. Cap contraction and clean error: PASS

Contracting the nine fixed-label rows

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i              \tag{A5}
\]

against an arbitrary physical pair covector \(K=(K_{ij})\) gives

\[
 \sigma(K)q^{[h]}+r(K)q^{[h-1]}
       =\sum_i\kappa_i(K)X_i,                               \tag{A6}
\]

where

\[
 \sigma(K)=\sum_{ij}K_{ij}a_{ij},\qquad
 r(K)=\sum_{ij}K_{ij}p_i s_j,\qquad
 \kappa_i(K)=K_{ii}.                                       \tag{A7}
\]

For \(K_c=cd^{\mathsf T}\), its entries are \((K_c)_{ij}=c_i d_j\),
so distributivity in the site-square-zero algebra gives

\[
 \sigma(K_c)=c^{\mathsf T}ad,\qquad
 r(K_c)=\left(\sum_i c_ip_i\right)
          \left(\sum_jd_js_j\right)=P(c)S(d),\qquad
 \kappa_i(K_c)=c_i d_i.                                    \tag{A8}
\]

The endpoint order is retained in the first and second factors of the
outer product.  Commutativity of the residual algebra does not transpose
the matrix \(K_c\).

For \(\sigma\ne0\), the canonical effective quadratic is

\[
                            y=q+\frac r\sigma.                \tag{A9}
\]

The divided-power binomial rule gives

\[
 \sigma^{h}y^{[h]}
 =\sum_{j=0}^{h}\sigma^{h-j}q^{[h-j]}r^{[j]}.               \tag{A10}
\]

Using (A6), the \(j=0,1\) terms are precisely the
denominator-cleared capped target.  The remaining canonical error is

\[
 {\cal E}(K)=\sum_{j=2}^{h}
       \sigma(K)^{h-j}q^{[h-j]}r(K)^{[j]}.                  \tag{A11}
\]

This agrees with equations (4), (15), and (16) of
[the exact descent target](clean-pair-cap-exact-descent-target.md).
There is no missing \(\binom hj\), \(j!\), or \((h-j)!\): those factors
are already built into \(q^{[h-j]}\) and \(r^{[j]}\).

The exact descent theorem calls a cap active exactly when

\[
                 \sigma(K)\kappa_0(K)\kappa_1(K)
                     \kappa_2(K)\ne0.                        \tag{A12}
\]

Substitution of (A8) therefore gives, up to the fixed choice of the
nonzero generator \(d\), exactly

\[
 {\cal A}(c)=\bigl(c^{\mathsf T}ad\bigr)
                  \prod_{i=0}^2c_i d_i.                     \tag{A13}
\]

Scaling \(c\), \(d\), or \(K_c\) changes only an overall nonzero scalar,
so both activity and cleanliness are projective properties as claimed.

## 5. The entire pencil is clean: PASS

For \(c\in C_0\), equations (A1)--(A4) imply

\[
                         P(c)|_A=0,
 \qquad                   S(d)|_A=0.                          \tag{A14}
\]

Hence both degree-one factors in \(P(c)S(d)\) are supported on
\(B=\{u,v\}\).  Expanding by site,

\[
 P(c)S(d)=P_u(c)S_v(d)+P_v(c)S_u(d),                         \tag{A15}
\]

because the same-site products at \(u\) and \(v\) vanish.  Therefore

\[
                         r(K_c)\in V_u\otimes V_v.            \tag{A16}
\]

Every monomial in a product of two elements of
\(V_u\otimes V_v\) repeats both sites.  The defining relations
\(V_uV_u=V_vV_v=0\) thus give

\[
                         r(K_c)^2=0,
 \qquad                   r(K_c)^{[2]}=0.                     \tag{A17}
\]

Associativity then gives \(r(K_c)^{[j]}=0\) for every \(j\ge2\), so
(A11) vanishes.  This includes the case \(r(K_c)=0\).  It neither cancels
a power of \(q\) nor assumes that a lower divided power of \(q\) is
nonzero.

## 6. Integral-domain and finite-hyperplane step: PASS

Regard each coordinate restriction \(c_i|_{C_0}\) and the scalar
restriction

\[
                         \ell(c)=c^{\mathsf T}ad|_{C_0}       \tag{A18}
\]

as elements of \(\operatorname{Sym}(C_0^*)\cong\mathbb C[x,y]\).
If every \(d_i\ne0\) and no \(c_i|_{C_0}\) is the zero linear form,
then the three coordinate factors in (A13) are nonzero polynomials.  Since
\(\mathbb C[x,y]\) is an integral domain,

\[
                   {\cal A}|_{C_0}\equiv0
        \quad\Longrightarrow\quad \ell\equiv0.              \tag{A19}
\]

Equivalently, each kernel \(\ker(c_i|_{C_0})\) is a proper line in the
two-dimensional vector space \(C_0\).  A finite union of these three
lines cannot cover \(C_0\) over \(\mathbb C\), so there is a \(c\in C_0\)
with

\[
                         c_0c_1c_2\ne0.                       \tag{A20}
\]

The source uses both formulations consistently.  There is no finite-field
exception because the ground field throughout is \(\mathbb C\).

## 7. The \(B\mid A\) Schmidt-rank contradiction: PASS

Assume the scalar-only alternative in (A19), and choose \(c\) as in
(A20).  Then \(\sigma(K_c)=0\), while every \(c_i d_i\ne0\).  Equation
(A6) becomes

\[
              r(K_c)q^{[h-1]}=\sum_i c_i d_iX_i.              \tag{A21}
\]

Since \(r(K_c)\) already occupies both sites of \(B\), every summand of
\(q^{[h-1]}\) that meets \(B\) collides with it.  The surviving summands
are exactly the restriction to \(A\):

\[
 r(K_c)q^{[h-1]}
       =r(K_c)\otimes q_A^{[h-1]}.                            \tag{A22}
\]

There is no numerical factor in (A22).  In the divided power
\(q^{[h-1]}=q^{h-1}/(h-1)!\), the \((h-1)!\) orders of every matching on
\(A\) cancel its denominator, exactly as they do in
\(q_A^{[h-1]}\).

Factoring the fixed-colour target across \(B\mid A\) gives

\[
 r(K_c)\otimes q_A^{[h-1]}
 =\sum_{i=0}^2c_i d_i
    \bigl(e_i^{(u)}e_i^{(v)}\bigr)\otimes
    \left(\bigotimes_{x\in A}e_i^{(x)}\right).               \tag{A23}
\]

The left side is a decomposable tensor and hence has Schmidt rank at most
one; this remains true if either factor is zero.  The three displayed
vectors on the \(B\)-side are independent, and the three constant-colour
vectors on the nonempty \(A\)-side are independent.  With all three
coefficients nonzero, the right side has Schmidt rank exactly three.  This
contradiction rules out (A19).

No hypothesis \(q_A^{[h-1]}\ne0\) is needed here.  If that power vanished,
the left side would have rank zero and the contradiction would be even
more immediate.  The assumption \(h\ge3\) ensures
\(|A|=2h-2\ge4\), although independence of the three right factors only
needs \(A\ne\varnothing\).

It follows that an identically zero activity polynomial on the clean
pencil forces

\[
 d_i=0\text{ for some }i,
 \qquad\text{or}\qquad
 c_i|_{C_0}=0\text{ for some }i.                             \tag{A24}
\]

Conversely, either condition in (A24) visibly kills the product in
(A13).  Thus these are exact inactivity gates for the pencil, not merely
necessary conditions obtained by a dimension count.

If \(c_i|_{C_0}=0\), then the two-dimensional subspace \(C_0\) is contained
in the two-dimensional coordinate plane \(\{c:c_i=0\}\), hence equals it.
The rank-one map \(P_A\) consequently factors without any label change as

\[
                         P_A(c)=c_iU,
 \qquad                   U=P_A(e_i)\ne0.                     \tag{A25}
\]

Thus the other two fixed physical rows vanish on \(A\) and are supported
on \(B\), exactly as the source states.

## 8. Scalar-zero refinement: PASS

The linear equation \(c^{\mathsf T}ad=0\) always has a nonzero solution in
the two-dimensional space \(C_0\).  For any solution, the same collision
calculation gives

\[
 r(K_c)\otimes q_A^{[h-1]}
 =\sum_i c_i d_i
     \bigl(e_i^{(u)}e_i^{(v)}\bigr)\otimes Y_i^A.             \tag{A26}
\]

If

\[
                         I=\{i:c_i d_i\ne0\},                 \tag{A27}
\]

then the right side of (A26) has Schmidt rank exactly \(|I|\), while the
left side has rank at most one.  Therefore

\[
                              |I|\le1.                         \tag{A28}
\]

When \(I=\{t\}\), the right side is nonzero.  Both factors on the left
are consequently nonzero, and uniqueness of factors of a nonzero pure
tensor gives nonzero scalars \(\lambda,\mu\) with

\[
 r(K_c)=\lambda e_t^{(u)}e_t^{(v)},\qquad
 q_A^{[h-1]}=\mu Y_t^A,\qquad
 \lambda\mu=c_t d_t.                                      \tag{A29}
\]

When \(I=\varnothing\), equation (A26) says
\(r(K_c)\otimes q_A^{[h-1]}=0\).  Over \(\mathbb C\), if
\(q_A^{[h-1]}\ne0\), this forces \(r(K_c)=0\).  The source states this
nonvanishing condition explicitly and does not infer separate vanishing
from a cancelling matching sum.

## 9. Interface with exact descent and the six-site obstruction

An active point of this pencil meets exactly the hypotheses of
[the clean-pair descent theorem](clean-pair-cap-exact-descent-target.md):
its direct scalar and all three diagonal target coefficients are nonzero,
and (A17) makes the homogeneous canonical error zero.  The theorem then
produces an exact ternary aggregate source on the \(2h\) residual sites,
retaining arbitrary complex coefficients and endpoint order.

At the first boundary \(h=3\), this is a six-site aggregate source of the
precise form excluded by
[the arbitrary-complex six-site theorem](../proofs/six-site-arbitrary-complex-obstruction.md).
That theorem permits arbitrary endpoint-ordered \(3\times3\) blocks,
parallel-source aggregation, zero coefficients, and complex cancellation,
so no model restriction is lost at this interface.  At higher order, the
same cap is the exact \(N\)-to-\(N-2\) descent required by the minimal-order
induction in the clean-pair target note.

## 10. Exact remaining open target

After orienting the line--plus--plane shore so that
\((\operatorname{rank}P_A,\operatorname{rank}S_A)=(1,2)\), the only
remaining no-descent coefficient geometries are

\[
 \boxed{
 \begin{array}{ll}
 \text{(G1)}&d_i=0\text{ for some fixed physical label }i,\\[2mm]
 \text{(G2)}&\ker P_A=\{c:c_i=0\}\text{ for some fixed label }i.
 \end{array}}                                               \tag{A30}
\]

For the oppositely oriented shore, include the transposed versions of
(G1)--(G2).  The open task is to eliminate these fixed-coordinate gates,
or derive an exact descent within them, by coupling the scalar-zero member
(A26) to additional literal full-nine rows or to the quotient probes at
the two sites \(u,v\).

The scalar-zero restriction \(|I|\le1\) and its purity consequences are
valid extra data, but they do not by themselves eliminate (G1) or (G2).
Accordingly, the source note is a strict and exact reduction of the
\(b=2\) branch, not a closure of those two boundary cases.
