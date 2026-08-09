# N=8 D1: first frontier from only the six mandatory cells

Restarting the exploratory arbitrary-support CEGAR from only the six
canonical D1 cells, rather than the `77`-cell branch-63 support, produces a
new semantic frontier.  The smallest first representative has `109`
localized cells, of which `29` lie in the residue K4.  It passes the complete
`8,100`-fibre support shadow.

Independent reconstruction gives `1,889` distinct coefficient generators,
no monomial generator, `376` binomials, and `375` plus-binomials.  The
checker freezes the exact support and the digest of every generator.  It
does not trust the exploratory CEGAR clauses.

The first `50` semantic escapes sampled after exact-model blocking fell into
only two residue-support orbits: `26` on this `29`-cell pattern and `24` on a
`30`-cell one-cell extension.  Their total support sizes ranged from `109`
to `123`.  This is an exploratory census, not a completeness theorem.

After promoting the checked injective-tripod theorem as a concrete
required-cell/absent-cell witness clause, this entire first family
disappears.  Promoting the pure-lift theorem through all three boundary
perfect matchings leaves a particularly simple next structural case.  In a
sample of `50` semantic models, every residue support is the same orbit:
five residue blocks are full, while the sixth is full except for two
same-diagonal non-target holes, which can be written

```text
F00=F11=0.                                             (1)
```

The sampled total support sizes range from `205` to `211`; the residue has
`52/54` cells.  Pattern (1) has no blocked row, no center with three
support-forced injective projections (the two full-row supports can still
have coefficient rank one), and dense competing full matchings defeat every
pure lift.  It is the smallest uncovered structural case in this audit.
The existing exact dense two-hole atoms treat a target-row pair and an
opposite off-diagonal pair, not the same-diagonal pair (1).

The checker also records, at each residue vertex, the support-forced rank
range and kernel-line incidence of the three projections of the two
non-target tripod rows.  “Rank” here means what is forced solely by the two
row zero patterns; coefficient relations may further lower a `[1,2]`
entry.  At vertices `5` and `6`, all three projections have distinct nonzero
row supports and are therefore forced rank two.  The independently checked
injective two-kernel tripod theorem applies at either vertex and closes this
frontier over every field.  Thus this first support is a stable regression
target, but not a new surviving coefficient component.

Finally, it tests the checked pure-residue lift against all `80` mixed
boundary words for each of the three boundary perfect matchings
`{01,23}`, `{02,13}`, and `{03,12}`.  Any surviving exact lift would close
the support immediately; the printed census states whether one remains
after permuting the boundary pairing.

The exact checker
[`verify_n8_d1_six_mandatory_first_frontier.py`](../computations/verify_n8_d1_six_mandatory_first_frontier.py)
reconstructs all of these data from the frozen support.
