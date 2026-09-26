# Independent audit of all-even omission pure-response vanishing

**Verdict: COMPLETE INDEPENDENT PASS, without source correction.**
Auditor: `/root/one_bad_tree`, 2026-09-13. I read all 204 frozen
source lines and the complete 73-line author receipt, reconstructed
every finite-mean and covariance step, and checked all consequences.
No numerical experiment is needed for the all-order argument.

Frozen source:
`/tmp/krenn_all_even_omission_pure_response_vanishing_20260913.md`
— 204 lines, 9807 bytes, SHA256
`3cb6853afd6b3926e39b1bd3bb04cda6e3a9af44d86ed20e7131a96bff85eeee`.

## 1. The row-space hypotheses and the exact odd-response dependency

D is any linear space of actual rows on one odd ordinary R, with
whole responses in the designated diagonal target space. It need
not be the entire preimage, injective, or a kernel space. Every
coordinate function f_h must be nonzero as a function on D, and
their joint rank must be at least two. A rank-two plane with three
active coordinates is included; a coordinate binary plane is not.
Individual rows may have zero response or some zero amplitudes.

I read the entire canonical higher-pure-response proof and its
independent audit. Its hypotheses explicitly allow this D and
this rank-two case. Its conclusion includes zero coefficients of
EVERY higher odd word using at most two designated colors. The
source uses that complete binary conclusion in equation (7), not
merely its three pure coefficients. The retained-vacuum proof,
which I separately audited in full, supplies covariance for the
complete finite means on arbitrary even Q, with F retained.

For extra finite local dimensions, project each local space onto
the designated a,b,c axes. This is an algebra map preserving the
ordinary quadratic and the displayed whole target equations.
If a row is killed by the projection, its projected response is
zero, so all its f_h vanish. Thus these functions descend to the
projected row space and their joint rank is unchanged. The pure
coefficients being asserted are unchanged by this projection too.
This justifies the extension without assuming a ternary theorem
already controls words containing extra coordinates.

## 2. Exact omission occupancy and the finite derivative formula

The even mean E(U) on S has term

    U^(2r) Q^[m-r]/(2r)!,       0<=r<=m.

In the q=h sector of L^(2r+1)R^[m-r]/(2r+1)!, q can be
occupied in precisely two ways. A row factor at q contributes

    d_h(L) U^(2r) Q^[m-r]/(2r)!.

Alternatively, one q-star edge contributes

    U^(2r+1) V_h Q^[m-r-1]/(2r+1)!,       0<=r<m.

The first coefficient uses the 2r+1 choices of its distinguished
row factor. The second uses the unit coefficient of one star edge
in a divided power. Two q occupancies vanish. Summing the second
display and reindexing by j=r+1 gives exactly partial_(V_h)E(U).
This proves equation (6), including the highest row-degree term
and the absence of a negative power at r=m.

Project S onto h,k while keeping q=h. Every higher odd word then
uses at most those two colors on all of Omega, so the reviewed
vanishing theorem removes it. The degree-one contribution is the
actual original h response f_h(L)h^S. Hence equation (7) retains
both d_h E(U) and partial_(V_h)E(U), with no missing direct-row term.
The V_h are the fixed original q-star rows; they need not lie in
the restricted row space U(D).

## 3. Covariance and the differentiated 45-degree identity

The product B_hk of local alternating forms is symmetric on S
because |S|=2m is even. Only h,k coordinates contribute. For
B_hk(Z,h^S), every contributing coordinate of Z is k, and the
2m local signs epsilon(k,h)=-1 multiply to +1. This proves
equation (8) with no omitted sign or normalization factor.

In ordinary replicas the local differential operator is
partial_(x_h)partial_(y_k)-partial_(x_k)partial_(y_h).
An SO2 change of the two replica columns preserves it: same-replica
terms cancel by antisymmetry and commuting derivatives, and the
remaining factor is the determinant one. The literal quadratic
sum Q(x)+Q(y) is also invariant. Extracting one coordinate per
physical site in each replica gives B_hk(E(U),E(M)) exactly.
This argument is on ordinary variables before physical extraction,
not an unjustified rotation of the site-square-zero quotient.

At the rotation with c=s=1/sqrt(2), means (U,U) become
(sqrt(2)U,0). Thus the complete covariance gives source (9).
For (U,U+tV), the rotated means are

    sqrt(2)U+tV/sqrt(2),      tV/sqrt(2).

Differentiate at t=0. E has no linear term, so its derivative at
zero is zero. The remaining derivative is precisely

    B(E(U),partial_V E(U))
      =B(F,partial_V E(sqrt(2)U))/sqrt(2).

The covariance was established for arbitrary mean rows, so this
step is valid when V=V_h lies outside U(D). Only the later use of
the original response equation is restricted to L in D.

## 4. The receiving component and both square-root factors cancel

Equation (7), inside a pairing which only sees h,k, gives

    partial_(V_h)E(U)=f_h(L)h^S-d_h(L)E(U).

At sqrt(2)L, linearity multiplies BOTH f_h and d_h by sqrt(2),
while the derivative direction V_h remains the same original row.
Consequently the right side of the differentiated covariance is

    f_h(L)B(F,h^S)-d_h(L)B(F,E(sqrt(2)U)).

Its left side is

    f_h(L)B(E(U),h^S)-d_h(L)B(E(U),E(U)).

Subtracting proves (11). The bracket multiplying d_h is zero by
the complete equal-mean covariance. No d_h value, direct block,
cofactor, or quartic term was assumed to vanish.

The remaining scalar identity is a polynomial on the ordinary
vector space D. Its coordinate ring is an integral domain and
f_h is a nonzero polynomial, so it cancels identically. This is
not pointwise division at rows where f_h(L)=0, and it is not
cancellation inside the physical algebra with zero divisors.
For each requested k there exists a different active h, proving
(12) for all three colors under the stated hypotheses.

## 5. Every even degree and every physical quadratic change

U depends linearly on L. The terms of E(U(L))-F have distinct
homogeneous degrees 2,4,...,2m, so (12) kills each pure coefficient
separately. Substitute L=sum_i t_i L_i in the degree-2r identity.
The coefficient of t_1...t_(2r) in the raw row power is (2r)!
times the desired product of restricted rows. Division by this
nonzero complex scalar proves full polarization (2), with repeats
and arbitrary row dependence allowed.

For K in the physical image of Sym^2 U_q, expand each positive
term K^[r]Q^[m-r] in (Q+K)^[m]. It is a finite linear combination
of products of 2r restricted rows, with its factor 1/r! retained.
Equation (2) therefore kills every pure coefficient of every such
term. This proves (13) for arbitrary finite K of the stated form.
Different presentations of K or zero physical products cause no
problem. No injectivity of the formal Sym^2 map is assumed.

This is pure-coefficient invariance on the even core. Binary and
three-color mixed top coefficients may change. Nor does this
calculation preserve any complete source equation outside that core.
In particular it is not an improving source operation by itself.

## 6. Full-source specialization, support and endpoints

Deleting p from a full ternary source leaves an actual odd R whose
three original p rows have three independent pure responses. They
supply a D of rank three. Its restriction off q is exactly the
original U family on Q=A restricted off p,q. Deleting q first
gives the V family on the SAME Q. Applying (2) separately proves
both parts of (14), with arbitrary direct p-q block allowed.

The claim concerns products entirely within either endpoint family.
It does not assert pure vanishing for mixed U/V products or for the
quadratic space generated by their combined span. Those mixed
products are precisely where the original pure target grid lives.
Whole deleted-pair nonvanishing is consistent additional information;
it was not used to prove this new theorem.

At r=m the pure coefficient of U(L)^(2m) is (2m)! times the product
of the receiving coordinate functions outside q. For every q this
product is zero. If at most one receiving function were identically
zero, omit that site, or any site if none is zero. Every remaining
factor would be a nonzero polynomial in C[D], a contradiction.
Thus two distinct whole missing receiving coordinates per color
follow for arbitrary D under the theorem's premises.

I checked the attribution against notes/slice-cover.md, Section 2:
the full original star already has three distinct nonzero whole
receiving-axis blocks. The two witnesses of colors different from k
have zero receiving-k columns. Hence the stated full-star count was
already known; no stronger degree or exception count is being claimed.

For m=1, E(U)=Q+U^2/2, the same derivative and scaling proof applies,
and r=1 is the only even response. This covers an odd three-site
core and a full four-site source without a negative power. The
one-site odd case m=0 is outside the stated theorem.

## 7. Other-core scope and preservation

I read the complete transverse-cofactor ratio theorem cited for
comparison. It concerns whole kernel rows and two pure cofactors
on a different odd core; it does not supply a three-active D of
rank at least two there. Its nonzero binary example therefore does
not contradict vanishing on the present restricted U_q spaces.
No arbitrary omitted core is silently assigned the new D premises.

Only this new audit and its receipt were written. The 204-line
source, author receipt and all checked frozen inputs remain intact.
All 361 authoritative records, including 174 audits, were verified
by complete text, SHA256 and line count. The separate frozen
227-line opposite-axis closure source and its receipt were also
preserved. The accompanying receipt records these exact checks.
