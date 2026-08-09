# N=8 D1: exact closure of the eight-cell support frontier

The checker
`computations/verify_n8_d1_m8_support_shadow_closure.py` proves that a D1
packet cannot have exactly eight nonzero aggregate cells outside Sigma.  It
uses only finite support combinatorics and unit propagation; no SAT solver or
numerical ideal computation is trusted by the certificate.

For either monochrome colour there are 22 possible off-Sigma cells.  An
exhaustive subset census gives 72 minimal three-cell anchors and 27 minimal
four-cell anchors.  Every valid five-cell support contains one of those
smaller anchors, so there is no new size-five normal form.  Therefore every
eight-cell support occurs in one of the distributions `3+3+2`, `3+4+1`,
`4+3+1`, or `4+4`.  Choosing a genuinely live monochrome matching also
freezes its Sigma anchor factors.  The D1 group reduces these branches to
132, 64, 64, and 52 anchor-unit orbits, respectively: 312 total.

There are 989,832 raw addition choices over those orbit representatives.
For every currently unique mixed fibre, any added cells must complete the
off-Sigma part of an alternative matching.  Intersecting these exact repair
requirements leaves 9,891 choices.  Reapplying the direct unique-fibre test
after the additions kills 9,651 of them (3,399 residue, 3,749 six-site, and
2,503 full-fibre certificates).  The remaining 240 branch candidates project
to 165 support orbits.

Each residual support is then fixed exactly.  Matching conjunctions are
rebuilt from the committed E1 domain, monochrome target fibres are required
to be nonempty, and every target-zero fibre is required to have zero or at
least two live matchings.  The 78 full-fibre words already frozen by the
`m=7` closure unit-refute 123 supports.  For the other 42, deterministic unit
propagation on the complete 8,100-fibre Boolean shadow derives a conflict.
Thus all 165 residual supports are impossible, independently of coefficient
values.

Together with commits `f5c43d3` and `48f4bc0`, this proves that the remaining
D1 locus must have at least nine nonzero off-Sigma aggregate cells.  The
`m >= 9` strata remain open.

Frozen ledger SHA-256:
`78204953d39924fe3bc46d405a577613e7901e022a29e91150ca4d5dd767ee19`.

Run:

```text
python3 computations/verify_n8_d1_m8_support_shadow_closure.py
python3 -O computations/verify_n8_d1_m8_support_shadow_closure.py
```
