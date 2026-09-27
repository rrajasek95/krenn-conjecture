# Universal-rate feasibility gate

Read the [scope, proofs, and go/no-go assessment](../../notes/universal-rate-bound-feasibility-2026-09-26.md).
These are new research deductions, **not independently audited or certified**.

```sh
python3 computations/universal-rate-gate-2026-09-26/verify.py
python3 -O computations/universal-rate-gate-2026-09-26/verify.py
```

Python 3.10+, standard library only. The checks take well under a minute and
do not launch an optimizer, SAT solver, or symbolic elimination system.

The replay verifies two different finite certificates:

1. Every one of 3,375 triples of six-site pure matchings has an appropriate
   mixed matching. Exact rational averaging yields the nonnegative-source
   constant B²=41/1440, with 5,130 squarefree quotient monomials.
2. The sparse functional in [dual.json](dual.json) annihilates all 6,480
   mixed-generator monomial multiples in the target multidegree, but evaluates
   to -16 on the product of the three pure hafnians. This disproves one proposed
   cubic-product identity. It does not disprove a square-root rate inequality.

It also checks the exact Gaussian normalization factors, a negative-weight
cancellation guard, and the fixed prism-tangent obstruction. A corrupted
functional is deliberately rejected. [verification.json](verification.json)
records the output and the relevant source hashes.

The universal complex power-law existence argument uses the admitted case
exclusions and the Nullstellensatz; it is a written proof, not an output of
these finite enumerations. The nonnegative assumption is essential to the
explicit square-root bound. Physical probabilities additionally require the
specified ideal pure Gaussian source and exact photon-number selection model.

The optional generator uses a different reduction than the verifier:

```sh
python3 computations/universal-rate-gate-2026-09-26/build_dual.py
```

It prints the stored functional. The verifier instead enumerates every mixed
word and its allowed complement monomials directly, without trusting the
generator's graph reduction.
