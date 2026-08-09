# N=8 D1: complete m=10 4+3+3 shadow closure

The checker `computations/verify_n8_d1_m10_433_full_shadow.py` closes all 54
remaining symbolic `4+3+3` branches at the complete 8,100-fibre support
level.  No complete-shadow SAT support was found, so there is no coefficient
problem in this family.

The proof recomputes necessary repair DNFs after every partial support
extension.  This exact dynamic search visits 71,901 partial states and leaves
3,480 complete ten-cell supports.  The 19 root-unit fibre palettes inherited
from the `3+4+3` closure, together with 11 newly extracted palettes, then
refute every residual support.  Each palette contains only input fibres from
the complete shadow, and every conflict is independently recomputed by plain
unit propagation; native SAT verdicts are not used.

Branch checks run in isolated batches to bound peak memory.  An individual
batch is checked directly with, for example:

```text
python3 computations/verify_n8_d1_m10_433_full_shadow.py \
  --batch-start 0 --batch-end 3 --batch-output /tmp/433/0.json
```

After partitioning all 54 branch positions into disjoint batches, combine
their JSON outputs with `--aggregate-dir`.  Both normal and optimized complete
batch replays reproduce the ledger below.  The deterministic palette generator
is `computations/generate_n8_d1_m10_433_palettes.py`.

The palette artifact
`computations/certificates/n8_d1_m10_433_rup_palettes.json` has SHA-256
`989e74059eb626a588e810c339f87ae3b5269f0909fc7d2003e72102c9810dbc`.
The checked aggregate ledger SHA-256 is
`731316a9b6a0758b70c4bfafcf14b1dbeaf450e38ee1088ca4199c78fc258f8f`.

Together with the earlier `4+4+2` and `3+4+3` closures, this reduces the m=10
symbolic frontier from 243 to 131 branches.  Every remaining branch is in the
`3+3+4` family.  The subsequent complete `3+3+4` support/coefficient audit
closes those 131 branches as well.
