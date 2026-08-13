# Conjugate hybrid interference repairs the last Cartan rank fork

## Result

The 270 double-coloop packets do not merely reach a generic active minor.
Using the shared-arm hybrid identity in both bright-colour orientations
forces either selected-arm reselection or a certified distinct-head active
four-good overlap.

Let the two selected bright matchings share

```text
P--p,  S--n.
```

On `S--n`, the first hybrid row uses the selected `22` cell and the other
three pure-1 cells.  Its avoiding mates carry a new external `S--u:21`
cell.  The conjugate row uses `11` on `S--n` and the other three pure-2
cells; its avoiding mates carry `S--v:12`.

Checker:
[`verify_h3_order6_double_coloop_conjugate_hall_interference.py`](../computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py).

## The two exact branches

Group either complete crossed row by whether its matching retains `S--n`.
If the corresponding complete pure cofactor is zero, the pure target row
forces an alternate pure matching omitting `S--n`.  After reselection, the
already proved selected-arm Cartan theorem lands the packet.

Suppose both complete pure cofactors are nonzero.  Then both avoiding
aggregates are nonzero, so each contains a nonzero literal matching term.
The normalized direct block forbids `PS` in a mixed word.  Every remaining
mate has an `S` arm absent from the unary and both bright anchors.  Thus the
two rows give nonempty active sets

```text
A21 = {u : S--u:21 has a nonzero complete cofactor},
A12 = {v : S--v:12 has a nonzero complete cofactor}.
```

This is exactly the common-effective-side branch of the strict Hall-star
source theorem, with centre `n` and effective endpoint `S`.

* If `u != v`, the two off-anchor pairs `S--u,S--v` have distinct heads and
  deleted-star ranks three.  They are the pinned transverse four-good wedge.
* If every possible choice has `u=v`, both sets are the same singleton.
  The same off-anchor block carries reciprocal `21/12` debts.  The direct
  unary block is `lambda E00`, so the pinned co-located unary-wedge theorem
  repairs the Hall-centre arm and again produces a distinct-head active
  four-good overlap.

No common complement tail between the chosen mates is being assumed.  The
Hall theorems use the two genuine complete crossed cofactors separately.

## Exact incidence audit

For every one of the 270 packets and for either conjugate row, there are 75
physical avoiding matchings.  They are evenly distributed over the five
off-centre internal sites:

```text
5 debt sites x 15 matchings per site = 75.
```

Auditing every ordered choice of one `21` mate and one `12` mate gives, per
packet,

```text
different debt sites:  4,500  -> transverse Hall wedge
same debt site:         1,125  -> co-located reciprocal closure
total:                  5,625.
```

Across all 270 packets the counts are `1,215,000` and `303,750`.

## Frontier shift

The double-coloop branch no longer reaches the generic same-head
`(2,2,3,3)` active-minor obstruction.  It either reselects to the already
active selected Cartan arm, or lands directly in a distinct-head active
four-good overlap.  The remaining downstream issue is shared with every
curved four-good packet: source-reduce that overlap to the proved sparse
full-nine unit (or obtain a support descent).  Uniform entry from an
arbitrary minimum counterexample and the inactive `Yw -> W` comparison also
remain separate.

Verification:

```text
python3 computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py
python3 -O computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py
python3 -I -S computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py
```

Frozen ledger SHA-256:

```text
7ecdc14a0466a42bea73ce69b41308b51b00ca856c09d12ca206fe9ae7532f9e
```
