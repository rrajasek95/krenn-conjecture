# Fixed-base residual hitting design for four-coordinate repair

## Outcome

There are no four-coordinate supports capable of repairing all 13 missing
pair01 amplitudes while the sealed 17 nonzero coordinates remain fixed at
their exact rational values.  In fact, the exact residual-monomial
hypergraph has minimum hitting size seven; it has six minimum supports.

Accordingly, the requested symmetry-normalized four-support count is zero,
with zero projected Q runtime and storage.  No Singular ideal was launched.

## Exact necessary condition

For each of the 13 violated words, the source-faithful 13-matching amplitude
was expanded over `Q` and the 17 base coordinates were substituted literally.
The resulting polynomial has a nonzero constant equal to the sealed residual.
Every remaining monomial is labelled by the subset of the 70 zero coordinates
that it requires.

If a candidate support `S` admits none of those monomial supports for some
residual, setting all coordinates outside `S` to zero leaves that equation's
nonzero constant unchanged.  Therefore a literal fixed-base repair must, for
each residual, contain at least one complete activation-monomial support.
This is the exact hitting condition used here.

The exhaustive counts are:

```text
support size 0: 0 hits
support size 1: 0 hits
support size 2: 0 hits
support size 3: 0 hits
support size 4: 0 hits
```

An exact union/transversal closure after all 13 residual families leaves 259
inclusion-minimal supports.  Their minimum size is seven, attained by six
supports.  Each of the six is stored in the JSON ledger with source labels.

## Load-bearing scope restriction

This hitting condition is necessary only for a **literal repair of the fixed
rational point**.  It is not necessary for an arbitrary point on a
`base17 + S` coordinate chart, because the 17 formerly nonzero coordinates
may move and cancel residuals differently.  Thus the zero four-support count
does not replace an exhaustive treatment of `C(70,4)` charts and does not
raise the already sealed global sparse-chart lower bound beyond four.

The exact established claims remain:

- arbitrary-chart full-pair01 points require at least four extra coordinates;
- fixed-base coefficient repair requires at least seven;
- guard, adjoint, incidence, and rank equations are not part of either
  amplitude-only statement.

Triple-boundary parent manifest:
`fb5f9d9bb179bccff0daad0e2bb6dc551280eed388a7db93dedf07683a6cff7e`.
