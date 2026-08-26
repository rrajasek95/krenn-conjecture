# Gröbner and Macaulay computation toolkit

This directory is the common execution layer for the conjecture proof.  Its
purpose is reproducibility and scope control: it makes expensive modular
discovery fast without allowing a modular computation to silently become a
characteristic-zero theorem.

## Required proof ladder

1. Derive and label every polynomial from the literal source equations.
2. Run modular discovery at two suitable primes.  Record the variable order,
   monomial/block order, localizers, row hashes, source hashes, commands,
   stdout/stderr, exit code, time, and peak RSS.
3. For saturation, put the saturating polynomial in the **final input row**.
   Run native F4SAT first and block elimination as a separate second stage.
4. Compare normalized factor profiles across primes.  A special-prime split
   is discovery evidence only; coefficient CRT is allowed only when supports,
   multidegrees, and multiplicities agree.
5. Close the result over `Q` by a literal identity, exact Gröbner reduction,
   or independently replayed exact certificate.  Modular ideal containment,
   two matching primes, and an msolve characteristic-zero `[1]` are not by
   themselves a theorem-grade source certificate.
6. Replay exact checkers under `std`, `-O`, and `-I -S`, with distinct
   `PYTHONHASHSEED` values and a mutation/must-fire control.

## msolve rules

- The strict parser forbids parentheses, `**`, and integer coefficients after
  symbolic factors.  msolve 0.10.1 silently misparses both `z*(poly)-1` and
  terms such as `z*2*x`; exporters must fully distribute localizers and print
  every integer coefficient first, for example `2*x*z`.
- Native `-S` currently rejects small primes such as 1009.  Use a large
  32-bit prime (the default recommendation is 1073741827); use a prime below
  `2^29` when a Singular cross-check is also required.
- Never combine `-S` with `-e` in msolve 0.10.1.  `run_msolve.py` writes the
  full saturated DRL basis, reparses it strictly, then starts elimination.
- A zero-byte output, crash, timeout, or parser-success banner is not a
  mathematical result.  Output, stdout, and stderr are recorded separately.
- F4SAT has a false-negative corner case when the saturator is literally
  duplicated as an ideal generator.  The must-fire regression therefore uses
  `<xy,xz>:x^infinity=<y,z>`.
- Product localizers can dominate the computation.  Keep a manifest of
  individual factors and prefer staged saturation when the algebra permits.

Example:

```sh
python3 computations/toolkit/groebner/run_msolve.py input.msolve \
  --output-prefix results/run \
  --mode saturate-eliminate --eliminate 1 \
  --threads 8 --timeout 1800 \
  --saturator-label pivot \
  --source exporter.py \
  --scope 'pivot-open component only'
```

## Tools

- `msolve_io.py`: strict input/output parser, logical row hashes, basis-count
  and reduced-leading-monomial checks, and safe full-basis staging.
- `run_msolve.py`: guarded basis/F4SAT/elimination runner and resource manifest.
- `run_msolve_parametrize.py`: fixed-seed zero-dimensional rational-
  parametrization runner.  It can seed from a strictly parsed full basis,
  records genericity/normal-form policy, and structurally parses the RUR
  envelope.  Characteristic zero is an explicit source-input-only opt-in and
  adds `-P 1`; finite-field points still require literal source replay.
- `factor_profile.py`: python-flint factor census for unique elimination rows;
  run with the repository `.venv/bin/python`.
- `run_checker_modes.py`: exact checker replay in the three standard modes;
  requested artifacts must be byte-identical.
- `run_macaulay.py`: manifested multi-prime wrapper around
  `anchor-k-echelon solve`.  Its output remains modular until an independent
  selected-column or rational-ledger verifier passes.
- `export_macaulay_spasm.py`: strict column-JSONL to SpaSM/SMS transpose
  exporter with source, matrix, and RHS hashes.
- `compress_spasm_equations.py`: removes exactly the equation coordinates
  absent from both the matrix and RHS, serializing the sorted row map so the
  compression is auditable and source-level replay remains unchanged.
- `run_spasm.py`: multi-core SpaSM sparse-direct solve wrapper.  It records
  block size/resources and requires `verify_spasm_solution.py` to replay the
  returned vector against the original JSONL before reporting success.
- `verify_spasm_solution.py`: independent source-level modular `A*x=b` replay;
  a verified modular vector is still not a characteristic-zero certificate.
- `linbox_parallel_wiedemann.cpp`: OpenMP CSR black box for LinBox's
  Wiedemann solver; it stores both orientations so `apply` and
  `applyTranspose` are parallel row traversals instead of atomic scatters.
- `run_linbox_wiedemann.py`: manifested Wiedemann wrapper with strict
  orientation/hash guards, process-group cleanup, and the same mandatory
  source-level solution replay as SpaSM.
- `build_linbox_wiedemann.sh`: reproducible Rosetta/x86_64 build against the
  vendored LinBox/FFLAS-FFPACK/Givaro prefix and Homebrew OpenMP runtime.
- `self_test.py`: parser, Rabinowitsch, F4SAT, and staged-elimination must-fires.

The parallel LinBox/Wiedemann binary reports `LinboxError` messages explicitly.
Set `LINBOX_WIEDEMANN_PRECONDITIONER=butterfly` for singular systems whose
leading rank-sized submatrix is not generic.  `sparse` remains experimental
and is not the default; the bundled rectangular toy succeeds with `none` and
`butterfly` but deliberately does not certify `sparse`.

Run the core regression before and after changing the machinery:

```sh
python3 computations/toolkit/groebner/self_test.py
.venv/bin/python computations/toolkit/groebner/self_test.py
```

## Scope fields

Every manifest must state the open chart or branch explicitly (for example,
`pivot != 0`, `Cprod != 0`, or `boundary face only`).  A unit on one localized
chart says nothing about the complementary divisor unless a separate result
closes it.  The current proof ledger relies on this distinction throughout.
