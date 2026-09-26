# Independent audit of the complete two-replica closure

Fresh UNFROZEN complete analytic audit by /root/routing_author, 2026-09-26.
Verdict: **PASS for the pointwise complex theorem**. The sole wording
clarification requested during review is applied in the final bound text. This is an
independent mathematical reconstruction, not an extrapolation from the finite
replica calculation, a Lean formalization, or external peer review.

## 1. Exact reviewed sources

I read every line of both fresh proof sources:

- [Complete proof](../../proofs/krenn-gu-all-orders-two-replica-proof.md),
  final 336 lines / 15658 bytes, SHA256
  fb0fa1e9447d8044981692d6e9bbbeff8e6a2cfc90119b6a296cbf506b9a3c9d.
- [Endpoint source](FINITE-TWO-REPLICA-COVARIANCE-FORCES-HAFNIAN-ENDPOINT-IDENTITIES-PROVISIONAL-CLOSING-PROOF.md),
  243 lines / 10550 bytes, SHA256
  e5e9e1ba7a396e307ce176bfdd75c1c905e1fd33e5f6b75acd5bac18a542a230.

I also read and reconstructed in full the following five earlier sources in
the higher-common-power directory; the exact hashes are part of this audit:

- [Common odd factors](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-ALL-ODD-DIAGONAL-RESPONSE-FACTORS-AND-NULL-PAIR-TRANSFER.md),
  230 lines, 3f75dcf21adffb42369985efe37ef947152b4db8f2ad8192bff36031fa3f612c.
- [Sitewise mixed reflection](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-ALL-ODD-TWO-COLOR-MIXED-VANISHING-AND-KERNEL-PENCIL.md),
  186 lines, 03edf88285ca2a0d1dda8354d266b5d3e329be05149129e8843b2bb2dd9a12e1.
- [Higher pure responses](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md),
  240 lines, 14811c0332c217e1a5520bd619482f641573b9456783404f48a93dbc3542b190.
- [All-even omission](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING.md),
  211 lines, 450f75c2c6280c601e2d012c1ae892d1f18f14f62aae8ec5dd448c3a157b7688.
- [Global diagonal reduction](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-GLOBAL-EDGE-MONOCHROMATICITY-AND-COFACTOR-INVERSE.md),
  229 lines, 4e140eb5cd74a4e0d9869f76e975ce2f7d46c8d7d1ba9be332a8128424082e89.

The full proof includes these foundations explicitly. Their prior audit
labels are not being substituted for the present reconstruction.

## 2. Original model and the complete higher-response foundation

The theorem concerns an ordinary quadratic on distinct physical pairs in the
commutative physical-site-square-zero algebra. Divided powers count each
perfect matching once. Arbitrary complex aggregate endpoint-color blocks,
parallel-edge aggregation, unequal nonzero pure amplitudes and arbitrary
density are permitted. Projection onto three active target axes is an algebra
homomorphism, so the ternary exclusion covers target dimension at least three.

At any original root the three incident rows have responses
tau_i i^(V without root), giving three independent active linear response
functionals before any diagonal or binary projection. All response identities
in Sections 2--3 of the full proof therefore have their stated rank premises.

The formal reflection preserves the covariance of two identical Wick replicas,
fixes one auxiliary combination, and changes the product of an odd number of
local alternating factors by a minus sign. Its moment is zero. Coefficient
extraction gives the displayed antisymmetric higher-response relation with
the correct raw factorials; no positive Gaussian measure is assumed.

For constant receiving axes this gives f_j t_i=f_i t_j. Coprime independent
linear f_i,f_j in the polynomial ring on the root-row space yield a common
factor q_r. For a mixed word avoiding active h, the site-dependent reflection
leaves only the all-h complementary response. Polynomial cancellation of
nonzero f_h gives the entire binary mixed vanishing, even where f_h evaluates
to zero at a particular row.

The finite odd mean restricted to two colors is g(L)Phi(L). Its SO2 covariance
permits cancellation of the NONZERO POLYNOMIAL determinant of two independent
functionals. The resulting identity g(L/sqrt(2))^2=g(L), with g even and
g(0)=1, forces g=1 by highest degree over C. Thus pure higher responses vanish
as well. Polarization gives the whole binary conclusion for arbitrary
products of the same original root-family rows, through degree n-1.

This does not set three-color receiving errors to zero. The new proof only
uses binary projections, so no surviving three-color error is discarded.

## 3. Omission and diagonal reduction reconstructed

The complete coefficient at the omitted vertex is d_h E(U)+E_(V_h)(U).
The direct omitted-site contribution is retained. Differentiated equal-mean
covariance, together with its undifferentiated version, cancels the d_h terms.
The surviving equation is f_h(L) times the pure-k coefficient of E(U)-F=0.
Polynomial cancellation and
polarization give the stated raw two-row pure omission identity.

The off-diagonal entry (B_ih C_h)[p,q] is exactly that identity, after expanding
the ACTUAL cofactor at retained p. Both sides are sums over ordered pairs;
the coincident-row factor two is present on both sides. The diagonal entry
is the original complete one-defect word. Hence

    B_ih C_h=delta_(i,h) tau_h I.

For i=h this makes C_h invertible over C; for i!=h it gives B_ih=0.
Thus the original edge cells are diagonal without assuming diagonality or a
basis change. The n=4 boundary is valid. This chain has no minimum-source,
cofactor-nonvanishing, positivity, finite-order, or source-inheritance premise.

## 4. The new endpoint boundaries are licensed at every degree

Fix B,H and physical p,q, put N=n-2, d=B_pq, e=H_pq, beta=haf B,
eta=haf H, and retain the source notation x,y,u,v for the actual rows.
The binary core Q is literal. Its finite mean is

    E(L)=sum_j L^(2j)Q^[N/2-j]/(2j)!.

Expanding the original root-p odd mean at q gives

    E_y(sx+tu)+dsE(sx+tu)=s beta b^U,
    E_v(sx+tu)+etE(sx+tu)=t eta h^U,

and the analogous q-root identities. Both q occupancies are included:
a direct departure and a core edge. These are polynomial identities in row
parameters on a fixed source, so differentiating them in t is licensed.

The terminal degree N+1 is essential. For example E_yu(sx) has degree at most
N-2, while -dsE_u(sx) could have degree N. The maximal original odd response
kills that highest coefficient. Likewise it kills the would-be highest term
in E_uv(sx)+eE(sx). The complete tower proved in Section 2 supplies precisely
this degree. It is not a convention or an omitted residual.

In particular the proof legitimately uses

    E_u(ay)=0, E_v(sx)=0,
    E_yu(sx)=-dsE_u(sx),
    E_y(sx)+dsE(sx)=s beta b^U,
    E_uv(0)+eF=eta h^U.

No cross-root row is assumed to lie in the other root's diagonal-response
space; it occurs only through the literal omitted-site expansion.

## 5. Covariant matrix and invariant-ring audit

The retained site count N is EVEN. The product alternating pairing K is
therefore symmetric, and the finite Wick kernel is invariant under all O2:
rotations preserve the local determinants, and reflection contributes
(-1)^N=1. This mixes proof replicas, not physical source axes.

For the four independent two-component parameter columns, differentiating
the scalar kernel gives a covariant matrix M. The original plane zeros make
M_12 divisible by P_1 Qc_2 and M_21 divisible by P_2 Qc_1 literally.
After an orthogonal rotation on the dense nonisotropic locus this implies
MP parallel to P and M^T Qc parallel to Qc.

The two eigenvalues agree when P dot Qc is nonzero. In dimension two the
remaining rank-one operator annihilates P and has left kernel Qc, so it is a
multiple of (P dot Qc)I-P Qc^T. Hence M=a_0 I+b P Qc^T generically.
The quotient b=M_12/(P_1 Qc_2) is already polynomial by divisibility, and
a_0=M_11-bP_1Qc_1 is polynomial too. All entries then agree identically.
There is no unresolved denominator or exclusion of auxiliary isotropic values.

The endpoint source provides a second, direct check: writing the two
off-diagonal quotients b,b' and the parallel-vector equations yields
(P dot Qc)(b-b')=0. Polynomial cancellation gives b=b' and the same matrix
form. Adding e f I preserves the form, with scalar coefficient a.

Uniqueness and covariance make a,b O2 invariants. In complex coordinates
p_+,p_-,q_+,q_-, rotation weight zero generates sigma,tau,r,s with
rs=sigma tau. Averaging under reflection exchanges r,s, and symmetric
polynomials reduce to r+s=2c and rs. Thus the invariant ring is exactly
C[sigma,tau,c]. The axis substitution

    sigma=P_1^2+P_2^2, tau=Qc_2^2, c=P_2Qc_2

is injective: every tau!=0 with arbitrary sigma,c is attained over C.
Equivalently its Jacobian is -4 P_1 Qc_2^2. This verifies both invariant
dependence and the later transfer of axis equations to polynomial identities.

## 6. Both finite polynomial ODEs and the supported-edge scope

Differentiating the full off-diagonal kernel in Qc_1, then setting Qc_1=0,
uses E_yu(sx)=-dsE_u(sx). In the invariant matrix form it is exactly

    P_1^2 Qc_2 (b_c+d b)=0.

Canceling auxiliary monomials and using the injective Gram substitution gives
b_c+d b=0. For a supported physical B edge d is a nonzero complex constant.
A finite polynomial in c satisfying this equation is zero, by its highest
coefficient. Thus T=M+e f I=a I.

For the diagonal entry use the UNRESTRICTED expression
T_22=K(E(P_1x+Qc_1y),E_uv(P_2x+Qc_2y)+eE(P_2x+Qc_2y)).
Differentiate in Qc_1 before restriction. The root identity for E_y gives

    partial_(Qc_1)T_22=P_1 beta eta-dP_1 T_22 at Qc_1=0.

The eta factor is exact: any positive B-only mean insertion has a retained
B coordinate, so it cannot contribute to the all-H word. At zero the second
tensor is E_uv(0)+eF=eta h^U. No direct H-edge term is lost.

The invariant expression gives a_c+d a=beta eta. Finite polynomiality and
d!=0 force a=beta eta/d. At the origin a(0)=eta haf(B[U]); cancel only the
nonzero GLOBAL eta to obtain beta=d haf(B[U]).

The final full proof explicitly differentiates the unrestricted T_22 expression
before setting Qc_1=0. I requested and checked this wording clarification;
the calculation above and the held endpoint source use precisely that order.
No mathematical correction or added hypothesis was needed.
The final rendering and grammar edits were also checked by reversing exactly
those two substitutions and recovering the previously reviewed source hash.

No division by a retained hafnian, inverse-matrix assignment, differentiation
of ideal membership, or source-preserving flow is used. The endpoint argument
needs neither scalar cofactor identities nor an infinite hierarchy extrapolation.

## 7. Matching and the final graph obstruction

At each vertex the ordinary hafnian expansion sums to beta. The endpoint
identity makes EVERY supported summand equal beta. Since beta!=0 over C,
each vertex has degree one in B. Repeating for the other colors makes all
three color graphs weighted perfect matchings.

A word supports at most one colored matching, so any supported mixed matching
has a nonzero coefficient. Shared edges already yield mixed words; otherwise
the matchings are pairwise disjoint. The union of two must be one alternating
Hamilton cycle, since separate components can be colored differently.

The third-color chords cannot join opposite parities on that cycle: deleting
such endpoints leaves two even paths that can be matched by the first two
colors. An interlacing pair of opposite-parity same-shore chords likewise
leaves four even paths, giving a mixed matching when n>4.

The full proof's final innermost-arc argument is sound. Choose any chord and
side minimizing the number of interior vertices. Its equal-parity endpoints
ensure an interior vertex of the opposite parity. That vertex's same-parity
partner must be interior too, since an exterior partner would interlace the
chosen chord. This gives a strictly interior chord with a smaller side,
contradicting minimality. If there is only one interior vertex of that parity,
the requirement of an interior partner itself is already impossible.

As an independent alternative check, absence of interlacing forces every
shore-matching chord to preserve parity of its cyclic shore index. Restricting
both shores to odd indices halves their sizes and preserves the hypotheses.
Repeated halving reaches an odd shore size, impossible for a perfect matching.

The four-site exception is exact: two interlacing third-color chords then
exhaust all vertices and give only the pure third matching. For n>4 at least
one first/second-color edge remains, so the output is genuinely mixed.
No external graph theorem or computational census is needed for this step.

## 8. Completion scope

Sections 1--7 of the complete proof have been independently reconstructed.
They cover the original general complex weighted matching model, not merely
an assumed diagonal subclass. The common-factor/reflection hypotheses,
terminal coefficients, complex orthogonal frames, polynomial cancellations,
retained-core scope and four-site boundary were checked explicitly.

The conclusion is pointwise nonexistence for every even n>4 with three active
GHZ target colors. This audit does not claim an explicit ordinary-ideal power
certificate, a nonreduced-scheme argument, or formal Lean certification.
The finite r=2 replica calculation and the earlier endpoint extraction formula
are not premises of this proof.

Only this fresh audit was written. Previously bound sources, checkers,
canonical files and external README changes remain unchanged.
