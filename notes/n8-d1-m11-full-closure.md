# N=8 D1: complete m=11 closure

The checker `computations/verify_n8_d1_m11_full_shadow.py` closes every m=11
D1 normal-form branch over fields of characteristic other than two.  It uses
the global all-size anchor theorem, exact dynamic repair, complete 8,100-fibre
support shadows, and the independently checked coefficient certificate for
the only semantic support survivors.

Global anchor completeness leaves four m=11 partitions:

| family | anchor orbits | repair-DNF survivors | added cells |
|---|---:|---:|---:|
| 3+3+5 | 132 | 132 | 5 |
| 3+4+4 | 64 | 64 | 4 |
| 4+3+4 | 64 | 64 | 4 |
| 4+4+3 | 52 | 25 | 3 |

Thus 27 of the 312 anchor orbits close before complete-support enumeration,
leaving 285 symbolic branches.  This replaces 28,464,032,688 raw addition
choices by a dynamic search over 3,222,382 memoized partial states.

The complete family census is:

| family | dynamic states | complete supports | palette closures | coefficient closures |
|---|---:|---:|---:|---:|
| 3+3+5 | 1,906,499 | 226,666 | 226,654 | 12 |
| 3+4+4 | 711,235 | 40,998 | 40,998 | 0 |
| 4+3+4 | 592,570 | 28,822 | 28,822 | 0 |
| 4+4+3 | 12,078 | 280 | 280 | 0 |
| total | 3,222,382 | 296,766 | 296,754 | 12 |

The twelve coefficient closures occur as six semantic supports on each of
branches `335:63` and `335:79`; the two branches give the same six supports.
Each support is a one-cell witness-invisible extension of the m=10 semantic
support and inherits the exact three-binomial `U^3` saturation certificate.
There are therefore six distinct coefficient supports and all are empty.

The palette generator starts from the 86 m=10 palettes and extracts 65 more:

```text
python3 computations/generate_n8_d1_m11_palettes.py --fresh
```

The resulting 151-palette artifact has SHA-256
`7db4241383a41988fa0245900f4c3f13a2118f226987b97c5fe058c59e8ae096`.
Its union contains 282 of the 8,100 input fibres.  Every claimed conflict is
recomputed by plain root unit propagation; no native UNSAT verdict is used.

Branch replay is partitioned into isolated batches, for example:

```text
python3 computations/verify_n8_d1_m11_full_shadow.py \
  --batch-start 0 --batch-end 20 --batch-output /tmp/m11/0.json
```

Normal and optimized complete batch replays agree on every row and reproduce
aggregate ledger SHA-256
`d8f3a84b54abac22a110f2da0e52f7a269f10e790acee54e21957371bb83d44e`.
The remaining m=11 symbolic frontier is zero.

This is an exact m=11 layer closure, not yet the all-support D1 theorem.  The
global anchor result shows that all higher layers remain inside the same 312
charts; chart-wide coefficient obstructions are the structural route beyond
further cardinality-by-cardinality enumeration.
