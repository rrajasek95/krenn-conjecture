# Lean formalization of the all-orders argument

This package checks the physical-site algebra, parts of the two-replica
argument, and the full combinatorial obstruction in the written Krenn–Gu argument.
It does **not** yet prove the full conjecture in Lean. The physical source
identities needed by the endpoint argument remain unformalized.

The [formalization workplan](WORKPLAN.md) records the parallel assignments,
integration owner, exact target, and requirements for accepting new milestones.

Read the [cited research PDF](../../proofs/krenn-gu-all-orders-paper.pdf) for the
complete written argument and its review status.

## What is checked

| Module | Proved content | Scope |
|---|---|---|
| [PolynomialODE.lean](PolynomialODE.lean) | Six lemmas: polynomial solutions of `p' + d p = 0` vanish when `d ≠ 0`; solutions of `p' + d p = k` are constant; coefficient and cancellation consequences give the scalar endpoint identity. | The first five lemmas work over any commutative integral domain, including polynomial coefficient rings. The division form assumes a field. |
| [EndpointDegree.lean](EndpointDegree.lean) | Two lemmas: the endpoint identities and a nonzero row expansion imply that the row has exactly one supported entry, and hence a unique supported neighbor. | A finite index type and a field of characteristic zero; the expansion and endpoint identities are hypotheses. |
| [MatchingModel.lean](MatchingModel.lean) | The recursive matching polynomial has the prescribed word coefficients and degree one at each physical site. | Arbitrary aggregate endpoint-colour weights; the ordered matching enumeration agrees with the upstream model through the separate adapter. |
| [SiteAlgebra.lean](SiteAlgebra.lean) | Constructs the same-site-zero quotient; proves the entire divided quadratic top power equals the matching tensor, and makes word coefficients well-defined on the quotient. | Exact arbitrary-weight graph-to-algebra bridge over characteristic-zero fields. |
| [RootResponse.lean](RootResponse.lean) | Derives the actual pure root-response tensor, arbitrary-root Laplace expansion, and unit pure cofactor row sum from the original equation system. | Root extraction first deletes the root; it never differentiates an arbitrary quotient representative. |
| [ReplicaCovariance.lean](ReplicaCovariance.lean) | Orthogonal covariance and off-diagonal divisibility force a polynomial matrix to have the form `a I + b P Qᵀ`, including isotropic parameters. | The covariance and divisibility are explicit hypotheses. Their derivation for the physical kernel is still required. |
| [GramInvariants.lean](GramInvariants.lean) | Proves the two-column orthogonal invariant ring directly by light-cone monomials, including Gram-map and axis-restriction injectivity. | Every covariant matrix satisfying the divisibility premises has unique Gram-coordinate normal-form coefficients. |
| [EndpointPDE.lean](EndpointPDE.lean) | Derives the Gram differential equations from Cartesian boundary identities, eliminates their finite polynomial solutions, and obtains the scalar endpoint identity. | The kernel covariance, divisibility, boundary identities, and origin value remain physical-source premises. |
| [WickCovariance.lean](WickCovariance.lean) | Constructs normalized finite pairing moments and proves multilinearity, linear covariance, shifted-mean expansion, and two-replica orthogonal invariance. | The identification with physical quadratic coefficients and independent-replica factorization remain separate bridges. |
| [ThreeMatching.lean](ThreeMatching.lean) | Partner involutions agree with graph perfect matchings; matching switches and shared edges yield mixed words; absence of mixed words forces a spanning two-colour cycle. | Used by the checked final combinatorial theorem below. |
| [CycleCoordinates.lean](CycleCoordinates.lean) | A spanning cycle gives bijective cyclic coordinates preserving its edges. | Supplies the coordinate bridge needed for the chord argument. |
| [MatchingTransport.lean](MatchingTransport.lean) | Relabels matchings and proves that a matching covered by disjoint colour matchings has a consistent receiving word. | Two differently coloured witness edges then certify a mixed word. |
| [ChordObstruction.lean](ChordObstruction.lean), [ThreeMatchingObstruction.lean](ThreeMatchingObstruction.lean) | On more than four vertices, every family containing three labelled perfect matchings has a mixed receiving word. | The combinatorial obstruction is unconditional; deriving colour matchings from the weighted source remains necessary. |
| [FiniteResponseRigidity.lean](FiniteResponseRigidity.lean) | A finite multivariate polynomial with `g(s L)^2 = g(L)`, `s ≠ 0`, and `g(0) = 1` is identically one. | The rotation identity is an explicit premise until formal Wick covariance is instantiated. |
| [ResponseFactor.lean](ResponseFactor.lean) | Coordinatewise proportional higher responses share a polynomial scalar factor. | The cross-multiplication identities supplied by reflection are explicit premises. |
| [ForcedMatchingSum.lean](ForcedMatchingSum.lean), [SupportMatching.lean](SupportMatching.lean) | Proves noncancellation through the actual weighted recursion; extracts partner matchings from diagonal unique-neighbour support; derives the exact ternary contradiction. | The remaining premises are the physical diagonal reduction, row expansion, and supported endpoint identities. |
| [CofactorDiagonal.lean](CofactorDiagonal.lean) | The actual source colour blocks vanish off the diagonal once the pure and mixed cofactor matrix products are established. | The cofactor sum identities remain physical-source obligations. |
| [BinaryPairing.lean](BinaryPairing.lean) | Constructs the signed-complement tensor contraction, proves pure-word extraction, parity symmetry, and the odd-site determinant formula. | Works over arbitrary commutative rings, including row-parameter polynomial rings. |
| [OmissionCancellation.lean](OmissionCancellation.lean) | Cancels the direct term using the two rotation equations and polarizes a vanishing quadratic coefficient into two independent rows. | Rotation and source-response identities remain explicit premises. |
| [PhysicalClosure.lean](PhysicalClosure.lean) | Assembles the exact ternary contradiction with actual deleted-pair cofactors. | Its only remaining physical premises are diagonalisation and the supported endpoint identity. |

The integrated modules compile with warnings treated as errors. The
[axiom report](axioms.txt) lists only `propext`, `Classical.choice`, and
`Quot.sound`; there are no proof holes, custom axioms, or native-evaluation
proofs. [Verification metadata](verification.json) records the source hashes
and exact toolchain. The audit lists every checked declaration individually,
including definitions with proof fields; its declaration count is not a count
of theorems.

The [upstream adapter](../upstream-adapter/README.md) proves exact equivalence
between local and upstream solution existence. Its eight checked theorems
compare the definitions through their recursion.

## Upstream contribution

[Draft PR #6627 in google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures/pull/6627)
adds a color-restriction definition and nine proved API lemmas to the existing
`MonochromaticQuantumGraph` model. It transports matching sums along a palette
map, restricts the equation system along an injection, and shows that ternary
nonexistence would imply nonexistence for every palette of size at least three.
The ternary nonexistence premise is not proved by that PR.

The upstream patch was compiled with Lean 4.33.1 using
`lake --wfail build FormalConjectures.Paper.MonochromaticQuantumGraph`.
Its nine new theorems also pass an axiom audit without `sorryAx` or custom axioms.
The initial upstream commit is `e2c4441f9545b85790aebcfaa445e194fcab9d5b`.

## Reproduce

Install Lean through `elan`, then run from this directory:

```sh
lake exe cache get
python3 verify.py
```

The toolchain is Lean 4.33.1. The manifest pins mathlib revision
`0df444a360eaa60ab8c11dca51a86af692955474` (tag `v4.33.1`).

## Remaining formalization

1. Identify the explicit Wick construction with the quadratic coefficients
   and independent replicas. The full quotient top-power identity and original
   root-response source interface are checked.
2. Derive the reflection identities, the whole binary response tower including
   its terminal term, and even-omission vanishing. Use these to establish the
   cofactor sum premises of the checked diagonal-reduction theorem.
3. Construct the finite physical two-replica kernel and prove its covariance,
   off-diagonal divisibility, and boundary differential identities. The
   abstract matrix normal form and complete invariant-ring theorem are checked.
4. Instantiate the checked boundary-to-Gram calculation with the physical
   kernel to obtain the supported endpoint identity.
5. Supply diagonalisation and endpoint identities to `PhysicalClosure.lean`,
   then transport the unconditional theorem through the upstream adapter and
   palette-restriction API. The actual row expansion and weighted-to-graph
   contradiction are already checked.

These steps contain substantial mathematical work. The compiled algebraic
lemmas do not certify the unformalized bridges or the entire written proof.
