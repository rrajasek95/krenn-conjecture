# Finite two-replica covariance forces every supported endpoint identity

PROVISIONAL CLOSING PROOF by /root/global_bridge and /root, 2026-09-26.
Independent complete proof audits are required before a resolution claim.
This fresh source supplies the new finite-polynomial step. The preceding
diagonal reduction, original whole odd-response tower, and final matching
obstruction are identified separately below. Prior bound files are unchanged.

## 1. Exact hypotheses and endpoint theorem

Let |V|=2m>=4. Let B,H be complex symmetric hollow matrices, and use the
two physical axes b_i,h_i at each site. Put beta=haf(B), eta=haf(H), with
eta!=0. Assume that their whole binary top is

    (Q_B+Q_H)^[m]=beta b^V+eta h^V,       Q^[j]=Q^j/j!.

Assume also the ORIGINAL WHOLE higher odd responses vanish: at every
root p, for every odd ell=3,5,...,2m-1 and every scalar s,t,

    (s Y_B(p)+t Y_H(p))^ell
                 R_p^[(2m-1-ell)/2]=0.                         (1)

Here R_p is the actual B/H quadratic off p, Y_B,Y_H are its actual
monochromatic root rows, and zero means the entire b/h receiving tensor.
Repeated rows in (1) are RAW powers. These are equations on the original
rows and core, including ell=2m-1; they assert no inheritance to a repair.

**Endpoint theorem.** Under these hypotheses, for every p!=q with
d=B[p,q]!=0,

    beta=d haf(B[V without p,q]).                              (2)

If beta!=0, B is a supported perfect matching: every vertex has exactly
one B neighbor. In an actual full diagonal ternary source, the
[reviewed whole-response reflection theorem](ACTIVATED-MATCHING-IDEAL-CONTAINS-ACTUAL-INVERSE-DEFECTS-AND-MIDDLE-QUARTIC-RESEARCH-NOTE.md)
supplies (1) for every binary palette, using the nonzero third amplitude.
Thus the theorem applies separately to every color of that source.

## 2. Retained finite means and the licensed source boundaries

Fix p!=q. Set U=V without p,q, N=|U|, and let Q be the actual retained
B/H quadratic on U. In the commutative site algebra, any product using
a physical site twice is zero. Write

    x=sum_(i in U) B_pi b_i,  y=sum_(i in U) B_qi b_i,
    u=sum_(i in U) H_pi h_i,  v=sum_(i in U) H_qi h_i,
    d=B_pq, e=H_pq, alpha=haf(B[U]), gamma=haf(H[U]).

The finite WHOLE even mean is

    E(L)=sum_(j=0)^(N/2) L^(2j)/(2j)! Q^[N/2-j],  F=E(0).

Subscripts denote directional derivatives of this finite polynomial:
E_y(L)=partial_y E(L), E_yu(L)=partial_y partial_u E(L), etc.
The full top and (1) imply the exact polynomial boundary equations

    E_y(sx+tu)+sd E(sx+tu)=s beta b^U,
    E_v(sx+tu)+te E(sx+tu)=t eta h^U,
    E_x(ay+bv)+ad E(ay+bv)=a beta b^U,
    E_u(ay+bv)+be E(ay+bv)=b eta h^U.                (3)

For example, the q=b coefficient of the finite odd mean at p has
two literal possibilities: a direct p-q B departure gives sd E;
a q-to-U B edge gives E_y. Its degree-one term is the binary full
top. Every higher odd term is zero by (1). Its highest degree is
N+1=2m-1, coming from sd E's highest even term. That degree is
INCLUDED in (1). The q=h coefficient gives the second equation;
interchanging p,q gives the last two. This proves (3) at all degrees.

The following licensed specializations and plane derivative suffice:

    E_v(sx)=0,           E_u(ay)=0,
    E_y(sx)+sd E(sx)=s beta b^U,
    E_yu(sx)+sd E_u(sx)=0,
    E_uv(0)+eF=eta h^U.                             (4)

The fourth equation differentiates the FIRST identity of (3) in t
at t=0. It does not differentiate a source constraint in edge space.
The last equation is the coefficient of t in the second identity.

## 3. Universal two-replica orthogonal covariance

For whole retained tensors Z,W define the complementary alternating
pairing

    K(Z,W)=sum_(S subset U) (-1)^|S|
                Z(b on S,h off S) W(h on S,b off S).

N is even, so this pairing is symmetric. In particular
K(h^U,Z)=[b^U]Z and K(b^U,Z)=[h^U]Z.
The universal finite-Wick identity is

    K(E(cL+sM),E(-sL+cM))=K(E(L),E(M)), c^2+s^2=1. (5)

It follows by mixing two identical Wick replicas: their sum of actual
quadratics is orthogonally invariant, and the product of their local
b/h determinants is invariant under determinant-one replica rotation.
This is the reviewed covariance used in
[polarized replica transfer](POLARIZED-REPLICA-TRANSFER-PUTS-ALL-MIXED-ROOT-STAR-DERIVATIVES-IN-THE-ACTIVATED-IDEAL-RESEARCH-NOTE.md).
Since E(-L)=E(L), reflection of either replica preserves the scalar
kernel as well. Consequently (5) holds for the whole complex O(2).
Replica rotation is an algebraic identity, not a source operation.

Let P,Q',U',V' be four independent two-component parameter columns.
To avoid confusing the retained quadratic Q with a parameter, write
Q'=(q_1,q_2), P=(p_1,p_2). Set

    L_i=p_i x+q_i y+U'_i u+V'_i v,
    G=K(E(L_1),E(L_2)),  f=G|_(U'=V'=0),
    M_ij=partial_(U'_i) partial_(V'_j)G|_(U'=V'=0),
    Nmat=M+e f I_2.                                  (6)

All are finite polynomials. Under any replica R in O(2), f is invariant
and M(RP,RQ')=R M(P,Q') R^T; the same holds for Nmat.
For i!=j, M_ij=K(E_u(p_i x+q_i y),E_v(p_j x+q_j y)).
By (4), this vanishes at p_i=0 and at q_j=0. Thus

    M_12=p_1 q_2 B,       M_21=p_2 q_1 B'             (7)

for polynomial B,B'. No physical row independence is required.

## 4. A polynomial covariant-matrix lemma

Whenever P is a nonisotropic parameter vector, rotate it onto its
first coordinate axis. There M_21=0, so MP is parallel to P.
Covariance transfers the conclusion back. The identity det(P,MP)=0
extends polynomially to every P,Q'. In the same way M^T Q' is parallel
to Q', using M_12=0 when q_2=0. These two identities and (7) give

    M_22-M_11=p_2 q_2 B-p_1 q_1 B',
    M_22-M_11=p_2 q_2 B'-p_1 q_1 B.

Subtracting gives (p_1 q_1+p_2 q_2)(B-B')=0, hence B=B'. Therefore
there is a polynomial A such that exactly

    Nmat=A I_2+B P (Q')^T.                            (8)

For example A=M_11-p_1 q_1 B+e f. The coefficients A,B are uniquely
determined on the generic parameter locus; covariance makes them
O(2)-invariant, and hence invariant as polynomials everywhere.

For completeness, the scalar invariant ring is

    C[P,Q']^O(2)=C[sigma,tau,c],
    sigma=p_1^2+p_2^2, tau=q_1^2+q_2^2, c=p_1q_1+p_2q_2. (9)

Indeed in complex coordinates p_+=p_1+i p_2, p_-=p_1-i p_2 and q_+,
q_-, rotations have torus weights +1,-1. Weight-zero monomials are
generated by sigma=p_+p_-, tau=q_+q_-, z=p_+q_-, w=p_-q_+, with
zw=sigma tau. Reflection exchanges z,w. Symmetric polynomials in z,w
reduce to z+w=2c and zw=sigma tau. This proves (9). The three
generators are algebraically independent: the axis substitution

    sigma=s^2+a^2, tau=b^2, c=ab                    (10)

is injective on C[sigma,tau,c]. For b!=0 it attains every complex
(sigma,tau,c) with tau!=0 by taking complex square roots. Thus a
polynomial vanishing on its image is identically zero.

Regard A,B in (8) henceforth as polynomials in sigma,tau,c.

## 5. The first finite-polynomial ODE kills the offdiagonal coefficient

At q_1=0, differentiate M_12 with respect to q_1. The fourth boundary
of (4), paired with E_v(p_2x+q_2y), gives

    partial_(q_1)M_12=-d p_1 M_12.                  (11)

From (7),(8), the left side at q_1=0 is p_1^2 q_2 B_c; the right side
is -d p_1^2 q_2 B. Cancelling auxiliary monomials and using the
injective substitution (10) proves the polynomial identity

    B_c+d B=0.                                      (12)

d!=0 is a fixed complex scalar. A finite polynomial in c cannot satisfy
(12) unless B=0: its highest c coefficient must first be zero, and
descending induction removes every coefficient. Consequently

    Nmat=A(sigma,tau,c) I_2.                         (13)

Finiteness is essential; an unrestricted exponential series would
admit B=exp(-dc) times a function of sigma,tau. Here the actual mean
and every kernel coefficient are finite polynomials.

## 6. The second finite-polynomial ODE extracts the endpoint

Set q_1=0 but keep p_1,p_2,q_2 independent. By (6),

    Nmat_22=K(E(p_1x), E_uv(p_2x+q_2y)+eE(p_2x+q_2y)).

The pure-h receiving coefficient of the second tensor is exactly eta.
Every positive B-only mean monomer prevents an all-h output, so only
its constant mean term survives; that term is E_uv(0)+eF=eta h^U
by (4). Differentiate the displayed equality in q_1 before setting
q_1=0. The third boundary of (4) then gives

    partial_(q_1)Nmat_22=p_1 beta eta-d p_1 Nmat_22.  (14)

By (13), the left side is p_1 A_c: the tau derivative has factor q_1
and vanishes on this axis. Cancel p_1 and use (10). We obtain

    A_c+d A=beta eta.                               (15)

Again A is a finite polynomial and d!=0, so the sole solution is
A=beta eta/d, independent of all three invariants. At all parameters
zero, (6) and the HH pair top give

    A(0)=K(F,E_uv(0)+eF)=eta K(F,h^U)=eta alpha.

Since eta!=0, beta=d alpha. This proves (2).

## 7. Matching consequence and the precise proof boundary

If beta!=0, expand the literal hafnian at any p:

    beta=sum_(q!=p) B_pq haf(B[V without p,q]).

Each supported summand equals beta by (2), so deg_B(p) beta=beta.
In characteristic zero this forces deg_B(p)=1. Every vertex is thus
on one isolated B edge, with all matching weights nonzero. The same
argument applies to all three colors of an actual diagonal ternary
source with three nonzero amplitudes, because the original whole odd
tower is available separately for each binary palette.

The existing global diagonal reduction then reduces the original
weighted conjecture to three supported colored perfect matchings.
The reviewed three-matching obstruction supplies a mixed colored
perfect matching for n>=6, whose receiving coefficient is a unique
nonzero monomial. The final graph step is independent of this kernel
proof and must be checked with those existing foundations in the
complete proof audit. No generic inverse or candidate inheritance is
used in the new endpoint argument.

At n=4 the endpoint theorem remains valid and forces matching colors;
the final obstruction is not asserted. The three distinct perfect
matchings of K4 do give the usual three-color diagonal source. For
N=2 the finite mean, derivative, and oversized-zero conventions above
remain literal, including the terminal odd degree three in (1).

This is a provisional complete new endpoint proof, pending independent
audits of the saved text and the full chain of earlier foundations.
It is not yet a public resolution announcement. Only this fresh source
is written; previous receipts and canonical files are unchanged.
