# Independent r1448 cap-2.25m equivalence audit

Verdict: `PASS_EXACT_CAP2000_TO_CAP2250_EQUIVALENCE`.

The control (`--column-cap 2000000`) and candidate (`--column-cap 2250000`) resumed the same independently sealed r1447 state and produced exactly the same r1448 checkpoint and vector cache. After output-directory normalization, the only command difference is the column-cap literal. Both watchdogs report atomic PASS with no breach under 115 seconds and 36 GiB; the maximum observed elapsed time was 58.634889 seconds and maximum RSS was 23,594,320 KiB.

The common endpoint is r1448 with 1,974,608 columns, support 2,131, and target pairing 1. It added 4,286 columns and selected `cold/rare`. The common checkpoint SHA-256 is `4a4ceb16738127a41af8f783265f745cccbf849b827f97d7e0618e609cf3055a`; the common cache SHA-256 is `829028724fb39e37fd9ffb07d5d85094515a0a84e8634307fab17c2833e45007`.

This certifies only the cap-parameter equivalence for the one-round r1447→r1448 transition. It does not assert closure, global completion, or any later-round result.
