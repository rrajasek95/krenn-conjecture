# Round 1343 cap-only gate: PASS

The independently sealed Poincaré input is round 1342 at 1,491,824 columns/support 1,954, with checkpoint `7e3174c8...`, cache `852c711f...`, audit result `bd17df82...`, and manifest `7dea99f6...`.

The no-portfolio gate ran unchanged sealed v4.1 hierarchical cold/rare twice from independent APFS clones, at caps 1.5M and 1.75M. Both produced round 1343 with 1,496,171 columns (+4,347), support 1,949, and 1,045 new support rows. The checkpoint (`d2dbdee8...`) and cache (`d5517dfd...`) are byte-identical, every structural result field checked by `validate.py` agrees, and the normalized commands differ only at `--column-cap 1500000` versus `1750000`.

The control/candidate took 45.111/44.599 seconds; maximum measured RSS was 20,990,512 KiB under the 36 GiB gate. Both stopped exactly at the round-1343 cap. No portfolio, continuation, or production-source mutation occurred. Incomplete round-cap results intentionally emit no dual file; identical persisted checkpoint/cache bytes and the full structural result comparison are the accepted equivalence certificate.
