# Round 1262 sequential six-lane portfolio

This clean sibling replaces the nonpromotable parallel portfolio attempts. It uses the sealed round-1261 checkpoint/cache and the already audited tree-capable source/binary. Each of the six fixed strategy/pivot candidates starts from an independent APFS clone and is limited to one round, 120 seconds, and 36 GiB.

Execution starts with cold/rare for continuity, but selection is fail-closed until all six candidates exist. Selection is by the exact production objective `(unseen incident frontier, support size)`, with the original stable task order `repair/{first,last,rare}, cold/{first,last,rare}` as the tertiary tie-break. Failed parallel attempts contribute zero coverage.

Candidate lane output is not a selected continuation state. An exact frontier scorer and all-six assembler must pass before fixed selected replay or cap equivalence is authorized.
