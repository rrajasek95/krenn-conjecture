# Independent D12 round-1601 cap-equivalence audit

Status: `PASS_EXACT_DIRECT_CAP3250_TO_CAP3500_EQUIVALENCE`.

Fresh control and candidate clones of the independently sealed round-1600 state were advanced by exactly one round with column caps 3,250,000 and 3,500,000.  The round-1601 records and all normalized non-timing semantics agree exactly; the sole normalized command difference is the column-cap value.

Both lanes produce byte-identical checkpoint and vector-cache files.  The accepted candidate endpoint has 3,104,755 columns, support 6,070, checkpoint SHA-256 `83955dbcc460c5fe39623e25b8337eb80bcfc9921eeafb4c1a887cfa6f5abb01`, and cache SHA-256 `c9d850754e9451015a3bf4fa6b51d6f0bb8c3ecdaeecbdef456abaa5fae7b046`.

Both watchdogs pass with return code zero, clean atomic outputs, no breach, frozen source/binary/watchdog pins, and no dual output.  Maximum watchdog elapsed time is 97.966498 s (<150 s); maximum peak RSS is 22,234,304 KiB (<36 GiB).

The candidate is accepted as an exact restart state only.  This audit launches no continuation and makes no global-closure claim.
