# O4 downsets: the boundary-star double quotient

Suppose that, for one non-target colour `a=0` or `1` at residue site 6,
every admissible edge from a boundary site to site 6 is absent.  The O4 edge
`67` is target-supported too.  In the full eight-site coefficient slice with
site-6 colour `a`, site 6 can therefore be paired only with site 4 or site 5.

The exact O4 residue family has

```text
B46[:,a]=alpha_a*c,       D56[:,a]=-alpha_a*e.
```

Partitioning the 105 perfect matchings by the partner of site 6 gives the
seven-site tensor equation

```text
alpha_a*(c(site4) tensor P - e(site5) tensor Q) = e_a^tensor7.
```

Quotient the site-4 factor by `<c>` and the site-5 factor by `<e>`.  Both
left-hand routes die.  The pure right-hand side survives as soon as `c` and
`e` each have one localized coordinate away from the line `<e_a>`.  This is
a division-free contradiction over every field.

The checker

```text
computations/verify_n8_d1_residue_orbit4_boundary_star_quotient.py
```

audits both non-target colours, all `2,187` seven-site words, and the exact
matching partition (`15+15` surviving and `75` killed matchings per word).
It emits eight support-faithful clauses, each with the ten positive
boundary-star escape literals and two negative quotient witnesses.

Frozen ledger SHA-256:
`8e5e56eecbfd0d3ebf88a71f9598308fd16c437e0bb07662e8126f37fe84e6c9`.
