# Certificate engineering for the six-site phase boundary

This note records proof-backend tests for the static exact-35 formula in
`notes/n6-unrestricted-minimum-closure-phase-obstruction.md`.  It is a
certificate workflow audit, not an additional mathematical assumption.

## 1. Persisted semantic formulas

The deterministic generator

```text
computations/generate_n6_full_closure_formula_bundle.py
```

writes the CNF before attempting any proof search and records every semantic
phase core in JSON.  The exact-35 bundle is

```text
computations/certificates/n6-full-closure-phase-exact35.cnf
computations/certificates/n6-full-closure-phase-exact35.json
```

with 12,212 variables, 59,031 clauses, and 73 phase cores.  Its JSON has
`drup_lines: null`, so it cannot be mistaken for a completed proof bundle.
The semantic replay mode independently rebuilt all 73 inconsistent Laurent
cores and matched the DIMACS bytes and SHA-256:

```bash
.venv/bin/python computations/verify_n6_full_closure_phase_certificate.py \
  computations/certificates/n6-full-closure-phase-exact35 --skip-drup
```

The smaller backend test uses the complete no-singleton formula at cap 29:

```text
computations/certificates/n6-full-closure-cap29.cnf
computations/certificates/n6-full-closure-cap29.json
```

It has 11,591 variables and 56,323 clauses, with no phase refinements.  Its
semantic replay also passes.

## 2. Proof-capable backend benchmark at cap 29

All runs used the same persisted CNF and a 120-second process cutoff.

| backend | solve time | additions | proof size | status |
|---|---:|---:|---:|---|
| CaDiCaL 1.0.3 | 54.139 s | 982,397 | 72 MB | pure RUP; verified |
| MapleSAT | 61.121 s | 338,216 | 90 MB | deletion-stripped trace fails DRAT; reject |
| Glucose 4.2 | 65.029 s | 457,216 | 81 MB | pure RUP; verified |
| Gluecard 4 | 82.307 s | 541,088 | 119 MB | generated, not replayed |
| MapleChrono | 97.565 s | 528,664 | 138 MB | generated, not replayed |
| MapleCM | 102.415 s | 533,397 | 93 MB | generated, not replayed |
| Lingeling | (>120) s | -- | -- | timeout |

CaDiCaL 1.0.3 is both the fastest tested proof backend and the smallest raw
trace.  PySAT's CaDiCaL 1.5.3 and 1.9.5 wrappers solve but expose no proof;
the 3.0.0 wrapper exposed a trace without a final empty-clause addition in a
small audit and is rejected.  Kissat 4.0.4 and MergeSat3 do not support proof
logging through PySAT.

The repository's simple Python RUP checker processed about 90,000 of the
982,397 CaDiCaL additions in 120 seconds.  The official native `drat-trim`
checker verified the raw trace in 79.204 seconds and reported zero RAT lemmas.
Its core extraction, followed by deletion stripping, reduced the certificate
to 290,128 additions and 27 MB; that deletion-free proof reverified natively
in 38.284 seconds.  Removing deletions is sound here because `drat-trim -U`
first certifies that every addition is RUP, whose validity is monotone when
deleted clauses are retained.

The producing and replay commands are

```bash
.venv/bin/python computations/prove_dimacs_pysat.py FORMULA.cnf RAW.drup \
  --solver cadical103
drat-trim FORMULA.cnf RAW.drup -U -l CORE-WITH-DELETIONS.drup
python3 computations/strip_drat_deletions.py \
  CORE-WITH-DELETIONS.drup CORE.drup
drat-trim FORMULA.cnf CORE.drup -U
```

## 3. Exact-35 status and next workflow

CaDiCaL 1.9.5 returned `UNSAT` on the full exact-35 formula after about 18.5
minutes.  A subsequent Glucose4 proof attempt was stopped after 41.5 minutes,
and five-minute capped proof tests of CaDiCaL 1.0.3, Glucose4.2, and MapleSAT
all timed out.  Hence blindly changing proof backends is not enough.

The next exact step guards each of the 73 phase clauses by a separate
assumption selector and asks CaDiCaL 1.9.5 for an UNSAT assumption core.  A
returned core is solver-certified: unselected guards can be false, so the base
formula plus precisely the selected unguarded phase clauses is UNSAT.  The
driver then persists that reduced semantic CNF/JSON before any proof search:

```bash
.venv/bin/python computations/extract_n6_phase35_assumption_core.py \
  computations/certificates/n6-full-closure-phase-exact35 \
  computations/certificates/n6-full-closure-phase-exact35-core \
  --solver cadical195
```

Only after semantic replay of the reduced bundle should CaDiCaL 1.0.3 receive
a bounded proof run.  No replayable exact-35 DRUP proof is claimed until that
trace ends in the empty clause and passes an independent checker.

The guarded assumption-core call was run with an external 20-minute cutoff.
It reached the cutoff without returning a core, so the process was stopped and
no reduced `exact35-core` CNF/JSON was written.  Consequently the conditional
ten-minute CaDiCaL 1.0.3 proof benchmark on a reduced formula was not launched.
The persisted full exact-35 semantic bundle remains the current artifact; an
exact-35 DRUP trace remains open.
