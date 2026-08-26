# D12 v4.1 short production: round 1484 to 1504

Verdict: **PASS_PRODUCER_HELD_FOR_INDEPENDENT_AUDIT**.

Starting from the independently accepted round-1484 state, five atomic cold/rare hierarchical stages cover exactly rounds 1485–1504. All watchdogs passed under 36 GiB. Aggregate watchdog time is 522.860128 seconds, below 540 seconds; maximum observed RSS is 25,914,336 KiB.

The final round-1504 state has 2,256,332 exposed columns and support 2,705. Its checkpoint SHA-256 is `10807f9505b37832a29d17be7b02b4ac295db5e6fda4b11140c5d2e54b0e8a52`; its cache SHA-256 is `2e52546ad403df0b5c45151f34350025fd3fe85262a8aa5423dff4cb3d31ccfd`.

Production is held at the requested target pending independent five-edge descendant audit and final-cache replay.
