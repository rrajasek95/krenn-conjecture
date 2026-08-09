# O4 later 158-cell character-graph batch

This batch continues the exact maximum-support O4 CEGAR while testing the
quotient-character graph dichotomy.  Each face is reduced modulo its complete
integral plus-binomial lattice.  A coefficient-one one-class row is expanded
through its exact parent relations, denominators are cleared, and the result
is checked as an ordinary `U^k` identity in the original 4,321-generator
ideal.  Support clauses use only the cells appearing in that ordinary source
graph and are transported through the O4 stabilizer.

The first face in this batch has 12 one-class rows and 30 opposite-character
parallel pairs; record 3613 supplies an all-characteristic ordinary `U^1`
certificate.  It therefore does not yet disprove the proposed signed-graph
dichotomy.

The second face has 24 one-class rows and 24 opposite-character parallel
pairs.  Record 1575 expands to an all-characteristic ordinary `U^1`
certificate.  It also remains on the local-unit side of the dichotomy.

The third face in this batch has 12 one-class rows.  Record 2595 expands to
an all-characteristic ordinary `U^2` certificate, so the full SNF holonomy
test is not needed to close it.

The fourth face has 12 one-class rows; record 3613 again supplies an
all-characteristic ordinary `U^1`, with the source indices and clearing
identity independently recomputed on the new support.

The fifth face has 12 one-class rows.  Record 2304 expands to an
all-characteristic ordinary `U^1`; the full-SNF dependency test is again
unnecessary for closure.

For this fifth identity the checker also enumerates every perfect matching of
its seven full-output source words inside the 193-cell O4 universe.  The 29
possible repair masks have exactly nine inclusion-minimal masks, all
singletons.  Hence the identity survives arbitrary support additions outside
those nine cells.  Its emitted clause uses those nine visible cells rather
than all 35 omissions, making this a chart-wide repair-mask atom rather than
one more isolated face.

## Exact quotient-edge criterion over the complex torus

Let `L` be the integral exponent lattice of the plus binomials and retain its
exact multiplicative character `rho:L -> C*`.  A reduced two-class row adds an
integral displacement `e_j` and a required value `r_j`.  All such rows have a
simultaneous torus solution exactly when every integral dependency among the
old lattice rows and the `e_j` has character product one.  Necessity is
immediate.  For sufficiency, consistency defines a character on the subgroup
they generate; `C*` is divisible, so that character extends to the ambient
free exponent group.

This statement does not assume that `L` is primitive.  Torsion in the quotient
is harmless precisely because roots exist in `C*`; the implementation must
therefore retain the integral dependency lattice/SNF data and exact rational
characters, rather than reduce only modulo signs or over `Q`.  A dependency
with product `q != 1` expands to `(1-q)` times one Laurent monomial.  Each
reduction is traced to original generators, all negative exponents are cleared,
and multiplication by the complementary localized variables produces the
ordinary `U^k` identity.  The same clearing guard applies to a one-class row.

The criterion exactly decides the subsystem of rows with at most two quotient
classes.  Character-consistency alone is not a coefficient point when reduced
generators with three or more classes remain; those are the genuine next
mechanism if a support face escapes all one-/two-class units.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_158_character_graph_batch2.py
python3 -O computations/verify_n8_d1_residue_orbit4_158_character_graph_batch2.py
```
