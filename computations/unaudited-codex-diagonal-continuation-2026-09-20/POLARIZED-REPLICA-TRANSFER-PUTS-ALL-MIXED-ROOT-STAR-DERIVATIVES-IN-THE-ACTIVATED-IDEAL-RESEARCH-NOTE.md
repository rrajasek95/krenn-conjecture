# Polarized replica transfer eliminates every mixed second root-star error

UNFROZEN analytic research by /root/audit_det_bridge and /root,
2026-09-26; independently reconstructed by /root/global_bridge.
Complete independent analytic audit requested. This is a first-power
identity in the ORIGINAL activated ideal, with no localization at the
variable hafnian and no assumption of derivative stability. It is a
new constraint on a hypothetical full source, not general conjecture
closure or a source-preserving finite operation.

## 1. Fixed binary partners and the exact theorem

Let |V|=2m>=4. Fix symmetric hollow C,H whose WHOLE diagonal
binary top has exactly the two nonzero pure amplitudes tau_C,tau_H.
Let B be a variable symmetric hollow matrix, beta=haf(B), and let
R=C[b_ij:i<j]. The ordinary activated ideal is exactly

    I=<haf(B[W]): W proper nonempty even,
                    whole C/H tensor on V without W is nonzero>.

Thus the candidate whole top equals beta b^V+tau_C c^V+tau_H h^V
modulo I. The [reviewed first-power reflection/covariance theorem](ACTIVATED-MATCHING-IDEAL-CONTAINS-ACTUAL-INVERSE-DEFECTS-AND-MIDDLE-QUARTIC-RESEARCH-NOTE.md)
supplies two polynomial inputs: every coefficient of every candidate
B/H higher odd response belongs to I, and the ACTUAL cofactor defect
B C(B)-beta I_V belongs entrywise to I. These inputs are valid even
on the nonreduced scheme and with beta zero. They are not a geometric
three-active-source theorem applied inside R/I.

For a physical root p put

    D_p=sum_(i<j; i,j!=p) b_pi b_pj partial_(b_ij).

**Theorem.** For every DISTINCT pair p,q, exactly

    D_p D_q beta belongs to I.                         (1)

In particular every ACTUAL original full ternary source satisfies
D_p D_q haf(B)=0, separately for each of its three color matrices.
The repeated-root version D_p^2 beta in I is already supplied by
the pure higher-response theorem; (1) controls two different frames.
No conclusion D_p(I) subset I, flow invariance, or strict descent
follows from (1).

## 2. Whole retained tensors and all direct-edge terms

Fix p!=q and U=V without p,q, N=|U|. Work in the B/H palette on
these retained physical sites. Write Q for its ACTUAL retained
quadratic and Q^[r]=Q^r/r!. Define monochromatic rows

    x=sum_(i in U) B_pi b_i,  y=sum_(i in U) B_qi b_i,
    u=sum_(i in U) H_pi h_i,  v=sum_(i in U) H_qi h_i,
    d=B_pq,  e=H_pq.

For any EVEN row multiset A define its WHOLE binary tensor

    T(A)=(product of its rows) Q^[(N-|A|)/2],  F=T(empty).

Set T(A)=0 when |A|>N. Repeated rows are RAW powers, not divided
powers. All equalities from here through Section 5 are in R/I.
They are therefore exact first-power coefficient statements.

The four root-pair slices of the whole candidate top give

    T(xy)=beta b^U-dF,      T(uv)=tau_H h^U-eF,
    T(xv)=T(yu)=0.                                    (2)

The original-scheme WHOLE binary cubic responses give

    T(x^3 y)=-3d T(x^2),  T(x y^3)=-3d T(y^2),
    T(x^3 v)=T(y^3 u)=0,
    T(x^2 u y)=-2d T(xu),  T(x y^2 v)=-2d T(yv),
    T(x^2 uv)=-e T(x^2),  T(y^2 uv)=-e T(y^2).        (3)

For example, at root p the B^2 H departure product, with q
receiving B, has two choices to use the direct B departure at q:
its exact coefficient is T(x^2 u y)+2d T(xu). With q receiving
H it is T(x^2 uv)+e T(x^2). The pure B cube at p similarly
gives the first and third equations, and root q gives the others.
These are WHOLE receiving tensors, whose coefficients lie in I
by the polynomial input in Section 1. No candidate inheritance or
deletion of a retained mixed coefficient has been assumed.

## 3. The exact polarized replica-transfer identity

For whole binary tensors Z,W on even U use the symmetric pairing

    K(Z,W)=sum_(S subset U) (-1)^|S|
       Z(b on S,h off S) W(h on S,b off S).

Thus K(h^U,Z)=[b^U]Z and K(b^U,Z)=[h^U]Z. Abbreviate
K(A;B)=K(T(A),T(B)) for row multisets. For ANY two ODD
multisets A,B the universal polynomial identity is

    sum_(a in A) K(A without a; B with a)
      =sum_(b in B) K(A with b; B without b).           (4)

Each occurrence is counted, so repeated-row multiplicities are
literal integers. This identity does not require source equations.

Proof: the finite even mean is
E(L)=sum_j L^(2j)Q^[N/2-j]/(2j)!. In two independent identical
Wick replicas, the product of local B/H determinants is invariant
under their simultaneous SO2 rotation. Therefore

    K(E(cL+sM),E(-sL+cM))=K(E(L),E(M)), c^2+s^2=1.

Its infinitesimal relation is M.partial_L-L.partial_M=0.
Extracting the coefficient for the odd row multisets A in L and
B in M gives (4), after multiplying the raw factorials. This is
a finite polynomial identity of actual Wick tensors. Rotating
proof replicas is not a transformation of the source or its axes.
Pairing a tensor with coefficients in I against any polynomial
tensor again has its scalar value in I; no derivative of I is used.

## 4. Six short transfers keep the boundary corrections explicit

Use the scalar abbreviations

    S=K(x^2;y^2),       R_0=K(xu;yv),
    J=K(empty;x^2 y^2 uv),  W=K(uv;x^2 y^2),
    F_4=K(empty;x^2 y^2),   F_6=K(empty;x^3 y^3),
    C_0=K(x^3 u;y^3 v), D_0=K(x^2;x y^3 uv),
    E_0=K(xu;x^2 y^3 v), F_8=K(empty;x^3 y^3 uv),
    Z=K(uv;x^3 y^3).

Apply (4) to the following multisets, substituting (2),(3):

| A | B | Exact resulting identity modulo I |
| --- | --- | --- |
| x^3 | y^3 uv | C_0=3D_0-9deS |
| x^2 u | x y^3 v | 2E_0+D_0=C_0+12d^2 R_0+3deS |
| x | x^2 y^3 uv | F_8=E_0+2D_0-3dJ |
| u | x^3 y^3 v | F_8=Z+3E_0 |
| u | x^2 y^2 v | J=-4d R_0+W |
| x | x^2 y^3 | F_6=-6dS-3dF_4 |

Here terms K(T(xy),T(x^2 y^2 uv)) contribute -dJ because
the beta b^U contribution pairs against the all-H coefficient
of a tensor containing B monomers, which is structurally zero.
The same observation gives -dF_4 in the last line. Mixed-pair
terms involving T(xv) or T(yu) are zero by (2), and the remaining
cross quartics reduce by (3). Thus none is discarded merely
because its pure receiving coefficient vanishes.

Eliminating C_0,D_0,E_0,F_8,R_0 using the first five lines gives

    Z=6deS-3dW.                                      (5)

The sixth line retains the other correction F_4 explicitly.
All these computations use integer coefficients and polynomial
multipliers, with no cancellation of d,e,beta or a matching sum.

## 5. The two H completions cancel the remaining corrections

Set

    Phi_22=[b^U]T(x^2 y^2),  Phi_33=[b^U]T(x^3 y^3).

Pair T(uv)=tau_H h^U-eF with the two B response tensors. It gives

    W=tau_H Phi_22-eF_4,
    tau_H Phi_33=eF_6+Z.                              (6)

Substitute (5), the last transfer, and the first equation of (6):

    tau_H Phi_33
      =e(-6dS-3dF_4)+6deS-3d(tau_H Phi_22-eF_4)
      =-3d tau_H Phi_22.

Only the fixed NONZERO scalar tau_H is canceled. We have proved
the first-power ordinary-ideal statement

    Phi_33+3d Phi_22 belongs to I.                    (7)

This holds at all pairs, including d=0 and e=0, and does not
require a nonzero complementary H hafnian. For d=0 it says
Phi_33 belongs to I+(d) even if d itself is not in I; at a live
cofactor-active H edge the stronger d in I is already known.
No localization at d is used. The formulas remain valid at n=4,6
with oversized departure tensors set to zero.

Let A=B[U], L=C(A) be ACTUAL scalar cofactors, and k=x^T L y
in scalar B coordinates. The first-power inverse-defect identity
from Section 1 gives, by its literal root/core block,

    Phi_22+2d k belongs to I.                         (8)

The [generic mixed-star identity](MIXED-ROOT-STAR-DERIVATIVES-HAVE-GAUGE-BRACKETS-AND-SIX-MONOMER-OBSTRUCTIONS-RESEARCH-NOTE.md)
is an equality in the full polynomial ring:

    D_p D_q beta=3d^2 k+(9d/4)Phi_22+Phi_33/4.

Combining it with (7),(8) proves the explicit decomposition

    D_p D_q beta
      =(Phi_33+3d Phi_22)/4+(3d/2)(Phi_22+2d k) in I. (9)

This proves (1) on the original possibly nonreduced activated
scheme, with no nonzero variable amplitude assumption.

## 6. Verification and remaining scope

The stdlib [checker](verify_polarized_even_mean_transfer.py) builds
ONE generic eight-site retained binary Wick tensor with fixed
integer covariance matrices and four fixed row vectors. It uses
raw site-square-zero row multiplication and actual hafnian
recursion. All six polarized transfer identities pass literally;
the independent equal-mean coefficient identity

    K(F;T(x^3 y^3))=K(x^2;x y^3)
                  +3K(xy;x^2 y^2)+K(y^2;x^3 y)

also passes. The deterministic [saved output](polarized_even_mean_transfer_results.json)
records every exact input and value. This check tests normalization
of a generic universal identity, not the conjecture at one order
or any scalar/full-source family. The analytic proof supplies
the all-order identities and the ideal consequences.

Equation (9) removes the symmetric six-monomer second-root error
left in the preceding note. It uses the genuinely coupled cubic
and mixed root-pair equations. It does not show that higher
compositions of different root operations vanish, that their
generator ideals are derivative-stable, or that a finite operation
preserves all full mixed coefficients. It gives no strict descent,
scalar converse, matching classification, or new excluded order.
The general conjecture remains OPEN. Prior bound objects and
canonical files are held unchanged; only this new package is written.
