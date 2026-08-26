# Read-only storage audit at accepted round 1636

Status: `PASS_READ_ONLY_RECOMMENDATION_AWAITING_EXPLICIT_DELETION_AUTHORIZATION`

No file was deleted, moved, truncated, or modified by this audit. No stage 10
directory was created and no arithmetic was launched. The accepted live chain
`production_from_round1627_cap4000_to1639`, its round-1627 input
`round1627-direct-cap4000-gate/candidate_cap4000`, all audit/report/manifest
evidence, and unrelated symbolic gates are excluded.

## Hold and live endpoint

- Filesystem free space at audit: `75,839,308 KiB`.
- Frozen prelaunch reserve: `75,497,472 KiB`.
- Margin: `341,836 KiB`; therefore stage 10 remains forbidden.
- Accepted endpoint: round `1636`, columns `3,798,271`, support `15,825`.
- Endpoint checkpoint SHA-256:
  `5f29efd99b81830a3aea35707ff91acc7847d0d86b1bc4277c9b076794ebd1a9`.
- Endpoint cache SHA-256:
  `8553a5bff1404d882bd604987bf15ecc1c548677411e6a64e32ac1d78b3e09e9`.
- Amendment 3 SHA-256:
  `fd535a1f686524a077c969260548c3b19b2bcfa72b1e58928b3adaf4050e0153`.

## Ranked obsolete payload candidates

All sizes below are exact logical byte sizes from `stat`. Only the named
`checkpoint.bin` and `vectors.bin` files are candidates; all small evidence
must remain.

1. Failed external portfolio lane, zero accepted coverage — `4,475,643,285`
   bytes (`4.168268 GiB`):
   - `computations/unaudited-codex-n8-affine251-d12-round1464-external-sequential-six-cap2500-design-2026-08-25/lane00_repair_first/checkpoint.bin`
     (`30,793,148` bytes)
   - `computations/unaudited-codex-n8-affine251-d12-round1464-external-sequential-six-cap2500-design-2026-08-25/lane00_repair_first/vectors.bin`
     (`4,444,850,137` bytes)
   - Basis: failure audit SHA-256
     `a7d9b04d0b58c4f3b74710918b460bfd02495854e501d70f6f5e93fd553e6920`,
     status `PASS_FAIL_CLOSED_ZERO_PORTFOLIO_COVERAGE`, result absent.

2. Failed original round-1447 stage 15, explicitly classified safe to remove —
   `4,250,770,352` bytes (`3.958838 GiB`):
   - `computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1363_portfolio_cap2000/stage15/checkpoint.bin`
     (`29,599,730` bytes)
   - `computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1363_portfolio_cap2000/stage15/vectors.bin`
     (`4,221,170,622` bytes)
   - Basis: `FAILURE_EVIDENCE.json` SHA-256
     `98e0e7993007bf14b9fd96a32c1548f410fa325943f92fc1ff7b75b4a2175472`,
     status `REJECT_NO_SPACE_DURING_ATOMIC_CACHE_WRITE`, no result and no
     accepted coverage. Recovery attempt 2 and the later round-1447 chain are
     independently sealed by audit `63e65b41...` and manifest
     `a60825d7f5c80b47ce3f74249a1727928cdec76559ae01fcc8ebc5e90bf71cd1`.

3. Superseded accepted round-1363 cap-2m restart — `3,463,076,480` bytes
   (`3.225241 GiB`):
   - `computations/unaudited-codex-n8-affine251-d12-round1363-internal-sequential-portfolio-cap2000-design-2026-08-25/cap2000_candidate/checkpoint.bin`
     (`23,854,415` bytes)
   - `computations/unaudited-codex-n8-affine251-d12-round1363-internal-sequential-portfolio-cap2000-design-2026-08-25/cap2000_candidate/vectors.bin`
     (`3,439,222,065` bytes)
   - Basis: producer audit SHA-256
     `8c55b66916dcfc14fc27a51cb7337bfe37e4ef32b65cb9bf3ca8ccba01d1ee11`;
     its descendants through round 1447 are independently sealed by manifest
     `a60825d7f...` and have much later accepted descendants.

4. Superseded round-1342 production endpoint — `3,254,055,026` bytes
   (`3.030575 GiB`):
   - `computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1262_portfolio_cap1500/stage10/checkpoint.bin`
     (`22,418,438` bytes)
   - `computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1262_portfolio_cap1500/stage10/vectors.bin`
     (`3,231,636,588` bytes)
   - Basis: independent round-1342 audit
     `bd17df8241623848ad52244de8a53f6bfd06c1541909b0d56e9a1cf09606e248`
     and manifest
     `7dea99f68ab4d5e04be287b6e382165b679ca29e8271001400152c6c01c33d20`.

5. Three byte-equivalent, superseded round-1262 portfolio/cap states — each
   `2,705,013,604` bytes (`2.519240 GiB`), total `8,115,040,812` bytes:
   - `computations/unaudited-codex-n8-affine251-d12-round1262-internal-sequential-portfolio-cap1500-2026-08-25/selected_control/{checkpoint.bin,vectors.bin}`
   - `computations/unaudited-codex-n8-affine251-d12-round1262-internal-sequential-portfolio-cap1500-2026-08-25/portfolio/{checkpoint.bin,vectors.bin}`
   - `computations/unaudited-codex-n8-affine251-d12-round1262-internal-sequential-portfolio-cap1500-2026-08-25/cap1500_candidate/{checkpoint.bin,vectors.bin}`
   - Per directory: checkpoint `18,635,867` bytes, cache `2,686,377,737`
     bytes. Basis: producer audit SHA-256
     `29d0b05b2ebca3c686a90276d9b881eb8c6c8f583169322b74bcef2dce0c0c1f`,
     status `PASS_EXACT_INTERNAL_SIX_PORTFOLIO_AND_CAP1500_EQUIVALENCE`, plus
     the independently sealed round-1342 descendant above.

6. Two byte-equivalent, superseded round-1343 cap-gate states — each
   `3,263,574,137` bytes (`3.039440 GiB`), total `6,527,148,274` bytes:
   - `computations/unaudited-codex-n8-affine251-d12-round1343-cap1750-gate-2026-08-25/cap1750_candidate/{checkpoint.bin,vectors.bin}`
   - `computations/unaudited-codex-n8-affine251-d12-round1343-cap1750-gate-2026-08-25/cap1500_control/{checkpoint.bin,vectors.bin}`
   - Per directory: checkpoint `22,483,538` bytes, cache `3,241,090,599`
     bytes. Basis: cap-gate manifest SHA-256
     `c07168d65ba9caa604bf38235b4ff9f5442b217fd82934c84f18f4f0c9665e9b`;
     the accepted candidate's descendants through round 1362 are independently
     sealed by audit `7386c9d8...` and manifest `ab0d32a9...`.

The enumerated set is exactly 18 files totaling `30,085,734,229` logical bytes
(`28.019523 GiB`), exceeding the requested `24 GiB` logical threshold.

## Safety and recovery caveat

APFS clone sharing means logical bytes are not a promise of equally large
physical recovery. If deletion is explicitly authorized, enumerate these same
18 paths again, verify the cited small seals first, delete only the exact files,
record pre/post `df`, append the central compaction ledger, and rehash the live
round-1636 endpoint. Continue only if post-delete free space exceeds the frozen
reserve by enough for three complete output/cache clones plus audit scratch.
