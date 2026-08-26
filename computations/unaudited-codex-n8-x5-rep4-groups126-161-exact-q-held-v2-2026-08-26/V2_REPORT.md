# Rep4 final 36 exact-Q executor v2

Status before launch: **compatibility-repaired / same 36 ideals / zero runs**.

The original final-batch package expected an obsolete first-batch status and `groups_closed` field. This package changes only that provenance interface: a sealed alias replays the first-batch terminal proof and maps `unit_groups_closed` to `groups_closed`. Groups 26–75 and 76–125 are replayed directly. The exact sources, strict order 126–161, 240/250-second limits, 8-GiB cap, and stop-first rule are unchanged.
