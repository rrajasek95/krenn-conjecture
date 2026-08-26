# Held D11 cap-750k continuation

`PASS_HELD`: the next exact continuation is frozen from the independently replayed 307,885-column / 184,659-support triangle checkpoint. It has no clearance file and no output directory, and its launcher was hostile-tested to refuse execution.

The sole engine-source change from the accepted parent is the checked column-cap ceiling `500,000 -> 750,000`. Prime, provider, branch, arithmetic, 590-second native wall, comparator, checkpoint writes, and all other source bytes are unchanged. The watchdog changes only from 20 GiB to 24 GiB, retaining the 600-second wrapper.

The parent peak was 7,099,376 KiB at 307,885 selected columns. A deliberately simple column-linear projection gives about 17.3 GiB at 750,000 columns and about 21.6 GiB with a 25% margin, below the 24-GiB cap. The parent exposed 192,116 next-round violations, while the new cap leaves 442,115 slots from the seed. Both figures are diagnostics only because rebuilding changes the frozen pivot order, but they support a feasible bounded continuation rather than a preflight rejection.

Launch remains blocked until the r1538 audit/compaction is sealed and explicit clearance names this package manifest. No arithmetic or D12 read occurred during preparation.
