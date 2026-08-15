# Minimum endpoint-offdiagonal repairs of the first terminal `C6` fibre create new units

## Result

The first endpoint-offdiagonal layer after `c5e9407` does not close.  Among
the 46,702 terminal vertices of the diagonal repair DAG, 68 have the minimum
size of fifteen cells.  Choose the lexicographically canonical labelled one:

```text
01;1 01;2 02;0 03;1 05;1
12;1 13;0 14;1 23;1 25;1 25;2
34;0 34;1 34;2 45;0.                                    (1)
```

Its labelled vertex stabilizer is trivial.  Its complete diagonal output has
eight mixed singleton rows: three of type `2+2+2` and five of type `4+2`.

For every singleton, enumerate all fourteen alternative perfect matchings
using literal endpoint-colour cells `uv;ab`.  An exact minimum-union solve
gives two useful versions of the answer.

* Allowing diagonal companions together with the necessary off-axis cells,
  the minimum packet has seven cells.  There are exactly eight packets, and
  each has five endpoint-offdiagonal plus two diagonal cells.
* Requiring every new cell itself to be endpoint-offdiagonal, the minimum is
  eight cells.  There are exactly 24 packets.

Every packet mates all eight old singleton rows.  Nevertheless, a complete
replay of all 729 physical output words creates new mixed singleton rows in
every case.  The seven-cell packets create between nine and 38 new units;
the strict eight-offdiagonal packets create between sixteen and 33.  Thus
the first off-axis repair layer exits immediately through an ordinary source
unit.  There is no minimum full-row counterguard.

The exact checker is
`computations/verify_c6_three_direct_minimum_offdiagonal_repair_unit.py`.

## 1. The canonical terminal fibre

The eight old singleton records are

| word | profile | fine | decorated cells |
|---|---:|---|---|
| `112002` | `2+2+2` | `01|25|34` | `01;11,25;22,34;00` |
| `112222` | `4+2` | `01|25|34` | `01;11,25;22,34;22` |
| `221001` | `2+2+2` | `01|25|34` | `01;22,25;11,34;00` |
| `221100` | `2+2+2` | `01|23|45` | `01;22,23;11,45;00` |
| `221111` | `4+2` | `01|25|34` | `01;22,25;11,34;11` |
| `221221` | `4+2` | `01|25|34` | `01;22,25;11,34;22` |
| `222002` | `4+2` | `01|25|34` | `01;22,25;22,34;00` |
| `222112` | `4+2` | `01|25|34` | `01;22,25;22,34;11` |

Every row retains the original cap `34`, window `0125`, tail `T`, output
word, fine matching, and literal coefficient operation.  The displayed
cells use the full endpoint convention: for example `15;12` means colour
one at site 1 and colour two at site 5.

The diagonal closure made the first three rows terminal because a
`2+2+2` word has only one diagonal occurrence.  Once offdiagonal cells are
allowed, each fixed word again has all fifteen perfect matchings available,
so there are fourteen possible mates for its selected fine.

## 2. Exact minimum-union problem

For a row `w` and alternative matching `M`, let

\[
 C(w,M)=\{uv;w_u w_v:uv\in M\}\setminus S_0,             \tag{2}
\]

where `S0` is the full endpoint-coloured lift of (1).  A repair packet `P`
mates the row precisely when some `C(w,M)` is contained in `P`.  The finite
optimization problem is therefore

\[
 \min |P|\quad\text{subject to}\quad
 \forall w\ \exists M\ne M_w:\ C(w,M)\subseteq P.         \tag{3}
\]

Strict supersets among the fourteen candidates for one row may be discarded:
the smaller candidate already repairs that row, while any useful extra cell
must occur in the selected candidate of another row.  After this reduction,
seven rows retain fourteen candidates.  Row `221111` retains twelve because
one one-cell candidate dominates two larger ones.  Candidate sizes are one,
two, or three.

The exact depth-limited search for unrestricted endpoint-coloured packets is

```text
budget       2   3   4   5   6   7
solutions    0   0   0   0   0   8.                      (4)
```

All eight solutions have type `(offdiagonal,diagonal)=(5,2)`.  If candidates
containing any new diagonal cell are forbidden, the search is

```text
budget       2   3   4   5   6   7   8
solutions    0   0   0   0   0   0  24.                  (5)
```

Equations (4)--(5) are cardinality certificates, not greedy upper bounds:
the checker exhausts every viable candidate union at each smaller budget.

## 3. Complete source replay

For each minimum packet the checker adjoins its cells to (1), enumerates all
fifteen matchings for each of the `3^6=729` words, and records the literal
occurrence fibre.  It first verifies that every old row in the table has at
least two occurrences.  It then counts all new mixed rows having exactly one
occurrence.

For the eight seven-cell packets the histogram is

```text
new singleton rows  9 20 22 23 25 33 38
packets             1  1  1  1  2  1  1.                 (6)
```

The sharp packet with only nine new units is

```text
02;12 02;21 05;22 12;22 13;21 15;12 15;21.               (7)
```

Its first new physical singleton is

```text
word       010002
profile    4+1+1
fine       02|15|34
cells      02;00, 15;12, 34;00
operation  coefficient:010002
cap/window 34 / 0125
tail       T.                                               (8)
```

The coefficient in (8) is the product of three live source entries and is
therefore nonzero.  Its word is mixed, so its target coefficient is zero.
This is an immediate source unit; no coefficient signs or auxiliary
presentation labels enter.

For the 24 strict-offdiagonal packets, the exact new-singleton histogram is

```text
16:1, 17:1, 18:2, 19:2, 20:4, 21:4, 22:2, 23:1,
24:1, 25:1, 26:1, 27:1, 29:1, 30:1, 33:1.                 (9)
```

Thus forbidding the two diagonal helpers does not improve the physical
landing; it increases both the packet size and the best residual unit count.

## Consequence and scope

For the canonical smallest terminal fibre, the first full endpoint-coloured
repair alternative is

```text
minimum off-axis repair -> new literal mixed singleton.                    (10)
```

This closes the requested first repair layer without invoking an active-cap
criterion: the stronger source-unit exit already occurs.

The result is deliberately local.  It classifies the minimum packets mating
all old singleton rows of one canonical terminal among the 68 smallest
terminal states.  It does not yet classify the other 67 labelled terminals,
larger packets that also mate the new rows, or a full iterative
endpoint-coloured repair closure.

## Reproduction

```text
python3 computations/verify_c6_three_direct_minimum_offdiagonal_repair_unit.py --mode structural
python3 -O computations/verify_c6_three_direct_minimum_offdiagonal_repair_unit.py --mode full
python3 -I -S computations/verify_c6_three_direct_minimum_offdiagonal_repair_unit.py --mode exhaustive
```

All modes return the same frozen ledger digest.
