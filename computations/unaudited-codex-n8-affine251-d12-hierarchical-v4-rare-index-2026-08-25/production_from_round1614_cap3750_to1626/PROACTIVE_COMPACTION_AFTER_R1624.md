# Proactive compaction after round 1624

Status: PASS

The round1624 endpoint passed exactly but free space (67,060,452 KiB) fell 48,412 KiB below the frozen64 GiB proactive hold. No current-chain payload is in scope.

Old seals independently revalidated before deletion:

- round950 audit `8e60e9d33483bd493d1e16b4664382ecb56a62db4b4a10b71236b600a5e20c6e`, replay `96cc92350d475b286abde2e9f44889a018d5da1a261ff42cb1ea3b167e0965e7`, manifest `1e61b818d9a8aa85488a4b90a2f68934b65696fe2f4870764ef7942d78ca0ae0`;
- round849 audit `156b55fc8f86c2f842d02875854e15f0d81ec3d9236b8c33a8c2fe40a2f9743e`, replay `a2ea0f27800bf2d46b0367cf6e7eb5a9dba93af74f2d9400bd4a772cbc60046c`, manifest `30be587a44928b418ff51a6fa58791eff90f168a542c22e4d603e7fad72177d8`.

Exactly18 old payload files totaling9,338,455,391 bytes are authorized:

- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage01/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage01/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage02/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage02/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage03/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage03/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage04/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage04/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage05/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round850/stage05/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage01/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage01/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage02/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage02/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage03/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage03/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage04/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage04/vectors.bin`

Pre-deletion accepted endpoint pins:

- result `0dfc91c00bf08b23eaa738e0035fa9573916cb3b882fb8c207339a8e5b16ff74`
- watchdog `f24d07a42df4834118d467a0e9ee4e8b40aba5876583e8596e54a3da57c237f7`
- checkpoint `f0003d41b2f49fb5d40fa693fc9d0210dc3cbc05ff3e043b1836f968d0482b87`
- cache `a3c43d2bd49e375bab777d365e3662401ca6356e90cec496b5489d0b1123d237`

Post-deletion verification:

- all18 enumerated old payload paths are absent;
- free space increased from67,060,452 KiB to76,189,220 KiB;
- result rehash `0dfc91c00bf08b23eaa738e0035fa9573916cb3b882fb8c207339a8e5b16ff74`;
- watchdog rehash `f24d07a42df4834118d467a0e9ee4e8b40aba5876583e8596e54a3da57c237f7`;
- checkpoint rehash `f0003d41b2f49fb5d40fa693fc9d0210dc3cbc05ff3e043b1836f968d0482b87`;
- cache rehash `a3c43d2bd49e375bab777d365e3662401ca6356e90cec496b5489d0b1123d237`.

The accepted round1624 state is unchanged and the64 GiB proactive launch gate is restored.
