# An all-orders two-replica proof of the complex weighted Krenn–Gu conjecture

**Review status (2026-09-26): candidate complete proof, undergoing final independent review.**
This document gives the entire argument, including the earlier reflection and
diagonal-reduction steps. It is a written mathematical proof, not a Lean
formalization or an assertion of external peer review. Review records will be
linked here after they have checked these exact bytes.

## 1. Statement and algebraic model

Let V have even cardinality n > 4. At each vertex take three designated
coordinates a, b, c. In the commutative algebra in which the product of any two
coordinates at the same vertex is zero, let A be any quadratic involving only
distinct vertices, with arbitrary complex coefficients. Write A^[j] = A^j/j!.
We prove that

    A^[n/2] = tau_a a^V + tau_b b^V + tau_c c^V,
    tau_a tau_b tau_c != 0                                      (1)

is impossible. Here h^S means the product of coordinate h over S.

Coefficients of A are aggregate endpoint-color edge weights. Its divided top
power is exactly the perfect-matching tensor: every matching occurs once.
Parallel edges of identical endpoint colors aggregate by addition. Projecting
any larger target palette onto three active colors preserves (1), so the result
covers every target dimension at least three. Unequal nonzero pure amplitudes,
arbitrary edge density, and arbitrary complex weights are allowed.

We use formal Wick moments, defined as sums over pairings of labeled factors
with assigned symmetric covariances. Odd moments are zero. These are polynomial
identities; they require neither positivity nor an invertible covariance.

## 2. Whole binary higher responses vanish

Let Omega have 2m+1 >= 3 vertices, R be an arbitrary quadratic on Omega, and
D be a vector space of rows L such that

    Phi(L) = L R^[m] = sum_h f_h(L) h^Omega.                    (2)

Assume all three linear functions f_h are nonzero, and at least two are
independent. Define H_p(L) = L^p R^[(2m+1-p)/2] for odd p <= 2m+1.
We will prove that every H_p, p >= 3, has zero coefficient on every word
using at most two colors.

Give formal variables X_(i,h) their R covariances, zero covariances within a
vertex, and give an auxiliary g covariance L_i(h) with X_(i,h) and zero
covariance with itself. A Wick moment with p copies of g and one specified
coordinate at each vertex is the corresponding coefficient of H_p(L).
The p! assignments of auxiliary occurrences are precisely those of the raw
power L^p; the divided power of R counts each remaining matching once.

Take two independent identical replicas (X,g_1), (Y,g_2). Choose distinct
local colors alpha_i,beta_i at each vertex and set
Delta_i = X_(i,alpha_i)Y_(i,beta_i) - X_(i,beta_i)Y_(i,alpha_i).
Over C(s,t) the orthogonal reflection

    (s^2+t^2)^(-1) [[s^2-t^2, 2st], [2st, t^2-s^2]]

fixes s g_1+t g_2 and negates each Delta_i. It preserves the replicated
covariance, so the moment of (s g_1+t g_2)^(p+1) product_i Delta_i is zero:
there are an odd number of determinants. Extracting s^p t gives

    sum_I (-1)^|I| H_p(L)(w_I) Phi(L)(w'_I) = 0,               (3)

where w_I uses beta on I and alpha elsewhere, and w'_I is complementary.
Equality over C(s,t) gives a polynomial identity, including isotropic parameter
values by extension. No operation on the original source is being made.

With constant local pair a,b, (3) says
f_b [a^Omega]H_p = f_a [b^Omega]H_p. Two independent f's are coprime in
C[D], hence for p=2r+1 there is a common homogeneous polynomial q_r of
degree 2r such that [h^Omega]H_p = f_h q_r for every h; q_0=1.
For a mixed word w avoiding an active color h, choose alpha_i=w_i,
beta_i=h. The only constant complementary word in (3) is h^Omega, giving
f_h [w]H_p=0. Polynomial cancellation proves all binary mixed coefficients
zero, even at individual rows where f_h(L)=0.

Define finite polynomials

    Psi(L) = sum_(r=0)^m H_(2r+1)(L)/(2r+1)!,
    g(L)   = sum_(r=0)^m q_r(L)/(2r+1)!.

On any binary palette a,b, Psi(L) thus equals
g(L)(f_a(L)a^Omega + f_b(L)b^Omega).
For two tensors on Omega let K be the product of local alternating pairings,
normalized by K(a^Omega,b^Omega)=1. Wick moments with shifted variables
X_i+L_i show that K(Psi(L),Psi(M)) is invariant under simultaneous SO(2)
rotation of the two mean rows: the replica covariance and each determinant
are unchanged. Choose independent f_a,f_b. This pairing is

    (f_a(L)f_b(M)-f_b(L)f_a(M)) g(L)g(M).

The determinant factor is a nonzero polynomial and is rotation invariant.
Cancel it in C[D x D], then rotate by 45 degrees and set M=0. Since g is
even and g(0)=1,

    g(L/sqrt(2))^2 = g(L).

If g had positive degree, the degrees of the two sides would differ. Thus
g=1 and all q_r with r>=1 vanish. Together with (3), this proves the claimed
whole binary vanishing, through the terminal degree 2m+1. Polarization gives
the same statement for products of arbitrary rows from this same D.

For a source (1), delete any root p. Its three actual incident rows have
responses tau_h h^(V\p), so their span satisfies (2) with three independent
f_h. Thus this lemma applies at every original root, before diagonalization.

## 3. Even omission identities and diagonal reduction

In the setting of (2), omit a vertex q. Write S=Omega\{q},

    R = Q + sum_h h_q V_h,     L = U + sum_h d_h h_q,
    E(U) = sum_(r=0)^m U^(2r)/(2r)! Q^[m-r],   F=E(0).

The full coefficient of q=h in Psi(L) is

    d_h E(U) + E_(V_h)(U),

where subscripts mean directional derivatives in the mean, with Q fixed.
By Section 2 its projection onto any palette h,k on S is f_h(L)h^S.
All the following pairings use this binary projection implicitly.

Because |S| is even, K is symmetric and K(Z,h^S)=[k^S]Z. The same
two-replica rotation used above gives

    K(E(U),E(U)) = K(F,E(sqrt(2)U)),
    K(E(U),E_V(U)) = K(F,E_V(sqrt(2)U))/sqrt(2).                (4)

The second identity follows by differentiating the rotation identity at
means U,U+tV: the second rotated mean is zero at t=0 and E'(0)=0.
Substitute E_(V_h)(U)=f_h h^S-d_h E(U), and the corresponding identity for
sqrt(2)L, into the second equation of (4). The first equation cancels the
d_h terms, leaving f_h(L) [k^S] {E(U)-F}=0. Cancel the nonzero polynomial f_h.
Separating homogeneous degrees and polarizing yields, in particular,

    [k^S] U(L_1) U(L_2) Q^[m-1] = 0                          (5)

for any L_1,L_2 in D. The formula includes m=1.

Return to (1). For a fixed color h define M_h[p,r]=A_pr(h,h) off the
diagonal, with zero diagonal, and define C_h[r,q]=haf(M_h[V\{r,q}]) for
r!=q, with C_h[q,q]=0. Also let B_ih[p,r]=A_pr(i,h), with zero diagonal.
Expansion of the original one-defect word at p gives

    (B_ih C_h)[p,p] = delta_(i,h) tau_h.

For p!=q, expand each C_h[r,q] at its retained vertex p. This gives

    (B_ih C_h)[p,q]
      = sum_(r,s distinct in V\{p,q}) A_pr(i,h) A_ps(h,h)
          haf(M_h[V\{p,q,r,s}]) = 0.                         (6)

The last expression is exactly (5) for two rows of the original p family
after omitting q. Both sums are ordered; there is no factor 1/2. Consequently
B_ih C_h = delta_(i,h)tau_h I. Taking i=h proves C_h invertible. Taking
i!=h then proves B_ih=0. Every original edge block is therefore diagonal
in the given target coordinates. This uses neither cofactor nonvanishing
assumptions nor a change of basis.

## 4. The endpoint identity

Fix two colors B,H after the diagonal reduction and roots p!=q. Put
U=V\{p,q}, N=|U| (even), and let Q be the literal binary quadratic on U.
Write

    d=B_pq, e=H_pq, beta=haf(B), eta=haf(H), alpha=haf(B[U]),
    x=sum_i B_pi b_i, y=sum_i B_qi b_i,
    u=sum_i H_pi h_i, v=sum_i H_qi h_i,
    E(L)=sum_(j=0)^(N/2) L^(2j)/(2j)! Q^[N/2-j], F=E(0).

We prove beta=d alpha whenever d!=0. Derivatives of E always keep Q fixed.
Section 2, applied to the original p and q row planes and expanded at the
other root, gives the exact polynomial identities

    E_y(sx+tu) + ds E(sx+tu) = s beta b^U,
    E_v(sx+tu) + et E(sx+tu) = t eta h^U,
    E_x(ay+bv) + da E(ay+bv) = a beta b^U,
    E_u(ay+bv) + eb E(ay+bv) = b eta h^U.                    (7)

These include the highest coefficient, which uses the terminal original odd
response of degree N+1. They are identities in mean parameters on the
unchanged source. Differentiating those parameters is legitimate and gives

    E_u(ay)=0, E_v(sx)=0,
    E_yu(sx)=-ds E_u(sx),
    E_uv(sx)+eE(sx)=eta h^U,
    E_xy(0)+dF=beta b^U.                                    (8)

On tensors on U use the symmetric binary alternating pairing K, normalized
by K(b^U,h^U)=1. The polynomial K(E(L_1),E(L_2)) is invariant under the
full O(2) action on the two means. The Wick proof is as in Section 2;
a determinant -1 transformation contributes (-1)^N=1.

Introduce independent columns P,Qc,Rc,Sc in C^2 and means
L_i=P_i x+Qc_i y+Rc_i u+Sc_i v. Set

    G=K(E(L_1),E(L_2)),  f=G|_(Rc=Sc=0),
    M_ij=partial_(Rc_i) partial_(Sc_j) G|_(Rc=Sc=0),
    T=M+e f I.

These are finite polynomials. O(2) invariance gives
M(OP,OQc)=O M(P,Qc) O^T, and similarly for T. By (8),
M_12=K(E_u(P_1x+Qc_1y),E_v(P_2x+Qc_2y)) is divisible by P_1 Qc_2;
likewise M_21 is divisible by P_2 Qc_1.

We spell out the resulting elementary matrix lemma. In an orthonormal frame
where P_1=0, M_12=0, so MP is parallel to P. In a frame where Qc_2=0,
M_12=0, so M^T Qc is parallel to Qc. Such frames exist on a dense open
set of nonisotropic columns. Their eigenvalues agree when P dot Qc !=0.
For two independent columns in dimension two these conditions force

    M=a_0 I+b P Qc^T.

Indeed M minus the common eigenvalue times I annihilates P and has left
kernel Qc; its rank-one form is a multiple of
(P dot Qc)I-P Qc^T. Literal divisibility above proves that
b=M_12/(P_1 Qc_2) is polynomial, and so is a_0=M_11-bP_1Qc_1.
The generic identity therefore extends everywhere. Uniqueness and covariance
make a_0,b scalar O(2) invariants. Hence

    T=a I+b P Qc^T,
    a,b in C[sigma,tau,c],
    sigma=P dot P, tau=Qc dot Qc, c=P dot Qc.                 (9)

For completeness the invariant ring assertion is elementary: in coordinates
p_+=P_1+iP_2, p_-=P_1-iP_2 and q_+,q_-, SO(2) acts with weights +1,-1.
Its invariant monomials are generated by sigma,tau,r=p_+q_-,s=p_-q_+,
with rs=sigma tau. Reflection exchanges r,s. Symmetric polynomials reduce
to r+s=2c and rs=sigma tau, giving C[sigma,tau,c]. These three Gram
coordinates are algebraically independent.

At Qc_1=0, differentiate M_12 in Qc_1 and use (8). One obtains

    partial_(Qc_1) M_12 = -d P_1 M_12,
    P_1^2 Qc_2 (b_c+d b)=0.

The substitution (sigma,tau,c)=(P_1^2+P_2^2,Qc_2^2,P_2Qc_2) is injective
on polynomial rings: every tau!=0 and arbitrary sigma,c is attained over C.
Thus b_c+d b=0. If d!=0, comparison of the highest power of c forces
the finite polynomial b to be zero. Therefore T=a I.

Write Z=E_uv(P_2x+Qc_2y)+eE(P_2x+Qc_2y). The full expression is
T_22=K(E(P_1x+Qc_1y),Z). Differentiate this expression in Qc_1,
then set Qc_1=0. Equation (7) gives

    partial_(Qc_1)T_22=P_1 beta K(b^U,Z)-dP_1 T_22.

The pure-H coefficient of Z is eta: positive B mean insertions cannot
contribute to an all-H word, so it is the same as at zero, where (8)
gives E_uv(0)+eF=eta h^U. Thus K(b^U,Z)=eta. Using (9) and the same
injective substitution proves

    a_c+d a=beta eta.

Finite polynomial degree and d!=0 force a=beta eta/d, independent of all
three Gram variables. At the origin,

    a(0)=K(F,E_uv(0)+eF)=eta K(F,h^U)=eta alpha.

Since eta!=0, we have proved

    beta = B_pq haf(B[V\{p,q}])   whenever B_pq!=0.           (10)

No source deformation, differentiation of source equations along an
unlicensed direction, infinite series, or positivity argument occurs here.
The variables P,Qc are independent proof parameters, not actual graph rows.

## 5. Every color is a perfect matching

The ordinary hafnian expansion at a vertex p says

    beta=sum_q B_pq haf(B[V\{p,q}]).

By (10) every nonzero summand equals beta. Since beta!=0, the number of
supported B neighbors of p is exactly one. This holds at every vertex, and
for each of the three colors by choosing any other active color as H.
Thus each color graph is a weighted perfect matching.

Two such matchings cannot share an edge pq: choosing that edge in color B
and the other matching in color H off p,q gives a mixed word with nonzero
coefficient, the product of nonzero matching weights. Consequently their
union is a simple cubic graph properly colored with three colors. Any
receiving color word supports at most one matching, because each vertex
has exactly one incident edge of its requested color. Therefore a mixed
perfect matching would have a nonzero coefficient and violate (1).

## 6. The remaining graph lemma

We include the standard unweighted obstruction, usually attributed to
Bogdanov; it is also stated as Theorem 7 in the HTML version of
[Chandran–Gajjala–Illickan, Krenn–Gu conjecture for sparse graphs](https://arxiv.org/html/2407.00303).
No new graph-theoretic result is claimed here.

Suppose three pairwise disjoint perfect matchings F,G,H on n>4 vertices
have no mixed perfect matching in their union. The union F union G must
be a single alternating Hamilton cycle C: otherwise choosing F on one
component and G on the others already gives a mixed matching. Label its
vertices 0,...,n-1 cyclically. H is a matching of chords.

A chord with endpoints of opposite parity leaves two even paths when its
endpoints are deleted. Matching those paths along C and adding the chord
gives a mixed perfect matching. Hence all H chords join equal parities.
The two parity classes must each have even size; otherwise H is impossible.

An even-even chord and an odd-odd chord whose endpoints interlace leave
four even paths on deleting their endpoints. Those paths and the two
chords give a mixed perfect matching when n>4. Thus no such pair interlaces.

Choose a chord and one of its sides with the fewest vertices strictly
inside, over all chords and both sides. Its endpoints have equal parity,
so its interior contains a vertex of the opposite parity. Every vertex
of that opposite parity in the interior must be H-matched to another
interior vertex; a partner outside would give an interlacing opposite-parity
chord. Therefore some H chord lies strictly inside the chosen arc. One
side of that chord has fewer interior vertices, a contradiction.

This proves that a mixed perfect matching exists, contradicting Section 5.
Equation (1) is impossible for every even n>4.

## 7. Boundaries, provenance, and review scope

For n=4 the three matchings of K4 give the permitted ternary source. In
Section 6 a pair of interlacing chords then exhausts the vertices and gives
the pure third matching, so no contradiction is asserted. Sections 2–5
remain valid at n=4, including their terminal response coefficients.
For n=2 the odd-core lemma does not apply and arbitrary target dimension
is possible. Odd n has no perfect matchings in this model.

The earlier written foundations are collected in
[the higher-response directory](../computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md),
with separate proofs and audits of reflection, even omission, and global
diagonal reduction. The new step is Section 4: finite O(2) covariance and
two original root identities force the endpoint equality. Sections 2–3
are included here so that the all-orders conclusion has no dependency on
a finite enumeration, an unproved normalization operation, or an assumed
vanishing of three-color higher responses.
