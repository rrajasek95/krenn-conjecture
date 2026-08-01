# Archive: orphaned Claude checkers from 2026-08-01

This branch is a provenance archive, not an integration branch. Krenn's
conjecture remains open; none of these files modifies the certified spine.
They were left untracked at commit `c871c2c` when the Claude session ended.

| File | SHA-256 | Trace and status |
|---|---|---|
| `verify_binary_pair_restriction_split_and_null_rows.py` | `c995410071b736bafdecf2e2a457e3f2b4fd2f92f76848e8b27347ea99590117` | Authored by `agent-a958c3a9a371481f2`. Its split, null-row interface, and parity family fed later work, but the rigidity framing was superseded by the stronger independently audited theorem in commit `6a222b6`. Archive only. |
| `verify_h3_cross_colour_terminal_class_vanishing.py` | `1c07d61547935c59edd92bcbea76714593bb5c0cecb9d293ea8fbaf29603879b` | Authored by `agent-a4319830eb6df6e10`. It claims a heavy 160-branch terminal-class closure; the independent audit `agent-a6f5b03003f51fbc5` hit its session limit. Not accepted or replayed here. |
| `verify_three_mode_contraction_slice_boundary.py` | `ff1b14859f1c3cb2c0f9efddc5f9852d4549a14d6585137b1aab953e27ada586` | Authored by `agent-ad7be97d6e75e59d5`. It reconstructs the bound `D <= N-1` and explains why slice rank is saturated at `(8,3)`; useful negative-route evidence, not progress on the remaining case. |
| `verify_universal_support_rules_at_eight.py` | `fa6eba08a535ffea15d29a5f7cc8db1b6a9f110ee16671857677bd414100f9cb` | Authored by `agent-aac438e5301d9721e`. R1 and R2 are sound hand theorems at eight vertices; R3 is superseded by `slice-cover.md`. The file checks ingredients rather than the quantified implications and overlabels them as machine-proved. Archive only. |

The main integration branch contains a separate lightweight proof and checker
for the R2 consequence actually consumed by the level-two differential route.
Do not merge this archive wholesale; promote an individual artifact only after
a fresh independent audit and an explicit status correction.
