# Rep1 remaining-161 exact-Q canonical input census

Status: **PASS exact enumeration; no additional ideal was run.**

The sealed minor-quotient construction has 972 refined charts.  Exact common-color `S3` quotienting gives 162 groups of six raw charts each.  One group is the already closed all-equal-y exact-Q chart, leaving 161 groups.

The allowed renamings were audited, not inferred from source byte differences.  Source block labels and stored orientations are retained.  The pure GHZ normalization forces any local color relabelings to be one common permutation on all eight sites.  An exhaustive `8!` graph test finds no nonidentity vertex automorphism preserving the fixed identity edges and supported source graph.  Therefore the existing 162 common-`S3` representatives are the exact polynomial groups under the stated source-faithful contract; there is no further group collapse.  Regeneration over `Q` gives 162 distinct canonical source hashes and byte-matches the closed source hash.

No inputs were persisted beyond the JSON ledger.  Materializing all remaining inputs would use exactly `286,969,760` bytes (`273.676 MiB`); on-demand generation needs at most `1,841,468` source bytes.  Naively scaling the closed chart's `9.3076` seconds gives `24.98` sequential minutes, but this is not evidence that Gröbner complexity is equal.

`HELD_RESOURCE_GATE.json` selects the lexicographically first of the 27 maximum-size remaining groups.  It is explicitly non-launchable until an independent audit and new manager clearance, and permits at most one 240-second/8-GiB exact-Q lane with no continuation.
