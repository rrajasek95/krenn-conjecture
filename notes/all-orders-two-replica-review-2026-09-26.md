# Complete all-orders proof: research acceptance, September 26, 2026

**Outcome: accepted as a complete written proof in the stated complex weighted
matching model after root review and two independent analytic audits.** No
remaining mathematical obligation has been identified in this argument.
This records internal mathematical review, not external peer review or Lean
verification. It does not modify an earlier immutable certification package.

The [self-contained proof](../proofs/krenn-gu-all-orders-two-replica-proof.md)
excludes every ordinary complex weighted source with an even number of
vertices greater than four, three nonzero pure target amplitudes, and zero
mixed target amplitudes. Projection gives the same exclusion for any larger
target dimension. Arbitrary endpoint colors, parallel-edge aggregation,
unequal amplitudes, and arbitrary density are included.

The allowed four-vertex source remains the three perfect matchings of K4.
The argument makes no exclusion at two vertices. It concerns actual finite
weights and exact matching tensors, not limits of tensors or approximate
preparation schemes.

## What closes the argument

The proof incorporates the earlier reflection and even-omission arguments,
which make every original edge block diagonal and supply the complete
higher odd response identities on each binary palette. The new step uses
two identical Wick replicas on a literal retained core.

Orthogonal covariance and the original root identities force a polynomial
matrix to have the form `a I + b P Q^T`. Its scalar coefficients satisfy

    b_c + d b = 0,        a_c + d a = beta eta,

where `d` is a supported edge weight. Because these are finite polynomials
and `d != 0`, they force `b=0` and `a=beta eta/d`. Evaluation at zero gives

    haf(B) = B_pq haf(B[V without p,q])

for every supported edge of every color. Hafnian expansion at a vertex then
forces its degree in each color to be one. Every receiving word consequently
supports at most one matching. The standard three-matching graph obstruction,
proved directly in the final section, supplies a mixed matching for every
even order greater than four, giving the contradiction.

This bypasses the former need to prove each higher balanced derivative
identity separately. No finite-order extrapolation or unproved source
deformation is a premise of the complete proof.

## Exact proof and independent reviews

The complete 336-line proof has SHA256
`fb0fa1e9447d8044981692d6e9bbbeff8e6a2cfc90119b6a296cbf506b9a3c9d`.
Its candidate-review header is retained as part of the frozen bytes; this
acceptance record supplies the subsequent review outcome.

- [Independent full-chain audit by routing_author](../computations/unaudited-codex-diagonal-continuation-2026-09-20/POINTWISE-ORTHOGONAL-COVARIANCE-CLOSURE-AND-FOUNDATION-CHAIN-INDEPENDENT-AUDIT.md):
  PASS, SHA256 `94e3808f717d14b9f755b1adad2eb5dde830e021fbcf7d2da03d483310c0d545`.
- [Independent full-chain audit by audit_det_bridge](../computations/unaudited-codex-diagonal-continuation-2026-09-20/FINITE-TWO-REPLICA-COVARIANCE-FORCES-HAFNIAN-ENDPOINT-IDENTITIES-PROVISIONAL-CLOSING-PROOF-UNFROZEN-AUDIT.md):
  PASS, SHA256 `416aa8094a5ca0513866f66eff8761eff2f87718abb5a231716738559a6e41f8`.
- [Detailed endpoint source](../computations/unaudited-codex-diagonal-continuation-2026-09-20/FINITE-TWO-REPLICA-COVARIANCE-FORCES-HAFNIAN-ENDPOINT-IDENTITIES-PROVISIONAL-CLOSING-PROOF.md):
  SHA256 `e5e9e1ba7a396e307ce176bfdd75c1c905e1fd33e5f6b75acd5bac18a542a230`.

Both auditors reconstructed every section, including the earlier foundations,
the terminal odd coefficient, the polynomial invariant ring, and the final
graph argument. One wording clarification was requested and applied:
differentiate the full kernel before restricting a parameter to zero.
Two later typography changes were checked and do not alter the mathematics.

## Reproducible supporting checks

Run from the repository root:

```sh
python3 computations/unaudited-codex-diagonal-continuation-2026-09-20/verify_finite_two_replica_endpoint_kernel.py
```

Root replay reproduced the [saved PASS output](../computations/unaudited-codex-diagonal-continuation-2026-09-20/finite_two_replica_endpoint_kernel_results.json):
nonzero scalar and matrix orthogonal-covariance examples on four and six
retained sites; 768 exact polynomial boundary checks across all ordered root
pairs of a weighted K4 source; and a genuine binary-only source that fails
the required terminal response and has a nonzero endpoint defect. The latter
checks that the necessary third-color premise has not been silently dropped.
These are normalization and scope checks; the all-orders proof is analytic.

All 1,248 baseline artifacts and 176 subsequently bound objects were checked
unchanged before integration. Only README.md and PROOF-SKETCH.md receive
current research-status updates; prior proof and audit bytes are preserved.
The [completion receipt](../computations/unaudited-codex-diagonal-continuation-2026-09-20/ROOT-RESEARCH-REVIEW-ALL-ORDERS-TWO-REPLICA-CLOSURE-2026-09-26.json)
records the final hashes and scope.
