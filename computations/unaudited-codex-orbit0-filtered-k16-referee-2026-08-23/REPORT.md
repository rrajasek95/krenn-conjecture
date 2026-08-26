# Independent exact referee: completed filtered K16 bucket

## Result

The corrected bounded reducer passes an independent streaming replay.  The
actual orientation is

```text
direct K16 seed - frozen K14-pivot response,
```

as proved by the separate literal sign referee.  The isolated frozen response
was replayed byte-for-byte against all `1,848,174` JSON records.  A streaming
two-way merge of it with all `24,097,095` collected direct records, followed by
the exact 78-head pivotability projection, reproduces the reduced checkpoint
row-for-row and coefficient-for-coefficient.

Exact census:

```text
combined:           25,945,269 H-orbits
removed pivotable:  24,003,767 H-orbits
reduced K16:         1,941,502 H-orbits
signed orbit mass:    -113,094,144
orbit-mass L1:        1,187,764,512
cycle partitions:               121
77-cycle charge:       +375,127,296
```

The 77-cycle charge was evaluated from the actual reduced rows and the frozen
integer dual; it is not the signed coefficient mass.

This completes only the chosen K16 initial bucket.  K16 pivot tails at
K18/K19/K20 were not emitted, and no K17+, confluence, membership, or
localization statement follows.

Replay:

```text
python3 computations/unaudited-codex-orbit0-filtered-k16-referee-2026-08-23/referee_filtered_k16.py --write-results
```

Logical digest:
`34dc111259fcffefc33acf2675efeb4315121e8b3735d592566e067f85caf120`.
