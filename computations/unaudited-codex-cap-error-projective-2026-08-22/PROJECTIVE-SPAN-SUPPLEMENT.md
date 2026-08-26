# Projective coordinate-span supplement

Exact row reduction of the homogeneous cap-error coordinate polynomials over
their coefficient fields gives:

| control | degree | nonzero coordinates | coordinate span | active base locus |
|---|---:|---:|---:|---|
| `n4` GHZ, pair 01 | — | 0 | 0 | nonempty (`P^8`) |
| phased `n6`, pair 01 | 2 | 24 | 19 | empty (`g in I`) |
| W25, pair 04 | 3 | 4 | 3 | empty (`g^2 in I`) |
| W40, pair 67 | 3 | 4 | 2 | nonempty (contains `K=I`) |

Thus a small coordinate span does not force an active basepoint: W25 has
only three independent cubic sections, but all of its projective base locus
lies on the activity boundary.  The phased smooth isotropic local minimum is
the stronger basepoint-free-active-open countermap.  Chern/top-degree
arguments must include the activity divisor and therefore add no forcing
power without the GHZ mixed rows.

The ranks are obtained directly from `cap_polynomials` in
`audit_cap_error_projective.py`; no elimination or new Gröbner basis is used.
