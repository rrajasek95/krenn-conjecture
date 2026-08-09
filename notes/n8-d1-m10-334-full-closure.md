# N=8 D1: complete m=10 3+3+4 closure

The checker `computations/verify_n8_d1_m10_334_full_shadow.py` closes all 131
symbolic `3+3+4` branches.  This finishes the m=10 D1 frontier over every
field of characteristic other than two.

Exact dynamic repair visits 208,218 partial states and leaves 13,994 complete
ten-cell supports.  A frozen union of 86 input-fibre palettes root-unit-refutes
13,992 of them.  The other two occur on symbolic branches 63 and 79, but they
have exactly the same semantic 77-cell support.  The independently committed
three-binomial certificate proves that support's localized coefficient ideal
empty, so there is only one distinct coefficient problem and it is closed.

The 86-palette artifact starts with all 30 palettes from the `4+3+3` closure
and deterministically extracts 56 more.  A fresh reconstruction is run with:

```text
python3 computations/generate_n8_d1_m10_334_palettes.py --fresh
```

It reproduces artifact SHA-256
`5af17387cf56780b0f358ba91b393e7658047197425164ee49057d4205d4ad27`.
Every extracted palette is a subset of the complete 8,100-fibre input and is
checked by plain root unit propagation; no native UNSAT verdict is trusted.

Branch checks run in isolated batches to bound memory.  For example:

```text
python3 computations/verify_n8_d1_m10_334_full_shadow.py \
  --batch-start 0 --batch-end 20 --batch-output /tmp/334/0.json
```

The JSON batches are combined with `--aggregate-dir`.  Both normal and
optimized complete replays give 208,218 dynamic nodes, 13,994 complete
supports, 13,992 palette closures, two coefficient-ideal closures, and zero
remaining branches.  The aggregate ledger SHA-256 is
`be640c9830a68b5a671fbc403f646ae8e6ce80f63e7896899ef083203fa0907a`.

Together with the previous `4+4+2`, `3+4+3`, and `4+3+3` audits, this closes
every symbolic m=10 normal-form branch.  This is an m=10 result inside the
N=8 D1 lane; it does not by itself address supports with more than ten
off-Sigma cells or upgrade the finite N=8 computation to all orders.
