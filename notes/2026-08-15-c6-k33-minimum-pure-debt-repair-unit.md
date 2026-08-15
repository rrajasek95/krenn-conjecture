# Every minimum repair of the first `K3,3` pure debt creates a source unit

## Result

The first repair layer above the `15`-cell `K3,3` exit guard closes exactly.

There are `66` pure-witness completions with the minimum ten mixed
singletons; all have `23` cells.  Choose the lexicographically canonical
one.  Mating all ten old singleton rows requires at least seven additional
endpoint-coloured cells.  There are exactly twelve minimum seven-cell
packets.  Every one creates the new private mixed coefficient

```text
word   000011
fine   01|23|45
cells  01;00, 23;00, 45;11.                              (1)
```

The target of `000011` is zero and all three displayed cells are nonzero,
so (1) is a literal source unit.  No coefficient solving, clean-cap test, or
presentation projection is needed.

The exact checker is
`computations/verify_c6_k33_minimum_pure_debt_repair_unit.py`.

## 1. Canonical minimum pure completion

Starting from the guard in `64e98dc`, the three pure witnesses are

```text
colour 0: 01|24|35,
colour 1: 03|12|45,
colour 2: 01|25|34.                                      (2)
```

Their union with the guard has 23 decorated cells and ten singleton debts:

```text
000001  01|24|35
000201  01|24|35
001221  01|25|34
002222  01|25|34
112102  03|14|25
112122  03|14|25
220000  01|24|35
220001  01|24|35
220201  01|24|35
221221  01|25|34.                                       (3)
```

The checker independently enumerates all `15^3` witness triples before
selecting (2).  Exactly `66` have the minimum count ten, their supports are
pairwise distinct, and each has 23 cells.

## 2. Exact minimum-union problem

For a singleton word `w` with old fine `M_w`, and an alternative matching
`M`, let

\[
 C(w,M)=\{uv;w_uw_v:uv\in M\}\setminus S_0,             \tag{4}
\]

where `S0` is the canonical support.  Strict supersets among the candidate
sets for one row may be discarded.  A packet `P` mates all old rows exactly
when

\[
       \forall w\text{ in (3)},\quad
       \exists M\ne M_w:\ C(w,M)\subseteq P.             \tag{5}
\]

The depth-limited exact solve gives

```text
budget       1  2  3  4  5  6   7
solutions    0  0  0  0  0  0  12.                      (6)
```

This is a cardinality certificate: every child is the union with one
minimal candidate set, and all viable unions at each budget are exhausted.

All twelve minimum packets contain the four cells

```text
13;11, 23;00, 23;02, 45;00.                              (7)
```

Their numbers of new mixed singleton rows are

```text
23:2, 24:2, 25:2, 26:1, 27:2, 28:2, 30:1.               (8)
```

Thus every packet repairs all ten old rows but creates at least 23 new
singleton rows.

## 3. Universal new unit

The canonical pure completion already contains `01;00` and `45;11`.
Equation (7) shows that every minimum repair must add `23;00`.  Consequently
the fine `01|23|45` occurs in word `000011`.

Complete replay of all fifteen matchings shows that no other matching of
that word is supported in any of the twelve packets.  Its coefficient row
is therefore

\[
              a_{01}^{00}a_{23}^{00}a_{45}^{11}=0.       \tag{9}
\]

After localization at occupied cells, the left side is a unit.  This closes
the cardinality-minimum simultaneous-repair branch by the strongest terminal
alternative.

## Scope

The theorem covers the lexicographically canonical member of the 66
minimum pure completions and every cardinality-minimum packet mating all ten
of its old singleton rows.  It does not yet classify:

* the other 65 minimum pure completions up to the physical word-section
  stabilizer;
* nonminimum packets with eight or more new cells; or
* recursive mates added specifically to cancel the new row (9).

The next uniform step is to use the forced cell `23;00` as a potential:
either its mate completes a private permanent triangle, restores an active
clean cap, or moves to a strictly smaller `K3,3` debt packet.

Run:

```text
python3 computations/verify_c6_k33_minimum_pure_debt_repair_unit.py --mode structural
python3 -O computations/verify_c6_k33_minimum_pure_debt_repair_unit.py --mode full
python3 -I -S computations/verify_c6_k33_minimum_pure_debt_repair_unit.py --mode exhaustive
```

All modes have frozen ledger SHA-256
`e436369afb5a94268ce65f4189ba5562746ee150c90134c789bb8a1c5bb822af`.
