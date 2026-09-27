# Site balancing and the sharp four-site response bound

**Written proofs with exact supporting checks; independent audit pending.**

[Normalization proof](../../notes/site-balancing-rate-reduction-2026-09-26.md) ·
[Norm identity and sharp bound](../../notes/balanced-four-site-response-bound-2026-09-26.md) ·
[Illustrated undergraduate guide](../../explainers/SITE-BALANCING.md)

Every nonzero-output source can be pruned and positively scaled at its sites
to preserve the entire output, reduce source strength, and equalize the total
incident strength at every site. Universal normalized-rate upper bounds may
therefore be proved on balanced sources. This applies to GHZ and W targets
at every even site count.

At six sites, balanced sources satisfy the sharp bound
`sum ||four-site tensor||² >= S²/15`. At least one column of the full
six-site derivative has norm at least `S/15`. A real symmetric conference
matrix attains equality. This excludes complete derivative collapse from the
balanced boundary search; partial rank loss and the unrestricted square-root
law remain open. It does not prove the global unrestricted W optimum.

Python 3.10+, standard library only, from the repository root:

```sh
python3 computations/site-balancing-2026-09-26/verify.py > /tmp/site-balancing.json
diff -u computations/site-balancing-2026-09-26/results.json /tmp/site-balancing.json
python3 -O computations/site-balancing-2026-09-26/verify.py > /tmp/site-balancing-optimized.json
diff -u /tmp/site-balancing.json /tmp/site-balancing-optimized.json
```

The replay checks:

- Exact output preservation and rate improvement for a distorted prism and
  a source with an edge in no supported perfect matching.
- The four-site norm identity on six complex, colored, real, balanced, and
  unbalanced examples, including equality and a negative control.
- An independent expansion of 4,995 commuting monomials for a dense complex
  source, including the factorial norm and both site-collision formulas.
- All 32,768 six-site support graphs against the fractional matching cover
  classification: only ten triangle pairs have fractional but no ordinary
  perfect matchings.
- Rejection of site factors whose product is not one. Every acceptance check
  remains active under Python's `-O` option.

The finite computations support the general analytic proofs; they do not
replace them. `core.py` also provides an exact checker for user-supplied
positive rational balancing factors. It verifies balance and hence the
hypotheses for orbit minimality. It does not find factors for arbitrary input
or claim a global optimum over different source architectures.

`dependencies.json` pins imported arithmetic, fixtures, and their imports.
`results.json` records those pins and hashes of this package and both proofs.
