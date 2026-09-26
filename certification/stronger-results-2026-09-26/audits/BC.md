# Independent audit: every larger-shore bipartite cofactor is nonzero

**Verdict: COMPLETE INDEPENDENT PASS for frozen v2.** The cofactor
theorem and isotropic response lemma pass without mathematical correction.
Version 1 needed the explicit larger-shore domain correction recorded
below. Auditor: `/root/audit_tree_chords`, independently of author
`/root/dense_nontree`, 2026-09-13. I read both full versions, their exact
diff, and the complete retained-vacuum dependency and independent audit.

Accepted source:
[/tmp/krenn_bipartite_two_active_response_all_rectangular_cofactors_nonzero_20260913_v2.md](/tmp/krenn_bipartite_two_active_response_all_rectangular_cofactors_nonzero_20260913_v2.md)
— 176 lines, 8277 bytes, SHA256
`fe41b263b3020c61d41903fc12f34a7376c1c955c7a63685686eaa5567893a2a`.

The preserved v1 has 164 lines, 7703 bytes, SHA256
`6eac0d97f588c0c996d0c9523f4774c88297120384fa77af06e832fc0660eb4b`.

## 1. The correction and the precise theorem being accepted

Version 1 said that Phi_P is injective on each individual site's row
space and that there is no nonzero singleton kernel, without explicitly
limiting those assertions to T. As an unrestricted assertion this is
false: EVERY W-supported row annihilates P^[w] by bipartite occupancy.
The full map on both shores always has those smaller-shore kernels.
Root flagged this scope issue, and I independently confirmed it.

Version 2 defines Phi_P on the direct sum of the V_t for t in T,
restricts the singleton and multi-site kernel discussion to that domain,
and states the contrasting W-supported kernels explicitly. The other
change is a three-line version note. I compared every changed line;
the cofactor theorem, invariant lemma, proof, and balanced-source
corollary are unchanged. The unrestricted v1 singleton wording is
not endorsed by this audit. The two frozen versions remain immutable.

The accepted hypotheses are one actual ordinary bipartite quadratic
P on W,T, with sizes w,w+1 and w>=1, and ONE T-supported row Y whose
whole output is tau_a a^(W union T)+tau_b b^(W union T), both nonzero.
There is no third active target, separate pure-row frame, density,
minimum-source, or full-receiving-support premise. The conclusion
concerns each actual larger-shore deletion, including sites where
Y itself vanishes.

## 2. Retained vacuum and finite local dimensions

I read the entire canonical retained-vacuum proof and its independent
audit, and reconstructed the four-row normalization. For a decomposable
final tensor, contracting local determinant forms gives alternating
bilinear forms. Their two-replica differential operator and the ordinary
quadratic sum are invariant under SO2. The comparison of total mean
degree four gives factor three; full polarization contributes 24 on
the quartic side and 3 times 8 on the paired side. Thus each of the
three pairings in source (4) has coefficient one.

This reasoning is performed in ordinary replica variables before
physical coefficient extraction. It does not rotate the physical
square-zero ideals, require positive covariance, or invert the actual
quadratic. Linearity extends from decomposable final tensors to every
whole Z. The m=1 endpoint has H4=0 and follows from the same comparison.

If an original local space has only a,b, embed it into its direct sum
with an unused c direction. More generally one may make this extension
at every site and extend the basis further. Embed P and its rows with
zero coefficients in the new directions. This is an injective algebra
map and changes none of the original equalities or coefficients.
The determinant forms can be zero on all extra basis directions.
On 2w sites their product is symmetric and
Omega3(a^S,b^S,c^S)=1. The use of the auxiliary c^S does not posit a
third target in the original bipartite source.

## 3. The abstract isotropic-image lemma

Assume an actual even Q has F=Q^[w]=0 and beta(X,X)=0 as a WHOLE
tensor for one fixed row X. Apply the four-row identity to X,X,A,B.
Its vacuum side is zero, and the beta(X,X) term is zero. The other
two terms are equal by symmetry of Omega3, yielding

    2 Omega3(beta(X,A),beta(X,B),Z)=0

for every A,B and every whole Z. Division by two is valid over C.
No premise about beta(A,B), row independence, graph structure, or
the pure coefficients of those other responses is used.

If a tensor D=d_a a^S+d_b b^S+d_c c^S lies in this image, set A=B
to one of its preimages. Choosing Z=a^S,b^S,c^S gives respectively
2d_b d_c=0, 2d_a d_c=0, 2d_a d_b=0. Thus at most one coefficient
is active. The image is a linear space, and its intersection with
the diagonal space is linear. If it contained nonzero tensors on
two distinct coordinate axes it would also contain their forbidden
two-active sum. This proves the fixed-axis, or zero, conclusion.
The argument is valid with arbitrary extra local coordinates.

Both whole vanishing hypotheses are retained. In particular this
is not the generally false assertion that a zero vacuum alone makes
every fixed-row image isotropic, nor an assertion about arbitrary
unrelated pair-response images.
For a direct guard, take Q=0 on two sites, X=a_1+b_2, A=a_2,
B=b_1. Then beta(X,A)=a_1 a_2 and beta(X,B)=b_1 b_2, while
beta(X,X)=2a_1 b_2!=0. The extra isotropy premise excludes exactly
this elementary zero-vacuum example.

## 4. Exact deleted-site slices and the shore-square zero

Fix t in T. The actual Q=P restricted off t is balanced, with w
sites per shore. Its t-star rows U_j are all supported on W. Split
the original row as Y=Y_0+sum_j y_j e_j(t), with Y_0 on T without t.
In the coefficient of h_t in Y P^[w], site t can be occupied by
exactly one of two mechanisms:

    the row at t:       y_h Q^[w];
    a t-star edge:     Y_0 U_h Q^[w-1].

No term uses t twice. A single star edge in a divided power has
coefficient one, so their sum is exactly source (5), with the
original pure target tau_h h^S for h=a,b. This is a whole tensor
equation, including all mixed and extra-coordinate sectors on S.

Also beta(Y_0,Y_0)=Y_0^2 Q^[w-1]=0 as a whole physical tensor.
Each putative monomial uses two T monomers and w-1 crossing edges,
so it attempts w+1 T occupancies among only w retained T sites.
Equivalently it cannot cover all w W sites. Every such monomial
vanishes by physical occupancy, regardless of complex cancellations.
For w=1, Y_0 occupies just one site, so its square is directly zero.

If F were zero, the two actual slices would give
beta(Y_0,U_a)=tau_a a^S and beta(Y_0,U_b)=tau_b b^S. These have
the SAME Y_0 and the SAME Q. The four-row identity applied to
Y_0,Y_0,U_a,U_b with Z=c^S then gives 0=2tau_a tau_b, impossible.
The mixed response beta(U_a,U_b) multiplies the whole zero
beta(Y_0,Y_0); it was not itself discarded or assumed zero.

These hypothetical pure bilinear responses follow only after assuming
F=0. They do not turn the original single row Y into separate pure
row preimages on the odd P. For F nonzero the two terms y_h F in
the original equations persist. At w=1 the proof uses H4=0 and
Q^[0]=1 throughout, with no negative divided power.

## 5. Every active-plane projection and the balanced corollary

Choose arbitrary local projections onto the designated a,b planes
at the retained sites, fixing a,b individually. Extend these maps
by the identity at t, or by any such projection there as well.
They preserve the original two whole target tensors, physical
occupancy and bipartiteness. Applying them to P and Y gives an
instance of the theorem just proved. Restriction and divided powers
commute with these sitewise algebra maps, so its deletion cofactor
is precisely the chosen projection of F_t. It must be nonzero.
This proves the assertion for EVERY choice, not only for a projection
that kills a particular preselected complementary basis.

For a balanced binary source B with r>=2 sites in each shore, delete
any vertex p in one shore. Its actual a,b root rows lie on the other
shore and have their two separate pure responses by coefficient
extraction at p. Their sum supplies the one row needed by the theorem,
with w=r-1. Deleting any opposite-shore t therefore proves (9),
without assuming the physical edge p--t is present. At r=1 the
deleted cofactor is the empty unit; that endpoint is handled directly.
Same-shore cofactors are excluded from the assertion, correctly.

The result is whole active-plane cofactor nonvanishing, not a claim
that a specified pure coefficient is nonzero, that the cofactor is
diagonal, or that every original block is palette-contained.

## 6. Singleton injectivity and the retained crossing contribution

On the corrected larger-shore domain, a row supported only at t
has response z_t F_t: all t-incident edges vanish when multiplied
by z_t. Since z_t and F_t occupy disjoint sets of sites, a nonzero
z_t times the now-proved nonzero F_t is a nonzero simple tensor.
Thus the map is injective on each individual V_t for t in T,
including every extra local direction. This proves no general
injectivity on the sum of those site spaces.

For a T-supported kernel K, extracting its t-coordinate j yields
the same exhaustive two-occupancy formula

    k_(t,j) F_t+K_(T without t) U_j Q_t^[w-1]=0.

For an outside-palette j=c, a nonzero scalar k_(t,c) forces the
second WHOLE term to be the nonzero tensor -k_(t,c)F_t. There is
no support contradiction: K away from t is on the opposite shore
from U_c and their product can fill Q_t together with its crossing
edges. If U_c=0 the second term is zero and the scalar is excluded,
but no such zero is supplied for general rows by other-site axis
witnesses or the two protected target equations in this proof.
The source preserves this exact crossing term and leaves general
multi-site outside-palette kernels and coupled minor problems open.

## 7. Dependency checks, frozen inputs and final scope

The complete retained-vacuum canonical proof has 161 lines and SHA256
`b2cd2d28691d5d502bc24cc7be1bbe321053b2bedfcb1ada86e7a096c9d29997`.
Its independent companion has 169 lines and SHA256
`3d731cf9d0387e5f6ac8ddd735b0321a0ca62c828c22e1bbb5cff21528b6501f`.
The source link and its Section 1 fragment resolve. Both v1 and v2,
these two inputs, and all 375 canonical records including 181 audits
remain unchanged. The canonical records match their saved complete
texts, hashes and line counts in the authoritative manifest, SHA256
`0c8b0bbc7785c72934d58f26177f14bebcb7cdc887e679736ce97662354e88a4`.

Only this new audit was written. No numerical census, auxiliary
injectivity theorem, or independent cofactor fitting enters the proof.
The corrected all-order cofactor theorem and its stated corollaries
pass completely; no general forbidden-order or source-coverage claim
is inferred.
