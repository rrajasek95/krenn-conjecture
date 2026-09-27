# Explainers

Illustrated introductions to the Krenn–Gu conjecture, written at undergraduate
math level. Start with the **all-orders proof guide** for the complete argument
that passed two internal audits on September 26, 2026. The main and six-site
guides preserve the September 25 research snapshot; the consequences and rate
guides describe separate follow-up questions.
The [project README](../README.md) describes the completed Lean verification
of the exact theorem. Quantitative follow-ups have their own evidence status. The
[research subprojects](../research/README.md) organize them by question and
provide a shared replay command.

| Guide | Read on GitHub | Browser edition |
|---|---|---|
| The complete proof, from cancellation to the all-size contradiction | [All-orders proof guide](ALL-ORDERS-PROOF.md) | [Seven diagrams and offline equations](ALL-ORDERS-PROOF.html) |
| A universal W-design guarantee, response rigidity, and a competing scalar minimum | [Global W guarantee](W-GLOBAL-GUARANTEE.md) | — |
| Unrestricted local W optimality at every even size, including the four-site exception | [All-even local W optimality](W-LOCAL-OPTIMALITY.md) | — |
| Flat supports, triangle projections, and GHZ onset with three arms or two invertible arms | [Critical-direction geometry](CRITICAL-DIRECTION-GEOMETRY.md) | — |
| All-even W optimality and a strict six-site gap with cancelling ground matchings | [W ground cancellation](W-GROUND-CANCELLATION.md) | — |
| Classification of triangle rank loss and unrestricted W response bounds | [The balanced frontier](BALANCED-FRONTIER.md) | — |
| Global source balancing and a sharp response bound for both research paths | [Site balancing](SITE-BALANCING.md) | — |
| Regular GHZ limits, exact cancellation identities, and two-root W optimality | [Boundary structure on both research paths](BOUNDARY-STRUCTURE.md) | — |
| Optimal W-state designs, robust response certificates, and sharp-rate proof tools | [Utility of the methods](METHOD-UTILITY.md) | — |
| Certified design optimization, prism optimality, and a singular boundary | [Latest design and rate results](RATE-DESIGN-FRONTIER.md) | — |
| Sharper rates, smaller constants, and a paired-hafnian application | [Rate follow-ups](RATE-FOLLOWUPS.md) | — |
| An explicit rate bound for arbitrary complex endpoint colors | [Full-model rate bound](GENERAL-RATE-BOUND.md) | — |
| An explicit rate bound for all diagonal complex sources | [Quantitative follow-up](QUANTITATIVE-PROOF.md) | — |
| The conjecture, prior work, and workspace findings | [Main explainer](EXPLAINER.md) | [Illustrated HTML](EXPLAINER.html) |
| The six-site impossibility proof | [Proof walkthrough](SIX-SITE-PROOF.md) | [Illustrated HTML](SIX-SITE-PROOF.html) |
| Architecture exclusions and fidelity–success tradeoffs | [Useful consequences](USEFUL-CONSEQUENCES.md) | [Illustrations and calculator](USEFUL-CONSEQUENCES.html) |
| Which zero-output limits could threaten the rate bound? | [Boundary exclusions](RATE-BOUNDARIES.md) | — |
| Perfect matchings and cancellation | — | [Interactive examples](EXPLAINER-LAB.html) |

Download the browser editions and open them locally. Their diagrams, equations,
and interactive examples work without a network connection. Keep this folder
together to retain navigation between guides and links to full-size diagrams.
Proof-source links refer to the surrounding repository.

## Assets and builders

- `all-orders-assets/` contains seven SVG diagrams and the standard-library
  builder for the complete proof guide. Its Markdown is the prose source;
  the browser edition embeds the diagrams and native MathML equations.
  Rebuild with `python3 explainers/all-orders-assets/build.py`.
- `explainer-assets/` contains the main guide's eight SVG diagrams and builder.
- `six-site-assets/` contains the six-site guide's five SVG diagrams and builder.
- `useful-consequences-assets/` contains two SVG diagrams and the standard-library
  builder for the offline interactive follow-up. Rebuild with
  `python3 explainers/useful-consequences-assets/build.py`.
- `rate-boundary-assets/` contains the vector diagram of the two excluded limits.
- `rate-followup-assets/` contains the phase-cone diagram for the latest rate guide.

To rebuild the main diagrams and embed them into the existing reading editions,
run from the repository root using Python's standard library:

```sh
python3 explainers/explainer-assets/build_diagrams.py
```

The six-site builder also regenerates its HTML from Markdown. It requires Node.js
and an existing copy of the `marked` parser:

```sh
python3 explainers/six-site-assets/build_explainer.py --marked /path/to/marked.esm.js
```

The builders locate the reading editions relative to their own files. Reading
the checked-in HTML or SVGs requires neither builder nor build dependencies.
