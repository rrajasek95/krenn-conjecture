# Independent D12 round1161→1261 chain audit

Status: `PASS_EXACT_FULLY_TELEMETERED_ROUND1261_CHAIN`.

The sealed round1161 portfolio/cap gate was independently pinned first: manifest `d05e1ff544bae130ca960fd1fc6c454f96bb137953d21a3d27628026dc2f44f0`, checkpoint `e7d53052997394ee43d110ead3b74d72cba97773df9076a5eff7dab8033d143a`, and cache `0df2928faf351531f04b936afc06d6a7d8a105f9330ef7200322ca78f257e6c3`. The production chain then covers exactly rounds 1162 through 1261 with no gap across ten stages.

Every checkpoint is a strict descendant of its predecessor and every inherited cache record is byte-identical. The chain grows from 961,803 to 1,238,541 columns. The final candidate has support 1,065 and target coefficient 1. Independent replay checked all 1,238,541 cached columns / 126,329,382 terms with zero pairing failures.

Both predeclared resource blocks pass: 496.679810 s and 428.310805 s, each below 540 s. Maximum sampled RSS was 14,755,360 KiB, below the 37,748,736 KiB limit. All ten watchdog-v2 records pass, retain source/binary/watchdog pins, and report atomic clean outputs.

Authoritative terminal artifacts:

- result: `2eb3788e5559d6dccf73164c95029f12e6f7371443e6b0f79f3d7d6a3d5be4e7`
- checkpoint: `6fb20b1c7f87674fe97b36995c4d9f92b1df9ed67728fdcf1ef483cdaa0c7a01`
- cache: `a1cf70310c0cc8507a922fd82456d3a29b073b2aa3d649d1bc91d4a3dbfd7792`
- watchdog: `6881434c19ca0658b147841edaad404321a3885fc90289613e765b0190362cce`

Scope caveat: round1261 ended at `INCOMPLETE_SEARCH_CAP / ROUND_CAP`. This is an exact, fully replayed, resumable state; it is not a terminal global dual and does not by itself settle the conjecture.
