# The h=3 axis-pure exact-source branch is empty

## Result

There is no larger inclusion-minimal no-singleton stratum beyond the six
support-27 packets already excluded by `b0e1551`.  An unrestricted global
Boolean census has exactly six `F0`-normalized minimum-support models.  All
six have support `27` and type

```text
pure q:00 matching F0 + bright K2,2 + bright K2,4.
```

After blocking those six cell supports, the formula is UNSAT.  The pinned
coefficient certificate excludes every one of the six.  Therefore

\[
                  \boxed{\text{the h=3 axis-pure branch is empty}.}
\]

No arbitrary-coloop normalization theorem is needed for this branch.

Checker:

```text
computations/verify_h3_axis_pure_global_min_support_census.py
```

Run it with the repository virtual environment, normally, optimized, and
isolated/no-site.  Under `-I -S` the checker adds only the repository-local
`.venv` site-packages path so it uses the identical two native solver
backends without enabling user site initialization.  Frozen ledger digest:

```text
89c67e45a7ba5e05cba4dfbef988957d14ffd996bc8b3a53739c9dff9692d3b9
```

## Global formula

The checker constructs the entire axis-pure presentation, not a bounded
continuation of the support-27 closure tree:

```text
69 coordinate variables,
3,645 matching-monomial variables,
849 output fibres,
21,345 CNF clauses.
```

Each monomial variable is equivalent to the conjunction of its coordinate
variables.  The clauses impose:

1. at least one live monomial in each of the three target fibres;
2. never exactly one live monomial in any of the `846` off-target fibres;
3. every occupied coordinate occurs in at least one live monomial;
4. the pure-zero target matching is normalized to `F0=01|23|45`.

Condition 3 is the exact minimum-support reduction.  If an occupied
coordinate occurs in no active matching term, deleting it changes neither a
coefficient nor a target value.  Hence no inclusion-minimal exact source can
violate it.

The canonical integer-clause payload has SHA-256
`691b28345d53eb60daadee66b805db6b2f396240cda8264102c80dc151cdd654`.

The formula contains no cardinality bound.  Models are enumerated by
blocking only their 69 coordinate variables; auxiliary monomial variables
are deterministic functions of those coordinates.  After six projected
blocks the unrestricted formula is UNSAT.

## Independent and direct checks

Both Glucose4 and CaDiCaL 1.9.5 enumerate the same canonical list of six
supports and return UNSAT after the sixth block.  Every solver model is also
rechecked directly against all `3,645` monomials and all `849` fibres before
it enters the frozen ledger.

The direct recheck verifies for every model:

- all three target fibres are occupied;
- no off-target fibre is a singleton;
- every selected coordinate is used;
- support size is exactly `27`;
- its graph and shore profile is `F0 + K2,2 + K2,4`.

Thus there are no minimum-support models of sizes `28` or above—not merely
none through a preselected search cutoff.

## From support census to exact-source emptiness

If any exact axis-pure source exists, the finite coordinate universe contains
one with minimum occupied support.  Every coordinate of such a source must
occur in a live matching monomial: otherwise setting that coordinate to zero
changes neither an equation nor the target and strictly lowers support.
Therefore its support satisfies the global Boolean formula.  The six formula
models are the only possibilities.

Commit `b0e1551` supplies two independent coefficient contradictions on
each such support: three K2,4 permanent equations force `2*unit=0`, and the
K2,2 target factor gives

\[
                 q_{01}f_{target}-E_1f_q=-q_{01}X_1\ne0.
\]

Therefore none of the six support shadows lifts to a coefficient point.
The axis-pure exact-source branch is empty.

## Scope

This is exact for canonical `h=3` axis-purified five-tensor equations over a
characteristic-zero field.  It does not address the unpurified source branch.

Expected output:

```text
axis-pure global minimum-support models: 6
model support sizes: [27, 27, 27, 27, 27, 27]
after six projected cell blocks: UNSAT (g4 + cadical195)
support-27 coefficient certificate excludes every model
h=3 axis-pure exact source branch: EMPTY
```
