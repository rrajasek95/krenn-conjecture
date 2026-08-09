# O4 second incidence frontier: iterated Laurent closure

The maximal plus-binomial character of the second 159-cell incidence face is
consistent, but it is not the end of the coefficient attack.  Reduce all
4,321 generators modulo that character, adjoin every exact two-class normal
form, and repeat.  The exact closure has the following rank profile:

| stage | Laurent rows | rank | newly adjoined rows |
|---:|---:|---:|---:|
| 0 | 54 | 20 | 33 |
| 1 | 87 | 28 | 1 |
| 2 | 88 | 29 | 4 |
| 3 | 92 | 33 | 2 |
| 4 | 94 | 35 | 0 |

At stage four, full-output record 412 reduces to

```text
-x06_00*x17_00*x23_10*x45_00*x56_21/x56_20.
```

Every variable in this Laurent monomial is localized, so the normal form is
a unit.  The checker verifies every exponent rewrite and every exact rational
character multiplication, reconstructs all lattice dependencies, and tracks
the induction from original coefficient generators through the derived
two-class relations.  Thus the localized coefficient ideal is empty over
characteristic zero.  The only non-integral character appearing in the chain
is `1/2`.

The dependency graph is minimized back to its original source records.  The
checker emits a support-faithful face clause: either one of the 34 omitted
cells is restored or one of the named source-monomial witnesses is removed.
It also emits all eight distinct transports under the eight automorphisms of
the O4 universe.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py
python3 -O computations/verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py
```
