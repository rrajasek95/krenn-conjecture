# Independent r1640 cap-4.25m attempt-2 referee

Status: **PASS_EXACT_R1640_CAP4250_DESCENDANT**.

The fresh v3 attempt-2 state is an exact strict descendant of sealed r1639. A single independent streaming scan checked both checkpoint and cache edges, preserving all 3,968,369 inherited records byte-for-byte in canonical order and adding exactly 101,342 new records. It replayed 414,162,800 literal terms across all 4,069,711 final columns, found target coefficient 1 and zero pairing failures, and matched the producer/provider fingerprints.

The endpoint is exactly r1640 with one r1640 record, 4,069,711 columns, and support 76,616. Independent endpoint hashes are checkpoint `12f79c86...` and cache `1d7ce92a...`. The frozen engine used native 210 seconds and wrapper 240 seconds; it completed atomically in 196.456243/198.715821 seconds at 21,528,480 KiB with no breach or temporary output. Relative to failed attempt 1, the solver command changes only native wall 150→210 and the wrapper changes only hard wall 180→240.

All v2/v3 approval bindings are pinned, and failed attempt 1 remains excluded with zero accepted coverage and reuse forbidden. This audit accepts only the exact r1639→r1640 promotion. It does not authorize r1641 or claim a terminal D12 certificate or the conjecture.
