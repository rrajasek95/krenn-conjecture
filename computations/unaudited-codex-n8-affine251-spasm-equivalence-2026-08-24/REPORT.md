# Bounded SpaSM exact-equivalence gate

Status: **D10 PASS; D11 gate failed closed; D12 not launched.**

This is a new sibling package. It did not edit or replace the retained
`unaudited-codex-n8-affine251-orbit-membership-2026-08-24` package.

## D10 accepted result

The exporter rebuilt the complete orbit matrix from the retained provider and
complete D10 checkpoint, in the orientation `A^T` required by SpaSM's left-hand
solver.  The exact integer lift has maximum absolute coefficient 1440, safely
below half of either pinned odd prime.

- shape of `A^T`: 2,120 by 36,475
- nonzeros: 101,283
- primes: 1,073,741,827 and 1,073,741,789
- SpaSM rank at each prime: 2,014, exactly matching the retained validator
- target: inconsistent/nonmember at each prime, exactly matching the retained
  validator
- retained separating dual at each prime: support 114, all 2,120 exported
  columns annihilated, target pairing 1
- SpaSM wall time: 0.210 and 0.212 seconds; cumulative child peak RSS recorded
  by `getrusage`: 177,602,560 bytes
- hostile equivalence checks: 6/6 rejected

The authoritative machine result is `results_spasm_equivalence_d10.json`,
SHA-256 `37f6243afb8187cb9636f827fff49825ca8f1b178b28f2409a3cfa3be2ff7394`.

## D11 stopped result

The exact export itself completed within the bounded gate:

- shape of `A^T`: 195,924 by 3,722,556
- nonzeros: 18,713,801
- exporter wall time: 268.459 seconds
- matrix size: 301,126,467 bytes
- matrix SHA-256:
  `19b5773339a74e2ff68d794ba7ac20acc846cc3643557fc20d493551dbc29983`

An independent streaming pass checked all 18,713,801 entries against both
retained D11 separating duals. Each support-7 dual annihilates every exported
column and pairs to 1 with the target. This verifies the exported interface and
the retained nonmembership witness; it is not a SpaSM rank result.

The D11 gate's 300-second limit is end-to-end. The exact export consumed
268.459 seconds, leaving only 31.541 seconds; acceptance was therefore already
impossible when a separately bounded SpaSM diagnostic began. SpaSM's default
greedy alternating-cycle pivot search had processed 40,454 of 195,924 rows
after about 194.204 diagnostic seconds, for a linear projection of about
940.554 seconds, and was terminated. No D11 solution file exists, the second
prime was not started, and no SpaSM rank/residual/equivalence claim is accepted
for D11. External `ps` samples were below 0.4 GiB, but no formal peak RSS trace
was captured for this incomplete diagnostic.

The fail-closed machine record is
`results_spasm_equivalence_d11_gate_failure.json`, SHA-256
`ad89afbbeb0fccf653bebee2e1ec9aab3cec1171d39c4de4f850bb22d6af8280`.
The final strict audit rejected 9/9 hostile mutations, including forged D11
PASS, rank, solution, dimension, and dual claims.

## Source and scope controls

The exporter binary is SHA-256
`58392b53606a5a64eece7faadacfe1bafe29c182bbfcae604411c2c525260b54`.
It embeds the build-time retained source whose original SHA-256 was
`241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`;
the sanitized build snapshot is pinned in the manifest. The live retained
source was edited by another task after the exporter build, so this package
does not silently recompile against or claim equivalence to that later source.

SpaSM source, binary, provider, checkpoints, retained results/duals, the
build-time source snapshot, exported matrices, logs, results, and auditors are
pinned by `MANIFEST.sha256`. The vendor SpaSM checkout was used read-only at
commit `09c40943f1d4b754f89fb97fc9ddf2b8e53e967e`; it already contained unrelated
local CMake modifications. No D12 elimination was launched.
