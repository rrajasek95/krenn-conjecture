# All-orders proof: reading and rebuilding

**Read the [cited research manuscript (PDF)](krenn-gu-all-orders-paper.pdf).**
This is the preferred reading version; GitHub's math preview can distort
numbered equations.

- [Manuscript LaTeX source](krenn-gu-all-orders-paper.tex)
- [Frozen written proof](krenn-gu-all-orders-two-replica-proof.md)
- [Presentation reviews, scores and revision responses](reviews/2026-09-26/README.md)
- [Earlier mathematical review record](../notes/all-orders-two-replica-review-2026-09-26.md)
- [Complete Lean formalization](../formal/all-orders/README.md)
- [Exact upstream theorem and real-weight corollaries](../formal/upstream-adapter/README.md)
- [Earlier eight-page presentation](krenn-gu-all-orders-two-replica.pdf)

The opening explains cancellation through a worked graph example, states the
conjecture, and exhibits the four-vertex exception. The proof overview shows
why the supported-edge identity forces one incident edge of each colour at
every vertex, and why this makes the final combinatorial obstruction apply.
The algebraic introduction teaches matching polynomials, formal pairings, and
the symmetry of two copies through small examples before the technical proofs.

The current manuscript incorporates two rounds of internal simulated referee
review from quantum optics, algebra/mathematical physics, and graph theory.
The reviewers consulted primary literature and visually inspected the figures.
The [review record](reviews/2026-09-26/README.md) preserves their reports,
actual scores, frozen reviewed versions, concrete recommendations and responses.
These are internal presentation reviews, not external journal acceptance.

The 22-page paper defines rows, colour words, formal pairings, copies, shifts,
responses and derivative conventions before using them. It separates the site
quotient from the ordinary polynomial ring used by the Wick functional. Three
figures explain cancellation, copy symmetry and the final graph obstruction.
The results are explicitly labeled: three theorems, eight lemmas and three
corollaries, alongside a named definition. The main text explains the matrix
argument; Appendix A supplies its coordinate proof. Appendix B gives the exact
formal statement and reproduction commands. All ten numbered equations from
the frozen presentation are retained, and the frozen mathematical source is
unchanged.

Sixteen references distinguish published graph and physics results, the
classical pairing and scalar invariant-theory tools, public formal artifacts,
recent announcements and the repository's internal provenance. In particular,
the paper credits the established aggregation and normalization reductions and
the Bogdanov endgame, while explaining what the matching equations add to the
matrix argument. Unavailable forthcoming manuscripts are not treated as read
or used as proof inputs.

The full normalized equation-system theorem is formalized for every even
`N ≥ 6` and every `D ≥ 3`, using the exact upstream definitions. The PDF
states that checked scope and separately explains graph aggregation and the
normalization of arbitrary nonzero pure amplitudes. It links to the complete
proof and real-weight corollaries at a fixed repository revision. External
peer review remains distinct from formal verification and internal audits.

To rebuild, install Python 3 and Tectonic. On a fresh machine, populate the TeX
cache once:

```sh
tectonic --outdir proofs proofs/krenn-gu-all-orders-paper.tex
```

Then regenerate the cited PDF from its LaTeX source:

```sh
python3 -B proofs/build_krenn_gu_paper.py
```

The script uses Tectonic's offline cache, checks all bibliography keys and
absolute PDF links, rejects citation, cross-reference and layout warnings, and
verifies the frozen source's SHA-256 before and after the build. It prints the
resulting artifact hashes. PDF bytes can vary between TeX versions; the source
hash check protects the audited input, not PDF byte identity.
