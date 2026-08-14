# Every support-17 graph deletes safely to support 16

Let `G` be a simple graph on eight vertices with 17 edges and minimum degree
at least three.  Put

```text
H = {v : deg(v) >= 4},    L = V(G) - H.
```

The total excess above degree three is

```text
sum_v (deg(v)-3) = 2*17 - 3*8 = 10.
```

Since a vertex contributes at most four excess units, `|H| >= 3`.
Suppose `H` were independent.  Every edge incident with `H` would then run
from `H` to `L`, so the degree sum on `H` would have to fit inside the total
degree capacity of the cubic vertices in `L`:

```text
sum_(v in H) deg(v) = 3|H| + 10 <= 3|L| = 3(8-|H|).
```

This inequality forces `|H| <= 2`, a contradiction.  Hence two vertices of
degree at least four are adjacent.  Deleting their edge lowers both degrees
by one, preserves minimum degree three, and produces a 16-edge graph.

This gives a canonical reduction of every support-17 topology to the
completed support-16 census.  It does not by itself prove that a particular
support-16 clean cap remains clean when the deleted edge is reinserted; that
source-labelled persistence/repair statement is the sole remaining
support-17 obligation.

Exact degree-sequence audit:

```text
python3 computations/verify_n8_support17_high_degree_deletion_lemma.py
python3 -O computations/verify_n8_support17_high_degree_deletion_lemma.py
python3 -I -S computations/verify_n8_support17_high_degree_deletion_lemma.py
```

Frozen ledger SHA-256:

```text
d79dd734c485958f88567d8dc683f03408d09b47c695ff87e9dc7b1a99e61631
```
