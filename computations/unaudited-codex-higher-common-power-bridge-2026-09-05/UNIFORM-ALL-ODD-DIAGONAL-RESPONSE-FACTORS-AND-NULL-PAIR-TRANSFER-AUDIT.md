# Independent full audit: all odd diagonal-response factors and null-pair transfer

**Outcome: PASS.** I read the complete frozen source and independently
reconstructed every theorem and application. No author correction is
required. The all-order conclusions control specified pure coefficients;
the source correctly leaves general mixed-error and coverage questions open.

Auditor: `/root/dense_nontree`, 2026-09-12.

## 1. Exact frozen input and read scope

Source:

    /tmp/krenn_all_odd_diagonal_response_factors_and_null_pair_transfer_20260912.md
    228 lines; 10113 bytes
    SHA256 b6b4c8aa4942ed26ea1b6ffde5f5e648a62a802c0992453f827e8c925d419dc4

I read all seven source sections in full after the author supplied this
freeze, including the reflection, polynomial factorization, radical
claim, complete pair expansion, and the minimum-order scope restriction.
The source is self-contained and has no unresolved Markdown link or
fragment dependency. Its mathematical proof does not rely on numerical
rank experiments, the special path family, or the failed variable-weight
repair as an input.

I also fully read the independent reflection derivation:

    /tmp/krenn_same_row_all_odd_wick_reflection_20260912.md
    170 lines; 7212 bytes
    SHA256 d5868437e5035799bc63ae44108e5fbb162fab3a0f3fc07e334b23e83a46ae8d

Its formal auxiliary calculation agrees with my independent two-replica
reconstruction. I separately read the actual rank-one mixed-error control
and the complete 275-line variable-weight lower-core note to check the
application's hypothesis boundary. Neither is needed for the main proof.

## 2. Actual map, target rank, and degree conventions

The ambient core has odd order N=2m+1>=3. Phi_R is the WHOLE response
L R^[m], and D_R is the inverse image of the designated three-dimensional
diagonal tensor space. It is a linear space and contains the complete
kernel K_R. The f_h are genuine linear functionals on D_R.

The premise is rank at least two for the joint diagonal target image.
It is stronger than merely having two independent row preimages: two
independent kernel directions or two preimages of the same target do
not suffice. At an actual full ternary source the original three root
rows have three independent nonzero pure responses, so its odd core
meets this premise at every root.

For r in 0,...,m, the expression L^(2r+1) R^[m-r] has degree N and is
a homogeneous polynomial of degree 2r+1 in the row coefficients. The
notation divides the R power by (m-r)!, but does NOT divide the row
power by (2r+1)!. I retained that distinction throughout the audit.

## 3. Exact formal Wick realization and reflection

The formal Wick functional is defined by finite sums of products of
symmetric covariances over pairings of labeled occurrences. It is
well-defined for arbitrary complex, singular, or indefinite covariance.
No probabilistic existence assertion or analytic integration is used.

For a word containing one physical coordinate per site, each auxiliary
g occurrence must pair with a different physical occurrence because
cov(g,g)=0. For d such occurrences there are d! assignments to a chosen
set of d physical sites. This exactly matches the multiplicity of L^d.
The remaining physical pairings each occur once in R^[(N-d)/2]. Thus
the whole tensor represented by the moment is H_d, with no extra or
missing factorial.

The replicated covariance is the direct sum of two identical full
covariance matrices, including auxiliary-to-physical entries. Applying
the same orthogonal two by two matrix to EVERY corresponding pair,
including g_X,g_Y, preserves all covariances. Wick invariance follows
by multilinearity of the pairing definition.

The displayed rational reflection has determinant -1, squares to the
identity, and fixes (s,t). Consequently it fixes s g_X+t g_Y and negates
each local two-color determinant Delta_i. Their product changes by
(-1)^N=-1. The moment therefore vanishes over C(s,t).

The original moment is a polynomial in s,t, so equality in the rational
function field is a polynomial identity. This reasoning makes no
invalid specialization at s^2+t^2=0 and needs no positivity premise.
Extracting s^p t^q yields the nonzero binomial(p+q,p) times precisely
the stated antisymmetrized product H_p H_q. The identity is valid for
arbitrary actual L and R before any diagonal specialization.

The reflection is performed in an auxiliary ordinary polynomial
algebra. It is not asserted to be a physical-site-algebra automorphism
or an operation on the source. Repeated sites in intermediate replica
expressions therefore cause no conflict with the matching realization.

## 4. Diagonal specialization and the common polynomial factors

With one factor H_1 diagonal, all antisymmetrization terms except the
empty and full subsets vanish. Odd N gives opposite signs for these
two terms. The resulting exact identity is

    f_b t_(a,r)=f_a t_(b,r).

It holds as a polynomial identity on the entire linear space D_R.
Rank at least two supplies two independent linear functions f_a,f_b;
they are nonzero, irreducible, and relatively prime in C[D_R]. Unique
factorization then gives t_(a,r)=f_a q_r and t_(b,r)=f_b q_r. Using
the same identity with the remaining color gives its factorization,
even when that remaining f_h is identically zero.

Uniqueness follows by cancellation of a nonzero polynomial f_a in an
integral domain. This is ordinary polynomial divisibility on row space,
not cancellation by a zero divisor in the physical-site algebra.
The quotient is homogeneous of degree 2r, and q_0=1. Zero q_r and
points where individual f_h vanish are included; no pointwise division
or nonvanishing assumption is imposed there.

The rank-one boundary is substantive. A lone active f_h does not
force its own higher coefficient to be divisible by it. The known
actual pure-c kernel-triple control has only a rank-one diagonal
response image and is therefore outside the theorem. It does not
contradict the new zero-kernel-triple conclusion.

## 5. Polarization, kernel insertions, and the radical claim

The multilinear polarization Q_r is normalized by Q_r(L,...,L)=q_r(L).
The polarization of f_h q_r is the average over the 2r+1 choices of
the argument assigned to f_h. Therefore the factor 2r+1 in source
Equation (4) is correct, including repeated row arguments.

For all arguments in K_R, every f_h term is zero. Thus all designated
pure coefficients of every allowed odd kernel product vanish. This
is not a statement that the full colored tensor vanishes.

At r=1 the formula is exactly

    3 [h^Omega] C U V R^[m-1]=f_h(C) B(U,V)

for C in D_R and U,V in K_R. In particular the coefficient is B/3,
not B or B/6, in the pair-transfer formula.

If a kernel row U has no receiving component of an active color h,
the pure-h coefficient of U L L R^[m-1] is zero. Its polarization
identity reduces to 2 f_h(L) B(U,L)=0. Polynomial cancellation then
makes B(U,.) zero on D_R, as claimed. This does not require U to be
coordinate-supported, but the source's one-coordinate corollary is
valid under its stated active-color assumption.

## 6. Full two-site expansion and the common pair matrix

For the actual extension Q0, omitting q leaves R plus the r star.
Only one r-star factor can occur, so its complete top cofactor is
sum_j e_j(r) B_j R^[m]=0. The q-star case is identical. Thus even
arbitrary q,r components of C_total have zero WHOLE response and
may be omitted in Equation (7).

For its retained Omega row C, a full output must occupy both q and r.
There are exactly two possibilities: the direct pair J once, or one
q-star and one r-star. They give

    J C R^[m]
      +sum_(i,j) e_i(q)e_j(r) C A_i B_j R^[m-1].

The latter has coefficient one: the two ordered star choices cancel
the 2! from the relevant divided expansion. There are no further
pair-occupancy terms, no unstated square-zero condition on A_i B_j,
and no discarded higher contraction-error term.

When C lies in D_R, projection onto the three pure Omega words and
the cubic formula give exactly

    Phi_R(C) tensor M,
    M=J+(1/3)sum_(i,j)B(A_i,B_j)e_i(q)e_j(r).

M is independent of both C and the chosen color. All nine q,r cells
remain in it. An additional ordinary pair E changes only M to M+E.
The formula projects the Omega factor alone; it does not declare the
other colored Omega coefficients zero.

## 7. Pure-target obstruction and conditional smaller source

If the WHOLE extended response is nonzero pure c and C is in D_R,
its pure projection forces f_c(C) M=tau c_q c_r. In particular both
f_c(C) and M are nonzero. The pure-a and pure-b equations then force
f_a(C)=f_b(C)=0. Hence the actual lower response is already nonzero
pure c.

This also excludes the case Phi_R(C)=0, without needing a separate
assumption that a nonzero lower response was diagonal: a zero response
already puts C in K_R, hence in D_R. In the actual two-pure lower-core
branch the target-rank premise follows from its a_x and b_y responses,
so a zero third lower response contradicts the ORIGINAL full c target.
This is stronger than failure of one particular repair.

A single M cannot be a nonzero multiple of two distinct coordinate
pair tensors. The source's obstruction to two different full pure
targets from diagonal lower responses, including after a shared pair
correction, therefore follows directly.

If actual pure-a and pure-b preimages on R are present and the lifted
c preimage has a diagonal lower response, the latter is nonzero pure c.
Adding a root to these three actual rows constructs an ordinary source
on Omega plus one site, exactly two sites smaller. Each nonzero target
amplitude can be fitted. This is a contradiction only when that smaller
order is forbidden; the allowed four-site ternary source is explicitly
excluded from the contradiction claim. No preservation of every old
anchor during this smaller-source construction is asserted or needed.

A nonzero MIXED lower response is not in D_R and is not covered by
this implication. Neither its diagonality nor useful-pair existence
is supplied by the theorem. These remaining gaps are correctly stated.

## 8. Additional independently checked consequences

The general transverse pure-cofactor pairing identity is already a
cubic specialization of this source. Actual pure cofactors at distinct
x,y put a_x,b_y in D_R with independent responses kappa_x a^Omega and
kappa_y b^Omega. Equation (5) gives

    3 lambda_x=kappa_x B(U,V),
    3 lambda_y=kappa_y B(U,V).

The normalized pure coefficients therefore agree. This does not need
a_x or b_y to be absent from R; multiplication by the displayed row
selects its omission cofactor. The independent colored matching proof
is a cross-check, not a required input to the frozen common-factor proof.

The following paragraph records an audited consequence of the theorem;
it is not an extra claim silently inserted into the source text.
For U,V in K_R, C in D_R, and a scalar z, the exact divided-power
expansion and source Equation (4) imply

    projection_pure [C(R+z UV)^[m]]=p(z) Phi_R(C),

    p(z)=sum_(j=0)^m z^j Q_j(U repeated j,V repeated j)
                         /[j!(2j+1)],                 (A)
    Q_0=1,             p(0)=1.

Indeed the j-th insertion is z^j C U^j V^j R^[m-j]/j!. In its
2j+1-linear polarization only the C argument has a potentially
nonzero f_h, giving the additional divisor 2j+1. Thus p is the
same polynomial for every C and every designated color. This
retains every finite insertion, not merely the first one.

Formula (A) controls pure coefficients only. It does not make the
full outputs diagonal, assert that a nonzero z solves the mixed
constraints, or prescribe an operation preserving old anchor weights.
Even when scalar amplitude fitting is algebraically possible, those
separate source-preservation requirements must still be checked.

## 9. Exact checks, immutability, and final verdict

I fully read the independent 53-line exact verifier, then imported it
without executing its output-writing entry point. Replaying its nine
actual integer controls at 3,5,7 sites gave 30 distinct odd-pair
antisymmetrization residuals, all exactly zero. These checks support
the signs and factorial convention; the reflection proves all orders.
No benchmark, census, or arbitrary-source existence conclusion is
inferred from these controls.

All 219 protected files were read and compared against their full
manifest texts, SHA256 hashes, and line counts. Every record matches.
The manifest is /tmp/krenn_pruning_frame_transfer_final.json with
SHA256 f07014765f39f83dba4ac9fdb627fe466b4ebaa05aea7d7f58ff3990f2c31338.
The frozen source, independent reflection source, and verifier remain
unchanged. I wrote only this new /tmp audit and its machine receipt.

**Final verdict: PASS without correction.** The general common-factor
and null-pair conclusions are proved under their stated actual-source
hypotheses. Mixed-error control and a general coverage or descent
argument remain unresolved.
