# D11 triangle-dual cross-branch transport diagnostic

Status: **PASS exact bounded diagnostic; negative small-repair verdict.**

The sealed triangle `p=1073741827` dual from production manifest
`a41b060659d86a3fbd908a8f2241b0bf6b52fe0f57bd7ce1f253482412fb0232`
was transported literally to the two unresolved coloured providers.  All three
providers have the same ordered 361-name header (header SHA-256
`9cbfbc5e67f636b7ebf80dbea1a3d036d583b859c47b14e8b02c74adee2c06df`),
so this is an exact identity-coordinate transport, not a guessed permutation.
The source dual has 184,659 nonzero rows; its `t^11` coefficient is already 1,
so the exact normalization factor is 1 in both target branches.

## Exhaustive incident results

| target branch | incident columns | violating columns | violation-row union | new rows | support union violation rows | wall | peak RSS |
|---|---:|---:|---:|---:|---:|---:|---:|
| third colour | 411,275 | 208,088 | 21,331,925 | 21,230,547 | 21,415,206 | 19.09 s | 2,450,368 KiB |
| cap endpoint colour | 411,275 | 208,088 | 21,332,929 | 21,231,551 | 21,416,210 | 16.78 s | 2,450,272 KiB |

Each incident count is an exhaustive deduplicated scan of every target-provider
column incident to the transported nonzero support.  Materialized columns were
discarded after pairing; only violating column keys and the exact violation-row
union were retained.  Both watchdogs passed the 120-second/4-GiB bounds.

## Load-bearing verdict and scope

Neither transport yields a *small* support-repair system.  Each has 208,088
violation equations, exceeding the frozen 100,000-column solve gate, and adding
their rows would expand the allowed set from 184,659 to more than 21.4 million
rows.  Therefore modular consistency of those large systems was deliberately
not evaluated.  This is a negative feasibility diagnosis, not a proof that the
large systems are inconsistent.

No repair dual was emitted.  No second prime, general CEGAR round, global-dual
claim, D12 cache read, or degree-12 computation occurred.  In particular, this
package does not turn the incomplete triangle checkpoint into an obstruction
for either other branch.

## Pins

- source dual SHA-256: `eeea4d8278a798ae829f28ac92a70bbdff9b3660144b618835091c470cbcbdea`
- triangle / third / cap provider SHA-256:
  `06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c`,
  `b5ce054d529a5390c366254d08e43595cfa16e04854514f80db1b34f109d4ae8`,
  `d040d1525989588bce3b912413aa6841869de63575bb3ebf976de817869e0b64`
- diagnostic source / binary SHA-256:
  `dbed9910aa791c59e6077a3064dfd9777f92831eb3315a4772d7ded310267d97`,
  `3cb03b9276dfacf5b877428242c15048c27d14e5da73af158a78783db4ae5efa`
- result SHA-256 (third / cap):
  `eac216731bf6aafa48e27e18f2d12b60a1c7368562e1cc046f1537d1571c3bb9`,
  `04ce560286dcd3006871b09bde786d655610c1fde98a56a8bb2aaa13236fd03c`

`results_audit.json` independently checks all input/code pins, literal source
dual normalization, coordinate-header identity, result schemas/counts, watchdog
bounds, absence of repair output, and six hostile mutations.
