# D11 triangle 16-GiB resume result

`PASS_FAIL_CLOSED_CHECKPOINT_ADVANCED`: the single cleared p=1073741827 triangle resume stopped at the 360-second wrapper wall after 360.177739 seconds. Peak RSS was 15,308,688 KiB, below the 16-GiB cap. The process was terminated with no `result.json`, so this is not a modular or characteristic-zero mathematical verdict.

The checkpoint advanced substantially:

- seed: 94,526 selected columns and dual support 13,116;
- newest: 230,091 selected columns and dual support 80,922;
- added: 135,565 selected columns;
- selected SHA: `9c70caaf26b71345b03565dbdf2edba8c52f06eca4ad74d6e7b888fa8a49cca5`;
- dual SHA: `06ded311e326a66105d69ae7be2eb56c7ba9720ab19718f7cd173c09efb2ce02`.

An independent Python parser pinned the provider, checked strict column/row ordering and coefficients, proved every one of the original 94,526 columns occurs in the new selected set, verified target coefficient 1, and literally replayed all 230,091 selected-column pairings in 11.17 seconds with zero failures. No global incident scan was performed, so the new dual is a restart certificate only.

No second prime, other X5 branch, D12 computation, or post-resume arithmetic was launched. `D12_RESOURCE_CLEAR` was reported immediately after the independent replay terminated.
