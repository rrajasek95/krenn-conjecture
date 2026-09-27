# Krenn–Gu conjecture

Lean formalization and written proof of the complex weighted equation-system
conjecture: for every even `N ≥ 6` and every `D ≥ 3`, no assignment of complex
edge weights has matching amplitude `1` on every monochromatic vertex colouring
and `0` on every other colouring.

**Status:** the full complex theorem and its real-weight corollaries are
Lean-verified, with no proof holes or additional axioms. The proof uses only
`propext`, `Classical.choice`, and `Quot.sound`.
[Formal Conjectures PR #6627](https://github.com/google-deepmind/formal-conjectures/pull/6627)
records the proof links and is awaiting maintainer review.

[Paper PDF](proofs/krenn-gu-all-orders-paper.pdf) ·
[Complex theorem](formal/upstream-adapter/FullProof.lean#L29) ·
[Real corollaries](formal/upstream-adapter/RealCorollaries.lean#L63) ·
[Proof-module guide](formal/all-orders/README.md)

## Run the Lean formalization

Install Git, **Python 3.11 or later**, and
[elan](https://github.com/leanprover/elan#installation), which provides `lean`
and `lake`. The project pins Lean **4.33.1** and its mathlib revision.
The verification scripts use only Python's standard library; the research
dependencies in `pyproject.toml` are optional for this build.

Clone the repository and verify the local proof:

```sh
git clone https://github.com/rrajasek95/krenn-conjecture.git
cd krenn-conjecture
(cd formal/all-orders && lake exe cache get)
python3 formal/all-orders/verify.py
```

Expected final line:

```text
PASS: 55 integrated modules; 919 declarations axiom-checked.
```

To check the full theorem and real corollaries against the **exact upstream
definitions**, continue from the repository root:

```sh
git clone https://github.com/rrajasek95/formal-conjectures.git ../krenn-upstream
git -C ../krenn-upstream checkout e2c4441f9545b85790aebcfaa445e194fcab9d5b
(cd ../krenn-upstream && lake exe cache get)
python3 formal/upstream-adapter/verify.py --upstream ../krenn-upstream
```

Expected final line:

```text
PASS: exact upstream all-orders theorem; 21 declarations axiom-checked.
```

Both verifiers build with warnings treated as errors and reject nonstandard
axiom dependencies. The declaration counts include definitions with proof
fields. Source hashes and complete axiom reports are stored with the
[local proof](formal/all-orders/verification.json) and
[upstream verification](formal/upstream-adapter/verification.json).
The upstream checkout must remain at the pinned revision for this replay.

## Read the proof

- [Cited paper](proofs/krenn-gu-all-orders-paper.pdf) and
  [LaTeX source](proofs/krenn-gu-all-orders-paper.tex).
- [Written all-orders argument](proofs/krenn-gu-all-orders-two-replica-proof.md).
- [Lean proof chain](formal/all-orders/README.md), from matching coefficients
  through diagonalisation and endpoint identities to the graph contradiction.
- [Exact upstream statements and reproduction details](formal/upstream-adapter/README.md).
- [Statement-fidelity audit](formal/all-orders/EXACT-UPSTREAM-STATEMENT-AND-CLOSURE-AUDIT-2026-09-26.md).
- [Illustrated undergraduate guides](explainers/README.md), including the complete proof walkthrough.

## Timeline

Milestones are listed newest first. Written-proof audits and Lean verification
are identified separately; dates follow the repository's Pacific-time records.

- [2026-09-26] Verified real-to-complex transfer and five exact real corollaries; added their proof links to PR #6627.
- [2026-09-26] Completed the full complex Lean theorem for every even `N ≥ 6` and `D ≥ 3`; submitted the fixed proof link for upstream review.
- [2026-09-26] Published the cited all-orders paper and its LaTeX source.
- [2026-09-26] Recorded the complete written two-replica proof and its internal analytic audits.
- [2026-09-26] Froze the audited package for global diagonal reduction and the general eight- and ten-site results.
- [2026-08-26] Archived the research program and computational results through August.
- [2026-08-19] Recorded the audited written obstruction for diagonal eight-site sources.
- [2026-08-14] Recorded the audited conditional clean-pair descent theorem.

[Historical records and source commits](docs/history/README.md) preserve the
earlier proof frontier and the scope of each milestone.

## Repository guide

| Location | Contents |
| --- | --- |
| [formal/](formal/README.md) | Completed Lean proof, upstream adapter, and separately labelled legacy projects. |
| [proofs/](proofs/) | Paper, LaTeX sources, written proofs, and presentation build scripts. |
| [explainers/](explainers/README.md) | Illustrated undergraduate guides to the proof and its consequences. |
| [research/](research/README.md) | Follow-up subprojects, current frontiers, and a shared replay command. |
| [certification/](certification/) | Frozen historical proof packages, audits, and exact replay records. |
| [docs/history/](docs/history/README.md) | Archived overview, proof sketch, and milestone references. |
| [notes/](notes/) | Research notes and intermediate arguments, with their original evidence status. |
| [computations/](computations/) | Research scripts and experiments; older root-level outputs are in [archive/](computations/archive/README.md). |
| [references/](references/) | Background literature. |

For a reproducible citation, link the relevant Lean declaration at the fixed
proof commit: [complex result](https://github.com/rrajasek95/krenn-conjecture/blob/7f78a17ecedd245bd1c17b0dce3f6a9ea2afd66f/formal/upstream-adapter/FullProof.lean#L29)
or [real result](https://github.com/rrajasek95/krenn-conjecture/blob/5e7d0fe0b6058f4658ccc5dae5f148ea8e7bc248/formal/upstream-adapter/RealCorollaries.lean#L63).

## Research subprojects

Follow-up work has its own proofs, explainers, and reproducible checks.
The rate and design results are written research with exact supporting checks;
independent audit is pending. The unrestricted targets below remain open.

| Subproject | Results so far and next question |
| --- | --- |
| [GHZ fidelity and rate](research/ghz-rates/README.md) | Explicit rate bounds, local square-root laws, and stronger control of singular limits; pursuing the unrestricted square-root law. |
| [Optimal W-state design](research/w-state-design/README.md) | A universal factor-two guarantee, all-even local optimality, and exact optima for broad classes; pursuing the exact global optimum. |
| [Response identities and reconstruction](research/response-methods/README.md) | Reusable optimization certificates, source balancing, stability estimates, and source-reconstruction methods. |

[Research overview and replay instructions](research/README.md) ·
[Illustrated guides](explainers/README.md)
