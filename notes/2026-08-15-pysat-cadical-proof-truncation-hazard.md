# Tooling hazard: pysat + cadical `get_proof()` truncates DRUP proofs (2026-08-15)

Found by the W11 verification lane
(`computations/unaudited-sat-pair-w11-2026-08-15/`, §6 of its report).

**Symptom.** `Cadical195` / `Cadical153` via pysat with
`with_proof=True` + `get_proof()` can return a proof file cut off
mid-clause (the tail decodes to an unterminated literal run). Such
proofs never derive the empty clause and do not replay: the UNSAT
verdict may be correct while the stored certificate is worthless.

**Observed impact.** 7 of the W8 sweep's stored DRUP files fail
replay (4 at m<=15, 3 at m16_closure). All were re-solved UNSAT by
three independent solvers, and verified lingeling replacement proofs
are stored in
`computations/unaudited-sat-pair-w11-2026-08-15/w8_reproofs/`.
The mathematics stands; the certificate files were defective.

**Action required by any lane emitting SAT certificates** (including
the `computations/certificates/n8_*` CNF/DRUP work): check that every
stored proof (a) terminates in the empty clause `0`, and (b) replays
under an independent checker (drat-trim, or the forward RUP checker
`rupcheck.c` in the W11 directory). Prefer solvers whose native
proof-file writing is used directly (lingeling `-t`, cadical run as a
binary with a proof-path argument) over pysat's in-memory
`get_proof()` extraction.
