# D11 triangle p107 recovery result

The cleared recovery stopped fail-closed at the 12-GiB RSS boundary after 255.671 seconds. Peak observed RSS was 12,626,848 KiB. No `result.json`, modular terminal claim, second-prime run, other-branch run, or D12 run exists.

The periodic checkpoint mechanism preserved a restart-safe pair:

- 94,526 selected columns, SHA `1f70a3220d6091e0877fd00d86c6ff9f06f25789e03cc854556e6d7ae34fb2a7`;
- modular dual support 13,116, SHA `a91f2be59901b4f29c09f64845e700fb40d7f15181bcd7ac8df89022d4e39d93`;
- target coefficient 1.

`validate_checkpoint.py` independently parsed the frozen provider and replayed all 94,526 selected-column pairings in 5.007 seconds with zero failures. This proves only that the pair is a valid restart checkpoint; no global incident scan was performed and there is no mathematical D11 verdict.
