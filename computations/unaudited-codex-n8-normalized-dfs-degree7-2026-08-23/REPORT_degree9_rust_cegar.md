# Chart-26 degree-nine lazy dual: bounded terminal report

## Outcome

The selected exact degree-eight dual was advanced by one saturation level,
but the degree-nine lazy CEGAR did not terminalize inside the resource gate.
The frozen result is `WALL_CAP_UNRESOLVED`: it proves neither degree-nine
membership nor nonmembership, and it is not a Bockstein obstruction.

## Exact initial boundary

The independently replayed rational `lambda8` has 561 rows and digest

    561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d.

Enumerating every genuinely new multiplier-degree-five incident column gives

    3,111 candidates,
    2,308 nonzero exact boundary pairings.

All violating source labels and rational pairings are in
`results_degree9_initial_census.json`, logical SHA-256

    2c36f6054bacd4654236037849a2dc841b96b6ecb2161f3ee0322734c7ce94b1.

This census is only the boundary of the selected `lambda8`; by itself it has
no degree-nine implication.

## Bounded modular CEGAR

The same literal provider/canonicalization and Rust sparse solver were used
over `p=1,073,741,827`.  Every completed system had full selected rank and
zero target remainder.  The component nevertheless expanded rapidly:

| round | selected/rank | degree-9 rows | extension | new crossings |
|---:|---:|---:|---:|---:|
| 0 | 2,308 | 164,465 | 1,771 | 3,965 |
| 5 | 23,004 | 1,373,719 | 8,687 | 3,694 |
| 10 | 40,623 | 2,350,542 | 11,636 | 3,094 |
| 14 | 51,543 | 2,943,313 | 12,795 | 2,452 |

Round 14 has 3,983,401 nonzeros.  After adjoining its 2,452 crossings, the
checkpoint contains 53,995 selected columns.  Round 15 was stopped before
completion.  The last completed driver time was 536.858 seconds; the process
was interrupted before the external 600-second guard.  The largest sampled
RSS was 10,659,520 KiB (10.166 GiB), below the 12-GiB ceiling.  macOS did not
provide a usable `RLIMIT_AS`, so memory was polled externally.

Because there was neither a zero-crossing extension nor a relative
inconsistency, no exact-Q terminal replay was applicable.  In particular,
full modular rank in the completed prefixes is not a characteristic-zero
theorem.

## Artifacts

- `results_degree9_initial_census.json`: exact initial source boundary.
- `audit_degree9_lazy_dual_cegar_rust.py`: bounded degree-nine driver.
- `results_degree9_rust_cegar_checkpoint.json`: all 53,995 selected columns
  and 15 completed round records.
- `results_degree9_rust_cegar.json`: terminal scope/result packet.
- `package_degree9_cap.py`: deterministic cap-result packager.

The next computational version, if pursued, should retain a persistent
incremental row basis and stream only new column incidences.  Rebuilding the
multi-million-row exposed system each round is the present bottleneck.  That
engineering observation does not alter the unresolved algebraic status.
