# Krenn–Gu conjecture

**Read the paper:** [PDF with references](proofs/krenn-gu-all-orders-paper.pdf) · [LaTeX source](proofs/krenn-gu-all-orders-paper.tex) · [Reading and build guide](proofs/PRESENTATION.md).
**Initial Lean formalization:** [checked lemmas and remaining work](formal/all-orders/README.md) · [DeepMind draft PR #6627](https://github.com/google-deepmind/formal-conjectures/pull/6627).

Proofs, reproducible certificates, and independent audits for the Krenn–Gu
conjecture in the general complex-weighted graph model.

The question is whether interference can cancel every mixed-color output while
preserving three or more pure-color outputs. The conjecture says this is
impossible for an even number of sites greater than four.

**Research status (September 26, 2026):** a [complete all-orders proof](proofs/krenn-gu-all-orders-two-replica-proof.md)
has passed two independent internal analytic audits. The [review record](notes/all-orders-two-replica-review-2026-09-26.md)
gives its exact scope, proof hashes, and reproducible checks. External peer
review and a complete Lean formalization have not been performed.

[Learn](#learn) · [Results](#results) · [Verify](#verify) · [Repository guide](#repository-guide)

## Learn

- **[Complete proof explainer](explainers/ALL-ORDERS-PROOF.md)** — an undergraduate
  walkthrough of the all-orders argument, with seven diagrams explaining the
  endpoint identity, the graph contradiction, and the four-site exception.
- **[Undergraduate explainer](explainers/EXPLAINER.md)** — the conjecture, prior work,
  and what this workspace has established, with diagrams.
- **[Six-site proof walkthrough](explainers/SIX-SITE-PROOF.md)** — the structural inputs
  and the steps leading to the six-site contradiction.
- **[Useful consequences](explainers/USEFUL-CONSEQUENCES.md)** — new deductions on
  architecture exclusions and fidelity–success tradeoffs, with an interactive calculator.
- **[Rates near perfect fidelity](explainers/GENERAL-RATE-BOUND.md)** — an explicit
  bound for arbitrary complex endpoint colors, with a stronger bound for diagonal
  sources; new written research with exact checks, awaiting independent audit.
- **[Interactive matching examples](explainers/EXPLAINER-LAB.html)** — explore matching
  contributions and cancellation; download and open the HTML file in a browser.

The complete proof explainer describes the September 26 all-orders closure;
the main and six-site explainers preserve the September 25 research snapshot.
The useful-consequences follow-up and certification update are dated September 26.
Browser editions of the [complete proof guide](explainers/ALL-ORDERS-PROOF.html),
[main explainer](explainers/EXPLAINER.html) and [six-site walkthrough](explainers/SIX-SITE-PROOF.html)
are also available to download and open locally.

## Results

Previously admitted certification package, **September 26, 2026**:

| Result | Scope | Proof |
|---|---|---|
| Global diagonal reduction | Every original edge block is diagonal for even `n >= 4`; actual hafnian cofactors give scaled matrix inverses. | [Statement and dependencies](certification/stronger-results-2026-09-26/THEOREMS.md#gd-global-diagonal-reduction) |
| Color-degree restrictions | For `n = 2m >= 6`, each color degree is between `1` and `m - 2`; degree two is impossible and leaves form isolated edges. | [Degree theorem](certification/stronger-results-2026-09-26/THEOREMS.md#degree-restrictions) |
| Six-site impossibility | General complex endpoint-color matrices. | [Previously certified proof](proofs/six-site-arbitrary-complex-obstruction.md) |
| Eight- and ten-site impossibility | General complex endpoint-color matrices. | [Certified proof package](certification/stronger-results-2026-09-26/THEOREMS.md) |

These statements concern actual complex ternary sources with three nonzero
pure amplitudes and all mixed outputs zero. The finite-order exclusions extend
by projection to three or more target colors. The new
[all-orders research proof and audits](notes/all-orders-two-replica-review-2026-09-26.md)
cover every even `n > 4`; the four-site example remains allowed. The table
above and its frozen verification package retain their prior admitted scope.

**Quantitative follow-up, awaiting audit:** a new
[written rate theorem](notes/general-complex-rate-bound-2026-09-26.md) gives exponent
\(8/[n(3n+14)]\) for arbitrary complex sources and any target dimension at least
three. Diagonal sources have the stronger exponent \(4/(3n+2)\). The
[replay package](computations/general-complex-rate-2026-09-26/README.md) supports
the identities and constants; the sharp global rate remains open.

[Repository certification](certification/BASELINE.md#certification-meaning)
means exact written proofs and an independent research-agent audit, with exact
computational certificates where used. A complete Lean formalization is still
pending. The [admission record](certification/SUPERSESSIONS.md#supersession-2026-09-26-01)
and [independent audit](certification/audits/SUPERSESSION-2026-09-26-01.md)
define the accepted scope.

## Verify

Requires **Python 3.10+**, with no additional packages. From the repository root:

```sh
python3 certification/stronger-results-2026-09-26/verify.py
```

A successful run prints a JSON report with `"status": "PASS"`. It checks the
frozen artifact hashes, all **1,884** eight-site matching cases, and exact
identity and scope controls. The all-order conclusions also rely on the written
proofs and their audits.

See the [verification guide](docs/verification.md) for optimized and isolated
replay, the auditor's separate checker, and expected outputs. The
[portable ZIP](certification/archives/stronger-results-2026-09-26.zip)
([SHA-256](certification/archives/stronger-results-2026-09-26.zip.sha256))
contains everything needed to replay the certified package offline.

## Repository guide

| Location | Contents |
|---|---|
| [explainers/](explainers/) | Illustrated guides, interactive examples, and their diagram assets. |
| [certification/](certification/) | Admitted results, frozen proof packages, audits, and replay receipts. |
| [proofs/](proofs/) | Established case proofs and their supporting certificates. |
| [notes/](notes/) | Mathematical arguments, open routes, and the evolving research frontier. |
| [computations/](computations/) | Exact checkers, experiments, and exploratory computations. |
| [formal/](formal/) | Lean formalization work and its status records. |
| [docs/](docs/) | Verification, research timeline, and archived context. |
| [references/](references/) | Background literature and source material. |

Exploratory material has its own evidence status; only explicitly admitted
claims belong to the certified results. The [earlier certified proof frontier](notes/consolidated-proof-frontier.md)
records the preceding program; the [all-orders review](notes/all-orders-two-replica-review-2026-09-26.md)
records the current research conclusion. The [archived research overview](docs/research-history.md)
preserves the detailed descent program, earlier certificates, and historical
related-work notes. The [research timeline](docs/research-timeline.md) traces
the key insights, elapsed intervals, and unresolved proof hurdles.

## Cite

Cite this repository with the relevant theorem and certification record. For
the September package, use
[SUPERSESSION-2026-09-26-01](certification/SUPERSESSIONS.md#supersession-2026-09-26-01),
which pins the audited proof commit and exact scope. The
[stable references](docs/verification.md#stable-references) provide the commit
identifiers and artifact manifests.
