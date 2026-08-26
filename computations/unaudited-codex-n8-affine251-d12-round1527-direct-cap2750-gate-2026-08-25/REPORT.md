# Round 1527 direct cap gate plan

This is an isolated one-round cap-equivalence gate, not a portfolio or continuation run. It remains held until the round1526 endpoint is independently sealed.

The control and candidate will run sequentially from distinct fresh clones of the exact same round1526 checkpoint/cache. All mathematical and resource settings are fixed; only `--column-cap 2500000` versus `2750000` differs. Promotion requires byte-identical round1527 checkpoint and cache, equal semantic fields after path/timing/cap normalization, and independent audit acceptance.

Both lanes are now complete and producer checks pass. They reached round1527 with 2,400,337 columns and support 3,389. Checkpoints and vector caches are byte-identical; normalized non-timing result semantics agree, with the column cap as the sole configured mathematical difference. The candidate remains held pending independent audit.
