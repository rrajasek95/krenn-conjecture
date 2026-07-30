# Related work and Lean artifacts for the remaining frontier

Search date: 2026-07-30.

This search used ordinary background literature and the official Mathlib
repository.  It did not search for a solution or status report for Krenn's
conjecture.  The Mathlib declaration audit used commit
[`60af7185`](https://github.com/leanprover-community/mathlib4/tree/60af7185ecf32ed5cab100f9960f1d588b9a6cab).

## 1. Verdict

No standard theorem closes the source-relative full-nine overlap gate in the
[consolidated frontier](consolidated-proof-frontier.md).  The established
results divide into three classes.

1. Numata's strong-Lefschetz theorem gives a genuinely useful inverse at the
   **aggregated six-site matching-algebra layer**.  The repository's weighted
   provenance guard shows that this inverse, separated selectors, and one
   diagonal anchor still do not produce a physical own-edge tangent.
   Transporting the four complementary-cut curvature normal through two
   differently labelled anchors and a crossed four-index row in a
   source-faithful, grade-preserving decorated overlap is the sharpened
   candidate; its sufficiency and minimality remain open.
2. Nullstellensatz/localization and Sylvester/resultant APIs already cover
   most of the commutative-algebra shell needed after the physical overlap
   lemma is found.
3. Determinantal exactness, tensor splitting, and matroid union explain the
   shape of the remaining arguments but do not supply their source-provenant
   hypotheses.

Thus the literature sharpens the next work; it does not replace the missing
physical lemma.

## 2. Matching-algebra Lefschetz inverse

For the matching-generating polynomial

\[
 \Phi_{U,k}=\sum_{M\text{ a }k\text{-matching of }K_U}
                   \prod_{e\in M}x_e,
\]

[Numata](https://arxiv.org/abs/2302.11039) proves that its apolar algebra is
strong Lefschetz over a field of characteristic zero (in the nonzero range
\(2k\leq |U|\)), with Lefschetz element \(\ell=\sum_e x_e\).
Multiplication gives isomorphisms

\[
 \ell^{k-2d}:A_\Phi^d\longrightarrow A_\Phi^{k-d}.
\]

For \(|U|=6\) and \(k=3\), \(\Phi\) is the generic \(K_6\) hafnian and
\(\ell:A^1\to A^2\) is an isomorphism.  In the edge and four-subset bases,
its matrix is

\[
                         W_{V,e}=1_{e\subset V}.
\]

After identifying a four-set with its complementary edge, this is the
disjointness matrix of \(KG(6,2)\).  An independent exact audit gives
\(|\det W|=1458\) and the inverse coefficients

\[
 W^{-1}_{e,f}=
 \begin{cases}
  1/2,&e=f,\\
 -1/6,&|e\cap f|=1,\\
  1/6,&e\cap f=\varnothing.
 \end{cases}
\tag{1}
\]

The inverse statement is over characteristic zero, as above; the same finite
identity works over any coefficient ring in which \(6\) is invertible.

Indeed, for fixed edges \(e,h\), summing the proposed inverse coefficient over
the six edges disjoint from \(e\) gives respectively

\[
 6(1/6)=1,\qquad 3(-1/6)+3(1/6)=0,\qquad
 1/2+4(-1/6)+1/6=0
\]

when \(h=e\), \(|e\cap h|=1\), and \(e\cap h=\varnothing\).  Thus both matrix
products are the identity (the two matrices are symmetric).  The
complement-indexed disjointness matrix has
spectrum \(6^1,(-3)^5,1^9\), hence determinant \(-1458\); the original
lexicographically indexed four-set/edge matrix has determinant \(+1458\).
Formula (1) is therefore an exact, audited finite aggregate incidence
inverse; it is not by itself a physical own-edge lift.  The lightweight exact checker
[`verify_k6_matching_lefschetz_inverse.py`](../computations/verify_k6_matching_lefschetz_inverse.py)
multiplies both rational matrices and computes the determinant without a
computer-algebra dependency.

[Shafiei's hafnian apolar theorem](https://arxiv.org/abs/1212.0515), over a
field of characteristic zero or characteristic \(p>2\) using the contraction
action, gives the complementary local relations: edge squares, incident-edge
products, and two independent differences among the three matchings on every
four-set generate the apolar ideal in the off-diagonal variables.  In the full
symmetric-variable ring, the diagonal differential variables are additional
linear annihilators.  Differentiating by an edge deletes its two endpoints
from the hafnian.  The repository's
[independent apolar audit](shafiei-generic-hafnian-apolar-lift-obstruction-independent-audit.md)
checks the six-site specialization and its limitations.

**Exact relevance.**  These results invert the aggregated matching incidence
and organize the cofactor relations.  They forget which fixed-label physical
row supplied a coefficient.  The
[weighted source-provenance guard](k6-lefschetz-source-provenance-guard.md)
shows more precisely that maximal rank and one complete labelled anchor are
still insufficient.  A weighted four-cycle obstruction transports under the
inverse to exactly four complementary cuts and is the derivative of
residual-edge curvature on the rank-one torus.  It is only a linearized
one-chart normal in that construction.  The repository's
[finite-polarization theorem](k6-finite-curvature-polarization-and-grade-transport.md)
removes the abstract finite-to-linear mismatch: every invertible
\(2\times2\) curvature rectangle is a sum of two rank-one rectangles and
its determinant is exactly the four-cycle derivative in the second
direction.  The remaining lemma must realize that transverse correction
through the physical labelled anchors and crossed four-index row while
preserving fixed-label source provenance and the direct/star/internal
grading.  The existential aggregate polarization is not itself a source
map.

**Lean status.**  No hafnian, matching apolar algebra, Kneser incidence
matrix, or strong-Lefschetz declaration was found.  The smallest useful Lean
artifact is finite: define the degree-one and degree-two \(K_6\) matching
spaces, prove (1) by matrix multiplication, and formalize the four-cycle to
weighted-complementary-cut identity.  A decorated-to-aggregated comparison
should be stated only after its exact physical source map is proved.  A
second small artifact should prove hafnian edge deletion and the four-vertex
exchange relation.

## 3. Active zeros from localization

For an algebraically closed field \(K\), a finite polynomial ring, an ideal
\(I\), and activity polynomial \(a\), the standard equivalences are

\[
 \exists x\in Z(I),\ a(x)\ne0
 \iff a\notin\sqrt I
 \iff (\forall n,\ a^n\notin I)
 \iff I K[x,a^{-1}]\ne K[x,a^{-1}].
\tag{2}
\]

When \(a\) is homogeneous of positive degree, an active affine zero is
nonzero and hence determines a projective point.  Equation (2) is exactly the
last conversion needed after a proof that an activity localization or
saturation is proper.  It does not prove that properness.

Relevant Mathlib declarations are:

* `MvPolynomial.vanishingIdeal_zeroLocus_eq_radical` in
  [`RingTheory/Nullstellensatz`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/RingTheory/Nullstellensatz.lean);
* `Ideal.mem_radical_iff` in
  [`Ideal/Operations`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/RingTheory/Ideal/Operations.lean); and
* `IsLocalization.map_algebraMap_ne_top_iff_disjoint` and
  `IsLocalization.algebraMap_mem_map_algebraMap_iff` in
  [`Localization/Ideal`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/RingTheory/Localization/Ideal.lean).

No packaged ideal \((I:a^\infty)\) saturation API was located at the audited
commit.  The next Lean wrapper should be a project theorem such as
`exists_active_zero_iff_away_map_ne_top`, followed by the homogeneous
projective specialization.

## 4. Binary resultants and jets

Over a commutative ring, Mathlib's `Polynomial.sylvesterMap` is the
bounded-degree linear map

\[
                    (p,q)\longmapsto fq+gp.
\]

The module
[`Polynomial/Resultant/Basic`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/RingTheory/Polynomial/Resultant/Basic.lean)
contains:

* `Polynomial.sylvesterMap` and `Polynomial.toMatrix_sylvesterMap'`;
* `Polynomial.adjSylvester`;
* `Polynomial.sylveserMap_comp_adjSylvester` and
  `Polynomial.adjSylvester_comp_sylveserMap` (the spelling is literal);
* `Polynomial.exists_mul_add_mul_eq_C_resultant`;
* `Polynomial.isUnit_resultant_iff_isCoprime`, with a monicity hypothesis on
  the first polynomial; and
* `Polynomial.resultant_eq_zero_iff`, over a field.

Binary projective forms have `Polynomial.homogenize`,
`Polynomial.homogenizeLM`, `Polynomial.homogenize_eq_of_isHomogeneous`, and
`Polynomial.eval_homogenize` in
[`Polynomial/Homogenize`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/Algebra/Polynomial/Homogenize.lean).
Over an infinite field, a finite family of dual hyperplanes can be avoided
with
`Module.Dual.exists_forall_mem_ne_zero_of_forall_exists` in
[`Submodule/Union`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/Algebra/Module/Submodule/Union.lean).
For a nonzero polynomial over a commutative ring, the exact order-two jet
criterion

\[
  1<\operatorname{rootMultiplicity}_t(p)
  \iff p(t)=0\ \text{and}\ p'(t)=0
\]

is `Polynomial.one_lt_rootMultiplicity_iff_isRoot` in
[`Polynomial/FieldDivision`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/Algebra/Polynomial/FieldDivision.lean).

**Exact relevance.**  This is sufficient infrastructure for the abstract
rootless Macaulay/resultant ledger once a source-derived annihilator is
constructed.  It cannot construct that annihilator.  The useful project
wrappers are a fixed-bidegree projective common-root/resultant theorem and a
homogeneous two-chart order-two-vanishing lemma.

## 5. Determinantal exactness

The
[Buchsbaum--Eisenbud exactness criterion](https://stacks.math.columbia.edu/tag/00MR)
characterizes exactness of a finite free complex over a local Noetherian
ring by expected ranks and grade/regular-sequence conditions on maximal-rank
minor ideals.  The
[original paper](https://doi.org/10.1016/0021-8693(73)90044-6) gives the
classical source.

This could certify a two-chart overlap complex after activity localization
only after the project constructs the literal differentials and proves the
minor-grade hypotheses.  Those are the missing physical assertions, and the
square-zero matching relations make them nonautomatic.

Mathlib contains `RingTheory.Sequence.IsRegular` and
`ModuleCat.exists_isRegular_tfae` in
[`RegularSequence`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/RingTheory/Regular/RegularSequence.lean)
and
[`Depth/Rees`](https://github.com/leanprover-community/mathlib4/blob/60af7185ecf32ed5cab100f9960f1d588b9a6cab/Mathlib/RingTheory/Depth/Rees.lean).
It does not currently provide the determinantal/Fitting-ideal layer,
algebraic Koszul complexes, Eagon--Northcott, Buchsbaum--Rim, or the
Buchsbaum--Eisenbud criterion.  A project-specific three-term exactness
lemma is much smaller than formalizing this general stack.

## 6. Product-tensor splitting

[Lovitz--Petrov](https://doi.org/10.1017/fms.2023.20) prove over any field
that, for \(n\geq2\) product tensors with \(m\geq2\) factors, if the finite
multiset of nonzero product tensors has span dimension at most
\(\sum_j(d_j-1)\), where \(d_j\) is its factor-span dimension in slot \(j\),
then it splits into two proper submultisets whose spans form a direct sum.
In particular, an \(n\)-term product-tensor circuit has \(d_j>1\) in at most
\(n-2\) slots.

This advances the Segre-circuit backup only after a matching-compatible
separator is proved: an abstract split need not survive edge deletion or
exchange.  Mathlib has tensor-product constructors and bases, including
`TensorProduct.mk`, `TensorProduct.induction_on`,
`Module.Basis.tensorProduct`, and `PiTensorProduct.tprod`, but no packaged
product-tensor predicate, tensor rank, Segre variety, or splitting theorem.

## 7. Rado and matroid union

[Rado's theorem](https://doi.org/10.1093/qmath/os-13.1.83) characterizes
independent representatives of a finite family by the rank inequalities
\(r(\bigcup_{j\in J}A_j)\ge|J|\).  The
[Edmonds--Fulkerson matroid-union theorem](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn3p147_A1b.pdf)
for finite matroids on a common ground set gives

\[
 r_{M_1\vee M_2}(X)=
 \min_{T\subseteq X}\bigl(|X\setminus T|+r_1(T)+r_2(T)\bigr).
\]

These results validate the abstract selector/maximal-shore split already
used in the project.  They do not produce the own-edge coefficient lift.
Mathlib has substantial matroid basics—bases, circuits, extended rank, and
duality—but no matroid union, transversal matroid, Rado theorem, or
vector-representability API.  The declarations `Matroid.sum` and
`Matroid.disjointSum` in the module `Mathlib.Combinatorics.Matroid.Sum` are
direct/disjoint-ground-set sums, not matroid union.

## 8. Recommended formalization order

1. Formalize the audited explicit \(K_6\) middle-Lefschetz inverse (1) and
   four-cycle/complementary-cut guard, followed by the finite-curvature
   rank-one polarization.  State the source congruence
   \(d\kappa_q(\beta_{\rm src})=AU-BF\) only after the exact physical overlap
   map and its grading are fixed.
2. Package the active-zero/localization equivalence (2).
3. Add projective resultant/common-root and two-chart jet wrappers around
   the existing polynomial APIs.
4. Formalize full determinantal exactness or product-tensor splitting only
   after the physical overlap map is fixed.

The first item is the only literature-derived object here with a plausible
chance of advancing the mathematical proof rather than merely formalizing
an already understood implication.
