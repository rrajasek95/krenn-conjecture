# A two-active bipartite row forces every rectangular cofactor nonzero

**Status.** New all-order deduction, 2026-09-13, by
`/root/dense_nontree`, using the independently audited retained-vacuum
identity. The parent independently reconstructed the main contradiction.
A [complete independent mathematical audit](UNIFORM-BIPARTITE-TWO-ACTIVE-RECTANGULAR-COFACTOR-NONVANISHING-AUDIT.md) passes. It proves
no general outside-palette kernel confinement or forbidden source order.
Version 2 clarifies the larger-shore domain of the kernel corollary and
records the contrasting smaller-shore occupancy kernels. The original
164-line version remains unchanged; the cofactor proof is unchanged.

## 1. Actual source and statement

Work over C in the commutative physical-site-square-zero algebra,
with Q^[j]=Q^j/j!. Each finite local space V_v contains designated
independent vectors a_v,b_v. Extra coordinates and arbitrary complex
whole edge blocks are allowed. Let P be an ordinary bipartite quadratic
on W disjoint-union T, with |W|=w, |T|=w+1, and w>=1.
Suppose ONE actual T-supported row Y has the WHOLE response

    Y P^[w]=tau_a a^(W union T)+tau_b b^(W union T),
    tau_a tau_b!=0.                                      (1)

For each t in T define its actual balanced deletion cofactor

    Q_t=P restricted off t,        F_t=Q_t^[w].           (2)

**Theorem.** Every F_t is nonzero. More precisely, choose at each
retained site a linear projection pi_ab onto its designated a,b plane
which fixes those two axes. Then

    pi_ab(F_t)!=0                 for EVERY t in T.       (3)

The statement holds for every choice of these projections. It requires
neither separate pure-a/pure-b row preimages, full receiving support,
graph restrictions, nor an ambient three-target source. It concerns
larger-shore deletions; smaller-shore deletion tops vanish by occupancy.

## 2. Retained-vacuum input and the complete slices

The sole invariant input is the audited
[retained-vacuum four-row identity](/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-RETAINED-VACUUM-PAIRING-AND-CUBIC-PALETTE-COFACTORS.md#1-a-four-row-identity-with-the-vacuum-retained).
For an actual quadratic Q on an even set S of size 2w, put

    F=Q^[w],                 beta(A,B)=A B Q^[w-1],
    H4(A,B,C,D)=A B C D Q^[w-2] if w>=2, and H4=0 if w=1.

After adjoining an unused third coordinate c_v at each site if needed,
let Omega3 be the product of the local alternating determinant forms
on a,b,c, zero on extra basis directions. For every whole tensor Z,

    Omega3(F,H4(A,B,C,D),Z)
      =Omega3(beta(A,B),beta(C,D),Z)
       +Omega3(beta(A,C),beta(B,D),Z)
       +Omega3(beta(A,D),beta(B,C),Z).                   (4)

Adjoining unused coordinates changes no coefficient or equality of
the original source. At an even number of sites Omega3 is symmetric,
and Omega3(a^S,b^S,c^S)=1.

The following abstract specialization makes the needed hypothesis
explicit. If F=0 and beta(X,X)=0 for one fixed row X, then (4) gives

    Omega3(beta(X,A),beta(X,B),Z)=0
                for ALL rows A,B and ALL whole tensors Z. (4a)

Indeed, apply (4) to X,X,A,B; the two remaining terms are equal.
In particular the intersection of im(beta(X,-)) with
span{a^S,b^S,c^S} is contained in ONE fixed coordinate axis, or is
zero. To see this, put A=B and successively choose Z=a^S,b^S,c^S.
For a diagonal response with coefficients d_a,d_b,d_c, the resulting
equations are 2 d_b d_c=2 d_a d_c=2 d_a d_b=0. Every such response
therefore has at most one active coordinate. Since the intersection
is linear, two different active axes would give a forbidden sum.
The same statement for two designated targets follows after adjoining
an unused third coordinate. No bipartiteness is assumed in (4a).

Fix t in T and write the ORIGINAL source and row literally as

    P=Q+sum_j e_j(t) U_j,       Y=Y_0+sum_j y_j e_j(t),
    Q=Q_t,                     S=(W union T) without t.

Here every U_j is supported on W and Y_0 on T without t. In particular
Q is balanced bipartite on w sites per shore. Taking the coefficient
of h_t in the whole identity (1) gives exactly

    y_h F+beta(Y_0,U_h)=tau_h h^S,       h=a,b.           (5)

The first term uses the row at t; the second uses precisely one
edge from the original t star. Repeated use of t vanishes. Thus no
crossing term or factorial is omitted in (5).

Since Y_0 has support only on the T shore,

    beta(Y_0,Y_0)=Y_0^2 Q^[w-1]=0.                      (6)

Indeed, after two T monomers the w-1 crossing edges cannot cover all
w W sites. At w=1 the same equality holds because Y_0 is on one site.

## 3. The contradiction and the active-plane strengthening

Suppose F=0. Equation (5) then gives the TWO whole tensors

    beta(Y_0,U_a)=tau_a a^S,
    beta(Y_0,U_b)=tau_b b^S.                             (7)

Apply (4) to (A,B,C,D)=(Y_0,Y_0,U_a,U_b), with Z=c^S.
Its left side vanishes because F=0. The first right-side term
vanishes by (6); the other two equal tau_a tau_b. Consequently

    0=2 tau_a tau_b,                                    (8)

contrary to (1). This proves F_t!=0, including w=1 without a negative
divided power. No assumption about beta(U_a,U_b) was necessary.

For (3), first apply the chosen local projections to P,Y and (1).
They are homomorphisms of the physical-site algebra, preserve both
whole nonzero target tensors, and retain bipartiteness. Their deletion
cofactor at t is precisely pi_ab(F_t). The same proof therefore makes
it nonzero. A particular pure coefficient of F_t need not be nonzero;
the conclusion is nonvanishing of its ENTIRE active-plane projection.

## 4. Balanced sources and the exact kernel limitation

Let B be an actual balanced bipartite source with r>=2 sites per shore
and whole top sigma_a a^(2r)+sigma_b b^(2r), both amplitudes nonzero.
Deleting any smaller-shore vertex p gives an odd core P and its actual
root rows U_a,U_b. Their sum Y=U_a+U_b satisfies (1), with w=r-1.
Thus, for EVERY opposite-shore vertex t,

    pi_ab((B restricted off {p,t})^[r-1])!=0.            (9)

At r=1 the cofactor is the empty unit, so (9) holds directly. This
strengthens physical matching extendability to whole cofactor
nonvanishing, even when p--t is absent. Same-shore deletions are not
covered. No restriction on an individual c_p c_t block follows here.

Define the odd map ONLY on larger-shore rows:

    Phi_P: direct_sum_(t in T) V_t -> tensor_(v in W union T) V_v,
    Phi_P(L)=L P^[w].

For t in T a singleton row z_t has response z_t F_t. Since these
factors occupy disjoint sites and F_t!=0, this map is injective on
each individual V_t with t in T. Hence there is no nonzero
T-supported singleton kernel, of any local color. In contrast,
EVERY row supported on W has zero response by bipartite occupancy;
in particular smaller-shore singleton kernels do exist if that
larger domain is used. No injectivity on that domain is asserted.

A general multi-site kernel K supported on T still has, for t in T,
the exact t-coordinate slice

    k_(t,j) F_t+K_(T without t) U_j Q_t^[w-1]=0.         (10)

An outside-palette coefficient k_(t,c)!=0 alone does NOT set F_t=0:
the second term is an actual allowed crossing contribution. The new
theorem says that contribution must then be nonzero. If a separate
actual argument made it zero, the coefficient would be excluded; for
example U_c=0 suffices. Receiving-axis witnesses at OTHER sites and
the two pure equations do not isolate that term in this argument;
no such general implication is claimed. Dense outside-palette kernels and
the original-source coupled inactive-minor problem remain open.

## 5. Dependency and scope record

The cited retained-vacuum source has 161 lines and SHA256
b2cd2d28691d5d502bc24cc7be1bbe321053b2bedfcb1ada86e7a096c9d29997.
Its independently audited companion has 169 lines and SHA256
3d731cf9d0387e5f6ac8ddd735b0321a0ca62c828c22e1bbb5cff21528b6501f.
The existing all-omission theorem uses a THREE-active row on an
arbitrary odd core. The present two-active assertion instead uses
bipartiteness and the one-shore square vanishing (6). Existing finite
seven-site and K4-minor-free injectivity theorems are not inputs here.
At source freezing, only the new /tmp source was written; all 375
then-current canonical records and prior proof/audit files were unchanged.

**Integration provenance.** Independently audited frozen source:
/tmp/krenn_bipartite_two_active_response_all_rectangular_cofactors_nonzero_20260913_v2.md
SHA256 fe41b263b3020c61d41903fc12f34a7376c1c955c7a63685686eaa5567893a2a.
Only review status, dependency links and provenance changed.
The companion audit is byte-identical to its frozen accepted input.
This research result remains outside the formally certified dependency spine.
