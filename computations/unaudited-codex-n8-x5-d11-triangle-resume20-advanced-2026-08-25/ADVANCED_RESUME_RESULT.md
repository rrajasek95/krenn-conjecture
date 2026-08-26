# Advanced D11 triangle resume result

`PASS_FAIL_CLOSED_COLUMN_CAP_CHECKPOINT_ADVANCED`: the cleared p=1073741827 triangle resume completed normally in 34.1405 seconds and advanced the checkpoint from 230,091 to 307,885 selected columns. Its modular dual grew from support 80,922 to 184,659. Peak watchdog RSS was 7,099,376 KiB, far below 20 GiB.

This is not a mathematical verdict. Round 0 added 77,794 violating columns. On round 1 the engine found 192,116 violations, one more than the 192,115 remaining slots in the frozen 500,000-column cap, and stopped before adding that truncated batch. The exact result status is `INCOMPLETE_COLUMN_CAP`, reason `MORE_VIOLATING_COLUMNS_THAN_REMAINING_CAPACITY`, with `global_modular_dual` and `mathematical_verdict` both null. The watchdog conservatively labels it `FAIL_CLOSED` because that resource status is outside its accepted terminal-result map; the engine return code was zero and all atomic artifacts landed.

The newest restart pair is:

- selected: 307,885 columns, SHA `e3c300a7992e22ffb52e79f84ae4e87a64a4a9951fb2c0794461bf2077e4994f`;
- dual: support 184,659, SHA `eeea4d8278a798ae829f28ac92a70bbdff9b3660144b618835091c470cbcbdea`;
- target coefficient: 1.

An independent Python replay checked strict row/column ordering, provider and coefficient pins, inclusion of all 230,091 input columns, and all 307,885 modular pairings in 17.27 seconds with zero failures. No second prime, other branch, D12 read, or relaunch occurred. `D12_RESOURCE_CLEAR` was reported immediately after replay.
