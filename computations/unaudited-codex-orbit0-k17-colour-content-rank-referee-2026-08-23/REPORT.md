# K17 colour-content first-shell rank referee

Tail's corrected literal target-rooted first shell contains `100,000` distinct mixed-source completion vectors on `16,412` colour-content coordinates (`6,800` original target coordinates plus `9,612` exposed exterior coordinates).  It stopped at the profile cap after visiting `4,690,558` literal columns from `139,818` target rows, so every conclusion below is strictly a partial-shell statement.

## Modular rank

| prime | rank | target-augmented rank | target in span | reduced target support |
|---:|---:|---:|---|---:|
| 32003 | 10,917 | 10,918 | no | 4,612 |
| 32009 | 10,917 | 10,918 | no | 4,612 |

The two fully reduced modular remainders have the same `4,612` coordinate labels.  The labelled common support is in `target_remainder_common_support.tsv` (SHA `1813af0fffbe28c545e5110975c2c86a9ca241e44a6ca095f2bea676e4c4c1c0`).

## Guards and scope

- Source vectors are literal mixed-word K17 same-filtration completion vectors, not an abstract superset.
- Corrected anchor list `[0,4,8,117,121,125,198,202,206,243,247,251]` is pinned by the producer against the frozen structure.
- Input coordinate/vector hashes are `10ebfdcf...` / `f642f9b0...`; the retracted anchor-mismatched files were not consumed.
- Optimized and unoptimized Rust ranks/remainders agree.  Standard, `-O`, and `-I -S` audits pass with logical digest `45ef6f5c11690deb18bd20cf19f16c54dd2003263f6ec9c3f1eb7aba7dc4b8ac`; hostile rank mutation fails.

This does **not** prove rational nonmembership or nonmembership in the complete literal shell.  It establishes only two-prime rank and nonmembership in the capped first-shell quotient.

