# The unrestricted eight-site direct-repair boundary

This is a checkpoint, not a global closure theorem.  Start from the twenty-cell
Hamiltonian-cover seed in
`computations/search_hamiltonian_cycle_cover_closure.py`.  Its mixed histogram
is

\[
                            \{1:24,2:2\}.                 \tag{1}
\]

Allow every one of the 252 coordinate cells (uv;ab), including new
monochromatic cells.  Impose only the 24 exact missing-mate clauses for the
singleton terms already present in (1).  Unit soft clauses charge every cell
outside the seed.  Exact RC2 optimization gives cost thirteen.  Thus every
simultaneous direct repair of the original 24 singleton fibres has at least
(20+13=33) cells, and the bound is attained.

One returned set of thirteen additions is

```text
01;12 03;21 04;01 13;01 14;10 23;12 24;00
24;21 27;01 34;02 36;21 56;02 57;11
```

Exact re-enumeration of this 33-cell support gives pure sizes ((1,1,1)) and
the complete mixed histogram

\[
 \{1:58,2:41,3:9,4:5,5:1,6:1,8:1\}.                    \tag{2}
\]

So the minimum direct repair creates 58 new singleton fibres and is very far
from closed.  The direct lower bound can be rerun as the first two rounds of

```bash
.venv/bin/python computations/optimize_hamiltonian_cycle_cover_closure.py \
  --order 8 --max-rounds 2 --solver cadical195
```

The displayed witness and both complete histograms are independently checked
without SAT by

```bash
python3 computations/verify_n8_unrestricted_direct_repair.py
```

The distinct fixed-cap global-closure run

```bash
.venv/bin/python computations/search_hamiltonian_cycle_cover_closure.py \
  --cap 33 --allow-new-monochromatic --solver cadical195
```

printed only

```text
seed_cells=20 mixed_histogram={1:24,2:2} cap=33 pure_safe=False
round=0 cells=20 singletons=24 add=24 gadgets=24
```

and remained inside the next SAT call for thirty minutes.  It was manually
stopped at elapsed time `30:04`, with about 144 MB resident memory.  It gave no
SAT or UNSAT verdict.  Therefore global no-singleton closure at 33 cells is
unresolved; the certified statement here is only the thirteen-cell minimum
for repairing the original 24 obligations.
