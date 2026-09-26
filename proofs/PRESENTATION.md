# All-orders proof: reading and rebuilding

- [GitHub Markdown with LaTeX mathematics](krenn-gu-all-orders-two-replica-latex.md)
- [Eight-page PDF](krenn-gu-all-orders-two-replica.pdf)
- [LaTeX source](krenn-gu-all-orders-two-replica.tex)
- [Frozen written proof](krenn-gu-all-orders-two-replica-proof.md)
- [Internal review record](../notes/all-orders-two-replica-review-2026-09-26.md)
- [Initial Lean formalization and remaining work](../formal/all-orders/README.md)

The presentation includes all seven sections and eight named core statements:
the complex weighted no-go theorem, the whole binary response lemma, the
even-omission lemma, global diagonal reduction, the supported endpoint identity,
the polynomial orthogonal-kernel normal form, matching rigidity, and the
three-matching obstruction. External peer review and a full Lean proof remain
pending.

The original audited Markdown is unchanged. The presentation has been checked
against that source, and all eight PDF pages have been visually inspected.

To rebuild, install Python 3 and Tectonic. On a fresh machine, populate the TeX
cache once:

```sh
tectonic --outdir proofs proofs/krenn-gu-all-orders-two-replica.tex
```

Then regenerate both GitHub math Markdown and the PDF from the LaTeX source:

```sh
python3 -B proofs/build_krenn_gu_presentation.py
```

The script uses Tectonic's offline cache, checks for reference and layout
warnings, and verifies the frozen source's SHA-256 before and after the build.
It prints the resulting artifact hashes. PDF bytes can vary between TeX
versions; the source hash check protects the audited input, not PDF byte identity.
