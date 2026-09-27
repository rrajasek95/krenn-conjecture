# Research subprojects

Follow-up questions and reusable methods arising from the Krenn–Gu proof.
The [main README](../README.md) is the entry point for the completed,
Lean-verified exact theorem.

| Project | Main question | Current frontier |
| --- | --- | --- |
| [GHZ fidelity and rate](ghz-rates/README.md) | How quickly must production rate vanish as GHZ fidelity approaches one? | An unrestricted six-site exponent of $1/15$, local square-root laws, and reductions of the remaining singular cases. The unrestricted square-root law is open. |
| [Optimal W-state design](w-state-design/README.md) | What is the best exact W-state rate at every even site count? | A universal factor-two guarantee, all-even local optimality, and exact optima for broad support and core classes. The exact unrestricted optimum is open. |
| [Response identities and reconstruction](response-methods/README.md) | Which proof tools help with design, stability, and source recovery? | Exact optimization certificates, balancing and response identities, and separate source-reconstruction results. |

## How to read the evidence

The rate and design results are **written proofs with exact supporting
checks; independent audit is pending**. They have not been added to the
Lean-verified theorem. Finite checks establish their stated identities,
certificates, and examples; the general claims also depend on the written
arguments. Numerical searches are labelled separately.

Each project page links to its accessible guides, precise statements, and
replay packages. The [explainer collection](../explainers/README.md) includes
diagrams and offline browser editions at undergraduate mathematics level.

## Reproduce the follow-up checks

From the repository root, with Python 3.11 or later:

~~~sh
python3 research/verify.py
~~~

This runs the 36 rate, design, and shared-method packages in normal and
optimized Python, compares their JSON outputs with the saved receipts, and
checks their recorded repository-file hashes. It uses the standard library
and does not run the optional numerical searches or rebuild the Lean proof.
Source-reconstruction checks have their own entry points on the
[methods page](response-methods/README.md).

Package directories retain their dated names so that proof sources,
dependencies, and receipts stay together. These project pages provide stable
links as the research develops.
