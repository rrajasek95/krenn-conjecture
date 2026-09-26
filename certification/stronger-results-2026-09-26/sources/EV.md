# Every positive even omission response has zero pure coefficients

**Status.** Exact all-order theorem, 2026-09-13, by
`/root/dense_nontree`; [complete independent audit PASS](UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING-AUDIT.md). The retained-vacuum
calculation and its all-even extension were independently reconstructed
by `/root`. No general source exclusion or successful pair operation
is claimed. The original proof was frozen before research integration.

## 1. Actual odd core and the all-even omission theorem

Work over C in the commutative physical-site-square-zero algebra,
with divided powers R^[j]=R^j/j!. Let R be an actual ordinary quadratic
on Omega, |Omega|=2m+1>=3, with designated ternary axes a,b,c. Let D be
a linear space of actual rows on this SAME R satisfying

    L R^[m]=sum_(h=a,b,c) f_h(L) h^Omega,       L in D.   (1)

Assume every f_h is a nonzero linear function and their joint image
has dimension at least TWO. They need not be independent. Fix ANY
site q, put S=Omega without q, and set

    Q=R restricted to S,       F=Q^[m],
    U(L)=L restricted to S.

**Theorem.** For each 1<=r<=m, every color k, and arbitrary rows
L_1,...,L_(2r) in D,

    [k^S] U(L_1)...U(L_(2r)) Q^[m-r]=0.                 (2)

The restriction Q is the literal omitted-site core. No pure cofactor,
whole kernel row, selected support, nonedge, direct-block rank, source
minimum or positivity is assumed. The proof does not divide by F.
Additional finite local dimensions are permitted by first projecting
onto the designated ternary axes: this preserves (1), its target rank,
and every coefficient in (2).

The [reviewed higher-response theorem](/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md)
says that every higher odd response on D has zero pure and two-color
mixed coefficients. The proof below uses that whole binary conclusion,
not just the vanishing of its three pure coefficients.

## 2. The exact finite mean and the original omitted-site equation

Define the even finite mean tensor on the actual core Q by

    E(U)=sum_(r=0)^m U^(2r)/(2r)! Q^[m-r].              (3)

Thus E(0)=F and its derivative at zero is zero. For any actual row V
on S, the notation partial_V E(U) means the ordinary directional
derivative of the polynomial (3), with Q fixed.

Write the literal original decompositions

    R=Q+sum_h h_q V_h,
    L=U(L)+sum_h d_h(L) h_q,                            (4)

where the three V_h are the actual q-star rows and d_h are linear
functions on D. Also form the finite odd mean

    G_R(L)=sum_(r=0)^m L^(2r+1)/(2r+1)! R^[m-r].       (5)

The COMPLETE q=h coefficient of (5) is

    [h_q]G_R(L)=d_h(L) E(U(L))+partial_(V_h)E(U(L)).    (6)

Indeed q is occupied either by one row factor or by one q-star edge.
The first choice has coefficient d_h U^(2r)/(2r)!; the second has
U^(2r+1)V_h/(2r+1)!, with the residual divided power of Q. These are
exactly (3) and its derivative. No other q occupancy survives and no
coefficient, mixed term, or direct-root component is omitted.

Fix distinct colors h,k and let pi_hk project every site of S onto
its h,k axes. By the reviewed whole binary higher-response vanishing,
all positive higher terms in (5) disappear in this palette, including
when q has color h. Equations (1) and (6) therefore give

    pi_hk( d_h E(U)+partial_(V_h)E(U) )=f_h(L) h^S.     (7)

This is an identity for all L in D. The d_h E(U) term is retained.
For the scaled row sqrt(2)L it gives the same identity with U replaced
by sqrt(2)U and both d_h,f_h multiplied by sqrt(2).

## 3. Ordinary two-replica covariance and the exact cancellation

On S let B_hk be the product of the local alternating forms normalized
by epsilon(h,k)=1, extended by zero on the third coordinate. Because
|S| is even, B_hk is a symmetric bilinear form on the whole tensor
space. It only sees the pi_hk projections, and

    B_hk(Z,h^S)=[k^S]Z.                                (8)

For this fixed actual Q, the polynomial B_hk(E(U),E(M)) is invariant
under simultaneous SO2 rotations of its two mean rows. This is the
full covariance used in the
[retained-vacuum proof](/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-RETAINED-VACUUM-PAIRING-AND-CUBIC-PALETTE-COFACTORS.md).
For completeness it follows by using two ORDINARY replica variable
sets: the sum of their quadratics is orthogonally invariant, and the
product of local alternating differential operators is invariant
under determinant-one rotations. Extracting one coordinate per site
in each replica gives B_hk(E(U),E(M)). No rotation of a site-square-zero
quotient, covariance inverse or measure is assumed.

Write B=B_hk. Applying the 45-degree rotation to equal means gives

    B(E(U),E(U))=B(E(sqrt(2)U),F).                      (9)

Apply that same identity with means U,U+tV, and differentiate at t=0.
The rotated means are sqrt(2)U+tV/sqrt(2), tV/sqrt(2). Since the
derivative of E at zero vanishes, this gives exactly

    B(E(U),partial_V E(U))
      =(1/sqrt(2)) B(F,partial_V E(sqrt(2)U)).          (10)

Both identities hold for arbitrary mean rows, even if V is outside
the restricted image U(D). Use V=V_h and substitute (7) on the left
of (10), and its sqrt(2)L version on the right. Their difference is

    f_h(L) B(E(U)-F,h^S)
      =d_h(L) [B(E(U),E(U))-B(F,E(sqrt(2)U))]=0.       (11)

The bracket vanishes by (9) and symmetry of B. Thus the original
receiving component d_h cancels exactly; it has not been set to zero.
Since f_h is a nonzero polynomial on the vector space D, polynomial
cancellation in C[D] yields

    [k^S](E(U(L))-F)=0              for every L in D.   (12)

For any desired k, choose another color h. All three target functions
are active, so this proves (12) for every k. Separating its homogeneous
mean degrees proves (2) with all rows equal. Substituting a linear
combination of arbitrary rows of D and taking its fully multilinear
coefficient proves (2) as stated. All factorials are nonzero over C.
The endpoint m=1 uses E(U)=Q+U^2/2 and the same calculation directly.

## 4. Pure cofactor invariance under an actual quadratic family

Let U_q be the linear image U(D) of the restriction map. For ANY
ordinary quadratic K in the span of the physical products XY with
X,Y in U_q, equation (2) gives

    [k^S](Q+K)^[m]=[k^S]Q^[m]      for k=a,b,c.        (13)

Indeed expand (Q+K)^[m]=sum_r K^[r]Q^[m-r]. Each r>=1 term is a
linear combination of products of 2r rows in U_q, so its pure
coefficients vanish by (2). Same-site row products are already zero;
K is an actual distinct-site quadratic, not an independently fitted
tensor. Neither its mixed top nor any whole original pair grid is
asserted to be unchanged. Equation (13) is not a source operation.

## 5. Full-source pair specialization and the top-degree support limit

For any full ternary source A on n=2m+2>=4 sites, delete p and take
D to be the span of its three original root rows. Its target image
has rank three, so the theorem applies after deleting any further q.
Let Q=A restricted off p,q, and let U_i,V_i be the two original
exterior row families on that same Q. Then, for either family,

    [k^S] U_(i_1)...U_(i_(2r)) Q^[m-r]=0,
    [k^S] V_(i_1)...V_(i_(2r)) Q^[m-r]=0.              (14)

In particular every same-endpoint pair response beta(U_i,U_j) and
beta(V_i,V_j) has zero pure coefficients. This includes physical
nonedges, rank-one direct blocks and arbitrary direct blocks alike.
The retained cofactor is nonzero by the reviewed whole-pair theorem,
but its nonvanishing was not needed in the calculation.

There is also a support consequence on the GENERAL space D in (1).
For a receiving site v and color k put ell_(v,k)(L)=[k_v]L. Taking
r=m after any omission q in (2) gives the polynomial identity

    product_(v!=q) ell_(v,k)=0.                        (15)

The coordinate ring C[D] is an integral domain. If at most one of
these coordinate functions were identically zero on D, omitting that
site (or any site if none were zero) would make every factor nonzero,
contradicting (15). Thus for each k there are AT LEAST TWO distinct
receiving sites at which every row in D has zero k component.

For a full original root frame this says that each receiving color
is absent from at least two original incident block columns. That
particular column count is already implied by the known three
receiving-axis slice witnesses, using the other two witness colors.
No improved physical-degree or exception count is claimed here.

## 6. Relation to earlier identities and the remaining operation question

The older higher-response theorem concerns ODD products on the odd
core R. Here the conclusion concerns all positive EVEN products on
every actual one-site restriction Q, without assuming U(D) is itself
a diagonal or kernel row space there. Equation (6) and the differentiated
45-degree covariance are the additional bridge.

The [transverse-cofactor ratio theorem](/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-TRANSVERSE-PURE-COFACTOR-KERNEL-PAIR-RATIO.md)
requires two pure omission cofactors and whole kernel rows on another
odd core. It equates two normalized scalar responses, which can both
be nonzero. Neither those hypotheses nor that nonvanishing example
are assertions about the restricted space U_q used here.

No full even response is asserted to vanish, and no input-target
factorization of higher mixed responses is supplied. The actual
mixed terms in (13), the complete pair grid after changing Q, and
the existence of a useful reduction remain uncontrolled. This is
an all-order necessary identity and pure-coefficient invariance,
not a general conjecture closure or a forbidden-order certificate.

**Integration provenance.** Independently audited frozen source:
/tmp/krenn_all_even_omission_pure_response_vanishing_20260913.md
SHA256 3cb6853afd6b3926e39b1bd3bb04cda6e3a9af44d86ed20e7131a96bff85eeee.
Only review status, dependency links and this provenance paragraph changed.
The companion audit is byte-identical to its frozen input.
This research result remains outside the formally certified dependency spine.
