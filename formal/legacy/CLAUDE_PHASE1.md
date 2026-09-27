# Claude formalization task: phase 1

Work as a rigorous Lean 4 formalization agent.

The proof-search repository is /Users/rishi/workplace/krenn-conjecture.
The compile-only upstream checkout is
/Users/rishi/workplace/formal-conjectures. Its relevant source is
FormalConjectures/Paper/MonochromaticQuantumGraph.lean, pinned to the
checkout's current main. Read that whole Lean file before designing the
extension.

Read these mathematical sources from the proof-search repository:

- /Users/rishi/krenn_conjecture_agent_prompt.md
- notes/clean-pair-cap-exact-descent-target.md
- notes/uniform-selector-union-maximal-defect-shore.md
- notes/line-plus-plane-shore-clean-cap-pencil.md
- proofs/six-site-arbitrary-complex-obstruction.md

The conjecture is not solved. Do not formalize an unproved implication
as an axiom or theorem, and do not fill anything with sorry, admit,
axiom, or an unresolved placeholder.

Create and edit only files under
/Users/rishi/workplace/krenn-conjecture/formal/. Use the sibling Formal
Conjectures checkout only to import definitions and compile with commands
of the form:

    cd /Users/rishi/workplace/formal-conjectures
    lake env lean /Users/rishi/workplace/krenn-conjecture/formal/FILE.lean

Phase-1 deliverables:

1. formal/FORMALIZATION.md: a concise dependency map from the original
   decorated-source statement to the existing EqSystemN formulation,
   then to the audited cap/descent lemmas. Mark every item as formalized,
   ready to formalize, or still mathematically open. Include exact
   proposed Lean declarations and state clearly that the
   active-line-to-active-clean-point bridge is open.
2. formal/MonochromaticQuantumGraphKeyLemmas.lean: a compile-checked,
   no-sorry extension importing
   FormalConjectures.Paper.MonochromaticQuantumGraph. Prioritize:
   - the missing N = 2 witness for arbitrary finite D over a semiring,
     proving EqSystemN 2 D;
   - an elementary fixed-label lemma capturing the rank-one-flattening
     fact used in the two-site clean-pencil proof: an outer-product table
     that is diagonal can have at most one nonzero diagonal entry;
   - if feasible without scaffolding bloat, the finite-hyperplane
     avoidance lemma used to choose an active member of a two-dimensional
     pencil over C.
3. Compile the Lean file. Keep only declarations that compile. If the
   hyperplane lemma becomes expensive, leave its exact signature in the
   ledger rather than weakening or axiomatizing it.

Prefer small reusable declarations and theorem statements faithful to
the fixed endpoint labels. Avoid a large custom square-zero algebra in
this first phase; specify that as phase 2 in the ledger. Do not modify or
commit either git repository.

At the end, report exactly which files changed, the compile command and
result, and any mismatch you found between our graph model and the
upstream WeightsN model.
