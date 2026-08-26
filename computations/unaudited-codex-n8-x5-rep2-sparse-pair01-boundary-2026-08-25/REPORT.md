# Rep2 sparse full-pair01 boundary

## Exact outcome

On the exact 17-coordinate zero-pattern chart supplied by the rational
core43 countermodel, the complete 257-equation pair01 amplitude ideal is the
unit ideal over `Q`.  Allowing any one or any two of the remaining 70
amplitude coordinates still gives the unit ideal.  Therefore every
full-pair01 point extending this chart needs **at least three additional
coordinates**.

This is an exact sparse-support boundary theorem, not a rep2 closure.  The
guard, cap67 adjoint, carrier-incidence, and rank-nonzero equations were kept
out of every amplitude ideal.

## Exhaustive chart ledger

The amplitude parameterization has 87 coordinates: 81 retained source
entries and the six rank-one factors `u0..u2,v0..v2`.  The core43 rational
point has 17 nonzero coordinates, leaving 70 zero coordinates available for
relaxation.

The exact coverage is:

| Extra coordinates | Raw charts | Exact normalized groups | Q outcome |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 UNIT |
| 1 | 70 | 28 | 28 UNIT |
| 2 | 2,415 | 381 | 381 UNIT |

The rep2 source-labelled site automorphism group stabilizing the fixed,
variable, added, and rank-one substitution skeleton is trivial.  The
pair01 color swap `0<->1` also does not stabilize the 17-coordinate chart.
The reductions from 70 to 28 and 2,415 to 381 are instead exact polynomial
isomorphisms: programs are byte-identical after canonical renaming of the one
or two newly admitted variables and canonicalizing the ring declaration.

The independent audit regenerated all 2,485 raw single/double programs in a
temporary directory, recovered every sealed normalized hash, and reran all
410 representative Q ideals.  Every representative returned `UNIT_IDEAL`;
there were zero nonunit results, timeouts, or process failures.  The longest
two-coordinate run took under 0.07 seconds in the production census.

## Scope of the parent rational point

The 17-coordinate parent point remains a literal solution of the minimized
43-equation core, but it violates 13 other pair01 amplitudes.  It also fails
the rank-one guard already at

```text
(A06 v)_1 = a06_10 v0 = -1/2,
```

and fails the cap45-inactivity incidence because its only `A04` entry is
`a04_01=1`, hence `Row(A04)=span(e1)` does not contain `e0`.  Thus neither the
parent point nor any point from this package satisfies the complete
guard/adjoint/incidence system; in fact, no full-pair01 point exists on any
of the enumerated charts.

## Diagnostics beyond the sealed theorem

Before the explicit hold on broader triple work arrived, 388 triples that
co-occur in a newly activated amplitude monomial were tested; all were unit.
This is not exhaustive over `C(70,3)=54,740` triples and is not used in the
lower-bound theorem.  A characteristic-three support-cap-3 search and an
unrestricted amplitude search both stopped at their 60-second diagnostic
wall.  They have zero characteristic-zero coverage.

## Remaining obligation

The exact minimum is at least three, but no rational full-pair01 point has
been found.  Any continuation should begin with an explicitly authorized,
exhaustive or certificate-producing treatment of three-coordinate charts;
the guard, adjoint, and carrier equations must remain a later, separately
audited filter.

Parent tensor/core43 manifest:
`16d459603ae0107e0da21ded47b67de62dd289c128667b67bad83bdd36deae1b`.
