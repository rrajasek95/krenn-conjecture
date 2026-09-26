# Three active target colors force every higher pure response to vanish

**Status.** Exact all-order research theorem, 2026-09-12;
[independent full mathematical audit PASS](UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING-AUDIT.md). Written by `/root/dense_nontree`, using
the finite-polynomial cancellation identified by `/root` in the
three-replica calculation. The proof below uses a simpler two-replica
translation identity. The general conjecture remains open.

## 1. Actual source, hypotheses and theorem

Work over C in the commutative physical-site-square-zero algebra: any
product of two coordinates at the same physical site is zero. Let Omega
have N=2m+1>=3 sites, each with ternary local color space having basis
a,b,c. Let R be an actual ordinary quadratic on distinct physical pairs,
and put R^[j]=R^j/j!.

Let D be any linear space of actual rows on this SAME R such that

    Phi(L)=L R^[m]=f_a(L) a^Omega+f_b(L) b^Omega+f_c(L) c^Omega,
    L in D.                                                     (1)

Assume that all THREE linear functions f_a,f_b,f_c are nonzero, and
that their joint image has dimension at least TWO. They need not all
be independent. A full ordinary ternary source supplies such a space
at any root, with image dimension three.

**Theorem.** For every 1<=r<=m, every designated color h, and all rows
L_0,...,L_(2r) in D,

    [h^Omega] L_0 ... L_(2r) R^[m-r]=0.                         (2)

Every mixed coefficient using only two designated colors is also zero.
Thus these entire higher odd product responses are supported only on
words using ALL THREE designated colors. They are not asserted to be
zero tensors.

The result is uniform in order, density and complex weights. It needs
no source minimum, anchor, sparse row, kernel, selected graph, or
positivity hypothesis.

## 2. Two reviewed inputs and the finite generating tensor

The [common-factor theorem](UNIFORM-ALL-ODD-DIAGONAL-RESPONSE-FACTORS-AND-NULL-PAIR-TRANSFER.md)
gives unique homogeneous polynomials q_r of degree 2r on D, with q_0=1,
such that

    [h^Omega] H_(2r+1)(L)=f_h(L) q_r(L),
    H_(2r+1)(L)=L^(2r+1) R^[m-r].                              (3)

Its hypothesis is joint target-image rank at least two, as assumed here.
The [sitewise reflection theorem](UNIFORM-ALL-ODD-TWO-COLOR-MIXED-VANISHING-AND-KERNEL-PENCIL.md)
says that a higher mixed word avoiding an active color has coefficient
zero. Each binary mixed word avoids one of our three active colors, so
all binary mixed coefficients vanish on D. This use requires all three
coordinate functions to be nonzero, not that their joint rank be three.

Define the finite whole tensor and the finite even polynomial

    Psi(L)=sum_(r=0)^m H_(2r+1)(L)/(2r+1)!,
    G(L)=sum_(r=0)^m q_r(L)/(2r+1)!.                            (4)

Consequently

    Psi(L)=G(L) Phi(L)+E(L),                                  (5)

where E(L) is supported only on all-three-color words. In particular
G(0)=1 and G(-L)=G(L). No formal infinite series or convergence assertion
is involved.

## 3. Exact two-replica translation covariance

For clarity, this identity is proved for arbitrary actual R and rows
L,M; diagonal-response hypotheses are not needed until Section 4.

Introduce formal variables X_(i,h) with symmetric covariances equal to
the actual R coefficients at distinct sites, and zero within a site.
Their Wick functional is the finite sum over pairings of labeled
variables, with odd moments zero. It is algebraic and does not require
a positive or nonsingular covariance matrix.

For a word w, expand the shifted physical moment

    Wick product_(i in Omega) (X_(i,w_i)+L_i(w_i)).              (6)

If d sites contribute their means, the remaining N-d variables must
pair, so d is odd. The contribution from all subsets of d sites is
the coefficient of L^d R^[(N-d)/2]/d!. The factor d! in the raw row
power counts its ordered choices of distinct physical sites; the
divided power of R counts each remaining matching once. Therefore
(6) is exactly [w]Psi(L), with the factorials in (4).

Choose any two distinct local axes a,b, fixed across the sites. For
whole tensors T,U define the alternating contraction

    B_ab(T,U)=sum_(I subset Omega) (-1)^|I|
      T(a off I,b on I) U(b off I,a on I).                      (7)

It is alternating because N is odd. In two independent identical
replicas X,Y, the moment of the product of local determinants

    (X_(i,a)+L_i(a))(Y_(i,b)+M_i(b))
      -(X_(i,b)+L_i(b))(Y_(i,a)+M_i(a))

equals B_ab(Psi(L),Psi(M)) by replica independence and (6).

For any c,s in C satisfying c^2+s^2=1, the simultaneous substitutions

    X'=cX+sY,       Y'=-sX+cY,
    L'=cL+sM,       M'=-sL+cM                                  (8)

preserve the complete replicated covariance. They also preserve every
displayed local determinant, since the two-column transformation has
determinant one. The Wick pairing definition is invariant under a
covariance-preserving substitution. It follows that

    B_ab(Psi(cL+sM),Psi(-sL+cM))=B_ab(Psi(L),Psi(M)).             (9)

This is an identity on the SAME actual R. The replicas are proof
variables; (8) is not a local basis change of the source or its target.
No reflection is assumed to fix two or three independent auxiliaries.

## 4. Cancellation forces G to be constant

Relabel the colors so that f_a,f_b are independent, which is possible
by the rank premise. Restricting Psi(L) to words using only a,b leaves
exactly

    G(L)(f_a(L) a^Omega+f_b(L) b^Omega).                       (10)

Indeed its binary mixed words vanish by the active third color c, and
its all-three-color words are absent from this restriction. Thus

    B_ab(Psi(L),Psi(M))=Delta(L,M) G(L)G(M),
    Delta(L,M)=f_a(L)f_b(M)-f_b(L)f_a(M).                       (11)

The determinant Delta is a nonzero polynomial on D x D. Under (8) it
is unchanged. Equations (9)-(11) therefore imply, in the integral
domain C[D x D],

    G(cL+sM)G(-sL+cM)=G(L)G(M).                               (12)

Cancellation is of the nonzero polynomial Delta, not its value at a
particular pair. Hence (12) holds also at pairs for which Delta=0.

Choose c=s=1/sqrt(2), and only NOW specialize M=0. Evenness and G(0)=1
give the polynomial identity

    G(L/sqrt(2))^2=G(L).                                      (13)

If G had positive total degree d, its nonzero highest homogeneous part
would give degree 2d on the left and degree d on the right. A nonzero
polynomial does not have square zero over C. Therefore G is constant,
and G(0)=1 forces G=1.

The terms q_r/(2r+1)! in (4) have distinct homogeneous degrees. Hence

    q_r=0 identically on D,     1<=r<=m.                       (14)

Equation (3) proves the repeated-row version of (2). Substituting
L=sum_j t_j L_j and extracting t_0...t_(2r) yields (2), after dividing
by (2r+1)!. The reviewed binary mixed vanishing admits the same full
polarization. This proves the stated whole-support restriction.

## 5. Exact consequences for ordinary quadratic changes

Let S be any element of the PHYSICAL image of Sym^2 D: explicitly,
S is a finite complex linear combination of ordinary products U V
with U,V in D, formed in the physical-site-square-zero algebra.
There is no kernel condition. Such S is an ordinary quadratic on the
same site set, though it may introduce new physical pairs or entries.

For every C in D the complete finite expansion is

    C (R+S)^[m]=sum_(j=0)^m (1/j!) C S^j R^[m-j]
              =Phi(C)+E_C(S),                                 (15)

where every word of E_C(S) uses all three colors. For j>=1, each term
in the expanded product contains 2j+1 rows from D, so (2) and binary
mixed vanishing apply directly. The remainder is linear in C and
E_C(0)=0. All three original pure coefficients are exactly unchanged;
no target rescaling or potentially zero common scalar is needed.

In particular, for the reviewed kernel-pair pencil R+tUV, the scalar
polynomial p_(U,V)(t) is identically one. More generally (15) applies
to U,V in D even when their whole original responses are nonzero.
The deformed response may contain E_C(S), so membership of C in the
diagonal-response space of R+S is not asserted.

In the reviewed null-pair transfer, if its LOWER core satisfies this
note's three-active-color and rank premises, the bilinear pure factor
B=Q_1 is zero. Its common pair matrix is therefore exactly the original
pair block J. This conclusion does not follow merely because a larger
source has three targets: a lower coordinate a,b target plane with
f_c=0 is outside the present theorem.

## 6. Exact controls and remaining scope

The third-active-color condition cannot be dropped from this argument.
On sites 0,1,2 take the actual quadratic and rows

    R=b_0 b_1+a_1 a_2+b_0 a_2,
    U=a_1-b_0,       V=b_1-a_2,
    D=span{a_0,b_2,U,V}.

Direct multiplication gives U R=V R=0, a_0 R=a^Omega and b_2 R=b^Omega.
For L=alpha a_0+beta b_2+sU+tV,

    Phi(L)=alpha a^Omega+beta b^Omega,
    [a^Omega]L^3=-6 alpha s t,
    [b^Omega]L^3=-6 beta s t.                                (16)

Thus the common q_1=-6st is nonzero on this actual rank-two coordinate
binary frame. There is no active third target; it is not a full ternary
source or a counterexample to the theorem.

Nonzero whole higher responses remain possible under the full premises.
For the actual allowed four-site source, use its three-site core

    R=a_2 a_3+b_1 b_3+c_1 c_2,
    D=span{a_1,b_2,c_3}.

Then Phi(alpha a_1+beta b_2+gamma c_3) is the full diagonal tensor,
but L^3=6 alpha beta gamma a_1 b_2 c_3. Here q_1=0, as proved, while
the higher mixed tensor is nonzero. The map Phi on this D is injective.
Taking S=t a_1 b_2, formula (15) becomes

    c_3(R+S)=c^Omega+t a_1 b_2 c_3.                            (17)

Thus exact pure transfer does not make an arbitrary quadratic change
a valid normalization. It does not guarantee a kernel, a useful S,
zero mixed errors, old-anchor preservation, entry decrease, or descent.
No minimum-order contradiction or arbitrary-source coverage follows
without an additional argument controlling the all-three-color terms.


**Integration provenance.** The independently audited frozen source is
/tmp/krenn_three_active_color_higher_pure_response_vanishing_20260912.md, SHA256
06e567224b4687f5f9456f497001a756073ad39054990b78d4bcf0a1526e246d.
This repository copy updates status, links and this provenance paragraph;
the mathematical body is unchanged. The accompanying audit is byte-exact.
