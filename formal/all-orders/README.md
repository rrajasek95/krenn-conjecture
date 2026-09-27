# Lean formalization of the all-orders argument

This package checks the matching-polynomial model, parts of the two-replica
algebra, and the spanning-cycle reduction in the written Krenn–Gu argument.
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
| [ReplicaCovariance.lean](ReplicaCovariance.lean) | Orthogonal covariance and off-diagonal divisibility force a polynomial matrix to have the form `a I + b P Qᵀ`, including isotropic parameters. | The covariance and divisibility are explicit hypotheses. Their derivation for the physical kernel is still required. |
| [ThreeMatching.lean](ThreeMatching.lean) | Partner involutions agree with graph perfect matchings; matching switches and shared edges yield mixed words; absence of mixed words forces a spanning two-colour cycle. | Used by the checked final combinatorial theorem below. |
| [CycleCoordinates.lean](CycleCoordinates.lean) | A spanning cycle gives bijective cyclic coordinates preserving its edges. | Supplies the coordinate bridge needed for the chord argument. |
| [MatchingTransport.lean](MatchingTransport.lean) | Relabels matchings and proves that a matching covered by disjoint colour matchings has a consistent receiving word. | Two differently coloured witness edges then certify a mixed word. |
| [ChordObstruction.lean](ChordObstruction.lean), [ThreeMatchingObstruction.lean](ThreeMatchingObstruction.lean) | On more than four vertices, every family containing three labelled perfect matchings has a mixed receiving word. | The combinatorial obstruction is unconditional; deriving colour matchings from the weighted source remains necessary. |
| [FiniteResponseRigidity.lean](FiniteResponseRigidity.lean) | A finite multivariate polynomial with `g(s L)^2 = g(L)`, `s ≠ 0`, and `g(0) = 1` is identically one. | The rotation identity is an explicit premise until formal Wick covariance is instantiated. |

The integrated modules compile with warnings treated as errors. The
[axiom report](axioms.txt) lists only `propext`, `Classical.choice`, and
`Quot.sound`; there are no proof holes, custom axioms, or native-evaluation
proofs. [Verification metadata](verification.json) records the source hashes
and exact toolchain. The current audit checks 153 declarations, including
definitions with proof fields; this number is not a count of theorems.

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

1. Finish the physical-site quotient algebra and identify the divided top
   power with the matching polynomial. The ordinary polynomial coefficient
   bridge and the exact upstream adapter are checked.
2. Formalize the reflection identities, the whole binary response tower
   including its terminal term, even-omission vanishing, and global diagonal
   reduction.
3. Define the finite two-replica kernel, prove its orthogonal covariance, and
   establish its invariant-ring description. The abstract polynomial matrix
   normal form is checked; its physical hypotheses remain to be proved.
4. Derive the two polynomial differential equations from those identities,
   then apply `PolynomialODE.lean` to obtain the supported endpoint identity.
5. Prove the hafnian row expansion and instantiate `EndpointDegree.lean`.
6. Apply the checked three-matching obstruction to the supported colour
   matchings and connect the ternary contradiction to the upstream equation
   system and color-restriction API.

These steps contain substantial mathematical work. The compiled algebraic
lemmas do not certify the unformalized bridges or the entire written proof.
