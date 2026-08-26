# Downstream audit of the provisional holonomy closure

Status: **UNAUDITED exact structural audit; the holonomy target is not a
finishing theorem.**  Even granting the proposed `closure22 + profile71`
membership, two source-level bridges remain before an all-triangle-blocked
source is contradicted.

## 1. What the provisional theorem would literally give

Let `M` be the fixed pure matching cone used by the joint-semigroup target
and let

```text
H = det [[u00,v00,w00],
         [u10,v10,w10],
         [u20,v20,w20]].                              (1)
```

The provisional ideal membership says `M H in I_X5`.  At an exact `X5`
point it therefore gives

```text
M(A) H(A)=0.                                           (2)
```

Only on the chart `M(A)!=0` may one conclude `H(A)=0`.  Pure normalization
says that the sum of the 105 pure matching monomials is one; it does not make
this particular `M` nonzero.  A global use of (2) consequently needs the 105
pure-matching chart cover, or an orbit-complete version with a cone known to
be live.

On such a chart, `H=0` has one exact meaning: the three selected six-site
cofactor triples in (1) are linearly dependent.  The frozen comparison uses
the global outside slices

```text
11222, 00000, 11111
```

inside the `6561 x 27` internal-triangle-cell map.  This is not yet the
carrier-aligned matrix used by the blocker Cramer construction.

## 2. The carrier-alignment gap

For a fixed pure residual colour `c`, the blocker attachment uses an `8 x 3`
matrix `C_c`: its eight rows are the mixed cap endpoint colours and its three
columns are the internal triangle-edge coefficients.  Its rank-at-most-two
boundary is

```text
all C(8,3)=56 maximal minors of C_c vanish.             (3)
```

Across three colours this is 168 minors.  The determinant (1) is one global
three-slice determinant; its outside words do not lie in a single pure
residual-colour cap block.  Hence the audited implication stops at

```text
H=0  => one selected cofactor triple is dependent,
```

not

```text
H=0  => rank(C_c)<=2.                                  (4)
```

A transported family of coned memberships may eventually prove (4), but
that orbit/localizer alignment is an additional theorem.  It is not supplied
merely by adding the `7+1` word orbit to the Macaulay packet.

## 3. Even carrier rank at most two is not a contradiction

Grant (4) as a second provisional step.  For the canonical triangle `T` and
cap `67`, the no-cap carrier has the `108 x 9` response matrix `L_T`.  All
triangle carriers blocked means that one of

```text
K00, K11, K22, <K,A_67> lies in rowspan(L_T).           (5)
```

On the simultaneous cyclic five-set rank-nine open, the three omitted
triangle-edge response maps are absorbed into `rowspan(L_T)`.  If the three
six-site pure cofactors `P_0 P_1 P_2` are also nonzero, the pure quotient
identity gives

```text
[Kcc] = P_c [<K,A_67>] mod rowspan(L_T),                (6)
```

so the four branches (5) collapse to the single direct membership.  Neither
(3) nor (6) makes that membership impossible.  In particular, if
`rank(L_T)=9`, its row span is all of `Mat_3^*`, and every blocker is blocked
vacuously.

The checker freezes an exact rational linear-algebra counterguard:

```text
rank(C_c)=2, all 56 maximal minors zero,
rank(L_T)=9,
all nine cyclic/colour quotient maps have rank 9,
all four blocker forms lie in rowspan(L_T).
```

This guard is deliberately not a literal source or an `X5` point.  Its role
is precise: rank and incidence algebra alone cannot finish the proof; the
missing theorem must use the literal `X5` source coupling.  The existing
source controls reinforce the warning: W40 and W25 have zero nonzero mixed
cap minors in all three colours, although neither is a full `X5` point.

## 4. Smallest theorem still needed on the generic boundary

Write `Delta_(t,c)` for one selected nonzero `9 x 9` minor of each of the
nine cyclic five-set quotient maps, and put

```text
Omega = P_0 P_1 P_2 product_(t,c) Delta_(t,c).          (7)
```

After choosing the canonical live cell `A_06[0,1]!=0`, the smallest exact
open-boundary statement is:

> **Rank-two carrier escape lemma.**  On normalized full `X5`, if
> `Omega!=0` and `rank(C_c)<=2`, then the direct blocker is not in
> `rowspan(L_T)` for the selected triangle (equivalently, the triangle is
> active), or the branch is empty.

Under the hypothesis that all 560 triangles are blocked, this lemma would be
an immediate contradiction on the open.  By (6), only one membership branch
must be tested rather than four.

There is already a fully source-labelled bounded system for the test.  Start
from the canonical incidence manifest:

```text
252 source variables + 108 row-span witnesses + 1 live inverse = 361,
6558 mixed + 3 pure + 9 membership + 1 live equation = 6571.
```

Adjoin the 56 minors (3), one inverse for (7), and its inverse equation:

```text
variables                                               362
equations                                              6628.    (8)
```

Imposing rank at most two in all three colours instead gives 6,740
equations.  The exact algebraic target is the saturated unit statement

```text
1 in <I_X5, direct membership, I_3(C_c)> : Omega^infinity.       (9)
```

This is the smallest current source-faithful boundary gate.  A sensible
bounded attack is coefficient-first: eliminate the 27 internal triangle
cells using the frozen observation map, absorb the `36+18` response sectors
using membership and the nine quotient minors, and test the remaining six
direct-`A_67` terms.  No full 362-variable Gröbner run is warranted before
that reduction.

## 5. What remains after the open theorem

Even a proof of (9) would not finish the conjecture.  The complement
`Omega=0` consists of:

1. a vanishing six-site pure cofactor `P_c`; or
2. a rank drop of one of the nine five-set quotient maps.

The existing artifacts only screen these boundaries.  They do not prove the
needed source-labelled implication to the old good-pair `E1/E2` descent.
The complete remaining theorem is therefore:

> Every normalized `X5`, live-cell, all-triangle-blocked point on
> `rank(C_c)<=2` either violates (5) on the open, or a divisor of `Omega`
> forces an `E1/E2` good-pair descent (or another active clean cap).

Until both the carrier-alignment implication (4) and this open/boundary
escape theorem are proved, the coned holonomy membership cannot finish the
eight-site conjecture.  It is a valid reduction into a determinantal
boundary, not the contradiction itself.

## Replay

[`audit_holonomy_boundary_spine.py`](audit_holonomy_boundary_spine.py)
checks the pinned row/variable counts, the 56/168 minor counts, and the exact
linear-algebra counterguard.

```sh
python3 computations/unaudited-codex-holonomy-boundary-spine-audit-2026-08-23/audit_holonomy_boundary_spine.py --check-results
python3 -O computations/unaudited-codex-holonomy-boundary-spine-audit-2026-08-23/audit_holonomy_boundary_spine.py --check-results
python3 -I -S computations/unaudited-codex-holonomy-boundary-spine-audit-2026-08-23/audit_holonomy_boundary_spine.py --check-results
```

Logical SHA-256:
`4e81b9bcc837343e08095b4fd6ce1739de62ec412e154dc46c35ff1a66a25325`.
