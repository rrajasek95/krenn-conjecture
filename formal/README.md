# Lean formalization

The completed proof uses Lean 4.33.1. Start with the
[repository build instructions](../README.md#run-the-lean-formalization).

| Project | Status and purpose |
| --- | --- |
| [all-orders/](all-orders/README.md) | Complete local complex ternary proof: 55 modules and 919 axiom-checked declarations. |
| [upstream-adapter/](upstream-adapter/README.md) | Exact upstream theorem for every even `N ≥ 6`, `D ≥ 3`, plus real-weight corollaries; 21 axiom-checked declarations. |
| [legacy/](legacy/README.md) | Archived phase-one lemmas and planning documents, preserved at their original scope. |
| [n8-diagonal/](n8-diagonal/) | Earlier independent eight-site formalization project; outside the completed all-orders build. |

`all-orders` and `upstream-adapter` contain the current verification scripts,
source hashes, and axiom reports. The phase-one ledger and standalone Lean
file retain compatibility symlinks at their former paths for historical
references. The completed proof does not depend on those legacy files.
