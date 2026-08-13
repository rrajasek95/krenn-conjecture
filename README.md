# Krenn's graph-coloring conjecture

Research workspace for the task specified in
`/Users/rishi/krenn_conjecture_agent_prompt.md`.

## Layout

- `notes/` — route registry, exploratory lemmas, and adversarial findings
- `proofs/` — candidate proof drafts and independent audits
- `computations/` — exact symbolic or combinatorial experiments
- `references/` — ordinary mathematical background material

The required deliverable is either a complete proof of the stated formula for
all even orders or an exact finite counterexample, including every audit listed
in the task prompt.

The compact authoritative proof spine and task frontier are maintained in
[`notes/consolidated-proof-frontier.md`](notes/consolidated-proof-frontier.md).
The current three-interface proof frontier and shortest attack order are
summarized in
[`notes/2026-08-13-three-interface-proof-frontier.md`](notes/2026-08-13-three-interface-proof-frontier.md).
The earlier interference--Cartan map remains useful background, but predates
the separation between universal source-side homotopy and physical labelled
descent.
The longer
[`notes/proof-route-supersession-audit.md`](notes/proof-route-supersession-audit.md)
records why historical routes are closed, guarded, demoted, or still live.
Reusable background theorems and exact Mathlib coverage are catalogued in
[`notes/related-work-and-lean-artifacts.md`](notes/related-work-and-lean-artifacts.md),
and the current phase-one Lean ledger is
[`formal/FORMALIZATION.md`](formal/FORMALIZATION.md).
The chronological registry and older attack boards remain research logs, not
lists of independent current obligations.
