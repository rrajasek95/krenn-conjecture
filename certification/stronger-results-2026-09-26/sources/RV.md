# Retained-vacuum pairing and the three binary projections of a cubic core

**Status.** Exact all-order identities and a source-level cofactor
consequence, 2026-09-13; complete [independent audit PASS](UNIFORM-RETAINED-VACUUM-PAIRING-AND-CUBIC-PALETTE-COFACTORS-AUDIT.md).
The retained-vacuum calculation was reconstructed by the author and
`/root`; the arbitrary-final-tensor extension was proposed by `/root`
and checked below. No successful pair correction is forced here.

## 1. A four-row identity with the vacuum retained

Let S have 2m>=2 sites, with arbitrary finite complex local spaces
containing designated independent a,b,c vectors. All products are in
the commutative physical-site algebra. Let Q be any actual ordinary
quadratic on S and put

    F=Q^[m],                 beta(A,B)=A B Q^[m-1],
    H4(A,B,C,D)=A B C D Q^[m-2]  if m>=2,
    H4=0                                      if m=1.

There is no vanishing or nonvanishing assumption on F. Let Omega3
be the product of the local determinant forms on a,b,c, extended by
zero on extra basis directions. It is symmetric because |S| is even.

For ANY whole tensor T and ANY four rows A,B,C,D on S,

    Omega3(F,H4(A,B,C,D),T)
       =Omega3(beta(A,B),beta(C,D),T)
        +Omega3(beta(A,C),beta(B,D),T)
        +Omega3(beta(A,D),beta(B,C),T).                 (1)

To prove this, first take T decomposable. Contracting one argument
of each local determinant with its T factor leaves an alternating
bilinear form. Hence B(X,Z)=Omega3(X,Z,T) is a product of local
alternating pairings, and it is symmetric on the whole tensor space.

Use two ORDINARY replica variable sets. Their quadratic sum Q(x)+Q(y)
is invariant under simultaneous SO2 rotations, as is the product of
the local alternating differential operators defining B. Thus

    B(Psi(L),Psi(M))

is invariant when the two means are rotated, where the exact physical
coefficient tensor has expansion

    Psi(L)=F+beta(L,L)/2+H4(L,L,L,L)/24+terms of degree>=6.

The operator extracts one coordinate at every site in each replica;
the rotation is performed before extraction, not in the physical
quotient. This justifies the identity for arbitrary complex Q and
extra local dimensions, with no Gaussian measure or inverse.

Compare total mean degree four at (L,0) and at (cL,-sL), where
c^2+s^2=1 and cs!=0. The identity c^4+s^4=1-2c^2s^2 gives

    B(F,H4(L,L,L,L))=3 B(beta(L,L),beta(L,L)).           (2)

The coefficient of t1 t2 t3 t4 after setting L=sum_i t_i A_i
is 24 times the left side of (1) and 3*8 times its three right-side
pairings. This proves (1). Every whole T is a linear combination
of decomposable tensors, so linearity proves its full stated scope.
When m=1, the degree-four term of Psi is absent and the same argument
proves (1) with H4=0.

Two polarizations of (1) yield the useful common-row form

    6 Omega3(beta(Y,M1),beta(Y,M2),beta(Y,M3))
      =3 Omega3(F,H4(Y,Y,M1,M2),beta(Y,M3))
       -Omega3(F,H4(Y,Y,Y,M3),beta(M1,M2)).              (3)

Indeed (1) with Y,Y,M1,M2 gives the first right-side term before
eliminating Omega3(beta(Y,Y),beta(M1,M2),beta(Y,M3)). Equation (1)
with Y,Y,Y,M3 says that this latter pairing is one third of the last
term in (3). All factors and signs follow without dividing by F.

## 2. What the full nonedge grid forces

For an actual full ternary source on 2m+2 sites, delete p,q and use
its original pair grid on the same retained Q:

    D_hk F+beta(U_h,V_k)=delta_hk tau_h P_h,
    P_h=h^S,                         tau_a tau_b tau_c!=0. (4)

If p,q are a physical nonedge, D=0. Set Y=U_a+U_b+U_c and
(M1,M2,M3)=(V_a,V_b,V_c). Then (3) reads

    6 tau_a tau_b tau_c
      =3 tau_c Omega3(F,H4(Y,Y,V_a,V_b),P_c)
       -Omega3(F,H4(Y,Y,Y,V_c),beta(V_a,V_b)).           (5)

Thus the vacuum-containing terms cannot both be set to zero at a
full nonedge packet. Their displayed combination must be nonzero.
The nine equations (4) give mixed U/V responses; they do not directly
specify the V/V response or the quartic responses in (5). This is
an exact additional identity, not a proof that no further consequence
of the full source equations can determine those terms.

In particular (5) is not a clean-cap theorem. When m=1 its right
side is zero, giving the familiar impossibility of a nonedge in a
four-site full ternary source. For larger m the quartic terms remain.

## 3. Every binary projection of the closed cubic core is nonzero

Let a full ordinary source on 2h+4 sites have a vertex p with exactly
the three incident blocks

    p--x: w_a a_p a_x,   p--y: w_b b_p b_y,
    p--z: w_c c_p c_z,                  w_a w_b w_c!=0. (6)

No minimum-order, anchor-maximality, or entry-minimality premise is
used. Let R be the actual core after deleting p,x,y,z, and let
G=R^[h]. For a palette ij let pi_ij act locally on every core site,
retaining its i,j axes and killing all other basis coordinates.
Then

    pi_ab(G)!=0,       pi_ac(G)!=0,       pi_bc(G)!=0.   (7)

Proof: delete p,z first, retaining S={x,y} union sites(R). Call
its actual quadratic Q, so m=h+1. In its full pair grid the direct
block has only D_cc=w_c, and

    U_a=w_a a_x,     U_b=w_b b_y,     U_c=0,
    F=Q^[h+1]=(tau_c/w_c) P_c,
    beta(U_a,V_a)=tau_a P_a,
    beta(U_b,V_b)=tau_b P_b,
    beta(U_a,V_b)=beta(U_b,V_a)=0.                      (8)

Apply (1) to U_a,V_a,U_b,V_b with T=P_c. Its left side is zero,
because F is proportional to P_c and each local determinant then
has two c arguments. The full right side gives

    Omega3(beta(U_a,U_b),beta(V_a,V_b),P_c)
       =-tau_a tau_b!=0.                              (9)

The first response in (9) is exactly

    beta(U_a,U_b)=w_a w_b a_x b_y G.                    (10)

The two fixed endpoint factors remove every Q edge incident to x
or y; hence G here is the original closed-neighborhood core top,
not an independent cofactor. Pairing against P_c only sees the
a/b projections of the other two arguments. If pi_ab(G)=0, (10)
makes (9) zero, a contradiction. Deleting p,x or p,y instead gives
the b/c and a/c statements for this SAME G. This proves (7).

When h=0, the core is empty and G=1; the three projections are the
unit, so the endpoint remains valid. The supplied form (6) is the
established cubic rigidity form recalled in
[CUBIC-PORT-COMPRESSION, Section 1](/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-higher-common-power-bridge-2026-09-05/CUBIC-PORT-COMPRESSION.md).

Statement (7) strengthens whole cofactor nonvanishing. It does not
assert that G is diagonal, that any particular pure coefficient is
nonzero, or that any same-port defect satisfies the exact reduction
criterion of that note. The ordinary higher cap errors have been
retained throughout, and general source coverage remains open.

**Integration provenance.** Independently audited frozen source:
/tmp/krenn_retained_vacuum_pairing_identity_and_cubic_palette_cofactors_20260913.md
SHA256 8a6b3d9bad709dfdd6b6817b7f424278dac9be0feed81d573802fbd6302c39ad.
Only review status and this provenance paragraph changed.
The companion audit is byte-identical to its frozen input.
This research result remains outside the formally certified dependency spine.
