# The crossed-label M return is killed by its private target row

## Result

The double-companion transfer can return to the selected pure-2 matching

```text
M = P0 | S1 | Q_M
```

and force the literal nonzero zero-row monomial

```text
P0:12 * S1:21 * Q_M^22.                         (1)
```

This branch is impossible.  The decisive coefficient is not the opposite
`p2s1` row and does not require a five-lock.  The cell `P0:12` together with
the three pure-2 factors of `M` gives the target-augmented private word

```text
22222212.                                        (2)
```

Its complete row forces a pure-2 reselection away from `P0`, an external
offdiagonal P arm, or a crossed response matching.  The first two enter the
certified nonanchor rank-`(3,3)` active-minor route (using `P0` after
reselection); the last enters the pinned crossed-response route.

Checker:
[`verify_h3_axis_target_coloop_crossed_m_private_site_closure.py`](../computations/verify_h3_axis_target_coloop_crossed_m_private_site_closure.py).

## Why the opposite row is not the argument

Freeze the exact selected carrier support from the `812` same-tail returns.
Over residual output word `212222`, the four response coefficients have
the literal matching-term profile

```text
             p1s1   p1s2   p2s1   p2s2
term count:    0       2      0       2
```

The two supported terms in each nonempty row are `M` and the same-tail
return matching.  Thus the full opposite `p2s1` coefficient is genuinely
empty on this support.  Exactness of the five rows does **not** manufacture
an opposite crossed cell, nor does one fine coefficient supply the full
column relation required for the five-lock or one-sided proportional-column
theorems.

The first additional source coefficient that is already forced is (2).
On the frozen support it has one old term in `392` states and two old terms
in `420` states.  The two-term states already contain a pure-2 matching
avoiding `P0` after replacing `P2:12` by the selected `P2:22` cell.

## Complete private-row proof

Let `H_P0^2` be the complete pure-2 cofactor after deleting `P,0`, and let
`O` be the sum of all terms of (2) whose physical matching avoids `P0`.
The literal mixed row is

```text
0 = P0:12 * H_P0^2 + O.                           (3)
```

If `O=0`, then `H_P0^2=0`.  The pure-2 target coefficient is one, so some
pure-2 matching avoids `P0`.  If `O!=0`, one literal avoiding monomial is
nonzero.  The exact `812*75` avoiding-matching census is

| route | slots |
|---|---:|
| external offdiagonal P arm | 48,720 |
| `P2` with an external S arm, pure-2 reselection | 7,308 |
| crossed ports `P2,S1` | 2,436 |
| internal ports `P2,S3` | 2,436 |

For both routes whose P port is `P2` and which are not crossed, every factor
except `P2:12` is already pure 2, while `P2:22` is selected by the
S-companion return.  Replacing that one cell therefore gives a nonzero
pure-2 matching avoiding `P0`.  If the P port itself is external, its
offdiagonal cell lies outside all three selected anchor matchings and enters
the nonanchor active-minor route directly.

The edge `P0` belongs to none of the other two pure anchors `K,L`.  After
the reselection it belongs to none of the three selected pure anchors.
Consequently its nonzero offdiagonal cell `P0:12` has rank three at both
deleted endpoint stars by the matching-coordinate lemma, and the
target-augmented private-site identity supplies the active minor.

## What happens to the earlier Hall/diagonal alternatives

The `606` Hall and `1,454` diagonal-q slots from the return-hybrid row split
by endpoint ports as follows:

```text
Hall:        P0,S1 = 238,   P2,S3 = 368,
diagonal q:  P0,S1 = 1386,  P2,S3 = 68.
```

Every `P0,S1` term contains `P0:12`, so the same private-row proof closes
all `1,624` of those slots.  Together with the `812` literal M slots this
removes `2,436` P0-bearing alternatives.

The remaining `436` `P2,S3` slots do not force `P0:12`.  They retain the
one-sided target-augmented active-minor/common-q return recurrence and are
not silently declared empty here.

## Specialization to the four diagonal common-q packets

The four packets isolated by the common-q minimax audit have, up to the
residual symmetry,

```text
M tail = K tail = 24|35,   B tail = 25|34,
L tail = C tail = 05|14.
```

After adding the same-tail S companion and the crossed M cell `P0:12`, all
four have the same literal response profile

```text
(p1s1,p1s2,p2s1,p2s2) = (0,2,0,2).
```

The opposite `p2s1` row is still empty.  The P-private row has exactly the
two matchings `M,C`; moreover, replacing its `C` factor `P2:12` by the
selected S-companion factor `P2:22` makes `C` a pure-2 matching.  Thus every
one of the four packets immediately reselects the pure-2 anchor away from
`P0`.

Consequently the crossed-M row does not supply the multiplicative relation
missing from the rank-two five-lock incidence.  It leaves that boundary by
target reselection.  A genuine diagonal survivor must avoid `P0:12` (or add
new response support before this specialization).

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_crossed_m_private_site_closure.py
python3 -O computations/verify_h3_axis_target_coloop_crossed_m_private_site_closure.py
python3 -I -S computations/verify_h3_axis_target_coloop_crossed_m_private_site_closure.py
```

Frozen ledger SHA-256:

```text
5f916eb3033b77a82328a1fd989d8f56fb77cbbb38c320d7489dc9212e0f85e7
```
