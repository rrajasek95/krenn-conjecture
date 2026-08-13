# The E14 landing obstruction is one companion term, then target normal

## Result

In the canonical word-`000101` unary-times-`q` first-hit module, the pinned
22-support cokernel functional does **not** see the already identified
decorated rootless core. Its complete pairing with the twelve-term target is
concentrated on one different monomial:

```text
(p1_0_1 s1_1_1) u05_01 v13_01 v24_11.
```

The target coefficient is `-1`, the rational-dual coefficient is `+1`, and
their product is the full target pairing `-1`. By contrast, the promoted
decorated-core term

```text
(p1_0_1 s1_1_1) u05_01 v24_11 v34_10
```

has target coefficient `+1` but dual coefficient zero. Thus matching the
decorated `2K2` factor is genuinely orthogonal to the first landing
obstruction.

Verified by
[`verify_h3_e14_companion_target_normal_specialization_gate.py`](../computations/verify_h3_e14_companion_target_normal_specialization_gate.py).

## 1. Exact concentration

The old first-hit block has 269 complete unary/`G11` columns of rank 269,
and the twelve-term target raises that rank. Back substitution gives the
known rational functional of support 22. Among all twelve target monomials,
only the displayed `u05*v13*v24` companion contributes to its pairing.

The distinction is physical, not just a change of coefficient basis. Using
external endpoint sites `6,7`, the visible companion has site profile

```text
(2,2,1,1,1,1,1,1),
```

whereas the promoted decorated core has profile

```text
(2,1,1,1,2,1,1,1).
```

The missing comparison must therefore move the repeated residual incidence
from the internal decorated-core site to the endpoint-root site while also
changing the word decoration. A monomial-level `2K2` identification cannot
do this.

## 2. Silent chords do not erase the obstruction

It is tempting to use the fact that the visible companion contains the
missing chord `v13`. Exact specialization rules this out.

Setting the entire `q13` table to zero changes the old rank from 269 to 211
and removes the visible coefficient coordinate, but the specialized target
still has nine nonzero terms outside the old image. After echelon reduction,
all nine surviving coordinates lie in the pure unary-target-normal summand.

Setting both missing chord tables `q04=q13=0` changes the rank to 185 and
leaves eight such target-normal coordinates. Hence the obstruction does not
vanish on the strict silent-C6 branch. It migrates from the occurrence
coefficient to the target readout.

This also explains why the unit return factors in the first S-pair theorem
do not by themselves construct the desired target-zero chain. They control
the coefficient-side self-loop, but using the complete pure rows incurs the
displayed target-normal debt.

## 3. Shortest next theorem

The first physical datum is now sharper than an unspecified word arrow. One
needs a source-valid endpoint-word-change/relative-`P2` cell whose complete
boundary simultaneously carries

1. the occurrence coefficient joining the retained carrier to the E14
   unary remainder; and
2. the target-normal unary face exposed by silent-chord specialization.

This is precisely the target-bearing even Cartan/Spencer cone shape already
seen in the `B-4`/`C_+` comparison. The present theorem does not identify the
two cells physically; it proves that an occurrence-only or decorated-core
landing cannot suffice.

If the complete endpoint-word-change columns fill these target-normal
coordinates, the E14 landing proceeds. If not, their extended cokernel
functional is the first candidate for the physical generator/Fredholm arm.

## Scope

The statement is exact for the selected canonical E14 first-hit block and
for literal zero specialization of the full `q04,q13` coefficient tables.
The surviving target-normal coordinates have not yet been extended through
all anchor, physical-`q`, ridge, eta and sigma rows, so they are not claimed
to be terminal separators.
