# Low connectivity does not place the first extra crossing in the rank-two fibre

## Result

Start with the literal eight-site coefficient row

\[
 a_{01}^{00}a_{23}^{00}
 \left(a_{45}^{01}a_{67}^{22}
       +a_{46}^{02}a_{57}^{12}\right)=0                 \tag{1}
\]

in word `00000122`, with fines

```text
01|23|45|67,   01|23|46|57.
```

The proved low-connectivity theorem does force an exact realization's
**aggregate** support graph to be 3-vertex-connected.  It does not force an
extra aggregate crossing cell to have the endpoint colours of `00000122`,
and therefore it does not force a third occurrence into (1).

This distinction is sharp.  There is a minimum 15-cell full-pure packet
whose aggregate support is 3-vertex-connected, whose three pure rows are
each normalized by one occurrence, and whose row (1) remains exactly the
displayed rank-two fibre.  Its four new separator-crossing cells are all
colour-incompatible with `00000122`.  The packet is not a full exact source:
its first complete mixed-row failure is the singleton

```text
operation  coefficient:00000022
fine       01|23|45|67
cells      a01^00 a23^00 a45^00 a67^22.
```

Thus the correct positive recurrence is driven by a **literal mixed
singleton debt**, not by aggregate low connectivity.  Any mate of that debt
either stays in the two remaining local `C4` fines or strictly reduces the
number of protected common-tail edges.  This gives a finite fixed-word tail
potential, but not yet a source deletion or an all-order induction.

The exact checker is
`computations/verify_n8_rank_two_tail_separator_breaking_guard.py`.

## 1. What the separator theorem does and does not say

Put

```text
L={0,1,2,3},   R={4,5,6,7},   C={01,23}.
```

The low-connectivity theorem is a theorem about the simple graph containing
an edge `pq` whenever the aggregate `3x3` table `A_pq` is nonzero.  It forgets
the endpoint-colour cell `a_pq^ab`, the coefficient word, and the matching
fine.  Consequently an aggregate edge from `L` to `R` may be present only in
a pure-one or pure-two decoration and be absent from the `00000122` row.

For literal perfect matchings, parity gives an exact, source-labelled
classification.  Among all 105 fines on eight sites the pair

```text
(number of L|R crossings, number of retained edges from C)
```

has census

```text
(0,0): 6     (0,2): 3
(2,0): 48    (2,1): 24
(4,0): 24.
```

There are no odd crossing counts.  After removing the two fines already in
(1), only one fine retains all of `C`, namely
`01|23|47|56`; the other 102 fines retain at most one protected tail edge.
Of those 102, 96 genuinely cross `L|R`; the remaining six rewire both sides
internally and still destroy the selected tail `C`.
This is a statement about actual matchings and ordered endpoint colours, not
an unlabelled support projection.

## 2. The minimum full-pure counterguard

The six seed cells are

```text
a01^00 a23^00 a45^01 a67^22 a46^02 a57^12.
```

Pure normalization requires at least two new colour-zero cells, four new
colour-one cells, and three new colour-two cells.  Hence every full-pure
completion has at least nine new cells.  Exhaustion of all
`105^3=1,157,625` triples of pure matching fines finds 880 minimum
completions which simultaneously

1. have exactly one occurrence in each pure word;
2. have 3-vertex-connected aggregate support; and
3. leave `00000122` with exactly the two seed fines.

The lexicographically first uses

```text
pure 0: 01|23|45|67
pure 1: 02|14|37|56
pure 2: 03|15|24|67
```

and adds

```text
a02^11 a03^22 a14^11 a15^22 a24^22
a37^11 a45^00 a56^11 a67^00.
```

Its aggregate edge set is

```text
01 02 03 14 15 23 24 37 45 46 56 57 67
```

with degree sequence `(3,3,3,3,4,4,3,3)`.  Deleting every set of zero, one,
or two vertices leaves a connected graph.  The crossing cells

```text
a14^11 a15^22 a24^22 a37^11
```

are all incompatible with the endpoint colours of `00000122`.

Set every cell to one except `a57^12=-1`.  Then the two monomials in (1)
have values `+1,-1`, while the three unique pure monomials each have value
one.  This is an exact coefficient counterexample to the inference

```text
3-connected aggregate support
    => a separator-breaking mate in coefficient:00000122.
```

It is intentionally not promoted to a Krenn source.  Complete occurrence
enumeration finds five mixed singletons, the first being the row displayed
in the Result.  That row is the correct next source obligation.

## 3. The true finite recurrence

Let `M` be the fine of a mixed singleton and let `C` be the set of protected
tail edges outside its four-site window.  Exactness forces another fine
`M'` in the **same word**.  There are two alternatives.

* If `C` is contained in `M'`, then `M'` differs only inside the four-site
  window.  At order eight it is one of the two other local `C4` fines, and
  the complete row retains its literal common cofactor.
* Otherwise the integer

  \[
             \tau_C(M')=|C\cap M'|                         \tag{2}
  \]

  is strictly smaller than `|C|`.  The symmetric difference is a union of
  alternating even cycles, so this loss is a physical change of matching
  fine; it cannot be hidden by an odd one-edge crossing.

For the canonical singleton above, the 104 possible distinct mates split
as follows.  Exactly two retain both `01,23`: `01|23|46|57` needs the one
new cell `a57^02`, while `01|23|47|56` needs
`a47^02,a56^02`.  Every other mate lowers (2) to at most one.  The checker
records the complete census by crossing count, retained-tail count, and
number of missing ordered-colour cells.

More invariantly, for a fixed word define the common-tail set

\[
       \Gamma_w=\bigcap_{M\in{\cal O}_w}M .                \tag{3}
\]

Adjoining a new cancellation occurrence never enlarges `Gamma_w`, and any
tail-changing mate (including every separator-crossing mate) strictly
decreases it.  Thus `|Gamma_w|` is a
well-founded potential for repeated repairs **inside one coefficient row**.
This is the strongest uniform conclusion presently justified by the first
crossing packet.

It is not yet the desired all-order recurrence.  At `Gamma_w=empty`, or
when the proof pivots to a newly created word, (3) supplies neither an active
clean cap nor a lower-order source.  Closing the induction still needs one
of the following source-level statements:

```text
zero common tail => Laurent/unit or active clean cap,
zero common tail => full-row support deletion,
or a global potential that also decreases when the debtor word changes.
```

The full-pure packet above is the smallest exact guard showing why aggregate
3-connectivity alone cannot supply that statement.

## 4. Reproduction

Run all modes:

```text
python3 computations/verify_n8_rank_two_tail_separator_breaking_guard.py --mode structural
python3 -O computations/verify_n8_rank_two_tail_separator_breaking_guard.py --mode full
python3 -I -S computations/verify_n8_rank_two_tail_separator_breaking_guard.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
16601e3a9b4ecb8fadfd3ed46402bc5214a3b554bcb1e63c313485f162ef2750
```
