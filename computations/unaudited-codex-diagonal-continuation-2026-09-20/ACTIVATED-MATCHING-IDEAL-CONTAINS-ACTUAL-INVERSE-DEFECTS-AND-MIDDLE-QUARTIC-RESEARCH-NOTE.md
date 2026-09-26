# Activated matching equations contain actual inverse defects in first power

UNFROZEN analytic research by /root/global_bridge, 2026-09-26.
Independent analytic audit requested. This is an exact polynomial
consequence of the full activated equations. It does not assume
candidate cubic inheritance, a radical ideal, or a nonzero candidate
pure amplitude, and it does not construct a strict source descent.
The general weighted Krenn--Gu conjecture remains OPEN.

## 1. Fixed binary pair and the literal activated ideal

Let |V|=2m>=4. Fix symmetric zero-diagonal matrices C,H whose
WHOLE diagonal two-color top is

    (A_C+A_H)^[m]=tau_C c^V+tau_H h^V,
    tau_C tau_H!=0,              Q^[j]=Q^j/j!.

Let B be a VARIABLE symmetric zero-diagonal third-color matrix,
with polynomial ring R=C[b_ij:i<j]. Put f_U=haf(B[U]),
beta=f_V, and let F_CH(W) be the whole fixed binary tensor on W.
Define exactly

    Z={proper nonempty even U subset V: F_CH(V without U)!=0},
    I=<f_U: U in Z> subset R.                            (1)

This is also the ideal of ALL candidate mixed full top coefficients.
Indeed each word with third-color set U has coefficient f_U times
one fixed coefficient of F_CH(V without U). If that fixed tensor
is nonzero, one coefficient is a nonzero complex scalar and thus
a unit. Words without the third color already obey the fixed binary
top. Odd third-color subsets have no matching. This proves equality
of the two ideals, not just equality of their zero sets.

Modulo I the complete candidate top is therefore

    beta b^V+tau_C c^V+tau_H h^V.                        (2)

The formal beta need NOT be a unit or nonzero in R/I. No geometric
full-source theorem is applied to this possibly nonreduced ring.
We instead use universal polynomial reflection and covariance.

The [matching-context formulation](MATCHING-CONTEXT-HAFNIAN-IDEAL-CERTIFICATES-AND-RADICAL-GAP-RESEARCH-CHECKPOINT.md)
defines (1). The two polynomial identities used below are the
reviewed [reflection identity](TWO-REPLICA-REFLECTION-GIVES-DEGREE-ONE-THIRD-COLOR-CERTIFICATES-RESEARCH-NOTE.md)
and [finite-mean covariance](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING.md).

## 2. Candidate higher B/H responses belong to the ideal

Fix p, put Omega=V without p, and let R_p be the candidate quadratic
off p. Its literal root rows are Y_B,Y_C,Y_H. Let

    L=sY_B+tY_H+uY_C,
    Phi(L)=L R_p^[m-1],
    T_d(L)=L^d R_p^[m-1-r],       d=2r+1, 1<=r<=m-1.

For ANY b/h word w on Omega, let w_I equal c on I and w off I,
and let w'_I equal w on I and c off I. Universal reflection gives

    sum_(I subset Omega) (-1)^|I|
                  T_d(L)(w_I) Phi(L)(w'_I)=0.           (3)

This identity is polynomial in B, so it is valid in R and R/I.
The I=empty term is exactly

    u tau_C [w](sY_B+tY_H)^d R_p^[m-1-r].

The I=Omega term is identically zero. Its first factor receives
only c and hence equals u^d times the fixed pure C higher response.
That pure response is zero: the fixed full C/H pair has zero pure
higher odd receiving coefficients by the reflection calculation
in Section 5 of the linked certificate source. This uses both fixed
nonzero amplitudes and makes no assumption about B.

For proper nonempty I, every coefficient of Phi(L)(w'_I) is an
actual mixed full top coefficient: the retained word contains at
least one c and at least one b or h. Thus it is in I. Consequently
EVERY coefficient of the candidate B/H higher response is in I.
The word w may be pure or mixed. In particular there is an explicit
first-power representation

    tau_C [s^a t^(d-a)] [w](sY_B+tY_H)^d R_p^[m-1-r]
      =sum_(empty!=I proper subset Omega) (-1)^(|I|+1)
         [s^a t^(d-a) u] T_d(L)(w_I) Phi(L)(w'_I).      (4)

The scalar parameter coefficient includes its raw binomial factor;
division by binomial(d,a), if desired, divides the whole equation.
Only the fixed nonzero complex scalar tau_C is divided out. No
candidate hafnian or polynomial in R/I is canceled. Formula (4)
retains all actual matching sums in every mixed top generator.

## 3. Candidate even omissions belong to the ideal in first power

Fix v!=p, set S=V without p,v, and let W be the actual candidate
quadratic on S. In this section L=sY_B+tY_H, U=L restricted to S,
and V_H is the unchanged H row from v into S. Put

    F=W^[m-1],
    E(U)=sum_(j=0)^(m-1) U^(2j)/(2j)! W^[m-1-j].

Let pi_bh project each S site onto its b,h axes. The COMPLETE
v=h coefficient of the finite odd mean at p is, literally,

    P_H(L)=pi_bh( d_H(L) E(U)+partial_(V_H) E(U) ),
    d_H(L)=t H[p,v].

Define its error against the fixed pure target by

    Err_H(L)=P_H(L)-t tau_H h^S.                        (5)

Every coefficient of Err_H(L) belongs to I. The degree-one mean
term has only its fixed h target modulo I by (2); higher terms are
in I by (4). This is a derivation of candidate response membership,
not an assertion that original response zeros survive a repair.

Let B_pair be the product of the local alternating b/h pairings
on the EVEN set S, normalized as in the covariance source. It is
symmetric and satisfies B_pair(Z,h^S)=[b^S]Z. The universal exact
mean identities are

    B_pair(E(U),E(U))=B_pair(F,E(sqrt(2)U)),
    B_pair(E(U),partial_V E(U))
        =(1/sqrt(2)) B_pair(F,partial_V E(sqrt(2)U)).

Use V=V_H in the second equation and substitute (5) at L and
sqrt(2)L. The complete d_H terms cancel by the first equation.
What remains is the exact polynomial ERROR identity

    t tau_H [b^S](E(U)-F)
       =(1/sqrt(2)) B_pair(F,Err_H(sqrt(2)L))
                       -B_pair(E(U),Err_H(L)).          (6)

In particular the right side is in I[s,t]. Rather than canceling
anything in a quotient ring, extract [s^(2r)t] in (6). Since pure
b receiving selects only the B row and B core, this gives

    E_(p,v,r)=[b^S](Y_B restricted to S)^(2r)
                             (A_B restricted to S)^[m-1-r]
      =((2r)!/tau_H) [s^(2r)t]
          { (1/sqrt(2)) B_pair(F,Err_H(sqrt(2)L))
                           -B_pair(E(U),Err_H(L)) } in I, (7)

for every r=1,...,m-1. This explicit first-power identity uses
the fixed unit tau_H; it needs neither reducedness of I nor a
nonzero beta. Combining (4),(5),(7) gives actual polynomial
multipliers for the original activated hafnian generators.

There is a useful localized consequence of the B vertex grading.
The polynomial E_(p,v,r) has degree 2r at p, degree zero at v,
and degree one at each S vertex. Each f_U has degree 1_U.
Projecting an ideal representation onto this multidegree removes
every generator whose U contains v. Thus already

    E_(p,v,r) in <f_U: U in Z, v notin U>.              (8)

No chosen nonzero matching term replaces any hafnian in this claim.

## 4. Actual cofactor inverse defects and the middle quartic

Let K=C(B) be the ACTUAL deleted-pair hafnian matrix, zero on
its diagonal. The diagonal entries of BK are identically beta
by ordinary hafnian expansion. For p!=v, expansion at the retained
p in K[j,v] gives exactly

    (BK)[p,v]=E_(p,v,1).                                (9)

The two ordered departures occur on both sides of (9); there is
no factor one half. Equations (7)--(9) prove the entrywise identity

    BK-beta I_V belongs to Mat_V(I).                    (10)

This strengthens the geometric necessity to FIRST-POWER membership
in the activated ideal, even on its nonreduced scheme and when the
candidate pure amplitude vanishes. It does not make B invertible
in R/I, and does not say beta belongs to I or its radical.

Now fix two roots p,q, their literal retained A=B[V without p,q],
and write x=B[p,U], y=B[q,U], d=B[p,q], L_A=C(A). Let S_A and Phi
be the actual four-deletion response of the reviewed
[zero-core compatibility theorem](ZERO-CORE-TWO-ROOT-SCALAR-ERRORS-COMPRESS-TO-THREE-QUARTIC-COORDINATES-RESEARCH-NOTE.md).
Literal matching expansion, without any scalar assumption, gives

    sum_(v in U) y_v (BK)[p,v]
        =2d x^T L_A y+Phi(x,x,y,y).                     (11)

If the fixed H has eta_H=haf(H[V without p,q])!=0, then d itself
is in I from the mixed word B at p,q and H on U. Combining
(10),(11) therefore proves

    Phi(x,x,y,y) in I.                                 (12)

This is an exact activated-equation implication for candidate rows,
not inherited original cubic vanishing. If one also fixes a live H
edge, its opposite mixed word gives haf(A) in I. This is ideal
membership for the variable core, and haf(A)=0 at points of V(I);
it is not an identity haf(A)=0 in the full polynomial ring. At an
ACTUAL original source the retained core has haf(A)=0 as in the
[original endpoint-plane theorem](LIVE-COFACTOR-ACTIVE-EDGES-FORCE-NULL-ORIGINAL-ENDPOINT-QUARTIC-PLANES-RESEARCH-NOTE.md).
The base-free candidate core equation and nonzero amplitude still
have to be found. Equations (10),(12) alone are not such a construction.

## 5. The quadratic middle error is an activated second-order obstruction

Specialize to an ACTUAL original full source, fix C,H and the literal
retained B core, and impose d=0 at a live cofactor-active H edge.
Write x=x_0+r, y=y_0+s. All pulled-back activated generators have
the exact form

    g_i(r,s)=ell_i(r,s)+b_i(r,s),

where ell_i is linear and b_i is bilinear (possibly zero), with no
constant term. This follows by literal expansion on each activated
subset, keeping every quadratic edge of the fixed core. It is the
whole-volume version of the reviewed
[two-root activated system](ACTIVATED-TWO-ROOT-BILINEAR-EQUATIONS-AND-ONE-SIDED-PROJECTIVE-FINITENESS-RESEARCH-NOTE.md).
If the original component cut is preserved, its nonzero exterior
factors are retained exactly as in that source. No assumption that
p,q originally lie in the same B component is needed here.

The original arbitrary-vector quartic identities make the constant
and linear terms of Phi(x,x,y,y) zero. Its quadratic term is

    Q(r,s)=Phi(r,r,y_0,y_0)+4Phi(r,x_0,s,y_0)
                                      +Phi(x_0,x_0,s,s).

By (12), write Phi(x,x,y,y)=sum_i P_i(r,s)g_i(r,s).
Let c_i=P_i(0), and let P_i^(1) be the linear part of P_i.
Comparing linear and quadratic terms gives the EXACT relations

    sum_i c_i ell_i=0,
    Q=sum_i c_i b_i+sum_i P_i^(1) ell_i.                (13)

Thus modulo the activated linearizations, Q is a cokernel
combination of the original bilinear activation terms. It is not
an additional independent second-order equation beyond them.
This does NOT assert that the linearizations alone kill Q.

For example, any formal candidate (r,s)=t v+t^2 a satisfying
every g_i=0 modulo t^3 has ell_i(v)=0 and
ell_i(a)+b_i(v)=0. Equation (13) then forces Q(v)=0 exactly.
No actual smooth curve, candidate cubic inheritance, or integration
of that second-order solution has been assumed. If the core varies,
its four-deletion tensor also varies; this fixed-core Q statement
does not omit those extra derivatives.

## 6. What this bridge does and does not resolve

The universal identities convert the remaining middle quartic into
the actual activated ideal in FIRST power and identify its tangent
quadratic as one existing coupled second-order obstruction. They
avoid importing original higher responses onto changed rows.

They supply no reason that every colored-cell minimum has a
non-gauge tangent, a second-order compatible direction, or a finite
support-contained descent. The original activated system can still
leave only its original gauge class. No radical membership of beta,
third-color certificate for every fixed pair, or new excluded order
is proved. The general conjecture remains OPEN.

Only this distinct unfrozen note is written. All current/prior
receipt-bound sources and audits, the 1248-record baseline,
PROOF-SKETCH.md and the external README remain unchanged.
