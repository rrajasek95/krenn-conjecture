# Initial Lean formalization of the all-orders argument

This package proves eight algebraic lemmas used in the written Krenn–Gu
argument. It does **not** yet prove the full conjecture in Lean. The source
identities needed by these lemmas remain explicit hypotheses.

Read the [cited research PDF](../../proofs/krenn-gu-all-orders-paper.pdf) for the
complete written argument and its review status.

## What is checked

| Module | Proved content | Scope |
|---|---|---|
| [PolynomialODE.lean](PolynomialODE.lean) | Six lemmas: polynomial solutions of `p' + d p = 0` vanish when `d ≠ 0`; solutions of `p' + d p = k` are constant; coefficient and cancellation consequences give the scalar endpoint identity. | The first five lemmas work over any commutative integral domain, including polynomial coefficient rings. The division form assumes a field. |
| [EndpointDegree.lean](EndpointDegree.lean) | Two lemmas: the endpoint identities and a nonzero row expansion imply that the row has exactly one supported entry, and hence a unique supported neighbor. | A finite index type and a field of characteristic zero; the expansion and endpoint identities are hypotheses. |

All eight proofs compile with warnings treated as errors. The
[axiom report](axioms.txt) lists only `propext`, `Classical.choice`, and
`Quot.sound`; there are no proof holes, custom axioms, or native-evaluation
proofs. [Verification metadata](verification.json) records the source hashes
and exact toolchain.

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
lake --wfail build
lake env lean -DwarningAsError=true CheckAxioms.lean
```

The toolchain is Lean 4.33.1. The manifest pins mathlib revision
`0df444a360eaa60ab8c11dca51a86af692955474` (tag `v4.33.1`).

## Remaining formalization

1. Define the physical-site algebra and identify its divided top power with
   the upstream recursive perfect-matching sum.
2. Formalize the reflection identities, the whole binary response tower
   including its terminal term, even-omission vanishing, and global diagonal
   reduction.
3. Define the finite two-replica kernel, prove its orthogonal covariance, and
   establish the polynomial matrix normal form and invariant-ring description.
4. Derive the two polynomial differential equations from those identities,
   then apply `PolynomialODE.lean` to obtain the supported endpoint identity.
5. Prove the hafnian row expansion and instantiate `EndpointDegree.lean`.
6. Formalize the three-matching obstruction and connect the resulting ternary
   contradiction to the upstream equation system and color-restriction API.

These steps contain substantial mathematical work. The compiled algebraic
lemmas do not certify the unformalized bridges or the entire written proof.
