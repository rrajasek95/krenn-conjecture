# D12 r1641 cap4.75/support200k resource retry — HELD

Status: **HELD_AWAIT_INDEPENDENT_RESOURCE_REFEREE_AND_EXPLICIT_MANAGER_CLEARANCE**. No retry clone or arithmetic has been launched.

Attempt1 is sealed `REJECT_HARD_WALL_ZERO_COVERAGE`: the external watchdog killed it at 241.229560s, with no result, dual, temporary output, or changed checkpoint/cache. Peak RSS was 18,523,808KiB; the last sample at 240.167356s was only 2,688,096KiB. This low-RSS tail is consistent with finalization but does not prove mathematical completion. Attempt1 is evidence only and cannot be resumed or reused.

The proposed retry changes exactly two resource literals relative to attempt1: native wall 210→300 seconds and hard wrapper wall 240→360 seconds. Source `3139689f...`, binary `79410bc8...`, watchdog implementation `75bccbb6...`, provider, prime, cold/rare/hierarchical/16/nonincremental mode, cap4.75m, support200k, RSS36, and target r1641 are unchanged.

Native300 leaves 58.77044s beyond the observed hard-wall path (about 24%); wrapper360 reserves another 60s for atomic publication. A hard wrapper or RSS breach remains a rejection, and this is not a generic wall relaxation.

If independently approved and manager-cleared, retry2 must be a distinct fresh audited-r1640 clone named `candidate_r1641_cap4750_support200k_retry2`. Acceptance still requires atomic `ROUND_CAP` at exactly r1641, no r1642, all 4,069,711 inherited records byte-identical, strict checkpoint descendant, and full replay target 1/zero failures. Any cap or resource result is zero coverage and held fail-closed.

The 96GiB preclone floor and exact input rehash remain mandatory. Attempt1 payloads and all small evidence are protected; no deletion or continuation is authorized.
