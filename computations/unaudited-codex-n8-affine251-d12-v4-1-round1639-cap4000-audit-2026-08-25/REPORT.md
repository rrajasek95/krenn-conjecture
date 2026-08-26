# Independent D12 round-1639 chain audit

Status: **PASS_EXACT_ROUND1639_CAP4000_CHAIN**.

The accepted cap-equivalent round-1627 state is an exact ancestor of all twelve one-round states 1628 through 1639. The independent single-pass scanner checked all 12 checkpoint and cache-descendant edges, byte equality of every inherited vector, the complete final candidate against all 3,968,369 cached columns (403,999,306 terms), target normalization, and zero pairings. It reported zero failures in 28.515606 seconds. The final endpoint was independently rehashed as checkpoint `ab63c22095dd44d771525af9ba218ee36c9e6f4236a80addbc15692165c531a5` and cache `4d342801fa9e6d25aff95d7b1172f5bff803e8436c01f9237b79e5a42bf6999e`; its support is 32,704.

The exact exceptional set is fail-closed: cooperative top-of-loop native overshoots only at stages 06/r1633, 07/r1634, 11/r1638, and 12/r1639; a sole exact-target `WALL_CAP` state at stage 08/r1635; and a refused stage-09 wrapper attempt with only an unchanged clone and zero result/watchdog/log outputs or coverage. All accepted states passed their hard wrappers atomically below the applicable 150/180-second limits and below 36 GiB. Generic native-limit and status relaxation are both false. The five provenance block sums are 342.493546, 359.461065, 408.832617, 303.108930, and 167.219453 seconds, each below 540 seconds; they are not treated as single-run wall times.

The frozen original plan reconstructs byte-for-semantics from the final plan by exactly the recorded amendments: growth bounds 25k→40k after r1632, 40k→50k after r1636, and 50k→75k for r1639 only; the r1635-only status/resource exception and 120/150→150/180 resource transition; and the storage compaction. The wrapper source diff is exactly bound 155→540 plus matching error text. Producer ledger/report/manifest are pinned at `7c56ae5e...`/`eb548022...`/`8d95f913...`.

Scanner source/binary are pinned at `8593fb69a16c8348f171c1d4423c8fd361aa2f165eaaf801ac893ae4894aa1b1` and `9d86e743658d6f9e9cc5a653a4fc4521f3d47c47a77ec47130526e7fcf63da9e`. This audit accepts an exact nonterminal r1639 search state only. It makes no r1640, closure, or conjecture claim.
