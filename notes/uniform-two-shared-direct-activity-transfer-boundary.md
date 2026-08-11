# The direct third-colour label needs a common transfer class

## Exact positive theorem

The terminal cell `q_e^{mm}` from `07a1f02` becomes proof-completing once
the successive cancellation terms retain one literal complement matching
class.  After factoring that common nonzero tail, the transfer equations
have the signless incidence matrix of a path or cycle.

* An open path has full column rank and exposes an unmatched endpoint.  In
  the source packet that endpoint is the required active cofactor,
  reselection, or off-anchor exit.
* An odd cycle has determinant `2`; over characteristic zero its localized
  rows give an ordinary unit.
* An even cycle has the one-dimensional alternating kernel
  `(1,-1,...,1,-1)`.  Moving along this kernel preserves every transfer
  row and can zero a chosen nonzero coordinate, giving the anchor-safe
  support descent.

This is the exact signed-even-cycle/partial-character alternative requested
at the next interface.  The checker verifies the path and cycle matrices
through length twelve.

Checker:
`computations/verify_uniform_two_shared_direct_activity_transfer_boundary.py`.

## Why shared labels are not a shared matching class

The common-tail hypothesis is not automatic.  There is a uniform literal
common-`q` guard at every even order `n>=6`.

Let

```text
P0 = 01 | 23 | 45 | ...,
```

let `P1` be a second perfect matching sharing exactly `e=01` with `P0`, and
choose `P2` avoiding `e` and the displayed edges.  Put the three normalized
coordinate cells of colours `0,1,2` on `P0,P1,P2`.  Add the terminal direct
cell

```text
q01_22 = 1,
```

but no pure-two perfect matching on the complement of `01`.  Hence

```text
C01^2 = 0.                                             (1)
```

The word

```text
c = 2200...0
```

has the through matching consisting of `q01_22` and the `P0` tail.  Add the
opposite perfect matching of the Hamilton cycle

```text
01,12,23,34,...,(n-1)0
```

with the endpoint labels prescribed by `c` and product `-1`.  The complete
fibre of `c` is exactly these two matchings, so its coefficient vanishes.
Their symmetric difference is the whole Hamilton cycle: the mate has no
common local complement tail with the through term.

At the same time, each constant fibre is still the singleton `Pi` of weight
one.  Thus the data

```text
three normalized pure targets,
q01_22 != 0,
C01^2 = 0,
one complete mixed transfer row = 0
```

do **not** imply activity or a local path/cycle matrix.  Matching-class
incidence, not endpoint labels, is the load-bearing datum.

The construction is the two-shared/direct-label counterpart of the pinned
global winding countermodel `f127fd7`.  Existence of `P1,P2` at all larger
orders follows by choosing perfect matchings in the dense complement; the
checker chooses them exactly and audits orders through twelve.

## First omitted full row

At six sites the guard is completely literal.  It has eight mixed output
debts.  In lexicographic order the first is

```text
word 001111: coefficient +1,
matching 01 | 24 | 35.
```

This is a singleton fibre.  A genuine full source must add a cancellation
mate for this row, and that mate is the first datum capable of identifying
a new transfer class or exposing an endpoint.  The previously exact word
`220000` and the pure normalizations cannot supply it.

Therefore the theorem-level boundary is sharp:

```text
common complement class
    -> active/open endpoint, odd unit, or even deletion kernel;
unequal winding class
    -> consume the next complete coefficient, first 001111 at six sites.
```

## Scope

The winding construction is a physical common-`q` **partial-row guard**,
not a full GHZ source and not a counterexample to Theorem 1.  It refutes the
shortcut from a direct label and pure normalizations to cofactor activity,
and identifies exactly why the remaining full rows are load-bearing.  No
support/cardinality layer is used.

Run

```text
python3 computations/verify_uniform_two_shared_direct_activity_transfer_boundary.py
python3 -O computations/verify_uniform_two_shared_direct_activity_transfer_boundary.py
python3 -I -S computations/verify_uniform_two_shared_direct_activity_transfer_boundary.py
```

Frozen ledger SHA-256:

```text
6ffef57d02ee591a4fe948236ad50d50f6d1157132c55e5d67b675f10b31ad42
```
