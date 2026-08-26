# Independent rep2 corrected contraction and modular-pilot referee

Status: **PASS design / APPROVE_HELD one modular diagnostic / zero runs.**

The support ledger independently regenerates the same 13 matchings. The corrected cap03/star4 carrier is `A06^T K [A23^T|A35]`, not the superseded A04 carrier. Eliminating `A56=-A57 A26^T` gives the two reduced guard matrices. Both y/z inputs independently parse as 91 variables and 6,577 generators; the nine A06 variables are absent. The chart ledger is an exact partition of 972 raw charts into 162 size-six colour orbits, 81 y and 81 z.

The modular source is byte-for-byte the Q source with only the unique ring substitution and solver/status epilogue. The runner is pinned at SHA `845bf792...`; it refuses missing/malformed dual clearances or an existing result, writes its result atomically, enforces the native 180-second and direct-child 8-GiB libproc gates, and is to be invoked only through the pinned external 195-second `gtimeout` wrapper.

The acceptance payload is sealed here but deliberately absent from the producer directory. No result, producer clearance, modular run, exact-Q run, second lane, or closure exists. A future launch still requires explicit manager/resource clearance.
