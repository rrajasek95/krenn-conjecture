# N=8 D1: one-site target incidence

Fix a site `v` and a pure output colour `a`.  Expanding the eight-site
hafnian by the partner of `v` gives

```text
sum_(u != v) p_(u,a)(site u) tensor C_u = e_a^tensor7.
```

Here `p_(u,a)` is the colour vector on edge `uv` after fixing colour `a` at
`v`.  If `p_(u,a)=0`, its route is absent.  For every other route, quotient
the colour space at site `u` by the line spanned by `p_(u,a)`.  Every term on
the left dies.  The pure target on the right survives unless at least one
nonzero incident vector is itself on the target line `<e_a>`.

Therefore, for every `(v,a)`, at least one incident column is active and
target-only.  In support language its target cell is live and all of its
off-target cells are absent.  This is characteristic-free after passage to
the fraction field of the localized coefficient domain.

The exact checker

```text
computations/verify_n8_d1_one_site_target_incidence.py
```

audits the `7*15=105` matching recursion at every site, exhausts all eight
support masks of an incident ternary vector for every target colour, and
emits the 24 target-incidence DNF packets specialized to the O4 universe.
The paired-routing O4 frontier is the `(v,a)=(7,0/1)` instance: after its
holes, only the fully supported/non-target columns on edges `17,37` remain,
so no target-only incidence exists.

Frozen ledger SHA-256:
`091f1fb4305131bea5b5dc0c73cf27c5af5efe3d196b8e60a007ae75eee897ec`.
