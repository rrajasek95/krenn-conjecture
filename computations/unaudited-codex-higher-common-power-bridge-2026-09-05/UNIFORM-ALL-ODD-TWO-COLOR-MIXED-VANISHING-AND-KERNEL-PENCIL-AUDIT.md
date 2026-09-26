# Independent audit of binary mixed-word vanishing and the kernel pencil

**Result: complete mathematical audit PASS, without source correction.**
The site-dependent reflection proves the stated vanishing on the whole
diagonal-response space. The finite pencil has the exact common factor
1/[r!(2r+1)] at order r and an explicit remainder using all three colors.
It gives a conditional target-preserving operation, with no existence
of a useful parameter or improvement guaranteed.

Auditor: `/root/one_bad_tree`, independently of author
`/root/audit_tree_chords`, 2026-09-12. Only new `/tmp` audit artifacts
are written. All 219 protected repository records remain unchanged.

## 1. Complete frozen inputs and actual hypotheses

I read and reconstructed every section of the new source:

    /tmp/krenn_sitewise_reflection_binary_mixed_vanishing_20260912.md
    184 lines; 7973 bytes
    SHA256 6faf37edbe2a85fe6b6d5e839e3283c7a13d84184d7483e79dcbd28fa39382cd

I also read both full underlying all-order notes, including their
reflection, divisibility and polarization arguments:

    /tmp/krenn_same_row_all_odd_wick_reflection_20260912.md
    170 lines; 7212 bytes
    SHA256 d5868437e5035799bc63ae44108e5fbb162fab3a0f3fc07e334b23e83a46ae8d

    /tmp/krenn_all_odd_diagonal_response_factors_and_null_pair_transfer_20260912.md
    228 lines; 10113 bytes
    SHA256 b6b4c8aa4942ed26ea1b6ffde5f5e648a62a802c0992453f827e8c925d419dc4

The new proof uses an actual ordinary quadratic R on 2m+1 physical
sites, m>=1, in the commutative site-square-zero algebra. The local
spaces are EXACTLY ternary in the main decomposition: their designated
axes a,b,c exhaust every output word. The response space D is linear,
every row in D has a whole diagonal response, and its three amplitude
functionals are independent. In particular each is a nonzero polynomial.

D need not be the entire diagonal-response preimage space. Taking it
to be that entire space is permitted and gives the strongest stated
application to a full rank-three root response. For a smaller D, the
pencil kernel is correctly defined as D intersect ker(Phi_R); arbitrary
kernel rows outside that chosen D are not silently included.

## 2. The site-dependent reflection is valid on the same actual core

The formal Wick functional is a polynomial sum over labeled pairings.
Its physical covariance entries are precisely R, and an auxiliary g
has covariance L_i(h) with each physical coordinate and zero covariance
with itself. Thus a moment with p labeled g occurrences and one
coordinate at each of the 2m+1 sites is exactly L^p R^[m-r] for
p=2r+1: the p! auxiliary assignments agree with L^p, and the remaining
ordinary pairings agree with the divided power. This is not a Gaussian
positivity argument and does not require a nonsingular covariance.

For two independent identical replicas, the displayed rational matrix
is orthogonal, has determinant -1, and fixes (s,t). Applying it to ALL
replica pairs, including both auxiliary variables, preserves every
pairwise covariance. Multilinearity of the pairing definition therefore
preserves the full Wick functional under that substitution.

Each local determinant changes by det(M)=-1 even when its two chosen
colors depend on the physical site. The auxiliary combination s g_1+t
g_2 is fixed, while the odd number of determinants changes overall sign.
This proves equation (4). Although the proof uses C(s,t), the original
moment is polynomial, so coefficient extraction is justified over C
without assigning values at s^2+t^2=0.

Extracting s^p t from the moment of degree p+1 gives exactly p+1 times
the antisymmetrized product in (5). Replica independence supplies the
actual two response coefficients at the complementary local words.
No discarded matching, source change, or change of target basis is
involved. Intermediate variables belong to the full auxiliary polynomial
algebra; physical site occupancy is used when identifying the final
matching coefficients, not imposed incorrectly during the reflection.

## 3. Isolation, polynomial cancellation, and full polarization

For a mixed word w avoiding an active color h, choose at each site
the determinant with first color w_i and second color h. In a diagonal
second-factor word, a constant color other than h would need to occur
in w at every site, which is impossible because w is mixed. The all-h
word uses the second choice at every site and occurs only at I empty.
Its sign is positive. The first-factor word is then exactly w.

Consequently the reflection gives

    f_h(L) [w](L^p R^[m-r])=0

on the entire vector space D. This is a polynomial identity, not merely
an identity on rows at which f_h(L) happens to be nonzero. Since f_h is
a nonzero linear polynomial in the integral domain C[D], it can be
cancelled. The coefficient therefore vanishes on ALL D, including the
kernel and every hyperplane f_h(L)=0.

The broader wording in the theorem is correct: this particular mixed
word requires only one active omitted color, not three independent
functionals. Rank three ensures an active omitted color for every
mixed two-color word in the ternary alphabet.

Substitution of L=sum z_j L_j and extraction of z_1...z_p produces
p! times the corresponding product of arbitrary rows L_j in D.
Division is valid over C. Thus equation (7) is the full multilinear
identity, including repeated rows by specialization. It is stronger
than checking only equal-row products and is the version required
for the pencil containing C, repeated U and repeated V.

## 4. The common pure factor and its polarization constants

Using the constant a,b local pair in the same reflection leaves only
the two opposite pure words against a diagonal response. The odd site
count gives their relative minus sign. Hence

    f_b t_a=f_a t_b.

Independent linear polynomials f_a,f_b are relatively prime, so f_a
divides t_a. The resulting common quotient q_r works for all three
colors by the same identity and cancellation of a nonzero f_a. It is
unique and homogeneous of degree 2r; q_0=1. The quotient may be zero.

Let Q_r denote its symmetric polarization normalized on repeated rows.
For p=2r+1, extracting p distinct scalar parameters from t_h=f_h q_r
gives p! times the product-response coefficient on the left and
(p-1)! times the sum of f_h(L_j)Q_r(remaining rows) on the right.
Their ratio is precisely 1/(2r+1), as stated in (9).

In the product C U^r V^r, all terms except the one evaluating f_h on C
vanish because U,V are kernels. There is no extra binomial multiplicity
from assigning the repeated U,V rows after this multilinear identity.
The pure coefficient is therefore

    f_h(C) Q_r(U repeated r,V repeated r)/(2r+1).

For r=0 this reduces to the original response, with the zero-linear
polarization Q_0=1 understood. For r=m the remaining R power is zero
and well defined. Thus all boundary orders are covered.

## 5. Literal quadratic pencil, whole output, and conditional operation

The product UV is an ordinary pair quadratic in the site algebra:
its block on distinct sites i,j is U_i tensor V_j plus V_i tensor U_j;
same-site products vanish. It may have zero or previously absent pair
blocks. It need not satisfy (UV)^2=0. The new source correctly retains
every allowed power and expands

    (R+tUV)^[m]
      =sum_(r=0)^m (t^r/r!) U^r V^r R^[m-r].

Combining the preceding pure coefficient with t^r/r! gives exactly
the claimed p_(U,V)(t). For example the first correction is
t Q_1(U,V)/3 and the second is
t^2 Q_2(U,U,V,V)/10. These low-order constants agree with the general
1/[r!(2r+1)] formula and are not powers of the cubic coefficient.

The scalar factor is independent of C and of the chosen color because
the same q_r is used and all remaining rows are kernels. At t=0 it is
one, even if every positive-degree q_r vanishes on the chosen kernel
arguments. This proves the pure part of the decomposition.

All mixed two-color coefficients vanish term by term by the fully
polarized identity. Since the local alphabet is exactly ternary, every
remaining word uses all three colors. Subtracting the common pure
part therefore gives the stated whole tensor M_C(t), linear in C,
polynomial in t, and zero at t=0. No other kind of output was dropped.

For actual root rows C_h with the stated nonzero pure responses, if
all three M_(C_h)(t) vanish and p(t) is nonzero, dividing all three rows
by p(t) gives exactly the original amplitudes on the literal new core.
This is a correct conditional ordinary-source construction.

It is not an existence or progress theorem. The hypotheses do not
force a nontrivial kernel, UV!=0, a nonconstant p, a useful nonzero t
satisfying the common remainder equations, or an improvement of any
source complexity. Merely choosing nonzero row representatives does
not by itself establish that their product is a useful correction.
The core change may add pairs, alter old sole ports, or add scalar
entries. No anchor-preservation or decrease follows from this formula.
Avoiding the finite zero set of p(t) resolves only the rescaling
denominator; it does not solve the three-color mixed equations.

## 6. Sharp limitation: all diagonal-factor reflection tests are blind

There is a stronger scope fact than the existence of a displayed
three-color example. It follows directly from the same contractions
and holds even if arbitrary covectors replace the local coordinate
choices in the determinants.

Let ell_i,k_i be any two covectors at site i. Contracting its local
alternating tensor against a second-factor coordinate h produces the
first-factor covector

    v_i^(h)=k_i(h) ell_i-ell_i(h) k_i,
    v_i^(h)(h)=0.

If a first-factor word w uses all three colors, then for each h in
{a,b,c} some site carries w_i=h. At that site the displayed covector
kills the word. Therefore the full alternating contraction of w
against h^Omega is zero for EVERY choice of local covectors. Summing
over h proves the same statement against any diagonal second tensor.

Consequently the entire span of all-three-color words is invisible
to EVERY such q=1 reflection identity, even with arbitrary independent
site-dependent covectors. Adding a tensor from that span to a higher
response cannot be detected by these diagonal-factor tests. Repeating
or varying those tests alone cannot control M_C(t). Further constraints
must use, for example, higher p,q compatibility with a nondiagonal
factor or another actual full-source equation. This is a precise
limitation of this proof step, not a claim that the actual remainder
can be independently chosen or that it must be nonzero.

## 7. Actual four-site control and preservation

In the example, multiplication of a_1,b_2,c_3 by the displayed R gives
respectively a^Omega,b^Omega,c^Omega. Every unwanted product occupies
a site twice and vanishes. Cubing alpha a_1+beta b_2+gamma c_3 gives
exactly 6 alpha beta gamma a_1 b_2 c_3, including its factorial.
Attaching the fourth root with those three pure rows is thus an actual
ordinary ternary source with a nonzero three-color higher odd response.

The specified D in this example maps injectively to its three targets,
so its kernel K is zero. The source explicitly refrains from claiming
that the example exhibits a nonzero kernel pencil or nonzero M_C(t).
It verifies the broader odd-response limitation only, which is the
correct scope of this control.

No correction to the frozen 184-line source was required. The separate
receipt verifies it, both full frozen dependencies, and all 219 actual
repository texts, hashes and line counts against

    /tmp/krenn_pruning_frame_transfer_final.json
    SHA256 f07014765f39f83dba4ac9fdb627fe466b4ebaa05aea7d7f58ff3990f2c31338.

The result is universal for the stated actual rank-three response
spaces. It isolates the remaining three-color errors but neither
eliminates them nor proves an admissible improving move or a descent.
