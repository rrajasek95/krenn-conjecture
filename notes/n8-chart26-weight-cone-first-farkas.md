# A two-row weight-cone obstruction in chart 26

The first squarefree degree-six term after the (t)-last lexicographic lead
of the 546-term compatibility cell is

```text
s = 0948cfd9e1ef.
```

The current non-squarefree lead is

```text
m = 0948cfcfebef.
```

For an additive weight (w), making (s) strictly beat (m), after
integral scaling, requires

\[
 \langle m-s,w\rangle\le -1.                         \tag{1}
\]

But the completed degree-five cell from source codes 1459 and 1466 has
certified lead `0275cfebfb` and contains the term `0275d9e1fb`.  Retaining
that lead requires

\[
 \langle
   \mathtt{0275d9e1fb}-\mathtt{0275cfebfb},w
 \rangle\le0.                                         \tag{2}
\]

The exponent-difference vectors in (1) and (2) are exact negatives: after
cancelling common variables, (1) asks for

\[
                 w_{cf}+w_{eb}<w_{d9}+w_{e1},
\]

while (2) asks for the reverse weak inequality.  Adding (1) and (2) gives
(0\le-1).  The integral Farkas multipliers are simply ((1,1)).

Thus no additive weight inside the already certified degree-four/degree-five
Groebner cone can select `0948cfd9e1ef` as the new degree-six lead.  This is
an exact obstruction, not a numerical LP failure.

The 546-term cell has 350 squarefree top-degree terms.  This note excludes
only one of them.  A complete cone obstruction must either find analogous
Farkas combinations for the other candidates or produce a feasible weight
for one candidate.

Run the exact replay with

```text
python3 computations/verify_n8_chart26_weight_cone_farkas.py
```
