# Chart-26 degree-eight lazy dual: exact terminal report

## Theorem

On the frozen normalized chart 26, the exact degree-seven functional extends
to a rational functional `lambda8` satisfying

    lambda8(t^8) = 1,
    lambda8(m F_w) = 0

for every mixed source word `w` and every normalized multiplier whose output
degree is at most eight.  Therefore `t^8` is not in the degree-eight
homogeneous mixed ideal over `Q`.

This is a chart-relative, degree-bounded theorem.  It does not decide degree
nine or unrestricted `t`-saturation.

## Computation

The digest-pinned Python source provider was retained literally.  A new Rust
sparse solver performs the same least-column-pivot elimination modulo
`p=1,073,741,827` and transports the solution back to source-labelled top
rows.  Rounds 0 through 10 and round 47 match every frozen count exactly.

The CEGAR terminalized at round 197:

    selected columns       3,097
    exposed degree-8 rows 147,521
    nonzeros               226,338
    rank                    3,097
    modular extension         512 rows
    incident new columns      696
    new violations               0

The modular terminal was then replayed with the original exact `Fraction`
solver.  The resulting functional has 561 rows: all 49 frozen degree-seven
weights plus 512 degree-eight weights.  Its record digest is

    561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d.

The independent verifier re-enumerates all 752 bounded incident columns
(multiplier-degree histogram `1,3,6,46,696` in degrees `0..4`) and obtains
zero nonzero pairings.  A hostile mutation of the lexicographically first
degree-eight weight creates the literal crossing

    word 56, multiplier 02061ec0, pairing 1.

## Artifacts and replay

- `results_degree8_rust_cegar.json`: exact functional and the 198-round ledger.
- `results_degree8_rust_cegar_checkpoint.json`: all 3,097 selected source columns.
- `results_degree8_rust_cegar_replay.json`: independent exact replay and mutation.
- `src/bin/degree8_modsolve.rs`: sparse modular solver.
- `audit_degree8_lazy_dual_cegar_rust.py`: provider/CEGAR/exact terminal replay.
- `verify_degree8_rust_cegar_result.py`: independent exact verifier.

Replay:

    cargo build --release --bin degree8_modsolve
    uv run python verify_degree8_rust_cegar_result.py

The second command completes in about one second after the terminal result is
present.  The attempted 12-GB `RLIMIT_AS` was unavailable on this macOS host;
no peak-memory claim is made.  The combined modular discovery prefix and
resume took about 101 seconds, and the exact terminal replay about 17 seconds.
