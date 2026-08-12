# The nine four-base bridges have a sharp first decoration boundary

## Result

The nine pure-zero physical `C4` bridges forced by `c44d784` do not all
enter the same source-labelled exchange.  With the selected fixed endpoint
holes

```text
G11:01,   G12:04,   G21:13,   G22:34,
```

their first complete rows split exactly as follows.

1. `01|25|34` occurs in both diagonal rows.  Its `G11[110000]` cofactor
   triangle is `{A,B,01|25|34}`, while its `G22[000220]` triangle is
   `{K,L,01|25|34}`.  It is therefore not silent: it is the unique bridge
   whose literal response occurrences meet both old components.
2. Four bridges contain one selected crossed hole.  Each enters its literal
   crossed cofactor triangle together with another forced bridge and the
   crossed separator `04|13|25`.  This is exact source propagation, but it
   is not yet an old-base typed edge.
3. Four bridges contain none of the four selected holes.  No fixed-port
   response monomial can contain them.

The checker is
`computations/verify_h3_four_base_c4_bridge_decoration_sync_boundary.py`.

## The five bridges avoiding crossed holes

Exactly five bridges avoid the crossed holes `04,13`:

```text
01|25|34,
02|14|35, 03|12|45, 03|15|24, 05|14|23.
```

The first is already visible in the two diagonal rows above.  For each of
the remaining four, choose one pure-one target cofactor

```text
A1=23|45, A2=24|35, A3=25|34
```

and one pure-two target cofactor

```text
B1=01|25, B2=02|15, B3=05|12.
```

There are nine bright charts per bridge.  In exactly five charts, one
bright q edge is shared by the bridge and one of its old adjacent bases.
The corresponding mixed unary coefficient has exactly two supported terms:

```text
02|14|35:  000101 -> {B,R},   202000 -> {R,K};
03|12|45:  000011 -> {A,R},   022000 -> {R,L};
03|15|24:  001010 -> {B,R},   020002 -> {K,R};
05|14|23:  001100 -> {A,R},   200002 -> {L,R}.
```

The displayed bright edge is the literal common decorated tail.  Hence
these are genuine two-term same-word `C4` rows, not graph-only adjacency.
Across the four bridges the exact chart count is

```text
20 bright charts with a binomial C4 row,
16 bright charts with no such occurrence.
```

In each of the sixteen residual charts, neither selected bright q tail
shares an edge with the bridge.  Since the bridge also contains no selected
endpoint hole, it occurs in no fixed-port response row and in no
positive-bright-degree top coefficient inside the minimal decorated
envelope.  It remains visible only in `q^[3][000000]`.

## Consequence

Bright completion does not uniformly synchronize all nine forced bridges.
It closes the overlap bridge immediately and gives a literal binomial row
in twenty hole-free charts, but leaves sixteen exact first-layer silent
charts.  The missing theorem is now precise: a complete source row must
force a bright/offdiagonal decoration onto an edge shared by the silent
bridge and an old adjacent base, or route the compensating mate to the
already certified nonanchor/Hall/lock branches.

The sixteen records are not full-source counterexamples.  Arbitrary extra
decorated q cells may cancel the private bright rows and create the required
shared decoration; the checker freezes only the first source-labelled
decoration boundary.

## Verification

```text
python3 computations/verify_h3_four_base_c4_bridge_decoration_sync_boundary.py
python3 -O computations/verify_h3_four_base_c4_bridge_decoration_sync_boundary.py
python3 -I -S computations/verify_h3_four_base_c4_bridge_decoration_sync_boundary.py
```

Frozen ledger SHA-256:

```text
bf2f107bdf19d2bcd8206a9d70fe73f457bec0afb55a37475228573fb009c2a5
```
