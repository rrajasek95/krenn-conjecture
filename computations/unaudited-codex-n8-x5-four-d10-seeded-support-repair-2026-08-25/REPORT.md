# Exact seeded D10 transport/repair gate for the four frozen X5 branches

## Outcome

PASS. Each of the direct, triangle-endpoint-colour, third-colour, and cap-endpoint-colour branches has an explicit characteristic-zero homogeneous degree-10 dual with value 1 on `t^10` and value 0 on every degree-10 generator multiple. Therefore `t^10` is not in the frozen branch ideal in degree 10 for all four branches. This is a degree-10 statement only; no D11 computation was launched and this package does not assert an all-degree induction.

## Exact construction

The four sealed D9 integer duals were transported by appending `t=361` to every supported row. Literal source replay against the pinned 361-variable/6,571-generator providers found 58 initial violations for direct and 54 for each coloured branch. Every offender was a t-free generator multiple. Those exact columns formed the only initial repair checkpoint.

The fixed-width Rust engine incrementally inserted globally violating columns and recomputed a target-normalized dual over `p=1073741827`, with per-branch gates of 180 seconds, 8 GiB, and 200,000 selected columns. All four closed. Only then was the identical source-independent checkpoint run over `p=1000000007`. The two runs produced equal selected-column sets, equal supports, and identical signed small-integer maps.

The signed maps lift directly to primitive integer certificates. An independent Python parser then enumerated every generator multiple incident to the certificate support, replayed all integer pairings, and checked the modular reductions at both primes. Nonincident columns are identically zero because none of their rows belongs to the support.

| Branch | Transport violations | Selected | Integer support | Weights | Incident columns replayed | p107 / p100 wall (s) | Peak RSS KiB |
|---|---:|---:|---:|---|---:|---:|---:|
| direct | 58 | 4,316 | 243 | -1,1 | 326 | 44.587 / 38.802 | 1,209,168 |
| triangle endpoint colour | 54 | 1,678 | 251 | -2,-1,1,2 | 348 | 3.980 / 4.144 | 342,992 |
| third colour | 54 | 1,588 | 253 | -2,-1,1,2 | 350 | 3.957 / 4.014 | 338,560 |
| cap endpoint colour | 54 | 1,557 | 247 | -2,-1,1,2 | 341 | 3.907 / 4.072 | 339,312 |

Exact certificate hashes, in branch order, are:

- direct: `c639faa986903b66d003dc4513bb9ad029f5b0027dd15714d8c5449a494c8246`
- triangle endpoint colour: `67daf29cdbf5e2919441f1227c01b933f37ac7dfe6e832a5d09779218d758174`
- third colour: `5a9e86a19980b77da51925b4d78be2c198aa3c7ef9f41a3ffc92ac016551517d`
- cap endpoint colour: `d90a6270359cbf79520caff7be64b1a4f99f3b66d9a8aa630e850dde3ee9f567`

## Fail-closed validation

`validate.py` is independent of the Rust solver and re-parses the physical providers and certificates. Standard and `python3 -I -S` executions emitted byte-identical audit SHA `399b86e7e2625806db294f1b8a1203cffef078639f11c7892fd47359061998c0`. Eight hostile tests reject a wrong schema, unsorted row, duplicate row, zero target, coefficient magnitude 3, wrong modular reduction, wrong provider hash, and optimized execution with assertions disabled.

`results_final_audit.json` is the strict cross-artifact summary. `INPUT_PINS.json` freezes source providers, D9 certificates, replay code, watchdog, engine source, and binary. `MANIFEST.sha256` covers the package plus explicit external inputs and is verified fail closed.
