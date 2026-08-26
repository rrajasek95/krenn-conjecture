# Orbit-85 Tail2 is nonzero but does not force an active carrier

Status: **UNAUDITED exact reduced-circuit theorem and source-faithful
counterguard**.

## Verdict

The stored orbit-85 arithmetic DAG has a genuinely nonzero quadratic tail
coefficient.  Exact reverse-mode evaluation at a canonical orbit-85 Boolean
selector point reduces the entire degree-398 proof circuit to one literal
`4+4` amplitude leaf:

```text
CNF/source row 12979
partition masks (135,120,0)
word            F_00011110
Tail2 value     19146
root weight     1
C2              19146.
```

Thus the order-two interface is not merely a possible degree: `C2` is not
the zero polynomial.

However, the parallel-colour quadratic packet alone does **not** force a
clean carrier.  An explicit pure-normalized integer source on the exact
orbit-85 diagonal support branch has this nonzero `C2` and all 728 response
carrier matrices of rank nine.  Hence every blocker belongs to every carrier
row space and there are zero active star or triangle carriers.

This source is deliberately not X5.  It is a counterguard to the implication

```text
orbit85 branch support + nonzero Tail2  => active carrier,
```

not to a future theorem that also uses all 6,558 full mixed equations.

## Exact orbit-85 diagonal control

Number the 28 site edges lexicographically.  The three diagonal colour graph
masks are

```text
G0 = 0x0a800c0 = {07,12,35,37,46}
G1 = 0x8885002 = {02,17,24,35,46,67}
G2 = 0x0aa1001 = {01,17,27,35,37,46}.
```

All displayed diagonal cells have coefficient one.  Exact Hafnian support
enumeration gives

```text
F0 = {0,3,4,5}
F1 = {1,3,4,5,6}
F2 = {2,3,4,5,6},
```

so after deleting the mandatory sites `0,1,2`, the branch case is literally

```text
((3,4,5),(3,4,5,6),(3,4,5,6)),
```

the orbit-85 representative.  For every colour, the pure eight-site
Hafnian, selected `7c` star, and complementary six-site cofactor are all
exactly one.  Thus the control is pure-normalized and satisfies every open
condition used by the branch.

The free-set calculation is coefficient-level, not a support heuristic:
inside-free residual products vanish and every outside-free position has a
literal nonzero residual product, so its complement witness can be chosen.

## Bounded exact reduction of C2

Set each `p` selector to the actual zero/nonzero value of its diagonal
Hafnian and each `g` selector to the product of its two defining `p`
selectors.  Reverse automatic differentiation through the 2,159-node
resolution/weakening DAG gives the only tail-sensitive leaf weights

```text
A2 : 12979 -> 1

C0 : 13429 -> 2, 13430 -> 2, 13431 -> 2, 13738 -> 1

XF : 13562 -> 1, 13565 -> 2, 13566 -> 1.
```

Every reached `C0` compiler has star selector zero, so its tail multiplier
`p_x u_x` vanishes.  Every reached `XF` compiler has zero clause-falsity
factor `a(1-b)` or `(1-a)b`.  The 448 `FR` branch equations remain
epsilon-constant, as in the source packet.  Consequently the sole quadratic
contribution is row 12979.

For this row the two live diagonal Hafnians and their inverses equal one.
Direct enumeration of the 72 two-cross-edge matchings of profile `4+4`
under the tail below gives

```text
Tail2_00011110 = 19146.
```

This proves exact nonvanishing without expanding the full certificate
polynomial.

## All-carrier counterguard

For every off-diagonal endpoint-colour cell, with `i<j` and `a!=b`, set

```text
T_ij^(ab)
 = 1 + ((17i + 31j + 43a + 59b + 7ab + 11ij) mod 97).
```

Let `A=D+T` using the diagonal graphs above.  The audit rebuilds the literal
response formula

```text
A_pa[i,alpha] A_qb[j,beta]
 + A_pb[i,beta] A_qa[j,alpha]
```

for all carriers.  The exact result is

```text
168 star matrices       rank 9
560 triangle matrices   rank 9
total                    728.
```

For every matrix, modular elimination at `p=1000003` selects nine literal
source rows, after which a Bareiss calculation proves the corresponding
integer `9 x 9` determinant nonzero.  The prime is therefore only a pivot
selector; the rank theorem is characteristic zero.  All 728 row labels,
pivot indices, integer determinants, and residues are frozen in the result
file.  Their canonical ledger digest is

```text
955dd973f2331c547ab13b08d6f7c64b59d62e33cb2c99c99d3b95061fd31032.
```

Rank nine makes every carrier row space all of `Q^9`.  Hence `K00`, `K11`,
`K22`, and `<K,A_pq>` all belong to it, and no star or triangle carrier is
active.

## Scope guard and consequence

The full source is intentionally far from X5: all 6,558 mixed amplitudes are
nonzero, with counts

```text
off-count 1:48, 2:336, 3:1344, 4:3150, 5:1680.
```

Therefore the valid conclusion is narrow but decisive for routing: neither
nonzero `C2` nor the complete parallel `Tail2` packet has an intrinsic
clean-cap incidence implication.  Any successful orbit-85-to-cap theorem
must use additional full mixed equations, eliminate the selector/inverse
variables, or extract a different higher-order relation.  Carrier incidence
cannot be read off from this quadratic coefficient alone.

The 448 `FR` equations were not silently promoted to full X5 rows.  They
remain fixed diagonal constructible-branch equations throughout.

## Replay

```bash
python3 computations/unaudited-codex-n8-orbit85-tail2-carrier-counterguard-2026-08-23/audit_orbit85_tail2_carrier_counterguard.py --check-results
python3 -O computations/unaudited-codex-n8-orbit85-tail2-carrier-counterguard-2026-08-23/audit_orbit85_tail2_carrier_counterguard.py --check-results
python3 -I -S computations/unaudited-codex-n8-orbit85-tail2-carrier-counterguard-2026-08-23/audit_orbit85_tail2_carrier_counterguard.py --check-results
```

The hostile `--mutate-tail` mode changes the reduced coefficient from
`19146` to `19198` and is rejected.

Frozen logical digest:
`00e8e347b3d034cb93c078bffba5b0580a972bf9835975c4a0440695360f27a8`.
