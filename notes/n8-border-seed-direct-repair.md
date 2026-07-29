# Minimum direct repairs of the eight-site border seed

This note closes the smallest, most literal repair of the Laurent border
family in [`n8-counterexample-recon.md`](n8-counterexample-recon.md),
equations (3)--(5).  It does not exclude arbitrary denser supports.  The
solver-free checker is

```text
computations/verify_n8_border_seed_direct_repair.py
```

and enumerates all 105 perfect matchings and every output fibre exactly.

## 1. Every direct repair costs at least four cells

Let `S` be the twelve decorated diagonal cells of the three selected
matchings.  Its two mixed singleton colourings are

```text
22101000  and  01002102.
```

For either colouring, decorate each of the other 104 perfect matchings by
that fixed endpoint colouring and remove the cells already in `S`.  The
cardinalities of the resulting missing-cell sets are

\[
   \#\{|D|=2,3,4\}=(12,32,60).
\]

Thus each old singleton needs at least two new cells.  Exhausting all
`104^2` pairs of candidate mates shows that the union of their missing cells
has size at least four.  Equality occurs for exactly 144 distinct added-cell
sets (always a pair of two-cell mates).

## 2. All 144 minimum repairs create new singleton fibres

For each of those 144 supports, exact re-enumeration gives the following
distribution according to the number of mixed singleton fibres:

\[
\begin{array}{c|rrrrrr}
\text{new singleton count}&4&5&6&7&8&9\\ \hline
\text{number of supports}&8&20&75&13&20&8.
\end{array}
\]

In particular every four-cell direct repair is impossible over
`C*`: a singleton coefficient is a nonzero monomial and cannot cancel.
This is an exact obstruction to the smallest natural repair chart, not just
a support heuristic.

## 3. Sharp countermodel to a stronger local claim

The lower bound above is sharp for mating the *two old* border terms.  Add

```text
02;21  14;21  17;12  45;21.
```

The resulting sixteen-cell support has mixed-fibre histogram

\[
             \{|F|=1:4,\ |F|=2:3\}.
\]

Give `02;21` and `17;12` weight `-1` and every other selected cell weight
`+1`.  All three binomial mixed coefficients (including both original
border errors) then vanish, and all three pure coefficients remain one.
The complete nonzero output is

\[
 \Delta_{8,3}
 +e_{02001000}-e_{11111222}-e_{20100000}+e_{22222111}.
\]

Consequently, the tempting stronger assertion that compatible cancellation
mates for the two old singletons suffice is false in the smallest possible
support: they necessarily expose fresh singleton fibres.  This explicit
rational sixteen-cell point is a minimal countermodel to that local repair
principle.

The later twelve-cell closure `B24` in
[`n8-orbit8-pairwise-boundary-repair.md`](n8-orbit8-pairwise-boundary-repair.md)
does remove all singleton fibres, but its 22 binomial equations contain
twelve odd Laurent triangles.  Hence passing from four to twelve added cells
removes the support obstruction without resolving the coefficient
obstruction.

## 4. Exact second-generation mate enumeration

The sixteen-cell support has exactly two target-preserving support
automorphisms.  Besides the identity, the nontrivial one is

```text
vertices: 01234567 -> 24031765
colours:  012      -> 021.
```

The displayed `+/-1` weighting is preserved only by the identity.  On the
four singleton residuals, the support involution fixes `02001000` and
`20100000` and swaps `11111222` with `22222111`.

For each residual singleton, the 104 possible distinct mate matchings again
have missing-cell census `(12,32,60)` in sizes `(2,3,4)`.  Dynamic
programming over unions of these exact missing-cell sets gives

\[
\begin{array}{c|rrrr}
\text{added-cell cap}&\text{after fibre 1}&\text{after fibre 2}
 &\text{after fibre 3}&\text{after fibre 4}\\ \hline
4&104&144&24&0\\
5&104&912&88&0\\
6&104&3376&2284&288.
\end{array}
\]

Thus six further cells are necessary and sufficient merely to mate all four
old residuals.  There are 288 minimum supports, forming 144 free orbits under
the residual involution.  Re-enumerating their complete fibres shows that
none is singleton-free: they create between 14 and 29 singleton mixed
fibres.  The complete count by number of new singletons is

```text
14:2  15:2  16:16 17:20 18:20 19:36 20:50 21:54
22:30 23:22 24:12 25:10 26:8  27:2  28:2  29:2.
```

This is the requested symmetry-quotiented enumeration of every minimum mate
set.  It also shows why iterating the visually obvious cancellation repair
gets worse rather than converging.

## 5. Bounded unrestricted support closure

The dedicated exact search is

```text
computations/search_n8_border_nearsolution_completion.py
```

Its support variables range over all 252 decorated aggregate cells.  For a
singleton trigger it introduces selectors for every feasible distinct mate.
Two reductions make the replay smaller without changing its support
projection:

1. a mate is deleted if the fixed seed, trigger, and mate exceed the global
   cell cap;
2. a mate requirement is deleted if it strictly contains another mate
   requirement for the same trigger.

The sole support involution is quotiented by a Boolean lex leader.  Exact SAT
replay gives no singleton-free extension through 25 total cells.  In
particular the sixteen-cell point needs at least ten additional cells before
all mixed fibres can even *possibly* cancel.  The cap-25 replay is

```sh
.venv/bin/python computations/search_n8_border_nearsolution_completion.py \
  --cap 25
```

This is a bounded exhaustive solver result; no portable DRUP trace is claimed.

There is a useful structured upper chart.  Transport the twelve `B24` cells
to the present labels and adjoin `35;00,67;00`.  Together with the sixteen
fixed cells this gives a 28-cell base with mixed histogram

\[
             \{1:3,\ 2:35,\ 3:1,\ 4:3,\ 6:1\}.
\]

Within this fixed-base chart, no singleton-free extension exists through 31
cells.  At 32 cells the first one is obtained by adjoining

```text
36;01 57;01 67;01 67;10.
```

It has no singleton fibres at all:

\[
              \{2:65,\ 4:12,\ 6:4\},
\]

and its three pure fibre sizes are `(2,2,2)`.

## 6. Exact coefficient obstruction on the singleton-free chart

Support viability does not survive the Laurent equations.  Three complete
binomial fibres of the 32-cell support, after canceling their displayed
common nonzero monomial factors, are

\[
\begin{array}{c|l}
01001102&x_{15}^{11}x_{47}^{12}+x_{17}^{12}x_{45}^{11}=0,\\
11111100&x_{12}^{11}x_{45}^{11}+x_{15}^{11}x_{24}^{11}=0,\\
11111222&x_{12}^{11}x_{47}^{12}+x_{17}^{12}x_{24}^{11}=0.
\end{array}
\]

The first two equations multiply to ratio `+1` for

\[
 \frac{x_{12}^{11}x_{47}^{12}}
      {x_{17}^{12}x_{24}^{11}},
\]

whereas the third requires the same ratio to be `-1`.  All cells are nonzero
on the support torus, so this is an immediate contradiction over
characteristic zero.  The full lattice audit finds 108 such unit odd
triangles.

The unrestricted-multiterm CEGAR over this 28-cell base is UNSAT through 34
total cells: every singleton-free support encountered has an inconsistent
binomial core, and the core-breaking clauses exhaust all alternatives.  For
the minimum layer, replay with

```sh
.venv/bin/python computations/search_n8_border_nearsolution_completion.py \
  --structured --full --cap 32
```

The independent checker verifies the complete 32-cell fibre census and the
three-row Laurent contradiction directly.  Hence this continuation produces
no exact ternary realization: the smallest local cancellation is the signed
sixteen-cell point of Section 3, while all unrestricted supports through 25
cells and the structured coefficient-complete chart through 34 cells are
excluded exactly.
