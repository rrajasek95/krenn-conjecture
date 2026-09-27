# All-orders proof: reading and rebuilding

**Read the [cited research manuscript (PDF)](krenn-gu-all-orders-paper.pdf).**
This is the preferred reading version; GitHub's math preview can distort
numbered equations.

- [Manuscript LaTeX source](krenn-gu-all-orders-paper.tex)
- [Frozen written proof](krenn-gu-all-orders-two-replica-proof.md)
- [Internal review record](../notes/all-orders-two-replica-review-2026-09-26.md)
- [Initial Lean formalization and remaining work](../formal/all-orders/README.md)
- [Earlier eight-page presentation](krenn-gu-all-orders-two-replica.pdf)

The manuscript follows the exposition of Chandran, Gajjala and Illickan's
*Krenn–Gu Conjecture for Sparse Graphs*: graph definitions, related work, main
result and proof overview, followed by numbered lemmas and their proofs. It
adds a graph-to-algebra explanation and a named polynomial differential-equation
lemma to the complete argument. All ten numbered equations from the frozen
presentation are retained.

Twelve references identify the published graph model, Bogdanov's obstruction,
classical pairing and invariant-theory background, and the repository's own
foundational results. Citations to internal research notes and agent audits are
explicitly distinguished from published literature. External peer review and
a full Lean proof remain pending. The frozen mathematical source is unchanged.

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
