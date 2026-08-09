# N=8 D1: complete m=10 3+4+3 shadow closure

The checker `computations/verify_n8_d1_m10_343_full_shadow.py` closes all 58
symbolic `3+4+3` branches at the complete 8,100-fibre support level.  No
complete-shadow SAT support was found, so there is no coefficient problem in
this family.

The proof recomputes necessary repair DNFs after every partial support
extension.  This exact dynamic search visits 81,119 partial states and
reduces the nominal 58 by 287,980 three-cell choices to 4,393 complete
ten-cell supports.  A frozen basis of 19 compact fibre palettes then
root-unit-refutes every residual support.  Each palette contains only input
fibres from the complete shadow, and each claimed conflict is recomputed by
plain unit propagation; native SAT verdicts are not used.

Branch checks run in isolated batches to keep the peak memory of repeated
Tseitin construction bounded.  Individual batches are checked directly
with, for example:

```text
python3 computations/verify_n8_d1_m10_343_full_shadow.py \
  --batch-start 0 --batch-end 3
```

Run the same command with `python3 -O` for an optimized replay.  The 58
branch positions are partitioned into batches of three; their JSON outputs
are combined with `--aggregate-dir`.  Both normal and optimized complete
batch replays reproduce the ledger below.

The palette artifact
`computations/certificates/n8_d1_m10_343_rup_palettes.json` has SHA-256
`bd415532c49edad0df200a6a59debea79cba89a54389a79f99e6a5565ff11319`.
The checked aggregate ledger SHA-256 is
`3c0dcf1d30ce34e4daf3f8f5389bd7084ba178b27b4c62c8b519e8338a6af6f2`.

Together with the earlier `4+4+2` closure, this reduces the m=10 symbolic
frontier from 243 to at most 185 branches, all in `3+3+4` and `4+3+3`.
