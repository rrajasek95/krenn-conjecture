# Terminal `C6` repair orbits and the first signed-exit recurrence

## Result

The deterministic diagonal repair closure of `c5e9407` has 46,702 terminal
supports.  Quotienting those supports by the order-eight stabilizer of the
labelled three-direct guard gives 21,483 canonical orbit keys, of which
eighteen have the minimum size fifteen.  For every one of those eighteen
minimum classes, every cardinality-minimum endpoint-coloured packet mating
the old singleton rows creates a new literal mixed singleton under the full
729-word replay.

There is nevertheless an occurrence-level recurrence beyond that first
layer.  On the most favourable minimum class, the smallest endpoint-coloured
extension with no mixed singleton uses sixteen new cells.  This minimum is
exact: the finite Boolean problem is UNSAT at cost at most fourteen and at
cost exactly fifteen, while an explicit cost-sixteen packet exists.

The cost-sixteen packet is **not** an exact source guard.  Three of its
two-term rows, consisting of the parent anti-diagonal and two literal `C4`
geometries among the thirteen exits of `9ab9b48`, give the Laurent unit

\[
  1=-1.                                                       \tag{1}
\]

Thus the first singleton-free recurrence closes by a signed source
contradiction.  It does not produce a recurrent exact-source packet.

The exact checker is
`computations/verify_c6_terminal_orbit_offdiagonal_signed_exit_gate.py`.

## 1. Terminal-orbit census

The number of deterministic diagonal terminal supports at each size is

```text
15:68, 16:76, 17:127, 18:293, 19:626, 20:1118,
21:1655, 22:2882, 23:4330, 24:6482, 25:8679,
26:9093, 27:6730, 28:3164, 29:1199, 30:169, 31:11.
```

The deterministic list is not itself invariant under the guard stabilizer:
after applying a symmetry, the lexicographically first repairable singleton
can change.  Therefore the checker does not divide 46,702 by orbit sizes.
It assigns each listed support the canonical key of its full order-eight
orbit and groups equal keys.  The resulting class-key histogram is

```text
15:18, 16:32, 17:58, 18:117, 19:257, 20:430,
21:611, 22:1087, 23:1770, 24:2688, 25:3686,
26:4395, 27:3613, 28:1846, 29:740, 30:124, 31:11.
```

This convention preserves the literal labelled support while avoiding the
false assumption that each observed fibre is a complete group orbit.

## 2. All minimum classes export a first-layer singleton

For each of the eighteen size-fifteen keys, enumerate all current mixed
singleton rows.  For a singleton at word `w` and its selected matching
`M_w`, every other perfect matching `M` gives the endpoint-coloured repair
candidate

\[
 C(w,M)=\{uv;w_u w_v:uv\in M\}\setminus S.                 \tag{2}
\]

The checker solves the exact minimum-union problem requiring at least one
candidate for every old singleton, then replays all fifteen matchings on all
`3^6=729` words.  The minimum numbers of new cells for the eighteen classes
are

```text
7 7 9 8 8 8 5 5 8 8 8 8 8 8 7 9 8 7.
```

The numbers of minimum packets are

```text
8 2 48 24 6 24 2 2 8 8 6 24 168 168 8 48 24 2.
```

Even the best packet in each class creates respectively

```text
9 20 10 18 21 18 12 12 23 23 21 18 18 18 9 10 18 20
```

new mixed singleton rows.  These are literal coefficient occurrences with
word, fine matching, and endpoint colours retained; no cap-presentation or
`B/Eq` label is used.

## 3. The first occurrence recurrence

The favourable class used for the next search has diagonal support

```text
01;1 02;0 02;2 03;1 05;1
12;1 13;0 14;1 14;2 25;1
34;0 34;1 34;2 35;2 45;0.                                  (3)
```

It has six old singleton rows.  The following sixteen endpoint-coloured
cells remove every mixed singleton:

```text
13;02 13;10 13;12 13;21
14;01 14;20
15;00 15;10 15;22
23;11
34;02 34;20
35;02 35;10
45;12 45;20.                                                (4)
```

The complete output has exactly fifty mixed rows, each with two matching
occurrences.  Of the three pure rows, two have two occurrences and one has
four.  There are no singleton rows.

For minimality, introduce one Boolean variable for every one of the 135
endpoint-coloured edge cells.  Fix (3), use a Tseitin variable for each
matching occurrence in every mixed word, and impose

```text
an occurrence is live  =>  at least one other occurrence in its row is live.
```

The generated SMT instances prove `cost <= 14` UNSAT and `cost = 15`
UNSAT.  Together with (4), this proves exact minimum cost sixteen.  The
checker freezes hashes of both generated SMT programs and replays them with
Z3 in exhaustive mode.

## 4. Signed thirteen-exit closure

Write `m_{w,M}` for the nonzero cell monomial of occurrence `M` in word
`w`.  Three binomial rows of (3)--(4) are

| word | first fine and cells | second fine and cells | type |
|---|---|---|---|
| `101111` | `03|14|25`: `03;11,14;01,25;11` | `05|14|23`: `05;11,14;01,23;11` | `C4` exit |
| `111001` | `01|25|34`: `01;11,25;11,34;00` | `05|12|34`: `05;11,12;11,34;00` | parent anti-diagonal |
| `111100` | `01|23|45`: `01;11,23;11,45;00` | `03|12|45`: `03;11,12;11,45;00` | `C4` exit |

The four nonparent matching fines in the first and third rows occur among
the thirteen outside exits of the parent `S`-chain in `9ab9b48`.  The two
matching pairs are genuine `C4` moves: their common fine edges are `14` and
`45`, respectively, and the remaining four edges are exchanged.  Hence the
common endpoint-coloured factors `14;01` and `45;00` cancel inside their
rows.

More intrinsically, the nine uncoloured edges appearing in this table form
the complete bipartite graph

\[
 K_{\{0,2,4\},\{1,3,5\}}.                                  \tag{5}
\]

After reversing the middle row as prescribed by its coefficient `-1`, the
three first-side fines are

```text
03|14|25, 05|12|34, 01|23|45,
```

the three even permutations of (5).  The other side consists of

```text
05|14|23, 01|25|34, 03|12|45,
```

the three odd permutations.  Each side uses every edge of the `K3,3`
exactly once.  The signed exit is therefore exactly the permanent-triangle
edge-product identity, on a bipartition symmetry-equivalent to the
tail-free `K3,3` orbit.

Let `d_1,d_2,d_3` be the exponent difference “first monomial minus second
monomial” in the displayed order.  Direct cellwise replay gives

\[
 d_1-d_2+d_3=0.                                             \tag{6}
\]

Every complete mixed source row is a sum of its two live monomials, so each
ratio is `-1`.  Raising those three ratios to the coefficients `(1,-1,1)`
in (6) gives `-1`.  But (6) says the same Laurent monomial is `1`, proving
(1) over the complex source torus.

The fine label and spectator factor are not discarded here.  At six sites,
the two local `C4` exit rows retain the labelled common fine edges `14` and
`45`.  A further row-independent nonzero perfect-matching spectator tail
`T` tensors through this calculation formally.  A repair path that changes
the spectator tail is not covered and remains the actual uniform all-height
interface.

## Consequence and scope

The current repair frontier is

```text
all 18 minimum diagonal terminal classes
  -> every cardinality-minimum endpoint-coloured repair exports a singleton;

first exact-minimum singleton-free occurrence recurrence
  -> parent plus two of the 13 signed exits
  -> Laurent unit 1=-1.
```

This closes the first recurrent branch at minimum support without invoking
an active typed `C4` criterion: the exact source equations already exclude
the packet.  It does **not** classify larger diagonal terminal classes,
nonminimum repairs of the other seventeen minimum classes, or paths whose
spectator matching tail changes.  Those are the remaining repair-DAG scope.
The permanent-triangle form does promote verbatim to any later packet whose
six complementary `K3,3` permutation fines occur in three nonzero binomial
rows with the same odd sign product.  Merely having the uncoloured `K3,3`
support, without those endpoint-coloured row pairings, is not yet enough.
In particular this note does not prove that every singleton-free repair of
a three-channel `K3,3` seed has the required subconfiguration.  The first
contamination is a third live matching in one of the three triangle rows:
then the source equation is `m_even+m_odd+m_extra=0` and no longer forces
the even/odd ratio to be `-1`.  Endpoint colours can also distribute the six
permutation fines among different, unpaired words.  Excluding these two
contaminations is the precise promotion lemma still needed.

## Reproduction

```text
python3 computations/verify_c6_terminal_orbit_offdiagonal_signed_exit_gate.py --mode structural
python3 -O computations/verify_c6_terminal_orbit_offdiagonal_signed_exit_gate.py --mode full
python3 -I -S computations/verify_c6_terminal_orbit_offdiagonal_signed_exit_gate.py --mode exhaustive
```

All modes return the same frozen ledger digest; exhaustive mode additionally
replays the two UNSAT instances.
