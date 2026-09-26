# Independent audit of retained-vacuum pairing and cubic palette cofactors

**Verdict: COMPLETE INDEPENDENT PASS, without source correction.**
Auditor: `/root/one_bad_tree`, 2026-09-13. I read all 154 frozen
source lines and independently reconstructed every identity, endpoint,
and stated limitation. I also checked the complete original cubic-port
reference used to identify its actual closed-neighborhood core.

Frozen source:
`/tmp/krenn_retained_vacuum_pairing_identity_and_cubic_palette_cofactors_20260913.md`
— 154 lines, 6694 bytes, SHA256
`8a6b3d9bad709dfdd6b6817b7f424278dac9be0feed81d573802fbd6302c39ad`.

No numerical test, ordinary-source replacement, or vanishing-vacuum
assumption is used in this audit. The replica proof in the source
is self-contained; its cubic rigidity form is supplied explicitly.

## 1. Arbitrary final tensor and the two-replica operator

For a decomposable whole tensor T=product_v t_v, define the local
bilinear form b_v(r,s)=epsilon_v(r,s,t_v). It is alternating, even
when t_v has extra-coordinate components or makes that form zero.
Then B(X,Z)=Omega3(X,Z,T) is exactly the product of these local
alternating forms. Since there are 2m sites, B is symmetric.

In ordinary replica coordinates, its local differential operator is

    D_v=sum_(i,j) b_v(e_i,e_j) partial_(x_i) partial_(y_j).

Under an SO2 substitution, the same-replica derivative terms vanish
by antisymmetry of b_v and commutativity of the derivatives. The
remaining mixed-replica operator is (c^2+s^2)D_v=D_v. This holds
for every local alternating form, not only the particular a/b
coordinate determinant. The literal sum Q(x)+Q(y) and evaluation
at zero are likewise invariant. Thus the asserted mean-rotation
identity holds for this B, with all original Q coefficients retained.

The differential operator selects one coordinate at every physical
site in each replica. It therefore gives the stated coefficient
pairing with no extraction factorial. The calculation takes place
in ordinary commuting variables before the physical top is selected;
replica mixing is not asserted to preserve the square-zero ideals.
Finite-dimensional whole tensor spaces are spanned by decomposable
tensors. Since every resulting identity is linear in T, the extension
to an arbitrary, possibly entangled, final tensor is justified.

## 2. Degree four, factor three, and full polarization

Occupancy on 2m sites gives the exact low mean-degree expansion

    Psi(L)=F+beta(L,L)/2+H4(L,L,L,L)/24+O(mean degree 6).

The coefficients 1/2! and 1/4! count the indistinguishable linear
insertions, while the Q factors are already divided powers. There
are no odd mean degrees. When m=1 the fourth-degree term is absent.

Write b=B(F,H4(L,L,L,L)) and c0=B(beta(L,L),beta(L,L)).
The total mean-degree-four coefficient at (L,0) is b/24. At the
rotated pair (cL,-sL), it is

    (c^4+s^4)b/24+c^2s^2 c0/4.

Equality, c^4+s^4=1-2c^2s^2, and cs nonzero give b=3c0.
No division by F or any response tensor occurs. For m=1 the same
comparison gives c0=0, which is exactly the identity with H4=0.

Set L=t1 A+t2 B+t3 C+t4 D. The coefficient of t1t2t3t4 in H4
is 24 H4(A,B,C,D). On the quadratic-response side, each partition
into two pairs contributes the two factors of two from the cross
terms in beta(L,L), and a further factor two from the two orders
of the response factors. The coefficient is therefore eight times
the sum of the three pairings. The prefactor three makes 3*8=24,
so division by 24 proves source equation (1) with coefficient one
on each right-side term. Dependent or repeated rows are allowed.

## 3. The common-row identity has the stated factor six

Put

    X=Omega3(beta(Y,M1),beta(Y,M2),beta(Y,M3)),
    Z=Omega3(beta(Y,Y),beta(M1,M2),beta(Y,M3)),
    A0=Omega3(F,H4(Y,Y,M1,M2),beta(Y,M3)),
    B0=Omega3(F,H4(Y,Y,Y,M3),beta(M1,M2)).

The four-row identity first with (Y,Y,M1,M2) gives A0=Z+2X.
With (Y,Y,Y,M3) it gives B0=3Z, using symmetry of Omega3.
Consequently 3A0-B0=6X, precisely equation (3). The negative sign
and both numerical factors are therefore necessary and correct.
These are polynomial identities for the same Q; no higher response
is discarded or assumed to factor through beta.

## 4. The original nonedge grid

For an actual full source with a physical nonedge p,q, its complete
grid has D=0 and beta(U_h,V_k)=delta_hk tau_h P_h. For
Y=U_a+U_b+U_c this gives beta(Y,V_h)=tau_h P_h separately.
The three target tensors have

    Omega3(P_a,P_b,P_c)=1.

Substituting M1=V_a,M2=V_b,M3=V_c into the preceding identity
therefore gives exactly source (5), including the factor tau_c
in the first term and the unrestricted beta(V_a,V_b) in the second.
Its left side is 6 tau_a tau_b tau_c, which is nonzero.

The nine original U/V equations do not directly prescribe the V/V
or quartic responses on the right. The source does not assert they
are free of further source constraints; it correctly states only
the displayed nonzero balance. When m=1, both H4 terms vanish,
excluding a physical nonedge in a four-site full source. For larger
m this identity alone does not eliminate the quartic terms or
construct a clean cap.

## 5. All three palette projections use one actual cubic core

For the supplied physical cubic form (6), deleting p,z retains
the actual even Q on x,y and the same exterior core R. Its direct
block is w_c E_cc, while the exterior rows at p are

    U_a=w_a a_x,  U_b=w_b b_y,  U_c=0.

The original cc equation gives F=(tau_c/w_c)P_c. The aa and bb
equations give the two nonzero pure pair responses, and the ab/ba
equations give their two whole mixed zeros, exactly as in (8).
Neither reverse-port soleness nor a minimum-source condition is used.

Apply equation (1) with rows U_a,V_a,U_b,V_b and T=P_c.
The left side is zero because F is a multiple of P_c, so every
local determinant has two proportional c factors. The first
right-side term is tau_a tau_b; the last term is zero by the two
mixed grid equations. Hence the middle term is -tau_a tau_b,
as in (9), and is nonzero.

The other middle response is literally

    beta(U_a,U_b)=w_a w_b a_x b_y (A|R)^[h].

Both fixed linear factors already occupy x,y, so every quadratic
edge using either endpoint is killed by site occupancy. This proves
that G is the unchanged closed-neighborhood top, with coefficient
one. Pairing against P_c uses only a/b components of the remaining
arguments. Thus pi_ab(G)=0 would contradict (9).

Deleting p,x and p,y gives the corresponding b/c and a/c arguments.
In each case the induced core after removing all four named vertices
is exactly A|R. No independently fitted cofactor, different source,
or assumption that a deletion preserves a graph class is involved.
The target determinant sign is still positive under relabeling:
each local sign is repeated an even number of times. This verifies
all three simultaneous nonvanishing statements in (7).

At h=0, R is empty and G=1. The first retained core has m=1, for
which equation (1) was proved with H4=0. Each binary projection of
the empty unit is again one, so no negative quadratic power or
excluded four-site boundary has been used.

## 6. Scope and preservation

The result proves nonzero binary palette projections, not nonzero
individual pure coefficients or a successful cubic correction.
The source correctly leaves the same-port correction-span criterion
and general source coverage open. The first identity allows arbitrary
finite local dimensions and arbitrary F, including zero.

Only this new audit and its matching receipt were written. The
154-line source and the separately frozen forced-matching source114
and receipt remain unchanged. All 355 authoritative records,
including 171 audits, and all 124 older frozen-input records were
verified by complete text, SHA256, and line count at finalization.
